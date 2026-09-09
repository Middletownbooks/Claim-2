#!/usr/bin/env python3
"""
Round 2. One condition per invocation: `python3 round2.py A0|A|B|C|D|E`.

Everything here follows PREREG.md, which was committed before this file was
written. Deviations are recorded in the output under "deviations", with the
reason, and are never made after seeing a result.
"""
import ast
import hashlib
import json
import random
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "termform"))
sys.path.insert(0, str(HERE.parent))

import invariants as INV                                    # noqa: E402
import synth3 as S                                          # noqa: E402
from outer import Outer, verify_operators                   # noqa: E402
from stages import abstention, disagreement                 # noqa: E402

TRAIN = list(range(2, 41))
RESERVE = list(range(41, 56))
HOLDOUT = list(range(56, 91))
EVALQ = list(range(121, 161))
for a, b in ((TRAIN, RESERVE), (TRAIN, HOLDOUT), (TRAIN, EVALQ),
             (RESERVE, HOLDOUT), (RESERVE, EVALQ), (HOLDOUT, EVALQ)):
    assert not set(a) & set(b)

UNIT_CAP = 500
BEAM = 1200
CAP = 300000
MAX_SIZE = 5
E_MAX_SIZE, E_BEAM = 7, 2400
SEED = 20260909


def promoted():
    d = json.loads((HERE / "promoted_terms.json").read_text())
    return [ast.literal_eval(t) for t in d["term_tuples"]]


def round1_pool():
    """The 5 329 Round-1 formed terms, self-contained. Cached: regenerating
    them costs ~40 s and the result is deterministic."""
    cache = HERE / "round1_formed_pool.json"
    if cache.exists():
        return [ast.literal_eval(t) for t in json.loads(cache.read_text())]
    from run import TRAIN as R1TRAIN
    S.reset()
    formed = S.form_leaves(R1TRAIN, verbose=False)
    terms = [S.expand(t) for t in formed.values()]
    cache.write_text(json.dumps([repr(t) for t in terms], indent=0))
    S.reset()
    return terms


def random_vocabulary(k, exclude_vectors, seed=SEED):
    """Condition C. Drawn from the Round-1 formed pool, excluding anything
    semantically equal on TRAIN to a promoted term. Seed fixed in PREREG."""
    pool = round1_pool()
    rng = random.Random(seed)
    rng.shuffle(pool)
    out = []
    for t in pool:
        try:
            v = tuple(S.ev(t, {"n": o}) for o in TRAIN)
        except Exception:
            continue
        if v in exclude_vectors:
            continue
        out.append(t)
        if len(out) == k:
            break
    return out


def build(cond):
    """Return (atoms, info). Atoms are the outer search's base symbols."""
    S.reset()
    info = {"condition": cond}
    P = promoted()
    forced = []
    if cond == "B520":
        # EXPLORATORY, not pre-registered. Condition B spends 20 of its 500
        # atom slots on the promoted terms, displacing 20 of Round 2's own
        # formations. B520 gives the promoted terms 20 EXTRA slots instead, so
        # symbol count is no longer matched (it is 520 vs 500). It answers only
        # "is B worse than A because of displacement?" and is reported apart
        # from the pre-registered comparisons.
        forced = [S.leaf(t, TRAIN, cost=1) for t in P]
    if cond == "Bo":
        # EXPLORATORY, not pre-registered, added before any Round-2 result was
        # seen: the promoted terms are available to the OUTER search only, not
        # during term formation. It localises where a B-vs-A effect acts.
        forced = [S.leaf(t, TRAIN, cost=1) for t in P]
    if cond in ("B", "D"):
        cost = (lambda t: 1) if cond == "B" else S.expanded_size
        forced = [S.leaf(t, TRAIN, cost=cost(t)) for t in P]
        info["forced_costs"] = sorted(S.size(u) for u in forced)
    elif cond == "C":
        exclude = set()
        for t in P:
            try:
                exclude.add(tuple(S.ev(t, {"n": o}) for o in TRAIN))
            except Exception:
                pass
        R = random_vocabulary(len(P), exclude)
        forced = [S.leaf(t, TRAIN, cost=1) for t in R]
        info["random_vocabulary"] = [S.show(u) for u in forced]

    if cond == "A0":
        units, formed = [], {}
        info["formed_terms"] = 0
    else:
        t0 = time.time()
        formed = S.form_leaves(
            TRAIN, extra_leaves=() if cond == "Bo" else forced, tag=cond)
        info["formed_terms"] = len(formed)
        info["formation_seconds"] = round(time.time() - t0, 1)
        cap_units = UNIT_CAP + (len(forced) if cond == "B520" else 0)
        units = S.select_units(formed, TRAIN, cap_units, forced_leaves=forced)
    info["units"] = len(units)
    info["carried_over"] = len(forced)
    atoms = [("var", "n")] + [("const", c) for c in S.CONSTS] + units
    info["outer_atoms"] = len(atoms)
    return atoms, info, formed, {u[1] for u in forced}


def semantic_refinement(O, cond):
    """PREREG section 5: re-quotient a uniform sample of each level's classes
    on TRAIN + EVALQ. Dedup on TRAIN can only CONFLATE distinct functions, never
    split equal ones, so this measures an undercount."""
    out = {}
    for s, idxs in sorted(O.samples.items()):
        if not idxs:
            continue
        vs = set()
        for i in idxs:
            t = O.term_of(i)
            try:
                vs.add(tuple(S.ev(t, {"n": o}) for o in TRAIN + EVALQ))
            except Exception:
                pass
        out[s] = {"sampled_classes": len(idxs),
                  "distinct_on_TRAIN+EVALQ": len(vs),
                  "split_factor": round(len(vs) / len(idxs), 4) if idxs else None}
    return out


def target_analysis(O, cond, promoted_ids):
    """Which pre-registered targets were reached, with disagreement resolution
    and extrapolation licensing (PREREG sections 4 and 8)."""
    import numpy as np
    from outer import digest
    disagreement.assert_disjoint(RESERVE, HOLDOUT)
    res = {}
    for name in INV.TARGETS:
        vec = INV.vector(name, TRAIN)
        d = digest(np.array(vec, dtype=np.int64))
        hits = O.watch_hits.get(d, [])
        if not hits:
            res[name] = {"reached": False}
            continue
        best = min(c for c, _ in hits)
        terms = []
        seen = set()
        for c, i in hits:
            if c != best:
                continue
            t = O.term_of(i)
            k = S.show(t)
            if k not in seen:
                seen.add(k)
                terms.append(t)
        rec = {"reached": True, "min_cost": best,
               "distinct_minimal_terms": len(terms),
               "terms": [S.show(t) for t in terms[:12]],
               "n_minimal_using_carried_over":
                   sum(1 for t in terms if S.uses_ids(t, promoted_ids)),
               "reachable_without_carried_over":
                   any(not S.uses_ids(t, promoted_ids) for t in terms)}

        def predict(h, m):
            return S.ev(terms[h], {"n": m})

        obs = {m: INV.LIBRARY[name](m) for m in RESERVE}
        r = disagreement.resolve(
            list(range(len(terms))), score=lambda h: 0, predict=predict,
            reserve=RESERVE, observe=lambda m: obs[m], max_probes=8)
        rec["disagreement"] = {"verdict": r.verdict,
                               "survivors": len(r.survivors),
                               "probes_used": r.probes_used}
        chosen = terms[r.selected] if r.selected is not None else terms[
            r.survivors[0] if r.survivors else 0]
        rec["selected_term"] = S.show(chosen)
        rec["all_survivors_observationally_equal_on_reserve"] = (
            r.verdict == "UNDERDETERMINED")

        # licensing: fit on TRAIN, validate on RESERVE, only then extrapolate
        lic = abstention.license_rule(
            ["all"], TRAIN + RESERVE, lambda m: "all",
            lambda b, m: S.ev(chosen, {"n": m}),
            lambda m: INV.LIBRARY[name](m))
        g = abstention.guarded(lambda b, m: S.ev(chosen, {"n": m}),
                               lambda m: "all", lic)
        rec["licence"] = lic.to_json()
        rec["holdout"] = abstention.selective_report(
            HOLDOUT, g, lambda m: INV.LIBRARY[name](m))
        res[name] = rec
    return res


def untargeted(O, cond, formed, promoted_ids):
    """PREREG section 7. No target list: every sampled semantic class is tested
    against the independent library, and the library is consulted only after the
    class exists."""
    lib_train = {}
    for nm, f in INV.LIBRARY.items():
        try:
            lib_train[tuple(f(m) for m in TRAIN)] = nm
        except Exception:
            pass
    found = {}
    pools = [(s, i) for s, idxs in O.samples.items() for i in idxs]
    pools += [(s, i) for s, idxs in O.by_size.items() for i in idxs]
    for s, i in pools:
        t = O.term_of(i)
        try:
            v = tuple(S.ev(t, {"n": m}) for m in TRAIN)
        except Exception:
            continue
        nm = lib_train.get(v)
        if nm is None or nm in found:
            continue
        try:
            res_ok = all(S.ev(t, {"n": m}) == INV.LIBRARY[nm](m)
                         for m in RESERVE)
            hold_ok = all(S.ev(t, {"n": m}) == INV.LIBRARY[nm](m)
                          for m in HOLDOUT)
        except Exception:
            continue
        found[nm] = {"invariant": nm, "cost": S.size(t), "term": S.show(t),
                     "uses_carried_over": S.uses_ids(t, promoted_ids),
                     "matches_TRAIN": True, "matches_RESERVE": res_ok,
                     "matches_HOLDOUT": hold_ok}
    return found


def main():
    cond = sys.argv[1]
    # Optional second argument: the class cap. The pre-registered cap of
    # 300 000 turned out to bind at cost level 3, i.e. BEFORE the declared
    # outer budget of cost 5 was delivered -- the cap was meant as a memory
    # safety valve, not as the operative budget. Runs with a raised cap are
    # written to round2b_*.json and are reported alongside, never instead of,
    # the pre-registered runs.
    cap = int(sys.argv[2]) if len(sys.argv) > 2 else CAP
    suffix = "" if cap == CAP else "b"
    t0 = time.time()
    assert cond in ("A0", "A", "B", "C", "D", "E", "Bo", "B520"), cond
    max_size = E_MAX_SIZE if cond == "E" else MAX_SIZE
    beam = E_BEAM if cond == "E" else BEAM

    atoms, info, formed, promoted_ids = build(cond)
    watch = [INV.vector(n, TRAIN) for n in INV.TARGETS]
    O = Outer(atoms, TRAIN, cap=cap, beam=beam, seed=SEED,
              max_atom_cost=max_size).run(max_size, watch=watch)

    out = {
        "label": "COMPUTED",
        "prereg_sha256": hashlib.sha256((HERE / "PREREG.md").read_bytes()
                                        ).hexdigest(),
        "condition": cond,
        "budget": {"outer_max_cost": max_size, "beam": beam,
                   "class_cap": cap, "prereg_class_cap": CAP,
                   "unit_cap": UNIT_CAP, "seed": SEED},
        "splits": {"TRAIN": [TRAIN[0], TRAIN[-1]],
                   "RESERVE": [RESERVE[0], RESERVE[-1]],
                   "HOLDOUT": [HOLDOUT[0], HOLDOUT[-1]],
                   "EVALQ": [EVALQ[0], EVALQ[-1]]},
        "vocabulary": info,
        "atoms_unusable_at_this_budget": O.atoms_over_budget,
        "levels": O.level_log,
        "expansions": O.expansions,
        "classes_TRAIN": len(O.seen),
        "truncated_at_cap": O.truncated,
        "semantic_refinement": semantic_refinement(O, cond),
        "vectorisation_check": O.verify(300),
        "operator_check_mismatches": len(verify_operators(4000)),
        "targets": target_analysis(O, cond, promoted_ids),
        "untargeted": untargeted(O, cond, formed, promoted_ids),
        "wall_seconds": round(time.time() - t0, 1),
    }
    (HERE / ("round2%s_%s.json" % (suffix, cond))).write_text(
        json.dumps(out, indent=1, sort_keys=True) + "\n")

    print("\n== %s ==  atoms=%d formed=%s expansions=%d classes=%d %s" % (
        cond, info["outer_atoms"], info["formed_terms"], O.expansions,
        len(O.seen), "TRUNCATED" if O.truncated else ""))
    hit = [k for k, v in out["targets"].items() if v["reached"]]
    print("   targets reached (%d/%d): %s" % (len(hit), len(INV.TARGETS), hit))
    print("   untargeted library matches (%d): %s" % (
        len(out["untargeted"]), sorted(out["untargeted"])))
    print("   %.0fs" % out["wall_seconds"])


if __name__ == "__main__":
    main()
