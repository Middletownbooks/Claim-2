# Worker brief — Arm 1b: the `II` records nobody assessed

**Read `board-finder/gap/discovery/prompts/COMMON.md` first. Everything in it applies.**

## Why these records

A 499-record ranking of important open problems was screened for "playability": can the problem be
settled by exhibiting one finite object? A class of 22 records — **exact-value or optimality
determinations** ("determine the constant", "determine the order of magnitude") — was excluded as
a class and never assessed. The question now is whether that exclusion hid record problems whose
*tracked bound* can be moved by exhibiting a finite object. You are assessing 9 of them.

After your nine records, **also decompose three records already assessed elsewhere — 221, 282, 337 — using the same block.** They are not counted in any tally; they are a consistency check against earlier work (337 is recorded elsewhere as dead because arXiv:2609.19412 narrowed the deletion-channel gap to a hundredth of a bit in Sep 2026; 221's lower bound 3.52 is recorded as unmoved since 2003; 282's bounds are recorded as tightened in 2025 by arXiv:2506.03429). If your evidence contradicts any of those three statements, say so — that is the most useful thing you can report about them.


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

Write every block, in the order given, to **`board-finder/gap/discovery/A1_b.md`** (create it). Start the file with a summary
table: one row per record, columns `rank | S0 | S1 | S2 | S3 | S4 | S5`, each cell PASS / FAIL /
CANNOT EVALUATE — and derive it from your blocks, don't retype it from memory.

When finished, reply with the path, the summary table, and anything that contradicts this brief.

## Your records

### 375 — Sharp asymptotic order of minimal star discrepancy in each dimension d >= 3  *(domain: combinatorics_discrete_geometry; corpus status: open_with_solved_subcases)*

> For every fixed integer d >= 3, determine the asymptotic order, up to positive multiplicative constants depending only on d, of Delta_d(N)=inf_{P subset [0,1)^d, |P|=N} sup_{x in [0,1]^d} |#(P intersect product_j[0,x_j))-N product_j x_j| as N tends to infinity.

### 385 — Lieb-Thirring Conjecture on the Sharp Constant for Riesz Means of Order One in Three Dimensions  *(domain: mathematical_physics; corpus status: open)*

> Prove that the optimal constant L_{1,3} in Tr(-Delta+V)_- <= L_{1,3} integral_{R^3} V_-(x)^(5/2) dx equals the semiclassical constant L_{1,3}^{cl}=1/(15*pi^2).

### 410 — Smallest number of variables for undecidable Hilbert's Tenth Problem over Z  *(domain: logic_foundations_set_theory; corpus status: open_with_solved_subcases)*

> Determine the least integer n for which no algorithm decides whether an arbitrary integer-coefficient polynomial in at most n variables has an integer zero.

### 413 — Zarankiewicz Problem on K_{t,t}-Free Bipartite Graphs  *(domain: combinatorics_discrete_geometry; corpus status: open)*

> Determine the asymptotic order of magnitude of ex(n, K_{t,t}), the maximum number of edges in an n-vertex bipartite graph containing no K_{t,t}, for each fixed t >= 2.

### 417 — Exact Consistency Strength of the Proper Forcing Axiom (PFA)  *(domain: logic_foundations_set_theory; corpus status: open)*

> Determine the exact large-cardinal consistency strength of the Proper Forcing Axiom.

### 428 — Exact value of the site-percolation threshold on the square lattice  *(domain: probability_ergodic_dynamics; corpus status: open)*

> Determine the exact critical probability p_c for Bernoulli site percolation on the nearest-neighbor square lattice Z^2. The corresponding bond-percolation threshold is p_c = 1/2, whereas the site threshold is known only numerically, p_c approximately 0.592746, and no exact value is known.

### 441 — Witsenhausen Counterexample: Optimal Strategy and Cost  *(domain: applied_computational_mathematics; corpus status: open)*

> Determine the optimal control strategies and exact minimum expected cost for the two-stage Witsenhausen problem x1 = x0 + u1, x2 = x1 + u2, where x0 ~ N(0, sigma^2), decision maker 1 observes x0 and incurs k u1^2, and decision maker 2 observes z2 = x1 + v with v ~ N(0,1) and incurs x2^2.

### 450 — Exact critical exponents of oriented percolation in 1+1 dimensions  *(domain: probability_ergodic_dynamics; corpus status: open)*

> For nearest-neighbor oriented percolation in 1+1 space-time dimensions at criticality, determine the exact values of rho, eta, and nu governing survival probability, the expected number of vertices connected from the origin at time t, and the gyration radius, respectively.

### 479 — Ruzsa-Szemerédi (6,3)-Problem on Triple Systems  *(domain: combinatorics_discrete_geometry; corpus status: open)*

> Determine the asymptotic order of f(n,6,3), the largest number of edges in a 3-uniform hypergraph on n vertices in which no six vertices span three or more edges.

## Consistency-check records (decompose, not counted)

### 221 — Exact satisfiability threshold for random k-SAT for small k (k = 3)  *(domain: probability_ergodic_dynamics; corpus status: open)*

> In the uniform random 3-SAT model, choose a 3-CNF formula with n variables and m clauses uniformly from formulas whose clauses contain three distinct literals. Determine the exact constant r_3 such that, as n tends to infinity with m/n tending to r, satisfiability has probability tending to 1 for r < r_3 and tending to 0 for r > r_3.

### 282 — Exact Unassisted Quantum Capacity of the Qubit Depolarizing Channel  *(domain: quantum_information_computation; corpus status: open_with_solved_subcases)*

> For every p in [0,1], determine the exact unassisted quantum capacity Q(D_p) of the memoryless qubit channel D_p(rho)=(1-p)rho+pI/2. Capacity is the supremum of asymptotically achievable rates in qubits per channel use for quantum-information transmission with vanishing error and arbitrary block coding, without preshared entanglement or auxiliary classical communication.

### 337 — Capacity of the binary deletion channel  *(domain: cryptography_coding_information_optimization; corpus status: open)*

> Determine the exact average-error Shannon capacity C_del(d) of the binary deletion channel for every fixed deletion probability d with 0 < d < 1.
