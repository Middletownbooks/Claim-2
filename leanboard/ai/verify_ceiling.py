"""Independent arithmetic audit of moffatstudio/union-closed-constant (VibeMathed,
"The ceiling of the single-letter entropy method for the union-closed sets conjecture").

Checks every constant in the paper's Theorems A/B/C against a from-scratch computation.
This does NOT rebuild the Lean development (no toolchain here); source-level and
definitional checks are recorded in REPORT_AI_ceiling_audit.md.
"""

from math import log2, sqrt

def h(x):
    """Binary entropy in bits, the paper's `ent`; h(1/2) = 1."""
    return 0.0 if x in (0.0, 1.0) else -x * log2(x) - (1 - x) * log2(1 - x)

CHECKS = []
def check(name, got, want, tol=0.0):
    ok = (got == want) if tol == 0.0 else (abs(got - want) <= tol)
    CHECKS.append((name, ok, got, want))

# --- h is the right function -------------------------------------------
check("h(1/2) = 1 (bits normalisation)", h(0.5), 1.0, 1e-15)
check("h(0) = h(1) = 0", (h(0.0), h(1.0)), (0.0, 0.0))
check("h <= 1 on a grid", all(h(i/1000) <= 1 + 1e-12 for i in range(1001)), True)

# --- Theorem A: c_ceil = 1 - h(1/sqrt2)/sqrt2 ---------------------------
xs = 1 / sqrt(2)
c_ceil = 1 - h(xs) / sqrt(2)
check("Theorem A: c_ceil", c_ceil, 0.3830992976, 1e-9)
# the alternate form stated in CEILING_THEOREM.md, 1 - (1/sqrt2)*h(1/sqrt2)/h(1/2)
check("Theorem A: alternate form agrees", 1 - (1/sqrt(2))*h(xs)/h(0.5), c_ceil, 1e-15)
# the proof's own arithmetic: p >= h(x*), mean = 1 - p/sqrt2
check("Theorem A: proof step mean = 1 - h(x*)/sqrt2", 1 - h(xs)/sqrt(2), c_ceil, 1e-15)
# the step "h(Prot(0,0)) <= 1 = h(x*^2)" needs x*^2 = 1/2 exactly
check("Theorem A: x*^2 = 1/2 (so h(x*^2) = 1)", xs*xs, 0.5, 1e-15)

# --- Theorem B: the (H)+(D) fixed point ---------------------------------
cpp = 0.382885260
check("Theorem B: w_iid from (H) 2*w*(1-c)=1", 1/(2*(1-cpp)), 0.810222, 1e-6)
check("Theorem B: beta = 1 - w_iid", 1 - 1/(2*(1-cpp)), 0.189778, 1e-6)
check("Theorem B: c** < c_ceil (refined is tighter)", cpp < c_ceil, True)

# --- the record chain is below both ceilings ----------------------------
CHAIN = [("Gilmer/iid (3-sqrt5)/2", (3-sqrt(5))/2), ("Sawin-Yu-Cambie", 0.3823455),
         ("Liu 2023", 0.382709), ("this paper, certified", 0.38284)]
for nm, v in CHAIN:
    check(f"chain below c**: {nm}", v < cpp, True)
check("chain is increasing", all(CHAIN[i][1] < CHAIN[i+1][1] for i in range(len(CHAIN)-1)), True)

# --- the headroom claims ------------------------------------------------
check("headroom c** - Liu ~ 1.8e-4", cpp - 0.382709, 1.8e-4, 2e-5)
check("paper: +0.000176 over Liu (at 0.382885)", 0.382885 - 0.382709, 0.000176, 5e-7)
check("paper: +0.000131 over Liu (certified)", 0.38284 - 0.382709, 0.000131, 5e-7)
# NOTE: the correction block leaves "+0.00054 over Cambie" attached to the certified
# constant; that figure belongs to 0.382885, not to 0.38284.
check("+0.00054 over Cambie holds for 0.382885", 0.382885 - 0.3823455, 0.00054, 5e-6)
check("...but NOT for the certified 0.38284", abs((0.38284 - 0.3823455) - 0.00054) > 5e-6, True)
check("correct Cambie delta for certified", 0.38284 - 0.3823455, 0.0004945, 1e-7)

# --- Lean's numeric bound vs the headline -------------------------------
lean = 3829/10000
check("Lean proves c <= 0.3829", lean, 0.3829, 1e-15)
check("Lean bound is WEAKER than c**", lean > cpp, True)
check("Lean bound still excludes 1/2 (Frankl out of range)", lean < 0.5, True)
check("Lean bound does NOT pin the paper's own record", 0.38284 < lean, True)
check("gap Lean - c**", lean - cpp, 1.474e-5, 1e-8)
check("headroom left above certified, to c**", cpp - 0.38284, 4.526e-5, 1e-8)

if __name__ == "__main__":
    ok = 0
    for nm, passed, got, want in CHECKS:
        print(f"[{'PASS' if passed else 'FAIL'}] {nm}\n         got {got!r}  want {want!r}")
        ok += passed
    print(f"\n{ok}/{len(CHECKS)} checks pass")
    raise SystemExit(0 if ok == len(CHECKS) else 1)
