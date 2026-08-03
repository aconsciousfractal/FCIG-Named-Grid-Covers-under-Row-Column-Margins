#!/usr/bin/env python3
"""Independent verification of the co-area sharpening package.

This verifier is deliberately separate from the supplied external bundle.  It
uses the independent bounding-box placement engine from
``verify_coarea_fpt.py`` and adds three checks that matter for the sharpening:

1. an exhaustive small-set audit and a locked-specimen audit of the
   translation cap;
2. an exact reconstruction of the Phi-energy panel on C46/P49/P21/P26;
3. a non-vacuous participation-type test with genuinely colliding named
   copies, plus a negative control whose exact type changes.

The script writes one deterministic JSON report under ``reports/``.
"""
from __future__ import annotations

import hashlib
import json
import math
from collections import Counter, defaultdict, deque
from itertools import combinations, product
from pathlib import Path

from verify_coarea_fpt import (
    Model,
    Shape,
    load_models,
    norm,
    poses,
    reflect,
    rotate,
)


HERE = Path(__file__).resolve().parent
PACKAGES = HERE.parent.parent
PROJECT = PACKAGES.parent
SPECIMENS = PACKAGES / "package_c_comparative_hypergraphs" / "specimens"
REPORT = PROJECT / "reports" / "P42_COAREA_NEXT_VERIFICATION.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def orientation_count(shape: Shape) -> int:
    output: set[Shape] = set()
    current = shape
    for _ in range(4):
        output.add(norm(current))
        output.add(reflect(current))
        current = rotate(current)
    return len(output)


def translations_into(shape: Shape, target: Shape) -> tuple[tuple[int, int], ...]:
    """All translations, derived by aligning one fixed shape cell to target."""
    anchor = min(shape)
    output = []
    for target_cell in target:
        shift = (
            target_cell[0] - anchor[0],
            target_cell[1] - anchor[1],
        )
        moved = frozenset(
            (row + shift[0], col + shift[1]) for row, col in shape
        )
        if moved <= target:
            output.append(shift)
    return tuple(sorted(output))


def exhaustive_translation_cap() -> dict:
    universe = tuple((row, col) for row in range(2) for col in range(3))
    subsets = [
        frozenset(
            universe[index]
            for index in range(len(universe))
            if mask & (1 << index)
        )
        for mask in range(1, 1 << len(universe))
    ]
    checks = 0
    equalities = 0
    for shape in subsets:
        for target in subsets:
            count = len(translations_into(shape, target))
            cap = len(target) - len(shape) + 1
            if count > max(0, cap):
                raise AssertionError(
                    f"translation cap failed: {shape=} {target=} {count=} {cap=}"
                )
            checks += 1
            equalities += count > 0 and count == cap
    return {
        "universe": "2x3",
        "ordered_nonempty_subset_pairs": checks,
        "equality_cases": equalities,
        "violations": 0,
    }


def line_counts(cells: Shape) -> tuple[Counter, Counter]:
    rows: Counter = Counter()
    columns: Counter = Counter()
    for row, col in cells:
        rows[row] += 1
        columns[col] += 1
    return rows, columns


def locked_translation_cap(model: Model) -> dict:
    target_rows, target_columns = line_counts(model.target)
    orientations = tuple(orientation_count(piece) for piece in model.pieces)
    checks = 0
    maximum_ratio = 0.0
    global_checks = 0

    for index, piece in enumerate(model.pieces):
        q_value = len(model.target) - len(piece)
        cap = orientations[index] * (q_value + 1)
        actual = len(model.placements[index])
        if actual > cap:
            raise AssertionError(
                f"{model.name} piece {index}: global {actual}>{cap}"
            )
        global_checks += 1

    for largest, piece in enumerate(model.pieces):
        q_value = len(model.target) - len(piece)
        for placed in model.placements[largest]:
            placed_rows, placed_columns = line_counts(placed)
            active_rows = {
                row
                for row, count in target_rows.items()
                if count - placed_rows[row] > 0
            }
            active_columns = {
                col
                for col, count in target_columns.items()
                if count - placed_columns[col] > 0
            }
            active_grid = frozenset(
                (row, col)
                for row, col in model.target
                if row in active_rows and col in active_columns
            )
            if (
                len(active_rows) > q_value
                or len(active_columns) > q_value
                or len(active_grid) > q_value * q_value
            ):
                raise AssertionError(f"{model.name}: active-grid bound failed")
            for residual, residual_piece in enumerate(model.pieces):
                if residual == largest or len(residual_piece) > q_value:
                    continue
                actual = sum(
                    candidate <= active_grid
                    for candidate in model.placements[residual]
                )
                cap = orientations[residual] * max(
                    0, len(active_grid) - len(residual_piece) + 1
                )
                if actual > cap:
                    raise AssertionError(
                        f"{model.name}: active cap {actual}>{cap}"
                    )
                if cap:
                    maximum_ratio = max(maximum_ratio, actual / cap)
                checks += 1
    return {
        "global_piece_checks": global_checks,
        "active_grid_piece_checks": checks,
        "maximum_active_ratio": maximum_ratio,
        "violations": 0,
    }


def model_from_locked(filename: str) -> Model:
    path = SPECIMENS / filename
    data = json.loads(path.read_text(encoding="utf-8"))
    target_data = data["target"]
    removed = {tuple(cell) for cell in target_data.get("remove", [])}
    target = frozenset(
        (row, col)
        for row in range(target_data["rows"])
        for col in range(target_data["cols"])
        if (row, col) not in removed
    )
    pieces = tuple(
        norm(tuple(cell) for cell in piece) for piece in data["pieces"]
    )
    return Model(
        data["specimen"],
        tuple(range(len(pieces))),
        pieces,
        target,
        path,
    )


def adjacency(nodes: tuple[tuple[Shape, ...], ...]) -> list[set[int]]:
    result = [set() for _ in nodes]
    width = len(nodes[0]) if nodes else 0
    for changed in combinations(range(width), 2):
        fixed = tuple(index for index in range(width) if index not in changed)
        buckets: dict[tuple[Shape, ...], list[int]] = defaultdict(list)
        for index, node in enumerate(nodes):
            buckets[tuple(node[position] for position in fixed)].append(index)
        for values in buckets.values():
            for left, right in combinations(values, 2):
                if all(
                    nodes[left][position] != nodes[right][position]
                    for position in changed
                ):
                    result[left].add(right)
                    result[right].add(left)
    return result


def energy_summary(nodes: tuple[tuple[Shape, ...], ...], target: Shape) -> dict:
    energy = [
        len(target) - len(frozenset().union(*node))
        for node in nodes
    ]
    tilings = {index for index, value in enumerate(energy) if value == 0}
    edges = adjacency(nodes)
    component = [-1] * len(nodes)
    components: list[list[int]] = []
    for start in range(len(nodes)):
        if component[start] >= 0:
            continue
        number = len(components)
        component[start] = number
        stack = [start]
        values = []
        while stack:
            current = stack.pop()
            values.append(current)
            for neighbour in edges[current]:
                if component[neighbour] < 0:
                    component[neighbour] = number
                    stack.append(neighbour)
        components.append(values)
    tiled_components = {component[index] for index in tilings}
    trapped = {
        index
        for index in range(len(nodes))
        if component[index] not in tiled_components
    }
    local_minima = {
        index
        for index, value in enumerate(energy)
        if value > 0
        and not any(energy[neighbour] < value for neighbour in edges[index])
    }
    distances: list[int | None] = [None] * len(nodes)
    queue = deque(tilings)
    for index in tilings:
        distances[index] = 0
    while queue:
        current = queue.popleft()
        for neighbour in edges[current]:
            if distances[neighbour] is None:
                distances[neighbour] = distances[current] + 1  # type: ignore[operator]
                queue.append(neighbour)
    finite = [value for value in distances if value is not None]
    return {
        "fiber_nodes": len(nodes),
        "tilings": len(tilings),
        "extras": len(nodes) - len(tilings),
        "trapped_nodes": len(trapped),
        "nonzero_local_minima": len(local_minima),
        "trapped_equals_nonzero_local_minima": trapped == local_minima,
        "maximum_finite_repair_distance": max(finite, default=0),
    }


def energy_panel(model: Model) -> dict:
    totals: Counter = Counter()
    exact_every_row = True
    for quad in model.quaternes():
        nodes = model.fiber(quad)
        if not nodes:
            continue
        row = energy_summary(nodes, model.target)
        for field in (
            "fiber_nodes",
            "tilings",
            "extras",
            "trapped_nodes",
            "nonzero_local_minima",
        ):
            totals[field] += row[field]
        totals["margin_feasible_rows"] += 1
        totals["maximum_finite_repair_distance"] = max(
            totals["maximum_finite_repair_distance"],
            row["maximum_finite_repair_distance"],
        )
        exact_every_row &= row["trapped_equals_nonzero_local_minima"]
    return {
        "area_compatible_rows": len(model.quaternes()),
        "margin_feasible_rows": totals["margin_feasible_rows"],
        "fiber_nodes": totals["fiber_nodes"],
        "tilings": totals["tilings"],
        "extras": totals["extras"],
        "trapped_nodes": totals["trapped_nodes"],
        "nonzero_local_minima": totals["nonzero_local_minima"],
        "all_rows_exact": exact_every_row,
        "maximum_finite_repair_distance": totals[
            "maximum_finite_repair_distance"
        ],
    }


def participation_signature(model: Model, largest: int, piece: int) -> tuple:
    per_largest = []
    for placed, placed_xray in zip(
        model.placements[largest], model.xrays[largest]
    ):
        residual = tuple(
            target - value
            for target, value in zip(model.target_xray, placed_xray)
        )
        values = tuple(
            sorted(
                (
                    tuple(sorted(candidate))
                    for candidate, candidate_xray in zip(
                        model.placements[piece], model.xrays[piece]
                    )
                    if all(
                        value <= bound
                        for value, bound in zip(candidate_xray, residual)
                    )
                )
            )
        )
        per_largest.append((tuple(sorted(placed)), values))
    return len(model.pieces[piece]), tuple(per_largest)


def synthetic_type_collision() -> dict:
    target = frozenset((row, col) for row in range(2) for col in range(3))
    largest = norm(((0, 0), (1, 0), (1, 1)))
    monomino = norm(((0, 0),))
    domino = norm(((0, 0), (0, 1)))
    separated_pair = norm(((0, 0), (0, 2)))
    pieces = (
        largest,
        monomino,
        monomino,
        domino,
        domino,
        separated_pair,
    )
    model = Model(
        "synthetic-type-collision",
        tuple(range(len(pieces))),
        pieces,
        target,
        Path(__file__),
    )
    signatures = {
        index: participation_signature(model, 0, index)
        for index in range(1, len(pieces))
    }
    if signatures[1] != signatures[2] or signatures[3] != signatures[4]:
        raise AssertionError("named duplicate pieces did not collide by type")
    if signatures[3] == signatures[5]:
        raise AssertionError("placement-sensitive negative control collapsed")

    rows = ((0, 1, 3), (0, 1, 4), (0, 2, 3), (0, 2, 4))
    grouped: dict[tuple, list[dict]] = defaultdict(list)
    for row in rows:
        key = tuple(sorted(signatures[index] for index in row[1:]))
        nodes = tuple(
            tuple(model.placements[row[position]][choice[position]] for position in range(3))
            for choice in product(
                *(range(len(model.placements[index])) for index in row)
            )
            if tuple(
                sum(
                    model.xrays[row[position]][choice[position]][coordinate]
                    for position in range(3)
                )
                for coordinate in range(len(model.target_xray))
            )
            == model.target_xray
        )
        grouped[key].append(energy_summary(nodes, target))
    if len(grouped) != 1 or len(next(iter(grouped.values()))) != 4:
        raise AssertionError("synthetic type collision was not non-vacuous")
    values = next(iter(grouped.values()))
    if any(value != values[0] for value in values[1:]):
        raise AssertionError("same exact type vector changed fiber behavior")
    return {
        "named_sublibraries": len(rows),
        "exact_type_vectors": len(grouped),
        "duplicate_monomino_type_equal": True,
        "duplicate_domino_type_equal": True,
        "placement_sensitive_negative_control_separated": True,
        "common_fiber_summary": values[0],
        "output_size_control": {
            "q": 5,
            "named_monominoes": 30,
            "literal_outputs": math.comb(30, 5),
            "compressed_vectors": 1,
        },
    }


def main() -> int:
    c32, c46, p49 = load_models()
    del c32
    p21 = model_from_locked("p21_locked.json")
    p26 = model_from_locked("p26_locked.json")
    models = (c46, p49, p21, p26)

    translation = {
        model.name: locked_translation_cap(model) for model in models
    }
    if sum(
        item["active_grid_piece_checks"] for item in translation.values()
    ) != 44_910:
        raise AssertionError("locked translation-check total changed")

    panel = {model.name: energy_panel(model) for model in models}
    expected = {
        "C46": (352, 344, 8, 0, 0, True, 1),
        "P49-base": (1344, 1208, 136, 16, 16, True, 1),
        "P21": (1680, 672, 1008, 736, 792, False, 2),
        "P26": (1554, 1051, 503, 329, 343, False, 3),
    }
    for name, values in expected.items():
        observed = panel[name]
        actual = (
            observed["fiber_nodes"],
            observed["tilings"],
            observed["extras"],
            observed["trapped_nodes"],
            observed["nonzero_local_minima"],
            observed["all_rows_exact"],
            observed["maximum_finite_repair_distance"],
        )
        if actual != values:
            raise AssertionError(f"{name}: energy panel {actual} != {values}")

    report = {
        "status": "PASS",
        "scope": {
            "theorems": [
                "translation cap finite audits",
                "Phi-energy finite panel",
                "exact participation-type invariance",
            ],
            "nonclaim": "finite checks support but do not prove the general theorems",
        },
        "small_translation_exhaustion": exhaustive_translation_cap(),
        "locked_translation_audit": translation,
        "locked_translation_checks": 44_910,
        "energy_panel": panel,
        "synthetic_type_collision": synthetic_type_collision(),
        "input_hashes": {
            model.name: sha256(model.source) for model in models
        },
    }
    REPORT.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print("co-area sharpening verification: PASS")
    print("  exhaustive small translation pairs:", report["small_translation_exhaustion"]["ordered_nonempty_subset_pairs"])
    print("  locked active-grid checks:", report["locked_translation_checks"])
    for name, values in panel.items():
        print(
            f"  {name:8s}: {values['fiber_nodes']}="
            f"{values['tilings']}+{values['extras']}; "
            f"trapped={values['trapped_nodes']}; "
            f"local-min={values['nonzero_local_minima']}; "
            f"radius={values['maximum_finite_repair_distance']}"
        )
    collision = report["synthetic_type_collision"]
    print(
        "  synthetic exact-type collision:",
        f"{collision['named_sublibraries']} named rows -> "
        f"{collision['exact_type_vectors']} type vector",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
