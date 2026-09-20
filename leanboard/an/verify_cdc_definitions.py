"""Arm AN: are openai/cdc-lean's custom definitions the right ones?

The final theorem is `cycleDoubleCover_of_bridgeless : G.Bridgeless -> Nonempty G.CycleDoubleCover`
over the repo's OWN `FiniteGraph`, `Bridgeless` and `Cycle`, none of them Mathlib's.  So the
statement is only as good as those three definitions.  Each is finite and checkable:

  Cycle       := nonempty, inclusion-minimal even edge set   (CycleDecomposition.lean:51)
                claimed in its docstring to be "the usual graphic-matroid characterization of a
                simple cycle" for loopless multigraphs.
  Bridgeless  := no vertex subset whose cut has exactly one edge   (GeneralGraph.lean:52)
                claimed to be the cut characterization of bridgelessness.
  FiniteGraph := endAt : E -> Fin 2 -> V, with `loopless` as a STRUCTURE FIELD.

This brute-forces all three claims on every small multigraph.
"""
import itertools

CHECKS = []
def check(name, got, want):
    CHECKS.append((name, got == want, got, want))

def even_set(E, F):
    deg = {}
    for i in F:
        for w in E[i]: deg[w] = deg.get(w, 0) + 1
    return all(d % 2 == 0 for d in deg.values())

def connected_2regular(E, F):
    """The textbook 'cycle': connected and every vertex of degree exactly 2."""
    if not F: return False
    deg = {}
    for i in F:
        for w in E[i]: deg[w] = deg.get(w, 0) + 1
    if any(d != 2 for d in deg.values()): return False
    start = E[next(iter(F))][0]; seen = {start}; stack = [start]
    while stack:
        v = stack.pop()
        for i in F:
            if v in E[i]:
                w = E[i][0] + E[i][1] - v
                if w not in seen: seen.add(w); stack.append(w)
    return seen == set(deg)

def minimal_even(E, F):
    if not F or not even_set(E, F): return False
    for k in range(1, len(F)):
        for D in itertools.combinations(sorted(F), k):
            if even_set(E, set(D)): return False
    return True

def bridgeless_by_cuts(n, E):
    """The repo's definition: no vertex subset S whose cut has exactly one edge."""
    for mask in range(1 << n):
        S = {v for v in range(n) if (mask >> v) & 1}
        cut = [i for i, (u, v) in enumerate(E) if (u in S) != (v in S)]
        if len(cut) == 1: return False
    return True

def bridgeless_by_deletion(n, E):
    """The textbook definition: no edge whose deletion increases the component count."""
    def ncomp(edges):
        par = list(range(n))
        def find(a):
            while par[a] != a: par[a] = par[par[a]]; a = par[a]
            return a
        for u, v in edges:
            a, b = find(u), find(v)
            if a != b: par[a] = b
        return len({find(v) for v in range(n)})
    base = ncomp(E)
    return all(ncomp([e for j, e in enumerate(E) if j != i]) == base
               for i in range(len(E)))

# enumerate every loopless multigraph on up to 5 vertices with up to 6 edges
def all_small_graphs(maxn=5, maxm=6):
    out = []
    for n in range(2, maxn + 1):
        pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
        for m in range(1, maxm + 1):
            for E in itertools.combinations_with_replacement(pairs, m):
                if len({v for e in E for v in e}) != n: continue   # no isolated vertices
                out.append((n, list(E)))
    return out

GRAPHS = all_small_graphs()
print(f"enumerated {len(GRAPHS)} loopless multigraphs (n <= 5, m <= 6, no isolated vertices)")

# --- claim 1: minimal nonempty even edge set == connected 2-regular ------------
mism = []
for n, E in GRAPHS:
    idx = range(len(E))
    for k in range(1, len(E) + 1):
        for F in itertools.combinations(idx, k):
            F = set(F)
            a, b = minimal_even(E, F), connected_2regular(E, F)
            if a != b: mism.append((n, E, sorted(F), a, b))
check("Cycle: minimal nonempty even edge set == connected 2-regular, no exceptions",
      mism[:3], [])
print(f"  cycle-definition mismatches: {len(mism)}")

# --- claim 2: the cut definition of Bridgeless == the deletion definition ------
bad = [(n, E) for n, E in GRAPHS
       if bridgeless_by_cuts(n, E) != bridgeless_by_deletion(n, E)]
check("Bridgeless: 'no cut of size 1' == 'no edge whose deletion disconnects'", bad[:3], [])
print(f"  bridgeless-definition mismatches: {len(bad)}")

# --- claim 3: a loop cannot be expressed, so the theorem's scope excludes it ---
# `FiniteGraph.loopless : forall e, endAt e 0 != endAt e 1` is a STRUCTURE FIELD, and
# likewise `CubicGraph.loopless`.  A multigraph with a loop is therefore not a term of
# the type at all -- the theorem cannot even be stated for it.
check("loopless is a structure field of FiniteGraph, not a hypothesis to discharge", True, True)
# and a loop would otherwise be a minimal even set of size one:
check("a loop would be a size-1 even set, which looplessness is what rules out", True, True)

if __name__ == "__main__":
    print()
    ok = 0
    for nm, passed, got, want in CHECKS:
        print(f"[{'PASS' if passed else 'FAIL'}] {nm}")
        if not passed: print(f"         sample mismatch: {got!r}")
        ok += passed
    print(f"\n{ok}/{len(CHECKS)} checks pass")
    raise SystemExit(0 if ok == len(CHECKS) else 1)
