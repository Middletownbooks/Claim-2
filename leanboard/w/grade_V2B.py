from fractions import Fraction as F
from verify import check_family, coverage, isprime

def l1a(n):                      # n = 4k
    k = n // 4
    return (2 * k, 3 * k, 6 * k)

def l1b(n):                      # n = 4k+2
    k = (n - 2) // 4
    return (2 * k + 2, 2 * k + 2, (k + 1) * (2 * k + 1))

def l3(m):                       # m = 3 mod 4
    return ((m + 1) // 4, m * (m + 1) // 2, m * (m + 1) // 2)

def l4(m):                       # m = 2 mod 3
    return (m, (m + 1) // 3, m * (m + 1) // 3)

fams = [
    ("L1a: n = 0 mod 4", lambda n: n % 4 == 0, l1a),
    ("L1b: n = 2 mod 4", lambda n: n % 4 == 2, l1b),
    ("L3:  m = 3 mod 4", lambda n: n % 4 == 3, l3),
    ("L4:  m = 2 mod 3", lambda n: n % 3 == 2, l4),
]
conds = []
for name, cond, xyz in fams:
    ok, *_ = check_family(name, cond, xyz, 2, 20000)
    if ok:
        conds.append(cond)

# its coverage theorem: uncovered = odd n with EVERY prime factor = 1 mod 12
def pfac(m):
    fs, d = set(), 2
    while d * d <= m:
        while m % d == 0:
            fs.add(d); m //= d
        d += 1
    if m > 1:
        fs.add(m)
    return fs

direct = [n for n in range(2, 5000) if not any(c(n) for c in conds)]
rescued = [n for n in direct if any(any(c(p) for c in conds) for p in pfac(n))]
remain = [n for n in direct if n not in set(rescued)]
print("\nn in [2,5000): not directly covered %d, rescued by scaling %d, remain %d"
      % (len(direct), len(rescued), len(remain)))
print("V2-B claimed:                          832,                    649,       183")
print("remaining are exactly n with all prime factors = 1 mod 12:",
      all(all(p % 12 == 1 for p in pfac(n)) for n in remain))
print("first ten remaining:", remain[:10])
print("V2-B listed:        [13, 37, 61, 73, 97, 109, 157, 169, 181, 193]")

odd = [p for p in range(3, 20000) if isprime(p)]
cov = [p for p in odd if any(c(p) for c in conds)]
unc = [p for p in odd if p not in set(cov)]
print("\nodd primes < 20000: %d total, %d covered (%.1f%%), %d uncovered"
      % (len(odd), len(cov), 100.0 * len(cov) / len(odd), len(unc)))
print("V2-B claimed:       2261 total, 1706 covered (75.4%), 555 uncovered")
print("all uncovered = 1 mod 12:", all(p % 12 == 1 for p in unc))

print("\n-- its witnesses --")
for p, t in ((13, (4, 18, 468)), (37, (10, 124, 22940)),
             (61, (16, 326, 159088)), (73, (20, 210, 30660))):
    print(" p=%-4d %s -> %s" % (p, t, sum((F(1, v) for v in t), F(0)) == F(4, p)))

print("\n-- its F5 impossibility theorem, checked empirically --")
for a in (3, 7, 11, 15, 19, 23, 27, 31):
    hits = 0
    for p in unc:
        if (p + a) % 4:
            continue
        x = (p + a) // 4
        if x > 0 and (p * x + 1) % a == 0:
            hits += 1
    print("  a=%-3d covers %d of %d uncovered primes" % (a, hits, len(unc)))
