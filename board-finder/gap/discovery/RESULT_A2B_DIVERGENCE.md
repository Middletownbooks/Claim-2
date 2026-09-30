# Arm 2b — P-35 fires, the signal does not generate, and the run corrects three of this project's own numbers

Run by a Sonnet 5.5 chat instance against `prompts/s55/A_DIVERGENCE.md`. 22 of 25 calls used, 11 of
12 entries written, stopped under both caps. Four calls failed: three arXiv fetch rate limits on
2609.35051, and one refused URL — **the bare `github.com/…` string from my brief, which the fetch
tool rejected until a search had surfaced it.** Every ratio was recomputed by the run locally, and
re-derived again here.

## 1. P-35 is CORRECT on the letter, and the letter is the problem

> **P-35:** the directed search finds ≥ 1 §3.2 divergence meeting the registered definition.
> **0 → §3.2 does not generate.**

**4 COUNT blocks, 3 independent observations. P-35 passes.** And the run's own next sentence is worth
more than the pass:

> *"The four COUNT blocks meet the registered definition literally. None of them has two independent
> groups with contemporaneous methods and a ≥2 reach ratio."*

| entry | object | ratio | why it counts, and why it is worthless to us |
|---|---|---:|---|
| 1 | complex Golay pairs, length | **2.154** | Fiedler 2013 (28) against Holzmann–Kharaghani **1994** (13). **19 years apart, with Craigen–Holzmann–Kharaghani 2002 (19) sitting between them.** Against the nearest predecessor it is 28/19 = **1.474**, below the bar. Run's verdict on the gap: *"No gap now."* |
| 3, 4 | SIC fiducials, dimension | **17.89** | Stark units (5,779) against Fibonacci–Lucas 2017 (323). Closest to a real method-class gap, 2017–2021. One source, one phenomenon — the run counts them as one observation. |
| 5 | Barker sequences, length | **2000** | Borwein–Mossinghoff 2013 against Mossinghoff **2009** — **same author, same method family, four years apart.** The gap is closed by the later paper itself. |

**The registered definition has no time window and no independence requirement.** So it admits *the
field's own progress over time* — a sequence in which the lagging method is superseded and nobody is
behind. That is the opposite of what a divergence is for. The model case, Hadamard 2092, is **two
parties at the same time**, one holding an idea the other lacks: Alpöge's implied exponent ≈0.25
against this project's measured 0.503.

Read the `STILL OPEN?` column across the entries: **"No gap now"**, **"Closed"**, **"The gap is closed
by A itself"**. Only the SIC pair is live, and that is this project's own retired U16.

**So: the prediction fires and the instrument does not deliver.** §3.2 generates *temporal* reach
ratios in abundance and did not produce one contemporaneous capability gap in 22 calls. That is a
sharper negative than P-35's zero-branch would have been, because it says *why*. Registered as
**D48**; the definition is **not** redrawn after the fact.

## 2. The correction that matters most: 5,799 was never right, and our own check caught it and dismissed it

**The exact-SIC ceiling is d = 5,779, not 5,799.** The run read Grassl's 2021 slides and verified
locally that **5,779 = 76² + 3**, while 5,799 − 3 = 5,796 is not a square. Re-derived here:

```
5779 - 3 = 5776 = 76^2      perfect square   ✓
5799 - 3 = 5796             isqrt = 76, 76^2 = 5776 ≠ 5796   ✗
140^2 + 3 = 19603     199^2 + 3 = 39604     22^2 + 3 = 487
```

**The digit came from the relayed response**, `../../playability/sources/GATE_SIC_RESPONSE_RAW.md`
("up to a maximum of 5799"), so it was not introduced here. **What was introduced here is worse.**
`../../playability/GATE_RESULT_SIC.md` §2 exists to check the quoted dimensions against the n²+3
form. Three of four fit. The fourth did not, and the gate wrote:

> *"5799 − 3 = 5796 is **not** a square → the exact ceiling comes from a different family, consistent
> with the report's account."*

**The check fired and the interpretation invented a family to absorb it.** One digit's difference from
a perfect-square fit, in a document whose whole subject was the n²+3 family, was read as evidence of
a *second* family rather than as a typo. It then propagated into nine documents, including **lesson 24
in the ledger** — this project's most-cited lesson — and into all five of the briefs I wrote last
night.

That is a new failure mode and it is not "an unsourced number". It is **an anomaly detected by a
working check and then explained away**, which is the one thing a check cannot protect against.
Registered as **D49**.

## 3. Lesson 24's phenomenon is right and its attribution is wrong

Lesson 24 says a *breadth pass* reported *"reaching d = 19,603"* where a *dedicated gate* had
established the ceiling. The run corrects the framing:

> *"19,603 is more than a breadth-pass number. It is the headline of the refereed JMP 2022 abstract:
> SICs shown to exist in 13 prime dimensions of the form n²+3, the highest being p = 19,603."*

It depends on conjectural Stark units, and the slides show its numerical check at **1,000 digits**; a
2025 refereed follow-up reaches d = **39,604**, checked at **100 digits**; the 5,779 row is checked
at **2,000 digits**.

**So there are not two senses here, there are at least three** — an exact expression conditional on
conjectural units, a numerical verification to a stated precision, and contiguous versus sparse
coverage — and the "ceiling" depends on which you pick. The breadth pass relayed the refereed headline
**correctly**. The gate's "the exact ceiling is 5,799" was itself a choice among senses presented as
a fact.

Lesson 24's rule — *a breadth cell is triage-grade and may not be gated on* — survives intact and is
if anything better supported. Its story about who erred does not. Corrected in the ledger in place.

## 4. My brief's own worked example was not a divergence

Brief A gave, as the model of the right shape: *"method A enumerated all Costas arrays up to n = 29;
method B, published earlier, reached n = 14 — ratio 29/14 ≈ 2.07."*

**The run found no source for a 14.** The 2011 review it read says the 1988 count was fitted to known
C(n) for n ≤ **17**, which gives 29/17 = **1.706** — below the threshold the example was illustrating.
**The example I used to define "counts" does not count.** Marked wrong in the brief rather than
replaced, and the run's own entry 1 substituted as the worked example, with its time-window flaw
stated.

## 5. Operational findings for the remaining briefs — B1, B2 and C are being patched

* **The fetch tool only opens a URL a search has already surfaced.** The bare `github.com/…` string in
  brief A was refused until searched for. B1, B2 and C all hand over bare URLs — **La Jolla, Brouwer,
  the Handbook successors** — and will lose calls the same way. Patched to say: search for the host
  first, then fetch from the result.
* **arXiv is rate-limited, not blocked, and asymmetrically.** It opened 1907.04987, 1102.5727 and
  1306.0045 and refused 2609.35051 three times. Recent IDs appear to be the problem. Where a brief
  points at a recent paper, **paste the passage instead of the pointer** — I had the Qiushi §1.3 text
  in hand from the operator transcript and pointed at it rather than quoting it, which cost the run
  three calls for nothing.
* **A live artifact changed under the run mid-session.** Qiushi's README had 10 dimensions and a d=32
  baseline of 346,432 (+1,152) in the search snapshot, then 19 dimensions and 346,944 (+640) when
  fetched — **the claimed d=32 increase shrank 44.4%.** The run verified the new baseline locally:
  2¹⁷ + 128·1671 + 2·32·31 = 346,944, re-derived here. **A record claim that moves while you read it
  cannot be gated on at any tier.**

## 6. Two source-level contradictions worth carrying into B1

* **Williamson, two papers by the same authors disagree.** The AAAI 2018 paper says no even-order
  enumeration existed before it; the 2019 survey cites Kotsireas–Koukouvinos 2006 reaching order 18.
  B1 asks about Williamson — this is the first thing it should resolve.
* **Costas is live at 29** and a Feb 2026 paper still says so. An Aug 2026 preprint gives an exhaustive
  census of *main-diagonal symmetric* Costas arrays for orders 37–42 — a **subclass**, so it fails the
  same-object test at 42/29 = 1.448. B2 should expect that distinction to matter.

## 7. What the run did that neither cap nor brief asked for

It recomputed every ratio locally before reporting, labelled that `PRIMARY-VERIFIED-LOCALLY`, and
stated that the computation was not a search call. It reported four failed calls with their causes. It
distinguished *"I found no source for a 14"* from *"there is no 14."* And it refused entry 11 — the
Qiushi kissing bounds — at the boundary, on the correct ground that the improvements are **a count of
objects, not a reach**, which is one of the three refusals the brief carried forward.

**P-31 A-1 gets a second favourable data point.** No verdict was issued on a cell the run could not
evaluate, and the cells it could not reach are named.
