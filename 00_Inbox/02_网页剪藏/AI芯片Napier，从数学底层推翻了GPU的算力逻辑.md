---
title: "AI芯片Napier，从数学底层推翻了GPU的算力逻辑"
source: "https://mp.weixin.qq.com/s/cxgS6DXG7rrgsZvIZb7VWA"
author:
  - "[[芝能芯芯]]"
published:
created: 2026-06-26
description:
tags:
  - "clippings"
---
芝能芯芯 芝能智芯 *2026年6月18日 07:58*

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/icDRsboO3nzJh79xbqanE59jmeBI9sFn02UDkDPpBbaiaDKz3wMkRZIeJVjmeMGXib7DTCrVqa1TFdFUf8yuiaqpKg/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0) 芝能智芯出品

AI芯片的军备竞赛，这几年基本上沿着同一条路在跑。晶体管越堆越多，制程越走越小，HBM带宽越拉越高。从H100到B200到GB300，每一代都是在前一代的基础上往大了做。

TensorDyne，一家之前没怎么听过名字的公司，发布了叫Napier的AI推理芯片。这颗芯片没有沿着上面那条路走。回到一百多年前的一本对数表，把AI计算里最耗资源的一道工序重新发明了。

![图片](https://mmbiz.qpic.cn/mmbiz_png/OVjf9zMOS9CdQjCUvLyhhXd7mJfVqFOKUlzfAp0Cg3G1SZojNwkFkzXicqYWQwBwbbmibtTBIKeKeedQvF78phBSPicmcGJWSSpBuW80fSGeMI/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=1)

## Part 1

**四百年前的一本对数表，**

**为什么要被翻出来**

Napier这颗芯片的名字本身就藏着密码。

John Napier，16世纪的苏格兰数学家，对数的发明者。他做对数表的时候有一个朴素的出发点：把乘法变成加法。

两个大数相乘，手工算一次要好几分钟。但如果你先查对数表把两个数转成对数值，把两个对数相加（加法只需要几秒钟），再反查对数表转回去，结果一样，但速度快了几十倍。

这个思路在计算尺时代被用到出神入化，直到电子计算器出现以后才被遗忘。

TensorDyne把四百年前的这条思路捡了回来，用在了AI推理芯片上。

AI推理最吃算力的地方是矩阵乘法。每一层神经网络都在做海量的浮点数乘法。GPU的做法是堆乘法器，乘法器占面积、费功耗、发热量大。

TensorDyne的做法是把对数运算做进了芯片的硬件层。乘法在对数域里变成了加法，加法器比乘法器小一个数量级，功耗低一个数量级。

省出来的硅面积，全给了SRAM。

## Part 2

**一块Napier到底装了什么**

这颗芯片用了台积电3纳米工艺，集成1380亿个晶体管。单芯片算力2.1 Petaflops，加速器核心频率1.33GHz，CPU核心频率1.5GHz。芯片上放了256MB的SRAM。

这个数字单独看可能没什么感觉。做对比的话，TensorDyne自己的说法是，这是NVIDIA Blackwell片上SRAM的5倍。

AI推理的瓶颈已经不在算力了，在数据搬运。GPU花在从HBM往计算单元搬数据上的功耗，常常超过计算本身。SRAM越大，数据就能在离计算单元更近的地方被处理，不用频繁地穿过整个芯片去访问外部内存。

Napier的策略是把乘法器省下来的硅面积，全部换成离计算单元更近的SRAM。

外部内存也没有含糊。每颗Napier配了144GB的HBM3E。加上256MB片上SRAM的深度缓冲，整颗芯片的存算比例是专门为推理场景重新设计的。

架构层面，Napier走了对数数学加脉动阵列加向量处理器的组合路线。对数处理吞吐量，脉动阵列处理矩阵运算，向量处理器处理不规则的计算模式。三条线各自扛各自的负载。

## Part 3

**从一颗芯片到一个机架**

一颗芯片只是起点。TensorDyne把九颗Napier装进一个1RU的计算托盘，九个托盘组成一个TDN72 Pod。一个Pod里面有72颗芯片，总算力68 Petaflops，总HBM内存42TB。四个Pod塞进一个标准52RU机架，功耗120千瓦。

一个很关键的设计选择：全部风冷。120千瓦的风冷机架在密度上已经到了传统风冷的极限，但TensorDyne选择不走液冷路线。

风冷意味着可以用标准数据中心基础设施直接部署，不需要改造机房配电和液冷管路。这对企业客户的部署门槛是一个实际的降压。

芯片之间的互联叫TDN Link，亚微秒级延迟，1TB/s的跨72芯片吞吐量。拓扑上支持任意芯片分组，可以把一部分芯片专门分给某一个超大规模模型，其余的处理其他工作负载。还支持故障转移，一颗芯片出问题不影响其余。

机架网络用的是传统机箱交换机方案。不像NVIDIA NVL72用了定制的背板互联，TensorDyne在机架内走的是标准以太网交换。兼容性更好，但相比NVIDIA的NVLink在带宽和延迟上会有天然劣势。这是一个取舍：用标准化换部署灵活性的取舍。

## Part 4

**一台风冷机架**

TensorDyne放出了自己的性能对比。

针对一个2万亿参数的GPT MoE模型推理，TDN72用一个机架、120千瓦功耗，跑出了每用户1300 tokens每秒。同等吞吐量下，NVIDIA和Groq的方案需要9个机架、1.5兆瓦；AWS和Cerebras的方案需要14个机架、800千瓦。

![图片](https://mmbiz.qpic.cn/mmbiz_png/OVjf9zMOS9ANBQuTXOgD1GDnXC0IkYOsgyZON9y3kmGwWibKHHhlnyFWnv18DkYyQnULBxqpdp7gcXDBVTOS4fwDTsdah2B9dwic9SlFkDtibo/640?wx_fmt=png&from=appmsg#imgIndex=2)

功耗降低约8倍，地板空间节省约6倍。这些数字需要等第三方实测来验证，但方向是清楚的：对数数学省下来的乘法器面积和功耗，在超大参数模型的推理上产生了数量级的效率差。

Napier目标的应用场景也很聚焦。10万亿到20万亿参数的超大规模模型、长上下文推理、智能体工作流和混合专家模型。不是要去替代训练卡，是在推理这个赛道上，用对数数学直接把单位功耗的吞吐量打到一个新的水平上。

TensorDyne给了三条接入路径。Hugging Face上的Model Hub配上SDK，支持PyTorch和Triton的直接编译，还有一个叫tensordyne.nn的嵌入式Python DSL。

硬件好做，软件难做。NVIDIA的CUDA生态不是一两年能追上的。框架层、内核层、分析工具、开发者社区，每一层都是时间堆出来的。任何新的AI加速器要说服客户试用自己的平台，软件路径必须足够简单。

TensorDyne目前给出的三条路径覆盖了从"直接用现成模型"到"手写底层算子"的不同需求，但真实开发者上手以后会发现多少坑，现在谁也说不准。

数值精度是另一个待验证的变量。把乘法换成对数域的加法，中间不可避免会引入近似误差。这个误差在大模型的推理场景下会不会累积到影响输出质量，需要第三方用真实工作负载跑完才能下结论。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/OVjf9zMOS9DjOqtMNic3Dbe1fKzdKAj0k5siaAqWiaaWYIvookhxb4hvM8IdRyF1LXE4NMIWKUpP9iaGSq7kic5ibUWJ0MXywFOePk7ziaqYZn2cPs/640?wx_fmt=png&from=appmsg#imgIndex=3)

时间窗口也是一个实际的变量。Napier现在只是流片完成，Beta测试要等到2027年第一季度，系统出货要等到2027年第二季度末。到那个时候，NVIDIA的下一代架构、Groq的下一代LPU、Cerebras的下一代晶圆级芯片都已经迭代过了。

TensorDyne今天拿出的性能数据，一年后还能不能保持优势，是一个问号。

**小结**

TensorDyne这公司能在AI芯片这个已经被NVIDIA统治了多年的市场里拿到关注，有它站得住脚的原因。大多数AI芯片是设计一颗比NVIDIA跑得更快的GPU。架构思路是跟着NVIDIA走的，在制程或者某些局部模块上做出一点差异。

Napier 从数学底座出发，根本不走传统浮点乘法这条路。对数数学是它的根基，更大的SRAM是这个根基带来的自然结果，风冷机架又是低功耗优势带来的自然延伸。这条路的风险当然有。

软件适配、数值精度、上市时间，每一个都是不好过的关。2027年第二季度能不能按时出货，技术验证能不能经得起客户实测，生态能不能在有限的窗口期里拉到第一批开发者。

**微信扫一扫赞赏作者**