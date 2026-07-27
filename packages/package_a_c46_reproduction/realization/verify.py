"""INDEPENDENT verifier for R_certificates.json (second engine — its own D4,
orientation, placement and exact-cover code, not geomagic_engine). It re-derives
everything from the LOCKED pieces+target (c46_verify), so it verifies the math,
not the generator's word.

  positive: each placement must be D4-congruent to its locked piece, lie in T,
            and the four must partition T exactly.
  negative: an independent exhaustive exact-cover must find 0 tilings.
Also checks the bundle's normalization block equals the locked pieces+target."""
import json
from pathlib import Path
from c46_locked import PIECE, TARGET
HERE = Path(__file__).resolve().parent
T=frozenset(TARGET)

def _rot(cells): return [(c,-r) for r,c in cells]
def _refl(cells): return [(r,-c) for r,c in cells]
def norm(cells):
    r0=min(r for r,c in cells); c0=min(c for r,c in cells)
    return tuple(sorted((r-r0,c-c0) for r,c in cells))
def orbit(cells):
    out=set(); cur=list(cells)
    for _ in range(4):
        out.add(norm(cur)); out.add(norm(_refl(cur))); cur=_rot(cur)
    return out
ORBIT={a:orbit(PIECE[a]) for a in range(1,17)}

def own_placements(area):
    rs=[r for r,c in T]; cs=[c for r,c in T]
    minr,maxr,minc,maxc=min(rs),max(rs),min(cs),max(cs)
    out=[]
    for ori in ORBIT[area]:
        h=max(r for r,c in ori); w=max(c for r,c in ori)
        for dr in range(minr,maxr-h+1):
            for dc in range(minc,maxc-w+1):
                pl=frozenset((r+dr,c+dc) for r,c in ori)
                if pl<=T: out.append(pl)
    return out
PLAC={a:own_placements(a) for a in range(1,17)}

def has_cover(areas):
    plc=[PLAC[a] for a in areas]
    if any(len(x)==0 for x in plc): return False
    order=sorted(range(4), key=lambda i:len(plc[i]))
    def rec(k, rem):
        if k==4: return not rem
        for pl in plc[order[k]]:
            if pl<=rem and rec(k+1, rem-pl): return True
        return False
    return rec(0, T)

def verify_one(c):
    """return list of problems with a single certificate (empty == valid)."""
    fails=[]; areas=c["areas"]
    if c["tiles"]:
        placed=[]; pareas=[]
        for pr in c["placements"]:
            pl=frozenset(tuple(x) for x in pr["cells"]); a=pr["area"]
            placed.append(pl); pareas.append(a)
            if len(pl)!=a: fails.append("area mismatch (size or duplicate cells)"); continue
            if not (pl<=T): fails.append("outside T"); continue
            if norm(pl) not in ORBIT[a]: fails.append(f"not congruent to piece {a}")
        if sorted(pareas)!=sorted(areas): fails.append("wrong pieces")
        union=set(); overlap=False
        for pl in placed:
            if union & pl: overlap=True
            union|=pl
        if overlap or union!=set(T): fails.append("not an exact partition")
    else:
        if has_cover(areas): fails.append("REFUTATION FALSE - a cover exists")
    return fails

def main():
    b=json.loads((HERE / 'R_certificates.json').read_text(encoding='utf-8'))
    nz=b["normalization"]
    assert [tuple(x) for x in nz["target_cells"]]==sorted(T), "target mismatch"
    for a in range(1,17):
        assert norm([tuple(x) for x in nz["pieces"][str(a)]])==PIECE[a], f"piece {a} mismatch"
    certs=b["certificates"]
    assert len(certs)==86, f"expected 86 certs, got {len(certs)}"
    pos=neg=0; fails=[]
    for key,c in certs.items():
        if c["tiles"]: pos+=1
        else: neg+=1
        for f in verify_one(c): fails.append((key,f))
    R=pos
    print(f"certificates: {len(certs)}  positive(verified tile): {pos}  negative(verified no-tile): {neg}")
    print(f"failures: {len(fails)}")
    for f in fails[:10]: print("   ",f)
    print(f"\nVERIFIED R = {R}  (independent second engine)  ALL_OK={len(fails)==0}")
    return len(fails)==0
if __name__=="__main__":
    import sys; sys.exit(0 if main() else 1)
