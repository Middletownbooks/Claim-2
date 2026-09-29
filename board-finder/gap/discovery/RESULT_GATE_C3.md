# Gate C-3 — FAIL, and the gate found two things the bar did not ask about

Run by a Sonnet 5.5 instance outside any repository, web search plus code execution, against
`prompts/GATE_C3_CAPS.md`. Bar quoted from `../RESULT_DISCOVERY.md` §2. Response relayed; this
session verified nothing in it — the two pages that would settle the §3 finding are blocked by this
container's egress proxy (`yvesedel.de`, `arxiv.org`, `math.tugraz.at`, `mathi.uni-heidelberg.de` all
refused).

## 1. The verdict

**C-3: FAIL**, on the bar as written, on positive evidence rather than absence.

> **FAIL if any AI search system published after 2023 (AlphaEvolve, X-evolve, others) reports
> attempting AG(8,3) caps directly.**

Three post-2023 systems report direct *n* = 8 runs:

| system | id | evidence given | reached |
|---|---|---|---|
| **X-evolve** | 2508.07932 | Table 2 has an *n* = 8 column; §3.1 "Largest cap sets" reports 3 of 5 runs reaching 512; Table 5 is an *n* = 8 ablation; Table D1 gives *n* = 8 settings; Programs 4–6 build 512-caps | 512, matched |
| Ellenberg et al. | 2503.11061 | Table 1: 8 runs × 7 LLMs at *n* = 8, best 448; Table 4: 349 and 370 at 10⁸ tokens | below 512 |
| QUBE | 2412.20694 | finds a cap 16 larger than its own FunSearch reproduction at *n* = 8 | below 512 |

**The prompt's §3 escape hatch does not apply.** It hedged that X-evolve had moved the *capacity*
(C ≥ 2.2203 via a partial admissible set) rather than the finite cell, and that the two are different
objects. The distinction is real and the hedge was wrong on the facts: **X-evolve worked both.**

Two rows were returned as **"cannot adjudicate"** rather than guessed — AlphaEvolve (2506.13131: the
results notebook lists only *improved* problems and its README says matched-only ones were omitted,
so its silence is uninformative) and the OpenEvolve/ShinkaEvolve/CodeEvolve/EFT family. That is the
required behaviour and it is the reason this verdict is worth something.

## 2. The local verification worked, and it is the one PRIMARY cell here

The snippet in `prompts/GATE_C3_CAPS.md` §5 was run as prescribed: positive control 0 lines, negative
test 1 line, then the real object. The run cloned `google-deepmind/funsearch`, took
`cap_set/n8_size512.txt`, and reports **512 distinct 8-tuples over {0,1,2} with 0 violating lines**.

It went further than asked, and correctly: it cross-checked by enumerating **all C(512,3) =
22,238,720 triples** for *x* + *y* + *z* ≡ 0 (mod 3) — also 0 — against the pair trick's C(512,2) =
130,816 lookups, and it negative-tested *the real set* by adding a completing point, finding 19
deduplicated lines all passing through the added point, as they must.

**Both counts were derived rather than typed, and the deduplication the snippet was corrected for
mattered**: 19 lines, not 57 hits. That correction was made because the snippet's own negative test
caught the 3× overcount before it shipped.

This establishes the file is a 512-cap. It does **not** establish the file is FunSearch's output —
provenance is the repo README, relayed — and the run says so.

## 3. The finding the bar did not ask for: the deliverable table may not exist

`../RESULT_DISCOVERY.md` §2 gives C-3's Δ as *"Edel's cap tables, n = 8"* with the deliverable
sentence *"A cap of size 513 in AG(8,3)."* The run reports, having fetched the page:

* it was **last changed 28 April 2010**, so it cannot have been updated for FunSearch;
* its table is **m₂(*k*,*q*) for *projective* caps**, and row 8, *q* = 3 is **541** — a cap in
  PG(8,3), a different object;
* its affine section gives only C₄(3) = 20, C₅(3) = 45 and an upper bound C₆(3) ≤ 114. **There is no
  affine *n* = 8 row at all.**

**Tier: SECONDARY-RELAYED and not confirmable from here.** I tried both the Heidelberg and
`yvesedel.de` addresses and this container's egress proxy refused both. It needs one fetch from a
machine that can reach the page.

If it holds, **C-3's Δ fails independently of the crowding bar** — there is no table row to move —
and worse, a reader taking "row 8" at face value would aim at **541**, a projective figure, and be
building the wrong object.

## 4. A live, unresolved flag that would invalidate the premise, not just the candidate

Searching around the verdict, one summariser returned *"for dimension 8 in AG(*n*,3), the lower bound
on maximal cap cardinality is **532** … a doubling construction"*, alongside the claim that a 541-cap
in PG(8,3) "would correspond to affine caps as well".

**If an affine lower bound of 532 at *n* = 8 stands, then 512 was never the frontier**, and C-3 was
built on a stale figure — the same numerical-versus-exact failure this board keeps meeting.

**It is not established, and I am explicitly not promoting it.** Provenance: a search summariser, not
a source anyone read. Against it: the obvious candidate paper, Elsholtz–Lipnik *"Exponentially Larger
Affine and Projective Caps"* (2211.09772, Mathematika 2023), applies to primes **p ≡ 5 (mod 6) with
p ≤ 41** and so **not to p = 3** — its worked example is p = 23, improving Bose's (8.0875…)ⁿ and
Edel's (8.0901…)ⁿ to (9 − o(1))ⁿ. So the likeliest source of a 532 is *not* that paper, which makes
the number less credible, not more. The gate run itself found 512 stated as current in a Feb 2026
source.

**Promoting search, named before anyone looks:** read the affine table in arXiv:2310.03382 *"Maximal
line-free sets in 𝔽ₚⁿ"* (2023, rev. May 2024) and the bounds table in the TU Delft cap-set thesis,
and settle whether any affine AG(8,3) lower bound above 512 is in print. One fetch each, from a
machine with egress.

## 5. Corrections to my own prompt, marked and not rewritten

* **§4 mis-scoped X-evolve.** I wrote that on the available description it "moved the capacity, not
  the AG(8,3) cell". It did both, and that is what decided the gate. The instruction to *check*
  rather than assume is what saved it, but the hedge itself was wrong.
* **§4 mis-characterised arXiv:2609.19799.** I called it "a critical evaluation paper … papers of
  this kind enumerate which benchmark instances these systems actually run". It is a three-strategy,
  five-task study (OpenEvolve, EvoX, AdaEvolve on PRISM, Cloudcast, transaction scheduling, circle
  packing, Heilbronn) with no cap sets, so it cannot settle coverage for other systems. **I inferred
  the paper's content from its title**, which is the failure the tiering rules exist to prevent, and
  I did it in a prompt whose whole subject was that failure.
* **One small correction to the discovery run, relayed:** AlphaEvolve's kissing-number move is
  dimension **11** (592 → 593) and the table in 2511.02864 stops at *n* = 11. `../RESULT_DISCOVERY.md`
  §2's C-1 entry says AI systems "moved dimensions 11 and 12"; the 12 is not corroborated here and
  d13/d14 remain untouched by that table. C-1's bar requires evidence a system *attempted* d13, and
  this run gives none either way.

## 6. Incidental, recorded because it is cheap to lose

The run found a digit slip in X-evolve: the partial admissible set A(27,19) is given as **1,270,863**
in §3.1 and Program 3 and as **1,270,683** in §6. It does not affect the bar. Also flagged and
unverified: Hametner–Tyrrell (2606.12194) reportedly shows product constructions are provably
suboptimal for a class including cap sets, credited with a post-X-evolve capacity improvement; no
*n* = 8 claim seen.

## 7. What this run says about P-31

**One favourable data point for A-1, which is not yet settled.** A-1 claims gate execution moves to
the cheaper tier without loss; its threshold is a single verdict issued on a bar the run could not
evaluate. This run issued FAIL on positive evidence, read four sources in full, and returned
"cannot adjudicate" on the two rows it could not settle rather than filling them. **It also did
something A-1 does not predict and is worth more than the verdict**: it corrected two errors in the
bar-writer's own prompt and produced a finding (§3) about a field no bar asked about.

A-2 is untouched: the candidate did not enter or leave the queue without a bar.
