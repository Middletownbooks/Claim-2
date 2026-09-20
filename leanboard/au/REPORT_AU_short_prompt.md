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

**The artifact was first** — the disproof of C = 1 is its own — **and was overtaken on the
constant within nine days.** Neither fact is visible from the document, which carries no
references and no statement of what was known. A reader cannot tell whether it is first,
current, or superseded.

That is the same gap flagged in arm AQ's prompt translation and again in arm AS on the Chow
LaTeX. Across five process artifacts it is the most consistently absent instruction, and the
only one whose absence has now cost something observable in three separate cases.

**n = 5. Still a taxonomy, not a rate.**
