# The openai/math gate — result

`GATE_EPOCH.md` answered one question: *is this target on FrontierMath: Open Problems?* A CLEAR
from it meant **"not on that list"**, and the list is a 21 Sep transcription. On 6 Oct 2026 OpenAI
published `github.com/openai/math`: 722 manuscripts in 372 result families, cut to 719 the next
day by three withdrawals. Each family claims a result on a problem posed to an internal model,
from an evaluation that posed about 4,000. No list check could have seen it before 6 Oct, and the
Epoch gate cannot see it now. `openai_gate.py` is the missing gate. It runs against the snapshot
in `../../openai-math/families.json` (commit `fd4aeeb`, 7 Oct).

## 1. Verdict

**Four of the 25 live items are claimed settled. One of them is the target this branch was
working on 1 Oct.**

| item | verdict | family | formal tier | what it does to the item |
|---|---|---|---|---|
| **V2** Zarankiewicz, cr(K₇,₁₁) / cr(K₉,₉) | **SETTLED-CLAIMED** | 165 | **FORMAL** | cr(K_{m,n}) = Z(m,n) for all m, n. So cr(K₇,₁₁) = 225 and cr(K₉,₉) = 256. The refute branch is claimed impossible and the verify branch claimed done. **The v4 thread's live target**: see `v4/CLOSED_BY_165.md` |
| **V1** Hill's conjecture at n = 13 | **SETTLED-CLAIMED** | 165 | **FORMAL** | cr(K_n) = H(n) for all n, so cr(K₁₃) = 225, the top of the {223, 225} bracket |
| **U11** Seymour second-neighbourhood counterexample | **SETTLED-CLAIMED** | 173 | **FORMAL** | the conjecture is claimed **true** for every finite oriented graph, so there is no counterexample to find |
| **C6** four MUBs in ℂ⁶ | **SETTLED-CLAIMED** | 266 | **FORMAL_WEAKER** | N(6) = 3 is claimed. The exclusion of four is a computer-assisted run "under the stated binary64 arithmetic and compiler conditions". The Lean statement proves only N(6) ≤ 5 |
| the other 21 | CLEAR | — | — | including all five Hadamard-family items, MOLS(10), PTE 11, Costas 32/33, the 3×3 matmul rank, APN, SIC, kissing numbers, caps and the Hirsch ladder |

**Formal tier is read from each family's own Lean scope note, never from the presence of a Lean
file.** FORMAL means the note says the formalized statement *is* the claim this item needs.
FORMAL_WEAKER means a formalization exists and proves something weaker. Neither is a check
performed here, with one exception. The 165 formalization was compiled here: all 2,581 build
jobs pass, and the main theorem uses only Lean's three standard axioms
(`../../openai-math/LEAN_CHECK_165.md`).

### Three of the four had already been dropped here, and the fourth was the live target

| item | demoted here by | when | what openai/math adds |
|---|---|---|---|
| C6 | its own premise-falsification line: mod-*p* shadow, ASD 0.9983 < 1, so "the object probably is not there" (`RESULT_GAP_v2.md`) | 21 Sep | the claimed proof that it is not there |
| U11 | v4 Step 2 on **witness polarity**: δ⁺ = 8 is a non-existence task (`v4/RESULT_V4.md` §4 (iv)) | 30 Sep | the claimed proof that the polarity call was right |
| V1 | v4 R kill, left UNDETERMINED for want of method-section access | 30 Sep | — |
| V2 | **not demoted.** It cleared, became the working target, and absorbed nine relay rounds | 30 Sep – 1 Oct | the claimed proof, dated 23 Sep, one week **before** the thread started |

The two falsification-shaped instruments, the premise line and the polarity step, called their
items correctly six to fifteen days before the claimed proofs were published. The crowding
checks did not. V2 passed them: absent from formal-conjectures (`v4/RESULT_V4.md` §4a), no workspace, no
move since Woodall 1993. It had been closed privately on 23 Sep, and everything it was checked
against was public.

## 2. Why this gate screens phrases, not tokens

`epoch_gate.py` screens distinctive object **tokens** against 41 short titles. Run unchanged
against openai/math's prose, the same tokens produce **454 collisions** on titles and summaries,
and **666** with abstracts (the script prints both). "1", "perfect", "square", "line", "power", "lattice" and "degree" are
distinctive in a list of titles and generic in a paragraph. So this gate matches distinctive
**phrases** over each family's full text: title, summary, and every manuscript title and
abstract. It then does what the Epoch gate does. It refuses to return a verdict until every
collision carries a reasoned adjudication. The phrase screen produces **12** collisions.

That buys precision and costs recall. A family that names one of these objects in words none of
its phrases contain would pass the screen silently. Two mitigations, neither replaced by the
script:

- all 372 family titles were read directly;
- a semantic sweep of the whole repository ran separately against all 372 families. For these
  25 items it independently returned the same four hits and no others
  (`../../openai-math/RESULT_INTAKE.md` §5).

## 3. The false friends

Of the ten non-control collisions, four are SETTLED_CLAIMED, one is
SAME_FAMILY_DIFFERENT_PARAMETER, and five are DIFFERENT_OBJECT. Those five come from three
shared names:

- **Zauner** names two conjectures: SIC-POVM existence (U16, CLEAR) and the dimension-six MUB bound
  (C6, settled-claimed). This board has now met one name carrying two problems four times:
  Zarankiewicz (crossing vs extremal), Rota, SIC and Zauner.
- **Seymour** in family 157 is the Reed–Seymour fractional weakening of Hadwiger's conjecture,
  not the second-neighbourhood conjecture.
- **Hadamard** in family 266 is complex Hadamard matrices of order 6, and in 179 it is circulant
  real Hadamard matrices. Neither touches existence at the open orders. 179 is recorded as
  SAME_FAMILY_DIFFERENT_PARAMETER for U2. It rules out the circulant ansatz at every order above 4,
  which for orders 2000–3000 had long since been excluded computationally. The one thing it does
  say is that **this family is being harvested by proof, not only by search**.

## 4. Negative tests

A gate that cannot fail is not a gate. Six perturbations were run on a copy of the tree. Each
aborts the run, and the clean run exits 0:

| perturbation | result |
|---|---|
| rename family 179 so "circulant Hadamard" no longer occurs | `FAIL: adjudications for pairs the screen no longer makes: [('K3', '179'), ('U1', '179'), ('U2', '179')]` |
| append "Costas arrays of order 32 exist" to family 377's summary | `UNADJUDICATED  C3 vs 377 …` then `FAIL: screen produced collisions with no recorded adjudication` |
| misjudge the K4 / 196 control as DIFFERENT_OBJECT | `FAIL self-test: positive control K4 … The matcher is broken; no verdict below is trustworthy.` |
| delete family 266's Lean scope note while C6 claims FORMAL_WEAKER | `AssertionError: ('C6', '266') claims a formal tier but family 266 ships no scope note` |
| drop one family from the snapshot | `AssertionError: family snapshot is not the 372 at fd4aeeb` |
| add a 373rd family | same assertion; the second row isolates the collision check that this one pre-empts |

The fourth row is the one this gate has and the Epoch gate does not need. A tier claim is
checked against the source, so "FORMAL" cannot be typed for a family that ships no formal
statement.

## 5. Residual risk, stated

- **These are claims.** openai/math's own catalogue says `review: status: unchecked`. Three
  manuscripts were withdrawn within a day of release, and fourteen more were repaired. A
  SETTLED-CLAIMED verdict removes an item from *this board's* queue because the expected value of
  working it has collapsed. It does not certify the mathematics.
- **The snapshot will move.** openai/math's history.md already records one dated revision. Re-derive with
  `../../openai-math/derive_families.py` and re-run this script on every new entry. The count
  assertion fires on any change in the number of families, and the stale-adjudication check
  fires when a revised summary drops a phrase.
- **Two gates are still not all the lists.** TheoremDB, Horizon and erdosproblems.com remain
  undiffed, as `GATE_EPOCH.md` §5 said. A private evaluation like OpenAI's is by construction on
  no list until its owner publishes. §1's second table is the only defence this board has
  against that: an instrument that kills a target on its own mathematics does not need to know
  who else is working on it.

## 6. What to do next

1. **Stop V2.** The (11,7) sweep, the code request in `v4/GET_THE_CODE.md` and P-43's component (A)
   no longer buy anything. See `v4/CLOSED_BY_165.md`.
2. **Run both gates before any new target starts**, and record both verdicts in its
   pre-registration.
3. **Promote the two instruments that called these correctly.** A premise-falsification line and
   a witness-polarity check cost minutes and were right on C6 and U11. The crowding screen cost
   days and was wrong on V2. That is a selection-policy finding and belongs in the next prompt,
   not only here (`../../openai-math/RESULT_INTAKE.md` §6).
