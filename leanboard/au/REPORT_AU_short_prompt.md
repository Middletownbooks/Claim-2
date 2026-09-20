# Arm AU — the short prompt, and what it does to arm AT's claim

**Input.** Four conversational prompts, roughly sixty words in total, no agent architecture,
no output bans, no checklist:

> 1. *"Construct a counterexample to general (non-planar) case of Dinitz Garg Goemans
>    conjecture. You should do a breakthrough and find a structured counterexample."*
> 2. *"please continue research and find a complete unconditional counterexample"*
> 3. *"Continue the search. Have a clear strategy obtained from deeper understanding of the
>    problem structure."*
> 4. *"it's enough of partial results. let's finish with a complete unconditional
>    counterexample"*

**Output.** A finite arithmetic certificate: seven vertices, nine arcs, two source–terminal
paths per terminal, eight routings.

## The mathematics checks completely — `verify_ssuf.py`, 19/19

Recomputed with exact integers from the instance alone. Flow conservation at every node;
source outflow 40 = 15 + 10 + 15; fractional cost 2·10 + 3·6 + 2·10 = **58**. Path
enumeration confirms **exactly two** s–tᵢ paths per terminal, so the eight routings really are
exhaustive. Every Eᵢ routes at cost exactly 30 and every Zᵢ at zero. All eight routings
recomputed: four satisfy every additive-`dmax` bound, at costs **90, 60, 60, 60**; the other
four each use two or more Zᵢ and each violates a bound, with the document's excesses exact
(three singles of 1, then 1 + 11 + 1 on the all-Z routing). Cheapest capacity-good routing
**60 > 58**. The structural form in exact rationals: ⅓ + ⅖ + ⅓ = **16/15 > 1**, and all three
normalized inequalities hold strictly at b = ⅔, r = ⅓, q = ⅖.

One check failed on my first run — **my** miscount of the violation list (five entries where
the table has six). The document was right.

**The planar wording is not an error.** The prompt asks for the "general (non-planar) case"
and the artifact is planar. Planar instances are a subset of general ones, so a planar
counterexample refutes the general statement a fortiori. The artifact is stronger than the
request.

## This breaks the confound arm AT part 2 could not resolve

| artifact | search stage | output stage | core reached | prompt |
|---|---|---|---|---|
| Nevanlinna | elaborate | nothing | **0%** | ~800 w |
| CDC | most elaborate of the set | nothing | **0%** | ~900 w |
| Allikvere | modest | four features | **100%** | — |
| LaTeX to author | modest | four features | **100%** | — |
| **SSUF** | **four casual sentences** | **finite object** | **100%** | **~60 w** |

Prompt length and output-stage features were perfectly correlated across the first four
artifacts, so nothing separated them. **The shortest prompt in the set produced the most
checkable artifact.** Length is not the variable.

## The four separating features collapse to one

SSUF carries **two** of the six specification items — a finite deliverable, and a proof that
stands without machine work — and verified 100%. It has no separately written checker and no
control. And feature 4 follows from feature 1: once the object is finite and small, the
hand-checkable proof *is* the enumeration.

**AT's prediction survives in a narrower form:** an artifact whose deliverable is a finite
object is verifiable at the cost of reading it, whatever the prompt; one whose deliverable is
an existence argument is not, however elaborate the search that produced it.

The control keeps its separate justification from AT part 2 — it is what calibrates a search
forbidden to report failure — but it is **not** what decides the audit surface. Part 1 ran
those two claims together and this case separates them.

## Two things the short prompts did anyway

**The output ban, at five per cent of the words.** Three of the four prompts express
dissatisfaction with partial results. That is functionally the same mechanism CDC states
formally (*"Do not return a reduction, partial result, isolated missing lemma, best-effort
summary"*) and Nevanlinna states as three forbidden sentences — here delivered across turns as
four impatient lines. Whatever the long prompts' bans buy, it is not something only a long
prompt can buy.

**Statement fidelity, unrequested.** The prompt says "Dinitz Garg Goemans conjecture". Per the
corpus the DGG result is the *congestion* statement; the cost-preserving strengthening is
*Goemans'* conjecture — *"Goemans conjectured C = 1"*. The artifact retitles itself **"Goemans'
SSUF Cost Conjecture"** and states the cost version precisely. It corrected a loose prompt.
CDC bought the same property by pinning every definition at length; here it came free. One
case each — not a claim that pinning is unnecessary, only that it is not the sole route.

## The one axis where the short prompt cost something

The corpus entry *Common-Point Interval Systems for SSUF* (2026-07-31) records:

> *"Goemans conjectured C = 1; this was disproved in July 2026 by a separate **seven-vertex**
> counterexample with critical constant **16/15** (see the Dinitz–Garg–Goemans entry),
> leaving the optimal C open."*

The artifact has exactly seven vertices and its own §7 computes 16/15. Two independent
parameters match: **this is that counterexample.** The corpus carries it as
*Dinitz-Garg-Goemans*, 2026-07-22, significance 20, `disproved`, **`unreviewed`**.

What happened next, from the same corpus:

| date | entry | |
|---|---|---|
| **2026-07-22** | **this artifact** | C > 1, critical constant **16/15 ≈ 1.0667** |
| 2026-07-23 | Four-terminal planar DGG | four terminals, planar |
| 2026-07-31 | Common-Point Interval Systems | **C ≥ 1.28249…** |
| 2026-08-04 | Four-terminal scenario ladder | exact envelope ladder |
| 2026-08-13 | 1.17353 planar bound | C ≥ 1.17353 for planar instances |

**The artifact was first** — the disproof of C = 1 is its own.

### Correction: the successors are descendants, not competitors

I first wrote that it "was overtaken on the constant within nine days" and that "a reader
cannot tell whether it is first, current, or superseded", presenting the missing references
as a cost. **That is wrong, and the corpus says so in the entries' own words.**

This was immediate big news, and the later results were built on it. `relations` edges in the
corpus, unprompted by me:

- *Common-Point Interval Systems* → **`builds-on`** → `dinitz-garg-goemans-unsplittable-flow`:
  *"The optimal-constant question this entry attacks is exactly what the Dinitz–Garg–Goemans
  disproof left open."*
- *Four-terminal scenario ladder* → `related` → the same slug.
- *1.17353 planar bound* → `continues` → the 1.28249 entry: *"Part III of the same programme."*

Being superseded in nine days by work your own result enabled is impact, not a cost. The
absence of references cost nothing, because the field already knew.

### What has to be withdrawn

The claim that literature placement's absence "cost something observable in three separate
cases". Re-examined, **none of the three is a cost**:

- **Nevanlinna** — the instruction was *present*. Prompt 3 asks *"if you find that my result
  is already covered by the literature, tell me"*, and the model reported a negative search
  honestly and recommended expert confirmation. It worked.
- **Chow LaTeX** — omits Harvey–Király–Lau, but was sent directly to the conjecture's author,
  who knows his own literature.
- **SSUF** — big news from the outset.

**Confirmed costs: zero.** Withdrawn entirely, not softened. What survives is only a fact
about the prompts: literature placement is the most consistently absent instruction across
the five. Its consequence is unevidenced.

### The same error, for the third time

1. **Concurrency** — I read near-simultaneous claims as evidence about models converging. The
   channel was social. (arm AR)
2. **M4** — I wrote that two independent refutations could both exist and *"the dependent
   literature never learn"*. A preprint existed and the author was written to by **both**
   researchers. (arm AR)
3. **SSUF** — I read missing references as a cost. The result was news and the successors
   built on it. (here)

**I keep treating the document and the corpus as the channel. The channel is social.** Each
time, what I called missing from the world was only missing from my instrument.

### What the corpus is good and bad at — `cascade_visibility.py`, 8/8

**Only 14 of 664 entries (2.1%) carry a `relations` field at all. Five of those fourteen are
this one chain** — 36% of the corpus's entire relation graph, on a single cascade.

| | seed | entries | relation edges |
|---|---|---|---|
| **SSUF** | loud — immediate news | **5** across three weeks | **5** |
| **Chow C(3)** | quiet — preprint + a letter | **0** | **0** |

Chow's C(3) is not in the corpus at all, though White's conjecture and Rota flat unimodality
are. Both cascades are real and comparably structured — a seed, a second independent finder,
downstream work. The difference in visibility is **newsworthiness of the seed**, not anything
about the work.

### Where the instruction would matter

Not where it has been shown to cost — nowhere has. Where the social channel is thin: a quiet
result on an obscure target. That is exactly the M4 class from arm AR, and exactly where the
operator's own case sits, in which the two independent finders learned of each other only
because both wrote to the same author.

Stated as a conditional with no confirming instance, which is what the evidence supports.

**n = 5. Still a taxonomy, not a rate.**
