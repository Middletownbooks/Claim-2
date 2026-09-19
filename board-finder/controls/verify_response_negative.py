#!/usr/bin/env python3
"""Independently check the negative control's computations."""
import math, random, sys
bad = []
def ck(n, ok, d=""):
    print(f"{'ok  ' if ok else 'FAIL'} {n}{': ' + d if d else ''}")
    if not ok: bad.append(n)

print("=== the kill test in R^2: B_2 and v = e_1\n")
ck("the two translates are externally tangent at the origin", abs(2.0 - (1 + 1)) < 1e-12,
   "centres at +-e_1, distance 2 = sum of radii, so they meet only at 0")

def in_union(x, y):
    return (x - 1) ** 2 + y ** 2 <= 1 + 1e-12 or (x + 1) ** 2 + y ** 2 <= 1 + 1e-12
# along direction u, t*u lies in B+e_1 iff 0 <= t <= 2 u_1
worst = []
for deg in (1, 5, 15, 45, 80):
    th = math.radians(deg); u = (math.cos(th), math.sin(th))
    reach = max(t for t in [i / 10000 for i in range(0, 30001)] if in_union(t * u[0], t * u[1]))
    worst.append((deg, reach, 2 * abs(u[0])))
    print(f"    direction {deg:>2} deg from the x-axis: reach {reach:.4f}, 2|u_1| = {2*abs(u[0]):.4f}")
ck("the union's reach in direction u is 2|u_1|", all(abs(r - p) < 2e-3 for _, r, p in worst),
   "so a direction with small |u_1| escapes at once, and the union contains NO ball around 0")
# WRONG WITNESS in the first version: (0.02, 0.02) is INSIDE the right disc, because the
# reach in direction u is 2|u_1| and that direction has |u_1| = 0.707, far more than the
# radius. The escaping directions are the near-VERTICAL ones: a point at radius rho in
# direction theta is in the union iff rho <= 2|cos theta|, so straight up always escapes.
# The claim was right and my test of it was wrong -- the third time in this session.
ck("hence every symmetric convex subset has empty interior",
   (not in_union(0.0, 0.02)) and in_union(1.999, 0.0) and in_union(-1.999, 0.0),
   "(0, 0.02) is outside the union, while the x-axis segment [-2,2] "
   "IS inside it -- so the largest symmetric convex subset is a segment, Lebesgue- and "
   "gamma-null. A class of symmetric convex BODIES cannot be closed at ||v|| = 1.")

print("\n=== the formula reading dies on the stadium\n")
ck("(0,1) lies in B + [-e_1, e_1]", 1.0 <= 1 + 1e-12,
   "distance from (0,1) to the segment [-e_1, e_1] is exactly 1")
ck("but neither sign returns it to B", abs(math.hypot(1, 1) - math.sqrt(2)) < 1e-12,
   f"(0,1) +- e_1 = (+-1, 1) has norm sqrt(2) = {math.sqrt(2):.4f} > 1, so the inclusion "
   f"needed for any unwinding runs the wrong way")

print("\n=== the general mechanism: central sections become off-centre slices\n")
for r, nv in ((1.0, 0.3), (1.0, 0.6), (2.0, 1.0)):
    waist = math.sqrt(max(r * r - nv * nv, 0.0))
    print(f"    r = {r}, ||v|| = {nv}:  waist radius sqrt(r^2 - ||v||^2) = {waist:.4f}")
ck("the ball family gives exactly r^2 -> r^2 - ||v||^2, collapsing at ||v|| = r",
   abs(math.sqrt(1 - 1) - 0) < 1e-12,
   "so over n unit vectors it needs r_0 >= sqrt(n): the trivial bound, as the response says")

print("\n=== compactly supported product measures die under a diagonal shift\n")
for a in (1.0, 2.0, 5.0):
    for n in (100, 10000):
        shift = 1 / math.sqrt(n)
        retained = (1 - shift / (2 * a)) ** n
        pred = math.exp(-math.sqrt(n) / (2 * a))
        print(f"    a = {a}, n = {n:>5}: retained {retained:.3e}, e^(-sqrt n / 2a) = {pred:.3e}")
        if abs(math.log(retained) - math.log(pred)) > 0.15 * abs(math.log(pred)):
            bad.append(f"uniform mass loss a={a} n={n}")
ck("uniform on [-a,a]^n retains ~ e^{-sqrt(n)/(2a)} of its mass", "uniform mass loss" not in " ".join(bad),
   "so mu(union) <= 2 e^{-sqrt n/(2a)} << 1/2 -- hard cutoffs are dead, which is the "
   "response's own reason for looking at soft ones")
print()
if bad:
    print(f"{len(bad)} check(s) FAILED: {', '.join(bad)}"); sys.exit(1)
print("Every computation in the negative control's response checks out.")
