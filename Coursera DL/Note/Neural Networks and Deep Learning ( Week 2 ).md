# Neural Networks and Deep Learning ( Week 2 )
整个第二周的第一个任务就是将一个低效的用循环实现的逻辑回归计算图用向量化的形式改写，以提升速率。
## Vectorization
此节阐述了概念并证明了向量化可以显著提升性能。向量化是指将循环操作的向量运算转化为直接的向量运算。可以显著提升性能。

- 内积

```
//a，b 分别为百万数量级的数组，求两个数组的内积

//向量化
c = np.dot(a, b) 
//消耗时间约1.5ms 

//非向量化

for i in range(1000000):
    c += a[i]*b[i]
// 消耗时间约500ms

```

>注意： `np.dot`只有在运算秩为 1 的向量（即数组）的时候，会直接把两个向量直接做内积（因为行向量和列向量并没有区别）
> 对于普通矩阵来说，会遵循矩阵乘法规律

## More Vectorization Examples
一些可以向量化的计算例子。

- 矩阵内元素作为幂指数

```
import numpt as np
u = np.exp(v)
```

完成了从：

$$
v = 
\begin{bmatrix}
	v_1\\
	... \\
	v_n \\
\end{bmatrix}
$$

到：

$$
u = 
\begin{bmatrix}
	e^{v_1}\\
	... \\
	e^{v_n} \\
\end{bmatrix}
$$

的转换。

同样支持向量的还有：

- 对数转换：

```
np.log(v) \\以 e 为底
np.log10(v)\\以 10 为底
```

- 绝对值：

```
np.abs(v)
```

- 比较大小：

```
np.maxium(v, 0)
```

- 乘方：

```
v**2
```

- 倒数

```
1 / v
```

## Vectorizing Logistic Regression

## Vectorizing Logistic Regression's Gradient Output

### 改写过程
基于计算图：
![](media/15325090336943/15325887840529.jpg)

可以写一个低效的实现：

```
// 1. 初始化各变量
J = 0; dw1 = 0; dw2 = 0; db = 0;
// 2. 求导过程
for  i = 1 to m:
    //正向传播
    z = w.T * x[i] + b //假设 x[i] 为第i个样本，列向量
    a = sigmoid(z)
    J += -( y[i]log(a) + (1-y[i])log(1-a) ) // y[i]为第 i 个真值
    //反向
    dz = a - y[i] // dz为单样本导数，即 L 对 z 求导
    //此时 J 并非为代价函数值，同理 J dw db 也都为累加器
    //[ Update: 这里使用了遍历每个 w 来累加的方法，相当于一个 for 循环，可以使用向量化消解]
    dw1 += x[i][0]dz
    dw2 += x2[i][1]dz
    db += dz
J /= m //此时 J 为代价函数值
dw1 /= m 
dw2 /= m
db /= m
```
改写为：

```
// 首先将 m 个样本组织为 nx * m 的矩阵，每一列为一个样本。针对上方计算图 nx 为 2，命名为 X
// m 个真值组织为长度为 m 的行向量 Y
// 权值 w 则初始化为长度为 nx 的列向量，命名为 W
// 偏置 b 为一个数

// 1. 初始化其他各变量
dw = np.zeros((nx,1)); // 将 dw 初始化为容量为 nx 的列向量  
J = np.zeros((m,1)); // 将 J 初始化为容量为 m 的列向量
db = 0;

// 2. 正向传播
Z = np.dot(w.T, X) + b // Z 为 1 * m 的行向量
A = sigmoid (Z) // A 为 1 * m 的行向量
//J = -( np.dot(log(A), Y.T) + np.dot(log(1-A), (1 - Y)) )

// 3. 反向传播
dZ = A - Y // dZ 为 1 * m 的行向量 
dw = 1 / m * np.dot(X, dZ.T) //dw 显然为一长度为 nx 的列向量
db = 1 / m * np.sum(dZ)

// 4. 更新权重
W = W - alpha * dw
b = b - alpha * db

```


## Broadcasting in Python
#### General rules
![](media/15332854384545/15336267376652.jpg)

- 向量加常量，会自动展常量变向量

![](media/15332854384545/15336268073151.jpg)

- 当(m, n) 矩阵和 (1, n)矩阵发生运算，则后者展为(m, n)

![](media/15332854384545/15336269065764.jpg)

- 当(m, n) 矩阵和 (m, 1) 矩阵发生运算，后者展为(m, n)


```
import numpy as np

A = np.array([[56.0, 0.0, 4.4, 68.0],
                   [1.2, 104.0, 52.0, 8.0],
                   [1.8, 135.0, 99.0, 0.9]])

print(A)

// [[ 56.    0.    4.4  68. ]
// [  1.2 104.   52.    8. ]
// [  1.8 135.   99.    0.9]]
 
cal = A.sum(axis=0) //（沿着第0维度求和，即垂直求和，得到每列的和）

print (cal) 

// [ 59.  239.  155.4  76.9]

new_cal = cal.reshape(1,4)

print(new_cal)

// [[ 59.  239.  155.4  76.9]] 数组化为 1 * 4 的矩阵

percentage = 100 * A / new_cal // [ 广播 ] ： 3 * 4 的矩阵 乘上（除以） 1 * 4 的矩阵

print(percentage)

// [[94.91525424  0.          2.83140283 88.42652796]
// [ 2.03389831 43.51464435 33.46203346 10.40312094]
// [ 3.05084746 56.48535565 63.70656371  1.17035111]]

```

## A note on python/numpy vectors
- 秩为 1 的数组

```

import numpy as np

a = np.random.randn(5)
print(a)

// [-1.97883759 -0.28026896  1.16111207  1.2592107   1.28862289]

print(a.shape) 

// (5,) 这是一个秩为 1 的数组
 
print(a.T)

// [-1.97883759 -0.28026896  1.16111207  1.2592107   1.28862289] 
// 转置和本身相同

print(np.dot(a,a.T))

// 8.588690696216716

```

基于以上特殊特性，尽量不要使用这种形状的数组。

作为代替使用：

```
a = np.random.randn(5)
print(a)

/*
[[-2.26039006]
 [ 0.21935117]
 [ 0.36571892]
 [-1.70798974]
 [ 0.42144928]]
 得到一个 5 * 1 的列向量
 */
```

- 断言语句

```
assert(a.shape == (5,1))
```

- reshape 语句

```
a = a.reshape(n, m)
```

## Explanation of logistic regression cost function (optional)














