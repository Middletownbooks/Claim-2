"""Verification of arXiv 2508.07383 (Ghermoul, Erdos-Straus polynomial families).

Every identity and coverage claim checked with exact Fraction / integer
arithmetic. Nothing graded from reading.
"""
from fractions import Fraction as F

def p1(x, y, z): return x * (4 * y * z - 1) - y * z
def p2(x, y, z): return x * (4 * y * z - z - 1) - y * z
def p3(x, y, z): return x * (8 * y - 3) - 6 * y + 2
def p4(x, y, z): return x * x - x

R = range(1, 13)

# ---- (18)-(21): the factorisations 4p_i + 1
bad = []
for x in R:
    for y in R:
        for z in R:
            if 4 * p1(x, y, z) + 1 != (4 * x - 1) * (4 * y * z - 1): bad.append(("18", x, y, z))
            if 4 * p2(x, y, z) + 1 != (4 * x - 1) * (4 * y * z - 1) - 4 * x * z: bad.append(("19", x, y, z))
            if 4 * p3(x, y, z) + 1 != (8 * y - 3) * (4 * x - 3): bad.append(("20", x, y, z))
            if 4 * p4(x, y, z) + 1 != (2 * x - 1) ** 2: bad.append(("21", x, y, z))
print("factorisation identities (18)-(21):", "ALL HOLD" if not bad else bad[:5])

# ---- (22), (26), (30): the three explicit Erdos-Straus decompositions
def case1(x, y, z):
    b = (4*x-1)*y*z*(4*y*z + z - 1)
    c = (4*x-1)*y*z
    d = (4*x-1)*y*(4*y*z-1)*(4*y*z + z - 1)
    return (4*p1(x,y,z)+1), (b, c, d)

def case2(x, y, z):
    K = 4*x*y - x - y
    b = z*K
    c = K*((4*y-1)*z - 1)*((4*x-1)*(4*y*z-1) - 4*x*z)
    d = z*K*((4*y-1)*z - 1)
    return (4*p2(x,y,z)+1), (b, c, d)

def case3(x, y, z):
    b = (4*x-3)*(3*y-1)
    c = 2*(4*x-3)*(3*y-1)
    d = (4*x-3)*(6*y-2)*(8*y-3)
    return (4*p3(x,y,z)+1), (b, c, d)

for name, fn in (("case 1 / eq (22)", case1), ("case 2 / eq (26)", case2), ("case 3 / eq (30)", case3)):
    n = ok = 0
    fail = None
    for x in R:
        for y in R:
            for z in R:
                a, t = fn(x, y, z)
                n += 1
                if any((not isinstance(v, int)) or v <= 0 for v in t):
                    fail = fail or (x, y, z, "non-positive denominator", t); continue
                if sum((F(1, v) for v in t), F(0)) == F(4, a):
                    ok += 1
                else:
                    fail = fail or (x, y, z, "identity fails", a, t)
    print("%-18s %5d/%5d exact  %s" % (name, ok, n, "" if ok == n else fail))

# ---- Theorem 1
print("\nTheorem 1(a)  p2(1,1,z) = 2z-1 for z=1..40:",
      all(p2(1, 1, z) == 2*z - 1 for z in range(1, 41)))
print("Theorem 1(b)  p2(1+c,2,1) = 6c+4:",
      all(p2(1 + c, 2, 1) == 6*c + 4 for c in range(0, 40)))
print("Theorem 1(b)  p1(1+2c,1,1) = 6c+2:",
      all(p1(1 + 2*c, 1, 1) == 6*c + 2 for c in range(0, 40)))
