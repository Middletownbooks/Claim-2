#!/usr/bin/env python3
"""Phase 3: empirical holdout-integrity checks on a completed run directory."""
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


def main(run):
    run = Path(run)
    recs = [json.loads(l) for l in open(run / "oracle.jsonl", encoding="utf-8")]
    out = {"run": str(run), "queries": len(recs)}

    # 1. every query id is unique and monotone; the cache never re-asks
    ids = [r["id"] for r in recs]
    out["ids_strictly_increasing"] = ids == sorted(set(ids)) == sorted(ids)
    keys = [(r["request"]["family"], tuple(r["request"]["coord"]),
             r["request"].get("op", "full")) for r in recs]
    out["duplicate_requests"] = len(keys) - len(set(keys))

    # 2. partition membership by first_phase; check disjointness per family
    by_phase = defaultdict(set)
    for r, k in zip(recs, keys):
        by_phase[r["first_phase"]].add(k)
    out["phase_sizes"] = {p: len(s) for p, s in sorted(by_phase.items())}
    overlaps = {}
    phases = sorted(by_phase)
    for i, a in enumerate(phases):
        for b in phases[i + 1:]:
            n = len(by_phase[a] & by_phase[b])
            if n:
                overlaps["%s|%s" % (a, b)] = n
    out["cross_phase_overlaps"] = overlaps  # must be empty: cache is first-touch

    # 3. the freeze boundary: no final-phase query may precede the freeze
    for fam, freeze_file in (("E", "E_freeze.json"), ("T", "T_freeze.json"),
                             ("U", "U_freeze.json")):
        f = run / freeze_file
        if not f.exists():
            continue
        before = json.loads(f.read_text())["oracle_queries_before_final"]
        finals = [r["id"] for r in recs
                  if r["first_phase"] == fam + ":final"]
        out[fam + "_freeze_at_query"] = before
        out[fam + "_first_final_query_id"] = min(finals) if finals else None
        out[fam + "_final_after_freeze"] = (
            not finals or min(finals) > before
        )

    # 4. E grid partition arithmetic: calibration/validation/final disjoint,
    #    and the union is the full box
    cfg = json.loads((run / "manifest.json").read_text())["configuration"]
    M, R0, R1, R2 = cfg["m_test"], cfg["r_train"], cfg["r_valid"], cfg["r_test"]
    D0, D1, D2 = cfg["d_train"], cfg["d_valid"], cfg["d_test"]
    calib = {(m, r, d) for m in range(1, M + 1)
             for r in range(1, R0 + 1) for d in range(1, D0 + 1)}
    val = {(m, r, d) for m in range(1, M + 1)
           for r in range(1, R1 + 1) for d in range(1, D1 + 1)
           if r > R0 or d > D0}
    fin = {(m, r, d) for m in range(1, M + 1)
           for r in range(1, R2 + 1) for d in range(1, D2 + 1)
           if r > R1 or d > D1}
    box = {(m, r, d) for m in range(1, M + 1)
           for r in range(1, R2 + 1) for d in range(1, D2 + 1)}
    out["E_partition"] = {
        "calibration": len(calib), "validation": len(val), "final": len(fin),
        "pairwise_disjoint": not (calib & val or calib & fin or val & fin),
        "union_is_full_box": calib | val | fin == box,
    }

    # 5. how much of the final region actually tests a POSITIVE prediction?
    #    (one-sided extrapolation is weak evidence)
    truths = {}
    for r in recs:
        if r["request"]["family"] == "E" and r["request"].get("op") == "full":
            truths[tuple(r["request"]["coord"])] = r["response"]["truth"]
    pos = Counter()
    per_m_pos = defaultdict(int)
    for c in fin:
        if truths.get(c):
            pos["final_true"] += 1
            per_m_pos[c[0]] += 1
        else:
            pos["final_false"] += 1
    out["E_final_label_balance"] = dict(pos)
    out["E_moduli_with_no_positive_final_point"] = sorted(
        m for m in range(1, M + 1) if per_m_pos[m] == 0
    )
    out["E_positive_final_points_per_modulus"] = {
        m: per_m_pos[m] for m in range(1, M + 1)
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main(sys.argv[1])
