# K₇,₁₁ is claimed closed, with a Lean proof, by a result dated a week before this thread began

**Source.** `github.com/openai/math`, family **165**, *The Harary–Hill and Zarankiewicz
crossing-number formulas*. The manuscript *The crossing number of complete bipartite graphs* is
dated **23 Sep 2026**. The repository's first public commit (`adc7f12`) is **6 Oct 2026**. This
thread opened with `PROMPT_GAP_v4.md` on 30 Sep and closed its last relay on 1 Oct. Snapshot and
derivation: `../../../openai-math/`. Gate verdict: `../GATE_OPENAI.md` (V1 and V2, both
SETTLED-CLAIMED at FORMAL).

## 1. What is claimed

> **Theorem 1.1.** For all positive integers m, n, cr(K_{m,n}) = d_m · d_n, with
> d_r = ⌊r/2⌋⌊(r−1)/2⌋.

So **cr(K₇,₁₁) = 3·3·5·5 = 225** and **cr(K₉,₉) = 4⁴ = 256**. The companion manuscript claims
Hill's formula for every complete graph, so **cr(K₁₃) = 225**. All three of this thread's live
numbers sit at the top of their brackets: {221, 223, 225}, {248, …, 256} and {223, 225}.

The crossing number is the ordinary point count. Arcs are simple; crossings are finite, proper and
never triple, and repeated crossings of one pair count separately. That is the quantity
`RESULT_V4.md` §3 and Woodall bound. The paper's Appendix A carries the reduction from
arbitrary drawings to this class.

## 2. What is formal, and what was checked here

openai/math's own scope note (lean/docs/165.md in that repository) says the formalization
*"proves this equality for every positive m, n and constructs a drawing attaining it"*. The
Comparator challenge (ComparatorChallenges/BipartiteCrossing.lean in openai/math) states it as
`OAI.Zarankiewicz.MainTarget`. For every m, n > 0 there is an admissible drawing with exactly `axisPairs m * axisPairs n` crossings,
and every admissible drawing has at least that many.

Checked on this side:

- **All 11 definitions in the challenge file are textually identical to the solution's**
  (`axisPairs`, `Plane`, `BipartiteVertex`, `BipartiteEdge`, `ContinuousDrawing`, `edgeInterior`,
  `ProperCrossing`, `crossingPoints`, `AdmissibleDrawing`, `crossingCount`, `MainTarget`). The
  theorem the solution proves is therefore the statement a reader sees.
- **The definitions say what the conjecture says.** Simple arcs (`edge_injective`), interiors
  avoiding vertices, finitely many crossings, each a proper transverse crossing, no point on three
  edge interiors. Adjacent edges are *not* forbidden from crossing, so the lower bound is if
  anything stronger than needed.
- **It compiles here.** `lake build` completes all 2,581 jobs, and `#print axioms` on
  `mainTarget_proof` gives only `propext`, `Classical.choice` and `Quot.sound`, so there is no
  `sorry` and no `native_decide`. `axisPairs 7 * axisPairs 11 = 225` checks by `decide`. See
  `../../../openai-math/LEAN_CHECK_165.md`. This is the first Lean toolchain this project has run. The STATUS.md line "no Lean toolchain is reachable" was true of
  the routes tried then and is false of GitHub's release assets.

What is **not** checked: Comparator itself (needs `landrun` and `lean4export`), and the paper's
Appendix A reduction from arbitrary drawings to admissible ones, which the Lean statement does not
need because it quantifies over admissible drawings directly. For this thread's question, that
gap is closed by the classical normalisation. A drawing of K₇,₁₁ with 221 or 223 crossings, if one
existed, could be made admissible without adding crossings.

## 3. What it does to every open item in this directory

| item | before | now |
|---|---|---|
| **P-43 (B)**: "the search returns NO counterexample" | open | **direction confirmed** by an external proof. The prediction was right; the computation that was to score it will not be run |
| **P-43 (A)**: "the (11,7) sweep completes within 30 days" | at risk three times | **moot.** Nobody should spend 5 days to 10 months exhausting an instance of a formalized theorem. Not rescored, per D44; the ledger records why it can never be scored |
| **H = PASS** (`K711_POTENTIAL.md`) | PASS | moot for the same reason. Reachable, and pointless to reach |
| **K₉,₉** (`K99_AND_THE_M_AXIS.md`) | out of reach | claimed 256 |
| **Hill at n = 13** (`RESULT_V4.md` §3) | {223, 225}, killed at R | claimed 225 |
| **the refute branch** (`K711_POTENTIAL.md` §3(a)) | "a cheap attempt with a self-certifying positive" | claimed impossible. A low-crossing search would return nothing, which is now known in advance |
| **`GET_THE_CODE.md`**: fetch the other instance's code | recommended | **withdrawn.** Its purpose was to make the (11,7) cost estimate trustworthy, and there is no (11,7) run to estimate |
| rotation systems + CP-SAT (`K711_POTENTIAL.md` §3(b)) | "the genuinely new idea" | moot for this target |

**What survives, because it was never about the value of cr(K₇,₁₁):**

- `VERIFIED_PSEUDOTIGHT.md`: the explicit (4,6)-set that is pseudo-tight but not tight is a
  counterexample to **Woodall's** tight/pseudo-tight equivalence. That is a different statement,
  and 165 does not touch it.
- The deficit form of Woodall's Theorem 7 (`theorem7_deficit.py`, `verify_theorem7_transfer.py`)
  is mathematics about his method and stands as derived.
- **SPECIFICATION as a sixth constraint shape** (`RESULT_STALL_ZARANKIEWICZ.md`), **D66**
  (one-sided controls) and **D67** (relays degrade measurements). These are findings about how
  this programme works, and 165 is silent on them.

## 4. The finding, and it is about selection rather than about K₇,₁₁

Cycle 0 framed this candidate in July with one question: *"The register must establish whether it
stalled on compute or on the cyclic-order realizability theory. **If theory, Claude Code adds
little and this is dead.**"* The register filled that cell on 1 Oct with a third answer,
SPECIFICATION. 165 supplies the answer from outside, and it is the one Cycle 0 called fatal:
**theory.**

The proof is not an exhaustion and not a search. It is a linear-algebra inequality: Σ dim(Uᵢ ∩ Vⱼ)
≤ ⌊m²/4⌋N for subspaces with Uᵢ ∩ Vᵢ = 0, proved by interpolation and zero-counting of
polynomial minors. That inequality is applied, through a rank-bounding linear map built from
barycentric Lagrange weights, to a matrix of signed crossing counts plus half incident-order
signs. Its own introduction places it after Kleitman's and Woodall's cyclic-order methods as a
different kind of argument. **The whole family fell at once, and the instance this thread costed
at 5 days to 10 months of compute was never the binding object.**

Three consequences, each registered in `../../../proof-protocol/debts.json`:

1. **A finite instance of a conjecture with a closed-form prediction for every n is exposed to a
   proof of the family**, and no instance-level crowding check sees that exposure. Every screen
   this thread passed asked whether anyone was working *this instance* or listing *this problem*.
   None asked whether the general statement was being attacked. A lab posing ~4,000 named
   problems to a model is attacking exactly the general statements.
2. **The thread's remedy label was read from the wrong document, and the first reading was the
   right one.** v4's R kill labels the remedy (THEORY, ALGORITHM, FLOPS, BREADTH or CONTEST) from
   the frontier paper's method section at PRIMARY tier. For V2 that paper was Woodall 1993.
   `WOODALL_1993_METHOD.md` §2 first read R as **ALGORITHM + THEORY**. §2c then narrowed it to
   **ALGORITHM** on pages 667–671, because Woodall's machinery is general in n and his paper names
   no obstruction. That correction "keeps the candidate alive". The narrowing was a faithful
   reading of Woodall and the wrong question. A 1993 paper's method section says how the *last
   instance* was closed, not what kind of argument closes the *family*. For a conjecture with a
   closed-form prediction over all (m, n), the default should be THEORY unless the instance is
   the whole content.
3. **This branch's instruments that kill on the mathematics were right twice in the same fortnight**:
   C6's premise-falsification line and U11's polarity step. The instruments that kill on
   crowding passed V2. See `../GATE_OPENAI.md` §1.

## 5. Recommendation

**Close V2 and do not reopen it as a verification exercise.** If the operator wants anything
further from this target, the one thing worth having is the method, not the number. 165 claims
both Hill's K_n formula and Zarankiewicz's, so the open question is whether its
subspace-intersection inequality reaches **crossing-number families openai/math does not claim**,
such as complete multipartite graphs or the rectilinear crossing number. That is a reading task
on a 23 Sep manuscript and its LaTeX source (the build/ directory of that preprint in openai/math),
not a computation.
