#!/usr/bin/env python3
"""
PREREG_R section 4, the PADDED control: `python3 padded.py N`.

Same atom count as a rung that carried N terms, made up with the receiving round's
own next-best formed units instead of carried ones. If a rung's gain survives this,
it is not an atom-count effect.

Written after the random control because PREREG_R promised both and the first
implementation of `ladder_r.py` shipped only one. Run before any rung's result was
interpreted.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from ladder_r import UNITS, run_rung                         # noqa: E402
import ladder_r as L                                         # noqa: E402


def main():
    n = int(sys.argv[1])
    L.UNITS = UNITS + n
    r, _, _ = run_rung([], "padded%d" % n, "padded control: %d extra self-formed units" % n)
    out = {"label": "PADDED_CONTROL", "extra_units": n,
           "atoms": r["atoms"], "classes": r["classes"], "exhausted": r["exhausted"],
           "certified_count": r["certified_count"], "net_new": r["net_new"],
           "certified": r["certified"]}
    (HERE / ("padded_%d.json" % n)).write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print("padded(+%d): %d atoms, %d classes, exhausted=%s, certified %d, net new %d"
          % (n, r["atoms"], r["classes"], r["exhausted"], r["certified_count"],
             len(r["net_new"])))


if __name__ == "__main__":
    main()
