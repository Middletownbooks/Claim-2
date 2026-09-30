# Brief C — five arm-1 verdicts that rest on a tier the last run could not improve

> **[DISPATCH VERSION, 30 Sep 2026.]** This brief was written before briefs A, B1, B2 and D ran.
> **The five questions in §1, their order, and the 22-call cap are unchanged** — those are the
> pre-registration and re-scoping them after four runs is exactly what D44 forbids. What has been
> added is four rules those runs paid for, a verified control for the brief's own model case, and one
> clause that turned out to matter more than any bar: **§5, report anything that contradicts this
> brief.** Brief D's single most valuable finding arrived through that clause and not through its
> gate.

**For a Sonnet 5.5 instance in a chat conversation with web search and page fetching. No repository,
no filesystem. Your output is a document in your reply.**

Arm 1 screened nineteen records and returned **0 full-bar survivors**. That result stands and this
brief does not reopen it. But **five of those nineteen failed on a cell the earlier container could
not reach**, and each is one specific question with a yes-or-no answer. This brief asks those five
questions and nothing else.

Four of the five turn on the **same clause**, so read it once and carry it through:

> **S1 COUPLED** … An asymptotic-order headline is COUPLED only through a **published lifting
> theorem** that turns a finite object into an asymptotic bound (the cap-set product construction is
> the model case).

The model case is worth holding in mind precisely, because it is the shape you are looking for
everywhere below: a cap set of size *c* in 𝔽₃ⁿ can be **tensored** with itself to give caps of size
*c*^k in 𝔽₃^(nk), so **one finite object of size *c* in dimension *n* yields the asymptotic lower
bound *c*^(1/n) on the cap-set constant.** That is a lifting theorem. It is what makes a finite search
move an asymptotic headline. **Your question, four times over, is whether the analogous theorem exists
and is published.**

**That arithmetic is verified, not asserted, and you can re-run it in seconds.** This matters because
the last brief in this series shipped a locally-computed claim marked *"treat it as given"* that was
the only false statement in the document (debt **D53**), so the model case here is given to you as a
control you can break rather than a premise you must accept:

```python
import itertools
def is_cap(S):
    Sset = set(S)
    for i, x in enumerate(S):
        for y in S[i+1:]:
            z = tuple((-(a+b)) % 3 for a, b in zip(x, y))
            if z in Sset and z != x and z != y:
                return False
    return True

def tensor(S, T):
    return [s + t for s in S for t in T]

# maximal caps in dimensions 1, 2, 3 — sizes 2, 4, 9
c1 = [(0,), (1,)]
c2 = [(0,0), (0,1), (1,0), (1,1)]
c3 = [(0,0,0),(0,0,1),(0,1,0),(0,1,1),(1,0,0),(1,0,1),(1,1,2),(1,2,2),(2,1,2)]
# (c3 was produced by exhaustive search, not typed from memory: my first attempt at
#  writing these nine points by hand was NOT a cap, and the assertion below caught it.)
assert is_cap(c1) and is_cap(c2) and is_cap(c3)
assert len(c3) == 9
# NEGATIVE TEST: (0,2) completes the line {(0,0),(0,1),(0,2)}, so this MUST fail
assert not is_cap(c2 + [(0,2)])

# the lifting: a cap of size c in dim n gives caps of size c^k in dim nk
cur = c2
for k in (2, 3):
    cur = tensor(cur, c2)
    assert is_cap(cur) and len(cur) == 4**k
    assert abs(len(cur)**(1.0/(2*k)) - 2.0) < 1e-12     # constant c^(1/n), invariant in k
# and a better finite object gives a better constant — this is the whole mechanism
assert 9**(1/3) > 4**(1/2)
```

**Run it, including the negative test.** Note the last line: the dimension-3 cap certifies
9^(1/3) ≈ 2.080 against the dimension-2 cap's 4^(1/2) = 2.0. **That is why a finite search moves an
asymptotic headline, and it is the exact shape you are looking for four times below.** If any of these
assertions fails, say so — it would mean this brief's model case is wrong, which outranks all five
answers.

## Why you are being asked, and it is not that the last run was careless

An earlier run of this work was done by nine parallel agents inside a container whose network
**blocked arxiv.org, Wikipedia, every publisher, and every maintained-table host it probed** — Cohn's
kissing tables, the La Jolla difference-set repository, Brouwer's tables, Packomania. Only web search
and `raw.githubusercontent.com` were reachable.

That run's own provenance rule says a cell seen **only in a search-result summary** is
`SEARCH-SUMMARY`, which is **RECALL-grade and not usable for any gate**. So almost every literature
verdict it produced rests on a tier that cannot support it, and the run says so itself: *"in this
environment almost every literature cell will be `SEARCH-SUMMARY`, so no survivor of this run can be
more than triage-grade."* Two of its arms also stopped on a concurrency cap and a search budget
rather than on evidence.

**You can reach the hosts it could not.** That is the entire reason this is being re-run, and it is
your job: **move cells from `SEARCH-SUMMARY` to `SECONDARY-RELAYED` by reading the source itself.** A
verdict you return at `SEARCH-SUMMARY` adds nothing that is not already on file.

## Provenance tiers. Every cell you report carries one.

| tier | meaning | usable for a gate? |
|---|---|---|
| `PRIMARY-VERIFIED-LOCALLY` | you computed or checked it yourself | yes |
| `SECONDARY-RELAYED` | **you read the source text itself** — the table page, the paper, the repository file | yes |
| `SEARCH-SUMMARY` | seen only in a search result's title or snippet; source not opened | **no** |
| `RECALL` | you believe it; no source found | no |

Every value also carries **EXACT / RIGOROUS-NUMERIC / NUMERICAL / UNKNOWN** and **REFEREED /
PREPRINT / ANNOUNCED / WITHDRAWN**.

**Do not upgrade a tier to make an entry count.** A `SEARCH-SUMMARY` cell reported honestly is worth
more than a `SECONDARY-RELAYED` cell you did not earn — the project's worst near-miss was a
nine-year-stale recall that would have produced an entirely fictitious worklist.

## Two rules that have cost this project more than any others

**Numerical is not exact, and claimed is not refereed.** A breadth pass once reported exact SIC-POVM
constructions *"reaching d = 19,603"*; a dedicated check had already established the exact ceiling
was **5,779**, with the higher papers admitting their verification was *"mostly partial."* Both cells
were true at their own precision; one was usable. **Where a value's meaning depends on which sense is
meant, report both senses rather than picking one.** Watch especially for *projective* versus
*affine*, *numerical* versus *exact*, and asymptotic constants versus finite instances.

**Withdrawn and unrefereed claims are data, not resolutions.** A claimed full resolution of the
anisotropic Calderón problem was posted and withdrawn days later by its own authors — *"the argument
is incorrect"* — and still recirculates in citation lists. If you find a record claim, check whether
it stands.

## Four more rules, each paid for by a run since this brief was drafted

**Two quantities can share one name, and that is worse than two precisions of one quantity.** Brief B2
was sent out with *"exhaustive enumeration reaches order 29"* as though it answered the record *"the
smallest order with no known Costas array"*, which is **32**. Three apart, both correct, different
things. The numerical-versus-exact rule above catches two readings of one number; this catches two
numbers wearing one label. **For Q4 especially — star discrepancy — ask which variable the asymptotics
is in before you accept any statement.**

**Report the strength of a theorem, not only its existence.** Brief D found a genuine published
theorem constraining Costas arrays (ascent counts within 2.5 of (*n*−1)/2) and computed that applied at
the target order it retains **93.4% of all permutations — 0.10 bits.** A real, refereed, correctly
stated theorem worth essentially nothing as a constraint. **So a lifting theorem that exists but gives
α < 1, or a constant far from the truth, is a different answer from one that gives the sharp order**,
and a bare YES that hides the difference is close to useless. The answer block below has a `STRENGTH`
line for this.

**Do not describe a paper from its title.** This project characterised an arXiv paper from its title
alone, inside a prompt that warned against doing so, and separately reported a system as having moved
one quantity when it had moved two. **If you did not open it, write that you did not open it.** The
tier table above is how you say that; use it rather than hedged prose.

**"Not seen" is not "does not exist", and the difference is Q4's whole verdict.** Arm 1's own note on
record 375 was *"no lifting theorem seen"* from a container that could not open the sources. Your job
is to convert that into one of three things — a theorem, an established absence, or an honest
UNRESOLVED — and the third is a perfectly good answer.

## Budget, and the failure this replaces

The earlier run died on search limits. **So: a hard cap per brief, stated in the brief, and a
partial report is a success.** Stop at the cap and report what you have, marking the rest NOT
REACHED. Do not silently run dry. A brief that returns three solid `SECONDARY-RELAYED` rows and
names the rest as unreached is worth more than one that returns ten `SEARCH-SUMMARY` rows.

## You have no repository

Everything you need is inside your brief. Return your output **in your reply**, as a single
document. Do not ask for files and do not assume you can write any.


## Fetch mechanics, learned the hard way on Brief A — read this before your first call

Brief A lost four of its 22 calls to two mechanics. Both are avoidable:

* **The fetch tool only opens a URL that a search result (or this brief) has already surfaced.** A bare
  hostname written in a brief was **refused** until a search had produced it. So for every maintained
  table below: **search for it first, then fetch from the result link.** Budget one search plus one
  fetch per host, not one fetch.
* **arXiv is rate-limited rather than blocked, and asymmetrically.** Older identifiers opened;
  a September 2026 identifier was refused three times in a row. If a recent paper refuses, **do not
  retry more than once** — spend the call elsewhere and mark the cell NOT REACHED.

* **`robots.txt` refusals are a third, distinct cause.** A run lost a call to `mathweb.ucsd.edu`
  (a PDF) **refused because robots disallowed it** — not a rate limit and not an unsurfaced URL. If a
  host refuses this way, it will keep refusing; look for the same paper on arXiv or a different mirror
  rather than retrying.

A fourth mechanic, worth knowing because it invalidates a cell rather than costing a call: **a live
artifact can change while you read it.** On Brief A a GitHub README showed ten dimensions in the
search snapshot and nineteen when fetched, with one record's claimed increase shrinking 44.4%. If a
value moves between your search and your fetch, **report both and gate on neither.**

---

## 1. The five questions

**Q1 — record 186, the order of magnitude of maximum 3-term-AP-free subsets of {1,…,N}.**
Arm 1 returned **S1 FAIL** on this note: *"asymptotic; only lifting known is the product lemma, giving
N^α with α<1"* — **and tiered that note `RECALL`.** A FAIL resting on RECALL is the weakest verdict in
the whole arm.
> **Ask:** is there a published lifting or product theorem taking a finite AP-free set in {1,…,N} to
> an asymptotic bound on the order of magnitude of the maximum? What exactly does the product lemma
> give, and is α<1 correct? Behrend's construction and the Kelley–Meka upper bound are the landmarks
> to orient by. **Answer at `SECONDARY-RELAYED` — read the statement, do not relay a summary of it.**

**Q2 — record 277, the growth rate of 3-uniform hypergraph Ramsey numbers.**
Arm 1 returned **S1 = CANNOT EVALUATE**: *"could not check for a lifting theorem."*
> **Ask:** does a published construction lift a finite 3-uniform hypergraph colouring into an
> asymptotic lower bound on the growth rate? Erdős–Hajnal–Rado is the classical line; look for a
> product or amplification lemma.

**Q3 — record 353, the asymptotic Turán numbers of even cycles.**
Arm 1 returned **S1 = CANNOT EVALUATE**, same reason.
> **Ask:** for ex(n, C_2k), does a published theorem take a finite extremal or near-extremal graph to
> an asymptotic constant or order? The Bondy–Simonovits upper bound O(n^(1+1/k)) is the landmark;
> the question is about the **lower-bound** side and whether a finite object lifts.

**Q4 — record 375, the sharp asymptotic order of the minimal star discrepancy in each dimension.**
Arm 1 returned **S1 FAIL** on *"asymptotic, no lifting theorem seen."* **"Not seen" is a weaker claim
than "does not exist"**, and the container could not open the sources that would settle it.
> **Ask:** does a published theorem take a finite point set of given discrepancy to an asymptotic
> bound on the order in that dimension? Note the specific trap here: this literature is full of
> results where the **dimension dependence** is the open part, so be precise about which quantity the
> asymptotics is in — *n* or *d*.

**Q5 — record 385, the Lieb–Thirring conjecture on the sharp constant for Riesz means.**
Arm 1 returned **S1 = PASS (formal)** but **S2 = CANNOT EVALUATE**: *"the witness side is a
counterexample potential; no rigorous-enclosure source found."* This one is not a lifting question.
> **Ask:** is there a published **rigorous numerical enclosure** — interval arithmetic, a
> computer-assisted proof, a certified bound — for the relevant Lieb–Thirring constant, such that a
> candidate counterexample could be certified by terminating computation? The distinction that decides
> S2 is **RIGOROUS-NUMERIC versus merely NUMERICAL**, and this project has been burned by exactly that
> distinction before. If the literature offers only floating-point computations, say so: that is a
> clean S2 FAIL and a real answer.

---

## 2. What a good answer looks like, and what an answer is not

For each question, one block:

```
RECORD        | <number and name>
QUESTION      | <restated in one line>
ANSWER        | YES, a published theorem exists | NO, and here is why that is established | UNRESOLVED
THE THEOREM   | <name, authors, year, and the statement in one or two lines> — or "none found"
SOURCE OPENED | <url or citation you actually read>
TIER          | SECONDARY-RELAYED | SEARCH-SUMMARY | RECALL
WHAT IT GIVES | <what a finite object of size X in dimension/length n yields asymptotically — the arithmetic, if any>
STRENGTH      | <sharp order | correct order, loose constant | weaker than the known bound | negligible as a constraint> — and the number, if you can compute one
GATE EFFECT   | <does S1 (or S2 for Q5) now PASS or FAIL, and is that a change from arm 1's verdict?>
```

**A `NO` is as valuable as a `YES` and harder to earn.** "I searched and found nothing" is not a NO;
it is UNRESOLVED. A NO needs either a source saying no such lifting is known, or a survey of the
lower-bound methods that would have mentioned one. **Say which of the three you are giving.**

**If any answer flips a gate, say so plainly but do not re-run the rest of the bar.** Arm 1's other
gates for that record stand as recorded; your job is the one cell. Flipping S1 on record 186 from a
RECALL-grade FAIL to a sourced PASS would not resurrect the record — it still has S3, S4 and S5 to
pass — but it would mean the arm's headline number was reached partly by a cell that could not carry
it, and that is worth knowing about the instrument regardless of the record.

---

## 3. Budget

**Stop after 22 searches-or-fetches.** Report what you have and mark the rest NOT REACHED.

**The cap was raised from 15, and the reason is a measurement rather than generosity.** A sibling
brief ran with a cap of 25 and used 22 to cover roughly five topics at depth, with **four of its 22
calls failing** — three arXiv rate limits and one refused URL. At that observed rate, five questions
each needing *search a survey → open it → read its lower-bound section* do not fit in fifteen calls,
and my original figure of "roughly three per question" was wrong.

**Work the questions in this order and stop when the cap is reached.** The order is by how much the
answer would change:

1. **Q1, record 186** — highest value, because its FAIL rests on a cell tiered `RECALL`, the weakest
   verdict in the whole arm, and because this is the literature the model lifting case comes from, so
   the answer should be findable.
2. **Q2, record 277** and **3. Q3, record 353** — the same question in two places.
3. **Q4, record 375** — a weaker starting claim (*"not seen"*), but a sprawling literature.
4. **Q5, record 385** — a different question, and the likeliest answer (only floating-point
   computations exist) is a clean FAIL that changes nothing.

**Three questions answered at `SECONDARY-RELAYED` with two marked NOT REACHED is the expected
outcome and is a success.** Five answered at `SEARCH-SUMMARY` adds nothing to what is already on
file.

## Report a call ledger. A sibling brief did this unasked and it is why its failures were diagnosable.

Give **the number of calls used against the cap** and **every failed call with its cause**. Those
lines are what identified the two fetch mechanics above; a run that reports only findings cannot be
audited the same way.

## 5. Report anything that contradicts this brief. This clause has outperformed every bar on this board.

Several statements above are relayed or derived rather than checked: arm 1's five quoted notes, the
landmark attributions (Behrend, Kelley–Meka, Erdős–Hajnal–Rado, Bondy–Simonovits), and the three fetch
mechanics. **If one is wrong, that is the most useful thing you can report**, ahead of all five
answers.

**This is not boilerplate, and here is the evidence.** The previous brief in this series told its
reader to *"Treat it as given"* that the known Costas arrays at order 31 were sporadic and had been
found by search, and built its entire justification on a 5-bit figure derived from that. The claim was
locally computed and carried this project's highest provenance tier. **It was also the only false
statement in the brief** — the arrays are constructible, from a second operator the computation never
modelled. The run refused the premise it had been instructed to accept, and was right; the finding was
worth more than the verdict it was sent to produce. Debt **D53**: *a verified computation licenses only
the claim it computes, and the tier does not travel to the next sentence.*

So: **when a premise here is load-bearing, ask what would falsify it, and say so if you cannot.** You
are not expected to defer to this document.

**Do not recommend what to do next.** The five answers and their tiers are the deliverable.
