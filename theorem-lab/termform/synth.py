#!/usr/bin/env python3
"""
Staged enumerative synthesis with observational-equivalence pruning.

Stage 1  bodies B(n,k) over {n,k,consts}         -> derived leaves least/count
Stage 2  bodies B(n,k,d) where d is a stage-1 leaf -> deeper derived leaves
Stage 3  outer terms over {n, consts, derived leaves} matching the target

Two terms with the same value vector on the training objects are the same
hypothesis as far as the data can tell, so only one representative of each
vector is kept -- which is what makes the search finish. ALL minimal-size terms
matching the target are returned, never one chosen by tie-break.
"""
import itertools
from collections import OrderedDict

from language import BINOPS, ev, show, size

CONSTS = [0, 1, 2, 4]


def _leaves(vars_):
    return [("var", v) for v in vars_] + [("const", c) for c in CONSTS]


def enumerate_terms(vars_, objects, max_size, extra_leaves=(), ops=None,
                    env_for=None, cap=200000):
    """
    Enumerate terms over `vars_`, deduplicated by their value vector on
    `objects`. Returns an OrderedDict vector -> smallest term with that vector.
    """
    ops = ops or list(BINOPS)
    env_for = env_for or (lambda o: {"n": o})
    by_size = {1: list(_leaves(vars_)) + list(extra_leaves)}
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
        by_size[s] = new
    return seen


def derived_leaves(objects, body_size=3, extra_body_leaves=(), cap=4000):
    """
    Form new unary functions of n by wrapping 2-variable bodies in least/count.
    This is where `spf` is expected to appear as least(k: n % k).
    """
    envs = [{"n": o, "k": 1} for o in objects]
    bodies = enumerate_terms(
        ["n", "k"], list(range(len(objects))), body_size,
        extra_leaves=extra_body_leaves,
        env_for=lambda i: envs[i], cap=cap)
    out = OrderedDict()
    for body in bodies.values():
        for wrap in ("least", "count"):
            t = (wrap, body)
            try:
                v = tuple(ev(t, {"n": o}) for o in objects)
            except Exception:
                continue
            if v not in out:
                out[v] = t
    return out


def synthesize(objects, target, max_size=5, body_size=3, verbose=True):
    """Return every minimal-size term matching `target` on `objects`."""
    d1 = derived_leaves(objects, body_size=body_size)
    if verbose:
        print("  stage 1: %d distinct derived leaves" % len(d1))
    # stage 2: allow a stage-1 leaf inside bodies (needed for exponent-like terms)
    best_leaf_terms = list(d1.values())[:40]
    extra = [("_derived", t) for t in best_leaf_terms]
    d2 = OrderedDict(d1)
    for lt in best_leaf_terms[:12]:
        envs = [{"n": o, "k": 1, "d": None} for o in objects]
        try:
            bodies = enumerate_terms(
                ["n", "k"], list(range(len(objects))), body_size,
                extra_leaves=[lt],
                env_for=lambda i, envs=envs: envs[i], cap=1500)
        except Exception:
            continue
        for body in bodies.values():
            for wrap in ("least", "count"):
                t = (wrap, body)
                try:
                    v = tuple(ev(t, {"n": o}) for o in objects)
                except Exception:
                    continue
                if v not in d2:
                    d2[v] = t
    if verbose:
        print("  stage 2: %d distinct derived leaves" % len(d2))

    leaves = [t for t in d2.values() if size(t) <= 6]
    matches = []
    for s in range(1, max_size + 1):
        pool = enumerate_terms(["n"], objects, s, extra_leaves=leaves,
                               cap=120000)
        for v, t in pool.items():
            if v == tuple(target) and size(t) <= s:
                matches.append(t)
        if matches:
            m = min(size(t) for t in matches)
            return [t for t in matches if size(t) == m], len(pool)
    return [], 0
