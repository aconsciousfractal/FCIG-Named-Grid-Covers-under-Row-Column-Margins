"""Validate the source-locked comparative specimens P21, P26 IN-TREE.
Loads the locked derived coordinates (p21_locked.json / p26_locked.json), rebuilds
the target, and confirms that all 10 lines (4 rows + 4 cols + 2 diagonals) of each
4x4 geomagic square exact-cover tile the stated target under the full-D4 isometry.
A wrong piece would make some line fail, so 10/10 validates the digitisation against
the live-verified source hash. Self-contained; P42-native; no bootstrap import.

Run:  PYTHONIOENCODING=utf-8 python validate_specimens.py
"""
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent

def norm(cells):
    r0 = min(r for r, c in cells); c0 = min(c for r, c in cells)
    return frozenset((r - r0, c - c0) for r, c in cells)
def _rot(cells): return [(c, -r) for r, c in cells]
def _ref(cells): return [(r, -c) for r, c in cells]
def orientations(cells):
    out = set(); cur = list(cells)
    for _ in range(4):
        out.add(norm(cur)); out.add(norm(_ref(cur))); cur = _rot(cur)
    return out
def placements(piece, T):
    rs = [r for r, c in T]; cs = [c for r, c in T]
    mnr, mxr, mnc, mxc = min(rs), max(rs), min(cs), max(cs); out = []
    for o in orientations(piece):
        h = max(r for r, c in o); w = max(c for r, c in o)
        for dr in range(mnr, mxr - h + 1):
            for dc in range(mnc, mxc - w + 1):
                pl = frozenset((r + dr, c + dc) for r, c in o)
                if pl <= T: out.append(pl)
    return out
def tiles(pieces, T):
    """exact cover of T by one placement of each of the 4 pieces (Algorithm-X style)."""
    plac = [placements(p, T) for p in pieces]
    order = sorted(range(len(pieces)), key=lambda i: len(plac[i]))
    def rec(k, rem):
        if k == len(order):
            return not rem
        i = order[k]
        for pl in plac[i]:
            if pl <= rem:
                if rec(k + 1, rem - pl):
                    return True
        return False
    return rec(0, T)

LINES = {"R0": (0,1,2,3), "R1": (4,5,6,7), "R2": (8,9,10,11), "R3": (12,13,14,15),
         "C0": (0,4,8,12), "C1": (1,5,9,13), "C2": (2,6,10,14), "C3": (3,7,11,15),
         "D+": (0,5,10,15), "D-": (3,6,9,12)}

def validate(fn):
    obj = json.load(open(HERE / fn, encoding="utf-8"))
    pieces = [norm([tuple(x) for x in p]) for p in obj["pieces"]]
    areas = [len(p) for p in pieces]
    t = obj["target"]; rm = {tuple(x) for x in t["remove"]}
    T = frozenset((r, c) for r in range(t["rows"]) for c in range(t["cols"])) - rm
    TA = len(T)
    assert areas == obj["areas"], f"{obj['specimen']}: area drift vs locked JSON"
    # line-area consistency (necessary): every line's 4 areas sum to |T|
    for nm, idx in LINES.items():
        assert sum(areas[i] for i in idx) == TA, f"{obj['specimen']} {nm}: area sum != {TA}"
    ok = 0; fails = []
    for nm, idx in LINES.items():
        if tiles([pieces[i] for i in idx], T): ok += 1
        else: fails.append(nm)
    print(f"{obj['specimen']:4} [{obj['source']['gallery_signature']}] target {t['rows']}x{t['cols']}"
          f"{'-'+str(len(rm)) if rm else ''} ({TA} cells): {ok}/10 lines tile"
          + (f"  FAILS {fails}" if fails else "  OK")
          + f"  | src sha256 {obj['source']['sha256'][:16]}… live-verified")
    return ok == 10

if __name__ == "__main__":
    r21 = validate("p21_locked.json")
    r26 = validate("p26_locked.json")
    r49 = validate("p49_locked.json")
    print(f"\nALL SPECIMENS VALIDATED (10/10 each): {r21 and r26 and r49}")
