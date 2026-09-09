#!/usr/bin/env python3
"""
Post-hoc extension (NOT pre-registered): can the learner detect that its own
training data under-determines the composition law, and resolve it with a
targeted query?

The main run found `lcm` and `max` both perfect on training (30/30) and the
tie-break chose `max`, which is wrong at m = 35 and m = 45. That is an
under-determination, and under-determination is detectable WITHOUT the answer:
two surviving hypotheses disagree on a specific, nameable object.

Procedure: keep every op tied for best on training; find the smallest object
not yet observed on which the survivors disagree; query that one object; repeat
until one hypothesis remains or no disagreement is findable. Count the queries.
"""
import json
import math
import subprocess
import sys
from pathlib import Path

from crossobject import (K_TRAIN, M_TEST, M_TRAIN, OPS, Oracle,
                         coprime_splits, fit_period)

HERE = Path(__file__).resolve().parent


def main():
    oracle = Oracle()
    observed = {}
    for m in range(1, M_TRAIN + 1):
        row = [oracle.truth(m, k) for k in range(1, K_TRAIN + 1)]
        observed[m] = fit_period(row)
    base_queries = oracle.calls

    def train_score(op):
        ok = tot = 0
        for m in sorted(observed):
            for a, b in coprime_splits(m):
                if observed.get(a) and observed.get(b) and observed.get(m):
                    tot += 1
                    ok += int(OPS[op](observed[a], observed[b]) == observed[m])
        return ok, tot

    rounds = []
    survivors = None
    for _ in range(6):
        scored = {op: train_score(op) for op in OPS}
        best = max(s[0] / s[1] for s in scored.values() if s[1])
        survivors = sorted(op for op, s in scored.items()
                           if s[1] and s[0] / s[1] == best)
        rounds.append({"survivors": survivors,
                       "training_accuracy": round(best, 4),
                       "objects_observed": len(observed)})
        if len(survivors) <= 1:
            break
        # find the smallest UNOBSERVED object where survivors disagree
        probe = None
        for m in range(2, M_TEST + 1):
            if m in observed:
                continue
            vals = set()
            for op in survivors:
                for a, b in coprime_splits(m):
                    if observed.get(a) and observed.get(b):
                        vals.add(OPS[op](observed[a], observed[b]))
                        break
            if len(vals) > 1:
                probe = m
                break
        if probe is None:
            rounds[-1]["probe"] = None
            break
        rounds[-1]["probe"] = probe
        row = [oracle.truth(probe, k) for k in range(1, K_TRAIN + 1)]
        observed[probe] = fit_period(row)
        rounds[-1]["probe_period_observed"] = observed[probe]

    chosen = survivors[0] if survivors else None

    # re-forecast the ORIGINAL held-out set with the resolved law
    def predict_f(m, known):
        if m in known:
            return known[m], "observed"
        for a, b in coprime_splits(m):
            fa, _ = predict_f(a, known)
            fb, _ = predict_f(b, known)
            if fa and fb:
                return OPS[chosen](fa, fb), "composed"
        return None, "base-not-used-here"

    main_res = json.loads((HERE / "result.json").read_text())
    base_rule = {r["condition"]: r["value"] for r in main_res["base_rule"]}
    from crossobject import BASE_EXPRS, CONDS

    def predict_full(m, known):
        v, how = predict_f(m, known)
        if v:
            return v, how
        for cname, cond in CONDS:
            if cond(m):
                return BASE_EXPRS[base_rule[cname]](m), "base"
        return None, "none"

    correct = total = 0
    per_object = {}
    for m in range(M_TRAIN + 1, M_TEST + 1):
        if m in observed and m > M_TRAIN:
            pass  # a probed object is no longer held out; scored separately
        v, how = predict_full(m, {k: x for k, x in observed.items()
                                  if k <= M_TRAIN or k == m})
        c = t = 0
        actual = None
        row = []
        for k in range(1, 141):
            truth = oracle.truth(m, k)
            row.append(truth)
            c += int(bool(v and (k - 1) % v == 0) == truth)
            t += 1
        actual = fit_period(row)
        per_object[m] = {"route": how, "f_pred": v, "f_obs": actual,
                         "exact": v == actual, "accuracy": round(c / t, 4),
                         "was_probed": m in observed and m > M_TRAIN}
        correct += c
        total += t
    oracle.close()

    scored_unprobed = [m for m, v in per_object.items() if not v["was_probed"]]
    out = {
        "label": "POST-HOC EXTENSION, not pre-registered",
        "rounds": rounds,
        "resolved_op": chosen,
        "extra_objects_queried": len(observed) - M_TRAIN,
        "extra_oracle_queries": oracle.calls - base_queries
        - 140 * (M_TEST - M_TRAIN),
        "invariant_exact_all_18": sum(1 for v in per_object.values()
                                      if v["exact"]),
        "invariant_exact_excluding_probed": sum(
            1 for m in scored_unprobed if per_object[m]["exact"]),
        "held_out_excluding_probed": len(scored_unprobed),
        "end_to_end_accuracy_all_18": round(correct / total, 5),
        "per_object": per_object,
    }
    (HERE / "disagreement.json").write_text(json.dumps(out, indent=1,
                                                       sort_keys=True))
    print(json.dumps({k: v for k, v in out.items() if k != "per_object"},
                     indent=2))
    print("\nobjects that were wrong in the main run:")
    for m in (35, 45):
        v = per_object[m]
        print("  m=%2d %-10s f_pred=%-4s f_obs=%-4s %s probed=%s" % (
            m, v["route"], v["f_pred"], v["f_obs"],
            "EXACT" if v["exact"] else "wrong", v["was_probed"]))


if __name__ == "__main__":
    main()
