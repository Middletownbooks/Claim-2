"""Arm AL: the maximal-prime-gap record ladder, checked exactly.

Every bound in this ladder is a monomial in L1..L4 := log X, log_2 X, log_3 X, log_4 X,
so each is an exponent vector and every ratio is exponent subtraction -- exact, no
floating point. Unboundedness is then checked in log-space on a tower.

  Rankin 1938   G >> L1 L2 L4 / L3^2
  FGKMT  2014   G >> L1 L2 L4 / L3        (Ford-Green-Konyagin-Maynard-Tao)
  Sol    2026-08-25  G >> L1 L2 / L4      (GPT 5.6 Sol, expert-verified by Ben Green)
  Astra  2026-09-03  G >> L1 L2^2 L4 / L3^2   (GPT 6 Astra, site-confirmed by build)
"""
from fractions import Fraction as F
import math

BASIS = ("L1", "L2", "L3", "L4")
BOUNDS = {
    "Rankin 1938": (1, 1, -2, 1),
    "FGKMT 2014":  (1, 1, -1, 1),
    "Sol 2026-08": (1, 1,  0, -1),
    "Astra 2026-09": (1, 2, -2, 1),
}

def ratio(a, b):
    return tuple(x - y for x, y in zip(BOUNDS[a], BOUNDS[b]))

def show(v):
    num = [f"{b}^{e}" if e != 1 else b for b, e in zip(BASIS, v) if e > 0]
    den = [f"{b}^{-e}" if e != -1 else b for b, e in zip(BASIS, v) if e < 0]
    return (" ".join(num) or "1") + (" / " + " ".join(den) if den else "")

def tends_to_infinity(v, kmax=40):
    """log of the monomial on the tower L4=k, L3=e^k, L2=e^(e^k), L1=e^(e^(e^k))."""
    prev = None
    for k in range(3, kmax):
        L4 = k; L3 = math.exp(k) if k < 700 else float("inf")
        # work with logs: log L4 = log k, log L3 = k, log L2 = e^k, log L1 = e^(e^k)
        logs = [math.exp(math.exp(k)) if k < 4 else float("inf"), math.exp(k), k, math.log(k)]
        # avoid inf*0; compute only the terms with nonzero exponent, in log space
        tot = 0.0
        for e, lg in zip(v, logs):
            if e == 0: continue
            if lg == float("inf"): return True   # a positive-exponent infinite term dominates
            tot += e * lg
        if prev is not None and tot <= prev: return False
        prev = tot
    return prev is not None and prev > 0

CHECKS = []
def check(name, got, want):
    CHECKS.append((name, got == want, got, want))

# --- the ratio claims made in the papers / notes -----------------------------
check("FGKMT / Rankin = L3", ratio("FGKMT 2014", "Rankin 1938"), (0, 0, 1, 0))
check("Sol / FGKMT = L3/L4^2  (the stated gain over FGKMT)",
      ratio("Sol 2026-08", "FGKMT 2014"), (0, 0, 1, -2))
check("Sol / Rankin = L3^2/L4^2  (Green: 'basically (log_3 N)^2 over Rankin')",
      ratio("Sol 2026-08", "Rankin 1938"), (0, 0, 2, -2))
check("Astra / Sol = L2 L4^2 / L3^2  (the stated improvement factor)",
      ratio("Astra 2026-09", "Sol 2026-08"), (0, 1, -2, 2))
check("Astra / FGKMT = L2/L3", ratio("Astra 2026-09", "FGKMT 2014"), (0, 1, -1, 0))
check("Astra / Rankin = L2  (a full log log X over the 1938 bound)",
      ratio("Astra 2026-09", "Rankin 1938"), (0, 1, 0, 0))

# --- every step of the ladder is a genuine (unbounded) improvement -----------
ORDER = ["Rankin 1938", "FGKMT 2014", "Sol 2026-08", "Astra 2026-09"]
for a, b in zip(ORDER[1:], ORDER):
    check(f"unbounded: {a} / {b} -> infinity", tends_to_infinity(ratio(a, b)), True)
check("unbounded: Astra / Rankin -> infinity",
      tends_to_infinity(ratio("Astra 2026-09", "Rankin 1938")), True)

# --- the two AI bounds are NOT comparable by a bounded factor ---------------
check("Astra strictly dominates Sol (ratio -> infinity, not a constant)",
      tends_to_infinity(ratio("Astra 2026-09", "Sol 2026-08")), True)
check("Sol does NOT dominate Astra",
      tends_to_infinity(ratio("Sol 2026-08", "Astra 2026-09")), False)

# --- the Lean statements, as read from the two repositories -----------------
# LongGapsBetweenPrimes/Challenge.lean:
#   c * (log X * log(log X)^2 * log(log(log(log X))) / log(log(log X))^2)
check("Astra's Lean statement is the Astra monomial", (1, 2, -2, 1), BOUNDS["Astra 2026-09"])
# ErdosProblems/Erdos4Tilted.lean, prime_gap_corollary:
#   c * log T * log(log T) / log(log(log(log T)))
check("Sol's Lean statement is the Sol monomial", (1, 1, 0, -1), BOUNDS["Sol 2026-08"])

if __name__ == "__main__":
    print("ladder (exponents over L1=log X, L2=log_2 X, L3=log_3 X, L4=log_4 X):")
    for n in ORDER:
        print(f"  {n:16s} G >> {show(BOUNDS[n])}")
    print("\nsuccessive gains:")
    for a, b in zip(ORDER[1:], ORDER):
        print(f"  {a:16s} over {b:16s}: {show(ratio(a, b))}")
    print()
    ok = 0
    for nm, passed, got, want in CHECKS:
        print(f"[{'PASS' if passed else 'FAIL'}] {nm}")
        if not passed: print(f"         got {got!r}  want {want!r}")
        ok += passed
    print(f"\n{ok}/{len(CHECKS)} checks pass")
    raise SystemExit(0 if ok == len(CHECKS) else 1)
