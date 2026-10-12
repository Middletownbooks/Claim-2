# What openai/math changes here

**Intake of `github.com/openai/math` at `fd4aeeb` (7 Oct 2026), into a tree whose snapshots are
dated 9 Sep to 1 Oct.** Every number below is printed by a script in this directory or in
`../board-finder/gap/`. None is typed from memory. The mathematics is openai/math's claim
throughout. Where this tree checked something itself, it says so.

---

## 0. Headline

1. **This branch's live target was claimed closed, with a Lean proof, a week before the thread on
   it began.** The v4 thread worked cr(K₇,₁₁) from 30 Sep to 1 Oct. openai/math family 165 claims
   cr(K_{m,n}) = Z(m,n) for every m and n; its manuscript is dated 23 Sep and was published 6 Oct.
   Its Lean statement's definitions are identical to the challenge's, and **it compiles here** with
   only the standard axioms, in the first Lean run this project has made (`LEAN_CHECK_165.md`). See
   `../board-finder/gap/v4/CLOSED_BY_165.md`.
2. **79 of the 499 "open" problems in the ProofAtlas ranking this tree mines are claimed settled
   on their exact target.** That is 15.8%, from one lab in one release. **42** of the 79 carry a
   Lean statement that, by openai/math's own scope note, is the claim; **3** carry a weaker one;
   **34** are paper only. A further **51** records have a claimed sub-case or bound. In all,
   **130 of 499** records are touched.
3. **Four of the 25 live gap items are claimed settled** (C6, U11, V1, V2), and so is **record
   280**, which `../board-finder/playability/README.md` calls the board's strongest single
   target. It is claimed *refuted* in characteristic 2 (paper only) and *proved* in characteristic
   0 (formal).
4. **The instruments that kill a target on its own mathematics were right. The crowding screens
   were not.** C6's premise-falsification line and U11's polarity step had already demoted both
   items before the claimed proofs were public. V2 passed the crowding checks it was put through and
   was the one that had been closed. §6 is the argument that this is a selection-policy result rather
   than bad luck.

---

## 1. What openai/math is

Facts from the repository itself (`README.md` here has the table and the commands):

- **First public commit 6 Oct 2026**, 722 manuscripts in 372 families. **The 7 Oct update**, 31
  hours later, withdrew three of them, with notices dated 6 Oct, for a sign error that invalidated a
  stabilization-trace argument, and repaired fourteen others. Now 719.
- **"An unreleased internal OpenAI model"**, roughly three hours of thinking compute per result.
  **About 4,000 problems posed**; aggregating and "requiring an appropriate level of
  significance" left 372 families. The Hodge conjecture for CM abelian varieties and the zeta
  zero-free work are named exceptions to that procedure.
- **Lean.** 242 families ship a scope note. The catalogue declares `status.scope: "Partial
  progress."` and `review.status: unchecked`, and the README says ~42% of top-line results are
  formalized. The scope notes are candid: 64 of the 242 contain at least one of the limiting
  phrases `derive_families.py` lists ("does not establish", "weaker", "outside this selected
  statement", …). This intake relies on them for every tier and checks one by compilation.
- **Process records.** Abridged reasoning summaries for 10 families, plus a public changelog
  recording withdrawals and repairs. §6.6 says what that does to `REPORT_U`.

---

## 2. How the intake was made, and what it cost

| step | by | output | check |
|---|---|---|---|
| derive the snapshot | `derive_families.py` | `families.json` | header counts asserted (719 / 372) |
| propose ranking pairs | five subagents, 100 records each, reading all 372 family summaries and grepping full abstracts and scope notes | 494 proposed pairs | — |
| verify every status-bearing pair | this session, against abstracts and scope notes | 135 pairs; tiers assigned; **2 relation changes, 1 miss** | `apply_ranking_overlay.py` |
| recall screen 1: lexical overlap | `recall_screens.py` | 1,184 pairs the sweep never considered, ranked; top 70 read | **recovered record 272** (Kuznetsov), which the sweep missed |
| recall screens 2–3: every conjecture name in the family texts against every record title; every rare eponym in a family title against every record | `recall_screens.py` | 142 and 138 unconsidered pairs, all read | 272 again, otherwise name collisions only |
| sweep the rest of the tree | two subagents, proof-protocol and board-finder/leanboard | 119 located statements | every quote verified verbatim: `check_stale_quotes.py` |
| gate the live targets | `../board-finder/gap/openai_gate.py` | 4 of 25 settled-claimed | six perturbations, all abort |

**Where this pass departed from the sweep**, so the error rate of the cheaper pass is on file:

- **one miss**: record **272** / family 054, found only by the recall screens;
- **two relation changes**: record **280** upgraded ADJACENT → SAME_TARGET (the idempotent
  argument in §4.2), and **379** downgraded SAME_TARGET → SUBCASE, because the record includes
  the nonunital case;
- **no tier corrections, because the sweep assigned no tiers.** It quoted scope notes, and every
  tier was assigned here from them. The least obvious calls each carry their reason in
  `ranking_overlay.json`: **184** and **265** FORMAL_WEAKER, **392** FORMAL_WEAKER, **426**'s
  K = 7 instance FORMAL (Lean proves N(6) ≤ 5), and **444** PAPER_ONLY (the Lean file checks the
  ring exists, not the claim).

**One defect of mine, found and fixed before anything used it.** The first derivation stripped
HTML with `<[^>]+>`, which also deletes the text between the two sides of an inequality in inline
math. It garbled **11 of 242** scope notes (family 003's lost its Landau–Siegel statement) and one
CONTENTS cell. A subagent noticed the garbling in its output. The tag pattern is now explicit, and
the derivation reruns clean.

**What was not done.** No paper was refereed. Apart from 165's introduction, no paper was read
past its abstract. Comparator was not run; it needs `landrun` and `lean4export`. ADJACENT and
NAME_COLLISION pairs (360) are kept for the record and were not individually verified.

---

## 3. The ranking: 79 of 499 claimed settled

`apply_ranking_overlay.py`, against `../board-finder/playability/ranking_v16.json` (ProofAtlas
top-500 v16, edition 2026-09-19), which stays byte-identical.

| strongest relation per record | records |
|---|---:|
| SAME_TARGET | **79** (46 proved, 32 disproved, 1 independent of ZFC) |
| SUBCASE only | 44 |
| BOUND_OR_NUMBER only | 7 |
| **touched** | **130 / 499** |

| SAME_TARGET by tier | records |
|---|---:|
| FORMAL | **42** |
| FORMAL_WEAKER | 3 (Polyakov 184, Cartan–Hadamard 265, separable quotient 392) |
| PAPER_ONLY | 34 |

**The 42 at FORMAL tier include**: Unique Games (34), Landau–Siegel zeros (43), Hadwiger,
disproved (79), Erdős #3 (130), Cannon (133), residual finiteness of hyperbolic groups, disproved
(140), BPL = L (158), free group factors (171), Falconer (193), Kaplansky zero divisors, disproved
(202), Kadison similarity (231), Artin K(π,1) (244), Sidorenko, disproved (257), Mahler (271), the
DFT n log n lower bound, disproved (286), Thompson's F nonamenable (317), Nagata (361), Rokhlin
multiple mixing (402) and Catalan's constant irrational (422). The full list, each with its reason,
is `ranking_overlay.json`.

### 3.1 Where the harvest fell

| rank band | SAME_TARGET | any |
|---|---:|---:|
| 1–100 | **7** | 28 |
| 101–200 | 13 | 27 |
| 201–300 | 20 | 25 |
| 301–400 | 16 | 20 |
| 401–500 | **23** | 30 |

**The more important the problem, the less often it fell**: 7% in the top hundred, 23% in the
bottom. `../board-finder/playability/README.md` finding 2 was that *importance and playability run
against each other*. This is the same shape on a different axis.

| domain | SAME_TARGET | of |
|---|---:|---:|
| algebra / representation / category | **17** | 48 (35%) |
| geometry / topology | **23** | 73 (32%) |
| probability / ergodic / dynamics | 9 | 37 |
| analysis / PDE | 9 | 40 |
| combinatorics / discrete geometry | 7 | 38 |
| theoretical computer science | 3 | 54 |
| mathematical physics | 2 | 19 |
| quantum information | 2 | 18 |
| **number theory / arithmetic geometry** | **4** | **119 (3%)** |
| logic, cryptography / coding, applied | 1 each | 19, 26, 8 |

### 3.2 Against the playability census

| census class | SAME_TARGET | any |
|---|---:|---:|
| playable (a finite witness settles a branch) | 5 / 35 (14%) | 6 / 35 |
| not playable | 74 / 464 (16%) | 124 / 464 |
| has a workspace | 19 / 123 (15%) | 36 / 123 |
| no workspace | 60 / 376 (16%) | 94 / 376 |

**Playability gave no protection, and neither did neglect.** The playable records that fell are
Hadwiger, Sidorenko and Kaplansky idempotent, all by counterexample, plus Alperin weight and
Kazhdan–Lusztig invariance by proof. The three counterexamples are *explicit constructions*: a
35-vertex bipartite graph, a family of graphs with independence number 2, a finitely presented
group. The finite witness this census was built to find did turn up. It came from a
reasoning pipeline, not a search.

---

## 4. This branch's live and recent targets

### 4.1 The gap pool (`../board-finder/gap/GATE_OPENAI.md`)

| item | family | tier | effect |
|---|---|---|---|
| **V2** Zarankiewicz cr(K₇,₁₁), cr(K₉,₉) — **the live thread** | 165 | FORMAL, **compiled here** (`LEAN_CHECK_165.md`) | 225 and 256; refute branch impossible |
| V1 Hill at n = 13 | 165 | FORMAL | 225 |
| U11 Seymour counterexample | 173 | FORMAL | conjecture claimed true; nothing to find |
| C6 four MUBs in ℂ⁶ | 266 | FORMAL_WEAKER | N(6) = 3 claimed; Lean proves ≤ 5 |
| the other 21: Hadamard family ×5, MOLS(10), PTE 11, Costas 32/33, 3×3 matmul rank, APN, SIC, kissing, caps, Hirsch… | — | — | CLEAR |

### 4.2 Record 280, "the strongest single target"

The record asks that K[G] have no idempotents but 0 and 1, for **every field and every
torsion-free G**. Two families bear on it:

- **207 claims the characteristic-0 case, FORMAL.** Every torsion-free G, every commutative
  unital domain of characteristic 0.
- **197 refutes it in characteristic 2, PAPER_ONLY, by a one-line argument this intake supplies.**
  If ab = 1 and ba ≠ 1 then e = ba satisfies e² = b(ab)a = e. It is not 1 by hypothesis, and not
  0, since a = (ab)a = a(ba). So the 4 Oct manuscript's finitely presented **torsion-free** group
  with 𝔽₂[G] not directly finite gives a nontrivial idempotent in 𝔽₂[G]. The formalized
  direct-finiteness counterexample uses a group *with* torsion and does not reach this record.

Claimed net state: **true in characteristic 0, false in characteristic 2.** The adjacent zero-divisor
conjecture (record 202) is claimed false over 𝔽₂ at FORMAL tier (family 196). The original recon
said 280 was untouched. That was wrong, and it is the most consequential single correction here.

### 4.3 Cycle 0's seven, and Epoch's 41

**Cycle 0's shortlist** (`../board-finder/gap/register/REGISTER.md` §7):

- *Kaplansky ZD*: claimed false (196, FORMAL);
- *Zarankiewicz/Hill*: claimed true (165, FORMAL);
- *Mahler*: claimed true in the volume-product sense (087, FORMAL for the symmetric case and the
  general bound).
- Kalai 3^d, Tuza, MDS in characteristic 2 and union-closed: no family.

**Three of seven.** One caution belongs to this tree rather than to openai/math. The register's
*Mahler* row and `../board-finder/gap/v4/PROMPT_GAP_v4.md` line 278 point at Epoch #34,
*Littlewood polynomials with large normalized **Mahler measure***. That is a different problem from Mahler's **volume-product**
conjecture, which is the one 087 claims. Which one Cycle 0 meant is not recoverable here. It is
the fifth one-name-two-problems collision on this board.

**Epoch's 41 unsolved**: #2 symplectic ball packing is claimed for every 2n ≥ 6 (343, FORMAL).
Whether that covers Epoch's item depends on a dimension scope that was never transcribed. #34
looks settled in substance: 076 claims ultraflat real Littlewood polynomials at every large length,
which forces normalized Mahler measure → 1. That is paper only, since the formal statement bounds
the maximum, not the minimum. #3 (Apéry-style irrationality via recurrences) is possibly touched
by 005 (Catalan's constant, FORMAL); the item's exact ask was never transcribed. **At most 3 of 41,
against 79 of 499 on the ranking.** §6.2 says why that gap is the most informative number here.

---

## 5. Stale statements across the tree

`stale_statements.json`: **119** statements written 9 Sep – 1 Oct that a family now bears on. All
119 quotes were verified verbatim; `check_stale_quotes.py` re-verifies them on demand.

| relation (the sweeps' labels) | rows |
|---|---:|
| LIVE_TARGET_HIT | 52 |
| SUBCASE | 16 |
| LABEL_AT_RISK | 15 |
| BOUND_SUPERSEDED | 14 |
| METHOD | 13 |
| CONTRADICTED | 9 |

**Policy: dated records are not rewritten.** A retrodiction encoding, a relayed response, a
pre-registration or a result file records what was known when it was written. Rewriting it to
today's knowledge would destroy what it is evidence of, and for the retrodiction tree it would
break the blinding rule outright. Twin N9's "conjectured 2" for the sensitivity exponent, the
`../proof-protocol/p1-retrodiction/twins/REJECTED.json` distinct-distances row,
`../proof-protocol/p3-taxonomy/d28_bound_strength.json`'s ω ≤ 2.3715, control 15's Roth
ceiling and the prospective log stay as they are. They are listed in `stale_statements.json` and
covered by `D70`.

**Live documents — ones that direct future work — carry a dated note instead:**

| document | note |
|---|---|
| `../board-finder/gap/v4/K711_POTENTIAL.md` | banner: target claimed closed, see `../board-finder/gap/v4/CLOSED_BY_165.md` |
| `../board-finder/gap/v4/GET_THE_CODE.md` | banner: recommendation withdrawn |
| `../board-finder/gap/register/REGISTER.md` §7 | Part D rows for Kaplansky ZD, Zarankiewicz/Hill, Mahler; the Mahler naming collision |
| `../board-finder/gap/README.md` | the second gate, and what a CLEAR from the first one means |
| `../board-finder/playability/README.md` | record 280; the overlay |
| `../leanboard/REPORT_U_meta_game.md` §3 | "four for four" superseded three times |
| `../proof-protocol/ledger.json` P-43 | dated addendum; why it cannot be scored |
| `../proof-protocol/citations.json` C1-chain | the "best known separation is quadratic" refinement now has a claimed superquadratic successor (132, FORMAL) |
| `../STATUS.md` | pointer to this file; the Lean-toolchain line |

**The prospective arm is unaffected.** Entry 2608.14454 is a prediction about an arXiv paper's
method, logged *not-applicable*. Family 166 is a different and stronger claim on the same problem
(c_d n^{2/d} for every d ≥ 3, paper only). It neither resolves that entry nor reads its method, and
the log is append-only.

---

## 6. What this says about choosing targets

n = 1 release from one lab. Each point below is stated as what this release shows. None is a
law.

### 6.1 Crowding moved from public lists to private evaluations

`../board-finder/gap/README.md` priced the field at **~40 AI-resolution claims a month**, and
`../leanboard/aj/REPORT_AJ_vibemathed_census.md` counted **664** disclosed AI results from Jul 2025
to Sep 2026. openai/math is **719 manuscripts with dates spanning four weeks**, released at once,
with no prior trace on any list. Every crowding instrument on this board checks a *public* artifact:
Epoch's list, formal-conjectures, a workspace count, a recent move on the problem. **None can see a
lab's evaluation set before publication, by construction.** V2 was cleared against
formal-conjectures, the largest agent-facing database (`../board-finder/gap/v4/RESULT_V4.md`
§4a), and its frontier had not moved since Woodall 1993. Both answers were correct as asked:
nobody public was working K₇,₁₁.

### 6.2 The harvest was theory-shaped, and it went around this board's niche, not through it

Three numbers from three populations:

| population | shape | touched |
|---|---|---:|
| ProofAtlas ranking | named conjectures | **79 / 499** exact target |
| this board's 25 gap items | mostly finite constructions | **4 / 25**, and all four are *proof- or impossibility-shaped* outcomes |
| Epoch's 41 unsolved | mostly `Construction – Finite`, `Record Breaking` | **≤ 3 / 41** |

The construction targets this board was built around are **untouched**: MOLS(10), PTE 11, Costas
32/33, the thirteen Hadamard orders, D-optimal U13. So are the Epoch list's record-breaking items.
Where a construction target *was* hit, it was hit by proving the construction impossible (C6, U11)
or by proving the closed form (V1, V2). And where the ranking's counterexamples fell, they fell as
explicit constructions found by reasoning (§3.2).

**This supports the v2 rubric's central distinction and sharpens it.**
`../board-finder/gap/RESULT_GAP_v2.md` scored *whether the unknown set can be written down*: thirteen Hadamard orders against an open tail. The
sharper statement after this release: **a finite instance is protected only if no single theorem
decides it.** K₇,₁₁ had a finite unknown set, {221, 223, 225}, and failed that test, because
Zarankiewicz's formula is one statement over all (m, n). The thirteen Hadamard orders pass it.
The Hadamard conjecture would decide them, but no proof of it is in sight, and openai/math does
not claim one (record 331 is untouched). Each order is its own construction.

### 6.3 The instruments that killed on mathematics were right

| item | instrument | cost | right? |
|---|---|---|---|
| C6 | premise-falsification line (mod-*p* shadow) | one line of arithmetic, during triage | **yes**, by 21 Sep, three days before the claimed proof's manuscript date |
| U11 | witness polarity (Step 2) | one reading | **yes** |
| V2 | crowding checks: formal-conjectures, no move since 1993, no workspace | days | **no.** Passed a target closed a week earlier |
| V2 | R remedy label from the frontier method section | a primary-tier read | read ALGORITHM + THEORY, narrowed to ALGORITHM. **The first reading was right** (`../board-finder/gap/v4/CLOSED_BY_165.md` §4) |

**Recommendation.** Make **"is there a single theorem that would decide this instance, and is it
the kind of statement a lab would pose?"** a step-0 kill, beside the list filter.
*Closed-form conjecture over all n with this instance as one case* is the exposure profile. It is
cheap to ask and it was the right question here.

### 6.4 The two proxies for "uncontested" gave no protection, and one ran the wrong way

This board used two proxies for a target nobody else is on: lower prominence, and no workspace.
Under this harvest the second made no difference: 15% of workspaced records fell against 16% of
the rest (§3.2). The first ran the wrong way. The 7% → 23% gradient in §3.1 means the *less
famous* named conjectures fell more often: tractable in a few hours of model thinking, and too
specialised for any human group to have made them a programme. **Under a lab harvest, low
prominence is a risk factor, not a shelter.** The one profile that held is §6.2's: no single
theorem decides the instance.

### 6.5 Verification is now the scarce input, and it is available here

openai/math formalized ~42% of top-line results and labels the rest honestly. Its scope notes
are the most useful single artifact in the release: 64 of 242 say in so many words that the formal
statement is narrower than the paper. **"A scope note exists" and "the claim relied on is formal"
diverged on 16 of the 135 pairs adjudicated here**: 12 PAPER_ONLY and 4 FORMAL_WEAKER. Family 197
shows the trap at its sharpest: one note covers a formal counterexample that settles record 439
and does not reach records 280 or 427. The project's own tiering is the right unit, and both
gates now enforce it.

And this environment can now check. `../STATUS.md` §3 records "no Lean toolchain is reachable".
That was true of the routes tried (the community site and Mathlib's binary cache, both denied). It
is false of GitHub's release assets: the toolchain installs from there, and Mathlib builds from
source on this container: 33 minutes for the ~2,000 Mathlib modules 165's proof needs
(`LEAN_CHECK_165.md`). **The FLT and NS artifacts' relayed
verification claims (Reports H and N) are now checkable here,** at the cost of a Mathlib build.

### 6.6 The publication regularity in REPORT_U has now failed three times

`../leanboard/REPORT_U_meta_game.md` §3 found **four for four** major AI results published as final
results only, with no trajectory. It has been contradicted by:

- `../leanboard/ak/REPORT_AK_zeta_audit.md` §6: a disclosed run of ~650 approaches, ~60
  subagents, ~31 M output tokens, with attribution per agent;
- `../leanboard/at/REPORT_AT_audit_surface.md` part 2: the full CDC prompt;
- **openai/math**: reasoning summaries for 10 families, the denominator (~4,000 posed → 372
  families, ~9%), and a public withdrawal-and-repair changelog within 31 hours of release.

The regularity was a fact about four artifacts in one month. The note in REPORT_U says so where a
reader of §3 will see it.

### 6.7 A yield figure this board did not have

~4,000 problems at ~3 hours each is ~12,000 model-hours for 372 families, ~32 hours per kept
family, ~9% kept. This board's own register
(`../board-finder/gap/register/REGISTER.md` §4.1) records two results (A7, A8) across nine
attempted targets. The rates are not comparable: different significance bars, different
problem populations, and the lab's 91% discards are unpublished. But it is the first denominator on
file for an AI harvest, and any future estimate of *how fast is the field turning over* should
start from it rather than from a count of claims.

---

## 7. What to do

1. **Close V2.** `../board-finder/gap/v4/CLOSED_BY_165.md`. Do not fetch the other instance's code.
2. **Run both gates before any target starts**, and record both verdicts in its
   pre-registration. Add §6.3's single-theorem question as a step-0 kill in the next gap prompt.
3. **Re-derive on every entry in openai/math's history.md** (`README.md`, *Refreshing*).
   Withdrawals happen, and three already have.
4. **Use the toolchain.** Report H's and Report N's relayed verifications can now be reproduced.
   That is the first time this project could turn a relayed formal claim into a checked one.
5. **Treat the playability census's 35 as 29.** Hadwiger, Sidorenko and Kaplansky idempotent are
   claimed settled by counterexample, Alperin weight and KL invariance by proof (§3.2), and record
   426's playable branch, seven MUBs in ℂ⁶, is claimed impossible at FORMAL tier.
6. **Feed the prospective arm from here, in a session that has not read the papers.** The arm's
   five sealed items cannot be resolved, because arXiv is blocked. openai/math's manuscripts and
   their LaTeX sources clone from GitHub, which is reachable here, so predictions sealed from abstracts *can* be
   resolved against the method. That makes this the first batch the arm could actually score.
   Candidate families and the contamination statement for this session are in `D73`. Nothing was
   sealed here, deliberately.
