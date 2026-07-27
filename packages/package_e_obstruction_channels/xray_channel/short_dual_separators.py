#!/usr/bin/env python3
"""Extract a shortest target-invariant dual separator for robust P21."""
from __future__ import annotations

import hashlib
import itertools
import json
import math
import platform
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

from sympy.polys.matrices.normalforms import smith_normal_decomp

from placement_quotient import (
    action_permutations,
    graph_components,
    shape_key,
    target_symmetries,
)
from robust_p21_quotient import (
    QUAD,
    Context,
    direct_graph,
    integer_matrix,
    matvec,
    matrix_rows,
    sub,
)
from verify_coarea_next import model_from_locked


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent.parent
OUTPUT = PROJECT / "reports" / "P42_SHORT_DUAL_SEPARATOR_ANALYSIS.json"
PREREGISTRATION = HERE / "SHORT_DUAL_SEPARATOR_PREREGISTRATION.md"
METHOD_AUDIT = PROJECT / "reports" / "P42_P39_P41_METHOD_REUSE_AUDIT.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dot(left: Iterable[int], right: Iterable[int]) -> int:
    return sum(a * b for a, b in zip(left, right))


def rank(rows: list[list[int]]) -> int:
    return int(integer_matrix(rows).rank()) if rows else 0


def permutation_inverse(permutation: tuple[int, ...]) -> tuple[int, ...]:
    inverse = [0] * len(permutation)
    for index, image in enumerate(permutation):
        inverse[image] = index
    return tuple(inverse)


def placement_action(
    context: Context,
    actions,
) -> tuple[tuple[int, ...], ...]:
    permutations = []
    for name, action in actions:
        permutation = []
        for position, values in enumerate(context.active):
            lookup = {
                shape_key(placed): context.column_index[position][placed]
                for placed in values
            }
            for placed in values:
                image = frozenset(
                    action(row, col) for row, col in placed
                )
                key = shape_key(image)
                if key not in lookup:
                    raise AssertionError(
                        f"target action {name} leaves participating placements"
                    )
                permutation.append(lookup[key])
        if len(set(permutation)) != context.columns:
            raise AssertionError(
                f"target action {name} is not a placement permutation"
            )
        permutations.append(tuple(permutation))
    return tuple(permutations)


def orbits(
    count: int,
    permutations: tuple[tuple[int, ...], ...],
) -> tuple[list[list[int]], list[int]]:
    unseen = set(range(count))
    output = []
    orbit_by_coordinate = [-1] * count
    while unseen:
        start = min(unseen)
        orbit = sorted({permutation[start] for permutation in permutations})
        identifier = len(output)
        for coordinate in orbit:
            if orbit_by_coordinate[coordinate] not in (-1, identifier):
                raise AssertionError("placement orbit collision")
            orbit_by_coordinate[coordinate] = identifier
        unseen.difference_update(orbit)
        output.append(orbit)
    if any(value < 0 for value in orbit_by_coordinate):
        raise AssertionError("placement action did not cover the catalogue")
    return output, orbit_by_coordinate


def coordinate_record(
    context: Context,
    coordinate: int,
) -> dict[str, object]:
    position = max(
        index
        for index, offset in enumerate(context.offsets)
        if offset <= coordinate
    )
    local = coordinate - context.offsets[position]
    placed = context.active[position][local]
    return {
        "coordinate": coordinate,
        "piece_position": position,
        "piece_index": QUAD[position],
        "piece_id": context.model.ids[QUAD[position]],
        "cells": [list(cell) for cell in sorted(placed)],
    }


def target_fixed_gauge_rank(
    context: Context,
    permutations: tuple[tuple[int, ...], ...],
) -> int:
    rowspace_rank = rank(context.constraint_rows)
    averaged = []
    for row in context.constraint_rows:
        orbit_rows = []
        for permutation in permutations:
            inverse = permutation_inverse(permutation)
            transformed = [row[inverse[index]] for index in range(context.columns)]
            if rank(context.constraint_rows + [transformed]) != rowspace_rank:
                raise AssertionError("constraint rowspace is not target-invariant")
            orbit_rows.append(transformed)
        averaged.append(
            [
                sum(values)
                for values in zip(*orbit_rows)
            ]
        )
    return rank(averaged)


def constraint_smith(context: Context) -> tuple[int, list[int]]:
    ambient = integer_matrix(context.constraint_rows)
    diagonal, left, right = smith_normal_decomp(ambient)
    if left * ambient * right != diagonal:
        raise AssertionError("constraint Smith decomposition failed")
    rows = matrix_rows(diagonal)
    matrix_rank = sum(
        rows[index][index] != 0
        for index in range(min(diagonal.shape))
    )
    factors = [
        abs(rows[index][index])
        for index in range(matrix_rank)
    ]
    return matrix_rank, factors


def invariant_equations(
    context: Context,
    placement_orbits: list[list[int]],
) -> list[list[int]]:
    return [
        [
            sum(move[coordinate] for coordinate in orbit)
            for orbit in placement_orbits
        ]
        for move in context.moves
    ]


def expand_orbit_coefficients(
    coefficients: tuple[int, ...],
    orbit_by_coordinate: list[int],
) -> tuple[int, ...]:
    return tuple(
        coefficients[orbit_by_coordinate[coordinate]]
        for coordinate in range(len(orbit_by_coordinate))
    )


def sign_canonical(coefficients: tuple[int, ...]) -> bool:
    return next(value for value in coefficients if value) > 0


def complexity(weight: tuple[int, ...]) -> tuple[int, int, int]:
    return (
        max(map(abs, weight)),
        sum(value != 0 for value in weight),
        sum(map(abs, weight)),
    )


def search_invariant_scalar(
    context: Context,
    placement_orbits: list[list[int]],
    orbit_by_coordinate: list[int],
    tilings: list[int],
    trapped: list[int],
) -> tuple[dict[str, object], tuple[int, ...], tuple[int, ...]]:
    equations = invariant_equations(context, placement_orbits)
    counters: Counter[str] = Counter()
    separators = []
    for coefficients in itertools.product(
        (-1, 0, 1),
        repeat=len(placement_orbits),
    ):
        counters["tested"] += 1
        if not any(coefficients):
            continue
        if any(dot(row, coefficients) for row in equations):
            continue
        counters["admissible"] += 1
        if math.gcd(*map(abs, coefficients)) != 1:
            continue
        counters["primitive"] += 1
        if not sign_canonical(coefficients):
            continue
        counters["sign_canonical"] += 1
        weight = expand_orbit_coefficients(
            coefficients,
            orbit_by_coordinate,
        )
        values = [
            dot(weight, vector) for vector in context.node_vectors
        ]
        tiling_values = {values[index] for index in tilings}
        trapped_values = {values[index] for index in trapped}
        if not tiling_values.isdisjoint(trapped_values):
            continue
        counters["separators"] += 1
        separators.append(
            (
                (*complexity(weight), coefficients),
                coefficients,
                weight,
                sorted(tiling_values),
                sorted(trapped_values),
            )
        )
    if not separators:
        raise AssertionError("no invariant scalar within the frozen bound")
    separators.sort()
    best = separators[0]
    best_metric = best[0][:3]
    optimal = [
        item for item in separators if item[0][:3] == best_metric
    ]
    orbit_sizes = [len(orbit) for orbit in placement_orbits]
    if min(orbit_sizes) != 8 or best_metric != (1, 8, 8):
        raise AssertionError("short-separator optimality pattern changed")
    search = {
        "coefficient_bound": 1,
        "search_space": "all target-invariant orbit coefficients in {-1,0,1}",
        "tested": counters["tested"],
        "admissible_move_annihilators": counters["admissible"],
        "primitive": counters["primitive"],
        "sign_canonical": counters["sign_canonical"],
        "separators": counters["separators"],
        "best_complexity": list(best_metric),
        "optimal_candidates": len(optimal),
        "optimal_orbit_coefficient_tuples": [
            list(item[1]) for item in optimal
        ],
        "global_target_invariant_optimality": {
            "proved": True,
            "linfinity_lower_bound": 1,
            "support_lower_bound": min(orbit_sizes),
            "l1_lower_bound_at_optimal_support": min(orbit_sizes),
            "reason": (
                "a separating integer functional is nonzero; every target "
                "placement orbit has size eight; the returned primitive "
                "indicator attains (1,8,8)"
            ),
        },
    }
    return search, best[1], best[2]


def move_support_distribution(context: Context) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for move in context.moves:
        positions = []
        for position, offset in enumerate(context.offsets):
            width = len(context.active[position])
            if any(
                move[index]
                for index in range(offset, offset + width)
            ):
                positions.append(position)
        counts["-".join(map(str, positions))] += 1
    return dict(sorted(counts.items()))


def analyse() -> dict[str, object]:
    started = time.perf_counter()
    model = model_from_locked("p21_locked.json")
    context = Context(model)
    energy = [
        len(model.target) - len(frozenset().union(*node))
        for node in context.nodes
    ]
    tilings = [
        index for index, value in enumerate(energy) if value == 0
    ]
    edges = direct_graph(context.nodes, {1, 2})
    components, component_by_node = graph_components(edges)
    tiled_components = {
        component_by_node[index] for index in tilings
    }
    trapped = sorted(
        node
        for component, values in enumerate(components)
        if component not in tiled_components
        for node in values
    )
    live_extras = [
        index
        for index, value in enumerate(energy)
        if value > 0 and index not in trapped
    ]

    actions = target_symmetries(model.target)
    node_permutations = action_permutations(context.nodes, actions)
    placement_permutations = placement_action(context, actions)
    placement_orbits, orbit_by_coordinate = orbits(
        context.columns,
        placement_permutations,
    )
    equations = invariant_equations(context, placement_orbits)
    equation_rank = rank(equations)
    fixed_gauge_rank = target_fixed_gauge_rank(
        context,
        placement_permutations,
    )
    constraint_rank, constraint_factors = constraint_smith(context)

    search, orbit_coefficients, weight = search_invariant_scalar(
        context,
        placement_orbits,
        orbit_by_coordinate,
        tilings,
        trapped,
    )
    values = [
        dot(weight, vector) for vector in context.node_vectors
    ]
    if any(dot(weight, move) for move in context.moves):
        raise AssertionError("selected functional does not annihilate moves")
    if any(
        tuple(weight[permutation[index]] for index in range(context.columns))
        != weight
        for permutation in placement_permutations
    ):
        raise AssertionError("selected functional is not target-invariant")

    base = context.node_vectors[0]
    signatures = [
        context.quotient_class(sub(vector, base))
        for vector in context.node_vectors
    ]
    ordered = sorted(set(signatures), key=repr)
    class_id = {
        signature: index
        for index, signature in enumerate(ordered)
    }
    classes = [class_id[signature] for signature in signatures]
    class_profiles = []
    for identifier in range(len(ordered)):
        nodes = [
            index
            for index, value in enumerate(classes)
            if value == identifier
        ]
        class_values = {values[index] for index in nodes}
        if len(class_values) != 1:
            raise AssertionError("dual value varies inside a quotient class")
        class_profiles.append(
            {
                "class_id": identifier,
                "nodes": nodes,
                "components": sorted(
                    {component_by_node[index] for index in nodes}
                ),
                "tiling_nodes": [
                    index for index in nodes if index in tilings
                ],
                "trapped_nodes": [
                    index for index in nodes if index in trapped
                ],
                "dual_value": next(iter(class_values)),
            }
        )

    sparse_weight = [
        {
            **coordinate_record(context, coordinate),
            "coefficient": value,
        }
        for coordinate, value in enumerate(weight)
        if value
    ]
    selected_orbits = [
        index
        for index, value in enumerate(orbit_coefficients)
        if value
    ]
    if len(selected_orbits) != 1:
        raise AssertionError("expected a single-orbit indicator")
    selected_orbit = selected_orbits[0]
    complement = next(
        index
        for index, orbit in enumerate(placement_orbits)
        if index != selected_orbit
        and {
            coordinate_record(context, coordinate)["piece_position"]
            for coordinate in orbit
        }
        == {
            coordinate_record(
                context,
                placement_orbits[selected_orbit][0],
            )["piece_position"]
        }
    )
    piece_position = int(
        coordinate_record(
            context,
            placement_orbits[selected_orbit][0],
        )["piece_position"]
    )
    piece_row = tuple(context.constraint_rows[piece_position])
    complement_weight = tuple(
        int(coordinate in placement_orbits[complement])
        for coordinate in range(context.columns)
    )
    if tuple(a + b for a, b in zip(weight, complement_weight)) != piece_row:
        raise AssertionError("complement is not the piece-count gauge")

    trapped_orbits = []
    unseen = set(trapped)
    while unseen:
        start = min(unseen)
        orbit = sorted(
            {permutation[start] for permutation in node_permutations}
        )
        if not set(orbit) <= set(trapped):
            raise AssertionError("trapped family not target-invariant")
        unseen.difference_update(orbit)
        trapped_orbits.append(orbit)

    separation_matrix = [
        [
            values[trapped_node] != values[tiling]
            for tiling in tilings
        ]
        for trapped_node in trapped
    ]
    if not all(map(all, separation_matrix)):
        raise AssertionError("not all trapped/tiling pairs are separated")

    move_pairs = move_support_distribution(context)
    if sum(
        count
        for pair, count in move_pairs.items()
        if str(piece_position) in pair.split("-")
    ):
        raise AssertionError("separator piece participates in a move")

    return {
        "interpretation_branch": "ONE_TARGET_INVARIANT_SCALAR",
        "piece_indices": list(QUAD),
        "piece_ids": [model.ids[index] for index in QUAD],
        "fiber_nodes": len(context.nodes),
        "tiling_nodes": tilings,
        "trapped_nodes": trapped,
        "live_extra_nodes": live_extras,
        "node_energy": energy,
        "participating_columns": context.columns,
        "constraint_rows": len(context.constraint_rows),
        "constraint_rank": constraint_rank,
        "constraint_smith_factors": constraint_factors,
        "constraint_row_lattice_saturation_index": math.prod(
            value for value in constraint_factors if value > 1
        ),
        "move_lattice_rank": context.move_rank,
        "ambient_move_annihilator_rank": context.columns - context.move_rank,
        "fiber_constant_gauge_rank": constraint_rank,
        "quotient_dual_free_rank": (
            context.columns - context.move_rank - constraint_rank
        ),
        "target_automorphisms": [name for name, _ in actions],
        "target_automorphism_order": len(actions),
        "participating_placement_orbits": [
            {
                "orbit_id": identifier,
                "size": len(orbit),
                "coordinates": orbit,
                "piece_positions": sorted(
                    {
                        int(coordinate_record(context, coordinate)["piece_position"])
                        for coordinate in orbit
                    }
                ),
                "placements": [
                    coordinate_record(context, coordinate)
                    for coordinate in orbit
                ],
            }
            for identifier, orbit in enumerate(placement_orbits)
        ],
        "placement_orbit_sizes": [
            len(orbit) for orbit in placement_orbits
        ],
        "target_invariant_ambient_rank": len(placement_orbits),
        "target_invariant_move_equation_rank": equation_rank,
        "target_invariant_move_annihilator_rank": (
            len(placement_orbits) - equation_rank
        ),
        "target_invariant_gauge_rank": fixed_gauge_rank,
        "target_invariant_quotient_dual_rank": (
            len(placement_orbits) - equation_rank - fixed_gauge_rank
        ),
        "move_changed_piece_position_distribution": move_pairs,
        "selected_piece_never_changes_under_moves": True,
        "search": search,
        "separator": {
            "name": "piece_12_second_target_orbit_indicator",
            "coefficient_domain": "Z",
            "orbit_coefficients": list(orbit_coefficients),
            "selected_placement_orbit": selected_orbit,
            "full_weight_vector": list(weight),
            "sparse_weight_vector": sparse_weight,
            "primitive_gcd": math.gcd(*map(abs, weight)),
            "sign_canonical": sign_canonical(orbit_coefficients),
            "linfinity_norm": complexity(weight)[0],
            "support": complexity(weight)[1],
            "l1_norm": complexity(weight)[2],
            "move_values": [dot(weight, move) for move in context.moves],
            "all_144_move_values_zero": True,
            "target_action_images": [
                list(weight) for _ in placement_permutations
            ],
            "target_fixed": True,
            "node_values": values,
            "tiling_value_set": sorted({values[index] for index in tilings}),
            "trapped_value_set": sorted({values[index] for index in trapped}),
            "live_extra_value_set": sorted(
                {values[index] for index in live_extras}
            ),
            "trapped_orbit_value_sets": [
                sorted({values[index] for index in orbit})
                for orbit in trapped_orbits
            ],
            "distinguishes_trapped_node_orbits": (
                len(
                    {
                        tuple(
                            sorted({values[index] for index in orbit})
                        )
                        for orbit in trapped_orbits
                    }
                )
                == len(trapped_orbits)
            ),
            "separation_matrix": separation_matrix,
            "separated_trapped_tiling_pairs": sum(
                sum(row) for row in separation_matrix
            ),
            "total_trapped_tiling_pairs": len(trapped) * len(tilings),
            "class_profiles": class_profiles,
            "trapped_class_value_set": sorted(
                {
                    profile["dual_value"]
                    for profile in class_profiles
                    if profile["trapped_nodes"]
                }
            ),
            "live_class_value_set": sorted(
                {
                    profile["dual_value"]
                    for profile in class_profiles
                    if profile["tiling_nodes"]
                }
            ),
            "gauge_complement": {
                "complement_placement_orbit": complement,
                "relation": (
                    "selected indicator + complement indicator "
                    "= selected-piece count row"
                ),
                "selected_piece_position": piece_position,
                "selected_piece_index": QUAD[piece_position],
                "selected_piece_id": model.ids[QUAD[piece_position]],
            },
        },
        "trapped_node_orbits": trapped_orbits,
        "conclusion": (
            "the support-at-most-two lattice never changes piece 12; its two "
            "target placement orbits are exactly the live and trapped channels"
        ),
        "nonclaims": [
            "finite certificate for the participating robust P21 fiber only",
            "not a universal P21 or geomagic invariant",
            "not a degree-three generating or Markov-basis theorem",
            "not a public claim or paper-readiness decision",
        ],
        "runtime_seconds": round(time.perf_counter() - started, 6),
    }


def validate(primary: dict[str, object]) -> None:
    expected = {
        "interpretation_branch": "ONE_TARGET_INVARIANT_SCALAR",
        "fiber_nodes": 32,
        "participating_columns": 72,
        "constraint_rank": 12,
        "move_lattice_rank": 34,
        "ambient_move_annihilator_rank": 38,
        "quotient_dual_free_rank": 26,
        "target_automorphism_order": 8,
        "target_invariant_ambient_rank": 9,
        "target_invariant_move_equation_rank": 2,
        "target_invariant_move_annihilator_rank": 7,
        "target_invariant_gauge_rank": 6,
        "target_invariant_quotient_dual_rank": 1,
    }
    for key, value in expected.items():
        if primary[key] != value:
            raise AssertionError(f"frozen field changed: {key}")
    separator = primary["separator"]
    if not isinstance(separator, dict):
        raise AssertionError("separator record missing")
    if (
        separator["linfinity_norm"],
        separator["support"],
        separator["l1_norm"],
        separator["separated_trapped_tiling_pairs"],
    ) != (1, 8, 8, 128):
        raise AssertionError("short separator certificate changed")


def main() -> int:
    started = time.perf_counter()
    primary = analyse()
    validate(primary)
    output = {
        "schema_version": "p42.short_dual_separator.v1",
        "status": "PASS",
        "scope": {
            "library": "P21",
            "row": list(QUAD),
            "lattice": "72 participating named placements",
            "moves": "all primitive support-at-most-two moves",
            "search": "target-invariant integer scalar first",
        },
        "preregistration": {
            "path": str(PREREGISTRATION.relative_to(PROJECT)).replace("\\", "/"),
            "sha256": sha256(PREREGISTRATION),
        },
        "method_reuse_audit": {
            "path": str(METHOD_AUDIT.relative_to(PROJECT)).replace("\\", "/"),
            "sha256": sha256(METHOD_AUDIT),
        },
        "inputs": {
            "p21_path": str(
                model_from_locked("p21_locked.json").source.relative_to(PROJECT)
            ).replace("\\", "/"),
            "p21_sha256": sha256(
                model_from_locked("p21_locked.json").source
            ),
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
        },
        "primary": primary,
        "runtime_seconds": round(time.perf_counter() - started, 6),
    }
    OUTPUT.write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        "PASS: "
        f"branch={primary['interpretation_branch']}; "
        f"orbits/invariant-annihilator/dual="
        f"{primary['target_invariant_ambient_rank']}/"
        f"{primary['target_invariant_move_annihilator_rank']}/"
        f"{primary['target_invariant_quotient_dual_rank']}; "
        "separator=(Linf,supp,L1)="
        f"({primary['separator']['linfinity_norm']},"
        f"{primary['separator']['support']},"
        f"{primary['separator']['l1_norm']}); "
        f"pairs={primary['separator']['separated_trapped_tiling_pairs']}/128; "
        f"{output['runtime_seconds']:.3f}s"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
