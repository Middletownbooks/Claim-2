"""Score task-2 step D: inter-rater agreement on transformation labels.

Rater A order: Q1..Q8 = C1 C2 C3 C4 C5 K1 K2 K3
Rater B order: Q1..Q8 = K2 C3 K1 C5 C2 K3 C4 C1
"""
import sys, re, json, random
ORDER = {"A": ["C1","C2","C3","C4","C5","K1","K2","K3"],
         "B": ["K2","C3","K1","C5","C2","K3","C4","C1"]}
SCORED = ["C1","C2","C3","C4","C5"]          # C4 is the same-board control
CONTROL = "C4"
NAMES = {c["id"]: c["name"] for c in json.load(open("cases.json"))}

def parse(txt, who):
    out = {}
    for m in re.finditer(r"^\s*Q(\d)\s*[:.]\s*(\d)\s*\|\s*(\d)", txt, re.M):
        q, lab, conf = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if 1 <= q <= 8 and 1 <= lab <= 6:
            out[ORDER[who][q-1]] = (lab, conf)
    return out

def kappa(pairs):
    n = len(pairs)
    if not n: return float("nan"), float("nan")
    agree = sum(1 for a,b in pairs if a==b)/n
    la = [a for a,_ in pairs]; lb = [b for _,b in pairs]
    cats = set(la)|set(lb)
    pe = sum((la.count(c)/n)*(lb.count(c)/n) for c in cats)
    return agree, (float("nan") if pe==1 else (agree-pe)/(1-pe))

def boot(pairs, n=20000, seed=1):
    random.seed(seed); ks=[]
    for _ in range(n):
        s=[random.choice(pairs) for _ in pairs]
        _,k=kappa(s)
        if k==k: ks.append(k)
    ks.sort()
    return (ks[int(.025*len(ks))], ks[int(.975*len(ks))]) if ks else (float("nan"),)*2

A = parse(open(sys.argv[1]).read(), "A")
B = parse(open(sys.argv[2]).read(), "B")
print("parsed: rater A %d items, rater B %d items" % (len(A), len(B)))
print("\n case                          A            B        agree")
for cid in SCORED + ["K1","K2","K3"]:
    a, b = A.get(cid), B.get(cid)
    tag = " (control)" if cid==CONTROL else (" (calib)" if cid.startswith("K") else "")
    print(" %-12s%-14s %-12s %-12s %s" % (cid, NAMES[cid][:13]+tag,
          "%d (c%d)"%a if a else "-", "%d (c%d)"%b if b else "-",
          "yes" if a and b and a[0]==b[0] else "no"))

sp = [(A[c][0], B[c][0]) for c in SCORED if c in A and c in B]
kp = [(A[c][0], B[c][0]) for c in ["K1","K2","K3"] if c in A and c in B]
ag, k = kappa(sp)
print("\nSCORED CASES (n=%d): raw agreement %.2f, Cohen kappa %.3f" % (len(sp), ag, k))
if len(sp) >= 3:
    lo, hi = boot(sp)
    print("   bootstrap 95%% interval on kappa: [%.2f, %.2f]" % (lo, hi))
agk, kk = kappa(kp)
print("CALIBRATION CASES (n=%d): raw agreement %.2f, kappa %.3f" % (len(kp), agk, kk))

print("\n--- pre-registered predictions ---")
print("D1 kappa < 0.6 on scored cases : %s (kappa = %.3f)" %
      ("HELD" if k==k and k<0.6 else "FAILED" if k==k else "UNDETERMINED", k))
labs = [l for c in SCORED for r in (A,B) if c in r for l in [r[c][0]]]
from collections import Counter
cnt = Counter(labs)
modal = cnt.most_common(1)[0] if cnt else (None,0)
print("D2 NONE modal among scored     : %s (label counts %s)" %
      ("HELD" if modal[0]==6 else "FAILED", dict(sorted(cnt.items()))))
ctrl = [r[CONTROL][0] for r in (A,B) if CONTROL in r]
print("D3 >=1 rater over-fits control : %s (labels on the control: %s)" %
      ("HELD" if any(l!=6 for l in ctrl) else "FAILED", ctrl))
t35 = sum(cnt.get(x,0) for x in (3,5))
print("D4 transformations 3 and 5 rare: %s (%d of %d scored labels)" %
      ("HELD" if t35 <= 1 else "FAILED", t35, len(labs)))
