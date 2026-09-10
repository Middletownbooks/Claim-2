import sm2
from math import gcd
def odd_divs(n): return sorted(d for d in range(3,n+1) if n%d==0 and d%2==1)
def certified(r,q,L):
    b = sm2.crt(1,24,r%q,q)
    if b is None: return False
    a = 24*q//gcd(24,q)
    return sm2.egyptian_class(a,b,CLIM=L,ELIM=L) is not None
G,R = 24,[1]
for m in (5,7,11,13):
    G2 = G*m
    R = [x for r in R for s in range(m) for x in [sm2.crt(r,G,s,m)] if x is not None]
    G = G2
    qs = odd_divs(G)
    R = [r for r in R if not any(certified(r,q,60) for q in qs)]
print("i=4 at CLIM=60 :", len(R), flush=True)
for L in (200, 600):
    qs = odd_divs(G)
    R = [r for r in R if not any(certified(r,q,L) for q in qs)]
    print("i=4 at CLIM=%d: %d   (paper: 192)" % (L, len(R)), flush=True)
    if len(R) == 192: break
