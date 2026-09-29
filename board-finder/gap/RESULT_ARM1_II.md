# Arm 1 — the `II` records: no contradiction, a real defect, and a correct rejection in yield

Bars: `SELECT_v1.md` Part I, registered in commit fab89d8 before dispatch. Raw worker output:
`discovery/A1_a.md` (ranks 17–368) and `discovery/A1_b.md` (ranks 375–479, plus 221/282/337 as
checks). Briefs: `discovery/prompts/A1_a.md`, `discovery/prompts/A1_b.md`.

## 1. The contradiction in the handoff dissolves, and what is left is sharper

The handoff reads the situation as "the playability screen says record problems are unplayable, and
the queue is made of nothing else; one instrument is wrong." Applied to the *same object*, the two
instruments do not disagree:

| queue item | its deliverable | class under `../playability/classify.py`'s own definitions |
|---|---|---|
| U13 D-optimal | exhibit a ±1 matrix of order n attaining the Ehlich–Wojtas bound | **P1** — existence-headed, finite checkable witness |
| U8 kissing | exhibit τ+1 unit vectors at mutual angle ≥ 60° | **P1** |
| U10 caps | exhibit a cap of size s+1 | **P1** |
| U9 snakes | exhibit an induced path of length L+1 | **P1** |

The *headline* of each ("determine τ₁₁ exactly") is `II`. For a headline that is an extremum over
finite objects, "the maximum equals m" is the conjunction **"∃ an object of value m" ∧ "∀ objects,
value ≤ m"**. The first conjunct is P1, the second is U. **So `II` = P1 ∧ U, the screen marked the
conjunction unplayable because one conjunct is U, and the queue plays only the P1 conjunct.** The
class definition "a record, not a witness" is the error: a record *is* a witness for one conjunct.
This is the same split-at-`∧` that `../playability/INTERESTINGNESS.md` P2 proposes for
interestingness, pointed at playability.

It holds **only for extremal headlines**. An asymptotic-order headline ("determine the order of
r₃(N)") has no finite P1 conjunct: its lower side needs a construction *family*, and a finite
object bears on it only through a lifting theorem. That is exactly what gate S1 tests.

## 2. The measurement

`CE` = CANNOT EVALUATE, which counts as FAIL.

| rank | record | S1 coupled | S2 not vetoed | what decided it |
|---:|---|---|---|---|
| 17 | BQP vs NP | FAIL | FAIL | not a record at all — a truth-value question misfiled as `II` |
| 186 | r₃(N) order | FAIL | PASS | asymptotic; only lifting known is the product lemma, giving N^α with α<1 (RECALL) |
| 199 | Waring G(k) | FAIL | FAIL | bounds move by proof |
| 246 | MZV dimensions | FAIL | FAIL | no tracked number |
| 277 | 3-uniform hypergraph Ramsey growth | CE | PASS | could not check for a lifting theorem |
| 288 | mapping-class-group linearity | FAIL | CE | no tracked number |
| **308** | **real Grothendieck constant** | **PASS** | **PASS** | route (a): K_G is a sup over finite matrices |
| 351 | Gaussian interference channel | FAIL | FAIL | no scalar record |
| 353 | Turán number of even cycles | CE | PASS | could not check for a lifting theorem |
| **368** | **Thomson problem** | **PASS** | **PASS** | route (a): inf over N-point configurations |
| 375 | star discrepancy order | FAIL | FAIL | asymptotic, no lifting theorem seen |
| 385 | Lieb–Thirring L₁,₃ | PASS (formal) | CE | the witness side is a counterexample potential; no rigorous-enclosure source found |
| 410 | Hilbert's 10th, fewest variables | FAIL | FAIL | a universal polynomial is an ALGORITHM → **vetoed** |
| 413 | Zarankiewicz | CE | CE | not searched (budget) |
| 417 | PFA consistency strength | FAIL | FAIL | moves only by proof |
| 428 | site percolation p_c | CE | CE | not searched (budget) |
| 441 | Witsenhausen | CE | CE | not searched (budget) |
| 450 | oriented percolation exponents | CE | CE | not searched (budget) |
| 479 | Ruzsa–Szemerédi (6,3) | CE | CE | not searched (budget) |

**COUPLED ∧ NOT VETOED: 2 of 19 (308, 368).** Derived from the table: rows with S1 = PASS and
S2 = PASS. 385 fails on S2 = CE.

**Full-bar survivors: 0 of 19.**
* **308 dies on S4 (crowded).** Read directly from teorth/optimizationproblems, file constants/10a.md,
  on raw GitHub (SECONDARY-RELAYED, fetched by me as well as by the worker): the lower bound jumped
  from Davie–Reeds ≈1.67696 to **6π/11 ≈ 1.71360** in 2026 [SLXCKKM26], fixing the tenths digit of
  K_G at 7. The authors say the bounds "were discovered by a long-running collaborative effort of
  humans and a long-horizon AI research system". Two further 2026 papers moved the lower bound by
  1e-26 and 1e-12, and three moved the upper bound. The note that goes with it also matters: the
  6π/11 bound is "the first not obtained via an explicit low-dimensional gap instance". **So the
  coupled witness side stopped being the side that moves.**
* **368 dies on S3 (CE).** The Wales table's history was unreadable, so the kind of the latest move
  is unknown. New and unrefereed: arXiv:2609.22077 claims a Lean-checked, computer-assisted proof
  for N = 8.

## 3. Scored against the registration

* **P-32a (≥ 4 coupled and unvetoed → defect): WRONG.** 2 of 19. Scored as registered, but read
  with its limitation: **9 of 19 records were left partly or wholly unevaluated** (277, 288, 353,
  413, 428, 441, 450, 479, and 385's S2) after the session's shared search budget (200 calls) ran
  out. Three of those — 428, 441, 413 — are the ones I expected to be coupled. The unevaluable-is-
  FAIL rule does its job here: it stops a prediction from being rescued by the records nobody
  looked at. But the count measures the environment as much as the class.
* **P-32b (≤ 1 full survivor): CORRECT.** 0 of 19.

## 4. The §0 verdict

**Neither instrument is wrong about the object it classifies.** The screen is right that `II`
*headlines* are unplayable. The defect is the missing decomposition: at least 2 of 19 headlines
(308, 368) hide a P1 conjunct, and up to 5 more might (385, 428, 441, 413, 479) once evidence is
available. **In yield the exclusion was a correct rejection.** Nothing survives, and the reason is
not the one the screen gave:

* the one coupled record with a readable history was **moved in August 2026 by a human–AI team**
  — the gap closed in the direction `GAP_V3.md` §6 predicted, and by someone else;
* **three of the 19 moved in August–September 2026:**
  * 308 — the 6π/11 lower bound, and a claimed upper bound of 1.7813;
  * 368 — the N = 8 case, claimed with an AI-produced Lean warrant;
  * 385 — Read–Schulz, arXiv:2609.10478, claim L₁,d ≤ (2/√3)·L^cl in every dimension, against the
    previous 1.456.

  The `II` class is where AI-assisted work is landing *now*. That makes it the wrong place for a
  project whose edge is not compute, and the right place to watch.

The queue's record-shaped items are therefore not "`II` problems the screen wrongly rejected". They
are P1 conjuncts of headlines the corpus never contained, and they must pass gap type and crowding
on their own. That is Arm 2.

## 5. Consistency checks (221, 282, 337)

All three blocks came back CE — the budget was gone before the worker reached them. The earlier
statements about them are **neither confirmed nor contradicted by this run**. The worker makes one
fair point on 337: "narrowed to a hundredth of a bit" is not "closed". It is dead to *us* because
the headroom is gone, not because it is resolved.
