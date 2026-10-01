/* cog.c -- CO_n, the antidistance matrix, the relabel group and the stabiliser.
 *
 * A faithful port of the received cog.py.  Faithful is the operative word: the
 * node-keep predicate in search.c is gated on reproducing level counts that were
 * measured from the Python, so any divergence here is a silent wrong answer
 * rather than a crash.  Every construction below therefore mirrors the Python
 * line for line, including the vertex ORDER, because the stabiliser lex-min
 * clause compares vertex INDICES and a different ordering changes which nodes
 * survive.
 *
 *   V(CO_n) = the (n-1)! cyclic orders of {0..n-1}, each rotated so 0 leads,
 *             listed in the order permutations(range(1,n)) produces.
 *   u ~ v   iff v is u with two CYCLICALLY adjacent entries transposed.
 *   rev[u]  = the reverse cyclic order.
 *   ad[a][b] = d(a, rev[b]).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "cog.h"

int CO_n, CO_NV;
uint16_t (*CO_adj)[MAXN];
uint16_t *CO_rev;
uint8_t *CO_ad;            /* CO_NV * CO_NV, row-major */
uint16_t (*CO_stab)[MAXNV];
int CO_nstab;

static uint8_t (*vlist)[MAXN];

/* rotate so that 0 leads */
static void canon(const uint8_t *in, uint8_t *out, int n)
{
    int i, z = 0;
    for (i = 0; i < n; i++) if (in[i] == 0) { z = i; break; }
    for (i = 0; i < n; i++) out[i] = in[(z + i) % n];
}

/* permutations of 1..n-1 in lexicographic order, exactly as Python's
 * itertools.permutations(range(1,n)) yields them */
static int next_perm(uint8_t *a, int k)
{
    int i = k - 2, j, l;
    while (i >= 0 && a[i] >= a[i + 1]) i--;
    if (i < 0) return 0;
    j = k - 1;
    while (a[j] <= a[i]) j--;
    uint8_t t = a[i]; a[i] = a[j]; a[j] = t;
    for (l = i + 1, j = k - 1; l < j; l++, j--) { t = a[l]; a[l] = a[j]; a[j] = t; }
    return 1;
}

static int *vhash;                            /* perfect hash on the tail */
static int tail_key(const uint8_t *v)
{
    /* v[0] == 0 always; encode v[1..n-1] in base n */
    int k = 0, i;
    for (i = 1; i < CO_n; i++) k = k * CO_n + v[i];
    return k;
}

void cog_init(int n)
{
    int i, j, nv = 1;
    CO_n = n;
    for (i = 2; i < n; i++) nv *= i;          /* (n-1)! */
    CO_NV = nv;
    vlist = malloc((size_t)nv * sizeof(*vlist));
    CO_adj = malloc((size_t)nv * sizeof(*CO_adj));
    CO_rev = malloc((size_t)nv * sizeof(*CO_rev));
    CO_ad  = malloc((size_t)nv * nv);
    if (!vlist || !CO_adj || !CO_rev || !CO_ad) { fprintf(stderr, "oom\n"); exit(1); }

    uint8_t tail[MAXN];
    for (i = 0; i < n - 1; i++) tail[i] = (uint8_t)(i + 1);
    int idx = 0;
    do {
        vlist[idx][0] = 0;
        for (i = 0; i < n - 1; i++) vlist[idx][i + 1] = tail[i];
        idx++;
    } while (next_perm(tail, n - 1));
    if (idx != nv) { fprintf(stderr, "vertex count %d != %d\n", idx, nv); exit(1); }

    int hsize = 1; for (i = 1; i < n; i++) hsize *= n;
    vhash = malloc((size_t)hsize * sizeof(int));
    for (i = 0; i < hsize; i++) vhash[i] = -1;
    for (i = 0; i < nv; i++) vhash[tail_key(vlist[i])] = i;

    uint8_t w[MAXN], c[MAXN];
    for (i = 0; i < nv; i++) {
        for (j = 0; j < n; j++) {
            int k = (j + 1) % n;
            memcpy(w, vlist[i], n);
            uint8_t t = w[j]; w[j] = w[k]; w[k] = t;
            canon(w, c, n);
            CO_adj[i][j] = (uint16_t)vhash[tail_key(c)];
        }
        for (j = 0; j < n; j++) w[j] = vlist[i][n - 1 - j];
        canon(w, c, n);
        CO_rev[i] = (uint16_t)vhash[tail_key(c)];
    }

    /* BFS from every vertex, then ad[a][b] = d(a, rev[b]) */
    int *dist = malloc((size_t)nv * sizeof(int));
    int *q = malloc((size_t)nv * sizeof(int));
    uint8_t *drow = malloc((size_t)nv);
    for (i = 0; i < nv; i++) {
        for (j = 0; j < nv; j++) dist[j] = -1;
        int head = 0, tailq = 0;
        dist[i] = 0; q[tailq++] = i;
        while (head < tailq) {
            int u = q[head++];
            for (j = 0; j < n; j++) {
                int v = CO_adj[u][j];
                if (dist[v] < 0) { dist[v] = dist[u] + 1; q[tailq++] = v; }
            }
        }
        for (j = 0; j < nv; j++) drow[j] = (uint8_t)dist[j];
        memcpy(CO_ad + (size_t)i * nv, drow, nv);   /* temporarily plain distance */
    }
    /* turn distance into antidistance in place, row by row, using a copy */
    uint8_t *tmp = malloc((size_t)nv * nv);
    memcpy(tmp, CO_ad, (size_t)nv * nv);
    for (i = 0; i < nv; i++)
        for (j = 0; j < nv; j++)
            CO_ad[(size_t)i * nv + j] = tmp[(size_t)i * nv + CO_rev[j]];
    free(tmp); free(dist); free(q); free(drow);
}

/* The stabiliser of vertex 0 inside S_n x <rev>, as maps on vertex indices.
 * The Python builds the whole group of order 2*n! and filters; we do the same,
 * one permutation at a time, so no 10080 x 720 table is ever held. */
void cog_stab_init(void)
{
    int nfact = 1, i, j, n = CO_n;
    for (i = 2; i <= n; i++) nfact *= i;
    CO_stab = malloc((size_t)(2 * n) * sizeof(*CO_stab));
    CO_nstab = 0;

    uint8_t perm[MAXN], w[MAXN], c[MAXN];
    for (i = 0; i < n; i++) perm[i] = (uint8_t)i;
    int count = 0;
    do {
        count++;
        for (int withrev = 0; withrev < 2; withrev++) {
            /* image of vertex 0 under this map */
            for (j = 0; j < n; j++) w[j] = perm[vlist[0][j]];
            canon(w, c, n);
            int img = vhash[tail_key(c)];
            if (withrev) img = CO_rev[img];
            if (img != 0) continue;
            if (CO_nstab >= 2 * n) { fprintf(stderr, "stabiliser too big\n"); exit(1); }
            for (int v = 0; v < CO_NV; v++) {
                for (j = 0; j < n; j++) w[j] = perm[vlist[v][j]];
                canon(w, c, n);
                int m = vhash[tail_key(c)];
                CO_stab[CO_nstab][v] = (uint16_t)(withrev ? CO_rev[m] : m);
            }
            CO_nstab++;
        }
    } while (next_perm(perm, n));
    if (count != nfact) { fprintf(stderr, "perm count %d != %d\n", count, nfact); exit(1); }
}

/* drop the identity, as the Python does before passing stab into search() */
int cog_stab_drop_identity(void)
{
    int w = 0;
    for (int i = 0; i < CO_nstab; i++) {
        int ident = 1;
        for (int v = 0; v < CO_NV; v++) if (CO_stab[i][v] != v) { ident = 0; break; }
        if (ident) continue;
        if (w != i) memcpy(CO_stab[w], CO_stab[i], sizeof(CO_stab[0]));
        w++;
    }
    CO_nstab = w;
    return w;
}

int Zfun(int n) { return (n / 2) * ((n - 1) / 2); }
