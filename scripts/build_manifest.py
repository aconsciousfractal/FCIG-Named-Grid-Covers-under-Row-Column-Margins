#!/usr/bin/env python3
"""Build the standalone Output T reviewer and portable SHA-256 manifests."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JSON_MANIFEST = ROOT / "certificates" / "MANIFEST.json"
SHA_MANIFEST = ROOT / "MANIFEST_SHA256.txt"

GENERATED = {
    "certificates/MANIFEST.json",
    "MANIFEST_SHA256.txt",
    "results/verification.json",
    "results/verification_run.json",
    "results/repository_validation.json",
    "results/final_red_team_verification.json",
    "SHA256SUMS",
}
TEX_SUFFIXES = {".aux", ".log", ".out", ".toc", ".bbl", ".blg", ".fls", ".fdb_latexmk", ".synctex.gz"}
ACCEPTED_BUILD_LOG = "paper/Named_Grid_Covers_under_Row-Column_Margins.log"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def excluded(path: Path) -> bool:
    rel = relative(path)
    parts = rel.split("/")
    if rel in GENERATED or ".git" in parts or ".venv" in parts or "__pycache__" in parts:
        return True
    if any(part == "render" or part.startswith("render_") for part in parts) or "tmp" in parts:
        return True
    if (path.suffix in TEX_SUFFIXES or path.name.endswith(".synctex.gz")) and rel != ACCEPTED_BUILD_LOG:
        return True
    return False


def category(rel: str) -> str:
    if rel.startswith("paper/"):
        return "manuscript"
    if rel.startswith("registry/"):
        return "source_lock"
    if rel.startswith("external_reviews/"):
        return "sources"
    if rel.startswith("packages/"):
        return "replay_code" if rel.endswith(".py") else "certificate"
    if rel.startswith("scripts/"):
        return "verification"
    if rel.startswith("reports/") or rel.startswith("results/"):
        return "certificate"
    if rel.startswith("certificates/") or rel == "requirements.txt":
        return "environment"
    if rel in {"README_REVIEWER.md", "REPRODUCE.md"} or rel.endswith("REVIEW_CHECKLIST.md"):
        return "reviewer"
    if rel.startswith("docs/") and any(token in rel for token in ("SOURCE", "PRIOR_ART")):
        return "sources"
    if rel.startswith("docs/") and any(token in rel for token in ("THEOREM", "PROOF", "FOUNDATIONAL", "P21_CASE")):
        return "theorem"
    return "governance"


def role(rel: str) -> str:
    if rel == "paper/Named_Grid_Covers_under_Row-Column_Margins.pdf":
        return "accepted title-named release-candidate PDF"
    if rel == "scripts/verify.py":
        return "single manifest/core/full verification entry point"
    if rel == "docs/CLAIM_LEDGER.md":
        return "authoritative release-candidate claim ledger"
    if rel == "docs/PUBLIC_CLAIM_BOUNDARY.md":
        return "public wording and owner-action boundary"
    if rel == "docs/RED_TEAM_REPORT.md":
        return "final repository red-team report"
    return "standalone Output T package artifact"


def files() -> list[Path]:
    return sorted(
        (path for path in ROOT.rglob("*") if path.is_file() and not excluded(path)),
        key=lambda path: relative(path),
    )


def main() -> int:
    artifact_rows = []
    for path in files():
        rel = relative(path)
        artifact_rows.append(
            {
                "bytes": path.stat().st_size,
                "category": category(rel),
                "path": rel,
                "role": role(rel),
                "sha256": sha256(path),
            }
        )

    manifest = {
        "artifacts": artifact_rows,
        "boundary": {
            "external_reproduction": False,
            "p21_exact_markov_basis": "open_owner_parked",
            "priority_or_firstness_clearance": False,
            "public_authority": False,
            "remote_or_release_authority": False,
            "source_raster_bytes_redistributed": False,
        },
        "parameter_name": "largest-piece residual area",
        "profiles": {
            "manifest": [],
            "core": [
                "manuscript",
                "c32_certificate",
                "c32_analysis",
                "c46_certificate",
                "coarea",
                "specimens",
                "coarea_next",
                "p21_smoke",
                "repository",
                "release_checksums",
            ],
            "full": [
                "manuscript",
                "c32_certificate",
                "c32_analysis",
                "c46_certificate",
                "coarea",
                "specimens",
                "coarea_next",
                "c32_mutation",
                "c46_mutation",
                "coarea_mutation",
                "p21_full",
                "repository",
                "release_checksums",
                "manifest_only_tree",
            ],
        },
        "project_id": "P42-T",
        "project_root_contract": ".",
        "schema": "p42.output-t.public-candidate-manifest.v1",
        "status": "LOCAL_PUBLIC_RELEASE_CANDIDATE",
        "title": "Named Grid Covers under Row--Column Margins: Three Exactness Levels and Largest-Piece Localization",
    }
    JSON_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    JSON_MANIFEST.write_text(
        json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    portable = []
    for row in artifact_rows:
        rel = row["path"]
        if rel.endswith(".pdf") or rel.startswith("results/"):
            continue
        portable.append(f"{row['sha256'].upper()}  {rel}")
    SHA_MANIFEST.write_text(
        "# Portable source/documentation manifest; PDF and generated/frozen results excluded.\n"
        + "\n".join(portable)
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"WROTE {JSON_MANIFEST.relative_to(ROOT)}: {len(artifact_rows)} artifacts")
    print(f"JSON_SHA256 {sha256(JSON_MANIFEST)}")
    print(f"WROTE {SHA_MANIFEST.name}: {len(portable)} source rows")
    print(f"SHA_MANIFEST_SHA256 {sha256(SHA_MANIFEST)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
