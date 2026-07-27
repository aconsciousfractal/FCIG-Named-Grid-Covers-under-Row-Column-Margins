#!/usr/bin/env python3
"""Replay the integrated P42 orbit/Markov closure.

Smoke mode replays the minimum-orbit theorem, the degree-2/3 and degree-7
Markov obstruction, and the 4ti2 export.  ``--full`` includes the degree-4
Betti census.  ``--single-block`` additionally reruns the longer degree-2-to-7
single-block audit.  Semantic JSON comparison is intentional; the 4ti2 export
is byte-compared after its writer freezes LF line endings on every platform.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
REPORTS = PROJECT / "reports"


def run(command: list[str]) -> None:
    print("+", " ".join(command), flush=True)
    subprocess.run(command, check=True)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def assert_equal(actual, expected, label: str) -> None:
    if actual != expected:
        raise AssertionError(f"{label} mismatch")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--xray-dir", type=Path, required=True)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--single-block", action="store_true")
    args = parser.parse_args()
    xray = args.xray_dir.resolve()
    python = sys.executable

    with tempfile.TemporaryDirectory(prefix="p42_orbit_markov_") as tmp_name:
        tmp = Path(tmp_name)

        minimum_out = tmp / "minimum.json"
        run([
            python, "-X", "utf8", "-B",
            str(HERE / "verify_minimum_orbit_generators.py"),
            "--xray-dir", str(xray),
            "--output", str(minimum_out),
        ])
        assert_equal(
            load(minimum_out),
            load(REPORTS / "P42_MINIMUM_ORBIT_GENERATORS_CERTIFICATE.json"),
            "minimum-orbit certificate",
        )
        print("PASS minimum-orbit byte-semantic replay")

        markov_out = tmp / "markov.json"
        command = [
            python, "-X", "utf8", "-B",
            str(HERE / "verify_markov_no_go.py"),
            "--xray-dir", str(xray),
            "--output", str(markov_out),
        ]
        if not args.full:
            command.append("--skip-degree4")
        run(command)
        actual = load(markov_out)
        expected = load(REPORTS / "P42_MARKOV_NO_GO_CERTIFICATE.json")
        if args.full:
            assert_equal(actual, expected, "full Markov certificate")
            print("PASS full Markov certificate replay")
        else:
            for key in ("configuration", "terminology_correction", "degree_two", "degree_seven_indispensable_witness"):
                assert_equal(actual[key], expected[key], f"smoke Markov field {key}")
            for degree in ("2", "3"):
                assert_equal(
                    actual["low_degree_betti_census"][degree],
                    expected["low_degree_betti_census"][degree],
                    f"smoke Betti degree {degree}",
                )
            assert actual["verdict"]["squarefree_support_le_4_is_all_rhs_Markov"] is False
            assert actual["verdict"]["Markov_degree_lower_bound"] == 7
            print("PASS Markov smoke replay (degrees 2,3 and indispensable degree 7)")

        export_dir = tmp / "export"
        run([
            python, "-X", "utf8", "-B",
            str(HERE / "export_4ti2_configuration.py"),
            "--xray-dir", str(xray),
            "--out-dir", str(export_dir),
        ])
        for name in (
            "p21_participating_markov_14x72.mat",
            "p21_participating_markov_rank12.mat",
            "p21_participating_markov.sign",
            "p21_participating_markov_metadata.json",
        ):
            assert_equal((export_dir / name).read_bytes(), (HERE / name).read_bytes(), f"export {name}")
        print("PASS 4ti2 export replay")

        if args.single_block:
            block_out = tmp / "single_block.json"
            run([
                python, "-X", "utf8", "-B",
                str(HERE / "audit_single_block_markov_degrees.py"),
                "--xray-dir", str(xray),
                "--output", str(block_out),
            ])
            assert_equal(
                load(block_out),
                load(REPORTS / "P42_SINGLE_BLOCK_MARKOV_DEGREES.json"),
                "single-block audit",
            )
            print("PASS optional single-block audit")

    print("PASS P42 orbit/Markov closure replay")


if __name__ == "__main__":
    main()
