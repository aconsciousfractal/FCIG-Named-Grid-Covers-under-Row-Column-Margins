# Named Grid Covers under Row--Column Margins

Companion repository for the public preprint

> **Named Grid Covers under Row--Column Margins: Three Exactness Levels and
> Largest-Piece Localization**  
> Oleksiy Babanskyy, 2026.

PDF: [`paper/Named_Grid_Covers_under_Row-Column_Margins.pdf`](paper/Named_Grid_Covers_under_Row-Column_Margins.pdf).

## What the paper proves

The paper studies finite exact covers by named grid pieces through their row
and column margins. Its uniform result is a fixed-parameter algorithm in the
largest-piece residual area `q` and orientation bound `h`:

- a largest pose has at most `h(q+1)` possibilities;
- after it is fixed, every margin-compatible residual placement is supported
  on an active carrier of at most `q^2` cells;
- the relevant margin fiber has size at most
  `h(q+1)(h q^2)^q = 2^(O(q log(qh)))`, and therefore
  `2^(O(q log q))` for fixed `h`;
- support exactness, fiber purity, and exact-two-replacement repair exactness
  are FPT-decidable;
- implicit decision and compressed classification are FPT under exact
  participation types, while literal named listing remains output-sensitive.

The logical hierarchy

```text
fiber purity => repair exactness => support exactness
```

is strict in the certified C32/C46/P49 library. The P21 case study then
separates fixed-fiber connectivity, integral lattice generation, and
all-right-hand-side Markov connectivity.

## Certified finite layer

The repository independently enumerates downstream from source-locked,
normalized discrete models and checks these exact aggregates:

| Library | Margin fiber | Tiling nodes | Role |
| --- | ---: | ---: | --- |
| C32 | 136 | 136 | pure anchor |
| C46 | 352 | 344 | repair-exact but impure |
| P49 | 1,344 | 1,208 | support/repair negative control |

For the frozen P21 row, the package certifies a `14x72` rank-12 configuration,
kernel rank 60, 7,444 support-four relations in 1,119 target orbits, an exact
three-orbit minimum with 1,404 triples, 74 missing indispensable quadrics, and
Markov degree at least seven.

## Claim boundary

The theorem and finite statements are asserted only at the scopes stated in
the manuscript and [`docs/CLAIM_LEDGER.md`](docs/CLAIM_LEDGER.md). This
repository makes **no priority or firstness claim**. In particular, it does not
claim a complete P21 Markov basis, an exact P21 Markov degree, arbitrary-tile
tomography, a sharp repair radius, or literal Total-FPT enumeration.

Lee Sallows owns the underlying geomagic specimens and displayed source
arrangements. This repository contains no source raster bytes; it starts from
documented discrete normalizations and certifies the downstream enumeration
and tomography. See [`docs/SOURCE_LOCK.md`](docs/SOURCE_LOCK.md) and
[`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

## Verification

The primary entry point is:

```bash
python -X utf8 -B scripts/verify.py --profile core
```

The exact environment and slower `full` profile are documented in
[`REPRODUCE.md`](REPRODUCE.md). A successful run checks manifest integrity,
import closure, manuscript/PDF consistency, C32/C46 certificates, P21/P26/P49
specimen validation, the regenerated residual-area panel, P21 replay,
archive-level checksums, repository policy, and---in the full profile---a
complete replay from a manifest-only temporary tree. Generated receipts are
written under `results/`.

## Layout

```text
paper/          modular LaTeX source and title-named PDF
scripts/        repository verifier, manifest builder, policy validators
certificates/   environment lock and frozen manifest
registry/       C32/C46 source locks
packages/       self-contained C32/C46/residual-area/P21 replay code
reports/        finite certificates and source audits
results/        frozen mathematical outputs plus generated verification receipts
docs/           claim, source, proof, prior-art, artifact, and review maps
```

`LICENSE_SCOPE.md` records the licensing boundary. `MANIFEST_SHA256.txt` pins
the environment-independent package source. `SHA256SUMS` covers the complete
allowlisted release payload, including the PDF, frozen results, JSON manifest,
and portable source manifest; volatile top-level replay logs are excluded.
