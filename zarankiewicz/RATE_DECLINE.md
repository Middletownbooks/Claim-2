# The rate decline: unidentified, and two of my explanations for it are wrong

Nine whole-cycle means, nodes/core-s:

```
1,773,311  1,758,144  1,767,101  1,740,214  1,656,845  1,629,509  1,632,896  1,608,256  1,557,635
```

Cycle 13 is the slowest of the run, **12.2% below the peak** and inside the 15% action
threshold but no longer comfortably. Two mechanisms have been on the table: container aging,
and shard difficulty drifting with shard index. Neither is established, and the attempt to
settle it produced mostly corrections.

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
