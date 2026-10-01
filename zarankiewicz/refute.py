#!/usr/bin/env python3
"""The refutation branch: hunt a straight-line drawing of K_{7,11} below 225 crossings.

WHAT THIS CAN AND CANNOT DO, because the asymmetry is the whole point.

  cr(K_{7,11})  <=  rcr(K_{7,11})  <=  Z(7)Z(11) = 225

the upper bound being Zarankiewicz's own rectilinear construction.  So:

  * a straight-line drawing below 225 REFUTES Zarankiewicz, and is self-certifying
    by direct segment intersection -- no exhaustion, no specification error, no
    trust in anyone's canonical form;
  * finding none proves NOTHING about the topological conjecture, because an
    optimal drawing need not be rectilinear.

It is a lottery ticket with a free negative, and it is a LONG shot: rcr < 225
would itself be a separately notable result.  It is run because hours against a
multi-day sweep is the right price for a self-certifying positive, not because
it is likely.

AND IT IS NOT A SHORTCUT THROUGH THE SWEEP.  Lowering the top rung from 223 to
221 moves only two levels of the staircase -- 223,182,... becomes 221,180,... and
the levels at k <= 9 are untouched -- so "search only for refutations" costs
essentially what the full sweep costs.  Measured, not assumed; see PLAN_K711.md.

POSITIVE CONTROL FIRST.  The counter is validated on the known-optimal drawing:
Zarankiewicz's construction, perturbed into general position, must come back at
exactly 225.  The construction puts ceil(m/2) points on the positive x-axis and
floor(m/2) on the negative, and likewise for n on the y-axis -- which is wildly
degenerate for a predicate built on strict orientation tests, so the perturbation
is part of what is being checked.
"""
import json, math, pathlib, random, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / "intake"))
from generator import total_crossings, crosses                      # noqa: E402
from cog import Z                                                    # noqa: E402

M, N = 7, 11
TARGET = Z(M) * Z(N)


def zarankiewicz(m=M, n=N, eps=0.0, rng=None):
    """The optimal construction, optionally perturbed into general position."""
    P, Q = [], []
    for i in range(m):
        x = (i // 2 + 1) * (1 if i % 2 == 0 else -1)
        P.append([float(x), 0.0])
    for j in range(n):
        y = (j // 2 + 1) * (1 if j % 2 == 0 else -1)
        Q.append([0.0, float(y)])
    if eps:
        rng = rng or random.Random(0)
        for pt in P + Q:
            pt[0] += rng.uniform(-eps, eps)
            pt[1] += rng.uniform(-eps, eps)
    return [tuple(p) for p in P], [tuple(q) for q in Q]


def general_position(pts, tol=1e-12):
    """No three points collinear -- required for the orientation predicate."""
    n = len(pts)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                a, b, c = pts[i], pts[j], pts[k]
                if abs((b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])) < tol:
                    return False
    return True


def control():
    print("POSITIVE CONTROL: Zarankiewicz's construction must count %d" % TARGET)
    P, Q = zarankiewicz()
    print("  unperturbed (degenerate: all 7 collinear, all 11 collinear)")
    print("    general position: %s   crossings: %d"
          % (general_position(P + Q), total_crossings(P, Q)))
    ok = 0
    for eps in (1e-6, 1e-4, 1e-3, 1e-2):
        hits = []
        for s in range(5):
            P, Q = zarankiewicz(eps=eps, rng=random.Random(s))
            hits.append(total_crossings(P, Q))
        good = all(h == TARGET for h in hits)
        ok += good
        print("    eps=%-7g  crossings %s  %s" % (eps, hits, "ok" if good else "NOT %d" % TARGET))
    print("  -> %d of 4 perturbation scales reproduce %d exactly" % (ok, TARGET))
    return ok > 0


def anneal(seed, iters=200000, t0=2.0, t1=0.01, start=None, report=None):
    """Minimise crossings by annealed single-point moves."""
    rng = random.Random(seed)
    if start is None:
        P = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(M)]
        Q = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(N)]
    else:
        P, Q = [list(p) for p in start[0]], [list(q) for q in start[1]]
        P = [tuple(p) for p in P]; Q = [tuple(q) for q in Q]
    cur = total_crossings(P, Q)
    best, bestcfg = cur, (list(P), list(Q))
    for it in range(iters):
        T = t0 * (t1 / t0) ** (it / iters)
        side = rng.random() < M / (M + N)
        arr = P if side else Q
        i = rng.randrange(len(arr))
        old = arr[i]
        step = T * 0.5
        arr[i] = (old[0] + rng.gauss(0, step), old[1] + rng.gauss(0, step))
        new = total_crossings(P, Q)
        if new <= cur or rng.random() < math.exp((cur - new) / max(T, 1e-9)):
            cur = new
            if new < best:
                best, bestcfg = new, (list(P), list(Q))
                if report:
                    report(best, bestcfg)
        else:
            arr[i] = old
    return best, bestcfg


if __name__ == "__main__":
    if not control():
        print("\nCONTROL FAILED -- the counter does not reproduce 225 on the optimal")
        print("drawing, so nothing it says about any other drawing means anything.")
        sys.exit(1)
    budget = float(sys.argv[1]) if len(sys.argv) > 1 else 1800.0
    seed0 = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    print()
    print("SEARCH: budget %.0f s, target < %d" % (budget, TARGET))
    t0 = time.time()
    overall, cfg, runs, seed = TARGET + 1, None, 0, seed0
    hist = {}
    while time.time() - t0 < budget:
        # half the restarts random, half perturbed from the optimal construction
        start = None if seed % 2 == 0 else zarankiewicz(eps=0.05, rng=random.Random(seed))
        b, c = anneal(seed, iters=40000, start=start)
        hist[b] = hist.get(b, 0) + 1
        runs += 1
        if b < overall:
            overall, cfg = b, c
            print("  seed %-4d new best %d  [%.0f s]" % (seed, b, time.time() - t0), flush=True)
            if b < TARGET:
                print("\n*** BELOW %d -- CANDIDATE REFUTATION ***" % TARGET, flush=True)
                break
        seed += 1
    el = time.time() - t0
    print()
    print("%d restarts in %.0f s; best %d; distribution of local minima %s"
          % (runs, el, overall, dict(sorted(hist.items())[:8])))
    res = dict(m=M, n=N, target=TARGET, best=overall, restarts=runs, seconds=round(el, 1),
               refuted=bool(overall < TARGET),
               local_minima_histogram={str(k): v for k, v in sorted(hist.items())},
               best_P=[list(p) for p in cfg[0]] if cfg else None,
               best_Q=[list(q) for q in cfg[1]] if cfg else None)
    if cfg:
        res["best_recount"] = total_crossings(cfg[0], cfg[1])
        res["best_general_position"] = general_position(list(cfg[0]) + list(cfg[1]))
    pathlib.Path("refute_result.json").write_text(json.dumps(res, indent=2) + "\n")
    print("wrote refute_result.json ; refuted=%s" % res["refuted"])
