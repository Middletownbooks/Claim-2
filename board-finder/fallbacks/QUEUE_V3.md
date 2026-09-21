# The v3 queue — record problems, and why the pool already contained them

Built on `../gap/GAP_V3.md`. Everything below is **recall, not verified**; the first check named
for each is the promoting search that decides it, and is named before anyone looks so it cannot be
re-scoped afterwards.

## The move, in one line

v2's E dimension asked *"is the null publishable?"*, which rejects by construction the class where
the deliverable is cleanest. **Four record problems have been sitting in the unverified pool since
the v2 run, unpromoted, for exactly that reason.** They are the queue.

A record has a stated current value, so the three v3 dimensions are all computable *without a
literature survey*: **H** from the record itself, **Δ** from the table it lives in, **P** from
whether the record has moved recently.

## The evidence that this category is model-sensitive

DeepMind's FunSearch (Romera-Paredes et al., *Nature* 2024) used an LLM-driven search to improve
the **cap-set** record in AG(8,3). That is a direct existence proof that this exact class of
record problem moves under model capability — which is the `GAP_V3.md` §3 claim, demonstrated
rather than argued.

It cuts both ways, and the cut matters: **the flagship instance is taken.** The right reading is
to use FunSearch as evidence *for the category* and then pick a record inside it that FunSearch
did not touch. That is why cap sets are third below and not first.

## The queue

| # | candidate | pool id | table it moves | first check |
|---|---|---|---|---|
| **1** | **D-optimal designs of order 2*v*** | U13 | the D-optimal existence/determinant table (Fletcher–Koukouvinos–Seberry lineage) | current table: which *v* are open, and when was each last moved? |
| **2** | **Kissing-number lower bounds, dims 11–14** | U8 | the kissing-number table (Nebe–Sloane) | current τ*ₙ* lower bounds for *n* = 11–14 and the date each was last improved |
| **3** | **Caps in AG(7,3) / AG(8,3)** | U10 | the cap-set record table | post-FunSearch records, and whether anyone is still running on it |
| **4** | **Snake-in-the-box, dims 9–11** | U9 | the longest-induced-path record table | current records and the method that set them |

**Why 1 is first.** D-optimal designs are the nearest neighbour of the Hadamard machinery this
project already has — ±1 matrices, determinant maximisation, the same orbit and PAF apparatus —
so the algorithmic-idea gap, if there is one, is one we are already tooled for. They are also the
least famous of the four, which under `GAP_V3.md` §3 is a feature rather than a defect.

**Why 4 is last.** Snake-in-the-box has been attacked with genetic algorithms and SAT for
decades; the records are likely compute-set rather than idea-set, which is the category that does
not improve.

## A fifth candidate that is not in the corpus and needs the original instance

`Cooperative-AI-Defense/hadamard/findings/OPEN_ORDERS.md` says, of the thirteen open orders:

> *"Across all 13 orders there are 126+ admissible (v, b) pairs with b > 2."*

and, of orders 669 and 721:

> *"those two orders have never been screened or settled by anything in this repository."*

That is a **writable, un-swept region inside the primary thread**, requiring no new literature.
**But I cannot tell from outside whether it is live**: `FINDING_128` finds the *b* = 1 border
inert (for reverse-engineering — a different question), and `FINDING_133` reports the
orbit-reduction route stopping at *m* = 82 with failures that are emptiness rather than solver
weakness. **Question for the original instance, not a proposal from me:** is the *b* > 2 region
open, or closed by something I did not read?

## Direction B, answered with a number rather than a hunch

"Items closer to the head" was worth testing because collaboration routes concentrate there:

| rank band | records with a collaboration route |
|---|---|
| 1–100 | **48%** |
| 101–200 | 25% |
| 201–300 | 21% |
| 301–400 | 16% |
| 401–500 | 13% |

3.7× the density at the head. **But it does not convert.** Every head record in the discrete /
TCS / crypto domains with a route attached is a complexity separation — P vs NP, one-way
functions, NC vs P, P vs BPP, VP ≠ VNP, Unique Games, ETH, SETH, L vs NL, Hadwiger. Those have no
finite witness, no stated record, and a gap that is neither compute nor a bounded algorithmic
deficit but an open research programme. The collaboration density is real and it is attached to
problems where nothing we can do moves anything.

**So: head of the list, no. The collaboration routes worth harvesting are the ones on items we
already hold** — Hadamard (331), CC-6 (393), MUB (426) — and that is a harvest, not a target.

## Direction C, as an operating rule rather than a forecast

From `../gap/GAP_V3.md` §6, with no claim about what is coming or when:

1. **Run the screen wider, not deeper.** The expensive part of this session was reading and
   adjudicating — 41 Epoch entries, 499 corpus records, 163 findings, two papers. That is a
   breadth gap and it is the one that gets cheaper. A v3 screen that currently yields four
   candidates per expensive run should be run over a far larger candidate space instead of over
   one corpus again.
2. **Hold exactly one algorithmic-idea target and state its gap as a number.** Hadamard 2092
   qualifies: 0.503 against 0.252, from FINDING 157 §3. Nothing else on this board does.
3. **Stop holding compute-gap targets.** PTE 11 stays dead through any release.

## What would put something in the queue tomorrow

Any one of the four first checks above coming back with: *a record that has not moved in ten
years, in a table we can name, with a construction method we are already tooled for.* That is
three cheap lookups and it is the whole gate.
