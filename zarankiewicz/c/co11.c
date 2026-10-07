/* co11.c -- the OTHER side of the same drawing.
 *
 * Woodall's pairwise bound applies to any two stars that share their leaves.
 * This programme has only ever used the eleven 7-stars (multisets of 11 vertices
 * of CO_7, 720 vertices).  But the seven 11-stars share THEIR eleven leaves,
 * so the same bound holds in CO_11 (10! = 3628800 vertices, 11-regular), and
 *      crossings >= sum over the C(7,2) = 21 pairs of dbar_{CO_11}
 * is an INDEPENDENT lower bound on the same number of crossings.
 *
 * S_11 acts transitively on the vertices of CO_11, and relabelling preserves
 * distance, so ONE breadth-first search settles the whole distance profile.
 * dbar(a,b) = d(a, rev b) and rev is just reversal, so the number of partners
 * at antidistance at most r is the size of the ball of radius r.
 *
 * A vertex is the cyclic order (0, p_1, ..., p_10); it is stored as the
 * lexicographic rank of p.  The eleven neighbours are the nine internal
 * adjacent transpositions plus the two that move 0 and need re-canonicalising.
 *
 *   cc -O2 -o co11 co11.c && ./co11
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define K 10                   /* permuted symbols 1..10 */
#define NV 3628800             /* 10! */

static const int FACT[11] = {1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800};

static void unrank(int r, int *p)
{
    int avail[K], i, j;
    for (i = 0; i < K; i++) avail[i] = i + 1;
    int n = K;
    for (i = 0; i < K; i++) {
        int f = FACT[n - 1], k = r / f;
        r -= k * f;
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

static uint8_t dist[NV];
static int32_t q[NV];

int main(void)
{
    int p[K], t[K], i;
    memset(dist, 0xff, sizeof dist);
    int v0 = 0;                       /* p = (1,2,...,10): the identity order */
    dist[v0] = 0;
    long long head = 0, tail = 0;
    q[tail++] = v0;
    long long lvl[64];
    memset(lvl, 0, sizeof lvl);
    lvl[0] = 1;
    int maxd = 0;
    while (head < tail) {
        int u = q[head++];
        int du = dist[u];
        unrank(u, p);
        for (i = 1; i <= 9; i++) {            /* internal adjacent transpositions */
            memcpy(t, p, sizeof t);
            int a = t[i - 1]; t[i - 1] = t[i]; t[i] = a;
            int w = rank_of(t);
            if (dist[w] == 0xff) { dist[w] = du + 1; if (du + 1 > maxd) maxd = du + 1; lvl[du + 1]++; q[tail++] = w; }
        }
        /* swap positions 0,1 of (0,p1..p10): (p1,0,p2..p10) -> (0,p2,..,p10,p1) */
        for (i = 0; i < K - 1; i++) t[i] = p[i + 1];
        t[K - 1] = p[0];
        {
            int w = rank_of(t);
            if (dist[w] == 0xff) { dist[w] = du + 1; if (du + 1 > maxd) maxd = du + 1; lvl[du + 1]++; q[tail++] = w; }
        }
        /* swap positions 10,0 (wraparound): -> (0,p10,p1..p9) */
        t[0] = p[K - 1];
        for (i = 1; i < K; i++) t[i] = p[i - 1];
        {
            int w = rank_of(t);
            if (dist[w] == 0xff) { dist[w] = du + 1; if (du + 1 > maxd) maxd = du + 1; lvl[du + 1]++; q[tail++] = w; }
        }
    }
    printf("vertices reached %lld of %d, eccentricity %d\n", tail, NV, maxd);
    long long cum = 0;
    for (i = 0; i <= maxd; i++) {
        cum += lvl[i];
        printf("  d=%2d : %10lld   cumulative %10lld\n", i, lvl[i], cum);
    }
    /* dbar(v0, b) = d(v0, rev b); rev is reversal of p, a bijection, so the
     * antidistance profile equals the distance profile.  dbar(a,a) = d(a,rev a). */
    int rv[K];
    for (i = 0; i < K; i++) rv[i] = K - i;        /* reverse of the identity */
    printf("dbar(a,a) = d(identity, reversed) = %d   [Z(11) = 25]\n", dist[rank_of(rv)]);
    return 0;
}
