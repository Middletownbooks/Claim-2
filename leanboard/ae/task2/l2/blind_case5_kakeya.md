# Blind re-encoding — case 5, finite-field Kakeya (cutoff 2008-02-29)

state: a partial counting certificate for K — lines indexed by direction set,
plus either incidence data (bush/hairbrush) or Fourier-side restriction data.
Encoder notes explicitly: "Nothing is yet a polynomial vanishing on K — that
object does not appear in any pre-cutoff attempt."

move: two kinds. (1) bush/hairbrush plus Cauchy-Schwarz slicing — EXPLICIT
formula. (2) sum-product dichotomy on the direction set — REQUIRES AN EXISTENCE
THEOREM (Bourgain-Katz-Tao, proved by compactness/contradiction, giving only a
qualitative eps(delta) > 0, not an effective value).

invariant: an exponent gamma with the current k-dimensional slice certified at
size >~ q^{gamma k}, degrading slightly under slicing; plus the additive/
multiplicative energy of the direction set, bounded only in aggregate.

composition: Kakeya-ness is hereditary under generic hyperplane slicing, so an
(n-1)-dimensional bound feeds back. The sum-product dichotomy composes by an
exhaustive but non-additive case split, and the eps-loss compounds at every
level of the induction.

terminal: |K| >= c_n q^{gamma(n)} with c_n non-explicit and gamma(n) a rational
exponent, not the conjectured n.

bound: TWO REGIMES, not one.
 - general n: |K| >= c_n q^{4n/7} (Rogers 2001; Mockenhaupt-Tao, Duke 121
   (2004) 35-74; both resting on Bourgain-Katz-Tao GAFA 14 (2004) 27-57).
 - small n: Wolff's |K| >= c_n q^{(n+2)/2} REMAINS BEST, because (n+2)/2
   exceeds 4n/7 for n < 14. "there is no single exponent beating both regimes
   uniformly in n as of the cutoff."

leaks:
 - "exponent 4n/7 vs conjectured n" | FEASIBILITY THEOREM | the BKT sum-product
   step supplies only a qualitative growth exponent.
 - "c_n degrading badly in n" | ITERATION COUNT | each dimension-reduction step
   reuses the non-constructive eps(delta); composing n steps multiplies shrinking
   constants.
 - "exponent (n+2)/2 in Wolff's bound" | UNION BOUND OVER MANY ITEMS | the bush
   argument double-counts incidences uniformly across all directions with no use
   of structure in the direction set.

sources: Wolff 1999, Katz-Tao, Rogers 2001, Bourgain-Katz-Tao 2004,
Mockenhaupt-Tao 2004, Faber arXiv:math/0510356.

RECOGNITION: YES — Dvir, arXiv 3 March 2008, JAMS 22 (2009) 1093-1097, |K| >=
c_n q^n by the polynomial method. Self-reported contamination: states the later
work did NOT influence state/move/invariant/composition/terminal, "since that
object simply was not part of any legal move available before the cutoff", and
influenced bound/leaks "only in the negative sense of confirming ... which
factors were artefacts", with the diagnosis argued from the pre-cutoff proof
structure.

## VERIFIED CORRECTION TO THE P1 ENCODING

Fable's P1 case 5 gives the before-bound as "|K| >~ q^{(n+2)/2}, later
~q^{4n/7}", ordering them as though 4n/7 simply superseded (n+2)/2 — and Fable
itself flagged this line as a verification debt.

The blind encoder is right and the debt is real. `DERIVED HERE`:
(n+2)/2 > 4n/7  <=>  7n + 14 > 8n  <=>  n < 14, with equality at n = 14.

| n | (n+2)/2 | 4n/7 | better |
|---|---|---|---|
| 3 | 2.500 | 1.714 | Wolff |
| 13 | 7.500 | 7.429 | Wolff |
| 14 | 8.000 | 8.000 | equal |
| 15 | 8.500 | 8.571 | 4n/7 |
| 30 | 16.000 | 17.143 | 4n/7 |

So Wolff's bound was still the best known for every dimension below 14 at the
cutoff. The P1 encoding's `bound` field is incomplete, not merely imprecise:
it collapses two regimes into one and loses the fact that no single exponent
dominated uniformly.
