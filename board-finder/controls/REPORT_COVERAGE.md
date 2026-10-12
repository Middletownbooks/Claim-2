# Report — the second rater on T3's coverage column

Scored against `PREREG_COVERAGE.md`, which was committed before the rater was asked,
by `score_coverage.py`, which was committed before the rater's answer existed.
Verdicts as transcribed: `coverage_verdicts.json`. Arithmetic checked independently:
`verify_coverage_arithmetic.py`, and for the measure board `verify_arm3_mechanism.py`,
committed earlier still.

## 1. The mechanical result

```
agreement: 6/6
  B-1: PASS  declined = ['02-cap-set', '09-vinogradov', '13-pcp']
  B-2:04: PASS  scale="the deviation from 1/2 in units of sqrt(delta) ..."  matched=['delta']
  B-2:08: PASS  scale='the discrepancy in units of sqrt(n) ...'            matched=['discrepanc']
  B-3:    PASS  scale='the cube half-width (side parameter) C of [-C,C]^n' matched=['side','cube']
  B-4:    n/a   not applicable: 0 flips
  B-5: PASS  declines lacking a structural reason: []
```

Both pre-registered failure conditions are retired. Agreement is not ≤ 4/6, and it is
not a *different* three that declined — which the prereg named as the worse outcome,
because it would have made the threshold-vs-per-round dichotomy mine rather than the
boards'.

## 2. What the mechanical result is worth

The prereg said this in advance and it still holds: **6/6 is consistency, not truth.**
Two raters of similar training, on six famous boards, can agree for reasons that have
nothing to do with the boards. What the run establishes is narrower and still worth
having: the split is *reproducible from the before-board alone*, by someone who was not
shown the after-boards, the dichotomy, or the existence of a split.

## 3. Where the scoring rule over-credited me, and what actually happened

`B-2:04` passed on the substring `delta` occurring inside `sqrt(delta)`. That is not the
prediction I made. I predicted the scale parameter would be **δ, the bound on ‖vᵢ‖²**;
the rater named **the constant C in the target's 1/2 + C√δ**.

Both solve the same inequality, `t ≥ √(2δ ln 2n)`, for different variables — mine for δ
at a fixed target constant, the rater's for the constant at fixed δ — and both put the
`Θ(√log n)` in the invariant rather than in the move. So the *cap* agreed and the
*quantity* did not, and B-2's own wording was "wording may differ, the quantity may not."
On its own terms that prediction missed.

The rule is left exactly as committed and this adjudication is recorded beside it. Editing
the predicate after seeing the answer is the move this programme exists to catch, and the
right time to catch a loose predicate was the self-test — which is where the `" t"`
substring was caught, and where this one was not.

## 4. Three corrections the rater forced

**(a) T3's inference sentence was wrong as written.** It said: *"If it is not O(1), no
improvement to the move can reach O(1)."* A cap computed from the invariant is a cap **on
the invariant**. On `04-kadison-singer` and `08-spencer` the incumbent move is itself
lossy *and the target is true* — Marcus–Spielman–Srivastava, Spencer — so the cap says
the certificate must be replaced, not that the bound is unreachable. Only where the move
is **monotone** in the invariant does the original sentence hold literally, and of the
three parsing boards that is exactly one: Banaszczyk's measure board, where the move can
only shrink measure, so the requirement fails before the move is specified at all.

`PROMPT.md`'s T3 now asks for the monotonicity check and says which of the two conclusions
a cap licenses. This is the second patch T3 has taken from a control run, and D37's warning
about patch-from-the-item-that-broke-it applies to it — with the difference that this one
*narrows* a claim rather than adding a discriminator.

**(b) Only one of the three parsing boards is a literal fit.** On `04-kadison-singer` the
rater flagged its own reconstrual: a matrix Chernoff bound is a tail statement about a
random process, not a predicate a state satisfies at scale C. What is scale-indexed is the
certificate's *resolution* at the target norm. Coverage is therefore better stated as
**1 literal + 2 by one step of interpretation + 3 declined** than as "3 of 6".

**(c) The decline clause earns its place more sharply than I argued it did.** I justified
it by saying a forced respondent would invent a threshold. On `13-pcp` the rater showed
worse: forcing the most plausible scale — the size exponent — yields **no cap**, since for
fixed constant soundness the repetition count is O(1) and the size polynomial. A forced
answer there does not merely invent a threshold; it invents one pointing the *wrong way*,
and it would have scored as a pass. The genuine obstruction on that board is that any
k ≥ 2 gives size ≥ n², which is cost accounting and not a threshold at all.

## 5. Arithmetic

Every number the rater produced reproduces independently:

| board | rater | recomputed here |
|---|---|---|
| 04-kadison-singer | `t ≥ √(2δ ln 2n)`, so `min C = √(2 ln 2n)` | 3.255 at n=100, 6.545 at n=10⁹; closed form confirmed against a bisection on the crossing point |
| — variance step | `‖Σ‖vᵢ‖²vᵢvᵢᵀ‖ ≤ δ‖Σvᵢvᵢᵀ‖ = δ` | holds in every trial on random exactly-isotropic systems; worst ratio 0.743 |
| 08-spencer | `min C = √(2 ln 2n)`, i.e. `Θ(√(n log n))` | same threshold |
| K1-to-K3 | `γₙ(K_C) ≥ ½` iff `C²/2 = ln n − O(log log n)` | `min C / √(2 ln n)` = 0.854 at n=10 rising to 0.958 at n=10⁹; at fixed C the measure is `e^{−c(C)n}` with c(2) ≈ 0.0466 |

The measure-board figure was fixed in `verify_arm3_mechanism.py` **before** any answer was
read, including the direction of approach — from below and increasing — which an earlier
version of this programme had backwards.

## 6. What this arm does not show

It says nothing about whether T3 is a useful **screen**. A question can be perfectly
well-posed on three boards and tell you nothing on any of them. That is arm 3's job, and
this result must not be quoted for it.

One partial exception, stated precisely because it is tempting to overclaim: this rater,
blind and under a different framing, independently computed T3 on the **measure**
invariant and returned *a cap at Θ(√log n), literally independent of the move*. That is
one half of arm 3's pair. The other half — T3 on the directional-TV invariant, where it
must return *no cap* — is what arm 3 exists to get, and `PREREG_ARM3.md`'s A-5 says it
outright: **the pair is the whole test, and one arm cannot pass it.**
