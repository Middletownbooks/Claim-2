#!/usr/bin/env python3
"""
Cross-object experiment, run through the standard disagreement stage.

This supersedes the post-hoc extension in disagreement.py (Report K.5), which
resolved the lcm/max tie by probing m = 35 -- a HELD-OUT object. That answered
the question but spent holdout to do it.

Here the protocol is clean: training objects [1,30], a declared probe reserve
[49,60], and the final holdout [31,48], with `assert_disjoint` checking at
set-up that the reserve cannot touch the holdout. The tie must be resolved
using the reserve alone, so all 18 held-out objects stay virgin.
"""
import hashlib
import itertools
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "stages"))
from disagreement import assert_disjoint, resolve            # noqa: E402

from crossobject import (BASE_EXPRS, CONDS, K_TRAIN, M_TEST, M_TRAIN, OPS,
                         Oracle, coprime_splits, fit_period)  # noqa: E402

HERE = Path(__file__).resolve().parent
RESERVE = list(range(49, 61))
HOLDOUT = list(range(M_TRAIN + 1, M_TEST + 1))
K_FINAL = 140


def main():
    assert_disjoint(RESERVE, HOLDOUT)        # protocol check, before any query
    oracle = Oracle()

    observed = {}
    for m in range(1, M_TRAIN + 1):
        row = [oracle.truth(m, k) for k in range(1, K_TRAIN + 1)]
        observed[m] = fit_period(row)
    queries_after_training = oracle.calls

    # ---- stage 1: score the composition hypotheses on training objects ----
    def train_err(op):
        bad = tot = 0
        for m in sorted(observed):
            for a, b in coprime_splits(m):
                if observed.get(a) and observed.get(b) and observed.get(m):
                    tot += 1
                    bad += int(OPS[op](observed[a], observed[b]) != observed[m])
        return (bad, -tot)

    # ---- stage 2: DISAGREEMENT RESOLUTION (the standard stage) ----
    def predict_op(op, m):
        for a, b in coprime_splits(m):
            fa = observed.get(a)
            fb = observed.get(b)
            if fa and fb:
                return OPS[op](fa, fb)
        return None                      # no split from observed factors

    def observe_reserve(m):
        row = [oracle.truth(m, k) for k in range(1, K_TRAIN + 1)]
        p = fit_period(row)
        observed[m] = p                  # a probe is an observation, kept
        return p

    res = resolve(list(OPS), train_err, predict_op, RESERVE, observe_reserve,
                  max_probes=4)
    chosen = res.selected

    # ---- base case for objects with no coprime split ----
    atoms = [m for m in range(2, M_TRAIN + 1) if not coprime_splits(m)]
    best, best_err = None, None
    for combo in itertools.product(BASE_EXPRS, repeat=len(CONDS)):
        err = sum(
            int(BASE_EXPRS[e](n) != observed[n])
            for n in atoms
            for (cname, cond), e in [next(
                ((c, x) for c, x in zip(CONDS, combo) if c[1](n)))]
        )
        if best_err is None or err < best_err:
            best_err, best = err, combo

    def predict_f(m, known):
        if m in known:
            return known[m], "observed"
        for a, b in coprime_splits(m):
            fa, _ = predict_f(a, known)
            fb, _ = predict_f(b, known)
            if fa and fb:
                return OPS[chosen](fa, fb), "composed"
        for (cname, cond), e in zip(CONDS, best):
            if cond(m):
                return BASE_EXPRS[e](m), "base:" + e
        return None, "none"

    # ---- freeze before touching the holdout ----
    training_view = {k: v for k, v in observed.items()
                     if k <= M_TRAIN or k in RESERVE}
    predicted = {m: predict_f(m, training_view) for m in HOLDOUT}
    forecasts = [[m, k, bool(predicted[m][0] and (k - 1) % predicted[m][0] == 0)]
                 for m in HOLDOUT for k in range(1, K_FINAL + 1)]
    fhash = hashlib.sha256(
        json.dumps(forecasts, separators=(",", ":")).encode()).hexdigest()
    (HERE / "freeze_v2.json").write_text(json.dumps({
        "reserve": RESERVE, "holdout": HOLDOUT,
        "disagreement_stage": res.to_json(),
        "chosen_composition_op": chosen,
        "base_rule": [{"condition": c[0], "value": e}
                      for c, e in zip(CONDS, best)],
        "predicted_invariants": {m: predicted[m][0] for m in HOLDOUT},
        "forecast_hash": fhash,
        "queries_before_holdout": oracle.calls,
    }, indent=1, sort_keys=True))

    # ---- score on the untouched holdout ----
    correct = total = exact = 0
    per_object = {}
    true_count = 0
    for m in HOLDOUT:
        v, how = predicted[m]
        row = [oracle.truth(m, k) for k in range(1, K_FINAL + 1)]
        true_count += sum(row)
        c = sum(int(bool(v and (k - 1) % v == 0) == row[k - 1])
                for k in range(1, K_FINAL + 1))
        actual = fit_period(row)
        per_object[m] = {"route": how, "f_pred": v, "f_obs": actual,
                         "exact": v == actual, "accuracy": round(c / len(row), 4)}
        exact += int(v == actual)
        correct += c
        total += len(row)
    oracle.close()

    out = {
        "label": "COMPUTED",
        "protocol": "training [1,30]; probe reserve [49,60]; holdout [31,48]",
        "holdout_untouched_until_freeze": True,
        "disagreement_stage": res.to_json(),
        "chosen_composition_op": chosen,
        "probes_used": res.probes_used,
        "probe_objects": sorted(res.observations),
        "invariants_exact": "%d/%d" % (exact, len(HOLDOUT)),
        "end_to_end_accuracy": round(correct / total, 5),
        "majority_class_baseline": round(1 - true_count / total, 5),
        "oracle_queries_total": oracle.calls,
        "queries_after_training": queries_after_training,
        "forecast_hash": fhash,
        "per_object": per_object,
    }
    (HERE / "result_v2.json").write_text(json.dumps(out, indent=1,
                                                    sort_keys=True))
    print(json.dumps({k: v for k, v in out.items()
                      if k not in ("per_object", "disagreement_stage")},
                     indent=2))
    print("\ndisagreement stage rounds:")
    for r in res.rounds:
        print("  survivors=%s probe=%s observed=%s -> %s" % (
            r["survivors"], r.get("probe"), r.get("observed"),
            r.get("survivors_after")))
    wrong = [m for m, v in per_object.items() if not v["exact"]]
    print("\nobjects with a wrong invariant:", wrong or "none")


if __name__ == "__main__":
    main()
