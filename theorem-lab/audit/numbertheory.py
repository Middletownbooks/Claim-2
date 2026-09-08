#!/usr/bin/env python3
"""
Independent number-theoretic ground truth.

This module is NOT part of the laboratory and is never imported by lab.py.
It exists so the auditor can compare what the blind learner produced against
independently computed invariants (nu, lambda, phi, orders).

Everything here is MATHEMATICALLY_DERIVED background knowledge supplied by
the auditor. It must never be fed into the learner.
"""
import math
from functools import lru_cache


@lru_cache(maxsize=None)
def factorize(n):
    f = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return tuple(sorted(f.items()))


def nu(m):
    """max_p v_p(m); nu(1) = 0."""
    fs = factorize(m)
    return max((e for _, e in fs), default=0)


def carmichael(m):
    """Carmichael exponent lambda(m); lambda(1) = 1."""
    if m == 1:
        return 1
    total = 1
    for p, e in factorize(m):
        if p == 2:
            if e == 1:
                part = 1
            elif e == 2:
                part = 2
            else:
                part = 2 ** (e - 2)
        else:
            part = (p - 1) * p ** (e - 1)
        total = math.lcm(total, part)
    return total


def euler_phi(m):
    r = 1
    for p, e in factorize(m):
        r *= (p - 1) * p ** (e - 1)
    return r


def squarefree(m):
    return all(e == 1 for _, e in factorize(m))


def L(m):
    """lcm over p | m of (p-1); the classical T-family exponent."""
    t = 1
    for p, _ in factorize(m):
        t = math.lcm(t, p - 1)
    return t


# --- direct definitional predicates (brute force, no theory used) ---

def E_direct(m, r, d):
    return all(pow(x, r + d, m) == pow(x, r, m) for x in range(m))


def T_direct(m, k):
    return all(pow(x, k, m) == x % m for x in range(m))


def U_direct(m, k):
    return all(pow(x, k, m) == x % m
               for x in range(m) if math.gcd(x, m) == 1)


# --- theory-side predictions ---

def E_formula(m, r, d):
    return r >= nu(m) and d % carmichael(m) == 0


def T_formula(m, k):
    """Classical classification, valid for k >= 2."""
    return squarefree(m) and (k - 1) % L(m) == 0
