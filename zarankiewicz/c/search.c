/* search.c -- the node-keep predicate and DFS, ported from the received search.py.
 *
 * A partial (m,n)-set a_1..a_k is kept iff all of:
 *   (1) STAIRCASE            antisum(a_1..a_k) <= B[k]
 *   (2) PREFIX-MINIMALITY    the newly added element has MAXIMAL contribution
 *                            within the new prefix
 *   (3) STABILISER LEX-MIN   a_1 = vertex 0, and (a_2..a_k) is lex-minimal under
 *                            Stab(vertex 0), the dihedral group of order 2n
 *   (4) THEOREM 7 (optional, and measured NET NEGATIVE at (7,7): it shrinks the
 *       tree 1.442x and costs 3.08x per node, so it defaults OFF)
 *
 * The port is deliberately literal.  Clause (3) compares vertex INDICES, so it
 * depends on the vertex ORDER, which is why cog.c reproduces Python's
 * permutations(range(1,n)) ordering exactly rather than any convenient one.
 *
 * `--start` resumes from a prefix: the only state a node needs is its prefix,
 * since the contributions, the antisum and the row are all recomputable from it.
 * That makes a shard a prefix and a resume a re-issue of the same command.
 */
#define _POSIX_C_SOURCE 199309L
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "cog.h"

#define MAXM 14

static int   B[MAXM + 2];
static int   Mtarget, Depth = -1;
static int   excl2 = -1, excl4 = -1;        /* Theorem 7 limits, -1 = off */
static uint64_t counts[MAXM + 2];
static int16_t  *rowv;                      /* (MAXM+2) x CO_NV, their antisums */
static int16_t  *AD16;                      /* CO_NV x CO_NV as int16 */
static int   ch[MAXM + 2];
static int32_t co[MAXM + 2];
static double t_start, t_cap = -1.0;
static int   aborted = 0;

static double now(void)
{
    struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

/* Three changes from the received Python, none of which may alter a count.
 *
 *  (a) int16 THROUGHOUT.  Antisums cap at 223 and antidistances at 9, so the
 *      row and the antidistance matrix both fit in int16.  That doubles the
 *      SIMD width and halves the memory traffic of the inner pass.
 *  (b) A DENSE ROW, deliberately NOT compacted.  A compact candidate list was
 *      tried first and was barely faster, because indexing it turns the inner
 *      pass into a GATHER -- Av[cl[i]] rather than Av[i] -- and a gather does
 *      not vectorise.  Keeping the row dense and indexed by vertex makes all
 *      three operands sequential, which is what lets 16 lanes issue at once.
 *      The lesson generalises: compaction that saves iterations but introduces
 *      indirection is usually a loss.
 *  (c) The candidate scan writes a small index list, which IS worth compacting,
 *      because its consumers -- prefix-minimality and the stabiliser clause --
 *      are per-candidate and few, so indirection costs nothing there.
 *
 * The gate is what licenses all three: zsearch must still print the exact level
 * counts measured from the Python.
 */
static void rec(int k, int32_t S)
{
    counts[k]++;
    if (aborted) return;
    if (k == Mtarget) return;
    if (Depth > 0 && k >= Depth) return;
    if (t_cap > 0 && (counts[k] & 0xFFF) == 0 && now() - t_start > t_cap) { aborted = 1; return; }

    const int16_t *row = rowv + (size_t)k * CO_NV;
    int16_t *nrow = rowv + (size_t)(k + 1) * CO_NV;
    const int nv = CO_NV;
    const int lim = B[k + 1];

    /* (c) collect the candidates once; prefix-minimality also gives a LOWER
     * bound, since the new element's contribution must dominate every existing
     * one, so row[v] = S + cv >= S + max_i co[i]. */
    int32_t maxco = 0;
    for (int i = 0; i < k; i++) if (co[i] > maxco) maxco = co[i];
    const int lo = (int)(S + maxco);

    uint16_t cl[MAXNV];
    int ncl = 0;
    for (int v = 0; v < nv; v++) {
        const int r = row[v];
        if (r <= lim && r >= lo) cl[ncl++] = (uint16_t)v;
    }

    for (int ci = 0; ci < ncl; ci++) {
        const int v = cl[ci];
        const int32_t nS = row[v];
        const int32_t cv = nS - S;
        const int16_t *Av = AD16 + (size_t)v * nv;

        if (excl2 >= 0) {                                   /* (4) m' = 2 */
            int bad = 0;
            for (int i = 0; i < k; i++) if (Av[ch[i]] <= excl2) { bad = 1; break; }
            if (bad) continue;
        }

        int32_t nc[MAXM + 2];                               /* (2) prefix-minimality */
        int bad = 0;
        for (int i = 0; i < k; i++) {
            int32_t c2 = co[i] + Av[ch[i]];
            if (c2 > cv) { bad = 1; break; }
            nc[i] = c2;
        }
        if (bad) continue;
        nc[k] = cv;

        ch[k] = v;
        const int nk = k + 1;

        if (excl4 >= 0 && nk >= 4) {                        /* (4) m' = 4 */
            int viol = 0;
            for (int a = 0; a < k && !viol; a++)
                for (int b = a + 1; b < k && !viol; b++)
                    for (int c = b + 1; c < k; c++) {
                        int q0 = ch[a], q1 = ch[b], q2 = ch[c];
                        int ss = AD(q0, q1) + AD(q0, q2) + AD(q0, v)
                               + AD(q1, q2) + AD(q1, v) + AD(q2, v);
                        if (ss <= excl4) { viol = 1; break; }
                    }
            if (viol) continue;
        }

        int sm = 0;                                         /* (3) stabiliser lex-min */
        for (int g = 0; g < CO_nstab && !sm; g++) {
            const uint16_t *gm = CO_stab[g];
            for (int i = 1; i < nk; i++) {
                int t = ch[i], gt = gm[t];
                if (gt < t) { sm = 1; break; }
                if (gt > t) break;
            }
        }
        if (sm) continue;

        /* (a) + (b): the one pass that dominates everything.  All three operands
         * sequential and int16, so this is the loop the compiler must vectorise. */
        const int16_t cv16 = (int16_t)cv;
        for (int w = 0; w < nv; w++) nrow[w] = (int16_t)(row[w] + Av[w] + cv16);

        int32_t save_co[MAXM + 2];
        memcpy(save_co, co, sizeof(co));
        memcpy(co, nc, sizeof(int32_t) * (size_t)nk);
        rec(nk, nS);
        memcpy(co, save_co, sizeof(co));
        if (aborted) return;
    }
}

static int parity_required(int k, int n)
{
    if (k % 2 == 0 || n % 2 == 0) return -1;
    return (k % 4 == 3 && n % 4 == 3) ? 1 : 0;
}

static void staircase(int m, int n, int top)
{
    int t = (top > 0) ? top : Zfun(m) * Zfun(n) - 1;
    int p = parity_required(m, n);
    while (p >= 0 && (t % 2) != p) t--;
    B[m] = t;
    for (int k = m; k > 2; k--) {
        int b = (B[k] * (k - 2)) / k;
        int pk = parity_required(k - 1, n);
        while (pk >= 0 && (b % 2) != pk) b--;
        B[k - 1] = b;
    }
}

int main(int argc, char **argv)
{
    int n = 7, m = 7, top = -1, nstart = 0, start[MAXM + 2];
    int shard = 0, nshards = 1;
    const char *thm7 = "", *startfile = NULL;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "-m")) m = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-n")) n = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-d")) Depth = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-top")) top = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-cap")) t_cap = atof(argv[++i]);
        else if (!strcmp(argv[i], "-thm7")) thm7 = argv[++i];
        else if (!strcmp(argv[i], "-startfile")) startfile = argv[++i];
        else if (!strcmp(argv[i], "-shard")) shard = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-of")) nshards = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-start")) {
            char *s = argv[++i], *tok = strtok(s, ",");
            while (tok) { start[nstart++] = atoi(tok); tok = strtok(NULL, ","); }
        } else { fprintf(stderr, "unknown arg %s\n", argv[i]); return 2; }
    }
    Mtarget = m;
    double t0 = now();
    cog_init(n);
    cog_stab_init();
    cog_stab_drop_identity();
    staircase(m, n, top);
    if (strchr(thm7, '2')) excl2 = Zfun(2) * Zfun(n);
    if (strchr(thm7, '4')) excl4 = Zfun(4) * Zfun(n);
    double t_setup = now() - t0;

    rowv = malloc((size_t)(MAXM + 2) * CO_NV * sizeof(int16_t));
    AD16 = malloc((size_t)CO_NV * CO_NV * sizeof(int16_t));
    if (!rowv || !AD16) { fprintf(stderr, "oom\n"); return 1; }
    for (size_t i = 0; i < (size_t)CO_NV * CO_NV; i++) AD16[i] = (int16_t)CO_ad[i];
    memset(counts, 0, sizeof(counts));

    printf("{\"n\": %d, \"m\": %d, \"depth\": %d, \"thm7\": \"%s\", \"top\": %d,\n",
           n, m, Depth, thm7, B[m]);
    printf(" \"setup_s\": %.2f, \"NV\": %d, \"nstab_without_identity\": %d,\n",
           t_setup, CO_NV, CO_nstab);
    printf(" \"staircase\": [");
    for (int k = m; k >= 2; k--) printf("%d%s", B[k], k > 2 ? ", " : "");
    printf("],\n");
    fflush(stdout);

    t_start = now();
    if (startfile) {
        /* One prefix per line, comma-separated vertex indices.  Shard i of N takes
         * lines i, i+N, i+2N, ...  Sibling subtrees are disjoint, so the level
         * counts of the shards ADD, and level k < prefix length is contributed by
         * the frontier pass rather than by any shard. */
        FILE *f = fopen(startfile, "r");
        if (!f) { fprintf(stderr, "cannot open %s\n", startfile); return 1; }
        char line[512];
        long lineno = 0, used = 0;
        while (fgets(line, sizeof line, f)) {
            if (line[0] == '\n' || line[0] == '\0') continue;
            if (lineno++ % nshards != shard) continue;
            int k = 0;
            for (char *tok = strtok(line, ",\n"); tok; tok = strtok(NULL, ",\n"))
                ch[k++] = atoi(tok);
            int32_t S = 0;
            for (int i = 0; i < k; i++) {
                int32_t c = 0;
                for (int j = 0; j < k; j++) if (j != i) c += AD(ch[i], ch[j]);
                co[i] = c;
            }
            for (int i = 0; i < k; i++) for (int j = i + 1; j < k; j++) S += AD(ch[i], ch[j]);
            int16_t *rv = rowv + (size_t)k * CO_NV;
            for (int w = 0; w < CO_NV; w++) {
                int32_t ss = S;
                for (int i = 0; i < k; i++) ss += AD(ch[i], w);
                rv[w] = (int16_t)ss;
            }
            rec(k, S);
            used++;
            if (aborted) break;
        }
        fclose(f);
        printf(" \"shard\": %d, \"of\": %d, \"prefixes_done\": %ld,\n", shard, nshards, used);
    } else if (nstart == 0) {
        /* The Python does buf[1] = A_np[0]: the row for LEVEL 1, not level 0.
         * Writing it to buf[0] left rec(1, .) scanning uninitialised memory,
         * which is what the first gate run caught. */
        /* The Python does buf[1] = A_np[0]: the row for LEVEL 1, not level 0.
         * Writing it to level 0 left rec(1, .) scanning uninitialised memory,
         * which is what the first gate run caught. */
        int16_t *rv1 = rowv + (size_t)1 * CO_NV;
        for (int w = 0; w < CO_NV; w++) rv1[w] = (int16_t)AD(0, w);
        ch[0] = 0; co[0] = 0;
        rec(1, 0);
    } else {
        int k = nstart;
        int32_t S = 0;
        for (int i = 0; i < k; i++) ch[i] = start[i];
        for (int i = 0; i < k; i++) {
            int32_t c = 0;
            for (int j = 0; j < k; j++) if (j != i) c += AD(ch[i], ch[j]);
            co[i] = c;
        }
        for (int i = 0; i < k; i++) for (int j = i + 1; j < k; j++) S += AD(ch[i], ch[j]);
        int16_t *rv = rowv + (size_t)k * CO_NV;
        for (int w = 0; w < CO_NV; w++) {
            int32_t ss = S;
            for (int i = 0; i < k; i++) ss += AD(ch[i], w);
            rv[w] = (int16_t)ss;
        }
        rec(k, S);
    }
    double el = now() - t_start;

    uint64_t tot = 0;
    for (int k = 0; k <= m + 1; k++) tot += counts[k];
    printf(" \"level_counts\": [");
    for (int k = 1; k <= m; k++) printf("%llu%s", (unsigned long long)counts[k], k < m ? ", " : "");
    printf("],\n");
    printf(" \"total_nodes\": %llu, \"leaves\": %llu, \"elapsed_s\": %.3f,\n",
           (unsigned long long)tot, (unsigned long long)counts[m], el);
    printf(" \"nodes_per_s\": %.0f, \"aborted\": %s, \"level_counts_valid\": %s}\n",
           el > 0 ? tot / el : 0.0, aborted ? "true" : "false", aborted ? "false" : "true");
    return 0;
}
