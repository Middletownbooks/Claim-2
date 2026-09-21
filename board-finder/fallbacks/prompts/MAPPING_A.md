# Mapping layer, chunk A of 4 — Discrete, computational and coding

**HIGHEST expected yield -- numeric record tables are commonest here. Run this one first.**

## What this is for

A 499-record corpus ranks open mathematical problems by editorial importance. It records each
problem in its **headline form** — *"determine the exact value"*, *"prove the conjecture"* — which
is almost always the hopeless form. What a working group can actually move is usually a **tracked
quantity underneath** the headline: a best-known bound, a record construction, a verification
height, a competitive ratio.

The corpus never names that quantity. Your job is to supply it, for 31 records.

**Example of the gap, so the task is unambiguous:**

| recorded headline | the quantity the literature actually tracks |
|---|---|
| "Determine the exact capacity C_del(d) of the binary deletion channel" | best known upper and lower bounds on C_del(d) |
| "Prove every metric space admits a k-competitive deterministic k-server algorithm" | the best known competitive ratio for general metrics (2k−1) |
| "Determine the exact least integer ES(n) forcing n points in convex position" | the bounds on ES(7) |

## For each record below, answer exactly four questions

1. **TRACKED QUANTITY** — what number (or object) does the working literature actually report
   progress on? One clause. If there is none — the problem is structural and nobody reports a
   number — write `NONE` and move on; that is a real answer and it is expected to be common.
2. **CURRENT VALUE** — the value as of the most recent source you can date.
3. **LAST MOVED** — the year it last changed, and by whom. If it has never moved since first
   stated, say so with the original year.
4. **WHAT MOVES IT** — in one clause: a construction, an algorithm, a proof technique, or raw
   computation. This is the single most useful field; be specific about which.

## Rules

- **Source or NOT FOUND.** Every value needs a citation you can name and date. If you cannot find
  one, write `NOT FOUND` — never estimate, never interpolate, never reason from what "should" be
  the case.
- **Tier every answer.** `PRIMARY` = you read a paper, table or database that states it.
  `SECONDARY` = a survey or secondary source relays it. `RECALL` = you believe it but found no
  source this session. RECALL entries are treated as unverified downstream, so marking them
  honestly costs nothing and mislabelling them costs a great deal.
- **Do not rank, recommend or triage.** Later stages do that. Filling a field with judgement
  instead of a citation makes the whole table unusable.
- **`NONE` is a good answer.** A high `NONE` rate is informative and expected in some chunks.

## Output format — one block per record, nothing else

```
RANK  | <rank>
TITLE | <title>
TRACKED QUANTITY | <one clause, or NONE>
CURRENT VALUE    | <value, or NOT FOUND>
LAST MOVED       | <year, by whom, or NEVER MOVED since <year>>
WHAT MOVES IT    | construction | algorithm | proof technique | computation | N/A
TIER             | PRIMARY | SECONDARY | RECALL
SOURCE           | <citation with a date, or NOT FOUND>
```

## The records


**128 — NP-Completeness of the Minimum Circuit Size Problem (MCSP)**  *(Theoretical computer science)*
> Prove or disprove that MCSP is NP-hard under deterministic polynomial-time many-one reductions, where an input is the truth table of a Boolean function and a size bound and asks whether a circuit of at most that size computes the function.

**129 — Polynomial pivot rule for the simplex method**  *(Cryptography, coding, information & optimization)*
> Construct a deterministic or randomized simplex pivot rule and a polynomial p such that, for every bounded nondegenerate rational linear program with m equality constraints and n variables and every feasible starting basis, the rule reaches an optimal basis in at most p(m,n) pivots, in expectation w…

**131 — Planted Clique Conjecture**  *(Theoretical computer science)*
> For every fixed real alpha with 0<alpha<1/2, set k_n=floor(n^(1/2-alpha)). Sample a uniform k_n-subset S of n labeled vertices, put every edge inside S, and independently include each other edge with probability1/2. There is no randomized algorithm running in time polynomial in n that, given this gr…

**134 — Superlinear Circuit Lower Bounds for Explicit Boolean Functions**  *(Theoretical computer science)*
> There exists a Boolean function family f_n:{0,1}^n->{0,1}, n>=1, evaluated by a single deterministic polynomial-time algorithm on (1^n,x), whose minimum gate count C_B2(f_n) over single-output fan-in-two circuits using arbitrary binary Boolean gates satisfies C_B2(f_n)=omega(n): for every c>0 there …

**136 — Indistinguishability Obfuscation from Constant-Degree Homomorphic Assumptions**  *(Cryptography, coding, information & optimization)*
> Construct indistinguishability obfuscation based purely on standard polynomial-time assumptions (such as standard LWE, LPN, and degree-2 multilinear pairings) without sub-exponential loss.

**137 — Log-Rank Conjecture in Communication Complexity**  *(Cryptography, coding, information & optimization)*
> Prove that there is a universal constant C >= 1 such that, for every Boolean function f:X x Y -> {-1,1} on finite nonempty sets X,Y, D(f) <= C[log_2 max{2,rank_R(M_f)}]^C, where M_f(x,y)=f(x,y) is its sign communication matrix and D(f) is deterministic two-party communication complexity in bits.

**142 — Asymptotic tightness of the binary Gilbert–Varshamov bound**  *(Cryptography, coding, information & optimization)*
> For integers n>=1 and d>=0, let A_2(n,d) be the maximum cardinality of a binary code C subset {0,1}^n, not necessarily linear, with Hamming distance at least d between distinct codewords. For each fixed real 0<delta<1/2 define R_2(delta)=limsup_{n->infinity} n^(-1) log_2 A_2(n,floor(delta n)) and H_…

**156 — Randomized Integer Word-RAM 3SUM Conjecture**  *(Theoretical computer science)*
> For every epsilon>0, there is no uniform Las Vegas randomized integer word-RAM algorithm that, on every set S of n distinct integers in [-n^3,n^3], decides whether three distinct elements sum to zero in worst-case expected O(n^(2-epsilon)) time. Use the standard logarithmic-word model of Abboud–Vass…

**158 — BPL = L (Derandomizing Bounded-Error Logspace)**  *(Cryptography, coding, information & optimization)*
> Prove or disprove that every language decidable by a probabilistic Turing machine using O(log n) workspace, polynomial time, and bounded two-sided error is decidable by a deterministic Turing machine using O(log n) workspace.

**163 — Metric TSP Subtour LP Integrality Gap Conjecture**  *(Cryptography, coding, information & optimization)*
> Prove or disprove that the integrality gap of the subtour (Held-Karp) LP relaxation of the symmetric metric traveling salesman problem equals 4/3.

**181 — Berman-Hartmanis Isomorphism Conjecture**  *(Theoretical computer science)*
> Prove or disprove that for every two languages A and B complete for NP under polynomial-time many-one reductions, there is a bijection h on binary strings such that h(A)=B and both h and its inverse are computable in polynomial time.

**185 — Polynomial Freiman-Ruzsa Conjecture for General Abelian Groups**  *(Combinatorics & discrete geometry)*
> Prove that there is an absolute constant C such that for every finite subset A of an arbitrary abelian group with |A+A| <= K|A|, the set A can be covered by exp(C log K) translates of a centred convex coset progression of dimension at most C log K and size at most exp(C log K)|A|.

**217 — All-Pairs Shortest Paths in Truly Subcubic Time**  *(Cryptography, coding, information & optimization)*
> Determine whether exact all-pairs shortest paths on weighted n-vertex graphs can be computed in O(n^(3-epsilon)) time for some fixed epsilon greater than zero.

**220 — Polynomial-Time Distribution-Free PAC Learning of DNF Formulas**  *(Theoretical computer science)*
> Given an unknown s-term DNF f on {0,1}^n and random labeled examples drawn from an arbitrary unknown distribution D, construct a possibly improper hypothesis in time polynomial in n, s, 1/epsilon, and log(1/delta) whose D-error is at most epsilon with probability at least 1-delta.

**234 — The k-Server Conjecture for General Metric Spaces**  *(Theoretical computer science)*
> For every integer k >= 1 and every metric space, prove that there is a deterministic online k-server algorithm whose movement cost on every request sequence is at most k times the offline optimum, up to an additive constant.

**236 — Perfect-Matching Search in Deterministic NC (General Graphs)**  *(Theoretical computer science)*
> Assert the existence of one logspace-uniform family (C_n) of deterministic Boolean AND/OR/NOT circuits which, for every n>=1 and every finite simple undirected graph G on labelled vertices 1,...,n given by its n-by-n adjacency matrix, outputs a perfect matching of G if one exists and outputs a disti…

**238 — Chromatic Number of the Plane (Hadwiger-Nelson Problem)**  *(Combinatorics & discrete geometry)*
> Determine the chromatic number of the plane: the minimum number of colors needed to color every point of the Euclidean plane so that any two points at Euclidean distance exactly 1 receive distinct colors.

**248 — Universal Optimality of the Hexagonal Lattice in Dimension Two**  *(Combinatorics & discrete geometry)*
> Let A2 be the triangular lattice scaled to density1 in R^2. A configuration C is a discrete closed subset with lim(R->infinity)|C intersect B_R(0)|/area(B_R(0))=1. For p(r)=f(r^2), where f:(0,infinity)->R is C-infinity and (-1)^k f^(k)>=0 for every integer k>=0, define lower energy by liminf(R->infi…

**249 — RL versus L**  *(Theoretical computer science)*
> Let L be the languages of binary strings decided by deterministic Turing machines using O(log(N+2)) work space on length-N inputs. Let RL use the same read-only input and read-write work-tape convention but allow fresh unbiased read-once random bits, retaining an old bit only by storing it in counte…

**259 — Polynomial-Time Decidability of Semidefinite Programming Feasibility**  *(Cryptography, coding, information & optimization)*
> Determine whether feasibility of a semidefinite program with rational symmetric input matrices can be decided in polynomial time in the Turing bit model.

**262 — Classical Worst-Case Hardness Reduction for LWE**  *(Cryptography, coding, information & optimization)*
> Determine whether there is a classical (non-quantum) worst-case hardness reduction for the Learning With Errors problem that fully subsumes Regev's quantum reduction, i.e. reducing both GapSVP_gamma and SIVP_gamma to LWE for the same parameters, with polynomial modulus and no loss in lattice dimensi…

**264 — MAJORITY is not in ACC0**  *(Theoretical computer science)*
> Let MAJORITY_n(x)=1 exactly when sum_i x_i>=n/2. Define nonuniform ACC0 as Boolean families computed, for every input length n>=1, by circuits of polynomial size and some fixed constant depth using unbounded-fan-in AND, OR and MOD_m gates and fan-in-one NOT gates, with constants allowed and one fixe…

**283 — Polynomial-time explicit logarithmic Ramsey graphs**  *(Theoretical computer science)*
> Does there exist one deterministic algorithm A and constants C,c>0 such that, for every integer N>=2 given in unary, A outputs the adjacency matrix of a simple N-vertex graph in time at most O(N^c), with both its clique number and independence number at most C log_2 N? This is ordinary output-size p…

**309 — Bodirsky-Pinsker Tractability Conjecture for Infinite-Domain Constraint Satisfaction**  *(Theoretical computer science)*
> For every finite-signature first-order reduct A of a countable finitely bounded homogeneous relational structure, determine whether absence of a primitive-positive construction of the three-vertex complete graph K3 implies that CSP(A), the finite-input homomorphism problem to the fixed template A, h…

**310 — Deterministic polynomial-time exact bipartite matching**  *(Theoretical computer science)*
> Does there exist a deterministic algorithm which, for every explicitly encoded finite simple bipartite graph G=(U∪V,E), a red/blue colouring of E and an integer k encoded in binary, decides in time polynomial in the total input bit length whether G has a perfect matching with exactly k red edges? Un…

**315 — The Dynamic Optimality Conjecture for Splay Trees**  *(Theoretical computer science)*
> Prove that there is a universal constant C such that, for every access sequence, the cost of the splay-tree algorithm is at most C times the minimum cost of any offline dynamic binary search tree algorithm, up to the standard additive initialization term.

**329 — Černý Conjecture on Shortest Reset Words of Synchronizing Automata**  *(Theoretical computer science)*
> Prove or refute that every synchronizing deterministic finite automaton with n states admits a reset (synchronizing) word of length at most (n-1)^2, i.e., that the reset threshold of every n-state synchronizing automaton does not exceed (n-1)^2.

**337 — Capacity of the binary deletion channel**  *(Cryptography, coding, information & optimization)*
> Determine the exact average-error Shannon capacity C_del(d) of the binary deletion channel for every fixed deletion probability d with 0 < d < 1.

**340 — The Online Boolean Matrix-Vector Multiplication Conjecture**  *(Theoretical computer science)*
> Prove or refute that for every epsilon > 0 there is no randomized algorithm which, given an n by n Boolean matrix and then n Boolean query vectors one at a time, outputs each Boolean-semiring product before receiving the next vector in total time O(n^(3-epsilon)) with error probability at most 1/3.

**341 — Existence of a p-Optimal Propositional Proof System**  *(Theoretical computer science)*
> Determine whether there exists a Cook-Reckhow propositional proof system that polynomially simulates every other propositional proof system, including a polynomial-time translation of proofs.

**345 — Erdos-Szekeres Convex Polygon Problem (Happy Ending Problem)**  *(Combinatorics & discrete geometry)*
> Determine the exact least integer ES(n) such that every set of ES(n) points in general position in the plane contains n points in convex position; prove or disprove ES(n)=2^(n-2)+1 for every n >= 3.

---

When finished, state how many of the 31 records returned `NONE` and how many returned `NOT FOUND`. Those two counts are the headline result of this chunk.
