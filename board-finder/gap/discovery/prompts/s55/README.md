# Five self-contained briefs for a non-agent Sonnet 5.5 in chat

The Opus 5.5 discovery run spawned nine parallel agents and exhausted the session's search budget,
which is why arm 2's tables 6–10 and arm 2b were never assessed. Briefs A through C finish that
work from chat conversations instead, one brief per conversation, each with a hard query cap. **Brief
D is different in kind** — it reopens a cell those briefs closed, and §"Why brief D exists" below says
why that is not a re-scope.

| brief | finishes | cap |
|---|---|---|
| `A_DIVERGENCE.md` | arm 2b, the divergence search (P-35, still OPEN — the instrument has never produced an observation) | 25 |
| `B1_DESIGNS.md` | arm 2 tables 6–8: Williamson, Steiner systems, cyclic difference sets | 20 |
| `B2_SEQUENCES.md` | arm 2 tables 9–10: Costas arrays, bent functions | 14 |
| `C_ARM1_CELLS.md` | arm 1's five verdicts resting on a tier the container could not reach: 186, 277, 353, 375, 385 | 22 |
| `D_COSTAS.md` | phase 0 on **Costas arrays at order 32** — five literature reads against one registered bar | 20 |

`_SHARED.md` records the rules common to A–C; every brief repeats them so it stands alone. C's cap
was raised from 15 to 22 after 15 proved undersized for five source-reading questions at the observed
call-failure rate.

## Why brief D exists

B2 closed Costas at **S3, "method unread → UNKNOWN"**. That is an **access** failure — the publisher
page returned abstract and references only — and it is one of the six that opened **D50**: *a long run
of FAILs reads as a well-screened empty seam and may be a well-documented paywall.* Re-running a gate
whose input was never obtained is not the retroactive re-scope **D44** forbids, and the distinction is
recorded in `../../../../costas/PLAN_COSTAS.md` §1 so a later reader can check it rather than take it.

What is new is a local computation, `../../../../costas/costas_support.py`: **orders 31, 32 and 33 have no
Welch or Golomb array at any corner-deletion depth**, yet order 31 has ≥ 8 known arrays, so those are
necessarily sporadic — **a solved instance of the same unstructured problem 5.00 bits away.** Brief D
spends 20 calls establishing whether a structural lever exists before any Opus time is committed.

## Why re-run rather than accept the verdicts

`../../../SELECT_v1.md` §5 records that the Opus container **blocked arxiv.org, Wikipedia, every
publisher, and every maintained-table host probed** — Cohn, La Jolla, Brouwer, Packomania — leaving
web search and `raw.githubusercontent.com`. The same section rules that a cell seen only in a search
summary is `SEARCH-SUMMARY`, **RECALL-grade and not usable for any gate**, and states the consequence
itself: *"in this environment almost every literature cell will be `SEARCH-SUMMARY`, so no survivor
of this run can be more than triage-grade."*

**A chat instance reaches those hosts.** The C-3 gate run fetched a maintained cap table, cloned two
GitHub repositories and read arXiv papers in full. So the tier that the gates actually require,
`SECONDARY-RELAYED`, is achievable from chat and was not achievable from the container. That is the
whole reason to re-run, and it is stated as the job in every brief.

## Three things the briefs add that the originals lacked

**A hard query cap and an explicit partial-report rule.** The failure being fixed is a run that spent
its budget and recorded nothing, so every brief says a partial report is a success and asks for
unreached items to be named.

**S4 reported twice, prospectively.** `../../../RESULT_ARM2_TABLES.md` §3 concluded the crowding gate is scoped
wrongly — a table three AI systems moved neighbouring cells on is crowded even where one cell has not
moved — and registered the fix without applying it. The B briefs ask for both `S4-record` and
`S4-table` so the two scopings can be compared on real data for the first time. Not applied
retroactively to any existing verdict.

**Step (iii) named as the one that matters.** Opening the *method section* of the paper that last
moved a record is what S3 needs and is exactly what the container could never do. The B briefs order
the budget around it and say to drop it last.

## One reordering, with the reason

`A_DIVERGENCE.md` promotes SAT/CAS enumeration papers from third place to first. Such a paper's own
introduction routinely states *"previous methods reached n = X"*, which is a divergence served at
`SECONDARY-RELAYED` for a single fetch — the cheapest gate-usable cell available anywhere in this
work. It also carries forward the three refusals the earlier run earned: runtime ratios, the APN
dimension-8 "292× larger output" (a count, not a reach), and the Grothendieck constant (a method
class, not a frontier parameter). Two of those look like divergences until you ask what the parameter
is.
