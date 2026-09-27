# Gap analysis v3 — what v1 and v2 selected for, and why it was the wrong thing

Three targets cleared the v2 rubric. All three are dead. They died for **three different
reasons, none of which the rubric scored**, and underneath them is one selection effect that
explains the empty queue better than any of the individual failures.

## 1. The three deaths

| target | what killed it | cost to establish |
|---|---|---|
| **PTE size 11** | our exhaustive region sits *inside* the published one — height 80 against 3500, and the cost is C(H,6) | one afternoon of arithmetic |
| **unsearched rings** (d = 43, 67, 163) | every solution ever found sits at \|Δ\| ≤ 8, and the three unsearched rings are 2.3–4.5× thinner; d = 163 has no sieve prime at all | one afternoon |
| **MOLS(12) ≥ 6** | the null is a null about *two specific 5-sets*, not about the recorded lower bound | one afternoon |

Each was cheap. **Each was available before the target was chosen.** None of them is a property
of the problem — they are properties of **our position in it**, and v2's eight dimensions (A–H)
score only the problem.

## 2. The selection effect underneath

> **A problem settled by one explicit finite object in a huge space is, almost by definition, a
> problem whose frontier is set by search capacity.**

That is the whole finite-witness screen, restated. And search capacity is the one thing that does
**not** improve when models get better or cheaper — a model does not add FLOPs.

So the screen this project has used since v1 systematically selects for **compute-gap** targets,
which are exactly the targets where a well-funded group with a better algorithm is already ahead
and stays ahead. PTE 11 is the pure case: Coppersmith et al. reach height 3500 with an
enumeration ~10⁴–10⁵ times smaller than ours at the same height, and no amount of capability
closes that; only *their algorithm* does.

The empty queue is not bad luck. It is what this screen returns.

## 3. Classify the gap, not the problem

v3's first change. Before scoring anything, ask **what stands between us and the frontier**:

| gap type | example | does it improve? |
|---|---|---|
| **compute** | PTE 11: 10⁶ core-hours vs one | **no.** Models do not add FLOPs. Deprioritise. |
| **algorithmic idea** | Hadamard: growth exponent 0.503, needs ≤ 0.252 — FINDING 157 §3 | **yes, with capability.** This is the category to hold. |
| **breadth / literature** | reading 163 findings, 499 records, 41 list entries, one Math. Comp. paper | **yes, with cost.** The expensive part of this whole session was reading and adjudicating. |
| **verification** | d = 67 missing from a published list; 17/17 constraint checks; two 5-MOLS(12) sets proved maximal | **already our strength**, and it is the only category where this project has actually produced output. |

**Every target that died had a compute gap. The one that survived — Hadamard 2092 — has an
algorithmic-idea gap, named and quantified by the repo itself.** That is not a coincidence and it
is the selection rule v3 should run on.

## 4. Three new dimensions, scoring our position

These are cheap, and each is a death this project already paid for.

**H — Headroom.** The ratio of the region we can cover to the region published work covers.
Requires a **cost model with a measured rate**, not an estimate. *(A-2 vs B-2: the same mechanism
claim was wrong when guessed and right when costed.)* Single threshold, no middle band — A-4 was
two-sided with a gap and declined to score (D44). **H ≤ 1 kills the target outright**, whatever
else it scores.

**P — Prior.** Is there evidence the object exists in the region we can reach? The rings' G2 is
the worked example: five non-empty cells across 30, all at |Δ| ≤ 8, with the confound (thin rings
covered less) registered in advance and checked. **A target that is cheap and probably empty is
more dangerous than one that is expensive**, because nothing stops you starting it.

**Δ — Deliverable.** What exactly does each outcome establish, and is it the quantity a published
table records? MOLS(12) passed reachability in microseconds and died here. Ask it as: *write the
sentence that would appear in the abstract, for the positive and for the null, and check that a
table somewhere changes.*

## 5. The E-dimension inversion

v2's E asked **"is the null publishable?"** and scored PTE 11 at E = 5 on it. That question
rejects, by construction, the whole class where the deliverable is cleanest: **record problems.**

A record — a kissing-number lower bound, a cap-set size, a snake-in-the-box length, a D-optimal
determinant — has a *stated current value*, so:

- the unknown set is trivially writable (it is a table),
- headroom **H** is computable from the record itself, not from a literature search,
- the deliverable **Δ** is unambiguous: the table records exactly the quantity you would move,
- and the positive is publishable by definition, while the null is worthless.

v2 scored the null and so never promoted one. **U8 (kissing numbers, dims 11–14), U9
(snake-in-the-box, 9–11), U10 (caps in AG(7,3)/AG(8,3)) and U13 (D-optimal designs) have been
sitting in the unverified pool since the v2 run, unpromoted, for exactly this reason.**

v3's E becomes: *for the polarity that is achievable, name the table, the current value, the date
it was last moved, and what a one-step improvement would be.*

## 6. What this says about near-future models, without speculating about any

No claim here about what is coming or when. Only about **which gaps a given kind of improvement
closes**:

- **Cheaper** → breadth gaps close. The costly part of this session was reading and adjudicating:
  41 Epoch entries, 499 corpus records, 163 findings, two papers. A screen that currently produces
  four candidates per expensive run could produce four hundred. **So prefer targets whose
  bottleneck is candidate-space search, and run the screen wider rather than agonising over one
  corpus.**
- **More capable** → algorithmic-idea gaps close. The Hadamard plan is the shape: a named deficit
  with a measured exponent and a factor-of-two target. **So prefer targets where the gap can be
  written as a number that an algorithm has to beat.**
- **Neither** closes a compute gap. PTE 11 stays dead through any model release.

The operational consequence is the opposite of intuition: **do not wait for a better model to
attack a harder object. Use a cheaper one to look at far more problems, and a better one to
attack the one deficit that is stated as an exponent.**

## 7. What v3 does not change

The step-0 public-list filter stays (v2's own best correction), with one weakening measured this
session: the three curated lists in play overlap pairwise at **5–20%**, so clearing one says
little about the others. The premise-falsification line stays — it has now fired three times
(Cooper–Wallis, SIC, the rings) and twice before a build. The provenance tiering stays.
