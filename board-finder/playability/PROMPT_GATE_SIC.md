# The gate prompt — record 235, Zauner / SIC existence

One question decides whether the target is worth starting: **are the dimensions without exact
fiducials scattered, or do they form a clean prefix?** Scattered ⇒ breadth, which is the shape
an agent is good at. Prefix ⇒ depth at a specialist frontier, and `TARGET_DECISION.md`'s
re-rating is wrong.

Run this **before** any computation. Nothing downstream is worth starting until it returns.

**Model: Opus.** Reasoning in Part B §Model — this gate's hard content is three
nearly-identical claims that a well-sourced answer can still confuse, and the cost of confusing
them is a programme rather than a cell.

Paste **Part A only**.

---

## Part A — paste from here

> You have web search and fetch. Your job is to establish the current state of **exact**
> SIC-POVM fiducial vectors, and nothing else. Do not attempt any mathematics, do not search for
> new fiducials, and do not estimate anything you cannot source.
>
> Your answer decides whether a computational programme starts. **A cell you guess becomes a
> permanent repository fact.** Leave it empty instead.
>
> ### Three claims that are not the same claim, and the main way this task goes wrong
>
> Every source you read will blur at least one of these. Keep them separate in every line you
> write:
>
> 1. **Numerical** fiducial — found to high floating-point precision. These exist for very many
>    dimensions.
> 2. **Exact** fiducial — an algebraic solution: coordinates in an explicit number field, with
>    the SIC conditions verified symbolically. **This is the only one this task is about.**
> 3. **Zauner's conjecture** — that a **Weyl–Heisenberg covariant** SIC exists in every
>    dimension, with a fiducial invariant under a specific order-3 unitary. "A SIC exists in
>    dimension d", "a WH-covariant SIC exists in d", and "Zauner's conjecture holds in d" are
>    three different statements.
>
> If a source says "SICs are known in all dimensions up to N", it is almost always talking about
> (1). Say which of the three each number you report refers to. **A quote that does not itself
> disambiguate is not evidence for (2).**
>
> ### Rules
>
> **1. Source or `NOT FOUND`.** Never fill a cell from memory. `NOT FOUND` is a real answer.
> **2. Every number needs a verbatim quoted sentence containing it**, plus URL and source date.
> **3. Date everything.** This field has moved repeatedly; a 2010 list and a 2024 list are
> different facts.
> **4. Do not compute.** Report what is published.
> **5. Where you cannot settle a cell, name the paper** — exact title plus arXiv id or DOI —
> under `transcribeThis`. Someone will paste the full text to another agent.
>
> ### What to establish, in this order
>
> **(a) The exact-solution set.** Which dimensions d have a published **exact** fiducial? Give
> the set as explicitly as the sources allow, with the source and date for each block of it.
> Relevant literature includes the Scott–Grassl computer studies, Scott's later extension of the
> solution list, work by Appleby, Flammia, McConnell, Yard and collaborators, and any maintained
> online SIC table or database. Do not assume that list is complete — find what is current.
>
> **(b) THE SHAPE QUESTION — the one that matters.** Within the range covered, is the
> exact-known set:
> * **a clean prefix** — every d from 2 up to some N, with few or no holes below N; or
> * **scattered** — holes below the largest known d?
>
> Answer `PREFIX` or `SCATTERED`, and **list the holes**: every d below the maximum
> exactly-known dimension for which no exact fiducial is published. That list, if it is
> non-empty, is the actual target set, so its accuracy matters more than anything else here.
>
> **(c) The numerical frontier**, separately and clearly labelled: to what d are numerical
> fiducials known, and with what precision?
>
> **(d) Method and competition.** What method produced the most recent exact solutions — the
> pipeline, in a sentence or two, and specifically whether it is high-precision numerics
> followed by algebraic-number recovery (integer relation / PSLQ / LLL). Is anyone running that
> pipeline now? Is there a maintained database that accepts submissions?
>
> **(e) Known obstructions.** Is any dimension known *not* to admit a WH-covariant SIC, or is
> any sub-case of Zauner's conjecture proved or disproved? If the answer is "none known", say so
> explicitly — that is a finding.
>
> ### Output
>
> A block per item (a)–(e), each with: the claim, `verdict` (CONFIRMED / CORRECTED / NOT FOUND),
> `whichClaim` (NUMERICAL / EXACT / ZAUNER-WH / MIXED-IN-SOURCE), `url`, `date`, `quote`,
> `transcribeThis`, `note`.
>
> Then three short closing sections:
>
> **§A The verdict.** `PREFIX` or `SCATTERED`, the hole list, and the single quote that settles
> it.
>
> **§B Your confidence in §A**, and precisely what would change it.
>
> **§C Recall against source — answer last.** Which of these figures did you believe before
> searching? For each: **confirmed**, **corrected**, or **failed to settle**, with counts. A
> wrong recall the search caught is the most useful line you can write, because it calibrates
> how far unsourced claims elsewhere in this project can be trusted.

## Part A ends here

---

## Part B — operator notes, do not paste

### What each clause is built against

| clause | the observed failure |
|---|---|
| the three-claims section, first, before anything else | this is the whole risk. The numerical frontier is far ahead of the exact one, and sources move between them mid-paragraph. A model that reports the numerical frontier as the exact one returns `PREFIX` with a real quote attached, and the target dies for a wrong reason |
| "a quote that does not itself disambiguate is not evidence" | the sweep's rule was *a quote containing the number*. That is not enough here, because the number can be right and attached to the wrong one of three claims — the failure mode that survives the earlier discipline |
| the hole list required, not just the verdict | `SCATTERED` without holes is unusable: the holes *are* the target set. It also forces the shape answer to be derived rather than asserted |
| numerical frontier asked separately | makes the conflation visible instead of latent — if (b) and (c) come back with the same number, that is a red flag to check, not a coincidence |
| (d) competition | the deep-vs-broad screen needs it. An actively-run pipeline means arriving late with less |
| (e) "none known is a finding" | the same clause that made the Kaplansky absence the useful answer in the frontier sweep |
| §C recall against source | this project has one measurement of what a `[recall]` tag is worth and it came from the last sweep. A second data point on a different domain is nearly free |

### Model

**Opus, not Sonnet.** Not a general preference — the previous frontier sweep covered 24 records
across more domains and came back well-calibrated on a lesser model, and cost is negligible
either way (Sonnet 5 is \$2/\$10 per MTok against Opus 5's \$5/\$25, on a job whose whole input is
a few hundred thousand tokens of fetched pages). Three things make this gate different:

1. **The hard content is a semantic distinction, not a lookup.** Numerical vs exact vs
   WH-covariant-Zauner are three claims that share their vocabulary and their numbers. Prompt
   discipline cannot rescue this: the failure produces a *correctly quoted* sentence supporting
   the wrong cell. That is the exact shape of the error that cost this session a day on W(103) —
   a validated computation attached to a claim that did not follow.
2. **The output is a gate, and the costs are asymmetric.** A wrong `SCATTERED` sends a Claude
   Code programme into a specialist depth frontier; a wrong `PREFIX` discards the
   best-ranked target on the board. Either error costs orders of magnitude more than the
   difference in inference price.
3. **(b) is synthesis, not retrieval.** "Is this set a prefix or does it have holes" is a
   judgement over an assembled set gathered from several papers with inconsistent conventions —
   the part of the job least like quoting.

Do **not** split it (Sonnet enumerates, Opus judges the shape). The conflation would happen in
the cheap half and be inherited, sourced and confident, by the expensive one. One model, one
pass, Opus.

**Where Sonnet would be the right call:** re-running this gate later as a refresh, once the hole
list exists and the task is "has anything changed since <date>" — that is retrieval against a
known baseline, and the semantic trap has already been navigated.
