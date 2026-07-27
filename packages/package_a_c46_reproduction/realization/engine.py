"""Geomagic realization engine — the core tool for the geomagic/FCIG project.

A geomagic square is a 3x3 (or 4x4) array of polyomino PIECES such that the
pieces of every magic line tile a common TARGET region. This module:

  * represents pieces as sets of unit cells;
  * generates all placements of a piece inside a target under the allowed
    isometries (default: the full dihedral group D4 = 4 rotations x 2 reflections,
    which is Sallows' stated convention "pieces may be rotated or reflected");
  * decides, and counts, exact-cover tilings of the target by a multiset of
    pieces (Algorithm X);
  * checks all 8 magic lines of a 3x3 square (the geomagic property);
  * enumerates the REALIZATION HYPERGRAPH: every cell-subset whose pieces tile
    the target, not only the 8 declared lines.

No external dependencies. Everything exact over integer cell coordinates.
"""
from itertools import combinations


# --------------------------------------------------------------------------
# pieces as frozensets of (row, col); isometries; placements
# --------------------------------------------------------------------------

def normalize(cells):
    """translate a cell set so its min row/col is 0; return a sorted tuple."""
    rs = min(r for r, c in cells)
    cs = min(c for r, c in cells)
    return tuple(sorted((r - rs, c - cs) for r, c in cells))


def _rot(cells):
    return [(c, -r) for r, c in cells]


def _mir(cells):
    return [(r, -c) for r, c in cells]


def orientations(cells, allow_reflection=True):
    """all distinct normalized orientations under D4 (or C4 if reflections off)."""
    out = set()
    cur = list(cells)
    for _ in range(4):
        cur = _rot(cur)
        out.add(normalize(cur))
        if allow_reflection:
            out.add(normalize(_mir(cur)))
    return out


def placements(piece, target, allow_reflection=True):
    """every placed copy of `piece` whose cells all lie in `target` (a set)."""
    target = set(target)
    out = []
    seen = set()
    minr = min(r for r, c in target)
    maxr = max(r for r, c in target)
    minc = min(c for r, c in target)
    maxc = max(c for r, c in target)
    for ori in orientations(piece, allow_reflection):
        h = max(r for r, c in ori)
        w = max(c for r, c in ori)
        for dr in range(minr, maxr - h + 1):
            for dc in range(minc, maxc - w + 1):
                placed = frozenset((r + dr, c + dc) for r, c in ori)
                if placed <= target and placed not in seen:
                    seen.add(placed)
                    out.append(placed)
    return out


# --------------------------------------------------------------------------
# exact cover of the target by a multiset of pieces (Algorithm X, recursive)
# --------------------------------------------------------------------------

def tilings(piece_list, target, allow_reflection=True, limit=None):
    """
    Return the list of tilings of `target` by the pieces in `piece_list`
    (each piece used exactly once). A tiling is a tuple of placed frozensets,
    in piece order. `limit` caps the count (None = all).
    Requires sum of piece areas == |target| (checked).
    """
    target = frozenset(target)
    if sum(len(p) for p in piece_list) != len(target):
        return []
    plc = [placements(p, target, allow_reflection) for p in piece_list]
    if any(len(x) == 0 for x in plc):
        return []
    results = []

    def rec(idx, remaining, chosen):
        if limit is not None and len(results) >= limit:
            return
        if idx == len(piece_list):
            if not remaining:
                results.append(tuple(chosen))
            return
        # prune: cheapest un-coverable check — the next piece must be placeable
        for pl in plc[idx]:
            if pl <= remaining:
                chosen.append(pl)
                rec(idx + 1, remaining - pl, chosen)
                chosen.pop()
                if limit is not None and len(results) >= limit:
                    return

    rec(0, target, [])
    return results


def tiles(piece_list, target, allow_reflection=True):
    return len(tilings(piece_list, target, allow_reflection, limit=1)) > 0


# --------------------------------------------------------------------------
# the 3x3 geomagic property and the realization hypergraph
# --------------------------------------------------------------------------

# cells of a 3x3 board, row-major 0..8; the 8 magic lines
LINES_3 = {
    "R1": (0, 1, 2), "R2": (3, 4, 5), "R3": (6, 7, 8),
    "C1": (0, 3, 6), "C2": (1, 4, 7), "C3": (2, 5, 8),
    "D1": (0, 4, 8), "D2": (2, 4, 6),
}


def check_lines(pieces9, target, allow_reflection=True, lines=LINES_3):
    """pieces9: list of 9 cell-sets (row-major). Returns {line: tiling_count}."""
    out = {}
    for name, cells in lines.items():
        pl = [pieces9[i] for i in cells]
        out[name] = len(tilings(pl, target, allow_reflection))
    return out


def is_geomagic(pieces9, target, allow_reflection=True, lines=LINES_3):
    return all(v > 0 for v in check_lines(pieces9, target, allow_reflection, lines).values())


def realization_hypergraph(pieces9, target, size=3, allow_reflection=True):
    """
    Every `size`-subset of the 9 cells whose pieces tile the target.
    Returns a dict {frozenset(cells): tiling_count} for those that tile.
    For 3x3 the natural size is 3 (a "line-sized" triple).
    """
    out = {}
    for combo in combinations(range(9), size):
        if sum(len(pieces9[i]) for i in combo) != len(target):
            continue
        n = len(tilings([pieces9[i] for i in combo], target, allow_reflection))
        if n:
            out[frozenset(combo)] = n
    return out


# --------------------------------------------------------------------------
# small self-test on a KNOWN, hand-built exact instance (no external source)
# --------------------------------------------------------------------------

if __name__ == "__main__":
    # sanity 1: an L-tromino and an I-tromino do NOT both fit unless areas match;
    #           two L-trominoes tile a 2x3 rectangle.
    L = normalize([(0, 0), (1, 0), (1, 1)])
    rect23 = {(r, c) for r in range(2) for c in range(3)}
    n = len(tilings([L, L], rect23))
    print(f"[test] two L-trominoes tiling 2x3: {n} tilings (expect > 0):", n > 0)

    # sanity 2: orientation count of an L-tromino under D4 is 4 (it is chiral-free)
    print(f"[test] L-tromino orientations (D4): {len(orientations(L))}  (expect 4)")

    # sanity 3: a 1x1 and a domino and an L-tromino tile an L-hexomino? area 1+2+3=6
    mono = normalize([(0, 0)])
    domino = normalize([(0, 0), (0, 1)])
    # target: 2x3 rectangle again (area 6)
    print(f"[test] mono+domino+L tiling 2x3 (area 6):",
          tiles([mono, domino, L], rect23))

    # sanity 4: the P-pentomino tiles nothing of area 5 that is 1x5 (too wide)
    P = normalize([(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)])
    row5 = {(0, c) for c in range(5)}
    print(f"[test] P-pentomino in 1x5 strip (should NOT fit):",
          not tiles([P], row5))
    print("engine self-test done.")
