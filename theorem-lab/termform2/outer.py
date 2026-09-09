#!/usr/bin/env python3
"""
The Round-2 outer search, vectorised.

The outer enumeration is where the work is: with 506 atoms and the Round-1 beam
it expands ~13 million candidates per condition, and the reference evaluator in
`termform/language.py` walks a tree per object per candidate. Here each
candidate's value vector is computed once, elementwise, from its two children's
vectors.

This is an implementation change, not a semantic one, and it is checked: every
vectorised operator is verified against the reference evaluator on random
inputs, and a random sample of enumerated terms is re-evaluated with the
reference evaluator and compared (`verify()`).
"""
import hashlib
import random

import numpy as np

import synth3 as S

CAP = 10 ** 9


def _np_pow(a, b):
    """Exactly `language._pow`, elementwise.

    For a <= 1 the reference returns a. Otherwise it returns CAP when b > 40,
    and min(a**b, CAP) below that. Repeated squaring with a clamp after every
    multiply is exact here: for base >= 1 every intermediate is <= the true
    value, so a clamp fires only when the true value already exceeds CAP.
    """
    e = np.minimum(b, np.int64(41)).copy()
    res = np.ones_like(a)
    base = np.minimum(a, np.int64(CAP)).copy()
    while e.any():
        odd = (e & 1).astype(bool)
        res = np.where(odd, np.minimum(res * base, np.int64(CAP)), res)
        e = e >> 1
        if e.any():
            base = np.minimum(base * base, np.int64(CAP))
    return np.where(a <= 1, a, res)


def _safe(f):
    def g(a, b):
        nz = b != 0
        bb = np.where(nz, b, np.int64(1))
        return np.where(nz, f(a, bb), np.int64(0))
    return g


NPOPS = {
    "add": lambda a, b: a + b,
    "sub": lambda a, b: np.maximum(a - b, np.int64(0)),
    "mul": lambda a, b: np.minimum(a * b, np.int64(CAP)),
    "div": _safe(lambda a, b: a // b),
    "mod": _safe(lambda a, b: a % b),
    "gcd": np.gcd,
    "min": np.minimum,
    "max": np.maximum,
    "pow": _np_pow,
}
OPS = list(S.BINOPS)
assert set(OPS) == set(NPOPS)


def _neg(d):
    """Order key that makes a max-heap select the SMALLEST digests, matching
    the batch `sort(key=digest)[:beam]` the incremental beam replaces."""
    return -int.from_bytes(d, "big")


def digest(v):
    return hashlib.blake2b(v.tobytes(), digest_size=16).digest()


class Outer:
    """One outer enumeration. `atoms` is a list of terms; their costs come from
    the cost model in synth3 (1 for a named unit, the expanded size under the
    re-expansion condition)."""

    def __init__(self, atoms, objects, cap=300000, beam=1200,
                 sample_per_level=5000, seed=20260909, max_atom_cost=None):
        self.objects = list(objects)
        self.cap, self.beam = cap, beam
        self.rng = random.Random(seed)
        self.sample_per_level = sample_per_level
        self.nodes = []          # i -> ("atom", term) | ("op", name, i1, i2)
        self.vec = {}            # i -> np.ndarray, kept nodes only
        self.by_size = {}
        self.seen = set()
        self.level_log = []
        self.watch_hits = {}
        self.samples = {}
        self.expansions = 0
        self.truncated = False
        self.atoms_over_budget = 0
        for t in atoms:
            c = S.size(t)
            if max_atom_cost is not None and c > max_atom_cost:
                self.atoms_over_budget += 1   # unusable at this budget
                continue
            v = np.array([S.ev(t, {"n": o}) for o in self.objects],
                         dtype=np.int64)
            i = self._node(("atom", t), v)
            self.by_size.setdefault(c, []).append(i)
            self.seen.add(digest(v))

    def _node(self, rec, v=None):
        self.nodes.append(rec)
        i = len(self.nodes) - 1
        if v is not None:
            self.vec[i] = v
        return i

    def term_of(self, i):
        r = self.nodes[i]
        return r[1] if r[0] == "atom" else (r[1], self.term_of(r[2]),
                                            self.term_of(r[3]))

    def run(self, max_size, watch=()):
        watch = {digest(np.array(v, dtype=np.int64)): v for v in watch}
        for d in watch:
            self.watch_hits.setdefault(d, [])
        # atoms may already hit a watched vector
        for c, idxs in list(self.by_size.items()):
            for i in idxs:
                d = digest(self.vec[i])
                if d in watch:
                    self.watch_hits[d].append((c, i))
        for s in range(1, max_size + 1):
            if s > 2:
                self._level(s, watch)
            self.level_log.append({
                "cost": s, "classes_cumulative": len(self.seen),
                "kept_at_level": len(self.by_size.get(s, ())),
                "expansions_cumulative": self.expansions,
                "truncated": self.truncated})
            if self.truncated:
                break
        return self

    def _level(self, s, watch):
        """One cost level.

        The beam is applied INCREMENTALLY through a bounded heap keyed on the
        value-vector digest, so at most `beam` candidate vectors are ever
        resident. An earlier version buffered every new class of the level
        before sorting, which made memory -- not the declared budget -- the
        binding constraint."""
        import heapq
        heap = []                      # max-heap of (-digest_rank, seq, rec, v)
        res, nres, seq = [], 0, 0
        for a in range(1, s):
            b = s - a - 1
            if b < 1:
                continue
            left = self.by_size.get(a, ())
            right = self.by_size.get(b, ())
            if not left or not right:
                continue
            for i1 in left:
                v1 = self.vec[i1]
                for i2 in right:
                    v2 = self.vec[i2]
                    for op in OPS:
                        self.expansions += 1
                        v = NPOPS[op](v1, v2)
                        d = digest(v)
                        if d in watch:
                            self.watch_hits[d].append(
                                (s, self._node(("op", op, i1, i2))))
                        if d in self.seen:
                            continue
                        self.seen.add(d)
                        rec = ("op", op, i1, i2)
                        nres += 1
                        if len(res) < self.sample_per_level:
                            res.append(rec)
                        else:
                            j = self.rng.randrange(nres)
                            if j < self.sample_per_level:
                                res[j] = rec
                        seq += 1
                        item = (_neg(d), seq, rec, v)
                        if len(heap) < self.beam:
                            heapq.heappush(heap, item)
                        elif item[0] > heap[0][0]:
                            heapq.heapreplace(heap, item)
                        if len(self.seen) >= self.cap:
                            self.truncated = True
                            break
                    if self.truncated:
                        break
                if self.truncated:
                    break
            if self.truncated:
                break
        kept = sorted(heap, key=lambda x: (x[0], x[1]), reverse=True)
        self.by_size[s] = [self._node(rec, v) for _, _, rec, v in kept]
        self.samples[s] = [self._node(rec) for rec in res]

    # ---- verification -------------------------------------------------
    def verify(self, k=300, rng=None):
        """Re-evaluate a random sample of enumerated terms with the reference
        evaluator and compare against the vectorised value."""
        rng = rng or random.Random(7)
        pool = [i for idxs in self.by_size.values() for i in idxs
                if i in self.vec]
        bad = 0
        for i in rng.sample(pool, min(k, len(pool))):
            t = self.term_of(i)
            ref = np.array([S.ev(t, {"n": o}) for o in self.objects],
                           dtype=np.int64)
            if not np.array_equal(ref, self.vec[i]):
                bad += 1
        return {"checked": min(k, len(pool)), "mismatches": bad}


def verify_operators(trials=40000, seed=1):
    """Every vectorised operator against `language.BINOPS` on random inputs."""
    rng = random.Random(seed)
    vals = [0, 1, 2, 3, 4, 7, 10, 41, 42, 100, 999, 10 ** 6, CAP - 1, CAP]
    bad = []
    for _ in range(trials):
        a = rng.choice(vals) if rng.random() < .5 else rng.randrange(0, 2000)
        b = rng.choice(vals) if rng.random() < .5 else rng.randrange(0, 2000)
        A = np.array([a], dtype=np.int64)
        B = np.array([b], dtype=np.int64)
        for op in OPS:
            if int(NPOPS[op](A, B)[0]) != S.BINOPS[op](a, b):
                bad.append((op, a, b, int(NPOPS[op](A, B)[0]),
                            S.BINOPS[op](a, b)))
    return bad


if __name__ == "__main__":
    bad = verify_operators()
    print("operator mismatches: %d" % len(bad))
    for x in bad[:10]:
        print("  ", x)
