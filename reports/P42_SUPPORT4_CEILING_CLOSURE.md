# P42 robust P21 support-four ceiling closure

**Date:** 2026-07-26  
**Row:** zero-based P21 `(4,5,12,13)`  
**Scope:** 72 participating named placements and the fixed 32-node fiber  
**Producer:** `support4_ceiling.py`  
**Independent verifier:** `verify_support4_ceiling.py`  
**Branch:** `SUPPORT4_GENERATES_KERNEL_ONE_ORBIT_CONNECTS`

## 1. Verdict

The last possible support level for this four-piece row is closed.

Inside the frozen 72-coordinate participating catalogue:

```text
primitive support-four moves       7,444
target-action move orbits          1,119
rank K                                60
rank M_<=3                            51
rank M_<=4                            60
K/M_<=4                           trivial
nontrivial torsion                    none
```

Thus the complete primitive support-at-most-four family generates the entire
integer kernel of the participating configuration.

On the fixed 32-node fiber, direct `G_<=4` is the complete graph, as it must be
for four named positions. More sharply, 64 support-four move orbits occur on
degree-four fiber edges, and exactly 36 individual orbits each connect the
four components left by `G_<=3`.

These are two different statements. A single connecting orbit does **not**
generate the kernel: every minimum one-orbit connector raises the lattice
rank only from 51 to 54 and leaves free quotient rank six.

## 2. Complete support-four census

The producer enumerated all

```text
8 * 24 * 16 * 24 = 73,728
```

assignments containing one participating placement in each named piece
position. They split into 44,669 aggregate-X-ray buckets, with maximum bucket
size 32.

The bucket census is:

```text
same-X-ray unordered assignment pairs      44,596
pairs changing every one of four positions  7,444
deduplicated primitive moves                 7,444
deduplication collisions                         0
```

Every admitted vector has four `-1` and four `+1` entries, satisfies all
piece-count and aggregate row-column constraints, and belongs to the frozen
72-coordinate kernel. The deterministic compact move-set digest is:

```text
bceea7b5671bc45e8a970dff0c73c5b9b2a63ca31fc2656a53c0158e9875179c
```

The order-eight target action partitions the 7,444 moves as:

```text
742 orbits of size 8
377 orbits of size 4
total: 1,119 orbits
```

Closure under all eight target actions was checked for every move.

## 3. Final participating lattice

The complete support filtration is now:

| Ceiling | New primitive moves | Lattice rank | Free rank of quotient | Nontrivial torsion |
| --- | ---: | ---: | ---: | --- |
| support at most two | 144 | 34 | 26 | none |
| support at most three | 932 | 51 | 9 | none |
| support at most four | 7,444 | 60 | 0 | none |

All 60 Smith factors at the final ceiling are one. Therefore

```text
M_<=4 = K
```

integrally, not merely over the rationals and not merely up to finite index.

This statement is stronger than finite-fiber connectivity but narrower than
a Markov-basis theorem. It says that every integral kernel vector in this
participating configuration is an integer combination of the enumerated
primitive moves. It does not say that such a combination can be ordered while
remaining nonnegative in every fiber.

## 4. Direct graph ceiling

The direct all-pairs graph census is:

| Exact changed-position degree | Edges |
| --- | ---: |
| 1 | 0 |
| 2 | 16 |
| 3 | 48 |
| 4 | 432 |
| **total** | **496** |

Since `binomial(32,2)=496`, `G_<=4` is the complete graph on the 32 nodes.
This verifies the expected combinatorial ceiling directly.

The 432 degree-four edges use 64 of the 1,119 support-four move orbits:

```text
44 active orbits contribute 8 fiber edges each
20 active orbits contribute 4 fiber edges each
```

Relative to the four fixed `G_<=3` components, they divide into three exact
types:

```text
36 orbits: induce K_(2,2), hence connect all four base components
20 orbits: induce only edges (C0,C1) and (C2,C3)
 8 orbits: act internally and merge no base components
```

The 36 singleton connectors are the orbit IDs

```text
714-728, 908-918, 1015-1021, 1086-1088.
```

Therefore the exact minimum number of fiber-active target move orbits needed
to connect the fixed fiber is one, and there are 36 minimum choices.

## 5. Canonical minimum connector

The lexicographically first minimum choice is move orbit `714`. It contains
four moves. Its representative compact move is:

```text
negative coordinates: (0,21,43,68)
positive coordinates: (2,14,47,56)
```

On the fiber it contributes exactly four edges:

```text
(0,8), (4,19), (12,27), (23,31).
```

On the four `G_<=3` components these induce:

```text
(C0,C2), (C0,C3), (C1,C2), (C1,C3),
```

which is a connected `K_(2,2)`. Hence this one orbit makes the 32-node graph
connected.

Its lattice effect is:

```text
rank M_<=3                         51
rank after adjoining orbit 714     54
remaining free quotient rank        6
nontrivial torsion                none
```

All 36 singleton connectors have the same rank-54, torsion-free profile.
Consequently:

- one target orbit is exactly minimal for this fiber's connectivity;
- one target orbit is provably insufficient for kernel generation;
- the full 7,444-move support-four family is needed for the result
  `M_<=4=K`, although no minimal lattice-generating orbit family is claimed.

This is the decisive red-team distinction. Reporting only that one orbit
connects the graph would hide six remaining lattice directions. Reporting
only that all support-four moves generate the kernel would hide how little is
needed for this particular finite fiber.

## 6. Independent replay

The verifier imports neither the support-four producer nor any earlier
producer. It independently reconstructs:

- the 32-node fiber and all 72 participating coordinates;
- the integer kernel through a separately built Smith transform;
- all primitive moves of support one through four by assignment buckets;
- the eight target isometries and all 1,119 support-four move orbits;
- the complete Smith data for `M_<=3` and `M_<=4`;
- all 496 graph edges and the four-to-one component merger;
- every active orbit and all minimum connecting subsets through cardinality
  three.

Result:

```text
PASS: 91,335 independent checks
6/6 adversarial mutations rejected
support-four moves / orbits / final rank = 7,444 / 1,119 / 60
minimum connector = 1 orbit, with 36 choices
```

The mutations alter the support-four count, an orbit representative, the
final rank/Smith record, the number of minimum subsets, the canonical
component partition and the interpretation branch.

## 7. What is now closed

Closed exactly for the participating robust P21 row:

- every primitive move at the final support ceiling;
- the complete target-orbit decomposition;
- integral equality `M_<=4=K`;
- the complete `G_<=4` graph;
- the exact minimum number and complete list of singleton target-orbit
  component mergers;
- the fact that every singleton merger still leaves free lattice rank six.

This removes the old questions “does support four generate the participating
kernel?” and “how many target orbits are needed to merge the four surviving
components?” from the open list.

## 8. What remains open and how the plan changes

The immediate finite question is no longer another support census. The
natural next task is:

> Find the minimum number of complete target-action support-four move orbits
> that, when adjoined to `M_<=3`, generate `K` integrally.

This is a different optimization from fiber connectivity. One orbit cannot
suffice because every target orbit has at most eight moves while the quotient
`K/M_<=3` has rank nine. Hence the minimum is at least two. The existing
1,119-orbit census reduces the problem to an exact search in a
nine-dimensional torsion-free quotient, so no placement or fiber
reenumeration is needed. Estimated difficulty: `3/5` for finding and
certifying the minimum, `4/5` if the minimum family is large enough to require
branch-and-bound rather than exhaustive pairs/triples.

After that, the genuinely harder bridge is:

- determine whether these moves form a Markov basis for all nonnegative
  right-hand sides of the same participating configuration, or exhibit a
  disconnected nonnegative fiber;
- then decide whether any statement survives enlargement to inactive
  placements, other P21 rows or a uniform support-degree theorem.

Those are estimated `5/5`. Lattice generation alone does not settle them.
The co-area novelty audit, uniform quotient-splitting criterion, persistent
`beta` bound, one-piece X-ray injectivity criterion and optional C34-L/G work
remain separate lanes.

## 9. Nonclaims

- No inactive legal placements.
- No other P21 row or right-hand side.
- No all-fibers Markov or Graver basis.
- No minimal lattice-generating orbit family yet.
- No global support-four theorem.
- No external novelty, public claim, manuscript or release action.
