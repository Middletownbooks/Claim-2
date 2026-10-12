#!/usr/bin/env python3
"""
Auditor-side analysis of an E-family run.

Reads a run directory produced by lab.py and reports, per modulus:
  * the learned r-factor (threshold / prefix structure);
  * the learned d-factor (period and which residues are positive);
  * comparison against independently computed nu(m) and lambda(m);
  * marginal errors err(A), err(B), err(A and B) on each phase.

Nothing here is fed back into the laboratory.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from numbertheory import nu, carmichael, E_direct  # noqa: E402


def seq_predict(model, coordinate):
    i = coordinate - 1
    prefix = model["prefix"]
    if i < len(prefix):
        return prefix[i]
    cycle = model["cycle"]
    return cycle[(i - len(prefix)) % len(cycle)]


def load_points(run, families=("E",)):
    """Replay the oracle log: coord -> (truth, phase)."""
    pts = {}
    with open(Path(run) / "oracle.jsonl", encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            req = rec["request"]
            if req["family"] not in families or req.get("op") != "full":
                continue
            pts[tuple(req["coord"])] = (
                rec["response"]["truth"], rec["first_phase"]
            )
    return pts


def describe_row(row):
    """Threshold-like summary of a fitted prefix/cycle sequence."""
    if row is None:
        return None
    out = {}
    for side in ("a", "b"):
        q = row[side]
        prefix, cycle = q["prefix"], q["cycle"]
        out[side] = {
            "prefix_len": len(prefix),
            "prefix": prefix,
            "period": len(cycle),
            "cycle": cycle,
            "positives_in_cycle": sum(cycle),
            "observed_repetitions": q["observed_repetitions"],
            # first coordinate (1-based) at which the sequence is true forever
            "always_true_from": (
                len(prefix) + 1
                if all(cycle) and all(not v for v in prefix) else None
            ),
            # if exactly one positive residue per period, report its offset
            "single_positive_offset": (
                [i for i, v in enumerate(cycle) if v][0] + len(prefix) + 1
                if sum(cycle) == 1 else None
            ),
        }
    return out


def main(run):
    run = Path(run)
    freeze = json.loads((run / "E_freeze.json").read_text())
    models = {("%s/%s" % (m["kind"], m.get("op", "-"))): m
              for m in freeze["models"]}
    ledger = json.loads((run / "ledger.json").read_text())["entries"]
    e_entries = [e for e in ledger if e["id"].startswith("E-")]
    id_of = {}
    for e in e_entries:
        h = e["hypothesis"]
        id_of["%s/%s" % (h["kind"], h.get("op", "-"))] = e["id"]

    pts = load_points(run)
    report = {"run": str(run), "selected_id": freeze["selected_id"],
              "model_ids": id_of, "per_modulus": {}, "marginals": {}}

    andmodel = models.get("factor/and")
    rows = andmodel["rows"]
    agree = disagree = 0
    for m_str, row in sorted(rows.items(), key=lambda kv: int(kv[0])):
        m = int(m_str)
        d = describe_row(row)
        if d is None:
            report["per_modulus"][m] = {"learned": None,
                                        "nu": nu(m), "lambda": carmichael(m)}
            continue
        learned_threshold = d["a"]["always_true_from"]
        learned_period = d["b"]["period"]
        # A modulus is "matching" when the r-factor turns on exactly at nu(m)
        # (clamped to 1, since r >= 1 is the queried domain) and the d-factor
        # has period lambda(m).
        expected_threshold = max(1, nu(m))
        ok = (learned_threshold == expected_threshold
              and learned_period == carmichael(m))
        agree += ok
        disagree += (not ok)
        report["per_modulus"][m] = {
            "learned_r_threshold": learned_threshold,
            "learned_d_period": learned_period,
            "learned_d_positive_offset": d["b"]["single_positive_offset"],
            "d_repetitions_observed": d["b"]["observed_repetitions"],
            "r_repetitions_observed": d["a"]["observed_repetitions"],
            "nu": nu(m),
            "lambda": carmichael(m),
            "matches_theory": ok,
            "a_prefix": d["a"]["prefix"], "a_cycle": d["a"]["cycle"],
            "b_period_positives": d["b"]["positives_in_cycle"],
        }
    report["moduli_matching_theory"] = agree
    report["moduli_not_matching_theory"] = disagree

    # Marginal errors: A alone (ignore d), B alone (ignore r), A and B.
    def A(m, r):
        row = rows[str(m)]
        return None if row is None else seq_predict(row["a"], r)

    def B(m, d):
        row = rows[str(m)]
        return None if row is None else seq_predict(row["b"], d)

    phases = {}
    for (m, r, d), (truth, phase) in pts.items():
        st = phases.setdefault(phase, {"n": 0, "errA": 0, "errB": 0,
                                       "errAND": 0, "abstain": 0})
        st["n"] += 1
        a, b = A(m, r), B(m, d)
        if a is None or b is None:
            st["abstain"] += 1
            continue
        st["errA"] += int(a != truth)
        st["errB"] += int(b != truth)
        st["errAND"] += int((a and b) != truth)
    report["marginals"] = phases
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main(sys.argv[1])
