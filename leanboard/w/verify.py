"""Phase W scoring harness.

An agent's return will contain identities of the form "for n in residue class
C, take x = f(n), y = g(n), z = h(n)". This verifies such a family exactly,
over a range, using Fraction arithmetic - no floating point, no trusting the
algebra as written.

Usage: register a family with check_family(name, cond, xyz, lo, hi) and it
reports (i) how many n in range satisfy cond, (ii) how many the formulas solve,
(iii) the first failure with its reason.
"""
from fractions import Fraction as F


def check_family(name, cond, xyz, lo=2, hi=20000):
    seen = solved = 0
    first_fail = None
    for n in range(lo, hi + 1):
        if not cond(n):
            continue
        seen += 1
        try:
            t = xyz(n)
        except Exception as e:                       # noqa: BLE001
            if first_fail is None:
                first_fail = (n, "formula raised %r" % (e,))
            continue
        if len(t) != 3:
            if first_fail is None:
                first_fail = (n, "not a triple")
            continue
        bad = None
        for v in t:
            if not isinstance(v, int):
                bad = "non-integer value %r" % (v,)
            elif v <= 0:
                bad = "non-positive value %r" % (v,)
        if bad:
            if first_fail is None:
                first_fail = (n, bad)
            continue
        lhs = F(4, n)
        rhs = sum((F(1, v) for v in t), F(0))
        if lhs != rhs:
            if first_fail is None:
                first_fail = (n, "%s != 4/%d, got %s" % (rhs, n, rhs))
            continue
        solved += 1
    ok = (seen > 0 and solved == seen)
    print("%-28s class size %6d  solved %6d  %s" %
          (name, seen, solved, "OK" if ok else "FAIL %r" % (first_fail,)))
    return ok, seen, solved, first_fail


def coverage(conds, lo=2, hi=20000, restrict=None):
    """Report which n in range are covered by no registered condition."""
    missed = []
    for n in range(lo, hi + 1):
        if restrict and not restrict(n):
            continue
        if not any(c(n) for c in conds):
            missed.append(n)
    return missed


def isprime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


if __name__ == "__main__":
    # Self-test on a family that is certainly correct:
    # n = 2m even  =>  4/n = 2/m = 1/m + 1/(m+1) + 1/(m(m+1)).
    check_family("even n", lambda n: n % 2 == 0,
                 lambda n: (n // 2, n // 2 + 1, (n // 2) * (n // 2 + 1)))
    # And on one that is wrong, to confirm the harness catches it.
    check_family("bogus (should FAIL)", lambda n: n % 2 == 0,
                 lambda n: (n // 2, n // 2 + 1, n // 2 + 2))
