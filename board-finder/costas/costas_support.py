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
print("  *** THE NEXT THREE PARAGRAPHS WERE WRONG. SEE PART 7. ***")
print("  *** Corner DELETION is not the only operator: a dot ADDED at a corner")
print("  *** also preserves the Costas property, and Welch p=31 plus one added")
print("  *** dot gives exactly the 8 known order-31 arrays. They are")
print("  *** CONSTRUCTIBLE, not sporadic. Retained unedited because the")
print("  *** computation was right and the INFERENCE from it was wrong, and")
print("  *** that distinction is the finding. See debt D53.")
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


# ---------------------------------------------------------------- PART 7
# CORRECTION. Brief D (a Sonnet 5.5 chat run, 30 Sep 2026) falsified PART 6's
# closing inference, and it was right.
#
# PART 6 concluded that because no Welch/Golomb array reaches order 31 by corner
# DELETION, the >= 8 known order-31 arrays "are necessarily sporadic -- somebody
# found them by search", and built a 5-bit positive control on that. The brief
# reported instead that they are W0 arrays: a Welch p=31 array with a corner dot
# ADDED. Addition is a second operator that also preserves the Costas property,
# and I never modelled it. The computation was correct; the inference drawn from
# it was not, because it generalised from "unreachable by the operator I
# implemented" to "unreachable by any construction".
#
# PART 7 adds the missing operator and the missing fields, and re-runs the whole
# question. Two results survive and one dies.

def add_corner(perm, c):
    """A dot added at a corner of an enlarged grid. The Costas property is NOT
    automatic here -- unlike deletion -- so every result is tested."""
    n = len(perm)
    if c == 'TL': return [0] + [r + 1 for r in perm]
    if c == 'BL': return [n] + list(perm)
    if c == 'TR': return [r + 1 for r in perm] + [0]
    if c == 'BR': return list(perm) + [n]
    raise ValueError(c)

# --- Golomb over GF(p^k) for non-prime prime powers, which PART 4 omitted.
# Irreducibility is DERIVED, not recalled: F_p[x]/(f) is a field iff it holds an
# element of multiplicative order p^k - 1.
import itertools

def _polymulmod(a, b, f, p):
    k = len(f) - 1
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                r[i + j] = (r[i + j] + x * y) % p
    for i in range(len(r) - 1, k - 1, -1):
        c = r[i]
        if c:
            r[i] = 0
            for j in range(k + 1):
                r[i - k + j] = (r[i - k + j] - c * f[j]) % p
    return tuple(r[:k] + [0] * (k - len(r[:k])))

def golomb_gf(p, k):
    """All Golomb G2 arrays of order p^k - 2 over GF(p^k)."""
    q = p ** k
    one = tuple([1] + [0] * (k - 1))
    field = None
    for tail in itertools.product(range(p), repeat=k):
        f = list(tail) + [1]
        prims = []
        for coeffs in itertools.product(range(p), repeat=k):
            g = tuple(coeffs)
            if all(c == 0 for c in g):
                continue
            x, order = g, 1
            while x != one and order <= q:
                x = _polymulmod(list(x), list(g), f, p); order += 1
            if x == one and order == q - 1:
                prims.append(g)
        if prims:
            field = (f, prims); break
    if field is None:
        return []
    f, prims = field
    out = []
    for a in prims:
        pa, x = {}, a
        for i in range(1, q):
            pa[i] = x; x = _polymulmod(list(x), list(a), f, p)
        for b in prims:
            pb, x = {}, b
            for j in range(1, q):
                pb[j] = x; x = _polymulmod(list(x), list(b), f, p)
            logb = {v: j for j, v in pb.items()}
            perm, ok = [None] * (q - 2), True
            for i in range(1, q - 1):
                t = tuple((one[m] - pa[i][m]) % p for m in range(k))
                if all(c == 0 for c in t):
                    ok = False; break
                j = logb.get(t)
                if j is None or j > q - 2:
                    ok = False; break
                perm[i - 1] = j - 1
            if ok and sorted(perm) == list(range(q - 2)):
                out.append(perm)
    return out

print()
print("PART 7 -- the correction: dot ADDITION, and the prime-power fields")
print()

# (i) The order-31 arrays are W0, not sporadic.
p = 31
w1_31 = [welch_shift(p, g, c) for g in primitive_roots(p) for c in range(1, p)]
add31 = [h for a in w1_31 for c in ('TL', 'BL', 'TR', 'BR')
         if is_costas(h := add_corner(a, c))]
orb31 = set()
for h in add31:
    orb31 |= dihedral(h)
print(f"  Welch p=31: {len(w1_31)} arrays of order 30.")
print(f"  Plus one ADDED corner dot: {len(set(map(tuple, add31)))} distinct Costas "
      f"arrays of order 31, {len(orb31)} under the dihedral group.")
assert len(orb31) == 8, len(orb31)
print("  ASSERTED: exactly 8 -- one equivalence class, matching the relayed")
print("  'C(31) >= 8' exactly. The known order-31 arrays are CONSTRUCTIBLE.")

# The array brief D returned, 1-indexed, must lie in that class.
BRIEF_D_31 = [1,28,20,27,17,18,21,30,26,14,9,25,11,31,29,23,5,13,6,16,15,12,3,
              7,19,24,8,22,2,4,10]
bd = [r - 1 for r in BRIEF_D_31]
assert sorted(bd) == list(range(31)) and is_costas(bd)
assert tuple(bd) in orb31
print("  ASSERTED: the explicit order-31 array brief D returned is Costas and")
print("  lies in that dihedral class, so it is a W0 array.")

# (ii) Full closure under BOTH operators, over every field that matters.
seeds = set()
for q in BASE_PRIMES:
    rs = primitive_roots(q)
    for g in rs:
        for c in range(1, q):
            seeds.add(tuple(welch_shift(q, g, c)))
    for a in rs:
        for b in rs:
            x = golomb(q, a, b)
            if x is not None:
                seeds.add(tuple(x))
for (pp, kk) in [(5, 2), (3, 3), (2, 5)]:
    for a in golomb_gf(pp, kk):
        seeds.add(tuple(a))

seen, frontier, rounds = set(), set(seeds), 0
while frontier and rounds < 80:
    rounds += 1
    nxt = set()
    for s in frontier:
        if s in seen:
            continue
        seen.add(s); L = list(s)
        if len(s) > 3:
            for c in corners(L):
                nxt.add(tuple(delete_corner(L, c)))
        if len(s) < 40:
            for c in ('TL', 'BL', 'TR', 'BR'):
                h = add_corner(L, c)
                if is_costas(h):
                    nxt.add(tuple(h))
    frontier = nxt - seen
closure = {}
for s in seen:
    closure.setdefault(len(s), set()).update(dihedral(list(s)))

print()
print(f"  Closure under BOTH operators, seeded from Welch over primes < "
      f"{max(BASE_PRIMES)+1} and")
print(f"  Golomb over GF(p) plus GF(25), GF(27), GF(32): {len(seen)} arrays, "
      f"{rounds} rounds.")
print()
FULL = {20: 6464, 21: 3536, 22: 2052, 23: 872, 24: 200, 25: 88, 26: 56,
        27: 204, 28: 712, 29: 164}
print(f"  {'n':>3} {'C(n) known':>11} {'constructible':>14} {'unexplained':>12}")
for n in range(24, 34):
    got = len(closure.get(n, ()))
    k = FULL.get(n)
    if k is None:
        print(f"  {n:>3} {'?':>11} {got:>14} {'?':>12}"
              + ("   <-- UNREACHED" if got == 0 else ""))
    else:
        print(f"  {n:>3} {k:>11} {got:>14} {k-got:>12}"
              + ("   <-- ZERO UNEXPLAINED" if k - got <= 0 else ""))

print()
print("  What survives, what dies:")
print()
print("  SURVIVES -- orders 32 and 33 are still unreached, now under a strictly")
print("  LARGER operator set and more fields than PART 6 used. That conclusion")
print("  is stronger than before, not weaker.")
assert not closure.get(32) and not closure.get(33)
print()
print("  SURVIVES -- order 30's constructible count is EXACTLY 664, matching the")
print("  relayed '>= 664 known at order 30' to the digit, and order 31's is")
print("  exactly 8. Two independent corroborations of the relayed figures.")
assert len(closure[30]) == 664, len(closure[30])
assert len(closure[31]) == 8, len(closure[31])
print()
print("  DIES -- the 5-bit positive control. Order 31 is constructible, so no")
print("  search ever reached it and it cannot calibrate a search. The real")
print("  distances to order 32, all of them far larger:")
for n, lab in [(23, "best heuristic from scratch (Adaptive Search, relayed)"),
               (27, "last UNEXPLAINED array (relayed)"),
               (29, "exhaustive enumeration frontier")]:
    b = math.lgamma(n + 1) / math.log(2)
    print(f"    order {n}: log2(n!) = {b:7.2f}  ->  order 32 is "
          f"{117.66 - b:5.2f} bits above   {lab}")
print()
print("  AND THE REAL ARGUMENT AGAINST THE CELL, which is now measured:")
print("  order 28 is fully explained (712 of 712), order 30 fully explained")
print("  (664), order 31 fully explained (8), and order 29's 16-array residual")
print("  is exactly 2 equivalence classes x 8 -- matching the two order-29")
print("  classes brief D attributes to Rickard's periodicity method, a THIRD")
print("  construction not modelled here. So nothing near the frontier is")
print("  unexplained. Arrays above order 27 exist where a construction lands,")
print("  and orders 32 and 33 are precisely where none lands.")
print()
print("PART 7 CHECKS PASSED.")
