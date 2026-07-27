#!/usr/bin/env python3
"""Fail closed on incomplete, unsafe, or stale release-payload checksums."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "certificates" / "MANIFEST.json"
CHECKSUMS = ROOT / "SHA256SUMS"
CONTROLS = {"certificates/MANIFEST.json", "MANIFEST_SHA256.txt"}


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_file(relative: str) -> Path:
    posix = PurePosixPath(relative)
    require(not posix.is_absolute() and ".." not in posix.parts, f"unsafe checksum path: {relative}")
    target = ROOT.joinpath(*posix.parts)
    require(target.is_file(), f"missing checksum payload: {relative}")
    root_real = ROOT.resolve(strict=True)
    resolved = target.resolve(strict=True)
    require(root_real in resolved.parents, f"checksum path escapes root: {relative}")
    cursor = target
    while cursor != ROOT:
        require(not cursor.is_symlink(), f"symlinked checksum path: {relative}")
        cursor = cursor.parent
    return target


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    expected = {row["path"] for row in manifest["artifacts"]} | CONTROLS
    observed: dict[str, str] = {}
    for line in CHECKSUMS.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        match = re.fullmatch(r"([0-9A-Fa-f]{64})  (.+)", line)
        require(match is not None, f"malformed SHA256SUMS row: {line}")
        digest, relative = match.groups()
        require(relative not in observed, f"duplicate SHA256SUMS path: {relative}")
        observed[relative] = digest.lower()
    require(set(observed) == expected, "SHA256SUMS payload coverage")
    for relative, digest in observed.items():
        require(sha256(safe_file(relative)) == digest, f"SHA-256 mismatch: {relative}")
    print(f"PASS release checksums ({len(observed)} allowlisted payload files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
