#!/usr/bin/env python3
"""Stage A of the Theorem 6(c) sweep: every (11,7)-set of antisum 219 or 221 has
antisum + 2*tau >= 225.  See THEOREM6C_SWEEP.md.

The completed top-221 sweep wrote every such set, up to relabelling, to
sweep_L5/low_*.txt -- 53,514,110 rows: 976 at antisum 219 and 53,513,134 at 221.
For each row `c/ptcheck -need` decides only whether tau >= ceil((225 - T)/2),
stopping as soon as that is certain (tau >= 2 at T = 221: two non-pseudo-tight
(4,7)-subsets with no pair in common is already enough; tau >= 3 at T = 219), and
prints every row for which it is NOT.  Writes stageA.json.

    python3 stageA.py            # ~6 core-minutes
"""
import glob, json, os, pathlib, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

HERE = pathlib.Path(__file__).resolve().parent
EXE = HERE / "c" / "ptcheck"
FILES = sorted(glob.glob(str(HERE / "sweep_L5" / "low_*.txt")),
               key=lambda p: int(re.search(r"low_(\d+)", p).group(1)))
JOBS = int(os.environ.get("JOBS", "0")) or (os.cpu_count() or 1)


def one(path):
    with open(path) as f:
        r = subprocess.run([str(EXE), "-need"], stdin=f, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("ptcheck failed on %s: %s" % (path, r.stderr[-300:]))
    m = re.search(r"rows (\d+)\s+fails (\d+)\s+pt_calls (\d+)\s+target (\d+)\s+rows by K:(.*)", r.stderr)
    byk = {k: int(v) for k, v in re.findall(r"K(\d+):(\d+)", m.group(5))}
    return dict(file=os.path.basename(path), rows=int(m.group(1)), fails=int(m.group(2)),
                pt_calls=int(m.group(3)), target=int(m.group(4)), by_K=byk,
                failing_rows=r.stdout.splitlines())


if __name__ == "__main__":
    assert len(FILES) == 2400, len(FILES)
    with ThreadPoolExecutor(JOBS) as ex:
        res = list(ex.map(one, FILES))
    byk = {}
    for r in res:
        for k, v in r["by_K"].items():
            byk[k] = byk.get(k, 0) + v
    out = dict(files=len(res), rows=sum(r["rows"] for r in res),
               fails=sum(r["fails"] for r in res), pt_calls=sum(r["pt_calls"] for r in res),
               target=225, rows_by_tau_needed={str(k): v for k, v in sorted(byk.items())},
               failing_rows=[x for r in res for x in r["failing_rows"]])
    (HERE / "stageA.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k != "failing_rows"}, indent=1))
    print("failing rows:", len(out["failing_rows"]))
