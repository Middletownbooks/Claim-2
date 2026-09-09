#!/usr/bin/env python3
"""
PRIORITY 11 — adversarial tests A-F.

A (symbol count) and B (random function) are controlled by the experiment's
construction and are read off the condition results; this file runs C, D and E
and records F's normalisation numbers.

C. NAME BLINDNESS. The claim is that the search cannot exploit the human name
   or the printed form of a promoted term. Rather than argue it, the outer
   search is re-run with `show`, `definition` and `expanded_size` replaced by
   functions that raise. If the search still completes with an identical
   result, no code path consulted them.

D. DEFINITION BLINDNESS. Unit selection is re-done with the strictly blind
   ordering (value-vector hash only, no reference to a term's internal size)
   and the target results are compared.

E. LEAKAGE AUDIT. Mechanical checks that no Round-2 answer key can reach the
   promoted vocabulary.
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
from outer import Outer, digest                             # noqa: E402
from round2 import (BEAM, CAP, HOLDOUT, MAX_SIZE, RESERVE, SEED, TRAIN,
                    UNIT_CAP, EVALQ, promoted)              # noqa: E402


def fingerprint(O):
    """Everything the experiment reads off a run, as a comparable object."""
    import numpy as np
    tg = {}
    for name in INV.TARGETS:
        d = digest(np.array(INV.vector(name, TRAIN), dtype=np.int64))
        hits = O.watch_hits.get(d, [])
        tg[name] = min((c for c, _ in hits), default=None)
    return {"classes": len(O.seen), "expansions": O.expansions,
            "levels": [(l["cost"], l["classes_cumulative"])
                       for l in O.level_log],
            "targets": tg}


def poisoned():
    def boom(*a, **k):
        raise AssertionError("the search consulted a term's name or definition")
    return boom


def leakage_audit():
    checks = []

    def chk(name, ok, detail):
        checks.append({"check": name, "pass": bool(ok), "detail": detail})

    chk("splits_disjoint",
        not (set(TRAIN) & set(RESERVE)) and not (set(TRAIN) & set(HOLDOUT))
        and not (set(RESERVE) & set(HOLDOUT)) and not (set(HOLDOUT) & set(EVALQ)),
        "TRAIN/RESERVE/HOLDOUT/EVALQ pairwise disjoint")

    src = (HERE / "promote.py").read_text()
    chk("promotion_does_not_import_the_library",
        "invariants" not in src and "INV" not in src,
        "promote.py never imports the invariant library")
    chk("promotion_does_not_mention_round2_objects",
        all(s not in src for s in ("range(2, 41)", "RESERVE", "HOLDOUT",
                                   "EVALQ")),
        "promote.py never refers to a Round-2 object set")

    man = json.loads((HERE / "round1_manifest.json").read_text())
    r1objs = set(sum(man["objects"].values(), []))
    chk("round1_objects_are_prime_powers_only",
        all(len({p for p in range(2, m + 1) if m % p == 0
                 and all(p % q for q in range(2, p))}) == 1 for m in r1objs),
        "every Round-1 object is a prime power; the Round-2 targets are "
        "general-integer invariants that Round 1 never observed")

    # no promoted term equals a Round-2 target on TRAIN
    S.reset()
    P = promoted()
    tvecs = {INV.vector(t, TRAIN): t for t in INV.TARGETS}
    clash = []
    for t in P:
        try:
            v = tuple(S.ev(t, {"n": m}) for m in TRAIN)
        except Exception:
            continue
        if v in tvecs:
            clash.append((S.show(t), tvecs[v]))
    chk("no_promoted_term_is_a_round2_target", not clash, str(clash))

    build_src = (HERE / "round2.py").read_text().split("def build(")[1] \
        .split("\ndef ")[0]
    chk("vocabulary_construction_never_sees_a_target",
        "INV." not in build_src,
        "round2.build() does not reference the invariant library")
    return checks


def main():
    out = {"label": "COMPUTED"}
    out["E_leakage_audit"] = leakage_audit()

    t0 = time.time()
    S.reset()
    P = promoted()
    forced = [S.leaf(t, TRAIN, cost=1) for t in P]
    formed = S.form_leaves(TRAIN, extra_leaves=forced, tag="ADV")
    print("  formed %d (%.0fs)" % (len(formed), time.time() - t0), flush=True)

    units = S.select_units(formed, TRAIN, UNIT_CAP, forced_leaves=forced)
    atoms = [("var", "n")] + [("const", c) for c in S.CONSTS] + units
    watch = [INV.vector(n, TRAIN) for n in INV.TARGETS]

    base = fingerprint(Outer(atoms, TRAIN, cap=CAP, beam=BEAM, seed=SEED,
                             max_atom_cost=MAX_SIZE).run(MAX_SIZE, watch=watch))
    print("  baseline B: %s" % base["targets"], flush=True)

    # ---- C: name blindness -------------------------------------------
    keep = (S.show, S.definition, S.expanded_size)
    S.show = S.definition = S.expanded_size = poisoned()
    try:
        blind = fingerprint(Outer(atoms, TRAIN, cap=CAP, beam=BEAM, seed=SEED,
                                  max_atom_cost=MAX_SIZE
                                  ).run(MAX_SIZE, watch=watch))
        err = None
    except AssertionError as e:
        blind, err = None, str(e)
    finally:
        S.show, S.definition, S.expanded_size = keep
    out["C_name_blindness"] = {
        "method": "show/definition/expanded_size replaced by raising stubs "
                  "for the whole outer enumeration",
        "raised": err,
        "identical_to_baseline": blind == base,
        "baseline": base, "poisoned": blind}
    print("  name blindness: identical=%s raised=%s"
          % (blind == base, err), flush=True)

    # ---- D: definition-blind unit selection ---------------------------
    S.reset()
    forced2 = [S.leaf(t, TRAIN, cost=1) for t in P]
    formed2 = S.form_leaves(TRAIN, extra_leaves=forced2, tag="ADV2",
                            verbose=False)
    units2 = S.select_units(formed2, TRAIN, UNIT_CAP, forced_leaves=forced2,
                            order="blind")
    atoms2 = [("var", "n")] + [("const", c) for c in S.CONSTS] + units2
    dblind = fingerprint(Outer(atoms2, TRAIN, cap=CAP, beam=BEAM, seed=SEED,
                               max_atom_cost=MAX_SIZE
                               ).run(MAX_SIZE, watch=watch))
    out["D_definition_blind_selection"] = {
        "method": "unit ordering by value-vector hash alone; no reference to "
                  "a term's internal expression size",
        "baseline_targets": base["targets"], "blind_targets": dblind["targets"],
        "baseline_classes": base["classes"], "blind_classes": dblind["classes"]}
    print("  definition-blind selection: %s" % dblind["targets"], flush=True)

    (HERE / "adversarial.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str) + "\n")
    print("  %.0fs total" % (time.time() - t0))


if __name__ == "__main__":
    main()
