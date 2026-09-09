#!/usr/bin/env python3
"""
PRIORITY 2 (first half) — apply the FROZEN promotion rule to Round 1.

The rule is quoted verbatim from `round1_manifest.json`, which was written and
hashed before any Round-2 target was chosen:

    "promote every certified term, plus every formed term appearing as a NAMED
     UNIT inside a certified term. Mechanical, applied before any Round-2
     result is seen; no hand selection."

This file only *applies* it. It performs no selection of its own, and it does
not look at Round-2 objects, targets or results.

Round-1 terms are stored in `result_v2.json` in printed form, e.g.

    count(k: (k // <count(k: (n % k))>))

where `<...>` marks a NAMED UNIT: a term that was itself formed earlier in
Round 1 and used as a size-1 atom. Promotion therefore has two parts: the outer
term, and every `<...>` body inside it. Both are parsed back into the tuple
representation of `termform/language.py` so that Round 2 re-evaluates them from
scratch on Round-2 objects -- no Round-1 value is carried across.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "termform"))

from language import ev, show, size  # noqa: E402

SYM = {"+": "add", "-": "sub", "*": "mul", "//": "div", "%": "mod", "^": "pow"}


def parse(s):
    """Parse the printed form back into a term. Total, and asserted below by
    round-tripping every parsed term through `show`."""
    s = s.strip()
    if s.startswith("<") and s.endswith(">") and _balanced(s[1:-1]):
        return parse(s[1:-1])
    if s.startswith("(") and s.endswith(")") and _balanced(s[1:-1]):
        inner = s[1:-1]
        d = 0
        # split on the top-level infix operator, rightmost first
        for i in range(len(inner) - 1, -1, -1):
            c = inner[i]
            if c in ")>":
                d += 1
            elif c in "(<":
                d -= 1
            elif d == 0 and c == " ":
                # candidate operator lies between two spaces
                j = inner.find(" ", i + 1)
                if j > i:
                    op = inner[i + 1:j]
                    if op in SYM:
                        return (SYM[op], parse(inner[:i]), parse(inner[j + 1:]))
        raise ValueError("infix: " + s)
    m = re.match(r"^(least|count)\(k: (.*)\)$", s, re.S)
    if m and _balanced(m.group(2)):
        return (m.group(1), parse(m.group(2)))
    m = re.match(r"^(gcd|min|max)\((.*)\)$", s, re.S)
    if m and _balanced(m.group(2)):
        args, d, start = [], 0, 0
        body = m.group(2)
        for i, c in enumerate(body):
            if c in "(<":
                d += 1
            elif c in ")>":
                d -= 1
            elif c == "," and d == 0:
                args.append(body[start:i])
                start = i + 1
        args.append(body[start:])
        return (m.group(1), parse(args[0]), parse(args[1]))
    if s in ("n", "k"):
        return ("var", s)
    if re.match(r"^\d+$", s):
        return ("const", int(s))
    raise ValueError("cannot parse: " + repr(s))


def _balanced(s):
    d = 0
    for c in s:
        if c in "(<":
            d += 1
        elif c in ")>":
            d -= 1
            if d < 0:
                return False
    return d == 0


def named_units(s):
    """Every `<...>` substring at any depth, outermost first."""
    out, d, start = [], 0, None
    for i, c in enumerate(s):
        if c == "<":
            if d == 0:
                start = i
            d += 1
        elif c == ">":
            d -= 1
            if d == 0:
                body = s[start + 1:i]
                out.append(body)
                out.extend(named_units(body))
    return out


def main():
    man = json.loads((HERE / "round1_manifest.json").read_text())
    rule = man["promotion_rule_for_round_2"]

    promoted, provenance = [], []
    seen = set()

    def add(printed, why, target):
        t = parse(printed)
        # round-trip: `show` has no <> markers, so compare structure only
        assert show(t) == printed.replace("<", "").replace(">", ""), \
            (show(t), printed)
        key = repr(t)
        if key in seen:
            for p in provenance:
                if p["term"] == show(t) and target not in p["from_targets"]:
                    p["from_targets"].append(target)
            return
        seen.add(key)
        promoted.append(t)
        provenance.append({"term": show(t), "expanded_size": size(t),
                           "reason": why, "from_targets": [target]})

    for c in man["certified_terms"]:
        add(c["term"], "certified Round-1 term", c["target"])
    for c in man["certified_terms"]:
        for u in named_units(c["term"]):
            add(u, "named unit inside a certified term", c["target"])

    out = {
        "label": "PROMOTED_V1",
        "promotion_rule": rule,
        "applied_by": "termform2/promote.py",
        "source_manifest_sha256": hashlib.sha256(
            (HERE / "round1_manifest.json").read_bytes()).hexdigest(),
        "count": len(promoted),
        "terms": provenance,
        "term_tuples": [repr(t) for t in promoted],
        "note": ("Round 2 re-evaluates every promoted term from its tuple form "
                 "on Round-2 objects. No Round-1 value is carried across."),
    }
    (HERE / "promoted_terms.json").write_text(
        json.dumps(out, indent=1, sort_keys=True) + "\n")

    print("promoted %d distinct terms\n" % len(promoted))
    for p in provenance:
        vals = [ev(parse(p["term"]), {"n": n}) for n in (6, 10, 12, 16, 30, 36)]
        print("  exp.size %2d  %-52s %s" % (p["expanded_size"],
                                            p["term"][:52], vals))
        p["values_6_10_12_16_30_36"] = vals
    (HERE / "promoted_terms.json").write_text(
        json.dumps(out, indent=1, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
