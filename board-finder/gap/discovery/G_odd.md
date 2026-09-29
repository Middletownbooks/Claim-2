SUMMARY | 34 problems processed. 27 labelled with a RECORD (1, 3, 5, 7, 11, 13, 15, 17, 19, 21, 23, 25, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 55, 57, 59, 61, 63). NO-RECORD: 6 (9, 27, 51, 53, 65, 67). CANNOT EVALUATE (record existence/value not established): 1 (49). MOVE-1 kind UNKNOWN: 8 (1, 3, 5, 7, 11, 31, 39, 61). Provenance: WebSearch summaries only (no paper text readable; arxiv/publishers blocked; WebSearch budget ran out once mid-run and later reset), local computation, and RECALL where tagged. Results dated 2025 or later that surfaced in searches were not used. Precision/refereed tags default to UNKNOWN when not seen.

Tier key: PVL = PRIMARY-VERIFIED-LOCALLY, SS = SEARCH-SUMMARY, RC = RECALL. Format of MOVE lines: date | authors | value | kind | evidence | tier | precision (refereed status given inside evidence).

======================================================================

PROBLEM | 1. Kakeya and Nikodym sets in finite fields
SIDE    | upper — least size is minimised; exhibiting a set gives an upper bound on C^K(d,q), C^N(d,q)
RECORD  | YES (chosen parameter d=2, Kakeya, since statement emphasises none and d=1 is trivial): C^K(2,q) = q(q+1)/2 + (q-1)/2 for q odd, q(q+1)/2 for q even (exact, both sides); Blokhuis-Mazzocca, 2008 [SS]. Nikodym: no pre-2025 construction-side value found.
MOVE-1  | 2008 | Blokhuis, Mazzocca | q(q+1)/2+(q-1)/2 (q odd); q(q+1)/2 (q even) | UNKNOWN | search summary says they "gave exact bounds" (lower-bound proof plus matching size); it does not say who first exhibited the matching construction or how | SS | EXACT; REFEREED-UNKNOWN (Bolyai Soc. volume per RC, not seen)
MOVE-2  | NOT FOUND (attribution of the earlier ~q^2/2 constructions, e.g. Mockenhaupt-Tao style, not established this session)
NOTES   | Higher d: summaries say general Kakeya/Nikodym lower bound q^d/2^(d-1)+O(q^(d-1)) (Dvir; Saraf-Sudan) and constructions of size about q^d/2^(d-1) for Kakeya; not read. Nikodym upper-bound (construction) record before 2025: NOT FOUND (only results dated 2025+ surfaced; not used). Nikodym part of this problem therefore unlabelled.

PROBLEM | 3. Autocorrelation of a non-negative function vs indicator function
SIDE    | lower — C is a best constant valid for all f; one f exhibits a lower bound on C
RECORD  | YES: C >= 0.88922, Matolcsi-Vinuesa, 8 Jul 2009 (step function with 20 steps) [SS]
MOVE-1  | 2009-07-08 | Matolcsi, Vinuesa | 0.88922 | UNKNOWN | summary: "a step function with 20 steps giving c >= 0.88922" (J. Math. Anal. Appl. 372 (2010) 439-447); the method that found the step function is not stated in what I saw | SS | UNKNOWN precision (a step function's value is exactly computable; whether rigorously certified not seen)
MOVE-2  | 2009-04-01 | Martin, O'Bryant | log16/pi = 0.88254 | UNKNOWN | closed-form value suggests an explicit function, but I saw nothing on what the paper did; not inferred | RC (value from the brief) | EXACT (closed form)
NOTES   | Boyer-Li: the brief dates it 'Nov 2024 / 10 Aug 2025'. Search results show arXiv id 2506.16750 (June 2025 submission) and describe it as improving on a 2025 result, so I found no evidence of a Nov 2024 version and treat it as post-cutoff: excluded, value not used. White 2022 (arXiv 2210.16437) concerns a different L2 autoconvolution constant (inf ||f*f||_2), not this ratio; not used.

PROBLEM | 5. Erdos minimum overlap problem
SIDE    | upper — exhibiting f (with g=1-f) upper-bounds the largest guaranteed overlap C
RECORD  | YES: C <= 0.380927 (0.3809268534330870 from a 51-step function), Haugland, 2016 [SS]
MOVE-1  | 2016-09 | Haugland | 0.380927 | UNKNOWN | summary: "a step function [51 steps] that improves the upper bound from 0.382002... to 0.380926... is given", via Swinnerton-Dyer's reduction to step functions; how the step function was found is not stated in what I saw | SS | UNKNOWN precision; PREPRINT seen (arXiv 1609.08000), journal status not seen
MOVE-2  | 1996 | Haugland | 0.382002 (0.38200298812) | UNKNOWN | summary: 21-step function using Swinnerton-Dyer's result (J. Number Theory 58 (1996), 'Advances in the minimum overlap problem'); optimisation method not stated | SS | UNKNOWN; REFEREED (journal listing seen)
NOTES   | Before that: Motzkin-Ralston-Selfridge 1956, 2/5 [SS]. Step count 21 -> 51 suggests a bigger run of the same approach but the sources seen do not say a computer search was used, so no SEARCH-REPEAT label. Lower side (White 2022) is proof-side, not reported.

PROBLEM | 7. Difference bases
SIDE    | upper — a basis of size k for {1..n} gives C <= k^2/n
RECORD  | YES: C <= 2.6571 (n=6166 example, D[6166]^2/6166), Golay 1972 [SS/RC]; whether anything lower exists before 2025 not established
MOVE-1  | 1972 | Golay | 2.6571 (128^2/6166 = 2.65715, PVL arithmetic; the 128 is my deduction from 2.6571*6166) | UNKNOWN | summary quoting Finch's errata: "2.434 <= lim D[n]^2 <= D[6166]^2 <= 2.6571"; attribution of the 6166 example to Golay (J. London Math. Soc. 4 (1972) 729-734) is RC; how it was found not seen | SS+RC | EXACT (finite set)
MOVE-2  | 1963 | Wichmann | ~3 asymptotically (explicit family: n = 12r^2+18r+6 with 6r+4 elements per summary) | ANALYTIC | summary: "Wichmann showed for n = 12r^2+18r+6, l(n) <= 6r+4" (explicit algebraic family) | SS | EXACT; REFEREED (J. London Math. Soc. 1963)
NOTES   | I recalled 2.6457 as the repository figure but found no source for it; not used. Pegg 2020 (Wolfram blog, 'Wichmann-like' rulers) is pre-2025 and may have changed some ruler bounds; I could not tell whether it changes this constant. Lower side (Leech 1956, 2.434; Bernshteyn-Tait 2019) is proof-side.

PROBLEM | 9. Kakeya needle problem (discrete triangles/parallelograms)
SIDE    | upper for C^T, C^P (a configuration bounds min area from above); lower for S^T, S^P (a configuration bounds max score from below)
RECORD  | NO-RECORD: no numeric value at any fixed n and no explicit asymptotic constant found before 2025; only order of magnitude 1/log n (Cordoba lower bound; Keich 1999 sharpness via Schoenberg construction) [SS/RC]
MOVE-1  | NONE (no numeric record)
MOVE-2  | NONE
NOTES   | Keich (Bull. LMS 31 (1999) 213-221) shows Cordoba's bounds sharp using Schoenberg's construction [SS]. The score functions S^T, S^P appear to be defined by this problem set (no earlier source found). Numeric values quoted for Keich's construction in results seen were from 2025 papers: not used.

PROBLEM | 11. Uncertainty principle
SIDE    | upper — exhibiting an f gives an upper bound on the largest constant C
RECORD  | YES: C <= 0.32831, Cohn-Goncalves, Dec 2017 (brief) [brief; not seen in source]
MOVE-1  | 2017-12 | Cohn, Goncalves | 0.32831 | UNKNOWN | one search snippet loosely linked 0.32831 to Cohn et al. "computer search techniques", but it was garbled and concerns eigenfunction quantities A_s(d); I could not confirm what was done for this bar | SS (weak) | UNKNOWN; REFEREED-UNKNOWN (Invent. Math. 2019 paper is the published twelve-dimension paper; whether it contains this figure not confirmed)
MOVE-2  | 2016-02 | Goncalves, Oliveira e Silva, Steinerberger | 0.353 | UNKNOWN | paper (J. Math. Anal. Appl. 451 (2017) 678-711, arXiv 1602.03366) confirmed to exist and to state 0.2025 and 0.353 [SS]; construction method not seen | SS | UNKNOWN
NOTES   | Snippets gave 0.45 <= c <= 0.594 for the eigenfunction (self-Fourier) version, which is a different constant. Cannot verify that Cohn-Goncalves' 0.32831 applies to the exact problem as stated.

PROBLEM | 13. A Linear Programming Bound
SIDE    | upper — an admissible f gives an upper bound on C(n) (Cohn-Elkies LP bound on sphere packing density)
RECORD  | YES (smallest n=1, per rule): C(1) = 1, exact; LP bound trivially sharp in dimension 1 (Cohn-Elkies) [SS]
MOVE-1  | 2003 | Cohn, Elkies | 1 (n=1) | ANALYTIC | summary: bound "trivially sharp in dimension 1"; explicit function (e.g. triangle function) is my recollection, not read | SS+RC | EXACT
MOVE-2  | NONE (n=1 trivial)
NOTES   | Family points: n=8 and n=24 exact (Viazovska 2016; Cohn-Kumar-Miller-Radchenko-Viazovska 2017), both explicit modular-form constructions, ANALYTIC [SS: 'sharp in 8 and 24'; dates RC]. n=2..7 etc.: numerical LP values from Cohn-Elkies 2003 (NUMERICAL/RIGOROUS status not established). Later non-LP (three-point/SDP) bounds are a different quantity.

PROBLEM | 15. Gagliardo-Nirenberg inequality
SIDE    | lower — a test function u lower-bounds the best constant C
RECORD  | YES (family; parameter chosen j=0, m=1, smallest): sharp constants known in 1D, e.g. Nagy inequality, by variational/ODE methods [SS]; general j<m: not established here
MOVE-1  | 1941 | Sz.-Nagy | exact sharp constants for j=0, m=1 (functions of p,q,r) | ANALYTIC | summary: one-dimensional Nagy inequality best constant obtained variationally / from explicit optimisers (year and exact scope RC: Acta Sci. Math. Szeged 10 (1941)) | SS+RC | EXACT
MOVE-2  | NONE
NOTES   | Summaries also say explicit optimisers/constants exist for several Gagliardo-Nirenberg families (Del Pino-Dolbeault, mostly higher dimension). Coverage of j>=1 not established; that part unlabelled.

PROBLEM | 17. Young's convolution inequality
SIDE    | lower — pairs (f,g) lower-bound the supremum C(p,q,r)
RECORD  | YES: exact, Gaussians extremal (sharp constant by Beckner 1975 / Brascamp-Lieb 1976) [RC]
MOVE-1  | 1975/1976 | Beckner; Brascamp, Lieb | exact constant (Gaussian value) | ANALYTIC | RC: proved sharp Young inequality with Gaussian extremisers (proof side); lower bound is the explicit Gaussian computation | RC | EXACT; REFEREED
MOVE-2  | 1961 | Babenko | sharp constants in special cases | ANALYTIC | RC: special exponent cases | RC | EXACT
NOTES   | No search on this problem returned a source; entire block is RECALL.

PROBLEM | 19. The Ovals Problem
SIDE    | upper — a curve gives an upper bound on the infimum C
RECORD  | YES: C <= 1, the circle (kappa = 1 gives lambda_0 = 1) [SS + PVL]
MOVE-1  | <= 2004-02 | Benguria, Loss (posed the problem, conjecture C=1) | 1 | ANALYTIC | summary: "the unit circle yields the upper bound 1"; for kappa=1, H = -d^2/ds^2 + 1 has lowest eigenvalue 1 (checked by hand); first-attribution date is the Benguria-Loss arXiv paper (Feb 2004) | SS+PVL | EXACT
MOVE-2  | NONE
NOTES   | I recall (RC, unverified) a family of ovals with lambda_0 = 1 also attained in the limit, so nothing below 1 is known. Lower-bound chain (Benguria-Loss, Linde, Denzler) is proof side, not reported.

PROBLEM | 21. Schmeisser's conjecture
SIDE    | lower — the smallest valid constant C(n) is lower-bounded by an example polynomial
RECORD  | YES: C(n) >= 1 (matches the conjecture) via f = z^n - 1, weights on one zero [PVL]
MOVE-1  | UNKNOWN date | UNKNOWN | 1 | ANALYTIC | f = z^n - 1 has the single critical point 0 and zeros on the unit circle; put all weight on one zero: distance is 1 (checked locally for n=3,5) | PVL | EXACT
MOVE-2  | NONE
NOTES   | Who first noted the example (Schmeisser 1971 posed it) not established. Search summary: Schmeisser proved special cases; no counterexample found; conjecture open pre-2025 [SS]. The conjecture's difficulty is on the proof side.

PROBLEM | 23. Smale's problem
SIDE    | lower — the least valid C(n) is lower-bounded by an example polynomial
RECORD  | YES: C(n) >= (n-1)/n (attained by an explicit polynomial); conjectured equal [SS]
MOVE-1  | 1981 | Smale | (n-1)/n | ANALYTIC | summary: Smale noted (d-1)/d "would be the best possible bound as it is attained" (explicit example; year RC) | SS+RC | EXACT
MOVE-2  | NONE
NOTES   | Upper side: Smale 4, Beardon-Minda-Ng 4(n-2)/(n-1) and later 4 - O(1/sqrt n) (proof side, not reported). The 1/d example belongs to a dual conjecture.

PROBLEM | 25. Crouzeix's conjecture
SIDE    | lower — a matrix and polynomial give a lower bound on C
RECORD  | YES: C >= 2, attained (2x2 nilpotent Jordan block, p(z)=z: ||A||=1, W(A)=disc of radius 1/2) [RC + hand check]
MOVE-1  | UNKNOWN date (posed by Crouzeix c. 2004, RC) | Crouzeix | 2 | ANALYTIC | explicit 2x2 example, checked by hand | RC | EXACT
MOVE-2  | NONE
NOTES   | Upper side 1+sqrt2 (Crouzeix-Palencia 2017) is proof side [SS]. Summary: conjectured sharp constant is 2.

PROBLEM | 27. The Prime Number Theorem
SIDE    | other — no construction side: asymptotic identity resolved by proof
RECORD  | NO-RECORD: C^- = C^+ = 1 (Hadamard, de la Vallee Poussin 1896) [RC]; bounds before that (Chebyshev) are proof-side, not constructions
MOVE-1  | NONE
MOVE-2  | NONE
NOTES   | No search performed; RECALL only.

PROBLEM | 29. Block stacking problem
SIDE    | lower — a stack lower-bounds the supremum C(n)
RECORD  | YES: C(n) = H_n/2 exactly (H_n = harmonic number) under the stated constraints [PVL]
MOVE-1  | UNKNOWN | UNKNOWN | H_n/2 | ANALYTIC | equality case of the constraints gives x_{i+1}-x_i = 1/(2(n-i)), so x_n = H_n/2; LP maximisation of x_n for n=1,2,3,5,8 returned exactly H_n/2 | PVL | EXACT
MOVE-2  | NONE
NOTES   | Who first published the harmonic stack and when: not established.

PROBLEM | 31. Furstenberg-Sarkozy problem
SIDE    | lower — a large set with no k-th power differences lower-bounds C(k,N)
RECORD  | YES (k=2, smallest): C(2,N) >= N^0.7334117 (exponent), Beigel-Gasarch and independently Lewko [SS]
MOVE-1  | ~2015 (Lewko, Electron. J. Combin. 22 (2015), RC; Beigel-Gasarch date not established) | Lewko; Beigel, Gasarch | exponent 0.7334117 | UNKNOWN | summary: improved via "computer search" within Ruzsa's framework; whether NEW or REPEAT relative to the earlier of the two is undecidable from the sources | SS | EXACT (exponent from a finite set); REFEREED (Lewko, RC)
MOVE-2  | 1984 | Ruzsa | 0.733077... = (1+ln7/ln65)/2 | ANALYTIC | summary: 7 residues mod 65 with no distinct pair differing by a square, iterated; exponent arithmetic checked locally = 0.73308 | SS+PVL | EXACT; REFEREED
NOTES   | Bounds beyond exponent 3/4 appear only in 2026 results: not used. Modulus-Z/M variant and k>=3 not covered.

PROBLEM | 33. The Thomson problem
SIDE    | upper — a configuration gives an upper bound on the infimal energy
RECORD  | YES (N=2, smallest, per rule): C(2) = 1/2, antipodal points, exact [PVL by hand]
MOVE-1  | UNKNOWN | UNKNOWN | 0.5 | ANALYTIC | two antipodal points: energy 1/2 | PVL | EXACT
MOVE-2  | NONE
NOTES   | Family: exact known for N = 1,2,3,4,5,6,12; N=4,6 Yudin, N=5 Schwartz (computer-assisted), N=12 Cohn-Kumar [SS]. Putative minima for larger N from basin-hopping (Wales et al., up to N about 4352) are NUMERICAL tables [SS]; smallest N without a proof is 7. Ground-state type: not asked to label here.

PROBLEM | 35. Packing in a dilate
SIDE    | upper — a packing gives an upper bound on the smallest scale C(n,P)
RECORD  | YES (chosen P = unit square, n=5, first non-trivial case; statement covers every shape): s = 2 + 1/sqrt2 = 2.7071, Goebel 1979 [RC]
MOVE-1  | 1979 | Goebel | 2.7071 | ANALYTIC | RC: explicit tilted-square packing of 5 unit squares | RC | EXACT
MOVE-2  | NONE
NOTES   | Chosen shape/n is my choice; no search made on this problem. Other shapes (hexagons, etc.) not covered.

PROBLEM | 37. Hypergraph Turan number of the tetrahedron
SIDE    | lower — a K4^(3)-free hypergraph gives a lower bound on C
RECORD  | YES: C >= 5/9, Turan's construction, 1941 [RC + PVL]
MOVE-1  | 1941 | Turan | 5/9 = 0.5556 | ANALYTIC | three-part construction (one vertex in each part, or two in part i and one in part i+1): density limit 5/9 by hand; a 12-vertex instance was checked K4-free by brute force (density 0.618 at n=12, finite-size) | PVL+RC | EXACT
MOVE-2  | NONE
NOTES   | Upper side (Razborov flag algebras ~0.5617) is proof-side. Other extremal constructions with the same density (Kostochka, Brown) RC.

PROBLEM | 39. Beat the average game
SIDE    | lower — a distribution mu lower-bounds the supremum C
RECORD  | YES: C >= 0.400695, Bellec-Fritz (arXiv 2412.15179, Dec 2024) [SS]
MOVE-1  | 2024-12 | Bellec, Fritz | 0.400695 | UNKNOWN | summary: paper 'Optimizing over iid distributions and the Beat the Average game'; states 0.400695 <= C <= 0.417 (upper by mixed-integer LP); it says lower bound conjectured exact as a one-parameter supremum; how the lower-bound distribution was found not stated | SS | UNKNOWN; PREPRINT
MOVE-2  | NOT FOUND
NOTES   | The 0.400695 figure came from a snippet of a later 2025 survey citing this paper; I cannot be sure the Dec 2024 version (v1) already stated it. Earlier value NOT FOUND.

PROBLEM | 41. Points on sphere maximizing the volume
SIDE    | lower — a polyhedron gives a lower bound on the maximum volume C(n)
RECORD  | YES (n=4, smallest): regular tetrahedron, 8*sqrt3/27 = 0.5132 [PVL by hand]; solved n<=8 (Berman-Hanes 1970) and n=12 (icosahedron, Fejes Toth) [SS]
MOVE-1  | 1970 | Berman, Hanes | exact for n <= 8 (n=4: 0.5132) | ANALYTIC | summary: 'determined the maximum volume polyhedra with n <= 8 vertices' (proof) | SS | EXACT; REFEREED-UNKNOWN
MOVE-2  | NONE
NOTES   | n=9 resolution appears only in a 2026 paper: not used. n=10, 11 and n>=13 pre-2025 numeric records not found here.

PROBLEM | 43. Sum-difference problem II
SIDE    | lower — a set A with |A-A| large vs |A+A| lower-bounds C
RECORD  | YES: C >= 1.14465, Gyarmati-Hennecart-Ruzsa, 2007 [SS]
MOVE-1  | 2007 | Gyarmati, Hennecart, Ruzsa | 1.14465 (1.144655) | ANALYTIC | summary: construction from a combinatorial set V(m,L) in N^m with an injective map f on V+V and V-V, image U = f(V); Functiones et Approximatio 37 (2007) 175-186 | SS | RIGOROUS-NUMERIC (exponent evaluated from the construction; certification not seen); REFEREED
MOVE-2  | NOT FOUND
NOTES   | Snippets mention a Hennecart-Robert-Yudin (1999) simplex construction reaching about 1.58 for a related (different-direction) quantity; not this bar. Upper bound side 4/3 is proof-side (RC). Post-2025 improvements exist in results seen; not used.

PROBLEM | 45. Sum-product problems
SIDE    | upper — exhibiting A gives an upper bound on C(R,N)
RECORD  | YES (R = Z, chosen since statement emphasises none): max(|A+A|,|A.A|) <= N^2 exp(-c log N / log log N), Erdos-Szemeredi [SS]
MOVE-1  | 1983 | Erdos, Szemeredi | N^2 exp(-c log N/loglog N), c unspecified | ANALYTIC | summary: 'a family of examples' of integer sets with both sum and product sets small (explicit construction, no constant) | SS | EXACT (asymptotic, unspecified constant); REFEREED-UNKNOWN
MOVE-2  | NOT FOUND (A = {1..N} gives about N^2/(log N)^0.086 by Erdos multiplication table / Ford, RC)
NOTES   | Other rings (finite fields, reals) not covered; a 2026 result on reals appeared in searches: not used.

PROBLEM | 47. Matrix multiplications and AM-GM inequalities
SIDE    | upper — C <= 1 trivially (equal matrices); a counterexample would give C < 1
RECORD  | YES: Recht-Re conjecture (C = 1) is false for some parameters; holds for m = 2, 3 [SS]; numeric value of the ratio not found
MOVE-1  | 2020 | Lai, Lim | C < 1 (counterexample from n = 5; ratio value not found) | SEARCH-NEW | summary: 'noncommutative Positivstellensatz reduces to a semidefinite program that shows the conjecture is false as soon as n = 5' (ICML 2020, PMLR 119; arXiv 2006.01510) | SS | UNKNOWN precision; REFEREED (conference)
MOVE-2  | NONE (C=1 trivial bound from equal matrices)
NOTES   | Whether the counterexample was found by SDP search or hand-refined not confirmed; label SEARCH-NEW rests on the summary wording. Zhang (2018) extended: holds for m=2,3 any n [SS]. Parameters (n,m,d) for the counterexample not found.

PROBLEM | 49. Heilbronn problem in an arbitrary convex bounding box
SIDE    | lower — a point configuration gives a lower bound on C(n)
RECORD  | CANNOT EVALUATE: searches returned unit-square/triangle Heilbronn results (n=7 0.0838591 Zeng-Chen 2008; n=8 0.0723764, Dehbi-Zeng 2022 [SS]) which are a different normalisation; nothing found for the convex-hull-area version before 2025
MOVE-1  | CANNOT EVALUATE
MOVE-2  | CANNOT EVALUATE
NOTES   | I did not find the source for hull-area normalisation. No values recalled with confidence.

PROBLEM | 51. Erdos-Gyarfas conjecture
SIDE    | other — a counterexample (graph with min degree 3 and no 2^k cycle) would be the construction; none known
RECORD  | NO-RECORD: open decision question; no counterexample or numeric quantity before 2025 [RC]
MOVE-1  | NONE
MOVE-2  | NONE
NOTES   | No search performed.

PROBLEM | 53. Equidistant points in convex polygons
SIDE    | other — a counterexample polygon (every vertex with 4 equidistant others) would be the construction; none known
RECORD  | NO-RECORD: for 4 equidistant vertices the question is open; for 3 it was answered by counterexamples (Danzer 9 points; Fishburn-Reeds 20 points with a common radius), and Danzer showed any k fails for varying radius per summary [SS]
MOVE-1  | NONE
MOVE-2  | NONE
NOTES   | Summary claims Danzer proved for any k a convex polygon exists where every vertex has k equidistant vertices; this conflicts with the problem being open for k=4 unless the equidistance is per-vertex radius counted differently or the summary is wrong. I did not resolve this: possible contradiction with 'open' status; treat with caution.

PROBLEM | 55. Erdos squares in a square problem
SIDE    | lower — a packing gives a lower bound on C(n)
RECORD  | YES (family): f(k^2+2c+1) >= k + c/k for |c| < k [SS]
MOVE-1  | 1995 | Erdos, Soifer (independently Campbell, Staton) | k + c/k | ANALYTIC | summary: 'established the lower bound f(k^2+2c+1) >= k + c/k' by explicit packings (dates RC: Geombinatorics 1995; Amer. Math. Monthly 2005 for Campbell-Staton) | SS+RC | EXACT; REFEREED
MOVE-2  | UNKNOWN date | Halasz | k + c/k (same form; summary garbled on whether weaker) | ANALYTIC | summary: 'Halasz came up with a construction' for these bounds | SS | EXACT
NOTES   | Campbell-Staton repeated the bound independently, so not a new move. Erdos conjecture f(k^2+1)=k open; Praton showed the generalised conjecture equivalent.

PROBLEM | 57. Rudin problem for polynomials
SIDE    | lower — a harmonic u lower-bounds the maximum ratio C^p(d,D)
RECORD  | YES (p = infinity only): C^inf(d,D) = sqrt(dim of degree-D harmonics) exactly, zonal harmonic attains it (reproducing-kernel argument) [RC]; p=4: no pre-2025 numeric record found
MOVE-1  | UNKNOWN | UNKNOWN | sqrt(dim H_D(S^d)) | ANALYTIC | RC: zonal harmonic saturates Cauchy-Schwarz at the pole | RC | EXACT
MOVE-2  | NONE
NOTES   | Searches gave only order-of-growth results (Sogge sharp L^p; Bourgain Rudin-Shapiro on S^3). Real-valued and normalisation subtleties not checked.

PROBLEM | 59. Subsets of the grid with no isosceles triangles
SIDE    | lower — a subset lower-bounds C(n)
RECORD  | YES: at n = 64, 108 points, PatternBoost (Nov 2024) [SS]
MOVE-1  | 2024-11 | Charton, Ellenberg, Wagner, Williamson | 108 points in [64]^2 | SEARCH-NEW +AI-SEARCH | summary: PatternBoost 'found a solution with 108 points in [64]^2 without an isosceles triangle' (transformer + local search; arXiv 2411.00566) | SS | EXACT (explicit set); PREPRINT
MOVE-2  | NOT FOUND (prior n=64 value not established)
NOTES   | Deviation: I chose n=64 rather than the smallest n because that is the only n with a move history found; small n (n<=14) optimal values are known from computation (28 points at n=14) [SS]. A 110-point result is 2025: not used. Asymptotic sublinear lower bound (Charton-Ellenberg-Wagner-Williamson) also seen.

PROBLEM | 61. The Ring Loading Problem
SIDE    | lower — an instance forces alpha above a value
RECORD  | YES: alpha >= 11/10, Skutella (arXiv 1405.0789), improving 101/100 [SS]
MOVE-1  | 2014 (arXiv; journal 2016 RC) | Skutella | 11/10 | UNKNOWN | summary: 'presents an improved lower bound of (11/10)D (previously (101/100)D)' and disproves a conjecture of Schrijver et al.; how the instance was found not stated | SS | EXACT (instance value); REFEREED-UNKNOWN
MOVE-2  | UNKNOWN date/authors | UNKNOWN | 101/100 | UNKNOWN | only as 'previous bound' in Skutella's abstract | SS | UNKNOWN
NOTES   | Upper side: Schrijver-Seymour-Winkler 3/2, Skutella 19/14, Daubel 1.3 (arXiv 1904.02119) are proof-side. My recall of 11/8 was wrong; source says 11/10.

PROBLEM | 63. The ambidextrous moving sofa problem
SIDE    | lower — a shape lower-bounds the largest area
RECORD  | YES: area 1.64495521..., Romik's ambidextrous sofa [SS]
MOVE-1  | 2016 (arXiv 1606.08111) | Romik | 1.64495521 = x + arctan y, x^2(x+3)=8, y(4y^2+3)=1 | ANALYTIC | summary: shape with 18 boundary curves (circle arcs and sextics) derived via differential equations, exact area formula (Exp. Math. 2018 RC) | SS | EXACT
MOVE-2  | 2014 | Gibbs | about 1.64495 | SEARCH-NEW | summary: 'developed another numerical technique ... computed a similar-looking shape (higher resolution), area about 1.64495' | SS | NUMERICAL
NOTES   | Chronology of Gibbs vs Romik's shape for the ambidextrous variant not fully clear from the summary (Gibbs numerics may follow other work). Upper bound 2.37 (from Kallus-Romik) is proof-side.

PROBLEM | 65. Variant of IMO 2025, Problem 6
SIDE    | upper — a tiling exhibits an upper bound on C(n)
RECORD  | NO-RECORD: problem is from IMO 2025 (July 2025), after the cutoff; no pre-2025 value [RC]
MOVE-1  | NONE
MOVE-2  | NONE
NOTES   | No search performed.

PROBLEM | 67. Logic puzzles
SIDE    | other — finite puzzle with a definite optimum, no bound history
RECORD  | NO-RECORD: single puzzle; no construction-side record history
MOVE-1  | NONE
MOVE-2  | NONE
NOTES   | Question statement leaves open whom questions may be addressed to; not computed.
