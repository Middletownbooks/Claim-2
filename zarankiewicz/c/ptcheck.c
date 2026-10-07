/* ptcheck.c -- Theorem 6(c) over rows: t (non-pseudo-tight (4,7)-subsets) and
 * tau (minimum transversal of them by pairs), so f = antisum + 2*tau.
 *
 *   cc -O2 -o ptcheck ptcheck.c pt.c cog.c
 *   ./ptcheck -selftest
 *   ./ptcheck [-family arbitrary|distinct|twice] [-cap K] [-print] < rows
 *   ./ptcheck -quads < quads        # "a,b,c,d" lines -> verdict per line
 *   ./ptcheck -need [-target 225] < rows   # print rows with antisum + 2*tau < target
 *
 * Rows are "T,v0,...,v_{m-1}" (m <= 12), as zsearch -survivors and the sweep's
 * low_*.txt write them.  Prints a histogram of (antisum, tau) and of t, and the
 * weakest f = antisum + 2*tau seen.  tau is exact up to -cap (default 12).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "cog.h"
#include "pt.h"

static int fam_of(const char *s)
{
    if (!strcmp(s, "arbitrary")) return PT_ARBITRARY;
    if (!strcmp(s, "distinct")) return PT_DISTINCT;
    if (!strcmp(s, "twice")) return PT_TWICE;
    fprintf(stderr, "unknown family %s\n", s); exit(2);
}

static unsigned long long rng = 88172645463325252ULL;
static unsigned rnd(void) { rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17; return (unsigned)(rng >> 11); }

int main(int argc, char **argv)
{
    int family = PT_ARBITRARY, cap = 12, print = 0, selftest = 0, quads = 0, need = 0, target = 225;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "-family")) family = fam_of(argv[++i]);
        else if (!strcmp(argv[i], "-cap")) cap = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-print")) print = 1;
        else if (!strcmp(argv[i], "-selftest")) selftest = 1;
        else if (!strcmp(argv[i], "-quads")) quads = 1;
        else if (!strcmp(argv[i], "-target")) target = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-need")) need = 1;
        else { fprintf(stderr, "unknown arg %s\n", argv[i]); return 2; }
    }
    cog_init(7);
    if (selftest) {
        static const char *nm[3] = {"arbitrary", "distinct", "twice"};
        for (int f = 0; f < 3; f++) { pt_init(f); printf("family %-9s size %d\n", nm[f], PT_family_size); free(PT_F); free(PT_P); }
        pt_init(family);
        long asym = 0;
        for (int a = 0; a < CO_NV; a++) for (int b = 0; b < CO_NV; b++) {
            size_t k = (size_t)a * CO_NV + b, k2 = (size_t)b * CO_NV + a;
            if (PT_F[k] != PT_F[k2] || PT_P[k] != PT_P[k2]) asym++;
            if ((PT_F[k] & ~PT_P[k]) != 0) { printf("F not within P at %d %d\n", a, b); return 1; }
            if (__builtin_popcount(PT_F[k]) > AD(a, b)) { printf("more forced labels than steps at %d %d\n", a, b); return 1; }
        }
        printf("F/P asymmetric pairs: %ld (expect 0)\n", asym);
        /* order invariance of pt4 under the 24 orderings of the four elements */
        int perms[24][4], np = 0;
        for (int a = 0; a < 4; a++) for (int b = 0; b < 4; b++) for (int c = 0; c < 4; c++) for (int d = 0; d < 4; d++)
            if (a != b && a != c && a != d && b != c && b != d && c != d) { perms[np][0] = a; perms[np][1] = b; perms[np][2] = c; perms[np][3] = d; np++; }
        long npt = 0, nbad = 0, tot = 20000;
        for (long s = 0; s < tot; s++) {
            int e[4];
            for (int i = 0; i < 4; i++) e[i] = (int)(rnd() % CO_NV);
            int r0 = pt4(e[0], e[1], e[2], e[3]);
            npt += r0;
            for (int p = 1; p < 24; p++)
                if (pt4(e[perms[p][0]], e[perms[p][1]], e[perms[p][2]], e[perms[p][3]]) != r0) { nbad++; break; }
        }
        printf("random 4-multisets: %ld of %ld pseudo-tight; order-dependent: %ld (expect 0)\n", npt, tot, nbad);
        return 0;
    }
    pt_init(family);
    if (quads) {                        /* "a,b,c,d" per line -> "a,b,c,d verdict" */
        char ql[256];
        while (fgets(ql, sizeof ql, stdin)) {
            int e[4];
            if (sscanf(ql, "%d,%d,%d,%d", &e[0], &e[1], &e[2], &e[3]) != 4) continue;
            printf("%d,%d,%d,%d %d\n", e[0], e[1], e[2], e[3], pt4(e[0], e[1], e[2], e[3]));
        }
        return 0;
    }
    if (need) {
        /* Stage A: for each row decide only whether antisum + 2*tau >= target, i.e.
         * tau >= K := ceil((target - antisum)/2), stopping as soon as that is certain.
         * Prints every row that FAILS (tau < K) and a one-line summary. */
        long rows = 0, fails = 0, calls = 0;
        static long byK[64];
        char ln[1024];
        while (fgets(ln, sizeof ln, stdin)) {
            int v[16], k = 0;
            char copy[1024]; strcpy(copy, ln);
            for (char *tok = strtok(ln, ",\n"); tok && k < 16; tok = strtok(NULL, ",\n")) v[k++] = atoi(tok);
            if (k < 5 || k > 12) continue;
            int T = v[0], m = k - 1, *M = v + 1;
            int Tre = 0;                        /* read the row itself, not its label */
            for (int a = 0; a < m; a++) for (int b = a + 1; b < m; b++) Tre += AD(M[a], M[b]);
            if (Tre != T) { fprintf(stderr, "antisum mismatch: row says %d, rotations give %d\n", T, Tre); return 1; }
            int K = (target - T + 1) / 2;
            if (K < 0) K = 0;
            rows++;
            if (K < 64) byK[K]++;
            if (K == 0) continue;
            uint16_t S[512]; int ns = 0, done = 0;
            uint64_t common = ~0ULL;
            for (int a = 0; a < m && !done; a++) for (int b = a + 1; b < m && !done; b++)
                for (int c = b + 1; c < m && !done; c++) for (int d = c + 1; d < m && !done; d++) {
                    calls++;
                    if (pt4(M[a], M[b], M[c], M[d])) continue;
                    uint16_t s4 = (uint16_t)((1 << a) | (1 << b) | (1 << c) | (1 << d));
                    S[ns++] = s4;
                    uint64_t pm = 0; int p[4] = {a, b, c, d};
                    for (int x = 0; x < 4; x++) for (int y = x + 1; y < 4; y++) pm |= 1ULL << (p[x] * (21 - p[x]) / 2 + p[y] - p[x] - 1);   /* < 55 for m <= 11 */
                    common &= pm;
                    if (K == 1) done = 1;                       /* one non-PT set: tau >= 1 */
                    else if (K == 2 && common == 0) done = 1;   /* no common pair: tau >= 2 */
                }
            if (!done && K >= 2 && ns > 0) done = !pt_feasible(S, ns, K - 1);
            if (!done) { fails++; fputs(copy, stdout); }
        }
        fprintf(stderr, "need: rows %ld  fails %ld  pt_calls %ld  target %d  rows by K:", rows, fails, calls, target);
        for (int q = 0; q < 64; q++) if (byK[q]) fprintf(stderr, " K%d:%ld", q, byK[q]);
        fprintf(stderr, "\n");
        return 0;
    }
    static long hist[512][16];
    static long thist[400];
    long rows = 0;
    int worst = 1 << 30;
    char line[1024];
    while (fgets(line, sizeof line, stdin)) {
        int v[16], k = 0;
        for (char *tok = strtok(line, ",\n"); tok && k < 16; tok = strtok(NULL, ",\n")) v[k++] = atoi(tok);
        if (k < 5) continue;
        int T = v[0], m = k - 1, *M = v + 1;
        uint16_t S[512]; int ns = 0;
        for (int a = 0; a < m; a++) for (int b = a + 1; b < m; b++)
            for (int c = b + 1; c < m; c++) for (int d = c + 1; d < m; d++)
                if (!pt4(M[a], M[b], M[c], M[d])) S[ns++] = (uint16_t)((1 << a) | (1 << b) | (1 << c) | (1 << d));
        int tau = pt_tau(S, ns, m, cap);
        if (print) printf("%d %d %d\n", T, ns, tau);
        if (T >= 0 && T < 512) hist[T][tau < 15 ? tau : 15]++;
        thist[ns < 399 ? ns : 399]++;
        if (T + 2 * tau < worst) worst = T + 2 * tau;
        rows++;
    }
    printf("rows %ld   weakest f = antisum + 2*tau = %d\n", rows, worst);
    for (int T = 0; T < 512; T++) {
        int any = 0; for (int q = 0; q < 16; q++) any |= hist[T][q] != 0;
        if (!any) continue;
        printf("antisum %d  tau:", T);
        for (int q = 0; q < 16; q++) if (hist[T][q]) printf("  %d%s:%ld", q, q == cap + 1 ? "+" : "", hist[T][q]);
        printf("\n");
    }
    printf("t histogram:");
    for (int q = 0; q < 400; q++) if (thist[q]) printf(" %d:%ld", q, thist[q]);
    printf("\n");
    return 0;
}
