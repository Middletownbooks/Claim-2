# Pre-registration — Phase T: construction-trajectory transport

Written and committed BEFORE any Phase T intervention was run.

## 0. The binding technical limitation, stated first

**There is no Lean toolchain in this environment.** `elan.lean-lang.org` has
been egress-blocked since the first phase of this programme, and the pinned
mathlib would have to be built from source. So the literal experiment the brief
describes — supply a skeleton to a prover, measure whether the target proof
succeeds and at what search cost — **cannot be run here.**

Per §1, the smallest valid substitute is used instead, and its limitations are
declared here rather than discovered later.

### The substitute: prospective next-move search guidance

A *guide* is built from source development A's proofs alone and is then used to
order candidate moves at every step of each unseen proof in target development
B. The score is the rank of the move B actually made. Expected search cost is
the mean rank: if a guide puts the true next move first, a searcher trying
moves in guide order examines one candidate; if it ranks it tenth, ten.

This is prospective in the sense §12 demands: the guide never sees any target
proof, and is fixed before target evaluation. It is a genuine measure of
whether A's construction process reduces search in B.

**What it is not.** It measures search *guidance*, not proof *success*: it
cannot tell us whether a target proof would have been found at all. And it
cannot separate "the proof followed the plan" from "the plan predicted the
proof" — in this surrogate those are the same quantity. §9's "did the target
actually use the skeleton" check is therefore automatically satisfied and
correspondingly uninformative. Evidence from this phase is downgraded
accordingly and must not be reported as if a prover had been run.

## 1. What Phase S's architecture metric actually was

`COMPUTED`. Phase S's architecture similarity was a cosine over 35 tactic rates
per 1000 proofs. Decomposing it: **`have` alone contributes 54% of the squared
magnitude**, and `have`, `exact`, `rw`, `simp`, `apply`, `intro` contribute 96%.

Under the brief's §2 taxonomy those are category **C** (toolchain artifacts) and
category **A** (proof engineering). **None is category B** (mathematical
construction). So the Phase S architecture correlation was, as operationalized,
largely a *`have`-rate* correlation. Phase T therefore does not reuse it.

## 2. Representations (three levels, plus a decomposition)

* **L1 TACTIC** — normalized tactic sequence, all identifiers stripped.
* **L2 STRUCTURAL** — tactics collapsed into construction moves:
  INTRO, AUX, CASE, INDUCT, CONTRA, CHAIN, REWRITE, APPLY, BOUND, EXT, AUTOM,
  CLOSE.
* **L3 ARCHITECTURE** — collapsed again into phases:
  SETUP, CONSTRUCT, BRANCH, TRANSFORM, ESTIMATE, CLOSE.
* **ENG** — the L2 sequence keeping only engineering/toolchain moves
  (REWRITE, APPLY, AUTOM, CLOSE).
* **MATH** — the L2 sequence keeping only mathematically contentful moves
  (AUX, CASE, INDUCT, CONTRA, CHAIN, BOUND, EXT).

## 3. Arms (§7, §10), computational budget matched by construction

For target development B and source A, all four guides rank the same alphabet
at the same positions:

* **NONE** — uniform over the alphabet. No supplied strategy.
* **RANDOM** — order-0 model from A: A's move *frequencies* with all sequence
  information destroyed. This is §7's matched-random skeleton — same length,
  same move distribution, randomized order.
* **WRONG-DOMAIN** — order-k model from the development with the *lowest*
  vocabulary similarity to B among those with at least 200 proofs. Rule fixed
  here; applied mechanically.
* **SOURCE** — order-k model from A.

The decisive contrast is **SOURCE vs RANDOM**, because it holds A's move
frequencies fixed and varies only whether the *trajectory* carries information.

## 4. Target selection (§6) — no selection at all

Every proof in every development with at least 8 moves is a target. There is no
target list to freeze because nothing is excluded on any outcome-related
criterion. This is maximally blind and removes the leakage §6 worries about.

## 5. Falsification criteria (§15), written before running

Construction-trajectory transport is **falsified** if any of:

1. SOURCE does not beat RANDOM on target search cost;
2. any SOURCE advantage vanishes once vocabulary similarity is controlled;
3. only L1/ENG transports and L2/L3/MATH do not;
4. SOURCE does not beat WRONG-DOMAIN;
5. the representation's cross-development similarity is collinear with
   vocabulary similarity (**architecture proxy failure**, §5).

## 6. Declared prediction

The author's prior is **Outcome D (null) for MATH and a small positive for
ENG** — i.e. that what transports between these developments is Lean
boilerplate, not mathematical construction. Phases Q, R and S found four
upstreamable lemmas and zero actual transport, and §2's decomposition above
shows the Phase S signal was mostly `have`. A null for MATH is the expected
result and will be reported as such.

## 7. Statistics (§14)

Development-label permutation, clustering targets by their development. The
effective sample is 10 developments, not the thousands of proofs.
