# Costas arrays, order 32 — the action plan, with the bar registered before phase 0 runs

**30 Sep 2026.** Reopening a cell this board already failed. The analysis behind this is
`ANALYSIS_CPRO1.md`; the structural computations are `costas_support.py` / `VERIFIED_OUTPUT.txt`.

> **[CLOSED the same day, `../gap/discovery/RESULT_D_COSTAS.md`.] Phase 0 ran, the bar FAILED on
> clause (a), and P-37 is CORRECT — but the plan's own premise was falsified and that is the real
> result.** §2 below claims order 31's arrays are "necessarily sporadic" and builds a 5.00-bit
> positive control on it. They are **W₀ arrays** — a Welch *p* = 31 array with a corner dot **added**
> — and I had modelled corner *deletion* only. Re-verified locally: exactly 8 under the dihedral
> group, matching the relayed count to the digit, and the run's explicit array lies in that class.
> **So the control does not exist**; the nearest search frontier is order 22–23, **43.21 bits** below
> the target, not 5.00. **Phase 1 is not run.** The cell closes on measured evidence — everything near
> the frontier is constructible and orders 32/33 are where no construction lands — rather than on the
> bar. Left standing below, unedited except this box, because the failure is in the *inference* from a
> correct computation and that is the finding. Debt **D53**.

---

## 1. Why reopening is legitimate rather than a re-scope

`../gap/discovery/RESULT_B2_SEQUENCES.md` returned **Costas: FAIL at S3**, and the reason it gives is
*"method unread → UNKNOWN"*. That is an **access failure, not an evidence failure** — the
aimsciences page returned abstract and references only. It is one of the six consecutive S3 failures
that debt **D50** was opened for: *"a long run of FAILs reads as a well-screened empty seam and may be
a well-documented paywall."*

**So this is not softening a threshold after the fact.** D44 forbids redrawing a bar once the answer
is in; it does not forbid re-running a gate whose input was never obtained. The distinction is
recorded here so the next reader can check it: S1 **passed** (existence frontier, route (a)), S4
passed, and S3 died on access. Nothing in B2 constitutes evidence against the cell.

Two further things B2 established that stand and are not revisited:

* the record is **the smallest order with no known Costas array = 32**, and 32/33 are the two
  smallest such orders. The **enumeration** frontier is 29 and is a different quantity — I conflated
  the two when writing B2's brief and the run corrected me. Order 32 has never been exhaustively
  searched and the order-29 enumeration reportedly cost **366.55 CPU-years**.
* **CPro1 attempted Costas in 2025 and moved nothing** (D51). That fact is the reason for caution and
  is not neutralised by anything below.

## 2. What the local computation adds, and it is the whole reason to proceed

`PRIMARY-VERIFIED-LOCALLY`, from `costas_support.py`:

> **Orders 31, 32 and 33 receive zero arrays from any Welch or Golomb generator at any
> corner-deletion depth**, because the prime gap 31 → 37 leaves no prime in [32,36] and no prime
> power in [33,36]. **Order 31 nonetheless has ≥ 8 known arrays** (relayed), so those are necessarily
> **sporadic** — found by search, by somebody, with no algebraic scaffold.
> **log2(31!) = 112.66, log2(32!) = 117.66, a gap of exactly 5.00 bits.**

That gives this cell something no other candidate on this board has ever had: **a positive control
five bits from the target, on the same object, under the same absence of structure.** Every gate this
project has run failed for want of a measurable handle on difficulty. Here there is one.

It also sets the calibration test that CPro1 never applied, and which is the core of phase 1.

## 3. The plan. Sonnet first, and Opus only through a gate.

### Phase 0 — one Sonnet 5.5 chat conversation, ~18 calls. Structural reconnaissance, not search.

Prompt: `../gap/discovery/prompts/s55/D_COSTAS.md`. It asks five questions, ordered by decision value,
and **none of them is "find a Costas array."** All five are reads. The reason Sonnet does this and not
Opus is the tier finding in `../gap/TIERS_2026-09.md`: *bar design and adjudication are Opus, bar
execution and breadth are Sonnet.* Phase 0 is execution against a bar written here.

The five questions:

1. **How were the order-31 sporadics found?** Exhaustive search, a structured partial search, or a
   heuristic? This is the single most decision-relevant fact available and it is a citation, not a
   computation. If heuristic — a working method sits 5 bits from the target. If exhaustive — then the
   community reached 112.7 bits by brute force with large compute, and 117.7 is not 5 bits away in
   any useful sense.
2. **Is there a published structural characterisation of sporadic Costas arrays?** Drakakis and
   co-authors have a body of work here. Symmetry, shift-sequence structure, proximity to algebraic
   arrays — anything that constrains the space is the lever the whole attempt depends on.
3. **Has a heuristic (non-exhaustive) search at order 32 been run and reported as failed?** D51's
   middle state. This is the question that kills the cell if answered yes.
4. **What is the best published heuristic result on Costas arrays** — did anyone reach order 30 or 31
   that way, and at what cost?
5. **Do the counts and the order-31 figure hold up?** C(29) = 164, ≥664 at order 30, ≥8 at order 31,
   32 and 33 the two smallest unknown orders. All relayed; one of them anchors §2.

### The bar, registered now, before phase 0 is dispatched

> **PASS iff both of the following hold:**
> **(a)** a published structural characterisation of sporadic Costas arrays exists that constrains the
> search space — not merely a list of them, and not merely the observation that they exist; **and**
> **(b)** no report can be found of a heuristic search at order 32 having been run and failed.
>
> **FAIL on either.** On FAIL the cell is *attempted-and-failed with no structural lever* and Opus is
> not spent on it. A bar that cannot be evaluated is FAIL, not unscored.

**Note what this bar does and does not do.** It deliberately does *not* make question 1's answer a
gate condition, because either answer is informative and I do not want to be able to read the
threshold off the evidence afterwards. Question 1 sizes the attempt; (a) and (b) decide it.

**And note the asymmetry with C-1 and C-3, since this board has now made the same mistake twice.**
C-1's bar made a prior attempt a PASS condition; C-3's made it a FAIL condition; S4 could not see it
at all. **This bar makes a prior *heuristic* attempt at the *target order* a FAIL condition, and says
so in one clause** — narrower than C-3's "attempting the neighbourhood," because CPro1's attempt on
the design type is already known and is not being double-counted as fresh evidence.

### Phase 1 — Opus 5.5 in Claude Code, only if the bar passes

Two things are pre-registered about phase 1 so it cannot be graded on a moving target.

**The calibration gate, which is CPro1's missing control.**

> The positive control is **rediscovering a known sporadic array at order 31 from scratch**, with the
> known arrays withheld from the search. Not "finding a Costas array at a small order" — the
> algebraic families make small orders free, so a search that finds order-20 arrays has demonstrated
> nothing about order 32. **A method that cannot recover an order-31 sporadic is not pointed at
> order 32.** This is one measurement and it is cheap relative to the run it gates.

**The search brief must carry the structure CPro1's did not.** CPro1's Table 5 handed its model the
raw permutation definition only. Phase 1's brief carries the Welch and Golomb generators, corner
deletion, the verified `is_costas()`, whatever characterisation phase 0 question 2 turns up, and the
explicit fact that orders 31–33 have no algebraic support so the target is sporadic by construction.

Budget shape, for comparison against CPro1's: CPro1 spent 1000 candidate programs and 48 hours per
open instance, across 16 design types. Phase 1 is one design type, one order, with the order-31
control as the stopping test.

## 4. The counterweight, recorded at the same time as the plan

This belongs next to the plan and not in a footnote, because the plan will look better in hindsight
than the evidence warrants if it is recorded alone.

1. **The state of the art for Costas is backtracking DFS, which is exactly what an LLM writes.** There
   is no algorithmic gap to discover here — the community's version has decades of tuning and 366.55
   CPU-years behind order 29. CPro1's generated strategies included DFS, so the model already found
   the right algorithm and it was not enough.
2. **CPro1's failure on Costas fits the paper's own §5 pattern** — heavily-worked design types with
   purpose-built computational attack. That pattern is a prediction about *this* cell and it predicts
   failure. The budget criticism that rescues CPro1's cap-set failure does not obviously transfer.
3. **Non-existence at order 32 is possible and no constructive search can settle it.** If C(32) = 0
   the entire attempt is unfalsifiable from the inside: it returns nothing and we cannot distinguish
   that from having searched badly. **This is the asymmetry that makes the order-31 control
   mandatory** — the control is the only thing that can tell those two apart.
4. **The 5-bit gap cuts both ways.** Order 31's sporadics were found and order 32's were not, at a
   difference of one order and a factor of 32 in space. Either 31 was much easier than it looks, or
   order 32 has already absorbed more search than is documented. Phase 0 question 3 exists to find
   out, and a yes there is fatal.
5. **D47 stands: three bars on this board tested crowding and crowding decided none of them.** This
   bar is not a crowding bar — it is a structural-lever bar — which is a deliberate change of
   observable, and it may fail for its own new reasons.

## 5. Registered prediction

**P-37. SCORED CORRECT** — the bar failed on clause (a), for the predicted reason: sporadic arrays
turned out to be catalogued, not characterised, with Drakakis's own open-problems paper saying almost
nothing is known about them. **A correct prediction that was nearly irrelevant**, since the cell was
decided by evidence neither clause asked about.

Registered before phase 0 ran:

> **Predicted:** phase 0's bar **FAILS**, on clause (a) — no published structural characterisation of
> sporadic Costas arrays that constrains a search will be found at `SECONDARY-RELAYED` or better.
>
> Scoring: PASS on (a) with a citation the run actually read falsifies this and is the more valuable
> outcome. A FAIL on (b) instead of (a) is a **different** result and is scored as such, not as
> confirmation.

My reason for predicting FAIL is §4.1: sporadic arrays are defined by the absence of structure, and
the literature's word for them is "sporadic". I expect the answer to be that they are catalogued, not
characterised. **If that is right, the plan stops at phase 0 for the cost of one chat conversation,
which is the point of ordering it this way.**
