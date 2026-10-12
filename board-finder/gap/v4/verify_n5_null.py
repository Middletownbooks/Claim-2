#!/usr/bin/env python3
"""The n=5 null under all four readings, and a direct test of non-monotonicity.

The n=5 null is a UNIVERSAL NEGATIVE over a non-monotone conjunction, which is
exactly where the bracket instrument fails. So it must be checked at every
reading separately -- the point the other instance correctly made. Done here.
"""
from itertools import permutations, product, combinations_with_replacement as cwr
from collections import deque
import random, sys
exec(open('/home/user/claim-2/board-finder/gap/v4/verify_fourteen.py').read().split('RAW = """')[0])

# ------------------------------------------------- the other two readings
def fam_walk(src):
    out=set(); seen={(src,0)}; st=[(src,0)]
    while st:
        v,m=st.pop(); out.add((v,m))
        for w,l in A4[v]:
            b=1<<LI[l]
            if not (m&b) and (w,m|b) not in seen: seen.add((w,m|b)); st.append((w,m|b))
    return out
def fam_path(src):
    out=set()
    def go(v,vis,m):
        out.add((v,m))
        for w,l in A4[v]:
            if w in vis: continue
            go(w,vis|{w},m|(1<<LI[l]))
    go(src,{src},0); return out
WALK={s:fam_walk(s) for s in verts(4)}; PATH={s:fam_path(s) for s in verts(4)}
FAMS={"both":BOTH, "walk":WALK, "path":PATH, "arbitrary":ANY}
QS={k:{(u,v):q(f,u,v) for u in verts(4) for v in verts(4)} for k,f in FAMS.items()}
print("family sizes:", {k: sum(len(f[s]) for s in verts(4)) for k,f in FAMS.items()})

# ------------------------------------------------- isomorphism classes of (4,n)-sets
def group(n):
    """S_n on the ground set, composed with reversal: order 2*n!."""
    g=[]
    for s in permutations(range(n)):
        g.append((s, False)); g.append((s, True))
    return g
def act(v, s, r):
    w = canon([s[x] for x in v])
    return rev(w) if r else w
def classes(n):
    G=group(n); V=verts(n); seen=set(); out=[]
    for M in cwr(V, 4):
        key=min(tuple(sorted(act(v,s,r) for v in M)) for s,r in G)
        if key not in seen: seen.add(key); out.append(key)
    return out

def is_ce(M, n, A, fam_key):
    P,SLS,XY,F,PO = analyse(list(M), n, A)
    Q = QS[fam_key]
    # pseudo-tight: does SOME N work?
    nbrP={k:[] for k in range(n)}
    for x,y in XY:
        fm,pm=mask_of(F[(x,y)]),mask_of(PO[(x,y)])
        nbrP[x].append((y,fm,pm,True)); nbrP[y].append((x,fm,pm,False))
    asg=[None]*n
    def btp(k):
        if k==n: return True
        for cand in V4:
            ok=True
            for (o,fm,pm,fwd) in nbrP[k]:
                if asg[o] is None: continue
                u,v=(cand,asg[o]) if fwd else (asg[o],cand)
                if not any((m&fm)==fm and (m|pm)==pm for m in Q[(u,v)]): ok=False;break
            if ok:
                asg[k]=cand
                if btp(k+1): return True
                asg[k]=None
        return False
    if not btp(0): return False
    return not is_tight(P,SLS,XY,Q,n)

A5=adjof(5)
print()
print("1. n = 5, EXHAUSTIVE over isomorphism classes, all four readings")
C5=classes(5)
ck("isomorphism classes of (4,5)-sets", len(C5), 131)
counts5={k: sum(1 for M in C5 if is_ce(M,5,A5,k)) for k in FAMS}
print(f"      {counts5}")
ck("n=5 null holds under EVERY reading", set(counts5.values()), {0})
print("      => confirmed independently. This is the half the bracket CANNOT do:")
print("         a universal negative over a non-monotone conjunction has to be")
print("         checked at each reading, and it was.")

print()
print("2. Is the conjunction really non-monotone? A direct search at n = 6.")
A6=adjof(6); V6=verts(6); random.seed(20261001)
found=None; tested=0
while tested < 4000 and found is None:
    M=tuple(sorted(random.choices(V6, k=4)))
    tested+=1
    verd={k: is_ce(M,6,A6,k) for k in FAMS}
    if len(set(verd.values()))>1:
        found=(M,verd)
print(f"      sampled {tested} random (4,6)-sets")
if found:
    M,verd=found
    print(f"      FOUND a reading-dependent class: {[''.join(map(str,v)) for v in M]}")
    print(f"        {verd}")
    ck("the conjunction is NOT monotone in the family -- verdicts differ by reading",
       len(set(verd.values())), 2)
    print("      => confirms their window finding directly: a class can be a")
    print("         counterexample under one reading and not another, so COUNTS")
    print("         cannot be bracketed even though each FIXED object can.")
else:
    print("      none found in this sample; their 45 reading-dependent of 6,930")
    print("      is 0.65%, so ~26 expected in 4000 -- absence here would be odd.")
    FAIL.append("expected a reading-dependent class")

print()
print("="*72)
if FAIL: print(f"{len(FAIL)} FAILED: {FAIL}"); sys.exit(1)
print("n=5 null confirmed at every reading; non-monotonicity confirmed directly.")
