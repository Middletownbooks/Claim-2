# What orchestrated agents should be pointed at, and the three checks that decide it

*Priority 2 of two. Built from failures this project has already observed, not from
a hopeful pipeline. Benchmark: `benchmark.json`.*

## 1. Point them at verification and at invariants, not at boards

Two facts from `leanboard/ab/REPORT_AB_metagame_corpus.md` settle the target:

* **4/4 independent convergence on the same board.** Board-finding is the abundant
  step; spending agent budget there buys what four models produce unprompted.
* **arXiv:2609.11189 credits its proof to an automated research agent** — and the
  report's own conclusion is that *"a human programme's edge moved entirely to
  verification."*

So the two jobs worth orchestrating are **proposing candidate conserved
functionals** for an ACCUMULATION board (`FINDER.md` §2) and **verifying a fresh
claim at its load-bearing step**. Both are narrow enough to score.

## 2. The three checks, each from a specific observed failure

### Check 1 — enumeration completeness (from the Horn 1 failure)

A no-tools response asserted that any certificate certified by smooth/analytic data
and closed under the convolution *"forces the certificate to factor through the
subgaussian comparison"*, hence a Θ(√log) floor, and built a **negative verdict** on
it. Guo–Fang–Lu's class — densities of bounded directional total variation — is
analytic, closed under the transform, and reaches O(1). The counterexample was on
arXiv **five days before the response was written**. Inspecting the argument: it
enumerates MGF majorants, moments, log-concave relaxations and Gaussian-measure
comparisons, then asserts all smooth certificates reduce to those. *"The word
'forces' carries the entire argument and is unsupported."*

**The check, as a required output field.** Any claim of the form *no certificate of
this kind can work* must carry: (a) the enumerated class, listed; (b) **one named
functional outside it**; (c) the argument that the class is closed. A claim missing
(b) is not a negative result, it is an unchecked quantifier. Directional total
variation is an L¹ derivative norm — not a moment functional, not a function of Σ —
and would have failed Horn 1 immediately.

This is mechanisable and it is the single highest-value check in the set, because
impossibility claims are what stop a search.

### Check 2 — rank by load-bearing weight before checking anything (from the verification asymmetry)

A tool-enabled response ran a Monte Carlo on the seed-density constant across seven
dimensions and reported it independently verified. **Reproduced exactly** — and the
quantity has a closed form the response missed: Tᵢ = t₃/√3, so Var(Tᵢ) = 1 exactly,
so the claimed bound √(2/π) **is** E|N(0,1)| and the claimed asymptotic tightness is
just the CLT. Meanwhile the same response correctly flagged that it could *not* check
the crux. *"The checking was sound; the selection of what to check is where the
information was lost."*

**The check.** Before any verification runs, the agent emits a ranked list of the
claim's steps with, for each, *what fails if this step fails*. Checking proceeds from
the top. A run that verifies only steps below the crux reports **coverage 0 on the
load-bearing step**, not a pass. This is the `abstention.py` discipline — a branch
earns the right to extrapolate only where it reproduces what it covers — applied to
proof steps instead of data points.

### Check 3 — ask the agent whether its candidate relocates or removes the obstruction (because they answer honestly)

Three of the four responses **correctly reported that their own novel candidate
relocated the obstruction rather than removing it** — one exhibiting two explicit
counterexamples against its own invariant, one finding its cross term reduced to
affine spectral independence *"verbatim, not a relabeling"*, one running an
experiment that falsified the monotone version of its own board. That is a
capability, not a hope: make it a required field and the honest negative arrives for
free. The one response that produced the most polished artifact is also the one whose
impossibility claim was false, so **polish and reliability were anticorrelated in
this corpus of four.**

## 3. The roles, and what each is allowed to conclude

| role | input | output | may conclude |
|---|---|---|---|
| **proposer** | a before-board with `leak_kind = ACCUMULATION`, and the class list of functionals already refuted | k candidate functionals with, for each, the conservation claim under the move | nothing on its own |
| **adversary** | one candidate | either a counterexample to conservation, or a pass on the test battery | that a candidate is dead |
| **enumerator** | the refuted-class list | the updated list, and for any impossibility claim, Check 1's fields | that a claim is *not yet* a negative result |
| **ranker** | a fresh paper's argument | Check 2's ranked steps with failure consequences | what to check first |

Ties and disagreements go through `stages/disagreement.resolve` with a declared
probe reserve (no silent tie-breaks); extrapolation beyond checked steps goes through
`stages/abstention` (no silent extrapolation). Both already exist and were built
before the experiments that needed them.

## 4. Build the benchmark before the pipeline

This project's own rule. `benchmark.json` holds it: **five ACCUMULATION boards whose
conserved replacement is already known**, scored on whether a proposer names the
actual functional — or one an adversary cannot kill.

| board | the degrading invariant | the conserved replacement that worked |
|---|---|---|
| K1 Banaszczyk → K3 Guo–Fang–Lu | Gaussian measure ≥ ½, degrades per move | directional total variation, **preserved exactly** |
| case 2 cap set | density increment, 1/δ rounds × one dimension | slice rank, one shot, no iteration |
| case 4 Kadison–Singer | tr exp sums n blocks → log n | interlacing families: largest root of a direct sum is the **max** over blocks |
| case 8 Spencer | union bound over n sets → √log n | entropy / partial colouring |
| case 9 Vinogradov | log k rounds × fixed fraction | efficient congruencing: all scales simultaneously |
| case 13 PCP | k-fold repetition → nᵏ | graph powering with constant-factor blow-up |

Scoring is blind in the only way that matters here: the proposer sees the
before-board and the leak, never the after-board. Six items is small, and it is six
more than a pipeline with no benchmark has.

**Not runnable in this session** — no `ANTHROPIC_API_KEY` and no model access, which
is the same wall the P2 pilot has hit since the start (debt D18). What is finished is
the part that does not need a key: the items, the blinding rule, the scoring rule,
and the three checks. The harness to run it against models already exists in
`proof-protocol/p2-ablation/`, fidelity-tested against the published artifact's own
JavaScript, with two judge families and a defect of the original instrument found and
fixed.

## 5. What I would not orchestrate

* **Board-finding.** 4/4 convergence says it is not scarce.
* **Anything producing a polished write-up as its deliverable.** In the corpus of
  four, the most polished artifact carried the false impossibility claim, and the most
  experimentally honest response *"hit a tool limit and never produced its
  deliverable."* Score the checks, not the prose.
* **Impossibility claims without Check 1.** They are the one output that can stop a
  search, and the one the corpus shows is least reliable.
