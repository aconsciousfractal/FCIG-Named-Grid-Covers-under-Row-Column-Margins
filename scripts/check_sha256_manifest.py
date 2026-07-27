#!/usr/bin/env python3
"""Cross-platform checker for MANIFEST_SHA256.txt."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST_SHA256.txt"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def main() -> int:
    failures = []
    checked = 0
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        match = re.fullmatch(r"([0-9A-Fa-f]{64})  (.+)", line)
        if not match:
            failures.append(f"malformed row: {line!r}")
            continue
        expected, raw = match.groups()
        posix = PurePosixPath(raw)
        if posix.is_absolute() or ".." in posix.parts or re.match(r"^[A-Za-z]:", raw):
            failures.append(f"unsafe path: {raw}")
            continue
        target = ROOT.joinpath(*posix.parts)
        resolved = target.resolve(strict=False)
        if not target.is_file() or not (resolved == ROOT.resolve() or ROOT.resolve() in resolved.parents):
            failures.append(f"missing/escaping path: {raw}")
            continue
        actual = sha256(target)
        checked += 1
        if actual != expected.upper():
            failures.append(f"hash mismatch: {raw}")
    if failures:
        for failure in failures:
            print("FAIL", failure)
        return 1
    print(f"PASS source SHA-256 manifest ({checked}/{checked})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
