# Brief E (v2) — does the border-width axis offer anything the Williamson axis does not?

**For a Claude Code instance with (i) read access to `Cooperative-AI-Defense`, branch
`claude/hadamard-matrix-methods-vs79hi`, and (ii) a clone of `github.com/bbeartheancient/hoa64`.**
Without both, say which you lack and answer what you can — that is a clean partial result.

> **v1 of this brief is superseded and `PRECHECK_E.md` says why.** It was written in ignorance of prior
> work two directories away in this same repository, and three of its findings were already on file with
> one of them **retracted**. v1 also treated "which thirteen" as open; it is now settled. **Read
> `PRECHECK_E.md` §§1–2 before this brief** — it tells you what not to re-derive, which is most of what
> v1 asked for.

**This is not a search and not a change to the live *v* = 523 work.** Four questions, one measurement.

---

## 1. Settled. Do not spend budget re-deriving any of this.

**The two thirteens, both real** (`PRECHECK_E.md` §1):

* **FINDING_05's thirteen — the open orders under 3000**, and this is what
  `Cooperative-AI-Defense/hadamard/findings/OPEN_ORDERS.md` almost certainly means by "all 13 orders",
  since it sits in the same directory. *N* = 2060, 2092, 2148, 2284, 2292, 2396, 2572, 2588, 2636, 2676,
  2876, 2884, 2956; *v* = *N*/4 = 515, 523, 537, 571, 573, 599, 643, 647, 659, 669, 719, 721, 739.
  Quoted verbatim in `../../playability/HADAMARD_CROSS.md` §1.
* **hoa64's thirteen — solved, all below 2000**: Alpöge's **12** (668, 716, 892, 1132, 1244, 1388, 1436,
  1676, 1772, 1916, 1948, 1964) plus **Đoković's H(1852)**. All verified in this repository on
  2026-09-20, ±1 entries and **H Hᵀ = nI in exact integer arithmetic, 13/13**
  (`../../playability/hoa64/verify_matrices.py`, write-up `../../playability/HOA64_ASSESSMENT.md` §1).

**So the *b* > 2 pairs are parameter choices at OPEN orders and the entry is not void.**

***b* is a border width, odd** (`OPERATOR-SUPPLIED`). Of Alpöge's 12: **4 at *b* = 1, one each at
*b* = 3, 5, 7, and 5 unbordered.** So "*b* > 2" is "*b* ≥ 3" — there is no *b* = 2, 4, 6 case.

**Verified arithmetic** (`derive.py`, all assertions passing): all six rows of `../PLAN_2092.md` §1's
table reproduce, *d*-lists included; **`free_bits = 4(v−1)/d` exactly** on all six — four bits per orbit;
`density = free_bits − log2 E[#sol]`. **All thirteen open orders are uncovered by Paley I/II, Sylvester
and Kronecker closure** (necessary condition, passes). The five **composite** *v* are exactly 515, 537,
573, 669, 721 — and 669, 721 give orders 2676, 2884.

## 2. The prior work, and the retraction that is the reason for this brief

`../../playability/HADAMARD_CROSS.md` worked the composite-*v* route and then **retracted it in §8**:

> §§2–3: the five composite *v* were *"set aside on an assumption that was never checked"* — that each
> has a Baumert–Hall × Williamson route. **One object, W(103), would close two of the thirteen**, 2060
> and 2884; both assembly paths were validated locally.
>
> **§8, the retraction.** A Williamson quadruple of order *m* hands you *H*(4*m*) immediately.
> **716 = 4·179 and 892 = 4·223 were open until 2026** — they are two of Alpöge's twelve. **So W(179)
> and W(223) cannot be known**, and the routes for *v* = 537 and *v* = 669 are **dead on arrival**. And
> W(103) is doubtful: *H*(412) is known, and 412 = 4·103 is what a four-circulant Goethals–Seidel
> quadruple of length 103 produces — a weaker, more plentiful object than a Williamson quadruple — so
> *H*(412) being known is **consistent with W(103) not existing**.

**Hold that argument's shape, because it is the best move on this board and it is already made:
Alpöge's twelve solved matrices are used as evidence about which Williamson orders CANNOT exist.** A
solved order at 4*m* that was open until 2026 proves W(*m*) was not available.

**So the question this brief exists to ask is whether the border axis escapes that.** A naive free-bit
count points at *v* = 721 (192 free bits, 24 fewer than the order Alpöge solved) — and 721's route is
exactly one of the two §8 leaves doubtful. **If the border axis is just the Williamson axis in other
clothing, option 3 is dead for the reason already on file.**

## 3. The four questions

**Q1. What does `Cooperative-AI-Defense/hadamard/findings/OPEN_ORDERS.md` actually say?** Quote verbatim: the definition of *b*, what makes a
(*v*, *b*) pair **admissible**, whether the 126+ count is **computed or typed**, any upper bound on *b*,
and whether "all 13 orders" is FINDING_05's thirteen. Confirm or correct §1.

**Q2. Is the border axis independent of the Williamson/GS axis?** Given §2: does a bordered construction
at *b* ≥ 3 need a Williamson or GS quadruple as an ingredient, or does it not? **If it does, §8's
non-existence argument applies to it and the region inherits the retraction.** If it does not, say what
it needs instead. **This is the question that decides the brief** and it is a read, not a computation.

**Q3. Has anything screened *b* ≥ 3 since?** `../PLAN_2092.md` read ~15 of **163** findings and is dated.
How many exist now, and has any screened, entered, settled or abandoned *b* ≥ 3? **Was `FINDING_155`'s
ranking scoped to a single *b*?** If it ranked across *b*, nothing was ever unswept.

**Q4. Measure the border widths rather than relaying them.** `border.py` in this directory does it, and
**it was built and control-tested first** — Paley I detects exactly *b* = 1 at *q* = 7, 11, 19, 23;
Sylvester detects nothing; flipping one core entry stops detection; and a minimum-core guard exists
because the first version reported spurious large *b* on 1×1 cores. Run it on the hoa64 clone:

```
python3 border.py /path/to/hoa64/matrices
```

**Report the measured table** — order against the *b* values whose core is circulant. **An empty list is
a real result**, meaning the core is not circulant under this convention, and it tells us the convention
is different, which is itself the answer to part of Q1. The tool's limitation is stated in its
docstring: it implements **one** precise reading of "border of width *b* around a core", and a source
meaning block-circulant cores or non-leading borders will not be measured by it. **So get the convention
in Q1 and measure in Q4, in that order.**

## 4. The bar. Registered before dispatch; not to be re-scoped after.

> **PASS iff all three hold:**
> **(a)** `Cooperative-AI-Defense/hadamard/findings/OPEN_ORDERS.md` confirms the *b* > 2 pairs are at the **thirteen open orders**, and gives the
> admissibility condition; **and**
> **(b)** a bordered construction at *b* ≥ 3 **does not** require a Williamson or GS quadruple as an
> ingredient — i.e. the border axis escapes `../../playability/HADAMARD_CROSS.md` §8's non-existence argument; **and**
> **(c)** no finding since `../PLAN_2092.md` has screened, entered, settled or abandoned *b* ≥ 3, **and**
> `FINDING_155`'s ranking was scoped to a single *b*.
>
> **FAIL on any one.** Clause (b) is the decision: an axis that inherits the retraction is not a new
> region.

**`E: VOID`** remains available on positive sourced evidence that "all 13 orders" means hoa64's **solved**
thirteen rather than FINDING_05's open thirteen. §1 makes that unlikely; it costs nothing to keep.

**Grade every failed clause** (D54): **FAIL-ESTABLISHED** (positive evidence it fails) or
**FAIL-UNEARNED** (you could not establish it). Both block promotion, so hedging buys nothing, but they
are different facts and this project recorded them identically until a replication split two runs on
exactly that.

## 5. Budget — two numbers

**Cap: 25 reads or searches across the repositories.** No web access needed. **And a context ceiling:**
`Cooperative-AI-Defense/hadamard/findings/` holds 163+ documents, some long — prefer targeted greps,
read `Cooperative-AI-Defense/hadamard/findings/OPEN_ORDERS.md` in full and little else, and **say which of the two limits you stopped on.** A
previous brief stopped at 18 of 22 calls on context while the cap counted calls.

**A partial report is a success.** Q1 and Q2 answered with Q3–Q4 NOT REACHED is a complete run.

## 6. Rules. Each cost this project something real.

1. **A bar you cannot evaluate is FAIL**, graded FAIL-UNEARNED — never "unscored".
2. **Tier every claim.** `PRIMARY-VERIFIED-LOCALLY` / `SECONDARY-RELAYED` (you opened the file) /
   `OPERATOR-SUPPLIED` / `RECALL`. **Reading a document that quotes a file is not reading the file.**
3. **Check what object a computation is about, not just whether it is correct.** v1 of this brief derived,
   correctly, that a block count must be ≡ 4 (mod 8) — about the wrong object, since *b* is a border
   width. And debt **D53**: a verified computation licenses only the claim it computes.
4. **Search the local tree before claiming something is unworked.** v1 did not, and **D56** is the debt
   for it. Two documents in this repository already held three of its findings.
5. **Necessary is not sufficient.** Admissibility permits; it does not populate.
6. **Derive counts; never type them twice.** Say which command produced any count.
7. **Do not guess to produce a tidy verdict.** *"I could not establish this"* is required when true.

## 7. Report anything that contradicts this brief

§1's *b* definition is `OPERATOR-SUPPLIED`, not sourced. The identification of "all 13 orders" with
FINDING_05's thirteen is an **inference from co-location**, not a reading. §2 is `SECONDARY-RELAYED` from
`../../playability/HADAMARD_CROSS.md`, which **retracts part of itself**, so check which parts §8 leaves standing. **If one of
these is wrong it outranks the verdict.**

One thing is verified and you should use it rather than re-derive it: hoa64's 13 matrices are genuinely
Hadamard, checked in exact integer arithmetic in this repository. One thing is unresolved and small: my
recalled sub-2000 open list had **1004** where hoa64 ships **1852**, and whether 1004 is open,
closed-but-unshipped, or misremembered is **not established**. Say if you can settle it.

## 8. What to return

1. **The verdict line first**: `E: PASS` / `E: FAIL` / `E: VOID`, with **each failed clause's grade**.
2. **The bar quoted verbatim** from §4.
3. **Q1 in full**, since §1 and the bar both depend on it.
4. **Q2 next** — it decides the brief.
5. **Q3, Q4**, each tiered, naming the file you opened. Q4's measured table in full; **NOT REACHED** if
   you had no hoa64 clone.
6. **A finding count** for `Cooperative-AI-Defense/hadamard/findings/` against the 163
   `../PLAN_2092.md` saw, and **any path this brief cites that does not resolve** (this project carries
   89 broken cited paths, debt **D52**).
7. **Calls used against 25, and which limit you stopped on.**
8. **Anything contradicting §§1–2.**

**Do not recommend what to do next.** The verdict and the evidence are the deliverable.
