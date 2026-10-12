# C7 resolved — and case 7 should be restructured

Source: Granville, *Primes in intervals of bounded length*, arXiv:1410.8400v1, 30 Oct 2014
(fetched primary; outranks `CITATIONS_ASSIST.md`). This closes C7 and both after-boards,
supplies two slots Fable left empty, and turns up a structural finding that is worth more
than the citation.

---

## 1. The row: VERIFIED, every field

| P1 field | Granville | verdict |
|---|---|---|
| `S:` sieve weights λ_d with d \| ∏(n+h_i) on an admissible k-tuple | §4.1: `weight(n) := (∑_{d\|P(n), d≤R} λ(d))²`, `λ(d) = μ(d)G(log d/log R)`; §6: *"we studied the divisors d of the product of the k-tuple values; that is d\|P(n) = (n+a₁)…(n+a_k)"* | **VERIFIED**, verbatim |
| `I:` ratio S₂/S₁ > 1 | §4.1 sets up `∑ weight(n)(∑θ(n+a_i) − log 3x) > 0`, which is that ratio | **VERIFIED** in substance — see the refinement below |
| `T:` two primes in the tuple | §4.1: *"at least two of n+a₁,…,n+a_k are prime"* | **VERIFIED**, verbatim |
| `bound_then:` GPY needs θ > ½; Bombieri–Vinogradov gives exactly ½ | §5: *"if the Elliott-Halberstam conjecture holds with any exponent > ½, then … the k-tuple contains two primes. However the Elliott-Halberstam conjecture remains unproven."* BV is stated with `Q = x^{1/2}/(log x)^B` | **VERIFIED** |

**One refinement to `I`.** The threshold is not literally 1. Granville's Proposition 6.3:
the criterion is `ρ(F) > 4h` unconditionally and `ρ(F) > 2h` under Elliott–Halberstam,
where ρ(F) is the variational ratio. Fable's "S₂/S₁ > 1" is the normalised form; if the
field is meant to be checkable, write the threshold.

**One addition to `bound_then`.** There are *two* exponents, and the P1 field names only
one. θ = ½ is the level of distribution; but the sieve support R obeys D = [d₁,d₂] ≤ R²,
so the binding constraint on the sieve is R < x^{1/4−o(1)}. Granville §4.2: *"Going any
further is difficult, so that the **1/4 is an important barrier**. Goldston, Pintz and
Yıldırım showed that if one can go just beyond 1/4 then one can prove that there are
bounded gaps between primes."* Both are correct and they are the same barrier seen from
two sides; a field that names only θ loses the form in which the constraint actually
binds the sieve. (Compare case 5, where a single-regime `bound` field lost a whole
dimension range.)

**Two slots Fable left empty are now fillable.** Case 7's P1 row has no `M` and no `C`
— consistent with the pattern L2 found (composition empty in 3 of 5, terminal in 3 of 5).
Granville supplies both: the move is Selberg's construction, `λ(d) = μ(d)G(log d/log R)`,
an **explicit formula, not an existence theorem**; the composition is the multiplicativity
of ω(·), which lets the divisor sums factor prime-by-prime (§4.2).

---

## 2. The leak: confirmed in the survey's own words, and the constant derived

Fable's leak: *"Weights are a one-dimensional function of the product. The ratio saturates
at 2θ·(1+o(1)) regardless of k."*

**Granville says the first half outright**, §6.6:

> If F(t₁,…,t_k) = f(t₁+…+t_k) then … ρ(F) = ρ_k(f) … That is, **we have reverted to the
> original GPY argument, which was not quite powerful enough for our needs. We want to
> select F that does not lead us back to the original GPY argument, so we should avoid
> selecting F to be a function of one variable.**

That is the leak *and* the fix, stated by the survey author, on the same page.

**The second half checks out numerically.** `DERIVED HERE` from §4.8. For the GPY choice
F(t) = (1−t)^ℓ/ℓ!, the beta integrals give

    ρ_k(F) = [k/(k+2ℓ+1)] · [2(2ℓ+1)/(ℓ+1)]

| k \ ℓ | 1 | 2 | 5 | 20 | 100 |
|---|---|---|---|---|---|
| 10 | 2.308 | 2.222 | 1.746 | 0.766 | 0.189 |
| 1 000 | 2.991 | 3.317 | 3.627 | 3.751 | 3.314 |
| 10⁶ | 3.000 | 3.333 | 3.667 | 3.905 | 3.979 |
| 10¹² | 3.000 | 3.333 | 3.667 | 3.905 | 3.980 |

Both factors are increasing and bounded: k/(k+2ℓ+1) → 1, and 2(2ℓ+1)/(ℓ+1) → 4. **So
ρ_k(F) saturates at 4 and never reaches it, for any k whatsoever.** Granville's criterion
(4.13) is `(1/2)·θ·ρ_k(F) > 1`, whose value therefore saturates at `(1/2)·θ·4 = 2θ`.
Requiring 2θ > 1 gives **θ > ½** — the barrier, recovered from the leak rather than quoted.

Fable's phrasing is exactly right, and the "regardless of k" is the load-bearing clause:
the cap is a *constant*, not a function of the problem parameter.

**And the after-board lifts precisely that cap.** Granville §6.9/§6.10, for F in k
variables: `log k − 2 log log k − 1 ≤ ρ(F) ≤ k log k/(k−1)`.

| k | Maynard lower bound | Tao upper bound |
|---|---|---|
| 105 | 0.579 | 4.699 |
| 10⁶ | 7.564 | 13.816 |

**GPY: capped at the constant 4. Maynard–Tao: grows like log k.** Fable's held-out 7a
("the ratio grows like log k") is verified, and so is the matching before-fact, which P1
asserted and nobody had checked.

Both after-boards verified: **7a** Maynard's k=105 polynomial in P₁ and P₂ with
ρ(F) = 4.0020697… (§6.7); **7b** Zhang's Theorem 3.2, y-smooth moduli, Q = x^{1/2+η},
η/2 = δ = 1/1168 (§3.2). The rubric's two-accepted-answers requirement is sound.

---

## 3. The finding: case 7 is a within-problem matched pair, and should be split

This is worth more than the citation, and it is not something the row was asked about.

The two after-boards are **not two routes to the same thing**. They are a board change and
a bound improvement, achieved independently, months apart, on the same problem:

- **Zhang (7b) plays better on the GPY board.** He leaves the sieve alone and improves the
  *input*: a Bombieri–Vinogradov estimate past x^{1/2} for smooth moduli. Granville §5
  opens by asking whether the GPY argument survives Zhang's restrictions — Zhang works
  *within* GPY.
- **Maynard–Tao (7a) change the board and keep the old input.** §6.5: *"By the
  Bombieri-Vinogradov Theorem we can take R = x^{1/4−o(1)}"* — the unimproved estimate.
  Granville is explicit about why this was the surprise: *"it was suddenly much easier to
  prove Zhang's Main Theorem and to go far beyond, **because one can avoid having to prove
  any difficult new results about primes in arithmetic progressions**."*

So case 7 is **the cleanest natural experiment in the corpus**: one problem, one period,
two teams, one changing the board and one not, with the counterfactual actually run rather
than argued. Every other positive/control comparison in P1 is cross-problem and therefore
confounded by difficulty; this one is not. It is the structure the repo already says it
prefers — N2's within-problem pairing — and it arrived free.

**Recommendation: split the case.** Keep **7a (Maynard–Tao) as the positive**; promote
**7b (Zhang) to a control**, alongside 14 (sphere packing) and 15 (Kelley–Meka). That
raises the control count from 2 to 3, and the third is the only one where the board change
and the non-board-change are contemporaneous on identical stakes.

**One honesty flag on that recommendation.** Zhang is not simply "better play". He did
change a board — the *equidistribution* board, one level down: factoring the modulus,
restricting to smooth q, Graham–Ringrose amplification. What is unchanged is the GPY
sieve board that the case is encoded at. So 7b is a board change at level n−1 feeding an
unchanged board at level n. That is a **third category** the five-transformation catalogue
never had and the rebuilt diagnostic does not currently express, and it should be recorded
as such rather than flattened into "control". Encode the level explicitly or the control
is wrong.

---

## 4. What it does to the diagnostics

**Product-law matching: NOT APPLICABLE, correctly.** There is no product operation on
admissible k-tuples of linear forms, so the rule declines to speak. Case 7 joins the 11
of 23 outside the domain — consistent, not a failure.

**Union-bound refinement: does not fire, correctly.** Case 7's factor comes from a
variational optimum, not a union bound over m events.

**But case 7 exhibits a third mechanism, and it has a computable trigger.** Fable's P3
finding 5 already put case 7 outside the catalogue ("enlarges the dimension of the move
space — it *de-collectivizes*, the reverse of #4"). Granville shows exactly what that
means, and it is mechanical:

> **Candidate diagnostic — variational-ceiling.** The invariant is an optimum of a ratio
> over a function class. Compute `sup ρ` over the current class. **FIRE iff that supremum
> is bounded by a constant independent of the problem's size parameter, while the class is
> legally enlargeable.**

On case 7: sup ρ = 4 over one-variable F, independent of k → fires; and enlarging to k
variables gives log k, which is what happened. The inputs are the bound and the extremal
function — **no leak table** — so it is of the same kind as the rebuilt product-law rule
and testable the same way.

Three caveats, stated up front so they are not discovered later. n = 1. It is a
*proposal*, not a result. And it must be run against the twins before it means anything —
in particular against N6 (discrepancy of APs, n^{1/4} tight) and N1/N8, where a bounded
optimum is bounded because the answer is, and the rule must decline. What it does have
that auxiliary-witness-lift never did is a stated trigger computable from the before-board.

It is also **not circular in the way product-law matching was**: it comes from a case that
was already outside the taxonomy before anyone looked for a rule, rather than from the
cases it would be scored on.

---

## 5. Register

| item | status |
|---|---|
| C7 `bound_then` | **VERIFIED** |
| C7 `state`, `invariant`, `terminal` | **VERIFIED**; add the ρ > 4h / 2h threshold to `invariant` |
| C7 `move`, `composition` | **now fillable** — Selberg formula (not an existence theorem); multiplicativity of ω |
| C7 leak | **VERIFIED in the source's own words, and the constant 4 derived here** |
| after-board 7a (Maynard) | **VERIFIED**, ρ = 4.0020697… at k = 105, ρ ≥ log k − 2 log log k − 1 |
| after-board 7b (Zhang) | **VERIFIED**, Theorem 3.2, η/2 = δ = 1/1168 |
| case 7 structure | **split recommended** — 7a positive, 7b control, with the level flag |
| controls | 2 → 3 if the split is taken |

D19 drops from seven rows to four: C10, C12, and the two lower-priority twins N16/N20.
Control 15 remains unsourced (my earlier error, see `CITATIONS_RESOLVED.md`).
