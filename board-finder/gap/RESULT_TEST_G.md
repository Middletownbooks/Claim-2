# Test G — the first outcome-scored test of `g(gap_type)`: the COMPUTE class is empty

Registered in `SELECT_v1.md` §6 (commit fab89d8) before any label existed. Scorer:
`discovery/score_test_g.py`, written and negative-tested before any label existed. It returned the
expected verdict on six synthetic files: perfect, reversed, a missing problem, a duplicate problem,
a class too small to score, and an ambiguous kind. Labels are in `discovery/G_odd.md`, the score in
`discovery/G_odd_score.json`, and outcomes in `discovery/aerp_outcomes.json`.

## 1. Result on the ODD test slice (34 problems)

```
excluded, known optimal (dark grey)     7   15 17 19 29 63 65 67
excluded, NO-RECORD                     4   9 27 51 53
excluded, move kind UNKNOWN            12   1 3 5 7 11 21 25 31 33 39 57 61
excluded, unparsed (worker: CE)         1   49
testable                               10   13 23 35 37 41 43 45 47 55 59

by kind          ANALYTIC 1/8 improved     SEARCH-NEW 1/2     SEARCH-REPEAT 0/0
G-1  IDEA vs COMPUTE          2/10 vs 0/0   UNEVALUABLE → §3.1 NOT VALIDATED
G-2  SEARCH-NEW vs ANALYTIC   1/2  vs 1/8   UNEVALUABLE → NOT VALIDATED
flip-11 sensitivity: unchanged (11 is UNKNOWN-kind, so it is excluded either way)
```

## 2. What this says

**§3.1's discriminator could not be evaluated, because its COMPUTE class is empty.** Not one of the
10 testable problems' most recent pre-2025 move was labelled "the same method run bigger". The
same holds across the arms:
* Arm 2a assigned S3 four times and never assigned SEARCH-REPEAT;
* Arm 2c assigned it once, on a single search-summary sentence.

The likely mechanism is structural rather than an artefact of this environment. **A published record
move has to claim novelty, so the literature almost never describes a move as "we ran the old method
longer."** The COMPUTE label exists in `GAP_V3.md` §3's rubric, but movement history — the only
evidence §3.1 reads — does not supply it. In practice §3.1 collapses to two questions: is the move
kind knowable, and is it a hand construction or a new search? Neither answers "will this move under
capability?"

What actually decided cases in this run was **not** gap type:
* crowding (S4) killed 308, kissing dimension 11, and cap-set capacity;
* **UNKNOWN** move kinds killed most of the rest.

Descriptively, and too small to count: new search methods improved 1 of 2 and hand constructions
1 of 8. That is the direction G-2 predicted, at n = 2.

## 3. Scored

* **P-33 G-1 (§3.1 not validated): CORRECT** — by the unevaluable route. That is the weak way to
  be right, and I record it as such.
* **P-33 G-2 (Δ₂ > 0): WRONG** — unevaluable at n = 2, which the registration counts as not
  validated.

## 4. Threats to validity, as they occurred

* **Blinding breach.** The worker reports that it "briefly saw part of aerp_outcomes.json before
  recognising what it was" and did not use it. The briefs did not forbid reading the repository.
  They should have, and the file should not have been in the tree the worker could see. No
  statistic here could have been moved by the breach, since none is evaluable.
* **12 of 27 non-excluded problems had UNKNOWN kind.** Search summaries give values and dates but
  rarely say how an object was found, and no paper text was readable.
* The worker declined to use the brief's "Nov 2024" dating of Boyer–Li (problem 3); it found only
  a June 2025 arXiv id. It also caught a recall error of its own (problem 61: 11/10, not 11/8).

## 5. The EVEN slice

**Not run, and still unread.** Its worker was stopped when I capped concurrency. Because G-1 failed
for lack of a class rather than on a value, there is no revision to test. **EVEN stays reserved,
intact, for a future run with readable sources.** Here is what would make that run worth doing: a
COMPUTE label assigned from the text of the papers, not from summaries. If the class is empty even
then, the novelty-bias explanation in §2 is confirmed, and §3.1 should be retired rather than
repaired.
