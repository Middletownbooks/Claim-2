# Arm AJ — census of the VibeMathed corpus

**Data.** `src/data/problems.json` from `mrconter1/vibemathed`, pinned at commit `982830e`
(clone dated 2026-09-15). MIT code; the classifications, scores and notes are **CC BY 4.0,
VibeMathed**, operated by Rasmus Lindahl as a non-commercial personal project. Reproduce with
`analyze_vibemathed.py`; full output in `census_output.txt`.

**Scope and its limit.** 664 entries, `solveDate` 2025-07-20 .. 2026-09-03. **The repo
snapshot lags the live site**: the union-closed ceiling result audited in arm AI
(`solveDate` 2026-09-08) is *not* in this file. So every number below is a lower bound on the
live corpus, and the site's DB is the authority. `/api/dataset` is blocked from here; the
GitHub lane is not, which is how this arm exists at all.

**The corpus's own inclusion rule, which is the most important fact about it.** A result
appears "only if its authors said what the model did." This is a census of **disclosed** AI
contribution, not of AI contribution. Every growth curve below therefore confounds two
things — how much AI is doing, and how willing authors are to say so — and the site states
this itself rather than letting a reader assume otherwise.

---

## 1. The finding: the corpus is growing far faster than the checking

| | n | share |
|---|---:|---:|
| **Never seen by a named human expert** | **651** | **98.0%** |
| Not peer reviewed | 662 | 99.7% |
| `unreviewed` | 418 | 63.0% |
| `lean-checked` (compiles, **statement unaudited**) | 30 | 4.5% |
| Any Lean tier | 167 | 25.2% |
| Retracted after audit | 3 | 0.5% |

Two peer-reviewed entries out of 664. Thirteen expert-verified. **Formal verification is not
supplementing peer review in this corpus; it is substituting for it** — a quarter of entries
carry a Lean tier, which is eight times the rate of any human check.

And the verified share is **falling as volume rises**:

| month | n | Lean % | unreviewed % |
|---|---:|---:|---:|
| 2026-01 | 13 | 76.9% | 15.4% |
| 2026-03 | 24 | 41.7% | 45.8% |
| 2026-05 | 67 | 20.9% | 64.2% |
| 2026-07 | 223 | 22.9% | 69.1% |
| 2026-09 (part) | 14 | 14.3% | 71.4% |

Seventeen-fold growth in monthly volume against a Lean share that fell from 77% to ~20%.
**The audit backlog is growing monotonically, and nothing in the trend bends it.** That is
this programme's opening stated as a measurement rather than a hunch.

## 2. Checking is inversely related to significance

| tier | n | median sig | max |
|---|---:|---:|---:|
| `unreviewed` | 418 | **15.0** | 65 |
| `expert-verified` | 13 | 15.0 | 65 |
| `lean-checked` | 30 | 12.0 | **68** |
| `lean-verified` | 137 | **10.0** | 60 |
| `site-confirmed` | 64 | 10.0 | 60 |

**Lean-verified entries score *lower* than unreviewed ones.** The plain reading: what gets
formalised is what *can* be formalised — small, self-contained, mechanically tractable. The
larger claims are the ones nobody has checked. Of the 89 entries at significance ≥ 30,
**64 (71.9%) are `unreviewed` or `lean-checked`.**

This is the opposite of reassuring, and it is the single most useful number in the arm.

**The top of the corpus is in the unaudited tier.** The highest-significance entry of all 664
— *The Proportion of Zeta Zeros on the Critical Line*, sig **68**, the Hardy–Selberg–Levinson–
Conrey ladder, `ai-discovered`, model "Claude (unreleased research version)" (Anthropic),
human collaborators including Levent Alpöge, arXiv:2608.13637 — is `lean-checked`: sorry-free
Lean 4 against Mathlib's own `riemannZeta`, with the statement audit incomplete. Three of the
top ten are `lean-checked` and two more are `unreviewed`.

## 3. The three known-bad entries validate audit as an instrument

All three were caught by **audit**, not by review or by publication:

- **Erdős #7** — a claimed Lean proof that no such covering system exists, *withdrawn after
  audit*: **its central axiom asserted that a product of factors greater than one is less
  than one.** A false axiom inside a formalisation.
- **Erdős #684** — "a deterministic audit later found a counterexample to its key Lemma 18."
  The stated conclusion is not established.
- **Cyclic number conjectures** — the paper was retracted from arXiv.

**This retrospectively justifies the check I ran in arm AI.** I verified `moffatstudio`'s
axiom whitelist (`propext`, `Classical.choice`, `Quot.sound`, nothing else) and looked for
`native_decide` and user-declared axioms. Erdős #7 is exactly that failure mode, realised.
A `lean-verified` badge means the artifact compiles; it does not mean the axioms are sound or
the statement is the intended one. **The axiom check is not pedantry — it is the check that
has already caught a real failure in this corpus.**

## 4. What kind of mathematics this is

- **Old problems, not fresh ones.** Median age at solution **28.5 years**; 38.4% of the
  datable entries had been open 26 years or more; max 177. This is backlog clearance.
- **Modest individually.** Significance median 15, **max 68** — nothing claimed at
  Millennium level. 55% sit in [10,20).
- **Fields:** Combinatorics 177, Number theory 134, Analysis 74, Geometry & topology 65.
- **Method:** argument 392, construction 234, computation 38. Computation is the *rarest*
  route, which is worth remembering against my repeated instinct to look for finite checks.

**This is the cheap-but-real class, and it is where the mass is.** Exactly the profile arm AI
found at the union-closed ceiling: significance 18, headroom closed 1.8·10⁻⁴, genuine.

## 5. Vendor and model composition

OpenAI-made models dominate (329 entries name OpenAI alone). **Anthropic models appear in
138 entries (20.8%); a Fable model is named in 79 (11.9%).** A cross-vendor referee pattern
is visible in the data — 13 entries are "GPT-5.6 starships (Claude Fable 5 reviewer)", 4 are
"GPT-5.6 Star Fleet (Claude Fable 5 referee)".

**RETRACTED — the contamination claim in this section.** I wrote that Fable-family models
are "a major producer across this whole corpus" and that therefore every Fable-named entry
should be "treated as non-independent until someone outside decides otherwise." That is
wrong, and the user's analogy is the refutation: a third of the races were won by Ferraris,
and they once rode in a Ferrari Uber. **I conflated a shared model family with a shared
information channel.** Contamination requires a channel — information flowing between this
programme and the thing being measured. A commercial model used independently by two
unconnected parties is not a channel; it is a mass-produced tool. Moffat's campaign and this
programme share no data, no prompts and no people. There is nothing to control for.

This is the same defect as the rank-429 badge, pointed the other way: a surface token (there
a status label, here a model name) treated as evidence of underlying structure, with no check
for whether a mechanism exists. Being over-cautious rather than over-confident does not make
it a different error.

### The real independence axis is the training cutoff, and it is computable

Worrying about the model name obscured the variable that actually matters. For a prospective
arm the question is *whether the answer is already in my context* — and that is a **date**,
not a name.

| filter | excludes | mechanism? |
|---|---:|---|
| Fable-named (what I proposed) | 79 (11.9%) | **none — withdrawn** |
| `solveDate` ≤ 2026-05 (assistant knowledge cutoff) | 188 (28.3%) | training data |

**476 of 664 entries (71.7%) post-date the cutoff and are clean on this axis.** Within that
clean set the audit queue is 327 `unreviewed` and 22 `lean-checked`, and **55 entries sit at
significance ≥ 30 while unreviewed or statement-unaudited**, including every one of the
targets named in §2:

| sig | tier | solved | entry |
|---:|---|---|---|
| 68 | `lean-checked` | 2026-08-10 | Zeta zeros on the line |
| 65 | `unreviewed` | 2026-08-24 | A Complex Structure on S⁶ |
| 62 | `lean-checked` | 2026-09-03 | Prime gaps at most 212 |
| 62 | `unreviewed` | 2026-09-01 | Prime gaps at most 236 |
| 55 | `lean-checked` | 2026-08-19 | Carathéodory conjecture (smooth) |
| 55 | `unreviewed` | 2026-08-17 | Matrix multiplication exponent |

So the bad filter would have thrown away 79 usable entries for no reason, and the good filter
both *keeps* the whole target list and tells me exactly which 188 entries I must not treat as
prospective. **Use the date. Retire the model-name control.**

---

## 6. What this changes

1. **The instrument question is settled.** ProofAtlas indexes problems; VibeMathed indexes
   *AI contributions with verification status, model, vendor, method and a significance
   score* — this programme's actual variables, CC BY 4.0, with a public changelog and
   per-entry discussion. Arm AG's ProofAtlas work stands as a negative result about the
   wrong instrument.
2. **The audit queue is now enumerable, not conjectural.** 30 `lean-checked` entries are
   compiled-but-statement-unaudited by the site's own label; 418 are `unreviewed`; 64 of the
   89 high-significance entries are in one of those two buckets. Arm AI worked one of them
   end to end, so the cost is known.
3. **Audit is the validated move.** Three known-bad entries, all found by audit, one of them
   a false axiom in a Lean development. That is the empirical case for the thing this
   programme is good at, and it did not exist before this arm.
4. **Governance is thin, and that is not a criticism so much as a measurement.** One
   operator, volunteer moderators, one of whom is a physics PhD candidate in quantum error
   correction. The union-closed entry is extremal set theory. Its own label — "not peer
   reviewed and not checked by a named expert" — is accurate and the site says so plainly.
   **The honesty of the labelling is what makes the corpus usable.**

## 7. Next

- **Pull `/api/dataset` live** when reachable, to get past the 2026-09-03 snapshot.
- **Zeta zeros (sig 68) is done — see `leanboard/ak/`.** 33/33 on the arithmetic, clean at
  source level, and the textual half of the missing statement audit completed (15/15
  statements and 9/9 counting functions identical). Only the kernel re-run remains. The arm
  also found that this census's praise of the site's labelling needs one qualification: the
  site's source audit of that entry quotes a **superseded** `sorry` count from the
  repository's own `AUDIT.md` (27, pre-XiPrime) where the true figure at the audited tag is
  33. Conclusion sound, number inherited rather than recomputed.
- **The barrier predicate is retired, refuted by that same arm.** The zeta paper doubles a
  fifty-year record *and* proves its own method's ceiling, landing within 0.0152 of it. It
  was selected as the top of the audit queue, not for declaring a barrier — so it is the
  neutral control this section asked for, and it fires the predicate on the least exhausted
  board in the corpus. Barrier language indicates rigour, not exhaustion.
- **The two large-gap entries (sig 60 each) are done — see `leanboard/al/`.** The record
  ladder Rankin → FGKMT → Sol → Astra checks exactly, 14/14, as monomials in
  `log X, log₂X, log₃X, log₄X`; both Lean statements say what their papers say; neither
  development has a gap token. The arm's structural finding sharpens this census: the two
  results have **disjoint** verification halves — Sol has Ben Green's reading but no build,
  Astra has the kernel replay but no reader — and the *stronger* bound is the unread one.
  Same problem, nine days apart, allocation still backwards.
- **`Prime Gaps at Most 186` is done — see `leanboard/am/`.** 22/22, including a *complete*
  finite check of the explicit admissible 40-tuple (40 elements, diameter exactly 186,
  admissible at every prime). The three axioms assessed individually: one is Deligne's
  hyper-Kloosterman bound exactly, one asserts square-root cancellation a factor ~`√p/2` past
  the trivial bound uniformly over all pairs, and one is a package of **152 scalar numerical
  bounds** on 39-/40-dimensional integrals with no literature to check it against. My count
  independently reproduces the site's "104 outer, 45 inner, 3 cap".
- **`lean-checked` is not one condition — it is at least four.** Four artifacts audited now
  stop in four different places: statement fidelity (zeta), no human reader (LongGaps), a
  patched external dependency (Erdős 4), and the axioms themselves (PrimeGaps186). Only the
  last is visible from an axiom listing. **This census's single `lean-checked` bucket hides
  that distinction**, and §4 of arm AM tabulates it.
- **Cycle Double Cover (sig 55) is done — see `leanboard/an/`.** `openai/cdc-lean` is clean at
  source with **no project axioms at all**, and its three custom definitions (`Cycle`,
  `Bridgeless`, `CycleDoubleCover`) were brute-forced against their textbook meanings over
  4,860 small multigraphs with **zero mismatches** — `Cycle` really is a graphic-matroid
  circuit, not the weaker "even subgraph". The sibling paper's construction was implemented and
  produces valid covers on Petersen, Blanuša and flower snarks J₅/J₇/J₉. **The one scope
  finding: the theorem is the *loopless* case**, since `loopless` is a structure field, and the
  loop reduction — trivial but real — is not formalized. Both README and VERIFICATION.md
  disclose this; the site's entry does not.
- **Next on the queue:** Carathéodory smooth (sig 55), then the remaining `lean-checked` entries.
- **The control class is no longer outstanding.** Arm AK supplied it by accident and it went
  against the hypothesis. No further sampling pass is needed for that question.
