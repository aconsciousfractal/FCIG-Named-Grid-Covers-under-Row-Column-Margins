# Manuscript build

Status: public preprint, version 1.0.0.

## Source

- `main.tex`
- `macros.tex`
- `references.tex`
- `sections/01_introduction.tex` through `sections/11_reproducibility.tex`

## Canonical build

From `paper/`, with Tectonic 0.16.9:

```bash
tectonic main.tex --outdir . --reruns 2
```

Rename `main.pdf` to `Named_Grid_Covers_under_Row-Column_Margins.pdf`. The
reruns resolve the table of contents and cross-references.

## Verification

From the repository root:

```text
python -X utf8 -B scripts/verify_tomographic_manuscript.py
pdfinfo paper/Named_Grid_Covers_under_Row-Column_Margins.pdf
pdftoppm -png paper/Named_Grid_Covers_under_Row-Column_Margins.pdf paper/render/page
```

The PDF is accepted only after all pages have been visually inspected.
