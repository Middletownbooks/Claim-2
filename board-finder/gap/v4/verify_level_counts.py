#!/usr/bin/env python3
"""Can the relayed (7,7) level counts be reconstructed locally?

The whole cost picture for K7,11 -- mine and theirs -- is computed from one
relayed sequence, the per-level node counts of the other instance's (7,7)
enumeration:

    Theorem 7 ON  : 1, 12,  329, 25346, 615817
    Theorem 7 OFF : 1, 13,  377, 29099, 801503

Every figure downstream of it (the 4-5e8 full-tree extrapolation, the 1-3 hour
(7,7) estimate, the 3-8x speedup over Woodall, the 5-10 month (11,7) sweep) is
a function of those five numbers.  This script asks the only question that can
be asked from this side: are the SMALL terms reproducible?  Levels 1 and 2 are
small enough to enumerate exactly here, so they are checkable; levels 3 and 4
are not.

The natural reading of a "level" is: isomorphism classes of k-element subsets
of V(CO_7) under the ground-set relabelling group, kept when the antisum is
within Woodall's prefix bound for that depth (the staircase 79/56/36/21/9/3,
so 3 at k=2 and 9 at k=3).

Result: under that reading neither term reproduces, and they miss in OPPOSITE
directions -- 14 against their 13, and 280 against their 377.  No antisum
threshold whatsoever yields 13 or 377, so the mismatch cannot be repaired by
changing the bound.  CO_7 here is built by the same construction that
reproduced Woodall's published n=4 antidistances and n=5 class count; the
extension to n=7 is not validated against any published n=7 figure, so the
mismatch could be on either side.  That is the point: it cannot be settled by
relay, only by running the same code twice.

Runtime ~25 s.  Set B higher (15 works, ~90 s) to extend the 3-set scan.
"""
from itertools import permutations
from collections import deque, Counter
from math import factorial
import array
import sys

B = int(sys.argv[1]) if len(sys.argv) > 1 else 11

FAIL = []
def ck(label, got, want):
    ok = got == want
    if not ok:
        FAIL.append(label)
    print(("  ok   " if ok else "  FAIL ") + "%-58s %s" % (label, got if ok else "%s (want %s)" % (got, want)))

print(__doc__.split("\n\n")[0])
print()

# ------------------------------------------------------------------ CO_n
# Same construction as verify_pseudotight.py: vertices are cyclic orders of
# {0..n-1} rooted at 0; u ~ v when v is u with two cyclically adjacent ground
# elements transposed.
n = 7
def canon(w):
    w = list(w); k = w.index(0); return tuple(w[k:] + w[:k])

V = [(0,) + p for p in permutations(range(1, n))]
IDX = {v: i for i, v in enumerate(V)}
N = len(V)

nb = [[] for _ in range(N)]
for v in V:
    i0 = IDX[v]
    for i in range(n):
        j = (i + 1) % n
        w = list(v); w[i], w[j] = w[j], w[i]
        u = canon(w)
        if u != v:
            nb[i0].append(IDX[u])

print("1. CO_7, against Woodall's two structural facts")
ck("|V(CO_7)| = (n-1)!", N, factorial(n - 1))
ck("CO_7 is n-regular", sorted({len(x) for x in nb}), [n])

# all-pairs distance, then antidistance d(a, reverse(b))
D = []
for s in range(N):
    d = array.array('b', [-1] * N); d[s] = 0; q = deque([s])
    while q:
        x = q.popleft()
        for y in nb[x]:
            if d[y] < 0:
                d[y] = d[x] + 1; q.append(y)
    D.append(d)
RV = [IDX[canon(list(reversed(v)))] for v in V]
AD = [array.array('b', [D[a][RV[b]] for b in range(N)]) for a in range(N)]
ck("antidistance is symmetric", all(AD[a][b] == AD[b][a] for a in range(0, N, 37) for b in range(N)), True)

# ------------------------------------- the relabelling group acting on V(CO_7)
ACT = [tuple(IDX[canon(tuple(g[x] for x in v))] for v in V) for g in permutations(range(n))]
v0 = 0
print()
print("2. the group a canonical form has available")
ck("|S_7|", len(ACT), factorial(n))
ck("stabiliser of one vertex is C_7", sum(1 for a in ACT if a[v0] == v0), n)
ck("so S_7 is transitive on the 720 vertices", len({a[v0] for a in ACT}), N)
print("     -> the maximum collapse a canonical form can reach is 5040x, not the")
print("        720x the other instance quoted as its expectation; 720 is the")
print("        VERTEX COUNT, which equals |S_7|/|C_7| and is not a group order.")
print("        Their measured collapse was 20.9x: short of 720 by 34x and of")
print("        5040 by 241x.")

# ------------------------------------------------------- level 1: 2-element sets
print()
print("3. level 1 -- 2-element sets, exact orbit count at every antisum bound")
ck("orbits of S_7 on 1-element sets", len({min(a[v] for a in ACT) for v in range(N)}), 1)
pair_as = {}
for v in range(1, N):
    cf = min(tuple(sorted((a[v0], a[v]))) for a in ACT)
    pair_as[cf] = AD[v0][v]
d2 = Counter(pair_as.values())
cum2, seq2 = 0, []
for b in range(0, 10):
    cum2 += d2.get(b, 0); seq2.append(cum2)
ck("orbits of 2-SETS, cumulative by bound 0..9", seq2, [1, 2, 6, 14, 29, 48, 63, 69, 70, 70])
ck("at Woodall's k=2 prefix bound of 3", seq2[3], 14)
ck("13 is not attained at ANY bound", 13 in seq2, False)
ck("the one 2-multiset orbit sits at antisum", AD[v0][v0], 9)
print("     -> their OFF level 1 is 13.  Local count 14.  Over by one, and 13 is")
print("        not an orbit count at any threshold.")

# ------------------------- the SAME scan under the full automorphism group
# Reversal of the cyclic order is also an automorphism of CO_n and also
# preserves antidistance, so a canonical form may quotient by S_7 x <rev>,
# order 10080.  A larger group gives FEWER classes, so this is the other end
# of the admissible range -- D66 asks for every reading, not the implemented one.
print()
print("3b. the same scan under the full automorphism group S_7 x <rev>")
REV = tuple(RV)
ck("reversal is a graph automorphism",
   all(sorted(REV[y] for y in nb[x]) == sorted(nb[REV[x]]) for x in range(N)), True)
ck("reversal preserves antidistance",
   all(AD[REV[a]][REV[b]] == AD[a][b] for a in range(0, N, 31) for b in range(N)), True)
G2 = ACT + [tuple(REV[a[v]] for v in range(N)) for a in ACT]
ck("|S_7 x <rev>| distinct as maps", len(set(G2)), 2 * factorial(n))
pair2 = {}
for v in range(1, N):
    cf = min(tuple(sorted((a[v0], a[v]))) for a in G2)
    pair2[cf] = AD[v0][v]
dd = Counter(pair2.values()); cum, seqB = 0, []
for b in range(0, 10):
    cum += dd.get(b, 0); seqB.append(cum)
ck("orbits of 2-SETS, cumulative by bound 0..9", seqB, [1, 2, 5, 11, 21, 35, 48, 54, 55, 55])
ck("13 is not attained at ANY bound here either", 13 in seqB, False)
print("     -> so 13 is unreachable as an orbit count of 2-element sets under")
print("        EITHER admissible group, at EVERY antisum threshold.")

# ------------------------------------------------------- level 2: 3-element sets
print()
print("4. level 2 -- 3-element sets, exact orbit count at every antisum bound <= %d" % B)
A0 = AD[v0]
surv = {}
for i in range(1, N):
    a = A0[i]
    if a > B: continue
    Ai = AD[i]
    for j in range(i + 1, N):
        s = a + A0[j] + Ai[j]
        if s <= B:
            surv[(v0, i, j)] = s
reps = Counter(); done = set()
for S, s in surv.items():
    if S in done: continue
    for a in ACT:
        T = tuple(sorted((a[S[0]], a[S[1]], a[S[2]])))
        if T in surv: done.add(T)
    reps[s] += 1
cum3, seq3 = 0, []
for b in range(0, B + 1):
    cum3 += reps.get(b, 0); seq3.append(cum3)
print("     cumulative: " + ", ".join("b=%d:%d" % (b, c) for b, c in enumerate(seq3) if c))
ck("at Woodall's k=3 prefix bound of 9", seq3[9], 280)
ck("every 3-set orbit has ODD antisum", all(b % 2 == 1 for b in reps), True)
ck("377 is not attained at ANY bound <= %d" % B, 377 in seq3, False)
if B >= 11:
    ck("the count steps 280 -> 1710, straddling 377", (seq3[9], seq3[11]), (280, 1710))
reps2 = Counter(); done2 = set()
for S, sv in surv.items():
    if S in done2: continue
    for a in G2:
        T = tuple(sorted((a[S[0]], a[S[1]], a[S[2]])))
        if T in surv: done2.add(T)
    reps2[sv] += 1
ck("under S_7 x <rev>, orbits at bound 9", sum(v for b, v in reps2.items() if b <= 9), 158)
print("     -> their OFF level 2 is 377.  Local count 280 under S_7 and 158 under")
print("        the full automorphism group.  UNDER by 97 and by 219, i.e. the")
print("        opposite direction to level 1, so no single cause explains both.")

# ------------------------------------------------------------------ consequence
print()
print("5. what the mismatch costs")
print("   The five relayed terms are the input to every cost figure on this")
print("   target.  Under the reading above, levels are 1,2,3,.. -element sets and")
print("   a full (7,7) run needs two levels beyond the reported depth, giving the")
for lv, ratio in (("two more levels", 24.3),):
    print("     %-16s 615817 * %.1f^2 = %.2e nodes" % (lv, ratio, 615817 * ratio ** 2))
print("   Under the one re-reading that fits the SHAPE of both misses -- level 0")
print("   is the empty set, so their level k holds k-element sets and the")
print("   canonical form is far from orbit-complete (13 singletons against 1")
print("   orbit, 377 pairs against 70) -- a full run needs THREE more levels:")
print("     three more levels 615817 * 24.3^3 = %.2e nodes" % (615817 * 24.3 ** 3))
print("   a factor of %.0fx, which moves their (7,7) run from 1-3 hours to" % 24.3)
print("   12-24 hours and weakens 'the stall was a budget finding'.")
print("   NEITHER reading can be confirmed from this side.")

print()
print("FAILURES: %d" % len(FAIL) + ("" if not FAIL else " -> " + "; ".join(FAIL)))
sys.exit(1 if FAIL else 0)
