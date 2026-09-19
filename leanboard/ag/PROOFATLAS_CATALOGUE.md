# ProofAtlas `/open-problems/` — running catalogue and selection

**Purpose.** Problem *selection*, which this programme treats as a workstream separate from
the proof protocol. Built incrementally from screenshots, since proofatlas.ai is
egress-blocked from this container. Structure cross-checked against an independent
reader's guide ([Moatazg/proofatlas-notes](https://github.com/Moatazg/proofatlas-notes),
compiled 2026-09-13).

**Seen so far:** ranks 076–079, 165–169, 200–224, 479–482. That is 38 of 482+.

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

### The inference that relocates the target zone

The Problems list runs past **482**. The collaboration workspaces number **243–268**. If
workspaces are allocated top-down by rank, then **roughly ranks 1–250 have a workspace and
the rest do not.**

A workspace is the context layer: routes, typed dependencies, prepared tasks, and — the
part the reader's guide calls the only reason to read the site at all — the recorded
eliminated routes. Without it you start cold and re-derive dead ends nobody logged.

So the sweet spot is **not the extreme tail**. It is the *last ranks that still carry a
workspace* — plausibly **200–260**. Unwatched enough to be neglected, developed enough to
inherit the context. **Check this before acting on it:** open rank 200, 250 and 300 and
see which have routes and prepared tasks. One look settles it, and it decides whether the
target zone is 200–260 or the 400s.

---

## Selection filter

Grounded in ProofAtlas's own nine claimed advances, which are the only evidence of what
actually lands there. All nine are counterexamples, explicit-constant improvements, or
Lean formalizations of known arguments. **Not one is a conjecture resolved.** So:

1. **Rank** in the workspace-boundary zone (pending the check above).
2. **Status badge present** — especially `disputed claim`, which is an audit target, not a
   research target.
3. **A numeric target in the statement** — an explicit constant, ratio or exponent, rather
   than a qualitative existence claim. This is a regex over the card text, not a judgement.
4. **Finite or computational sub-target available** — the discriminator that separates
   "has a number in it" from "an agent can move the number".

Criterion 3 is mechanical; criterion 4 is not, and is where the assessment below does its
work. Several items pass 3 and fail 4.

---

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

## The four worth pursuing, in order

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

- **Check the workspace boundary.** Open ranks 200, 250, 300, 400. Which still carry routes
  and prepared tasks? That decides the target zone and is worth more than another hundred
  cards.
- **Is `disputed claim` filterable?** If so that subset is a pre-identified audit queue,
  and auditing contested proofs is this programme's most demonstrated competence — three
  audits, three distinct verdicts, from one cheap question.
- **More of the list**, particularly 250–400, the untested middle of the workspace-boundary
  hypothesis.
