# Independent replication: Mazur's Domineering temperature-33/16 counterexample

**Verdict: the mathematics replicates. Every claim I could test is true, and I found no
defect the paper had not already disclosed.**

Target: Lech Mazur, *An exact counterexample to Berlekamp's temperature-2 conjecture for
Domineering*, 14 August 2026, ProofAtlas. This is ProofAtlas's **only** claimed advance whose
evidence label reads `Unverified manuscript` rather than Lean-checked or accepted, and its
collaboration card carries a standing request: `INDEPENDENT CHECKS STILL OPEN — Specialist
review and unrelated replication`.

Two programs, written here from the paper's coordinate lists and move table alone:

- `verify_mazur.py` — 19 structural checks. All pass.
- `cgt_engine.py` — a from-scratch combinatorial-game engine. Confirms the central value.

## 1. What replicated

**The value.** `G(B) = {17/8 | −2+*}` — **confirmed**, by direct Conway-order comparison
against a constructed target.

**Proposition 4.1 in full.** `G(B − C–U) = 17/8` and `G(B − C–W) = −2+*`, both confirmed.
All 14 Left options satisfy `G ≤ 17/8` with **exactly one** attaining equality; all 14 Right
options satisfy `−2+* ≤ G` with **exactly one** attaining equality. The uniqueness claims
hold.

**The paper's own route-4 cross-check.** `G(B) + (−{17/8 | −2+*}) = 0`, confirmed
independently. I also verified by hand and by machine that `−{17/8 | −2+*} = {2+* | −17/8}`,
which is the difference game the paper says it tests.

**Structural claims, all 19:** B has 26 cells and is connected; 14 vertical and 14 horizontal
legal moves; C–U vertical and C–W horizontal; checkerboard split 14/12, imbalance 2, which
exceeds any rectangle's 0 or 1 — so B genuinely is not a rectangle remainder; components after
C–U are 19+5 and after C–W are 17+7, as stated; B′ has 28 cells in exactly 3 components
(26+1+1); the two adjoined cells have **no legal move**, so they contribute 0 and
`G(B′) = G(B)`; the 30-move table replays legally with every domino in bounds, correctly
oriented and non-overlapping, covering 60 of 88 cells, and **the final uncovered set is exactly
B′**; and the thermograph walls `17/8 − s` and `−2 + s` meet at `s = 33/16 = 2.0625` at height
`1/16`, clearing 2 by exactly 1/16.

## 2. Why this counts as independent

The engine shares no code or lineage with the paper's five routes, and takes a deliberately
different algorithmic path: **no canonicalization at all.** Conway's order relation is valid on
arbitrary forms, so raw memoized game trees suffice —

    X ≤ Y  ⟺  (no X^L with Y ≤ X^L)  and  (no Y^R with Y^R ≤ X)

Canonical-form computation (domination removal, reversible-option bypass) is the most
error-prone part of any CGT implementation, and routes 1–3 all rely on it. Omitting it removes
a whole class of shared failure mode. Route 4 is closest to mine but uses win/loss minimax
rather than the order relation directly.

**Self-check on my own instrument.** The memo tables use an optimistic guard that would
silently return `True` on a cycle. I re-ran the four decisive comparisons with guards that
raise instead. **The guard fired 0 times**, so the results do not depend on it — as expected,
since every move removes exactly two cells and the mask lattice is strictly decreasing.

**The honest limit on "unrelated".** The paper discloses GPT-5.6 Pro in its discovery and
derivation; this replication is also machine-produced. Different model family, different
session, no shared code — but if there were a failure mode common to LLM-written CGT code, this
would not catch it. It supplies the *unrelated replication* half of what the card asks for. It
does **not** supply specialist review.

## 3. One discrepancy — in a reported statistic, not in the mathematics

| quantity | paper (route 1) | here |
|---|---|---|
| board masks visited | 17,673 | 254,560 |
| raw game forms interned | 15,774 | **15,770** |

The mask gap is explained: a real engine decomposes disconnected positions into components and
evaluates each separately, so distinct masks repeat far less. I evaluate whole masks and do not
decompose, so I visit more.

The **4-form gap is unexplained.** It is small, it is in an instrument statistic rather than a
mathematical claim, and every mathematical comparison agrees exactly. Recorded as an
observation, not a finding. Worth one question to the author.

## 4. The formalization gap stands — and the paper declares it

This is the hook I flagged before reading the paper, and it is real. Verbatim:

> The Lean theorem uses the deliberately narrow predicate `HasValueTemperature`: it exhibits an
> explicit thermographed representative game-equivalent to the Domineering board. The
> development proves that exact equivalence and that representative's exact thermograph; **it
> does not yet prove a general theorem that thermographs are invariant under every
> game-equivalence presentation.**

So the machine-checked chain is: `B′ ≡ T`, and `T`'s thermograph meets at 33/16. Concluding
`t(G(B′)) = 33/16` needs thermograph-invariance under game equality — **the one step not
formalized, and the step that connects the checked content to the conjecture's statement.**

**Mathematically the gap is harmless.** Temperature and thermograph are functions of the game
value, so any two equivalent presentations have the same thermograph; this is standard (Siegel,
*Combinatorial Game Theory*). The gap is formal, not mathematical.

**But it means "Lean-checked rectangle-reachable witness at 33/16", as ProofAtlas's card puts
it, is stronger than what Lean proves.** Lean proves an equivalence and a representative's
thermograph. The inference to *this board's temperature* is sound and unformalized. That is a
smaller gap than the three this programme found before, and unlike those it is disclosed by the
author rather than discovered by the auditor.

## 5. What the audit did not find, and why that matters

Nothing undisclosed. The paper qualifies its own priority claim, states that its five routes'
agreement "is not the same as unrelated external replication", states that "Python output and
hashes are not theorem evidence", states that digests "do not by themselves establish
correctness", flags that B's checkerboard unreachability is not formalized, and flags the
`HasValueTemperature` narrowness itself.

That is a different outcome from Ghermoul, auro-zera and Guo–Fang–Lu, where the audits found
real defects. Those three overclaimed; this one does not. **Recorded as evidence about the
audit instrument as much as about the paper:** a check that only ever fires would be worthless,
and this is the first target where it correctly does not.

## 6. Reproducing

    python3 verify_mazur.py     # 19 structural checks, exit 0 on success
    python3 cgt_engine.py       # the value, prop 4.1, dominance, uniqueness, route-4 check

Standard library only. `cgt_engine.py` runs in well under a minute.

## 7. What is still open

- **Specialist review.** Untouched by this and by the paper's own five routes.
- **The invariance lemma.** Formalizing thermograph-invariance under game equivalence would
  close the one gap, and is a self-contained Lean target.
- **The 4-form discrepancy.** One question to the author.
- **The paper's own open questions**, unaffected: whether the crossing-option mechanism extends
  to an infinite hotter family, whether temperatures well above 33/16 occur, and what the
  smallest connected or rectangle-reachable example is. The boiling point is now known only to
  be ≥ 33/16.
