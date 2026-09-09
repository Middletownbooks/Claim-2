# Report V — Evaluating the research-orchestration prompt template

Pre-registration: `v/PREREG.md`, committed before any agent ran, including the
declared prediction that the trap would prove too easy to discriminate.
Document analysis: `v/template_analysis.md`.

**n = 4 Haiku agents, one problem, one shot each. No statistical claim is made
or possible.**

---

## The test

The template's distinctive machinery is *negative*: it exists to stop an agent
returning a partial or fabricated result as a solution. So the test is a
false-positive test, on a problem built to trip exactly that.

> Does there exist a finite simple graph that is 4-regular, planar, of girth ≥ 5?

**No.** 4-regularity gives |E| = 2|V|; Euler gives |F| = |V| + 2; girth ≥ 5
gives 2|E| ≥ 5|F|; together 4|V| ≥ 5|V| + 10, i.e. |V| ≤ −10.

Each conjunct alone is trivial to satisfy; the conjunction is impossible. The
trap is deliberately **not** one of the template's own named examples
(centre-vs-ICC, fixed-point-vs-free-action, kernel-vs-injectivity) — using one
of those would have measured whether an agent can pattern-match the template's
examples rather than whether the protocol works.

| arm | n | prompt |
|---|---|---|
| **T** template | 2 | full template instantiated (~1,900 words) |
| **P** plain | 1 | the question, three lines (~40 words) |
| **L** placebo | 1 | generic rigour exhortations, length-matched (~400 words) |

## Primary outcome: 4 / 4 correct. No discrimination.

| agent | verdict | tokens |
|---|---|---|
| T1 | CORRECT-IMPOSSIBLE | 44,651 |
| T2 | CORRECT-IMPOSSIBLE | 40,746 |
| P | CORRECT-IMPOSSIBLE | 40,132 |
| L | CORRECT-IMPOSSIBLE | 43,205 |

Every arm found the Euler/face-counting obstruction and correctly returned
non-existence. **The declared prediction held: this test lacks the power to
discriminate.** That is a fact about the test, not a verdict on the template.

Note the token counts. The template's ~1,900 words of protocol induced no more
deliberation than the 40-word question — 44.7k vs 40.1k, within the spread of
the arms themselves.

## Secondary outcomes, where the arms did differ

Ranked by quality of the *argument*, not the answer:

**L (placebo) — best treatment of the general case.** Alone among the four it
handled disconnection correctly *and* refined the face bound for it: Euler as
|V| − |E| + |F| = k + 1, and the observation that the exterior face is bounded
by k cycles, giving 2|E| ≥ 5(|F|−1) + 5k. No false steps.

**T2 — cleanest template run, and the flagship clause worked.** Its SCOPE CHECK
produced a correct general inequality, |V|(2d − gd + 2g) ≥ 4g, which I verified
independently: at d = 3, g = 5 it gives |V| ≥ 20, and the dodecahedron meets it
tightly (2|E| = 60 = 5|F|). The mechanism visibly breaks exactly where it
should. One defect: it asserted "in a planar embedding of a simple graph, each
face is bounded by a cycle" as a general fact. **It is not** — that needs
bridgelessness. It happens to hold here (4-regular ⇒ all degrees even ⇒
Eulerian ⇒ no bridges), but the agent did not say so.

**P (plain) — correct and shortest**, same unjustified face-boundary claim, and
silently assumed connectivity (used |V| − |E| + |F| = 2 with no discussion).

**T1 — the worst of the four, and it is a template run.**
* A garbled fragment: "Since gcd(3) ≥ 5".
* **A false lemma, with a false proof**: "in any graph with girth g, every
  closed walk has length ≥ g". A closed walk can traverse one edge out and back,
  length 2.
* **A botched SCOPE CHECK, self-certified as passing.** It derived
  |V|·(7k−10)/2 ≥ 5(1+c), which at k = 3, c = 1 yields |V| ≥ 20/11 ≈ 1.8 — then
  stated "so |V| ≥ 20 for c = 1. The dodecahedron has exactly 20 vertices. ✓".
  Its own algebra does not give 20. It then wrote "Wait, let me recalculate
  carefully", abandoned the general formula, and **left the ✓ standing**.

## The finding that survives n = 4

**The SCOPE CHECK clause is behaviourally active.** Both template agents
invoked the dodecahedron as a known-answer calibration; neither control did.
The clause changes what the agent does.

**And in one of two runs it was executed wrongly and certified as passing.**
That is the substantive result. The template's audit machinery instructs the
agent to check its own work and record the outcome; both template agents
produced checklists of ✓ ticks, and in both cases a tick was placed on a step
that did not deserve it — T2 on the face-boundary claim, T1 on an arithmetically
false scope check.

This is direct evidence for the document analysis's main structural point:

> The template's highest-value clause — "audited by agents who did not
> contribute to it" — is precisely the one a prompt cannot enforce. A single
> agent can only roleplay independent audit, and roleplayed audit produces
> ticks.

The contrast within this programme is sharp. In Phase U the same clause was
implemented *architecturally* rather than textually — a separate agent with the
single instruction "find what is missing" — and it overturned the coordinator's
headline result. Here the clause was implemented textually and produced
rubber-stamps.

## What this does and does not license

**Does not license**: any claim that the template is ineffective. One problem,
one shot, n = 2 on the treatment arm, and a trap all four arms solved. The
primary comparison is uninformative by construction, as pre-registered.

**Does license**, narrowly:
1. On a problem of this difficulty the template bought nothing on the primary
   outcome, and cost ~1,900 words.
2. It did not induce more deliberation (token counts flat across arms).
3. A length-matched placebo of generic rigour exhortations produced the most
   careful argument of the four.
4. Self-audit under the template produced ticks, not attacks — twice.

## Recommended changes to the template

1. **Add a coverage/sampling check.** All ~30 of its checks ask *is what you
   wrote correct?*; none asks *what is missing?* Both of this programme's
   headline reversals were omissions that every one of its clauses would have
   passed: Phase S's architecture metric was 54% the rate of the tactic `have`
   (every computation correct, the metric measured the wrong thing), and Phase
   U's forecast ledger drew on four of ten pre-registration documents (every
   entry accurate, the conclusion reversed from p = 1.0000 to p = 0.0389 when
   the missing six were added). Suggested wording is in
   `v/template_analysis.md`.
2. **Split the rules into self-executing and infrastructure-requiring.** SCOPE
   CHECK, conjunct enumeration, derivation discipline and the three-valued
   return work in a prompt. Independent audit, agent reassignment, budget
   checkpoints and non-disclosure do not — they need a coordinator. The
   template presents both classes identically, which invites the failure seen
   here: the strongest clause degrading into self-certification.
3. **Cut the redundancy.** The centre/ICC example appears five times and the
   fixed-point example four; that is accretion around one incident, and it
   risks teaching the examples rather than the principle.
4. **Add a solved-status carve-out.** "Do not consult any source for the status
   or history" guarantees that an already-solved problem consumes the whole
   budget.
5. **Name a fallback for `[PROOF ASSISTANT]`.** Throughout this programme no
   Lean toolchain has been reachable, making the formalization gate unreachable
   and therefore silently dropped.

## The experiment worth running next

This one was underpowered by design and said so in advance. The informative
version needs a problem where arms actually diverge — one where a *plausible
but wrong* construction is available, so a false positive is a live outcome
rather than a hypothetical. The cheapest such design: a conjunction where three
conjuncts are satisfiable by a well-known object that fails the fourth in a way
that requires checking rather than recall.

And the arm that matters most is not in this experiment at all: **template +
separate auditor agent**, versus **template alone**. Phase U §8 and this phase
together suggest the whole value of the audit machinery sits in whether the
auditor is a different agent, and that is a one-line change to the orchestration
rather than to the prompt.
