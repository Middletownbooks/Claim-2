#ifndef PT_H
#define PT_H
#include <stdint.h>

/* pt.c -- Woodall's pseudo-tightness of (4,7)-sets, in C.
 * Call cog_init(7) first, then pt_init(family). */

#define PT_ARBITRARY 0   /* any walk in CO_4: the largest family, the conservative one */
#define PT_DISTINCT  1   /* walks with every label at most once                         */
#define PT_TWICE     2   /* walks with every label at most twice (what a good drawing gives) */

extern uint32_t *PT_F, *PT_P;     /* [a*NV+b]: labels in EVERY / in SOME shortest a->rev(b) path */
extern int PT_family_size;        /* sum over src of |{(end, labelset)}|, the published check */

void pt_init(int family);
int  pt4(int a, int b, int c, int d);            /* 1 iff the (4,7)-multiset is pseudo-tight */
void pt_expand(uint32_t m, uint64_t out[3]);               /* 21 bits -> 21 byte lanes */
int  pt4_lanes(const uint64_t fm[3], const uint64_t pm[3]);  /* the same test from lanes */
int  pt4_witness(int a, int b, int c, int d, int *N);  /* same, and writes an N in CO_4^7 */

/* can k pairs of positions meet every set in S (4-element bitmasks, ns <= 1024)? */
int  pt_feasible(const uint16_t *S, int ns, int k);
/* minimum number of pairs meeting every set in S: exact if <= cap, else cap+1 */
int  pt_tau(const uint16_t *S, int ns, int m, int cap);

#endif
