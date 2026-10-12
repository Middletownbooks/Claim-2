# Brief F — records 239 and 345. Three registered bars, and two of them were written to fail.

**For a Sonnet 5.5 instance with web search and page fetching, in a chat conversation.** You have **no
repository and no filesystem.** Your output is a document you return in the reply.

**This brief cites no repository paths at all, deliberately.** A sibling brief was sent to an instance in
a different repository citing paths relative to the author's tree; the run correctly reported all three as
unresolvable, and the tool built to catch that had passed them because it checks the *author's* tree
(debt **D57**). **Resolvability is reader-relative.** Everything you need is inline.

**Budget: 22 search-or-fetch calls, plus a context ceiling.** Prefer abstract pages and HTML renditions
to full PDFs; a single large fetch can consume more of your real budget than several small ones. **Say at
the end which of the two limits you stopped on** — a sibling run spent 18 of 22 and stopped on *context*,
which is a datum the call count alone could not show. **A partial report is a success.**

---

## 1. Why these two, and why the bars are unflattering

These are the last two record-shaped candidates in a queue whose other four options are now all closed on
evidence. A handoff registered three bars for them **months before this brief**, and **two of the three
were written expecting to fail.** That is deliberate: the cheapest outcome is a clean kill, and the
project's standing rule is that a go/no-go default is *no*.

**Do not soften a bar to produce a survivor.** Six screens on this board have returned zero promotable
candidates; a seventh returning zero is a result, and a seventh returning a survivor obtained by relaxing
a threshold is a cost that surfaces later.

## 2. Record 239 — the lower bound on an odd perfect number

**The tracked value: a hypothetical odd perfect number *N* satisfies *N* > 10¹⁵⁰⁰.** Ochem–Rao,
*Mathematics of Computation* 81 (2012), by exhaustive branch-and-bound over factor chains. Published,
refereed, and **unmoved in publication for 14 years.** Also recorded: **at least 101 prime factors with
multiplicity**, and **largest component > 10⁶²**. All `RECALL`/`SECONDARY-RELAYED` — verifying them is
part of the job.

**A perfect number satisfies σ(*N*) = 2*N*.** Any odd perfect number must have **Euler's form**
*N* = *q*ᵃ·*m*², with *q* prime and *q* ≡ *a* ≡ 1 (mod 4), gcd(*q*,*m*) = 1.

**This snippet was written, run and negative-tested before you were given it.** Use it on any explicit
claim you meet — it is the cheapest sanity check on a relayed record:

```python
def sigma(n):
    total, m, p = 1, n, 2
    while p * p <= m:
        if m % p == 0:
            k = 0
            while m % p == 0:
                m //= p; k += 1
            total *= (p**(k + 1) - 1) // (p - 1)
        p += 1
    if m > 1:
        total *= (m + 1)
    return total

def is_perfect(n): return n > 1 and sigma(n) == 2 * n

# POSITIVE CONTROL: exactly four perfect numbers below 10^5.
assert [n for n in range(2, 100000) if is_perfect(n)] == [6, 28, 496, 8128]
# NEGATIVE TEST: the check must reject near-misses, or it proves nothing.
for n in (12, 24, 100, 495, 8129):
    assert not is_perfect(n)
# and none of them is odd, which is the record's direction at small scale
assert [n for n in (6, 28, 496, 8128) if n % 2 == 1] == []
```

### The two bars, quoted verbatim. Registered in advance; you may not re-scope them.

> **B-1 — is the published record the real frontier?**
> Ochem is *reported* to have reached **10²⁰⁰⁰ unpublished**. **PASS** iff no credible report of an
> unpublished or in-progress bound beyond 10¹⁵⁰⁰ can be found. **FAIL** → beating a published record that
> a working researcher has privately passed is a weak position and it muddies the deliverable; say so and
> stop.

> **B-2 — headroom, and it needs a measured cost, not an estimate.**
> **PASS** iff the 2012 computation's cost is documented well enough to compare against **10
> container-hours**, *and* that comparison leaves a reachable margin. **FAIL** → stop.

**"10 container-hours" is this project's budget unit**: roughly one ordinary cloud container running for
ten hours, no cluster and no GPU. **B-2 is the bar that killed the last two targets on this board**, both
of which were affordable and worthless. **An estimate with no measured or documented rate behind it does
not clear it** — that is this project's most-repeated lesson, and the same claim was wrong when guessed
and right when costed.

**The prior assessment on file, for you to agree with or overturn:** 239 is *"the only chunk-B candidate
worth gating"*, its deliverable is clean, and its shape is exactly right — a stated current value,
computation as the mover, 14 years without publication movement. **The two risks above are what it dies
of, if it dies.**

## 3. Record 345 — Erdős–Szekeres, the exact value of ES(7)

**ES(*n*)** is the smallest *N* such that any *N* points in general position in the plane contain *n* in
convex position. **ES(4) = 5, ES(5) = 9, ES(6) = 17** — the last proven by Szekeres–Peters (2006),
computer-assisted. **ES(7) is open and conjectured 33**, following the pattern ES(*n*) = 2^(*n*−2) + 1.
Suk (JAMS 2017) gives ES(*n*) = 2^(*n*+o(*n*)) asymptotically.

**Verified locally before this brief, so you can check the convex-position code rather than trust it:**
the standard ES(4) > 4 witness is a triangle with a point strictly inside — four points with no four in
convex position — and over the 5×5 integer grid, **all 25,052 general-position 5-subsets contain 4 in
convex position**, consistent with ES(4) = 5. Zero failures.

```python
import itertools
def cross(o, a, b):
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
def convex_hull(pts):
    pts = sorted(set(pts))
    if len(pts) <= 2: return pts
    lo = []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    up = []
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]
def in_convex_position(pts): return len(convex_hull(pts)) == len(set(pts))

# POSITIVE CONTROL
assert in_convex_position([(0,0), (1,0), (1,1), (0,1)])
# NEGATIVE TEST: triangle + interior point has NO 4 in convex position. MUST fire.
tri = [(0,0), (4,0), (0,4), (1,1)]
assert not in_convex_position(tri)
assert not any(in_convex_position(list(c)) for c in itertools.combinations(tri, 4))
```

### The bar, quoted verbatim

> **C-1:** **PASS** iff the paper leaves a *stated, unswept* subfamily whose closure would move the ES(7)
> bound, and names the cost of sweeping it. **FAIL** → stop.

**The paper the bar refers to**, and its existence and contents are **`RECALL` on this side**:

> arXiv:2512.24061 (Bogdan, Dec 2025) — a SAT attack on ES(7) = 33 with UNSAT certificates for anchored
> subfamilies, explicitly unresolved, citing **heavy-tailed solver runtime** as the bottleneck.

**Step one is establishing that this paper exists and says that.** This project has twice described a
paper from its title alone and been wrong, once *inside a prompt warning against it*. **If the identifier
is wrong, the paper does not exist, or it says something else, that finding outranks the verdict** and
you should stop and report it.

**The prior assessment on file says C-1 FAILS, and here is its reasoning so you can overturn it:**
heavy-tailed runtime in SAT is a textbook phenomenon, and the textbook fixes — randomised restarts and
portfolios — are already inside every modern solver. What this project holds that is *not* textbook is a
measurement discipline, and that is thin ground on which to claim an edge. **If you disagree after
reading, say why, with the specific subfamily and the specific cost.** Overturning a prior with evidence
is worth more here than confirming one.

**And one addition the bar does not contain, which you should answer separately.** C-1 asks whether the
*paper* leaves a subfamily unswept. **Also ask whether anything since has swept it.** A sibling brief's
clause tested whether one instrument had covered a region, got a true answer, and was wrong about the
world — four other instruments had covered it and found nothing (**D57**). **"Unswept according to one
source" is not "unswept."** Report this as a separate finding; it does not change C-1's verdict either
way.

## 4. Grading. Every failure gets one of two grades.

> **FAIL-ESTABLISHED** — you have positive evidence the bar fails (you found the unpublished bound; you
> found the cost and the margin is not reachable; you read the paper and it names no unswept subfamily).
> **FAIL-UNEARNED** — it fails only because you could not establish it (the paper was unreachable, the
> cost is undocumented, the searches came back empty).
>
> **Both block promotion**, so nothing is bought by hedging. But they are different facts, and this
> project recorded them identically until a replication split two independent runs of one brief on
> exactly that distinction — both compliant. **Name the grade for every bar you fail.**

**A bar you cannot evaluate is FAIL-UNEARNED, never "unscored."**

## 5. Provenance tiers. Every cell you report carries one.

| tier | meaning | gate-usable? |
|---|---|---|
| `PRIMARY-VERIFIED-LOCALLY` | you computed or checked it yourself | yes |
| `SECONDARY-RELAYED` | **you opened the source and read it** | yes |
| `SEARCH-SUMMARY` | seen only in a search result's snippet | **no — recall-grade** |
| `RECALL` | you believe it; no solid citation | no |

**Reading a document that quotes a source is not reading the source.** Also tag values
**EXACT / RIGOROUS-NUMERIC / NUMERICAL** and **REFEREED / PREPRINT / ANNOUNCED / WITHDRAWN**.

## 6. Rules that are not negotiable. Each cost this project something real.

1. **Single threshold, no middle band.** A previous gate registered a two-sided test with an unregistered
   gap, landed in the gap, and declined to score. If you want a middle band, say so in the write-up
   instead of inventing one.
2. **Distinguish *numerical* from *exact*, and *claimed* from *refereed*.** A breadth pass reported exact
   SIC-POVM constructions *"reaching d = 19,603"* where the exact ceiling was **5,779**, the higher papers
   admitting verification was *"mostly partial."* Both true at their own precision; one usable.
3. **Two quantities can share one name, and that is worse than two precisions of one.** A brief was sent
   out with *"enumeration reaches order 29"* as the answer to *"the smallest order with no known array,"*
   which is **32**. Three apart, both correct, different things. **For 239, watch the difference between
   a bound on *N*, a bound on its number of prime factors, and a bound on its largest component** — three
   different records that all read as "the odd perfect number bound."
4. **A threshold is not a frontier unless the set is an interval.** This project has made that mistake
   three times, most recently treating "the largest decided order" as a frontier when the decided set was
   scattered.
5. **Report the strength of a result, not only its existence.** A real refereed theorem was found that
   constrained a search space by **0.10 bits** — correct, and worth nothing. A "yes" that hides that is
   close to useless.
6. **Withdrawn and unrefereed claims are data, not resolutions.** A claimed resolution of the anisotropic
   Calderón problem (arXiv:2409.01583) was withdrawn days later by its own authors — *"the argument is
   incorrect"* — and still recirculates in citation lists. If you find a record claim, check it stands.
7. **Do not describe a paper from its title.** See §3. If you did not open it, write that you did not.
8. **Derive counts; never type them twice.** Say which script produced any count you state.
9. **Do not guess to produce a tidy verdict.** *"I could not establish this"* is required when true and
   costs nothing.

## 7. Report anything that contradicts this brief

The 10¹⁵⁰⁰ bound, the 101 prime factors, the 10⁶² component, the 10²⁰⁰⁰ report, ES(6) = 17, Suk's
asymptotic, and **the entire existence of arXiv:2512.24061** are relayed or `RECALL` here. **If one is
wrong that outranks all three verdicts.** The two code blocks are locally verified and you are invited to
break them.

**You are not expected to defer to this document.** Every brief in this series has had a load-bearing
premise corrected by the run or the operator, and the most valuable finding any of them produced came
from a run refusing a premise it had been told to treat as given.

## 8. What to return

1. **Three verdict lines first**: `B-1: PASS / FAIL` (+ grade), `B-2: PASS / FAIL` (+ grade),
   `C-1: PASS / FAIL` (+ grade).
2. **Each bar quoted verbatim** before its evidence.
3. **Per bar**: what you found, the source you actually opened, the tier, and for B-2 **the cost figure
   and its units** — a number with no documented rate behind it does not clear that bar.
4. **The separate "has anything swept it since" finding** for §3.
5. **Whether arXiv:2512.24061 exists and says what §3 claims.** First if it does not.
6. **Coverage of the negative.** B-1 is an absence claim if it passes: say where you looked.
7. **Calls used against 22, how many failed and why, and which limit you stopped on** — calls or context.
8. **Anything contradicting §§2–3.**

**Do not recommend what to do next.** The verdicts and the evidence are the deliverable; the decision
belongs to the instance holding the queue.
