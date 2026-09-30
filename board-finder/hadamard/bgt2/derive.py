#!/usr/bin/env python3
"""What can be DERIVED locally about the b > 2 Hadamard region, before any claim
about it is repeated.

The option-3 queue entry rests on one sentence quoted from a file in ANOTHER
repository (Cooperative-AI-Defense, hadamard/findings/OPEN_ORDERS.md) that the
quoting instance never opened -- it read a plan that read that file. So the
symbol `b` in "126+ admissible (v, b) pairs with b > 2" is undefined here. This
script establishes what does not depend on knowing b, and states one hypothesis
about b with its falsifier.

Run: python3 derive.py
"""
import math

# ---------------------------------------------------------------- 1. the parametrisation
# From board-finder/hadamard/PLAN_2092.md sec 1.1, which states the law but whose
# sweep is reproduced here rather than trusted:
#   H of order 4v from b circulant blocks with row sums a_1..a_b, sum a_k^2 = 4v
#   (b = 4 is the Williamson / Goethals-Seidel array, the case the live work uses)
#   d is an odd divisor of v-1;  r = (v-1)/d + 1;  D = (r-1)/2
#   each row sum has the form a_k = +-1 + d*(2u - (r-1)),  u in {0..r-1}

def odd_divisors(m):
    return sorted((x for x in range(1, m + 1) if m % x == 0 and x % 2 == 1),
                  reverse=True)

def row_sum_values(v, d):
    """The a_k values the law permits at this (v, d), bounded by sum a_k^2 = 4v."""
    r = (v - 1) // d + 1
    lim = int(math.isqrt(4 * v))
    out = set()
    for u in range(r):
        step = d * (2 * u - (r - 1))
        for s in (+1, -1):
            a = s + step
            if abs(a) <= lim:
                out.add(a)
    return sorted(out), r

def admissible(v, d, b=4):
    """Can b row sums from the permitted set square-sum to exactly 4v?"""
    vals, r = row_sum_values(v, d)
    sq = sorted({a * a for a in vals})
    target = 4 * v
    # can we write target as a sum of exactly b squares from sq (with repetition)?
    reach = {0: 0}
    cur = {0}
    for _ in range(b):
        nxt = set()
        for t in cur:
            for s in sq:
                if t + s <= target:
                    nxt.add(t + s)
        cur = nxt
    return target in cur, r

def sweep(v, b=4):
    ok = [d for d in odd_divisors(v - 1) if admissible(v, d, b)[0]]
    if not ok:
        return None
    d = max(ok)
    r = (v - 1) // d + 1
    D = (r - 1) // 2
    return ok, d, r, D

# ---------------------------------------------------------------- 2. reproduce the table
print("=" * 74)
print("1. PLAN_2092.md sec 1's table, reproduced independently (b = 4)")
print("=" * 74)
TABLE = {   # v: (admissible d list, d, r, D, free_bits, log2E, density_exp)
    487: ([9, 3, 1], 9,  55,  27, 216,  83.9, 132),
    523: ([9, 3, 1], 9,  59,  29, 232,  90.9, 141),
    571: ([5, 3, 1], 5, 115,  57, 456, 172.8, 283),
    643: ([3, 1],    3, 215, 107, 856, 308.0, 548),
    659: ([7, 1],    7,  95,  47, 376, 132.7, 243),
    739: ([9, 3, 1], 9,  83,  41, 328, 117.0, 211),
}
print(f"  {'v':>4} {'4v':>6} | {'claimed d':>12} {'mine':>14} | "
      f"{'r':>4} {'D':>4} | free bits")
allok = True
for v in sorted(TABLE):
    claim_ds, cd, cr, cD, cfb, clg, cden = TABLE[v]
    got = sweep(v)
    ds, d, r, D = got
    match = (ds == claim_ds and d == cd and r == cr and D == cD)
    allok &= match
    print(f"  {v:>4} {4*v:>6} | {str(claim_ds):>12} {str(ds):>14} | "
          f"{r:>4} {D:>4} | {cfb:>5}   {'OK' if match else 'MISMATCH'}")
assert allok, "the d-sweep does not reproduce PLAN_2092's table"
print("  ASSERTED: all six rows reproduce, d list included.")

# the two relations the table satisfies but never states
print()
print("  Two relations PLAN_2092 does NOT state, holding on all six rows:")
for v in sorted(TABLE):
    _, _, r, D, fb, lg, den = TABLE[v]
    assert fb == 8 * D == 4 * (r - 1), (v, fb, D, r)
    assert abs((fb - lg) - den) < 0.35, (v, fb - lg, den)
print("    free_bits = 8D = 4(r-1)                     -- exact, all six")
print("    density exponent = free_bits - log2 E[#sol] -- all six to <0.35")
print()
print("  CONSEQUENCE, and it is the useful part: free_bits is a function of d")
print("  alone, via r = (v-1)/d + 1. So the entire difficulty ranking of the")
print("  worklist is decided by ONE arithmetic quantity -- the largest odd")
print("  divisor of v-1 that the row-sum law admits. Nothing about the search.")

# ---------------------------------------------------------------- 3. the classical thirteen
print()
print("=" * 74)
print("2. The classical thirteen smallest open Hadamard orders")
print("=" * 74)
print("  The ORDER LIST is RECALL, not verified here -- flagged, and step 1 of")
print("  the brief is to check it against the other repository:")
CLASSICAL = [668, 716, 892, 1004, 1132, 1244, 1388, 1436, 1676, 1772, 1916, 1948, 1964]
def isprime(m):
    if m < 2: return False
    if m % 2 == 0: return m == 2
    i = 3
    while i * i <= m:
        if m % i == 0: return False
        i += 2
    return True
print(f"  {len(CLASSICAL)} orders, all divisible by 4: "
      f"{all(n % 4 == 0 for n in CLASSICAL)}")
print(f"  v = n/4 all prime: {all(isprime(n // 4) for n in CLASSICAL)}")
print()
print(f"  {'order':>6} {'v':>5} {'d':>4} {'r':>5} {'D':>5} {'free bits':>10}")
for n in CLASSICAL:
    v = n // 4
    got = sweep(v)
    if got is None:
        print(f"  {n:>6} {v:>5}    -- no admissible d at b=4")
        continue
    ds, d, r, D = got
    print(f"  {n:>6} {v:>5} {d:>4} {r:>5} {D:>5} {8*D:>10}")

print()
print("  AND A DISCREPANCY THAT MATTERS: the repo's six targets are")
print("  v = 487, 523, 571, 643, 659, 739 -> orders 1948, 2092, 2284, 2572,")
print("  2636, 2956. Only 1948 is in the classical thirteen. So 'the thirteen")
print("  open orders' in the quoted sentence and 'thirteen' in the repo's own")
print("  target ranking are DIFFERENT LISTS, or one of them is not what I think.")
print("  Two quantities sharing a name -- resolve before using the 126+ figure.")

# ---------------------------------------------------------------- 4. 669 and 721
print()
print("=" * 74)
print("3. Orders 669 and 721, said never to have been screened")
print("=" * 74)
def fac(m):
    out, x, p = [], m, 2
    while p * p <= x:
        while x % p == 0: out.append(p); x //= p
        p += 1
    if x > 1: out.append(x)
    return out
for m in (669, 721):
    print(f"  {m}: mod 4 = {m % 4}, factors {fac(m)}, prime: {isprime(m)}")
print()
print("  A Hadamard matrix of order > 2 requires order = 0 mod 4. Both are 1 mod 4,")
print("  so NEITHER IS A HADAMARD ORDER. They must be v or m values, giving")
print(f"  orders 4*669 = {4*669} and 4*721 = {4*721}.")
print("  And both are COMPOSITE, while every v in the repo's worklist is prime.")
print("  HYPOTHESIS, offered as such: they were never screened because the")
print("  machinery assumes v prime. Falsifier: the other repo screening a")
print("  composite v anywhere. This is a guess about a file I have not read.")
for m in (669, 721):
    got = sweep(m)
    print(f"    v={m}: admissible d at b=4 -> "
          f"{got[0] if got else 'NONE'}"
          + (f", d={got[1]}, r={got[2]}, D={got[3]}, free bits {8*got[3]}" if got else ""))

# ---------------------------------------------------------------- 5. the b hypothesis
print()
print("=" * 74)
print("4. One hypothesis about b, with its falsifier. NOT a finding.")
print("=" * 74)
print("  free_bits = 8D at b = 4. If the b blocks each contribute 2D free bits,")
print("  then free_bits = 2*b*D, which fits 8D at b=4 -- a relation fitted at a")
print("  SINGLE value of b, which is exactly the D53 trap. Stated as a")
print("  hypothesis with the number it predicts, so it can be killed:")
print()
print(f"  {'b':>3} {'2bD at v=523, D=29':>20} {'vs b=4':>10}")
for b in (2, 3, 4, 5, 6, 8):
    print(f"  {b:>3} {2*b*29:>20} {2*b*29 - 232:>+10}")
print()
print("  IF that scaling is right, b > 2 is a region with MORE free bits than")
print("  b = 2, i.e. HARDER, and the 126+ admissible pairs are not a cheaper")
print("  frontier but a more expensive one. FALSIFIER: any statement in the")
print("  other repo giving free bits or density for a b != 4 case. One number")
print("  kills or confirms this, and the brief asks for it first.")
print()
print("  Separately, admissibility counted under the b-blocks reading:")
print(f"  {'b':>3} {'admissible v of the classical 13':>34}")
for b in (2, 3, 4, 5, 6, 8):
    ok = [n // 4 for n in CLASSICAL if sweep(n // 4, b) is not None]
    print(f"  {b:>3} {len(ok):>4}  {ok if len(ok) < 14 else ''}")
print("  This is a DERIVED count under MY reading of b (number of circulant")
print("  blocks, sum of b row-sum squares = 4v). If the other repo's b means")
print("  something else, every number in this block is void. Check first.")
print()
print("=" * 74)
print("ALL ASSERTIONS PASSED.")
print("=" * 74)


# ---------------------------------------------------------------- 6. b mod 8
print()
print("=" * 74)
print("5. MY READING OF b IS REFUTED BY THE SENTENCE IT WAS MEANT TO CHECK")
print("=" * 74)
# a_k = +-1 + d(2u - (r-1)). v odd => v-1 even => (v-1)/d even (d odd) => r odd
# => r-1 even => d(2u-(r-1)) even => a_k odd. Always.
for v in list(TABLE) + [167, 179, 491, 669, 721]:
    for d in odd_divisors(v - 1):
        vals, r = row_sum_values(v, d)
        assert r % 2 == 1, (v, d, r)
        assert all(a % 2 != 0 for a in vals), (v, d)
print("  ASSERTED: every permitted row sum a_k is ODD, at every (v, d) checked.")
print("  Because v is odd, so (v-1)/d is even for odd d, so r is odd, so")
print("  d(2u-(r-1)) is even, so a_k = +-1 + even is odd.")
print()
print("  An odd square is 1 mod 8. So a sum of b odd squares is b mod 8.")
print("  And 4v with v odd is 4 mod 8. Therefore:")
print()
print("      sum_{k=1..b} a_k^2 = 4v  forces  b = 4 (mod 8).")
print()
for b in range(2, 30):
    feas = (b % 8 == 4)
    ok = [n // 4 for n in CLASSICAL if sweep(n // 4, b) is not None]
    assert (len(ok) > 0) == feas or len(ok) == 0, (b, len(ok))
    if feas or len(ok):
        print(f"    b={b:>3}: b mod 8 = {b%8}, admissible v of the 13: {len(ok)}")
print()
print("  So under my reading, b > 2 means b in {12, 20, 28, ...} and NOTHING")
print("  else -- there is no b = 3, 5, 6 or 8 case at all. A source reporting")
print("  '126+ admissible (v, b) pairs with b > 2' therefore CANNOT mean b =")
print("  the number of circulant blocks whose odd row sums square-sum to 4v.")
print()
print("  THIS IS THE MOST USEFUL THING IN THIS SCRIPT. It does not tell us what")
print("  b is; it proves my guess is wrong, so the brief must not ship the guess.")

# ---------------------------------------------------------------- 7. the 721 lead
print()
print("=" * 74)
print("6. One lead worth checking, and one reason to distrust it")
print("=" * 74)
g = sweep(721)
print(f"  v=721 (composite, 7*103) admits d=15, r=49, D=24, free bits {8*g[3]}.")
print(f"  v=487, the order Alpoge SOLVED, has free bits 216.")
print(f"  v=523, the LIVE target, has free bits 232.")
print(f"  So on the free-bit metric 721 is {216 - 8*g[3]} bits cheaper than the")
print("  solved order and", 232 - 8*g[3], "cheaper than the live target.")
print()
print("  WHY TO DISTRUST IT: free bits is only one of the two coordinates.")
print("  density = free_bits - log2 E[#sol], and E[#sol] needs the constraint")
print("  count, which I cannot compute without the repo's estimator. A cheap")
print("  free-bit count with few solutions is not an easier target. Also")
print("  unverified: whether 4*721 = 2884 is an OPEN order at all.")
print()
print("=" * 74)
print("ALL ASSERTIONS PASSED (part 2).")
print("=" * 74)
