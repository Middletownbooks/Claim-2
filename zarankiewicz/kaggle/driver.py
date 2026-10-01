# ---------------------------------------------------------------- configuration
MODE     = os.environ.get("ZMODE", "calibrate")   # calibrate | sweep
M        = int(os.environ.get("ZM", "11"))
N        = int(os.environ.get("ZN", "7"))
LEVEL    = int(os.environ.get("ZLEVEL", "5"))     # 5, not 4 -- see the note below
NSHARDS  = int(os.environ.get("ZNSHARDS", "2400"))
FIRST    = int(os.environ.get("ZFIRST", "0"))
COUNT    = int(os.environ.get("ZCOUNT", "1000000"))
THREADS  = int(os.environ.get("ZTHREADS", "0")) or (os.cpu_count() or 1)
WALL     = float(os.environ.get("ZWALL", "39600"))     # 11 h, inside the 12 h cap
TOP_RUNG = 223                                         # B[11]; parity makes rungs odd
OUT      = pathlib.Path(os.environ.get("ZOUT", "/kaggle/working/zout"))
PREV     = os.environ.get("ZPREV", "/kaggle/input")

# LEVEL 5, NOT 4.  At level 4 a single prefix can be a twenty-minute
# single-threaded subtree, so every shard ends with a tail the other cores sit
# out: measured at 1.88 and then 1.00 of 4 cores.  At level 5 the same work used
# 3.84.  The restructure is gated -- the level-5 units under level-4 shard 0
# reproduce its level counts, its leaf count and its antisum histogram exactly.

# THE REFERENCE NUMBERS, from the session that produced this bundle.  COMPARE,
# do not assume: the same container gave 7.65 s on the gate when fresh and
# 10.38 s four hours later, and its sweep rate fell 31% over that life and
# recovered fully on restart.  A rate is a property of a host AND of when you
# asked it, which is why this script measures rather than trusts.
# THE REFERENCE IS A RANGE, NOT A NUMBER, and that is the single most useful
# thing this bundle carries.  The same gate on the same account's containers has
# been measured at 6.47, 7.65 and 10.38 seconds -- a 1.60x spread on bit-identical
# work, with the slow figure coming from a container that had been up four hours.
# Its sweep rate over that same life fell 31% and recovered fully on restart.
#
# So a Kaggle gate time is interpretable only against the RANGE: it tells you
# which end of this account's own spread the host resembles, and nothing finer.
# Comparing it to a single number would say "Kaggle is 1.6x faster/slower" when
# the truth is that this account's own machines differ by that much.
REF = {
    "gate_off_s": {"fast": 6.47, "mid": 7.65, "slow": 10.38},
    "gate_on_s": {"fast": 4.97, "slow": 8.06},
    # measured on the SLOW (10.38 s) container, so these are the pessimistic end
    "quantum_nodes_per_core_s": {1: 1924549, 2: 1873640, 3: 1742353, 4: 1821979},
    "quantum_measured_on_gate_s": 10.38,
    "sweep_fresh": 1825602,
    "sweep_aged": 1250483,
    "tree_nodes": 1.0510e13,        # rel SE 4.39%
    "budget_core_hours": 2880,      # P-43(A): 4 cores x 30 days, fixed in advance
}
GATE = {"": [1, 13, 377, 29099, 801503, 14623179, 809438],
        "24": [1, 12, 329, 25346, 615817, 9827953, 809438]}
GATE_HIST = {"79": 809438}
# 384 is the calibration quantum the REF numbers were measured on.  ZQUANTUM
# lowers it for a smoke test: the thread curve stays meaningful but the absolute
# rates stop being comparable to REF, so the script says so when it is not 384.
QUANTUM = int(os.environ.get("ZQUANTUM", "384"))


def sh(cmd, **kw):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, **kw)


def probe():
    print("=== environment ===")
    print("python     :", sys.version.split()[0])
    print("cpus       :", os.cpu_count())
    cc = None
    for c in ("cc", "gcc", "clang"):
        r = sh("%s --version" % c)
        if r.returncode == 0:
            cc = c
            print("compiler   : %s -> %s" % (c, r.stdout.splitlines()[0]))
            break
    if not cc:
        print("compiler   : NONE FOUND.  apt-get -qq install -y build-essential")
    for label, path, key in (("memory     ", "/proc/meminfo", "MemTotal"),):
        try:
            v = [l for l in open(path) if l.startswith(key)][0].split()[1]
            print("%s: %d MB" % (label, int(v) // 1024))
        except Exception:
            pass
    try:
        print("cpu model  :", [l for l in open("/proc/cpuinfo") if "model name" in l][0]
              .split(":")[1].strip())
    except Exception:
        pass
    # A noexec mount is the one plausible blocker and is cheaper to test than to
    # look up: a binary can be written and still not be allowed to run.
    workdir = None
    for d in ("/kaggle/working", "/tmp", os.getcwd()):
        try:
            q = pathlib.Path(d) / ".exectest.sh"
            q.write_text("#!/bin/sh\necho ok\n")
            q.chmod(0o755)
            r = sh(str(q))
            ok = (r.returncode == 0 and r.stdout.strip() == "ok")
            print("exec from  : %-18s %s" % (d, "YES" if ok else "NO (%s)"
                  % (r.stderr.strip()[:60] or "rc=%d" % r.returncode)))
            q.unlink(missing_ok=True)
            if ok and workdir is None:
                workdir = pathlib.Path(d)
        except Exception as e:
            print("exec from  : %-18s NO (%s)" % (d, e))
    print("free disk  :", shutil.disk_usage("/").free // (1 << 30), "GB on /")
    return cc, workdir


def build(cc, wd):
    bd = wd / "zbuild"
    bd.mkdir(parents=True, exist_ok=True)
    for name, text in SOURCES.items():
        (bd / name).write_text(text)
    flags = "-O3 -funroll-loops -std=gnu11"
    r = sh("%s %s -march=native -o zsearch search.c cog.c -lpthread" % (cc, flags), cwd=bd)
    if r.returncode != 0:
        print("-march=native failed, retrying without it")
        r = sh("%s %s -o zsearch search.c cog.c -lpthread" % (cc, flags), cwd=bd)
    if r.returncode != 0:
        print(r.stderr[-2000:])
        sys.exit("BUILD FAILED")
    print("built %s  (source digest %s)" % (bd / "zsearch", SRC_DIGEST))
    return bd / "zsearch"


def gate(exe, repeats=3, label="gate"):
    print("=== %s: the exact (7,7) level counts, or we stop ===" % label)
    best = {}
    for thm7, want in GATE.items():
        el = []
        for _ in range(repeats):
            r = sh("%s -m 7 -n 7 %s" % (exe, ("-thm7 " + thm7) if thm7 else ""))
            if r.returncode != 0:
                print(r.stderr[-1000:])
                sys.exit("%s: the binary failed to run" % label)
            d = json.loads(r.stdout)
            if d["level_counts"] != want:
                sys.exit("%s FAILED: %s != %s -- nothing this binary prints can be trusted"
                         % (label, d["level_counts"], want))
            if thm7 == "" and d.get("antisum_histogram") != GATE_HIST:
                sys.exit("%s FAILED on the histogram: %s != %s"
                         % (label, d.get("antisum_histogram"), GATE_HIST))
            el.append(d["elapsed_s"])
        best[thm7 or "off"] = min(el)
        band = REF["gate_off_s"] if thm7 == "" else REF["gate_on_s"]
        lo, hi = min(band.values()), max(band.values())
        b = min(el)
        where = ("FASTER than anything measured there" if b < lo else
                 "SLOWER than anything measured there" if b > hi else
                 "inside the range measured there")
        print("  thm7=%-3s counts+histogram exact; %s s; best %.2f against %.2f-%.2f -> %s"
              % (thm7 or "off", ["%.2f" % x for x in el], b, lo, hi, where))
    print("  %s passed" % label)
    return best


def frontier(exe, wd, level):
    f = wd / ("frontier_m%d_L%d.txt" % (M, level))
    if f.exists() and f.stat().st_size > 0:
        print("frontier already present: %s (%d prefixes)" % (f, sum(1 for _ in open(f))))
        return f
    r = sh("%s -m %d -n %d -d %d -dump %s" % (exe, M, N, level, f))
    if r.returncode != 0:
        print(r.stderr[-1000:])
        sys.exit("frontier dump failed")
    d = json.loads(r.stdout)
    print("frontier: %d prefixes at level %d in %.1f s, counts to L %s"
          % (sum(1 for _ in open(f)), level, d["elapsed_s"], d["level_counts"][:level]))
    return f


def quantum_file(exe, wd):
    # A DETERMINISTIC work quantum: every (len/384)th level-5 prefix, first 384.
    # Reproducible from the frontier alone on any machine, which is the point --
    # the REF numbers above were measured on exactly this definition.
    f = frontier(exe, wd, 5)
    lines = open(f).read().split()
    stride = max(1, len(lines) // QUANTUM)
    q = wd / "quantum.txt"
    q.write_text("\n".join(lines[::stride][:QUANTUM]) + "\n")
    print("quantum: %d prefixes at stride %d of %d%s"
          % (QUANTUM, stride, len(lines),
             "" if QUANTUM == 384 else "   <-- NOT 384, so the REF comparison below is void"))
    return q


def calibrate(exe, wd):
    g = gate(exe)
    q = quantum_file(exe, wd)
    print()
    print("=== the same work at 1..%d threads, sequential, nothing else running ===" % THREADS)
    rows, nodes0 = {}, None
    for T in ([t for t in (1, 2, 3, 4, 8, 16) if t <= THREADS] or [THREADS]):
        r = sh("%s -m %d -n %d -startfile %s -threads %d" % (exe, M, N, q, T))
        d = json.loads(r.stdout)
        if d["aborted"]:
            sys.exit("the quantum aborted; it must complete")
        if nodes0 is None:
            nodes0 = d["total_nodes"]
        if d["total_nodes"] != nodes0:
            sys.exit("the quantum is not fixed: %d != %d" % (d["total_nodes"], nodes0))
        rows[T] = d
        ref = REF["quantum_nodes_per_core_s"].get(T) if QUANTUM == 384 else None
        # that reference was taken on the SLOW container; a fast one should beat it
        print("  T=%-2d wall %7.1f s  core %7.1f s  %.2f of %d cores  %8.0f nodes/core-s%s"
              % (T, d["elapsed_s"], d["core_seconds"], d["core_seconds"] / d["elapsed_s"], T,
                 d["nodes_per_core_s"],
                 "   reference %d -> %.2fx" % (ref, d["nodes_per_core_s"] / ref) if ref else ""))
    best = max(rows, key=lambda T: rows[T]["total_nodes"] / rows[T]["elapsed_s"])
    per = rows[best]["nodes_per_core_s"]
    agg = rows[best]["total_nodes"] / rows[best]["elapsed_s"]
    ch = REF["tree_nodes"] / per / 3600
    print()
    print("=== what this host means for the sweep ===")
    if QUANTUM != 384:
        print("  (ZQUANTUM=%d, not the reference 384: treat the rate as indicative only)" % QUANTUM)
    print("  best aggregate at T=%d: %.3e nodes/s, %d nodes/core-s" % (best, agg, per))
    print("  the (11,7) tree is %.4e nodes (rel SE 4.39%%)" % REF["tree_nodes"])
    print("  -> %.0f core-hours against P-43(A)'s %d: margin %.2fx"
          % (ch, REF["budget_core_hours"], REF["budget_core_hours"] / ch))
    print("  -> %.1f days of wall clock at T=%d" % (ch / best / 24, best))
    print("  -> %.0f sessions of 12 h x %d cores" % (ch / (12 * best), best))
    print()
    print("  TWO CAVEATS, NEITHER BOILERPLATE.")
    print("  (1) The rate fell 31%% over one container's four-hour life there (%d ->"
          % REF["sweep_fresh"])
    print("      %d nodes/core-s) and recovered fully on restart.  If that happens"
          % REF["sweep_aged"])
    print("      inside a 12-hour session, the session count above is optimistic by the")
    print("      same factor.  Run ZMODE=sweep and watch the per-shard rate -- it flags")
    print("      its own drift at 0.9x of the first shard.")
    print("  (2) The quantum reference was measured on the SLOWEST of three observed")
    print("      containers (gate 10.38 s, against 6.47 s on the fastest).  A ratio")
    print("      against it is therefore flattering by up to 1.6x.  What is NOT")
    print("      host-dependent is the core-hour figure above divided by THIS host's")
    print("      own measured rate, which is what the margin uses.")
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / "calibration.json"
    out.write_text(json.dumps(dict(
        src_digest=SRC_DIGEST, cpus=os.cpu_count(), gate_s=g,
        quantum_prefixes=QUANTUM, quantum_nodes=nodes0,
        curve={str(T): dict(wall_s=rows[T]["elapsed_s"], core_s=rows[T]["core_seconds"],
                            nodes_per_core_s=rows[T]["nodes_per_core_s"]) for T in rows},
        best_threads=best, best_nodes_per_core_s=per,
        sweep_core_hours=round(ch), margin=round(REF["budget_core_hours"] / ch, 2),
        reference=REF), indent=2) + "\n")
    print()
    print("wrote %s" % out)


def already_done():
    done = set()
    for root in (OUT, pathlib.Path(PREV)):
        if not root.exists():
            continue
        for q in root.rglob("sh_m%d_L%d_*of%d.json" % (M, LEVEL, NSHARDS)):
            try:
                d = json.loads(q.read_text())
                if d.get("complete"):
                    done.add(d["shard"])
            except Exception:
                pass
    return done


def run_shard(exe, f, i):
    # ATOMIC: the C writes low_i.txt.partial and it is renamed only after the
    # shard completes and its line count agrees with the histogram.  Writing the
    # final name directly already produced a committed half-file once.
    final = OUT / ("low_%d.txt" % i)
    part = OUT / ("low_%d.txt.partial" % i)
    t0 = time.time()
    r = sh("%s -m %d -n %d -startfile %s -shard %d -of %d -threads %d -survmax %d -survivors %s"
           % (exe, M, N, f, i, NSHARDS, THREADS, TOP_RUNG - 2, part))
    if r.returncode != 0:
        print(r.stderr[-1000:])
        sys.exit("shard %d failed" % i)
    d = json.loads(r.stdout)
    if d["aborted"]:
        part.unlink(missing_ok=True)
        sys.exit("shard %d aborted; its counts would be invalid" % i)
    hist = {int(k): v for k, v in d["antisum_histogram"].items()}
    if sum(hist.values()) != d["leaves"]:
        sys.exit("histogram does not sum to the leaf count")
    nlow = sum(v for k, v in hist.items() if k <= TOP_RUNG - 2)
    got = sum(1 for _ in open(part)) if part.exists() else 0
    if got != nlow:
        sys.exit("survivor file disagrees with the histogram: %d != %d" % (got, nlow))
    if nlow:
        part.replace(final)
    else:
        part.unlink(missing_ok=True)
    rec = dict(shard=i, of=NSHARDS, m=M, n=N, level=LEVEL, complete=True,
               src_digest=SRC_DIGEST, prefixes_done=d["prefixes_done"],
               level_counts=d["level_counts"], total_nodes=d["total_nodes"],
               leaves=d["leaves"], elapsed_s=round(d["elapsed_s"], 2),
               core_seconds=round(d["core_seconds"], 2),
               nodes_per_core_s=d["nodes_per_core_s"], threads=d["threads"],
               antisum_histogram={str(k): v for k, v in sorted(hist.items())},
               below_top_rung=nlow, wall_s=round(time.time() - t0, 2))
    # Written LAST: the presence of sh_*.json is what certifies the shard.
    (OUT / ("sh_m%d_L%d_%dof%d.json" % (M, LEVEL, i, NSHARDS))).write_text(json.dumps(rec) + "\n")
    return rec


def sweep(exe, wd):
    gate(exe)
    f = frontier(exe, wd, LEVEL)
    OUT.mkdir(parents=True, exist_ok=True)
    done = already_done()
    print("=== shards: %d total, %d already complete, this session takes %d from %d ==="
          % (NSHARDS, len(done), COUNT, FIRST))
    t0, first_rate, lowest = time.time(), None, None
    for i in range(FIRST, min(FIRST + COUNT, NSHARDS)):
        if i in done:
            continue
        if time.time() - t0 > WALL:
            print("wall budget reached before shard %d" % i)
            break
        rec = run_shard(exe, f, i)
        if first_rate is None:
            first_rate = rec["nodes_per_core_s"]
        drift = rec["nodes_per_core_s"] / first_rate
        h = {int(k): v for k, v in rec["antisum_histogram"].items()}
        deep = min(h) if h else None
        if deep is not None and (lowest is None or deep < lowest):
            lowest = deep
        print("  shard %4d: %13d nodes, %9d leaves, %5d below %d, lowest antisum %s, "
              "%7.1f s, %.2f of %d cores, %8.0f nodes/core-s (%.2fx the first)%s"
              % (i, rec["total_nodes"], rec["leaves"], rec["below_top_rung"], TOP_RUNG,
                 deep, rec["elapsed_s"], rec["core_seconds"] / rec["elapsed_s"], THREADS,
                 rec["nodes_per_core_s"], drift,
                 "   <-- RATE FALLING" if drift < 0.9 else ""), flush=True)
    print()
    gate(exe, repeats=1, label="gate again, to expose intra-session drift")
    print("=== session done; %d shard files in %s ; lowest antisum seen %s ==="
          % (len(list(OUT.glob("sh_*.json"))), OUT, lowest))


def main():
    cc, wd = probe()
    if not cc:
        sys.exit("no compiler")
    if wd is None:
        sys.exit("no filesystem on this host will execute a freshly built binary")
    exe = build(cc, wd)
    print()
    if MODE == "calibrate":
        calibrate(exe, wd)
    elif MODE == "sweep":
        sweep(exe, wd)
    else:
        sys.exit("ZMODE must be calibrate or sweep")


if __name__ == "__main__":
    main()
