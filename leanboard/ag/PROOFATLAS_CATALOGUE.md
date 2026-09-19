# ProofAtlas `/open-problems/` — running catalogue and selection

**Purpose.** Problem *selection*, which this programme treats as a workstream separate from
the proof protocol. Built incrementally from screenshots, since proofatlas.ai is
egress-blocked from this container. Structure cross-checked against an independent
reader's guide ([Moatazg/proofatlas-notes](https://github.com/Moatazg/proofatlas-notes),
compiled 2026-09-13).

**Seen so far:** ranks 076–079, 165–169, 200–224, 479–482, plus expanded cards for
200, 250, 300 and 400. That is 41 of 482+.

---

## What the list is

Explicitly **rank-ordered**, 001 → 482+, one numbered card per problem with title,
one-sentence formal question, and an area tag. A status line appears on some cards
(rank 479 carries `Open · disputed claim`); most show none.

**The rank gradient is centrality, not difficulty.** Head: FPT vs W[1] (076), Abundance
(077), Chowla (078), Hadwiger (079) — load-bearing for whole fields. Middle: Held–Karp
gap (165), Furstenberg ×2×3 (166), L-space (167). Tail: Chern affine (479), Square Peg
(480), Liouville for stationary NS (482) — narrow, or famous but inconsequential. Square
Peg at 480 is the giveaway: very well known, ranked low because solving it moves little
downstream.

**This is the sort order that makes the tail heuristic safe.** Low rank means low
attention without implying high difficulty — the opposite of a progress- or
readiness-ordering, which would have made "end of list" a proxy for "hardest".

### The workspace-boundary hypothesis — RAISED, THEN REFUTED

I proposed that since the Problems list runs past 482 while the collaboration workspaces
number 243–268, workspaces must be allocated top-down by rank, putting the sweet spot at
the last ranks that still carry one — plausibly 200–260. I flagged it as a hypothesis with
a one-look test: open ranks 200, 250, 300, 400 and see which still show routes and tasks.

**The test was run. The hypothesis is wrong, and wrong in its premise.**

Expanding a card at rank 200, 250, 300 or 400 gives the same four sections every time:
**EXACT STATEMENT**, **WHY IT MATTERS**, **STATUS**, **SOURCES**. No routes. No dependency
graph. No prepared tasks. No eliminated routes.

So `/open-problems/` is not a ranked prefix of the workspaces — it is **a separate
artifact**: an encyclopedia of problem statements, not a research record. Whether any given
problem also has a `/collaboration/` workspace is an independent question, answerable only
by checking for a matching slug there. Rank tells you nothing about it.

Retracted in full. The target zone is not 200–260 on these grounds.

### What replaced it: the card fields are the filter

The expanded card carries three fields that are better selection signals than rank, and all
three are machine-readable.

**1. STATUS discriminates.** Rank 200 reads plain `Open`. Ranks 250, 300 and 400 all read
`Open · subcases solved`. Rank 479 read `Open · disputed claim`. So the status field marks,
in the site's own vocabulary, whether partial results exist — which is exactly the
"finite checkable sub-target" test, pre-computed and filterable. Three values seen so far;
there are likely more.

**2. WHY IT MATTERS contains a pre-written counterexample specification.** Verbatim:

> 250: "A counterexample would exhibit a compact set whose holomorphic hull escapes every
> compact region."
> 300: "A counterexample would establish a one-ended hyperbolic group lacking all the
> prescribed surface subgroups."
> 400: "A counterexample would be a convex body exceeding the simplex value; **neither
> outcome requires classifying all equality cases**."

Counterexamples are 2 of ProofAtlas's 9 advances and are the most agent-tractable outcome
available, because the deliverable is a finite object you exhibit and check. The card
states what that object is. Rank 400 goes further and says the sub-target is smaller than
the conjecture looks.

**3. SOURCES carry dates, so recency of activity is readable.** Rank 250 cites Annals 2012;
rank 400 cites arXiv:2407.01353v2, 27 May 2025. A problem whose newest source is thirteen
years old is in a different state from one with a paper from this year.

## Selection filter (revised after the refutation)

Grounded in ProofAtlas's own nine claimed advances, which are the only evidence of what
actually lands there. All nine are counterexamples, explicit-constant improvements, or Lean
formalizations of known arguments. **Not one is a conjecture resolved.**

1. **STATUS is `subcases solved` or `disputed claim`.** Mechanical. The first says a
   sub-target exists; the second says an audit target exists.
2. **WHY IT MATTERS names a finite counterexample object.** Mechanical enough to grep for
   "A counterexample would".
3. **A numeric target in the EXACT STATEMENT** — an explicit constant, ratio or exponent.
4. **Can an agent actually move it?** Not mechanical, and where most candidates die. A
   sharp constant you can search for numerically passes; a sharp constant gated behind
   Seiberg–Witten theory does not.

Rank is demoted to a tiebreaker: it buys neglect, nothing else.

## Catalogue, ranks 200–224

`N` = numeric target in statement. `C` = computational or finite sub-target available.

| # | Problem | Area | N | C | note |
|---|---|---|---|---|---|
| 200 | Effective Roth Theorem | NT & arith geom | ✓ | — | effectivity, not a bound to push |
| 201 | Kaplansky Zero-Divisor (torsion-free) | Algebra | — | — | |
| 202 | Polynomial Diameter Bound for Polytopes | Optimization | ✓ | ✓ | Kalai–Kleitman n^{log d}; incremental exponent + small-case search |
| 203 | Poly-time Quantum Dihedral HSP | Quantum info | — | — | |
| 204 | Serre's Conjecture II | Algebra | — | — | |
| 205 | Palis finite-attractor density | Dynamics | — | — | |
| 206 | Density of Hyperbolicity (complex polys) | Dynamics | — | — | |
| 207 | Brauer–Manin, Hasse-principle form | NT & arith geom | — | — | |
| 208 | Breuil–Mézard | NT & arith geom | — | — | |
| **209** | **Sharp Erdős Distinct-Distances in the Plane** | Combinatorics | ✓ | ✓ | **n/√log n vs proved N/log N; and Guth–Katz is a formalization target** |
| **210** | **Skolem Problem for Linear Recurrences** | Logic | — | ✓ | **decidability frontier is discrete: settled ≤ order 4, open at 5** |
| 211 | Rank One Abelian Stark | NT & arith geom | — | — | |
| 212 | Morton–Silverman Uniform Boundedness | NT & arith geom | ✓ | — | quantitative existence, no number to push |
| 213 | Parshin, higher K-theory / finite fields | NT & arith geom | — | — | |
| 214 | De Giorgi for Allen–Cahn, dims 4–8 | Analysis & PDE | ✓ | — | dimension range is discrete but each case is hard analysis |
| 215 | Moonshine Uniqueness (VOA form) | Algebra | ✓ | ✓ | central charge 24, finite classification flavour |
| 216 | All-Pairs Shortest Paths subcubic | Optimization | ✓ | — | O(n^{3−ε}); heavily watched in fine-grained complexity |
| 217 | UCT for separable nuclear C*-algebras | Algebra | — | — | |
| 218 | Poly-time PAC learning of DNF | TCS | — | — | |
| **219** | **Exact k-SAT threshold, k = 3** | Probability | ✓ | ✓ | **one real constant; decades of computer-assisted interval narrowing** |
| 220 | Shub–Smale τ-conjecture, integer zeros | TCS | ✓ | ✓ | universal constants a, c; τ-complexity is computable per polynomial |
| 221 | Equidistribution of Galois orbits, Shimura | Dynamics | — | — | |
| 222 | Vaught's conjecture | Logic | — | — | |
| **223** | **11/8-Conjecture, spin 4-manifolds** | Geom & topology | ✓ | — | **b₂ ≥ (11/8)\|σ\|; live frontier at 10/8+4** |
| 224 | Wall's Poincaré Duality Group | (partial card) | — | — | statement truncated in source |

---

## Expanded cards seen: 200, 250, 300, 400

| # | Problem | Area | STATUS | newest source |
|---|---|---|---|---|
| 200 | Effective Roth Theorem | NT & arith geom | `Open` | arXiv:1601.02243, Jan 2016 |
| 250 | Shafarevich universal-cover conjecture | Geom & topology | `Open · subcases solved` | Annals 176 (2012) 1545–1581 |
| 300 | Gromov's Surface Subgroup Question | Geom & topology | `Open · subcases solved` | Gardam–Kielak–Logan |
| 400 | **Strong Hyperplane Conjecture for Isotropic Constants** | Combinatorics & disc geom | `Open · subcases solved` | **arXiv:2407.01353v2, 27 May 2025** |

Note the contrast at 200: plain `Open`, no subcases marker, and its newest source is a
decade old. The field is doing real work.

---

## The new top pick: rank 400, Strong Hyperplane Conjecture

It passes all four criteria, and it is the first thing seen on this list that passes the
fourth.

**The statement is a sharp constant, per dimension.** For a compact convex body K ⊂ ℝⁿ with
X uniform on K, `L_K = (det Cov(X)/Vol_n(K)²)^(1/2n)`, and the claim is `L_K ≤ L_Δ_n` with
Δ_n a nondegenerate n-simplex and `L_Δ_n = (n!)^(1/n)/((n+1)^((n+1)/(2n))·√(n+2))`. Bodies
need not be symmetric or smooth.

**Why the sub-target is small.** [BACKGROUND, not from the card and not verified here:] the
*bounded* slicing problem — is L_K ≤ C for a universal C — was resolved through the Chen /
Klartag–Lehec line of work. What remains open is this **sharp** version, that the simplex is
extremal in each dimension. So the open part is a constant, not a growth rate. **Check this
before relying on it**; it is my background knowledge, not a sourced claim.

**Why an agent can move it.** A counterexample is a **finite, exhibitable object**: a convex
body — a polytope suffices — in some fixed low dimension whose L_K exceeds the stated
simplex value. L_K is computable from the body's volume and covariance matrix, which for a
polytope in low dimension is an exact rational computation. So the attack is a *search*:
enumerate or sample polytopes in dimensions 3–8, compute L_K exactly, compare against
L_Δ_n. Either a counterexample falls out, or the search bounds the region where one cannot
be.

That is the same shape as this programme's Erdős–Straus sieve work — exhaustive verified
search to 10^11, with the negative result stated as a bound rather than dressed up. The
card even pre-authorises the reduced target: *"neither outcome requires classifying all
equality cases."*

**Stated risks.** L_K computation is #P-hard in general, so dimension is the binding
constraint and the honest scope is small n. The simplex has been conjectured extremal for
decades and low dimensions are the first place anyone would have looked, so the prior on a
counterexample below n = 8 is low. The realistic deliverable is therefore a *verified
negative* — "no counterexample among this enumerated class up to dimension d" — which is
publishable in this programme's idiom and is exactly what the Erdős–Straus work produced.
The newest source (May 2025, "Isotropic constants and regular polytopes") suggests someone
is already computing in this space; read it before starting.

---

## The four from ranks 200–224, in order

### 1. Rank 209 — Sharp Erdős Distinct-Distances. *Already inside this programme.*

Guth–Katz proved N/log N; the sharp conjecture asks for n/√log n, so the target is an
explicit residual gap. Two separable sub-targets, and the second is the reason this ranks
first:

- close some of the √log gap — hard;
- **formalize Guth–Katz in Lean** — finite, valuable, and exactly the class that supplies
  2 of ProofAtlas's 9 advances.

**And this is P1's case 6.** The retrodiction corpus already carries a before/after
encoding of Erdős distinct distances (before: Szemerédi–Trotter-type incidence bounds,
N^{0.864}; after: Elekes–Sharir lift plus polynomial partitioning). So the programme can
attack it with machinery it has already built, and the attempt doubles as a test of
whether the board-change analysis is any use for *choosing* a target rather than
retrodicting one. Nothing else on the list has that property.

### 2. Rank 219 — Exact 3-SAT threshold. *The most computation-friendly item seen.*

A single real constant (≈4.267). Ding–Sly–Sun settled large k; k = 3 is open, and the
rigorous upper and lower bounds have been narrowed for decades by **computer-assisted**
arguments. An agent with compute can attempt an interval improvement and the result is
checkable. Low-hanging fruit is long gone, but an increment here is a definite, statable
result of precisely the shape ProofAtlas rewards.

### 3. Rank 210 — Skolem Problem. *A discrete frontier, not an asymptotic one.*

Decidability is settled for order ≤ 4 and open from order 5. That is a **bounded,
nameable sub-target** — "settle order 5" — rather than an epsilon to shave, and the logic
setting is formalization-friendly. Rare on this list: most items ask for an asymptotic or
a universal statement.

### 4. Rank 223 — 11/8-Conjecture. *Best numeric frontier, worst machinery.*

b₂ ≥ (11/8)|σ| for spin 4-manifolds, with the live frontier at the 10/8+4 theorem. Every
increment from 10/8 toward 11/8 is a definite result, which is the ideal shape. **Flagged
honestly: it fails criterion 4.** The machinery is Seiberg–Witten and equivariant stable
homotopy — no finite search, no computation an agent can run. Included because the *shape*
is right and the programme should know the difference between a problem with a number in
it and a problem an agent can move.

---

## Next

- **Read arXiv:2407.01353** ("Isotropic constants and regular polytopes", May 2025) before
  any search on rank 400. It is the newest source on the card and may already cover the
  low-dimensional enumeration.
- **Confirm the sharp-vs-bounded split** on the hyperplane conjecture from a source rather
  than from my background knowledge.
- **Enumerate the STATUS vocabulary.** Three values seen (`Open`, `Open · subcases solved`,
  `Open · disputed claim`). If the site exposes a filter on it, that plus a grep for
  "A counterexample would" is the whole selection instrument.
- **Cross-check `/collaboration/`** for slugs matching high-rank problems, to find out
  whether workspace coverage correlates with rank at all — the question my refuted
  hypothesis assumed the answer to.
