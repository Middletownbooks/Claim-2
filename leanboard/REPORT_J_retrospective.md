# Report J — Retrospective benchmark on the FLT proof's early layers

**Question.** A complete traversal of a hard theorem is available. Its
load-bearing interfaces are known in hindsight. Standing at the *beginning* of
that proof, could the interfaces that end up carrying it be identified?

Method and predictions fixed in `flt/PREREG_retrospective.md` before running.
Code: `flt/retro.py` (pre-registered), `flt/retro2.py` (post-hoc, corrected),
`flt/retro_stability.py` (sweep). Data: `flt/retro*.json`.

---

## J.1 Setup

* **Answer key, hidden from every predictor:** for each of the 1 230 definition
  modules, its statement usage across the proof. Target = the modules carrying
  80% of usage.
* **Early layers:** bottom-up citation depth, `depth(v)=0` for theorems citing
  nothing. The pre-registered rule — *smallest `D` with ≥25% of theorems at
  depth ≤ D* — selected **D = 0**: the 8 230 leaves, 27.9% of the proof.
* **Predictors:** all unsupervised, computed from early layers only. No
  training step, so nothing can leak through fitting.

## J.2 Pre-registered scorecard

| prediction | outcome |
|---|---|
| **Q1** >20% of load-bearing definitions are invisible early | **FAILED, decisively** — **0 of 282** are invisible. Every definition that ends up carrying the proof already appears in a depth-0 statement |
| **Q2** `early_usage` reaches AUC ≥ 0.80 | **PASSED** — AUC 0.963 (0.953 among early-visible) |
| **Q3** no structural feature beats `early_usage` by >5pp on precision | **PASSED** — best structural (`cooccurrence_breadth`) 0.780 vs 0.816 |
| **Q4** `cooccurrence_breadth` ranks the true top-20 higher than `early_usage` | **marginal** — 12/20 vs 11/20, within noise |

Pre-registered results (P@282, random baseline 0.229): `early_usage` **0.816**,
`early_users_distinct` 0.816, `cooccurrence_breadth` 0.780, `combined` 0.755,
`community_breadth` 0.628, `early_consumer_degree` 0.273.

## J.3 Three defects in my own pre-registered design

Found while reading the results, and all three inflate the case for the naive
baseline:

1. **The depth rule produced a degenerate early set.** Leaves cite nothing, so
   at D = 0 the early subgraph has **zero internal edges** and
   `early_consumer_degree` is identically zero. Its 0.273 / AUC 0.500 is not a
   negative finding, it is an undefined feature.
2. **`community_breadth` leaked the future.** It used the blind communities from
   Report I, which were computed on the *whole* graph including late layers. It
   still lost, so the leak did not manufacture a win — but the feature as scored
   was not an early-layer measurement.
3. **The target contained the predictor's own input.** Total usage includes
   early usage, so `early_usage` was partly predicting a component of its own
   label. That is not forecasting.

## J.4 Corrected run (post-hoc, labelled)

`flt/retro2.py`: D = 2 (47% of theorems, 11 306 internal edges), communities
recomputed **on the early subgraph alone**, and the target changed to the
definitions carrying 80% of **late-only** usage — a genuine forecast.

| predictor | P@K (K=251) | AUC | true top-20 hits |
|---|---|---|---|
| **`community_breadth` (early-only)** | **0.797** | **0.964** | 10/20 |
| `combined` | 0.749 | 0.946 | 8/20 |
| `early_usage` | 0.741 | 0.947 | 8/20 |
| `cooccurrence_breadth` | 0.689 | 0.938 | 10/20 |
| `early_consumer_degree` | 0.530 | 0.816 | 3/20 |

Random baseline 0.204. **The structural breadth measure beats naive frequency
counting by 5.6 percentage points of precision** — the exact condition Q3
named as evidence that a bridge-like signal carries content the naive count
lacks.

## J.5 Stability sweep

Because that win appeared only after I corrected my own design, it needed a
check that it is not an artifact of D = 2. `flt/retro_stability.py`, run once
over six splits:

| D | early fraction | target | `early_usage` P / AUC | `cooccurrence` P / AUC | `community_breadth` P / AUC |
|---|---|---|---|---|---|
| 1 | 0.396 | 258 | 0.764 / 0.951 | 0.771 / 0.955 | **0.798 / 0.962** |
| 2 | 0.473 | 251 | 0.741 / 0.947 | 0.689 / 0.938 | **0.797 / 0.964** |
| 3 | 0.531 | 244 | 0.738 / 0.944 | 0.705 / 0.941 | **0.803 / 0.963** |
| 4 | 0.573 | 235 | 0.694 / 0.931 | 0.685 / 0.934 | **0.791 / 0.960** |
| 6 | 0.635 | 223 | 0.677 / 0.926 | 0.637 / 0.926 | **0.794 / 0.965** |
| 8 | 0.677 | 213 | 0.643 / 0.918 | 0.601 / 0.918 | **0.789 / 0.965** |

**`community_breadth` wins in 6 of 6 splits**, and the margin *widens* with
depth: +3.4pp at D = 1, +14.6pp at D = 8. Its AUC is flat (0.960–0.965) while
naive usage decays (0.951 → 0.918). Frequency counting degrades as the horizon
lengthens; breadth-across-regions does not.

**Invisible targets: 0 at every split.**

## J.6 What this does and does not establish

**It establishes:** within a developing formal proof, *how many distinct regions
use an abstraction early* forecasts whether that abstraction will carry the
proof better than *how often it is used early*, robustly across horizons, and
the advantage grows with the forecast distance. This is the first positive
evidence in this programme for a bridge-value-shaped quantity, and it arrived in
a controlled forecast setting rather than a retrospective narrative.

**It does not establish that discovery is easy.** Q1's failure — every
load-bearing definition already visible in the bottom layer — has a mundane
explanation: in this corpus each definition arrives together with basic lemmas
about it, so nothing can be load-bearing later without appearing early. The
benchmark therefore measures **ranking abstractions that already exist**, not
**inventing** them. A discovery system faces the harder problem where the
abstraction is not yet in the corpus at all, and this experiment says nothing
about that case. Read as a claim about discovery, the "no ceiling" result would
be badly over-read.

**Relation to the earlier "no" on bridge value as an objective.** These are
different claims and both stand. Report G argued against putting *Lean bridge
value* into the discovery objective, because it rewards proximity to what is
already formalized. Report J finds that *breadth across regions* predicts
load-bearing status **inside a proof under construction**. The first is about
scoring candidate theorems against a mature library; the second is about
prioritizing work within an active development. The honest recommendation is
unchanged for the discovery engine and new for proof engineering: **use breadth,
not frequency, to decide which abstractions to invest in while a proof is being
built.**

## J.7 Methodological note

The pre-registered experiment answered a badly-posed question and the corrected
one answered the intended question. Both are reported, in that order, with the
defects named. The corrections were specified before their results were seen,
and the stability sweep was run once. Anyone re-running this should treat J.4–J.5
as post-hoc-but-controlled, not as pre-registered.
