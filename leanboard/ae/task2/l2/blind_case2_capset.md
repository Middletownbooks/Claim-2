# Blind re-encoding — case 2, cap set (cutoff 2016-04-30)

state: triple (n, A, alpha) with A in F_3^n 3AP-free, density alpha, plus the
Fourier data of the balanced function f = 1_A - alpha, and in the refined
version the large spectrum Spec_theta(f). (encoder marked MEMORY)

move: a density-increment step. The 3AP count identity forces some nonzero r
with |fhat(r)| >= c*alpha; this existence step is NON-CONSTRUCTIVE (pigeonhole
on the Fourier side). Meshulam: pass to the hyperplane where that character is
constant, costing codimension 1 per unit density gain. Bateman-Katz: work with
the whole large spectrum and invoke an additive-structure EXISTENCE THEOREM
guaranteeing a low-codimension subspace exists - "a feasibility theorem, not an
explicit construction".

invariant: (i) 3AP-freeness is preserved exactly on any coset; (ii) the rate at
which codimension is spent per unit multiplicative density gain. Meshulam O(1)
per O(1); Bateman-Katz amortised o(1), which is what lifts the exponent from 1
to 1+eps.

composition: each move yields a genuine sub-copy of F_3^{n'}, same shape as
before, so the move reapplies verbatim. Halts because n' decreases and alpha
increases.

terminal: either the trivial bound takes over at small n', or alpha would exceed
1. Unwinding certifies |A| <= 3^n g(n).

bound: |A| <= C 3^n / n^{1+eps}, Bateman-Katz, JAMS 25 (2012) 585-613,
improving Meshulam 3^n/n, JCTA 71 (1995) 168-172. Encoder deliberately declined
to state a numeric eps, flagging any specific figure as low-confidence MEMORY.

leaks:
 - "polynomial-only saving rather than exponential" | TERMINAL CERTIFICATE TOO
   WEAK | the halting argument bounds iterations by a fraction of n, so
   unwinding can only give 3^n/n^power. Grounded pre-cutoff in the gap to Edel's
   ~2.2173^n construction (2004).
 - "the exponent eps" | FEASIBILITY THEOREM | the non-constructive spectral
   structure theorem fixes eps by its own combinatorics.
 - "the baseline linear-in-n cost" | UNION BOUND OVER MANY ITEMS | pigeonhole
   over ~3^n characters, one hyperplane per iteration, summed over ~n iterations.
 - "the constant C" | MULTIPLICATIVE INVARIANT | per-iteration factors compounded
   across the recursion plus base-case patching.

sources: Meshulam 1995, Bateman-Katz 2012, Edel 2004 (all confirmed by search).

RECOGNITION: YES — names Croot-Lev-Pach (5 May 2016) and Ellenberg-Gijswijt
(30 May 2016), c ~ 2.756^n. Self-reported contamination, again localised:
states the later work did NOT influence state/move/invariant/composition/
terminal/bound, but DID influence the framing of the first leak entry — and
says it deliberately grounded that leak in the pre-cutoff Edel-vs-Bateman-Katz
gap rather than in the 2016 solution.
