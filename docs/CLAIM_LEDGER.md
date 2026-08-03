# Claim ledger

Status: public release `v1.0.0`. Last reviewed: 2026-08-03.

| Claim | Level | Statement and exact scope | Evidence | Public wording |
| --- | --- | --- | --- | --- |
| Model | CLM | Finite named cell-list pieces, finite lattice-orientation action, one-copy placements, row-column X-rays, coverage, margin fiber, exact-cover subset, and exact-two replacement graph. | Paper Sec. 2; `SOURCE_LOCK.md` | Define the conjunction; do not claim invention of tomography or tiling reconstruction. |
| Hierarchy | CL5 + CL3 witnesses | Fiber purity implies repair exactness, which implies support exactness. Strictness is witnessed by certified C32/C46/P49 rows. | Paper Secs. 3--4; `FOUNDATIONAL_SECTION.md`; finite certificates | State the implications and named finite witnesses. |
| Translation cap | CL5 | For finite nonempty `A,B subset Z^2`, `|D(A,B)| <= max(0,|B|-|A|+1)`. | Paper Lemma 5.1; `PROOF_RECONSTRUCTION.md` | State with the empty branch; the sumset mechanism is classical. |
| Active carrier | CL5 | After fixing a largest selected pose with residual area `q`, every participating residual placement lies in an active carrier of at most `q^2` target cells. | Paper Sec. 5; `PROOF_RECONSTRUCTION.md`; replay | Core theorem mechanism; no firstness. |
| FPT theorem | CL5 | For a fixed selected named set and orientation bound `h`, support, purity, and repair in `G_E^(2)` are FPT in `(q,h)`, with fiber bound `h(q+1)(h q^2)^q`. | Paper Sec. 6; verifier; theorem spine | Sole uniform headline; no practical-runtime or arbitrary-tile claim. |
| Type compression | CL5 supporting | Under the exact finite-cell-list and canonical-largest contract, implicit decision and compressed classification are FPT under exact participation types. Literal named listing is output-sensitive. | Paper Sec. 7; exact verification panel | State only decision and compressed classification. |
| Energy | CL5 supporting | Overlap mass equals half the `L1` coverage deviation; strict descent is a sufficient repair criterion with radius at most `q`. | Paper Sec. 7 | Sufficient, not necessary or characterizing. |
| C32 | CL3 | The source-locked C32 library has 20 positive and 66 negative area rows, 136 tilings, and a pure 136-node margin fiber. | C32 lock, certificate, structural verifier, mutation suite | Certified finite result; no priority. |
| C46 | CL3 | The source-locked C46 library has 44 positive and 42 negative rows, 344 tilings, and margin fiber `352=344+8`; repair-exact but impure. | C46 lock, certificate, verifier, mutation suite | Certified finite result; Sallows attribution required. |
| P49 | CL3/CLN | The locked P49 panel has `1344=1208+136`; one tiling row has eight trapped singleton components and another margin-feasible row has no tiling. | P49 lock; residual-area certificate | Certified finite negative controls only. |
| P21 fixed fiber | CL3 | For row `(4,5,12,13)`, the `14x72` configuration has rank 12 and kernel rank 60; a rank-54 move module connects the fixed 32-node fiber but does not generate the lattice. | P21 certificates and integrated replay | Bounded case study only. |
| P21 orbit minimum | CL3 | Support-four relations number 7,444 in 1,119 target orbits; three complete orbit modules are necessary and sufficient, with 1,404 minimum triples and channel sizes `6,3,78`. | Minimum-orbit certificate | Exact for the frozen configuration only. |
| P21 Markov boundary | CL3 + CLN | `M_<=4=K`, but the family is not all-RHS Markov: 74 indispensable same-block quadrics are missing; Markov degree is at least seven; at least 6,941 generators occur through degree four. | Markov no-go and single-block certificates | State lower bounds and separation, never a complete basis. |
| P21 open questions | CLO | Exact Markov degree, complete basis, four block-internal bases, and structured lifting remain open. | Paper Sec. 9; boundary | Keep explicitly open. |
| Priority | CLB | No novelty, priority, or firstness claim is made. | Prior-art audit and source lock | Do not use first, novel, or unprecedented wording. |

The release records only the claims supported by the paper and replay package.
A repository release is not a DOI, arXiv deposit, journal submission, or
evidence of independent external reproduction.
