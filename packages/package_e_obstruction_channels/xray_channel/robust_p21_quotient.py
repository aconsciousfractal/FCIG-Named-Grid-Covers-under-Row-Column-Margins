#!/usr/bin/env python3
"""Robust P21 quotient under all participating moves of support at most two."""
from __future__ import annotations

import hashlib
import json
import platform
import time
from collections import Counter, defaultdict, deque
from itertools import combinations, product
from pathlib import Path
from typing import Iterable

from sympy import ZZ
from sympy.polys.matrices import DomainMatrix
from sympy.polys.matrices.normalforms import smith_normal_decomp

from placement_quotient import (
    action_permutations,
    graph_components,
    node_key,
    shape_key,
    target_symmetries,
)
from verify_coarea_fpt import Model, Node, Shape
from verify_coarea_next import model_from_locked


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent.parent
OUTPUT = PROJECT / "reports" / "P42_ROBUST_P21_QUOTIENT_ANALYSIS.json"
PREREGISTRATION = HERE / "ROBUST_P21_QUOTIENT_PREREGISTRATION.md"
QUAD = (4, 5, 12, 13)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def integer_matrix(rows: list[list[int]]) -> DomainMatrix:
    return DomainMatrix(
        [[ZZ(value) for value in row] for row in rows],
        (len(rows), len(rows[0])),
        ZZ,
    )


def matrix_rows(matrix: DomainMatrix) -> list[list[int]]:
    return [[int(value) for value in row] for row in matrix.to_list()]


def matvec(
    rows: Iterable[Iterable[int]],
    vector: Iterable[int],
) -> tuple[int, ...]:
    frozen = tuple(vector)
    return tuple(
        sum(value * coordinate for value, coordinate in zip(row, frozen))
        for row in rows
    )


def add(
    left: tuple[int, ...],
    right: tuple[int, ...],
) -> tuple[int, ...]:
    return tuple(a + b for a, b in zip(left, right))


def sub(
    left: tuple[int, ...],
    right: tuple[int, ...],
) -> tuple[int, ...]:
    return tuple(a - b for a, b in zip(left, right))


def scale(value: int, vector: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(value * coordinate for coordinate in vector)


def canonical(vector: tuple[int, ...]) -> tuple[int, ...]:
    return min(vector, scale(-1, vector))


def sparse(vector: tuple[int, ...]) -> list[list[int]]:
    return [
        [index, value]
        for index, value in enumerate(vector)
        if value
    ]


def distribution(values: Iterable[int | str]) -> dict[str, int]:
    counts = Counter(str(value) for value in values)
    return dict(sorted(counts.items(), key=lambda item: item[0]))


def direct_graph(
    nodes: tuple[Node, ...],
    accepted_degrees: set[int],
) -> list[set[int]]:
    edges = [set() for _ in nodes]
    for left, right in combinations(range(len(nodes)), 2):
        degree = sum(a != b for a, b in zip(nodes[left], nodes[right]))
        if degree in accepted_degrees:
            edges[left].add(right)
            edges[right].add(left)
    return edges


def primitive_moves(
    model: Model,
    active: tuple[tuple[Shape, ...], ...],
    column_index: tuple[dict[Shape, int], ...],
) -> tuple[tuple[tuple[int, ...], ...], tuple[tuple[int, ...], ...]]:
    columns = sum(len(values) for values in active)
    xrays = tuple(
        {placed: model.xray(placed) for placed in values}
        for values in active
    )
    support_one: set[tuple[int, ...]] = set()
    for position, values in enumerate(active):
        buckets: dict[tuple[int, ...], list[Shape]] = defaultdict(list)
        for placed in values:
            buckets[xrays[position][placed]].append(placed)
        for bucket in buckets.values():
            for old, new in combinations(bucket, 2):
                vector = [0] * columns
                vector[column_index[position][new]] += 1
                vector[column_index[position][old]] -= 1
                support_one.add(canonical(tuple(vector)))

    support_two: set[tuple[int, ...]] = set()
    for first, second in combinations(range(len(active)), 2):
        buckets: dict[tuple[int, ...], list[tuple[Shape, Shape]]] = defaultdict(list)
        for left, right in product(active[first], active[second]):
            key = tuple(
                a + b for a, b in zip(xrays[first][left], xrays[second][right])
            )
            buckets[key].append((left, right))
        for assignments in buckets.values():
            for old, new in combinations(assignments, 2):
                if old[0] == new[0] or old[1] == new[1]:
                    continue
                vector = [0] * columns
                vector[column_index[first][new[0]]] += 1
                vector[column_index[second][new[1]]] += 1
                vector[column_index[first][old[0]]] -= 1
                vector[column_index[second][old[1]]] -= 1
                support_two.add(canonical(tuple(vector)))
    return tuple(sorted(support_one)), tuple(sorted(support_two))


class Context:
    def __init__(self, model: Model) -> None:
        self.model = model
        self.nodes: tuple[Node, ...] = tuple(model.fiber(QUAD))
        self.active = tuple(
            tuple(
                sorted(
                    {node[position] for node in self.nodes},
                    key=shape_key,
                )
            )
            for position in range(len(QUAD))
        )
        offsets = []
        cursor = 0
        for values in self.active:
            offsets.append(cursor)
            cursor += len(values)
        self.offsets = tuple(offsets)
        self.columns = cursor
        self.column_index = tuple(
            {
                placed: offsets[position] + local
                for local, placed in enumerate(values)
            }
            for position, values in enumerate(self.active)
        )
        self.node_vectors = tuple(self.vector(node) for node in self.nodes)
        self.constraint_rows = self.build_constraints()
        self.rhs = matvec(self.constraint_rows, self.node_vectors[0])
        self.support_one, self.support_two = primitive_moves(
            model,
            self.active,
            self.column_index,
        )
        self.moves = tuple(sorted(set(self.support_one) | set(self.support_two)))
        self.oriented_moves = tuple(
            sorted(
                {
                    signed
                    for move in self.moves
                    for signed in (move, scale(-1, move))
                }
            )
        )
        self.kernel_coordinates, self.kernel_rank = self.build_kernel_map()
        (
            self.quotient_class,
            self.solve,
            self.move_rank,
            self.invariants,
        ) = self.build_move_lattice()

    def vector(self, node: Node) -> tuple[int, ...]:
        result = [0] * self.columns
        for position, placed in enumerate(node):
            result[self.column_index[position][placed]] = 1
        return tuple(result)

    def build_constraints(self) -> list[list[int]]:
        rows = [
            [0] * self.columns
            for _ in range(len(QUAD) + len(self.model.target_xray))
        ]
        for position, values in enumerate(self.active):
            for placed in values:
                column = self.column_index[position][placed]
                rows[position][column] = 1
                for index, value in enumerate(self.model.xray(placed)):
                    rows[len(QUAD) + index][column] = value
        return rows

    def build_kernel_map(self):
        ambient = integer_matrix(self.constraint_rows)
        diagonal, left, right = smith_normal_decomp(ambient)
        if left * ambient * right != diagonal:
            raise AssertionError("ambient Smith decomposition failed")
        diagonal_rows = matrix_rows(diagonal)
        rank = sum(
            diagonal_rows[index][index] != 0
            for index in range(min(diagonal.shape))
        )
        inverse, denominator = right.inv_den()
        denominator = int(denominator)
        if abs(denominator) != 1:
            raise AssertionError("ambient right transform is not unimodular")
        inverse_rows = [
            [value // denominator for value in row]
            for row in matrix_rows(inverse)
        ]

        def coordinates(vector: tuple[int, ...]) -> tuple[int, ...]:
            transformed = matvec(inverse_rows, vector)
            if any(transformed[:rank]):
                raise AssertionError("purported kernel vector left the kernel")
            return transformed[rank:]

        return coordinates, self.columns - rank

    def build_move_lattice(self):
        move_coordinates = tuple(
            self.kernel_coordinates(move) for move in self.moves
        )
        move_matrix = integer_matrix(
            [
                [move[index] for move in move_coordinates]
                for index in range(self.kernel_rank)
            ]
        )
        diagonal, left, right = smith_normal_decomp(move_matrix)
        if left * move_matrix * right != diagonal:
            raise AssertionError("move Smith decomposition failed")
        diagonal_rows = matrix_rows(diagonal)
        rank = sum(
            diagonal_rows[index][index] != 0
            for index in range(min(diagonal.shape))
        )
        invariants = tuple(
            abs(diagonal_rows[index][index]) for index in range(rank)
        )
        left_rows = matrix_rows(left)
        right_rows = matrix_rows(right)

        def quotient_class(
            vector: tuple[int, ...],
        ) -> tuple[tuple[int, ...], tuple[int, ...]]:
            transformed = matvec(
                left_rows,
                self.kernel_coordinates(vector),
            )
            torsion = tuple(
                transformed[index] % invariants[index]
                for index in range(rank)
            )
            return torsion, transformed[rank:]

        def solve(vector: tuple[int, ...]) -> tuple[int, ...]:
            transformed = matvec(
                left_rows,
                self.kernel_coordinates(vector),
            )
            diagonal_values = [0] * len(self.moves)
            for index in range(rank):
                value = diagonal_rows[index][index]
                if transformed[index] % value:
                    raise ValueError("difference outside the move lattice")
                diagonal_values[index] = transformed[index] // value
            if any(transformed[rank:]):
                raise ValueError("difference outside the move lattice")
            coefficients = matvec(right_rows, diagonal_values)
            rebuilt = [0] * self.columns
            for coefficient, move in zip(coefficients, self.moves):
                for index, value in enumerate(move):
                    rebuilt[index] += coefficient * value
            if tuple(rebuilt) != vector:
                raise AssertionError("move decomposition failed")
            return coefficients

        return quotient_class, solve, rank, invariants

    def move_record(self, move: tuple[int, ...]) -> dict:
        positions = []
        for position, offset in enumerate(self.offsets):
            width = len(self.active[position])
            if any(move[index] for index in range(offset, offset + width)):
                positions.append(position)
        return {
            "support": len(positions),
            "changed_piece_positions": positions,
            "sparse_vector": sparse(move),
        }


def quotient_data(
    context: Context,
    components: list[list[int]],
    component_by_node: list[int],
    energy: list[int],
) -> tuple[dict, list[int], list[dict]]:
    base = context.node_vectors[0]
    signatures = [
        context.quotient_class(sub(vector, base))
        for vector in context.node_vectors
    ]
    ordered = sorted(set(signatures), key=repr)
    class_id = {signature: index for index, signature in enumerate(ordered)}
    classes = [class_id[signature] for signature in signatures]
    component_classes = []
    for component in components:
        values = {classes[node] for node in component}
        if len(values) != 1:
            raise AssertionError("nonnegative component crosses quotient class")
        component_classes.append(next(iter(values)))

    profiles = []
    for identifier, signature in enumerate(ordered):
        nodes = [
            index for index, value in enumerate(classes) if value == identifier
        ]
        component_ids = sorted({component_by_node[index] for index in nodes})
        tilings = [index for index in nodes if energy[index] == 0]
        trapped = [
            index
            for index in nodes
            if energy[index] > 0
            and not any(
                energy[node] == 0
                for node in components[component_by_node[index]]
            )
        ]
        profiles.append(
            {
                "class_id": identifier,
                "torsion_coordinates": list(signature[0]),
                "free_coordinates": list(signature[1]),
                "nodes": nodes,
                "components": component_ids,
                "tiling_nodes": tilings,
                "trapped_nodes": trapped,
                "extra_nodes": [
                    index for index in nodes if energy[index] > 0
                ],
                "mixes_tiling_and_trapped": bool(tilings and trapped),
            }
        )
    summary = {
        "hit_quotient_classes": len(ordered),
        "split_hit_classes": sum(
            len(profile["components"]) > 1 for profile in profiles
        ),
        "mixed_tiling_trapped_classes": sum(
            profile["mixes_tiling_and_trapped"] for profile in profiles
        ),
        "maximum_components_per_hit_class": max(
            len(profile["components"]) for profile in profiles
        ),
        "components_per_hit_class_distribution": distribution(
            len(profile["components"]) for profile in profiles
        ),
    }
    return summary, classes, profiles


def bounded_depth_path(
    context: Context,
    start: tuple[int, ...],
    target: tuple[int, ...],
    depth: int,
    maximum_states: int = 2_000_000,
) -> tuple[tuple[int, ...], ...] | None:
    queue = deque([start])
    predecessor: dict[
        tuple[int, ...],
        tuple[tuple[int, ...], tuple[int, ...]] | None,
    ] = {start: None}
    while queue:
        current = queue.popleft()
        for move in context.oriented_moves:
            candidate = add(current, move)
            if min(candidate) < -depth or candidate in predecessor:
                continue
            predecessor[candidate] = (current, move)
            if candidate == target:
                states = [candidate]
                while states[-1] != start:
                    record = predecessor[states[-1]]
                    if record is None:
                        raise AssertionError("broken bounded-depth predecessor")
                    states.append(record[0])
                return tuple(reversed(states))
            queue.append(candidate)
            if len(predecessor) > maximum_states:
                raise RuntimeError(
                    f"depth-{depth} search exceeded {maximum_states} states"
                )
    return None


def pairing_certificates(
    context: Context,
    profiles: list[dict],
    components: list[list[int]],
    component_by_node: list[int],
    energy: list[int],
) -> tuple[list[dict], list[dict]]:
    trapped_nodes = sorted(
        {
            node
            for profile in profiles
            for node in profile["trapped_nodes"]
        }
    )
    tilings_by_class = {
        profile["class_id"]: profile["tiling_nodes"]
        for profile in profiles
    }
    class_by_node = {
        node: profile["class_id"]
        for profile in profiles
        for node in profile["nodes"]
    }
    status = []
    certificates = []
    for trapped in trapped_nodes:
        class_id = class_by_node[trapped]
        paired_tilings = tilings_by_class[class_id]
        status.append(
            {
                "trapped_node": trapped,
                "class_id": class_id,
                "tilings_in_same_class": paired_tilings,
                "algebraically_separated": not paired_tilings,
            }
        )
        for tiling in paired_tilings:
            if component_by_node[trapped] == component_by_node[tiling]:
                raise AssertionError("trapped and tiling nodes share a component")
            difference = sub(
                context.node_vectors[tiling],
                context.node_vectors[trapped],
            )
            coefficients = context.solve(difference)
            path = None
            exact_depth = None
            searched_depth = 0
            for depth in (1, 2):
                searched_depth = depth
                path = bounded_depth_path(
                    context,
                    context.node_vectors[trapped],
                    context.node_vectors[tiling],
                    depth,
                )
                if path is not None:
                    exact_depth = depth
                    break
            record = {
                "trapped_node": trapped,
                "tiling_node": tiling,
                "class_id": class_id,
                "gamma_lower_bound": 1,
                "searched_depth": searched_depth,
                "gamma_exact": exact_depth,
                "smith_particular_coefficient_l1": sum(map(abs, coefficients)),
                "smith_particular_nonzero_coefficients": [
                    [index, value]
                    for index, value in enumerate(coefficients)
                    if value
                ],
            }
            if path is not None:
                steps = [
                    sub(path[index + 1], path[index])
                    for index in range(len(path) - 1)
                ]
                record.update(
                    {
                        "path_steps": len(steps),
                        "maximum_negative_mass": max(
                            sum(max(0, -value) for value in state)
                            for state in path
                        ),
                        "maximum_coordinate": max(
                            max(state) for state in path
                        ),
                        "states": [sparse(state) for state in path],
                        "steps": [
                            context.move_record(step) for step in steps
                        ],
                    }
                )
            certificates.append(record)
    return status, certificates


def direct_repairs(
    context: Context,
    trapped_nodes: list[int],
    tilings: list[int],
) -> tuple[list[dict], list[tuple[int, int]]]:
    output = []
    minimizing_pairs = []
    for trapped in trapped_nodes:
        degrees = {
            tiling: sum(
                context.nodes[trapped][position]
                != context.nodes[tiling][position]
                for position in range(len(QUAD))
            )
            for tiling in tilings
        }
        rho = min(degrees.values())
        minimizers = sorted(
            tiling for tiling, value in degrees.items() if value == rho
        )
        minimizing_pairs.extend((trapped, tiling) for tiling in minimizers)
        output.append(
            {
                "trapped_node": trapped,
                "rho": rho,
                "minimizing_tilings": minimizers,
                "degree_to_all_tilings": {
                    str(tiling): degrees[tiling] for tiling in tilings
                },
            }
        )
    return output, minimizing_pairs


def pair_orbits(
    pairs: list[tuple[int, int]],
    permutations: tuple[tuple[int, ...], ...],
) -> list[list[int]]:
    lookup = {pair: index for index, pair in enumerate(pairs)}
    unseen = set(range(len(pairs)))
    output = []
    while unseen:
        start = min(unseen)
        left, right = pairs[start]
        orbit = sorted(
            {
                lookup[(permutation[left], permutation[right])]
                for permutation in permutations
            }
        )
        unseen.difference_update(orbit)
        output.append(orbit)
    return output


def node_orbits(
    members: list[int],
    permutations: tuple[tuple[int, ...], ...],
) -> list[list[int]]:
    member_set = set(members)
    unseen = set(members)
    output = []
    while unseen:
        start = min(unseen)
        orbit = sorted({permutation[start] for permutation in permutations})
        if not set(orbit) <= member_set:
            raise AssertionError("node family is not target-action invariant")
        unseen.difference_update(orbit)
        output.append(orbit)
    return output


def representative_repair(
    context: Context,
    pair: tuple[int, int],
) -> dict:
    trapped, tiling = pair
    changed = [
        position
        for position in range(len(QUAD))
        if context.nodes[trapped][position] != context.nodes[tiling][position]
    ]
    return {
        "trapped_node": trapped,
        "tiling_node": tiling,
        "degree": len(changed),
        "changed_piece_positions": changed,
        "changed_piece_indices": [QUAD[position] for position in changed],
        "changed_piece_ids": [
            context.model.ids[QUAD[position]] for position in changed
        ],
        "replacements": [
            {
                "piece_position": position,
                "piece_index": QUAD[position],
                "piece_id": context.model.ids[QUAD[position]],
                "from_cells": [
                    list(cell)
                    for cell in sorted(context.nodes[trapped][position])
                ],
                "to_cells": [
                    list(cell)
                    for cell in sorted(context.nodes[tiling][position])
                ],
            }
            for position in changed
        ],
    }


def analyse(model: Model) -> dict:
    started = time.perf_counter()
    context = Context(model)
    energy = [
        len(model.target) - len(frozenset().union(*node))
        for node in context.nodes
    ]
    tilings = [index for index, value in enumerate(energy) if value == 0]
    edges = direct_graph(context.nodes, {1, 2})
    components, component_by_node = graph_components(edges)
    tiled_components = {component_by_node[index] for index in tilings}
    trapped_components = [
        index
        for index in range(len(components))
        if index not in tiled_components
    ]
    trapped_nodes = sorted(
        node
        for component in trapped_components
        for node in components[component]
    )

    quotient_summary, classes, profiles = quotient_data(
        context,
        components,
        component_by_node,
        energy,
    )
    pairing_status, cone_certificates = pairing_certificates(
        context,
        profiles,
        components,
        component_by_node,
        energy,
    )
    repairs, minimizing_pairs = direct_repairs(
        context,
        trapped_nodes,
        tilings,
    )

    actions = target_symmetries(model.target)
    permutations = action_permutations(context.nodes, actions)
    for permutation in permutations:
        for index, image in enumerate(permutation):
            if energy[index] != energy[image]:
                raise AssertionError("target action changes energy")
            if {permutation[value] for value in edges[index]} != edges[image]:
                raise AssertionError("target action changes G<=2")
            if classes[index] != classes[image]:
                # The action need only induce a well-defined permutation, not
                # fix every quotient class. Checked below by class images.
                pass
    class_images = []
    for permutation in permutations:
        image_by_class: dict[int, set[int]] = defaultdict(set)
        for index, class_id in enumerate(classes):
            image_by_class[class_id].add(classes[permutation[index]])
        if any(len(values) != 1 for values in image_by_class.values()):
            raise AssertionError("target action is not well-defined on classes")
        class_images.append(
            tuple(next(iter(image_by_class[index])) for index in range(len(profiles)))
        )

    trapped_orbits = node_orbits(trapped_nodes, permutations)
    tiling_orbits = node_orbits(tilings, permutations)
    repair_orbits = pair_orbits(minimizing_pairs, permutations)
    algebraically_separated = sum(
        row["algebraically_separated"] for row in pairing_status
    )
    paired = len(pairing_status) - algebraically_separated
    if algebraically_separated and paired:
        branch = "mixed_mechanisms"
    elif algebraically_separated:
        branch = "algebraic_separation"
    else:
        branch = "nonnegative_hole"

    result = {
        "piece_indices": list(QUAD),
        "piece_ids": [model.ids[index] for index in QUAD],
        "fiber_nodes": len(context.nodes),
        "tiling_nodes": len(tilings),
        "extra_nodes": len(context.nodes) - len(tilings),
        "energy_distribution": distribution(energy),
        "participating_placements_by_piece": [
            len(values) for values in context.active
        ],
        "participating_columns": context.columns,
        "constraint_rows": len(context.constraint_rows),
        "ambient_kernel_rank": context.kernel_rank,
        "primitive_support_one_moves": len(context.support_one),
        "primitive_support_two_moves": len(context.support_two),
        "move_lattice_rank": context.move_rank,
        "quotient_free_rank": context.kernel_rank - context.move_rank,
        "quotient_torsion_factors": [
            value for value in context.invariants if value > 1
        ],
        "degree_at_most_two_edges": sum(map(len, edges)) // 2,
        "components": len(components),
        "component_profiles": [
            {
                "component": index,
                "nodes": component,
                "tiling_nodes": [
                    node for node in component if energy[node] == 0
                ],
                "trapped": index in trapped_components,
            }
            for index, component in enumerate(components)
        ],
        "trapped_components": len(trapped_components),
        "trapped_nodes": len(trapped_nodes),
        "trapped_node_indices": trapped_nodes,
        **quotient_summary,
        "hit_class_profiles": profiles,
        "interpretation_branch": branch,
        "algebraically_separated_trapped_nodes": algebraically_separated,
        "quotient_paired_trapped_nodes": paired,
        "pairing_status": pairing_status,
        "cone_certificates": cone_certificates,
        "direct_repairs": repairs,
        "rho_distribution": distribution(row["rho"] for row in repairs),
        "target_automorphisms": [name for name, _ in actions],
        "target_automorphism_order": len(actions),
        "trapped_node_orbits": trapped_orbits,
        "tiling_node_orbits": tiling_orbits,
        "hit_class_action_permutations": [
            list(permutation) for permutation in class_images
        ],
        "minimizing_repair_pairs": [
            list(pair) for pair in minimizing_pairs
        ],
        "minimizing_repair_pair_orbits": repair_orbits,
        "representative_repairs": [
            representative_repair(
                context,
                minimizing_pairs[orbit[0]],
            )
            for orbit in repair_orbits
        ],
        "runtime_seconds": round(time.perf_counter() - started, 6),
    }
    return result


def validate(result: dict) -> None:
    if (
        result["fiber_nodes"],
        result["tiling_nodes"],
        result["extra_nodes"],
        result["primitive_support_one_moves"],
        result["trapped_nodes"],
    ) != (32, 8, 24, 0, 16):
        raise AssertionError("robust-row frozen facts changed")
    if any(row["rho"] <= 2 for row in result["direct_repairs"]):
        raise AssertionError("trapped node has a degree-at-most-two repair")
    if result["target_automorphism_order"] != 8:
        raise AssertionError("P21 target action changed")


def main() -> int:
    started = time.perf_counter()
    model = model_from_locked("p21_locked.json")
    primary = analyse(model)
    result = {
        "schema_version": "p42.robust_p21_quotient.v1",
        "status": "PASS",
        "scope": {
            "library": "P21",
            "row": list(QUAD),
            "move_support": "one or two named placements",
            "lattice": "participating placements only",
            "nonclaim": "finite exact quotient, not a universal Markov basis",
        },
        "preregistration": {
            "path": str(PREREGISTRATION.relative_to(PROJECT)).replace("\\", "/"),
            "sha256": sha256(PREREGISTRATION),
        },
        "inputs": {
            "p21_path": str(model.source.relative_to(PROJECT)).replace("\\", "/"),
            "p21_sha256": sha256(model.source),
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
        },
        "primary": primary,
        "runtime_seconds": round(time.perf_counter() - started, 6),
    }
    validate(primary)
    OUTPUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        "PASS: "
        f"branch={primary['interpretation_branch']}; "
        f"K/M/Q={primary['ambient_kernel_rank']}/"
        f"{primary['move_lattice_rank']}/"
        f"{primary['quotient_free_rank']}; "
        f"classes/components={primary['hit_quotient_classes']}/"
        f"{primary['components']}; "
        f"rho={primary['rho_distribution']}; "
        f"{result['runtime_seconds']:.3f}s"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
