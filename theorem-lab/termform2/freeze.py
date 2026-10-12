#!/usr/bin/env python3
"""
PRIORITY 1 — freeze Round 1 as an immutable upstream artifact.

Verification performed before writing this manifest: `run2.py` was re-executed
from the committed code and its output compared field-by-field against the
committed `result_v2.json`. The ONLY difference in the entire artifact was
`/nu/search_seconds` (1.4 -> 1.3), a wall-clock field. Round 1 is therefore
exactly recoverable and is frozen here.
"""
import hashlib
import json
import subprocess
from pathlib import Path

R1 = Path(__file__).resolve().parent.parent / "termform"
OUT = Path(__file__).resolve().parent


def h(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    res = json.loads((R1 / "result_v2.json").read_text())

    # ---- the certification rule, stated before it is applied ----
    # A Round-1 term is CERTIFIED iff it matched its target with zero error on
    # the Round-1 training atoms AND reproduced the Round-1 holdout atoms
    # exactly. Report M records both facts per term.
    certified = []
    for t in res["nu"]["terms"]:
        if t["generalizes"]:
            certified.append({"target": "nu", **t})
    for name, br in res["lambda"]["branches"].items():
        for t in br.get("terms", []):
            if t.get("generalizes"):
                certified.append({"target": "lambda:" + name, **t})

    manifest = {
        "label": "FROZEN",
        "round": 1,
        "source_report": "theorem-lab/termform/REPORT_M.md",
        "reproduction_check": {
            "method": "re-ran run2.py from committed code, diffed every field",
            "differences": ["/nu/search_seconds: 1.4 -> 1.3 (wall clock)"],
            "verdict": "EXACTLY RECOVERABLE",
        },
        "code_hashes": {f: h(R1 / f) for f in
                        ("language.py", "synth.py", "synth2.py", "run.py",
                         "run2.py", "resolve_ties.py")},
        "artifact_hashes": {f: h(R1 / f) for f in
                            ("result.json", "result_v2.json",
                             "resolve_ties.json", "PREREG.md")},
        "primitive_vocabulary": {
            "variables": ["n", "k"],
            "constants": [0, 1, 2, 4],
            "binops": ["add", "sub", "mul", "div", "mod", "gcd", "min", "max",
                       "pow"],
            "quantifiers": {
                "least": "least k in [2..n] with body(n,k) = 0, else 0",
                "count": "how many k in [1..n] satisfy body(n,k) = 0"},
            "NOT_given": ["spf", "phi", "tau", "nu", "exponent", "primality",
                          "factorisation"],
        },
        "search_limits": {"stage1_body_size": 3, "stage2_body_size": 5,
                          "outer_max_size": 5, "unit_cap": 500, "beam": 1200,
                          "dedup": "by value vector on the training objects; "
                                   "bodies on an (n,k) grid"},
        "cost_model": "a formed term counts as size 1 (the Report M finding)",
        "objects": {
            "train_atoms": [2, 3, 4, 5, 7, 8, 9, 11, 13, 16, 17, 19, 23, 25,
                            27, 29],
            "holdout_atoms": [31, 32, 37, 41, 43, 47],
            "reserve_atoms": [49, 64, 81, 121, 125, 128, 169, 243],
        },
        "randomness": "none; the search is deterministic and consumes no RNG",
        "formed_terms_total": res["formed_terms"],
        "certification_rule": (
            "zero error on the Round-1 training atoms AND exact reproduction "
            "of the Round-1 holdout atoms"),
        "certified_terms": certified,
        "promotion_rule_for_round_2": (
            "promote every certified term, plus every formed term appearing as "
            "a NAMED UNIT inside a certified term. Mechanical, applied before "
            "any Round-2 result is seen; no hand selection."),
    }
    (OUT / "round1_manifest.json").write_text(
        json.dumps(manifest, indent=1, sort_keys=True) + "\n")
    print("certified terms (%d):" % len(certified))
    for c in certified:
        print("  %-14s size %d  %s" % (c["target"], c["size"], c["term"]))
    print("\nmanifest hash:", hashlib.sha256(
        (OUT / "round1_manifest.json").read_bytes()).hexdigest()[:32])


if __name__ == "__main__":
    main()
