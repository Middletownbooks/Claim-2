#!/usr/bin/env python3
"""Independent verification of H(2292) -- bordered Goethals-Seidel, b=1.

Self-contained: no dependency on the Cooperative-AI-Defense tree. Builds the
2292x2292 matrix from the four core sequences in core.txt plus the stated
border, and certifies H H^T = 2292 I over the integers.

Construction as stated by its authors:
    bordered Goethals-Seidel, b=1, border S, T in H(4), corner = -S Sigma^T T / 4

Measured here: Sigma = 2I (integral), the corner is itself an H(4), and the
cross condition Z x_k = -2 y_k holds exactly with the border ROWS taken from T
and the border COLUMNS from S.

Positive controls: the FINDING-100 search-free family at v = 15, 39, 63, 159
is NOT reproduced here (it needs paley_core from the other repo); instead the
control is structural -- the same assembler is run on a deliberately corrupted
core, which must fail.

Usage:  python3 verify_2292.py [core.txt]
"""
import sys, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

S = np.array([[1, 1, 1, 1], [1, 1, -1, -1], [1, -1, 1, -1], [1, -1, -1, 1]], dtype=np.int64)
T = np.array([[1, 1, 1, -1], [1, 1, -1, 1], [1, -1, 1, 1], [-1, 1, 1, 1]], dtype=np.int64)
Z = np.array([[-1, -1, -1, -1], [-1, -1, 1, 1], [-1, 1, -1, 1], [1, -1, -1, 1]], dtype=np.int64)


def load_core(path):
    rows = []
    for line in open(path):
        if '=' in line and line.split('=', 1)[0].strip() in 'ABCD':
            rows.append([1 if c == '+' else -1 for c in line.split('=', 1)[1].strip()])
    X = np.array(rows, dtype=np.int64)
    assert X.shape[0] == 4, f'expected 4 blocks, got {X.shape[0]}'
    return X


def law(X):
    """(Sum_k PAF_k(0), distinct values of Sum_k PAF_k(t) for t != 0, row sums)."""
    m = X.shape[1]
    tot = np.zeros(m, dtype=np.int64)
    for k in range(4):
        F = np.fft.rfft(X[k].astype(float), n=m)
        tot += np.rint(np.fft.irfft(F * np.conj(F), n=m)).astype(np.int64)
    return int(tot[0]), sorted(set(tot[1:].tolist())), X.sum(axis=1).tolist()


def circ(x):
    m = len(x)
    return x[(np.arange(m)[:, None] - np.arange(m)[None, :]) % m]


def gs(X):
    """Standard Goethals-Seidel array on four circulants, order 4m."""
    m = X.shape[1]
    R = np.zeros((m, m), dtype=np.int64)
    R[np.arange(m), (-np.arange(m)) % m] = 1
    A, B, C, D = [circ(X[k]) for k in range(4)]
    z = lambda M: M @ R
    return np.block([[A,     z(B),   z(C),   z(D)],
                     [-z(B),  A,     z(D.T), -z(C.T)],
                     [-z(C), -z(D.T), A,      z(B.T)],
                     [-z(D),  z(C.T), -z(B.T), A]])


def hadamard(X):
    """Bordered GS: border rows from T, border columns from S, corner Z."""
    m = X.shape[1]
    assert np.array_equal((Z @ T.T).T, -2 * S), 'stated border fails the cross condition'
    Xb = np.repeat(T, m, axis=0)                                     # 4m x 4
    Yb = np.concatenate([np.repeat(S[k][:, None], m, axis=1) for k in range(4)], axis=1)
    return np.block([[Z, Yb], [Xb, gs(X)]])


def certify(H, N):
    return (H.shape == (N, N)
            and set(np.unique(H).tolist()) <= {-1, 1}
            and np.array_equal(H @ H.T, N * np.eye(N, dtype=np.int64)))


def report(X, tag):
    m = X.shape[1]; v = m + 1; N = 4 * v
    p0, nz, rs = law(X)
    print(f'{tag}: m={m} v={v} N={N}')
    print(f'  Sum_k PAF_k(0)     = {p0}   (4m = {4*m})')
    print(f'  Sum_k PAF_k(t!=0)  = {nz}   constant: {len(nz) == 1}')
    print(f'  row sums           = {rs}   sum of squares = {int((X.sum(axis=1)**2).sum())}')
    H = hadamard(X)
    G = H @ H.T
    off = int(np.abs(G - np.diag(np.diag(G))).max())
    print(f'  entries in +-1     = {set(np.unique(H).tolist()) <= {-1, 1}}')
    print(f'  max |off-diagonal| = {off}')
    print(f'  diagonal values    = {sorted(set(np.diag(G).tolist()))}')
    ok = certify(H, N)
    print(f'  >>> H H^T = {N} I   :  {ok}\n')
    return ok


if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'core.txt')
    X = load_core(path)

    print('=== IDENTITY CHECK on the law ===')
    m = X.shape[1]
    p0, nz, _ = law(X)
    lhs = p0 + (m - 1) * nz[0] if len(nz) == 1 else None
    print(f'  Sum_t Sum_k PAF_k(t) = {lhs}  must equal Sum_k a_k^2 = '
          f'{int((X.sum(axis=1)**2).sum())}  -> '
          f'{lhs == int((X.sum(axis=1)**2).sum())}\n')

    print('=== THE CLAIM ===')
    ok = report(X, 'H(2292)')

    print('=== NEGATIVE CONTROL: one sign flipped, must fail ===')
    Y = X.copy(); Y[0, 0] *= -1
    bad = report(Y, 'corrupted core')

    print('VERDICT:', 'VERIFIED' if (ok and not bad) else 'FAILED')
    sys.exit(0 if (ok and not bad) else 1)
