# Brief F — all three bars FAIL, and the operator's two notes outrank the run

Run 30 Sep 2026 by a Sonnet 5.5 chat instance. **14 of 22 calls, stopped on neither limit**, with 8
unspent because all three bars were decidable — **and it reported that oversized returns had made context
the nearer constraint**, which is D55's datum arriving cleanly for the second time.

**`B-1: FAIL` (ESTABLISHED) · `B-2: FAIL` (UNEARNED) · `C-1: FAIL` (ESTABLISHED)**

## 1. The two things the operator said, and they matter more than the verdicts

**(i) An Opus 5.5 instance already worked 239 extensively — and found an error in Ochem–Zelinsky's
Algorithm 1 program in their most recent paper, accepted by Ochem by email.** It judges further progress
unlikely.

**That is the most concrete external result this programme has produced, and it is not in the ledger.**
41 predictions and 57 debts record what the *screen* did, and an accepted correction to a published
paper's program appears nowhere. Registered as **D58**, because the asymmetry is the finding: the
bookkeeping is exhaustive about the screen's failures and silent about the programme's one success,
since the screen is what got instrumented. **It also reframes the 0-of-7 tally — that number measures
the screen, and the thing that worked was not the screen.**

**(ii) arXiv:2512.24061 had already been checked by an LLM and ruled out.** So C-1 was effectively
answered too.

**So brief F was substantially redundant, and the reason is a new form of D56.** I *did* grep the local
tree before writing — that was D56's registered fix, applied for the first time — and the tree was
silent, because **both prior efforts happened in other instances and left no trace in this repository.**
Grepping the tree is necessary and not sufficient: **the fix has to include asking the operator what has
already been tried.** Recorded against D56.

**What brief F was not redundant about**, and this is the honest ledger of what the 14 calls bought: the
10²²⁰⁰ update, the Figure 2 cost table, the structural kill in §3, and the certificate-versus-verdict
correction in §4. Four items, none of which were on file here.

## 2. B-1 — FAIL-ESTABLISHED, and my figure was eleven years stale

**Ochem's own OPN page** (`SECONDARY-RELAYED`, opened) says 10¹⁵⁰⁰ is what the 2012 paper proves and the
computation **has since been pushed to 10²²⁰⁰**, with **Ω(*N*) ≥ 115** against the published 101, plus a
separate unpublished *m* > 10¹⁰⁰⁰. Composite-factor lists run to 10²³⁰⁰, dated **Feb 2025**, with a
roadblock list for the 10²²⁰⁰ target. `ANNOUNCED`, no date on the claim, and the only proof tree linked is
for 10⁵⁴⁰.

**My brief's 10²⁰⁰⁰ is a 2014 slide figure** (Ochem–Rao, Montpellier, 2 July 2014, opened) — real, and
superseded by the authors' own page. A 2012 seminar deck gives 10¹⁶⁰⁰ (`SEARCH-SUMMARY`). **So the gap
between the published record and the private one is ~700 orders of magnitude, not ~500.**

**No refereed bound beyond 10¹⁵⁰⁰ exists**, which is consistent with "unmoved in publication for 14
years" and does **not** make 10¹⁵⁰⁰ the frontier. That is exactly what B-1 was written to catch.

## 3. B-2 — FAIL-UNEARNED, and the grading is right

The only measured figure is **Figure 2** of the author-hosted preprint (opened):

| theorem | branchings | of which roadblock | time |
|---|---|---|---|
| 1 — *N* > 10¹⁵⁰⁰ | 22,514,255 | 10,406,935 | **≈12 h** |
| 2 — Ω ≥ 101 | 447,019,005 | 444,022 | ≈93 h |
| 3 — component > 10⁶² | 6,574,758 | 0 | ≈30 min |

on an **AMD Phenom II X4 945**, with thread count and core-hours unstated. Re-checked here: **105.5 h
documented in total against a 10-container-hour bar, 10.6×; Theorem 1 alone is 1.2× over** on 2008-era
hardware. The run flagged a parse ambiguity in Theorem 2's row (`447 019 005 444 022`) — the right
instinct.

**And the paper explicitly excludes the factoring**, which was volunteer-distributed across the Mersenne
forum, yoyo@home and RSALS and **never aggregated anywhere**. The known-factor database alone is 2.5 GB.

**So the dominant cost is unreported and the margin is not computable.** `FAIL-UNEARNED`, not
`FAIL-ESTABLISHED` — the bar fails for want of evidence, not on a measured margin. **The run declined to
register a middle band and said so.** That is the distinction D54 exists for, working as designed on its
second outing.

## 4. C-1 — FAIL-ESTABLISHED, and the structural kill makes the bar nearly beside the point

**arXiv:2512.24061 is real and says what the brief claimed.** Submitted 30 Dec 2025; arXiv lists the
author as *Bogdan Dumitru*, the byline reads *Dumitru Bogdan*, University of Bucharest. **My P-39 side
bet — better than even odds it would not check out — is WRONG.**

**But the relayed description overstated one word.** *"UNSAT certificates"* means solver **UNSAT
verdicts**: no DRAT/LRAT proof, no independent checking, and the linked repository holds only a README
and a CNF generator — **no logs, proofs or coverage records.** `Certificate` versus `verdict` is rule 2's
numerical-versus-exact distinction in a new costume, and it was in the chain that reached me.

**The paper names no unswept subfamily and no sweep cost.** Table 1 is titled *"Selected"*; the *w*
sub-cubing is explicitly not a balanced or exhaustive split; future work is two encoding refinements and
one anchoring refinement. Derived counts, reproduced here exactly: **13 rows, 9 distinct layer templates,
only 3 with H = 33**, rows summing to **7.01 × 10⁶ s ≈ 81 days single-thread**, and **10,121 compositions
of 33 into parts 3–6** as a scale indicator. Within 5⁶ the reported times span **912×**, and one
*w*-restricted sub-cube ran **8.8× longer than the unrestricted baseline** — the heavy tail, in the
paper's own numbers.

**And the finding that outranks the bar** (rule 5, strength):

> **No subfamily's closure could move the ES(7) bound on its own.** The lower bound is already 33. Only
> UNSAT over **all** 33-point sets moves the upper bound, and a partial UNSAT changes nothing.

**C-1 asked whether a subfamily was unswept when no subfamily closure could have mattered.** Same shape
as brief E: the bar tested something adjacent and the decisive fact came from the strength rule. The best
explicit upper bounds are **113** (Mojarrad–Vlachos) and **127** (Tóth–Valtr); the run **correctly
declined** to treat 92 (Norin–Yuditsky) as proved, since it is a formula with an o(1) term evaluated at
*n* = 7.

**Separate finding, as the brief asked (D57).** No evidence of a subsequent sweep, and the run says
plainly that is not the same as showing none exists. Koshelev–Koshka (arXiv:2604.20120, April 2026,
opened) tabulates ES(7) = 33 as conjectural with no Bogdan reference. Baek (SoCG 2025 / JCTA 2026) proves
the conjecture for *decomposable sets* — a structural subfamily unrelated to layer templates. Not
searched: Bogdan's citation graph, SAT-competition archives, erdosproblems.com, MathOverflow.

## 5. Corrections to the brief

1. **10²⁰⁰⁰ → 10²²⁰⁰**, and Ω ≥ 115 unpublished.
2. **Suk's bound is superseded** by 2^(*n*+O(√(*n* log *n*))) — Holmsen–Mojarrad–Pach–Tardos, 2020. My
   brief cited Suk 2017 as current. Venue disputed between sources (JEMS vs JCTA), unresolved.
3. **"UNSAT certificates" → UNSAT verdicts** (§4).
4. Author name order differs between the arXiv listing and the byline.
5. **Both code blocks passed and could not be broken** beyond noting the general-position assumption the
   brief states. The 25,052 general-position 5-subsets reproduce with 0 failures; Bogdan's variable and
   clause counts reproduce exactly, and **9,493,440 = 40 × C(33,5)** — re-verified here.

## 6. P-39 scored

**Threshold CORRECT: all three FAIL. Grades 3 of 3** — B-1 ESTABLISHED ✓, B-2 UNEARNED ✓, C-1
ESTABLISHED ✓. **Side bet WRONG:** the paper is real and says what was claimed.

**Against P-38's 1-of-3 on clauses, that is a usable distinction rather than luck.** P-38's guesses were
about *which* clause would fail — a question about evidence I did not have. P-39's grades were predicted
from **structural features of the sources**: a 2012 paper will not document compute in container-hours, so
B-2 fails for want of evidence; a specific numeric report is findable, so B-1 fails on positive evidence.
**Structural predictions held; guesses about which clause did not.** Worth carrying: predict the *kind* of
failure, not the location.
