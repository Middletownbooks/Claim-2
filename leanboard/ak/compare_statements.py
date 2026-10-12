"""Arm AK: the textual half of the statement audit VibeMathed names as missing.

The comparator design is: comparator/Challenge*.lean state each theorem against Mathlib
alone with a placeholder proof; comparator/Solution.lean restates them and delegates to
the Zeta23 library. A promotion needs the comparator tool (kernel) to confirm the
statements coincide. This script confirms the TEXTUAL half -- that the statement source
is identical -- which is checkable without a Lean toolchain.

Usage: python3 compare_statements.py [path/to/zeta-23-lean]   (default: the v1.0 checkout)
"""
import re, sys, pathlib

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1
                    else "/home/user/anthropics/zeta-23-lean")

def strip(txt):
    return re.sub(r"--.*", "", re.sub(r"/-.*?-/", "", txt, flags=re.S))

def theorems(rel):
    """name -> statement text (between the name and the proof marker), whitespace-normalised."""
    txt = strip((ROOT / rel).read_text())
    return {m.group(1): re.sub(r"\s+", " ", m.group(2)).strip()
            for m in re.finditer(r"^\s*theorem\s+(\w+)\s*(.*?)(?::=\s*by\b|:=)",
                                 txt, flags=re.S | re.M)}

def definitions(rel, names):
    txt = strip((ROOT / rel).read_text())
    out = {}
    for m in re.finditer(r"^\s*(?:noncomputable\s+)?def\s+(\w+)\s*(.*?):=\s*(.*?)$", txt, flags=re.M):
        if m.group(1) in names:
            out[m.group(1)] = re.sub(r"\s+", " ", f"{m.group(2)}:={m.group(3)}").strip()
    return out

COUNTING = {"IsNontrivialZero", "zeroMult", "zerosIn", "Ncount", "Ndist",
            "N0", "N0star", "N0simple", "Nsimple"}
fails = []

ch, so = theorems("comparator/Challenge.lean"), theorems("comparator/Solution.lean")
shared = sorted(set(ch) & set(so))
print(f"Challenge statements: {len(ch)}   Solution statements: {len(so)}   shared: {len(shared)}")
print(f"only in Solution (expected: the constant identity): {sorted(set(so) - set(ch))}")
if set(ch) - set(so):
    fails.append(f"challenge statements with no solution: {sorted(set(ch) - set(so))}")
bad = [n for n in shared if ch[n] != so[n]]
print(f"statements identical: {len(shared) - len(bad)}/{len(shared)}")
for n in bad:
    fails.append(f"statement mismatch: {n}")
    print(f"  MISMATCH {n}\n    challenge: {ch[n][:160]}\n    solution : {so[n][:160]}")

a = definitions("comparator/ChallengeDeps.lean", COUNTING)
b = definitions("Zeta23/Statement.lean", COUNTING)
shared_d = sorted(set(a) & set(b))
print(f"\ncounting functions compared: {len(shared_d)}")
for n in shared_d:
    ok = a[n] == b[n]
    print(f"  {'MATCH ' if ok else 'DIFFER'}  {n}")
    if not ok:
        fails.append(f"counting-function mismatch: {n}")
missing = COUNTING - set(shared_d)
if missing:
    fails.append(f"counting functions not found in both files: {sorted(missing)}")

print("\nNOT CHECKED HERE (needs a Lean toolchain): that the delegations typecheck, that the"
      "\ncounting functions agree DEFINITIONALLY rather than textually, and the axiom set.")
print(f"\n{'FAIL: ' + '; '.join(fails) if fails else 'PASS: textual statement audit clean'}")
raise SystemExit(1 if fails else 0)
