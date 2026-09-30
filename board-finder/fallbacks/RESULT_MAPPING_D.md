# Mapping chunk D — result, and the first out-of-sample test of the corrected metric

27 records, ranks 120–350, analysis / quantum / logic / probability / applied. Classification
derived from `mapping_D_class.json`, not typed.

```
NONE (structural, no tracked number)   5  (125, 126, 167, 172, 346)
NOT FOUND (no source located)          1  (328 — no numeric q0(d) for nearest-neighbour Potts)
RESOLVED in the last 90 days           0
CLOSED IN PRACTICE in the last 90 days 0
```

All 27 remain formally open. Chunk D is the last chunk; **106 of 106 records are now mapped.**

## 1. The NONE metric does not order the chunks, and D is the proof

| | records | NONE | rate |
|---|---:|---:|---:|
| A discrete / TCS / coding | 31 | 0 | **0%** |
| B number theory & algebra | 26 | 3 | 12% |
| C geometry & topology | 22 | 1 | 4.5% |
| **D analysis / quantum / logic** | **27** | **5** | **18.5%** |

D returns the highest `NONE` rate of the four. The pre-registered prediction in
`RESULT_MAPPING_A.md` §5 was **specifically about C** and was scored in `RESULT_MAPPING_C.md` §1 —
it is closed, and nothing here re-opens it. But D settles the wider claim that prediction rested
on: I ordered the chunks A-richest-to-C-poorest and the `NONE` rate runs **0% → 12% → 4.5% →
18.5%**, which is not an ordering at all. The metric was not just mis-aimed, as C showed; it does
not even rank domains monotonically.

## 2. D is held-out data for the metric I built after C, and that is what makes it worth having

The corrected metric in `RESULT_MAPPING_C.md` §3 — *tracked quantity is a **number** and
`WHAT MOVES IT` is **construction** or **computation*** — was constructed **after** A, B and C had
been read. Applying it to them was fitting. **D had not been run when it was written, so D is the
only clean test it will ever get.**

| | records | quantity is a number | of those, mover is construction/computation | survives reading |
|---|---:|---:|---:|---|
| A | 31 | — | ~4 (238, 283, 337, 345) | **345** |
| B | 26 | — | 3 (239, 301, 348) | **239** |
| C | 22 | — | 1 (335) | none |
| **D** | **27** | **10** | **2** (235, 282) | **none** |

Out of sample the metric behaves the way it did in fit: it selects a small handful, and the
handful mostly dies on a second criterion. **2 of 27, both dead.** No new queue entry from D.

### Both clauses are load-bearing, which a post-hoc two-clause metric had no right to be

D is also the first chance to ask whether the metric's two clauses are doing independent work or
whether one is decorative:

* **Clause 1 (must be a number) rejects 3** records whose mover is exactly right — **126**
  (unconditional BQP verification: construction, but a binary existence question), **152**
  (∃R: construction of new completeness reductions, but the quantity is a growing catalogue), and
  **266** (2D inviscid Boussinesq: the mover is literally *computer-assisted proof*, and there is
  still no number to beat).
* **Clause 2 (mover must be construction/computation) rejects 8** records with a perfectly real
  number — **174, 191, 212, 215, 306, 320** on `proof technique`, and **205, 221** on asymptotic
  algorithm design.

Neither clause is redundant, and each rejects records the other would have let through. That is
not something I arranged; it fell out of held-out data.

**266 is the sharpest of these.** It has the right mover and no number, while **212** (Skolem: the
order-4 threshold) and **320** (Positivity: orders 5 / 9 / 11 / 17) have crisp numbers and a
pure-proof mover. Put side by side they show why the old `NONE` screen kept mis-scoring: three
records that all look "quantified" and are in three different categories for us.

## 3. Adjudications the two clauses owe, because "adjudicate" is not a verdict

`../gap/epoch_gate.py` refuses a verdict until every collision carries a reasoned adjudication.
Same rule here. Three records sat on the boundary and each gets a decision:

**205, dihedral HSP — FAIL on Δ.** The tracked number is real and frozen since 2003–2005:
2^O(√log N), Kuperberg and Regev. Enormous headroom. But the deliverable is *an asymptotically
faster quantum algorithm with a proof*, and there is no object to exhibit and no witness to check.
H without Δ is worthless — that is the v3 rule, applied against a record that scores maximally on H.

**221, random 3-SAT threshold — FAIL on Δ and on verification.** This is **the longest-frozen
number in all 106 records**: the lower bound r₃ ≥ 3.52 has not moved since Hajiaghayi–Sorkin 2003,
twenty-three years, against a physics estimate of ≈4.267 and an upper bound of 4.49. It is the one
record in D I would have wanted to want. It fails anyway: the bound comes from a
differential-equation analysis of a specific algorithm, so the deliverable is a theorem whose
verification is an analytic argument, not a mechanically checkable witness — and this project's
one durable strength is verification. Twenty-three years of freeze on a famous number in a heavily
worked area is also evidence of a barrier, not of neglect.

**266, 2D inviscid Boussinesq — FAIL on clause 1, as above.** Blowup is proven *with* a boundary
(Chen–Hou) and *with* forcing; the free smooth problem is open in both directions. The region is a
function space, not a writable unknown set.

## 4. 235 is the finding in chunk D, and it cuts two ways

**235, Zauner / SIC existence, is the one record in D that passes the metric cleanly** — highest
dimension with an exact fiducial constructed, moved by construction. It is also
**`board-finder/gap/RESULT_GAP_v2.md`'s U16, which this project retired in August**, killed by
`../playability/GATE_RESULT_SIC.md`: **PREFIX, hole list EMPTY**, exact fiducials covering every
dimension through 53 (safe) / 57 (probable), and above that a sparse structured tail at a frontier
with a Grassl seminar three days before the gate ran.

### The good cut: the metric re-found, from a cold corpus scan, a target we had picked ourselves

C got one consistency check of this kind — 335, the Jones unknot conjecture, was the single record
the metric liked in chunk C and it was already excluded at step 0 as Epoch entry #9. D gives the
second, and a stronger one, because 235 was excluded not by an external list but **by our own
gate, by a different route, on a criterion (`PREFIX` vs finite hole list) the mapping metric knows
nothing about.** Two independent screens agreeing on held-out data is the most reassurance this
instrument has produced.

### The bad cut, and it is the one to carry forward

The searcher's cell for 235 reports exact solutions *"for select much higher dimensions via a
2022–2025 Stark-units program … reaching d=19,603"*, tiered **PRIMARY**, sourced to
*J. Math. Phys.* 66, 082202.

Our own gate, run earlier and independently, recorded the correction to exactly that number:

> *"39604 is the **numerical** maximum; the exact ceiling is 5799 [**5,779** — the digit was wrong; D49], and the papers reaching
> 19603/39604 'admit their exact verification was mostly partial'."*

So on **the one record in all four chunks where we hold an independently obtained local result,
the mapping layer's PRIMARY-tiered cell reproduces the numerical/exact conflation that a
dedicated gate was built to catch.** Not a fabrication — the paper and the dimension are real, and
19,603 = 140² + 3 checks out — but the cell is coarser than the question a gate has to answer.

**That is a measured resolution limit, and it is the transferable result of this chunk:** the
mapping layer is triage-grade, not gate-grade. One question per record buys you *which records
have a movable number*. It does not buy you *what the number is*. Nothing may be gated on a
mapping cell; every candidate that leaves this layer still needs its own promoting search. Had we
met 235 here first instead of in a dedicated gate, we would have started work against a ceiling of 19,603 where the verified exact ceiling is 5,799 — a
factor of 3.4, in the direction that makes a search look feasible when it is not.

The Jan 2026 single-author preprint (arXiv:2601.13475) claiming general SIC existence changes
none of this either way, and the searcher was right to decline it: **U16 was retired on shape, not
on the conjecture's status** — a prefix with an open tail at a crowded frontier is worthless to us
whether or not Zauner is eventually proven.

## 5. 282 is the only genuinely new pass, and it dies on headroom

**282, exact unassisted quantum capacity of the qubit depolarizing channel.** A real numeric
target — tightest known upper and lower bounds on Q(D_p), with a real gap at essentially all p —
and the mover includes numerical optimization, which is our shape.

It fails **H**. The bounds were tightened in **2025** (arXiv:2506.03429) by Riemannian optimization
over flagged channel extensions: that is precisely the method we would bring, applied within the
last year by people who own the tooling. This is the PTE 11 lesson in a new domain — our reachable
region sits inside someone else's, and we would find it out after paying for the search rather
than before. Verification is the second problem: a capacity bound certificate is a numerical
optimization argument, not a witness.

## 6. Three declined claims in 27 records — the tiering fired at 11%

| rank | claim | searcher's handling |
|---:|---|---|
| 172 | arXiv:2204.03295 (2022) claims general poly-time HSP | RECALL, "not treating it as a resolution" |
| 183 | arXiv:2409.01583 (Uhlmann–Zhai) claims anisotropic Calderón resolved | reported as **posted and WITHDRAWN days later**, *"the argument is incorrect"* |
| 235 | arXiv:2601.13475 (Jan 2026) claims general SIC existence | RECALL, no corroboration found |

**183 is the one worth keeping.** A claimed full resolution of a top-200 problem was posted in
September 2024 and withdrawn within days by its own authors, and the searcher flagged it
specifically as *"a live false-positive that periodically resurfaces in citation lists"*. That is
the W(103) failure mode with a DOI attached: a retraction does not propagate as fast as the claim.
Any future screen that reads a citation list rather than the abstract page will pick 183 up as
resolved and be wrong.

Set against chunk A, where the same instrument caught three real resolutions I did not know about,
the record is now: the mapping layer detects fresh movement reliably, declines uncorroborated
claims correctly, and **states known quantities less precisely than a gate needs.** All three are
worth knowing and only the third was a surprise.

## 7. Movement outside the 90-day window

Real, dated, correctly placed outside the resolution window by the `STATUS TODAY` field — the same
behaviour C §4 recorded for 272:

| rank | movement | date |
|---:|---|---|
| 212 | Skolem decidable for algebraic LRS of order ≤4 (Bacik), journal version | Dec 2025 |
| 235 | Stark-units construction reaching d = 19,603 (n²+3 = 4p) | Aug 2025 |
| 253 | Witten WRT proven for all Seifert fibered homology spheres, r ≥ 3 fibres | Oct 2025 |
| 306 | Mumford–Shah: ≤ 3 traces near any singular point in dimension 2 | Sept 2025 |
| 167 | P_C ≠ NP_C implies VP ≠ VNP (Bürgisser), tightening the link | 2026 |

Five of 27 records moved in the last thirteen months without any of them resolving. The corpus
lists all five as `open` and is right to; what it cannot show is that four of the five moved.

## 8. Final tally — 106 records, two candidates, neither of them first

| chunk | records | usable on the metric | survived reading |
|---|---:|---:|---|
| A | 31 | ~4 | 345 Erdős–Szekeres |
| B | 26 | 3 | 239 odd perfect number |
| C | 22 | 1 | — |
| D | 27 | 2 | — |
| **total** | **106** | **~10** | **2** |

**The corpus is exhausted as a candidate source.** 106 records carrying record-or-algorithmic-
deficit language, screened across four independent passes, produced two queue entries, and the
candidate still standing at the head of the queue came from our own pool instead. The mapping
layer was worth building — it was the cheap breadth task `../gap/GAP_V3.md` §6 said would get
cheaper, it corrected the "the band is barren" reading that `QUEUE_V3.md` Direction B was wrong
about, and it caught five resolutions or near-resolutions. It did not find us a target.

That is a publishable null on our own method, and it should be read the way we ask anyone else's
null to be read: the screen ran to completion, the bars were set in advance, and the answer is no.

## 9. Queue after four chunks — unchanged

| | candidate | from | first check |
|---|---|---|---|
| **1** | **U13 D-optimal designs** | **our own pool** | current table: which *v* are open, and when was each last moved? |
| 2 | 239 odd perfect number | chunk B | the two risks in `RESULT_MAPPING_B.md` §3 |
| 3 | 345 Erdős–Szekeres | chunk A | one cheap read of arXiv:2512.24061 |

Unchanged by C and unchanged by D. `prompts/U13_D_OPTIMAL.md` is ready to hand over if the
Hadamard 2092 kill test in `../hadamard/PLAN_2092.md` fails.

**Nothing further is owed to the mapping layer.** All four chunks are run, all 106 records are
mapped, and the next expensive act on this board is the 2092 growth-law re-fit, not another screen.
