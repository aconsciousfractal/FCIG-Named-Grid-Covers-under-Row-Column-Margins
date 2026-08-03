# Co-area residual-state analysis method

**Method frozen:** 2026-07-26, before running the co-area implementation.

## Objective

Decide whether the already proved bound

```text
support(coverage - 1_T) <= 2q,
q = |T| - area(largest selected piece),
```

can be upgraded to a genuine bounded algorithm for the placement-coloured
one-copy model.  The desired output is a theorem-level algorithm or a precise
failure, not another classifier fitted to C32, C46 and P49.

The selected lane is co-area alone.  Strip width is deliberately not added as
a parameter unless the co-area argument fails.

## Locked model

Input consists of:

- a finite grid target `T`;
- nonempty named pieces whose total area is `|T|`;
- a fixed finite orientation group followed by translations;
- one legal placement per named piece;
- the row-and-column X-ray map;
- the 2-replacement fiber graph: adjacent nodes differ in exactly two named
  placements.

Choose and freeze one largest named piece `L`, put
`q = |T| - |L|`, and treat ties by a deterministic piece-index rule.

The three predicates remain:

```text
support-exact:  F_E nonempty iff T_E nonempty
fiber-pure:     F_E = T_E
repair-exact:   every 2-replacement component of F_E meets T_E
```

## Predeclared lemmas and algorithm

### L1 — active-line lemma

Fix a legal placement `P` of `L` and set
`b = X(T) - X(P)`.  The positive coordinates of `b` occur on at most `q`
rows and at most `q` columns.  Every placement of a residual piece that can
participate in a margin match must:

- be componentwise bounded by `b`;
- use only those active rows and columns;
- therefore lie in an active grid of at most `q^2` cells.

### L2 — bounded residual state space

There are at most `q` residual pieces.  For fixed `P`:

- margin feasibility is decidable by a named-piece dynamic programme with at
  most
  `prod_j (b_j + 1) <= (q + 1)^(2q)` margin states;
- exact tiling is decidable by a named-piece subset dynamic programme on the
  `q` cells of `T - P`, with at most `2^q` coverage states;
- every residual placement is a subset of the active grid, so there are at
  most `2^(q^2)` distinct placements per residual piece and at most
  `2^(q^3)` complete residual placement tuples.

### T — predeclared FPT conclusion

For a fixed finite orientation group, support-exactness and fiber purity are
fixed-parameter tractable in co-area `q`.  The full 2-replacement fiber can
also be enumerated in `f(q) * poly(input size)` time, so repair-exactness and
maximum finite repair radius are fixed-parameter tractable in `q`.

A deliberately loose explicit bound is:

```text
support decision:
  O(M_L * S * (q + 1)^(2q))

tiling decision:
  O(M_L * S * 2^q)

full fiber and naive graph:
  O(M_L^2 * q * 2^(2q^3))
```

where `M_L` is the number of legal placements of the frozen largest piece and
`S` is the total number of residual placement records inspected.  Legal
placements themselves are polynomially enumerable from grid-cell input by
anchoring an oriented piece cell to a target cell.

The theorem is about parameterised decidability.  These worst-case bounds are
not claimed to predict the practical runtime on C32, C46 or P49.

## Frozen computational tests

The same implementation must be run without feature tuning on:

| Library | Required classification |
| --- | --- |
| C32 | support-exact, fiber-pure, repair-exact |
| C46 | support-exact, not fiber-pure, repair-exact |
| P49-base | not support-exact, not fiber-pure, not repair-exact |

Required exact cross-checks against the independently established fibers:

```text
C32: 20 margin-feasible rows; 136 = 136 + 0 fiber nodes
C46: 44 margin-feasible rows; 352 = 344 + 8 fiber nodes
P49: 61 margin-feasible rows; 1344 = 1208 + 136 fiber nodes
```

The implementation must also record, for every fiber row:

- co-area `q`;
- active row count, active column count and active-grid size for each largest
  placement participating in a match;
- observed margin-state count versus the L2 bound;
- support, purity and repair verdicts.

## Independence and mutations

1. The principal implementation may reuse locked input parsers but not stored
   support/purity verdicts.
2. A second verifier must reconstruct legal placements, residual states and
   expected classifications without importing the principal implementation.
3. Mutations must include:
   - deleting one required residual placement;
   - inserting an illegal/out-of-target placement;
   - changing one target cell;
   - corrupting one stored co-area or active-grid bound;
   - corrupting one expected library verdict.

Every mutation must be rejected or change the computed result in the
predeclared direction.

## Pass, partial and fail conditions

**PASS** requires proofs of L1, L2 and T plus exact agreement on all three
locked libraries, independent replay and mutation rejection.

**PARTIAL** is used if support/purity FPT survives but the repair graph bound
or verifier does not.

**FAIL** is mandatory if any of the following occurs:

- a participating residual placement uses an inactive line;
- a residual state exceeds the declared bound;
- the residual algorithm disagrees with a locked exact fiber;
- correctness requires adding a feature chosen after seeing C32/C46/P49;
- the complexity contains an exponent depending on `q` applied to the input
  size rather than only to an `f(q)` factor.

Failed formulations remain recorded rather than being silently discarded.
