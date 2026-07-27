#!/usr/bin/env python3
"""Fail-closed final RT-1..RT-15 gate for the Output T repository candidate."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs" / "RED_TEAM_REPORT.md"
OUTPUT = ROOT / "results" / "final_red_team_verification.json"
PDF = ROOT / "paper" / "Named_Grid_Covers_under_Row-Column_Margins.pdf"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def add(checks: list[dict], name: str, passed: bool, detail) -> None:
    checks.append({"name": name, "passed": bool(passed), "detail": detail})


def write(payload: dict) -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    write({"schema": "p42.output-t.final-red-team-verification.v1", "status": "IN_PROGRESS"})
    checks: list[dict] = []
    report = REPORT.read_text(encoding="utf-8") if REPORT.is_file() else ""
    rows = re.findall(r"^\| (RT-(?:[1-9]|1[0-5])) \| (pass|not_applicable) \| (low|medium|high|critical) \|", report, flags=re.MULTILINE)
    ids = [row[0] for row in rows]
    add(checks, "rt_1_through_15_complete", ids == [f"RT-{number}" for number in range(1, 16)], {"ids": ids})
    add(checks, "report_closure", all(fragment in report for fragment in [
        "Verdict: **PASS_WITH_REPAIRS**",
        "Known package defects block publication: **no**",
        "Priority or firstness cleared: **no**",
        "Recommended next package: **Maintainer**",
    ]), None)
    unresolved = re.findall(r"^\| F-[^|]+ \| (?:high|critical) \| open \|", report, flags=re.MULTILINE)
    add(checks, "no_open_high_or_critical_finding", not unresolved, unresolved)

    main_receipt_path = ROOT / "results" / "verification.json"
    main_receipt = json.loads(main_receipt_path.read_text(encoding="utf-8")) if main_receipt_path.is_file() else {}
    add(checks, "full_replay_pass", main_receipt.get("status") == "PASS" and main_receipt.get("profile") == "full", {"status": main_receipt.get("status"), "profile": main_receipt.get("profile")})

    manifest_path = ROOT / "certificates" / "MANIFEST.json"
    manifest_sha = sha256(manifest_path) if manifest_path.is_file() else None
    receipt_manifest = main_receipt.get("manifest", {})
    add(checks, "full_receipt_current_manifest", all([
        manifest_sha is not None,
        receipt_manifest.get("pre_replay_sha256") == manifest_sha,
        receipt_manifest.get("post_replay_sha256") == manifest_sha,
        receipt_manifest.get("snapshot_unchanged") is True,
    ]), {"current": manifest_sha, "receipt": receipt_manifest})

    repo_receipt_path = ROOT / "results" / "repository_validation.json"
    repo_receipt = json.loads(repo_receipt_path.read_text(encoding="utf-8")) if repo_receipt_path.is_file() else {}
    add(checks, "repository_policy_pass", repo_receipt.get("status") == "PASS", repo_receipt.get("checks", []))

    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.is_file() else {}
    boundary = manifest.get("boundary", {})
    add(checks, "manifest_owner_boundary", all([
        boundary.get("public_authority") is False,
        boundary.get("remote_or_release_authority") is False,
        boundary.get("priority_or_firstness_clearance") is False,
        boundary.get("external_reproduction") is False,
    ]), boundary)

    machine_report_path = ROOT / "reports" / "P42_T11_RED_TEAM.json"
    machine_report = json.loads(machine_report_path.read_text(encoding="utf-8")) if machine_report_path.is_file() else {}
    machine_tests = machine_report.get("tests", [])
    add(checks, "machine_red_team_report", all([
        machine_report.get("status") == "pass",
        machine_report.get("verdict") == "PASS_WITH_REPAIRS",
        machine_report.get("blocked_publication") is False,
        machine_report.get("promotion_allowed") is False,
        machine_report.get("priority_or_firstness_cleared") is False,
        [row.get("id") for row in machine_tests] == [f"RT-{number}" for number in range(1, 16)],
        all(row.get("status") in {"pass", "not_applicable"} for row in machine_tests),
    ]), {"status": machine_report.get("status"), "verdict": machine_report.get("verdict"), "tests": machine_tests})

    pdf_detail = {"exists": PDF.is_file()}
    pdf_ok = False
    if PDF.is_file():
        reader = PdfReader(PDF)
        text = "\n".join((page.extract_text() or "") for page in reader.pages)
        pdf_detail.update({"pages": len(reader.pages), "bytes": PDF.stat().st_size, "sha256": sha256(PDF)})
        pdf_ok = len(reader.pages) == 18 and "Author manuscript" in text and "Lee Sallows" in text
    add(checks, "accepted_pdf", pdf_ok, pdf_detail)

    sha_check = subprocess.run([sys.executable, "-X", "utf8", "-B", str(ROOT / "scripts" / "check_sha256_manifest.py")], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    add(checks, "portable_source_manifest", sha_check.returncode == 0, {"exit_code": sha_check.returncode, "stdout": sha_check.stdout, "stderr": sha_check.stderr})

    remotes = []
    remote_urls = []
    if (ROOT / ".git").is_dir():
        config = ROOT / ".git" / "config"
        config_text = config.read_text(encoding="utf-8", errors="replace") if config.is_file() else ""
        remotes = re.findall(r'(?im)^\s*\[remote\s+"([^"]+)"\]\s*$', config_text)
        remote_urls = re.findall(r"(?im)^\s*url\s*=\s*(\S+)\s*$", config_text)
    canonical_urls = {
        "https://github.com/aconsciousfractal/FCIG-Named-Grid-Covers-under-Row-Column-Margins",
        "https://github.com/aconsciousfractal/FCIG-Named-Grid-Covers-under-Row-Column-Margins.git",
        "git@github.com:aconsciousfractal/FCIG-Named-Grid-Covers-under-Row-Column-Margins.git",
        "ssh://git@github.com/aconsciousfractal/FCIG-Named-Grid-Covers-under-Row-Column-Margins.git",
    }
    remote_ok = (not remotes and not remote_urls) or (
        remotes == ["origin"] and len(remote_urls) == 1 and remote_urls[0] in canonical_urls
    )
    add(
        checks,
        "git_remote_absent_or_canonical",
        remote_ok,
        {"names": remotes, "urls": remote_urls},
    )

    status = "PASS" if all(check["passed"] for check in checks) else "FAIL"
    payload = {
        "checks": checks,
        "manifest_sha256": sha256(manifest_path) if manifest_path.is_file() else None,
        "pdf_sha256": sha256(PDF) if PDF.is_file() else None,
        "public_authority": False,
        "report_sha256": sha256(REPORT) if REPORT.is_file() else None,
        "schema": "p42.output-t.final-red-team-verification.v1",
        "status": status,
    }
    write(payload)
    print(f"{status}: {sum(check['passed'] for check in checks)}/{len(checks)} checks")
    print(f"receipt: {OUTPUT}")
    print(f"receipt_sha256: {sha256(OUTPUT)}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
