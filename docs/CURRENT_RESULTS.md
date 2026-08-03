# Current results

## Public preprint and replay package

The modular LaTeX source and canonical 18-page PDF are under `paper/`. The
paper has one uniform headline: the active-carrier/largest-piece residual-area
FPT theorem. C32/C46/P49 are finite certified witnesses, and P21 is a bounded
case study.

The replay package exposes three profiles through `scripts/verify.py`:

- `manifest`: byte, size, path, import, semantic-anchor, and policy integrity;
- `core`: manuscript, C32, C46, specimen-lock, residual-area, P21 smoke,
  repository-policy, and release-checksum verification;
- `full`: core coverage plus mutation suites, the complete degree-four P21
  replay, the single-block audit through degree seven, and a full replay from
  a temporary tree containing only the manifest allowlist.

A passing replay establishes package coherence and author replay. It does not
establish novelty, priority, independent external reproduction, or publication
in another venue.

## Foundational census

| Library | Positive / negative rows | Tilings | Margin fiber | Support | Pure | Repair |
| --- | ---: | ---: | ---: | --- | --- | --- |
| C32 | 20 / 66 | 136 | `136=136+0` | yes | yes | yes |
| C46 | 44 / 42 | 344 | `352=344+8` | yes | no | yes, radius 1 |
| P49 | 61 margin-feasible rows | 1,208 in the tested fibers | `1344=1208+136` | no | no | no |

C32 and C46 are independently source-locked. The C32 positive set includes
seven non-affine rows, so affine selection is false. The P49 tiling row
`(4,9,10,11)` has areas `{4,13,1,14}` and eight trapped singleton components;
the separate support-failure row `(0,1,3,14)` has areas `{15,2,3,12}` and
eight more trapped singletons.

## Uniform theorem

For a fixed selected named set with largest-piece residual area `q` and
orientation bound `h`:

```text
number of largest poses <= h(q+1)
active carrier size      <= q^2
fiber size V             <= h(q+1)(h q^2)^q
repair radius            <= V-1, when repair-exact
```

Support, purity, and exact-two-replacement repair in `G_E^(2)` are
FPT-decidable in `(q,h)`. The same method handles `G_E^(<=2)`, but the graphs
remain distinct. Implicit decision and compressed behavior classification are
FPT under exact participation types; literal named listing is output-sensitive.

The corrected translation cap is
`|D(A,B)| <= max(0,|B|-|A|+1)`. Strict energy descent gives a sufficient
repair criterion with radius at most `q`, but is not necessary.

## P21 case study

The frozen row `(4,5,12,13)` has areas `(7,6,6,6)`, 72 participating
variables, a `14x72` matrix of rank 12, kernel rank 60, and a 32-node one-copy
fiber containing 8 tilings and 24 extras. The package certifies 7,444
support-four relations in 1,119 target orbits, an exact three-orbit minimum
with 1,404 triples, channel-family sizes `6,3,78`, 74 missing indispensable
quadrics, and Markov degree at least seven. The exact degree and complete basis
remain open.
