# P-40, the retrodiction test — and the paper overturns my first answer

> **[CORRECTED 30 Sep 2026, after the operator supplied the paper's transcript. Two corrections, and
> the second retracts a verdict I had already pushed.]**
>
> **(1) The search summary lied about Chow's stance, and I leaned on it.** It said Chow *"notes that
> Conjecture 2 might very well be false, although he looked for a counterexample without success."*
> **The paper says the opposite:** *"Despite these counterexamples to C(2), we believe that Conjecture 2
> is plausible,"* and *"we have computationally verified Conjecture 2 for the case n = 3"* using Royle's
> nine-element matroid database. There is no failed counterexample search for Conjecture 2 and no
> statement that it might be false. **I tiered that cell `SEARCH-SUMMARY — not gate-usable`, which is
> exactly why the rule exists, and then used it rhetorically anyway** — I wrote that the author had
> "flagged it as a counterexample target and documented a null result." He did not.
>
> **(2) Theorem 4 supplies the tracked quantity I said did not exist.** *"For any ℓ ≥ k ≥ 2, C(k) implies
> C(ℓ)"*, and **C(2) is false**. So {k : C(k) holds} is upward-closed and **k\* = min{k : C(k) holds} is
> a well-defined integer, currently known only to satisfy k\* ≥ 3.** That is a tracked quantity with two
> sides, and a counterexample to Conjecture 2 = C(3) moves the lower side from 3 to 4. **§2 below, which
> says the decomposition cannot be performed, is wrong as stated.** The corrected analysis is §2a.


**Target: Conjecture 2 of Timothy Chow, "Reduction of Rota's basis conjecture to a problem on three
bases."** The programme came close to the first counterexample about a month ago and was scooped by
another researcher weeks earlier.

**Verdict: SELECT v1 FAILS it, and worse than P-40 predicted — it fails *before any gate*, at the
decomposition step in §1 that every candidate must pass through first.**

## 1. Provenance, stated first because the container blocks the sources

**`arxiv.org` and `cs.uwaterloo.ca` are both blocked by this container's egress proxy** — D50's exact
condition. I could not open the paper. So:

| claim | tier |
|---|---|
| arXiv:math/0504367, submitted **18 April 2005**, accepted SIAM J. Discrete Math | `SEARCH-SUMMARY` — **not gate-usable** |
| Conjecture 2: *if M is a matroid of rank n that is a disjoint union of 3 bases, and I₁…Iₙ are disjoint independent sets with \|Iᵢ\| ≤ 3, then there is an n×3 grid containing each element of M once, with Iᵢ's elements in row i, whose three columns are bases of M* | `SEARCH-SUMMARY` |
| ~~Chow's own remark that Conjecture 2 "might very well be false"~~ **FALSE — see the correction box. He calls it *plausible* and verified n = 3 computationally.** | was `SEARCH-SUMMARY`, now refuted at `SECONDARY-RELAYED` |
| the paper gives two counterexamples to the **two**-basis analogue | `SEARCH-SUMMARY` |
| Polymath 12 (Feb 2017) attacked Rota's basis conjecture | `SEARCH-SUMMARY` |

**2005 makes it 21 years old**, consistent with "twenty-year-old".

**The finding below does not depend on any of that.** It depends only on the target being *a conjecture
whose falsification is a finite counterexample* — which the operator stated and the summary corroborates.
**It is a fact about SELECT v1, which I can read, not about Chow's paper, which I cannot.** A gate-grade
confirmation of the paper's details needs an instance that can reach arXiv.

## 2. The failure is before gate 1

`SELECT_v1.md` §1 requires, **of every candidate and prior to any gate**:

```
headline  →  tracked quantity  →  its two sides (lower, upper)
          →  for each side, the BOUND OBJECT whose exhibition moves that side
```

**Conjecture 2 has no tracked quantity.** Its headline is a truth value. There is no lower side, no upper
side, and therefore no bound object per side. **The decomposition cannot be performed, so the target never
reaches S0.**

That propagates into three gates for the same reason:

| gate | on this target |
|---|---|
| **S0 OPEN** | **PASS.** Open, and no withdrawn resolution claim. |
| **S1 COUPLED** | **FAIL.** Requires *"exhibiting a better witness moves a published bound on the headline quantity itself"*, via route (a) the headline is an **extremum** over finite objects, or (b) a **published bound** established by finite certificate. A truth value is neither an extremum nor a bound. Both routes are inapplicable, not merely unmet. |
| **S2 NOT VETOED** | **PASS.** The counterexample predicate is decidable — finitely many n×3 grids to check. |
| **S3 IDEA GAP** | **FAIL, and not for the reason P-40 gave.** I predicted S3 would fail because a 21-year-old conjecture has no *knowable* move kind. It fails because there is **no coupled side whose most recent move could be typed at all.** |
| **S4 NOT CROWDED** | **unevaluable** — same cause: no coupled side to have moved. |
| **S5 DELIVERABLE** | **FAIL.** Requires *"a named maintained table, or a named published bound, changes on a one-step improvement"*. A counterexample settles a conjecture; it changes no table and no bound. |

**Four of six gates are inapplicable rather than unmet**, and all four for one cause: **SELECT v1 is built
for record problems with a tracked numeric quantity and two bounding sides. A conjecture-counterexample
target has none of that.**

## 2a. Corrected: the decomposition IS possible, via Theorem 4, and then the gates plausibly all pass

`rota/verify_c2.py`, run here, makes the mathematics primary rather than relayed. **Both of Chow's
C(2) counterexamples are verified exactly**, with positive controls and negative tests:

* **M(K₄)** with I₁, I₂, I₃ the three pairs of non-incident edges: of the **8** ways to split them into a
  3×2 grid, **0** have both columns spanning trees. The obstruction is total and elegant — in every one
  of the 8, **exactly one** column is a tree and the other is a triangle.
* **Oxley's J**, Chow's 8 explicit vectors in ℝ⁴: of the **16** splittings, **0** have both columns bases,
  by exact determinant over the rationals.

So **k\* ≥ 3 is established by a finite certificate checked by terminating computation** — I just ran the
check. Under that reading SELECT v1's gates apply and, as far as I can judge them:

| gate | verdict under the Theorem-4 reading |
|---|---|
| **S0 OPEN** | PASS — k\* unresolved, conjectured 3 |
| **S1 COUPLED** | **PASS via route (b)** — *"a published bound on the headline was established by a finite certificate checked by terminating computation"*, which is precisely the C(2) counterexamples |
| **S2 NOT VETOED** | PASS — decidable, finitely many grids |
| **S3 IDEA GAP** | **PASS** — the most recent move of the lower side is Chow 2005, kind **ANALYTIC** (hand-built from M(K₄) and J). S3 asks only about *kind*, not date. |
| **S4 NOT CROWDED** | **PASS as of before the scoop** — no movement since 2005 by AI search or large-scale optimisation |
| **S5 DELIVERABLE** | judgement call — does *"C(2) false, C(3) open"* count as a named published bound? Arguably yes, and the abstract sentence is writable. |

**On that reading the target passes all six, and P-40 is FALSE.**

**But the realistic reading is still that the screen would never have seen it**, and for a reason that is
neither of my first two: **k\* is a quantity nobody tracks.** It appears in no table, Chow does not name
it, and the 499-record corpus holds records with stated current values. **The re-parameterisation is
something I constructed just now, with the decomposition step in front of me.**

**So the finding is neither "the screen filtered out the class" nor "the screen would have caught it".**
It is this:

> **SELECT v1 has no step that asks whether a headline can be re-parameterised into a graded ladder, and
> whether this target is in scope depends entirely on whether the analyst notices Theorem 4.** Every gate
> downstream is pass/fail with a single registered threshold. **The step that decides whether any of them
> run — the §1 decomposition — is unregistered judgement.** That is where the screen's reach is actually
> set, and it is the one part that was never given a threshold.

**And P-40's threshold is therefore unevaluable as worded** — *"if the target passes all of S0–S5"*
presupposes a decomposition, and the decomposition is the thing in dispute. **D54's shape for the second
time:** a threshold whose answer is fixed by a prior choice the prediction did not fix.

## 3. My first answer, left standing for the record — and superseded by §2a

**P-40 predicted a false negative and got one, but understated the mechanism.** A gate rejecting a good
target is a calibration error you can fix by re-scoping a clause. **A decomposition step that cannot
express the target is a domain error, and no amount of gate tuning reaches it.**

**And the irony is exact:** the programme's near-success was on a target class its own selection function
structurally excludes. Seven screens searched a corpus of **record** problems for something to attack,
while the thing that nearly worked was a **conjecture counterexample** — filtered out before gate 1.

**Note which screen would have liked it.** `../playability/INTERESTINGNESS.md`'s playability classes put an
existence-headed statement with a finite checkable YES branch in **P1** — the good class. Conjecture 2 is
exactly that. **It is SELECT v1's record decomposition, not the playability screen, that excludes it.** The
two instruments disagree about this target and only one of them was driving the queue.

## 4. And if the screen had seen Rota at all, it would have picked the wrong side

This is rule 3 — two quantities sharing a name — and it is my reasoning rather than a literature claim.

*"The largest n for which Rota's basis conjecture is verified"* **is** record-shaped: a tracked value, two
sides, a witness that moves one. **That is what SELECT v1 would select if Rota entered the corpus.** And
extending a verification frontier by one n is **not** what nearly succeeded; finding a counterexample to a
reduced conjecture is. **So the screen does not merely miss the target — it substitutes a worse one that
looks like a record.**

## 5. What P-40 scores — RETRACTED, see §2a and the correction box

**Threshold CORRECT** — SELECT v1 fails the target. **Location right, mechanism wrong**: I named S3, and
S3 does fail, but because there is no coupled side rather than because its move kind is unknowable. **The
mechanism I missed is more damaging to the screen than the one I predicted.**

I also wrote that *"a failure at S4 would be the more interesting outcome."* The actually-more-interesting
outcome was available and I did not consider it: **failure before any gate.**

Against lesson 33 — *predict the kind of failure, not its location* — this is a third data point and an
unflattering one. P-39's structural grade predictions went 3 of 3. Here my structural mechanism was wrong
while the location happened to be right, which is the opposite error and warns that "structural" is not
self-certifying.

## 6. What this does not establish

* **Chow's paper is unread here.** Everything in §1 is `SEARCH-SUMMARY`.
* **It does not show a conjecture-counterexample screen would have worked.** It shows this one could not
  have run. Whether a screen over that class finds anything is untested, and the base rate of
  counterexample searches is presumably brutal — the programme's own attempt was scooped.
* **n = 1.** One target, one demonstrated domain error. That is far stronger than a null across seven
  instruments, and it is still one target.
