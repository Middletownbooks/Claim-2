#!/usr/bin/env python3
"""
Phase 12: adversarial exception mining against a frozen E candidate.

The frozen model is read from a run's E_freeze.json. Ground truth is obtained
from audit/worlds.py --world A, an independent re-implementation of the
predicate, so the miner never trusts lab.py's own oracle code.

Probed regions (all outside the run's tested box):
  * d far beyond the calibration window, including many further periods;
  * r far beyond the tested range;
  * exact boundary coordinates: one below / at / one above each learned
    threshold and each learned period multiple;
  * moduli beyond m_test, where the model has no row at all.
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


class World:
    def __init__(self, world="A"):
        self.proc = subprocess.Popen(
            [sys.executable, str(HERE / "worlds.py"), "--world", world],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True,
            bufsize=1)
        self.n = 0

    def truth(self, coord):
        self.proc.stdin.write(json.dumps(
            {"family": "E", "coord": list(coord), "op": "full"},
            separators=(",", ":")) + "\n")
        self.proc.stdin.flush()
        ans = json.loads(self.proc.stdout.readline())
        self.n += 1
        if "error" in ans:
            return None
        return ans["truth"]

    def close(self):
        self.proc.stdin.close()
        self.proc.wait()


def seq_predict(q, i):
    j = i - 1
    if j < len(q["prefix"]):
        return q["prefix"][j]
    c = q["cycle"]
    return c[(j - len(q["prefix"])) % len(c)]


def main(run, m_max_extra=64, d_max=400, r_max=40):
    freeze = json.loads((Path(run) / "E_freeze.json").read_text())
    andmodel = next(m for m in freeze["models"]
                    if m["kind"] == "factor" and m.get("op") == "and")
    rows = andmodel["rows"]
    cfg = json.loads((Path(run) / "manifest.json").read_text())["configuration"]
    M, R2, D2 = cfg["m_test"], cfg["r_test"], cfg["d_test"]

    def predict(m, r, d):
        row = rows.get(str(m))
        if row is None:
            return None                      # model undefined here
        return bool(seq_predict(row["a"], r) and seq_predict(row["b"], d))

    w = World("A")
    findings = []
    tested = 0

    def probe(m, r, d, region):
        nonlocal tested
        p = predict(m, r, d)
        t = w.truth((m, r, d))
        tested += 1
        if p is None:
            findings.append({"coord": [m, r, d], "region": region,
                             "kind": "model_undefined", "observed": t})
        elif p != t:
            findings.append({"coord": [m, r, d], "region": region,
                             "kind": "prediction_error",
                             "predicted": p, "observed": t})

    # 1. deep d-extrapolation, every modulus, several further periods
    for m in range(1, M + 1):
        period = len(rows[str(m)]["b"]["cycle"]) if rows.get(str(m)) else None
        for d in list(range(D2 + 1, d_max + 1, 7)):
            probe(m, R2, d, "d_beyond_tested")
        if period:
            for k in range(1, 9):
                for delta in (-1, 0, 1):
                    d = k * period + delta
                    if d > D2:
                        probe(m, R2, d, "period_boundary")

    # 2. deep r-extrapolation and threshold boundaries
    for m in range(1, M + 1):
        row = rows.get(str(m))
        thr = None
        if row:
            pre = row["a"]["prefix"]
            thr = len(pre) + 1
        for r in range(R2 + 1, r_max + 1, 3):
            probe(m, r, len(row["b"]["cycle"]) if row else 1, "r_beyond_tested")
        if thr:
            for r in (max(1, thr - 1), thr, thr + 1):
                probe(m, r, 2 * len(row["b"]["cycle"]), "threshold_boundary")

    # 3. moduli the model has never seen
    for m in range(M + 1, M + m_max_extra + 1):
        for r in (1, 3, 8):
            for d in (1, 6, 12, 60):
                probe(m, r, d, "modulus_beyond_tested")

    w.close()
    by_kind = {}
    for f in findings:
        by_kind.setdefault(f["kind"], []).append(f)
    out = {
        "label": "COMPUTED",
        "run": str(run),
        "probes": tested,
        "prediction_errors": len(by_kind.get("prediction_error", [])),
        "model_undefined_points": len(by_kind.get("model_undefined", [])),
        "regions_probed": sorted({f["region"] for f in findings}) or
                          ["all clean"],
        "examples": {k: v[:5] for k, v in by_kind.items()},
    }
    print(json.dumps(out, indent=2, sort_keys=True))
    Path(HERE / "exceptions_found.json").write_text(
        json.dumps({"summary": out, "findings": findings[:2000]},
                   indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main(sys.argv[1])
