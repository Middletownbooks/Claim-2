#!/usr/bin/env python3
"""
Ablations A, B, C for the E family (Phases 5, 6, 7).

Imports lab.py as a module and reuses its primitives, so each ablation differs
from the audited pipeline only in the representation language it is allowed.

  A  --no-boolean-factorization : the AND/OR/XOR/IFF tensor factoriser is removed.
                                  Remaining: 2-D tiles, per-(m,r) prefix/block codes,
                                  feature-pair quotient tables, atom/Boolean grammar.
  B  --no-periodicity           : every prefix/block and tile representation is removed.
                                  Remaining: congruence features, quotient tables,
                                  and a difference/equivalence-class period estimator
                                  that never stores a block.
  C  --no-history               : the full tensor experiment, but with no T family,
                                  no transport, and no parent theorem in scope.

Splits are identical to the audited run: calibration r<=R0,d<=D0; validation the rest of
r<=R1,d<=D1; final the rest of r<=R2,d<=D2. Selection uses validation only. Final labels
are read once, after the candidate is chosen.
"""
import argparse
import collections
import importlib.util
import itertools
import json
import math
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAB_PATH = HERE.parent / "lab.py"
spec = importlib.util.spec_from_file_location("lab", LAB_PATH)
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)

# Pure speed patch: the feature map is a deterministic function of one integer,
# recomputed millions of times by lab.predict. Memoising it changes no result.
import functools as _ft
lab.arithmetic_features = _ft.lru_cache(maxsize=None)(lab.arithmetic_features)


class DirectOracle:
    """Same protocol as the laboratory's client, one subprocess, no theory."""

    def __init__(self, command):
        self.proc = subprocess.Popen(
            command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            text=True, bufsize=1)
        self.calls = 0
        self.cache = {}

    def truth(self, family, coord):
        key = (family, tuple(coord))
        if key in self.cache:
            return self.cache[key]
        req = {"family": family, "coord": list(coord), "op": "full"}
        self.proc.stdin.write(json.dumps(req, separators=(",", ":")) + "\n")
        self.proc.stdin.flush()
        ans = json.loads(self.proc.stdout.readline())
        if "error" in ans:
            raise RuntimeError(ans["error"])
        self.calls += 1
        self.cache[key] = ans["truth"]
        return ans["truth"]

    def close(self):
        self.proc.stdin.close()
        self.proc.wait()


# ---------------- representations available to the ablations ----------------

def probe_features(m, r, row_truths, allow_periodic):
    """Features of the r-axis object, computed from calibration observations."""
    f = dict(lab.arithmetic_features(r))
    positives = [i + 1 for i, v in enumerate(row_truths) if v]
    f["probe:true_count"] = sum(row_truths)
    f["probe:first_true"] = min(positives, default=0)
    f["probe:first_false"] = min(
        [i + 1 for i, v in enumerate(row_truths) if not v], default=0)
    if allow_periodic:
        q = lab.fit_sequence(row_truths)
        f["probe:onset"] = len(q["prefix"])
        f["probe:period"] = len(q["cycle"])
        f["probe:cycle_positives"] = sum(q["cycle"])
    return f


def grammar_models(state_rf, calib_cells, R0, D0):
    """Atoms, depth-2 Boolean combinations, and feature-pair quotient tables."""
    rnames = sorted(state_rf[1])
    cnames = sorted(lab.arithmetic_features(1))
    models = [{"kind": "constant", "value": v} for v in (False, True)]
    atoms = [{"kind": "atom", "op": op, "r": rn, "c": cn}
             for rn in rnames for cn in cnames
             for op in ("eq", "le", "divides", "coprime")]
    models += atoms
    return models, atoms, rnames, cnames


def eval_model(model, points, state, per_row_seq=None):
    err = abst = 0
    for (r, d), truth in points:
        if per_row_seq is not None:
            q = per_row_seq.get(r)
            p = None if q is None else lab.sequence_predict(q, d)
        else:
            try:
                p = lab.predict(model, r, d, state)
            except KeyError:
                p = None
        if p is None:
            abst += 1
            err += 1
        elif p != truth:
            err += 1
    return err, abst


def gcd_period_estimator(positives, r_positive_rows):
    """
    Ablation-B mechanism: no stored block, no tile. Estimate a modulus-level
    period as the gcd of the differences between successive positive d values,
    and a threshold as the least r at which any positive is observed.
    """
    if not positives:
        return None
    p = 0
    for a, b in zip(sorted(positives), sorted(positives)[1:]):
        p = math.gcd(p, b - a)
    if p == 0:
        p = sorted(positives)[0]
    base = min(positives) % p if p else 0
    return {"period": p, "residue": base,
            "threshold": min(r_positive_rows) if r_positive_rows else None}


def run(world_command, ablation, R, D, out):
    R0, R1, R2 = R
    D0, D1, D2 = D
    M = 48
    oracle = DirectOracle(world_command)

    calib = [(m, r, d) for m in range(1, M + 1)
             for r in range(1, R0 + 1) for d in range(1, D0 + 1)]
    valid = [(m, r, d) for m in range(1, M + 1)
             for r in range(1, R1 + 1) for d in range(1, D1 + 1)
             if r > R0 or d > D0]
    final = [(m, r, d) for m in range(1, M + 1)
             for r in range(1, R2 + 1) for d in range(1, D2 + 1)
             if r > R1 or d > D1]

    truths = {}
    for c in calib + valid:
        truths[c] = oracle.truth("E", c)

    report = {"ablation": ablation, "world_command": world_command,
              "grid": {"R": R, "D": D, "M": M},
              "calibration_points": len(calib), "validation_points": len(valid),
              "final_points": len(final), "per_modulus": {}}

    allow_periodic = ablation != "B"
    chosen = {}
    for m in range(1, M + 1):
        rows = {r: [truths[(m, r, d)] for d in range(1, D0 + 1)]
                for r in range(1, R0 + 1)}
        state = {"rf": {r: probe_features(m, r, rows[r], allow_periodic)
                        for r in range(1, R0 + 1)},
                 "cycles": {}}
        cal_pts = [((r, d), truths[(m, r, d)])
                   for r in range(1, R0 + 1) for d in range(1, D0 + 1)]
        val_pts = [((r, d), truths[(m, r, d)]) for (mm, r, d) in valid
                   if mm == m]

        candidates = []

        # (i) generic grammar: atoms, depth-2 Booleans, quotient tables
        models, atoms, rnames, cnames = grammar_models(
            state["rf"], cal_pts, R0, D0)
        scored = []
        for mod in models:
            e, _ = eval_model(mod, cal_pts, state)
            scored.append((e, lab.canonical(mod), mod))
        scored.sort()
        best_atoms = [x[2] for x in scored[:12]]
        for left, right in itertools.combinations(best_atoms, 2):
            for op in ("and", "or", "xor"):
                models.append({"kind": "combine", "op": op,
                               "args": [left, right]})
        for rn in ["n"] + rnames[:5]:
            for cn in ["n"] + cnames[:5]:
                cells = collections.defaultdict(list)
                for (r, d), t in cal_pts:
                    cells["%d,%d" % (state["rf"][r][rn],
                                     lab.arithmetic_features(d)[cn])].append(t)
                models.append({
                    "kind": "table", "r": rn, "c": cn,
                    "cells": {k: lab.majority(v) for k, v in cells.items()},
                    "default": lab.majority(t for _, t in cal_pts)})
        for mod in models:
            ce, _ = eval_model(mod, cal_pts, state)
            ve, va = eval_model(mod, val_pts, state)
            candidates.append({"family": "grammar", "model": mod,
                               "calib_err": ce, "val_err": ve,
                               "cost": lab.model_cost(mod, state, [1])})

        # (ii) per-(m,r) prefix/block code along d  (periodicity allowed)
        if allow_periodic:
            seqs = {r: lab.fit_sequence(rows[r]) for r in range(1, R0 + 1)}
            # rows beyond R0 are not calibrated: reuse the last calibrated row,
            # which is the only honest choice without new observations
            per_row = {r: seqs[min(r, R0)] for r in range(1, R2 + 1)}
            ce, _ = eval_model(None, cal_pts, state, per_row)
            ve, _ = eval_model(None, val_pts, state, per_row)
            candidates.append({
                "family": "row_sequences", "model": {"kind": "row_sequences"},
                "calib_err": ce, "val_err": ve,
                "cost": sum(lab.sequence_cost(q) for q in seqs.values()),
                "_per_row": per_row})

            # (iii) 2-D tile
            matrix = [[rows[r][d - 1] for d in range(1, D0 + 1)]
                      for r in range(1, R0 + 1)]
            tile = lab.fit_tile(matrix)

            def tile_pred(r, d, tile=tile):
                return tile["tile"][(r - 1) % tile["pr"]][(d - 1) % tile["pd"]]
            ce = sum(tile_pred(r, d) != t for (r, d), t in cal_pts)
            ve = sum(tile_pred(r, d) != t for (r, d), t in val_pts)
            candidates.append({"family": "tile", "model": {"kind": "tile",
                                                           "pr": tile["pr"],
                                                           "pd": tile["pd"]},
                               "calib_err": ce, "val_err": ve,
                               "cost": tile["pr"] * tile["pd"] + 2,
                               "_tile": tile})
        else:
            # (iv) difference / equivalence-class period estimator
            top = R0
            positives = [d for d in range(1, D0 + 1) if rows[top][d - 1]]
            rpos = [r for r in range(1, R0 + 1) if any(rows[r])]
            est = gcd_period_estimator(positives, rpos)
            if est:
                def est_pred(r, d, est=est):
                    return (r >= (est["threshold"] or 1)
                            and d % est["period"] == est["residue"])
                ce = sum(est_pred(r, d) != t for (r, d), t in cal_pts)
                ve = sum(est_pred(r, d) != t for (r, d), t in val_pts)
                candidates.append({"family": "difference_estimator",
                                   "model": {"kind": "difference_estimator",
                                             **est},
                                   "calib_err": ce, "val_err": ve, "cost": 4,
                                   "_est": est})

        best = min(candidates, key=lambda c: (c["val_err"], c["calib_err"],
                                              c["cost"],
                                              lab.canonical(c["model"])))
        chosen[m] = (best, state)
        report["per_modulus"][m] = {
            "selected_family": best["family"],
            "selected_model": best["model"],
            "calib_err": best["calib_err"], "val_err": best["val_err"],
            "cost": best["cost"],
        }

    # ---- freeze, then read the final labels exactly once ----
    forecasts = {}
    for m in range(1, M + 1):
        best, state = chosen[m]
        preds = []
        for (mm, r, d) in final:
            if mm != m:
                continue
            if best["family"] == "row_sequences":
                q = best["_per_row"].get(r)
                p = None if q is None else lab.sequence_predict(q, d)
            elif best["family"] == "tile":
                t = best["_tile"]
                p = t["tile"][(r - 1) % t["pr"]][(d - 1) % t["pd"]]
            elif best["family"] == "difference_estimator":
                e = best["_est"]
                p = (r >= (e["threshold"] or 1)
                     and d % e["period"] == e["residue"])
            else:
                try:
                    p = lab.predict(best["model"], r, d, state)
                except KeyError:
                    p = None
            preds.append(((r, d), p))
        forecasts[m] = preds
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    (Path(out).parent / (Path(out).stem + "_forecasts.json")).write_text(
        json.dumps({m: [[list(c), p] for c, p in v]
                    for m, v in forecasts.items()}, sort_keys=True))

    total_err = total_abst = total = 0
    for m in range(1, M + 1):
        err = abst = 0
        for (r, d), p in forecasts[m]:
            t = oracle.truth("E", (m, r, d))
            if p is None:
                abst += 1
                err += 1
            elif p != t:
                err += 1
        report["per_modulus"][m]["final_err"] = err
        report["per_modulus"][m]["final_abstentions"] = abst
        report["per_modulus"][m]["final_points"] = len(forecasts[m])
        total_err += err
        total_abst += abst
        total += len(forecasts[m])
    report["final_errors"] = total_err
    report["final_abstentions"] = total_abst
    report["final_points_total"] = total
    report["final_accuracy"] = 1 - total_err / total
    report["total_description_cost"] = sum(
        report["per_modulus"][m]["cost"] for m in range(1, M + 1))
    report["selected_family_counts"] = dict(collections.Counter(
        report["per_modulus"][m]["selected_family"] for m in range(1, M + 1)))
    report["oracle_queries"] = oracle.calls
    oracle.close()
    Path(out).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: v for k, v in report.items()
                      if k != "per_modulus"}, indent=2, sort_keys=True))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--ablation", choices=("A", "B"), required=True)
    p.add_argument("--world-command", default=None)
    p.add_argument("--r", default="8,10,12")
    p.add_argument("--d", default="92,102,112")
    p.add_argument("--out", required=True)
    a = p.parse_args()
    cmd = (a.world_command.split() if a.world_command
           else [sys.executable, str(LAB_PATH), "--worker", "--oracle", "real"])
    run(cmd, a.ablation,
        tuple(int(x) for x in a.r.split(",")),
        tuple(int(x) for x in a.d.split(",")), a.out)
