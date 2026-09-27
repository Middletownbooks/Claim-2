# Gate — ideal PTE solutions in the unsearched imaginary quadratic rings

**Bars registered 21 Sep 2026, before any of the measurements below were run.** Every bar is a
**single threshold with no gap**, because the last gate this project wrote (A-4) was two-sided
with an unregistered middle and declined to score — D44.

Each gate below states what PASS means, what FAIL means, and what happens next in each case.
A gate that cannot be evaluated counts as FAIL, not as "not scored": this is a go/no-go before
any build, and the default is no.

## The target

Coppersmith–Mossinghoff–Scheinerman–VanderKam 2024 §6 searches for symmetric ideal PTE solutions
over the rings of integers of Q(i√d) for **d ∈ {1, 2, 3, 7, 11, 19}**, and says: *"we need to use
one of Q(i√d) with d ∈ {1, 2, 3, 7, 11, 19, 43, 163}. We concentrate here on the first six such
fields."* Algorithms 6.1 and 6.2 are published in full.

So the candidate is: **run their published algorithm in the rings they did not.**

## G0 — the public-list check, at step 0

`RESULT_GAP_v2.md` §4 established this belongs first, not last. The four known agent-facing
databases are FrontierMath: Open Problems (all 41 unsolved entries transcribed at
`../../gap/sources/EPOCH_UNSOLVED_LIST.md`), TheoremDB, Horizon/HorizonMath, erdosproblems.com.

> **PASS** iff the target collides with nothing on the Epoch exclusion set under
> `../../gap/epoch_gate.py`'s screen-and-adjudicate discipline.
> **FAIL** → stop; it is somebody's benchmark item.

## G1 — is it actually unsearched, and is the list of rings right?

> **PASS** iff the set of imaginary quadratic fields with class number 1 is exactly
> {1, 2, 3, 7, 11, 19, 43, 67, 163} and the paper searched a strict subset of it, leaving at
> least two rings untouched — verified here, not taken from the paper's own sentence.
> **FAIL** → the gap is smaller than advertised; stop.

Note before running: the paper's list has **eight** entries and the Heegner numbers are nine.
If that is right the paper omits one, and this gate is the place to establish it rather than
assert it.

## G2 — the premise-falsification line: is the object plausibly there?

The v2 rubric requires this during triage, and it is the gate that killed the Cooper–Wallis route
and the SIC target. The question: **is there evidence that symmetric ideal solutions occur in the
sparser rings at reachable size?**

Evidence available without any new search: Table 5 of the paper records 30 (ring, size) cells
searched across six rings, and the text reports every solution found. The rings differ in
density — the count of algebraic integers of norm ≤ H is ≈ 2π*H*/√|Δ|, so a large discriminant
means a thinner ring.

> **PASS** iff at least one solution was found in a ring with **|Δ| ≥ 11**.
> **FAIL** → every known find sits in the three smallest discriminants, and d = 43, 67, 163 are
> 4×, 6× and 15× thinner than the thinnest ring that has ever produced one. Stop.

**The confound is registered too, because it cuts the other way.** At equal *H* the thin rings
contain fewer lattice points, so they may simply have been searched less in the only unit that
matters. So the FAIL branch is only taken if it survives this: recompute each cell's coverage in
**lattice points** rather than in *H*, and FAIL only if the sparse rings were covered at least as
well as the dense ones in point terms and still returned nothing. If instead the sparse rings
were materially under-covered, G2 is **INCONCLUSIVE**, which counts as FAIL for the go/no-go but
is recorded differently, because it names a cheap experiment that would settle it.

## G3 — reachability

The question that killed PTE 11 over ℤ: can this project cover a region comparable to the
published one, or is it six orders of magnitude short?

> **PASS** iff matching, in d = 43, the largest lattice-point coverage the paper achieved at the
> same size *n* in any ring costs **≤ 10 container-hours** under a cost model derived from
> Algorithm 6.1 and this project's measured throughput.
> **FAIL** → same failure as PTE 11; stop.

## G4 — is the unknown set writable?

The third screen category, the one that separated Hadamard from SIC.

> **PASS** iff the open set is a finite list of (ring, size) cells below a stated ceiling.
> **FAIL** if it is a prefix with an open tail.

## G5 — publishable either way?

> **PASS** iff a null would extend a named published table rather than vanish.
> **FAIL** → only a find counts, and the find is improbable; stop.

## Decision rule, registered

**All five of G0–G4 must PASS**, and G5 must PASS, for this to become a target. Any FAIL stops
it, and the registered next move on a stop is the **Hadamard worklist at order 2284** — the same
fallback as `../PREREG_PTE11.md` §6, which is by now the only thing on this board that has
survived a gate.

Results are recorded in `RESULT_RINGS.md`.
