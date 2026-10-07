/* screen.c -- the cheap half of the mixed bound, over every row the sweep wrote.
 *
 * For an 11-multiset of CO_7 rotations with antidistance matrix W and antisum T,
 * every subset S of the eleven stars is a good drawing of K_{7,|S|}, so
 *      crossings >= T + ( cr(K_{7,|S|}) - antisum(S) )
 * for each S -- one dual variable at weight 1.  The strongest single-subset
 * form of that is T + max over S of the deficit, which is what this computes,
 * exactly, over all 2^11 subsets.  It is a valid lower bound with no conjecture
 * assumed (cr(K_{7,k}) for k <= 10 are theorems), and mixedlp.py's LP can only
 * raise it.  Rows it already pushes to 225 or more are settled and need no LP.
 *
 *   cc -O2 -o screen screen.c
 *   ./screen A720.bin 225 survivors.txt < rows.txt
 * Reads "T,v0,...,v_{m-1}" lines (m taken from the first row, up to 11); prints a histogram of the bound and writes every
 * row whose bound is below the cut to survivors.txt (- to discard).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MMAX 11
static int M = 11;    /* set from the first row; proper subsets are size 3..M-1 */
#define NV 720
#define NS (1 << MMAX)

static uint8_t A[NV][NV];
/* cr(K_{7,k}) for k = 0..10; index 11 is never used as a clamp (open case). */
static const int CR7[12] = {0, 0, 0, 9, 18, 36, 54, 81, 108, 144, 180, -1};
static uint8_t pc[NS];
static int anti[NS];
static int sub[MMAX][1 << (MMAX - 1)]; /* sub[h][t] = sum over j in t of W[h][j] */

static int sizehist[12][16];   /* [subset size that gave the max deficit][deficit] */

static inline int bound_for(const int *v, int *Tout, int *bestk)
{
    int W[MMAX][MMAX], i, j, h, t, s, T = 0;
    for (i = 0; i < M; i++)
        for (j = 0; j < M; j++)
            W[i][j] = (i == j) ? 0 : A[v[i]][v[j]];
    for (i = 0; i < M; i++)
        for (j = i + 1; j < M; j++)
            T += W[i][j];
    for (h = 1; h < M; h++) {
        int lim = 1 << h;
        sub[h][0] = 0;
        for (t = 1; t < lim; t++) {
            int lb = t & (-t), k = __builtin_ctz(t);
            sub[h][t] = sub[h][t ^ lb] + W[h][k];
        }
    }
    anti[0] = 0;
    for (i = 0; i < M; i++) anti[1 << i] = 0;
    for (i = 0; i < M; i++) for (j = 0; j < M; j++) (void)W[i][j];
    int best = 0, bk = 0;
    int lim = 1 << M;
    for (s = 3; s < lim; s++) {
        if (pc[s] < 2) continue;
        h = 31 - __builtin_clz(s);
        int sp = s ^ (1 << h);
        anti[s] = anti[sp] + sub[h][sp];
        if (pc[s] >= 3 && pc[s] <= M - 1 && CR7[pc[s]] > 0) {
            int d = CR7[pc[s]] - anti[s];
            if (d > best) { best = d; bk = pc[s]; }
        }
    }
    *Tout = T;
    *bestk = bk;
    if (bk && best < 16) sizehist[bk][best]++;
    return T + best;
}

int main(int argc, char **argv)
{
    if (argc < 4) { fprintf(stderr, "usage: screen A720.bin CUT survivors.txt\n"); return 2; }
    FILE *f = fopen(argv[1], "rb");
    if (!f || fread(A, 1, sizeof A, f) != sizeof A) { perror("A720.bin"); return 2; }
    fclose(f);
    int cut = atoi(argv[2]);
    FILE *out = strcmp(argv[3], "-") ? fopen(argv[3], "w") : NULL;
    for (int s = 0; s < NS; s++) pc[s] = __builtin_popcount(s);

    static char buf[1 << 22];
    long long rows = 0, surv = 0;
    long long hist[512];
    memset(hist, 0, sizeof hist);
    size_t have = 0;
    for (;;) {
        size_t got = fread(buf + have, 1, sizeof(buf) - have, stdin);
        size_t avail = have + got;
        if (!avail) break;
        char *p = buf, *end = buf + avail, *last = buf;
        while (p < end) {
            char *nl = memchr(p, '\n', (size_t)(end - p));
            if (!nl) break;
            int v[MMAX], claimed = 0, k = 0;
            char *q = p;
            long x = 0; int any = 0, field = 0;
            while (q <= nl) {
                if (*q >= '0' && *q <= '9') { x = x * 10 + (*q - '0'); any = 1; }
                else {
                    if (any) {
                        if (field == 0) claimed = (int)x;
                        else if (k < MMAX) v[k++] = (int)x;
                        field++;
                    }
                    x = 0; any = 0;
                }
                q++;
            }
            if (rows == 0 && k >= 3 && k <= MMAX) M = k;
            if (k == M) {
                int T, bk;
                int b = bound_for(v, &T, &bk);
                if (T != claimed) { fprintf(stderr, "ANTISUM MISMATCH %d vs %d\n", T, claimed); return 3; }
                rows++;
                if (b >= 0 && b < 512) hist[b]++;
                if (b < cut) {
                    surv++;
                    if (out) fwrite(p, 1, (size_t)(nl - p + 1), out);
                }
            }
            p = nl + 1; last = p;
        }
        have = (size_t)(end - last);
        memmove(buf, last, have);
        if (!got) break;
    }
    if (out) fclose(out);
    fprintf(stderr, "rows %lld  below %d: %lld\n", rows, cut, surv);
    for (int b = 0; b < 512; b++) if (hist[b]) printf("bound %d: %lld\n", b, hist[b]);
    for (int k = 3; k <= 10; k++)
        for (int d = 1; d < 16; d++)
            if (sizehist[k][d]) printf("argmax |S|=%d deficit %d: %d\n", k, d, sizehist[k][d]);
    return 0;
}
