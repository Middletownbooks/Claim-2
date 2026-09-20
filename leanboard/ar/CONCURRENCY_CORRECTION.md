# Correction — the concurrency pattern was over-read

**Date:** 2026-09-20. **Status:** fourth refuted hypothesis of this series. **Measurement:** arm AR — `ar/base_rate_concurrency.py` 7/7, `ar/benchmark_ramp.py` 5/5, `ar/verify_hezhang.py` 27/27, `ar/m4_incidental_refutation.py` 6/6 (null result).

## What I claimed

Across arms AN, AM, AJ and AQ I recorded three instances of near-simultaneous AI-assisted
claims on a single problem and built an inference about *models* on top of them:

> "Shared method plus shared training data produces correlated discovery, and therefore
> correlated error." — AJ
>
> "The pattern is now too frequent to be coincidence and it is the single most important
> thing this programme has noticed." — AQ

## Four proposed mechanisms

**M1 — social seeding.**

> Someone says to someone else "I think I just got an LLM to find a counterexample for
> problem X, but I can't get a coherent writeup." The other someone then prompts an LLM
> and the race is on to see who has something publishable first.

**M2 — a shared list.**

> Two groups are working off a known open-conjectures list using LLMs.

Under M1 the correlation lives in the **social layer** — one description travelling between
people. Under M2 it lives in the **target layer** — no communication at all, just two
parties drawing from the same short public list of attractive problems. Neither needs any
claim about models converging, and under both the clustering of *announcement dates* is
evidence about publication incentives, which reward being first, rather than evidence about
when anything was discovered.

M2 has the advantage of being **measurable from the corpus**, because the corpus records
which list each problem came from. Arm AR (`ar/base_rate_concurrency.py`, 7/7) measures it.

## The disconfirming fact was already in my own report

Arm AN, four paragraphs before the inference it supports, records:

> Kintali, *Three-Bit Flows and Cycle Covers Part I*, arXiv:2607.14140v1 (13 July 2026),
> whose §11 explicitly compares itself to OpenAI's: *"OpenAI's proof is linear-algebraic
> while our proof is graph-theoretic... Both papers share the high-level flow to label
> arguments."*

OpenAI announced 10 July. Kintali posted 13 July **citing it**. The two CDC artifacts are
not two independent events; they are one announcement and one response. The shared
"high-level flow to label" route — which I read as common-mode error, i.e. as a fact about
model methodology — is fully explained by the second author having read the first. I had
the citation in hand and drew the opposite inference from it.

## M2 measured

From the 664-entry VibeMathed snapshot (day-precision on 647; 410-day window):

| quantity | value |
|---|---|
| mean claim rate | **1.58 / day**; busiest single day **25** |
| pairs of claims falling within 3 days of each other | **12,231** of 208,981 |
| entries whose problem was **posed by Erdős** | **109 (16.4%)** |
| entries **sourced from erdosproblems.com** | **124 (18.7%)** |

One eighty-year-old problem list supplies roughly a sixth of everything in the corpus. That
is mechanism M2 observed rather than hypothesised.

The birthday arithmetic on that sub-list alone, with **uniform** draws (the conservative
case — real attention is fame-weighted, which shortens the effective list and raises the
collision rate):

| nominal list size | expected same-problem pairs, whole window | within 3 days |
|---|---|---|
| 600 | 9.81 | 0.57 |
| 1100 | 5.35 | 0.31 |
| 1500 | 3.92 | 0.23 |

**Read this honestly: it does not by itself explain three near-simultaneous instances.**
0.31 expected collisions within three days is below one, and two of the three observed
instances are not Erdős problems at all. What the number establishes is weaker and
sufficient: same-problem collisions are an *expected feature* of a corpus assembled this
way, at single digits over the window, so no instance of one is evidence of anything on its
own. The work of dissolving the pattern is done by the case-by-case reading below, not by
this arithmetic.

## The three instances are not three instances

Re-read against the deflation, the instances separate by mechanism:

| pair | gap | same object? | mechanism |
|---|---|---|---|
| CDC — `openai/cdc-lean` (10 Jul) vs Kintali (13 Jul) | 3 days | same conjecture, shared high-level route, **second cites first** | **social transmission — established, not inferred** |
| prime gaps, 2026-09-03 — **three** claims, not two: `H₁ ≤ 212` (Axiom Math, sig 62), `H₁ ≤ 186` (OpenAI, sig 62), *Maximal prime-gap lower bound* (OpenAI, sig 60) | same day | **no** — three distinct objects, different bounds, different conditionality, different methods | **M2.** Polymath8b's 246 is a public record with a known ladder. Counting this as a "pair" was itself an error: one of the three is a lower-bound result on a different question |
| Nevanlinna — He–Zhang (25 Aug) vs 2608.26062 (26 Aug; release 24 Aug) | 1 day | **no** — different domain, different obstruction, different divergence engine | **M2, settled below.** Both descend from EKS26 (revised 24 Jul 2026), which poses the question as a numbered Question and names λ as the starting point. `ar/verify_hezhang.py`, 27/27 |

**The count collapses.** Of three instances: one has transmission established from the
artifact's own text, one is three different results descending a public ladder on a busy
day, and and one is two different constructions from one shared ancestor (settled below once
He–Zhang arrived). That leaves **n = 0 unexplained**. "Too frequent to be coincidence" required n = 3 independent events,
and there were never three.

## Supporting evidence for the deflation, from the Nevanlinna transcript

The prompt sequence translated in `aq/PROMPTS_nevanlinna_translated.md` exhibits the exact
shape the mechanism predicts, inside a single session:

1. **The find and the write-up are separate steps by separate models.** Prompt 2 is one
   sentence — *"Then please write the proof up as complete English LaTeX code for me"* —
   and prompt 3 is addressed to a *different* model (那个LLM, third person). "I got an LLM
   to find it but I can't get a coherent writeup" is not a caricature; it is the literal
   prompt sequence.
2. **The priority anxiety is explicit.** Prompt 3: *"If you find that my result is already
   covered by the literature, tell me — then I won't have to write this paper."*

This is evidence that the *practice* the deflation describes is real. It is not evidence
that transmission occurred in this particular pair.

## What survives

The artifact-level conclusion, unchanged in words and **strengthened** in force:

> **Two AI-assisted claims on one problem probably cannot corroborate each other.**

Under the original reading they were non-independent because the models share training
data. Under the deflation the second may have known the first's target and route outright,
which is *worse* for corroboration, not better. Anyone reading "two independent proofs
appeared within a week" as increased confidence in CDC is wrong under either hypothesis,
and most wrong under the one best supported by the evidence.

## What does not survive

- The model-level explanation ("shared training data produces correlated discovery").
- "Too frequent to be coincidence" — an unquantified claim, made without a base rate for
  how many problems were under simultaneous attack.
- The ranking "the single most important thing this programme has noticed." That ranking
  was earned by the model-level reading, which is the part now withdrawn.

## Discriminator, and what separates M1 from M2

The question changes from *why do models converge* to *which mechanism produced each
instance*. The cheap discriminator is **whether the two artifacts are the same mathematical
object**:

- **M1 (seeding)** sends the second party after the first's *specific* target, so it
  predicts the same counterexample or construction, a shared high-level route, and an
  asymmetry in polish between the two write-ups.
- **M2 (shared list)** predicts *different* objects on a common target, chosen for fame
  rather than for tractability, with no route in common and no asymmetry.

CDC is M1 and says so in its own §11. The prime-gap day is M2 — three different objects,
and the third isn't even the same question. Nevanlinna needs He–Zhang, arXiv:2608.24829,
which this session cannot fetch; its release/claim ordering (release 24 Aug, He–Zhang 25
Aug, paper 26 Aug) rules out simple seeding *in that direction* and nothing more.

One further test worth recording: a secondary check in arm AR found that **days carrying
three or more claims are not the high-significance days** (mean significance 17.7 on burst
days vs 14.9 on single-claim days, against a corpus mean of 16.9). Bursts in this corpus are
throughput, not fame — so "several claims landed together" is, by default, a statement about
how fast the pipeline is running.

## M3 — the lists are benchmarks, which is why the bands collide

A third refinement, and the one that explains why M1 and M2 have anything to work with:

> Individuals and groups have been using sites like Erdős problems (among others) for
> roughly a year as benchmarks for frontier models. Model x.1 solves an easy one a year
> ago; model x.2 and model y.2 compete to solve a slightly less easy one six months later.

This is not a fourth route to the same collisions. It changes what the corpus **is**. Under
M3, problem selection is driven by *difficulty calibration against the previous frontier*
rather than by mathematical interest, so competing labs are pushed into the **same
difficulty band at the same time by construction** — no shared conversation (M1) and not
even a shared taste in problems (M2) required. Simultaneity is then the design of the
exercise, not a finding about it.

M3 makes falsifiable predictions. `ar/benchmark_ramp.py` (5/5) tests four:

**P1 — difficulty ramp.** OLS of significance on days since 2025-07-20 over 647 dated
entries: slope **+0.0438/day = +16.0/year**, r = **+0.254**. Monthly means climb
10.7 (2026-04) → 17.5 (05) → 16.5 (07) → 21.6 (08) → 30.7 (09, only 14 entries, thin).

**P2 — the frontier band arrives late.** Splitting the corpus in half at 2026-07-17,
323 entries each side:

| | first half | second half |
|---|---|---|
| significance ≥ 40 | 3 | **22** |
| significance ≥ 50 | 2 | **16** |
| significance ≥ 60 | **0** | **9** |
| max significance | 55 | **68** |

Nothing above 60 exists in the first half of the corpus. That is the shape of a frontier
being pushed, exactly as described.

**P3 — head-to-head days are the harder days.** On 73 of 184 active days, two or more model
makers both posted. Mean significance 18.0 on those days against 15.7 on single-maker days
(+2.3). Competition concentrates where the band is.

**P4 — but the list share falls as volume explodes.** Reported against the check, which only
asked for persistence:

| quarter | curated-list / total | share |
|---|---|---|
| 2025Q4 | 6 / 11 | 54.5% |
| 2026Q1 | 24 / 48 | 50.0% |
| 2026Q2 | 80 / 189 | 42.3% |
| 2026Q3 | 50 / 396 | **12.6%** |

The absolute count holds near 50–80 per quarter while the stream widens sevenfold. So the
curated lists were the **early** benchmark and are now a minority of a much larger flow
sourced from arXiv and self-publication. This fits M3's history rather than undercutting it:
the benchmark phase is visible at the start of the window and has since been outgrown.

**What P1–P4 cannot show.** `significance` is VibeMathed's own curated score, assigned after
the fact. A rising trend is equally consistent with the site's inclusion policy tightening or
with scorer drift, and nothing here separates those from a real capability ramp. The correct
reading is that **the corpus behaves like a leaderboard**, not that the leaderboard measures
what it appears to.

## Consequence for arm AJ's census thesis

AJ concluded that *checking is inversely related to significance*. If significance is partly
a benchmark-difficulty coordinate rather than a mathematical-importance coordinate, the
thesis should be restated: what goes unchecked is the **frontier band** — the problems
selected precisely because they sit just past what was previously solvable. That is a
sharper claim than the original and points the same way: verification effort lags capability,
and it lags hardest where the selection process is deliberately hardest. The AJ correlation
itself is unaffected; only its interpretation moves.

## The Nevanlinna instance is settled: M2

He–Zhang, arXiv:2608.24829v1, arrived after the discriminator was declared. Scaffolding
checked in `ar/verify_hezhang.py` (**27/27**), then the test run.

**Twenty-seven checks on He–Zhang's computable content.** λ = ϑ₂⁴/ϑ₃⁴ real on the imaginary
axis, 2-periodic, omitting 0 and 1; the cusp expansion λ = 16q + O(q²) with the remainder
ratio settling on **128** exactly; Lemma 4.1's Stern–Brocot bounds `q+s ≥ m+2`, `qs ≥ m+1`
**attained at every depth** by the spine (1, m+1), so the estimate is tight rather than
slack; children inside the parent half-disk, checked in exact rationals; the bays
`B_n = [6n, 6n+4]` disjoint with `J_n ⋐ int B_n`; `Im z_{c,d} = 1/(c²+d²)` over 89 primitive
pairs with the fourfold stabiliser multiplicity; `N(R) = (6/π)R² + O(R log R)` to **0.1%** at
R = 160; the anharmonic group (3.1) closed and of order 6; Lemma 6.2's Möbius identities
`A(v+it) = a/q + i/(q²t)` and `A(u) − a/q = −s/(q(qr−ps))` exact; and §8's Edrei bound
`ρ(F) ≤ 1`, forcing infinite order and `δ(0) = δ(1) = δ(∞) = 0`.

**Two checks failed on the first run; both were my test's fault, not the paper's.** I used
`6/π²` for the lattice count where the paper says `6/π` — `6/π²` is the coprime *density*,
`6/π` the count in a disk of area `πR²`, and the paper is right. And I computed the
determinant of `A = [[a,b],[q,−p]]` as `aq − bp` instead of `−(ap+bq)`. Corrected, both pass.

**The same-object test.**

| | He–Zhang (25 Aug) | AQ paper 2608.26062 (26 Aug) | |
|---|---|---|---|
| target | Nevanlinna half-plane, Question 1.1 | same | **same** |
| common ancestor | EKS26 Question 2, arXiv:2604.06136 | EKS26 | **same** |
| starting function | modular λ, Γ(2) | modular λ, Γ(2) | **same** |
| **the domain** | boundary is a chain of **Farey edges**, Stern–Brocot mediant refinement in disjoint bays, chosen by a diagonal procedure | boundary is the **graph of a Gaussian-perturbed function**, bi-Lipschitz with δ = 2ε/√π ≈ 0.00113 | **different** |
| **the obstruction** | **Green energy / spherical area**: `∫_Ω G_Ω(i,z)(λ^#)² dA = ∞`, via Ahlfors–Shimizu and Riesz decomposition | **Blaschke condition**: `Σ G_ℍ(i,z_n) = ∞` over an explicit Γ(2) orbit | **different** |
| **the divergence engine** | log-mean of λ via Jensen plus coprime lattice counting | `Σ φ(2m)/(m² log m)`, a totient series | **different** |
| extension to ℂ | Schwarz reflection across Farey edges | Schwarz reflection | same (forced) |
| authorship | 2 named humans, Fudan + Xi'an Jiaotong | 7 human collaborators | different |

**All three load-bearing components differ.** What the two share is precisely what EKS26
hands out for free: the target, its question number, and λ as the function that already
omits three values on ℍ without being of bounded type.

**M1 predicted the same object, a shared route, and an asymmetry in polish. None is
present. M2 predicted different objects on a common famous target. That is what is there.**

The shared ancestor is cited rather than inferred: He–Zhang's Lemma 3.1 is proved *"following
the idea of [EKS26, Lemma 6]"*, they thank Eremenko, Kulikov and Sodin in the
acknowledgements, and they record accessing the revised EKS26 PDF on **24 August 2026** — the
same day as the other paper's timestamped release. EKS26 was revised 24 July 2026. Two groups
read a month-old preprint that *poses the question as a numbered Question* and *names the
starting function*, and posted a day apart.

This is the list mechanism at its highest resolution: not a generic catalogue of open
problems but a specific recent paper that supplied the target and the first move. No
communication between the groups is required, and none is in evidence.

**The count is now zero.** Of three instances: CDC is established transmission from the
artifact's own text, the prime-gap day is three different results on a public ladder, and
Nevanlinna is two different constructions from one shared ancestor. **No instance remains
unexplained.** The hypothesis is fully retracted, not merely demoted.

## M4 — incidental refutation, and why the corpus cannot see it

A fourth mechanism, reported first-hand by this programme's operator:

> Independent researchers X and Y attempt, with LLM assistance, to make progress on a
> well-known open problem. In the course of work each LLM finds a twenty-year-old paper
> carrying a conjecture which, if true, makes the problem at hand more tractable. While
> stress-testing that conjecture, each LLM finds a counterexample to it — and the two
> counterexamples are different.

**M4 is structurally unlike the other three.** The collision target is not the problem
either party set out to solve; it is an auxiliary conjecture surfaced by the *retrieval
layer* as relevant prior art. That target is typically obscure, carries no list membership
and has no audience. The two parties need not share a top-level goal at all — only a
sub-goal their tools chose for them.

**It is also the one mechanism in this series that is genuinely about models — narrowly.**
Shared retrieval over a shared literature produces correlated *sub-target selection*. It
does **not** produce correlated error: the operator's account has the two counterexamples
differing, which is the same signature M2 leaves on the same-object test. So M4 revives a
strict subset of what I originally claimed and refutes the rest. My claim was "shared method
plus shared training data produces correlated discovery **and therefore correlated error**."
The second half stays dead.

### The test, and its null result

`ar/m4_incidental_refutation.py` (6/6 checks, but **4 of 5 declared predictions did not
survive**). Every comparison carries a significance test, because the hypothesis this whole
document exists to correct was an uncounted eyeball pattern.

| prediction | result | statistic |
|---|---|---|
| **P1** disproved problems are younger | **null** | Mann–Whitney z = −1.48, **p = 0.138** (medians 27y vs 31y) |
| **P2** disproved entries sit lower in significance | **refuted, opposite direction** | z = +2.61, **p = 0.009**; disproofs mean 18.2 vs 16.4 |
| **P3** disproved entries are less list-sourced | **marginal** | z = −1.88, **p = 0.060** (22.4% vs 29.5%) |
| **P4** an M4 band: age 10–30, sig ≤ 20, unlisted | **null** | z = +1.10, **p = 0.271** (12.7% vs 9.8%) |
| **P5** construction dominates disproofs | confirmed but **definitional** | z = +18.6, p ≈ 5·10⁻⁷⁷ — a counterexample *is* a construction |

**P4 is the one this arm came closest to publishing as a finding.** The band is populated —
26 entries, and they read exactly like the mechanism: *Carlitz–Wieferich primes* (11y),
*AdaBoost cycling* (14y), *Steurer's conjecture* (16y), *Strong Graph Reconstruction* (16y),
all `construction`. A populated band whose contents look like the story is not evidence for
the story when the same band is almost as populated among proofs. p = 0.271. Killed by its
own test, one step before it would have gone into a report.

### Why the null is uninformative about M4, and what that itself shows

The corpus cannot see this mechanism, for three reasons that are themselves the finding:

1. **M4's own logic predicts non-publication.** These refutations are working byproducts of
   an unfinished attack on something else. That is exactly what does not get written up. The
   corpus indexes published claims.
2. **P2 measures the selection directly.** Refutations here skew toward *famous* conjectures
   (p = 0.009) — a corpus assembled from newsworthy results hides the obscure-auxiliary
   class by construction. The failed prediction is better evidence than the passed ones.
3. **The decisive field does not exist in the schema:** what the session was *originally*
   after. Nothing distinguishes a conjecture attacked on purpose from one met on the way to
   something else.

**What would test it:** process artifacts, not outcome records. The Nevanlinna transcript in
arm AQ is the only one this programme has seen, and one transcript is not a rate.

### The consequence, which holds whatever the rate turns out to be

Under M1–M3 the colliding artifacts sit on a famous problem, so the community eventually
looks. **Under M4 the collision is on an obscure conjecture nobody is watching, which may
have been load-bearing for conditional results for twenty years.** Two independent
refutations can both exist, neither be published, and the dependent literature never learn.

That is a worse failure mode than anything the original concurrency hypothesis described,
and it is invisible to every instrument this programme has used so far.

## Error class

Same shape as the rank-429 badge inference and the Fable contamination flag: a structural
reading asserted over evidence that was available and said otherwise. Here it compounds:

1. the contradicting line (Kintali citing OpenAI) was **in my own report, in the same
   section** as the inference it refutes;
2. I never counted the events I was calling too frequent for coincidence, and one of the
   three was not the event I described — it is three claims, not two;
3. no base rate was computed, although the corpus needed to compute it was already cloned
   and already censused in arm AJ.

The general fault is treating simultaneity as a signal without first asking what the
arrival rate was. At 1.58 claims/day against public target lists, simultaneity is the
null hypothesis.
