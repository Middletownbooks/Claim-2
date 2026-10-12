# Brief C — answered twice, independently, by accident. The replication outranks the verdicts.

Two Sonnet 5.5 chat instances ran `prompts/s55/C_ARM1_CELLS.md` without knowledge of each other.
**This project has never had a replication of a registered brief**, and it is the first robustness
measurement available on any instrument here. Locally re-verified numbers in
`c_checks/verify_brief_c.py`, output in `c_checks/VERIFIED_OUTPUT.txt`.

Run 1 used **22 of 22** calls, 1 failed. Run 2 used **18 of 22**, 1 failed, and stopped early on a
constraint the brief did not anticipate (§6).

## 1. The verdicts: four of five agree, and the fifth splits on labelling only

| record | run 1 | run 2 | gate |
|---|---|---|---|
| **186** AP-free subsets | S1 **FAIL**, basis RECALL → sourced | S1 **FAIL**, basis RECALL → sourced | **agree** |
| **277** hypergraph Ramsey | CANNOT EVALUATE → **FAIL** | CANNOT EVALUATE → **FAIL** | **agree** |
| **353** even-cycle Turán | CANNOT EVALUATE → **FAIL** | CANNOT EVALUATE → **FAIL** | **agree** |
| **375** star discrepancy | **FAIL**, now established | **FAIL**, now sourced | **agree** |
| **385** Lieb–Thirring | S2 CE → **FAIL** | S2 **stays CANNOT EVALUATE** | **split** |

**Arm 1's 0 of 19 stands, and is now better founded than it was.** Three cells move from CANNOT
EVALUATE to FAIL and 186's FAIL loses its `RECALL` basis. **Nothing was resurrected.**

## 2. The replication result: the evidence bases are nearly disjoint and the verdicts held anyway

Run 1 opened Wikipedia (Salem–Spencer), Gasarch–Glenn–Kruskal, Hunter (2401.16106), Bloom–Sisask
(2309.02353), Conlon–Fox–Sudakov (0808.3760), erdosproblems.com/564, Füredi–Naor–Verstraëte,
Ostromoukhov (MCQMC), Bilyk–Lacey, Levitt (1206.1473), Read–Schulz (2609.10478).

Run 2 opened Elsholtz–Hunter–Proske–Sauermann (2406.12290), Mubayi–Suk (1707.04229),
Füredi–Simonovits (1306.5167), Pillichshammer (1904.10346), Schimmer (2203.06051), Levitt
(1206.1473), Read–Schulz (2609.10478).

**The overlap is two sources out of sixteen.** Every question was answered from a different paper:

| question | run 1's source | run 2's source | same conclusion? |
|---|---|---|---|
| Q1 | Hunter — the 9/32 torus block, *c* ≈ 0.9567 | EHPS — the 7/24 block, *C* = 2.6665 vs Behrend's 2.828 | **yes**, and the two papers are the same research line one step apart |
| Q2 | Conlon–Fox–Sudakov | Mubayi–Suk survey | **yes** |
| Q3 | Füredi–Naor–Verstraëte | Füredi–Simonovits survey | **yes**, and both independently reach the Feit–Higman restriction *k* ∈ {2,3,5} |
| Q4 | Ostromoukhov + Bilyk–Lacey | Pillichshammer | **yes on the order**; run 1 additionally found a positive *constant* lifting run 2 missed |
| Q5 | Levitt | Levitt + Schimmer | **split**, see §3 |

**Four verdicts survived a near-total change of evidence base.** That is the strongest statement
available about this instrument, and it is worth more than any of the four.

**Two things both runs did unprompted and identically**, which is itself evidence the brief's design
is doing the work: both built a finite-difference control on the Lieb–Thirring equality case to show a
bare float certifies nothing, and both independently flagged that Q2's and Q4's record labels each
cover several different quantities.

## 3. The Q5 split, and it exposes a defect in a registered prediction

Both runs opened **exactly one** of the four numerical studies (Levitt) and both hedged in prose in
almost the same words. They differ only in whether they converted that into a verdict:

> **Run 1:** *"NO at the level reached … Absolute absence is UNRESOLVED, since two searches and one
> opened numerics paper do not exclude an interval-arithmetic paper I did not surface."* → **S2 FAIL.**
>
> **Run 2:** *"UNRESOLVED, leaning NO … I opened one of the four numerical studies, so a NO would be
> unearned."* → **S2 stays CANNOT EVALUATE.**

**Under the brief's own rule 1 — "a bar you cannot evaluate counts as FAIL, not unscored" — these land
in the same place.** The gate outcome is identical. So the rule, which exists to stop hedging,
**also erases the difference between an established absence and an absence the run says it did not
earn.** Run 2's is the more disciplined answer and the rule gives it no credit.

**And that breaks P-31 A-1's threshold.** A-1 reads: *"if one or more of the four queued promoting
searches … issues a verdict on a bar the run could not actually evaluate, A-1 is FALSE."* Rule 1
instructs runs to do exactly that. So:

* if returning CANNOT EVALUATE is **not** issuing a verdict, run 2 complies and run 1 arguably breaks
  A-1 — for obeying the standing rule;
* if CE **is** a verdict (rule 1 says CE = FAIL), then **every** run that ever hits an unevaluable cell
  breaks A-1, which cannot be the intent.

**Neither reading is usable, so A-1 is not evaluable as worded.** Registered as **D54**. Per D44 the
threshold is **not redrawn** — recorded as a defect, and A-1 stays OPEN.

**Brief C is not in P-31's reserved slice** (U13 D1, the D-optimal transfer item 1, 239's two risks,
345's read), so none of this scores A-1. Scoring a metric against a slice nobody reserved is D45's
failure and P-31's own outcome field cites it. This is additional evidence only.

## 4. The two apparent numerical disagreements, both re-checked here, both non-disagreements

**Q3, the C₁₀ constant.** Run 1 gives 0.5919, run 2 gives 0.5798. `PRIMARY-VERIFIED-LOCALLY`: both
arithmetics are correct. Run 1's is *c*₅/2 from the amplification formula
*c_k* = 2*k*(√(*k*+2)−2)/((*k*−2)(√(*k*+2)−1)^(1+1/*k*)), giving *c*₃ = 1.0677, *c*₄ = 1.1305,
*c*₅ = 1.1839; run 2's is 4/5^1.2 from vertex duplication of the girth-12 graph. **Different
constructions, not a contradiction — and run 1's bound is the stronger one.** Neither run mentions the
other's. Both agree on C₆ to four digits (0.5338/0.5339 against my 0.5339).

**Q5, the Lieb–Thirring equality case.** Run 1 states the product = 0.2500000; run 2 states the ratio
= 0.2450351. **These are the same statement twice.** Verified: maximising the Pöschl–Teller ratio
|*E*₀|/∫*V*^(3/2) over *V* = *a* sech²*x* gives λ = 1/2, hence *a* = 3/4, |*E*₀| = 1/4,
∫*V*^(3/2) = 1.0202621, and the ratio is **0.2450351 = 4/(3√3π) exactly** (asserted, passing). Both
runs are right and 2/√3 = 1.1547005 checks.

**One thing neither run supplied, and it is a one-line proof.** Both establish α < 1 empirically. It is
immediate: α(*M*) = ln *r*₃(*M*)/ln(2*M*−1) and *r*₃(*M*) ≤ *M* < 2*M*−1, so **α < 1 identically**, for
every *M*. The product lemma is verified here with a negative test (base 2*M*−2 permits carries and
breaks the lift in **14 of 26** cases — and run 2 independently reported "14 of the 27 sizes
tried", the same count), and the maximum of α over *M* ≤ 30 is exactly log₃2 = 0.63093,
attained at *M* = 2, 5, 14 — which are (3^*k*+1)/2, the base-3 sets themselves. Both runs found that
too.

**The control both runs invented, reproduced.** A 3-point finite-difference solve gives
|*E*₀| = 0.25001145, **overshooting the sharp value 1/4 by 1.1 × 10⁻⁵**, because the discrete
Laplacian underestimates kinetic energy — confirmed here by a separate infinite-well control returning
0.999980 against an exact 1. Both runs reported the same effect at the same order and drew the right
conclusion: a floating-point value cannot certify a bound claimed sharp.

## 5. Corrections to my brief, and two of the three are replicated

* **My arXiv mechanic is wrong.** §"Fetch mechanics" says a September 2026 identifier was refused
  three times. **Both runs opened `arxiv.org/html/2609.10478` on the first try.** The refusal is
  **PDF-specific, not date-specific** — run 2 says so explicitly. Replicated; the brief's rule should
  say "try the HTML rendition before spending a retry."
* **A fourth failure cause, and both runs hit it on the same call.** arXiv 2607.23571 returned *"empty
  or no machine-readable text"* — not a rate limit, not robots, not an unsurfaced URL. Both correctly
  classified it as distinct and neither retried. Replicated, so it is real.
* **Unreplicated, from run 2 only:** the fetch tool's token-limit parameter was not honoured on PDFs —
  four calls returned whole documents. Run 1 did not report this, and it is the likely cause of §6.

## 6. The binding constraint was not the one I capped

**Run 2 stopped at 18 of 22 calls**, stating: *"I'm stopping fetches here, since further large PDFs
risk swamping the report."* Run 1 spent all 22.

**My cap measured calls; the constraint that actually bound was context.** Two runs of one brief hit
two different limits, and the brief's whole budget apparatus — raised from 15 to 22 on a measured
call-failure rate — was calibrated against the wrong resource. Registered as **D55**. Note the cap was
not the problem: run 2 self-limited correctly and said why, which is the behaviour the partial-report
rule asks for. The problem is that the brief gave it no vocabulary for the limit it actually hit.

## 7. S1's clause cannot tell a constant from an order, and both runs had to say so

Both runs report **two readings** of S1 rather than choosing, and independently:

* **Q1.** A published lifting exists — Behrend-type torus blocks — but it moves the **constant inside
  the exponent**, not the order. Run 1: *"If a finite-description torus block counts … S1 flips to
  PASS on that quantity."* Run 2: *"Read literally as 'a lifting theorem exists', S1 would pass, but
  it cannot move the headline."*
* **Q4.** Run 1 found a genuine finite→asymptotic-constant lifting in *d* = 1 — Ostromoukhov's base-60
  permutation giving 0.222223 against Faure's 0.223585, an improvement of **0.61%** — and notes arm 1
  was asking about the order.

**So S1 COUPLED as worded is satisfied by theorems that cannot move the headline.** The `STRENGTH`
field added to the dispatch version is what surfaced this, and it worked: run 1 classifies its own Q1
finding as *"weaker than the known bound"* and its Q4 finding as *"−0.61%"*. **A gate clause that
passes on a 0.61% constant is not measuring what the board wants.** Recorded, not fixed.

## 8. D50 is confirmed and simultaneously defused

D50 held that six consecutive S3/tier failures might be measuring our access rather than the cells.
**The access remedy has now been applied three times — Costas, and these five arm-1 cells — and every
single cell died anyway, on evidence.** Access was real and it was not hiding survivors. D50's worry
was legitimate and its implied hope was not. Updated there.

## 9. One error of my own in the verification

My first finite-difference solver used a power-iteration shift of 2/*h*² + 1, below the discrete
spectrum's top of ≈ 4/*h*², so it converged to the **largest** eigenvalue and returned a *positive*
energy for a bound state. Caught by the sign, which is impossible. Fixed by solving the tridiagonal
problem directly and adding the infinite-well control. **Third hand-built control of mine to be wrong
in three consecutive documents**, after the order-4 Costas array and the dimension-3 cap — and the
third caught by a check rather than by review.
