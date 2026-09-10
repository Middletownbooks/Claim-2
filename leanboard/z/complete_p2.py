"""Complete p2 test for the final conj2 survivors.

Bounded (y,z) search cannot clear these -- the lone 10^9 survivor needed
y = 3,178,714 -- so use the divisor formulation instead:

    a = 4x(4yz - z - 1) - 4yz + 1,  u = 4x - 1
    =>  a + u = z * W   with   W = 4uy - u - 1

So for each u = 3, 7, 11, ... factor N = a+u, and for each divisor z of N set
W = N/z and test whether y = (W + u + 1) / (4u) is a positive integer.
This is COMPLETE for the u values scanned: it misses nothing at that x.
"""
import sys
from sympy import factorint, divisors

def p2_complete(a, UMAX=400):
    for x in range(1, UMAX + 1):
        u = 4 * x - 1
        N = a + u
        for z in divisors(N):
            W = N // z
            t = W + u + 1
            if t % (4 * u) == 0 and t // (4 * u) >= 1:
                return dict(x=x, y=t // (4 * u), z=z)
    return None

def verify(a, s):
    x, y, z = s['x'], s['y'], s['z']
    return 4 * x * (4 * y * z - z - 1) - 4 * y * z + 1 == a

if __name__ == '__main__':
    src = sys.argv[1]
    umax = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    vals = [int(l) for l in open(src) if l.strip()]
    print("complete p2 test on %d survivors, u = 4x-1 for x <= %d" % (len(vals), umax))
    left = []
    for i, a in enumerate(vals, 1):
        s = p2_complete(a, umax)
        if s is None:
            left.append(a)
        elif not verify(a, s):
            print("  !! witness failed verification for a=%d: %s" % (a, s))
            left.append(a)
        if i % 50 == 0:
            print("   %d/%d done, %d uncleared" % (i, len(vals), len(left)), flush=True)
    print("\nUNCLEARED after complete p2 (x <= %d): %d" % (umax, len(left)))
    for a in left[:40]:
        print("   a = %d   q = %d   q mod 6 = %d" % (a, (a - 1) // 4, ((a - 1) // 4) % 6))
    if left:
        open('conj2_uncleared.txt', 'w').write("\n".join(map(str, left)) + "\n")
