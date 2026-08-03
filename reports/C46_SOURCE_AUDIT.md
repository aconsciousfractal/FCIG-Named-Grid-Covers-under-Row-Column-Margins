# C46 source-to-model audit

**Date:** 2026-07-26  
**Decision:** `PASS_SOURCE_TO_MODEL_LOCKED`  
**Scope:** the official LS 4-09 raster and its discretisation only.

## Source lock

The load-bearing visual source is identified by descriptor and exact asset URL,
not by the mutable gallery page number:

- descriptor: `4x4 most perfect (2b)`, signed `LS 4-09`;
- URL: `https://www.geomagicsquares.com/images/gallery/groot/4x4%20most%20perfect(2b)-zoom.jpg`;
- SHA-256: `86430abfcfe5793fecdedf42a84a0e4f08e16636e5691ab25cf4509e9c69ef00`;
- bytes: `152854`;
- dimensions: `780 x 768`;
- HTTP `Last-Modified`: `Thu, 20 Nov 2014 16:24:36 GMT`;
- HTTP `ETag`: `"25516-5084cc39df900"`;
- access date: `2026-07-26`.

The copyrighted raster is not redistributed. The durable metadata, pixel
locators, target and piece masks are in `registry/c46_source_lock.json`.

## Independent target transcription

The image contains 36 displayed tiling panels. Their top-left pixel origins are
locked explicitly. Sampling the centre of each cell of each `6 x 6` panel gives,
in all 36 cases and without consulting the solver:

```text
holes = {(1,1), (4,4)}
consensus = 36/36
```

This resolves the previous contradiction. The certified model already used
`{(1,1),(4,4)}`; only the prose at the top of `c46_locked.py` incorrectly said
`{(1,1),(3,4)}`. No realization result changes.

## Independent piece transcription

The verifier segments the four source colours in the central panel, finds the
filled unit-cell interiors, groups cells only through pixel adjacency, and then
normalises each connected shape. It does not import `c46_locked.py`, `engine.py`,
the certificate generator, or any bootstrap code.

The four colour bands independently produce component areas:

```text
orange:  1, 2, 3, 4
gold:    5, 6, 7, 8
maroon:  9, 10, 11, 12
blue:    13, 14, 15, 16
```

All sixteen recovered masks agree cell-for-cell with the pre-existing
realization model. Total observed piece area is `136`.

## Boundary

This audit closes the source-to-discrete-model provenance gap for C46. It does
not establish novelty, priority, a uniform theorem, or the truth of any claim
outside the single locked LS 4-09 image.
