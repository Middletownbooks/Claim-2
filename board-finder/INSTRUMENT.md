# The board-search instrument — design notes

**The pasteable prompt is `PROMPT.md`.** This file is why it says what it says. The
prompt there is self-contained and carries no reference to this programme's internal
vocabulary: a respondent should never see `D25`, a kappa, or the names of the papers the
design was derived from, because two of those would leak the answer and the third would
mean nothing to them.

*A second instrument, deliberately **not** an extension of v2.1. Two reasons, both
measured: Phase V found the heaviest prompt produced the sloppiest derivation, and the
two jobs have opposite failure modes — **verification fails by accepting too much,
search fails by generating too little**. v2.1's spine is "don't claim what you haven't
proved", which is correct for verification and actively suppresses the generative
behaviour wanted here.*

*So this instrument does not ask for caution. It asks for candidates, and it makes each
one cheap to kill. Keep it short: every paragraph added to a prompt in this programme
has cost derivation quality.*

---

## The prompt

> You are given the state of a problem **before** a known advance. Do not look for the
> advance. Produce candidate boards, and make each one cheap to kill.
>
> **Step 1 — reconstruct the board, five slots.** State; move; invariant; composition;
> terminal certificate. Say "none recorded" where the source has no such slot. Do not
> smooth over a missing slot.
>
> **Step 2 — build the leak table.** For **each** log, dimension or iteration factor in
> the current bound, one row: the factor, and **the exact mechanism producing it**.
> "Roughly log n from the analysis" is not a row. "√log n from the union bound over n
> sets" is. If you cannot name the mechanism, write `MECHANISM UNKNOWN` — that is a
> result, not a gap to paper over.
>
> **Step 3 — classify each leak, one of three.**
> `ACCUMULATION` — the factor equals (rounds or items) × (per-step cost).
> `SATURATION` — the invariant caps at a value independent of the parameter being pushed.
> `WRONG_STATISTIC` — the invariant measures a quantity that is not the one being bounded.
>
> **Step 4 — one transformation per leak, from the catalogue, with its diagnostic run.**
> De-tensorize (compute I on a product); auxiliary-witness lift (is the invariant hard to
> transport, easy to re-derive?); move work terminal ↔ step (which end carries the
> weight?); collectivize a union bound (does the loss equal m × per-item cost?);
> formula-ize the move (does a legal move need an existence theorem?). **Run the
> diagnostic and report the number**, not the intention.
>
> **Step 5 — triage every candidate. These two decide it.**
> **T1. Can the invariant be verified on the starting state by an independent
> computation, without knowing whether the target theorem is true?** If no, you have
> produced a restatement of the conjecture, and you must say so.
> **T2. Is the legal move a formula, or does it require an existence theorem?** If a
> theorem, name it and say what it costs.
>
> **Step 6 — for every impossibility claim you make, three required fields.** (a) the
> enumerated class of certificates; (b) **one named functional outside it**; (c) the
> argument that the class is closed. A claim missing (b) is an unchecked quantifier,
> not a negative result.
>
> **Step 7 — say it yourself.** For each candidate: does it *remove* the obstruction or
> *relocate* it? You get credit for answering honestly.
>
> Output the five slots, the leak table, one candidate per leak with its diagnostic
> number, the T1/T2 verdicts, and the Step 7 self-assessment. Nothing else.

---

## Why each step is there

| step | the failure it is built against |
|---|---|
| 2, the leak table with mechanisms | *"the quantifier doing the real work left unchecked"* — the programme's recurring failure. A named mechanism is a checkable object; "roughly log n" is not |
| 4, run the diagnostic | the five labels scored **κ = 0.048**, and one rater applied de-tensorize *backwards*. The computation does not need the word |
| 5, T1 | all four models found the same board; **one proved it exists iff the conjecture holds** and reported that as a find. T1 is what separates a board from a restatement |
| 6, enumeration completeness | a confident impossibility claim (*"forces the certificate to factor through the subgaussian comparison"*) was contradicted by a paper **five days older**. Directional total variation is an L¹ derivative norm, outside the class that claim enumerated |
| 7, self-assessment | **three of four** responses reported, unprompted, that their own candidate relocated rather than removed the obstruction. It is a reliable signal, so ask for it |
| the brevity | Phase V: the heaviest prompt produced the sloppiest derivation |

## How a run is scored

On `benchmark.json`: the two discriminators as the primary outcome, the positive
control (Banaszczyk — real board, checkable invariant) and the **negative control**
(the convolution compiler — an invariant provably equivalent to the theorem, whose
correct answer is *decline and say why*). A rubric that cannot separate those two is
not measuring board-finding.

Read the **recognition probe first**. If a proposer names the problem, D25 applies:
a rule-less rater already ceilings the retrospective arm at J = 1.000 with 13/13
recognition, so a hit tells you the model remembers Ellenberg–Gijswijt. The negative
control is the one item recall cannot crack, which is why it carries the experiment.

**Not run here** — no API key in this container, the same wall as debt D18. What is
finished is everything that does not need one: the prompt, the required fields, the
controls, the scoring rule, and the diagnostics with their known answers.
