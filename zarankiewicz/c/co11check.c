/* co11check.c -- verify a CO_11 seven-multiset the independent way, and apply
 * the mixed bound to that side too.
 *
 * co11min.c computes dbar by relabelling one endpoint to the identity and
 * reading a single precomputed BFS.  That is the step most likely to be wrong,
 * so this programme instead runs a FRESH breadth-first search from each of the
 * seven vertices and reads d(a_i, rev a_j) straight off it.  No relabelling, no
 * rank arithmetic on the query path.
 *
 * It then applies PROOF_223.md's mixed bound on the seven-star side, where
 * every clamp is a theorem with no open cases: cr(K_{k,11}) = Z(k)*Z(11) for
 * k <= 6 is Kleitman 1970, so
 *      clamp[2..6] = 0, 25, 50, 100, 150
 * and crossings >= antisum + max over subsets of (clamp - antisum(subset)).
 *
 *   cc -O2 -o co11check c/co11check.c && ./co11check v1 v2 v3 v4 v5 v6 v7
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define K 10
#define NV 3628800
#define M7 7
static const int FACT[11] = {1,1,2,6,24,120,720,5040,40320,362880,3628800};
/* cr(K_{k,11}) = Z(k)*Z(11) for k <= 6 (Kleitman); index 7 is the open case. */
static const int CLAMP[8] = {0,0,0,25,50,100,150,-1};

static uint8_t *dist;
static int32_t *q;

static void unrank(int r,int*p){int a[K],i,j,n=K;for(i=0;i<K;i++)a[i]=i+1;
 for(i=0;i<K;i++){int f=FACT[n-1],k=r/f;r-=k*f;p[i]=a[k];for(j=k;j<n-1;j++)a[j]=a[j+1];n--;}}
static int rank_of(const int*p){int a[K],i,j,n=K,r=0;for(i=0;i<K;i++)a[i]=i+1;
 for(i=0;i<K;i++){for(j=0;j<n;j++)if(a[j]==p[i])break;r+=j*FACT[n-1];for(;j<n-1;j++)a[j]=a[j+1];n--;}return r;}

static void bfs_from(int src){
 int p[K],t[K],i;memset(dist,0xff,(size_t)NV);dist[src]=0;
 long long h=0,tl=0;q[tl++]=src;
 while(h<tl){int u=q[h++],du=dist[u],w;unrank(u,p);
  for(i=1;i<=9;i++){memcpy(t,p,sizeof t);int a=t[i-1];t[i-1]=t[i];t[i]=a;w=rank_of(t);
   if(dist[w]==0xff){dist[w]=du+1;q[tl++]=w;}}
  for(i=0;i<K-1;i++)t[i]=p[i+1];t[K-1]=p[0];w=rank_of(t);
  if(dist[w]==0xff){dist[w]=du+1;q[tl++]=w;}
  t[0]=p[K-1];for(i=1;i<K;i++)t[i]=p[i-1];w=rank_of(t);
  if(dist[w]==0xff){dist[w]=du+1;q[tl++]=w;}}}

static int rev_of(int v){int p[K],t[K],i;unrank(v,p);
 for(i=0;i<K;i++)t[i]=p[K-1-i];return rank_of(t);}

int main(int argc,char**argv){
 if(argc<1+M7){fprintf(stderr,"give seven CO_11 vertex ids\n");return 2;}
 int v[M7],i,j;
 for(i=0;i<M7;i++){v[i]=atoi(argv[1+i]);if(v[i]<0||v[i]>=NV){fprintf(stderr,"out of range\n");return 2;}}
 dist=malloc(NV);q=malloc((size_t)NV*4);
 int W[M7][M7];
 for(i=0;i<M7;i++){
  bfs_from(v[i]);
  for(j=0;j<M7;j++) W[i][j]=dist[rev_of(v[j])];
 }
 int bad=0;
 for(i=0;i<M7;i++)for(j=0;j<M7;j++) if(W[i][j]!=W[j][i]) bad=1;
 printf("dbar matrix%s symmetric\n", bad?" NOT":"");
 printf("dbar(a_i,a_i):");
 for(i=0;i<M7;i++) printf(" %d",W[i][i]);
 printf("   [must all be 25 = Z(11)]\n");
 int T=0;
 for(i=0;i<M7;i++)for(j=i+1;j<M7;j++) T+=W[i][j];
 printf("antisum over the 21 pairs: %d\n",T);
 printf("pairwise dbar:\n");
 for(i=0;i<M7;i++){printf("  ");for(j=0;j<M7;j++)printf("%3d",W[i][j]);printf("\n");}
 /* mixed bound on this side: all 2^7 subsets, clamps from Kleitman */
 int anti[1<<M7],lb[1<<M7],s,best=0,bk=0;
 for(s=0;s<(1<<M7);s++){
  int a=0;
  for(i=0;i<M7;i++) if(s>>i&1) for(j=i+1;j<M7;j++) if(s>>j&1) a+=W[i][j];
  anti[s]=a;
  int c=__builtin_popcount(s);
  if(c>=3&&c<=6){int d=CLAMP[c]-a; if(d>best){best=d;bk=c;}}
 }
 printf("best single-subset deficit: %d at |S| = %d\n",best,bk);
 printf("mixed bound on the seven-star side: %d + %d = %d   [target 225]\n",T,best,T+best);
 /* full counting recursion for completeness */
 for(s=0;s<(1<<M7);s++){
  int c=__builtin_popcount(s);
  if(c<2){lb[s]=0;continue;}
  int vv=anti[s];
  if(c<=6&&CLAMP[c]>vv) vv=CLAMP[c];
  if(c>=4){int tot=0;for(i=0;i<M7;i++) if(s>>i&1) tot+=lb[s^(1<<i)];
           int r=(tot+(c-3))/(c-2); if(r>vv) vv=r;}
  lb[s]=vv;
 }
 printf("counting recursion over all subsets: %d\n",lb[(1<<M7)-1]);
 return 0;}
