#!/usr/bin/env python3
"""
Term formation, v2. See REPORT_M.md for why v1 found nothing.

The change is one line of accounting, and it is the point of the experiment:
**a formed term becomes a unit.** In v1 a derived leaf like `least(k: n % k)`
cost its full expansion (size 3) every time it appeared, so the correct terms
cost 8 and 9 and sat far outside any feasible enumeration. Once a formed term is
named and counted as size 1, the same targets cost 5 -- reachable.

That is not a trick to make the search succeed; it is what abstraction IS. A
system that cannot name what it has formed cannot build on it.
"""
import itertools
from collections import OrderedDict

from language import BINOPS, ev as _ev, show as _show, size as _size

CONSTS = [0, 1, 2, 4]
_REGISTRY = {}          # leaf id -> underlying term
_TABLE = {}             # (leaf id, n) -> value, so a formed term is computed once


def leaf(term, objects=()):
    lid = len(_REGISTRY)
    _REGISTRY[lid] = term
    for o in objects:                     # precompute: this is the whole point
        try:
            _TABLE[(lid, o)] = _ev(term, {"n": o})
        except Exception:
            pass
    return ("leaf", lid)


def ev(t, env):
    if t[0] == "leaf":
        key = (t[1], env["n"])
        if key in _TABLE:
            return _TABLE[key]
        v = _ev(_REGISTRY[t[1]], env)
        _TABLE[key] = v
        return v
    if t[0] in ("least", "count"):
        n = env["n"]
        rng = range(2, n + 1) if t[0] == "least" else range(1, n + 1)
        c = 0
        for k in rng:
            if ev(t[1], {**env, "k": k}) == 0:
                if t[0] == "least":
                    return k
                c += 1
        return 0 if t[0] == "least" else c
    if t[0] in ("var", "const"):
        return _ev(t, env)
    return BINOPS[t[0]](ev(t[1], env), ev(t[2], env))


def size(t):
    if t[0] in ("var", "const", "leaf"):
        return 1                      # a formed term is a unit
    if t[0] in ("least", "count"):
        return 1 + size(t[1])
    return 1 + size(t[1]) + size(t[2])


def show(t):
    if t[0] == "leaf":
        return "<%s>" % show(_REGISTRY[t[1]])
    if t[0] in ("least", "count"):
        return "%s(k: %s)" % (t[0], show(t[1]))
    if t[0] in ("var", "const"):
        return _show(t)
    sym = {"add": "+", "sub": "-", "mul": "*", "div": "//", "mod": "%",
           "pow": "^"}.get(t[0])
    return ("(%s %s %s)" % (show(t[1]), sym, show(t[2]))) if sym else \
        "%s(%s, %s)" % (t[0], show(t[1]), show(t[2]))


def enumerate_terms(vars_, objects, max_size, extra_leaves=(), ops=None,
                    env_for=None, cap=400000, beam=None):
    """
    `beam`, when set, keeps at most that many terms per size level (smallest
    first). A declared search-budget heuristic: it bounds the quadratic growth
    of the outer enumeration and can therefore MISS a reachable term. Any
    failure under a beam is reported as a budget failure, not a language one.
    """
    ops = ops or list(BINOPS)
    env_for = env_for or (lambda o: {"n": o})
    base = [("var", v) for v in vars_] + [("const", c) for c in CONSTS]
    by_size = {1: base + list(extra_leaves)}
    seen = OrderedDict()

    def vector(t):
        try:
            return tuple(ev(t, env_for(o)) for o in objects)
        except Exception:
            return None

    for t in by_size[1]:
        v = vector(t)
        if v is not None and v not in seen:
            seen[v] = t
    for s in range(2, max_size + 1):
        new = []
        for a in range(1, s):
            b = s - a - 1
            if b < 1:
                continue
            for t1 in by_size.get(a, []):
                for t2 in by_size.get(b, []):
                    for op in ops:
                        t = (op, t1, t2)
                        v = vector(t)
                        if v is None or v in seen:
                            continue
                        seen[v] = t
                        new.append(t)
                        if len(seen) > cap:
                            by_size[s] = new
                            return seen
        if beam and len(new) > beam:
            new = sorted(new, key=lambda t: (size(t), show(t)))[:beam]
        by_size[s] = new
    return seen


def form_leaves(objects, size1=3, size2=5, verbose=True):
    """Stage 1 then stage 2: form unary functions, letting stage 2 build on
    stage 1's formed terms as units.

    Bodies live under `least`/`count`, so they must be deduplicated by their
    behaviour over a GRID of (n, k) -- an earlier version keyed them on k = 1
    alone, which collapsed precisely the bodies that differ where it matters.
    """
    grid = [(o, k) for o in objects for k in range(1, min(o, 6) + 1)]
    envs = {i: {"n": n, "k": k} for i, (n, k) in enumerate(grid)}
    b1 = enumerate_terms(["n", "k"], list(range(len(grid))), size1,
                         env_for=lambda i: envs[i], cap=6000)
    formed = OrderedDict()
    for body in b1.values():
        for wrap in ("least", "count"):
            t = (wrap, body)
            try:
                v = tuple(ev(t, {"n": o}) for o in objects)
            except Exception:
                continue
            if v not in formed:
                formed[v] = t
    if verbose:
        print("  stage 1: %d formed terms" % len(formed))
    units = [leaf(t, objects) for t in formed.values()]
    b2 = enumerate_terms(["n", "k"], list(range(len(grid))), size2,
                         extra_leaves=units, env_for=lambda i: envs[i],
                         ops=["mod", "div", "sub", "mul", "pow", "add"],
                         cap=40000)
    for body in b2.values():
        for wrap in ("least", "count"):
            t = (wrap, body)
            try:
                v = tuple(ev(t, {"n": o}) for o in objects)
            except Exception:
                continue
            if v not in formed:
                formed[v] = t
    if verbose:
        print("  stage 2: %d formed terms total" % len(formed))
    return formed


def synthesize(objects, target, formed, max_size=5, unit_cap=500,
               verbose=False, beam=1200):
    """
    The outer search is quadratic in the number of formed leaves, so the leaf
    set is capped, preferring SIMPLER formed terms (smallest underlying
    expression). This is a search-budget choice, not a semantic one, and it is
    reported: a target needing a complex formed term may be missed.
    """
    # A formed term may BE the answer. Check every one of them before any
    # combinatorial stage: this is O(len(formed)) and an earlier version's
    # unit cap hid exact hits behind a string tie-break.
    direct = [t for t in formed.values()
              if tuple(ev(t, {"n": o}) for o in objects) == tuple(target)]
    if direct:
        m = min(size(t) for t in direct)
        return [t for t in direct if size(t) == m], len(formed)

    ranked = sorted(formed.values(), key=lambda t: (size(t), show(t)))
    units = [leaf(t, objects) for t in ranked[:unit_cap]]
    for s in range(1, max_size + 1):
        if verbose:
            print("    outer size %d ..." % s, flush=True)
        pool = enumerate_terms(["n"], objects, s, extra_leaves=units,
                               beam=beam)
        hits = [t for v, t in pool.items() if v == tuple(target)]
        if hits:
            m = min(size(t) for t in hits)
            return [t for t in hits if size(t) == m], len(pool)
    return [], 0
