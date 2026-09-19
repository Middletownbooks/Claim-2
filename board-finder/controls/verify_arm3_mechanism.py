#!/usr/bin/env python3
"""Independent check of the two computations arm 3's board turns on.

Written BEFORE the arm-3 respondent's answer is read, so that the arithmetic I
score it against is not arithmetic I learned from it. Both earlier control arms
were verified this way, and in both cases the verifier -- not the respondent --
was what turned out to be wrong.

The arm-3 pair is: same problem, same target, SAME MOVE, only the invariant
changed.

  invariant A (the incumbent): the Gaussian measure of the body stays >= 1/2.
  invariant B (the carried one): the directional total variation of a density.

T3 asks for min{C : the invariant holds for the target at scale C}. The claim
under test is that T3 answers differently across the pair:

  A caps the bound at Theta(sqrt(log d))   -- a threshold that grows with d
  B does not cap it at all                 -- the quantity is dimension-free

Everything below is exact or Monte-Carlo-checked against an exact value. No
result here depends on any respondent's text.
"""
import math, random

SQRT2 = math.sqrt(2.0)


# ---------------------------------------------------------------- invariant A
def gauss_cube_measure(C: float, d: int) -> float:
    """gamma_d([-C, C]^d) for the standard Gaussian. Multiplicative in d:
    the measure of a product body is the product of the 1-D measures, which is
    the whole mechanism -- each coordinate charges the bound again."""
    return math.erf(C / SQRT2) ** d


def threshold_A(d: int) -> float:
    """min{C : gamma_d([-C,C]^d) >= 1/2}, by bisection on the exact formula."""
    lo, hi = 1e-9, 60.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if d * math.log(math.erf(mid / SQRT2)) >= math.log(0.5):
            hi = mid
        else:
            lo = mid
    return hi


def check_A():
    print("invariant A -- Gaussian measure of the target cube")
    print("  d           min C     C / sqrt(2 ln d)")
    ds = [2, 10, 100, 1000, 10 ** 4, 10 ** 6, 10 ** 9]
    ratios = {}
    for d in ds:
        C = threshold_A(d)
        r = C / math.sqrt(2 * math.log(d))
        ratios[d] = r
        print(f"  {d:<11} {C:8.5f}  {r:.5f}")
        # the threshold really is the threshold
        assert gauss_cube_measure(C, d) >= 0.5 - 1e-9
        assert gauss_cube_measure(C * (1 - 1e-6), d) < 0.5
    # the asymptotic, and the DIRECTION of approach. An earlier version of this
    # programme asserted the ratio falls to 1 from above; it rises to 1 from
    # below, and is below 1 throughout.
    assert all(r < 1 for r in ratios.values()), ratios
    tail = [ratios[d] for d in ds if d >= 10]
    assert all(b > a for a, b in zip(tail, tail[1:])), tail
    print("  -> min C ~ sqrt(2 ln d), approached from BELOW and increasing "
          "(d >= 10); unbounded in d.")
    print("  -> T3 on invariant A: CAP at Theta(sqrt(log d)). No improvement to "
          "the move reaches O(1).\n")
    return ratios


# ---------------------------------------------------------------- invariant B
def tv_directional_exact(d: int, u) -> float:
    """For the standard Gaussian density f on R^d, the directional total
    variation in direction u is

        int |<u, grad f>| dx = int |<u, x>| f(x) dx = E|<u, X>| = sqrt(2/pi)*|u|

    because grad f = -x f. With |u| = 1 this is sqrt(2/pi) in EVERY dimension:
    the functional is an AVERAGE over the direction, not a product over
    coordinates, so d never enters. That is the whole contrast with A."""
    nrm = math.sqrt(sum(x * x for x in u))
    return math.sqrt(2.0 / math.pi) * nrm


def tv_directional_mc(d: int, u, n=400000, seed=0) -> float:
    """Monte Carlo on E|<u, X>|, to check the exact value is the right one and
    not an algebra slip."""
    rng = random.Random(seed)
    g = rng.gauss
    tot = 0.0
    for _ in range(n):
        tot += abs(sum(ui * g(0.0, 1.0) for ui in u))
    return tot / n


def check_B():
    print("invariant B -- directional total variation of the carried density")
    target = math.sqrt(2.0 / math.pi)
    print(f"  exact value, any d, any unit u: sqrt(2/pi) = {target:.6f}")
    rng = random.Random(7)
    for d in (1, 2, 10, 100, 1000):
        u = [rng.gauss(0, 1) for _ in range(d)]
        nrm = math.sqrt(sum(x * x for x in u))
        u = [x / nrm for x in u]
        ex = tv_directional_exact(d, u)
        mc = tv_directional_mc(d, u, n=60000, seed=d)
        print(f"  d={d:<5} exact {ex:.6f}   MC {mc:.6f}   "
              f"rel err {abs(mc-ex)/ex:.2%}")
        assert abs(ex - target) < 1e-12
        assert abs(mc - ex) / ex < 0.02, (d, mc, ex)
    print("  -> the value is DIMENSION-FREE: bounded uniformly in d. Note the")
    print("     claim is 'bounded uniformly', not 'flat' -- for a general")
    print("     carried density it varies with d, it just does not grow.")
    print("  -> T3 on invariant B: NO CAP. min{C : B holds at scale C} is O(1),")
    print("     so whatever bound the proof reaches is the move's doing.\n")
    return target


def check_contrast(ratios, target):
    """The pair discriminates only if the two answers differ by an unbounded
    factor, not by a constant. Show the gap grows."""
    print("the pair")
    print("  d           A's threshold   B's value   ratio A/B")
    for d in (10, 1000, 10 ** 6, 10 ** 9):
        a = threshold_A(d)
        print(f"  {d:<11} {a:13.5f} {target:11.6f} {a/target:10.3f}")
    a1, a2 = threshold_A(10), threshold_A(10 ** 9)
    assert a2 / a1 > 3.0, (a1, a2)
    print("  -> the gap is unbounded in d, so the pair separates by more than a")
    print("     constant. A and B are the SAME problem, the SAME target and the")
    print("     SAME move; only the invariant differs. Any screen that reports")
    print("     the same thing on both is not reading the invariant.\n")


if __name__ == "__main__":
    ratios = check_A()
    target = check_B()
    check_contrast(ratios, target)
    print("All assertions passed. This file fixes the arithmetic BEFORE the "
          "arm-3 answer is read;\nif the respondent and this file disagree, "
          "the disagreement is resolved by computation,\nnot by which came "
          "first -- four of this programme's verifier predicates were the "
          "thing\nthat was wrong.")
