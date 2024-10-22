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

## 神经网络架构
### 输入
+ 尺寸: $(3,16,1)$
+ 是一个包含当前时刻的环境以及在此之前两个时刻的环境的张量
### 卷积层(Convolution2D)
+ filters: 32
+ kernal size: $(1,1)$
+ activation: $ReLu(x)=max(x,0)$
+ padding: same
### 展平层(Flatten)
### 全连接层1(Dense)
+ units: 64
+ activation: $ReLu(x)=max(x,0)$
### 全连接层2(Dense)
+ units: 128
+ activation: $ReLu(x)=max(x,0)$
### 丢弃层(Dropout)
+ rate: 0.5
### 全连接层3(Dense)
+ units: 512
+ activation: $\sigma (x)=\frac{1}{1+e^{-x}}$
### 丢弃层(Dropout)
+ rate: 0.5
### 全连接层4(Dense)
+ units: 64
+ activation: $ReLu(x)=max(x,0)$
### 全连接层3(Dense)
+ units: 6
+ activation: $\sigma (x)=\frac{1}{1+e^{-x}}$
### 输出
+ 输出长度为6的列表，代表六种行为的Q值

## 相关参数
+ $\epsilon_{initial}=0.99$
+ $\epsilon_{min}=0.05$
+ $k=0.998$
+ $\epsilon$更新频率: 4
+ $\gamma=0.3$
+ 主网络训练频率: 4
+ 目标网络更新频率: 40
+ Buffer size:5000
