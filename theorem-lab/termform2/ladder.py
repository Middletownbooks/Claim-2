#!/usr/bin/env python3
"""
PRIORITY 6 / PRIORITY 12 — the vocabulary ladder V0 -> V1 -> V2 -> V3.

Every rung uses the SAME procedure and the SAME budget. The only thing that
changes is the carried-over vocabulary. The certification and promotion rules
are fixed here, before any rung is run, and are the Round-1 rules unchanged:

  CERTIFY  a term is certified at a rung iff its values match an invariant in
           the independent library exactly on TRAIN, then on RESERVE, and then
           on HOLDOUT (evaluated once, after the term is frozen); and the
           invariant was NOT already reached at this budget by the previous
           rung's vocabulary.  ("novel at this rung")
  PROMOTE  every certified term, plus every named unit appearing inside a
           certified term. Mechanical; no hand selection.

The ladder is untargeted: no rung is told what to look for.

ONE TURN OF ABSTRACTION PER RUNG. Each rung runs stage-1 formation only.
Round 1's own procedure has two stages, and stage 2 builds on stage 1's formed
terms as units -- so a single round already contains two turns of the loop the
ladder is trying to observe, which is why the Round-2 conditions show no
carry-over effect: whatever Round 1 formed, Round 2 re-forms inside itself. The
ladder holds each rung to one turn so that compounding, if it exists, has to
cross a rung boundary to appear. This is a deliberate weakening of each rung,
declared here, and it applies identically to every rung including V0.
"""
import ast
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "termform"))
sys.path.insert(0, str(HERE.parent))

import invariants as INV                                    # noqa: E402
import synth3 as S                                          # noqa: E402
from outer import Outer                                     # noqa: E402
from round2 import (BEAM, CAP, HOLDOUT, MAX_SIZE, RESERVE, SEED, TRAIN,
                    UNIT_CAP, promoted)                     # noqa: E402

LADDER_CAP = int(sys.argv[1]) if len(sys.argv) > 1 else 20000000

LIB_TRAIN = {}
for _nm, _f in INV.LIBRARY.items():
    try:
        LIB_TRAIN[tuple(_f(m) for m in TRAIN)] = _nm
    except Exception:
        pass


def rung(vocab, tag):
    """Run one rung: form, select atoms, enumerate, certify."""
    S.reset()
    t0 = time.time()
    forced = [S.leaf(t, TRAIN, cost=1) for t in vocab]
    formed = S.form_leaves(TRAIN, extra_leaves=forced, tag=tag, levels=1)
    units = S.select_units(formed, TRAIN, UNIT_CAP, forced_leaves=forced)
    atoms = [("var", "n")] + [("const", c) for c in S.CONSTS] + units
    O = Outer(atoms, TRAIN, cap=LADDER_CAP, beam=BEAM, seed=SEED,
              max_atom_cost=MAX_SIZE).run(MAX_SIZE)

    certified = {}
    pool = [i for idxs in O.samples.values() for i in idxs]
    pool += [i for idxs in O.by_size.values() for i in idxs]
    for i in pool:
        t = O.term_of(i)
        try:
            v = tuple(S.ev(t, {"n": m}) for m in TRAIN)
        except Exception:
            continue
        nm = LIB_TRAIN.get(v)
        if nm is None or nm in certified:
            continue
        try:
            ok_r = all(S.ev(t, {"n": m}) == INV.LIBRARY[nm](m) for m in RESERVE)
            ok_h = all(S.ev(t, {"n": m}) == INV.LIBRARY[nm](m) for m in HOLDOUT)
        except Exception:
            continue
        if not (ok_r and ok_h):
            continue
        certified[nm] = {"invariant": nm, "cost": S.size(t),
                         "term": S.show(t), "expanded": S.expand(t),
                         "uses_carried_over": "<" in S.show(t)}
    return {
        "tag": tag, "vocabulary_size": len(vocab), "formed": len(formed),
        "atoms": len(atoms), "classes_TRAIN": len(O.seen),
        "expansions": O.expansions, "levels": O.level_log,
        "certified": certified, "seconds": round(time.time() - t0, 1),
    }


def promote_from(certified):
    """The frozen promotion rule applied to a rung's NOVEL certified terms."""
    out, seen = [], set()
    for nm in sorted(certified):
        for t in _units_of(certified[nm]["expanded"]):
            if repr(t) not in seen:
                seen.add(repr(t))
                out.append(t)
    return out


def _units_of(t):
    """A certified term, plus every quantifier sub-term inside it: the tuple-
    level equivalent of Round 1's `<...>` named units."""
    out, stack = [t], [t]
    while stack:
        x = stack.pop()
        for a in x[1:]:
            if isinstance(a, tuple):
                if a[0] in ("least", "count"):
                    out.append(a)
                stack.append(a)
    return out


def main():
    V, results, seen_names = {0: []}, {}, set()
    for k in (0, 1, 2, 3):
        r = rung(V[k], "V%d" % k)
        new = {n: v for n, v in r["certified"].items() if n not in seen_names}
        r["novel_at_this_rung"] = sorted(new)
        r["novel_using_carried_vocabulary"] = sorted(
            n for n, v in new.items() if v["uses_carried_over"])
        seen_names |= set(r["certified"])
        results["V%d" % k] = r
        print("V%d vocab=%-3d atoms=%-4d classes=%-9d certified=%-3d novel=%s"
              % (k, len(V[k]), r["atoms"], r["classes_TRAIN"],
                 len(r["certified"]), r["novel_at_this_rung"]), flush=True)
        if k < 3:
            add = promote_from(new)
            r["promoted_to_next"] = [repr(t) for t in add]
            V[k + 1] = V[k] + add

    # is the Round-1 promoted vocabulary a subset of what rung 0 reaches?
    S.reset()
    P = promoted()
    v0names = set(results["V0"]["certified"])
    out = {"label": "COMPUTED",
           "design": "one turn of abstraction per rung (stage-1 formation "
                     "only); the vocabulary carried across rung boundaries is "
                     "the only thing that changes",
           "certification_rule":
               "exact match to an independent library invariant on TRAIN, then "
               "RESERVE, then HOLDOUT; novel = not certified at an earlier rung",
           "promotion_rule":
               "every novel certified term plus every quantifier sub-term "
               "inside it; mechanical, no hand selection",
           "round1_promoted_terms": len(P),
           "rung0_certified_invariants": sorted(v0names),
           "rungs": results}
    (HERE / "ladder.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=repr) + "\n")
    print("wrote ladder.json")


if __name__ == "__main__":
    main()
