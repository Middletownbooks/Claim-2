#!/usr/bin/env python3
"""
General deformation oracle (Phase 8).

Unlike lab.py's worker, this one does not know a fixed list of families. It
evaluates ANY proposed exponent identity, so a searcher can invent families and
ask about them. It contains no number theory: it brute-forces the definition.

request  = {"lhs": <expr>, "rhs": <expr>, "domain": "all"|"units",
            "m": int, "a": int, "b": int}
expr     = one of the strings in EXPRS, evaluated at (a, b)
response = {"truth": bool, "witness": int|None, "fail_count": int,
            "pass_count": int}
"""
import json
import math
import sys

EXPRS = {
    "1": lambda a, b: 1,
    "a": lambda a, b: a,
    "b": lambda a, b: b,
    "a+1": lambda a, b: a + 1,
    "a+2": lambda a, b: a + 2,
    "2a": lambda a, b: 2 * a,
    "a+b": lambda a, b: a + b,
    "ab": lambda a, b: a * b,
}


def answer(req):
    m = int(req["m"])
    a, b = int(req["a"]), int(req["b"])
    if m < 1 or a < 1 or b < 1:
        raise ValueError("parameters must be positive")
    e1 = EXPRS[req["lhs"]](a, b)
    e2 = EXPRS[req["rhs"]](a, b)
    units_only = req.get("domain") == "units"
    witness = None
    fails = passes = 0
    for x in range(m):
        if units_only and math.gcd(x, m) != 1:
            continue
        ok = pow(x, e1, m) == pow(x, e2, m)
        if ok:
            passes += 1
        else:
            fails += 1
            if witness is None:
                witness = x
    return {"truth": fails == 0, "witness": witness,
            "fail_count": fails, "pass_count": passes}


def main():
    for line in sys.stdin:
        try:
            r = answer(json.loads(line))
        except Exception as exc:
            r = {"error": repr(exc)}
        print(json.dumps(r, sort_keys=True, separators=(",", ":")), flush=True)


if __name__ == "__main__":
    main()
