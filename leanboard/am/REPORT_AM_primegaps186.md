# Arm AM — `openai/PrimeGaps186`: the `lean-checked` tier doing exactly what it says

**Target.** `H₁ ≤ 186` — the bounded-gaps direction (Zhang → Maynard → Polymath), *not* the
maximal-gap lower bound audited in arm AL. VibeMathed entry "Prime Gaps at Most 186",
significance 62, `lean-checked`, `ai-discovered`, model GPT 6 Astra, no human collaborators,
`solveDate` 2026-09-03. Repo cloned at HEAD `61340d0`: two Lean files, **211,603 lines**, plus
`prime_gap_186_certificate.py` and `short_gaps_numerics.pdf`.

**Verdict up front.** The mathematics I can check, checks — 22/22. The reason this sits at
`lean-checked` rather than `lean-verified` is real, precise, and larger than in any artifact
audited so far: **the development declares three project-specific axioms, and it declares them
in `Challenge.lean`, the trusted statement file.**

---

## 1. The finite check I *can* complete: the admissible 40-tuple

`Challenge.lean` fixes an explicit tuple and the whole corollary rests on it being admissible.
That is a finite check, and it passes completely:

- **40 distinct elements**, sorted, starting at 0. ✅
- **Diameter exactly 186** — `max − min = 186`, the headline constant. ✅
- **Genuinely admissible**: for every prime `p`, the tuple misses at least one residue class
  mod `p`. Checked for all `p ≤ 186`; only `p ≤ 40` could have failed, since 40 elements
  cannot occupy `p > 40` classes. ✅
- The binding case is `p = 2`: every element is even, so class 1 is free. Mod 3, only two of
  three classes are occupied. ✅

**This is one component fully verified, not merely read.** If the tuple were inadmissible the
corollary would be false outright, and it is not.

## 2. The three axioms, assessed individually

They are declared at `Challenge.lean:48`, `:52`, `:896` — and identically at
`PrimeGaps186.lean:147`, `:159`, `:1055`.

**(1) `kloosterman3_bound` — Deligne, exactly.**
`normalizedKloosterman3 p c = p⁻¹ · Σ_{uvw=c} ψ(u+v+w)`, asserted `‖·‖ ≤ 3` for `c ≠ 0`.
This is Deligne's hyper-Kloosterman bound `|Kl_n(a;p)| ≤ n·p^{(n−1)/2}` at `n = 3`: the
normaliser `p` is exactly `p^{(3−1)/2}`, and the constant `3` is exactly `n`. The definition is
also correct in a detail worth naming — summing `u,v,w` over all of `ZMod p` is harmless
because `c ≠ 0` forces all three to be units. **A true, deep, standard theorem that Mathlib
does not have. Defensible as an axiom; a reference would settle it.**

**(2) `kloosterman2_correlation_bound` — the one that needs a citation.**
`‖Σ_{t≠0,−1} Kl₂(A/t)·Kl₂(B/(t+1))‖ ≤ 8·p^{3/2}` for all `A,B ≠ 0`.
Weil gives `|Kl₂| ≤ 2√p`, so the trivial bound on the `t`-sum is `(p−2)·4p ≈ 4p²`. The axiom
claims `8p^{3/2}` — **stronger by a factor of about `√p/2`** (4.9× at `p = 101`, 158× at
`p = 100003`). That is full square-root cancellation in the `t`-sum, a Katz-type correlation
estimate for Kloosterman sheaves, **asserted uniformly over every pair `A,B ≠ 0` with no
exceptional set.** The uniformity is the part I would want a reference for: correlation bounds
of this shape usually depend on the two sheaves being geometrically non-isomorphic, which is a
condition on the pair. I cannot settle it here and do not claim it is wrong — I claim it is the
axiom carrying the most weight per line of justification.

**(3) `physical_integral_bounds` — not a theorem at all, but a computation.**
This asserts explicit rational bounds on **39- and 40-dimensional integrals** against
`Measure.pi` of a `trialPhysicalMeasure`. Counted from the source:

| | list entries | bounds each | total |
|---|---:|---:|---:|
| outer (`Root` and `Face`) | 52 | 2 | **104** |
| inner (`Mass`) | 45 | 1 | **45** |
| caps (`trialIH` ×2, `trialJLambdaH`) | — | — | **3** |
| | | | **152 scalar bounds** |

**This independently reproduces the site's "104 outer, 45 inner and 3 cap"**, and explains the
decomposition: the outer clauses assert two bounds per entry. Unlike (1) and (2) this is not a
citable result — it is a numerical certificate, computed outside Lean (the repo ships
`prime_gap_186_certificate.py` and `short_gaps_numerics.pdf`) and asserted into it. **It is the
load-bearing axiom and the one with no external literature to check it against.**

## 3. The structural point: the axioms are in the *trusted* file

In `anthropics/zeta-23-lean` (arm AK), `Challenge.lean` contained only theorem statements with
`sorry` placeholders; the permitted axiom set was Lean's three standard ones, and the
comparator's job was to confirm the solution proved those statements within that set.

Here `Challenge.lean` contains **three `axiom` declarations followed by three `sorry`'d
statements** (`dhl_40_2`, `infinite_two_prime_translates_admissibleTuple`,
`primeGapLiminf_le_186`). So the assumptions are part of the agreed trusted base *by
construction*. The site's phrasing — "Comparator and Lean's kernel accept them — but all three
depend on three project-specific axioms" — is exactly right, and the two halves of that
sentence are not in tension: **the kernel accepts them because it was told to.**

This is transparent, not deceptive: the axioms are named, typed, and sitting at the top of the
file anyone would read first. But it means the machine check certifies a *deduction from stated
assumptions*, not a proof of `H₁ ≤ 186`.

Otherwise the source is clean: **no `sorry` in the solution file**, no `native_decide`, no
`unsafe`, no `implemented_by`. The 247 uses of `decide` are kernel-evaluated and unobjectionable.

## 4. Where verification stops — a typology from four audits

Four artifacts now audited, and each stops in a different place. This is the programme's real
subject, so it is worth tabulating:

| artifact | arm | project axioms | where the audit actually stops |
|---|---|---:|---|
| `anthropics/zeta-23-lean` | AK | 0 | statement fidelity — the kernel re-run nobody independent has done |
| `openai/LongGapsBetweenPrimes` | AL | 0 | **no mathematician has read it**; the build is done |
| `plby/lean-proofs` (Erdős 4) | AL | 0 in-repo | a **pinned, locally patched** external `BoundedGaps` dependency |
| `openai/PrimeGaps186` | **AM** | **3** | **the axioms themselves** — one classical, one needing a citation, one numerical |

"Lean-checked" is not one condition. It names at least four distinct failure surfaces, and only
the last of them is visible from an axiom listing.

## 5. Two records in one day, both conditional in different ways

`H₁ ≤ 212` (Axiom Math, nine named authors) and `H₁ ≤ 186` (GPT 6 Astra, no human author) are
both dated **2026-09-03**, both `lean-checked`, both at significance 62. Their conditionality
differs in kind: per the site, the 212 certificate is "conditional on the equidistribution
estimates and the Bombieri–Vinogradov theorem stated in the paper, so it certifies the
deduction rather than the analytic inputs"; the 186 certificate is conditional on the three
axioms above. **The record was pushed twice in one day by two labs, and neither artifact
certifies a complete proof — each certifies a deduction from a named frontier.**

The ladder checks: 70,000,000 → 4,680 → 600 → 246 → 240 → 236 → 212 → **186**, strictly
decreasing, with 186 comfortably below Polymath8b's long-standing 246 and below the same-day
212. And 186 is even, as any bound coming from an admissible tuple's diameter must be.

## 6. Next

1. **Axiom 2 is the one to chase.** A literature reference for a uniform
   `O(p^{3/2})` correlation bound on `Σ_t Kl₂(A/t)Kl₂(B/(t+1))`, valid for *all* `A,B ≠ 0`,
   would move this entry materially. Katz's *Gauss Sums, Kloosterman Sums and Monodromy* is
   where I would look first. This is a literature question, not a compute question.
2. **Axiom 3 is checkable in principle and expensive in practice** — 152 bounds on
   39-/40-dimensional integrals, with a Python certificate shipped in the repo. Re-running that
   certificate independently is a well-defined task for an environment with the budget.
3. **Axiom 1 needs only a citation** to be discharged, or a Mathlib contribution to be removed.
4. The typology in §4 suggests the census's `lean-checked` bucket should be read as *at least
   four different situations*, and that an axiom listing catches only one of them.
