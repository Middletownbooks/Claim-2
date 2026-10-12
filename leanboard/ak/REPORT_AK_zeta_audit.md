# Arm AK — audit of the zeta-zeros result (the corpus's sig-68 entry)

**Target.** Alpöge & Furman, *More than two thirds of the zeros of the Riemann zeta function
are simple and on the critical line*, arXiv:2608.13637v2 (19 Aug 2026). The mathematical
argument was discovered and written by Claude; the listed authors verified it and take
responsibility. Lean at `anthropics/zeta-23-lean`, **tag v1.0** (commit `82ee634`), which is
the version of record and what I audited. VibeMathed's highest-significance entry (68/664),
tier `lean-checked` — the top of the queue arm AJ enumerated.

**Result:** unconditionally `N^s_0 ≥ (2/3 − o(1))N` and `N_d ≥ (5/6 − o(1))N`, against prior
records `5/12` and `0.6603`. Montgomery's 1973 RH-conditional deduction made unconditional by
replacing termwise positivity with a rank–trace inequality on a finite compression of Weil's
Hermitian form, Sylvester's law of inertia handling off-line pairs.

**What I did not do.** No Lean rebuild — no toolchain, and Mathlib at the pinned commit would
dominate the budget. Arithmetic, source-level and statement-level checks only.

---

## 1. Arithmetic — 33/33, `verify_zeta23.py`

Every numerical constant recomputed from the paper's own definitions.

- **`R(ψ₀) = 4/3`** from (5.13): `∫ψ₀ = 1`, `∫ψ₀² = 1`, `∫∫|u−v| = 2∫₀¹w(1−w)dw = 1/3`.
  Hence `2 − R = 2/3` and `(3 − R)/2 = 5/6` — Theorem A exactly, in rationals.
- **`R(ψ_MT) = ½ + cot(1/√2)/√2`.** `G(0) = 1 + 2∫₀^{1/2} v cos(√2 v)dv` agrees with the
  closed form `cos(1/√2) + (1/√2)sin(1/√2)` to 1e-13; `∫ψ_MT = √2 sin(1/√2)`; the quotient is
  `1.327504`, giving `2 − c_MT⁻¹ = 0.672496` and `(3 − c_MT⁻¹)/2 = 0.836248` — the stated
  `0.67250` and `0.83625`. The Lean file's `cMT := √2·tan ϑ/(1 + ϑ·tan ϑ)` is its reciprocal.
- **Remark 6.1's λ-family.** `H(λ) = 2 − 1/λ − λ/3` has `H(1) = 2/3`, is strictly increasing
  on `(0,1)`, and its stationary point is `λ = √3 > 1`. So "no λ < 1 improves the constants"
  is right, and the reason is that the interior maximum lies outside the admissible range.
- **The integrality levels.** `(x−1)² ≥ 0` gives `x² ≥ 2x−1`; `(m−1)(m−2) ≥ 0` gives
  `m² ≥ 3m−2` on positive integers — the two levels §7.2(c) claims.
- **§7.2(f).** `Λ₂(0;1) = 5/36` with proportion `2(1−Λ) − 1` gives exactly `13/18`, and
  `13/18 > 2/3`. The same map sends the Cauchy–Schwarz stage `n₊ ≥ (3/4)N` to `1/2`, which is
  the intermediate constant Appendix B describes.
- **The ceiling.** `p₀ ≤ 0.6818287`, and `p₀ − 2/3 = 0.0152` — the claimed "within 0.016".
- **Remark 7.1 (ξ′).** `0.85838` and `0.92919` satisfy `(3−R)/2` against `R = 2 − 0.85838`
  exactly; likewise the quartic pair. The flat constant reproduces Farmer–Gonek–Lee's
  RH-conditional `85.84%` with RH removed, the quartic stays under the RH-conditional
  `0.8825`, and neither exceeds Wu's `0.86957` for on-line-without-simplicity — all as stated.
- **§7.3's cubic weight** `ω(m) = m/2 + (2m²−m³)/18 + (4/9)·1_{m=1}` equals 1 at m = 1, 2, 3.

**Two arithmetic observations worth recording.** `2/3 = 0.6667` already exceeds the previous
*distinct-zeros* record `0.6603` — Theorem A(i) alone beats the A(ii) predecessor before
A(ii) is applied. And the method reaches within `0.0152` of its own proven ceiling on first
use, which is the fact §5 turns on.

## 2. Source-level Lean — clean, at v1.0

- **Zero `sorry` tokens outside comments anywhere under `Zeta23/` or in any `Solution` file.**
  All 33 live in the three trusted challenge files (`Challenge.lean` 15,
  `Challenge/Multiplicity.lean` 12, `Challenge/XiPrime.lean` 6), which state each theorem with
  a placeholder proof **by design** — that is the `leanprover/comparator` format, not a gap.
- **No `axiom` declarations.** The two hits a plain grep reports sit inside a commented-out
  upstream test block in `FromPNTPlus/Tactic/AdditiveCombination.lean`; they declare nothing.
  The only `native_decide` hit is a comment asserting its absence.
- **Ported files carry their provenance.** `Mertens.lean` and `StrongPNTPrefix.lean` are
  truncated prefixes of `PrimeNumberTheoremAnd` with docstrings naming the upstream commit and
  stating explicitly that the truncation is *before* the upstream `sorry`s, so none enters.
  The grep hits in those two files are that prose. This is careful porting hygiene.
- `AUDIT.md` pins Lean `v4.33.0-rc2` and Mathlib `51e6992efd06`, and reproduces the
  `#print axioms` output verbatim for all 33 statements: three standard axioms, no `sorryAx`.

## 3. The statement audit the site says is missing — the textual half, done

VibeMathed holds this at `lean-checked` for a stated reason: *"the trusted statement files are
written in the same repository by the same team, so nobody independent has checked the Lean
statement against the paper's claim... running [comparator] is what a promotion would take."*

I cannot run the kernel. I can do the textual comparison it would check, and did:

| check | result |
|---|---|
| `Challenge.lean` vs `Solution.lean` statements, whitespace-normalised | **15/15 byte-identical** |
| declarations only in `Solution.lean` | 1 — `cStar_one_eq_cMT`, the constant identity its docstring declares |
| `ChallengeDeps.lean` counting functions vs `Zeta23/Statement.lean` | **9/9 identical** (`Ncount`, `Ndist`, `N0`, `N0star`, `N0simple`, `Nsimple`, `zerosIn`, `zeroMult`, `IsNontrivialZero`) |

The counting functions are defined against Mathlib's own `riemannZeta` and `analyticOrderAt`,
not an assumed form. **So the statements the solution proves are the statements the challenge
file states, and those are stated in Mathlib's vocabulary.** What remains for a promotion is
the kernel re-run — that the delegation typechecks and the axiom set is clean — which the
repository records but which no independent party has re-executed. **The remaining gap is
narrower than the tier label implies, and it is precisely locatable.**

## 4. A finding against the site's audit, not against the mathematics

VibeMathed's verification note says it *"audited the sources at tag v1.0"* and reports
*"no sorry under Zeta23/, the **27** real ones all in the comparator/Challenge files."*

**At v1.0 the count is 33, not 27.** The repository's own `AUDIT.md` contains both numbers, in
two revision sections: an earlier bullet reads *"Occurrences of the `sorry` token outside
comments: **27** ... (`Challenge.lean`: 15, `Challenge/Multiplicity.lean`: 12)"*, and a later
one, covering the revision that **adds `Zeta23/XiPrime/` and its six statements**, reads
*"Occurrences ... **33**, all in the three trusted challenge files."* The site quoted the
superseded line.

**This is an audit-trail finding, not a soundness one.** All 33 are deliberate placeholders in
challenge files; the site's *conclusion* is correct and its reasoning is sound. But the number
is stale, and the staleness is diagnostic: **it shows the source audit was a read of the
repository's own audit record rather than an independent count.** Reading someone's audit is
not auditing. That distinction is the whole premise of this programme, and here is a clean
instance of it — in the corpus's single most significant entry, from the site whose
verification labelling arm AJ praised.

*(The repository is not at fault: it updated its own number correctly when XiPrime landed.)*

## 5. The control case — and it refutes my barrier predicate

**This is the control I said in arm AJ was the binding requirement, and it arrived without my
choosing it.** I selected this paper as the top of the audit queue by significance, not because
it declares a barrier. It declares one anyway:

- §7.2 defines a *bandwidth-one certificate* and proves, in Lean
  (`Zeta23.PairCeiling.ceiling_law256`), that no such certificate exceeds ≈ **0.682**.
- §7.2(a): the restriction `X ≤ T` "comes from Proposition 5.4"; going past it "would require
  information on prime pairs (the Hardy–Littlewood conjectures, or equivalently Montgomery's
  pair correlation conjecture for support > 1)" — a named open problem, exactly the rank-429
  shape.
- §7.2(e): "unconditionally, higher moments add nothing."
- §1.4 is titled *What the results are not*.

So here is a paper that **doubles the record on a fifty-year ladder and bounds its own method
in the same breath**, within 0.0152 of the ceiling it proves. Barrier declaration therefore
does **not** mark an exhausted board. It marks a careful paper. My predicate — "a named
obstruction the practitioners state themselves, with a numerical ceiling attached" — fires
here, on the least exhausted board in the corpus.

**Retire the predicate as an instrument.** I flagged in arm AJ that widening it would make it
fire on every discussion section ever written; this is that prediction confirmed on the first
neutral sample. What barrier language actually indicates is *rigour*, not exhaustion. Rank 429
and the union-closed ceiling are still real board-exhaustion instances — but I identified them
by reading their mathematics, not by detecting their rhetoric, and only the former generalises.

## 6. Trajectory data — the richest instance this programme has seen

Appendix B is an unusually complete account, and it bears directly on the trajectory-publication
question (arm U3). Recorded, from the paper and the site's `aiRole` field:

- Session 1 attacked RH directly: ~650 candidate approaches generated, 106 survived adversarial
  review as internally consistent fragments, **none as even a partial proof**.
- Session 2: ~60 subagents, ~2,400 shell commands, 54 arXiv papers read, ~**31 million output
  tokens**. Attribution: **2 subagents produced the key steps, 13 fed them, 30 failed, 13
  refereed, 2 drafted**.
- **The result was a byproduct of failing at the stated goal.** Agent E2 was launched to bound
  the Pontryagin index *from above*; it found that route "empty — computed from primes, the
  negative index of any finite compression is identically zero, which bounds nothing" — and
  then inverted the same bookkeeping to get the dual count. The search was not aimed at
  proportions of zeros until after the 1/2 claim survived review.
- Method worth stealing: every agent got **control objects for which the analogue of RH is
  false** (Davenport–Heilbronn, Epstein with class number > 1, Beurling systems with planted
  off-line zeros), and the surviving line survived *because the controls under-certified*.
  Reviewers were blind to each other and each assigned a specific failure mode rather than
  asked to "check the proof"; a fresh agent reproved the key step from the statement alone.
- The model declined the initial encouragement to "take a big leap of faith", on the record,
  and stopped at "past the point where more of me looking at it adds information. It needs a
  human analytic number theorist."
- The paper **self-corrects an attribution** in print: priority for the Fejér-kernel case is
  Aryan's, and the body was amended accordingly.

## 7. On the human review, and the site's honesty about it

The site's note reads: *"two Anthropic mathematicians validated the work, and Brian Conrey and
Dan Goldston examined the paper. Examination is not endorsement, and Goldston is an author of
the prior work this builds on."* That conflict note is sharper than most journals would print,
and it is the reason arm AJ's assessment of the labelling stands even after §4: **the site
states its own limits accurately; what §4 shows is that one of its numbers was inherited
rather than recomputed.**

## 8. Next

1. **The kernel re-run is the whole remaining gap** on this entry, and it is one command
   (`lake exe cache get && lake build && lake env lean comparator/PrintAxioms*.lean` plus the
   comparator tool). It needs a Lean toolchain and a Mathlib cache — not available here. That
   is a concrete, bounded task for an environment that has them.
2. **Report the stale count.** §4 is a correction the site would plausibly want; its own
   changelog is public and per-entry discussion threads exist.
3. **Predicate retired; the audit queue is the live programme.** 22 `lean-checked` and 327
   `unreviewed` post-cutoff entries remain (arm AJ §5), and two of the three known-bad entries
   in the whole corpus were caught by exactly the checks run here.
