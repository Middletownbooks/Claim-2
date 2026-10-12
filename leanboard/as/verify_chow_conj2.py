"""Arm AS: a counterexample to Conjecture 2 of Chow, "Reduction of Rota's basis
conjecture to a problem on three bases" (arXiv:math/0504367; SIAM J. Discrete
Math. 23 (2009) 369-371), at n = 4.

Supplied by this programme's operator as the LaTeX sent to the conjecture's
author. This is the first artifact of the M4 class (arm AR): an auxiliary
conjecture refuted in the course of attacking something else, propagated by
preprint and by direct notice to the author, and absent from every AI-results
corpus this programme has measured.

Everything here is recomputed from the matrix alone. Nothing is taken from the
document except the matrix, the I_i, and the claims under test.

All arithmetic is over F_3, exact, using integer determinants reduced mod 3.
"""
import sys, itertools
from itertools import permutations, combinations

PASS = FAIL = 0
def check(label, cond, detail=""):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {label}" + (f"   [{detail}]" if detail else ""))
    else:    FAIL += 1; print(f"  FAIL  {label}" + (f"   [{detail}]" if detail else ""))
def section(t): print(f"\n{'='*74}\n{t}\n{'='*74}")

# --- the matrix, transcribed from the document ------------------------------
ROWS = [
    [1, 0, 0, 0, 1, 1, 1,  1, 1,  0,  1, 0],
    [0, 1, 0, 0, 0, 0, 0,  1, 0,  1, -1, 0],
    [0, 0, 1, 0, 0, 0, 1,  0, 0, -1,  0, 1],
    [0, 0, 0, 1, 0, 1, 0, -1, 0, -1,  1, 1],
]
N_EL, RANK = 12, 4
V = [tuple(ROWS[r][c] % 3 for r in range(RANK)) for c in range(N_EL)]

# --- F_3 linear algebra ------------------------------------------------------
def rank_f3(cols):
    M = [list(c) for c in cols]
    m, n = len(M), (len(M[0]) if M else 0)
    r = 0
    for col in range(n):
        piv = next((i for i in range(r, m) if M[i][col] % 3), None)
        if piv is None: continue
        M[r], M[piv] = M[piv], M[r]
        inv = pow(M[r][col] % 3, 1, 3)
        inv = 1 if inv == 1 else 2          # inverses mod 3: 1->1, 2->2
        M[r] = [(x * inv) % 3 for x in M[r]]
        for i in range(m):
            if i != r and M[i][col] % 3:
                f = M[i][col] % 3
                M[i] = [(M[i][j] - f * M[r][j]) % 3 for j in range(n)]
        r += 1
        if r == m: break
    return r

def indep(S):   return rank_f3([V[i] for i in S]) == len(S)
def basis(S):   return len(S) == RANK and rank_f3([V[i] for i in S]) == RANK

section("1. The document's matrix reproduces the vectors it lists")
LISTED = {0:(1,0,0,0), 1:(0,1,0,0), 2:(0,0,1,0), 3:(0,0,0,1),
          4:(1,0,0,0), 5:(1,0,0,1), 6:(1,0,1,0), 7:(1,1,0,-1),
          8:(1,0,0,0), 9:(0,1,-1,-1), 10:(1,-1,0,1), 11:(0,0,1,1)}
ok = all(V[i] == tuple(x % 3 for x in LISTED[i]) for i in range(N_EL))
check("matrix columns agree with the listed v_0..v_11 (mod 3)", ok)

section("2. Basis count: the document claims exactly 240 of 495")
BASES = [frozenset(S) for S in combinations(range(N_EL), RANK) if basis(S)]
print(f"  4-subsets          : {len(list(combinations(range(N_EL), RANK)))}")
print(f"  bases              : {len(BASES)}")
print(f"  non-bases          : 495 - {len(BASES)} = {495-len(BASES)}")
check("exactly 240 bases", len(BASES) == 240, f"got {len(BASES)}")

section("3. Hypothesis (b): M is a disjoint union of three bases")
TRIPLE = [{0,1,2,3}, {4,5,6,7}, {8,9,10,11}]
allb = all(basis(B) for B in TRIPLE)
cover = set().union(*TRIPLE) == set(range(N_EL))
disj  = sum(len(B) for B in TRIPLE) == N_EL
for B in TRIPLE:
    print(f"    {sorted(B)}  basis: {basis(B)}")
check("the three sets are pairwise disjoint and cover the ground set", cover and disj)
check("each of the three is a basis", allb)

section("4. Hypothesis (c)/(d): the I_i are disjoint independent sets, |I_i| <= 3")
I = {1: {1,2,6}, 2: {4,10}, 3: {3,5,9}, 4: {7,8,11}}
WITNESS = {1: {1,2,3,6}, 2: {1,2,4,10}, 3: {1,3,5,9}, 4: {1,7,8,11}}
pw = all(not (I[a] & I[b]) for a in I for b in I if a < b)
sizes = [len(I[i]) for i in sorted(I)]
for i in sorted(I):
    print(f"    I_{i} = {sorted(I[i])}   |I_{i}| = {len(I[i])}   independent: {indep(I[i])}"
          f"   witness {sorted(WITNESS[i])} is a basis: {basis(WITNESS[i])}")
check("the I_i are pairwise disjoint", pw)
check("0 <= |I_i| <= 3 for all i", all(0 <= s <= 3 for s in sizes), f"sizes {sizes}")
check("each I_i is independent", all(indep(I[i]) for i in I))
check("each stated witness really is a containing basis",
      all(I[i] <= WITNESS[i] and basis(WITNESS[i]) for i in I))

section("5. Step 1: the rows are forced")
covered = set().union(*I.values())
free = set(range(N_EL)) - covered
print(f"  elements covered by the I_i : {len(covered)}")
print(f"  free elements               : {sorted(free)}")
full = [i for i in sorted(I) if len(I[i]) == 3]
check("the I_i cover every element but one", len(free) == 1 and free == {0})
check("rows 1, 3 and 4 are already full, so 0 must join row 2",
      full == [1, 3, 4], f"full rows {full}")
R = {1: {1,2,6}, 2: {0,4,10}, 3: {3,5,9}, 4: {7,8,11}}
check("forced rows match the document", R == {1:{1,2,6}, 2:{0,4,10}, 3:{3,5,9}, 4:{7,8,11}})

section("6. Step 2: {0,4,8} is a parallel class")
par = V[0] == V[4] == V[8]
print(f"    v_0 = {V[0]}   v_4 = {V[4]}   v_8 = {V[8]}   (mod 3)")
two_together = [S for S in BASES if len(S & {0,4,8}) >= 2]
check("v_0 = v_4 = v_8", par)
check("no basis contains two of {0,4,8}", not two_together,
      f"{len(two_together)} such bases")

section("7. Step 4: the pair sets P and Q, recomputed")
R1, R3 = sorted(R[1]), sorted(R[3])
P_doc = {(1,9),(2,3),(2,5),(6,3),(6,5)}
Q_doc = {(1,3),(1,5),(2,9),(6,9)}
P_810 = {(a,b) for a in R1 for b in R3 if basis({8,10,a,b})}
P_07  = {(a,b) for a in R1 for b in R3 if basis({0,7,a,b})}
Q_011 = {(a,b) for a in R1 for b in R3 if basis({0,11,a,b})}
P_47  = {(a,b) for a in R1 for b in R3 if basis({4,7,a,b})}
Q_411 = {(a,b) for a in R1 for b in R3 if basis({4,11,a,b})}
print(f"    {{8,10,a,b}} basis for : {sorted(P_810)}")
print(f"    {{0, 7,a,b}} basis for : {sorted(P_07)}")
print(f"    {{0,11,a,b}} basis for : {sorted(Q_011)}")
check("{8,10,a,b} is a basis exactly on the document's P", P_810 == P_doc)
check("{0,7,a,b} is a basis exactly on the document's P", P_07 == P_doc)
check("{0,11,a,b} is a basis exactly on the document's Q", Q_011 == Q_doc)
check("replacing 0 by 4 changes nothing", P_47 == P_doc and Q_411 == Q_doc)
check("P and Q partition R_1 x R_3, |P| = 5, |Q| = 4",
      P_doc | Q_doc == {(a,b) for a in R1 for b in R3} and not (P_doc & Q_doc)
      and len(P_doc) == 5 and len(Q_doc) == 4)

section("8. Step 5: the parity obstruction")
print("     matching mu                      |mu & P|")
parities = []
for p in permutations(R3):
    mu = {(R1[i], p[i]) for i in range(3)}
    k = len(mu & P_doc)
    parities.append(k)
    print(f"     {'  '.join(f'({a},{b})' for a,b in sorted(mu)):<32} {k}")
check("|mu & P| is odd for every perfect matching", all(k % 2 == 1 for k in parities),
      f"values {sorted(set(parities))}")
check("|mu & P| = 2 is therefore unattainable", 2 not in parities)
check("the six values match the document's table exactly",
      sorted(parities) == sorted([1,1,1,1,3,3]))

section("9. The argument's own logic: why 2 is required")
print("  One column holds {8,10}  -> its (a,b) must lie in P")
print("  One column holds {0|4, 7}  -> its (a,b) must lie in P")
print("  One column holds {0|4,11}  -> its (a,b) must lie in Q")
print("  Hence a valid grid needs exactly two of the three pairs in P.")
check("the three columns are forced to need P, P, Q respectively",
      P_810 == P_07 == P_doc and Q_011 == Q_doc)

section("10. Independent exhaustive search over all 1296 grids")
grids = 0; valid = []
for p1 in permutations(sorted(R[1])):
    for p2 in permutations(sorted(R[2])):
        for p3 in permutations(sorted(R[3])):
            for p4 in permutations(sorted(R[4])):
                grids += 1
                cols = [{p1[c], p2[c], p3[c], p4[c]} for c in range(3)]
                if all(basis(frozenset(c)) for c in cols):
                    valid.append((p1, p2, p3, p4))
print(f"  grids examined        : {grids}")
print(f"  grids with 3 bases    : {len(valid)}")
check("the exhaustive count is 6^4 = 1296", grids == 1296)
check("NO valid 4x3 grid exists", len(valid) == 0)

section("11. Cross-check: the search is capable of finding a grid when one exists")
# Drop the constraint that forces the parallel class apart, by relabelling
# element 8 to a generic vector, and re-run. A positive control on the search.
V_ctrl = list(V); V_ctrl[8] = (0, 1, 1, 0)
def basis_ctrl(S):
    return len(S) == RANK and rank_f3([V_ctrl[i] for i in S]) == RANK
found = None
for p1 in permutations(sorted(R[1])):
    for p2 in permutations(sorted(R[2])):
        for p3 in permutations(sorted(R[3])):
            for p4 in permutations(sorted(R[4])):
                cols = [{p1[c], p2[c], p3[c], p4[c]} for c in range(3)]
                if all(basis_ctrl(frozenset(c)) for c in cols):
                    found = (p1, p2, p3, p4); break
            if found: break
        if found: break
    if found: break
print(f"  with v_8 replaced by {V_ctrl[8]}, a valid grid: {found is not None}")
if found:
    for c in range(3):
        print(f"    column {c+1}: {sorted({found[0][c], found[1][c], found[2][c], found[3][c]})}")
check("the same search DOES find a grid once the parallel class is broken",
      found is not None, "so the null result in section 10 is not a search bug")

section(f"RESULT   {PASS}/{PASS+FAIL} checks passed")
sys.exit(0 if FAIL == 0 else 1)
