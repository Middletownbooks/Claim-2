#!/usr/bin/env python3
"""Check that every quote in stale_statements.json still occurs verbatim in its file.

A pointer list goes stale in the same way the statements it points at did. If a cited file is
edited and the quote disappears, this fails and names the row, rather than leaving a register that
reads like evidence and points at nothing (the D52 defect class). Line numbers are re-derived, not
trusted: a quote found on a different line is reported and is not a failure.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def main():
    rows = json.load(open(os.path.join(HERE, "stale_statements.json"), encoding="utf-8"))["rows"]
    missing, moved = [], 0
    for r in rows:
        p = os.path.join(ROOT, r["file"])
        lines = open(p, encoding="utf-8").read().split("\n") if os.path.exists(p) else []
        hit = [i + 1 for i, l in enumerate(lines) if r["quote"][:80] in l]
        if not hit:
            missing.append(r)
        elif r["line"] not in hit:
            moved += 1
    for r in missing:
        print("MISSING  %s:%s  %r" % (r["file"], r["line"], r["quote"][:70]), file=sys.stderr)
    print("%d rows; %d quotes found (%d on a different line than recorded); %d missing" % (
        len(rows), len(rows) - len(missing), moved, len(missing)))
    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
