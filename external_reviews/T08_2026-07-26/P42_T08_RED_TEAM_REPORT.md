# P42 Output T — T‑08 Red-Team Report

**Target:** *Tomographic Exactness and Co-Area Localization for Named Grid Covers*  
**Reviewed snapshot:** internal reviewer package frozen on 2026-07-26  
**Overall verdict:** `FIX_FIRST — MATHEMATICAL CORE PASSES; REVIEWER PACKAGE AND ATTRIBUTION DO NOT YET PASS T‑08`

## 1. Executive verdict

The mathematical spine survives adversarial review:

- the translation cap is correct after the empty-translation branch is included;
- the active-carrier localization is correct under the finite cell-list and aggregate row/column-margin contract;
- the fixed-selected-set FPT theorem follows;
- the explicit fiber and repair-radius bounds follow;
- the support/purity/repair hierarchy and the C32/C46/P49 strictness witnesses are logically and computationally coherent;
- the P21 section correctly separates one-fiber connectivity, integral lattice generation, and all-right-hand-side Markov connectivity.

No mathematical counterexample was found to the principal theorem.

T‑08 nevertheless **cannot close on the current snapshot**. Four visible issues are release-blocking:

1. the manuscript does not name or cite Lee Sallows although the foundational C32/C46/P49 shapes and target arrangements are transcriptions of his geomagic-square gallery;
2. `REPRODUCE.md` says the replay uses only the Python standard library, but frozen replay scripts import `sympy` and `python-flint`;
3. `verify.py` checks the manifest only before executing replay commands and never rechecks it afterward, so a replay can mutate a frozen artifact and the same invocation can still emit `PASS`;
4. the title uses the unqualified phrase “Tomographic Exactness”, while the project’s own claim boundary forbids that phrase unless the exactness level is named.

The correct gate decision is therefore:

```text
T-08 = FIX_FIRST
mathematical theorem spine: PASS_WITH_EXPOSITION_REPAIRS
finite certificates: PASS_AS_FROZEN_RECEIPTS
reviewer-package integrity: FAIL_PENDING_HARDENING
source attribution: FAIL_PENDING_SALLOWS_CITATION
public/release readiness: NOT AUTHORIZED
```

The sole public P42 claim remains `PC-1`.

---

## 2. Work actually performed

The review did not rely only on the agent’s summary. It included:

- independent SHA-256 calculation of `MANIFEST.json`;
- independent parsing of all 86 manifest rows, categories, profiles, and boundary flags;
- static audit of `verify.py`;
- static audit of `REPRODUCE.md`, `README_REVIEWER.md`, and `REVIEW_CHECKLIST.md`;
- mathematical reconstruction of the translation-cap, active-carrier, state-space, graph, type-compression, and energy arguments;
- cross-check of C32/C46/P49 counts and witness semantics against the frozen theorem documents;
- cross-check of the bounded P21 claims against the frozen case-study chain;
- rendering and visual inspection of all 16 PDF pages;
- direct primary-source literature search in discrete tomography, tiling tomography, reconfiguration, toric tiling connectivity, geomagic squares, and the source gallery.

The complete 11-command full replay was **not rerun in the present runtime**, because the active container does not contain the entire 86-file project-relative tree and its external Python environment. The package’s existing full-profile receipt was inspected, but is not treated as an independent external reproduction.

---

## 3. Integrity findings

### 3.1 Manifest identity — PASS

Independent checks found:

```text
artifact count: 86
manifest SHA-256:
1c9327fc60f5fc13d1ef0cd2aa2d293164157f92c961cf4b14f7c6bcbddf4223
```

Category profile:

| Category | Count |
|---|---:|
| replay_code | 23 |
| certificate | 22 |
| manuscript | 17 |
| governance | 6 |
| reviewer | 5 |
| source_lock | 5 |
| theorem | 4 |
| verification | 3 |
| sources | 1 |

The boundary fields are correctly fail-closed:

```text
public_authority = false
public_claim_set_changed = false
coarea_priority_clearance = false
c32_public_promotion = false
p21_exact_markov_basis = open_owner_parked
```

### 3.2 Frozen receipt — internally coherent

The stored receipt records profile `full`, 11 command identifiers, 10 semantic checks, and status `PASS`. This is coherent with the manifest profile.

### 3.3 Pre-run-only hash checking — release blocker

Current order in `verify.py`:

```text
check_manifest()
check_semantics()
run_commands(...)
write PASS receipt
```

There is no second manifest or semantic check after the child processes return.

Therefore this sequence is possible:

1. manifest check passes;
2. a replay command changes a frozen certificate or source file;
3. every command returns zero;
4. the parent writes `PASS`;
5. the package is no longer the snapshot that was checked.

This is a time-of-check/time-of-use defect. It does not prove that any current child command mutates an artifact, but it means the verifier does not certify the property it appears to certify.

**Required repair:**

```text
snapshot and validate before run
run commands
validate every artifact and semantic anchor again
compare pre/post manifest identity and hashes
write PASS only after post-run equality
```

Prefer execution in a temporary or read-only manifest-only copy.

### 3.4 Path safety is lexical, not filesystem-safe

The verifier rejects absolute paths and `..`, but does not reject symlinks or require:

```python
target.resolve().is_relative_to(PROJECT.resolve())
```

A project-relative symlink can escape the project root. The build script should either reject symlinks in the frozen graph or verify realpath containment for every artifact.

### 3.5 No transitive import-closure check

The manifest freezes replay scripts, but no gate proves that all project-local modules imported transitively are themselves manifest-pinned. A full replay should run in an isolated tree populated only by manifest artifacts, or an import-dependency audit should be added.

### 3.6 Receipt provenance is too thin

The receipt stores only command IDs and `PASS`. For review-grade provenance, record:

- exact `argv`;
- Python version;
- versions of `sympy`, `python-flint`, and the TeX/PDF tools used where relevant;
- operating system and architecture;
- deterministic environment fields;
- duration;
- exit code;
- SHA-256 of stdout and stderr, or preserved log paths.

Avoid timestamps in the stable receipt if byte stability is required; put volatile run metadata in a separate non-pinned log.

---

## 4. Reproducibility finding: the “standard library only” statement is false

`REPRODUCE.md` currently states that the replay uses only Python’s standard library.

Frozen project scripts imported by the reviewer profiles include:

```python
from flint import fmpz_mat
import sympy
from sympy import ...
```

The full replay therefore requires, at minimum, external packages including:

- `python-flint`;
- `sympy`.

This is a factual error in the reviewer instructions and a high-severity reproducibility issue.

**Required repair:**

1. add a locked environment file, e.g. `requirements-review.txt` or `environment.yml`;
2. record exact versions from the successful frozen run;
3. add installation commands;
4. add a dependency preflight to `verify.py`;
5. change the wording to:

> The reviewer entry point is Python-based. Some profiles use only the standard library, while the full P21 algebraic replay additionally requires the version-locked `sympy` and `python-flint` dependencies listed in the reviewer environment file.

Also distinguish:

- replay from the **locked discrete normalization**, which the package supports;
- independent re-transcription from Sallows’s original rasters, which the package cannot support without the owner-supplied source bytes.

---

## 5. Mathematical audit

### 5.1 Definitions and hierarchy — PASS, with one terminology addition

The row-wise definitions are coherent:

\[
\mathcal F_E=\{\text{one-copy placement tuples with target margins}\},
\qquad
\mathcal T_E=\{x\in\mathcal F_E:c_x=\mathbf 1_T\}.
\]

The exact-two graph \(G_E^{(2)}\) is distinguished from \(G_E^{(\le 2)}\).

The implications

\[
\text{purity}\Longrightarrow \text{repair-exactness}
\Longrightarrow \text{support-exactness}
\]

are correct, including the empty-fiber convention.

**Needed exposition repair:** define library-level language explicitly. For example:

> A library is universally support-exact, pure, or repair-exact when the corresponding row-wise predicate holds for every declared area-compatible selected set.

Without this sentence, phrases such as “C46 is repair-exact” silently change quantifiers.

### 5.2 Translation cap — PASS

For finite nonempty \(A,B\subset\mathbb Z^2\),

\[
D(A,B)=\{t:A+t\subseteq B\}
\]

satisfies

\[
|D(A,B)|\le \max(0,|B|-|A|+1).
\]

The proof via an integer linear functional injective on the finite sumset and the one-dimensional torsion-free sumset bound is valid.

The empty branch is essential and is correctly repaired in the theorem spine.

### 5.3 Active-carrier lemma — PASS

After fixing a legal pose of a largest selected piece \(L\), let

\[
q=|T|-|L|.
\]

The residual row and column margins each have total mass \(q\). A participating residual placement cannot use a row or column with zero residual margin. It is therefore contained in at most \(q\) active rows and \(q\) active columns, hence at most \(q^2\) cells.

This is correct under the stated assumptions:

- all poses lie inside \(T\);
- margins are ordinary aggregate horizontal/vertical line sums;
- pieces are finite cell lists.

### 5.4 Fixed-selected-set FPT theorem — PASS

The bounds

\[
M_L\le h(q+1),
\]

and

\[
|\mathcal F_E|
\le h(q+1)(hq^2)^q
=2^{O(q\log q)}
\quad\text{for fixed }h
\]

follow.

The fixed-set algorithms for:

- support-exactness;
- purity;
- exact-two repair-exactness;
- finite repair radius;

are FPT in \((q,h)\) under the explicit finite cell-list input contract.

The radius bound

\[
\rho(E)\le |\mathcal F_E|-1
\]

is correct and is appropriately described as existential and non-sharp.

### 5.5 Orientation contract — needs one formal sentence

The manuscript should explicitly say that the supplied orientation group acts by lattice automorphisms of \(\mathbb Z^2\), or equivalently that every oriented mask is explicitly supplied as an integer cell list.

Otherwise “orientation followed by integer translation” is not fully formal for an arbitrary finite group.

### 5.6 Implicit-library FPT proposition — plausible, but under-specified

The type-compression argument is credible, but the theorem needs a fully quantified parameterized problem.

Recommended statement:

> Input: a finite target \(T\), a finite named library, an explicit finite lattice-orientation action, and an integer \(Q\). Decide whether there exists an area-compatible selected set \(E\) whose canonically chosen largest name \(L(E)\) satisfies \(|T|-|L(E)|\le Q\) and whose fiber has the requested predicate.

Then prove a formal **type-isomorphism lemma**:

> Equal exact participation-type count vectors yield isomorphic margin fibers, exact-cover subloci, and exact-two repair graphs after renaming equal-type names.

The type must retain:

- area;
- exact masks for every ordered largest-pose scenario;
- cross-scenario identity of the same placement;
- canonical-largest tie eligibility;
- available named multiplicity, truncated only after proving that no solution uses more than \(q\) residual names.

This is a severity-2 proof-exposition issue, not a detected counterexample.

### 5.7 Overlap energy — PASS

For a margin node,

\[
\Phi(x)=\sum_u\max(c_x(u)-1,0)
       =|T|-\left|\bigcup_i A_i\right|
       =\frac12\|c_x-\mathbf 1_T\|_1.
\]

The equality uses total selected area \(|T|\), and \(0\le\Phi\le q\) because the union contains the frozen largest piece.

Strict descent at every non-tiling node is sufficient for repair and gives \(\rho\le q\). The manuscript correctly does not claim necessity.

### 5.8 Foundational finite data — PASS in frozen scope

The frozen values are mutually consistent:

| Library | Carrier | Exact rows | Margin rows | Fiber |
|---|---:|---:|---:|---:|
| C32 | 86 | 20 | 20 | \(136=136+0\) |
| C46 | 86 | 44 | 44 | \(352=344+8\) |
| P49 | 94 | 60 | 61 | \(1344=1208+136\) |

Strictness witnesses are correctly separated:

- C46: repair-exact but impure;
- P49 `(4,9,10,11)`: tiling exists, but eight non-tiling nodes are trapped singletons;
- P49 `(0,1,3,14)`: eight margin nodes and no tiling.

### 5.9 P21 case study — PASS in declared scope

The bounded proposition chain is logically correct:

- \(14\times72\), rank 12, kernel rank 60;
- selected fiber \(32=8+24\);
- one complete support-four orbit can connect that fiber while leaving lattice rank 54;
- three complete orbit modules are minimally necessary and sufficient for integral generation above \(M_{\le3}\);
- all support-at-most-four squarefree one-copy relations generate the lattice;
- they are not an all-right-hand-side Markov basis;
- 74 within-block indispensable quadrics are missing;
- the Markov degree is at least 7, not proved equal to 7.

The case study is useful, but it should remain a bounded boundary example, not a second headline theorem.

---

## 6. Source attribution: Lee Sallows is missing

This is the most serious documentary problem.

The manuscript contains no occurrence of:

```text
Sallows
Lee
geomagic
```

yet C32, C46, and P49 are normalized from Lee Sallows’s geomagic-square gallery.

The paper currently speaks of source-owned assets and hashes, but does not tell the reader who created the shapes, targets, and displayed geomagic arrangements.

This must be corrected before circulation.

### Required attribution paragraph

Add near the first introduction of the finite libraries:

> The finite libraries C32, C46, and P49 are normalized from \(4\times4\) geomagic-square specimens created and displayed by Lee Sallows. The piece geometries, targets, and displayed arrangements are Sallows’s source material. The contributions of the present paper begin with the source-locked discrete transcription: exhaustive placement and exact-cover censuses, aggregate-margin fibers, repair graphs, and the uniform largest-piece localization theorem. We do not claim authorship of the underlying geomagic specimens.

### Required references

At minimum:

1. Lee Sallows, **Geometric Magic Squares**, *The Mathematical Intelligencer* 33 (2011), 25–31, DOI `10.1007/s00283-011-9229-0`.
2. Lee Sallows, **Geomagic Squares** official gallery, access date and stable source descriptors/digests.
3. Peter J. Cameron, **Geomagic squares** (2011), for the finite group-action/power-set abstraction, clearly labelled as expository context rather than a journal theorem.

The official gallery is mutable: it has changed its page count. Public specimen IDs should therefore not depend only on current page numbers. Include stable descriptive names, access date, direct asset identity, and SHA-256.

If any source-derived diagrams, colored shapes, or raster crops will appear in a public manuscript, obtain explicit permission or ensure the intended use is covered. Merely omitting the original raster from the repository does not settle figure rights.

---

## 7. Title and terminology conflict

The project’s claim boundary forbids:

> “Tomographic exactness” without naming which exactness level.

The manuscript title is:

> *Tomographic Exactness and Co-Area Localization for Named Grid Covers.*

That is an internal contradiction.

Moreover, **co-area** is established terminology in geometric measure theory and is a poor search term for the new parameter.

Recommended title:

> **Named Grid Covers under Row–Column Margins: Three Exactness Levels and Largest-Piece Localization**

Other acceptable variants:

- **Aggregate-Margin Fibers and Largest-Piece Localization for Named Grid Covers**
- **Support, Purity, and Repair in Named Grid-Cover Fibers**
- **Named Grid Covers under Aggregate Margins: Largest-Piece FPT and Certified Geomagic Case Studies**

Recommended parameter name:

```text
largest-piece residual area
largest-piece complement area
residual area q
```

Avoid making “co-area” the principal public term.

---

## 8. Prior-art verdict

### 8.1 What is definitely prior art

The following surrounding layers are established:

- discrete tomography from line sums;
- tilings under row/column tomographic constraints with multiple tile types;
- fixed-tile packing tomography and its hardness;
- polyatomic/colored tomography;
- domino reconstruction from two projections;
- repair or solution discovery from infeasible states;
- pair replacement and locked polyomino tilings;
- toric/binomial move connectivity of tiling spaces;
- Markov-basis/fiber language;
- geomagic squares and their group-action abstraction.

The paper correctly avoids broad firstness claims.

### 8.2 Missing direct sources

The publication-stage bibliography should add:

- G. T. Herman and A. Kuba, eds., *Discrete Tomography: Foundations, Algorithms, and Applications* (1999).
- M. Chrobak and C. Dürr, *Reconstructing Polyatomic Structures from Discrete X-Rays: NP-Completeness Proof for Three Atoms*, TCS 259 (2001), 81–98.
- L. Sallows, *Geometric Magic Squares*, 2011.
- Lee Sallows’s official gallery.
- Peter Cameron’s finite group-action formulation as contextual prior art.
- Tracy Chin, *A Computational Commutative Algebra Approach to Tilings* (2019 honors thesis), after directly obtaining and reading the full thesis. The author page states that it proves a primary decomposition for an ideal generated by flip moves in a grid graph.

### 8.3 Safe novelty boundary

No direct source collision was found for the exact conjunction:

```text
one named copy of each selected heterogeneous piece
+ aggregate untyped row/column margins
+ overlaps/holes allowed in the relaxed fiber
+ exact covers as a distinguished sublocus
+ support/purity/exact-two-repair predicates
+ FPT by largest-piece residual area q
```

That absence is not a priority certificate.

The strongest defensible positioning is:

> We study a named exact-cover sublocus of an overlap-permitted aggregate-margin placement fiber. Fixing a largest piece localizes every participating residual placement to a \(q\times q\) active carrier, yielding FPT algorithms in the largest-piece residual area and the orientation bound.

The **active-carrier lemma plus its exact problem contract** is the plausible contribution. The dynamic programming and bounded-type compression mechanisms are standard once the localization is available.

---

## 9. Reviewer checklist defect

The checklist currently says:

> P49 uses zero-based piece indices and a complete `94`-piece carrier.

P49 has:

- 16 named pieces;
- 94 area-compatible selected rows.

Replace it with:

> P49 uses zero-based piece indices and a complete 94-row area-compatible carrier over 16 named pieces.

---

## 10. Recommended T‑08 issue closure order

### Gate A — release blockers

1. add Sallows attribution and geomagic references;
2. rename the manuscript/title terminology;
3. correct the false standard-library-only claim;
4. lock and document external dependencies;
5. add post-replay manifest/semantic revalidation.

### Gate B — theorem exposition

6. formalize the implicit-library parameterized problem;
7. add the type-isomorphism lemma;
8. make the orientation/lattice-action contract explicit;
9. add the library-level quantifier definition.

### Gate C — package hardening

10. realpath/symlink containment;
11. transitive import closure or isolated manifest-only replay;
12. richer receipt provenance;
13. correct the P49 checklist row;
14. clarify normalized-model replay versus source-raster reconstruction.

### Gate D — final prior-art pass

15. read Tracy Chin’s thesis in full;
16. add the foundational discrete-tomography book and the three-atom paper;
17. complete bibliographic metadata;
18. perform one final current citation-forest search before any public submission.

---

## 11. Final gate decision

```text
MATHEMATICAL CORE
PASS_WITH_EXPOSITION_REPAIRS

FINITE FOUNDATION AND P21 CASE STUDY
PASS_IN_FROZEN_SOURCE-LOCKED_SCOPE

NOVELTY / PRIORITY
NOT CLEARED; SAFE CONTRIBUTION WORDING AVAILABLE

REVIEWER PACKAGE
FAIL_FIX_FIRST

PUBLIC ACTION
NOT AUTHORIZED

T-08
OPEN — 4 SEVERITY-1, 5 SEVERITY-2, 4 SEVERITY-3 FINDINGS
```
