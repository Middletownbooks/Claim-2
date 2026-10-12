# Three rows resolved from primary sources

Two Bourbaki transcripts arrived (Pierce, arXiv:1707.00119; Peluse, arXiv:2206.10037),
plus two negative reports from the reader. **These are fetched primary sources and
outrank everything in `CITATIONS_ASSIST.md`.** Where the two collide, the transcript wins.

One of my own predictions was wrong; it is corrected below rather than quietly dropped.

---

## C3 — VERIFIED. The attribution is Shannon's, exactly as P1 has it.

The reader's quote settles it outright, and is stronger than what I asked for:

> Shannon [Sha56] determined Θ(G) for all graphs G with at most six vertices, except
> for the five cycle C5, for which he famously proved α(C5^⊠2) ≥ 5 (and thus
> Θ(C5) ≥ √5) using the independent set {t·(1,2) : t ∈ Z5} and **Θ(C5) ≤ 5/2 via an
> upper bound method that we now refer to as the fractional clique covering number**
> (and which we denote by χ̄_f). Lovász [Lov79] in breakthrough work introduced the
> Lovász theta function (denoted by ϑ), proved that it upper bounds the Shannon
> capacity, and used this to determine Θ(C5) = ϑ(C5) = √5.

So: the before-board is √5 ≤ Θ(C5) ≤ 5/2, the lower bound is Shannon's explicit
5-element independent set in C5^⊠2, and **the upper bound 5/2 is Shannon's own, by the
fractional clique covering number.** P1's `bound_then` field is correct as written.
Record C3 as VERIFIED, source: the fetched survey, quoting Sha56.

Two small corrections while the row is open. The graphs Shannon settled are those on
**at most six vertices**, not five — a search snippet I relayed said five, and it was
wrong. And the value 5/2 still needs no source: C5 is vertex-transitive so χ_f = n/α =
5/2, and self-complementary so the clique-cover convention does not bite.

**This is load-bearing and it holds.** `DIAGNOSTIC.md` calls case 3 the one principled
false negative, on the grounds that the pre-Lovász invariant was *already*
multiplicative and merely not tight. The quote confirms the invariant was χ̄_f, which is
multiplicative under the strong product — that is why it bounds capacity at all. The
false negative stands on a sourced fact.

---

## C4 — the threshold is unsourced. Reword the row; do not keep the number.

The reader reports that **neither Weaver (math/0209078) nor MSS (1306.3969) states the
threshold as δ ≲ 1/log n.** That is the answer, and it is the case I flagged in advance.

Act on it: rewrite case 4's `bound_then` to the claim the sources support — *the
matrix-Chernoff / random-partition route loses a factor logarithmic in the dimension,
and interlacing families remove it* — and drop the 1/log n figure. A field that keeps a
number no source states is exactly the defect C2 and C5 already were.

The diagnostic is unaffected. Case 4 fires because the target's law under direct sum is
`max` while the bound's is `additive`; that reading needs the log-dimension loss, which
is sourced, not the threshold, which is not.

---

## C9 — VERIFIED, and the *leak* is now derivable rather than asserted

Pierce §1 gives the classical chain verbatim:

> Vinogradov's original work [Vin35] was taken up by Linnik [Lin43] (who moved it to a
> p-adic setting) and polished by Karatsuba [Kar73] and Stechkin [Ste75]. In total,
> this approach showed that for s ≥ k,
>   J_{s,k}(X) ≤ D(s,k) X^{2s − ½k(k+1) + η_{s,k}}
> for an explicit constant D(s,k), and **η_{s,k} = ½k²(1 − 1/k)^{[s/k]} ≤ k²e^{−s/k²}**
> for k ≥ 2. As a consequence of the decay of η_{s,k}, one can verify for
> **s ≥ 3k²(log k + O(log log k))** the bound in the Main Conjecture … (Indeed, along
> the same lines of argument, the leading 3 can be improved to a 2 …)

and then, for the 1990s:

> Wooley's thesis [Woo92, Woo96] developed an efficient differencing method … showing
> the Main Conjecture held for **s ≥ k²(log k + 2 log log k + O(1))**.

**P1's `s ≳ c·k² log k (classical)` is correct as a shape.** The constant has a history:
3 (Vinogradov–Linnik–Karatsuba–Stechkin), improvable to 2, then 1 with Wooley 1992. The
L2 blind encoder wrote "(1+o(1))k² log k … sharpened by Karatsuba–Stechkin and Wooley
1992"; since k²(log k + 2 log log k + O(1)) = (1+o(1))k² log k, **the blind encoder's
figure and attribution chain are both correct.** Record the constant's history in the
field so the era is unambiguous.

### The leak, derived

Fable's case-9 leak reads: *"Each iteration recovers a fixed fraction of the defect, so
~log k rounds are needed."* Pierce §4.2 gives the recursion that makes this literal —
`η_{s+k,k} ≤ η_{s,k}(1 − 1/k)` — so each block of k variables multiplies the defect by a
**fixed fraction** (1 − 1/k), starting from η ≈ k²/2. Burning that down to O(1) needs

    (½)k²(1 − 1/k)^m ≤ 1   ⟹   m ≈ k·log(k²/2)   ⟹   s = km ≈ 2k² log k

| k | contractions m needed | s = km | k²(2 ln k − ln 2) | s / (k² ln k) |
|---|---|---|---|---|
| 10 | 38 | 380 | 391.2 | 1.650 |
| 100 | 848 | 84,800 | 85,171.9 | 1.841 |
| 1000 | 13,116 | 13,116,000 | 13,122,363.4 | 1.899 |

s/(k² log k) → 2, matching Pierce's "the leading 3 can be improved to a 2". `DERIVED
HERE` from Pierce eq. (6).

**This matters beyond the citation.** Case 9 is one of only two cases where L2's two
encoders agreed on the leading leak mechanism, and the agreement was explained as "the
leak is visible in the algebra of the bound itself". That explanation is now a
demonstration: the log k *is* the contraction count, and the arithmetic reproduces the
paper's own constant. One of the two agreements is no longer taken on trust.

### A bonus finding the transcript hands over free

Pierce §8.5, "Glimmers of parallel structure", argues that efficient congruencing and ℓ²
decoupling share rescaling (translation-dilation ↔ affine invariance), multilinear
estimates, iteration (p-adic concentration ↔ ball inflation), and transversality
(Wooley's "conditioning" step removing singular solutions ↔ Kakeya transversality). She
quotes Wooley's own speculation that the two "will ultimately be understood as p-adic
and Archimedean perspectives of one unified method."

That is a **same-mechanism-two-substrates** claim about a case the taxonomy classes as a
board change, and it is made by the survey author, not by us. Worth a row of its own:
it is the best-documented instance in the corpus of a change that may be a change of
*substrate* rather than of board, which is a distinction the five-transformation
catalogue never had.

---

## N3 — VERIFIED, but the citation is **Salem–Spencer 1942, not Behrend 1946**

This is the correction with teeth. Peluse §0 states the power-saving exclusion explicitly
and attributes it to the *earlier* construction:

> **Salem and Spencer (1942)** constructed subsets of the first N integers of density
> exp(−log N/log log N) lacking three-term arithmetic progressions, **showing that the
> true order of magnitude of r₃(N) is larger than N^{1−ε} for any fixed ε > 0.** For
> this reason, sets free of three-term arithmetic progressions are sometimes called
> Salem–Spencer sets. A construction of **Behrend (1946)** shows that
> r₃(N) = Ω(N/exp(C√log N)) for some absolute constant C > 0, which is still essentially
> the best known lower bound.

So N3's claim — *the construction excludes power savings* — is **Salem–Spencer's**.
Behrend is the stronger bound and the best one known, but the exclusion does not need it.
Both figures check out: exp(−log N/log log N) > N^{−ε} once log log N > 1/ε, and
Behrend's exp(−C√log N) is stronger still.

Update the twin to cite **Salem–Spencer 1942 for the exclusion and Behrend 1946 for the
best known lower bound**. The twin's status as a negative is unchanged and now rests on
a source that states the consequence in so many words, rather than on my arithmetic.

Two further rows fall out of the same transcript, free:

- **Case 2's bound**: Meshulam O(3^n/n) and Bateman–Katz O(3^n/n^{1+c}) both confirmed,
  as is Edel 2004's Ω(2.217^n) and Ellenberg–Gijswijt's O(2.756^n).
- **Case 2's after-board attribution needs a fix.** Peluse: Croot–Lev–Pach proved a bound
  for **(Z/4Z)^n** (O(3.61^n), improving Sanders' O(4^n/n(log n)^c)); **Ellenberg–Gijswijt
  adapted the method to prove the cap-set bound.** P1 §1.3 credits both jointly for the
  cap-set after-board. CLP supplied the method, EG the theorem — separate the two.

Peluse also corroborates the repo's structural reason for N3 being the discriminator,
and gives a sharper version of it: the density increment costs O(1) codimension per step
in F₃ⁿ (N_{i+1} ≍ N_i) but N_{i+1} ≍ α^{O(1)}√N_i in [N], which is precisely why the
same argument yields 3^n/n there and only N/log log N here. That is a better statement of
"the product operation that makes case 2 fire is absent" than the one currently in
`DIAGNOSTIC.md`.

---

## A prediction of mine that was wrong

`CITATION_SOURCES.md` said the Peluse survey would also cover **Kelley–Meka (control
15)**, "three rows from one document". **It does not.** The survey is Séminaire Bourbaki
June 2022, on Bloom–Sisask 2020; its table of records ends at Schoen 2021 and
Kelley–Meka does not appear anywhere in it. Control 15 is still unsourced and needs its
own document — arXiv:2302.07211 (Bloom–Sisask's write-up of the Kelley–Meka bounds) is
the obvious candidate.

Two rows from that transcript, not three.

---

## Net effect on the debt register

| row | was | now |
|---|---|---|
| C3 | UNVERIFIED | **VERIFIED** — Shannon's own fractional-clique-cover bound |
| C4 | UNVERIFIED | **REWORD** — threshold unsourced; keep the log-dimension loss |
| C9 | UNVERIFIED (D1) | **VERIFIED** — plus the leak derived from Pierce eq. (6) |
| N3 | STANDARD | **VERIFIED, re-attributed** — Salem–Spencer 1942, not Behrend |
| case 2 bound | recalled | **VERIFIED** |
| case 2 after-board | joint credit | **SPLIT** — CLP method, EG theorem |
| control 15 | unsourced | **still unsourced** — my error, see above |

D1 closes. D19 drops from ten rows to seven.
