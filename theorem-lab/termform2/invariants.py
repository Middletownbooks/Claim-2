#!/usr/bin/env python3
"""
An INDEPENDENT library of number-theoretic invariants.

Implemented here by trial division, with no reference to the search language
and no import from `termform/`. Its only roles are (a) to supply the values of
the pre-registered targets and (b) to interpret, after the fact, what the
untargeted search found. It never steers a search.

An entry is removed if it duplicates another exactly (`smallest_div_gt_1` was
`spf` under a second name); a match must identify one invariant, not two.
"""
import math


def factor(n):
    f, d = {}, 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def divisors(n):
    ds = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            ds.append(i)
            if i != n // i:
                ds.append(n // i)
        i += 1
    return sorted(ds)


def _order(a, n):
    if math.gcd(a, n) != 1 or n == 1:
        return 0
    x, k = a % n, 1
    while x != 1:
        x = x * a % n
        k += 1
        if k > n:
            return 0
    return k


def carmichael(n):
    if n == 1:
        return 1
    out = 1
    for p, e in factor(n).items():
        if p == 2 and e >= 3:
            l = 2 ** (e - 2)
        else:
            l = (p - 1) * p ** (e - 1)
        out = out * l // math.gcd(out, l)
    return out


def _sq(n):
    r = math.isqrt(n)
    return r * r == n


def _core(n):
    out = 1
    for p, e in factor(n).items():
        if e % 2:
            out *= p
    return out


# name -> callable. Every entry is total on the positive integers.
LIBRARY = {
    "tau":              lambda n: len(divisors(n)),
    "tau_minus_1":      lambda n: len(divisors(n)) - 1,
    "sigma":            lambda n: sum(divisors(n)),
    "sigma_proper":     lambda n: sum(divisors(n)) - n,
    "sigma2":           lambda n: sum(d * d for d in divisors(n)),
    "phi":              lambda n: sum(1 for k in range(1, n + 1)
                                      if math.gcd(k, n) == 1),
    "carmichael":       carmichael,
    "mobius":           lambda n: 0 if any(e > 1 for e in factor(n).values())
                                  else (-1) ** len(factor(n)),
    "omega":            lambda n: len(factor(n)),
    "Omega":            lambda n: sum(factor(n).values()),
    "spf":              lambda n: min(factor(n)) if n > 1 else 0,
    "gpf":              lambda n: max(factor(n)) if n > 1 else 0,
    "rad":              lambda n: math.prod(factor(n)) if n > 1 else 1,
    "core":             _core,
    "is_prime":         lambda n: 1 if n > 1 and len(factor(n)) == 1
                                  and sum(factor(n).values()) == 1 else 0,
    "is_prime_power":   lambda n: 1 if n > 1 and len(factor(n)) == 1 else 0,
    "is_squarefree":    lambda n: 0 if any(e > 1 for e in factor(n).values())
                                  else 1,
    "is_square":        lambda n: 1 if _sq(n) else 0,
    "is_cube":          lambda n: 1 if round(n ** (1 / 3)) ** 3 == n else 0,
    "is_even":          lambda n: 1 if n % 2 == 0 else 0,
    "v_2":              lambda n: factor(n).get(2, 0),
    "v_3":              lambda n: factor(n).get(3, 0),
    "v_spf":            lambda n: factor(n)[min(factor(n))] if n > 1 else 0,
    "v_gpf":            lambda n: factor(n)[max(factor(n))] if n > 1 else 0,
    "nu":               lambda n: max(factor(n).values()) if n > 1 else 0,
    "n_div_spf":        lambda n: n // min(factor(n)) if n > 1 else 0,
    "n_div_gpf":        lambda n: n // max(factor(n)) if n > 1 else 0,
    "n_minus_n_div_spf": lambda n: n - n // min(factor(n)) if n > 1 else 0,
    "n_minus_phi":      lambda n: n - sum(1 for k in range(1, n + 1)
                                          if math.gcd(k, n) == 1),
    "tau_of_square":    lambda n: len(divisors(n * n)),
    "unitary_divisors": lambda n: 2 ** len(factor(n)) if n > 1 else 1,
    "odd_divisors":     lambda n: sum(1 for d in divisors(n) if d % 2),
    "even_divisors":    lambda n: sum(1 for d in divisors(n) if d % 2 == 0),
    "composite_divisors": lambda n: sum(1 for d in divisors(n) if d > 1 and
                                        len(factor(d)) + sum(factor(d).values())
                                        > 2),
    "divisors_le_sqrt": lambda n: sum(1 for d in divisors(n) if d * d <= n),
    "largest_div_le_sqrt": lambda n: max(d for d in divisors(n) if d * d <= n),
    "ord_2_mod_n":      lambda n: _order(2, n),
    "ord_3_mod_n":      lambda n: _order(3, n),
    "dedekind_psi":     lambda n: math.prod(p ** (e - 1) * (p + 1)
                                            for p, e in factor(n).items())
                                  if n > 1 else 1,
    "jordan_J2":        lambda n: math.prod(p ** (2 * e) - p ** (2 * e - 2)
                                            for p, e in factor(n).items())
                                  if n > 1 else 1,
    "n":                lambda n: n,
    "n_minus_1":        lambda n: n - 1,
    "floor_n_2":        lambda n: n // 2,
    "floor_n_3":        lambda n: n // 3,
    "floor_n_4":        lambda n: n // 4,
    "isqrt":            math.isqrt,
    "digit_sum_10":     lambda n: sum(int(c) for c in str(n)),
    "bit_count":        lambda n: bin(n).count("1"),
    "bit_length":       lambda n: n.bit_length(),
}

# The thirteen pre-registered Round-2 targets (PREREG section 4).
TARGETS = ["is_prime", "is_square", "n_div_spf", "gpf", "omega", "Omega",
           "is_squarefree", "rad", "v_2", "sigma", "is_prime_power", "phi",
           "v_spf"]


def vector(name, objects):
    f = LIBRARY[name]
    return tuple(f(n) for n in objects)


if __name__ == "__main__":
    for t in TARGETS:
        print("%-16s %s" % (t, vector(t, range(2, 14))))
