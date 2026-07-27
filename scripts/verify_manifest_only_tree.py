#!/usr/bin/env python3
"""Replay the full profile from a temporary tree containing only manifest payload."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "certificates" / "MANIFEST.json"
CHILD_FLAG = "P42_MANIFEST_ONLY_CHILD"


def main() -> int:
    if os.environ.get(CHILD_FLAG) == "1":
        print("PASS manifest-only nested replay guard")
        return 0

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    payload = {row["path"] for row in manifest["artifacts"]}
    payload.update({"certificates/MANIFEST.json", "MANIFEST_SHA256.txt", "SHA256SUMS"})

    with tempfile.TemporaryDirectory(prefix="p42-manifest-only-") as raw_stage:
        stage = Path(raw_stage)
        for relative in sorted(payload):
            posix = PurePosixPath(relative)
            if posix.is_absolute() or ".." in posix.parts:
                raise AssertionError(f"unsafe manifest path: {relative}")
            source = ROOT.joinpath(*posix.parts)
            target = stage.joinpath(*posix.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)

        command = [
            sys.executable,
            "-X",
            "utf8",
            "-B",
            str(stage / "scripts" / "verify.py"),
            "--profile",
            "full",
            "--output",
            str(stage / "results" / "manifest_only_verification.json"),
            "--run-log",
            str(stage / "results" / "manifest_only_run.json"),
        ]
        environment = os.environ.copy()
        environment[CHILD_FLAG] = "1"
        environment["PYTHONHASHSEED"] = "0"
        environment.pop("PYTHONPATH", None)
        completed = subprocess.run(
            command,
            cwd=stage,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if completed.stdout:
            print(completed.stdout, end="")
        if completed.stderr:
            print(completed.stderr, end="", file=sys.stderr)
        if completed.returncode:
            raise RuntimeError(
                f"manifest-only full replay failed with exit code {completed.returncode}"
            )

    print(f"PASS manifest-only full replay ({len(payload)} staged payload files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
