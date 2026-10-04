# The clean uncontended measurement

Every throughput figure before this one was taken with other jobs on the same four cores, at
varying and unrecorded levels. The gated **counts** were exact regardless; the **rates** carried
that noise, and the budget verdict rests on a rate. `bench.py`, `runs/bench_clean.json`.

## Method, and the three things it does differently

1. **Sequential.** One configuration at a time, nothing else running. The load average is recorded
   before every run, so a dirty measurement is visible rather than silent.
2. **A fixed work quantum, not a time cap.** Every configuration processes **the same 384 prefixes
   to completion** — asserted identical, 5.5177 × 10⁸ nodes every time — so thread counts are
   compared on identical work. A time cap compares different amounts of it.
3. **Repeats**, so run-to-run spread is reported rather than assumed away. On shared cloud silicon
   the spread *is* the honest error bar.

Host: 4 × Intel Xeon @ 2.80 GHz.

## The scaling curve

| T | wall s | core s | nodes/core-s | aggregate/s | speedup | per-core eff | wall spread |
|---|---|---|---|---|---|---|---|
| 1 | 286.7 | 286.7 | **1,924,549** | 1,924,522 | 1.00× | 100% | 3.2% |
| 2 | 150.4 | 294.5 | 1,873,640 | 3,667,965 | 1.91× | 97% | 2.0% |
| 3 | 108.9 | 316.7 | 1,742,353 | 5,068,418 | 2.63× | 91% | 0.8% |
| 4 | 79.5 | 302.8 | **1,821,979** | **6,936,293** | **3.60×** | **95%** | 2.8% |

**Threads scale 3.60× on four cores at 95% per-core efficiency.** The dip at T = 3 (91%) against
T = 4 (95%) is larger than the run-to-run spread at either point and I have no explanation for it;
it is recorded as measured rather than smoothed.

## Same-host speedup over the received Python

| | Python | C | ratio |
|---|---|---|---|
| (7,7), Theorem 7 off | 165.6 s | **10.38 s** | **15.95×** |
| (7,7), Theorem 7 on | 393.2 s | 8.06 s | **48.78×** |

Both uncontended, same host, best of three, counts exact every run.

The gap is far larger with Theorem 7 **on** because its m′ = 4 clause is a C(k−1,3) triple scan in
pure Python loops, which is where an interpreter loses most. It is still net negative at 1.442×
tree shrink against 3.08× per-node cost, and still defaults off.

## Three retractions

> **`24.3×` → `15.95×`.** The 24.3× came from 186.1 s ÷ 7.65 s on the *previous* container, and
> **both of those were measured with other jobs running.** The clean same-host ratio is 16×.
>
> **`2,321–2,759` core-hours and a 12% margin → `1,464–1,740` and a 1.80× margin.** That figure
> came from the contended 1,149,393 nodes/core-s; clean, the rate is 1,821,979, so the contended
> number was **pessimistic by 59%**.
>
> **`32% → 106%` parallel efficiency**, already withdrawn in `c/README.md`, compared two different
> binaries. The honest figure is the 95% in the table above.

Three performance claims, three corrections, all from the same root: **comparing numbers taken
under conditions I had not controlled or recorded.** That is the same error as pinning a node
threshold to a rate I was about to improve, and as reasoning for nine rounds on relayed level
counts whose index set I could not restate. `D68` names the general form.

## Host-to-host variation, now observed rather than assumed

The C gate is 10.38 s here against 7.65 s on the previous container — **36% apart** — while Python
is 165.6 s here against 186.1 s there, **11% apart the other way.** Moving in opposite directions
is the signature of contention rather than of silicon, and is why only the numbers on this page
count.

**The consequence for anyone booking sessions: this budget is host-dependent.** 1,602 core-hours
here, against a 2,880 budget, absorbs a host 1.8× slower than this one and no more. Kaggle's host
is a third unknown, and the first thing `kaggle_shard.py` prints is the gate time, which is the
calibration — **compare it to 10.38 s before trusting any session count.**

## The budget

| | |
|---|---|
| tree | 1.0510 × 10¹³ nodes (rel. SE 4.39%) |
| rate, T = 4, clean | 1,821,979 nodes/core-s |
| **the sweep** | **1,464 / 1,602 / 1,740 core-hours** (95% lo / point / hi) |
| `P-43`(A) budget | 2,880 core-hours |
| **margin** | **1.80× at the point, 1.65× at the 95% high** |
| wall clock | **16.7 days on 4 cores** |
| 12-hour 4-core sessions | **33** |

Core-hours are marginally lowest at T = 1 (1,517 against 1,602, a 6% difference) while wall clock
is 3.6× better at T = 4. The 6% is not worth optimising for; **run T = 4.** The earlier version of
this note made more of that gap than 6% deserves.

## The gate says it is not the silicon — and the gate is not enough

Measured in the idle gap between cycles 21 and 22, nothing else on the machine, three reps:

| | |
|---|---|
| this host, `./zsearch -m 7 -n 7` | **10.164 / 9.722 / 9.716 s** |
| reference above | 10.38 s |
| counts and histogram | exact, all three reps |
| CPU | Intel Xeon @ 2.80 GHz, 4 logical cores |

So single-threaded this host is **2-6% faster** than the reference host. At four threads it
produces **1,294,336 nodes/core-s** in production against that host's clean **1,821,979** —
**29% worse.** Equal or better on one thread, 29% worse on four: the deficit is in **parallel
scaling, not single-core speed.** That is consistent with shared logical cores or with a
co-tenant's memory traffic, and this measurement does not separate those two.

**The provenance matters and it is imperfect.** The 10.38 s above was recorded in `5bd3020` on
Oct 1, which is a container *earlier* than the one that booted 00:32 on Oct 2 and ran fifteen
cycles at about 1.73e6. So the matched pair here is Oct-1 host against today's host. **The 00:32
host was never gate-timed** — its gate was run for counts only, every heartbeat, and the time
was never recorded. That was free information, available 22 hours running, and it is the reason
the middle host cannot be placed on the single-thread axis at all. Record the time, not just the
verdict.

A second imperfection, bounded rather than waved away: 1,821,979 came from `bench.py`'s fixed
384-prefix quantum and 1,294,336 comes from production shards of about 2,774 prefixes, so the
work is not identical. The 00:32 host's production figure (~1.73e6) sits 5% under the Oct-1
host's bench figure, so the bench-versus-production bias is a few percent against a 29% gap.

### The correction to this page's own advice

Above, this page says: "the first thing `kaggle_shard.py` prints is the gate time, which is the
calibration — **compare it to 10.38 s before trusting any session count.**"

**That is now falsified by this host.** It matches the gate and delivers 29% less. A
single-threaded timing cannot calibrate a four-threaded budget, which is exactly the error
diagnosed in `KAGGLE_CALIBRATION.md`, where a gate-proxy prediction of 2,000-2,150 core-hours
met a measured 3,840 because the gate is single-threaded and the production figure is not. The
calibration that works is the **threaded** one, and `kaggle_shard.py` already prints it:
`ZMODE=calibrate` with `ZQUANTUM=384` walks T = 1..4 on the same fixed quantum. Compare *that*,
not the gate.

### What is deliberately not being measured

The full thread curve on this host would say whether the loss is SMT siblings or a neighbour.
It is **not being run**, and the reason is a rule this repo has already paid for: on either
answer the sweep still wants T = 4, because wall clock is the binding axis and four threads
maximise aggregate throughput under both. The curve costs about 16 minutes of four cores — more
than a shard — for an answer attached to no decision. `RATE_DECLINE.md` consumed four reports
and three retractions on exactly that shape of question. The 30-second gate was worth taking
because it discriminates; the 16-minute curve is not.

## The denominator: `core_seconds` is measured, not `wall_s x threads`

Every shard certificate carries both, and they are **not the same number**:

```
sh_221.json   wall_s 563.32   core_seconds 2207.54   nodes_per_core_s 1889781
              wall_s x 4 = 2253.28, so core_seconds is 97.97% of it
```

`core_seconds` is accumulated CPU time; `wall_s x threads` is the wall window times the thread
count. The second is an upper bound on the first and overstates the denominator whenever a
thread is not running, so dividing nodes by it **understates the rate**.

This cost a published comparison. `a9dfc16` reported cycle 33's full mean as 1,802,227
nodes/core-s and called it "0.38% apart" from cycle 32's 1,795,488 — but 1,802,227 was computed
as `nodes / (sum(wall_s) * 4)` while 1,795,488 was `nodes / sum(core_seconds)`.

| cycle | `nodes / sum(core_seconds)` | `nodes / (sum(wall_s) * 4)` |
|---|---|---|
| 32 (201..208) | **1,795,488** | 1,780,576 |
| 33 (209..216) | **1,814,693** | 1,802,227 |

Cycle 33's comparable full mean is **1,814,693** and the gap to cycle 32 is **1.07%**, not 0.38%.
Both columns are defensible quantities; mixing them inside one comparison is not — and the error
ran in the direction that flattered the claim, since the understated figure was the one being
compared in. **Every cycle full mean in this programme is `nodes / sum(core_seconds)`.**

### What this does and does not measure

The ratio `sum(core_seconds) / (sum(wall_s) * threads)` is free in every certificate, and on this
host it reads:

```
cycle 32   99.17%      cycle 38   99.23%
cycle 33   99.31%      cycle 39   98.87%
cycle 34   99.23%      cycle 40   99.09%
cycle 35   99.05%      cycle 42   98.81%
cycle 37   99.20%
```

Recomputed over each cycle's **whole** shard range from the committed certificates, which is why
cycle 34 reads 99.23% here and 98.95% in an earlier draft of this section: that figure was the
first five shards of a nine-shard cycle, a partial quoted as a cycle's. Cycle 36 is omitted as
VOID and cycle 41 as truncated. The range over the nine clean full cycles is **98.81% to
99.31%** — a spread of half a percentage point across 74 shards on one host.

That is a **busy fraction**: it says the four threads were almost never idle, so almost nothing
is lost to serialisation, lock waits, or the single-threaded head and tail of a shard. It bounds
one failure mode tightly and cheaply.

It is **not** the thread curve the section above declines to run, and it must not be quoted as
one. Four threads contending for shared execution resources — SMT siblings, a shared L3, a noisy
neighbour — stay 100% *busy* while each core does less work per second. A busy fraction of 99%
is therefore compatible with a large scaling loss, which is exactly the shape of the previous
host's 29% deficit. The thread curve remains unrun, for the reason already given; what changed
is only that one narrow question now has a free answer, and the repo had been accumulating that
answer in every certificate without reading it.
