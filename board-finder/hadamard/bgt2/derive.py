#!/usr/bin/env python3
"""What can be DERIVED locally about the b > 2 Hadamard region, before any claim
about it is repeated.

The option-3 queue entry rests on one sentence quoted from a file in ANOTHER
repository (Cooperative-AI-Defense, hadamard/findings/OPEN_ORDERS.md) that the
quoting instance never opened -- it read a plan that read that file. So the
symbol `b` in "126+ admissible (v, b) pairs with b > 2" is undefined here. This
script establishes what does not depend on knowing b, and states one hypothesis
about b with its falsifier.

Run: python3 derive.py
"""
import math

# ---------------------------------------------------------------- 1. the parametrisation
# From board-finder/hadamard/PLAN_2092.md sec 1.1, which states the law but whose
# sweep is reproduced here rather than trusted:
#   H of order 4v from b circulant blocks with row sums a_1..a_b, sum a_k^2 = 4v
#   (b = 4 is the Williamson / Goethals-Seidel array, the case the live work uses)
#   d is an odd divisor of v-1;  r = (v-1)/d + 1;  D = (r-1)/2
#   each row sum has the form a_k = +-1 + d*(2u - (r-1)),  u in {0..r-1}

def odd_divisors(m):
    return sorted((x for x in range(1, m + 1) if m % x == 0 and x % 2 == 1),
                  reverse=True)

def row_sum_values(v, d):
    """The a_k values the law permits at this (v, d), bounded by sum a_k^2 = 4v."""
    r = (v - 1) // d + 1
    lim = int(math.isqrt(4 * v))
    out = set()
    for u in range(r):
        step = d * (2 * u - (r - 1))
        for s in (+1, -1):
            a = s + step
            if abs(a) <= lim:
                out.add(a)
    return sorted(out), r

def admissible(v, d, b=4):
    """Can b row sums from the permitted set square-sum to exactly 4v?"""
    vals, r = row_sum_values(v, d)
    sq = sorted({a * a for a in vals})
    target = 4 * v
    # can we write target as a sum of exactly b squares from sq (with repetition)?
    reach = {0: 0}
    cur = {0}
    for _ in range(b):
        nxt = set()
        for t in cur:
            for s in sq:
                if t + s <= target:
                    nxt.add(t + s)
        cur = nxt
    return target in cur, r

def sweep(v, b=4):
    ok = [d for d in odd_divisors(v - 1) if admissible(v, d, b)[0]]
    if not ok:
        return None
    d = max(ok)
    r = (v - 1) // d + 1
    D = (r - 1) // 2
    return ok, d, r, D

# ---------------------------------------------------------------- 2. reproduce the table
print("=" * 74)
print("1. PLAN_2092.md sec 1's table, reproduced independently (b = 4)")
print("=" * 74)
TABLE = {   # v: (admissible d list, d, r, D, free_bits, log2E, density_exp)
    487: ([9, 3, 1], 9,  55,  27, 216,  83.9, 132),
    523: ([9, 3, 1], 9,  59,  29, 232,  90.9, 141),
    571: ([5, 3, 1], 5, 115,  57, 456, 172.8, 283),
    643: ([3, 1],    3, 215, 107, 856, 308.0, 548),
    659: ([7, 1],    7,  95,  47, 376, 132.7, 243),
    739: ([9, 3, 1], 9,  83,  41, 328, 117.0, 211),
}
print(f"  {'v':>4} {'4v':>6} | {'claimed d':>12} {'mine':>14} | "
      f"{'r':>4} {'D':>4} | free bits")
allok = True
for v in sorted(TABLE):
    claim_ds, cd, cr, cD, cfb, clg, cden = TABLE[v]
    got = sweep(v)
    ds, d, r, D = got
    match = (ds == claim_ds and d == cd and r == cr and D == cD)
    allok &= match
    print(f"  {v:>4} {4*v:>6} | {str(claim_ds):>12} {str(ds):>14} | "
          f"{r:>4} {D:>4} | {cfb:>5}   {'OK' if match else 'MISMATCH'}")
assert allok, "the d-sweep does not reproduce PLAN_2092's table"
print("  ASSERTED: all six rows reproduce, d list included.")

# the two relations the table satisfies but never states
print()
print("  Two relations PLAN_2092 does NOT state, holding on all six rows:")
for v in sorted(TABLE):
    _, _, r, D, fb, lg, den = TABLE[v]
    assert fb == 8 * D == 4 * (r - 1), (v, fb, D, r)
    assert abs((fb - lg) - den) < 0.35, (v, fb - lg, den)
print("    free_bits = 8D = 4(r-1)                     -- exact, all six")
print("    density exponent = free_bits - log2 E[#sol] -- all six to <0.35")
print()
print("  CONSEQUENCE, and it is the useful part: free_bits is a function of d")
print("  alone, via r = (v-1)/d + 1. So the entire difficulty ranking of the")
print("  worklist is decided by ONE arithmetic quantity -- the largest odd")
print("  divisor of v-1 that the row-sum law admits. Nothing about the search.")

# ---------------------------------------------------------------- 3. the classical thirteen
print()
print("=" * 74)
print("2. The classical thirteen smallest open Hadamard orders")
print("=" * 74)
print("  The ORDER LIST is RECALL, not verified here -- flagged, and step 1 of")
print("  the brief is to check it against the other repository:")
CLASSICAL = [668, 716, 892, 1004, 1132, 1244, 1388, 1436, 1676, 1772, 1916, 1948, 1964]
def isprime(m):
    if m < 2: return False
    if m % 2 == 0: return m == 2
    i = 3
    while i * i <= m:
        if m % i == 0: return False
        i += 2
    return True
print(f"  {len(CLASSICAL)} orders, all divisible by 4: "
      f"{all(n % 4 == 0 for n in CLASSICAL)}")
print(f"  v = n/4 all prime: {all(isprime(n // 4) for n in CLASSICAL)}")
print()
print(f"  {'order':>6} {'v':>5} {'d':>4} {'r':>5} {'D':>5} {'free bits':>10}")
for n in CLASSICAL:
    v = n // 4
    got = sweep(v)
    if got is None:
        print(f"  {n:>6} {v:>5}    -- no admissible d at b=4")
        continue
    ds, d, r, D = got
    print(f"  {n:>6} {v:>5} {d:>4} {r:>5} {D:>5} {8*D:>10}")

print()
print("  AND A DISCREPANCY THAT MATTERS: the repo's six targets are")
print("  v = 487, 523, 571, 643, 659, 739 -> orders 1948, 2092, 2284, 2572,")
print("  2636, 2956. Only 1948 is in the classical thirteen. So 'the thirteen")
print("  open orders' in the quoted sentence and 'thirteen' in the repo's own")
print("  target ranking are DIFFERENT LISTS, or one of them is not what I think.")
print("  Two quantities sharing a name -- resolve before using the 126+ figure.")

# ---------------------------------------------------------------- 4. 669 and 721
print()
print("=" * 74)
print("3. Orders 669 and 721, said never to have been screened")
print("=" * 74)
def fac(m):
    out, x, p = [], m, 2
    while p * p <= x:
        while x % p == 0: out.append(p); x //= p
        p += 1
    if x > 1: out.append(x)
    return out
for m in (669, 721):
    print(f"  {m}: mod 4 = {m % 4}, factors {fac(m)}, prime: {isprime(m)}")
print()
print("  A Hadamard matrix of order > 2 requires order = 0 mod 4. Both are 1 mod 4,")
print("  so NEITHER IS A HADAMARD ORDER. They must be v or m values, giving")
print(f"  orders 4*669 = {4*669} and 4*721 = {4*721}.")
print("  And both are COMPOSITE, while every v in the repo's worklist is prime.")
print("  HYPOTHESIS, offered as such: they were never screened because the")
print("  machinery assumes v prime. Falsifier: the other repo screening a")
print("  composite v anywhere. This is a guess about a file I have not read.")
for m in (669, 721):
    got = sweep(m)
    print(f"    v={m}: admissible d at b=4 -> "
          f"{got[0] if got else 'NONE'}"
          + (f", d={got[1]}, r={got[2]}, D={got[3]}, free bits {8*got[3]}" if got else ""))

# ---------------------------------------------------------------- 5. the b hypothesis
print()
print("=" * 74)
print("4. One hypothesis about b, with its falsifier. NOT a finding.")
print("=" * 74)
print("  free_bits = 8D at b = 4. If the b blocks each contribute 2D free bits,")
print("  then free_bits = 2*b*D, which fits 8D at b=4 -- a relation fitted at a")
print("  SINGLE value of b, which is exactly the D53 trap. Stated as a")
print("  hypothesis with the number it predicts, so it can be killed:")
print()
print(f"  {'b':>3} {'2bD at v=523, D=29':>20} {'vs b=4':>10}")
for b in (2, 3, 4, 5, 6, 8):
    print(f"  {b:>3} {2*b*29:>20} {2*b*29 - 232:>+10}")
print()
print("  IF that scaling is right, b > 2 is a region with MORE free bits than")
print("  b = 2, i.e. HARDER, and the 126+ admissible pairs are not a cheaper")
print("  frontier but a more expensive one. FALSIFIER: any statement in the")
print("  other repo giving free bits or density for a b != 4 case. One number")
print("  kills or confirms this, and the brief asks for it first.")
print()
print("  Separately, admissibility counted under the b-blocks reading:")
print(f"  {'b':>3} {'admissible v of the classical 13':>34}")
for b in (2, 3, 4, 5, 6, 8):
    ok = [n // 4 for n in CLASSICAL if sweep(n // 4, b) is not None]
    print(f"  {b:>3} {len(ok):>4}  {ok if len(ok) < 14 else ''}")
print("  This is a DERIVED count under MY reading of b (number of circulant")
print("  blocks, sum of b row-sum squares = 4v). If the other repo's b means")
print("  something else, every number in this block is void. Check first.")
print()
print("=" * 74)
print("ALL ASSERTIONS PASSED.")
print("=" * 74)


# ---------------------------------------------------------------- 6. b mod 8
print()
print("=" * 74)
print("5. MY READING OF b IS REFUTED BY THE SENTENCE IT WAS MEANT TO CHECK")
print("=" * 74)
# a_k = +-1 + d(2u - (r-1)). v odd => v-1 even => (v-1)/d even (d odd) => r odd
# => r-1 even => d(2u-(r-1)) even => a_k odd. Always.
for v in list(TABLE) + [167, 179, 491, 669, 721]:
    for d in odd_divisors(v - 1):
        vals, r = row_sum_values(v, d)
        assert r % 2 == 1, (v, d, r)
        assert all(a % 2 != 0 for a in vals), (v, d)
print("  ASSERTED: every permitted row sum a_k is ODD, at every (v, d) checked.")
print("  Because v is odd, so (v-1)/d is even for odd d, so r is odd, so")
print("  d(2u-(r-1)) is even, so a_k = +-1 + even is odd.")
print()
print("  An odd square is 1 mod 8. So a sum of b odd squares is b mod 8.")
print("  And 4v with v odd is 4 mod 8. Therefore:")
print()
print("      sum_{k=1..b} a_k^2 = 4v  forces  b = 4 (mod 8).")
print()
for b in range(2, 30):
    feas = (b % 8 == 4)
    ok = [n // 4 for n in CLASSICAL if sweep(n // 4, b) is not None]
    assert (len(ok) > 0) == feas or len(ok) == 0, (b, len(ok))
    if feas or len(ok):
        print(f"    b={b:>3}: b mod 8 = {b%8}, admissible v of the 13: {len(ok)}")
print()
print("  So under my reading, b > 2 means b in {12, 20, 28, ...} and NOTHING")
print("  else -- there is no b = 3, 5, 6 or 8 case at all. A source reporting")
print("  '126+ admissible (v, b) pairs with b > 2' therefore CANNOT mean b =")
print("  the number of circulant blocks whose odd row sums square-sum to 4v.")
print()
print("  THIS IS THE MOST USEFUL THING IN THIS SCRIPT. It does not tell us what")
print("  b is; it proves my guess is wrong, so the brief must not ship the guess.")

# ---------------------------------------------------------------- 7. the 721 lead
print()
print("=" * 74)
print("6. One lead worth checking, and one reason to distrust it")
print("=" * 74)
g = sweep(721)
print(f"  v=721 (composite, 7*103) admits d=15, r=49, D=24, free bits {8*g[3]}.")
print(f"  v=487, the order Alpoge SOLVED, has free bits 216.")
print(f"  v=523, the LIVE target, has free bits 232.")
print(f"  So on the free-bit metric 721 is {216 - 8*g[3]} bits cheaper than the")
print("  solved order and", 232 - 8*g[3], "cheaper than the live target.")
print()
print("  WHY TO DISTRUST IT: free bits is only one of the two coordinates.")
print("  density = free_bits - log2 E[#sol], and E[#sol] needs the constraint")
print("  count, which I cannot compute without the repo's estimator. A cheap")
print("  free-bit count with few solutions is not an easier target. Also")
print("  unverified: whether 4*721 = 2884 is an OPEN order at all.")
print()
print("=" * 74)
print("ALL ASSERTIONS PASSED (part 2).")
print("=" * 74)


# ---------------------------------------------------------------- 7. b DEFINED
print()
print("=" * 74)
print("7. b IS A BORDER WIDTH. Operator-supplied, 30 Sep 2026.")
print("=" * 74)
print("  Section 5's refutation stands and is now explained: b is not a block")
print("  count at all, so the b = 4 (mod 8) derivation was about the wrong")
print("  object. The definition, OPERATOR-SUPPLIED (not read from the source):")
print()
print("    b is a BORDER WIDTH. A bordered example is a border of width b")
print("    around a core. b must be ODD. Of Alpoge's 12 examples, 7 are")
print("    bordered; the majority of those are b=1, and there is one each")
print("    at b=3, b=5, b=7.")
print()
# the decomposition this forces, checked for consistency
bordered, b357 = 7, 3
b1 = bordered - b357
unbordered = 12 - bordered
assert b1 == 4 and unbordered == 5
assert b1 > b357, "b=1 must be the majority of bordered examples"
print(f"  FORCED DECOMPOSITION of the 12, and it is self-consistent:")
print(f"    unbordered            {unbordered}")
print(f"    b = 1                 {b1}   <- majority of the {bordered} bordered, as stated")
print(f"    b = 3, 5, 7           {b357}   (one each)")
print(f"    total                {unbordered + b1 + b357}")
print()
print("  CONSEQUENCE 1 -- b odd means 'b > 2' is 'b >= 3'. There is no b = 2,")
print("  4, 6 case, so the region is b in {3, 5, 7, 9, ...}.")
print()
print("  CONSEQUENCE 2, and it reverses the queue entry's framing:")
print("  THE REGION IS NOT UNSWEPT. Alpoge has one example at each of b = 3,")
print("  5 and 7 -- the method the whole worklist is modelled on has already")
print("  produced objects there. That is worse news than 'virgin territory'")
print("  and much better news than it sounds, because it supplies what the")
print("  Costas cell fatally lacked: GENUINE POSITIVE CONTROLS INSIDE THE")
print("  REGION, solved instances found by the method in question.")

# ---------------------------------------------------------------- 8. free bits, cleanest form
print()
print("=" * 74)
print("8. free_bits in its cleanest form, and what it predicts for a border")
print("=" * 74)
for v in sorted(TABLE):
    ds, d, r, D, fb, lg, den = TABLE[v]
    assert fb == 4 * (v - 1) // d, (v, fb, 4*(v-1)//d)
print("  ASSERTED on all six rows:   free_bits = 4(v-1)/d")
print("  i.e. four bits per orbit, and the orbit count is (v-1)/d.")
print()
print("  HYPOTHESIS, and it is the OPPOSITE of the one section 5 offered:")
print("  a border of width b removes rows and columns from the core, so the")
print("  core is smaller and carries FEWER free parameters. If free_bits")
print("  scales with the core rather than with v, then LARGER b IS CHEAPER,")
print("  not dearer. That is a mechanism for why anyone would flag b > 2 as")
print("  an opportunity, and it is the reverse of what I guessed last time.")
print()
print("  FALSIFIER, one number: the free-bit or density figure of Alpoge's")
print("  b = 3, 5 and 7 examples against his b = 1 examples at comparable")
print("  order. If free bits fall as b rises, the region is cheaper and the")
print("  queue entry is live. If they do not, it is not. I am NOT asserting")
print("  the scaling -- section 5 is what happens when I assert one.")

# ---------------------------------------------------------------- 9. where 126 could come from
print()
print("=" * 74)
print("9. Where '126+ admissible (v, b) pairs with b > 2' could come from")
print("=" * 74)
print("  Unconstrained count: 13 orders x (odd b from 3 up to B).")
print(f"  {'B':>4} {'odd b in [3,B]':>15} {'x 13 orders':>13}")
for B in range(3, 30, 2):
    k = len(range(3, B + 1, 2))
    tot = 13 * k
    flag = "   <-- first B reaching 126" if tot >= 126 and 13 * (k - 1) < 126 else ""
    print(f"  {B:>4} {k:>15} {tot:>13}{flag}")
print()
print("  So 126+ is consistent with b running to about 21 across 13 orders,")
print("  with a few pairs inadmissible. OFFERED AS A CONSISTENCY OBSERVATION,")
print("  NOT A DERIVATION: I do not know the admissibility condition for a")
print("  bordered core, so I cannot compute the real count. What this does")
print("  give the brief is a shape to check the source's number against, and")
print("  a specific question -- what is the upper bound on b, and what makes")
print("  a (v, b) pair admissible?")
print()
print("=" * 74)
print("ALL ASSERTIONS PASSED (part 3).")
print("=" * 74)


# ---------------------------------------------------------------- 10. which thirteen
print()
print("=" * 74)
print("10. THE TWO THIRTEENS, and the ambiguity is decision-critical")
print("=" * 74)
def prime_power_q(m):
    if m < 2: return False
    p = 2
    while p * p <= m:
        if m % p == 0: break
        p += 1
    else:
        return True
    x, k = m, 0
    while x % p == 0: x //= p; k += 1
    return x == 1

LIM = 3200
# Paley I: n = q+1, q prime power = 3 mod 4.  Paley II: n = 2(q+1), q = 1 mod 4.
known = {1, 2}
for q in range(3, LIM):
    if prime_power_q(q):
        if q % 4 == 3 and q + 1 <= LIM: known.add(q + 1)
        if q % 4 == 1 and 2 * (q + 1) <= LIM: known.add(2 * (q + 1))
n = 1
while n <= LIM: known.add(n); n *= 2          # Sylvester
# close under Kronecker product (H(m) x H(n) -> H(mn)) to a fixed point
changed = True
while changed:
    changed = False
    cur = sorted(known)
    for a in cur:
        for b_ in cur:
            if a > 1 and b_ > 1 and a * b_ <= LIM and a * b_ not in known:
                known.add(a * b_); changed = True

mult4 = [m for m in range(4, LIM + 1, 4)]
uncovered = [m for m in mult4 if m not in known]
print(f"  Coverage by Paley I/II + Sylvester + Kronecker closure only.")
print(f"  This is a SUBSET of the known constructions -- Williamson, Turyn,")
print(f"  Goethals-Seidel, Baumert-Hall and the sporadics are NOT modelled --")
print(f"  so 'uncovered' here is a SUPERSET of the genuinely open orders.")
print()
CLASSICAL13 = [668, 716, 892, 1004, 1132, 1244, 1388, 1436, 1676, 1772, 1916, 1948, 1964]
miss = [m for m in CLASSICAL13 if m in known]
print(f"  NECESSARY CONDITION CHECK: all 13 classical sub-2000 orders must be")
print(f"  uncovered by these constructions. Covered (should be none): {miss}")
assert not miss
print("  PASSED.")
print()
for lo, hi in ((4, 2000), (2000, 3000)):
    u = [m for m in uncovered if lo <= m < hi] if lo > 4 else [m for m in uncovered if m < hi]
    print(f"  uncovered multiples of 4 in [{lo}, {hi}): {len(u)}")
print()
print("  So I CANNOT derive either thirteen: my superset is far larger than 13")
print("  in both bands, because the constructions I cannot model are exactly the")
print("  ones that close most orders. Stated rather than papered over.")

print()
print("  WHAT IS DERIVABLE, and it discriminates the two readings:")
print()
print("  Reading A -- the 13 OPEN orders in (2000, 3000).")
print("    The worklist's own targets are 4v for v = 523, 571, 643, 659, 739:")
for v in (523, 571, 643, 659, 739):
    print(f"      v={v:>4} -> order {4*v:>5}  in (2000,3000): {2000 < 4*v < 3000}")
print(f"      v= 487 -> order {4*487:>5}  in (2000,3000): {2000 < 4*487 < 3000}"
      "   <-- below 2000, and recorded SOLVED by Alpoge")
print("    FIVE of the six live targets lie in (2000,3000) and the sixth is the")
print("    sub-2000 order Alpoge closed. Reading A fits the worklist exactly.")
print()
print("  Reading B -- Alpoge's 12 new examples plus 1 H matrix from elsewhere.")
print(f"    12 + 1 = 13, and the classical sub-2000 open list has "
      f"{len(CLASSICAL13)} entries.")
print("    Arithmetically consistent, and it would mean the 13 are all CLOSED.")
print()
print("  THE DISCRIMINATOR IS NOT ARITHMETIC, IT IS WHAT THE COUNT IS FOR:")
print("    under A, '126+ admissible (v,b) pairs with b > 2' counts parameter")
print("    choices available at THIRTEEN STILL-OPEN ORDERS -- an opportunity.")
print("    under B, it counts parameter choices at THIRTEEN SOLVED ORDERS --")
print("    the unexplored residue of finished problems, worth nothing as a")
print("    target. A file named OPEN_ORDERS.md could hold either: the open")
print("    orders, or the history of how the formerly-open ones were closed.")
print()
print("  ** SO THE SAME SENTENCE IS EITHER THE WHOLE OPPORTUNITY OR NO")
print("     OPPORTUNITY AT ALL, AND NOTHING I HOLD DECIDES WHICH. **")
print("  This outranks the cost comparison: if B holds, clause (c) is moot.")
print()
print("=" * 74)
print("ALL ASSERTIONS PASSED (part 4).")
print("=" * 74)


# ---------------------------------------------------------------- 11. 1004 and 2004
print()
print("=" * 74)
print("11. 2004 is NOT open, and 1004's status sharpens rather than resolves")
print("=" * 74)
def isprime_simple(m):
    if m < 2: return False
    if m % 2 == 0: return m == 2
    i = 3
    while i * i <= m:
        if m % i == 0: return False
        i += 2
    return True

print("  The claim circulating on the web -- '2004 is the first open order above")
print("  2000' -- is FALSE, and one line settles it:")
print(f"    2003 is prime: {isprime_simple(2003)}   2003 mod 4 = {2003 % 4}")
assert isprime_simple(2003) and 2003 % 4 == 3
print("  Paley I builds H(q+1) for q = 3 (mod 4) a prime power, so H(2004)")
print("  follows immediately. ASSERTED. The smallest open order above 2000 is")
print("  2060, per FINDING_05's thirteen.")
print()
print("  1004: hoa64's own closed-form families (replicated in")
print("  ../../playability/hoa64/coverage.py) return NOT REACHABLE for 1004,")
print("  and hoa64 ships no matrix for it. That is exactly how 1212 and 1940")
print("  behave -- and hoa64's README names 1212 and 1940 as its remaining")
print("  sub-2000 gaps while OMITTING 1004.")
print()
print("  So 1004 is a THIRD unshipped, closed-form-unreachable order below 2000")
print("  that the README does not list. My recall of 1004 as a classical open")
print("  order is therefore NOT refuted; it is mildly supported, because 1004")
print("  behaves identically to the two orders the README calls gaps.")
print("  STILL UNRESOLVED: whether 1004 is open, closed by a construction")
print("  hoa64 does not implement, or missing from the README by oversight.")
print()
print("  A NOTE ON MY OWN TEST: I first asserted that Alpoge's twelve must come")
print("  back UNREACHABLE from coverage.py. They come back REACHABLE, because")
print("  the function treats the shipped CSVs as a source. The code is right and")
print("  my expectation was wrong -- reachable-by-library is not")
print("  reachable-by-construction, and conflating them is how 1004 would get")
print("  silently reclassified.")

# ---------------------------------------------------------------- 12. not known vs cannot exist
print()
print("=" * 74)
print("12. 'Cannot be KNOWN' is not 'cannot EXIST' -- operator correction")
print("=" * 74)
print("  HADAMARD_CROSS.md sec 8 argues: a Williamson quadruple of order m hands")
print("  you H(4m), so H(716) and H(892) being open until 2026 proves W(179) and")
print("  W(223) were NOT KNOWN. That inference is valid.")
print()
print("  It does NOT follow that they do not EXIST, and sec 8's 'dead on arrival'")
print("  overstates it. OPERATOR-SUPPLIED: W(65) is still an open question, so")
print("  the DECIDED Williamson frontier sits below 65 and higher orders are")
print("  undecided rather than refuted.")
print()
print("  What the routes actually need, and the distance is the cost statement")
print("  clause (b) should test:")
for m, orders in ((103, "2060 and 2884"), (179, "2148 (v=537)"), (223, "2676 (v=669)")):
    print(f"    W({m:>3}) would close {orders:<16} -- {m - 65:>3} orders beyond 65")
print()
print("  So the route is not dead; it is a WILLIAMSON SEARCH at an order 38 to")
print("  158 beyond the decided frontier. That is a cost, not an impossibility,")
print("  and it is a different claim from the one sec 8 makes.")
print()
print("=" * 74)
print("ALL ASSERTIONS PASSED (part 5).")
print("=" * 74)


# ---------------------------------------------------------------- 14. b>=3 admissibility, DERIVED
print()
print("=" * 74)
print("14. The admissibility condition, derived from the worker's description")
print("=" * 74)
print("  The Hadamard worker (30 Sep 2026) describes the b >= 3 construction as a")
print("  four-block Goethals-Seidel-type array on an abelian group G of order")
print("  v - b, with target PAF sum -4b on a subgroup H of INDEX b+1 minus the")
print("  identity and +4 off H. A subgroup of index b+1 exists in an abelian")
print("  group of order v-b only if (b+1) | (v-b), and since")
print("      v - b = (v+1) - (b+1),   (b+1) | (v-b)  <=>  (b+1) | (v+1).")
print()
KNOWN = [(347,5,"order 1388"), (359,7,"order 1436"), (479,3,"order 1916"),
         (523,1,"order 2092, live; b=1 inferred from free_bits = 4(v-1)/d")]
for v,b,note in KNOWN:
    assert (v+1) % (b+1) == 0, (v,b)
    print(f"    v={v:>4} b={b:>2}: |G|={v-b:>4}, index={b+1}, |H|={(v-b)//(b+1):>4}   OK   {note}")
print("  ASSERTED on all four (v, b) pairs now known. Four for four.")
print()
F05_V = [515,523,537,571,573,599,643,647,659,669,719,721,739]
print("  Admissible (v, b), b odd, 3 <= b < v, over FINDING_05's thirteen:")
tot = 0
per = {}
for v in F05_V:
    bs = [d-1 for d in range(4, v+1, 2) if (v+1) % d == 0 and d-1 < v]
    per[v] = bs; tot += len(bs)
    print(f"    v={v:>4} (order {4*v:>5})  v+1={v+1:>4}  {len(bs):>2}: {bs}")
print()
print(f"  DERIVED TOTAL: {tot}.  The relayed figure is '126+'.")
print(f"  MISMATCH of {126-tot} ({100*(126-tot)/126:.0f}% low). Adding b=1, which is")
print(f"  admissible at every odd v since 2 | (v+1), gives {tot+13} -- still short.")
print("  So either the condition is stricter than the source's, or the 126+ counts")
print("  something else (a different thirteen, or an extra family, or it is typed).")
print("  THIS IS THE SHARPEST FORM OF CLAUSE (a): a condition confirmed on the")
print("  source's OWN four examples yields 96, not 126+. One of them is wrong.")
print()
print("  Per-order bordered freedom, which is decision-relevant on its own:")
print(f"    ZERO admissible b >= 3:  v=537 (order 2148) -- no bordered route at all")
print(f"    exactly ONE:             v=721 (order 2884), b=37")
print(f"    the LIVE target v=523:   only b in {per[523]} -- nearly at the b=1 boundary,")
print("                             consistent with the live search being b=1")
print(f"    richest:                 v=719 ({len(per[719])}), v=599 ({len(per[599])}), "
      f"v=659 ({len(per[659])}), v=647 ({len(per[647])})")
print("  That ranking is NOT the b=1 free-bit ranking, which puts 523 first. If the")
print("  border axis matters, it points at different orders than the live worklist.")
print()
print("  WHAT I CANNOT COMPUTE, and an error of mine that proves the point.")
print("  I first tabulated orbit counts at b >= 3 using the largest odd divisor of")
print("  v-b. It returned 2 orbits at v=523 where PLAN_2092's VERIFIED sweep gives")
print("  58, and the contradiction caught it: the largest odd divisor is not the")
print("  admissible d -- d must satisfy the ROW-SUM LAW, and the law I verified is")
print("  the b=1 one (sum a_k^2 = 4v with a_k = +-1 + d(2u-(r-1))). At b >= 3 the")
print("  target is the relaxed PAF condition above, so that law does not apply and")
print("  I HAVE NO ADMISSIBILITY TEST FOR d AT b >= 3. Therefore no free-bit or")
print("  density figure at b >= 3 can be computed here. That is clause (c), and it")
print("  stays with whoever can read the source. Applying a b=1-fitted relation at")
print("  b >= 3 is exactly the D53 trap, and I nearly shipped a table of it.")
print()
print("=" * 74)
print("ALL ASSERTIONS PASSED (part 6).")
print("=" * 74)
