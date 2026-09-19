"""Rank 429: check that both routes to a lower bound on l(n) cap at exactly 2/3.

l(n) = longest path guaranteed in an n-vertex connected vertex-transitive graph.
Bucic-Christoph-Pokrovskiy-Steiner (arXiv:2606.09742v2) prove l(n) >= n^{2/3-o(1)}
and state this is a natural barrier of the existing methods. This file checks that
claim arithmetically, in both directions.

Route A (longest path transversals): lpt(G) <= l^beta with l >= n/lpt - 1 gives
    l^{1+beta} >~ n, so the exponent is 1/(1+beta).
Route B (Smith's conjecture, local form): s(k) = O(k^alpha) gives exponent
    (1+alpha)/(1+2alpha), and the trivial s(k) >= k forces alpha >= 1.
"""

from fractions import Fraction as F


def route_a(beta):
    """Exponent obtainable from a transversal bound lpt <= l^beta."""
    return F(1, 1) / (1 + beta)


def route_b(alpha):
    """Exponent obtainable from a local Smith bound s(k) = O(k^alpha)."""
    return (1 + alpha) / (1 + 2 * alpha)


CHECKS = []


def check(name, got, want):
    CHECKS.append((name, got == want, got, want))


# --- Route A ------------------------------------------------------------
# This paper's Theorem 1.2 achieves beta = 1/2.
check("A: beta=1/2 (this paper) gives 2/3", route_a(F(1, 2)), F(2, 3))
# The exponent improves only as beta -> 0, and beta = 0 is Gallai's 1966 question.
check("A: beta=0 (Gallai) would give 1, the full conjecture", route_a(F(0)), F(1))
# Monotone decreasing in beta: no weaker transversal bound does better.
check("A: monotone decreasing in beta",
      all(route_a(F(i, 8)) > route_a(F(i + 1, 8)) for i in range(0, 16)), True)
# Earlier links in the chain, for the record.
for name, e in [("Babai", F(1, 2)), ("DeVos", F(3, 5)),
                ("Groenland et al", F(13, 21)), ("Norin et al", F(9, 14))]:
    check(f"chain: {name} = {e} < 2/3", e < F(2, 3), True)

# --- Route B ------------------------------------------------------------
# Decreasing in alpha, so one wants alpha small...
check("B: decreasing in alpha",
      all(route_b(F(i, 4)) > route_b(F(i + 1, 4)) for i in range(4, 12)), True)
# ...but s(k) >= k forces alpha >= 1, and alpha = 1 is the best conceivable case.
check("B: alpha=1 (best possible) gives 2/3", route_b(F(1)), F(2, 3))
# Ma-Zhao's current alpha = 3/2 is worse than route A already delivers.
check("B: alpha=3/2 (Ma-Zhao) gives 5/8", route_b(F(3, 2)), F(5, 8))
check("B: alpha=3/2 is worse than route A's 2/3", route_b(F(3, 2)) < F(2, 3), True)

# --- The barrier --------------------------------------------------------
# Two independent routes, both capped at exactly 2/3 -- one by a 1966 open
# problem, the other by a trivial inequality.
check("both routes cap at the same exponent",
      route_a(F(1, 2)) == route_b(F(1)) == F(2, 3), True)


if __name__ == "__main__":
    ok = 0
    for name, passed, got, want in CHECKS:
        print(f"[{'PASS' if passed else 'FAIL'}] {name}   (got {got}, want {want})")
        ok += passed
    print(f"\n{ok}/{len(CHECKS)} checks pass")
    raise SystemExit(0 if ok == len(CHECKS) else 1)
