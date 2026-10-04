#!/usr/bin/env python3
"""One-call heartbeat: commit certified shards, push, print one compact line.

Minimal-token mode (operator instruction, Oct 4): no rankings, no doc edits, no
narrative.  Run this BEFORE relaunching, so the 219 verifiers run on an idle
machine (rule 1).  Detail lives in INSTRUMENTS.md / BENCHMARK.md and is not to
be read routinely until the weekly limit resets.
"""
import json, os, glob, subprocess, sys

Z = os.path.dirname(os.path.abspath(__file__))
R = os.path.dirname(Z)
L = os.path.join(Z, "sweep_L5")

def sh(cmd, cwd=R):
    p = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout.strip(), p.stderr.strip()

# shards certified but not yet committed
_, out, _ = sh("git status --porcelain zarankiewicz/sweep_L5")
new = sorted(int(l.split("sh_")[1].split(".json")[0])
             for l in out.splitlines() if l.startswith("?? ") and "/sh_" in l)

running = sh("pgrep -x zsearch")[0] == 0
done = len(glob.glob(os.path.join(L, "sh_*.json")))
# A group banked while the sweep still runs is a PARTIAL WINDOW, not a cycle
# figure (rule 4).  Label it so, in the line and in the commit message.
kind = "partial window" if running else "cycle"

line = []
if new:
    ds = [json.load(open(os.path.join(L, "sh_%d.json" % i))) for i in new]
    bad = [d["shard"] for d in ds if not d.get("complete")]
    r = [d["nodes_per_core_s"] for d in ds]
    tn = sum(d["total_nodes"] for d in ds)
    cs = sum(d["core_seconds"] for d in ds)
    ws = sum(d["wall_s"] for d in ds)
    spread = (max(r) / min(r) - 1) * 100
    mean = tn / cs
    line.append("shards %d-%d (%d, %s)  mean %d  spread %.2f%%  %.1f s/shard"
                % (new[0], new[-1], len(new), kind, mean, spread, ws / len(new)))
    if spread > 10:
        line.append("*** SPREAD OVER 10%% -- CYCLE VOID, do not quote the mean ***")
    if bad:
        line.append("*** INCOMPLETE CERTIFICATES: %s ***" % bad)

    # 219 bin
    idx = os.path.join(L, "ANTISUM_219.txt")
    _, live, _ = sh("grep -h '^219,' sweep_L5/low_*.txt | sort", cwd=Z)
    old = open(idx).read() if os.path.exists(idx) else ""
    grew = (live + "\n" if live else "") != old
    nrows = len(live.splitlines())
    if grew:
        open(idx, "w").write(live + "\n" if live else "")
        line.append("219 GREW to %d rows" % nrows)
    else:
        line.append("219 unchanged at %d rows" % nrows)

    # lowest antisum anywhere in this cycle
    low = min(int(k) for d in ds for k in d["antisum_histogram"])
    line.append("lowest antisum this cycle %d" % low)
    if low <= 217:
        line.append("*** ANTISUM %d -- STOP AND FLAG TO THE OPERATOR ***" % low)

    sh("./zarankiewicz/sweep_commit.sh > /dev/null 2>&1")
    if grew:
        sh("git add zarankiewicz/sweep_L5/ANTISUM_219.txt")
        for v in ("verify_219.py", "verify_219_orbit.py"):
            c, o, _ = sh("python3 %s" % v, cwd=Z)
            keep = [x.strip() for x in o.splitlines()
                    if any(k in x for k in ("mismatch", "classes", "outside the orbit",
                                            "distinct multisets", "rows checked",
                                            "rows claiming"))]
            line.append("%s: %s" % (v, "; ".join(keep)))

    msg = ("Sweep: shards %d-%d, %s mean %d, spread %.2f%%, 219 at %d rows\n\n"
           "Minimal-token mode: figures only, no analysis until the weekly reset.\n"
           "%s\n"
           "Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>\n"
           "Claude-Session: https://claude.ai/code/session_0184ooepmZGQd7zabkbmXLiR\n"
           % (new[0], new[-1], kind, mean, spread, nrows,
              "This group was banked while the sweep was still running, so it is a\n"
              "PARTIAL WINDOW over the shards named and not a cycle figure; it does not\n"
              "belong in the cycle table.\n" if running else
              "Whole cycle: these were every shard the cycle certified.\n"))
    p = subprocess.run(["git", "commit", "-F", "-"], cwd=R, input=msg,
                       capture_output=True, text=True)
    if p.returncode:
        line.append("*** COMMIT FAILED: %s %s ***" % (p.stdout[-300:], p.stderr[-300:]))
    else:
        sh("git fetch origin claude/zarankiewicz-k711 > /dev/null 2>&1")
        behind = sh("git rev-list --count HEAD..FETCH_HEAD")[1]
        if behind not in ("0", ""):
            line.append("*** REMOTE AHEAD by %s -- merge, never rebase ***" % behind)
        else:
            c, o, e = sh("git push -u origin zara:claude/zarankiewicz-k711")
            line.append("pushed" if c == 0 else "*** PUSH FAILED: %s ***" % e[-300:])
else:
    line.append("no uncommitted shards")

_, head, _ = sh("git log --oneline -1")
_, up, _ = sh("uptime")
print("\n".join(line))
print("%d/2400 certified (%.4f%%)   %s   %s"
      % (done, done / 2400 * 100, "SWEEP RUNNING" if running else "IDLE - RELAUNCH", head))
print(up)
