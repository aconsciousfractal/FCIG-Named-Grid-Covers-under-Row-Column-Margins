# Artifact map

## Paper and proof

| Layer | Canonical artifact | Verification |
| --- | --- | --- |
| Manuscript source | `paper/main.tex`, `paper/macros.tex`, `paper/references.tex`, `paper/sections/*.tex` | `scripts/verify_tomographic_manuscript.py` |
| Built paper | `paper/Named_Grid_Covers_under_Row-Column_Margins.pdf` | text/page checks plus rendered visual QA |
| Proof reconstruction | `docs/PROOF_RECONSTRUCTION.md` | manuscript and repository validators |
| Theorem roles | `docs/THEOREM_SPINE.md`, `docs/THEOREM_ROLE_MATRIX.md` | repository validator |
| Prior-art boundary | `docs/THEOREM_LEVEL_PRIOR_ART_AUDIT.md` | source and scope checks |

## Finite libraries

| Layer | Locked input and code | Public report or result |
| --- | --- | --- |
| C32 | `registry/c32_source_lock.json`; `packages/package_b_c32_durer_realization/realization/` | `reports/C32_SOURCE_AUDIT.md`; `reports/C32_EXACT_CENSUS.md`; `results/c32_structural_analysis.json` |
| C46 | `registry/c46_source_lock.json`; `packages/package_a_c46_reproduction/realization/` | `reports/C46_SOURCE_AUDIT.md`; `R_certificates.json` |
| P49 | `packages/package_c_comparative_hypergraphs/specimens/p49_locked.json` | `results/coarea_fpt_analysis.json` |
| Residual-area panel | `packages/package_e_obstruction_channels/xray_channel/coarea_fpt.py` | `results/coarea_fpt_analysis.json` |

## P21

The public case-study map is `docs/P21_CASE_STUDY.md`. The underlying JSON
certificates retain stable legacy filenames because scripts and frozen hashes
refer to them. They are machine artifact identifiers, not public claim labels.

## Package integrity

- `certificates/MANIFEST.json`: fail-closed release snapshot including the PDF.
- `MANIFEST_SHA256.txt`: portable source and documentation hashes.
- `SHA256SUMS`: complete allowlisted release-payload checksums.
- `scripts/verify.py`: manifest, core, and full replay entry point.
- `scripts/validate_repository.py`: public-package path, wording, license, and
  structure validation.
- `results/verification.json`: generated replay receipt.
- `docs/VERIFICATION_ARCHITECTURE.md`: verification design and trust boundary.
