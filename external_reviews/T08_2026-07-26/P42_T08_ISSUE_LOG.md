# P42 Output T — T‑08 Issue Log

| ID | Severity | Area | Finding | Evidence | Required closure |
|---|---:|---|---|---|---|
| T08-001 | 1 | Attribution | Lee Sallows and geomagic squares are not named or cited although C32/C46/P49 derive from his gallery specimens. | Zero manuscript hits for `Sallows`, `Lee`, `geomagic`; source locks identify gallery assets. | Add explicit ownership paragraph, Sallows 2011 paper, gallery citation, access date and stable specimen IDs; resolve figure permissions. |
| T08-002 | 1 | Reproducibility | `REPRODUCE.md` says standard-library only; frozen replay scripts import `sympy` and `python-flint`. | Static imports in P21/co-area scripts. | Add locked environment/dependencies, preflight, installation instructions, corrected wording. |
| T08-003 | 1 | Integrity | Manifest and semantic checks run only before replay; no post-run revalidation. | `verify.py`: check → run → write PASS. | Recheck all frozen artifacts/anchors after commands; preferably execute in isolated read-only snapshot. |
| T08-004 | 1 | Claim wording | Title uses unqualified “Tomographic Exactness”, explicitly forbidden by the project claim boundary. | Title versus `CLAIM_BOUNDARY.md`. | Rename title and replace public term `co-area` with residual/complement area. |
| T08-005 | 2 | Parameterized theorem | Implicit-library FPT problem lacks a fully quantified input/parameter/output statement. | T-TYPE prose. | State parameter \(Q\), canonical-largest contract and decision/classification output formally. |
| T08-006 | 2 | Proof | No standalone type-isomorphism lemma proves that equal participation-type vectors yield isomorphic fibers and repair graphs. | T-TYPE proof sketch. | Add lemma retaining cross-largest-pose placement identity and tie eligibility. |
| T08-007 | 2 | Source reproducibility | Package replays locked normalized masks but cannot independently reconstruct from absent copyrighted source rasters. | Source-lock policy. | State this boundary explicitly in README/abstract/reproducibility appendix. |
| T08-008 | 2 | Reviewer checklist | “94-piece carrier” is false; P49 has 16 pieces and 94 area-compatible rows. | `REVIEW_CHECKLIST.md`. | Replace with “94-row carrier over 16 named pieces”. |
| T08-009 | 2 | Filesystem safety | Lexical path check does not stop symlink escape; no transitive import-closure gate. | `verify.py`. | Enforce realpath containment/reject symlinks; run in manifest-only tree or audit imports. |
| T08-010 | 3 | Definitions | Library-wide use of “pure/repair-exact/support-exact” is not formally quantified. | Row-wise definitions; table-level prose. | Define universal library predicate over declared area-compatible rows. |
| T08-011 | 3 | Input model | Orientation group action on \(\mathbb Z^2\) is not formally specified. | Finite-placement definition. | Say orientations are explicit lattice automorphisms or explicit oriented masks. |
| T08-012 | 3 | Receipt provenance | Receipt lacks exact argv, versions, platform, logs/digests and duration. | `verification.json` schema. | Add deterministic provenance receipt plus separate volatile log. |
| T08-013 | 3 | Prior art | Foundational discrete-tomography sources and Tracy Chin’s thesis are absent or unresolved. | Current 15-entry bibliography/audit. | Add Herman–Kuba, Chrobak–Dürr 2001; acquire/read Chin thesis before publication. |

## Gate rule

T‑08 may close only when:

- every severity-1 issue is fixed and replayed;
- every severity-2 mathematical/source issue is fixed or explicitly owner-waived with a written boundary;
- the full profile passes on the accepted post-fix snapshot;
- the post-run hash check proves snapshot identity;
- the public claim set remains unchanged unless separately owner-promoted.
