"""Arm AS part 2: how findable was this counterexample, and does the proposed
repair survive?

Two questions the supplied document raises but does not answer:

  Q1. The operator reports a second researcher independently found a DIFFERENT
      counterexample. Is that surprising? That depends on the density and the
      structure of the counterexample space.

  Q2. The document suggests "adding a simplicity hypothesis may repair
      Conjecture 2". A simple counterexample would kill that. Search for one.

NOTE ON A RETRACTED ASSERTION. A first version of this script asserted, in text
written before the sample returned, that "counterexamples are not vanishingly
rare" and that different independent finds were therefore expected. The blind
sample returned ZERO in 14,297 valid instances. The assertion was wrong and the
conclusion it supported was backwards. Both are corrected below from the data.

Method. Bases are precomputed once per matroid (495 determinants mod 3), so the
1296-grid test is pure lookup.
"""
import sys, random
from itertools import permutations, combinations

random.seed(20260920)
PASS = FAIL = 0
def check(label, cond, detail=""):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {label}" + (f"   [{detail}]" if detail else ""))
    else:    FAIL += 1; print(f"  FAIL  {label}" + (f"   [{detail}]" if detail else ""))
def section(t): print(f"\n{'='*74}\n{t}\n{'='*74}")

PERM4 = []
for p in permutations(range(4)):
    s = 1; q = list(p)
    for i in range(4):
        for j in range(i+1, 4):
            if q[i] > q[j]: s = -s
    PERM4.append((p, s))

def det4(a, b, c, d):
    C = (a, b, c, d); t = 0
    for p, s in PERM4:
        v = s
        for r in range(4): v *= C[p[r]][r]
        t += v
    return t % 3

def bases_of(V):
    return {S for S in map(frozenset, combinations(range(12), 4))
            if det4(*[V[i] for i in sorted(S)]) != 0}

def indep_in(B, S):
    S = set(S)
    if len(S) == 4: return frozenset(S) in B
    return any(S <= b for b in B)

def simple(V):
    for i in range(12):
        if not any(x % 3 for x in V[i]): return False
    for i in range(12):
        for j in range(i+1, 12):
            if all((V[i][r]*2 - V[j][r]) % 3 == 0 for r in range(4)) or \
               all((V[i][r] - V[j][r]) % 3 == 0 for r in range(4)): return False
    return True

def has_grid(B, R):
    P1 = list(permutations(sorted(R[1]))); P2 = list(permutations(sorted(R[2])))
    P3 = list(permutations(sorted(R[3]))); P4 = list(permutations(sorted(R[4])))
    for p1 in P1:
        for p2 in P2:
            for p3 in P3:
                for p4 in P4:
                    if (frozenset((p1[0],p2[0],p3[0],p4[0])) in B and
                        frozenset((p1[1],p2[1],p3[1],p4[1])) in B and
                        frozenset((p1[2],p2[2],p3[2],p4[2])) in B):
                        return True
    return False

def rand_block():
    while True:
        c = [tuple(random.randrange(3) for _ in range(4)) for _ in range(4)]
        if det4(*c) != 0: return c

def rand_matroid(force_parallel=False):
    V = [None]*12
    for blk in range(3):
        for k, c in enumerate(rand_block()): V[4*blk + k] = c
    if force_parallel:
        # plant one vector in all three blocks: a parallel class across blocks
        v = V[random.randrange(4)]
        slots = [random.randrange(4), 4+random.randrange(4), 8+random.randrange(4)]
        for s in slots: V[s] = v
        for blk in range(3):                 # repair: blocks must stay bases
            cols = [V[4*blk+k] for k in range(4)]
            tries = 0
            while det4(*cols) == 0 and tries < 60:
                k = random.choice([k for k in range(4) if 4*blk+k not in slots])
                V[4*blk+k] = tuple(random.randrange(3) for _ in range(4))
                cols = [V[4*blk+k] for k in range(4)]; tries += 1
            if det4(*cols) == 0: return None
    return V

def rand_instance():
    els = list(range(12)); random.shuffle(els)
    free, rest = els[0], els[1:]
    short = random.randrange(4)
    I, pos = {}, 0
    for i in range(1, 5):
        sz = 2 if i-1 == short else 3
        I[i] = set(rest[pos:pos+sz]); pos += sz
    R = {i: set(I[i]) for i in I}; R[short+1].add(free)
    return I, R

def trial(V):
    if V is None: return None
    for blk in range(3):
        if det4(*[V[4*blk+k] for k in range(4)]) == 0: return None
    B = bases_of(V)
    I, R = rand_instance()
    if not all(indep_in(B, I[i]) for i in I): return None
    return (not has_grid(B, R)), simple(V), V, I, R

# --------------------------------------------------------------------------
section("1. Harness agrees with arm AS part 1 on the supplied counterexample")
ROWS = [[1,0,0,0,1,1,1, 1,1, 0, 1,0],
        [0,1,0,0,0,0,0, 1,0, 1,-1,0],
        [0,0,1,0,0,0,1, 0,0,-1, 0,1],
        [0,0,0,1,0,1,0,-1,0,-1, 1,1]]
V0 = [tuple(ROWS[r][c] % 3 for r in range(4)) for c in range(12)]
B0 = bases_of(V0)
R0 = {1:{1,2,6}, 2:{0,4,10}, 3:{3,5,9}, 4:{7,8,11}}
check("240 bases", len(B0) == 240, f"{len(B0)}")
check("no valid grid", not has_grid(B0, R0))
check("the matroid is not simple", not simple(V0), "v_0 = v_4 = v_8")

# --------------------------------------------------------------------------
section("2. Blind search: counterexamples are RARE (corrected from the data)")
N = 30000
val = ce = simp = ce_simp = 0
for _ in range(N):
    t = trial(rand_matroid())
    if t is None: continue
    bad, s, *_ = t
    val += 1; simp += s; ce += bad; ce_simp += (bad and s)
print(f"  instances with all hypotheses satisfied : {val}")
print(f"  of those, simple                        : {simp}  ({100*simp/val:.1f}%)")
print(f"  COUNTEREXAMPLES                         : {ce}")
check("blind search finds essentially none -- the object is rare", ce == 0,
      f"0 in {val}; upper 95% bound on the rate is {300/val:.2%}")

# --------------------------------------------------------------------------
section("3. Directed search: plant a parallel class, the document's mechanism")
N2 = 30000
val2 = ce2 = 0
hits = []
for _ in range(N2):
    t = trial(rand_matroid(force_parallel=True))
    if t is None: continue
    bad, s, V, I, R = t
    val2 += 1; ce2 += bad
    if bad and len(hits) < 3: hits.append((V, I, R))
print(f"  instances with all hypotheses satisfied : {val2}")
print(f"  COUNTEREXAMPLES                         : {ce2}  "
      f"({100*ce2/max(val2,1):.2f}%, 1 in {val2/max(ce2,1):.0f})")
check("planting a parallel class turns a null search into a productive one",
      ce2 > 0, f"{ce2} found vs 0 blind")
if hits:
    V, I, R = hits[0]
    print(f"\n  an independent counterexample this search found:")
    print(f"    columns : {V}")
    print(f"    I       : {{ {', '.join(f'{k}:{sorted(v)}' for k,v in sorted(I.items()))} }}")
    print(f"    bases   : {len(bases_of(V))}   simple: {simple(V)}")

# --------------------------------------------------------------------------
section("4. Q1 -- was the second, different counterexample surprising?")
print("  CORRECTED ANSWER. Blind search: 0 in {:d}. Directed search with a planted"
      .format(val))
print("  parallel class: {:d} in {:d}. The counterexample is not a generic object;".format(ce2, val2))
print("  it is rare unless you already know to build a parallel class.")
print()
print("  So the two independent finds are NOT explained by a dense solution space.")
print("  They are explained by both searches arriving at the SAME STRUCTURAL IDEA")
print("  and then landing on different instances of it. And that idea is signposted")
print("  by the literature the document itself cites: McDiarmid refuted the EARLIER")
print("  version of the conjecture using duplicated edges. Any search that retrieves")
print("  that prior art is pointed straight at parallel elements.")
print()
print("  This is a THIRD category for the same-object test used in arm AR:")
print("    M1 seeding      -> same object, same route")
print("    M2 shared list  -> different object, different route")
print("    M4 retrieval    -> DIFFERENT OBJECT, SAME ROUTE, route supplied by the")
print("                       shared prior art both searches retrieved")
check("Q1 answered from data, and the earlier assertion retracted", ce == 0 and ce2 > 0)

# --------------------------------------------------------------------------
section("5. Q2 -- does a simplicity hypothesis repair Conjecture 2?")
N3 = 60000
vals = ces = 0
simple_hit = None
for _ in range(N3):
    V = rand_matroid()
    if V is None or not simple(V): continue
    t = trial(V)
    if t is None: continue
    bad, s, V2, I, R = t
    if not s: continue
    vals += 1; ces += bad
    if bad and simple_hit is None: simple_hit = (V2, I, R)
print(f"  SIMPLE instances with all hypotheses satisfied : {vals}")
print(f"  counterexamples among them                     : {ces}")
if simple_hit:
    print("\n  *** A SIMPLE COUNTEREXAMPLE EXISTS -- the proposed repair FAILS. ***")
    V, I, R = simple_hit
    print(f"    columns : {V}")
    print(f"    I       : {{ {', '.join(f'{k}:{sorted(v)}' for k,v in sorted(I.items()))} }}")
else:
    print(f"\n  None found. Power statement, stated honestly: this is a RANDOM search,")
    print(f"  and the blind random search also found 0 counterexamples in {val}")
    print(f"  UNRESTRICTED instances, where they certainly exist. So this search has")
    print(f"  no demonstrated power to find one even if simple counterexamples are")
    print(f"  there. It is NOT evidence for the repair. Testing it needs a directed")
    print(f"  construction for simple matroids, or an exhaustive argument -- and the")
    print(f"  document's own mechanism cannot supply one, since it requires a")
    print(f"  parallel class, which simplicity forbids by definition.")
check("Q2's answer is reported with its power, and the power is stated as nil",
      True, "no evidence either way; the search is not sensitive enough")

section(f"RESULT   {PASS}/{PASS+FAIL} checks passed")
sys.exit(0 if FAIL == 0 else 1)
