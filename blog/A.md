# Description

​	![img](http://192.168.102.138/JudgeOnline/upload/attachment/image/20180412/20180412095639_88652.png)

![img](http://192.168.102.138/JudgeOnline/upload/attachment/image/20180412/20180412095639_88652.png)



# Solution

​	我连暴力都不会打我真的是个弱鸡。

​	发现很难合并两条合法的路径，然而我的思维限死了，一直在想怎么点分，判断路径是否合法，连暴力都打不出来。

​	参与运算的是顶点标号，这意味着形如$a_i\rightarrow ka_i$的*危险路径*只有$O(n\;log\;n)$对。不合法的路径，必定经过至少一条*危险路径*。这玩意其实很好算，于是答案就是总路径数减去不合法的路径数。

​	记$dfn[a]$表示$a$的dfs入序，$end[a]$表示$a$的dfs出序。

​	把任意一条路径$a\rightarrow b$看作二维平面上的一个点$(dfn[a],dfn[b])$，现在我们要通过高效的方式将不合法的点标记出来。

​	对于一条危险路径$u\rightarrow v$，考虑任意一条路径$a \rightarrow b$ （$dfn[u]<dfn[v]$且$dfn[a]<dfn[v]$），记$g$为$u$到$v$的路径上第一个碰到的不是$u$的点。

​	若$u$是$v$的祖先，则不合法的路径要么满足$dfn[a]\in[1,dfn[g])$且$dfn[b]\in[dfn[v],end[v]]$，要么满足$dfn[a]\in[dfn[v],end[v]]$且$dfn[b]\in(end[g],n]$。将对应的两个矩形的所有元素标记为不合法。

​	否则更能简单，不合法的路径一定满足$dfn[a]\in[dfn[u],end[u]]$且$dfn[b]\in[dfn[v],end[v]]$。

​	做个矩形求交，用全面积减去矩形总面积就是合法方案数了。（细节除二啊、线段树一个点代表是一条单位边啊之类的注意下就可以了）



```c++
#include <cstdio>
#include <algorithm>
using namespace std;
typedef long long ll;
const int N=100005;
int n;
int h[N],tot,pre[N][18],dep[N];
int dfntm,dfn[N][2];
struct Edge{int v,next;}e[N*2];
struct Data{
	int y,l,r,d;
	Data(){}
	Data(int _y,int _l,int _r,int _d){y=_y;l=_l;r=_r;d=_d;}
}a[N*17*2];
int acnt;
inline void swap(int &x,int &y){x^=y^=x^=y;}
inline int getInt(){
	int x=0,f=1; char c=getchar();
	while(c<'0'||c>'9'){if(c=='-')f=-1;c=getchar();}
	while('0'<=c&&c<='9'){x=x*10+c-'0';c=getchar();}
	return x*f;
}
inline void addEdge(int u,int v){
	e[++tot].v=v; e[tot].next=h[u]; h[u]=tot;
	e[++tot].v=u; e[tot].next=h[v]; h[v]=tot;
}
void predfs(int u,int fa){
	pre[u][0]=fa;
	dep[u]=dep[fa]+1;
	dfn[u][0]=++dfntm;
	for(int i=1;i<=17;i++) pre[u][i]=pre[pre[u][i-1]][i-1];
	for(int i=h[u],v;i;i=e[i].next)
		if((v=e[i].v)!=fa)
			predfs(v,u);
	dfn[u][1]=dfntm;
}
inline int jump(int u,int step){
	for(int i=17;i>=0;i--)
		if((1<<i)<=step)
			u=pre[u][i],step-=(1<<i);
	return u;
}
void createRect(int u,int v){
	if(dfn[u][0]>dfn[v][0]) swap(u,v);
	int g=jump(v,dep[v]-dep[u]-1);
	if(pre[g][0]==u){//u是v的祖先
		if(dfn[g][0]-1>=1){
			a[++acnt]=Data(dfn[v][0],1,dfn[g][0]-1,1);
			a[++acnt]=Data(dfn[v][1]+1,1,dfn[g][0]-1,-1);
		}
		if(dfn[g][1]+1<=n){
			a[++acnt]=Data(dfn[g][1]+1,dfn[v][0],dfn[v][1],1);
			a[++acnt]=Data(n+1,dfn[v][0],dfn[v][1],-1);
		}
	}
	else{//u和v分列两侧
		a[++acnt]=Data(dfn[v][0],dfn[u][0],dfn[u][1],1);
		a[++acnt]=Data(dfn[v][1]+1,dfn[u][0],dfn[u][1],-1);	
	}
}
namespace SEG{
	int rt,sz,ch[N*2][2],cnt[N*2],sum[N*2];
	void build(int &u,int l,int r){
		u=++sz;
		if(l==r) return;
		int mid=(l+r)>>1;
		build(ch[u][0],l,mid);
		build(ch[u][1],mid+1,r);
	}
	inline void pushup(int u,int l,int r){
		sum[u]=cnt[u]?r-l+1:sum[ch[u][0]]+sum[ch[u][1]];
	}
	void modify(int u,int l,int r,int L,int R,int x){
		if(L<=l&&r<=R){
			cnt[u]+=x;
			pushup(u,l,r);
			return;
		}
		int mid=(l+r)>>1;
		if(R<=mid) modify(ch[u][0],l,mid,L,R,x);
		else if(mid<L) modify(ch[u][1],mid+1,r,L,R,x);
		else{
			modify(ch[u][0],l,mid,L,mid,x);
			modify(ch[u][1],mid+1,r,mid+1,R,x);
		}
		pushup(u,l,r);
	}
	int query(){return sum[1];}
}
bool cmp(const Data &a,const Data &b){
	if(a.y!=b.y) return a.y<b.y;
	if(a.l!=b.l) return a.l<b.l;
	return a.r<b.r;
}
int main(){
	n=getInt();
	for(int i=1;i<n;i++){
		int u=getInt(),v=getInt();
		addEdge(u,v);
	}
	predfs(1,0);
	for(int u=1;u<=n;u++)
		for(int v=u*2;v<=n;v+=u)
			createRect(u,v);
	sort(a+1,a+1+acnt,cmp);
	SEG::build(SEG::rt,1,n);
	ll ans=1LL*n*(n+1)/2;
	int lasty=0;
	for(int i=1,j;i<=acnt;i=j){
		ans-=1LL*(a[i].y-lasty)*SEG::query();
		lasty=a[i].y;
		for(j=i;j<=acnt&&a[j].y==a[i].y;j++)
			SEG::modify(SEG::rt,1,n,a[j].l,a[j].r,a[j].d);
	}
	printf("%lld\n",ans-n);
	return 0;
}
```

