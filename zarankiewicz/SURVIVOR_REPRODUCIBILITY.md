# Survivor files: sort before you compare

## The claim I should not have made

Commit 07d35b5 says of the shard the fifth restart killed:

> it was redone and its survivors are identical in content to what the discarded partial
> was accumulating

I never checked that. The partial was deleted unread, before any comparison was possible, so
the sentence asserts as observed something I could at best have argued from determinism. It is
pushed and stays; this file is the correction.

## What is actually guaranteed, and what merely happens

`search.c` writes a survivor the moment a worker reaches a qualifying leaf, under a mutex:

```c
if (survf && (survmax < 0 || (int)S <= survmax)) {
    pthread_mutex_lock(&survlock);
    fprintf(survf, "%d", (int)S);
    ...
```

The mutex serialises the *writes*. It does not order them. Which worker reaches a qualifying
leaf first depends on thread scheduling, so **line order is not guaranteed**. The set of
survivors is: the search is deterministic given the shard index, and `take_next()` hands out
prefixes in index order.

| | |
|---|---|
| the set of survivor lines | **guaranteed** identical across runs |
| their order in the file | **not** guaranteed |

## Measured

Three runs over the same 60-prefix strided slice, genuinely parallel at 2.83, 3.01 and 2.91
of 4 cores, 44,486,903 nodes each, 217 survivors each:

```
run1 vs run2 byte-identical : YES
run1 vs run3 byte-identical : YES
all three identical sorted  : YES
```

So in practice the files came out byte-identical, and the reason is visible rather than
mysterious: survivors are rare (217 in 44.5 million nodes), each prefix's survivors are
emitted in one contiguous burst while that prefix's subtree is searched, and prefixes are
claimed in index order. Bursts therefore tend to land in prefix order. "Tend to" is the
operative phrase — one prefix slow enough that a later prefix finishes first inverts two
bursts, and nothing prevents that.

A first attempt at this test proved nothing and looked like it had passed. `zsearch -m 7 -n 7`
with no `-startfile` reported 1.00 of 4 cores: parallelism comes from the prefix queue, which
only exists when there is a startfile, so the two "4-thread" runs I compared were both
single-threaded. The thread count on the command line is not evidence that threads ran.

## The rule

**Compare survivor files sorted.** `cmp -s <(sort a) <(sort b)`, never `cmp -s a b`. A bare diff
of two correct runs can report a mismatch, and on this evidence it would be the comparison that
is wrong, not the data.

This matters for anyone re-deriving a shard to check it — the other instance, a reviewer, or a
future session reconciling Kaggle output against local output. `sh_i.json` carries the
histogram and the level counts, which are order-free and are the right things to compare first.
