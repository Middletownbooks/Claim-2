#!/usr/bin/env python3
"""Term formation on the two cross-object invariants. See PREREG.md."""
import json
import subprocess
import sys
import time
from pathlib import Path

from language import ev, show, size
from synth import synthesize

HERE = Path(__file__).resolve().parent
LAB = HERE.parent / "lab.py"

TRAIN = [2, 3, 4, 5, 7, 8, 9, 11, 13, 16, 17, 19, 23, 25, 27, 29]
HOLDOUT = [31, 32, 37, 41, 43, 47]
RESERVE = [49, 64, 81, 121, 125, 128, 169, 243]
R_MAX, D_MAX = 8, 260


class Oracle:
    def __init__(self):
        self.p = subprocess.Popen(
            [sys.executable, str(LAB), "--worker", "--oracle", "real"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True,
            bufsize=1)
        self.calls = 0

    def ask(self, fam, coord):
        self.p.stdin.write(json.dumps(
            {"family": fam, "coord": list(coord), "op": "full"},
            separators=(",", ":")) + "\n")
        self.p.stdin.flush()
        self.calls += 1
        return json.loads(self.p.stdout.readline())["truth"]

    def period(self, m):                      # U-family row period = lambda
        row = [self.ask("U", (m, k)) for k in range(1, 2 * D_MAX + 1)]
        for p in range(1, len(row) // 2 + 1):
            if all(row[i] == row[i % p] for i in range(len(row))):
                return p
        return None

    def threshold(self, m):                   # E-family r-threshold = max(1,nu)
        for r in range(1, R_MAX + 1):
            for d in range(1, D_MAX + 1):
                if self.ask("E", (m, r, d)):
                    return r
        return None

    def close(self):
        self.p.stdin.close()
        self.p.wait()


def main():
    oracle = Oracle()
    obs = {}
    t0 = time.time()
    for label, fn in (("lambda", oracle.period), ("nu", oracle.threshold)):
        obs[label] = {m: fn(m) for m in TRAIN + HOLDOUT + RESERVE}
    print("observed in %.0fs, %d oracle queries" % (time.time() - t0,
                                                    oracle.calls))
    oracle.close()

    results = {}
    for label in ("nu", "lambda"):
        target = [obs[label][m] for m in TRAIN]
        print("\n=== target: %s ===\ntrain values: %s" % (label, target))
        t0 = time.time()
        terms, pool = synthesize(TRAIN, target, max_size=5, body_size=3)
        dt = time.time() - t0
        rec = {"target_train": target, "search_seconds": round(dt, 1),
               "minimal_terms_found": len(terms), "terms": []}
        for t in terms:
            hold = [ev(t, {"n": m}) for m in HOLDOUT]
            truth = [obs[label][m] for m in HOLDOUT]
            res = [ev(t, {"n": m}) for m in RESERVE]
            rec["terms"].append({
                "term": show(t), "size": size(t),
                "holdout_pred": hold, "holdout_true": truth,
                "generalizes": hold == truth,
                "reserve_pred": res,
            })
        rec["generalizing_terms"] = sum(1 for x in rec["terms"]
                                        if x["generalizes"])
        results[label] = rec
        print("  found %d minimal term(s) in %.0fs; %d generalize" % (
            len(terms), dt, rec["generalizing_terms"]))
        for x in rec["terms"][:6]:
            print("    size %d  %-46s holdout %s %s" % (
                x["size"], x["term"][:46], x["holdout_pred"],
                "OK" if x["generalizes"] else "x"))
    results["_holdout_truth"] = {l: [obs[l][m] for m in HOLDOUT]
                                 for l in ("nu", "lambda")}
    results["_observations"] = {l: {str(k): v for k, v in obs[l].items()}
                                for l in obs}
    (HERE / "result.json").write_text(json.dumps(results, indent=1,
                                                 sort_keys=True))


if __name__ == "__main__":
    main()
