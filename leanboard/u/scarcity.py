#!/usr/bin/env python3
"""
U4 -- which lever actually buys verified findings under scarcity?

This is a SIMULATION and its conclusions are conditional on the model. It is
included because the measured record makes one question sharp and answerable:
this programme's directional forecasts carried no information (Fisher p = 1.00,
P(effect|GO) = 0.111 vs P(effect|NOGO) = 0.167, base rate 0.143), yet the
programme still produced verified findings. So the useful question is not
"which ranking policy wins" -- ranking was worthless -- but:

    at a fixed budget, does a small team gain more from IMPROVING ITS FORECAST
    or from REDUCING ITS COST PER DECISIVE TEST?

The two grounded inputs are taken from the record, not invented:
  base rate of true effects in the hypothesis pool  = 20/44 = 0.455 (corrected)
  forecaster informativeness as measured            = INFORMATIVE (Fisher p = 0.039)

Everything else is swept, so the reader can see what the answer depends on.
"""
import json
import random
import statistics as st
from pathlib import Path

OUT = Path(__file__).resolve().parent
SEED = 20260909
BASE_RATE = 20 / 44          # CORRECTED: effects existed in 20 of 44 predictions
TRIALS = 4000


def run(budget, cost_per_test, informativeness, n_candidates=40, rng=None):
    """Returns verified findings. A test costs `cost_per_test`; it resolves the
    hypothesis either way (that is what pre-registration buys). A 'finding' is
    a true effect correctly identified. `informativeness` shifts the forecaster
    from chance (0) to perfect (1)."""
    truth = [rng.random() < BASE_RATE for _ in range(n_candidates)]
    # forecaster score: mixes truth with noise according to informativeness
    score = [informativeness * (1.0 if t else 0.0) +
             (1 - informativeness) * rng.random() for t in truth]
    order = sorted(range(n_candidates), key=lambda i: -score[i])
    ntests = int(budget // cost_per_test)
    return sum(1 for i in order[:ntests] if truth[i])


def main():
    rng = random.Random(SEED)
    budgets = [10, 20, 100, 1000]          # C, 2C, 10C, 100C
    rows = []
    print("Findings at fixed budget. Base rate %.3f (measured). "
          "TRIALS=%d\n" % (BASE_RATE, TRIALS))
    print("%-8s %-8s %-14s %10s" % ("budget", "cost", "informativeness",
                                    "findings"))
    for B in budgets:
        for cost in (1.0, 0.5, 0.25):
            for info in (0.0, 0.25, 0.5, 0.9):
                v = [run(B, cost, info, rng=rng) for _ in range(TRIALS)]
                rows.append({"budget": B, "cost_per_test": cost,
                             "informativeness": info,
                             "mean_findings": round(st.mean(v), 4)})
                print("%-8d %-8.2f %-14.2f %10.3f"
                      % (B, cost, info, st.mean(v)))
        print()

    # the decisive comparison, at the measured operating point
    print("=== THE LEVER COMPARISON, from the measured operating point "
          "(cost 1.0, informativeness 0.0) ===")
    for B in budgets:
        base = st.mean([run(B, 1.0, 0.0, rng=rng) for _ in range(TRIALS)])
        halve_cost = st.mean([run(B, 0.5, 0.0, rng=rng) for _ in range(TRIALS)])
        better_fc = st.mean([run(B, 1.0, 0.5, rng=rng) for _ in range(TRIALS)])
        both = st.mean([run(B, 0.5, 0.5, rng=rng) for _ in range(TRIALS)])
        print("  budget %4d : base %.3f | halve cost %.3f (%+.0f%%) | "
              "forecast 0->0.5 %.3f (%+.0f%%) | both %.3f"
              % (B, base, halve_cost, 100 * (halve_cost - base) / base,
                 better_fc, 100 * (better_fc - base) / base, both))

    json.dump({"label": "SIMULATION",
               "caveat": "conditional on the model; the only grounded inputs "
                         "are the measured base rate (0.143) and the measured "
                         "forecaster informativeness (0.0)",
               "base_rate": BASE_RATE, "trials": TRIALS, "rows": rows},
              open(OUT / "scarcity.json", "w"), indent=1)


if __name__ == "__main__":
    main()
