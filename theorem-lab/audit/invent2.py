#!/usr/bin/env python3
"""
Phase 8 / Ablation D (v2, corrected objective): can the system SELECT a worthwhile deformation itself?

The searcher is given a deformation language (pairs of exponent expressions over
two parameters, with an optional unit-domain restriction) and an objective that
is fixed in this file BEFORE any family is evaluated. It is never told that
x^(r+d) = x^r is the intended answer, and the objective contains no term that
mentions that family, its arity, or its shape.

Every family is scored identically. The ranking is reported in full, including
the families that beat or tie the E-like one.

Objective (pre-registered weights, declared here before execution):

    score = 0.30 * nontriviality           two-sided, per-row as well as global
          + 0.25 * extrapolation           accuracy of a frozen fit outside its window
          + 0.20 * compressibility         1 - description bits / raw bits
          + 0.15 * cross_modulus_invariance whether a simple feature of m predicts the row
          + 0.10 * exception_structure     whether failures cluster rather than scatter

`nontriviality` guards against constant families; `extrapolation` against finite
memorisation; `compressibility` against lookup tables; `cross_modulus_invariance`
rewards families whose behaviour is governed by something about m;
`exception_structure` rewards families with a structured boundary.
"""
import collections
import importlib.util
import itertools
import json
import math
import subprocess
import zlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("lab", HERE.parent / "lab.py")
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)

EXPRS = ["1", "a", "b", "a+1", "a+2", "2a", "a+b", "ab"]
WEIGHTS = {"nontriviality": 0.30, "extrapolation": 0.25,
           "compressibility": 0.20, "cross_modulus_invariance": 0.15,
           "exception_structure": 0.10}

M = 20                      # moduli 1..M
A0, A1 = 6, 8               # first parameter: calibration / final
B0, B1 = 24, 36             # second parameter: calibration / final


class Oracle:
    def __init__(self):
        self.proc = subprocess.Popen(
            [sys.executable, str(HERE / "deform_oracle.py")],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True,
            bufsize=1)
        self.calls = 0

    def ask(self, lhs, rhs, domain, m, a, b):
        req = {"lhs": lhs, "rhs": rhs, "domain": domain,
               "m": m, "a": a, "b": b}
        self.proc.stdin.write(json.dumps(req, separators=(",", ":")) + "\n")
        self.proc.stdin.flush()
        ans = json.loads(self.proc.stdout.readline())
        if "error" in ans:
            raise RuntimeError(ans["error"])
        self.calls += 1
        return ans

    def close(self):
        self.proc.stdin.close()
        self.proc.wait()


def uses(expr_pair):
    txt = " ".join(expr_pair)
    return ("a" in txt, "b" in txt)


def entropy(counts):
    n = sum(counts)
    if n <= 1:
        return 0.0
    h = -sum((c / n) * math.log(c / n) for c in counts if c)
    return h / math.log(len(counts)) if len(counts) > 1 else 0.0


def score_family(oracle, lhs, rhs, domain):
    """Evaluate one candidate deformation family."""
    grid = {}
    for m in range(1, M + 1):
        for a in range(1, A1 + 1):
            for b in range(1, B1 + 1):
                if a > A0 and b > B0:
                    pass  # still needed for the final region
                grid[(m, a, b)] = oracle.ask(lhs, rhs, domain, m, a, b)

    truths = {c: r["truth"] for c, r in grid.items()}
    calib = [(m, a, b) for m in range(1, M + 1)
             for a in range(1, A0 + 1) for b in range(1, B0 + 1)]
    final = [(m, a, b) for m in range(1, M + 1)
             for a in range(1, A1 + 1) for b in range(1, B1 + 1)
             if a > A0 or b > B0]

    # --- nontriviality -----------------------------------------------------
    vals = [truths[c] for c in calib]
    p = sum(vals) / len(vals)
    global_nt = 2 * min(p, 1 - p)
    varying_rows = sum(
        1 for m in range(1, M + 1)
        if len({truths[(m, a, b)] for a in range(1, A0 + 1)
                for b in range(1, B0 + 1)}) > 1)
    nontriviality = global_nt * (varying_rows / M)

    # --- fit the laboratory's own representations on the calibration box ----
    matrices = {m: [[truths[(m, a, b)] for b in range(1, B0 + 1)]
                    for a in range(1, A0 + 1)] for m in range(1, M + 1)}
    best_models = {}
    total_cost = 0
    for m, matrix in matrices.items():
        options = []
        for op in ("and", "or", "xor", "iff"):
            row = lab.fit_boolean_factor(matrix, op)
            if row is not None:
                options.append((
                    lab.sequence_cost(row["a"]) + lab.sequence_cost(row["b"]),
                    ("factor", op, row)))
        tile = lab.fit_tile(matrix)
        options.append((tile["pr"] * tile["pd"] + 2, ("tile", None, tile)))
        cost, model = min(options, key=lambda x: (x[0], str(x[1][0])))
        best_models[m] = model
        total_cost += cost

    def predict(m, a, b):
        kind, op, row = best_models[m]
        if kind == "factor":
            return lab.boolop(op, lab.sequence_predict(row["a"], a),
                              lab.sequence_predict(row["b"], b))
        return row["tile"][(a - 1) % row["pr"]][(b - 1) % row["pd"]]

    calib_err = sum(predict(*c) != truths[c] for c in calib)
    final_err = sum(predict(*c) != truths[c] for c in final)
    extrapolation = 1 - final_err / len(final)

    raw_bits = len(calib)
    desc_bits = 8 * len(zlib.compress(lab.canonical(
        {str(m): best_models[m][2] for m in best_models}).encode(), 9))
    compressibility = max(0.0, 1 - desc_bits / raw_bits)

    # --- cross-modulus invariance -----------------------------------------
    sigs = {m: tuple(truths[(m, a, b)] for a in range(1, A0 + 1)
                     for b in range(1, B0 + 1)) for m in range(1, M + 1)}
    feats = {m: lab.arithmetic_features(m) for m in range(1, M + 1)}
    inv = lab.invariant_search(list(range(1, M + 1)), feats, sigs)
    singles = [c for c in inv["candidates"] if len(c["features"]) == 1
               and not c["vacuous"]
               and c["comparable_pairs"] >= M // 2]
    best_collision = min(
        (c["contradictory_pairs"] / max(1, c["comparable_pairs"])
         for c in singles), default=1.0)
    cross_modulus_invariance = 1 - best_collision

    # --- exception structure ----------------------------------------------
    witness_classes = collections.Counter(
        grid[c]["witness"] for c in calib if not truths[c])
    exception_structure = (
        1 - entropy(list(witness_classes.values())) if witness_classes else 0.0)

    parts = {
        "nontriviality": nontriviality,
        "extrapolation": extrapolation,
        "compressibility": compressibility,
        "cross_modulus_invariance": cross_modulus_invariance,
        "exception_structure": exception_structure,
    }
    return {
        "family": "x^(%s) = x^(%s) on %s" % (lhs, rhs, domain),
        "lhs": lhs, "rhs": rhs, "domain": domain,
        "components": parts,
        "score": sum(WEIGHTS[k] * v for k, v in parts.items()),
        "calibration_errors": calib_err,
        "final_errors": final_err,
        "true_rate": p,
        "description_bits": desc_bits,
        "representation_choice": collections.Counter(
            best_models[m][0] for m in best_models),
    }


def main():
    oracle = Oracle()
    results = []
    seen = set()
    for lhs, rhs in itertools.combinations(EXPRS, 2):
        for domain in ("all", "units"):
            key = (frozenset((lhs, rhs)), domain)
            if key in seen:
                continue
            seen.add(key)
            try:
                results.append(score_family(oracle, lhs, rhs, domain))
            except Exception as exc:      # a family may be degenerate
                results.append({"family": "%s=%s/%s" % (lhs, rhs, domain),
                                "error": repr(exc), "score": -1.0})
    oracle.close()
    results.sort(key=lambda r: -r["score"])
    out = {
        "label": "COMPUTED",
        "pre_registered_weights": WEIGHTS,
        "grid": {"M": M, "A": [A0, A1], "B": [B0, B1]},
        "oracle_queries": oracle.calls,
        "ranking": results,
        "note": ("Scoring is identical for every family and mentions no "
                 "particular deformation. T is (a,1,all); U is (a,1,units); "
                 "the human-designed E deformation is (a+b,a,all)."),
    }
    Path(HERE / "invention_ranking_v2.json").write_text(
        json.dumps(out, indent=2, sort_keys=True) + "\n")
    for r in results[:12]:
        print("%-34s score=%.3f  %s" % (
            r.get("family"), r["score"],
            {k: round(v, 3) for k, v in r.get("components", {}).items()}))


if __name__ == "__main__":
    main()
