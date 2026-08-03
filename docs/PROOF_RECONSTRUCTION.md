# Proof reconstruction and dependency audit

Date: 2026-07-26

This dossier reconstructs the mathematical spine in manuscript order. It is
the proof authority for the public preprint, but it does not
settle novelty, priority, or replace the finite certificates.

## 1. Exact input contract

Let `T` be a finite set of square-grid cells. A library consists of nonempty,
named finite cell-list pieces. Legal poses are obtained from a supplied finite
orientation group of order at most `h`, followed by integer translations, and
must be contained in `T`.

For a selected named set `E={P_0,...,P_r}` with

```text
sum_i |P_i| = |T|,
```

write `Pi_i` for the legal poses of name `i`. A one-copy placement tuple
`x=(A_0,...,A_r)` chooses one `A_i in Pi_i`. Let:

```text
X(A) = joint row-and-column margin vector of A;
c_x(u) = number of chosen poses containing cell u;
F_E = {x : sum_i X(A_i)=X(T)};
T_E = {x in F_E : c_x=1_T}.
```

Thus `T_E subseteq F_E`. Area-incompatible selections are rejected before
the co-area algorithm and are not instances of the theorem. All pieces are
named and used exactly once; this is not an unlimited-multiplicity or
anonymous tile-type model.

### Frozen move graph

`G_E^(2)` has vertex set `F_E` and an edge precisely when two tuples differ
in exactly two named placements. The optional graph `G_E^(<=2)` also includes
one-name changes. They are not interchangeable:

- C32, C46 and P49 have zero one-name edges in the certified census, so their
  `G^(2)` and `G^(<=2)` conclusions coincide;
- the frozen P21 case-study row also has no one-name edge;
- other P21/P26 rows do have one-name edges, and their component structure
  can change after those edges are added.

Every unqualified repair statement below refers to `G_E^(2)`. The same
enumeration proof is FPT for `G_E^(<=2)`, but that is a separately labelled
variant.

## 2. Empty-fiber conventions and exactness hierarchy

For an area-compatible selected set define:

- support-exact: `F_E` is nonempty iff `T_E` is nonempty;
- pure: `F_E=T_E`;
- repair-exact: every connected component of `G_E^(2)` meets `T_E`;
- finite repair distance of a node: its graph distance to `T_E`, when such a
  path exists;
- repair radius: the maximum finite repair distance, set to zero when `F_E`
  is empty or has no non-tiling node.

An empty fiber is support-exact, pure and repair-exact vacuously. A nonempty
fiber with a component disjoint from `T_E` is not repair-exact; its trapped
nodes do not receive a finite repair distance.

### Proposition T-HIER

```text
purity => repair-exactness => support-exactness.
```

Proof. If `F_E=T_E`, every vertex is a tiling, hence every component meets
`T_E`. If repair-exactness holds and `F_E` is nonempty, any component contains
a tiling, so `T_E` is nonempty. The reverse implication
`T_E nonempty => F_E nonempty` always holds because `T_E subseteq F_E`.
The empty case was fixed above.

Both implications are strict:

- C46 has `F=352=344+8`; all eight defects repair in one `G^(2)` edge. It is
  repair-exact but not pure.
- P49 row `(4,9,10,11)` has a tiling and hence is support-exact, but it also
  has eight trapped singleton components, containing one node each. It is not
  repair-exact.
- Separately, P49 row `(0,1,3,14)` has eight margin nodes and no tiling, so
  support-exactness itself can fail.

C32 (`F=T=136`) is the positive pure anchor, not a strictness witness.

## 3. Corrected translation cap

For finite nonempty `A,B subset Z^2`, put

```text
D(A,B)={t in Z^2 : A+t subseteq B}.
```

### Lemma T-TRANS

The unconditional statement is

```text
|D(A,B)| <= max(0, |B|-|A|+1).
```

Equivalently, when `D(A,B)` is nonempty,

```text
|D(A,B)| <= |B|-|A|+1.
```

Proof. The empty case is immediate. Suppose `D=D(A,B)` is nonempty. Then
`A+D subseteq B`. Choose an integer linear functional `ell` that is injective
on the finite set `A+D`; this is possible by avoiding finitely many forbidden
integer slopes. Translating `A` by one fixed element of `D`, and conversely
translating `D` by one fixed element of `A`, shows that `ell` is also
injective on each factor. The finite nonempty subsets
`ell(A),ell(D) subset Z` satisfy

```text
|ell(A)+ell(D)| >= |ell(A)|+|ell(D)|-1.
```

Indeed, if `a_1<...<a_m` and `d_1<...<d_n`, then

```text
a_1+d_1 < ... < a_m+d_1 < a_m+d_2 < ... < a_m+d_n
```

is a chain of `m+n-1` distinct sums. Since
`ell(A+D)=ell(A)+ell(D)` and `ell` is injective on `A+D`, this gives

```text
|B| >= |A+D| >= |A|+|D|-1.
```

Rearrangement proves the claim. The mechanism is classical torsion-free
sumset theory; no novelty is assigned to this lemma.

If `|B|-|A|=q`, each orientation with at least one admissible translation has
at most `q+1` of them. Summing over at most `h` group elements gives at most
`h(q+1)` legal poses. Repeated orientations can only lower the actual count.

Scope repair. Earlier project prose omitted the `D=empty` branch and was
literally false when `|A|>|B|+1`. Every pose counted by the co-area proof has
nonempty `D`, so no algorithmic or finite result changes.

## 4. Active carrier and bounded states

Choose the canonical largest selected name `L`, breaking area ties by the
fixed name order, and define

```text
q=|T|-|L|.
```

The residual pieces are nonempty and their areas sum to `q`, so their number
`r` is at most `q`.

Freeze a legal pose `A` of `L` and let

```text
b=X(T)-X(A).
```

Because `A subseteq T`, `b` is nonnegative. Its row coordinates sum to `q`,
as do its column coordinates. Hence at most `q` rows and at most `q` columns
have positive residual margin.

If a residual pose `Q` occurs in a tuple whose residual margins sum to `b`,
then `X(Q)<=b` coordinatewise. Consequently `Q` uses only active rows and
active columns and lies in

```text
G_A=T intersect (active rows x active columns),   |G_A|<=q^2.
```

This proves T-ACTIVE. It depends on legal poses being contained in `T` and on
the declared row/column finite-grid margins. It does not assert a continuous
tomography theorem.

For a margin dynamic program the exact partial-state box has size

```text
B(b)=product_j (b_j+1).
```

Since `n+1<=2^n` for every nonnegative integer `n`, the row factor is at most
`2^q`, as is the column factor. Thus `B(b)<=4^q`. For exact coverage after
freezing `A`, the residual target has `q` cells and a subset-mask dynamic
program has at most `2^q` states.

These two DPs decide, for each frozen `A`, margin feasibility and tiling
feasibility. Their disjunctions over the poses of `L` decide support
exactness. Reconstructing all accepting margin paths supplies the full fiber
for purity and repair.

## 5. Sharpened fiber and graph bounds

T-TRANS applied to `L` inside `T` gives at most `h(q+1)` largest poses.
For a fixed largest pose and a residual piece of area `a_i`, each orientation
having a margin-compatible candidate placement has

```text
at most |G_A|-a_i+1 <= q^2-a_i+1
```

translations. Orientations with no placement contribute zero; this is exactly
where the corrected empty-set branch is used. Therefore

```text
V(E)
 <= h(q+1) h^r product_i(q^2-a_i+1)
 <= h(q+1)(h q^2)^q
 = 2^(O(q log(qh)))
```

For fixed `h` this is `2^(O(q log q))`, for `q>=1`. The case `q=0` contains
only the largest piece and is handled directly.

To construct `G_E^(2)`, start from each hashed fiber node, choose the two names
to change, enumerate their alternative candidate poses, and retain tuples
found in the hash set. Residual/residual changes contribute at most
`q^2(hq^2)^2`; largest/residual changes fit the same coarse bound after
enumerating at most `h(q+1)` new largest poses. Hence:

```text
time <= O(V(E) h^2 q^6 poly(|I|))
     = 2^(O(q log(qh))) poly(|I|).
```

For fixed `h` this simplifies to `2^(O(q log q)) poly(|I|)`.

Adding the one-name cases gives the same FPT class for `G_E^(<=2)`.

This proves T-FPT for support, purity and exact-two repair of a fixed selected
set. The algorithm may be extremely conservative; no practical runtime claim
is licensed by the asymptotic theorem.

### Radius

In a repair-exact fiber, choose a nearest tiling in the component of a node.
A shortest path is simple, so it uses at most the component size minus one
edges. Therefore:

```text
rho(E) <= V(E)-1 <= h(q+1)(h q^2)^q-1.
```

This is an existence bound, not a polynomial, linear, sharp or useful
worst-case estimate.

## 6. Implicit selected-sublibrary compression

This is a separate parameterized problem, not an automatic consequence of the
fixed-selected-set theorem. Input `T`, a finite named library, the explicit
orientation action, a threshold `Q`, and one requested predicate. Ask whether
there is an area-compatible selected set `E` whose canonical largest name
`L(E)` satisfies `|T|-|L(E)|<=Q` and whose fiber has the predicate. The output
version is compressed classification, not literal named listing.

For a candidate `L`, order its poses `A_1,...,A_s`, let
`b_j=X(T)-X(A_j)`, and define `M_j(P)` as the exact labelled masks of `P` with
`X(B)<=b_j`. Canonical-largest eligibility is part of the record. The exact
type is

```text
tau_L(P)=(area(P), eligibility, (M_1(P),...,M_s(P))).
```

All masks live in the common carrier `S_L=union_j G_{A_j}` with
`|S_L|<=h(Q+1)Q^2`. A mask is stored by its actual cells, so its identity is
retained across scenarios.

### Lemma T-TYPE-ISO

If two residual selections admit a name bijection preserving `tau_L`, retain
the same mask in each matched coordinate. This is a bijection of placement
tuples, preserves margin sums and cell coverage, and therefore maps the fiber
and exact-cover sublocus isomorphically. It also preserves the set of named
coordinates that change, including when the largest pose changes. Hence it is
an isomorphism of `G^(2)` and `G^(<=2)`.

Only `f(Q,h)` exact types exist. Nonempty residual names total at most `Q`
cells, so every availability can be truncated at `Q`. Enumerate eligible type
vectors with `sum_tau k_tau area(tau)=q_L` and run T-FPT on one representative.
The represented named multiplicity is

```text
product_tau binomial(m_L(tau),k_tau).
```

Signature construction over all candidate largest names is polynomial in the
explicit library size; superpolynomial work depends only on `(Q,h)`. Literal
listing is output-sensitive: the `1 x 2Q` bar/monomino example has
`binomial(N,Q)` named outputs. No Total-FPT or Delay-FPT listing claim follows.
## 7. Overlap energy

For `x in F_E`, let

```text
Phi(x)=sum_u max(c_x(u)-1,0).
```

All poses lie in `T` and their total area is `|T|`. Hence

```text
Phi(x)=|T|-|union_i A_i|.
```

Also `sum_u(c_x(u)-1)=0`. Positive deviation therefore equals uncovered mass,
so

```text
Phi(x)=(1/2)||c_x-1_T||_1.
```

The largest pose covers `|T|-q` distinct cells, giving `0<=Phi<=q`.
Moreover `Phi=0` exactly when `c_x=1_T`, that is, exactly on `T_E`.

If every non-tiling vertex has a `G_E^(2)` neighbor with smaller `Phi`,
integer strict descent reaches a tiling in at most `Phi(x)<=q` steps. The
fiber is repair-exact and `rho<=q`.

This criterion is sufficient, not necessary. The certified P21/P26 panel has
repairable nonzero local minima that require a temporary nondecreasing or
uphill move. No local-minimum characterization is claimed.

## 8. Foundational finite propositions

The proof layer and the finite-certificate layer have different jobs:

| Object | Certified role | What it does not prove |
| --- | --- | --- |
| C32 | `20/66`, 136 tilings, `F=136=136+0`; pure | a classification of pure libraries |
| C46 | `44/42`, 344 tilings, `F=352=344+8`; radius 1 | that all impure fibers repair |
| P49 | support-failure row and separate tiling row with trapped component | a universal forbidden pattern |

The paper may use them to witness the strict hierarchy and motivate the
algorithm. It must cite the source locks and replay artifacts. The repository
candidate exposes C32, C46, P49 and the largest-piece residual-area theorem only
at the exact scopes in `CLAIM_LEDGER.md`, with no priority or firstness claim.

## 9. P21 case study: three distinct connectivity questions

The full publication-readable chain is `P21_CASE_STUDY.md`. Freeze the
zero-based P21 row `(4,5,12,13)`, whose areas are `(7,6,6,6)`. Its
participating configuration is a rank-12 `14×72` matrix with integer-kernel
rank 60. The selected one-copy fiber has

```text
32 nodes = 8 tilings + 24 extras.
```

### Layer A - one fixed nonnegative fiber

Let `M_<=s` be the integer span of all squarefree one-copy relations of piece
support at most `s`, and use the separately labelled graph `G_<=s` on the
chosen fiber. Piece support is not toric degree.

At support at most two, the graph has sixteen two-node components and sixteen
trapped nodes. At support at most three, all nodes reach tilings but four
components remain. Adding any one of 36 complete target-action support-four
connector orbits makes the fixed graph connected.

For the canonical orbit `O_714`, however,

```text
rank(M_<=3 + <O_714>) = 54 < 60.
```

Therefore connectivity of this selected fiber does not imply generation of
the full participating relation lattice.

### Layer B - integral lattice generation

The complete support filtration gives

```text
support <=2:  144 relations, rank 34
support <=3:  +932 relations, rank 51
support <=4: +7444 relations, rank 60
```

All final Smith factors are one, hence `M_<=4=K` integrally.

The torsion-free quotient `K/M_<=3` has rank nine. Exactly three complete
target-action support-four orbit modules are needed to generate it. There are
1,404 minimum triples, one from each integral rank-three family of sizes
`6,3,78`. Among these three families the fixed fiber activates `0,0,36`
orbits. Thus two algebraically necessary channel families are invisible in
the chosen fiber.

Integer generation allows signed intermediate combinations. It does not
assert that a move sequence stays nonnegative.

### Layer C - all-RHS Markov connectivity

The squarefree one-copy family is not a Markov basis for all nonnegative
right-hand sides. Among 218 indispensable quadratic generators, 74
within-block quadrics are absent. A two-monomial fiber with block count
`(2,0,0,0)` is therefore disconnected even though `M_<=4=K`.

A separate exact two-monomial fiber forces an indispensable degree-seven
binomial, so the Markov degree is at least seven. The bounded
minimum-generator census is:

```text
degree 2:  218
degree 3:  996
degree 4: 5727
total through degree 4: 6941.
```

None of these facts gives an upper bound of seven or a complete Markov basis.
The exact degree, complete basis, blockwise bases and structured lift are
open and absent from the paper dependency graph.

## 10. Dependency audit

```text
T-DEF
  -> T-HIER
  -> finite interpretation of C32/C46/P49

T-TRANS + T-ACTIVE + area compatibility
  -> T-FPT
     -> graph construction
     -> radius existence
     -> T-TYPE (with canonical-largest and compressed-output contract)

T-DEF + total-area identity
  -> T-ENERGY

finite P21 relation certificates
  -> T-P21 bounded case study
```

No theorem above depends on:

- C34 lattice transcription or continuous completeness;
- a structural forbidden-pattern theorem;
- a sharp repair radius;
- a Delay-FPT literal enumerator;
- the exact P21 Markov degree or complete basis;
- a novelty or priority conclusion.
