# The congruence sieve — verified, and it prunes nothing here

The user identified this as *the* method in the Cançado–Coutinho–Spier transcript, and the
identification is right: it is a real technique, it is in the paper, and this project was not
using it. It is also, measured rather than argued, **worth nothing to the search as built** — for
a reason worth writing down.

## 1. What the sieve is

It is in the proof of **Theorem 24**, used there for one prime and one purpose. Generalised:

> **Kleiman** (the paper's [16]): if *E*, *F* solve PTE_n then (*n*−1)! divides
> *p_E*(0) − *p_F*(0), which by Theorem 20 is the constant *C* = *p_E* − *p_F*.
>
> Hence for every prime *p* | *C*, *p_E* ≡ *p_F* (mod *p*). Both split over ℤ, so over 𝔽_p both
> are products of linear factors, and equal polynomials means **equal multisets of residues**:
>
> > **E ≡ F (mod p), as multisets, for every prime p dividing C.**

CCS use only *p* = 2, to derive a contradiction about the multiplicity of 0 in 𝔽₂[*x*]. But
(*n*−1)! hands over several primes at once for free: for *n* = 11, **10! = 2⁸·3⁴·5²·7**, so
*p* = 2, 3, 5 and 7 all divide *C* whatever the solution is.

In the swapping-symmetric case *F* = −*E*, so the residue multiset of *E* must be **invariant
under negation** mod 3, mod 5 and mod 7. (Mod 2 is vacuous there: −1 ≡ 1.)

## 2. Verified

**17 of 17** ideal solutions this project can produce — eight at *n* = 4, six at *n* = 5, two at
*n* = 6, the *n* = 7 classic — satisfy the multiset congruence at **every** prime dividing their
own *C*, and in all 17 every prime factor of (*n*−1)! does divide *C*, so the sieve is available
before you know anything about the solution. The three known symmetric solutions pass the
negation-symmetry form at 3, 5 and 7.

## 3. How hard it bites

400,000 random pattern-signed 11-sets, at two heights:

| | mod 3 alone | mod 5 alone | mod 7 alone | all three | prune |
|---|---:|---:|---:|---:|---:|
| H = 90 | 0.14541 | 0.03485 | 0.01049 | 0.00016 | **6,250×** |
| H = 300 | 0.14459 | 0.03497 | 0.01052 | 0.00005 | **20,000×** |

(The H = 300 figure rests on 20 hits, so ±22%; the product of the three marginals, 5.3 × 10⁻⁵,
agrees with it and disagrees with the H = 90 figure, where the three events are still positively
correlated because 90 is not a multiple of 7.)

A prune of 6,250–20,000× sounds decisive. Under the cost law C(*H*,6) it is **4.3–5.2× in
height** — the same conversion that cost Corollary 21 its apparent 17× (see D44's lesson).

## 4. And it saves no work at all, which is the finding

A filter can only save work that is being done. So: how many candidate 11-sets actually reach the
point where the sieve would be applied?

| H | right-hand tuples enumerated | candidate 11-sets reaching the power-sum join |
|---:|---:|---:|
| 40 | 3,838,380 | **0** |
| 50 | 15,890,700 | **0** |

**Zero.** The meet-in-the-middle's cost is enumerating C(*H*,6) six-tuples at O(1) each, and the
five power-sum conditions are already a perfect filter — nothing false ever survives them to be
sieved. The sieve is a predicate on the *completed* 11-set, and no predicate on the completed
object can reduce the cost of enumerating its parts.

So the 6,250× is a prune on a set that is already empty.

## 5. Where it would pay, and why that is not here

The sieve pays exactly when **candidates are expensive to test** — an architecture that generates
a candidate and then does real work on it (factor a degree-11 polynomial, solve a system, lift a
residue vector). There, a cheap congruence check that kills 99.98% of candidates before the
expensive step is worth a factor of thousands.

This search has the opposite shape: candidates are free to generate and free to test, and
generating them *is* the entire cost. The reduction in §3 of `PREREG_PTE11.md` already spends
5 of the 11 degrees of freedom on the power-sum equations, leaving 6 — and C(*H*,6) is what six
free parameters cost. That is the floor for any method that enumerates rather than solves.

## 6. What this says about the height-3500 frontier — **THIS SECTION IS WRONG, see `CMSV2024.md` §3**

> **[Corrected 21 Sep 2026, same day, on reading the actual paper.]** The conclusion below —
> that the published frontier is compute rather than method — is **false**. Coppersmith et al.
> §4.1 use the divisibility structure as the **generator** of the enumeration, not as a filter
> on it: every newly selected element is forced into a residue class mod *p*₁ = 31 or *p*₂ = 29,
> so it has ≈2*H*/*p* candidates instead of 2*H*. Their enumeration is **52,684×** smaller than
> this project's at *H* = 90 and 1,599× smaller at *H* = 3500, before the checks mod 19, 17, 13,
> the moment table mod 23, and the polynomial *F*₁₁. §5 above names exactly that use case and
> then fails to imagine it had been implemented. The divisor set used here was also the weak
> one — Kleiman alone gives 2, 3, 5, 7, while their Table 1 gives 2⁸·3⁴·5³·7²·11·13·17·19 for
> *C*₁₁ and 31 more for *C′*₁₁.
>
> The text below is kept as written, because it is the record of a wrong inference made
> confidently from a partial source.



At C(*H*,6) and ~170 k/s, height 3500 is ≈ 2.5 × 10¹⁸ tuples. In tight C at 10⁹–10¹⁰ ops per
core-second that is **tens to hundreds of core-years** — a large but entirely ordinary budget for
a *Mathematics of Computation* paper, and about 10⁶ times a container-hour.

Which reframes the gap, and is the honest correction to `VERDICT_PTE11.md` §3: it is most likely
**not** an algorithmic secret we are missing. 10⁶ in compute is exactly 10× in height under H⁶,
and 10× is the distance from where this search lands to 3500. The published frontier is
consistent with the same method and a real machine.

**That does not change the decision, it sharpens the reason.** We are not one clever trick short;
we are six orders of magnitude of compute short, and the two cleverest tricks in the transcript —
Corollary 21 and this sieve — are worth 1.6× and 1.0× in height respectively.
