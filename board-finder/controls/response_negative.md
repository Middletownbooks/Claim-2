# Negative control — respondent's verbatim reply

Fresh subagent context, tools forbidden, given only the triage prompt and the one input.
It did not know another control existed, nor which of the two it had.

---

## Step 1 — The five slots, as recorded

**STATE** — a class C of symmetric convex bodies in R^n. (Recorded as a *class*, not as an indexed sequence, and with no slot tying C to the target body c·B_∞^n. Nothing in the board mentions l_∞, the cube, or the constant to be bounded.)

**MOVE** — K ↦ K * v, "convolution with (1/2)(δ_v + δ_{−v})", for the next vector v with ||v||_2 ≤ 1; C required to be closed under it.

**INVARIANT** — membership in C. (No property of C is recorded other than the closure demand in MOVE and the origin condition in TERMINAL.)

**COMPOSITION** — none recorded. The phrase "the next vector" presupposes an n-fold iteration, but the board does not say how steps combine: not the order, not which direction the set inclusion runs, not how a sign ε_i is extracted from a step, not how the n bodies are indexed against the n vectors. This is the load-bearing omission (see the kill test).

**TERMINAL** — every member of C contains the origin. Yields: nothing, as literally stated — a nonempty symmetric convex set contains 0 automatically, since x ∈ K and −x ∈ K give 0 = (x + (−x))/2. The only content this slot can carry is *nonemptiness*, and it can only produce the theorem if the iteration is run **backwards** from K_0 = c·B_∞^n, so that "0 ∈ K_n" is the base of a forward unwinding. That reading is not recorded.

Two silent repairs the board needs before it is even a candidate: (i) the move must be read as "pass to a convex K′ **contained in** (K+v) ∪ (K−v)", not as a formula; (ii) STATE must be initialised at the target cube. Without (i) and (ii) the TERMINAL cannot reach the theorem.

## Step 5 — Triage

**T1. Can the invariant be verified on the STARTING state, by an independent computation, without knowing whether the target theorem is true?**

**No — as recorded this is a RESTATEMENT.** Saying it plainly: the invariant is "membership in C", and the only thing C is required to satisfy is precisely the property that makes the induction go through. Checking the invariant on the starting state means checking "c·B_∞^n ∈ C", which is unverifiable until C is named by some *external* property. The board is a template with the hard lemma named but not supplied; its single non-vacuous requirement (closure) is an unproved existence statement. It is not quite equivalent to the theorem — the closure scheme implies Komlós by unwinding, but the converse is not automatic, so it is a possibly-stronger certificate scheme rather than a literal logical restatement.

The board becomes non-vacuous exactly when C is named. And then T1 has a striking answer: **the T1 computation *is* the whole bound.** For every instantiation I know how to write down, the entire cost is paid at initialisation, not accumulated over steps:

- C = {convex K : γ_n(K) ≥ 1/2}, vectors rescaled to ||v||_2 ≤ 1/5. T1: yes, independently checkable. γ_n(c·B_∞^n) = (1 − 2Q(c))^n with Q(c) = P(g > c). This is ≥ 1/2 iff Q(c) ≲ (ln 2)/(2n), i.e. c ≍ √(2 ln n). For *constant* c it is e^{−Θ(n)}. So this instantiation is hard-capped at O(√log n) — and the cap is entirely in the starting-state check, because the invariant is *exactly* conserved along the n steps.
- Anisotropic Gaussians buy nothing: with covariance diag(σ_i²), the move needs ||Σ^{−1/2}v||_2 ≤ 1/5, forcing min σ_i ≳ 5, while initialisation needs c/σ_i ≳ √(2 ln n) per coordinate. The pair (measure, norm bound) enters only through their ratio — the tradeoff is scale-invariant, so no Gaussian escapes √log n.
- C = {r·B_2^n} (the simplest genuinely closed family): the move gives r² ↦ r² − ||v||² at best (for ||x|| ≤ √(r²−||v||²), min_± ||x ± v||² ≤ ||x||² + ||v||² − 2|⟨x,v⟩| ≤ r²; and the section of any admissible K′ by v^⊥ is capped by the waist √(r²−||v||²)). Over n unit vectors this needs r_0 ≥ √n, i.e. c = √n — the trivial bound.

**T2. Is the legal move a FORMULA, or does it need an EXISTENCE THEOREM?**

**An existence theorem.** The formula reading of "convolution" — K ↦ conv((K+v) ∪ (K−v)) = K + [−v, v] — is refuted below; the union itself is not convex, so remaining in a class of convex bodies requires *choosing* a convex subset. The theorem needed is Banaszczyk's subset/gluing lemma (1998): if K ⊆ R^n is convex with γ_n(K) ≥ 1/2 and ||v||_2 ≤ 1/5, there exists a convex K′ with γ_n(K′) ≥ 1/2 and K′ ⊆ (K+v) ∪ (K−v) (built by cutting the two translates along a hyperplane and gluing).

What it costs: (a) it is Gaussian-specific — it leans on properties of γ_n (rotation invariance, isoperimetric/Ehrhard-type convexity), so it fixes the currency in which T1's initialisation bill is paid, and that bill is √(2 ln n) on the cube; (b) the threshold 1/2 and the radius bound 1/5 are coupled and cannot be traded to give a constant; (c) it was originally non-constructive (algorithmic versions came much later); (d) **it is incompatible with "symmetric" in STATE** — the glued body is not symmetric, and symmetry cannot be restored (see kill test).

## THE KILL TEST

**The single computation:** in R², take K = B_2 (unit disc) and v = e_1 (||v||_2 = 1, legal). Compute the largest symmetric convex K′ ⊆ (K+v) ∪ (K−v), and separately check whether every point of the convolution K + [−v, v] admits a sign returning it to K.

**Ran it. Both halves fail, and they kill the two possible readings of the unrecorded COMPOSITION slot.**

1. *Formula / forward reading.* K + [−e_1, e_1] is the stadium {x : dist(x, [−e_1, e_1]) ≤ 1}. The point (0,1) lies in it, but (0,1) ± e_1 = (±1, 1) has norm √2 > 1, so neither sign returns it to K. The inclusion needed for any unwinding runs the wrong way. Under this reading the whole board is trivially satisfiable — iterating gives the zonotope c·B_∞ + Σ_i[−v_i, v_i], 0 is in it from step 0, and no bound on ||Σ ε_i v_i||_∞ follows. It proves nothing.
2. *Backward / subset reading, with STATE as recorded.* (B + e_1) and (B − e_1) are externally tangent at the origin. Along a line through 0 in direction u, the union is the segment {t u : |t| ≤ 2|u_1|}, so the union contains **no ball around 0**: any direction with |u_1| < ρ/2 escapes at radius ρ. Hence every symmetric convex subset of the union has empty interior — it is contained in a line, and is Lebesgue-null and γ-null. So a class of symmetric convex *bodies* containing the Euclidean ball cannot be closed under the move at ||v||_2 = 1.

The general mechanism, for the record: the central section is the culprit. ((K+v) ∪ (K−v)) ∩ v^⊥ equals the union of two *off-centre* slices of K (at levels ±||v||² in direction v), shifted to the origin. So the move replaces central sections by off-centre slices; for K = r·B_2 this is exactly r² ↦ r² − ||v||², and at ||v|| = r it collapses.

**Diagnosis, not a death sentence.** The board survives only after four edits, three of which are forced by the kill test: drop "symmetric" from STATE (Banaszczyk's bodies are not symmetric); rescale to ||v||_2 ≤ 1/5 (harmless, costs a constant); record COMPOSITION explicitly as *backward construction K_0 = c·B_∞^n, K_1, …, K_n with K_i ⊆ (K_{i−1} + v_i) ∪ (K_{i−1} − v_i), then forward unwinding of the signs from 0 ∈ K_n*; and name C by an externally checkable invariant so that T1 has an answer. With those edits the board is sound — and it is capped at O(√log n) by the T1 computation, not by any step loss.

**Where an O(1) would have to come from, on this board.** Because the invariant is exactly conserved along the steps, the *only* place to win is the starting-state check. The design target is therefore: a measure μ (or non-measure potential) that is cheap to translate by a unit l_2 vector yet gives mass ≥ 1/2 to a cube of *constant* side. A useful necessary condition that is easy to test: μ((K+v) ∪ (K−v)) ≥ 1/2 whenever μ(K) ≥ 1/2. I ran it on hard-cutoff candidates and they die immediately: for μ uniform on [−a, a]^n, K = the support and v = (1/√n, …, 1/√n), the shifted copies retain only Π_i(1 − 1/(2a√n)) ≈ e^{−√n/(2a)} of the mass, so μ(union) ≤ 2e^{−√n/(2a)} ≪ 1/2. Compactly supported product measures are dead. Soft cutoffs are not: a marginal that is Gaussian on [−c, c] and then decays at rate A = ln n survives the same diagonal-shift test (the mass gained on the right nearly cancels the mass lost on the left; the net relative loss is O(A²/n) over all n coordinates) while giving γ-mass e^{−Θ(1)} to a constant-side cube. So the barrier is specific to the *standard* Gaussian, not to the measure-invariant family as such; the open cost is that the gluing lemma is proved by Gaussian-specific tools, and nobody has it for a soft-truncated measure. That is the honest live opening this board points at.

## (c) Recognition

Yes. This is the Komlós conjecture (vector balancing, the Beck–Fiala circle: for ||v_i||_2 ≤ 1 the conjecture is ||Σ ε_i v_i||_∞ = O(1); Beck–Fiala's 2t−1 for t-sparse columns is the discrete cousin; the lower bound is a constant, e.g. v_i = e_i forces 1). The proposed board is the skeleton of **Banaszczyk's 1998 argument** ("Balancing vectors and Gaussian measures of n-dimensional convex bodies", Random Structures & Algorithms) with the class left abstract: he takes C = {convex K : γ_n(K) ≥ 1/2}, vectors of norm ≤ 1/5, and proves exactly the closure lemma that T2 demands, with the backward-then-unwind composition the board leaves unrecorded. Because γ_n(c·B_∞^n) ≥ 1/2 needs c ≍ √(2 ln n), that yields ||Σ ε_i v_i||_∞ = O(√log n) for Komlós (and O(√(t log n)) for Beck–Fiala).

What happened next: Banaszczyk's bound has stood since 1998 and is still the best known. The subsequent work made it constructive rather than stronger — Bansal–Dadush–Garg gave an algorithm matching the Banaszczyk bound for Komlós (2016/2019), Bansal–Dadush–Garg–Lovett's Gram–Schmidt walk (2018) gave a constructive subgaussian version, and Dadush–Garg–Lovett–Nikolov gave convex-geometric reformulations; Dadush–Nikolov–Talwar–Tomczak-Jaegermann extended Banaszczyk-type balancing to general norms. Earlier methods (Beck's entropy method, Spencer's six standard deviations, Lovett–Meka's random walk) compose over O(log n) rounds of partial colouring and lose the same √log n. Komlós itself, and the Beck–Fiala conjecture, remain open as of my knowledge; the √log n gap in the l_∞ case has never been closed, and on this board it sits entirely in the T1 check on the cube.
