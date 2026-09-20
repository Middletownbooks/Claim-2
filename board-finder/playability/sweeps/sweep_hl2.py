#!/usr/bin/env python3
"""Second Hardy-Littlewood conjecture -- a real witness sweep, rank 488, class P2.

    pi(x+y) <= pi(x) + pi(y)   for all integers x, y >= 2.

A counterexample is one pair (x,y): finite, and the check is a prime count.
Equivalently, the conjecture fails iff some interval (x, x+y] holds strictly
more primes than [1, y] does. So for each window length y we want

    W(y) = max over x >= 2 of  ( pi(x+y) - pi(x) )

and the conjecture survives at length y exactly when W(y) <= pi(y).

CAUTION, learned the hard way. Taking the max over ALL x >= 2 is vacuous: the
boundary window (2, 2+y] holds pi(y+2)-1 primes, so it ties pi(y) for most y
and dominates the max. A first run of this script reported 859 "near misses"
in y <= 3000 and every one of them sat at x = 2. The informative quantity is
the max over windows FAR from the origin,

    W_far(y) = max over x >= X0 of ( pi(x+y) - pi(x) ),   X0 >> 0

whose margin  D_far(y) = pi(y) - W_far(y)  measures how close a prime-rich
window out in the wild gets to the initial segment. That is the trend that
says whether a search at reachable scales could ever succeed.

This is PROMPT_WITNESS.md steps 4 and 5 run on a live item rather than recalled.

Usage:  python3 sweep_hl2.py [N] [YMAX] [X0]   default N=2*10^7, YMAX=3000, X0=10^6
"""
import sys, time, json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

def sieve(n):
    """Boolean array, is_prime[0..n]."""
    s = np.ones(n + 1, dtype=bool)
    s[:2] = False
    for p in range(2, int(n**0.5) + 1):
        if s[p]:
            s[p*p::p] = False
    return s

def main():
    N    = int(sys.argv[1]) if len(sys.argv) > 1 else 20_000_000
    YMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
    X0   = int(sys.argv[3]) if len(sys.argv) > 3 else 1_000_000

    t0 = time.time()
    is_p = sieve(N)
    # P[n] = pi(n) = number of primes <= n
    P = np.cumsum(is_p, dtype=np.int32)
    t_sieve = time.time() - t0
    print(f'sieved to N = {N:,}   pi(N) = {int(P[N]):,}   [{t_sieve:.1f}s]')
    print(f'window lengths y = 2 .. {YMAX:,}')
    print(f'windows restricted to x >= X0 = {X0:,} (the boundary window at x=2 is')
    print(f'excluded: it ties pi(y) automatically and tells you nothing)\n')

    rows = []
    ties = []
    counterexamples = []
    t0 = time.time()
    for y in range(2, YMAX + 1):
        # counts in (x, x+y] for x = X0 .. N-y -- boundary window excluded
        d = P[X0+y:] - P[X0:N-y+1]
        W = int(d.max())
        xstar = int(d.argmax()) + X0
        piy = int(P[y])
        D = piy - W
        rows.append((y, piy, W, D, xstar))
        if D < 0:
            counterexamples.append((y, piy, W, xstar))
        elif D == 0:
            ties.append((y, piy, W, xstar))
    t_scan = time.time() - t0
    print(f'scanned {YMAX-1:,} window lengths [{t_scan:.1f}s]\n')

    # ---- results ---------------------------------------------------------
    print('=' * 62)
    if counterexamples:
        print('COUNTEREXAMPLES FOUND:')
        for y, piy, W, x in counterexamples[:20]:
            print(f'  y={y}  pi(y)={piy}  max window count={W}  at x={x}')
    else:
        print('NO COUNTEREXAMPLE in this range. The conjecture survives.')
    print('=' * 62)
    print(f'\nties (W_far(y) == pi(y), the real near-miss frontier): {len(ties)}')
    for y, piy, W, x in ties[:12]:
        print(f'  y={y:5d}  pi(y)={piy:4d}  window (x,x+y] at x={x:,} holds {W}')
    if len(ties) > 12:
        print(f'  ... and {len(ties)-12} more')

    # margin trend -- the feasibility signal
    print('\nmargin D_far(y) = pi(y) - W_far(y), sampled:')
    print(f"  {'y':>6} {'pi(y)':>7} {'W(y)':>7} {'D(y)':>6}")
    for y in [10, 50, 100, 250, 500, 1000, 1500, 2000, 2500, 3000]:
        if 2 <= y <= YMAX:
            _, piy, W, D, _ = rows[y - 2]
            print(f'  {y:6d} {piy:7d} {W:7d} {D:6d}')
    mins = min(r[3] for r in rows)
    argmin = [r[0] for r in rows if r[3] == mins]
    print(f'\nsmallest margin over the whole range: D = {mins}, first at y = {argmin[0]}')
    # is the margin growing?
    half = len(rows) // 2
    print(f'  mean D over first half of range:  {np.mean([r[3] for r in rows[:half]]):.2f}')
    print(f'  mean D over second half of range: {np.mean([r[3] for r in rows[half:]]):.2f}')

    out = dict(
        problem='Second Hardy-Littlewood conjecture', releaseRank=488, cls='P2',
        statement='pi(x+y) <= pi(x) + pi(y) for all integers x,y >= 2',
        sweepBound_N=N, maxWindowLength_YMAX=YMAX, windowFloor_X0=X0, piN=int(P[N]),
        counterexamples=counterexamples, tieCount=len(ties), ties=ties[:50],
        minMargin=int(mins), minMarginFirstAt=int(argmin[0]),
        sieveSeconds=round(t_sieve, 1), scanSeconds=round(t_scan, 1),
        margins={str(r[0]): r[3] for r in rows},
    )
    p = os.path.join(HERE, 'hl2_result.json')
    json.dump(out, open(p, 'w'), indent=1)
    print(f'\nwrote {p}')

if __name__ == '__main__':
    main()
