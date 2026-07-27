# Output T — current admissible results

## Release-candidate manuscript

`T-06` is closed. The complete modular LaTeX source is under `paper/`, and the
locally built release-candidate PDF is
`paper/Named_Grid_Covers_under_Row-Column_Margins.pdf` (18 pages).

The manuscript contains nine main sections, two evidence/reproducibility
appendices and twenty-one primary/prior-art references. Its sole uniform
headline is the active-carrier/largest-piece residual-area FPT theorem. C32/C46/P49 are explicitly
finite certified witnesses, and P21 is explicitly a bounded case study.

`scripts/verify_tomographic_manuscript.py` passes fail-closed checks.
The final PDF was reopened, rendered and visually inspected on all 18 pages.
No clipping, overlap, broken cross-reference, missing citation or
unreadable table was found.

## Standalone reviewer package

The historical `T-07` package is closed. In this standalone candidate,
`certificates/MANIFEST.json` freezes the manuscript, theorem/source
governance, C32/C46/P49 finite evidence, the residual-area panel and the
bounded P21 closure.

`scripts/verify.py` exposes three profiles:

- `manifest`: byte/size/path integrity plus semantic anchors;
- `core`: independent manuscript, C32, C46, specimen-lock, residual-area and
  P21 smoke replays, followed by repository and release-checksum validators;
- `full`: core mathematical coverage plus C32/C46/co-area mutation suites,
  the complete degree-four P21 Betti replay and the single-block audit through
  degree seven, followed by a full replay from a manifest-only temporary tree.

The candidate receipt is `results/verification.json`. A full `PASS`
certifies package coherence and author replay, not novelty, priority, external
reproduction or publication authority. T-08 is preserved as historical review;
T-11 closes as `PASS_WITH_REPAIRS` only when
`results/final_red_team_verification.json` passes against the current full
receipt and current manifest.

## Foundational census

| Library | Positive / negative rows | Tilings | Margin fiber | Support | Pure | Repair |
| --- | ---: | ---: | ---: | --- | --- | --- |
| C32 | 20 / 66 | 136 | `136=136+0` | yes | yes | yes |
| C46 | 44 / 42 | 344 | `352=344+8` | yes | no | yes, radius 1 |
| P49 | 61 margin-feasible rows | 1,208 in the tested fibers | `1344=1208+136` | no | no | no |

C32 and C46 are independently source-locked. The C32 positive set includes
seven non-affine rows, so affine selection is false.

For C32/C46, selected rows are sets of unique area labels. For P49, row
tuples are zero-based locked piece indices because areas 4 and 12 repeat.
The P49 tiling row `(4,9,10,11)` has areas `{4,13,1,14}` and eight trapped
singleton components; the separate support-failure row `(0,1,3,14)` has
areas `{15,2,3,12}` and eight more trapped singletons.

The publication-readable evidence and responsibility chain is
`FOUNDATIONAL_SECTION.md`.

## Uniform theorem

For a fixed selected named set with largest-piece residual area `q` and orientation
bound `h`:

```text
number of largest poses <= h(q+1)
active carrier size      <= q^2
fiber size V             <= h(q+1)(h q^2)^q
repair radius            <= V-1, when repair-exact
```

Support, purity and exact-two-replacement repair in `G_E^(2)` are
FPT-decidable in `(q,h)`. The same method handles `G_E^(<=2)`, but the two
graphs are kept distinct.
Implicit decision and compressed behavior classification are FPT under exact
participation types; literal named listing is output-sensitive.

The proof reconstruction corrected the unconditional translation lemma to
`|D(A,B)|<=max(0,|B|-|A|+1)`. This changes no margin-compatible candidate-pose
or fiber bound because each counted orientation has nonempty `D(A,B)`.

Independent replay records:

- 2,956 stored-result checks;
- 14,656 active-line/state-bound checks;
- 3,969 small translation pairs;
- 44,910 locked active-grid translation checks;
- one control and six mutations accepted/rejected as expected.

## Energy layer

`Phi` is exactly overlap mass and half the `L1` coverage deviation. Strict
descent gives repair with radius at most `q`, but the criterion is not
necessary. The C46/P49/P21/P26 panel is evidence for that boundary.

## P21 case study

Frozen object: zero-based row `(4,5,12,13)`, areas `(7,6,6,6)`, 72
participating variables, `14×72` matrix of rank 12, rank-60 integer kernel,
and a 32-node one-copy fiber containing 8 tilings and 24 extras.

Certified statements:

- support-three: 932 relations, rank 51, four fiber components;
- `M_<=3` plus any of 36 singleton connector orbits makes the fixed fiber
  connected but reaches only rank 54, leaving free quotient rank six;
- support-four: 7,444 relations in 1,119 target orbits and `M_<=4=K`;
- exactly 36 singleton orbit modules connect the four old fixed-fiber
  components, while each alone leaves free lattice rank six;
- exact complete-orbit minimum: three, with 1,404 triples;
- integral channel-family sizes: `6,3,78`;
- fixed fiber visibility: `0,0,36`;
- all-RHS Markov test: negative;
- indispensable quadrics: 218 total, 74 absent from the one-copy family;
- Markov degree: at least seven;
- minimum generators forced through degree four: 6,941.

The exact Markov degree and complete basis are open and owner-parked.
The publication-readable implication chain is `P21_CASE_STUDY.md`.
