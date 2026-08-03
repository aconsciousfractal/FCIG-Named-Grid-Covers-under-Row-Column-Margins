#!/usr/bin/env python3
"""Fail-closed structural and public-boundary check for the repository."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "results" / "repository_validation.json"

REQUIRED = [
    "README.md",
    "README_REVIEWER.md",
    "REPRODUCE.md",
    "LICENSE",
    "LICENSE_SCOPE.md",
    "THIRD_PARTY_NOTICES.md",
    "CITATION.cff",
    "requirements.txt",
    "MANIFEST_SHA256.txt",
    "certificates/MANIFEST.json",
    "docs/CLAIM_LEDGER.md",
    "docs/PUBLIC_CLAIM_BOUNDARY.md",
    "docs/SOURCE_LOCK.md",
    "docs/THEOREM_LEVEL_PRIOR_ART_AUDIT.md",
    "docs/VERIFICATION_ARCHITECTURE.md",
    "reports/C32_SOURCE_AUDIT.md",
    "reports/C32_EXACT_CENSUS.md",
    "reports/C46_SOURCE_AUDIT.md",
    "paper/main.tex",
    "paper/Named_Grid_Covers_under_Row-Column_Margins.pdf",
    "scripts/verify.py",
]

TEXT_SUFFIXES = {".md", ".tex", ".py", ".json", ".txt", ".cff", ".yaml", ".yml", ".sign", ".mat"}
DOCUMENT_SUFFIXES = {".md", ".tex", ".txt", ".cff", ".yaml", ".yml"}
VOLATILE_TEXT_OUTPUTS = {"results/verification_run.json"}
FORBIDDEN_GLOBAL = [
    ("drive path", re.compile(r"(?i)(?:^|[\s`'\"])[A-Z]:[\\/]")),
    ("private repository path", re.compile(r"(?i)(?:^|[\s`'\"])(?:HAN|HAN_WORKTREE)[\\/]")),
    ("Unix home path", re.compile(r"(?:^|[\s`'\"])(?:/home/|/Users/)")),
    ("internal output path", re.compile(r"internal_outputs/", re.IGNORECASE)),
]
FORBIDDEN_READER_WORKFLOW = [
    ("release-candidate label", re.compile(r"(?:public[- ]release|release)[- ]candidate", re.IGNORECASE)),
    ("local-public label", re.compile(r"local public", re.IGNORECASE)),
    ("owner workflow", re.compile(r"owner[- ](?:gate|action|authority|authorization|parked)", re.IGNORECASE)),
    ("internal manuscript", re.compile(r"internal manuscript", re.IGNORECASE)),
    ("review workflow", re.compile(r"red[- ]team", re.IGNORECASE)),
    ("private stage id", re.compile(r"\b(?:P42|Output T|T-0[2-9]|T-1[01])\b", re.IGNORECASE)),
    ("orchestration vocabulary", re.compile(r"\b(?:agent|handoff|PAPP|HAN)\b", re.IGNORECASE)),
    ("private history", re.compile(r"external_reviews/|closeout receipt|next gate", re.IGNORECASE)),
]


def record(rows: list[dict], name: str, passed: bool, detail) -> None:
    rows.append({"name": name, "passed": bool(passed), "detail": detail})


def public_text_files() -> list[Path]:
    return [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.suffix.lower() in TEXT_SUFFIXES
        and ".git" not in path.parts
        and ".venv" not in path.parts
        and path.relative_to(ROOT).as_posix() not in VOLATILE_TEXT_OUTPUTS
    ]


def main() -> int:
    checks: list[dict] = []
    missing = [rel for rel in REQUIRED if not (ROOT / rel).is_file()]
    record(checks, "required_public_files", not missing, {"missing": missing})

    path_hits = []
    workflow_hits = []
    broken_refs = []
    root_real = ROOT.resolve()
    for path in public_text_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(ROOT).as_posix()
        for label, pattern in FORBIDDEN_GLOBAL:
            if rel != "scripts/validate_repository.py" and pattern.search(text):
                path_hits.append({"file": rel, "kind": label})
        if path.suffix.lower() in DOCUMENT_SUFFIXES:
            for label, pattern in FORBIDDEN_READER_WORKFLOW:
                if pattern.search(text):
                    workflow_hits.append({"file": rel, "kind": label})
            for raw_ref in re.findall(r"\]\(([^)]+)\)", text):
                ref = raw_ref.split("#", 1)[0].strip().strip("<>")
                if not ref or re.match(r"^(?:https?://|mailto:)", ref, re.IGNORECASE):
                    continue
                resolved = (path.parent / ref).resolve()
                contained = resolved == root_real or root_real in resolved.parents
                if not contained or not resolved.exists():
                    broken_refs.append({"file": rel, "reference": raw_ref})
    record(checks, "no_private_or_absolute_paths", not path_hits, path_hits)
    record(checks, "no_internal_workflow_language_in_reader_docs", not workflow_hits, workflow_hits)
    record(checks, "all_local_markdown_links_resolve", not broken_refs, broken_refs)

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    boundary = (ROOT / "docs/PUBLIC_CLAIM_BOUNDARY.md").read_text(encoding="utf-8")
    claims = (ROOT / "docs/CLAIM_LEDGER.md").read_text(encoding="utf-8")
    paper = (ROOT / "paper/main.tex").read_text(encoding="utf-8")
    current_public = "\n".join((readme, boundary, claims, paper))
    required_phrases = [
        "largest-piece residual area",
        "no priority or firstness claim",
        "exact P21 Markov degree",
        "Public preprint, version 1.0.0",
        "Lee Sallows",
    ]
    phrase_map = {phrase: phrase.lower() in current_public.lower() for phrase in required_phrases}
    record(checks, "public_claim_boundary_anchors", all(phrase_map.values()), phrase_map)

    forbidden_claims = [
        "we give the first FPT algorithm for tomography",
        "the exact P21 Markov degree is seven",
        "we provide a complete P21 Markov basis",
        "independently externally reproduced",
        "Author manuscript",
        "date-released:",
    ]
    forbidden_hits = [phrase for phrase in forbidden_claims if phrase.lower() in current_public.lower()]
    record(checks, "forbidden_public_claims_absent", not forbidden_hits, forbidden_hits)

    cited_paths = [
        "registry/c32_source_lock.json",
        "registry/c46_source_lock.json",
        "reports/C32_SOURCE_AUDIT.md",
        "reports/C32_EXACT_CENSUS.md",
        "reports/C46_SOURCE_AUDIT.md",
        "docs/FOUNDATIONAL_SECTION.md",
        "docs/P21_CASE_STUDY.md",
        "docs/CLAIM_LEDGER.md",
    ]
    cited_missing = [rel for rel in cited_paths if not (ROOT / rel).is_file()]
    record(checks, "paper_evidence_paths_resolve", not cited_missing, cited_missing)

    manifest = json.loads((ROOT / "certificates/MANIFEST.json").read_text(encoding="utf-8"))
    manifest_ok = all([
        manifest.get("schema") == "fcig.named-grid-covers.public-manifest.v1",
        manifest.get("status") == "PUBLIC_RELEASE_V1_0_0",
        manifest.get("boundary", {}).get("priority_or_firstness_claimed") is False,
        manifest.get("boundary", {}).get("source_raster_bytes_redistributed") is False,
        manifest.get("boundary", {}).get("p21_exact_markov_basis") == "open_out_of_scope",
    ])
    record(checks, "public_manifest_boundary", manifest_ok, manifest.get("boundary"))

    remotes = []
    remote_urls = []
    if (ROOT / ".git").is_dir():
        config = ROOT / ".git/config"
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
    record(checks, "git_remote_absent_or_canonical", remote_ok, {"names": remotes, "urls": remote_urls})

    status = "PASS" if all(row["passed"] for row in checks) else "FAIL"
    payload = {
        "checks": checks,
        "schema": "fcig.named-grid-covers.repository-validation.v1",
        "status": status,
    }
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(f"{status}: {sum(row['passed'] for row in checks)}/{len(checks)} checks")
    print(f"receipt: {RESULT}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
