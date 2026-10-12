/* Stage 3: deeper witness families applied to stage-1/2 survivors.
 *
 * conj2 : widen the bounded p2 test (y,z <= YZ).  Clearing a survivor here is
 *         a PROOF it is covered (an explicit witness); failing is not a proof
 *         of anything, only promotion to a still deeper search.
 * rigid : hed1 for r = 7, 11, 15, ...  A witness is a divisor d of
 *         M = p*((p+r)/4) with d = -1 (mod r).  Since p = 1 mod r is not
 *         guaranteed, build the set of residues mod r reachable as products
 *         of prime-power divisors of M and test whether r-1 is among them.
 *         Finding one PROVES p is not rigid.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int p2_test(uint64_t a, int YZ){
    for (int y = 1; y <= YZ; y++)
        for (int z = 1; z <= YZ; z++) {
            int64_t den = 4LL*(4LL*y*z - z - 1);
            if (den <= 0) continue;
            int64_t num = (int64_t)a + 4LL*y*z - 1;
            if (num > 0 && num % den == 0 && num/den >= 1) return 1;
        }
    return 0;
}

/* residues mod r reachable as divisors of n (n factored by trial division) */
static int divisor_hits(uint64_t n, int r, int target){
    unsigned char reach[512]; memset(reach, 0, r);
    reach[1 % r] = 1;
    uint64_t m = n;
    for (uint64_t d = 2; d*d <= m; d++) {
        if (m % d) continue;
        int e = 0; while (m % d == 0) { m /= d; e++; }
        unsigned char nr[512]; memcpy(nr, reach, r);
        uint64_t pw = 1;
        for (int i = 0; i < e; i++) {
            pw = pw * (d % r) % r;
            for (int s = 0; s < r; s++) if (reach[s]) nr[s * pw % r] = 1;
        }
        memcpy(reach, nr, r);
    }
    if (m > 1) {
        unsigned char nr[512]; memcpy(nr, reach, r);
        for (int s = 0; s < r; s++) if (reach[s]) nr[s * (m % r) % r] = 1;
        memcpy(reach, nr, r);
    }
    return reach[target % r];
}

int main(int argc, char**argv){
    int rigid = !strcmp(argv[1], "rigid");
    FILE *f = fopen(argv[2], "r");
    int PARAM = argc > 3 ? atoi(argv[3]) : (rigid ? 60 : 400);
    if (argc < 5) { fprintf(stderr, "usage: stage3 MODE INFILE PARAM OUTFILE\n"); return 1; }
    FILE *out = fopen(argv[4], "w");   /* explicit: must differ from INFILE */
    uint64_t v, n = 0, left = 0;
    while (fscanf(f, "%llu", (unsigned long long*)&v) == 1) {
        n++;
        int cleared = 0;
        if (!rigid) {
            cleared = p2_test(v, PARAM);
        } else {
            for (int r = 7; r <= PARAM && !cleared; r += 4) {
                if ((v + r) % 4) continue;
                uint64_t M1 = (v + r) / 4;          /* M = p * M1 */
                /* reachable residues of divisors of M = p*M1 */
                int rr = r;
                unsigned char reach[512]; memset(reach, 0, rr);
                /* start from divisors of M1, then optionally multiply by p */
                if (divisor_hits(M1, rr, rr - 1)) cleared = 1;
                else {
                    /* target/p: need d1 | M1 with d1 = -1 * p^{-1} (mod r) */
                    long long pm = v % rr; if (pm == 0) continue;
                    long long inv = 1;
                    while ((inv * pm) % rr != 1) { inv++; if (inv > rr) break; }
                    if (inv <= rr && divisor_hits(M1, rr, (int)(((rr - 1) * inv) % rr)))
                        cleared = 1;
                }
            }
        }
        if (!cleared) { left++; fprintf(out, "%llu\n", (unsigned long long)v); }
        if (n % 20000 == 0) fprintf(stderr, "\r  %llu processed, %llu left",
            (unsigned long long)n, (unsigned long long)left);
    }
    fclose(out);
    fprintf(stderr, "\n%s stage3 (param %d): %llu in, %llu survive\n",
            argv[1], PARAM, (unsigned long long)n, (unsigned long long)left);
    return 0;
}
