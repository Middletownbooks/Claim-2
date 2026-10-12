# Best first target among the 499, after the sweep — and who should run it

## 1. The screens that survived

Three, and only three came out of the sweep with anything behind them:

1. **Breadth, not depth.** *Specialists saturate depth; they do not saturate breadth.* This is
   the only screen on the board with a demonstrated win behind it, and after
   `HOA64_ASSESSMENT.md` that win rests on **13 matrices verified here in exact arithmetic**
   rather than on a press report.
2. **Unworkspaced.** Playable records are workspaced 46% against a 25% baseline, so
   *playable ∧ unworkspaced* is the scarce intersection — 19 records of 499.
3. **FEASIBLE**, i.e. the witness is reachable at reachable scale, not merely finite.

The sweep also removed candidates rather than adding them: **287** and **472** are theorems at
ℓ=2 (no counterexample exists to find), **355** never reduced to snarks, **295** and **335** are
explicitly *deep*, and **331** is now an active programme of yours rather than an opening.

## 2. Applying them

FEASIBLE ∧ unworkspaced leaves five: 132, 235, 280, 401, 495.

| rank | why it does or doesn't survive |
|---|---|
| 132 congruent number | **out.** Mechanism class `d`: a rational point settles *an n*, the ranked target is a characterisation. `FEASIBILITY.md` §3(d) flags exactly this inflation |
| 495 list edge-colouring | depth — one exhaustive generation pipeline over small multigraphs |
| 401 KL combinatorial invariance | depth — one pipeline, and heavily worked with ML assistance already |
| 280 Kaplansky idempotent | **the sweep demoted it.** The chain is unit ⇒ zero-divisor ⇒ idempotent; Promislow's group satisfies zero-divisor, so Gardam's counterexample gives nothing free; the live object is **zero-divisor**, and a Bar-Ilan AI-algebra lab is already pointed at it |
| **235 Zauner / SIC existence** | **the pick** |

## 3. Why 235

- **Highest breadth re-rating of anything not already demonstrated** (`FEASIBILITY.md` §6 moved
  it 20% → ~35%): *many dimensions, each a fiducial search plus integer-relation recovery.*
  That is structurally the Hadamard shape — a hundred small independent searches, each cheap.
- **Unworkspaced**, so inside the scarce intersection.
- **The witness is a finite object with an exact check**, and the check is verified here, not
  asserted. A fiducial ψ ∈ ℂ^d satisfies |⟨ψ, D_{jk} ψ⟩|² = 1/(d+1) for every
  (j,k) ≠ (0,0), with D the Weyl–Heisenberg displacement operators:

  ```
  d=2 known fiducial          SIC fiducial = True   max dev 5.00e-16
  d=3 known fiducial          SIC fiducial = True   max dev 3.33e-16
  d=3 basis vector (control)  SIC fiducial = False  max dev 7.50e-01
  cost of one full check at d=100 (9999 overlaps): 14.0s
  ```

  The control fires, so the check has teeth. Arm AV's (A)/(B) split applies cleanly: *this
  vector is a fiducial* is decidable in seconds; *this dimension was open* is literature.
- **The hard half is a pipeline, not an insight.** Numerical fiducials are the easy part; the
  work is **exact** recovery — high-precision numerics → integer-relation (PSLQ/LLL) → exact
  verification in a number field. That is bookkeeping at scale, which is the breadth claim.

## 4. The gate, and I am putting it first because I just paid for skipping it

**Do not start until one frontier lookup is done: which dimensions d have *exact* fiducials,
and are the remaining gaps scattered or a clean prefix?**

The entire case above rests on the gaps being scattered. If exact fiducials are known for all
d up to some bound and unknown above it, this is **depth** — specialist compute at the frontier
— and the re-rating is wrong, exactly as "has this been worked?" was wrong about Hadamard in
the other direction.

I have no business asserting which d are open: that is a *frontier* fact, and this project
measured that frontier recall is systematically stale and reads confident. One line of
arithmetic would have killed my W(103) route a day early — **W(m) ⇒ H(4m), so check whether 4m
was open** — and I had the data in hand and didn't run it. This is the same check, one target
later. Run it first.

## 5. Executor: Claude Code, with the LLM confined to the gate

Opposite weighting to the frontier sweep, and for a reason that is about the work rather than
about cost:

| step | who | why |
|---|---|---|
| §4's gate — which d are exactly known, scattered or prefix | **LLM** with search | pure lookup-and-quote, one afternoon, no filesystem needed |
| high-precision numerical fiducial search per d | **Claude Code** | long-running mpmath jobs, checkpointed to disk, parallel over d |
| exact recovery (PSLQ/LLL → number field) | **Claude Code** | iterative, tooling-heavy, needs to keep and re-read intermediate precision |
| the witness check | **Claude Code** | exact arithmetic that must be *run*; §3 above is that check already written |
| write-up and provenance | **Claude Code** | the artifact is a repo of verified fiducials plus the harness |

The decisive argument is this session's own record. Twice now — my "W(103) FOUND in 0.1s" and
the ANNOUNCED-UNVERIFIED downgrade that the actual matrices overturned — **reasoning about
whether a finite object exists produced a confident wrong answer, and running the check settled
it in seconds.** SIC fiducials are the same kind of object. Put the execution where the checks
can be run and the intermediate state survives, and give the LLM the one genuinely
literature-shaped step.

## 6. What would make me change the pick

- The gate comes back "clean prefix" → 235 is depth; fall back to **495** (list edge-colouring,
  small multigraphs, directly computable) and re-run this ranking.
- The Bar-Ilan zero-divisor work publishes a negative result or stalls → **280** returns, because
  the idempotent search genuinely has nobody on it, and *that absence is still the finding*.
