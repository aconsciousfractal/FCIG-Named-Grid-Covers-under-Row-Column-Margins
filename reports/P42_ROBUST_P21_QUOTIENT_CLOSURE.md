# P42 robust P21 degree-at-most-two quotient closure

**Date:** 2026-07-26  
**Decision:** `ROBUST_P21_ALGEBRAIC_SEPARATION_CLOSED_DEGREE3_REPAIR`.  
**Public boundary:** unchanged; `PC-1 = P42-C020` only.  
**Paper action:** none.

## 1. Verdict

The unique P21 row that remains mixed tiling/trapped under moves of support at
most two, `(4,5,12,13)`, is now exactly classified.

The mechanism is **not** another nonnegative hole:

> All 16 robust trapped nodes lie in participating quotient classes disjoint
> from every tiling. Their separation is already algebraic in
> `K_E^part / M_E^(<=2)`.

Consequently no integer path made from one- and two-piece moves can connect a
trapped node to a tiling, even if arbitrarily negative intermediate
coordinates are allowed. Cone depth `gamma` is therefore undefined for these
pairs, not infinite.

Nevertheless every trapped node has a direct degree-three repair:

```text
rho(z) = 3 for all 16 trapped nodes.
```

This is the robust higher-support obstruction that the previous
`(0,1,2,3)` target failed to provide.

## 2. Exact participating quotient

For the 32-node fiber:

```text
participating placements by named piece    8, 24, 16, 24
participating columns                      72
constraint rows                            14
rank K_E^part                              60
primitive support-one moves                 0
primitive support-two moves               144
rank M_E^(<=2)                             34
free rank of K/M                           26
nontrivial torsion factors                  none
```

Torsion absence is a statement about this one participating witness only.

The nonnegative and quotient partitions agree exactly on the hit set:

```text
G_<=2 edges                         16
G_<=2 components                    16
hit quotient classes                16
split hit quotient classes           0
mixed tiling/trapped classes         0
maximum components per hit class     1
```

Every component and every hit quotient class has two nodes. There are:

- eight live classes, each containing one tiling and one repairable
  non-tiling node;
- eight trapped classes, each containing two trapped non-tiling nodes.

Thus the participating quotient is neither too coarse nor too fine on these
32 actual nodes: its hit classes coincide with the complete `G_<=2`
components.

## 3. Exhaustive algebraic separation

There are `16 × 8 = 128` trapped/tiling differences. The independent verifier
tests every one against a Hermite column basis for the complete primitive
support-at-most-two move lattice.

Result:

```text
differences in M_E^(<=2)       0 / 128
algebraically separated        128 / 128
```

The producer reaches the same classification using Smith coordinates. No
trapped node has a tiling in its quotient class, so no pairing or cone-depth
path is selected post hoc.

This distinguishes the two P21 mechanisms sharply:

| Row | `G_<=2` status | Algebraic relation to tilings | Correct mechanism |
| --- | --- | --- | --- |
| `(0,1,2,3)` | repaired by degree 1 | paired in the `G_2` quotient | exact-degree artefact plus cone hole |
| `(4,5,12,13)` | 16 nodes remain trapped | all 128 differences outside `M_<=2` | robust algebraic separation |

## 4. Direct repair degree

For every trapped node, all eight tilings were compared exhaustively. The
complete distribution is:

```text
rho=3: 16 nodes
rho=4:  0 nodes
```

Because the complete graph contains every endpoint pair differing in one or
two names, `rho>=3` also follows from trapping. The explicit tiling
comparisons give `rho<=3`.

The order-eight target action organizes the finite result as follows:

```text
tiling-node orbits                 1 orbit of size 8
trapped-node orbits                2 orbits of size 8
minimum repair pairs              24
minimum repair-pair orbits         3 orbits of size 8
```

The first trapped orbit has two minimizing tilings per node, producing two
repair-pair orbits. The second trapped orbit has one minimizing tiling per
node, producing the third orbit.

Three representative minimum repairs are stored:

```text
trapped 1 -> tiling 0:  pieces {5,12,13}
trapped 1 -> tiling 27: pieces {4,12,13}
trapped 3 -> tiling 0:  pieces {5,12,13}
```

One prototype cannot repair both trapped-node orbits because the target
action preserves those two orbits. Two prototypes suffice to give at least
one degree-three repair for every trapped node. The third prototype is the
second optimal repair choice for the first trapped orbit.

## 5. What is concrete now

The P21 repair landscape has been reduced to two fully explicit mechanisms:

1. **degree-one X-ray collision**, responsible for the collapsed
   `(0,1,2,3)` witness and the vanished `beta=4` barriers;
2. **degree-three algebraic jump**, responsible for the robust
   `(4,5,12,13)` failure.

For the robust row, support-at-most-two connectivity is not blocked by
nonnegativity after lattice equivalence. The lattice equivalence itself is
absent. This is a cleaner obstruction and requires no unbounded integer-state
search.

The result remains a finite participating-placement statement. It is not a
Markov basis for all legal placements or right-hand sides.

## 6. Revised next tasks and difficulty

### A. Short dual separators — next mathematical task, difficulty 3–4/5

The quotient has free rank 26, far too large to be an explanation. Extract
short primitive integer linear functionals that:

1. vanish on all 144 support-two moves;
2. are constant on each `G_<=2` component;
3. separate the eight trapped classes from all tiling classes;
4. compress into target-action orbits;
5. determine whether one small family, rather than 26 arbitrary Smith
   coordinates, explains the separation.

This is the shortest path from a computation to an interpretable invariant.

### B. Degree-three augmentation — finite closure, difficulty 2–3/5

Add the three minimum repair-pair orbits as candidate support-three
generators and determine:

- which two orbits are necessary and sufficient to repair all 16 trapped
  nodes;
- whether `G_<=3` becomes connected or merely repair-exact;
- how the quotient rank and hit classes collapse;
- whether a smaller non-symmetric generator set suffices.

The node census already proves that two target-orbit prototypes are necessary
to cover both trapped-node orbits and sufficient for direct repair. It does
not yet prove a lattice/Markov minimality statement.

### C. Uniform support-degree theory — difficulty 5/5

Characterizing the minimum support needed to connect arbitrary
placement-coloured X-ray fibers, or bounding it sharply in co-area, remains a
uniform research problem. The present witness supplies a clean degree-three
finite test, not a theorem.

### D. P26 compression — difficulty 4/5

P26 still has 200 robust trapped nodes inside tiling rows spread over 87
mixed rows and no target symmetry. It should follow only after the P21 dual
separator/degree-three mechanism is understood.

## 7. Independent verification

Producer:

```text
python -X utf8 -B packages\package_e_obstruction_channels\xray_channel\robust_p21_quotient.py
```

Independent replay:

```text
python -X utf8 -B packages\package_e_obstruction_channels\xray_channel\verify_robust_p21_quotient.py
```

The verifier imports neither producer nor the previous quotient
implementation. It rebuilds:

- all 72 participating coordinates;
- all primitive support-one and support-two relations;
- a Hermite column basis for exact membership;
- independent Smith invariant factors in saturated kernel coordinates;
- the direct all-pairs graph;
- all 128 trapped/tiling lattice non-memberships;
- all 128 direct repair degrees;
- target actions, node orbits, class actions and repair-pair orbits.

Current result:

```text
1,134 independent checks
6/6 adversarial mutations rejected
```

The finite robust-row task is closed. No authoritative claim or public
wording is changed.
