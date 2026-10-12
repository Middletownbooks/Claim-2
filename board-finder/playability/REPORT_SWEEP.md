# Report — the frontier sweep, adjudicated

Instrument: `PROMPT_SWEEP.md` Part A. Executor: a Claude chat surface with web search,
no repo access. Raw reply verbatim in `sources/SWEEP_RESPONSE_RAW.md`; parsed by
`parse_sweep.py` into `frontier_sweep.json`; merged into `classification.json` by
`classify.py` so a regeneration keeps the sourced values instead of reverting to the
`[recall]` ones.

**23 of 23 records returned.** 14 CONFIRMED, 9 CORRECTED. The quote supports the cell in
19, partly in 3, and **not at all in 1**.

**Provenance, stated once and applying to everything below:** this session fetched none of
these pages. Every URL, date and quote is **relayed**, tier `SECONDARY-RELAYED`. One row is
the exception and it is the most important row in the sweep.

## 1. The one cell verified here rather than relayed — and it overturns a HOPELESS verdict

**488b.** Sieved locally: **π(3159) = 446**, and **p₄₄₇ = 3163**, exactly as the quoted
Engelsma theorem says. So an admissible 447-tuple of diameter 3158 spans 3159 consecutive
integers and contains 447 elements against π(3159) = 446 — **a violation with margin
exactly 1.** Under the prime k-tuple conjecture that refutes the second Hardy–Littlewood
conjecture.

This is the factor `FEASIBILITY.md` §1 said was skipped. The sweep run in this repo pushed
**x** and found the margin growing hopelessly; the question is decided in **y**, and the
deciding object was already tabulated in 2005. `488` keeps its HOPELESS verdict for the
direct sweep and gains `subTarget: 488b` at **FEASIBLE** — kept as a sub-target rather than
re-rating the record, because only one of its two factors is feasible and collapsing them
would be the inflation §3(d) warns about.

The recalled *"past y ≈ 1600"* was **1.97× optimistic**. And a caution against my own first
explanation: I tried to justify why 447 is the first witness with the crude bound
H(k) ≳ k ln k, and it does not — at k = 300 that bound sits at 1711 against p₃₀₀ = 1987, so
it fails to exclude a smaller witness. Why 3159 is first needs the actual H(k) table, which
I do not have. The margin-1 violation is verified; the *"why there"* is not.

## 2. The registered prediction is confirmed — and confirming it kills the recommendation

`RANKING_FIT.md` §4 predicted: *if the four finite-group block conjectures are as checkable
as this reads, someone has already swept the small groups and the sweep is published.*

Swept and published, all four. But two went further than a sweep:

| | status |
|---|---|
| **287 Alperin–McKay** | *"Theorem A. The Alperin–McKay conjecture holds for the prime ℓ=2."* |
| **472 McKay–Navarro** | *"We complete the proof of the McKay–Navarro conjecture … for the prime 2"* |
| **356 Brauer k(B)** | sweep published; sporadics + Tits + A₆/A₇ + exceptional covers done **directly from GAP character tables** |
| **300 Alperin weight** | sporadics swept; general case sourced as *"out of reach"* |

**So the four records rated the best neglect-to-checkability ratio on the whole board are
the ones where the literature had already finished the job** — at ℓ=2, for two of them, by
proving the theorem. A counterexample search cannot succeed against a theorem, so 287 and
472 are re-rated **BOUNDED → NARROWED**: the witness target survives only at odd primes,
where the inductive condition is still incomplete.

That is the pre-registration doing exactly what it was for. The branch it called "the more
interesting one" was the absence; the branch that fired was the presence, and it retires the
recommendation rather than endorsing it. **300 is now the only one of the four still open in
the shape the record assumed.** The pre-registered low confidence on **356** was also
vindicated in the right place: it was about the *mechanism* — a minimal-counterexample
argument, not a normalizer-compatible bijection — and that flag was correct while the sweep
itself turned out to exist.

## 3. Three cells where the quote does not carry what the cell says

The rule was *a verbatim sentence containing the number*. Applied strictly:

- **500 Lehmer's τ — the quote does not contain the claimed number.** The quote gives
  n < 982,149,821,766,199,295,999 (2013). The cell claims 816,212,624,008,487,344,127,999,
  which is **831× larger** and whose source the respondent said it could not pin down. By
  the prompt's own rule the sourced frontier is the quoted figure; the larger one is recorded
  as unsourced. The respondent flagged the discrepancy honestly, which is why this is a
  clean catch rather than a silent error.
- **307 Legendre — the quote is about Oppermann's conjecture, not Legendre's.** Oppermann is
  strictly stronger, so verifying it to 7.05×10¹³ does verify Legendre to that bound. The
  inference is sound, but it *is* an inference, and a later reader must not think the quoted
  sentence names Legendre.
- **348 Beal — the quote sources the search bound, not the null result.** It establishes
  C^z ≤ 2¹⁰⁰ and reports a min/gcd statistic; it does not say no counterexample was found.

## 4. Two mechanism claims in the record were wrong, and both were mine

- **355 Tutte 3-flow → NOT-A-SEARCH.** The record said *"as for the 5-flow: structured graph
  generation, known wall."* It does not reduce to snarks and has no finite-checkable
  reduction; it reduces to 5-regular graphs and is chased by edge-connectivity theorems
  (8 → 6, target 4). Grouping it with the 5-flow was my inference and it was wrong.
- **79 Hadwiger.** *"Minor-closed structure cuts the candidates"* describes **Linear**
  Hadwiger, which does have a finite-check reduction. The exact conjecture has none beyond
  t ≤ 6, and t = 7 is sourced as *"out of reach at the moment."*

## 5. The Hadamard claim is overstated, and a screen this project built rests on it

**331: DEMONSTRATED → ANNOUNCED-UNVERIFIED.**

What is established: a real, independently covered announcement (John D. Cook, 13 Aug 2026;
Chinese tech press the same window) crediting Levent Alpöge, two collaborators and Claude
with an order-668 matrix and *"all remaining gaps below 2000"*. The user reported this
first-hand, and that report stands.

What is **not** established: verification. `epoch.ai`, one of the two sources the record
itself names, still lists order 668 as unsolved; a separate account has another researcher
failing to reproduce a 668 matrix that same weekend. `DEMONSTRATED` asserts an agent produced
*verified* witnesses at multiple open parameters. The sourced status is *announced*.

**This matters beyond one cell**, because `FEASIBILITY.md` §6 used that reclassification as
the evidence for its best screen — *specialists saturate depth, not breadth*. The screen's
**reasoning** survives untouched: it is an argument about where specialist compute lives, and
it does not need this weekend to have happened. Its **headline evidence** is weaker than
recorded, so the screen should be carried as a well-argued heuristic and not as a heuristic
with a demonstrated win behind it.

## 6. What moved, what is frozen

**Moved recently, unprompted by us:** snark generation 36 → 38/40 vertices on a 14–29×
faster algorithm (March 2026), Collatz 2⁶⁸ → 2⁷¹ (2025), Legendre 2×10⁹ → 7.05×10¹³ (2024),
Voronoi d = 5 closed (Inventiones 2025). Four frontiers this project had recorded at stale
values.

**Frozen:** odd perfect numbers at 10¹⁵⁰⁰ since 2012, Beal at 2¹⁰⁰ since 2010. Both are
class (c) records whose entire value was the frontier, and in both cases the frontier has not
moved in over a decade — which is the answer to whether the next push is cheap.

**Disputed, flagged not filed:** 458 Erdős matching. A single-author preprint claims a full
proof (Feb 2026, fifth revision by mid-March); a community tracker reports a specific gap on
page 11. Recorded as disputed, and the range-by-range list is kept as the safe answer.

**280 Kaplansky survives but changes shape.** The Gardam citation is confirmed exactly. But
the chain is unit ⇒ zero-divisor ⇒ idempotent, and Promislow's group is known to satisfy the
zero-divisor conjecture, so Gardam's counterexample yields **no** idempotent one. The live
target is the intermediate zero-divisor conjecture — and an AI-algebra lab is already
pointed at it, which changes the neglect calculus the recommendation rested on.

## 7. What the `[recall]` tag is worth — the number nobody had

§C, answered last, is the first measurement in this project of how far unsourced cells can be
trusted. The executor's own accounting, before searching: **≈7–8 would have been confirmed,
6 corrected, 7 no prior at all.**

Read against the sweep's outcome — 9 of 23 CORRECTED — that self-report is roughly calibrated
rather than optimistic, which is itself worth knowing. The misses cluster in one place, and it
is not random: **every heavy miss was a post-cutoff event.** Two 2025 theorems it would have
called open programmes, two frontiers superseded in 2025–26 that it would have quoted at the
old value, and zero prior knowledge of either the Aug 2026 Hadamard announcement or the Feb
2026 matching-proof dispute — the two cells needing the heaviest hedging in the whole sweep.

**The operational rule that follows:** a `[recall]` cell about a *stable mathematical fact* is
usually fine. A `[recall]` cell about **where a frontier stands** is unreliable in exactly the
direction that matters — it reports the last value the model saw, which is systematically
stale, and stale in a way that reads confident. This project's `[recall]` tags were applied
overwhelmingly to frontier values. That is the wrong half to have guessed.
