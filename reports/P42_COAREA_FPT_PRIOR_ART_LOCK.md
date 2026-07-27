# P42 co-area FPT prior-art lock

**Status:** partial source lock, 2026-07-26.
**Agent package:** `source_lock_agent`.
**Purpose:** complexity boundary for the internal co-area algorithm.
**Public use:** blocked pending a systematic MathSciNet/zbMATH-level novelty
search and maintainer review.

## Locked external statements

### `PA-COAREA-01` — tile-packing tomography hardness

- Primary source: M. Chrobak, C. Dürr, F. Guíñez, A. Lozano,
  N. K. Thang, *Tile-Packing Tomography is NP-hard*,
  arXiv:0911.2567.
- URL: <https://arxiv.org/abs/0911.2567>
- Directly checked: 2026-07-26.
- Source model: disjoint translated copies of one fixed tile in an
  `m x n` grid, with prescribed row and column projections; a full cover is
  not required.
- Locked statement: `TPTP(T)` is NP-complete for every fixed non-bar tile.

Allowed use: the unrestricted tomographic-packing problem is hard even with
one fixed non-bar tile.

Not allowed: transferring this hardness automatically to P42's
large-piece/co-area parameterisation.  P42 uses named one-copy pieces, D4
poses, a fixed complete target margin and a distinguished piece occupying all
but `q` cells.  A reduction preserving that parameter has not been supplied.

### `PA-COAREA-02` — Exact Cover parameterised by number of selected sets

- Primary source: V. Guruswami, P. Lin, *Parameterized
  Inapproximability of Exact Cover and Nearest Codeword*, arXiv:1905.06503.
- URL: <https://arxiv.org/abs/1905.06503>
- Directly checked: 2026-07-26.
- Source parameter: `k`, the number of sets chosen in the Exact Cover.
- Locked boundary statement: the paper records exact `k`-ExactCover as
  W[1]-complete and proves stronger parameterised inapproximability results
  under ETH/SETH.

Allowed use: bounding only the number of selected pieces is not, by itself, a
route to an FPT theorem for arbitrary set systems.

Not allowed: reading the W[1]-hardness as a contradiction of the P42
algorithm.  The P42 co-area argument additionally kernels every
margin-participating residual placement into at most `q^2` active cells.  That
bounded active universe is absent from generic `k`-ExactCover.

### `PA-COAREA-03` — geometric Exact Cover warning

- Primary bibliographic record: P. Ashok, S. Kolay, N. Misra, S. Saurabh,
  *Unique covering problems with geometric sets*, COCOON 2015,
  DOI `10.1007/978-3-319-21398-9_43`.
- DOI: <https://doi.org/10.1007/978-3-319-21398-9_43>
- Abstract directly checked through the authors' institutional research
  portal on 2026-07-26.
- Locked boundary statement: Exact Cover parameterised by the number of sets
  remains W[1]-hard for geometric unit squares, while some other geometric
  set classes have different behaviour.

Allowed use: geometry alone does not make Exact Cover FPT in the number of
selected sets.

Not allowed: importing its square-set hardness into the P42 co-area model
without a parameter-preserving reduction.

## PAPP notation and import boundary

PAPP uses:

```text
q = |T| - |L|
```

for a frozen largest named piece `L`.  This `q` is neither:

- the number of copies in tile-packing tomography;
- the `k` of generic `k`-ExactCover;
- target width or height.

The internal proof is self-contained and imports none of the external
theorems above.  They are used only to delimit overclaims.

## Search result and source gap

Targeted searches for:

- polyomino tiling parameterised by largest-piece complement;
- residual-cell/co-area tiling algorithms;
- placement-coloured tomography parameterised by a near-spanning piece;

found no direct formulation matching the P42 theorem.  This is **not** a
novelty verdict.  The search was web/arXiv/DOI-level, not a systematic
MathSciNet, zbMATH, monograph and citation-graph audit.  Moreover, the exact
cover and bounded-universe dynamic-programming ingredients are standard
enough that the honest current posture is:

> internally correct parameterised closure; external novelty unknown and
> plausibly limited to the placement-coloured repair formulation.

## Sharpening and added prior-art boundary

The 2026-07-26 next-closure audit adds a self-contained translation-cap proof,
the sharpened `2^(O(q log q))` fiber bound, an explicit radius bound and exact
participation-type compression. The following sources delimit what P42 must
not claim:

- Böröczky–Pálfy–Serra, *On the cardinality of sumsets in torsion-free
  groups*, BLMS 44(5), 2012,
  <https://academic.oup.com/blms/article/44/5/1034/495967>: broad classical
  sumset background. P42 does not depend on this paper because the elementary
  finite proof is included.
- Tucker-Foltz, *Locked Polyomino Tilings*, arXiv:2307.15996,
  <https://arxiv.org/abs/2307.15996>: pair removal/replacement and isolated
  ReCom states are prior art.
- Gross–Yamzon, *Binomial ideals of domino tilings*, arXiv:2008.02896,
  <https://arxiv.org/abs/2008.02896>: toric/binomial connectivity of tiling
  spaces is prior art.
- Creignou et al., *Parameterized Enumeration with Ordering*,
  arXiv:1309.5009, <https://arxiv.org/abs/1309.5009>: Total-FPT and Delay-FPT
  are established enumeration-complexity terms.
- Chrobak–Couperus–Dürr–Woeginger, *A Note on Tiling under Tomographic
  Constraints*, arXiv:cs/0108010,
  <https://arxiv.org/abs/cs/0108010>: heterogeneous tile types with
  tomographic projections are prior art.

The possibly distinctive conjunction is narrower: named heterogeneous
one-copy placements, a near-spanning piece, a coarse aggregate X-ray fiber,
an exact-cover sublocus and pair-repair predicates, parameterised by co-area.
No exact collision was found in the targeted check, but no priority
certificate exists.

## Non-claims

- No new NP-hardness or lower bound is claimed.
- No contradiction with known Exact Cover hardness is claimed.
- FPT decision and compressed classification for an implicit library are
  internal theorem candidates only under the exact finite-cell input
  contract; no Total-FPT literal listing claim is made.
- Delay-FPT expansion is not represented as an implemented P42 artifact.
- No continuous/polygonal extension covering C34 is claimed.
- No public or paper-ready novelty claim follows from this lock.

## Handoff

The source boundary is adequate for an internal theorem report and experiment
ledger entry.  Claim promotion or paper use requires a later Claim Curator
and Red Team run plus a systematic novelty audit.
