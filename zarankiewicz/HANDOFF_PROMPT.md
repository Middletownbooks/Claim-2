# Handoff prompt

Paste the block below into a fresh Claude Code session that has access to
`Middletownbooks/Claim-2`.  It is written for a model being asked to do the
reasoning this programme could not: find the one new lemma, or close the
remaining gap of 2 by computation.

---

You are picking up a research-measurement programme on **Zarankiewicz's
conjecture at K_{7,11}**, in `Middletownbooks/Claim-2`, branch
`claude/zarankiewicz-k711`, directory `zarankiewicz/`.  Clone with
`--depth 1` -- the sweep data in the tree is 2.2 GB and all of it is tracked.

**Read `zarankiewicz/HANDOFF.md` first, then `zarankiewicz/PROOF_223.md`.**
Between them they state every result with the command that reproduces it.  Do
not re-derive what is already there; the whole point of the handoff is that the
finite computations are done.

## Where things stand

`Z(7,11) = 225`, the Zarankiewicz drawing achieves it, and K_{7,11} is the
frontier case: Kleitman settled `min(m,n) <= 6`, Woodall settled K_{7,7} = 81
and K_{7,9} = 144 by computer in 1993, and n = 8, 10 follow by counting.
Settling K_{7,11} also settles K_{7,12}.

Lower bounds, in order: the pairwise antidistance bound gives **219** (a
completed 2400-shard exhaustive sweep in this repo -- that is the minimum
antisum over all (11,7)-sets, not an estimate); elementary subset counting
already gives **220**; and `PROOF_223.md` gives **223** by combining the
antidistances with cr(K_{7,7}) and cr(K_{7,9}) over all 2^11 sub-drawings,
verified over all 53,514,110 rows the sweep wrote, zero of them below 223.
The gap to 225 is **2**.

That 223 is provably the ceiling of that whole method: the full LP over
`x_ij >= dbar` plus every subset constraint has optimum exactly 223 for the
orbit that attains antisum 219, certified by a single dual variable.  Going
further requires a constraint from outside that family.

## Your task, in priority order

The two cheap routes are gone (see 1 below).  What is left is one new lemma or
one genuinely stronger relaxation -- and, failing both, a rigorous write-up of
223 with a precise statement of the obstruction, which is itself a result.

1. **Both of the obvious routes are closed, and the second was closed inside
   the handoff session -- read why before proposing either.**  Woodall's bound
   also applies to the seven 11-stars in CO_11, giving an independent bound on
   the same crossings; a heuristic search there landed on 225 in 22 of 24
   restarts, which looked like the whole proof, and then one restart found a
   7-multiset of antisum **223**, re-verified by an independent breadth-first
   search sharing no query code.  On that side the subset clamps add nothing at
   all.  So the joint bound over both sides is 223: **that is the ceiling of
   Woodall's pairwise bound on either side of K_{7,11} combined with every
   complete bipartite crossing number currently known.**  Closing the last 2
   requires new mathematics, not a better search.

2. **Rotation-dependent triple bounds** (R2).  The LP's weakest input is the
   clamp cr(K_{7,3}) = 9.  Any lower bound c3(a,b,c) above max(9, antisum) for
   the true minimum over good drawings of K_{7,3} with those rotations tightens
   it directly, and only 2 is needed.  This is genuinely new topological input.
3. **An SDP / sum-of-squares lift** (R3).  219 is the value of a level-1
   relaxation; a level-2 lift over triples encodes the local-global consistency
   the pairwise bound throws away, and its dual is a short certificate -- the
   one proof object an exhaustive negative search cannot produce.
4. **Do not restart the realisability / order-type route** (R4).  It is closed
   by measurement (the achievable rotation set is not an order-type invariant:
   30 of 33 repeated order types gave different sizes), and it would not pay
   even if it worked, because the entire 223-antisum level -- about 6.9e10
   multisets, never enumerated -- sits at 223 for free.

Any lemma you propose must be consistent with two measurements that are not in
doubt: the antisum-219 orbit exists combinatorially (5040 members, 13 canonical
multisets, row-verified), and a genuinely achievable antisum-223 configuration
draws 387 crossings -- 304 after optimising placement -- with only 28 of 55
pairs attaining their antidistance.  Pair-optimality, not realisability, is the
obstruction.

## Before claiming novelty

Run the literature check this programme never did: Woodall 1993, J. Graph Theory
17(6) 657-671, and de Klerk-Maharry-Pasechnik-Richter-Salazar on semidefinite
bounds for cr(K_{m,n}).  The minimum antisum for (11,7)-sets, and the mixed
bound, may already be published.

## How this programme works, and please keep it that way

`zarankiewicz/INSTRUMENTS.md` logs every instrument and the mistake it caused;
`HANDOFF.md` has the short version.  The habits that earned their place: compute
the set before quoting a rank or a superlative; state the denominator; a range
over n observations constrains those n observations and nothing more; prefer a
check that reads the thing itself over one that reads bookkeeping about it;
validate a search on the real data, because random inputs made one validation
vacuous; power-analyse a hunt before running it; and never `pgrep -f`/`pkill -f`
a pattern that matches your own command line.

Operationally: develop and push only to `claude/zarankiewicz-k711`; another
instance may be on that branch, so **merge, never rebase, never force-push**; no
pull request unless asked; `pip install scipy` is needed for `mixedlp.py`;
regenerate `A720.bin` with the one-liner in `PROOF_223.md`; and the real gate is
`c/zsearch -m 7 -n 7` at 8.4 seconds, not `check_gate.py` at eleven minutes.
