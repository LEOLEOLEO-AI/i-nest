# 一文了解Nvidia GB200 SuperPod NVL576的互联架构

> 笔记本: 我的剪贴板  
> 创建时间: 2025-08-05  

---

大家好我是小咖，之前我们讲过了Nvidia GB200 NVL72单机柜的组网架构，今天来说一下多个NVL72机柜的互联架构。如果对单机柜还不太熟悉的，可以移步至：
[一文带你深入了解Nvidia GB200 NVL72的组成结构](https://mp.weixin.qq.com/s?__biz=Mzk3NTQ1Nzc0Mw==&mid=2247483806&idx=1&sn=5300416cbf92948f092ca5285aefd960&scene=21#wechat_redirect)
[一文超详解Nvidia GB200/GB300 NVL72机柜的组网架构](https://mp.weixin.qq.com/s?__biz=Mzk3NTQ1Nzc0Mw==&mid=2247484139&idx=1&sn=54d44b6ba8f2f7c856207370012d1593&scene=21#wechat_redirect)
所谓多个机柜，最典型的就是GB200 NVL576（8个NVL72机柜）互联。我们先来看看官方的渲染图：

从图中可以看到，前排“镶着金边”的4个机柜和后排有密密麻麻垂直白线的4个机柜，都是GB200 NVL72，剩下的就是电源柜、网络柜等。
我们之前讲过，一台GB200 NVL72机柜有72个B200 GPU和18个NvSwitch芯片，每个B200 GPU支持18通道，每个NvSwitch芯片支持72通道，72*18=18*72，正好是一一对应的，没有多余通道了，那么多个机柜间的SuperPod级互联是怎么做到的呢？

答案非常简单，就是增加NvSwitch芯片来进行Scale out（横向扩展）。

从上图可以看出，GB200 NVL72单机柜版，就是标准的18个计算节点+9个NvLink Switch，而NVL576中的GB200 NVL72机柜则是18个计算节点+18个NvLink Switch。
那么问题来了，我们知道1个GB200 NVL72机柜里18个计算节点+9个NvLink Switch就塞得满满当当了，再往哪放多余的9个NvLink Switch？所以，我们可以使用GB200 NVL72的另一种形态，GB200 NVL36*2。

在GB200 NVL36*2中，NvLink Switch的一半通道用于和本机柜的B200 GPU互联，另一半通道用于和另一个机柜的NvLink Switch互联。这样做理论上会慢一点（经过两次switch），但可以忽略不计。

这个机柜形式存在的本意是降低单机柜的总功率以及提升散热空间，同时也给NVL576互联提供了很好的解决方案。

那么，机柜级的组网画像就是：

有人会问，L1和L2之间的NvLink Switch是怎么连的，除了后面的铜连接，也没看到多余接口啊？

事实上，这个交换机有两种型号，non-scalable NvSwitch tray和scalable NvSwitch tray，即不可扩展的和可扩展的。像上图就是不可扩展的，而可扩展的前端会有18个OSFP光接口。

我们算一下：
（1）36通道对应18个OSFP光接口，那么就是每个光接口需要对应2通道，而每个通道是100GB/s的传输速率，也就是800Gbps，那么光接口就需要满足1.6Tbps的带宽。
（2）一个NVL36机柜上有9个NvLink Switch，一个NvLink Switch上有18个OSFP接口，那么一个NVL36机柜上就是162个OSFP接口，16个NVL36机柜就是2592个OSFP接口，L2层的交换机需要按这个数量去配。
关于这一块，大家可以看一下Semianalysis的原文分析，结合我的解读、你的理解，综合佐证一下。

以上，欢迎大家点赞和关注。