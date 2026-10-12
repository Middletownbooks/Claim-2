# Handoff — drain the promoting-search queue

**For a Sonnet 5.5 instance in Claude Code, reasoning effort `max`.** Three lookups, four queue
items, bars all registered in advance. **You are not building a solver and not looking for a new
target.**

**This prompt is self-contained.** Every bar and every number you need is inline. A previous handoff
on this project cited repository paths that turned out to be private and a gate came back
provisional because of it; that is not repeated here. Paths are given as corroboration, never as a
dependency.

**One repository.** Everything is in the private repo you are working in — `board-finder/` holds the
research, `proof-protocol/` holds the ledger, debts and the 14 consistency checks. All paths below
are relative to the repository root. (Until recently the ledger lived on a branch of a public fork
of an unrelated upstream project; it has been consolidated here, so ignore any older document that
sends you to a second repository.)

---

## 0. Why you, and why this scope

You are near-parity with the frontier model on this exact class of work — locating a maintained
table, reading what it says, and deciding a registered threshold — and materially behind it on
agentic coding. **So this handoff is all lookup and adjudication and contains no engine work.** The
engine work (a Hadamard search at order 2092) is running elsewhere and is not yours. If you find
yourself writing a search, you have left the scope.

**Your run scores a registered prediction, and the way you can fail it is specific.**
`proof-protocol/ledger.json` P-31 A-1 claims that gate *execution* can move to a cheaper tier without
loss, because all the judgment in one of this project's gates is spent when the bar is written. The
registered threshold:

> **If one or more verdicts below is issued on a bar the run could not actually evaluate, A-1 is
> FALSE.**

So the single most valuable thing you can do is **say "I could not evaluate this bar" out loud when
that is the truth.** That is a PASS for the instrument and a FAIL for the gate, which is the
correct outcome and costs nothing. Guessing to produce a tidy verdict is the only real failure
available to you here.

---

## 1. Standing rules. Each one cost this project something real.

1. **A bar you cannot evaluate counts as FAIL, not "unscored."** These are go/no-go gates and the
   default is no.
2. **Single threshold, no middle band.** A previous gate registered a two-sided test with an
   unregistered gap, the answer landed in the gap, and it declined to score. If you find yourself
   wanting a middle band, say so in the write-up instead of inventing one.
3. **Tier every claim.** `PRIMARY-VERIFIED-LOCALLY` (you computed or checked it yourself),
   `SECONDARY-RELAYED` (a source says it and you read the source), `RECALL` (you believe it and the
   citation is not solid). **A `RECALL` cell with the value given is worth more than a confident
   cell with no tier** — this project's worst near-miss was a nine-year-stale recall that would
   have produced a fictitious worklist.
4. **Distinguish *numerical* from *exact*, and *claimed* from *refereed*.** This is the single
   failure mode that has cost this project the most. A breadth pass reported exact SIC-POVM
   constructions "reaching d=19,603"; a dedicated gate had already established the exact ceiling is
   **5,779**, with the 19,603 papers admitting their verification was "mostly partial." Both cells
   were true at their own precision. Only one was usable. **When a record's value depends on which
   sense is meant, report both senses or report NOT FOUND.**
5. **Withdrawn and unrefereed claims are data, not resolutions.** A claimed full resolution of the
   anisotropic Calderón problem (arXiv:2409.01583) was posted and withdrawn days later by its own
   authors — "the argument is incorrect" — and still recirculates in citation lists. If you find a
   resolution claim, check whether it stands.
6. **Derive counts, never type them twice.** If you state a count, produce it with a script and say
   which script.
7. **Negative-test anything you write.** Break each check deliberately and confirm it fails. Two
   checks written on this project in one day could not fail at all; one of them passed for hours
   while matching nothing, because a regex was escaped for a heredoc rather than for Python.

---

## 2. Search A — the maximal-determinant table. Do this one first; it can end two queue items.

**Background you need and nothing more.** For an *n* × *n* ±1 matrix, |det| ≤ *n*^(*n*/2) is
attained only for *n* = 1, 2 and *n* ≡ 0 (mod 4). For **n ≡ 2 (mod 4)** the maximum is the
**Ehlich–Wojtas** bound, (2*n*−2)(*n*−2)^((*n*−2)/2), and a matrix attaining it is a **D-optimal
design**. Writing *n* = 2*v* with *v* odd, the classical construction uses two **circulant** ±1
matrices *A*, *B* of order *v* with *AA*ᵀ + *BB*ᵀ = (2*v*−2)*I* + 2*J*, equivalently
**PAF_A(s) + PAF_B(s) = 2** for *s* = 1…*v*−1, with row sums satisfying **a² + b² = 4v − 2**.

Find the maintained maximal-determinant tables — the Orrick lineage, plus the Koukouvinos–Seberry
survey line, plus whatever has superseded them.

**A-1 (bar registered in `fallbacks/prompts/U13_D_OPTIMAL.md` as D1):**
> **PASS** iff the table exists, is dated, and the open *n* ≡ 2 (mod 4) orders form a **finite
> enumerable list**. Record which orders are known, which are open, and when each entry last
> changed. **FAIL** → report what the table actually is, and stop.

**A-2 (bar registered in `doptimal/PROMPT_U13_TRANSFER.md` §6.1):**
> **PASS** iff the set of open *n* ≡ 2 (mod 4) orders **intersects** the orders where a
> two-circulant construction is the live route. **FAIL** → say so and stop; the entire D-optimal
> parallel track is moot and that is a cheap, clean answer.

**A filter you can apply mechanically, and it is already verified.** A two-circulant design of
order *n* = 2*v* requires *a*² + *b*² = 4*v* − 2 = 2(2*v*−1), so **4*v*−2 must be a sum of two
squares** — i.e. every prime ≡ 3 (mod 4) divides 2*v*−1 to an even power. This is necessary before
any search. Verified here by exhaustion over all ±1 pairs: *n* = 14 has 392 designs, *n* = 18 has
1944, and **n = 22 has none at all**, because 4·11−2 = 42 = 2·3·7. Apply it to the open orders:

```python
import math
def two_squares(n):
    i = 0
    while 2*i*i <= n:
        j = math.isqrt(n - i*i)
        if j*j == n - i*i: return (i, j)
        i += 1
    return None
for n in OPEN_ORDERS:              # n = 2v, v odd
    print(n, two_squares(2*n - 2)) # 4v - 2 where v = n/2
```

Any open order failing this has no two-circulant design regardless of how much searching anyone
does. **Report the filtered list — that is the real answer to A-2.** (Corroboration:
`doptimal/transfer_check.py` and `doptimal/VERIFIED_OUTPUT.txt`.)

---

## 3. Search B — 239, odd perfect numbers. Two named risks, both registered before anything is built.

The tracked record: **a hypothetical odd perfect number N satisfies N > 10¹⁵⁰⁰** (Ochem–Rao,
*Math. Comp.* 81, 2012), by exhaustive branch-and-bound over factor chains. Published, refereed,
and **unmoved in publication for 14 years**. Also recorded: at least 101 prime factors with
multiplicity, largest component > 10⁶².

**B-1 — is the published record the real frontier?**
> Ochem is *reported* to have reached **10²⁰⁰⁰ unpublished**. **PASS** iff no credible report of an
> unpublished or in-progress bound beyond 10¹⁵⁰⁰ can be found. **FAIL** → beating a published
> record that a working researcher has privately passed is a weak position and it muddies the
> deliverable; say so and stop.

**B-2 — headroom, and it needs a measured cost, not an estimate.**
> **PASS** iff the 2012 computation's cost is documented well enough to compare against **10
> container-hours**, *and* that comparison leaves a reachable margin. **FAIL** → stop.

B-2 is the bar that killed the last two targets on this board, both of which were affordable and
worthless. An estimate with no measured or documented rate behind it **does not clear it** — that
is this project's most-repeated lesson: the same claim was wrong when guessed and right when
costed.

---

## 4. Search C — 345, Erdős–Szekeres. One read.

ES(6) = 17 is proven (Szekeres–Peters 2006, computer-assisted). **ES(7) is open, conjectured 33**;
Suk (JAMS 2017) gives ES(*n*) = 2^(*n*+o(*n*)) asymptotically.

Read **arXiv:2512.24061** (Bogdan, Dec 2025) — a SAT attack on ES(7) = 33 with UNSAT certificates
for anchored subfamilies, explicitly unresolved, citing **heavy-tailed solver runtime** as the
bottleneck.

**C-1:**
> **PASS** iff the paper leaves a *stated, unswept* subfamily whose closure would move the ES(7)
> bound, and names the cost of sweeping it. **FAIL** → stop.

**Register this before you read it.** The prior assessment on file is that C-1 **fails**: heavy-
tailed runtime in SAT is textbook, and the textbook fixes — randomised restarts and portfolios —
are already inside every modern solver. What this project holds that is not textbook is a
*measurement* discipline, and that is thin ground on which to claim an edge. **If you disagree
after reading, say why, with the specific subfamily and the specific cost.** Overturning a prior
with evidence is worth more here than confirming one.

---

## 5. If the gates fail early — and several are designed to

Do **not** go looking for a replacement target. That search has been run twice and returned empty
both times, and the reason is understood: a screen selecting for problems settled by one finite
object in a huge space is selecting for problems whose frontier is set by search capacity, which is
the one thing that does not improve with model capability. All 106 records of the corpus are mapped
and produced two candidates, both of which are in this queue.

**Spend the remainder on a verification sweep instead**, which is named work with a measured
justification. This project has shipped two checks that could not fail. In
`proof-protocol/tools/` there are 14 consistency checks; in `board-finder/` there are gate and
verifier scripts including `gap/epoch_gate.py`, `pte/verify.py` and `doptimal/transfer_check.py`.

> For each check: break it deliberately, confirm it fails, and record the break you used. Report
> any check that passes when it should not. **Do not fix a check without reporting it first** — a
> check that could not fail is a finding, and silently repairing it destroys the evidence.

---

## 6. What to write, and where

One document per search, under board-finder/fallbacks/, named "RESULT_S55_A_TABLE.md",
"RESULT_S55_B_239.md" and "RESULT_S55_C_345.md" (plain quotes deliberately, not backticks — this
tree runs a check that every backticked path resolves, and these three do not exist yet). Each
one:

1. **The verdict line first** — `A-1: PASS` / `A-1: FAIL` / `A-1: CANNOT EVALUATE`, then the bar
   quoted verbatim, then the evidence, then the tier.
2. **What you looked at**, including dead ends. A search that found nothing where something was
   expected is a result.
3. **Anything that contradicts this prompt.** Several numbers here are relayed rather than verified
   and are marked as such; if one is wrong, that is the most useful thing you can report.

Then update the queue table in `fallbacks/QUEUE_V3.md` and, if A-2 fails, say so at the top of
`doptimal/README.md`.

**Git.** Push to `claude/theorem-discovery-lab-jpbph1` — from whatever local branch your session
starts you on: `git push -u origin HEAD:claude/theorem-discovery-lab-jpbph1`.

**Another instance is working on that branch.** If the push is rejected, `git fetch origin
claude/theorem-discovery-lab-jpbph1` then `git merge FETCH_HEAD` — **never rebase, never
force-push.** Note that this repo only tracks `main`, so `origin/claude/...` is not a valid
revision locally; use `FETCH_HEAD` to compare.

**Before you finish**, run `proof-protocol/tools/check_consistency.py` — check 14 fails the build if
any backticked path you wrote does not resolve.

**Do not open a pull request** unless asked.

---

## 7. The one thing to carry through all three

Every bar above was written before anyone looked, by an instance that will not be scoring your
answers. **That is the point of the design: the judgment is already spent, and your job is to
evaluate honestly and to report the bars you cannot.** Three FAILs with clean evidence is a
complete, successful run and drains the queue. Three PASSes obtained by softening a threshold is a
failure that will be discovered later and will cost more than the searches did.
