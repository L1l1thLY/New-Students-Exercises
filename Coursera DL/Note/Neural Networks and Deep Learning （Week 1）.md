# Neural Networks and Deep Learning （Week 1）
## Logistic Regression as a Neural Network
### Binary Classification
#### 本周要学习的内容
- 不显式使用`for`循环处理m个训练样本
- 前向传播与反向传播

#### 以Logistic Regression为例
逻辑回归是一个一种二元分类算法。课程举例：输入一张图片，算法输出0或1标签，指明图上是不是猫。
#### 术语表
[Deep Learning Course Notation](media/15325090336943/Deep%20Learning%20Course%20Notation.pdf)
### Logistic Regression
logistic回归是一种广义线性回归（generalized linear model），因此与多重线性回归分析有很多相同之处。
它们的模型形式基本上相同，都具有 $w^Tx+b$，其中$w$和$b$是待求参数，其区别在于他们的因变量不同，多重线性回归即$\hat{y}=w^Tx+b$。但这种形式对于二分类来说并不是好的算法，因为无法把输出值规定在 $[0,1]$ 内，来表示一个概率。
而logistic回归则通过函数 $L$ 将 $w^Tx+b$ 对应一个隐状态 $p$ ， $p =L(w^Tx+b)$ ，然后根据 $p$ 与 $1-p$ 的大小决定因变量的值。如果$L$是logistic函数，就是logistic回归，如果L是多项式函数就是多项式回归。 
Logistic函数曲线就是sigmoid曲线。其形式为：
$\sigma(z) = \frac{1}{1+e^{-z}}$
这是一种针对二分类问题的算法。

### Logistic Regression Cost Function
为了优化逻辑回归模型的参数 $w$ 和 $b$ 需要定义一个代价函数。

#### Loss（error）function
适用于单一的优化实例。  
形式为：$L(\hat{y},y)$    
优化目的是使此函数值尽可能小。  

- 不适合用于梯度下降优化算法的平方误差函数：$L(\hat{y},y) = \frac{1}{2}(\hat{y} - y)^2$。
- 更适合的误差函数：$L(\hat{y},y) = - (log\hat{y} + (1-y)log(1-\hat{y}))$，如果 $y=1$，$\hat{y}$ 需要比比较大，反之需要比较小。

#### Cost function
反映参数成本。  
形式为：$J(w,b) = \frac{1}{m} \sum_{i=1}^m L(\hat{y}^{(i)},y^{(i)})$    
训练过程是，寻找$w$，$b$来减少 $J$的整体成本。  
针对上方误差函数得到的代价函数为：
$J(w,b) = - \frac{1}{m} \sum_{i=1}^m [y^{(i)}log\hat{y}^{(i)} + (1-y^{(i)})log(1-\hat{y}^{(i)} )]$
### Gradient Descent
梯度下降整体来说做了一件事情：

```
Repeat {
    w:= w - alpha * dw   //dw 为 J 对 w 求导 
}
```

### Computation graph
一个计算图的图示：
![](media/15325090336943/15325850349520.jpg)


### Derivatives with a Computation Graph
针对以上计算图：

1. 首先求出$\frac{dJ}{dv}$：因为 J = 3 * v，而 v 为11，若 v 提高0.001则，J提高0.003，所以$\frac{dJ}{dv}$为3。
- 然后求出$\frac{dJ}{da}$：因为 a 为5，若提高为5.001，则 J 提高到33.003，所以 $\frac{dJ}{da}$ 为 3
- 并且，若a 增加了0.001，则 v 增加了0.001。

由此可见，a 一旦发生变化，则会逐次影响 v 和 J。即 a→v→J。

可以得到：

$\frac{dJ}{da} = \frac{dJ}{dv}  \times \frac{dv}{da}$ 

此为链式法则。
若任意变量为 `var` 则 $\frac{dJ}{dvar}$起名为 `dvar`  

由此可见：正向传播为计算图求值过程，而反向传播为求导过程。而导数，是通过两个变量的变化量相除得到的。

### Logistic Regression Gradient Descent
![](media/15325090336943/15325886750534.jpg)
基于以上方程，得到计算图：
![](media/15325090336943/15325887840529.jpg)
针对一个样本时：
1. 首先求出`da`：$\frac{dL}{da} = - \frac{y}{a} + \frac{1-y}{1-a}$
2. 然后求出`dz`：针对 sigmoid 函数为$\frac{dL}{dz} = \frac{dL}{da} \frac{da}{dz} = \frac{dL}{da} \times a(1-a)= a - y$
3. 然后求出`dw1` 为`x_1 * dz`。

其他变量同理。

### Gradient Descent on m Examples
考虑 `m` 个样本的情情况，则考虑 Cost function J:
$J(w,b) = \frac{1}{m} \sum_{i=1}^m L(\hat{y}^{(i)},y^{(i)})$   
或写为：
$J(w,b) = \frac{1}{m} \sum_{i=1}^m L({a}^{(i)},y^{(i)})$ 
而：
$a^{(i)} = \sigma(z^{(i)})$  
由此可以得到，实际上把代价函数作为最终变量时，其对于各参数的导数即为多个样本损失函数值对于各参数的导数的平均：
$\frac{d}{w1}J(w, b) =  \frac{1}{m}  \sum_{i=1}^m  \frac{d}{w1} L({a}^{(i)},y^{(i)})$

```
// 1. 初始化各变量
J = 0; dw1 = 0; dw2 = 0; db = 0;
// 2. 求导过程
for  i = 1 to m:
    //正向传播
    z = w * x[i] + b
    a = sigmoid(z[i])
    J += -( y[i]log(a) + (1-y[i])log(1-a) ) 
    //反向
    dz = a - y[i] // dz为单样本导数，即 L 对 z 求导
    //此时 J 并非为代价函数值，同理 J dw db 也都为累加器
    dw1 += x1[i]dz
    dw2 += x2[i]dz
    db += dz
J /= m //此时 J 为代价函数值
dw1 /= m 
dw2 /= m
db /= m

```

 









