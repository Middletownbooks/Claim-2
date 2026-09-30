#!/usr/bin/env python3
"""Re-derivation of every number the prior-work register cites.

Cycle 0's Task 1 asks for each attempted target's costed estimate "with the
arithmetic re-derived here". This file is that clause. Nothing below is copied
from the document it supports: each figure is recomputed from the stated inputs
and asserted against the value the register prints. A figure that cannot be
recomputed from inputs held locally is NOT asserted here -- it is tiered in the
register instead, which is the honest treatment.

Run: python3 register_arithmetic.py
"""
from math import comb, log2, factorial, isqrt
from itertools import combinations

FAIL = []
def check(label, got, want, tol=0.0):
    ok = abs(got - want) <= tol if isinstance(want, float) or tol else got == want
    print(f"  [{'ok ' if ok else 'FAIL'}] {label}: got {got!r}, want {want!r}")
    if not ok:
        FAIL.append(label)

# ================================================================== 1. PTE 11
print("1. PTE size 11 -- the cost curve that killed the target")
# Inputs, all PRIMARY-VERIFIED-LOCALLY from pte/: the search enumerates C(H,6)
# right-hand tuples at a measured 167,000-172,000 tuples/s (rate held constant
# to within 3% across a 38x range of H, per PREREG_PTE11 scoring of A-1).
RATE = 172_000.0          # tuples/s, top of the measured band
SEC_PER_YEAR = 365.25 * 24 * 3600

def pte_tuples(H): return comb(H, 6)
def pte_seconds(H): return pte_tuples(H) / RATE

check("tuples at H=50", pte_tuples(50), 15_890_700)
check("seconds at H=50", round(pte_seconds(50)), 92)          # doc says 96 s at 167k/s
check("tuples at H=80", pte_tuples(80), 300_500_200)
check("minutes at H=80", round(pte_seconds(80) / 60), 29)
check("tuples at H=3500", pte_tuples(3500), 2_542_222_346_415_251_500)
years_3500 = pte_seconds(3500) / SEC_PER_YEAR
print(f"       H=3500 costs {years_3500:,.0f} years at {RATE:,.0f} tuples/s")
check("years at H=3500 (to 3 s.f.)", round(years_3500, -3), 468_000.0, tol=1500.0)

# The compute multiplier from where the run actually stopped to the frontier.
mult = pte_tuples(3500) / pte_tuples(80)
print(f"       frontier/reached compute multiplier = {mult:,.3g}")
check("multiplier is ~8e9", round(log2(mult)), 33)
# And the height ratio a sixth power turns into that multiplier:
print(f"       height ratio 3500/80 = {3500/80:.1f}x, and {3500/80:.1f}**6 = {(3500/80)**6:,.3g}")
# Corollary 21 bought 17x in TUPLES, which in HEIGHT is the sixth root:
check("Corollary 21's 17x tuples = height factor (2dp)", round(17 ** (1/6), 2), 1.60)
print("  => THEORY-SHAPED. 8e9x compute under our method; the published frontier")
print("     was set by residue-class chaining we do not have (SECONDARY-RELAYED,")
print("     Coppersmith-Mossinghoff-Scheinerman-VanderKam 2024 sec 4.1).")
print()

# ============================================== 2. PTE unsearched rings (G2)
print("2. PTE rings -- the class-number list the paper got short")
def class_number_imag(d):
    """h(Q(sqrt(-d))) for squarefree d, by counting reduced forms of the
    fundamental discriminant."""
    D = -d if (d % 4) == 3 else -4 * d       # fundamental discriminant
    h = 0
    a = 1
    while 3 * a * a <= abs(D):
        for b in range(-a, a + 1):
            num = b * b - D
            if num % (4 * a): continue
            c = num // (4 * a)
            if c < a: continue
            if abs(b) > a or a > c: continue
            if (abs(b) == a or a == c) and b < 0: continue
            h += 1
        a += 1
    return h

squarefree = [d for d in range(1, 2000)
              if all(d % (p * p) for p in range(2, isqrt(d) + 1))]
h1 = [d for d in squarefree if class_number_imag(d) == 1]
check("h=1 for exactly the nine Heegner numbers", h1, [1, 2, 3, 7, 11, 19, 43, 67, 163])
PAPER_LIST = [1, 2, 3, 7, 11, 19, 43, 163]
missing = [d for d in h1 if d not in PAPER_LIST]
check("the paper's list omits d=67", missing, [67])
check("so the unsearched gap is three rings, not two", len(h1) - 6, 3)

# G2's premise-falsification, re-derived: lattice density is 2*pi*H/sqrt(|Delta|),
# so the thinnest ring that ever produced a solution is d=2 (|Delta|=8).
def disc(d): return -d if (d % 4) == 3 else -4 * d
for d in (43, 67, 163):
    thinner = (abs(disc(d)) / abs(disc(2))) ** 0.5
    print(f"       d={d:>3}: {thinner:.1f}x thinner than d=2, the thinnest ring with a find")
check("d=43 thinness (1dp)", round((abs(disc(43)) / abs(disc(2))) ** 0.5, 1), 2.3)
check("d=67 thinness (1dp)", round((abs(disc(67)) / abs(disc(2))) ** 0.5, 1), 2.9)
check("d=163 thinness (1dp)", round((abs(disc(163)) / abs(disc(2))) ** 0.5, 1), 4.5)
# d=163's norm form a^2+ab+41b^2: the only small norms are rational integers.
norms = sorted({a * a + a * b + 41 * b * b for a in range(-9, 10) for b in range(-9, 10)}
               - {0})
check("norms <= 20 represented in O_163", [n for n in norms if n <= 20], [1, 4, 9, 16])
print("  => THEORY-SHAPED, premise-falsifying: the region is unsearched because")
print("     it is a bad place to look, not for want of compute.")
print()

# ================================================================ 3. Costas 32
print("3. Costas arrays order 32 -- the 5-bit gap, and what it is a gap in")
# bits_search(n) = log2(n!) - log2(#solutions). The "5.00 bits from the target"
# framing is a statement about permutation space alone:
check("log2(32!) - log2(31!) is exactly log2 32", round(log2(factorial(32)) - log2(factorial(31)), 10), 5.0)
print(f"       so one order costs exactly 5 bits of permutation space, always;")
print(f"       the figure never depended on order 31 being a search result.")
# With C(31) >= 8 (SECONDARY-RELAYED) the order-31 search cost would have been:
print(f"       log2(31!) = {log2(factorial(31)):.1f} bits; minus log2(8) = "
      f"{log2(factorial(31)) - 3:.1f} bits of search, IF it were a search.")
print("     It is not: the 8 arrays are one dihedral class of Welch p=31 plus one")
print("     added corner dot (PRIMARY-VERIFIED-LOCALLY, ../../costas/costas_support.py")
print("     PART 7). => the positive control never existed.")
print("  => THEORY-SHAPED: the missing objects are a structural lever and a control.")
print()

# ============================================ 4. Hadamard, b>2 border region
print("4. Hadamard b>2 -- admissibility over the thirteen open orders")
F05_V = [515, 523, 537, 571, 573, 599, 643, 647, 659, 669, 719, 721, 739]
check("the thirteen", len(F05_V), 13)

def admissible(v, b):          # (b+1) | (v+1), from the four-block border structure
    return (v + 1) % (b + 1) == 0

odd_pairs  = [(v, b) for v in F05_V for b in range(3, v) if b % 2 == 1 and admissible(v, b)]
any_pairs  = [(v, b) for v in F05_V for b in range(3, v) if admissible(v, b)]
check("admissible pairs, b odd, 3 <= b < v", len(odd_pairs), 96)
check("admissible pairs, even b allowed (the source's rule as written)", len(any_pairs), 134)
ELEVEN = [v for v in F05_V if v not in (669, 721)]
eleven_any = [(v, b) for v in ELEVEN for b in range(3, v) if admissible(v, b)]
check("the eleven orders the source's code hard-codes", len(eleven_any), 126)
check("the pairs it then lists by hand for 669 and 721", len(any_pairs) - len(eleven_any), 8)
print("       so '126+' = eleven orders with even b included, plus two by hand.")

# b must be odd, re-derived: the border reduces to S with S S^T = 4cI - 4J, so
# the squared row-sum norm is 4c(b - c + 1), which at c = b+1 is zero.
for b in (3, 5, 7, 9, 37):
    c = b + 1
    check(f"squared row-sum norm at b={b}, c=b+1", 4 * c * (b - c + 1), 0)
print("       every row sum zero => each column is a zero-sum +-1 vector of")
print("       length c => c even => b odd. The source lists b = 4, 66, 334, 18, 360.")

# The region was already entered: border_S.py built S only for 4 < c <= 12.
built = [(v, b) for (v, b) in odd_pairs if b in (5, 7, 9, 11)]
check("pairs at b in {5,7,9,11} -- the worklist actually run", len(built), 18)
# RESULT_E.md left one question open: the source says "18 pairs across 8 of
# the 13 open orders", it reproduced 18 but counted 7, and asked which was
# right. Settled here: NO (b-range, parity) reading that preserves 18 pairs
# yields 8 orders. Under the only reading that gives 18 -- odd b in {5,7,9,11},
# i.e. 4 < c <= 12 -- the order count is FORCED to 7. The nearby readings:
for bs, lab in [((5, 7, 9, 11), "odd b in {5,7,9,11}"),
                (tuple(range(4, 12)), "any b, 4 < c <= 12 "),
                (tuple(range(3, 12)), "any b, c <= 12     "),
                ((3, 5, 7, 9, 11), "odd b, c <= 12     ")]:
    ps = [(v, b) for v in F05_V for b in bs if b < v and admissible(v, b)]
    print(f"       {lab}: pairs={len(ps):>3}  orders={len({v for v, _ in ps}):>2}")
check("orders spanned, under the reading that gives 18", len({v for v, _ in built}), 7)
check("and the 18-pair reading is unique among those four",
      sum(1 for bs in [(5, 7, 9, 11), tuple(range(4, 12)), tuple(range(3, 12)), (3, 5, 7, 9, 11)]
          if len([(v, b) for v in F05_V for b in bs if b < v and admissible(v, b)]) == 18), 1)
print("       => the source's pair count reproduces; its ORDER count does not.")
print("       Second failure of the same summary line, after '126+'.")
print("  => THEORY-SHAPED: admissible does not mean the border exists, and the")
print("     region was entered at 135 configurations with no solution. The")
print("     Williamson route W(103)/W(179)/W(223) is COMPUTE-SHAPED at distance")
print("     38/114/158 orders beyond the decided frontier at 65.")
print()

# ================================================ 5. Rota / Chow C(3), rank 4
print("5. Chow's Conjecture 2 -- the two counterexamples are different matroids")
P3 = 3
A = [[1,0,0,0,1,1,1, 1,1, 0, 1,0],
     [0,1,0,0,0,0,0, 1,0, 1,-1,0],
     [0,0,1,0,0,0,1, 0,0,-1, 0,1],
     [0,0,0,1,0,1,0,-1,0,-1, 1,1]]
COLS = [tuple(A[r][c] % P3 for r in range(4)) for c in range(12)]

def det4_mod3(cols):
    """Gaussian elimination over F_3; returns 0 iff singular."""
    M = [list(col) for col in cols]                 # 4 columns of length 4
    M = [[M[c][r] for c in range(4)] for r in range(4)]   # transpose to rows
    det = 1
    for i in range(4):
        piv = next((r for r in range(i, 4) if M[r][i] % 3), None)
        if piv is None: return 0
        if piv != i:
            M[i], M[piv] = M[piv], M[i]
            det = (-det) % 3
        det = (det * M[i][i]) % 3
        inv = pow(M[i][i], -1, 3)
        for r in range(i + 1, 4):
            f = (M[r][i] * inv) % 3
            if f:
                for c in range(i, 4):
                    M[r][c] = (M[r][c] - f * M[i][c]) % 3
    return det % 3

ours = sum(1 for S in combinations(range(12), 4) if det4_mod3([COLS[j] for j in S]))
check("our matroid: bases of the 495 four-subsets", ours, 240)
check("C(12,4)", comb(12, 4), 495)

# Allikvere's: K_5 with edge 34 tripled; bases = spanning trees of the multigraph.
E = ['01','02','03','04','12','13','14','23','24','34a','34b','34c']
def ends(e): return (3, 4) if e.startswith('34') else (int(e[0]), int(e[1]))
def is_spanning_tree(es):
    parent = list(range(5))
    def find(x):
        while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for e in es:
        a, b = ends(e); ra, rb = find(a), find(b)
        if ra == rb: return False
        parent[ra] = rb
    return True
alli = sum(1 for S in combinations(E, 4) if is_spanning_tree(S))
check("Allikvere's matroid: spanning trees", alli, 225)
check("the two counts differ, so the matroids differ", ours != alli, True)
print("  => NEITHER compute- nor theory-shaped. The binding constraint was")
print("     PRIORITY: Allikvere's preprint, 27 July 2026, weeks earlier.")
print()

# ========================================= 6. Record 239, odd perfect numbers
print("6. Record 239 -- the gap between the published and the private frontier")
check("orders of magnitude, published 10^1500 to private 10^2200", 2200 - 1500, 700)
check("composite-factor lists reach 10^2300, so the lead is", 2300 - 1500, 800)
# B-2's budget arithmetic, from Figure 2 of the author-hosted preprint.
hours = {"Thm 1 (N > 10^1500)": 12.0, "Thm 2 (Omega >= 101)": 93.0, "Thm 3 (component)": 0.5}
total = sum(hours.values())
check("documented hours in Figure 2", total, 105.5)
check("against a 10-container-hour bar (1dp)", round(total / 10, 1), 10.6)
check("Theorem 1 alone, over the bar (1dp)", round(12.0 / 10, 1), 1.2)
print("       and the paper excludes the factoring, which was volunteer-distributed")
print("       and never aggregated -- so the dominant cost is unreported.")
print("  => COMPUTE-SHAPED and already spent by the record's own authors. The")
print("     result that came out of working it was theory-shaped and unscored:")
print("     an error in Algorithm 1's program, accepted by Ochem by email.")
print()

# =============================================== 7. Record 345, ES(7) / Erdos-Szekeres
print("7. Record 345 -- the scale indicator, and the structural kill")
# compositions of 33 into ordered parts of size 3..6
def compositions(n, parts):
    dp = [0] * (n + 1); dp[0] = 1
    for t in range(1, n + 1):
        dp[t] = sum(dp[t - p] for p in parts if t - p >= 0)
    return dp[n]
check("compositions of 33 into parts 3-6", compositions(33, (3, 4, 5, 6)), 10_121)
print("       lower bound 33 by construction; only UNSAT over ALL 33-point sets")
print("       moves the upper bound, so no subfamily's closure can move ES(7).")
print("  => THEORY-SHAPED, and the bar asked the wrong question: it tested whether")
print("     a subfamily was unswept when no subfamily could have mattered.")
print()

# ================================================================== summary
print("=" * 72)
if FAIL:
    print(f"{len(FAIL)} CHECK(S) FAILED: {FAIL}")
    raise SystemExit(1)
print("All re-derivations agree with the figures the register prints.")
