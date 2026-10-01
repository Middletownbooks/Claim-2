#!/usr/bin/env python3
"""Their repair test, run -- and it is far cheaper than either of us costed.

Key simplification, from Woodall p.663: "every subset of a tight set is tight".
Contrapositive: an extension of a NON-TIGHT set is non-tight. So extending each
of the 14 core (4,6)-sets by one element gives a (5,6)-set that is AUTOMATICALLY
not tight -- the expensive half is free. The test reduces to a PSEUDO-TIGHTNESS
check on the extension, which is one CSP with no row-choice enumeration.

If some extension is pseudo-tight, it is a (5,6)-set that is pseudo-tight and
not tight, so a (5,n)-subset condition does NOT catch these and the repair fails
at that level. If no extension is pseudo-tight, the (5,n) condition catches them.
"""
from itertools import permutations, product
from collections import deque
import time, sys

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

A6=adjof(6); A5=adjof(5); V5=verts(5); V6=verts(6)
L5=sorted({l for _,_,l in edges(5)}, key=lambda s:sorted(s)); LI5={l:i for i,l in enumerate(L5)}
def mask5(S): return sum(1<<LI5[l] for l in S)

def fam(src, A, LI, simple, labdist):
    out=set()
    if simple:
        def go(v,vis,m):
            out.add((v,m))
            for w,l in A[v]:
                b=1<<LI[l]
                if w in vis or (labdist and (m&b)): continue
                go(w,vis|{w},m|b)
        go(src,{src},0)
    else:
        seen={(src,0)}; st=[(src,0)]
        while st:
            v,m=st.pop(); out.add((v,m))
            for w,l in A[v]:
                b=1<<LI[l]
                if labdist and (m&b): continue
                s=(w,m|b)
                if s not in seen: seen.add(s); st.append(s)
    return out

print("Building the two bracket families on CO_5 (24 vertices, 10 labels)")
t=time.time()
BOTH5={s:fam(s,A5,LI5,True,True) for s in V5}
ANY5 ={s:fam(s,A5,LI5,False,False) for s in V5}
print(f"  both {sum(len(x) for x in BOTH5.values()):,}   "
      f"arbitrary {sum(len(x) for x in ANY5.values()):,}   [{time.time()-t:.1f}s]")
def qset(F,x,y):
    t_=rev(y); return {m for (v,m) in F[x] if v==t_}
QB={(u,v):qset(BOTH5,u,v) for u in V5 for v in V5}
QA={(u,v):qset(ANY5 ,u,v) for u in V5 for v in V5}

def bfs(a,A):
    d={a:0}; dq=deque([a])
    while dq:
        u=dq.popleft()
        for w,_ in A[u]:
            if w not in d: d[w]=d[u]+1; dq.append(w)
    return d

def forced_possible(M, n, A):
    P=[(i,j) for i in range(len(M)) for j in range(i+1,len(M))]
    SLS={}
    for i,j in P:
        a,t_=M[i],rev(M[j]); da,dt=bfs(a,A),bfs(t_,A); D=da[t_]; res=set()
        def go(v,m):
            if v==t_: res.add(m); return
            for w,l in A[v]:
                if da[w]==da[v]+1 and da[w]+dt[w]==D: go(w,m|frozenset([l]))
        go(a,frozenset()); SLS[(i,j)]=res
    XY=[(x,y) for x in range(n) for y in range(n) if x<y]
    F,PO={},{}
    for x,y in XY:
        lab=frozenset((x,y)); f,p=set(),set()
        for (i,j) in P:
            s=SLS[(i,j)]
            if all(lab in u for u in s): f.add(frozenset((i,j)))
            if any(lab in u for u in s): p.add(frozenset((i,j)))
        F[(x,y)],PO[(x,y)]=frozenset(f),frozenset(p)
    return XY,F,PO

def pseudotight(M, n, A, Q, V, mk):
    XY,F,PO = forced_possible(M, n, A)
    allow={}
    for x,y in XY:
        fm,pm=mk(F[(x,y)]),mk(PO[(x,y)])
        tb={}
        for u in V:
            for v in V:
                tb[(u,v)]=any((m&fm)==fm and (m|pm)==pm for m in Q[(u,v)])
        allow[(x,y)]=tb
    nbr={k:[] for k in range(n)}
    for x,y in XY: nbr[x].append((y,x,y)); nbr[y].append((x,x,y))
    asg=[None]*n
    def bt(k):
        if k==n: return True
        for cand in V:
            ok=True
            for (o,lo,hi) in nbr[k]:
                if asg[o] is None: continue
                u,v=(cand,asg[o]) if lo==k else (asg[o],cand)
                if not allow[(lo,hi)][(u,v)]: ok=False; break
            if ok:
                asg[k]=cand
                if bt(k+1): return True
                asg[k]=None
        return False
    return bt(0)

CORE = """012345 014532 032514 054231
012345 013542 032541 045231
012345 013524 032541 045231
012345 014532 032514 042315
012345 013542 032541 042531
012345 013542 032541 052314
012345 013542 021453 031254
012345 013542 032541 042513
012345 013542 032415 042513
012345 013524 032541 045213
012345 013254 021534 052143
012345 012453 023154 052143
012345 013254 025134 052143
012345 012453 031524 041325"""
CORE=[[tuple(int(c) for c in t) for t in ln.split()] for ln in CORE.strip().split("\n")]

print()
print("Extending each of the 14 by one element of V(CO_6): 14 x 120 = 1,680 sets.")
print("Non-tightness is INHERITED (p.663: every subset of a tight set is tight),")
print("so only pseudo-tightness of the extension has to be computed.")
print()
print("  A (5,6)-set extension that is PSEUDO-TIGHT is pseudo-tight AND not tight,")
print("  i.e. a counterexample at m = 5 -- the (5,n)-subset repair would NOT catch it.")
print()
t0=time.time(); rows=[]
for idx,M4 in enumerate(CORE,1):
    hits_b=hits_a=0
    for e in V6:
        M5=M4+[e]
        if pseudotight(M5,6,A6,QB,V5,mask5): hits_b+=1
        if pseudotight(M5,6,A6,QA,V5,mask5): hits_a+=1
    rows.append((idx,hits_b,hits_a))
    print(f"  core #{idx:>2}: pseudo-tight extensions -- at 'both' {hits_b:>3}/120, "
          f"at 'arbitrary' {hits_a:>3}/120   [{time.time()-t0:.0f}s]")
tb=sum(r[1] for r in rows); ta=sum(r[2] for r in rows)
print()
print(f"  TOTAL: {tb}/1680 at 'both', {ta}/1680 at 'arbitrary'   [{time.time()-t0:.0f}s]")
print()
if tb>0:
    print("  => THE (5,n) REPAIR FAILS. There exist (5,6)-sets that are pseudo-tight")
    print("     and not tight, so strengthening the subset size from 4 to 5 does not")
    print("     restore the equivalence -- it is refuted at m = 5 by extensions of")
    print("     the very counterexamples that refuted it at m = 4.")
else:
    print("  => THE (5,n) CONDITION CATCHES ALL 14. No extension of any core case is")
    print("     pseudo-tight, so at least on this evidence the repair survives.")
