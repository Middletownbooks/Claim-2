/* co11count.c -- pricing the seven-star sweep on the OTHER side.
 *
 * If min over 7-multisets of CO_11 of the 21-pair antisum is 225, then
 * cr(K_{7,11}) >= 225 and Zarankiewicz holds for K_{7,11}.  Proving it needs the
 * same staircase enumeration this programme ran on CO_7, now on CO_11:
 *
 *   B[7]=223  B[6]=159  B[5]=106  B[4]=63  B[3]=31  B[2]=10
 *
 * (an 11-multiset of antisum T has a k-subset of antisum at most floor(T(k-2)/k),
 * so by prefix-minimality the prefix may be assumed to obey the rung).  S_11 is
 * transitive on V(CO_11), so a_1 = the identity order with no loss, and
 * Stab(a_1) has order 22 (eleven rotations times reversal).
 *
 * This measures the branching: the exact level-2 count, then sampled level-3 and
 * level-4 counts, which is what decides whether the sweep is hours or never.
 *
 *   cc -O2 -o co11count co11count.c && ./co11count [samples] [seed]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define K 10
#define NV 3628800
static const int FACT[11] = {1,1,2,6,24,120,720,5040,40320,362880,3628800};
static const int BR[8] = {0,0,10,31,63,106,159,223};

static uint8_t dist[NV];
static int32_t q[NV];
static uint8_t (*PERM)[K];

static void unrank(int r, int *p){int a[K],i,j,n=K;for(i=0;i<K;i++)a[i]=i+1;
 for(i=0;i<K;i++){int f=FACT[n-1],k=r/f;r-=k*f;p[i]=a[k];for(j=k;j<n-1;j++)a[j]=a[j+1];n--;}}
static int rank_of(const int *p){int a[K],i,j,n=K,r=0;for(i=0;i<K;i++)a[i]=i+1;
 for(i=0;i<K;i++){for(j=0;j<n;j++)if(a[j]==p[i])break;r+=j*FACT[n-1];for(;j<n-1;j++)a[j]=a[j+1];n--;}return r;}

static void bfs(void){int p[K],t[K],i;memset(dist,0xff,sizeof dist);dist[0]=0;
 long long h=0,tl=0;q[tl++]=0;
 while(h<tl){int u=q[h++],du=dist[u],w;unrank(u,p);
  for(i=1;i<=9;i++){memcpy(t,p,sizeof t);int a=t[i-1];t[i-1]=t[i];t[i]=a;w=rank_of(t);
   if(dist[w]==0xff){dist[w]=du+1;q[tl++]=w;}}
  for(i=0;i<K-1;i++)t[i]=p[i+1];t[K-1]=p[0];w=rank_of(t);
  if(dist[w]==0xff){dist[w]=du+1;q[tl++]=w;}
  t[0]=p[K-1];for(i=1;i<K;i++)t[i]=p[i-1];w=rank_of(t);
  if(dist[w]==0xff){dist[w]=du+1;q[tl++]=w;}}}

static void sigma_of(int a,int *sig){int i;sig[0]=0;for(i=0;i<K;i++)sig[PERM[a][i]]=i+1;}

static inline int dbar_with(const int *sig,int b){
 int seq[K+1],c[K+1],t[K],i,z=0;seq[0]=0;
 for(i=0;i<K;i++)seq[i+1]=PERM[b][K-1-i];
 for(i=0;i<=K;i++){c[i]=sig[seq[i]];if(!c[i])z=i;}
 for(i=0;i<K;i++)t[i]=c[(z+1+i)%(K+1)];
 return dist[rank_of(t)];}

/* f[b] = dbar(a, b) for all b */
static void build(int a,uint8_t *f){int sig[K+1],b;sigma_of(a,sig);
 for(b=0;b<NV;b++)f[b]=(uint8_t)dbar_with(sig,b);}

int main(int argc,char**argv){
 int samples=argc>1?atoi(argv[1]):48;
 unsigned seed=argc>2?(unsigned)atoi(argv[2]):7u;
 int p[K];
 PERM=malloc((size_t)NV*K);
 bfs();
 for(int r=0;r<NV;r++){unrank(r,p);for(int i=0;i<K;i++)PERM[r][i]=(uint8_t)p[i];}
 fprintf(stderr,"CO_11 ready\n");
 uint8_t *f1=malloc(NV),*f2=malloc(NV),*f3=malloc(NV);
 build(0,f1);
 long long l2=0;
 int32_t *cand=malloc((size_t)NV*4);
 for(int b=0;b<NV;b++) if(f1[b]<=BR[2]) cand[l2++]=b;
 printf("level 2: %lld vertices with dbar(a1,.) <= %d   (/22 for Stab(a1): about %lld orbits)\n",
        l2,BR[2],l2/22);
 srandom(seed);
 double s3=0; long long n3=0, mx3=0;
 int32_t *keep3=malloc(1<<22);
 long long nk3=0;
 for(int s=0;s<samples;s++){
  int a2=cand[random()%l2];
  build(a2,f2);
  int base=f1[a2];
  long long c=0;
  for(int b=0;b<NV;b++){int v=base+f1[b]+f2[b];if(v<=BR[3]){c++;if(nk3<(1<<20)){keep3[nk3*2]=a2;keep3[nk3*2+1]=b;nk3++;}}}
  s3+=c;n3++;if(c>mx3)mx3=c;
 }
 printf("level 3: %lld level-2 nodes sampled, mean %.1f extensions, max %lld\n",n3,s3/n3,mx3);
 printf("         => level 3 is about %.3g nodes before symmetry\n",(double)l2*s3/n3);
 double s4=0;long long n4=0,mx4=0;
 for(int s=0;s<samples && nk3;s++){
  long long i=random()%nk3;int a2=keep3[i*2],a3=keep3[i*2+1];
  build(a2,f2);build(a3,f3);
  int base=f1[a2]+f1[a3]+f2[a3];
  long long c=0;
  for(int b=0;b<NV;b++){int v=base+f1[b]+f2[b]+f3[b];if(v<=BR[4])c++;}
  s4+=c;n4++;if(c>mx4)mx4=c;
 }
 if(n4) printf("level 4: %lld level-3 nodes sampled, mean %.2f extensions, max %lld\n",n4,s4/n4,mx4);
 return 0;}
