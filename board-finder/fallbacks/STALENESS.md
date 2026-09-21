# The frontier is moving faster than the screening cycle

**Measured 21 Sep 2026, prompted by the user finding that rank 234 was resolved.** **All five** of the candidates named in `QUEUE_V3.md`, plus one from the tail screen, were already gone when I named them, all
within the preceding eight days.

## 1. What moved

| rank | candidate | what happened | date |
|---:|---|---|---|
| **234** | k-Server Conjecture, general metrics | **RESOLVED.** arXiv:2609.15979, Coester–Koutsoupias–Zbysiński (Oxford), *"The k-server conjecture is true"* — WFA is *k*-competitive on every metric space | **14 Sep 2026** |
| **438** | Matroid Secretary Conjecture | **RESOLVED.** arXiv:2609.14555, Singla (Georgia Tech), *"The Matroid Secretary Conjecture is True"*, 1/4-competitive. Three follow-ups within days (2609.17782 → 3.7321-competitive; 2609.19118; 2609.20797) | **13 Sep 2026** |
| **310** | Deterministic poly-time exact bipartite matching | **claimed RESOLVED** — arXiv:2604.01571, Du, deterministic O(n⁶) with machine-checked formalization | **Apr 2026** |
| **283** | Polynomial-time explicit log-Ramsey graphs | **closed up to polylog** — Li, ECCC TR23-023, K = log^O(1) N | 2023 |
| **337** | Capacity of the binary deletion channel | **effectively closed as a target.** arXiv:2609.19412, *"Binary Deletion Channel Capacity to Within One Hundredth of a Bit"*, plus 2609.13351 and 2604.05867 in the same window | **Sep 2026** |

I named 337 six hours before writing this as *"the best single mid-band candidate… no
collaboration route, so on this corpus's own signal nobody has flagged it."* It is one of the most
actively worked problems on the list. The corpus's collaboration field measured the corpus, not
the literature, and I read it as the literature.

## 2. The corpus is not stale — it is unreviewed

This is the part that generalises.

```
corpus editionDate      2026-09-19
records with statusReviewedAt = None      398 of 499   (80%)
review dates present    2026-09-14 (97), 2026-09-16 (2), 2026-09-19 (2)
```

Rank 234 was resolved on **14 September**; the corpus shipped on **19 September** still listing it
`open`, with `statusReviewedAt: None`. Its status was *carried forward*, not re-checked — which the
`statusQualification` boilerplate says outright: *"This is reuse of accepted evidence, not a new
source or status certification."*

**And all ten of the candidates this project has named from the corpus sit in the unreviewed 80%** —
234, 337, 283, 310, 345, 331 (Hadamard), 393 (CC-6), 426 (MUB), 349 (kissing), 235 (SIC).

So every `open` we relied on is, in this project's own provenance scheme, **RECALL tier**: believed,
with no dated source behind it. We treated a field as a status certificate and it is explicitly not
one.

## 3. VibeMathed — a fifth step-0 database, and the most relevant one

`vibemathed.com` (community-curated, CC BY 4.0, mirror at `github.com/mrconter1/vibemathed`) tracks
problems *"no human had solved before, proved or disproved with AI in the loop"*, with model
attribution, dates, and explicit verification labels. It is the database that would have caught 234
immediately — its entry carries `Solved 2026-09-14`, `Model GPT 6 Astra`, `Verification Unreviewed`.

It also lists **Hadamard order 668** as AI-solved, credited to three humans and Claude — our own
thread's context, tracked by a list we did not know existed.

Step 0 was four databases (Epoch FrontierMath, TheoremDB, Horizon, erdosproblems). **It is five.**

*Operational note: `vibemathed.com` is blocked by this container's egress proxy. It has to be
checked from outside, or from its GitHub mirror.*

## 4. The correction this forces on GAP_V3

`../gap/GAP_V3.md` §3 classified gaps and concluded: hold **algorithmic-idea** targets, because
that category improves with model capability.

**k-server and matroid secretary are both exactly that category, and both were taken in the same
week.** One with an AI supplying the central generalization, one apparently without. The category
that improves is also **the category being swept fastest**, and the sweep is not only by AI — the
field is moving.

So the amended rule:

> A gap type that improves is not thereby an opportunity. **Improving fast and being contested fast
> are the same property.** What is durable is not a gap type — it is an **asset nobody else holds.**

Which points where the evidence has been pointing all along: the Hadamard repository — 163 findings,
an orbit apparatus, a measured growth law, thirteen ranked open orders — is **our own enumeration**,
on none of the five databases, and cannot be swept out from under us because nobody else has it.
D-optimal designs (U13) inherit that apparatus. **Everything drawn from a public list is exposed;
those two are not.**

## 5. The workflow template, which is the most useful thing in the k-server entry

How that proof actually happened, per VibeMathed's note:

1. The **authors** proved the previously unknown *k* = 3 case on arbitrary metrics, **without AI**.
2. Discussions with two frontier models helped them *understand and symmetrize* that potential.
3. A third model derived an **algebraic proof valid for arbitrary *k*** from the symmetrized form.
4. The authors supplied an explicit column representation; the model adapted the proof to it.

Not "point a model at a conjecture". The human contribution is **the smallest open case, solved by
hand**, and the model's contribution is **the reformulation that generalizes it.**

That maps onto this board exactly. `FINDING 157` §3 asks for the growth exponent to be halved —
0.503 to 0.252 — which is a request for a reformulation, not for compute. And the smallest-open-case
step is available: *v* = 487 is solved by Alpöge and the repo has never found it in its own ansatz.
**Solve 487 by hand or by any means, then ask for the reformulation that generalizes.**

## 6. What changes in the gates

Add one bar, ahead of all others, because it is the cheapest and it would have caught all three:

> **S0 — freshness.** Before a candidate is named, list arXiv postings in its area for the last
> **60 days** and check none resolves or closes it. A corpus status field is not a substitute; 80%
> of them were never reviewed.

`QUEUE_V3.md` is corrected in place. The mid-band mapping prompts are unaffected in structure — but
their `LAST MOVED` field is now the most important one on the sheet, not the third.
