# Source-locked comparative specimens: P21, P26, and P49

The tracked artifacts contain derived coordinates and source hashes only.
Raster images remain with their copyright holder, Lee Sallows.

## Files

| File | Contents |
| --- | --- |
| `p21_locked.json` | P21 (LS 11-02): 16 pieces, `5x5` target, source URL and SHA-256 |
| `p26_locked.json` | P26 (LS 4-04): 16 pieces, `4x6` target minus two cells, source block |
| `p49_locked.json` | P49-base (LS 7-09): 16 pieces, `6x6` target minus four corners, source block |
| `validate_specimens.py` | Rebuilds each target and confirms all ten displayed lines tile under full D4 semantics |

## Provenance

| Specimen | Signature | Descriptor | Target | Areas |
| --- | --- | --- | --- | --- |
| P21 | LS 11-02 | `4x4 square target` | `5x5` (25) | twelve 6s and four 7s |
| P26 | LS 4-04 | `Most perfect (2)` | `4x6-2` (22) | Latin `{4,5,6,7}` |
| P49-base | LS 7-09 | `Art of Fugue` | `6x6-4 corners` (32) | constant-32 square, 14 of 16 areas distinct |

The P49 source shows four boards on the same sixteen pieces. The gold, blue,
and orange panels were independently extracted and agree as cyclic shifts of
the locked base board; the low-contrast brown panel is the fourth shift. The
base has duplicated areas 4 and 12, absent areas 8 and 16, and provides the
finite negative-control rows used in the paper.

## Validation

From the repository root:

```bash
python -X utf8 -B packages/package_c_comparative_hypergraphs/specimens/validate_specimens.py
```

The validator confirms all ten displayed lines for each specimen. This checks
the in-tree digitization against the locked geometry. It does not reproduce
the absent source rasters or claim a complete realization hypergraph for P21
or P26.

The P21 lock corrects an earlier area-inconsistent digitization: every locked
line now sums to 25 and validates on the `5x5` target.
