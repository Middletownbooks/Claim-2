#!/usr/bin/env python3
"""Which orders in [2000,3000] can hoa64's IMPLEMENTED classical families reach?

Conditions replicated from the repo's own code (hadamard.py:hadamard_known,
miyamoto.py:miyamoto_from_cache, README 'Construction Methods Implemented'), not
from memory:

  Sylvester   n = 2^k
  Paley I     n = q+1,    q prime power, q = 3 mod 4
  Paley II    n = 2(q+1), q prime power, q = 1 mod 4
  Kronecker   n = a*b with a,b both reachable
  Miyamoto    n = 4q,     q prime power, q = 1 mod 4, and H(q-1) reachable
  CSV import  the 13 shipped matrices (12 Alpoge + Djokovic 1852)

Cooper-Wallis and Goethals-Seidel are implemented too but are parameterised by
Turyn/T-sequence and Williamson databases rather than a closed-form condition on n,
so they are reported separately as ROUTES rather than folded into coverage.
"""
import math
from functools import lru_cache

SHIPPED = {668, 716, 892, 1132, 1244, 1388, 1436, 1676, 1772, 1852, 1916, 1948, 1964}


def is_prime(n):
    if n < 2: return False
    if n % 2 == 0: return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0: return False
        d += 2
    return True


def is_prime_power(n):
    """returns (p,e) or None"""
    if n < 2: return None
    for p in range(2, int(math.isqrt(n)) + 1):
        if n % p == 0:
            if not is_prime(p): continue
            m, e = n, 0
            while m % p == 0:
                m //= p; e += 1
            return (p, e) if m == 1 else None
    return (n, 1) if is_prime(n) else None


@lru_cache(maxsize=None)
def reachable(n):
    """(True, family) if hoa64's implemented closed-form families build H(n)."""
    if n == 1: return (True, 'trivial')
    if n == 2: return (True, 'trivial')
    if n in SHIPPED: return (True, 'CSV import (Alpoge/Djokovic)')
    if n & (n - 1) == 0: return (True, 'Sylvester 2^k')
    if n % 4: return (False, None)
    q = n - 1
    if q % 4 == 3 and is_prime_power(q): return (True, f'Paley I (q={q})')
    if n % 2 == 0:
        q = n // 2 - 1
        if q % 4 == 1 and is_prime_power(q): return (True, f'Paley II (q={q})')
    q = n // 4
    if q >= 5 and q % 4 == 1 and is_prime_power(q) and reachable(q - 1)[0]:
        return (True, f'Miyamoto (q={q}, needs H({q-1}))')
    for d in range(2, int(math.isqrt(n)) + 1):
        if n % d: continue
        a, b = reachable(d), reachable(n // d)
        if a[0] and b[0]:
            return (True, f'Kronecker {d}x{n//d}')
    return (False, None)


def cw_routes(n):
    """Cooper-Wallis: H(4*t*m) from T-sequences of length t and Williamson order m.
    Report the arithmetic factorisations; EXISTENCE of each ingredient is a lookup."""
    if n % 4: return []
    k = n // 4
    out = []
    for t in range(1, k + 1):
        if k % t: continue
        m = k // t
        if m % 2 == 1:                      # Williamson matrices have odd order
            out.append((t, m))
    return out


if __name__ == '__main__':
    lo, hi = 2000, 3000
    orders = [n for n in range(lo, hi + 1) if n % 4 == 0]
    cov, gap = [], []
    for n in orders:
        ok, fam = reachable(n)
        (cov if ok else gap).append((n, fam))

    print(f"orders = 0 mod 4 in [{lo},{hi}]: {len(orders)}")
    print(f"  reachable by hoa64's closed-form families: {len(cov)}"
          f"  ({100*len(cov)/len(orders):.0f}%)")
    print(f"  NOT reachable:                             {len(gap)}"
          f"  ({100*len(gap)/len(orders):.0f}%)\n")

    from collections import Counter
    fams = Counter(f.split(' (')[0].split(' ')[0] for _, f in cov)
    print("by family:", dict(fams), "\n")

    print(f"the {len(gap)} orders this toolchain cannot build in closed form:")
    for i in range(0, len(gap), 10):
        print('   ' + '  '.join(f'{n}' for n, _ in gap[i:i+10]))

    print("\n--- 2060 specifically ---")
    n = 2060
    print(f"  2060 = {' * '.join(str(p)+'^'+str(e) if e>1 else str(p) for p,e in [(2,2),(5,1),(103,1)])}")
    print(f"  Sylvester : 2060 is not a power of 2                      -> no")
    print(f"  Paley I   : q = 2059 = 29*71, not a prime power           -> no")
    print(f"  Paley II  : q = 1029 = 3*7^3, not a prime power           -> no")
    q = n // 4
    print(f"  Miyamoto  : q = {q} = 5*103, and {q} mod 4 = {q%4} (needs 1) -> no")
    print("  Kronecker : factor pairs a*b = 2060 with BOTH Hadamard orders:")
    for d in range(2, int(math.isqrt(n)) + 1):
        if n % d: continue
        e = n // d
        okd, oke = reachable(d)[0], reachable(e)[0]
        print(f"      {d:>4} x {e:<5} -> H({d}) {'yes' if okd else 'NO '} , H({e}) {'yes' if oke else 'NO '}")
    print("  => every closed-form family in the repo misses 2060.\n")

    print("  Cooper-Wallis routes, 4*t*m = 2060 so t*m = 515 (m odd):")
    for t, m in cw_routes(n):
        note = ''
        if t in (2,3,4,5,6,7,8,13,15): note = '   <- Turyn length IS in the repo db'
        print(f"      t = {t:<4} m = {m:<4}  (T-sequences of length {t}, Williamson order {m}){note}")
