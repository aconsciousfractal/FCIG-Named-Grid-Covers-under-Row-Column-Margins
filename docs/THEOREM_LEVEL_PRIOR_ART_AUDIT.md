# Theorem-level primary-source audit

Last reviewed: 2026-07-26. This audit assigns each result a source-aware role;
it is not a priority certificate. A negative search is not evidence of
firstness, so the paper makes no novelty or priority claim.

## Primary comparison set

| ID | Primary source | Role in the comparison |
| --- | --- | --- |
| `PA-CCDW` | Chrobak, Couperus, Dürr, Woeginger, *A Note on Tiling under Tomographic Constraints*, arXiv `cs/0108010` | several tile types, typed projections, reconstruction, complexity |
| `PA-DGRR` | Dürr, Goles, Rapaport, Rémila, *Tiling with bars under tomographic constraints*, arXiv `cs/9903020v3` | exact bar tilings and exchange arguments |
| `PA-TPTP` | Chrobak et al., *Tile-Packing Tomography is NP-complete*, arXiv `0911.2567` | translations of one fixed tile and hardness |
| `PA-FS04` | Frosini, Simi, TCS 319 (2004), DOI `10.1016/j.tcs.2004.02.004` | bicolored domino tomography and complexity |
| `PA-FS05` | Frosini, Simi, DAM 151 (2005), DOI `10.1016/j.dam.2005.02.032` | domino reconstruction under structural restrictions |
| `PA-GL20` | Gritzmann, Langfeld, DCG 64 (2020), DOI `10.1007/s00454-020-00180-5` | polyatomic consistency and complexity |
| `PA-DSMR` | Desreux et al., arXiv `math/0302344` | tiling configuration spaces and flips |
| `PA-LOCK` | Tucker-Foltz, *Locked Polyomino Tilings*, arXiv `2307.15996` | pair-removal locking phenomena |
| `PA-GY` | Gross, Yamzon, *Binomial ideals of domino tilings*, arXiv `2008.02896` | toric encoding and move connectivity |
| `PA-SDR` | Fellows et al., *On Solution Discovery via Reconfiguration*, arXiv `2304.14295` | generic repair from infeasible states |
| `PA-EC` | Guruswami, Lin, arXiv `1905.06503` | parameterized hardness of generic exact cover |
| `PA-DS98` | Diaconis, Sturmfels, Ann. Statist. 26 (1998), DOI `10.1214/aos/1030563990` | Markov bases and all nonnegative fibers |
| `PA-ATY` | Aoki, Takemura, Yoshida, arXiv `math/0511290` | indispensable monomials and generators |
| `PA-CTV` | Charalambous, Thoma, Vladoiu, arXiv `1501.05142` | binomial fibers and indispensable binomials |
| `PA-RS` | Rauh, Sullivant, arXiv `1404.6392` | lifting Markov bases and toric fiber products |

## Adjudication

| Result | Source relationship | Public role |
| --- | --- | --- |
| Named one-copy placement/X-ray/coverage model | shaped and typed tiling tomography is prior art | Definition chosen for this paper; no invention claim. |
| Purity, repair, and support hierarchy | implications are elementary; general repair settings are prior art | Organizing proposition with certified strictness witnesses. |
| C32/C46/P49 values | finite outputs for source-attributed specimens | Certified finite propositions at their exact scopes. |
| Translation cap | classical torsion-free sumset mechanism | Self-contained supporting lemma. |
| Active-carrier lemma | nearby sources study related hardness or consistency questions | Core structural lemma under the stated finite semantics; no firstness claim. |
| FPT theorem in `(q,h)` | generic hardness does not contradict the localized parameterization | Sole uniform algorithmic headline at the stated scope. |
| Fiber and radius bounds | finite-state consequences of the active carrier | Corollaries, not sharp-distance results. |
| Participation types | adaptation of bounded-type compression | Supporting decision and compressed-classification result. |
| Energy descent | elementary potential identity and sufficient descent | Explanatory sufficient criterion only. |
| P21 connectivity and lattice statements | general Markov and lattice theory is classical | Frozen-configuration calculations, not a general basis theorem. |

## Contribution boundary

The paper studies a named exact-cover sublocus inside an aggregate tomographic
placement fiber. Its main uniform contribution is the active-carrier lemma and
the resulting FPT decision theorem in the complement area `q` and orientation
bound `h`. The finite libraries make the three predicates non-equivalent; the
P21 example separates fixed-fiber, lattice, and all-RHS Markov connectivity.

This wording describes the contribution without asserting firstness. The paper
does not claim a new general tomography model, a first repair framework, a
sharp repair radius, or a general Markov-basis theorem.
