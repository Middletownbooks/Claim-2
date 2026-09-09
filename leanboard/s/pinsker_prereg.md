# Pre-registration — QPR Pinsker intervention (Phase S §9)

Written and committed BEFORE any target development was inspected for
suitability. The brief forbids choosing a target after seeing its theorems, so
the selection rule below is mechanical and is applied as written.

## Source interface

The QPR Pinsker cluster: the declarations in namespace
`QuantumParallelRepetition.Pinsker`, which prove

* `quadratic_le_klFun : 3(x-1)^2 / (2(x+2)) <= InformationTheory.klFun x`
* `finite_pinsker : 2 * TV(p,q)^2 <= KL(p,q)` for finite distributions

built on mathlib's own `InformationTheory.klFun`.

## Target selection rule (mechanical)

A development other than QPR qualifies as a target if its source text
references at least one of:

1. `InformationTheory.klFun`, `InformationTheory.klDiv`, or any mathlib name
   containing `klDiv`/`klFun`;
2. `Real.negMulLog`, `Real.binEntropy`, or any mathlib name containing
   `negMulLog`/`binEntropy`;
3. a total-variation quantity: any mathlib name containing `totalVariation`;
4. entropy-like summations: a `∑` in the same statement as `Real.log` applied
   to a ratio.

Developments are ranked by the number of distinct qualifying references. The
**top two** qualifying developments are the targets. If fewer than two qualify,
the finding is reported as "no valid target exists" and no intervention is run.

## Arms

* **BASELINE** — target's exportable statements matched against a source pool
  of QPR's exportable statements with the Pinsker cluster removed.
* **INTERVENTION** — the same pool with the Pinsker cluster added.
* **NEGATIVE CONTROL** — the same pool with an equal number of QPR exportable
  lemmas drawn at random (seed 20260909), matched on median statement length
  to within 20%.

## Measures

Change, from baseline to each arm, in: matched target statements at J >= 0.4;
mean best-match score; and the number of target statements whose best match is
a Pinsker declaration specifically.

## Declared prediction

The author's prior is that the intervention will produce **no** measurable
gain, because Phases Q and R found every portable object to be a
mathlib-shaped lemma that no other development needed. A null result here is
the expected outcome and will be reported as such.

## Interpretation rule

A gain in the intervention arm that is not matched by the negative control
counts as ACTUAL TRANSPORT. A gain matched by the negative control counts as a
pool-size artifact. No gain in either counts as UPSTREAMABLE-ONLY: the lemma
belongs in mathlib but carries no cross-development capability.
