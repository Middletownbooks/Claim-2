# ---------------------------------------------------------------- configuration
# PASTE-INTO-A-NOTEBOOK PATH.  Paste this whole script into one cell, change the
# one word below, run the cell.  No second cell, no %env, no shell prefix.
#
#   "smoke"      ~2 min   every step the long run does, on 1/24th of the work
#   "calibrate"  ~20 min  the real measurement; the discounted core-hour figure
#                         at the end is the answer you came for
#   "sweep"      hours    production shards -- what this is set to
#
# IT IS SET TO "sweep" because this account's hosts are already calibrated and the
# only thing left to do with them is shards.  That is not a shortcut past the
# checks: sweep runs the same gate first and stops dead if the (7,7) level counts
# or histogram are off by one node, re-runs the gate at the end to expose
# intra-session slowdown, and flags per-shard rate drift as it goes.  Change the
# word to "smoke" if you want the two-minute version on a host you do not trust.
#
# PRECEDENCE: an explicit ZMODE in the environment wins outright, so running the
# file as `!ZMODE=calibrate python kaggle_shard.py` ignores RUN entirely and the
# two ways of driving this script cannot contradict each other.
RUN = "sweep"

# PARALLEL SESSIONS: change ONE digit per session.  Set SLOT to 0, 1, 2, 3, 4 in
# the five sessions and change nothing else.
SLOT = 0

# THE BLOCK EACH SLOT OWNS, first and last shard inclusive.  THIS TABLE IS THE
# ONLY THING THAT CHANGES BETWEEN ROUNDS, and the end of every session prints the
# exact line to paste back here, so no resume dataset is ever needed.
#
# WHY A TABLE AND NOT A DIVISION.  An earlier version derived each slot's slice by
# dividing SLOT_FROM..SLOT_UPTO into NSLOTS parts.  That is correct for a first
# round and wrong for a second: moving SLOT_FROM up to resume re-divides the whole
# range, so slot 0 resumed where it stopped while slot 1 jumped from 1151 to 1401
# and the shards between were simply skipped.  Nothing was corrupted -- shard i is
# the same subtree in every session because NSHARDS is fixed and goes to the C as
# -of -- but the coverage grew holes that no file recorded.  An explicit block per
# slot cannot do that: each slot's range is written down, and the ranges are
# checked below for overlap and for straying into the container's half.
#
# Set an entry to None when its block is finished, and give that slot a new one.
BLOCKS = [
    (828,  1119),    # slot 0
    (1154, 1439),    # slot 1
    (1461, 1759),    # slot 2
    (1781, 2079),    # slot 3
    (2109, 2399),    # slot 4
]

# THE CONTAINER OWNS 0..799 AND KAGGLE OWNS 800..2399.  The container works
# upward from shard 0, so a Kaggle block reaching below KAGGLE_FROM would have
# both machines redo the same subtrees while the shard count advanced twice as
# fast -- duplicated effort that looks exactly like progress.  The cut is set so
# that Kaggle stopping ENTIRELY still leaves the container finishing inside the
# one-month bar.
KAGGLE_FROM = 800

_PRESETS = {
    "smoke":     {"ZMODE": "calibrate", "ZQUANTUM": "16"},
    "calibrate": {"ZMODE": "calibrate"},
    "sweep":     {"ZMODE": "sweep"},
}
if "ZMODE" not in os.environ:
    if RUN not in _PRESETS:
        raise SystemExit("RUN must be one of: %s" % ", ".join(sorted(_PRESETS)))
    os.environ.update(_PRESETS[RUN])

MODE     = os.environ.get("ZMODE", "calibrate")   # calibrate | sweep
M        = int(os.environ.get("ZM", "11"))
N        = int(os.environ.get("ZN", "7"))
LEVEL    = int(os.environ.get("ZLEVEL", "5"))     # 5, not 4 -- see the note below
NSHARDS  = int(os.environ.get("ZNSHARDS", "2400"))
FIRST    = int(os.environ.get("ZFIRST", "0"))
COUNT    = int(os.environ.get("ZCOUNT", "1000000"))

# CHECK THE WHOLE TABLE, not just this slot's row.  The point of writing the
# blocks down is that they can be checked; a table that is never validated is
# just five chances to make the mistake the table was meant to prevent.  These
# run in every session, so whichever slot you launch first catches a bad edit.
def _check_blocks():
    seen = []
    for k, b in enumerate(BLOCKS):
        if b is None:
            continue
        lo, hi = b
        if not (isinstance(lo, int) and isinstance(hi, int)):
            raise SystemExit("BLOCKS[%d]: want (first, last) integers, got %r" % (k, b))
        if hi < lo:
            raise SystemExit("BLOCKS[%d] = (%d, %d): last is below first" % (k, lo, hi))
        if lo < KAGGLE_FROM:
            raise SystemExit(
                "BLOCKS[%d] starts at %d, below KAGGLE_FROM=%d -- the container owns "
                "0..%d and both machines would redo the same shards"
                % (k, lo, KAGGLE_FROM, KAGGLE_FROM - 1))
        if hi >= NSHARDS:
            raise SystemExit("BLOCKS[%d] ends at %d, past the last shard %d"
                             % (k, hi, NSHARDS - 1))
        for j, lo2, hi2 in seen:
            if lo <= hi2 and lo2 <= hi:
                raise SystemExit("BLOCKS[%d] (%d..%d) overlaps BLOCKS[%d] (%d..%d)"
                                 % (k, lo, hi, j, lo2, hi2))
        seen.append((k, lo, hi))
    return seen


if "ZFIRST" not in os.environ and "ZCOUNT" not in os.environ:
    _live = _check_blocks()
    if not (0 <= SLOT < len(BLOCKS)):
        raise SystemExit("SLOT must be 0..%d, got %r" % (len(BLOCKS) - 1, SLOT))
    _mine = BLOCKS[SLOT]
    if _mine is None:
        raise SystemExit("BLOCKS[%d] is None: this slot's block is finished.  Give it a "
                         "new range before running, or change SLOT." % SLOT)
    FIRST, _last = _mine
    COUNT = _last - FIRST + 1
    _total = sum(hi - lo + 1 for _, lo, hi in _live)
    print("SLOT %d takes shards %d..%d (%d shards); the %d live blocks cover %d of %d"
          % (SLOT, FIRST, _last, COUNT, len(_live), _total, NSHARDS), flush=True)
    print("blocks checked: no overlap, none below %d, none past %d"
          % (KAGGLE_FROM, NSHARDS - 1), flush=True)

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
# THE REFERENCE IS A RANGE, NOT A NUMBER, and that is the most useful thing this
# bundle carries.  The same gate on this account's containers has measured 6.47,
# 6.75, 7.65 and 10.38 seconds on bit-identical work -- a 1.60x spread, the slow
# end from a container up four hours, whose sweep rate over that life fell 31%
# and recovered fully on restart.  A Kaggle gate time tells you which END of that
# spread a host resembles and nothing finer.
#
# AND THE QUANTUM OVER-READS SUSTAINED THROUGHPUT.  Measured on the same
# container each time: on one it matched the sweep to 0.2% (1,821,979 against
# 1,825,602); on another it read 1.20x high (2,146,567 against ~1,783,000).  The
# quantum is 384 prefixes and 5.5e8 nodes; a production shard is 2,774 and
# 4.2e9.  A short fresh-cache measurement flatters itself, and by an amount that
# is not stable between hosts.  So the calibration reports BOTH the raw figure
# and one discounted by PRODUCTION_DISCOUNT, and the discounted one is what to
# plan sessions against.
REF = {
    "gate_off_s": {"fast": 6.47, "obs2": 6.75, "mid": 7.65, "slow": 10.38},
    "gate_on_s": {"fast": 4.85, "obs2": 4.92, "slow": 8.06},
    # the quantum at T threads, observed on two containers
    "quantum_nodes_per_core_s": {1: 2190225, 2: 2181870, 3: 2156826, 4: 2146567},
    "quantum_range_T4": {"low": 1821979, "high": 2146567},
    "quantum_measured_on_gate_s": 6.75,
    "sweep_fresh": 1825602,
    "sweep_aged": 1250483,
    # GATE TIME AS A PROXY FOR SUSTAINED RATE.  The product (gate_off_s x sustained
    # nodes/core-s) is roughly constant across containers, which makes the gate -- a
    # fixed single-threaded workload long enough not to be dominated by startup --
    # the one thing a 2-minute smoke run measures honestly.  Two clean pairs:
    #   aged  10.38 s x 1,250,483 = 1.298e7
    #   fresh  7.65 s x 1,825,602 = 1.397e7
    # agreeing to 7%.  A third, 6.59 s x 1,676,447 = 1.105e7, is 15-21% low but its
    # gate ran while the sweep held all four cores, so it is not a clean refutation.
    # Treat the proxy as good to about +/-20%, no better.
    "gate_rate_product": {"lo": 1.298e7, "hi": 1.397e7},
    "gate_rate_product_uncertainty": 0.20,
    "tree_nodes": 1.0510e13,        # rel SE 4.39%
    "budget_core_hours": 2880,      # P-43(A): 4 cores x 30 days, fixed in advance
}
PRODUCTION_DISCOUNT = 1.20
GATE = {"": [1, 13, 377, 29099, 801503, 14623179, 809438],
        "24": [1, 12, 329, 25346, 615817, 9827953, 809438]}
GATE_HIST = {"79": 809438}
# 384 is the calibration quantum the REF numbers were measured on.  ZQUANTUM
# lowers it for a smoke test: the thread curve stays meaningful but the absolute
# rates stop being comparable to REF, so the script says so when it is not 384.
QUANTUM = int(os.environ.get("ZQUANTUM", "384"))


# LINE-BUFFER STDOUT.  A notebook cell shows nothing until the buffer flushes,
# so a twenty-minute calibration looked like a hung cell -- found by running this
# very script and watching an empty output pane while four cores were busy.
try:
    sys.stdout.reconfigure(line_buffering=True)
except Exception:
    pass


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
        # ANNOUNCE BEFORE BLOCKING.  subprocess output is captured, so without this
        # the cell prints nothing for the length of `repeats` full (7,7) searches.
        print("  thm7=%-4s running %d repeats, ~%ds each ..."
              % (thm7 or "off", repeats, 10 if thm7 == "" else 8), flush=True)
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
        # T=1 is the longest single wait of the whole script; say so before it starts.
        print("  T=%-2d running ..." % T, flush=True)
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
    # THE TWO OPTIMA CAN DIFFER, and on an SMT host they do.  `best` maximises
    # aggregate throughput, which minimises WALL time.  `cheap` maximises per-core
    # rate, which minimises CORE-HOURS -- the quantity P-43(A) budgets.  Where the
    # per-core rate is flat in T these coincide and the distinction is invisible;
    # where extra threads are SMT siblings returning ~16% each, they do not.
    cheap = max(rows, key=lambda T: rows[T]["nodes_per_core_s"])
    # BUT DISTINGUISH TWO CAUSES, because they call for opposite actions and the
    # naive test (cheap != best) cannot tell them apart.  If the run could not get
    # the cores it asked for -- core_seconds/elapsed well below T -- then something
    # ELSE was running and the curve measures contention, not the host.  Caught by
    # running this on a container where the production sweep held all four cores:
    # it reported "does not scale flat in threads" at 1.72 of 4 cores, which is a
    # busy machine, not an SMT one.  A genuine SMT or bandwidth ceiling shows high
    # utilisation AND low yield: Kaggle gave 3.75 of 4 cores with per-core down 41%.
    util = rows[best]["core_seconds"] / rows[best]["elapsed_s"] / best
    if cheap != best and util < 0.85:
        print()
        print("  *** THIS HOST WAS BUSY DURING THE RUN ***")
        print("  at T=%d it got only %.2f of %d cores (%.0f%% of what it asked for),"
              % (best, rows[best]["core_seconds"] / rows[best]["elapsed_s"], best, 100 * util))
        print("  so the thread curve above measures contention, not this host.  Every")
        print("  rate here is a floor.  Re-run with nothing else on the machine.")
    elif cheap != best:
        ch_b = REF["tree_nodes"] / rows[best]["nodes_per_core_s"] / 3600
        ch_c = REF["tree_nodes"] / rows[cheap]["nodes_per_core_s"] / 3600
        w_b = REF["tree_nodes"] / (rows[best]["total_nodes"] / rows[best]["elapsed_s"]) / 3600
        w_c = REF["tree_nodes"] / (rows[cheap]["total_nodes"] / rows[cheap]["elapsed_s"]) / 3600
        print()
        print("  *** THIS HOST DOES NOT SCALE FLAT IN THREADS ***")
        print("  per-core rate peaks at T=%d (%d nodes/core-s) but aggregate peaks at T=%d."
              % (cheap, rows[cheap]["nodes_per_core_s"], best))
        print("  Extra threads past T=%d return only %.0f%% each, the signature of SMT"
              % (cheap, 100 * (rows[best]["total_nodes"] / rows[best]["elapsed_s"]
                               / (rows[cheap]["total_nodes"] / rows[cheap]["elapsed_s"]) - 1)
                 / max(1, best - cheap)))
        print("  siblings or a saturated memory path rather than %d independent cores." % best)
        print("    T=%-2d  %6.0f core-hours, %5.0f wall-hours   <- cheapest in core-hours"
              % (cheap, ch_c, w_c))
        print("    T=%-2d  %6.0f core-hours, %5.0f wall-hours   <- fastest in wall time"
              % (best, ch_b, w_b))
        print("  Pick by which budget binds.  P-43(A) is in CORE-hours.")
    per = rows[best]["nodes_per_core_s"]
    agg = rows[best]["total_nodes"] / rows[best]["elapsed_s"]
    ch = REF["tree_nodes"] / per / 3600
    print()
    print("=== what this host means for the sweep ===")
    if QUANTUM != 384:
        print("  (ZQUANTUM=%d, not the reference 384: treat the rate as indicative only)" % QUANTUM)
    print("  best aggregate at T=%d: %.3e nodes/s, %d nodes/core-s" % (best, agg, per))
    print("  the (11,7) tree is %.4e nodes (rel SE 4.39%%)" % REF["tree_nodes"])
    chd = ch * PRODUCTION_DISCOUNT
    bud = REF["budget_core_hours"]
    if QUANTUM != 384:
        # A SMOKE RUN CANNOT PRODUCE A BUDGET VERDICT, and must not print one.  At
        # ZQUANTUM=16 each thread gets four prefixes, so spawn/join and load
        # imbalance dominate: a smoke run on an IDLE host measured 1.63 of 4 cores
        # against 3.96 in production.  The quantum rate is then an artefact of the
        # quantum size, and running it through the budget printed "OVER BUDGET" for
        # a host the gate says is comfortably inside it.  An earlier version of this
        # script did exactly that.
        glo = REF["gate_rate_product"]["lo"] / g["off"]
        ghi = REF["gate_rate_product"]["hi"] / g["off"]
        u = REF["gate_rate_product_uncertainty"]
        clo = REF["tree_nodes"] / (ghi * (1 + u)) / 3600
        chi = REF["tree_nodes"] / (glo * (1 - u)) / 3600
        print("  NO BUDGET VERDICT FROM A SMOKE RUN.  ZQUANTUM=%d, not 384: the thread" % QUANTUM)
        print("  curve above is dominated by spawn/join and imbalance, not by this host,")
        print("  and the core-hour figure it implies would be meaningless.  Re-run with")
        print("  RUN=\"calibrate\" (or ZQUANTUM=384) for the measurement.")
        print()
        print("  What this run DOES measure honestly is the gate: %.2f s single-threaded" % g["off"])
        print("  on fixed work.  Against the gate/rate product observed elsewhere that")
        print("  predicts sustained %.2fe6 - %.2fe6 nodes/core-s, so roughly" % (glo / 1e6, ghi / 1e6))
        print("    %.0f - %.0f core-hours against P-43(A)'s %d  (+/-20%%, a PREDICTION," % (clo, chi, bud))
        print("     not a measurement -- the full calibrate is what tests it)")
    else:
        print("  raw, as the quantum measures it:")
        print("    %.0f core-hours against P-43(A)'s %d: margin %.2fx ; %.1f days at T=%d ; %.0f sessions of 12 h"
              % (ch, bud, bud / ch, ch / best / 24, best, ch / (12 * best)))
        print("  DISCOUNTED %.2fx for sustained production, which is what to plan against:"
              % PRODUCTION_DISCOUNT)
        print("    %.0f core-hours, margin %.2fx ; %.1f days at T=%d ; %.0f sessions of 12 h"
              % (chd, bud / chd, chd / best / 24, best, chd / (12 * best)))
        if bud / chd < 1.0:
            print("    *** OVER BUDGET on the discounted figure ***")
    print()
    print("  TWO CAVEATS, NEITHER BOILERPLATE.")
    print("  (1) The rate fell 31%% over one container's four-hour life there (%d ->"
          % REF["sweep_fresh"])
    print("      %d nodes/core-s) and recovered fully on restart.  If that happens"
          % REF["sweep_aged"])
    print("      inside a 12-hour session, the session count above is optimistic by the")
    print("      same factor.  Run ZMODE=sweep and watch the per-shard rate -- it flags")
    print("      its own drift at 0.9x of the first shard.")
    print("  (2) The quantum OVER-READS sustained production: on one container it")
    print("      matched the sweep to 0.2%, on another it read 1.20x high.  Hence the")
    print("      %s  The ratios against REF are informative about"
          % ("discounted line above." if QUANTUM == 384 else "1.20x discount, applied once a real quantum runs."))
    print("      the host, but the core-hour figure uses THIS host's own rate, which")
    print("      is the part that does not depend on which of my containers I happened")
    print("      to measure.")
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / "calibration.json"
    out.write_text(json.dumps(dict(
        src_digest=SRC_DIGEST, cpus=os.cpu_count(), gate_s=g,
        quantum_prefixes=QUANTUM, quantum_nodes=nodes0,
        curve={str(T): dict(wall_s=rows[T]["elapsed_s"], core_s=rows[T]["core_seconds"],
                            nodes_per_core_s=rows[T]["nodes_per_core_s"]) for T in rows},
        best_threads=best, best_nodes_per_core_s=per,
        sweep_core_hours=round(ch), margin=round(REF["budget_core_hours"] / ch, 2),
        production_discount=PRODUCTION_DISCOUNT,
        sweep_core_hours_discounted=round(ch * PRODUCTION_DISCOUNT),
        margin_discounted=round(REF["budget_core_hours"] / (ch * PRODUCTION_DISCOUNT), 2),
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

    # THE NEXT ROUND'S LINE, computed from the certificates this session wrote.
    # This is what replaces a resume dataset: nothing has to be carried forward
    # except one tuple, and the session that did the work is the thing that
    # reports it, so the number cannot be a guess about what got done.
    last = min(FIRST + COUNT, NSHARDS) - 1
    done2 = already_done()
    mine = [i for i in range(FIRST, last + 1) if i in done2]
    todo = [i for i in range(FIRST, last + 1) if i not in done2]
    print()
    print("=== NEXT ROUND: paste this into BLOCKS[%d] ===" % SLOT)
    if not todo:
        print("    None,            # %d..%d COMPLETE (%d shards) -- give slot %d a new block"
              % (FIRST, last, len(mine), SLOT))
    else:
        print("    (%d, %d),    # was (%d, %d); %d done, %d left"
              % (todo[0], last, FIRST, last, len(mine), len(todo)))
        # CONTIGUOUS OR NOT.  If the remaining shards are one run then resuming at
        # todo[0] is exact.  If they are not, resuming there redoes the completed
        # ones above the gap -- waste, not error, since a redone shard writes the
        # same certificate -- but it is said out loud, because silently redoing
        # work is precisely what the old slot arithmetic did.
        runs = []
        for i in todo:
            if runs and i == runs[-1][1] + 1:
                runs[-1][1] = i
            else:
                runs.append([i, i])
        if len(runs) > 1:
            print("    *** NOT a clean prefix: the %d remaining shards are %d separate runs,"
                  % (len(todo), len(runs)))
            print("        %s" % ", ".join("%d..%d" % (a, b) for a, b in runs[:6]))
            print("        so resuming at %d redoes %d already-certified shards.  Use the"
                  % (todo[0], (last - todo[0] + 1) - len(todo)))
            print("        line above anyway unless that waste matters; a redone shard")
            print("        writes the same certificate and cannot corrupt anything.")
    if mine:
        el = time.time() - t0
        print("    %d shards in %.1f h = %.1f min/shard; the remaining %d need about %.1f more sessions"
              % (len(mine), el / 3600, el / 60 / max(1, len(mine)), len(todo),
                 (len(todo) * (el / max(1, len(mine)))) / WALL))


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
