# P42 T-08 external red-team adjudication

Date: 2026-07-27  
External review date: 2026-07-26  
Current gate state: **PASS_INTERNAL_REVIEW**  
Public claim set: unchanged; C46 remains the sole public P42 claim.

## Verdict on the external package

The package is authentic and internally consistent: all six declared payload
hashes in `SHA256SUMS` were recomputed and passed. The external `FIX_FIRST`
verdict is correct in substance. The mathematical spine survives; the
blocking defects were attribution, wording, and reviewer-package integrity,
not counterexamples to the active-carrier or FPT theorem.

The source bundle is preserved byte-for-byte under
`external_reviews/T08_2026-07-26/` with its own `SOURCE_LOCK.json`.

## Independent mathematical verification

- The translation cap, active-carrier lemma, FPT fiber bound, radius bound,
  and overlap-energy identity remain valid under the declared finite-cell-list
  model.
- C32, C46, and P49 retain their frozen aggregate counts and distinct logical
  roles. The checklist's “94-piece carrier” was indeed false: P49 has 16 named
  pieces and 94 area-compatible rows.
- P21 remains a bounded 14x72 configuration. The rank-51/rank-54/rank-60
  distinctions, minimum three-orbit families, 74 missing quadrics, and Markov
  degree lower bound seven are unchanged.
- T-TYPE had a formalization gap but no counterexample. The manuscript now
  states the input threshold `Q`, canonical-largest eligibility, exact
  cross-pose mask identity, availability multiplicities, and a standalone
  type-isomorphism lemma.

## Independent source verification

Direct primary or institutional records confirm:

- Lee Sallows, “Geometric Magic Squares”, *The Mathematical Intelligencer* 33
  (2011), 25-31, DOI `10.1007/s00283-011-9229-0`;
- Sallows' official geomagic gallery and authorship of the underlying
  specimens;
- Peter Cameron's 21 January 2011 finite group-action formulation;
- Herman-Kuba, *Discrete Tomography* (1999), DOI
  `10.1007/978-1-4612-1568-4`;
- Chrobak-Durr (2001), polyatomic reconstruction from discrete X-rays, DOI
  `10.1016/S0304-3975(99)00325-4`;
- Chrobak et al., “Tile-Packing Tomography Is NP-hard”, *Algorithmica* 64
  (2012), DOI `10.1007/s00453-011-9498-1`;
- full Fellows et al. ECAI 2023 metadata, DOI `10.3233/FAIA230334`;
- Tracy Chin's author page and direct Brown institutional record
  `bdr:919199` for *A Computational Commutative Algebra Approach to Tilings*.

The Chin repository record is direct, but the thesis interior has not been
used to authorize a priority claim. A full interior comparison remains a
publication-stage source task, not a blocker for internal T-08 because the
manuscript makes no firstness claim.

## Issue disposition

| Issue | Severity | Disposition | Concrete closure evidence |
| --- | ---: | --- | --- |
| T08-001 | 1 | closed | manuscript explicitly credits Sallows; Sallows 2011, official gallery, and Cameron are cited; source/P42 ownership boundary stated |
| T08-002 | 1 | closed | `requirements-review.txt`, `environment-review.json`, exact-version preflight for CPython, pypdf, sympy, python-flint |
| T08-003 | 1 | closed | manifest, semantic anchors, and complete frozen snapshot checked before and after replay; byte change fails |
| T08-004 | 1 | closed | title changed to *Named Grid Covers under Row-Column Margins: Three Exactness Levels and Largest-Piece Localization*; prose uses “largest-piece residual area” |
| T08-005 | 2 | closed | implicit input and parameter threshold `Q` stated formally |
| T08-006 | 2 | closed | exact participation type plus type-isomorphism lemma and multiplicity formula added |
| T08-007 | 2 | closed | raster acquisition/transcription explicitly separated from normalized-mask replay |
| T08-008 | 2 | closed | checklist corrected to 94 rows over 16 names |
| T08-009 | 2 | closed | resolved-path containment, symlink rejection, static transitive import and literal child-script closure |
| T08-010 | 3 | closed | library predicates quantified over a declared selection domain |
| T08-011 | 3 | closed | finite orientation action specified as explicit lattice automorphisms; duplicate masks identified |
| T08-012 | 3 | closed | stable receipt records normalized argv, exit code, environment, and output digests; volatile log records raw argv, duration, timestamps, stdout/stderr |
| T08-013 | 3 | closed for internal gate; publication follow-up | foundational references added and Chin institutional record acquired; no priority clearance granted |

## What changes in the project plan

1. Output T remains the P42 paper. The core theorem and finite/P21 numbers do
   not change.
2. The public-facing mathematical vocabulary changes from “co-area” to
   “largest-piece residual area”. Legacy `coarea_*` filenames remain stable
   artifact identifiers only.
3. Sallows attribution is now load-bearing, not optional editorial polish.
4. T-TYPE is retained because it now has a complete problem contract and
   isomorphism proof; it remains supporting material, not the headline.
5. Reviewer-package closure is stronger: exact dependencies, import closure,
   resolved path safety, command provenance, and post-replay snapshot
   invariance are required.
6. T-08 is `PASS_INTERNAL_REVIEW`: the rebuilt 103-artifact manifest and
   hardened `full` profile pass on the same unchanged snapshot, and all 18
   pages of the accepted PDF have been freshly rendered and inspected.
7. None of this authorizes a public repository, submission, C32 promotion, or
   priority claim. Those remain separate owner/publication gates.