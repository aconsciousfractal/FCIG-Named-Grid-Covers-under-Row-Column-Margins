# Bounded P21 connectivity case study

Scope: one source-locked P21 row, its participating placement configuration,
and three non-equivalent connectivity questions. This is a bounded case study
at the frozen row and makes no priority claim.

## 1. Why P21 is in the paper

The uniform part of the paper decides support, purity and repair in a selected
one-copy tomographic fiber. P21 is retained because it shows exactly what such
a finite fiber does **not** decide.

For one frozen configuration, three questions must be distinguished:

1. does a chosen move family connect one specified nonnegative fiber?
2. does its integer span equal the complete relation lattice?
3. does it connect every nonnegative fiber of the same matrix, and hence form
   a Markov basis?

The first is a statement about one right-hand side, the second permits signed
intermediate combinations, and the third quantifies over all right-hand
sides while preserving nonnegativity. P21 supplies explicit separations in
both directions needed by the paper:

```text
one fixed fiber connected  does not imply  full lattice generation;
full lattice generation    does not imply  all-RHS Markov connectivity.
```

This is a bounded explanatory example, not a uniform theorem about geomagic
libraries.

## 2. Frozen source and algebraic object

The source-locked specimen is gallery asset `4x4 square target`, signed
`LS 11-02`, with SHA-256
`2248f6e9d0d4cb793ef2ff8069a37ae62ed67629cee6263a0f7071ae4a274120`.
Its target is the `5×5` square. The locked piece library validates all ten
source magic lines under the declared `D4` exact-cover semantics.

We freeze the zero-based piece-index row

```text
E = (4,5,12,13),
```

whose piece areas are `(7,6,6,6)`. The indices are not area labels.

Only placements occurring in the selected margin fiber are retained. Their
counts by named piece are

```text
8, 24, 16, 24,
```

giving 72 participating variables. For each participating placement `P` in
named block `i`, the column of the configuration matrix `A` is

```text
e_i | X_row(P) | X_col(P).
```

Thus `A` has four block-count rows and ten target-margin rows. It is a
`14×72` integer matrix of rank 12, and

```text
K = ker_Z(A)
```

has rank 60.

For `s=1,2,3,4`, let `M_<=s` be the integer span of all squarefree one-copy
relations whose two placement tuples differ in at most `s` named piece
positions. Here *piece support* is not toric degree, Graver support or a
claim of Graver primitiveness.

Let `G_<=s(b)` be the graph induced by those relations on the fixed
nonnegative one-copy fiber `A x=b`. These graphs are deliberately labelled
`G_<=s`: they are not silently substituted for the paper's canonical
exact-two repair graph.

## 3. The fixed one-copy fiber

The chosen fiber contains

```text
32 nodes = 8 exact tilings + 24 non-tiling margin matches.
```

Its complete support filtration is:

| Move family | New relations at this support | Lattice rank | Free rank of `K/M` | Fixed-fiber components | Fixed-fiber verdict |
| --- | ---: | ---: | ---: | ---: | --- |
| `M_<=2` | 144 | 34 | 26 | 16 | 8 tiling components and 8 trapped components; 16 trapped nodes |
| `M_<=3` | 932 | 51 | 9 | 4 | every node reaches a tiling, but the fiber is disconnected |
| `M_<=3 + <O_714>` | one complete target orbit | 54 | 6 | 1 | the fixed fiber is connected |
| `M_<=4` | 7,444 | 60 | 0 | 1 | the 32-node graph is complete |

The move counts in the second column are the relations appearing for the
first time at that exact piece support. Hence the complete `M_<=3` and
`M_<=4` families contain respectively 1,076 and 8,520 relations.

At support at most two, the graph has sixteen edges and sixteen two-node
components. Eight components contain one tiling and one extra. The remaining
eight components contain the sixteen trapped nodes. All 128 differences
between a trapped node and a tiling lie outside `M_<=2`; their separation is
already algebraic, not merely a nonnegativity barrier.

Adding all piece-support-three relations produces four components of eight
nodes, and every formerly trapped node then reaches a tiling. The graph is
repair-exact but not connected. At support four, every pair of the 32 nodes is
an edge, so the graph is complete.

## 4. Fixed-fiber connectivity does not certify the lattice

The order-eight target symmetry partitions the 7,444 support-four relations
into 1,119 complete target-action orbits. Exactly 36 individual orbit modules
connect the four components of `G_<=3`.

For every one of these 36 choices,

```text
rank(M_<=3 + <O>) = 54 < 60 = rank(K),
```

and the quotient remains torsion-free of rank six. The canonical witness is
orbit `O_714`.

**Proposition T-P21-A.** The move family `M_<=3 + <O_714>` connects the fixed
32-node nonnegative fiber but does not generate the participating integer
kernel.

This is the first required separation. A connected graph on one selected
fiber cannot certify that every signed relation of the configuration has
been generated.

## 5. What symmetry reveals about the missing lattice directions

The quotient

```text
Q = K/M_<=3
```

is torsion-free of rank nine. Among the 1,119 support-four target orbits,
there are 87 cyclic orbit modules of quotient rank three. They fall into
three exact integral families of sizes

```text
6, 3, 78.
```

Exactly three complete target-action orbits are necessary and sufficient to
generate `Q` integrally. Every minimum triple contains one orbit from each
family, and therefore the number of minimum triples is

```text
6 × 3 × 78 = 1,404.
```

The canonical triple `(283,603,714)` has determinant `-1` in the stored
quotient basis.

Among these three rank-three families, the fixed 32-node fiber activates

```text
0, 0, 36
```

orbits respectively. It sees no representative of the first two integral
channels. Thus the exact three-orbit calculation is not an ornamental
symmetry census: it explains why inspection of this single fiber misses six
of the nine quotient directions.

**Proposition T-P21-B.** Three complete target-action support-four orbit
modules are exactly minimal for integral generation above `M_<=3`; the fixed
fiber is blind to the first two of the three necessary integral channel
families.

The values `3`, `6,3,78` and `1,404` are configuration-specific finite facts,
not a general invariant-basis theorem.

## 6. Lattice generation does not certify Markov connectivity

The full squarefree one-copy support-at-most-four family satisfies

```text
M_<=4 = K
```

integrally: all 60 Smith factors are one. This permits every kernel vector to
be written as an integer combination of the one-copy relations. It does not
guarantee that those signed combinations can be ordered while remaining
nonnegative.

A Markov basis for `A` must connect every fiber

```text
{x in N^72 : A x=b}
```

for every feasible right-hand side `b`, including block counts larger than
one. The one-copy family fails already in degree two. The complete quadratic
census contains 218 indispensable binomials:

```text
144 cross-block quadrics present in the one-copy family,
 74 within-block quadrics absent from it.
```

A canonical missing quadratic lies in a two-monomial fiber with block count
`(2,0,0,0)`. No one-copy cross-block relation is applicable inside that
fiber, so it remains disconnected.

**Proposition T-P21-C.** Although `M_<=4=K`, the squarefree one-copy
support-at-most-four family is not an all-right-hand-side Markov basis for
the frozen 72-variable matrix.

This is the second required separation. Integer lattice generation does not
imply nonnegative connectivity in every fiber.

## 7. What the Markov certificate does and does not close

A separate two-monomial fiber with block count `(0,0,0,7)` forces an
indispensable binomial of toric degree seven. Therefore every Markov basis of
the frozen matrix has degree at least seven.

The bounded Betti census through degree four is:

| Toric degree | Betti fibers | Minimum generators forced |
| ---: | ---: | ---: |
| 2 | 218 | 218 |
| 3 | 996 | 996 |
| 4 | 5,705 | 5,727 |

Thus at least 6,941 minimal generators are forced through degree four, before
the degree-five through degree-seven layers.

These statements do **not** prove:

- that the Markov degree equals seven;
- any upper bound on the Markov degree;
- a complete or minimal Markov basis;
- a Graver or universal Markov basis;
- blockwise bases or a structured lifting theorem;
- any conclusion for inactive placements, another P21 row or another
  library.

The exact Markov degree, complete basis, four blockwise bases, and structured
lift remain mathematically open and are not manuscript dependencies.

## 8. Evidence and responsibility map

| Statement | Canonical evidence |
| --- | --- |
| P21 source identity and locked geometry | `../packages/package_c_comparative_hypergraphs/specimens/p21_locked.json`, `../packages/package_c_comparative_hypergraphs/specimens/SPECIMENS.md` |
| robust quotient and support filtration | `../packages/package_e_obstruction_channels/xray_channel/robust_p21_quotient.py`, `degree3_augmentation.py`, `support4_ceiling.py` |
| exact orbit minimum | `../packages/package_e_obstruction_channels/xray_channel/verify_minimum_orbit_generators.py` |
| all-RHS no-go and degree-seven lower bound | `../packages/package_e_obstruction_channels/xray_channel/verify_markov_no_go.py` |
| integrated reconstruction | `../packages/package_e_obstruction_channels/xray_channel/verify_orbit_markov_closure.py` |

The source supplies the specimen geometry. The repository supplies the
selected-row restriction, participating configuration, and finite graph,
lattice, orbit, and Betti calculations. Markov bases, indispensable fibers,
equivariant bases, and lifting theory remain prior art as recorded in
`THEOREM_LEVEL_PRIOR_ART_AUDIT.md`.

## 9. Reproduction contract

From the repository root:

```text
python -X utf8 -B packages/package_e_obstruction_channels/xray_channel/verify_orbit_markov_closure.py --xray-dir packages/package_e_obstruction_channels/xray_channel --full --single-block
```

The integrated final verifier reconstructs the 72 columns, all 7,444
support-four relations, the 1,119 target orbits, the rank-nine quotient, the
minimum triples and the Markov obstructions without reading the principal
support-four analysis file.
