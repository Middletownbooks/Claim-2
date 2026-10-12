# The witness-search prompt, standalone

*Companion to `PROMPT.md`, not a replacement. `PROMPT.md` screens boards whose
**bound leaks**; it needs a quantitative target with a pushable parameter, and
`RANKING_FIT.md` §3 measures where that bites: **23 of the 35 playable records in
the top 500 are pure yes/no questions on which the leak table has no row to
write.** This prompt covers that half. Same shape — Part A is pasted verbatim,
Part B is for the operator and names the failure each clause is built against.*

*Scope rule, applied before either prompt: if the target is quantitative, use
`PROMPT.md`. If a single finite object could settle a branch, use this one. Twelve
records take both (`RANKING_FIT.md` §3). Most take neither, and declining is a
first-class outcome here as it is there.*

---

## Part A — paste from here

> You are given an open mathematical problem. Your job is to decide whether it can
> be **played** — whether some single finite object, checkable by a terminating
> computation, would settle one of its branches — and if so, to specify the search
> exactly enough that someone could start it tomorrow.
>
> You are not being asked whether the problem is true, or how to prove it.
>
> ### Input
>
> ```
> PROBLEM:        <one line>
> EXACT TARGET:   <the formal statement, verbatim from its source>
> ```
>
> Report all six steps below, in order, and nothing else.
>
> **1. The quantifier prefix, written out.**
> Rewrite the exact target as a quantifier string — ∀x∃y∀z… — naming the domain of
> each variable. Then answer: **is the outermost existential nested under a
> universal?** If it is, the object it binds is a *constant*, not a witness, and
> this problem is not playable however existential it sounds. Say so and go to step
> 6. Examples that fail here: *abc* (∀ε∃C), log-rank (∃C∀f), Beck–Fiala (∃C∀H).
>
> **2. The witness schema.**
> Name the object that would settle a branch, as a **data type**, not as a
> description. Not "a counterexample to the conjecture" — *"a pair of finite simple
> graphs on n vertices with equal vertex-deleted decks"*. Write down what a file
> containing one would hold. If you cannot write the schema, say **NO SCHEMA** —
> that is a finding and it usually means step 1 was answered too generously.
>
> State which branch the witness settles, and what the **other** branch would
> require. A witness that settles only one side is normal; claiming it settles both
> is the error to avoid.
>
> **3. The check.**
> Name the terminating computation that verifies a candidate, and give its cost as
> a function of the witness size. Name the algorithm or the library routine, not
> the idea: *"character table via GAP's `CharacterTable`, then compare k_0(B)"*, not
> *"compute the relevant invariants"*.
>
> Then the question that kills more candidates than any other: **is the predicate
> decidable at all?** Some finite objects cannot be checked. A knot diagram is
> finite; *"is this knot slice and not ribbon"* is not decidable. If the check is
> only semi-decidable, or decidable in principle by an algorithm nobody has
> implemented, say which and stop calling it a check.
>
> **4. The search space, with a number.**
> Give the size of the space the witness lives in at the smallest untried parameter,
> as an explicit figure — 10^k, not "large". Then: **what bounds the search?** Name
> the structural constraint that cuts it — a congruence, a known lower bound on the
> counterexample, a classification that restricts the candidates. A search space
> with no stated constraint is not a search, it is enumeration, and you should say
> so.
>
> Distinguish **finite** from **feasible** explicitly. Both branches of that
> distinction are results: *"finite and hopeless at 10^154"* is worth as much here
> as *"feasible, 10^9 candidates at 3μs each"*.
>
> **5. What has already been swept.**
> How far has this space been searched, by whom, and where is that recorded? Give
> the frontier as a number — *verified to 4·10^18*, *all groups of order < 2000*,
> *all knots to 24 crossings*. If you do not know, write **SWEEP UNKNOWN**: it is
> the single most valuable thing to find out next and the cheapest, and guessing it
> destroys the estimate in step 4.
>
> A published sweep that found nothing is not discouraging — it is the constraint
> that makes step 4's number mean something.
>
> **6. Three closing fields.**
> (a) **Verdict**: PLAYABLE, with the branch named; or NOT PLAYABLE, with the step
> that failed (1, 2, 3 or 4). A clean NOT PLAYABLE with its reason is worth more
> than a strained PLAYABLE.
> (b) Any claim that no witness can exist must carry: the class of objects you
> enumerated, **one named object outside that class**, and the argument that the
> class is closed. A claim missing the second is an unchecked quantifier, not a
> negative result.
> (c) Do you recognise this problem? If so, name it and say what is known. Answer
> this **last**; it is read **first** when your response is scored.

## Part A ends here

---

## Part B — operator notes, do not paste

### What each clause is built against

| clause | the observed failure |
|---|---|
| **step 1, the prefix, written before anything else** | the first pass over the top 500 classified on keyword presence and put `abc`, log-rank, Erdős–Hajnal and Beck–Fiala in the existence bucket — all four say "there exists", all four bind a constant under a universal. The pass had to be thrown away. Writing the prefix out is the whole fix, and it is one line |
| **step 2 demanding a data type** | `PLAYABILITY.md` §1: the ranking's own `resolutionConsequences` field describes both branches in prose for **493 of 499 records in the identical binary shape**, and carries no information about whether either branch is reachable. Prose about a branch is not a schema. A file layout is |
| step 2's **which branch** clause | the congruent number problem is playable on the YES side only — a rational point certifies, nothing finite refutes. Recording a one-sided witness as two-sided is the commonest inflation |
| **step 3's decidability question** | class **W**: slice-ribbon and Quillen's conjecture both have finite, writable witnesses and undecidable predicates. Against the I/I\*/II/III taxonomy this is a new cell — I\* was finite-but-unlistable, W is listable-but-uncheckable — and no earlier screen in this project had a clause that catches it |
| step 3 naming **the routine, not the idea** | the same remedy D35 forced on `move_kind` and D20 forced on the five-transformation vocabulary: a label does not transfer between raters, a named object does. `CharacterTable` is checkable by a third party; "compute the invariants" is not |
| **step 4's finite-vs-feasible split** | the Shannon artifact's witness is an independent set in C₁₁²¹³ with ~10¹⁵⁴ elements — finite, unlistable, and the reason category I\* exists. Every verdict in `PLAYABILITY.md` §2 is classified on whether a check *terminates*, not on whether it terminates this century. That is the census's own stated gap and this step is where it gets closed, one problem at a time |
| **step 5, and its SWEEP UNKNOWN escape** | `PROOFATLAS_FIT.md`'s finding that encoding, not selection, is the bottleneck — restated for this half of the corpus. The sweep frontier is the one input that makes step 4 mean anything, it is absent from every field of the ranking, and it is cheap to look up. Forcing the model to *declare* ignorance rather than estimate around it is the point |
| 6(b) | carried unchanged from `PROMPT.md`: a confident impossibility claim in the reference corpus asserted all smooth certificates reduce to a moment class, and a paper five days older reached the target with an L¹ derivative norm outside it. Impossibility claims are the output that stops a search and the one least reliable |
| 6(c) last, read first | contamination has to be measured, not assumed away. Recall is higher here than for board-search — these are famous problems with famous sweeps — so the probe matters more, not less |
| brevity | the heaviest prompt in this programme produced the sloppiest derivation |

### Controls — run these two before trusting any result

* **Positive: Hadamard matrix of order 668.** Real, playable, and *settled by a
  witness that was actually checked* — the ranking project validated row norms and
  all 222,778 pairwise dot products. Schema, check and cost are all unambiguous. A
  rubric that does not return PLAYABLE here is not measuring witness-search.
* **Negative: polynomial-time integer factorization.** Reads existential — "does
  there exist an algorithm" — and an algorithm *is* a finite object, so step 2 can
  be answered. It dies at step 3: correctness is universally quantified over all
  inputs, so exhibiting the algorithm settles nothing by exhibition. The correct
  response is **NOT PLAYABLE, step 3**. This is the item that separates reading the
  quantifier from reading the vocabulary, and it carries the experiment — class
  **A** holds 16 records including four of the top 25, and any screen keying on
  "there exists" fires on all of them.

### Scoring

Primary outcome is **steps 3 and 4** — decidability and the feasibility split — not
the PLAYABLE/NOT verdict. Step 1 is nearly free once asked and step 2 follows from
it; the discrimination lives in whether a model will say *finite and hopeless* and
whether it will admit a predicate is undecidable. Secondary: the **SWEEP UNKNOWN
rate**, which is a pre-registrable number and measures whether the model
hallucinates search frontiers. The **NOT PLAYABLE rate** is a first-class number,
not a footnote — on the top-500 corpus the truth is 464 of 499, so a rubric
returning PLAYABLE often is miscalibrated by construction.

### Items with known answers

`classification.json` holds 499 scored records: 35 playable with the witness object
named for each, 16 class-A negative controls, 2 class-W items where the predicate
is undecidable, and 424 class-U. The 35 are hand-adjudicated by **one rater with no
blind second pass** — that is this file's weakest link, stated where it can be
acted on. Every verdict names its object precisely so a second rater can score the
object rather than the label, which is the D35 remedy applied prospectively. Run
that second pass before any of this enters a scored set.

### A contamination channel specific to this prompt

Step 5 asks for a search frontier. Those are exactly the facts a tool-enabled model
retrieves in seconds and a tools-off model confabulates fluently — *"verified to
10^20"* is the shape of a sentence a model will produce whether or not it is true,
and unlike a board-search claim it looks checkable, so it survives review. Either
run tools-on and treat step 5 as retrieval rather than reasoning, or run tools-off
and score **SWEEP UNKNOWN as the correct answer**, penalising any specific figure.
Do not mix the arms: prompt wording and tool access were confounded once already in
this programme and no causal claim survived it.
