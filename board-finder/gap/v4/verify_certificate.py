#!/usr/bin/env python3
"""Independent re-derivation of the (4,6)-set certificate, and of the claim
that Woodall's Theorem 7 is unavailable at m = 11.

CO_n and the antidistance are built here from the paper's own definitions
(pp. 659, 661), not from the originating program's code. This is deliberately a
fourth reading of the specification rather than a fourth implementation of the
same reading.
"""
from itertools import permutations
from collections import deque

FAIL = []
def ck(label, got, want):
    ok = got == want
    print(f"  [{'ok ' if ok else 'FAIL'}] {label}: {got!r} vs {want!r}")
    if not ok: FAIL.append(label)

# ---------------------------------------------------------------- CO_n, p.659
# "Its vertices are the (n-1)! different cyclic orderings of a set V_n of n
#  elements, and two such orderings are adjacent if one can be obtained from the
#  other by transposing two adjacent elements."  Cyclic, so 0 is pinned first.
def verts(n):
    return [(0,) + p for p in permutations(range(1, n))]

def neighbours(v):
    n = len(v)
    out = set()
    for i in range(n):                       # transpose positions i, i+1 cyclically
        j = (i + 1) % n
        w = list(v); w[i], w[j] = w[j], w[i]
        k = w.index(0)                       # re-root at 0
        out.add(tuple(w[k:] + w[:k]))
    out.discard(v)
    return out

def rev(v):
    """abar: the reverse ordering, re-rooted at 0 (p.659's worked example)."""
    w = list(reversed(v)); k = w.index(0)
    return tuple(w[k:] + w[:k])

print("1. CO_n built from p.659, checked against the paper's own numbers")
for n in (4, 6, 7):
    V = verts(n)
    ck(f"|V(CO_{n})| = {n-1}!", len(V), len(list(permutations(range(1, n)))))
    deg = {len(neighbours(v)) for v in V}
    ck(f"CO_{n} is {n}-regular", deg, {n})
# p.659's worked example of the reverse map
ck("p.659: a = 0354162 has abar = 0261453",
   rev((0,3,5,4,1,6,2)), (0,2,6,1,4,5,3))
print()

def bfs(n, src):
    dist = {src: 0}; q = deque([src])
    while q:
        u = q.popleft()
        for w in neighbours(u):
            if w not in dist:
                dist[w] = dist[u] + 1; q.append(w)
    return dist

print("2. Theorem 3(c): d(a, abar) = Z(n), the Appendix's conclusion, checked directly")
def Z(n): return (n // 2) * ((n - 1) // 2)
for n in (4, 5, 6, 7):
    V = verts(n)
    a = V[0]
    d = bfs(n, a)
    ck(f"d(a, abar) = Z({n}) in CO_{n}", d[rev(a)], Z(n))
    # and it is the eccentricity -- "abar is the unique vertex at maximum distance"
    mx = max(d.values())
    far = [v for v in V if d[v] == mx]
    ck(f"  ...and abar is the UNIQUE farthest vertex in CO_{n}", (mx, far), (Z(n), [rev(a)]))
print()

# ---------------------------------------------------------- the (4,6)-set, p.661
# "The antidistance dbar(a,b) between two vertices a and b is the distance
#  d(a, bbar) ... the sum of all C(m,2) antidistances ... is the antisum."
print("3. The relayed (4,6)-set: antidistances and antisum, re-derived")
M = [(0,1,2,3,4,5), (0,1,3,5,4,2), (0,3,2,5,4,1), (0,4,5,2,3,1)]
ck("all four are vertices of CO_6", all(m in set(verts(6)) for m in M), True)
ck("the four are distinct", len(set(M)), 4)

D6 = {m: bfs(6, m) for m in M}
pairs = [(0,1), (0,2), (0,3), (1,2), (1,3), (2,3)]
anti = [D6[M[i]][rev(M[j])] for i, j in pairs]
print(f"      pair order (a0a1, a0a2, a0a3, a1a2, a1a3, a2a3)")
ck("antidistances", anti, [3, 4, 2, 3, 2, 1])
ck("antisum", sum(anti), 15)
# dbar is symmetric: d(a, bbar) = d(abar, b)
ck("antidistance is symmetric, d(a,bbar) = d(abar,b)",
   all(D6[M[i]][rev(M[j])] == bfs(6, rev(M[i]))[M[j]] for i, j in pairs), True)
ck("antisum 15 exceeds Z(4)Z(6) = 12", (Z(4)*Z(6), sum(anti) > Z(4)*Z(6)), (12, True))
print("      => the certificate's arithmetic half checks, independently of their code.")
print("      The pseudo-tight / not-tight half needs the Q_xy system, which is")
print("      in the writeup still to arrive. Count stays at two until then.")
print()

# ------------------------------------------------- Theorem 7 availability, p.665
print("4. Their claim: Theorem 7 is UNAVAILABLE at m = 11. Checked against p.665.")
# "Let m and n be odd integers and m' < n an even integer such that every
#  (m'+1, n)-set has antisum at least Z(m'+1)Z(n) and every (m - m', n)-set has
#  antisum at least Z(m-m')Z(n)."
# Established antisum lower bounds at n = 7, from sections 5 and their sessions:
established = {
    3: ("Z(3)Z(7) = 9",   True,  "Theorem 4(a)"),
    5: ("Z(5)Z(7) = 36",  True,  "program 2: every (5,7)-set >= 36"),
    7: ("Z(7)Z(7) = 81",  False, "program 4: 13,448 sets sit at 79"),
    9: ("Z(9)Z(7) = 144", False, "their session 1: (9,7)-sets at 140"),
}
def theorem7_applies(m, n=7):
    rows = []
    for mp in range(2, n, 2):                  # m' even, m' < n
        need = [mp + 1, m - mp]
        ok = all(established.get(k, (None, False, "unknown"))[1] for k in need)
        rows.append((mp, need, ok))
    return rows

for m in (7, 9, 11):
    rows = theorem7_applies(m)
    any_ok = any(ok for _, _, ok in rows)
    print(f"      m = {m}:")
    for mp, need, ok in rows:
        why = ", ".join(f"({k},7)>={established.get(k,('?',))[0]}"
                        f"{'' if established.get(k,(0,False))[1] else '  FAILS'}"
                        for k in need)
        print(f"        m'={mp}: needs {why}   -> {'applies' if ok else 'no'}")
    print(f"        => Theorem 7 {'IS' if any_ok else 'is NOT'} available at m = {m}")

ck("available at m = 7, as the paper states for (2,7,7) and (4,7,7)",
   any(ok for _, _, ok in theorem7_applies(7)), True)
ck("NOT available at m = 11 -- their claim, confirmed, and for ALL THREE m'",
   any(ok for _, _, ok in theorem7_applies(11)), False)
print()
print("      THE STRUCTURAL REASON, which is the part worth keeping:")
print("      Theorem 7 at m needs the ANTISUM bound at m - m'. Verifying")
print("      Zarankiewicz at K_{7,m} does NOT establish that bound -- (7,7) is")
print("      verified yet sets sit at 79 < 81, and (9,7) likewise at 140 < 144.")
print("      So Theorem 7's applicability DOES NOT PROPAGATE UP THE LADDER, and")
print("      the gap that blocks it is exactly the relaxation's non-tightness.")
print()
print("      CONSEQUENCE FOR MY OWN HEADROOM FIGURE: the 4,838x scaling proxy was")
print("      stated as valid 'because the same two reductions apply at every")
print("      case' -- canonical form and antisum pruning. THERE IS A THIRD,")
print("      Theorem 7, used at both (7,7) and (9,7) and ABSENT at (11,7).")
print("      The proxy is therefore OPTIMISTIC BY AN UNMEASURED FACTOR, and H")
print("      moves from PASS to UNDETERMINED.")

print()
print("=" * 72)
if FAIL:
    print(f"{len(FAIL)} FAILED: {FAIL}"); raise SystemExit(1)
print("Certificate arithmetic checks; Theorem 7 unavailability at m = 11 confirmed.")

# ================================================ 5. Q_xy: is its length bounded?
print()
print("5. Their question: does Woodall bound the LENGTH of Q_xy? (pp. 657-671)")
print("      Textual answer: NO. Neither definition on p.662 bounds it; both say")
print("      only 'not necessarily shortest'. And the paper's ONE length-reduction")
print("      device cannot be borrowed: Theorem 3(b)'s proof removes a repeated")
print("      label by deleting two edges and swapping x<->y on the segment between")
print("      them, which CHANGES THE LABEL SET. So it shortens a walk without")
print("      preserving the thing the definitions actually read off it.")
print()
print("      But the question is ELIMINABLE rather than answerable, because both")
print("      definitions reference Q_xy ONLY through which labels OCCUR in it.")
print("      Q_xy's identity and length are invisible to the conditions; only its")
print("      LABEL SET is read. Q_xy is a walk in CO_m (labels = pairs of M's")
print("      indices), so at m = 4 there are C(4,2) = 6 labels and 2^6 = 64 sets.")
print()
# CO_4, checked against Figure 1 on p.659
V4 = verts(4)
ck("CO_4 has 6 vertices", len(V4), 6)
E4 = []
for v in V4:
    n = len(v)
    for i in range(n):
        j = (i + 1) % n
        w = list(v); x, y = w[i], w[j]
        w[i], w[j] = w[j], w[i]
        k = w.index(0); u = tuple(w[k:] + w[:k])
        if u != v: E4.append((v, u, frozenset((x, y))))
und = {(frozenset((a, b)), lab) for a, b, lab in E4}
ck("CO_4 has 12 edges (4-regular on 6 vertices)", len(und), 12)
from collections import Counter
labcount = Counter(lab for _, lab in und)
ck("each of the 6 labels appears on exactly 2 edges", set(labcount.values()), {2})
ck("the 6 labels are the 2-subsets of {0,1,2,3}", len(labcount), 6)

LABELS = sorted(labcount, key=lambda s: sorted(s))
LIDX = {l: i for i, l in enumerate(LABELS)}
ADJ = {}
for a, b, lab in E4:
    ADJ.setdefault(a, []).append((b, LIDX[lab]))

def reachable_label_sets(src):
    """All (vertex, exact label set) reachable from src by a walk."""
    seen = {(src, 0)}
    stack = [(src, 0)]
    while stack:
        v, mask = stack.pop()
        for w, li in ADJ[v]:
            st = (w, mask | (1 << li))
            if st not in seen:
                seen.add(st); stack.append(st)
    return seen

ALL = {v: reachable_label_sets(v) for v in V4}
# an xy-antipath is an xy-path or an x-ybar-path (p.661)
def achievable(x, y):
    tgt = {y, rev(y)}
    return {m for (v, m) in ALL[x] if v in tgt}

counts = {}
for x in V4:
    for y in V4:
        counts[(x, y)] = len(achievable(x, y))
print(f"      Achievable label sets per ordered (x,y), out of 64:")
print(f"        min {min(counts.values())}   max {max(counts.values())}   "
      f"distinct values {sorted(set(counts.values()))}")
union_all = set().union(*(achievable(x, y) for x in V4 for y in V4))
ck("every one of the 64 label sets is achievable for SOME endpoint pair",
   len(union_all), 64)
print("      => the family is finite and small at m = 4, with no length bound")
print("         needed and none hiding: enumerate the 64 SETS, test achievability")
print("         by reachability over (vertex, label-mask) states -- 6 x 64 = 384")
print("         states, exhaustive. Any length cap in an implementation is then")
print("         an UNSTATED SPECIFICATION CHOICE, which is where their residual")
print("         epsilon would live; enumerating sets removes the choice entirely.")
