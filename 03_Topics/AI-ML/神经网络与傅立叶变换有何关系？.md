---
title: 神经网络与傅立叶变换有何关系？
tags:
- ai-ml
- artificial-intelligence
- chiplet
- deep-learning
- neural-networks
- neuroscience
- paper
---
> 笔记本: 我的剪贴板  
> 创建时间: 2023-09-11  

---

点击上方“**图灵人工智能**”，选择“星标”公众号 
您想知道的人工智能干货，第一时间送达 

 

                             
 

 

 
【导读】大家好，我是泳鱼。一个乐于探索和分享AI知识的码农！ 
机器学习和深度学习中的模型都是遵循数学函数的方式创建的。从数据分析到预测建模，一般情况下都会有数学原理的支撑，比如：欧几里得距离用于检测聚类中的聚类。  
傅里叶变换是一种众将函数从一个域转换到另一个域的数学方法，它也可以应用于深度学习。  
**本文将讨论傅里叶变换，以及如何将其用于深度学习领域。**    
  
**什么是傅里叶变换？**  
在数学中，变换技术用于将函数映射到与其原始函数空间不同的函数空间。傅里叶变换时也是一种变换技术，它可以将函数从时域空间转换到频域空间。例如以音频波为例，傅里叶变换可以根据其音符的音量和频率来表示它。  
我们可以说，任何函数的傅里叶变换所执行的变换都是频率的函数。其中结果函数的大小是原始函数所包含的频率的表示。  
让我们举一个信号的例子，它的时域函数如下所示：  
  
在同一时间范围内获取另一个信号的一部分  
  
将这两个信号的称为 A(n) 和 B(n)，其中 n 是时域。因此，如果我们添加这些信号，信号的结构将如下所示：  
C(n) = A(n) + B(n)  
  
可以看到，函数的信号相加是将两个信号进行了加的操作，如果我们试图从这个相加信号 C 中提取信号 A 或 B，我们会遇到一个问题，因为 这些信号只是功率相加，和时间没有关系。也就是说相加的操作是同一时间上的功率的相加。  
 
*Image from: **https://analyticsindiamag.com* 
可以在上图中看到，频域可以很容易地突出信号之间的差异。如果希望将这些信号转换回时域，我们可以使用傅里叶逆变换。   
**傅立叶变数学原理**  
正弦序列可用于表示时域中的信号，这是傅立叶变换的基础。所以如果函数是一个连续信号，函数f可以用来表示为：  
  
可以看到该函数是由无限正弦曲线相加组成的，我们可以将其视为函数信号的表示，并且该函数具有定义输出信号结构所需的两个系数。  
求解傅里叶变换积分（本质上是频率的函数）会产生这些系数。傅里叶变换的结果可以被认为是一组系数。它可以用数学表示如下： 
 
而这个函数的倒数可以看作是我们用来将频域函数转换为时域函数的时间函数，也就是傅里叶逆变换。 
  
求解上面的这些积分可以得到a和b的值，这里讨论的是信号是连续信号的情况。但是在现实生活中，大多数问题都是从离散采样的信号中产生的，为了找出这种信号变换的系数，我们需要执行离散傅里叶变换 (DFT)。  
使用DFT我们可以得到一个相同长度等间隔的样本序列，这个函数是由一组等间隔的样本序列组成的。上面给出的函数f(t)的系数可以由下面的函数得到。 
 
a 和 b 的值将是，  
  
在函数 f(t) 中使用项 a 和 b，就可以找到频域中的信号。  
**使用 Python 进行傅里叶变换**  
Python 的 scipy 模块提供了数学中所需的所有转换技术，所以可以直接使用它  

 
import numpy as npimport matplotlib.pyplot as pltfrom scipy.fft import fft, fftfreq  
制作正弦波  

 
# sample pointsN = 1200# sample spacingT = 1.0 / 1600.0x = np.linspace(0.0, N*T, N, endpoint=False)sum = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x)plt.plot(sum)plt.title('Sine wave')plt.xlabel('Time')plt.ylabel('Amplitude')plt.grid(True, which='both')plt.show()  
  
上面的输出中，可以看到使用 NumPy 生成的正弦波，现在可以使用 scipy 库的 FFT 模块对其进行转换。  

 sumf = fft(sum)xf = fftfreq(N, T)[:N//2]plt.ylabel('frequency')plt.xlabel('sample')plt.title("FFT of sum of two sines")plt.plot(xf, 2.0/N * np.abs(sumf[0:N//2]))plt.show()  
  
  
现在可以清楚地看到各种波的频率是多少，作为时域的函数形成的时这些并不明显，只有在频域表示时才能清楚的看到这些区别。  
通过上面的介绍已经了解了傅立叶变换的基本内容，但它现在与神经网络有什么关系呢？傅里叶变换是一种逼近其他频域函数的工具，而神经网络也可以逼近任意函数。我们将在本文的下一部分中介绍神经网络和傅里叶变换之间的关系。   
**神经网络和傅里叶变换之间有什么关系？**  
可以将傅里叶变换视为一种有助于逼近其他函数的函数，并且我们还知道神经网络可以被认为是一种函数逼近技术或通用函数逼近技术。  
 
*Image fro**m: **https://analyticsindiamag.com*  
上图描绘了一个采用傅里叶变换方法的神经网络。一个相对基本的神经网络的目标是希望在特定时间逼近一个未知函数及其值。大多数神经网络的任务是学习整个函数或算法或数据中指定的值点处的函数，傅里叶网络也是一样通过迭代技术找到逼近函数的参数。   
**卷积神经网络中的傅立叶变换**  
卷积神经网络中卷积层是主要基础组件，在网络中，任何卷积层的主要工作是将滤波器（卷积核）应用于输入数据或特征图，对前一层的输出进行卷积。该层的任务是学习过滤器的权重。在一个复杂的卷积神经网络中看到，层数很多，每层的过滤器也很多，这使得计算成本非常高。  
使用傅里叶变换可以将层计算转换为频域中的元素乘积，网络的任务将是相同的，但是可以通过使用傅里叶变换来节省计算器的能量。  
综上所述，我们可以说卷积层或卷积层的过程与傅里叶变换有关。大多数时域中的卷积层可以被认为是频域中的乘法。我们可以很容易地通过多项式乘法来理解卷积。  
假设我们必须对任意值 x 的 y 和 g 进行函数处理，如下所示： 
y(x) = ax + b 
g(x) = cx + d 
而这些函数的多项式乘法可以写成函数h 
h(x) = y(x).g(x) 
= (ax + b)(cx + d) 
= ac x² + (ad+bc) x + bd 
综上所述，我们可以说卷积层过程可以定义为上述给定函数的乘积。函数的向量形式可以写成： 
y[n] = ax[n] + b 
g[n] = cx[n] + d 
向量形式的向量乘法为： 
h[n] = y[n] X g[n] 
H[w] = F(y[n]) ‧ F(g[n]) = Y[w] ‧ G[w] 
h[n] = F^-1(H[w]) 
其中： 
- 
乘法中的符号“.”表示乘法，X 是卷积的。
- 
F 和 F^-1 分别是傅里叶变换和傅里叶逆变换。
-  
“n”和“w”分别是时域和频域。   
综上所述，我们可以看到如果函数与时域相关，卷积层最终意味着傅里叶变换及其在乘法中的逆。   
**如何在深度学习中使用傅立叶变换？**  
在上一节中，我们已经看到时域中的卷积过程可以简单地认为是频域中的乘法。这证明它可以用于各种深度学习算法，即使它可以用于各种静态预测建模算法。  
让我们来看一个类似的卷积神经网络示例，这样我们就不会偏离本文的主题。  
卷积数学操作是在时域中执行乘法，而傅里叶变换背后的数学是在频域中进行乘法。  
  
为了在任何卷积神经网络中应用傅里叶变换，我们可以对输入和滤波器进行一些更改。  
如果 CNN 中的输入矩阵和滤波器矩阵可以转换为频域进行乘法运算，并且频域乘法的结果矩阵可以转换为时域矩阵，则不会对算法的准确性造成任何影响。矩阵从时域到频域的转换可以通过傅里叶变换或快速傅里叶变换来完成，而从频域到时域的转换可以通过傅里叶逆变换或快速傅里叶逆变换来完成。  
下图展示了我们如何使用快速傅里叶变换代替卷积。  
  
正如我们所讨论的，在任何复杂的网络中滤波器和层的数量都是非常高的，由于这些数量的增加，使用卷积的计算过程变得非常缓慢。而利用傅里叶变换可以减少这种计算的复杂性，使模型运行速度更快。  
如果你对这篇文章的思路有兴趣可以自行尝试，并欢迎留言讨论。 
*转自：DeepHub IMBA* 
*原作者：Lorenzo Castagno* 
*原文链接：https://medium.com/@lorenzojcducv/how-are-neural-networks-related-to-fourier-transforms-54e0b78e50de* 

**版权声明**  
  转自机器学习算法那些事，版权属于原作者，仅用于学术分享 

   
文章精选： 
- 
[大卫·查尔默斯：大型语言模型预示，不出十年，我们很可能搞出有意识的人工智能](http://mp.weixin.qq.com/s?__biz=MzIyMzk1MDE3Nw==&mid=2247607993&idx=1&sn=eac62053679dc0e507a4ca405f05c851&chksm=e81502b7df628ba1478eba0372a9efe6a756edcc31f16afdee36f04dd818fa69684a66ee8d09&scene=21#wechat_redirect)
- 
[机器学习泰斗迈克尔 · 乔丹的人工智能八问：马斯克并不懂 AI](http://mp.weixin.qq.com/s?__biz=MzIyMzk1MDE3Nw==&mid=2247608707&idx=1&sn=f43f711f80cb1e1f048f2398fe9b735c&chksm=e8150d8ddf62849b46e027ad8e67d0f21cd664111fc1566b55f436ff53b8b4b0876868e58cdb&scene=21#wechat_redirect)
- 
[图灵奖得主杨立昆：生成式AI有点过时了](http://mp.weixin.qq.com/s?__biz=MzIyMzk1MDE3Nw==&mid=2247608831&idx=2&sn=48c6fa62fdb083c1ef9b12f76b79588a&chksm=e8150df1df6284e7357ccf64c572312060fd450ceb23a41eb2d642119ad437e853789a664059&scene=21#wechat_redirect)
- 
[GPT-4没有意识！但图灵奖得主Bengio等88页论文暗示「天网」迟早降临](http://mp.weixin.qq.com/s?__biz=MzIyMzk1MDE3Nw==&mid=2247608831&idx=1&sn=b78a824c27a17aca22b502d37ada4b48&chksm=e8150df1df6284e780b53cbac4419ff513c67e005d206822f7b3c86bcc9bfe45a3c7c83a8371&scene=21#wechat_redirect)
- 
[从计算到人类知识：ChatGPT与智能演化](http://mp.weixin.qq.com/s?__biz=MzIyMzk1MDE3Nw==&mid=2247607662&idx=1&sn=0636f2addf7a985b2a6877c4d0a3c354&chksm=e8150160df6288768d1ef53da63d5bd2ed30f610d5087f945a02ee9d1c1a77410c6ffc91c13d&scene=21#wechat_redirect)
- 
[数学到底有多重要？看看手机背后的数学](http://mp.weixin.qq.com/s?__biz=MzIyMzk1MDE3Nw==&mid=2247607433&idx=1&sn=d74683ff0318ec6d4849dc0f73344967&chksm=e8150087df628991e247beb2aee640fb6a1e7903227bca456a8b1d71b508f70d288735500a7e&scene=21#wechat_redirect)
- 
[图灵奖得主：为什么中国顶尖学生入学赢了，毕业时却输了？](http://mp.weixin.qq.com/s?__biz=MzIyMzk1MDE3Nw==&mid=2247607191&idx=1&sn=1d28d1e797569a144eac1cf1ec494529&chksm=e8150799df628e8fed25f7d6d617203370d7add46993904059ba43e2084d20eef667ac356e8d&scene=21#wechat_redirect)
- 
[人工智能的终极基础是哲学认识论](http://mp.weixin.qq.com/s?__biz=MzIyMzk1MDE3Nw==&mid=2247607153&idx=4&sn=55b07a5083d8069e595c2d98ab64b580&chksm=e815077fdf628e69c3c513ed60d93437cfa115d5bdc2b1c4d28d1daf5431a27005949da0af0b&scene=21#wechat_redirect)
- 
[图灵奖获得者专辑|图灵奖获得者、信息安全常青树Adi Shamir：从密码学到AI对抗性样本研究](http://mp.weixin.qq.com/s?__biz=MzIyMzk1MDE3Nw==&mid=2247606935&idx=3&sn=9cf83c116cc39a70fce51816c27a39d5&chksm=e8150699df628f8fa06829164e35316174f3d36f03f132c97cd5b3f70e7211f38941e8918043&scene=21#wechat_redirect)
- 
[图灵奖获得者专辑|图灵奖得主 Yann LeCun：AI 仅仅学语言走不远](http://mp.weixin.qq.com/s?__biz=MzIyMzk1MDE3Nw==&mid=2247606935&idx=1&sn=8178ece16911e7bbd043884c6758731d&chksm=e8150699df628f8fdb3100064085ca881ea83f854c41bf35a24eb9bd113ba4cace656394e198&scene=21#wechat_redirect)

---
**Tags:** [[NaaS]] [[Chiplet]]
