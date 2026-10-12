#!/usr/bin/env python3
"""
T -- corrected statistics.

The first stats pass used development-label permutation for BOTH contrasts.
That is valid for SOURCE vs WRONG (permuting the source label breaks the
source-target correspondence while WRONG stays fixed per target), but it has
NO POWER for SOURCE vs RANDOM: both quantities come from the same source, so
permuting the label carries them together and the difference distribution is
almost unchanged. Every p came back at ~0.5 for that reason, which is an
artifact of my test, not a property of the data.

SOURCE vs RANDOM is therefore re-tested by a development-clustered bootstrap
over TARGET developments -- the clustering the brief asks for, and the unit at
which observations are actually independent.
"""
import json
import random
import statistics as st
from collections import defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent
LEVELS = ["L1", "L2", "L3", "ENG", "MATH"]
SEED = 20260909
NBOOT = 20000


def cluster_bootstrap(rows, ka, kb):
    """Mean of (kb - ka), bootstrapped by resampling TARGET developments."""
    by = defaultdict(list)
    for r in rows:
        by[r["target"]].append(r[kb] - r[ka])
    devs = sorted(by)
    permean = {d: st.mean(by[d]) for d in devs}
    obs = st.mean([permean[d] for d in devs])
    rng = random.Random(SEED)
    draws = []
    for _ in range(NBOOT):
        s = [permean[rng.choice(devs)] for _ in devs]
        draws.append(st.mean(s))
    draws.sort()
    lo = draws[int(.025 * NBOOT)]
    hi = draws[int(.975 * NBOOT)]
    # sign test over developments
    pos = sum(1 for d in devs if permean[d] > 0)
    return obs, lo, hi, pos, len(devs), permean


def main():
    R = json.loads((OUT / "result.json").read_text())
    rows_all = R["rows"]
    out = {"label": "EXPERIMENTAL_RESULT",
           "note": "SOURCE vs RANDOM by target-development cluster bootstrap; "
                   "SOURCE vs WRONG by source-label permutation (from stats.py)"}
    prev = json.loads((OUT / "stats.json").read_text())

    print("%-6s %-18s %9s %19s %9s %10s" %
          ("level", "contrast", "delta", "95% CI (cluster)", "devs>0",
           "relative"))
    for L in LEVELS:
        rows = [r for r in rows_all
                if r["level"] == L and r["source"] != "__WITHIN__"]
        base = st.mean([r["RANDOM"] for r in rows])
        for name, ka, kb in (("SOURCE vs RANDOM", "SOURCE", "RANDOM"),
                             ("WRONG  vs RANDOM", "WRONG", "RANDOM"),
                             ("SOURCE vs WRONG", "SOURCE", "WRONG")):
            obs, lo, hi, pos, nd, permean = cluster_bootstrap(rows, ka, kb)
            sig = "" if lo <= 0 <= hi else "  *"
            print("%-6s %-18s %+9.4f  [%+7.4f,%+7.4f] %6d/%d %9.2f%%%s"
                  % (L, name, obs, lo, hi, pos, nd, 100 * obs / base, sig))
            out.setdefault(L, {})[name] = {
                "delta": round(obs, 5), "ci95": [round(lo, 5), round(hi, 5)],
                "devs_positive": pos, "n_devs": nd,
                "relative_pct": round(100 * obs / base, 3),
                "excludes_zero": not (lo <= 0 <= hi)}
        # how much of the SOURCE benefit is available from a wrong domain?
        o1 = out[L]["SOURCE vs RANDOM"]["delta"]
        o2 = out[L]["WRONG  vs RANDOM"]["delta"]
        share = o2 / o1 if o1 else float("nan")
        out[L]["generic_share_of_benefit"] = round(share, 4)
        print("%-6s %-18s %s" % ("", "-> generic share",
                                 "%.1f%% of the SOURCE benefit is already "
                                 "available from a WRONG-DOMAIN source"
                                 % (100 * share)))
        print()

    for L in LEVELS:
        out[L]["SOURCE vs WRONG (label permutation p)"] = \
            prev["contrasts"][L]["SOURCE vs WRONG"]["p"]
    (OUT / "stats2.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
