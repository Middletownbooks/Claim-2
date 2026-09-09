#!/usr/bin/env python3
"""Term formation v2: formed terms are units. See PREREG.md / REPORT_M.md."""
import json
import time
from pathlib import Path

from run import HOLDOUT, RESERVE, TRAIN, Oracle
from synth2 import ev, form_leaves, show, size, synthesize

HERE = Path(__file__).resolve().parent
CONDS = [("n mod 8 = 0", lambda n: n % 8 == 0),
         ("n mod 4 = 0", lambda n: n % 4 == 0),
         ("n mod 2 = 0", lambda n: n % 2 == 0),
         ("otherwise", lambda n: True)]


def branch_of(n):
    for name, c in CONDS:
        if c(n):
            return name


def main():
    oracle = Oracle()
    obs = {"lambda": {}, "nu": {}}
    for m in TRAIN + HOLDOUT + RESERVE:
        obs["lambda"][m] = oracle.period(m)
        obs["nu"][m] = oracle.threshold(m)
    oracle.close()

    t0 = time.time()
    formed = form_leaves(TRAIN)
    print("  forming took %.0fs" % (time.time() - t0))

    out = {"formed_terms": len(formed)}

    # --- nu: a single term over all atoms ---
    target = [obs["nu"][m] for m in TRAIN]
    t0 = time.time()
    terms, pool = synthesize(TRAIN, target, formed, max_size=5, verbose=True)
    rec = {"search_seconds": round(time.time() - t0, 1),
           "minimal_terms": len(terms), "terms": []}
    for t in terms:
        pred = [ev(t, {"n": m}) for m in HOLDOUT]
        rec["terms"].append({
            "term": show(t), "size": size(t), "holdout_pred": pred,
            "holdout_true": [obs["nu"][m] for m in HOLDOUT],
            "generalizes": pred == [obs["nu"][m] for m in HOLDOUT],
            "reserve_pred": [ev(t, {"n": m}) for m in RESERVE],
            "reserve_true": [obs["nu"][m] for m in RESERVE]})
    rec["generalizing"] = sum(1 for x in rec["terms"] if x["generalizes"])
    out["nu"] = rec
    print("\nnu: %d minimal term(s), %d generalize (%.0fs)" % (
        len(terms), rec["generalizing"], rec["search_seconds"]))
    for x in rec["terms"][:8]:
        print("   size %d %-52s %s %s" % (x["size"], x["term"][:52],
                                          x["holdout_pred"],
                                          "OK" if x["generalizes"] else "x"))

    # --- lambda: per branch of the decision list (P4) ---
    out["lambda"] = {"branches": {}}
    for name, cond in CONDS:
        atoms = [m for m in TRAIN if branch_of(m) == name]
        if not atoms:
            out["lambda"]["branches"][name] = {"atoms": 0, "skipped": True}
            continue
        tgt = [obs["lambda"][m] for m in atoms]
        terms, _ = synthesize(atoms, tgt, formed, max_size=5)
        hold = [m for m in HOLDOUT if branch_of(m) == name]
        b = {"atoms": len(atoms), "train_values": tgt,
             "minimal_terms": len(terms), "terms": []}
        for t in terms[:8]:
            pred = [ev(t, {"n": m}) for m in hold]
            b["terms"].append({
                "term": show(t), "size": size(t),
                "holdout_objects": hold, "holdout_pred": pred,
                "holdout_true": [obs["lambda"][m] for m in hold],
                "generalizes": pred == [obs["lambda"][m] for m in hold]})
        b["generalizing"] = sum(1 for x in b["terms"] if x["generalizes"])
        out["lambda"]["branches"][name] = b
        print("\nlambda / %-14s atoms=%d minimal terms=%d generalizing=%d" % (
            name, len(atoms), len(terms), b["generalizing"]))
        for x in b["terms"][:4]:
            print("   size %d %-48s -> %s %s" % (
                x["size"], x["term"][:48], x["holdout_pred"],
                "OK" if x["generalizes"] else "x"))

    (HERE / "result_v2.json").write_text(json.dumps(out, indent=1,
                                                    sort_keys=True))


if __name__ == "__main__":
    main()
