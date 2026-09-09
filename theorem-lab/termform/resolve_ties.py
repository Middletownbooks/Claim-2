#!/usr/bin/env python3
"""
P5: the term search over-generates (32 minimal terms on a one-atom branch,
5 on another). Feed the ties to the standard disagreement stage and see whether
probing the declared reserve picks a generalizing term.
"""
import importlib.util as ilu
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = ilu.spec_from_file_location("stage_dis",
                                   HERE.parent / "stages" / "disagreement.py")
stage = ilu.module_from_spec(spec)
sys.modules["stage_dis"] = stage
spec.loader.exec_module(stage)

from run import HOLDOUT, RESERVE, TRAIN, Oracle          # noqa: E402
from run2 import CONDS, branch_of                        # noqa: E402
from synth2 import ev, form_leaves, show, size, synthesize  # noqa: E402


def main():
    oracle = Oracle()
    obs = {m: oracle.period(m) for m in TRAIN + HOLDOUT + RESERVE}
    oracle.close()

    formed = form_leaves(TRAIN, verbose=False)
    out = {"branches": {}}
    for name, cond in CONDS:
        atoms = [m for m in TRAIN if branch_of(m) == name]
        if not atoms:
            continue
        target = [obs[m] for m in atoms]
        terms, _ = synthesize(atoms, target, formed, max_size=6)
        hold = [m for m in HOLDOUT if branch_of(m) == name]
        reserve = [m for m in RESERVE if branch_of(m) == name]
        stage.assert_disjoint(reserve, HOLDOUT)

        def gen(t):
            return all(ev(t, {"n": m}) == obs[m] for m in hold) if hold else None

        rec = {"atoms": len(atoms), "minimal_terms": len(terms),
               "generalizing_before": sum(1 for t in terms if gen(t)),
               "reserve_available": reserve}
        if len(terms) > 1 and reserve:
            res = stage.resolve(
                terms, lambda t: 0,
                lambda t, m: ev(t, {"n": m}),
                reserve, lambda m: obs[m], max_probes=4)
            rec["stage"] = res.to_json()
            surv = res.survivors
            rec["survivors_after"] = len(surv)
            rec["generalizing_after"] = sum(1 for t in surv if gen(t))
            rec["verdict"] = res.verdict
            rec["selected"] = show(res.selected) if res.selected else None
        else:
            rec["verdict"] = "NO_TIE" if len(terms) <= 1 else "NO_RESERVE"
        out["branches"][name] = rec
        print("%-14s atoms=%2d terms=%3d gen_before=%3d %s" % (
            name, len(atoms), len(terms), rec["generalizing_before"],
            rec.get("verdict", "")), end="")
        if "survivors_after" in rec:
            print(" -> survivors=%d gen_after=%d probes=%d" % (
                rec["survivors_after"], rec["generalizing_after"],
                rec["stage"]["probes_used"]), end="")
        print()
        if rec.get("selected"):
            print("      selected: %s  generalizes=%s" % (
                rec["selected"], gen(res.selected)))
    (HERE / "resolve_ties.json").write_text(json.dumps(out, indent=1,
                                                       sort_keys=True))


if __name__ == "__main__":
    main()
