# PTE size 11 — first result, scored against `PREREG_PTE11.md` §5

Run 21 Sep 2026. Five exhaustive heights, one hour of budget, and the predictions scored by
`score_pte11.py`, which was committed before any of this existed.

```
A-1  CONFIRMED   exhaustive to H=36: at or above 20, below 50
A-2  FALSIFIED   stopped by the clock with memory to spare
A-3  CONFIRMED   no solution in 5 run(s); exhaustive at H in [20, 24, 28, 32, 36]
A-4  NOT-SCORED  evidence/A4_literature.json absent -- promoting search not run
A-5  NOT-SCORED  evidence/A5_asymmetric.json absent -- promoting search not run
```

## 1. The runs

| H | right-hand tuples | left-table keys | seconds | peak RSS | solutions |
|---:|---:|---:|---:|---:|---:|
| 20 | 4,496,388 | 583,569 | 26.1 | 267 MB | 0 |
| 24 | 13,983,816 | 1,547,489 | 80.5 | 710 MB | 0 |
| 28 | 36,288,252 | 3,500,337 | 207.4 | 1,563 MB | 0 |
| 32 | 82,598,880 | 7,061,121 | 471.1 | 3,124 MB | 0 |
| 36 | 170,230,452 | 13,065,937 | 1,001.7 | 5,802 MB | 0 |
| 40 | 324,540,216 | — | **incomplete**, 1,811 s (96.1 % of the way) | — | — |

Every completed row asserts `right_enumerated == C(2H+1, 6)` before it is allowed to call itself
exhaustive, so "no solution" means the region was actually swept, not that the loop ended.

**The cost model is clean enough to extrapolate from.** Pooled over the five runs, the search
does **172 k right-hand tuples per second** — constant to within 3 % across a 38× range — and the
left table costs **445 bytes per key**, constant to within 4 %. The number of distinct keys is
0.855 × C(2H+1, 5): about one key in seven is a collision.

## 2. A-1 confirmed, and not by luck

Predicted: reaches H ≥ 20, does not reach H = 50. Reached **H = 36** exhaustively.

The constant rate makes the second half of that prediction a statement rather than a hope: H = 50
is C(101,6) ≈ 1.27 × 10⁹ tuples, which at 172 k/s is **7,362 s — just over two hours**. It was
never within an hour's reach. And H = 40 at 1,811 s reached 96.1 % of its region, which the same
rate predicts to within the run's own measurement error.

## 3. A-2 falsified — and the near-miss is the interesting part

Predicted: **memory** binds, not the clock. Observed: `stopped_by: clock`, with
`memory_headroom: true` — 5.8 GB peak against the 12 GB cap and 16 GB on the box.

The prediction is wrong as written and is scored wrong. It is **not** rescued below; this is
where the two walls actually stand, because that is worth knowing for the next run:

| wall | where it binds |
|---|---|
| 12 GB cap, at 445 bytes/key | 28.9 M keys → **H ≈ 42.5** |
| one hour on a single height, at 172 k/s | 620 M tuples → **H ≈ 44.4** |

So the mechanism claim was off by about **two rungs of the ladder**. What actually stopped this
run was neither wall: the hour was a *cumulative ladder* budget, and four fifths of it went on
heights far below either limit. That is a flaw in how the prediction was operationalised, not a
second reading of the result — A-2 said memory would bind and the clock bound, so A-2 failed.

*(A first attempt at the ladder died mid-H=32 when the container suspended on an idle session,
taking a `nohup`'d process with it. Nothing was scored from that: the stop was neither of A-2's
two outcomes, and `RUN_LOG.json` was never written. The three heights it had completed were kept
and the remaining budget was re-run under harness tracking.)*

## 4. A-3 confirmed, and much weaker than it sounds

No ideal symmetric solution of size 11 exists whose **primitive centred form** has height ≤ 36.

That region is smaller than it looks, and there is a local calibration that shows exactly how
small. The classic size-**7** solution

> {0, 18, 27, 58, 64, 89, 101} / {1, 13, 38, 44, 75, 84, 102}

is swapping-symmetric with *t* = 102, centred form *C* = 2*A* − 102 = {−102, −66, −48, 14, 26, 76,
100}, and gcd 2 — so its **primitive centred height is 51**, and its diameter is 102. Verified
here, including the round trip back to the pair.

**So this run did not reach the height at which the smallest known size-7 solution lives**, let
alone a size-11 one. The null is real and it is exhaustive over what it covers, and what it
covers is well inside the region anyone would have looked at first. A-3 is confirmed and carries
almost no weight against the target.

That is the honest reading, and it makes **A-4 the prediction that matters**: if the published
symmetric bound is ≥ 1000× ours, this whole direction is inside somebody else's null.

## 5. Where that leaves the target

§6 of the pre-registration cannot fire: it needs A-3, A-4 and A-5, and two are unrun. The scorer
says so itself rather than defaulting to a pass.

What the run changes: **nothing about the target, and quite a lot about the method.** A one-hour
container gets to H ≈ 44 on a single height, which is roughly where both walls stand; getting
materially past that needs a better algorithm, not a bigger budget — the ×9 memory factor per
eight rungs is what kills it, and the obvious move is an on-disk or sorted-merge left side rather
than a Python dict.

Next, in order:
1. **The A-4 promoting search.** Borwein–Lisoněk–Percival (Math. Comp., 2003) and whatever has
   superseded it: what height did the exhaustive symmetric size-11 search actually cover? One
   number decides whether anything here is worth continuing.
2. **The A-5 promoting search**, on whether the asymmetric region is as unswept as
   `../gap/RESULT_GAP_v2.md` §6 claims.
3. Only if A-4 fails — i.e. there is real room — rebuild the left side to get past H ≈ 44.
