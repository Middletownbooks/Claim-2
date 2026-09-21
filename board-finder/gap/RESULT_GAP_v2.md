# Gap analysis v2 — result, scored against the prompt's own criterion

Run 20 Sep 2026. Response stored at `sources/GAP_V2_RESPONSE_RAW.md`.

## 1. Did it pass?

`PROMPT_GAP_v2.md` Part B set the bar before the run: **2–4 verified candidates at D = 5**.

Four came back at D = 5 — 3 MOLS(10), Costas 32/33, rank-22 matmul, 4-MUB in ℂ⁶ — so the
criterion is met. But **two of those four are demoted by their own falsification lines**: the
matmul tensor is *"technically excellent and strategically bad"* (multiple agent teams running
that exact search now, one of them stating rank 22 as its original objective fourteen days before
the triage), and the MUB candidate's mod-*p* shadow result says the object probably is not there.

**So: two clean D = 5 candidates, at the bottom of the success band.** That is a pass, narrowly,
and the honest reading is that the named-conjecture literature is thinner than hoped rather than
empty.

## 2. What I verified here rather than relaying

| claim | result |
|---|---|
| Costas: 32 = 37−5 and 33 = 37−4 with 37 prime, while 33 is not prime and 34/35/36 are not prime powers | **exact** — the Golomb/Welch parameter argument holds, so the resistance really is located at the sporadic *q*−4/*q*−5 side conditions |
| 3 MOLS(10) is 300 symbols; C(32,2) = 496; Brent equations 9³ = 729; PTE size 11 ⇒ power sums k = 1…10 | all four correct |
| **the twelve Alpöge Hadamard orders** | see below — this is the one that matters |

**The cross-check.** The response lists twelve orders: 668, 716, 892, 1132, 1244, 1388, 1436,
1676, 1772, 1916, 1948, 1964. `hoa64` ships **thirteen** matrix files. The difference is exactly
**1852**, which hoa64's own README attributes to *Đoković 1992*, not to Alpöge. Two independent
sources, exact agreement, **including the attribution split.** That upgrades `HOA64_ASSESSMENT.md`
§1 from "verified objects, relayed provenance" to "verified objects, provenance corroborated by a
second independent source."

And the apparent contradiction with hoa64 is not one: hoa64 says gaps below 2000 remain at 1212
and 1940 *"(existence proven, construction data still inaccessible)"* — a **library** gap, not an
existence gap. Consistent with "constructions available for every order below 2000".

## 3. Two pool items closed from work already on this branch

**U2 — smallest open Hadamard order above 2000. ANSWERED.** The response could not pin this down
and it is the item most relevant to the existing Hadamard thread. It is in
`Middletownbooks/Cooperative-AI-Defense`, branch `claude/hadamard-matrix-methods-vs79hi`,
`hadamard/findings/FINDING_05`: **thirteen open orders between 2000 and 3000**, indexed by
v = N/4 — 515, 523, 537, 571, 573, 599, 643, 647, 659, 669, 719, 721, 739, i.e. N = 2060, 2092,
2148, 2284, 2292, 2396, 2572, 2588, 2636, 2676, 2876, 2884, 2956.

Smallest is **2060**. But that source also *ranks* them, and 2060 is **10th of 13** — the best
target there is **2284** (v = 571) at 156 free bits, tighter than any of the twelve solved orders.
So U2's answer is not just a number, it is a ranked worklist with an attack already profiled.

**U16 — exact SIC fiducial in an open dimension. RETIRE.** Closed this session, one day before
this triage: `GATE_RESULT_SIC.md` returns **PREFIX, hole list EMPTY** — exact fiducials cover every
dimension through 53 (safe floor) / 57 (probable), the 2017 holes are filled, and above ~57 the
set is a sparse tail at an actively worked frontier (a Grassl seminar three days before the gate).
Under this rubric that is **D = 1**, not a candidate.

**U3 — Williamson, partially answered.** `HADAMARD_CROSS.md` §8: W(179) and W(223) **cannot** be
known, because W(m) ⇒ H(4m) and 716 = 4·179 and 892 = 4·223 were open until August 2026. hoa64's
Williamson database tops out at order 63. That is the shape of the answer; the exact smallest open
*w* still needs the table.

## 4. The finding that corrects my own prompt

> *"The properties that make a problem score well here are the same properties that make a
> benchmark designer select it. The anti-criterion about public lists is not a side constraint on
> this triage — it is in direct tension with the scoring function, and any future run should apply
> it first, as a filter, rather than last, as a check."*

**That is right, and it is a defect in v2's design.** I put the list check in the anti-criteria
section, which is consulted at exclusion time — after candidates have been assembled and scored.
The respondent demonstrated the cost: Conway's 99-graph and the missing Moore graph score
*near-perfectly* on A–C and G–H, are the two best problems in mathematics by this rubric, and are
for exactly that reason both on FrontierMath: Open Problems, one with an agent attack paper
already on arXiv.

**v3 fix: the list check becomes step 0.** Enumerate the agent-facing databases first, build the
exclusion set, and only then cast the net. Four such databases are now known — FrontierMath: Open
Problems, TheoremDB, Horizon/HorizonMath, erdosproblems.com — two of which this project had never
seen. And Epoch's submission criteria *paraphrase this commission*: verifiable by a typical
program on a laptop in under an hour, constructions preferred. **Whatever selection function this
triage runs, Epoch ran a version of it first and published the answer.**

That is the single most consequential output of the run, and it is about the method rather than
any candidate.

## 5. Where I disagree with the ranking

**The Epoch check is a gate, not a caveat, and the run did not treat it as one.** Only ~10 of 50
FrontierMath: Open Problems entries were readable; the remaining forty sit behind a JavaScript
control. So **the four ranked candidates are cleared only against a fifth of the exclusion list.**
3 MOLS(10) and Costas 32/33 could both be on the unreadable forty. The promoting action is named
and cheap — download `open_problems_data.zip` (dated 16 Sep 2026) and diff.

Nothing should start before that runs. This is precisely the SIC-gate pattern: a cheap lookup that
decides whether a programme has a target at all, and the one lesson this project has paid for
twice is to run it *first*.

**Costas should drop below PTE until its status is refreshed.** Its most recent *dated* status
source is Jedwab–Wodlinger **2014**, and the response itself notes the corroborating sources are
*"less precise about the 32/33 frontier."* This project has measured what a stale frontier source
does: recall and old sources both reproduce a snapshot, and both read confident. A 2014 source for
a "smallest open order" claim in 2026 is the weakest link in the document.

**PTE size 11 is the right first target, and the response says so against its own ranking.** Its
E = 5 is the only 5 in that column: extending a height bound and finding nothing is *itself a
paper*, and one exists (Coppersmith–Mossinghoff–Scheinerman–VanderKam 2023). Its status rests on a
2023 paper plus a June 2025 survey — the freshest in the top group. And its D = 4 is *correctly*
scored: the respondent scored the hole at 11 and explicitly refused to score the tail from 13 up.
That is the rubric working as designed.

## 6. Recommendation

1. **Run the Epoch gate.** Download the data zip, diff the full fifty against 3 MOLS(10), PTE 11,
   Costas 32/33. Cheap, and it decides whether anything here survives.
2. **Then PTE size 11**, symmetric-ansatz extension first — bounded, publishable either way, and
   the asymmetric region is genuinely unswept.
3. **Refresh Costas status** before spending anything on it; the Rickard database check the
   response names would do it.
4. **Drop the matmul tensor.** Crowded by teams with more compute, and rank 23 has stood 50 years.
5. **Fold U2 into the Hadamard thread** — thirteen orders, ranked, with 2284 rather than 2060 as
   the best first target.

## 7. What the run says about the fallback

The commission's fallback was: if no unlisted named conjecture suits the criteria, go to the
499-record corpus. **That fallback is now more attractive than it looked**, for a reason the run
surfaced rather than argued: the off-list named-conjecture space is being enumerated into
agent-facing databases faster than a triage can survey it, and the highest-scoring items are
exactly the ones already taken. The 499 corpus's advantage is not that its items score better —
it is that it is **our** enumeration, with collaborative leads attached, rather than a commons
being strip-mined.

The honest synthesis: **two clean candidates here, both gated on a zip file; thirteen ranked
Hadamard orders already in hand from the user's own repo.** The Hadamard worklist is the stronger
position, and it was already ours.
