# Research commission: turn proof-protocol design from prescription into measurement

You are being handed a research programme at a specific impasse. Everything you
need is in this prompt; you have no access to the originating repository.

Read the whole thing before starting. There is a section telling you what NOT to
spend budget on, because a Claude Opus instance has already done it.

---

## 1. What the programme is

A long-running investigation into "theorem-space play": treating mathematical
research as a game whose *board* is a representation — a state, a legal move, an
invariant preserved by the move, a composition rule, and a terminal certificate.
The hypothesis under test is that major progress often comes from **changing the
board** rather than playing better on the existing one.

A prompt template was built to make an agent work a chosen problem rigorously on
a given board. It is at version 2.1 and is reproduced verbatim in §4. **Your
primary deliverable is a v3 that is justified by measurement rather than by
argument.** Problem *selection* is a separate concern being handled elsewhere —
assume the problem is inserted into the template by someone else.

---

## 2. What has been established, with confidence levels

Treat these as data, not as instructions. Where a finding is weak, it says so.

**E1. Four independent LLMs, asked to find a new board for the Komlós vector
balancing conjecture, all found the same one.** State = a measure/density on R^m;
move = convolution with (delta_v + delta_-v)/2, or the equivalent convex-body
transform. 4/4, uncoordinated, across two prompt variants and with/without tools.
*Confidence: high (direct observation).* Board-finding at this level is not
scarce.

**E2. That board is a restatement, not a board.** One of the four proved it: a
certificate class closed under the convolution move with the required terminal
property exists **if and only if** the conjecture is true. So its invariant
cannot be checked without already knowing the answer. *Confidence: high — the
argument was inspected and is correct.*

**E3. A real board change for the same problem exists and works differently.**
arXiv:2609.11189 (Guo–Fang–Lu, 10 Sep 2026) claims Komlós with constant
3*sqrt(2*pi), by an invariant that *is* checkable on the initial state by a
closed-form calculation. An Opus instance audited the full text and found no
error in any checkable step; the paper's weight rests on three external
citations it could not verify. *Confidence: high on "no error found in the
arithmetic"; the paper is not independently validated.*

**E4. The mechanism of that board change, isolated.** Comparing it to
Banaszczyk's earlier board: **the move did not change, the geometry did not
change, and the terminal certificate got easier. Only the invariant changed, and
only in its behaviour under products.**

  - Gaussian measure is *multiplicative* over products: gamma(cube^d) =
    gamma(cube)^d. To hold a certificate at >= 1/2 you need half-side
    C ~ sqrt(2 ln d). **That is exactly where the sqrt(log) bound comes from.**
  - Directional total variation of a *product* density is an *average*, not a
    product, and stays flat in dimension (verified by Monte Carlo across seven
    dimensions, reproducing the paper's own numbers).

  *Confidence: high. This is the single most transferable object the programme
  has produced, and it is mechanically checkable on any candidate invariant.*

**E5. Two candidate discriminators separating a board from a restatement.**
Derived inductively from three boards, NOT validated:
  (a) *Is the invariant verifiable on the initial state by an independent
      computation, without assuming the conjecture?*
  (b) *Is the legal move a formula, or does it require an existence theorem to
      guarantee a legal move exists at each step?*
  On these, Guo–Fang–Lu scores (yes, formula); Bansal–Jiang's earlier board
  scores (yes, existence theorem — an SDP feasibility result); the convolution
  board scores (no, formula). *Confidence: low. n = 3, unblinded, and the same
  model that proposed the discriminators scored them.*

**E6. Prompt weight does not buy rigour, and may cost it.** In a four-agent
trial, the agent under the heaviest prompt produced the sloppiest derivation: a
garbled step, a false lemma, and a self-certified check that its own text
immediately contradicted. *Confidence: moderate, n = 4, one problem.*

**E7. Clause presence is not clause execution.** The largest single error found
across a four-response corpus — a confident impossibility theorem, false, with
its counterexample already published — would have been caught by a clause
present in the template since v1 and simply not run. *Confidence: high for the
instance; the generalisation is untested.*

**E8. Impossibility claims are the highest-risk output class.** Asymmetry: a
false possibility claim gets refuted by someone trying; a false impossibility
claim is believed and closes the line. Both no-tool responses in the corpus
built a NEGATIVE verdict on an unsupported "this forces that" step.

**E9. Verification *selection* dominates verification *quality*.** One agent ran
a Monte Carlo check correctly, honestly reported it, and reproduced exactly —
but the quantity it checked has variance exactly 1 by construction, so the
"bound" it confirmed is the Gaussian value and the claimed tightness is the
central limit theorem. Sound checking, near-zero discriminating power, because
of what was chosen for checking.

**E10. Ceiling effects destroyed the one template experiment that was run.** The
test problem was solvable by every arm including the placebo control, so the
primary outcome was null and nothing was learned about the template. *A problem
battery with a non-zero baseline failure rate is a hard design requirement.*

---

## 3. What has NOT been established — the hole you are being asked to fill

**Every version of the template (v1 -> v2 -> v2.1) was justified post-hoc, from
n <= 4 observations, unblinded, by the same model that wrote the clauses.**

There is no ground truth, no ablation, and no evidence that any individual
clause changes agent behaviour in the direction claimed. The programme has been
producing *prescriptions*. It needs *measurements*, and it has never had the
budget or the breadth to get them.

That is the commission.

---
## 4. The current template (v2.1), verbatim

This is what you are improving. It is an instrument for an agent working a
problem that someone else has chosen and inserted. Rules marked (S) require
substrate the prompt cannot supply.

```
================================================================
RESEARCH PROTOCOL — v2.1
Fill every [BRACKET] before use. Rules marked (S) require substrate the
prompt itself cannot supply; see §0.
================================================================

0. SUBSTRATE DECLARATION            [filled by the operator, not the agent]

  Concurrent agents available: [N]
  Independent auditor available: [YES / NO]
  Proof assistant available: [NAME / NONE]
  Budget meter visible to agents: [YES / NO]
  Status of this problem as of [DATE]: [OPEN / SOLVED — do not proceed]

  If N = 1, every rule marked (S) is UNENFORCED and must be reported as
  such, not simulated. A rule whose substrate is absent is not to be
  role-played. Writing an "audit" of an argument you also wrote is not an
  audit; label it SELF-REVIEW (UNENFORCED) wherever the protocol calls for
  an independent one. Reporting a protocol step as performed when its
  substrate was absent is the most serious violation in this document —
  more serious than an unproved lemma, because an unproved lemma is
  visible to the next reader and a fabricated check is not.

1. PROBLEM SPECIFICATION

  [FORMAL STATEMENT: every object defined from scratch; all quantifiers
   explicit. Do not substitute nearby or more convenient definitions.]
  [EDGE CASES: resolve degenerate instances explicitly — empty structures,
   trivial sizes, disconnected or reducible cases — stating how each is
   handled.]

  DECOMPOSITION. State whether the target factors into sub-claims normally
  established by different mechanisms (an obstruction half and a matching
  witness half; necessity and sufficiency). If the target requires a
  CONJUNCTION of named properties, enumerate the conjuncts and register
  each as its own sub-target with its own gap-ledger entry and its own
  certificate. Establishing k−1 of k conjuncts is not a partial solution;
  it is return-condition (c). No conjunct may be discharged by "the same
  argument", "by symmetry", or "an analogous computation" (see PARALLELISM,
  §4).

  SCALE REGIME. State which quantifiers are asymptotic and which are
  claimed for every instance. An argument established only on a
  subsequence, parity class, or asymptotic regime must carry an explicit
  interpolation, padding, or boundary argument extending it to everything
  the target quantifies over, or the target is restated with the weaker
  scope made visible. It may not be absorbed into "for large n".

2. TARGET AND NON-TARGETS

  A complete solution proves exactly [EXACT CLAIM], with no auxiliary
  hypotheses. None of the following counts, and none may be returned as a
  solution:
   - restricted subclasses: [LIST KNOWN PARTIAL CLASSES];
   - weakened or approximate versions: [LIST RELAXATIONS AND BEST BOUNDS];
   - reduction to any unproved statement, including these known to be
     equivalent to or stronger than the target: [LIST EQUIVALENT-STRENGTH
     TRAPS];
   - computational verification to any finite bound, however large;
   - a candidate counterexample without a complete audited certificate;
   - an argument whose central inequality, threshold, or gap rests on a
     parameter choice justified only by "optimizing appropriately";
   - a construction satisfying only part of a conjunctively required list
     of named hypotheses;
   - a construction whose recipe is incompatible in principle with a
     required property (see RECIPE–PROPERTY INCOMPATIBILITY, §4),
     explained away case-by-case without ever testing the elements the
     recipe itself forces.

3. EPISTEMIC STANCE

  Do not assume the statement is true or false. Run a proof track and a
  disproof track; the disproof track searches for counterexamples and for
  obstructions explaining why proposed mechanisms must fail. It holds at
  least [max(1, N/4)] agents at all times and is never the first thing
  cut. Mine failures in each direction for constraints usable by the other.

  Every abandoned approach returned as an artifact must name the specific
  invariant, quantity, or piece of structure it could not control — "this
  bound forgets the location of the negative mass", "this normalization is
  not preserved under transport", "this witness is not fixed before the
  adversarial choice is revealed", "this recipe forces a nontrivial
  centre". "It failed", or "it lost a constant", is not a diagnosis, and
  the artifact is returned incomplete.

  Do not consult any source for the status, history, or attempted
  solutions of this exact problem; §0 already records its status. External
  search is permitted for standard named theorems, ordinary background,
  and barrier or no-go results (§4). Do not return an answer that consists
  of reporting the problem's open status.

  Tag every claim with exactly one of: DERIVED HERE (a proof appears in
  this artifact) / STANDARD (a named theorem, cited) / COMPUTED (an
  explicit calculation, shown) / CONJECTURED (believed, unproved) /
  ASSUMED (used without support). Untagged prose is read as ASSUMED.

4. NAMED FAILURE PRINCIPLES

  Each is stated once here and referred to by name elsewhere. The examples
  are a bank, not a list to match against: the same shape of failure in
  another domain is the same failure.

  RECIPE–PROPERTY INCOMPATIBILITY. Before proving that an object built by
  a general recipe (extension, quotient, gluing, deformation, limit) has a
  required property, verify from the shape of the recipe alone that the
  property is possible at all. A nontrivial centre rules out ICC; a global
  fixed point rules out a free action; a nonzero kernel rules out
  injectivity claimed alongside it; a common invariant subobject rules out
  simplicity or primitivity; a counting or parity obstruction (Euler,
  degree-sum, Hall) rules out an incidence structure however its pieces
  are chosen. This check precedes and is independent of any
  generic-element argument, because such arguments can succeed on every
  element tested while never touching the distinguished element the recipe
  introduced.

  FORCED ELEMENTS. When a property requires no fixed points, only infinite
  orbits, or trivial stabilizers, test it explicitly on the elements the
  construction distinguishes — base points, gluing elements, markers, the
  lattice or subgroup used to build an extension, a chosen generator.
  State what the argument does to those elements. "The same bound applies"
  is not a statement of what it does.

  PARALLELISM. Any step justified by "the same argument", "by symmetry",
  or "analogously" is written out in full for the parallel case,
  especially where the cases differ in a structural feature — split vs
  non-split, trivial vs nontrivial centre, generic vs degenerate parameter
  — that plausibly bears on the property being proved.

  CONFLATED OBJECTS. Two quantities that agree at a point, share a
  derivative, or look alike under an integral or expectation are not
  identical. If only an inequality (Jensen, convexity, Cauchy–Schwarz)
  relates them, only that inequality may be used, and only in the
  direction it goes.

  QUANTIFIER ORDER. Any random, greedy, or existential object — a matrix,
  a shift, an index, a cutoff — must be fixed before, and independently
  of, the instance, adversarial choice, or conditioning event it is
  applied to. Flag every step where ∃ and ∀ could be silently swapped.

  DIVISION BLOWUP. A bound obtained before conditioning, or in
  expectation, is checked for what happens when it is divided by a
  probability, weight, or norm that the instance can make small. A bound
  that survives only on the typical branch is not a bound.

  HEURISTIC COUNTS. Any Bézout-type, volume, or dimension count is checked
  for base loci, non-reduced components, and non-generic strata that the
  count silently assumes away.

  PARAMETER JUSTIFICATION. Every optimized parameter, threshold, or cutoff
  is traced to an explicit inequality placing it in the required range,
  with the sign of the resulting margin proved outright.

  COVERAGE DIRECTION. A construction that emits only valid instances says
  nothing about the instances it does not emit. Name the map, its image,
  and the target set, and state which containment you are claiming: that
  every output is good — usually easy, and usually not the theorem — or
  that every element of the target is an output, which is usually the
  theorem and usually unproved. Exhibiting a family and observing that it
  happens to hit every target instance up to a bound establishes the first
  containment and a finite check of the second; it does not establish the
  second. This is the constructive form of QUANTIFIER ORDER, and it is the
  dominant failure mode in parametric, recipe-based, and generative work.

  BARRIER CHECK. Before a family receives a second agent, state whether a
  known no-go or barrier theorem in this domain excludes mechanisms of its
  type, and if so, which specific feature of this mechanism escapes it. An
  approach that cannot answer this is speculative, not active.

5. DERIVATION DISCIPLINE

  A formula, recurrence, or coefficient obtained by analogy with a
  structurally similar known object may not be used in any later step
  until it has both:
   (a) been re-derived from the actual defining maps and objects of this
       problem, not assumed to transfer from the analogous setting; and
   (b) been checked against at least one small explicit instance computed
       by hand or by direct enumeration, with the check shown.

  A check is reported by its content, not by its verdict. Show the
  instantiation: the object chosen, the numbers, the expression that
  results. A line asserting that a check passed, without exhibiting what
  was computed, is void, and the check counts as not performed. Checklists
  of ticks are not audit output and are discarded unread.

  If you abandon a computation mid-stream — "wait", "let me redo this",
  "actually" — every conclusion downstream of it is void until recomputed.
  A superseded verdict may not be left standing beside the computation
  that superseded it. Delete it, or redo it.

6. ORCHESTRATION                                                       (S)

  Up to [N] concurrent agents.
   - Registry: one entry per approach FAMILY, and per sub-target or
     conjunct from §1, recording the core mathematical mechanism (not its
     wording), the specific invariant or structure that mechanism
     controls, agents assigned, the strongest lemma proved so far, the
     current gap stated as a formal proposition, and a status ∈ {active,
     blocked, merged, refuted}.
   - An approach is BLOCKED when its gap is a proposition of strength
     comparable to the target. Blocked approaches receive no agents until
     a materially new mechanism is proposed; log what that mechanism
     controls that the previous ones did not.
   - (S) Independence: in early rounds, do not disclose the favoured
     approach or other agents' progress to exploring agents.
     Cross-pollinate only between approaches that have each produced at
     least one nontrivial proved lemma.
   - (S) If more than [K] agents converge on one family, reassign the
     excess to the least-explored active families.
   - Progress on conjunct i of k is never logged as progress toward the
     target without the explicit count of conjuncts still unestablished.
   - Agents return artifacts only: proved lemmas with complete proofs,
     explicit constructions, counterexamples to proposed sublemmas, the
     small-instance and compatibility checks required above, or a formal
     statement of the obstruction hit and the invariant it could not
     control. Status reports, confidence estimates, and steps called
     "routine", "standard", or "parallel to the previous case" are
     rejected, and the step goes to the gap ledger.

7. ADVERSARIAL AUDIT

  Before exploration, generate a domain-specific failure checklist: the
  known ways proofs of this and neighbouring statements have historically
  been wrong. [DOMAIN-SPECIFIC TRAPS: definitional near-misses, degenerate
  cases, quantifier slips, operations that silently violate the
  hypotheses, circular use of equivalent statements.]

  Every candidate is audited against §4 and against the three checks
  below. Those three exist because §4 is a taxonomy of commission — of
  what is written down wrongly — and an argument in which every written
  step is correct can still be worthless. These ask what is missing.

   - COVERAGE. State the rule by which the case list, registry, or
     evidence set was populated. Report both the number of items that rule
     yields and the number actually treated. Any difference is a
     gap-ledger entry. "The ones I found" is not an enumeration rule.
     (S) An auditor who did not populate the set re-runs the rule and
     diffs the result.
   - MEASUREMENT VALIDITY. For every quantity offered as evidence, state
     what its value would be if the claim were false. If you cannot, it is
     not evidence. Decompose any composite quantity and report the share
     contributed by its largest component; a quantity more than half
     driven by one uninformative component is renamed after that component
     or dropped.
   - SCOPE CHECK. Apply the proof mechanism, unchanged, to a nearby or
     structurally analogous statement with a KNOWN false, weaker, or tight
     answer — a neighbouring object, a classical special case, the same
     statement one parameter step outside the range where it holds — and
     report the expression the mechanism produces there. If it does not
     visibly break or weaken exactly where it should, treat that as
     evidence of an error, not of extra strength. If it does break, name
     the step OF THE MECHANISM that breaks.
     The target must be one where the mechanism would plausibly appear to
     succeed and must not. Observing that the statement fails outside its
     own stated domain does NOT satisfy this clause: the domain boundary is
     always available, the mechanism is usually not even applied there, and
     it discriminates nothing. Nor does an appeal to a general inequality
     that holds whatever the mechanism is. If the only breaking point you
     can find is the domain boundary, report the SCOPE CHECK as NOT
     PERFORMED rather than as passed.

  (S) Candidates are audited by agents who did not contribute to them,
  with a mandate to break them; a candidate survives only if every
  objection is answered with a proof, not a clarification. Where no
  independent auditor exists, this is SELF-REVIEW (UNENFORCED) and is
  labelled so in the return.

  Before verification, the surviving proof is reduced to a compact
  mechanism statement: a short, self-contained restatement of exactly
  which objects, invariants, and inequalities compose the argument, with,
  for a conjunctive target, the list confirming each conjunct's
  independent certificate. That statement, not the exploration record, is
  what proceeds.

8. VERIFICATION LADDER

  Formalize the surviving proof in [PROOF ASSISTANT]; a step that resists
  formalization returns to the gap ledger and the proof is not complete.
  Where no proof assistant is available, say so and descend the ladder,
  reporting in the return which rung was actually reached:
   1. machine-checked in [PROOF ASSISTANT];
   2. every quantitative step recomputed by an independent executable
      script, with the script and its output included;
   3. every quantitative step recomputed by hand on an explicit small
      instance, shown in full;
   4. (S) re-derived by an agent given only the compact mechanism
      statement and the problem, never the proof;
   5. none of the above — the proof is unverified, and says so in its
      first sentence.

9. BUDGET AND RETURN CONDITIONS

  Budget: [T], in whatever unit the operator can actually meter. An agent
  cannot see its own consumption, so checkpoints are keyed to countable
  events instead: log the registry state — for each active family or
  conjunct, its controlled invariant and its current gap — after every [C]
  returned artifacts, and at the end of every wave.

  Early return is permitted only for (a) or (b) below. Do not return early
  because approaches have failed: a failed wave triggers a new wave with
  genuinely new mechanisms, and the new wave's registry entry records what
  invariant it proposes to control that the exhausted ones did not. Stop
  opening waves when [W] consecutive waves have produced no new controlled
  invariant. That condition, not exhaustion of the clock, ends the search.

  Return exactly one of:
   (a) a complete audited proof, with its compact mechanism statement, the
       verification rung reached in §8, and, for a conjunctive target, the
       checklist confirming every conjunct was independently certified;
   (b) a verified counterexample with a complete certificate;
   (c) a structured failure report: the registry including controlled
       invariants, the single strongest fully proved derivation, its
       remaining gap stated as one formal proposition, an explicit list of
       any conjuncts left unestablished, the coverage figures from §7, and
       a declaration in its first sentence that this is NOT a solution.

  Never return anything in the space between (a)/(b) and (c): no
  "essentially complete" proof, no reduction presented as progress, no
  best-effort essay, no construction presented as a solution when a
  required conjunct has been asserted rather than proved.

  (c) is a success condition of this protocol, not a failure of it. On an
  open problem it is the expected outcome. A correct (c) is worth more
  than an (a) that does not survive.
```

---

## 5. Your tasks, in priority order

Priority is set by what a long-reasoning model with agent creation and tools can
do that the originating instance demonstrably could not. **Do them in order. A
completed P1 with nothing else is a better outcome than four sketches.**

### P1 — Build a retrodiction benchmark with ground truth

The programme has never had a scoreable target. Build one.

Assemble a set of historical board changes in mathematics where the *before*
state and the *after* board are both documented well enough to reconstruct. For
each case, produce: the pre-breakthrough board in the five slots (state, move,
invariant, composition, terminal certificate); the bound or obstruction that
held at the time; a **leak table** naming, for each dimension- or log-factor in
that bound, the exact mechanism producing it; and the board that actually
superseded it, held out.

Candidate cases, offered as starting points and not as a validated list —
verify each and discard any whose before/after is not cleanly documented:
sensitivity conjecture (before: combinatorial approaches; after: Huang's signed
adjacency matrix and eigenvalue interlacing); sphere packing in dimensions 8 and
24 (after: Viazovska's modular-form magic functions); cap set (before: Fourier
analytic; after: Croot–Lev–Pach / Ellenberg–Gijswijt polynomial method); the PCP
theorem (after: Dinur's gap amplification); discrepancy (before: entropy and
partial colouring; after: Banaszczyk's Gaussian measure). Extend this list —
breadth across fields matters more than depth in any one.

**The central methodological difficulty, which is yours to solve and which the
originating instance could not:** you already know all of these answers, so a
naive "did it rediscover the known board?" score is contaminated by
construction. Do not paper over this. Design the contamination control
explicitly and argue for it. One direction worth considering — not a
prescription — is scoring *discrimination* rather than *recall*: present the
diagnostic with matched pairs of (leak, candidate transformation) where half are
the historically correct move and half are constructed to be superficially
attractive and wrong, and measure separation. Contamination inflates recall much
more obviously than it inflates discrimination. Find something better if you
can, and say why it is better.

**Deliverable:** the benchmark itself, with per-case sources, the held-out
answers, the scoring rubric, and an explicit statement of what the rubric can
and cannot detect.

### P2 — Ablate the template

Run a factorial ablation to find which clauses actually change agent behaviour
in the direction claimed. Use your agent-creation capability; this is the
experiment the originating instance could not afford.

Hard design constraints, learned expensively (see E10 and E6):

  - **The problem battery must have a non-zero baseline failure rate.** If an
    unaided agent solves everything, every arm scores 100% and you learn
    nothing. Pilot this before committing budget.
  - **Include a length-matched placebo arm**, not just a short-prompt control.
    Otherwise you measure instruction volume, not instruction content.
  - **Pre-register outcomes before running**, as yes/no questions with their
    evidence named. State predictions and score them as written afterwards,
    including the ones you get wrong.
  - Distinguish **clause present** from **clause executed** (E7). A clause that
    is never run is not a clause that failed; report the two separately.

**Deliverable:** for each clause — does it change behaviour, in which direction,
at what cost in tokens, and does it survive the placebo comparison? Clauses that
do not earn their place should be named for deletion. Expect some of them to be
ornamental; saying so is a result.

### P3 — Turn the catalogue into a decision procedure

The programme has a *vocabulary* of board transformations and no procedure for
choosing among them. The object that is missing sits upstream of both the
insight and the board: **given a leak table, which transformation do you attempt
first, and what is the expected yield?**

Five candidate transformations, inductively derived from three examples and
therefore weak (this is a starting point to be attacked, not a result to be
extended):

  1. **De-tensorize.** Invariant multiplicative under the product construction
     that generates hard instances -> replace with an averaging one.
     *Diagnostic: compute I on a product and compare to I on the factors.*
     This is E4 and is the only entry with real support.
  2. **Auxiliary-witness lift.** Replace "state S has property P" with
     "there exists w attached to S with property P'", where w may be rebuilt
     from scratch at each step rather than transported.
  3. **Move work between the step invariant and the terminal certificate.**
  4. **Collectivize a union bound.** Per-item control plus a union over m items
     -> joint control on the collection.
  5. **Formula-ize the move.** Replace a constrained move needing a feasibility
     theorem with an unconditionally defined operator, pushing the difficulty
     into the invariant.

Test these against P1's benchmark. Specifically: **do the diagnostics predict?**
Look hard for counterexamples — cases where the diagnostic fires and the
transformation fails, or where a real historical board change fits none of the
five. Both would be more valuable than a sixth entry.

### P4 — Write v3, justified by P1–P3

Only after the above. Constraints:

  - **v3 may be shorter than v2.1.** Given E6 and E7, adding clauses is the
    suspect move. Deletions justified by P2 are as valuable as additions.
  - Every clause must cite the measurement that justifies it, or be marked
    explicitly as unmeasured and retained on judgement.
  - Address E7 directly: the template's problem may be execution rather than
    content. If so, the fix is structural (forcing execution, demanding the
    computed content of a check rather than its verdict) rather than textual.
  - Keep it an instrument for an agent working an *inserted* problem. Problem
    selection is out of scope.

---

## 6. What NOT to spend budget on

An Opus instance has already done these. Redoing them is waste.

  - **Auditing arXiv:2609.11189.** Done to rung 2 — every arithmetic step
    recomputed, no error found, the weight located in three external citations.
    The one open item needs a specialist in Finsler p-Laplacian eigenvalue
    theory, not more general reasoning. Do not re-derive it unless that is
    genuinely within reach for you, in which case say so and do it as a separate
    aside, not in place of P1–P4.
  - **Rediscovering the convolution board for Komlós.** Four models already did;
    it is a restatement (E2).
  - **Producing another prose framework without measurement.** That is the
    failure mode this commission exists to break. A well-argued taxonomy with no
    experiment attached is the specific thing not wanted.
  - **Arithmetic verification, computational reproduction, or empirical
    extension of published claims.** The originating instance does this well
    and cheaply; it is not where your comparative advantage lies.

---

## 7. Honesty requirements

These are not decoration; the programme has repeatedly overturned its own
headline findings and expects you to do the same.

  - Separate what you **measured** from what you **reasoned** from what you
    **assume**. Tag claims.
  - **Report negative results as results.** The most valuable outcomes available
    here are: "clause X does nothing", "diagnostic Y fails on case Z", "the
    benchmark cannot detect W".
  - **State impossibility claims with extreme care** (E8). Before asserting that
    some class of approach cannot work, test the argument against one small
    instance where the answer is known. The corpus's largest error was exactly
    this failure.
  - If contamination defeats P1, **say so and report the attempt**, rather than
    producing a benchmark whose scores do not mean what they appear to.
  - Where you disagree with anything in §2, say so and give the reason. Several
    of those findings rest on n <= 4.

---

## 8. Deliverables

1. The retrodiction benchmark (P1), with sources, held-out answers, scoring
   rubric, and contamination control.
2. Ablation results (P2), pre-registered and scored as written.
3. The decision procedure (P3), with its counterexamples.
4. Template v3 (P4), every clause traced to a measurement or flagged unmeasured.
5. A short register of everything you tried that failed, and what it cost.
