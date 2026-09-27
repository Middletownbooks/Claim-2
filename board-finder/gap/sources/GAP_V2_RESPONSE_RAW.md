<!-- Verbatim response to PROMPT_GAP_v2.md, run 20 Sep 2026, pasted by the user.
     Recovered from the session transcript on 21 Sep 2026: RESULT_GAP_v2.md cited this
     path from the start but the file had never actually been written to the repo.
     Only the surrounding `Document: "` wrapper was stripped. -->

# Finite-Witness Triage

**Date of search: 20 September 2026.** All status claims below were checked against a dated
source during this session. Anything I could not check is in the unverified pool, unscored.

---

## 0. The headline finding, before the table

The single most important thing this session turned up is not a candidate. It is that **the
category "open problem settled by one explicit finite object" has been industrialised into at
least four agent-facing problem databases since late 2025**, and the obvious candidates are
already on them:

| Database | Nature | Evidence found this session |
|---|---|---|
| **Epoch AI, FrontierMath: Open Problems** | 50 curated problems, verifier-gated, sold to labs | Type filter literally reads *Construction – Finite (32), Counterexample (12), Record Breaking (11)*. 41 unsolved, 8 solved (4 by AI, 4 human+AI) |
| **TheoremDB** | Per-problem pages with prior-work digests | Hadamard-668 page carries the line "Point a connected agent at this problem" |
| **Horizon / HorizonMath** (reachthehorizon.com) | Agent problem set with attack hints | Hadamard-668 page lists specific SDF/Goethals–Seidel attack strategies and which have been "thoroughly evaluated and rejected" |
| **erdosproblems.com** | ~1,100 Erdős problems, community wiki | Cited in an April 2026 survey as the main AI4Math testbed, with a cumulative-AI-contribution chart |

Epoch's own submission criteria are, almost word for word, the criteria in this commission:
<cite index="13-1">problems must be "Verifiable: solutions can be verified to a high degree of confidence by a typical computer program (not Lean) running on a typical laptop in under an hour"</cite>, and <cite index="13-1">"Good problems often involve asking for constructions or algorithms"</cite>.
Whatever selection function this triage runs, Epoch ran a version of it first and published the
answer.

Two consequences, both acted on below:

1. **Conway's 99-graph and the missing Moore graph are excluded, not ranked.** A naive triage
   puts them at #1 and #2 — both are single finite graphs, exactly checkable, with a unit-size
   unknown set. Both are on FrontierMath: Open Problems, and Conway-99 already has an
   autonomous-agent attack paper on arXiv (2608.11211, July 2026).
2. **Hadamard matrices are dead below order 2000.** See §1.1.

### 1.1 The correction that matters most

I began this session believing 668 was the smallest open Hadamard order. It is not, and neither
is the next one, or the next eleven.

<cite index="87-1">Epoch AI reported in 2026 that L. Alpöge, P. Voinov, and S. Reynolds-Haertle announced constructions obtained with Claude for the twelve previously unresolved orders below 2000: 668, 716, 892, 1132, 1244, 1388, 1436, 1676, 1772, 1916, 1948, and 1964</cite> — so <cite index="87-1">"constructions are now available for every positive order below 2000 divisible by 4"</cite>
(MathWorld, *Hadamard Matrix*, retrieved 20 Sep 2026; Epoch changelog entry dated 2026-08-12).

This is directly relevant to the existing `/areas/hadamard-constructions.md` thread. The
reverse-engineering target there — *"open orders above 668"* — is now the wrong frame. There are
no open orders below 2000. The live question is the smallest open multiple of 4 **above** 2000,
which I could not pin down this session and which sits in the unverified pool as item U2.

---

## 1. Ranked table — verified candidates only

Six candidates survived status verification. Scores are 1–5 per dimension, 40 max.

| # | Problem | Field | Polarity | A | B | C | D | E | F | G | H | Total | Status | One-line rationale |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **Triple of MOLS of order 10** | Design theory | CONSTRUCTION | 5 | 5 | 5 | 5 | 4 | 4 | 5 | 5 | **38** | OPEN-SWEPT-IN-RANGE | Unknown set is a single named instance; witness is 300 integers; but the standard reduction (prescribed symmetry) is *provably* unavailable |
| 2 | **Ideal PTE solution of size 11** | Number theory | CONSTRUCTION | 5 | 5 | 5 | 4 | 5 | 4 | 5 | 5 | **38** | OPEN-SWEPT-IN-RANGE (symmetric ansatz only) | A hole below a settled ceiling — size 12 is done, 11 is not — with no known local obstruction and a publishable null |
| 3 | **Costas array of order 32 (or 33)** | Combinatorics / signal design | CONSTRUCTION | 5 | 5 | 5 | 5 | 4 | 4 | 4 | 5 | **37** | OPEN-SWEPT-IN-RANGE (structured subspaces) | Named finite gap list; witness is a permutation of 32 symbols; the algebraic constructions fail at exactly these two parameters for a reason you can name |
| 4 | **Rank-≤22 decomposition of the 3×3 matmul tensor** | Algebraic complexity | CONSTRUCTION | 5 | 5 | 5 | 5 | 3 | 4 | 5 | 5 | **37** | OPEN-SWEPT-IN-RANGE (ternary alphabets, small fields) | Perfect on every scored dimension and **heavily contested** — multiple AI-agent teams are running this search right now |
| 5 | **APN permutation of F₂⁸ ("Big APN Problem")** | Cryptography | CONSTRUCTION | 5 | 5 | 5 | 3 | 2 | 3 | 5 | 5 | **31** | OPEN-SWEPT-IN-RANGE | The only route that ever produced one was swept at scale in 2025 with a null result |
| 6 | **Four MUBs in C⁶ (refuting Zauner's MUB conjecture)** | Quantum information | REFUTATION | 5 | 3 | 4 | 5 | 3 | 4 | 3 | 3 | **30** | OPEN-SWEPT-IN-RANGE | Demoted by its own falsification line: the object probably is not there |

**Where I would actually spend the first week, which differs from the ranking.** Rank order is
dominated by D, as commissioned. But #2 (PTE size 11) is the better first target, because it is
the only one of the six where **E = 5**: extending a height bound and finding nothing is itself a
paper, and there is a 2023 paper that is exactly that. #1 and #3 have higher D but their null
results are only publishable if you can certify what you covered, which is harder. #4 is
technically excellent and strategically bad — see its dossier.

---

## 2. Unverified pool — unscored, not ranked

Each item names the one search that would promote it to scoreable. I did not score these because
I did not confirm their status against a dated source this session.

| ID | Candidate | Polarity | The promoting search |
|---|---|---|---|
| U1 | Skew-Hadamard matrix at the smallest open order | CONSTRUCTION | Đoković closed 276 and 292 (arXiv 2301.02751, v3 Nov 2024); a Sage tracker citing him says the first unresolved case is 356. **Fetch Colbourn–Dinitz *Handbook* Table 1.51 or Seberry's current table and confirm the smallest *v* with no known skew-Hadamard of order 4*v* as of 2026.** |
| U2 | Smallest open Hadamard order above 2000 | CONSTRUCTION | Does the Alpöge–Voinov–Reynolds-Haertle release extend above 2000? Fetch the decoder output listing and the current Hadamard existence table above 2000. |
| U3 | Williamson matrices of order 4*n*, smallest *n* with none known | CONSTRUCTION | Current Williamson / good-matrix existence table (Awyzio–Seberry lists *w* up to 35 and 127 via Đoković); confirm the smallest open *w*. |
| U4 | Perfect 1-factorisation of K₂ₙ, smallest open 2*n* | CONSTRUCTION | Current P1F existence table; the conjecture is proven for 2*n* = *p*+1 and 2*p*, so the open set is the non-covered even orders — confirm the smallest. |
| U5 | Symmetric Hadamard / propus arrays at open orders | CONSTRUCTION | Đoković's symmetric-372 result (2024) implies a live table; fetch it. |
| U6 | *x*³+*y*³+*z*³ = 114 | CONSTRUCTION | Has 114 fallen since Booker–Sutherland? Almost certainly OPEN-BEYOND-REACH given the 10¹⁵–10¹⁶ sweep, but confirm. |
| U7 | Lonely runner counterexample at *n* = 8 | REFUTATION | Is *n* = 8 still open, and is there a bound that makes the witness space finite and enumerable? |
| U8 | Kissing-number lower-bound records, dimensions 11–14 | CONSTRUCTION | Current records post-Ganzhinov (2023); check whether the unknown set is a named list or a tail. |
| U9 | Snake-in-the-box lower bounds, dimensions 9–11 | CONSTRUCTION | Current record table; note that *optimality* is non-existence and therefore excluded — only lower-bound records qualify. |
| U10 | Largest cap in AG(7,3) / AG(8,3) | CONSTRUCTION | Post-FunSearch records; same caveat as U9 about optimality. |
| U11 | Seymour's second-neighbourhood counterexample | REFUTATION | Smallest *n* to which the conjecture has been verified, and whether a counterexample digraph is checkable in one direction. |
| U12 | Caccetta–Häggkvist counterexample for *r* ≥ 4 | REFUTATION | Current verified range; the *r* = 1,2,3 cases are theorems. |
| U13 | D-optimal designs of order 2*v* at open *v* | CONSTRUCTION | Current D-optimal existence table (Fletcher–Koukouvinos–Seberry lineage). |
| U14 | AME states / quantum orthogonal Latin squares at open parameters | CONSTRUCTION | Post-AME(4,6) (2022) parameter table; check which parameters remain. |
| U15 | Bent and vectorial bent functions at open parameters | CONSTRUCTION | Current existence tables; high risk of sitting on a public coding-theory table. |
| U16 | Exact SIC-POVM fiducial in an open dimension | CONSTRUCTION | **Overlaps your existing `/areas/sic-povm-fiducials.md` scoping.** Promoting search: current exact-fiducial dimension table (Grassl / Scott–Grassl lineage) as of 2026. |

---

## 3. Dossiers

### 3.1 Triple of mutually orthogonal Latin squares of order 10 — rank 1

**Statement.** Do there exist three 10×10 Latin squares, pairwise orthogonal? Equivalently,
is *N*(10) ≥ 3? It is known that *N*(10) ≥ 2 (Bose–Shrikhande–Parker, 1959) and *N*(10) ≤ 6.

**Polarity.** CONSTRUCTION. The witness is one triple.

**Scores.**
- **A = 5.** One triple settles it outright.
- **B = 5.** Exact and one-directional: check each of three arrays is Latin, then check the three
  pairwise superpositions each give 100 distinct ordered pairs. Integer comparisons only, no
  solver, no floating point.
- **C = 5.** 300 symbols. Fits in a tweet, as order 668 recently demonstrated.
- **D = 5.** The unknown set is *one named instance*. <cite index="32-1">A sequence of results culminating with Todorov established that N(n) ≥ 3 unless n = 2, 3, 6 and possibly n = 10</cite>. Orders 2, 3 and 6 are settled negatively. Order 10 is the entire remaining unknown set.
- **E = 4.** Bounded increments exist and have been published as null results (the relation-restricted
  enumerations below). Not a 5 because the residual space has no natural finite stratification.
- **F = 4.** Prior searches published **with code or data**, so coverage is knowable — and what it
  shows is bad for the easy attacks. See the falsification line.
- **G = 5.** SAT and CP encodings for MOLS(10) are published and reusable (2021 ILP/CP paper,
  2025 SAT enumerations); nauty handles the isomorphism side.
- **H = 5.** A referee checks 300 integers in seconds. Uncontroversial.

**Premise-falsification line, and its result.** *If a 3-MOLS(10) existed with any nontrivial
symmetry, the prescribed-automorphism search — the single most productive technique in design
construction, and the one that produced Hadamard 668 — would have found it. So check whether
prescribed symmetry is viable here.*

**Result: it is not, and this is the whole diagnosis of resistance.** McKay, Meynert and Myrvold
proved <cite index="36-1">that no square of order 10 with non-trivial autoparatopism group is part of an orthogonal triple</cite>, and the same source notes that this also rules out transitive
triples, since a transitive triple can be converted into one where some square has nontrivial
autoparatopisms. Any witness therefore has **trivial symmetry**, and the standard reduction is
unavailable by theorem, not by bad luck. That is why the problem resists: the search cannot be
compressed by the usual factor.

The candidate survives, because a second published constraint *does* compress it, in a different
direction — see the attack sketch.

**Near-miss evidence.** Parker found a 10×10 Latin square with 5504 transversals and roughly a
million orthogonal mates that <cite index="33-1">is not a member of any triad of mutually orthogonal 10×10 latin squares</cite>. Relation-restricted enumerations are complete: Delisle
enumerated all 4-nets(10) with at least two nontrivial relations, Myrvold independently verified
it, and a 2025 SAT re-run confirmed both with independently checkable certificates. Gill and
Wanless enumerated all 4-nets(10) with at least one nontrivial relation — 18,526,229 up to
isomorphism.

**Attack sketch.** The Gill–Wanless enumeration yields the sharpest usable filter: it is now
known that the incidence matrix of any pair of squares in a 3-MOLS(10) must have only trivial
linear dependencies, so **the rank of the linear code generated by any pair must be exactly 37**.
That is a cheap, exact test on candidate pairs, and it prunes before any third square is
attempted. The attack is therefore: enumerate or sample orthogonal pairs, filter to rank exactly
37, then run a completion search for the third square under a SAT encoding. Space size: the
number of main classes of Latin squares of order 10 is known and large; the pair space is the
binding constraint, not the completion step. **Fits sustained compute, not one session** — but a
*bounded* version (sample the rank-37 pair space, run completions, report coverage) fits one
extended session and produces a legitimate null.

**Verification method.** Three 10×10 integer arrays; check Latin property by row/column set
equality; check orthogonality by hashing the 100 ordered pairs per superposition.

**Status: OPEN-SWEPT-IN-RANGE.** <cite index="37-1">"the existence of such an orthogonal triple remains an open problem"</cite> — arXiv 2503.10504, *Myrvold's Results on Orthogonal Triples of 10×10 Latin Squares: A SAT Investigation*, March 2025,
https://arxiv.org/pdf/2503.10504. The frontier: every symmetry-restricted and
relation-restricted region is exhausted; the trivial-symmetry, trivial-relation region is not.

**Risks.** (a) The object may not exist, and non-existence is the excluded polarity — a failed
search here can never become a proof. (b) The problem is old and famous; a null result needs
certified coverage to be publishable, which means DRAT-style certificates, which means the SAT
route rather than bespoke backtracking. (c) Sits adjacent to the projective-plane-of-order-10
literature, which is heavily trodden.

---

### 3.2 Ideal Prouhet–Tarry–Escott solution of size 11 — rank 2

**Statement.** Find two disjoint multisets of 11 integers each, with identical *k*-th power sums
for *k* = 1,…,10. (*Ideal* means degree = size − 1, the maximal nontrivial case.)

**Polarity.** CONSTRUCTION.

**Scores.**
- **A = 5.** Twenty-two integers settle it.
- **B = 5.** Ten integer identities. Exact, one-directional, instant.
- **C = 5.** Two lists of eleven integers.
- **D = 4, not 5.** <cite index="71-1">"For n = 11 and n ≥13, no ideal solutions are known."</cite> That is a *hole* at 11 below a settled ceiling at 12, plus a tail from 13 up. The
  hole is the target and scores 4; the tail scores 1 and is not the target. I am scoring the hole.
- **E = 5.** Both conditions hold. The region is a height bound, extending it is bounded, and the
  null result is publishable — Coppersmith, Mossinghoff, Scheinerman and VanderKam published
  exactly that paper in 2023: <cite index="75-1">they significantly extended searches for symmetric ideal solutions at sizes 9, 10, 11 and 12 over Z, and conducted extensive first-time searches at larger sizes up to 16</cite>.
- **F = 4.** Prior search published with height bounds and search parameters tabulated (CMSV 2023
  reports the height bound *H* used and the bound *H*₀ reached by predecessors, per *n*). Coverage
  is knowable. Capped at 4 rather than 5 only because the searches cover a restricted ansatz.
- **G = 5.** Integer arithmetic, symmetric-function reductions, lattice methods. Commodity tooling.
- **H = 5.** Anyone can check it by hand in ten minutes.

**Premise-falsification line, and its result.** *Size 12 is solved and size 11 is not, which is
backwards from the usual pattern. If the obstruction at 11 were arithmetic — a congruence or
parity condition — it would be known, and the candidate would be dead. So check whether any local
obstruction at size 11 is known.*

**Result: none is known, and the candidate survives cleanly.** <cite index="71-1">"there is no lower bound on N(k) that would rule out ideal solutions"</cite>, and Wright's conjecture
predicts ideal solutions at every size. The gap at 11 is a *search* gap, not a structural one.

The actual diagnosis of resistance is different and more encouraging: the known ideal solutions
at even sizes come from parametric families and from rational points on elliptic curves, and
those constructions are tied to even size. Odd sizes have always been thin — <cite index="70-1">at n = 9, ideal solutions are known only in the symmetric case, with just two known up to affine equivalence, both found by Letac</cite>, while infinite families exist at the other solved
sizes. Size 11 is odd and therefore inherits the thin case, not a hard one.

**Near-miss evidence.** Borwein, Lisoněk and Percival searched size 11 up to height 2000 and found
nothing. CMSV 2023 extended the symmetric searches substantially and found nothing at 11, while
finding *new* ideal solutions in imaginary quadratic settings — sizes 10 and 12 in the Gaussian
integers, 9 in Z[i√2], and 9 and 12 in the Eisenstein integers. That last datum is the most
interesting one in this dossier: **the object exists over nearby rings at sizes where it is hard
over Z.** Choudhry and Wróblewski separately derived degree-11 solutions from a degree-10 system.

**Attack sketch.** Two distinct lines.
1. *Push the symmetric ansatz.* For odd size, symmetric means *A* = −*A* and *B* = −*B*, which
   collapses the search from 22 free integers to roughly 5 plus a centre. This is what CMSV did;
   extending their height bound is straightforward, bounded, and publishable as a null. **Fits
   one extended session with light tooling.**
2. *Attack the asymmetric region, which nobody has swept.* Symmetry at odd size is an empirical
   regularity, not a theorem. The entire asymmetric space at *n* = 11 is unswept. This is the
   higher-variance line and the one with the better payoff.
   Practical route: use the multiplicity-lemma reduction over F_p to seed candidate
   configurations, then lift. **Needs sustained compute.**

**Verification method.** Ten power-sum equalities over Z with exact integer arithmetic.

**Status: OPEN-SWEPT-IN-RANGE within the symmetric ansatz; OPEN-UNSWEPT outside it.**
Source: arXiv 2304.11254, *Ideal solutions in the Prouhet–Tarry–Escott problem*, Coppersmith,
Mossinghoff, Scheinerman, VanderKam, dated 21 April 2023, https://arxiv.org/abs/2304.11254.
Status corroborated by the June 2025 survey arXiv 2506.11429.

**Risks.** (a) Heights may be enormous — the second known size-10 solution has entries around
10¹², so size 11 could sit far beyond any reachable bound, which would move this to
OPEN-BEYOND-REACH. (b) The symmetric line is well-trodden and the marginal extension is small.
(c) PTE appears in general number-theory problem collections; it is not on FrontierMath: Open
Problems, but it is recognisable enough to be swept.

---

### 3.3 Costas array of order 32 or 33 — rank 3

**Statement.** Does there exist a 32×32 permutation matrix in which all C(32,2) = 496 displacement
vectors between pairs of dots are distinct?

**Polarity.** CONSTRUCTION.

**Scores.**
- **A = 5.** One permutation of 32 symbols settles it.
- **B = 5.** Exact, one-directional: compute 496 vector differences, check distinctness.
- **C = 5.** Thirty-two integers.
- **D = 5.** A named finite list below a known ceiling. Golomb and Taylor listed all known
  constructions for 271 values of *n* up to 360: <cite index="47-1">"The first eight gaps in this table occur at n = 32, 33, 43, 48, 49, 53, 54, 63."</cite> Eight named instances; everything else
  below 360 is constructed.
- **E = 4.** Completing full exhaustive enumeration at *n* = 30 and 31 is a bounded extension with
  a publishable null (the enumeration papers at 26, 27, 28 are exactly this genre). Not 5 because
  the cost grows by roughly a factor of 5 per order.
- **F = 4.** Prior search published **with data**: comprehensive databases by Beard and by Rickard,
  plus a published symmetry-restricted enumeration through order 32.
- **G = 4.** No dominant off-the-shelf tool; bespoke backtracking and FPGA implementations are the
  state of the art, though SAT/CP encodings exist. Capped below 5 for that reason.
- **H = 5.** Trivially checkable.

**Premise-falsification line, and its result.** *Every known Costas array comes from the Golomb or
Welch constructions, which produce orders* p−1, q−2, q−3*, and sometimes* q−4 *and* q−5*, for*
p *prime and* q *a prime power. If the arithmetic admitted one of these at n = 32, the array would
already exist. So run the arithmetic.*

**Result: the arithmetic does not exclude it, and that is the informative outcome.**
33 is not prime, so *p*−1 fails. 34, 35 and 36 are not prime powers, so *q*−2, *q*−3 and *q*−4
fail. But **37 is prime**, so 32 = 37−5 and 33 = 37−4 sit at exactly the parameters where the
sporadic Golomb *q*−4 and *q*−5 variants could apply. They do not — both remain listed as gaps in
the construction table. So the resistance is precisely located: the side conditions on the
sporadic variants fail at *q* = 37. That is a concrete, checkable thing to attack, rather than a
vague "nobody has found one."

**Second falsification result.** A published enumeration covered all Costas arrays through order
32 satisfying three kinds of symmetry, with the stated aim of finding a 32×32 array or gathering
evidence against one. Nothing was found. Any witness at order 32 is therefore **asymmetric** —
the same structural verdict as 3 MOLS(10), reached independently.

**Near-miss evidence.** <cite index="43-1">Rickard's semi-empirical method, the only method since the 1980s to produce previously unknown Costas arrays, found four: two of order 29, one of order 36, and one of order 42</cite>. That it reached 36 and 42 but not 32 or 33 is the sharpest
near-miss available. <cite index="42-1">"All Costas arrays of orders n ≤ 29 have been found through exhaustive search"</cite> — note that sources disagree on the exhaustive frontier (26,
27, 28 and 29 all appear in the literature, in papers of different dates); the 2014 Jedwab–Wodlinger
statement gives 29 and is the most recent I checked.

**Attack sketch.** Target: a 32-element permutation with 496 distinct difference vectors. Space:
32! ≈ 2.6 × 10³⁵ — exhaustive search is out of reach and will remain so. Two viable lines:
1. *Extend the Rickard periodicity method to q = 37.* It is the only method in forty years to
   produce new arrays, and it works by exploiting the periodicity of Golomb/Welch arrays. Order 32
   sits at *q*−5 for *q* = 37, so the method's natural domain includes it. **Fits one extended
   session with light tooling**, and is the highest-value cheap experiment in this entire document.
2. *Constrained stochastic search under the asymmetry constraint.* Lower value; the space is too
   large for local search to be credible.

**Verification method.** Compute the 496 differences; check for duplicates with a hash set.

**Status: OPEN-SWEPT-IN-RANGE for structured and symmetric subspaces; the full space at order 32
is unreachable.** Source: Jedwab and Wodlinger, *The Deficiency of Costas Arrays*, 2014 —
<cite index="41-1">"the smallest values of n for which existence is currently open"</cite>
are 32 and 33; <cite index="41-1">"There is no value of n for which a Costas array of order n is known not to exist"</cite>.
https://www.sfu.ca/~jed/Papers/Jedwab%20Wodlinger.%20Costas%20Deficiency.%202014.pdf. Status
corroborated as still current by a 2026 NSF-hosted survey and the Wikipedia entry, both checked
this session.

**Risks.** (a) My most recent *dated* status source is 2014; the corroborating sources are recent
but less precise about the 32/33 frontier. One targeted check of the Rickard database would fix
this and is cheap. (b) Costas arrays have a dedicated "Open problems in Costas arrays" survey
(Drakakis, arXiv 1102.5727) — that is a domain compendium, which brushes the anti-criterion. It
is not an agent-enumerable numbered tracker, and Costas arrays do not appear on FrontierMath: Open
Problems, TheoremDB or Horizon in anything I found. I am flagging this as a partial hit rather
than clearing it. (c) Existence for all *n* is conjectured but the counts *fall* monotonically
after *n* = 16, which is weak evidence that the gaps are real.

---

### 3.4 Rank-≤22 decomposition of the 3×3 matrix multiplication tensor — rank 4

**Statement.** The 3×3 matrix multiplication tensor has rank at most 23 (Laderman, 1976) and at
least 19 (Bläser). Exhibit a decomposition of rank 20, 21 or 22 — or confirm none exists, which
is the excluded polarity.

**Polarity.** CONSTRUCTION.

**Scores.** A = 5; B = 5 (the 729 Brent equations over Z, exact and one-directional);
C = 5 (three coefficient matrices); **D = 5** (the unknown set is {20, 21, 22} — finite, named,
pinned between two published bounds); E = 3 (a null here is the normal state of the world and is
not publishable alone); F = 4 (flip-graph code and SAT encodings are public, so coverage over
small fields and ternary alphabets is knowable); G = 5; H = 5. **Total 37.**

**Premise-falsification line, and its result.** *Strassen's rank-7 2×2 scheme, Laderman's rank-23,
and essentially every record for small formats have ternary coefficients in {−1, 0, 1}. If rank
22 were attainable with ternary coefficients, the flip-graph and SAT sweeps — which search exactly
that alphabet — would plausibly have hit it.*

**Result: they have not, across multiple fields and several independent research groups.** The
implication is that a rank-22 witness, if it exists, likely needs a coefficient alphabet outside
{−1, 0, 1} — which is precisely the region no existing tool searches well. The candidate survives,
but the attack is redirected away from every published pipeline.

**Why this is ranked 4th despite scoring 37.** It is the most contested target in this document.
The additive-complexity race at rank 23 has run 60 → 59 → 58 → 56 → 55 → 52 additions in roughly
thirteen months, entirely driven by AI-agent pipelines, and at least one of those teams was
aiming at rank 22 along the way: <cite index="64-1">"The original objective was to search for an exact rank-22 decomposition"</cite> of the 3×3 tensor (arXiv 2607.28676, dated 6
September 2026 — fourteen days before this triage). This is not on a numbered problem list, so it
passes the letter of the anti-criterion, but it fails its spirit completely. You would be entering
a crowded race late, against teams with more compute.

**Attack sketch.** Search rank-22 decompositions over coefficient alphabets strictly larger than
ternary — small rationals, or roots of unity — using numerical ALS followed by rationalisation,
with the 729 Brent equations as the exact gate. **Needs sustained compute**, and the crowding
means the expected value is low even so.

**Status: OPEN-SWEPT-IN-RANGE** over ternary alphabets and small finite fields; OPEN-UNSWEPT over
general characteristic zero with larger alphabets.

**Risks.** Crowding, principally. Also: rank 23 has stood since 1976, which is 50 years of
resistance; the lower bound of 19 has not moved either. Both facts suggest the true rank may
simply be 23, in which case the polarity is unwinnable.

---

### 3.5 APN permutation of F₂⁸ — rank 5

**Statement.** Does an almost perfect nonlinear permutation exist on an even number of bits
greater than 6? The first open case is 8 bits.

**Polarity.** CONSTRUCTION. Witness: a permutation of 256 values with differential uniformity 2.

**Scores.** A = 5; B = 5 (65,536 XOR-and-count operations, exact); C = 5 (256 bytes);
**D = 3** (the unknown set is all even *n* ≥ 8 — a tail with a named first element, not a list);
**E = 2** (no bounded region whose extension yields a publishable null — the one paper of that
genre has already been written); **F = 3** (prior search published with data, and what the data
shows is that the productive region is exhausted); G = 5; H = 5. **Total 31.**

**Premise-falsification line, and its result.** *The only known APN permutation in even dimension
— Dillon et al.'s 6-bit example, 2009 — was found as a CCZ-equivalent representation of a
quadratic APN function. If the 8-bit witness is of the same kind, a large sweep of quadratic APN
functions in 8 variables should find it.*

**Result: this largely kills the candidate.** A 2025 paper generated more than 3.5 million
inequivalent quadratic APN functions in eight variables — far more than previously possible and
more than had been predicted to exist — and <cite index="50-1">"none of these is CCZ-equivalent to an APN permutation"</cite> (arXiv 2508.04644). Independently, the other
structural route is closed: the butterfly structure that contains Dillon's permutation has been
shown not to be APN for generalised Gold exponents when *n* > 3.

Both known routes are dead. What remains is the unstructured space of 256! permutations with no
guiding construction — which is not a target, it is a wilderness.

**Status: OPEN-SWEPT-IN-RANGE.** The cheap win is gone. Source: arXiv 2508.04644, August 2025.
Problem confirmed open and important as of 2023 in Springer's *Cryptography and Communications*:
<cite index="57-1">the existence of APN permutations over F₂ⁿ with even n "is one of the oldest and most important questions in the field of cryptographic Boolean functions"</cite>.

**Retained anyway, at rank 5, for one reason.** The verification is so cheap and the object so
small that it is a near-zero-cost passenger on any other search infrastructure. It is not worth a
dedicated programme.

---

### 3.6 Four mutually unbiased bases in C⁶ — rank 6

**Statement.** Zauner conjectured the maximum number of pairwise MUBs in dimension 6 is 3. A
fourth basis refutes it.

**Polarity.** REFUTATION.

**Scores.** A = 5; **B = 3** (a numerical near-MUB is not a witness; an exact algebraic one would
be, but no realistic search produces exact entries — this is the floating-point cap, applied
hard); C = 4 (four 6×6 matrices, but entries may be high-degree algebraic numbers);
**D = 5** (one named instance, *d* = 6); E = 3; F = 4; G = 3 (Gröbner bases blow up; SMT does not
scale past *d* = 4); H = 3. **Total 30.**

**Premise-falsification line, and its result.** *If a 4-MUB set in C⁶ existed with algebraic
entries of complexity comparable to the known 3-MUB families, it would reduce modulo a prime to a
"shadow" over a finite field. Check whether any such shadow exists.*

**Result: demote hard.** McConnell, Spencer and Tahir found that <cite index="79-1">if a counter-example to Zauner's conjecture were to exist, it would leave no such shadow upon reduction modulo several different primes, forcing its algebraic complexity level to be much higher than that of current well-known examples</cite>. Independently, three numerical
methods — see-saw optimisation, non-linear SDP and Monte Carlo — all converge on the same
sub-maximal optimum, and a separate distance-based study found a maximum average squared distance
of 0.9983, strictly below the 1.0 that four MUBs would require.

The weight of evidence is that the object is not there. Under the commission's rules, a witness
that probably does not exist is not a target, and the only remaining resolution route is
non-existence, which is the excluded polarity.

**One counter-datum, worth recording.** In April 2025, McNulty and Weigert showed that a lemma of
Chen et al. constraining the structure of any complex Hadamard matrix in a 4-MUB set has an
erroneous proof, <cite index="80-1">"ultimately invalidating three theorems derived in later publications"</cite>. Part of the structural *exclusion* literature is therefore retracted.
This does not make the object more likely to exist — it makes the case against it slightly less
complete than published summaries suggest.

**Status: OPEN-SWEPT-IN-RANGE numerically.** Source: Quantum 8, 1318 (30 April 2024) —
<cite index="83-1">"it is not known whether there exist more than 3 such bases"</cite>,
https://quantum-journal.org/papers/q-2024-04-30-1318/pdf/.

**Risks.** Also sits on a curated list: the conjecture was <cite index="83-1">"highlighted as one of five important open problems in quantum information theory"</cite>. Partial
anti-criterion hit.

---

## 4. Precedent discipline

Four precedents are commonly cited in this space. Three of them point the opposite way from how
they are usually deployed.

| Precedent | Implication direction | Effect on the target |
|---|---|---|
| **Euler's MOLS conjecture refuted (Bose–Shrikhande–Parker, 1959)** — 2 MOLS(10) constructed | "No 3 MOLS(10)" ⟹ nothing about Euler; but 3 MOLS(10) ⟹ 2 MOLS(10). The 1959 target is the **weaker, easier** one. | Makes 3 MOLS(10) look **easier than it is**. The sibling that fell is the one below it, not above it. Do not read 1959 as evidence that 1959's methods reach three squares — they were tried and did not. |
| **Hadamard order 668 constructed (Aug 2026)** | Skew-Hadamard of order *n* ⟹ Hadamard of order *n*. Skew is the **stronger** object. | Makes U1 (skew-Hadamard at the open frontier) **harder** than the 668 precedent suggests, not easier. The 668 techniques do not transfer for free. |
| **Kaplansky unit conjecture refuted (Gardam, 2021)** | Unit conjecture ⟹ zero-divisor conjecture ⟹ idempotent conjecture. Gardam refuted the **strongest**, which is the easiest to refute. The weaker siblings remain open. | Weak evidence for anything. Refuting the strongest member of a chain is the standard, easiest outcome. |
| **Bunkbed conjecture refuted by explicit counterexample (2024)** | The bunkbed conjecture is a strong universal statement; refuting it is the easier direction. | Weak evidence for "plausible combinatorial conjectures fall to explicit counterexamples." The counterexample was also enormous, which is the relevant warning for every REFUTATION candidate here. |

The general rule this table encodes: **refuting a stronger sibling is the easier task, so a
fallen-stronger-sibling precedent is weaker evidence than it looks.** Every precedent above is of
that form. None of them is a fallen *weaker* sibling, which is the form that would actually be
encouraging.

---

## 5. Exclusion list

| Excluded candidate | Anti-criterion failed | Note |
|---|---|---|
| **Conway's 99-graph, srg(99,14,1,2)** | On an enumerable public problem list | FrontierMath: Open Problems, with a $1,000 Conway prize attached. Already has an autonomous-agent attack paper (arXiv 2608.11211, July 2026). Would otherwise rank #1: D = 5 (the only unknown parameter sets with λ=1, μ=2 are 99, 6273 and 494019), B = 5, C = 5. |
| **Missing Moore graph, 57-regular on 3250 vertices** | On an enumerable public problem list | FrontierMath: Open Problems. A 2026 paper ("No involutions in the missing Moore graph") shows active structural work. Would otherwise score very highly. |
| **Hadamard matrix of order 668, and all orders < 2000** | **Solved** | Closed 2026-08-12. See §1.1. |
| **Perfect cuboid** | (i) unbounded tail, D = 1; (ii) on public lists | Open Problem Garden and unsolvedproblems.org. Frontier: no perfect cuboid with odd side below 2.5 × 10¹³ or minimum side below 5 × 10¹¹ (Matson). Near-miss statistics trend *against* existence. |
| **Circulant Hadamard (Ryser) conjecture** | NON-EXISTENCE polarity | Settling it means proving no circulant Hadamard matrix of order > 4 exists. |
| **Barker sequences of length > 13** | NON-EXISTENCE polarity | Same shape. |
| **Optimal Golomb rulers, order ≥ 29** | NON-EXISTENCE polarity | A ruler is a construction, but *optimality* requires exhaustive infeasibility. |
| **Projective plane of order 12** | Known lower bounds put the witness beyond verification | The order-10 non-existence result (Lam–Thiel–Swiercz, 1989) took an extraordinary computation at a far smaller parameter. |
| **R(5,5) ≥ 44 via a 43-vertex Ramsey graph** | On an enumerable public problem list | *Dynamic Survey of Small Ramsey Numbers* is the canonical enumerable tracker for this whole family. Verification also needs a solver infeasibility claim (no K₅, no independent 5-set), capping B at 4. |
| **Any Erdős problem** | On an enumerable public problem list | erdosproblems.com is explicitly the most-swept AI4Math testbed; Epoch runs a separate FrontierMath: Erdős track. |
| **Frankl union-closed counterexample** | On public lists; witness probably does not exist | Verified to large ground-set sizes; recent asymptotic progress points toward truth. |
| **Odd perfect number** | Known lower bounds put the witness beyond verification | Bounds exceed 10¹⁵⁰⁰. |
| **6-chromatic unit-distance graph (Hadwiger–Nelson)** | On public lists; B capped | Polymath16 swept this; Epoch cites the unit distance problem as a flagship AI contribution. Verification needs a 5-colourability infeasibility certificate. |
| **Sudoku minimum-clue problem** | Solved (2012), and by non-existence | Listed only because it is a common false positive. |
| **Block designs / Steiner systems at small open parameters** | On an enumerable public problem list | Epoch commissioned a "Finding Small Block Designs" problem; the La Jolla difference set repository and the *Handbook of Combinatorial Designs* tables are the enumerable lists here. |

---

## 6. Methodology appendix

Every search run and page fetched this session, in order. Tool names as issued.

| # | Tool | Query or URL | What it settled |
|---|---|---|---|
| 1 | web_search | Conway 99-graph strongly regular graph (99,14,1,2) existence open 2025 | Conway-99 open; **discovered it is on FrontierMath: Open Problems**; found arXiv 2608.11211 (agent attack), 2606.29183 (Moore graph), Cesarz–Woldar 2025 |
| 2 | web_fetch | https://epoch.ai/frontiermath/open-problems | **Rejected** — PERMISSIONS_ERROR, URL not yet in a search result |
| 3 | web_search | Epoch AI FrontierMath Open Problems list of problems construction witness | Submission criteria; benchmark structure; block-designs problem |
| 4 | web_fetch | https://epoch.ai/frontiermath/open-problems | Full problem-type breakdown (Construction–Finite 32, Counterexample 12, …); full changelog; **Hadamard 668 marked solved 2026-08-12** |
| 5 | web_search | epoch.ai frontiermath/open-problems unsolved list Costas Moore graph Latin squares APN | Missing Moore Graph and Book Ramsey Numbers confirmed on FM:OP |
| 6 | web_search | three mutually orthogonal Latin squares of order 10 existence open status N(10) | 3 MOLS(10) open (2025 source); McKay–Meynert–Myrvold symmetry exclusion; Gill–Wanless rank-37 constraint; Delisle/Myrvold/SAT enumerations |
| 7 | web_search | Costas arrays smallest open order 32 33 existence unknown enumeration status | 32/33 confirmed smallest open; Golomb–Taylor eight-gap list; exhaustive frontier; symmetry-restricted enumeration through 32; Rickard's four new arrays |
| 8 | web_search | "big APN problem" APN permutation dimension 8 even n open 2025 2026 | Open; **3.5M quadratic APN sweep (2025) with null result**; butterfly route closed |
| 9 | web_search | 3x3 matrix multiplication tensor rank 23 lower bound 19 open rank 22 AlphaEvolve 2025 2026 | Rank 23 upper / 19 lower unchanged; addition race 60→52; **rank-22 search explicitly underway by agent teams** |
| 10 | web_search | Prouhet-Tarry-Escott ideal solution degree 11 13 unknown open smallest unsolved | Ideal solutions known n ≤ 10 and n = 12; open at 11 and ≥ 13; CMSV 2023 search bounds; quadratic-field solutions |
| 11 | web_search_fast | four mutually unbiased bases dimension 6 open problem status 2025 Zauner conjecture MUB | Open; ASD 0.9983; three numerical methods converge; McConnell shadow result; **McNulty–Weigert 2025 retraction of Chen et al. lemma** |
| 12 | web_search | Hadamard matrix smallest open order after 668 solved 716 779 list unresolved orders 2026 | **All twelve orders < 2000 closed**; discovered TheoremDB and Horizon/HorizonMath |
| 13 | web_search | theoremdb.org OR reachthehorizon.com Costas / MOLS / PTE / APN | No list hits for the four surviving candidates; surfaced the Gill–Wanless rank-37 result |
| 14 | web_search_fast | perfect cuboid perfect Euler brick search bound 2024 2025 | Frontier 2.5 × 10¹³ odd side / 5 × 10¹¹ min side; on Open Problem Garden |
| 15 | web_search | skew-Hadamard smallest open order unresolved orders list 276 Williamson survey | 276 and 292 closed by Đoković 2023–24; frontier ambiguous (356?) → sent to unverified pool as U1 |

**Currency caveat.** Fifteen searches is not an exhaustive sweep. The candidates in §2 are
unverified *because* I ran out of verification budget, not because they are weak — U1 and U3 in
particular look strong on every dimension except confirmed status.

---

## 7. Recall against source — what I believed before searching

Answered last, as commissioned. Thirteen beliefs checked.

**Corrected — 4.** These are the valuable lines.

1. **"The smallest open Hadamard order is 668."** **Corrected, and badly.** All twelve open orders
   below 2000 were closed on 12 August 2026 by Alpöge, Voinov and Reynolds-Haertle working with
   Claude. Had this triage not caught it, it would have sent effort at a closed problem — the exact
   failure mode the commission warns about. It also means the framing in the existing
   `/areas/hadamard-constructions.md` needs revising.
2. **"The smallest open skew-Hadamard order is 276."** **Corrected.** Đoković constructed 276 and
   292 (arXiv 2301.02751, revised through November 2024). The current frontier is probably 356 but
   I could not confirm it, hence U1.
3. **"The perfect cuboid search frontier is ~10¹⁰ minimum side / 3 × 10¹² odd side."**
   **Corrected upward.** Matson's later sweep reaches 5 × 10¹¹ and 2.5 × 10¹³ respectively.
4. **"FrontierMath is a benchmark of bespoke closed-form problems (Tiers 1–4)."** **Corrected.**
   There is now a separate Open Problems track of 50 genuinely unsolved problems, eight of which
   have fallen, plus a FrontierMath: Erdős track. This is the finding that reshaped the whole
   triage.

**Confirmed — 7.**

5. 3 MOLS(10) is open, and McKay–Meynert–Myrvold ruled out nontrivial autoparatopism groups. ✔
6. Costas arrays: 32 and 33 are the smallest orders with no known example. ✔
7. PTE ideal solutions are known for *n* ≤ 10 and *n* = 12; 11 and ≥ 13 are open. ✔
8. 3×3 matrix multiplication: rank 23 upper (Laderman 1976), 19 lower (Bläser); nothing between
   has moved. ✔
9. The Big APN Problem is open, with Dillon et al.'s 6-bit example the only known even-dimension
   APN permutation. ✔
10. MUBs in dimension 6: three are known, Zauner conjectured three is maximal, unresolved. ✔
11. Conway's 99-graph and the 57-regular Moore graph are both still open. ✔ (Though my *reason*
    for ranking them highly was wrong — see below.)

**Failed to settle — 2.**

12. **The exhaustive-enumeration frontier for Costas arrays.** Sources give 26, 27, 28 and 29 in
    papers of different dates, and I could not determine which is current. I used 29 (Jedwab–
    Wodlinger, 2014) as the most recent explicit claim. One check of the Rickard database resolves
    this.
13. **Whether the FrontierMath: Open Problems list contains any of my four surviving candidates.**
    I confirmed Conway-99, the Moore graph, Book Ramsey and Hadamard-668 are on it, and saw a
    partial listing covering roughly ten of fifty problems. The remaining forty are behind a
    JavaScript "See more" control I could not expand. **The four ranked candidates are therefore
    cleared only against the portion of the list I could read.** The promoting action is to
    download `https://epoch.ai/data/open_problems_data.zip` (updated 16 Sep 2026) and diff the
    full problem list against §1.

**The single most valuable correction.** Not any individual status update, but a structural one:
I came in ranking by *object smallness and verification cleanliness*, which is what dimensions
A–C and G–H measure. On those grounds Conway-99 and the Moore graph are the two best problems in
mathematics. They are also, for exactly that reason, the two problems most certain to be on an
agent-swept list. **The properties that make a problem score well here are the same properties
that make a benchmark designer select it.** The anti-criterion about public lists is not a side
constraint on this triage — it is in direct tension with the scoring function, and any future run
should apply it first, as a filter, rather than last, as a check." Response: "I'll work through this systematically. Starting with a wide cast, then verifying status before scoring anything.Important early signal — let me check what's on the agent-swept lists before scoring anything.The Hadamard 668 result changes things. Let me enumerate more of that list, since it's the key exclusion filter.Now verifying candidates that are *not* on the swept lists. Several searches in sequence.Two more agent-facing problem databases just surfaced. Checking my candidates against them.I have enough verified material. Writing the document now.Three things from this run are worth flagging before you read the file.

**Hadamard is closed below 2000.** On 12 August 2026 Alpöge, Voinov and Reynolds-Haertle posted constructions for all twelve remaining orders under 2000 — 668, 716, 892, and nine more. That directly undercuts the framing in your Hadamard thread, which targets "open orders above 668." There are none below 2000. The live frontier is above it, and I couldn't pin down where.

**The selection function is self-defeating.** Scoring well on this rubric — tiny object, exact one-directional check, unit-size unknown set — is precisely what makes a benchmark designer pick a problem. Epoch's FrontierMath: Open Problems has a filter literally labelled *Construction – Finite (32)*, and its submission criteria paraphrase your commission. Conway's 99-graph and the missing Moore graph score near-perfectly and are both on it, Conway-99 with an agent attack paper already on arXiv. I excluded both rather than ranking them. There are at least four such databases now, two of which I'd never seen (TheoremDB, Horizon).

**Six candidates survived status verification, not twenty.** 3 MOLS(10) and PTE size 11 tie at 38; Costas 32 and the rank-22 matmul tensor at 37. The falsification step did its job twice: the 3.5-million-function APN sweep from 2025 killed the only productive route to an 8-bit APN permutation, and the mod-*p* shadow result demoted the MUB candidate to "the object probably isn't there."

Two honest gaps. I could only read about ten of Epoch's fifty problems — the rest sit behind a JavaScript control — so the four ranked candidates are cleared against a partial list. Their data zip would close that. And the Costas exhaustive-enumeration frontier is reported as 26, 27, 28 and 29 in different papers; I used 29 and flagged it.
