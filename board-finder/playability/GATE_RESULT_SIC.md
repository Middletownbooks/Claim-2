# Gate result — record 235 is killed, by the condition set before it ran

Response verbatim in `sources/GATE_SIC_RESPONSE_RAW.md`. Tier SECONDARY-RELAYED: this session
fetched none of it.

## 1. The verdict, and the pre-registered consequence

**`PREFIX`. Hole list: EMPTY.**

Exact fiducials cover every dimension up to **53** (safe floor) or **57** (probable, and the
respondent flagged the disagreement rather than picking). The 2017 holes — 22, 23, 25–27, 29,
32–34, 36, 38, 40–42, 44–47, 49–52 — **are filled**, between roughly 2021 and 2024.

`TARGET_DECISION.md` §6 said, before the gate ran: *"The gate comes back 'clean prefix' → 235
is depth; fall back to 495 and re-run this ranking."* So **235 is out.** Not renegotiated, not
softened: the condition was written down first and it fired.

Above ~57 the exact set is sparse and structured — n²+3 families, Fibonacci–Lucas, dimension
towers — so the unknown set is an **open tail**, not a finite list of oversights. And the field
is actively worked: a Grassl seminar dated **three days ago**, a Bengtsson–Grassl preprint in
Dec 2025, the Appleby–Flammia–Kopp paper under submission with code published, Kopp–Lagarias
revised May 2026. Pushing the prefix upward means competing directly with the people who own
the tooling.

## 2. What I checked myself

Only the arithmetic is checkable without fetching, and it is consistent:

* 19603 = 140² + 3, and prime → fits *"prime dimensions n²+3"* (arXiv:2112.05552)
* 39604 = 199² + 3 = 4 × 9901, 9901 prime → fits *"n²+3 = 4p"* (arXiv:2403.02872)
* 487 = 22² + 3, prime → the one dimension that paper verified **fully** exactly
* 5799 − 3 = 5796 is **not** a square → the exact ceiling comes from a different family,
  consistent with the report's account

This confirms the dimensions cited have the stated form. It does not verify any SIC property.

## 3. The prompt earned its cost, and the Opus call was right — measured in §C

The two traps `PROMPT_GATE_SIC.md` was built around both fired **in the respondent's own
recall**, and the search caught both:

| its prior | outcome |
|---|---|
| exact known for d ≤ 21 plus scattered 24, 28, 30, 31, 35, 37, 39, 43, 48, 124, 323 | **CORRECTED** — that is the 2017 table. *"Recall was nine years stale and would have produced an entirely fictitious hole list."* |
| maximum exact dimension ≈ 39604 | **CORRECTED** — 39604 is the **numerical** maximum; the exact ceiling is 5799, and the papers reaching 19603/39604 *"admit their exact verification was mostly partial"* |

Read that first row again: **unsourced, this gate would have produced a hole list that does not
exist**, and a Claude Code programme would have started work against fictitious targets. That
is the W(103) failure mode — a confident, plausible claim about a finite object — caught
prospectively this time instead of a day late.

The second row is the numerical/exact conflation, which is exactly why the prompt led with the
three-claims section and tightened the quote rule. It fired in recall and was caught in source.

Three things the respondent did that the design asked for and that a weaker pass would plausibly
have skipped: it flagged the **53 vs 57** disagreement instead of picking; it refused to name
PSLQ vs LLL because the source says only *"an integer relation algorithm"*; and it named the
**Flammia table** as *"the fossil that keeps the 2017 picture alive at the top of search
results"* — the specific mechanism by which this field's stale recall is manufactured.

## 4. The screen needed a third category, and this is it

`FEASIBILITY.md` §6 split targets into **deep** and **broad**. That is one distinction short.

| shape | unknown set | example | agent-shaped? |
|---|---|---|---|
| deep | one pipeline pushed further | Jones unknot, snark generation | no |
| **broad, finite list below a ceiling** | a specific enumerable set of holes | **Hadamard: 13 open orders in 2000–3000** | **yes** |
| **broad, prefix + open tail** | unbounded | **SIC: everything above ~57** | **no** |

The last two are indistinguishable under "is the remaining work a hundred small things?" — both
are per-instance searches with identical structure. What separates them is **whether the
unknown set can be written down.** Hadamard's could: thirteen numbers. SIC's cannot.

So the operating rule gains a clause: *look up the frontier to find out whether the remaining
work is deep or broad —* **and if broad, whether the unknown set is a finite list or a tail.
Only the finite list is a target.**

## 5. A correction to the sweep, verified here

`REPORT_SWEEP.md` §6 relayed, on record 280 Kaplansky: *"a zero-divisor counterexample would
automatically hand you an idempotent counterexample too."* **The implication runs the other
way.** If e² = e with e ∉ {0,1} then e(1−e) = 0 with both factors non-zero, so a nontrivial
**idempotent yields zero divisors** — not conversely. Witnesses: in ℤ/6ℤ, e = 3 and e = 4 are
nontrivial idempotents giving zero divisors; ℤ/4ℤ and ℤ/9ℤ have zero divisors and **no**
nontrivial idempotent.

The conjectures nest unit ⇒ zero-divisor ⇒ idempotent, so **idempotent is the weakest claim and
its counterexample is the strictly hardest object.** The Bar-Ilan lab on the zero-divisor search
is therefore working the *easier* target, not a superset that would hand an idempotent
counterexample over for free. That **demotes 280 further**, for a reason the sweep had backwards.

## 6. So: no first target survives, and that is the honest answer

Applying the corrected screens to FEASIBLE ∧ unworkspaced:

| rank | verdict |
|---|---|
| 132 congruent number | out — mechanism class `d`, no finite witness settles the ranked target |
| **235 Zauner SIC** | **out — prefix + open tail, and actively worked** |
| **280 Kaplansky idempotent** | **out — the weakest conjecture, so the hardest witness; §5** |
| 401 KL invariance | out — depth, and heavily ML-worked |
| 495 list edge-colouring | the nominated fallback, but it is a counterexample hunt in an unbounded space with no finite hole list — **the same defect that killed 235** |

**The set is exhausted.** 495 does not survive its own promotion, because §4's new clause
applies to it too. Reporting that plainly is better than promoting the next name on a list:
the sweep's own headline was *10 playable now of 499*, and the corrected screens say the
intersection of *playable ∧ unworkspaced ∧ finite-list-below-a-ceiling* is **empty** in this
corpus.

That is not a failure of the sweep. It is the sweep working: four of five candidates were
eliminated by facts that cost an afternoon each to establish, and none of the eliminations
needed a programme to discover.

## 7. The one thing the gate did surface, offered as what it is

§B flags a real gap that is *not* a research result: **the exact vectors for the filled holes
22–52 may not be publicly available anywhere.** Kopp 2021 called d=53 unpublished; the
respondent found no repository hosting those fiducials; there is **no maintained,
submission-accepting SIC database** at all.

That is a finite list below a ceiling — the one agent-shaped category — and the deliverable is
verifiable in seconds by the checker in `TARGET_DECISION.md` §3. But be clear what it is: **data
recovery and publication, not a new theorem.** Nobody is competing for it because it is not a
result. If the project wants a useful, uncontested, completable artifact rather than an open
problem, this is the one on the table.

And §B names something cheaper than any of it: *"asking Grassl or Flammia directly — this is a
small field and the answer is one email away, which is cheaper than anything I or your
programme can compute."* That is almost certainly right.
