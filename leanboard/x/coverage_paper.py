"""What the paper's Conjecture 2 actually amounts to."""
from sympy import divisors, isprime

def p1_covers(q):
    # q = x(4yz-1) - yz.  With w = yz: 4x = (4q+1)/(4w-1) + 1, so this holds
    # iff 4q+1 has a divisor = 3 mod 4 that is >= 3 (the cofactor is then
    # automatically = 3 mod 4, so x is a positive integer).
    return any(d % 4 == 3 for d in divisors(4 * q + 1) if d >= 3)

def p3_covers(q):
    a = 4 * q + 1
    return any(A % 8 == 5 and (a // A) % 4 == 1 for A in divisors(a))

def p4_covers(q):
    x = 1
    while x * (x - 1) <= q:
        if x * (x - 1) == q:
            return True
        x += 1
    return False

def p2_covers(q):
    # a + u = z(4uy - u - 1) with u = 4x-1
    a = 4 * q + 1
    x = 1
    while True:
        u = 4 * x - 1
        if u * u > 4 * a + 4 * u:            # generous cut-off
            return False
        for z in divisors(a + u):
            D = (a + u) // z
            if (D + u + 1) % (4 * u) == 0 and (D + u + 1) // (4 * u) >= 1:
                return True
        x += 1

# cross-check the p1 characterisation against brute force
def p1_brute(q, cap=400):
    for y in range(1, cap):
        for z in range(1, cap // y + 1):
            w = y * z
            num = q + w
            if num % (4 * w - 1) == 0 and num // (4 * w - 1) >= 1:
                return True
    return False
print("p1 characterisation matches brute force on q=1..600:",
      all(p1_covers(q) == p1_brute(q) for q in range(1, 601)))

N = 60000
uncovered, only_p2 = [], []
for q in range(1, N + 1):
    if p1_covers(q) or p3_covers(q) or p4_covers(q):
        continue
    if p2_covers(q):
        only_p2.append(q)
    else:
        uncovered.append(q)
print("\nq in [1,%d]: uncovered by ALL FOUR: %d" % (N, len(uncovered)))
print("q needing p2 specifically: %d" % len(only_p2))
print("  of those, q = 0 mod 6:", sum(1 for q in only_p2 if q % 6 == 0),
      " q odd:", sum(1 for q in only_p2 if q % 2))

# where is the genuinely hard part?
hard = [q for q in range(1, N + 1) if isprime(4 * q + 1)
        and not (p1_covers(q) or p3_covers(q) or p4_covers(q))]
print("\nprimes a=4q+1 with q<=%d not reachable by p1/p3/p4: %d" % (N, len(hard)))
print("  all have a = 1 mod 24:", all((4 * q + 1) % 24 == 1 for q in hard))
print("  all have q = 0 mod 6 :", all(q % 6 == 0 for q in hard))
print("  first ten a:", [4 * q + 1 for q in hard[:10]])

print("\n--- what Theorem 1 leaves unproven ---")
# Theorem 1 proves coverage for: q odd (14), q = 4 mod 6 (15), q = 2 mod 6 (16).
proved_by_thm1 = lambda q: (q % 2 == 1) or (q % 6 == 4) or (q % 6 == 2)
rest = [q for q in range(1, N + 1) if not proved_by_thm1(q)]
print("q in [1,%d] not covered by Theorem 1's explicit formulas: %d" % (N, len(rest)))
print("  all are q = 0 mod 6:", all(q % 6 == 0 for q in rest))
print("  equivalently a = 4q+1 = 1 mod 24:", all((4 * q + 1) % 24 == 1 for q in rest))
print("  of these, covered by some p_i (unproved, computational): %d of %d"
      % (sum(1 for q in rest if p1_covers(q) or p2_covers(q)
             or p3_covers(q) or p4_covers(q)), len(rest)))
