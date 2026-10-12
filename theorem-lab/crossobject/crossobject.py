#!/usr/bin/env python3
"""
Cross-object holdout experiment. See PREREG.md.

The learner observes the U-family oracle for training objects only, fits a
per-object invariant (the row period), then searches a declared language for a
LAW RELATING OBJECTS, freezes forecasts for unseen objects, and only then are
the held-out oracle answers read.

Nothing here imports audit/numbertheory.py: the answer key (lambda, and
mathlib's carmichael_lcm / carmichael_factorization) is never in scope.
"""
import hashlib
import itertools
import json
import math
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAB = HERE.parent / "lab.py"

M_TRAIN, M_TEST = 30, 48
K_TRAIN, K_FINAL = 60, 140


class Oracle:
    """Blind client: the same worker protocol the laboratory uses."""

    def __init__(self):
        self.proc = subprocess.Popen(
            [sys.executable, str(LAB), "--worker", "--oracle", "real"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True,
            bufsize=1)
        self.calls = 0
        self.log = []

    def truth(self, m, k):
        req = {"family": "U", "coord": [m, k], "op": "full"}
        self.proc.stdin.write(json.dumps(req, separators=(",", ":")) + "\n")
        self.proc.stdin.flush()
        ans = json.loads(self.proc.stdout.readline())
        self.calls += 1
        self.log.append((m, k, ans["truth"]))
        return ans["truth"]

    def close(self):
        self.proc.stdin.close()
        self.proc.wait()


# ---------- per-object invariant: the observed period ----------

def fit_period(values):
    """Smallest p with two observed copies explaining the whole row."""
    n = len(values)
    for p in range(1, n // 2 + 1):
        if all(values[i] == values[i % p] for i in range(n)):
            return p
    return None


# ---------- the declared hypothesis language ----------

OPS = {
    "lcm": lambda a, b: math.lcm(a, b),
    "gcd": lambda a, b: math.gcd(a, b),
    "mul": lambda a, b: a * b,
    "add": lambda a, b: a + b,
    "max": lambda a, b: max(a, b),
    "min": lambda a, b: min(a, b),
    "left": lambda a, b: a,
    "right": lambda a, b: b,
}


def spf(n):
    for d in range(2, n + 1):
        if n % d == 0:
            return d
    return n


BASE_EXPRS = {
    "n-1": lambda n: n - 1,
    "n": lambda n: n,
    "n+1": lambda n: n + 1,
    "n-2": lambda n: n - 2,
    "n//2": lambda n: n // 2,
    "n//4": lambda n: n // 4,
    "n//8": lambda n: n // 8,
    "n - n//spf(n)": lambda n: n - n // spf(n),
    "(n-1)//2": lambda n: (n - 1) // 2,
}
CONDS = [
    ("n mod 8 = 0", lambda n: n % 8 == 0),
    ("n mod 4 = 0", lambda n: n % 4 == 0),
    ("n mod 2 = 0", lambda n: n % 2 == 0),
    ("otherwise", lambda n: True),
]


def coprime_splits(m):
    return [(a, m // a) for a in range(2, m) if m % a == 0
            and math.gcd(a, m // a) == 1 and m // a > 1]


def main():
    oracle = Oracle()

    # ---------- observe training objects ----------
    observed = {}
    for m in range(1, M_TRAIN + 1):
        row = [oracle.truth(m, k) for k in range(1, K_TRAIN + 1)]
        observed[m] = fit_period(row)
    train_queries = oracle.calls

    # ---------- STAGE A: discover the composition law ----------
    scores = {}
    for name, op in OPS.items():
        ok = tot = 0
        for m in range(2, M_TRAIN + 1):
            for a, b in coprime_splits(m):
                if observed.get(a) and observed.get(b) and observed.get(m):
                    tot += 1
                    ok += int(op(observed[a], observed[b]) == observed[m])
        scores[name] = {"cases": tot, "correct": ok,
                        "accuracy": round(ok / tot, 4) if tot else None}
    chosen_op = max(scores, key=lambda k: (scores[k]["accuracy"] or 0, k))

    # ---------- STAGE B: base case for objects with no coprime split ----------
    atoms = [m for m in range(2, M_TRAIN + 1) if not coprime_splits(m)]
    best_list, best_err = None, None
    for combo in itertools.product(BASE_EXPRS, repeat=len(CONDS)):
        err = 0
        for n in atoms:
            for (cname, cond), ename in zip(CONDS, combo):
                if cond(n):
                    err += int(BASE_EXPRS[ename](n) != observed[n])
                    break
        if best_err is None or err < best_err:
            best_err, best_list = err, combo
    base_rule = [{"condition": c[0], "value": e}
                 for c, e in zip(CONDS, best_list)]

    def predict_f(m, known):
        """Predict the invariant for an unseen object."""
        if m in known:
            return known[m], "observed"
        splits = coprime_splits(m)
        for a, b in splits:
            fa = predict_f(a, known)[0]
            fb = predict_f(b, known)[0]
            if fa and fb:
                return OPS[chosen_op](fa, fb), "composed"
        for (cname, cond), ename in zip(CONDS, best_list):
            if cond(m):
                return BASE_EXPRS[ename](m), "base:" + ename
        return None, "none"

    # ---------- freeze forecasts BEFORE reading held-out answers ----------
    predicted = {}
    forecasts = []
    for m in range(M_TRAIN + 1, M_TEST + 1):
        val, how = predict_f(m, observed)
        predicted[m] = {"f_pred": val, "route": how}
        for k in range(1, K_FINAL + 1):
            # U(m,k) predicted true iff the period divides k-1
            p = bool(val and (k - 1) % val == 0)
            forecasts.append([m, k, p])
    frozen = {
        "chosen_composition_op": chosen_op,
        "composition_scores": scores,
        "base_rule": base_rule,
        "base_rule_training_errors": best_err,
        "observed_training_periods": observed,
        "predicted_invariants": predicted,
        "forecast_hash": hashlib.sha256(
            json.dumps(forecasts, separators=(",", ":")).encode()).hexdigest(),
        "queries_before_final": train_queries,
    }
    (HERE / "freeze.json").write_text(json.dumps(frozen, indent=1,
                                                 sort_keys=True))

    # ---------- now, and only now, read the held-out objects ----------
    correct = total = 0
    per_object = {}
    baseline_true = 0
    for m in range(M_TRAIN + 1, M_TEST + 1):
        c = t = 0
        obs_row = []
        for k in range(1, K_FINAL + 1):
            truth = oracle.truth(m, k)
            obs_row.append(truth)
            baseline_true += int(truth)
            pred = bool(predicted[m]["f_pred"]
                        and (k - 1) % predicted[m]["f_pred"] == 0)
            c += int(pred == truth)
            t += 1
        actual = fit_period(obs_row)
        per_object[m] = {
            "route": predicted[m]["route"],
            "f_predicted": predicted[m]["f_pred"],
            "f_actual_observed": actual,
            "invariant_exact": actual == predicted[m]["f_pred"],
            "accuracy": round(c / t, 4),
        }
        correct += c
        total += t

    replay = []
    for m in range(M_TRAIN + 1, M_TEST + 1):
        for k in range(1, K_FINAL + 1):
            v = predicted[m]["f_pred"]
            replay.append([m, k, bool(v and (k - 1) % v == 0)])
    assert hashlib.sha256(json.dumps(replay, separators=(",", ":")).encode()
                          ).hexdigest() == frozen["forecast_hash"]

    comp = [m for m in per_object if per_object[m]["route"] == "composed"]
    non = [m for m in per_object if per_object[m]["route"].startswith("base")]
    def acc(ms):
        if not ms:
            return None
        return round(sum(per_object[m]["accuracy"] for m in ms) / len(ms), 4)

    majority = 1 - baseline_true / total
    out = {
        "label": "COMPUTED",
        "chosen_composition_op": chosen_op,
        "composition_scores": scores,
        "base_rule": base_rule,
        "base_rule_training_errors": best_err,
        "held_out_objects": len(per_object),
        "composable": sorted(comp),
        "non_composable": sorted(non),
        "invariant_exact_overall": sum(
            1 for v in per_object.values() if v["invariant_exact"]),
        "invariant_exact_composable": sum(
            1 for m in comp if per_object[m]["invariant_exact"]),
        "invariant_exact_non_composable": sum(
            1 for m in non if per_object[m]["invariant_exact"]),
        "end_to_end_accuracy": round(correct / total, 5),
        "majority_class_baseline": round(majority, 5),
        "accuracy_composable": acc(comp),
        "accuracy_non_composable": acc(non),
        "oracle_queries": oracle.calls,
        "queries_before_freeze": train_queries,
        "forecast_hash": frozen["forecast_hash"],
        "per_object": per_object,
    }
    oracle.close()
    (HERE / "result.json").write_text(json.dumps(out, indent=1,
                                                 sort_keys=True))
    print(json.dumps({k: v for k, v in out.items()
                      if k not in ("per_object", "composition_scores")},
                     indent=2))
    print("\ncomposition op scores:")
    for n, s in sorted(scores.items(), key=lambda kv: -(kv[1]["accuracy"] or 0)):
        print("   %-6s %s/%s = %s" % (n, s["correct"], s["cases"],
                                      s["accuracy"]))
    print("\nper held-out object:")
    for m in sorted(per_object):
        v = per_object[m]
        print("  m=%2d %-14s f_pred=%-4s f_obs=%-4s %s acc=%.3f" % (
            m, v["route"], v["f_predicted"], v["f_actual_observed"],
            "EXACT" if v["invariant_exact"] else "wrong", v["accuracy"]))


if __name__ == "__main__":
    main()
