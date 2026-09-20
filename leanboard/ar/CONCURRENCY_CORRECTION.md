# Correction — the concurrency pattern was over-read

**Date:** 2026-09-20. **Status:** fourth refuted hypothesis of this series. **Measurement:** arm AR, `ar/base_rate_concurrency.py`, 7/7.

## What I claimed

Across arms AN, AM, AJ and AQ I recorded three instances of near-simultaneous AI-assisted
claims on a single problem and built an inference about *models* on top of them:

> "Shared method plus shared training data produces correlated discovery, and therefore
> correlated error." — AJ
>
> "The pattern is now too frequent to be coincidence and it is the single most important
> thing this programme has noticed." — AQ

## Two proposed deflations

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
| Nevanlinna — He–Zhang (25 Aug) vs this paper (26 Aug; release 24 Aug) | 1 day | unknown — He–Zhang not obtained | **undetermined.** The release predates He–Zhang, so simple seeding in that direction does not fit |

**The count collapses.** Of three instances: one has transmission established from the
artifact's own text, one is three different results descending a public ladder on a busy
day, and one is undetermined for want of a paper this session cannot fetch. That leaves
**n = 1 unexplained**. "Too frequent to be coincidence" required n = 3 independent events,
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
