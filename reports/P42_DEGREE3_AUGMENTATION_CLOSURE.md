# P42 robust P21 degree-three augmentation closure

**Date:** 2026-07-26  
**Route:** `P42-E / robust P21 / degree-three augmentation`  
**Decision:** `DEGREE3_AUGMENTATION_CLOSED_FOUR_COMPONENTS_REMAIN`  
**Public effect:** none.

## 1. Outcome

The complete degree-three calculation is closed for the robust P21 row
`(4,5,12,13)`.

Two statements that looked similar before the run must now be separated:

1. repairing every formerly trapped node requires only one of the three
   frozen repair-move orbits;
2. neither those repair orbits nor the complete set of degree-three moves
   connects the 32-node fiber or generates the full participating kernel.

The preregistered branch is
`TWO_PROTOTYPES_REPAIR_THIRD_ADDS_STRUCTURE`. More sharply, the exhaustive
subset table shows that the canonical two prototypes are already more than
is needed for finite repair, while the third orbit is still nonredundant
relative to that particular canonical pair.

## 2. Complete degree-three ceiling

The producer enumerates every primitive support-three relation in the frozen
72-coordinate participating catalogue:

| Changed piece positions | Moves |
| --- | ---: |
| `(0,1,2)` | 96 |
| `(0,1,3)` | 288 |
| `(0,2,3)` | 80 |
| `(1,2,3)` | 468 |
| **total** | **932** |

Under the order-eight target action these form 136 move orbits:

```text
97 orbits of size 8
39 orbits of size 4
```

Adding all 932 moves to the 144 support-two moves gives:

```text
rank K                         60
rank M_<=2                     34
rank M_<=3                     51
free rank K/M_<=3               9
nontrivial torsion              none
```

Therefore support at most three does not generate the participating kernel.
The remaining obstruction is nine-dimensional and free.

The target-invariant quotient-dual rank does collapse from one to zero.
Thus the piece-12 orbit indicator is genuinely killed at degree three, but
the disappearance of that scalar explains only one of the 17 new lattice
directions and does not imply lattice generation.

## 3. Complete `G_<=3` graph

The direct graph on the 32 fiber nodes has:

```text
degree-one edges       0
degree-two edges      16
degree-three edges    48
degree-three orbits    6 x 8
components             4 x 8 nodes
```

Every component contains:

- two tilings;
- two live extras;
- four formerly trapped nodes.

All sixteen formerly trapped nodes therefore reach tilings, but the full
fiber remains split into four components:

```text
C0: tilings 0,27;  trapped 1,3,24,26
C1: tilings 4,31;  trapped 5,7,28,30
C2: tilings 8,19;  trapped 9,11,16,18
C3: tilings 12,23; trapped 13,15,20,22
```

This is a complete negative result for `G_<=3`, not a failed search.

## 4. Exact repair-orbit comparison

The three frozen minimizing repair-pair orbits are:

```text
R0: representative 1 -> 0,  changed positions (1,2,3)
R1: representative 1 -> 27, changed positions (0,2,3)
R2: representative 3 -> 0,  changed positions (1,2,3)
```

Every one of the eight subsets was checked:

| Selected orbits | Added moves/edges | Lattice rank | Free quotient | Components | Trapped reaching tiling |
| --- | ---: | ---: | ---: | ---: | ---: |
| none | 0 / 0 | 34 | 26 | 16 | 0 |
| `R0` | 8 / 8 | 42 | 18 | 8 | 16 |
| `R1` | 8 / 8 | 42 | 18 | 8 | 16 |
| `R2` | 8 / 8 | 42 | 18 | 8 | 16 |
| `R0,R1` | 16 / 16 | 46 | 14 | 4 | 16 |
| `R0,R2` | 16 / 16 | 42 | 18 | 8 | 16 |
| `R1,R2` | 16 / 16 | 46 | 14 | 4 | 16 |
| all three | 24 / 24 | 46 | 14 | 4 | 16 |

Consequences:

- the minimum number of repair-move orbits needed to place every formerly
  trapped node in a tiling component is **one**;
- all three singleton choices work;
- each singleton already kills the old short separator;
- the minimum number of repair orbits needed to reproduce the complete
  `G_<=3` component partition is **two**;
- the exact minimal pairs are `{R0,R1}` and `{R1,R2}`;
- the preregistered canonical pair `{R0,R2}` repairs everything but leaves
  eight components and adds no rank beyond either singleton;
- adding `R1` to `{R0,R2}` raises the lattice rank from 42 to 46 and reduces
  eight components to four, so `R1` is not structurally redundant relative
  to the canonical pair;
- once `R1` is paired with either `R0` or `R2`, the remaining outer orbit is
  redundant for all frozen graph/rank criteria.

The earlier statement that one direct-repair pair orbit does not cover both
trapped-node orbits remains correct at the pair-census level. The stronger
augmentation calculation shows why it was insufficient as a generator
statement: the same move vectors apply at additional fiber nodes and combine
with support-two paths. One move orbit consequently repairs both trapped-node
orbits indirectly.

## 5. Repair graph versus lattice

The three repair-pair orbits contribute only 24 of the 48 degree-three fiber
edges, but they already reproduce the full four-component `G_<=3` partition.
The other three edge orbits do not merge components.

At the lattice level the distinction is real:

```text
all repair orbits: rank 46
all degree-three moves: rank 51
```

Thus non-repair degree-three relations contribute five additional integral
directions even though they do not improve finite-fiber connectivity. This
is the clearest current example in P42 of why graph connectivity, lattice
generation and Markov generation cannot be collapsed into one statement.

## 6. Independent replay

`verify_degree3_augmentation.py` imports neither the degree-three producer nor
the robust-quotient/short-separator producers. It independently rebuilds:

- the 32-node fiber and 72-coordinate catalogue;
- all support-one, support-two and support-three relations;
- Smith kernel coordinates and FLINT rank/SNF;
- the eight target isometries and all move/edge orbits;
- all 24 minimizing repair pairs;
- all eight repair-orbit subsets;
- the complete direct `G_<=3` graph.

Result:

```text
PASS: 11,608 independent checks
6/6 adversarial mutations rejected
support-three moves / full rank / components = 932 / 51 / 4
```

The mutations alter the degree-three count, a move-orbit member, a subset
rank, the complete component count, a separator-killing field and the
interpretation branch.

## 7. What is now closed

Closed for the participating robust P21 fiber:

- the complete primitive support-three move census;
- its target-orbit decomposition;
- the exact `M_<=3` rank and torsion-free quotient;
- the complete `G_<=3` component partition;
- exact minimality within the three frozen repair-pair orbits;
- failure of full degree-three lattice generation and fiber connectivity.

Still open:

- the complete support-four lattice, the last possible support level for
  this four-piece row;
- minimal target-orbit generators merging the four surviving components;
- whether support four generates the full participating kernel integrally;
- any Markov statement for other right-hand sides;
- a uniform support-degree theorem and external novelty.

## 8. Next concrete task

The next finite task should not rerun degree three. It should:

1. enumerate all primitive support-four relations in the same participating
   catalogue;
2. compute `rank M_<=4`, torsion and `K/M_<=4`;
3. decompose the support-four moves into target orbits;
4. identify the smallest target-orbit family that merges the four surviving
   `G_<=3` components;
5. keep the trivial fact that direct `G_<=4` is complete separate from the
   nontrivial integral-generation question.

Estimated difficulty is `3/5` for this final finite support ceiling and `5/5`
for a uniform/all-right-hand-side Markov theorem.

## 9. Nonclaims

- No inactive legal placements or other P21 row.
- No global minimality outside the three frozen repair orbits.
- No support-three Markov or Graver basis.
- No inference from four components to a uniform obstruction.
- No external novelty, public claim, manuscript or release action.

