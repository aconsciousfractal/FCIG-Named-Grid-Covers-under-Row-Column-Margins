# Output T — source-aware theorem spine

Status: **proof-reconstructed release candidate**  
Public wording: theorem/certificate scope only; no priority or firstness

Source roles and forbidden priority wording are frozen in
`THEOREM_LEVEL_PRIOR_ART_AUDIT.md`.

## Definitions block

Fix a finite target cell set `T`, a finite set of named pieces and a finite
orientation group of order at most `h`. For a selected named set `E`, let:

```text
F_E = one-copy placements having the target X-ray;
T_E = placements in F_E whose coverage is exactly 1_T;
G_E^(2) = graph on F_E whose edges change exactly two named placements.
```

The paper uses:

- **support-exactness:** `F_E` is nonempty iff `T_E` is nonempty;
- **fiber purity:** every node of `F_E` lies in `T_E`;
- **repair-exactness:** every connected component of `G_E^(2)` meets `T_E`;
- **repair radius:** maximum graph distance to `T_E` over nodes that reach it.

The optional graph `G_E^(<=2)` additionally contains one-placement edges and
is a different object in general. The FPT proof works for either graph, but
all unqualified repair statements and foundational finite rows use
`G_E^(2)`.

Area-incompatible selected sets are rejected at preprocessing and lie outside
the largest-piece residual-area theorem's decision domain. For an area-compatible set, `T_E` is
always a subset of `F_E`. Empty fibers are support-exact, pure and
repair-exact vacuously, with radius zero.

## Proposition T-HIER — exactness hierarchy and strictness

Under the frozen conventions:

```text
fiber purity  =>  repair-exactness  =>  support-exactness.
```

Both implications are strict in the source-locked finite library class:

- C32 is pure;
- C46 is repair-exact but not pure;
- the P49 row `(4,9,10,11)` is support-exact but has eight trapped singleton
  components, so repair-exactness fails despite tiling existence;
- the separate P49 row `(0,1,3,14)` has a nonempty margin fiber and no tiling,
  so support-exactness itself fails.

The logical implications are elementary. The strictness witnesses are
certified finite propositions, not a general classification of shapes.
Generic repair from an infeasible state is prior art; the role here is to
organize the exact tomographic predicates and their non-collapse witnesses.

## Lemma T-TRANS — translation cap

For finite nonempty `A,B subset Z^2`, with

```text
D(A,B) = {t in Z^2 : A+t subseteq B},
```

one has the unconditional bound:

```text
|D(A,B)| <= max(0, |B|-|A|+1).
```

Equivalently, if `D(A,B)` is nonempty, then
`|D(A,B)| <= |B|-|A|+1`. The proof uses an integer linear functional
injective on the finite sumset. The sumset mechanism is classical; the
self-contained proof is retained. Every orientation counted in the co-area
application has nonempty `D`, so the corrected empty-set branch changes no
fiber or FPT bound.

## Lemma T-ACTIVE — co-area active carrier

Let `L` be a largest selected piece and

```text
q = |T|-|L|.
```

After freezing a pose of `L`, every residual placement participating in a
target-margin solution is confined to at most `q` active rows, `q` active
columns and hence at most `q^2` active cells.

The statement is for finite cell-list pieces and the declared X-ray
directions. It must not be generalized silently to arbitrary continuous
tomography.

## Theorem T-FPT — largest-piece residual-area decision theorem

For an area-compatible fixed selected named grid-piece set and a finite
orientation group of order at most `h`, support-exactness, fiber purity and
exact-two-replacement repair-exactness are fixed-parameter tractable in
`(q,h)`.

The full margin fiber satisfies:

```text
V(E) <= h(q+1)(h q^2)^q = 2^(O(q log q))   for fixed h.
```

The replacement graph can be built in
`2^(O(q log q)) poly(|I|)` time under the finite cell-list input contract.
Every repair-exact fiber satisfies:

```text
rho(E) <= V(E)-1
       <= h(q+1)(h q^2)^q-1.
```

The radius is an existence bound. No polynomial, linear, sharp or practical
worst-case bound is claimed.

This is the sole uniform headline after the `T-03` audit. It is stated as a
theorem for the frozen model, without a “first FPT” or other priority claim.

## Proposition T-TYPE - implicit finite-library problem

Input a target `T`, a finite named cell-list library, the explicit orientation
action, an integer threshold `Q`, and one of support, purity or exact-two
repair. Decide whether an area-compatible selected set exists whose canonical
largest name `L` satisfies `|T|-|L|<=Q` and the requested predicate.

For each candidate `L`, the exact participation type records area,
canonical-largest eligibility and, for every ordered pose of `L`, the exact
labelled participating masks. Identity of the same mask across largest-pose
scenarios is retained. Two residual selections with the same type-count vector
have isomorphic fibers, exact-cover subloci, `G^(2)` and `G^(<=2)` under
coordinate renaming.

Therefore existential decision and compressed behavior classification are FPT
in `(Q,h)`. A record contains `L`, a type-count vector `k`, the named
multiplicity `product_tau binomial(m_L(tau),k_tau)`, and fiber behavior/counts.
Literal listing remains output-sensitive and no Delay-FPT enumerator is
claimed.
## Proposition T-ENERGY — sufficient descent

For a margin node `x`, define:

```text
Phi(x) = sum_u max(c_x(u)-1,0)
       = |T|-|union_i P_i|
       = (1/2)||c_x-1_T||_1.
```

Then `0 <= Phi <= q`, and `Phi=0` exactly on tilings. If every non-tiling node
has an exact-two-replacement neighbor of smaller `Phi`, the fiber is
repair-exact and `rho<=q`.

This criterion is sufficient only. P21 and P26 refute a universal
"nonzero local minimum iff trapped" characterization.

## Proposition block T-FOUND — foundational finite libraries

The publication-readable statement, source normalization, responsibility
boundary and witness rows are frozen in `FOUNDATIONAL_SECTION.md`. The main
text may state:

```text
C32: 20/66, 136 tilings, F=136=136+0, pure.
C46: 44/42, 344 tilings, F=352=344+8, repair radius 1, not pure.
P49: support failure and eight separate trapped singleton components on a
     different tiling row.
```

The release candidate exposes the C32, C46 and P49 certified finite statements
at these exact scopes. It makes no priority or firstness claim.

## Case-study block T-P21 — three connectivity layers

The publication-readable model, proposition chain and stop boundary are
frozen in `P21_CASE_STUDY.md`. For the zero-based P21 row `(4,5,12,13)`,
whose areas are `(7,6,6,6)`, the participating matrix is `14×72` of rank 12
and has integer-kernel rank 60. Its chosen one-copy fiber has 32 nodes:
8 tilings and 24 extras.

The bounded case-study chain is:

1. `M_<=3` plus one complete target-action support-four orbit connects the
   fixed 32-node fiber but has lattice rank 54, not 60;
2. exactly three complete target-action support-four orbit modules are needed
   to generate `K/M_<=3` integrally, with 1,404 minimum triples and integral
   channel-family sizes `6,3,78`;
3. among those three rank-three families, the fixed fiber activates
   `0,0,36` orbits;
4. the full squarefree one-copy support-at-most-four family satisfies
   `M_<=4=K`;
5. that family is nevertheless not an all-right-hand-side Markov basis,
   because 74 indispensable within-block quadrics are absent;
6. an indispensable degree-seven binomial gives Markov degree at least seven.

This is a bounded conceptual case study. The exact Markov degree and complete
basis stay open and outside the paper's dependency graph.

## Dependency graph

```text
definitions
  -> T-HIER
  -> T-FOUND

T-TRANS + T-ACTIVE
  -> T-FPT
     -> T-TYPE
     -> radius bound

definitions
  -> T-ENERGY

T-FOUND + finite relation certificates
  -> T-P21 case study
```

No node depends on C34 or on completing the P21 Markov basis.
