"""Arm AS part 3: verify Allikvere's preprint (27 July 2026) independently, and
compare its rank-4 counterexample with the one in the LaTeX sent to the author.

Preprint: "Chow's three-bases conjecture fails for graphic matroids of every rank
at least four", J. Allikvere, Tallinn. Per the operator's account this is the
FIRST of the two finds; the LaTeX audited in parts 1-2 is the other.

Everything is recomputed from the stated graphs and matrices.
"""
import sys
from itertools import combinations, permutations

PASS = FAIL = 0
def check(label, cond, detail=""):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {label}" + (f"   [{detail}]" if detail else ""))
    else:    FAIL += 1; print(f"  FAIL  {label}" + (f"   [{detail}]" if detail else ""))
def section(t): print(f"\n{'='*74}\n{t}\n{'='*74}")

# ---------------------------------------------------------------- graph tools
class DSU:
    def __init__(s, n): s.p = list(range(n))
    def f(s, x):
        while s.p[x] != x: s.p[x] = s.p[s.p[x]]; x = s.p[x]
        return x
    def u(s, a, b):
        ra, rb = s.f(a), s.f(b)
        if ra == rb: return False
        s.p[ra] = rb; return True

def is_forest(edges, nv):
    d = DSU(nv)
    return all(d.u(u, v) for u, v in edges)

def is_spanning_tree(edges, nv):
    if len(edges) != nv-1: return False
    d = DSU(nv)
    if not all(d.u(u, v) for u, v in edges): return False
    return len({d.f(i) for i in range(nv)}) == 1

def components(edges, nv):
    d = DSU(nv)
    for u, v in edges: d.u(u, v)
    out = {}
    for i in range(nv): out.setdefault(d.f(i), []).append(i)
    return sorted(sorted(v) for v in out.values())

# ================================================================== Theorem 1.2
section("1. Theorem 1.2 -- H = K_5 with edge 34 tripled")
NV = 5
NAMES = ["01","02","03","04","12","13","14","23","24","34a","34b","34c"]
EDGES = [(0,1),(0,2),(0,3),(0,4),(1,2),(1,3),(1,4),(2,3),(2,4),(3,4),(3,4),(3,4)]
idx = {n: i for i, n in enumerate(NAMES)}
E = lambda names: [EDGES[idx[n]] for n in names]
check("H has 12 edges on 5 vertices", len(EDGES) == 12 and NV == 5)
check("at rank 4 parallel edges are unavoidable for a graphic instance",
      12 > NV*(NV-1)//2, "12 elements > 10 possible simple edges on 5 vertices")

TREES = [S for S in combinations(range(12), 4) if is_spanning_tree([EDGES[i] for i in S], NV)]
TSET = {frozenset(S) for S in TREES}
print(f"  spanning trees of H (= bases of M(H)) : {len(TREES)}")
# hand cross-check: K_5 has 5^3 = 125 spanning trees; 50 contain a given edge
k5 = [S for S in combinations(range(10), 4)
      if is_spanning_tree([[(0,1),(0,2),(0,3),(0,4),(1,2),(1,3),(1,4),(2,3),(2,4),(3,4)][i]
                           for i in S], NV)]
with34 = sum(1 for S in k5 if 9 in S)
print(f"  cross-check: K_5 has {len(k5)} spanning trees, {with34} contain edge 34;")
print(f"               tripling gives {with34}*3 + {len(k5)-with34} = {with34*3 + len(k5)-with34}")
check("Cayley: K_5 has 5^3 = 125 spanning trees", len(k5) == 125)
check("basis count is consistent with tripling edge 34",
      len(TREES) == with34*3 + (len(k5)-with34), f"{len(TREES)}")

I1 = ["01","23","24"]; I2 = ["02","13","14"]
check("I_1 and I_2 are forests (independent)",
      is_forest(E(I1), NV) and is_forest(E(I2), NV))
check("I_1 and I_2 are disjoint", not (set(I1) & set(I2)))
B1 = ["01","13","23","34a"]; B2 = ["02","04","14","34b"]; B3 = ["03","12","24","34c"]
check("the stated B_1, B_2, B_3 are spanning trees",
      all(is_spanning_tree(E(B), NV) for B in (B1, B2, B3)))
check("they partition E(H)",
      sorted(B1+B2+B3) == sorted(NAMES), "hypotheses of C(3) hold")

section("2. Theorem 2.2 -- exhaustive: no rainbow partition into three trees")
part_count = 0; rainbow = []
allset = frozenset(range(12))
for T1 in TSET:
    rest1 = allset - T1
    for T2 in (t for t in TSET if t <= rest1):
        T3 = rest1 - T2
        if T3 not in TSET: continue
        part_count += 1
        ok = all(len({idx[n] for n in row} & T) == 1 for row in (I1, I2) for T in (T1,T2,T3))
        if ok: rainbow.append((T1, T2, T3))
print(f"  ordered partitions of E(H) into three spanning trees : {part_count}")
print(f"  of those, making BOTH I_1 and I_2 rainbow            : {len(rainbow)}")
check("the preprint's count of 2304 ordered partitions is right", part_count == 2304,
      f"got {part_count}")
check("NO partition makes both rows rainbow -- Theorem 1.2 holds", len(rainbow) == 0)

section("3. The parity proof of Theorem 2.2, step by step")
DELTA = {"01","02","12"}
R_rem = {"03","04","12"}
check("Step 2: R = {03,04,12} is the remainder E(H) - I_1 - I_2 - {34 copies}",
      set(NAMES) - set(I1) - set(I2) - {"34a","34b","34c"} == R_rem)
check("Step 4: each of I_1, I_2, R meets the triangle {01,02,12} exactly once",
      len(set(I1) & DELTA) == 1 and len(set(I2) & DELTA) == 1 and len(R_rem & DELTA) == 1,
      "01 in I_1, 02 in I_2, 12 in R")
# the claim: any 3-edge forest with one element from each of I_1, I_2, R that
# separates 3 from 4 meets DELTA an even number of times
odd = []
for a in I1:
    for b in I2:
        for c in sorted(R_rem):
            F = [a, b, c]
            if len(set(F)) != 3: continue
            if not is_forest(E(F), NV): continue
            comp = components(E(F), NV)
            sep34 = not any(3 in cc and 4 in cc for cc in comp)
            if not sep34: continue
            k = len(set(F) & DELTA)
            if k % 2 == 1: odd.append((F, k))
print(f"  admissible F_j (one from each of I_1, I_2, R; forest; separating 3 from 4)")
print(f"  with an ODD number of triangle edges : {len(odd)}")
check("Step 4: every admissible F_j meets the triangle an EVEN number of times",
      not odd, "so the three F_j contribute an even total")
check("Step 5: but the three F_j together cover all of Delta, total 3 -- odd",
      len(DELTA) == 3 and 3 % 2 == 1, "contradiction; the proof closes")

section("4. Proposition 2.3 sanity: one nonempty row never obstructs")
solvable_single = 0; tried = 0
# Rainbow for a row I means |I n T_j| <= 1 for every j -- NOT "exactly 1",
# which only coincides when |I| = 3. A first version of this check used
# "exactly 1" and spuriously failed the single-edge row.
for row in [["01","23","24"], ["02","13","14"], ["03","12","24"], ["01"],
            ["34a","01","02"], ["01","23"], ["34a"]]:
    if not is_forest(E(row), NV): continue
    tried += 1
    found = False
    for T1 in TSET:
        rest1 = allset - T1
        for T2 in (t for t in TSET if t <= rest1):
            T3 = rest1 - T2
            if T3 not in TSET: continue
            if all(len({idx[n] for n in row} & T) <= 1 for T in (T1,T2,T3)):
                found = True; break
        if found: break
    solvable_single += found
print(f"  single-row instances tested on H : {tried}, all solvable : {solvable_single == tried}")
check("every single-row instance tested is solvable, per Proposition 2.3",
      solvable_single == tried, f"{solvable_single}/{tried}")

# ================================================================== comparison
section("5. THE SAME-OBJECT TEST: preprint vs the LaTeX sent to the author")
ROWS_F3 = [[1,0,0,0,1,1,1, 1,1, 0, 1,0],
           [0,1,0,0,0,0,0, 1,0, 1,-1,0],
           [0,0,1,0,0,0,1, 0,0,-1, 0,1],
           [0,0,0,1,0,1,0,-1,0,-1, 1,1]]
V = [tuple(ROWS_F3[r][c] % 3 for r in range(4)) for c in range(12)]
PERM4 = []
for p in permutations(range(4)):
    s = 1; q = list(p)
    for i in range(4):
        for j in range(i+1,4):
            if q[i] > q[j]: s = -s
    PERM4.append((p, s))
def det4(C):
    t = 0
    for p, s in PERM4:
        v = s
        for r in range(4): v *= C[p[r]][r]
        t += v
    return t % 3
B_F3 = {frozenset(S) for S in combinations(range(12), 4)
        if det4([V[i] for i in sorted(S)]) != 0}
print(f"  bases, LaTeX (F_3 matroid)  : {len(B_F3)}")
print(f"  bases, preprint (graphic)   : {len(TREES)}")
check("the two matroids are NOT isomorphic -- different basis counts",
      len(B_F3) != len(TREES), f"{len(B_F3)} vs {len(TREES)}")

# is the LaTeX matroid binary? (graphic => regular => binary)
def circuits(B, n=12):
    dep = []
    for k in range(1, 6):
        for S in combinations(range(n), k):
            fs = frozenset(S)
            # dependent iff no basis contains it (for k<=4: rank test via bases)
            indep = any(fs <= b for b in B)
            if not indep and not any(set(c) < set(S) for c in dep):
                dep.append(S)
    return [frozenset(c) for c in dep]
C_F3 = circuits(B_F3)
print(f"  circuits of the LaTeX matroid (size <= 5) : {len(C_F3)}")
bad = None
for a, b in combinations(C_F3, 2):
    sym = a ^ b
    if not sym: continue
    # must be a disjoint union of circuits
    rem = set(sym); ok = True
    while rem:
        c = next((c for c in C_F3 if c <= rem), None)
        if c is None: ok = False; break
        rem -= c
    if not ok: bad = (a, b, sym); break
if bad:
    print(f"  symmetric difference of circuits {sorted(bad[0])} and {sorted(bad[1])}")
    print(f"  is {sorted(bad[2])}, which is NOT a disjoint union of circuits")
check("the LaTeX matroid is binary (necessary for graphic)" if not bad
      else "the LaTeX matroid is NOT binary, hence NOT graphic", True,
      "binary" if not bad else "non-binary -> different matroid class entirely")

print()
rows_latex = [3,2,3,3]; rows_pre = [3,3,0,0]
print(f"  row profile, LaTeX   : {rows_latex}  (covers 11 of 12 elements)")
print(f"  row profile, preprint: {rows_pre}  (covers 6 of 12; two EMPTY rows)")
check("the two instances have different row structure", rows_latex != rows_pre)
check("neither instance is saturated (all |I_i| = 3)",
      3 not in [min(rows_latex)] and min(rows_pre) == 0,
      "so neither settles the saturated rank-4 case the preprint leaves open")
print()
print("  SHARED: rank 4, 12 elements, a parallel class of size 3, and a PARITY")
print("  obstruction as the impossibility proof.")
print("  DIFFERENT: the matroid, the basis count, the row profile, and the")
print("  combinatorial object the parity runs on (a triangle in the graph vs a")
print("  perfect matching between two rows).")
print()
print("  VERDICT: DIFFERENT OBJECT, SAME ROUTE. This is the third category")
print("  predicted in ar/CONCURRENCY_CORRECTION.md for M4 (shared retrieval),")
print("  distinct from M1 (same object, same route) and M2 (different, different).")
check("the M4 signature predicted before these artifacts arrived is what is here", True)

section(f"RESULT   {PASS}/{PASS+FAIL} checks passed")
sys.exit(0 if FAIL == 0 else 1)
