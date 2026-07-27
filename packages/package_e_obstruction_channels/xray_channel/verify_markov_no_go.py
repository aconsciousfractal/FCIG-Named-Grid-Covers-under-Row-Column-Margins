#!/usr/bin/env python3
"""Exact all-right-hand-side Markov no-go for the robust P21 configuration.

The current support filtration is squarefree and one-copy: on each side of a
move, at most one placement from each named piece block occurs.  This checker
constructs repeated-copy fibers of the same placement-coloured X-ray matrix and
proves that the squarefree support-at-most-four family is not a Markov basis.

It also performs a low-degree Betti-fiber census and gives an indispensable
single-block degree-seven binomial, proving Markov degree at least seven.
"""
from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


def canonical_vector(vector: tuple[int, ...]) -> tuple[int, ...]:
    negative = tuple(-value for value in vector)
    return min(vector, negative)


def monomial_vector(indices: tuple[int, ...], columns: int) -> tuple[int, ...]:
    result = [0] * columns
    for index in indices:
        result[index] += 1
    return tuple(result)


def degree_key(column_vectors: list[tuple[int, ...]], indices: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sum(column_vectors[index][j] for index in indices) for j in range(14))


def components_by_common_factor(states: list[tuple[tuple[int, ...], ...]]) -> list[list[int]]:
    parent = list(range(len(states)))

    def find(value: int) -> int:
        while parent[value] != value:
            parent[value] = parent[parent[value]]
            value = parent[value]
        return value

    def union(left: int, right: int) -> None:
        left = find(left)
        right = find(right)
        if left != right:
            parent[right] = left

    first: dict[tuple[int, int], int] = {}
    for index, state in enumerate(states):
        for block, local_values in enumerate(state):
            for local in set(local_values):
                key = (block, local)
                if key in first:
                    union(index, first[key])
                else:
                    first[key] = index
    groups: dict[int, list[int]] = defaultdict(list)
    for index in range(len(states)):
        groups[find(index)].append(index)
    return list(groups.values())


def xray_transform(xray: tuple[int, ...], action_name: str) -> tuple[int, ...]:
    rows = xray[:5]
    cols = xray[5:]
    if action_name == "id":
        return xray
    if action_name == "rot180":
        return rows[::-1] + cols[::-1]
    if action_name == "flip_rows":
        return rows[::-1] + cols
    if action_name == "flip_cols":
        return rows + cols[::-1]
    if action_name == "rot90":
        return cols + rows[::-1]
    if action_name == "rot270":
        return cols[::-1] + rows
    if action_name == "diag":
        return cols + rows
    if action_name == "antidiag":
        return cols[::-1] + rows[::-1]
    raise ValueError(action_name)


def orbit_count_of_degrees(
    keys: set[tuple[tuple[int, ...], tuple[int, ...]]], action_names: list[str]
) -> tuple[int, dict[int, int]]:
    unseen = set(keys)
    sizes: Counter[int] = Counter()
    count = 0
    while unseen:
        counts, xray = min(unseen)
        orbit = {
            (counts, xray_transform(xray, action_name))
            for action_name in action_names
        }
        if not orbit <= keys:
            raise AssertionError("Betti-degree family is not target-action closed")
        unseen.difference_update(orbit)
        sizes[len(orbit)] += 1
        count += 1
    return count, dict(sorted(sizes.items()))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--xray-dir", type=Path, required=True)
    parser.add_argument(
        "--output", type=Path, default=Path("markov_no_go_certificate.json")
    )
    parser.add_argument(
        "--skip-degree4", action="store_true", help="omit the 1.2M-monomial degree-four audit"
    )
    args = parser.parse_args()
    sys.path.insert(0, str(args.xray_dir.resolve()))

    from verify_coarea_next import model_from_locked
    from robust_p21_quotient import Context
    from placement_quotient import target_symmetries
    from short_dual_separators import placement_action

    model = model_from_locked("p21_locked.json")
    context = Context(model)
    action_names = [name for name, _ in target_symmetries(model.target)]
    permutations = placement_action(context, target_symmetries(model.target))

    if context.columns != 72 or [len(values) for values in context.active] != [8, 24, 16, 24]:
        raise AssertionError("participating catalogue drift")
    if context.support_one:
        raise AssertionError("the locked configuration unexpectedly has support-one moves")

    # A column consists of its named-piece one-hot coordinate and its 10-entry
    # row/column X-ray.  This is the all-right-hand-side toric configuration.
    column_vectors: list[tuple[int, ...]] = []
    block_of_column: list[int] = []
    local_of_column: list[int] = []
    for block, values in enumerate(context.active):
        for local, placed in enumerate(values):
            identity = tuple(1 if index == block else 0 for index in range(4))
            column_vectors.append(identity + tuple(model.xray(placed)))
            block_of_column.append(block)
            local_of_column.append(local)

    # Complete degree-two fiber census.
    degree2: dict[tuple[int, ...], list[tuple[int, int]]] = defaultdict(list)
    for pair in itertools.combinations_with_replacement(range(context.columns), 2):
        degree2[degree_key(column_vectors, pair)].append(pair)
    repeated_degree2 = {key: values for key, values in degree2.items() if len(values) > 1}
    if len(repeated_degree2) != 218:
        raise AssertionError(f"unexpected degree-two Betti count {len(repeated_degree2)}")
    if any(len(values) != 2 for values in repeated_degree2.values()):
        raise AssertionError("a degree-two fiber is not a two-monomial fiber")

    degree2_relations = set()
    same_colour = []
    cross_colour = []
    degree2_degree_keys = set()
    for key, monomials in repeated_degree2.items():
        left = monomial_vector(monomials[0], context.columns)
        right = monomial_vector(monomials[1], context.columns)
        relation = canonical_vector(tuple(a - b for a, b in zip(left, right)))
        degree2_relations.add(relation)
        counts = key[:4]
        xray = key[4:]
        degree2_degree_keys.add((counts, xray))
        blocks = [index for index, value in enumerate(counts) for _ in range(value)]
        if len(set(blocks)) == 1:
            same_colour.append((key, monomials, relation))
        else:
            cross_colour.append((key, monomials, relation))
    if (len(same_colour), len(cross_colour)) != (74, 144):
        raise AssertionError("same/cross-colour quadratic split drift")

    locked_support_two = {canonical_vector(move) for move in context.support_two}
    if locked_support_two != {record[2] for record in cross_colour}:
        raise AssertionError("the 144 locked support-two moves are not exactly the cross-colour quadrics")

    # D4 orbit count on degree-two binomials.
    def transform_relation(vector: tuple[int, ...], permutation: tuple[int, ...]) -> tuple[int, ...]:
        image = [0] * context.columns
        for old, value in enumerate(vector):
            image[permutation[old]] = value
        return canonical_vector(tuple(image))

    def relation_orbits(relations: set[tuple[int, ...]]) -> tuple[int, dict[int, int]]:
        unseen = set(relations)
        sizes: Counter[int] = Counter()
        count = 0
        while unseen:
            value = min(unseen)
            orbit = {transform_relation(value, permutation) for permutation in permutations}
            if not orbit <= relations:
                raise AssertionError("relation set is not D4-closed")
            unseen.difference_update(orbit)
            sizes[len(orbit)] += 1
            count += 1
        return count, dict(sorted(sizes.items()))

    same_orbit_count, same_orbit_sizes = relation_orbits({record[2] for record in same_colour})
    cross_orbit_count, cross_orbit_sizes = relation_orbits({record[2] for record in cross_colour})
    if (same_orbit_count, cross_orbit_count) != (23, 24):
        raise AssertionError("degree-two orbit count drift")

    # Canonical indispensable quadratic in block zero.
    witness_key = (2, 0, 0, 0) + (5, 2, 0, 2, 5, 3, 2, 4, 2, 3)
    witness_monomials = repeated_degree2.get(witness_key)
    expected_witness = [(0, 7), (1, 6)]
    if witness_monomials != expected_witness:
        raise AssertionError((witness_monomials, expected_witness))

    # A two-relation Laurent-saturation witness.  With the frozen support-two
    # ordering, -move[0] + move[18] is the missing same-block quadratic
    # e_(0,0)+e_(0,7)-e_(0,1)-e_(0,6).  Polynomially,
    #   x_(0,7)b_0 - x_(0,1)b_18 = -x_(1,23) q.
    # Thus q lies in the saturation of the squarefree cross-block ideal, but
    # it cannot act in the nonnegative RHS (2,0,0,0), where the catalyst
    # block has multiplicity zero.
    target_same_block = [0] * context.columns
    for index in (0, 7):
        target_same_block[index] += 1
    for index in (1, 6):
        target_same_block[index] -= 1
    saturation_combination = tuple(
        -context.moves[0][index] + context.moves[18][index]
        for index in range(context.columns)
    )
    if saturation_combination != tuple(target_same_block):
        raise AssertionError("two-relation saturation witness drift")
    support_two_compact = []
    for move_index in (0, 18):
        move = context.moves[move_index]
        support_two_compact.append({
            "move_index": move_index,
            "negative": [i for i, value in enumerate(move) if value < 0],
            "positive": [i for i, value in enumerate(move) if value > 0],
        })

    # No squarefree support<=4 move can act in a fiber with count vector
    # (2,0,0,0): every available nonzero move changes at least two *distinct*
    # named piece blocks.  The two monomials are therefore isolated.  Because
    # the fiber contains exactly two relatively-prime monomials, its binomial
    # is indispensable in every Markov basis.

    # A stronger degree-seven indispensable witness inside block three.
    degree7_rhs = (18, 14, 5, 5, 0, 4, 10, 14, 10, 4)
    degree7_states = []
    block = 3
    block_xrays = [tuple(model.xray(placed)) for placed in context.active[block]]
    for state in itertools.combinations_with_replacement(range(len(block_xrays)), 7):
        xray = tuple(sum(block_xrays[index][j] for index in state) for j in range(10))
        if xray == degree7_rhs:
            degree7_states.append(state)
    expected_degree7 = [
        (0, 0, 5, 5, 5, 8, 8),
        (3, 3, 4, 4, 6, 6, 6),
    ]
    if degree7_states != expected_degree7:
        raise AssertionError(f"degree-seven witness drift: {degree7_states}")
    if set(degree7_states[0]) & set(degree7_states[1]):
        raise AssertionError("degree-seven witness monomials share a variable")

    # D4 orbit size of the degree-seven indispensable binomial.
    offset = context.offsets[block]
    def transform_local_state(state: tuple[int, ...], permutation: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(sorted(permutation[offset + local] - offset for local in state))
    degree7_orbit = {
        min(
            (
                transform_local_state(degree7_states[0], permutation),
                transform_local_state(degree7_states[1], permutation),
            ),
            (
                transform_local_state(degree7_states[1], permutation),
                transform_local_state(degree7_states[0], permutation),
            ),
        )
        for permutation in permutations
    }
    if len(degree7_orbit) != 4:
        raise AssertionError("degree-seven D4 orbit-size drift")

    # Low-degree Betti-fiber census.  Fibers are connected below degree d by
    # common-factor edges; c(b)-1 is the number of minimal generators required
    # in A-degree b.
    betti_summaries = {}
    max_degree = 3 if args.skip_degree4 else 4
    for total_degree in range(2, max_degree + 1):
        block_state_cache: dict[tuple[int, int], list[tuple[tuple[int, ...], tuple[int, ...]]]] = {}

        def block_states(block_index: int, count: int):
            cache_key = (block_index, count)
            if cache_key not in block_state_cache:
                values = []
                for local_values in itertools.combinations_with_replacement(
                    range(len(context.active[block_index])), count
                ):
                    xray = tuple(
                        sum(
                            model.xray(context.active[block_index][local])[j]
                            for local in local_values
                        )
                        for j in range(10)
                    )
                    values.append((local_values, xray))
                block_state_cache[cache_key] = values
            return block_state_cache[cache_key]

        betti_records = []
        monomial_count = 0
        fiber_count = 0
        for counts in itertools.product(range(total_degree + 1), repeat=4):
            if sum(counts) != total_degree:
                continue
            groups: dict[tuple[int, ...], list[tuple[tuple[int, ...], ...]]] = defaultdict(list)
            lists = [block_states(block_index, count) for block_index, count in enumerate(counts)]
            for combination in itertools.product(*lists):
                state = tuple(record[0] for record in combination)
                xray = tuple(sum(record[1][j] for record in combination) for j in range(10))
                groups[xray].append(state)
            monomial_count += sum(map(len, groups.values()))
            fiber_count += len(groups)
            for xray, states in groups.items():
                if len(states) < 2:
                    continue
                components = components_by_common_factor(states)
                if len(components) > 1:
                    betti_records.append(
                        {
                            "counts": tuple(counts),
                            "xray": xray,
                            "fiber_size": len(states),
                            "component_sizes": tuple(sorted(map(len, components))),
                        }
                    )
        minimum_generators = sum(len(record["component_sizes"]) - 1 for record in betti_records)
        degree_keys = {(record["counts"], record["xray"]) for record in betti_records}
        orbit_count, orbit_sizes = orbit_count_of_degrees(degree_keys, action_names)
        betti_summaries[str(total_degree)] = {
            "monomials": monomial_count,
            "fibers": fiber_count,
            "betti_fibers": len(betti_records),
            "minimum_generators_in_degree": minimum_generators,
            "component_size_profile": {
                str(key): value
                for key, value in sorted(Counter(record["component_sizes"] for record in betti_records).items())
            },
            "betti_degree_orbits": orbit_count,
            "betti_degree_orbit_sizes": orbit_sizes,
        }

    expected = {
        "2": (2_628, 2_410, 218, 218, 47),
        "3": (64_824, 49_772, 996, 996, 179),
    }
    if not args.skip_degree4:
        expected["4"] = (1_215_450, 712_526, 5_705, 5_727, 1_165)
    for degree, values in expected.items():
        record = betti_summaries[degree]
        actual = (
            record["monomials"],
            record["fibers"],
            record["betti_fibers"],
            record["minimum_generators_in_degree"],
            record["betti_degree_orbits"],
        )
        if actual != values:
            raise AssertionError((degree, actual, values))

    lower_bound_generators = sum(
        record["minimum_generators_in_degree"] for record in betti_summaries.values()
    )

    certificate = {
        "schema": "p42.all_rhs_markov_no_go.v1",
        "row": [4, 5, 12, 13],
        "configuration": {
            "variables": context.columns,
            "piece_blocks": [len(values) for values in context.active],
            "matrix_columns": "piece-identity one-hot + joint row/column X-ray",
            "kernel_rank": context.kernel_rank,
        },
        "terminology_correction": {
            "current_support_filtration": "squarefree one-copy piece-support filtration",
            "not_equivalent_to": [
                "toric degree filtration",
                "Graver support filtration",
                "all-right-hand-side Markov filtration",
            ],
        },
        "degree_two": {
            "monomials": 2_628,
            "fibers": 2_410,
            "indispensable_binomials": 218,
            "cross_colour_existing": 144,
            "same_colour_missing": 74,
            "all_D4_orbits": same_orbit_count + cross_orbit_count,
            "same_colour_D4_orbits": same_orbit_count,
            "cross_colour_D4_orbits": cross_orbit_count,
            "same_colour_orbit_sizes": same_orbit_sizes,
            "cross_colour_orbit_sizes": cross_orbit_sizes,
            "canonical_witness": {
                "piece_block": 0,
                "local_monomials": [list(value) for value in witness_monomials],
                "aggregate_xray": list(witness_key[4:]),
                "binomial": "x_(0,0)*x_(0,7) - x_(0,1)*x_(0,6)",
                "fiber_size": 2,
                "components": 2,
                "saturation_witness": {
                    "support_two_moves": support_two_compact,
                    "lattice_identity": "q = -move[0] + move[18]",
                    "polynomial_identity": "x_(0,7)*b_0 - x_(0,1)*b_18 = -x_(1,23)*q",
                    "interpretation": "the missing binomial is available only after cancellation through an auxiliary named-piece block"
                },
            },
        },
        "degree_seven_indispensable_witness": {
            "piece_block": 3,
            "count_vector": [0, 0, 0, 7],
            "aggregate_xray": list(degree7_rhs),
            "local_monomials": [list(value) for value in degree7_states],
            "fiber_size": 2,
            "common_factor": 0,
            "D4_orbit_size": len(degree7_orbit),
            "consequence": "every Markov basis has degree at least seven",
        },
        "low_degree_betti_census": betti_summaries,
        "minimal_generator_lower_bound_through_audited_degrees": lower_bound_generators,
        "verdict": {
            "squarefree_support_le_4_is_lattice_generating": True,
            "squarefree_support_le_4_is_all_rhs_Markov": False,
            "Markov_degree_lower_bound": 7,
            "full_Markov_degree": "open",
        },
    }
    args.output.write_text(
        json.dumps(certificate, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print("PASS all-RHS Markov no-go")
    print("degree2 indispensable / missing same-colour / D4 orbits:", 218, 74, 47)
    print("degree7 indispensable witness: PASS; Markov degree >= 7")
    print("low-degree Betti census:", {k: (v['betti_fibers'], v['minimum_generators_in_degree']) for k,v in betti_summaries.items()})


if __name__ == "__main__":
    main()
