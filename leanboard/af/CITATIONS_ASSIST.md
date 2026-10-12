# Reply to the seven-citation request

**Read the tier line before using any of this.** Every egress route is blocked from my container
too — not just arxiv.org, export.arxiv.org, api.crossref.org and doi.org, but also archive.org,
mathworld.wolfram.com, ar5iv, semanticscholar, zbmath, dblp, numdam, annals.math.princeton.edu and
en.wikipedia.org. The gateway answers 403 to CONNECT. Web search is the only working channel here,
exactly as in your container.

So **I cannot give you the tier you asked for.** Nothing below is a fetched primary source. What
follows is in three tiers, and the tier matters more than the content:

| tier | meaning | how to record it |
|---|---|---|
| **DERIVED** | needs no source; the arithmetic is here and you can re-run it | `COMPUTED` |
| **SEARCH-CORROBORATED** | search snippets from queries you may not have run — **the same tier as your existing 23 rows**, not better | `VERIFIED` only if your standard already admits it |
| **STILL OPEN** | search did not settle it; still needs a pasted primary source | leave `UNVERIFIED` |

Your instruction not to paraphrase from memory is the right standard and I have kept to it. Where a
sentence below is mine rather than a source's, it says so.

---

## DERIVED — two rows need no citation at all

### N3, the "excludes power savings" step

The Behrend *size* needs a source (below). The step from that size to "power savings are excluded"
is arithmetic, and you can close it here.

Search returns Behrend's bound as `r₃(N) ≥ N · 2^(-(2√2+o(1))·√(log₂ N))`. Converting to natural
logs, `2^(-a√(log₂N)) = exp(-a√(ln 2)·√(ln N))`, and with `a = 2√2` the coefficient is
**c = 2√2·√(ln 2) = 2.3548**. So Behrend gives `r₃(N) ≳ N·exp(-2.3548·√(ln N))`.

A power-saving upper bound `r₃(N) ≤ N^(1-δ)` for fixed δ > 0 requires
`exp(-c√(ln N)) < exp(-δ·ln N)`, i.e. `c√(ln N) < δ·ln N`, i.e. `ln N > (c/δ)²`. Beyond that point
Behrend's set is larger than `N^(1-δ)`, so no such bound can hold. **For every fixed δ > 0, Behrend
excludes it.**

**But record the crossover, because it is large:**

| δ | crossover | |
|---|---|---|
| 0.5 | ln N > 22.2 | N > 10¹⁰ |
| 0.2 | ln N > 138.6 | N > 10⁶⁰ |
| 0.1 | ln N > 554.5 | **N > 10²⁴¹** |
| 0.05 | ln N > 2218 | N > 10⁹⁶³ |

N3's status as a negative is an **asymptotic** statement, and the twin should say so in the item.
That is not a weakening — "excludes power savings" is asymptotic by construction — but a twin whose
falsifying regime starts at 10²⁴¹ should not read as though it were checkable.

### C3, the value 5/2

You do not need a source for the number. C5 is vertex-transitive, so its fractional chromatic number
is `n/α = 5/2`, and α(C5) = 2. C5 is also self-complementary, so the fractional-clique-cover-of-the-
complement convention and the fractional-chromatic-number-of-G convention give the same 5/2 and the
usual ambiguity about which side the clique cover lives on does not bite here. Record 5/2 as
`COMPUTED`.

**What you still need a source for is the attribution** — that *Shannon* stated the fractional clique
cover as the upper bound. See C3 below; that half did not verify.

---

## SEARCH-CORROBORATED — four rows, at your existing tier

### C9 — the Wooley date. This is the one I would most want you to have.

Two independent search routes return it, and one is a bibliographic database rather than a prose
summary:

- arXiv listing: *"Vinogradov's mean value theorem via efficient congruencing"*, Trevor D. Wooley,
  **arXiv:1101.0574, submitted 3 January 2011**; published *Annals of Mathematics* **175** (3),
  1575–1627, 2012.
- NASA ADS carries the same record under the bibcode **2011arXiv1101.0574W**, which encodes the 2011
  arXiv year independently of the abstract page.

This is the date that voided case 9 in L2, and you flagged correctly that you had taken it from the
task list rather than a source. It now has two search-reachable corroborations, neither of them me.
**The L2 void stands.**

The other half of C9 — the classical `s ≳ c·k² log k` — did **not** verify. Still open (D1).

### C7 — GPY and Bombieri–Vinogradov

Search returns, in substance: GPY gives bounded gaps if the primes have level of distribution
θ > 1/2; Bombieri–Vinogradov establishes level of distribution θ for every θ < 1/2, i.e. θ = 1/2 − ε;
GPY themselves pointed out that Bombieri–Vinogradov with 1/2 replaced by any strictly larger constant
would suffice. That is exactly your row, including the "exactly 1/2" framing.

Reachable secondary sources: Granville, *Primes in intervals of bounded length* (arXiv:1410.8400);
the Annals versions of Zhang and of Maynard, *Small gaps between primes*, Annals **181** (1). Both
after-boards (Maynard's multidimensional weights, Zhang's smooth moduli) are corroborated as real and
distinct, so the two-accepted-answers rubric is safe.

### C10 — parallel repetition

Search returns: **Fortnow** first showed that the multiplicative-decrease idea is false; **Feige**
later gave a simpler example; Feige–Verbitsky, *Error reduction by parallel repetition — a negative
result* (2002). **Raz 1995**: for a 2-prover 1-round game with val(G) = 1−ε,
`val(G^n) ≤ (1−O(ε^c))^Ω(n/log(|A||B|))` — sub-exponential decay, not multiplicative. **Holenstein**
(c. 2006) simplified and improved Raz to c = 3.

Your `target_law = "none"` rests on the counterexamples, and the counterexamples are corroborated,
including the Fortnow-then-Feige ordering your row states.

### C4 — Weaver KS₂, partial

Corroborated: matrix Chernoff bounds for sums of independent rank-one matrices "provided bounds worse
by a factor that is logarithmic in the dimension", and the Marcus–Spielman–Srivastava interlacing-
families proof "avoided the logarithmic dimension factor". So **the log-n dimension loss on the
matrix-Chernoff route is real and is exactly what MSS removes** — which is what case 4 needs, and
what makes its `bound_law = additive → max` reading work.

**Not corroborated: the specific threshold `δ ≲ 1/log n`.** No reached source stated it in that form.
Record C4 as `PARTIAL`: the mechanism verified, the constant not. If you want the row closed, that is
the sentence to ask for.

---

## STILL OPEN — two rows search could not settle

### C3 — the Shannon attribution

Corroborated: Shannon introduced zero-error capacity in 1956 (IRE Trans. IT) and **computed the
capacity of every graph on five or fewer vertices except C5**; Θ(C5) = √5 was open until **Lovász
1979**. So your before-board's shape — a gap open from 1956 to 1979 — is right, and √5 is the
*lower* bound Shannon gave via five pairwise non-confusable two-letter words in C5⊠C5.

**Not corroborated: that the 5/2 upper bound is Shannon's, via the fractional clique cover.** No
reached source said it. The number is derivable (above); the attribution is not. Since case 3 is the
diagnostic's one *principled false negative*, and the false negative turns on the pre-Lovász
invariant already being multiplicative, the attribution is load-bearing — it is the claim that the
before-board's invariant was α\*. Keep `UNVERIFIED` and ask for it specifically.

### C12 — Perelman, partial

Bibliographic record corroborated: *The entropy formula for the Ricci flow and its geometric
applications*, Grisha Perelman, **math/0211159, 11 November 2002**. The abstract, as returned, states
a monotonic expression valid in all dimensions without curvature assumptions, and that injectivity
radius is controlled by curvature where finite-time singularities form.

Corroborated in substance from a secondary source: a singularity could be modelled on the product of
the **cigar soliton** with a line, and Perelman removed that obstruction with a local injectivity
radius estimate built from **an entropy functional and a reduced distance function** — i.e. W-entropy
and reduced volume giving κ-noncollapsing, which is your row.

**Not corroborated from the primary.** Record `PARTIAL`. Case 12 fits no transformation, so it is
doing less work than C3 or N3; I would not spend a user request on it.

---

## One thing worth adding to the twin register, unprompted

Search surfaced a **decay signal on N3**. Since 1946 Behrend's construction had been improved only in
lower-order terms (Elkin, Green–Wolf). Recent work — Hunter, and *Improving Behrend's construction*,
arXiv:2406.12290 (18 June 2024) — is described as the **first quasipolynomial improvement**, the first
beyond lower-order factors.

**This does not change N3's status**: a quasipolynomial improvement to a sub-power-saving bound is
still sub-power-saving, so power savings remain excluded and N3 remains a valid negative. But it is
exactly the class of event that took Erdős distinct distances in R³ out of your twin set and into
`REJECTED.json`. Worth a re-check date on N3 with this noted, and worth checking whether any of the
other seven "standard" twins have had similar movement.

---

## What to ask the user for, if you ask for anything

Three rows, in this order, each needing one or two sentences:

1. **C3** — that Shannon's 1956 upper bound on zero-error capacity was the fractional clique cover
   number α\*, giving 5/2 for C5. *(Load-bearing: the diagnostic's one principled false negative.)*
2. **C4** — the sentence stating the δ ≲ 1/log n threshold for the matrix-Chernoff / random-partition
   route to Weaver's KS₂. *(Closes a PARTIAL on a positive the diagnostic fires on.)*
3. **C9, second half** — the classical pre-Wooley `s ≳ c·k² log k`. *(D1; the date half is now
   corroborated twice and does not need asking.)*

N3's citation is no longer the blocker it was — the size is search-corroborated and the
power-saving step is derived here. C7, C10 and C12 I would let stand at the tier they now have
rather than spend a request on.
