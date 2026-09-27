#!/usr/bin/env python3
"""Exhaustive search for SWAPPING-symmetric ideal PTE solutions at odd size n.

The reduction (PREREG_PTE11.md sec 3). A swapping-symmetric solution has B = t - A. Centre at
t/2 and double: C = 2A - t is an n-element integer set with -C the centred-doubled form of B,
and the ideal conditions k = 1..n-1 collapse to

    p_k(C) = 0   for every ODD k <= n-2,

because the even k hold identically once B = -A in centred coordinates. For n = 11 that is five
equations, p_1 = p_3 = p_5 = p_7 = p_9 = 0, in eleven unknowns.

C = -C must be excluded: it makes B = A, which is not a solution.

Meet in the middle on the (n-1)/2 odd power sums. Nothing is reported on the strength of that
reduction: every hit is turned back into an explicit (A, B) and checked against all n-1 power
sums by verify.is_ideal.
"""
import argparse, json, math, os, sys, time
from collections import defaultdict
from itertools import combinations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verify


def odd_ks(n):
    return [k for k in range(1, n - 1) if k % 2 == 1]


def search(n, H, n1=None, cap=None, progress=None):
    ks = odd_ks(n)
    n1 = n1 or n // 2
    n2 = n - n1
    dom = range(-H, H + 1)
    t0 = time.time()

    left = defaultdict(list)
    for S in combinations(dom, n1):
        left[tuple(sum(x ** k for x in S) for k in ks)].append(S)
    t_left = time.time() - t0

    hits, seen, enumerated = [], set(), 0
    for T in combinations(dom, n2):
        enumerated += 1
        if progress and enumerated % progress == 0:
            print(f"    ... {enumerated:,} right tuples, {len(hits)} kept", flush=True)
        key = tuple(-sum(x ** k for x in T) for k in ks)
        bucket = left.get(key)
        if not bucket:
            continue
        for S in bucket:
            if S[-1] >= T[0]:                       # keep the union strictly increasing
                continue
            C = S + T
            if sorted(C) == sorted(-x for x in C):  # C = -C makes B = A
                continue
            A, B = verify.from_centre(C)
            ok, why = verify.is_ideal(A, B)
            if not ok:                              # the reduction is not trusted; the object is
                raise AssertionError(f"reduction produced a non-solution from {C}: {why}")
            key2 = verify.normalise(A, B)
            if key2 in seen:
                continue
            seen.add(key2)
            hits.append({"centre": list(C), "A": list(key2[0]), "B": list(key2[1]), "why": why})
            if cap and len(hits) >= cap:
                break
        if cap and len(hits) >= cap:
            break

    expected = math.comb(2 * H + 1, n2)
    complete = cap is None or len(hits) < cap
    if complete:
        assert enumerated == expected, f"enumerated {enumerated}, expected {expected}"
    return {"n": n, "H": H, "split": [n1, n2], "equations": ks,
            "left_table_keys": len(left), "right_enumerated": enumerated,
            "right_expected": expected, "exhaustive": complete,
            "solutions": hits, "seconds": round(time.time() - t0, 1),
            "seconds_building_left": round(t_left, 1)}


def controls():
    """The machinery must find objects that are known to be there before a null means anything."""
    out = []
    r5 = search(5, 12)
    got5 = {tuple(s["A"]) for s in r5["solutions"]}
    assert (0, 4, 8, 16, 17) in got5, f"n=5 control failed: {sorted(got5)}"
    out.append(f"n=5 H=12 exhaustive: {len(r5['solutions'])} solution(s), including the known "
               f"[0,4,8,16,17]/[1,2,10,14,18}}".replace("}", "]") + f" ({r5['seconds']}s)")
    r7 = search(7, 60)
    got7 = {tuple(s["A"]) for s in r7["solutions"]}
    assert (0, 18, 27, 58, 64, 89, 101) in got7, f"n=7 control failed: {sorted(got7)}"
    out.append(f"n=7 H=60 exhaustive: {len(r7['solutions'])} solution(s), including the classic "
               f"[0,18,27,58,64,89,101] ({r7['seconds']}s)")
    return out, [r5, r7]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=11)
    ap.add_argument("--H", type=int)
    ap.add_argument("--split", type=int, help="size of the left half")
    ap.add_argument("--cap", type=int)
    ap.add_argument("--progress", type=int)
    ap.add_argument("--out")
    ap.add_argument("--controls", action="store_true")
    a = ap.parse_args()

    if a.controls:
        print("search_symmetric.py controls:")
        lines, runs = controls()
        for line in lines:
            print("  ok   " + line)
        print("\nControls passed: the search finds known ideal solutions at n=5 and n=7.")
        if a.out:
            json.dump(runs, open(a.out, "w"), indent=1)
        sys.exit(0)

    if not a.H:
        ap.error("--H is required unless --controls")
    r = search(a.n, a.H, a.split, a.cap, a.progress)
    print(json.dumps({k: v for k, v in r.items() if k != "solutions"}, indent=1))
    print(f"solutions: {len(r['solutions'])}")
    for s in r["solutions"]:
        print("  ", s["A"], "/", s["B"])
    if a.out:
        json.dump(r, open(a.out, "w"), indent=1)
        print(f"\nwrote {a.out}")
