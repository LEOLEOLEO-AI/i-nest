# 从智能网卡的产品定义出发，谈谈DPU的投资

> 笔记本: 微信  
> 创建时间: 2021-08-11  

---

智能摘要
面向数据中心不断扩展的背景下，解决效率降低的一个方案。而DPU产品定义的内涵更广，因此DPU面向客户去定制，相比GPU，可能是一条更稳妥的捷径，因为通用化的方案目前还没有被完全定义出来。绑定了客户，就意味着限制了自己的市场规模，对于投资者来讲，意味着项目收益的Upside降低，那么在估值上就需要有一定考虑，因为Upside/本轮估值的比值，应该等于我们的期望收益倍数/项目失败概率。文中所有的版图、Paper均可自行在DPU企业官网，和Google Scholar中找到。
原文约 6714  字   |  图片 18 张  |  建议阅读 14 分钟  |  [评价反馈](https://static.app.yinxiang.com/embedded-web/clipper/#/Evaluating?d=2021-08-11&nu=986bef7e-6df2-4307-9d18-b8f576fb5d10&fr=myyxbj&ud=1bb10ab&v=2&sig=C9B886AD8B96AF2966900CCF9751D1FE)

 


##  从智能网卡的产品定义出发，谈谈DPU的投资 

 软硬件市场智库 **

以下文章来源于Cheney的岛上书店，作者辰睿[

**Cheney的岛上书店**
记录一个投资新人的思考与成长](https://mp.weixin.qq.com/s/wcDnFkxcE3BUzyvq2TNsVg#)


**为您精选硬核ICIT文章**√


 关注公众号，并回复“社群”，加入软硬件交流社群  

DPU最近属实火热，从接触第一个DPU案子到现在，其实也有大半年了。看着这个市场热度逐渐飙升，还是决定沉下来做点研究。

个人智商有局限，以及观点会偏颇，所以本文可能颇有错漏，欢迎交流指正。


本文分几个部分：
1. DPU是什么
2. 从投资角度怎么看DPU产品和技术
3. 从投资角度怎么看DPU的商业模型
4. DPU市场现状


**01**


**DPU是什么**


1


●


DPU的源起


DPU最早源于美国一家初创公司Fungible于2019年推出的产品F1 DPU，该产品第一次定义了DPU这个概念。但是Fungible没有带火DPU，是NVIDIA带火了DPU。2020年4月，NVIDIA以69亿美金的对价，收购了Mellanox，后者2019年的收入为13.3亿美元，净利润2.05亿美元。


从Fungible的官网中，我们可以窥见其对DPU的定义：**面向数据中心不断扩展的背景下，解决效率降低的一个方案。**


The Fungible DPU™ was invented to address the largest inefficiencies in scale-out data centers: the inefficient execution of data-centric computations within server nodes and the inefficient interchange of data among server nodes, while strengthening the reliability and security.


而NVIDIA的定义就更为直白：**DPU是对网络、安全和存储的卸载平台。**


The NVIDIA® BlueField® data processing unit (DPU) ignites unprecedented innovation for modern data centers. By offloading, accelerating, and isolating a broad range of advanced networking, storage, and security services, BlueField DPUs provide a secure and accelerated infrastructure for any workload in any environment, from cloud to data center to edge. BlueField DPUs combine powerful computing, full infrastructure-on-chip programmability and high-performance networking for addressing the most demanding workloads.


**DPU的变迁和数仓的变迁遵循类似的技术演化规律：**这个描述里非常有意思的一点在于，DPU锚向了数据中心计算和存储单元扩张中，低效的缺点。非常有意思，触类旁通的地方在于，和数仓从第一代到第四代变革的规律类似：伴随着计算资源的不断扩张，计算资源本身的要素（计算、存储、通信）总是在不断的耦合和解耦，耦合的过程本质上是下游应用的定义；解耦的过程则是应用的爆发或者架构的重构。


**第一次耦合：**在Intel服务器推出之前，RISC服务器占据了市场60%的份额。基于Risc CPU的服务器厂商的特点在于，其产品是服务器整机+芯片+工作站的一体化模式，这本质是古早服务器对下游应用的集合定义。类似于第一代数仓的共享存储架构。

**第一次解耦：**以Intel最早的服务器Pentium Pro为例，不同于之前的垂类整合的服务器模式，Intel率先开创了服务器芯片平台的商业模式，在芯片端集成了高速缓存芯片、外部总线等，开放服务器生态给其他厂商，芯片端专注于存储、计算和通信的硬件模块。类似于第二代和第三代数仓中，第一次实现存算分离。解耦的过程本质上是，在应用激增的Driver下，将敏感度高的模块（随着应用增长，需求变化大）和敏感度低的模块（随着应用增长，需求变化小）相分离，以便实现随应用的快速扩展。

**第二次耦合：**当高速的模块化扩张达到某个极限时，一定会存在一个更高维度的架构优化方案，即从模块当中再抽象出共性的要素，集合到一个新的单元上。第二次耦合的Driver可能是模块化扩张超过极限后的系统效率降低（类似于DPU的出现于服务器市场），或者是整体计算架构的变革（类似于Cloud-Native的出现于数据仓库）。


以上都是一些关于技术架构变革路径的思考，那么，为什么最近几年DPU这个概念会出现？


**DPU本质上是服务器架构的第二次耦合：**将服务器CPU中分立的计算、网络、存储资源整合到一个单元里，以进行专用计算。促使该过程的核心Driver是数据中心税的急剧增加。


**占据IDC负载30%的数据中心税（Data Center Tax）的构成：**根据Fungible和AWS的统计，Data Center Tax目前占据了服务器CPU计算量的30%。而关于究竟是什么拖累了服务器CPU的效率，即Data Center Tax的核心构成是什么，我目前看到的写的比较完善的是哈佛大学Kanev教授在2015年和2018年发布的两篇文章《Profiling a warehouse-scale computer》和《Efficiency in warehouse-scale computers: a datacenter tax study》。Kanev将数据中心税的来源分解为六个部分，这六部分合计占了服务器中约25%的负载比例。分别为：


**Protobuf management Protobuf 管理：**Protobuf全称Protocol Buffer，是Google提出的一个数据序列化协议，有点像一个二进制的Compiler，将数据包序列化进行传输，读取的时候再进行反序列化。是一个适用于大数据量场景的json或者XML。而Protobuf Management造成的数据中心税，我理解是用于处理Protobuf编解码的计算量。虽然Kanev的Paper是基于Google服务器，但我理解在所有的服务器中，都有数据序列化的工作量。

**Remote procedure calls (RPCs)远程过程调用：**RPC是一个很老的概念，1984年由Birrell在《Implementing remote procedure calls》里提出。是指，如果两条服务器的函数/方法/算法/应用不同，那么服务器A要调用B里的内容，这个过程就是RPC，包括5步：建立连接、寻址、序列化请求、反序列化、返回数据。RPC的计算负载主要来自于寻址、序列化和反序列化。                                          
RPC构成了数据中心税的1/3，其应用范围很广，包括负载平衡，加密和故障检测，这些Task都需要服务器间通信和传输。

**Data movement数据搬运：**这部分我没有特别理解，可能是指通用的数据搬运。这里面两个重要的库函数memcpy和memmove就占据了数据中心税的4-5%。

**Compression数据压缩：**这部分很好理解，在数据传输前后，均有编解码/压缩解压缩的工作。、

**Memory allocation内存分配：**在任务处理的过程中，编译器需要将任务在不同的内存之间进行分配和重分配。但这部分不一定能由DPU来实现，因为内存分配大多是源于基于递归算法的软件，而此类过程较难硬件化。

**Kernel内核：**这部分负载被计入数据中心税是非常有趣的，因为内核本身就是服务器的核心计算单元，本身不应该被计入“Tax”这种概念。但是，Kernel里有相当一部分是用来处理并行计算的调度，这部分内核被归为调度器或者程序机（Scheduler），即使在充分调优之后，该部分负载也占据总负载的5%。（这部分听起来有点像DPU能为GPU做的事情）。


总结来讲，DPU应该核心解决的问题包括：数据传输过程中的压缩/解压缩，序列化/反序列化，RPC，内存分配，多线程调度，和数据搬运本身。


**将数据中心税的内涵向上一层，扩展到商业和成本层面：**对于 24 核的 CPU 服务器，单价是 60 美金/年（我在阿里云官网上看的），以 100G 光模块为例，需要占用 6 个核做计算，每年的成本为 360 美金。这个数字是DPU经济模型的核心指标。


2


●


现行DPU的解决方案


整体来看，DPU的方案分为两部分（Intel的IPU可能不应该被单独列为一个解决方案）：FPGA和ASIC/SoC。


**FPGA方案：**如果要解决30%的Datacenter Tax，最简单的方法就是增加算力，并且简单化的加速某些特定应用。最简洁的方案就是FPGA。这里面的玩家包括Xilinx，Altera和Mellanox（早年也有FPGA方案）。


**SoC/Asic方案：**这也是目前DPU的主流形态，或者说未来的形态。但做一颗SoC的前提是定义一颗SoC，以及有一个能承载SoC的大市场。


**FPGA方案很难从架构上做分析，我们主要关注ASIC和SoC路线。**由于目前国内DPU厂商都还没有成熟的产品推出，我们选取几家代表性的国外厂商：Fungible、Netronome（FPGA方案）、Pensando（FPGA方案）、Mellanox（NVIDIA）、Broadcom、AWS。


从性能指标上来看：


从性能指标的对比上，我们可以看出以下特点：


要达到更高的传输速率和主频，功耗必然大幅上升；
**DPU属于大核：**以Mellanox为例，16颗A78的主频可以达到48Ghz（经朋友指正，此处表述并不严谨）
主流DPU均搭载了完善（至少表面上是）的软件开发平台。

我们从架构上对Fungible的产品和NVIDIA的产品进行对比：


**Fungible和NVIDIA的架构类似：**传输协议,处理器，加速器，存储。

**上层接入光模块，下层接入服务器：**从工作流上来讲（这里不一定对），Fungible板块上的Data Threads和ConnectX7类似，承担NIC的作用，与光模块通信；PCIE端则负责与服务器通信。

**中间层有大量的硬件加速单元：**两个产品的版图上均放置了大量的硬件加速单元，面向网络处理中各种典型计算，NVIDIA的版图上画的更清晰，包括Crypto和Sha-256，Reg-EX正则表达式，TRNG硬件随机数生成器等。

**在硬件加速单元之外，两者均有通用计算核：**这部分CORE一方面是承担前文说的，数据中心税的工作量。另一部分，应该也是为了承担硬件加速单元溢出的工作量，但这两部分的占比不得而知。


**02**


**从投资角度来看DPU的产品和技术定义**


由于所学专业的原因，我甚至在读研期间都没有这么认真的看过Harvard的paper。不过研究的目的最终还是辅助投资决策，虽然可能我看了这么久，对网络芯片、服务器依然很外行，但我们依然需要硬着头皮去接近一个结论：DPU产品应该怎么做，以及，怎么去判断一个DPU项目。


1


●


DPU产品的最终长相应该是什么样子


下图是一个经典的服务器网络架构：


**服务器计算架构分为六个部分：**图中是两台服务器，因为在服务器计算场景中，经常需要服务器之间的信息交换，也对应到DataCenter Tax里的RPC。这里有六个组成部分：


DPU的最终目的是让Host CPU更纯粹，而这里分为三个层次：


**做一颗DMA-Plus：**从服务器架构上来讲，DMA本身就是一颗小的DPU，因为它帮Host CPU处理了一些简单的网络工作（姑且这么理解）。那简单一点将DMA做大，固化一些通用逻辑、网络协议，理论上也是可行的。这就是传统的FPGA方案在做的事情，本质上，它并没有架构上的革新，或者我们激进一点讲，他就是一颗外挂的Host CPU。而这种方案注定是会被淘汰的，因为它涉及到一个Co-Processor的基础逻辑：一颗协处理器没有大的架构变革下，相比集中处理器，功耗一定是提升的；
**从上文Fungible和Mellanox的架构对比上，其实Fungible就有点类似于DMA-Plus：**因此也一直有业内人士质疑Fungible产品的可用性。从架构上看，对于Accelerator究竟要加速什么东西，Fungible至少在版图上没有清晰的定义，但NVIDIA的定义就清晰很多，可以看到很多具体的硬件加速单元；
**做一颗充分定义化的DPU：**Mellanox Bluefield算是一个还不错的方案，对于需要加速的模块，定义的非常清楚，并且基于NVIDIA强大的系统级研发实力，其对LPDDR5的应用，BF3是非常强的解决方案。但是NVIDIA的局限可能就是，他必须要把DPU和GPU联动起来，这里可能会涉及到一些非通用的架构，导致其在非GPU场景里的应用有局限。
**真正定义一颗通用的DPU：**一个真正的DPU应该长成什么样子，可能是下面这样：把Host CPU里除了APP，就是上面的黑圈之外，其他的（下面的黑圈）都完全卸载到DPU里，这样，Host CPU只需要处理服务器应用就可以。这个就需要非常强大的产品定义，和硬件实现能力。如果能实现到这一部分，就相当于把服务器进一步标准化（之前的服务器也是标准化的，但是网络模块还没有标准化），把用户地址和内核地址的存储/计算，VMware，总线全部集成或者连接到DPU上面，让服务器只承担计算功能。


2


●


DPU究竟应该怎么做：


在看DPU的时候，首先有三个观点：


** 产品定义比技术实现更重要：**DPU一定要有十分清晰的产品定义，因为DPU很容易就定义成Fungible和Mellanox那种，他也叫DPU，从逻辑上是没有问题的，但是这个产品有可能不是最终的、或者说最通用的解决方案。
**DPU和GPU完全不同：**大家都把DPU叫做数据中心第三颗大芯片，和GPU、CPU并称。但同样大热的DPU和GPU是完全不同的。两者的核心区别在于，他们的应用对象不同。GPU无论是应用于什么终端场景，底层就是相对单一的卷积和矩阵乘，虽然GPU难度也很大，但相比DPU复杂的计算种类，其技术实现至少有迹可循；另一方面，GPU应该具有的功能是已经被清晰定义了的，Graphic CORE的公司已经存在好多年了，某种程度上，一颗GPU产品需要做什么，总是有先例可循，即使有一些ASIC方案的云端芯片，也只是做了一些小程度的创新定义，比如瀚博。但DPU目前还没有被清晰定义。
**DPU的Timing本身就在未来：**从核心的经济账来看，DPU作为芯片本身肯定是很贵的（在出货量很少的情况下），因此，如果IDC数据传输速率慢，其实DPU的经济账是算不过来的，因为低速传输的计算负载没有那么大。我们大概了解到的情况是，光模块传输速率200G是一个很关键的节点。超过这个标准，DPU的必要性就大大增加。而国内目前其实200G的渗透率还不高。


因此，DPU应该怎么被定义？这里分为三层，场景——功能——性能。**一个产品的定义，本质上是从面向的场景出发，确定产品的功能，之后再进行系统设计，由各方面的性能指标来实现定义的功能。**


**第一：应用场景定义：**

要回答这个问题，首先要穿过DPU需要卸载的工作实质，去看到最终端的应用。以NVIDIA的产品应用场景为基准，综合其他市场信息，DPU下游的场景包括几部分：


在这四个核心场景里，存储/计算是应用于IDC中，也是DPU给市场讲的最Attractive的故事。除了这部分之外，边缘计算是长期来看DPU最有想象空间的部分。而安全和纯网络通信加速，则是DPU当前可以应用的方向。作为一个DPU产品，其终端究竟定义给哪个应用，又针对这个场景做了哪些优化，是非常重要的。


**第二：应用功能定义：**

我们从三个维度来拼接一个DPU产品的功能：一方面是Datacenter Tax的实质，另一方面，我们参照Fungible和NVIDIA的功能。如下图所示：


**第三：产品性能实现：**

这部分有几个特别有意思的指标：
**带宽：**刚刚从Fungible和Mellanox的产品参数里我们看到，他们都号称能实现400G乃至800G，但应用时候的表现其实并不一定。实现高带宽的障碍其实就是两个：一个是算力（算力要做数据传输的计算），一个是内存墙（因为数据传输还是要涉及到和内存的交换）；

**算力：**毫无疑问，DPU是一个大算力、大核的芯片。但是需要考虑到的是，某一款产品的大算力，有可能就是为了弥补他们硬件加速单元和产品定义的不足。因为没有做好对单个硬件加速模块的定义，因此采用高算力核来cover通用性的场景（类似于把Host CPU搬了出来），因此高算力不一定好，甚至可能代表团队产品定义能力的不足。

**功耗：**Fungible F1的功耗是120W。一台Intel SC5600的功耗是600W。一颗DPU就干了服务器功耗的1/5,这个经济账究竟还算不算的过来？

**对协议的支持，以及硬件加速单元的设计：**传统的网卡其实主要支持一种协议，比如Tcp/IP，但智能网卡希望能够支持更多的应用层协议（这个说法其实并不准确，参照OSI/RM模型，应该是包括会话层、表示层和应用层协议）。


**存储：**在DPU里，存储是一个还挺Tricky的参数，用多大的存储，采用什么形式的存储，背后可能都有考虑；

**PCIE/总线：**其传输速率是否能和带宽、存储相匹配。


**03**


**三、从投资角度来看DPU产品的商业模型**


从技术和产品的判断标准上来讲，上一部分已经讲的比较清楚了（比较清楚，但不一定正确）。这一部分从商业逻辑来分析：


**DPU的市场规模：**这个帐算起来其实很有意思，理论上，DPU如果能成为数据中心第三颗芯片，和GPU和CPU齐名，那市场空间非常大。但是如果按照服务器插DPU的逻辑来计算，其实并没有那么性感。2022 年， 100G 及以上光模块占比超过 70% 2019 年中国服务器出货量达到318.6 万台， SmartNIC 单价为 600 美元，芯片单价为 200 美金。则网卡规模为 13.4 亿美金，芯片市场规模为 4.5 亿美金（国内）。这里面有一个很有趣的点，因为服务器市场的销量其实增长没有我们想象的那么快，和应用/数据的增长不成正比。


**DPU本身的经济账：**上文提到过，假如一台服务器一年能省下360美金，那么客户究竟能接受几年的回本周期？产品售价和毛利又是多少？（360美金这个数据不一定正确）；
。


**ASIC本身的经济账：**为什么DPU值得做一颗ASIC？又为什么要做5nm-7nm-12nm？本质上，只有足够多的出货量，才能撑得起一个ASIC的空间。我有一个比较简单的表格来计算这个模型，概况来讲，就是这个市场的出货量要能Cover住mask的费用，并且还能留给芯片厂商足够的毛利率，否则这个市场就撑不起来一颗ASIC。


** 产品和客户的选择：**对于所有企业，选择大客户/中小客户都是一个需要深思熟虑的问题。GPU和DPU不同的地方在于，由于GPU产品定义相对清晰，因此更容易面向应用去设计；而DPU产品定义的内涵更广，因此DPU面向客户去定制，相比GPU，可能是一条更稳妥的捷径，因为通用化的方案目前还没有被完全定义出来。但这背后就是市场规模的Tradeoff。绑定了客户，就意味着限制了自己的市场规模，对于投资者来讲，意味着项目收益的Upside降低，那么在估值上就需要有一定考虑，因为Upside/本轮估值的比值，应该等于我们的期望收益倍数/项目失败概率。So，需要自己去考量。


**04**


**DPU市场现状**


国内目前主要是几家：（这里隐去一些市场非公开信息）


文中所有的版图、Paper均可自行在DPU企业官网，和Google Scholar中找到。

限于本人知识水平和智商，本文中可能有一定疏漏与错误，欢迎指正。

As usual ,欢迎关注科技行业的朋友交流。文章作者就职于就职于光远资本，个人微信号是Garfield_706。

附上一些过往的思考[投资人如何做好管理层访谈？（附管理层访谈问题清单）](http://mp.weixin.qq.com/s?__biz=MzU4MTA3MjQxMw==&mid=2247483749&idx=1&sn=3a8e980f795759b435373dca2e964dca&chksm=fd4c6217ca3beb015f14dc40a6565df4a25654c96541651dd435bb80097bf7caeb01361b4252&scene=21#wechat_redirect)[一万三千字长文——AI芯片投资人应具有的知识储备和投资逻辑](http://mp.weixin.qq.com/s?__biz=MzU4MTA3MjQxMw==&mid=2247483745&idx=1&sn=d549d683edc2a671b5df33db5cca8c18&chksm=fd4c6213ca3beb05a823569a5b2c46c0fa493d3f126b06bfcc182b924e85fe22af012c8dac5a&scene=21#wechat_redirect)[PEVC能力框架构建——从协议条款来反推LDD的尽调要素](http://mp.weixin.qq.com/s?__biz=MzU4MTA3MjQxMw==&mid=2247483708&idx=1&sn=27aeaebb363cda52c4a0134dd7fed83e&chksm=fd4c624eca3beb589193528565d1460e2541c89641efaf58f5a62eebbe4ddf1e4129337b1475&scene=21#wechat_redirect)


**免责声明**
此文内容为第三方自媒体作者发布的观察或评论性文章，所有文字和图片版权归作者所有，且仅代表作者个人观点，与软硬件市场智库无关。文章仅供读者参考，并请自行核实相关内容。


*推 荐*


★[被黄仁勋称为“IT史上最大机会” | 玩法解密](http://mp.weixin.qq.com/s?__biz=MzU1NjcyNzk5OQ==&mid=2247486584&idx=1&sn=7b6ca6c9a913080b2e9f96f91b76fc74&chksm=fbc1e7a8ccb66ebecfd437b0615f9671bf6a8781090ccc7f6723982071b5586ee748670c184f&scene=21#wechat_redirect)
★[“硬通货”DPU进入黄金时代 | 融资频传](http://mp.weixin.qq.com/s?__biz=MzU1NjcyNzk5OQ==&mid=2247487439&idx=5&sn=cb525f062a6897bf7b5c7f1ec4148cbf&chksm=fbc1e41fccb66d09fb9508b7d5337e1b7345c080bb7d29e15d053d614ffb3215aac619aea36f&scene=21#wechat_redirect)
★[DPU/IPU关键价值：云计算的业务和管理分离](http://mp.weixin.qq.com/s?__biz=MzU1NjcyNzk5OQ==&mid=2247487467&idx=2&sn=10863ec57239ca419d2f496009efa7c9&chksm=fbc1e43bccb66d2d79bc9a1498faaa307f2357e9971fbdd74083dffed77f77a09abde1bc8b31&scene=21#wechat_redirect)
★[处理器“三国鼎立”：从CPU、GPU到DPU](http://mp.weixin.qq.com/s?__biz=MzU1NjcyNzk5OQ==&mid=2247486089&idx=1&sn=ade8f90145f5793ed9f20d33757d016c&chksm=fbc1e159ccb6684f762d5f1e82c3aaf66bf2340e5e188da9028b82f3e2ae31065d8d17badac4&scene=21#wechat_redirect)
★[DPU芯片数据中心奇袭Intel，不止英伟达一个](http://mp.weixin.qq.com/s?__biz=MzU1NjcyNzk5OQ==&mid=2247485219&idx=2&sn=b818909b70e27988a762d58feecdb2bd&chksm=fbc1ecf3ccb665e589a851bd79d47c808709dd5412dacbfec5a245f06f924180564ca68e178f&scene=21#wechat_redirect)
★[Fungible DPU：一种新的处理器类型](http://mp.weixin.qq.com/s?__biz=MzU1NjcyNzk5OQ==&mid=2247486584&idx=2&sn=755c9ba7f1ae16232194f9e8558e6630&chksm=fbc1e7a8ccb66ebe6a0bedcbc406a90edfda06d5a938f0e9f5df32ad7ae7e7d2ec10665905b2&scene=21#wechat_redirect)
★[软硬件融合的时代](http://mp.weixin.qq.com/s?__biz=MzU1NjcyNzk5OQ==&mid=2247484292&idx=1&sn=844602b5a18a9db26b2a08c011b3c4d4&chksm=fbc1e854ccb66142d2cd27426f74a0bbd7c25a1e750a151940d72305c3f4da4a5e41fff7b3f7&scene=21#wechat_redirect)


*END*

---
**Tags:** [[Chiplet]]
