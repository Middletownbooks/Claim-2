# Gate C-3 — caps in AG(8,3). One verdict, one bar.

**For a Sonnet 5.5 instance with web search and code execution, outside any repository.** You have
no filesystem and no git. Everything you need is below; your output is a document you return in the
reply.

You are evaluating **one registered bar** on one candidate. The bar was written before anyone looked,
by a different instance, and **you may not re-scope it.** If it cannot be evaluated, the answer is
FAIL — not "unscored." These are go/no-go gates and the default is no.

---

## 1. The candidate

**C-3. Caps in AG(8,3): the standing record is a cap of size 512.**

A **cap** in AG(*n*,3) = 𝔽₃ⁿ is a subset containing no three distinct points on a line —
equivalently, no three distinct *x*, *y*, *z* in the set with **x + y + z ≡ 0 (mod 3)**,
coordinatewise. (Equivalently again: no three-term arithmetic progression.) The **cap set problem**
asks for the largest such subset.

What the project holds on this candidate, as recorded when the bar was written:

| field | value |
|---|---|
| record | cap of size **512** in AG(8,3) |
| set by | **FunSearch**, Dec 2023 (Romera-Paredes et al., *Nature*), improving a previous 496 |
| table it would move | **Edel's cap tables**, row *n* = 8 |
| the deliverable sentence | *"A cap of size 513 in AG(8,3)."* |
| gap type as assessed | IDEA (SEARCH-NEW + AI-SEARCH) |
| `bits_search` | **UNDEFINED** — no density estimate exists for this cell |
| `V_arg` class | **CHECK** — the 512-point object was verified by an all-pairs check |

**Everything in that table is RECALL except the local verification, and verifying it is step 1.** If
the record is not 512, or was not set by FunSearch, or Edel's tables say something else, stop and
report that — it is more valuable than the verdict.

Two pieces of context that were part of the assessment and are also recall:

* The upper bound side is **Ellenberg–Gijswijt (2016)**, roughly O(2.756ⁿ) by the polynomial method.
* This is the cell that `QUEUE_V3.md` already called **"the flagship instance … taken"** — FunSearch
  is cited by this project as the existence proof that record problems move under model capability,
  and AG(8,3) is the very instance it moved. C-3 was ranked **weakest of three** candidates for
  exactly this reason.

---

## 2. The bar. Quoted verbatim; this is the whole of your task.

> **FAIL if any AI search system published after 2023 (AlphaEvolve, X-evolve, others) reports
> attempting AG(8,3) caps directly.** X-evolve moved the adjacent capacity record in 2025, so the
> neighbourhood is already worked by the systems this project would be imitating. This is the
> weakest of the three, and it is the flagship instance QUEUE_V3.md already called taken.

Three things follow from the exact wording, and you should hold them precisely:

1. **"published after 2023"** excludes FunSearch itself. FunSearch set the standing record; it cannot
   be the disqualifier, or the bar would be trivially FAIL and meaningless. Apply the bar to systems
   *other than* the one that set 512.
2. **"attempting … directly"** is weaker than succeeding. A system that ran AG(8,3) as a benchmark
   and merely *matched* 512 has attempted it directly. A system that improved some other cap-set
   quantity has not.
3. **"AG(8,3) caps"** is a specific finite object. See §3 — this is where the gate is actually
   decided.

**PASS is the complement:** no such system reports attempting AG(8,3) caps directly.

---

## 3. The discrimination the whole gate turns on

**"Cap set" names at least three different objects in this literature, and a careless read will
conflate them.** Keep them apart:

| object | what it is | is it AG(8,3) caps? |
|---|---|---|
| a **cap in AG(8,3)** | a finite subset of 𝔽₃⁸, currently 512 points | **yes — this is the target** |
| the **cap set capacity / constant** | the asymptotic growth rate, a lower bound on *C* where caps of size ~*Cⁿ* exist | **no** |
| **admissible sets / partial admissible sets** | combinatorial objects used to *construct* asymptotic lower bounds, typically in a different and often much larger dimension | **no** |

FunSearch's own paper did **both** the finite *n* = 8 cell and the admissible-set route, so a system
replicating FunSearch's benchmark suite plausibly did both too — **but you must establish that from
the source, not assume it.** A paper that improves the capacity constant via partial admissible sets
has not, on the bar's wording, attempted AG(8,3) directly. A paper whose results table has a row for
*n* = 8 in 𝔽₃ⁿ has.

This distinction is the same failure mode that has cost this project the most: a breadth pass
reported exact SIC-POVM constructions "reaching d = 19,603" where the exact ceiling was **5,799**,
the higher papers admitting their verification was "mostly partial." Both cells were true at their
own precision; only one was usable. **When a claim's meaning depends on which object is meant, report
both readings rather than picking one.**

---

## 4. Where to look. These entry points are given so your negative evidence has coverage.

Named so you can be held to having looked; not a claim about what is in them.

* **X-evolve — arXiv:2508.07932.** Reported as establishing a tighter asymptotic lower bound on the
  cap set constant (**C ≥ 2.2203**) via a larger **partial admissible set**, and separately a larger
  independent set in the 15-vertex cycle graph (19,946) raising a Shannon-capacity bound. **On that
  description it moved the capacity, not the AG(8,3) cell — check whether its results also include a
  direct *n* = 8 run.**
* **AlphaEvolve — arXiv:2506.13131**, plus the results repository
  `github.com/google-deepmind/alphaevolve_results`, which is reported to contain a notebook of its
  discoveries *and verification code*. AlphaEvolve is reported to have moved matrix-multiplication
  algorithms and **a kissing-number lower bound**. Whether it ran AG(8,3) caps is exactly the open
  question.
* **arXiv:2511.02864**, "Mathematical exploration and discovery at scale" — the large-scale
  AlphaEvolve application paper, covering many problems at once. A results table here is the most
  likely single place to settle the question either way.
* **arXiv:2609.19799**, "Evolution or Illusion? Rethinking Evaluation in LLM Evolutionary Search" — a
  critical evaluation paper. Papers of this kind enumerate which benchmark instances these systems
  actually run, which is precisely what the bar asks about.
* **arXiv:2604.26989**, "Subgroups of Finite Fields As Cap Sets" (2026) — a non-AI cap-set paper;
  check whether it reports the current *n* = 8 state.
* **Edel's cap tables** — the maintained table the deliverable would move. Find it, date it, and
  record what row *n* = 8 says today.

Also worth one query each: any 2024–2026 system in this family (OpenEvolve, ShinkaEvolve, or
whatever now exists) with a published results table, and any successor to FunSearch's own
`cap_set` benchmark.

---

## 5. A verification you can actually do yourself, and it upgrades a tier

FunSearch released code and the constructed sets. **If you can obtain the 512 vectors, verify the cap
property directly** — that is the one cell available to you at `PRIMARY-VERIFIED-LOCALLY` rather than
relayed. Do not check all C(512,3) ≈ 2.2 × 10⁷ triples; use the pair trick, which is ~1.3 × 10⁵
lookups. **This snippet was written, run and negative-tested before being given to you**, including
the positive control and the deliberate break shown at the bottom:

```python
def bad_lines(S):
    """Return the set of collinear triples (as frozensets) inside S, in F_3^n."""
    Sset = set(S)
    lines = set()
    for i, x in enumerate(S):
        for y in S[i+1:]:
            z = tuple((-(a + b)) % 3 for a, b in zip(x, y))   # unique third point of the line
            if z in Sset and z != x and z != y:
                lines.add(frozenset((x, y, z)))               # dedupe: see the note below
    return lines

# POSITIVE CONTROL first — this is a genuine 4-cap in F_3^2, verified by exhaustive search
ctrl = [(0,0), (0,1), (1,0), (1,1)]
assert len(bad_lines(ctrl)) == 0

# NEGATIVE TEST — (0,2) completes the line {(0,0),(0,1),(0,2)}; the check MUST fire
assert len(bad_lines(ctrl + [(0,2)])) == 1

# only now run it on the real object
S = [...]                    # the 512 vectors, each an 8-tuple over {0,1,2}
assert len(set(S)) == 512, len(set(S))
print("violating lines:", len(bad_lines(S)))    # a cap has 0
```

**Deduping is not cosmetic.** Each collinear triple is discovered once from each of its three pairs,
so an undeduped counter reports **exactly 3×** the number of violating lines — confirmed here: the
broken control gives 3 undeduped against 1 real line. Reporting "3 violations" where there is one
line is the kind of wrong number this project's rules exist to prevent, so count lines, not hits.

If you cannot obtain the vectors, say so and leave the cell relayed. Do not simulate having done it.

---

## 6. One inconsistency you will notice. Report it; do not fix it.

The sibling candidates C-1 and C-2 (kissing numbers in dimensions 13 and 14) carry a bar that runs
**opposite** to this one on the same signal. C-1's reads:

> PASS iff 1154 still stands at primary tier **AND at least one of those systems reports having
> attempted dimension 13.** An unattempted cell is only unvisited, and the next run of theirs will
> visit it.

So for C-1, *a system having attempted the cell* is a **PASS** condition — evidence the cell is
genuinely hard. For C-3, a system having attempted the cell is a **FAIL** condition. The same
evidence, opposite directions.

There is a defensible reason (for C-1 the record was *not* set by an AI system, so an attempt that
failed is evidence of hardness; for C-3 the record *was* AI-set, so further attempts mean an actively
contested cell). **But the asymmetry is real and it is not stated in either bar.** Apply C-3's bar
exactly as written in §2, and report the asymmetry as a finding. This project's rule is that bars are
recorded, not redrawn after the fact — a previous gate whose bands were wrong was closed as
*recorded, not fixed*, and the bands were explicitly not redrawn.

---

## 7. Rules that are not negotiable

1. **A bar you cannot evaluate is FAIL.** Not "unscored."
2. **Tier every claim**: `PRIMARY-VERIFIED-LOCALLY` (you computed or checked it), `SECONDARY-RELAYED`
   (a source says it and you read the source), `RECALL` (you believe it, citation not solid). **A
   RECALL cell with its value stated beats a confident cell with no tier.** This project's worst
   near-miss was a nine-year-stale recall that would have produced an entirely fictitious worklist.
3. **Withdrawn and unrefereed claims are data, not resolutions.** A claimed resolution of the
   anisotropic Calderón problem was posted and withdrawn days later by its own authors — "the
   argument is incorrect" — and still recirculates in citation lists. If you find a record claim,
   check whether it stands.
4. **Do not guess to produce a tidy verdict.** Saying "I could not establish this" is the required
   answer when true, and it costs nothing. A registered prediction in this project's ledger turns on
   exactly that: a verdict issued on a bar the run could not evaluate falsifies it.
5. **Derive counts; do not type them twice.**

---

## 8. What to return

A single document, in this order:

1. **The verdict line, first:** `C-3: PASS` / `C-3: FAIL` / `C-3: CANNOT EVALUATE`.
2. **The bar, quoted verbatim** from §2.
3. **The record as you found it** — value at *n* = 8, the table, its date, who set it, each cell
   tiered. Flag any disagreement with §1.
4. **A per-system adjudication table.** One row per AI search system you examined: system, paper
   identifier, *which cap-set object it actually worked* (§3's three columns), whether it reports
   attempting AG(8,3) **directly**, and the tier of that determination. **Every row gets a reasoned
   adjudication — a row you cannot adjudicate is named as such, not dropped.**
5. **Coverage of the negative.** If your verdict is PASS, it rests on absence, so say where you
   looked and found nothing. A PASS with no stated coverage is not evaluable.
6. **The §6 asymmetry**, stated as a finding.
7. **Anything that contradicts this prompt.** Several figures here are relayed and marked so; if one
   is wrong that is the most useful thing you can report.

**Do not recommend what to do next.** The verdict and the evidence are the deliverable; the decision
belongs to the instance holding the queue.
