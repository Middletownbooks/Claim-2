# Pre-registration — Report R: how many times does it compound?

Committed before any Round-4 search is run. Predictions in section 5, scored as
written.

## 1. The question Report Q leaves

Report Q established that carry-over transmits when the carried structure is
certified outside the receiving round's formation reach, and that the payoff was
two enabled invariants from seven carried terms: `is_prime_power` at cost 5 and
`odd_divisors` at cost 3, each composing a carried term with one the round formed
for itself. It explicitly did **not** establish compounding, and named the test:
run the design again with the enabled terms promoted, and re-certify.

That is this experiment, run as a **ladder** rather than a single comparison,
because the interesting quantity is not whether one more step exists but **how
many steps there are before it stops**.

## 2. The ladder

Every rung is a complete, **unbeamed, exhaustive** cost-≤5 outer search at body
budget 3, with unit cap 40 plus the carried atoms — the configuration Report Q
used for `A3u` and `B3u`, so rung 0 and rung 1 reproduce those two exactly.

```
rung 0   carry nothing                                    (= Report Q's A3u)
rung k+1 carry promote(certified set of rung k)            (rung 1 = Report Q's B3u)
```

`promote` is the frozen rule, unchanged and applied mechanically: *promote every
certified term, plus every formed term appearing as a named unit inside a
certified term*. The ladder stops when a rung certifies no invariant that the
previous rung did not — a fixpoint in the certified set, not in the atom set.

## 3. Two kinds of transmission, distinguished

Report Q's carried terms were outside the receiving round's reach. The terms
promoted at rung 2 and beyond mostly are **not**: `is_prime_power` was *found* by
rung 1 at cost 5. Carrying it at cost 1 does not extend reach, it **compresses
cost** — which is Report M's within-round mechanism, now applied across a round
boundary.

Each rung therefore classifies every newly carried term:

* **reach extension** — the receiving round cannot produce it at all within its
  budget (certified by exhaustive enumeration, as in Report Q);
* **cost compression** — the round can produce it, but at cost *c* > 1, and
  carrying it makes it cost 1. The certificate records *c*.

And every newly certified invariant is classified the same way: whether its
minimal term uses a carried atom, and whether it is reachable without one.

## 4. Controls at every rung

| control | what it holds fixed |
|---|---|
| **random** | the same NUMBER of carried terms, drawn with a fixed seed from the previous rung's formed pool, excluding anything semantically equal on TRAIN to a real carried term |
| **padded** | the same atom count, made up with the receiving round's own next-best formed units instead of carried ones |

Both are run at every rung that certifies something new, because the carried set
grows along the ladder and atom count grows with it.

## 5. Falsifiable predictions

| | prediction |
|---|---|
| **R-1** | rung 0 certifies 14 and rung 1 certifies 21, reproducing Report Q exactly |
| **R-2** | rung 2 certifies at least one invariant rung 1 does not |
| **R-3** | the ladder reaches a fixpoint within 5 rungs |
| **R-4** | at every rung, the random control certifies strictly fewer than the real carried set |
| **R-5** | at every rung, the padded control certifies no more than the previous rung |
| **R-6** | at least one rung ≥ 2 transmits by **cost compression** rather than reach extension — i.e. a newly certified invariant whose minimal term uses a carried atom that the round could itself have produced, but only at cost > 1 |
| **R-7** | the number of newly certified invariants per rung is non-increasing after rung 1 |

I expect R-1, R-3, R-4 and R-5 to hold. R-2 is the one I am unsure of, and R-6 is
the mechanism I expect if R-2 holds. If R-2 fails, transmission in this laboratory
is exactly **one step deep**, and the programme's loop does not compound even when
its precondition is certified — a sharper negative than Report P's, because the
redundancy explanation has already been removed.

## 6. What this cannot show

Same limits as Report Q, and one more: a ladder built by promoting a rung's own
certified set will eventually carry most of the library, at which point "certified"
stops meaning "discovered". The net-new count, which excludes any invariant equal
to a carried atom, is the only figure that should be read as discovery, and the
fixpoint is defined on it.
