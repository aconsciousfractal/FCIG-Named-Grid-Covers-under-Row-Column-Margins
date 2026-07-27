#!/usr/bin/env python3
"""Final support-four ceiling for the robust P21 participating catalogue."""
from __future__ import annotations

import hashlib
import itertools
import json
import platform
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

from flint import fmpz_mat

from degree3_augmentation import primitive_support_three
from placement_quotient import (
    action_permutations,
    graph_components,
    target_symmetries,
)
from robust_p21_quotient import Context, QUAD, sub
from short_dual_separators import placement_action
from verify_coarea_next import model_from_locked


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent.parent
OUTPUT = PROJECT / "reports" / "P42_SUPPORT4_CEILING_ANALYSIS.json"
PREREGISTRATION = HERE / "SUPPORT4_CEILING_PREREGISTRATION.md"
LOCKED_SHA256 = (
    "6a2f4ed590f50831f04f083656c3b7f0067cca898c5617773fecf38481e42b8f"
)

MoveKey = tuple[tuple[int, ...], tuple[int, ...]]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest_json(value: object) -> str:
    payload = json.dumps(
        value,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def distribution(values: Iterable[int]) -> dict[str, int]:
    counts = Counter(str(value) for value in values)
    return dict(sorted(counts.items(), key=lambda item: int(item[0])))


def add_xrays(values: Iterable[tuple[int, ...]]) -> tuple[int, ...]:
    frozen = tuple(values)
    return tuple(sum(row) for row in zip(*frozen))


def canonical_key(
    negative: tuple[int, ...],
    positive: tuple[int, ...],
) -> MoveKey:
    """Orient a squarefree move as the lexicographically smaller full vector."""
    if len(negative) != 4 or len(positive) != 4:
        raise AssertionError("support-four key must have four coordinates per side")
    if any(left == right for left, right in zip(negative, positive)):
        raise AssertionError("support-four key did not change every position")
    # The first nonzero coordinate decides lexicographic orientation. It must
    # carry -1 in the canonical full vector.
    if min(negative + positive) in negative:
        return negative, positive
    return positive, negative


def compact_record(key: MoveKey) -> list[list[int]]:
    return [list(key[0]), list(key[1])]


def compact_to_vector(key: MoveKey, columns: int) -> tuple[int, ...]:
    vector = [0] * columns
    for coordinate in key[0]:
        vector[coordinate] = -1
    for coordinate in key[1]:
        if vector[coordinate]:
            raise AssertionError("support-four sides overlap")
        vector[coordinate] = 1
    return tuple(vector)


def vector_to_key(
    vector: tuple[int, ...],
    offsets: tuple[int, ...],
    widths: tuple[int, ...],
) -> MoveKey:
    negative = []
    positive = []
    for offset, width in zip(offsets, widths):
        values = vector[offset : offset + width]
        local_negative = [offset + index for index, value in enumerate(values) if value < 0]
        local_positive = [offset + index for index, value in enumerate(values) if value > 0]
        if len(local_negative) != 1 or len(local_positive) != 1:
            raise AssertionError("fiber difference is not primitive support four")
        negative.append(local_negative[0])
        positive.append(local_positive[0])
    return canonical_key(tuple(negative), tuple(positive))


def primitive_support_four(
    context: Context,
) -> tuple[tuple[MoveKey, ...], dict[str, object]]:
    xrays = tuple(
        tuple(context.model.xray(placed) for placed in values)
        for values in context.active
    )
    buckets: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
    ranges = tuple(range(len(values)) for values in context.active)
    assignment_count = 0
    for local_assignment in itertools.product(*ranges):
        assignment_count += 1
        key = add_xrays(
            xrays[position][local]
            for position, local in enumerate(local_assignment)
        )
        coordinates = tuple(
            context.offsets[position] + local
            for position, local in enumerate(local_assignment)
        )
        buckets[key].append(coordinates)

    moves: set[MoveKey] = set()
    same_xray_pair_count = 0
    admissible_pair_count = 0
    for assignments in buckets.values():
        same_xray_pair_count += len(assignments) * (len(assignments) - 1) // 2
        for old, new in itertools.combinations(assignments, 2):
            if any(left == right for left, right in zip(old, new)):
                continue
            admissible_pair_count += 1
            moves.add(canonical_key(old, new))

    frozen = tuple(sorted(moves))
    statistics = {
        "assignment_count": assignment_count,
        "xray_bucket_count": len(buckets),
        "xray_bucket_size_distribution": distribution(map(len, buckets.values())),
        "maximum_xray_bucket_size": max(map(len, buckets.values())),
        "same_xray_unordered_pair_count": same_xray_pair_count,
        "admissible_pair_instance_count": admissible_pair_count,
        "deduplicated_move_count": len(frozen),
        "deduplication_collisions": admissible_pair_count - len(frozen),
    }
    return frozen, statistics


def transform_key(key: MoveKey, permutation: tuple[int, ...]) -> MoveKey:
    return canonical_key(
        tuple(permutation[coordinate] for coordinate in key[0]),
        tuple(permutation[coordinate] for coordinate in key[1]),
    )


def compact_move_orbits(
    moves: tuple[MoveKey, ...],
    permutations: tuple[tuple[int, ...], ...],
) -> tuple[list[list[int]], list[int]]:
    lookup = {move: index for index, move in enumerate(moves)}
    unseen = set(range(len(moves)))
    orbits: list[list[int]] = []
    orbit_by_move = [-1] * len(moves)
    while unseen:
        start = min(unseen)
        orbit = sorted(
            {
                lookup[transform_key(moves[start], permutation)]
                for permutation in permutations
            }
        )
        identifier = len(orbits)
        for index in orbit:
            orbit_by_move[index] = identifier
        unseen.difference_update(orbit)
        orbits.append(orbit)
    if any(identifier < 0 for identifier in orbit_by_move):
        raise AssertionError("support-four target action is incomplete")
    return orbits, orbit_by_move


def lattice_data(
    context: Context,
    moves: Iterable[tuple[int, ...]],
) -> dict[str, object]:
    frozen = tuple(moves)
    coordinates = [
        list(context.kernel_coordinates(move))
        for move in frozen
    ]
    matrix = fmpz_mat(coordinates)
    lattice_rank = int(matrix.rank())
    diagonal = matrix.snf()
    factors = [
        abs(int(diagonal[index, index]))
        for index in range(min(diagonal.nrows(), diagonal.ncols()))
        if diagonal[index, index]
    ]
    return {
        "generator_count": len(frozen),
        "rank": lattice_rank,
        "free_quotient_rank": context.kernel_rank - lattice_rank,
        "smith_factors": factors,
        "nontrivial_torsion_factors": [
            factor for factor in factors if factor > 1
        ],
    }


def edge_census(
    nodes,
) -> tuple[dict[int, list[tuple[int, int]]], list[set[int]]]:
    by_degree = {degree: [] for degree in range(1, 5)}
    complete = [set() for _ in nodes]
    for left, right in itertools.combinations(range(len(nodes)), 2):
        degree = sum(a != b for a, b in zip(nodes[left], nodes[right]))
        by_degree[degree].append((left, right))
        complete[left].add(right)
        complete[right].add(left)
    return by_degree, complete


def adjacency_through_degree(
    nodes,
    maximum: int,
) -> list[set[int]]:
    adjacency = [set() for _ in nodes]
    for left, right in itertools.combinations(range(len(nodes)), 2):
        degree = sum(a != b for a, b in zip(nodes[left], nodes[right]))
        if degree <= maximum:
            adjacency[left].add(right)
            adjacency[right].add(left)
    return adjacency


def graph_summary(
    adjacency: list[set[int]],
    energy: list[int],
    formerly_trapped: list[int],
) -> dict[str, object]:
    components, component_by_node = graph_components(adjacency)
    profiles = []
    for identifier, component in enumerate(components):
        profiles.append(
            {
                "component": identifier,
                "nodes": component,
                "tiling_nodes": [
                    node for node in component if energy[node] == 0
                ],
                "live_extra_nodes": [
                    node
                    for node in component
                    if energy[node] > 0 and node not in formerly_trapped
                ],
                "formerly_trapped_nodes": [
                    node for node in component if node in formerly_trapped
                ],
            }
        )
    return {
        "components": len(components),
        "component_partition": components,
        "component_by_node": component_by_node,
        "component_profiles": profiles,
        "full_fiber_connected": len(components) == 1,
    }


def connected_component_graph(
    vertex_count: int,
    edges: Iterable[tuple[int, int]],
) -> bool:
    adjacency = [set() for _ in range(vertex_count)]
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    reached = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for neighbor in sorted(adjacency[vertex] - reached):
            reached.add(neighbor)
            stack.append(neighbor)
    return len(reached) == vertex_count


def subset_graph(
    nodes,
    base_adjacency: list[set[int]],
    degree_four_edges: list[tuple[int, int]],
    edge_orbit_ids: list[int],
    selected: set[int],
) -> list[set[int]]:
    adjacency = [set(neighbors) for neighbors in base_adjacency]
    for edge, orbit in zip(degree_four_edges, edge_orbit_ids):
        if orbit not in selected:
            continue
        left, right = edge
        adjacency[left].add(right)
        adjacency[right].add(left)
    return adjacency


def analyse() -> dict[str, object]:
    started = time.perf_counter()
    model = model_from_locked("p21_locked.json")
    context = Context(model)
    support_three, by_positions = primitive_support_three(context)
    support_four_keys, enumeration = primitive_support_four(context)
    support_four_vectors = tuple(
        compact_to_vector(key, context.columns)
        for key in support_four_keys
    )

    for vector in support_four_vectors:
        if (
            vector.count(-1),
            vector.count(1),
            vector.count(0),
        ) != (4, 4, context.columns - 8):
            raise AssertionError("support-four vector is not squarefree 4-by-4")
        if any(
            sum(row[column] * vector[column] for column in range(context.columns))
            for row in context.constraint_rows
        ):
            raise AssertionError("support-four vector left the ambient kernel")

    actions = target_symmetries(model.target)
    node_permutations = action_permutations(context.nodes, actions)
    coordinate_permutations = placement_action(context, actions)
    move_orbits, move_orbit_by_move = compact_move_orbits(
        support_four_keys,
        coordinate_permutations,
    )
    support_four_index = {
        move: index for index, move in enumerate(support_four_keys)
    }

    full_degree_three_moves = tuple(
        sorted(set(context.moves) | set(support_three))
    )
    degree_three_lattice = lattice_data(context, full_degree_three_moves)
    full_moves = tuple(
        sorted(set(full_degree_three_moves) | set(support_four_vectors))
    )
    full_lattice = lattice_data(context, full_moves)

    energy = [
        len(model.target) - len(frozenset().union(*node))
        for node in context.nodes
    ]
    g2 = adjacency_through_degree(context.nodes, 2)
    g2_components, g2_component_by_node = graph_components(g2)
    tiling_components = {
        g2_component_by_node[node]
        for node, value in enumerate(energy)
        if value == 0
    }
    formerly_trapped = sorted(
        node
        for identifier, component in enumerate(g2_components)
        if identifier not in tiling_components
        for node in component
    )

    edges_by_degree, complete_adjacency = edge_census(context.nodes)
    base_adjacency = adjacency_through_degree(context.nodes, 3)
    base_graph = graph_summary(base_adjacency, energy, formerly_trapped)
    complete_graph = graph_summary(
        complete_adjacency,
        energy,
        formerly_trapped,
    )
    if base_graph["components"] != 4:
        raise AssertionError("frozen G<=3 component count changed")
    base_component_by_node = base_graph["component_by_node"]

    widths = tuple(len(values) for values in context.active)
    degree_four_edges = edges_by_degree[4]
    degree_four_move_indices = []
    degree_four_move_orbits = []
    for left, right in degree_four_edges:
        difference = sub(
            context.node_vectors[right],
            context.node_vectors[left],
        )
        key = vector_to_key(difference, context.offsets, widths)
        move_index = support_four_index[key]
        degree_four_move_indices.append(move_index)
        degree_four_move_orbits.append(move_orbit_by_move[move_index])

    active_orbit_ids = sorted(set(degree_four_move_orbits))
    active_orbit_records = []
    induced_edges_by_orbit: dict[int, set[tuple[int, int]]] = {}
    for orbit_id in active_orbit_ids:
        fiber_edges = [
            edge
            for edge, edge_orbit in zip(
                degree_four_edges,
                degree_four_move_orbits,
            )
            if edge_orbit == orbit_id
        ]
        induced = {
            tuple(
                sorted(
                    (
                        base_component_by_node[left],
                        base_component_by_node[right],
                    )
                )
            )
            for left, right in fiber_edges
            if base_component_by_node[left] != base_component_by_node[right]
        }
        induced_edges_by_orbit[orbit_id] = induced
        active_orbit_records.append(
            {
                "move_orbit": orbit_id,
                "move_orbit_size": len(move_orbits[orbit_id]),
                "move_indices": move_orbits[orbit_id],
                "fiber_edge_count": len(fiber_edges),
                "fiber_edges": [list(edge) for edge in fiber_edges],
                "induced_base_component_edges": [
                    list(edge) for edge in sorted(induced)
                ],
            }
        )

    minimum_size = None
    connecting_subsets: list[tuple[int, ...]] = []
    for size in range(1, 4):
        for subset in itertools.combinations(active_orbit_ids, size):
            induced = set().union(
                *(induced_edges_by_orbit[orbit] for orbit in subset)
            )
            if connected_component_graph(4, induced):
                connecting_subsets.append(subset)
        if connecting_subsets:
            minimum_size = size
            break
    if minimum_size is None:
        raise AssertionError("support-four merger search found no connector")

    minimum_subset_records = []
    for subset in connecting_subsets:
        selected_orbits = set(subset)
        selected_move_indices = sorted(
            {
                move_index
                for orbit in subset
                for move_index in move_orbits[orbit]
            }
        )
        selected_moves = tuple(
            support_four_vectors[index]
            for index in selected_move_indices
        )
        augmented_moves = tuple(
            sorted(set(full_degree_three_moves) | set(selected_moves))
        )
        adjacency = subset_graph(
            context.nodes,
            base_adjacency,
            degree_four_edges,
            degree_four_move_orbits,
            selected_orbits,
        )
        induced = set().union(
            *(induced_edges_by_orbit[orbit] for orbit in subset)
        )
        selected_edges = [
            edge
            for edge, orbit in zip(degree_four_edges, degree_four_move_orbits)
            if orbit in selected_orbits
        ]
        minimum_subset_records.append(
            {
                "selected_move_orbits": list(subset),
                "selected_support_four_move_count": len(selected_move_indices),
                "selected_support_four_move_indices": selected_move_indices,
                "selected_fiber_edge_count": len(selected_edges),
                "selected_fiber_edges": [list(edge) for edge in selected_edges],
                "induced_base_component_edges": [
                    list(edge) for edge in sorted(induced)
                ],
                "move_lattice": lattice_data(context, augmented_moves),
                "graph": graph_summary(
                    adjacency,
                    energy,
                    formerly_trapped,
                ),
            }
        )

    canonical_subset = connecting_subsets[0]
    canonical_record = minimum_subset_records[0]
    if full_lattice["rank"] < context.kernel_rank:
        branch = "SUPPORT4_RANK_DEFICIENT"
    else:
        kernel_generated = not full_lattice["nontrivial_torsion_factors"]
        one_orbit = minimum_size == 1
        if kernel_generated and one_orbit:
            branch = "SUPPORT4_GENERATES_KERNEL_ONE_ORBIT_CONNECTS"
        elif kernel_generated:
            branch = "SUPPORT4_GENERATES_KERNEL_MULTIPLE_ORBITS_CONNECT"
        elif one_orbit:
            branch = "SUPPORT4_FINITE_INDEX_ONE_ORBIT_CONNECTS"
        else:
            branch = "SUPPORT4_FINITE_INDEX_MULTIPLE_ORBITS_CONNECT"

    move_manifest = [
        compact_record(key) for key in support_four_keys
    ]
    orbit_records = [
        {
            "move_orbit": identifier,
            "size": len(orbit),
            "representative_move_index": orbit[0],
            "representative_move": compact_record(
                support_four_keys[orbit[0]]
            ),
            "member_indices": orbit,
            "member_move_set_sha256": digest_json(
                [move_manifest[index] for index in orbit]
            ),
            "fiber_active": identifier in active_orbit_ids,
        }
        for identifier, orbit in enumerate(move_orbits)
    ]
    primary = {
        "piece_indices": list(QUAD),
        "piece_ids": [model.ids[index] for index in QUAD],
        "fiber_nodes": len(context.nodes),
        "tiling_nodes": [
            node for node, value in enumerate(energy) if value == 0
        ],
        "formerly_trapped_nodes": formerly_trapped,
        "participating_placements_by_piece": list(widths),
        "participating_columns": context.columns,
        "ambient_kernel_rank": context.kernel_rank,
        "target_automorphism_order": len(actions),
        "target_automorphisms": [name for name, _ in actions],
        "preceding_support_three": {
            "support_one_moves": len(context.support_one),
            "support_two_moves": len(context.support_two),
            "support_three_moves": len(support_three),
            "support_three_counts_by_positions": {
                "-".join(map(str, positions)): len(moves)
                for positions, moves in by_positions.items()
            },
            "move_lattice": degree_three_lattice,
            "graph": base_graph,
        },
        "support_four": {
            **enumeration,
            "move_count": len(support_four_keys),
            "move_set_sha256": digest_json(move_manifest),
            "compact_move_encoding": (
                "[negative coordinates by piece position, "
                "positive coordinates by piece position]"
            ),
            "target_move_orbit_count": len(move_orbits),
            "target_move_orbit_size_distribution": distribution(
                map(len, move_orbits)
            ),
            "target_move_orbits": orbit_records,
            "target_action_closed": True,
        },
        "complete_support_ceiling": {
            "move_lattice": full_lattice,
            "graph_edge_counts_by_exact_degree": {
                str(degree): len(edges)
                for degree, edges in edges_by_degree.items()
            },
            "graph_total_edges": sum(map(len, edges_by_degree.values())),
            "graph": complete_graph,
            "all_distinct_node_pairs_are_edges": (
                sum(map(len, edges_by_degree.values()))
                == len(context.nodes) * (len(context.nodes) - 1) // 2
            ),
        },
        "component_merger": {
            "base_component_count": base_graph["components"],
            "base_component_partition": base_graph["component_partition"],
            "fiber_active_move_orbit_count": len(active_orbit_ids),
            "fiber_active_move_orbit_ids": active_orbit_ids,
            "fiber_active_move_orbits": active_orbit_records,
            "degree_four_edges": [list(edge) for edge in degree_four_edges],
            "degree_four_edge_move_indices": degree_four_move_indices,
            "degree_four_edge_move_orbit_ids": degree_four_move_orbits,
            "minimum_connecting_orbit_count": minimum_size,
            "minimum_connecting_subset_count": len(connecting_subsets),
            "minimum_connecting_subsets": [
                list(subset) for subset in connecting_subsets
            ],
            "canonical_connecting_subset": list(canonical_subset),
            "minimum_subset_results": minimum_subset_records,
            "canonical_result": canonical_record,
            "minimality_scope": (
                "exact among target-action support-four move orbits "
                "active on the fixed 32-node fiber"
            ),
        },
        "interpretation_branch": branch,
        "conclusion": (
            "complete participating support-four lattice and exact finite "
            "target-orbit component-merger ceiling"
        ),
        "nonclaims": [
            "finite 72-coordinate participating P21 catalogue only",
            "no inactive placements or other right-hand sides",
            "no all-fibers Markov or Graver basis",
            "merger minimality only among fiber-active target move orbits",
            "not a public claim or paper-readiness decision",
        ],
        "runtime_seconds": round(time.perf_counter() - started, 6),
    }
    validate(primary)
    return primary


def validate(primary: dict[str, object]) -> None:
    preceding = primary["preceding_support_three"]
    if (
        primary["fiber_nodes"],
        len(primary["tiling_nodes"]),
        len(primary["formerly_trapped_nodes"]),
        primary["participating_placements_by_piece"],
        primary["participating_columns"],
        primary["ambient_kernel_rank"],
        primary["target_automorphism_order"],
    ) != (32, 8, 16, [8, 24, 16, 24], 72, 60, 8):
        raise AssertionError("frozen robust P21 scope changed")
    if (
        preceding["support_one_moves"],
        preceding["support_two_moves"],
        preceding["support_three_moves"],
        preceding["move_lattice"]["rank"],
    ) != (0, 144, 932, 51):
        raise AssertionError("preceding degree-three result changed")
    support_four = primary["support_four"]
    if (
        support_four["assignment_count"] != 73_728
        or not support_four["move_count"]
        or support_four["move_count"] != support_four["deduplicated_move_count"]
        or not support_four["target_action_closed"]
    ):
        raise AssertionError("support-four census is incomplete")
    ceiling = primary["complete_support_ceiling"]
    if ceiling["graph_edge_counts_by_exact_degree"] != {
        "1": 0,
        "2": 16,
        "3": 48,
        "4": 432,
    }:
        raise AssertionError("direct G<=4 edge census changed")
    if (
        ceiling["graph_total_edges"] != 496
        or ceiling["graph"]["components"] != 1
        or not ceiling["all_distinct_node_pairs_are_edges"]
    ):
        raise AssertionError("direct G<=4 is not complete")
    merger = primary["component_merger"]
    if not 1 <= merger["minimum_connecting_orbit_count"] <= 3:
        raise AssertionError("component-merger minimum is out of range")
    if not merger["canonical_result"]["graph"]["full_fiber_connected"]:
        raise AssertionError("canonical merger subset does not connect")
    if ceiling["move_lattice"]["rank"] < preceding["move_lattice"]["rank"]:
        raise AssertionError("support-four augmentation lowered lattice rank")


def main() -> int:
    started = time.perf_counter()
    primary = analyse()
    output = {
        "schema_version": "p42.support4_ceiling.v1",
        "status": "PASS",
        "scope": {
            "library": "P21",
            "row": list(QUAD),
            "lattice": "72 participating named placements",
            "moves": "all primitive support-at-most-four relations",
            "graph": "complete 32-node fiber under G<=4",
            "minimality": (
                "exact among fiber-active target-action support-four "
                "move orbits"
            ),
        },
        "preregistration": {
            "path": str(PREREGISTRATION.relative_to(PROJECT)).replace("\\", "/"),
            "sha256": sha256(PREREGISTRATION),
        },
        "inputs": {
            "p21_path": (
                "packages/package_c_comparative_hypergraphs/"
                "specimens/p21_locked.json"
            ),
            "p21_sha256": LOCKED_SHA256,
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
    lattice = primary["complete_support_ceiling"]["move_lattice"]
    merger = primary["component_merger"]
    print(
        "PASS: "
        f"branch={primary['interpretation_branch']}; "
        f"support4/orbits="
        f"{primary['support_four']['move_count']}/"
        f"{primary['support_four']['target_move_orbit_count']}; "
        f"rank/free/torsion={lattice['rank']}/"
        f"{lattice['free_quotient_rank']}/"
        f"{lattice['nontrivial_torsion_factors']}; "
        f"merger={merger['minimum_connecting_orbit_count']} "
        f"of {merger['fiber_active_move_orbit_count']}; "
        f"{output['runtime_seconds']:.3f}s"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
