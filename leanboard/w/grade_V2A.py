from fractions import Fraction as F
from verify import check_family, coverage, isprime

def f0(n):  # n = 0 mod 4
    k = n // 4
    return (3 * k, 3 * k, 3 * k)

def f2(n):  # n = 4k+2
    k = (n - 2) // 4
    return (2 * k + 1, 2 * k + 2, (2 * k + 1) * (2 * k + 2))

def f3(n):  # n = 4k+3
    k = (n - 3) // 4
    return (2 * k + 2, 2 * k + 2, n * (k + 1))

def c1(p):  # p = 8j+5
    j = (p - 5) // 8
    return (2 * (j + 1), 2 * p * (j + 1), p * (j + 1))

def factors(m):
    fs, d = set(), 2
    while d * d <= m:
        while m % d == 0:
            fs.add(d); m //= d
        d += 1
    if m > 1:
        fs.add(m)
    return fs

def c2(p):  # p = 1 mod 8, needs a prime factor of M congruent to 2 mod 3
    t = (p + 3) // 4
    M = p * t
    q = min((q for q in factors(M) if q % 3 == 2), default=None)
    if q is None:
        raise ValueError("no divisor = 2 mod 3")
    return (t, (M + q) // 3, (M + M * M // q) // 3)

fams = [
    ("n = 0 mod 4",              lambda n: n % 4 == 0,                          f0),
    ("n = 2 mod 4",              lambda n: n % 4 == 2,                          f2),
    ("n = 3 mod 4",              lambda n: n % 4 == 3,                          f3),
    ("C1: p = 5 mod 8",          lambda p: isprime(p) and p % 8 == 5,           c1),
    ("C2: p=1 mod8, q=2 mod3",   lambda p: isprime(p) and p % 8 == 1
                                           and any(q % 3 == 2 for q in factors(p * ((p + 3) // 4))), c2),
]
conds = []
for name, cond, xyz in fams:
    ok, *_ = check_family(name, cond, xyz, 2, 20000)
    if ok:
        conds.append(cond)
missed = coverage(conds, 2, 20000)
print("\nn in [2,20000] uncovered by V2-A's families:", len(missed))
print("all uncovered are prime, = 1 mod 24:",
      all(isprime(n) and n % 24 == 1 for n in missed), " first ten:", missed[:10])

print("\n-- its quoted witnesses --")
for p, t in ((73, (20, 210, 30660)), (1033, (260, 38370, 1030541460)),
             (17, (5, 30, 510)), (41, (11, 154, 6314))):
    print(" p=%-5d %s -> %s" % (p, t, sum((F(1, v) for v in t), F(0)) == F(4, p)))
