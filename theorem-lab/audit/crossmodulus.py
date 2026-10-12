#!/usr/bin/env python3
"""
Extra experiment (auditor-initiated): hold out MODULI, not axis ranges.

The audited E experiment calibrates on every modulus it is scored on. This asks the
question that the laboratory never asks: fitted on m <= 30, can any model in the
laboratory's own hypothesis language predict the truth table of an unseen modulus?

Setup: r is fixed at 8 (above every threshold for m <= 48), so the task isolates the
d-axis law. Row features are the laboratory's arithmetic features of m -- no probe
features, because a held-out modulus has no observations by definition. Column features
are the laboratory's arithmetic features of d. Models: constants, atoms, depth-2 Boolean
combinations, and feature-pair quotient tables, exactly as in table_experiment.
"""
import collections
import importlib.util
import itertools
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("lab", HERE.parent / "lab.py")
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)
import functools as _ft
lab.arithmetic_features = _ft.lru_cache(maxsize=None)(lab.arithmetic_features)

R_FIXED, M_TRAIN, M_TEST, D_MAX = 8, 30, 48, 112

proc = subprocess.Popen([sys.executable, str(HERE / "worlds.py"), "--world", "A"],
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                        text=True, bufsize=1)


def truth(m, d):
    proc.stdin.write(json.dumps({"family": "E", "coord": [m, R_FIXED, d],
                                 "op": "full"}, separators=(",", ":")) + "\n")
    proc.stdin.flush()
    return json.loads(proc.stdout.readline())["truth"]


data = {(m, d): truth(m, d) for m in range(1, M_TEST + 1)
        for d in range(1, D_MAX + 1)}
proc.stdin.close()
proc.wait()

train = [((m, d), data[(m, d)]) for m in range(1, M_TRAIN + 1)
         for d in range(1, D_MAX + 1)]
held = [((m, d), data[(m, d)]) for m in range(M_TRAIN + 1, M_TEST + 1)
        for d in range(1, D_MAX + 1)]

state = {"rf": {m: lab.arithmetic_features(m) for m in range(1, M_TEST + 1)},
         "cycles": {}}
names = sorted(state["rf"][1])

models = [{"kind": "constant", "value": v} for v in (False, True)]
atoms = [{"kind": "atom", "op": op, "r": rn, "c": cn}
         for rn in names for cn in names
         for op in ("eq", "le", "divides", "coprime")]
models += atoms


def err(model, pts):
    e = 0
    for (m, d), t in pts:
        try:
            p = lab.predict(model, m, d, state)
        except KeyError:
            p = None
        e += int(p is None or p != t)
    return e


scored = sorted(((err(a, train), lab.canonical(a), a) for a in atoms))
best_atoms = [x[2] for x in scored[:12]]
for l, r in itertools.combinations(best_atoms, 2):
    for op in ("and", "or", "xor"):
        models.append({"kind": "combine", "op": op, "args": [l, r]})
for rn in names:
    for cn in names:
        cells = collections.defaultdict(list)
        for (m, d), t in train:
            cells["%d,%d" % (state["rf"][m][rn],
                             lab.arithmetic_features(d)[cn])].append(t)
        models.append({"kind": "table", "r": rn, "c": cn,
                       "cells": {k: lab.majority(v) for k, v in cells.items()},
                       "default": lab.majority(t for _, t in train)})

results = [(err(mo, train), err(mo, held), mo) for mo in models]
best_train = min(results, key=lambda x: (x[0], x[1]))
best_held = min(results, key=lambda x: x[1])
majority_rate = max(sum(t for _, t in held), len(held) - sum(t for _, t in held))

out = {
    "label": "COMPUTED",
    "question": "fitted on m<=30, predict unseen moduli 31..48 from features of m alone",
    "r_fixed": R_FIXED, "d_max": D_MAX,
    "train_points": len(train), "held_out_points": len(held),
    "majority_class_accuracy_on_held_out": majority_rate / len(held),
    "best_by_training": {
        "model": best_train[2] if best_train[2]["kind"] != "table"
        else {k: v for k, v in best_train[2].items() if k != "cells"},
        "train_accuracy": 1 - best_train[0] / len(train),
        "held_out_accuracy": 1 - best_train[1] / len(held)},
    "best_possible_on_held_out_cheating": {
        "model": best_held[2] if best_held[2]["kind"] != "table"
        else {k: v for k, v in best_held[2].items() if k != "cells"},
        "held_out_accuracy": 1 - best_held[1] / len(held)},
    "models_tried": len(models),
}
print(json.dumps(out, indent=2, sort_keys=True))
(HERE / "crossmodulus.json").write_text(json.dumps(out, indent=2,
                                                   sort_keys=True) + "\n")
