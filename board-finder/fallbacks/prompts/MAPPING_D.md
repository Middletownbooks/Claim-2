# Mapping layer, chunk D of 4 — Analysis, physics, quantum, logic, probability, applied

**Mixed. Quantum information and applied entries sometimes carry hard numeric records; analysis and logic entries usually do not.**

## What this is for

A 499-record corpus ranks open mathematical problems by editorial importance. It records each
problem in its **headline form** — *"determine the exact value"*, *"prove the conjecture"* — which
is almost always the hopeless form. What a working group can actually move is usually a **tracked
quantity underneath** the headline: a best-known bound, a record construction, a verification
height, a competitive ratio.

The corpus never names that quantity. Your job is to supply it, for 27 records.

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


**125 — Tarski's Exponential Function Problem**  *(Logic, foundations & set theory)*
> Determine whether the first-order theory of the real exponential field (R; 0, 1, +, *, exp, <, =) is decidable.

**126 — Unconditional Single-Prover Classical Verification of BQP Computations**  *(Quantum information & computation)*
> Determine whether every language L in BQP admits a polynomial-round interactive proof with only classical messages between a probabilistic classical polynomial-time verifier and a single honest uniform quantum polynomial-time prover, with completeness at least 2/3 and soundness at most 1/3 against e…

**152 — NP versus the Existential Theory of the Reals**  *(Applied & computational mathematics)*
> Determine whether every problem decidable in the existential theory of the reals (exists R) can be decided in nondeterministic polynomial time, i.e., decide whether NP = exists R.

**167 — Separation of P_R from NP_R in the Blum–Shub–Smale Model**  *(Applied & computational mathematics)*
> In the standard ordered-real Blum–Shub–Smale model, machines use finitely many built-in real constants, real-valued registers, exact field operations (+,-,multiplication,division where defined) and order/equality tests at unit cost. Inputs are finite real vectors and size is vector length. Let P_R b…

**172 — Polynomial-Time Quantum Algorithm for Symmetric-Group Hidden Subgroups**  *(Quantum information & computation)*
> Give a polynomial-time quantum algorithm that recovers a subgroup hidden by an oracle over the symmetric group S_n.

**174 — Inhomogeneous Landau–Coulomb Global Regularity (HST All-Moment Data)**  *(Analysis & PDE)*
> Fix a positive physical constant a. On [0,infinity) times R^3_x times R^3_v consider the classical Landau equation (partial_t+v dot grad_x)f=Q(f,f), where Q(f,f)=div_v integral_{R^3} A(v-w)[f(t,x,w) grad_v f(t,x,v)-f(t,x,v) grad_w f(t,x,w)]dw and A(z)=a |z|^(-1)(I-z tensor z/|z|^2) for z!=0. For eve…

**176 — Soliton Resolution for the Focusing Energy-Critical Wave Equation without Radial Symmetry**  *(Analysis & PDE)*
> For d in {3,4,5}, consider the real focusing wave equation u_tt-Delta u=|u|^(4/(d-2))u on R^d, with energy data in dot-H1 x L2 and the usual strong energy solution on [0,infinity), uniformly bounded in that norm. Assertion: every such solution has, for all t->infinity, a decomposition of (u,u_t) int…

**183 — Smooth anisotropic Calderón uniqueness from full boundary data**  *(Analysis & PDE)*
> For every compact connected smooth manifold M of dimension n>=3 with smooth nonempty boundary and every pair of smooth Riemannian metrics g1,g2 on that same M, let Lambda_gj f be the outward metric-unit normal derivative of the unique solution of Delta_gj u=0 with u|boundary=f. If Lambda_g1=Lambda_g…

**191 — Global Existence of Classical Solutions to the Relativistic Vlasov-Maxwell System**  *(Analysis & PDE)*
> Prove or disprove that the Cauchy problem for the three-dimensional relativistic Vlasov-Maxwell system has a global classical solution (f,E,B) for every sufficiently regular finite-energy initial datum.

**205 — Polynomial-Time Quantum Algorithm for the Dihedral Hidden Subgroup Problem**  *(Quantum information & computation)*
> Find a polynomial-time quantum algorithm with poly(log N) operations and space for the hidden subgroup problem in dihedral groups D_N.

**208 — Density of Hyperbolicity for Complex Polynomials**  *(Probability, ergodic theory & dynamics)*
> For each complex polynomial T of degree at least two, determine whether T can be approximated by polynomials of the same degree all of whose critical points converge under iteration to attracting periodic cycles, that is, whether hyperbolic polynomials are dense in the space of complex polynomials o…

**212 — Skolem Problem for Linear Recurrence Sequences**  *(Logic, foundations & set theory)*
> Decide algorithmically, given an integer (or algebraic) linear recurrence sequence, whether it has a zero term.

**215 — De Giorgi Conjecture for the Allen-Cahn Equation in Dimensions 4 to 8**  *(Analysis & PDE)*
> For each ambient dimension N with 4 <= N <= 8, prove that every bounded entire C^2 solution u from R^N to (-1,1) of the Allen-Cahn equation Laplacian u = u^3 - u that is strictly monotone in one direction is one-dimensional, that is, u(x) = g(a . x) for some unit vector a and one-variable profile g.

**221 — Exact satisfiability threshold for random k-SAT for small k (k = 3)**  *(Probability, ergodic theory & dynamics)*
> In the uniform random 3-SAT model, choose a 3-CNF formula with n variables and m clauses uniformly from formulas whose clauses contain three distinct literals. Determine the exact constant r_3 such that, as n tends to infinity with m/n tending to r, satisfiability has probability tending to 1 for r …

**223 — Vaught's conjecture**  *(Logic, foundations & set theory)*
> Prove or disprove that for every complete theory T in a countable first-order language, the number I(T,aleph_0) of pairwise nonisomorphic countable models of T is either at most countable or exactly 2^{aleph_0}.

**235 — Zauner's Conjecture: Unrestricted Complex SIC Existence in Every Dimension**  *(Quantum information & computation)*
> Decide whether for EVERY integer d>=2 there exist d^2 unit vectors v_1,...,v_(d^2) in the standard complex Hilbert space C^d with |<v_i,v_j>|^2=1/(d+1) whenever i!=j. Their complex lines are distinct. Equivalently, their rank-one projectors P_i=v_i v_i^* have sum_i P_i=d I_d and define SIC-POVM elem…

**253 — Witten's Asymptotic Expansion Conjecture for SU(2) WRT Invariants**  *(Mathematical physics)*
> For every closed oriented three-manifold Y, let WRT_k(Y) be the SU(2) Witten-Reshetikhin-Turaev invariant at level k-2 in the standard compact-gauge normalization WRT_k(S^3)=1. For every value S in CS(Y), the set of Chern-Simons actions modulo Z of flat SU(2) connections, there should exist a formal…

**266 — Global Regularity of the 2D Inviscid Boussinesq Equations**  *(Analysis & PDE)*
> Determine whether all smooth, finite-energy solutions of the two-dimensional inviscid Boussinesq equations (velocity coupled to a temperature or density by buoyancy, without dissipation) on R^2 remain smooth for all time, or whether finite-time singularity formation occurs for some C^infinity initia…

**269 — Equivalence or Strict Containment of QMA and QMA(2)**  *(Quantum information & computation)*
> Determine whether QMA(2)=QMA in the ordinary unrelativized, uniform polynomial-time quantum verification model. For a promise problem (Y,N), QMA(2) allows two polynomial-size quantum witnesses, required to be a product across the two prover registers: each YES input has some such witness accepted wi…

**282 — Exact Unassisted Quantum Capacity of the Qubit Depolarizing Channel**  *(Quantum information & computation)*
> For every p in [0,1], determine the exact unassisted quantum capacity Q(D_p) of the memoryless qubit channel D_p(rho)=(1-p)rho+pI/2. Capacity is the supremum of asymptotically achievable rates in qubits per channel use for quantum-information transmission with vanishing error and arbitrary block cod…

**294 — Lions' Open Problem on Small-Time Global Exact Null Controllability of the Navier-Stokes Equations with Dirichlet Boundary Conditions**  *(Applied & computational mathematics)*
> Let Omega be a bounded domain, Gamma a nonempty open subset of its boundary, and T > 0. For every divergence-free initial velocity u_0 in the natural L^2 phase space, does there exist boundary data f supported on Gamma and a weak solution of the incompressible Navier-Stokes equations with u=f on Gam…

**306 — Planar homogeneous Mumford–Shah local-structure conjecture**  *(Analysis & PDE)*
> Let Omega be any open subset of R^2. Consider every reduced absolute local minimizer (u,K) of E0(u,K;U)=integral_{U minus K}|grad u|^2 dx+H^1(K intersect U): K is relatively closed and countably 1-rectifiable, u is real and in W^{1,2}_loc(Omega minus K), E0 is finite on each relatively compact open …

**320 — Positivity Problem for Linear Recurrence Sequences**  *(Logic, foundations & set theory)*
> Select arbitrary finite order k>=1, rational constant coefficients a_1,...,a_k and rational initial values u_0,...,u_(k-1), each finitely encoded in binary, with u_(n+k)=sum_(i=1)^k a_i u_(n+k-i) for all n>=0. The assertion is that a total algorithm exists which, for EVERY such input, halts and corr…

**326 — Calderón uniqueness for bounded measurable real isotropic conductivities**  *(Analysis & PDE)*
> For every integer n>=3, every bounded connected Lipschitz domain Omega in R^n and every pair of real scalar conductivities gamma_1,gamma_2 in L-infinity(Omega) with 0<c<=gamma_j<=C<infinity almost everywhere for some constants c,C, equality Lambda_gamma_1=Lambda_gamma_2 of the full weak Dirichlet-to…

**328 — Discontinuity of the q-State Potts Phase Transition on Z^d for d >= 3 and q >= 3**  *(Mathematical physics)*
> Prove that the order/disorder phase transition of the nearest-neighbor q-state Potts model on Z^d with d >= 3 is discontinuous (first-order) for every integer q >= 3.

**344 — Koebe circle-domain uniformization conjecture**  *(Analysis & PDE)*
> For every nonempty connected open domain Omega of the Riemann sphere, there exist a circle domain D in the Riemann sphere and a conformal homeomorphism Omega -> D. A circle domain means a nonempty connected open set each of whose complementary components is a closed round disk or a point. Allow arbi…

**346 — Corona problem for the unit polydisc**  *(Analysis & PDE)*
> For every integer n>=2 and every finite integer m>=1, let f_1,...,f_m be scalar bounded holomorphic functions on the unit polydisc D^n={z in C^n: |z_k|<1 for all k}. If inf_{z in D^n} sum_{j=1}^m |f_j(z)|>0, then there exist scalar bounded holomorphic g_1,...,g_m on D^n such that sum_{j=1}^m f_j g_j…

---

When finished, state how many of the 27 records returned `NONE` and how many returned `NOT FOUND`. Those two counts are the headline result of this chunk.
