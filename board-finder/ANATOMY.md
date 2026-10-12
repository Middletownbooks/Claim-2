# The anatomy of one transformation, and the mechanism verified independently

*From the line-by-line audit of Banaszczyk against Guo–Fang–Lu ("Odin"), with both
halves of its central claim re-checked here from the composition laws alone.
Instrument: `verify_mechanism.py`.*

## 1. What actually changed

| slot | Banaszczyk | Guo–Fang–Lu |
|---|---|---|
| state | convex body K | convex body K **+ a density ρ on it** |
| move | K ↦ K∗v | K ↦ T_vK — **the same transform**, open-set convention |
| terminal | γ(K) ≥ ½ ⟹ 0 ∈ K | symmetric + convex + nonempty ⟹ 0 ∈ K |
| invariant | γ_n(K) ≥ ½ | ∃ρ with V_u(ρ) ≤ κ‖u‖ for all u |

**The move did not change. The geometry did not change. The terminal check got
*easier*.** Only the invariant changed, and only in one respect.

## 2. The one respect, and it is checkable in an afternoon

* Gaussian measure is **multiplicative** over products: γ(cube^d) = γ(cube)^d. A
  multiplicative certificate decays geometrically in dimension, so holding the line
  needs half-side **C ≍ √(2 ln d)**. *That is literally where the √log comes from.*
* Directional total variation of a product density is an **average**, not a product:
  V_u(Πρᵢ) = (π/C)·E|Σuᵢ Tᵢ| ≤ **√(2π)/C·‖u‖**.

So the transformation was: **swap a multiplicative invariant for an averaging one,
leaving everything else fixed.**

**Verified here, independently of either paper** — `verify_mechanism.py` needs only the
two composition laws:

| d | half-side C for γ₁(C)^d ≥ ½ | √(2 ln d) | ratio |
|---|---|---|---|
| 2 | 1.0520 | 1.1774 | 0.893 |
| 256 | 3.2643 | 3.3302 | 0.980 |
| 10¹⁰ | 6.5221 | 6.7861 | 0.961 |
| 10¹⁴ | 7.7856 | 8.0295 | 0.970 |

C **diverges** — 1.05 at d = 2 against 7.79 at d = 10¹⁴ — and tracks √(2 ln d) to
within 4% once the lower-order term washes out. Past d ≈ 10¹⁶ the table saturates from
double-precision `erf`, which the audit flagged itself; the √(2 ln d) column is the
honest statement and the numbers illustrate it.

The averaging side: `E|Σuᵢ Tᵢ|` for a uniform unit u runs **0.638 → 0.754** over
d = 1…20, monotone, never above √(2/π) = 0.7979, and the d = 1 value sits at
2/π = 0.6366 — E|t₃/√3|, not E|N(0,1)|. The algebra closes exactly:
(π/C)·√(2/π) = √(2π)/C.

**One correction to how this gets stated.** My first version of the check asserted the
average is *flat* in d. It is not — it rises toward the Gaussian value as the CLT takes
over from the heavy t₃ tails. What the mechanism needs is weaker and is what holds:
the quantity is **bounded above uniformly in d**. The multiplicative certificate's
threshold diverges; the averaging certificate's bound does not move. "Flat" was my
word and it was too strong. (My other predicate was wrong too: I had the ratio
approaching 1 from above and decreasing, where it approaches from below and rises.
Both were errors in my tests, not in the audit's claims.)

## 3. Why this makes a diagnostic rather than a description

Because the property is a **computation on a product**: given a candidate invariant I
and a hard-instance product ⊗Sᵢ, compute I(⊗Sᵢ) and compare it to {I(Sᵢ)}. If it is a
product, the certificate will pay a √log; if it is an average, it will not. No paper is
needed, and no label has to be agreed on — which matters, because the label for this
very transformation drew **three different answers from three independent readers**
(originating audit: DE-TENSORIZE; rater A: WORK MOVED; rater B: AUXILIARY-WITNESS
LIFT), and the five-label vocabulary scored **κ = 0.048**.

The vocabulary failed. The computation behind one of its entries is fine, and has never
been tested as a computation. That distinction is what `CATALOGUE.md` is built on.
