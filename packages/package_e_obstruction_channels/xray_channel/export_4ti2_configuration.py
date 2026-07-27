#!/usr/bin/env python3
"""Export the robust-P21 participating configuration for 4ti2/Macaulay2.

The configuration column for placement P of named piece block i is
    e_i | X_row(P) | X_col(P),
so the nonnegative fibers are exactly the named-piece-count / row-column-X-ray
fibers studied in the all-RHS Markov question.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from sympy import Matrix


def write_4ti2(path: Path, rows: list[list[int]]) -> None:
    path.write_text(
        f"{len(rows)} {len(rows[0])}\n"
        + "\n".join(" ".join(map(str, row)) for row in rows)
        + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--xray-dir", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    xray_dir = args.xray_dir.resolve()
    out = args.out_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(xray_dir))

    from verify_coarea_next import model_from_locked
    from robust_p21_quotient import Context, QUAD
    from placement_quotient import target_symmetries
    from short_dual_separators import placement_action

    model = model_from_locked("p21_locked.json")
    context = Context(model)
    if context.columns != 72 or context.kernel_rank != 60:
        raise AssertionError("robust P21 participating configuration drift")

    rows = [list(map(int, row)) for row in context.constraint_rows]
    matrix = Matrix(rows)
    if matrix.rank() != 12:
        raise AssertionError(f"expected rank 12, got {matrix.rank()}")

    # Select an independent subset of the original integer rows.  Row pivots are
    # column pivots of the transpose.
    independent = list(matrix.T.rref()[1])
    reduced_rows = [rows[index] for index in independent]
    if Matrix(reduced_rows).rank() != 12:
        raise AssertionError("rank-reduced export failed")

    write_4ti2(out / "p21_participating_markov_14x72.mat", rows)
    write_4ti2(out / "p21_participating_markov_rank12.mat", reduced_rows)
    (out / "p21_participating_markov.sign").write_text(
        "1 72\n" + " ".join(["1"] * 72) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    variables = []
    for position, values in enumerate(context.active):
        for local, placed in enumerate(values):
            coordinate = context.offsets[position] + local
            variables.append(
                {
                    "coordinate": coordinate,
                    "symbol": f"x_{position}_{local}",
                    "named_position": position,
                    "source_piece_index": QUAD[position],
                    "local_placement": local,
                    "cells": [list(cell) for cell in sorted(placed)],
                    "xray": list(model.xray(placed)),
                }
            )

    actions = target_symmetries(model.target)
    permutations = placement_action(context, actions)
    metadata = {
        "schema": "p42.robust_p21_markov_export.v1",
        "row": list(QUAD),
        "target": {"rows": 5, "cols": 5},
        "variables": 72,
        "matrix_rows_full": 14,
        "matrix_rank": 12,
        "independent_original_row_indices": independent,
        "row_semantics_full": [
            "piece_count_position_0",
            "piece_count_position_1",
            "piece_count_position_2",
            "piece_count_position_3",
            "target_row_0",
            "target_row_1",
            "target_row_2",
            "target_row_3",
            "target_row_4",
            "target_col_0",
            "target_col_1",
            "target_col_2",
            "target_col_3",
            "target_col_4",
        ],
        "D4_action_order": [name for name, _ in actions],
        "D4_variable_permutations": [list(p) for p in permutations],
        "variables_table": variables,
        "recommended_4ti2_command": "markov --precision=arbitrary --minimal=yes p21_participating_markov_rank12",
    }
    (out / "p21_participating_markov_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print("PASS exported robust-P21 4ti2 configuration")
    print("matrix: 14x72, rank 12; kernel rank 60")
    print("independent rows:", independent)


if __name__ == "__main__":
    main()
