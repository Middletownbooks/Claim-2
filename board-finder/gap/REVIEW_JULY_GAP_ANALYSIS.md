# Review of the July 2026 gap analysis

Checked against what this project has since measured. The response is good work — better
than its own ranking table admits — and it has one rubric defect that would have sent us
where we in fact went.

## 1. What I verified here rather than relaying

| claim | check | result |
|---|---|---|
| Kalai: cube attains 3^d nonempty faces exactly | Σ_k C(d,k)·2^(d−k) for d = 1…6 | **3, 9, 27, 81, 243, 729** — exact at every d |
| Tuza: K₄ and K₅ are exactly tight | exhaustive ν and τ | K₄: ν=1, τ=2. K₅: ν=2, τ=4. **τ = 2ν both** |
| MDS: Ball's k ≤ 2p−2 is vacuous at p = 2 | 2p−2 = 2 < 3 | **correct, and a genuinely sharp observation** |
| Kaplansky family nesting | unit ⇒ ZD ⇒ idempotent | **correct, and it breaks the response's own D score — §2.1** |

Every tightness signal the top candidates rest on is real. The analysis is not hand-waving.

## 2. Four defects, in descending order of consequence

### 2.1 Dimension F is the trap we walked into, written into the rubric

F rewards *"does generalizing to more variables, higher dimensions, or larger parameters
plausibly loosen the constraints."* That is exactly the property that made **Zauner/SIC**
look attractive to us and it is exactly why it was worthless: many dimensions, each an
independent search, maximal F — and the unknown set is an **unbounded tail at an actively
worked frontier**.

Compare Hadamard: identical surface shape — many orders, each an independent construction —
and a **good** target, because its unknown set is *thirteen numbers*.

**F as written cannot distinguish those two.** The distinguishing question is not "does the
parameter space loosen" but **"can the unknown set be written down?"** A finite list below a
ceiling is a target; a prefix plus an open tail is a frontier you arrive at late. This is the
single most consequential fix, and the v2 prompt replaces F with it.

### 2.2 Kaplansky ZD is over-scored at D = 5, and the response carries the disproof

The justification is *"the unit conjecture — same problem family, same witness shape, same
group — was disproved by Gardam in 2021… the best possible D signal."*

The family nests **unit ⇒ ZD ⇒ idempotent**, so the unit conjecture is the **strongest**
statement and therefore the **easiest to refute**. Gardam refuted the easiest member. ZD is
strictly harder, and the response's own cited bound is the quantitative form of exactly that:
|supp α| = 3 forces |supp β| ≥ 20 over 𝔽₂. An adjacent success on a *stronger* sibling is
weaker evidence than the same success on a weaker one, and D = 5 does not distinguish them.

This error mode recurs in this family: our own `REPORT_SWEEP.md` §6 got the same direction
backwards on the third member (idempotent), and `GATE_RESULT_SIC.md` §5 corrects it with
witnesses. **Standing note: whenever a fallen sibling is cited as precedent, state the
implication direction and say whether it makes the target easier or harder.**

### 2.3 The ranked table mixes verified and unverified status

20 of 31 rows are `[?]` — training-data recall, unconfirmed. Positions 8, 9, 11, 13–16,
18–26 and 28–31 are therefore **rankings of unknown-status problems**, presented in one table
with the 11 that were checked. §4 says this plainly, which is to the analysis's credit, but
the table is what a reader acts on.

We now have a measurement of what that costs. The SIC gate's respondent reported that its own
unsourced recall would have produced *"an entirely fictitious hole list"* — nine years stale —
and separately upgraded a numerical bound to an exact one. In a field the response itself
measures at **~40 AI-resolution claims/month**, unverified status is not a soft caveat.

**Fix: score only verified candidates. Unverified go to a separate unscored pool** with the
searches needed to promote them.

### 2.4 No premise-falsification step

Nothing in the rubric asks: *what one-line check would kill this candidate before any compute
is spent?* Our cost for that omission is on the record — I spent a day on a Cooper–Wallis
route to H(2060) that one line of arithmetic kills (**W(m) ⇒ H(4m), so check whether 4m was
ever open**; 716 and 892 were, so the Williamson matrices needed cannot exist). I had the data
in hand throughout.

Every candidate should carry that line explicitly, and it should be run during triage.

### 2.5 Minor: "exhaustively searched" is one field with three states

Dimension E treats prior search as a scalar. It has three distinct states, and only the first
lets you know what was covered: **searched and published with artifacts** (Černý binary n ≤ 12,
~100 CPU-years — the response's own best example); **searched and asserted** without public
code or data; **not searched**. The SIC gate found the analogous gap in a construction
setting: results claimed in print with the data nowhere public.

## 3. What I would keep verbatim

Three things the response got right that I would carry into any successor:

1. **Anti-criterion E applied at the level of *lists*, not problems.** *"Anything on a numbered
   public list of the kind an agent can enumerate should be assumed contested."* That is a real
   finding, it is why the candidates were drawn from the named-conjecture literature, and it is
   the reason this whole exercise is worth redoing rather than replaced by mining the 499.
2. **Freshness as a measured decay rate, not a vibe** — ~40 claims/month, 247 logged — with the
   derived rule that any candidate must be re-checked *immediately* before work starts.
3. **Refusing to score freshness numerically**, for the stated reason: averaging it in would let
   a stale-but-attractive problem outrank a fresh one. Correct, and correctly argued.

And the Fuglede warning — *"one of my strongest initial candidates may have fallen 11 days
ago"* — is the decay rule demonstrated on its own output, which is the most useful single
paragraph in the document.

## 4. The exclusion that was right, and that we re-derived the hard way

The response **excluded** Zauner/SIC-POVM, Hadamard matrices and the projective plane of order
12, on the grounds that they are *existence* claims whose refutation needs exhaustive
non-existence proofs.

That is correct, and our `playability/` work spent two days independently arriving at the same
place from the other side: those problems are **construction** targets, not counterexample
targets. The witness polarity is opposite — *exhibit an object that is conjectured to exist*
versus *exhibit an object violating a universal claim* — and both are one-directionally
checkable, which is why both are tractable and why the July rubric's exclusion is a scoping
decision rather than a judgement of difficulty.

**So the two programmes are complementary, not competing**, and the v2 prompt makes witness
polarity an explicit declared field instead of an exclusion. That is the main structural change
besides replacing F.
