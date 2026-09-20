#!/usr/bin/env python3
"""Verify every matrix shipped in github.com/bbeartheancient/hoa64.

Run against a clone:  python3 verify_matrices.py /path/to/hoa64/matrices

Checks, per file: shape is (n,n) for the n in the filename, every entry is +-1, and
H H^T = n I EXACTLY in integer arithmetic. That is the definition of a Hadamard
matrix, so a pass here settles the mathematical content of the claim independently of
any announcement, benchmark page or press report.

Result when this was run (2026-09-20, commit d825201): 13/13 pass.
"""
import glob, gzip, os, re, sys
import numpy as np

d = sys.argv[1] if len(sys.argv) > 1 else "matrices"
files = sorted(glob.glob(os.path.join(d, "*.csv.gz")),
               key=lambda f: int(re.search(r"(\d+)", os.path.basename(f)).group(1)))
if not files:
    sys.exit(f"no *.csv.gz under {d}")

print(f"{'order':>6} {'shape':>12} {'entries +-1':>12} {'H H^T = nI':>12}")
ok = []
for f in files:
    n = int(re.search(r"(\d+)", os.path.basename(f)).group(1))
    with gzip.open(f, "rt") as fh:
        rows = [r for r in (line.strip() for line in fh) if r]
    M = np.array([[int(x) for x in r.split(",")] for r in rows], dtype=np.int64)
    pm1 = bool(np.all(np.abs(M) == 1))
    had = M.shape == (n, n) and bool(np.array_equal(M @ M.T, n * np.eye(n, dtype=np.int64)))
    print(f"{n:>6} {str(M.shape):>12} {str(pm1):>12} {str(had):>12}")
    if pm1 and had:
        ok.append(n)
print(f"\nverified Hadamard: {len(ok)}/{len(files)} -> {ok}")
