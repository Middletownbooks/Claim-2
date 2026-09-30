# The predecessor already had four of the things I registered as findings today

**The Cycle 0 target-selection prompt** — gap analysis of open problems plus Opus-in-Claude-Code gating,
predating all the playability work — is the instrument that produced the Rota target. Read against
`SELECT_v1.md` and against this session's debts, it is not a rougher earlier version. **On the two
observables that decide everything, it is better, and SELECT v1's own post-mortem says so without
knowing it.**

## 1. Four of today's debts were already designed in

| what I registered today | Cycle 0 already had it |
|---|---|
| **D56** — nothing checks whether a question has already been answered here | **Task 1, the whole prompt's reason for existing.** *"In every case the missing input was the same: what the prior explorations actually established. That input is cheap to obtain and has never been obtained."* A register of seven prior attempts with **the binding constraint stated as a formal proposition**, costed estimates re-derived, and claims entering as `assumed`. |
| **D51** — the crowding gate counts moves, so it cannot see an attempt | **Task 2's fourth question:** *"Has anyone announced work in progress on the next rung?"* — *"including independent-researcher preprints."* **That is the Allikvere case, named in advance.** |
| the reproduction gate I invented for Costas phase 1 | *"A candidate that cannot clear the reproduction gate on paper — i.e. where the run cannot see how it would reproduce the current frontier — is rejected at selection, not at cycle 20."* |
| null-as-deliverable | *"If no candidate clears the rule, say so and return the register. That is a real result."* |

Also there: **"Record negatives as 'searched, not found, on this date' — never as 'open'"**, and Task 3's
insistence on the frontier paper's *method section* because *"it cannot be done from an abstract"* —
which is D50's access problem with its reason attached.

## 2. The compute-shaped / theory-shaped distinction, and where each instrument measures it

**Cycle 0 measures it from our own prior attempt:**

> *"The binding constraint hit — stated as a formal proposition, not prose. 'We ran out of session' and
> 'the realizability constraints could not be encoded' are entirely different findings."*
> *"Claude Code … multiplies compute-shaped constraints and does almost nothing for theory-shaped ones. A
> problem whose prior run stalled on encoding theory is not made tractable by a longer run."*

**SELECT v1's S3 tries to infer the same distinction from the literature** — the *move kind* of the most
recent move on the coupled side. Its own §II.1 records the result:

> **"Does not survive as a discriminator. Test G: the COMPUTE class is empty (0 of 10 testable problems;
> 0 of 4 S3 calls in Arm 2a). In practice S3 measured whether a move kind is *knowable* … The likely
> cause is structural: record papers must claim novelty, so the literature never labels a move 'the same
> method, run bigger'."**

**Same distinction, two sources. From the literature it is unmeasurable — 0 of 10. From our own
transcripts it is directly observable, and it is what Task 1's key field records.**

And §II.4 proposal 1 then asks for a replacement: *"Movement history cannot supply the COMPUTE label. Use
a direct question instead: has a general-purpose AI search system been pointed at this record and failed
to move it?"* **That is Cycle 0's move, reinvented — and weaker, because it asks about some external
system's failure rather than about our own binding constraint, and its own text concedes the sign is
ambiguous.**

## 3. The fair caveat, which is the actual finding

**Cycle 0's observables require prior attempts, and do not scale.** Task 1 needs seven transcripts to
register. It cannot run over 499 records nobody has touched. So SELECT v1, built for a corpus two orders
of magnitude larger, *had* to substitute literature-derived proxies:

* compute-vs-theory → **S3**, the move kind. **Measured empty, 0 of 10.**
* crowding → **S4**, counting moves. **Blind to attempts** (D51), and blind to contemporaneous work — the
  thing that actually cost us Rota.

> **The scaling was paid for in exactly the two observables that decide everything, and both substitutes
> failed.**

That is a sharper claim than "SELECT v1 is a regression", and it is the one the evidence supports. It
also says what a v2 needs: not better gates over the same corpus, but **a population small enough that
the direct observables are available** — which is what Cycle 0's shortlist of four candidates was.

## 4. And the corpus question answers itself

Cycle 0's population: **open problems** with a numeric frontier, machine-checkable verification, and a
null result that is itself a deliverable — explicitly *"not previously attempted by this collaboration."*
Four candidates, not 499.

`RESULT_RETRODICTION_P40.md` §2b concluded that SELECT v1's gates would have passed the Chow target and
that **the binding constraint was corpus coverage** — the 499-record corpus holds tabulated records, and
the bracket 4 ≤ n ≤ 9 is in no table. **Cycle 0 was running over precisely the population that contains
such targets, and Rota was item D on its shortlist**, with its collision risk named in advance:
*"Polymath12 swept it in 2017 with strong participants; establish what they actually left."*

## 5. What this costs me

Four debts registered today as findings were solved a lineage ago, in a document in this project's own
history. **D56 — the debt about not checking prior work — is the one I most conspicuously earned**, since
I wrote it after failing to check prior work, and the prior work I failed to check was a prompt whose
entire first task is checking prior work.

The pattern across today's corrections holds here too: **each wrong reading was more favourable to a
clean story than the truth.** The clean story was "the screen produced nothing and working-a-problem
produced everything." The truth is that an earlier, better-instrumented selector produced one result, the
record lineage produced the other, and the scoring vocabulary recognised neither.
