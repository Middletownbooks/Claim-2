/* Stage-1 + stage-2 sieve for the two falsifiable claims.  See sieve.c for
 * the derivations; validated against independent Python at small bounds.
 *
 * conj2:  survivor = q = 0 mod 6 whose a = 4q+1 is covered by NO p_i.
 *   p1 <=> a has a prime factor = 3 mod 4
 *   p3 <=> a has a prime factor = 5 mod 8
 *   p4 <=> a is an odd square
 *   p2 <=> exists x,y,z>=1 with a = 4x(4yz - z - 1) - 4yz + 1; tested for
 *          y,z <= YZ by solving for x (a bounded, not complete, test - so a
 *          survivor is a CANDIDATE, never a refutation).
 *
 * rigid:  survivor = prime p in the six hard classes mod 840 defeating both
 *   cheap witness families:
 *     hed1 at r=3   fails  <=>  (p+3)/4 has a prime factor = 2 mod 3
 *     hshift, q=4a-1 fails <=>  (p+1)/2 has a prime factor = 3 mod 4
 *       [q = 4a-1 divides p+4a iff it divides p+1, since 4a = 1 mod q]
 *   Both are NECESSARY conditions for rigidity, so survivors are a superset
 *   of the rigid primes: an empty survivor set PROVES none exist in range.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static uint32_t *sp; static int nsp;
static void small_primes(uint32_t lim){
    char *c = calloc(lim+1,1); sp = malloc(sizeof(uint32_t)*(lim/4+1024)); nsp=0;
    for(uint64_t i=2;i<=lim;i++) if(!c[i]){ sp[nsp++]=(uint32_t)i;
        for(uint64_t j=i*i;j<=lim;j+=i) c[j]=1; }
    free(c);
}
static uint64_t inv_mod(uint64_t a,uint64_t m){
    int64_t g=m,x=0,x1=1,q,t; int64_t aa=a%m;
    while(aa){q=g/aa;t=g-q*aa;g=aa;aa=t;t=x-q*x1;x=x1;x1=t;}
    return (uint64_t)((x%(int64_t)m+(int64_t)m)%(int64_t)m);
}
static int is_sq(uint64_t v){ uint64_t r=(uint64_t)__builtin_sqrtl((long double)v);
    while(r*r>v)r--; while((r+1)*(r+1)<=v)r++; return r*r==v; }

static int p2_small(uint64_t a,int YZ){
    for(int y=1;y<=YZ;y++) for(int z=1;z<=YZ;z++){
        int64_t den = 4LL*(4LL*y*z - z - 1);
        if(den<=0) continue;
        int64_t num = (int64_t)a + 4LL*y*z - 1;
        if(num>0 && num%den==0 && num/den>=1) return 1;
    }
    return 0;
}
/* first index i>=0 with base + i*stride = 0 (mod p) */
static uint64_t first_idx(uint64_t base,uint64_t k,uint64_t stride,uint64_t p){
    uint64_t r = (base % p + (k % p) * (stride % p)) % p;
    return r ? (p - r) * inv_mod(stride % p, p) % p : 0;
}

int main(int argc,char**argv){
    if(argc<4){fprintf(stderr,"usage: %s conj2|rigid START LIMIT [SEG] [YZ]\n",argv[0]);return 1;}
    int rigid = !strcmp(argv[1],"rigid");
    uint64_t start=strtoull(argv[2],0,10), limit=strtoull(argv[3],0,10);
    uint64_t SEG = argc>4?strtoull(argv[4],0,10):(1u<<21);
    int YZ = argc>5?atoi(argv[5]):40;

    /* iterate over  conj2: a = 1+24k (a<=4*limit+1)    rigid: p = 1+24k (p<=limit) */
    uint64_t stride=24, base=1, maxv = rigid?limit:4*limit+1;
    uint32_t root=1; while((uint64_t)(root+1)*(root+1)<=maxv) root++;
    small_primes(root+1);
    fprintf(stderr,"%s: primes to %u (%d), max %llu, YZ=%d\n",argv[1],root,nsp,
            (unsigned long long)maxv,YZ);

    uint64_t *rA=malloc(SEG*8), *rB=malloc(SEG*8), *rP=malloc(SEG*8);
    unsigned char *hA=malloc(SEG), *hB=malloc(SEG);
    uint64_t k0 = start>base ? (start-base+stride-1)/stride : 0;
    uint64_t kmax = (maxv-base)/stride, tot=0, surv=0;
    FILE*out=fopen(rigid?"surv_rigid.txt":"surv_conj2.txt","w");

    for(uint64_t k=k0;k<=kmax;k+=SEG){
        uint64_t n = (k+SEG-1<=kmax)?SEG:(kmax-k+1);
        for(uint64_t i=0;i<n;i++){
            uint64_t v = base+(k+i)*stride;         /* a  (conj2)  or p (rigid) */
            rP[i]=v;
            rA[i] = rigid ? (v+3)/4 : v;            /* (p+3)/4   or  a          */
            rB[i] = rigid ? (v+1)/2 : 0;            /* (p+1)/2                  */
            hA[i]=hB[i]=0;
        }
        for(int pi=0;pi<nsp;pi++){
            uint64_t p=sp[pi];
            /* --- quantity A --- */
            uint64_t bA = rigid?1:1, sA = rigid?6:24;   /* A = 1 + 6k or 1 + 24k */
            if(sA%p){
                int intA = rigid ? (p%3==2) : (p%4==3 || p%8==5);
                for(uint64_t i=first_idx(bA,k,sA,p);i<n;i+=p){
                    if(rA[i]%p) continue;
                    while(rA[i]%p==0) rA[i]/=p;
                    if(intA) hA[i]=1;
                }
            }
            /* --- quantity B and primality of p (rigid only) --- */
            if(rigid){
                uint64_t bB=1, sB=12;                  /* B = 1 + 12k */
                if(sB%p) for(uint64_t i=first_idx(bB,k,sB,p);i<n;i+=p){
                    if(rB[i]%p) continue;
                    while(rB[i]%p==0) rB[i]/=p;
                    if(p%4==3) hB[i]=1;
                }
                if(stride%p) for(uint64_t i=first_idx(base,k,stride,p);i<n;i+=p)
                    if(rP[i]!=p) rP[i]=0;              /* composite */
            }
        }
        for(uint64_t i=0;i<n;i++){
            uint64_t v=base+(k+i)*stride;
            if(rigid){
                if(!rP[i] || v<2) continue;           /* p composite, or v=1 */
                uint64_t c=v%840;
                if(!(c==1||c==121||c==169||c==289||c==361||c==529)) continue;
                tot++;
                if(rA[i]>1 && rA[i]%3==2) hA[i]=1;
                if(rB[i]>1 && rB[i]%4==3) hB[i]=1;
                if(!hA[i] && !hB[i]){ surv++; fprintf(out,"%llu\n",(unsigned long long)v); }
            } else {
                if(v<25) continue;
                tot++;
                if(rA[i]>1 && (rA[i]%4==3||rA[i]%8==5)) hA[i]=1;
                if(hA[i]) continue;
                if(is_sq(v)) continue;                 /* p4 */
                if(p2_small(v,YZ)) continue;           /* p2, bounded */
                surv++; fprintf(out,"%llu\n",(unsigned long long)v);
            }
        }
        fprintf(stderr,"\r  %llu/%llu tested=%llu surv=%llu",
            (unsigned long long)(k+n),(unsigned long long)kmax,
            (unsigned long long)tot,(unsigned long long)surv);
    }
    fclose(out);
    fprintf(stderr,"\n%s: tested %llu, survivors %llu\n",argv[1],
        (unsigned long long)tot,(unsigned long long)surv);
    return 0;
}
