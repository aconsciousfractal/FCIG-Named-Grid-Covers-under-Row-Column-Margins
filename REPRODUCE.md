# Reproducing the paper and finite controls

Run commands from the repository root.

## Exact environment

- CPython 3.12, 3.13, or 3.14
- `pypdf==6.14.2`
- `sympy==1.14.0`
- `python-flint==0.9.0`

Install into an isolated environment with the same interpreter used for the
replay:

```bash
python -m pip install -r requirements.txt
```

No network or external dataset is required after dependency installation.
The supported interpreter interval and the recorded release environment are
explicit in `certificates/environment.json`.

## Verification profiles

```bash
python -X utf8 -B scripts/verify.py --profile manifest
python -X utf8 -B scripts/verify.py --profile core
python -X utf8 -B scripts/verify.py --profile full
```

- `manifest` checks environment, resolved-path containment, symlinks, hashes,
  sizes, import/subprocess closure, semantic anchors, and repository policy.
- `core` additionally runs the manuscript verifier, C32/C46 certificates and
  structural checks, the P21/P26/P49 source-lock validator, both residual-area
  producers, a P21 integrated smoke replay, the repository validator, and the
  complete release-checksum audit.
- `full` adds the C32/C46/residual-area mutation suites, the complete P21
  degree-four plus single-block audit, and a nested full replay from a temporary
  tree containing only the manifest allowlist.

Every profile snapshots all frozen artifacts before execution and requires
byte identity afterward. The stable receipt is `results/verification.json`;
timestamps, durations, raw commands, stdout, and stderr are separated into
the ignored file `results/verification_run.json`.

## Build the paper

The manuscript uses an inline bibliography, so no BibTeX/Biber pass is needed.
The canonical PDF was built with Tectonic 0.16.9. From `paper/`, run:

```bash
tectonic main.tex --outdir . --reruns 2
```

Rename `main.pdf` to `Named_Grid_Covers_under_Row-Column_Margins.pdf`.
The canonical output is
`paper/Named_Grid_Covers_under_Row-Column_Margins.pdf`. Its digest, page count,
and build environment are recorded in `certificates/build_environment.json`.
PDF bytes are manifest-bound; the LaTeX source remains the portable object.

## Check the manifests

```bash
python -X utf8 -B scripts/check_sha256_manifest.py
python -X utf8 -B scripts/check_release_checksums.py
```

`MANIFEST_SHA256.txt` excludes `.git/`, TeX auxiliaries, the compiled PDF, and
generated top-level verification receipts. `SHA256SUMS` covers the complete
allowlisted release payload, including the PDF, frozen results,
`certificates/MANIFEST.json`, and `MANIFEST_SHA256.txt`; it excludes only
itself and volatile replay receipts.

## What is imported

The surrounding tomography, reconstruction, reconfiguration, and algebraic
statistics results are imported by citation and are not recomputed. Their role
and hypotheses are recorded in `docs/SOURCE_LOCK.md` and
`docs/THEOREM_LEVEL_PRIOR_ART_AUDIT.md`. No priority inference is made from a
negative literature search.
