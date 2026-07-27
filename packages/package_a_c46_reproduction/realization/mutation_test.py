"""Mutation testing of the verifier: perturb certificates in ways that MUST be
caught. If the verifier accepts any mutation, it is unsound (vacuous)."""
import json, copy
from pathlib import Path
from verify import verify_one, T, PLAC

HERE = Path(__file__).resolve().parent
b=json.loads((HERE / 'R_certificates.json').read_text(encoding='utf-8'))
certs=b["certificates"]
pos_key=next(k for k,c in certs.items() if c["tiles"])
neg_key=next(k for k,c in certs.items() if not c["tiles"])
Tsorted=sorted([r,c] for (r,c) in T)

rows=[]
def case(name, cert, must_reject=True):
    fails=verify_one(cert)
    rejected=len(fails)>0
    ok = rejected==must_reject
    rows.append((ok, name, "REJECTED" if rejected else "accepted", fails[:1]))

# controls: the genuine certificates must PASS
case("control: genuine positive passes",  certs[pos_key], must_reject=False)
case("control: genuine negative passes",  certs[neg_key], must_reject=False)

# M1 shift one placement by (0,1)
m=copy.deepcopy(certs[pos_key])
m["placements"][0]["cells"]=[[r,c+1] for r,c in m["placements"][0]["cells"]]
case("M1 placement shifted by (0,1)", m)

# M2 wrong shape (same size, but not congruent to the piece)
m=copy.deepcopy(certs[pos_key]); a=m["placements"][0]["area"]
m["placements"][0]["cells"]=[list(x) for x in Tsorted[:a]]
case("M2 wrong-shape placement", m)

# M3 drop one cell (gap + area mismatch)
m=copy.deepcopy(certs[pos_key])
m["placements"][0]["cells"]=m["placements"][0]["cells"][1:]
case("M3 dropped cell (gap)", m)

# M4 false refutation: a true tiling marked no-tiling
m=copy.deepcopy(certs[pos_key]); m["tiles"]=False; m.pop("placements",None)
case("M4 false refutation (tiles=False on a real cover)", m)

# M5 fake cover on a genuine negative: real congruent placements that cannot partition
m=copy.deepcopy(certs[neg_key]); m["tiles"]=True
m["placements"]=[{"area":a,"cells":sorted([r,c] for (r,c) in list(PLAC[a])[0])} for a in m["areas"]]
case("M5 fabricated cover on a true negative", m)

# M6 isolate the congruence check: claim the V-pentomino (area 5) is 5 collinear cells
posk5=next((k for k,c in certs.items() if c["tiles"] and 5 in c["areas"]), None)
if posk5:
    m=copy.deepcopy(certs[posk5])
    i=[p["area"] for p in m["placements"]].index(5)
    m["placements"][i]["cells"]=[[0,0],[0,1],[0,2],[0,3],[0,4]]   # I-pentomino, in T, NOT congruent to piece 5
    fails=verify_one(m)
    rows.append((any("congruent" in f for f in fails), "M6 non-congruent shape (isolates congruence)",
                 "REJECTED" if fails else "accepted", [f for f in fails if "congruent" in f][:1]))

allok=all(r[0] for r in rows)
for ok,name,verdict,info in rows:
    print(f"  [{'OK' if ok else 'FAIL'}] {name:52s} -> {verdict} {info}")
print(f"\nmutation test: {'ALL PASS - verifier is sound' if allok else 'VERIFIER UNSOUND'}")
