#!/usr/bin/env python3
"""
Ladder control: is rung V1's extra invariant OUTSIDE R(V0), or just outside
V0's beam?

The rungs are not budget-matched and cannot be. V0's stage-1 formation yields
35 units, V1's yields 480, so V0 enters its outer search with 40 atoms against
V1's 493 and spends ~880 000 candidate expansions against ~13 200 000. The
vocabulary causes that gap -- that IS the mechanism under test -- but it means
a difference in what the two rungs certify could be a difference in search
size rather than in reachability.

V0's space is small enough to settle it outright: with 40 atoms the whole
cost-<=5 space is about 10.4 million candidates, so it can be enumerated with
the beam effectively switched off. Anything V1 certifies that an UNBEAMED V0
still cannot reach is outside R(V0), full stop.
"""
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
from round2 import HOLDOUT, MAX_SIZE, RESERVE, SEED, TRAIN   # noqa: E402


def main():
    t0 = time.time()
    S.reset()
    formed = S.form_leaves(TRAIN, tag="V0x", levels=1)
    units = [S.leaf(t, TRAIN) for t in formed.values()]
    atoms = [("var", "n")] + [("const", c) for c in S.CONSTS] + units
    print("V0 unbeamed: %d atoms" % len(atoms), flush=True)
    O = Outer(atoms, TRAIN, cap=20000000, beam=10 ** 9, seed=SEED,
              max_atom_cost=MAX_SIZE).run(MAX_SIZE)
    print("  %d classes, %d expansions, truncated=%s (%.0fs)"
          % (len(O.seen), O.expansions, O.truncated, time.time() - t0),
          flush=True)

    lib = {}
    for nm, f in INV.LIBRARY.items():
        try:
            lib[tuple(f(m) for m in TRAIN)] = nm
        except Exception:
            pass
    found = {}
    pool = [i for idxs in O.samples.values() for i in idxs]
    pool += [i for idxs in O.by_size.values() for i in idxs]
    for i in pool:
        t = O.term_of(i)
        try:
            v = tuple(S.ev(t, {"n": m}) for m in TRAIN)
        except Exception:
            continue
        nm = lib.get(v)
        if nm is None or nm in found:
            continue
        try:
            ok = all(S.ev(t, {"n": m}) == INV.LIBRARY[nm](m)
                     for m in RESERVE + HOLDOUT)
        except Exception:
            continue
        if ok:
            found[nm] = {"cost": S.size(t), "term": S.show(t)}

    ladder = json.loads((HERE / "ladder.json").read_text())
    v1 = set(ladder["rungs"]["V1"]["certified"])
    out = {"label": "COMPUTED",
           "question": "does an UNBEAMED V0 reach what V1 certified?",
           "v0_unbeamed": {"atoms": len(atoms), "classes": len(O.seen),
                           "expansions": O.expansions,
                           "truncated": O.truncated,
                           "certified": {k: v for k, v in sorted(found.items())}},
           "v1_certified": sorted(v1),
           "in_V1_not_in_unbeamed_V0": sorted(v1 - set(found)),
           "in_unbeamed_V0_not_in_V1": sorted(set(found) - v1)}
    (HERE / "ladder_control.json").write_text(
        json.dumps(out, indent=1, sort_keys=True) + "\n")
    print("  unbeamed V0 certifies %d: %s" % (len(found), sorted(found)))
    print("  in V1 but NOT in unbeamed V0: %s" % out["in_V1_not_in_unbeamed_V0"])


if __name__ == "__main__":
    main()
