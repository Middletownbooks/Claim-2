/* Segmented factor-class sieve for two falsifiable claims.
 *
 * Both targets reduce to the same primitive: over an arithmetic progression,
 * decide for each term whether it has a prime factor in a given residue class.
 *
 * MODE conj2  (Ghermoul, arXiv:2508.07383, Conjecture 2)
 *   Theorem 1 of that paper proves coverage for q odd, q=2 mod 6, q=4 mod 6.
 *   Only q = 0 mod 6 is open, i.e. a = 4q+1 = 1 mod 24.
 *   p1 covers q  <=>  a has a divisor = 3 mod 4  <=>  a has a prime factor
 *                     = 3 mod 4  (a = 1 mod 4, so such factors come in pairs;
 *                     either one alone is a divisor = 3 mod 4).
 *   p3 covers q  <=>  a has a prime factor = 5 mod 8 (then A = that prime,
 *                     B = a/A = 5 mod 8 = 1 mod 4, matching (8y-3)(4x-3)).
 *   So a survivor here has EVERY prime factor = 1 mod 8; only those need
 *   the slow p2 search and the p4 square test.
 *
 * MODE rigid  (Suro-One/auro-zera, axiom good_divisor_exists)
 *   RigidPrime requires hed1: for EVERY r = 3 mod 4 and every d | p(p+r)/4,
 *   NOT r | d+1.  Take r = 3: need no divisor d = 2 mod 3 of M = p(p+3)/4.
 *   M = 1 mod 3 always for these p, and p = 1 mod 3, so this fails - i.e. a
 *   witness exists and p is NOT rigid - exactly when t = (p+3)/4 has a prime
 *   factor = 2 mod 3.  Survivors are rigid-candidates needing deeper search.
 *
 * A survivor is never a proof of anything; it is a candidate promoted to the
 * expensive test.  A non-survivor IS a proof (an explicit witness exists).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static uint32_t *sp;        /* small primes */
static int nsp;

static void small_primes(uint32_t lim) {
    char *c = calloc(lim + 1, 1);
    sp = malloc(sizeof(uint32_t) * (lim / 4 + 1024));
    nsp = 0;
    for (uint64_t i = 2; i <= lim; i++) {
        if (!c[i]) { sp[nsp++] = (uint32_t)i;
            for (uint64_t j = i * i; j <= lim; j += i) c[j] = 1; }
    }
    free(c);
}

/* modular inverse of a mod m, m prime and a not divisible by m */
static uint64_t inv_mod(uint64_t a, uint64_t m) {
    int64_t g = m, x = 0, x1 = 1, q, t; int64_t aa = a % m;
    while (aa) { q = g / aa; t = g - q * aa; g = aa; aa = t;
                 t = x - q * x1; x = x1; x1 = t; }
    return (uint64_t)((x % (int64_t)m + (int64_t)m) % (int64_t)m);
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr,
        "usage: %s conj2|rigid START LIMIT [SEG]\n", argv[0]); return 1; }
    int mode_rigid = (strcmp(argv[1], "rigid") == 0);
    uint64_t start = strtoull(argv[2], 0, 10);
    uint64_t limit = strtoull(argv[3], 0, 10);
    uint64_t SEG   = argc > 4 ? strtoull(argv[4], 0, 10) : (1u << 20);

    /* conj2: terms a = 1 + 24k, want a prime factor = 3 mod 4
       rigid: terms t = 1 +  6k, want a prime factor = 2 mod 3, p = 4t-3     */
    uint64_t stride = mode_rigid ? 6 : 24;
    uint64_t base   = 1;
    uint64_t maxval = mode_rigid ? (limit + 3) / 4 : 4 * limit + 1;

    uint32_t root = 1; while ((uint64_t)(root + 1) * (root + 1) <= maxval) root++;
    small_primes(root + 1);
    fprintf(stderr, "sieving primes to %u (%d primes), maxval %llu\n",
            root, nsp, (unsigned long long)maxval);

    uint64_t *res = malloc(SEG * sizeof(uint64_t));
    unsigned char *hit = malloc(SEG);
    uint64_t k0 = (start > base) ? (start - base + stride - 1) / stride : 0;
    uint64_t kmax = (maxval - base) / stride;
    uint64_t total = 0, surv = 0;
    FILE *out = fopen(mode_rigid ? "survivors_rigid.txt" : "survivors_conj2.txt", "w");

    for (uint64_t k = k0; k <= kmax; k += SEG) {
        uint64_t n = (k + SEG - 1 <= kmax) ? SEG : (kmax - k + 1);
        for (uint64_t i = 0; i < n; i++) { res[i] = base + (k + i) * stride; }
        memset(hit, 0, n);
        for (int pi = 0; pi < nsp; pi++) {
            uint64_t p = sp[pi];
            if (stride % p == 0) continue;
            int interesting = mode_rigid ? (p % 3 == 2) : (p % 4 == 3 || p % 8 == 5);
            /* first index i with base + (k+i)*stride = 0 mod p */
            uint64_t r = (base + k % p * (stride % p)) % p;
            uint64_t i = r ? (p - r) * inv_mod(stride % p, p) % p : 0;
            for (; i < n; i += p) {
                if (res[i] % p) continue;
                while (res[i] % p == 0) res[i] /= p;
                if (interesting) hit[i] = 1;
            }
        }
        for (uint64_t i = 0; i < n; i++) {
            uint64_t v = base + (k + i) * stride;
            if (mode_rigid) { if (v % 6 != 1) continue; }
            total++;
            if (res[i] > 1) {                       /* residual is prime */
                if (mode_rigid ? (res[i] % 3 == 2)
                               : (res[i] % 4 == 3 || res[i] % 8 == 5)) hit[i] = 1;
            }
            if (!hit[i]) { surv++; fprintf(out, "%llu\n", (unsigned long long)v); }
        }
        fprintf(stderr, "\r  ... %llu / %llu  survivors %llu",
                (unsigned long long)(k + n), (unsigned long long)kmax,
                (unsigned long long)surv);
    }
    fclose(out);
    fprintf(stderr, "\n%s: examined %llu terms, %llu survivors (%.4f%%)\n",
            mode_rigid ? "rigid" : "conj2",
            (unsigned long long)total, (unsigned long long)surv,
            100.0 * surv / (total ? total : 1));
    return 0;
}
