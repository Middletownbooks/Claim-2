# Response to the seven-citation request

**This is the handover document.** It supersedes, for use, the four files it was built
from: `CITATIONS_ASSIST.md` (search-tier reply), `CITATION_SOURCES.md` (the arXiv URL
list), `CITATIONS_RESOLVED.md` and `C7_RESOLVED.md` (the transcript analyses). Those stay
in the repo as the record of how each row moved; nothing below needs them.

Three primary sources arrived as pasted transcripts, plus two negative reports from the
reader. **A pasted transcript is a fetched primary source by this project's own standard.**
Where a transcript and a search snippet disagree, the transcript wins and the snippet row
is corrected, not reconciled.

## The tier rule, which governs every verdict below

| tier | meaning | how to record it |
|---|---|---|
| **PRIMARY** | a fetched source states it; quoted here | `VERIFIED` |
| **DERIVED** | arithmetic, reproducible here, needs no source | `COMPUTED` |
| **SEARCH** | search snippets only — the same tier as the existing 23 rows, no better | `VERIFIED` only if your standard already admits that tier |
| **OPEN** | nothing reached it | leave `UNVERIFIED` |

Direct HTTP is egress-blocked at the gateway in both containers — not only arxiv,
export.arxiv, crossref and doi, but archive.org, mathworld, ar5iv, semanticscholar,
zbmath, dblp, numdam, annals.math.princeton.edu and en.wikipedia.org. Search is the only
live channel. That is why the transcripts mattered.

---

## 1. Disposition of every row

| row | was | now | tier | action required in the repo |
|---|---|---|---|---|
| **C3** Shannon | UNVERIFIED | **VERIFIED** | PRIMARY | none — the field is correct as written |
| **C4** Weaver KS₂ | UNVERIFIED | **REWORD** | negative result | drop `δ ≲ 1/log n`; write the log-dimension loss |
| **C7** GPY | UNVERIFIED | **VERIFIED** | PRIMARY | add the ρ threshold and the x^{1/4} form; fill `move`, `composition`; **split the case** |
| **C9** Vinogradov | UNVERIFIED (D1) | **VERIFIED** | PRIMARY + DERIVED | record the constant's history; **D1 closes** |
| **N3** Behrend | STANDARD | **VERIFIED, re-attributed** | PRIMARY | cite **Salem–Spencer 1942** for the exclusion, Behrend for the best bound |
| **C10** parallel repetition | UNVERIFIED | **SEARCH** | SEARCH | leave; a transcript is unlikely to improve it |
| **C12** Perelman | UNVERIFIED | **PARTIAL** | SEARCH | leave, or close with math/0211159 |
| **N16** border rank | STANDARD | **SEARCH** | SEARCH | lower priority; note sub- vs full multiplicativity |
| **N20** Kővári–Sós–Turán | STANDARD | **SEARCH** | SEARCH | lower priority; carry the range restriction |
| **case 2** bound | recalled | **VERIFIED** | PRIMARY | none |
| **case 2** after-board | joint credit | **SPLIT** | PRIMARY | CLP = method on (Z/4Z)ⁿ; EG = the cap-set theorem |
| **control 15** Kelley–Meka | unsourced | **still unsourced** | OPEN | my error — see §5 |

**D1 closes. D19 drops from ten rows to four** (C10, C12, N16, N20), plus control 15.

---

## 2. Row by row

### C3 — Shannon. VERIFIED, and the attribution is his.

> Shannon [Sha56] determined Θ(G) for all graphs G with **at most six vertices**, except
> for the five cycle C5, for which he famously proved α(C5^⊠2) ≥ 5 (and thus Θ(C5) ≥ √5)
> using the independent set {t·(1,2) : t ∈ Z5} and **Θ(C5) ≤ 5/2 via an upper bound method
> that we now refer to as the fractional clique covering number** (χ̄_f). Lovász [Lov79] …
> proved that it upper bounds the Shannon capacity, and used this to determine
> Θ(C5) = ϑ(C5) = √5.

The before-board √5 ≤ Θ(C5) ≤ 5/2 is right; the lower bound is Shannon's explicit
5-element independent set; **the 5/2 upper bound is Shannon's own**. P1's field needs no
change. (A search snippet I relayed earlier said *five* vertices; the transcript says six.
Use six.)

**Load-bearing and it holds.** `DIAGNOSTIC.md` calls case 3 the one principled false
negative because the pre-Lovász invariant was already multiplicative and merely not tight.
χ̄_f is multiplicative under the strong product — that is why it bounds capacity at all.
The false negative now stands on a sourced fact.

### C4 — Weaver KS₂. The threshold is unsourced. Reword.

Neither Weaver (math/0209078) nor Marcus–Spielman–Srivastava (1306.3969) states the
threshold as **δ ≲ 1/log n**. This was the case flagged in advance, and the flagged
remedy applies: rewrite `bound_then` to what the sources support — *the matrix-Chernoff /
random-partition route loses a factor logarithmic in the dimension, and interlacing
families remove it* — and **drop the number**. A field keeping a figure no source states
is exactly the defect C2 and C5 already were.

The diagnostic is unaffected: case 4 fires because the target's law under direct sum is
`max` while the bound's is `additive`. That reading needs the loss, which is sourced, not
the threshold, which is not.

### C7 — GPY. VERIFIED on every field, and the case should be restructured.

Source: Granville, *Primes in intervals of bounded length*, arXiv:1410.8400v1.

| field | Granville | verdict |
|---|---|---|
| `S:` sieve weights λ_d with d \| ∏(n+h_i) | §4.1: `weight(n) = (∑_{d\|P(n), d≤R} λ(d))²`, `λ(d) = μ(d)G(log d/log R)` | VERIFIED, verbatim |
| `I:` ratio S₂/S₁ > 1 | §4.1's `∑ weight(n)(∑θ(n+a_i) − log 3x) > 0` | VERIFIED in substance |
| `T:` two primes in the tuple | §4.1, verbatim | VERIFIED |
| `bound_then:` θ > ½ needed; BV gives exactly ½ | §5; BV stated with Q = x^{1/2}/(log x)^B | VERIFIED |

**Two additions the row needs.** The invariant's threshold is not literally 1 — Proposition
6.3 gives **ρ(F) > 4h** unconditionally, **> 2h** under Elliott–Halberstam. And
`bound_then` names only θ; because D = [d₁,d₂] ≤ R², the constraint binds the sieve as
**R < x^{1/4−o(1)}**, which §4.2 calls *"an important barrier"*. Both are the same barrier
from two sides, and a field naming only one loses the form in which it bites. (Compare
case 5, where a single-regime field lost a dimension range.)

**Two empty slots are now fillable.** `move`: Selberg's construction
`λ(d) = μ(d)G(log d/log R)` — an **explicit formula, not an existence theorem**.
`composition`: multiplicativity of ω(·), which lets the divisor sums factor prime-by-prime
(§4.2). Case 7 had 2 of 5 slots empty, consistent with L2's finding across P1.

**Both after-boards verified.** 7a: Maynard's k = 105 polynomial in P₁ and P₂,
ρ(F) = 4.0020697… (§6.7). 7b: Zhang's Theorem 3.2, y-smooth moduli, Q = x^{1/2+η},
η/2 = δ = 1/1168. The two-accepted-answers rubric is sound.

### C9 — Vinogradov. VERIFIED, both halves, and the leak is now derived.

Source: Pierce, Séminaire Bourbaki, arXiv:1707.00119. §1:

> … polished by Karatsuba [Kar73] and Stechkin [Ste75]. In total, this approach showed
> that for s ≥ k, J_{s,k}(X) ≤ D(s,k) X^{2s − ½k(k+1) + η_{s,k}} … and
> **η_{s,k} = ½k²(1 − 1/k)^{[s/k]} ≤ k²e^{−s/k²}** … one can verify for
> **s ≥ 3k²(log k + O(log log k))** the bound in the Main Conjecture … (the leading 3 can
> be improved to a 2) …

and for the 1990s: Wooley's thesis gives **s ≥ k²(log k + 2 log log k + O(1))**.

P1's `s ≳ c·k² log k (classical)` is correct as a shape. **Record the constant's history:
3 → 2 → 1** (Vinogradov–Linnik–Karatsuba–Stechkin; the same argument sharpened; Wooley
1992). The L2 blind encoder's "(1+o(1))k² log k, sharpened by Karatsuba–Stechkin and
Wooley 1992" is correct, since k²(log k + 2 log log k + O(1)) = (1+o(1))k² log k.

The posting date is independently confirmed: **arXiv:1101.0574, 3 January 2011**, Annals
175(3) 1575–1627 — which is what voided case 9 in L2. That void stands on a source.

### N3 — Behrend. VERIFIED, but **the citation is Salem–Spencer, not Behrend**.

Source: Peluse, Séminaire Bourbaki, arXiv:2206.10037. §0:

> **Salem and Spencer (1942)** constructed subsets of the first N integers of density
> exp(−log N/log log N) lacking three-term arithmetic progressions, **showing that the true
> order of magnitude of r₃(N) is larger than N^{1−ε} for any fixed ε > 0.** … A
> construction of **Behrend (1946)** shows that r₃(N) = Ω(N/exp(C√log N)) …, which is still
> essentially the best known lower bound.

The exclusion of power savings — the thing N3 asserts — is **Salem–Spencer's**. Behrend is
the stronger bound and the best known, but the exclusion does not need it. Update the twin
to cite both, in those roles. The twin's status as a negative is unchanged and now rests
on a source that states the consequence outright.

### C10, C12, N16, N20 — search tier, left there

**C10** (parallel repetition): search gives Fortnow first showing multiplicativity false,
Feige a simpler example later (Feige–Verbitsky 2002), Raz 1995's sub-exponential decay and
Holenstein's simplification — including the Fortnow-then-Feige ordering the row asserts.
The primary sources are largely pre-arXiv, so a transcript is unlikely to improve this.
Note that case 10's `target_law = "none"` rests on these counterexamples.

**C12** (Perelman): bibliographic record confirmed (math/0211159, 11 Nov 2002); the
cigar-soliton obstruction and the entropy-plus-reduced-distance remedy corroborated from a
secondary source. Case 12 fits none of the five transformations, so it does the least work
of any row here. `math/0211159` closes it if wanted.

**N16**: border rank is submultiplicative under Kronecker product, possibly strictly; and
ω = liminf log_n(R̲(M_⟨n⟩)). N16's role as a negative depends on the law being **sub**-
rather than fully multiplicative — arXiv:1801.04852 exists precisely because that
distinction is live, and the twin's statement should make it explicit.

**N20**: Kollár–Rónyai–Szabó norm graphs give tightness for t ≥ s!, improved by
Alon–Rónyai–Szabó to t ≥ (s−1)!+1; KST is tight up to constants in that range. **The twin
is only valid in the range where tightness is proved** — whether KST is tight for t ≥ 4 is
reported still open — so N20's statement must carry the range.

---

## 3. Derivations — reusable, no source needed

**(a) N3's power-saving step.** Search gives Behrend as
`r₃(N) ≥ N·2^{−(2√2+o(1))√(log₂N)}`. In natural logs the coefficient is
c = 2√2·√(ln 2) = **2.3548**. A bound `r₃(N) ≤ N^{1−δ}` needs `c√(ln N) < δ·ln N`, i.e.
`ln N > (c/δ)²`. Beyond that, Behrend's set exceeds N^{1−δ}. So **every fixed δ > 0 is
excluded** — but record the crossover, because it is large:

| δ | 0.5 | 0.2 | 0.1 | 0.05 |
|---|---|---|---|---|
| crossover | N > 10¹⁰ | N > 10⁶⁰ | **N > 10²⁴¹** | N > 10⁹⁶³ |

N3's status is an **asymptotic** statement and the item should say so.

**(b) C3's value 5/2.** C5 is vertex-transitive, so χ_f = n/α = 5/2; it is self-
complementary, so the clique-cover convention does not bite. `COMPUTED`.

**(c) C9's leak, derived.** Pierce §4.2 gives `η_{s+k,k} ≤ η_{s,k}(1 − 1/k)`: each block
of k variables multiplies the defect by a **fixed fraction**, from a start of ≈ k²/2.
Burning it to O(1) needs `(½)k²(1 − 1/k)^m ≤ 1`, i.e. `m ≈ k·log(k²/2)`, i.e.
**s = km ≈ 2k² log k**.

| k | contractions m | s = km | s/(k² ln k) |
|---|---|---|---|
| 10 | 38 | 380 | 1.650 |
| 100 | 848 | 84,800 | 1.841 |
| 1000 | 13,116 | 13,116,000 | 1.899 |

→ 2, matching Pierce's "the leading 3 can be improved to a 2". **The log k *is* the
contraction count.** Case 9 was one of only two cases where L2's encoders agreed on the
leading mechanism, explained as "the leak is visible in the algebra of the bound itself."
That is now a demonstration rather than a claim.

**(d) C7's leak, derived.** Granville §6.6 states the qualitative half outright:

> If F(t₁,…,t_k) = f(t₁+…+t_k) then … **we have reverted to the original GPY argument,
> which was not quite powerful enough for our needs. We want to select F that does not lead
> us back to the original GPY argument, so we should avoid selecting F to be a function of
> one variable.**

The quantitative half follows from §4.8's beta integrals. For F(t) = (1−t)^ℓ/ℓ!,

    ρ_k(F) = [k/(k+2ℓ+1)] · [2(2ℓ+1)/(ℓ+1)]

Both factors increase and are bounded: → 1 and → 4. **So ρ_k saturates at 4 and never
reaches it, for any k.** Granville's criterion is `(½)·θ·ρ_k(F) > 1`, whose value therefore
caps at **2θ**; requiring 2θ > 1 gives **θ > ½** — the barrier, recovered from the leak
rather than quoted beside it.

| k \ ℓ | 1 | 5 | 20 | 100 |
|---|---|---|---|---|
| 10 | 2.308 | 1.746 | 0.766 | 0.189 |
| 10⁶ | 3.000 | 3.667 | 3.905 | 3.979 |

Fable's "regardless of k" is the load-bearing clause: the cap is a **constant**, not a
function of the parameter. Maynard–Tao lifts it — §6.9/§6.10 give
`log k − 2 log log k − 1 ≤ ρ(F) ≤ k log k/(k−1)`, so 0.58 at k=105 and 7.56 at k=10⁶.
**GPY: capped at 4. Maynard–Tao: grows like log k.** That is the board change in one number,
and it verifies held-out answer 7a.

---

## 4. Findings the request did not ask for

### 4.1 Case 7 is a within-problem matched pair. Split it.

The two after-boards are not two routes to one thing:

- **Zhang (7b) plays better on the GPY board.** He leaves the sieve alone and improves the
  *input*. Granville §5 asks whether GPY survives Zhang's restrictions — Zhang works
  *within* GPY.
- **Maynard–Tao (7a) change the board and keep the old input.** §6.5: *"By the
  Bombieri-Vinogradov Theorem we can take R = x^{1/4−o(1)}"* — unimproved. Granville on why
  this was the surprise: *"one can avoid having to prove any difficult new results about
  primes in arithmetic progressions."*

One problem, one period, two teams, one changing the board and one not, **with the
counterfactual actually run**. Every other positive/control comparison in P1 is
cross-problem and confounded by difficulty. This is the structure the repo already prefers
(N2's within-problem pairing), and it arrived free.

**Recommendation:** keep **7a as the positive**, promote **7b to a control** alongside 14
and 15. Controls go 2 → 3, and the third is the only one where board-change and
no-board-change are contemporaneous on identical stakes.

**Honesty flag on that.** Zhang is not simply better play: he changed the *equidistribution*
board one level down — smooth moduli, factored modulus, Graham–Ringrose. So 7b is a
level-(n−1) board change feeding an unchanged level-n board. That is a **third category**
the five-transformation catalogue never had and the rebuilt diagnostic does not express.
Encode the level explicitly or the control is mislabelled.

### 4.2 A third diagnostic, with a computable trigger

Fable's P3 finding 5 already put case 7 outside the catalogue ("enlarges the dimension of
the move space — it *de-collectivizes*"). Granville shows what that means, mechanically:

> **Variational-ceiling.** The invariant is an optimum of a ratio over a function class.
> Compute `sup ρ` over the current class. **FIRE iff that supremum is bounded by a constant
> independent of the problem's size parameter, while the class is legally enlargeable.**

On case 7: sup ρ = 4 over one-variable F, independent of k → fires; enlarging to k
variables gives log k, which is what happened. Inputs are the bound and the extremal
function — **no leak table** — so it is the same kind of object as the rebuilt product-law
rule and testable the same way.

Caveats stated up front: **n = 1**; it is a proposal, not a result; and it must be run
against the twins first — especially **N6** (discrepancy of APs, n^{1/4} tight) and N1/N8,
where a bounded optimum is bounded because the answer is, and the rule must decline. What
it has that auxiliary-witness-lift never did is a trigger computable from the before-board.
It is also **not circular the way product-law matching was**: it comes from a case that was
outside the taxonomy before anyone went looking for a rule.

### 4.3 Case 2's after-board credit should be split

Peluse: **Croot–Lev–Pach** proved a bound for **(Z/4Z)ⁿ** (O(3.61ⁿ), improving Sanders'
O(4ⁿ/n(log n)^c)); **Ellenberg–Gijswijt adapted the method** to prove the cap-set bound.
P1 §1.3 credits both jointly. CLP supplied the method, EG the theorem.

Also confirmed from the same transcript: Meshulam O(3ⁿ/n), Bateman–Katz O(3ⁿ/n^{1+c}),
Edel Ω(2.217ⁿ), Ellenberg–Gijswijt O(2.756ⁿ).

Peluse additionally gives a **better reason than the one in `DIAGNOSTIC.md`** for N3 being
the discriminator: the density increment costs O(1) codimension per step in F₃ⁿ
(N_{i+1} ≍ N_i) but N_{i+1} ≍ α^{O(1)}√N_i in [N] — which is precisely why the same argument
yields 3ⁿ/n there and only N/log log N here.

### 4.4 A twin-decay signal on N3

Behrend has had its **first quasipolynomial improvement since 1946** (arXiv:2406.12290,
June 2024 — the first beyond lower-order factors). It does **not** change N3's status: a
quasipolynomial improvement to a sub-power-saving bound is still sub-power-saving. But it
is the class of event that moved Erdős distinct distances in R³ into `REJECTED.json`. Give
N3 a re-check date noting it, and check whether the other "standard" twins have moved.

### 4.5 Pierce's substrate parallel — a category the catalogue lacks

Pierce §8.5, "Glimmers of parallel structure", argues that efficient congruencing and ℓ²
decoupling share rescaling (translation-dilation ↔ affine invariance), multilinear
estimates, iteration (p-adic concentration ↔ ball inflation), and transversality (Wooley's
conditioning step ↔ Kakeya transversality) — and quotes Wooley's own speculation that they
"will ultimately be understood as **p-adic and Archimedean perspectives of one unified
method**."

That is a **same-mechanism-two-substrates** claim about a case the taxonomy calls a board
change, made by the survey author rather than by us. Together with §4.1's level-(n−1)
finding, it is the second independent sign that the catalogue is missing an axis: *what
level, and in what substrate, did the change occur?*

---

## 5. Errors of mine, recorded

1. **I predicted the Peluse survey would also cover Kelley–Meka (control 15)** — "three
   rows from one document". **It does not.** The survey is Bourbaki June 2022 on
   Bloom–Sisask 2020; its table of records ends at Schoen 2021 and Kelley–Meka appears
   nowhere. Two rows from that transcript, not three. **Control 15 remains unsourced**;
   arXiv:2302.07211 is the candidate.
2. **I relayed a search snippet saying Shannon settled all graphs on five or fewer
   vertices.** The transcript says **six**. Use six.

---

## 6. Action checklist

Citation work produces edits, not just acknowledgements. In rough priority:

- [ ] **C4**: delete `δ ≲ 1/log n` from case 4's `bound_then`; write the log-dimension loss.
- [ ] **N3**: re-attribute the power-saving exclusion to **Salem–Spencer 1942**; keep
      Behrend 1946 as the best known lower bound; state the claim asymptotically; add a
      re-check date noting arXiv:2406.12290.
- [ ] **C9**: record the constant's history (3 → 2 → 1) in `bound_then`. **Close D1.**
- [ ] **C7**: add the `ρ > 4h` / `> 2h` threshold to `invariant`; add the x^{1/4} form to
      `bound_then`; fill `move` (explicit formula) and `composition` (multiplicativity of ω).
- [ ] **case 7**: split — 7a positive, 7b control with an explicit level flag. Controls 2 → 3.
- [ ] **case 2**: split the after-board credit (CLP method / EG theorem).
- [ ] **N16, N20**: add the qualifiers (sub- vs full multiplicativity; the proved-tightness
      range).
- [ ] **`DIAGNOSTIC.md`**: replace N3's stated reason with Peluse's codimension-cost version.
- [ ] **`debts.json`**: D1 closed; D19 from ten rows to four; control 15 opened.
- [ ] **New**: log the variational-ceiling proposal as a candidate diagnostic with its
      caveats, and log the "what level / what substrate" axis as a gap in the catalogue.

## 7. What is still open, and how to close it

| row | route |
|---|---|
| control 15 | arXiv:2302.07211 — one transcript |
| C12 | math/0211159 — one transcript, low stakes (case 12 fits no transformation) |
| C10 | probably unimprovable by transcript; primaries are largely pre-arXiv |
| N16, N20 | low priority; search already gives them in substance |

**A closing note on priority.** Citations were task 1 of 8 and are now in good shape.
Further effort here has worse returns than the two things actually blocking the programme:
**D20** — whose commit message says three blind raters ran, but whose key file, rater
sheets and scorer output are nowhere in the tree, with `debts.json` still marking it
`open` — and the **missing telegraph baseline**, without which the rebuilt diagnostic's
4-fires / 0-false-positives headline is a raw accuracy the repo's own inherited rule
forbids quoting.
