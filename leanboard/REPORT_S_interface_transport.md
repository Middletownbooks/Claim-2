# Report S — Ten-Development Census and Interface-Mediated Transport

Corpus: `openai/ten-proofs` @ `94bc0fe`, Lean 4.32.0 / mathlib v4.32.0, plus the
mathlib source at `leanprover-community/mathlib4`. Provenance tags follow the
Phase Q convention. Nothing is Lean-checked (`elan` remains egress-blocked);
every claim is about source text and graphs.

---

## 15. The falsification question, answered first

> Does interface overlap predict transport beyond generic vocabulary overlap,
> pool sizes, statement length and generic infrastructure?

$$\boxed{\textbf{NO — the interface-mediated transport channel is FALSIFIED for this corpus.}}$$

Not merely absent: **negative**. Controlling for vocabulary overlap and the
declared confounds, interface overlap is *negatively* associated with
transport.

| predictor | raw (90 pairs, 10 devs) | size-matched (56 pairs, 8 devs) |
|---|---|---|
| V alone | **+0.480** (p = 0.002) | **+0.598** (p = 0.001) |
| I alone | +0.254 (p = 0.149) | +0.266 (p = 0.129) |
| V \| I + controls | **+0.579** (p = 0.0001) | **+0.628** (p = 0.0008) |
| **I \| V + controls** | **−0.439** (p = 0.0008) | −0.328 (p = 0.064) |
| Vr \| Ir + controls *(generic stripped)* | **+0.598** (p = 0.0001) | **+0.653** (p = 0.0003) |
| **Ir \| Vr + controls** | **−0.439** (p = 0.002) | **−0.380** (p = 0.036) |
| Arch \| controls | +0.455 (p = 0.008) | +0.576 (p = 0.009) |
| **Arch \| V + controls** | **+0.349** (p = 0.032) | +0.410 (p = 0.068) |

`V` = shared mathlib **theorems/lemmas**; `I` = shared mathlib
**types/classes/defs/instances**; `r` = subscript for the generic strip (every
mathlib declaration used by ≥ 8 of the ten removed); `Arch` = tactic-profile
cosine. Significance by **development-label permutation** (20 000 draws), which
respects that the effective sample is 8–10 developments, not 56–90 pairs.

Against §11's outcome list this is **Outcome A**, with a rider the list did not
anticipate:

* mathematical/vocabulary proximity predicts transport — strongly and robustly;
* interface proximity does **not**, and its partial is negative;
* **proof-architecture similarity predicts transport independently of
  vocabulary** (r = +0.35, p = 0.032 raw) — a third channel neither Phase Q nor
  Phase R measured.

And the brief's own warning applies to the positive half: this shows little
more than that *similar mathematics tends to reuse similar words*. `V` **is**
word similarity. The non-trivial predictor — sharing the same abstractions —
is the one that fails.

---

## A. Ten-development structural census

`COMPUTED FROM ARTIFACT` (`s/census.py`). Regions are inferred by **label
propagation on each development's internal declaration-reference graph**, not
from namespaces: Phase R found QPR carrying 94% of declarations in one
namespace while having a dense internal graph, so the two are different things.
An *interface node* is a declaration with an edge crossing a community
boundary.

| development | decls | thms | defs | ns | edges | out-deg | comm ≥20 | largest comm | cross-edge | iface nodes | exportable |
|---|---|---|---|---|---|---|---|---|---|---|---|
| GapCVP | 8 025 | 3 683 | 4 325 | 442 | 39 482 | 4.92 | 22 | 0.33 | 0.142 | 0.54 | 184 (5.0%) |
| MetricCodes | 5 683 | 4 328 | 1 314 | 432 | 24 411 | 4.30 | **35** | 0.25 | 0.124 | 0.37 | **538 (12.4%)** |
| ConnesRigidity | 2 776 | 1 930 | 773 | 33 | 11 947 | 4.30 | 15 | 0.26 | **0.252** | 0.59 | 312 (16.2%) |
| **QPR** | 2 638 | 1 813 | 822 | 8 | 16 221 | **6.15** | **6** | **0.65** | **0.066** | 0.27 | 150 (8.3%) |
| Ehrhart | 2 361 | 1 875 | 482 | 220 | 13 815 | 5.85 | **3** | **0.55** | 0.112 | 0.45 | 105 (5.6%) |
| SpherePacking | 2 220 | 1 809 | 391 | 28 | 7 730 | 3.48 | 19 | 0.38 | 0.096 | 0.29 | 357 (19.7%) |
| NonSoficGroup | 1 436 | 1 061 | 356 | 90 | 4 729 | 3.29 | 15 | 0.24 | 0.119 | 0.28 | 267 (25.2%) |
| Permanent | 1 393 | 972 | 419 | 18 | 4 285 | 3.08 | **27** | **0.14** | 0.190 | 0.46 | 155 (16.0%) |
| CompactnessAndDegeneracy | 941 | 656 | 277 | 4 | 3 737 | 3.97 | 11 | 0.17 | 0.174 | 0.50 | 69 (10.5%) |
| MulticolorTriangleRamsey | 139 | 96 | 43 | 2 | 352 | 2.53 | 3 | 0.24 | 0.153 | 0.32 | 16 (16.7%) |

The census vindicates Phase R's classification of QPR by a name-independent
route: **6 communities, largest holding 65% of declarations, the lowest
cross-community edge fraction of the ten (0.066)**. QPR is one dense territory
with a thin rim, not several territories with interfaces.

## B. Classification

Criteria declared before application:

* **BOARD** — ≥ 10 communities of ≥ 20 declarations, **and** largest community
  < 40%, **and** ≥ 1 000 declarations, **and** ≥ 100 exportable statements.
* **SUB-BOARD** — ≥ 500 declarations, failing one or more of the above.
* **PIECE-COLLECTION** — < 500 declarations.
* **THIN-APPLICATION** — a theorem assembled from existing infrastructure.

| class | developments |
|---|---|
| **BOARD** (6) | GapCVP, MetricCodes, ConnesRigidity, SpherePacking, NonSoficGroup, Permanent |
| **SUB-BOARD** (3) | **QPR** (6 communities, largest 0.65), Ehrhart (3, 0.55), CompactnessAndDegeneracy (941 decls, 69 exportable) |
| **PIECE-COLLECTION** (1) | MulticolorTriangleRamsey (139 decls, 16 exportable) |
| **THIN-APPLICATION** | none |

Six of the ten meet the board criteria. QPR does not, on the region limb —
confirming Phase R.

## C–D. Distances and the interface graph

`COMPUTED FROM ARTIFACT` (`s/distance.py`), all 45 unordered pairs in
`s/distance.json`.

| matrix | mean | median | min | max |
|---|---|---|---|---|
| vocabulary (mathlib lemmas) | 0.138 | 0.137 | 0.064 | 0.233 |
| interface (mathlib types) | 0.168 | 0.169 | 0.051 | 0.297 |
| vocabulary, generic stripped | 0.087 | 0.081 | 0.023 | 0.193 |
| interface, generic stripped | 0.095 | 0.092 | 0.007 | 0.236 |
| architecture (tactic cosine) | **0.927** | 0.945 | 0.814 | 0.990 |

Two facts constrain everything else:

1. **`r`(interface, vocabulary) = 0.83** over unordered pairs (0.74 over the
   ordered size-matched set). The two predictors are highly collinear, which
   limits how sharply the design can separate them. This is stated as a limit,
   not hidden — though note the observed interface partial is *negative*, which
   collinearity alone does not produce.
2. **The ten developments are architecturally near-identical**: tactic-profile
   cosine averages 0.927 across subjects ranging from sphere packing to quantum
   games. Consistent with Phase Q's finding that what large Lean developments
   share is generic proof engineering.

**Bridge-rich developments** (§12), mean rare-interface Jaccard to the other
nine, beside realised transport:

| development | iface-rare | vocab-rare | as source | as target | class |
|---|---|---|---|---|---|
| MetricCodes | **0.129** | 0.115 | **0.051** | 0.043 | BOARD |
| **Ehrhart** | **0.113** | 0.095 | **0.007** | **0.014** | SUB-BOARD |
| SpherePacking | 0.102 | 0.088 | 0.031 | 0.019 | BOARD |
| Permanent | 0.102 | 0.072 | 0.027 | 0.016 | BOARD |
| ConnesRigidity | 0.101 | 0.091 | 0.050 | 0.029 | BOARD |
| NonSoficGroup | 0.098 | **0.106** | 0.039 | **0.047** | BOARD |
| **QPR** | 0.096 | **0.115** | 0.036 | **0.053** | SUB-BOARD |
| GapCVP | 0.091 | 0.065 | 0.002 | 0.003 | BOARD |
| CompactnessAndDegeneracy | 0.087 | 0.076 | 0.004 | 0.011 | SUB-BOARD |
| MulticolorTriangleRamsey | 0.029 | 0.046 | 0.001 | 0.012 | PIECE |

The two rows in bold make the headline concrete. **Ehrhart is second-richest in
interfaces and near-last in transport**; **QPR is seventh in interfaces and
first as a transport target**, on the strength of its vocabulary rank. Interface
richness does not buy transport. Vocabulary richness does.

## E–F. Transport and confounds

`EXPERIMENTAL RESULT` (`s/transport.py`, `s/model.py`).

Phase R found `r`(transport, source pool size) = 0.413, so pool size is removed
**by design** here rather than regressed away: every source pool is subsampled
to a common 69 statements, averaged over 20 draws with a fixed seed.
MulticolorTriangleRamsey (16 exportable) and CompactnessAndDegeneracy fall
below the threshold and are excluded from the matched analysis, leaving 8
developments and 56 ordered pairs. The raw 90-pair analysis is retained with
log pool sizes and log median statement lengths as covariates.

| measure | within-development | cross-development |
|---|---|---|
| raw (90 pairs) | **0.6888** | **0.0247** |
| size-matched (56 pairs) | — | **0.0206** |

The 28× within/cross gap of Phases Q and R reproduces exactly, and survives
removing pool size by construction. Phase R's tentative signal (partial
r = 0.308, p = 0.048) not only survives but **strengthens** under the better
design — to +0.598 (p = 0.001) — because size-matching is a cleaner instrument
than regression adjustment. What changes is its interpretation: the predictor
that carries it is vocabulary, and Phase R's proxy was a vocabulary proxy.

## G. QPR game analysis, retested

Phase R's claim — that state transition appears in the **proof machinery**
rather than in the game — is preserved and re-checked against the census.
`DIRECTLY OBSERVED`:

| | mathematical game | proof-construction game `S=(G,L,B,C)` |
|---|---|---|
| state | `Strategy`: a shared `DensityMatrix (Alice × Bob)` plus `X → POVM A Alice` | goals, lemmas, budget, context |
| action | none — the strategy is a *fixed function* chosen before play | prove a lemma, introduce a definition, split a goal |
| **transition** | **absent** | **essential** |
| value | `entangledValue = sSup (range winProbability)` | proved / cost |
| composition | `Game.repeat n`, parallel product | sequential |

The transition is present one level up, in the proof: the argument is indexed
by `D : Finset (Fin n)` (revealed coordinates), carries an `ExactHistoryFlag`
history, and normalises `martingaleRate` by `(Finset.univ \ D).card`. The census
adds independent support: QPR's internal graph has max depth 36 with a single
dominant community — the shape of one long conditioning argument, not of
several interacting territories.

Where it breaks, restated: QPR's proof state space is the lattice of subsets of
a **fixed finite** index set, monotone and bounded, with a decreasing potential
`(univ \ D).card`. Proof construction has no fixed `n` and no such potential —
"introduce a definition" creates objects that did not exist. `EVIDENCE LEVEL: 5
(analogy)`, unchanged, not promoted.

## H. The Pinsker intervention

Pre-registered in `s/pinsker_prereg.md` **before** any target was inspected,
including the declared prediction of a null result.

**Target selection** (mechanical rule, applied as written): developments
ranked by references to `klFun`/`klDiv`, `negMulLog`/`binEntropy`,
`totalVariation`, or entropy-like sums. Qualifying: CompactnessAndDegeneracy
(88), MetricCodes (70), NonSoficGroup (5), SpherePacking (2). **Targets = the
top two.**

**Result: no effect in any arm.**

| arm | Compactness matched | MetricCodes matched | matched to a Pinsker lemma |
|---|---|---|---|
| BASELINE | 0 | 28 | 0 |
| INTERVENTION | 0 | 28 | **0** |
| NEGATIVE CONTROL | 0 | 28 | 0 |

**A power limitation that must be stated plainly.** Only **one** Pinsker
declaration is exportable — `quadratic_le_klFun`. `finite_pinsker` names QPR's
own `finiteTotalVariation` and `finiteRelativeEntropy`, so it cannot be stated
on another board without those definitions travelling too. An intervention arm
of size 1 has almost no power to detect a small effect, and this test does not
rule one out.

**But the substantive finding does not depend on that power.** `DIRECTLY
OBSERVED`, and it corrects a claim I made in Phase R: MetricCodes uses
`InformationTheory.klDiv` — the **measure-theoretic** KL divergence, applied to
`comparisonMeasure`, `arcsineMeasure`, `ν.tilted f` — 17 times. It does not use
`klFun` at all. QPR's Pinsker is about **finite distributions as functions**
`ι → ℝ` via `klFun`. The two developments that both reach for KL divergence do
so **at different levels of the mathlib hierarchy**, and QPR's inequality is not
applicable to MetricCodes' measures without a finite-to-measure bridge that
neither development has and mathlib does not supply.

That is a mechanism for the headline result. Sharing an *interface* — here, the
concept of KL divergence — does not imply transportability, because the same
concept is instantiated at incompatible levels of abstraction. It is a concrete
instance of why `I | V` comes out negative.

## I. Upstreamability versus transport, kept separate

| category | instances found | evidence |
|---|---|---|
| **UPSTREAMABLE** | `quadratic_le_klFun`; `finite_pinsker`; `trace_mul_posSemidef_nonneg`; Phase Q's polynomial × exp integrability | mathlib lacks them; each is stated about mathlib objects |
| **REUSABLE INTERFACE** | none demonstrated | Pinsker would connect mathlib's KL and TV — but the one target that uses KL uses it at an incompatible level |
| **ACTUAL TRANSPORT** | **none** | intervention null; cross-development transport 0.021–0.025 against 0.689 within |
| **ARCHITECTURE TRANSPORT** | **not demonstrated, but the only positive signal** | Arch \| V + controls = +0.35, p = 0.032. Association, not demonstrated transfer. |
| **STRATEGY TRANSPORT** | untestable | no construction trajectory in any artifact (Phase Q §G) |

The distinction the brief insists on is now empirically forced, not just
terminological: four upstreamable lemmas have been found across three phases,
and **zero** instances of source-board knowledge producing a target-board
capability.

## J. Recommendation

Against the six options:

| option | verdict |
|---|---|
| 1. Continue ten-board interface transport | **No.** The channel is falsified; the interface partial is negative at p = 0.0008. |
| 2. Promote selected developments to full boards | **Already done, and it changes nothing.** Six qualify as BOARD, and transport is at the floor for all of them — GapCVP is the largest, most region-rich development in the corpus and has the *lowest* transport of any (0.002 as source). |
| 3. Treat the collection primarily as pieces | **Partly right, and insufficient.** It is where the evidence points, but "pieces" does not explain the architecture signal. |
| 4. Seek a genuinely larger third board | **No** (§13 below). |
| 5. Return to FLT/NS upstreamability | **No as a research programme.** Phase R already judged it engineering; Phase S confirms — four upstreamable lemmas, zero transport. |
| 6. Return to mathematical deformation/transport | **Not yet.** |

**Recommended: pursue the architecture channel — the one positive signal, and
the only untested one.** Proof-architecture similarity predicts transport
independently of vocabulary (+0.35, p = 0.032 raw; +0.41, p = 0.068
size-matched), and no phase has yet tested whether it is *causal* rather than
merely associated.

The experiment: take proof-architecture patterns as the transported object
rather than statements or types. Concretely, extract tactic-level proof
skeletons — the sequence of structural moves, with mathematical content
abstracted away — from one development's proofs, and test whether supplying
them to another development's search reduces proof-search cost, against a
matched-length random-skeleton control. That is the Phase-P design applied to
architectures rather than terms, and this corpus supplies ten sources.

**Falsifier**: if skeletons transfer no better than length-matched random
skeletons, then all three channels — object, interface, architecture — are
dead for this corpus, and the honest conclusion is that these developments do
not exchange mathematics at any granularity, which would itself close the
board hypothesis.

## 13. Is another board warranted?

$$\boxed{\text{DO NOT SEEK A NEW BOARD YET}}$$

The corpus already spans 139 to 8 025 declarations, 3 to 35 regions, four
classification bands, and 45 pairs at controlled production. It produced a
significant result in both directions. Adding an eleventh development of the
same kind would add a row, not a variable.

The one structural property no available artifact has, and which would justify
a new acquisition, is stated exactly: **a preserved construction trajectory** —
intermediate states, failed attempts, ordering. Phase Q established that
neither FLT nor NS has one; Phase R that none of the ten does either (single
squashed commits, zero comments in FLT and in all ten `ten-proofs` files). That
is a sourcing problem, not an analysis problem, and Level III remains untestable
until an artifact is published with its history.

## Negative results

1. **Interface overlap does not predict transport; its partial is negative**
   (−0.439, p = 0.0008 raw; −0.380, p = 0.036 with generic stripped). The
   central hypothesis of this phase is falsified.
2. **The Pinsker intervention produced no effect in any arm** — and its
   intervention arm was a single lemma, so it also lacked power. Both facts are
   reported.
3. **The two KL-using developments use KL at incompatible levels** (`klFun` on
   finite functions vs `klDiv` on measures), so the corpus's best interface
   candidate cannot connect them.
4. **A Phase R claim is corrected**: MetricCodes uses `klDiv` 17 times, not
   `klFun`. I stated the latter; it was wrong, and the correction strengthens
   rather than weakens the negative result.
5. **The positive predictor is the trivial one.** `V` is shared-word
   similarity; the brief anticipated that this would be unimpressive, and it is.
6. **`r`(I, V) = 0.83** limits separation power; reported rather than hidden.
7. **GapCVP is the counterexample to size**: largest development, 22 regions,
   442 namespaces — and the lowest transport in the corpus, 0.002 as source.
   Being board-like does not make a development a transport partner.

## Artifacts

`s/kinds.json`, `s/kinds_summary.json` · `s/census.json` · `s/vocab_sets.json`
· `s/distance.json` · `s/tactics_profile.json` · `s/transport.json` ·
`s/model_raw.json`, `s/model_size_matched.json` · `s/pinsker_prereg.md`,
`s/pinsker_targets.json`, `s/pinsker_result.json` · `s/classification.json` ·
scripts `s/*.py`.
