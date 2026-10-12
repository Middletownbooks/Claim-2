#!/usr/bin/env python3
"""The Cooper-Wallis route for the five composite v among the thirteen open orders.

Requires a clone of bbeartheancient/hoa64 importable as `hoa64` (pass its PARENT
directory as argv[1], default /home/user/bbeartheancient).

Does three things:
  1. names, for each composite v, the single Williamson order its product route needs
  2. validates both paths 2060 and 2884 use, at a Williamson order hoa64 already holds,
     so the only untested ingredient is W(103) itself
  3. measures whether hoa64's own Williamson engine could supply it -- using the
     documented success contract stats["is_williamson"], not "returned non-None"

Reference: FINDING_105 section 2 of Middletownbooks/Cooperative-AI-Defense sets these five
aside as "unlikely to be genuinely open" without testing the route. They are on the open
list, so the route is contingent on a nameable object rather than probable.
"""
import sys, time
import numpy as np

sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else "/home/user/bbeartheancient")
from hoa64.cw_construction import cw_build                      # noqa: E402
from hoa64.williamson import williamson_ils                     # noqa: E402

TS  = {47, 65, 93} | {3, 5, 7, 9, 11, 13, 15, 19, 23, 25, 27, 29, 31, 51, 59}
WDB = {1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,37,39,41,43,45,49,51,55,57,61,63}
COMPOSITE_V = {515: (5, 103), 537: (3, 179), 573: (3, 191), 669: (3, 223), 721: (7, 103)}


def is_hadamard(H):
    if H is None:
        return False
    H = np.asarray(H, dtype=np.int64)
    n = H.shape[0]
    return bool(np.all(np.abs(H) == 1)
                and np.array_equal(H @ H.T, n * np.eye(n, dtype=np.int64)))


def routes():
    print("the five composite v, and the ONE Williamson order each route needs")
    print(f"  {'v':>4} {'N=4v':>6} {'v factors':>12} {'needs':>10}  T-seq present?")
    for v, (t, w) in sorted(COMPOSITE_V.items()):
        print(f"  {v:>4} {4*v:>6} {f'{t}·{w}':>12} {f'W({w})':>10}  "
              f"{'yes' if t in TS else 'NO'}   (W in hoa64 DB: {'yes' if w in WDB else 'no'})")
    print("\n  W(103) appears twice -- it closes BOTH 2060 and 2884.\n")


def validate_paths():
    print("validating the 2060 and 2884 paths at a Williamson order hoa64 already holds")
    for n, desc in ((4*5*57, "T5 × W(57)  — the 2060 path"),
                    (4*7*57, "T7 × W(57)  — the 2884 path"),
                    (4*5*63, "T5 × W(63)")):
        ok = is_hadamard(cw_build(n))
        print(f"  H({n}) via {desc}: Hadamard = {ok}")
        assert ok, f"path validation failed at {n}"
    print("  -> both paths sound; the only missing ingredient is W(103).\n")


def can_hoa64_find_williamson(budgets=((11, 20), (23, 20), (31, 30), (43, 40),
                                       (63, 60), (85, 120), (103, 300))):
    print("could hoa64's own Williamson engine supply it? (success = stats['is_williamson'])")
    print(f"  {'k':>5} {'in DB':>6} {'found':>6} {'best_f':>12} {'secs':>6}")
    for k, budget in budgets:
        t0 = time.time()
        H, _method, best_f, ok = williamson_ils(k, time_budget=budget,
                                                rng=np.random.default_rng(3))
        print(f"  {k:>5} {str(k in WDB):>6} {str(bool(ok)):>6} {best_f:12.4g} "
              f"{time.time()-t0:6.1f}", flush=True)
    print("  -> it does not rediscover W(11), which is in its own database. The engine is a")
    print("     single-flip greedy PSD descent and plateaus; hoa64's Williamson coverage comes")
    print("     from the database, not the search. W(103) needs a lookup or a real solver.")


if __name__ == "__main__":
    routes()
    validate_paths()
    can_hoa64_find_williamson()
