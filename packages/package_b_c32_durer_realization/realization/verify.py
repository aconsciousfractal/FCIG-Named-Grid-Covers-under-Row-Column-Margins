#!/usr/bin/env python3
"""Independent verifier for the C32 certificate bundle.

The verifier deliberately imports neither ``engine.py`` nor ``certify.py``.
It regenerates D4 placements with explicit coordinate maps and enumerates
covers by branching on the most constrained uncovered target cell.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from itertools import combinations
from pathlib import Path
from typing import Iterable


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DEFAULT_BUNDLE = HERE / "R_certificates.json"
DEFAULT_LOCK = ROOT / "registry" / "c32_source_lock.json"


Cell = tuple[int, int]
Shape = frozenset[Cell]
TilingKey = tuple[tuple[int, tuple[Cell, ...]], ...]


def normalized(cells: Iterable[Cell]) -> Shape:
    cells = tuple(cells)
    row0 = min(row for row, _ in cells)
    col0 = min(col for _, col in cells)
    return frozenset((row - row0, col - col0) for row, col in cells)


def independent_orientations(shape: Shape) -> tuple[Shape, ...]:
    maps = (
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
            {normalized(transform(row, col) for row, col in shape) for transform in maps},
            key=lambda cells: tuple(sorted(cells)),
        )
    )


def independent_placements(shape: Shape, target: Shape) -> tuple[Shape, ...]:
    result: set[Shape] = set()
    for oriented in independent_orientations(shape):
        height = max(row for row, _ in oriented) + 1
        width = max(col for _, col in oriented) + 1
        for top in range(7 - height):
            for left in range(7 - width):
                placed = frozenset(
                    (row + top, col + left) for row, col in oriented
                )
                if placed <= target:
                    result.add(placed)
    return tuple(sorted(result, key=lambda cells: tuple(sorted(cells))))


def independent_tilings(
    labels: tuple[int, ...],
    catalogue: dict[int, tuple[Shape, ...]],
    target: Shape,
) -> tuple[TilingKey, ...]:
    result: set[TilingKey] = set()
    assignment: dict[int, Shape] = {}

    def search(remaining_labels: tuple[int, ...], remaining: Shape) -> None:
        if not remaining_labels:
            if not remaining:
                result.add(
                    tuple(
                        (label, tuple(sorted(assignment[label])))
                        for label in sorted(assignment)
                    )
                )
            return
        choices_by_cell: list[tuple[int, Cell, list[tuple[int, Shape]]]] = []
        for cell in sorted(remaining):
            options = [
                (label, placed)
                for label in remaining_labels
                for placed in catalogue[label]
                if cell in placed and placed <= remaining
            ]
            choices_by_cell.append((len(options), cell, options))
        _, _, options = min(choices_by_cell, key=lambda item: (item[0], item[1]))
        for label, placed in options:
            assignment[label] = placed
            search(
                tuple(value for value in remaining_labels if value != label),
                remaining - placed,
            )
            del assignment[label]

    search(tuple(sorted(labels)), target)
    return tuple(sorted(result))


def affine(quad: Iterable[int]) -> bool:
    value = 0
    for label in quad:
        value ^= label - 1
    return value == 0


def certificate_tiling_key(tiling: list[dict[str, object]]) -> TilingKey:
    return tuple(
        sorted(
            (
                int(item["piece"]),
                tuple(sorted(tuple(cell) for cell in item["cells"])),
            )
            for item in tiling
        )
    )


def panel_tiling_key(panel: dict) -> TilingKey:
    rows = panel["rows"]
    holes = sorted(
        (row, col)
        for row, text in enumerate(rows)
        for col, value in enumerate(text)
        if value == "."
    )
    if holes == [(1, 1), (4, 4)]:
        transform = lambda row, col: (row, col)
    elif holes == [(1, 4), (4, 1)]:
        transform = lambda row, col: (row, 5 - col)
    else:
        raise AssertionError(f"unexpected panel holes: {panel['id']} {holes}")
    result = []
    for color in "RBYG":
        placed = frozenset(
            transform(row, col)
            for row, text in enumerate(rows)
            for col, value in enumerate(text)
            if value == color
        )
        result.append((len(placed), tuple(sorted(placed))))
    return tuple(sorted(result))


def verify_bundle(bundle: dict, lock: dict) -> dict[str, object]:
    errors: list[str] = []
    model = lock["canonical_model"]
    target = frozenset(
        (row, col)
        for row in range(model["target"]["rows"])
        for col in range(model["target"]["columns"])
        if [row, col] not in model["target"]["holes"]
    )
    pieces = {
        int(label): frozenset(tuple(cell) for cell in cells)
        for label, cells in model["pieces"].items()
    }
    catalogue = {
        label: independent_placements(shape, target)
        for label, shape in sorted(pieces.items())
    }
    expected_quads = tuple(
        quad for quad in combinations(range(1, 17), 4) if sum(quad) == len(target)
    )
    expected_keys = {",".join(map(str, quad)) for quad in expected_quads}

    lock_digest = hashlib.sha256(DEFAULT_LOCK.read_bytes()).hexdigest()
    if bundle.get("source", {}).get("source_lock_sha256") != lock_digest:
        errors.append("source lock SHA-256 mismatch")
    if bundle.get("source", {}).get("raster_sha256") != lock["source"]["sha256"]:
        errors.append("raster SHA-256 mismatch")
    normalization = bundle.get("normalization", {})
    if {
        tuple(cell) for cell in normalization.get("target_cells", ())
    } != target:
        errors.append("bundle target differs from source lock")
    bundle_pieces = {
        int(label): frozenset(tuple(cell) for cell in cells)
        for label, cells in normalization.get("pieces", {}).items()
    }
    if bundle_pieces != pieces:
        errors.append("bundle pieces differ from source lock")

    records = bundle.get("records", {})
    if set(records) != expected_keys:
        errors.append("record-key set is not the complete 86-row carrier")

    source_square = tuple(tuple(row) for row in model["durer_source_square"])
    owner_square = tuple(tuple(row) for row in model["owner_durer_complement_square"])
    position_by_value = {
        source_square[row][col]: 4 * row + col
        for row in range(4)
        for col in range(4)
    }
    line_lookup: dict[tuple[int, ...], list[str]] = {}
    for name, values in model["magic_lines"].items():
        line_lookup.setdefault(tuple(sorted(values)), []).append(name)

    computed: dict[tuple[int, ...], tuple[TilingKey, ...]] = {}
    positive = 0
    total_tilings = 0
    positive_affine = 0
    displayed_positive = 0
    for index, quad in enumerate(expected_quads, 1):
        key = ",".join(map(str, quad))
        record = records.get(key)
        if not isinstance(record, dict):
            continue
        tilings = independent_tilings(quad, catalogue, target)
        computed[quad] = tilings
        expected_positions = sorted(position_by_value[label] for label in quad)
        expected_owner = sorted(17 - label for label in quad)
        expected_lines = sorted(line_lookup.get(quad, ()))
        expected_affine = affine(quad)
        cert_tilings = tuple(
            sorted(certificate_tiling_key(tiling) for tiling in record.get("tilings", ()))
        )
        if record.get("row_id") != f"C32-Q{index:03d}":
            errors.append(f"{key}: row id mismatch")
        if record.get("source_piece_ids") != list(quad):
            errors.append(f"{key}: source-piece id mismatch")
        if record.get("board_positions") != expected_positions:
            errors.append(f"{key}: board-position crosswalk mismatch")
        if record.get("owner_complement_values") != expected_owner:
            errors.append(f"{key}: owner complement crosswalk mismatch")
        if record.get("affine_value_minus_one") is not expected_affine:
            errors.append(f"{key}: affine flag mismatch")
        if record.get("source_displayed_lines") != expected_lines:
            errors.append(f"{key}: source-line annotation mismatch")
        if record.get("tiles") is not bool(tilings):
            errors.append(f"{key}: tiling verdict mismatch")
        if record.get("tiling_count") != len(tilings):
            errors.append(f"{key}: tiling count mismatch")
        if cert_tilings != tilings:
            errors.append(f"{key}: explicit tiling set mismatch")
        expected_placement_counts = {
            str(label): len(catalogue[label]) for label in quad
        }
        if record.get("placement_counts") != expected_placement_counts:
            errors.append(f"{key}: placement-count mismatch")
        negative = record.get("negative_proof")
        if tilings and negative is not None:
            errors.append(f"{key}: positive row carries a negative proof")
        if not tilings and (
            not isinstance(negative, dict)
            or negative.get("exhaustive_covers") != 0
        ):
            errors.append(f"{key}: negative row lacks an exhaustive-zero record")
        if tilings:
            positive += 1
            total_tilings += len(tilings)
            positive_affine += int(expected_affine)
            displayed_positive += int(bool(expected_lines))

    panel_failures = []
    canonical_panel_tilings: set[TilingKey] = set()
    for panel in lock["pixel_transcription"]["panels"]:
        tiling = panel_tiling_key(panel)
        quad = tuple(label for label, _ in tiling)
        canonical_panel_tilings.add(tiling)
        if tiling not in computed.get(quad, ()):
            panel_failures.append(panel["id"])
    if panel_failures:
        errors.append(f"source panel witnesses missing from census: {panel_failures}")

    expected_summary = {
        "additive_rows": len(expected_quads),
        "positive_rows": positive,
        "negative_rows": len(expected_quads) - positive,
        "total_tilings": total_tilings,
        "affine_rows": sum(affine(quad) for quad in expected_quads),
        "non_affine_rows": sum(not affine(quad) for quad in expected_quads),
        "positive_affine_rows": positive_affine,
        "positive_non_affine_rows": positive - positive_affine,
        "source_displayed_unique_rows": len(line_lookup),
        "source_displayed_positive_rows": displayed_positive,
        "positive_not_source_displayed_rows": positive - displayed_positive,
    }
    if bundle.get("summary") != expected_summary:
        errors.append(
            f"summary mismatch: expected {expected_summary}, observed {bundle.get('summary')}"
        )

    return {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "metrics": {
            **expected_summary,
            "placement_counts": {
                str(label): len(catalogue[label]) for label in sorted(catalogue)
            },
            "source_panels_checked": len(lock["pixel_transcription"]["panels"]),
            "distinct_canonical_panel_tilings": len(canonical_panel_tilings),
        },
    }


def main() -> int:
    bundle = json.loads(DEFAULT_BUNDLE.read_text(encoding="utf-8"))
    lock = json.loads(DEFAULT_LOCK.read_text(encoding="utf-8"))
    result = verify_bundle(bundle, lock)
    if result["status"] == "PASS":
        metrics = result["metrics"]
        print("[PASS] complete 86-row key set and source-lock identity")
        print("[PASS] independent D4 placement catalogues and exact-cover counts")
        print("[PASS] all explicit positive certificates equal the regenerated tiling sets")
        print("[PASS] all 66 negatives independently exhaust to zero")
        print(
            "[PASS] 20 source panels replay; "
            f"{metrics['distinct_canonical_panel_tilings']} distinct after target canonicalisation"
        )
        print(
            "[PASS] summary "
            f"{metrics['positive_rows']} positive / {metrics['negative_rows']} negative / "
            f"{metrics['total_tilings']} tilings"
        )
        print(
            "[PASS] positive affine/non-affine "
            f"{metrics['positive_affine_rows']}/{metrics['positive_non_affine_rows']}"
        )
        print("\nSTATUS: PASS")
        return 0
    print("STATUS: FAIL")
    for error in result["errors"]:
        print(f"[FAIL] {error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
