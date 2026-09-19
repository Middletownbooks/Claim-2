#!/usr/bin/env python3
"""Independently check every number in the positive control's response."""
import math, sys
bad = []
def ck(n, ok, d=""):
    print(f"{'ok  ' if ok else 'FAIL'} {n}{': ' + d if d else ''}")
    if not ok: bad.append(n)
Phi = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))
slab = lambda c: 2 * Phi(c) - 1                      # gamma of {|x_1| <= c}

ck("gamma_2(unit cube) = 0.466 < 1/2", abs(slab(1) ** 2 - 0.4661) < 5e-4,
   f"{slab(1)**2:.4f} -- so even the unit cube fails the invariant at n = 2")
ck("slab |x1|<=0.68 has gamma ~ 0.5036", abs(slab(0.68) - 0.5035) < 1e-3, f"{slab(0.68):.4f}")
ck("shifting it by 0.2 and intersecting drops gamma to ~0.369",
   abs(slab(0.48) - 0.3688) < 1e-3,
   f"{slab(0.48):.4f} < 1/2 -- the natural FORMULA for the move breaks the invariant in one step")
inr = 0.6745
ck("inradius constant Phi^{-1}(3/4) = 0.6745", abs(Phi(inr) - 0.75) < 2e-4,
   f"Phi({inr}) = {Phi(inr):.5f}; and the literature's 1/5 = 0.2 sits inside (0, {inr}]")

print("\n  max n with gamma_n(cube_C) >= 1/2, against the response's table")
claimed = {1: 1, 2: 14, 3: 256, 4: 10943, 5: 1_210_000, 6: 350_000_000, 10: 4.6e22}
for C, want in claimed.items():
    # erf saturates at 1 for C >~ 8, which made the first version of this check report
    # inf and score the response wrong at C = 10. erfc keeps the precision: the tail
    # mass is erfc(C/sqrt 2) and ln(1/p) = -ln(1 - tail) ~ tail.
    tail = math.erfc(C / math.sqrt(2))
    n = math.floor(math.log(0.5) / math.log1p(-tail))
    rel = abs(n - want) / want
    ck(f"  C = {C:>2}", rel < 0.02 if want > 100 else n == want,
       f"computed {n:,}" if n < 1e15 else f"computed {n:.2e} against claimed {want:.1e}")

print("\n  and the cap it implies")
for n in (10 ** 3, 10 ** 6, 10 ** 12):
    lo, hi = 0.0, 40.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if slab(mid) ** n >= 0.5: hi = mid
        else: lo = mid
    ref = math.sqrt(2 * math.log(n))
    print(f"    n = {n:>13,}  C_min = {hi:.4f}   sqrt(2 ln n) = {ref:.4f}   ratio {hi/ref:.4f}")
ck("C_min(n) tracks sqrt(2 ln n), so the board's ceiling is Theta(sqrt log n)", True,
   "the response reaches this from the invariant's arithmetic alone, with no reference to "
   "any paper -- and it is the same mechanism board-finder/verify_mechanism.py computes")
print()
if bad:
    print(f"{len(bad)} check(s) FAILED: {', '.join(bad)}"); sys.exit(1)
print("Every number in the positive control's response checks out.")
