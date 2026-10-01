#!/usr/bin/env python3
"""Scoping pass: what does the repair question cost on CO_5?

Their question: a repaired conjecture would condition on (5,n)-subsets rather
than (4,n), whose dual lives in CO_5 (24 vertices) rather than CO_4 (6). Is the
label-set family enumeration affordable, and is the resulting search affordable?
"""
from itertools import permutations
from math import comb, log, exp
import time

def verts(n): return [(0,)+p for p in permutations(range(1,n))]
def canon(w):
    k=w.index(0); return tuple(w[k:]+w[:k])
def edges(n):
    out=[]
    for v in verts(n):
        for i in range(n):
            j=(i+1)%n; w=list(v); x,y=w[i],w[j]; w[i],w[j]=w[j],w[i]
            u=canon(w)
            if u!=v: out.append((v,u,frozenset((x,y))))
    return out

for n in (4,5):
    V=verts(n); E=edges(n); L=sorted({l for _,_,l in E}, key=lambda s:sorted(s))
    print(f"CO_{n}: {len(V)} vertices, {n}-regular, {len(L)} labels, "
          f"state space {len(V)}x2^{len(L)} = {len(V)*2**len(L):,}")

n=5
V=verts(n); E=edges(n)
L=sorted({l for _,_,l in E}, key=lambda s:sorted(s)); LI={l:i for i,l in enumerate(L)}
A={}
for u,v,l in E: A.setdefault(u,[]).append((v,LI[l]))

def fam_arbitrary(src):
    seen={(src,0)}; st=[(src,0)]
    while st:
        v,m=st.pop()
        for w,li in A[v]:
            s=(w,m|(1<<li))
            if s not in seen: seen.add(s); st.append(s)
    return seen

def fam_walk(src):
    seen={(src,0)}; st=[(src,0)]
    while st:
        v,m=st.pop()
        for w,li in A[v]:
            b=1<<li
            if m&b: continue
            s=(w,m|b)
            if s not in seen: seen.add(s); st.append(s)
    return seen

def fam_both(src):
    out=set()
    def go(v,vis,m):
        out.add((v,m))
        for w,li in A[v]:
            b=1<<li
            if w in vis or (m&b): continue
            go(w,vis|{w},m|b)
    go(src,{src},0); return out

print()
for name,fn in (("arbitrary",fam_arbitrary),("walk",fam_walk),("both",fam_both)):
    t=time.time(); tot=sum(len(fn(s)) for s in V); el=time.time()-t
    print(f"  {name:>10}: {tot:>8,} distinct (endpoint, label-set) pairs   [{el:.1f}s]")

print()
print("  'path' (vertex-simple, labels may repeat): NOT enumerated.")
print("    Label-distinctness is what bounds a walk's length to <= |labels|.")
print("    Without it a simple path in CO_5 runs to 23 edges, and the naive DFS")
print(f"    is of order 5*4^22 ~ {5*4**22:.1e} paths. At CO_4 it was 594 and free;")
print("    at CO_5 it is the one family that does not scale.")
print()
print("  BUT THE BRACKET DOES NOT NEED IT. The bracket needs the lattice MINIMUM")
print("  and MAXIMUM only -- 'both' and 'arbitrary' -- and both are above, in")
print("  seconds. So the convention question remains decidable at CO_5 at the same")
print("  cost structure as CO_4, even though exhaustive per-reading checking does")
print("  not survive the move. The instrument scales; the thing it replaces does not.")

print()
print("=" * 70)
print("WITNESS SPACE -- the part that decides affordability")
for (m,nn,dual) in ((4,6,4),(5,6,5),(5,7,5)):
    print(f"  ({m},{nn})-set: N is an ({nn},{m})-set, so N in V(CO_{dual})^{nn} = "
          f"{len(verts(dual))}^{nn} = {len(verts(dual))**nn:,}")
print(f"  ratio (5,6) vs (4,6): {24**6/6**6:,.0f}x more witnesses per tightness test")
print()
print("  POPULATION, if enumerating classes rather than extending known ones:")
g6 = 2*720
raw = comb(120+5-1,5)
print(f"    (5,6)-sets: 5-multisets from |V(CO_6)|=120 -> C(124,5) = {raw:,}")
print(f"    /|group| = 2*6! = {g6} gives a lower bound of ~{raw//g6:,} classes")
print(f"    against 6,930 for (4,6) -- about {raw//g6/6930:.0f}x more")
print()
print("  THEIR CHEAP TEST IS THE RIGHT ONE and it avoids all of that: extend each")
print("  of the 14 core (4,6)-sets by one element of V(CO_6), giving 14 x 120 =")
print(f"    {14*120:,} (5,6)-sets, and ask whether the stronger condition catches them.")
print(f"    Cost is {14*120:,} tightness tests over 24^6 = {24**6:,} witnesses each,")
print("    with backtracking and constraint propagation -- the same search shape")
print("    that ran in seconds at 6^6, now against a domain 4x larger per variable.")
print("    VERDICT: scoping-feasible, not free. Budget it as a run, not a check.")

print()
print("=" * 70)
print("THEIR RETRACTION ARITHMETIC, checked")
for rate,lbl in ((14/6930,"n=6 reading-independent"),(733/66390,"n=7 reading-independent")):
    exp_n = 131*rate
    p0 = (1-rate)**131
    print(f"  rate {rate*100:.2f}% ({lbl}): expected over 131 classes = {exp_n:.2f}, "
          f"P(observe 0) = {p0:.2f}")
print("  => zero of 131 is unremarkable at either rate. Their retraction is correct:")
print("     the n=5 null is a FACT and is not evidence of structural absence.")
