#!/usr/bin/env python3
"""Local re-derivation of every arithmetic claim in the v4 run's response.

The run is RELAYED: this session fetched none of its sources. What IS checkable
without fetching is the arithmetic, and all of it is checked here from the
stated definitions. A run whose arithmetic holds under independent derivation is
worth more than one whose conclusions merely agree.
"""
from math import comb

FAIL = []
def ck(label, got, want):
    ok = got == want
    print(f"  [{'ok ' if ok else 'FAIL'}] {label}: {got!r} vs {want!r}")
    if not ok: FAIL.append(label)

# ============================================ 1. Hill / cr(K_n)
print("1. Hill's conjecture at n = 13")
def H(n): return (n//2)*((n-1)//2)*((n-2)//2)*((n-3)//2)//4
ck("H(13) = 225", H(13), 225)
ck("H(12) = 150 (the K12 optimum)", H(12), 150)

# Each crossing uses 4 vertices, so deleting one vertex kills the crossings
# containing it; summing over all n vertices counts each crossing (n-4) times.
n = 13
ck("multiplier n-4 = 9", n - 4, 9)
print("      so 9*cr(D) = sum_v cr(D-v), and min_v cr(D-v) <= floor(9*cr/13):")
for c in (217, 219, 221, 223):
    thresh = (9 * c) // 13
    print(f"        cr(D) = {c}: 9c = {9*c:>5}, floor/13 = {thresh}  "
          f"({'exactly optimal' if thresh == H(12) else f'{thresh - H(12)} above optimal'})")
ck("threshold at 217 is the K12 optimum itself", (9*217)//13, 150)
ck("threshold at 219", (9*219)//13, 151)
ck("threshold at 221", (9*221)//13, 153)
ck("threshold at 223", (9*223)//13, 154)
print("      => the run's ladder holds: each step up the bracket needs K12")
print("         drawings with 1-2 more crossings. 151 is McQuillan-Pan-Richter's")
print("         stated subject, which is the 219 rung. Consistent with ALGORITHM")
print("         or FLOPS depth rather than missing theory.")
print()

# ============================================ 2. Zarankiewicz
print("2. Zarankiewicz at K7,11 and K9,9")
def Z(m, k): return (m//2)*((m-1)//2)*(k//2)*((k-1)//2)
ck("Z(7,11) = 225", Z(7,11), 225)
ck("Z(9,9)  = 256", Z(9,9),  256)
ck("Z(7,10) = 180 (the K7,10 optimum)", Z(7,10), 180)
ck("Z(8,9)  = 192 (the K8,9 optimum)",  Z(8,9),  192)

# A crossing uses 2 vertices from each side, so deleting one n-side vertex
# counts each crossing (n-2) times over the sum.
print("      (n-2)*cr(D) = sum over n-side v of cr(D-v):")
lo_711 = -(-(11 * Z(7,10)) // 9)          # ceil(11*180/9)
ck("K7,11 lower bound before parity: ceil(11*180/9)", lo_711, 220)
# Kleitman parity: for m,n both odd the crossing number has the parity of Z.
print(f"      Z(7,11) = 225 is ODD, and 7, 11 both odd, so cr is odd:")
ck("K7,11 bracket after parity", [c for c in range(lo_711, 226) if c % 2 == 1], [221, 223, 225])
lo_99 = -(-(9 * Z(8,9)) // 7)             # ceil(9*192/7)
print(f"      K9,9: 9*192/7 = {9*192/7:.2f}, so cr >= {lo_99}")
ck("K9,9 lower bound before parity", lo_99, 247)
ck("K9,9 bracket after parity (Z even)", [c for c in range(lo_99, 257) if c % 2 == 0][:1] +
   [max(c for c in range(lo_99, 257) if c % 2 == 0)], [248, 256])
# the run's premise-falsification arithmetic for K7,11 at 223
ck("a 223-drawing forces a K7,10 subdrawing <= floor(223*9/11)", (223*9)//11, 182)
ck("...which is 2 above the K7,10 optimum", (223*9)//11 - Z(7,10), 2)
print()

# ============================================ 3. skew-Hadamard at v = 89
print("3. Skew-Hadamard, smallest open order 356 = 4*89")
v = 89
ck("4v = 356", 4*v, 356)
ck("89 is prime", all(89 % p for p in range(2, 10)), True)
ck("|Z_89^*| = 88 = 8*11", v-1, 88)
odd_div = [d for d in range(1, 89) if 88 % d == 0 and d % 2 == 1]
ck("odd divisors of 88", odd_div, [1, 11])
print("      so the only nontrivial odd-order subgroup H has order 11;")
print("      -1 has order 2, hence -1 not in H. Cosets: 88/11 = 8, in 4 +- pairs.")
ck("number of cosets", 88 // 11, 8)
ck("+- pairs", (88 // 11) // 2, 4)
ck("H-invariant skew block choices: 2^4", 2**4, 16)
ck("each other block: 8 orbits + {0} -> 2^9", 2**9, 512)
total = 16 * 512**3
print(f"      total before parameter filtering = 16 * 512^3 = {total:,} = {total/1e9:.1f}e9")
ck("the run's 2.1e9", round(total/1e9, 1), 2.1)
print("      => the run's conclusion stands: the H-invariant region at order 356")
print("         is trivially searchable, which makes P (evidence against the object")
print("         in the cheap region) the dimension to settle, exactly as at the")
print("         PTE rings. UNSETTLED until Dokovic's searched orbits are obtained.")
print()

# ============================================ 4. Hirsch
print("4. Hirsch ladder")
ck("bracket m* in [7,19] has 12 open values", len(range(7, 19)), 12)
print("      lower side 7: Hirsch known for n-d <= 6; upper side 19 via a")
print("      24-vertex 5-prismatoid of width 6, Feb 2025. The run's recall")
print("      correction (20 -> 19) is the document's own most valuable line.")
print()

print("=" * 70)
if FAIL:
    print(f"{len(FAIL)} FAILED: {FAIL}"); raise SystemExit(1)
print("Every arithmetic claim in the run's response re-derives correctly.")
