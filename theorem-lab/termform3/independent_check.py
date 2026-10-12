#!/usr/bin/env python3
"""
An INDEPENDENT check of Report Q's decisive negative claim.

Report Q's positive result rests entirely on one negative: that the exhaustive
control `A3u` cannot reach `is_prime_power` or `odd_divisors` at cost <= 5. That
claim comes from `outer.py`, which is vectorised with numpy, deduplicates by a
blake2b digest of the value vector, and records target hits through a `watch`
dictionary. A bug in any of those three -- an operator mismatch, a digest
collision, a watch miss -- would manufacture exactly this result.

So the claim is re-derived here without any of them: plain Python tuples, the
reference `BINOPS` from `language.py`, exact tuple equality for dedup, and a direct
comparison against the library's own values. If this agrees, the negative does not
depend on the fast path.
"""
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
T2 = HERE.parent / "termform2"
sys.path.insert(0, str(HERE.parent / "termform"))
sys.path.insert(0, str(T2))

import invariants as INV                                     # noqa: E402
import synth3 as S                                           # noqa: E402
from round2 import TRAIN                                     # noqa: E402

OPS = ["add", "sub", "mul", "div", "mod", "pow", "gcd", "min", "max"]
TARGETS = ["is_prime_power", "odd_divisors", "is_squarefree", "v_2", "isqrt",
           "bit_length", "even_divisors", "is_prime", "is_square", "n_div_spf"]


def atoms_of(carry):
    """A3u's atom set (carry=False) or B3u's (carry=True), built exactly as
    ladder_r/round3 build it."""
    S.reset()
    forced = []
    if carry:
        from promote import parse
        cert = json.loads((HERE / "certificate.json").read_text())
        forced = [S.leaf(parse(t), TRAIN, cost=1) for t in cert["certified_out_of_reach"]]
    formed = S.form_leaves(TRAIN, size1=3, size2=3, extra_leaves=forced,
                           verbose=False, tag="ind")
    units = S.select_units(formed, TRAIN, 40 + len(forced), forced_leaves=forced)
    return [("var", "n")] + [("const", c) for c in S.CONSTS] + units


def vec(t):
    return tuple(S.ev(t, {"n": m}) for m in TRAIN)


def enumerate_plain(atoms, max_cost=5):
    """Every value vector reachable at cost <= max_cost, using the reference
    operators on plain tuples. Dedup is exact tuple equality, not a hash."""
    by_cost = {}
    seen = {}
    for t in atoms:
        c = S.size(t)
        if c > max_cost:
            continue
        try:
            v = vec(t)
        except Exception:
            continue
        by_cost.setdefault(c, []).append(v)
        seen.setdefault(v, c)
    B = S.BINOPS
    for s in range(3, max_cost + 1, 2):
        new = []
        for a in range(1, s):
            b = s - a - 1
            if b < 1:
                continue
            L, R = by_cost.get(a, ()), by_cost.get(b, ())
            if not L or not R:
                continue
            for v1 in L:
                for v2 in R:
                    for op in OPS:
                        f = B[op]
                        v = tuple(f(x, y) for x, y in zip(v1, v2))
                        if v not in seen:
                            seen[v] = s
                            new.append(v)
        by_cost.setdefault(s, []).extend(new)
    return seen


def main():
    t0 = time.time()
    out = {}
    for carry in (False, True):
        name = "B3u" if carry else "A3u"
        atoms = atoms_of(carry)
        seen = enumerate_plain(atoms)
        rows = {}
        for tgt in TARGETS:
            try:
                v = tuple(INV.LIBRARY[tgt](m) for m in TRAIN)
            except Exception:
                continue
            rows[tgt] = seen.get(v)          # minimal cost, or None if unreachable
        out[name] = {"atoms": len(atoms), "distinct_value_vectors": len(seen),
                     "minimal_cost_or_null": rows}
        print("%s: %d atoms, %d distinct value vectors (exact tuple dedup, reference ops)"
              % (name, len(atoms), len(seen)), flush=True)
        for k, v in sorted(rows.items()):
            print("    %-16s %s" % (k, "cost %d" % v if v else "UNREACHABLE"), flush=True)

    # the claims under test
    a, b = out["A3u"]["minimal_cost_or_null"], out["B3u"]["minimal_cost_or_null"]
    checks = {
        "A3u cannot reach is_prime_power": a.get("is_prime_power") is None,
        "A3u cannot reach odd_divisors": a.get("odd_divisors") is None,
        "B3u reaches is_prime_power": b.get("is_prime_power") is not None,
        "B3u reaches odd_divisors": b.get("odd_divisors") is not None,
        "both reach is_prime, is_square, n_div_spf":
            all(a.get(k) and b.get(k) for k in ("is_prime", "is_square", "n_div_spf")),
    }
    out["checks"] = checks
    out["seconds"] = round(time.time() - t0, 1)
    (HERE / "independent_check.json").write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print()
    for k, v in checks.items():
        print("%s %s" % ("ok  " if v else "FAIL", k))
    print("\n%.0fs" % out["seconds"])
    sys.exit(0 if all(checks.values()) else 1)


if __name__ == "__main__":
    main()
