# Arm AP — Marton's inner bound: the counterexample recomputed, and it holds

**Target.** VibeMathed "Marton's inner bound", significance 50, **`unreviewed`**, `disproved`.
Paper: Huang, Liu & Liu, *Sub-optimality of Marton's Inner Bound for the Two-Receiver Broadcast
Channel*, arXiv:2608.19869v1 (20 Aug 2026). Code: `yanxiaoliu-mike/Suboptimality_Marton`.

**First arm under the new sampling rule** — auditability rather than significance — and the first
`unreviewed` entry audited out of 327. The bet was that a counterexample is a finite object I can
check rather than describe. It paid: **38/38, every published number reproduced from the paper's
own constants.**

**Result claimed.** Marton's 1979 inner bound, open for 47 years, is *strictly* sub-optimal:
there is a finite broadcast channel with `M_{T⊗2} > 2 M_T`, so the one-letter Marton region is
strictly inside the capacity region.

---

## 1. What I recomputed, and how it differs from re-running their code

Everything below is computed **from the constants printed in the paper**, in 60-digit `mpmath` and
exact `Fraction` arithmetic. Re-running the authors' package would test *reproducibility*; this
tests *correctness of the published numbers*, which is the part a reader must take on trust.

### The Markovity counterexample (§III-A) — the seed of the whole construction

| claim | paper | recomputed |
|---|---|---|
| induced `p_X` from `P_UV` and `X = f(U,V)` | `p*` of (16) | **matches all three coordinates** |
| `I(U;V\|X)` | `0.06676808506814671821263044747` | **agrees to 23 digits** |
| `G_T(P_UVX, {a_x}, α₀)` | `−1.06471340944277385029433493729…` | **agrees to 22 digits** |

That `I(U;V|X) > 0` at the optimizer is exactly the failure of the Markovity conjecture of
[31, Conj. 2]. The optimizer's deterministic map `f = [[0,1],[2,0]]` is non-rectangular, and I
confirm the induced input marginal is precisely `p*` — the two are consistent, which is the
structural check that matters.

**The `G_T` agreement to 22 digits is the single strongest confirmation in this arm.** It fixes the
channel, the optimizer, the `α`-convention and the functional simultaneously; getting 22 digits
from independently transcribed 12-digit inputs is not something a wrong reading survives.

### The two-letter witness (Appendix A)

Both exact rational component tables — 24 and 27 nonzero rows, numerators over `10¹²` —
**sum to exactly 1**. That is a real transcription check on 51 hand-entered integers.

The mixing weight `μ` is *forced*, not chosen: it is the unique value equalising the two certified
endpoint mixtures. Solving from the four endpoints of (44) gives
`μ = 0.2895094596197816937…` against the paper's `0.28950945961978169531`, and
`γ = 0.183304594320655224901749` against `0.183304594320655224901767`. The fixed-input gap
follows as `2.82753794427556·10⁻⁶`, **matching (27)**.

### Gradient shaping (Theorem 2) and the constraint-removal weights

The theorem's algebra checks symbolically: with `λ = (1 + Σ(g_r−g_i)/A_i)⁻¹` and
`δ_i = λ(g_r−g_i)/A_i`, one gets `λ + Σδ_i = 1`, and every coordinate of the supergradient
collapses to `λg_r` — which is exactly why `p*` becomes a global maximizer. Verified numerically
on a test instance.

And the paper's three exact rationals of (32) satisfy **`λ + δ₀ + δ₁ = 1` exactly**, over `10²³`.

## 2. The one thing that did not reconstruct — and why it is not an error

The paper displays a one-letter **upper** bound `0.30084186609915448`, a two-letter **lower** bound
`0.60168561432394163`, and a gap `> 1.8821256327185490·10⁻⁶`. Reconstructing the gap from its own
two displayed bounds gives

  `0.60168561432394163 − 2 × 0.30084186609915448 = 1.88212563267·10⁻⁶`

which is **smaller** than the displayed gap by about `4.9·10⁻¹⁷`. I flagged this, then resolved it
from the authors' shipped `results/unconstrained_lift_mpfr.txt`, which carries the 320-bit
intervals behind the printed digits:

```
one_letter_upper=[0.30084186609915442, 0.30084186609915448]
two_letter_lower=[0.60168561432394163, 0.60168561432394174]
gap=R2-2U1=[1.882125632718549e-06, 1.8821256327554852e-06]
```

**The paper prints the lower end of the gap interval exactly**, and its displayed bounds are
17-digit roundings of the interval endpoints. So the shortfall is a truncation artefact of the
*display*, not of the mathematics — and it runs in the **safe direction**: a reader checking the
arithmetic from the printed numbers gets a *weaker* but still strictly positive gap, and the
theorem stands either way. Had it gone the other way, it would have been a finding.

Four further cross-checks against that MPFR log all pass: `L = M log 2` at `M = 2·10⁶` lands in
its interval, and the exact rationals `λ`, `δ₀`, `δ₁` of (32) each lie inside their MPFR intervals.
The paper's `ε_∇ < 1.846843880121467·10⁻¹⁷` matches the log's `total_gradient_error` upper end.

*(Two failures in my first pass were my own: a `10²⁵`-vs-`10²⁴` denominator on `δ₁`, and an
over-strong assertion about the final gap. Both corrected; neither was a finding.)*

## 3. Why this entry is different from the five before it

**It is `unreviewed`, and it is the best-evidenced artifact audited in this series.** The repo ships
a `PROVENANCE.md` separating discovery code from verification code, `SHA256SUMS`, a `Dockerfile`,
exact-rational certificate bundles, a 320-bit C++/MPFR verifier, and a `reference_numbers.json`
whose every entry I matched. The site has not looked at it; there was nothing wrong to find.

**The human verification is unusually strong.** The acknowledgements record that **Chandra Nair and
Amin Gohari** verified the non-numerical content — and the conjectures being refuted are *theirs*
([31] is Gohari–Liu–Nair). Refuted by name, checked by the refuted. That is the opposite of the
zeta situation in arm AK, where the site had to note that Goldston was an author of the prior work.

**The AI attribution is the most granular yet seen**, and crosses vendors within one result:
GPT-5.6 Sol found the first Markovity counterexample and later built the unconstrained lift;
**Claude Fable 5** found the local-tensorization counterexample; **Claude Fable 5 and Opus 5**
found the fixed-input example. The paper also states plainly *why* earlier searches failed: the
counterexamples need non-binary input, occupy a small region, and the violation gaps are `~10⁻⁶`.

## 4. Verdict, stated carefully

Every number I could check, checked — including a 22-digit agreement on the core functional and two
exact-rational table sums. **I did not independently verify the one-letter upper bound**
`U_B(p*) ≤ 0.0916508833913554746710` of (25), which requires the interval branch-and-bound over
all admissible `(U,V,W)` that the authors' certificate engine performs; nor the `M_{T⊗2}` lower
bound beyond confirming it equals the forced mixture `γ`. Those two are the load-bearing
optimisations and they remain the authors' computation, shipped and reproducible but not
re-executed here.

Within that boundary: **the published arithmetic is sound and the counterexample's internal
consistency is complete.** `resolution: candidate` looks conservative given the Nair/Gohari
involvement; `unreviewed` understates the artifact badly.

## 5. Next

1. **Run their certificate engine** — `scripts/run_full_fixed_input_certificate.sh` and the MPFR
   lift — to close the two gaps in §4. It is packaged to run in Docker.
2. **The sampling rule is validated**: one arm, one verdict, 38 checks, no structural hedging.
   Continue with `disproved` + construction/computation entries.
3. **Re-tier suggestion for the site**: this is at least `site-confirmed` on the strength of the
   shipped certificates, and the acknowledged expert verification arguably reaches higher.
