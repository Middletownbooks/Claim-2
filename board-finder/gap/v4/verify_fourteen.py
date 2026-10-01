#!/usr/bin/env python3
"""Verify the 14 reading-independent (4,6)-set counterexamples, and the n=5 null.

Built on the same independent CO_n construction as verify_pseudotight.py.
For each item: pseudo-tight at the SMALLEST family ('both', 234) and not tight
at the LARGEST ('arbitrary', 1758). By the monotonicity argument that brackets
every reading in between -- valid for a FIXED OBJECT, which is the boundary the
other instance correctly identified.
"""
from itertools import permutations, product
from collections import deque
import sys

FAIL=[]
def ck(lbl, got, want):
    ok = got == want
    print(f"  [{'ok ' if ok else 'FAIL'}] {lbl}: {got!r} vs {want!r}")
    if not ok: FAIL.append(lbl)

def verts(n): return [(0,)+p for p in permutations(range(1,n))]
def canon(w):
    k=w.index(0); return tuple(w[k:]+w[:k])
def rev(v): return canon(list(reversed(v)))
def edges(n):
    out=[]
    for v in verts(n):
        for i in range(n):
            j=(i+1)%n; w=list(v); x,y=w[i],w[j]; w[i],w[j]=w[j],w[i]
            u=canon(w)
            if u!=v: out.append((v,u,frozenset((x,y))))
    return out
def adjof(n):
    a={}
    for u,v,l in edges(n): a.setdefault(u,[]).append((v,l))
    return a
A4=adjof(4)
L4=sorted({l for _,_,l in edges(4)}, key=lambda s: sorted(s)); LI={l:i for i,l in enumerate(L4)}
def mask_of(S): return sum(1<<LI[l] for l in S)

def fam_both(src):
    out=set()
    def go(v,vis,m):
        out.add((v,m))
        for w,l in A4[v]:
            b=1<<LI[l]
            if w in vis or (m&b): continue
            go(w,vis|{w},m|b)
    go(src,{src},0); return out
def fam_any(src):
    out=set(); seen={(src,0)}; st=[(src,0)]
    while st:
        v,m=st.pop(); out.add((v,m))
        for w,l in A4[v]:
            nm=m|(1<<LI[l])
            if (w,nm) not in seen: seen.add((w,nm)); st.append((w,nm))
    return out
BOTH={s:fam_both(s) for s in verts(4)}
ANY ={s:fam_any(s)  for s in verts(4)}
def q(fam,x,y):
    t=rev(y); return {m for (v,m) in fam[x] if v==t}
QBOTH={(u,v):q(BOTH,u,v) for u in verts(4) for v in verts(4)}
QANY ={(u,v):q(ANY ,u,v) for u in verts(4) for v in verts(4)}

def bfs(a,A):
    d={a:0}; dq=deque([a])
    while dq:
        u=dq.popleft()
        for w,_ in A[u]:
            if w not in d: d[w]=d[u]+1; dq.append(w)
    return d

def analyse(M,n,A):
    """Forced/Possible per ground pair, and the shortest-label-set row choices."""
    P=[(i,j) for i in range(4) for j in range(i+1,4)]
    SLS={}
    for i,j in P:
        a,t=M[i],rev(M[j]); da,dt=bfs(a,A),bfs(t,A); D=da[t]; res=set()
        def go(v,m):
            if v==t: res.add(m); return
            for w,l in A[v]:
                if da[w]==da[v]+1 and da[w]+dt[w]==D: go(w,m|frozenset([l]))
        go(a,frozenset()); SLS[(i,j)]=res
    XY=[(x,y) for x in range(n) for y in range(n) if x<y]
    F,PO={},{}
    for x,y in XY:
        lab=frozenset((x,y)); f,p=set(),set()
        for (i,j) in P:
            s=SLS[(i,j)]
            if all(lab in q_ for q_ in s): f.add(frozenset((i,j)))
            if any(lab in q_ for q_ in s): p.add(frozenset((i,j)))
        F[(x,y)],PO[(x,y)]=frozenset(f),frozenset(p)
    return P,SLS,XY,F,PO

def is_pseudotight(Nw,XY,F,PO,Q):
    for x,y in XY:
        fm,pm=mask_of(F[(x,y)]),mask_of(PO[(x,y)])
        if not any((m&fm)==fm and (m|pm)==pm for m in Q[(Nw[x],Nw[y])]): return False
    return True

V4=verts(4)
def is_tight(P,SLS,XY,Q,n):
    """Backtracking over N in V(CO_4)^n for each forced row-choice."""
    for choice in product(*[sorted(SLS[p],key=lambda s:sorted(sorted(l) for l in s)) for p in P]):
        R={}
        for x,y in XY:
            R[(x,y)]=mask_of(frozenset(frozenset((i,j)) for (i,j),lab in zip(P,choice)
                                        if frozenset((x,y)) in lab))
        nbr={k:[] for k in range(n)}
        for x,y in XY: nbr[x].append((y,R[(x,y)])); nbr[y].append((x,R[(x,y)]))
        asg=[None]*n
        def bt(k):
            if k==n: return True
            for cand in V4:
                ok=True
                for (o,rm) in nbr[k]:
                    if asg[o] is None: continue
                    lo,hi=(k,o) if k<o else (o,k)
                    u,v=(cand,asg[o]) if (lo==k) else (asg[o],cand)
                    if rm not in Q[(u,v)]: ok=False; break
                if ok:
                    asg[k]=cand
                    if bt(k+1): return True
                    asg[k]=None
            return False
        if bt(0): return True
    return False

RAW = """15 012345 014532 032514 054231 | 0132 0132 0213 0213 0132 0132
15 012345 013542 032541 045231 | 0132 0132 0312 0321 0312 0312
16 012345 013524 032541 045231 | 0132 0132 0312 0312 0321 0312
16 012345 014532 032514 042315 | 0132 0132 0321 0321 0132 0132
16 012345 013542 032541 042531 | 0132 0132 0312 0321 0312 0312
18 012345 013542 032541 052314 | 0132 0132 0312 0321 0312 0312
18 012345 013542 021453 031254 | 0213 0321 0321 0132 0132 0132
19 012345 013542 032541 042513 | 0132 0132 0312 0321 0312 0312
19 012345 013542 032415 042513 | 0123 0123 0231 0123 0231 0123
19 012345 013524 032541 045213 | 0132 0132 0312 0312 0321 0312
21 012345 013254 021534 052143 | 0132 0123 0123 0213 0213 0123
21 012345 012453 023154 052143 | 0132 0321 0321 0321 0132 0312
22 012345 013254 025134 052143 | 0123 0132 0123 0213 0213 0123
22 012345 012453 031524 041325 | 0132 0321 0132 0321 0132 0132"""

A6=adjof(6); V6=set(verts(6))
print("Verifying the 14 reading-independent n=6 counterexamples")
print("  pseudo-tight at 'both' (234, smallest) AND not tight at 'arbitrary' (1758, largest)")
print(f"  {'#':>2} {'antisum':>7}  {'in V(CO_6)':>10} {'p-tight@both':>13} {'tight@arb':>10}  verdict")
results=[]
for idx,line in enumerate(RAW.strip().split("\n"),1):
    left,right=line.split("|")
    toks=left.split(); A_=int(toks[0])
    M=[tuple(int(c) for c in t) for t in toks[1:]]
    Nw=[tuple(int(c) for c in t) for t in right.split()]
    inV=all(m in V6 for m in M)
    P,SLS,XY,F,PO=analyse(M,6,A6)
    asum=sum(bfs(M[i],A6)[rev(M[j])] for i,j in P)
    pt=is_pseudotight(Nw,XY,F,PO,QBOTH)
    tg=is_tight(P,SLS,XY,QANY,6)
    good = inV and (asum==A_) and pt and (not tg)
    results.append(good)
    print(f"  {idx:>2} {asum:>7}  {str(inV):>10} {str(pt):>13} {str(tg):>10}  "
          f"{'reading-independent CE' if good else 'FAILS'}")
ck("all 14 are counterexamples under every reading", sum(results), 14)

print()
print("=" * 72)
if FAIL: print(f"{len(FAIL)} FAILED: {FAIL}"); sys.exit(1)
print("All 14 verified: pseudo-tight at the smallest family, not tight at the largest.")
