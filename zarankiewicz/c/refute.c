/* refute.c -- hunt a straight-line drawing of K_{m,n} below Z(m)Z(n) crossings.
 *
 * EXACT ARITHMETIC, NOT FLOATING POINT.  Points live on an integer grid, so the
 * orientation test is an int64 cross product and every crossing count is exact.
 * A candidate refutation must be checkable without anyone trusting a tolerance,
 * and a search that uses doubles cannot offer that even when it is right.
 * Coordinates are bounded by 2^20, so the cross product is bounded by 2^42 and
 * cannot overflow.
 *
 * WHAT A NEGATIVE RESULT MEANS: nothing about the topological conjecture.
 *   cr(K_{7,11}) <= rcr(K_{7,11}) <= Z(7)Z(11) = 225
 * the upper bound being Zarankiewicz's own rectilinear construction.  A drawing
 * below 225 refutes the conjecture and is self-certifying; finding none leaves
 * the conjecture exactly where it was, because an optimal drawing need not be
 * rectilinear.  This is a lottery ticket with a free negative, run because the
 * ticket is cheap, not because it is likely.
 *
 * The Python version of this search managed about 14 restarts in 1800 s, which
 * is too few to mean anything; the point of the port is restarts, not elegance.
 */
#define _POSIX_C_SOURCE 199309L
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <math.h>
#include <stdint.h>

#define MM 16
#define NN 24
static int M = 7, N = 11;
static long X[MM + NN], Y[MM + NN];      /* first M are the P side, then N */
#define PX(i) X[i]
#define PY(i) Y[i]
#define QX(j) X[M + (j)]
#define QY(j) Y[M + (j)]

static double now(void)
{
    struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

static inline int sgn64(long long v) { return (v > 0) - (v < 0); }

static uint64_t rs;
static inline uint64_t xs(void)
{
    rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs;
}
static inline long urnd(long mod) { return (long)(xs() % (uint64_t)mod); }

static inline int orient(long ax, long ay, long bx, long by, long cx, long cy)
{
    long long v = (long long)(bx - ax) * (cy - ay) - (long long)(by - ay) * (cx - ax);
    return sgn64(v);
}

/* proper crossing of open segments p1p2 and q1q2 */
static inline int crosses(long p1x, long p1y, long p2x, long p2y,
                          long q1x, long q1y, long q2x, long q2y)
{
    int d1 = orient(q1x, q1y, q2x, q2y, p1x, p1y);
    int d2 = orient(q1x, q1y, q2x, q2y, p2x, p2y);
    int d3 = orient(p1x, p1y, p2x, p2y, q1x, q1y);
    int d4 = orient(p1x, p1y, p2x, p2y, q2x, q2y);
    return d1 * d2 < 0 && d3 * d4 < 0;
}

/* crossings of the complete bipartite straight-line drawing.  Two edges (a,i)
 * and (b,j) are compared only when a != b and i != j; edges sharing an endpoint
 * do not cross in a good drawing. */
static long total_crossings(void)
{
    long c = 0;
    for (int a = 0; a < M; a++)
        for (int b = a + 1; b < M; b++)
            for (int i = 0; i < N; i++)
                for (int j = 0; j < N; j++) {
                    if (i == j) continue;
                    if (crosses(PX(a), PY(a), QX(i), QY(i), PX(b), PY(b), QX(j), QY(j))) c++;
                }
    /* NO division by 2.  For a < b and ordered (i,j) with i != j, the edge pair
     * {(a,i),(b,j)} arises exactly once: (a,b,j,i) gives the DIFFERENT pair
     * {(a,j),(b,i)}, and b < a is excluded.  Halving here is what the control
     * caught, reporting 112 = floor(225/2) on the known-optimal drawing. */
    return c;
}

static int Zf(int n) { return (n / 2) * ((n - 1) / 2); }

/* Zarankiewicz's construction, perturbed onto the grid into general position */
static void zarankiewicz(long eps)
{
    for (int i = 0; i < M; i++) {
        long v = (i / 2 + 1) * ((i % 2 == 0) ? 1 : -1);
        X[i] = v * 65536; Y[i] = 0;
    }
    for (int j = 0; j < N; j++) {
        long v = (j / 2 + 1) * ((j % 2 == 0) ? 1 : -1);
        QX(j) = 0; QY(j) = v * 65536;
    }
    if (eps) for (int k = 0; k < M + N; k++) {
        X[k] += urnd(2 * eps + 1) - eps;
        Y[k] += urnd(2 * eps + 1) - eps;
    }
}

int main(int argc, char **argv)
{
    double budget = (argc > 1) ? atof(argv[1]) : 600.0;
    uint64_t seed0 = (argc > 2) ? (uint64_t)atoi(argv[2]) : 1u;
    int iters = (argc > 3) ? atoi(argv[3]) : 60000;
    const long TARGET = Zf(M) * Zf(N);
    const long RANGE = 1 << 20;

    /* control: the construction must count exactly TARGET */
    printf("control: Zarankiewicz at eps =");
    int ctl = 0;
    for (long eps = 1; eps <= 10000; eps *= 10) {
        rs = 12345u;
        zarankiewicz(eps);
        long c = total_crossings();
        printf(" %ld->%ld", eps, c);
        if (c == TARGET) ctl++;
    }
    printf("   (target %ld, %d of 5 exact)\n", TARGET, ctl);
    if (ctl == 0) { printf("CONTROL FAILED\n"); return 1; }
    fflush(stdout);

    rs = seed0 * 2654435761u + 1u;
    long best_overall = TARGET + 1, bestX[MM + NN], bestY[MM + NN];
    long hist[64]; memset(hist, 0, sizeof hist);
    long restarts = 0;
    double t0 = now();

    while (now() - t0 < budget) {
        if (restarts % 2 == 0)
            for (int k = 0; k < M + N; k++) {
                X[k] = urnd(2 * RANGE) - RANGE;
                Y[k] = urnd(2 * RANGE) - RANGE;
            }
        else
            zarankiewicz(RANGE / 16);

        long cur = total_crossings(), best = cur;
        for (int it = 0; it < iters; it++) {
            double T = 2.0 * pow(0.005, (double)it / iters);
            long step = (long)(T * RANGE / 4) + 1;
            int k = (int)urnd(M + N);
            long ox = X[k], oy = Y[k];
            X[k] += urnd(2 * step + 1) - step;
            Y[k] += urnd(2 * step + 1) - step;
            if (X[k] > RANGE || X[k] < -RANGE || Y[k] > RANGE || Y[k] < -RANGE) {
                X[k] = ox; Y[k] = oy; continue;
            }
            long nw = total_crossings();
            double acc = exp(-(double)(nw - cur) / (T > 1e-9 ? T : 1e-9));
            if (nw <= cur || (double)(xs() >> 11) / 9007199254740992.0 < acc) {
                cur = nw;
                if (nw < best) best = nw;
                if (nw < best_overall) {
                    best_overall = nw;
                    memcpy(bestX, X, sizeof X); memcpy(bestY, Y, sizeof Y);
                    printf("  restart %ld  new best %ld  [%.0f s]\n", restarts, nw, now() - t0);
                    fflush(stdout);
                }
            } else { X[k] = ox; Y[k] = oy; }
        }
        if (best < 64) hist[best]++;
        restarts++;
        if (best_overall < TARGET) break;
    }
    double el = now() - t0;

    printf("\n{\"m\": %d, \"n\": %d, \"target\": %ld, \"best\": %ld, \"refuted\": %s,\n",
           M, N, TARGET, best_overall, best_overall < TARGET ? "true" : "false");
    printf(" \"restarts\": %ld, \"seconds\": %.1f, \"restarts_per_s\": %.2f,\n",
           restarts, el, restarts / el);
    printf(" \"iters_per_restart\": %d, \"crossing_evals_per_s\": %.3g,\n",
           iters, restarts * (double)iters / el);
    printf(" \"arithmetic\": \"exact int64 on a 2^20 grid\",\n");
    if (best_overall <= TARGET) {
        printf(" \"best_P\": [");
        for (int i = 0; i < M; i++) printf("[%ld,%ld]%s", bestX[i], bestY[i], i < M - 1 ? "," : "");
        printf("],\n \"best_Q\": [");
        for (int j = 0; j < N; j++) printf("[%ld,%ld]%s", bestX[M + j], bestY[M + j], j < N - 1 ? "," : "");
        printf("],\n");
        memcpy(X, bestX, sizeof X); memcpy(Y, bestY, sizeof Y);
        printf(" \"best_recount\": %ld,\n", total_crossings());
    }
    printf(" \"note\": \"a negative says nothing about the topological conjecture: an optimal "
           "drawing need not be rectilinear, and rcr >= cr.\"}\n");
    return 0;
}
