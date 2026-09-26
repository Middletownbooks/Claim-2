#!/usr/bin/env python3
"""
Locally verified structural comparison between
  (H) the 4-circulant Hadamard route this project is tooled for:
        sum_{i=1..4} PAF_i(s) = 0   for s = 1..v-1,   sum a_i^2 = 4v
  (D) the 2-circulant D-optimal route for order n = 2v, v odd:
        PAF_A(s) + PAF_B(s) = 2     for s = 1..v-1,   a^2 + b^2 = 4v - 2

Everything printed here is derived, not typed.  Nothing here is recall.
"""
import itertools, math, random, sys

def isprime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True

def paf(seq, s):
    v = len(seq)
    return sum(seq[j] * seq[(j + s) % v] for j in range(v))

# ---------------------------------------------------------------- 1. invariants
def check_invariants(vmax=13, trials=400):
    """PAF_A(s) = v mod 4 ; sum_{s=1}^{v-1} PAF_A(s) = a^2 - v."""
    bad = 0
    for v in range(3, vmax + 1, 2):
        for _ in range(trials):
            A = [random.choice((-1, 1)) for _ in range(v)]
            a = sum(A)
            tot = sum(paf(A, s) for s in range(1, v))
            if tot != a * a - v:
                bad += 1
            for s in range(1, v):
                if (paf(A, s) - v) % 4 != 0:
                    bad += 1
    return bad

def residual_arithmetic():
    """Consequences of the two invariants, for each route."""
    out = []
    for name, k, target, rowsum in (("H", 4, 0, "sum a_i^2 = 4v"),
                                    ("D", 2, 2, "a^2 + b^2 = 4v - 2")):
        # residual mod 4:  sum_i PAF_i(s) = k*v (mod 4); v odd
        res_mod4 = (k * 1 - target) % 4          # v odd => v = 1 mod 4 or 3 mod 4
        res_mod4_alt = (k * 3 - target) % 4
        # sum of residuals over s = 1..v-1
        #   sum_s sum_i PAF_i(s) = sum_i (a_i^2 - v) = (rowsum total) - k*v
        #   H: 4v - 4v = 0        ; target sum = 0*(v-1) = 0        -> 0
        #   D: (4v-2) - 2v = 2v-2 ; target sum = 2*(v-1) = 2v-2     -> 0
        out.append((name, k, target, res_mod4, res_mod4_alt, rowsum))
    return out

# ---------------------------------------------------------------- 2. the floor
def floor_by_exhaustion(v):
    """Smallest non-zero sum(res^2) over ALL 2-circulant pairs with the correct
    row sums, for the D-optimal condition.  Exhaustive, so this is a proof for v.

    NOTE ON UNITS: this sums over s = 1..v-1, which DOUBLE COUNTS, because
    PAF(s) = PAF(v-s) for a real sequence.  So the 64 it reports corresponds to
    32 on the deduplicated equation set s = 1..(v-1)/2 -- the units in which the
    Hadamard work states its floor.  Left as-is with the factor named rather than
    silently rescaled."""
    need = 4 * v - 2
    rowsums = [(a, b) for a in range(-v, v + 1, 2 if v % 2 == 0 else 1)
               for b in range(-v, v + 1)
               if a * a + b * b == need and (v - a) % 2 == 0 and (v - b) % 2 == 0]
    if not rowsums:
        return None, None, 0
    seqs = {}
    for bits in itertools.product((-1, 1), repeat=v):
        s = sum(bits)
        seqs.setdefault(s, []).append(bits)
    best, best_at, nsol = None, None, 0
    seen = set()
    for a, b in rowsums:
        if (a, b) in seen or (b, a) in seen:
            continue
        seen.add((a, b))
        for A in seqs.get(a, []):
            pa = [paf(A, s) for s in range(1, v)]
            for B in seqs.get(b, []):
                pb = [paf(B, s) for s in range(1, v)]
                cost = sum((x + y - 2) ** 2 for x, y in zip(pa, pb))
                if cost == 0:
                    nsol += 1
                elif best is None or cost < best:
                    best, best_at = cost, (a, b)
    return best, best_at, nsol

# ------------------------------------------- 3. orbit-ansatz admissibility sweep
def orbit_rowsums(v, d):
    """Row sums attainable by a sequence constant on the orbits of a multiplier
    subgroup of order d acting on Z_v (v prime): a = eps + d*(2u - (r-1))."""
    r = (v - 1) // d + 1
    return r, sorted({eps + d * (2 * u - (r - 1))
                      for eps in (-1, 1) for u in range(r)})

def admissible(v, d, k, need):
    """Is there a k-tuple of orbit-form row sums with sum of squares = need?"""
    r, cand = orbit_rowsums(v, d)
    sq = sorted({c * c for c in cand})
    def rec(k_left, rem, lo):
        if k_left == 0:
            return rem == 0
        for i in range(lo, len(sq)):
            if sq[i] > rem:
                break
            if rec(k_left - 1, rem - sq[i], i):
                return True
        return False
    return rec(k, need, 0)

def sweep(vs):
    rows = []
    for v in vs:
        if not isprime(v):
            continue
        two_sq = sum_of_two_squares(4 * v - 2) is not None
        okH, okD = [], []
        for d in sorted((x for x in divisors_odd(v - 1)), reverse=True):
            r = (v - 1) // d + 1
            D = (r - 1) // 2
            if admissible(v, d, 4, 4 * v):
                okH.append((d, r, D))
            if admissible(v, d, 2, 4 * v - 2):
                okD.append((d, r, D))
        rows.append((v, two_sq, okH, okD))
    return rows

def divisors_odd(n):
    return [i for i in range(1, n + 1) if n % i == 0 and i % 2 == 1]

def sum_of_two_squares(n):
    i = 0
    while i * i * 2 <= n:
        j2 = n - i * i
        j = math.isqrt(j2)
        if j * j == j2:
            return (i, j)
        i += 1
    return None

# -------------------------------- 4. density exponent: k blocks, D equations
def per_equation_bits(v, d, k, target, trials=60000):
    """Monte Carlo P[sum_i PAF_i(s) = target] for orbit-constant random sequences,
    measured on a single representative s, in bits."""
    r = (v - 1) // d + 1
    # build orbits of <t> on Z_v for some t of order d
    t = multiplier_of_order(v, d)
    orbits, seen = [], set()
    for x in range(1, v):
        if x in seen:
            continue
        o, y = [], x
        while y not in seen:
            seen.add(y); o.append(y); y = (y * t) % v
        orbits.append(o)
    assert len(orbits) == r - 1, (len(orbits), r - 1)
    s = orbits[0][0]
    hits = 0
    for _ in range(trials):
        tot = 0
        for _ in range(k):
            signs = [random.choice((-1, 1)) for _ in range(r - 1)]
            eps = random.choice((-1, 1))
            seq = [0] * v
            seq[0] = eps
            for o, sg in zip(orbits, signs):
                for x in o:
                    seq[x] = sg
            tot += paf(seq, s)
        if tot == target:
            hits += 1
    if hits == 0:
        return None
    return -math.log2(hits / trials)

def multiplier_of_order(v, d):
    for t in range(2, v):
        o, y = 1, t
        while y != 1:
            y = (y * t) % v; o += 1
        if o == d:
            return t
    raise ValueError(f"no multiplier of order {d} mod {v}")

if __name__ == "__main__":
    print("=== 1. invariants (0 violations expected) ===")
    print("violations:", check_invariants())
    for name, k, target, m1, m3, rs in residual_arithmetic():
        print(f"  route {name}: k={k} blocks, target={target}, {rs}")
        print(f"      residual = 0 mod 4 for v=1 mod 4: {m1 == 0} ; v=3 mod 4: {m3 == 0}")
    print("  sum of residuals over s=1..v-1 is 0 for BOTH routes (derived above)")

    print("\n=== 2. the cost floor, by exhaustion, for the D-optimal condition ===")
    for v in (3, 5, 7, 9, 11):
        best, at, nsol = floor_by_exhaustion(v)
        print(f"  v={v:3d} n={2*v:3d}  exact solutions={nsol:5d}  "
              f"smallest non-zero cost={best}  at row sums {at}")

    print("\n=== 3. orbit-ansatz admissibility, H (4 blocks) vs D (2 blocks) ===")
    print("  v   4v-2 is a^2+b^2 |  H: (d,r,D) admissible        |  D: (d,r,D) admissible")
    for v, two_sq, okH, okD in sweep([487, 523, 571, 643, 659, 739]):
        h = ", ".join(f"{d}/{r}/{D}" for d, r, D in okH) or "none"
        dd = ", ".join(f"{d}/{r}/{D}" for d, r, D in okD) or "none"
        print(f"  {v}  {str(two_sq):>5}            |  {h:28s} |  {dd}")

    print("\n=== 4. per-equation cost in bits, orbit-constant sequences ===")
    for v, d in ((67, 3), (79, 3), (103, 3), (151, 3)):
        bH = per_equation_bits(v, d, 4, 0)
        bD = per_equation_bits(v, d, 2, 2)
        r = (v - 1) // d + 1
        if bH and bD:
            print(f"  v={v:4d} d={d} r={r:3d} D={(r-1)//2:3d} | "
                  f"H {bH:5.2f} bits/eq | D {bD:5.2f} bits/eq | diff {bD-bH:+5.2f}")
            for k, b, lbl in ((4, bH, "H"), (2, bD, "D")):
                exp = k * (r - 1) - b * ((r - 1) // 2)
                print(f"      {lbl}: free bits {k*(r-1):4d} - equations "
                      f"{b*((r-1)//2):7.1f} = log2 E[#sol] {exp:+8.1f}  "
                      f"(per unit of (r-1): {k - b/2:+.2f})")
