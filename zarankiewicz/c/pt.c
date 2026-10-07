/* pt.c -- pseudo-tightness of (4,7)-sets (Woodall 1993, pp. 662-663), in C.
 *
 * The Python reference is theorem6c.py; this is a re-derivation from the same
 * definition, not a port, and it is cross-checked against the Python on real rows
 * (ptcheck -compare).  The definition, for a (4,7)-multiset M' = (e0,e1,e2,e3):
 *
 *   For each of the 6 pairs {ei,ej}, take the label sets of all SHORTEST
 *   ei -> rev(ej) paths in CO_7.  Ground pair xy is FORCED for the pair if it is
 *   in every one of them, POSSIBLE if it is in at least one.  M' is pseudo-tight
 *   iff some N in V(CO_4)^7 (one cyclic order of {0,1,2,3} per ground symbol)
 *   has, for every ground pair x<y, an N[x] -> rev(N[y]) antipath in CO_4 whose
 *   label set L satisfies  FORCED(xy) <= L <= POSSIBLE(xy)  (as sets of M'-pairs).
 *
 * Two observations make it cheap:
 *
 *  (1) FORCED and POSSIBLE need no path enumeration.  Over the BFS DAG from a,
 *        F(v) = AND over DAG predecessors p of ( F(p) | label(p,v) )
 *        P(v) =  OR over DAG predecessors p of ( P(p) | label(p,v) )
 *      give the intersection and the union of the label sets of all shortest
 *      a -> v paths, for every v at once.  720 BFSs build the whole table.
 *  (2) The constraint on (N[x], N[y]) depends only on the pair of 6-bit masks
 *      (FORCED(xy), POSSIBLE(xy)), so it is one of at most 3^6 = 729 relations on
 *      6 x 6, tabulated once.  What is left is a binary CSP on 7 variables with
 *      domain 6, solved by backtracking with forward checking.
 *
 * The antipath family in CO_4 is a parameter.  Pseudo-tightness is monotone in
 * it, so PT_ARBITRARY (any walk) makes sets easiest to call pseudo-tight and is
 * the conservative reading every bound in this repository uses.  PT_TWICE (each
 * label at most twice) is what a good drawing actually produces -- two stars x, y
 * cross on label ab only as xa x yb or xb x ya -- and is reported for comparison.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "cog.h"
#include "pt.h"

uint32_t *PT_F, *PT_P;
int PT_family_size;

static int  lab7[MAXNV][MAXN];             /* label index of each edge of CO_7 */
static int  c4v[6][4], c4adj[6][4], c4lab[6][4], c4rev[6];
static uint64_t Q4[6][6];                  /* bitset over 64 label masks: walks src -> end */
static uint8_t ALLOW[4096][6];             /* [fm*64+pm][u] = mask of v */

static int pairidx(int x, int y, int n)    /* combinations(range(n),2) order */
{
    if (x > y) { int t = x; x = y; y = t; }
    return x * (2 * n - x - 1) / 2 + (y - x - 1);
}

static void build_co4(void)
{
    static const int tails[6][3] = {{1,2,3},{1,3,2},{2,1,3},{2,3,1},{3,1,2},{3,2,1}};
    for (int i = 0; i < 6; i++) { c4v[i][0] = 0; for (int j = 0; j < 3; j++) c4v[i][j + 1] = tails[i][j]; }
    for (int i = 0; i < 6; i++) {
        for (int j = 0; j < 4; j++) {
            int w[4], c[4], z = 0;
            memcpy(w, c4v[i], sizeof w);
            int k = (j + 1) % 4, t = w[j]; w[j] = w[k]; w[k] = t;
            for (int q = 0; q < 4; q++) if (w[q] == 0) z = q;
            for (int q = 0; q < 4; q++) c[q] = w[(z + q) % 4];
            int f = -1;
            for (int q = 0; q < 6; q++) if (!memcmp(c, c4v[q], sizeof c)) f = q;
            c4adj[i][j] = f;
            c4lab[i][j] = pairidx(c4v[i][j], c4v[i][k], 4);
        }
        int w[4], c[4], z = 0;
        for (int q = 0; q < 4; q++) w[q] = c4v[i][3 - q];
        for (int q = 0; q < 4; q++) if (w[q] == 0) z = q;
        for (int q = 0; q < 4; q++) c[q] = w[(z + q) % 4];
        for (int q = 0; q < 6; q++) if (!memcmp(c, c4v[q], sizeof c)) c4rev[i] = q;
    }
}

/* every (end, label-set) reachable from each source under the chosen family */
static void build_walks(int family)
{
    memset(Q4, 0, sizeof Q4);
    PT_family_size = 0;
    int cap = (family == PT_TWICE) ? 3 : (family == PT_DISTINCT ? 2 : 0);
    for (int s = 0; s < 6; s++) {
        if (cap == 0) {                         /* state (v, mask) */
            static uint8_t seen[6][64];
            int st[6 * 64][2], sp = 0;
            memset(seen, 0, sizeof seen);
            seen[s][0] = 1; st[sp][0] = s; st[sp][1] = 0; sp++;
            while (sp) {
                sp--; int v = st[sp][0], m = st[sp][1];
                for (int j = 0; j < 4; j++) {
                    int w = c4adj[v][j], nm = m | (1 << c4lab[v][j]);
                    if (!seen[w][nm]) { seen[w][nm] = 1; st[sp][0] = w; st[sp][1] = nm; sp++; }
                }
            }
            for (int v = 0; v < 6; v++) for (int m = 0; m < 64; m++)
                if (seen[v][m]) { Q4[s][v] |= 1ULL << m; PT_family_size++; }
        } else {                                /* state (v, label counts in base cap) */
            int ns = 1; for (int q = 0; q < 6; q++) ns *= cap;
            uint8_t *seen = calloc((size_t)6 * ns, 1);
            int *st = malloc(sizeof(int) * 2 * 6 * (size_t)ns), sp = 0;
            int pw[6]; pw[0] = 1; for (int q = 1; q < 6; q++) pw[q] = pw[q - 1] * cap;
            seen[s * ns] = 1; st[0] = s; st[1] = 0; sp = 1;
            while (sp) {
                sp--; int v = st[2 * sp], c = st[2 * sp + 1];
                for (int j = 0; j < 4; j++) {
                    int l = c4lab[v][j], cl = (c / pw[l]) % cap;
                    if (cl + 1 >= cap) continue;
                    int w = c4adj[v][j], nc = c + pw[l];
                    if (!seen[w * ns + nc]) { seen[w * ns + nc] = 1; st[2 * sp] = w; st[2 * sp + 1] = nc; sp++; }
                }
            }
            uint8_t got[6][64]; memset(got, 0, sizeof got);
            for (int v = 0; v < 6; v++) for (int c = 0; c < ns; c++) if (seen[v * ns + c]) {
                int m = 0; for (int q = 0; q < 6; q++) if ((c / pw[q]) % cap) m |= 1 << q;
                got[v][m] = 1;
            }
            for (int v = 0; v < 6; v++) for (int m = 0; m < 64; m++)
                if (got[v][m]) { Q4[s][v] |= 1ULL << m; PT_family_size++; }
            free(seen); free(st);
        }
    }
    for (int fm = 0; fm < 64; fm++) for (int pm = 0; pm < 64; pm++) {
        uint8_t *R = ALLOW[fm * 64 + pm];
        for (int u = 0; u < 6; u++) {
            R[u] = 0;
            if (fm & ~pm) continue;
            for (int v = 0; v < 6; v++) {
                uint64_t b = Q4[u][c4rev[v]];
                for (int m = 0; m < 64 && !(R[u] >> v & 1); m++)
                    if ((b >> m & 1) && (m & fm) == fm && !(m & ~pm)) R[u] |= (uint8_t)(1 << v);
            }
        }
    }
}

/* FORCED / POSSIBLE label masks for every ordered pair of CO_7 vertices */
static void build_fp(void)
{
    int nv = CO_NV, n = CO_n;
    for (int u = 0; u < nv; u++) {
        const uint8_t *t = cog_vertex(u);
        for (int j = 0; j < n; j++) lab7[u][j] = pairidx(t[j], t[(j + 1) % n], n);
    }
    PT_F = malloc(sizeof(uint32_t) * (size_t)nv * nv);
    PT_P = malloc(sizeof(uint32_t) * (size_t)nv * nv);
    int *d = malloc(sizeof(int) * nv), *q = malloc(sizeof(int) * nv);
    uint32_t *F = malloc(sizeof(uint32_t) * nv), *P = malloc(sizeof(uint32_t) * nv);
    for (int a = 0; a < nv; a++) {
        for (int v = 0; v < nv; v++) { d[v] = -1; F[v] = 0xFFFFFFFFu; P[v] = 0; }
        int h = 0, tl = 0;
        d[a] = 0; F[a] = 0; q[tl++] = a;
        while (h < tl) {                        /* BFS order is a topological order of the DAG */
            int u = q[h++];
            for (int j = 0; j < n; j++) {
                int w = CO_adj[u][j];
                if (d[w] < 0) { d[w] = d[u] + 1; q[tl++] = w; }
                if (d[w] == d[u] + 1) {
                    uint32_t b = 1u << lab7[u][j];
                    F[w] &= F[u] | b;
                    P[w] |= P[u] | b;
                }
            }
        }
        for (int b = 0; b < nv; b++) {
            int t = CO_rev[b];
            if (d[t] != AD(a, b)) { fprintf(stderr, "pt: distance mismatch\n"); exit(1); }
            PT_F[(size_t)a * nv + b] = F[t];
            PT_P[(size_t)a * nv + b] = P[t];
        }
    }
    free(d); free(q); free(F); free(P);
}

void pt_init(int family)
{
    if (CO_n != 7) { fprintf(stderr, "pt_init: CO_7 only\n"); exit(1); }
    build_co4();
    build_walks(family);
    build_fp();
}

static int csp(uint8_t rel[7][7][6], uint8_t *dom, int i, int *N)
{
    if (i == 7) return 1;
    for (int u = 0; u < 6; u++) {
        if (!(dom[i] >> u & 1)) continue;
        uint8_t nd[7];
        int ok = 1;
        for (int j = i + 1; j < 7; j++) { nd[j] = dom[j] & rel[i][j][u]; if (!nd[j]) { ok = 0; break; } }
        if (!ok) continue;
        if (N) N[i] = u;
        if (csp(rel, nd, i + 1, N)) return 1;
    }
    return 0;
}

int pt4_witness(int a, int b, int c, int d, int *N)
{
    const int e[4] = {a, b, c, d};
    uint32_t F[6], P[6];
    int pi = 0;
    for (int i = 0; i < 4; i++) for (int j = i + 1; j < 4; j++, pi++) {
        size_t k = (size_t)e[i] * CO_NV + e[j];
        F[pi] = PT_F[k]; P[pi] = PT_P[k];
    }
    uint8_t rel[7][7][6];
    int g = 0;
    for (int x = 0; x < 7; x++) for (int y = x + 1; y < 7; y++, g++) {
        int fm = 0, pm = 0;
        for (pi = 0; pi < 6; pi++) { fm |= (int)((F[pi] >> g) & 1) << pi; pm |= (int)((P[pi] >> g) & 1) << pi; }
        const uint8_t *R = ALLOW[fm * 64 + pm];
        for (int u = 0; u < 6; u++) rel[x][y][u] = R[u];
    }
    uint8_t dom[7];
    for (int i = 0; i < 7; i++) dom[i] = 0x3F;
    return csp(rel, dom, 0, N);
}

int pt4(int a, int b, int c, int d) { return pt4_witness(a, b, c, d, NULL); }

/* The fast path the search uses.  A 21-bit label mask is spread into 21 byte
 * lanes (3 x u64, lane g = ground pair g in combinations(range(7),2) order); a
 * (4,7)-set's FORCED masks are then six shifted ORs of its pairs' lanes, in the
 * pair order (0,1),(0,2),(0,3),(1,2),(1,3),(2,3) that pt4_witness uses. */
void pt_expand(uint32_t m, uint64_t out[3])
{
    for (int q = 0; q < 3; q++) {
        uint64_t r = 0, b = (m >> (8 * q)) & 0xFF;
        for (int i = 0; i < 8; i++) r |= ((b >> i) & 1ULL) << (8 * i);
        out[q] = r;
    }
}

int pt4_lanes(const uint64_t fm[3], const uint64_t pm[3])
{
    uint8_t rel[7][7][6];
    int g = 0;
    for (int x = 0; x < 7; x++) for (int y = x + 1; y < 7; y++, g++) {
        int f = (int)((fm[g >> 3] >> (8 * (g & 7))) & 0x3F);
        int p = (int)((pm[g >> 3] >> (8 * (g & 7))) & 0x3F);
        const uint8_t *R = ALLOW[f * 64 + p];
        if (!(R[0] | R[1] | R[2] | R[3] | R[4] | R[5])) return 0;   /* an empty relation */
        memcpy(rel[x][y], R, 6);
    }
    uint8_t dom[7];
    for (int i = 0; i < 7; i++) dom[i] = 0x3F;
    return csp(rel, dom, 0, NULL);
}

/* ------------------------------------------------------------ transversals */
static int packing(const uint16_t *S, int ns)
{
    uint16_t K[64]; int nk = 0;
    for (int i = 0; i < ns && nk < 64; i++) {
        int ok = 1;
        for (int j = 0; j < nk; j++) if (__builtin_popcount(S[i] & K[j]) >= 2) { ok = 0; break; }
        if (ok) K[nk++] = S[i];
    }
    return nk;
}

int pt_feasible(const uint16_t *S, int ns, int k)
{
    if (ns == 0) return 1;
    if (k == 0) return 0;
    if (packing(S, ns) > k) return 0;
    uint16_t R[1024];
    int pos[4], np = 0;
    for (int i = 0; i < 16 && np < 4; i++) if (S[0] >> i & 1) pos[np++] = i;
    for (int x = 0; x < 4; x++) for (int y = x + 1; y < 4; y++) {
        uint16_t pr = (uint16_t)((1u << pos[x]) | (1u << pos[y]));
        int nr = 0;
        for (int i = 0; i < ns; i++) if ((S[i] & pr) != pr) R[nr++] = S[i];
        if (pt_feasible(R, nr, k - 1)) return 1;
    }
    return 0;
}

int pt_tau(const uint16_t *S, int ns, int m, int cap)
{
    (void)m;
    for (int k = 0; k <= cap; k++) if (pt_feasible(S, ns, k)) return k;
    return cap + 1;
}
