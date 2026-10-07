/* search6c.c -- the sweep with Woodall's Theorem 6(c) as a node predicate.
 *
 * Same tree as search.c (staircase, prefix-minimality, stabiliser lex-min, all
 * unchanged), plus one thing: every node carries the family of its
 * non-pseudo-tight (4,7)-subsets and tau, the minimum number of pairs meeting all
 * of them.  Each such pair is drawn with at least dbar + 2 crossings in any good
 * drawing (THEOREM6C.md), and tau can only grow down a path of the tree, so every
 * leaf below a node has
 *
 *      crossings  >=  antisum(leaf) + 2*tau(node).
 *
 * A leaf is a candidate counterexample only if antisum + 2*tau <= TOP (223 for
 * K_{7,11}), so a node with tau = j only needs leaves of antisum <= TOP - 2j and
 * is cut by THAT top's staircase -- the same construction search.c uses.  Nodes
 * whose effective top falls below -tmin are cut outright; the default 219 is the
 * minimum antisum over (11,7)-sets proved by the completed sweep.
 *
 * Survivors are exactly the leaves with antisum + 2*tau <= TOP: the multisets
 * Theorem 6(c) does not settle.  Zero survivors over the whole tree means every
 * good drawing of K_{7,m} has at least TOP + 2 crossings.
 *
 * Three economies, none of which changes the survivor set:
 *  (1) LAZY.  A node's own non-PT sets (those containing its newest element) are
 *      computed only once it is known to have a child passing every cheap clause.
 *      A childless internal node cannot hold a survivor whatever its tau.
 *  (2) EARLY EXIT.  With budget allow = max j such that S <= staircase_j, the node
 *      dies at the first non-PT set when allow = 0, and as soon as no single pair
 *      meets all of them when allow = 1.
 *  (3) LANES.  Each pair's FORCED/POSSIBLE masks are spread into byte lanes once
 *      per path position, so a (4,7)-test is six ORs and a 7-variable CSP.
 * -check re-runs every PT verdict through the reference pt4() and aborts on any
 * disagreement.
 *
 *   ./zsearch6c -m 11 -n 7 -startfile F -shard s -of N -threads T -survivors out
 *   ./zsearch6c -m 7  -n 7 -tmin 79              # Woodall's K_{7,7}: 0 survivors
 *   ./zsearch6c -m 7  -n 7 -tmin 79 -top 81      # positive control: many survivors
 */
#define _POSIX_C_SOURCE 199309L
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <pthread.h>
#include "cog.h"
#include "pt.h"

#define MAXM 14
#define MAXTAU 40
#define MAXSETS 1024                         /* C(12,4) = 495 */

static int   BT[MAXTAU + 2][MAXM + 2];      /* BT[j][k]: staircase for top TOP - 2j */
static int   Mtarget, Depth = -1, TOP, TMIN = 219, TAUCAP, usept = 1, check = 0;
static FILE *dumpf = NULL, *survf = NULL;
static pthread_mutex_t survlock = PTHREAD_MUTEX_INITIALIZER;
#define HMAX 512
static int16_t *AD16;
static uint8_t PIDX[16][16];                 /* position pair -> bit in a 64-bit pair mask */
static int skiplev[MAXM + 2];                /* levels whose internal nodes defer their sets */
static int clamp = 0;
static int cachebits = 22;
static int eagerlev[MAXM + 2];                /* -eager L: test a level-L node's sets before building its row */                    /* -cache B: 2^B entries per thread (0 = off) */                         /* -clamp: also cut on a sub-multiset below its crossing number */
/* cr(K_{7,k}) for k <= 10: Kleitman (k <= 6), Woodall (7, 9), counting (8, 10).  All theorems. */
static const int CR7[11] = {0, 0, 0, 9, 18, 36, 54, 81, 108, 144, 180};

typedef struct {
    int16_t *rowv;
    int      ch[MAXM + 2];
    int32_t  co[MAXM + 2];
    uint64_t visited[MAXM + 2];               /* nodes entered (cheap clauses passed)  */
    uint64_t kept[MAXM + 2];                  /* nodes whose own 6(c) test passed      */
    uint64_t cut6c[MAXM + 2];                 /* nodes cut by the 6(c) term            */
    uint64_t taucount[MAXM + 2][MAXTAU + 2];  /* kept nodes by level and tau           */
    uint64_t hist[HMAX][MAXTAU + 2];          /* survivors by antisum and tau          */
    uint64_t ptcalls;
    uint64_t lf[MAXM + 2][MAXM + 2][3], lp[MAXM + 2][MAXM + 2][3];  /* lanes per position pair */
    uint16_t fam[MAXSETS];                    /* non-PT 4-subsets, as position masks   */
    int      famn[MAXM + 2];                  /* famn[k]: sets inside the first k positions */
    uint64_t common[MAXM + 2];                /* AND of the sets' pair masks (~0 if none) */
    int16_t  anti[1 << 12];                   /* -clamp: antisum of every subset of the computed positions */
    uint64_t *cache;                          /* direct-mapped PT verdicts, keyed by the sorted 4-multiset */
    uint64_t cachehits;
    long     prefixes_done;
    double   busy_s;
} W;

static double now(void)
{
    struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

static int tau_allow(int32_t S, int k)
{
    int j = -1;
    while (j + 1 <= TAUCAP && S <= BT[j + 1][k]) j++;
    return j;
}

static uint64_t setpairs(uint16_t s)
{
    int p[4], n = 0;
    for (int i = 0; i < 16 && n < 4; i++) if (s >> i & 1) p[n++] = i;
    uint64_t r = 0;
    for (int x = 0; x < 4; x++) for (int y = x + 1; y < 4; y++) r |= 1ULL << PIDX[p[x]][p[y]];
    return r;
}

static int pt_at(W *w, int a, int b, int c, int d)
{
    uint64_t fm[3], pm[3];
    for (int q = 0; q < 3; q++) {
        fm[q] = w->lf[a][b][q] | w->lf[a][c][q] << 1 | w->lf[a][d][q] << 2
              | w->lf[b][c][q] << 3 | w->lf[b][d][q] << 4 | w->lf[c][d][q] << 5;
        pm[q] = w->lp[a][b][q] | w->lp[a][c][q] << 1 | w->lp[a][d][q] << 2
              | w->lp[b][c][q] << 3 | w->lp[b][d][q] << 4 | w->lp[c][d][q] << 5;
    }
    w->ptcalls++;
    int r;
    uint64_t *slot = NULL, tag = 0;
    if (w->cache) {
        /* A verdict depends only on the multiset {ch[a],ch[b],ch[c],ch[d]} (checked over
         * 20,000 random multisets x 24 orders in ptcheck -selftest), so key on it sorted. */
        uint32_t q[4] = {(uint32_t)w->ch[a], (uint32_t)w->ch[b], (uint32_t)w->ch[c], (uint32_t)w->ch[d]};
        for (int i = 1; i < 4; i++) for (int j = i; j > 0 && q[j] < q[j - 1]; j--) { uint32_t t = q[j]; q[j] = q[j - 1]; q[j - 1] = t; }
        uint64_t key = ((uint64_t)q[0] << 30) | ((uint64_t)q[1] << 20) | ((uint64_t)q[2] << 10) | q[3];
        tag = (key << 2) | 2;                                  /* bit 1: occupied, bit 0: verdict */
        slot = &w->cache[(key * 0x9E3779B97F4A7C15ULL) >> (64 - cachebits)];
        if ((*slot & ~1ULL) == tag) { w->cachehits++; r = (int)(*slot & 1); goto have; }
    }
    r = pt4_lanes(fm, pm);
    if (slot) *slot = tag | (uint64_t)r;
have:
    if (check && r != pt4(w->ch[a], w->ch[b], w->ch[c], w->ch[d])) {
        fprintf(stderr, "pt mismatch at %d,%d,%d,%d\n", w->ch[a], w->ch[b], w->ch[c], w->ch[d]);
        exit(3);
    }
    return r;
}

/* The node is the prefix ch[0..k-1].  Positions below fdp already have their
 * non-PT sets on the stack (famn[fdp], common[fdp]); bring positions fdp..k-1 up
 * to date -- lanes first, then the sets containing each -- and return the node's
 * tau, or -1 if it exceeds the budget the node's antisum leaves (the node is cut).
 * full = 1 computes every set regardless of budget (used when seeding a prefix). */
static int node_family(W *w, int k, int32_t S, int full, int fdp)
{
    int allow = full ? TAUCAP : tau_allow(S, k);
    if (allow < 0) return -1;
    int n = w->famn[fdp];
    uint64_t common = w->common[fdp];
    for (int p = fdp; p < k; p++) {
        for (int i = 0; i < p; i++) {
            size_t key = (size_t)w->ch[i] * CO_NV + w->ch[p];
            pt_expand(PT_F[key], w->lf[i][p]);
            pt_expand(PT_P[key], w->lp[i][p]);
        }
        if (clamp) {
            /* Every sub-multiset T + {p} of k' stars is a good drawing of K_{7,k'}, so if its
             * antisum is below cr(K_{7,k'}) one of its pairs is drawn with >= dbar + 2
             * crossings: a set the transversal must meet, exactly like a non-PT 4-set.
             * Only used with TAUCAP = 0, where the first such set cuts the node. */
            int16_t rp[1 << 11];
            rp[0] = 0;
            w->anti[1 << p] = 0;
            for (int T = 1; T < (1 << p); T++) {
                int lb = __builtin_ctz(T);
                rp[T] = (int16_t)(rp[T & (T - 1)] + AD(w->ch[lb], w->ch[p]));
                int a = w->anti[T] + rp[T], sz = __builtin_popcount(T) + 1;
                w->anti[T | (1 << p)] = (int16_t)a;
                if (sz >= 3 && sz <= 10 && a < CR7[sz]) return -1;
            }
        }
        if (usept && p >= 3) {
            for (int a = 0; a < p; a++) for (int b = a + 1; b < p; b++) for (int c = b + 1; c < p; c++) {
                if (pt_at(w, a, b, c, p)) continue;
                uint16_t s = (uint16_t)((1u << a) | (1u << b) | (1u << c) | (1u << p));
                w->fam[n++] = s;
                common &= setpairs(s);
                if (!full && (allow == 0 || (allow == 1 && common == 0))) return -1;
            }
        }
        w->famn[p + 1] = n;
        w->common[p + 1] = common;
    }
    int tau;
    if (n == 0) tau = 0;
    else if (common) tau = 1;
    else {
        tau = 2;
        while (tau <= allow && !pt_feasible(w->fam, n, tau)) tau++;
    }
    return tau <= allow ? tau : -1;
}

static int prefix_ok(W *w, int k, int v, int32_t cv, int32_t *nc)
{
    const int16_t *Av = AD16 + (size_t)v * CO_NV;
    for (int i = 0; i < k; i++) {
        int32_t c2 = w->co[i] + Av[w->ch[i]];
        if (c2 > cv) return 0;
        if (nc) nc[i] = c2;
    }
    w->ch[k] = v;
    for (int g = 0; g < CO_nstab; g++) {                /* stabiliser lex-min */
        const uint16_t *gm = CO_stab[g];
        for (int i = 1; i <= k; i++) {
            int t = w->ch[i], gt = gm[t];
            if (gt < t) return 0;
            if (gt > t) break;
        }
    }
    return 1;
}

/* taup: a lower bound on this node's tau (exact for the first fdp positions);
 * fdp: how many positions of the path have their sets on the stack. */
static void rec(W *w, int k, int32_t S, int taup, int fdp)
{
    w->visited[k]++;
    if (k == Mtarget) {
        int tau = node_family(w, k, S, 0, fdp);
        if (tau < 0) { w->cut6c[k]++; return; }
        w->kept[k]++; w->taucount[k][tau]++;
        if (S >= 0 && S < HMAX) w->hist[S][tau]++;
        if (survf) {
            pthread_mutex_lock(&survlock);
            fprintf(survf, "%d", (int)S);
            for (int i = 0; i < k; i++) fprintf(survf, ",%d", w->ch[i]);
            fprintf(survf, " tau=%d t=%d\n", tau, w->famn[k]);
            pthread_mutex_unlock(&survlock);
        }
        return;
    }
    const int16_t *row = w->rowv + (size_t)k * CO_NV;
    int16_t *nrow = w->rowv + (size_t)(k + 1) * CO_NV;
    const int nv = CO_NV;

    if (Depth > 0 && k >= Depth) {
        int tau = node_family(w, k, S, 0, fdp);
        if (tau < 0) { w->cut6c[k]++; return; }
        w->kept[k]++; w->taucount[k][tau]++;
        if (dumpf) {
            pthread_mutex_lock(&survlock);
            for (int i = 0; i < k; i++) fprintf(dumpf, "%d%c", w->ch[i], i < k - 1 ? ',' : '\n');
            pthread_mutex_unlock(&survlock);
        }
        return;
    }

    int32_t maxco = 0;
    for (int i = 0; i < k; i++) if (w->co[i] > maxco) maxco = w->co[i];
    const int lo = (int)(S + maxco);
    int lim = BT[taup][k + 1];

    uint16_t cl[MAXNV];
    int ncl = 0;
    for (int v = 0; v < nv; v++) {
        const int r = row[v];
        if (r <= lim && r >= lo) cl[ncl++] = (uint16_t)v;
    }
    /* (1) lazy: is there any child at all? */
    int any = 0;
    for (int ci = 0; ci < ncl && !any; ci++) any = prefix_ok(w, k, cl[ci], row[cl[ci]] - S, NULL);
    if (!any) return;

    int tau = taup, fd = fdp;
    if (!skiplev[k]) {
        tau = node_family(w, k, S, 0, fdp);
        if (tau < 0) { w->cut6c[k]++; return; }
        w->kept[k]++; w->taucount[k][tau]++;
        fd = k;
        lim = BT[tau][k + 1];
    }

    for (int ci = 0; ci < ncl; ci++) {
        const int v = cl[ci];
        const int32_t nS = row[v];
        if (nS > lim) continue;
        const int32_t cv = nS - S;
        int32_t nc[MAXM + 2];
        if (!prefix_ok(w, k, v, cv, nc)) continue;
        nc[k] = cv;
        const int nk = k + 1;
        int ctau = tau, cfd = fd;
        if (eagerlev[nk] && nk < Mtarget) {
            /* (4) eager: with cached verdicts the child's own sets are cheaper than its row.
             * A cut child would have been cut (or found childless) in rec() anyway. */
            ctau = node_family(w, nk, nS, 0, fd);
            if (ctau < 0) { w->visited[nk]++; w->cut6c[nk]++; continue; }
            cfd = nk;
        }
        if (nk < Mtarget) {
            /* Exact shortcut: a child's candidates must satisfy nS + max(nc) <= row <= its
             * staircase, so if that window is already empty the child has no children and
             * rec() would return at once.  Count it and skip the 720-wide row. */
            int32_t mx = 0;
            for (int i = 0; i < nk; i++) if (nc[i] > mx) mx = nc[i];
            if (nS + mx > BT[ctau][nk + 1] && !(Depth > 0 && nk >= Depth)) { w->visited[nk]++; continue; }
            const int16_t *Av = AD16 + (size_t)v * nv;
            const int16_t cv16 = (int16_t)cv;
            for (int x = 0; x < nv; x++) nrow[x] = (int16_t)(row[x] + Av[x] + cv16);
        }
        int32_t save_co[MAXM + 2];
        memcpy(save_co, w->co, sizeof(w->co));
        memcpy(w->co, nc, sizeof(int32_t) * (size_t)nk);
        rec(w, nk, nS, ctau, cfd);
        memcpy(w->co, save_co, sizeof(w->co));
    }
}

static int parity_required(int k, int n)
{
    if (k % 2 == 0 || n % 2 == 0) return -1;
    return (k % 4 == 3 && n % 4 == 3) ? 1 : 0;
}

/* exactly search.c's staircase, for an arbitrary top */
static void staircase(int *B, int m, int n, int top)
{
    int t = top;
    int p = parity_required(m, n);
    while (p >= 0 && (t % 2) != p) t--;
    B[m] = t;
    for (int k = m; k > 2; k--) {
        int b = (B[k] * (k - 2)) / k;
        int pk = parity_required(k - 1, n);
        while (pk >= 0 && (b % 2) != pk) b--;
        B[k - 1] = b;
    }
    B[1] = 0; B[0] = 0;
}

static W *worker_new(void)
{
    W *w = calloc(1, sizeof(W));
    if (!w) { fprintf(stderr, "oom\n"); exit(1); }
    w->rowv = malloc((size_t)(MAXM + 2) * CO_NV * sizeof(int16_t));
    if (!w->rowv) { fprintf(stderr, "oom\n"); exit(1); }
    w->famn[0] = 0; w->common[0] = ~0ULL;
    if (cachebits > 0) {
        w->cache = calloc((size_t)1 << cachebits, sizeof(uint64_t));
        if (!w->cache) { fprintf(stderr, "oom (cache)\n"); exit(1); }
    }
    return w;
}

/* Seed at a prefix of length k: contributions, antisum, row, and the full family
 * of its first k-1 positions; *Sout is the prefix's antisum.  Returns tau of the
 * first k-1 positions (the parent's tau), or -1 if some ancestor of the prefix is
 * already cut by its own 6(c) budget -- in which case the subtree is empty.  The
 * prefix's newest position is left for rec(), exactly as in a run from the root. */
static int worker_seed(W *w, const int *pre, int k, int32_t *Sout)
{
    int32_t S = 0, Sq[MAXM + 2];
    for (int i = 0; i < k; i++) w->ch[i] = pre[i];
    for (int i = 0; i < k; i++) {
        int32_t c = 0;
        for (int j = 0; j < k; j++) if (j != i) c += AD(w->ch[i], w->ch[j]);
        w->co[i] = c;
    }
    Sq[0] = 0;
    for (int q = 1; q <= k; q++) {
        int32_t add = 0;
        for (int i = 0; i < q - 1; i++) add += AD(w->ch[i], w->ch[q - 1]);
        Sq[q] = Sq[q - 1] + add;
    }
    S = Sq[k];
    int16_t *rv = w->rowv + (size_t)k * CO_NV;
    for (int x = 0; x < CO_NV; x++) {
        int32_t ss = S;
        for (int i = 0; i < k; i++) ss += AD(w->ch[i], x);
        rv[x] = (int16_t)ss;
    }
    w->famn[0] = 0; w->common[0] = ~0ULL;
    int tau = 0;
    for (int q = 1; q < k; q++) {
        tau = node_family(w, q, Sq[q], 1, q - 1);
        if (tau > tau_allow(Sq[q], q)) return -1;
    }
    *Sout = S;
    return (S <= BT[tau][k]) ? tau : -1;
}

static int  (*PRE)[MAXM + 2];
static int   PRE_K;
static long  PRE_N, next_idx = 0;
static pthread_mutex_t qlock = PTHREAD_MUTEX_INITIALIZER;

static long take_next(void)
{
    long i;
    pthread_mutex_lock(&qlock);
    i = (next_idx < PRE_N) ? next_idx++ : -1;
    pthread_mutex_unlock(&qlock);
    return i;
}

/* A prefix is a level-k node whose own clauses were already passed by whoever
 * wrote it: it is re-entered as rec(k) with its full family, so its subtree is
 * exactly the subtree the root run would have explored below it. */
static void *worker_main(void *arg)
{
    W *w = (W *)arg;
    double t0 = now();
    long i;
    while ((i = take_next()) >= 0) {
        int32_t S;
        int tau = worker_seed(w, PRE[i], PRE_K, &S);
        if (tau >= 0) rec(w, PRE_K, S, tau, PRE_K - 1);   /* rec computes the newest position's sets */
        else w->cut6c[PRE_K]++;
        w->prefixes_done++;
    }
    w->busy_s = now() - t0;
    return NULL;
}

static long load_prefixes(const char *path, int shard, int nshards)
{
    FILE *f = fopen(path, "r");
    if (!f) { fprintf(stderr, "cannot open %s\n", path); exit(1); }
    long cap = 4096, n = 0, lineno = 0;
    PRE = malloc((size_t)cap * sizeof(*PRE));
    char line[512];
    while (fgets(line, sizeof line, f)) {
        if (line[0] == '\n' || line[0] == '\0') continue;
        if (lineno++ % nshards != shard) continue;
        if (n == cap) { cap *= 2; PRE = realloc(PRE, (size_t)cap * sizeof(*PRE)); }
        int k = 0;
        for (char *tok = strtok(line, ",\n"); tok; tok = strtok(NULL, ",\n")) PRE[n][k++] = atoi(tok);
        if (PRE_K == 0) PRE_K = k;
        else if (PRE_K != k) { fprintf(stderr, "ragged prefix file at line %ld\n", lineno); exit(1); }
        n++;
    }
    fclose(f);
    return n;
}

int main(int argc, char **argv)
{
    int n = 7, m = 11, top = -1, nstart = 0, start[MAXM + 2];
    int shard = 0, nshards = 1, nthreads = 1;
    const char *startfile = NULL;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "-m")) m = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-n")) n = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-d")) Depth = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-top")) top = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-tmin")) TMIN = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-nopt")) usept = 0;
        else if (!strcmp(argv[i], "-check")) check = 1;
        else if (!strcmp(argv[i], "-clamp")) clamp = 1;
        else if (!strcmp(argv[i], "-cache")) cachebits = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-eager")) {
            char *sk = argv[++i], *tok = strtok(sk, ",");
            while (tok) { int L = atoi(tok); if (L >= 0 && L <= MAXM) eagerlev[L] = 1; tok = strtok(NULL, ","); }
        }
        else if (!strcmp(argv[i], "-skip")) {
            char *sk = argv[++i], *tok = strtok(sk, ",");
            while (tok) { int L = atoi(tok); if (L >= 0 && L <= MAXM) skiplev[L] = 1; tok = strtok(NULL, ","); }
        }
        else if (!strcmp(argv[i], "-startfile")) startfile = argv[++i];
        else if (!strcmp(argv[i], "-threads")) nthreads = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-survivors")) {
            survf = fopen(argv[++i], "w");
            if (!survf) { fprintf(stderr, "cannot write %s\n", argv[i]); return 1; }
        }
        else if (!strcmp(argv[i], "-dump")) {
            dumpf = fopen(argv[++i], "w");
            if (!dumpf) { fprintf(stderr, "cannot write %s\n", argv[i]); return 1; }
        }
        else if (!strcmp(argv[i], "-shard")) shard = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-of")) nshards = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-start")) {
            char *s = argv[++i], *tok = strtok(s, ",");
            while (tok) { start[nstart++] = atoi(tok); tok = strtok(NULL, ","); }
        } else { fprintf(stderr, "unknown arg %s\n", argv[i]); return 2; }
    }
    if (n != 7) { fprintf(stderr, "pseudo-tightness is implemented for CO_7 only\n"); return 2; }
    if (m > 11) { fprintf(stderr, "m <= 11 (pair masks are 64-bit)\n"); return 2; }
    Mtarget = m;
    double t0 = now();
    cog_init(n);
    cog_stab_init();
    cog_stab_drop_identity();
    pt_init(PT_ARBITRARY);
    {
        int q = 0;
        for (int i = 0; i < 16; i++) for (int j = i + 1; j < 16; j++) PIDX[i][j] = (uint8_t)(q < 64 ? q++ : 63);
    }
    {
        int B0[MAXM + 2];
        staircase(B0, m, n, (top > 0) ? top : Zfun(m) * Zfun(n) - 1);
        TOP = B0[m];
    }
    TAUCAP = 0;
    for (int j = 0; j <= MAXTAU; j++) {
        if (TOP - 2 * j < TMIN) break;
        staircase(BT[j], m, n, TOP - 2 * j);
        TAUCAP = j;
    }
    if (!usept) TAUCAP = 0;
    if (clamp && TAUCAP != 0) { fprintf(stderr, "-clamp is implemented for -tmin = top (TAUCAP 0) only\n"); return 2; }
    for (int j = TAUCAP + 1; j <= MAXTAU + 1; j++) for (int k = 0; k <= MAXM + 1; k++) BT[j][k] = -1;
    double t_setup = now() - t0;

    AD16 = malloc((size_t)CO_NV * CO_NV * sizeof(int16_t));
    for (size_t i = 0; i < (size_t)CO_NV * CO_NV; i++) AD16[i] = (int16_t)CO_ad[i];

    printf("{\"n\": %d, \"m\": %d, \"depth\": %d, \"top\": %d, \"tmin\": %d, \"pt\": %d, \"taucap\": %d, \"check\": %d, \"clamp\": %d, \"skip\": [",
           n, m, Depth, TOP, TMIN, usept, TAUCAP, check, clamp);
    { int f = 1; for (int L = 0; L <= MAXM; L++) if (skiplev[L]) { printf("%s%d", f ? "" : ", ", L); f = 0; } }
    printf("],\n");
    printf(" \"setup_s\": %.2f, \"staircases\": [", t_setup);
    for (int j = 0; j <= TAUCAP; j++) {
        printf("%s[", j ? ", " : "");
        for (int k = m; k >= 2; k--) printf("%d%s", BT[j][k], k > 2 ? ", " : "");
        printf("]");
    }
    printf("],\n");
    fflush(stdout);

    double ts = now();
    W **ws;
    int nw;
    if (startfile) {
        PRE_N = load_prefixes(startfile, shard, nshards);
        if (nthreads < 1) nthreads = 1;
        if (nthreads > PRE_N) nthreads = (int)(PRE_N > 0 ? PRE_N : 1);
        nw = nthreads;
        ws = malloc((size_t)nw * sizeof(W *));
        pthread_t th[256];
        for (int i = 0; i < nw; i++) ws[i] = worker_new();
        for (int i = 1; i < nw; i++) pthread_create(&th[i], NULL, worker_main, ws[i]);
        worker_main(ws[0]);
        for (int i = 1; i < nw; i++) pthread_join(th[i], NULL);
    } else {
        nw = 1;
        ws = malloc(sizeof(W *));
        W *w = ws[0] = worker_new();
        double tw = now();
        if (nstart == 0) {
            int16_t *rv1 = w->rowv + (size_t)1 * CO_NV;
            for (int x = 0; x < CO_NV; x++) rv1[x] = (int16_t)AD(0, x);
            w->ch[0] = 0; w->co[0] = 0;
            rec(w, 1, 0, 0, 0);
        } else {
            int32_t S;
            int tau = worker_seed(w, start, nstart, &S);
            if (tau >= 0) rec(w, nstart, S, tau, nstart - 1);
        }
        w->busy_s = now() - tw;
        w->prefixes_done = 1;
    }
    double el = now() - ts;
    if (dumpf) fclose(dumpf);
    if (survf) fclose(survf);

    uint64_t vis[MAXM + 2] = {0}, kept[MAXM + 2] = {0}, cut[MAXM + 2] = {0}, ptcalls = 0, cachehits = 0;
    static uint64_t taucount[MAXM + 2][MAXTAU + 2], HIST[HMAX][MAXTAU + 2];
    long prefixes_done = 0;
    double core_s = 0;
    for (int i = 0; i < nw; i++) {
        for (int k = 0; k <= m + 1; k++) {
            vis[k] += ws[i]->visited[k]; kept[k] += ws[i]->kept[k]; cut[k] += ws[i]->cut6c[k];
            for (int j = 0; j <= MAXTAU + 1; j++) taucount[k][j] += ws[i]->taucount[k][j];
        }
        for (int a = 0; a < HMAX; a++) for (int j = 0; j <= MAXTAU + 1; j++) HIST[a][j] += ws[i]->hist[a][j];
        ptcalls += ws[i]->ptcalls;
        cachehits += ws[i]->cachehits;
        prefixes_done += ws[i]->prefixes_done;
        core_s += ws[i]->busy_s;
    }
    printf(" \"shard\": %d, \"of\": %d, \"threads\": %d, \"prefixes_done\": %ld, \"core_seconds\": %.2f,\n",
           shard, nshards, nw, prefixes_done, core_s);
    printf(" \"survivor_histogram\": {");
    {
        int first = 1;
        for (int a = 0; a < HMAX; a++) for (int j = 0; j <= MAXTAU + 1; j++) if (HIST[a][j]) {
            printf("%s\"%d/tau%d\": %llu", first ? "" : ", ", a, j, (unsigned long long)HIST[a][j]);
            first = 0;
        }
    }
    printf("},\n \"visited\": [");
    for (int k = 1; k <= m; k++) printf("%llu%s", (unsigned long long)vis[k], k < m ? ", " : "");
    printf("],\n \"kept\": [");
    for (int k = 1; k <= m; k++) printf("%llu%s", (unsigned long long)kept[k], k < m ? ", " : "");
    printf("],\n \"cut_by_6c\": [");
    for (int k = 1; k <= m; k++) printf("%llu%s", (unsigned long long)cut[k], k < m ? ", " : "");
    printf("],\n \"tau_by_level\": [");
    for (int k = 1; k <= m; k++) {
        printf("%s[", k > 1 ? ", " : "");
        for (int j = 0; j <= TAUCAP; j++) printf("%llu%s", (unsigned long long)taucount[k][j], j < TAUCAP ? ", " : "");
        printf("]");
    }
    uint64_t tot = 0;
    for (int k = 0; k <= m + 1; k++) tot += vis[k];
    printf("],\n \"total_visited\": %llu, \"survivors\": %llu, \"pt_calls\": %llu, \"cache_hits\": %llu, \"elapsed_s\": %.3f}\n",
           (unsigned long long)tot, (unsigned long long)kept[m], (unsigned long long)ptcalls, (unsigned long long)cachehits, el);
    return 0;
}
