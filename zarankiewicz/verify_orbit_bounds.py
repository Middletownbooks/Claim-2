#!/usr/bin/env python3
"""None of the three checkable relayed level counts is an orbit count, at ANY threshold.

board-finder/gap/v4/verify_level_counts.py showed that the relayed (7,7) level
counts 1, 13, 377, 29099, 801503 (Theorem 7 off) do not reconstruct at levels 1
and 2 -- 14 and 280 locally against 13 and 377.  That comparison rested on
reading Woodall's prefix staircase as a condition on canonical sets, which is an
interpretation, and on a choice of threshold.

THIS SCRIPT REMOVES BOTH DEPENDENCIES.  The number of isomorphism classes of
k-element subsets of V(CO_7) with antisum at most b is a property of CO_7 alone:
no ordering convention, canonical-form choice or search order can raise it,
because every such convention DISCARDS sets and none invents them.  Computing it
at EVERY b therefore settles whether a reported figure could be an orbit count
at all, without anyone having to agree on the staircase.

    k   their term   orbit classes of k-sets, cumulative by threshold   attainable?
    2        13      1, 2, 6, 14, 29, 48, 63, 69, 70                        no
    3       377      280 (b=9), 1710 (11), 5040 (13), 9123 (15)             no
    4    29,099      69 (18), 497 (19), 3119 (20), 12484 (21), 38309 (22)   no

Three terms, three misses, each checked across every threshold.  So the relayed
level counts are not counts of isomorphism classes -- not under the relabelling
group S_7, not under the full automorphism group, not at any antisum bound.
Whatever they are, the arithmetic performed on them (growth ratios -> full-tree
size -> throughput -> months) was arithmetic on an unidentified quantity.

AND THE SIGN IS UNDETERMINED, which is the part worth being careful about.  At
the staircase values read from the paper (3, 9, 21) their terms miss by -1, +97
and +16,615; one threshold up (4, 11, 22) the same terms miss by -16, -1,333 and
-9,210.  The direction flips with the threshold, so nothing here establishes
whether their tree is larger or smaller than the tree that needs traversing.
Two earlier readings are therefore BOTH withdrawn as undetermined: the one where
an offset costs a whole level and makes the full (7,7) tree 8.8e9 nodes, and the
one where an incomplete canonical form inflates their tree and makes the sweep
cheaper.  Neither is supported.  What is established is that the sign of the
error in every cost estimate on this target is unknown from this side.

Runtime ~7 min.  Pass "fast" to skip the second group.
"""
from itertools import permutations
from collections import deque, Counter
from math import factorial
import array, sys, time

FAST = len(sys.argv) > 1 and sys.argv[1] == "fast"
FAIL = []
def ck(label, got, want):
    ok = got == want
    if not ok: FAIL.append(label)
    print(("  ok   " if ok else "  FAIL ") + "%-54s %s" % (label, got if ok else "%s (want %s)" % (got, want)))

THEIRS = {1: 13, 2: 377, 3: 29099, 4: 801503}      # Theorem 7 OFF, as relayed
n, BOUND = 7, 22
t0 = time.time()

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
        if u != v: nb[i0].append(IDX[u])
D = []
for s in range(N):
    d = array.array('b', [-1] * N); d[s] = 0; q = deque([s])
    while q:
        x = q.popleft()
        for y in nb[x]:
            if d[y] < 0: d[y] = d[x] + 1; q.append(y)
    D.append(d)
RV = [IDX[canon(list(reversed(v)))] for v in V]
AD = [array.array('b', [D[a][RV[b]] for b in range(N)]) for a in range(N)]
S7 = [tuple(IDX[canon(tuple(g[x] for x in v))] for v in V) for g in permutations(range(n))]
BIG = S7 + [tuple(RV[a[v]] for v in range(N)) for a in S7]

print("1. CO_7 and the two groups that act on its subsets")
ck("|V(CO_7)|", N, factorial(n - 1))
ck("CO_7 is n-regular", sorted({len(x) for x in nb}), [n])
ck("|S_7|", len(set(S7)), factorial(n))
ck("|S_7 x <rev>|", len(set(BIG)), 2 * factorial(n))
print("     reversal is checked to be an automorphism preserving antidistance in")
print("     board-finder/gap/v4/verify_level_counts.py sec 3b; not repeated here.")

# ------------------------------------------------- level 3: 4-element sets
print()
print("2. every 4-element subset of V(CO_7) with antisum <= %d, up to isomorphism" % BOUND)
A0 = AD[0]
surv = {}
for i in range(1, N):
    ai = A0[i]
    if ai > BOUND: continue
    Ai = AD[i]
    for j in range(i + 1, N):
        s2 = ai + A0[j] + Ai[j]
        if s2 > BOUND: continue
        Aj = AD[j]
        for k in range(j + 1, N):
            s3 = s2 + A0[k] + Ai[k] + Aj[k]
            if s3 <= BOUND: surv[(0, i, j, k)] = s3
# every orbit has a representative containing vertex 0, since S_7 is transitive
ck("4-sets containing v0 with antisum <= %d" % BOUND, len(surv), 1058701)
ck("  ... and with antisum <= 21", sum(1 for s in surv.values() if s <= 21), 344568)

def cumulative(G, keep):
    """Cumulative orbit count by antisum, over the survivors with antisum <= keep."""
    sub = {S: s for S, s in surv.items() if s <= keep}
    reps = Counter(); done = set()
    for S, s in sub.items():
        if S in done: continue
        a0, a1, a2, a3 = S
        for a in G:
            T = tuple(sorted((a[a0], a[a1], a[a2], a[a3])))
            if T in sub: done.add(T)
        reps[s] += 1
    cum, seq = 0, []
    for b in range(keep + 1):
        cum += reps.get(b, 0); seq.append(cum)
    return seq

seq = cumulative(S7, BOUND)
print("   under S_7:  " + ", ".join("b=%d:%d" % (b, c) for b, c in enumerate(seq) if c))
ck("classes at bounds 18..22 under S_7", seq[18:23], [69, 497, 3119, 12484, 38309])
if not FAST:
    seqB = cumulative(BIG, 21)
    print("   under S_7 x <rev>: " + ", ".join("b=%d:%d" % (b, c) for b, c in enumerate(seqB) if c))
    ck("classes at bounds 18..21 under the larger group", seqB[18:22], [60, 282, 1648, 6387])

# ------------------------------------------------------------ the bound-free test
print()
print("3. is their level 3 an orbit count at ANY threshold?")
ck("29099 is not in the cumulative sequence", THEIRS[3] in seq, False)
lo = max(c for c in seq if c < THEIRS[3]); hi = min(c for c in seq if c > THEIRS[3])
ck("it falls strictly inside one step of the ladder", (lo, hi), (12484, 38309))
print("   %d sits between the counts at bound 21 and bound 22, so there is no" % THEIRS[3])
print("   threshold at which it is the number of isomorphism classes of 4-element")
print("   sets.  The same holds at k=2 (13 against 1,2,6,14,..) and k=3 (377")
print("   between 280 and 1710), both from the earlier script.  THREE FOR THREE.")

print()
print("4. the sign of the error, which is what a cost estimate needs")
print("   threshold read from the paper   miss at k=2,3,4:  %+d, %+d, %+d"
      % (THEIRS[1] - 14, THEIRS[2] - 280, THEIRS[3] - seq[21]))
print("   one threshold higher            miss at k=2,3,4:  %+d, %+d, %+d"
      % (THEIRS[1] - 29, THEIRS[2] - 1710, THEIRS[3] - seq[22]))
print("   The direction flips with the threshold, so whether their tree is larger")
print("   or smaller than the one that needs traversing is UNDETERMINED here.")
print("   Both directional readings are withdrawn; see the module docstring.")

print()
print("elapsed %.0fs" % (time.time() - t0))
print("FAILURES: %d" % len(FAIL) + ("" if not FAIL else " -> " + "; ".join(FAIL)))
sys.exit(1 if FAIL else 0)
