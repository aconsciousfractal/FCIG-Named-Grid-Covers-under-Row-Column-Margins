# Prior-art audit — the tomographic spine (Phase 3)

**Date:** 2026-07-26 · **Gate:** the novelty gate for `C066`–`C082` and Output T `T-03` ·
**Method:** targeted audits plus direct reads of the load-bearing primary sources.
**Status of the public claim set: UNCHANGED — `PC-1` only.** Nothing here promotes anything.

> **Standing rule (PAPP): a negative search is NOT a priority certificate.** Every "no prior art
> found" below is bounded by the coverage gaps in §8, which are stated in full.

---

## 1. The object, stated precisely enough to be audited

Fix a finite target `T ⊂ Z²`. Fix a finite **heterogeneous library of named, pairwise-distinct
polyomino pieces**, **one named copy of each**. Each piece has legal placements in `T` under `D4`.
For a sublibrary `E` (areas summing to `|T|`) compare

- the **projection fiber** `F_E` = one placement per piece of `E`, whose **aggregate cell**
  row+column line sums equal those of `T` (overlaps *permitted*);
- the **exact-cover locus** `T_E ⊆ F_E` = those that actually partition `T`.

Questions: **(Q1) support-exactness** `F_E ≠ ∅ ⟺ T_E ≠ ∅`; **(Q2) fiber structure** — components
under the 2-piece swap, repairable vs trapped, repair radius; **(Q3) how many directions**;
**(Q4) a bound on trapped-deviation support**.

---

## 2. The map of the territory (the single most useful output of this audit)

> **Polyatomic tomography gives types WITHOUT shapes. Tile-packing tomography gives shapes
> WITHOUT types. Chrobak–Couperus–Dürr–Woeginger 2003 already gives BOTH AT ONCE.**

So **"a heterogeneous library of shaped pieces measured by row/column margins" is NOT a new
object.** It was published in 2001/2003. What CCDW does *not* have, and what remains:

| axis | CCDW 2003 | ours |
| --- | --- | --- |
| supply | tile **types** = colours, **unlimited copies** | **named pieces, exactly one copy each** |
| what the projections count | **tiles of each type** per line (richer data) | **cells**, aggregated over all pieces (poorer data) |
| isometries | **translations only** (rotations explicitly declined) | full `D4` |
| covering | **packing** by default (needn't cover) | **exact cover** of `T` |
| question | **complexity** of reconstruction (NP-completeness) | **existence equivalence** + fiber structure |

**The structural fact that matters most.** In *every* model in this literature — CCDW's
`T`-tiling ("disjoint and contained in `G`"), Chrobak–Dürr–Guiñez–Lozano–Thang's packing
("pairwise disjoint"), Dürr–Goles–Rapaport–Rémila's *tillable* ("partitioned into"), Sevenster's
Battleships — **disjointness is built into the definition of a solution.** The
directly read closest models therefore do not supply a relaxed feasible set to
compare against the exact-cover locus. The exact `F_E` conjunction — margins
matched, overlaps allowed, one named copy — was not located in those sources.
This is a bounded source comparison, not a claim that nobody has defined it
anywhere. In CCDW's model our question cannot be asked without changing the
feasible-object semantics.

**Two branches that never meet.** Everything in tiling-tomography (CCDW; Dürr et al.; Chrobak et
al.; Frosini–Simi; Picouleau) is **complexity classification**. Everything in switching-component
theory (Ryser; Gérard; Dulio–Frosini) is about **0/1 arrays**, single lattice sets, no pieces.
**Our contribution, if it survives, is the bridge between those two branches — not the object and
not the margins, which already exist.**

---

## 3. Verdicts, claim by claim

| claim | verdict | basis |
| --- | --- | --- |
| **`C066`/`C073`** support-exactness of C46 | **NO PRIOR ART FOUND** for existence-equivalence on a heterogeneous one-copy library — but the **question type is classical** | structural argument in §2; ancestry = Ryser/Gale–Ryser (the `k=1` shadow: for the 1×1 tile, projection-feasibility ⟺ realizability) and **DGRR Thms 1–2** (necessary condition proved sufficient, for uniform bar margins) |
| **`C074`/`C082`** repairable vs trapped fibers, repair radius, fiber graph | **Exact projection-fiber version not located; general repair framing is KNOWN.** Fellows et al. (arXiv `2304.14295`) formalize solution discovery from infeasible/corrupted states by restricted modifications; Tucker-Foltz gives pair-locked exact tilings. Claim only the exact tomographic instantiation and certified component/radius results. | DGRR's exchange is a proof device; Thurston/Rémila and Gross–Yamzon study valid tilings; Ryser interchanges arrays; Fellows et al. own the general infeasible-to-feasible reconfiguration paradigm |
| **`C075`/`C078`** `τ_D`, uniform ceiling | **KNOWN — and the governing theorem is KATZ (1977), not Gardner–Gritzmann** | ⚠️ *Correction applied 2026-07-24 after the 4th audit thread:* "four valid directions determine every subset of a rectangle" is **NOT a theorem** — it conflates two results. **Gardner–Gritzmann** (TAMS 349, 1997, Thm 5.7) is about **convex** subsets of **unbounded** `Z²`. The result governing a **box** is **M. Katz (1977)**, restated as Hajdu–Tijdeman Thm 1: with `M=Σ\|a_d\|`, `N=Σ\|b_d\|`, the zero-line-sum space has **`dim ker = (m−M)(n−N)`** if `M<m, N<n`, else **0** — the kernel is the multiples of `P_S = ∏(x^{a_d}y^{b_d}−1)` that fit in the box. Our rank-36 is exactly this: our set has `N = 6 = n` **at equality**, and the switching atom needs a `4×7` window — one row taller than our box. **Our 4-set is not even minimal:** `{c, r+2c, r+3c}` (three directions) already gives rank 36. The same four directions **fail on 7×7** (kernel 4) — so "four" was never the operative parameter, as we suspected |
| **`C076`** toric/Markov backbone | **KNOWN — demote to a worked instance** | Ohsugi–Hibi 1999 Thm 1 (chordal bipartite ⟺ quadric-generated) + Reyes–Tatakis–Thoma 2012 Thm 4.14 (4-cycle binomials indispensable ⟹ our 176 are the **unique** minimal basis) + Sturmfels GBCP Prop. 8.11 (unimodular ⟹ circuits = Graver = universal GB) + Villarreal (bipartite circuits = even cycles). The Ohsugi–Hibi ⟺ structural-zeros bridge is explicit in Hara–Takemura–Yoshida |
| **`C079`** co-area bound | **no prior art found, but it is ELEMENTARY** | two-line counting; claim it as a lemma, never as a theorem |
| **`C081`** lattice-invisible fission | **AUDITED 2026-07-24 → the lattice half is a ROUTINE COROLLARY; only the group chain + the external-selector question survive** | Fourier duality on `F_2^4`: `rank_Q` = a covering count in **PG(3,2)**; the 13 balanced directions are exactly the **13 lines disjoint from a frame**, covering 11 of 15 points, with **coverage multiplicity min 3** — so dropping 2 families cannot change the lattice (**forced in two lines**). Only **7 of 13 families** already generate it (751 such 7-subsets), so `A_44` has **four families of slack**; the `Z`-vs-`Q` gap first opens at k=4. Not C46-specific either: **#balanced = 13 ⟺ gnomon-magic ⟺ the 432**, all sharing `(12, 11, (1¹¹,2))`. Ambient design = **S(3,4,16)**, `F_2` code **RM(2,4)** dim 11 — SNF is a special case of **Chandler–Sin–Xiang** (Trans. AMS 358, 2006). Slogan retired (it is the ambient content of the **Hamada/Tonchev** p-rank programme). **Surviving and unclaimed:** an *external geometric criterion* selecting blocks + which invariants detect it — **NO PRIOR ART FOUND** |
| **`C020`/`PC-1`** the 44/86 realization | **safe — see §5** | Sallows publishes **36** for this square, not 44 |

### 3b. Co-area FPT update — 2026-07-26

The preregistered follow-up to `C079`/`C082` proves internally that, per
selected named grid-piece set, support-exactness, fiber purity and
2-replacement repair-exactness are FPT in
`q = |T| - area(largest selected piece)`. The new ingredient is an active-grid
kernel: after fixing the large pose, every margin-participating residual pose
lies in at most `q^2` cells.

The targeted boundary check adds:

- **Chrobak–Dürr–Guíñez–Lozano–Thang**, arXiv:0911.2567: fixed non-bar
  tile-packing tomography is NP-complete, but has no near-spanning named-piece
  parameter;
- **Guruswami–Lin**, arXiv:1905.06503: generic Exact Cover parameterised only
  by the number of selected sets is W[1]-complete/hard, so the bounded
  residual universe—not merely the number of pieces—is essential;
- **Ashok–Kolay–Misra–Saurabh**, COCOON 2015,
  DOI `10.1007/978-3-319-21398-9_43`: geometry alone does not make
  `k`-ExactCover FPT.

No matching largest-piece-complement formulation was found in the targeted
search. This is **not** a priority verdict. The subset-DP ingredients are
standard, and systematic MathSciNet/zbMATH/citation-graph coverage is still
missing. The theorem-level Output T audit closes the source-positioning gate
for a **no-firstness release candidate**: `T-ACTIVE/T-FPT` are the uniform
contribution candidates, while no firstness wording is allowed. Priority
remains unknown. See `THEOREM_LEVEL_PRIOR_ART_AUDIT.md`.

### 3c. Co-area sharpening and repair prior art — 2026-07-26

The next-closure audit improves the fiber bound to `2^(O(q log q))`, proves an
explicit co-area-only radius bound and gives FPT decision/compressed
classification for the implicit library by exact participation types. These
are internal theorem candidates, not novelty-cleared claims.

The framing must now cite and distinguish:

- **Tucker-Foltz**, arXiv:2307.15996: locked polyomino tilings are isolated
  states under pair recombination, so pair-replacement obstruction is not a
  new bare phenomenon;
- **Gross–Yamzon**, arXiv:2008.02896: tiling connectivity via binomial/toric
  ideals is known;
- **Chrobak–Couperus–Dürr–Woeginger**, arXiv:cs/0108010: heterogeneous tile
  types under tomographic projections are known;
- **Creignou et al.**, arXiv:1309.5009: Total-FPT and Delay-FPT are standard
  parameterized-enumeration categories;
- **Fellows et al.**, arXiv:2304.14295: solution discovery from an
  infeasible/corrupted state by restricted reconfiguration is a known general
  framework;
- classical torsion-free sumset bounds: the translation cap mechanism is not
  itself a novelty axis.

The defensible contribution positioning is the full conjunction
`named one-copy + near-spanning + aggregate X-ray + exact-cover sublocus +
pair repair + co-area`, with `T-ACTIVE/T-FPT` carrying the uniform theorem and
without a priority claim.

### 3d. Participating quotient and nonnegative split — 2026-07-26

The preregistered placement-coloured follow-up computes

```text
K_E^part / M_E^(2)
```

on placements that actually occur in a fixed squarefree fiber. Its decisive
P21 witness has eight hit quotient cosets but sixteen graph components; every
coset contains one tiling singleton and one trapped singleton. This is a
finite, named-placement instance of the standard algebraic-statistics warning
already locked in §6b: lattice generation does not imply connectivity inside
a nonnegative fiber.

The bare phenomenon is therefore not a novelty axis. The narrower possible
contribution is:

- an explicit coarse-X-ray, one-copy, heterogeneous placement model;
- a quotient/nonnegative-component separation with paired tiling/trapped
  representatives;
- the additional minimax energy barrier `beta`, which distinguishes
  zero-barrier plateaux, activated repair and trapped components.

The current computation is restricted to the participating placement
catalogue. It is not a Markov basis for all legal placements or all
right-hand sides. No priority conclusion follows. See
`reports/P42_PLACEMENT_QUOTIENT_CLOSURE.md`.

**Sharpening of `C076` we should adopt (better than what we had).** Chordal-bipartiteness here is
not luck: **all 630 two-cell deletions** from the `6×6` grid are chordal bipartite (an induced
`2k`-cycle needs `k(k−2)` structural zeros: 3 for `k=3`), and the bound is **tight** — exactly
**2400** of the 7140 three-cell deletions break it, and `2400 = C(6,3)²·3!` = precisely the
transversals of a `3×3` subgrid. So *"removing 2 cells cannot raise the Markov degree"* is a
theorem with a two-line proof; *"removing a few cells cannot"* is **false**, with a minimal
counterexample at 3. (Our 176 and 58 200 were independently reproduced; they also **pin down `T`**:
the two deleted cells must lie in distinct rows and distinct columns — deleting two from one row
gives 180 and 54 780.)

---

## 4. Citations we may not omit

1. **Chrobak, Couperus, Dürr, Woeginger**, *On tiling under tomographic constraints*, TCS
   **290**(3):2125–2136, 2003 (arXiv `cs/0108010`) — **the object with both shapes and types**.
   Highest collision risk on the *object*.
2. **Gross & Yamzon**, *Binomial ideals of domino tilings*, Discrete Math. **344**(11):112530,
   2021 (arXiv `2008.02896`) — already does "tilings as a Markov-basis fiber". Highest collision
   risk on the *method*. They use the **fine** statistic (cell coverage), under which
   `fiber = tiling set` exactly, so they cannot express our gap. **Must be cited and distinguished.**
3. **Dürr, Goles, Rapaport, Rémila**, *Tiling with bars under tomographic constraints*, TCS
   **290**(3):1317–1329, 2003 — the logical **ancestor** of our question type (necessary condition
   proved sufficient).
4. **Ryser** (1957) / **Gale–Ryser** — the `k=1` shadow of Q1, and the origin of switching.
5. **Ohsugi–Hibi** (J. Algebra 218, 1999) + **Reyes–Tatakis–Thoma** (Adv. Appl. Math. 48, 2012) +
   **Sturmfels** GBCP Prop. 8.11 — all of `C076`.
6. **Gardner–Gritzmann–Prangenberg** (TCS 233, 2000) and **Gale–Ryser** — the home of the
   "fiber non-empty, sublocus empty" phenomenon. **Frame Q1's failure side here, not in algebraic
   statistics.**
7. **De Loera–Onn** (JSC 41, 2006; SIAM J. Optim. 17, 2006) — universality: once slacks are added,
   our fiber is a no-3-way-interaction fiber, so *disconnection is the expected generic behaviour*.
8. **Diaconis–Sturmfels** (Ann. Statist. 26, 1998), Remark 3.4 + §4 — the 2-way-yes/3-way-no
   dichotomy ("*alas, the chain they generate is not connected*").
9. **Sallows**, *Geometric Magic Squares*, Math. Intelligencer **33**(4):25–31, 2011 (**not** "vol
   23" — Wikipedia's typo) + the gallery; **Cameron** (2011) for the group-action abstraction with
   both layers (representatives partitioning `T`, and the cardinality **shadow**).
10. **Chandler–Sin–Xiang** (Trans. AMS **358**, 2006, 3537–3559) — SNF of points vs `r`-flats of `AG(n,q)`, covering our `AG(4,2)` 2-flats; plus
    **Hamada** (Hiroshima Math. J. 3, 1973), **Assmus–Key** *Designs and Their Codes* (CUP 1992), **Wilson** (EJC 11, 1990), **Tonchev** (JCTA 42, 1986) /
    **Jungnickel–Tonchev** (DCC 51, 2009) for the p-rank / same-invariant-different-design programme — the correct home of `C081`'s framing.
11. **Hara–Takemura** (Contemp. Math. 516, 2010) §3.4 — 0-1 fibers and the Latin-square sublocus:
    the closest precedent for "a distinguished sublocus needs different moves".

---

## 5. The Sallows collision — checked directly, and it clears

Sallows **does** go beyond the declared lines and **does** count: gallery p.24 says *"Besides rows,
columns and diagonals, 4×4 geomagic squares **often** contain many other quadruplets of pieces that
are able to tile the target. **Here there are 44**."* We must not claim priority for "looking
beyond the lines" or for "counting the 4-subsets that tile", and must cite pp. 3, 24, 28, 43.

**But the numerical collision is only apparent, and the lead verified the decisive plate directly:**

- p.24's square is **self-interlocking with 16 equal-area pieces**, so the additive condition is
  **vacuous**: his 44 is out of `C(16,4)=1820`.
- **Our square is gallery p.46** (its central panel is signed **LS 4-09**). Its "More Info" key
  (`Key plus Ziggurat-key.jpg`, read directly) displays **36** letter-quadruples — exactly the "36
  source-declared groups" this project has always cited. **For our square Sallows publishes 36, not
  44**, and the p.46 caption gives no count of extra quadruples.
- Ours is **44 out of the 86 additively admissible** subsets. The extra
  `44 − 36 = 8` (two whole direction families) is a P42 census finding among
  groups not displayed by the source; because the source does not assert
  exhaustiveness, it is not an erratum claim. The ratio 44/86 is not reported
  in the located literature.

**Nearest genuine precedent for the additive-vs-realization comparison:** gallery p.3, credited to
**Meltem Ceylan** — *"If the combined area of any set of three or more distinct pieces is 15, then
they tile the target"* — a complete additive-vs-realization audit of a normal `3×3`, with verdict
**"no gap"**. Our project is the same question with the opposite answer. **Cite it.** Also p.43
("Aztech"): his published data contains a 52-of-80 realization gap he never names.

**Serious mathematical follow-ups to Sallows 2011: essentially none** (citations are dominated by
mathematics-education articles and popular expositions). The advances are amateur and non-journal.

---

## 6. Two attacks a referee will make — answers prepared

**Attack 1: "Your `F_E ∖ T_E` is just a generalized switching component (Ryser). Doesn't classical
switching theory already force your answer?"**

*Answer.* No — it supplies the **ambient**, not the **selection**. Classical theory says any
deviation `ℓ = coverage − 1_T` lies in the kernel lattice of the margin map: for our `T` that is
dimension **23**, spanned by **176** switches (this *is* `C076`, and it is KNOWN). It says nothing
about which of those elements are **realizable by placements of the given named pieces**. The
piece structure cuts that ambient down enormously: on C46 only **8** deviations are realized, all
single switches; and the **1-piece move graph has ZERO edges** (`C082`) — with three placements
frozen, a replacement would need an identical margin vector. The contribution is the selection, and
the selection is what the classical theory cannot see. *(We adopt the switching-component framing
explicitly in the write-up rather than waiting to be told.)*

**Attack 2: "Isn't this a routine variation of Gross–Yamzon?"**

*Answer.* They choose the **fine** statistic (`Ax = 1`, cell coverage), under which — as they state
— `T_R = F(T)`: the fiber **is** the tiling set, so no gap, no repair radius, nothing to study. Our
gap exists precisely because we **drop cell coverage** and replace it with `(U, X_D)`: one-copy plus
**aggregate** margins. That is one sentence from their setup and must be stated as such, honestly —
the novelty is the **coarseness of the sufficient statistic**, plus named heterogeneous pieces,
which they do not have (dominoes are anonymous graph edges).

**A third caution we adopt unprompted.** Tile-packing tomography is NP-hard for every non-bar tile,
and CCDW prove NP-completeness for small tile sets. A **general** "equal margins ⟹ differ by one
switch" theorem over arbitrary libraries would be a very strong structural claim in that landscape.
It is not formally contradicted (fiber *connectivity* is compatible with NP-hard *consistency*), but
every such statement of ours must stay **library-specific** — which our flagship framing already is.
Relatedly: our trapped components are precisely CCDW's consistency phenomenon, so **trapped fibers
are expected, not anomalous** — P49's value is as a clean separating witness, not as a surprise.

---

## 6b. The hardest finding: a general switching theorem would be FALSE — and we never claimed one

A fifth audit thread went further than prior art and **attacked the mathematics**, building explicit
counterexamples where 2×2 switches fail to connect a margin fiber (e.g. the 12 Latin squares of
order 3 as a fiber with 12 isolated components). It concluded that *"the 2×2 switch is not the atom
once ≥3 labels are present"* and that a general switching theorem is refuted.

**That conclusion is correct — and it targets a claim P42 does not make. Two model differences and
one discipline point, all verified in-tree:**

1. **Its margins are PER TYPE; ours are AGGREGATE.** Its witnesses fix each type's own row/column
   margins (making the fiber exactly a **no-three-way-interaction** 3-way table, which is where the
   De Loera–Onn/Aoki–Hara–Takemura negative results bite). Our `X_D` sums cells over **all** pieces
   (`fiber_graph.py`, `xray()`): one 12-vector for the whole configuration. Strictly **poorer** data,
   hence *larger* fibers — so disconnection is, if anything, **more** expected for us, not less.
2. **Its witnesses are PACKINGS with empty cells; ours are EXACT COVERS** of `T`.
3. **Every P42 statement of this kind is already library-specific or conditional.** `C074` is about
   *C46's* deviations; **`Theorem 1` in `TOMOGRAPHIC_RESOLUTION.md` is explicitly conditional**
   ("*If* every margin-match … *then* any oblique closes"); Lemma H is a statement about the ambient
   lattice, not about connectivity. **We have never asserted that switches connect fibers in
   general.**

**Far from refuting us, this thread independently reproduces our own `C082`:** we found and
documented trapped components ourselves — P49 has a margin-feasible quaterne with **8 matches in 8
isolated components and no tiling**, plus a second quaterne that tiles yet carries a trapped
component. Its "479 of 7889 fibers disconnected" is the same phenomenon in its own model.

**What we adopt from it (high value):**
- A **published reason** why our results must stay library-specific: basic moves are *not* a Markov
  basis for no-three-way-interaction when two dimensions exceed 2 (Aoki–Hara–Takemura 2012 Ch. 9),
  and no bounded move set suffices in general (De Loera–Onn 2006). **Guardrail: never state a
  general "equal margins ⟹ one switch" theorem.**
- A **sanity test we pass**: Gritzmann–Langfeld (DCG 2020) leave *uniqueness* for the 2-atom problem
  **open**. A general switching theorem would settle it; we claim nothing of the sort.
- A **second sanity test**: a Ryser-style normal-form proof would yield polynomial consistency,
  contradicting NP-hardness (Dürr–Guiñez–Matamala) unless P=NP. Our proofs are finite verifications
  on a fixed library, not normal-form arguments — so we are not in that trap.
- Attribution corrections: *Regular switching components* is **Gérard** (TCS 2019), not Frosini
  et al.; the DCG polyatomic paper is **Gritzmann–Langfeld**, not Alpers–Gritzmann.

**Net effect: our claims survive unchanged, and we gain the citations that explain why they must be
scoped the way they already are.**

### 6b-bis. Four further corrections and one positive argument (4th thread, applied)

- **Terminology trap — invert our usage.** In this literature **"valid" set of directions means
  switching components EXIST** (i.e. *non*-determining). We had been using "valid" for the
  opposite. Get this backwards in a write-up and a referee pounces. Use **Katz condition** /
  *invalid* (= determining) with the source's polarity.
- **Sharp adversarial fact about our own direction set.** `{(1,0),(0,1),(1,2),(1,3)}` has cross
  ratio **exactly 3** — one of Gardner–Gritzmann's five *excluded* values. So our set **passes Katz
  and fails GG's criterion**: the two theorems give **opposite verdicts on our own example**. That
  is the strongest possible demonstration that they are different theorems. (Careful: GG's
  cross-ratio condition is necessary-for-a-U-polygon, so this means their certificate does not
  apply, not that a U-polygon exists — our atom's 12 points are not in convex position.)
- **CCDW already contains our atom, twice, unnamed.** A "bad tiling" with one block's row
  projections and another's column projections, and Figure 6's caption *"The last two tilings have
  the same projections."* **A referee will find this** — cite it ourselves, first.
- **A positive argument we should use, not a hedge: the flip literature is transverse, not prior
  art.** Thurston (*Conway's tiling groups*, 1990), Saldanha–Tomei et al., Freire–Klivans–
  Milet–Saldanha: connectivity there is over **all** tilings of a region, obstructed by
  **topological** invariants (flux, twist), never tomographic. And a domino flip turns two
  horizontal pieces into two vertical ones — **if the pieces are named types, the flip changes the
  margins**. The flip graph and the margin-fiber are **transverse structures on the same vertex
  set**. State it that way.
- **The closest archetype for our trapped components, and it is not in tomography:**
  **Jacobson & Matthews**, *Generating uniformly distributed random Latin squares*, J. Combin.
  Designs **4**(6):405–437 (1996) — they relax to "improper" states with one `−1` cell to fix
  irreducibility, then **prove every improper state reaches a proper one**. *They had to rule out
  exactly our failure mode, and never named it.* Also: **Markov-basis fiber graphs cannot exhibit
  our phenomenon by construction** (every vertex is already a valid table), so a *relaxed* state
  space is required — which is precisely what is understudied. The one framework that puts a move
  graph on **all** configurations, feasible and infeasible, is **solution discovery via
  reconfiguration** (Fellows et al., ECAI 2023, arXiv 2304.14295), and it has **never characterised
  that graph's components**. That is our defensible niche.

## 7. What we may and may not say

**May say** (at the weakest sufficient level, library-specific, with §4 citations):
- C46 is **support-exact** and **repair-exact** (radius 1) but **not fiber-pure**; P49 separates the
  three levels with explicit witnesses (`C082`). The logical hierarchy is elementary and generic
  repair is prior art; P42 owns the frozen taxonomy application and certificates.
- The **placement-colored model** `(U, X_D)` indexing placements of **named** pieces with a one-copy
  block stacked on an aggregate X-ray block. The exact conjunction was not located in the closest
  direct sources; do not call it the first or a new general model.
- The `44/86` realization hypergraph of C46, certified (`PC-1`), and the 8 undeclared families.

**May NOT say:** that heterogeneous shaped pieces with row/column margins is a new object (CCDW);
that generic repair from infeasible states is new (Fellows et al.); that "tilings as a
Markov-basis fiber" is new (Gross–Yamzon); that the *question type*
"necessary condition proved sufficient" is new (DGRR, Ryser); that the empty-sublocus phenomenon is
new (Gale–Ryser, GGP); that `C076` is a result (Ohsugi–Hibi et al.); that the direction-count
ceiling is a theorem of ours (classical 4-direction results); that we discovered looking beyond the
declared lines (Sallows p.24), or the additive-vs-realization comparison (Ceylan, p.3).

---

## 8. Coverage gaps — declared

1. **DGRR §5+ CLOSED `R-DIRECT` 2026-07-26.** The full arXiv primary PDF
   `cs/9903020v3` was read. §5 is exactly the **sub-grid domino** reconstruction problem and proves
   strong NP-hardness by a reduction from 3-colour consistency. §6 gives two necessary conditions
   for the unrestricted bar problem (unit-bar relaxations and separated-rectangle tileability)
   and exhibits examples showing they are not sufficient. This strengthens the complexity
   guardrail but does **not** define our overlap-permitted placement fiber, named one-copy pieces,
   repair graph or support-exactness question. The highest-risk unread-section flag is removed.
2. **Frosini–Simi 2004/2005 CLOSED `R-DIRECT` 2026-07-26.** The publisher
   full text for DAM 151 (2005), DOI `10.1016/j.dam.2005.02.032`, was read.
   It defines strip-based complexity degree for an exact anonymous domino
   tiling and proves polynomial reconstruction through degree four (Theorem
   11). The TCS 319 (2004) publisher record, DOI
   `10.1016/j.tcs.2004.02.004`, fixes the bicolored exact-tiling
   reconstruction/NP-completeness semantics. Neither source defines an
   overlap-permitted margin fiber, exact-cover sublocus, pair-repair graph or
   repair radius.
3. **Tracy Chin**, *A Computational Commutative Algebra Approach to Tilings* (Brown, 2019) — the
   Gross–Yamzon reference most likely to generalize beyond dominoes. Bot-walled. **Obtain.**
4. **Journal versions unread** (arXiv preprints used): CCDW's TCS version is retitled and may differ.
5. **arXiv search is metadata-only** — a paper containing our construction in §4 with neither phrase
   in its abstract is invisible to every zero-result query above. **The biggest hole in the negatives.**
6. **zbMATH/MathSciNet inaccessible; Semantic Scholar rate-limited** — the review literature and
   post-2012 citation forest are largely unchecked.
7. **Sallows' Dover 2013 book (144 pp.) unread**; the *Intelligencer* article is paywalled (our
   reading rests on the site's verbatim intro/appendix).
8. **Statistical-mechanics domino literature (flip/height functions, flip *distance*)** not audited —
   flagged as the most likely site of an independent rediscovery of our swap.
9. **`C081` audited 2026-07-24** — verdict above. Residual thin spots from that audit: MathSciNet/zbMATH still inaccessible; Henrich's magic-square pages (closest expository prior art for the 13 partitions) unreachable (DNS + archive blocked), known only from snippets; pre-1990 recreational corpus (Frénicle 1693, Dudeney 1917, Andrews) unsearched, where the 13-directions observation most plausibly originates.
10. **Frosini & Simi** (DAM **151**:154–168, 2005; precursor *Reconstruction of low degree domino
    tilings*, ENDM **12**:94–105, 2003; and TCS **319**:447–454, 2004 bicolored) — **CLOSED
    `R-DIRECT` 2026-07-26.** The DAM publisher full text confirms that their
    **"degree of a domino tiling" is a structural
    parameter of a SINGLE tiling** — *"the complexity degree of the tiling is calculated by
    partitioning each tiling into strips-like subtilings"* — used to **parametrise a reconstruction
    algorithm** (degree 2 generalised to degrees 3 and 4). It is **not** a local move, **not** a
    repair radius, and **not** a fiber structure; there is no relaxed set.
    Their objects are also anonymous dominoes (or 2 colours), not a named
    heterogeneous library.
11. **Ghiglione CLOSED `R-DIRECT` 2026-07-26.** The full 185-page TUM dissertation
    (`mediatum.ub.tum.de/1453778`, official PDF) was acquired and searched. It gives a complete
    algebraic characterization of switching components for finite lattice sets/multisets
    (Theorem 3.1.7: toric-ideal membership), the Hajdu–Tijdeman pure-product representation,
    size constructions and number-theoretic applications. It contains no tilings, polyominoes,
    named pieces, Markov/fiber repair graph or relaxed-vs-exact-cover sublocus. Verdict:
    **the ambient X-ray-kernel language is decisively prior art; the placement-selected subfiber
    remains outside the thesis's object.**
12. **Vedhanayagam & Krithivasan**, LNCS 3992 (2006) — reconstruction with **three named tile
    types**; judged algorithmic from the title only. That is inference, not verification.
13. Two agents hit their WebSearch caps; one caught the PDF summarizer **fabricating** theorem
    numbers and a quote twice (both corrected from primary text) — a reminder that agent output was
    itself verified, not trusted.

---

## 9. Bottom line

The tomographic spine **survives the audit, smaller and better placed**. The
object, margins, exact domino reconstruction, general infeasible-state repair
and tiling move connectivity are not ours. The exact coarse-statistic
relaxation conjunction was not located, but the paper should be carried by
the active-carrier/FPT theorem rather than by novelty of the definition. The
support/purity/repair hierarchy is an organizing proposition with certified
non-collapse witnesses, not an abstract novelty headline. `C076` remains
known, `C078` is classical, and the question type is attributed to
DGRR/Ryser.

`T-03` is closed for the no-firstness candidate in
`THEOREM_LEVEL_PRIOR_ART_AUDIT.md`. Before any novelty or priority claim,
obtain Tracy Chin's thesis and audit
the remaining journal/citation forests for the exact placement-selected
subfiber and co-area parameter. Frosini–Simi, DGRR and Ghiglione are now
closed by direct reading; `C081` is audited and demoted. **`PC-1` remains the
only public claim.**
