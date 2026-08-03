# Foundational C32/C46/P49 section

Scope: source identity, discrete model, exhaustive finite certificates, and
strict exactness witnesses. The results are limited to the stated finite
libraries and make no priority claim.

## Source authorship boundary

C32, C46 and P49 are discrete normalizations of 4x4 geomagic specimens created
and published by Lee Sallows. Sallows owns the displayed piece geometry,
targets and source arrangements; Peter Cameron's 2011 finite group-action
formulation is prior conceptual context. The repository begins at the
source-locked mask normalization and supplies the exhaustive censuses,
aggregate-margin fibers, replacement graphs, and uniform deductions. The original raster bytes are not
redistributed, so the replay does not independently reproduce segmentation or
transcription from the images.
## 1. From a source image to a finite theorem

The three libraries are used only after four logically separate layers have
been fixed.

1. **Source identity.** A descriptor, signature, direct asset URL, access date
   and SHA-256 digest identify the raster from which the geometry was
   transcribed. The copyrighted rasters are not redistributed.
2. **Discrete normalization.** The target cells, named piece masks, coordinate
   convention and full `D4` pose convention are stored independently of the
   raster.
3. **Exact realization census.** For every area-compatible selected set, a
   positive record contains its complete labelled tiling set and a negative
   record certifies exhaustive zero over the locked placement catalogue.
4. **Tomographic replay.** A separate calculation reconstructs the
   row-and-column margin fiber, labels its exact covers, builds the graph that
   changes exactly two named placements, and checks every component.

The source supplies the displayed geometry and arrangements. This repository
is responsible for the normalization, the exhaustive rows not asserted by the
source, the certificates and the fiber-graph conclusions. In particular, the
86 area-sum rows for C32 and C46 are an imported additive carrier, not a new
additive theorem.

## 2. Common semantics

Let `T` be a finite target cell set. Each named piece `i` has a finite
catalogue `P_i` of legal `D4` orientations and translations in `T`. For a
selected named set `E`, write

```text
F_E = one-copy placement tuples with the row-and-column X-ray of T,
T_E = tuples in F_E whose cell coverage is exactly 1_T,
G_E^(2) = graph on F_E joining tuples that differ in exactly two
          named placements.
```

Thus `T_E` is always a subset of `F_E`. We use:

- **support-exactness:** `F_E` is nonempty if and only if `T_E` is nonempty;
- **fiber purity:** `F_E=T_E`;
- **repair-exactness:** every component of `G_E^(2)` meets `T_E`;
- **repair radius:** the largest finite distance from a node of `F_E` to
  `T_E`.

Empty fibers satisfy all three predicates vacuously and have radius zero.
Area-incompatible selected sets are rejected before these predicates are
tested.

The optional graph `G_E^(<=2)` is a different object in general. In the three
complete finite panels below, however, the one-placement graph has no edges:
the exact-two and at-most-two conclusions therefore agree on these particular
libraries. The manuscript nevertheless uses `G_E^(2)` as its canonical
unqualified repair graph.

### Label convention

The notation for selected rows must not be mixed across libraries.

- In C32 and C46, piece areas are all distinct and the source piece label is
  its area. A row such as `{1,3,14,16}` therefore lists both labels and areas.
- In P49, areas `4` and `12` each occur twice. A row such as
  `(4,9,10,11)` lists **zero-based locked piece indices**, not areas. Its area
  multiset is `{4,13,1,14}`. Similarly, `(0,1,3,14)` has areas
  `{15,2,3,12}`.

This distinction is part of the statement, not merely an implementation
detail.

## 3. The three source locks

### C32

C32 is the official asset `4x4 Durer5`, signed `LS 11-06`, with SHA-256
`c6093ccd58e725d6efde1750cccf47124a56d6a335fbe3c9b70c8ef66a9bf2cb`.
The locked model has a `6×6` target with zero-based holes `(1,1)` and `(4,4)`,
sixteen connected grid pieces labelled by areas `1,…,16`, and full `D4`
placements.

The source audit exposed and repaired one normalization trap. Twelve of the
twenty displayed panels have holes `(1,1),(4,4)`, while eight have the
horizontally reflected holes `(1,4),(4,1)`. Applying
`(r,c) -> (r,5-c)` to the second group puts every panel in the canonical
target. The twenty raw panels show the ten rows, columns and diagonals of the
Dürer square twice and reduce to sixteen distinct labelled tilings after
target canonicalization. The source-to-model audit passes 13/13 checks.

### C46

C46 is the official asset `4x4 most perfect (2b)`, signed `LS 4-09`, with
SHA-256
`86430abfcfe5793fecdedf42a84a0e4f08e16636e5691ab25cf4509e9c69ef00`.
Its locked model uses the same `6×6` target with holes `(1,1),(4,4)`, sixteen
connected pieces labelled by areas `1,…,16`, and full `D4` placements. All 36
displayed target panels agree on the target mask, and the independently
recovered color components agree with the sixteen locked masks. The source
audit passes 7/7 checks.

### P49

P49-base is the source-locked `Art of Fugue`, signed `LS 7-09`, with SHA-256
`77efa6d693726aa026fce49e14480b933606ce552ff51a24eca453626d175c1e`.
Its target is `6×6` with the four corners removed. The sixteen named pieces
have area sequence, by zero-based index,

```text
(15,2,12,3,4,11,7,10,4,13,1,14,9,6,12,5).
```

Thus the target area is 32 and only 14 of the 16 areas are distinct. Three
separately extracted color panels agree as cyclic shifts of the same base
board; the low-contrast fourth panel is recorded only as the remaining
source-described shift. The locked base validates all ten magic lines under
the same `D4` exact-cover semantics.

The P49 source package establishes the specimen, not the full fiber theorem.
The 94-row realization and tomographic counts below come from the later
co-area closure and its independent replay.

## 4. Exhaustive finite proposition

**Proposition T-FOUND.** Under the source locks and common semantics above,
the complete area-compatible carriers have the following exact behavior.

| Library | Area-compatible rows | Tiling / zero rows | Margin rows | Fiber decomposition | Support | Pure | Repair |
| --- | ---: | ---: | ---: | ---: | --- | --- | --- |
| C32 | 86 | `20 / 66` | 20 | `136 = 136 + 0` | yes | yes | yes, radius 0 |
| C46 | 86 | `44 / 42` | 44 | `352 = 344 + 8` | yes | no | yes, radius 1 |
| P49-base | 94 | `60 / 34` | 61 | `1344 = 1208 + 136` | no | no | no; maximum finite radius 1 |

In each fiber decomposition the first summand counts exact labelled tilings
and the second counts non-tiling margin matches. “Zero row” means no exact
cover; it need not mean an empty margin fiber, as P49 demonstrates.

### C32: the pure anchor

The exact census finds 20 realizable and 66 exhaustive-zero rows, with 136
labelled tilings in total. Ten positive rows are source-displayed and ten are
not source-displayed. Every positive certificate contains its complete tiling
set; every negative certificate is exhaustive over the locked `D4` catalogue.
An independently coded verifier reconstructs the placement catalogues and
agrees on all 86 rows. Two genuine controls pass and eight adversarial
mutations are rejected.

The row-and-column replay finds exactly 136 margin nodes, all of them tilings.
Consequently every C32 fiber is pure and hence repair- and support-exact. The
same census also finds seven non-affine positive rows. This refutes affine
selection as a characterization, but it is auxiliary to the exactness
hierarchy.

### C46: repair without purity

The exact census finds 44 realizable and 42 exhaustive-zero rows, with 344
labelled tilings. The source displays 36 realizable rows; the remaining eight
positive rows are neutrally described as *not source-displayed*. The source
does not assert that its display is exhaustive, so this is not an erratum
claim. The independent verifier agrees on all 86 certificate records, and the
mutation suite rejects all six adversarial changes while accepting both
controls.

The margin fibers contain 352 nodes: 344 tilings and eight extras. The extras
occur in exactly two rows:

| C46 row | Fiber nodes | Tilings | Extras | Components | Exact-two edges | Trapped | Radius |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `{1,3,14,16}` | 20 | 16 | 4 | 2 | 22 | 0 | 1 |
| `{2,3,13,16}` | 8 | 4 | 4 | 4 | 4 | 0 | 1 |

Every extra is adjacent to a tiling in `G_E^(2)`. C46 is therefore
repair-exact with radius one but is not fiber-pure. This gives the strict
separation between purity and repair.

### P49: the two failures are independent

The complete P49 carrier has 94 area-compatible index rows. Sixty tile,
whereas 61 have a nonempty margin fiber. Its 1,344 margin nodes split into
1,208 tilings and 136 extras. Two different rows are needed to expose the two
failure modes:

| P49 zero-based indices | Areas | Fiber nodes | Tilings | Extras | Components | Exact-two edges | Trapped components / nodes |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `(4,9,10,11)` | `{4,13,1,14}` | 24 | 8 | 16 | 16 | 8 | `8 / 8` |
| `(0,1,3,14)` | `{15,2,3,12}` | 8 | 0 | 8 | 8 | 0 | `8 / 8` |

The first row is support-exact because both its margin fiber and its tiling
set are nonempty. Eight extras are paired by exact-two edges with tilings and
have distance one; the other eight extras form **eight trapped singleton components**.
Hence repair-exactness fails on a row where support-exactness holds.

The second row has eight margin nodes and no tiling. All eight nodes are
trapped singletons, so support-exactness itself fails. Across the entire P49
carrier there are therefore sixteen trapped components, contributed eight by
each of these rows. This row-level statement corrects the older shorthand
“one trapped component of eight nodes,” which is false for the canonical
exact-two graph.

## 5. Strict hierarchy

For every area-compatible selected set,

```text
fiber purity  =>  repair-exactness  =>  support-exactness.
```

Indeed, purity makes every fiber node a tiling. If every component contains a
tiling and the fiber is nonempty, then a tiling exists. The C46 and P49 rows
above show that neither implication reverses:

```text
C32                     pure, repair-exact, support-exact
C46                     not pure, repair-exact, support-exact
P49 (4,9,10,11)         not pure, not repair-exact, support-exact
P49 (0,1,3,14)          not pure, not repair-exact, not support-exact
```

The logical implications are elementary. The certified contribution of this
section is that the three predicates do not collapse in these source-locked
named exact-cover libraries, with every separation carried by an explicit
finite witness.

## 6. Evidence and responsibility map

| Statement | Source input | Repository result | Canonical evidence |
| --- | --- | --- | --- |
| C32 geometry | official raster, Dürer square, displayed panels | two-orientation normalization, masks and panel crosswalk | `../registry/c32_source_lock.json`, `../reports/C32_SOURCE_AUDIT.md` |
| C32 full census | locked model and imported 86-row carrier | `20/66`, 136 tilings, pure fiber, seven non-affine positives | `../reports/C32_EXACT_CENSUS.md` |
| C46 geometry | official raster and 36 displayed panels | calibrated target/piece transcription | `../registry/c46_source_lock.json`, `../reports/C46_SOURCE_AUDIT.md` |
| C46 full census | none beyond the locked model and imported 86-row carrier | `44/42`, 344 tilings and complete certificates | `../packages/package_a_c46_reproduction/realization/REPORT.md` |
| P49 geometry | official raster and four cyclic presentations | locked base specimen and ten-line validation | `../packages/package_c_comparative_hypergraphs/specimens/SPECIMENS.md` |
| Three-library fibers | locked finite models | all row counts, graph components, radii and hierarchy witnesses | `../results/coarea_fpt_analysis.json` |

The machine result is independently replayed without importing the principal
fiber engine: it regenerates `D4` poses by a different method, reconstructs
every fiber by a direct `2+2` meet-in-the-middle calculation and compares all
row counts, edge counts, components, radii and verdicts.

## 7. Reproduction contract

From the repository root, the load-bearing checks are:

```text
python -X utf8 -B packages/package_b_c32_durer_realization/realization/verify.py
python -X utf8 -B packages/package_b_c32_durer_realization/realization/mutation_test.py
python -X utf8 -B packages/package_b_c32_durer_realization/realization/verify_analysis.py

python -X utf8 -B packages/package_a_c46_reproduction/realization/verify.py
python -X utf8 -B packages/package_a_c46_reproduction/realization/mutation_test.py

python -X utf8 -B packages/package_c_comparative_hypergraphs/specimens/validate_specimens.py
python -X utf8 -B packages/package_e_obstruction_channels/xray_channel/coarea_fpt.py
python -X utf8 -B packages/package_e_obstruction_channels/xray_channel/verify_coarea_fpt.py
python -X utf8 -B packages/package_e_obstruction_channels/xray_channel/mutation_coarea_fpt.py
```

Source-image audits additionally require local copies whose bytes match the
locked hashes; the raw rasters are intentionally absent from the repository.
