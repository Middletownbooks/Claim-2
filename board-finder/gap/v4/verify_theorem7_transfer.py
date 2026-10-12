#!/usr/bin/env python3
"""Item (1), discharged: does Theorem 2's argument transfer to antisums with the
same coefficients, and do the deficits propagate as reconstructed?

Woodall's proof of Theorem 7 (p.665) is one line: "This follows by the argument
of Theorem 2 with 'number of crossings' replaced by 'sum of antidistances'."
So the transfer has to be checked against Theorem 2's printed proof (pp.658-659),
term by term. That is a reading task on page images, which is why the other
instance handed it back. Done here; the algebra is then asserted numerically.
"""
from math import comb
FAIL=[]
def ck(l,g,w):
    ok=g==w; print(f"  [{'ok ' if ok else 'FAIL'}] {l}: {g!r} vs {w!r}")
    if not ok: FAIL.append(l)
def Z(n): return (n//2)*((n-1)//2)

print("THEOREM 2's proof, p.659, term by term -- and its antisum image")
print()
print("  'Each crossing in the drawing of K_{m,n} involves exactly one pair of")
print("   vertices u, v in M.'")
print("   ANTISUM IMAGE: the antisum of M is BY DEFINITION the sum over all C(m,2)")
print("   pairs of their antidistances (p.661), so it partitions by pair exactly.")
print("   The transfer is not merely analogous here -- it is definitional, and the")
print("   partition is exact rather than 'at least'.")
print()
print("  TERM 1. 'The number of crossings corresponding to vertices u, v in M'")
print("   is k.'  -> the antisum of M', which the theorem bounds by k <= Z(m')Z(n).")
print()
print("  TERM 2. '...u and v both in M \\ M' is at least cr(K_{m-m',n}).'")
print("   -> M \\ M' is an (m-m', n)-set, so the hypothesis 'every (m-m',n)-set has")
print("   antisum at least Z(m-m')Z(n)' applies DIRECTLY. One application.")
print()
print("  TERM 3. '...u in M' and v in M \\ M' is at least (m-m')[cr(K_{m'+1,n}) - k].'")
print("   -> THIS IS THE TERM THE MULTIPLIER LIVES ON, and it transfers because:")
print("      for each of the m-m' elements v of M \\ M', the set M' + {v} is an")
print("      (m'+1, n)-SET, so the hypothesis gives")
print("          A(M') + sum_{u in M'} dbar(u,v)  >=  Z(m'+1)Z(n),")
print("      i.e. v's cross-contribution >= Z(m'+1)Z(n) - k. Summing the m-m'")
print("      inequalities, one per v, gives the stated bound.")
print("   SO THE (m-m') MULTIPLIER IS THE COUNT OF ELEMENTS OF M \\ M', and the")
print("   hypothesis on (m'+1,n)-sets is invoked ONCE PER ELEMENT. That is exactly")
print("   where a deficit d3 gets multiplied and d2 does not.")
print()

print("The algebra, asserted symbolically over a grid")
def lower_bound(mp, m, n, k, d2=0, d3=0):
    """k + [Z(m-m')Z(n) - d2] + (m-m')[Z(m'+1)Z(n) - d3 - k]"""
    return k + (Z(m-mp)*Z(n) - d2) + (m-mp)*(Z(mp+1)*Z(n) - d3 - k)

print("  coefficient of k is 1-(m-m') < 0 whenever m-m' > 1, so the bound is")
print("  minimised at the largest admissible k, namely k = Z(m')Z(n):")
bad=[]
for n in range(3,14,2):
    for m in range(5,20,2):
        for mp in range(2,min(m,n),2):
            if m-mp <= 1: continue
            kmax = Z(mp)*Z(n)
            # minimised at kmax
            vals = [lower_bound(mp,m,n,k) for k in range(0, kmax+1)]
            if min(vals) != lower_bound(mp,m,n,kmax): bad.append(("argmin",mp,m,n))
            if lower_bound(mp,m,n,kmax) != Z(m)*Z(n): bad.append(("collapse",mp,m,n))
ck("minimised at k = Z(m')Z(n), and collapses to Z(m)Z(n), over the whole grid", bad, [])

bad2=[]
for n in range(3,14,2):
    for m in range(5,20,2):
        for mp in range(2,min(m,n),2):
            if m-mp <= 1: continue
            for d2 in range(0,7):
                for d3 in range(0,7):
                    got = lower_bound(mp,m,n,Z(mp)*Z(n),d2,d3)
                    want = Z(m)*Z(n) - d2 - (m-mp)*d3
                    if got != want: bad2.append((mp,m,n,d2,d3))
ck("with deficits, bound = Z(m)Z(n) - d2 - (m-m')*d3, over the same grid", bad2, [])

print()
print("VERDICT: the transfer is exact and the reconstruction was right.")
print("  The (m-m') multiplier survives because term 3 invokes the (m'+1,n)")
print("  hypothesis once per element of M \\ M'. Item (1) is DISCHARGED: the")
print("  weakened Theorem 7 is derived, not conjectured.")
print()
print("  At m=11, n=7, m'=4, with d2 = 2 at (7,7) and d3 = 0 at (5,7):")
ck("weakened conclusion", lower_bound(4,11,7,Z(4)*Z(7),2,0), 223)

print()
print("=" * 70)
print("SEPARATELY: their ablation extrapolation, recomputed")
ON  = [1, 12, 329, 25346, 615817]
OFF = [1, 13, 377, 29099, 801503]
ck("ON total", sum(ON), 641505); ck("OFF total", sum(OFF), 830993)
cum = sum(OFF)/sum(ON)
print(f"  cumulative {cum:.4f}x")
ratios=[o/n for o,n in zip(OFF,ON)]
print("  per-level  " + "  ".join(f"{r:.3f}" for r in ratios))
print(f"  deepest level is {ON[-1]/sum(ON)*100:.1f}% of the ON tree and "
      f"{OFF[-1]/sum(OFF)*100:.1f}% of the OFF tree")
ck("so the cumulative is ~ the deepest LEVEL ratio, not a product of them",
   round(cum,2), round(ratios[-1],2))
print()
print("  THEIR 2-3x LOOKS LIKE COMPOUNDING, WHICH DOUBLE-COUNTS. Because the")
print("  deepest level holds 96% of the nodes, the full-tree ratio is approximately")
print("  the ratio AT the deepest level, not the product of the per-level ratios.")
from math import log, exp
lv=[2,3,4,5]; lr=[log(r) for r in ratios[1:]]
slope=(lr[-1]-lr[0])/(lv[-1]-lv[0]); inter=lr[0]-slope*lv[0]
for L in (6,7):
    print(f"    log-linear fit on the four observed level ratios -> r_{L} ~ {exp(slope*L+inter):.2f}")
print("  So a defensible full-tree figure is ~1.5x, not 2-3x -- still an order of")
print("  magnitude under the 10x threshold, and their own case is stronger than")
print("  they stated it.")

print()
print("=" * 70)
if FAIL: print(f"{len(FAIL)} FAILED: {FAIL}"); raise SystemExit(1)
print("Item (1) discharged. Weakened Theorem 7 at m'=4 gives antisum >= 223, derived.")
