# Yes — and while writing the answer I found the hard reason

**Short answer: yes, and it is not an efficiency question.** I went looking for something I
could check locally before answering, and what came back says the relay has been moving numbers
whose definition neither side has pinned down.

## 1. The measurement I ran instead of arguing

Every cost figure on this target — mine and theirs — is a function of one relayed sequence, the
per-level node counts of their (7,7) enumeration:

```
Theorem 7 ON  : 1, 12, 329, 25346, 615817
Theorem 7 OFF : 1, 13, 377, 29099, 801503
```

The 4–5 × 10⁸ full-tree extrapolation, the 1–3 hour (7,7) estimate, the 3–8× speedup over
Woodall, the 5–10 month (11,7) sweep, the 1.30× Theorem 7 ablation that moved **H** to PASS: all
of them are arithmetic on those five numbers. **Levels 1 and 2 are small enough to enumerate
exactly here.** So I did, under the natural reading — isomorphism classes of *k*-element subsets
of *V*(CO₇) below Woodall's prefix bound for that depth, 3 at *k* = 2 and 9 at *k* = 3.

| | their OFF | local, under S₇ | local, under S₇ × ⟨rev⟩ |
|---|---|---|---|
| level 1 | **13** | **14** | **11** |
| level 2 | **377** | **280** | **158** |

**Neither term reproduces, and they miss in opposite directions.** Level 1 is *over* by one and
level 2 is *under* by 97, so no single cause — a weak canonical form, a different threshold —
explains both: a weaker canonical form inflates every level, and level 1 is deflated.

And it is not a threshold question. The cumulative orbit count of 2-element sets as the antisum
bound runs 0…9 is `1, 2, 6, 14, 29, 48, 63, 69, 70, 70` under S₇ and `1, 2, 5, 11, 21, 35, 48,
54, 55, 55` under the full automorphism group. **13 does not appear in either, at any
threshold.** For 3-element sets the count steps 280 → 1710 as the bound goes 9 → 11, straddling
377 without touching it.

Two by-products of the same hour:

* **Their 720× expectation for the canonical collapse was the wrong reference.** 720 is the
  *vertex count* of CO₇; the group a canonical form has available is S₇, order **5040**, acting
  transitively on those 720 vertices with stabiliser C₇ — and with reversal it is **10080**. So
  the measured 20.9× is short by **241×** against S₇ and 482× with reversal, not by 34×.
* **One re-reading fits the *shape* of both misses**: if their level 0 = 1 is the empty set, their
  level *k* holds *k*-element sets, and the canonical form is simply far from orbit-complete —
  13 singletons against **1** true orbit, 377 pairs against 70. That reading is self-consistent
  and it costs a level: a full (7,7) run then needs **three** more levels, not two, which is
  615,817 × 24.3³ ≈ **8.8 × 10⁹ nodes** against my 3.6 × 10⁸ — a 24× miss that moves their (7,7)
  run from 1–3 hours to **12–24 hours** and weakens my own conclusion that the stall was purely a
  budget finding.

`board-finder/gap/v4/verify_level_counts.py`, 15 assertions, all passing.

## 2. So this is not "the relay is slow"

The relay has been a *good* instrument for one thing and a bad one for another, and the record
splits cleanly:

* **Reasoning travels fine.** They found the over-strict pseudo-tightness predicate that had held
  155 objects under a wrong definition; I found the one-sided control (`D66`); they refuted four of
  my hypotheses; I corrected two of their numbers and conceded two of mine. All of that moved as
  prose and all of it landed.
* **Measurements arrive degraded.** Their 2–3× full-tree extrapolation compounded per-level
  ratios and had to be corrected to 1.30×. Their 720× expectation was the wrong group. Three
  rescue-ablation numbers were discarded by their own validity check. Their "(7,7) stalled" read
  as a difficulty finding and was a budget finding. My 38 hours divided by a *hardware* speedup.
  My 1.47 came from a two-point slope where least squares gives 1.42. And now two of five level
  counts do not reconstruct at all.

Every item in the second list is a **number about a run** rather than the run. That is the
channel, not either party: a summary of a computation cannot carry its index set, and without the
index set the arithmetic downstream is unanchored. Nine rounds of correspondence cannot fix that,
because the tenth round would also be a summary.

## 3. What the code buys, in priority order

1. **It identifies what the level counts count.** Twelve lines of their canonicalisation routine
   settle §1 outright, and with it the 24× ambiguity in the full-tree size and the 3×-vs-300×
   ambiguity in the throughput. This is currently unresolvable from either side.
2. **It makes the (7,7) positive control runnable.** This machine has 4 cores, 15 GB, 28 GB free
   and will run a **two-hour background job**; their calls are **100–300 s**. That is a 24–72×
   instrument gap before parallelism, and it is the whole reason the control has never completed.
   Completing (7,7) once and comparing wall-clock against Woodall's 4 hours pins the one input
   every cost estimate rests on — and it is the reproduce-then-extend gate both rubrics demand,
   attempted once, stalled on budget, never retried.
3. **It clears five caveats at once, all with one cause.** The (9,7) ablation unmeasured because
   its ON run aborted; the frontier 475,733-vs-288 split explicitly flagged as "a truncated-DFS
   artifact and not a measurement"; depths 6 and 7 at (7,7) unmeasured; the collapse factor
   measured on a truncated prefix tree; the control never completed. Every one of those is a
   **300-second wall-clock cap with no checkpointing**, and every one is removed by moving the code
   to a machine with a two-hour budget and adding a checkpoint.
4. **It promotes the provenance tier.** Everything in `P-43`'s outcome field is
   `SECONDARY-RELAYED`. Numbers produced by running their code here are
   `PRIMARY-VERIFIED-LOCALLY`. For a programme whose gates refuse `SEARCH-SUMMARY` that is not
   cosmetic — it changes what the numbers may be used for.

## 4. What the code does not buy, stated plainly

* **It does not buy the (11,7) sweep.** If their implementation is Python at ~10⁵ nodes/s, 4 cores
  here do not touch a 5–10 month job, and the ambiguity in §1 could make it worse. The sweep needs
  a compiled rewrite and a machine neither instance has. **The port gets the control; a rewrite
  gets the result.** They answer different questions and both are wanted, in that order — and the
  port must come first, because the quantity in dispute is a property of *their* tree, so a rewrite
  measures my implementation and leaves every existing number uninterpretable.
* It does nothing for the refutation branch (a different search entirely) or for K₉,₉, which is
  theory-shaped at 5.16 × 10¹⁵ and does not care about throughput.
* This container is ephemeral with a fixed disk allowance and is reclaimed on inactivity. A
  two-hour job is fine. A five-day job is not runnable here by anyone.

## 5. What to ask for

Not the repository — four things, smallest first, in this order:

1. **the canonicalisation routine**, verbatim, and the predicate that decides whether a node is
   kept — this alone settles §1;
2. **the search driver**, enough to re-run (7,7) end to end, plus whatever the level counter
   increments, since §1 turns on exactly what gets counted;
3. **the raw output** of the runs already reported — not the summary, the file;
4. **the (4,6)-set certificate** in whatever form their program emits, so the port has a positive
   control before it is trusted on anything new.

Two constraints on how this is asked. **Where it lands is your call, not mine** — it is their
work and their container. And the request itself has to stay leak-free under `D57`(ii): it names
the code, never a destination, a path, or an identifier. A paste-ready version:

> Before any further analysis I would like to run your program rather than reason about its
> output, because two of your five (7,7) level counts do not reconstruct here. Taking 2-element
> sets of cyclic orders on 7 points with antisum at most 3, up to ground-set relabelling, I count
> **14** classes where you report 13 — and no antisum threshold gives 13 under either the
> relabelling group alone (order 5040) or that group with reversal (10080). At 3-element sets with
> antisum at most 9 I count **280** (or 158 under the larger group) where you report 377. One miss
> is high and the other low, so a single cause does not cover both. Could you send, in this order:
> your canonicalisation routine and node-keep predicate; the search driver and the line that
> increments the level counter; the raw output files of the runs you have already reported; and the
> (4,6)-set certificate as your program emits it? Separately — one number worth re-checking: 720 is
> the vertex count of CO₇, not a group order. The relabelling group is S₇ of order 5040, acting
> transitively on the 720 vertices with stabiliser C₇, and reversal doubles it to 10080. So the
> ceiling your 20.9× collapse should be measured against is 5040, and the shortfall is 241×, not
> 34×.

## 6. The counterweights

**The mismatch could be mine.** My CO₇ comes from the construction that reproduced Woodall's
published *n* = 4 antidistances and the 131 isomorphism classes at *n* = 5 and verified the
(4,6)-set end to end — but the extension to *n* = 7 is validated against no published *n* = 7
figure, and my reading of the prefix staircase as a condition on canonical sets is itself an
interpretation. I have scanned both admissible groups at every threshold, which is what `D66`
asks for, and that is as far as this side reaches. **Which is the argument, not a hedge:** two
implementations disagree and neither can be audited from the other's summary.

**There is a real cost, and it is mostly already spent.** The relay's value was that two instances
held *different* artefacts: the over-strict-predicate catch and the one-sided-control catch each
happened because neither side could see the other's work. Taking their code ends that
independence. But the remaining questions are not cross-check questions — they are measurement
questions, and a measurement needs one instrument, not two blinded parties. The independence was
worth more at round 2 than it is at round 9.

**And a rewrite might dominate a port.** If their code is a 300-second-shaped Python script, the
honest outcome of reading it may be "reimplement this", with the original kept only as the oracle
for the positive control. That is still a reason to have it.

## 7. Register effects

* `P-43`(A) is **at risk for a third and independent reason**: not Theorem 7, not implementation
  throughput, but that the sequence both estimates are computed from does not reconstruct at its
  two checkable terms. **H is unaffected and stays PASS** — at every tree size considered, 10⁸ to
  10¹⁰, the target is reachable, which is what H asks.
* `D67` registers the channel finding: a relay transports reasoning and degrades measurements,
  because a summary of a computation cannot carry its index set.
