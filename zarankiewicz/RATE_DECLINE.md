# The rate decline: shard index is excluded, the cause is NOT established

Nine whole-cycle means, nodes/core-s:

```
1,773,311  1,758,144  1,767,101  1,740,214  1,656,845  1,629,509  1,632,896  1,608,256  1,557,635
```

Cycle 14 then came in at 1,643,035, above cycle 13, so the series is a **band** of 1.56-1.65e6
after an early step down from 1.74-1.77e6, not a monotone slide. Cycle 13 was a low outlier.

**The controlled re-run settles the mechanism.** Scroll to the bottom; the sections between are
kept because each records a wrong turn worth not repeating.

## Per-shard rate against everything measurable (all 91 completed shards)

| | Pearson r |
|---|---|
| rate vs **shard index** | **−0.303** |
| rate vs nodes in shard | −0.049 |
| rate vs survivors below the top rung | −0.008 |

By ten-shard block:

```
  0- 9   1,568,099      40-49   1,699,092
 10-19   1,773,485      50-59   1,635,000
 20-29   1,764,763      60-69   1,644,545
 30-39   1,762,882      70-79   1,583,035
                        80-89   1,576,608
```

## Retraction: shard difficulty does not explain the variance

Twice I explained the ±2% shard-to-shard scatter as differing work per prefix, citing shard 20
emitting 52,441 survivors against shard 19's 16,325. Over 91 shards the correlation between
survivor count and rate is **r = −0.008**, and between node count and rate **r = −0.049**.
Neither explains anything. The scatter is real; my account of its cause was invented and is
withdrawn.

## The restart is not the clean experiment I claimed it would be

I said a container restart would separate aging from index drift in one cycle, because the two
predict opposite signs. The flaw is that shards run in **index order**, so index and elapsed
time advance together and every restart lands at the index the sweep had reached. The
before/after comparison is therefore not a controlled contrast.

Taking it anyway, at the two gaps longer than 20 minutes:

| gap | before | after | |
|---|---|---|---|
| shards 11 \| 12 | 1,748,993 | 1,777,575 | +1.6%, favours aging |
| shards 68 \| 69 | 1,627,086 | 1,616,471 | −0.7%, favours index |

Opposite signs, both inside the per-shard scatter. **Inconclusive.** And the five restarts I
know about mostly do not appear as gaps at all, because relaunch was prompt — only two gaps
exceed 20 minutes, so there are only two pairs to test, not five.

A further point against reading cycle 13 as evidence: it ran on a container twenty minutes old
and was the slowest cycle of the run, which looks like a clean refutation of aging until you
notice its shards were also the highest-index ones yet. Both hypotheses predict "slow" for that
block. It discriminates nothing.

## The experiment that would actually identify it

Re-run an **already-completed low-index shard** on the current container, with nothing else
running, and compare against its original rate.

* shard 12 originally ran at the top of the range (block mean 1,773,485);
* if it now returns ~1.77e6, the decline tracks **shard index**;
* if it returns ~1.56e6, the decline tracks **elapsed time or container state**.

Cost: one shard, about 11 minutes of four cores, 0.004% of the remaining budget. It must run
at a cycle boundary with no sweep competing, and must write survivors to a scratch path so the
committed `low_12.txt` is not touched. `sh_12.json` already records the original rate, so the
comparison needs no new bookkeeping.

## Why this is not urgent

The bar is wall-clock under one month and the measured figure is 18.0 days for all 2,400 shards
including every restart — 1.68x margin. A 12% rate decline moves 18.0 days to about 20 days.
The question is worth settling because I have mis-called it twice, not because the schedule
depends on the answer.

# The controlled re-run: what it does and does not show

Shard 12 re-run on idle cores, nothing else on the machine, survivors to a scratch path so the
committed `low_12.txt` was untouched.

## Determinism first, because it matters more than the rate

| | |
|---|---|
| `total_nodes` | **MATCH** |
| `leaves` | **MATCH** |
| `level_counts` | **MATCH** |
| `antisum_histogram` | **MATCH** |

All four exact against `sh_12.json`. The 98 committed shards rest on this and it holds. Had any
of them differed, the rate question would have been irrelevant and every shard in the repo
would have been in question.

## The rate

| | |
|---|---|
| shard 12 at **00:42**, 10 minutes after boot | **1,808,277** nodes/core-s |
| shard 12 at **16:05**, 15 h 33 m after boot | **1,655,165** nodes/core-s |
| ratio | **0.915** |
| cores used, both runs | 3.92 |

Identical work, identical parallelism, **8.5% slower**. Shard index is held fixed by
construction, so **shard index is excluded**. That is the whole of what this measurement
establishes.

## Where I over-claimed, one hour later

I titled this section RESOLVED and wrote that the decline "tracks machine uptime". Two points do
not establish a functional dependence, and **the very next cycle contradicted it**: cycle 15
averaged 1,696,247 nodes/core-s over machine uptime 15 h 43 m to 17 h 08 m — the fastest cycle
since cycle 4, at the highest uptime yet. A monotone uptime effect predicts the opposite.

Eleven cycle means:

```
1,773,311  1,758,144  1,767,101  1,740,214  1,656,845  1,629,509
1,632,896  1,608,256  1,557,635  1,643,035  1,696,247
```

What survives: the ~8% gap between the 10-minute-uptime measurement and every later one is real
and reproducible on identical work. Whether it is uptime, a one-time change in host conditions,
or fluctuation on a timescale of hours is **not determined by two points**, and the later points
drift upward rather than down.

This is the third time on this one question that I have named a mechanism the data did not
support — first container aging, then shard difficulty, then uptime. The pattern is the finding:
a description was available each time and I reached past it for a cause. What is honestly known
is a description.

## What is honestly known

| | |
|---|---|
| determinism | **verified exactly** |
| shard index as the cause | **excluded** (held fixed, effect persisted) |
| survivor count or node count as the cause of scatter | **excluded** (r = −0.008, −0.049) |
| early-vs-later level difference on identical work | **~8%, reproducible** |
| the mechanism behind it | **unknown** |
| the schedule consequence | none: 17.9 days against a 30-day bar |

## A correction that came with it

The machine booted at **00:32 and has been up continuously for 15 h 43 m**. So the five
"container restarts" I logged were not all machine reboots — the one at 13:29 restarted this
session's background tasks while `uptime` ran straight through it. Commit 24f64b8 says "fifth
container restart survived" and credits the repo, binary and 116 MB frontier with surviving it.
True, but for a smaller reason than implied: the filesystem never went away, so nothing was at
risk that time. Only the restarts at or before 00:32 were real reboots.

## What follows

Report the band and the uptime as two facts side by side, and claim no relation between them
until a measurement establishes one. The honest prediction for a fresh machine is "possibly
faster at first, by something like 8%, on one prior observation" — not a curve.

The question does not need settling. It has consumed four reports and three retractions against
a schedule with 1.68x margin, and the only decision it could inform — whether to want a reboot —
is one I cannot act on anyway. Measuring it further is a cost with no decision attached.

# The reboot of Oct 2, 23:21: a different host, and the answer was in another file

Everything above was measured on one machine. It booted at 00:32 on Oct 2 and the sweep ran on
it for 22 hours and 49 minutes, fifteen whole cycles. At 23:21 it rebooted onto **different
hardware** — `uptime` read 0 min *and* the kernel went `6.18.44-fc-v51` to `-v64`, which is the
pair of facts that distinguishes a reboot from the process-level restart of 13:29.

`53dd8eb` pre-registered the prediction before the next cycle could be seen: near the 1,773,311
peak if uptime mattered, anywhere in 1.56-1.77e6 if it was wander. The measured mean was
**1,304,482 nodes/core-s** — 24.5% below the bottom of the wander band, at 3.91-3.96 of 4 cores,
in a tight three-shard cluster rather than a dip. Neither branch. Numbers in `0610424`.

**This document's own closing prediction is refuted in the direction that costs something.** It
reads: "the honest prediction for a fresh machine is 'possibly faster at first, by something
like 8%, on one prior observation'." The fresh machine was 26% slower.

## The omission, which is the real finding

`BENCHMARK.md` carries a section headed "Host-to-host variation, now observed rather than
assumed". It measures the C gate at 10.38 s on one container against 7.65 s on the previous one,
calls it 36% apart, and states the consequence in bold: **this budget is host-dependent.**

That page and this one are about the same quantity, and this one never cites it. Every mean
above came from a single host, so the band they describe is **within-host wander** — and the
between-host step, the larger effect, was already on the page next door. Three mechanisms were
named and withdrawn here while the fourth sat in another file, measured and bolded.

So the honest decomposition is two effects, not one:

| | |
|---|---|
| within-host wander | ~12% peak to trough, timescale of hours, mechanism unknown |
| between-host step | **26% observed once**, same binary, same work, same core count |

## The one sentence here that has to go

> "Measuring it further is a cost with no decision attached."

There is a decision attached, and it was visible in `BENCHMARK.md` before this reboot. The bar
is wall-clock under one month, so the margin is a function of which host the session draws: 18.0
days and 1.68x on the old one, **23.0 days and 1.30x on this one** (829 s/shard over cycle 21's
three shards, gaps included and now nil). A host 1.3x slower than this one would not clear the
bar at all. The measurement also costs nothing — it arrives as a side effect of work that was
going to run anyway, which is the reason the prediction could be pre-registered for free.

What this does **not** establish: whether this host is slower in silicon or is sharing its
logical cores with another tenant. Accounted core-seconds cannot separate those — a shared SMT
sibling bills you the full time while delivering less, which is exactly the Kaggle thread curve
in `KAGGLE_CALIBRATION.md`. The discriminator is the single-threaded gate against
`BENCHMARK.md`'s 10.38 s, and that page's three retractions all come from comparing timings
taken under uncontended conditions with timings taken under load, so it counts only if it is
measured in an inter-cycle gap with nothing else running.
