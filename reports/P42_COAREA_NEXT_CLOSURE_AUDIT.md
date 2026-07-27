# P42 co-area next-closure audit

**Date:** 2026-07-26  
**Input:** owner-supplied external bundle `P42_COAREA_NEXT_CLOSURE` plus the
attached external verdict.  
**Decision:** `ACCEPT_WITH_SCOPE_REPAIRS_NO_CLAIM_PROMOTION`.  
**Public boundary:** unchanged, `PC-1 = P42-C020` only.  
**Purpose:** verify the proposed mathematical sharpening, import only the
parts that survive, and replace the obsolete next-task fork.

**2026-07-26 proof-reconstruction correction.** The mathematical conclusions
below survive, but the unconditional translation-cap statement must include
the empty-translation branch. The canonical repair graph changes exactly two
named placements; `G^(<=2)` is a separate variant. See
`docs/PROOF_RECONSTRUCTION.md`.

## 1. Bottom line

The external agent found three genuine closures and one useful structural
coordinate:

1. the number of translations of a near-spanning piece is bounded by co-area;
2. the full placement fiber improves from the deliberately crude
   `M_L 2^(q^3)` bound to `2^(O(q log q))`;
3. an explicit co-area-only repair-radius bound exists;
4. the implicit all-sublibrary **decision** and compressed-classification
   problems are FPT after exact participation-type compression.

The overlap energy `Phi` gives a clean sufficient descent criterion and a
useful finite explanation of C46 versus P49, but it is not a universal
characterization. P21 and P26 are decisive negative controls.

The bundle's C34 atomization is a good route split, not a solved C34 result.

## 2. Accepted proof: translation cap

For finite nonempty `A,B subset Z^2`, let

```text
D(A,B) = {t : A+t subseteq B}.
```

Then, unconditionally,

```text
|D(A,B)| <= max(0, |B|-|A|+1).
```

Equivalently, if `D(A,B)` is nonempty, then
`|D(A,B)| <= |B|-|A|+1`. In that case the proof is valid. Since
`A+D(A,B) subseteq B`, choose an integer linear functional injective on the
finite sumset. The one-dimensional chain of `|A|+|D|-1` distinct sums gives

```text
|B| >= |A+D| >= |A|+|D|-1.
```

This is a classical torsion-free sumset mechanism, but the included proof is
self-contained. The external OUP source is background, not a theorem
dependency of P42.

The earlier unconditional wording was false when `D(A,B)` is empty and
`|A|>|B|+1`. Every orientation counted below has nonempty `D(A,B)`, so this
repair changes no placement, fiber, runtime or radius bound.

If a piece has at most `h` orientations and co-area `q`, it therefore has at
most

```text
h(q+1)
```

legal placements. Here `h` may count group elements; repeated orientations
only make the bound looser.

## 3. Accepted proof: sharpened fiber and graph bounds

Freeze one canonical largest piece `L`, with

```text
q = |T|-|L|.
```

For each pose of `L`, the previous active-line theorem confines every
participating residual pose to an active carrier `G` with `|G|<=q^2`.
If residual piece `i` has area `a_i`, the translation cap gives at most

```text
h(|G|-a_i+1) <= h(q^2-a_i+1)
```

participating placements. Since the residual pieces are nonempty,
`r<=q` and `sum a_i=q`. Thus

```text
V(E)
 <= h(q+1) h^r product_i(q^2-a_i+1)
 <= h(q+1)(h q^2)^q
 = 2^(O(q log q))
```

for fixed `h`. The `q=0` case is separate and trivial.

The proposed near-linear graph construction also survives, with an explicit
case split omitted from the external report:

- for a residual/residual replacement, choose at most `q^2` named pairs and
  at most `(h q^2)^2` replacement poses;
- for a largest/residual replacement, enumerate the at most `h(q+1)` new
  largest poses and the residual poses in each new active carrier.

With a hash set of fiber nodes this gives

```text
O(V(E) h^2 q^6 poly(|I|))
 = 2^(O(q log q)) poly(|I|).
```

The old `2^(q^3)` statement was correct but is now superseded.

## 4. Accepted proof: radius existence is closed

In a repair-exact fiber, every component contains a tiling. A shortest path
from a node to a tiling is simple and has length at most the component size
minus one. Therefore

```text
rho(E) <= V(E)-1
       <= h(q+1)(h q^2)^q-1.
```

For the declared D4 model:

```text
rho(E) <= 8(q+1)(8q^2)^q-1.
```

This closes the logical question “does some `f(q)` exist?”. It does not close
the useful question: whether a polynomial, linear, or sharp bound exists.

## 5. Accepted with repaired statement: implicit all-sublibrary FPT

The external proof is correct after the following problem contract is made
explicit.

### Input contract

- target and pieces are finite cell lists;
- pieces are nonempty and named;
- the orientation group has order at most `h`;
- selected sublibraries have total area `|T|`;
- `L` is the canonical largest selected name, with a fixed tie order;
- the parameter is an upper bound on `|T|-|L|`;
- the requested output is a decision or a compressed behavior
  classification, not the literal list of all names.

For fixed candidate `L`, its at most `h(q+1)` poses induce a common labelled
carrier

```text
S_L = union_A G_A,
|S_L| <= h(q+1)q^2.
```

The exact participation type of a residual named piece records:

1. its area;
2. for every ordered pose of `L`, its exact participating placement masks on
   `S_L`;
3. the identity of a mask that participates in more than one largest-pose
   scenario.

The number of possible exact types is a function of `(q,h)` only. At most `q`
residual nonempty pieces are selected, so available multiplicities can be
truncated to `q`. Enumerating the type-count vectors and applying the
fixed-selected-set algorithm is therefore FPT after polynomial-time signature
construction.

The candidate loop is polynomial — at worst quadratic in the number of named
pieces if every candidate signature is rebuilt directly — and does not
reintroduce an `N^q` exponent. Eligibility must be restricted according to the
canonical largest-name rule to obtain a duplicate-free classification.

Literal listing is different. A `1 x 2q` target, one named `q`-bar and `N`
named monominoes has `binomial(N,q)` distinct valid named sublibraries. Thus
literal listing is not Total-FPT in general. The present closure proves FPT
decision and compressed classification. A duplicate-free Delay-FPT enumerator
is straightforward from accepted type vectors but has not been implemented in
P42, so it remains an engineering corollary rather than a current artifact.

### Important verifier correction

The external `verify_type_kernel.py` passes, but on C46/P49/P21/P26 every
area-compatible named row has its own behavior vector:

```text
C46 86 -> 86
P49 94 -> 94
P21 880 -> 880
P26 360 -> 360
```

Hence those four checks contain no real type collision and do not empirically
test compression. The general result rests on the proof.

The P42-native verifier adds a non-vacuous synthetic library:

```text
4 distinct named sublibraries -> 1 exact participation-type vector
```

and confirms identical full-fiber behavior. A same-area piece with different
placement masks is separated as a negative control.

## 6. Accepted structural coordinate: overlap energy

For a margin node `x`, let `c_x(u)` be cell multiplicity and define

```text
Phi(x) = sum_u max(c_x(u)-1,0).
```

Because total placed area is `|T|`,

```text
Phi(x)
 = |T|-|union_i P_i|
 = (1/2)||c_x-1_T||_1,
0 <= Phi(x) <= q.
```

Thus `Phi=0` exactly on tilings.

If every non-tiling node has an exact-two-replacement neighbor with strictly
smaller `Phi`, repeated descent reaches a tiling in at most `q` moves.
Therefore this is a valid sufficient criterion for `G^(2)` repair-exactness
with `rho<=q`.

The independently reconstructed finite panel is:

| Library | Fiber | Trapped | Nonzero local minima | Equal? | Max finite radius |
| --- | ---: | ---: | ---: | --- | ---: |
| C46 | `352=344+8` | 0 | 0 | yes | 1 |
| P49 | `1344=1208+136` | 16 | 16 | yes | 1 |
| P21 | `1680=672+1008` | 736 | 792 | no | 2 |
| P26 | `1554=1051+503` | 329 | 343 | no | 3 |

So the useful finite explanation is:

- C32 has no tomographic defects;
- C46 has defects, all immediately downhill-repairable;
- P49 has genuine nonzero energy wells;
- P21/P26 prove that a nonzero local minimum need not be trapped, because
  repair may require a temporary uphill step.

The proposed barrier

```text
beta(x) = min_path_to_tiling (max_y Phi(y)-Phi(x))
```

is therefore a better next coordinate: zero for monotone repair, positive for
activated repair, and infinity for trapped components.

## 7. C34 decision

The current source lock already confirms that C34 has C32's two-hole target,
sixteen polygonal pieces, angles in `{45,90,135}` and some square holes.

The external split is adopted:

- **C34-L:** exact rational transcription and a lattice-aligned
  right-isosceles atom census;
- **C34-G:** proof that unrestricted congruent placements are lattice-aligned,
  or an exact continuous configuration-space exclusion of off-lattice
  solutions.

The co-area transfer to C34-L is conditional. The atom carrier, atom X-ray,
atom co-area and the maximum multiplicity `mu` in a row-column box must be
defined first. Only then does

```text
V <= h(q+1)(h mu q^2)^q
```

follow. Nothing in this audit closes C34-G.

## 8. Prior-art correction

The following are not P42 inventions:

- torsion-free sumset lower bounds;
- pair replacement and isolated/locked polyomino tilings;
- toric/binomial methods for tiling connectivity;
- Delay-FPT/Total-FPT enumeration terminology;
- heterogeneous tile types under tomographic projections.

The defensible possible contribution is narrower:

> co-area kernelization of a named heterogeneous one-copy placement fiber,
> with a coarse aggregate X-ray statistic, an exact-cover sublocus and
> pair-repair predicates.

The exact conjunction still lacks a systematic MathSciNet/zbMATH and citation
graph audit. No novelty claim follows.

Primary links checked during this audit:

- [Locked Polyomino Tilings](https://arxiv.org/abs/2307.15996)
- [Binomial ideals of domino tilings](https://arxiv.org/abs/2008.02896)
- [Parameterized Enumeration with Ordering](https://arxiv.org/abs/1309.5009)
- [A Note on Tiling under Tomographic Constraints](https://arxiv.org/abs/cs/0108010)
- [Tile Packing Tomography is NP-hard](https://arxiv.org/abs/0911.2567)
- [C34 official gallery page](https://www.geomagicsquares.com/gallery.php?page=34)

## 9. Replay and provenance

The external bundle:

```text
verify_all.py                         PASS
16/16 manifest hashes                PASS
JSON parsing                         PASS
translation active-grid checks       44,910, zero violations
```

Its four input hashes match the current in-tree C46/P49/P21/P26 artifacts
byte-for-byte.

The P42-native verifier:

```text
python -X utf8 -B packages\package_e_obstruction_channels\xray_channel\verify_coarea_next.py
```

reports:

```text
3,969 exhaustive small translation pairs, zero violations
44,910 locked active-grid checks, zero violations
energy panel exactly reproduced
4 named synthetic rows -> 1 exact type vector
placement-sensitive negative control separated
```

See `reports/P42_COAREA_NEXT_VERIFICATION.json`.

## 10. Claim-curator decision

No external proposed row is inserted into the authoritative claim ledger.
The correct proposal is split by evidence kind:

- `C086A`: translation cap, proposed `CL5`, classical mechanism;
- `C086B`: sharpened fiber/graph bound, proposed `CL5`;
- `C086C`: radius existence bound, proposed `CL5`;
- `C087`: implicit decision/compressed classification FPT, proposed `CL5`
  under the exact input contract above;
- `C088A`: strict-energy descent theorem, proposed `CL5`;
- `C088B`: four-library energy panel, proposed `CL3`;
- `PO-C34-L`, `PO-C34-G`, `PO-PLACEMENT-MARKOV`: remain `CLO`.

All are promotion-review proposals requiring a maintainer decision. Public
claim set and public wording remain unchanged.

## 11. Changed plan

The previous fork

```text
repair-radius existence  OR  implicit all-sublibrary complexity
```

is obsolete: both decision questions are internally closed.

The next high-value task is now:

```text
placement-coloured quotient + nonnegative component classification
```

For every selected row, compute and compare:

1. `ker_Z[U;X] / <two-piece moves>`;
2. actual nonnegative/squarefree connected components;
3. tilings per component;
4. minimum `Phi` and barrier `beta`;
5. automorphism orbits.

The lattice quotient alone cannot certify connectivity because nonnegativity
may split one lattice class. C34-L is a separate engineering lane and C34-G a
separate geometry gate. Paper preparation remains premature.
