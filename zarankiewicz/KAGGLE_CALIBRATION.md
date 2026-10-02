# What a Kaggle host is worth, measured — and the prediction it falsified

`ZMODE=calibrate`, `ZQUANTUM=384`, nothing else on the host. Source digest
`580821cb27c118fe`. Gate counts and histogram exact, so the binary is the right one.

```
cpu model  : Intel(R) Xeon(R) CPU @ 2.20GHz      cpus: 4      memory: 32099 MB
gate       : thm7=off 9.04 s      thm7=24 6.66 s

  T=1  wall  506.4 s  core  506.4 s  1.00 of 1 cores   1,293,222 nodes/core-s
  T=2  wall  267.3 s  core  530.6 s  1.99 of 2 cores   1,234,193 nodes/core-s
  T=3  wall  250.1 s  core  709.8 s  2.84 of 3 cores     922,677 nodes/core-s
  T=4  wall  229.9 s  core  861.4 s  3.75 of 4 cores     760,316 nodes/core-s
```

## The finding: four logical cores, about two cores' worth of throughput

Per-core rate falls **41%** from T=1 to T=4 while the OS hands out 3.75 of 4 cores. The
threads are running; they are not getting work done. Going 2 -> 4 threads buys **16%** of
aggregate throughput, which is the classic yield of SMT siblings, and the cliff is between
T=2 and T=3 — exactly where a 2-physical-core machine runs out of real cores.

The contrast is the point. On the container running the production sweep, per-core rate is
**flat** in T (2,190,225 / 2,181,870 / 2,156,826 / 2,146,567, a 2% spread) and the sweep
sustains 3.96 of 4 cores. Same binary, same work.

| | per-core T=1 -> T=4 | cores used at T=4 |
|---|---|---|
| this account's container | 2,190,225 -> 2,146,567 (−2%) | 3.96 |
| Kaggle | 1,293,222 -> 760,316 (**−41%**) | 3.75 |

## Two optima, and they disagree

Because the per-core rate is not flat, the thread count that minimises **wall time** is not
the one that minimises **core-hours**, and P-43(A) is written in core-hours.

| | core-hours | wall-hours | aggregate |
|---|---|---|---|
| T=1 | **2,257** | 2,257 | 1.293e6 nodes/s |
| T=2 | 2,365 | 1,192 | 2.450e6 |
| T=3 | 3,164 | 1,115 | 2.619e6 |
| T=4 | 3,840 | **1,025** | 2.849e6 |

T=4 finishes soonest and costs 1.62x the core-hours of T=1 to do it. **T=2 is the knee**:
it halves the wall time of T=1 for 5% more core-hours, and it is the only multi-threaded
setting that stays inside the 2,880 budget.

## The prediction this falsified

From the smoke run's 9.54 s gate I predicted **2,000–2,150 core-hours**, widened to
1,700–2,600 at ±20%. The measurement is **3,840** at T=4. Outside the interval; the
prediction was wrong.

The diagnosis is exact, and it is not that the proxy is noisy. The gate is **single
threaded**. It predicted sustained 1.36–1.46e6 nodes/core-s and the measured **T=1** rate
is 1,293,222 — within 5–11%, so the proxy did its job. I then applied a single-threaded
prediction to a four-threaded production figure. That substitution is only valid on a host
whose per-core rate is flat in T, and every host I had calibrated the proxy on was one.
The proxy cannot see a scaling cliff, by construction.

Against T=2 (2,365 core-hours) the prediction would have been nearly right, which is a
coincidence of this host and not a rescue.

## What it means for the plan

Five parallel sessions, whole tree, from this measurement:

| | wall time | rounds of 12 h | session-hours |
|---|---|---|---|
| T=4 | 205 h | 17.1 | 1,025 |
| T=2 | 238 h | 19.9 | 1,192 |

Against this container alone at 6.63e6 nodes/s aggregate: **440 wall-hours**. So five
Kaggle sessions are a **2.15x** speedup over the machine already in hand, not the order of
magnitude the core count suggests — four logical cores times five is twenty, but the
throughput is nearer eight cores' worth. Running both gives 2.09e7 nodes/s, **140
wall-hours, 5.8 days**.

## The budget comparison, resolved

P-43(A) fixed 2,880 core-hours in advance, meaning **4 cores x 30 days** — an encoding of a
one-month wall-clock bar, which the operator has since confirmed is the criterion that
actually matters to them. On a machine whose cores are real the two readings are the same
criterion, so there is nothing to reconcile *here*:

| | |
|---|---|
| measured wall/shard, including every container restart and idle gap | **669 s** |
| overhead above pure compute | 6% |
| 2,318 shards remaining, container alone | **17.9 days** |
| against the bar | passes, 1.68x margin |

The apples-to-oranges problem was real but is now moot: it only bit if Kaggle core-hours had
to be charged against a core-hour budget. At T=4 the sweep would consume 3,840 Kaggle
core-hours for work that costs 1,790 here, and a core-hour on an SMT sibling is not
P-43(A)'s unit. Since the binding criterion is wall clock and the container alone clears it,
Kaggle is **optional acceleration** and its core-hour inefficiency costs nothing that is
being measured. T=4 is therefore the right setting there: it is fastest in wall time, which
is the only axis that matters now.

## The split, sized so that Kaggle failing entirely still passes

| | shards | time |
|---|---|---|
| this container | 0..799 | 5.6 days |
| Kaggle, 5 slots of 320 | 800..2399 | 5.5 days, ~11 rounds of 12 h |
| both | | **~5.6 days** |
| **Kaggle never runs at all** | container takes everything | **17.9 days, still passes** |

The cut at 800 is chosen for that last row, not to balance the two. Kaggle is strictly a
bonus: if the operator never opens a notebook again the result lands in 17.9 days, and if
they run all five slots it lands in 5.6. Nothing about the plan depends on Kaggle working.

`SLOT_FROM`/`SLOT_UPTO` in the bundle encode the window, and the slices tile 800..2399
exactly. The container works upward from shard 0 and Kaggle downward from the top, so
neither can redo the other's work — duplicated effort is the failure mode that would look
most like progress.
