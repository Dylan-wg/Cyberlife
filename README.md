# Cyberlife
Cyberlife: cyber living entity with intelligence based on Deep Q Learning.

## 训练算法

### 深度Q学习(Deep Q Learning, DQL)
$$Q(s,a)=r+\gamma maxQ_{target}(s', a';\theta^-)$$

### $\epsilon-Greedy$策略
$$
action=\begin{cases}
randomly & probability=\epsilon\\
arg maxQ_{a'}(s, a') & probability=1-\epsilon
\end{cases}
$$

$$\epsilon=max(\epsilon_{min}, \epsilon_{initial}\cdot k^t)$$

## 相关参数
+ $\epsilon_{initial}=0.99$
+ $\epsilon_{min}=0.05$
+ $k=0.998$
+ $\epsilon$更新频率: 4
+ 主网络训练频率: 4
+ 目标网络更新频率: 40
+ Buffer size:5000
