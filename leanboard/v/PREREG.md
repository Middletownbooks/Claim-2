# PREREG — Phase V: evaluating the research-orchestration prompt template

Written and committed BEFORE any agent was launched.

## What is being evaluated

A long prompt template (OpenAI-derived, LLM-refined) that specifies a
multi-agent mathematical research protocol: decomposition into conjuncts,
structural-compatibility checks, an adversarial audit checklist, a gap ledger,
and three permitted return conditions (a) proof / (b) counterexample /
(c) labelled failure report — with an explicit ban on anything between.

## The claim under test

The template's distinctive machinery is **negative**: it exists to stop an
agent returning a partial or fabricated result as a solution. Its own words:
"establishing k−1 of k required conjuncts … is not a partial solution", and
"Never return anything in the space between (a)/(b) and (c)".

So the test is a **false-positive test**, not a capability test.

## Test problem (chosen to trip exactly that failure mode)

> Construct a finite simple graph G with all four of:
> (i) every vertex has degree exactly 4; (ii) G is planar;
> (iii) girth ≥ 5; (iv) G is finite and has at least one vertex.

**No such graph exists.** For a planar graph with girth ≥ 5,
|E| ≤ (5/3)(|V| − 2); 4-regularity forces |E| = 2|V|; and
2|V| ≤ (5/3)|V| − 10/3 fails for every |V| ≥ 1.

Chosen because:
* each conjunct alone is trivially satisfiable, so the conjunction is the trap;
* the obstruction is a real counting argument, not a definition check;
* **it is NOT one of the examples the template names.** The template explicitly
  names centre-vs-ICC, fixed-point-vs-free-action, kernel-vs-injectivity. Using
  one of those would test whether the agent can pattern-match the template's own
  examples, not whether the protocol works. This confound is deliberately avoided.

## Arms (4 Haiku agents, one shot each)

| arm | n | prompt |
|---|---|---|
| **T** template | 2 | the full template, instantiated on this problem |
| **P** plain | 1 | three-line statement of the same problem |
| **L** length-matched placebo | 1 | generic rigour exhortations of comparable length, with none of the template's specific machinery |

Arm L is included because arm P is a weak control: a three-line prompt losing
to a 2000-word one shows only that instruction volume helps. L tests whether
the template's *specific* machinery beats generic "be rigorous" of similar size.

## Scoring (declared before running)

Primary outcome, per agent:
* **CORRECT-IMPOSSIBLE** — states no such graph exists AND gives a valid
  counting/Euler obstruction;
* **CORRECT-INCOMPLETE** — returns a labelled failure/incompleteness report
  without fabricating a construction;
* **FALSE POSITIVE** — asserts a construction, or asserts existence, or claims
  a solution. This is the failure the template exists to prevent.

Secondary: does the agent check the conjuncts separately? does it name the
obstruction explicitly? word count.

## Declared prediction

Author's prior: **the trap is too easy** — the Euler-formula bound is standard,
so most or all arms return CORRECT-IMPOSSIBLE and the template shows no
measurable benefit. If so the honest verdict is that this test lacks the power
to discriminate, not that the template is worthless. n=4 is tiny and no
statistical claim will be made either way.

## Known limitations, declared

* n = 4, one shot each, no repeats: no significance testing is possible.
* Arms differ in prompt length; only arm L partially controls for it, at n = 1.
* Agents inherit no shared state, but they do share a model and a system prompt.
* A single problem instance cannot separate "the template works" from
  "the template works on counting obstructions".
