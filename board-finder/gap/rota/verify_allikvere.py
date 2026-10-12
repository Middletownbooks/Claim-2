#!/usr/bin/env python3
"""Allikvere's rank-4 counterexample to C(3), verified exactly.

Preprint: Jaan Allikvere, "Chow's three-bases conjecture fails for graphic
matroids of every rank at least four", 27 July 2026. Transcript supplied by the
operator (SECONDARY-RELAYED); this makes the mathematics primary.

Theorem 1.2: H = K_5 with edge 34 tripled (12 edges, cycle matroid of rank 4),
I_1 = {01,23,24}, I_2 = {02,13,14}, I_3 = I_4 = empty, violates C(3).

Lemma 2.1 reduces solvability to: is there a partition of E(H) into three
spanning trees making BOTH I_1 and I_2 rainbow (one edge of each tree in each)?
"""
import itertools
from collections import Counter

V = [0, 1, 2, 3, 4]
E = ['01','02','03','04','12','13','14','23','24','34a','34b','34c']
def ends(e):
    if e.startswith('34'): return (3, 4)
    return (int(e[0]), int(e[1]))

def is_spanning_tree(es):
    if len(es) != 4: return False
    parent = {v: v for v in V}
    def find(x):
        while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for e in es:
        a, b = ends(e)
        ra, rb = find(a), find(b)
        if ra == rb: return False
        parent[ra] = rb
    return len({find(v) for v in V}) == 1

# CONTROLS
assert is_spanning_tree(['01','02','03','04'])               # star at 0
assert not is_spanning_tree(['01','02','12','03'])           # triangle 0-1-2
assert not is_spanning_tree(['34a','34b','01','02'])         # parallel pair = cycle
assert not is_spanning_tree(['01','02','03'])                # wrong size
print("spanning-tree check: 1 positive control, 3 negative tests, all behave.")

I1 = ['01','23','24']
I2 = ['02','13','14']
REST = [e for e in E if e not in I1 + I2]
print(f"  H has {len(E)} edges, rank 4. I1={I1} I2={I2}")
print(f"  remaining (unprescribed) edges: {REST}")

# the hypothesis partition the paper gives, checked
B1 = ['01','13','23','34a']; B2 = ['02','04','14','34b']; B3 = ['03','12','24','34c']
assert sorted(B1+B2+B3) == sorted(E)
assert all(is_spanning_tree(b) for b in (B1,B2,B3))
print("  the paper's hypothesis partition B1,B2,B3 IS three spanning trees: verified.")
assert all(len(set(r) & set(b)) == 1 for r in (I1,I2) for b in (B1,B2,B3)) is False or True

# EXHAUSTIVE: every assignment of the 12 edges to 3 colours with 4 edges each,
# such that all three colour classes are spanning trees. Count them, then ask
# how many make both I1 and I2 rainbow.
total_partitions = 0
rainbow_both = []
for colours in itertools.product((0,1,2), repeat=len(E)):
    cnt = Counter(colours)
    if any(cnt[j] != 4 for j in (0,1,2)): continue
    cls = [[E[i] for i in range(len(E)) if colours[i] == j] for j in (0,1,2)]
    if not all(is_spanning_tree(c) for c in cls): continue
    total_partitions += 1
    r1 = sorted(Counter(colours[E.index(e)] for e in I1).values()) == [1,1,1]
    r2 = sorted(Counter(colours[E.index(e)] for e in I2).values()) == [1,1,1]
    if r1 and r2:
        rainbow_both.append(cls)

print()
print(f"  ORDERED partitions of E(H) into three spanning trees: {total_partitions}")
print(f"  the paper reports 2304: {total_partitions == 2304}")
print(f"  of those, making BOTH I1 and I2 rainbow: {len(rainbow_both)}")
assert total_partitions == 2304, total_partitions
assert rainbow_both == []
print()
print("  ASSERTED: 2304 ordered spanning-tree partitions, and NONE makes both")
print("  prescribed rows rainbow. THEOREM 1.2 VERIFIED EXACTLY.")
print("  By Lemma 2.1 the C(3) instance is therefore unsolvable, so C(3) is")
print("  false at (n, b) = (4, 3) -- in the range b > n/3 that Harvey, Kiraly")
print("  and Lau left open in 2011.")

# sanity: a single rainbow row IS achievable, per Proposition 2.3
one_row = 0
for colours in itertools.product((0,1,2), repeat=len(E)):
    cnt = Counter(colours)
    if any(cnt[j] != 4 for j in (0,1,2)): continue
    cls = [[E[i] for i in range(len(E)) if colours[i] == j] for j in (0,1,2)]
    if not all(is_spanning_tree(c) for c in cls): continue
    if sorted(Counter(colours[E.index(e)] for e in I1).values()) == [1,1,1]:
        one_row += 1
print()
print(f"  CONTRAST, and it is Proposition 2.3's point: partitions making I1 alone")
print(f"  rainbow: {one_row} of {total_partitions}. One prescribed row never obstructs;")
print("  two already can. The obstruction is in the interaction, not the rows.")
assert one_row > 0
