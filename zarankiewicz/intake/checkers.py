"""
checkers.py -- tight / pseudo-tight for an (m,n)-set, with the Q_xy antipath
family as an explicit parameter.  Works for any m (the dual lives on CO_m).

Woodall p.662.  M is TIGHT iff there exist an (n,m)-set N, a SHORTEST ab-antipath
P_ab for each of the C(m,2) pairs, and an xy-antipath Q_xy for each pair of
N-indices, with   xy in labels(P_ab)  <=>  ab in labels(Q_xy).
M is PSEUDO-TIGHT iff there exist N and Q_xy with
   {ab : xy in EVERY shortest ab-antipath} subset labels(Q_xy)
                                            subset {ab : xy in SOME shortest ab-antipath}.

INDEX CORRESPONDENCE (the thing easiest to get wrong):
  CO_n labels are pairs of N-indices;  CO_m labels are pairs of M-indices.
  So combinations(range(m),2) must equal Gm.labellist -- asserted below.

THE Q FAMILY.  Woodall never defines "path" in pp.657-671.  Four readings:
    'both'      simple AND label-distinct       CO_4: 234    CO_5: 8,088
    'walk'      label-distinct, revisits ok     CO_4: 282    CO_5: 8,448
    'path'      simple, labels may repeat       CO_4: 594    CO_5: does not scale
    'arbitrary' any walk                        CO_4: 1,758  CO_5: 296,544
  Ordered by inclusion with 'both' at the bottom and 'arbitrary' at the top;
  'walk' and 'path' are incomparable.
  Shortest objects are automatically simple, so the reading can only bite on Q_xy.

THE BRACKET (use this, not per-reading checking).  pseudo-tightness is monotone
increasing in the family, non-tightness monotone decreasing.  So:
    pseudo-tight at 'both'  AND  not tight at 'arbitrary'
      <=>  pseudo-tight and not tight under EVERY reading in the lattice.
This is exact, not conservative, and it covers readings nobody enumerated.
BOUNDARY: valid for a FIXED OBJECT.  It does NOT transfer to counts or to
universal negatives -- (pseudo-tight AND not tight) is a WINDOW in the lattice,
neither an up-set nor a down-set, so a set can satisfy it at an intermediate
reading and at neither extreme.  Measured at n=6: counts 48/19/54/22 across the
four readings, with only 14 classes common to all.
"""
import time
from itertools import combinations

KINDS = ('both', 'walk', 'path', 'arbitrary')


def family(Gm, kind):
    """Label-set family for Q_xy in CO_m.  Returns fam[u][w] = set of bitmasks
    over Gm's labels realisable by an admissible u->w object."""
    NV = Gm.NV
    out = [[set() for _ in range(NV)] for _ in range(NV)]
    for s in range(NV):
        if kind in ('arbitrary', 'walk'):
            seen = {(s, 0)}
            st = [(s, 0)]
            while st:
                u, mask = st.pop()
                out[s][u].add(mask)
                for v, lab in Gm.adj[u]:
                    if kind == 'walk' and (mask >> lab) & 1:
                        continue
                    k = (v, mask | (1 << lab))
                    if k not in seen:
                        seen.add(k)
                        st.append(k)
        else:
            st = [(s, 1 << s, 0)]
            while st:
                u, vis, mask = st.pop()
                out[s][u].add(mask)
                for v, lab in Gm.adj[u]:
                    if (vis >> v) & 1:
                        continue
                    if kind == 'both' and (mask >> lab) & 1:
                        continue
                    st.append((v, vis | (1 << v), mask | (1 << lab)))
    return out


def forced_possible(Gn, D, a, b):
    """(forced, possible) label bitmasks over Gn's labels for the pair (a,b):
    labels occurring in EVERY / in SOME shortest ab-antipath.
    Computed by shortest-path-DAG reachability.  Cross-checked against explicit
    enumeration (intersection / union of shortest_label_sets) -- they agree."""
    tb = Gn.rev[b]
    da, db = D[a], D[tb]
    L = da[tb]
    dag = []
    for u in range(Gn.NV):
        du = da[u]
        if du < 0 or du >= L:
            continue
        for v, lab in Gn.adj[u]:
            if du + 1 + db[v] == L:
                dag.append((u, v, lab))
    poss = 0
    for _, _, lab in dag:
        poss |= 1 << lab
    order = sorted({u for u, _, _ in dag} | {v for _, v, _ in dag}, key=lambda z: da[z])
    byu = {}
    for u, v, l in dag:
        byu.setdefault(u, []).append((v, l))
    forced = 0
    for lab in range(Gn.NL):
        if not (poss >> lab) & 1:
            continue
        reach = {a}
        for u in order:
            if u in reach:
                for v, l2 in byu.get(u, ()):
                    if l2 != lab:
                        reach.add(v)
        if tb not in reach:
            forced |= 1 << lab
    return forced, poss


def shortest_label_sets(Gn, D, a, b, cap=50000):
    """All label bitmasks of shortest ab-antipaths.  None if it blows `cap`."""
    tb = Gn.rev[b]
    da, db = D[a], D[tb]
    L = da[tb]
    if L == 0:
        return {0}
    nodes = [u for u in range(Gn.NV) if da[u] >= 0 and db[u] >= 0 and da[u] + db[u] == L]
    nodes.sort(key=lambda u: -da[u])
    sets = {tb: {0}}
    for u in nodes:
        if u == tb:
            continue
        acc = set()
        for v, lab in Gn.adj[u]:
            if da[u] + 1 + db[v] == L and v in sets:
                bit = 1 << lab
                for m in sets[v]:
                    acc.add(m | bit)
                    if len(acc) > cap:
                        return None
        if acc:
            sets[u] = acc
    return sets.get(a, set())


def _csp(Gn, Gm, cm):
    """Assign each of the n N-indices a vertex of CO_m, subject to a binary
    constraint per pair.  Returns (ok, assignment)."""
    n = Gn.n
    asg = {}

    def rec(k):
        if k == n:
            return True
        for v in range(Gm.NV):
            if all(cm(Gn.labelidx[(j, k)], asg[j], v) for j in range(k)):
                asg[k] = v
                if rec(k + 1):
                    return True
                del asg[k]
        return False

    return rec(0), dict(asg)


def _lb_ub(Gn, D, M, cache):
    m = len(M)
    mp = list(combinations(range(m), 2))
    LB = [0] * Gn.NL
    UB = [0] * Gn.NL
    for pi, (i, j) in enumerate(mp):
        key = (M[i], M[j])
        if key not in cache:
            cache[key] = forced_possible(Gn, D, M[i], M[j])
        f, p = cache[key]
        for lab in range(Gn.NL):
            if (f >> lab) & 1:
                LB[lab] |= 1 << pi
            if (p >> lab) & 1:
                UB[lab] |= 1 << pi
    return LB, UB


def pseudo_tight(Gn, D, Gm, fam, M, cache=None, want_witness=False):
    assert list(combinations(range(len(M)), 2)) == Gm.labellist, "m / dual mismatch"
    cache = {} if cache is None else cache
    LB, UB = _lb_ub(Gn, D, M, cache)

    def cm(lab, u, v):
        lb, ub = LB[lab], UB[lab]
        return any((S & lb) == lb and (S & ~ub) == 0 for S in fam[u][Gm.rev[v]])

    ok, asg = _csp(Gn, Gm, cm)
    if want_witness:
        return ok, ([asg[x] for x in range(Gn.n)] if ok else None)
    return ok


def is_tight(Gn, D, Gm, fam, M, budget=None, product_cap=200000):
    """True / False, or None if undetermined (shortest-set cap, product cap, or
    time budget).  Given the row choices the dual label sets are FORCED, so this
    is: pick one shortest-antipath label set per M-pair, require every induced
    column to be realisable in CO_m for one common N."""
    assert list(combinations(range(len(M)), 2)) == Gm.labellist, "m / dual mismatch"
    mp = list(combinations(range(len(M)), 2))
    rows = []
    for (i, j) in mp:
        s = shortest_label_sets(Gn, D, M[i], M[j])
        if s is None:
            return None
        if not s:
            return False
        rows.append(sorted(s))
    prod = 1
    for r in rows:
        prod *= len(r)
    if prod > product_cap:
        return None
    ch = [None] * len(mp)
    t0 = time.time()

    def rec(pi):
        if budget is not None and time.time() - t0 > budget:
            raise TimeoutError
        if pi == len(mp):
            cols = []
            for lab in range(Gn.NL):
                x = 0
                for q in range(len(mp)):
                    if (ch[q] >> lab) & 1:
                        x |= 1 << q
                cols.append(x)
            return _csp(Gn, Gm, lambda lab, u, v: cols[lab] in fam[u][Gm.rev[v]])[0]
        for mm in rows[pi]:
            ch[pi] = mm
            if rec(pi + 1):
                return True
        ch[pi] = None
        return False

    try:
        return rec(0)
    except TimeoutError:
        return None


def bracket(Gn, D, Gm, fams, M, cache=None):
    """Reading-independent verdict.  Returns (is_counterexample, pt_at_min, tight_at_max).
    is_counterexample is True iff M is pseudo-tight AND not tight under EVERY reading."""
    pt = pseudo_tight(Gn, D, Gm, fams['both'], M, cache)
    tg = is_tight(Gn, D, Gm, fams['arbitrary'], M)
    return (bool(pt) and tg is False), pt, tg
