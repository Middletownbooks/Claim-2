#!/usr/bin/env python3
"""planted-truth step 5 applied to claims_status.json: change the last digit of
each quote once and check that row's status flips to FINDING.
Run from emitall-pilot/. Needs BOOTLOOPS=<path to a bootloops checkout>."""
import copy, json, os, subprocess, sys, tempfile
EM = os.path.join(os.environ.get("BOOTLOOPS", "/home/user/bootloops-ai/bootloops"), "tools/emitall/run.py")
spec = json.load(open("claims_status.json"))

def run(s):
    with tempfile.TemporaryDirectory() as t:
        sp, rp = os.path.join(os.getcwd(), "_mut_spec.json"), os.path.join(t, "r.json")
        json.dump(s, open(sp, "w"))
        try:
            r = subprocess.run([sys.executable, EM, sp, "--out", rp, "--quiet"], capture_output=True, text=True)
        finally:
            os.remove(sp)
        if r.returncode == 2 or not os.path.exists(rp):
            raise SystemExit("emitall failed: " + r.stderr[:300])
        return {(c["section"], c["label"]): c["status"] for c in json.load(open(rp))["table"]}

def mutate(q):
    for i in range(len(q) - 1, -1, -1):
        if q[i].isdigit():
            return q[:i] + str((int(q[i]) + 1) % 10) + q[i + 1:]
    return q + "1"

base = run(spec)
print("baseline: %d rows, %d already FINDING" % (len(base), sum(v == "FINDING" for v in base.values())))
fired = missed = already = 0
for i, c in enumerate(spec["claims"]):
    key = (c["section"], c["label"])
    s = copy.deepcopy(spec); s["claims"][i]["quoted"] = mutate(c["quoted"])
    after = run(s)[key]
    if base[key] == "FINDING":
        already += 1; print("ALREADY FINDING (mutation uninformative):", c["label"])
    elif after == "FINDING":
        fired += 1
    else:
        missed += 1; print("NOT CAUGHT:", c["label"], c["quoted"], "->", s["claims"][i]["quoted"], "status", after)
print("clean rows mutated: %d; comparator fired %d; did not fire %d; uninformative %d" % (fired + missed, fired, missed, already))
