#!/usr/bin/env python3
"""PRIORITY 14 — the machine-readable experiment manifest."""
import hashlib
import json
import platform
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def h(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    files = sorted(p.name for p in HERE.iterdir()
                   if p.suffix in (".py", ".json", ".md") and p.is_file()
                   and p.name != "experiment_manifest.json")
    r1 = HERE.parent / "termform"
    man = {
        "label": "COMPUTED",
        "experiment": "Iterated Term Formation (Round 2)",
        "prereg": {"file": "PREREG.md", "sha256": h(HERE / "PREREG.md")},
        "frozen_upstream": {
            "round1_manifest.json": h(HERE / "round1_manifest.json"),
            **{"termform/" + f: h(r1 / f) for f in
               ("language.py", "synth2.py", "run.py", "run2.py",
                "result_v2.json", "REPORT_M.md")},
        },
        "files": {f: h(HERE / f) for f in files},
        "splits": {"TRAIN": "2..40", "RESERVE": "41..55",
                   "HOLDOUT": "56..90", "EVALQ": "121..160",
                   "disjoint": True},
        "budgets": {"outer_max_cost": 5, "outer_max_cost_E": 7,
                    "beam": 1200, "beam_E": 2400, "class_cap": 300000,
                    "unit_cap": 500, "stage1_body_size": 3,
                    "stage2_body_size": 5, "stage1_cap": 6000,
                    "stage2_cap": 40000},
        "seeds": {"global": 20260909,
                  "used_for": ["condition C vocabulary draw",
                               "reservoir sampling of semantic classes"],
                  "note": "the search itself is deterministic and consumes no "
                          "RNG; only the two uses above draw from it"},
        "deviations_from_prereg": [
            {"what": "PREREG section 3 lists the V0 atom count as 6",
             "correction": "6 is the atom count inside a quantifier body "
                           "(n, k, 0, 1, 2, 4); the OUTER search has 5 "
                           "(n, 0, 1, 2, 4). A miscount in the table, not a "
                           "change of design.",
             "when": "before any Round-2 result"},
            {"what": "removed `smallest_div_gt_1` from the invariant library",
             "correction": "it was an exact duplicate of `spf`; a library "
                           "match must identify one invariant, not two.",
             "when": "before any Round-2 result"},
            {"what": "the outer enumeration was vectorised (numpy)",
             "correction": "an implementation change only. All nine operators "
                           "are checked against the reference evaluator on "
                           "40 000 random inputs, and a 300-term sample of "
                           "each run is re-evaluated with the reference "
                           "evaluator; both checks are recorded in every "
                           "round2_*.json.",
             "when": "before any Round-2 result"},
            {"what": "condition E's raised budget was fixed at "
                     "max cost 7, beam 2400",
             "correction": "PREREG said 'raised until candidate expansions >= "
                           "B' without naming numbers; these were chosen to "
                           "satisfy that and the achieved counts are reported.",
             "when": "before any Round-2 result"},
            {"what": "an exploratory condition `Bo` was added",
             "correction": "promoted terms available to the outer search only, "
                           "not during term formation. Not pre-registered, "
                           "labelled exploratory, and reported separately from "
                           "the pre-registered comparisons.",
             "when": "before any Round-2 result"},
        ],
        "environment": {"python": sys.version.split()[0],
                        "platform": platform.platform()},
    }
    try:
        import numpy
        man["environment"]["numpy"] = numpy.__version__
    except Exception:
        pass
    (HERE / "experiment_manifest.json").write_text(
        json.dumps(man, indent=1, sort_keys=True) + "\n")
    print("wrote experiment_manifest.json (%d files hashed)" % len(files))


if __name__ == "__main__":
    main()
