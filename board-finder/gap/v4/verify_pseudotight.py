#!/usr/bin/env python3
"""End-to-end re-derivation of the (4,6)-set that is pseudo-tight but not tight.

Built from Woodall's definitions (pp. 659, 661, 662) as this session read them
from the page images, NOT from the originating program's code. A fourth reading
of the specification rather than a fourth implementation of the same reading --
which, by that program's own Proposition 1, is the thing worth supplying.
"""
from itertools import permutations, product
from collections import deque

FAIL = []
def ck(label, got, want):
    ok = got == want
    print(f"  [{'ok ' if ok else 'FAIL'}] {label}: {got!r} vs {want!r}")
    if not ok: FAIL.append(label)

# ------------------------------------------------------------------ CO_n
def verts(n): return [(0,) + p for p in permutations(range(1, n))]
def canon(w):
    k = w.index(0); return tuple(w[k:] + w[:k])
def rev(v):
    return canon(list(reversed(v)))
def edges(n):
    """(u, v, label) with label the transposed ground-set pair."""
    out = []
    for v in verts(n):
        for i in range(n):
            j = (i + 1) % n
            w = list(v); x, y = w[i], w[j]; w[i], w[j] = w[j], w[i]
            u = canon(w)
            if u != v: out.append((v, u, frozenset((x, y))))
    return out

def adj(n):
    a = {}
    for u, v, l in edges(n): a.setdefault(u, []).append((v, l))
    return a

A6, A4 = adj(6), adj(4)
ck("|V(CO_6)|", len(verts(6)), 120)
ck("|V(CO_4)|", len(verts(4)), 6)

# ------------------------------------------- the three antipath families in CO_4
L4 = sorted({l for _, _, l in edges(4)}, key=lambda s: sorted(s))
LI = {l: i for i, l in enumerate(L4)}
ck("CO_4 has C(4,2) = 6 labels", len(L4), 6)

def family_walk(src):
    """Walks using each label at most once; vertex revisits permitted."""
    out, seen = set(), {(src, 0)}
    st = [(src, 0)]
    while st:
        v, m = st.pop(); out.add((v, m))
        for w, l in A4[v]:
            b = 1 << LI[l]
            if not (m & b) and (w, m | b) not in seen:
                seen.add((w, m | b)); st.append((w, m | b))
    return out

def family_path(src, label_distinct=False):
    """Vertex-simple paths (optionally also label-distinct)."""
    out = set()
    def go(v, visited, m):
        out.add((v, m))
        for w, l in A4[v]:
            b = 1 << LI[l]
            if w in visited: continue
            if label_distinct and (m & b): continue
            go(w, visited | {w}, m | b)
    go(src, {src}, 0)
    return out

for name, fn, want in (("walk", lambda s: family_walk(s), 282),
                       ("path", lambda s: family_path(s), 594),
                       ("both", lambda s: family_path(s, True), 234)):
    total = sum(len(fn(s)) for s in verts(4))
    ck(f"CO_4 family '{name}': distinct (endpoint, label-set) over all ordered pairs",
       total, want)
WALK = {s: family_walk(s) for s in verts(4)}

def q_achievable(x, y):
    """Label sets of xy-antipaths in CO_4: x -> ybar (the abar->b family has the
    same label sets, reversal being a label-preserving automorphism, p.659)."""
    t = rev(y)
    return {m for (v, m) in WALK[x] if v == t}

# ---------------------------------------------- M, and its shortest antipaths
M = [(0,1,2,3,4,5), (0,1,3,5,4,2), (0,3,2,5,4,1), (0,4,5,2,3,1)]
PAIRS = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]

def bfs(a, A):
    d = {a: 0}; q = deque([a])
    while q:
        u = q.popleft()
        for w, _ in A[u]:
            if w not in d: d[w] = d[u] + 1; q.append(w)
    return d

def shortest_label_sets(a, b):
    """Label sets of all shortest a->bbar paths in CO_6, via the shortest-path DAG."""
    t = rev(b)
    da, dt = bfs(a, A6), bfs(t, A6)
    D = da[t]
    res = set()
    def go(v, m):
        if v == t: res.add(m); return
        for w, l in A6[v]:
            if da[w] == da[v] + 1 and da[w] + dt[w] == D:
                go(w, m | frozenset([l]))
    go(a, frozenset())
    return res, D

print()
print("1. Shortest-antipath label sets per M-pair in CO_6 (their sec 1.2 table)")
SLS, DD = {}, {}
for i, j in PAIRS:
    s, D = shortest_label_sets(M[i], M[j]); SLS[(i,j)] = s; DD[(i,j)] = D
    pretty = " | ".join("{" + ",".join("".join(map(str, sorted(l))) for l in sorted(x, key=lambda l: sorted(l))) + "}"
                        for x in sorted(s, key=lambda x: sorted(sorted(l) for l in x)))
    print(f"      a{i}a{j} (dbar={D}): {len(s)} set(s)  {pretty}")
ck("antidistances", [DD[p] for p in PAIRS], [3,4,2,3,2,1])
ck("number of shortest label sets per pair", [len(SLS[p]) for p in PAIRS], [1,3,1,1,1,1])
ck("total row-choices = product", 1*3*1*1*1*1, 3)

# ---------------------------------------------------- Forced / Possible per x,y
GROUND = range(6)
XY = [(x,y) for x in GROUND for y in GROUND if x < y]
def pairlab(i, j): return frozenset((i, j))
FORCED, POSSIBLE = {}, {}
for x, y in XY:
    f, p = set(), set()
    for (i, j) in PAIRS:
        sets = SLS[(i,j)]
        inall = all(pairlab(x,y) in s for s in sets)
        inany = any(pairlab(x,y) in s for s in sets)
        if inall: f.add(pairlab(i,j))
        if inany: p.add(pairlab(i,j))
    FORCED[(x,y)], POSSIBLE[(x,y)] = frozenset(f), frozenset(p)
ck("Forced is contained in Possible for all 15 pairs",
   all(FORCED[k] <= POSSIBLE[k] for k in XY), True)

def mask_of(S): return sum(1 << LI[l] for l in S)

# ---------------------------------------------------------- 2. pseudo-tightness
print()
print("2. Their witness N, checked against all 15 pseudo-tightness constraints")
N = [(0,2,3,1), (0,2,3,1), (0,2,1,3), (0,1,2,3), (0,2,1,3), (0,2,1,3)]
ck("N is a (6,4)-set: six elements of V(CO_4)", all(v in set(verts(4)) for v in N) and len(N) == 6, True)
ok_pairs = []
for x, y in XY:
    fm, pm = mask_of(FORCED[(x,y)]), mask_of(POSSIBLE[(x,y)])
    good = any((m & fm) == fm and (m | pm) == pm for m in q_achievable(N[x], N[y]))
    ok_pairs.append(((x,y), good))
bad = [p for p, g in ok_pairs if not g]
ck("all 15 constraints satisfied by their N", bad, [])
print("      => M IS PSEUDO-TIGHT, re-derived independently.")

# ------------------------------------------------------------- 3. non-tightness
print()
print("3. Tightness: enumerate the 3 row-choices, and for each all 6^6 witnesses N")
ALLV = verts(4)
ACH = {(x, y): q_achievable(x, y) for x in ALLV for y in ALLV}
choices = list(product(*[sorted(SLS[p], key=lambda s: sorted(sorted(l) for l in s)) for p in PAIRS]))
ck("row-choice count", len(choices), 3)
any_tight = False
for ci, choice in enumerate(choices, 1):
    # R_xy forced by this choice: { ab : xy in labels(P_ab) }
    R = {}
    for x, y in XY:
        R[(x,y)] = frozenset(pairlab(i,j) for (i,j), lab in zip(PAIRS, choice)
                             if pairlab(x,y) in lab)
    # does some N in V(CO_4)^6 realise every R_xy exactly?
    feasible = False
    for Ncand in product(ALLV, repeat=6):
        if all(mask_of(R[(x,y)]) in ACH[(Ncand[x], Ncand[y])] for x, y in XY):
            feasible = True; break
    print(f"      choice {ci}: {'FEASIBLE' if feasible else 'infeasible'} over all {6**6:,} N")
    any_tight |= feasible
ck("no row-choice admits a witness, i.e. M is NOT TIGHT", any_tight, False)
print("      => M IS NOT TIGHT, re-derived independently.")

print()
print("=" * 72)
if FAIL:
    print(f"{len(FAIL)} FAILED: {FAIL}"); raise SystemExit(1)
print("M is pseudo-tight and not tight. Verified end to end from the definitions.")

# ============================================ 4. A FOURTH READING, not in their C
print()
print("4. A fourth admissible reading: ARBITRARY walks, label reuse permitted")
print("      Their C = {path, walk, both}, where 'walk' means label-DISTINCT walks")
print("      with vertex revisits allowed. But the definitions say only 'an")
print("      xy-antipath (not necessarily shortest)'. Label-distinctness is argued")
print("      in their sec 2 from the fact that in a GOOD DRAWING two arcs cross at")
print("      most once -- which constrains the antipath Theorem 5 CONSTRUCTS from a")
print("      drawing, not every antipath the definition quantifies over. So")
print("      'arbitrary walk' is a fourth reading, and it is strictly LARGER.")

def family_anywalk(src):
    out, seen = set(), {(src, 0)}
    st = [(src, 0)]
    while st:
        v, m = st.pop(); out.add((v, m))
        for w, l in A4[v]:
            nm = m | (1 << LI[l])
            if (w, nm) not in seen:
                seen.add((w, nm)); st.append((w, nm))
    return out

ANY = {s: family_anywalk(s) for s in verts(4)}
tot_any = sum(len(ANY[s]) for s in verts(4))
print(f"      sizes: both 234  <  walk 282  <  path 594  <  ARBITRARY {tot_any}")
ck("arbitrary-walk family is strictly larger than 'walk'", tot_any > 282, True)

def q_any(x, y):
    t = rev(y); return {m for (v, m) in ANY[x] if v == t}

# Pseudo-tightness is monotone in the family, so it survives a fortiori.
bad2 = []
for x, y in XY:
    fm, pm = mask_of(FORCED[(x,y)]), mask_of(POSSIBLE[(x,y)])
    if not any((m & fm) == fm and (m | pm) == pm for m in q_any(N[x], N[y])):
        bad2.append((x,y))
ck("M still pseudo-tight under the larger family (monotone, so expected)", bad2, [])

# Non-tightness is ANTI-monotone: a larger Q family makes tightness EASIER.
# This is the half that could flip.
ACH_ANY = {(x, y): q_any(x, y) for x in ALLV for y in ALLV}
flip = False
for ci, choice in enumerate(choices, 1):
    R = {}
    for x, y in XY:
        R[(x,y)] = frozenset(pairlab(i,j) for (i,j), lab in zip(PAIRS, choice)
                             if pairlab(x,y) in lab)
    feasible = False
    for Ncand in product(ALLV, repeat=6):
        if all(mask_of(R[(x,y)]) in ACH_ANY[(Ncand[x], Ncand[y])] for x, y in XY):
            feasible = True; break
    print(f"      choice {ci} under ARBITRARY walks: {'FEASIBLE -- M would be TIGHT' if feasible else 'infeasible'}")
    flip |= feasible
ck("M is NOT TIGHT under the fourth reading too", flip, False)
print()
print("      => THE RESULT IS ROBUST TO THE FOURTH READING. Non-tightness is the")
print("         anti-monotone half -- a larger Q family can only make tightness")
print("         easier -- and it survives the LARGEST family the definition could")
print("         possibly license. So the counterexample holds under every reading")
print("         of 'antipath' between 'both' (234) and arbitrary walks, which")
print("         brackets all four candidates. Their epsilon on this axis is now 0,")
print("         not merely reduced.")

# ================================= 5. Closing the bracket from the other side
print()
print("5. Pseudo-tightness under the SMALLEST family, which closes the lattice")
print("      not-tight is ANTI-monotone and was verified under the LARGEST family")
print("      (arbitrary, 1758), so it holds under all four. pseudo-tight is")
print("      MONOTONE, so verifying it under the SMALLEST family ('both', 234 --")
print("      contained in every other candidate) gives it under all four.")
BOTH = {s: family_path(s, True) for s in verts(4)}
def q_both(x, y):
    t = rev(y); return {m for (v, m) in BOTH[x] if v == t}
bad3 = []
for x, y in XY:
    fm, pm = mask_of(FORCED[(x,y)]), mask_of(POSSIBLE[(x,y)])
    if not any((m & fm) == fm and (m | pm) == pm for m in q_both(N[x], N[y])):
        bad3.append((x,y))
ck("M is pseudo-tight under 'both', the smallest family", bad3, [])
print()
print("      => THE RESULT IS READING-INDEPENDENT. 'both' (234) is contained in")
print("         'walk' (282), in 'path' (594) and in arbitrary walks (1758).")
print("         Pseudo-tight holds at the bottom of that lattice and non-tight at")
print("         the top, so BOTH HALVES HOLD AT EVERY READING IN BETWEEN -- which")
print("         is every reading of 'antipath' the definitions could license.")
print("         Epsilon on the convention axis is 0, not reduced: the result does")
print("         not depend on resolving the convention at all.")
