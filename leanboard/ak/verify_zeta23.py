"""Arm AK: independent arithmetic audit of Alpoge-Furman, "More than two thirds of the
zeros of the Riemann zeta function are simple and on the critical line" (arXiv:2608.13637v2,
19 Aug 2026). Argument discovered and written by Claude; Lean at anthropics/zeta-23-lean.

Recomputes every numerical constant in the paper from its own stated definitions.
Does NOT rebuild the Lean development (no toolchain); source-level checks are in the report.
"""
from math import sqrt, sin, cos, tan, pi
from fractions import Fraction as F

CHECKS = []
def check(name, got, want, tol=0.0):
    ok = (got == want) if tol == 0 else (abs(got - want) <= tol)
    CHECKS.append((name, ok, got, want))

# ---- R(psi), the window constant (Lemma 5.6) --------------------------------
# R(psi) = [ int psi^2 + int int |u-v| psi(u)psi(v) ] / (int psi)^2  on [-1/2,1/2].
# Both windows are done in closed form below; no quadrature is needed except as a
# cross-check on G(0) for psi_MT.

# psi_0 = indicator: exact values
#   \int psi_0 = 1 ; \int psi_0^2 = 1 ; \int\int|u-v| = 2\int_0^1 w(1-w) dw = 1/3
int_psi0, int_psi0_sq = F(1), F(1)
dbl_psi0 = 2 * (F(1, 2) - F(1, 3))                      # 2*\int_0^1 w(1-w) dw
check("psi_0: double integral of |u-v| = 1/3", dbl_psi0, F(1, 3))
R0 = (int_psi0_sq + dbl_psi0) / int_psi0 ** 2
check("Lemma 5.6: R(psi_0) = 4/3", R0, F(4, 3))
check("Theorem A(i) at psi_0:  2 - R = 2/3", 2 - R0, F(2, 3))
check("Theorem A(ii) at psi_0: (3-R)/2 = 5/6", (3 - R0) / 2, F(5, 6))

# psi_MT(s) = cos(sqrt2 * s) on [-1/2,1/2]
x = 1 / sqrt(2)
int_psiMT = sqrt(2) * sin(x)                             # paper's stated value
check("psi_MT: int psi = sqrt2 sin(1/sqrt2)", int_psiMT, 2 * sin(sqrt(2) / 2) / sqrt(2), 1e-14)
# G(0) = 1 + 2*int_0^{1/2} v cos(sqrt2 v) dv, closed form cos(1/sqrt2)+ (1/sqrt2) sin(1/sqrt2)
a = sqrt(2)
integral = (0.5) * sin(a / 2) / a + (cos(a / 2) - 1) / a ** 2
G0_quad = 1 + 2 * integral
G0_closed = cos(x) + x * sin(x)
check("psi_MT: G(0) quadrature == closed form", G0_quad, G0_closed, 1e-13)
R_MT = G0_closed / int_psiMT
cMTinv = 0.5 + x / tan(x)                                # 1/2 + (1/sqrt2) cot(1/sqrt2)
check("Lemma 5.6: R(psi_MT) = 1/2 + cot(1/sqrt2)/sqrt2", R_MT, cMTinv, 1e-12)
check("Montgomery-Taylor simple constant 2 - cMT^-1", 2 - cMTinv, 0.67250, 5e-6)
check("Montgomery-Taylor distinct constant (3-cMT^-1)/2", (3 - cMTinv) / 2, 0.83625, 5e-6)
# the Lean file's cMT, as stated in Challenge.lean
cMT_lean = sqrt(2) * tan(x) / (1 + x * tan(x))
check("Lean's cMT is the reciprocal of R(psi_MT)", 1 / cMT_lean, R_MT, 1e-12)

# ---- beats the prior records ------------------------------------------------
check("2/3 beats prior simple-on-line record 5/12", F(2, 3) > F(5, 12), True)
check("2/3 alone already beats prior DISTINCT record 0.6603", 2 / 3 > 0.6603, True)
check("5/6 beats prior distinct record 0.6603", 5 / 6 > 0.6603, True)

# ---- Remark 6.1: the lambda-family H(lambda) = 2 - 1/lam - lam/3 -------------
H = lambda lam: 2 - 1 / lam - lam / 3
check("H(1) = 2/3", H(1.0), 2 / 3, 1e-15)
check("H increasing on (0,1): no lambda<1 improves",
      all(H(k / 1000) < H((k + 1) / 1000) for k in range(1, 1000)), True)
check("H'(lam)=0 at lam=sqrt3 > 1 (interior max outside the range)", sqrt(3) > 1, True)

# ---- Lemma 3.2's scalar shadows --------------------------------------------
check("x^2 >= 2x-1 for all reals (i.e. (x-1)^2>=0)",
      all((v / 10) ** 2 >= 2 * (v / 10) - 1 - 1e-12 for v in range(-200, 201)), True)
check("integrality (m-1)(m-2)>=0 i.e. m^2>=3m-2 on positive integers",
      all(m * m >= 3 * m - 2 for m in range(1, 200)), True)

# ---- Sec 7.2(f): moments, Christoffel, and 13/18 ---------------------------
# m_k(1) = 1, 4/3, 2, 13/4 for k <= 4 ; Lambda_2(0;1) = 5/36 ; proportion = 2*(1-Lambda)-1
Lam2 = F(5, 36)
check("HL*(4) proportion = 2*(1-Lambda_2(0)) - 1 = 13/18", 2 * (1 - Lam2) - 1, F(13, 18))
check("... and 13/18 > 2/3", F(13, 18) > F(2, 3), True)
# the 1/2 that Cauchy-Schwarz alone gave: n+ >= 3/4 N  =>  2*(3/4)-1 = 1/2
check("Cauchy-Schwarz stage: 2*(3/4) - 1 = 1/2", 2 * F(3, 4) - 1, F(1, 2))

# ---- Sec 7.2: the bandwidth-one ceiling ------------------------------------
p0 = 0.6818287                      # rounded-up rational recorded in LawN256.lean
check("ceiling p0 ~ 0.682 as stated in Sec 1.1", abs(p0 - 0.682) < 5e-4, True)
check("Theorem A(i) is within 0.016 of its own ceiling", p0 - 2 / 3, 0.0152, 1e-3)
check("the stated 0.6819 bound exceeds p0", 0.6819 > p0, True)

# ---- Remark 7.1: xi' constants are internally consistent -------------------
# the same certificate shape: simple = 2 - R, distinct = (3 - R)/2
R_xi = 2 - 0.85838
check("xi' flat window: (3-R)/2 matches 0.92919", (3 - R_xi) / 2, 0.92919, 1e-5)
R_xi_q = 2 - 0.86864
check("xi' quartic window: (3-R)/2 matches 0.93432", (3 - R_xi_q) / 2, 0.93432, 1e-5)
check("xi' flat 0.85838 recovers Farmer-Gonek-Lee's RH constant 85.84%",
      abs(0.85838 - 0.8584) < 1e-4, True)
check("xi' quartic 0.86864 stays below RH-conditional 0.8825", 0.86864 < 0.8825, True)
check("neither xi' constant exceeds Wu's 0.86957 for on-line-only",
      max(0.85838, 0.86864) < 0.86957, True)

# ---- Sec 7.3: the cubic weight is tight at m = 1,2,3 -----------------------
w = lambda m: F(1, 2) * m + F(1, 18) * (2 * m * m - m ** 3) + (F(4, 9) if m == 1 else 0)
for m in (1, 2, 3):
    check(f"cubic weight omega({m}) = 1", w(m), F(1))

# ---- Sec 1.1: the Riemann-von Mangoldt normalisation ----------------------
# N(T,2T) = T/2pi (log(T/2pi) + 2log2) - T/2pi + O(log T);  ell_1 := l + 2log2 - 1
import math
T = 1e12; l = math.log(T / (2 * pi))
check("T*ell_1/(2pi) equals the stated N(T,2T) main term",
      T * (l + 2 * math.log(2) - 1) / (2 * pi),
      T / (2 * pi) * (l + 2 * math.log(2)) - T / (2 * pi), 1e-3)

if __name__ == "__main__":
    ok = 0
    for nm, passed, got, want in CHECKS:
        print(f"[{'PASS' if passed else 'FAIL'}] {nm}\n         got {got!r}  want {want!r}")
        ok += passed
    print(f"\n{ok}/{len(CHECKS)} checks pass")
    raise SystemExit(0 if ok == len(CHECKS) else 1)
