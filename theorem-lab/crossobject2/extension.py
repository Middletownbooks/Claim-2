#!/usr/bin/env python3
"""
Pre-registered follow-up to task 2 (PREREG.md, final paragraph): add ONE
expression -- the exponent of n as a prime power -- to the transferred base
grammar, and measure how much of the base-case failure that single missing
primitive accounts for.

Everything else is unchanged: same composition law (max, resolved in Arm B),
same conditions, same training objects, same holdout.
"""
import itertools
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "crossobject"))
from crossobject import BASE_EXPRS, CONDS, OPS, coprime_splits  # noqa: E402
from task2 import EOracle, M_TRAIN, R_MAX, HOLDOUT, fit_base    # noqa: E402


def exp_spf(n):
    """Exponent e with n = p^e for the smallest prime p | n; 0 for n < 2."""
    if n < 2:
        return 0
    p = next(d for d in range(2, n + 1) if n % d == 0)
    e = 0
    while n % p == 0:
        n //= p
        e += 1
    return e


def main():
    oracle = EOracle()
    observed = {m: oracle.threshold(m) for m in range(1, M_TRAIN + 1)}
    truth = {m: oracle.threshold(m) for m in HOLDOUT}
    oracle.close()

    atoms = [m for m in range(2, M_TRAIN + 1) if not coprime_splits(m)]
    grammars = {
        "transferred grammar (as in task 2)": dict(BASE_EXPRS),
        "+ exponent of n": {**BASE_EXPRS, "exp_spf(n)": exp_spf},
        "only exponent of n": {"exp_spf(n)": exp_spf},
    }
    out = {}
    for name, exprs in grammars.items():
        combo, err = fit_base(atoms, observed, exprs)
        rule = [{"cond": c[0], "value": e} for c, e in zip(CONDS, combo)]

        def predict_t(m, known=observed, combo=combo, exprs=exprs):
            if m in known:
                return known[m], "observed"
            for a, b in coprime_splits(m):
                fa, _ = predict_t(a, known)
                fb, _ = predict_t(b, known)
                if fa and fb:
                    return OPS["max"](fa, fb), "composed"
            for (cname, cond), e in zip(CONDS, combo):
                if cond(m):
                    return exprs[e](m), "base"
            return None, "none"

        exact = correct = total = 0
        exact_atoms = atom_n = 0
        for m in HOLDOUT:
            v, how = predict_t(m)
            exact += int(v == truth[m])
            if how == "base":
                atom_n += 1
                exact_atoms += int(v == truth[m])
            for r in range(1, R_MAX + 1):
                correct += int(bool(v and r >= v) == (r >= truth[m]))
                total += 1
        out[name] = {
            "base_rule": rule,
            "training_errors_on_atoms": err,
            "held_out_invariants_exact": "%d/%d" % (exact, len(HOLDOUT)),
            "held_out_prime_powers_exact": "%d/%d" % (exact_atoms, atom_n),
            "end_to_end_accuracy": round(correct / total, 5),
        }
    (HERE / "extension.json").write_text(json.dumps(out, indent=1,
                                                    sort_keys=True))
    print("%-36s %-10s %-12s %-14s %s" % (
        "base grammar", "train err", "invariants", "prime powers", "end-to-end"))
    for name, v in out.items():
        print("%-36s %-10d %-12s %-14s %s" % (
            name, v["training_errors_on_atoms"],
            v["held_out_invariants_exact"], v["held_out_prime_powers_exact"],
            v["end_to_end_accuracy"]))
    print("\nmajority-class baseline: 0.91667")
    print("\nrule found with the exponent available:")
    for r in out["+ exponent of n"]["base_rule"]:
        print("   %-16s -> %s" % (r["cond"], r["value"]))


if __name__ == "__main__":
    main()
