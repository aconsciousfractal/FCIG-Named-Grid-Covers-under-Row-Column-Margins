#!/usr/bin/env python3
"""Mutation tests for the co-area residual-state experiment."""
from __future__ import annotations

import copy
import json
from dataclasses import replace

import coarea_fpt as principal


def expect_rejection(label: str, action) -> None:
    try:
        action()
    except (AssertionError, ValueError):
        print(f"PASS mutation rejected: {label}")
        return
    raise AssertionError(f"mutation was accepted: {label}")


def main() -> int:
    result = json.loads(principal.OUTPUT.read_text(encoding="utf-8"))
    principal.validate_result(result)
    print("PASS control: stored result validates")

    c32, _, _ = principal.load_libraries()
    prepared = principal.PreparedLibrary.build(c32)
    positive_quad = None
    positive_nodes = None
    for quad in prepared.candidate_quaternes():
        nodes, _ = principal.row_fiber(prepared, quad)
        if nodes:
            positive_quad = quad
            positive_nodes = nodes
            break
    if positive_quad is None or positive_nodes is None:
        raise AssertionError("control could not find a positive C32 row")
    baseline_count = len(positive_nodes)
    largest_position = principal.choose_largest(prepared, positive_quad)
    residual_position = next(
        position
        for position in range(4)
        if position != largest_position
    )
    residual_piece = positive_quad[residual_position]
    required_placement = positive_nodes[0][residual_position]
    old_values = prepared.placements[residual_piece]
    old_xrays = prepared.placement_xrays[residual_piece]
    kept = [
        (placed, vector)
        for placed, vector in zip(old_values, old_xrays)
        if placed != required_placement
    ]
    mutated_placements = list(prepared.placements)
    mutated_xrays = list(prepared.placement_xrays)
    mutated_placements[residual_piece] = tuple(
        placed for placed, _ in kept
    )
    mutated_xrays[residual_piece] = tuple(vector for _, vector in kept)
    deleted = replace(
        prepared,
        placements=tuple(mutated_placements),
        placement_xrays=tuple(mutated_xrays),
    )
    changed_nodes, _ = principal.row_fiber(deleted, positive_quad)
    if len(changed_nodes) >= baseline_count:
        raise AssertionError("deleting a participating placement did not shrink the fiber")
    print(
        "PASS mutation detected: deleted participating residual placement "
        f"{baseline_count}->{len(changed_nodes)}"
    )

    illegal_placements = list(prepared.placements)
    illegal_placements[residual_piece] = (
        *illegal_placements[residual_piece],
        frozenset({(999, 999)}),
    )
    illegal = replace(prepared, placements=tuple(illegal_placements))
    expect_rejection(
        "out-of-target placement",
        illegal.validate_placements,
    )

    removed_cell = min(c32.target)
    changed_target = replace(c32, target=c32.target - {removed_cell})
    changed_prepared = principal.PreparedLibrary.build(changed_target)
    if (
        len(changed_prepared.candidate_quaternes())
        == len(prepared.candidate_quaternes())
        and changed_prepared.target_xray == prepared.target_xray
    ):
        raise AssertionError("target-cell mutation was computationally invisible")
    print("PASS mutation detected: one target cell removed")

    corrupt_bound = copy.deepcopy(result)
    row = corrupt_bound["libraries"][0]["rows"][0]
    row["active_grid_max"] = row["active_grid_bound_q_squared"] + 1
    expect_rejection(
        "stored active-grid/co-area bound",
        lambda: principal.validate_result(corrupt_bound),
    )

    corrupt_verdict = copy.deepcopy(result)
    c46_record = next(
        record
        for record in corrupt_verdict["libraries"]
        if record["library"] == "C46"
    )
    c46_record["repair_exact"] = False
    expect_rejection(
        "stored expected library verdict",
        lambda: principal.validate_result(corrupt_verdict),
    )

    corrupt_count = copy.deepcopy(result)
    p49_record = next(
        record
        for record in corrupt_count["libraries"]
        if record["library"] == "P49-base"
    )
    p49_record["fiber_nodes"] -= 1
    expect_rejection(
        "stored exact fiber count",
        lambda: principal.validate_result(corrupt_count),
    )

    print("PASS: 1 control + 6 mutations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
