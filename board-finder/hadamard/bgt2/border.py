#!/usr/bin/env python3
"""A border/core detector for Hadamard matrices, with controls.

Brief E asks a run to MEASURE the border width of Alpoge's twelve matrices rather
than relay it. This is the instrument for that, built and tested here first --
because the last three hand-written controls shipped from this session were wrong
and were caught by their own assertions.

What it does: given H of order N, for each candidate border width b it tests
whether the core H[b:, b:] is CIRCULANT (every row a cyclic shift of the first).
That is the structure the classical bordered constructions produce: Paley I gives
H(q+1) as a width-1 border around a circulant core of order q.

LIMITATION, stated because it bounds any conclusion: "border of width b around a
core" is a convention, and I do not have the source's. This detector implements
ONE precise version of it -- circulant core after deleting b leading rows and
columns. A source meaning block-circulant with several blocks, or a border that is
not the leading rows, will not be measured by this. Brief E asks for the
convention first, and this tool second.

Run: python3 border.py            (controls only)
     python3 border.py DIR        (also every *.csv.gz in DIR, e.g. an hoa64 clone)
"""
import glob, gzip, os, re, sys

def is_hadamard(M):
    n = len(M)
    if any(len(r) != n for r in M): return False
    if any(abs(x) != 1 for r in M for x in r): return False
    for i in range(n):
        for j in range(i, n):
            s = sum(M[i][k] * M[j][k] for k in range(n))
            if s != (n if i == j else 0): return False
    return True

def is_circulant(C):
    """Every row a left cyclic shift of the row above."""
    m = len(C)
    if m == 0: return False
    first = C[0]
    for i in range(m):
        if C[i] != first[-i:] + first[:-i]:
            return False
    return True

def core_after(M, b):
    return [row[b:] for row in M[b:]]

MIN_CORE = 3   # a 1x1 or 2x2 core is trivially circulant -- see the note below

def detect(M, max_b=8):
    """Return the b values whose core is circulant and big enough to mean anything.

    MIN_CORE exists because the controls caught a false positive: at Paley q=7
    (order 8) b=7 leaves a 1x1 core, which is circulant by definition, and small
    Sylvester matrices hit the same way. Every spurious detection in the first
    run of this file had a 1x1 core. Without the guard the tool reports noise on
    real data, and the noise looks like a large border width."""
    return [b for b in range(0, max_b + 1) if len(M) - b >= MIN_CORE
            and is_circulant(core_after(M, b))]

# ------------------------------------------------------------------ controls
def legendre(a, q):
    a %= q
    if a == 0: return 0
    return 1 if pow(a, (q - 1) // 2, q) == 1 else -1

def paley1(q):
    """H(q+1) for q = 3 mod 4 prime: width-1 border, circulant core of order q."""
    Q = [[legendre(j - i, q) for j in range(q)] for i in range(q)]
    H = [[0] * (q + 1) for _ in range(q + 1)]
    H[0][0] = 1
    for j in range(q): H[0][j + 1] = 1
    for i in range(q): H[i + 1][0] = -1
    for i in range(q):
        for j in range(q):
            H[i + 1][j + 1] = Q[i][j] if i != j else 1
    return H

def sylvester(k):
    H = [[1]]
    for _ in range(k):
        H = [r + r for r in H] + [r + [-x for x in r] for r in H]
    return H

print("CONTROLS")
print()
for q in (7, 11, 19, 23):
    H = paley1(q)
    assert is_hadamard(H), f"Paley I at q={q} is not Hadamard"
    bs = detect(H)
    print(f"  Paley I q={q:>3}: order {q+1:>3}, Hadamard OK, circulant core at b = {bs}")
    # POSITIVE CONTROL: b=1 must be detected, because the core IS Q+I, a circulant
    assert 1 in bs, (q, bs)
    # NEGATIVE CONTROL: b=0 must NOT be, because the full bordered matrix is not circulant
    assert 0 not in bs, (q, bs)
    # and with the guard, b=1 is now the ONLY detection at every Paley order
    assert bs == [1], (q, bs)
print("  ASSERTED: b=1 detected and b=0 rejected at every Paley order. The")
print("  detector can both fire and fail to fire, which is the point of a control.")
print()
for k in (2, 3, 4):
    H = sylvester(k)
    assert is_hadamard(H)
    bs = detect(H)
    print(f"  Sylvester 2^{k} = {2**k:>3}: Hadamard OK, circulant core at b = {bs}")
print("  Sylvester matrices are a NEGATIVE CASE for this convention -- they are")
print("  built by doubling, not bordering, so a circulant core is not expected.")
print()
# A third negative test: break a Paley core and confirm detection stops.
H = paley1(11)
H[3][5] *= -1
assert not is_hadamard(H), "the break should destroy the Hadamard property"
assert 1 not in detect(H), "the detector must stop firing on a broken core"
print("  THIRD NEGATIVE TEST: flipping one entry of the Paley q=11 core destroys")
print("  both the Hadamard property and the b=1 detection. Both asserted.")

# ------------------------------------------------------------------ real data
if len(sys.argv) > 1:
    d = sys.argv[1]
    files = sorted(glob.glob(os.path.join(d, "*.csv.gz")),
                   key=lambda f: int(re.search(r"(\d+)", os.path.basename(f)).group(1)))
    if not files:
        sys.exit(f"no *.csv.gz under {d}")
    print()
    print(f"MEASURED, {len(files)} files under {d}")
    print(f"  {'order':>6} {'circulant core at b':>22}")
    for f in files:
        n = int(re.search(r"(\d+)", os.path.basename(f)).group(1))
        with gzip.open(f, "rt") as fh:
            M = [[int(x) for x in line.split(",")] for line in fh if line.strip()]
        print(f"  {n:>6} {str(detect(M)):>22}")
    print()
    print("  An EMPTY list is a real result: it means the core is not circulant")
    print("  under this convention, and the convention is wrong or the matrix is")
    print("  normalized differently. Report it as measured, not as a failure.")
else:
    print()
    print("No directory given, so controls only. Pass an hoa64 matrices/ clone to measure.")
