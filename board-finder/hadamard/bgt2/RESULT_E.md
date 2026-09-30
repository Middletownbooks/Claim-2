# Brief E — `E: FAIL`. Option 3 is dead, and the derivation beat the source's own summary line.

Run 30 Sep 2026 by a Claude Code instance with read access to `Cooperative-AI-Defense`. **18 of 20
calls, stopped on neither limit — the questions were answered.** Verdict: **(a) PASSES, (b) PASSES,
(c) FAIL-UNEARNED.** Everything below re-verified in `derive.py` §15, all assertions passing.

## 1. The 96-against-126 disagreement resolves in my favour, and that is a first

The source's condition, quoted verbatim by the run from `Cooperative-AI-Defense/hadamard/findings/OPEN_ORDERS.md`:

> *"`c = b+1` must divide `v+1` (equivalently `c | m`, FINDING 62)."*

**That is exactly the condition derived in `derive.py` §14 from the worker's structural description.**
`SECONDARY-RELAYED`, and the derivation stands confirmed against the source.

**The reconciliation, all four numbers asserted locally:**

| count | value |
|---|---|
| all 13 orders, *b* > 2, **even *b* allowed** (the source's rule as written) | **134** |
| the **eleven** orders the source's code hard-codes, omitting 669 and 721 | **126** |
| the pairs the source lists **by hand** for 669 and 721 | **8** |
| eleven + hand-added | **134** |
| **odd *b* only — the correct set** | **96** |

**So "126+" is the eleven-order count with even *b* included, plus two orders added by hand. It was
never a count of the admissible set.**

**And 96 is right, because even *b* is impossible.** `Cooperative-AI-Defense/hadamard/findings/FINDING_69_b_must_be_odd.md` proves it and the
proof checks: the border reduces to *S* with *SS*ᵀ = 4*cI* − 4*J*, so the squared row-sum norm is
4*c*(*b* − *c* + 1), which at *c* = *b*+1 is **4*c*·0 = 0**. Every row sum is zero, so each column is a
zero-sum ±1 vector of length *c*, hence ***c* is even and *b* odd.*** Asserted for *b* = 3, 5, 7, 9, 37.
**`Cooperative-AI-Defense/hadamard/findings/OPEN_ORDERS.md` over-counts by including even *b*** — and lists *b* = 4, 66, 334 at *v* = 669 and
*b* = 18, 360 at *v* = 721 among its own examples.

**This is the first time in this programme that a local derivation corrected the source rather than
reproducing it.** Every prior agreement was independent reproduction, which I recorded as "worth
something, not a finding". This one is a finding.

## 2. What actually kills option 3, and it is none of the three clauses

**Admissible does not mean the border exists.** `FINDING_69`: `Cooperative-AI-Defense/hadamard/findings/border_S.py` constructed *S* only for
*c* ≤ 12, and its worklist was cut to 4 < *c* ≤ 12 — *"18 pairs across 8 of the 13 open orders, at
*b* = 5, 7, 9, 11."*

**Reproduced exactly: 18 pairs.** `PRIMARY-VERIFIED-LOCALLY`:

| *v* | order | *b* ∈ {5,7,9,11} |
|---|---|---|
| 515 | 2060 | 5, 11 |
| 599 | 2396 | 5, 7, 9, 11 |
| 647 | 2588 | 5, 7, 11 |
| 659 | 2636 | 5, 9, 11 |
| 669 | 2676 | 9 |
| 719 | 2876 | 5, 7, 9, 11 |
| 739 | 2956 | 9 |

**18 pairs of 96 — 19%, a factor of 5.3.** *"Necessary is not sufficient"* fired exactly as the brief's
rule 5 warned. **One small discrepancy: I get 7 orders, the run reports 8 of 13.** Worth one line to
settle; mine or theirs.

**And the region was entered, not merely admissible.** FINDINGs 62–69 cover it; `Cooperative-AI-Defense/hadamard/findings/settled_*_b*.txt` holds
**17 odd-*b* pairs and 135 configurations — 104 EMPTY_SCOUT, 19 EMPTY, 8 EMPTY_UNSETTLED, 4 NOSOL** —
even-*b* files were 73% of that sweep, and **a grep of the 33 `Cooperative-AI-Defense/hadamard/findings/open_*_b*.out` files found no solution.**

**The cost case was withdrawn by its own author.** FINDING 62 gave open-order *b* ≥ 3 walls; **FINDING 63
withdrew them**, concluding *b* > 1 lowers the wall *"by roughly 1 to 2.3 decimal orders, not by 3 to 8."*
The only corrected *b* ≥ 3 row is at a **solved** order (*v* = 347, *b* = 3, *K* = 35, log*E* = +3.3,
wall 11.4) and that is not even the *b* Alpöge used there (*b* = 5). A *v* = 523, *b* = 3 row exists in
`Cooperative-AI-Defense/hadamard/findings/tvopen.out` with log*E* = −3.7 — **fewer than one expected solution** — but it is the withdrawn version.

**So option 3 dies on evidence, at the strongest grade this board has produced: the region was entered
and returned nothing, and its optimistic cost figures were retracted by the programme itself.**

## 3. The instrument finding, and it is a new variant of D51

Clause (c)'s second conjunct asked whether `FINDING_155`'s ranking was scoped to a single *b*. **It was —
the title is "the open b=0 orders" and every row is *b* = 0. It did not rank across *b*.** By the brief's
own logic that made the region unswept.

**It was not.** F62–F69 screened it with entirely different instruments. So:

> **An "unswept" claim scoped to one instrument is worthless when the programme has others.**

That is **D51's shape one level out.** D51: S4 counts *moves*, so it cannot see an *attempt*. Here: I
asked whether the *ranking* covered *b* ≥ 3, when the question was whether *anything* had. Registered as
**D57**.

## 4. Two errors of mine, one of them in the brief's design

**The live target is *b* = 0, not *b* = 1.** FINDING 155's row is a *b* = 0 row; FINDING 134 §3 gives
*r* = (*v*−1)/*d* + 1 **at *b* = 0** with the Σ*a*² = 4*v* law holding there, and admissibility is
*"b = 0 or b odd"*. So the relation §3 of the brief called "*b* = 1-fitted" was fitted at ***b* = 0***.

**Consequence, and I overstated my evidence:** (*b*+1) | (*v*+1) at *b* = 0 reads 1 | 524, **trivially
true and carrying no information.** So the condition is confirmed on **three** non-trivial pairs —
(347,5), (359,7), (479,3) — **not four.** The claim survives; the count of evidence for it does not. I
asserted "four for four" and it was three for three plus a vacuous case I had mislabelled.

**And the brief cited paths that cannot resolve for its reader.** The run reports `../PLAN_2092.md`,
`PRECHECK_E.md` and `derive.py` as unresolvable — **of course they are: they are in Claim-2, and the run
was in Cooperative-AI-Defense.** `board-finder/tools/check_paths.py` validated them against *my* tree,
which is exactly the wrong tree for a brief shipped elsewhere. **D52's disease in a new form**, and the
tool that exists to catch it cannot: it checks resolvability in the author's repository when what matters
is the reader's. Added to **D57**.

## 5. Also established

* **The thirteen are the open thirteen**, from **Cati & Pasechnik Table 4**, and the *v* values match my
  table exactly. **`E: VOID` does not apply.** The run did not open FINDING_05, so equating the two lists
  is still an inference.
* **"126+" has no provenance.** The file names no command and a grep for "126" in the scripts and outputs
  found no source. **Typed, not computed** — or computed somewhere unrecorded.
* **`Cooperative-AI-Defense/hadamard/findings/OPEN_ORDERS.md` is stale on 669 and 721.** It says they were *"never screened"*; FINDING 72 settles
  both at *b* = 0 and *b* = 1, and `Cooperative-AI-Defense/hadamard/findings/settled_669_b4.txt` and `Cooperative-AI-Defense/hadamard/findings/open_721_b37.out` exist. **That sentence is
  what `../../fallbacks/QUEUE_V3.md` option 3 was built on.**
* **160 FINDING files**, numbered 1–163 with 81–83 missing; highest is 163, the same as `../PLAN_2092.md`
  saw. So nothing has been added since — the currency worry was unfounded.

## 6. P-38 scored

**CORRECT on the threshold: the bar FAILED.** But the record should show how the clause-level commentary
went, because it is a calibration datum and it is unflattering:

| revision | expected failure clause | outcome |
|---|---|---|
| v1 | (a) or (b), "bookkeeping" | wrong |
| v2 | **(c)** | **right** |
| v3 | (b) | wrong — (b) passed cleanly |

**One of three.** The threshold prediction held across every revision; the clause prediction was near
chance. Worth remembering the next time I attach confident commentary to a registered threshold.
