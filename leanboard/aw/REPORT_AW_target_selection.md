# Arm AW — why "ship a finite object" fits a constrained budget, and the rule that follows

Arms AT, AU and AV argued for finite deliverables on **audit** grounds. That is the weaker
argument. The stronger one is about **spend**, and this programme's own artifacts show it.
`target_selection.py`, 10/10.

## 1. The real argument: a terminating success condition

A finite-object search **decides**. The SAT encoder returns SAT or UNSAT. The 1296-grid
enumeration finishes. You know when you are done, and you know when you have failed.

An existence-argument search has no such condition — and that is exactly why both elaborate
prompts in this series had to manufacture one:

- CDC: *"Spend at least 8 hours on this before even thinking of returning or giving up."* A
  **floor**, not a bound.
- CDC: *"Do not return a reduction, partial result, isolated missing lemma, best-effort
  summary."*
- Nevanlinna: three forbidden sentences, including *"no counterexample was found."*

**Those instructions exist to substitute for a missing stopping condition.** Neither prompt
bounds effort from above, because neither *can*: nothing in the task says when the search is
over. Nevanlinna spent 7 h 14 min and ~1.02M tokens and its core is still unreached by any
outside auditor. SSUF took four sentences.

**On a constrained budget, the unbounded search is the thing you cannot afford.**

## 2. The search is its own control

Arm AT named the control — run the apparatus on a case with a known answer — as the one
domain-independent feature separating the verified artifacts from the unverified. For a
finite-object search it comes **free**, because the instrument is a decision procedure:

- *"the same encoder returns UNSAT at n = 3 … agreeing with the verification reported in the
  paper"*
- exhaustive audits at ranks 3 and 4 returning zero counterexamples where none should exist

You do not add a control. Running the same encoder one parameter lower **is** the control, and
it costs one run. Audit surface, calibration and budget turn out to be three faces of one
property.

## 3. Failure is cheap and informative

| | fails as | tells you |
|---|---|---|
| finite-object search | a definite negative on a defined space | where not to look |
| existence-argument search | unbounded spend, no verdict | nothing |

The preprint is the clearest case: **4,358,045 rank-4 instances and 1,120,230 on K₆ returning
zero counterexamples became Theorem 1.5** — a published result. A null from a finite search is
a theorem. A null from an existence-argument search is a bill.

## 4. Not a settle-for-less strategy

| | n | mean | median | max |
|---|---|---|---|---|
| construction-refuted | 178 | **18.1** | 15 | 65 |
| everything else in the corpus | 486 | 16.5 | 13 | 68 |

**178 of 205 disproofs (87%) are constructions** — this is how disproof happens, not a niche.
And they score *above* the corpus average, not below.

## 5. Where the class lives

| share construction-refuted | | field |
|---|---|---|
| **40.0%** | 26/65 | Geometry & topology |
| **39.1%** | 9/23 | Quantum information & computing |
| **38.6%** | 22/57 | Algebra |
| 30.5% | 54/177 | Combinatorics |
| 29.7% | 22/74 | Analysis |
| 20.0% | 8/40 | Probability & statistics |
| 16.7% | 5/30 | Algorithms & optimization |
| 14.2% | 19/134 | Number theory |
| 8.8% | 3/34 | Theoretical computer science |

A factor of four and a half between the top and bottom. Number theory and TCS are the
expensive places to run this strategy.

## 6. The rule both successes actually used

Neither picked a famous problem. Both picked a **parametrized universal claim** and attacked
**at the smallest parameter above the verified boundary**:

- **Chow C(3)** — Chow verified n = 3 over *all* matroids on nine elements. Both
  counterexamples are at **n = 4**.
- **Goemans C = 1** — the counterexample is seven vertices, three terminals, eight routings.

That is not a coincidence. The minimal parameter above the verified boundary is the cheapest
place a finite search can live; the only place an exhaustive control is affordable; where the
residual open region is thinnest, so anything found there is new; and small enough that the
write-up is hand-checkable — which is what made both artifacts verify in one sitting.

> **Rule.** Take a conjecture of the form *"for all instances of size n, P."* Find the largest
> n already verified exhaustively. Attack n + 1. **UNSAT is a theorem extending the verified
> boundary. SAT is a counterexample. There is no losing branch.**

## 7. What it does not get you

- **Not a famous open problem.** Those are famous because no small parameter settles them.
- **Not a universal theorem** — per arm AV, shipping a finite object is available exactly when
  the target is an existence claim.
- **Nothing for the significance claim.** "Previously open" stays a literature question no
  certificate answers.
- **122 of 178 construction-refuted entries sit at `unreviewed`.** A checkable artifact is not
  the same as a checked one — and this programme has spent several arms establishing that
  nobody does the checking.
