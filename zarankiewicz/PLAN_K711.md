# Preparing (11,7): yes — but the platform choice should wait about an hour

Short answer: **the preparation is worth doing now and is done; the Kaggle decision is not yet
ripe, and two measurements already in flight decide it.** Building the harness is the common
prerequisite to every route, so it is not wasted whichever way those land.

## 1. First, what "`P-43`(A) is open" does and does not mean

**Open** means not falsified and not at risk on any ground currently on file. It does **not** mean
measured to pass. Nothing yet measures (11,7).

And the registered wording has a clause that the platform question runs straight into:

> *(A) FEASIBILITY: a re-implementation of Woodall's (11,7) search … completes on **one modern
> machine** within **30 DAYS** of wall-clock compute.*

**A run sharded across twenty Kaggle sessions is not one machine.** If we shard and then score the
threshold in wall clock, we would be passing a bar by changing its subject — which is exactly what
`D44` exists to stop. So the conversion has to be fixed **now, before the measurement**, not after
it:

| | |
|---|---|
| "one modern machine" | **4 cores** — what this container gives and what a Kaggle CPU session gives |
| so the budget is | **2,880 core-hours** |
| at the measured single-core rate of 125,730 nodes/s | **1.30 × 10¹² nodes** |

A sharded run passes (A) iff its **total core-hours ≤ 2,880**, regardless of how little wall clock
it takes. Recorded before any (11,7) number exists.

## 2. The ladder as measured, all Theorem 7 off, all complete to the stated depth

| | nodes | seconds | note |
|---|---|---|---|
| (7,7) full | 16,263,610 | 186 | leaves 809,438 |
| (9,7) to depth 6 | 57,339,889 | 456 | depth 7 in flight |
| (11,7) to depth 5 | 6,740,484 | 46.5 | |

## 3. A structural fact that makes (11,7) cheaper to reason about than expected

The staircases line up almost exactly:

| k | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|
| (9,7) | 3 | 11 | 22 | 38 | 57 | 81 | 110 | 142 | — | — |
| (11,7) | 3 | 11 | 22 | 38 | **59** | **83** | **112** | **144** | 182 | 223 |

**Identical at k ≤ 5, exactly +2 at k = 6…9, then two extra levels.** The other two clauses —
prefix-minimality and stabiliser lex-min — are local conditions that never mention m. So levels
1–5 of the (11,7) tree must be *identical* to levels 1–5 of the (9,7) tree.

I registered that before running it and it came back exact: **1 · 13 · 2,131 · 82,512 ·
6,655,827** both times. So (11,7) is "the (9,7) tree with each budget 2 looser, plus two levels on
top", and once the (9,7) total is known the only unmeasured quantities are what +2 per level costs
and what the last two levels add. The +2 is not small — on 4-element sets the class count goes
12,484 → 38,309 as the bound moves 21 → 22, a factor of 3.07 — which is why this is a measurement
and not an estimate.

## 4. Three routes, and the measurement picks one

| if the full (11,7) tree is | route | why |
|---|---|---|
| **≲ 10⁹ nodes** | one job in this container | 2.2 core-hours. No Kaggle, no sharding |
| **10⁹ – 10¹² nodes** | **Kaggle, sharded** | 2.2–2,880 core-hours; inside the budget; this is where the harness earns its keep |
| **≳ 10¹² nodes** | compiled rewrite first | Python at 1.3 × 10⁵ nodes/s is the wrong instrument; bitsets and C buy the ~30× the upstream README's own reasoning implies, and only then shard |

Note the third row is not a dead end — it is a 30× multiplier on every figure in the table.

## 5. The harness, built and gated

`shard.py`. The design turns on one observation: **the only state a node needs is its prefix.**
Everything in `rec(k, S, ch, co)` plus `buf[k]` is recomputable from `ch` alone, so a prefix at any
split level is a complete serialisable task, sibling subtrees are disjoint, and their level counts
add.

* **Phase 1, frontier.** Enumerate every surviving prefix at level L. This needs no new code:
  the received `search()` takes the staircase as a parameter, so calling it with `m = L` and
  `B = staircase(11, 7)` runs the *target's* node-keep predicate and returns the level-L prefixes.
* **Phase 2, shards.** Each worker takes a slice and runs the continuation. `search_from()` is the
  received `search()` with one added argument.
* **Resumability is free**: `run` is idempotent per shard, so a session killed by the wall clock is
  resumed by re-issuing the identical command.

**A fork of someone else's search is a liability unless it is gated**, so `shard.py selftest`
requires the fork to reproduce (7,7) exactly — both configurations, as a single process *and* as
the sum over shards at two different split levels, with the frontier count required to equal the
shard roots.

> **GATE PASSED**, 10 of 10 assertions. Both configurations reproduce exactly, single-process and
> summed over shards at L = 3 and L = 4, with the frontier counts equal to the shard roots (377 and
> 29,099 off; 329 and 25,346 on). The fork is faithful.

## 5a. The estimator — and the reason the old numbers were wrong

Sharding buys something beyond parallelism, and it is the more valuable half: **an estimator with
an error model.**

The tree is a disjoint union of the subtrees rooted at the level-L prefixes, so the total is a sum
over independent subproblems, and a systematic sample of *complete* subtrees scaled by the frontier
size is **unbiased** for the total. Validated against the known (7,7) total of 16,263,610:

| split level | frontier | sampled | estimate | ratio to truth | skew max/mean |
|---|---|---|---|---|---|
| L = 4 | 29,099 | 50 | 1.424 × 10⁷ | 0.876 | 6 |
| L = 4 | 29,099 | 200 | 1.665 × 10⁷ | 1.024 | 12 |
| L = 4 | 29,099 | 1,000 | 1.579 × 10⁷ | 0.971 | 15 |
| **L = 5** | **801,503** | **3,000** | **1.6407 × 10⁷** | **1.0088** | **4.8** |

**Within 0.9% for 8 seconds of compute**, and a deeper split level is both cheaper per subtree and
less skewed. Every cost estimate this target has produced was instead an extrapolation of an
*aggregate* — the 4,838× raw-space proxy, the 10³ hardware speedup, the growth-ratio fit that
missed by 32× — and an aggregate growth curve has **no error model at all**, so a wrong answer is
indistinguishable from a right one until the truth arrives. `D68` records this; the operative rule
is: ask whether the quantity decomposes, and if it does, sample it.

Choosing L is the trick. At (11,7) the level-4 subtrees are large enough that two dozen of them do
not finish in fifteen minutes, so the sample runs at L = 5 where the frontier is 6.66 million
prefixes and each subtree is correspondingly small.

## 5b. The harness, continued

## 6. Kaggle specifics

* **12 hours** per CPU session, and **no weekly cap on CPU** — only the per-session limit. That is
  the one feature that matters here, and it is a good one.
* ~4 cores per session, so Kaggle is not *more* compute per session than this container; it is
  *more sessions, in parallel, free*.
* 20 minutes of idle time in an interactive session, so the work must be a committed/saved run,
  not an interactive one.
* Persistence between sessions is via notebook output → attach as a dataset input to the next run.
  `shard.py`'s `runs/` directory is already the right shape for that: one small JSON per shard.
* Two honest caveats. **Fair use**: 960 core-hours of free compute is a lot to take from a free
  tier, and a rented VM at that scale is tens of dollars, which avoids the question entirely —
  your call, not mine. And **the core-hour accounting in §1** applies whichever you pick.

## 7. The cheaper thing to try first

The **refutation branch** is still unrun, and it just got cheaper: `generator.py`'s
`total_crossings` is a direct segment-intersection count, it is now verified locally (37 crossings
on the realised (4,6)-set, against antisum 15), and `realise` already does the
abstract-set-to-drawing direction. One drawing of K₇,₁₁ with 221 or 223 crossings settles the
conjecture negatively, is **self-certifying**, needs no exhaustion and no ε exposure.

The prior says it fails. But it is hours of local search against a multi-day sweep, with a free
negative, and nobody has spent those hours. **I would spend them before committing a platform.**

## 8. What I need from you

1. Whether to proceed on Kaggle at all, given §6's two caveats — or whether a rented VM is
   simpler.
2. If Kaggle: the account side is yours. I can produce the notebook and the shard commands; I
   cannot reach Kaggle from here.
3. Whether to spend a few hours on §7's refutation search first. I recommend yes.

Nothing in §8 blocks the next step, which is the two runs already in flight.
