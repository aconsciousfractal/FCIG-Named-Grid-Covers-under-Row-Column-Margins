#!/usr/bin/env python3
"""Independent checker for the C32 structural-analysis artifact.

This checker imports neither the realization engine nor ``analyse_c32.py``.
It reconstructs the D4 placement catalogues from the source lock, recomputes
the complete row/column margin fibers, and tests the coherence obstruction
directly from the explicit certified tilings.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path
from typing import Iterable


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LOCK_PATH = ROOT / "registry" / "c32_source_lock.json"
BUNDLE_PATH = HERE / "R_certificates.json"
ANALYSIS_PATH = ROOT / "results" / "c32_structural_analysis.json"

Cell = tuple[int, int]
Shape = frozenset[Cell]


def normalized(cells: Iterable[Cell]) -> Shape:
    values = tuple(cells)
    row0 = min(row for row, _ in values)
    col0 = min(col for _, col in values)
    return frozenset((row - row0, col - col0) for row, col in values)


def orientations(shape: Shape) -> tuple[Shape, ...]:
    transforms = (
        lambda row, col: (row, col),
        lambda row, col: (row, -col),
        lambda row, col: (-row, col),
        lambda row, col: (-row, -col),
        lambda row, col: (col, row),
        lambda row, col: (col, -row),
        lambda row, col: (-col, row),
        lambda row, col: (-col, -row),
    )
    return tuple(
        sorted(
            {
                normalized(transform(row, col) for row, col in shape)
                for transform in transforms
            },
            key=lambda value: tuple(sorted(value)),
        )
    )


def placements(shape: Shape, target: Shape) -> tuple[Shape, ...]:
    result: set[Shape] = set()
    for oriented in orientations(shape):
        height = max(row for row, _ in oriented) + 1
        width = max(col for _, col in oriented) + 1
        for top in range(7 - height):
            for left in range(7 - width):
                placed = frozenset(
                    (row + top, col + left) for row, col in oriented
                )
                if placed <= target:
                    result.add(placed)
    return tuple(sorted(result, key=lambda value: tuple(sorted(value))))


def margin(shape: Shape) -> tuple[int, ...]:
    result = [0] * 12
    for row, col in shape:
        result[row] += 1
        result[6 + col] += 1
    return tuple(result)


def fiber_counts(
    quad: tuple[int, ...],
    catalogue: dict[int, tuple[Shape, ...]],
    target: Shape,
) -> tuple[int, int]:
    target_margin = margin(target)
    first_half: dict[tuple[int, ...], list[tuple[Shape, Shape]]] = defaultdict(list)
    for first in catalogue[quad[0]]:
        first_margin = margin(first)
        for second in catalogue[quad[1]]:
            second_margin = margin(second)
            key = tuple(a + b for a, b in zip(first_margin, second_margin))
            if all(a <= b for a, b in zip(key, target_margin)):
                first_half[key].append((first, second))

    nodes = 0
    tilings = 0
    for third in catalogue[quad[2]]:
        third_margin = margin(third)
        for fourth in catalogue[quad[3]]:
            fourth_margin = margin(fourth)
            complement = tuple(
                target_margin[index] - third_margin[index] - fourth_margin[index]
                for index in range(12)
            )
            for first, second in first_half.get(complement, ()):
                nodes += 1
                coverage = Counter()
                for placed in (first, second, third, fourth):
                    coverage.update(placed)
                tilings += int(
                    len(coverage) == len(target)
                    and all(value == 1 for value in coverage.values())
                )
    return nodes, tilings


def affine(quad: Iterable[int]) -> bool:
    value = 0
    for label in quad:
        value ^= label - 1
    return value == 0


def parsed_tilings(record: dict) -> tuple[dict[int, Shape], ...]:
    return tuple(
        {
            int(item["piece"]): frozenset(tuple(cell) for cell in item["cells"])
            for item in tiling
        }
        for tiling in record["tilings"]
    )


def main() -> int:
    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    bundle = json.loads(BUNDLE_PATH.read_text(encoding="utf-8"))
    analysis = json.loads(ANALYSIS_PATH.read_text(encoding="utf-8"))
    model = lock["canonical_model"]
    target = frozenset(
        (row, col)
        for row in range(6)
        for col in range(6)
        if [row, col] not in model["target"]["holes"]
    )
    pieces = {
        int(label): frozenset(tuple(cell) for cell in cells)
        for label, cells in model["pieces"].items()
    }
    catalogue = {
        label: placements(shape, target) for label, shape in sorted(pieces.items())
    }
    quads = tuple(
        quad for quad in combinations(range(1, 17), 4) if sum(quad) == len(target)
    )
    positive = {
        tuple(record["source_piece_ids"])
        for record in bundle["records"].values()
        if record["tiles"]
    }
    displayed = {
        tuple(record["source_piece_ids"])
        for record in bundle["records"].values()
        if record["source_displayed_lines"]
    }

    row_counts = []
    total_nodes = 0
    total_tilings = 0
    margin_positive: set[tuple[int, ...]] = set()
    impure: list[tuple[int, ...]] = []
    for quad in quads:
        nodes, tilings = fiber_counts(quad, catalogue, target)
        row_counts.append((quad, nodes, tilings))
        total_nodes += nodes
        total_tilings += tilings
        if nodes:
            margin_positive.add(quad)
        if nodes != tilings:
            impure.append(quad)

    square = tuple(tuple(row) for row in model["durer_source_square"])
    board = tuple(label for row in square for label in row)
    position = {label: index for index, label in enumerate(board)}
    board_rows = tuple(tuple(4 * row + col for col in range(4)) for row in range(4))
    board_columns = tuple(
        tuple(4 * row + col for row in range(4)) for col in range(4)
    )

    def line_choices(line: tuple[int, ...]) -> tuple[dict[int, Shape], ...]:
        quad = tuple(sorted(board[index] for index in line))
        record = bundle["records"][",".join(map(str, quad))]
        return tuple(
            {position[label]: placed for label, placed in tiling.items()}
            for tiling in parsed_tilings(record)
        )

    row_choices = tuple(line_choices(line) for line in board_rows)
    row_assignments = []
    for choice in product(*row_choices):
        assignment: dict[int, Shape] = {}
        for partial in choice:
            assignment.update(partial)
        row_assignments.append(assignment)

    def exact_partition(assignment: dict[int, Shape], line: tuple[int, ...]) -> bool:
        coverage = Counter()
        for index in line:
            coverage.update(assignment[index])
        return set(coverage) == set(target) and all(
            value == 1 for value in coverage.values()
        )

    first_column_survivors = sum(
        exact_partition(assignment, board_columns[0])
        for assignment in row_assignments
    )

    expected_rows = [
        (
            tuple(row["source_piece_ids"]),
            row["margin_nodes"],
            row["tiling_nodes"],
        )
        for row in analysis["row_column_fiber"]["rows"]
    ]
    observed_non_affine = sorted(quad for quad in positive if not affine(quad))
    checks = {
        "certificate hash": (
            analysis["input"]["certificate_sha256"]
            == hashlib.sha256(BUNDLE_PATH.read_bytes()).hexdigest()
        ),
        "complete 86-row carrier": len(quads) == 86,
        "20 positive rows": len(positive) == 20,
        "10 displayed witnesses": len(displayed) == 10,
        "seven non-affine positives": (
            observed_non_affine
            == [tuple(value) for value in analysis["affine_selection"]["positive_non_affine"]]
            and len(observed_non_affine) == 7
        ),
        "fiber row table": row_counts == expected_rows,
        "fiber totals 136/136": total_nodes == total_tilings == 136,
        "fiber support exact": margin_positive == positive,
        "fiber purity": not impure,
        "256 row assignments": len(row_assignments) == 256,
        "first-column obstruction": first_column_survivors == 0,
        "analysis coherence values": (
            analysis["coherent"]["row_coherent_assignments"] == 256
            and analysis["coherent"]["successive_column_filter_counts"]
            == [0, 0, 0, 0]
            and analysis["coherent"]["fully_coherent_assignments"] == 0
        ),
    }
    failures = [name for name, passed in checks.items() if not passed]
    for name, passed in checks.items():
        print(f"[{'PASS' if passed else 'FAIL'}] {name}")
    print(f"\nSTATUS: {'PASS' if not failures else 'FAIL'} ({len(checks) - len(failures)}/{len(checks)})")
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
