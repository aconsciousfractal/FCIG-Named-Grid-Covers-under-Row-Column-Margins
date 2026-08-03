# Reviewer quickstart

This is a theory paper with a self-contained exact finite replay layer. The
package records author replay, not independent external reproduction.

## Ten-minute path

1. Read `paper/Named_Grid_Covers_under_Row-Column_Margins.pdf`.
2. Read `docs/CLAIM_LEDGER.md` and `docs/PUBLIC_CLAIM_BOUNDARY.md`.
3. Read the theorem roles in `docs/THEOREM_ROLE_MATRIX.md`.
4. Read `docs/VERIFICATION_ARCHITECTURE.md`.

The uniform headline is the largest-piece active-carrier/FPT theorem. The
three finite libraries are certified witnesses, and P21 is a bounded case
study, not a complete Markov-basis result.

## Thirty-minute path

Use CPython 3.12, 3.13, or 3.14 and the exact dependencies in
`requirements.txt`, then run from the repository root:

```bash
python -X utf8 -B scripts/verify.py --profile manifest
python -X utf8 -B scripts/verify.py --profile core
```

A successful core replay ends:

```text
PASS public release v1.0.0 (core)
```

Inspect `results/verification.json`, `results/manuscript_verification.json`,
and `certificates/MANIFEST.json`. The first is generated; the latter two are
manifest-bound.

## Full replay

```bash
python -X utf8 -B scripts/verify.py --profile full
```

The full profile adds all mutation suites and the complete degree-four and
single-block P21 audits. It is materially slower.

## Known limits

- No novelty or firstness is claimed.
- The replay starts from source-locked normalized masks; it does not reproduce
  image acquisition, segmentation, or transcription from Sallows' raster art.
- The exact P21 Markov degree and complete basis remain open.
- Literal enumeration of all named outputs is output-sensitive.
- This package records author replay, not independent external reproduction.
- A repository release is not a DOI, arXiv deposit, journal submission, or
  evidence of priority.
