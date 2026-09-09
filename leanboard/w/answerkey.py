"""Answer-key groundwork for Phase W (Erdos-Straus).

Establishes, computationally, the facts the scorer needs:
  1. reduction to primes is sound (composite n inherits a solution from any divisor);
  2. the residue classes mod 840 that survive the classical covering conditions;
  3. an independent brute-force check that solutions exist for all n in a range.
Nothing here is shown to the agents.
"""
from math import gcd


def isprime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True

M = 840

def qr(c, p):
    # nonzero quadratic residue; r = 0 is excluded deliberately
    return any((r * r - c) % p == 0 for r in range(1, p))

# Classical Mordell-type covering conditions dispatch n unless
# n is 1 mod 24 and a quadratic residue mod 5 and mod 7.
# primes > 7 are coprime to 840, so restrict to the unit classes
surv = [c for c in range(M)
        if gcd(c, M) == 1 and c % 24 == 1 and qr(c, 5) and qr(c, 7)]
print("surviving classes mod 840:", surv)
print("are they squares of units mod 840?",
      sorted(surv) == sorted({(r*r) % M for r in (1, 11, 13, 17, 19, 23)}))
print("squares:", sorted({(r*r) % M for r in (1, 11, 13, 17, 19, 23)}))

# Brute force: minimal solutions for primes up to a bound, recorded by class.
def solve(n, cap=4000):
    for x in range(n // 4 + 1, 3 * n // 4 + 2):
        r1 = 4 * x - n           # 4/n - 1/x = (4x-n)/(nx)
        if r1 <= 0:
            continue
        num, den = r1, n * x
        for y in range(den // num + 1, 2 * den // num + 2):
            if y > cap * n:
                break
            r2n, r2d = num * y - den, den * y
            if r2n <= 0:
                continue
            if r2d % r2n == 0:
                return (x, y, r2d // r2n)
    return None

bad = []
hard = {}
for n in range(2, 3000):
    if not isprime(n):
        continue
    s = solve(n)
    if s is None:
        bad.append(n)
    elif n % M in surv:
        hard[n] = s
print("primes < 3000 with no solution found:", bad)
print("sample solutions in surviving classes:",
      dict(list(hard.items())[:8]))
