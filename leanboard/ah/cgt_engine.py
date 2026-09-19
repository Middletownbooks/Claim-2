#!/usr/bin/env python3
"""A from-scratch combinatorial-game engine, used to check Mazur's central claim
    G(B) = {17/8 | -2+*}
independently of the paper's five routes.

Design note: NO canonicalization is used. Conway's order relation is valid on arbitrary
forms, so raw memoized game trees suffice and there is one less place to be wrong.

    X <= Y  <=>  (no X^L with Y <= X^L)  and  (no Y^R with Y^R <= X)

Games are hash-consed nodes: (tuple of left child ids, tuple of right child ids).
Board games and constructed target games live in the same node space, so they compare
directly.
"""
from fractions import Fraction as F
import sys
sys.setrecursionlimit(100000)

NODES, INTERN = [], {}
def mk(L, R):
    key = (tuple(sorted(set(L))), tuple(sorted(set(R))))
    if key in INTERN: return INTERN[key]
    i = len(NODES); NODES.append(key); INTERN[key] = i
    return i

ZERO = mk([], [])
STAR = mk([ZERO], [ZERO])

_leq = {}
def leq(x, y):
    k = (x, y)
    if k in _leq: return _leq[k]
    _leq[k] = True                      # coinductive guard; DAG is well-founded so safe
    xL, _ = NODES[x]; _, yR = NODES[y]
    r = (not any(leq(y, a) for a in xL)) and (not any(leq(b, x) for b in yR))
    _leq[k] = r
    return r

def eq(x, y): return leq(x, y) and leq(y, x)

_add = {}
def add(x, y):
    k = (x, y) if x <= y else (y, x)
    if k in _add: return _add[k]
    xL, xR = NODES[x]; yL, yR = NODES[y]
    L = [add(a, y) for a in xL] + [add(x, a) for a in yL]
    R = [add(b, y) for b in xR] + [add(x, b) for b in yR]
    r = mk(L, R); _add[k] = r
    return r

_neg = {}
def neg(x):
    if x in _neg: return _neg[x]
    xL, xR = NODES[x]
    _neg[x] = None
    r = mk([neg(b) for b in xR], [neg(a) for a in xL])
    _neg[x] = r
    return r

_num = {}
def num(v):
    """Canonical game for a dyadic rational."""
    v = F(v)
    if v in _num: return _num[v]
    if v.denominator == 1:
        n = v.numerator
        r = ZERO if n == 0 else (mk([num(n-1)], []) if n > 0 else mk([], [num(n+1)]))
    else:
        d = v.denominator                       # a power of two, v not an integer
        r = mk([num(F(v.numerator-1, d))], [num(F(v.numerator+1, d))])
    _num[v] = r
    return r

# ---- Domineering ----------------------------------------------------------------
B = [(0,0),(0,1),(0,2),(1,2),(1,5),(1,7),(2,2),(2,5),(2,6),(2,7),
     (3,2),(3,3),(3,4),(3,5),(3,6),(4,4),(4,5),(4,6),
     (5,2),(5,3),(5,4),(6,2),(7,2),(8,0),(8,1),(8,2)]
IDX = {c: i for i, c in enumerate(B)}
FULL = (1 << 26) - 1
VMOVES = [(1 << IDX[(x,y)]) | (1 << IDX[(x,y+1)]) for (x,y) in B if (x,y+1) in IDX]
HMOVES = [(1 << IDX[(x,y)]) | (1 << IDX[(x+1,y)]) for (x,y) in B if (x+1,y) in IDX]

_g = {}
def G(mask):
    if mask in _g: return _g[mask]
    L = [G(mask ^ m) for m in VMOVES if mask & m == m]
    R = [G(mask ^ m) for m in HMOVES if mask & m == m]
    r = mk(L, R); _g[mask] = r
    return r

if __name__ == "__main__":
    print(f"legal moves on B: {len(VMOVES)} vertical, {len(HMOVES)} horizontal")
    gB = G(FULL)
    print(f"game DAG built: {len(_g)} board masks, {len(NODES)} interned game forms")

    t_17_8 = num(F(17,8))
    t_m2s  = add(num(-2), STAR)                    # -2 + *
    TARGET = mk([t_17_8], [t_m2s])                 # {17/8 | -2+*}

    print("\n--- proposition 4.1: the two crossing followers -----------------")
    C, U, W = (3,5), (3,6), (4,5)
    mCU = (1 << IDX[C]) | (1 << IDX[U])
    mCW = (1 << IDX[C]) | (1 << IDX[W])
    gL, gR = G(FULL ^ mCU), G(FULL ^ mCW)
    print(f"  G(B - C-U) == 17/8      : {eq(gL, t_17_8)}")
    print(f"  G(B - C-W) == -2+*      : {eq(gR, t_m2s)}")

    print("\n--- dominance (4.2)/(4.3) and uniqueness of equality ------------")
    okL = eqL = 0
    for m in VMOVES:
        g = G(FULL ^ m)
        if leq(g, t_17_8): okL += 1
        if eq(g, t_17_8):  eqL += 1
    okR = eqR = 0
    for m in HMOVES:
        g = G(FULL ^ m)
        if leq(t_m2s, g): okR += 1
        if eq(g, t_m2s):  eqR += 1
    print(f"  Left  options with G <= 17/8 : {okL}/{len(VMOVES)}   attaining equality: {eqL}")
    print(f"  Right options with -2+* <= G : {okR}/{len(HMOVES)}   attaining equality: {eqR}")

    print("\n--- the main value claim ----------------------------------------")
    print(f"  G(B) == {{17/8 | -2+*}} : {eq(gB, TARGET)}")

    print("\n--- route 4 cross-check: difference game is a second-player win --")
    diff = add(gB, neg(TARGET))
    print(f"  G(B) + (-{{17/8 | -2+*}}) == 0 : {eq(diff, ZERO)}")
    negT = neg(TARGET)
    print(f"  -TARGET == {{2+* | -17/8}}     : "
          f"{eq(negT, mk([add(num(2), STAR)], [num(F(-17,8))]))}")
    print(f"\ntotal interned game forms: {len(NODES)}")
