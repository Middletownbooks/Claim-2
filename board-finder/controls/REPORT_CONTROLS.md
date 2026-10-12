# The two control runs — the rubric separates, and it corrected me three times

**Headline: the instrument discriminates.** The positive control returns **T1 = yes**
("a clean pass, which is rare here"); the negative returns **T1 = no — as recorded this
is a RESTATEMENT". That is the only claim the controls carry, and it holds. Prediction
C-6 — that the instrument would fail to discriminate and `PROMPT.md` would need an
explicit equivalence clause — does not apply.

Three of six predictions held. The three failures are all about **my** assumptions, and
they are the informative part.

| | prediction | outcome |
|---|---|---|
| C-1 | positive returns T1 = yes | **HELD** |
| C-2 | positive returns T2 = **formula** | **FAILED** — both respondents say *existence theorem*, independently, and they are right |
| C-3 | negative returns T1 = no, caught as a restatement | **HELD** |
| C-4 | negative is *not* caught (the contradictory twin) | **FAILED** |
| C-5a | positive is recognised and named | **HELD** |
| C-5b | negative is described but *not* named | **FAILED** — named as Banaszczyk's argument "with the class left abstract" |

Every verdict above is backed by a quote found verbatim in the response file;
`score_controls.py` fails if one is not. Every computation in both responses was
re-derived here (`verify_response_positive.py`, `verify_response_negative.py`) and all
of it checks out.

## 1. What the controls corrected in my own work

**(a) Banaszczyk's move is an existence theorem, not a formula.** My `benchmark.json`
listed T2 examples for Guo–Fang–Lu and Bansal–Jiang and left Banaszczyk unclassified; I
filled the gap wrongly in the prediction. Both respondents killed both formula readings
with computations I reproduced: `K ∩ (K−v)` is legal but loses measure (the slab
|x₁| ≤ 0.68 has γ = 0.5035; shifted by 0.2 and intersected it drops to **0.3688**), and
`conv((K+v) ∪ (K−v))` keeps the measure but is not a *subset* of the union, so the
sign-selection it is meant to license does not exist. What the move needs is a lemma
whose iteration **is** the theorem.

**(b) My negative-control input was defective.** It said "a class of **symmetric**
convex bodies". The gluing lemma's bodies are not symmetric, and symmetry cannot be
restored — with K = B₂ and v = e₁ the two translates are externally tangent at the
origin, the union contains no ball around 0 (reach in direction u is exactly 2|u₁|), so
every symmetric convex subset has empty interior and is γ-null. Verified. The defect did
not change the verdict, and it would have if the respondent had been less careful.

**(c) The iff I inherited is in doubt.** `PREREG_CONTROLS.md` C-3 predicted the reason
would be the equivalence: a class closed under the move with the terminal property
exists *iff* the conjecture holds — which is how the reference corpus reports the
original proof. The respondent declines it:

> It is not quite equivalent to the theorem — the closure scheme implies Komlós by
> unwinding, but the converse is not automatic, so it is a possibly-stronger certificate
> scheme rather than a literal logical restatement.

So the negative control is a restatement-**or-stronger**, and the corpus's "if and only
if" is the claim now needing a check. `benchmark.json`'s description of the negative
control is corrected accordingly. **This also exposed that my scoring rule had two cases
and needed three:** §5 said a correct verdict with a wrong reason is a lucky verdict, and
did not anticipate a reason that is *different from the predicted one and better*. That
fails the prediction, not the response, and the harness now says so instead of picking
the flattering reading.

## 2. The finding neither respondent was asked for, and both produced

They had different boards and no knowledge of each other. Both derived the **same
structural cap**, and both located it in the same place:

> *positive:* any board of the shape "invariant μ(K) ≥ θ with θ fixed; terminal =
> nonempty ⟹ 0 ∈ K" outputs an l_∞ bound of at least min{C : μ(cube_C) ≥ θ} … Improving
> the move-lemma cannot help; the slot design itself sets the answer.

> *negative:* the T1 computation **is** the whole bound … the cap is entirely in the
> starting-state check, because the invariant is *exactly* conserved along the n steps.

Verified independently: γ_n([−C,C]^n) = erf(C/√2)^n, so the invariant is false at
initialisation once n ≳ e^{C²/2} — even the unit cube fails at n = 2 (γ₂ = **0.4661**) —
and C_min(n) = √(2 ln n)(1−o(1)). The max-n table reproduces exactly: 1, 14, 256,
10 942, 1.21×10⁶, 3.5×10⁸, 4.55×10²² for C = 1…10.

**This is the same mechanism `verify_mechanism.py` computes for the multiplicative
invariant, reached blind, twice, and stated better than I stated it.** The positive
respondent names the trade exactly: *the fixed threshold 1/2 is simultaneously what makes
the composition lossless and what forbids the conjecture.*

## 3. A third discriminator, which the controls earned

T1 and T2 both **pass** on a board that cannot reach the target. So they are not
sufficient, and the missing test is one line:

> **T3. Evaluate the invariant's threshold on the target state. Does it already cap the
> bound?** Compute min{C : μ(target_C) ≥ θ}. If that is not O(1), no improvement to the
> move can make the board reach O(1).

It is cheaper than either existing triage question and it catches Banaszczyk's board
immediately. `PROMPT.md` now carries it as step 5's third question. Note what it is *not*:
a reason to reject a board. Banaszczyk's board is the best known result on this problem
and has stood for nearly thirty years. T3 says where its ceiling is, which is exactly the
`SATURATION` reading in `FINDER.md` — and it is the discriminator that would have flagged
the D28 blind spot, where a ratio test sees nothing because both sides are O(1).

## 4. The live opening, found unprompted

The negative respondent ran a necessary condition of its own devising —
μ((K+v) ∪ (K−v)) ≥ 1/2 whenever μ(K) ≥ 1/2 — and reported:

* **hard cutoffs die.** Uniform on [−a,a]^n with a diagonal shift retains
  ≈ e^{−√n/(2a)} of its mass. Verified at a = 1, 2, 5 and n = 100, 10⁴: 5.9×10⁻³,
  1.7×10⁻²², 8.0×10⁻², 1.3×10⁻¹¹, 3.7×10⁻¹, 4.5×10⁻⁵.
* **soft cutoffs survive**, giving mass e^{−Θ(1)} to a constant-side cube — "so the
  barrier is specific to the *standard* Gaussian, not to the measure-invariant family as
  such", with the honest caveat that the gluing lemma is Gaussian-specific and nobody has
  it for a soft-truncated measure.

That is the direction the real advance took — a density-based invariant rather than a
Gaussian measure — identified from the board alone by a respondent that was not asked to
propose anything.

## 5. What these two runs do not establish

* **n = 2.** Two boards, two respondents.
* **Same model family as the author**, and both recognised the problem and named the
  paper. Field (c) measured that rather than assuming it away, which is its whole
  purpose — but it means these runs test the *rubric*, not a blind search.
* **I wrote both inputs**, and one of them had a defect (§1b). Both are committed
  verbatim so the leading can be judged.
* The search arm is still unrun: it needs the six-item benchmark and an API key this
  container does not have (D18).

## 6. My own error rate, since this project keeps count

Four verification predicates of mine were wrong in this session while the claims they
tested were right: two in `verify_mechanism.py` (a ratio direction and "flat" for
"bounded uniformly"), one `erf` saturation that scored a correct table as failing, and
one wrong witness here — I tested (0.02, 0.02) for being outside a union that contains
it, when the escaping directions are the near-vertical ones. The respondents' claims
survived all four checks. That is consistent with the ledger's standing lesson on this
project, and it is the reason every number above was recomputed rather than read.
