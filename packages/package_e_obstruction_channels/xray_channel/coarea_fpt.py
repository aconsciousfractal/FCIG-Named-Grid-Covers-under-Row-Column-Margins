#!/usr/bin/env python3
"""Co-area residual-state algorithm for placement-coloured X-ray fibers.

This is the principal implementation for the experiment preregistered in
COAREA_FPT_PREREGISTRATION.md.  It computes the complete row+column fibers of
C32, C46 and P49-base by freezing a deterministic largest piece and exploring
only the bounded residual state space.

The script does not read stored support, purity or repair verdicts.
"""
from __future__ import annotations

import hashlib
import json
import platform
import sys
import time
from collections import Counter, deque
from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations
from pathlib import Path
from typing import Iterable, Iterator


HERE = Path(__file__).resolve().parent
PACKAGES = HERE.parent.parent
PROJECT = PACKAGES.parent
OUTPUT = PROJECT / "results" / "coarea_fpt_analysis.json"

Cell = tuple[int, int]
Shape = frozenset[Cell]
Vector = tuple[int, ...]
Node = tuple[Shape, ...]


def normalize(cells: Iterable[Cell]) -> Shape:
    values = tuple(cells)
    row0 = min(row for row, _ in values)
    col0 = min(col for _, col in values)
    return frozenset((row - row0, col - col0) for row, col in values)


def orientations(shape: Shape) -> tuple[Shape, ...]:
    result: set[Shape] = set()
    current = shape
    for _ in range(4):
        result.add(normalize(current))
        result.add(normalize((row, -col) for row, col in current))
        current = frozenset((col, -row) for row, col in current)
    return tuple(sorted(result, key=lambda value: tuple(sorted(value))))


def legal_placements(shape: Shape, target: Shape) -> tuple[Shape, ...]:
    """Enumerate D4+translation placements by cell anchoring.

    Anchoring one oriented shape cell to one target cell avoids assumptions
    about a solid bounding box and is polynomial in the cell-list input.
    """

    result: set[Shape] = set()
    for oriented in orientations(shape):
        anchor = min(oriented)
        for target_cell in target:
            delta = (
                target_cell[0] - anchor[0],
                target_cell[1] - anchor[1],
            )
            placed = frozenset(
                (row + delta[0], col + delta[1]) for row, col in oriented
            )
            if placed <= target:
                result.add(placed)
    return tuple(sorted(result, key=lambda value: tuple(sorted(value))))


@dataclass(frozen=True)
class Library:
    name: str
    piece_ids: tuple[int, ...]
    pieces: tuple[Shape, ...]
    target: Shape
    input_path: Path

    def __post_init__(self) -> None:
        if len(self.piece_ids) != len(self.pieces):
            raise ValueError("piece id/shape length mismatch")
        if not self.target or any(not piece for piece in self.pieces):
            raise ValueError("target and pieces must be nonempty")


@dataclass
class PreparedLibrary:
    source: Library
    rows: tuple[int, ...]
    columns: tuple[int, ...]
    row_index: dict[int, int]
    column_index: dict[int, int]
    placements: tuple[tuple[Shape, ...], ...]
    placement_xrays: tuple[tuple[Vector, ...], ...]
    target_xray: Vector

    @classmethod
    def build(cls, source: Library) -> "PreparedLibrary":
        rows = tuple(sorted({row for row, _ in source.target}))
        columns = tuple(sorted({col for _, col in source.target}))
        row_index = {value: index for index, value in enumerate(rows)}
        column_index = {value: index for index, value in enumerate(columns)}

        def xray(cells: Shape) -> Vector:
            result = [0] * (len(rows) + len(columns))
            for row, col in cells:
                result[row_index[row]] += 1
                result[len(rows) + column_index[col]] += 1
            return tuple(result)

        placements = tuple(
            legal_placements(piece, source.target) for piece in source.pieces
        )
        if any(not values for values in placements):
            raise ValueError(f"{source.name}: a piece has no legal placement")
        placement_xrays = tuple(
            tuple(xray(placed) for placed in values) for values in placements
        )
        prepared = cls(
            source=source,
            rows=rows,
            columns=columns,
            row_index=row_index,
            column_index=column_index,
            placements=placements,
            placement_xrays=placement_xrays,
            target_xray=xray(source.target),
        )
        prepared.validate_placements()
        return prepared

    def validate_placements(self) -> None:
        for piece_index, values in enumerate(self.placements):
            area = len(self.source.pieces[piece_index])
            for placed in values:
                if not placed <= self.source.target:
                    raise ValueError(
                        f"{self.source.name}: placement outside target"
                    )
                if len(placed) != area:
                    raise ValueError(
                        f"{self.source.name}: placement area changed"
                    )

    def candidate_quaternes(self) -> tuple[tuple[int, ...], ...]:
        target_area = len(self.source.target)
        return tuple(
            quad
            for quad in combinations(range(len(self.source.pieces)), 4)
            if sum(len(self.source.pieces[index]) for index in quad)
            == target_area
        )


def leq(left: Vector, right: Vector) -> bool:
    return all(a <= b for a, b in zip(left, right))


def subtract(left: Vector, right: Vector) -> Vector:
    return tuple(a - b for a, b in zip(left, right))


def add(left: Vector, right: Vector) -> Vector:
    return tuple(a + b for a, b in zip(left, right))


def is_tiling(node: Node, target: Shape) -> bool:
    coverage = Counter()
    for placed in node:
        coverage.update(placed)
    return (
        len(coverage) == len(target)
        and all(coverage[cell] == 1 for cell in target)
    )


def choose_largest(prepared: PreparedLibrary, quad: tuple[int, ...]) -> int:
    """Return the tuple position of a deterministic largest piece."""

    return min(
        range(len(quad)),
        key=lambda position: (
            -len(prepared.source.pieces[quad[position]]),
            quad[position],
        ),
    )


def forward_margin_states(
    candidate_vectors: tuple[tuple[Vector, ...], ...],
    bound: Vector,
) -> tuple[bool, int, int]:
    zero = (0,) * len(bound)
    states = {zero}
    peak = 1
    inspected = 0
    for vectors in candidate_vectors:
        next_states: set[Vector] = set()
        for state in states:
            for vector in vectors:
                inspected += 1
                value = add(state, vector)
                if leq(value, bound):
                    next_states.add(value)
        states = next_states
        peak = max(peak, len(states))
        if not states:
            break
    return bound in states, peak, inspected


def forward_tiling_states(
    candidate_placements: tuple[tuple[Shape, ...], ...],
    residual: Shape,
) -> tuple[bool, int, int]:
    cells = tuple(sorted(residual))
    bit = {cell: 1 << index for index, cell in enumerate(cells)}
    full = (1 << len(cells)) - 1
    states = {0}
    peak = 1
    inspected = 0
    for placements in candidate_placements:
        masks = tuple(
            sum(bit[cell] for cell in placed)
            for placed in placements
            if placed <= residual
        )
        next_states: set[int] = set()
        for state in states:
            for mask in masks:
                inspected += 1
                if state & mask == 0:
                    next_states.add(state | mask)
        states = next_states
        peak = max(peak, len(states))
        if not states:
            break
    return full in states, peak, inspected


def enumerate_margin_tuples(
    candidate_placements: tuple[tuple[Shape, ...], ...],
    candidate_vectors: tuple[tuple[Vector, ...], ...],
    bound: Vector,
) -> Iterator[tuple[Shape, ...]]:
    """Enumerate all named residual tuples with total X-ray ``bound``."""

    zero = (0,) * len(bound)

    @lru_cache(maxsize=None)
    def can_finish(position: int, remaining: Vector) -> bool:
        if position == len(candidate_vectors):
            return remaining == zero
        return any(
            leq(vector, remaining)
            and can_finish(position + 1, subtract(remaining, vector))
            for vector in candidate_vectors[position]
        )

    def walk(
        position: int,
        remaining: Vector,
        chosen: tuple[Shape, ...],
    ) -> Iterator[tuple[Shape, ...]]:
        if position == len(candidate_vectors):
            if remaining == zero:
                yield chosen
            return
        for placed, vector in zip(
            candidate_placements[position],
            candidate_vectors[position],
        ):
            if leq(vector, remaining):
                next_remaining = subtract(remaining, vector)
                if can_finish(position + 1, next_remaining):
                    yield from walk(
                        position + 1,
                        next_remaining,
                        chosen + (placed,),
                    )

    if can_finish(0, bound):
        yield from walk(0, bound, ())


def row_fiber(
    prepared: PreparedLibrary,
    quad: tuple[int, ...],
) -> tuple[tuple[Node, ...], dict]:
    largest_position = choose_largest(prepared, quad)
    largest_piece = quad[largest_position]
    residual_positions = tuple(
        position for position in range(len(quad))
        if position != largest_position
    )
    residual_pieces = tuple(quad[position] for position in residual_positions)
    target = prepared.source.target
    q_value = len(target) - len(prepared.source.pieces[largest_piece])

    nodes: set[Node] = set()
    margin_feasible_by_dp = False
    tiling_feasible_by_dp = False
    margin_peak = 0
    tile_peak = 0
    margin_inspected = 0
    tile_inspected = 0
    active_row_max = 0
    active_column_max = 0
    active_grid_max = 0
    exact_state_bound_max = 0
    participating_largest_placements = 0
    active_violations = 0

    for largest_placement, largest_xray in zip(
        prepared.placements[largest_piece],
        prepared.placement_xrays[largest_piece],
    ):
        bound = subtract(prepared.target_xray, largest_xray)
        if any(value < 0 for value in bound):
            raise AssertionError("a legal placement exceeded target margins")
        row_bound = bound[: len(prepared.rows)]
        column_bound = bound[len(prepared.rows) :]
        active_rows = {
            prepared.rows[index]
            for index, value in enumerate(row_bound)
            if value
        }
        active_columns = {
            prepared.columns[index]
            for index, value in enumerate(column_bound)
            if value
        }
        active_grid = frozenset(
            cell
            for cell in target
            if cell[0] in active_rows and cell[1] in active_columns
        )
        active_row_max = max(active_row_max, len(active_rows))
        active_column_max = max(active_column_max, len(active_columns))
        active_grid_max = max(active_grid_max, len(active_grid))
        if (
            len(active_rows) > q_value
            or len(active_columns) > q_value
            or len(active_grid) > q_value * q_value
        ):
            active_violations += 1

        candidate_placements: list[tuple[Shape, ...]] = []
        candidate_vectors: list[tuple[Vector, ...]] = []
        for piece in residual_pieces:
            kept_placements: list[Shape] = []
            kept_vectors: list[Vector] = []
            for placed, vector in zip(
                prepared.placements[piece],
                prepared.placement_xrays[piece],
            ):
                if leq(vector, bound):
                    if not placed <= active_grid:
                        active_violations += 1
                    kept_placements.append(placed)
                    kept_vectors.append(vector)
            candidate_placements.append(tuple(kept_placements))
            candidate_vectors.append(tuple(kept_vectors))

        margin_ok, peak, inspected = forward_margin_states(
            tuple(candidate_vectors), bound
        )
        margin_feasible_by_dp |= margin_ok
        margin_peak = max(margin_peak, peak)
        margin_inspected += inspected

        residual = target - largest_placement
        tile_candidates = tuple(
            tuple(
                placed
                for placed in prepared.placements[piece]
                if placed <= residual
            )
            for piece in residual_pieces
        )
        tile_ok, peak, inspected = forward_tiling_states(
            tile_candidates, residual
        )
        tiling_feasible_by_dp |= tile_ok
        tile_peak = max(tile_peak, peak)
        tile_inspected += inspected

        exact_state_bound = 1
        for value in bound:
            exact_state_bound *= value + 1
        exact_state_bound_max = max(exact_state_bound_max, exact_state_bound)

        local_count = 0
        for residual_tuple in enumerate_margin_tuples(
            tuple(candidate_placements),
            tuple(candidate_vectors),
            bound,
        ):
            node_values: list[Shape | None] = [None] * len(quad)
            node_values[largest_position] = largest_placement
            for position, placed in zip(
                residual_positions, residual_tuple
            ):
                node_values[position] = placed
            node = tuple(node_values)
            if any(value is None for value in node):
                raise AssertionError("incomplete node reconstruction")
            nodes.add(node)  # type: ignore[arg-type]
            local_count += 1
        if local_count:
            participating_largest_placements += 1

    ordered_nodes = tuple(
        sorted(
            nodes,
            key=lambda node: tuple(
                tuple(sorted(placed)) for placed in node
            ),
        )
    )
    tiling_count = sum(is_tiling(node, target) for node in ordered_nodes)
    if margin_feasible_by_dp != bool(ordered_nodes):
        raise AssertionError("margin DP/enumeration disagreement")
    if tiling_feasible_by_dp != bool(tiling_count):
        raise AssertionError("tiling DP/enumeration disagreement")
    if margin_peak > exact_state_bound_max:
        raise AssertionError("observed margin state count exceeds exact bound")
    if exact_state_bound_max > (q_value + 1) ** (2 * q_value):
        raise AssertionError("exact margin state bound exceeds preregistered bound")
    if exact_state_bound_max > 4**q_value:
        raise AssertionError("exact margin state bound exceeds sharp 4^q bound")
    if tile_peak > 2**q_value:
        raise AssertionError("tiling state count exceeds subset bound")
    if active_violations:
        raise AssertionError(f"active-line lemma violations: {active_violations}")

    metrics = {
        "piece_indices": list(quad),
        "piece_ids": [prepared.source.piece_ids[index] for index in quad],
        "piece_areas": [
            len(prepared.source.pieces[index]) for index in quad
        ],
        "largest_tuple_position": largest_position,
        "largest_piece_index": largest_piece,
        "largest_piece_id": prepared.source.piece_ids[largest_piece],
        "coarea_q": q_value,
        "largest_placements": len(prepared.placements[largest_piece]),
        "participating_largest_placements": participating_largest_placements,
        "margin_nodes": len(ordered_nodes),
        "tiling_nodes": tiling_count,
        "extra_nodes": len(ordered_nodes) - tiling_count,
        "margin_feasible_by_dp": margin_feasible_by_dp,
        "tiling_feasible_by_dp": tiling_feasible_by_dp,
        "active_row_max": active_row_max,
        "active_column_max": active_column_max,
        "active_grid_max": active_grid_max,
        "active_grid_bound_q_squared": q_value * q_value,
        "margin_state_peak": margin_peak,
        "margin_state_exact_product_bound_max": exact_state_bound_max,
        "margin_state_preregistered_bound": (q_value + 1)
        ** (2 * q_value),
        "margin_state_sharp_bound": 4**q_value,
        "tiling_state_peak": tile_peak,
        "tiling_state_bound": 2**q_value,
        "margin_transitions_inspected": margin_inspected,
        "tiling_transitions_inspected": tile_inspected,
        "active_line_violations": active_violations,
    }
    return ordered_nodes, metrics


def graph_metrics(nodes: tuple[Node, ...], target: Shape) -> dict:
    count = len(nodes)
    tile = [is_tiling(node, target) for node in nodes]
    adjacency = [[] for _ in nodes]
    edges = 0
    one_move_edges = 0
    for first in range(count):
        for second in range(first + 1, count):
            difference = sum(
                nodes[first][index] != nodes[second][index]
                for index in range(len(nodes[first]))
            )
            if difference == 1:
                one_move_edges += 1
            if difference == 2:
                adjacency[first].append(second)
                adjacency[second].append(first)
                edges += 1

    component_by_node = [-1] * count
    components: list[list[int]] = []
    for start in range(count):
        if component_by_node[start] != -1:
            continue
        component_id = len(components)
        queue = deque([start])
        component_by_node[start] = component_id
        component: list[int] = []
        while queue:
            node = queue.popleft()
            component.append(node)
            for neighbour in adjacency[node]:
                if component_by_node[neighbour] == -1:
                    component_by_node[neighbour] = component_id
                    queue.append(neighbour)
        components.append(component)

    trapped_components = sum(
        not any(tile[index] for index in component)
        for component in components
    )
    trapped_nodes = sum(
        len(component)
        for component in components
        if not any(tile[index] for index in component)
    )
    infinity = 10**9
    distance = [infinity] * count
    queue = deque()
    for index, value in enumerate(tile):
        if value:
            distance[index] = 0
            queue.append(index)
    while queue:
        node = queue.popleft()
        for neighbour in adjacency[node]:
            if distance[neighbour] > distance[node] + 1:
                distance[neighbour] = distance[node] + 1
                queue.append(neighbour)
    finite_distances = [
        value for value in distance if value < infinity and value > 0
    ]
    return {
        "components": len(components),
        "two_replacement_edges": edges,
        "one_replacement_edges": one_move_edges,
        "trapped_components": trapped_components,
        "trapped_nodes": trapped_nodes,
        "repair_exact": trapped_components == 0,
        "maximum_finite_repair_radius": max(finite_distances, default=0),
    }


def analyse_library(source: Library) -> dict:
    started = time.perf_counter()
    prepared = PreparedLibrary.build(source)
    row_results = []
    total_nodes = 0
    total_tilings = 0
    trapped_rows = 0
    trapped_components = 0
    maximum_radius = 0
    for quad in prepared.candidate_quaternes():
        nodes, metrics = row_fiber(prepared, quad)
        graph = graph_metrics(nodes, source.target)
        metrics.update(graph)
        metrics["support_exact_row"] = (
            not metrics["margin_nodes"] or bool(metrics["tiling_nodes"])
        )
        metrics["fiber_pure_row"] = metrics["extra_nodes"] == 0
        row_results.append(metrics)
        total_nodes += metrics["margin_nodes"]
        total_tilings += metrics["tiling_nodes"]
        trapped_rows += int(
            metrics["margin_nodes"] > 0 and metrics["tiling_nodes"] == 0
        )
        trapped_components += metrics["trapped_components"]
        maximum_radius = max(
            maximum_radius, metrics["maximum_finite_repair_radius"]
        )

    margin_rows = sum(row["margin_nodes"] > 0 for row in row_results)
    tiling_rows = sum(row["tiling_nodes"] > 0 for row in row_results)
    result = {
        "library": source.name,
        "target_area": len(source.target),
        "target_rows": len(prepared.rows),
        "target_columns": len(prepared.columns),
        "pieces": len(source.pieces),
        "placements": sum(len(values) for values in prepared.placements),
        "area_feasible_rows": len(row_results),
        "margin_feasible_rows": margin_rows,
        "tiling_rows": tiling_rows,
        "fiber_nodes": total_nodes,
        "tiling_nodes": total_tilings,
        "extra_nodes": total_nodes - total_tilings,
        "support_exact": trapped_rows == 0,
        "fiber_pure": total_nodes == total_tilings,
        "repair_exact": trapped_components == 0,
        "trapped_rows": trapped_rows,
        "trapped_components": trapped_components,
        "maximum_finite_repair_radius": maximum_radius,
        "active_line_violations": sum(
            row["active_line_violations"] for row in row_results
        ),
        "coareas_seen": sorted({row["coarea_q"] for row in row_results}),
        "runtime_seconds": round(time.perf_counter() - started, 6),
        "rows": row_results,
    }
    return result


def load_libraries() -> tuple[Library, ...]:
    c32_path = (
        PACKAGES
        / "package_b_c32_durer_realization"
        / "realization"
        / "R_certificates.json"
    )
    c32_data = json.loads(c32_path.read_text(encoding="utf-8"))
    c32_piece_map = {
        int(piece_id): normalize(tuple(cell) for cell in cells)
        for piece_id, cells in c32_data["normalization"]["pieces"].items()
    }
    c32_ids = tuple(sorted(c32_piece_map))
    c32 = Library(
        name="C32",
        piece_ids=c32_ids,
        pieces=tuple(c32_piece_map[piece_id] for piece_id in c32_ids),
        target=frozenset(
            tuple(cell)
            for cell in c32_data["normalization"]["target_cells"]
        ),
        input_path=c32_path,
    )

    c46_path = (
        PACKAGES
        / "package_a_c46_reproduction"
        / "realization"
        / "R_certificates.json"
    )
    c46_data = json.loads(c46_path.read_text(encoding="utf-8"))
    c46_piece_map = {
        int(piece_id): normalize(tuple(cell) for cell in cells)
        for piece_id, cells in c46_data["normalization"]["pieces"].items()
    }
    c46_square = (4, 5, 10, 15, 14, 11, 8, 1, 7, 2, 13, 12, 9, 16, 3, 6)
    c46 = Library(
        name="C46",
        piece_ids=c46_square,
        pieces=tuple(c46_piece_map[piece_id] for piece_id in c46_square),
        target=frozenset(
            tuple(cell)
            for cell in c46_data["normalization"]["target_cells"]
        ),
        input_path=c46_path,
    )

    p49_path = (
        PACKAGES
        / "package_c_comparative_hypergraphs"
        / "specimens"
        / "p49_locked.json"
    )
    p49_data = json.loads(p49_path.read_text(encoding="utf-8"))
    p49_pieces = tuple(
        normalize(tuple(cell) for cell in piece)
        for piece in p49_data["pieces"]
    )
    target_spec = p49_data["target"]
    removed = {tuple(cell) for cell in target_spec["remove"]}
    p49_target = frozenset(
        (row, col)
        for row in range(target_spec["rows"])
        for col in range(target_spec["cols"])
        if (row, col) not in removed
    )
    p49 = Library(
        name="P49-base",
        piece_ids=tuple(range(len(p49_pieces))),
        pieces=p49_pieces,
        target=p49_target,
        input_path=p49_path,
    )
    return c32, c46, p49


EXPECTED = {
    "C32": {
        "margin_feasible_rows": 20,
        "fiber_nodes": 136,
        "tiling_nodes": 136,
        "support_exact": True,
        "fiber_pure": True,
        "repair_exact": True,
    },
    "C46": {
        "margin_feasible_rows": 44,
        "fiber_nodes": 352,
        "tiling_nodes": 344,
        "support_exact": True,
        "fiber_pure": False,
        "repair_exact": True,
    },
    "P49-base": {
        "margin_feasible_rows": 61,
        "fiber_nodes": 1344,
        "tiling_nodes": 1208,
        "support_exact": False,
        "fiber_pure": False,
        "repair_exact": False,
    },
}


def validate_result(result: dict) -> None:
    if result.get("schema_version") != "p42.coarea_fpt.v1":
        raise ValueError("wrong result schema")
    libraries = {
        record["library"]: record for record in result.get("libraries", [])
    }
    if set(libraries) != set(EXPECTED):
        raise ValueError("wrong library set")
    for name, expected in EXPECTED.items():
        record = libraries[name]
        for field, value in expected.items():
            if record.get(field) != value:
                raise ValueError(
                    f"{name}: {field}={record.get(field)!r}, expected {value!r}"
                )
        if record.get("active_line_violations") != 0:
            raise ValueError(f"{name}: active-line violations")
        for row in record["rows"]:
            q_value = row["coarea_q"]
            if row["active_grid_max"] > q_value * q_value:
                raise ValueError(f"{name}: active-grid bound corrupted")
            if (
                row["margin_state_peak"]
                > row["margin_state_exact_product_bound_max"]
            ):
                raise ValueError(f"{name}: exact state bound violated")
            if (
                row["margin_state_exact_product_bound_max"]
                > row["margin_state_preregistered_bound"]
            ):
                raise ValueError(f"{name}: preregistered state bound violated")
            if (
                row["margin_state_exact_product_bound_max"]
                > row["margin_state_sharp_bound"]
            ):
                raise ValueError(f"{name}: sharp state bound violated")
            if row["tiling_state_peak"] > row["tiling_state_bound"]:
                raise ValueError(f"{name}: tiling state bound violated")


def main() -> int:
    total_started = time.perf_counter()
    libraries = load_libraries()
    analyses = []
    for library in libraries:
        record = analyse_library(library)
        analyses.append(record)
        print(
            f"{record['library']}: rows M/T "
            f"{record['margin_feasible_rows']}/{record['tiling_rows']}; "
            f"fiber {record['fiber_nodes']} = {record['tiling_nodes']} + "
            f"{record['extra_nodes']}; "
            f"support/pure/repair "
            f"{record['support_exact']}/{record['fiber_pure']}/"
            f"{record['repair_exact']}"
        )

    result = {
        "schema_version": "p42.coarea_fpt.v1",
        "preregistration": (
            "packages/package_e_obstruction_channels/xray_channel/"
            "COAREA_FPT_PREREGISTRATION.md"
        ),
        "algorithm": {
            "parameter": "coarea q = |T| - area(frozen largest piece)",
            "orientation_group": "D4",
            "directions": ["row", "column"],
            "move_graph": "nodes differing in exactly two named placements",
            "support_state_bound": "4^q (sharpening the preregistered (q+1)^(2q))",
            "tiling_state_bound": "2^q",
            "full_residual_tuple_bound": "2^(q^3) per largest placement",
            "strip_width_used": False,
        },
        "inputs": {
            library.name: {
                "path": library.input_path.relative_to(PROJECT).as_posix(),
                "sha256": hashlib.sha256(
                    library.input_path.read_bytes()
                ).hexdigest(),
                "bytes": library.input_path.stat().st_size,
            }
            for library in libraries
        },
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "random_seed": None,
        },
        "libraries": analyses,
        "runtime_seconds": round(time.perf_counter() - total_started, 6),
        "claim_boundary": {
            "status": "internal theorem candidate; no promotion",
            "does_not_claim": [
                "novelty against the parameterised-complexity literature",
                "a polynomial-time algorithm when q is unbounded",
                "a small or practical worst-case repair bound",
                "a paper-ready result",
            ],
        },
    }
    validate_result(result)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"PASS: {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
