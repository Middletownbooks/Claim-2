# Brief E (v3) — two questions. Clause (b) is discharged and the rest shrank.

**For a Claude Code instance with read access to `Middletownbooks/Cooperative-AI-Defense`, branch
`claude/hadamard-matrix-methods-vs79hi` — a PRIVATE repository, granted deliberately.** That is the
*only* access needed now. **No web search, no hoa64 clone** (see §4).

> **Versions.** v1 was written in ignorance of local prior work; `PRECHECK_E.md` records the three
> findings it duplicated and the one it resurrected after retraction. v2 had six questions. **v3 has
> two**, because the Hadamard worker discharged the decisive clause and a derivation replaced most of
> the rest. **Read §§1–3; they are short and they are what changed.**

---

## 1. Clause (b) is discharged: the border axis is NOT the Williamson axis

The Hadamard worker answered this directly (`SECONDARY-RELAYED` from its reply, structural details
marked KNOWN by it):

> **No Williamson or GS quadruple is needed as an ingredient, at any order.** The bordered construction
> at *b* ≥ 3 **is itself** a four-block Goethals–Seidel-type array. It sits on an abelian group *G* of
> order ***v* − *b***, with a relaxed target: **PAF sum −4*b* on a subgroup *H* of index *b*+1 minus the
> identity, and +4 off *H*.** The quadruple is the object you *search for* at order *v* − *b*; nothing
> comes from a pre-existing W(*m*). **None of the blocks in any of the 14 cores held is symmetric, even
> up to translation** — measured, not recalled. Williamson (four symmetric circulants) is the narrow
> special case.

**So the border axis is independent, and the clause the whole bar turned on PASSES.** Also located:
*b* = 5 at *v* = 347 (order 1388), *b* = 7 at *v* = 359 (1436), *b* = 3 at *v* = 479 (1916) — the whole
*b* = 3, 5, 7 trio.

**And two corrections to earlier versions of this brief, both accepted.**

* **There is no "decided Williamson frontier."** Turyn's construction gives W((*q*+1)/2) for *q* a prime
  power ≡ 1 (mod 4), which decides infinitely many *m* above 65, so the decided set is **not an
  interval**. v2's "38, 114 and 158 orders beyond the frontier" should read *beyond 65, the first
  undecided order* — a weaker claim. Derived here: for odd *m*, *q* = 2*m*−1 is ≡ 1 (mod 4) identically,
  so Turyn applies iff 2*m*−1 is a prime power; 125 = 5³ decides *m* = 63, 129 = 3·43 leaves 65 open, and
  205 = 5·41, 357 = 3·7·17, 445 = 5·89 mean **none of W(103), W(179), W(223) comes from Turyn.** Their
  status is individually **UNKNOWN**.
* **W(m) is decided for every *m* ≤ 64**: odd ≤ 59 exhaustively searched with none at 35, 47, 53, 59
  (Holzmann–Kharaghani–Tayfeh-Rezaie 2008); 61 and 63 by Turyn; even orders below 65 by
  Bright–Kotsireas–Ganesh (SAT+CAS, AAAI 2018). **65 is undecided.**

## 2. The admissibility condition, derived — and it disagrees with the 126+ figure

From §1's structure: a subgroup of index *b*+1 exists in an abelian group of order *v* − *b* only if
(*b*+1) | (*v* − *b*), and *v* − *b* = (*v*+1) − (*b*+1), so

> **(*b*+1) | (*v*+1),  with *b* odd.**

`PRIMARY-VERIFIED-LOCALLY` in `derive.py` §14, **asserted on all four (*v*, *b*) pairs now known**:
(347,5), (359,7), (479,3) and (523,1). Four for four.

Applied to FINDING_05's thirteen open orders, counting odd *b* with 3 ≤ *b* < *v*:

| *v* | order | # *b* ≥ 3 | | *v* | order | # *b* ≥ 3 |
|---|---|---|---|---|---|---|
| 515 | 2060 | 6 | | 647 | 2588 | 13 |
| 523 | 2092 | **2** — only {3, 261} | | 659 | 2636 | 14 |
| 537 | 2148 | **0** | | 669 | 2676 | 2 |
| 571 | 2284 | 6 | | 719 | 2876 | **22** |
| 573 | 2292 | 2 | | 721 | 2884 | **1** — only *b* = 37 |
| 599 | 2396 | 16 | | 739 | 2956 | 6 |
| 643 | 2572 | 6 | | | **total** | **96** |

**96, against the relayed "126+". A 24% shortfall, and adding *b* = 1 — admissible at every odd *v*,
since 2 | (*v*+1) — gives only 109.** So either my condition is stricter than the source's, or 126+
counts something else: a different thirteen, an extra family, or it is typed rather than computed.
**That is Q1, and it is much sharper than "what makes a pair admissible": a condition confirmed on the
source's own four examples returns the wrong total.**

**Three things in that table are decision-relevant on their own.** Order **2148 has no bordered route at
all**; order **2884 has exactly one**, *b* = 37; and the **live target 2092 has only {3, 261}**, sitting
almost at the *b* = 1 boundary — which is consistent with the live search being *b* = 1. **The richest
orders are 2876 (22), 2396 (16), 2636 (14), 2588 (13) — not the ones the *b* = 1 free-bit ranking points
at.** So if the border axis is worth anything, it points somewhere else than the current worklist.

## 3. What I could not compute, and the error that proves the point

I tried to tabulate orbit counts at *b* ≥ 3 from the largest odd divisor of *v* − *b*. It returned **2
orbits at *v* = 523 where `../PLAN_2092.md`'s verified sweep gives 58**, and that contradiction caught
it: the largest odd divisor is not the admissible *d*. **d must satisfy the row-sum law, and the law I
verified is the *b* = 1 one** — Σ*a_k*² = 4*v* with *a_k* = ±1 + *d*(2*u* − (*r*−1)). At *b* ≥ 3 the
target is §1's relaxed PAF condition, so that law does not apply and **I have no admissibility test for
*d* at *b* ≥ 3.**

**Therefore no free-bit or density figure at *b* ≥ 3 can be computed here.** That is clause (c) and it
is Q2. Applying a *b* = 1-fitted relation at *b* ≥ 3 is exactly the D53 trap and I nearly shipped a
table of it.

**Still verified and reusable:** `free_bits = 4(v−1)/d` exactly on all six `../PLAN_2092.md` rows,
`density = free_bits − log2 E[#sol]`, the *d*-sweep reproducing all six admissible-*d* lists, and all
thirteen orders uncovered by Paley I/II, Sylvester and Kronecker closure.

## 4. Two questions

**Q1. Why 96 and not 126+?** Quote `Cooperative-AI-Defense/hadamard/findings/OPEN_ORDERS.md` verbatim
on (i) what makes a (*v*, *b*) pair **admissible**, (ii) which thirteen orders it counts over, and
(iii) whether 126+ is **computed or typed**. Then say which side of §2's disagreement is wrong. **If the
source's condition is weaker than (*b*+1) | (*v*+1), give it** — that is the single most useful line you
can return, because it changes the per-order table and with it where the axis points.

**Q2. Is there a cost figure at *b* ≥ 3, and has anything screened the region?**
(i) Any free-bit, density or search-cost figure for a *b* ≥ 3 configuration — at a solved order (347,
359, 479 are the known ones) or an open one. §3 says why I cannot derive it. **Compare it to the live
target's 232 free bits / 2⁻¹⁴¹.**
(ii) `../PLAN_2092.md` read ~15 of **163** findings and is dated. **How many findings now, and has any
screened, entered, settled or abandoned *b* ≥ 3?** And **was `FINDING_155`'s ranking scoped to a single
*b*?** If it ranked across *b*, nothing was ever unswept and that ends the matter.

## 5. The bar. Clause (b) already discharged; you may not re-scope the rest.

> **PASS iff both remaining clauses hold:**
> **(a)** the source's admissibility condition and the thirteen it counts over are obtained, **and**
> §2's disagreement is resolved in a way that leaves a well-defined set of *b* ≥ 3 pairs at **open**
> orders; **and**
> **(c)** a free-bit or density figure for some *b* ≥ 3 configuration is obtained **and is better than
> the live target's 232 free bits / 2⁻¹⁴¹**.
>
> **(b) PASSES**, on §1: the bordered construction needs no Williamson or GS quadruple as an ingredient.
>
> **FAIL on either remaining clause.** **Grade each failure** (D54): **FAIL-ESTABLISHED** (positive
> evidence) or **FAIL-UNEARNED** (you could not establish it). Both block promotion; they are different
> facts.

**`E: VOID`** remains available only on sourced evidence that the thirteen are hoa64's **solved**
thirteen rather than FINDING_05's open thirteen. §2's table makes that unlikely.

**P-38 predicted FAIL and expected clause (b). That expectation is now falsified** — (b) passed cleanly.
The prediction stands as a threshold on (a) and (c).

## 6. Budget, and what not to do

**Cap: 20 reads or searches, all inside `Cooperative-AI-Defense`.** **And a context ceiling** —
`Cooperative-AI-Defense/hadamard/findings/` holds 163+ documents, some long. Prefer targeted greps; read
`Cooperative-AI-Defense/hadamard/findings/OPEN_ORDERS.md` in full and little else; **say which of the two limits you stopped on.**

**Do not** clone hoa64 or try to measure border widths from its matrices. v2 asked for that; it is
withdrawn. The border sits **within each block** of a four-block array, not on the leading rows of the
whole matrix, so `border.py` measures the wrong object — and hoa64's matrices are **normalized**, which
means sign flips and permutations that would destroy the block structure anyway. `border.py` is kept in
this directory with its controls, as a correct tool for the wrong question.

**Do not** re-derive §§1–3. **A partial report is a success**: Q1 answered with Q2 NOT REACHED is a
complete run.

## 7. Rules. Each cost this project something real.

1. **A bar you cannot evaluate is FAIL**, graded FAIL-UNEARNED — never "unscored".
2. **Tier every claim.** `PRIMARY-VERIFIED-LOCALLY` / `SECONDARY-RELAYED` (you opened the file) /
   `OPERATOR-SUPPLIED` / `RECALL`. **Reading a document that quotes a file is not reading the file.**
3. **A verified computation licenses only the claim it computes, and check what OBJECT it is about.**
   §3 is a live instance: a relation verified at *b* = 1, extrapolated to *b* ≥ 3, contradicted a verified
   table and was caught by that contradiction alone.
4. **Search the local tree before claiming something is unworked** (**D56** — v1 failed this).
5. **A threshold is not a frontier unless the set is an interval.** §1's Turyn correction is the third
   instance in this programme, after Costas's enumeration-versus-existence frontier and the two
   thirteens.
6. **Derive counts; never type them twice.** §2's 96 came from a script; say which command produced any
   count you state.
7. **Do not guess to produce a tidy verdict.** *"I could not establish this"* is required when true.

## 8. Report anything that contradicts this brief

§1 is `SECONDARY-RELAYED` from the Hadamard worker's reply and is the load-bearing item. §2's condition
is derived and confirmed on four pairs but **disagrees with the source's own total**, so at least one of
the two is wrong and it may be mine. The identification of "all 13 orders" with FINDING_05's thirteen is
an **inference from co-location**, not a reading.

**You are not expected to defer to this document.** Every previous brief in this series had its
load-bearing premise corrected by the run or the operator, and this one has been rewritten three times.

## 9. What to return

1. **The verdict line**: `E: PASS` / `E: FAIL` / `E: VOID`, with each failed clause's grade.
2. **The bar quoted verbatim** from §5.
3. **Q1 in full**, including the verbatim admissibility condition and your resolution of the 96/126
   disagreement.
4. **Q2**, tiered, naming the files you opened.
5. **A finding count** against the 163 `../PLAN_2092.md` saw, and **any path this brief cites that does
   not resolve** (this project carries 89 broken cited paths, **D52**).
6. **Calls used against 20, and which limit you stopped on.**
7. **Anything contradicting §§1–3.**

**Do not recommend what to do next.** The verdict and the evidence are the deliverable.
