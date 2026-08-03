# C32 source-to-model audit

**Date:** 2026-07-26
**Scope:** one official C32 raster, its exact grid model, twenty displayed
assemblies and the Dürer complement crosswalk.
**Verdict:** `PASS`, 13/13 checks.

## Locked source

- descriptor: `4x4 Durer5`, signed `LS 11-06`;
- direct asset:
  `https://www.geomagicsquares.com/images/gallery/groot/4x4%20Durer5-zoom.jpg`;
- SHA-256:
  `c6093ccd58e725d6efde1750cccf47124a56d6a335fbe3c9b70c8ef66a9bf2cb`;
- bytes: `167595`;
- dimensions: `782×768`;
- durable derived lock: `registry/c32_source_lock.json`;
- raw copyrighted raster: not tracked.

## Independent source channels

The first channel transcribes the sixteen clean central piece drawings onto
their own calibrated grids. The second channel samples all `20×36=720` cells
in the spatially separate target panels and reconstructs the four coloured
regions in each panel. These are independent image locations and algorithms;
they are not represented as two human transcriptions.

The panel channel confirms:

- all 720 cell samples have unambiguous palette assignments;
- all 20 pixel-derived grids match the durable panel records;
- every one of the 80 coloured regions is D4-congruent to the independently
  transcribed central mask of the same area;
- all labels `1,…,16` occur;
- the ten displayed quaternes are exactly the four rows, four columns and two
  diagonals of the source Dürer square, each shown twice;
- the 20 raw panels are distinct and become 16 distinct labelled tilings after
  target canonicalisation.

## Normalisation correction

The raster does not show one literal target orientation in every panel:

- 12 panels have zero-based holes `(1,1),(4,4)`;
- 8 have holes `(1,4),(4,1)`.

The two masks are globally horizontally reflected. The lock therefore uses the
first as canonical and applies `(r,c) ↦ (r,5-c)` to the second. Treating all
panels as having the same literal hole coordinates would have been a source
normalisation error; the audit detected and repaired that assumption before
the realization census.

## Exact model

- target: `6×6` minus `(1,1),(4,4)`, area `34`;
- pieces: connected grid polyominoes with areas exactly `1,…,16`;
- total piece area: `136`;
- allowed congruence: the eight D4 coordinate actions followed by integral
  translation inside the target;
- source square:
  `((16,3,2,13),(5,10,11,8),(9,6,7,12),(4,15,14,1))`.

The source complement crosswalk is the same-cell complement `x ↦ 17-x`. All
three read-only Magic 24 artifacts match their locked hashes, and the crosswalk
preserves the complete 86-row carrier and its `52 affine + 34 non-affine`
split.

## Claim boundary

This audit admits the exact C32 model and the twenty source-displayed
witnesses. It does not decide the other 76 additive rows, claim that the ten
displayed quaternes are exhaustive, assign an erratum to the source, or
establish novelty.
