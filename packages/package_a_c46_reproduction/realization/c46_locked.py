"""Source-locked discrete model for C46 / LS 4-09.

The canonical target and piece masks are loaded from
``registry/c46_source_lock.json``.  The independent pixel verifier
``scripts/audit_c46_source.py`` reconstructs those data directly from the
official image without importing this module or the realization engine.

All 36 displayed panels have target holes ``(1,1)`` and ``(4,4)``.  An earlier
docstring said ``(1,1)`` and ``(3,4)``; that was a prose transcription error.
The certified model and certificates already used the correct pair.
"""
import json
from pathlib import Path
import sys
import time

from engine import tiles, tilings, normalize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE_LOCK_PATH = ROOT / "registry" / "c46_source_lock.json"
SOURCE_LOCK = json.loads(SOURCE_LOCK_PATH.read_text(encoding="utf-8"))
MODEL = SOURCE_LOCK["canonical_model"]

# ----- the 16 source-audited pieces, indexed by AREA ----------------------
PIECE = {
    int(area): normalize([tuple(cell) for cell in cells])
    for area, cells in MODEL["pieces"].items()
}
for area, cells in PIECE.items():
    assert len(cells) == area, f"area mismatch {area}: {len(cells)}"
assert sum(PIECE)==136

# ----- the numerical magic square (P42), row-major areas ------------------
SQ = [4,5,10,15, 14,11,8,1, 7,2,13,12, 9,16,3,6]
def line(idx): return [PIECE[SQ[i]] for i in idx]
LINES = {
 "R0":(0,1,2,3), "R1":(4,5,6,7), "R2":(8,9,10,11), "R3":(12,13,14,15),
 "C0":(0,4,8,12),"C1":(1,5,9,13),"C2":(2,6,10,14),"C3":(3,7,11,15),
 "D+":(0,5,10,15),"D-":(3,6,9,12),
}
for nm,idx in LINES.items():
    assert sum(SQ[i] for i in idx)==34, nm

# ----- target: 36/36 source panels show these two holes --------------------
TARGET_HOLES = {tuple(cell) for cell in MODEL["target"]["holes"]}
def T6(holes): return frozenset((r,c) for r in range(6) for c in range(6)) - set(holes)
TARGET = T6(TARGET_HOLES)

def test_target(holes, label):
    T = T6(holes)
    if len(T)!=34:
        print(f"{label}: |T|={len(T)} != 34, skip"); return None
    t0=time.time(); ok={}
    for nm,idx in LINES.items():
        ok[nm]=tiles(line(idx), T)
    n=sum(ok.values())
    print(f"{label} holes={sorted(holes)}: {n}/10 lines tile   [{time.time()-t0:.1f}s]  "
          + " ".join(f"{k}{'+' if v else '-'}" for k,v in ok.items()))
    return n

if __name__=="__main__":
    print("=== C46 source-locked target ===")
    print(f"source: {SOURCE_LOCK['source']['descriptor']}")
    print(f"sha256: {SOURCE_LOCK['source']['sha256']}")
    print(f"panel consensus: {MODEL['target']['panel_consensus']}")
    test_target(TARGET_HOLES, "source-locked")
