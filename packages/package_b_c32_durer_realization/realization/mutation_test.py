#!/usr/bin/env python3
"""Adversarial mutation controls for the independent C32 verifier."""
from __future__ import annotations

import copy
import json

from verify import DEFAULT_BUNDLE, DEFAULT_LOCK, verify_bundle


def first_record(bundle: dict, *, tiles: bool) -> dict:
    return next(
        record
        for record in bundle["records"].values()
        if record["tiles"] is tiles
    )


def main() -> int:
    original = json.loads(DEFAULT_BUNDLE.read_text(encoding="utf-8"))
    lock = json.loads(DEFAULT_LOCK.read_text(encoding="utf-8"))
    controls = [
        ("original", original),
        ("lossless_deep_copy", copy.deepcopy(original)),
    ]
    mutations: list[tuple[str, dict]] = []

    changed = copy.deepcopy(original)
    changed["source"]["raster_sha256"] = "0" * 64
    mutations.append(("source_hash", changed))

    changed = copy.deepcopy(original)
    changed["normalization"]["target_cells"].pop()
    mutations.append(("target_cell", changed))

    changed = copy.deepcopy(original)
    changed["normalization"]["pieces"]["8"].pop()
    mutations.append(("piece_mask", changed))

    changed = copy.deepcopy(original)
    positive = first_record(changed, tiles=True)
    positive["tilings"][0][0]["cells"].pop()
    mutations.append(("positive_placement", changed))

    changed = copy.deepcopy(original)
    first_record(changed, tiles=True)["tiling_count"] += 1
    mutations.append(("tiling_count", changed))

    changed = copy.deepcopy(original)
    negative = first_record(changed, tiles=False)
    negative["tiles"] = True
    mutations.append(("negative_verdict", changed))

    changed = copy.deepcopy(original)
    first_record(changed, tiles=True)["owner_complement_values"][0] += 1
    mutations.append(("owner_crosswalk", changed))

    changed = copy.deepcopy(original)
    del changed["records"][next(iter(changed["records"]))]
    mutations.append(("missing_row", changed))

    failed = False
    for name, bundle in controls:
        status = verify_bundle(bundle, lock)["status"]
        ok = status == "PASS"
        failed |= not ok
        print(f"[{'PASS' if ok else 'FAIL'}] control {name}: verifier={status}")
    for name, bundle in mutations:
        result = verify_bundle(bundle, lock)
        ok = result["status"] == "FAIL" and bool(result["errors"])
        failed |= not ok
        print(
            f"[{'PASS' if ok else 'FAIL'}] mutation {name}: "
            f"verifier={result['status']} errors={len(result['errors'])}"
        )
    print(f"\nSTATUS: {'FAIL' if failed else 'PASS'}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
