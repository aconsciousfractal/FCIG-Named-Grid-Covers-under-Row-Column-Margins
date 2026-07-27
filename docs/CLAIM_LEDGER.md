# Claim ledger

Status: public repository, owner-published 2026-07-27; the replay gate retains
the technical label `public-release candidate`. No tag, GitHub Release, DOI,
arXiv deposit, journal submission, priority, or firstness is claimed.
Last reviewed: 2026-07-27.

| Claim | Level | Statement and exact scope | Evidence | Public wording |
| --- | --- | --- | --- | --- |
| T-DEF | CLM | Finite named cell-list pieces, finite lattice-orientation action, one-copy placements, row-column X-rays, coverage, margin fiber, exact-cover subset, and exact-two replacement graph. | Paper Sec. 2; `docs/SOURCE_LOCK.md` | May define the model; must not claim invention of tomography or tiling reconstruction. |
| T-HIER | CL5 + CL3 witnesses | Fiber purity implies repair exactness, which implies support exactness. Strictness is witnessed by certified C32/C46/P49 rows. | Paper Secs. 3–4; `docs/FOUNDATIONAL_SECTION.md`; finite certificates | May state the implications and named finite witnesses. |
| T-TRANS | CL5 | For finite nonempty `A,B subset Z^2`, `|D(A,B)| <= max(0,|B|-|A|+1)`. | Paper Lemma 5.1; proof reconstruction | May state with the empty branch; the sumset mechanism is classical. |
| T-ACTIVE | CL5 | After fixing a largest selected pose with residual area `q`, every participating residual placement lies in an active carrier of at most `q^2` target cells. | Paper Sec. 5; `docs/PROOF_RECONSTRUCTION.md`; mutation-backed replay | Core theorem mechanism; no firstness. |
| T-FPT | CL5 | For a fixed selected named set and orientation bound `h`, support, purity, and repair in `G_E^(2)` are FPT in `(q,h)`, with fiber bound `h(q+1)(hq^2)^q`. | Paper Sec. 6; verifier and theorem spine | Sole uniform headline; no practical-runtime or arbitrary-tile claim. |
| T-TYPE | CL5 supporting | Under the exact finite-cell-list and canonical-largest contract, implicit decision and compressed classification are FPT under exact participation types. Literal named listing is output-sensitive. | Paper Sec. 7; type-isomorphism proof; exact verification panel | May state only decision/compressed classification. |
| T-ENERGY | CL5 supporting | Overlap mass equals half the `L1` coverage deviation; strict descent is a sufficient repair criterion with radius at most `q`. | Paper Sec. 7 | Sufficient, not necessary or characterizing. |
| T-C32 | CL3 | The source-locked C32 library has 20 positive and 66 negative area rows, 136 tilings, and a pure 136-node margin fiber. | C32 lock, certificate, structural verifier, mutation suite | Certified finite result; no priority. |
| T-C46 | CL3 | The source-locked C46 library has 44 positive and 42 negative rows, 344 tilings, and margin fiber `352=344+8`; repair-exact but impure. | C46 lock, certificate, verifier, mutation suite | Certified finite result; Sallows source attribution required. |
| T-P49 | CL3/CLN | The locked P49 panel has `1344=1208+136`; one tiling row has eight trapped singleton components and another margin-feasible row has no tiling. | P49 lock; residual-area certificate | Certified finite negative controls only. |
| T-P21-A | CL3 | For row `(4,5,12,13)`, the `14x72` configuration has rank 12 and kernel rank 60; a rank-54 move module connects the fixed 32-node fiber but does not generate the lattice. | P21 certificates and integrated replay | Bounded case study only. |
| T-P21-B | CL3 | Support-four relations number 7,444 in 1,119 target orbits; three complete orbit modules are necessary and sufficient, with 1,404 minimum triples and channel sizes `6,3,78`. | Minimum-orbit certificate | Exact for the frozen configuration only. |
| T-P21-C | CL3 + CLN | `M_<=4=K`, but the family is not all-RHS Markov: 74 indispensable same-block quadrics are missing; Markov degree is at least seven; at least 6,941 generators occur through degree four. | Markov no-go and single-block certificates | May state the lower bounds and separation, never a complete basis. |
| T-P21-OPEN | CLO | Exact Markov degree, complete basis, four block-internal bases, and structured lifting remain open and owner-parked. | Paper Sec. 9; boundary | Must remain explicitly open. |
| T-PRIORITY | CLB | No claim of novelty, priority, or firstness has been cleared. | Prior-art audit and source lock | Must not use first/novel/unprecedented wording. |

## Promotion decision

The owner published the repository on 2026-07-27. This ledger records the
claims supported by that public repository; publication does not by itself
authorize a tag, GitHub Release, DOI, arXiv deposit, journal submission, or
priority language.
