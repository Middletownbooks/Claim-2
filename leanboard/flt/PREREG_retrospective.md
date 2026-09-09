# Pre-registration — retrospective benchmark on the FLT proof's early layers

Written and committed **before** the experiment is run and before any score is
inspected.

## The question

A complete traversal of a hard theorem is available (29 511 theorems, exact
citation graph). Its load-bearing interfaces are known *in hindsight*. If a
discovery system had been standing at the **beginning** of this proof, could it
have identified which abstractions would end up carrying it?

## The answer key (hidden from the predictor)

For each of the repository's definition modules, its **total statement usage**:
the number of theorem statements across all 29 511 theorems that import it.
The target set is the **282 definition modules that carry 80% of all statement
usage** (established in Report I).

The predictor never sees: usage counts outside the early layers, any theorem
outside the early layers, the citation graph outside the early layers, the root
theorem, PROOF-PATH.md, or the target set.

## The early layers

Bottom-up citation depth: `depth(v) = 0` if `v` cites nothing, else
`1 + max(depth(citations))`. The early split is

> the smallest depth cutoff `D` such that at least 25% of all theorems have
> `depth ≤ D`

— a rule fixed here, not a number chosen after seeing the distribution.

## Predictors (all computed from the early layers only, unsupervised)

1. `early_usage` — how many early statements import the definition. **This is
   the naive baseline and the one to beat.**
2. `early_users_distinct` — distinct early theorems importing it.
3. `early_consumer_degree` — summed early citation in-degree of its users.
4. `cooccurrence_breadth` — distinct other definitions it co-occurs with in
   early statements.
5. `community_breadth` — distinct blind communities (Report I partition,
   restricted to early nodes) its users span.
6. `combined` — mean of the per-feature normalized ranks of 1–5.

No feature is fitted against the answer key; there is no training step, so
there is nothing to leak.

## Metrics

Precision@282, recall@282, ROC-AUC over all definition modules, and lift over a
random ranking. Reported for every predictor, including the ones that lose.

## Pre-registered predictions

* **Q1 (ceiling).** Some load-bearing definitions are **invisible early** — they
  appear in zero early statements. I predict this is a substantial fraction
  (>20% of the 282). If so it is a hard ceiling on any early-prediction method,
  and the most important number in the experiment.
* **Q2 (naive baseline is strong).** `early_usage` achieves AUC ≥ 0.80 among
  definitions that are visible early. Rich-get-richer is expected to dominate.
* **Q3 (structure adds little).** No structural feature (3–5) beats
  `early_usage` on precision@282 by more than 5 percentage points. *If this
  fails and a structural feature wins clearly, that is direct evidence that a
  bridge-value-like signal has predictive content the naive count lacks.*
* **Q4 (breadth beats volume for the top).** Among the definitions visible
  early, `cooccurrence_breadth` ranks the eventual top-20 interfaces higher than
  `early_usage` does. This is the one place I expect structure to help.

Failures are reported as failures. The experiment is run once.
