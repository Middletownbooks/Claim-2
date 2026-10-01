# Woodall's 13,448 — the first validation against a published *class* count

Everything this programme had checked until now was a **count of nodes under the search's own
node-keep predicate**: 16,263,610 for (7,7), 809,438 leaves, and so on. Those are not published
quantities. They can be compared between the Python and the C, and they were — exactly — but they
cannot be compared with anything outside this tree. A whole day's confidence rested on internal
consistency.

Woodall (1993) reports **13,448 nonisomorphic (7,7)-sets at antisum 79**: the sets below
Z(7)Z(7) = 81 that he had to discharge to verify Zarankiewicz at K₇,₇.

So: emit the leaves, canonicalise them under the **full** automorphism group — `cog.class_canon`,
order 2·n! = 10,080, separately verified orbit-complete against brute force — and count distinct
classes.

```
leaves read               : 809438
antisum distribution      : {79: 809438}
isomorphism classes       : 13448
Woodall's published count : 13448
```

**Both hold.** Every leaf sits at antisum exactly 79, and the classes come to 13,448 on the nose.
`verify_woodall_13448.py`, 152 s.

## What that closes

> Woodall's paper → the staircase 79/56/36/21/9/3 → the node-keep predicate → the C port → the
> emitted leaves → back to Woodall's number.

Every link in that chain is now anchored at both ends. It is the difference between "the C matches
the Python" and "the pipeline computes the thing Woodall computed".

## And it prices the cheap canonical form at the leaves

809,438 nodes against 13,448 classes is a **60.2× duplication factor at depth 7** — the cost of
canonicalising under Stab(v₀), order 14, rather than the full 10,080. That is the measured version
of what the three-for-three "mismatch" was really about: the search's nodes were never classes, and
now the ratio between them is a number rather than an argument.

It also sets the expectation for the (11,7) sweep's output. A completed shard there emits 668,158
survivors of which **99.94% sit at the top rung 223 and 0.064% at 221**, with none below — and the
other instance's relayed frontier figure, which they had explicitly flagged as "a truncated-DFS
artifact and not a measurement", gave 288 at 221 against 475,733 at 223, a ratio of 0.061%.
**Their caveated number was right**, and a completed shard confirms it.

## Why survivors are emitted at all

Counting leaves cannot settle the conjecture. Each surviving (11,7)-set has antisum below
Z(11)Z(7) = 225 and has to be tested for realisability as an actual drawing — that is Woodall's
method, and the count alone discharges nothing. The sweep therefore records the histogram for every
rung and the full list for everything below the top rung; the top-rung lists run to terabytes and
are regenerable per shard, so they are not stored.
