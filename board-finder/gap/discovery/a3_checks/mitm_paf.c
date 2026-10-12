// C1, C2, C12 checker: meet-in-the-middle search for pairs A,B in {+-1}^n with
// PAF_A(s)+PAF_B(s) = target for all s != 0.
// usage: mitm_paf MODE n target     MODE = gen | sym ;  target = -2 or 2
// Sequences encoded as n-bit ints, bit=1 means -1.  A(0)=+1 fixed (negation leaves PAF unchanged).
// Hash: key = sum_s d_s * R[s] (mod 2^64), d_s = popcount(A xor rot(A,s)), s=1..(n-1)/2 ; PAF(s)=n-2 d_s.
// dA+dB = c := n - target/2 for every s  <=>  keyB = c*sumR - keyA.  Matches are re-verified exactly.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef unsigned long long u64;
static int n, h; static u64 mask, R[64];
typedef struct { u64 key; u64 a; } ent;
static inline u64 rot(u64 a,int s){ return ((a<<s)|(a>>(n-s)))&mask; }
static int cmp(const void*x,const void*y){ u64 a=((ent*)x)->key,b=((ent*)y)->key; return a<b?-1:a>b; }
static u64 keyof(u64 a){ u64 k=0; for(int s=1;s<=h;s++) k+=(u64)__builtin_popcountll(a^rot(a,s))*R[s]; return k; }
int main(int argc,char**argv){
  if(argc<4){fprintf(stderr,"usage\n");return 1;}
  int sym = !strcmp(argv[1],"sym"); n=atoi(argv[2]); int target=atoi(argv[3]);
  h=(n-1)/2; mask=(n==64)?~0ULL:((1ULL<<n)-1);
  u64 seed=88172645463325252ULL; for(int s=0;s<64;s++){ seed^=seed<<13; seed^=seed>>7; seed^=seed<<17; R[s]=seed; }
  u64 sumR=0; for(int s=1;s<=h;s++) sumR+=R[s];
  int c = n - target/2;
  int m=(n-1)/2;
  u64 N = sym ? (1ULL<<m) : (1ULL<<(n-1));
  ent *E = malloc(N*sizeof(ent)); if(!E){fprintf(stderr,"oom\n");return 2;}
  for(u64 x=0;x<N;x++){
    u64 a;
    if(!sym) a = x<<1;
    else { a=0; for(int i=1;i<=m;i++) if((x>>(i-1))&1){ a|=1ULL<<i; a|=1ULL<<(n-i);} }
    E[x].a=a; E[x].key=keyof(a);
  }
  qsort(E,N,sizeof(ent),cmp);
  u64 nsol=0; u64 fa=0,fb=0;
  for(u64 i=0;i<N;i++){
    u64 kb = (u64)c*sumR - E[i].key;
    // binary search lower bound
    u64 lo=0,hi=N; while(lo<hi){ u64 mid=(lo+hi)/2; if(E[mid].key<kb) lo=mid+1; else hi=mid; }
    for(u64 j=lo;j<N && E[j].key==kb;j++){
      u64 a=E[i].a,b=E[j].a; int ok=1;
      for(int s=1;s<=h;s++){ int pa=n-2*__builtin_popcountll(a^rot(a,s)); int pb=n-2*__builtin_popcountll(b^rot(b,s)); if(pa+pb!=target){ok=0;break;} }
      if(ok){ nsol++; if(!fa&&!fb){fa=a;fb=b;} }
    }
  }
  printf("MODE=%s n=%d target=%d  ordered_solutions(A(0)=B(0)=+1)=%llu",sym?"sym":"gen",n,target,nsol);
  if(nsol){ printf("  example A=");for(int i=0;i<n;i++)putchar(((fa>>i)&1)?'-':'+'); printf(" B=");for(int i=0;i<n;i++)putchar(((fb>>i)&1)?'-':'+'); }
  printf("\n"); return 0; }
