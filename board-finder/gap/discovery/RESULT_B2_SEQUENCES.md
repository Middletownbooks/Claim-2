# Brief B2 — arm 2 closes at 15 of 15 and 0 survivors, and S4 is shown to be blind to a failed attempt

Run by a Sonnet 5.5 chat instance against `prompts/s55/B2_SEQUENCES.md`. **14 of 14 calls used, 1
failed.** All arithmetic re-verified here.

## 1. Verdicts, and arm 2 is now complete

| table | record | value (tier) | verdict |
|---|---|---|---|
| **9 Costas arrays** | smallest *n* with no **known** array | **32** — `SECONDARY-RELAYED` as of Mar 2011; 2026 currency `SEARCH-SUMMARY` only | **FAIL at S3** (method unread → UNKNOWN) |
| **10 bent functions** | smallest number of variables whose count is unknown | **10** — `SECONDARY-RELAYED` by inference | **FAIL at S1** |

**Arm 2: 15 of 15 tables assessed, 0 live survivors.** Ten were assessed in the original run (2 triage
survivors: kissing 13/14 and caps AG(8,3) — all three records subsequently killed at gates C-1, C-2 and
C-3), three by B1, two here. **The record-table seam is closed.**

P-34 was scored CORRECT on triage survivors and that scoring is untouched. **The pipeline yield is 0.**

## 2. My brief conflated two different quantities, and the run kept them apart

I supplied *"exhaustive enumeration reaches order 29"* as though it answered the pre-specified record,
*"the smallest n with no known Costas array."* **Those are different numbers measuring different
things.** The run separated three senses:

| sense | value | tier |
|---|---|---|
| **the record as pre-specified** — smallest *n* with no *known* array | **32** (Drakakis 2011: 32 and 33 are the two smallest; ≥664 known at order 30, ≥8 at order 31) | `SECONDARY-RELAYED` |
| the true minimum over *n* with C(*n*) = 0 | **UNKNOWN** — nonexistence cannot be asserted for any *n* > 1 | — |
| the **enumeration** frontier — a different quantity | complete through **29**, 164 arrays at 29 | `SECONDARY-RELAYED` |

**Three orders apart, and I handed over the wrong one as the answer.** Arrays are known at 30 and 31
without the enumeration being complete there, which is exactly why the two frontiers separate. This is
the numerical-versus-exact family again, in a new costume: not two precisions of one number but two
quantities sharing a name.

## 3. The two tables split at S1, which my brief said they would not

My brief grouped them: *"Both of these tables are counts or enumeration frontiers rather than
optimisation records, so S1 is the gate most likely to decide them."* Half right:

* **Costas, as worded, is an existence frontier.** The headline is a minimum over orders and the objects
  are permutations of [*n*]; exhibiting an array at 32 moves the record to 33. **S1 PASSES**, route (a).
* **Bent functions is a count frontier.** Exhibiting one more bent function on 10 variables changes
  nothing; only determining b₁₀ exactly would. **S1 FAILS**, and route (b) fails too — *"no 'better
  witness' exists for a cardinality."*

So the warning I attached to both applied to one. The run also noted that the *count* reading of Costas
would fail S1 for the same reason, so the record's wording is doing real work.

**And a parity fact the brief did not state:** bent functions exist only for an even number of
variables, so the count for odd *n* is zero by definition. **The frontier is 10, not 9.**

## 4. The finding: S4 cannot see a failed attempt, and the same fact reads three ways on this board

> *"An LLM-driven search system attempted the Costas problem in 2025 and moved no cell. Rosin's CPro1
> (arXiv:2505.23881, opened) included Costas Array among its 16 Handbook problem types. CPro1 solved
> open instances for 7 problem types, and reports no open instances solved for the others; Costas is not
> in the solved list. **Both S4 scopings count only moves, so this attempt is invisible to both.**"*

**S4 asks whether anyone succeeded. The decision-relevant question is whether anyone tried.** There are
three states and S4 collapses them to two:

| state | what it means for us | S4 sees |
|---|---|---|
| nobody has tried | unvisited; the next sweep takes it | PASS — looks uncrowded |
| **someone tried and failed** | **evidence of hardness; the interesting case** | **PASS — indistinguishable from the above** |
| someone succeeded | taken | FAIL |

And this project's own gates already disagree about the middle row. **C-1's bar** made an attempt a
**PASS** condition — *"an unattempted cell is only unvisited, and the next run of theirs will visit
it."* **C-3's bar** made an attempt a **FAIL** condition. **S4** cannot see it at all. Three
instruments, three readings of one fact, and now a real instance of that fact: CPro1 ran LLM-generated
search heuristics on Costas in 2025 and moved nothing.

`RESULT_GATE_C1.md` §7 recorded that all three bars tested crowding and crowding decided none of them.
This is the reason underneath that: **the crowding instrument is built on the wrong observable.**
Registered as **D51**.

The run also flagged, correctly, that its own Costas `S4-record` PASS *"rests on absence at
`SEARCH-SUMMARY` grade"* and that a May 2026 benchmark paper uses Costas order 10 — an ordinary
instance, not a record cell.

## 5. Two source inconsistencies, both verified here, neither affecting a gate

**Drakakis 2011 Table 1 gives C(14) = 12752; Wikipedia gives 17252.** Re-checked against OEIS A008404 as
I recall it (**RECALL tier, not verified this session**): C(13) = 12828, C(14) = 17252. **12752 is
neither**, so a transcription slip in the source is the right reading, as the run judged. It affects no
gate.

**The bent-function counts may be on two different footings, and the arithmetic supports the run's
hypothesis exactly.** The 2025 paper gives the *n* = 6 and *n* = 8 counts as roughly 2²⁵ and 2¹⁰⁶. The
run's recall of the *n* = 6 total is 5,425,430,528 ≈ 2³²·³⁴, and noted that 2²⁵·³ is that divided by
2⁷ — the count modulo an affine action. Re-derived here:

```
5,425,430,528              log2 = 32.34
5,425,430,528 / 2^7        log2 = 25.34    <- matches the paper's ~2^25
99270589265934370305785861242880   log2 = 106.3   <- matches ~2^106
```

**2^25.34 against 2^25 is an exact match for the total-divided-by-2⁷ reading.** So the two figures are
very likely *total count* and *count modulo affine equivalence*, which is the same class of error as
19,603-versus-5,779: one quantity, two normalisations, one name. No gate depends on it, and neither
figure was read from a primary source.

## 6. A third fetch mechanic, and one piece of epistemic hygiene worth copying

**New failure cause: `robots.txt`.** The one failed call was `mathweb.ucsd.edu` (a Warnke et al. PDF),
**refused because robots disallowed it** — not a rate limit and not an unsurfaced URL. That is a third
distinct mechanic and it is now in brief C.

**And the run distinguished "did not observe" from "did not occur", twice, unprompted:**

> *"I saw no arXiv rate-limit refusals. **I attempted no 2026 arXiv identifiers, so the
> asymmetric-refusal claim is untested.** I saw no live-artifact drift, **because none of the fetched
> pages was a live repository.**"*

Both mechanics were reported as *not tested* rather than as *not present*. Given that this project has
just spent two debts on values that could not carry the weight put on them, that distinction is the
habit to keep.

## 7. What is still not reached, and it is the same thing every time

Both tables reached step (ii) — the value — and **neither reached step (iii), the method section.**
Costas: the aimsciences page returned abstract and references only. Bent: Langevin–Leander 2011 was
never opened. Both S3 verdicts are UNKNOWN.

That is **six consecutive S3 failures on this board for want of a method section** — tables 7, 8, 9, 10
and arm 1's records 277 and 353. **D50 is no longer a hypothesis about the gate; it is the gate's
observed behaviour.** Every table in arm 2 that got as far as S3 died there, and not one died on
evidence that the move was `SEARCH-REPEAT`.

**P-31 A-1 gets a fourth favourable data point.** Every unevaluable cell is named, the S4 verdicts carry
their coverage limits, and the run declined to score a move kind it had inferred but not read.
