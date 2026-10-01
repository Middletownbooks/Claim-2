#!/usr/bin/env python3
"""Woodall's 13,448: the strongest external check available, and nobody had run it.

Woodall (1993) reports 13,448 NONISOMORPHIC (7,7)-sets at antisum 79 -- the sets
that sit below Z(7)Z(7) = 81 and that he had to discharge by hand to verify
Zarankiewicz at K7,7.  Everything this programme has checked so far has been a
COUNT OF NODES under the search's own weak node-keep predicate, which is not a
published quantity and cannot be compared with anything outside this tree.

The 809,438 leaves the sweep emits are those nodes.  Canonicalising them under
the FULL automorphism group -- cog.class_canon, order 2*n! = 10,080, verified
orbit-complete against brute force -- turns them into isomorphism classes, which
IS a published quantity.

So this closes the loop end to end: Woodall's paper -> the staircase -> the
node-keep predicate -> the C port -> the emitted leaves -> back to Woodall's
number.  If it comes out at 13,448, every link held.
"""
import collections, pathlib, sys, time
sys.path.insert(0, 'intake')
from cog import CO, Z

SURV = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "surv77.txt")
t0 = time.time()
G = CO(7)
print("Z(7)Z(7) = %d ; the staircase's top rung is 79, so every leaf should sit at 79"
      % (Z(7) * Z(7)), flush=True)

anti = collections.Counter()
classes = set()
n = 0
for line in SURV.read_text().splitlines():
    if not line:
        continue
    parts = line.split(",")
    a = int(parts[0])
    M = tuple(int(x) for x in parts[1:])
    anti[a] += 1
    classes.add(G.class_canon(M))
    n += 1
    if n % 100000 == 0:
        print("  %d leaves, %d classes so far  [%.0f s]" % (n, len(classes), time.time() - t0), flush=True)

print()
print("leaves read              : %d" % n)
print("antisum distribution     : %s" % dict(sorted(anti.items())))
print("isomorphism classes      : %d" % len(classes))
print("Woodall's published count: 13448")
print()
ok1 = set(anti) == {79}
ok2 = len(classes) == 13448
print("  every leaf at antisum exactly 79 : %s" % ("YES" if ok1 else "NO -- %s" % dict(anti)))
print("  classes == 13,448                : %s" % ("YES" if ok2 else "NO"))
print()
if ok1 and ok2:
    print("BOTH HOLD.  The chain closes: Woodall's paper -> staircase -> node-keep")
    print("predicate -> C port -> emitted leaves -> Woodall's number.  And it gives the")
    print("collapse factor the weak predicate leaves on the table at depth 7:")
    print("  %d nodes / %d classes = %.1fx" % (n, len(classes), n / len(classes)))
    print("which is the price of the cheap canonical form, measured at the leaves.")
print("elapsed %.0f s" % (time.time() - t0))
sys.exit(0 if (ok1 and ok2) else 1)
