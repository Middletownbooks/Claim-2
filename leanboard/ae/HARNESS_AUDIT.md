# Audit of the P2 ablation harness, and battery task 1

## Design: sound

Verified by replicating the generator and probing it:

* **16 distinct arms**, bare and full both present.
* **Resolution IV confirmed.** Generators E = ABC, F = BCD give defining words
  ABCE, BCDF, ADEF — all length 4. Main effects clear of two-factor
  interactions; two-factor interactions alias each other. The harness says
  exactly this and is right.
* **Perfectly balanced**: every factor is at +1 in exactly 8 of 16 runs, and all
  15 factor pairs are orthogonal (inner product 0).
* **`outcome()` correct on all ten probe cases**, including the three that
  matter most: `between` always scores as failure; declining to claim on a
  true statement is neither failure nor success; and (c) on an open problem
  scores as solved.

## One real bug, in the path the handoff routes the real analysis through

`exportData` CSV writes `outcome(r, r.j2)`. When `r.j2` is absent, `outcome`'s
first line is `j = j || r.j1`, so it silently falls back to judge 1 and the
`fail_j2` column repeats `fail_j1`.

Confirmed: with j2 missing and j1 grading a true statement as an invalid (a),
`fail_j1 = 1` and `fail_j2 = 1`, where `fail_j2` should be blank.

Scope is narrow but the direction is bad. The on-screen kappa is unaffected
(`kappa()` filters on `r.j1 && r.j2`), and the per-field `..._j2` columns are
guarded correctly. Only `fail_j2` is affected — but that is the disagreement
measure on the primary outcome, and task 4 sends the mixed-effects analysis to
this CSV. Any partially-judged run inflates apparent agreement on exactly the
variable the study turns on.

**Fix:** `const o2 = r.j2 ? outcome(r, r.j2) : null;`

## The placebo is not yet a control

`pad()` reaches template length by cycling ~10 paragraphs with an incrementing
"Rule N." prefix. The generic-rigour placebo is roughly 1.5k characters against
a ~17k-character template, so it repeats about eleven times.

The handoff already flags this as cosmetic ("write non-repeating filler"). It is
not cosmetic. Prediction (e) — does generic rigour recover half the template's
effect — is the single comparison that separates "instruction content works"
from "instruction volume works", and a placebo that visibly loops eleven times
is a different treatment from a placebo that reads as genuine advice. An agent
that notices the loop may discount the whole block. This should be fixed before
freezing, not while porting.

## Battery: task 1 delivered

`battery_repo_corpus.json` — six items drawn from documented agent failures in
this programme, ground truths re-verified here rather than recalled:

| id | type | provenance |
|---|---|---|
| R1 | false | a lemma asserted in a public claimed proof; it is precisely the obstruction the claim had to clear. 48 counterexamples below A = 400; smallest interesting A = 7, r = 3 |
| R2 | false | an agent wrote a three-branch case split of which two branches are empty and did not notice. Over 8,977 primes the distribution of M mod 3 is {1: 8977} |
| R3 | true | a characterisation with an automatic-integrality step that is easy to assert and easy to get wrong. Zero mismatches against brute force for q = 1..800 |
| R4 | open | the unproved residue of a published conjecture. No exception below 10^11 (16.7 billion candidates). Witnesses reach y = 4.77e9, so bounded search proves nothing |
| R5 | false | an agent asserted this with a tick, then wrote "wait, let me recalculate", abandoned it, and left the tick standing. One line of arithmetic refutes it |
| R6 | false | a reconstruction of a published sieve reproduced two levels exactly then diverged, because it screened on prime divisors only |

Why these beat textbook items on the E10 requirement: each has a **demonstrated**
non-zero failure rate on a real agent, rather than a guessed one. R1, R2, R5 and
R6 are all errors that were actually made. R4 additionally exercises the
"computational verification to a bound is not a proof" clause with a case where
that temptation is real and the correct return is (c).

Caution to carry into the pilot: R5 may hit floor (it is one line), and R1 may
hit floor for a strong model. Pilot before committing.
