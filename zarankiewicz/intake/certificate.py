"""
certificate.py -- the (4,6) counterexamples to Woodall's tight <=> pseudo-tight
conjecture, in checkable form.

CLAIM, precisely scoped.  Woodall p.663 records (i) "there may be some nontight sets
that are also pseudo-tight, although I do not know of any" and (ii) a conjecture that
an (m,n)-set is tight iff every (4,n)-subset of it is pseudo-tight.  At m=4 a set is
its own only (4,n)-subset, so each set below ANSWERS (i) affirmatively and REFUTES (ii).
It bears on neither Zarankiewicz nor Hill, and leaves the K7,7 / K7,9 verifications
untouched -- those consume the direction (not pseudo-tight => not a counterexample)
that this does not touch.

COUNTS.  n=6 exhaustive, 6,930 isomorphism classes:
  per reading   both 48,  walk 19,  path 54,  arbitrary 22     (NOT monotone)
  under EVERY reading  14      under SOME reading  59      reading-dependent  45
The 14 below are the reading-independent core.  n=5 exhaustive (131 classes) gives 0
under all four readings, but that is NOT evidence of structural absence: at the n=6
and n=7 rates (0.20%, 1.10%) the expected count over 131 classes is 0.26 to 1.45, so
P(observe 0) is 0.24 to 0.77.  No onset is claimed.
"""
CORE_14 = [
    # M as four cyclic orderings of {0..5}; antisums 15,15,16,16,16,18,18,19,19,19,21,21,22,22
    "012345 014532 032514 054231",
    "012345 013542 032541 045231",   # <- the published one, antisum 15
    "012345 013524 032541 045231",
    "012345 014532 032514 042315",
    "012345 013542 032541 042531",
    "012345 013542 032541 052314",
    "012345 013542 021453 031254",
    "012345 013542 032541 042513",
    "012345 013542 032415 042513",
    "012345 013524 032541 045213",
    "012345 013254 021534 052143",
    "012345 012453 023154 052143",
    "012345 013254 025134 052143",
    "012345 012453 031524 041325",
]
PUBLISHED = CORE_14[1]

# Verified facts about PUBLISHED (see reproduce.py --certificate):
#   antidistances (a0a1..a2a3) = 3,4,2,3,2,1 ; antisum 15
#   pseudo-tight witness N (a (6,4)-set), under the SMALLEST family 'both',
#     hence valid under every reading:
#       N0=(0,2,3,1) N1=(0,2,3,1) N2=(0,2,1,3) N3=(0,1,2,3) N4=(0,2,1,3) N5=(0,2,1,3)
#   shortest-antipath label-set sizes per M-pair: 1,3,1,1,1,1  -> 3 row-choices
#   each row-choice is already infeasible on a SMALL subset of N-indices:
#       choice 1: {2,3,4,5}    6^4 = 1,296 cases
#       choice 2: {0,1,3,4}    6^4 = 1,296 cases
#       choice 3: {0,1,2,3,4}  6^5 = 7,776 cases
#     so non-tightness is checkable without the full 6^6 enumeration.
#     No single column is universally dead -- all 64 masks over the six M-pairs are
#     realisable in CO_4 for SOME endpoint pair -- so the failure is jointly across
#     columns, not a one-line exclusion.
#   geometric realisation: a straight-line K_{4,6} drawing induces an isomorphic copy;
#     crossings by direct segment intersection = 37 > antisum 15, with 4 of 6 pairs
#     exceeding their antidistance, exactly as non-tightness predicts.

# m=5 PROPAGATION (verified directly on CO_5, NOT by Woodall's subset lemma):
#   extending each of the 14 by all 120 elements of V(CO_6):
#     pseudo-tight at 'both'                775 / 1680
#     not tight at 'arbitrary', DIRECT      775 / 775
#     undetermined 0 ; lemma violations 0
#   per core: 40 55 64 46 64 52 53 71 44 61 54 32 64 75
#   So the (5,n)-subset repair of Woodall's conjecture fails, and the repair family
#   "tight <=> every (k,n)-subset is pseudo-tight" is refuted AT m=k for every k with
#   a pseudo-tight-not-tight (k,n)-set.  Any repair must strengthen the PREDICATE on
#   subsets, not enlarge the subsets.


def parse(s, G6):
    return [G6.idx[tuple(int(c) for c in w)] for w in s.split()]
