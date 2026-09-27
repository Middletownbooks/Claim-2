# D-optimal designs as a parallel track to Hadamard — transfer audit

**This is not the fallback prompt.** An earlier version of this document was written as a
go/no-go gate to run *if* the Hadamard programme died. That is not the ask here. The Hadamard
work is live and progressing, and the question is narrower and more interesting:

> **How much of what you have built for Hadamard applies, unchanged or nearly unchanged, to
> D-optimal designs — and what does the difference cost?**

The first deliverable is an **audit**, not a search. Do not build a solver. Read your own
machinery against the statement below and report where it lands.

**This prompt is self-contained on the D-optimal side.** Everything you need about D-optimal
designs is here. A previous handoff on this project pointed at repository paths that turned out
to be private and a bar came back provisional because of it; nothing below requires reading any
repository you do not already have. On the Hadamard side, use your own findings — you have them
and I do not.

---

## 1. The two problems side by side

**All of §1 is recall except where marked VERIFIED. Checking it is step 1.** If any of it is
wrong, stop and report, because everything after it depends on it.

For an *n* × *n* matrix with entries ±1, Hadamard's bound |det| ≤ *n*^(*n*/2) is attained only
when *n* = 1, 2, or *n* ≡ 0 (mod 4). For the other residues the maximum is smaller and the bound
has a different form. For **n ≡ 2 (mod 4)** it is the **Ehlich–Wojtas** bound,
(2*n*−2)(*n*−2)^((*n*−2)/2), and a matrix attaining it is a **D-optimal design**.

Writing *n* = 2*v* with *v* odd, the classical construction uses two **circulant** ±1 matrices
*A*, *B* of order *v* with

> ***A A*ᵀ + *B B*ᵀ = (2*v*−2)·*I* + 2·*J***

Put side by side with the four-circulant condition your Hadamard route is built on:

| | **your route (Hadamard, order 4*v*)** | **D-optimal, order 2*v*** |
|---|---|---|
| objects | **4** circulant ±1 sequences on Z_*v* | **2** circulant ±1 sequences on Z_*v* |
| invariant | periodic autocorrelation | periodic autocorrelation |
| condition | Σ_{i=1..4} PAF_i(*s*) = **0**, *s* = 1…*v*−1 | PAF_A(*s*) + PAF_B(*s*) = **2**, *s* = 1…*v*−1 |
| row sums | Σ_{i=1..4} *a_i*² = **4*v*** | *a*² + *b*² = **4*v* − 2** |
| independent equations | (*v*−1)/2, → *D* = (*r*−1)/2 under the orbit ansatz | identical: PAF(*s*) = PAF(*v*−*s*) |

**The defining equation differs in exactly two places: the number of summands, and a constant on
the right-hand side.** That is the whole of it. Same index group, same invariant, same shape of
quadratic side condition. I know of no other pair of open problems in this project's pool that sit
this close together.

The row-sum condition *a*² + *b*² = 4*v* − 2 is derived, not recalled: apply both sides of the
matrix identity to the all-ones vector and use *A*ᵀ**1** = *a***1** for a circulant.

---

## 2. Where I think the transfer is real

Ordered by how confident I am, and each one is cheap to check against your code.

**2.1 The residual arithmetic is identical. VERIFIED LOCALLY.**

For a ±1 sequence of odd length *v*, PAF(*s*) ≡ *v* (mod 4), and Σ_{s=1}^{v−1} PAF(*s*) = *a*² − *v*.
Both checked by brute force over all ±1 sequences for *v* ≤ 13. Their consequences:

* **Hadamard:** Σ_i PAF_i(*s*) ≡ 4*v* ≡ 0 (mod 4), target 0 → residuals ≡ 0 (mod 4). And
  Σ_s Σ_i PAF_i(*s*) = Σ_i(*a_i*²−*v*) = 4*v* − 4*v* = 0 → **residuals sum to zero.**
* **D-optimal:** PAF_A+PAF_B ≡ 2*v* ≡ 2 (mod 4), target 2 → residuals ≡ 0 (mod 4). And
  Σ_s(PAF_A+PAF_B) = (4*v*−2) − 2*v* = 2*v* − 2, against a target sum of 2(*v*−1) → **residuals
  sum to zero.**

**The same two facts hold on both routes, for different reasons that happen to cancel.** So the
cost landscape has the same arithmetic skeleton: residuals quantised in steps of 4, constrained to
sum to zero on the admissible manifold, hence the same discrete floor structure above zero and the
same lower bound on a non-zero cost. I confirmed by exhaustion at *v* = 7 and *v* = 9 that the
smallest non-zero cost is the one that arithmetic predicts. (My script sums over *s* = 1…*v*−1 and
so reports 64; on the deduplicated set *s* = 1…(*v*−1)/2, the units your findings use, that is 32.)

**Consequence: whatever descent you are running should apply unchanged.** Σres² over the
deduplicated equations, moves that are row-sum-preserving swaps so the walk stays on the
admissible manifold, the same delta-evaluation under a single swap. The only edit is the constant
in the residual: `res_s = PAF_A(s) + PAF_B(s) − 2` instead of `Σ_i PAF_i(s)`. **One line.**

**2.2 The multiplier-orbit reduction is available in principle.**

The reduction is a property of the index group and the autocorrelation, not of the number of
blocks: if every sequence is constant on the orbits of a multiplier subgroup ⟨*t*⟩ of order *d*
acting on Z_*v*, then PAF is constant on orbits of *s* and the *v*−1 equations deduplicate the
same way. With *d* odd, −1 ∉ ⟨*t*⟩, so *D* = (*r*−1)/2 with *r* = (*v*−1)/*d* + 1 — the same
formula. The per-block row-sum law is also per-block and so unchanged in form:
*a* = ±1 + *d*(2*u* − (*r*−1)).

**But see §3.2 — this is the piece I think is most likely to fail, and it is the cheapest to
settle.**

**2.3 The protocol apparatus transfers whole, and this is the part with no risk in it.**

Seven seeds / matched caps / matched seeds / medians. The form of the density estimator. The
growth-law fit log₂(seconds) = *a*·(−log₂ density) + *b*. The positive-control discipline. The
habit of costing a speedup in frontier units before letting it change a decision. None of that is
Hadamard-specific; all of it is this project's, and it is the expensive part to have built.

---

## 3. Where I think the transfer breaks, and what it costs

Each of these is a cheap check, and I would run them in this order before anything else.

**3.1 Two squares is far more restrictive than four. VERIFIED LOCALLY.**

Σ_{i=1..4} *a_i*² = 4*v* is nearly always solvable. *a*² + *b*² = 4*v* − 2 = 2(2*v*−1) is solvable
only when every prime ≡ 3 (mod 4) divides 2*v*−1 to an even power. This bites hard, and it is a
*necessary condition for the two-circulant design to exist at all*, before any search:

* Of the six orders on your Hadamard worklist, **4*v*−2 is a sum of two squares for only one**
  (*v* = 643). For 487, 523, 571, 659, 739 it is not.
* At *n* = 22 (*v* = 11) there is **no two-circulant D-optimal design**, confirmed by exhaustion
  over all 2²² pairs: 4·11−2 = 42 = 2·3·7 is not a sum of two squares, so no admissible row sums
  exist. The same exhaustion finds 392 designs at *n* = 14 and 1944 at *n* = 18.

**So the two problems do not share orders**, and you should not expect to reuse an instance. The
D-optimal parameter set is thinner and is filtered by a classical arithmetic condition your
Hadamard route does not have.

**3.2 Free bits halve; the equation count does not. This is the one I would check first.**

Under the orbit ansatz the free bits are *k*·(*r*−1) for *k* blocks, while the number of equations
is *D* = (*r*−1)/2 **independent of *k***. So going from four blocks to two halves the search
space's entropy and leaves the constraint count untouched:

> log₂ E[#solutions] ≈ (*r*−1)·(*k* − *b*/2),  where *b* = bits per equation.

Measured by Monte Carlo on orbit-constant random sequences at *d* = 3 (mine, crude, single
representative *s*, 60k trials):

| *v* | *b* (4 blocks) | *k*−*b*/2 | *b* (2 blocks) | *k*−*b*/2 |
|---:|---:|---:|---:|---:|
| 67 | 3.50 | **+2.25** | 2.86 | **+0.57** |
| 79 | 3.56 | +2.22 | 3.00 | +0.50 |
| 103 | 3.76 | +2.12 | 3.19 | +0.40 |
| 151 | 4.02 | +1.99 | 3.47 | **+0.26** |

*b* grows slowly with *v* on both routes. With *k* = 4 the coefficient stays comfortably positive
and E[#sol] grows with *r*−1. **With *k* = 2 it is small and falling, and it crosses zero at
*b* = 4 bits/equation** — which the 2-block column reaches somewhere in the low hundreds of *v*.
Past that point the orbit ansatz is *expected to be empty*, and larger *r* makes it worse rather
than better.

**If that is right, the orbit reduction — the piece that makes your Hadamard instances tractable
at all — is the piece that does not transfer**, and D-optimal has to be searched closer to full
space, which is in fact how the published D-optimal searches work. Then the transfer is *engine
yes, dimension-reduction no*.

A consistency check on the model, which you can do properly and I cannot: the same formula at
*v* = 523, *d* = 9 (*r*−1 = 58, *D* = 29) needs *b* = 4.87 to reproduce your own estimator's
log₂ E[#sol] = 90.9. My measured *b* is 4.02 at *v* = 151 and rising. **That is an independent
arrival at your estimator's number from a different computation** — worth a minute of your time
either to confirm or to tell me my model is too crude to carry the weight I just put on it.

**3.3 The endgame neighbourhood shrinks by a factor of *M*².**

A depth-4 meet-in-the-middle over four blocks joins *M*² against *M*², a neighbourhood of order
*M*⁴. With two blocks the natural analogue joins *M* against *M* — order *M*², four to five orders
of magnitude smaller at the sizes you work at. To hold the neighbourhood size constant you need
**two swaps per block instead of one**, which is a different move set and a different delta
algebra, not a parameter change. Budget for that, or accept a much weaker endgame.

**3.4 The orbit parametrisation assumes *v* prime.** Your worklist is all primes, so this has
never had to be faced. The orbit count *r* = (*v*−1)/*d* + 1 relies on ⟨*t*⟩ acting freely on
Z_*v* \ {0}. If the interesting D-optimal orders have composite *v*, the orbit structure changes
and so does *D*.

**3.5 Two circulants is not the only route to D-optimal designs.** If the open orders in the
maintained table are ones where the two-circulant construction is known not to apply, the whole
analogy is moot regardless of everything above. **Check this before the rest** — it is one lookup
and it can end the audit.

---

## 4. What does not transfer at all

* The target ranking and the density ladder — instance-specific, re-derive or drop.
* Any absolute cost figure or kill-test threshold from the Hadamard programme.
* The spectral/PSD filtering result. Not because the lesson is wrong but because the underlying
  structure differs: the Gram matrix here is (2*v*−2)*I* + 2*J*, not a multiple of *I*, so the
  eigenvalue picture is genuinely different and should not be assumed either way.
* Anything about reverse-engineering a published construction. No analogue on this side.

---

## 5. Why parallel, and not sequential — the argument that does not depend on §2 or §3

This is the part I would most like you to weigh, because it is a benefit to the **Hadamard** track
rather than to this one.

**Your route has never produced a solution, so a null on it is uninterpretable.** That is why the
plan proposes *v* = 487 as a positive control: it is the one order known settled, and it sits at
density 2⁻¹³². A positive control that expensive is barely a control.

**D-optimal designs have a dense public table of known solutions at small orders** — my exhaustion
above found 392 of them at *n* = 14 and 1944 at *n* = 18, and the maintained maximal-determinant
tables carry many more. So the same engine gets a **graded ladder of instances whose answers are
already known**, at costs from milliseconds upward. Two things follow:

1. **Any engine change can be validated where the answer is known before it is trusted where it
   is not.** At present an engine change on the Hadamard route is scored by whether the cost curve
   moves, which is a proxy; on D-optimal it can be scored by whether it finds the object.
2. **A second, independent fit of the growth law answers a question about Hadamard that Hadamard
   cannot answer about itself:** is the growth exponent a property of *the method* or of *the
   instance family*? If the D-optimal re-fit lands near your Hadamard exponent, the exponent is
   the method's, and any kill test asking the method for a much smaller exponent is asking for
   something it does not have. If it lands well below, the exponent is instance-specific and the
   Hadamard extrapolation deserves more optimism than it currently gets.

**That second point is worth more than the target is.** It is a diagnostic for the primary
programme, obtained on cheaper instances, and it is available whether or not D-optimal ever turns
into a result of its own.

---

## 6. What I am asking for

An audit document, cheapest checks first, stopping early if one of them ends it. Single-threshold
verdicts, no middle bands — a previous gate on this project registered a two-sided test with an
unregistered gap, the answer landed in the gap, and it declined to score.

1. **§3.5 first.** Does the maintained table's set of open *n* ≡ 2 (mod 4) orders intersect the
   orders where a two-circulant construction is the live route? One lookup. If no → say so and
   stop; everything else is moot.
2. **§1 verified or corrected.** Especially *a*² + *b*² = 4*v* − 2 and the Ehlich–Wojtas form.
3. **§3.2 settled**, since it decides whether this is a port or a rebuild. Your estimator is
   better than my Monte Carlo; run it for *k* = 2 and say where the coefficient crosses zero.
4. **A line-by-line verdict on your own modules**: for each, *transfers as-is* / *transfers with a
   named edit* / *does not transfer*. That is the deliverable I actually want, and only you can
   write it.
5. **§5 costed.** What would it take to stand up the smallest D-optimal instance with a known
   answer as a positive control for the engine you already have? If that is an afternoon, it is
   worth an afternoon regardless of how the rest of the audit comes out.

**Tell me where I am wrong.** §3.2 in particular is a crude model doing load-bearing work, and I
would rather have it corrected than agreed with. The six items in §7 exist because each one cost
this project something real.

---

## 7. Rules that are not negotiable, because each cost something

1. **Verify objects, never function returns.** Reconstruct the matrix and check
   *A A*ᵀ + *B B*ᵀ = (2*v*−2)*I* + 2*J* directly. A search reporting success once cost a day.
2. **Positive controls before nulls.** Code must find a *known* design at a solved order before
   any null is reported. A search that cannot find a known object proves nothing when it finds none.
3. **Negative-test every check.** Break each verifier deliberately and confirm it fails. Two
   checks written in one day on this project could not fail at all.
4. **Register predictions before running.** Single threshold, no middle band. A bar you cannot
   evaluate counts as FAIL, not "unscored".
5. **Seven seeds, matched caps, medians** for any timing claim. Single-seed timings here were
   bimodal, and every timing taken before that was discovered was unsafe.
6. **Convert a speedup into frontier units before it changes a decision.** A 17× improvement to a
   search whose cost is the sixth power of the frontier parameter buys 1.6× in frontier. That
   mistake was made here and nearly redirected a programme.
