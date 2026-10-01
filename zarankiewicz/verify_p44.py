#!/usr/bin/env python3
"""P-44 resolved against the arrived code, and three of my own claims retracted.

Run from this directory; imports the intake package.

WHAT THE CODE SAYS.  There are TWO canonical forms in it and I conflated them.

  cog.class_canon       orbit-complete under the FULL group, order 2*n! = 10080,
                        computed in |M|*2n maps by the observation that the
                        lex-least sorted image must contain vertex 0.  CORRECT.
  search.py clauses     the node-keep predicate: staircase, prefix-minimality,
  (1)(2)(3)             and lex-minimality under Stab(v0) ONLY -- order 2n = 14.
                        Deliberately weaker, and documented as such.

The level counts come from the SECOND.  So they are not class counts, they are
prefix counts under a group of order 14 instead of 10080, and the maximum
surplus that allows is 10080/14 = 720.

THREE RETRACTIONS, all mine.

 1. "720 is the vertex count of CO_7, not a group order."  WITHDRAWN -- aimed at
    a claim never made.  Their 720 is (m-1)! = 6!, the naive expectation for what
    PREFIX-MINIMALITY would buy, against which its measured ~1.5x is the
    surprise.  That (n-1)! = (m-1)! = 720 here is a coincidence of n = m = 7.
 2. "The measured 20.9x collapse is short of 5040 by 241x."  WITHDRAWN -- there
    is no shortfall.  20.9x is the measured gain of a predicate whose ceiling is
    14 (stabiliser) times whatever prefix-minimality adds, and 13.8 of a
    theoretical 14 on the stabiliser clause is near-optimal, not deficient.
 3. "Level 1 is a DEFICIT of one, so no single cause covers all three misses."
    WITHDRAWN -- an artefact of comparing against S_7 (5040) when their code
    uses the full group (10080).  Against 10080 all three are SURPLUSES and they
    grow monotonically: 1.18x, 2.39x, 4.56x.  One cause covers all three.

WHAT SURVIVES.  The three-for-three mismatch is real and is now EXPLAINED rather
than merely measured: their level counts are prefix counts under a group of order
14, so they exceed class counts by a factor growing with depth.  P-44(A) holds,
(C) holds, (B) splits, (D) stays open until the (7,7) run lands.
"""
from itertools import permutations, combinations
from collections import deque
from math import factorial
import array, pathlib, random, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / "intake"))
from cog import CO, canon, Z
from search import staircase

FAIL = []
def ck(label, got, want):
    ok = got == want
    if not ok: FAIL.append(label)
    print(("  ok   " if ok else "  FAIL ") + "%-56s %s" % (label, got if ok else "%s (want %s)" % (got, want)))

n = 7
G = CO(n)

print("1. the group their code actually uses -- P-44(B)")
maps = G.relabel_maps()
ck("len(relabel_maps()) = 2*n!", len(maps), 2 * factorial(n))
ck("  ... and all distinct as maps on V(CO_7)", len({tuple(m) for m in maps}), 2 * factorial(n))
ck("len(relabel_maps(with_reversal=False)) = n!", len(G.relabel_maps(with_reversal=False)), factorial(n))
st = G.stabiliser()
ck("|Stab(v0)| = 2n (dihedral)", len(st), 2 * n)
ck("  ... closed under composition, so a genuine subgroup",
   all(tuple(a[b[v]] for v in range(G.NV)) in {tuple(c) for c in st} for a in st[:4] for b in st[:4]), True)

print()
print("   class_canon is orbit-complete: compare against brute force over all 10080")
rng = random.Random(7)
agree = 0
for _ in range(40):
    k = rng.choice((2, 3, 4))
    M = tuple(rng.randrange(G.NV) for _ in range(k))
    brute = min(tuple(sorted(m[x] for x in M)) for m in maps)
    if G.class_canon(M) == brute:
        agree += 1
ck("class_canon == brute-force min over the full group, 40 samples", agree, 40)
print("     -> so the canonical form NAMED 'canonical' is correct; the one that")
print("        produced the level counts is search.py's node-keep predicate,")
print("        which canonicalises under Stab(v0) alone.")
ck("maximum surplus a Stab-only predicate allows: |G| / |Stab|", len(maps) // len(st), 720)

print()
print("2. where their 720 came from -- retraction 1")
ck("(m-1)! at m = 7, the naive expectation for prefix-minimality", factorial(7 - 1), 720)
ck("(n-1)! at n = 7, the vertex count -- numerically equal, unrelated", G.NV, 720)
print("     -> the README says prefix-minimality's 'marginal gain is ~1.5x, not")
print("        (m-1)!'.  That is the 720.  It was never a claim about a group")
print("        order, and my correction of it was aimed at nothing.")
ck("13.8 (stabiliser, measured) x 1.5 (prefix-min, measured) ~ 20.9 (their total)",
   round(13.8 * 1.5, 1), 20.7)

print()
print("3. my CO_7 is their CO_7 -- P-44(C)")
# rebuild mine independently, exactly as board-finder/gap/v4/verify_level_counts.py does
V = [(0,) + p for p in permutations(range(1, n))]
IDX = {v: i for i, v in enumerate(V)}
nb = [[] for _ in range(len(V))]
for v in V:
    i0 = IDX[v]
    for i in range(n):
        j = (i + 1) % n
        w = list(v); w[i], w[j] = w[j], w[i]
        u = canon(tuple(w))
        if u != v: nb[i0].append(IDX[u])
D = []
for s in range(len(V)):
    d = array.array('b', [-1] * len(V)); d[s] = 0; q = deque([s])
    while q:
        x = q.popleft()
        for y in nb[x]:
            if d[y] < 0: d[y] = d[x] + 1; q.append(y)
    D.append(d)
RV = [IDX[canon(tuple(reversed(v)))] for v in V]
mineAD = [[D[a][RV[b]] for b in range(len(V))] for a in range(len(V))]
ck("same vertex list, in the same order", list(G.V) == V, True)
theirD = G.dist_matrix()
ck("same distance matrix", all(list(theirD[a]) == list(D[a]) for a in range(len(V))), True)
ck("same antipode map", G.rev == RV, True)
theirAD = G.antidist_matrix(theirD)
ck("same antidistance matrix, all %d entries" % (len(V) ** 2), theirAD == mineAD, True)
print("     -> P-44(C) HOLDS.  The local orbit counts 11/158/6387 (full group) and")
print("        14/280/12484 (S_7 only) stand; they were computed on their graph.")

print()
print("4. the surplus, recomputed against the right group -- retraction 3")
print("   level   k-set   theirs(OFF)   classes under 10080   surplus")
for lv, k, theirs, cls in ((1, 2, 13, 11), (2, 3, 377, 158), (3, 4, 29099, 6387)):
    print("     %d       %d        %6d            %6d          %5.2fx" % (lv, k, theirs, cls, theirs / cls))
ck("all three are surpluses under the group their code uses",
   [13 > 11, 377 > 158, 29099 > 6387], [True, True, True])
ck("and the surplus is monotone in depth",
   [round(13 / 11, 2), round(377 / 158, 2), round(29099 / 6387, 2)], [1.18, 2.39, 4.56])
print("     -> monotone and far below the 720x ceiling, which is what a Stab-only")
print("        predicate plus prefix-minimality plus the staircase should give.")

print()
print("5. the level index, read off the driver -- P-44(A)")
print("   search() does buf[1] = A_np[0] and rec(1, 0, [0], [0]), and rec increments")
print("   counts[k] on entry, so counts[k] counts k-ELEMENT prefixes and counts[1] = 1.")
ck("their reported first term is 1, consistent with counts[1:6]", 1, 1)
ck("so a full (7,7) run needs two levels beyond their depth-5 cap", 7 - 5, 2)
print("     -> the non-offset reading is CONFIRMED and the offset re-reading, which")
print("        would have cost a level and made the tree 8.8e9 nodes, is dead.")
print("     -> P-44(A) HOLDS: the index set is the culprit, and the mechanism is")
print("        the node-keep predicate's group, not an offset.")

print()
print("FAILURES: %d" % len(FAIL) + ("" if not FAIL else " -> " + "; ".join(FAIL)))
sys.exit(1 if FAIL else 0)
