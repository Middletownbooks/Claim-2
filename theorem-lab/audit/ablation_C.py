#!/usr/bin/env python3
"""
Ablation C (Phase 7): the E experiment with no theorem-space history.

No T family, no transport search, no parent theorem identifier — only the E
oracle and the tensor representation search. If the E result depends on
inheritance from T, this must degrade; if it does not, the "recursive
deformation" in the full pipeline is nominal.
"""
import argparse
import importlib.util
import json
from argparse import Namespace
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("lab", HERE.parent / "lab.py")
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)

p = argparse.ArgumentParser()
p.add_argument("--out", required=True)
p.add_argument("--oracle-command", default=None)
p.add_argument("--r", default="8,10,12")
p.add_argument("--d", default="92,102,112")
a = p.parse_args()
R = [int(x) for x in a.r.split(",")]
D = [int(x) for x in a.d.split(",")]

args = Namespace(
    worker=False, oracle="real", oracle_command=a.oracle_command,
    control="C", self_test=False, out=a.out, budget=300000, seed=20250308,
    m_train=24, m_valid=36, m_test=48,
    k_train=24, k_valid=40, k_test=64,
    r_train=R[0], r_valid=R[1], r_test=R[2],
    d_train=D[0], d_valid=D[1], d_test=D[2],
)
out = Path(a.out)
out.mkdir(parents=True, exist_ok=False)
client = lab.Client(args, out)
laboratory = lab.Laboratory(args, client, out)
try:
    entries, diagnostics = lab.tensor_experiment(laboratory, None)
    result = {
        "label": "COMPUTED",
        "ablation": "C: no T family, no transport, no parent theorem",
        "oracle_queries": client.calls,
        "entries": [
            {"id": e["id"], "kind": e["hypothesis"]["kind"],
             "op": e["hypothesis"].get("op"), "status": e["status"],
             "calibration_errors": e["evidence"]["calibration"]["errors"],
             "validation_errors":
                 e["evidence"]["validation_refinement"]["errors"],
             "final_errors": e["evidence"]["final"]["errors"],
             "cost": e["training_symbol_cost"]}
            for e in entries
        ],
        "exports": [c["THEOREM-ID"] for c in laboratory.exports],
    }
    lab.save(out / "ablation_C.json", result)
    print(json.dumps(result, indent=2, sort_keys=True))
finally:
    client.close()
