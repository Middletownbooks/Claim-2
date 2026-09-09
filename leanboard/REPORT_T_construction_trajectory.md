# Report T — Construction-Trajectory Transport

Corpus: the ten `openai/ten-proofs` developments from Phase S (`94bc0fe`), not
broadened. Pre-registration: `t/PREREG.md`, written before any intervention,
including the declared prediction and the falsification criteria.

---

## 20. The central falsification question, answered first

> Can a normalized proof-construction trajectory from development A improve
> prospective proof construction in development B, beyond matched
> random/wrong-domain architectures and beyond vocabulary similarity?

$$\boxed{\textbf{NO — construction-trajectory transport is FALSIFIED for this corpus.}}$$

Source-specific benefit over a wrong-domain source, by representation level,
with 95% intervals from a bootstrap clustered on target development:

| level | what it encodes | SOURCE − WRONG | 95% CI | devs > 0 | verdict |
|---|---|---|---|---|---|
| **L1** | raw Lean tactic tokens | **+0.584 (6.1%)** | **[+0.147, +1.033]** | 8/10 | **significant** |
| L2 | structural construction moves | +0.022 (0.7%) | [−0.035, +0.080] | 6/10 | null |
| L3 | content-free architecture | +0.027 (1.0%) | [−0.028, +0.083] | 6/10 | null |
| ENG | engineering moves only | **−0.003 (−0.2%)** | [−0.012, +0.006] | 3/10 | null, negative point estimate |
| MATH | mathematical moves only | +0.022 (1.2%) | [−0.004, +0.049] | 5/10 | null |

**The only level at which it matters which development the trajectory came from
is the raw Lean tactic token sequence.** Every level that preserves
mathematical construction while stripping Lean-specific detail returns an
interval containing zero.

This is §16's **Outcome B**, and sharper than Outcome B as written: it is not
even proof *engineering* that transports — the ENG arm is null with a negative
point estimate. What transports is Lean *token style*.

My pre-registered prediction (§6 of the prereg) was "null for MATH, small
positive for ENG". MATH was null as predicted; ENG was **not** positive, so
half the prediction failed and is recorded failed.

---

## 1. What Phase S's architecture metric actually was

`COMPUTED FROM ARTIFACT`. Phase S's architecture similarity was a cosine over
35 tactic rates per 1000 proofs. Decomposed by contribution to squared
magnitude:

| tactic | share | cumulative |
|---|---|---|
| `have` | **0.538** | 0.538 |
| `exact` | 0.124 | 0.662 |
| `rw` | 0.123 | 0.784 |
| `simp` | 0.079 | 0.864 |
| `apply` | 0.049 | 0.913 |
| `intro` | 0.047 | **0.960** |

Under §2's taxonomy these are category **C** (toolchain) and category **A**
(proof engineering); **none is category B** (mathematical construction). Phase
S's architecture channel was, as operationalized, largely a **`have`-rate**
channel. Phase T therefore does not reuse it, and this report should be read
as retiring that metric rather than extending it.

---

## 2–4. The three representations

`COMPUTED FROM ARTIFACT` (`t/extract.py`). 6 153 proofs with ≥ 8 moves across
the ten. Every identifier — theorem, declaration, namespace, variable,
constant — is removed; what survives is the ordered sequence of what the proof
*does*.

* **L1 TACTIC** (alphabet 64) — normalized tactic tokens in order.
* **L2 STRUCTURAL** (12) — INTRO, AUX, CASE, INDUCT, CONTRA, CHAIN, REWRITE,
  APPLY, BOUND, EXT, AUTOM, CLOSE.
* **L3 ARCHITECTURE** (6) — SETUP, CONSTRUCT, BRANCH, TRANSFORM, ESTIMATE,
  CLOSE.
* **ENG** (4) — the L2 sequence keeping only REWRITE, APPLY, AUTOM, CLOSE.
* **MATH** (7) — keeping only AUX, CASE, INDUCT, CONTRA, CHAIN, BOUND, EXT.

| development | proofs | mean moves | dominant L2 moves |
|---|---|---|---|
| MetricCodes | 1 557 | 17.0 | REWRITE, AUX, APPLY, BOUND |
| SpherePacking | 880 | 20.0 | AUX, REWRITE, BOUND, APPLY |
| GapCVP | 883 | 15.9 | REWRITE, AUX, APPLY, CASE |
| QPR | 726 | 17.2 | REWRITE, AUX, APPLY, INTRO |
| Ehrhart | 599 | 17.1 | AUX, REWRITE, APPLY, BOUND |
| ConnesRigidity | 441 | 17.6 | AUX, REWRITE, APPLY, INTRO |
| NonSoficGroup | 418 | 19.1 | AUX, REWRITE, APPLY, INTRO |
| Permanent | 340 | 18.6 | REWRITE, AUX, APPLY, INTRO |
| CompactnessAndDegeneracy | 252 | 19.5 | AUX, REWRITE, APPLY, BOUND |
| MulticolorTriangleRamsey | 57 | 19.8 | AUX, APPLY, REWRITE, BOUND |

## 3 (§5). The proxy gate: is this just vocabulary again?

`EXPERIMENTAL RESULT`. Cross-development bigram-profile cosine against Phase
S's vocabulary and interface distances:

| level | bigram cos | r with vocabulary | r with interface |
|---|---|---|---|
| L1 | 0.798 ± 0.097 | +0.437 | +0.651 |
| **L2** | 0.896 ± 0.073 | **+0.471** | +0.603 |
| L3 | 0.918 ± 0.053 | +0.453 | +0.517 |
| ENG | 0.964 ± 0.037 | +0.344 | +0.487 |
| MATH | 0.936 ± 0.066 | +0.423 | +0.516 |

**The gate is passed, but not comfortably.** At r ≈ 0.44–0.47 with vocabulary
the representation is correlated with lexical similarity but far from the
collinearity that sank Phase S's interface measure (r(I,V) = 0.83). It carries
information not already in the words. Two things are worth flagging against my
own result: the trajectory profiles are *more* correlated with interface
overlap (0.52–0.65) than with vocabulary, and the cosines are extremely high in
absolute terms — 0.90 at L2, 0.96 at ENG — meaning **the ten developments have
nearly the same construction profile to begin with.** That is itself the
context for the null below.

---

## 5–8. The intervention

**The binding limitation, restated where it cannot be missed.** There is no
Lean toolchain in this environment — `elan.lean-lang.org` has been
egress-blocked since Phase 1 — so the literal experiment (supply a skeleton to
a prover; measure whether the proof succeeds and at what cost) **could not be
run.** Per §1 the smallest valid substitute was used, declared in the
pre-registration before results:

> A **guide** is built from source development A's proofs alone (order-2 Markov
> with backoff), then used to rank the whole move alphabet at every step of
> each unseen proof in target B. The score is the **rank of the move B actually
> made** — the number of candidates a searcher trying moves in guide order
> would examine. Lower is better.

It is prospective in §12's sense: the guide never sees a target proof. It is
not proof success, and — a limitation worth being explicit about — it cannot
separate "the proof followed the plan" from "the plan predicted the proof". In
this surrogate §9's *skeleton-use verification* is automatically satisfied and
therefore carries no information. Evidence from this phase is downgraded
accordingly and must not be read as if a prover had been run.

**Arms** (§7, §10), all ranking the same alphabet at the same positions, so
budget is matched by construction:

* **NONE** — uniform; expected rank (|alphabet|+1)/2.
* **RANDOM** — order-0 from A: A's move frequencies with sequence destroyed.
  This is §7's matched-random skeleton.
* **WRONG-DOMAIN** — order-2 from the least vocabulary-similar development with
  ≥ 200 proofs. Rule fixed in the prereg, applied mechanically.
* **SOURCE** — order-2 from A.

**Target selection** (§6): *none*. Every proof with ≥ 8 moves in every
development is a target — 6 153 of them. Nothing is excluded on any
outcome-related criterion, so there is no selection to leak.

### Results — mean rank of the true next move

| level | NONE | RANDOM | WRONG | SOURCE | WITHIN (ceiling) |
|---|---|---|---|---|---|
| L1 | 32.500 | 9.625 | 8.705 | **8.121** | 6.048 |
| L2 | 6.500 | 3.034 | 2.821 | **2.798** | 2.608 |
| L3 | 3.500 | 2.627 | 2.475 | **2.448** | 2.324 |
| ENG | 2.500 | 1.515 | **1.497** | 1.501 | 1.465 |
| MATH | 4.000 | 1.802 | 1.749 | **1.726** | 1.664 |

Trajectory order does carry information — SOURCE beats RANDOM at every level,
all ten developments positive, intervals excluding zero. **But almost all of
that benefit is generic:**

| level | SOURCE−RANDOM | WRONG−RANDOM | share of the benefit already available from a *wrong-domain* source |
|---|---|---|---|
| L1 | +1.505 | +0.921 | **61%** |
| L2 | +0.235 | +0.213 | **91%** |
| L3 | +0.179 | +0.152 | **85%** |
| ENG | +0.014 | +0.017 | **124%** |
| MATH | +0.076 | +0.053 | **70%** |

At L2, 91% of the apparent transport is obtained from a development chosen for
being *least* similar to the target. That residual 9% is the 0.73% effect whose
interval includes zero.

---

## 9. Mathematical versus engineering, and where the signal really lives

The one significant source-specific effect is at **L1**, the level that keeps
which *token* a development reaches for within a move class — `simp` vs
`simpa` vs `simp_rw`, `rcases` vs `obtain`, `linarith` vs `nlinarith`. That is
category C.

A direct test confirms it. **Fingerprint test**: how well can a held-out proof
be attributed to its development from its bigram profile alone?

| level | attribution accuracy (chance 0.100) |
|---|---|
| **L1** | **0.453** |
| L2 | 0.300 |
| L3 | 0.272 |
| MATH | 0.261 |

**The source-specific transport signal lives at exactly the level that carries
the authorial fingerprint.** L1 identifies its development almost twice as well
as MATH does, and L1 is the only level where SOURCE beats WRONG-DOMAIN. The
honest reading is that what transports source-specifically is a development's
Lean *style*, not its mathematics.

All levels are above chance, so there is real development-specific structure in
the mathematical moves too — it is simply not enough to beat a wrong-domain
guide.

## 11. Directionality

Mean |T(A→B) − T(B→A)| at L2 is 0.126 over all pairs, but the most asymmetric
pairs all involve MulticolorTriangleRamsey (57 proofs). Excluding it: 0.097 at
L2, 0.063 at MATH — still **four times the size of the SOURCE-vs-WRONG effect
itself (0.022)**. Directional asymmetry here is noise, not structure, and no
directional claim is made.

## 12. Retrospective versus prospective

Phase S found retrospective architectural similarity predicting transport
(r ≈ 0.35–0.41 beyond vocabulary). Phase T supplies the prospective test and it
comes back null for every mathematically meaningful representation. Per §12
that combination has a name:

$$\boxed{\text{architecture describes proofs but does not transport construction}}$$

with the added diagnosis from §1 that Phase S's "architecture" was 54% `have`.

## 17. Negative transfer

Explicitly looked for, per §17.

| level | SOURCE worse than RANDOM | SOURCE worse than WRONG-DOMAIN |
|---|---|---|
| L1 | 1 / 90 | 23 / 90 |
| L2 | 2 / 90 | 30 / 90 |
| L3 | 8 / 90 | 26 / 90 |
| **ENG** | **35 / 90** | **39 / 90** |
| MATH | 2 / 90 | 30 / 90 |

At the engineering level a source-specific guide is worse than its own
frequency model in 39% of pairs — a coin flip. At L2 and MATH the correct
source loses to a *deliberately wrong* one in a third of pairs. This is not the
systematic negative transfer §17 hypothesised (nothing like Phase S's
interface result, where the partial was significantly negative); it is
consistent with the source-specific component being ≈ 0 and the sign being
noise. The worst individual sources are dominated by
MulticolorTriangleRamsey — 57 proofs, a small-sample effect, not a
mathematical one.

## 18. QPR

`EXPERIMENTAL RESULT`. QPR is above the corpus average as a *source*
(SOURCE−WRONG = +0.088 at L2 against a corpus mean of +0.022) and **negative as
a target** (−0.145): guides from the "right" source predict QPR's proofs worse
than wrong-domain guides do.

Per §18's instruction, the pattern that makes QPR distinctive was inspected
before any label was attached. Its most over-represented L2 transitions
relative to the corpus:

| transition | QPR | corpus |
|---|---|---|
| APPLY → INTRO | 0.083 | 0.041 |
| REWRITE → REWRITE | 0.120 | 0.091 |
| INTRO → APPLY | 0.041 | 0.024 |
| INTRO → REWRITE | 0.024 | 0.014 |
| CHAIN → APPLY | 0.015 | 0.007 |

These are proof-engineering rhythms — apply-then-introduce, runs of rewriting.
**None corresponds to repetition, product construction, the martingale
argument, information-theoretic inequality, finite approximation, or
game/strategy decomposition.** So this is explicitly **not** game transport,
and is not labelled as such. Phase R's finding — that QPR's game has no state
transition and the sequential structure lives in the proof's coordinate
conditioning — is untouched by this phase: that structure does not surface in
the move-level trajectory at all.

## 14. The six channels, kept separate

| channel | status after Phases Q–T | evidence |
|---|---|---|
| **vocabulary transport** | the only positive predictor, and trivial | Phase S: V\|I+controls = +0.58, p = 0.0001. "Similar mathematics reuses similar words." |
| **interface transport** | **falsified, negative** | Phase S: I\|V+controls = −0.44, p = 0.0008 |
| **proof-engineering transport** | **null** | Phase T: ENG SOURCE−WRONG = −0.003, CI [−0.012, +0.006] |
| **mathematical architecture transport** | **null** | Phase T: MATH +0.022, CI [−0.004, +0.049]; L2 +0.022, CI [−0.035, +0.080] |
| **construction-trajectory transport** | **falsified** | the above, plus 91% of the L2 benefit available from a wrong-domain source |
| **upstreamability** | four instances, none of them transport | Q: polynomial×exp integrability; R/S: `quadratic_le_klFun`, `finite_pinsker`, `trace_mul_posSemidef_nonneg` |

The programme's running tally is unchanged and now covers four channels:
**four upstreamable lemmas, zero instances of source knowledge producing target
capability.**

## 15. Verdict, against the pre-registered criteria

Falsification criteria from `t/PREREG.md` §5, scored as written:

| # | criterion | met? |
|---|---|---|
| 1 | SOURCE does not beat RANDOM | **no** — it does, at every level |
| 2 | advantage vanishes under vocabulary control | partly — the gate passed at r ≈ 0.47 |
| 3 | **only L1/ENG transports, L2/L3/MATH do not** | **YES** — and ENG does not either |
| 4 | **SOURCE does not beat WRONG-DOMAIN** | **YES** at L2, L3, ENG, MATH |
| 5 | architecture proxy failure | no |

Criteria 3 and 4 — the two that matter — are met. The hypothesis is falsified,
and not by an ambiguous margin: at the structural level 91% of the benefit
survives replacing the source with the least similar development available.

## Limits, stated against my own conclusion

1. **No prover was run.** The surrogate measures search *guidance*, not proof
   *success*, and cannot distinguish plan-following from plan-prediction. A
   real Lean experiment could in principle find an effect this cannot see.
2. **The corpus is architecturally homogeneous.** Bigram cosine averages 0.90
   at L2 and 0.96 at ENG. Ten developments this similar leave little room for
   a source-specificity effect to appear; a null here is partly a fact about
   the corpus. A corpus spanning different provers, eras, or authors might
   behave differently — but §1 forbids broadening, correctly, since
   manufacturing variance to obtain power is what the brief warns against.
3. **A first statistical pass was wrong and is retracted.** I initially tested
   SOURCE-vs-RANDOM by source-label permutation, which carries both quantities
   together and has no power; every p came back ≈ 0.5 as an artifact of my
   test. Re-tested by target-development cluster bootstrap. SOURCE-vs-WRONG,
   where label permutation *is* valid, gave p = 0.52 at L2, agreeing with the
   bootstrap interval.
4. **The move taxonomy is mine.** Mapping `have` → AUX and `linarith` → BOUND
   is a judgement call, and a different taxonomy could redistribute the L1/L2
   gap. The fingerprint test is the check that matters, and it is
   taxonomy-independent in direction: L1 identifies developments far better
   than any collapsed level.

## Artifacts

`t/PREREG.md` · `t/extract.py`, `t/trajectories.json` · `t/experiment.py`,
`t/result.json` · `t/stats.py`, `t/stats.json` (superseded) · `t/stats2.py`,
`t/stats2.json` · `t/supplementary.txt`.
