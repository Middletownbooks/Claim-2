# The Nevanlinna session prompts, translated

Faithful English translation of the three Chinese-language prompts in the agentic transcript
behind arXiv:2608.26062 (audited in `REPORT_AQ_nevanlinna.md`). Kept for comparison against other
prompt strategies.

**Translation notes.** Numbering oddities are preserved as written — the first prompt's list, the
second prompt's jump from `1.` to `1.2.` and its `2.0.`, and the verbatim duplicated sentence in
`2.9.`. 那个LLM is rendered **"that LLM"**: the operator refers in the *third person* to the model
that produced the draft, addressing this prompt to a different model. 智能体 is rendered "agent".
严格 is rendered "rigorous" where mathematical and "strict" where not.

---

## Prompt 1 — the search instruction (issued as `/goal`; ran 7 h 14 m)

> ## Current task description
>
> Using only your own knowledge, computation and reasoning, find a rigorously valid counterexample
> to the original conjecture in the image I sent you; you may not search the public internet,
> connected data sources, or conclusions from earlier in this conversation.
>
> For the purposes of this task, assume that a counterexample does exist. Search iteratively until
> you find one that can be completely verified. Merely producing numerical indications, approximate
> violations, random-search results, or unproven candidates does not count as completion.
>
> Use multiple agents actively and dynamically. Have different agents independently explore
> different parametrisations, extreme cases, low- and high-dimensional constructions, symmetric and
> asymmetric structures, degenerate cases, random search, optimisation methods, symbolic
> computation, and theoretical constructions; avoid having all agents converge prematurely on a
> single line of thought.
>
> For promising candidate counterexamples, immediately assign an independent agent to carry out an
> adversarial check: recompute the key quantities, check all the hypotheses, look for hidden domain
> or boundary problems, and attempt to prove that the candidate is in fact not a counterexample. If
> a candidate fails, extract the reason for the failure and redirect the search.
>
> The root agent should keep synthesising results and launching new rounds of search; do not stop
> because several methods have failed.
>
> You may end the task only once you have found an explicit object $X$ and rigorously proved:
>
> 1. $X$ satisfies all the hypotheses of the conjecture;
> 2. $X$ genuinely violates the conclusion of the conjecture;
> 3. all key computations or inequalities can be independently re-checked.
>
> Finally, give a concise, self-contained counterexample certificate, including the precise
> definition of the counterexample, verification of the hypotheses, and a rigorous computation of
> the violation of the conclusion. You may not simply answer "the conjecture may be true", "no
> counterexample was found", or "this is an open problem".

## Prompt 2 — the write-up (ran 5 m 51 s)

> Then please write the proof up as complete English LaTeX code for me.

## Prompt 3 — the revision checklist (ran 45 m 52 s)

> I now want to polish this counterexample note into an article that reads as if a human wrote it
> and is submittable. Please do the following:
>
> **1.** Check carefully whether the proof in the note is rigorous and correct, and whether it has
> gaps. Where it is not rigorous, make it rigorous.
>
> **1.2.** Look carefully for further results that could be proved and would make the paper
> substantially stronger, and prove them. For instance, could you settle some new open problem
> related to the note's result, such that once settled it fits naturally into our note? Add it if
> you think it belongs, and don't if it doesn't.
>
> **2.** I want a version submittable to a good pure-mathematics journal, so the paper needs
> serious revision:
>
> **2.0.** Write the abstract, MSC class and keywords. Don't let the abstract get bloated — just
> say what the paper does; there's no need to describe the methods. No more than five keywords.
>
> **2.1.** The introduction needs to be written carefully and with a real sense of history, citing
> everything worth citing, because that LLM easily misses references. Cite the sources of the
> problem/conjecture as fully as possible. If the paper settles an open problem or conjecture,
> state it explicitly in the introduction inside `\begin{problem}...\end{problem}` or
> `\begin{conjecture}...\end{conjecture}`, then say that we settle it, then give the main theorem.
> The main theorem must also appear in the introduction, and there should be an organisation
> paragraph. If you find that my result is already covered by the literature, tell me — then I
> won't have to write this paper.
>
> **2.2.** Check that every numbered equation is actually referenced, and that every item in the
> bibliography is actually cited.
>
> **2.3.** Check whether any of the section and subsection titles are poorly written.
>
> **2.4.** Check the bibliography for inconsistent formatting, whether it is in alphabetical order,
> and whether the references genuinely exist with the correct journal, volume and page numbers.
>
> **2.5.** There seem to be a great many symbols; check for abuse of notation.
>
> **2.6.** Check carefully for grammatical errors, punctuation errors, inconsistent
> character-encoding style, and other low-level mistakes.
>
> **2.7.** I also dislike a "[xxx]" tag following `\begin{xxx}`; it should go *before* the
> environment, as a transitional sentence, which reads more like a human-written paper.
>
> **2.8.** I dislike invented terminology appearing in place of standard terminology, because that
> LLM often invents terms that are not in fact standard and could not appear in a human-written
> paper; find them all and change them.
>
> **2.9.** Check carefully whether each proposition's proof could be simplified by using results
> from the existing literature, because I find that papers written by that LLM tend to reinvent the
> wheel. Check carefully whether each proposition's proof could be simplified by using results from
> the existing literature, because I find that papers written by that LLM tend to reinvent the
> wheel. That LLM has known limitations in properly tracing the provenance of ideas, so you need
> not only to ensure the content is correct but also that attribution is done properly. Note: check
> proposition by proposition, leave none out.
>
> **2.10.** No undefined notation may appear in the paper.
>
> **2.11.** I also dislike propositions that carry derivations inside them (e.g. "Consequently,
> …" is odd, because that amounts to giving a derivation in the statement, and such a derivation
> would be better placed directly in the proof). A proposition should state only the conclusion the
> paper needs, rather than piling conclusions up.
>
> **2.12.** Write it to be reader-friendly; use figures where appropriate.
>
> **2.13.** Study carefully whether this problem has a simpler solution, or whether the proof can
> be substantially simplified. If the proof can be substantially simplified, then of course we
> choose the substantially simplified version.
>
> Finally, tell me what needs changing and where, then send me the complete English LaTeX source of
> the final revised version and the compiled PDF directly.

---

## The strategy, as reusable elements

Extracted for comparison. Each is a distinct, transferable move.

### Prompt 1 — search

| element | what it does |
|---|---|
| **Presume the answer** | "assume that a counterexample does exist" — removes the model's option to conclude the conjecture is true, forcing search rather than assessment. A strong and risky lever. |
| **Ban the retreat phrases by name** | "the conjecture may be true", "no counterexample was found", "this is an open problem" — closes the three specific exits a model takes when stuck. |
| **Ban weak evidence by name** | numerical indications, approximate violations, random-search results, unproven candidates — pre-empts exactly the failure modes an auditor checks for. |
| **Forced diversity** | eleven named search modes, plus an explicit instruction against premature convergence — treats mode collapse as the default failure. |
| **Adversarial check as a separate agent** | the checker is told to *try to prove the candidate is not a counterexample*, not to "verify" it. Falsification, not confirmation. |
| **Failure is fuel** | "extract the reason for the failure and redirect the search"; the root agent must not stop after several methods fail. |
| **A three-part exit condition** | hypotheses satisfied, conclusion violated, computations independently re-checkable — a termination test, not a vibe. |
| **Information isolation** | no internet, no connected sources, no earlier conversation. |

### Prompt 3 — revision

| element | what it does |
|---|---|
| **Third-person distrust** | the draft's author is "that LLM", a named-unreliable instrument; a *different* model is asked to correct it. Adversarial review across models, not self-review. |
| **Defect list from experience** | missing citations, invented terminology, reinvented wheels, undefined notation, derivations inside statements, unreferenced equations, mis-sorted bibliography, fake journal/volume/page data. |
| **Fabricated-citation check** | "whether the references genuinely exist with the correct journal, volume and page numbers" — the one check that catches hallucinated bibliography. |
| **Provenance as a first-class requirement** | "not only to ensure the content is correct but also that attribution is done properly", checked *proposition by proposition*. |
| **An exit for negative results** | "If you find that my result is already covered by the literature, tell me — then I won't have to write this paper." Explicitly rewards the disappointing answer. |
| **Simplify even if it costs the draft** | 2.13 asks whether the whole proof can be replaced by a simpler one. |
| **Human-likeness as a style spec** | 2.7 and 2.8 target tells rather than errors — `[tag]` placement, invented nouns. |

### What is absent, and worth noting

- **No requested self-assessment of confidence.** The exit condition is structural, not a probability.
- **No budget or stopping bound.** The run went 7 h 14 m and ~1.02 M tokens; nothing in the prompt
  capped it, and "do not stop because several methods have failed" pushes the other way.
- **No formalization or machine-checking anywhere.** Consistent with the artifact having no Lean
  and no certificate — the corpus entry's `unreviewed` status traces directly to this omission in
  the prompt.
- **Nothing asks for the negative space** — which lemmas remain unproved, which steps are weakest.
  Arm AQ had to identify those (cusp reflection, the Farey-path limit, the Jordan-domain property)
  from outside. **A single added instruction — "list the steps you consider least secure" — would
  have produced the audit's most useful output for free.**
