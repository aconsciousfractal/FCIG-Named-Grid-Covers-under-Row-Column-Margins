#!/usr/bin/env python3
"""Write archive-level checksums for the explicit release payload."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "certificates" / "MANIFEST.json"
OUTPUT = ROOT / "SHA256SUMS"
CONTROLS = {"certificates/MANIFEST.json", "MANIFEST_SHA256.txt"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_file(relative: str) -> Path:
    posix = PurePosixPath(relative)
    if posix.is_absolute() or ".." in posix.parts:
        raise AssertionError(f"unsafe release path: {relative}")
    target = ROOT.joinpath(*posix.parts)
    if not target.is_file():
        raise AssertionError(f"missing release payload: {relative}")
    return target


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    payload = {row["path"] for row in manifest["artifacts"]} | CONTROLS
    rows = [f"{sha256(safe_file(relative)).upper()}  {relative}" for relative in sorted(payload)]
    OUTPUT.write_text(
        "# SHA-256 for the complete allowlisted release payload; SHA256SUMS excludes itself.\n"
        + "\n".join(rows)
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"WROTE {OUTPUT.name}: {len(rows)} release payload rows")
    print(f"SHA256SUMS_SHA256 {sha256(OUTPUT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
