#!/usr/bin/env python3
"""
Q5 -- the blind cross-board transport experiment, FLT -> NS.

PROTOCOL

  Phase A, source-visible.  Candidates are generated from FLT alone by a rule
    that cannot see NS: a theorem whose STATEMENT uses only mathlib vocabulary
    and none of FLT's own 1450 definition modules. Such a theorem is by
    construction sayable on any board that speaks mathlib. The rule is the
    "upstreamable" criterion computed in the previous phase; it was fixed
    before this experiment and is not tuned here.

  Phase B, target-blind.  No re-ranking against NS. The whole candidate set is
    carried over, so there is no opportunity to select for the answer.

  Phase C, target application.  Each NS statement is matched against the
    candidate pool by signature Jaccard, and the same measurement is repeated
    against five control pools.

WHAT WOULD FALSIFY THE TRANSPORT HYPOTHESIS

  If NS's own statements (control B) match NS statements at least as well as
  FLT's candidates do, then FLT carries nothing NS did not already have, and
  the correct reading is that the boards are not connected at a level that
  matters. That is the outcome this design is built to be able to report.
"""
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent
SEED = 20260909


def jac(a, b):
    if not a or not b:
        return 0.0
    i = len(a & b)
    return i / (len(a) + len(b) - i)


class Index:
    """Inverted index over signature tokens; only pool entries sharing a token
    with the query are ever scored."""

    def __init__(self, pool):
        self.pool = pool
        self.sets = [set(e["sig"]) for e in pool]
        self.inv = defaultdict(list)
        for i, s in enumerate(self.sets):
            for t in s:
                self.inv[t].append(i)

    def best(self, sig, exclude_file=None):
        q = set(sig)
        cand = Counter()
        for t in q:
            for i in self.inv.get(t, ()):
                cand[i] += 1
        best, bi = 0.0, None
        for i, _ in cand.most_common(400):
            if exclude_file and self.pool[i]["file"] == exclude_file:
                continue
            v = jac(q, self.sets[i])
            if v > best:
                best, bi = v, i
        return best, (self.pool[bi] if bi is not None else None)


def summarize(name, scores):
    scores = sorted(scores, reverse=True)
    n = len(scores)
    return {
        "pool": name, "n_ns_statements": n,
        "mean_best_jaccard": round(sum(scores) / n, 4) if n else 0,
        "median": round(scores[n // 2], 4) if n else 0,
        "ge_0.3": sum(1 for s in scores if s >= .3),
        "ge_0.5": sum(1 for s in scores if s >= .5),
        "ge_0.7": sum(1 for s in scores if s >= .7),
        "ge_0.9": sum(1 for s in scores if s >= .9),
    }


def main():
    rng = random.Random(SEED)
    ns = json.load(open(OUT / "stmts_ns.json"))
    flt = json.load(open(OUT / "stmts_flt.json"))
    up = set(json.loads((OUT.parent / "flt" / "upstreamable.json").read_text()
                        )["self_contained"])
    contact = set(json.loads((OUT / "contact_files.json").read_text()))

    by_name = {e["name"]: e for e in flt}
    # Phase A: the target-blind candidate pool
    # `upstreamable.json` keys are the Thm_<key>.lean stems
    upfiles = {"Theorems/Thm_%s.lean" % u for u in up}
    cands = [e for e in flt if e["file"] in upfiles]
    print("candidate pool (FLT, mathlib-vocabulary-only): %d" % len(cands))

    k = len(cands)
    pools = {
        "TRANSPORT_flt_upstreamable": cands,
        "CONTROL_C_random_flt": rng.sample(flt, min(k, len(flt))),
        "CONTROL_E_architecture_contact": [e for e in flt
                                           if e["file"] in contact] or
                                          rng.sample(flt, 200),
        "CONTROL_B_ns_itself": ns,
    }
    # Control D: FLT's most-cited theorems
    cites = Counter()
    try:
        g = json.loads((OUT.parent / "flt" / "flt_graph.json").read_text())
        edges = g.get("edges") or g.get("citations") or {}
        if isinstance(edges, dict):
            for _, vs in edges.items():
                cites.update(vs)
        else:
            for a, b in edges:
                cites[b] += 1
    except Exception as e:
        print("citation graph unavailable:", e)
    if cites:
        top = {n for n, _ in cites.most_common(k)}
        pools["CONTROL_D_most_cited_flt"] = [e for e in flt if e["name"] in top]
    # Control A: generic-mathlib-only candidates (vocabulary that FLT uses
    # everywhere, i.e. nothing board-specific)
    fltuse = Counter()
    for e in flt:
        fltuse.update(e["sig"])
    generic = {t for t, c in fltuse.items() if c >= 500}
    pools["CONTROL_A_generic_mathlib"] = [
        e for e in flt if e["sig"] and set(e["sig"]) <= generic][:k] or []

    rows = []
    detail = {}
    for name, pool in pools.items():
        if not pool:
            print("pool %s empty, skipped" % name)
            continue
        idx = Index(pool)
        scores, best_examples = [], []
        for e in ns:
            s, hit = idx.best(e["sig"],
                              exclude_file=e["file"] if name ==
                              "CONTROL_B_ns_itself" else None)
            scores.append(s)
            if hit is not None and s >= .7:
                best_examples.append({"ns": e["name"], "ns_file": e["file"],
                                      "match": hit["name"], "jaccard": round(s, 3),
                                      "shared": sorted(set(e["sig"]) &
                                                       set(hit["sig"]))[:8]})
        r = summarize(name, scores)
        r["pool_size"] = len(pool)
        rows.append(r)
        detail[name] = best_examples[:40]
        print("%-34s pool=%-6d mean=%.4f  >=.3:%-5d >=.5:%-5d >=.7:%-4d >=.9:%d"
              % (name, len(pool), r["mean_best_jaccard"], r["ge_0.3"],
                 r["ge_0.5"], r["ge_0.7"], r["ge_0.9"]), flush=True)

    json.dump({"label": "EXPERIMENTAL_RESULT", "seed": SEED,
               "direction": "FLT -> NS", "rows": rows,
               "high_matches": detail},
              open(OUT / "transport_flt_to_ns.json", "w"), indent=1)


if __name__ == "__main__":
    main()
