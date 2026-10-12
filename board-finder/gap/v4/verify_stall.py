#!/usr/bin/env python3
"""Re-derivation of the Zarankiewicz program's stall analysis.

The response document is RELAYED -- this session ran none of its searches. What
is checkable without them is the probability model and its instantiation, and
all of it is recomputed here from the stated measurements.
"""
from math import log, exp

FAIL = []
def ck(label, got, want, tol=0.0):
    ok = abs(got - want) <= tol if tol else got == want
    print(f"  [{'ok ' if ok else 'FAIL'}] {label}: {got!r} vs {want!r}")
    if not ok: FAIL.append(label)

print("1. Proposition 1's bound, and the claim that the two errors do not trade off")
def pr_success(eps, sigma, delta): return (1 - eps)*(1 - sigma) + eps*delta
# the floor as B -> infinity (sigma -> 0)
def pr_failure_floor(eps, delta): return 1 - pr_success(eps, 0.0, delta)
ck("floor = eps(1-delta), algebraically", round(pr_failure_floor(0.4, 0.3), 12),
   round(0.4*(1-0.3), 12))
print("      so no budget removes eps(1-delta); the proposition is sound as stated.")
print()

print("2. The program's measured instantiation")
hit = 568 / 46812
ck("hit rate at n=7, 568 of 46,812 (4dp)", round(hit, 4), 0.0121)
EPS = 2/3                      # three admissible readings, diffuse prior
d_lo, d_hi = 118/155, 120/155  # full witnesses / still-non-tight, of the 155
ck("delta from 118 of 155 (2dp)", round(d_lo, 2), 0.76)
print(f"      delta in [{d_lo:.3f}, {d_hi:.3f}] depending on whether 'witness' means")
print(f"      still-non-tight (120) or full witness (118); the document uses 118.")
floor = EPS * (1 - d_lo)
ck("eps(1-delta) (2dp)", round(floor, 2), 0.16)
print()

print("3. The crossover, recomputed -- and the document's figure is conservative")
def sigma(B): return (1 - hit) ** B
B_star = log(floor) / log(1 - hit)
print(f"      sigma(B) = (1-{hit:.6f})^B crosses {floor:.4f} at B = {B_star:.1f}")
ck("crossover is ~151 samples, not ~400", round(B_star), 151)
rate = 12800 / 100   # 155 hits at a 1.21% rate in ~100 s => ~128 samples/s
print(f"      at ~{rate:.0f} samples/s (155 hits at this rate in ~100 s):")
print(f"        B = {B_star:.0f} is {B_star/rate:.1f} s;  B = 400 is {400/rate:.1f} s")
print("      The document says '~400 samples, roughly 4 seconds'. The true")
print("      crossover is EARLIER, so the error runs AGAINST its own thesis --")
print("      compute stopped binding sooner than it claimed. Self-penalising.")
print()

print("4. The sigma figures it quotes")
ck("sigma(500) ~ 2e-3, as the document states", round(sigma(500), 3), 0.002)
s2000 = sigma(2000)
print(f"      sigma(2000) = {s2000:.2e}; the document says 4e-11")
ck("sigma(2000) is ~2.6e-11, not 4e-11 (order of magnitude agrees)",
   round(log(s2000)/log(10)), -11)
print("      A 1.5x discrepancy at 1e-11. Immaterial to every conclusion drawn,")
print("      and recorded only because the figure is quoted.")
print()

print("5. Proposition 2's instantiation: the control that could not discriminate")
controls = {"path": 14, "walk": 13, "both": 14}
ck("every reading passes Woodall's >= 10 control", 
   {k: (v >= 10) for k, v in controls.items()}, {"path": True, "walk": True, "both": True})
print("      The only validation Session 2 had, and it is blind to the error:")
print("      it bounds over-permissiveness; the error was over-strictness.")
print()

print("6. The certified generator's discriminating power")
gen = {"path": (245, 247), "walk": (250, 250), "both": (245, 247)}
winners = [k for k, (t, p) in gen.items() if t == 250 and p == 250]
ck("exactly one reading survives the generator", winners, ["walk"])
print("      250/250 against 245/250 and 247/250 -- |C| collapses from 3 to 1.")
print()

print("7. A textual argument for 'walk', which the document lists as its first falsifier")
print("      Its own falsifier: 'If the walk reading is itself wrong -- if Woodall's")
print("      text settles the convention against it -- then eps was never reduced.'")
print("      From the full paper, now read at PRIMARY tier:")
print("      (a) Woodall NEVER DEFINES 'path' anywhere in pp.657-671.")
print("      (b) A shortest walk in an unweighted graph is always a path: a repeated")
print("          vertex admits excision of a closed section, giving a shorter walk.")
print("          So for P_ab, which tightness REQUIRES to be shortest, the two")
print("          readings COINCIDE and the convention cannot bite.")
print("      (c) It bites only on Q_xy, which p.662 explicitly says is")
print("          'NOT NECESSARILY SHORTEST' -- the one object in the definition")
print("          where walks and paths can differ.")
print("      (d) Theorem 5's own proof (p.662) CONSTRUCTS an antipath as the")
print("          sequence a, a_1, ..., a_r reached by iteratively opening crossings,")
print("          one adjacent transposition at a time, with nothing excluding a")
print("          repeated vertex -- and calls the result 'the required path'.")
print("      => the text does not settle the convention against 'walk', and")
print("         Theorem 5's construction is positive evidence FOR it.")
print()

print("=" * 72)
if FAIL:
    print(f"{len(FAIL)} FAILED: {FAIL}"); raise SystemExit(1)
print("The probability model and every instantiated figure re-derive.")
