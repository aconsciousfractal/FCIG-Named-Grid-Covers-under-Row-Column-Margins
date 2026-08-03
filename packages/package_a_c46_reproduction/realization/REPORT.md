# C46 exact-realization report

The 36 source-displayed C46 groups all tile the target. The remaining 50
area-compatible quaternes split into 8 positive and 42 negative rows, so all
86 rows have exact certificates.

## Result

| Quantity | Value | How established |
| --- | ---: | --- |
| additive quaternes | 86 | forced carrier count |
| realizable rows | **44** | 44 positive and 42 exhaustive-negative certificates |
| source-displayed rows | **36/36 tile** | all nine displayed balanced-direction families realize |
| remaining rows | **8 tile, 42 do not** | exact-cover certificates on both sides |
| split balanced-direction families | **0** | the realizable rows are 11 whole families |
| realizable rows in affine core | **44/44** | every realizing family is balanced-direction |

## Certificates and verification

- `R_certificates.json` records every positive tiling and every exhaustive
  negative result.
- `verify.py` uses its own D4, placement, and exact-cover implementation and
  reconstructs all 86 rows with zero failures.
- `mutation_test.py` rejects six targeted perturbations while two controls
  pass, exercising congruence, partition, area, and refutation branches.

## Structural findings

The two non-realizing balanced directions are `[0,2,8,10]` and
`[0,7,10,13]`; the latter is the broken-diagonal direction matching the
source's "most-perfect but not panmagic" caption.

The realizable set exceeds the 36 displayed groups by two whole
balanced-direction families, `[0,3,9,10]` and `[0,6,10,12]`, totaling eight
quaternes. The source does not assert that its display is exhaustive, so this
is a census observation rather than an erratum claim.

All negative records are closed exact-cover trees rather than solver status
codes. The report is a finite C46 statement, not a general law about
most-perfect arrangements.
