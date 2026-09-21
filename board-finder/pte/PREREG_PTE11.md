# Pre-registration — ideal Prouhet–Tarry–Escott solution of size 11

**Registered 21 Sep 2026, before any size-11 data exists.** The harness (`verify.py`,
`search_symmetric.py`, `score_pte11.py`) and the predictions in §5 are committed in the same
commit as this file and before the first n = 11 run. Everything in §2–§4 was established before
registration and is marked as such.

## 1. The target and how it got here

An **ideal PTE solution of size *n*** is a pair of multisets *A*, *B* of *n* integers, *A* ≠ *B*,
with Σaᵏ = Σbᵏ for every *k* = 1…*n*−1.

`../gap/GATE_EPOCH.md` cleared this target against all 41 FrontierMath: Open Problems entries;
`../gap/RESULT_GAP_v2.md` §6 ranks it first to work on, above two candidates with higher scores,
because it is the only one whose **null result is itself publishable**. This file is the
pre-registration that §6's recommendation was waiting on.

## 2. Settled before registration: no ideal solution of ODD size is symmetric about its own mean

A solution is **symmetric** if the configuration is invariant under a reflection *x* ↦ *t* − *x*.
That reflection permutes *A* ∪ *B*, so it either **fixes** each half or **swaps** them. These are
different objects and the distinction decides what the search is.

> **Theorem.** No ideal solution of odd size is of the fixing kind.
>
> *Proof.* Let *n* = 2*m*+1 and suppose *A* is invariant under *x* ↦ 2*c* − *x*. Since
> *p*₁(*A*) = *p*₁(*B*) and both halves have *n* elements, their means agree, so *B* is symmetric
> about the same *c*. The reflection is an involution on a multiset of odd size, so it has a
> fixed point; hence *c* ∈ *A* and *c* ∈ ℤ. Translate *c* to 0. Then *A* consists of 0 with some
> odd multiplicity *r* together with pairs ±*a*₁…±*a*ₘ′, and likewise *B* with multiplicity *s*
> and pairs ±*b*ᵢ. Every odd power sum vanishes identically on both sides, so the conditions
> *k* = 1…2*m* reduce to the even ones: Σ*aᵢ*²ʲ = Σ*bᵢ*²ʲ for *j* = 1…*m*. Pad {*aᵢ*²} and
> {*bᵢ*²} with zeros to size *m*. These are two multisets of size *m* with equal power sums
> *p*₁…*p*ₘ, so Newton's identities give equal *e*₁…*eₘ* and hence equal multisets. The nonzero
> parts agree and so do the zero counts, so *r* = *s* and *A* = *B* — not a solution. ∎

**Confirmed computationally, not only argued.** `verify.py` enumerates every ideal solution of
size 5 to height 30 — six of them — and finds **zero** symmetric about their own mean, while the
same routine at size 4 (height 20) finds **eight of eight** symmetric. The theorem's parity
boundary is visible in objects produced here, not recalled.

## 3. Settled before registration: what the search at n = 11 actually is

At odd *n* only the **swapping** kind survives, so *B* = *t* − *A*. Centre at *t*/2 and double:
*C* = 2*A* − *t* is an *n*-element integer set whose negative is *B*'s centred form. The even
conditions hold identically, and the whole ideal requirement collapses to

> *p*ₖ(*C*) = 0 for every odd *k* ≤ *n*−2,  with *C* ≠ −*C*.

For **n = 11** that is **five equations — *p*₁ = *p*₃ = *p*₅ = *p*₇ = *p*₉ = 0 — in eleven
unknowns**. The asymmetric problem has ten equations in eleven unknowns. That gap of five is the
entire reason to run the symmetric region first.

Nothing is reported on the strength of this reduction. Every hit is turned back into an explicit
(*A*, *B*) and checked against all ten power sums by `verify.is_ideal`, because the one
verification error that cost this branch a day was reading success off a function's return value
instead of off the object.

## 4. The premise-falsification line — it fires

`PROMPT_GAP_v2.md` requires every candidate to carry a falsification line run during triage.
Here it is, and it half-kills the plan as written:

> `RESULT_GAP_v2.md` §6 says *"Then PTE size 11, symmetric-ansatz extension first."* Under the
> **fixing** reading of "symmetric" — the one that fits the classic size-6 solution
> {0,5,6,16,17,22} / {1,2,10,12,20,21}, and the one a reader meets first — **that search space is
> provably empty at size 11**, by §2. Anyone implementing the recommendation the natural way
> enumerates nothing and reports a null that means nothing.

The recommendation survives only under the **swapping** reading, which is live (two of the six
size-5 solutions are of that kind). This cost one afternoon to find and would have cost a run to
find later. It is recorded here rather than quietly fixed, because the v2 rubric's whole claim is
that this line pays for itself.

## 5. Predictions, registered before any n = 11 data

Each is stated so that it can fail, with what would falsify it.

| id | prediction | falsified by |
|---|---|---|
| **A-1** | One hour on this container, meet-in-the-middle split 5 + 6: the exhaustive symmetric search reaches **H ≥ 20** and **does not reach H = 50**. | completing H = 50, or failing to complete H = 20 |
| **A-2** | The binding constraint is **memory for the left table, not CPU time**. | being killed by the clock with memory headroom left |
| **A-3** | **No** ideal solution of size 11 is found anywhere in the region covered. | one is found — in which case nothing else here matters |
| **A-4** | The published exhaustive symmetric search at *n* = 11 covers a height bound **at least 1000×** whatever we reach. | the published bound being within 10× of ours |
| **A-5** | `RESULT_GAP_v2.md` §6's *"the asymmetric region is genuinely unswept"* will **not** survive its promoting search — I expect asymmetric searches to have been run too, with less publicity. | the promoting search finding no asymmetric search in the literature |

**A-1 and A-2 are the risky pair**, and they are guesses from one data point: at *n* = 7 the same
code needed 21 s for H = 60 and 158 s for H = 100, with a left table of 1.3 M keys. At *n* = 11,
H = 30 the left table is C(61,5) ≈ 5.5 M keys of five entries each and the right side is
C(61,6) ≈ 50 M tuples. Extrapolating that is exactly the kind of estimate this project has been
wrong about before.

**A-4 and A-5 are the ones that decide the programme**, and both need a promoting search this
session did not run. Named precisely so the search is not re-scoped afterwards:

1. the height bound of the exhaustive symmetric size-11 search in Borwein–Lisoněk–Percival,
   *Computational investigations of the Prouhet–Tarry–Escott problem* (Math. Comp., 2003), and
   whatever has superseded it;
2. whether the 2023 paper relayed as Coppersmith–Mossinghoff–Scheinerman–VanderKam exists under
   that authorship and what region it covers;
3. whether any published search covers **asymmetric** size-11 candidates.

## 6. Failure conditions for the programme, stated before the data

- **If A-3, A-4 and A-5 all hold**, PTE 11 is **dead** as a target for this project: the
  symmetric region is closed, our null is inside someone else's null, and the asymmetric region
  is not virgin either. The registered next move in that case is the **Hadamard worklist** —
  order 2284, *v* = 571, 156 free bits, from the user's own `FINDING_05`. Recorded now so it
  cannot be rationalised into a smaller retreat later.
- **If A-4 fails**, there is real room in the symmetric region and the search should be scaled up
  properly rather than run on a container.
- **If A-5 fails**, the asymmetric region is the target — and it needs a **new** pre-registration,
  because its search shape is different (ten equations, not five) and nothing measured here
  transfers to it.
- **If A-3 fails**, everything above is moot.

## 7. What the harness will and will not score

`score_pte11.py` scores A-1…A-5 against evidence files and **refuses to score a prediction whose
evidence file does not exist** — it does not treat absence as a pass. It is committed before the
data for the same reason the coverage harness was: a scorer written after the numbers are in is
not a scorer.

It also re-runs the controls on every invocation. A null from a search that cannot find a known
object is not a null, and at size 11 there is no known object to find — so the controls at
*n* = 5 and *n* = 7 are the only evidence that the machinery works at all.

## 8. Provenance — the load-bearing claims are the unverified ones

**PRIMARY-VERIFIED-LOCALLY.** The §2 theorem and its size-4/5 confirmation; the §3 reduction; the
size-6 classic and the size-7 classic {0,18,27,58,64,89,101} / {1,13,38,44,75,84,102}, both
produced by search here rather than recalled, and verified against every power sum; the counts
"six essentially distinct size-5 solutions to height 30" and "eight of eight at size 4".

**SECONDARY-RELAYED, not verified here.** That ideal solutions are known for *n* ≤ 10 and
*n* = 12 with **11 the smallest open size**; the 2023 paper; the June 2025 survey. All of it
comes from `../gap/sources/GAP_V2_RESPONSE_RAW.md`.

**This is the honest shape of the target: everything that makes size 11 *interesting* is
relayed, and everything verified here is about sizes that are already solved.** The promoting
searches in §5 are not housekeeping — if the first of them comes back wrong, there is no target.

## 9. Negative tests on the scorer, run before registration

A scorer that cannot fail is not a scorer, and two checks written earlier today could not fail
(`../../..` → the fermats-last-theorem ledger, D43). Seven perturbations, all behaving correctly:

| perturbation | result |
|---|---|
| a fabricated exhaustive run at H = 50 | `A-1 FALSIFIED  reached H=50 exhaustively, predicted not to reach 50` |
| a fabricated H = 25 run with the hour spent | `A-1 CONFIRMED` · `A-2 CONFIRMED` · `A-3 CONFIRMED` |
| a fabricated H = 12 run with the hour spent | `A-1 FALSIFIED … only H=12, predicted >= 20` · `A-2 FALSIFIED` |
| a **fake** size-11 solution planted in a run file | `A-3 FALSIFIED  a solution is on file and DOES NOT verify … power sum k=1 differs: 55 != 66` |
| A-4 evidence at 5× and A-5 with an empty search list | both `FALSIFIED` |
| A-3, A-4, A-5 all confirmed | **`SECTION 6 FIRES`** — names the Hadamard worklist as the registered next move |
| the odd-*n* control inverted in `verify.py` | the scorer aborts before printing any verdict |

The fourth matters most: a planted solution is not taken at face value even though it arrived
through the harness's own file format. It is re-verified against every power sum, and the scorer
reports *which* one fails.

## 10. Addendum, registered 21 Sep 2026 — a second instrument, and four more predictions

The user pointed at Cançado–Coutinho–Spier, *Orthogonal polynomials, quantum walks and the
Prouhet–Tarry–Escott problem* (arXiv:2509.09948, 12 Sep 2025). Its Corollary 21 — Caley's
interlacing theorem — **forces the sign pattern of the centred set**, which the registered
search in §3 used not at all. See `CCS2025.md`. `search_pattern.py` implements it. Same n = 7
control, same two solutions, **1.2 s against 21.0 s**.

These are registered before the first n = 11 run of the new instrument. They do **not** re-score
A-1…A-3, which were about `search_symmetric.py` and are already settled in `RESULT_PTE11.md`.

| id | prediction | falsified by |
|---|---|---|
| **B-1** | one hour, split 5 + 6: the pattern search reaches **H ≥ 70** exhaustively and **does not reach H = 100** | completing 100, or failing 70 |
| **B-2** | **memory** binds this time, not the clock — the roles reverse relative to the registered run | stopping on the clock with memory headroom |
| **B-3** | still **no** solution anywhere in the covered region | finding one |
| **B-4** | the gain is from enumerating **fewer** tuples, not faster ones: the per-right-tuple rate stays within 2× of the registered search's 172 k/s | a rate outside 86 k–344 k/s |

**B-2 is the same mechanism claim that A-2 got wrong**, registered again because the arithmetic
now points the other way: at 445 bytes/key the 12 GB cap is reached around H ≈ 85, while one hour
at 172 k/s reaches C(H,6) ≈ 620 M, i.e. H ≈ 90. If that is right the walls have swapped order.
Registering it a second time is the point — the first version was a guess, this one has the
measured constants behind it, and it can fail the same way.

**B-1's floor of 70 is what makes this worth running at all.** §4 of `RESULT_PTE11.md` showed the
registered run's H = 36 never reached the primitive centred height 51 at which the smallest known
size-**7** solution sits. H ≥ 70 clears that bar; it is the first region this project would cover
that a solved case of the same shape would have been found in.

**Scope is narrower in one way, and it is not a free win.** The pattern derivation needs *C* and
−*C* disjoint, which is exactly PTE⁰ — Theorem 18's variant for odd *d*. Solutions with a
repeated element (PTE¹, PTE) are **not** covered by `search_pattern.py` and remain
`search_symmetric.py`'s business. A B-3 null is a null about PTE⁰ only.
