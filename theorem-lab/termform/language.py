#!/usr/bin/env python3
"""
A small total arithmetic language in which new terms can be FORMED.

Everything is bounded and total: division and modulo by zero yield 0, `pow` is
capped, and the two higher-order constructs range over [2..n] and [1..n]. No
primitive names a prime, a factorisation, a totient or an exponent; `spf` is
expected to emerge as `least(k -> n % k)`.

Terms are tuples: ("op", arg, ...). Evaluation is pure and side-effect free.
"""
import math

POW_CAP = 10 ** 9


def _div(a, b):
    return a // b if b else 0


def _mod(a, b):
    return a % b if b else 0


def _pow(a, b):
    if a <= 1:
        return a ** min(b, 1) if a else 0
    if b > 40:
        return POW_CAP
    v = a ** b
    return v if v <= POW_CAP else POW_CAP


BINOPS = {
    "add": lambda a, b: a + b,
    "sub": lambda a, b: max(0, a - b),
    "mul": lambda a, b: min(a * b, POW_CAP),
    "div": _div,
    "mod": _mod,
    "gcd": math.gcd,
    "min": min,
    "max": max,
    "pow": _pow,
}


def ev(t, env):
    """Evaluate a term in an environment mapping variable names to ints."""
    head = t[0]
    if head == "var":
        return env[t[1]]
    if head == "const":
        return t[1]
    if head == "least":
        n = env["n"]
        for k in range(2, n + 1):
            if ev(t[1], {**env, "k": k}) == 0:
                return k
        return 0
    if head == "count":
        n = env["n"]
        c = 0
        for k in range(1, n + 1):
            if ev(t[1], {**env, "k": k}) == 0:
                c += 1
        return c
    if head in BINOPS:
        return BINOPS[head](ev(t[1], env), ev(t[2], env))
    raise ValueError(head)


def size(t):
    if t[0] in ("var", "const"):
        return 1
    if t[0] in ("least", "count"):
        return 1 + size(t[1])
    return 1 + size(t[1]) + size(t[2])


def show(t):
    h = t[0]
    if h == "var":
        return t[1]
    if h == "const":
        return str(t[1])
    if h in ("least", "count"):
        return "%s(k: %s)" % (h, show(t[1]))
    sym = {"add": "+", "sub": "-", "mul": "*", "div": "//", "mod": "%",
           "pow": "^"}.get(h)
    if sym:
        return "(%s %s %s)" % (show(t[1]), sym, show(t[2]))
    return "%s(%s, %s)" % (h, show(t[1]), show(t[2]))
