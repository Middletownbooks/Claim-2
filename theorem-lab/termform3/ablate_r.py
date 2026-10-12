#!/usr/bin/env python3
"""
The sharpest challenge to Report R's compounding claim.

Rung 2 certified `is_cube` as
  (<is_prime_power> % gcd(<tau-1>, <floor_n_3 helper>))
where `is_prime_power` is the invariant rung 1 discovered BECAUSE of its carried
vocabulary. If that reading is right, deleting exactly that one term from rung 2's
carried set should cost rung 2 its discovery, while deleting an unrelated carried
term of the same count should not.

Two ablations, each an unbeamed exhaustive cost-5 search at body budget 3:
  minus_enabled  -- rung 2's carried set without the rung-1 enablements
  minus_other    -- rung 2's carried set without the same NUMBER of other terms
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "termform"))
sys.path.insert(0, str(HERE.parent / "termform2"))

from ladder_r import promote_from, run_rung                  # noqa: E402
from promote import parse                                    # noqa: E402

ENABLED = ["is_prime_power", "odd_divisors"]


def main():
    lad = json.loads((HERE / "ladder_r_seeded.json").read_text())
    rung1 = next(r for r in lad["rungs"] if r["rung"] == 1)
    rung2 = next(r for r in lad["rungs"] if r["rung"] == 2)
    full = promote_from(rung1["certified"])
    enabled_terms = {rung1["certified"][n]["term"] for n in ENABLED}
    # printed forms of the promoted set that ARE an enablement (markers stripped)
    def bare(s):
        return s.replace("<", "").replace(">", "")
    drop_enabled = {p for p, _ in full if bare(p) in {bare(e) for e in enabled_terms}}
    assert len(drop_enabled) == len(ENABLED), (drop_enabled, enabled_terms)

    out = {"label": "ABLATION_R", "rung2_baseline": {
        "carried": rung2["carried"], "certified": rung2["certified_count"],
        "is_cube": "is_cube" in rung2["certified"]}}

    minus_enabled = [(p, t) for p, t in full if p not in drop_enabled]
    r, _, _ = run_rung(minus_enabled, "ablate_minus_enabled",
                       "rung 2's carried set without the rung-1 enablements")
    out["minus_enabled"] = {"carried": r["carried"], "atoms": r["atoms"],
                            "classes": r["classes"], "exhausted": r["exhausted"],
                            "certified": r["certified_count"],
                            "is_cube": "is_cube" in r["certified"],
                            "net_new": r["net_new"]}
    print("minus_enabled: %d carried, %d certified, is_cube=%s"
          % (r["carried"], r["certified_count"], "is_cube" in r["certified"]), flush=True)

    # drop the same number of OTHER carried terms: the last two in promotion order
    # that are neither an enablement nor one of Report Q's seven reach extensions
    cert = json.loads((HERE / "certificate.json").read_text())["certified_out_of_reach"]
    protect = {bare(x) for x in cert} | {bare(e) for e in enabled_terms}
    others = [p for p, _ in full if bare(p) not in protect]
    drop_other = set(others[-len(ENABLED):])
    minus_other = [(p, t) for p, t in full if p not in drop_other]
    r2, _, _ = run_rung(minus_other, "ablate_minus_other",
                        "rung 2's carried set without two unrelated terms")
    out["minus_other"] = {"carried": r2["carried"], "atoms": r2["atoms"],
                          "classes": r2["classes"], "exhausted": r2["exhausted"],
                          "certified": r2["certified_count"],
                          "is_cube": "is_cube" in r2["certified"],
                          "dropped": sorted(drop_other),
                          "net_new": r2["net_new"]}
    print("minus_other:   %d carried, %d certified, is_cube=%s  (dropped %s)"
          % (r2["carried"], r2["certified_count"], "is_cube" in r2["certified"],
             sorted(drop_other)), flush=True)

    out["verdict"] = (
        "compounding chain confirmed" if (not out["minus_enabled"]["is_cube"]
                                          and out["minus_other"]["is_cube"])
        else "chain NOT confirmed: read the two rows")
    (HERE / "ablation_r.json").write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print("\n%s" % out["verdict"])


if __name__ == "__main__":
    main()
