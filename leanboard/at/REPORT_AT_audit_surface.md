# Arm AT — the audit surface: which process choices decide what an auditor can verify

**Question.** Not which prompt is better in the abstract. Which process choices produced an
artifact whose **load-bearing claims** an outside auditor could check, and which produced one
where only the scaffolding was reachable.

**Why now.** This programme has audited 664-entry corpora of *outcomes* and almost no
*processes*. Three process artifacts are now on the record, and I audited all three myself,
so the scores below are this programme's own results rather than self-report.

| | artifact | checks | load-bearing claims verified | cost to me |
|---|---|---|---|---|
| **N** | Nevanlinna half-plane (arm AQ) | 22/22 | **0 of 4** | one long arm; core never reached |
| **P** | Allikvere preprint (arm AS.3) | 20/20 | **5 of 5** | one sitting, end to end |
| **L** | LaTeX to the author (arm AS.1) | 25/25 | **4 of 4** | one sitting, end to end |

**The first thing this says is about my own instrument.** N scores 22/22 and reached 0% of
its core. A passing check count is not a verification result; it is a statement about what
was checkable. Every tier I have used in this programme — `lean-checked`, `site-confirmed`,
`unreviewed` — grades the artifact. None grades the *audit surface*, which is what actually
determined whether I could reach anything.

## Process features against outcome

| feature | N | P | L |
|---|---|---|---|
| deliverable is a finite object | · | **Y** | **Y** |
| separately written checker | · | **Y** | **Y** |
| control returning a known negative | · | **Y** | **Y** |
| hand-checkable proof independent of the machine work | · | **Y** | **Y** |
| reproducibility package shipped | · | Y | · |
| machine-checked proof *steps* | · | Y | · |
| independent third party audited the encoding | · | · | Y |
| literature placement requested | Y | Y | · |
| **confidence self-assessment** | · | · | · |
| **budget / stopping rule** | · | · | · |
| **formalization** | · | · | · |
| **negative space ("which steps are least secure?")** | · | · | · |

Four features separate the two outcomes cleanly. **And the four gaps I named in the
Nevanlinna prompt translation turn out to be universal** — absent from all three artifacts,
including the two that verified perfectly. They are not what made the difference here.

## The confound, stated before the conclusion

A finite combinatorial object is inherently more checkable than a complex-analysis
construction. Cusp reflection is not a matrix. **Part of the spread is subject matter, not
process, and a three-case comparison cannot separate them.** Three of the four separating
features are partly downstream of the mathematics.

What survives is narrower, and is the finding.

## The control is the feature that transfers

Running the apparatus on a case whose answer is already known, and checking it returns that
answer, needs only a search procedure. It is available in **every** domain.

- **L:** *"the same encoder returns UNSAT at n = 3 with a machine-checked proof, agreeing
  with the verification reported in the paper."* The instrument is tested against Chow's own
  published result.
- **P:** two separately written programs enumerate all 2304 ordered partitions; the lifts are
  re-verified for all 10 and all 20 attachment triples *"in agreement with the lemma."* The
  instrument is tested against its own theorem.
- **N:** no control anywhere in 7 h 14 min and ~1.02M tokens.

**This matters most for N, not least, because its prompt forbids the negative answer.**
*"No counterexample was found"* is a banned output. A search that cannot report failure, and
is never run on a case where it should fail, has no calibration at all. One instruction would
have supplied it.

That is the sharpest thing in this arm: the most elaborate prompt of the three — eleven named
search modes, an adversarial agent assigned to kill each candidate, a three-part exit
condition — omitted the cheapest and most transferable check, and its own output ban is what
made the omission dangerous.

## Specification

1. **Deliver a finite object wherever the problem admits one.** A certificate an auditor can
   rebuild beats an argument they must trust.
2. **Write the checker separately from the finder.** Both verified artifacts did; one used
   two independently written enumerators.
3. **Run a control on a case with a known answer, and report it.** Domain-independent, and
   most valuable exactly when the prompt bans the negative answer.
4. **Produce a proof that stands without the machine work.** *"The argument in Section 4 is
   independent of all of this and can be checked by hand"* is why arm AS closed in one sitting.
5. **Ask which steps are least secure.** Absent from all three. In arm AQ it would have named
   cusp reflection — where the audit stalled, and where an error would hide.
6. **Ask for literature placement, and act on the answer.** N and P did. L did not, and omits
   Harvey–Király–Lau 2011, leaving a reader unable to tell the result sits in the open range
   `b > n/3` — which it does.

## Part 2 — the CDC prompt tests the prediction, and it holds

A fourth process artifact arrived after part 1 was written: the full prompt OpenAI gave
GPT-5.6 Sol Ultra for the Cycle Double Cover Conjecture. Its output was audited here in arm
AN, so the loop is closed the same way — prompt on record, artifact audited by this
programme. `cdc_prompt_comparison.py`, 7/7.

**This is the best available test, because at the search stage the CDC prompt is by far the
most elaborate of the four.** Six mechanisms have no counterpart in the Nevanlinna prompt:

1. **Definitions pinned in the prompt** — *"A cycle is a connected 2-regular submultigraph;
   thus two parallel edges form a cycle of length two."*
2. **An insufficiency list**, seven named near-misses that do not count.
3. **A domain-specific adversarial checklist**, seven named failure modes: exact-two
   multiplicity, repeated-edge closed trails masquerading as cycles, parallel-edge 2-cycles,
   disconnected graphs, cutvertices, bridges introduced by reductions, circular use of an
   equivalent CDC statement.
4. **An anti-circularity guard** — *"A route that ends at a lemma equivalent in strength to
   the original conjecture is not close to completion."*
5. **An approach registry** with forced redistribution away from crowded families.
6. **Output-form requirements** — concrete lemmas or constructions only; status reports and
   "routine" claims rejected.

It shares with Nevanlinna: presumed existence, multi-agent independence, adversarial agents,
and **the ban on the negative answer** (*"do not answer that it is open"*). Neither prompt
has an upper bound on effort; CDC states a **floor** (*"at least 8 hours"*).

### Scored on the part-1 specification

| | CDC |
|---|---|
| 1 finite object as deliverable | **no** — a universal statement admits none |
| 2 separately written checker | partial — adversarial agents inside the same run |
| 3 **control returning a known negative** | **no** — "computational sanity checks" is one portfolio item, never required |
| 4 proof standing without machine work | formally yes; arm AN found the surface is 4,880 lines of Lean with no external reference |
| 5 which steps are least secure | **substituted** — the prompter supplies the failure modes rather than asking. Better when the prompter knows the domain; cannot surface one they did not anticipate |
| 6 literature placement | **forbidden** |

### The result

Arm AN: 9/9 properties across 15 graphs, 4,860 multigraphs with zero definitional mismatches
— and its own verdict, *"I verified its local lemmas by hand and its output by computation on
15 graphs; neither is a proof."* **CDC lands with N: high check count, core unreached.** The
prediction holds on the fourth artifact.

### The finding this forces

**Search-stage rigour and audit-stage rigour are different investments, and this set shows no
trade between them.**

| | search stage | output stage | core reached |
|---|---|---|---|
| N | elaborate | nothing | **0%** |
| **CDC** | **the most elaborate of the four** | nothing | **0%** |
| P | modest | four cheap features | **100%** |
| L | modest | four cheap features | **100%** |

The CDC prompt is the strongest counterexample available to the idea that a better search
prompt yields a more checkable result. Six mechanisms N lacks entirely, and the artifact is
exactly as unreachable as the one with none of them.

**What the search-stage work did buy should be credited precisely.** Arm AN found *zero*
mismatches between `minimal_even` and `connected_2regular` across 4,860 multigraphs. Pinning
the definitions in the prompt closed the statement-fidelity surface that arm AK found **open**
on the zeta paper. That is a real return — on **correctness of the target**, not on
**checkability of the result**. The two are separable and this set separates them.

### An unresolved tension, linking back to arm AR

CDC forbids the search that would reveal concurrent work: *"do not search the public web
merely to determine whether CDC is open."* The purpose is benchmark hygiene and it is
legitimate. The side effect is that the run cannot detect anyone else on the problem —
Kintali's paper appeared three days after the 10 July announcement, citing it.

The Nevanlinna prompt takes the opposite stance — *"If you find that my result is already
covered by the literature, tell me"* — and that single instruction is the only thing in any
of the four prompts that could surface a collision.

**Contamination control and priority awareness want opposite instructions, and none of the
four prompts resolves it.**

## Prediction, and how to falsify it

An artifact carrying features 1–4 is verifiable at roughly the cost of reading it; one
lacking them absorbs an arm and leaves the core untouched, **whatever its check count**.

Falsified by: an artifact with all four whose core an auditor still cannot reach, or one with
none that verifies end to end.

**n = 4. This is a taxonomy, not a rate.** The way to make it a rate is more process
artifacts, which remain the highest-value input this programme can receive — and which the
corpora do not carry.
