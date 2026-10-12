# arXiv URLs for the open citation rows

Ordered by value per transcript. Every arXiv id below was confirmed by search this session, not
recalled — but **the titles and dates are search-reported, so treat the arrival of the paper itself
as the verification**, and if a URL turns out to be a different paper than described, that is the
answer and the row stays open.

Three of the rows can be closed by **one transcript each**, and two of those transcripts close
several rows at once. Stop after item 3 and the three must-have rows are done.

---

## 1. C9 — both halves, one document

**https://arxiv.org/abs/1707.00119**
Pierce, *The Vinogradov Mean Value Theorem [after Wooley, and Bourgain, Demeter and Guth]*.
Séminaire Bourbaki, June 2017; Astérisque, Exposés Bourbaki 407 (2019), 479–564 — so roughly 85
pages. v2 revised 25 July 2020.

A Bourbaki survey states the prior state of the art before the new work, which is exactly what this
row needs. **Look for:** the classical threshold, `s ≳ c·k² log k`, attributed to
Vinogradov–Linnik and sharpened by Karatsuba–Stechkin and Wooley 1992 — and the reason the log k is
there (the classical recursion recovers a fixed fraction of the defect per round, so ~log k rounds
are needed). That second clause is the *leak* for case 9, not just the bound, and a survey is more
likely to state it explicitly than the primary is.

This is the highest-value single transcript in the list: it closes D1, and it independently
re-covers the Wooley chronology that voided case 9 in L2.

## 2. C4 — the δ ≲ 1/log n threshold

**https://arxiv.org/abs/math/0209078**
Weaver, *The Kadison-Singer problem in discrepancy theory*, submitted 7 September 2002. Short.
**Look for:** the statement of KS₂ — vectors with Σvvᵀ = I and ‖v‖² ≤ δ, partitioned into two parts
each with norm ≤ ½ + ε — and any statement of what δ the then-available methods required.

**https://arxiv.org/abs/1306.3969**
Marcus–Spielman–Srivastava, *Interlacing Families II: Mixed Characteristic Polynomials and the
Kadison-Singer Problem*.
**Look for:** the introduction's account of what the matrix-Chernoff route gave before, and the
size of the loss. Search already corroborates that the earlier bounds were "worse by a factor that
is logarithmic in the dimension" and that interlacing families removed it; what is missing is a
source stating the threshold as **δ ≲ 1/log n**. If neither paper says it in that form, that is
worth knowing — the row should then be *reworded* to the log-dimension loss it can support, rather
than left claiming a threshold nobody stated.

## 3. C3 — the Shannon attribution

**Shannon 1956 (IRE Trans. IT) and Lovász 1979 (IEEE Trans. IT) both predate arXiv**, so there is no
primary URL. A surrogate that states the attribution is what the row needs:

**https://arxiv.org/abs/1807.00169**
Zuiddam, *The asymptotic spectrum of graphs and the Shannon capacity*.

**https://arxiv.org/abs/2506.14654**
*A group-theoretic approach to Shannon capacity of graphs and a limit theorem from lattice packings*.

One of these two carries the sentence search surfaced: *"Shannon introduced an upper bound in
[Sha56], which is known as the fractional packing number, Rosenfeld number, or fractional clique
cover number."* I could not tell which from the snippet, so either will do and one may be enough.

**Look for:** that Shannon's 1956 upper bound on zero-error capacity is the fractional clique cover
number. The *value* 5/2 for C5 does not need a source — C5 is vertex-transitive so χ_f = n/α = 5/2,
and it is self-complementary so the clique-cover convention does not matter. **The attribution is
the whole ask.** Case 3 is the diagnostic's one principled false negative, and the false negative
depends on the pre-Lovász invariant already being multiplicative — that is, on the before-board's
invariant being α\*.

---

## Worth having if you are transcribing anyway

## 4. N3, plus two rows it closes for free

**https://arxiv.org/abs/2206.10037**
Peluse, *Recent progress on bounds for sets with no three terms in arithmetic progression*.
Séminaire Bourbaki, Astérisque 438; 33 pages. v1 20 June 2022, v2 25 September 2023.

**Look for:** Behrend's 1946 lower bound, stated as a formula. Search reports it as
`r₃(N) ≥ N·2^(−(2√2+o(1))√(log₂N))`; a Bourbaki text will state it precisely. That is the only part
of N3 still needing a source — the step from there to "power savings are excluded" is derived
arithmetic (see `CITATIONS_ASSIST.md`).

This one transcript also covers **Croot–Lev–Pach and Ellenberg–Gijswijt** (case 2's held-out
after-board) and **Kelley–Meka** (control 15), both of which the survey is explicitly about. Three
rows from one document.

While you have it: search reports a recent **quasipolynomial** improvement on Behrend
(arXiv:2406.12290, June 2024 — the first improvement beyond lower-order factors since 1946). It does
not change N3's status, but it is a twin-decay event and the re-check date should record it.

## 5. C12 — Perelman, primary

**https://arxiv.org/abs/math/0211159**
Perelman, *The entropy formula for the Ricci flow and its geometric applications*, 11 November 2002.
**Look for:** W-entropy and reduced volume giving κ-noncollapsing, and the no-local-collapsing
theorem excluding a singularity modelled on the cigar soliton crossed with a line.

Lower priority than the first four: case 12 fits none of the five transformations, so it is doing
less work than C3 or N3 — but it is the primary source, and it is one document.

## 6. N20 — Kővári–Sós–Turán tightness

Search already gives this row in substance: **Kollár–Rónyai–Szabó's norm graphs show tightness for
t ≥ s!, improved by Alon–Rónyai–Szabó to t ≥ (s−1)! + 1**, and KST is tight up to constants in that
range. If you want it sourced rather than snippet-corroborated:

**https://arxiv.org/abs/2311.13662** — *Zarankiewicz's problem via ε-t-nets*, or
**https://arxiv.org/abs/1705.01979** — *Zarankiewicz's problem for semi-algebraic hypergraphs*.

Either should restate the classical bound and the norm-graph tightness in its introduction. Note the
twin is only valid in the range where tightness is *proved*; whether KST is tight for t ≥ 4 is
reported as still open, so N20's statement should carry the range.

## 7. N16 — border rank submultiplicativity

Search corroborates both halves: border rank is **submultiplicative under the Kronecker product**
(possibly strictly), and **ω = liminf log_n(R̲(M_⟨n⟩))** — the exponent is defined through a limit of
tensor powers.

**https://arxiv.org/abs/1706.05074** — *Polynomials and the exponent of matrix multiplication*, or
**https://arxiv.org/abs/1801.04852** — *Border rank is not multiplicative under the tensor product*.

The second is directly on the multiplicativity question and would settle the exact form of the
claim, which matters here: N16's role as a negative depends on the law being *sub*multiplicative
rather than multiplicative, and 1801.04852 exists precisely because the distinction is real.

---

## Rows I would not spend a transcript on

**C7** (GPY / Bombieri–Vinogradov) and **C10** (parallel repetition) are corroborated well enough by
search that another document is unlikely to change them, and neither is load-bearing for a
diagnostic verdict. If you want them anyway: Granville, *Primes in intervals of bounded length*
(**https://arxiv.org/abs/1410.8400**) for C7.

**C5** (Kakeya) is already corrected and verified by derivation. **C9's date** is already
corroborated twice, including by the NASA ADS bibcode; item 1 above is for the *classical bound*
half, not the date.

---

## One note on how these get recorded

A transcript pasted into the conversation is a **fetched primary source** by the project's own
standard, and outranks everything in `CITATIONS_ASSIST.md`. Where a transcript and a search snippet
disagree, the transcript wins and the snippet-based row should be corrected, not reconciled. Two of
this project's existing corrections came from exactly that kind of collision.
