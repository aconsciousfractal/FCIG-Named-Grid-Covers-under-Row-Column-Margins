#!/usr/bin/env python3
"""Independent exact closure of the robust-P21 minimum orbit-generator problem.

This checker does not read P42_SUPPORT4_CEILING_ANALYSIS.json.  It rebuilds the
participating P21 row, enumerates the squarefree support-four relations, forms
K/M_{<=3}, computes the D4-orbit sublattices, and proves that exactly three
complete target-action orbits are necessary and sufficient to generate the
quotient integrally.

Usage
-----
python verify_minimum_orbit_generators.py \
  --xray-dir path/to/packages/package_e_obstruction_channels/xray_channel \
  --output minimum_orbit_generators_certificate.json
"""
from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

from sympy import Matrix, ZZ
from sympy.matrices.normalforms import hermite_normal_form
from sympy.polys.matrices import DomainMatrix
from sympy.polys.matrices.normalforms import smith_normal_decomp

MoveKey = tuple[tuple[int, ...], tuple[int, ...]]


def add_xrays(values: Iterable[tuple[int, ...]]) -> tuple[int, ...]:
    frozen = tuple(values)
    return tuple(sum(row) for row in zip(*frozen))


def canonical_key(negative: tuple[int, ...], positive: tuple[int, ...]) -> MoveKey:
    if min(negative + positive) in negative:
        return negative, positive
    return positive, negative


def compact_to_vector(key: MoveKey, columns: int) -> tuple[int, ...]:
    result = [0] * columns
    for index in key[0]:
        result[index] = -1
    for index in key[1]:
        if result[index]:
            raise AssertionError("overlapping move sides")
        result[index] = 1
    return tuple(result)


def primitive_support_four(context) -> tuple[MoveKey, ...]:
    """Rebuild the final squarefree one-copy support-four catalogue."""
    xrays = tuple(
        tuple(tuple(context.model.xray(p)) for p in values)
        for values in context.active
    )
    buckets: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
    ranges = tuple(range(len(values)) for values in context.active)
    assignments = 0
    for local_assignment in itertools.product(*ranges):
        assignments += 1
        signature = add_xrays(
            xrays[position][local]
            for position, local in enumerate(local_assignment)
        )
        coordinates = tuple(
            context.offsets[position] + local
            for position, local in enumerate(local_assignment)
        )
        buckets[signature].append(coordinates)
    if assignments != 73_728:
        raise AssertionError(f"unexpected assignment count {assignments}")

    moves: set[MoveKey] = set()
    for values in buckets.values():
        for old, new in itertools.combinations(values, 2):
            if all(a != b for a, b in zip(old, new)):
                moves.add(canonical_key(old, new))
    result = tuple(sorted(moves))
    if len(result) != 7_444:
        raise AssertionError(f"unexpected support-four count {len(result)}")
    return result


def transform_key(key: MoveKey, permutation: tuple[int, ...]) -> MoveKey:
    return canonical_key(
        tuple(permutation[i] for i in key[0]),
        tuple(permutation[i] for i in key[1]),
    )


def move_orbits(
    moves: tuple[MoveKey, ...], permutations: tuple[tuple[int, ...], ...]
) -> tuple[list[list[int]], list[int]]:
    lookup = {move: i for i, move in enumerate(moves)}
    unseen = set(range(len(moves)))
    orbits: list[list[int]] = []
    orbit_by_move = [-1] * len(moves)
    while unseen:
        start = min(unseen)
        orbit = sorted(
            {lookup[transform_key(moves[start], p)] for p in permutations}
        )
        oid = len(orbits)
        for index in orbit:
            orbit_by_move[index] = oid
        unseen.difference_update(orbit)
        orbits.append(orbit)
    return orbits, orbit_by_move


def exact_column_lattice_key(vectors: list[tuple[int, ...]]) -> tuple[tuple[int, ...], ...]:
    matrix = Matrix(9, len(vectors), lambda i, j: vectors[j][i])
    hnf = hermite_normal_form(matrix)
    return tuple(
        tuple(int(hnf[i, j]) for i in range(hnf.rows))
        for j in range(hnf.cols)
    )


def independent_columns(vectors: list[tuple[int, ...]]) -> list[int]:
    matrix = Matrix.hstack(*[Matrix(v) for v in vectors])
    return list(matrix.rref()[1])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--xray-dir", type=Path, required=True)
    parser.add_argument(
        "--output", type=Path, default=Path("minimum_orbit_generators_certificate.json")
    )
    args = parser.parse_args()
    xray_dir = args.xray_dir.resolve()
    sys.path.insert(0, str(xray_dir))

    from verify_coarea_next import model_from_locked
    from robust_p21_quotient import Context
    from degree3_augmentation import primitive_support_three
    from placement_quotient import target_symmetries
    from short_dual_separators import placement_action

    model = model_from_locked("p21_locked.json")
    context = Context(model)
    if context.columns != 72 or context.kernel_rank != 60 or len(context.nodes) != 32:
        raise AssertionError("locked robust P21 context drift")

    support_three, _ = primitive_support_three(context)
    moves_le3 = tuple(sorted(set(context.moves) | set(support_three)))
    le3_coordinates = [context.kernel_coordinates(v) for v in moves_le3]
    le3_matrix = Matrix(
        60,
        len(le3_coordinates),
        lambda i, j: le3_coordinates[j][i],
    )
    le3_hnf = hermite_normal_form(le3_matrix)
    if le3_hnf.shape != (60, 51):
        raise AssertionError(f"unexpected M_<=3 HNF shape {le3_hnf.shape}")

    diagonal, left, right = smith_normal_decomp(
        DomainMatrix.from_Matrix(le3_hnf).convert_to(ZZ)
    )
    diagonal_matrix = diagonal.to_Matrix()
    factors = [
        abs(int(diagonal_matrix[i, i]))
        for i in range(min(diagonal_matrix.shape))
        if diagonal_matrix[i, i]
    ]
    if factors != [1] * 51:
        raise AssertionError("M_<=3 is not the locked saturated rank-51 lattice")
    left_matrix = left.to_Matrix()
    quotient_rows = [
        [int(left_matrix[i, j]) for j in range(60)]
        for i in range(51, 60)
    ]

    def qcoord(vector: tuple[int, ...]) -> tuple[int, ...]:
        kernel = context.kernel_coordinates(vector)
        return tuple(
            sum(row[j] * kernel[j] for j in range(60))
            for row in quotient_rows
        )

    support_four = primitive_support_four(context)
    support_four_vectors = tuple(
        compact_to_vector(move, context.columns) for move in support_four
    )
    actions = target_symmetries(model.target)
    permutations = placement_action(context, actions)
    orbits, orbit_by_move = move_orbits(support_four, permutations)
    if len(orbits) != 1_119:
        raise AssertionError(f"unexpected orbit count {len(orbits)}")
    if Counter(map(len, orbits)) != Counter({8: 742, 4: 377}):
        raise AssertionError("support-four orbit-size profile drift")

    orbit_records = []
    for oid, member_indices in enumerate(orbits):
        qvectors = [qcoord(support_four_vectors[i]) for i in member_indices]
        rank = Matrix.hstack(*[Matrix(v) for v in qvectors]).rank()
        orbit_records.append(
            {
                "id": oid,
                "members": member_indices,
                "qvectors": qvectors,
                "rank": int(rank),
            }
        )
    rank_distribution = Counter(record["rank"] for record in orbit_records)
    expected_ranks = Counter({0: 458, 2: 568, 3: 87, 4: 6})
    if rank_distribution != expected_ranks:
        raise AssertionError((rank_distribution, expected_ranks))

    # Character of every cyclic D4-submodule.  The action-name order is fixed
    # by target_symmetries: id, rot180, flip_rows, flip_cols, rot90, rot270,
    # diag, antidiag.
    character_distribution: Counter[tuple[int, tuple[int, ...]]] = Counter()
    for record in orbit_records:
        rank = record["rank"]
        if rank == 0:
            character = (0,) * len(actions)
        else:
            qvectors = record["qvectors"]
            pivots = independent_columns(qvectors)
            basis_member_indices = [record["members"][j] for j in pivots]
            basis = Matrix.hstack(*[Matrix(qvectors[j]) for j in pivots])
            traces = []
            for permutation in permutations:
                columns = []
                for move_index in basis_member_indices:
                    ambient = support_four_vectors[move_index]
                    image = [0] * context.columns
                    for old, value in enumerate(ambient):
                        image[permutation[old]] = value
                    target = Matrix(qcoord(tuple(image)))
                    solution = basis.gauss_jordan_solve(target)[0]
                    if any(value.free_symbols for value in solution):
                        raise AssertionError("nonunique orbit action solution")
                    columns.append(solution)
                action_matrix = Matrix.hstack(*columns)
                traces.append(int(action_matrix.trace()))
            character = tuple(traces)
        character_distribution[(rank, character)] += 1

    expected_characters = {
        (0, (0, 0, 0, 0, 0, 0, 0, 0)): 458,
        (2, (2, -2, 0, 0, 0, 0, 0, 0)): 568,
        (3, (3, -1, 1, 1, -1, -1, -1, -1)): 87,
        (4, (4, -4, 0, 0, 0, 0, 0, 0)): 6,
    }
    if dict(character_distribution) != expected_characters:
        raise AssertionError("cyclic D4-module character profile drift")

    # The 87 rank-three orbits fall into exactly three *integral* sublattices.
    rank_three_by_lattice: dict[tuple[tuple[int, ...], ...], list[int]] = defaultdict(list)
    for record in orbit_records:
        if record["rank"] == 3:
            rank_three_by_lattice[exact_column_lattice_key(record["qvectors"])].append(
                record["id"]
            )
    families = sorted(rank_three_by_lattice.values(), key=min)
    if [len(values) for values in families] != [6, 3, 78]:
        raise AssertionError(f"rank-three family profile drift: {[len(x) for x in families]}")
    family_a, family_b, family_c = families

    canonical_orbits = (283, 603, 714)
    if not (
        canonical_orbits[0] in family_a
        and canonical_orbits[1] in family_b
        and canonical_orbits[2] in family_c
    ):
        raise AssertionError("canonical orbit family membership drift")

    witness_columns = []
    witness_moves = []
    for oid in canonical_orbits:
        record = orbit_records[oid]
        pivots = independent_columns(record["qvectors"])
        if pivots[:3] != [0, 1, 2]:
            raise AssertionError(f"canonical pivot drift in orbit {oid}: {pivots}")
        for j in pivots[:3]:
            witness_columns.append(Matrix(record["qvectors"][j]))
            move_index = record["members"][j]
            witness_moves.append(move_index)
    witness_matrix = Matrix.hstack(*witness_columns)
    witness_det = int(witness_matrix.det())
    if abs(witness_det) != 1:
        raise AssertionError(f"canonical orbit triple is not unimodular: {witness_det}")

    # Character of the full quotient, using the unimodular witness basis.
    full_traces = []
    for permutation in permutations:
        columns = []
        for move_index in witness_moves:
            ambient = support_four_vectors[move_index]
            image = [0] * context.columns
            for old, value in enumerate(ambient):
                image[permutation[old]] = value
            target = Matrix(qcoord(tuple(image)))
            columns.append(witness_matrix.inv() * target)
        action_matrix = Matrix.hstack(*columns)
        full_traces.append(int(action_matrix.trace()))
    expected_full_character = (9, -3, 3, 3, -3, -3, -3, -3)
    if tuple(full_traces) != expected_full_character:
        raise AssertionError((tuple(full_traces), expected_full_character))

    # Minimality proof:
    # Q_Q has three copies of the axial 1D character chi=(1,1,1,1,-1,-1,-1,-1).
    # A cyclic orbit span contains chi only in the rank-three profile, and then
    # with multiplicity exactly one. Hence at least three orbits are necessary.
    # The unimodular triple above proves three are sufficient.
    number_of_minimum_triples = len(family_a) * len(family_b) * len(family_c)
    if number_of_minimum_triples != 1_404:
        raise AssertionError("minimum triple count drift")

    # Which quotient channels are visible on the locked 32-node one-copy fiber?
    move_lookup = {move: index for index, move in enumerate(support_four)}
    active_orbits = set()
    degree_four_edges_by_orbit: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for left_node, right_node in itertools.combinations(range(len(context.nodes)), 2):
        if sum(a != b for a, b in zip(context.nodes[left_node], context.nodes[right_node])) != 4:
            continue
        left_vector = context.node_vectors[left_node]
        right_vector = context.node_vectors[right_node]
        difference = tuple(b - a for a, b in zip(left_vector, right_vector))
        negative = tuple(index for index, value in enumerate(difference) if value < 0)
        positive = tuple(index for index, value in enumerate(difference) if value > 0)
        key = canonical_key(negative, positive)
        move_index = move_lookup[key]
        oid = orbit_by_move[move_index]
        active_orbits.add(oid)
        degree_four_edges_by_orbit[oid].append((left_node, right_node))
    if len(active_orbits) != 64:
        raise AssertionError(f"fiber-active orbit count drift: {len(active_orbits)}")
    family_active_counts = [
        len(active_orbits & set(family))
        for family in (family_a, family_b, family_c)
    ]
    if family_active_counts != [0, 0, 36]:
        raise AssertionError(f"rank-three visibility profile drift: {family_active_counts}")

    # Base G_<=3 components and the canonical connector orbit 714.
    base_adjacency = [set() for _ in context.nodes]
    for left_node, right_node in itertools.combinations(range(len(context.nodes)), 2):
        if sum(a != b for a, b in zip(context.nodes[left_node], context.nodes[right_node])) <= 3:
            base_adjacency[left_node].add(right_node)
            base_adjacency[right_node].add(left_node)
    def components(adjacency):
        unseen = set(range(len(adjacency)))
        result = []
        while unseen:
            start = min(unseen)
            unseen.remove(start)
            stack = [start]
            comp = []
            while stack:
                current = stack.pop()
                comp.append(current)
                for neighbour in adjacency[current]:
                    if neighbour in unseen:
                        unseen.remove(neighbour)
                        stack.append(neighbour)
            result.append(sorted(comp))
        return sorted(result)
    base_components = components(base_adjacency)
    if [len(value) for value in base_components] != [8, 8, 8, 8]:
        raise AssertionError("G_<=3 component profile drift")
    connected_adjacency = [set(values) for values in base_adjacency]
    for left_node, right_node in degree_four_edges_by_orbit[714]:
        connected_adjacency[left_node].add(right_node)
        connected_adjacency[right_node].add(left_node)
    if len(components(connected_adjacency)) != 1:
        raise AssertionError("orbit 714 no longer connects the fixed fiber")

    certificate = {
        "schema": "p42.minimum_integral_orbit_generator.v1",
        "row": [4, 5, 12, 13],
        "participating_columns": context.columns,
        "kernel_rank": context.kernel_rank,
        "rank_M_le_3": 51,
        "quotient_rank": 9,
        "support_four_moves": len(support_four),
        "target_orbits": len(orbits),
        "orbit_size_distribution": dict(sorted(Counter(map(len, orbits)).items())),
        "orbit_quotient_rank_distribution": dict(sorted(rank_distribution.items())),
        "action_order": [name for name, _ in actions],
        "cyclic_module_character_distribution": [
            {
                "rank": rank,
                "character": list(character),
                "orbit_count": count,
            }
            for (rank, character), count in sorted(character_distribution.items())
        ],
        "quotient_character": list(full_traces),
        "axial_character": [1, 1, 1, 1, -1, -1, -1, -1],
        "standard_2d_character": [2, -2, 0, 0, 0, 0, 0, 0],
        "rational_module_decomposition": "3*(chi_axial + E_standard)",
        "rank_three_integral_families": [family_a, family_b, family_c],
        "family_sizes": [len(family_a), len(family_b), len(family_c)],
        "fixed_fiber_visibility": {
            "fiber_active_support_four_orbits": len(active_orbits),
            "rank_three_family_active_counts": family_active_counts,
            "interpretation": "the first two rank-three quotient channels are fiber-invisible; the third contains exactly the 36 singleton connector orbits",
            "G_le_3_component_sizes": [len(value) for value in base_components],
            "orbit_714_connects_fixed_fiber": True,
        },
        "minimum_complete_target_orbits": 3,
        "number_of_minimum_families": number_of_minimum_triples,
        "characterization_of_minimum_families": "one orbit from each of the three rank-three integral families",
        "canonical_orbit_family": list(canonical_orbits),
        "canonical_orbit_member_move_indices": witness_moves,
        "canonical_quotient_basis_matrix_columns": [
            [int(value) for value in column]
            for column in witness_columns
        ],
        "canonical_determinant": witness_det,
        "canonical_compact_representatives": [
            [
                list(support_four[orbits[oid][0]][0]),
                list(support_four[orbits[oid][0]][1]),
            ]
            for oid in canonical_orbits
        ],
        "interpretation": {
            "lattice_generation": "closed: minimum is exactly three target-action orbits",
            "fixed_fiber_connectivity": "orbit 714 alone connects the four G_<=3 components",
            "markov_basis": "not implied and tested separately",
        },
    }
    args.output.write_text(
        json.dumps(certificate, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print("PASS minimum integral orbit generators")
    print("support4/orbits/ranks:", len(support_four), len(orbits), dict(rank_distribution))
    print("rank-three families:", [len(x) for x in families])
    print("minimum / count / canonical determinant:", 3, number_of_minimum_triples, witness_det)


if __name__ == "__main__":
    main()
