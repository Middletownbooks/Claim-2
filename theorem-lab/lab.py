#!/usr/bin/env python3
"""
Blind theorem-discovery laboratory.

Python >= 3.9; standard library only.
No result in this file is a claim of execution or formal verification.

Default:
    python lab.py --oracle real --control C --out run-real-C

Synthetic control:
    python lab.py --self-test --out run-synthetic

An external worker may be supplied with:
    --oracle-command "python private_worker.py"

Worker protocol:
    one JSON request per line, one JSON response per line.
    request = {"family": "T"|"E"|"U",
               "coord": [m,k] or [m,r,d],
               "op": "full"|"witness"}
"""

import argparse
import collections
import hashlib
import itertools
import json
import math
import platform
import shlex
import subprocess
import sys
import zlib
from pathlib import Path


# ------------------------- Serialization -------------------------

def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False)


def digest(x):
    return hashlib.sha256(canonical(x).encode("utf-8")).hexdigest()


def save(path, x):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(x, f, indent=2, sort_keys=True, ensure_ascii=False)
        f.write("\n")


def majority(xs):
    xs = list(xs)
    return sum(bool(x) for x in xs) * 2 > len(xs)


# ------------------------- ORACLE-ONLY CODE -------------------------
# The discovery code below does not call oracle_answer.
# Auxiliary knowledge here:
#   - modular exponentiation implements the predicate definition;
#   - gcd implements the definition of the unit-restricted domain.
# There is no theorem-based implementation of a real oracle.

def oracle_answer(mode, request):
    family = request["family"]
    coord = tuple(int(x) for x in request["coord"])
    op = request.get("op", "full")

    if family not in ("T", "E", "U"):
        raise ValueError("Unknown family")
    if op not in ("full", "witness"):
        raise ValueError("Unknown operation")
    if len(coord) != (3 if family == "E" else 2):
        raise ValueError("Wrong arity")
    if any(x < 1 for x in coord):
        raise ValueError("All parameters must be positive")

    m = coord[0]

    # This branch is a separate toy world. It is never used for real queries.
    # Its hidden law is intentionally available to the test designer,
    # but is not passed to the discovery algorithms.
    if mode == "synthetic":
        if family == "E":
            _, r, d = coord
            hidden = (r >= 1 + m % 3) and (d % (2 + m % 4) == 0)
        else:
            _, k = coord
            hidden = ((m % 3) == (k % 3)) != (m % 2 == 0)

        # Artificial residue instrumentation, not modular arithmetic.
        def outcome(x):
            return bool(hidden or x != 0)

    else:
        if family == "E":
            _, r, d = coord

            def outcome(x):
                return pow(x, r + d, m) == pow(x, r, m)
        else:
            _, k = coord

            def outcome(x):
                if family == "U" and math.gcd(x, m) != 1:
                    return None
                return pow(x, k, m) == x

    profile = []
    checked = 0
    witness = None
    for x in range(m):
        y = outcome(x)
        profile.append(y)
        if y is not None:
            checked += 1
        if y is False and witness is None:
            witness = x
            if op == "witness":
                return {"witness": witness, "evaluated": checked}

    if op == "witness":
        return {"witness": None, "evaluated": checked}

    failures = sum(y is False for y in profile)
    successes = sum(y is True for y in profile)
    return {
        "truth": failures == 0,
        "witness": witness,
        "fail_count": failures,
        "pass_count": successes,
        "profile": profile,
        "evaluated": checked,
    }


def worker_main(mode):
    for line in sys.stdin:
        try:
            response = oracle_answer(mode, json.loads(line))
        except Exception as exc:
            response = {"error": repr(exc)}
        print(canonical(response), flush=True)


# ------------------------- BLACK-BOX CLIENT -------------------------

class Client:
    def __init__(self, args, out):
        if args.oracle_command:
            command = shlex.split(args.oracle_command)
        else:
            command = [
                sys.executable, str(Path(__file__).resolve()),
                "--worker", "--oracle", args.oracle,
            ]
        self.proc = subprocess.Popen(
            command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            text=True, bufsize=1
        )
        self.log = open(out / "oracle.jsonl", "w", encoding="utf-8")
        self.cache = {}
        self.budget = args.budget
        self.calls = 0
        self.hits = collections.Counter()
        self.phases = collections.Counter()

    @staticmethod
    def key(family, coord, op="full"):
        return (family, tuple(coord), op)

    def get(self, family, coord, phase, op="full"):
        key = self.key(family, coord, op)
        if key in self.cache:
            self.hits[phase] += 1
            return self.cache[key]

        if self.calls >= self.budget:
            raise RuntimeError("Unique oracle-query budget exhausted")

        request = {"family": family, "coord": list(coord), "op": op}
        self.proc.stdin.write(canonical(request) + "\n")
        self.proc.stdin.flush()
        line = self.proc.stdout.readline()
        if not line:
            raise RuntimeError("Oracle process terminated")
        answer = json.loads(line)
        if "error" in answer:
            raise RuntimeError(answer["error"])

        self.calls += 1
        self.phases[phase] += 1
        answer["_query_id"] = self.calls
        self.cache[key] = answer
        self.log.write(canonical({
            "label": "OBSERVED",
            "id": self.calls,
            "first_phase": phase,
            "request": request,
            "response": answer,
        }) + "\n")
        self.log.flush()
        return answer

    def query(self, m, k, phase="query"):
        return self.get("T", (m, k), phase)["truth"]

    def query_witness(self, m, k, phase="query_witness"):
        return self.get("T", (m, k), phase, "witness")["witness"]

    def close(self):
        self.log.close()
        if self.proc.stdin:
            self.proc.stdin.close()
        try:
            self.proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.proc.terminate()
            self.proc.wait()


# ------------------------- GENERIC FEATURE LANGUAGE -------------------------
# Same arithmetic vocabulary on both axes.
# No factorization, multiplicative-order computation, or special
# aggregate over factors occurs here.

def arithmetic_features(n):
    f = {"n": n}
    for s in range(1, 4):
        f["add:%d" % s] = n + s
        f["sub:%d" % s] = max(0, n - s)
    for q in range(2, 7):
        f["mod:%d" % q] = n % q
        f["gcd:%d" % q] = math.gcd(n, q)
    for q in range(2, 5):
        f["quo:%d" % q] = n // q
    for q in range(4):
        f["const:%d" % q] = q
    return f


def boolop(op, a, b):
    if a is None or b is None:
        return None
    if op == "and":
        return bool(a and b)
    if op == "or":
        return bool(a or b)
    if op == "xor":
        return bool(a) != bool(b)
    if op == "iff":
        return bool(a) == bool(b)
    raise ValueError(op)


def atomic(op, a, b):
    if op == "eq":
        return a == b
    if op == "le":
        return a <= b
    if op == "divides":
        return a != 0 and b % a == 0
    if op == "coprime":
        return math.gcd(a, b) == 1
    raise ValueError(op)


# ------------------------- ONE-DIMENSIONAL REPRESENTATIONS -------------------
# Search all exact prefix + repeating-block descriptions.
# A discovered repeating block needs two observed copies.
# If none exists, retain the full prefix and use a declared,
# speculative majority continuation. Absence of a positive observation
# is never interpreted as a proof of permanent absence.

def sequence_cost(model):
    return 2 + len(model["prefix"]) + len(model["cycle"])


def fit_sequence(values):
    values = list(map(bool, values))
    n = len(values)
    candidates = []
    for t in range(n):
        for p in range(1, (n - t) // 2 + 1):
            block = values[t:t + p]
            if all(values[i] == block[(i - t) % p]
                   for i in range(t, n)):
                candidates.append({
                    "prefix": values[:t],
                    "cycle": block,
                    "observed_repetitions": (n - t) // p,
                    "continuation_status": "CONJECTURED",
                })
    if candidates:
        return min(candidates, key=lambda q: (
            sequence_cost(q), len(q["prefix"]), len(q["cycle"]),
            canonical(q)
        ))
    return {
        "prefix": values,
        "cycle": [majority(values)],
        "observed_repetitions": 0,
        "continuation_status": "CONJECTURED",
    }


def sequence_predict(model, coordinate):
    i = coordinate - 1
    prefix = model["prefix"]
    if i < len(prefix):
        return prefix[i]
    cycle = model["cycle"]
    return cycle[(i - len(prefix)) % len(cycle)]


def row_features(m, records, cycle):
    f = arithmetic_features(m)
    truths = [r["truth"] for r in records]
    failures = [i + 1 for i, y in enumerate(truths) if not y]
    positives = [i + 1 for i, y in enumerate(truths) if y]
    f.update({
        "probe:true_count": sum(truths),
        "probe:first_true": min(positives, default=0),
        "probe:first_false": min(failures, default=0),
        "probe:total_failures": sum(r["fail_count"] for r in records),
        "probe:onset": len(cycle["prefix"]),
        "probe:period": len(cycle["cycle"]),
        "probe:cycle_positives": sum(cycle["cycle"]),
    })
    return f


# ------------------------- MODEL LANGUAGE -------------------------

def predict(model, m, k, state):
    kind = model["kind"]
    if kind == "constant":
        return model["value"]
    if kind == "atom":
        return atomic(
            model["op"], state["rf"][m][model["r"]],
            arithmetic_features(k)[model["c"]]
        )
    if kind == "combine":
        return boolop(
            model["op"],
            predict(model["args"][0], m, k, state),
            predict(model["args"][1], m, k, state),
        )
    if kind == "cycles":
        return sequence_predict(state["cycles"][m], k)
    if kind == "table":
        a = state["rf"][m][model["r"]]
        b = arithmetic_features(k)[model["c"]]
        return model["cells"].get("%d,%d" % (a, b), model["default"])
    raise ValueError(kind)


def model_cost(model, state, train_rows):
    kind = model["kind"]
    if kind == "constant":
        return 1
    if kind == "atom":
        return 3
    if kind == "combine":
        return 1 + sum(model_cost(x, state, train_rows)
                       for x in model["args"])
    if kind == "cycles":
        return 1 + sum(sequence_cost(state["cycles"][m])
                       for m in train_rows)
    if kind == "table":
        return 3 + 3 * len(model["cells"])
    raise ValueError(kind)


def requires_probes(model):
    kind = model["kind"]
    if kind == "cycles":
        return True
    if kind in ("atom", "table"):
        return model["r"].startswith("probe:")
    if kind == "combine":
        return any(requires_probes(x) for x in model["args"])
    return False


# ------------------------- EVIDENCE / FALSIFICATION -------------------------

def observable_structure(coord, record):
    """A coarse, preregistered observational signature, not a cause."""
    if record["truth"]:
        return canonical(["true"])
    m = coord[0]
    w = record["witness"]
    size = record["fail_count"] + record["pass_count"]
    return canonical([
        "false",
        w == 0,
        math.gcd(w, m) == 1,
        (4 * record["fail_count"]) // max(1, size),
    ])


def summarize(points, predictor, training_structures):
    result = {
        "label": "COMPUTED",
        "tests": len(points),
        "supporting": 0,
        "errors": 0,
        "abstentions": 0,
        "support_examples": [],
        "smallest_counterexample": None,
        "dataset_hash": digest([
            [list(c), r["truth"], r["_query_id"]] for c, r in points
        ]),
    }
    for coord, raw in points:
        p = predictor(coord)
        if p is None:
            result["abstentions"] += 1
            result["errors"] += 1
            continue
        if p == raw["truth"]:
            result["supporting"] += 1
            if len(result["support_examples"]) < 3:
                result["support_examples"].append({
                    "coord": list(coord), "query_id": raw["_query_id"]
                })
        else:
            result["errors"] += 1
            structure = observable_structure(coord, raw)
            ce = {
                "label": "COMPUTED",
                "coord": list(coord),
                "prediction": p,
                "observed": raw["truth"],
                "least_witness": raw["witness"],
                "query_id": raw["_query_id"],
                "observable_structure": structure,
                "structurally_novel": structure not in training_structures,
                "novelty_reference": "training observational signatures",
            }
            old = result["smallest_counterexample"]
            if old is None or tuple(ce["coord"]) < tuple(old["coord"]):
                result["smallest_counterexample"] = ce
    return result


def refresh_entry(entry):
    evidence = list(entry["evidence"].values())
    entry["number_of_tests"] = sum(x["tests"] for x in evidence)
    entry["evidence_supporting"] = sum(x["supporting"] for x in evidence)
    ces = [x["smallest_counterexample"] for x in evidence
           if x["smallest_counterexample"] is not None]
    entry["smallest_counterexample"] = (
        min(ces, key=lambda x: tuple(x["coord"])) if ces else None
    )
    if ces:
        entry["status"] = "REFUTED"
    elif any(x.get("abstentions", 0) for x in evidence):
        entry["status"] = "INCOMPLETE"
    else:
        entry["status"] = "UNREFUTED_ON_TESTED_DATA"


# ------------------------- INVARIANT SEARCH -------------------------

def invariant_search(objects, feature_map, signatures):
    names = sorted(feature_map[objects[0]])

    def score(features):
        groups = collections.defaultdict(list)
        for x in objects:
            key = tuple(feature_map[x][f] for f in features)
            groups[key].append(x)

        comparable = 0
        collisions = 0
        for members in groups.values():
            n = len(members)
            comparable += n * (n - 1) // 2
            counts = collections.Counter(signatures[x] for x in members)
            equal = sum(v * (v - 1) // 2 for v in counts.values())
            collisions += n * (n - 1) // 2 - equal

        quality = (
            collisions / max(1, comparable)
            + 0.05 * len(groups) / len(objects)
            + 0.001 * len(features)
        )
        return {
            "label": "COMPUTED",
            "features": list(features),
            "groups": len(groups),
            "comparable_pairs": comparable,
            "contradictory_pairs": collisions,
            "quality_score": quality,
            "vacuous": comparable == 0,
            "requires_row_probes": any(
                f.startswith("probe:") for f in features
            ),
        }

    singles = [score((f,)) for f in names]
    best = sorted(singles, key=lambda x: (
        x["quality_score"], x["features"]
    ))[:8]
    pair_names = [x["features"][0] for x in best]
    pairs = [score(p) for p in itertools.combinations(pair_names, 2)]

    classes = collections.defaultdict(list)
    for x in objects:
        classes[signatures[x]].append(x)
    return {
        "label": "COMPUTED",
        "scope": "observational equivalence on training coordinates only",
        "candidates": sorted(singles + pairs, key=lambda x: (
            x["quality_score"], x["features"]
        )),
        "signature_classes": [
            {"members": members, "signature": list(sig)}
            for sig, members in sorted(classes.items())
        ],
    }


def exception_search(points):
    partitions = {}
    failed = [(c, r) for c, r in points if not r["truth"]]

    functions = {
        "least_witness": lambda c, r: r["witness"],
        "witness_gcd": lambda c, r: math.gcd(r["witness"], c[0]),
        "coarse_profile": lambda c, r: observable_structure(c, r),
    }
    for q in range(2, 7):
        functions["column_mod_%d_and_witness_unit" % q] = (
            lambda c, r, q=q:
            (c[-1] % q, math.gcd(r["witness"], c[0]) == 1)
        )

    for name, function in functions.items():
        groups = collections.defaultdict(list)
        for coord, raw in failed:
            groups[canonical(function(coord, raw))].append((coord, raw))
        partitions[name] = [{
            "key": key,
            "count": len(items),
            "distinct_moduli": len({c[0] for c, _ in items}),
            "examples": [
                {"coord": list(c), "query_id": r["_query_id"]}
                for c, r in items[:5]
            ],
        } for key, items in sorted(groups.items())]

    return {
        "label": "COMPUTED",
        "interpretation": (
            "Clusters of observables; shared causal mechanisms are not proved."
        ),
        "failure_instances": len(failed),
        "partitions": partitions,
    }


# ------------------------- LEAN-TYPE RENDERING -------------------------
# Output consists of proposition definitions. No proof is generated.

def lean_or(parts):
    return "(" + " ∨ ".join(parts) + ")" if parts else "False"


def lean_bool(op, a, b):
    if op == "and":
        return "(%s ∧ %s)" % (a, b)
    if op == "or":
        return "(%s ∨ %s)" % (a, b)
    if op == "xor":
        return "((%s ∧ ¬ %s) ∨ (¬ %s ∧ %s))" % (a, b, a, b)
    if op == "iff":
        return "(%s ↔ %s)" % (a, b)
    raise ValueError(op)


def lean_sequence(model, variable):
    prefix = model["prefix"]
    cycle = model["cycle"]
    pieces = [
        "(%s = %d)" % (variable, i + 1)
        for i, value in enumerate(prefix) if value
    ]
    start = len(prefix) + 1
    residues = [
        "((%s - %d) %% %d = %d)" %
        (variable, start, len(cycle), j)
        for j, value in enumerate(cycle) if value
    ]
    if residues:
        pieces.append("(%d ≤ %s ∧ %s)" %
                      (start, variable, lean_or(residues)))
    return lean_or(pieces)


def lean_feature(variable, name, state):
    if name == "n":
        return variable
    kind, text = name.split(":", 1)
    if kind == "probe":
        tail = "0"
        for m in sorted(state["rf"], reverse=True):
            tail = "(if %s = %d then %d else %s)" % (
                variable, m, state["rf"][m][name], tail
            )
        return tail
    n = int(text)
    if kind == "const":
        return str(n)
    if kind == "gcd":
        return "(Nat.gcd %s %d)" % (variable, n)
    op = {"add": "+", "sub": "-", "mod": "%", "quo": "/"}[kind]
    return "(%s %s %d)" % (variable, op, n)


def lean_model(model, state):
    kind = model["kind"]
    if kind == "constant":
        return "True" if model["value"] else "False"
    if kind == "cycles":
        return lean_or([
            "(m = %d ∧ %s)" % (m, lean_sequence(q, "k"))
            for m, q in sorted(state["cycles"].items())
        ])
    if kind == "combine":
        return lean_bool(
            model["op"], lean_model(model["args"][0], state),
            lean_model(model["args"][1], state)
        )

    a = lean_feature("m", model["r"], state)
    b = lean_feature("k", model["c"], state)
    if kind == "atom":
        op = model["op"]
        if op == "eq":
            return "(%s = %s)" % (a, b)
        if op == "le":
            return "(%s ≤ %s)" % (a, b)
        if op == "divides":
            return "(%s ≠ 0 ∧ %s %% %s = 0)" % (a, b, a)
        return "(Nat.gcd %s %s = 1)" % (a, b)

    if kind == "table":
        exceptional_cells = []
        for key, value in sorted(model["cells"].items()):
            if value != model["default"]:
                x, y = map(int, key.split(","))
                exceptional_cells.append(
                    "(%s = %d ∧ %s = %d)" % (a, x, b, y)
                )
        exception = lean_or(exceptional_cells)
        return "(¬ %s)" % exception if model["default"] else exception

    raise ValueError(kind)


# ------------------------- LABORATORY / LEDGER -------------------------

class Laboratory:
    def __init__(self, args, client, out):
        self.args = args
        self.client = client
        self.out = out
        self.ledger = []
        self.exports = []
        self.targets = []
        self.events = []

    def entry(self, prefix, hypothesis, provenance, cost):
        e = {
            "label": "CONJECTURED",
            "id": "%s-H%05d" % (prefix, len(self.ledger) + 1),
            "hypothesis": hypothesis,
            "provenance": provenance,
            "training_symbol_cost": cost,
            "evidence": {},
            "revised_hypothesis": None,
        }
        self.ledger.append(e)
        return e

    def add_evidence(self, entry, phase, points, predictor, baseline):
        entry["evidence"][phase] = summarize(points, predictor, baseline)
        refresh_entry(entry)

    def export(self, entry, family, domain, statement, conclusion,
               lean_target=None, dependencies=None):
        spec = {
            "label": "CONJECTURED",
            "THEOREM-ID": entry["id"],
            "STATEMENT": statement,
            "DOMAIN": domain,
            "HYPOTHESES": domain,
            "CONCLUSION": conclusion,
            "DEPENDENCIES": dependencies or [],
            "EXPERIMENTAL EVIDENCE": entry["evidence"],
            "COUNTEREXAMPLES TESTED": {
                "tests": entry["number_of_tests"],
                "smallest_found": entry["smallest_counterexample"],
                "status": entry["status"],
            },
            "PROOF STRATEGY": {
                "label": "UNCHECKED SPECIFICATION",
                "plan": [
                    "Expand the exact oracle definition.",
                    "Explain the learned representation independently of fitting.",
                    "Try surviving transport candidates as intermediate lemmas.",
                    "Prove both directions, or return a counterexample.",
                    "Do not treat finite agreement as an induction principle.",
                ],
            },
            "UNVERIFIED LEAN TARGET": {
                "label": "UNCHECKED SPECIFICATION",
                "type": lean_target,
                "ast_if_no_type": conclusion if lean_target is None else None,
                "note": "No proof term has been constructed or checked.",
            },
        }
        self.exports.append(spec)
        if lean_target is not None:
            self.targets.append((entry["id"], family, lean_target))

    def table_experiment(self, family, parent=None):
        a = self.args
        M0, M1, M2 = a.m_train, a.m_valid, a.m_test
        K0, K1, K2 = a.k_train, a.k_valid, a.k_test
        state = {"rf": {}, "cycles": {}}

        def calibrate(lo, hi, phase):
            points = []
            for m in range(lo, hi + 1):
                records = [
                    self.client.get(family, (m, k), phase)
                    for k in range(1, K0 + 1)
                ]
                q = fit_sequence([r["truth"] for r in records])
                state["cycles"][m] = q
                state["rf"][m] = row_features(m, records, q)
                points.extend(((m, k), records[k - 1])
                              for k in range(1, K0 + 1))
            return points

        train = calibrate(1, M0, family + ":train")
        baseline = {observable_structure(c, r) for c, r in train}
        train_rows = list(range(1, M0 + 1))
        lookup = {c: r for c, r in train}

        row_sigs = {
            m: tuple(lookup[(m, k)]["truth"] for k in range(1, K0 + 1))
            for m in train_rows
        }
        col_sigs = {
            k: tuple(lookup[(m, k)]["truth"] for m in train_rows)
            for k in range(1, K0 + 1)
        }
        ri = invariant_search(train_rows, state["rf"], row_sigs)
        ci = invariant_search(
            list(range(1, K0 + 1)),
            {k: arithmetic_features(k) for k in range(1, K0 + 1)},
            col_sigs,
        )
        save(self.out / (family + "_invariants.json"),
             {"label": "COMPUTED", "rows": ri, "columns": ci})

        entries = []
        seen = set()

        def register(model, origin, val=None):
            key = canonical(model)
            if key in seen:
                return None
            seen.add(key)
            cost = model_cost(model, state, train_rows)
            e = self.entry(family, model, {
                "generator": origin,
                "parent_theorem": parent,
                "calibration_columns": [1, K0],
                "prediction_mode": (
                    "row-calibrated" if requires_probes(model)
                    else "input-features-only"
                ),
            }, cost)
            self.add_evidence(
                e, "train", train,
                lambda c: predict(model, c[0], c[1], state), baseline
            )
            if val is not None:
                self.add_evidence(
                    e, "validation_refinement", val,
                    lambda c: predict(model, c[0], c[1], state), baseline
                )
            entries.append(e)
            return e

        for value in (False, True):
            register({"kind": "constant", "value": value}, "constant baseline")

        atom_entries = []
        for r in sorted(state["rf"][1]):
            for c in sorted(arithmetic_features(1)):
                for op in ("eq", "le", "divides", "coprime"):
                    e = register(
                        {"kind": "atom", "op": op, "r": r, "c": c},
                        "symmetric arithmetic relation grammar"
                    )
                    atom_entries.append(e)

        def train_rank(e):
            return (
                e["evidence"]["train"]["errors"],
                e["training_symbol_cost"], e["id"]
            )

        best_atoms = sorted(atom_entries, key=train_rank)[:12]
        for left, right in itertools.combinations(best_atoms, 2):
            for op in ("and", "or", "xor"):
                register({
                    "kind": "combine", "op": op,
                    "args": [left["hypothesis"], right["hypothesis"]]
                }, "training-selected depth-two Boolean grammar")

        register({"kind": "cycles"}, "learned prefix/block row representation")

        def preferred_names(result):
            singles = [x for x in result["candidates"]
                       if len(x["features"]) == 1]
            return list(dict.fromkeys(
                ["n"] + [x["features"][0] for x in singles[:6]]
            ))

        for rname in preferred_names(ri):
            for cname in preferred_names(ci):
                cells = collections.defaultdict(list)
                for (m, k), raw in train:
                    key = "%d,%d" % (
                        state["rf"][m][rname],
                        arithmetic_features(k)[cname],
                    )
                    cells[key].append(raw["truth"])
                register({
                    "kind": "table", "r": rname, "c": cname,
                    "cells": {k: majority(v) for k, v in cells.items()},
                    "default": majority(raw["truth"] for _, raw in train),
                }, "feature-pair quotient table")

        initial = min(entries, key=train_rank)

        calibration = calibrate(
            M0 + 1, M1, family + ":validation-row-calibration"
        )
        validation = [
            ((m, k), self.client.get(family, (m, k), family + ":validation"))
            for m in range(1, M1 + 1)
            for k in range(K0 + 1, K1 + 1)
        ]

        for e in entries:
            h = e["hypothesis"]
            self.add_evidence(
                e, "validation_refinement", validation,
                lambda c, h=h: predict(h, c[0], c[1], state), baseline
            )

        def validation_rank(e):
            return (
                e["evidence"]["validation_refinement"]["errors"],
                e["evidence"]["train"]["errors"],
                e["training_symbol_cost"], e["id"]
            )

        # Explicit counterexample-driven enlargement of the grammar.
        if initial["evidence"]["validation_refinement"]["errors"]:
            refinement_atoms = sorted(
                atom_entries, key=validation_rank
            )[:12]
            for e in refinement_atoms:
                for op in ("and", "or", "xor"):
                    register({
                        "kind": "combine", "op": op,
                        "args": [initial["hypothesis"], e["hypothesis"]],
                    }, {
                        "method": "counterexample-triggered Boolean refinement",
                        "parent": initial["id"],
                        "exposed_by":
                            initial["evidence"]["validation_refinement"][
                                "smallest_counterexample"
                            ],
                    }, validation)

        selected = min(entries, key=validation_rank)
        if selected["id"] != initial["id"]:
            initial["revised_hypothesis"] = selected["id"]
            selected["provenance"]["selected_after"] = initial["id"]

        self.events.append({
            "label": "COMPUTED",
            "kind": "conjecture_evolution",
            "family": family,
            "H1": initial["id"],
            "counterexample":
                initial["evidence"]["validation_refinement"][
                    "smallest_counterexample"
                ],
            "what_it_exposes": (
                "An observable prediction failure, not an inferred cause."
            ),
            "H2": selected["id"],
            "revision_succeeded_on_refinement_set":
                selected["evidence"]["validation_refinement"]["errors"] == 0,
        })

        calibration += calibrate(
            M1 + 1, M2, family + ":final-row-calibration"
        )
        shortlist = sorted(entries, key=validation_rank)[:5]

        final_coords = [
            (m, k)
            for m in range(1, M2 + 1)
            for k in range((K1 + 1) if m <= M1 else (K0 + 1), K2 + 1)
        ]
        for coord in final_coords:
            assert self.client.key(family, coord) not in self.client.cache

        forecasts = {
            e["id"]: [
                [list(c), predict(e["hypothesis"], c[0], c[1], state)]
                for c in final_coords
            ] for e in shortlist
        }
        save(self.out / (family + "_forecasts.json"), {
            "label": "CONJECTURED", "forecasts": forecasts
        })

        frozen = {
            "label": "COMPUTED",
            "selected_id": selected["id"],
            "shortlist": [e["id"] for e in shortlist],
            "candidate_ids": [e["id"] for e in entries],
            "candidate_hash": digest([e["hypothesis"] for e in entries]),
            "forecast_hash": digest(forecasts),
            "oracle_queries_before_final": self.client.calls,
            "environment": state,
            "hypotheses": {
                e["id"]: e["hypothesis"] for e in shortlist
            },
            "selection_rule": "validation errors, training errors, symbol cost",
        }
        save(self.out / (family + "_freeze.json"), frozen)

        final = [
            (c, self.client.get(family, c, family + ":final"))
            for c in final_coords
        ]

        # All already-generated hypotheses are falsified, but none is revised.
        for e in entries:
            h = e["hypothesis"]
            p = lambda c, h=h: predict(h, c[0], c[1], state)
            self.add_evidence(e, "calibration_check", calibration, p, baseline)
            self.add_evidence(e, "final", final, p, baseline)

        for e in shortlist:
            replay = [[list(c), predict(e["hypothesis"], c[0], c[1], state)]
                      for c in final_coords]
            assert replay == forecasts[e["id"]]

            description = {
                "hypothesis": e["hypothesis"],
                "environment": state if requires_probes(e["hypothesis"])
                else None,
            }
            e["representation_metrics"] = {
                "label": "COMPUTED",
                "training_symbol_cost": e["training_symbol_cost"],
                "symbol_cost_is_not_a_bit_count": True,
                "serialized_zlib_bits": 8 * len(zlib.compress(
                    canonical(description).encode("utf-8")
                )),
                "uncompressed_training_truth_bits": len(train),
                "final_accuracy": (
                    1 - e["evidence"]["final"]["errors"] / len(final)
                ),
                "calibration_instances": len(calibration),
            }

            if e["status"] == "UNREFUTED_ON_TESTED_DATA":
                rhs = lean_model(e["hypothesis"], state)
                target = (
                    "∀ m k : Nat, 1 ≤ m → m ≤ %d → 1 ≤ k → "
                    "(Q m k ↔ %s)" % (M2, rhs)
                )
                self.export(
                    e, family,
                    {"m": [1, M2], "k": "all positive integers"},
                    "On the explicitly listed modulus range, the oracle "
                    "predicate equals the frozen learned decoder for every "
                    "positive column coordinate.",
                    {"model": e["hypothesis"], "environment": state},
                    target,
                    ["oracle definition", family + "_freeze.json"],
                )

        all_points = train + calibration + validation + final
        save(self.out / (family + "_exceptions.json"),
             exception_search(all_points))
        return {
            "selected": selected,
            "state": state,
            "invariants": {"rows": ri, "columns": ci},
            "points": all_points,
        }


# ------------------------- TRANSPORT SEARCH -------------------------

def transport_experiment(lab):
    a = lab.args
    C = lab.client
    records = {}

    def get(m, k):
        return C.get("T", (m, k), "transport")

    def update(name, schema, phase, eligible, ok, coord, detail, signature):
        if name not in records:
            records[name] = {
                "schema": schema, "evidence": {},
                "training_structures": set()
            }
        rec = records[name]
        if phase == "train":
            rec["training_structures"].add(signature)
        st = rec["evidence"].setdefault(phase, {
            "label": "COMPUTED",
            "cases": 0, "tests": 0, "supporting": 0, "errors": 0,
            "abstentions": 0, "smallest_counterexample": None,
        })
        st["cases"] += 1
        if not eligible:
            return
        st["tests"] += 1
        st["supporting"] += int(ok)
        st["errors"] += int(not ok)
        if not ok:
            ce = {
                "label": "COMPUTED",
                "coord": list(coord),
                "detail": detail,
                "observable_structure": signature,
            }
            old = st["smallest_counterexample"]
            if old is None or tuple(coord) < tuple(old["coord"]):
                st["smallest_counterexample"] = ce

    def unary(name, schema, source, target, coord):
        s = get(*source)
        t = get(*target)
        phase = (
            "train" if max(source[0], target[0]) <= a.m_train
            and max(source[1], target[1]) <= a.k_train else "final"
        )
        sig = canonical([
            math.gcd(source[0], target[0]) > 1,
            s["truth"], t["truth"],
            s["witness"] is None, t["witness"] is None,
        ])
        detail = {
            "source": list(source), "target": list(target),
            "source_query": s["_query_id"], "target_query": t["_query_id"],
        }
        for rel, eligible, ok in (
            ("implication", s["truth"], t["truth"]),
            ("reverse_implication", t["truth"], s["truth"]),
            ("equivalence", True, s["truth"] == t["truth"]),
        ):
            update(name + "/" + rel,
                   dict(schema, claim=rel), phase,
                   eligible, ok, coord, detail, sig)

        # These are distinct candidate statements.
        for x, value in enumerate(s["profile"]):
            if value is False:
                y = x % target[0]
                update(
                    name + "/all_witness_projection",
                    dict(schema, claim="every failing x maps to failing x % target_m"),
                    phase, True, t["profile"][y] is False,
                    tuple(coord) + (x,), dict(detail, x=x, mapped=y), sig,
                )

        w = s["witness"]
        eligible = w is not None
        y = w % target[0] if eligible else None
        tests = (
            ("least_witness_maps_to_a_witness",
             eligible and t["profile"][y] is False),
            ("mapped_least_witness_is_least",
             eligible and t["witness"] == y),
            ("literal_least_witness_preserved",
             eligible and t["witness"] == w),
        )
        for rel, ok in tests:
            update(name + "/" + rel, dict(schema, claim=rel), phase,
                   eligible, bool(ok), coord,
                   dict(detail, source_witness=w, mapped=y,
                        target_witness=t["witness"]), sig)

    # Transformation vocabulary; no assertion of preservation.
    for m in range(1, a.m_test + 1):
        for d in range(1, m + 1):
            if m % d == 0:
                for k in range(1, a.k_test + 1):
                    schema = {
                        "kind": "unary", "domain": "m,d,k >= 1; d divides m",
                        "source": ["m", "k"], "target": ["d", "k"]
                    }
                    unary("divisor_down", schema, (m, k), (d, k), (m, d, k))
                    unary(
                        "divisor_up",
                        dict(schema, source=["d", "k"], target=["m", "k"]),
                        (d, k), (m, k), (m, d, k)
                    )
        for k in range(1, a.k_test + 1):
            for s in range(1, 4):
                if k + s <= a.k_test:
                    unary(
                        "column_add_%d" % s,
                        {"kind": "unary", "domain": "m,k >= 1",
                         "source": ["m", "k"], "target": ["m", ["add", "k", s]]},
                        (m, k), (m, k + s), (m, k, s)
                    )
            for q in (2, 3):
                if q * k <= a.k_test:
                    unary(
                        "column_multiply_%d" % q,
                        {"kind": "unary", "domain": "m,k >= 1",
                         "source": ["m", "k"], "target": ["m", ["mul", q, "k"]]},
                        (m, k), (m, q * k), (m, k, q)
                    )

    operations = {
        "mul": lambda x, y: x * y,
        "lcm": math.lcm,
        "gcd": math.gcd,
        "add": lambda x, y: x + y,
    }
    for opname, operation in operations.items():
        for x in range(1, a.m_test + 1):
            for y in range(x, a.m_test + 1):
                z = operation(x, y)
                if not (1 <= z <= a.m_test):
                    continue
                restrictions = ["any", "coprime" if math.gcd(x, y) == 1
                                else "noncoprime"]
                for k in range(1, a.k_test + 1):
                    rx, ry, rz = get(x, k), get(y, k), get(z, k)
                    phase = (
                        "train" if max(x, y, z) <= a.m_train
                        and k <= a.k_train else "final"
                    )
                    sig = canonical([
                        math.gcd(x, y) == 1,
                        rx["truth"], ry["truth"], rz["truth"],
                    ])
                    detail = {
                        "a": x, "b": y, "output_modulus": z, "k": k,
                        "truths": [rx["truth"], ry["truth"], rz["truth"]],
                    }
                    for restriction in restrictions:
                        for connective in ("and", "or", "xor"):
                            p = boolop(connective, rx["truth"], ry["truth"])
                            q = rz["truth"]
                            for rel, eligible, ok in (
                                ("implication", p, q),
                                ("reverse_implication", q, p),
                                ("equivalence", True, p == q),
                            ):
                                name = "/".join(
                                    [opname, restriction, connective, rel]
                                )
                                schema = {
                                    "kind": "binary_modulus",
                                    "domain": "a,b,k >= 1",
                                    "operation": opname,
                                    "restriction": restriction,
                                    "source_connective": connective,
                                    "claim": rel,
                                }
                                update(name, schema, phase, eligible, ok,
                                       (x, y, k), detail, sig)

    entries = []
    by_name = {}
    for name, rec in sorted(records.items()):
        e = lab.entry("TR", rec["schema"], {
            "generator": "preregistered transport template",
            "template_name": name,
            "holdout_note": (
                "Transport templates are fixed in advance. Their final "
                "coordinates overlap the table experiment; this is not "
                "an independent replicate of that experiment."
            ),
        }, 1)
        e["evidence"] = rec["evidence"]
        for st in e["evidence"].values():
            ce = st["smallest_counterexample"]
            if ce is not None:
                ce["structurally_novel"] = (
                    ce["observable_structure"]
                    not in rec["training_structures"]
                )
                ce["novelty_reference"] = "transport training signatures"
        refresh_entry(e)
        entries.append(e)
        by_name[name] = e

    # Restriction proposals are selected using training counterexamples only.
    for name, e in by_name.items():
        if "/any/" not in name:
            continue
        train = e["evidence"].get("train", {})
        if not train.get("errors", 0):
            continue
        for restriction in ("coprime", "noncoprime"):
            refined_name = name.replace("/any/", "/" + restriction + "/")
            child = by_name.get(refined_name)
            if child:
                st = child["evidence"].get("train", {})
                if st.get("tests", 0) >= 5 and st.get("errors", 1) == 0:
                    e["revised_hypothesis"] = child["id"]
                    child["provenance"]["parent"] = e["id"]
                    break

    # Shortlist uses training evidence only, never final survival.
    eligible = [
        e for e in entries
        if e["evidence"].get("train", {}).get("tests", 0) >= 5
        and e["evidence"]["train"]["errors"] == 0
    ]
    shortlist = sorted(
        eligible,
        key=lambda e: (-e["evidence"]["train"]["tests"], e["id"])
    )[:12]
    for e in shortlist:
        final = e["evidence"].get("final", {})
        if (e["status"] == "UNREFUTED_ON_TESTED_DATA"
                and final.get("tests", 0) >= 5):
            lab.export(
                e, "T", e["hypothesis"].get("domain"),
                "Universal transport claim described by the exact AST.",
                e["hypothesis"], None,
                ["T definition", "transport AST semantics in lab.py"]
            )

    save(lab.out / "transport.json", {
        "label": "COMPUTED",
        "entries": entries,
        "training_selected_shortlist": [e["id"] for e in shortlist],
        "warning": "Implications with no eligible premises are not discoveries.",
    })
    return entries


# ------------------- SECOND-ORDER REPRESENTATION SEARCH -------------------

def fit_boolean_factor(matrix, op):
    """
    Exhaustive search over the first Boolean factor.
    The second factor is solved column by column.
    No particular connective is assumed to work.
    """
    nr, nd = len(matrix), len(matrix[0])
    candidates = []
    feasible_assignments = 0
    for av in itertools.product((False, True), repeat=nr):
        bv = []
        ambiguous = 0
        possible = True
        for j in range(nd):
            choices = [
                b for b in (False, True)
                if all(boolop(op, av[i], b) == matrix[i][j]
                       for i in range(nr))
            ]
            if not choices:
                possible = False
                break
            ambiguous += int(len(choices) > 1)
            # Deterministic ambiguity convention, explicitly reported.
            bv.append(choices[0])
        if possible:
            feasible_assignments += 1
            qa, qb = fit_sequence(av), fit_sequence(bv)
            candidates.append({
                "a": qa, "b": qb,
                "ambiguous_second_factor_columns": ambiguous,
            })
    if not candidates:
        return None
    best = min(candidates, key=lambda q: (
        sequence_cost(q["a"]) + sequence_cost(q["b"]),
        q["ambiguous_second_factor_columns"], canonical(q)
    ))
    best["feasible_first_factor_assignments"] = feasible_assignments
    return best


def fit_tile(matrix):
    nr, nd = len(matrix), len(matrix[0])
    candidates = []
    for pr in range(1, nr + 1):
        for pd in range(1, nd + 1):
            if all(matrix[i][j] == matrix[i % pr][j % pd]
                   for i in range(nr) for j in range(nd)):
                candidates.append({
                    "pr": pr, "pd": pd,
                    "tile": [row[:pd] for row in matrix[:pr]],
                    "two_copies_on_both_axes": nr >= 2 * pr and nd >= 2 * pd,
                })
    return min(candidates, key=lambda q: (
        q["pr"] * q["pd"], q["pr"], q["pd"]
    ))


def tensor_predict(model, coord):
    m, r, d = coord
    row = model["rows"][m]
    if model["kind"] == "factor":
        if row is None:
            return None
        return boolop(
            model["op"], sequence_predict(row["a"], r),
            sequence_predict(row["b"], d)
        )
    return row["tile"][(r - 1) % row["pr"]][(d - 1) % row["pd"]]


def tensor_cost(model):
    if model["kind"] == "factor":
        return 1 + sum(
            100000 if row is None
            else sequence_cost(row["a"]) + sequence_cost(row["b"])
            for row in model["rows"].values()
        )
    return 1 + sum(row["pr"] * row["pd"] + 2
                   for row in model["rows"].values())


def rectangle_diagnostic(matrix):
    nr, nd = len(matrix), len(matrix[0])
    rs = [i for i in range(nr) if any(matrix[i])]
    ds = [j for j in range(nd) if any(matrix[i][j] for i in range(nr))]
    missing = next(
        ((i, j) for i in rs for j in ds if not matrix[i][j]), None
    )
    certificate = None
    if missing is not None:
        i, j = missing
        j1 = next(t for t in range(nd) if matrix[i][t])
        i1 = next(t for t in range(nr) if matrix[t][j])
        certificate = {
            "positive_cells": [[i + 1, j1 + 1], [i1 + 1, j + 1]],
            "missing_cross_cell": [i + 1, j + 1],
        }
    return {
        "label": "COMPUTED",
        "finite_true_set_is_cartesian": missing is None,
        "positive_row_support": [i + 1 for i in rs],
        "positive_column_support": [j + 1 for j in ds],
        "nondegenerate": 0 < len(rs) < nr and 0 < len(ds) < nd,
        "empty_support_is_unidentifiable": len(rs) == 0,
        "counterexample_certificate": certificate,
    }


def lean_tensor(model):
    terms = []
    for m, row in sorted(model["rows"].items()):
        if row is None:
            continue
        if model["kind"] == "factor":
            body = lean_bool(
                model["op"], lean_sequence(row["a"], "r"),
                lean_sequence(row["b"], "d")
            )
        else:
            body = lean_or([
                "((r - 1) %% %d = %d ∧ (d - 1) %% %d = %d)" %
                (row["pr"], i, row["pd"], j)
                for i in range(row["pr"]) for j in range(row["pd"])
                if row["tile"][i][j]
            ])
        terms.append("(m = %d ∧ %s)" % (m, body))
    return lean_or(terms)


def tensor_experiment(lab, parent):
    a = lab.args
    M = a.m_test
    R0, R1, R2 = a.r_train, a.r_valid, a.r_test
    D0, D1, D2 = a.d_train, a.d_valid, a.d_test
    C = lab.client

    train = [
        ((m, r, d), C.get("E", (m, r, d), "E:calibration"))
        for m in range(1, M + 1)
        for r in range(1, R0 + 1)
        for d in range(1, D0 + 1)
    ]
    lookup = {c: raw for c, raw in train}
    matrices = {
        m: [[lookup[(m, r, d)]["truth"] for d in range(1, D0 + 1)]
            for r in range(1, R0 + 1)]
        for m in range(1, M + 1)
    }
    baseline = {observable_structure(c, raw) for c, raw in train}
    models = [
        {
            "kind": "factor", "op": op,
            "rows": {m: fit_boolean_factor(matrix, op)
                     for m, matrix in matrices.items()},
        } for op in ("and", "or", "xor", "iff")
    ]
    models.append({
        "kind": "tile",
        "rows": {m: fit_tile(matrix) for m, matrix in matrices.items()},
    })

    entries = []
    for model in models:
        e = lab.entry("E", model, {
            "parent": parent,
            "generator": "competing Boolean separations and 2D periodic tiles",
            "generalization_scope": "axis extrapolation on calibrated moduli",
        }, tensor_cost(model))
        lab.add_evidence(
            e, "calibration", train,
            lambda c, model=model: tensor_predict(model, c), baseline
        )
        entries.append(e)

    validation_coords = [
        (m, r, d)
        for m in range(1, M + 1)
        for r in range(1, R1 + 1)
        for d in range(1, D1 + 1)
        if r > R0 or d > D0
    ]
    validation = [
        (c, C.get("E", c, "E:validation")) for c in validation_coords
    ]
    for e in entries:
        model = e["hypothesis"]
        lab.add_evidence(
            e, "validation_refinement", validation,
            lambda c, model=model: tensor_predict(model, c), baseline
        )

    def rank(e):
        return (
            e["evidence"]["validation_refinement"]["errors"],
            e["evidence"]["calibration"]["errors"],
            e["training_symbol_cost"], e["id"]
        )

    selected = min(entries, key=rank)
    shortlist = sorted(entries, key=rank)[:3]
    final_coords = [
        (m, r, d)
        for m in range(1, M + 1)
        for r in range(1, R2 + 1)
        for d in range(1, D2 + 1)
        if r > R1 or d > D1
    ]
    for c in final_coords:
        assert C.key("E", c) not in C.cache

    forecasts = {
        e["id"]: [[list(c), tensor_predict(e["hypothesis"], c)]
                  for c in final_coords]
        for e in entries
    }
    save(lab.out / "E_forecasts.json", {
        "label": "CONJECTURED", "forecasts": forecasts
    })
    save(lab.out / "E_freeze.json", {
        "label": "COMPUTED",
        "selected_id": selected["id"],
        "shortlist": [e["id"] for e in shortlist],
        "models": models,
        "forecast_hash": digest(forecasts),
        "oracle_queries_before_final": C.calls,
    })

    final = [(c, C.get("E", c, "E:final")) for c in final_coords]
    for e in entries:
        model = e["hypothesis"]
        lab.add_evidence(
            e, "final", final,
            lambda c, model=model: tensor_predict(model, c), baseline
        )
        assert forecasts[e["id"]] == [
            [list(c), tensor_predict(model, c)] for c in final_coords
        ]

    full = {c: raw for c, raw in train + validation + final}
    diagnostics = {}
    for m in range(1, M + 1):
        matrix = [
            [full[(m, r, d)]["truth"] for d in range(1, D2 + 1)]
            for r in range(1, R2 + 1)
        ]
        diagnostics[m] = rectangle_diagnostic(matrix)

    for e in shortlist:
        if e["status"] != "UNREFUTED_ON_TESTED_DATA":
            continue
        target = (
            "∀ m r d : Nat, 1 ≤ m → m ≤ %d → 1 ≤ r → 1 ≤ d → "
            "(Q m r d ↔ %s)" % (M, lean_tensor(e["hypothesis"]))
        )
        lab.export(
            e, "E",
            {"m": [1, M], "r": "all positive integers",
             "d": "all positive integers"},
            "The eventual-equality predicate equals the frozen tensor decoder.",
            e["hypothesis"], target,
            ["E definition", "E_freeze.json"]
        )

    save(lab.out / "second_order.json", {
        "label": "COMPUTED",
        "selected_before_final": selected["id"],
        "competing_hypotheses": entries,
        "post_test_rectangularity_diagnostics": diagnostics,
        "interpretation": (
            "Rectangularity is a finite extensional property. "
            "It neither identifies a unique causal mechanism nor proves "
            "infinite independence. Empty supports do not identify factors."
        ),
    })
    save(lab.out / "E_exceptions.json",
         exception_search(train + validation + final))
    return entries, diagnostics


# ------------------- DEFORMATION / ALGORITHM AUDIT -------------------

def algorithm_audit(lab, parent):
    total_full = 0
    total_early = 0
    tests = 0
    for m in range(1, min(8, lab.args.m_train) + 1):
        for k in range(1, min(8, lab.args.k_train) + 1):
            full = lab.client.get("T", (m, k), "algorithm-audit:full")
            early = lab.client.get(
                "T", (m, k), "algorithm-audit:early", "witness"
            )
            assert full["witness"] == early["witness"]
            total_full += full["evaluated"]
            total_early += early["evaluated"]
            tests += 1
    lab.events.append({
        "label": "COMPUTED",
        "kind": "algorithm_deformation",
        "parent": parent,
        "change": "full profile -> early-stopping least-witness computation",
        "tests": tests,
        "full_residue_evaluations": total_full,
        "early_residue_evaluations": total_early,
        "scope": "bounded operational equivalence only",
    })


# ------------------------- FORMALIZATION FILES -------------------------

def write_formalization(lab):
    save(lab.out / "theorem_candidates.json", {
        "label": "CONJECTURED",
        "oracle_world": lab.args.oracle,
        "external_oracle": lab.args.oracle_command,
        "candidates": lab.exports,
        "warning": "No candidate in this file has a supplied proof.",
    })

    lines = [
        "import Mathlib",
        "",
        "-- UNCHECKED SPECIFICATION.",
        "-- These are proposition definitions, not theorem proofs.",
        "-- No `sorry` is used and no verification is claimed.",
        "namespace BlindLab",
        "",
        "def RealT (m k : Nat) : Prop :=",
        "  ∀ x : Nat, x < m → x ^ k % m = x",
        "",
        "def RealE (m r d : Nat) : Prop :=",
        "  ∀ x : Nat, x < m → x ^ (r + d) % m = x ^ r % m",
        "",
        "def RealU (m k : Nat) : Prop :=",
        "  ∀ x : Nat, x < m → Nat.gcd x m = 1 → x ^ k % m = x",
        "",
    ]
    for i, (theorem_id, family, target) in enumerate(lab.targets):
        arity = 3 if family == "E" else 2
        typ = " → ".join(["Nat"] * arity + ["Prop"])
        lines += [
            "-- " + theorem_id,
            "def target_%d (Q : %s) : Prop :=" % (i, typ),
            "  " + target,
            "",
        ]
        if lab.args.oracle == "real" and not lab.args.oracle_command:
            lines += [
                "def real_target_%d : Prop := target_%d Real%s" %
                (i, i, family),
                "",
            ]
    lines += ["end BlindLab", ""]
    (lab.out / "targets.lean").write_text("\n".join(lines), encoding="utf-8")


# ------------------------- SYNTHETIC ASSERTIONS -------------------------
# These assertions belong to the test harness, not discovery.
# They are disabled for real-oracle experiments.

def synthetic_assertions(table_result, tensor_entries):
    def find_invariant(axis, feature):
        return next(
            x for x in table_result["invariants"][axis]["candidates"]
            if x["features"] == [feature]
        )

    r = find_invariant("rows", "mod:6")
    c = find_invariant("columns", "mod:3")
    assert r["contradictory_pairs"] == 0 and r["comparable_pairs"] > 0
    assert c["contradictory_pairs"] == 0 and c["comparable_pairs"] > 0

    cycles = table_result["state"]["cycles"]
    assert all(
        sequence_predict(cycles[coord[0]], coord[1]) == raw["truth"]
        for coord, raw in table_result["points"]
    )

    factor = next(
        e for e in tensor_entries
        if e["hypothesis"]["kind"] == "factor"
        and e["hypothesis"]["op"] == "and"
    )
    assert factor["status"] == "UNREFUTED_ON_TESTED_DATA"
    return {
        "label": "COMPUTED",
        "result": "synthetic assertions passed",
        "note": "This message is produced only after executing the assertions.",
    }


# ------------------------- REPRODUCIBLE DRIVER -------------------------

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--worker", action="store_true")
    p.add_argument("--oracle", choices=("real", "synthetic"), default="real")
    p.add_argument("--oracle-command", default=None)
    p.add_argument("--control", choices=("B", "C"), default="C")
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--out", default="blind-lab-run")
    p.add_argument("--budget", type=int, default=40000)
    p.add_argument("--seed", type=int, default=20250308)

    p.add_argument("--m-train", type=int, default=24)
    p.add_argument("--m-valid", type=int, default=36)
    p.add_argument("--m-test", type=int, default=48)
    p.add_argument("--k-train", type=int, default=24)
    p.add_argument("--k-valid", type=int, default=40)
    p.add_argument("--k-test", type=int, default=64)

    p.add_argument("--r-train", type=int, default=4)
    p.add_argument("--r-valid", type=int, default=6)
    p.add_argument("--r-test", type=int, default=8)
    p.add_argument("--d-train", type=int, default=12)
    p.add_argument("--d-valid", type=int, default=18)
    p.add_argument("--d-test", type=int, default=24)
    return p.parse_args()


def main():
    args = parse_args()
    if args.worker:
        worker_main(args.oracle)
        return

    if args.self_test:
        if args.oracle_command:
            raise ValueError("--self-test cannot use an external oracle")
        args.oracle = "synthetic"
        args.control = "C"
        if args.m_train < 12 or args.k_train < 12:
            raise ValueError("Synthetic assertions require training bounds >= 12")

    if not (1 <= args.m_train < args.m_valid < args.m_test):
        raise ValueError("Require 1 <= m_train < m_valid < m_test")
    if not (1 <= args.k_train < args.k_valid < args.k_test):
        raise ValueError("Require 1 <= k_train < k_valid < k_test")
    if not (1 <= args.r_train < args.r_valid < args.r_test):
        raise ValueError("Require increasing positive r bounds")
    if not (1 <= args.d_train < args.d_valid < args.d_test):
        raise ValueError("Require increasing positive d bounds")
    if args.r_train > 12:
        raise ValueError("Exhaustive Boolean-factor search caps r_train at 12")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=False)
    source_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()

    save(out / "manifest.json", {
        "label": "COMPUTED",
        "configuration": vars(args),
        "source_sha256": source_hash,
        "python": sys.version,
        "platform": platform.platform(),
        "randomness": (
            "Search is deterministic. Seed is recorded for protocol identity; "
            "this version does not consume random numbers."
        ),
        "provenance_policy": (
            "Labels apply recursively unless a nested object overrides them."
        ),
        "verification_status": "No formal verification is performed.",
    })
    save(out / "preregistration.json", {
        "label": "UNCHECKED SPECIFICATION",
        "features": list(arithmetic_features(1)),
        "empirical_features": [
            "true count", "first true", "first false", "failure count",
            "learned onset", "learned period", "cycle positive count"
        ],
        "atomic_relations": ["eq", "le", "divides", "coprime"],
        "Boolean_relations": ["and", "or", "xor"],
        "sequence_search": "exact prefix/block; at least two block copies",
        "transport": {
            "unary": ["both divisor directions", "column +1,+2,+3",
                      "column times 2,3"],
            "binary": ["product", "lcm", "gcd", "sum"],
            "restrictions": ["any", "coprime", "noncoprime"],
            "truth_claims": ["implication", "reverse implication", "equivalence"],
            "witness_claims": [
                "every witness projection", "least maps to a witness",
                "mapped least remains least", "literal least preserved"
            ],
        },
        "second_order": ["AND factors", "OR factors", "XOR factors",
                         "IFF factors", "2D periodic tiles"],
        "selection": "validation errors, training errors, symbolic cost",
        "refinement": "only before final forecasts",
        "formal_export": (
            "Only preregistered shortlists with no observed counterexamples "
            "or abstentions; infinite extension remains conjectural."
        ),
        "transport_final_overlap": (
            "Transport evaluation reuses the T table, with a fixed template "
            "language. It is not an independent replication."
        ),
    })

    client = Client(args, out)
    lab = Laboratory(args, client, out)
    try:
        table_result = lab.table_experiment("T")
        transport_experiment(lab)

        tensor_entries = []
        if args.control == "C":
            parent = (
                lab.exports[0]["THEOREM-ID"] if lab.exports
                else table_result["selected"]["id"]
            )
            parent_status = (
                "unrefuted exported candidate" if lab.exports
                else "provisional or refuted best predictor"
            )
            lab.events += [
                {
                    "label": "CONJECTURED",
                    "kind": "theorem_deformation",
                    "parent": parent,
                    "parent_status": parent_status,
                    "operator": "x^k = x -> x^(r+d) = x^r",
                    "new_family": "E",
                    "operator_origin": "preregistered library, not discovered",
                },
                {
                    "label": "CONJECTURED",
                    "kind": "theorem_deformation",
                    "parent": parent,
                    "operator": "all residues -> residues satisfying gcd(x,m)=1",
                    "new_family": "U",
                    "operator_origin": "preregistered library, not discovered",
                },
                {
                    "label": "COMPUTED",
                    "kind": "representation_deformation",
                    "parent": parent,
                    "change": (
                        "raw table -> arithmetic rules / quotient tables / "
                        "prefix-block codes -> Boolean tensor factors"
                    ),
                },
                {
                    "label": "UNCHECKED SPECIFICATION",
                    "kind": "proof_deformation",
                    "parent": parent,
                    "change": (
                        "replace direct finite enumeration by a proof using "
                        "surviving transport lemmas"
                    ),
                    "status": "proof planning only; no proof synthesis engine",
                },
            ]
            tensor_entries, _ = tensor_experiment(lab, parent)
            lab.table_experiment("U", parent)
            algorithm_audit(lab, parent)

        if args.self_test:
            save(out / "synthetic_test.json",
                 synthetic_assertions(table_result, tensor_entries))

        write_formalization(lab)
        save(out / "ledger.json", {
            "label": "CONJECTURED",
            "entries": lab.ledger,
        })
        save(out / "deformations.json", {
            "label": "COMPUTED",
            "events": lab.events,
        })
        summary = {
            "label": "COMPUTED",
            "oracle_world": args.oracle,
            "control": args.control,
            "unique_oracle_queries": client.calls,
            "queries_by_first_phase": dict(client.phases),
            "cache_hits_by_phase": dict(client.hits),
            "hypotheses_tested": len(lab.ledger),
            "refuted_hypotheses": sum(
                e["status"] == "REFUTED" for e in lab.ledger
            ),
            "exported_candidates": len(lab.exports),
            "formally_verified_theorems": 0,
            "selected_T_id": table_result["selected"]["id"],
            "selected_T_status": table_result["selected"]["status"],
        }
        save(out / "summary.json", summary)
        print(json.dumps(summary, indent=2, sort_keys=True))

    except Exception as exc:
        save(out / "failure.json", {
            "label": "COMPUTED",
            "exception": repr(exc),
            "unique_oracle_queries": client.calls,
            "note": "A failed or budget-exhausted run is not a successful experiment.",
        })
        save(out / "partial_ledger.json", {
            "label": "CONJECTURED", "entries": lab.ledger
        })
        raise
    finally:
        client.close()


if __name__ == "__main__":
    main()
