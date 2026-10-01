#ifndef COG_H
#define COG_H
#include <stdint.h>

#define MAXN  13
#define MAXNV 40320          /* (n-1)! for n <= 9 */

extern int CO_n, CO_NV;
extern uint16_t (*CO_adj)[MAXN];
extern uint16_t *CO_rev;
extern uint8_t  *CO_ad;                   /* CO_NV x CO_NV, row-major */
extern uint16_t (*CO_stab)[MAXNV];
extern int CO_nstab;

void cog_init(int n);
void cog_stab_init(void);
int  cog_stab_drop_identity(void);
int  Zfun(int n);

#define AD(a, b) (CO_ad[(size_t)(a) * CO_NV + (b)])

#endif
