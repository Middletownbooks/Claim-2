# Brief B1 — 0 of 3 survive, a third crowding scoping appears, and S3 is revealed as an access gate

Run by a Sonnet 5.5 chat instance against `prompts/s55/B1_DESIGNS.md`. **20 of 20 calls used, 1
failed.** Full ledger in the response. All derivations below re-verified here.

## 1. Verdicts

| table | record | value (tier) | verdict |
|---|---|---|---|
| **6 Williamson** | smallest odd order with existence open | **65** — but "orders below 65 are settled" is `SECONDARY-RELAYED` while **"65 itself is unresolved" is `SEARCH-SUMMARY` only** | **FAIL at S0** — not evaluable at a usable tier |
| **7 Steiner** | smallest open admissible case | **S(2,6,51)**, `SECONDARY-RELAYED` | **FAIL at S3** — move kind UNKNOWN |
| **8 cyclic difference sets** | smallest open (v,k,λ) | **(1561,105,7)** by *k*, `SECONDARY-RELAYED` | **FAIL at S3** — move kind UNKNOWN |

**Arm 2 now stands at 13 of 15 tables assessed and 0 live survivors.** Tables 9–10 remain with B2.

Derivations re-checked here: S(2,6,51) has 51·50/30 = **85** blocks and 51 ≡ 6 (mod 15) is admissible;
S(2,7,43) is a projective plane of order 6 and **6 is not a sum of two squares**, so Bruck–Ryser
excludes it; S(2,7,49) is the affine plane AG(2,7) and exists. All as the run stated.

## 2. The finding: crowding has a **third** scoping, and it corrects something I wrote

`RESULT_ARM2_TABLES.md` §3 proposed scoping crowding to the **table** rather than the record. B1 asked
for both and got a third:

> *"In the same La Jolla repository family, the signed difference set table was swept in Aug–Sep 2026.
> A GitHub project resolved all 68 of its open small entries (16 exist, 52 do not). **Its README
> discloses extensive OpenAI Codex use.** … I read that README in full. It is a different object from
> cyclic difference sets, so I did not count it against S4-table. **It is a third scoping
> (repository-family), which would be FAIL.**"

The adjudication is correct — signed difference sets are not cyclic difference sets, and the run did
not stretch the gate to reach them. But the fact matters more than the verdict.

**`RESULT_GATE_C1.md` §6 and `QUEUE_V3.md` both say the design-theory seam is "not on EinsteinArena's
board", which the run confirms: none of Williamson, Steiner or cyclic difference sets appears in its
fifteen problems.** I then treated that as the seam being unswept. **That inference was wrong.** The
signed-DS sweep needed no board, no leaderboard and no platform — a GitHub project with an LLM coding
assistant cleared 68 open entries in a La Jolla-family table in two months. **Not on a board is not
the same as not being swept**, and the design-theory seam is being entered right now by a route that
no board-based crowding screen can see.

So the scoping question is not record-versus-table. It is **record / table / repository-family**, and
the third is where the activity this project would be competing with is actually appearing.

## 3. S4's wording is ambiguous, and the run flagged it instead of picking

Table 7's `S4-table` is returned as *"PASS on the gate's wording, reading-dependent"*:

> *"51 has not moved. **At least seven other cells were resolved between Nov 2025 and 2026** by
> human-authored group-based computer searches. Neither opened paper mentions an AI system. **If plain
> computer search counts as 'large-scale optimisation tooling', S4-table is FAIL.**"*

Named: Banakh–Hetman–Ravsky (Nov 2025) resolved S(2,6,226) and S(2,6,441); Hetman (Apr 2026) resolved
S(2,7,505), S(2,7,589), S(2,8,624), and S(2,8,225) in *J. Combin. Des.* 2026.

**S4 reads "by an AI-driven search system **or** by large-scale optimisation tooling", and the second
clause has no threshold.** A group-theoretic computer search by three humans either is or is not
"large-scale optimisation tooling", and the gate does not say. Refusing to pick and reporting the
dependency is the right behaviour and it exposes a defect the gate has carried since it was written.

## 4. A second live-artifact divergence — and this one decides a verdict

Brief A found a GitHub README that changed between search and fetch. B1 found worse:

| arXiv:2605.08661 | exhaustive to | existence to | the 65/67 sentence |
|---|---|---|---|
| unversioned PDF (snippet) | 47 | 69 | **present** — "not found for orders 53, 59, 65, 67" |
| v1 HTML, 9 May 2026 (fetched) | **35** | **63** | **absent entirely** |

The follow-up PDF fetch returned no machine-readable text and was not retried, correctly.

**The single sentence that would establish 65 as open exists only in a version the run could not
re-open.** That is precisely why table 6 fails at S0 rather than at a later gate — and it is the
honest verdict, not a technicality. **Two for two across A and B1** on artifacts that differ between
accesses. The rule stands and is now measured: a value that moves between accesses cannot be gated on
at any tier.

## 5. The maintained table contradicts itself, which bears on D46

D46 asks whether a candidate's named table exists and contains the claimed row. For table 8 the answer
is *yes, and it still does not settle the record*:

* The page is real and reachable (`dmgordon.org/difference-sets/`, "Site last updated 2026-08-21") —
  the old hosts `ccrwest.org/diffsets.html` and `dmgordo.github.io` now redirect there.
* **But the open-case data was not visible** — it lives in JSON and notebooks the run could not see. So
  the value came from the maintainer's April 2026 paper, not from the table.
* **And two of the maintainer's own statements disagree.** Baumert–Gordon 2003: cyclic existence for
  *k* ≤ 150 settled **except (419,133,42) and (465,145,45)**. Gordon, arXiv:2501.14924v2 (10 Apr 2026):
  known for all *k* < 105, smallest open cases **(1561,105,7), (2185,105,5), (1111,111,11),
  (465,145,45)**. The *k* = 105–111 cases are absent from the 2003 list; **(419,133,42) is absent from
  the 2026 list and the run found no source resolving it.**

**A table that exists, is dated, is maintained, and whose own maintainer's two papers cannot be
reconciled is a fourth failure mode for D46** — beyond "does not exist" (Edel) and "exists and
matches" (Cohn). The row was not readable and the prose contradicts itself.

## 6. The Williamson route does not reach this project's target anyway

The run checked, and it is worth having in writing:

* 668 is the smallest order with no known Hadamard matrix (confirmed from the v1 text).
* A Williamson matrix of order *m* gives a Hadamard matrix of order 4*m*.
* **Order 65 gives H(260), which is already known.** Reaching **H(668) needs Williamson order 167**,
  re-derived here: 668/4 = 167 and 4·167 = 668.

So even a settled 65 would not touch the live target. The brief said Williamson "is directly adjacent
to the only live target this project holds" — **adjacent in machinery, 102 orders away in reach.** My
wording overstated it.

## 7. The 2006 contradiction, resolved definitionally

From the 2019 *J. Symb. Comput.* paper read in full: Kotsireas–Koukouvinos 2006 gave **constructions in
all even orders to 22** and an **exhaustive search only to 18**; complete even-order enumeration then
reached **44** (Bright's 2017 thesis) and **64** (AAAI 2018).

So *"K–K reach 18"* stands, and *"no even-order enumeration before AAAI"* is best read as **"first
complete enumeration over n < 65"**. Two caveats the run stated: the AAAI abstract's claim was seen
only as a snippet, and the JSC paper **shares authors with the AAAI paper**, so this is not an
independent resolution. The 2006 primary was not opened.

## 8. S3 is an access gate, and it is now the binding one

**Tables 7 and 8 both died at S3, and neither died on evidence that the move was compute.** They died
on `UNKNOWN` — *"the 2001 method section was not opened"*. The rule that an unevaluable gate is FAIL is
right and is not in question. But look at what it selects for:

| gate | evidence needed | cost |
|---|---|---|
| S0, S1, S2, S5 | the record's statement and the table | one or two fetches |
| **S3** | **the method section of the paper that last moved it** — often decades old, often paywalled | **highest, and unbounded** |

S3's evidence is the most expensive on the sheet, so **S3 is where runs run out of budget, and its
FAILs are verdicts about our access rather than about the gap type.** Count the recent ones: table 7
(method section not opened), table 8 (same), and arm 1's records 277 and 353 (both CANNOT EVALUATE for
one reason). **Four of the last five FAILs on this board are access failures wearing gap-type
clothing.**

This is not D47 — those bars omitted criteria. This is a gate that is correctly specified and
systematically undecidable at the budget available, which means the screen's output is substantially a
measurement of what we can open. Registered as **D50**.

## 9. The fetch patch worked, measured

| run | calls | failed | rate | causes |
|---|---:|---:|---:|---|
| A (unpatched) | 22 | 4 | **18%** | 3 arXiv rate limits, 1 refused URL |
| **B1 (patched)** | 20 | **1** | **5%** | 1 PDF with no machine-readable text |

**No rate-limit refusals and no refused URLs** — the run searched before fetching and attempted no
recent arXiv identifier, exactly as patched. The call-ledger requirement is what makes this
measurable, and it was itself copied from A's unprompted behaviour.

## 10. What the run did that the brief did not ask for

It reported **two senses** for table 6's value (open-status frontier and enumeration frontier) and
flagged that Lang–Schneider's "Turyn type… up to order 99" may not mean full enumeration at 61. It
marked S1, S2, S3 and S5 for table 6 as **conditional readings** valid only if 65 is open, rather than
reporting them as verdicts on a record whose openness had failed. And it separated *"no maintained
table located"* with the hosts tried from *"none exists"* — the distinction added to the brief after A,
now confirmed as used.

**P-31 A-1 gets a third favourable data point.** Every unevaluable cell is named as such, and the
coverage limits on all three S4 verdicts are stated: only EinsteinArena Table 1 was opened; the
AlphaEvolve repository, PackingStar, X-evolve and Qiushi Engine are all NOT REACHED, so those verdicts
mean *"no move found in what I opened."*
