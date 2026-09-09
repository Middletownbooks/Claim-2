# The template as a document — structural analysis

Independent of the agent experiment. Counts are of the template text as supplied.

## What it is

A ~2,000-word research-orchestration protocol with seven sections. Its
distinctive content is a **failure taxonomy** — roughly 30 named ways an
argument can be wrong — plus a three-valued return condition that forbids
anything between "complete proof" and "labelled failure".

## The single best idea in it

> SCOPE CHECK: the proof mechanism is applied, as a sanity test, to a nearby or
> structurally analogous statement with a KNOWN false, weaker, or tight answer.
> If the mechanism does not visibly break or weaken exactly where it should,
> treat this as evidence of an error, not of extra strength.

This is a *positive control on the instrument*, and it is the item with the
strongest independent support in this programme. Phase Q's Euler→Navier-Stokes
calibration was exactly this move and it was the measurement that made the
FLT↔NS null interpretable; without it the null meant nothing. Phase T's
wrong-domain arm was the same idea again. Of everything in the template, this
is the item I would keep if forced to keep one.

## Second best: the three-valued return

Forcing (a) proof / (b) counterexample / (c) labelled failure, with an explicit
ban on the space between, converts a continuous confidence judgement into a
discrete auditable choice. Phase P's "RESULT A / B / C" framing did the same
work and was the reason that phase could report a clean negative rather than a
hedge.

## Redundancy: the ICC example appears five times

The centre-rules-out-ICC example recurs in DECOMPOSITION, twice in TARGET AND
NON-TARGETS, in DERIVATION DISCIPLINE, and in ADVERSARIAL AUDIT
(STRUCTURAL/RECIPE INCOMPATIBILITY and FIXED/FORCED-ELEMENT CHECK). The
fixed-point/free-action example appears four times.

This is the signature of a document grown by accretion around one painful
incident. It carries a specific risk: an agent may learn to pattern-match *the
named examples* rather than the general principle. That is why the experiment
here deliberately uses a counting obstruction the template never names — using
a centre/ICC trap would have measured recall, not protocol.

## The structural gap: it is a taxonomy of COMMISSION, not OMISSION

Every one of the ~30 checks asks *is what you wrote correct?* Not one asks
*what is missing from the registry?*

| failure class | covered? |
|---|---|
| a step is wrong | extensively |
| a step is unjustified ("by symmetry", "optimizing appropriately") | extensively |
| a conjunct is asserted rather than proved | extensively |
| a mechanism is applied outside its range | yes (SCOPE CHECK) |
| **the registry omits an entire approach family** | **no** |
| **the evidence base sampled is unrepresentative** | **no** |
| **the metric measures something other than what it names** | **no** |

The last two are not hypothetical. In this programme:

* **Phase S's architecture metric** was 54% driven by the rate of the tactic
  `have`. Every individual computation in it was correct. It measured
  boilerplate and was named "architecture". No item in the template's checklist
  catches a correctly-computed metric that measures the wrong thing.
* **Phase U's forecast ledger** drew from four pre-registration documents while
  claiming to transcribe ten. Every transcribed entry was accurate. The
  conclusion reversed (Fisher p = 1.0000 → p = 0.0389) when the missing six were
  added. The template's DECOMPOSITION and gap-ledger machinery would not have
  fired: there was no gap in the argument, only a hole in the sample.

A protocol that verifies each entry but never asks whether the entry set is
complete is vulnerable to exactly this. The cheapest fix is one line in the
audit checklist, in the template's own register:

> **COVERAGE / SAMPLING CHECK**: state the enumeration rule by which the
> registry, evidence set, or case list was populated, and have an auditor who
> did not populate it re-run that rule independently and diff the result. A
> registry whose population rule is "the ones I found" is not a registry.

## Rules that require infrastructure the prompt cannot supply

The ORCHESTRATION and ADVERSARIAL AUDIT sections assume a substrate:

| rule | self-executing in a prompt? |
|---|---|
| "audited by agents who did not contribute to it" | **no** — a single agent can only roleplay this |
| "this check must be performed by an auditor who did not write the detailed case argument" | **no** |
| "preserve independence: do not disclose the favored approach" | **no** — needs a coordinator withholding state |
| "if more than [K] agents converge, forcibly reassign" | **no** — needs a scheduler |
| "mandatory checkpoints every [T/8]" | **no** — needs a budget meter |
| SCOPE CHECK, DERIVATION DISCIPLINE (a)+(b), conjunct enumeration, three-valued return | **yes** |

The template does not distinguish these two classes, and the distinction is the
most practically important thing about it: **its highest-value clause
(independent audit) is precisely the one a prompt cannot enforce.** In this
programme the only clean instance of that clause working was Phase U §8, where
the audit was a genuinely separate agent with a different task — and it
overturned the coordinator's headline. That is an argument for the clause and
against expecting a prompt to deliver it.

## Smaller defects

* **No provision for the problem already being solved.** "Do not consult any
  source for the status, history, or attempted solutions" prevents anchoring but
  also guarantees that a solved problem consumes the entire budget. A carve-out
  — check solved-status once, at the start, and return immediately if solved —
  costs nothing and is not present.
* **`[PROOF ASSISTANT]` has no fallback.** "A proof that resists formalization
  at any step returns that step to the gap ledger" is unreachable when no
  assistant is available, as has been the case throughout this programme
  (`elan` egress-blocked). The template should name what substitutes.
* **"Budget: [T] of compute time"** is unmeasurable by an agent that cannot see
  its own consumption.
* **The disproof track is asserted but unresourced.** "Maintain both a proof
  track and a disproof track" appears once and gets no share of `[N]` in the
  orchestration rules.
