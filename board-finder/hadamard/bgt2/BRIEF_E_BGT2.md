# Brief E — the *b* > 2 Hadamard region. Establish whether it exists before screening it.

**For a Claude Code instance with read access to BOTH repositories.** The hard requirement is
`Cooperative-AI-Defense`, branch `claude/hadamard-matrix-methods-vs79hi`, directory
`Cooperative-AI-Defense/hadamard/findings/`. **Without that access this brief cannot be run at all** — say so and stop; that
is a clean answer and it costs nothing.

**This is not a search and not a change to the live *v* = 523 work.** Five questions, all of them
reads of a repository. If you find yourself writing a solver you have left the scope.

> **Why this brief is defensive rather than a proposal.** The queue entry it comes from rests on one
> sentence quoted from `Cooperative-AI-Defense/hadamard/findings/OPEN_ORDERS.md` — quoted by an instance that **never opened
> that file**, having read a plan that read it. The queue entry's own author wrote: *"I cannot tell
> from outside whether it is live … Question for the original instance, not a proposal from me."*
> That caution is correct and this brief inherits it. **Assume my information is stale**:
> `../PLAN_2092.md` states it read roughly **fifteen of 163 findings**, and the count is now higher.

---

## 1. The claim under examination, and its provenance, which is the weakest part

`../../fallbacks/QUEUE_V3.md` option 3 quotes `Cooperative-AI-Defense/hadamard/findings/OPEN_ORDERS.md`:

> *"Across all 13 orders there are 126+ admissible (v, b) pairs with b > 2."*

and, of two orders:

> *"those two orders have never been screened or settled by anything in this repository."*

| cell | tier | why |
|---|---|---|
| the "126+ admissible (*v*, *b*) pairs" sentence | **relayed at TWO removes** | I read a document that quotes a file neither of us opened |
| "*b* > 2" — what *b* **means** | **UNDEFINED HERE** | no document in the private repo defines it. §3 refutes my only guess |
| "the 13 orders" — which thirteen | **AMBIGUOUS** | §3 shows two different thirteens are in play |
| "orders 669 and 721" | **arithmetically impossible as stated** | both ≡ 1 (mod 4); see §3 |
| `FINDING_133`: orbit reduction stops at *m* = 82, *"failures that are emptiness rather than solver weakness"* | relayed at two removes | **the most important item here — see §4, Q4** |
| `FINDING_155`: *v* = 523 is the target, ordering 523 ≺ 739 ≺ 659 ≺ 571 ≺ 643, density 2⁻¹⁴¹ | relayed at two removes, **arithmetic reproduced locally** (§2) | |

## 2. What I verified locally, so you can check me rather than believe me

`derive.py` in this directory, output in `VERIFIED_OUTPUT.txt`, every assertion passing. The
construction assumed: *H* of order 4*v* from circulant blocks with row sums *a_k*, Σ*a_k*² = 4*v*;
*d* an odd divisor of *v*−1; *r* = (*v*−1)/*d* + 1; *D* = (*r*−1)/2; *a_k* = ±1 + *d*(2*u* − (*r*−1)).

* **All six rows of `../PLAN_2092.md` §1's table reproduce exactly**, admissible-*d* lists included:
  *v* = 487 → *d* ∈ [9,3,1], *r* = 55, *D* = 27; 523 → [9,3,1], 59, 29; 571 → [5,3,1], 115, 57;
  643 → [3,1], 215, 107; 659 → [7,1], 95, 47; 739 → [9,3,1], 83, 41.
* **Two relations that table satisfies and never states:** `free_bits = 8D = 4(r−1)` exactly on all
  six rows, and `density exponent = free_bits − log2 E[#sol]` on all six to within 0.35.
* **Consequence, and it is the useful one:** free bits is a function of *d* alone. **The entire
  difficulty ranking of the worklist is decided by one arithmetic quantity — the largest odd divisor
  of *v*−1 that the row-sum law admits.** Nothing about the search enters it.

## 3. Three things in the queue entry that do not survive contact with arithmetic

**(i) My reading of *b* is refuted, and that is the most useful thing I can give you.** Take *b* = the
number of circulant blocks. Then every permitted *a_k* is **odd** — *v* is odd, so (*v*−1)/*d* is even
for odd *d*, so *r* is odd, so *d*(2*u*−(*r*−1)) is even, so *a_k* = ±1 + even. Asserted at every
(*v*,*d*) checked. An odd square is 1 (mod 8), so a sum of *b* odd squares is *b* (mod 8), and 4*v*
with *v* odd is 4 (mod 8). Therefore

> **Σ_{k=1..b} *a_k*² = 4*v* forces *b* ≡ 4 (mod 8).**

Verified: of *b* = 2…29, only *b* = 4, 12, 20, 28 admit **any** of the thirteen; *b* = 2, 3, 5, 6, 8
admit **none**. So under this reading "*b* > 2" would mean *b* ∈ {12, 20, 28, …} and nothing else —
**and a source reporting 126+ pairs with *b* > 2 therefore cannot mean this.** I do not know what *b*
means. **Do not inherit my guess; Q1 exists because it is wrong.**

**(ii) Two different thirteens.** The repo's own targets are *v* = 487, 523, 571, 643, 659, 739 →
orders 1948, 2092, 2284, 2572, 2636, 2956. The classical thirteen smallest open Hadamard orders are
668, 716, 892, 1004, 1132, 1244, 1388, 1436, 1676, 1772, 1916, 1948, 1964 (**`RECALL`, not verified —
checking this list is part of Q3**), whose *v* = *n*/4 are 167, 179, 223, 251, 283, 311, 347, 359, 419,
443, 479, 487, 491, all prime. **Only 1948 is in both.** So "all 13 orders" in the quoted sentence and
"thirteen" in the repo's target ranking are different sets, or one of them is not what I think.

**(iii) 669 and 721 are not Hadamard orders.** Both are ≡ 1 (mod 4), and a Hadamard matrix of order
> 2 requires order ≡ 0 (mod 4). So they are *v* or *m* values, giving orders **2676** and **2884**.
Both are **composite** (669 = 3·223, 721 = 7·103) while every *v* in the worklist is prime.
*Hypothesis, offered as a hypothesis:* they were never screened because the machinery assumes *v*
prime. **Falsifier:** the repo screening a composite *v* anywhere.

**One lead, with the reason to distrust it.** *v* = 721 admits *d* = 15, giving *r* = 49, *D* = 24 and
**192 free bits** — 24 fewer than *v* = 487, the order Alpöge **solved**, and 40 fewer than the live
target. That is the only thing in this brief that looks like an opportunity. **Distrust it:** free bits
is one of two coordinates, density = free_bits − log2 E[#sol], and I cannot compute E[#sol] without the
repo's estimator. A cheap free-bit count with almost no solutions is not an easier target. And whether
2884 is open at all is unverified.

## 4. The five questions, in priority order. Q1 and Q2 can end the brief.

**Q1. What is *b*?** Quote `Cooperative-AI-Defense/hadamard/findings/OPEN_ORDERS.md`'s definition **verbatim**, and confirm the findings that use
it use it the same way. Then reconcile it with §3(i): if the source's pairs include *b* = 3 or 6, my
derivation is irrelevant to its *b*, and saying so is the answer. **Nothing below means anything until
this is settled**, so spend here first.

**Q2. Is the region still unscreened?** `../PLAN_2092.md` read ~15 of 163 findings and is dated. **How
many findings exist now, and has any of them screened, settled, entered or abandoned *b* > 2?** A yes
ends the brief, and that is a full success. Also: **was `FINDING_155`'s ranking scoped to a single
*b*?** If it ranked across all *b*, the region is already ranked and there is nothing unswept; if it
fixed one *b*, the region is genuinely unscreened. **This single fact decides whether the queue entry
was ever real.**

**Q3. Which thirteen, and is 126+ derived or typed?** Resolve §3(ii). Then: does `Cooperative-AI-Defense/hadamard/findings/OPEN_ORDERS.md`
*compute* the 126+ figure, or state it? Is it current? A stale summary line in an index file is the
most likely single failure here.

**Q4. Are the admissible pairs non-empty — and has anyone tested?** **This is the question that
decides the region's worth.** An admissible (*v*, *b*) pair is a **necessary condition on parameters,
not evidence that an object exists there.** `FINDING_133` reportedly found the orbit-reduction route's
failures at *m* = 82 to be *"emptiness rather than solver weakness"*. Apply that distinction to *b* > 2:
does any finding test emptiness in the region, and what did it find? **126 admissible-but-empty pairs
are worth nothing.**

**Q5. 669, 721, and the lead.** What are they — *v*, *m*, or something else? Is 4·721 = 2884 an open
order? And does 721's 192 free bits survive a density calculation with the repo's own estimator — what
is log2 E[#sol], and what is the density exponent against the live target's 2⁻¹⁴¹?

## 5. The bar. Registered before dispatch; you may not re-scope it.

> **PASS iff all three hold:**
> **(a)** `Cooperative-AI-Defense/hadamard/findings/OPEN_ORDERS.md`'s definition of *b* is obtained and is used consistently by the findings
> that cite it; **and**
> **(b)** no finding written since `../PLAN_2092.md` has screened, settled, entered or abandoned the
> *b* > 2 region, **and** `FINDING_155`'s ranking was scoped to a single *b* rather than across *b*;
> **and**
> **(c)** at least one (*v*, *b*) pair with *b* > 2 carries a free-bit or density figure **better than
> the live target *v* = 523's 232 free bits / 2⁻¹⁴¹**.
>
> **FAIL on any one.** Clause (c) is the decision: a region is worth entering only if something in it
> is cheaper than what is already being worked.

**Report the FAIL in one of two grades. This is new, and it is the fix registered as D54.**

> **FAIL-ESTABLISHED** — you have positive evidence the clause fails (you read the definition and it
> is inconsistent; you found the finding that settled it; you computed the densities and none beats
> 232/2⁻¹⁴¹).
> **FAIL-UNEARNED** — the clause fails only because you could not establish it (file unreachable,
> findings not read, estimator unavailable).
>
> **Both block promotion**, so nothing is bought by hedging. But they are different facts and this
> project has until now recorded them identically — a replication showed two runs of one brief
> splitting on exactly that, both compliant. **Name the grade for every clause you fail.**

## 6. Budget — two numbers, because the last brief proved the wrong one was being capped

**Cap: 30 file reads or searches within the repositories.** No web access is needed; if you find
yourself wanting the literature, that is a signal you have drifted out of scope.

**And a context ceiling.** `Cooperative-AI-Defense/hadamard/findings/` holds 163+ documents and some are long. A previous
brief in this series stopped at 18 of 22 calls because *"further large PDFs risk swamping the
report"* — the cap counted calls while **context** was what actually ran out. So: prefer targeted
greps over whole-file reads, read `Cooperative-AI-Defense/hadamard/findings/OPEN_ORDERS.md` and `QUEUE_STATE` in full and nothing else in full
unless a question needs it, and **state at the end which of the two limits you stopped on.** That last
clause is the cheap part and turns an inference into a datum.

**A partial report is a success.** Q1 and Q2 answered with Q3–Q5 marked NOT REACHED is a complete,
useful run.

## 7. Rules that are not negotiable. Each cost this project something real.

1. **A bar you cannot evaluate is FAIL** — graded FAIL-UNEARNED per §5, not "unscored".
2. **Tier every claim.** `PRIMARY-VERIFIED-LOCALLY` (you computed it) / `SECONDARY-RELAYED` (you
   opened the file) / `RECALL`. **Reading a document that quotes a file is not reading the file** —
   that is exactly the error this brief exists to repair, and §1's table marks my own cells accordingly.
3. **A verified computation licenses only the claim it computes.** The last brief in this series
   shipped a locally-computed claim marked *"treat it as given"* that was the only false statement in
   it: a result about corner *deletion* was generalised to "no construction reaches this order", and a
   second operator, corner *addition*, made it false. **§2's relations are verified; §3's *b* reading
   is verified and refuted. Do not promote either beyond what it says.** Debt D53.
4. **Two quantities can share one name.** §3(ii) is an instance, live and unresolved.
5. **Necessary is not sufficient.** Admissibility permits; it does not populate. Q4.
6. **Derive counts; never type them twice.** If you state a count, say which command produced it.
7. **Do not guess to produce a tidy verdict.** *"I could not establish this"* is required when true.

## 8. Report anything that contradicts this brief. This clause has outperformed every bar here.

§1's provenance table, §2's construction assumption, §3's three arithmetic points and the classical
thirteen are all either relayed at two removes or `RECALL`. **If one is wrong that outranks the
verdict.** §3(i) is offered *pre-refuted* on purpose: I could not check it against the source, so
rather than ship a premise you might inherit, I shipped the guess together with its disproof.

**You are not expected to defer to this document.** The previous brief's most valuable finding came
from a run refusing a premise it had been told to treat as given.

## 9. What to return

A single document:

1. **The verdict line first**: `E: PASS` / `E: FAIL` — and **for each failed clause, its grade**
   (FAIL-ESTABLISHED or FAIL-UNEARNED).
2. **The bar quoted verbatim** from §5.
3. **Q1's answer first and in full**, since everything is conditional on it — including the verbatim
   definition of *b*.
4. **Q2–Q5**, one section each, every claim tiered, naming the file you actually opened. **A question
   you could not answer is named as unanswered, not dropped.**
5. **A finding-count line**: how many documents are in `Cooperative-AI-Defense/hadamard/findings/` now, against the 163
   `../PLAN_2092.md` saw. **And if any path this brief cites does not resolve, say which** — this project
   currently carries 90 broken cited paths it has not repaired (debt D52), and a brief that sends you
   to a file that moved is the most likely way for this run to waste its budget.
6. **Calls used against 30, and which limit you stopped on** — calls or context.
7. **Anything contradicting §§1–3.**

**Do not recommend what to do next.** The verdict and the evidence are the deliverable.
