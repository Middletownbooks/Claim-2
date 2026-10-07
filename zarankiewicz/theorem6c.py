#!/usr/bin/env python3
"""theorem6c.py -- Woodall's augmented antisum, the device that closed K_{7,7}.

Theorem 6(c), p.663 of Woodall 1993, verbatim:

    If n is odd then  f(M) = Abar(M) + 2*floor( 2t / ((m-2)(m-3)) )
    is a lobspacron function, where t is the number of (4,n)-subsets of the
    (m,n)-set M that are NOT pseudo-tight.

("lobspacron" = LOwer Bound, Same PArity As, CROssing Number.)  The proof: a
(4,n)-subset that is not pseudo-tight is not tight, so some (2,n)-subset {a,b}
inside it is drawn with at least dbar(a,b) + 2 crossings; each (2,n)-subset lies
in exactly (m-2)(m-3)/2 of the (4,n)-subsets, so the floor counts distinct bad
pairs from below and each contributes 2.

    m =  7:  2*floor(t/10)   -- and Woodall's 13,448 sets at antisum 79 each had
                                t >= 10, which is exactly how 79 was lifted to 81.
    m = 11:  2*floor(t/36)   -- so antisum 219 needs t >= 108, 221 needs t >= 72,
                                and 223 needs t >= 36, to reach Z(11)Z(7) = 225.

PSEUDO-TIGHTNESS (pp. 661-663), as re-derived in board-finder/gap/v4.  For a
(4,n)-set M' take, for each of its 6 pairs (a,b), the label sets of all SHORTEST
a -> rev(b) antipaths in CO_n.  A ground pair xy is FORCED for the M'-pair if it
occurs in every such label set, and POSSIBLE if it occurs in at least one.  M' is
pseudo-tight iff there is an (n,4)-set N -- n vertices of CO_4, indexed by the
ground set -- such that for every ground pair {x,y} some N[x] -> rev(N[y])
antipath in CO_4 has a label set L with FORCED(xy) <= L <= POSSIBLE(xy).

CONVENTION.  "Antipath" admits a lattice of readings; pseudo-tightness is
MONOTONE in the antipath family, so the LARGEST family (arbitrary walks, label
reuse permitted) makes pseudo-tightness easiest, t smallest, and f smallest.
That is the conservative direction, so the default here is `arbitrary` and a
bound proved under it holds under every reading.  --family reports the others.

USAGE
  python3 theorem6c.py --selftest
  python3 theorem6c.py --class 0,0,15,74,105,438,569,647,660,671,689
  python3 theorem6c.py --rows sweep_L5/low_0.txt --limit 50
"""
import argparse, itertools, sys
from collections import deque

sys.path.insert(0, 'intake')
import cog

N_GROUND = 7


def build(n):
    C = cog.CO(n)
    return C


def rev_of(C, v):
    return C.rev[v]


# ---------------------------------------------------------------- CO_4 families
def co4_tables(family):
    """Q[(u,v)] = set of label-masks of u -> v antipaths in CO_4, for each of the
    four readings of "antipath" the definition can license.  Validated against the
    published family sizes 234 / 282 / 594 / 1758 (board-finder/gap/v4).

      both      vertex-simple AND label-distinct   234   (smallest)
      walk      label-distinct, revisits allowed   282
      path      vertex-simple, labels may repeat   594
      arbitrary any walk at all                   1758   (largest)

    Pseudo-tightness is MONOTONE in the family, so `arbitrary` minimises t and is
    the only reading that yields a conservative bound."""
    C4 = cog.CO(4)
    res = {}
    total = 0
    for src in range(C4.NV):
        out = set()
        if family in ("walk", "arbitrary"):
            seen = {(src, 0)}
            st = [(src, 0)]
            while st:
                v, m = st.pop()
                out.add((v, m))
                for w, l in C4.adj[v]:
                    b = 1 << l
                    if family == "walk" and (m & b):
                        continue
                    nm = m | b
                    if (w, nm) not in seen:
                        seen.add((w, nm))
                        st.append((w, nm))
        else:
            def go(v, visited, m):
                out.add((v, m))
                for w, l in C4.adj[v]:
                    b = 1 << l
                    if w in visited:
                        continue
                    if family == "both" and (m & b):
                        continue
                    go(w, visited | {w}, m | b)
            go(src, {src}, 0)
        total += len(out)
        for (v, m) in out:
            res.setdefault((src, v), set()).add(m)
    return C4, res, total


FAMILY_SIZES = {"both": 234, "walk": 282, "path": 594, "arbitrary": 1758}


def shortest_label_sets(C, a, b, cap=200000):
    """Label sets of all shortest a -> rev(b) paths in CO_n, as bitmasks."""
    t = C.rev[b]
    da = bfs(C, a)
    dt = bfs(C, t)
    D = da[t]
    out = set()
    stack = [(a, 0)]
    seen = set()
    while stack:
        u, m = stack.pop()
        if u == t:
            out.add(m)
            continue
        for w, l in C.adj[u]:
            if da[w] == da[u] + 1 and da[w] + dt[w] == D:
                st = (w, m | (1 << l))
                if st not in seen:
                    seen.add(st)
                    stack.append(st)
        if len(seen) > cap:
            raise RuntimeError("shortest-antipath DAG too large")
    return out, D


def bfs(C, s):
    d = [-1] * C.NV
    d[s] = 0
    q = deque([s])
    while q:
        u = q.popleft()
        for w, _ in C.adj[u]:
            if d[w] < 0:
                d[w] = d[u] + 1
                q.append(w)
    return d


def pseudo_tight(C, Msub, C4, Q, cache={}):
    """Is this (4,n)-multiset pseudo-tight?"""
    key = (tuple(Msub), id(Q))
    if key in cache:
        return cache[key]
    pairs = list(itertools.combinations(range(4), 2))
    pidx = {p: i for i, p in enumerate(pairs)}
    SLS = []
    for (i, j) in pairs:
        s, _ = shortest_label_sets(C, Msub[i], Msub[j])
        SLS.append(s)
    # FORCED / POSSIBLE per ground pair, as masks over the 6 M'-pairs
    nlab = C.NL
    forced = [0] * nlab
    possible = [0] * nlab
    for li in range(nlab):
        for pi, sets in enumerate(SLS):
            inall = all((m >> li) & 1 for m in sets)
            inany = any((m >> li) & 1 for m in sets)
            if inall:
                forced[li] |= 1 << pi
            if inany:
                possible[li] |= 1 << pi
    # ground pair {x,y} -> label index in CO_n's labellist
    gpair = {}
    for li, (x, y) in enumerate(C.labellist):
        gpair[(x, y)] = li
    # allowed (u,v) per ground pair
    allowed = {}
    for (x, y), li in gpair.items():
        fm, pm = forced[li], possible[li]
        A = set()
        for u in range(C4.NV):
            for v in range(C4.NV):
                tv = C4.rev[v]
                for m in Q.get((u, tv), ()):  # u -> rev(v) antipath
                    if (m & fm) == fm and (m | pm) == pm:
                        A.add((u, v))
                        break
        allowed[(x, y)] = A
    ok = search_N(C.n, C4.NV, allowed)
    cache[key] = ok
    return ok


def search_N(n, nv4, allowed):
    """Is there N in V(CO_4)^n meeting every ground-pair constraint?"""
    Nv = [-1] * n
    adjok = {}
    for (x, y), A in allowed.items():
        adjok[(x, y)] = A

    def rec(i):
        if i == n:
            return True
        for u in range(nv4):
            good = True
            for j in range(i):
                if (Nv[j], u) not in adjok[(j, i)]:
                    good = False
                    break
            if good:
                Nv[i] = u
                if rec(i + 1):
                    return True
                Nv[i] = -1
        return False

    return rec(0)


def t_of(C, M, C4, Q, verbose=False):
    bad = 0
    tot = 0
    for S in itertools.combinations(range(len(M)), 4):
        sub = [M[i] for i in S]
        tot += 1
        if not pseudo_tight(C, sub, C4, Q):
            bad += 1
    return bad, tot


def f_of(antisum, t, m):
    return antisum + 2 * ((2 * t) // ((m - 2) * (m - 3)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--class", dest="cls")
    ap.add_argument("--rows")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--family", default="arbitrary",
                    choices=["arbitrary", "walk", "path", "both"])
    a = ap.parse_args()
    C = build(N_GROUND)
    A = C.antidist_matrix(C.dist_matrix())
    C4, Q, tot = co4_tables(a.family)
    assert tot == FAMILY_SIZES[a.family], (a.family, tot, FAMILY_SIZES[a.family])
    if a.selftest:
        # Theorem 6(c)'s arithmetic at the two sizes the paper and this repo use.
        assert f_of(79, 10, 7) == 81, f_of(79, 10, 7)
        assert f_of(79, 9, 7) == 79
        assert f_of(219, 108, 11) == 225
        assert f_of(219, 107, 11) == 223
        assert f_of(221, 72, 11) == 225
        assert f_of(223, 36, 11) == 225
        print("Theorem 6(c) arithmetic: 79+2*floor(10/10)=81 (Woodall's own use at m=7);")
        print("  m=11 thresholds t >= 108 / 72 / 36 at antisum 219 / 221 / 223")
        for f in ("both", "walk", "path", "arbitrary"):
            _, _, tt = co4_tables(f)
            assert tt == FAMILY_SIZES[f], (f, tt)
            print("  CO_4 family %-9s size %4d  (published %d) ok" % (f, tt, FAMILY_SIZES[f]))
        return
    if a.cls:
        M = [int(x) for x in a.cls.split(",")]
        T = sum(A[x][y] for x, y in itertools.combinations(M, 2))
        t, tot = t_of(C, M, C4, Q)
        m = len(M)
        print("multiset   :", M)
        print("antisum    :", T)
        print("(4,7)-subsets: %d, not pseudo-tight: t = %d  (family %s)" % (tot, t, a.family))
        print("Theorem 6(c): f = %d + 2*floor(2*%d/%d) = %d"
              % (T, t, (m - 2) * (m - 3), f_of(T, t, m)))
        print("target     : 225")
        return
    if a.rows:
        n = 0
        worst = None
        for line in open(a.rows):
            p = [int(x) for x in line.split(",")]
            M = p[1:]
            t, tot = t_of(C, M, C4, Q)
            f = f_of(p[0], t, len(M))
            if worst is None or f < worst[0]:
                worst = (f, p[0], t, M)
            n += 1
            if a.limit and n >= a.limit:
                break
        print("rows %d   weakest f = %d at antisum %d with t = %d" % (n, worst[0], worst[1], worst[2]))
        print("  ", worst[3])


if __name__ == "__main__":
    main()
