# Brief E — the *b* ≥ 3 Hadamard region. Three solved instances sit inside it.

**For a Claude Code instance with read access to BOTH repositories.** The hard requirement is
`Cooperative-AI-Defense`, branch `claude/hadamard-matrix-methods-vs79hi`, directory
`Cooperative-AI-Defense/hadamard/findings/`. **Without that access this brief cannot be run** — say
so and stop; that is a clean answer and costs nothing.

**This is not a search and not a change to the live *v* = 523 work.** Five questions, all reads.

> **Revision note, and it matters for D44.** A first version of this brief was written and pushed
> before *b* was defined, with a bar whose clause (a) was *"obtain the definition of b."* The operator
> then supplied it. **This brief has not been dispatched**, so revising it now is a change to a
> pre-registration, not a re-scope after answers — the thing D44 forbids is redrawing a bar once a run
> has reported. The superseded reasoning is kept in §3 rather than deleted, because what it got wrong
> is instructive.

---

## 1. What *b* is, and the one consequence that reframes the whole entry

**`b` is a border width.** A bordered example is a border of width *b* around a core; **b must be
odd.** Of **Alpöge's 12 examples, 7 are bordered**; the majority of those are *b* = 1, with **one each
at *b* = 3, *b* = 5 and *b* = 7.** `OPERATOR-SUPPLIED` — authoritative, but *not* read from
`Cooperative-AI-Defense/hadamard/findings/OPEN_ORDERS.md`, so confirming it against the source is Q2.

That forces a decomposition of the 12, and it is self-consistent (asserted in `derive.py` §7):

| | count |
|---|---|
| unbordered | **5** |
| *b* = 1 | **4** — the majority of the 7 bordered, as stated |
| *b* = 3, 5, 7 | **3**, one each |
| total | **12** |

**Two consequences, and the second reverses the queue entry.**

1. ***b* odd means "*b* > 2" is "*b* ≥ 3".** There is no *b* = 2, 4 or 6 case; the region is
   *b* ∈ {3, 5, 7, 9, …}.
2. **The region is NOT unswept.** `../../fallbacks/QUEUE_V3.md` called it *"a writable, un-swept region
   inside the primary thread."* **Alpöge has one example at each of *b* = 3, 5 and 7** — the method the
   entire worklist is modelled on has already produced objects there.

**Consequence 2 is worse news than "virgin territory" and much better news than it sounds.** It
supplies the one thing the Costas cell fatally lacked: **genuine positive controls inside the region** —
solved instances, found by the method in question, at the exact parameter values in dispute. The Costas
attempt died because its apparent control at order 31 turned out to be constructible and therefore
never reached by search. **These three were reached.** That is why this brief is worth running and why
its first question is about them.

## 2. What I verified locally, so you can check me rather than believe me

`derive.py` in this directory, output `VERIFIED_OUTPUT.txt`, every assertion passing. Construction
assumed: *H* of order 4*v*, *d* an odd divisor of *v*−1, *r* = (*v*−1)/*d* + 1, *D* = (*r*−1)/2, row
sums *a_k* = ±1 + *d*(2*u* − (*r*−1)) with Σ*a_k*² = 4*v*.

* **All six rows of `../PLAN_2092.md` §1's table reproduce exactly**, admissible-*d* lists included:
  487 → [9,3,1], *r* = 55, *D* = 27; 523 → [9,3,1], 59, 29; 571 → [5,3,1], 115, 57; 643 → [3,1], 215,
  107; 659 → [7,1], 95, 47; 739 → [9,3,1], 83, 41.
* **`free_bits = 4(v−1)/d` exactly, on all six rows** — four bits per orbit, with (*v*−1)/*d* orbits.
  The table never states this and it is the cleanest form.
* **`density exponent = free_bits − log2 E[#sol]`** on all six to within 0.35.
* **So the worklist's entire difficulty ranking is a function of one arithmetic quantity**, the largest
  odd divisor of *v*−1 the row-sum law admits. Nothing about the search enters it.

**Two things in the queue entry that still do not survive arithmetic.**

* **"The 13 orders" names two different sets.** The repo's targets are orders 1948, 2092, 2284, 2572,
  2636, 2956; the classical thirteen smallest open orders are 668, 716, 892, 1004, 1132, 1244, 1388,
  1436, 1676, 1772, 1916, 1948, 1964 (**`RECALL` — checking this list is part of Q3**), whose *v* = *n*/4
  are all prime. **Only 1948 is in both.**
* **669 and 721 are ≡ 1 (mod 4), so neither is a Hadamard order.** They are *v* or *m* values giving
  **2676** and **2884**, and both are composite (669 = 3·223, 721 = 7·103) while every *v* on the
  worklist is prime. *Hypothesis:* never screened because the machinery assumes *v* prime. **Falsifier:**
  the repo screening a composite *v* anywhere.

**One lead, with its caveat.** *v* = 721 admits *d* = 15 → *r* = 49, *D* = 24, **192 free bits**: 24
fewer than *v* = 487, the order Alpöge **solved**, and 40 fewer than the live target. **Distrust it** —
free bits is one of two coordinates, density = free_bits − log2 E[#sol], and I cannot compute E[#sol]
without the repo's estimator. Whether 2884 is open is also unverified.

## 3. The reasoning that was wrong, kept because of what it shows

Before *b* was defined I took it to be a **block count** and derived, correctly for that object, that
every permitted *a_k* is odd, hence Σ*a_k*² ≡ *b* (mod 8) while 4*v* ≡ 4 (mod 8), hence **b ≡ 4
(mod 8)** — so of *b* = 2…29 only 4, 12, 20, 28 admit any of the thirteen, and *b* = 3, 5, 6, 8 admit
none. All of that is still true **about block counts**, and it is irrelevant, because *b* is a border
width. The first version of this brief shipped that derivation **together with its own refutation**
rather than as a premise, on the grounds that a source reporting pairs at *b* > 2 could not mean it.

**That was the right call and it is the reason this section exists.** The previous brief in this series
shipped a locally computed claim marked *"treat it as given"* that was the only false statement in the
document (debt **D53**). A verified computation licenses only the claim it computes. Here the
computation was sound and the *object* was wrong — a failure mode one step earlier than D53's, and one
no tier in this project's vocabulary marks.

**Which is why the hypothesis in §4 is labelled a hypothesis and given a one-number falsifier.**

## 4. The hypothesis the brief turns on, stated as a hypothesis

A border of width *b* removes rows and columns from the core, so the core is smaller and carries fewer
free parameters. **If free bits scale with the core rather than with *v*, then larger *b* is CHEAPER.**
That is a mechanism for why anyone would flag *b* > 2 as an opportunity — and it is the **reverse** of
what I guessed in the superseded version, where I supposed free bits grew with *b*.

> **FALSIFIER, one number per example:** the free-bit or density figure for Alpöge's *b* = 3, 5 and 7
> examples, against his *b* = 1 examples at comparable order. **If free bits fall as *b* rises, the
> region is cheaper and the queue entry is live. If they do not, it is not.**

I am not asserting the scaling. §3 is what happens when I assert one.

**And a consistency observation on the 126+ figure, not a derivation.** Thirteen orders × odd *b* from
3 gives 13 pairs per value of *b*; reaching 126 needs *b* running to about **21** (10 values, 130
pairs), with a few inadmissible. So the source's number is consistent with an upper bound on *b* near
21. **I do not know the admissibility condition for a bordered core and cannot compute the real count** —
what this gives you is a shape to check the source's number against, and a specific question in Q3.

## 5. The five questions, in priority order

**Q1. Alpöge's three *b* > 2 examples — the whole brief turns on this.** Which orders are they at? What
*b*, what core order, what free-bit and density figures? And the same for his *b* = 1 examples, so the
comparison in §4 can be made. **These are the only solved instances inside the region and they are the
positive control this project has never had on this route.** If the findings give a cost figure for
them, that single table answers §4's falsifier.

**Q2. Confirm the definition against the source, and get the admissibility condition.** Quote
`Cooperative-AI-Defense/hadamard/findings/OPEN_ORDERS.md` on what *b* is and what makes a (*v*, *b*)
pair **admissible**, verbatim. Is there an upper bound on *b*, and is it near 21 (§4)?

**Q3. Is the region still unscreened — and was it ever?** `../PLAN_2092.md` read ~15 of **163** findings
and is dated. **How many findings exist now, and has any screened, settled, entered or abandoned
*b* ≥ 3?** Also: **was `FINDING_155`'s ranking scoped to a single *b*?** If it ranked across *b*, the
region is already ranked and nothing was unswept. **This decides whether the queue entry was ever
real.** And resolve §2's two-thirteens ambiguity, and whether 126+ is computed or typed.

**Q4. Are the admissible pairs non-empty, and has anyone tested?** An admissible (*v*, *b*) pair is a
**necessary condition on parameters, not evidence an object exists there.** `FINDING_133` reportedly
found the orbit-reduction route's failures at *m* = 82 to be *"emptiness rather than solver weakness"*.
Apply that to *b* ≥ 3. **126 admissible-but-empty pairs are worth nothing** — and note that Alpöge's
three examples prove the region is *not* uniformly empty, which is a real asymmetry with the Costas
case.

**Q5. 669, 721, and the lead.** What are they — *v*, *m*, or something else? Is 4·721 = 2884 open? Does
721's 192 free bits survive a density calculation with the repo's estimator, and what is the exponent
against the live target's 2⁻¹⁴¹?

## 6. The bar. Revised before dispatch (see the revision note); you may not re-scope it after.

> **PASS iff all three hold:**
> **(a)** the source confirms *b* is a border width with *b* odd, and the findings that cite it use it
> consistently; **and**
> **(b)** no finding written since `../PLAN_2092.md` has screened, settled, entered or abandoned the
> *b* ≥ 3 region, **and** `FINDING_155`'s ranking was scoped to a single *b* rather than across *b*;
> **and**
> **(c)** a free-bit or density figure is obtained for at least one of Alpöge's *b* = 3, 5, 7 examples,
> **and** it is better than his *b* = 1 examples at comparable order **or** better than the live
> target's 232 free bits / 2⁻¹⁴¹.
>
> **FAIL on any one.** Clause (c) is the decision: a region is worth entering only if something in it
> is cheaper than what is already being worked, and Alpöge's three examples are the only place a
> figure for it can come from.

**Report each failed clause in one of two grades — this is the fix registered as D54.**

> **FAIL-ESTABLISHED** — positive evidence the clause fails (you read the definition and it is
> inconsistent; you found the finding that settled it; you got the figures and none beats *b* = 1).
> **FAIL-UNEARNED** — it fails only because you could not establish it (file unreachable, findings
> unread, estimator unavailable).
>
> **Both block promotion**, so hedging buys nothing. But they are different facts and this project has
> until now recorded them identically — a replication showed two runs of one brief splitting on exactly
> that, both compliant. **Name the grade for every clause you fail.**

## 7. Budget — two numbers, because the last brief proved the wrong one was capped

**Cap: 30 file reads or searches within the repositories.** No web access is needed; wanting the
literature is a signal you have drifted out of scope.

**And a context ceiling.** `Cooperative-AI-Defense/hadamard/findings/` holds 163+ documents, some long.
A previous brief stopped at 18 of 22 calls because *"further large PDFs risk swamping the report"* — the
cap counted calls while **context** ran out. Prefer targeted greps to whole-file reads; read
`Cooperative-AI-Defense/hadamard/findings/OPEN_ORDERS.md` and `QUEUE_STATE` in full and little else; **state which of the two limits you stopped
on.** That clause is cheap and turns an inference into a datum.

**A partial report is a success.** Q1 and Q3 answered with the rest NOT REACHED is a complete run.

## 8. Rules that are not negotiable. Each cost this project something real.

1. **A bar you cannot evaluate is FAIL** — graded FAIL-UNEARNED per §6, never "unscored".
2. **Tier every claim.** `PRIMARY-VERIFIED-LOCALLY` / `SECONDARY-RELAYED` (you opened the file) /
   `OPERATOR-SUPPLIED` / `RECALL`. **Reading a document that quotes a file is not reading the file** —
   that error is why this brief exists, and §1's *b* definition is `OPERATOR-SUPPLIED`, not sourced.
3. **A verified computation licenses only the claim it computes — and check what object it is about.**
   §3 is a worked instance of the second half, which is one step earlier than D53's failure and which
   no tier here marks.
4. **Necessary is not sufficient.** Admissibility permits; it does not populate. Q4.
5. **Two quantities can share one name.** §2's two thirteens, live and unresolved.
6. **Derive counts; never type them twice.** Say which command produced any count you state.
7. **Do not guess to produce a tidy verdict.** *"I could not establish this"* is required when true.

## 9. Report anything that contradicts this brief

§1's decomposition of the 12 is forced by an operator statement, not read from the source. §2's
construction, the classical thirteen, and §4's consistency observation are `RECALL` or relayed at two
removes. **If one is wrong that outranks the verdict.** §3 is included *already refuted*, on purpose.

**You are not expected to defer to this document.** The previous brief's most valuable finding came from
a run refusing a premise it had been told to treat as given, and the version of this brief that
preceded yours was wrong about the central term.

## 10. What to return

1. **The verdict line first**: `E: PASS` / `E: FAIL`, and **for each failed clause its grade**.
2. **The bar quoted verbatim** from §6.
3. **Q1 first and in full** — the table of Alpöge's bordered examples with *b*, order, core order, and
   cost figures, since §4's falsifier lives there.
4. **Q2–Q5**, one section each, every claim tiered, naming the file you opened. **A question you could
   not answer is named unanswered, not dropped.**
5. **A finding count**: how many documents are in `Cooperative-AI-Defense/hadamard/findings/` now,
   against the 163 `../PLAN_2092.md` saw. **And if any path this brief cites does not resolve, say
   which** — this project carries 89 broken cited paths it has not repaired (debt **D52**), and a brief
   sending you to a moved file is the likeliest way to waste your budget.
6. **Calls used against 30, and which limit you stopped on** — calls or context.
7. **Anything contradicting §§1–4.**

**Do not recommend what to do next.** The verdict and the evidence are the deliverable.
