# The board-search prompt, standalone

Two parts. **Part A is the prompt** — paste it verbatim, with the input template filled
in, and nothing else. **Part B is for the operator** and must not be pasted: it names
the failures each clause is built against, the controls, and the scoring.

The prompt is deliberately short. In this programme's own record the heaviest prompt
produced the sloppiest derivation, and no clause survives here that does not force a
checkable object.

---

## Part A — paste from here

> You are given the state of a mathematical problem as it stood **before** a known
> advance, and nothing else. Your job is to propose better boards for it. It is not to
> find the historical advance — do not go looking for what happened next.
>
> ### Input
>
> ```
> PROBLEM:            <one line>
> BEST KNOWN BOUND:   <the bound as it stood, with its source>
> BEST KNOWN LOWER BOUND OR CONSTRUCTION: <what the truth is known to be at least>
> HOW THE BOUND IS PROVED: <two or three sentences, mechanism only>
> ```
>
> Report all six steps below, in order, and nothing else.
>
> **1. The board, five slots.**
> `STATE` — the object the argument tracks. `MOVE` — the operation applied to it.
> `INVARIANT` — the quantity claimed to be preserved or controlled. `COMPOSITION` — how
> steps combine, including any iteration or union. `TERMINAL` — the condition that ends
> the argument, and what it yields.
> Write **none recorded** where the source has no such slot. Do not invent one to fill
> the table.
>
> **2. The leak table.** One row for every log, dimension, iteration or union factor in
> the current bound:
>
> | factor | the exact mechanism that produces it |
>
> *"Roughly log n from the analysis"* is not a row. *"√log n from the union bound over n
> sets"* is. If you cannot name the mechanism for a factor, write **MECHANISM UNKNOWN**
> — that is a finding, not a gap to fill.
>
> **3. Classify each leak**, exactly one label per row.
> `ACCUMULATION` — the factor equals (rounds or items) × (cost per step).
> `SATURATION` — the invariant caps at a value independent of the parameter being pushed.
> `WRONG STATISTIC` — the invariant controls a quantity other than the one being bounded.
>
> **4. One candidate per leak row, each with a diagnostic you have actually run.**
> Report the number, not the intention. Five moves and their diagnostics:
>
> * **Replace a multiplicative invariant with an averaging one.** Diagnostic: compute the
>   invariant on a product of hard instances, `I(⊗Sᵢ)`, against `{I(Sᵢ)}`. Multiplicative
>   ⟹ the certificate pays a factor per coordinate; averaging ⟹ it does not.
> * **Attach a witness rather than transport one.** Replace "S has property P" with
>   "there is a w attached to S with property P′", letting w be rebuilt at every step.
>   Diagnostic: is your invariant hard to transport but easy to re-derive?
> * **Shift weight between the terminal check and the step.** Diagnostic: which end
>   carries the work now, and what happens to the other end if you move it?
> * **Collectivize a union bound.** Per-item control plus a union over m becomes joint
>   control. Diagnostic: does the loss equal m × per-item cost?
> * **Replace a constrained move plus a feasibility theorem by an unconditionally defined
>   operator.** Diagnostic: does a legal move currently require an existence theorem?
>   Name it.
>
> A move outside this list is welcome, with a diagnostic of the same kind: a computation
> whose outcome could have gone either way.
>
> **5. Triage every candidate. Two questions decide it.**
> **T1.** Can the invariant be verified on the **starting state**, by an independent
> computation, *without knowing whether the target theorem is true*? If no, you have
> proposed a **restatement** of the theorem. Say so plainly — it is a valid finding and a
> common one.
> **T2.** Is the legal move a **formula**, or does it need an **existence theorem**?
> **Name the object either way**: if a theorem, which theorem and what it costs; if a
> formula, write it down. The label on its own is not an answer — two raters agreeing on
> a word is not evidence, and two raters applying the same criterion to a named object is.
> **T3.** Evaluate the invariant's threshold on the **target** state: compute
> min{C : the invariant holds for the target at scale C}. If that is not O(1), then no
> move *certified by this invariant* reaches O(1) — say so, and say where the cap sits.
> Say also whether the move is **monotone** in the invariant: if the move can only degrade
> it, the cap holds whatever the move does; if not, the cap is on the invariant and the
> target may still be true by another certificate.
> If min{C} comes back O(1), say **which way the threshold moves with the scale**. If the
> invariant gets *easier* as the target grows, it is **not binding at any scale** — that is a
> third answer, not a pass, and it means the whole burden has been moved into the move. If the invariant is not a threshold on
> a scale — if its loss is (rounds) × (cost per step) instead — answer **does not parse for
> this board** and say which it is. Do not manufacture a threshold to fill the field.
> Then, per candidate, **the kill test**: the single computation that would refute it. Run
> it if you can and report what happened.
>
> **6. Three closing fields.**
> (a) For each candidate: does it **remove** the obstruction or **relocate** it? A
> relocation reported as one is worth more here than a removal claimed without a kill
> test.
> (b) Any impossibility claim you made anywhere above must carry: the class of
> certificates you enumerated, **one named functional outside that class**, and the
> argument that the class is closed. A claim missing the second is an unchecked
> quantifier, not a negative result.
> (c) Do you recognise this problem? If so, name it and say what happened next. Answer
> this **last**, and answer it honestly — it is read **first** when your response is
> scored, and a candidate that survives its kill test loses nothing by your having
> recognised the problem.

## Part A ends here

---

## Part B — operator notes, do not paste

### What each clause is built against

| clause | the observed failure |
|---|---|
| leak table with **named mechanisms** | the programme's recurring failure mode: every written step defensible, the quantifier doing the real work left unchecked. A named mechanism is a checkable object |
| **run** the diagnostic, report the number | the five-transformation vocabulary scored **κ = 0.048** across three raters, who gave three different labels to the founding case, and one applied a label *backwards*. The computation needs no agreement on a word |
| **T1** | all four responses in the reference corpus converged on the same board, and one **proved** that such a class exists *if and only if* the conjecture holds — reporting it as a find when it is the diagnosis. T1 is what separates a board from a restatement |
| **T3** | added after the controls: T1 and T2 both **passed** on a board that provably cannot reach the target, so they are not sufficient. One line catches it — and it is the test a ratio-based tightness screen is blind to, because both sides can be O(1) while the constant is open |
| T3's **monotone** clause, and its restraint about what a cap means | a blind coverage rater found the first wording overstated: it inferred "no improvement to the move can reach O(1)" from a cap that is only a cap **on the invariant**. On two of the six benchmark boards the incumbent move is itself lossy and the target is nonetheless **true** (Marcus–Spielman–Srivastava; Spencer), so the sound inference needs the monotonicity check. Only where the move can only degrade the invariant — Banaszczyk's measure board — is the original sentence literally right |
| T3's **not binding at any scale** clause | arm 3 returned "no cap" **for the wrong reason**: min κ = Θ(1/C) on the target *decreases* in C, so the invariant is easier for bigger bodies and forces every state to be wide — a lower bound on size. An invariant that relaxes as the body grows cannot force the final object anywhere, so O(1) here meant "vacuous", not "clear". Three clauses of T3 are now patches from runs designed here, so **T3's next use should be scored on an item this project did not construct**; until then it is a question worth asking, not a validated screen |
| T3's **does not parse** escape | measured, not argued: T3's question is well-posed on 3 of the 6 benchmark boards and undefined on the three whose loss is (rounds) × (cost per step). A rater forced to answer on one of those three produced a threshold pointing the **wrong way** — for fixed soundness the PCP repetition count is O(1), so "no cap" — which would have scored as a pass |
| **T2** | most of the complexity difference between the two real papers in that corpus sits in exactly this gap: one needs an SDP feasibility theorem for a legal move at every step, the other's move is a formula |
| T2 demanding the **named object**, not the label | the same distinction exists as a coded field in the protocol tree (`move_kind`) and was rated blind on 17 items: **κ = 0.430**, with all six disagreements running one way, because one rater asked whether the prose reads like a computation and the other whether the move can proceed before a good object is shown to exist. A label did not transfer between raters; a named theorem or a written-out formula is checkable by a third party |
| kill test | search fails by generating too little and verification by accepting too much. Asking for candidates *with* their refutation keeps both failure modes in one response |
| **6(b)** | a confident impossibility claim asserted that all smooth certificates reduce to a moment class. A paper five days older reached the target with an L¹ derivative norm, outside that class |
| **6(a)** | three of four responses reported, unprompted, that their own candidate relocated rather than removed the obstruction. It is a reliable signal, so ask for it |
| **6(c)** last, read first | a rule-less rater ceilings the retrospective arm at J = 1.000 with 13/13 recognition. Contamination has to be measured, not assumed away |
| brevity | the heaviest prompt in this programme produced the sloppiest derivation |

### Controls — run these two before trusting any result

* **Positive: Banaszczyk's Gaussian-measure board.** A real board with a checkable
  invariant (γ of a body is computable) reaching √log n. A rubric that fails this is not
  measuring board-finding.
* **Negative: the convolution compiler.** A class closed under convolution with the
  terminal property. Its invariant is **provably equivalent to the conjecture**, so the
  correct response is *T1 fails, this is a restatement, decline*. This is the one item
  recall cannot crack: it is generic, not a famous problem to remember, so it separates
  computation from memory. It carries the experiment.

### Scoring

Primary outcome is **T1 and T2**, not board-discovery — in the reference corpus 4 of 4
found a composable invariant and 0 of 4 found a checkable one, so scoring discovery
would return 100% and measure nothing. Secondary: did 6(a) get answered honestly, and
did every impossibility claim carry 6(b)'s three fields. The **not-applicable rate** —
declining — is a first-class number, not a footnote.

Read 6(c) first. On a problem the respondent recognises, a hit tells you about its memory;
the negative control and the kill tests are what remain informative.

### Contamination

Withholding the source does not work with tool access: both tool-enabled responses in the
reference corpus found the surrounding literature within minutes, with zero fabricated
citations. Either run tools-off, or run a tool-enabled arm **purely to measure
contamination** — and keep the two arms separate, because prompt wording and tool access
were confounded once already and no causal claim survived it.

### Items with known answers

`benchmark.json` holds six boards whose conserved replacement is documented, plus the two
controls. Use them to calibrate the rubric before pointing it at anything open.
