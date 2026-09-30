#!/usr/bin/env python3
"""
Costas arrays: which orders have algebraic (generator) support, and what the
search space costs at the open orders.

Everything here is computed, not recalled. The three parts are:

  PART 1  is_costas(), with a positive control and a negative test.
  PART 2  the Welch and Golomb generators, BUILT and then checked by PART 1 --
          so the claim "order n has family support" is verified by exhibiting
          an array, not by citing a condition.
  PART 3  the orders 24..48 with zero family support, and log2(n!) at those
          orders, which is the search-space size the bits_search coordinate
          needs.

Run:  python3 costas_support.py
"""
import math

# ---------------------------------------------------------------- PART 1
def is_costas(perm):
    """perm[i] = row of the dot in column i, 0-indexed, a permutation.
    Costas iff all vectors (j-i, perm[j]-perm[i]) for i<j are distinct."""
    seen = set()
    n = len(perm)
    for i in range(n):
        for j in range(i + 1, n):
            v = (j - i, perm[j] - perm[i])
            if v in seen:
                return False
            seen.add(v)
    return True

def violations(perm):
    """Count repeated difference vectors -- for reporting, not for the test."""
    from collections import Counter
    c = Counter((j - i, perm[j] - perm[i])
                for i in range(len(perm)) for j in range(i + 1, len(perm)))
    return sum(k - 1 for k in c.values() if k > 1)

# POSITIVE CONTROL: the order-4 array (0,2,3,1). Differences by hand:
#   gap1: 2,1,-2   gap2: 3,-1   gap3: 1   -- all 6 pairs distinct.
assert is_costas([0, 2, 3, 1]), "positive control failed"
# NEGATIVE TEST: the identity permutation repeats (1,1) at every adjacent pair,
# so the check MUST fire for every n >= 3.
assert not is_costas([0, 1, 2, 3]), "negative test did not fire"
assert violations([0, 1, 2, 3]) == 3, violations([0, 1, 2, 3])
# SECOND NEGATIVE TEST: [0,2,1,3] repeats the vector (1,2) at gaps (0,1) and
# (2,3), so the check MUST fire. (My first attempt at this line used [0,1,3,2],
# which is in fact a genuine Costas array -- all six vectors distinct -- and the
# assertion caught it. The example is kept in the comment because the near-miss
# is the reason the negative test is here at all.)
assert not is_costas([0, 2, 1, 3]), "second negative test did not fire"
assert is_costas([0, 1, 3, 2]), "[0,1,3,2] is Costas; this control must pass"

# ---------------------------------------------------------------- PART 2
def isprime(m):
    if m < 2: return False
    if m % 2 == 0: return m == 2
    i = 3
    while i * i <= m:
        if m % i == 0: return False
        i += 2
    return True

def prime_power(m):
    """Return (p,k) if m = p^k with k>=1, else None."""
    if m < 2: return None
    p = 2
    while p * p <= m:
        if m % p == 0: break
        p += 1
    else:
        p = m
    x, k = m, 0
    while x % p == 0:
        x //= p; k += 1
    return (p, k) if x == 1 else None

def primitive_roots(p):
    """All primitive roots mod p, p prime."""
    out = []
    for g in range(2, p):
        seen, x = set(), 1
        for _ in range(p - 1):
            x = x * g % p
            seen.add(x)
        if len(seen) == p - 1:
            out.append(g)
    return out

def welch(p, g):
    """W1: order p-1. Column i (i=0..p-2) has its dot at row g^(i+1) mod p,
    mapped into 0..p-2."""
    return [(pow(g, i + 1, p) - 1) for i in range(p - 1)]

def welch_shift(p, g, c):
    """W1 with the exponent shifted; still Costas for any c."""
    return [(pow(g, i + c, p) - 1) for i in range(p - 1)]

def golomb(p, a, b):
    """G2 over GF(p): order p-2. Dot at (i,j) iff a^i + b^j = 1, i,j in 1..p-2.
    Returns the permutation as a list indexed by i-1, or None if not a bijection."""
    logb = {pow(b, j, p): j for j in range(1, p)}
    perm = [None] * (p - 2)
    for i in range(1, p - 1):
        t = (1 - pow(a, i, p)) % p
        if t == 0:
            return None
        j = logb[t]
        if j > p - 2:
            return None
        perm[i - 1] = j - 1
    return perm if sorted(x for x in perm if x is not None) == list(range(p - 2)) else None

# Verify the generators actually produce Costas arrays.
print("PART 2 -- generators built and checked by is_costas()")
print()
print("  Welch W1, order p-1:")
wk = []
for p in [5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
    gs = primitive_roots(p)
    ok = all(is_costas(welch(p, g)) for g in gs)
    ok2 = all(is_costas(welch_shift(p, g, c)) for g in gs for c in range(1, p - 1))
    wk.append(ok and ok2)
    print(f"    p={p:>3}  order {p-1:>3}  {len(gs):>2} primitive roots  "
          f"all Costas: {ok}   all shifts Costas: {ok2}")
assert all(wk), "a Welch array failed the Costas test"

print()
print("  Golomb G2 over GF(p), order p-2:")
gk = []
for p in [5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
    gs = primitive_roots(p)
    built = [golomb(p, a, b) for a in gs for b in gs]
    good = [x for x in built if x is not None]
    ok = len(good) > 0 and all(is_costas(x) for x in good)
    gk.append(ok)
    print(f"    p={p:>3}  order {p-2:>3}  {len(good):>3} of {len(built):>3} pairs give a "
          f"permutation   all Costas: {ok}")
assert all(gk), "a Golomb array failed the Costas test"

# ---------------------------------------------------------------- PART 3
# CONSERVATIVE support list. Welch supplies orders p-1, p-2, p-3 for p prime
# (W1 and its two corner deletions); Golomb supplies q-2 and q-3 for q a prime
# power (G2 and its one corner deletion). The further deletions q-4, q-5 are
# NOT counted: they need extra conditions on the primitive elements, and
# counting q-4 unconditionally predicts support at order 33, which is one of the
# two smallest orders with NO known Costas array. That contradiction is the
# reason the list stops where it does.
WELCH_OFFSETS  = (1, 2, 3)
GOLOMB_OFFSETS = (2, 3)

def support(n):
    hits = []
    for j in WELCH_OFFSETS:
        if isprime(n + j):
            hits.append(f"W:p={n+j}")
    for j in GOLOMB_OFFSETS:
        r = prime_power(n + j)
        if r:
            hits.append(f"G:q={n+j}={r[0]}^{r[1]}" if r[1] > 1 else f"G:q={n+j}")
    return hits

print()
print("PART 3 -- algebraic support, orders 24..48")
print()
print(f"  {'n':>3} {'#fam':>5}  {'log2(n!)':>9}  families")
zero = []
for n in range(24, 49):
    h = support(n)
    if not h:
        zero.append(n)
    lg = math.lgamma(n + 1) / math.log(2)
    print(f"  {n:>3} {len(h):>5}  {lg:>9.1f}  {', '.join(h) if h else 'NONE'}")

print()
print(f"  orders with ZERO algebraic support in 24..48: {zero}")
print(f"  log2(32!) = {math.lgamma(33)/math.log(2):.2f}")
print(f"  log2(33!) = {math.lgamma(34)/math.log(2):.2f}")
print()
print("  bits_search = log2(n!) - log2(#solutions), for assumed solution counts:")
for n in (32, 33):
    lg = math.lgamma(n + 1) / math.log(2)
    for s in (1, 8, 16, 64):
        print(f"    n={n}, {s:>3} solutions assumed: {lg - math.log2(s):>7.1f} bits")


# ---------------------------------------------------------------- PART 4
# How many arrays at each order do the algebraic families actually explain?
#
# The variant families (Welch W2/W3, Golomb G3/G4/G5) are usually stated as
# conditions on p or q that I would have to recall. Instead they are DERIVED
# here: a Costas array with a dot in a corner stays Costas when that corner's
# row and column are deleted, because every sub-multiset of the dots keeps its
# difference vectors distinct, and the result is a permutation array exactly
# when the deleted dot was at a corner. So corner-deletion, applied repeatedly
# to W1 and G2 and checked by is_costas() every time, generates the variants
# without any recalled condition.
#
# LIMITATION, stated because it bounds the conclusion: the generators are built
# over prime fields GF(p) only. Golomb over GF(2^5) = GF(32) and GF(7^2) is NOT
# included, and those supply arrays at orders 27..30. So the counts below are
# LOWER bounds on what the families explain, and the sporadic residual is an
# UPPER bound.

def corners(perm):
    """Which corners hold a dot: (col,row) in {0,n-1} x {0,n-1}."""
    n = len(perm)
    out = []
    if perm[0] == 0:      out.append('TL')
    if perm[0] == n - 1:  out.append('BL')
    if perm[-1] == 0:     out.append('TR')
    if perm[-1] == n - 1: out.append('BR')
    return out

def delete_corner(perm, c):
    n = len(perm)
    if c == 'TL': sub = [r - 1 for r in perm[1:]]
    elif c == 'BL': sub = list(perm[1:])
    elif c == 'TR': sub = [r - 1 for r in perm[:-1]]
    elif c == 'BR': sub = list(perm[:-1])
    assert sorted(sub) == list(range(n - 1)), (perm, c, sub)
    return sub

def dihedral(perm):
    """The <=8 images of an array under the symmetries of the square."""
    n = len(perm)
    out = set()
    cur = tuple(perm)
    for _ in range(4):
        out.add(cur)
        out.add(tuple(reversed(cur)))                 # reflect left-right
        # rotate 90 degrees: new[row] = col such that perm[col]=row, inverted
        inv = [0] * n
        for i, r in enumerate(cur): inv[r] = i
        cur = tuple(n - 1 - x for x in inv)
    return out

# Collect, per order, every array reachable from W1 or G2 over a prime field
# by corner deletion, closed under the dihedral group.
by_order = {}
BASE_PRIMES = [p for p in range(5, 60) if isprime(p)]
for p in BASE_PRIMES:
    roots = primitive_roots(p)
    seeds = []
    for g in roots:
        for c in range(1, p):
            seeds.append(welch_shift(p, g, c))
    for a in roots:
        for b in roots:
            x = golomb(p, a, b)
            if x is not None:
                seeds.append(x)
    frontier = [tuple(s) for s in seeds]
    seen_seed = set()
    while frontier:
        nxt = []
        for s in frontier:
            if s in seen_seed: continue
            seen_seed.add(s)
            if not is_costas(list(s)):
                raise SystemExit(f"generated non-Costas array: {s}")
            by_order.setdefault(len(s), set()).update(dihedral(list(s)))
            if len(s) > 3:                       # stop before the array vanishes
                for c in corners(list(s)):
                    nxt.append(tuple(delete_corner(list(s), c)))
        frontier = nxt

KNOWN = {24: 200, 25: 88, 26: 56, 27: 204, 28: 712, 29: 164}   # OEIS A008404, RECALL tier
print()
print("PART 4 -- arrays explained by Welch/Golomb over PRIME fields only")
print("         (a lower bound; GF(2^5) and GF(7^2) Golomb are not built here)")
print()
print(f"  {'n':>3} {'C(n) known':>11} {'from families':>14} {'residual':>9}  note")
for n in range(20, 34):
    fam = len(by_order.get(n, ()))
    k = KNOWN.get(n)
    if k is None:
        print(f"  {n:>3} {'?':>11} {fam:>14} {'?':>9}  "
              f"{'ZERO family support' if fam == 0 else ''}")
    else:
        print(f"  {n:>3} {k:>11} {fam:>14} {k - fam:>9}  "
              f"{'residual <= sporadic + missing GF(q)' if k - fam > 0 else ''}")
print()
print("  Extended support check -- Welch offsets 1..5 AND Golomb offsets 2..5,")
print("  i.e. every corner-deletion depth any variant could use:")
wide = []
for n in range(28, 40):
    h = [f"W:{n+j}" for j in (1,2,3,4,5) if isprime(n + j)] + \
        [f"G:{n+j}" for j in (2,3,4,5) if prime_power(n + j)]
    if not h: wide.append(n)
    print(f"    n={n:>3}: {', '.join(h) if h else 'NONE'}")
print(f"  zero support even at maximum deletion depth: {wide}")
print()
print("  Why the block exists:")
print("    primes in [32,36]:", [m for m in range(32, 37) if isprime(m)])
print("    prime powers in [33,36]:", [m for m in range(33, 37) if prime_power(m)])
print("    next prime power above 32:", next(m for m in range(33, 60) if prime_power(m)))


# ---------------------------------------------------------------- PART 5
# PART 3's offset table is a NECESSARY condition only, and PART 4 shows it is
# far from sufficient: corner deletions are rare, so the chains are short. The
# question order 32 actually turns on is how far the chain from p = 37 descends,
# because 37 is the next prime above the 31..36 gap and W1(37) has order 36.

print()
print("PART 5 -- how far does the deletion chain descend from each base?")
print()
for p in (29, 31, 37, 41, 43):
    roots = primitive_roots(p)
    seeds = {tuple(welch_shift(p, g, c)) for g in roots for c in range(1, p)}
    gol = {tuple(x) for a in roots for b in roots
           if (x := golomb(p, a, b)) is not None}
    for label, seedset, base in (("W1", seeds, p - 1), ("G2", gol, p - 2)):
        reach, frontier = {}, set(seedset)
        while frontier:
            nxt = set()
            for s in frontier:
                reach.setdefault(len(s), set()).add(s)
                if len(s) > 3:
                    for c in corners(list(s)):
                        nxt.add(tuple(delete_corner(list(s), c)))
            frontier = nxt - {x for v in reach.values() for x in v}
        orders = sorted(reach, reverse=True)
        chain = ", ".join(f"{o}({len(reach[o])})" for o in orders[:8])
        print(f"  p={p:>3} {label}: base order {base:>2}, chain reaches orders "
              f"{chain}{' ...' if len(orders) > 8 else ''}")
        print(f"          lowest order reached: {min(orders)}")


# ---------------------------------------------------------------- PART 6
# The gap argument. Stated so that it does NOT depend on the fields PART 4
# omitted, and so that the one place it could have been fudged is asserted.
#
# PART 5 measures chain depth: the deepest descent observed is p=41 G2, from
# base order 39 down to 36, i.e. 3 steps. Take 3 as the depth bound (it is a
# measurement, so PART 6 re-derives it rather than hard-coding my reading).
# A base array of order B then covers at most orders B, B-1, B-2, B-3. Welch
# needs a prime p and gives B = p-1; Golomb needs a prime power q, B = q-2.
# So order n can only be reached from
#     a prime p       with p-1 in {n, ..., n+depth}, or
#     a prime power q with q-2 in {n, ..., n+depth}.
# That is a NECESSARY condition and at depth 3 it does not by itself exclude
# order 32 -- q = 37 nominally covers it. What excludes it is the measured
# chain, which is why PART 6 checks the two together.

# Re-derive the depth bound from PART 5's own chains rather than asserting it.
def chain_orders(p):
    roots = primitive_roots(p)
    seeds = {tuple(welch_shift(p, g, c)) for g in roots for c in range(1, p)}
    seeds |= {tuple(x) for a in roots for b in roots
              if (x := golomb(p, a, b)) is not None}
    reach, frontier = set(), set(seeds)
    while frontier:
        nxt = set()
        for s in frontier:
            reach.add(s)
            if len(s) > 3:
                for c in corners(list(s)):
                    nxt.add(tuple(delete_corner(list(s), c)))
        frontier = nxt - reach
    return reach

depths = []
for p in BASE_PRIMES:
    r = chain_orders(p)
    for base in (p - 1, p - 2):
        got = {len(s) for s in r if len(s) <= base}
        if got:
            depths.append(base - min(got))
MAX_CHAIN_DEPTH = max(depths)
print()
print("PART 6 -- coverage, independent of which fields PART 4 built")
print()
print(f"  deepest corner-deletion chain measured over primes < {max(BASE_PRIMES)+1}: "
      f"{MAX_CHAIN_DEPTH} steps")
print()
print(f"  {'n':>3}  nominal covers at depth <= {MAX_CHAIN_DEPTH}"
      f"                    built in PART 4?   arrays found")
nominal_all_prime = {}
for n in range(26, 40):
    bases = range(n, n + MAX_CHAIN_DEPTH + 1)
    w = [b + 1 for b in bases if isprime(b + 1)]
    g = [b + 2 for b in bases if prime_power(b + 2)]
    covers = [f"W:p={x}" for x in w] + [f"G:q={x}" for x in g]
    fields = set(w) | set(g)
    allprime = all(isprime(f) for f in fields)
    nominal_all_prime[n] = (fields, allprime)
    found = len(by_order.get(n, ()))
    print(f"  {n:>3}  {', '.join(covers) if covers else 'NONE':<44} "
          f"{'yes' if allprime else 'NO -- prime power':<18} {found}")

# The load-bearing assertion: for orders 31, 32, 33 every field that could
# nominally reach them is a PRIME, hence was actually built in PART 4, and
# PART 4 found nothing there. So the omission of GF(2^5)/GF(7^2) cannot rescue
# these three orders.
for n in (31, 32, 33):
    fields, allprime = nominal_all_prime[n]
    assert allprime, (n, fields)
    assert all(f in BASE_PRIMES for f in fields), (n, fields)
    assert len(by_order.get(n, ())) == 0, (n, len(by_order[n]))
print()
print("  ASSERTED, and this is the result:")
print("    for n = 31, 32, 33 every field that could nominally reach order n is")
print("    a PRIME, every such prime was built in PART 4, and PART 4 produced")
print("    ZERO arrays at all three orders. The unbuilt prime-power fields")
print("    cannot supply them, so the three orders have no Welch/Golomb array")
print("    at any corner-deletion depth.")
print()
print("  Orders 32 and 33 are also the two smallest with no KNOWN Costas array")
print("  (Drakakis 2011 -- SECONDARY-RELAYED via this project's B2 run, NOT")
print("  verified here), while order 31 has >= 8 known arrays. Order 31 is in")
print("  the same uncovered block, so those arrays are necessarily SPORADIC.")
print("  Order 31 is therefore a positive control for any search aimed at 32:")
l31 = math.lgamma(32) / math.log(2)
l32 = math.lgamma(33) / math.log(2)
print(f"    log2(31!) = {l31:.2f} bits    log2(32!) = {l32:.2f} bits"
      f"    gap = {l32-l31:.2f} bits")
print()
print("ALL CHECKS PASSED.")
