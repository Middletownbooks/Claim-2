# Report — arm 3, the test T3 had not had

Scored against `PREREG_ARM3.md`, committed before the respondent was given anything.
Arithmetic checked two ways: `verify_arm3_mechanism.py` (committed **before** any answer
was read, fixing both sides of the pair) and `verify_response_arm3.py` (six checks on what
this respondent actually computed). All of it reproduces.

## 1. The verdict on the pre-registered question

**T3 discriminates.** A-5 — the failure condition — does not fire.

| | prediction | outcome |
|---|---|---|
| A-1 | T1 = yes | **correct.** "Yes… So this is not a restatement of the theorem," with a closed-form check on an explicit cos² product density |
| A-2 | T2 = formula | **wrong.** "Existence theorem, and an unnamed one" |
| A-3 | T3 = no cap | **correct.** min κ = Θ(1/C); the threshold is O(1) |
| A-4 | the respondent derives the averaging behaviour itself | **correct, and over-delivered** |
| A-5 | if A-3 fails, T3 does not discriminate | **did not fire** |

**A-2 being wrong is what makes the test pass.** The pre-registration asked for an item
where T3 answers differently *while T1 and T2 do not*. That is exactly what happened:
across the pair, T1 says yes/yes, T2 says existence-theorem/existence-theorem, and only T3
separates — a cap at Θ(√log n) on the measure invariant against **no cap** on the total
variation one. So D37's question, *is T3 merely re-detecting T1 and T2?*, is answered **no**,
and it is answered by the arm that could have said yes.

What A-2's failure does cost is an anatomy claim, below.

## 2. The computations, and they are better than predicted

A-4 predicted the respondent would derive that directional TV behaves as an *average* over
coordinates rather than a product. It did more than that — it produced the optimal constant
and a matching lower bound:

* **Upper.** With ρ(x) = Π g(xⱼ), g(t) = (1/C)cos²(πt/2C), the score Yⱼ = (g′/g)(Xⱼ) has
  mean 0 and variance the Fisher information I(g) = π²/C², so
  V_u(ρ) = E|Σⱼ uⱼYⱼ| ≤ √(Σⱼ uⱼ² I(g)) = (π/C)‖u‖₂. **No n.**
  Reproduced: ∫g = 1.000000000 and I(g) = π²/C² at C = 0.5, 1, 2.5 to six digits.
* **Optimality.** π/C is the best a product density can do, because the minimum Fisher
  information of a density on an interval of length L vanishing at the ends is 4π²/L² — the
  square-well ground state. Reproduced by discretising the Dirichlet Laplacian: 4λ₁ matches
  4π²/L² to 1e-4 at L = 1, 2, 5, and equals π²/C² at L = 2C.
* **Lower.** Projection contracts directional TV, so V_u(ρ) ≥ TV(f_u) ≥ 2 sup f_u ≥
  2/width = 1/C. Monte Carlo at n = 200 puts V_u ≈ 2.42 ∈ [1/C, π/C], and flat in n.

So min κ = Θ(1/C), and the target satisfies the invariant at constant κ once C = Ω(1).
That is the "no cap" answer, and it is not a judgement call.

## 3. The board is dead, and the kill test is what killed it

T1 passed. T3 passed. The board still cannot work, and the respondent's kill test is exact:

> **V_u is translation-invariant; the terminal condition is not.**

V_u(τ_aρ) = V_u(ρ) by change of variables — reproduced to machine precision. The move is
translation-equivariant, and the STATE slot pins the body to nothing. So any legal run has a
translate that is equally legal, with *identical invariant values at every step*, whose final
body misses the origin by as much as you like: every body in the run has Euclidean radius
≤ C√n + n, so take ‖a‖ larger. Concretely with every vᵢ = e₁, translating by 2n·e₁ preserves
every invariant value and would conclude Σεᵢe₁ ∈ C·B_∞ + 2n·e₁, false for C < n.

The dichotomy is clean: either no κ-preserving run exists (the scheme is vacuous) or the
invariant does not imply the terminal (it is unsound).

The respondent also found the board's move is not even satisfiable by the identity choice:
with K the unit disc and v = e₁, the point (0,1) ∈ K lies in neither translate, so U = K is
illegal. Reproduced.

**This is the second time in this programme that T1 and T3 have both passed a board that
cannot reach its target, and the second time the kill test caught it.** The instrument's
design — candidates must arrive with their own refutation — is doing the work that the triage
questions cannot.

## 4. What this costs me: the pair differed in two slots, not one

`PREREG_ARM3.md` says the pair is "the same problem, the same target, and *the same move*,
with **only the invariant changed**." That is false as I constructed it. Arm 1's STATE was
*"a symmetric convex body K"*; arm 3's STATE was *"a convex body K … together with a
probability density"*. **I dropped the symmetry qualifier.** The kill test is precisely an
exploit of the slot I changed without registering.

Worse, the contradiction was already visible in this project's own file. `FINDER.md`'s
anatomy table lists the state row as *symmetric convex body* against *convex body + a
density on it* — and the prose beneath it says "K1 and K3 differ in exactly one slot" and
"Same state, same move, different invariant." The table refutes the prose. Fixed now.

This is the **second symmetry mis-statement of mine in a control input**: the negative
control's input wrongly said the gluing lemma's bodies are *symmetric* when they are not,
and that one was also caught by a respondent rather than by me.

**Does the confound invalidate A-3?** No, and the reason is checkable rather than a plea.
T3 evaluates min{C : the invariant holds for the *target* at scale C}. Both sides of the
pair compute that on the same target — the cube — and neither computation references the
symmetry of any intermediate state: the measure side is γₙ([−C,C]ⁿ) ≥ ½, the TV side is
min κ over densities on the cube. The dropped qualifier changes which *runs* are legal, which
is what the kill test exploits; it does not touch either threshold. So the discrimination
result stands and the construction error is recorded against the anatomy claim, where it
belongs.

## 5. A third answer T3 needs, and the honest limit on T3 now

The respondent found something the two-answer form of T3 cannot express. κ_min(C) = Θ(1/C)
is **decreasing** in C: the invariant is *easier* for bigger bodies. It is a
"the density is spread out" condition, and via the same marginal bound it forces every state
to be **wide**, a lower bound on size. An invariant that relaxes as the body grows cannot be
what forces the final object to be small or to sit anywhere.

So "no cap" came back for the wrong reason. The threshold is O(1) not because the invariant
is cheap to maintain at the target but because **it is not binding at any scale** — 100% of
the work is pushed into the move, which then has to do something the invariant cannot
license. T3 now admits that third answer explicitly.

**And that is the third patch T3 has taken from a control run** — the decline clause from the
coverage measurement, the monotonicity clause from the coverage rater, and now the
not-binding clause from arm 3. The count matters more than any individual patch:

> T3 is now a heavily fitted instrument. Every clause in it was added by someone here after
> seeing a response from a run designed here. It discriminated on the one pair built to test
> it, and that pair turned out to differ in two slots rather than one. **Its next use should
> be scored on an item this project did not construct.** Until then it is quotable as a
> question worth asking and not as a validated screen.
