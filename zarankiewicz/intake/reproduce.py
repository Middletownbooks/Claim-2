"""
reproduce.py -- every externally-anchored control, in one run.
    python3 reproduce.py            # fast controls (~60 s)
    python3 reproduce.py --n6       # + exhaustive n=6 sweep (~60 s)
    python3 reproduce.py --certificate
"""
import sys, time
from itertools import combinations
import numpy as np
from cog import CO, Z, canon
from checkers import KINDS, family, pseudo_tight, is_tight, bracket, shortest_label_sets
from search import staircase, search, thm7_availability, ablation_valid
from generator import pair_optimal_sets, total_crossings, pair_crossings
import certificate as cert

OK = []
def chk(label, cond, detail=""):
    OK.append(bool(cond))
    print(f"[{'PASS' if cond else 'FAIL'}] {label} {detail}")

def classes(n, G=None):
    G = G or CO(n)
    out = {}
    for b in range(G.NV):
        for c in range(b, G.NV):
            for d in range(c, G.NV):
                q = (0, b, c, d)
                k = G.class_canon(q)
                if k not in out: out[k] = q
    return G, out

print("=== Woodall's published numbers ===")
G5 = CO(5); D5 = G5.dist_matrix(); A5 = G5.antidist_matrix(D5)
maps5 = G5.relabel_maps()
def cset(ms): return min(tuple(sorted(m[v] for v in ms)) for m in maps5)
def enum(m, cap):
    hits = []
    def rec(start, part, ch):
        if len(ch) == m:
            if part <= cap: hits.append((part, tuple(ch)))
            return
        for v in range(start, G5.NV):
            p = part
            for u in ch: p += A5[v][u]
            ch.append(v); rec(v, p, ch); ch.pop()
    rec(0, 0, []); return hits
h = enum(5, 16)
chk("program 1: 32 classes of (5,5)-sets at antisum 16",
    len({cset(s) for p, s in h if p == 16}) == 32 and min(p for p, _ in h) == 16)
h = enum(7, 35)
chk("program 3: unique (7,5)-set below 36, at 34 (Kleitman's)",
    min(p for p, _ in h) == 34 and len({cset(s) for p, s in h if p == 34}) == 1)
chk("K_{7,7} staircase = 79,56,36,21,9,3",
    [staircase(7,7)[k] for k in (7,6,5,4,3,2)] == [79,56,36,21,9,3])

G7 = CO(7); D7 = G7.dist_matrix(); A7p = G7.antidist_matrix(D7)
A7 = np.array(A7p, dtype=np.int32)
stab7 = [m for m in G7.stabiliser() if m != list(range(G7.NV))]
c, sv, el, ab = search(G7, A7, A7p, stab7, 5, staircase(5,7))
chk("program 2: every (5,7)-set has antisum >= 36 (zero-survivor sweep)",
    not ab and len(sv) == 0, f"nodes {sum(c)}")
chk("Thm 3(c): d(a,abar)=Z(n), abar the unique eccentric vertex",
    all(D7[a][G7.rev[a]] == Z(7) and D7[a].count(Z(7)) == 1 for a in range(G7.NV)))
av = thm7_availability(11, 7)
chk("Thm 7 availability: m=7 yes, m=9 via m'=4 only, m=11 none",
    all(not v['exact'] for v in av.values())
    and [k for k,v in thm7_availability(9,7).items() if v['exact']] == [4]
    and sorted(k for k,v in thm7_availability(7,7).items() if v['exact']) == [2,4],
    f"m=11 weakened bounds {{m': {{k: v['bound']}} }} = "
    f"{ {k: v['bound'] for k, v in av.items()} }")

print("\n=== the Q-family lattice and the bracket ===")
G4 = CO(4); G6 = CO(6); D6 = G6.dist_matrix(); A6 = G6.antidist_matrix(D6)
F4 = {k: family(G4, k) for k in KINDS}
tot = lambda f: sum(len(f[u][w]) for u in range(G4.NV) for w in range(G4.NV))
chk("CO_4 family sizes both/walk/path/arbitrary = 234/282/594/1758",
    [tot(F4[k]) for k in ('both','walk','path','arbitrary')] == [234,282,594,1758])
sub = lambda a,b: all(F4[a][u][w] <= F4[b][u][w] for u in range(6) for w in range(6))
chk("lattice: 'both' bottom, 'arbitrary' top, walk/path incomparable",
    all(sub('both',k) for k in ('walk','path','arbitrary'))
    and all(sub(k,'arbitrary') for k in ('both','walk','path'))
    and not sub('walk','path') and not sub('path','walk'))

print("\n=== two-sided control: the certified generator ===")
pos = pair_optimal_sets(G6, A6, 4, 120, seed=11, time_cap=40)
res = [bracket(G6, D6, G4, F4, list(M))[0] for M, _, _ in pos]
t_ok = sum(1 for M,_,_ in pos if is_tight(G6,D6,G4,F4['walk'],list(M)) is True)
p_ok = sum(1 for M,_,_ in pos if pseudo_tight(G6,D6,G4,F4['walk'],list(M)))
chk("pair-optimal drawings are tight AND pseudo-tight (over-strictness side)",
    t_ok == len(pos) == p_ok, f"{t_ok}/{len(pos)}")
chk("none of them is flagged a counterexample", not any(res))

print("\n=== the counterexamples ===")
M = cert.parse(cert.PUBLISHED, G6)
ok, pt, tg = bracket(G6, D6, G4, F4, M)
anti = sum(A6[M[i]][M[j]] for i,j in combinations(range(4),2))
chk("published (4,6)-set: pseudo-tight at 'both', not tight at 'arbitrary'",
    ok and pt and tg is False, f"antisum {anti}")
allok = all(bracket(G6, D6, G4, F4, cert.parse(s, G6))[0] for s in cert.CORE_14)
chk("all 14 core sets are counterexamples under EVERY reading", allok)

if '--n6' in sys.argv:
    print("\n=== exhaustive n=6 sweep (slow) ===")
    t0 = time.time(); _, cl = classes(6, G6)
    hits = {}
    for k in KINDS:
        cache = {}
        hits[k] = {key for key, q in cl.items()
                   if pseudo_tight(G6,D6,G4,F4[k],q,cache) and is_tight(G6,D6,G4,F4[k],q) is False}
    core = set.intersection(*hits.values()); anyk = set.union(*hits.values())
    chk("6,930 classes; per-reading 48/19/54/22; core 14; any 59",
        len(cl)==6930 and [len(hits[k]) for k in ('both','walk','path','arbitrary')]==[48,19,54,22]
        and len(core)==14 and len(anyk)==59, f"[{time.time()-t0:.0f}s]")

if '--certificate' in sys.argv:
    print("\n=== certificate for the published (4,6)-set ===")
    mp = list(combinations(range(4),2))
    for i,v in enumerate(M): print(f"  a{i} = {G6.V[v]}")
    print(f"  antidistances {[A6[M[i]][M[j]] for i,j in mp]}  antisum {anti}")
    rows = [sorted(shortest_label_sets(G6,D6,M[i],M[j])) for i,j in mp]
    lab = lambda m:[G6.labellist[b] for b in range(G6.NL) if (m>>b)&1]
    print(f"  shortest-antipath label sets, sizes {[len(r) for r in rows]}:")
    for pi,(i,j) in enumerate(mp):
        print(f"    a{i}a{j}: " + " | ".join(str(lab(x)) for x in rows[pi]))
    _, N = pseudo_tight(G6,D6,G4,F4['both'],M,{},want_witness=True)
    print(f"  pseudo-tightness witness N = {[G4.V[v] for v in N]}")
    r = __import__('generator').realise(G6, M, seed=77)
    if r:
        Pn, P4, img = r
        print(f"  geometric realisation found; isomorphic copy {img}")
        print(f"  crossings by direct segment intersection = {total_crossings(P4, Pn)} "
              f"(> antisum {anti})")
        print(f"  per-pair geometric vs antidistance: "
              f"{[(pair_crossings(P4,Pn,i,j), A6[img[i]][img[j]]) for i,j in mp]}")

print(f"\n{sum(OK)}/{len(OK)} controls passed")
sys.exit(0 if all(OK) else 1)
