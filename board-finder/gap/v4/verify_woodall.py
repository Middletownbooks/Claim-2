#!/usr/bin/env python3
"""Re-derivation of Woodall 1993's Appendix arithmetic, from the page images.

Pages 667-671 read directly (no OCR). The Appendix proves that the antipode is
the unique vertex at maximum distance in CO_n -- d(a,b) < d(a,abar) = Z(n) for
b != abar -- which is the theoretical foundation the whole enumeration rests on.
Everything below is recomputed from the paper's own definitions and checked
against the identities it states, for general n rather than for the cases it ran.
"""
from math import comb

FAIL = []
def ck(label, got, want):
    ok = got == want
    print(f"  [{'ok ' if ok else 'FAIL'}] {label}: {got!r} vs {want!r}")
    if not ok: FAIL.append(label)

# ---------------------------------------------------------- Z(n)
# Inferred from the paper's own numbers: Z(5)Z(5)=16, Z(5)Z(7)=36, Z(7)Z(7)=81,
# Z(2)Z(7)=0, Z(4)Z(7)=18. The Zarankiewicz factor is:
def Z(n): return (n // 2) * ((n - 1) // 2)

print("1. Z(n), inferred from the paper's stated products and checked against all of them")
for (a, b, prod) in [(5,5,16), (5,7,36), (7,7,81), (2,7,0), (4,7,18)]:
    ck(f"Z({a})Z({b})", Z(a)*Z(b), prod)
print(f"      so Z(5)={Z(5)}, Z(7)={Z(7)}, Z(9)={Z(9)}, Z(11)={Z(11)}")
ck("the open cases: Z(7)Z(11)", Z(7)*Z(11), 225)
ck("the open cases: Z(9)Z(9)",  Z(9)*Z(9),  256)
print("      -- matching the brackets the v4 run derived independently.")
print()

# ---------------------------------------------------------- f and g, p.667
def f(r, n):
    if r == 0: return 0
    if 2*r < n: return 2*r - 1
    if 2*r == n: return 2*r - 2
    raise ValueError("f defined for 0 <= r <= n/2")

def g(s, n):
    if 2*s <= n + 1:
        return comb(s, 2)
    if n % 2 == 1:
        h = (n + 1) // 2
        return comb(h, 2) + comb(s - h, 2)
    h = n // 2 + 1
    return comb(h, 2) + comb(s - h, 2) - 1

print("2. Lemma 1(a): g(n) = Z(n), for every n")
bad = [n for n in range(2, 200) if g(n, n) != Z(n)]
ck("g(n) = Z(n) for all 2 <= n < 200", bad, [])
print(f"      e.g. g(7)={g(7,7)}=Z(7), g(9)={g(9,9)}=Z(9), g(11)={g(11,11)}=Z(11)")

print("3. Lemma 1(b): g(r+1) = g(r-1) + f(r) for 1 <= r <= n/2")
bad = [(n, r) for n in range(3, 120) for r in range(1, n//2 + 1)
       if g(r+1, n) != g(r-1, n) + f(r, n)]
ck("Lemma 1(b) over all n < 120", bad, [])

print("4. Lemma 1(c): g(r+1) + g(s-r-1) <= g(s) for s > r+1, with the stated equality case")
viol, eqbad = [], []
for n in range(4, 80):
    for r in range(0, n//2 + 1):
        for s in range(r + 2, n + 1):
            lhs, rhs = g(r+1, n) + g(s-r-1, n), g(s, n)
            if lhs > rhs: viol.append((n, r, s))
            # equality iff r+1 or s-r-1 equals floor(n/2)+1, or r+1 = s-r-1 = n/2
            cond = (r+1 == n//2 + 1) or (s-r-1 == n//2 + 1) or \
                   (n % 2 == 0 and r+1 == s-r-1 == n//2)
            if (lhs == rhs) != cond: eqbad.append((n, r, s, lhs, rhs, cond))
ck("no violation of the inequality, all n < 80", viol, [])
ck("the stated equality condition is exact", eqbad, [])
print()

# ---------------------------------------------------------- Lemma 2's sum, p.668
print("5. Lemma 2's computation: sum over i of gamma(i,j) = Z(n)")
# n odd:  1 + 3 + 5 + ... + (n-2)            = (1/2)(n-1) * (1/2)(n-1)
# n even: 1 + 3 + ... + (n-3) + (1/2)(n-2)   = (1/2)(n-2) * (1/2)n
bad = []
for n in range(3, 200):
    if n % 2 == 1:
        tot = sum(range(1, n - 1, 2))
        want = ((n-1)//2) * ((n-1)//2)
    else:
        tot = sum(range(1, n - 2, 2)) + (n - 2)//2
        want = ((n-2)//2) * (n//2)
    if not (tot == want == Z(n)): bad.append((n, tot, want, Z(n)))
ck("the odd and even sums both equal Z(n), all n < 200", bad, [])
print("      => the Appendix's key identity holds for EVERY n, not only the")
print("         cases the paper ran. The framework is general in n.")
print()

# ---------------------------------------------------------- the cost ladder
print("6. The reported cost ladder, from sections 5 and its continuation")
ladder = [("K5,5 / K5,7 / K7,5", "programs 1-3", "'ran quite quickly'"),
          ("K7,7", "program 4", "about 4 hours on a Sun 4/110"),
          ("K7,9", "program 5", "about 6 hours, after Theorem 8 was incorporated")]
for case, prog, cost in ladder:
    print(f"      {case:<20} {prog:<12} {cost}")
print("      The paper then goes straight to the Appendix. There is NO concluding")
print("      section, NO statement of an obstruction, and NO reason given for")
print("      stopping at K7,9.")
print()

print("=" * 70)
if FAIL:
    print(f"{len(FAIL)} FAILED: {FAIL}"); raise SystemExit(1)
print("Every identity the Appendix states re-derives, and holds for general n.")

# ============================================================ 7. HEADROOM (H)
# Added after pages 657-660 and 666 arrived. Everything below is derived from
# the paper's own structural facts, all now PRIMARY:
#   p.658  Z(n) := C(floor(n/2),2) + C(ceil(n/2),2) = floor(n/2)*floor((n-1)/2)
#   p.659  CO_n has (n-1)! vertices
#   p.662  a drawing of K_{m,n} corresponds to an (m,n)-set: m elements of V(CO_n)
#   p.666  "It was clearly not going to be practicable to generate all (9,7)-sets
#           with antisum less than 144 = Z(9)Z(7)"
print()
print("7. HEADROOM -- the scaling from the cases Woodall ran to the two he left")

ck("p.658's Z(n) definition matches the inferred one",
   [comb(n//2, 2) + comb((n+1)//2, 2) for n in range(2, 14)],
   [Z(n) for n in range(2, 14)])
for n in (5, 7, 9, 11):
    print(f"      |V(CO_{n})| = {n-1}! = {__import__('math').factorial(n-1):,}")

def space(m, n):
    """Raw count of (m,n)-sets: multisets of size m from V(CO_n)."""
    from math import factorial
    N = factorial(n - 1)
    return comb(N + m - 1, m)

cases = [("K7,7  <- (7,7)-set",  7, 7, "4 hours, program 4"),
         ("K7,9  <- (9,7)-set",  9, 7, "6 hours, program 5, and NOT by full generation"),
         ("K7,9  <- (7,9)-set",  7, 9, "the representation he did NOT use"),
         ("K7,11 <- (11,7)-set", 11, 7, "OPEN"),
         ("K7,11 <- (7,11)-set", 7, 11, "OPEN, other representation"),
         ("K9,9  <- (9,9)-set",  9, 9, "OPEN")]
print()
print(f"      {'case':<22} {'raw (m,n)-sets':>14}   note")
for label, m, n, note in cases:
    print(f"      {label:<22} {space(m,n):>14.3g}   {note}")

base = space(9, 7)                      # the last case he completed
print()
print("      Woodall chose the representation with MORE elements from the SMALLER")
ck("...and (9,7) is indeed cheaper than (7,9)", space(9,7) < space(7,9), True)
print(f"         (9,7) = {space(9,7):.3g}  vs  (7,9) = {space(7,9):.3g}")
print("      CO -- so for K7,11 the analogous choice is (11,7), not (7,11):")
ck("(11,7) is cheaper than (7,11)", space(11,7) < space(7,11), True)
print(f"         (11,7) = {space(11,7):.3g}  vs  (7,11) = {space(7,11):.3g}")

print()
print("      Scaling against the last completed case, (9,7):")
r_711 = space(11, 7) / base
r_99  = space(9, 9)  / base
print(f"        K7,11 via (11,7):  x {r_711:,.0f}          (= 720^2 * 9!/11! to first order)")
print(f"        K9,9  via (9,9):   x {r_99:.3g}")
ck("the (11,7) ratio is ~720^2/(10*11)", round(r_711 / (720**2 / (10*11)), 1), 1.0)
ck("the (9,9) ratio is ~(40320/720)^9 = 56^9", round(r_99 / 56**9, 1), 1.0)

print()
print("      Against the 6 hours program 5 took on a Sun 4/110 (~10 MIPS):")
SUN_HOURS = 6.0
for label, r in (("K7,11 via (11,7)", r_711), ("K9,9 via (9,9)", r_99)):
    sun_h = SUN_HOURS * r
    for name, speedup in (("1e3 (one modern core, pessimistic)", 1e3),
                          ("1e4 (one modern core, optimistic)", 1e4)):
        h = sun_h / speedup
        unit = f"{h:,.1f} h" if h < 8760 else f"{h/8766:,.3g} yr"
        print(f"        {label:<18} at {name:<36} -> {unit}")
print()
print("      => K7,11 IS REACHABLE and K9,9 IS NOT. The run merged them as one")
print("         candidate; they differ by eleven orders of magnitude and must be")
print("         scored separately. H PASSES for K7,11, FAILS hard for K9,9.")
print()
print("      CAVEAT, stated because the number is load-bearing: these are RAW")
print("      multiset counts. Woodall enumerated neither -- p.664's canonical form")
print("      quotients by isomorphism and p.664's bound sequence (2) prunes by")
print("      partial antisum, and at (9,7) he could not generate the sub-threshold")
print("      sets at all and used Theorem 6(c)'s augmented antisum instead. The")
print("      ratio is a first-order SCALING proxy, valid because the same two")
print("      reductions apply at every case. It is not an absolute cost.")
