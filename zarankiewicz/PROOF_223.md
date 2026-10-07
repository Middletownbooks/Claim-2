# cr(K_{7,11}) >= 223

The completed sweep proved that some (11,7)-set has antisum 219, which is a
ceiling on the pairwise method, not loose arithmetic: no amount of care with
antidistances alone can reach 225.  This document records a bound that goes
past it, by using the antidistances *together with* the complete bipartite
crossing numbers that are already theorems.

    cr(K_{7,11}) >= 223        (Z(11)Z(7) = 225, so the gap is now 2)

Nothing below assumes Zarankiewicz's conjecture anywhere.

## Inputs

1. **Woodall's pairwise bound.** In a good drawing of K_{7,n}, two 7-stars with
   rotations a, b cross at least dbar(a, b) times, the antidistance in CO_7.
   (Woodall 1993, J. Graph Theory 17(6) 657-671; this programme's `intake/cog.py`.)
2. **Two computer-verified crossing numbers.** cr(K_{7,7}) = 81 and
   cr(K_{7,9}) = 144 (Woodall 1993).  These two are the only ones the argument
   actually uses -- see the load-bearing table below.  cr(K_{7,8}) = 108 and
   cr(K_{7,10}) = 180 follow from them by step 3 and are in the code for
   completeness; cr(K_{7,k}) for k <= 6 is Kleitman 1970.
3. **Subset counting.** Every pair inside a k-subset S lies in exactly k-2 of
   the (k-1)-subsets of S, so crossings(S) >= ceil( sum of the sub-bounds / (k-2) ).
4. **This programme's completed sweep.** All 2400 shards; the minimum antisum
   over (11,7)-sets is 219, and every orbit with antisum <= 221 has at least one
   row on disk (`sweep_L5/low_*.txt`, 53,513,134 rows at 221 and 976 at 219,
   row-verified against `zpredict.py`'s independent derivation).
5. **A parity fact, proved here and used only for commentary.** CO_7 is
   bipartite and reversal flips the two colours, so dbar(a,b) = 1 + col(a) +
   col(b) mod 2 and the antisum of an m-multiset is C(m,2) + (m-1) * sum of
   colours mod 2.  For odd m the second term vanishes, so for m = 11 the antisum
   is **always odd**: 220 and 222 cannot occur.  (Checked at m = 2..12 against
   20,000 random multisets per m; the predicted parities match exactly.)

## The argument

Let D be a good drawing of K_{7,11}, M its multiset of eleven 7-star rotations,
T = antisum(M), and x_ij the actual crossings between stars i and j.  For every
subset S of the eleven stars, the sub-drawing on S is a good drawing of
K_{7,|S|}, so

    sum of x_ij over pairs inside S  >=  cr(K_{7,|S|})           for |S| <= 10
    x_ij                             >=  dbar(a_i, a_j)          for every pair

Pick any one subset S and bound the pairs outside it by their antidistances:

    crossings(D)  >=  ( T - antisum(S) )  +  cr(K_{7,|S|})
                  =   T  +  deficit(S),     deficit(S) := cr(K_{7,|S|}) - antisum(S)

So `T + max over S of deficit(S)` is a lower bound, computed exactly over all
2^11 subsets by `c/screen.c`.  Then:

* **T >= 223.**  Immediate: crossings >= T >= 223.
* **T <= 222.**  By input 5 the antisum is odd, and by input 4 nothing is below
  219, so T is 219 or 221, and M's orbit has a row on disk.  The deficit is
  orbit-invariant (relabelling preserves every antidistance -- checked over 60
  random elements of the group, which leave antisum 219, recursion 222 and LP
  223 unchanged), so the scan over the rows settles every such M.

The scan, over all 53,514,110 rows:

| bound `T + max deficit` | rows |
|---|---|
| 223 | 45,689,450 |
| 225 | 7,824,660 |
| below 223 | **0** |

Hence cr(K_{7,11}) >= 223.

### Which theorem does the work

Every single row has a positive deficit, and only two subset sizes ever supply
the maximum:

| subset size | deficit | rows | share |
|---|---|---|---|
| 7 | 2 | 31,182,358 | 58.27% |
| 9 | 2 | 14,506,116 | 27.11% |
| 9 | 4 | 7,825,636 | 14.62% |

So the proof rests on exactly cr(K_{7,7}) = 81 and cr(K_{7,9}) = 144 -- Woodall's
two computer results -- plus the sweep.  Deficits are always even, which the
parity fact of input 5 explains: for odd k the antisum of a k-subset has the
same fixed parity as Z(7)Z(k).

## The certificate for the 219 class

The whole orbit that attains 219 is settled by two lines of arithmetic.  With
the canonical representative

    M = [0, 0, 15, 74, 105, 438, 569, 647, 660, 671, 689]        antisum 219

drop the stars at positions 1 and 10 (rotations 0 and 689).  The remaining nine
rotations [0, 15, 74, 105, 438, 569, 647, 660, 671] have antisum **140**.  The 55 - 36 = 19 pairs outside that nine-subset have antisum **79**:

    crossings  >=  79 + cr(K_{7,9})  =  79 + 144  =  223

All 976 rows of the class give 223, and so does every one of 60 random
relabellings.

## 223 is exactly this method's ceiling

The single-subset form above is one feasible dual solution.  `mixedlp.py` solves
the full linear program -- minimise sum(x) subject to x_ij >= dbar and the subset
constraints for all 2026 subsets of size 3..10 -- which dominates every
combination of those constraints, and for the 219 class its optimum is **223**,
certified by a single dual variable of weight 1 on that nine-subset.  So no
re-weighting of these constraints reaches 224, and since the 219 orbit exists
combinatorially, the bound

    min over all (11,7)-multisets of the LP optimum  =  223

is exact.  Going further needs a constraint that is not in this family.  Three
candidates, in decreasing order of how well we understand them:

1. **Rotation-dependent triple bounds.**  Replace `cr(K_{7,3}) = 9` with
   c3(a,b,c), the true minimum over good drawings of K_{7,3} with those three
   rotations.  Any c3 above max(9, antisum) tightens the LP directly.  This is
   new topological input, not a re-use of what we have.
2. **The other side of the drawing.**  The seven 11-stars give 21 pairs in
   CO_11 (3,628,800 vertices, 11-regular, eccentricity 25, dbar(a,a) = 25 =
   Z(11); `c/co11.c` maps it in six seconds).  That bound is independent of
   everything above, and because the joint LP over both sides with
   sum(x) = sum(y) separates when the two rotation systems are left uncoupled,
   what matters is exactly: **is the minimum of the CO_11 seven-star antisum
   above 223?**  The staircase there is 223 -> 159 -> 106 -> 63 -> 31 -> 10, so
   every pair must have dbar <= 10, which is a ball of 289,763 of the 3.6M
   vertices.  `c/co11min.c` is the heuristic probe.
3. **Non-realisability.**  Killing the 219 orbit now buys nothing by itself:
   45,688,474 rows at antisum 221 also sit at 223, and the 223-antisum level
   (about 6.9e10 multisets, never enumerated) sits at 223 for free.  The
   realisability route would have to clear all of it.

## Reproducing

```sh
cd zarankiewicz
python3 -c "import sys;sys.path.insert(0,'intake');import cog,numpy as np;
c=cog.CO(7);np.array(c.antidist_matrix(c.dist_matrix()),dtype=np.uint8).tofile('A720.bin')"
cc -O2 -o c/screen c/screen.c
cat sweep_L5/low_*.txt | ./c/screen A720.bin 223 -     # expect "below 223: 0"

python3 mixedbound.py --selftest                       # counting arithmetic
python3 mixedlp.py   --selftest                        # LP >= recursion >= antisum
python3 mixedlp.py   --class 0,0,15,74,105,438,569,647,660,671,689 --certificate
pip install scipy                                      # mixedlp.py only
```

`mixedbound.py --selftest` includes the test that matters: with the cr clamps
set to zero the counting recursion collapses to the antisum **exactly**, because
sum over i of antisum(S minus i) = (k-2) * antisum(S) identically.  That isolates
the clamp as the only source of lift, so a bug in the counting cannot inflate
the bound silently.

## Caveat before anyone calls this new

The minimum antisum for (11,7)-sets, and this mixed bound, may already be in the
literature.  Check Woodall 1993, and de Klerk-Maharry-Pasechnik-Richter-Salazar
on semidefinite bounds for cr(K_{m,n}), before claiming any of it is new.  The
elementary counting bound alone already gives 220 -- C(11,9) = 55 nine-subsets,
each pair in C(9,7) = 36 of them, 55 * 144 / 36 = 220 -- so 219 never was the
state of the art, and 223 should be compared against 220, not against 219.
