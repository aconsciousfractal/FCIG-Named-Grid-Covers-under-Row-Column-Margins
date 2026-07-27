# Final repository red-team report

Date: 2026-07-27  
Repository: `FCIG-Named-Grid-Covers-under-Row-Column-Margins`  
Gate: T-11  
Verdict: **PASS_WITH_REPAIRS**  
Known package defects block publication: **no**  
Priority or firstness cleared: **no**  
Recommended next package: **Maintainer**

**Post-publication record (2026-07-27).** The owner subsequently published the
canonical GitHub repository. This report retains its pre-publication scope and
verdict as provenance; the publication action does not imply a tag, GitHub
Release, DOI, arXiv deposit, journal submission, priority clearance, or
independent external reproduction.

This is a red-team verdict on a local release-candidate repository, not an
authorization to publish, push, tag, mint a DOI, or submit the manuscript. The
owner retains every external-action decision.

## Scope and success criteria

The target was the complete standalone Output T repository: manuscript source
and accepted PDF, source locks, theorem and claim governance, frozen exact
certificates, replay code, reviewer entry points, licensing, and local Git
state. Success required a coherent no-firstness manuscript, exact finite
claims matching their replay, a portable clean-room route, no unresolved high
or critical package defect, and a fail-closed final receipt.

Non-goals were an exhaustive novelty search, independent reacquisition of Lee
Sallows' raster sources, external reproduction on a second machine, closure of
the exact P21 Markov degree, and any publication action.

## Declared input entity list

Manual semantic review covered:

- `README.md`, `README_REVIEWER.md`, `REPRODUCE.md`, `CITATION.cff`,
  `LICENSE`, `LICENSE_SCOPE.md`, and `THIRD_PARTY_NOTICES.md`;
- `docs/CLAIM_LEDGER.md`, `docs/PUBLIC_CLAIM_BOUNDARY.md`,
  `docs/THEOREM_SPINE.md`, `docs/THEOREM_ROLE_MATRIX.md`,
  `docs/THEOREM_LEVEL_PRIOR_ART_AUDIT.md`, `docs/PRIOR_ART_TOMOGRAPHY.md`,
  `docs/SOURCE_LOCK.md`, `docs/PROOF_RECONSTRUCTION.md`,
  `docs/FOUNDATIONAL_SECTION.md`, `docs/P21_CASE_STUDY.md`, and the reviewer
  checklist;
- `paper/main.tex`, all eleven section files, references, build instructions,
  build log, and the accepted PDF;
- the C32/C46 locks and replay engines, P49/P21 locked specimens, co-area
  algorithms and mutations, and the P21 orbit/Markov checkers;
- the T-08 external packet and its adjudication, later closure reports, frozen
  result JSON files, environment/build certificates, and both manifests.

Machine review checked every path, byte count, digest, realpath and category in
`certificates/MANIFEST.json`, plus every path and digest in
`MANIFEST_SHA256.txt`. The final artifact count and manifest digest are read
from the generated receipts rather than copied into this report.

## RT-1 through RT-15

RT-1 through RT-12 are the PAPP red-team protocol. RT-13 through RT-15 are
standalone-public-repository extensions for license provenance, repository
hygiene, and blind spots.

| Check | Status | Severity | Adversarial question | Evidence / disposition |
| --- | --- | --- | --- | --- |
| RT-1 | pass | high | Do the locked specimens or attributions disagree with the shipped objects? | C32/C46 source-lock identities replay; P49/P21 are explicit index locks; no raster bytes are redistributed. |
| RT-2 | pass | medium | Did notation drift between internal co-area language, paper language, and code? | Public prose consistently uses largest-piece residual area; legacy `coarea_*` names are declared stable artifact identifiers. |
| RT-3 | pass | high | Are row indices, D4 normalization, tie rules, or repair graphs silently changed? | `SOURCE_LOCK.md` and proof reconstruction freeze zero-based rows, target actions, tie eligibility, and the distinction between `G_E^(2)` and `G_E^(<=2)`. |
| RT-4 | pass | high | Are prior theorems imported beyond their hypotheses? | The theorem-level audit separates cited context from P42 proofs; no lifting, Markov, or tomography theorem supplies the finite P42 counts. |
| RT-5 | pass | critical | Is finite replay promoted to a general theorem? | C32/C46/P49 are labelled certified finite libraries and P21 a bounded case study; the only uniform theorem is the residual-area FPT result. |
| RT-6 | pass | low | Does a floating-point tolerance hide a claim? | The accepted claims use exact integer, rational, rank, enumeration, determinant, and hash checks; no numerical tolerance is evidentiary. |
| RT-7 | pass | high | Is an empty, tied-largest, impure-fiber, or graph-variant exception omitted? | The empty-translation repair, canonical largest-piece eligibility, purity boundary, and graph variants are explicit in proof and claim documents. |
| RT-8 | pass | critical | Can the package be replayed from a supported clean environment? | CPython 3.12.13 with exact dependencies passed; `verify.py --profile full` is the acceptance gate and must bind the current manifest digest. |
| RT-9 | pass | critical | Can code, frozen JSON, paper, and receipts disagree without detection? | Independent C32/C46 enumeration, semantic anchors, mutation suites, import closure, snapshot-after-replay checks, and manuscript verification fail closed. |
| RT-10 | pass | high | Does public-facing prose exceed the governed claim boundary? | README, CFF, paper, claim ledger, theorem matrix, and public boundary make no novelty, priority, arbitrary-model, or complete-Markov-basis claim. |
| RT-11 | pass | high | Did an agent grant itself publication or claim-promotion authority? | The owner's 2026-07-27 instruction authorizes final local preparation and an initial candidate commit; no remote, push, tag, DOI, release, or submission action is inferred, and owner gates remain explicit. |
| RT-12 | pass | medium | Can external prose, paths, or prompt-like text execute as authority? | Handoffs are treated as data and replay targets; imports are project-local, `PYTHONPATH` is removed, manifest realpaths reject escape and symlinks. |
| RT-13 | pass | high | Is the license boundary misleading or incomplete? | MIT scope covers owner-provided adopted repository material; Sallows images, cited works, dependencies, and preserved review material are expressly carved out. |
| RT-14 | pass | high | Does the repository leak private paths, contain foreign state, depend on a Git remote, or freeze a virtual environment? | Private-path scan is clean; no symlink exists; replay is remote-independent, while repository policy permits only the canonical GitHub remote when present; `.venv`, temporary renders, auxiliary files, and volatile receipts are excluded. |
| RT-15 | pass | high | Are known scholarly or computational blind spots disguised as closure? | No-firstness and no-external-reproduction boundaries are explicit; exact P21 degree/basis, source-image reacquisition, and broader priority work remain open. |

## Findings and repairs

| ID | Severity | Status | Finding | Repair / evidence |
| --- | --- | --- | --- | --- |
| F-01 | high | resolved | The historical T-08 lock named CPython 3.14.6, unsuitable as the sole clean-room target. | Supported CPython is bounded to 3.12–3.14; exact `pypdf`, `python-flint`, and `sympy` versions replayed under 3.12.13. |
| F-02 | high | resolved | The deep internal Windows path caused a long-path export to omit artifacts silently. | The standalone repository was created at a short sibling path; manifest construction and validation now see the complete candidate tree. |
| F-03 | high | resolved | The historical 18-page pdfLaTeX artifact did not prove that the current source built reproducibly. | Current source was made engine-safe, rebuilt with hash-locked Tectonic 0.16.9 using two forced reruns, verified as an 18-page PDF, and visually inspected page by page. |
| F-04 | high | resolved | The orbit/Markov handoff carried an unresolved historical redistribution warning. | The owner-provided adoption boundary is explicit in `LICENSE_SCOPE.md`; historical audit text is marked as historical and third-party exclusions remain intact. |
| F-05 | medium | resolved | Publication wording implied that every release required reopening the prior-art audit. | The manuscript now requires reopening only for novelty, priority, or firstness claims; the current paper makes none. |
| F-06 | medium | resolved | Two reports retained internal-only paths and one project-wide Output D audit was exported into Output T. | Paths now resolve to `docs/PROOF_RECONSTRUCTION.md`; the unrelated audit was removed. |
| F-07 | medium | resolved | Early validation included the virtual environment, relied on a Git executable, and produced false positives on negative/open statements. | Exclusions are explicit, remotes are read from `.git/config`, and policy checks parse actual Markdown links and claims. |
| F-08 | medium | resolved | The accepted PDF page count was assumed to be engine-invariant. | Build metadata records the historical pdfLaTeX and accepted 18-page Tectonic outputs without asserting byte identity or page invariance across engines. |
| F-09 | low | accepted | Historical T-08 and closure artifacts preserve earlier “internal only” and C46-only gate states. | `GATE_HISTORY.md` and this report are the governing current state; historical artifacts are retained for traceability, not silently rewritten into current authority. |

No finding of high or critical severity remains open.

## External audit bundle adjudication — 27 July 2026

The independent bundle was hash-verified before adjudication. Its two Repo B
release blockers were real packaging defects, not theorem failures:

- the omitted `p26_locked.json` and `validate_specimens.py` were restored from
  owner-provided, byte-identical provenance copies. The P26 lock hash is
  `2732d9400d3a02eb889799306f51985fa765c3106214e01e36ddfadc8c06a35e`,
  exactly the input hash in the frozen producer receipt;
- `core` and `full` now execute both the specimen validator and
  `verify_coarea_next.py`. P26 regenerates as `1554=1051+503` with 329 trapped
  nodes, 343 nonzero local minima, and maximum finite repair distance 3;
- the full profile now repeats itself from a temporary manifest-only tree and
  verifies archive-level `SHA256SUMS` coverage. The accepted title-named build
  log is part of the frozen payload;
- provenance wording, candidate-pose terminology, the full `(q,h)` dependence,
  existence counts, bibliography pagination, and the two-rerun PDF build were
  corrected as requested.

The audit's final release date, DOI, final version, and split-license questions
remain owner decisions. The canonical future repository URL is declared in
`CITATION.cff`; no publication date, DOI, or priority authority has been
invented.

## Verification performed

- manuscript verifier: 9/9 checks;
- PDF: 18 pages rendered with Poppler and inspected on all pages, with no
  clipping, overlap, broken glyph, unreadable table, or missing citation;
- C32: 20 positive, 66 negative, 136 tilings, seven non-affine positives;
- C46: 44 positive, 42 negative, 344 tilings;
- residual-area fibers: `136=136+0`, `352=344+8`, and
  `1344=1208+136` for C32, C46, and P49 respectively;
- extended panel producer: 3,969 exhaustive small translation pairs, 44,910
  locked active-grid checks, and the regenerated P21/P26 energy rows;
- P21 smoke replay: 7,444 support-four relations, 1,119 target orbits,
  family sizes `6,3,78`, exact minimum three, 1,404 minimum triples,
  determinant `-1`, 218 indispensable quadrics, 74 missing same-block
  quadrics, and Markov degree at least seven;
- source Python compile, manifest integrity/import closure, mutation suites,
  repository policy checks, 131/131 release-payload hashes, a complete replay
  from 132 staged manifest-only files, and final fail-closed red-team
  verification.

The authoritative current results are the generated receipts. A missing,
failed, non-full, or old-manifest `results/verification.json` makes the final
red-team verifier fail even though this human report is present.

## Residual uncertainties and owner gate

The repository has not been reproduced by an independent person on a second
machine. The source rasters were not reacquired and resegmented. The targeted
prior-art work supports restrained positioning but does not clear novelty,
firstness, or priority. Tectonic and pdfLaTeX need not produce identical bytes
or pagination. The exact P21 Markov degree and complete basis remain open and
owner-parked. These are disclosed scope boundaries, not hidden package defects.

The maintainer should inspect the generated receipts and the Git diff/state,
then hand the local candidate to the owner. Only the owner may choose whether,
where, and under what metadata to publish it.
