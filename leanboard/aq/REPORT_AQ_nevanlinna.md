# Arm AQ — Nevanlinna's half-plane problem: the scaffolding checks, the core does not reduce to computation

**Target.** VibeMathed "Nevanlinna half-plane problem", significance 45, **`unreviewed`**,
`resolution: resolved`, `disproved`, `resolutionMethod: construction`, model **GPT-5.6 Sol Ultra**,
seven human collaborators, arXiv:2608.26062 (26 Aug 2026).

**What is unusual about the input.** The user supplied not the paper but the **raw agentic session
behind it** — a 7 h 14 min run under an explicit Chinese-language prompt instructing multi-agent
adversarial search and forbidding "numerical indications, approximate violations, random search
results or unproven candidates", followed by a 45 min polishing pass. The final claim in that
transcript matches the published `resultNote` word for word. **This is the first process artifact
this programme has seen for a corpus entry**, and it is far more informative than the paper alone.

**Why this arm exists.** The site's own note is explicit: *"no formalization and no computational
certificate, so there was nothing mechanical to re-run here and **no mathematics was checked**."*
Nobody public has checked it. The construction is explicit, so its analytic and arithmetic
scaffolding can be — and that is what I did.

---

## 1. Everything computable in the construction checks — 22/22

**The Cauchy transform and its Fourier representation.** The note asserts
`C(z) = (1/π)∫ e^{−t²}/(t−z)dt = (i/√π)∫₀^∞ e^{−s²/4}e^{isz}ds`. I derived it independently
(`1/(t−z) = i∫₀^∞ e^{−is(t−z)}ds` for `Im z > 0`, then the Gaussian transform) and confirmed the
two integrals agree numerically to **2.3·10⁻¹⁹**. The three bounds that follow are exactly right:
`∫₀^∞ e^{−s²/4}ds = √π` gives `|C| ≤ 1`; `∫₀^∞ s e^{−s²/4}ds = 2` gives `|C′| ≤ 2/√π`; and
Sokhotski–Plemelj gives `Im C(x) = e^{−x²}` on `ℝ`, confirmed to `1.1·10⁻¹²`. The bi-Lipschitz
constant `δ = 2ε/√π = 0.001128379… < 0.00113` as stated.

**The graph bound (1) is tight, which is the tell.** The claim `β(X) ≤ ε e^{ε²}e^{−X²/2}` reduces,
under `|X − t| ≤ ε`, to `X²/2 − 2ε|X| + 2ε² ≥ 0`. That expression is **identically
`(|X| − 2ε)²/2`** — verified in exact rationals — so it is non-negative with **equality exactly at
`|X| = 2ε`**. The factor `e^{ε²}` and the exponent `X²/2` are not slack constants chosen for
safety; they are the precise values that make the inequality hold with nothing to spare. **A
fabricated estimate is not tight.**

**The `Γ(2)` orbit.** For every `m ∈ [2,60)` and every `d` coprime to `2m`: `det γ_{m,d} = 1`,
`A` and `d` odd, `B` even — so `γ_{m,d} ∈ Γ(2)` as claimed. The closed form
`γz₀ = A/(2m) − 1/(2m(2mz₀+d))` is correct; `Im(γz₀) = 1/((m+d)² + 4m²)` is correct; and bound (5),
`1/(13m²) ≤ Im(γz₀) ≤ 1/(5m²)` with `0 < Re(γz₀) < 2`, holds throughout — the endpoints `13m²` and
`5m²` being exactly `d = 2m` and `d = 1`.

**The translation `N_m = ⌈√(2 log m)⌉` does its job.** It forces `X²/2 ≥ 4 log m`, hence
`e^{−X²/2} ≤ m^{−4}`, hence `β(Re w) < ½ Im w` — so every orbit point lands inside `Ω₀ ⊂ Ω`.
Checked for all `m < 400`.

**The elementary totient argument is exactly right.** `Σ_{n=2}^{5} 1/n² + ∫₅^∞ dx/x² = 2389/3600`
— confirmed as an exact rational — and `2389/3600 < 2/3`, which is the bound used for `Σ_p 1/p²`.
From it, `S(N) = Σ_{n≤N} φ(n) > N²/6`, verified for every `N ≤ 20000`. The series
`Σ φ(2m)/(m² log m)` tracks `Σ 1/(m log m)` to within a factor of **0.85** over the same range,
so it diverges — which is what breaks the Blaschke condition.

**The Green's function** `G_ℍ(i,ζ) = ½log[(u²+(v+1)²)/(u²+(v−1)²)]` agrees with
`log|(i−ζ̄)/(i−ζ)|` everywhere off the pole.

## 2. What I did **not** check, and cannot

The computable scaffolding is the *support* of the argument, not its load-bearing core. Four steps
are genuinely non-computational and I make no claim about them:

1. **That the Farey path `Γ` can be built** with arcs everywhere below `β` — a limiting/compactness
   construction over infinitely many Farey levels.
2. **Schwarz reflection at the Farey vertices.** The note handles cusps via a local coordinate
   `η = exp(πi(W−k)/N)` and argues the singularity is removable using the width-2 cusps of `Γ(2)`
   and the expansion (3). This is the most delicate point in the whole argument and it is precisely
   where an error would hide.
3. **That `Ω` is a Jordan domain** and that `Φ` extends to the boundary — invoked, not proved, in
   the transcript.
4. **The passage `G_Ω(p,w) ≥ G_{Ω₀}(p,w)`** is correct by domain monotonicity (`Ω₀ ⊂ Ω`), but the
   preceding estimate `Im ζ ≥ ⅓ Im w` for `ζ = ψ^{-1}(w)` is asserted from bi-Lipschitz bounds
   without derivation.

**So: nothing I could check is wrong, and the things I could check are the kind that go wrong when
a construction is confabulated.** That is real evidence and it is not a verification.

## 3. What the transcript reveals that the paper cannot

- **1,017,380 tokens over 7 h 14 m** for the counterexample, then 549,528 tokens over 35 m for the
  rewrite. This is the most precise resource accounting seen in this programme, and it comes free
  with the process artifact.
- **The prompt forbade exactly the failure modes an auditor worries about** — numerical indications,
  approximate violations, unproven candidates — and demanded adversarial re-checking of every
  candidate by independent agents. The human operator engineered against confabulation *in the
  instructions*, which is a different and more interesting control than post-hoc review.
- **The polishing request is a catalogue of known LLM paper-writing failures**, itemised by someone
  who has clearly been burned: missing citations, invented non-standard terminology, reinvented
  wheels instead of citing literature, undefined notation, derivations smuggled into proposition
  statements, unreferenced equations, mis-sorted bibliographies. §2.9 is asked twice in the same
  sentence. **This is a human-written quality-control checklist for AI mathematics**, and it is
  more useful as an artifact than most of the audits in this series.
- **The model reported a negative literature search honestly**, including the caveat that *"a
  negative search cannot logically substitute for absolute priority"* and a recommendation to have
  a domain expert confirm. It also **corrected an easy misreading of Edrei 1955** (the relevant
  theorem carries deficiency or convergence-exponent hypotheses) rather than citing it loosely.

## 4. Two provenance observations

**Concurrent work again — but "independent" was my word, not the evidence's.** The site's note
records He–Zhang, arXiv:2608.24829, dated **25 August** — one day before this paper — *also*
carrying an AI-assistance statement. That is the third instance after the two CDC proofs and the
two `H₁` bounds of the same day. I called the pattern too frequent to be coincidence and read it as
shared method plus shared training data producing correlated discovery. **That inference is
withdrawn**; a mundane social mechanism accounts for at least the CDC pair and needs no claim about
models at all. See `ar/CONCURRENCY_CORRECTION.md`. What the prompts in
`PROMPTS_nevanlinna_translated.md` do show is the *shape* that mechanism predicts: prompt 2 is
"write the proof up as complete English LaTeX code for me" — the find and the write-up are separate
steps by separate models — and prompt 3 carries the priority anxiety explicitly.

**Settled (2026-09-20).** He–Zhang arXiv:2608.24829v1 was supplied and audited in
`ar/verify_hezhang.py` (27/27). The two papers are **not the same mathematical object**: the
domain (Farey-edge chain vs Gaussian-perturbed graph), the obstruction (Green energy /
spherical area vs the Blaschke condition) and the divergence engine (log-mean of λ via
coprime lattice counting vs `Σ φ(2m)/(m² log m)`) all differ. What they share — the target,
λ, and Schwarz reflection — is exactly what EKS26 (arXiv:2604.06136, revised 24 July 2026)
hands out: it poses this as its Question 2 and names λ as the half-plane counterexample.
He–Zhang cite it, thank its authors, prove their Lemma 3.1 "following the idea of [EKS26,
Lemma 6]", and record accessing the revised PDF on 24 August — the same day as the other
paper's timestamped release. Shared ancestor, independent constructions, no communication
required or in evidence.

**The priority chain is checkable, and the site checked it.** A timestamped GitHub release of 24
August anchors the claim, and the site verified it resolves. That is better provenance than most
mathematics offers, AI-assisted or not.

## 5. Verdict

Twenty-two computable claims, all correct, several tight rather than merely true. The
non-computational core — cusp reflection, the Farey-path limit, Jordan-domain boundary behaviour —
is untouched by this arm and needs a complex analyst. `unreviewed` is accurate today; the entry's
`resolution: resolved` is ahead of its evidence, since nobody outside the author group has checked
the mathematics and the site says so.

## 6. Next

1. **This is the right target for an expert referral**, not more computation. The cusp-reflection
   step is where to look.
2. **Ask for more process artifacts.** The transcript was worth more than the paper. If the other
   corpus entries have sessions behind them, those are the highest-value inputs available.
3. **The concurrency pattern deserves its own arm, with the model-level reading withdrawn** — see
   `ar/CONCURRENCY_CORRECTION.md`. The arm's question is no longer "why do models converge" but "which
   of three mechanisms — social seeding, standing scoreboard, or genuine coincidence — produced each
   pair", and the corroboration conclusion holds regardless of the answer.
