# What Phases X–AC imply for the meta-game

Three audits, one corpus study, one sieve build. The strategic reading.

## 1. The board layer has commoditised; verification has not

Four models and one automated agent, uncoordinated, found the same board
(measure/density state, convolution move). Nobody verified the one published
result. The tool-enabled model that *found* the paper relayed a second-hand
concern it could not evaluate; I evaluated it and found it probably misplaced.

Scarcity moved from having the idea to checking the thing.

## 2. Three artifacts, three distinct verdicts — the instrument discriminates

| artifact | verdict | mechanism |
|---|---|---|
| Ghermoul | conditional on a statement at least as strong | relocation, not reduction |
| auro-zera | the axiom **is** the open case; README lemma false | relocation, plus a refutable side claim |
| Guo–Fang–Lu | no error found; weight on 3 citations | genuine discharge into literature |

The decisive question every time was the same and took minutes: **is what you
reduced to weaker than what you are proving?** That question is not in the
original template. It is COVERAGE DIRECTION in v2.1 and should be promoted from
a §4 principle to the first check.

## 3. Empirical support and soundness have decoupled — a trap

I strengthened auro-zera's empirical claim ~6,667x and Ghermoul's 100x. Neither
moved toward a theorem. Guo–Fang–Lu has **no** empirical support available at
all — existential, no algorithm, nothing to run — and is the soundest of the
three.

So the three rank *oppositely* on empirical-testability and on soundness. The
natural strategy "use compute to test conjectures" is cheap, works, and measures
the wrong variable.

## 4. Impossibility claims are the highest-risk output class

Batch-1 Response 2's Horn 1 — smooth certificate classes have a provable
sqrt(log) floor — was the most confident claim in the corpus, carried its
NEGATIVE verdict, and is false, with the counterexample already on arXiv.

Asymmetry: a false possibility claim is refuted by trying; a false impossibility
claim is believed and closes the line. The clause that catches it —
DERIVATION DISCIPLINE (b), check against one small instance — has been in the
template since v1 and was skipped.

## 5. Template additions are not the bottleneck; execution is

v2.1's new clause fired correctly on two of three artifacts. But the corpus's
largest error would have been caught by an original-template clause that was
simply not run. Prompt engineering as a lever caps out below the level of
"does the model actually execute the check".

## 6. The honest limit of the instrument

"No error found" is not "correct". I could not verify Proposition A.1 against
Mosconi–Riey–Squassina; that needs a specialist, not compute. And this session
overturned two of my own headline findings (the Phase U ledger; the i=4
explanation). The demonstrated capability is *catching arithmetic and structural
errors*, not certifying correctness.

## 7. Tiering, with an expiry date

* **Tier 1, commoditised:** finding boards, generating candidate proofs.
* **Tier 2, currently scarce and machine-amenable:** exact reproduction of
  published computation, cheap orders-of-magnitude extension of empirical
  claims, relocation-vs-reduction sorting, capture-artifact detection.
* **Tier 3, scarce and not yet machine-amenable:** specialist judgment on deep
  external dependencies.

The edge is Tier 2 and it is temporary. Across Phases P–U this programme found
essentially no new mathematics; every positive result was a negative result
about a hypothesis. That is the comparative advantage, and it argues for
building the instrument rather than the theorem.

## 8. The behavioural datum worth remembering

Given a published claimed resolution of the target problem, sitting unverified
for five days, **every model in the corpus generated a new board instead of
checking it** — including the two that had tools and had found the paper.
