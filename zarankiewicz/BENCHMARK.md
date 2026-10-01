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
