# Preparing (11,7): the harness is built, and the measurement says **not Kaggle — the rewrite**

> **VERDICT, 1 Oct 2026, from the first unbiased estimate of the (11,7) tree.** Sampling 65 of the
> 6,655,827 level-5 subtrees to completion puts the full tree at **8.8 × 10¹² nodes**, which in
> this Python implementation is **17,209 core-hours**. Against that:
>
> | route | cost at the estimate | verdict |
> |---|---|---|
> | one 4-core machine, Python | 17,209 core-hours = **179 days** | fails `P-43`(A)'s 2,880 by **6×** |
> | Kaggle, 12-hour 4-core sessions | **359 sessions** | not viable |
> | **compiled + bitsets, ~30×** | **574 core-hours = 6 days on 4 cores** | **passes with room** |
>
> **The rewrite is not an optimisation here; it is the difference between failing the registered
> threshold by 6× and passing it with room.** And it dominates across the whole uncertainty
> interval: at the optimistic end it turns 884 core-hours into 29, and at the pessimistic end it is
> the only thing that works at all. Kaggle is the right answer only in a narrow middle band — and
> even there, writing the C is less work than babysitting 359 notebook sessions.
>
> `P-45`, which predicted the tree below 1.30 × 10¹² nodes, is **heading for falsification** at
> 6.7× over. Not yet scored: see the uncertainty note in §5c. A larger randomised sample is in
> flight.

The preparation below was worth doing and is done — the harness is what produced the estimate, and
it is still the thing that runs the sweep once the rewrite exists.

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

## 4. Three routes, and the measurement picked the third

| if the full (11,7) tree is | route | why |
|---|---|---|
| ≲ 10⁹ nodes | one job in this container | 2.2 core-hours. No Kaggle, no sharding |
| 10⁹ – 10¹² nodes | Kaggle, sharded | inside the budget; where the harness would earn its keep |
| **≳ 10¹² nodes — THIS ONE** | **compiled rewrite first** | Python at 1.4 × 10⁵ nodes/s is the wrong instrument; bitsets and C buy the ~30× the upstream README's own reasoning implies, and only then shard |

The third row was never a dead end — it is a 30× multiplier on every figure in the table, and it is
now the only row that fits the registered budget.

### A measurement that was thrown away, and why it is recorded anyway

The depth-6 (11,7) run **aborted on its 3,000 s time cap**, so its level counts are invalid — and
the proof is inside them: levels 3, 4 and 5 read 2,098 / 79,994 / 6,448,262 against the exact
2,131 / 82,512 / 6,655,827 from the completed depth-5 run. Disagreement below the deepest level
*is* the proof of truncation, which is exactly what their `ablation_valid()` tests for and what
their README names as the trap that killed four of their numbers.

**It caught me after I had written the warning myself.** §5b of this document says depth caps give
exact counts and a time-capped abort gives none — and I then ran a depth-capped job *with* a time
cap. A depth cap yields exact counts only if the run completes; adding a time cap reintroduces
precisely the invalidity the depth cap was chosen to avoid. `run_search.py` now stamps
`level_counts_valid: false` and a loud warning into any aborted payload, and the run is kept as
`run_m11_thm7_none_d6_ABORTED.json` rather than deleted.

One thing survives as a **lower bound, not a count**: (11,7) level 6 ≥ 418,526,736, against (9,7)'s
exact 50,599,405. So the +2 loosening of the level-6 bound, 57 → 59, costs **at least 8.3×** —
where §3 had guessed ~3× from the k = 4 orbit-count jump. Four such loosenings compound, which is
why this needed a sample and not my arithmetic.

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

## 5c. The estimate, and how far to trust it

| | |
|---|---|
| frontier at L = 5 | 6,655,827 prefixes, enumerated in 76 s |
| sampled to completion | **65** (the 900 s sampling cap fired) |
| sampled nodes | 85,720,914 |
| **point estimate** | **8.78 × 10¹² nodes** |
| relative standard error | **49%** |
| normal-approx 95% band | 4.05 × 10¹¹ to 1.72 × 10¹³ |
| subtree mean / median | **253** |
| subtree max / mean | 28.1 |

**The distribution is extremely heavy-tailed** — median 5,222 against a mean of 1,318,783 — so the
mean is carried by a few enormous subtrees and the normal approximation *understates* the
uncertainty at n = 65. Treat the interval as roughly an order of magnitude either way, not as the
±49% the arithmetic says.

### Calibration, on every case where the truth is known

| case | mean/median | reported rel. SE | estimate / truth | actual error |
|---|---|---|---|---|
| (7,7) full, k = 5,000 | 1.0 | 0.6% | 0.9982 | **0.18%** |
| (9,7) to depth 6, k = 1,000 | 9 | 7.2% | 1.0219 | **2.2%** |
| (9,7) to depth 6, k = 8,000 | 9 | 2.6% | 1.0095 | **0.95%** |
| (11,7) full, k = 65 | **253** | 49% | — | unknown |

**In all three calibrated cases the actual error sits comfortably inside the reported standard
error**, and the error scales as it should: eight times the samples shrank the standard error by
7.2/2.6 = 2.77 against the √8 = 2.83 the theory predicts. So this is a working error model, not a
decorative one —
which is the thing every earlier estimate on this target lacked. But all three calibrations sit at
mean/median 1 or 9 and (11,7) is at **253** — **so the (11,7) interval extrapolates a calibration
rather than resting on one**, and that is the honest caveat, stated instead of a point estimate
quoted bare.

### And the (9,7) total, now estimated rather than attempted

The (9,7) depth-7 run was **stopped**, not completed: it was heading for the same time-cap abort,
and `D68` says to use the estimator. Sampling 4,000 of the level-5 subtrees gives the full (9,7)
tree at **1.634 × 10¹⁰ nodes, 32 core-hours, with a 4.8% relative standard error** — tight,
because the (9,7) subtrees are small (mean 2,455, median **1**: over half the level-5 prefixes have
no descendants at all under the (9,7) staircase).

That gives the cost of going from (9,7) to (11,7) directly: **537×**, which is what "+2 at four
levels, plus two more levels" is worth. The level-5 frontier is the *same* 6,655,827 prefixes for
both, by the identity in §3.

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

## 7a. The gate, for whoever writes the C

`GATE_VALUES.json` collects every exactly-known value on this target in one file —
`PRIMARY-VERIFIED-LOCALLY` only, nothing aborted and nothing relayed — and `check_gate.py` runs an
implementation against it. A rewrite that does not reproduce these is wrong however fast it is.

It includes two **predicate-independent** checks, so a rewrite that canonicalises *more* strongly
than the received node-keep predicate can still be gated: the orbit counts, which depend on CO₇
alone, and the identity that **leaf counts must not move when Theorem 7 is toggled** — 809,438
either way, because the prune may only remove interior nodes that cannot reach a survivor. Any
implementation whose leaf count changes with the prune has a bug in the prune.

## 8. What I need from you

1. Whether to proceed on Kaggle at all, given §6's two caveats — or whether a rented VM is
   simpler.
2. If Kaggle: the account side is yours. I can produce the notebook and the shard commands; I
   cannot reach Kaggle from here.
3. Whether to spend a few hours on §7's refutation search first. I recommend yes.

Nothing in §8 blocks the next step, which is the two runs already in flight.
