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
