"""S2 grading: given the covering families an agent actually produced, verify
each one exactly and report which primes remain uncovered, by residue mod 840.

The agent's stated gap is graded against THIS output, not against any
answer key held in advance.
"""
from verify import check_family, coverage, isprime

M = 840


def grade(families, lo=2, hi=20000):
    conds = []
    for name, cond, xyz in families:
        ok, seen, solved, fail = check_family(name, cond, xyz, lo, hi)
        if ok:
            conds.append(cond)
        else:
            print("   -> family rejected, not counted toward coverage")
    missed = coverage(conds, lo, hi, restrict=isprime)
    res = sorted({n % M for n in missed})
    print("\nprimes in [%d, %d] not covered by the accepted families: %d"
          % (lo, hi, len(missed)))
    print("residues mod %d they occupy (%d classes): %s" % (M, len(res), res))
    return missed, res


if __name__ == "__main__":
    # End-to-end self-test with two families derived here, not recalled.
    #   n even, n = 2m:  4/n = 2/m = 1/m + 1/(m+1) + 1/(m(m+1))
    #   n = 4k+3:        4/n - 1/(k+1) = 1/(n(k+1)), then split 1/A into
    #                    1/(A+1) + 1/(A(A+1)) to reach three terms.
    def odd3(n):
        k = (n - 3) // 4
        A = n * (k + 1)
        return (k + 1, A + 1, A * (A + 1))

    grade([
        ("even n", lambda n: n % 2 == 0,
         lambda n: (n // 2, n // 2 + 1, (n // 2) * (n // 2 + 1))),
        ("n = 3 mod 4", lambda n: n % 4 == 3, odd3),
    ], 2, 20000)
