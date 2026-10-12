# The Zarankiewicz stall, answered — and it is a constraint shape none of our taxonomies has

**Source:** response document from the Opus 5 instance that worked Zarankiewicz, supplied by the
operator 1 Oct 2026. Tier `SECONDARY-RELAYED` for its measurements; this session ran none of its
searches. **Its probability model and every instantiated figure re-derive here** —
`verify_stall.py`, all assertions passing.

**This fills the register's last empty Part D cell**, and it fills it in Cycle 0's own requested
form: *"the binding constraint hit — stated as a formal proposition, not prose."* The document
states three propositions with proofs. Cycle 0 asked for that in July and could not get it; it took
one message.

---

## 1. The answer, and Cycle 0's dichotomy does not contain it

Cycle 0's shortlist said of this candidate: *"The register must establish whether it stalled on
compute or on the cyclic-order realizability theory. **If theory, Claude Code adds little and this
is dead.**"*

**Neither.** The document's own statement:

> *"The binding constraint in this program was the identification and correct characterisation of a
> **certified generator** — a source of instances whose truth value under the target predicate is
> established independently of any implementation of that predicate."*

The mechanism, formalised: let **P** be the predicate the source intends, **P̂_c** the predicate as
implemented under reading *c* of the source's definitions, **σ(B)** the chance a budget-*B* search
finds nothing when something is there, and **ε** the chance the implemented reading is the wrong
one. Then

> **Pr[success] ≤ (1 − ε)(1 − σ(B)) + εδ**, so **Pr[failure] → ε(1 − δ) > 0 as B → ∞.**

Elementary, and the force is in what it denies: **the two errors do not trade off.** σ falls with
effort and is measurable from inside the program. ε is reducible only by external information and is
**invisible from inside**, because it is perfectly correlated across the output — every witness is
wrong together or right together.

**So a program can watch its witness set grow, confirm internal consistency across all of it, and
learn nothing whatever about ε.** The document's remark is the sharp form: *"568 witnesses under an
unvalidated predicate are no stronger than one, and the appearance of strength is itself the
hazard."*

## 2. SPECIFICATION is a sixth constraint shape, and `D61`'s five do not cover it

`../register/REGISTER.md` §4.5 proposed splitting the gap by remedy: **FLOPS · ALGORITHM · THEORY ·
BREADTH · CONTEST.** This is none of them.

It is not FLOPS or ALGORITHM — compute was slack from four seconds in. It is not THEORY — no new
mathematics was needed, and the program had the definitions in hand from Session 1. It is not
BREADTH — *"Woodall's paper was retrieved in Session 1, and its content was correctly extracted"*,
and the one thing the text did not settle was settled by computation rather than more reading. It is
not CONTEST.

> **SPECIFICATION — does the implemented predicate match the intended one, and is there any way to
> tell?** Closed only by a *certified generator*: a procedure producing instances whose truth value
> under the target predicate is known a priori, independently of the implementation.

**What closes it is neither compute nor reading but a construction** — here, that random
straight-line drawings of K₄,ₙ in general position are good drawings, and a good drawing all of whose
K₂,ₙ sub-drawings attain their antidistance induces a tight and pseudo-tight set. **That guarantee is
geometric and independent of every checker**, which is exactly the property that makes it
discriminating.

**And it is cheap to run and expensive to find.** 5,789,743 K₂,₇ drawings in 240 s; 1,989,388 K₂,₄
drawings in 70 s. The document: *"The scarce resource was not its execution but its identification."*

## 3. Three findings that bear directly on this board's instruments

**(i) A one-sided control cannot reduce ε, and ours was one-sided.** Proposition 2, instantiated on
Woodall's own published fact that each antisum-79 (7,7)-set contains ≥ 10 non-pseudo-tight
(4,7)-subsets. Measured minimum over 201 regenerated sets: **`path` 14, `walk` 13, `both` 14 — all
pass.** The only validation the program had, blind to the error it carried for two sessions. It
bounded over-permissiveness; the error was over-strictness.

> **This is `D47` and `P-31` generalised.** The corollary is sharper than anything on our board:
> *"a control's having been passed carries no information about ε unless the control is known to be
> sensitive in the direction the error actually lies."* Deploy controls two-sided by default, never
> selected by expected failure mode.

**(ii) The certified generator carries its own specification error.** The first attempt was wrong —
*"random straight-line drawings of K₄,₇ are good drawings, hence induce tight sets"* failed 6 of 180.
The correct statement needs **pair-optimality**, because tightness quantifies over *shortest*
antipaths. Corrected: **1,586 of 1,586**, and among non-pair-optimal drawings **36 of 1,262** induce
non-tight sets, exactly as the corrected statement predicts.

> **The failure mode worth keeping:** an apparent checker failure against a generator is evidence for
> (ε > 0) **or** (ε_G > 0) and the program cannot tell which. Had it "fixed" the checker to satisfy
> the faulty generator, it would have converged on a wrong predicate **with a clean control record** —
> the document calls this *"the most dangerous available outcome, and one no amount of additional
> compute would have exposed."* Agreed, and it is the shape of `D53`.

**(iii) A correctly executed measurement of the wrong object.** Step 0 tested vertex-revisiting in
CO₇ when the objects live in CO₄: **0 revisits in 5.79 M trials**, correct and irrelevant. Redone in
CO₄: **265,991 of 1,989,388** drawings admit *only* revisiting walks. That is `A9`/MOLS(12)'s failure
again — a null about the wrong object — in a third independent setting.

## 4. The crossover, recomputed — and the document understates its own case

| quantity | value |
|---|---|
| hit rate at n = 7 | 568/46,812 = **1.213%** |
| ε, three readings, diffuse prior | **⅔** |
| δ, measured after the fact (118 of 155 survived the correct reading) | **0.761** |
| **ε(1 − δ)** | **0.159** |
| **crossover B\*** where σ(B) = ε(1−δ) | **151 samples**, ≈ **1.2 s** |

**The document says ~400 samples and roughly 4 seconds. The true crossover is earlier**, so its
arithmetic errs *against* its own thesis — compute stopped binding sooner than it claimed. Its
σ(2000) is quoted as 4×10⁻¹¹ against a recomputed 2.5×10⁻¹¹; immaterial, and noted only because the
figure is quoted. **Both discrepancies are in the self-penalising direction, which is the one that
costs an argument nothing.**

**And the document names its own luck, which is the part worth keeping.** δ ≈ 0.76 was not
guaranteed: *"Had the readings differed more sharply — had `path` and `walk` disagreed on 95% of
witnesses rather than 24% — Session 2's 155 candidates would have been almost entirely spurious,
with identical internal evidence."* The program's instinct that a 1.5% hit rate was *"too easy,
therefore suspicious"* was a correct intuition that happened to coexist with a favourable δ. It was
not protective.

## 5. The result, and what it does to K₇,₁₁ — which is not what I said yesterday

The program's output: **an explicit (4,6)-set that is pseudo-tight but not tight.**

**Checked against the paper, which this session now holds at PRIMARY tier**, and the document's own
framing needs one correction:

| Woodall, p.663 | what the (4,6)-set does |
|---|---|
| *"there may be some nontight sets that are also pseudo-tight, although **I do not know of any**"* | **answers it affirmatively.** Woodall explicitly allowed that such sets may exist; exhibiting one settles his open question rather than refuting him |
| *"I know of no counterexample to the conjecture that an (m,n)-set is **tight if and only if every (4,n)-subset of it is pseudo-tight**"* | **refutes it.** For m = 4 the only (4,n)-subset of M is M itself, so the conjecture predicts a pseudo-tight (4,6)-set is tight. This one is not |

**So: a refutation of a published 1993 conjecture, and an affirmative answer to the remark beside
it.** The document's *"refuting a 1993 remark and conjecture"* overstates the first half by one
word, and the correction does not weaken the result.

**And it reverses my recommendation from yesterday.** I closed the Woodall reading by writing that
Woodall's tight/pseudo-tight equivalence *"is the one question worth putting to a capable
instance"*, and that **if the equivalence holds, Theorem 6(c) mechanises the closing argument at
every case and the residual THEORY component disappears.** Two things wrong with that:

1. **It had already been answered**, by the instance I was proposing to ask. `D56` again, and this
   time after being caught on it four times the same day.
2. **The equivalence is false, so the residual does not dissolve — it is confirmed.** Theorem 6(c)
   stays sound (its proof does not use the conjecture), but it cannot be a *complete* closing
   device: there exist sets with *t* = 0 that are nonetheless not tight, so the augmented antisum
   gives no boost exactly where a hard case would need one. **The "one new closing theorem per case"
   residual at (11,7) is now evidenced rather than merely unexcluded.**

`H` still passes for K₇,₁₁ and the arithmetic in `WOODALL_1993_METHOD.md` §2e is untouched. What
changes is the risk attached to R: the ALGORITHM label stands, and the THEORY rider is heavier than
I left it.

## 6. What this session can give back — the document's own first falsifier

Its §11 lists, as the first thing that would overturn the result: *"If the `walk` reading is itself
wrong — if Woodall's text settles the convention against it — then ε was never reduced, only
relocated."*

**This session now holds the complete paper at PRIMARY tier, and the text does not settle it against
`walk`. It arguably settles it for.** Four observations, in order of force:

1. **Woodall never defines "path" anywhere in pp. 657–671.** The convention is genuinely open in the
   text.
2. **A shortest walk in an unweighted graph is always a path** — a repeated vertex admits excision of
   a closed section, giving a shorter walk. So for *P_ab*, which tightness **requires** to be
   shortest, the two readings **coincide** and the convention cannot bite.
3. **It bites only on *Q_xy***, which p.662 explicitly says is ***"not necessarily shortest"*** — the
   one object in either definition where walks and paths can differ. That localises the whole
   question to a single clause.
4. **Theorem 5's own proof constructs an antipath as a walk.** p.662: the crossing is opened out, *a*
   is replaced by *a₁* obtained by transposing adjacent elements, and *"iteration of this procedure
   yields the required path a, a₁, …, a_r = b̄."* Nothing in that construction excludes a repeated
   vertex, and Woodall calls the result a path.

**Observation 3 is the one to send back**, because it converts a global convention question into a
single-clause one and explains *why* the empirical test discriminated at all: the generator's
pair-optimal drawings are exactly the ones where *P_ab* is forced shortest, leaving *Q_xy* as the
only free object.

## 7. The count, and I am not making yesterday's mistake

**This is a candidate third external result for the programme**, after the Ochem–Zelinsky Algorithm 1
error and the Chow C(3) counterexample. **It is not being counted yet.**

`D58` records that I previously counted three and there were two, having split one piece of work
described from two sources. The discipline that failure bought: **a result enters the ledger when it
is verified here end to end, as the Chow counterexample was in `../rota/verify_ours.py`.** This one
is `OPERATOR-SUPPLIED` and its mathematics is in a file this session has not seen —
a file named *woodall-pseudotight-counterexample.md*, which lives in the other instance’s tree.

**To verify it needs exactly one thing:** the explicit (4,6)-set, as six cyclic orderings of 6
elements, plus the *Q_xy* system witnessing pseudo-tightness. Given those, this session can re-derive
pseudo-tightness and non-tightness from the definitions on p.662 — which it now holds — without
relying on the program's checker. **That is the same end-to-end standard the Chow result met, and
until it is met the count stays at two.**

---

*Arithmetic: `verify_stall.py`, all assertions passing. Paper: `WOODALL_1993_METHOD.md`, PRIMARY.
Register cell: Part D, Zarankiewicz — **filled**.*
