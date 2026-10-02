import sys, itertools, collections
sys.path.insert(0, 'intake')
import cog

C = cog.CO(7)
D = C.dist_matrix()
A = C.antidist_matrix(D)
maps = C.relabel_maps(with_reversal=True)

rows = []
import glob
for fn in sorted(glob.glob('sweep_L5/low_*.txt')):
    for line in open(fn):
        line = line.strip()
        if not line.startswith('219,'): continue
        parts = [int(x) for x in line.split(',')]
        rows.append((fn, parts[0], parts[1:]))

print("rows claiming 219:", len(rows))
classes = collections.Counter()
bad = []
for fn, claimed, M in rows:
    s = sum(A[a][b] for a, b in itertools.combinations(M, 2))
    if s != claimed:
        bad.append((fn, claimed, s, M))
    classes[C.class_canon(tuple(M), maps=maps)] += 1
    if len(M) != 11:
        bad.append((fn, 'size', len(M), M))

print("antisum mismatches:", len(bad))
for b in bad: print("  MISMATCH", b)
print("distinct isomorphism classes:", len(classes))
for k, v in classes.items():
    rep = k
    mult = collections.Counter(rep)
    rep_mult = {x: c for x, c in mult.items() if c > 1}
    print("  class size %2d  canon=%s  repeated vertices=%s" % (v, rep, rep_mult or 'none (a true set)'))
