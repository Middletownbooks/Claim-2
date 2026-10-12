"""Verify arm V1's own propositions exactly, then grade its stated gap."""
from fractions import Fraction as F
from verify import check_family, coverage, isprime

def propA(p):                       # p = 4k+3
    k = (p - 3) // 4
    m = p * (k + 1)
    return (k + 1, m + 1, m * (m + 1))

def _M(p):
    k = (p - 1) // 4
    return k + 1, p * (k + 1)

def propB_even(p):                  # M even
    x, M = _M(p)
    return (x, M // 2, M)

def propB_div3(p):                  # M = 0 mod 3 -> 3/M = 1/(M/3), then split
    x, M = _M(p)
    A = M // 3
    return (x, A + 1, A * (A + 1))

def propB_2mod3(p):                 # M = 2 mod 3
    x, M = _M(p)
    return (x, (M + 1) // 3, M * (M + 1) // 3)

fams = [
    ("A: p = 3 mod 4",          lambda p: isprime(p) and p % 4 == 3,                          propA),
    ("B1: p=1 mod 4, M even",   lambda p: isprime(p) and p % 4 == 1 and _M(p)[1] % 2 == 0,    propB_even),
    ("B2: p=1 mod 4, 3|M",      lambda p: isprime(p) and p % 4 == 1 and _M(p)[1] % 3 == 0,    propB_div3),
    ("B3: p=1 mod 4, M=2 mod3", lambda p: isprime(p) and p % 4 == 1 and _M(p)[1] % 3 == 2,    propB_2mod3),
]

LO, HI = 5, 20000
conds = []
for name, cond, xyz in fams:
    ok, seen, solved, fail = check_family(name, cond, xyz, LO, HI)
    if ok:
        conds.append(cond)

missed = coverage(conds, LO, HI, restrict=isprime)
print("\nprimes in [%d,%d] uncovered by V1's own families: %d" % (LO, HI, len(missed)))
print("their residues mod 24:", sorted({p % 24 for p in missed}))
print("their residues mod  8:", sorted({p % 8 for p in missed}))
print("V1's gap claim was: p = 1 or 17 (mod 24), equivalently p = 1 (mod 8)")
print("claim matches computation:",
      sorted({p % 24 for p in missed}) == [1, 17] and sorted({p % 8 for p in missed}) == [1])

# its two quoted witnesses
for p, t in ((17, (5, 30, 510)), (97, (25, 810, 392850))):
    print("witness p=%d %s ->" % (p, t), sum((F(1, v) for v in t), F(0)) == F(4, p))
# its F5 refutation arithmetic
for p in (73, 97):
    k = (p - 3) // 4 if p % 4 == 3 else (p - 1) // 4
    Mp = p * ((p + 7) // 4)
    ds = [d for d in range(1, int(Mp ** 0.5) + 1) if Mp % d == 0]
    pairs = [(d, Mp // d) for d in ds if (d + Mp // d) == 7] + \
            [(d, e) for d in ds for e in [Mp // d] if False]
    # divisor pair {a,b} of M' with a+b = 7 and ab = M' is what the split needs;
    # the weaker reading is: some pair of divisors summing to 7
    small = [d for d in range(1, 8) if Mp % d == 0]
    print("p=%d  M'=%d  divisors<=7: %s  pairs summing to 7: %s"
          % (p, Mp, small, [(a, 7 - a) for a in small if (7 - a) > 0 and Mp % (7 - a) == 0]))
