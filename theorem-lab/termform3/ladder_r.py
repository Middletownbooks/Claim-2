#!/usr/bin/env python3
"""
Report R — the compounding ladder. `python3 ladder_r.py [max_rungs]`.

Follows PREREG_R.md (sha256 in PREREG_R.sha256), committed before this file was
written. Every rung is an unbeamed, exhaustive cost-<=5 outer search at body
budget 3 with unit cap 40 plus the carried atoms, which is Report Q's A3u/B3u
configuration -- so rungs 0 and 1 must reproduce those numbers exactly, and R-1
checks that they do.

Each rung carries `promote(certified set of the previous rung)` under the frozen
rule, and classifies every carried term as a REACH EXTENSION (the receiving round
cannot produce it within its budget at all) or a COST COMPRESSION (it can, at cost
c > 1, and carrying makes it 1). The ladder stops at a fixpoint in the NET-NEW
certified set -- invariants equal to a carried atom do not count as discovery.
"""
import json
import random
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
T2 = HERE.parent / "termform2"
sys.path.insert(0, str(HERE.parent / "termform"))
sys.path.insert(0, str(T2))
sys.path.insert(0, str(HERE.parent))

import invariants as INV                                     # noqa: E402
import synth3 as S                                           # noqa: E402
from outer import Outer, digest                              # noqa: E402
from promote import named_units, parse                       # noqa: E402
from round2 import HOLDOUT, RESERVE, TRAIN                   # noqa: E402
from stages import disagreement                              # noqa: E402

import numpy as np                                           # noqa: E402

# Formation at ladder depth nests units inside units; the reference evaluator walks
# those definitions, so the default limit of 1000 frames is not generous here.
sys.setrecursionlimit(20000)

BODY, COST, UNITS, BEAM = 3, 5, 40, 10 ** 9
SEED = 20260919
LIB_VEC = {}
for _n, _f in INV.LIBRARY.items():
    try:
        LIB_VEC[_n] = tuple(_f(m) for m in TRAIN)
    except Exception:
        pass


def promote_from(certified):
    """The frozen rule, applied to a rung's certified set: every certified term,
    plus every formed term appearing as a named unit inside one."""
    out, seen = [], set()

    def add(printed):
        t = parse(printed)
        if repr(t) in seen:
            return
        seen.add(repr(t))
        out.append((printed, t))

    for rec in certified.values():
        add(rec["term"])
    for rec in certified.values():
        for u in named_units(rec["term"]):
            add(u)
    return out


def run_rung(carried, tag, note=""):
    """One rung: build atoms, exhaust the cost-5 space, certify."""
    S.reset()
    forced = [S.leaf(t, TRAIN, cost=1) for _, t in carried]
    formed = S.form_leaves(TRAIN, size1=BODY, size2=BODY, extra_leaves=forced,
                           verbose=False, tag=tag)
    units = S.select_units(formed, TRAIN, UNITS + len(forced), forced_leaves=forced)
    atoms = [("var", "n")] + [("const", c) for c in S.CONSTS] + units
    carried_ids = {u[1] for u in forced}
    carried_vec = {}
    for u in forced:
        try:
            carried_vec[tuple(S.ev(u, {"n": m}) for m in TRAIN)] = S.show(u)
        except Exception:
            pass
    O = Outer(atoms, TRAIN, cap=20000000, beam=BEAM, seed=SEED,
              max_atom_cost=COST).run(COST, watch=list(LIB_VEC.values()))
    cert = {}
    for name, vec in LIB_VEC.items():
        hits = O.watch_hits.get(digest(np.array(vec, dtype=np.int64))) or []
        if not hits:
            continue
        best = min(c for c, _ in hits)
        terms, seen = [], set()
        for c, i in hits:
            if c == best:
                t = O.term_of(i)
                if S.show(t) not in seen:
                    seen.add(S.show(t))
                    terms.append(t)
        f = INV.LIBRARY[name]
        try:
            if not all(S.ev(terms[0], {"n": m}) == f(m) for m in RESERVE + HOLDOUT):
                continue
        except Exception:
            continue
        cert[name] = {"cost": best, "term": S.show(terms[0]),
                      "distinct_minimal_terms": len(terms),
                      "uses_carried": bool(S.uses_ids(terms[0], carried_ids)),
                      "reachable_without_carried":
                          any(not S.uses_ids(t, carried_ids) for t in terms),
                      "is_a_carried_atom": vec in carried_vec}
    return {"tag": tag, "note": note, "atoms": len(atoms), "carried": len(forced),
            "formed": len(formed), "classes": len(O.seen),
            "expansions": O.expansions, "exhausted": not O.truncated,
            "certified": cert, "certified_count": len(cert),
            "net_new": sorted(k for k, v in cert.items() if not v["is_a_carried_atom"]),
            "carried_terms": [S.show(u) for u in forced]}, O, carried_vec


def classify(carried, prev_rung):
    """REACH EXTENSION or COST COMPRESSION, per carried term, against the
    PREVIOUS rung's exhausted enumeration."""
    out = []
    prev_costs = {}
    for name, rec in (prev_rung or {}).get("certified", {}).items():
        prev_costs[name] = rec["cost"]
    prev_classes = set((prev_rung or {}).get("_class_digests", []))
    for printed, t in carried:
        try:
            v = tuple(S.ev(t, {"n": m}) for m in TRAIN)
        except Exception:
            out.append({"term": printed, "kind": "UNEVALUABLE"})
            continue
        d = digest(np.array(v, dtype=np.int64)).hex()
        name = next((n for n, vv in LIB_VEC.items() if vv == v), None)
        if d in prev_classes:
            c = prev_costs.get(name)
            out.append({"term": printed, "kind": "COST COMPRESSION",
                        "previous_min_cost": c, "invariant": name})
        else:
            out.append({"term": printed, "kind": "REACH EXTENSION", "invariant": name})
    return out


def random_control(n, exclude_vectors, tag):
    """The same number of carried terms, drawn from the body-budget-5 formation
    pool with a fixed seed, excluding anything semantically equal to a real one."""
    S.reset()
    formed = S.form_leaves(TRAIN, size1=3, size2=5, verbose=False, tag=tag + "pool")
    cand = [(v, t) for v, t in formed.items() if v not in exclude_vectors]
    random.Random(SEED).shuffle(cand)
    # Return SELF-CONTAINED terms. A term from this pool carries leaf ids into which
    # `run_rung`'s `S.reset()` then re-registers different definitions, and a leaf
    # whose definition contains a leaf that now contains it evaluates forever. That
    # is what killed the first seeded run with a RecursionError at rung 1's random
    # control; round3.py had already been bitten by the same class of bug. Parsing
    # the printed form expands every unit, so nothing survives the reset but syntax.
    return [(S.show(t), parse(S.show(t))) for _, t in cand[:n]]


def seed_carried():
    """Report Q's rung-1 vocabulary: the seven terms CERTIFIED out of reach at body
    budget 3, promoted from a round whose body budget was 5.

    The unseeded ladder cannot reproduce it, and that is the finding rather than a
    bug: promote(a rung's own certified set) is in-reach BY CONSTRUCTION, because
    the rung found those terms itself. New out-of-reach structure has to come from
    a round with a different reach -- which is Report P's point, restated as a
    property of the ladder."""
    cert = json.loads((HERE / "certificate.json").read_text())
    return [(t, parse(t)) for t in cert["certified_out_of_reach"]]


def main():
    seeded = "seeded" in sys.argv[1:]
    args = [a for a in sys.argv[1:] if a != "seeded"]
    max_rungs = int(args[0]) if args else 5
    disagreement.assert_disjoint(RESERVE, HOLDOUT)
    t0 = time.time()
    rungs, carried = [], []
    prev = None
    for k in range(max_rungs + 1):
        cls = classify(carried, prev) if carried else []
        r, O, carried_vec = run_rung(carried, "R%d" % k,
                                     "carry promote(certified of rung %d)" % (k - 1)
                                     if k else "carry nothing")
        r["rung"] = k
        r["carried_classification"] = cls
        r["_class_digests"] = [d.hex() for d in O.seen]
        prev_net = set(rungs[-1]["net_new"]) if rungs else set()
        r["newly_net_new"] = sorted(set(r["net_new"]) - prev_net)
        r["lost"] = sorted(prev_net - set(r["net_new"]))
        rungs.append(r)
        print("rung %d: %d atoms (%d carried), %d classes, exhausted=%s, "
              "certified %d, net new %d, NEW %s (%.0fs)"
              % (k, r["atoms"], r["carried"], r["classes"], r["exhausted"],
                 r["certified_count"], len(r["net_new"]), r["newly_net_new"],
                 time.time() - t0), flush=True)

        if k and not r["newly_net_new"]:
            print("  FIXPOINT: no net-new invariant beyond rung %d" % (k - 1), flush=True)
            break
        if k == max_rungs:
            break
        if seeded and k == 0:
            prev = r
            carried = seed_carried()
            continue
        # controls, run only at a rung that moved
        if k >= 1 and r["newly_net_new"]:
            excl = set()
            for _, t in carried:
                try:
                    excl.add(tuple(S.ev(t, {"n": m}) for m in TRAIN))
                except Exception:
                    pass
            rc = random_control(len(carried), excl, "rc%d" % k)
            rr, _, _ = run_rung(rc, "R%drand" % k, "random control for rung %d" % k)
            r["random_control"] = {"certified": rr["certified_count"],
                                   "net_new": len(rr["net_new"]),
                                   "net_new_list": rr["net_new"]}
            print("   random control: certified %d, net new %d"
                  % (rr["certified_count"], len(rr["net_new"])), flush=True)
        prev = r
        carried = promote_from(r["certified"])

    for r in rungs:
        r.pop("_class_digests", None)
    out = {"label": "LADDER_R_SEEDED" if seeded else "LADDER_R",
           "seeded": seeded, "prereg_sha256": (HERE / "PREREG_R.sha256").read_text().strip(),
           "config": {"body_budget": BODY, "outer_cost": COST, "unit_cap": UNITS,
                      "beam": "off (exhaustive)", "seed": SEED},
           "rungs": rungs, "wall_seconds": round(time.time() - t0, 1)}
    (HERE / ("ladder_r_seeded.json" if seeded else "ladder_r.json")).write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print("\nladder: %s" % " -> ".join(str(len(r["net_new"])) for r in rungs))


if __name__ == "__main__":
    main()
