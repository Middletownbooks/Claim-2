"""Compute S_m from Salez (2014) Proposition 3, rather than transcribing it.

For p = a*t + b, each reference equation must hold IDENTICALLY IN t, which
collapses it to divisibility conditions on the constant-degree variables.
Degrees per Lemma 1 / Prop 3:
  (14a) B,C,D const   (14b) A,B,E const   (14c) B,D,E const
  (15a) A,B,E const   (15b) B,C,F const   (15c) B,D,F const   (15d) C,D,F const
"""
from math import gcd
from functools import lru_cache


def divisors(n):
    ds, i = [], 1
    while i * i <= n:
        if n % i == 0:
            ds.append(i)
            if i != n // i:
                ds.append(n // i)
        i += 1
    return sorted(ds)


def egyptian_class(a, b, LIM=60):
    """Does one of the 7 reference equations certify the whole class
    p = a*t + b?  Returns the tag of the first equation that fires."""

    # ---- (14a):  M = 4BCD-1 ;  M | a*C  and  M | B + b*C
    for B in range(1, LIM + 1):
        for C in range(1, LIM + 1):
            if gcd(B, C) != 1:
                continue
            for D in range(1, LIM + 1):
                if gcd(C, D) != 1:
                    continue
                M = 4 * B * C * D - 1
                if (a * C) % M == 0 and (B + b * C) % M == 0:
                    return "14a"

    # the remaining six all force a product to divide a, so enumerate divisors
    da = divisors(a)

    # ---- (14b): 4AB | a ; 4AB | b+E ; E | A+B ; (4ABD,E)=1
    for P in da:                                   # P = 4AB
        if P % 4:
            continue
        AB = P // 4
        for A in divisors(AB):
            B = AB // A
            if gcd(A, B) != 1:
                continue
            for E in range(1, LIM + 1):
                if (b + E) % P == 0 and (A + B) % E == 0 and gcd(4 * A * B, E) == 1:
                    return "14b"

    # ---- (14c): N = 4BDE | a ; N | b + E + 4B^2 D
    for N in da:
        if N % 4:
            continue
        BDE = N // 4
        for B in divisors(BDE):
            for D in divisors(BDE // B):
                E = BDE // B // D
                if gcd(4 * B * D, E) != 1:
                    continue
                if (b + E + 4 * B * B * D) % N == 0:
                    return "14c"

    # ---- (15a): 4AB | a*E ; 4AB | b*E + 1 ; E | A+B
    for AB in range(1, LIM * LIM + 1):
        P = 4 * AB
        for E in range(1, LIM + 1):
            if (a * E) % P or (b * E + 1) % P:
                continue
            for A in divisors(AB):
                B = AB // A
                if gcd(A, B) == 1 and (A + B) % E == 0 and gcd(4 * A * B, E) == 1:
                    return "15a"

    # ---- (15b): 4BC | a ; 4BC | b+F ; F | a*B ; F | b*B + C
    for P in da:
        if P % 4:
            continue
        BC = P // 4
        for B in divisors(BC):
            C = BC // B
            if gcd(B, C) != 1:
                continue
            for F in range(1, 4 * LIM * LIM):
                if (b + F) % P:
                    continue
                if (a * B) % F == 0 and (b * B + C) % F == 0:
                    return "15b"

    # ---- (15c): 4BD | a ; 4BD | b+F ; F | 4B^2 D + 1
    for P in da:
        if P % 4:
            continue
        BD = P // 4
        for B in divisors(BD):
            D = BD // B
            for F in range(1, 4 * LIM * LIM):
                if (b + F) % P:
                    continue
                if (4 * B * B * D + 1) % F == 0:
                    return "15c"

    # ---- (15d): 4CD | a ; 4CD | b+F ; F | a^2, F | 2ab, F | b^2 + 4C^2 D
    for P in da:
        if P % 4:
            continue
        CD = P // 4
        for C in divisors(CD):
            D = CD // C
            if gcd(C, D) != 1:
                continue
            for F in range(1, 4 * LIM * LIM):
                if (b + F) % P:
                    continue
                if (a * a) % F == 0 and (2 * a * b) % F == 0 and \
                   (b * b + 4 * C * C * D) % F == 0:
                    return "15d"
    return None


def crt(r1, m1, r2, m2):
    g = gcd(m1, m2)
    assert (r2 - r1) % g == 0
    lcm = m1 // g * m2
    inv = pow(m1 // g, -1, m2 // g)
    return (r1 + (m1 * (((r2 - r1) // g * inv) % (m2 // g)))) % lcm, lcm


def S(m, LIM=60):
    """S_m = { x mod m : the class n = x (mod m), n = 1 (mod 24) is certified }"""
    a = 24 * m // gcd(24, m)
    out = set()
    for x in range(m):
        try:
            b, _ = crt(1, 24, x, m)
        except AssertionError:
            continue
        if egyptian_class(a, b, LIM):
            out.add(x)
    return out
