"""Arm AN: execute Kintali's CDC construction (arXiv:2607.14140v1) on real cubic graphs.

The paper claims the Cycle Double Cover Conjecture. Its pipeline, for a loopless
bridgeless cubic multigraph, is:

  1. nowhere-zero F_2^3 flow f (Seymour 6-flow + Tutte group-flow);
  2. at each vertex a "triangle" with a translation t_v, sides carrying two-element
     label sets whose XOR difference is the incident flow value;
  3. the gluing system   t_u XOR t_v XOR eps_e f(e) = d_e   over F_2, claimed always
     solvable (Theorem 9.1);
  4. for each label s, the edges whose common pair contains s form a subgraph in which
     every vertex has degree 0 or 2; its components are the cover's cycles.

Everything here is finite and computable, so this runs the whole pipeline end to end
and checks the output really is a cycle double cover.
"""
import itertools, random

# ---------------------------------------------------------------- graphs -----
def petersen():
    out = [(i, (i + 1) % 5) for i in range(5)]
    out += [(i, i + 5) for i in range(5)]
    out += [(5 + i, 5 + (i + 2) % 5) for i in range(5)]
    return 10, out

def k4():
    return 4, [(a, b) for a in range(4) for b in range(a + 1, 4)]

def k33():
    return 6, [(a, 3 + b) for a in range(3) for b in range(3)]

def theta():                      # multigraph: two vertices, three parallel edges
    return 2, [(0, 1), (0, 1), (0, 1)]

def cube():
    return 8, [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]

def flower_snark(k):              # J_k, k odd >= 5; 4k vertices
    # hub i: a_i=4i, and b_i=4i+1, c_i=4i+2, d_i=4i+3
    E = []
    for i in range(k):
        a, b, c, d = 4*i, 4*i+1, 4*i+2, 4*i+3
        E += [(a, b), (a, c), (a, d)]
    for i in range(k):            # outer cycle on b
        E.append((4*i+1, 4*((i+1) % k)+1))
    for i in range(k):            # inner 2k-cycle on c,d
        E.append((4*i+2, 4*((i+1) % k)+3))
        E.append((4*i+3, 4*((i+1) % k)+2))
    return 4*k, E

def blanusa1():
    # first Blanusa snark, 18 vertices, as an explicit cubic edge list
    E = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(8,9),(9,10),(10,11),
         (11,12),(12,13),(13,14),(14,15),(15,16),(16,17),(17,0),
         (0,8),(1,5),(2,12),(3,7),(4,16),(6,10),(9,13),(11,15),(14,17)]
    return 18, E

def random_cubic(n, seed):
    """Random cubic simple graph by pairing, retried until simple and connected."""
    rng = random.Random(seed)
    for _ in range(4000):
        pts = [v for v in range(n) for _ in range(3)]
        rng.shuffle(pts)
        E = [(pts[2*i], pts[2*i+1]) for i in range(len(pts)//2)]
        if any(u == v for u, v in E): continue
        if len(set(tuple(sorted(e)) for e in E)) != len(E): continue
        deg = [0]*n
        for u, v in E: deg[u] += 1; deg[v] += 1
        if any(d != 3 for d in deg): continue
        if not connected(n, E): continue
        return n, E
    return None

# ------------------------------------------------------------ graph utils ----
def incidence(n, E):
    inc = [[] for _ in range(n)]
    for i, (u, v) in enumerate(E):
        inc[u].append(i); inc[v].append(i)
    return inc

def connected(n, E):
    inc = incidence(n, E); seen = {0}; stack = [0]
    while stack:
        v = stack.pop()
        for i in inc[v]:
            w = E[i][0] + E[i][1] - v
            if w not in seen: seen.add(w); stack.append(w)
    return len(seen) == n

def bridgeless(n, E):
    for i in range(len(E)):
        if not connected(n, [e for j, e in enumerate(E) if j != i]): return False
    return True

def cycle_space_basis(n, E):
    """Fundamental cycles of a spanning tree, as bit-masks over edge indices."""
    inc = incidence(n, E); parent = {0: (None, None)}; order = [0]; tree = set()
    stack = [0]
    while stack:
        v = stack.pop()
        for i in inc[v]:
            w = E[i][0] + E[i][1] - v
            if w not in parent:
                parent[w] = (v, i); tree.add(i); order.append(w); stack.append(w)
    def path_to_root(v):
        out = 0
        while parent[v][0] is not None:
            p, i = parent[v]; out ^= 1 << i; v = p
        return out
    basis = []
    for i, (u, v) in enumerate(E):
        if i in tree: continue
        basis.append((1 << i) ^ path_to_root(u) ^ path_to_root(v))
    return basis

def nowhere_zero_flow(n, E, seed=0, tries=20000):
    """Three cycle-space vectors whose supports cover every edge = nz F_2^3 flow."""
    basis = cycle_space_basis(n, E)
    if not basis: return None
    rng = random.Random(seed); full = (1 << len(E)) - 1
    for _ in range(tries):
        cs = []
        for _ in range(3):
            c = 0
            for b in basis:
                if rng.getrandbits(1): c ^= b
            cs.append(c)
        if (cs[0] | cs[1] | cs[2]) == full:
            return [tuple((c >> i) & 1 for c in cs) for i in range(len(E))]
    return None

# --------------------------------------------------- F_2 linear solver -------
def solve_f2(rows, nvars):
    """rows: list of (mask_of_vars, rhs_bit). Returns a solution list or None."""
    rows = [list(r) for r in rows]
    piv = {}
    for idx in range(len(rows)):
        m, b = rows[idx]
        for p, (pm, pb) in piv.items():
            if (m >> p) & 1: m ^= pm; b ^= pb
        if m == 0:
            if b: return None                      # 0 = 1, inconsistent
            continue
        p = (m & -m).bit_length() - 1
        piv[p] = (m, b)
    x = [0]*nvars
    for p in sorted(piv, reverse=True):
        m, b = piv[p]
        val = b
        mm = m & ~(1 << p)
        while mm:
            j = (mm & -mm).bit_length() - 1
            val ^= x[j]; mm &= mm - 1
        x[p] = val
    return x

# ------------------------------------------------- the paper's pipeline ------
def run(name, n, E, seed=0):
    res = {"name": name, "n": n, "m": len(E)}
    res["bridgeless"] = bridgeless(n, E)
    inc = incidence(n, E)
    res["cubic"] = all(len(inc[v]) == 3 for v in range(n))
    f = nowhere_zero_flow(n, E, seed)
    res["flow"] = f is not None
    if not f: return res
    # Lemma 4.6: three incident values nonzero, distinct, XOR to zero
    ok46 = True
    for v in range(n):
        vals = [f[i] for i in inc[v]]
        x, y, z = vals
        ok46 &= all(any(t) for t in vals)
        ok46 &= len(set(vals)) == 3
        ok46 &= all((x[j] ^ y[j] ^ z[j]) == 0 for j in range(3))
    res["lemma46"] = ok46
    # local orderings and offsets (5.4): g = 000, f(a_v), 000 for a_v, b_v, c_v
    order = {v: inc[v][:] for v in range(n)}
    g = {}
    for v in range(n):
        a, b, c = order[v]
        g[(v, a)] = (0, 0, 0); g[(v, b)] = f[a]; g[(v, c)] = (0, 0, 0)
    # the gluing system: t_u XOR t_v XOR eps_e f(e) = d_e, 3 scalar rows per edge
    # variables: t_v coords 3v+j (j=0,1,2), then eps_e at 3n+e
    nvars = 3*n + len(E)
    rows = []
    for e, (u, v) in enumerate(E):
        d = tuple(g[(u, e)][j] ^ g[(v, e)][j] for j in range(3))
        for j in range(3):
            m = (1 << (3*u + j)) | (1 << (3*v + j))
            if f[e][j]: m |= 1 << (3*n + e)
            rows.append((m, d[j]))
    sol = solve_f2(rows, nvars)
    res["gluing_solvable"] = sol is not None
    if sol is None: return res
    t = [tuple(sol[3*v + j] for j in range(3)) for v in range(n)]
    # sides and the common pair P_e
    def Q(v, e):
        base = tuple(t[v][j] ^ g[(v, e)][j] for j in range(3))
        return frozenset({base, tuple(base[j] ^ f[e][j] for j in range(3))})
    agree = all(Q(u, e) == Q(v, e) for e, (u, v) in enumerate(E))
    res["sides_agree"] = agree
    if not agree: return res
    P = [Q(E[e][0], e) for e in range(len(E))]
    res["pairs_are_2elt"] = all(len(p) == 2 for p in P)
    # label subgraphs and their components
    cover = []
    for s in itertools.product((0, 1), repeat=3):
        Ms = [e for e in range(len(E)) if s in P[e]]
        if not Ms: continue
        sinc = {}
        for e in Ms:
            for w in E[e]: sinc.setdefault(w, []).append(e)
        res.setdefault("deg02", True)
        for w, es in sinc.items():
            if len(es) != 2: res["deg02"] = False
        # components
        seen = set()
        for e0 in Ms:
            if e0 in seen: continue
            comp, stack = set(), [e0]
            while stack:
                e = stack.pop()
                if e in comp: continue
                comp.add(e); seen.add(e)
                for w in E[e]:
                    for e2 in sinc[w]:
                        if e2 not in comp: stack.append(e2)
            cover.append((s, frozenset(comp)))
    # is every component a cycle (connected and 2-regular)?
    cyc = True
    for s, comp in cover:
        deg = {}
        for e in comp:
            for w in E[e]: deg[w] = deg.get(w, 0) + 1
        cyc &= all(d == 2 for d in deg.values())
        cyc &= len(comp) == len(deg)          # #edges == #vertices for a cycle
    res["components_are_cycles"] = cyc
    # THE CHECK: every edge in exactly two members
    cnt = {e: 0 for e in range(len(E))}
    for s, comp in cover:
        for e in comp: cnt[e] += 1
    res["is_CDC"] = all(c == 2 for c in cnt.values())
    res["n_cycles"] = len(cover)
    return res

GRAPHS = [("K4", *k4()), ("theta (multigraph)", *theta()), ("K3,3", *k33()),
          ("cube Q3", *cube()), ("Petersen", *petersen()),
          ("Blanusa snark 1", *blanusa1()),
          ("flower snark J5", *flower_snark(5)),
          ("flower snark J7", *flower_snark(7)),
          ("flower snark J9", *flower_snark(9))]
for s in range(6):
    r = random_cubic(12 + 2*s, 1000 + s)
    if r: GRAPHS.append((f"random cubic n={12+2*s}", *r))

if __name__ == "__main__":
    keys = ["bridgeless", "cubic", "lemma46", "gluing_solvable", "sides_agree",
            "pairs_are_2elt", "deg02", "components_are_cycles", "is_CDC"]
    print(f"{'graph':22s}{'n':>4}{'m':>4}  " + "".join(f"{k[:9]:>10}" for k in keys) + "  cycles")
    allok = True
    for name, n, E in GRAPHS:
        r = run(name, n, E)
        line = f"{name:22s}{r['n']:>4}{r['m']:>4}  "
        for k in keys:
            v = r.get(k, "-")
            line += f"{('YES' if v is True else 'NO' if v is False else '-'):>10}"
        line += f"  {r.get('n_cycles','-')}"
        print(line)
        allok &= all(r.get(k) is True for k in keys)
    print(f"\nconstruction produced a valid cycle double cover on every graph: {allok}")
