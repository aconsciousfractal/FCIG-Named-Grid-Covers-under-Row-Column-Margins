#!/usr/bin/env python3
"""Independent verifier for the co-area residual-state result.

This file intentionally imports neither coarea_fpt.py nor fiber_graph.py.  It
uses bounding-box placement generation and a direct two-by-two meet-in-the-
middle fiber construction, then compares every row with the principal JSON.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict, deque
from itertools import combinations
from pathlib import Path
from typing import Iterable


HERE = Path(__file__).resolve().parent
PACKAGES = HERE.parent.parent
PROJECT = PACKAGES.parent
RESULT_PATH = PROJECT / "results" / "coarea_fpt_analysis.json"

Cell = tuple[int, int]
Shape = frozenset[Cell]
Vector = tuple[int, ...]
Node = tuple[Shape, ...]


def norm(cells: Iterable[Cell]) -> Shape:
    values = tuple(cells)
    row0 = min(row for row, _ in values)
    col0 = min(col for _, col in values)
    return frozenset((row - row0, col - col0) for row, col in values)


def rotate(cells: Shape) -> Shape:
    return norm((col, -row) for row, col in cells)


def reflect(cells: Shape) -> Shape:
    return norm((row, -col) for row, col in cells)


def poses(shape: Shape, target: Shape) -> tuple[Shape, ...]:
    oriented: set[Shape] = set()
    current = shape
    for _ in range(4):
        oriented.add(norm(current))
        oriented.add(reflect(current))
        current = rotate(current)
    min_row = min(row for row, _ in target)
    max_row = max(row for row, _ in target)
    min_col = min(col for _, col in target)
    max_col = max(col for _, col in target)
    output: set[Shape] = set()
    for item in oriented:
        height = max(row for row, _ in item) + 1
        width = max(col for _, col in item) + 1
        for top in range(min_row, max_row - height + 2):
            for left in range(min_col, max_col - width + 2):
                placed = frozenset(
                    (row + top, col + left) for row, col in item
                )
                if placed <= target:
                    output.add(placed)
    return tuple(sorted(output, key=lambda value: tuple(sorted(value))))


class Model:
    def __init__(
        self,
        name: str,
        ids: tuple[int, ...],
        pieces: tuple[Shape, ...],
        target: Shape,
        source: Path,
    ) -> None:
        self.name = name
        self.ids = ids
        self.pieces = pieces
        self.target = target
        self.source = source
        self.rows = tuple(sorted({row for row, _ in target}))
        self.cols = tuple(sorted({col for _, col in target}))
        self.ri = {row: index for index, row in enumerate(self.rows)}
        self.ci = {col: index for index, col in enumerate(self.cols)}
        self.placements = tuple(poses(piece, target) for piece in pieces)
        self.xrays = tuple(
            tuple(self.xray(placed) for placed in values)
            for values in self.placements
        )
        self.target_xray = self.xray(target)

    def xray(self, cells: Shape) -> Vector:
        result = [0] * (len(self.rows) + len(self.cols))
        for row, col in cells:
            result[self.ri[row]] += 1
            result[len(self.rows) + self.ci[col]] += 1
        return tuple(result)

    def quaternes(self) -> tuple[tuple[int, ...], ...]:
        return tuple(
            quad
            for quad in combinations(range(len(self.pieces)), 4)
            if sum(len(self.pieces[index]) for index in quad)
            == len(self.target)
        )

    def fiber(self, quad: tuple[int, ...]) -> tuple[Node, ...]:
        first, second, third, fourth = quad
        half: dict[Vector, list[tuple[Shape, Shape]]] = defaultdict(list)
        for first_placement, first_xray in zip(
            self.placements[first], self.xrays[first]
        ):
            for second_placement, second_xray in zip(
                self.placements[second], self.xrays[second]
            ):
                key = tuple(
                    a + b for a, b in zip(first_xray, second_xray)
                )
                if all(
                    key[index] <= self.target_xray[index]
                    for index in range(len(key))
                ):
                    half[key].append((first_placement, second_placement))
        result: set[Node] = set()
        for third_placement, third_xray in zip(
            self.placements[third], self.xrays[third]
        ):
            for fourth_placement, fourth_xray in zip(
                self.placements[fourth], self.xrays[fourth]
            ):
                key = tuple(
                    self.target_xray[index]
                    - third_xray[index]
                    - fourth_xray[index]
                    for index in range(len(self.target_xray))
                )
                for first_placement, second_placement in half.get(key, ()):
                    result.add(
                        (
                            first_placement,
                            second_placement,
                            third_placement,
                            fourth_placement,
                        )
                    )
        return tuple(
            sorted(
                result,
                key=lambda node: tuple(
                    tuple(sorted(placed)) for placed in node
                ),
            )
        )


def tiling(node: Node, target: Shape) -> bool:
    coverage = Counter()
    for placed in node:
        coverage.update(placed)
    return (
        len(coverage) == len(target)
        and all(coverage[cell] == 1 for cell in target)
    )


def graph_summary(nodes: tuple[Node, ...], target: Shape) -> dict:
    flags = [tiling(node, target) for node in nodes]
    adjacency = [[] for _ in nodes]
    one_edges = 0
    two_edges = 0
    for left in range(len(nodes)):
        for right in range(left + 1, len(nodes)):
            changed = sum(
                nodes[left][position] != nodes[right][position]
                for position in range(4)
            )
            if changed == 1:
                one_edges += 1
            if changed == 2:
                two_edges += 1
                adjacency[left].append(right)
                adjacency[right].append(left)
    components: list[list[int]] = []
    seen: set[int] = set()
    for start in range(len(nodes)):
        if start in seen:
            continue
        queue = deque([start])
        seen.add(start)
        component: list[int] = []
        while queue:
            value = queue.popleft()
            component.append(value)
            for neighbour in adjacency[value]:
                if neighbour not in seen:
                    seen.add(neighbour)
                    queue.append(neighbour)
        components.append(component)
    trapped = [
        component
        for component in components
        if not any(flags[index] for index in component)
    ]
    infinity = 10**9
    distances = [infinity] * len(nodes)
    queue = deque()
    for index, flag in enumerate(flags):
        if flag:
            distances[index] = 0
            queue.append(index)
    while queue:
        value = queue.popleft()
        for neighbour in adjacency[value]:
            if distances[neighbour] > distances[value] + 1:
                distances[neighbour] = distances[value] + 1
                queue.append(neighbour)
    return {
        "margin_nodes": len(nodes),
        "tiling_nodes": sum(flags),
        "extra_nodes": len(nodes) - sum(flags),
        "components": len(components),
        "one_replacement_edges": one_edges,
        "two_replacement_edges": two_edges,
        "trapped_components": len(trapped),
        "trapped_nodes": sum(map(len, trapped)),
        "repair_exact": not trapped,
        "maximum_finite_repair_radius": max(
            (
                value
                for value in distances
                if 0 < value < infinity
            ),
            default=0,
        ),
    }


def largest_position(model: Model, quad: tuple[int, ...]) -> int:
    return min(
        range(4),
        key=lambda position: (
            -len(model.pieces[quad[position]]),
            quad[position],
        ),
    )


def verify_active_lemma(
    model: Model,
    quad: tuple[int, ...],
    nodes: tuple[Node, ...],
) -> tuple[int, int]:
    position = largest_position(model, quad)
    largest = quad[position]
    q_value = len(model.target) - len(model.pieces[largest])
    violations = 0
    checked = 0
    for node in nodes:
        big = node[position]
        bound = tuple(
            target - value
            for target, value in zip(model.target_xray, model.xray(big))
        )
        row_bound = bound[: len(model.rows)]
        column_bound = bound[len(model.rows) :]
        active_rows = {
            model.rows[index]
            for index, value in enumerate(row_bound)
            if value
        }
        active_columns = {
            model.cols[index]
            for index, value in enumerate(column_bound)
            if value
        }
        active_grid = {
            cell
            for cell in model.target
            if cell[0] in active_rows and cell[1] in active_columns
        }
        exact_product = 1
        for value in bound:
            exact_product *= value + 1
        conditions = [
            sum(row_bound) == q_value,
            sum(column_bound) == q_value,
            len(active_rows) <= q_value,
            len(active_columns) <= q_value,
            len(active_grid) <= q_value * q_value,
            exact_product <= (q_value + 1) ** (2 * q_value),
            exact_product <= 4**q_value,
            all(
                node[other] <= active_grid
                for other in range(4)
                if other != position
            ),
        ]
        checked += len(conditions)
        violations += sum(not condition for condition in conditions)
    return checked, violations


def load_models() -> tuple[Model, ...]:
    c32_path = (
        PACKAGES
        / "package_b_c32_durer_realization"
        / "realization"
        / "R_certificates.json"
    )
    c32_data = json.loads(c32_path.read_text(encoding="utf-8"))
    c32_map = {
        int(key): norm(tuple(cell) for cell in value)
        for key, value in c32_data["normalization"]["pieces"].items()
    }
    c32_ids = tuple(sorted(c32_map))
    c32 = Model(
        "C32",
        c32_ids,
        tuple(c32_map[key] for key in c32_ids),
        frozenset(
            tuple(cell)
            for cell in c32_data["normalization"]["target_cells"]
        ),
        c32_path,
    )

    c46_path = (
        PACKAGES
        / "package_a_c46_reproduction"
        / "realization"
        / "R_certificates.json"
    )
    c46_data = json.loads(c46_path.read_text(encoding="utf-8"))
    c46_map = {
        int(key): norm(tuple(cell) for cell in value)
        for key, value in c46_data["normalization"]["pieces"].items()
    }
    c46_ids = (4, 5, 10, 15, 14, 11, 8, 1, 7, 2, 13, 12, 9, 16, 3, 6)
    c46 = Model(
        "C46",
        c46_ids,
        tuple(c46_map[key] for key in c46_ids),
        frozenset(
            tuple(cell)
            for cell in c46_data["normalization"]["target_cells"]
        ),
        c46_path,
    )

    p49_path = (
        PACKAGES
        / "package_c_comparative_hypergraphs"
        / "specimens"
        / "p49_locked.json"
    )
    p49_data = json.loads(p49_path.read_text(encoding="utf-8"))
    p49_pieces = tuple(
        norm(tuple(cell) for cell in piece)
        for piece in p49_data["pieces"]
    )
    target_data = p49_data["target"]
    removed = {tuple(cell) for cell in target_data["remove"]}
    p49_target = frozenset(
        (row, col)
        for row in range(target_data["rows"])
        for col in range(target_data["cols"])
        if (row, col) not in removed
    )
    p49 = Model(
        "P49-base",
        tuple(range(16)),
        p49_pieces,
        p49_target,
        p49_path,
    )
    return c32, c46, p49


def main() -> int:
    result = json.loads(RESULT_PATH.read_text(encoding="utf-8"))
    stored = {item["library"]: item for item in result["libraries"]}
    checks = 0
    active_checks = 0
    active_violations = 0

    for model in load_models():
        if model.name not in stored:
            raise AssertionError(f"missing stored library {model.name}")
        source_record = result["inputs"][model.name]
        if hashlib.sha256(model.source.read_bytes()).hexdigest() != source_record["sha256"]:
            raise AssertionError(f"{model.name}: source hash mismatch")
        checks += 1

        stored_rows = {
            tuple(row["piece_indices"]): row
            for row in stored[model.name]["rows"]
        }
        if set(stored_rows) != set(model.quaternes()):
            raise AssertionError(f"{model.name}: quaterne set mismatch")
        checks += 1

        totals = Counter()
        for quad in model.quaternes():
            nodes = model.fiber(quad)
            direct = graph_summary(nodes, model.target)
            row = stored_rows[quad]
            for field in (
                "margin_nodes",
                "tiling_nodes",
                "extra_nodes",
                "components",
                "one_replacement_edges",
                "two_replacement_edges",
                "trapped_components",
                "trapped_nodes",
                "repair_exact",
                "maximum_finite_repair_radius",
            ):
                if row[field] != direct[field]:
                    raise AssertionError(
                        f"{model.name} {quad}: {field} mismatch "
                        f"{row[field]} != {direct[field]}"
                    )
                checks += 1
            q_value = len(model.target) - max(
                len(model.pieces[index]) for index in quad
            )
            if row["coarea_q"] != q_value:
                raise AssertionError(f"{model.name} {quad}: co-area mismatch")
            checks += 1
            checked, violations = verify_active_lemma(model, quad, nodes)
            active_checks += checked
            active_violations += violations
            totals["fiber_nodes"] += direct["margin_nodes"]
            totals["tiling_nodes"] += direct["tiling_nodes"]
            totals["margin_feasible_rows"] += bool(direct["margin_nodes"])
            totals["tiling_rows"] += bool(direct["tiling_nodes"])
            totals["trapped_components"] += direct["trapped_components"]

        library = stored[model.name]
        for field in (
            "fiber_nodes",
            "tiling_nodes",
            "margin_feasible_rows",
            "tiling_rows",
            "trapped_components",
        ):
            if library[field] != totals[field]:
                raise AssertionError(
                    f"{model.name}: aggregate {field} mismatch"
                )
            checks += 1
        expected_verdicts = {
            "support_exact": (
                totals["margin_feasible_rows"] == totals["tiling_rows"]
            ),
            "fiber_pure": totals["fiber_nodes"] == totals["tiling_nodes"],
            "repair_exact": totals["trapped_components"] == 0,
        }
        for field, expected in expected_verdicts.items():
            if library[field] != expected:
                raise AssertionError(
                    f"{model.name}: verdict {field} mismatch"
                )
            checks += 1
        print(
            f"{model.name}: independent direct fiber "
            f"{totals['fiber_nodes']} = {totals['tiling_nodes']} + "
            f"{totals['fiber_nodes'] - totals['tiling_nodes']} PASS"
        )

    if active_violations:
        raise AssertionError(
            f"active-line lemma violations: {active_violations}"
        )
    print(
        f"PASS: {checks} stored-result checks; "
        f"{active_checks} active-line conditions; 0 violations"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
