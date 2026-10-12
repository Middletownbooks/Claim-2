# Raw gate response — record 235, SIC/Zauner — verbatim

Returned by a Claude chat surface (web search + fetch, Opus) against
`../PROMPT_GATE_SIC.md` Part A, 2026-09-20. Stored unedited. **Nothing here was fetched by
this session**; all URLs, dates and quotes are relayed. Tier: SECONDARY-RELAYED.

The respondent noted a constraint up front: it did not reproduce full verbatim sentences
from copyrighted papers, giving short fragments (under 15 words, one per source) plus a
precise pointer instead. The fragments do contain the numbers at issue, so the prompt's
quote rule is met in substance; the exact sentences are checkable at the URLs.

Adjudication: `../GATE_RESULT_SIC.md`.

---

## (a) The exact-solution set

verdict: CORRECTED (relative to the commonly-cited 2017 picture) — whichClaim: EXACT

Source 1 — Bengtsson & Grassl, "A Conjecture on Almost Flat SIC-POVMs", arXiv:2512.13201,
December 2025. https://arxiv.org/abs/2512.13201
quote: "Exact solutions are known for all dimensions $d \le 57$"
note: explicitly labelled "exact", contrasted with the numerical statement in the same
paragraph, so unambiguous for claim (2).

Source 2 — Appleby, Flammia & Kopp, "A Constructive Approach to Zauner's Conjecture via the
Stark Conjectures", arXiv:2501.03970 (v2, 17 Mar 2025). https://arxiv.org/abs/2501.03970
quote: "constructed 1-SICs exactly in every dimension ≤53" — and in the same sentence, in
many further dimensions up to a maximum of 5799.
note: unambiguously EXACT. Note 5799, not 39604, as their exact ceiling.

Source 3 — Kopp & Lagarias, "SIC-POVMs and orders of real quadratic fields", arXiv:2407.08048
(latest version 13 May 2026; J. Number Theory). https://arxiv.org/abs/2407.08048
quote: "Weyl–Heisenberg SICs in all dimensions $1 \le d \le 53$", described as rigorously
constructed, plus the Hoggar lines at d=8.

Source 4 — the historical baseline, DO NOT treat as current. Flammia's "Exact SIC fiducial
vectors" table, https://www.physics.usyd.edu.au/~sflammia/SIC/ , last dated update
21 Sep 2017. Listed: 2, 3, 4–21, 24, 28, 30, 31, 35, 37, 39, 43, 48, plus 8H (Hoggar), and
124 and 323 added in the Sep 2017 update.
note: stale by roughly nine years and the single most likely source of a wrong repository
fact. It was the state of the art in 2017 and is still the first search hit.

Source 5 — Kopp, "SIC-POVMs and the Stark Conjectures", IMRN 2021.
https://www.its.caltech.edu/~matilde/StarkConjecturesOpValuedMeasures.pdf
Listed as proven by explicit construction: 1–21, 24, 28, 30, 31, 35, 37, 39, 43, 48, 124,
323, with a then-unpublished exact solution in dimension 53 by Grassl and Scott.
note: documents that the holes below 53 existed as recently as 2021 and were filled between
roughly 2021 and 2024.

Source 6 — the high-dimension tail. Bengtsson, Grassl & McConnell, "SIC-POVMs from Stark
Units: Dimensions n²+3=4p", arXiv:2403.02872 (5 Mar 2024; J. Math. Phys. 66, 082202 (2025)):
seventeen dimensions of this form, reaching d=39604. Predecessor: Appleby, Bengtsson, Grassl,
Harrison & McConnell, arXiv:2112.05552 (J. Math. Phys. 63, 112205 (2022)), 13 prime
dimensions, highest p=19603.

Critical caveat on Source 6 — this is the blur the brief warns about. The 2022 Stark-units
paper states of its own solutions that "the exact verification was at best partial" in all
but d=487, with complete high-precision numerical checks everywhere. So the 19603/39604
figures are algebraic constructions whose SIC property is mostly numerically verified, not
fully symbolically verified exact fiducials. That is almost certainly why AFK put the exact
ceiling at 5799 while quoting 39604 as the numerical ceiling.

transcribeThis:
1. arXiv:2501.03970 — Appendix F, "1-SIC data tables", pp. 151–173.
2. arXiv:2403.02872, DOI 10.1063/5.0212617 — Table 1 and the verification table.
3. arXiv:2112.05552, DOI 10.1063/5.0083520 — Table I, Table II, and the list of 49
   dimensions at the end of Section IX.

What could not be settled: the explicit set above d=57. No source found enumerates it; cell
left empty rather than reconstructed.

## (b) THE SHAPE QUESTION

verdict: CONFIRMED (as a prefix), with a scope correction — whichClaim: EXACT
url: https://arxiv.org/abs/2512.13201 — date: December 2025

Answer: PREFIX — for the contiguous range. Hole list below the prefix ceiling: EMPTY.

Both current sources state the exact set covers every dimension up to their ceiling, with no
exceptions noted. There is no published hole at 22, 23, 25, 26, 27, 29, 32–34, 36, 38, 40–42,
44–47, or 49–52 — those were the 2017 holes and they are filled.

The scope correction that matters. "PREFIX" is only true of the contiguous block. Taken
literally, the question — every d below the maximum exactly-known dimension with no published
exact fiducial — has an answer numbering in the thousands, because the maximum is 5799 (AFK's
exact ceiling) or arguably 39604 (if the Stark-units constructions count), while contiguous
coverage stops around 53–57. The set above the prefix is extremely sparse: a handful of
structured families (d = n²+3, the Fibonacci–Lucas family, dimension towers) and nothing else.

So the target set is not a short hole list. It is the unbounded tail d ≥ 58, minus a sparse
sourced list that could not be obtained. If the programme was predicated on "a few scattered
holes to fill below a high ceiling," that premise is wrong.

## (c) The numerical frontier

verdict: CONFIRMED — whichClaim: NUMERICAL

Ceiling. Markus Grassl, QOMBINE seminar abstract, University of Oslo, 17 Sep 2026:
https://www.mn.uio.no/math/english/research/projects/qombine/events/seminars/2026-09-17-grassl.html
quote: "numerical ones have been found for all dimensions up to 196"

Corroborated by Bengtsson & Grassl (Dec 2025): d ≤ 193 by Scott's method, d = 195 from a
relatively simple exact solution, d = 194 and 196 by more involved techniques. AFK (Mar 2025)
state numerical solutions in every dimension ≤ 193 and in further dimensions up to a maximum
of 39604.

Precision. Scott, "SICs: Extending the list of solutions", arXiv:1703.03993 (11 Mar 2017):
quote: "available with 150 digits of precision in the article source files" (for d > 50;
d ≤ 50 in Scott–Grassl 2010).
note: 150 decimal digits is the working standard. Scott's classification is believed complete
for d ≤ 50 (exhaustive) and, within the F_z/F_a eigenspaces, for d ≤ 90.

## (d) Method and competition

verdict: CONFIRMED — whichClaim: EXACT

Pipeline (dominant). Appleby, Chien, Flammia & Waldron, arXiv:1703.05981, J. Phys. A 51,
165302 (2018). https://arxiv.org/abs/1703.05981
quote: "converting high-precision numerical solutions into exact ones using an integer
relation algorithm", in conjunction with the Galois symmetries of the SIC.

So: high-precision numerics → integer-relation recovery of algebraic numbers, exactly as
hypothesised. Front end is Scott's L-BFGS global search minimising the Welch-bound frame
potential, refined in GMP/MPFR to 150 digits. The paper reports 69 new exact solutions in 9
new dimensions.
NOT FOUND: whether the integer relation algorithm is specifically PSLQ or LLL. The abstract
says only "an integer relation algorithm." Don't record a choice.

Second pipeline (producing the high-dimension results). Stark units / ray class fields:
construct fiducial entries directly as square roots of Stark units in a ray class field of
Q(sqrt((d+1)(d−3))), bypassing numerical search. This reaches d = 19603 and 39604. Third
route: AFK's Shintani–Faddeev modular cocycle construction, which subsumes both conceptually.

Is anyone running it now? Yes, actively. Grassl gave a seminar on exactly this on 17 Sep 2026;
Bengtsson & Grassl posted in Dec 2025; the AFK paper is under submission with source code at
https://github.com/sflammia/Zauner.jl ; Kopp & Lagarias revised in May 2026. Not a dormant
field.

Maintained database accepting submissions: NOT FOUND. The Flammia table is a static page last
updated Sep 2017. Zauner's own site hosts d ≤ 14. Scott's numerical solutions ship in arXiv
source files. Zauner.jl is a code repository, not a submission-accepting database. No curated,
versioned, submission-taking SIC registry found.

## (e) Known obstructions

verdict: NOT FOUND — and that absence is itself the finding — whichClaim: ZAUNER-WH

No dimension is known not to admit a WH-covariant SIC. Searched specifically for a
non-existence result, a counterexample, or a ruled-out dimension and found none. Every source
treats the question as fully open in both directions.

No unconditional sub-case is proved beyond "existence follows from explicit construction."
Zauner's conjecture is established in exactly those dimensions where a fiducial has been
exhibited — verified, not proved, and only for finitely many d. AFK's result is the strongest
conditional statement: their construction gives a valid SIC in every case assuming the order-1
abelian Stark conjecture for real quadratic fields and a special-value identity for the
Shintani–Faddeev modular cocycle. Conditional on two conjectures, not a proof.

Two structural facts, neither an obstruction: d = 3 is genuinely exceptional, with infinitely
many equivalence classes of WH SICs, and finiteness conjectured only for d ≠ 3. The Hoggar
lines in d = 8 are a SIC that is not WH(8)-covariant (covariant under Z_2^3 instead) — a
sporadic example, not an obstruction, since d = 8 also has ordinary WH SICs.

transcribeThis: arXiv:2501.03970, §1.5 "The main conjectures" and §1.6 "The main theorems:
existence" — for the precise logical form of what is and is not proved.

## §A The verdict

PREFIX, within the contiguous range. Hole list below the prefix ceiling: EMPTY. No d in 2…53
lacks a published exact fiducial (and per the most recent source, none in 2…57).

Settling quote — Bengtsson & Grassl, arXiv:2512.13201, December 2025:
"Exact solutions are known for all dimensions $d \le 57$"

But the operative finding for the go/no-go is not the hole list. It is that there is no short
hole list. Above ~57 the exact set is sparse and structured (n²+3 families, dimension towers),
and the "gap" is the open tail, not a finite set of oversights. A programme designed to fill
scattered holes below a high ceiling has no target. A programme designed to push the
contiguous prefix from 57 upward has a well-defined target, and is competing directly with
Grassl, who is actively working it with better tools.

## §B Confidence in §A, and what would change it

High that the prefix is ≥53 and has no holes. Three independent groups (Appleby–Flammia–Kopp;
Kopp–Lagarias; Bengtsson–Grassl), across Jan 2025 – May 2026, all state a hole-free prefix.
They would notice a gap.

Moderate on 53 vs 57. The two figures disagree and the disagreement is not resolved by
anything found. The later-dated source (Kopp–Lagarias, May 2026) says 53; the more recent
paper (Bengtsson–Grassl, Dec 2025) says 57. Read: Grassl runs the computations, so 57 is
likely the truer current number and Kopp–Lagarias's sentence is carried over from their
Dec 2024 submission. NOT confirmed. Record 53 as the safe floor and 57 as the probable value,
flagged.

Lower confidence on what "exact" means in the sources. Three standards are in play: (i) SIC
conditions verified symbolically; (ii) fiducial entries given in an explicit number field with
numerical verification only; (iii) a full analysis of the defining number field completed. The
Flammia page already distinguished (ii) from (iii) in 2017; the 2022 Stark-units paper openly
admits it mostly achieves (ii). AFK's 5799-vs-39604 split is almost certainly this
distinction. Do not record a single "exact ceiling" without recording which standard.

A genuine risk to the prefix claim: the fills below 53 may never have been published as data.
Kopp 2021 called d=53 unpublished, from Grassl and Scott. The dimensions 22, 23, 25–27, 29,
32–34, 36, 38, 40–42, 44–47, 49–52 are asserted done in print by 2024 but no public repository
hosting those vectors was found. If the programme needs the vectors, not the claim, the
availability picture may be much worse than the existence picture.

What would change §A: (1) a clean look at AFK Appendix F; (2) any statement from Grassl dating
the 53→57 extension; (3) locating a current data repository, or confirming none exists;
(4) asking Grassl or Flammia directly — a small field, and the answer is one email away, which
is cheaper than anything this programme can compute.

## §C Recall against source

Seven figures held before searching. 3 confirmed, 3 corrected, 1 failed to settle.

1. Exact known for d ≤ 21 plus scattered 24, 28, 30, 31, 35, 37, 39, 43, 48, 124, 323 —
   CORRECTED. That is the 2017 state. Current: hole-free through 53–57. Recall was nine years
   stale and would have produced an entirely fictitious hole list.
2. Numerical frontier ~151, maybe 193 — CORRECTED. 196 as of Sep 2026.
3. Pipeline is high-precision numerics + integer relation on Galois-symmetric data —
   CONFIRMED verbatim by ACFW.
4. Integer relation algorithm is PSLQ — FAILED TO SETTLE. Sources say only "an integer
   relation algorithm." Left empty.
5. Kopp's Stark-unit construction gave the first exact d=23 — CONFIRMED.
6. AFK 2025 proves Zauner conditional on Stark — CONFIRMED, with the refinement that it needs
   two conjectures (Stark + Twisted Convolution), not one.
7. Maximum exact dimension ≈ 39604 — CORRECTED. 39604 is the numerical maximum. AFK put the
   exact maximum at 5799, and the papers reaching 19603/39604 admit their exact verification
   was mostly partial. This is precisely the numerical/exact conflation the brief was built to
   catch, and recall fell into it.

The most useful lines are #1 and #7. Both are cases where the figure supplied from memory was
not merely imprecise but categorically wrong, and both errors point the same direction:
unsourced recall in this field reproduces the 2017 snapshot and silently upgrades numerical
results to exact ones. Weight other unsourced claims in this project accordingly —
particularly any that cite the Flammia table, which is the fossil that keeps the 2017 picture
alive at the top of search results.
