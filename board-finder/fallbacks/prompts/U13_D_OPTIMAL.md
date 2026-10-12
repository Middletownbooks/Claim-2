# D-optimal designs — fallback target, self-contained

**Use this only if the Hadamard plan has failed its kill test.** That test: re-fit the growth law
`log2(seconds) = a·(−log2 density) + b` on the four-instance density ladder under a seven-seed
protocol, and continue only if the extrapolation puts *v* = 487 under 10⁸ single-core seconds. The
current method gives 2⁴⁹·⁶ s. If that bar was not cleared, Hadamard 2092 is closed and this is next.

**This prompt is self-contained on purpose.** A previous handoff pointed at repository paths that
turned out to be private, and a gate bar came back provisional because of it. Everything you need
is below. Nothing here requires reading a repository.

---

## 1. Why this target

Three previous targets died, each for a different reason, and each reason was cheap to establish
*before* the work rather than after:

- **Headroom** — an exhaustive search region that turned out to sit *inside* the published one
  (height 80 against 3500, at a cost that grows as H⁶).
- **Prior** — a search space that was affordable and almost certainly empty.
- **Deliverable** — a null that was a null about *two specific objects* rather than about the
  quantity a published table records. This one passed reachability in **microseconds** and died
  anyway.

D-optimal designs are proposed because they have the property none of those had: **the record
table is explicitly maintained and public**, so headroom and deliverable are computable on day
one instead of after a literature survey.

## 2. The mathematics — ALL OF THIS IS RECALL, AND VERIFYING IT IS STEP 1

If any of it is wrong, stop and report; the rest of the prompt depends on it.

For an *n* × *n* matrix with entries ±1, Hadamard's bound gives |det| ≤ *n*^(*n*/2), attained
exactly when *n* = 1, 2 or *n* ≡ 0 (mod 4) with a Hadamard matrix of that order. For the other
residues the maximum is smaller and the bounds are different:

- *n* ≡ 1 (mod 4): the **Barba** bound, attainable only when 2*n*−1 is a perfect square.
- *n* ≡ 2 (mod 4): the **Ehlich–Wojtas** bound, `(2n−2)(n−2)^((n−2)/2)`.
- *n* ≡ 3 (mod 4): the **Ehlich** bound.

A matrix meeting the bound for its residue class is a **D-optimal design**. The *n* ≡ 2 (mod 4)
case is the one to work on, and it has a construction that matters here. Writing *n* = 2*v* with
*v* odd, the known route uses two **circulant** ±1 matrices *A*, *B* of order *v* with

> ***A A*ᵀ + *B B*ᵀ = (2*v*−2)·*I* + 2·*J***

which, written in periodic autocorrelation terms, is

> **PAF_A(s) + PAF_B(s) = 2 for every s = 1 … v−1.**

## 3. Why this project in particular

**That PAF condition is the same shape as the one the Hadamard work is already built around** —
there the condition is a sum of PAFs over *four* sequences equal to a constant. So the existing
apparatus should transfer with **two blocks instead of four**:

- cost function `Σ_s res_s²` over the PAF residuals;
- moves that are swaps preserving the row sum, so the search stays on the admissible manifold;
- an exact endgame that splits the move set in half and joins by hash.

If that transfer works, the engineering is a port rather than a build. **Check it early** — if the
two-block case has some structural difference that breaks the transfer, this target loses the
thing that made it attractive and you should say so before building anything.

## 4. The gate. Run it in this order and stop at the first FAIL.

Every bar is a **single threshold with no middle band**. A previous gate used a two-sided test
with an unregistered gap between the thresholds, the answer landed in the gap, and it declined to
score. Do not repeat that. A bar you cannot evaluate counts as **FAIL**, not "unscored" — this is
a go/no-go and the default is no.

**D1 — does the table exist and say what I think it says?**
Find the maintained maximal-determinant tables (the Orrick lineage, plus Koukouvinos–Seberry
surveys). Record: for *n* ≡ 2 (mod 4), which orders have a known D-optimal design, which are open,
and the date each entry last changed.
> **PASS** iff the table exists, is dated, and the open orders form a **finite enumerable list**.
> **FAIL** → stop and report what the table actually is.

**D2 — deliverable.** This is the bar that killed the last target, so do it second, not last.
> **PASS** iff constructing one new object would change a **published table entry**.
> **FAIL** → stop.
Write the sentence that would appear in an abstract, for both outcomes, and check a table moves.
Beware the exact trap that killed MOLS(12): *showing that some particular construction cannot be
extended is not the same as moving the record.*

**D3 — headroom.** Requires a **measured rate**, not an estimate.
> **PASS** iff the smallest open order is reachable in **≤ 10 container-hours** under a cost model
> with a measured throughput behind it. **FAIL** → stop.
State the enumeration count, the measured rate, and what fraction of the space an hour buys.

**D4 — prior.** Is there evidence a design exists at the orders you can reach?
> **PASS** iff the pattern of known solutions does not systematically exclude the reachable
> region. **FAIL** → stop.
Look at how the known entries are distributed against the parameter you are searching, and
register any confound *before* you check it.

**D5 — is our reachable region already inside someone else's?**
> **PASS** iff no published search covers your D3 region by **10×** or more. **FAIL** → stop.

## 5. Rules that are not negotiable, because each cost something

1. **Verify objects, never function returns.** Reconstruct the matrix and check *A A*ᵀ + *B B*ᵀ
   directly. A search reporting success once cost a day.
2. **Positive controls before nulls.** Your code must find a **known** D-optimal design at a
   solved order before any null is reported. A search that cannot find a known object proves
   nothing when it finds none.
3. **Negative-test every check.** Break each verifier deliberately and confirm it fails. Two
   checks written in one day on this project could not fail at all.
4. **Register predictions before running**, single threshold, no middle band.
5. **Seven seeds, matched caps, medians** for any timing claim. Single-seed timings here were
   bimodal and every one taken before that was discovered was unsafe.
6. **Convert any speedup into the units of the frontier before it changes a decision.** A 17×
   improvement to a search whose cost is the sixth power of the frontier parameter buys 1.6× in
   frontier — that mistake was made on this project and nearly redirected a programme.

## 6. If the gate passes

Pre-register before searching: predictions with single thresholds, the positive controls from
rule 2, and — stated in advance — **what result makes you abandon this and say so**. Then run.

## 7. If any bar fails

Say which, with the evidence, and stop. Do not look for a replacement target; that search has
been run twice and returned empty both times, and the reason is understood: a screen that selects
for problems settled by one finite object in a huge space is selecting for problems whose frontier
is set by search capacity, which is the one thing that does not improve. Report the failure and
wait.
