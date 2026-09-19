# ProofAtlas `/open-problems/` — running catalogue and selection

**Purpose.** Problem *selection*, which this programme treats as a workstream separate from
the proof protocol. Built incrementally from screenshots, since proofatlas.ai is
egress-blocked from this container. Structure cross-checked against an independent
reader's guide ([Moatazg/proofatlas-notes](https://github.com/Moatazg/proofatlas-notes),
compiled 2026-09-13).

**Seen so far:** `/collaboration/` bottom-ten picks, plus `/open-problems/` ranks 076–079, 165–169, 200–224, 479–482, plus expanded cards for
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

### Correction to that refutation, from the parallel session — and then the real answer

The parallel session narrowed my refutation and was right to. I argued `/open-problems/`
is not a ranked prefix of the workspaces *because the expanded cards show no routes*. That
argument does not work: **a card and a workspace are different pages**, so a problem can
have a workspace and still have a card with no routes on it, because routes are not where
cards put things. What the four expanded cards actually establish is narrower — that
`/open-problems/` has a uniform card format and is a separate artifact. Worth having, less
than I claimed.

**The allocation question is now settled directly, by better evidence than either of us
had.** The top-500 list can be **filtered to those with research attached: 123 of 500,
roughly a quarter, distributed relatively evenly through the ranked list.**

So coverage is **scatter, not a band**. Rank does not predict whether a problem has
research. My sweet-spot reasoning was wrong, my refutation of it was wrongly argued, and
the filter supplies the correct argument for both.

The practical consequence is better than either analysis: **"tail-ranked AND has research"
is directly obtainable** — apply the filter, read the bottom. No inference needed.

### The competition axis runs opposite in the two workstreams

Also from the parallel session, and worth encoding here because it governs how the
line-count metric is used:

- **Harvesting boards** (their workstream) consumes an incumbent mechanism plus a record of
  what leaked. Other agents' failures are the *input*. So harvest where the work is
  **thickest** — a heavily-worked workspace has more recorded dead ends.
- **Claiming a result** (this workstream) is a race. Another agent arriving first is a
  total loss. So claim where the work is **thinnest**.

Same metric, opposite directions. Investigation lines per workspace is the readable proxy
either way: ~2,900 average, Erdős–Hajnal at 24,107, Berlekamp Domineering at 60.

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

## Rank 400 read against its source: Kipp, arXiv:2407.01353v2

The card's cited source was obtained in full. It confirms one thing I flagged as unverified
and **refutes the attack I proposed**.

### Confirmed

My background claim was that the *bounded* slicing problem is resolved and only the sharp
version remains. Kipp §1, verbatim: *"In December 2024, the isotropic constant conjecture
was finally proven by Klartag and Lehec [13], building on a preprint by Guan [7]."* The
open part is (1.1), `L_K ≤ L_Δn`, and Kipp's formula for L_Δn is character-for-character
the one on the ProofAtlas card. The card is a faithful transcription. Promote the claim
from background to sourced.

Constants checked here: `1/√12 = 0.288675`; `L_Δn` rises from 0.288675 at n=1 to 0.352 at
n=12; Kipp's asserted `L_{C*_n} ≤ 1/√12` holds at every n tested.

### Refuted: enumerate-and-compute does not work

I proposed sampling or enumerating polytopes in dimensions 3–8, computing L_K exactly, and
comparing against L_Δn. **That attack is dead, and the paper says why.**

Theorem 3.4 (Campi–Colesanti–Gronchi): along any RS-movement, `t ↦ L²ⁿ_{K_t}` is
**convex** — strictly so when the speed function is non-affine. *"In particular, every
local maximizer of the isotropic constant is RS-indecomposable."*

L_K is a convex function along these deformations. So from almost any polytope you can move
and strictly **increase** L_K: generic polytopes are RS-decomposable and are therefore not
even local maxima. A search over sampled bodies is hill-climbing on a convex function whose
maxima sit at extreme points of a heavily constrained set. It finds nothing.

Kipp then closes the obvious classes outright. Theorem 1.2: a polytopal local maximizer
with a **simplicial vertex** is a simplex. Theorem 2.7: one whose ridges are all affine
reflectors is a simplex. Theorem 1.3: a centrally symmetric local maximizer with a
simplicial vertex is a cross-polytope. Remark 2.1: polytopal local *minimizers* do not
exist at all.

Retracted. This is the second hypothesis of mine this exchange has killed; the pattern is
that positional and volumetric heuristics keep losing to reading the source.

### What the paper hands over instead — three real targets

**(a) Zonotopes with n+2 generators.** Kipp's §6 settles n+1: Lemma 6.4 shows every such
zonotope is affinely equivalent to `C_n + [−y, y]` with `y ∈ [0,1]ⁿ` — an explicitly
parameterized, compact, n-dimensional family. Proposition 6.1 gives the maximizer (the
cube) and 6.5 the minimizer (`Q_n`, a hexagon at n=2, a rhombic dodecahedron at n=3). The
**n+2 case is the visible next step**: still finite-dimensional, still compact, and the
machinery — RS-movements plus reduction to the planar case — is laid out in full. Bounded,
with a worked precedent. This is the best-shaped target on the list so far.

**(b) Narrow the zonoid gap.** Kipp §1: the isotropic constant conjecture *is* known for
zonoids [18], and *"it seems that the best known upper bound is L_Z ≤ 1/2"* against a
conjectured `1/√12`. That is a factor of **√3 ≈ 1.732** between proved and conjectured, in
a class where the qualitative question is already settled. Explicit constants, restricted
class, incremental — the exact profile of ProofAtlas's own advances.

**(c) Formalize §6 in Lean.** Propositions 6.1 and 6.5 are self-contained and largely
computational. Formalization of a known argument is one of the three classes that actually
lands there (2 of their 9).

### What the paper also says about its own limits

*"We emphasize that all theorems up to this point are hypothetical in the sense that it is
unknown whether polytopes with the respective properties actually exist. In particular,
Theorem 1.4 yields no upper bound on isotropic constants of zonotopes."* §6 opens by naming
two reasons: the classes are not closed under Banach–Mazur distance, and the first-order
condition (2.3) only holds for maximizers within a fixed facet count. That is why §6 moves
to a **closed** subclass — and it is why (a) above is the tractable direction and the
structure theorems are not.

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

## The research / collaboration page — the layer that carries tasks

The bottom ten "picks" from `/collaboration/` were obtained. **This resolves the two-artifact
confusion: the selection instrument belongs here, not on `/open-problems/`.** These cards
carry what the problem cards lack —

- **`PRIORITY OPEN BRIDGE · NEXT TASK`**, a single stated next step in the site's own words;
- **investigation-line count**, the neglect metric;
- selected mapped statements, open-question count, and a progress bar;
- sometimes an `EVIDENCE` line and separate `INDEPENDENT CHECKS STILL OPEN` block.

Line counts across these ten run 60 to 1.3k, against the ~2,900 average the reader's guide
reports over 268 workspaces — consistent with these being bottom picks.

| workspace | area | lines | stated next task |
|---|---|---|---|
| **Berlekamp Domineering-Temperature** | comb. game theory | **60** | *(see below — it asks for replication, not research)* |
| Elliptic-Curve DLP challenge instance | comp. number theory | 900 | obtain source/notebook/API evidence for how the private scalar was sampled |
| Multiplicative persistence | digit dynamics | 1.0k | prove I¹⁰(Z)=∅ for the entire infinite positive zero boundary Z |
| Minimum Overlap Problem | signed graphs, discrepancy | 1.1k | combine row and column one-point tests without double-counting shared entries |
| Harary–Hill | crossings in K_n drawings | 1.1k | prove global accessibility through compatible nonincreasing moves |
| Kobon triangle | line arrangements | 1.1k | prove a uniform Bellman potential on the complete reachable state domain |
| Mutually unbiased bases, dim 6 | Hadamard matrices | 1.2k | exclude arbitrary nonsymmetric quartets, beyond triples with a shared conjugation |
| Markov uniqueness | Diophantine | 1.2k | exclude every proper nonempty zero subsum of the marked sequence 4g_i |
| Nakai conjecture | comm. algebra | 1.2k | establish the missing filtered presentation for the logarithmic fields |
| McMullen projective convex-position | real proj. geometry | 1.3k | produce a real full-spark zero-hole construction continuing in every rank |

---

## The pick: Berlekamp's Domineering-Temperature Conjecture

Every signal on the site points at this one, and it is the first candidate in this whole
exercise that survives the convexity check — because **there is no search and no
optimization in it at all.**

**It is their weakest-evidence claim.** The reader's guide's transcription of `/advances/`
lists nine claimed results. Eight are "Lean checked" or "Accepted in ProofAtlas". The ninth:

> Combinatorial game theory | Rectangle-reachable Berlekamp counterexample | **Unverified
> manuscript; adversarial audit attached**

That is the only one of the nine without a machine check behind it.

**The site is asking, in writing, for exactly what this programme does.** The card carries a
dedicated block:

> `INDEPENDENT CHECKS STILL OPEN` — **Specialist review and unrelated replication**

**It is 60 investigation lines.** An order of magnitude below every other card here, and
roughly 1/50th of the site average. Nobody has worked it.

**The claim is finite, exact, and numerically specific.** Tagged `EXACT FINITE COMPUTATION`.
Verbatim: *"Lech Mazur's manuscript gives a rectangle-reachable 28-cell Domineering position
with exact game {17/8 | -2+*} and temperature 33/16 > 2."* So the replication task is
completely determined: reconstruct that 28-cell position, compute its game value and
temperature independently, and check whether they equal {17/8 | -2+*} and 33/16.

**There is a second, sharper audit hook in the card's own hedging.** It says the Lean
development kernel-checks the board–target equality, the thermograph, a 30-move replay and
the existential statement *"through its narrow HasValueTemperature interface"*. That phrase
is doing real work. The question an audit should ask first is not whether Lean accepted the
proof — it did — but **whether that narrow interface states what the conjecture needs**.
Alignment between a formal statement and the informal claim is precisely what the site says
a Lean check does *not* establish, and it is the failure mode this programme has found three
times (Ghermoul, auro-zera, Guo–Fang–Lu).

**Two outcomes, both publishable.** Replication succeeds → the site's one unverified advance
gains independent confirmation, which is worth more to them than another partial result.
Replication fails, or the interface does not capture the claim → that is a finding of the
exact kind this programme already has a track record of producing.

**Stated risks.** Domineering game values are exactly computable but the state space grows
fast; 28 cells is large enough that a naive implementation will not finish, and a correct
one needs canonical-form simplification and transposition tables. The temperature
computation needs thermograph arithmetic on loopfree games, which is standard but fiddly.
And "rectangle-reachable" is a precise condition — get it wrong and the replication
disproves nothing. None of these is a research obstacle; all are implementation care.

### Runners-up

**Multiplicative persistence** (1.0k lines) — elementary, digit-based, highly computational,
and the next task is a precisely stated set-emptiness claim. Best of the rest.

**Markov uniqueness** (1.2k) — elementary statement, rich computational structure in the
Markov tree, precise next task.

**Kobon triangle** and **Harary–Hill** (1.1k each) — both report *exact finite cases*, which
is where an agent with compute can work.

### One flag

The **Elliptic-Curve DLP challenge instance** is not a mathematics task. Its stated next step
is *"obtain exact source, notebook, archive or API evidence for how the private scalar was
sampled"* — provenance archaeology, because a properly sampled instance is hard by
construction and a badly sampled one is the only opening. That is a sound judgement by
whoever wrote the workspace, but it means there is no mathematics to do, and it makes the
item a cryptanalysis target rather than a conjecture. Published challenge instances exist to
be attacked, so this is legitimate; anyone picking it up should just be clear which activity
they are in.

---

## The filtered tail — 123 of 500 have research, and here is its bottom

Twenty cards from the bottom of the **research-attached** filter. This is the target zone,
obtained directly rather than inferred.

| rank | problem | area | status |
|---|---|---|---|
| 363 | Four Exponentials Conjecture | NT & arith geom | *cluster: exponential transcendence · 3 problems* |
| 368 | Thomson problem | math physics | |
| **372** | **Whitehead Asphericity** | geom & topology | **Open · disputed claim** |
| 382 | Pólya's Conjecture for Dirichlet Eigenvalues | analysis & PDE | explicit (2π)²(k/(ω_d V))^(2/d) |
| 384 | Cherlin–Zilber Algebraicity | logic | |
| 393 | Projective planes of non-prime-power order | coding & optimization | order 12 the open case |
| 397 | Finiteness of central configurations, n ≥ 4 | math physics | |
| 403 | Frankl Union-Closed Sets | combinatorics | |
| **406** | **Yau's First Eigenvalue for Minimal Hypersurfaces** | geom & topology | **Open · disputed claim** |
| 415 | Greenberg's Conjecture, Iwasawa invariants | NT | *cluster: 2 problems* |
| 421 | GNRS Conjecture | TCS | |
| 423 | Zariski Cancellation (char 0, dim ≥ 3) | algebra | |
| 426 | Maximal MUBs in composite dimensions | quantum info | "can dimension six support seven?" |
| **429** | **Lovász, Hamiltonian paths in vertex-transitive graphs** | combinatorics | **Open · disputed claim** |
| 454 | Hadwiger–Boltyanski Illumination | combinatorics | 2ⁿ sources |
| 456 | Andrews–Curtis | algebra | |
| 457 | Campana–Peternell | geom & topology | |
| 474 | Quillen, posets of elementary abelian p-subgroups | algebra | |
| **480** | **Chern, Euler characteristic of affine manifolds** | geom & topology | **Open · disputed claim** |
| 482 | Square Peg (Toeplitz) | geom & topology | |

**Four `disputed claim` items in this tail alone.** That confirms the subset is real and
concentrated where the filter puts us. *(Written before I read one. See the retraction
below: the badge does not mean what I took it to mean, so this is a set of four cards to
open, not a pre-identified audit queue.)*

Three incidental findings:

- **Ranks drift.** Chern read 479 in the earlier screenshots and 480 here; Square Peg moved
  480 → 482. Do not hard-code rank; key on title.
- **A problem can appear in both layers.** Rank 426 (MUBs in composite dimensions) is the
  same topic as the `/collaboration/` card "Mutually unbiased bases in dimension six". That
  is direct evidence on the membership question, and it points the same way as the filter.
- **Some cards carry cluster links** — "Exponential transcendence · 3 problems", "Iwasawa
  invariants · 2 problems". So the list has a topic-grouping layer too.

### RETRACTED — "the pick from this tail: rank 429, Lovász on vertex-transitive graphs"

**The claim below is withdrawn. It was wrong, and it was wrong in a way I should have
caught before writing it.** I asserted, in the words committed to this file:

> *"A disputed claim here is a specific claimed counterexample — a finite vertex-transitive
> graph asserted to have no Hamiltonian path. Adjudicating it is completely determined:
> construct the graph, verify vertex-transitivity, run an exact Hamiltonicity check. No
> search over a space, no optimization, no convexity trap. Second Berlekamp-shaped target
> found."*

The research attached to rank 429 is **Bucić, Christoph, Pokrovskiy and Steiner, *Towards
the Lovász conjecture via sublinear expanders*, arXiv:2606.09742v2 (27 July 2026)**. It is
a **positive lower-bound paper by four academics**, not a counterexample. Its result is

  `ℓ(n) ≥ n^{2/3 − o(1)}`

where `ℓ(n)` is the longest path guaranteed in an `n`-vertex connected vertex-transitive
graph, improving the chain Babai `Ω(√n)` → DeVos `n^{3/5}` → Groenland et al `n^{13/21}`
→ Norin et al `n^{9/14}`. There is no claimed object to construct and no Hamiltonicity
check to run. **The "second Berlekamp-shaped target" claim is dead.**

**What the error was.** I read a status badge reading `Open · disputed claim` and inferred
its *content* — that a disputed claim must be a claimed counterexample — without opening
the card. Everything downstream ("finite and checkable", "completely determined", "no
convexity trap") was deduction from that single unchecked inference, stated with the
confidence of a fact. The failure is not that the inference was unlikely; it is that I
never marked it as an inference. This is the same defect as the rank-400 failure in a
different costume: there I reasoned past a property of the object (convexity) I had not
tested; here I reasoned past the object itself.

**This is the third hypothesis of mine refuted in this exercise** — after the
workspace-boundary band (retracted by me, then narrowed further by the parallel session as
wrongly argued, then settled against me by the user's filter data) and the rank-400
enumerate-and-compute attack (refuted by Thm 3.4 of its own source). Recording the count
is the point: the retrospective instrument is measuring me as much as anything else, and
three for three on the speculative picks is the number that belongs in the record.

**Do not re-use the badge taxonomy.** Until a `disputed claim` card has been opened and
read, the only thing the badge licenses is "the card says something is contested." It does
not license "there is a claimed counterexample," it does not license finiteness, and it
does not license checkability. The other three — 372 Whitehead, 406 Yau, 480 Chern — are
now **unassessed**, not "needing a hard argument read": that characterization was built on
the same inference and falls with it.

### What rank 429 actually is: a dated, self-declared board-exhaustion instance

The item's real value is different from and, for the programme, probably larger than the
audit target I thought I had. The paper states that it **hits a natural barrier of the
existing methods**, and the arithmetic confirms it. Both available routes cap at exactly
2/3, from opposite directions:

**Route A — longest path transversals.** With `lpt(G)` the longest-path transversal number,
the standard reduction gives `ℓ ≥ n/lpt(G) − 1`. If `lpt(G) ≤ ℓ^β` then

  `ℓ ≥ n/ℓ^β − 1`  ⟹  `ℓ^{1+β} ≳ n`  ⟹  `ℓ ≥ n^{1/(1+β)}`.

This paper's Theorem 1.2 achieves `β = 1/2`, giving `1/(1 + 1/2) = 2/3` **exactly**. The
exponent improves only as β → 0, and `β = 0` — `lpt` bounded by an absolute constant — is
**Gallai's question, asked in 1966 and open ever since**. So the ceiling does not sit at an
arbitrary technical limit; it sits precisely on a sixty-year-old open problem.

**Route B — Smith's conjecture, local form.** If `s(k) = O(k^α)`, the reduction yields

  `ℓ(n) ≥ Ω(n^{(1+α)/(1+2α)})`,

which is *decreasing* in α, so one wants α small — but the trivial bound `s(k) ≥ k` forces
`α ≥ 1`. The best conceivable α = 1 gives `(1+1)/(1+2) = 2/3` **exactly again**. And the
current state of the art, Ma–Zhao's `α = 3/2`, gives only `(1 + 3/2)/(1 + 3) = 5/8 = 0.625`
— *worse* than route A already delivers.

Two independent routes, one capped at 2/3 by a 1966 open problem and the other capped at
2/3 even under its own best possible hypothesis: that is a board on which the accessible
moves have been played out and the next move requires a new piece. **That is exactly the
shape the programme is trying to detect** — and here it is declared by the authors
themselves, in a dated paper, in a field with no contamination from this project.

Arithmetic checked in `leanboard/ag/lovasz_exponent_barrier.py` — 12/12, including the
monotonicity of each route in its parameter, the four earlier links of the chain all falling
below 2/3, and the coincidence of the two caps.

**Therefore: rank 429 is a candidate for the prospective arm, not the retrospective corpus.**
The prospective arm is the only uncontaminated instrument I have; a July 2026 paper whose
own authors name the barrier is a legitimate entry for it. Filed as such.

### Two observations to carry forward

**The AI-role disclosures point in opposite directions.** This paper states *"ChatGPT 5.6
was used to proofread this paper. All of the ideas and writing are due entirely to the
authors."* Mazur's Domineering paper, replicated in `leanboard/ah/`, discloses a
substantial AI role. Two 2026 papers, two opposite postures on the same question, both
attached to ProofAtlas items. Any claim this project makes about AI contribution rates in
the literature has to survive that spread; a single convention cannot be assumed.

**"Research attached" is not yet defined.** arXiv:2606.09742 is ordinary independent
literature by four academics — nothing ProofAtlas produced. If the filter's 123-of-500
counts links to external papers, then "research attached" measures *what the site's curators
found*, not *what the site generated*, and the even distribution through the ranking is
evidence about curation coverage rather than about where effort has been spent. That
distinction changes what the filter can be used for, and it is currently unresolved. **Open
question; do not build on either reading until a card settles it.**

*Partial answer, 2026-09-19, from the user, marked as their reading of the site and not as
a settled fact:* ProofAtlas is a **read-only beta** as far as collaboration goes, and the
problems and their status are **drawn from independent research, probably AI-rated or
AI-compiled**. If that holds, the second reading above is the right one, and three things
follow. (1) The 123-of-500 filter measures **curation coverage**, not effort spent — it is
evidence about the compiler's reach, and the even spread through the ranking is what one
would expect from a compiler working the whole list rather than from researchers
concentrating anywhere. (2) There is **no site-generated work to audit**, so the
retrospective audit-target hunt on this site is largely closed; Berlekamp/Mazur was findable
because the *paper* requested replication, not because ProofAtlas produced anything. (3) What
the site is actually good for is what rank 429 turned out to be: a **dated, compiled index of
where problems stand**, which is the cheapest available way to find board-exhaustion
instances. Re-scope accordingly — index, not workshop. Still to confirm against a card.

### Two others worth naming

**403 Frankl union-closed** — I called this a **live numeric frontier** with "multiple groups
actively pushing," the bound-improvement class exactly. *Corrected 2026-09-19.* It is a
**second barrier instance**, and the correction runs in the same direction as rank 429: I
described movement where the practitioners describe a ceiling.

*Provenance: web-search snippets, September 2026, **not verified against a paper**. Flagged
because I have relayed a snippet wrongly before (the Shannon five-vs-six-vertices error).
Everything in this paragraph needs a transcript before it is used.*

- The constant I recorded is **stale, not merely unsourced**. `(3−√5)/2 ≈ 0.381966` was a
  waypoint, not the front. Sawin showed it can be beaten; Yu and Cambie evaluate the convex
  combination of the i.i.d. and max-entropy couplings at **≈ 0.38234** (one snippet says
  0.38237). Gap to the conjectured `0.5` is therefore **≈ 0.1177**, not 0.118 from 0.381966.
- **The barrier is named by the practitioners, with a stated mechanism.** Progress "appears
  to require new ideas beyond the current entropy-based coupling approaches," and the
  specific obstruction is **single-letterization**: Rényi entropies do not satisfy the chain
  rule the way Shannon entropy does, so the multi-letter bound cannot be collapsed to a
  single-letter one. That is a technical wall with a name, not a frontier.

**This breaks my predicate, and I should say so before repairing it.** The rank-429 detector
was *two independent routes capping at the same exponent, with one cap sitting on a named
open problem*. Frankl does not have that form at all: it is **one** method, capped by a
**failure of an algebraic identity**, at a **constant** rather than an exponent. Two
instances, two different barrier mechanisms.

The tempting move is to widen the predicate to "a named obstruction the practitioners state
themselves, with a numerical ceiling attached." **That is how a predicate becomes
unfalsifiable.** Nearly every discussion section names a limitation; if the widened version
fires on all of them it measures rhetoric, not mathematics. So the widened form is recorded
here as a *hypothesis to be tested against controls*, not as an instrument — and the control
class (advances that came without a declared wall) is now the binding requirement before
either version can be used for anything.

**Not resolved, as far as search can tell.** A January 2026 preprint claims an algorithmic
proof; other 2026 sources still describe the conjecture as open, and one September 2026
source calls it wide open. Claimed proofs of Frankl are unusually frequent and the base rate
of correctness among them is low, so "a claimed proof exists" and "the problem moved" are
different statements. If ProofAtlas still ranks it `Open`, that is consistent with the
claimed proof not having been accepted. **Worth checking on the site; do not assume either
way from this note.**

**393 projective planes of order 12** is the instructive negative. It is genuinely finite —
and infeasible. Order 10 was ruled out by Lam et al. in 1989 at a cost of thousands of
CPU-hours, on a 111×111 incidence problem; order 12 is 157×157 and vastly larger. **This is
criterion 4 failing on scale rather than on kind**, and it is worth keeping in the file as
the example that distinguishes the two failure modes: rank 400 failed because sampling
cannot find the maximum of a convex functional; rank 393 fails because the search is the
right shape and too big.

---

## Next

- **One audit target, not two.** Berlekamp Domineering (60 lines, unverified advance,
  replication explicitly requested) — done, and it holds; see `leanboard/ah/`. Rank 429 was
  the second and is withdrawn: it is a positive lower-bound paper, not a checkable claim.
  **No second audit target is currently identified.**
- **A second compiled-problem site exists, and it may be the better instrument.** Search
  surfaced *VibeMathed*, whose items are titled as method ceilings directly — one is "The
  ceiling of the single-letter entropy method for the union-closed sets conjecture." If a
  site indexes barriers *by name*, it does by construction what I have been assembling by
  hand one paper at a time. **Look at it before investing more in hand-assembly.**
- **Rank 429 moves to the prospective arm** as a dated, self-declared board-exhaustion
  instance with both routes capped at 2/3 and the ceiling sitting on Gallai 1966.
- **Pull the three remaining `disputed claim` cards in full.** 372, 406, 480 — and pull them
  before saying anything further about what they contain. Rank 429 is the demonstration that
  the badge alone supports no conclusion at all.
- **Standing check, from the rank-429 failure:** a status label is a pointer to content, not
  content. Before building on what a card *is*, open it. If it cannot be opened, write the
  inference down as an inference, with the word.
- **The filter is the instrument.** Research-attached + bottom of rank is obtainable in two
  clicks. Everything I inferred about workspace allocation from card format was weaker than
  this one control.
- **Use line counts in opposite directions per workstream** — thickest for harvesting
  boards, thinnest for claiming a result. Recorded above.
- **Standing check, from the rank-400 failure:** before proposing an enumerate-and-compute
  attack, test whether the target functional is convex or concave along the natural
  deformations of the class. If it is convex and you are hunting a maximum, sampling cannot
  work. And check **scale** separately — rank 393 is the right shape and still infeasible.
