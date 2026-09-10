"""Salez (2014) Prop. 3, with EXACT divisor enumeration.

For p = a*t + b each reference equation must hold identically in t, so it
collapses to divisibility conditions on the constant-degree variables. Every
loop below enumerates divisors of a quantity the conditions force, rather
than ranging over a guessed bound -- the one exception is the single free
variable in (14a) and (15a), controlled by CLIM/ELIM.
"""
from math import gcd


def divisors(n):
    n = abs(n)
    ds, i = [], 1
    while i * i <= n:
        if n % i == 0:
            ds.append(i)
            if i != n // i:
                ds.append(n // i)
        i += 1
    return sorted(ds)


def egyptian_class(a, b, CLIM=400, ELIM=400):
    da = divisors(a)

    # (14a) M = 4BCD-1 ;  M | a*C ;  M | B + b*C
    for C in range(1, CLIM + 1):
        for M in divisors(a * C):
            if M % 4 != 3:
                continue
            q = (M + 1) // 4                       # = B*C*D
            if q % C:
                continue
            for B in divisors(q // C):
                if gcd(B, C) != 1:
                    continue
                D = q // C // B
                if gcd(C, D) != 1:
                    continue
                if (B + b * C) % M == 0:
                    return "14a"

    # (14b) 4AB | a ; 4AB | b+E ; E | A+B ; (4ABD,E)=1
    for P in da:
        if P % 4 or (b + 0) % 1:
            continue
        AB = P // 4
        for A in divisors(AB):
            B = AB // A
            if gcd(A, B) != 1:
                continue
            for E in divisors(A + B):
                if (b + E) % P == 0 and gcd(4 * A * B, E) == 1:
                    return "14b"

    # (14c) N = 4BDE | a ; N | b + E + 4B^2 D
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

    # (15a) 4AB | a*E ; 4AB | b*E+1 ; E | A+B ; (4ABD,E)=1
    for E in range(1, ELIM + 1):
        g = gcd(a * E, b * E + 1)
        for P in divisors(g):
            if P % 4:
                continue
            AB = P // 4
            for A in divisors(AB):
                B = AB // A
                if gcd(A, B) != 1:
                    continue
                if (A + B) % E == 0 and gcd(4 * A * B, E) == 1:
                    return "15a"

    # (15b) 4BC | a ; F = -b mod 4BC ; F | a*B ; F | b*B + C
    for P in da:
        if P % 4:
            continue
        BC = P // 4
        for B in divisors(BC):
            C = BC // B
            if gcd(B, C) != 1:
                continue
            for F in divisors(a * B):
                if (b + F) % P == 0 and (b * B + C) % F == 0:
                    return "15b"

    # (15c) 4BD | a ; F = -b mod 4BD ; F | 4B^2 D + 1
    for P in da:
        if P % 4:
            continue
        BD = P // 4
        for B in divisors(BD):
            D = BD // B
            for F in divisors(4 * B * B * D + 1):
                if (b + F) % P == 0:
                    return "15c"

    # (15d) 4CD | a ; F = -b mod 4CD ; F | a^2, 2ab, b^2 + 4C^2 D
    for P in da:
        if P % 4:
            continue
        CD = P // 4
        for C in divisors(CD):
            D = CD // C
            if gcd(C, D) != 1:
                continue
            g = gcd(gcd(a * a, 2 * a * b), b * b + 4 * C * C * D)
            for F in divisors(g):
                if (b + F) % P == 0:
                    return "15d"
    return None


def crt(r1, m1, r2, m2):
    g = gcd(m1, m2)
    if (r2 - r1) % g:
        return None
    lcm = m1 // g * m2
    inv = pow(m1 // g, -1, m2 // g)
    return (r1 + m1 * (((r2 - r1) // g * inv) % (m2 // g))) % lcm


def S(m, **kw):
    a = 24 * m // gcd(24, m)
    out = set()
    for x in range(m):
        b = crt(1, 24, x, m)
        if b is None:
            continue
        if egyptian_class(a, b, **kw):
            out.add(x)
    return out
