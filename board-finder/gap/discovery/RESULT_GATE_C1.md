# Gate C-1 — FAIL, and the two papers are worth more than the verdict

Both papers named in C-1's bar were supplied as transcripts by the operator: **arXiv:2606.10402v2**
(EinsteinArena, Bianchi–Kwon–Pappu–Zou, 26 Aug 2026) and **arXiv:2609.35051v1** (Qiushi Engine, Yang
et al., 28 Sep 2026). Tier **SECONDARY-RELAYED**: read from transcripts, not from the PDFs; this
container's egress proxy blocks arxiv.org.

## 1. The verdict

**C-1: FAIL.** The bar, verbatim from `../RESULT_DISCOVERY.md` §2:

> Read Cohn's table (dated ≥ June 2026) and the method sections of arXiv:2606.10402 (EinsteinArena)
> and arXiv:2609.35051. **PASS iff 1154 still stands at primary tier AND at least one of those
> systems reports having attempted dimension 13.** An unattempted cell is only unvisited, and the
> next run of theirs will visit it. FAIL otherwise.

| conjunct | outcome |
|---|---|
| 1154 still stands at primary tier | **satisfied** — Cohn's table, credited to Zinoviev–Ericson 1999 (`TABLE_KISSING.md`) |
| at least one of those systems attempted *d* = 13 | **not satisfied** |

* **EinsteinArena.** Table 1 lists every problem active on the platform as of May 2026 — fifteen of
  them, curated from AlphaEvolve. The kissing-number entry is **dimension 11 only**. No *d* = 13, no
  *d* = 14, and no other kissing dimension anywhere in the paper.
* **Qiushi Engine.** Nineteen new lower bounds, at **25, 27, 32–39, 43, 45, 49–55**. Neither 13 nor
  14 appears.

So the bar fires as written: **FAIL.**

## 2. The bar's own reasoning is mechanically vindicated, and it cuts harder than the bar said

The bar's justification was *"an unattempted cell is only unvisited, and the next run of theirs will
visit it."* Both papers are direct evidence of that mechanism running at scale:

* Qiushi produced **nineteen dimensions in one paper**, including the contiguous blocks 32–39 and
  49–55, each with machine-checkable finite certificates, exact integer/rational arithmetic and
  192-bit interval arithmetic where needed.
* EinsteinArena launched **19 March 2026** and its Table 1 reports **11 new state-of-the-art results**
  by May — two months from a standing start, across a curated board of record problems.

**The record-problem niche is being swept at industrial rate.** That is the crowding gate's whole
subject and it is now measured rather than asserted.

## 3. The reading the bar cannot see, and it argues the other way

**Every one of these systems' dimension ranges tracks where exploitable algebraic structure lives,
not where the problem is open.** From Qiushi's own method inventory: Leech-shell liftings, Golay
codes, constant-weight codes, √3·E₈ embeddings, the P48p/P48n line classes, spherical-design moment
identities, a ternary quadratic-residue neighbour. Those objects exist at 24 and 32–48. Hence 25–55.
PackingStar, Kallal–Kan–Wang and Takhanov–Yun all sit in **25–31** for the same reason. And *d* = 11
is worked only because AlphaEvolve seeded it and EinsteinArena inherited AlphaEvolve's problem list.

**Dimensions 13 and 14 have no Leech, E₈ or Golay structure to lift from.** That is plausibly *why*
Zinoviev–Ericson's 1999 code concatenation still stands after 27 years, and why de Laat–Leijenhorst's
2024 semidefinite programming works the *upper* bound there instead.

So "unattempted" admits two readings — **not yet visited**, and **outside the reach of the method
class doing the visiting** — and the bar collapsed them into one. The evidence distinguishes them and
points at the second. **I am not reversing the verdict on that**: the bar named its test before
anyone looked, and `D44` was closed as *recorded, not fixed* precisely so that a losing candidate
cannot be rescued by a criterion invented afterwards. Recorded as the finding.

## 4. Scope finding: the bar named two papers and the deciding evidence may sit in a third

`../RESULT_DISCOVERY.md` §2 records, at RECALL tier, that **PackingStar's best at *d* = 13 was a
rational 1146**. If that holds, then a system *did* attempt dimension 13 and fell short of 1154 —
which is exactly the PASS evidence the bar was asking for, from a system the bar did not name.
Qiushi cites PackingStar as reporting constructions across 25–31, which is in tension with the 1146
claim and does not settle it either way.

**Recorded, not used.** A bar that names its sources is not widened after the outcome is known. But
this is the second time in two gates that the bar's scope, rather than its threshold, decided the
result.

## 5. Two corroborations and one claim that stays uncorroborated

**The Ganzhinov dating, confirmed by a primary source's own footnote.** EinsteinArena's Figure 2
caption: *"Note that canonical citation for Ganzhinov's result is [6], even if the result first
appeared in the 2022 preprint"* — [6] being *Linear Algebra Appl.* **722** (2025), 12–37. That is the
exact ambiguity `TABLE_KISSING.md` handled by giving both datings rather than picking one, and C-2's
headroom failure holds on either.

**The *d* = 11 history, complete.** EinsteinArena's Figure 2: 440 (1964 lattice era) → **582 Best,
1980** → 592 Ganzhinov → 593 AlphaEvolve → **604 EinsteinArena**, with a *"~42-year plateau at 582"*.
A 27-year freeze at *d* = 13 is the same shape as the plateau that broke at *d* = 11 the moment a
capable searcher was pointed at it. That is an argument against C-1, not for it.

**The *d* = 12 claim is still RECALL.** `../RESULT_DISCOVERY.md` §2 says AI moved dimensions 11 and
12, citing *"a numerical 841 (June 2026) with an unknown method"*. EinsteinArena gives the full
*d* = 11 history and never mentions *d* = 12; Qiushi never mentions it. **Two primary sources that
would plausibly have mentioned it do not.** Not refuted — neither paper is about *d* = 12 — but it
has now survived two chances at corroboration and got none.

## 6. The transferable finding: EinsteinArena's Table 1 is the crowding instrument this board lacked

`../RESULT_DISCOVERY.md` §2's honest reading was that *"crowding is the operative gate"* and that the
per-record crowding screen was scoped too narrowly. **Table 1 is a maintained public list of record
problems that AI agents are actively working, with prior-best and current-best columns.** That is
exactly the missing instrument, and it is free.

Screened against the 22 `II` records from `../RESULT_ARM1_II.md`, on distinctive object tokens, with
every collision adjudicated (the `../epoch_gate.py` discipline):

| II record | collides with | adjudication |
|---|---|---|
| **368 Thomson problem** | Thomson problem, *n* = 282 | **GENUINE.** Same object. On the active board with AlphaEvolve's 37147.29442 as prior best and no platform improvement yet. **Crowded — strike it.** |
| 428 site-percolation threshold, square lattice | circles packing in a square, *n* = 26 | **SPURIOUS.** Collides on the word "square" only. A lattice percolation threshold and a circle-packing density are different objects. |

**1 genuine collision of 22.** That number is the first positive signal arm 1 has produced: the `II`
list is mostly *not* on the board these systems are sweeping. The `II` records that survive are the
ones whose tracked quantity is not a geometric packing or extremal-configuration record — which is
the same axis Table 1 is organised on.

**Also on Table 1 and worth noting for the pool rather than the corpus:** difference bases, Tammes,
Heilbronn, flat polynomials, and three autocorrelation inequalities. `../../fallbacks/QUEUE_V3.md`'s
pool ideas in the design-theory seam are not on it, which is a point in that seam's favour.

## 7. Three bars, three times the omission decided it

| candidate | bar tested | what actually decided it | in the bar? |
|---|---|---|---|
| C-3 caps | crowding | the deliverable table does not exist | no |
| C-2 τ₁₄ | crowding | the record moved in 2025, failing the queue's own ten-year rule | no |
| **C-1 τ₁₃** | crowding | attempted-versus-reachable, and the bar's own two-paper scope | **no** |

All three bars were written in one run, all three tested crowding, and in all three the crowding test
was not what mattered. Registered as **D47**.
