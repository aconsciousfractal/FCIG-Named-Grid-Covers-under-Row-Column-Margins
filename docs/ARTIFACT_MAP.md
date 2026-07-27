# Artifact map

## Paper and proof

| Layer | Canonical artifact | Verification |
| --- | --- | --- |
| Manuscript source | `paper/main.tex`, `paper/macros.tex`, `paper/references.tex`, `paper/sections/*.tex` | `scripts/verify_tomographic_manuscript.py` |
| Built paper | `paper/Named_Grid_Covers_under_Row-Column_Margins.pdf` | PDF text/page check plus rendered visual QA |
| Theorem reconstruction | `docs/PROOF_RECONSTRUCTION.md` | claim curator and final red team |
| Theorem roles | `docs/THEOREM_SPINE.md`, `docs/THEOREM_ROLE_MATRIX.md` | repository policy validator |
| Prior-art boundary | `docs/THEOREM_LEVEL_PRIOR_ART_AUDIT.md` | RT-4, RT-10, RT-15 |

## Finite libraries

| Claim layer | Locked input and code | Certificate/report |
| --- | --- | --- |
| C32 | `registry/c32_source_lock.json`; `packages/package_b_c32_durer_realization/realization/` | `R_certificates.json`; `results/c32_structural_analysis.json` |
| C46 | `registry/c46_source_lock.json`; `packages/package_a_c46_reproduction/realization/` | `R_certificates.json`; `reports/P42_C46_SOURCE_AUDIT.md` |
| P49 | `packages/package_c_comparative_hypergraphs/specimens/p49_locked.json` | `results/coarea_fpt_analysis.json` |
| Residual-area theorem panel | `packages/package_e_obstruction_channels/xray_channel/coarea_fpt.py` | `reports/P42_COAREA_NEXT_VERIFICATION.json` |

## P21

| Claim layer | Canonical artifacts |
| --- | --- |
| locked configuration | `packages/package_c_comparative_hypergraphs/specimens/p21_locked.json` |
| quotient and support filtration | `reports/P42_ROBUST_P21_QUOTIENT_VERIFICATION.json`, `P42_DEGREE3_AUGMENTATION_VERIFICATION.json`, `P42_SUPPORT4_CEILING_VERIFICATION.json` |
| exact orbit minimum | `reports/P42_MINIMUM_ORBIT_GENERATORS_CERTIFICATE.json` |
| Markov no-go | `reports/P42_MARKOV_NO_GO_CERTIFICATE.json`, `P42_SINGLE_BLOCK_MARKOV_DEGREES.json` |
| independent integrated replay | `packages/package_e_obstruction_channels/xray_channel/verify_orbit_markov_closure.py` |

## Package integrity

- `certificates/MANIFEST.json`: fail-closed reviewer snapshot including the PDF.
- `MANIFEST_SHA256.txt`: portable source/documentation hash list excluding PDF
  and generated top-level receipts.
- `scripts/verify.py`: manifest/core/full replay entry point.
- `scripts/validate_repository.py`: public-package path, wording, license, and
  structure gate.
- `scripts/verify_final_red_team.py`: final RT receipt gate.
- `results/verification.json`: generated main replay receipt.
- `results/final_red_team_verification.json`: generated final red-team receipt.
