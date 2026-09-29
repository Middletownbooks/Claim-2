# Worker brief — Arm 1a: the `II` records nobody assessed

**Read `board-finder/gap/discovery/prompts/COMMON.md` first. Everything in it applies.**

## Why these records

A 499-record ranking of important open problems was screened for "playability": can the problem be
settled by exhibiting one finite object? A class of 22 records — **exact-value or optimality
determinations** ("determine the constant", "determine the order of magnitude") — was excluded as
a class and never assessed. The question now is whether that exclusion hid record problems whose
*tracked bound* can be moved by exhibiting a finite object. You are assessing 10 of them.


## The gates you evaluate, verbatim from the registered selection function

A headline like "determine X exactly" is almost always hopeless as stated. What a working group
can move is a **tracked quantity** underneath it — best known lower and upper bounds. For each
side of that quantity, identify the **bound object** whose exhibition moves that side:

* `WITNESS` — a finitely describable object whose value is fixed by a terminating computation,
  exact or rigorous-numeric (a matrix, a point configuration, a graph, a step function, a finite
  certificate)
* `PROOF` — a new argument
* `ALGORITHM` — a finite string whose correctness is universally quantified (an algorithm, a
  universal polynomial, a reduction)
* `NONE` — nothing moves it (e.g. the side is only ever estimated numerically, not bounded)

Then evaluate each gate. **Every gate is PASS / FAIL / CANNOT EVALUATE. CANNOT EVALUATE is
required whenever the evidence is not there.**

| gate | PASS iff |
|---|---|
| **S0 OPEN** | the headline and the tracked record are unresolved. Report any resolution claim with its status; withdrawn or unrefereed claims are data, not resolutions. |
| **S1 COUPLED** | at least one side's bound object is a `WITNESS` **and** exhibiting a better witness moves a published bound **on the headline quantity itself**, not on a finite analogue of it. Two routes count: **(a)** the headline quantity is an extremum (sup / inf / max / min) over finitely describable objects, so any one object is a one-sided bound; or **(b)** a published bound on the headline was established by a finite certificate checked by terminating computation. An **asymptotic-order** headline ("determine the order of magnitude of f(n)") is COUPLED **only** through a published lifting theorem that turns a finite object into an asymptotic bound (model case: a cap in AG(n,3) of size s gives, by taking products, cap-set capacity ≥ s^(1/n)). Cite the extremal characterisation, the certificate paper, or the lifting theorem. |
| **S2 NOT VETOED** | the witness's defining predicate is decidable and its value is computable by terminating computation. **FAIL (vetoed) if** the bound object is an `ALGORITHM`, or if checking the witness's property is undecidable. |
| **S3 IDEA GAP** | the **most recent** move of the coupled side has kind `ANALYTIC` or `SEARCH-NEW` (definitions in COMMON.md). FAIL if `SEARCH-REPEAT`. CANNOT EVALUATE if `UNKNOWN`. |
| **S4 NOT CROWDED** | the coupled side has **not** moved on or after **2025-01-01** by an AI-driven search system or by large-scale optimisation tooling. Say what you searched for; "found nothing" with the searches listed is a PASS, "did not search" is CANNOT EVALUATE. |
| **S5 DELIVERABLE** | a named maintained table, or a named published bound, would change on a one-step improvement. Write the one sentence that would appear in the abstract of the paper reporting it. |

If S1 is FAIL, S2–S5 still get a one-line answer each, but you may keep them short.

Also report, per record:

* **DIVERGENCE** — are there two dated, published methods on the *same object* whose reach
  differs by a factor ≥ 2 **in the frontier parameter itself** (dimension, order, size, number
  of points — not runtime)? Cite both, or write `NONE FOUND` with what you searched.
* **bits_search** — `UNDEFINED` unless a named search ansatz for the witness **and** a published
  density estimate for it both exist; then cite them. Do not estimate this yourself.
* **verification class of one improvement step** — `CHECK` (exact finite computation),
  `RIGOROUS-NUMERIC`, or `PROOF` (a new argument needing refereeing).

## Output — one block per record, exactly this shape

```
RECORD      | <rank> — <title>
QUANTITY    | <the tracked quantity, one clause>
LOWER       | <best known lower bound, value, who, year> | <tier> | <precision tags>
UPPER       | <best known upper bound, value, who, year> | <tier> | <precision tags>
BOUND OBJ   | lower: <WITNESS|PROOF|ALGORITHM|NONE> — <why> ; upper: <…> — <why>
S0 OPEN     | <PASS|FAIL|CANNOT EVALUATE> — <evidence, any resolution claims with status>
S1 COUPLED  | <PASS|FAIL|CANNOT EVALUATE> — <route (a) or (b) or lifting theorem; citation> | <tier>
S2 VETO     | <PASS|FAIL|CANNOT EVALUATE> — <why>
MOVE-1      | <date> | <authors> | <value> | <kind> [+AI-SEARCH] | <evidence: what the paper did> | <tier>
MOVE-2      | <same fields> | or NONE
S3 IDEA     | <PASS|FAIL|CANNOT EVALUATE> — <derived from MOVE-1's kind>
S4 CROWDED  | <PASS|FAIL|CANNOT EVALUATE> — <what you searched; what you found>
S5 DELIVER  | <PASS|FAIL|CANNOT EVALUATE> — <table or bound; the abstract sentence>
DIVERGENCE  | <two methods, both reaches, the ratio, citations> | or NONE FOUND — <searches>
BITS_SEARCH | <UNDEFINED — why> | or <value, ansatz, source>
VERIF CLASS | <CHECK|RIGOROUS-NUMERIC|PROOF>
NOTES       | <dead ends, contradictions with this brief, anything the adjudicator should know>
```

MOVE-1 / MOVE-2 are about **the coupled side** (the side a witness bounds). If nothing is
coupled, give the most recent move on whichever side has moved and say so.

## Where to write

Write every block, in the order given, to **`board-finder/gap/discovery/A1_a.md`** (create it). Start the file with a summary
table: one row per record, columns `rank | S0 | S1 | S2 | S3 | S4 | S5`, each cell PASS / FAIL /
CANNOT EVALUATE — and derive it from your blocks, don't retype it from memory.

When finished, reply with the path, the summary table, and anything that contradicts this brief.

## Your records

### 17 — BQP Versus NP: Complete Language-Class Relation  *(domain: theoretical_computer_science; corpus status: open)*

> Determine the truth values of BOTH NP subseteq BQP and BQP subseteq NP for unrelativized, advice-free classes of total languages over {0,1}. NP consists of languages with polynomial-length binary witnesses and a deterministic polynomial-time verifier. BQP consists of languages decided by polynomial-time uniformly generated polynomial-size quantum circuits (a deterministic Turing machine outputs Q_n on 1^n), using Watrous's fixed Toffoli, Hadamard and phase-i gates with |0> ancillas and discarding, followed by a standard-basis output measurement. On every yes input acceptance is at least 2/3, and on every no input it is at most 1/3. No arbitrary real gate constants, advice or oracle are available. Establish equality, either proper containment, or incomparability.

### 186 — Order of Magnitude of Maximum 3-Term-AP-Free Subsets of {1,...,N}  *(domain: combinatorics_discrete_geometry; corpus status: open)*

> Let r_3(N) be the maximum cardinality of a subset of {1,...,N} containing no nontrivial three-term arithmetic progression. Determine the asymptotic order of r_3(N) as N tends to infinity; currently its scale lies between Behrend-type lower bounds N exp(-C sqrt(log N)) and the upper bound N exp(-c (log N)^(1/6)/log log N), up to constants and lower-order refinements.

### 199 — Exact Asymptotic Waring Function G(k)  *(domain: number_theory_arithmetic_geometry; corpus status: open)*

> For each integer k>=3, let G(k) be the least positive integer s for which every sufficiently large positive integer N is expressible as a sum of at most s positive integral k-th powers. Determine the entire function G(k) for all k>=3. Equivalently, zeros may be allowed and exactly s nonnegative integral k-th powers used; this is not the condition of exactly s positive summands.

### 246 — Zagier's dimension conjecture for classical multiple zeta values  *(domain: number_theory_arithmetic_geometry; corpus status: open_with_solved_subcases)*

> For positive integers k_1,...,k_r with k_1>=2, define the classical convergent real multiple zeta value zeta(k_1,...,k_r)=sum_(n_1>...>n_r>0) 1/(n_1^k_1 ... n_r^k_r), of weight k_1+...+k_r. For each k>=2 let Z_k be their Q-linear span at weight k, with Z_0=Q generated by the empty value1 and Z_1={0}. Define d_0=1,d_1=0,d_2=1 and d_k=d_(k-2)+d_(k-3) for k>=3. Is dim_Q Z_k=d_k for every k>=0?

### 277 — Growth Rate of 3-Uniform Hypergraph Ramsey Numbers  *(domain: combinatorics_discrete_geometry; corpus status: open)*

> Let r_3(t) be the least N such that every red-blue coloring of the triples of an N-element set has a monochromatic t-element set. Determine the asymptotic growth of r_3(t); in particular, prove or disprove that r_3(t) is at least 2^(2^(c t)) for some constant c>0 and all sufficiently large t.

### 288 — Complex linearity of closed-surface mapping class groups by genus  *(domain: geometry_topology; corpus status: open)*

> For every integer g >= 3, let S_g be the closed connected orientable surface of genus g and Mod(S_g) its group of isotopy classes of orientation-preserving homeomorphisms. Determine exactly the set of such genera g for which there exist an integer n >= 1 and an injective homomorphism Mod(S_g) -> GL_n(C), with n allowed to depend on g. A complete resolution proves the answer for every g >= 3; one nonlinear genus, a bounded-dimensional obstruction, or an isolated family of representations without the remaining genus answers is partial progress.

### 308 — Exact Real Grothendieck Constant  *(domain: analysis_pde; corpus status: open)*

> Determine the smallest real constant K_G such that, for every finite real m-by-n matrix (a_ij) and all unit vectors u_1,...,u_m,v_1,...,v_n in a real Hilbert space, abs(sum_ij a_ij <u_i,v_j>) <= K_G max_{epsilon_i,delta_j in {-1,1}} abs(sum_ij a_ij epsilon_i delta_j). The constant is uniform over both matrix sizes and Hilbert-space dimension.

### 351 — Exact Capacity Region of the Two-User Gaussian Interference Channel  *(domain: cryptography_coding_information_optimization; corpus status: open)*

> Determine the exact capacity region of the two-user Gaussian interference channel in the moderately weak and strong interference regimes.

### 353 — Asymptotic Turan Numbers of Even Cycles  *(domain: combinatorics_discrete_geometry; corpus status: open_with_solved_subcases)*

> Determine the order of magnitude of ex(n, C_{2k}), the maximum number of edges in an n-vertex graph with no cycle of length 2k, for every fixed k.

### 368 — Thomson problem  *(domain: mathematical_physics; corpus status: open_with_solved_subcases)*

> For each positive integer N, determine the configuration of N equal point charges on the unit sphere that minimizes total Coulomb energy.
