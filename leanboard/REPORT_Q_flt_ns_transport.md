# Report Q — Cross-Board Transport: FLT ↔ Navier–Stokes

Phase Q studies the missing edge of the triangle FLT ↔ mathlib ↔ NS. Every
number below is computed from the two clones; the provenance tag on each claim
follows §16 of the brief.

| | FLT | NS |
|---|---|---|
| repository | `anthropics/fermats-last-theorem` | `openai/NavierStokesAndEuler` |
| commit | `aa2d8b34` | `8937a8f4` |
| Lean modules | 60 474 | 2 484 |
| theorems | 48 503 | 37 330 |
| definitions (board-specific) | 8 015 | 8 392 |
| mathlib modules imported | 1 705 | 303 |
| mathlib declarations referenced | 25 413 | 2 486 |

`DIRECTLY OBSERVED`. Nothing here is Lean-checked: `elan.lean-lang.org` is
egress-blocked in this environment, as recorded since the first phase of this
programme. Every claim is about source text and graphs, never about
type-checking.

---

## A. Executive verdict

> **NEGATIVE**, with one qualification that matters more than the verdict.

Level I (object transport) is near zero in both directions. Level II
(architecture transport) is refuted for every mathematically contentful pattern
tested and holds only for generic proof engineering that any large Lean
development does. Level III (strategy transport) is **not testable** on these
artifacts, because neither preserves a construction trajectory.

The qualification: the same measurement returns a near-zero for **Euler →
Navier–Stokes** — two halves of one repository, same authors, same month,
adjacent equations. So the FLT ↔ NS null is not a fact about the distance from
number theory to fluid dynamics. It is a fact about how these artifacts are
built: internally redundant, externally closed. That is the finding of Phase Q,
and it is a stronger result than a bare negative.

---

## B. Board decomposition

`COMPUTED FROM ARTIFACT` (`q/regions.py`). Both boards are decomposed by the
mathlib each module actually references, not by module names — FLT's README
warns its names are machine-generated, and NS's name its construction stages
(`ActualCycleAssembly`, `AllOrderDriftBudget`, `ActivationCone`) rather than
its mathematics.

**FLT**, by dominant mathlib subarea (59 999 modules profiled):
`Algebra.Group` 15 501 · `Algebra.Algebra` 4 953 · `Algebra.Ring` 4 447 ·
`RingTheory.Ideal` 3 992 · `FieldTheory.IsAlgClosed` 2 515 ·
`Algebra.Module` 2 501 · `RingTheory.LocalRing` 1 493 ·
`NumberTheory.ModularForms` 1 423 · `LinearAlgebra.Matrix` 1 104 ·
`AlgebraicGeometry.EllipticCurve` 1 050.

By declaration prefix the classical regions are visible and large:
`ModularCurve` 7 711 · `AlgebraicGeometry` 3 322 · `CerednikDrinfeld` 2 376 ·
`AutomorphicForm` 2 336 · `AlgebraicCurve` 1 577 · `LanglandsTunnell` 1 543 ·
`WeierstrassCurve` 1 003 · `Deformation` 120.

**NS** (2 476 modules profiled): `Analysis.Calculus` 724 · `Algebra.Order` 350
· `Analysis.Normed` 186 · `Algebra.Group` 181 · `Topology.UniformSpace` 126 ·
`Analysis.InnerProductSpace` 110 · `Topology.ContinuousMap` 70 ·
`Order.Filter` 60.

The decomposition is close to disjoint where it counts:

* **1.9%** of FLT's modules are dominated by any analysis or topology subarea
  (961 of 50 567).
* **0** NS modules are dominated by `RingTheory`, `NumberTheory`, `FieldTheory`
  or `AlgebraicGeometry`. NS's 22.7% "algebra" share is `Algebra.Order` and
  `Algebra.Group` — inequality and arithmetic infrastructure for estimates.
* The subareas in which both boards have regions are `Algebra.Group`,
  `Basic.Logic`, `Tactic.FunProp`, `Topology.Defs`,
  `Analysis.SpecialFunctions` — generic infrastructure, i.e. Control A.

---

## C. Interfaces and the contact surface

`COMPUTED FROM ARTIFACT` (`q/substrate.py`, `q/decluse2.py`).

**Shared mathlib substrate.** 211 of NS's 303 mathlib modules are also
imported by FLT — **69.6% of NS's footprint, 12.4% of FLT's**. At declaration
level, 1 948 of NS's 2 486 mathlib declarations are also referenced by FLT —
**78.4% of NS's, 7.7% of FLT's**.

That overlap is *not* explained away as generic mathlib: about half of it
(999 of 1 948) is used by 30 or fewer of FLT's 60 474 files. But its content
settles the question. The shared-and-rare-in-FLT declarations are NS's analysis
toolkit — `ContinuousLinearMap` (10 FLT files, 647 NS), `HasDerivWithinAt`
(27 / 290), `BoundedContinuousFunction` (7 / 224), `ContinuousMap.norm_le`
(11 / 99), `EuclideanSpace.single` (2 / 73), `real_inner_self_eq_norm_sq`
(7 / 55), `iteratedFDerivWithin_of_isOpen` (19 / 52).

**The contact surface.** The FLT files touching that vocabulary number **406 of
60 474 — 0.67% of the board**, almost all under `P2M/Sol`. They cluster into
four recognisable places:

| FLT region | what it does analytically |
|---|---|
| `LanglandsTunnell.CubicInduction` (incl. `AdelicEpstein`, `archZetaDual`) | archimedean zeta and Epstein series, Jacquet vectors |
| `AutomorphicForm.ComplexIwasawa`, `GL2Real`, `bruhatEisenstein` | rapid-decay and Fourier-integral bounds on iterated derivatives |
| `AlgebraicCurve.CellDissection`, `Complex.integral_radial_loop` | contour integration, residues, periods |
| `LocalParametrix` (6 theorems) | symbol-class estimates for a second-order elliptic operator |

`LocalParametrix` is the most interesting single object found in Phase Q and is
worth stating exactly. `DIRECTLY OBSERVED` in
`Theorems/Thm_LocalParametrix_exists_symbol_norm_iteratedFDeriv_le_integrable_iterate_sub_one_of_span_eq_top.lean`:
it constructs `r : V → ℂ`, smooth, with

```
∀ n, ∃ C, ∀ ξ, ‖iteratedFDeriv ℝ n r ξ‖ ≤ C * (1 + ‖ξ‖) ^ (-(2*m + n : ℝ))
```

together with integrability of an iterated second-order operator applied to it.
That is a symbol of class S^(−2m) and a parametrix construction — genuine
pseudodifferential machinery, sitting inside a proof of Fermat's Last Theorem.
`STANDARD MATHEMATICAL INFERENCE` for the identification of the symbol class;
`DIRECTLY OBSERVED` for the Lean statement.

It is the best Level-I bridge candidate the board offers, and §E records that
it produced no measurable gain.

---

## D. FLT ↔ NS bridge ledger

Machine-readable: `q/bridge_ledger_flt_ns.json` and `.csv`.

| id | mechanism | evidence level | experiment | measurable gain |
|---|---|---|---|---|
| B1 | shared mathlib analysis substrate | **1** actual shared Lean dependency | exact module/declaration intersection | **none** — both import mathlib; this is Control A |
| B2 | FLT's analytic contact surface (`LocalParametrix` etc.) | **2** actual shared abstraction | used as Control E in transport | **none measured** — scored *below* the random-FLT control (0.105 vs 0.145) |
| B3 | integrability of polynomial × exp(−πμt) on a half-line | **3** actual shared proof infrastructure | exportable-surface matching | **3 NS lemmas (~0.1%)**; fails the §13 control — a mathlib gap, not board knowledge |
| B4 | both headline results are non-existence statements | **5** analogy | read both main theorems | **none** — the shapes are dual, not shared (below) |
| B5 | local-to-global assembly | **4 — REFUTED** | architecture profile | **none** — FLT 35.2%/15.75%, NS 3.95%/**0.04%** |
| B6 | have/calc chains, case splits, finite-level approximation | **4** genuinely shared | architecture profile | **none attributable** — Control A at the architecture level |
| B7 | strategy transport (Level III) | **not testable** | trajectory recovery | **not measurable** — no trajectory survives in either artifact |

On B4: FLT's theorem *is* a negation (`a^n + b^n ≠ c^n`); NS's is an
existential containing one (`∃ u₀ f, … ∧ ¬∃ v p, …`). FLT refutes a
counterexample by transporting it into a classification space and showing that
space is empty; NS constructs a counterexample and forces blowup by
quantitative estimates. Classification-and-obstruction versus
construction-and-estimate. Recorded so the analogy is not promoted.

---

## E. Transport experiments

### Protocol

`EXPERIMENTAL RESULT` (`q/transport2.py`).

*Phase A, source-visible.* Candidates are generated from the source board alone
by a target-independent rule fixed in the previous phase: a theorem whose
**statement** names no board-specific definition, hence is sayable on any board
that speaks mathlib. Exportable surfaces: **FLT 12 577 of 48 503 (25.9%)**,
**NS 4 054 of 37 330 (10.9%)**.

*Phase B, target-blind.* No re-ranking against the target. The whole pool is
carried over, so there is no opportunity to select for the answer.

*Phase C, application.* Each target statement is matched against the pool by
token-set Jaccard, and against controls. Both sides are restricted to
exportable statements, so the token sets come from the same vocabulary (median
sizes 12 and 7).

### FLT → NS, 2 829 NS queries

| pool | size | mean | median | ≥0.4 | ≥0.6 | ≥0.8 |
|---|---|---|---|---|---|---|
| **TRANSPORT** FLT exportable | 11 093 | 0.171 | 0.143 | **68 (2.4%)** | 4 | 0 |
| **Control B** NS itself | 2 829 | 0.416 | 0.333 | **1 233 (43.6%)** | 637 | 277 |
| **Control C** random FLT ¼ | 2 773 | 0.145 | 0.125 | 16 | 0 | 0 |
| **Control E** architecture contact | 101 | 0.105 | 0.091 | 18 | 3 | 0 |

### NS → FLT, 11 093 FLT queries

| pool | size | mean | ≥0.4 | ≥0.6 |
|---|---|---|---|---|
| **TRANSPORT** NS exportable | 2 829 | 0.116 | **34 (0.3%)** | 2 |
| **Control B** FLT itself | 11 093 | 0.574 | **8 238 (74.3%)** | 4 983 |
| **Control C** random NS ¼ | 707 | 0.100 | 11 | 1 |

In both directions the target board's own material outmatches the source
board's by 20–100×, and the transport arm barely separates from a random draw
from the same source board.

The four surviving FLT → NS matches at J ≥ 0.6 collapse to **one** FLT lemma,
`LanglandsTunnell.integrableOn_and_integral_Ioi_exp_neg_pi_mu`, matched by
`integrableOn_shift_exp`, `polynomial_exp_integrable` and
`const_polynomial_exp_integrable`, plus one generic parameter-integral lemma.

### The positive control that reframes the result

`EXPERIMENTAL RESULT` (`q/poscontrol.py`). A near-zero only means something if
the instrument can register a positive. So the identical protocol was run on
the pair that should transport if anything does — the **Euler** and
**NavierStokes** halves of the same repository.

| direction | pool | mean | ≥0.4 | ≥0.6 |
|---|---|---|---|---|
| Euler → NavierStokes | 876 | **0.192** | **108 (5.5%)** | 9 |
| NavierStokes → Euler | 1 953 | **0.207** | 64 (7.3%) | 7 |
| NavierStokes within itself | 1 953 | 0.424 | 874 (44.8%) | 465 |
| Euler within itself | 876 | 0.373 | 313 (35.7%) | 163 |

Siblings transport at 5.5%, against FLT → NS at 2.4% and a random-FLT floor of
0.6%. The instrument does discriminate — within-board scores run at twice the
cross-board ones — but it cannot separate a *related* cross-board pair from an
*unrelated* one, because both sit near the floor.

So the honest reading is narrower and more interesting than "FLT and NS are
unrelated": **statement-level transport between these formalizations is near
zero regardless of mathematical proximity.** What does transport between Euler
and NS is the same kind of thing as the single FLT bridge — duplicated generic
analysis lemmas (`integral_contDiff_finite` ↔ `compact_integral_contDiff`,
J = 0.80).

---

## F. Architecture comparison

`EXPERIMENTAL RESULT` (`q/arch.py`). Two channels kept apart: what statements
say, and what proofs do. Percentages are of files matching.

| pattern | FLT stmt | NS stmt | FLT tac | NS tac |
|---|---|---|---|---|
| local_to_global | **35.20** | 3.95 | **15.75** | **0.04** |
| functorial_transport | **48.69** | 7.13 | **17.53** | 0.64 |
| quotienting | **10.36** | 0.36 | **19.74** | 0.20 |
| contradiction | **22.23** | 3.06 | **35.91** | 7.57 |
| deformation_lifting | 3.33 | 5.16 | **17.76** | 3.14 |
| induction_on_parameter | — | — | **30.43** | 9.07 |
| regularity_upgrade | 4.35 | **54.63** | 2.69 | 7.74 |
| energy_height_inequality | 2.41 | **43.11** | 12.56 | **36.87** |
| approximation_limit | 0.72 | **15.11** | 3.38 | **10.56** |
| compactness_extraction | 2.23 | **14.79** | 5.79 | 9.39 |
| duality | 0.78 | **7.70** | 1.43 | 0.16 |
| *finite_level_approximation* | *43.41* | *44.96* | *45.90* | *28.53* |
| *intermediate_lemma_chain* | — | — | *93.52* | *90.05* |

### Proof moves

`EXPERIMENTAL RESULT` (`q/tactics.py`). Tactic occurrences per 1 000 proofs —
a sharper channel than files-containing-a-pattern, and one that machine-
generated names cannot contaminate.

| NS-heavy (estimate machinery) | FLT | NS | ratio |
|---|---|---|---|
| `bound` | 0.6 | 35.3 | **22.7×** |
| `filter_upwards` | 5.0 | 46.6 | 7.9× |
| `nlinarith` | 6.2 | 52.8 | 7.5× |
| `positivity` | 13.5 | 75.2 | 5.3× |
| `linarith` | 21.4 | 110.1 | 5.0× |
| `gcongr` | 3.0 | 7.1 | 2.0× |

| FLT-heavy (structural machinery) | FLT | NS | ratio |
|---|---|---|---|
| `absurd` | 14.3 | 0.0 | **14×** |
| `rintro` | 45.5 | 4.3 | 9.1× |
| `rcases` | 37.1 | 8.3 | 4.2× |
| `ext` | 151.8 | 44.0 | 3.4× |
| `obtain` | 255.4 | 75.7 | 3.3× |
| `refine` | 223.9 | 67.2 | 3.3× |
| `subst` | 30.4 | 8.8 | 3.2× |
| `induction` | 23.7 | 10.8 | 2.1× |

| shared backbone | FLT | NS | ratio |
|---|---|---|---|
| `have` | 1167.2 | 1037.4 | 0.89 |
| `simp` | 325.2 | 296.7 | 0.91 |
| `intro` | 243.8 | 259.9 | 1.07 |
| `by_cases` | 32.0 | 31.1 | 0.97 |
| `fun_prop` | 3.3 | 3.3 | 1.00 |

Both boards place almost exactly one `have` per proof and reach for `simp`,
`intro` and `by_cases` at the same rate. Everything with mathematical content
differs by 3–23× in one direction or the other. NS proves inequalities; FLT
destructures and rewrites structures.

The contentful architectures are disjoint and the split is sharp: FLT is
local-to-global, functorial, quotienting and contradiction-driven; NS is
regularity, energy estimates, compactness and limits. `local_to_global` — the
brief's leading candidate — appears in 15.75% of FLT proofs and **0.04%** of
NS's.

What is shared (italicised) is generic proof engineering: lemma chains at 93.5%
against 90.1%, finite-level approximation at 43.4% against 45.0%. Every large
Lean development does these. Promoting them to a shared architecture would be
exactly the category-5-to-category-4 error §1 warns against.

---

## G. LLM construction-trajectory analysis, and the game representation

`DIRECTLY OBSERVED`. The brief asks what trajectory data is actually available.
The answer is: **none, in either artifact.**

* Both repositories are a **single squashed commit** (`aa2d8b34`, `8937a8f4`).
* FLT's `ATTRIBUTION.md` states it plainly: *"The Lean files of this repository
  were assembled by AI agents and were published without their comments."*
  Measured comment density confirms it — **0.000%** of lines in `Theorems/`,
  **0.002%** in `P2M/Sol/`, against NS's **~2%**.
* NS's comments are mathematical documentation keyed to the source paper's
  numbered equations ("the literal covariance terms in (32)") — a Lean↔paper
  map, not a process record.
* No intermediate theorem DAG, failed attempt, routing decision, agent
  decomposition or timestamp is recoverable from either.

Therefore, keeping the brief's four levels apart:

| level | available? |
|---|---|
| final theorem graph | **yes** — 106 897 FLT citation edges, depth 118 |
| proof architecture | **yes** — measurable (§F); FLT additionally documents its route in `PROOF-PATH.md` |
| construction trajectory | **no** |
| agent / search strategy | **no** |

**Level III cannot be tested here, and no attempt was made to infer it from the
final graph.** Inferring strategy from a finished DAG is precisely the
inference §16 forbids.

**Game representation (§10): USEFUL BUT UNVALIDATED.** The state
`S = (G, L, B, C)` and the action set are a coherent way to describe what these
proofs contain, and FLT's `PROOF-PATH.md` narrates something close to it. But
validating it requires observing trajectories, and no trajectory survives in
either artifact. It is not supported by evidence here, and it is not merely
metaphorical either — it is untested. Calling it empirically supported on the
strength of the final graph would be the error the brief names.

One genuine, documented transport event does exist, and it is worth recording
because it is the only one in the ledger with real extent: FLT's
`ATTRIBUTION.md` identifies **106 files** carrying Lean text from the Imperial
College London FLT project and flt-regular, many "whole file (100%)". That is
`DOCUMENTED BY SOURCE` transport — from a prior human formalization into an
LLM-assembled one. It is not FLT ↔ NS, and it did not need any of the
machinery of this phase to find, but it is the shape a successful transport
actually takes.

---

## H. Negative results (mandatory)

1. **Level I object transport: near zero, both directions.** 2.4% of NS's
   exportable statements find any FLT near-twin at J ≥ 0.4, against 43.6% from
   NS's own board; 0.3% in reverse against 74.3%.
2. **The one surviving bridge fails its own negative control.** B3 is
   integrability of polynomial × exp on a half-line — a gap in mathlib. §13
   asks whether ordinary mathlib infrastructure would have sufficed; here it
   would, and the right fix is upstreaming, not transport.
3. **Control E was the worst pool tested.** The architecture-aware contact
   surface — the 400 FLT theorems selected precisely for speaking NS's analytic
   vocabulary, including `LocalParametrix` — scored *below* random FLT
   (0.105 vs 0.145). Selecting for shared vocabulary did not select for
   transportable content.
4. **`local_to_global` is refuted as a shared architecture**, at 0.04% of NS
   proofs. So are quotienting, functorial transport and deformation/lifting.
5. **The non-existence analogy (B4) does not survive inspection.** The two
   theorem shapes are dual, and the boards' work sits in opposite places.
6. **The positive control nearly matches the experimental arm.** Euler → NS
   scores 5.5% against FLT → NS's 2.4%. The measurement cannot distinguish a
   related cross-board pair from an unrelated one; both are near the floor.
   This limits how strongly the FLT ↔ NS null can be attributed to
   mathematical distance, and it is the reason §A's verdict carries a
   qualification.
7. **Two methodological failures of my own, both retracted in place.**
   * A first transport run scored NS against itself at mean **0.97** and is
     withdrawn: NS statements carry a median of **one** mathlib token, so it
     measured vocabulary poverty, not similarity. The corrected run restricts
     both sides to exportable surfaces (median token sets 12 and 7).
   * The shared-vocabulary ranking was initially topped by `by`, `the`, `and`,
     `of`, `is` — 20 English words that the previous phase's `decls.json`
     records as root-level mathlib declarations, from a regex matching a
     continuation line. Twenty entries out of 25 760, but they occur in every
     file of both boards. Root matching now requires an underscore or an
     uppercase letter.

---

## I. Research implications

Tied to the evidence, not to intuition.

**Not justified: (3) search for a third board.** §14 says to add one only if it
would distinguish competing hypotheses. The Euler/NS positive control already
supplied that datum from inside the existing material: it separated "these two
boards are far apart" from "these artifacts do not export", and it favoured
the second. A third board would re-ask a question now answered.

**Not available: (2) analyse LLM construction trajectories.** The data does not
exist in either artifact (§G). This is the single largest blocker in the
programme, and it is a *sourcing* problem, not an analysis problem. If
trajectory analysis is wanted, it needs artifacts published with their history
— which is a request to make of the artifact producers, not a computation.

**Most justified: (5) refine the board representation.** Three results point
the same way, and they point at the unit of transport rather than at the
boards:

* NS duplicates itself. 44.8% of its exportable statements have a near-twin
  elsewhere in NS, with literal repeats — `weighted_integrable` proved in two
  files, `factor_slice_contDiff` beside `factor_contDiff`,
  `kernel_contDiff_param` beside `kernel_contDiff_x`. FLT does the same at
  74.3%.
* The only cross-board bridge found is a missing mathlib lemma.
* Siblings transport barely better than strangers.

Taken together: the transport channel between large formalizations is not
board-to-board, it is **board → mathlib → board**. The two known edges of the
triangle carry the traffic; the missing edge is missing because it is not where
transport lives. The measurable quantity to chase next is *upstreamability* —
how much of each board's exportable surface is redundant with mathlib or with
itself — and the intervention that would produce measurable gain is
deduplication and upstreaming, not cross-board search.

That reframes the deeper question of §17. Of the four candidates —
objects, representations, proof architectures, search strategies — this phase
finds that **objects do not transport board-to-board** (§E), **contentful
architectures do not either** (§F), **generic architectures transport but carry
no information** (B6), and **strategies could not be tested at all** (§G). The
one thing observed actually moving between developments is a human formalization
being absorbed wholesale into a machine-assembled one, through shared source
text (106 files) — transport by *library*, at the granularity of a file.

**Falsifier for the current reading.** If a board pair were found whose
cross-board score approached its within-board score, the "formalizations are
externally closed" reading would fail and mathematical proximity would be back
in play. Euler/NS was the most favourable such pair available and did not do
it.

---

## Artifacts

`q/substrate.json` · `q/decluse2.json` · `q/regions.json` · `q/surface.json` ·
`q/transport2.json` · `q/transport2_reverse.json` · `q/poscontrol.json` ·
`q/arch.json` · `q/tactics.json` · `q/bridge_ledger_flt_ns.json` / `.csv` ·
`q/contact_files.json` · scripts `q/*.py`.

Regenerable intermediates (`per_module_vocab.json`, `stmts_*.json`, logs) are
gitignored; each rebuilds in two to six minutes from the two clones.
