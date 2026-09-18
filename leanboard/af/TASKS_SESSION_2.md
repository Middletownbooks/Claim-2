# Next-session task list — proof-protocol

You have the repo. Read `proof-protocol/MEASUREMENTS.md` and `proof-protocol/DEBTS.md`
first; this list assumes both and does not repeat them.

Last session's work is good. Two measurements stand, the citation layer is
audited to the limit of what the network allowed, the harness is ported with a
real defect found in the published instrument, the diagnostic is rebuilt on the
fields that reproduce, and the prospective arm has five sealed predictions. What
follows is what that work left open, in priority order.

---

## Task 1 — Close D20. This is the whole session's first job.

`be73717` is titled *"Build the two-field κ instrument (debt D20) and run three
blind raters."* The instrument is there. **The raters' output is not.** No key
file, no filled rater sheets, no `score_law_kappa.py` output anywhere in the
tree, and `debts.json` still carries D20 as `open`. The result was either never
obtained or lost when the session ended.

D20 is the test `p3-taxonomy/DIAGNOSTIC.md` names as the one that settles the
rebuild. Until it lands, the rebuilt diagnostic is an argument, not a
measurement — and the repo currently says so in three places while the commit
log implies otherwise.

Run it and commit **the inputs and the outputs**, not a summary: `key.json`, the
three filled rater files, and the verbatim stdout of `score_law_kappa.py`.

**One integrity condition, and it is not optional.** State in the commit message
whether this is a first run or a re-run of a lost result. If any rater output
from last session survives anywhere — scrollback, a stray file, your own memory
of the numbers — say so and report it alongside the new run. A re-run after
seeing an unwelcome number is a different experiment from a first run, and the
difference is invisible to anyone reading the repo later. This programme has
retracted its own claims twice; keep that standard.

Report whatever comes out. κ < 0.6 is a publishable result here: it would mean
the rebuild moved the judgement from one unreproducible field to another, which
is exactly what `DIAGNOSTIC.md` commits to reporting rather than defending.

Note the power limit while you are in there: 14 in-domain items, two fields, five
categories. Step D's 0.048 came from 8 items and the L2 substitute κ came from 5,
with a CI of [0.000, 0.667]. Compute an interval and print it next to the point
estimate, or the number will be quoted without one.

---

## Task 2 — The rebuilt diagnostic has never been scored as a lift

`DIAGNOSTIC.md` reports 4 fires, 0 false positives over 8 negatives, and 2/2 with
6/6 specificity for the union-bound refinement. Those are **raw accuracies**.

The programme's own rule, inherited from the seed and written into
`p1-retrodiction/README.md`, is: *"scores are lift over the telegraph baseline,
never raw accuracy."* `tools/pack.py --telegraph` implements the baseline arm and
**has never been run**. So the headline result of the rebuild is stated in a unit
the repo's own rules forbid.

Run the baseline. For the rebuilt diagnostic the relevant question is not quite
the seed's — the diagnostic reads no leak table — so state the baseline you use
and why before you run it:

- a rater given the item with no rule at all, asked only "did this board change?";
- and the trivial rule that fires on everything in domain.

If the diagnostic's separation survives the comparison, say so with the lift. If
the positives and twins are distinguishable by surface features a rule-less rater
also picks up, that is the finding, and it matters more than the 4/0.

---

## Task 3 — Try to break N9, with an agent that did not build it

`DIAGNOSTIC.md` calls N9 (case 1 after Huang) *"the single result here most worth
trying to break"* — the same problem on both sides of a board change, opposite
verdicts, driven entirely by the invariant's product law. It is the strongest
claim in the rebuild and it was written by the instance that also assigned the
laws.

Give a fresh agent the item and the two law assignments, not the rule, and ask it
to argue the assignments are wrong. Specifically worth pressure:

- The after-board's `bound_law = l2` rests on `A² = nI`. Check that this is a law
  of the *bound* and not of the construction that inspired it.
- The claim that after the signing "nothing further comes off" rests on CFGS's
  ⌈√n⌉ construction being tight against Huang's √n. Check the rounding and the
  constant, and check what the sensitivity conjecture's full statement needs
  beyond the degree bound.
- If both assignments survive an adversarial pass, N9 is worth a great deal more
  than it currently claims. If either moves, the specificity result moves with it.

---

## Task 4 — D19: the ten unverified citations, by a different route

Ten rows are `UNVERIFIED` because arxiv.org, export.arxiv.org, api.crossref.org
and semanticscholar were all egress-blocked. Declaring them rather than accepting
them was the right call and it should stay that way.

Test egress again at the start of the session — it is environment-dependent and
may differ. If the block holds, stop trying the same door:

- Several of the ten (Shannon's 5/2, Gotsman–Linial, Kneser, Kadison–Singer,
  Geometrization) are old enough to have non-arXiv canonical sources that may not
  be blocked. Try journal and society hosts before giving up.
- For the rest, ask the user to paste the abstract or the relevant page. That is a
  cheap request and it converts ten standing debts into verified rows. Name the
  exact ten and what you need from each, so it is one message, not ten.

Do not close a row on recall. The one thing this task has already proven is that
the recalled layer contains real errors — C2 was shorthand that became an error
in context, C5 was a missing regime.

---

## Task 5 — D21: verify the 8 "standard" twins before adding the 5 missing ones

Twenty negatives against a target of ~25. The shortfall is stated honestly, but it
is the *wrong* thing to fix first. Eight of the twenty carry their tightness claim
as STANDARD rather than fetched — which is precisely the recalled-citation
category that task 1 exists to catch, sitting inside the instrument that decides
whether a diagnostic takes a false positive.

A twin whose tightness is merely standard cannot falsify anything: if the
diagnostic fires on it, you cannot tell a false positive from a wrong twin.
Verify those eight first, then add.

`twins/REJECTED.json` already records one candidate removed because Erdős distinct
distances in R³ is no longer open. That decay is the general case, not an
exception. Give every twin a re-check date, as D21's own action line says.

---

## Task 6 — D18: the P2 pilot, and what to do without a key

The pilot is blocked on `ANTHROPIC_API_KEY`. Two moves:

1. Ask the user for a key at the start of the session, with the cost estimate
   attached. You know the arm count (20), the battery size and the judge count;
   produce the token and dollar estimate first so the request is answerable.
2. If no key arrives, do the part that needs none: the pre-registered analysis in
   `p2-ablation/analysis/preregistration.md` states power as roughly a 30-point
   shift at ~40 runs per factor level. Turn that into the actual run count the
   study needs, and say plainly whether the budget implied is realistic. A study
   that cannot reach its own power threshold should learn that before it spends
   anything, not after.

The battery retirement list is currently a labelled prediction. Keep it labelled.
When the pilot runs, score the prediction — it is a free, pre-registered forecast
and this programme should collect those.

---

## Task 7 — D9: attack the E5(b) replacement, the last contested claim standing

The seed proposed replacing "formula versus existence theorem" with *"is the
existence guarantee strictly cheaper than the target?"* and flagged the flaw
itself: n = 3, derived from the cases that motivated it. D8 (product-law
matching) has been rebuilt and tested. D10 and D11 are closed. D9 is untouched.

It is now testable in a way it was not before: `schema/encoder-schema-v2.json`
makes formula-versus-existence-theorem its own field, so the original criterion
can be scored mechanically across all 13 cases and 20 twins. Score both — the
original and the proposed replacement — and report the 2×2s side by side. If the
replacement does not beat the criterion it replaces, say so and drop it, the way
auxiliary-witness lift was dropped rather than rescued.

---

## Task 8 — Do NOT run the L2 re-run yet

`L2-RERUN.md` and its three instruments are built and the fourth fix is enforced
by `validate.py`. Leave them.

D20 is the cheap version of the same question: does a judgement moved onto a
closed-vocabulary field reproduce? If D20 comes back below 0.6, a full L2 re-run
measures reproducibility of an encoding whose diagnostic has already failed, at
many times the cost. Let D20 decide.

If D20 clears 0.6, the re-run becomes the right next big experiment — with fresh
cases and fresh encoders, and without the original five blind encodings.

---

## Task 9 — Keep the prospective arm alive

Five sealed predictions, three fires, one no-fire, one not-applicable, all logged
title-and-abstract-only with hashes. This is the only uncontaminated instrument in
the programme and it is also the slowest, so it needs maintenance, not attention.

- Add a written resolution procedure: who reads the method section, when, and how
  the seal is checked before the outcome is recorded. Write it before any
  prediction is resolvable, not after.
- Log more. Five is not a sample. Every session should add what it can.
- Record the not-applicable rate as a number in its own right. The log already
  says why, and it is the honest measure of how often the diagnostic declines to
  speak.

---

## Do not do

Carrying forward the seven rules in `proof-protocol/README.md`, plus three this
session's state adds:

8. **Do not quote the 4/0 and 2/2-6/6 figures as results until task 2 gives them
   a baseline.** They are currently stated in a unit the repo's own rules forbid.
9. **Do not re-run D20 and report only the run you like.** See task 1.
10. **Do not open a pull request against `anthropics/fermats-last-theorem`.** The
    protocol tree is hosted in the fork by arrangement and is not part of the Lean
    development; upstream has not asked for it.

And still: no P4, no sixth transformation, no rescue of the five, no unregistered
collapse to save a failed prediction.

---

## One thing to write if there is time left

`MEASUREMENTS.md` records what was measured. Nothing records **what this
programme predicted and got wrong** — and it now has a list: L2-1 failed on both
halves, case 9 was voided by a dating error, C5 was a missing regime rather than a
wrong exponent, one twin decayed out of the set, and the seed's own de-tensorize
entry did not survive contact with the cases.

A prediction ledger costs an hour and is the only artefact here that gets more
valuable as the programme continues. It also makes the next instance's judgement
calibratable instead of confident.
