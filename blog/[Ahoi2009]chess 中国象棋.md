# [Ahoi2009]chess 中国象棋

#####Time Limit: 10 Sec  Memory Limit: 64 MB

## Description

　　在N行M列的棋盘上，放若干个炮可以是0个，使得没有任何一个炮可以攻击另一个炮。 请问有多少种放置方法，中国像棋中炮的行走方式大家应该很清楚吧.

## Input

　　一行包含两个整数N，M，中间用空格分开.

## Output

　　输出所有的方案数，由于值比较大，输出其mod 9999973

## Sample Input

　　1 3

## Sample Output

　　7

## HINT

　　除了在3个格子中都放满炮的的情况外，其它的都可以.
　　100%的数据中N,M不超过100
　　50%的数据中，N,M至少有一个数不超过8
　　30%的数据中，N,M均不超过6



# Solution

​	这题的关键在于设置状态。

​	前面的数据范围很容易让人联想到状态压缩，但是这反而不利于解题。

​	考虑题目的本质是什么，其实是求在一个矩阵中放置每行不超过2个、每列不超过2个元素的方案数。

​	还是一行一行地计算，如何记录每列能不能放置一个新的元素？

​	观察到每一列元素的数量只可能是0或1或2，每列元素的数量也有重要意义：如果已有2个，则这列不可再考虑。否则还可以考虑在这行的这列的位置加一个元素。这个状态很方便记录。

​	那就设$f[i][a_1][a_2]$表示当前考虑到第$i$行，有$m-a_1-a_2$列还是空的，有$a_1$列已经有一个元素，有$a_2$列已经放好两个元素。

​	转移也是显然的，因为每行最多放置两个元素，所以一共只有五种简单的转移。每种已有元素相同的列其实本质上是一样的，暴力考虑一下就可以了。



```c++
#include <cstdio>
using namespace std;
const int N=105,MOD=9999973;
int n,m;
int f[N][N][N];
inline int C2(int n){
	if(n<=1) return 0;
	return (1LL*n*(n-1)/2)%MOD;
}
int main(){
	freopen("input.in","r",stdin);
	scanf("%d%d",&n,&m);
	f[0][0][0]=1;
	for(int i=0;i<n;i++)
		for(int a1=0;a1<=m;a1++)
			for(int a2=m-a1;a2>=0;a2--)
				if(f[i][a1][a2]){
					(f[i+1][a1][a2]+=f[i][a1][a2])%=MOD;
					int a0=m-a1-a2;
					if(a1+a2+1<=m)
						(f[i+1][a1+1][a2]+=1LL*a0*f[i][a1][a2]%MOD)%=MOD;
					if(a1+a2+2<=m)
						(f[i+1][a1+2][a2]+=1LL*C2(a0)*f[i][a1][a2]%MOD)%=MOD;
					if(a1>=1)
						(f[i+1][a1-1][a2+1]+=1LL*a1*f[i][a1][a2]%MOD)%=MOD;
					if(a1>=2)
						(f[i+1][a1-2][a2+2]+=1LL*C2(a1)*f[i][a1][a2]%MOD)%=MOD;
					if(a1+a2+1<=m)
						(f[i+1][a1][a2+1]+=1LL*a0*a1%MOD*f[i][a1][a2]%MOD)%=MOD;
				}
	int ans=0;
	for(int a1=0;a1<=m;a1++)
		for(int a2=m-a1;a2>=0;a2--)
			(ans+=f[n][a1][a2])%=MOD;
	printf("%d\n",ans);
	return 0;
}
```



​	