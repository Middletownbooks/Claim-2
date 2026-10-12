import numpy as np, sympy
X = []
for l in open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), 'core.txt')):
    if '=' in l and l.split('=',1)[0].strip() in 'ABCD':
        X.append([1 if c=='+' else -1 for c in l.split('=',1)[1].strip()])
X = np.array(X, dtype=np.int64); m = X.shape[1]
p, nprime = 11, 52
assert nprime*p == m
QR = sorted({(x*x) % p for x in range(1, p)})
NQR = sorted(set(range(1, p)) - set(QR))
print(f'G = Z_{nprime} x Z_{p}   (CRT on Z_{m})')
print(f'quadratic residues mod {p}: {QR}   non-residues: {NQR}')
print(f'|QR| = (p-1)/2 = {len(QR)}')

# CRT index: i in Z_572  <->  (i mod 52, i mod 11)
idx = np.zeros((nprime, p), dtype=np.int64)
for i in range(m):
    idx[i % nprime, i % p] = i

print('\n--- Paley-coset form: on each Z_11 coset, values are (alpha at 0, u+w on QR, -u+w on NQR) ---')
tot_tw = tot_const = 0
Kk = []; Nm = Np = 0
for k in range(4):
    tw = const = bad = 0
    for g in range(nprime):
        row = X[k][idx[g]]
        a = row[0]
        vq = set(row[QR].tolist()); vn = set(row[NQR].tolist())
        if len(vq) != 1 or len(vn) != 1:
            bad += 1; continue
        q, n = vq.pop(), vn.pop()
        u = (q - n)//2; w = (q + n)//2
        if u != 0 and w == 0:   tw += 1
        elif u == 0 and w != 0:
            const += 1
            if w == -a: Nm += 1
            else:       Np += 1
        else: bad += 1
    Kk.append(const); tot_tw += tw; tot_const += const
    print(f'  block {"ABCD"[k]}: twisted cosets {tw:3d}, constant cosets {const:2d}, violations {bad}')
print(f'\n  TOTAL: twisted {tot_tw}, constant K = {tot_const}  (K_k = {Kk})')
print(f'  N- = {Nm}, N+ = {Np}')
print(f'  norm identity (p+1)K - 4N- = 4n\' - 4b  ->  {12*tot_const - 4*Nm} == {4*nprime - 4} : '
      f'{12*tot_const - 4*Nm == 4*nprime - 4}')

print('\n--- the multiplier group, decomposed ---')
U = sorted({pow(9, e, m) for e in range(50)})
# the QR-on-Z_p part: mu = 1 mod 52, mu = square mod 11
qr_part = sorted(u for u in range(m) if u % nprime == 1 and u % p in QR and sympy.gcd(u, m) == 1)
# the Z_52 multiplier part: mu = 1 mod 11
g52 = sorted(u for u in U if u % p == 1)
print(f'  U = <9> mod {m}, |U| = {len(U)}')
print(f'  elements with mu = 1 mod 52 (pure Paley/QR part): {[u for u in U if u % nprime == 1]}')
print(f'    their residues mod 11: {sorted(u % p for u in U if u % nprime == 1)}  == QR? '
      f'{sorted(u % p for u in U if u % nprime == 1) == [1]+QR[:0] or set(u % p for u in U if u % nprime==1) <= set(QR)}')
print(f'  elements with mu = 1 mod 11 (pure Z_52 multiplier part): {g52}')
print(f'    their residues mod 52: {sorted(u % nprime for u in g52)}')
print(f'  |QR part| = {len([u for u in U if u % nprime == 1])},  |Z52 part| = {len(g52)},  product = '
      f'{len([u for u in U if u % nprime == 1]) * len(g52)}  vs |U| = {len(U)}')
print(f'  is 29 in the Z_52 part?  29 mod 52 in {sorted(u % nprime for u in g52)} : '
      f'{29 in [u % nprime for u in g52]}')
