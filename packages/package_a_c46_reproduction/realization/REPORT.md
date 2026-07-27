# P42-A realization — report (2026-07-23)

**Outcome: REPRODUCTION.** The 36 source-declared C46 groups all tile the target
(`36/36`, certificate each), and the remaining 50 quaternes are all decided — 8
positive, 42 negative — so all 86 carry a certificate. `PO-GMR-04` and `PO-GMR-05`
close; `P42-C020` is met by a certified finite result. **No public claim is
promoted here.**

## Result

| quantity | value | how established |
| --- | --- | --- |
| additive quaternes `\|H_34\|` | 86 | forced count (not a result) |
| realize `\|R\|` | **44** | certified: 44 positive + 42 negative, 86/86 |
| of the 36 source-declared | **36/36 tile** | all 9 declared balanced-direction families realize (`structure.py`) |
| remaining 50 | 8 tile, 42 do not | closed exact-cover certificates both sides |
| split families | **0** | `R` = 11 whole balanced-direction families exactly |
| `R ⊆ affine core` | yes, 44/44 | every realizing family is a balanced-direction family |

## Certificates and verification

- `certify.py` → `R_certificates.json`, sha256
  `37250629b284ae76ae5db3b606958239679b9253d1848cdfdce26fed2172d115`, byte-stable,
  re-generation byte-identical.
- **Independent second engine** `verify.py` (own D4/placement/exact-cover, re-derived
  from the locked pieces+target): **86/86, 0 failures → R = 44.** Positives checked for
  D4-congruence + containment + exact partition of `T`; negatives by an independent
  exhaustive exact-cover returning 0.
- **Verifier soundness** `mutation_test.py`: six perturbations all rejected (each
  branch — congruence, partition, area, refutation — exercised), two controls pass.

## What this closes

- **`PO-GMR-04`** (C46 geometric reproduction, "the one that matters most"): every one
  of the 36 declared groups has an exhibited placement that tiles `T`. The certificate
  minimum is met in full including the `Aut(T)` declaration (§5 of `PREREGISTRATION.md`;
  `Aut(T)` = Klein-4).
- **`PO-GMR-05`** (decide the remaining 50): all decided with certificates on both
  sides — no `unknown` remains. The negatives are closed exact-cover trees, not solver
  statuses (lock §7).
- **`P42-C020`** (`CLO`): satisfied by a certified finite result, exactly the
  `CLO → CL5` promotion condition ("reconstructed pieces, applied isometry, disjointness
  and union-equals-target checks"). Promotion to `CL5` is an owner-gate action.

## Structural finding (feeds `PO-GMR-07`, not claimed here as a law)

On C46, realization respects the affine coset structure exactly: `R` is 11 whole
balanced-direction families, `R ⊆` the 52 affine, **0 split**. The 2 non-realizing
balanced directions are `[0,2,8,10]` and `[0,7,10,13]` — the latter the pure
broken-diagonal direction, matching the source's "most-perfect but not panmagic"
caption (`P42-C035`).

**Source-display boundary observation.** `R` (44) exceeds the 36 displayed
groups by exactly **two whole balanced-direction families** —
`[0,3,9,10]` and `[0,6,10,12]`, 8 quaternes — that tile
`T` but are not among the source's 36 panels. This decides the sharpest part of
`PO-GMR-05`'s note (the undeclared affine quaternes): 8 of the 16 undeclared affine
quaternes realize, 8 do not. The source does not assert that its display is
exhaustive, so this is **not an erratum claim**. It is a P42 census observation
about C46, not a general law (the falsifiers for the affine-selection law live
in `P42-C`/`P42-B`; the
generality question was separately explored — see the exploratory note below).

## Guardrail compliance

- `86` and `52` are named as forced counts, claimed of nothing.
- "Source-declared → certified" happens only now, via these certificates.
- Negatives are closed exact-cover trees (lock §7), independently re-run — never a
  solver status. `Φ` is not consulted (`P42-C041`).
- No statement about C32/C34; no most-perfect general theorem (`BLK-02`).

## Exploratory context (scratch, CL0 — not part of this closure)

Beyond C46, three related items were explored in scratch and are recorded for the owner,
**not** promoted: (a) two further specimens (P21 generic, P26 panmagic+most-perfect) whose
realization is NOT coset-pure, showing purity is not a universal law; (b) a controlled
transport of this certified `R` across all 880 normal magic arrangements — **affine-normal
⟹ coset-purity, 432/432 exceptionless**, while distinct areas alone do not imply it (232
split); (c) `im_Z(A_36)=im_Z(A_52)` (Smith `1^11·2`) — the additive lattice is blind to the
declared/realized split, a candidate `P42-E` negative control. These need their own
source-locks, preregistration and gating before any promotion.
