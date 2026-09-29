#!/usr/bin/env python3
"""Score Test G (SELECT_v1.md Part I sec 6) from a worker's label file.

Written and negative-tested BEFORE any label file existed. Joins the worker's MOVE-1 kind per
problem with the registered outcome coding in aerp_outcomes.json and computes

    G-1  D1 = P(IMPROVED | IDEA) - P(IMPROVED | COMPUTE)       validated iff D1 > 0
    G-2  D2 = P(IMPROVED | SEARCH-NEW) - P(IMPROVED | ANALYTIC)  validated iff D2 > 0

IDEA = ANALYTIC or SEARCH-NEW, COMPUTE = SEARCH-REPEAT. A statistic whose smaller class has
fewer than 4 problems is UNEVALUABLE, which the registration counts as NOT VALIDATED.

It refuses to score (exit 2) rather than guess when the file does not parse into exactly one
block per problem of the slice -- a scorer that silently skips a malformed block is a check that
cannot fail.

usage: score_test_g.py LABELS.md {odd|even} [--flip N ...]
"""
from __future__ import annotations
import json, pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent
KINDS = ("ANALYTIC", "SEARCH-NEW", "SEARCH-REPEAT", "UNKNOWN")
MIN_N = 4


def parse(text: str) -> dict[int, dict]:
    """One dict per PROBLEM block: n, record (YES/NO-RECORD), kind, ai, tier."""
    blocks: dict[int, dict] = {}
    cur = None
    for raw in text.splitlines():
        line = raw.strip().strip("`")
        m = re.match(r"PROBLEM\s*\|\s*(\d+)\b", line)
        if m:
            n = int(m.group(1))
            if n in blocks:
                raise ValueError(f"problem {n} appears twice")
            cur = blocks[n] = {"n": n, "record": None, "kind": None, "ai": False, "tier": None}
            continue
        if cur is None:
            continue
        m = re.match(r"RECORD\s*\|\s*(.*)", line)
        if m:
            v = m.group(1).upper()
            cur["record"] = "NO-RECORD" if v.startswith("NO-RECORD") or v.startswith("NO RECORD") \
                else ("YES" if v.startswith("YES") else "UNPARSED")
            continue
        m = re.match(r"MOVE-1\s*\|\s*(.*)", line)
        if m:
            # The kind is the FIRST field carrying an upper-case kind token. Later fields are
            # evidence prose, which may legitimately say "not a SEARCH-REPEAT"; matching is
            # case-sensitive so prose like "an analytic construction" never counts.
            fields = [f.strip() for f in m.group(1).split("|")]
            found: list[str] = []
            for f in fields:
                found = [k for k in KINDS if re.search(rf"(?<![A-Za-z-]){k}(?![A-Za-z-])", f)]
                if found:
                    break
            cur["kind"] = found[0] if len(found) == 1 else ("AMBIGUOUS" if found else "MISSING")
            cur["ai"] = "AI-SEARCH" in m.group(1).upper()
            tiers = re.findall(r"PRIMARY-VERIFIED-LOCALLY|SECONDARY-RELAYED|SEARCH-SUMMARY|RECALL",
                               m.group(1).upper())
            cur["tier"] = tiers[-1] if tiers else None
    return blocks


def score(blocks: dict[int, dict], slice_ns: list[int], outcome: dict[int, str]) -> dict:
    missing = sorted(set(slice_ns) - set(blocks))
    extra = sorted(set(blocks) - set(slice_ns))
    if missing or extra:
        raise ValueError(f"slice mismatch: missing {missing}, unexpected {extra}")
    rows, excluded = [], {"known-optimal": [], "no-record": [], "unknown-kind": [],
                          "unparsed": []}
    for n in slice_ns:
        b, o = blocks[n], outcome[n]
        if o == "EXCLUDED-KNOWN-OPTIMAL":
            excluded["known-optimal"].append(n); continue
        if b["record"] == "NO-RECORD":
            excluded["no-record"].append(n); continue
        if b["record"] != "YES" or b["kind"] in (None, "MISSING", "AMBIGUOUS"):
            excluded["unparsed"].append(n); continue
        if b["kind"] == "UNKNOWN":
            excluded["unknown-kind"].append(n); continue
        rows.append({"n": n, "kind": b["kind"], "improved": o == "IMPROVED", "tier": b["tier"],
                     "ai": b["ai"]})

    def rate(pred):
        s = [r for r in rows if pred(r)]
        return (sum(r["improved"] for r in s), len(s), [r["n"] for r in s])

    def stat(a, b):
        (ka, na, la), (kb, nb, lb) = a, b
        if min(na, nb) < MIN_N:
            return {"value": None, "verdict": "UNEVALUABLE -> NOT VALIDATED",
                    "a": f"{ka}/{na}", "b": f"{kb}/{nb}", "a_list": la, "b_list": lb}
        d = ka / na - kb / nb
        return {"value": round(d, 4), "verdict": "VALIDATED" if d > 0 else "NOT VALIDATED",
                "a": f"{ka}/{na}", "b": f"{kb}/{nb}", "a_list": la, "b_list": lb}

    idea = rate(lambda r: r["kind"] in ("ANALYTIC", "SEARCH-NEW"))
    comp = rate(lambda r: r["kind"] == "SEARCH-REPEAT")
    sn = rate(lambda r: r["kind"] == "SEARCH-NEW")
    an = rate(lambda r: r["kind"] == "ANALYTIC")
    return {"testable": len(rows), "excluded": excluded,
            "G-1": stat(idea, comp), "G-2": stat(sn, an),
            "by_kind": {k: rate(lambda r, k=k: r["kind"] == k)[:2] for k in KINDS[:3]},
            "rows": rows}


def main(argv: list[str]) -> int:
    if len(argv) < 3 or argv[2] not in ("odd", "even"):
        print(__doc__); return 2
    labels = pathlib.Path(argv[1]).read_text(encoding="utf-8")
    flips = [int(x) for x in argv[argv.index("--flip") + 1:]] if "--flip" in argv else []
    oc = json.loads((HERE / "aerp_outcomes.json").read_text())["outcome"]
    outcome = {int(k): v for k, v in oc.items()}
    for n in flips:
        outcome[n] = {"IMPROVED": "NOT-IMPROVED", "NOT-IMPROVED": "IMPROVED"}[outcome[n]]
    ns = [n for n in range(1, 68) if n % 2 == (1 if argv[2] == "odd" else 0)]
    try:
        res = score(parse(labels), ns, outcome)
    except ValueError as e:
        print(f"REFUSED TO SCORE: {e}"); return 2
    print(json.dumps({k: v for k, v in res.items() if k != "rows"}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
