/* co11min.c -- how low can the SEVEN-star side go?
 *
 * The same drawing of K_{7,11} gives 21 pairs of 11-stars, and Woodall's bound
 * applies to them in CO_11 exactly as it does to the 55 pairs of 7-stars in
 * CO_7.  So min over 7-multisets of CO_11 of the 21-pair antisum is an
 * independent lower bound on cr(K_{7,11}).  The CO_7 side bottoms out at 219
 * (this programme's completed sweep) and the mixed bound lifts that to 223; if
 * the CO_11 side cannot go below 225 the conjecture follows for K_{7,11}.
 *
 * This is a HEURISTIC: exact coordinate descent (each of the seven positions
 * replaced by its global best, all 3628800 candidates scanned) from random
 * restarts.  It returns an UPPER bound on that minimum.  An upper bound below
 * 225 kills the route; one that never dips below 225 is encouragement, not
 * proof -- the proof needs the staircase sweep whose rungs this prints.
 *
 *   cc -O2 -o co11min co11min.c && ./co11min [restarts] [seed]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define K 10
#define NV 3628800
#define M7 7

static const int FACT[11] = {1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800};
static uint8_t dist[NV];
static int32_t q[NV];
static uint8_t *f[M7];
static uint16_t *S;

static void unrank(int r, int *p)
{
    int avail[K], i, j, n = K;
    for (i = 0; i < K; i++) avail[i] = i + 1;
    for (i = 0; i < K; i++) {
        int fa = FACT[n - 1], k = r / fa;
        r -= k * fa;
        p[i] = avail[k];
        for (j = k; j < n - 1; j++) avail[j] = avail[j + 1];
        n--;
    }
}

static int rank_of(const int *p)
{
    int avail[K], i, j, n = K, r = 0;
    for (i = 0; i < K; i++) avail[i] = i + 1;
    for (i = 0; i < K; i++) {
        for (j = 0; j < n; j++) if (avail[j] == p[i]) break;
        r += j * FACT[n - 1];
        for (; j < n - 1; j++) avail[j] = avail[j + 1];
        n--;
    }
    return r;
}

static void bfs(void)
{
    int p[K], t[K], i;
    memset(dist, 0xff, sizeof dist);
    dist[0] = 0;
    long long head = 0, tail = 0;
    q[tail++] = 0;
    while (head < tail) {
        int u = q[head++], du = dist[u], w;
        unrank(u, p);
        for (i = 1; i <= 9; i++) {
            memcpy(t, p, sizeof t);
            int a = t[i - 1]; t[i - 1] = t[i]; t[i] = a;
            w = rank_of(t);
            if (dist[w] == 0xff) { dist[w] = du + 1; q[tail++] = w; }
        }
        for (i = 0; i < K - 1; i++) t[i] = p[i + 1];
        t[K - 1] = p[0];
        w = rank_of(t);
        if (dist[w] == 0xff) { dist[w] = du + 1; q[tail++] = w; }
        t[0] = p[K - 1];
        for (i = 1; i < K; i++) t[i] = p[i - 1];
        w = rank_of(t);
        if (dist[w] == 0xff) { dist[w] = du + 1; q[tail++] = w; }
    }
}

/* sigma[] maps symbol -> its position in the cyclic order (0,a0..a9). */
static void sigma_of(int a, int *sig)
{
    int p[K], i;
    unrank(a, p);
    sig[0] = 0;
    for (i = 0; i < K; i++) sig[p[i]] = i + 1;
}

/* dbar(a,b) = d(a, rev b), computed by relabelling a to the identity. */
static inline int dbar_with(const int *sig, int b)
{
    int p[K], seq[K + 1], c[K + 1], t[K], i, z = 0;
    unrank(b, p);
    /* rev b, canonical: (0, p9, p8, ..., p0) */
    seq[0] = 0;
    for (i = 0; i < K; i++) seq[i + 1] = p[K - 1 - i];
    for (i = 0; i <= K; i++) { c[i] = sig[seq[i]]; if (c[i] == 0) z = i; }
    for (i = 0; i < K; i++) t[i] = c[(z + 1 + i) % (K + 1)];
    return dist[rank_of(t)];
}

static int antisum(const int *v)
{
    int sig[K + 1], i, j, s = 0;
    for (i = 0; i < M7; i++) {
        sigma_of(v[i], sig);
        for (j = i + 1; j < M7; j++) s += dbar_with(sig, v[j]);
    }
    return s;
}

int main(int argc, char **argv)
{
    int restarts = argc > 1 ? atoi(argv[1]) : 4;
    unsigned seed = argc > 2 ? (unsigned)atoi(argv[2]) : 20261007u;
    bfs();
    fprintf(stderr, "CO_11 distances ready\n");
    /* the staircase for seven stars, descending from Z(11)Z(7) - 2 = 223 */
    int B = 223;
    fprintf(stderr, "staircase: B[7]=%d", B);
    for (int k = 7; k > 2; k--) { B = B * (k - 2) / k; fprintf(stderr, " B[%d]=%d", k - 1, B); }
    fprintf(stderr, "\n");
    for (int i = 0; i < M7; i++) f[i] = malloc(NV);
    S = malloc(NV * sizeof *S);
    srandom(seed);
    int bestever = 1 << 30, bestv[M7];
    for (int r = 0; r < restarts; r++) {
        int v[M7];
        for (int i = 0; i < M7; i++) v[i] = random() % NV;
        int cur = antisum(v), it;
        for (it = 0; it < 40; it++) {
            int sig[K + 1];
            for (int i = 0; i < M7; i++) {
                sigma_of(v[i], sig);
                for (int b = 0; b < NV; b++) f[i][b] = (uint8_t)dbar_with(sig, b);
            }
            for (int b = 0; b < NV; b++) {
                int s = 0;
                for (int i = 0; i < M7; i++) s += f[i][b];
                S[b] = (uint16_t)s;
            }
            int moved = 0;
            for (int i = 0; i < M7; i++) {
                int bb = -1, bv = 1 << 30;
                for (int b = 0; b < NV; b++) {
                    int s = S[b] - f[i][b];
                    if (s < bv) { bv = s; bb = b; }
                }
                /* cost of the 21 pairs = (pairs not touching i) + bv */
                int old = v[i];
                v[i] = bb;
                int ns = antisum(v);
                if (ns < cur) { cur = ns; moved = 1; }
                else v[i] = old;
            }
            if (!moved) break;
        }
        fprintf(stderr, "restart %d: antisum %d after %d sweeps\n", r, cur, it);
        if (cur < bestever) { bestever = cur; memcpy(bestv, v, sizeof v); }
    }
    printf("CO_11 seven-star heuristic minimum antisum: %d   (target 225)\n", bestever);
    printf("multiset:");
    for (int i = 0; i < M7; i++) printf(" %d", bestv[i]);
    printf("\n");
    return 0;
}
