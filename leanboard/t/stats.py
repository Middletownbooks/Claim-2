#!/usr/bin/env python3
"""
T -- statistics, with the clustering the brief demands.

The effective sample is 10 developments, not 6153 proofs and not 90 pairs, so
significance is by development-label permutation. Two contrasts matter:

  SOURCE vs RANDOM  does trajectory ORDER carry information at all?
  SOURCE vs WRONG   does it matter WHICH development the order came from?

Only the second is transport. The first can be satisfied by any generic fact
about how Lean proofs are sequenced.
"""
import json
import random
import statistics as st
from collections import defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent
LEVELS = ["L1", "L2", "L3", "ENG", "MATH"]
NPERM = 20000
SEED = 20260909


def perm_test(rows, key_a, key_b, stat=None):
    """Paired difference key_b - key_a per pair, permuting SOURCE labels."""
    obs = st.mean([r[key_b] - r[key_a] for r in rows])
    srcs = sorted({r["source"] for r in rows})
    by = defaultdict(dict)
    for r in rows:
        by[r["target"]][r["source"]] = r
    rng = random.Random(SEED)
    cnt = used = 0
    for _ in range(NPERM):
        perm = srcs[:]
        rng.shuffle(perm)
        m = dict(zip(srcs, perm))
        vals = []
        for r in rows:
            q = by[r["target"]].get(m[r["source"]])
            if q is None:
                continue
            vals.append(q[key_b] - q[key_a])
        if len(vals) < 10:
            continue
        used += 1
        if abs(st.mean(vals)) >= abs(obs):
            cnt += 1
    return obs, (cnt / used if used else float("nan")), used


def main():
    R = json.loads((OUT / "result.json").read_text())
    rows_all = R["rows"]
    out = {"label": "EXPERIMENTAL_RESULT", "contrasts": {}}

    print("%-6s %-22s %10s %10s %9s %8s" %
          ("level", "contrast", "delta", "rel", "p", "n"))
    for L in LEVELS:
        rows = [r for r in rows_all
                if r["level"] == L and r["source"] != "__WITHIN__"]
        base = st.mean([r["RANDOM"] for r in rows])
        for name, ka, kb in (("SOURCE vs RANDOM", "SOURCE", "RANDOM"),
                             ("SOURCE vs WRONG", "SOURCE", "WRONG"),
                             ("WRONG vs RANDOM", "WRONG", "RANDOM")):
            d, p, n = perm_test(rows, ka, kb)
            rel = d / base
            out["contrasts"].setdefault(L, {})[name] = {
                "delta_rank": round(d, 5), "relative": round(rel, 5),
                "p": round(p, 4), "perms": n}
            print("%-6s %-22s %+10.4f %9.2f%% %9.4f %8d"
                  % (L, name, d, 100 * rel, p, len(rows)))
        print()

    # ---- negative transfer (section 17) ------------------------------
    print("=== NEGATIVE TRANSFER: pairs where SOURCE is WORSE than RANDOM ===")
    neg = {}
    for L in LEVELS:
        rows = [r for r in rows_all
                if r["level"] == L and r["source"] != "__WITHIN__"]
        bad = [r for r in rows if r["SOURCE"] > r["RANDOM"]]
        badw = [r for r in rows if r["SOURCE"] > r["WRONG"]]
        neg[L] = {"worse_than_random": len(bad), "worse_than_wrong": len(badw),
                  "of": len(rows),
                  "examples": ["%s->%s %+.3f" % (r["source"][:12],
                                                 r["target"][:12],
                                                 r["SOURCE"] - r["RANDOM"])
                               for r in sorted(bad, key=lambda r: -(r["SOURCE"] - r["RANDOM"]))[:4]]}
        print("  %-5s worse than RANDOM: %2d/%d   worse than WRONG-DOMAIN: %2d/%d"
              % (L, len(bad), len(rows), len(badw), len(rows)))
        if neg[L]["examples"]:
            print("        worst:", ", ".join(neg[L]["examples"]))
    out["negative_transfer"] = neg

    # ---- directionality (section 11) ---------------------------------
    print("\n=== DIRECTIONALITY: |T(A->B) - T(B->A)| at L2 (MATH in brackets) ===")
    for L in ("L2", "MATH"):
        rows = [r for r in rows_all
                if r["level"] == L and r["source"] != "__WITHIN__"]
        d = {(r["source"], r["target"]): r["RANDOM"] - r["SOURCE"] for r in rows}
        asym = []
        for (a, b), v in d.items():
            if (b, a) in d and a < b:
                asym.append((abs(v - d[(b, a)]), a, b, v, d[(b, a)]))
        asym.sort(reverse=True)
        print("  %-5s mean |asymmetry| = %.4f   most asymmetric:" %
              (L, st.mean([x[0] for x in asym])))
        for x in asym[:3]:
            print("      %-22s <-> %-22s  %+0.3f / %+0.3f"
                  % (x[1][:22], x[2][:22], x[3], x[4]))
        out.setdefault("directionality", {})[L] = {
            "mean_abs_asymmetry": round(st.mean([x[0] for x in asym]), 5)}

    # ---- how much of the within-development ceiling is recovered? ----
    print("\n=== CEILING RECOVERY ===")
    for L in LEVELS:
        cross = [r for r in rows_all
                 if r["level"] == L and r["source"] != "__WITHIN__"]
        wi = [r for r in rows_all
              if r["level"] == L and r["source"] == "__WITHIN__"]
        none = cross[0]["NONE"]
        rnd = st.mean([r["RANDOM"] for r in cross])
        src = st.mean([r["SOURCE"] for r in cross])
        wrg = st.mean([r["WRONG"] for r in cross])
        win = st.mean([r["SOURCE"] for r in wi])
        span = rnd - win
        print("  %-5s NONE %.3f  RANDOM %.3f  WRONG %.3f  SOURCE %.3f  "
              "WITHIN %.3f | source recovers %.1f%% of the RANDOM->WITHIN span"
              % (L, none, rnd, wrg, src, win,
                 100 * (rnd - src) / span if span else 0))
        out.setdefault("ceiling", {})[L] = {
            "NONE": none, "RANDOM": round(rnd, 4), "WRONG": round(wrg, 4),
            "SOURCE": round(src, 4), "WITHIN": round(win, 4),
            "pct_of_span_recovered": round(100 * (rnd - src) / span, 2)
            if span else None}

    (OUT / "stats.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
