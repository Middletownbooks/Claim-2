#!/usr/bin/env python3
"""Independent partial replication of Mazur, 'An exact counterexample to Berlekamp's
temperature-2 conjecture for Domineering' (Aug 14 2026).

Checks everything in the paper that does NOT require evaluating the 26-cell game tree:
coordinates, connectivity, legal-move counts, the checkerboard obstruction, the component
splits after the two canonical moves, the B' construction, the full 30-move rectangle
replay, and the thermograph arithmetic.

Does NOT check G(B) = {17/8 | -2+*}. That needs a CGT engine with canonical forms and
Conway-order comparison, and is the expensive part of any real replication.

Nothing here is taken from the paper's prose except the coordinate lists and the move
table, both transcribed verbatim.
"""
from fractions import Fraction as F
import itertools, sys

# --- sec.3 eq (3.1), transcribed verbatim -----------------------------------------
B = [(0,0),(0,1),(0,2),(1,2),(1,5),(1,7),(2,2),(2,5),(2,6),(2,7),
     (3,2),(3,3),(3,4),(3,5),(3,6),(4,4),(4,5),(4,6),
     (5,2),(5,3),(5,4),(6,2),(7,2),(8,0),(8,1),(8,2)]
C, U, W = (3,5), (3,6), (4,5)

# --- appendix A table 1, transcribed verbatim -------------------------------------
ROUNDS = [
 (((0,2),(0,3)), ((0,0),(1,0))), (((0,4),(0,5)), ((1,3),(2,3))),
 (((0,6),(0,7)), ((1,7),(2,7))), (((1,1),(1,2)), ((2,6),(3,6))),
 (((1,5),(1,6)), ((5,7),(6,7))), (((2,4),(2,5)), ((7,5),(8,5))),
 (((3,0),(3,1)), ((7,6),(8,6))), (((3,3),(3,4)), ((7,7),(8,7))),
 (((4,0),(4,1)), ((8,0),(9,0))), (((4,3),(4,4)), ((8,1),(9,1))),
 (((5,0),(5,1)), ((9,3),(10,3))), (((6,0),(6,1)), ((9,4),(10,4))),
 (((6,2),(6,3)), ((9,5),(10,5))), (((7,0),(7,1)), ((9,6),(10,6))),
 (((8,3),(8,4)), ((9,7),(10,7))),
]

fails = []
def check(label, cond, detail=""):
    print(f"  [{'PASS' if cond else 'FAIL'}] {label}" + (f"  — {detail}" if detail else ""))
    if not cond: fails.append(label)

def components(cells):
    cells = set(cells); seen = set(); out = []
    for c in cells:
        if c in seen: continue
        stack, comp = [c], []
        seen.add(c)
        while stack:
            x,y = stack.pop(); comp.append((x,y))
            for n in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
                if n in cells and n not in seen:
                    seen.add(n); stack.append(n)
        out.append(sorted(comp))
    return sorted(out, key=len, reverse=True)

def moves(cells):
    s = set(cells)
    v = [((x,y),(x,y+1)) for (x,y) in s if (x,y+1) in s]
    h = [((x,y),(x+1,y)) for (x,y) in s if (x+1,y) in s]
    return v, h

print("=" * 78)
print("PART 1 — the value core B  (prop 1.1, sec.3)")
print("=" * 78)
check("26 cells, no duplicates", len(B) == 26 and len(set(B)) == 26, f"{len(set(B))}")
check("B is connected", len(components(B)) == 1, f"{len(components(B))} component(s)")
v, h = moves(B)
check("14 legal Left (vertical) moves", len(v) == 14, f"got {len(v)}")
check("14 legal Right (horizontal) moves", len(h) == 14, f"got {len(h)}")
check("C-U is a legal vertical move", tuple(sorted((C,U))) in [tuple(sorted(m)) for m in v])
check("C-W is a legal horizontal move", tuple(sorted((C,W))) in [tuple(sorted(m)) for m in h])

print("\n" + "=" * 78)
print("PART 2 — the checkerboard obstruction  (sec.5)")
print("=" * 78)
blk = sum(1 for (x,y) in B if (x+y) % 2 == 0)
wht = 26 - blk
check("colour split is 14 / 12", {blk, wht} == {14, 12}, f"black {blk}, white {wht}, imbalance {abs(blk-wht)}")
check("imbalance 2 exceeds any rectangle's (0 or 1)", abs(blk-wht) == 2,
      "so B is not a rectangle remainder — the paper's reason for needing B'")

print("\n" + "=" * 78)
print("PART 3 — component splits after the two canonical moves  (prop 4.1)")
print("=" * 78)
afterL = components([c for c in B if c not in (C,U)])
afterR = components([c for c in B if c not in (C,W)])
check("after C-U: components of sizes 19 and 5",
      sorted(len(c) for c in afterL) == [5,19], f"got {sorted(len(c) for c in afterL)}")
check("after C-W: components of sizes 17 and 7",
      sorted(len(c) for c in afterR) == [7,17], f"got {sorted(len(c) for c in afterR)}")

print("\n" + "=" * 78)
print("PART 4 — the rectangle-reachable witness B'  (thm 1.2, eq 1.4)")
print("=" * 78)
Bp = set((x+2, y) for (x,y) in B) | {(0,1), (1,4)}
check("B' has 28 cells", len(Bp) == 28, f"got {len(Bp)}")
check("B' fits in {0..10} x {0..7}",
      all(0 <= x <= 10 and 0 <= y <= 7 for (x,y) in Bp))
comps = components(Bp)
check("B' has exactly 3 components", len(comps) == 3, f"sizes {[len(c) for c in comps]}")
check("components are 26 + 1 + 1", sorted(len(c) for c in comps) == [1,1,26])
vp, hp = moves(Bp)
check("the two adjoined cells have no legal move",
      all(cell not in [c for m in vp+hp for c in m] for cell in [(0,1),(1,4)]),
      "so they contribute game value 0 and G(B') = G(B)")

print("\n" + "=" * 78)
print("PART 5 — full replay of the 30-move sequence  (table 1)")
print("=" * 78)
board = set(itertools.product(range(11), range(8)))
check("11 x 8 rectangle has 88 cells", len(board) == 88)
ply = 0; ok = True
for rnd, (L, R) in enumerate(ROUNDS, 1):
    for mv, who, orient in ((L,"Left","V"), (R,"Right","H")):
        ply += 1
        (x1,y1),(x2,y2) = mv
        inb = all(0 <= x <= 10 and 0 <= y <= 7 for (x,y) in mv)
        good_or = (x1 == x2 and abs(y1-y2) == 1) if orient == "V" else (y1 == y2 and abs(x1-x2) == 1)
        free = mv[0] in board and mv[1] in board
        if not (inb and good_or and free):
            print(f"  [FAIL] ply {ply} (round {rnd}, {who}) {mv}: "
                  f"in-bounds={inb} orientation={good_or} cells-free={free}")
            ok = False
        board -= set(mv)
check("all 30 moves legal, in bounds, correctly oriented, non-overlapping", ok)
check("30 dominoes cover 60 cells", len(board) == 28, f"{88-len(board)} covered, {len(board)} left")
check("final uncovered set is EXACTLY B'", board == Bp,
      "identical" if board == Bp else f"symmetric difference {sorted(board ^ Bp)}")
check("15 Left moves and 15 Right moves", len(ROUNDS) == 15)

print("\n" + "=" * 78)
print("PART 6 — thermograph arithmetic  (prop 1.1, eq 2.2)")
print("=" * 78)
a, b = F(17,8), F(-2)          # left mast 17/8, right mast -2 (the * does not move the mast)
s = (a - b) / 2                 # walls a - s and b + s meet here
m = (a + b) / 2
check("walls meet at s = 33/16", s == F(33,16), f"s = {s} = {float(s)}")
check("meeting height (mean) = 1/16", m == F(1,16), f"m = {m}")
check("a - s == b + s at the meeting point", a - s == b + s, f"both = {a-s}")
check("temperature strictly exceeds 2", s > 2, f"{float(s)} > 2, margin {float(s-2)} = 1/16")

print("\n" + "=" * 78)
print(f"RESULT: {len(fails)} failure(s)" + (": " + "; ".join(fails) if fails else ""))
print("=" * 78)
print("""
NOT CHECKED HERE — and this is the whole mathematical content:
  G(B) = {17/8 | -2+*}, i.e. the value of the 26-cell game tree, the domination of
  the other 13+13 raw options, and the uniqueness of equality. That needs a CGT
  engine with canonical forms and Conway-order comparison. Everything above is
  scaffolding around that one unverified claim.
""")
sys.exit(1 if fails else 0)
