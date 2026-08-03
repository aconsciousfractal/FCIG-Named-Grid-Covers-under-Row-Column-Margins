# C32 exact realization census

**Date:** 2026-07-26
**Finite scope:** all 86 four-subsets of `{1,…,16}` summing to 34, on the
source-locked C32 target and piece library.
**Computational verdict:** complete.

## Exact outcome

| Quantity | Value |
| --- | ---: |
| additive carrier rows | 86 |
| realizable rows | 20 |
| exhaustive-zero rows | 66 |
| explicit tilings | 136 |
| source-displayed realizable rows | 10 |
| realizable but not source-displayed rows | 10 |
| affine realizable rows | 13 |
| non-affine realizable rows | 7 |

The certificate bundle SHA-256 is
`802776741190184481d20bf01190564105b0eca840692abf9d53d4246e9ddca4`.
Every positive record contains the complete explicit tiling set. Every
negative contains an exhaustive-zero record in the locked D4 placement
catalogue.

## Complete positive support

“Displayed” means that the quaterne is one of the ten magic lines drawn in the
source image. It does not mean that the source asserted exhaustiveness.

| Source piece IDs | Tilings | Affine | Displayed |
| --- | ---: | --- | --- |
| 1,4,14,15 | 4 | yes | yes |
| 1,5,12,16 | 20 | yes | no |
| 1,7,10,16 | 4 | yes | yes |
| 1,7,11,15 | 16 | **no** | no |
| 1,8,12,13 | 4 | yes | yes |
| 1,9,11,13 | 8 | **no** | no |
| 2,3,13,16 | 4 | yes | yes |
| 2,5,11,16 | 4 | yes | no |
| 2,6,10,16 | 4 | **no** | no |
| 2,6,11,15 | 16 | yes | no |
| 2,7,11,14 | 4 | yes | yes |
| 2,9,11,12 | 4 | **no** | no |
| 3,5,11,15 | 16 | **no** | no |
| 3,6,10,15 | 4 | yes | yes |
| 3,7,11,13 | 4 | **no** | no |
| 4,5,9,16 | 4 | yes | yes |
| 4,6,11,13 | 4 | yes | yes |
| 5,8,10,11 | 4 | yes | yes |
| 6,7,8,13 | 4 | **no** | no |
| 6,7,9,12 | 4 | yes | yes |

## Independent closure

The primary engine enumerates legal placements and exact covers generically
from the data lock. The independent verifier imports neither the engine nor
the certificate generator; it reconstructs all eight coordinate transforms
and branches on the most constrained uncovered target cell.

It verifies:

- the exact 86-row key set and source-lock identity;
- all placement catalogues and exact-cover counts;
- equality of every explicit positive tiling set;
- exhaustive zero for all 66 negatives;
- all twenty source panels, giving sixteen canonical labelled tilings;
- the complement crosswalk and every affine flag.

The mutation suite has two genuine controls and rejects eight adversarial
changes: source hash, target cell, piece cell, positive placement, tiling
count, negative verdict, complement crosswalk and missing row.

## Structural decisions

### Affine selection

The hypothesis “every realizable C32 quaterne is affine” is false. Seven exact
non-affine witnesses occur:

```text
{1,7,11,15}, {1,9,11,13}, {2,6,10,16},
{2,9,11,12}, {3,5,11,15}, {3,7,11,13},
{6,7,8,13}.
```

This is a finite counterexample to the proposed selector hypothesis, not a
general classification theorem.

### Row-and-column X-ray fiber

Across the complete 86-row carrier:

```text
margin-feasible rows: 20
fiber nodes:          136
exact tilings:        136
non-tiling extras:      0
false-positive rows:    0
```

Thus C32 is support-exact, fiber-pure and repair-exact for the declared
row+column direction family. Its tomographic closure in the declared
dictionary is `τ_D=2`, and `δ_X=0`. This remains a fixed finite statement.

### Coherence

Each Dürer row, column and diagonal has four local tilings. The four row
relations admit `4^4=256` independent choices. None partitions the target on
the first column, so:

```text
row-coherent assignments:        256
row+column-coherent assignments:   0
fully coherent assignments:        0
```

C32 therefore has no coherent semigeomagic fixed-placement section under the
locked definition. This obstruction is stronger and earlier than C46’s:
C46 has four row+column sections and fails only at a diagonal.

## Reproduce

From the repository root:

```powershell
python -X utf8 -B packages\package_b_c32_durer_realization\realization\verify.py
python -X utf8 -B packages\package_b_c32_durer_realization\realization\mutation_test.py
python -X utf8 -B packages\package_b_c32_durer_realization\realization\verify_analysis.py
```
