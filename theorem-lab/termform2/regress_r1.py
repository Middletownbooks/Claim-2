#!/usr/bin/env python3
"""Regression: synth3 must reproduce Round 1 when configured as Round 1.

The 500-unit selection differs by design (synth3 replaced the printed-form
tie-break), so the check is on the two things that are not tie-break
dependent: the number of formed terms, and whether the Round-1 nu discovery is
recovered at the same cost."""
import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "termform"))
import synth3 as S
from run import TRAIN, HOLDOUT, Oracle

t0 = time.time()
S.reset()
formed = S.form_leaves(TRAIN)
print("formed = %d   (Round 1 recorded 5329)" % len(formed))

o = Oracle()
nu = {m: o.threshold(m) for m in TRAIN + HOLDOUT}
o.close()
tgt = tuple(nu[m] for m in TRAIN)

direct = [t for t in formed.values()
          if tuple(S.ev(t, {"n": m}) for m in TRAIN) == tgt]
print("direct formed-term hits for nu: %d" % len(direct))
for t in sorted(direct, key=S.size)[:5]:
    print("   cost %d  %s" % (S.size(t), S.show(t)))
print("%.0fs" % (time.time() - t0))
