#!/usr/bin/env python3
"""Fail-closed standalone verification entry point for P42 Output T."""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import importlib.util
import json
import os
import platform
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

from audit_import_closure import audit as audit_import_closure


PACKAGE = Path(__file__).resolve().parent
PROJECT = PACKAGE.parent
MANIFEST = PROJECT / "certificates" / "MANIFEST.json"
ENVIRONMENT_LOCK = PROJECT / "certificates" / "environment.json"
DEFAULT_OUTPUT = PROJECT / "results" / "verification.json"
DEFAULT_RUN_LOG = PROJECT / "results" / "verification_run.json"
PYTHON = [sys.executable, "-X", "utf8", "-B"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def text_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def load_json(root: Path, relative: str):
    return json.loads((root / relative).read_text(encoding="utf-8"))


def safe_target(project: Path, raw: str) -> Path:
    posix = PurePosixPath(raw)
    require(not posix.is_absolute(), f"absolute manifest path: {raw}")
    require(not re.match(r"^[A-Za-z]:", raw), f"drive-qualified manifest path: {raw}")
    require(".." not in posix.parts, f"escaping manifest path: {raw}")
    target = project.joinpath(*posix.parts)
    require(target.is_file(), f"missing artifact: {raw}")

    project_real = project.resolve(strict=True)
    resolved = target.resolve(strict=True)
    require(
        resolved == project_real or project_real in resolved.parents,
        f"resolved path escapes project: {raw} -> {resolved}",
    )
    cursor = target
    while cursor != project:
        require(not cursor.is_symlink(), f"symlinked manifest path component: {raw}")
        cursor = cursor.parent
    return target


def snapshot_artifacts(project: Path, manifest: dict) -> dict[str, dict[str, int | str]]:
    return {
        row["path"]: {
            "bytes": safe_target(project, row["path"]).stat().st_size,
            "sha256": sha256(safe_target(project, row["path"])),
        }
        for row in manifest["artifacts"]
    }


def check_manifest() -> tuple[dict, list[str], dict[str, dict[str, int | str]]]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    require(manifest["schema"] == "p42.output-t.public-candidate-manifest.v1", "manifest schema")
    require(manifest["project_id"] == "P42-T", "project id")
    require(manifest["status"] == "LOCAL_PUBLIC_RELEASE_CANDIDATE", "candidate status")
    require(manifest["project_root_contract"] == ".", "project-root contract")
    require(manifest["parameter_name"] == "largest-piece residual area", "parameter wording")
    boundary = manifest["boundary"]
    require(boundary["public_authority"] is False, "public authority must be false")
    require(boundary["remote_or_release_authority"] is False, "release authority must be false")
    require(boundary["priority_or_firstness_clearance"] is False, "priority clearance must be false")
    require(boundary["source_raster_bytes_redistributed"] is False, "source raster boundary")
    require(boundary["external_reproduction"] is False, "external reproduction boundary")
    require(boundary["p21_exact_markov_basis"] == "open_owner_parked", "P21 stop boundary")

    seen: set[str] = set()
    categories: set[str] = set()
    for row in manifest["artifacts"]:
        raw = row["path"]
        require(raw not in seen, f"duplicate manifest path: {raw}")
        seen.add(raw)
        categories.add(row["category"])
        target = safe_target(PROJECT, raw)
        require(target.stat().st_size == row["bytes"], f"byte-count mismatch: {raw}")
        require(sha256(target) == row["sha256"], f"SHA-256 mismatch: {raw}")

    required_categories = {
        "reviewer",
        "environment",
        "governance",
        "theorem",
        "sources",
        "manuscript",
        "source_lock",
        "replay_code",
        "certificate",
        "verification",
    }
    require(required_categories <= categories, "manifest category coverage")
    snapshot = snapshot_artifacts(PROJECT, manifest)
    return manifest, [
        "manifest_schema_boundary_and_parameter_wording",
        "manifest_realpath_and_symlink_safety",
        "manifest_hashes_and_sizes",
        "manifest_category_coverage",
    ], snapshot


def check_environment() -> tuple[dict, list[str]]:
    lock = json.loads(ENVIRONMENT_LOCK.read_text(encoding="utf-8"))
    require(lock["schema"] == "p42.output-t.public-environment.v1", "environment lock schema")
    actual_python = platform.python_version()
    actual_implementation = platform.python_implementation()
    actual_major_minor = sys.version_info[:2]
    minimum = tuple(int(value) for value in lock["python"]["minimum"].split("."))
    maximum_exclusive = tuple(
        int(value) for value in lock["python"]["maximum_exclusive"].split(".")
    )
    require(
        minimum <= actual_major_minor < maximum_exclusive,
        (
            f"Python version {actual_python} is outside "
            f"[{lock['python']['minimum']}, {lock['python']['maximum_exclusive']})"
        ),
    )
    require(
        actual_implementation == lock["python"]["implementation"],
        f"Python implementation {actual_implementation}",
    )
    packages = []
    for row in lock["packages"]:
        version = importlib.metadata.version(row["distribution"])
        require(version == row["version"], f"{row['distribution']} version {version}")
        require(importlib.util.find_spec(row["import_name"]) is not None, f"missing import {row['import_name']}")
        packages.append({"distribution": row["distribution"], "version": version})
    fingerprint = {
        "architecture": platform.machine(),
        "operating_system": platform.platform(),
        "packages": packages,
        "python_implementation": actual_implementation,
        "python_version": actual_python,
    }
    return fingerprint, ["bounded_python_and_locked_dependency_preflight"]


def check_semantics(root: Path = PROJECT) -> list[str]:
    manuscript = load_json(root, "results/p42_tomographic_manuscript_verification.json")
    require(manuscript["status"] == "PASS", "manuscript receipt status")
    require(len(manuscript["checks"]) >= 9, "manuscript receipt check count")
    pdf_check = next(row for row in manuscript["checks"] if row["name"] == "built_pdf")
    require(pdf_check["passed"] is True, "manuscript PDF receipt")
    require(pdf_check["detail"]["pages"] == 18, "manuscript PDF page count")

    coarea = load_json(root, "results/coarea_fpt_analysis.json")
    libraries = {row["library"]: row for row in coarea["libraries"]}
    expected = {
        "C32": (136, 136, 20, 20, 0, True, True, True, 0),
        "C46": (352, 344, 44, 44, 8, True, False, True, 0),
        "P49-base": (1344, 1208, 61, 60, 136, False, False, False, 16),
    }
    fields = (
        "fiber_nodes",
        "tiling_nodes",
        "margin_feasible_rows",
        "tiling_rows",
        "extra_nodes",
        "support_exact",
        "fiber_pure",
        "repair_exact",
        "trapped_components",
    )
    for name, values in expected.items():
        require(name in libraries, f"missing residual-area library {name}")
        require(tuple(libraries[name][field] for field in fields) == values, f"aggregate {name}")

    coarea_next = load_json(root, "reports/P42_COAREA_NEXT_VERIFICATION.json")
    require(coarea_next["status"] == "PASS", "residual-area sharpening receipt")
    require(coarea_next["locked_translation_checks"] == 44910, "locked translation checks")
    require(
        coarea_next["small_translation_exhaustion"]["ordered_nonempty_subset_pairs"] == 3969,
        "small translation exhaustion",
    )
    require(coarea_next["synthetic_type_collision"]["named_sublibraries"] == 4, "type collision input")
    require(coarea_next["synthetic_type_collision"]["exact_type_vectors"] == 1, "type collision compression")
    require(
        coarea_next["input_hashes"]["P26"]
        == "2732d9400d3a02eb889799306f51985fa765c3106214e01e36ddfadc8c06a35e",
        "P26 locked-input hash",
    )
    p26 = coarea_next["energy_panel"]["P26"]
    require(
        (
            p26["fiber_nodes"],
            p26["tilings"],
            p26["extras"],
            p26["trapped_nodes"],
            p26["nonzero_local_minima"],
            p26["all_rows_exact"],
            p26["maximum_finite_repair_distance"],
        )
        == (1554, 1051, 503, 329, 343, False, 3),
        "P26 energy-panel anchors",
    )

    for relative in (
        "reports/P42_ROBUST_P21_QUOTIENT_VERIFICATION.json",
        "reports/P42_DEGREE3_AUGMENTATION_VERIFICATION.json",
        "reports/P42_SUPPORT4_CEILING_VERIFICATION.json",
    ):
        require(load_json(root, relative)["status"] == "PASS", f"frozen receipt {relative}")

    minimum = load_json(root, "reports/P42_MINIMUM_ORBIT_GENERATORS_CERTIFICATE.json")
    require(
        (
            minimum["participating_columns"],
            minimum["kernel_rank"],
            minimum["rank_M_le_3"],
            minimum["quotient_rank"],
            minimum["support_four_moves"],
            minimum["target_orbits"],
        )
        == (72, 60, 51, 9, 7444, 1119),
        "minimum-orbit structural ranks",
    )
    require(minimum["family_sizes"] == [6, 3, 78], "minimum-orbit family sizes")
    require(
        minimum["fixed_fiber_visibility"]["rank_three_family_active_counts"] == [0, 0, 36],
        "fixed-fiber visibility",
    )
    require(minimum["minimum_complete_target_orbits"] == 3, "minimum orbit count")
    require(minimum["number_of_minimum_families"] == 1404, "minimum family count")
    require(minimum["canonical_orbit_family"] == [283, 603, 714], "canonical orbit family")
    require(minimum["canonical_determinant"] == -1, "canonical determinant")

    markov = load_json(root, "reports/P42_MARKOV_NO_GO_CERTIFICATE.json")
    require(markov["degree_two"]["indispensable_binomials"] == 218, "indispensable quadrics")
    require(markov["degree_two"]["cross_colour_existing"] == 144, "existing cross-block quadrics")
    require(markov["degree_two"]["same_colour_missing"] == 74, "missing same-block quadrics")
    census = markov["low_degree_betti_census"]
    require(census["2"]["minimum_generators_in_degree"] == 218, "degree-2 Betti census")
    require(census["3"]["minimum_generators_in_degree"] == 996, "degree-3 Betti census")
    require(census["4"]["betti_fibers"] == 5705, "degree-4 Betti fibers")
    require(census["4"]["minimum_generators_in_degree"] == 5727, "degree-4 generators")
    require(markov["minimal_generator_lower_bound_through_audited_degrees"] == 6941, "generator lower bound")
    verdict = markov["verdict"]
    require(verdict["squarefree_support_le_4_is_lattice_generating"] is True, "support-four lattice generation")
    require(verdict["squarefree_support_le_4_is_all_rhs_Markov"] is False, "all-RHS Markov no-go")
    require(verdict["Markov_degree_lower_bound"] == 7, "Markov degree lower bound")
    require(verdict["full_Markov_degree"] == "open", "exact Markov degree boundary")

    single = load_json(root, "reports/P42_SINGLE_BLOCK_MARKOV_DEGREES.json")
    require(single["Markov_degree_lower_bound"] == 7, "single-block degree boundary")

    return [
        "manuscript_receipt_and_built_pdf",
        "C32_C46_P49_frozen_aggregates",
        "translation_type_energy_receipt",
        "bounded_P21_stage_receipts",
        "minimum_three_orbit_certificate",
        "markov_no_go_and_degree_seven_boundary",
    ]


def command_map(project: Path) -> dict[str, list[str]]:
    xray = project / "packages" / "package_e_obstruction_channels" / "xray_channel"
    c32 = project / "packages" / "package_b_c32_durer_realization" / "realization"
    c46 = project / "packages" / "package_a_c46_reproduction" / "realization"
    scripts = project / "scripts"
    specimens = project / "packages" / "package_c_comparative_hypergraphs" / "specimens"
    return {
        "manuscript": PYTHON + [str(scripts / "verify_tomographic_manuscript.py")],
        "c32_certificate": PYTHON + [str(c32 / "verify.py")],
        "c32_analysis": PYTHON + [str(c32 / "verify_analysis.py")],
        "c46_certificate": PYTHON + [str(c46 / "verify.py")],
        "coarea": PYTHON + [str(xray / "verify_coarea_fpt.py")],
        "specimens": PYTHON + [str(specimens / "validate_specimens.py")],
        "coarea_next": PYTHON + [str(xray / "verify_coarea_next.py")],
        "c32_mutation": PYTHON + [str(c32 / "mutation_test.py")],
        "c46_mutation": PYTHON + [str(c46 / "mutation_test.py")],
        "coarea_mutation": PYTHON + [str(xray / "mutation_coarea_fpt.py")],
        "p21_smoke": PYTHON + [str(xray / "verify_orbit_markov_closure.py"), "--xray-dir", str(xray)],
        "p21_full": PYTHON + [
            str(xray / "verify_orbit_markov_closure.py"),
            "--xray-dir",
            str(xray),
            "--full",
            "--single-block",
        ],
        "repository": PYTHON + [str(scripts / "validate_repository.py")],
        "release_checksums": PYTHON + [str(scripts / "check_release_checksums.py")],
        "manifest_only_tree": PYTHON + [str(scripts / "verify_manifest_only_tree.py")],
    }


def normalized_argv(command: list[str]) -> list[str]:
    project_text = str(PROJECT)
    normalized = []
    for value in command:
        if value == sys.executable:
            normalized.append("<PYTHON>")
        elif value.lower().startswith(project_text.lower()):
            suffix = value[len(project_text):].lstrip("\\/").replace("\\", "/")
            normalized.append(f"<PROJECT>/{suffix}" if suffix else "<PROJECT>")
        else:
            normalized.append(value)
    return normalized


def run_commands(command_ids: list[str], active_profile: str) -> tuple[list[dict], list[dict]]:
    commands = command_map(PROJECT)
    stable = []
    volatile = []
    environment = os.environ.copy()
    environment["P42_OUTPUT_T_REVIEWER_ACTIVE_PROFILE"] = active_profile
    environment["PYTHONHASHSEED"] = "0"
    environment.pop("PYTHONPATH", None)
    for command_id in command_ids:
        command = commands[command_id]
        print("+", command_id, flush=True)
        started = time.perf_counter()
        completed = subprocess.run(
            command,
            cwd=PROJECT,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        duration = time.perf_counter() - started
        if completed.stdout:
            print(completed.stdout, end="")
        if completed.stderr:
            print(completed.stderr, end="", file=sys.stderr)
        stable.append(
            {
                "argv": normalized_argv(command),
                "cwd": "<PROJECT>",
                "exit_code": completed.returncode,
                "id": command_id,
                "status": "PASS" if completed.returncode == 0 else "FAIL",
                "stderr_sha256": text_sha256(completed.stderr),
                "stdout_sha256": text_sha256(completed.stdout),
            }
        )
        volatile.append(
            {
                "argv": command,
                "duration_seconds": round(duration, 6),
                "exit_code": completed.returncode,
                "id": command_id,
                "stderr": completed.stderr,
                "stdout": completed.stdout,
            }
        )
        if completed.returncode:
            raise RuntimeError(f"{command_id} failed with exit code {completed.returncode}")
    return stable, volatile


def write_json(path: Path, payload: dict) -> None:
    path = path.resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=("manifest", "core", "full"), default="core")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--run-log", type=Path, default=DEFAULT_RUN_LOG)
    args = parser.parse_args()

    started_utc = datetime.now(timezone.utc)
    manifest_before, checks_before, snapshot_before = check_manifest()
    manifest_sha_before = sha256(MANIFEST)
    environment, environment_checks = check_environment()
    import_closure = audit_import_closure(PROJECT, manifest_before)
    require(import_closure["status"] == "PASS", f"import closure: {import_closure}")
    semantics_before = check_semantics()

    commands, volatile_commands = run_commands(manifest_before["profiles"][args.profile], args.profile)

    manifest_after, checks_after, snapshot_after = check_manifest()
    require(manifest_after == manifest_before, "manifest JSON changed during replay")
    require(sha256(MANIFEST) == manifest_sha_before, "manifest bytes changed during replay")
    require(snapshot_after == snapshot_before, "frozen artifact bytes changed during replay")
    semantics_after = check_semantics()
    require(semantics_after == semantics_before, "semantic anchors changed during replay")

    finished_utc = datetime.now(timezone.utc)
    run_log = {
        "commands": volatile_commands,
        "finished_utc": finished_utc.isoformat(),
        "note": "Volatile timestamps, durations and raw logs; excluded from MANIFEST.json.",
        "profile": args.profile,
        "schema": "p42.output-t.public-candidate-run-log.v1",
        "started_utc": started_utc.isoformat(),
        "status": "PASS",
    }
    write_json(args.run_log, run_log)

    receipt = {
        "commands": commands,
        "environment": environment,
        "import_closure": {
            key: value for key, value in import_closure.items() if key != "missing_project_local_files"
        },
        "manifest": {
            "artifact_count": len(manifest_before["artifacts"]),
            "post_replay_sha256": sha256(MANIFEST),
            "pre_replay_sha256": manifest_sha_before,
            "snapshot_unchanged": snapshot_after == snapshot_before,
        },
        "profile": args.profile,
        "schema": "p42.output-t.public-candidate-verification.v1",
        "semantic_checks_after": checks_after + semantics_after,
        "semantic_checks_before": checks_before + environment_checks + ["project_local_import_closure"] + semantics_before,
        "status": "PASS",
        "terminal": f"PASS P42 Output T public-repository candidate ({args.profile})",
        "volatile_run_log": "results/verification_run.json",
    }
    write_json(args.output, receipt)
    print(receipt["terminal"])
    print(f"WROTE {args.output.resolve()}")
    print(f"WROTE {args.run_log.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
