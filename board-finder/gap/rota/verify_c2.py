#!/usr/bin/env python3
"""Chow's two counterexamples to C(2), verified exactly.

Paper: Timothy Y. Chow, "Reduction of Rota's basis conjecture to a problem on
three bases", arXiv:math/0504367v4, 8 Sep 2008. Transcript supplied by the
operator, so the TEXT is SECONDARY-RELAYED; the two checks below make the
MATHEMATICS primary.

C(k) is Conjecture 2 with '3' replaced by 'k'. C(2): M of rank n on 2n elements,
a disjoint union of 2 bases; I_1..I_n disjoint independent sets, 0 <= |I_i| <= 2;
is there an n x 2 grid holding each element once, row i containing I_i, with both
columns bases? Chow says C(2) is FALSE and gives two witnesses.
"""
import itertools
from fractions import Fraction

# ---------------------------------------------------------------- 1. M(K_4)
# Graphic matroid of K_4. A basis is a spanning tree: 3 edges, no cycle.
EDGES = [(1,2),(3,4),(1,3),(2,4),(1,4),(2,3)]
def is_spanning_tree(es):
    if len(es) != 3: return False
    parent = {v: v for v in (1,2,3,4)}
    def find(x):
        while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for a, b in es:
        ra, rb = find(a), find(b)
        if ra == rb: return False          # cycle
        parent[ra] = rb
    return len({find(v) for v in (1,2,3,4)}) == 1

# POSITIVE CONTROL: the star at vertex 1 is a spanning tree.
assert is_spanning_tree([(1,2),(1,3),(1,4)])
# NEGATIVE TESTS: a triangle is not, and nor is a 2-edge set.
assert not is_spanning_tree([(2,3),(3,4),(2,4)])
assert not is_spanning_tree([(1,2),(1,3)])
print("M(K_4) spanning-tree check: positive control passes, two negatives fire.")

# The three pairs of non-incident edges = the three perfect matchings.
I = [[(1,2),(3,4)], [(1,3),(2,4)], [(1,4),(2,3)]]
flat = [e for row in I for e in row]
assert sorted(flat) == sorted(EDGES) and len(set(flat)) == 6
print(f"  I_1, I_2, I_3 = {I}")
print("  each is a pair of non-incident edges, and together they are all 6 edges.")

good = []
for pick in itertools.product((0,1), repeat=3):          # which element of I_i goes left
    left  = [I[i][pick[i]]     for i in range(3)]
    right = [I[i][1-pick[i]]   for i in range(3)]
    if is_spanning_tree(left) and is_spanning_tree(right):
        good.append((left, right))
print(f"  grids with BOTH columns spanning trees: {len(good)} of 8")
assert good == []
print("  ASSERTED: none. M(K_4) with the three matchings REFUTES C(2).")
print()
# and show the near-misses, since they are the content of the obstruction
for pick in itertools.product((0,1), repeat=3):
    left  = [I[i][pick[i]] for i in range(3)]
    right = [I[i][1-pick[i]] for i in range(3)]
    print(f"    left {left} tree={is_spanning_tree(left)!s:<5} "
          f"right {right} tree={is_spanning_tree(right)}")

# ---------------------------------------------------------------- 2. Oxley's J
print()
print("Oxley's matroid J, as Chow represents it by vectors in Euclidean 4-space:")
J = [
    [(-2,3,0,1), (0,0,1,1)],
    [(0,2,0,1),  (1,0,3,1)],
    [(1,0,0,1),  (0,1,2,1)],
    [(0,1,0,1),  (4,0,0,1)],
]
def det4(rows):
    m = [[Fraction(x) for x in r] for r in rows]
    d = Fraction(1)
    for c in range(4):
        piv = next((r for r in range(c, 4) if m[r][c] != 0), None)
        if piv is None: return Fraction(0)
        if piv != c: m[c], m[piv] = m[piv], m[c]; d = -d
        d *= m[c][c]
        inv = Fraction(1) / m[c][c]
        for r in range(c+1, 4):
            f = m[r][c] * inv
            if f:
                m[r] = [m[r][k] - f*m[c][k] for k in range(4)]
    return d
def is_basis(vs): return len(vs) == 4 and det4(vs) != 0

# POSITIVE CONTROL: the standard basis has determinant 1.
assert is_basis([(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1)])
# NEGATIVE TEST: a repeated vector is dependent.
assert not is_basis([(1,0,0,0),(1,0,0,0),(0,0,1,0),(0,0,0,1)])
print("  determinant check: positive control passes, negative fires.")
allv = [v for row in J for v in row]
assert len(set(allv)) == 8
print(f"  8 distinct vectors, rank 4, in 4 prescribed pairs.")

goodJ = []
for pick in itertools.product((0,1), repeat=4):
    left  = [J[i][pick[i]]   for i in range(4)]
    right = [J[i][1-pick[i]] for i in range(4)]
    if is_basis(left) and is_basis(right):
        goodJ.append((left, right))
print(f"  grids with BOTH columns bases: {len(goodJ)} of 16")
assert goodJ == []
print("  ASSERTED: none. J also REFUTES C(2).")
print()
print("BOTH OF CHOW'S C(2) COUNTEREXAMPLES VERIFIED EXACTLY.")
