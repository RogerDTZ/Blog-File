他是$\sum^r_lf_i​$



$g[i][x]=i+1$

$g[i][x\text^1]=g[nex[i]][x\text^1]$

$\begin{aligned}f_i&=0.5*1+0.5*(1+\sum_{j=g[i][wrong]}^{i}f_j)\\&=0.5*1+0.5*(1+f_i+\sum_{j=g[i][wrong]}^{i-1}f_j)\end{aligned}$


$$
\begin{aligned}
	f_i&=0.5*1+0.5*(1+\sum_{j=g[i][wrong]}^{i}f_j)\\
	f_i&=0.5*1+0.5*(1+f_i+\sum_{j=g[i][wrong]}^{i-1}f_j)\\
	
	\frac{1}{2}f_i&=0.5*1+0.5*(1+\sum_{j=g[i][wrong]}^{i-1}f_j)\\
	f_i&=2+\sum_{j=g[i][wrong]}^{i-1}f_j
\end{aligned}
$$
$sum_i=\sum\limits_{j=0}^{i-1}f_j​$



$f_i=2+sum_{i}-sum_{g[i][wrong]}$