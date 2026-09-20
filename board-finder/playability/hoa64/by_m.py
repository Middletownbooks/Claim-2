#!/usr/bin/env python3
"""The open-order question indexed by m, where n = 4m.

hoa64's micromag.py records the structural fact: "The open gaps below 2000 are all
4 (mod 8)". Verified against all 15 orders it knows about (13 shipped + the 1212 and
1940 its README still lists as missing) -- every one is n = 4m with m ODD.

The reason is one line: n = 0 mod 8 means n = 2*(n/2) with n/2 = 0 mod 4, so H(2) (x)
H(n/2) closes it by doubling. The genuinely hard orders are exactly n = 4m, m odd, and
indexing by m -- not by n -- is what makes the route structure visible.

This computes, for every odd m with 4m in [2000,3000], whether hoa64 can reach it and,
when it cannot, which single Williamson order would unlock it through cw_build.

NOTE ON SCOPE: the survivor set here is "not reachable by hoa64's implemented
constructions", which is a SUPERSET of the genuinely open orders. Intersecting it with a
real open-order table is a literature step this file does not take.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from coverage import reachable, is_prime_power

TS  = {47, 65, 93} | {3, 5, 7, 9, 11, 13, 15, 19, 23, 25, 27, 29, 31, 51, 59}
WDB = {1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,37,39,41,43,45,49,51,55,57,61,63}
SHIPPED_AND_MISSING = [668,716,892,1132,1244,1388,1436,1676,1772,1852,1916,1948,1964,1212,1940]


def factor(m):
    f, d, x = {}, 2, m
    while d * d <= x:
        while x % d == 0:
            f[d] = f.get(d, 0) + 1; x //= d
        d += 1
    if x > 1:
        f[x] = f.get(x, 0) + 1
    return f


def fstr(m):
    return '·'.join(f'{p}^{e}' if e > 1 else str(p) for p, e in sorted(factor(m).items()))


def cw_now(m):
    return [(ts, m // ts) for ts in sorted(TS) if m % ts == 0 and (m // ts) in WDB]


def cw_needs(m):
    return sorted({(ts, m // ts) for ts in sorted(TS)
                   if m % ts == 0 and (m // ts) % 2 == 1 and (m // ts) not in WDB})


def main(lo=2000, hi=3000):
    print("the 4-mod-8 structure, checked on every order hoa64 names:")
    bad = [n for n in SHIPPED_AND_MISSING if n % 8 != 4]
    print(f"  all {len(SHIPPED_AND_MISSING)} are n = 4m with m odd: {not bad}"
          + (f"  exceptions {bad}" if bad else ""))

    ms = [m for m in range(lo // 4 + (1 - (lo // 4) % 2), hi // 4 + 1, 2)]
    closed = [m for m in ms if reachable(4 * m)[0]]
    now = [m for m in ms if m not in closed and cw_now(m)]
    surv = [m for m in ms if m not in closed and not cw_now(m)]
    print(f"\nn = 4m in [{lo},{hi}] with m odd: {len(ms)} orders")
    print(f"  closed form (Paley / Kronecker / Miyamoto / CSV): {len(closed)}")
    print(f"  cw_build works today:                            {len(now)}")
    print(f"  survivors:                                       {len(surv)}\n")

    print(f"{'m':>5} {'n=4m':>6}  {'m':<14} route")
    for m in surv:
        need = cw_needs(m)
        r = ', '.join(f'W({w}) via T{ts}' for ts, w in need) if need else \
            ('no T-seq factorisation — m is PRIME' if len(factor(m)) == 1
             and list(factor(m).values()) == [1] else 'no T-seq factorisation')
        print(f"{m:>5} {4*m:>6}  {fstr(m):<14} {r}")

    prime_m = [m for m in surv if len(factor(m)) == 1 and list(factor(m).values()) == [1]]
    print(f"\nprime m among survivors: {len(prime_m)} -> {prime_m}")
    print("  For prime m there is no t*w factorisation, so Cooper-Wallis cannot help at ANY")
    print("  Williamson order: these need Williamson(m) itself, or a Goethals-Seidel / SDS")
    print("  difference family at prime length m.")
    print("\n  A COINCIDENCE NOT TO OVER-READ: that count can land on the same number as a")
    print("  reported open-order count without being the same set. Check the smallest")
    print("  element before treating the two as one list.")


if __name__ == '__main__':
    main()
