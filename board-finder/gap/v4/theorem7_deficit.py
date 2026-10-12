#!/usr/bin/env python3
"""Can Theorem 7 be RESCUED at m = 11 by tracking the deficit?

Theorem 7 fails at m = 11 because its hypotheses demand exact antisum bounds
Z(k)Z(n) at k = 7 and k = 9, and the measured bounds are 79 (vs 81) and 140
(vs 144). But those deficits are SMALL. Theorem 7 is "the argument of Theorem 2
with 'number of crossings' replaced by 'sum of antidistances'", and Theorem 2's
proof (p.658-659) is an explicit three-term sum -- so the deficits should
propagate ADDITIVELY and yield a weakened but nonvacuous conclusion.
"""
FAIL=[]
def ck(l,g,w):
    ok=g==w; print(f"  [{'ok ' if ok else 'FAIL'}] {l}: {g!r} vs {w!r}")
    if not ok: FAIL.append(l)

def Z(n): return (n//2)*((n-1)//2)

print("1. The identity Theorem 2's proof rests on (p.659), checked")
def ident(mp, m): return Z(mp) + Z(m-mp) + (m-mp)*(Z(mp+1)-Z(mp))
bad=[(mp,m) for m in range(3,40,2) for mp in range(2,m,2) if ident(mp,m)!=Z(m)]
ck("Z(m') + Z(m-m') + (m-m')[Z(m'+1) - Z(m')] = Z(m), all odd m < 40", bad, [])

print()
print("2. Theorem 2's three terms, and where a deficit enters")
print("     term 1: k, the crossings inside M'                 -- bounded by hypothesis k <= Z(m')Z(n)")
print("     term 2: >= cr(K_{m-m',n})                          -- HYPOTHESIS, = Z(m-m')Z(n) if Zarankiewicz holds there")
print("     term 3: >= (m-m')[cr(K_{m'+1,n}) - k]              -- HYPOTHESIS on K_{m'+1,n}")
print("   Coefficient of k is 1 - (m-m') < 0, so the bound is minimised at k = Z(m')Z(n),")
print("   and the three terms then collapse to Z(m)Z(n) by the identity above.")
print()
print("   WITH DEFICITS d2 at (m-m',n) and d3 at (m'+1,n), the same arithmetic gives")
print("        total >= Z(m)Z(n) - d2 - (m-m')*d3")

# established antisum lower bounds at n = 7
BOUND = {3: (Z(3)*Z(7), 0,  "Theorem 4(a), exact"),
         5: (Z(5)*Z(7), 0,  "program 2, exact"),
         7: (Z(7)*Z(7), 2,  "program 4: sets sit at 79 vs 81"),
         9: (Z(9)*Z(7), 4,  "their session 1: 140 vs 144")}

print()
print("3. The weakened Theorem 7 at m = 11, n = 7, for each admissible m'")
n, m = 7, 11
target = Z(m)*Z(n)
ck("Z(11)Z(7)", target, 225)
best=None
for mp in (2,4,6):
    k2, k3 = m-mp, mp+1
    if k2 not in BOUND or k3 not in BOUND: continue
    d2, d3 = BOUND[k2][1], BOUND[k3][1]
    concl = target - d2 - (m-mp)*d3
    print(f"   m'={mp}: deficit at ({k2},7) = {d2} [{BOUND[k2][2]}]")
    print(f"           deficit at ({k3},7) = {d3} [{BOUND[k3][2]}], multiplied by (m-m') = {m-mp}")
    print(f"           => antisum >= {target} - {d2} - {m-mp}*{d3} = {concl}")
    if best is None or concl > best[1]: best=(mp,concl)
print()
ck("the best weakening is m'=4 giving >= 223", best, (4,223))

print()
print("4. Does a bound of 223 prune anything? Parity decides it.")
print("   Theorem 4(b): m, n both odd and both = 3 (mod 4) => antisum is ODD")
ck("11 mod 4", 11%4, 3); ck("7 mod 4", 7%4, 3)
cands = [a for a in range(0, target) if a%2==1]
print(f"   so a counterexample's antisum is odd and < 225: top candidate is {max(cands)}")
ck("top candidate antisum", max(cands), 223)
print()
print("   WEAKENED THEOREM 7 (m'=4): any (11,7)-set containing a (4,7)-subset with")
print(f"   antisum <= Z(4)Z(7) = {Z(4)*Z(7)} has antisum >= 223.")
print("   => it excludes such sets at antisum <= 221, and does NOT exclude 223.")
print()
print("   The other instance sampled 404 sets ALL AT EXACTLY 223, so this prune")
print("   would have removed none of them -- but 223 is a single rung and the")
print("   search has to descend. The prune is live everywhere below the top.")
print()
print("5. And note what IS available at m = 11 but cannot be used")
print("   THEOREM 2's hypotheses are CONJECTURE-VERIFICATION, not antisum bounds:")
for mp in (2,4,6):
    print(f"     m'={mp}: needs Zarankiewicz at K_{{{mp+1},7}} and K_{{{m-mp},7}} -- "
          f"both hold (Kleitman min<=6; Woodall K77, K79)")
print("   So Theorem 2 IS available at m = 11, for all three m'. It is useless to")
print("   the search anyway, because it conditions on the SUB-DRAWING's crossing")
print("   count and the search only knows the subset's ANTISUM, which lower-bounds")
print("   crossings rather than bounding them above. THAT ASYMMETRY IS EXACTLY WHY")
print("   WOODALL NEEDED THE ANTISUM ANALOGUE, and it is why the rescue has to go")
print("   through the deficit rather than through Theorem 2 directly.")

print()
print("="*70)
if FAIL: print(f"{len(FAIL)} FAILED: {FAIL}"); raise SystemExit(1)
print("A weakened Theorem 7 survives at m = 11 with conclusion >= 223, not 225.")
