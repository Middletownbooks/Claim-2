#!/usr/bin/env python3
"""
Round-2 search engine: `termform/synth2.py` with four changes, each demanded by
a Priority in the brief.

1. **Cost is a per-leaf property, not a constant.** A promoted term can be
   charged 1 (condition B) or its full expanded size (condition D). The
   enumerator places base atoms into size buckets by their cost, so the two
   conditions differ only in that number. (Priority 9.)
2. **Definition-blind unit selection.** Round 1 broke ties by the printed form
   of a term's internal definition. Here the ordering key is
   `(cost, blake2b(value-vector))` -- the value vector is the permitted
   evaluation interface, the definition is not consulted. (Priority 11-D.)
3. **Instrumentation.** Candidate expansions, evaluations and per-level class
   counts are counted so conditions can be compared at matched budget rather
   than matched wall clock. (Priorities 3, 11-F.)
4. **Watched vectors.** Target vectors can be registered before the search; ALL
   terms hitting a watched vector are collected, including ones the dedup would
   otherwise drop, so the disagreement stage sees the full survivor set.
   (Priority 7.)

State is module-level and must be cleared with `reset()` between conditions.
"""
import hashlib
import itertools
from collections import OrderedDict, defaultdict

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "termform"))
from language import BINOPS, ev as _ev, show as _show, size as _size  # noqa

CONSTS = [0, 1, 2, 4]

_REGISTRY = {}
_TABLE = {}
_COST = {}
STATS = defaultdict(int)


def reset():
    _REGISTRY.clear()
    _TABLE.clear()
    _COST.clear()
    STATS.clear()


def leaf(term, objects=(), cost=1):
    lid = len(_REGISTRY)
    _REGISTRY[lid] = term
    _COST[lid] = cost
    for o in objects:
        try:
            _TABLE[(lid, o)] = ev(term, {"n": o})
        except Exception:
            pass
    return ("leaf", lid)


def expanded_size(t):
    """Cost of a term with every leaf recursively replaced by its definition.
    This is the Round-1 v1 cost model and the charge used by condition D."""
    if t[0] == "leaf":
        return expanded_size(_REGISTRY[t[1]])
    if t[0] in ("var", "const"):
        return 1
    if t[0] in ("least", "count"):
        return 1 + expanded_size(t[1])
    return 1 + expanded_size(t[1]) + expanded_size(t[2])


def expand(t):
    """Replace every leaf by its definition, giving a self-contained term.
    Used to serialise formed terms across processes."""
    if t[0] == "leaf":
        return expand(_REGISTRY[t[1]])
    if t[0] in ("var", "const"):
        return t
    if t[0] in ("least", "count"):
        return (t[0], expand(t[1]))
    return (t[0], expand(t[1]), expand(t[2]))


def uses_ids(t, ids):
    """Does `t` use any of these leaf ids, at any depth, including inside the
    definitions of other leaves it uses?

    Needed because a formed term prints as its own definition: Round 2's
    independently re-formed `least(k: (n % k))` and a CARRIED-OVER promoted
    term with the same definition are indistinguishable as strings but are
    different atoms. Only the identity of the atom answers the question
    "did the carried vocabulary actually get used?"."""
    if t[0] == "leaf":
        return t[1] in ids or uses_ids(_REGISTRY[t[1]], ids)
    if t[0] in ("var", "const"):
        return False
    return any(uses_ids(a, ids) for a in t[1:])


def definition(t):
    """The underlying term of a leaf. Used only for reporting and for the
    re-expansion cost, never inside the search."""
    return _REGISTRY[t[1]] if t[0] == "leaf" else t


def ev(t, env):
    h = t[0]
    if h == "leaf":
        key = (t[1], env["n"])
        v = _TABLE.get(key)
        if v is None:
            # NOTE: must recurse through THIS evaluator, not language.ev.
            # A promoted or stage-2 unit's definition can itself contain a
            # unit; language.ev raises ValueError("leaf") on those. In
            # termform/synth2.py the same fallback used language.ev, and the
            # ValueError was swallowed by the caller's try/except -- so every
            # unit whose definition contained a nested unit was silently
            # dropped from the Round-1 outer search. See REPORT_P section on
            # inherited defects. Round 2 fixes it, identically in every
            # condition.
            v = ev(_REGISTRY[t[1]], env)
            _TABLE[key] = v
        return v
    if h in ("least", "count"):
        n = env["n"]
        if h == "least":
            for k in range(2, n + 1):
                if ev(t[1], {**env, "k": k}) == 0:
                    return k
            return 0
        c = 0
        for k in range(1, n + 1):
            if ev(t[1], {**env, "k": k}) == 0:
                c += 1
        return c
    if h in ("var", "const"):
        return _ev(t, env)
    return BINOPS[h](ev(t[1], env), ev(t[2], env))


def size(t):
    if t[0] == "leaf":
        return _COST[t[1]]
    if t[0] in ("var", "const"):
        return 1
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


def vkey(vec):
    return hashlib.blake2b(repr(vec).encode(), digest_size=16).digest()


def enumerate_terms(vars_, objects, max_size, extra_leaves=(), ops=None,
                    env_for=None, cap=300000, beam=None, watch=None,
                    level_log=None, tag=""):
    """Enumerate terms up to `max_size` under the cost model, deduplicating by
    value vector on `objects`.

    `watch` maps a value vector to a name; every term reaching a watched vector
    is recorded in the returned `hits`, even when the dedup would drop it.
    `level_log`, if given, receives one record per cost level.
    """
    ops = ops or list(BINOPS)
    env_for = env_for or (lambda o: {"n": o})
    base = [("var", v) for v in vars_] + [("const", c) for c in CONSTS] \
        + list(extra_leaves)
    by_size = defaultdict(list)
    seen = OrderedDict()
    hits = defaultdict(list)
    truncated = False

    def vector(t):
        STATS["evals"] += 1
        try:
            return tuple(ev(t, env_for(o)) for o in objects)
        except Exception:
            return None

    for t in base:
        c = size(t)
        if c > max_size:
            continue
        by_size[c].append(t)
        v = vector(t)
        if v is None:
            continue
        if watch and v in watch:
            hits[v].append((c, t))
        if v not in seen:
            seen[v] = t

    for s in range(1, max_size + 1):
        if s > 1:
            new = []
            for a in range(1, s):
                b = s - a - 1
                if b < 1:
                    continue
                for t1 in by_size.get(a, ()):
                    for t2 in by_size.get(b, ()):
                        for op in ops:
                            STATS["expansions"] += 1
                            t = (op, t1, t2)
                            v = vector(t)
                            if v is None:
                                continue
                            if watch and v in watch:
                                hits[v].append((s, t))
                            if v in seen:
                                continue
                            seen[v] = t
                            new.append((t, v))
                            if len(seen) >= cap:
                                truncated = True
                                break
                        if truncated:
                            break
                    if truncated:
                        break
                if truncated:
                    break
            if beam and len(new) > beam:
                new = sorted(new, key=lambda tv: (size(tv[0]), vkey(tv[1])))
                STATS["beam_dropped"] += len(new) - beam
                new = new[:beam]
            by_size[s].extend(t for t, _ in new)
        if level_log is not None:
            level_log.append({"cost": s, "classes_cumulative": len(seen),
                              "kept_at_level": len(by_size.get(s, ())),
                              "expansions_cumulative": STATS["expansions"],
                              "truncated": truncated})
        if truncated:
            break
    return seen, hits, truncated


def form_leaves(objects, size1=3, size2=5, extra_leaves=(), verbose=True,
                tag="", levels=2):
    """Round 1's two-stage formation, with promoted units (if any) available in
    both stages. Bodies are deduplicated on an (n, k) grid.

    `levels=1` runs stage 1 only: ONE turn of abstraction per round. Round 1
    and the Round-2 conditions use the default 2, which is Round 1's own
    setting; the ladder uses 1 so that a single round cannot contain two turns
    of the very loop the ladder is trying to observe."""
    grid = [(o, k) for o in objects for k in range(1, min(o, 6) + 1)]
    envs = {i: {"n": n, "k": k} for i, (n, k) in enumerate(grid)}
    idx = list(range(len(grid)))
    b1, _, _ = enumerate_terms(["n", "k"], idx, size1, extra_leaves=extra_leaves,
                               env_for=lambda i: envs[i], cap=6000, tag=tag)
    formed = OrderedDict()

    def wrap_all(bodies):
        for body in bodies:
            for w in ("least", "count"):
                t = (w, body)
                try:
                    v = tuple(ev(t, {"n": o}) for o in objects)
                except Exception:
                    continue
                if v not in formed:
                    formed[v] = t

    wrap_all(b1.values())
    if verbose:
        print("    stage 1: %d formed" % len(formed), flush=True)
    if levels < 2:
        return formed
    units = [leaf(t, objects) for t in formed.values()]
    b2, _, _ = enumerate_terms(["n", "k"], idx, size2,
                               extra_leaves=list(extra_leaves) + units,
                               env_for=lambda i: envs[i],
                               ops=["mod", "div", "sub", "mul", "pow", "add"],
                               cap=40000, tag=tag)
    wrap_all(b2.values())
    if verbose:
        print("    stage 2: %d formed total" % len(formed), flush=True)
    return formed


def select_units(formed, objects, unit_cap, forced_leaves=(),
                 order="size_then_blind_tie"):
    """Definition-blind selection of the atom set (Priority 11-D).

    `forced` terms (the promoted vocabulary) always enter and OCCUPY SLOTS: the
    total number of atoms is `unit_cap` in every condition, so the comparison is
    not confounded by symbol count (Priority 11-A).

    The caller supplies the forced atoms as ready-made leaves, so their cost is
    already fixed by the condition. Round-2's own
    within-round formations are always charged 1, exactly as in Round 1, so
    condition D isolates the cost of CARRYING a term across a round rather than
    abolishing abstraction altogether -- condition A0 does the latter.
    """
    units = list(forced_leaves)
    forced_defs = {repr(_REGISTRY[u[1]]) for u in units}
    pool = []
    for t in formed.values():
        try:
            v = tuple(ev(t, {"n": o}) for o in objects)
        except Exception:
            continue
        if repr(t) in forced_defs:
            continue          # a promoted term is not also counted as its own
        pool.append((expanded_size(t), vkey(v), t))
    if order == "blind":
        # strict definition blindness (Priority 11-D sensitivity run): the only
        # key is the value vector, so nothing about the definition is consulted
        pool.sort(key=lambda x: x[1])
    else:
        # Round 1's declared preference for simpler formed terms, with its
        # printed-form tie-break replaced by a value-vector hash
        pool.sort(key=lambda x: (x[0], x[1]))
    for _, _, t in pool[:max(0, unit_cap - len(units))]:
        units.append(leaf(t, objects))
    return units
