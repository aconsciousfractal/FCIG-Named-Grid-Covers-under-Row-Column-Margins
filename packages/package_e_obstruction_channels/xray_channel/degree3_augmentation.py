#!/usr/bin/env python3
"""Exact degree-three augmentation of the robust P21 participating fiber."""
from __future__ import annotations

import hashlib
import itertools
import json
import platform
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

from sympy import Matrix, ZZ
from sympy.matrices.normalforms import hermite_normal_form, smith_normal_form

from placement_quotient import (
    action_permutations,
    graph_components,
    target_symmetries,
)
from robust_p21_quotient import (
    Context,
    QUAD,
    canonical,
    direct_graph,
    direct_repairs,
    node_orbits,
    pair_orbits,
    scale,
    sparse,
    sub,
)
from short_dual_separators import (
    invariant_equations,
    orbits,
    placement_action,
    rank,
    target_fixed_gauge_rank,
)
from verify_coarea_next import model_from_locked


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent.parent
OUTPUT = PROJECT / "reports" / "P42_DEGREE3_AUGMENTATION_ANALYSIS.json"
PREREGISTRATION = HERE / "DEGREE3_AUGMENTATION_PREREGISTRATION.md"
SEPARATOR_COORDINATES = (33, 35, 36, 39, 40, 42, 45, 46)
CANONICAL_REPAIR_ORBITS = (0, 2)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest_json(value: object) -> str:
    payload = json.dumps(
        value,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def dot(left: Iterable[int], right: Iterable[int]) -> int:
    return sum(a * b for a, b in zip(left, right))


def add_xrays(values: Iterable[tuple[int, ...]]) -> tuple[int, ...]:
    frozen = tuple(values)
    return tuple(sum(row) for row in zip(*frozen))


def primitive_support_three(
    context: Context,
) -> tuple[
    tuple[tuple[int, ...], ...],
    dict[tuple[int, int, int], tuple[tuple[int, ...], ...]],
]:
    xrays = tuple(
        {
            placed: context.model.xray(placed)
            for placed in values
        }
        for values in context.active
    )
    all_moves: set[tuple[int, ...]] = set()
    by_positions: dict[
        tuple[int, int, int],
        tuple[tuple[int, ...], ...],
    ] = {}
    for positions in itertools.combinations(range(len(context.active)), 3):
        buckets: dict[
            tuple[int, ...],
            list[tuple[object, ...]],
        ] = defaultdict(list)
        for assignment in itertools.product(
            *(context.active[position] for position in positions)
        ):
            key = add_xrays(
                xrays[position][placed]
                for position, placed in zip(positions, assignment)
            )
            buckets[key].append(assignment)
        moves: set[tuple[int, ...]] = set()
        for assignments in buckets.values():
            for old, new in itertools.combinations(assignments, 2):
                if any(left == right for left, right in zip(old, new)):
                    continue
                vector = [0] * context.columns
                for position, placed in zip(positions, new):
                    vector[context.column_index[position][placed]] += 1
                for position, placed in zip(positions, old):
                    vector[context.column_index[position][placed]] -= 1
                moves.add(canonical(tuple(vector)))
        frozen = tuple(sorted(moves))
        by_positions[positions] = frozen
        all_moves.update(frozen)
    return tuple(sorted(all_moves)), by_positions


def apply_coordinate_permutation(
    vector: tuple[int, ...],
    permutation: tuple[int, ...],
) -> tuple[int, ...]:
    image = [0] * len(vector)
    for coordinate, value in enumerate(vector):
        image[permutation[coordinate]] = value
    return tuple(image)


def vector_orbits(
    vectors: tuple[tuple[int, ...], ...],
    permutations: tuple[tuple[int, ...], ...],
) -> tuple[list[list[int]], list[int]]:
    lookup = {vector: index for index, vector in enumerate(vectors)}
    unseen = set(range(len(vectors)))
    output: list[list[int]] = []
    orbit_by_vector = [-1] * len(vectors)
    while unseen:
        start = min(unseen)
        orbit = sorted(
            {
                lookup[
                    canonical(
                        apply_coordinate_permutation(
                            vectors[start],
                            permutation,
                        )
                    )
                ]
                for permutation in permutations
            }
        )
        identifier = len(output)
        for index in orbit:
            orbit_by_vector[index] = identifier
        unseen.difference_update(orbit)
        output.append(orbit)
    if any(value < 0 for value in orbit_by_vector):
        raise AssertionError("move action did not cover all moves")
    return output, orbit_by_vector


def edge_orbits(
    edges: list[tuple[int, int]],
    permutations: tuple[tuple[int, ...], ...],
) -> list[list[int]]:
    lookup = {edge: index for index, edge in enumerate(edges)}
    unseen = set(range(len(edges)))
    output = []
    while unseen:
        start = min(unseen)
        left, right = edges[start]
        orbit = sorted(
            {
                lookup[
                    tuple(
                        sorted(
                            (
                                permutation[left],
                                permutation[right],
                            )
                        )
                    )
                ]
                for permutation in permutations
            }
        )
        unseen.difference_update(orbit)
        output.append(orbit)
    return output


def lattice_data(
    context: Context,
    moves: tuple[tuple[int, ...], ...],
) -> dict[str, object]:
    coordinates = tuple(
        context.kernel_coordinates(move)
        for move in moves
    )
    matrix = Matrix(
        context.kernel_rank,
        len(coordinates),
        lambda row, column: coordinates[column][row],
    )
    basis = hermite_normal_form(matrix)
    lattice_rank = basis.cols
    if lattice_rank != matrix.rank():
        raise AssertionError("Hermite column basis rank mismatch")
    diagonal = smith_normal_form(basis, domain=ZZ)
    factors = [
        abs(int(diagonal[index, index]))
        for index in range(min(diagonal.rows, diagonal.cols))
        if diagonal[index, index]
    ]
    return {
        "generator_count": len(moves),
        "rank": lattice_rank,
        "free_quotient_rank": context.kernel_rank - lattice_rank,
        "smith_factors": factors,
        "nontrivial_torsion_factors": [
            value for value in factors if value > 1
        ],
    }


def graph_edges_by_degree(
    nodes,
    accepted: set[int],
) -> tuple[list[set[int]], dict[int, list[tuple[int, int]]]]:
    adjacency = [set() for _ in nodes]
    by_degree = {degree: [] for degree in sorted(accepted)}
    for left, right in itertools.combinations(range(len(nodes)), 2):
        degree = sum(a != b for a, b in zip(nodes[left], nodes[right]))
        if degree not in accepted:
            continue
        adjacency[left].add(right)
        adjacency[right].add(left)
        by_degree[degree].append((left, right))
    return adjacency, by_degree


def adjacency_from_selected_moves(
    context: Context,
    selected: set[tuple[int, ...]],
) -> tuple[list[set[int]], list[tuple[int, int]]]:
    adjacency = direct_graph(context.nodes, {1, 2})
    added = []
    for left, right in itertools.combinations(range(len(context.nodes)), 2):
        if sum(
            a != b
            for a, b in zip(context.nodes[left], context.nodes[right])
        ) != 3:
            continue
        difference = canonical(
            sub(context.node_vectors[right], context.node_vectors[left])
        )
        if difference not in selected:
            continue
        adjacency[left].add(right)
        adjacency[right].add(left)
        added.append((left, right))
    return adjacency, added


def component_summary(
    adjacency: list[set[int]],
    energy: list[int],
    tilings: list[int],
    formerly_trapped: list[int],
) -> dict[str, object]:
    components, component_by_node = graph_components(adjacency)
    tiling_components = {
        component_by_node[node] for node in tilings
    }
    reached = [
        node
        for node in formerly_trapped
        if component_by_node[node] in tiling_components
    ]
    profiles = []
    for identifier, component in enumerate(components):
        profiles.append(
            {
                "component": identifier,
                "nodes": component,
                "tiling_nodes": [
                    node for node in component if energy[node] == 0
                ],
                "positive_energy_nodes": [
                    node for node in component if energy[node] > 0
                ],
                "formerly_trapped_nodes": [
                    node for node in component if node in formerly_trapped
                ],
            }
        )
    return {
        "components": len(components),
        "component_partition": components,
        "component_profiles": profiles,
        "formerly_trapped_reaching_tiling": reached,
        "formerly_trapped_reaching_tiling_count": len(reached),
        "full_fiber_connected": len(components) == 1,
    }


def invariant_dual_data(
    context: Context,
    moves: tuple[tuple[int, ...], ...],
    placement_orbits: list[list[int]],
    gauge_rank: int,
) -> dict[str, int]:
    equations = [
        [
            sum(move[coordinate] for coordinate in orbit)
            for orbit in placement_orbits
        ]
        for move in moves
    ]
    equation_rank = rank(equations)
    return {
        "target_invariant_ambient_rank": len(placement_orbits),
        "target_invariant_move_equation_rank": equation_rank,
        "target_invariant_move_annihilator_rank": (
            len(placement_orbits) - equation_rank
        ),
        "target_invariant_gauge_rank": gauge_rank,
        "target_invariant_quotient_dual_rank": (
            len(placement_orbits) - equation_rank - gauge_rank
        ),
    }


def repair_orbit_records(
    context: Context,
    repair_pairs: list[tuple[int, int]],
    repair_pair_orbits: list[list[int]],
    support_three_index: dict[tuple[int, ...], int],
    trapped_orbits: list[list[int]],
) -> tuple[list[dict[str, object]], list[set[tuple[int, ...]]]]:
    records = []
    orbit_moves = []
    for identifier, orbit in enumerate(repair_pair_orbits):
        pairs = [repair_pairs[index] for index in orbit]
        moves = {
            canonical(
                sub(
                    context.node_vectors[tiling],
                    context.node_vectors[trapped],
                )
            )
            for trapped, tiling in pairs
        }
        if not moves <= set(support_three_index):
            raise AssertionError("repair move absent from support-three census")
        representative = pairs[0]
        trapped_orbit = next(
            index
            for index, nodes in enumerate(trapped_orbits)
            if representative[0] in nodes
        )
        records.append(
            {
                "repair_orbit": identifier,
                "pair_indices": orbit,
                "pairs": [list(pair) for pair in pairs],
                "representative_pair": list(representative),
                "trapped_node_orbit": trapped_orbit,
                "move_indices": sorted(
                    support_three_index[move] for move in moves
                ),
                "move_count": len(moves),
                "changed_piece_positions": [
                    position
                    for position in range(len(QUAD))
                    if (
                        context.nodes[representative[0]][position]
                        != context.nodes[representative[1]][position]
                    )
                ],
            }
        )
        orbit_moves.append(moves)
    return records, orbit_moves


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
    base_adjacency = direct_graph(context.nodes, {1, 2})
    base_components, base_component_by_node = graph_components(base_adjacency)
    base_tiling_components = {
        base_component_by_node[node] for node in tilings
    }
    formerly_trapped = sorted(
        node
        for identifier, component in enumerate(base_components)
        if identifier not in base_tiling_components
        for node in component
    )

    actions = target_symmetries(model.target)
    node_permutations = action_permutations(context.nodes, actions)
    coordinate_permutations = placement_action(context, actions)
    placement_orbits, _ = orbits(
        context.columns,
        coordinate_permutations,
    )
    invariant_gauge_rank = target_fixed_gauge_rank(
        context,
        coordinate_permutations,
    )

    support_three, by_positions = primitive_support_three(context)
    support_three_index = {
        move: index for index, move in enumerate(support_three)
    }
    move_orbits, move_orbit_by_move = vector_orbits(
        support_three,
        coordinate_permutations,
    )

    repairs, repair_pairs = direct_repairs(
        context,
        formerly_trapped,
        tilings,
    )
    repair_pair_orbits = pair_orbits(
        repair_pairs,
        node_permutations,
    )
    trapped_orbits = node_orbits(
        formerly_trapped,
        node_permutations,
    )
    repair_records, repair_orbit_moves = repair_orbit_records(
        context,
        repair_pairs,
        repair_pair_orbits,
        support_three_index,
        trapped_orbits,
    )

    separator = tuple(
        int(coordinate in SEPARATOR_COORDINATES)
        for coordinate in range(context.columns)
    )
    base_moves = tuple(context.moves)
    subset_records = []
    for size in range(4):
        for subset in itertools.combinations(range(3), size):
            selected = set().union(
                *(repair_orbit_moves[index] for index in subset)
            ) if subset else set()
            augmented_moves = tuple(sorted(set(base_moves) | selected))
            lattice = lattice_data(context, augmented_moves)
            invariant = invariant_dual_data(
                context,
                augmented_moves,
                placement_orbits,
                invariant_gauge_rank,
            )
            adjacency, added_edges = adjacency_from_selected_moves(
                context,
                selected,
            )
            graph = component_summary(
                adjacency,
                energy,
                tilings,
                formerly_trapped,
            )
            separator_values = sorted(
                {dot(separator, move) for move in selected}
            )
            subset_records.append(
                {
                    "selected_repair_orbits": list(subset),
                    "selected_move_count": len(selected),
                    "selected_move_indices": sorted(
                        support_three_index[move] for move in selected
                    ),
                    "added_fiber_edges": [
                        list(edge) for edge in added_edges
                    ],
                    "added_fiber_edge_count": len(added_edges),
                    "lattice": lattice,
                    "invariant_dual": invariant,
                    "old_separator_values_on_selected_moves": separator_values,
                    "old_separator_killed": bool(
                        selected
                        and any(value != 0 for value in separator_values)
                    ),
                    "graph": graph,
                }
            )

    subset_by_key = {
        tuple(record["selected_repair_orbits"]): record
        for record in subset_records
    }
    canonical_record = subset_by_key[CANONICAL_REPAIR_ORBITS]
    all_record = subset_by_key[(0, 1, 2)]
    redundancy_fields = {
        "move_lattice_rank": (
            canonical_record["lattice"]["rank"]
            == all_record["lattice"]["rank"]
        ),
        "smith_factors": (
            canonical_record["lattice"]["smith_factors"]
            == all_record["lattice"]["smith_factors"]
        ),
        "target_invariant_quotient_dual_rank": (
            canonical_record["invariant_dual"][
                "target_invariant_quotient_dual_rank"
            ]
            == all_record["invariant_dual"][
                "target_invariant_quotient_dual_rank"
            ]
        ),
        "component_partition": (
            canonical_record["graph"]["component_partition"]
            == all_record["graph"]["component_partition"]
        ),
        "formerly_trapped_reaching_tiling": (
            canonical_record["graph"][
                "formerly_trapped_reaching_tiling_count"
            ]
            == all_record["graph"][
                "formerly_trapped_reaching_tiling_count"
            ]
        ),
    }
    third_redundant = all(redundancy_fields.values())
    canonical_repairs_all = (
        canonical_record["graph"][
            "formerly_trapped_reaching_tiling_count"
        ]
        == len(formerly_trapped)
    )
    all_repairs_all = (
        all_record["graph"][
            "formerly_trapped_reaching_tiling_count"
        ]
        == len(formerly_trapped)
    )
    if canonical_repairs_all and third_redundant:
        branch = "TWO_PROTOTYPES_SUFFICE_THIRD_REDUNDANT"
    elif canonical_repairs_all:
        branch = "TWO_PROTOTYPES_REPAIR_THIRD_ADDS_STRUCTURE"
    elif all_repairs_all:
        branch = "ALL_THREE_REPAIR_ORBITS_REQUIRED"
    else:
        branch = "REPAIR_ORBITS_INSUFFICIENT_FOR_ALL_TRAPPED"

    full_moves = tuple(sorted(set(base_moves) | set(support_three)))
    full_lattice = lattice_data(context, full_moves)
    full_invariant = invariant_dual_data(
        context,
        full_moves,
        placement_orbits,
        invariant_gauge_rank,
    )
    full_adjacency, full_edges_by_degree = graph_edges_by_degree(
        context.nodes,
        {1, 2, 3},
    )
    full_graph = component_summary(
        full_adjacency,
        energy,
        tilings,
        formerly_trapped,
    )
    degree_three_edges = full_edges_by_degree[3]
    degree_three_edge_orbits = edge_orbits(
        degree_three_edges,
        node_permutations,
    )
    degree_three_edge_move_indices = [
        support_three_index[
            canonical(
                sub(
                    context.node_vectors[right],
                    context.node_vectors[left],
                )
            )
        ]
        for left, right in degree_three_edges
    ]

    repairing_subsets = [
        record
        for record in subset_records
        if record["graph"][
            "formerly_trapped_reaching_tiling_count"
        ]
        == len(formerly_trapped)
    ]
    minimum_repair_orbit_count = min(
        len(record["selected_repair_orbits"])
        for record in repairing_subsets
    )
    minimal_repair_subsets = [
        record["selected_repair_orbits"]
        for record in repairing_subsets
        if len(record["selected_repair_orbits"])
        == minimum_repair_orbit_count
    ]
    maximum_repair_family_rank = max(
        record["lattice"]["rank"]
        for record in subset_records
    )
    maximum_rank_subsets = [
        record["selected_repair_orbits"]
        for record in subset_records
        if record["lattice"]["rank"] == maximum_repair_family_rank
    ]
    full_partition_subsets = [
        record["selected_repair_orbits"]
        for record in subset_records
        if record["graph"]["component_partition"]
        == full_graph["component_partition"]
    ]
    minimum_full_partition_orbit_count = min(
        map(len, full_partition_subsets)
    )
    minimal_full_partition_subsets = [
        subset
        for subset in full_partition_subsets
        if len(subset) == minimum_full_partition_orbit_count
    ]

    support_three_sparse = [
        sparse(move) for move in support_three
    ]
    result = {
        "piece_indices": list(QUAD),
        "piece_ids": [model.ids[index] for index in QUAD],
        "fiber_nodes": len(context.nodes),
        "tiling_nodes": tilings,
        "energy": energy,
        "formerly_trapped_nodes": formerly_trapped,
        "trapped_node_orbits": trapped_orbits,
        "participating_columns": context.columns,
        "ambient_kernel_rank": context.kernel_rank,
        "target_automorphism_order": len(actions),
        "target_automorphisms": [name for name, _ in actions],
        "placement_orbit_sizes": [
            len(orbit) for orbit in placement_orbits
        ],
        "base": {
            "support_one_moves": len(context.support_one),
            "support_two_moves": len(context.support_two),
            "move_lattice": lattice_data(context, base_moves),
            "invariant_dual": invariant_dual_data(
                context,
                base_moves,
                placement_orbits,
                invariant_gauge_rank,
            ),
            "graph": component_summary(
                base_adjacency,
                energy,
                tilings,
                formerly_trapped,
            ),
        },
        "support_three": {
            "move_count": len(support_three),
            "counts_by_changed_piece_positions": {
                "-".join(map(str, positions)): len(moves)
                for positions, moves in by_positions.items()
            },
            "move_set_sha256": digest_json(support_three_sparse),
            "moves_sparse": support_three_sparse,
            "target_move_orbits": move_orbits,
            "target_move_orbit_count": len(move_orbits),
            "target_move_orbit_sizes": [
                len(orbit) for orbit in move_orbits
            ],
            "move_orbit_by_move": move_orbit_by_move,
        },
        "repair_family": {
            "rho_distribution": dict(
                sorted(
                    Counter(
                        str(record["rho"]) for record in repairs
                    ).items()
                )
            ),
            "minimizing_repair_pairs": [
                list(pair) for pair in repair_pairs
            ],
            "repair_pair_orbits": repair_records,
            "canonical_two_prototype_orbits": list(
                CANONICAL_REPAIR_ORBITS
            ),
            "all_subset_results": subset_records,
            "minimum_orbit_count_for_all_trapped_reaching_tiling": (
                minimum_repair_orbit_count
            ),
            "minimal_repair_subsets": minimal_repair_subsets,
            "maximum_repair_family_lattice_rank": (
                maximum_repair_family_rank
            ),
            "maximum_rank_subsets": maximum_rank_subsets,
            "minimum_orbit_count_for_complete_G3_partition": (
                minimum_full_partition_orbit_count
            ),
            "minimal_subsets_reaching_complete_G3_partition": (
                minimal_full_partition_subsets
            ),
            "third_orbit_redundancy_checks": redundancy_fields,
            "third_orbit_structurally_redundant": third_redundant,
        },
        "complete_degree_at_most_three": {
            "move_lattice": full_lattice,
            "invariant_dual": full_invariant,
            "graph_edge_counts_by_degree": {
                str(degree): len(edges)
                for degree, edges in full_edges_by_degree.items()
            },
            "graph": full_graph,
            "degree_three_edges": [
                list(edge) for edge in degree_three_edges
            ],
            "degree_three_edge_orbits": degree_three_edge_orbits,
            "degree_three_edge_orbit_count": len(
                degree_three_edge_orbits
            ),
            "degree_three_edge_move_indices": (
                degree_three_edge_move_indices
            ),
            "degree_three_edge_move_orbit_ids": [
                move_orbit_by_move[index]
                for index in degree_three_edge_move_indices
            ],
            "component_partition_reached_by_all_repair_orbits": (
                all_record["graph"]["component_partition"]
                == full_graph["component_partition"]
            ),
        },
        "interpretation_branch": branch,
        "conclusion": (
            "repair-orbit comparison, full participating degree-three "
            "lattice and direct G<=3 graph completed independently"
        ),
        "nonclaims": [
            "finite participating robust P21 fiber only",
            "repair-family minimality only within the three frozen orbits",
            "not a full-placement or all-right-hand-side Markov basis",
            "not a public claim or paper-readiness decision",
        ],
        "runtime_seconds": round(
            time.perf_counter() - started,
            6,
        ),
    }
    return result


def validate(primary: dict[str, object]) -> None:
    if (
        primary["fiber_nodes"],
        len(primary["tiling_nodes"]),
        len(primary["formerly_trapped_nodes"]),
        primary["participating_columns"],
        primary["ambient_kernel_rank"],
        primary["target_automorphism_order"],
    ) != (32, 8, 16, 72, 60, 8):
        raise AssertionError("frozen robust P21 scope changed")
    repair = primary["repair_family"]
    if repair["rho_distribution"] != {"3": 16}:
        raise AssertionError("repair-degree distribution changed")
    if [
        row["representative_pair"]
        for row in repair["repair_pair_orbits"]
    ] != [[1, 0], [1, 27], [3, 0]]:
        raise AssertionError("frozen repair-orbit ordering changed")
    if len(repair["all_subset_results"]) != 8:
        raise AssertionError("repair-orbit subset census incomplete")
    support_three = primary["support_three"]
    if not support_three["move_count"]:
        raise AssertionError("degree-three move census is empty")
    full = primary["complete_degree_at_most_three"]
    if full["move_lattice"]["rank"] < primary["base"]["move_lattice"]["rank"]:
        raise AssertionError("degree-three augmentation lowered lattice rank")
    if (
        full["invariant_dual"]["target_invariant_quotient_dual_rank"]
        > primary["base"]["invariant_dual"][
            "target_invariant_quotient_dual_rank"
        ]
    ):
        raise AssertionError("degree-three augmentation created dual rank")


def main() -> int:
    started = time.perf_counter()
    primary = analyse()
    validate(primary)
    output = {
        "schema_version": "p42.degree3_augmentation.v1",
        "status": "PASS",
        "scope": {
            "library": "P21",
            "row": list(QUAD),
            "lattice": "72 participating named placements",
            "moves": "all primitive support-at-most-three relations",
            "graph": "complete 32-node fiber under G<=3",
            "minimality": "exact within three frozen repair-pair orbits",
        },
        "preregistration": {
            "path": str(PREREGISTRATION.relative_to(PROJECT)).replace(
                "\\",
                "/",
            ),
            "sha256": sha256(PREREGISTRATION),
        },
        "inputs": {
            "p21_path": (
                "packages/package_c_comparative_hypergraphs/"
                "specimens/p21_locked.json"
            ),
            "p21_sha256": (
                "6a2f4ed590f50831f04f083656c3b7f0067cca898c5617773fecf38481e42b8f"
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
    full = primary["complete_degree_at_most_three"]
    canonical = next(
        record
        for record in primary["repair_family"]["all_subset_results"]
        if record["selected_repair_orbits"] == [0, 2]
    )
    print(
        "PASS: "
        f"branch={primary['interpretation_branch']}; "
        f"support3={primary['support_three']['move_count']}; "
        f"full-rank/components="
        f"{full['move_lattice']['rank']}/"
        f"{full['graph']['components']}; "
        f"canonical-repaired="
        f"{canonical['graph']['formerly_trapped_reaching_tiling_count']}/16; "
        f"{output['runtime_seconds']:.3f}s"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
