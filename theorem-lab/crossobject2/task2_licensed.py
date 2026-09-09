#!/usr/bin/env python3
"""
Task 2 re-run with the extrapolation-licensing stage in place.

Nothing else changes: same transferred (wrong-shaped) grammar, same resolved
composition law `max`, same training objects, same holdout. The only difference
is that base-case branches which cannot reproduce their own training data now
abstain instead of extrapolating.
"""
import importlib.util as ilu
import itertools
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "crossobject"))


def _load(name, path):
    spec = ilu.spec_from_file_location(name, path)
    mod = ilu.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


ab = _load("lab_stage_abstention", HERE.parent / "stages" / "abstention.py")
from crossobject import BASE_EXPRS, CONDS, OPS, coprime_splits   # noqa: E402
from task2 import EOracle, HOLDOUT, M_TRAIN, R_MAX, fit_base     # noqa: E402


def main():
    oracle = EOracle()
    observed = {m: oracle.threshold(m) for m in range(1, M_TRAIN + 1)}
    truth = {m: oracle.threshold(m) for m in HOLDOUT}
    oracle.close()

    atoms = [m for m in range(2, M_TRAIN + 1) if not coprime_splits(m)]
    combo, err = fit_base(atoms, observed)
    branch_names = [c[0] for c in CONDS]
    expr_of = dict(zip(branch_names, combo))

    def branch_of(n):
        for cname, cond in CONDS:
            if cond(n):
                return cname
        return None

    def base_predict(branch, n):
        return BASE_EXPRS[expr_of[branch]](n)

    licence = ab.license_rule(branch_names, atoms, branch_of, base_predict,
                              observed.get)
    guarded_base = ab.guarded(base_predict, branch_of, licence)

    def predict_t(m, known):
        if m in known:
            return known[m], "observed"
        for a, b in coprime_splits(m):
            fa, _ = predict_t(a, known)
            fb, _ = predict_t(b, known)
            if fa is not None and fb is not None:
                return OPS["max"](fa, fb), "composed"
        v = guarded_base(m)
        return v, ("base:" + expr_of[branch_of(m)] if v is not None
                   else "ABSTAIN")

    preds = {m: predict_t(m, observed) for m in HOLDOUT}

    def invariant_pred(m):
        return preds[m][0]

    inv = ab.selective_report(HOLDOUT, invariant_pred, truth.get)

    pts = [(m, r) for m in HOLDOUT for r in range(1, R_MAX + 1)]

    def marginal_pred(pt):
        m, r = pt
        v = preds[m][0]
        return None if v is None else (r >= v)

    e2e = ab.selective_report(pts, marginal_pred,
                              lambda pt: pt[1] >= truth[pt[0]])

    out = {
        "label": "COMPUTED",
        "change_from_task2": "extrapolation licensing applied to the base rule",
        "base_rule": [{"cond": c, "value": expr_of[c]} for c in branch_names],
        "base_training_errors": err,
        "licence": licence.to_json(),
        "invariant_level": inv,
        "end_to_end_level": e2e,
        "majority_class_baseline": 0.91667,
        "task2_without_licensing": {
            "invariants_exact": "12/18",
            "end_to_end_accuracy": 0.71528,
            "note": "confidently wrong, below the 0.91667 baseline",
        },
        "per_object": {m: {"route": preds[m][1], "pred": preds[m][0],
                           "obs": truth[m]} for m in HOLDOUT},
    }
    (HERE / "result_licensed.json").write_text(
        json.dumps(out, indent=1, sort_keys=True))
    print(json.dumps({k: v for k, v in out.items()
                      if k not in ("per_object", "licence")}, indent=2))
    print("\nbranch licences:")
    for b in licence.to_json()["branches"]:
        print("  %-14s %-22s covered=%d errors=%d" % (
            b["branch"], b["verdict"], b["covered"], b["errors"]))
    print("\nheld-out objects:")
    for m in HOLDOUT:
        r = out["per_object"][m]
        print("  m=%2d %-12s pred=%-5s obs=%s" % (
            m, r["route"], r["pred"], r["obs"]))


if __name__ == "__main__":
    main()
