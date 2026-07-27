# Output T — theorem-level primary-source audit

Date: 2026-07-26  
Gate: `T-03`  
Verdict: **CLOSED FOR NO-FIRSTNESS RELEASE-CANDIDATE WORDING**  
Candidate claim set: exactly the scoped rows in `CLAIM_LEDGER.md`

## 1. What this gate does and does not certify

This audit answers a narrower and more useful question than “is the paper
new?”:

> For each result in the frozen theorem spine, what is imported, elementary,
> configuration-specific, or still a defensible paper contribution after
> direct comparison with the closest primary sources?

The gate is closed for release-candidate drafting because every headline has a
source-aware role and a safe wording boundary. It is **not** a priority
certificate. In particular:

- a negative search is not evidence of firstness;
- MathSciNet, zbMATH and the complete post-publication citation forests were
  not available;
- Tracy Chin's 2019 thesis now has a direct author-page and Brown institutional
  the later Gross–Yamzon paper, but its full interior was not acquired;
- public novelty adjectives remain prohibited without a separate owner gate
  and a fresh publication-stage source audit.

## 2. Primary-source comparison set

The following are the load-bearing comparison sources. “Direct” means that
the publisher text, arXiv text/PDF, or an author/institutional full text was
read rather than inferred from a citation snippet.

| ID | Primary source and locator | Direct content used here |
| --- | --- | --- |
| `PA-CCDW` | Chrobak, Couperus, Dürr, Woeginger, *A Note on Tiling under Tomographic Constraints*, arXiv `cs/0108010`, abstract and model/results | several tile types, row/column projections by type, reconstruction and NP-completeness |
| `PA-DGRR` | Dürr, Goles, Rapaport, Rémila, *Tiling with bars under tomographic constraints*, arXiv `cs/9903020v3`, full text | exact bar tilings/packings under projections and exchange arguments |
| `PA-TPTP` | Chrobak, Dürr, Guíñez, Lozano, Thang, *Tile-Packing Tomography is NP-complete*, arXiv `0911.2567`, Definition 1 and Theorem 1 | pairwise-disjoint translations of one fixed tile; NP-complete for every nonbar tile |
| `PA-FS04` | Frosini, Simi, *The NP-completeness of a tomographical problem on bicolored domino tilings*, TCS 319 (2004), DOI `10.1016/j.tcs.2004.02.004`, publisher text | exact bicolored domino tilings reconstructed from horizontal/vertical projections; NP-completeness |
| `PA-FS05` | Frosini, Simi, *The reconstruction of a subclass of domino tilings from two projections*, DAM 151 (2005), DOI `10.1016/j.dam.2005.02.032`, full publisher text, especially Theorem 11 | exact anonymous domino tilings; strip complexity degree; polynomial reconstruction through degree four |
| `PA-GL20` | Gritzmann, Langfeld, *On Polyatomic Tomography over Abelian Groups*, DCG 64 (2020), DOI `10.1007/s00454-020-00180-5`, §§1–2 and Theorems 2.1–2.2 | colored matrix entries with per-color row/column group sums; consistency and complexity |
| `PA-DSMR` | Desreux, Matamala, Rapaport, Rémila, *Domino tilings and related models: space of configurations of domains with holes*, arXiv `math/0302344`, abstract/full text | distributive lattice of exact tilings and connectivity by flips |
| `PA-LOCK` | Tucker-Foltz, *Locked Polyomino Tilings*, arXiv `2307.15996`, definition and main constructions | exact tilings isolated under removal/recombination of a pair of tiles |
| `PA-GY` | Gross, Yamzon, *Binomial ideals of domino tilings*, arXiv `2008.02896`, Theorems 3.8 and 4.3 | toric/binomial encoding of exact domino tilings and move sets connecting tiling spaces |
| `PA-SDR` | Fellows et al., *On Solution Discovery via Reconfiguration*, arXiv `2304.14295`, framework definition and abstract | feasible-solution discovery from an infeasible/corrupted state by restricted small modifications |
| `PA-EC` | Guruswami, Lin, *Parameterized Inapproximability of Exact Cover and Nearest Codeword*, arXiv `1905.06503`, problem statement/main lower bound | generic `k`-ExactCover is W[1]-complete/hard in solution size |
| `PA-DS98` | Diaconis, Sturmfels, *Algebraic Algorithms for Sampling from Conditional Distributions*, Ann. Statist. 26 (1998), DOI `10.1214/aos/1030563990`, Theorem 3.1 | Markov bases are the toric-ideal move sets connecting every nonnegative fiber |
| `PA-ATY` | Aoki, Takemura, Yoshida, *Indispensable monomials of toric ideals and Markov bases*, arXiv `math/0511290` | indispensable monomials/binomials and minimal Markov generators |
| `PA-CTV` | Charalambous, Thoma, Vladoiu, *Binomial fibers and indispensable binomials*, arXiv `1501.05142` | binomial fibers and indispensable-generator criteria |
| `PA-RS` | Rauh, Sullivant, *Lifting Markov Bases and Higher Codimension Toric Fiber Products*, arXiv `1404.6392` | lifting Markov bases along lattice maps and structured fiber-product context |

Supporting source maps and frozen locators remain in
`PRIOR_ART_TOMOGRAPHY.md`,
`../reports/P42_COAREA_FPT_PRIOR_ART_LOCK.md` and
`../reports/P42_ORBIT_MARKOV_SOURCE_LOCK.json`.

## 3. Adjudication matrix

The relation vocabulary is:

- **import** — the surrounding theorem or concept is source-owned;
- **elementary specialization** — correct and useful here, but not a novelty
  axis;
- **finite certified result** — P42 owns a source-locked computation for one
  frozen library/configuration;
- **candidate contribution** — the exact theorem-level conjunction was not
  found in the closest direct sources, without implying priority;
- **case-study application** — known general theory applied to one certified
  configuration.

| Spine item | Closest direct prior art | Relation and collision | Safe role after audit | Risk |
| --- | --- | --- | --- | --- |
| `T-DEF` named one-copy placement/X-ray/coverage model | `PA-CCDW`, `PA-DGRR`, `PA-FS04/05`, `PA-GL20` | Tomography of shaped/typed pieces and row/column consistency are known. The exact conjunction “one named copy, aggregate cell X-ray, overlaps allowed in the relaxed fiber, exact cover as a sublocus” was not located. | Definition chosen for this paper; describe the distinction, never claim invention of tiling tomography. | medium |
| `T-HIER` purity ⇒ repair ⇒ support | `PA-SDR`, `PA-LOCK`, classical implication logic | Repair from infeasible states is a known general framework; pair-locked tilings are known. The implications themselves are immediate from the definitions. | Organizing proposition plus certified strictness witnesses. The taxonomy is useful exposition, not a headline theorem of abstract novelty. | low |
| strictness via C32/C46/P49 | no external source can own the frozen P42 certificates; surrounding objects are source-attributed | The values and components are finite, library-specific facts. | Finite certified propositions at the exact candidate scopes, without priority wording. | low if attribution is retained |
| `T-TRANS` translation cap | classical torsion-free sumset inequality | The proof mechanism is classical; the corrected empty branch is bookkeeping. | Self-contained supporting lemma only. | low |
| `T-ACTIVE` active rows/columns/cells after fixing a largest piece | `PA-TPTP`, `PA-EC`, `PA-GL20` | Nearby work studies hard tiling tomography, generic exact cover, or “small/large matrix” polyatomic consistency. None gives this largest-piece-complement localization for the named aggregate-X-ray relaxation. | Core structural lemma and main technical contribution candidate. No firstness wording. | medium |
| `T-FPT` support/purity/exact-two-repair decision in `(q,h)` | `PA-TPTP` hardness; `PA-EC` W[1]-hardness in solution size; generic FPT/subset-DP methods | Generic hardness does not contradict the theorem because `q` bounds the active carrier after a largest pose is fixed. No parameter-preserving source collision was found for the exact three-predicate problem. | **Only algorithmic headline.** State as an FPT theorem for the frozen finite-cell-list model, not as the first FPT theorem in tomography. | medium/high until publication-stage citation-forest audit |
| fiber/radius bound | finite-state counting; `PA-SDR` supplies only the general repair setting | The explicit bound follows from the active-carrier proof; it is conservative and not a sharp-distance theorem. | Corollary of `T-FPT`, not a separate novelty headline. | low |
| `T-TYPE` exact participation types and multiplicity truncation | standard bounded-type compression and parameterized-enumeration distinctions | The proof is an adaptation of standard finite-type/multiplicity truncation once the active carrier is bounded. | Supporting algorithmic proposition. Claim the exact contract and output-sensitivity separation, not a new general compression paradigm. | medium/low |
| `T-ENERGY` overlap potential and strict descent | generic potential-function arguments; `PA-SDR` general repair context | The identity is elementary and strict descent is a standard sufficient argument. | Explanatory sufficient criterion and finite-panel diagnostic only. | low |
| C32/C46/P49 foundational block | tiling-tomography sources own the surrounding class | Counts and graph classifications are source-locked finite outputs, not laws of arbitrary tilings. | Foundational certified section needed to make the abstract predicates concrete. | low |
| P21 fixed-fiber connectivity and lattice generation | `PA-DSMR`, `PA-GY`, `PA-DS98` | Exact tiling connectivity and toric/fiber connectivity are known; lattice generation is not Markov connectivity. | Configuration-specific separation and certificate. | low |
| P21 orbit minimum and channel split | equivariant/lifting literature, including `PA-RS` | General equivariant Markov/lattice machinery is known. The `3` and `6,3,78` values are frozen-configuration results. | Bounded case-study proposition, not a general invariant-basis theorem. | low |
| P21 all-RHS Markov no-go and degree ≥7 | `PA-DS98`, `PA-ATY`, `PA-CTV` | The method and language are classical. The missing 74 quadrics and degree-seven witness are configuration-specific. | Case-study application showing that fixed-fiber/lattice success does not imply all-RHS Markov connectivity. | low |

## 4. The contribution boundary after red-team reduction

The paper does **not** rest on the novelty of any single generic ingredient.
The defensible contribution is:

1. a precise named one-copy exact-cover problem embedded as a sublocus of an
   overlap-permitted aggregate-X-ray fiber;
2. three explicitly separated decision predicates—support, purity and
   exact-two repair—made non-equivalent by certified finite libraries;
3. the active-carrier lemma for a fixed pose of a largest selected piece;
4. the resulting FPT decision theorem in the complement area `q` and
   orientation bound `h`, with explicit state and radius bounds;
5. an exact bounded P21 example separating fixed-fiber connectivity, integral
   lattice generation and all-right-hand-side Markov connectivity.

Only items 3–4 should be presented as the main uniform mathematical
contribution. Items 1–2 provide the model and theorem question; item 5 marks
the algebraic boundary.

The strongest honest one-sentence positioning is:

> We study a named exact-cover sublocus inside an aggregate tomographic
> placement fiber and prove that support, purity and exact-two repair are FPT
> when parameterized by the complement area of a largest selected piece and
> the orientation bound.

This is contribution wording, not priority wording.

## 5. Wording lock

### Admissible

- “We introduce the following named-placement relaxation for the purposes of
  this paper.”
- “The closest tiling-tomography models impose disjointness in their feasible
  objects and use different supply/projection semantics.”
- “For this finite-cell-list model, the three predicates are FPT in `(q,h)`.”
- “The active-carrier lemma localizes every residual participating placement
  after a largest pose is fixed.”
- “Our certified C32/C46/P49 examples show that the three predicates do not
  collapse.”
- “The P21 calculation is a bounded example of the gap between fixed-fiber,
  lattice and all-RHS Markov connectivity.”

### Forbidden

- “We introduce tiling tomography with heterogeneous pieces.”
- “This is the first repair framework for infeasible combinatorial states.”
- “Pair replacement / locked tilings are new.”
- “This is the first FPT algorithm for tomographic reconstruction.”
- “No previous work studies this model” or “the model is novel” based only on
  the absence of a search hit.
- “The taxonomy is a new general theorem.”
- “Exact participation types are a new parameterized-complexity technique.”
- “The energy criterion characterizes repairability.”
- “P21 yields a new general Markov-basis theorem.”

## 6. Material changes to the plan

1. `T-FPT`, with `T-ACTIVE`, remains the sole uniform headline.
2. `T-HIER` is demoted from “conceptual foundational headline” to an
   organizing proposition whose value is the strict certified witness chain.
3. General “repair from a relaxed/infeasible state” language must cite
   `PA-SDR`; P42 owns only the exact tomographic instance and theorem.
4. Frosini–Simi is no longer an unread high-risk interior. Its full publisher
   text confirms exact domino-tiling reconstruction with a structural
   strip-degree parameter, not an overlap-permitted margin fiber or repair
   radius.
5. `T-TYPE` and `T-ENERGY` remain in the paper only as supporting propositions.
6. P21 stays bounded exactly as decided; no exact Markov-basis work reopens.
7. `T-04` is closed in `FOUNDATIONAL_SECTION.md` and `T-05` is closed in
   `P21_CASE_STUDY.md`; `T-06` and `T-07` are now closed, and the next
   concrete gate is `T-08`, the mathematical and documentary red team.

## 7. Residual source risk

| Residual gap | Consequence | Handling |
| --- | --- | --- |
| Tracy Chin 2019 thesis interior not acquired | possible earlier algebraic tiling formulation broader than the author-page description | cite Gross–Yamzon for the published connectivity collision; reacquire Chin only before public submission |
| complete journal/citation forests not traversed | exact model or parameter may occur outside titles/abstracts | no firstness language; repeat audit at public gate |
| MathSciNet/zbMATH unavailable | reduced systematic backward/forward coverage | no priority claim |
| terminology “co-area” may not be standard for this parameter | search recall may be weak | define `q` mathematically and search by the formula/semantics at public gate |
| model conjunction may be rediscovered in application literature | medium residual collision risk for `T-DEF` | make `T-ACTIVE/T-FPT`, not the bare definition, carry the paper |

## 8. Gate disposition

`T-03` is closed because:

- every spine item has a primary-source comparison and a role;
- the two new collisions found in this pass—Frosini–Simi on domino
  tomography and Fellows et al. on generic infeasible-state repair—have been
  incorporated;
- the contribution sentence and forbidden firstness wording are frozen;
- the unresolved source gaps do not block a **no-firstness release candidate** when
  no priority claim is made.

The gate must be reopened before public release if the abstract,
introduction, title or cover letter uses “new model”, “first”, “novel”, “no
previous work”, or an equivalent priority claim.
