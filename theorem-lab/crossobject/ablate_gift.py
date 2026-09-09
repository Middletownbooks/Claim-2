#!/usr/bin/env python3
"""
How much of the base-case result is the SEARCH, and how much is the grammar I
handed it? I chose the base expression vocabulary knowing lambda's shape, which
is a gift of the same class as the d_train=92 window in the earlier phase.

Ablation: drop each 'suspiciously well-aimed' expression and re-fit the base
rule on the training atoms only, then score on the held-out prime powers.
"""
import json
import math
from pathlib import Path

from crossobject import (BASE_EXPRS, CONDS, K_TRAIN, M_TEST, M_TRAIN, Oracle,
                         coprime_splits, fit_period)
import itertools

HERE = Path(__file__).resolve().parent


def fit_base(atoms, observed, exprs):
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


def main():
    oracle = Oracle()
    observed = {}
    for m in range(1, M_TRAIN + 1):
        row = [oracle.truth(m, k) for k in range(1, K_TRAIN + 1)]
        observed[m] = fit_period(row)
    held = [m for m in range(M_TRAIN + 1, M_TEST + 1) if not coprime_splits(m)]
    truth = {}
    for m in held:
        row = [oracle.truth(m, k) for k in range(1, 141)]
        truth[m] = fit_period(row)
    oracle.close()

    atoms = [m for m in range(2, M_TRAIN + 1) if not coprime_splits(m)]
    variants = {
        "full grammar (as pre-registered)": dict(BASE_EXPRS),
        "without n - n//spf(n)": {k: v for k, v in BASE_EXPRS.items()
                                  if k != "n - n//spf(n)"},
        "without n//4": {k: v for k, v in BASE_EXPRS.items() if k != "n//4"},
        "without both": {k: v for k, v in BASE_EXPRS.items()
                         if k not in ("n - n//spf(n)", "n//4")},
        "only n-1, n, n+1": {k: BASE_EXPRS[k] for k in ("n-1", "n", "n+1")},
    }
    out = {}
    for name, exprs in variants.items():
        combo, err = fit_base(atoms, observed, exprs)
        hits = 0
        detail = {}
        for m in held:
            for (cname, cond), e in zip(CONDS, combo):
                if cond(m):
                    pred = exprs[e](m)
                    break
            detail[m] = {"pred": pred, "obs": truth[m], "exact": pred == truth[m]}
            hits += int(pred == truth[m])
        out[name] = {
            "rule": [{"cond": c[0], "value": e} for c, e in zip(CONDS, combo)],
            "training_errors_on_atoms": err,
            "held_out_prime_powers_exact": "%d/%d" % (hits, len(held)),
            "detail": detail,
        }
    (HERE / "ablate_gift.json").write_text(json.dumps(out, indent=1,
                                                      sort_keys=True))
    print("%-34s %-9s %s" % ("base grammar", "train err", "held-out exact"))
    for name, v in out.items():
        print("%-34s %-9d %s" % (name, v["training_errors_on_atoms"],
                                 v["held_out_prime_powers_exact"]))
    print("\nheld-out prime powers:", held)


if __name__ == "__main__":
    main()
