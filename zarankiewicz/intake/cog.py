"""
cog.py -- the cyclic-order graph CO_n of Woodall (1993), J. Graph Theory 17(6) 657-671.

V(CO_n) = the (n-1)! cyclic orderings of an n-set, canonicalised with 0 leading.
a ~ b   iff b comes from a by transposing two CYCLICALLY adjacent elements
          (positions i, i+1 mod n -- the wraparound pair is an edge too).
Each edge carries a LABEL: the 2-subset {x,y} of the ground set transposed.
abar    = the reverse cyclic ordering ("antipode").
dbar(a,b) := d(a, bbar)   ("antidistance").
An (m,n)-set is a MULTISET of m elements of V(CO_n); its antisum is the sum of
dbar over all C(m,2) pairs.

Validated against Woodall's published values -- see reproduce.py.
"""
from itertools import permutations, combinations
from collections import deque


def Z(n):
    """Z(n) = floor(n/2) * floor((n-1)/2).  cr(K_{m,n}) is conjectured = Z(m)Z(n)."""
    return (n // 2) * ((n - 1) // 2)


def canon(t):
    """Canonical representative of a cyclic ordering: rotate so 0 leads."""
    i = t.index(0)
    return t[i:] + t[:i]


class CO:
    """CO_n.  Attributes:
        V         list of (n-1)! cyclic orderings (tuples, 0 first)
        idx       ordering -> vertex index
        NV        |V(CO_n)| = (n-1)!
        labellist list of C(n,2) ground-set pairs, in combinations(range(n),2) order
        labelidx  pair -> label index
        NL        C(n,2)
        adj       adj[u] = [(v, label), ...], n entries, one per cyclic position
        labnbr    labnbr[u][lab] = v if lab is cyclically adjacent in u, else -1
        rev       rev[u] = index of ubar
    """

    def __init__(self, n):
        self.n = n
        self.V = [(0,) + p for p in permutations(range(1, n))]
        self.idx = {v: i for i, v in enumerate(self.V)}
        self.NV = len(self.V)
        self.labellist = list(combinations(range(n), 2))
        self.labelidx = {p: i for i, p in enumerate(self.labellist)}
        self.NL = len(self.labellist)
        self.adj, self.labnbr = [], []
        for t in self.V:
            row, ln = [], [-1] * self.NL
            for i in range(n):
                j = (i + 1) % n
                l = list(t)
                l[i], l[j] = l[j], l[i]
                lab = self.labelidx[(min(t[i], t[j]), max(t[i], t[j]))]
                w = self.idx[canon(tuple(l))]
                row.append((w, lab))
                ln[lab] = w
            self.adj.append(row)
            self.labnbr.append(ln)
        self.rev = [self.idx[canon(tuple(reversed(t)))] for t in self.V]

    def bfs(self, s):
        d = [-1] * self.NV
        d[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            du = d[u] + 1
            for v, _ in self.adj[u]:
                if d[v] < 0:
                    d[v] = du
                    q.append(v)
        return d

    def dist_matrix(self):
        """Full NV x NV distance matrix. n=7 -> 720^2, fine. n=9 -> 40320^2, ~1.6GB as int8."""
        return [self.bfs(s) for s in range(self.NV)]

    def antidist_matrix(self, D):
        r = self.rev
        return [[D[a][r[b]] for b in range(self.NV)] for a in range(self.NV)]

    def relabel_maps(self, with_reversal=True):
        """The isomorphism group acting on V(CO_n): ground-set relabellings S_n,
        optionally composed with a -> abar.  Order 2*n!.  Reproducing Woodall's
        counts 32 and 1 is what fixes this as the intended notion (reproduce.py)."""
        out = []
        for s in permutations(range(self.n)):
            m = [self.idx[canon(tuple(s[x] for x in v))] for v in self.V]
            out.append(m)
            if with_reversal:
                out.append([self.rev[i] for i in m])
        return out

    def stabiliser(self, v0=0):
        """Subgroup fixing vertex v0.  Dihedral, order 2n."""
        return [m for m in self.relabel_maps() if m[v0] == v0]

    def class_canon(self, M, maps=None, stab=None, _cache={}):
        """Canonical form of a multiset M under the full group, computed with
        |M| * 2n maps rather than 2*n!: the lex-least sorted image must begin
        with vertex 0, so only maps sending some element of M to 0 can win."""
        key = id(self)
        if key not in _cache:
            _cache[key] = (self.relabel_maps(), self.stabiliser())
        allm, st0 = _cache[key]
        best = None
        for e in set(M):
            me = next(m for m in allm if m[e] == 0)
            for h in st0:
                c = tuple(sorted(h[me[x]] for x in M))
                if best is None or c < best:
                    best = c
        return best
