#!/usr/bin/env python3
"""PRIORITY 14 — derived artifacts under the filenames the brief asks for."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import invariants as INV                                    # noqa: E402

ALIAS = {"A": "round2_static.json", "B": "round2_discovered.json",
         "D": "round2_reexpanded.json"}
CONDS = ["A0", "A", "B", "C", "D", "E", "Bo", "B520"]


def load(prefix):
    out = {}
    for c in CONDS:
        p = HERE / ("%s_%s.json" % (prefix, c))
        if p.exists():
            out[c] = json.loads(p.read_text())
    return out


def main():
    runs = {"prereg_cap": load("round2"), "budget_honoured": load("round2b")}

    # the brief's three named condition files, from the budget-honoured runs
    for c, name in ALIAS.items():
        src = runs["budget_honoured"].get(c) or runs["prereg_cap"].get(c)
        if src:
            (HERE / name).write_text(json.dumps(src, indent=1,
                                                sort_keys=True) + "\n")

    space = {"label": "COMPUTED",
             "definition": "R(s) = distinct value-vectors on TRAIN reachable "
                           "at outer cost <= s. Dedup on TRAIN can only "
                           "CONFLATE distinct functions, never split equal "
                           "ones, so |R_TRAIN(s)| is a LOWER bound on the "
                           "number of distinct semantic functions; the "
                           "EVALQ refinement measures the undercount.",
             "runs": {}}
    for tag, R in runs.items():
        space["runs"][tag] = {
            c: {"levels": {str(l["cost"]): l["classes_cumulative"]
                           for l in r["levels"]},
                "truncated": r["truncated_at_cap"],
                "expansions": r["expansions"],
                "class_cap": r["budget"]["class_cap"],
                "semantic_refinement": r["semantic_refinement"]}
            for c, r in R.items()}
    (HERE / "reachable_space.json").write_text(
        json.dumps(space, indent=1, sort_keys=True) + "\n")

    eq = {"label": "COMPUTED",
          "note": "Survivor sets after disagreement resolution. A verdict of "
                  "UNDERDETERMINED means the declared reserve contains no "
                  "coordinate on which the survivors disagree: they are the "
                  "SAME function on everything the protocol may observe, and "
                  "the stage reports the class rather than picking a member.",
          "targets": {}}
    src = runs["budget_honoured"] or runs["prereg_cap"]
    for t in INV.TARGETS:
        eq["targets"][t] = {}
        for c, r in src.items():
            x = r["targets"][t]
            if not x["reached"]:
                eq["targets"][t][c] = {"reached": False}
                continue
            eq["targets"][t][c] = {
                "reached": True, "min_cost": x["min_cost"],
                "class_size": x["distinct_minimal_terms"],
                "verdict": x["disagreement"]["verdict"],
                "probes_used": x["disagreement"]["probes_used"],
                "survivors_after_probing": x["disagreement"]["survivors"],
                "examples": x["terms"][:6],
                "holdout": x["holdout"]}
    (HERE / "candidate_equivalence_classes.json").write_text(
        json.dumps(eq, indent=1, sort_keys=True) + "\n")
    print("wrote reachable_space.json, candidate_equivalence_classes.json, "
          "and %d alias files" % len(ALIAS))


if __name__ == "__main__":
    main()
