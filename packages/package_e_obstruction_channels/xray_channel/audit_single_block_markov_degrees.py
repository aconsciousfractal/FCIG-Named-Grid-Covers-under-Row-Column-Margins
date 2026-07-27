#!/usr/bin/env python3
"""Exact single-piece-block Betti-degree census through degree seven.

Each count vector is supported on one named piece block, so every Betti fiber
found here embeds unchanged in the full four-block Cayley configuration.  The
result gives rigorous lower bounds on the full Markov degree without computing
an all-variable Markov basis.
"""
from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


def components(states: list[tuple[int, ...]]) -> list[list[int]]:
    parent = list(range(len(states)))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        a, b = find(a), find(b)
        if a != b:
            parent[b] = a

    first: dict[int, int] = {}
    for index, state in enumerate(states):
        for variable in set(state):
            if variable in first:
                union(index, first[variable])
            else:
                first[variable] = index
    result: dict[int, list[int]] = defaultdict(list)
    for index in range(len(states)):
        result[find(index)].append(index)
    return list(result.values())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--xray-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("single_block_markov_degrees.json"))
    args = parser.parse_args()
    sys.path.insert(0, str(args.xray_dir.resolve()))

    from verify_coarea_next import model_from_locked
    from robust_p21_quotient import Context

    model = model_from_locked("p21_locked.json")
    context = Context(model)
    xrays = [
        [tuple(model.xray(placed)) for placed in values]
        for values in context.active
    ]
    result = {
        "schema": "p42.single_block_markov_degree_census.v1",
        "row": [4, 5, 12, 13],
        "piece_block_sizes": [len(values) for values in context.active],
        "degrees": {},
    }
    highest = 0
    indispensable_witnesses = []
    for block in range(4):
        block_result = {}
        for degree in range(2, 8):
            groups: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
            for state in itertools.combinations_with_replacement(range(len(xrays[block])), degree):
                rhs = tuple(sum(xrays[block][index][j] for index in state) for j in range(10))
                groups[rhs].append(state)
            betti = []
            for rhs, states in groups.items():
                if len(states) < 2:
                    continue
                comps = components(states)
                if len(comps) > 1:
                    record = {
                        "rhs": list(rhs),
                        "fiber_size": len(states),
                        "component_sizes": sorted(map(len, comps)),
                    }
                    betti.append(record)
                    highest = max(highest, degree)
                    if len(states) == 2 and not (set(states[0]) & set(states[1])):
                        indispensable_witnesses.append(
                            {
                                "block": block,
                                "degree": degree,
                                "rhs": list(rhs),
                                "monomials": [list(states[0]), list(states[1])],
                            }
                        )
            block_result[str(degree)] = {
                "monomials": sum(map(len, groups.values())),
                "fibers": len(groups),
                "betti_fibers": len(betti),
                "minimum_generators_in_degree": sum(len(r["component_sizes"]) - 1 for r in betti),
                "fiber_size_profile": dict(sorted(Counter(r["fiber_size"] for r in betti).items())),
                "component_size_profile": {
                    str(key): value
                    for key, value in sorted(Counter(tuple(r["component_sizes"]) for r in betti).items())
                },
                "first_betti_witness": betti[0] if betti else None,
            }
        result["degrees"][str(block)] = block_result
    result["highest_certified_Betti_degree"] = highest
    result["Markov_degree_lower_bound"] = highest
    # Pin the clean degree-seven two-monomial witness.
    target = {
        "block": 3,
        "degree": 7,
        "rhs": [18, 14, 5, 5, 0, 4, 10, 14, 10, 4],
        "monomials": [[0, 0, 5, 5, 5, 8, 8], [3, 3, 4, 4, 6, 6, 6]],
    }
    if target not in indispensable_witnesses:
        raise AssertionError("canonical degree-seven indispensable witness missing")
    result["canonical_degree_seven_witness"] = target
    args.output.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print("PASS single-block Betti census through degree seven")
    print("Markov degree lower bound:", highest)
    for block, values in result["degrees"].items():
        profile = {degree: row["betti_fibers"] for degree, row in values.items() if row["betti_fibers"]}
        print("block", block, profile)


if __name__ == "__main__":
    main()
