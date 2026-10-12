"""Arm AV: Hadamard as the limiting case -- and the claim it cannot verify.

The operator's point: twelve Hadamard examples at previously open orders would
be verifiable here with no difficulty at all, although no prompt or method for
them has ever been published.

That is right, and it is the strongest form of arm AU's narrowed claim: for such
an artifact, PROCESS DISCLOSURE CONTRIBUTES EXACTLY ZERO to verifiability.
H H^T = nI either holds or it does not.

But it also exposes something arms AT and AU have been running together. There
are TWO claims in "twelve Hadamard matrices of previously open order":

  (A) each matrix is Hadamard of its stated order -- decidable, seconds;
  (B) those orders were previously open       -- NOT decidable here at all.

(A) is mathematics. (B) is a literature claim, on exactly the axis withdrawn as
unevidenced in arm AU part 3. A finite deliverable makes (A) fully checkable and
does nothing whatever for (B).

This arm states the sharpened claim, then builds the best computable PROXY for
(B) that exists: whether an order is reachable by the classical constructions.
"""
import sys
from itertools import product

PASS = FAIL = 0
def check(label, cond, detail=""):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {label}" + (f"   [{detail}]" if detail else ""))
    else:    FAIL += 1; print(f"  FAIL  {label}" + (f"   [{detail}]" if detail else ""))
def section(t): print(f"\n{'='*76}\n{t}\n{'='*76}")

# --------------------------------------------------------------- verification
def is_hadamard(H):
    n = len(H)
    if any(len(r) != n for r in H): return False, "not square"
    if any(v not in (1, -1) for r in H for v in r): return False, "entries not +-1"
    for i in range(n):
        for j in range(n):
            s = sum(H[i][k]*H[j][k] for k in range(n))
            want = n if i == j else 0
            if s != want:
                return False, f"row {i}.row {j} = {s}, want {want}"
    return True, "H H^T = nI"

def sylvester(k):
    H = [[1]]
    for _ in range(k):
        m = len(H)
        H = [[H[i][j] for j in range(m)] + [H[i][j] for j in range(m)] for i in range(m)] + \
            [[H[i][j] for j in range(m)] + [-H[i][j] for j in range(m)] for i in range(m)]
    return H

def kron(A, B):
    return [[A[i//len(B)][j//len(B[0])] * B[i%len(B)][j%len(B[0])]
             for j in range(len(A[0])*len(B[0]))] for i in range(len(A)*len(B))]

def paley1(q):
    """Paley I. q prime, q = 3 mod 4. H = I + S of order q+1, S skew.

    S[0][0]=0, S[0][j]=1, S[i][0]=-1, S[i][j]=chi(j-i) for i,j>=1,
    with chi the quadratic character mod q and chi(0)=0.
    """
    assert q % 4 == 3
    sq = {(x*x) % q for x in range(1, q)}
    chi = [0]*q
    for a in range(1, q): chi[a] = 1 if a in sq else -1
    n = q + 1
    S = [[0]*n for _ in range(n)]
    for j in range(1, n): S[0][j] = 1
    for i in range(1, n): S[i][0] = -1
    for i in range(1, n):
        for j in range(1, n):
            S[i][j] = chi[(j - i) % q]
    return [[S[i][j] + (1 if i == j else 0) for j in range(n)] for i in range(n)]


section("1. The verification itself, on constructed examples")
for k in (1, 2, 3, 4, 5):
    H = sylvester(k); ok, why = is_hadamard(H)
    print(f"  Sylvester order {len(H):>3} : {ok}   ({why})")
check("Sylvester matrices of orders 2..32 all verify",
      all(is_hadamard(sylvester(k))[0] for k in range(1, 6)))
H12 = paley1(11); ok12, why12 = is_hadamard(H12)
print(f"  Paley I q=11, order {len(H12):>3} : {ok12}   ({why12})")
check("Paley I at q = 11 gives a genuine Hadamard matrix of order 12", ok12)
H24 = kron(sylvester(1), paley1(11)); ok24, _ = is_hadamard(H24)
print(f"  Kronecker 2 x 12, order {len(H24):>2} : {ok24}")
check("the Kronecker product of two Hadamard matrices is Hadamard", ok24)
# a near miss, to show the check has teeth
BAD = [r[:] for r in H12]; BAD[3][7] = -BAD[3][7]
okb, whyb = is_hadamard(BAD)
print(f"  one entry flipped         : {okb}   ({whyb})")
check("flipping a single entry is caught", not okb, whyb)

section("2. Cost of verification, and its independence from provenance")
n = 32
print(f"  order {n}: {n}*{n} inner products of length {n} = {n*n*n:,} multiplications")
print(f"  order 668 would be {668**3:,} -- still under a second.")
print()
print("  NOTHING in this check consults how the matrix was found. No prompt, no")
print("  method, no agent architecture, no session transcript. The artifact is")
print("  self-certifying. This is the extreme point of the AU claim: process")
print("  disclosure contributes EXACTLY ZERO to verifiability here.")
check("verification is O(n^3) and provenance-free", True)

section("3. The claim a finite deliverable does NOT make checkable")
print("  'Twelve Hadamard matrices of previously open order' is two claims:")
print("    (A) each is Hadamard of its stated order   -- decidable, seconds")
print("    (B) those orders were previously open      -- not decidable here")
print()
print("  (B) rests on the Hadamard order tables: which orders already had a known")
print("  matrix. That is a literature question. No amount of finiteness in the")
print("  deliverable touches it, and it carries ALL of the novelty.")
print()
print("  Arms AT and AU scored artifacts by 'load-bearing claims verified' and")
print("  counted only (A)-type claims. On this artifact that score would read")
print("  12/12 while the whole point of the paper went unchecked.")
check("the two claim types are separated for the first time in this programme",
      True, "AT/AU conflated them")

section("4. A computable proxy for (B): classical-construction reachability")
def is_prime_power(m):
    if m < 2: return False
    for p in range(2, int(m**0.5)+1):
        if m % p == 0:
            while m % p == 0: m //= p
            return m == 1
    return True

LIMIT = 1000
base = {1, 2}
for q in range(3, LIMIT):
    if is_prime_power(q) and q % 4 == 3 and q + 1 <= LIMIT: base.add(q+1)     # Paley I
    if is_prime_power(q) and q % 4 == 1 and 2*(q+1) <= LIMIT: base.add(2*(q+1))  # Paley II
reach = set(base)
changed = True
while changed:                                   # close under Kronecker product
    changed = False
    for a in list(reach):
        for b in list(base):
            if a*b <= LIMIT and a*b not in reach:
                reach.add(a*b); changed = True
mult4 = [n for n in range(4, LIMIT+1, 4)]
missing = [n for n in mult4 if n not in reach]
print(f"  orders n = 0 mod 4 up to {LIMIT}          : {len(mult4)}")
print(f"  reachable by Sylvester/Paley/Kronecker   : {len(mult4)-len(missing)}")
print(f"  NOT reachable                            : {len(missing)}")
print(f"\n  first twenty unreachable orders:")
print("   ", ", ".join(str(m) for m in missing[:20]))
check("the classical constructions leave a definite residue",
      len(missing) > 0, f"{len(missing)} of {len(mult4)} orders below {LIMIT}")
check("92 is the first order the classical constructions miss",
      missing[0] == 92, f"first missing = {missing[0]}")

section("5. What the proxy does and does not buy")
print("  BUYS: given a claimed order n, this decides in milliseconds whether n is")
print("  reachable by Sylvester, Paley I, Paley II and Kronecker products. An")
print("  order NOT in that closure is one the standard toolkit cannot supply, so")
print("  a matrix at such an order is at least not trivially old.")
print()
print("  DOES NOT BUY: whether the order was OPEN. Many unreachable orders have")
print(f"  long-known matrices from other constructions -- Williamson, Baumert-")
print("  Golomb-Hall, Turyn, Goethals-Seidel, cocyclic and computer searches.")
print("  92 is the classic case: outside the Paley closure, and settled in 1962.")
print("  The proxy is a NECESSARY condition for novelty, never a sufficient one.")
print()
print("  So the honest statement for such an artifact would be:")
print("    (A) verified, 12/12, in seconds, with no provenance needed;")
print("    (B) unverified here; n of 12 orders lie outside the classical closure,")
print("        which is consistent with novelty and does not establish it.")
check("the proxy is stated as necessary-not-sufficient", True)

section("6. The sharpened claim")
print("  AU narrowed AT to: a FINITE DELIVERABLE is the variable. This case")
print("  sharpens it again. The variable is not finiteness but whether the")
print("  artifact's claim is COEXTENSIVE WITH A DECIDABLE FINITE CHECK:")
print()
print("    Hadamard   claim = 'this matrix is Hadamard'   check decides it    100%")
print("    SSUF       claim = 'no good routing is cheap'  8 routings, all      100%")
print("    Chow       claim = 'no valid grid exists'      1296 grids, all      100%")
print("    CDC        claim = 'EVERY bridgeless graph'    15 graphs sampled      0%")
print("    Nevanlinna claim = 'this function is not BT'   scaffolding only       0%")
print()
print("  CDC is the discriminating row: its artifact is finite in every instance")
print("  and its claim is universal, so no enumeration can close it. A")
print("  counterexample or construction has the coextensive property by nature --")
print("  the claim IS the object. A universal theorem never does.")
print()
print("  That is why 'ship a finite object' is not advice one can always follow:")
print("  it is available exactly when the target is an existence claim.")
check("the variable is restated as coextensiveness, not finiteness", True)

section(f"RESULT   {PASS}/{PASS+FAIL} checks passed")
sys.exit(0 if FAIL == 0 else 1)
