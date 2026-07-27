# Source-locked comparative specimens — P21, P26

**Locked:** 2026-07-23. **Level:** derived coordinates + source hashes (the licensing
posture: only derived coordinates and image hashes are tracked; raster images stay in
scratch, © Lee Sallows, `geomagicsquares.com`).

These order-4 geomagic squares are comparative controls for C46. Their public
claim role is recorded in
[`docs/PUBLIC_CLAIM_BOUNDARY.md`](../../../docs/PUBLIC_CLAIM_BOUNDARY.md);
the historical internal label was `N-P42-004`. This directory gives them a **live-verified
provenance** so those findings no longer rest on uncertified scratch digitisations.

## Files

| File | Contents |
| --- | --- |
| `p21_locked.json` | P21 (LS 11-02) derived coordinates: 16 pieces, target `5×5`, source block (URL + sha256 + live-verify) |
| `p26_locked.json` | P26 (LS 4-04) derived coordinates: 16 pieces, target `4×6−{(3,4),(3,5)}`, source block |
| `p49_locked.json` | P49-base (LS 7-09 "Art of Fugue") derived coordinates: 16 pieces, target `6×6−4corners`, source block. The four gallery boards are cyclic shifts of this one. |
| `validate_specimens.py` | self-contained in-tree validator; rebuilds each target and confirms **10/10** lines exact-cover tile under full `D4` |

## Provenance (live-verified 2026-07-23)

Both source images were re-fetched from the live gallery and hashed; **local == fresh
download == recorded hash** for both (the gallery is mutable, so this is checked at lock
time, per `SOURCE_LOCK.md` §7 and the `EXT-GALLERY` rule "identify by descriptor + image
hash + date + URL, never by page number").

| Specimen | Signature | Descriptor | sha256 (zoom) | Target | Areas |
| --- | --- | --- | --- | --- | --- |
| **P21** | LS 11-02 | `4x4 square target` | `2248f6e9d0d4cb79…` | `5×5` (25) | twelve `6` + four `7` |
| **P26** | LS 4-04 | `Most perfect (2)` | `c1c45ab8bc3d2dcd…` | `4×6−2` (22) | Latin `{4,5,6,7}` |
| **P49-base** | LS 7-09 | `Art of Fugue` | `77efa6d693726aa0…` | `6×6−4corners` (32) | constant-32 magic sq., 14/16 distinct |

**P49 note.** "Art of Fugue" shows **four** 4×4 geomagic boards (gold/blue/orange/brown) on the
**same 16 pieces**, each nasik+most-perfect. They are **cyclic (torus) shifts** of the one base
board locked here (blue = shift `(0,1)`, orange = shift `(1,1)` of the base). Three of the four
colour panels (gold/blue/orange) were extracted **independently** and all agree as cyclic shifts —
a strong cross-check; the brown panel was not extracted (low contrast) and is the 4th shift.
**Result:** the P49 base square is **degenerate** (constant 32; 14/16 distinct — `4,12` doubled,
`8,16` absent) yet **coset-PURE** (13 balanced directions, all full; `|A|=94, |R|=60`). So — unlike
P26 — a degenerate most-perfect square **can** be pure. Its admissible public
use remains controlled by the repository claim boundary.

## Validation (in-tree, reproducible)

```bash
cd packages/package_c_comparative_hypergraphs/specimens
PYTHONIOENCODING=utf-8 python validate_specimens.py
```

Confirms **10/10** lines tile for each specimen (a wrong piece makes some line fail, so
this validates the digitisation against the locked source hash). P21 also checked
area-consistent (every line sums to 25); P26 was additionally validated on its full
32-constraint property set (8/8 broken diagonals, 16/16 torus `2×2`, 4/4 embedded-`3×3`
corners) at digitisation time (scratch).

## What this does and does not license

- **Does:** give `N-P42-004` and the coset-purity puzzle a **source-locked, in-tree
  validated** basis — the specimens are no longer "scratch, not source-locked".
- **Does NOT:** promote those findings' claim level. They stay exploratory
  (`N-P42-004` is a `CLN` bounded-negative generality result; the puzzle is a `CL0`
  scope clarification of Theorem A). Source-locking fixes provenance, not epistemic level.
- **Does NOT:** compute a certified realization hypergraph for P21/P26 (that would be the
  separate `package_a`-style certification, not taken). Only the 10-line digitisation
  check is in-tree; the full `R`/purity numbers remain scratch analyses (cited as such).

## Correction folded in

The earlier scratch `p21_pieces.json` was area-inconsistent (line sums `24/25`). The
locked `p21_locked.json` uses the **corrected** P21 digitisation, which validates 10/10 on
the `5×5` target. The stale scratch file is superseded.

## Note on P49 — SUPERSEDED (now locked)

> **Superseded 2026-07-24.** This section's original claim ("not digitised; not locked here")
> is stale. P49-base **is** now digitised and locked as `p49_locked.json` (source hash
> `77efa6…`, validates 10/10, row above), and it appears in the comparative table as the
> `δ_X=1 / τ=3` near-exact specimen. The four gallery boards were confirmed to be **cyclic
> shifts of the single base square** (so only the base carries independent information).

Gallery page 49 (LS 7-09, "Art of Fugue") — four boards on the **same 16 pieces**, all
nasik + most-perfect — is the matched control that separates piece-effect from
arrangement-effect. The base square is degenerate (constant 32; 14/16 distinct areas —
`4,12` doubled), which is why it is the natural first non-`C46` point on the distinctness axis.
