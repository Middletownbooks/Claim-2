# Handoff — fallback queue, for a fresh instance

Written to be executed without re-deriving anything. Work top to bottom and **stop at the first
FAIL**. Every step names what to do, what decides it, and what to do on each outcome.

## What you are inheriting

- **Primary target, not yours:** Hadamard order 2092 — `../hadamard/PLAN_2092.md`. Do not start
  it; it is being tested separately.
- **Your job:** run the gate in `GATE_FALLBACKS.md` on one candidate, CC-6 / MOLS(12). If it
  passes, the fallback queue has one item. If it fails, the queue is empty and that is a real
  answer — see `RESULT_500_RESCAN.md` §3 for why it is the expected one.

## Rules that are not negotiable, because each cost this project something

1. **Verify objects, never function returns.** A search that reports success is not a solution;
   reconstruct the object and check every defining condition. (A "found W(103)" once cost a day.)
2. **Positive controls before nulls.** A search that cannot find a *known* object proves nothing
   when it finds none. For MOLS: your code must reproduce **5 MOLS(12)** and **2 MOLS(10)** from
   published data before any null is reported.
3. **Negative-test every check.** Break it on purpose and confirm it fails. Two checks written in
   one day here could not fail at all — one from a regex escape, one from a mis-scoped predicate.
4. **Register predictions before running, single threshold, no middle band.** A two-sided
   prediction with a gap declines to score (D44).
5. **Seven seeds, matched caps, medians** for any timing claim. Single-seed timings here were
   bimodal and every one taken before that was discovered was unsafe.
6. **Nothing is "clear" because it is absent from a list.** The three curated lists in play
   overlap pairwise at 5–20% (`RESULT_500_RESCAN.md` §3).

## Steps

**1. F1 first, not F0.** It is the cheapest and it can void everything else. Find a dated source
for the MOLS lower-bound table; confirm **N(10) = 2** and **N(12) = 5**; record when each was last
improved. Write `evidence/F1_mols_table.json` with `{n, known_lower_bound, source, dated,
last_improved}`. **If either figure is wrong → STOP and report.**

**2. F0.** Screen "6 MOLS of order 12" against the 41 entries in
`../gap/sources/EPOCH_UNSOLVED_LIST.md`, using the adjudicate-every-collision discipline in
`../gap/epoch_gate.py`. Expect the same near-miss it found for C1 — *Large Steiner Systems*, which
is design theory and is **not** MOLS. **Collision that survives adjudication → STOP.**

**3. F2, the one that matters.** Build the search: given five MOLS(12), find a sixth Latin square
orthogonal to all five. Cost it — enumeration count, measured rate on this machine, fraction of
the region an hour buys. **Report the model before running the search.** ≤ 10 container-hours →
pass; otherwise **STOP**.

**4. F3.** What have published searches already covered for *N*(12)? If they cover ≥ 10× your F2
region, **STOP**.

**5. F4.** Confirm a null extends the published table. Then write `RESULT_FALLBACKS.md` with every
bar's verdict and the evidence file behind each.

## If everything passes

Pre-register before searching: predictions with single thresholds, the positive controls from
rule 2, and the failure condition — *what result makes you abandon this and say so*. Then run.

## If anything fails

Say so plainly, commit the evidence, and stop. The queue being empty is the expected outcome of
a rescan whose own §3 shows the corpus is orthogonal to the screen. **Do not go looking for a
replacement candidate in the same corpus** — that search has been run and its result is in
`RESULT_500_RESCAN.md`.

## Where things are

```
board-finder/fallbacks/   screen_500.py  RESULT_500_RESCAN.md  GATE_FALLBACKS.md  this file
board-finder/gap/         Epoch exclusion set, epoch_gate.py, the v2 gap analysis
board-finder/pte/         a worked example of the whole discipline, including two failures
board-finder/hadamard/    PLAN_2092.md -- the primary target, not yours
```

`../pte/` is the best model to imitate: pre-registration, harness committed before data,
negative tests, a scorer that reports NOT-SCORED rather than a pass, and a verdict that closed
the target on arithmetic rather than on a test firing.
