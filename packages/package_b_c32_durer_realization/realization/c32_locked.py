"""Load the source-locked C32 discrete model.

This module contains no hand-copied geometry.  The authority is
``registry/c32_source_lock.json``; all executable structures are derived from
that file.
"""
from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LOCK_PATH = ROOT / "registry" / "c32_source_lock.json"
LOCK = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
MODEL = LOCK["canonical_model"]

TARGET = frozenset(
    (row, col)
    for row in range(MODEL["target"]["rows"])
    for col in range(MODEL["target"]["columns"])
    if [row, col] not in MODEL["target"]["holes"]
)
PIECE = {
    int(label): frozenset(tuple(cell) for cell in cells)
    for label, cells in MODEL["pieces"].items()
}
SOURCE_SQUARE = tuple(tuple(row) for row in MODEL["durer_source_square"])
OWNER_SQUARE = tuple(tuple(row) for row in MODEL["owner_durer_complement_square"])
BOARD_VALUES = tuple(value for row in SOURCE_SQUARE for value in row)
POSITION_BY_SOURCE_VALUE = {
    SOURCE_SQUARE[row][col]: 4 * row + col
    for row in range(4)
    for col in range(4)
}
MAGIC_LINES = {
    name: tuple(values) for name, values in MODEL["magic_lines"].items()
}


def is_affine(quad: tuple[int, ...]) -> bool:
    """Magic 24 value-minus-one affine-plane test, invariant under complement."""

    value = 0
    for label in quad:
        value ^= label - 1
    return value == 0


def owner_crosswalk(quad: tuple[int, ...]) -> dict[str, list[int]]:
    positions = sorted(POSITION_BY_SOURCE_VALUE[label] for label in quad)
    owner_values = sorted(OWNER_SQUARE[position // 4][position % 4] for position in positions)
    return {
        "board_positions": positions,
        "owner_complement_values": owner_values,
    }
