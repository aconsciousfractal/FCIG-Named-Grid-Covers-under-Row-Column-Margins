"""Primary exact-cover engine for the source-locked C32 model.

Pieces and target are arguments/data.  The search is exhaustive and exact over
integer cells; no image-processing code is imported here.
"""
from __future__ import annotations

from collections.abc import Iterable


Cell = tuple[int, int]
Shape = frozenset[Cell]


def normalize(cells: Iterable[Cell]) -> tuple[Cell, ...]:
    cells = tuple(cells)
    row0 = min(row for row, _ in cells)
    col0 = min(col for _, col in cells)
    return tuple(sorted((row - row0, col - col0) for row, col in cells))


def orientations(piece: Iterable[Cell]) -> tuple[tuple[Cell, ...], ...]:
    shape = list(piece)
    result: set[tuple[Cell, ...]] = set()
    for _ in range(4):
        result.add(normalize(shape))
        result.add(normalize((row, -col) for row, col in shape))
        shape = [(col, -row) for row, col in shape]
    return tuple(sorted(result))


def placements(piece: Iterable[Cell], target: Shape) -> tuple[Shape, ...]:
    row0 = min(row for row, _ in target)
    row1 = max(row for row, _ in target)
    col0 = min(col for _, col in target)
    col1 = max(col for _, col in target)
    result: set[Shape] = set()
    for oriented in orientations(piece):
        height = max(row for row, _ in oriented)
        width = max(col for _, col in oriented)
        for delta_row in range(row0, row1 - height + 1):
            for delta_col in range(col0, col1 - width + 1):
                placed = frozenset(
                    (row + delta_row, col + delta_col)
                    for row, col in oriented
                )
                if placed <= target:
                    result.add(placed)
    return tuple(sorted(result, key=lambda shape: tuple(sorted(shape))))


def enumerate_tilings(
    labels: tuple[int, ...],
    pieces: dict[int, Shape],
    target: Shape,
    placement_catalogue: dict[int, tuple[Shape, ...]] | None = None,
) -> tuple[tuple[Shape, ...], ...]:
    if sum(len(pieces[label]) for label in labels) != len(target):
        return ()
    catalogue = placement_catalogue or {
        label: placements(pieces[label], target) for label in labels
    }
    branch_order = tuple(
        sorted(range(len(labels)), key=lambda index: (len(catalogue[labels[index]]), labels[index]))
    )
    chosen: list[Shape | None] = [None] * len(labels)
    result: list[tuple[Shape, ...]] = []

    def search(depth: int, remaining: Shape) -> None:
        if depth == len(labels):
            if not remaining:
                result.append(tuple(shape for shape in chosen if shape is not None))
            return
        index = branch_order[depth]
        label = labels[index]
        for placed in catalogue[label]:
            if placed <= remaining:
                chosen[index] = placed
                search(depth + 1, remaining - placed)
                chosen[index] = None

    search(0, target)
    return tuple(
        sorted(
            result,
            key=lambda tiling: tuple(tuple(sorted(shape)) for shape in tiling),
        )
    )
