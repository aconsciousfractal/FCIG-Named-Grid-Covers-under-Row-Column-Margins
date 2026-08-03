#!/usr/bin/env python3
"""Fail-closed static and PDF verifier for the public manuscript."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

from pypdf import PdfReader


PROJECT = Path(__file__).resolve().parents[1]
PAPER = PROJECT / "paper"
PDF = PAPER / "Named_Grid_Covers_under_Row-Column_Margins.pdf"
RESULT = PROJECT / "results" / "manuscript_verification.json"

ORDERED_INPUTS = [
    "sections/01_introduction",
    "sections/02_model",
    "sections/03_exactness",
    "sections/04_finite_libraries",
    "sections/05_localization",
    "sections/06_fpt",
    "sections/07_types_energy",
    "sections/08_p21",
    "sections/09_limits",
    "sections/10_evidence",
    "sections/11_reproducibility",
]

REQUIRED_FILES = [
    "main.tex",
    "macros.tex",
    "references.tex",
    "BUILD.md",
    *(f"{name}.tex" for name in ORDERED_INPUTS),
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def add_check(
    checks: list[dict[str, object]],
    name: str,
    passed: bool,
    detail: object,
) -> None:
    checks.append({"name": name, "passed": bool(passed), "detail": detail})


def strip_comments(text: str) -> str:
    return "\n".join(
        re.sub(r"(?<!\\)%.*$", "", line) for line in text.splitlines()
    )


def balanced_environments(text: str) -> tuple[bool, str]:
    stack: list[str] = []
    for token in re.finditer(r"\\(begin|end)\{([^}]+)\}", text):
        kind, environment = token.groups()
        if kind == "begin":
            stack.append(environment)
        elif not stack or stack.pop() != environment:
            return False, f"mismatch at {token.group(0)}"
    if stack:
        return False, f"unclosed environments: {stack}"
    return True, "balanced"


def main() -> int:
    checks: list[dict[str, object]] = []
    missing = [name for name in REQUIRED_FILES if not (PAPER / name).is_file()]
    add_check(checks, "required_source_files", not missing, {"missing": missing})

    if missing:
        payload = {
            "schema": "fcig.named-grid-covers.public-manuscript-verification.v1",
            "status": "FAIL",
            "checks": checks,
            "files": {},
        }
        RESULT.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return 1

    file_text = {
        name: (PAPER / name).read_text(encoding="utf-8")
        for name in REQUIRED_FILES
        if name.endswith(".tex")
    }
    combined = "\n".join(file_text.values())
    uncommented = strip_comments(combined)

    main_inputs = re.findall(r"\\input\{([^}]+)\}", file_text["main.tex"])
    section_inputs = [name for name in main_inputs if name.startswith("sections/")]
    add_check(
        checks,
        "frozen_section_order",
        section_inputs == ORDERED_INPUTS,
        {"observed": section_inputs, "expected": ORDERED_INPUTS},
    )

    labels = re.findall(r"\\label\{([^}]+)\}", uncommented)
    duplicate_labels = sorted({label for label in labels if labels.count(label) > 1})
    references = {
        item.strip()
        for body in re.findall(
            r"\\(?:[Cc]ref|ref|pageref)\{([^}]+)\}", uncommented
        )
        for item in body.split(",")
    }
    undefined_references = sorted(references - set(labels))
    add_check(
        checks,
        "cross_references",
        not duplicate_labels and not undefined_references,
        {
            "label_count": len(labels),
            "duplicate_labels": duplicate_labels,
            "undefined_references": undefined_references,
        },
    )

    bibitems = set(re.findall(r"\\bibitem\{([^}]+)\}", uncommented))
    citations = {
        item.strip()
        for body in re.findall(r"\\cite\{([^}]+)\}", uncommented)
        for item in body.split(",")
    }
    undefined_citations = sorted(citations - bibitems)
    add_check(
        checks,
        "bibliography_links",
        not undefined_citations,
        {
            "citation_count": len(citations),
            "bibitem_count": len(bibitems),
            "undefined_citations": undefined_citations,
        },
    )

    structure: dict[str, dict[str, object]] = {}
    structure_ok = True
    for name, raw_text in file_text.items():
        text = strip_comments(raw_text)
        opens = len(re.findall(r"(?<!\\)\{", text))
        closes = len(re.findall(r"(?<!\\)\}", text))
        env_ok, env_detail = balanced_environments(text)
        file_ok = opens == closes and env_ok
        structure_ok = structure_ok and file_ok
        structure[name] = {
            "open_braces": opens,
            "close_braces": closes,
            "environments": env_detail,
            "passed": file_ok,
        }
    add_check(checks, "static_latex_structure", structure_ok, structure)

    required_fragments = {
        "public_preprint": "Public preprint, version 1.0.0",
        "exact_two_graph": r"\GG_E^{(2)}",
        "translation_empty_branch": r"\max(0,|B|-|A|+1)",
        "active_carrier": "at most \\(q^2\\) target cells",
        "fpt_bound": r"h(q+1)(h q^2)^q",
        "full_parameter_dependence": r"2^{O(q\log(qh))}",
        "candidate_pose_boundary": "margin-compatible candidate poses",
        "sallows_attribution": "created and published by Lee Sallows",
        "source_reconstruction_boundary": "does not independently reproduce image",
        "type_isomorphism": "Type-isomorphism lemma",
        "implicit_parameter": r"|T|-|L(E)|\leq Q",
        "no_priority_claim": "No priority or ``first FPT'' claim is made",
        "c32_panel": r"\(136=136+0\)",
        "c46_panel": r"\(352=344+8\)",
        "p49_singletons": "eight separate singleton components",
        "p21_matrix": r"\(14\times72\)",
        "p21_kernel_rank": "has rank 60",
        "fixed_fiber_rank_gap": r"lattice rank \(54<60=\rank K\)",
        "integral_generation": r"M_{\leq4}=K",
        "missing_quadrics": "74 within-block",
        "degree_lower_bound": "at least} seven",
        "degree_upper_boundary": "No upper",
        "public_boundary": "makes no novelty,\nfirstness, or priority claim",
    }
    fragment_results = {
        name: fragment in combined for name, fragment in required_fragments.items()
    }
    add_check(
        checks,
        "load_bearing_fragments",
        all(fragment_results.values()),
        fragment_results,
    )

    forbidden_unqualified = [
        "first FPT algorithm",
        "Markov degree equals seven",
        "one trapped component of eight nodes",
        "Tomographic Exactness and Co-Area Localization",
    ]
    forbidden_hits = [
        phrase for phrase in forbidden_unqualified if phrase in uncommented
    ]
    add_check(
        checks,
        "forbidden_claim_phrases",
        not forbidden_hits,
        {"hits": forbidden_hits},
    )

    pdf_detail: dict[str, object] = {"exists": PDF.is_file()}
    pdf_ok = False
    if PDF.is_file():
        try:
            reader = PdfReader(PDF)
            page_count = len(reader.pages)
            extracted = "\n".join((page.extract_text() or "") for page in reader.pages)
            required_pdf_text = [
                "Named Grid Covers under Row",
                "Three Exactness Levels and Largest-Piece Localization",
                "Public preprint, version 1.0.0",
                "Largest-piece residual-area FPT theorem",
                "Lee Sallows",
                "Type-isomorphism lemma",
                "P21: three non-equivalent connectivity questions",
                "References",
            ]
            text_hits = {item: item in extracted for item in required_pdf_text}
            pdf_ok = page_count == 18 and all(text_hits.values())
            pdf_detail.update(
                {
                    "pages": page_count,
                    "bytes": PDF.stat().st_size,
                    "sha256": sha256(PDF),
                    "required_text": text_hits,
                }
            )
        except Exception as exc:  # fail closed
            pdf_detail["error"] = repr(exc)
    add_check(checks, "built_pdf", pdf_ok, pdf_detail)

    files = {name: sha256(PAPER / name) for name in REQUIRED_FILES}
    if PDF.is_file():
        files[str(PDF.relative_to(PAPER))] = sha256(PDF)

    status = "PASS" if all(bool(check["passed"]) for check in checks) else "FAIL"
    payload = {
        "schema": "fcig.named-grid-covers.public-manuscript-verification.v1",
        "status": status,
        "checks": checks,
        "files": files,
    }
    RESULT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"{status}: {sum(bool(c['passed']) for c in checks)}/{len(checks)} checks")
    print(f"receipt: {RESULT}")
    print(f"receipt_sha256: {sha256(RESULT)}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
