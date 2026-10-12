#!/usr/bin/env python3
"""Symmetric ideal-PTE search with the sign pattern forced by Corollary 21.

WHAT CHANGED. search_symmetric.py enumerated 11-element subsets of [-H, H] with vanishing
odd power sums. It used nothing about which elements could be negative. Cancado-Coutinho-Spier
(arXiv:2509.09948) restate Caley's interlacing theorem as Corollary 21: in the sorted union
E u F of an ideal solution, the sides alternate in blocks 1,2,2,...,2,1 -- equivalently the
element at sorted position k belongs to E iff k mod 4 is 0 or 1.

For a SWAPPING-symmetric solution the union is C u (-C), so the rule fixes, for each of the n
absolute values in increasing order, whether it sits in C or in -C:

    s_i = +1 if (n + i) mod 4 in {0, 1} else -1,        C = { s_i * u_i }.

Verified against every ideal solution this project can produce (n = 4, 5, 6, 7): 17 of 17, and
the pattern reconstructs C exactly. So the search is no longer over subsets of [-H, H] with free
signs; it is over strictly increasing u_1 < ... < u_n in [1, H] with the signs handed to us.

At H = 36 and n = 11 that takes the right-hand side of the meet in the middle from C(73,6) =
170,230,452 to C(36,6) = 1,947,792.

SCOPE, narrower than search_symmetric.py in one way. The derivation assumes C and -C are
disjoint -- no c with -c also in C, and 0 not in C -- because a shared element is a repeat in
E u F. That is exactly PTE^0, which is the variant Theorem 18 needs for odd d. Solutions with a
repeat (PTE^1, PTE) are NOT covered here and remain search_symmetric.py's business.
"""
import argparse, json, math, os, sys, time
from collections import defaultdict
from itertools import combinations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verify


def signs(n):
    return [1 if (n + i) % 4 in (0, 1) else -1 for i in range(1, n + 1)]


def odd_ks(n):
    return [k for k in range(1, n - 1) if k % 2 == 1]


def search(n, H, n1=None, cap=None):
    s = signs(n)
    ks = odd_ks(n)
    n1 = n1 or n // 2
    n2 = n - n1
    t0 = time.time()

    # left half: u_1 < ... < u_{n1}, signs s[0:n1]
    left = defaultdict(list)
    for U in combinations(range(1, H + 1), n1):
        key = tuple(sum(si * ui ** k for si, ui in zip(s, U)) for k in ks)
        left[key].append(U)

    hits, seen, enumerated = [], set(), 0
    for V in combinations(range(1, H + 1), n2):
        enumerated += 1
        key = tuple(-sum(si * vi ** k for si, vi in zip(s[n1:], V)) for k in ks)
        bucket = left.get(key)
        if not bucket:
            continue
        for U in bucket:
            if U[-1] >= V[0]:                        # the u_i must be strictly increasing
                continue
            C = [si * ui for si, ui in zip(s, U + V)]
            A, B = verify.from_centre(C)
            ok, why = verify.is_ideal(A, B)
            if not ok:                               # the reduction is never trusted, the object is
                raise AssertionError(f"pattern search produced a non-solution from {C}: {why}")
            k2 = verify.normalise(A, B)
            if k2 in seen:
                continue
            seen.add(k2)
            hits.append({"centre": sorted(C), "A": list(k2[0]), "B": list(k2[1]), "why": why})
            if cap and len(hits) >= cap:
                break
        if cap and len(hits) >= cap:
            break

    expected = math.comb(H, n2)
    complete = cap is None or len(hits) < cap
    if complete:
        assert enumerated == expected, f"enumerated {enumerated}, expected {expected}"
    return {"n": n, "H": H, "split": [n1, n2], "equations": ks, "signs": s,
            "left_table_keys": len(left), "right_enumerated": enumerated,
            "right_expected": expected, "exhaustive": complete, "solutions": hits,
            "seconds": round(time.time() - t0, 1),
            "variant": "PTE^0 symmetric (C and -C disjoint)"}


def controls():
    """It must find the objects that are known to be there, at odd n, before a null means anything."""
    out = []
    r5 = search(5, 12)
    got = {tuple(h["A"]) for h in r5["solutions"]}
    assert (0, 4, 8, 16, 17) in got, f"n=5 control failed: {sorted(got)}"
    out.append(f"n=5  H=12 exhaustive: {len(r5['solutions'])} solution(s) incl. [0,4,8,16,17] "
               f"({r5['seconds']}s, {r5['right_enumerated']:,} right tuples)")
    r7 = search(7, 60)
    got = {tuple(h["A"]) for h in r7["solutions"]}
    assert (0, 18, 27, 58, 64, 89, 101) in got, f"n=7 control failed: {sorted(got)}"
    out.append(f"n=7  H=60 exhaustive: {len(r7['solutions'])} solution(s) incl. the classic "
               f"[0,18,27,58,64,89,101] ({r7['seconds']}s, {r7['right_enumerated']:,} right tuples)")
    return out, [r5, r7]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=11)
    ap.add_argument("--H", type=int)
    ap.add_argument("--split", type=int)
    ap.add_argument("--cap", type=int)
    ap.add_argument("--out")
    ap.add_argument("--controls", action="store_true")
    a = ap.parse_args()
    if a.controls:
        print("search_pattern.py controls:")
        lines, runs = controls()
        for line in lines:
            print("  ok   " + line)
        print("\nControls passed.")
        sys.exit(0)
    if not a.H:
        ap.error("--H is required unless --controls")
    r = search(a.n, a.H, a.split, a.cap)
    print(json.dumps({k: v for k, v in r.items() if k != "solutions"}, indent=1))
    for h in r["solutions"]:
        print("  ", h["A"], "/", h["B"])
    if a.out:
        json.dump(r, open(a.out, "w"), indent=1)
        print(f"wrote {a.out}")
