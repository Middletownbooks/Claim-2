#!/usr/bin/env python3
"""Controls for brief F's two candidates, built and run before the brief shipped.

Three hand-written control examples earlier in this session were WRONG and were
caught by their own assertions (a non-Costas array claimed as Costas, a dimension-3
"cap" that was not a cap, an eigensolver that returned a positive bound-state
energy). So nothing here is shipped unexecuted.

PART 1  record 239, odd perfect numbers: sigma(N) = 2N, with Euler's form.
PART 2  record 345, Erdos-Szekeres: convex position.
"""
import itertools

# ============================================================ PART 1
def sigma(n):
    """Sum of divisors, by trial division on the factorisation."""
    total, m, p = 1, n, 2
    while p * p <= m:
        if m % p == 0:
            k = 0
            while m % p == 0:
                m //= p; k += 1
            total *= (p**(k + 1) - 1) // (p - 1)
        p += 1
    if m > 1:
        total *= (m + 1)
    return total

def is_perfect(n):
    return n > 1 and sigma(n) == 2 * n

print("PART 1 -- record 239, odd perfect numbers")
print()
# POSITIVE CONTROL: the four even perfect numbers below 10^5 are 6, 28, 496, 8128.
found = [n for n in range(2, 100000) if is_perfect(n)]
print(f"  perfect numbers below 100000: {found}")
assert found == [6, 28, 496, 8128], found
print("  POSITIVE CONTROL passed: sigma() finds exactly the four known ones.")
# NEGATIVE TEST: sigma must NOT report a non-perfect number as perfect.
for n in (12, 24, 100, 496 - 1, 8128 + 1):
    assert not is_perfect(n), n
print("  NEGATIVE TEST passed: 12, 24, 100, 495 and 8129 are all rejected.")
# The actual claim: no ODD perfect number below the search bound.
odd = [n for n in found if n % 2 == 1]
print(f"  odd perfect numbers below 100000: {odd}")
assert odd == []
print("  So the record's DIRECTION is checkable at small scale, and the published")
print("  bound is 10^1500 -- about 1495 orders of magnitude beyond this control.")
print()
# EULER'S FORM, which any candidate must satisfy: N = q^a * m^2, q prime,
# q = a = 1 (mod 4), gcd(q, m) = 1. Checked as a FILTER on the even ones, where
# it must FAIL, since they are not odd -- so this is a negative test of the form.
def euler_form(n):
    """Return (q, a, m) if n = q^a * m^2 with q prime and q = a = 1 mod 4."""
    if n % 2 == 0:
        return None
    m, p, fac = n, 3, {}
    while p * p <= m:
        if m % p == 0:
            k = 0
            while m % p == 0:
                m //= p; k += 1
            fac[p] = k
        p += 2
    if m > 1:
        fac[m] = fac.get(m, 0) + 1
    odd_exp = [(q, k) for q, k in fac.items() if k % 2 == 1]
    if len(odd_exp) != 1:
        return None
    q, a = odd_exp[0]
    if q % 4 != 1 or a % 4 != 1:
        return None
    rest = 1
    for qq, kk in fac.items():
        if qq != q:
            rest *= qq**(kk // 2)
    return (q, a, rest)

# POSITIVE CONTROL for the form itself: 5^1 * 3^2 = 45 has q=5, a=1, m=3.
assert euler_form(45) == (5, 1, 3), euler_form(45)
# NEGATIVE: 9 = 3^2 has no odd exponent, 21 = 3*7 has two, 6 is even.
for n in (9, 21, 6):
    assert euler_form(n) is None, (n, euler_form(n))
print("  Euler's form checker: N = q^a * m^2 with q prime and q = a = 1 (mod 4).")
print("  POSITIVE: 45 = 5^1 * 3^2 gives (q,a,m) = (5,1,3).")
print("  NEGATIVE: 9 (no odd exponent), 21 (two), 6 (even) all rejected.")
print("  Any claimed odd perfect number must satisfy this. It is the cheapest")
print("  sanity check on a relayed record and it costs nothing.")

# ============================================================ PART 2
print()
print("PART 2 -- record 345, Erdos-Szekeres")
print()
def cross(o, a, b):
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

def convex_hull(pts):
    pts = sorted(set(pts))
    if len(pts) <= 2: return pts
    lo = []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    up = []
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]

def in_convex_position(pts):
    """All of pts are vertices of their own convex hull."""
    return len(convex_hull(pts)) == len(set(pts))

def has_k_in_convex_position(pts, k):
    return any(in_convex_position(list(c)) for c in itertools.combinations(pts, k))

# POSITIVE CONTROL: a square's four corners are in convex position.
assert in_convex_position([(0,0), (1,0), (1,1), (0,1)])
# NEGATIVE TEST: a triangle with a point strictly inside has NO 4 in convex
# position -- this is the standard ES(4) > 4 witness, and the check MUST fire.
tri = [(0,0), (4,0), (0,4), (1,1)]
assert not in_convex_position(tri)
assert not has_k_in_convex_position(tri, 4)
print("  POSITIVE CONTROL: the unit square's corners are in convex position.")
print("  NEGATIVE TEST: triangle (0,0),(4,0),(0,4) plus interior point (1,1) has")
print("  NO 4 points in convex position -- the standard ES(4) > 4 witness. Fires.")
print()
# ES(4) = 5: every 5 points in general position contain 4 in convex position.
# Checked exhaustively over a small integer grid, skipping collinear triples.
def general_position(pts):
    return all(cross(a, b, c) != 0 for a, b, c in itertools.combinations(pts, 3))

N = 5
grid = [(x, y) for x in range(N) for y in range(N)]
tested = fails = 0
for c in itertools.combinations(grid, 5):
    if not general_position(c): continue
    tested += 1
    if not has_k_in_convex_position(c, 4):
        fails += 1
        print(f"    COUNTEREXAMPLE to ES(4)=5: {c}")
print(f"  ES(4) = 5 tested on the {N}x{N} grid: {tested} general-position 5-sets,")
print(f"  {fails} without 4 in convex position.")
assert fails == 0
print("  ASSERTED: zero failures, consistent with ES(4) = 5.")
print()
print("  ES(5) = 9 and ES(6) = 17 are beyond a grid check of this kind; ES(6) = 17")
print("  took a computer-assisted proof (Szekeres-Peters 2006). ES(7) is the open")
print("  one, conjectured 33 by the ES(n) = 2^(n-2) + 1 pattern:")
for n in range(3, 8):
    print(f"    ES({n}) conjectured 2^({n}-2)+1 = {2**(n-2)+1}"
          + ("   PROVEN" if n <= 6 else "   OPEN"))
print()
print("ALL CONTROLS PASSED.")
