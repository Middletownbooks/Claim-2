# Mapping chunk B — result

26 records, ranks 120–350, number theory and algebra.

```
NONE (structural, no tracked number)   3  (173, 175, 230)
NOT FOUND (no source located)          8  (147, 170, 173, 175, 211, 230, 252, 276) — all RECALL
RESOLVED in the last 90 days           0
CLOSED IN PRACTICE in the last 90 days 0
```

## 1. The chunk ordering holds so far

| | records | NONE | NOT FOUND | resolved ≤90d |
|---|---:|---:|---:|---:|
| **A** discrete / TCS / coding | 31 | **0** | **0** | 2 |
| **B** number theory & algebra | 26 | 3 (12%) | 8 (31%) | **0** |

B came in intermediate, as predicted. The prediction registered before these ran was about **C**,
and C is still the real test.

**The `NOT FOUND` rate is the more interesting number.** Zero in A, 31% in B — and every one is
tiered `RECALL` with the value still given. That is the tiering doing exactly its job: the sheet
distinguishes *"I found a source"* from *"I believe this"*, so the eight weak rows are visibly
weak instead of silently mixed in. A pass that fabricated sources would have looked better and
been worthless.

## 2. Turnover differs sharply by domain, and it inverts the strategy

On a matched 90-day window: **A gave 2 of 31, B gave 0 of 26.** Small samples, but the direction
matches the domains — discrete/TCS is the fast-moving one, number theory and algebra are slow.

That cuts both ways and the second way matters more:

> **The slow domain is safer from being swept, and also has almost nothing record-shaped in it.**

Of 26 records, **three** have `WHAT MOVES IT = computation` and the rest are `proof technique` or
`construction` on objects that are not finite searches. A domain that does not move is a domain
where there is nothing for us to move either.

## 3. The three computation-driven records, and only one survives reading

**239 — odd perfect number. The only chunk-B candidate worth gating.**
Tracked quantity: the lower bound on a hypothetical odd perfect number *N*.
Current: **N > 10¹⁵⁰⁰** (Ochem–Rao, *Math. Comp.* 81, 2012) — a published, refereed record,
**unmoved in publication for 14 years**. Method: exhaustive branch-and-bound over factor chains.
Also: at least 101 prime factors with multiplicity, largest component > 10⁶².

- **Δ (deliverable): clean.** A refereed number in *Mathematics of Computation*.
- **Shape: exactly what `QUEUE_V3.md` said to look for** — a stated current value, computation as
  the mover, and 14 years without publication movement.
- **Two named risks, both to be settled before anything is built:**
  1. Ochem is reported to have reached **10²⁰⁰⁰ unpublished**. Beating a published record that a
     working researcher has privately passed is a weak position, and it muddies Δ.
  2. The 2012 computation was presumably CPU-months. A container-hour against that is the
     headroom question that killed PTE 11 and the rings, and it must be costed first, not last.

**301 — normality of π. Reject.** The tracked quantity is digits computed: 314 trillion, Dec 2025,
a 110-day run on a custom server array. Pure hardware, a compute gap in its purest form, and it
says nothing whatever about the conjecture. This is the exemplar of what `GAP_V3.md` §3 says not
to hold.

**348 — Beal. Reject, on Δ.** Verified to 1000 in all six variables, but the "table" is Britannica
and a personal blog, not a maintained record. A $1M prize also guarantees a stream of junk
preprints, so a modest null extension would land in noise. Δ fails before headroom is reached.

## 4. Two shape observations worth keeping

**216, moonshine uniqueness — a writable unknown set of size one.** 70 of Schellekens' 71
holomorphic *c* = 24 VOAs now have both existence and uniqueness proven (van Ekeren–Möller–
Scheithauer 2020; Betsumiya–Lam–Shimakura 2023). **The one remaining case is the moonshine module
itself** — which is exactly this record's statement. The most writable unknown set this project
has ever seen, and completely unreachable: the residual case is a deep VOA problem, not a finite
search. Worth keeping as the exemplar that **writable does not imply attackable** — the same
lesson `D44` recorded when §6's "unswept implies attackable" branch failed.

**154, Cramér — a second AI-attributed result, of a different character to k-server.** An August
2026 manuscript credited to GPT-5.6 improves the *adjacent* Erdős large-gaps bound, partially
formalized in Lean by Boris Alexeev, with favourable but unrefereed commentary from Bloom, Maynard
and Green. Bloom's description is the notable part: *"purely elementary, could have been
discovered decades earlier."*

Set against k-server — where the model supplied a deep algebraic reformulation after humans did
the *k* = 3 case by hand — these are two different modes:

| | k-server (Sep 2026) | Erdős large gaps (Aug 2026) |
|---|---|---|
| human input | smallest open case, solved by hand | prompt |
| model contribution | reformulation that generalizes | an elementary construction nobody had tried |
| character | deep | *"could have been discovered decades earlier"* |

The second mode is the one that should worry a screen like ours, because it says the overlooked-
elementary-argument shelf is being cleared — and that shelf is where a small operation's best
odds were.

## 5. Queue after B

| | candidate | status |
|---|---|---|
| 1 | **U13 D-optimal designs** | unchanged, still first — the record table is public and maintained, and the PAF apparatus already exists |
| 2 | **239 odd perfect number** | **new from chunk B**, gated on the two risks in §3 |
| 3 | 345 Erdős–Szekeres | from chunk A, pending one cheap read of arXiv:2512.24061 |

Nothing else from 57 records across two chunks.
