# P-40, the retrodiction test — the screen cannot represent the target at all

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
| **Chow's own remark that Conjecture 2 "might very well be false", and that he searched for a counterexample without success** | `SEARCH-SUMMARY` |
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

## 3. So the screen did not miss this target. It filtered out the class.

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

## 5. What P-40 scores

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
