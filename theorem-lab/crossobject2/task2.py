#!/usr/bin/env python3
"""
Cross-object task 2: the E-family r-threshold, whose law is `max`, not `lcm`,
and whose prime-power base case is the exponent. See PREREG.md.

The hypothesis language is imported unchanged from the lambda task: same eight
composition operators, same base grammar, same conditions, same disagreement
stage. Nothing is re-tuned.
"""
import hashlib
import itertools
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAB = HERE.parent / "lab.py"
sys.path.insert(0, str(HERE.parent / "crossobject"))
# Load the STAGE by explicit path so that no sibling module can shadow it.
import importlib.util as _ilu                                # noqa: E402
_spec = _ilu.spec_from_file_location(
    "lab_stage_disagreement", HERE.parent / "stages" / "disagreement.py")
_stage = _ilu.module_from_spec(_spec)
sys.modules[_spec.name] = _stage      # dataclasses need the module registered
_spec.loader.exec_module(_stage)
assert_disjoint, resolve = _stage.assert_disjoint, _stage.resolve
from crossobject import BASE_EXPRS, CONDS, OPS, coprime_splits  # noqa: E402

M_TRAIN, M_TEST = 30, 48
R_MAX, D_MAX = 8, 84
HOLDOUT = list(range(M_TRAIN + 1, M_TEST + 1))


class EOracle:
    def __init__(self):
        self.proc = subprocess.Popen(
            [sys.executable, str(LAB), "--worker", "--oracle", "real"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True,
            bufsize=1)
        self.calls = 0

    def truth(self, m, r, d):
        req = {"family": "E", "coord": [m, r, d], "op": "full"}
        self.proc.stdin.write(json.dumps(req, separators=(",", ":")) + "\n")
        self.proc.stdin.flush()
        self.calls += 1
        return json.loads(self.proc.stdout.readline())["truth"]

    def reachable(self, m, r):
        """Is there any d <= D_MAX with E(m,r,d)?  (= r >= nu(m))"""
        for d in range(1, D_MAX + 1):
            if self.truth(m, r, d):
                return True
        return False

    def threshold(self, m):
        for r in range(1, R_MAX + 1):
            if self.reachable(m, r):
                return r
        return None

    def close(self):
        self.proc.stdin.close()
        self.proc.wait()


def fit_base(atoms, observed, exprs=BASE_EXPRS):
    best, best_err = None, None
    for combo in itertools.product(exprs, repeat=len(CONDS)):
        err = 0
        for n in atoms:
            for (cname, cond), e in zip(CONDS, combo):
                if cond(n):
                    err += int(exprs[e](n) != observed[n])
                    break
        if best_err is None or err < best_err:
            best_err, best = err, combo
    return best, best_err


def run_arm(name, reserve, oracle, observed, base_exprs=BASE_EXPRS):
    assert_disjoint(reserve, HOLDOUT)

    def train_err(op):
        bad = tot = 0
        for m in sorted(k for k in observed if k <= M_TRAIN):
            for a, b in coprime_splits(m):
                if observed.get(a) and observed.get(b) and observed.get(m):
                    tot += 1
                    bad += int(OPS[op](observed[a], observed[b]) != observed[m])
        return (bad, -tot)

    def predict_op(op, m):
        for a, b in coprime_splits(m):
            fa, fb = observed.get(a), observed.get(b)
            if fa and fb:
                return OPS[op](fa, fb)
        return None

    def observe_reserve(m):
        t = oracle.threshold(m)
        observed[m] = t
        return t

    res = resolve(list(OPS), train_err, predict_op, reserve, observe_reserve,
                  max_probes=4)
    return res


def main():
    oracle = EOracle()
    observed = {}
    for m in range(1, M_TRAIN + 1):
        observed[m] = oracle.threshold(m)
    queries_training = oracle.calls

    arms = {}
    # Arm A first: its probes (if any) are legitimate observations either way.
    resA = run_arm("A", list(range(49, 72)), oracle, observed)
    arms["A_short_reserve_49_71"] = resA.to_json()
    resB = run_arm("B", list(range(49, 81)), oracle, observed)
    arms["B_long_reserve_49_80"] = resB.to_json()

    chosen = resB.selected or (resA.selected)
    atoms = [m for m in range(2, M_TRAIN + 1) if not coprime_splits(m)]
    base, base_err = fit_base(atoms, observed)

    def predict_t(m, known):
        if m in known:
            return known[m], "observed"
        for a, b in coprime_splits(m):
            fa, _ = predict_t(a, known)
            fb, _ = predict_t(b, known)
            if fa and fb:
                return OPS[chosen](fa, fb), "composed"
        for (cname, cond), e in zip(CONDS, base):
            if cond(m):
                return base_exprs_value(e, m), "base:" + e
        return None, "none"

    def base_exprs_value(e, m):
        return BASE_EXPRS[e](m)

    known = {k: v for k, v in observed.items() if k <= M_TRAIN or k >= 49}
    predicted = {m: predict_t(m, known) for m in HOLDOUT}
    forecasts = [[m, r, bool(predicted[m][0] and r >= predicted[m][0])]
                 for m in HOLDOUT for r in range(1, R_MAX + 1)]
    fhash = hashlib.sha256(
        json.dumps(forecasts, separators=(",", ":")).encode()).hexdigest()
    (HERE / "freeze.json").write_text(json.dumps({
        "arms": arms, "chosen_op": chosen,
        "base_rule": [{"cond": c[0], "value": e} for c, e in zip(CONDS, base)],
        "base_training_errors": base_err,
        "predicted_thresholds": {m: predicted[m][0] for m in HOLDOUT},
        "forecast_hash": fhash,
        "queries_before_holdout": oracle.calls,
    }, indent=1, sort_keys=True))

    # ---- score on the untouched holdout ----
    correct = total = exact = 0
    true_count = 0
    per_object = {}
    for m in HOLDOUT:
        v, how = predicted[m]
        actual = oracle.threshold(m)
        c = 0
        for r in range(1, R_MAX + 1):
            obs = r >= actual
            true_count += int(obs)
            c += int(bool(v and r >= v) == obs)
        per_object[m] = {"route": how, "t_pred": v, "t_obs": actual,
                         "exact": v == actual, "accuracy": round(c / R_MAX, 4)}
        exact += int(v == actual)
        correct += c
        total += R_MAX
    oracle.close()

    comp = [m for m, x in per_object.items() if x["route"] == "composed"]
    non = [m for m, x in per_object.items() if x["route"].startswith("base")]
    out = {
        "label": "COMPUTED",
        "task": "E-family r-threshold; true law is max, base case is the exponent",
        "language": "unchanged from the lambda task",
        "arms": arms,
        "chosen_op": chosen,
        "base_rule": [{"cond": c[0], "value": e} for c, e in zip(CONDS, base)],
        "base_training_errors": base_err,
        "invariants_exact": "%d/%d" % (exact, len(HOLDOUT)),
        "exact_composable": "%d/%d" % (
            sum(1 for m in comp if per_object[m]["exact"]), len(comp)),
        "exact_non_composable": "%d/%d" % (
            sum(1 for m in non if per_object[m]["exact"]), len(non)),
        "end_to_end_accuracy": round(correct / total, 5),
        "majority_class_baseline": round(
            max(true_count, total - true_count) / total, 5),
        "oracle_queries": oracle.calls,
        "queries_training": queries_training,
        "forecast_hash": fhash,
        "per_object": per_object,
    }
    (HERE / "result.json").write_text(json.dumps(out, indent=1, sort_keys=True))
    print(json.dumps({k: v for k, v in out.items()
                      if k not in ("per_object", "arms")}, indent=2))
    for nm, a in arms.items():
        print("\narm %s: verdict=%s selected=%s probes=%s survivors=%s" % (
            nm, a["verdict"], a["selected"], a["probes_used"], a["survivors"]))
    print("\nper held-out object:")
    for m in sorted(per_object):
        x = per_object[m]
        print("  m=%2d %-16s t_pred=%-5s t_obs=%-3s %s" % (
            m, x["route"], x["t_pred"], x["t_obs"],
            "EXACT" if x["exact"] else "wrong"))


if __name__ == "__main__":
    main()
