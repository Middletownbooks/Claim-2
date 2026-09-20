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

## Prediction, and how to falsify it

An artifact carrying features 1–4 is verifiable at roughly the cost of reading it; one
lacking them absorbs an arm and leaves the core untouched, **whatever its check count**.

Falsified by: an artifact with all four whose core an auditor still cannot reach, or one with
none that verifies end to end.

**n = 3. This is a taxonomy, not a rate.** The way to make it a rate is more process
artifacts, which remain the highest-value input this programme can receive — and which the
corpora do not carry.
