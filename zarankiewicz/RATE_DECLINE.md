# The rate decline: identified. It tracks machine uptime, not shard index

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

# RESOLVED: the same shard, the same binary, 15 hours apart

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
construction, so it is excluded: the decline tracks **elapsed machine uptime**.

That accounts for most of the ~12% spread in the cycle means; the remainder is shard mix, which
is real even though my account of its cause was wrong (see above — survivor count explains
nothing, r = −0.008).

## A correction that came with it

The machine booted at **00:32 and has been up continuously for 15 h 43 m**. So the five
"container restarts" I logged were not all machine reboots — the one at 13:29 restarted this
session's background tasks while `uptime` ran straight through it. Commit 24f64b8 says "fifth
container restart survived" and credits the repo, binary and 116 MB frontier with surviving it.
True, but for a smaller reason than implied: the filesystem never went away, so nothing was at
risk that time. Only the restarts at or before 00:32 were real reboots.

## What follows

A genuine reboot should recover the 8.5%, which is consistent with the earlier observation on a
different host of a 31% fall over four hours that "recovered fully on restart" — same
phenomenon, larger magnitude. I cannot reboot the machine, and at 17.9 days against a 30-day
bar there is no reason to want to: 8.5% moves 17.9 days to about 19.5.

The useful part is that the quantity is now named. Future reports should say *uptime*, and a
future session that does get a fresh machine should expect roughly 1.8e6 again at the start and
watch it settle toward 1.65e6 over the first day.
