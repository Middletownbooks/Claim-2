# The 219 class is a single orbit under S_7 x <rev>, so the set of multisets it
# contains is FINITE, KNOWN, and computable without looking at any search output.
# That makes a membership test possible which is strictly stronger than
# recanonicalising each row: a row either lies in the enumerated orbit or it is a
# new class, and the test needs no reference to previously observed data.
#
# verify_219.py answers "how many classes are in the local survivor files".
# This answers "is every row we have ever seen, from any source, in THE class" and
# "how much of the class have we seen".
import sys, itertools, collections, glob, os
sys.path.insert(0, 'intake')
import cog

CANON = (0, 0, 15, 74, 105, 438, 569, 647, 660, 671, 689)

C = cog.CO(7)
D = C.dist_matrix()
A = C.antidist_matrix(D)
maps = C.relabel_maps(with_reversal=True)

orbit = set()
for g in maps:
    orbit.add(tuple(sorted(g[v] for v in CANON)))

stab = len(maps) // len(orbit)
print("group order              %d" % len(maps))
print("orbit size (multisets)   %d" % len(orbit))
print("stabiliser order         %d" % stab)

# Every member must carry antisum 219.  If this ever fails the canonical
# representative is wrong, not the data.
off = sum(1 for M in orbit
          if sum(A[a][b] for a, b in itertools.combinations(M, 2)) != 219)
print("orbit members not at 219 %d   %s" % (off, "OK" if off == 0 else "*** BROKEN ***"))
print()

sources = [(fn, 'local') for fn in sorted(glob.glob('sweep_L5/low_*.txt'))]
sources += [(fn, 'kaggle') for fn in sorted(glob.glob('kaggle/rows/ANTISUM_219_shard*.txt'))]

seen = {}
rows = outside = 0
for fn, tag in sources:
    for line in open(fn):
        if not line.startswith('219,'):
            continue
        p = [int(x) for x in line.strip().split(',')]
        M = tuple(sorted(p[1:]))
        rows += 1
        if M not in orbit:
            outside += 1
            print("  *** NOT IN THE ORBIT -- A NEW CLASS *** %s  %s" % (fn, M))
        seen.setdefault(M, set()).add(tag + ':' + os.path.basename(fn))

print("rows checked             %d" % rows)
print("rows outside the orbit   %d   %s" % (outside, "OK" if outside == 0 else "*** NEWS ***"))
print("distinct multisets seen  %d of %d   (%.2f%%)" % (len(seen), len(orbit),
                                                        100.0 * len(seen) / len(orbit)))
print()
both = [M for M, s in seen.items()
        if any(t.startswith('local') for t in s) and any(t.startswith('kaggle') for t in s)]
print("multisets seen from BOTH local and Kaggle: %d" % len(both))
for M in both:
    print("   %s" % ' '.join(map(str, M)))
    for t in sorted(seen[M]):
        print("      %s" % t)
