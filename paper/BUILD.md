# Manuscript build

Status: repository release candidate. Building the PDF does not authorize
publication, submission, DOI, or priority wording.

## Source

- `main.tex`
- `macros.tex`
- `references.tex`
- `sections/01_introduction.tex` through `sections/11_reproducibility.tex`

## Accepted build

The accepted standalone-candidate PDF was built with Tectonic 0.16.9:

```bash
tectonic main.tex --outdir . --keep-logs --reruns 1
```

Rename `main.pdf` and `main.log` to
`Named_Grid_Covers_under_Row-Column_Margins.pdf` and
`Named_Grid_Covers_under_Row-Column_Margins.log`.

## pdfLaTeX alternative

From `paper/`, with `pdflatex` on `PATH`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error \
  -jobname=Named_Grid_Covers_under_Row-Column_Margins main.tex
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error \
  -jobname=Named_Grid_Covers_under_Row-Column_Margins main.tex
```

Two passes are required for the table of contents and cross-references.

## Verification

From the repository root:

```text
python -X utf8 -B scripts/verify_tomographic_manuscript.py
pdfinfo paper/Named_Grid_Covers_under_Row-Column_Margins.pdf
pdftoppm -png paper/Named_Grid_Covers_under_Row-Column_Margins.pdf paper/render/page
```

The final PDF is accepted only after all pages have been visually inspected.
