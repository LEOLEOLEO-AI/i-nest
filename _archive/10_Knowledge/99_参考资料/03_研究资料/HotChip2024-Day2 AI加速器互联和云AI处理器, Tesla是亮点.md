# HotChip2024-Day2: AI加速器互联和云AI处理器, Tesla是亮点

> 笔记本: 我的剪贴板  
> 创建时间: 2024-11-03  

---

原文链接: [https://mp.weixin.qq.com/s/EAfWMqiSkunW3MxOYuJyyQ](https://mp.weixin.qq.com/s/EAfWMqiSkunW3MxOYuJyyQ)


第二日的亮点也很多,特别是Tesla, Tesla的传输协议TTPoE, 借助iWARP的TCP拥塞控制机制和RoCEv1二层转发构建了基于以太网Lossy的转发. 他们这次讲的非常清楚,而且还可以FrontEnd和ScaleOut混跑, 唯一就是多路径上还有点问题要处理一下就好了,  这个话题后面会单独再开一篇来详细探讨.
其它几家的概述如下.
- 
Azure Maia 100 和Meta MTIA这两个云上用的AI加速器
- 
AMD Versal继续在推AIE-ML v2
- 
Cerebras WSE-3,谈了谈部署的集群, 然后架构上没啥变化.然后也开始卷推理服务了
- 
Stanford的稀疏张量处理器Onyx,有点意思, 值得后面单独分析一下
- 
Intel谈了一下CPO
- 
Enfabrica也讲了一下它的Fabric,言之无物的感觉.
- 
针对HPC应用的MN-Core 2有点意思,主要是NOC上的bcast和reduce
- 
CPU则是 Ampere, AMD Zen5, 国内的香山RISC-V等几颗处理器, 后面再单独谈
这次HC2024最想听的就是Nv Blackwell和Telsa TTPoE了, 最后Nv不谈Blackwell微架构一点诚意都没有, 而且自家BF3+SP4 Lossy支持有问题就扯Lossless,完全是扯淡, 是男人就硬干Lossy.
而Tesla则是诚意满满, 从Session题目就点名了A new Lossy Fabric. 开篇就是第一性原理陈述问题

DC Ethernet RDMA有一堆问题, Lossless是垃圾PFC在瞎搞, 然后TCP/IP要过CPU, 内核和软件协议栈开销太大,需要GPU-Direct通信. 然后就缝合了一个Remote DMA over TCP over Ethernet 的缝合怪出来. 这才是第一性原理去解决问题的方式, 而不是天天号称掌握了第一性原理然后又天天到处调研分不清现实是啥. 看看人家Tesla写的多清楚, **TCP got it right- just do it in hardware**


其实这件事情无论Google的Falcon以及DirectTCP-X早就想明白了的...这是正路啊, 各位同学.
本质上就是硬件处理TCP类似的基于Window CC/SACK/快重传这些东西, 然后网络层可选, 底层物理层和数据链路层还是以太网, 一个字节都没改, 什么以太网交换机都可以用. 我真不知道那些天天想着改以太网报文的人在干嘛...

整个事务层和TCP几乎一样, NACK做丢包处理

然后状态机相对于TCP做了简化

协议层很有趣, 像RoCEv1那样直接over在Layer2 Ethernet之上, 然后提供了VC的概念

然后针对Lossy, 像TCP那样搞就行了, 快重传加上, Window based CC.

然后TX控制, 不要交换机和网络来给控制信号

想想渣一直给你们灌输的东西, 下面这个业务目标是非常明确的.


采用Spine-Leaf拓扑, 不用任何框式交换机, 不需要DeepBuffer. **如何不利用交换机任何Hash函数信息, 不需要交换机任何特殊配置, 不启用ECN和PFC. 通过网卡算法自动打散流量,并维持交换网97.5%以上的利用率, 对于交换机的buffer需求为队列深度低于3us.** 并能够针对128:1的时候incast时最大流和最小流量之间的带宽差异小于100Kbps, 同时针对任何网络线缆故障, 通信中断无感知, 模型训练收敛时间小于100ms.
可惜就是不听, 有人说我分不清现实与幻想? 那么天天说第一性原理的Tesla也分不清了?
然后**人家Tesla就要用标准的以太网MAC,其它都不用改, 和渣一样要去薅以太网量大的羊毛.**

它的MAC微架构

然后100G的网卡

你说这玩意和NetDAM是不是同一个东西?


好好看看这图吧

然后人家说从存储捞数据和训练的Backward Pass的Allreduce可以混跑呀, Front-End和Scale-Out可以融合呀

只要用TCP一样的拥塞控制算法, 混跑就行了啊, TCP和TTP一张网~

**不过我也要Diss一下Tesla, 多跳交换机只能做到80%的Fabric利用率, 我们完全解决了多路径Hash冲突的问题, 轻松97.5%**

最后这玩意又要弄到UEC里面去, 估计大家都要把UEC搞黄么? AMD一套方案, 微软一套, 博通一套, Tesla一套, 估计NV还要来一套....有一点当年OpenDayLight的感觉.

# 2. Azure Maia 100

Target应该是OpenAI的推理业务, 然后软件做的很不错, 高密部署很不错, 标准以太网融合ScaleUP和ScaleOut也不错, 但是用RoCE就需要配一个额外的Tile控制器, 和Intel Gaudi3要一个中断管理器一样的缺点.这个后面单独写一篇.

规格来看, 主要是用来推理的, 算力并不是很大

片上架构, 有一个Tile控制核TCP, 类似于Nvidia TMA的(TDMA)配上了, 向量和张量引擎都有

Tensor Core也是16xRx16的, 这个size是合适的, 某些128x128真的太大了,没意思

和Hopper TMA一样, 有Tensor加速, 不过NV用内存屏障,而它用信号量来做
片上网络来看, 2D-Mesh, 然后支持数据压缩挺好的, 很大的Scratch Pad都是这类AI处理器的标配

互联ScaleUp和ScaleOut标准以太网融合好评, 然后RDMA数据加密了好评,毕竟对OAI的推理业务加密很关键.

软件SDK有自己的集合通信库MCCL, 然后支持Triton和底层Maia API, 但是用RoCE就需要配一个额外的Tile控制器, 和Intel Gaudi3要一个中断管理器一样的缺点.

这里详细介绍了一下信号量的控制流程

然后Overlap计算和通信是常规操作, 在网络上传输量化的数据和DeepSpeed Zero++类似

生态兼容很好,两行代码从cuda换maia

通信库中规中矩

# 3. Meta MTIA

先谈业务需求,好评~ 针对搜广推的主业, 模型越来越Dense化,规模越来越大, GenAI/LLM也开始使用.

然后业务目标要优化Perf/TCO和Perf/W, 以及方便支持多个模型和快速开发

功能上的需求

加速器Spec, 没有用HBM,直接用LPDDR5, 成本考虑控制TCO, 功耗90W, FP16 177TFLOPS

架构如下, 8x8的2D-Mesh, 16Channel LPDDR5, onchip 256MB SRAM

控制处理器为4x RISC-V标量处理器, 支持8M L2Cache, 然后PCIe控制器上还有4MB Descriptor SRAM

然后片上网络支持一些组播/广播, 和Hopper的Distribute-Shared-Memory类似

然后计算Core架构如下, 两个RISC-V处理器,一个标量一个向量,配置了矩阵/特殊函数处理,动态量化, 数据动态搬移等协处理器和一个命令处理器和其它block的PE交互

向量采用点积的方式, 支持稀疏矩阵

有384KB的Local的SMEM提高峰值处理能力

动态量化的能力

组播的NOC好评

支持25GB/s的解压缩能力来支撑Embedding Table

数据在NOC上传输也可以压缩解压缩

然后针对推荐系统Embeding的Batch操作和Index aligned DMA/prefetch

单卡双芯片
整机支持12个模块, 单机柜支持3台, 累积72卡

# 4. AMD Versal

主要还是介绍Xilinx搞的AIE-ML, 但是这东西说实话在AMD收购以后发展的并不是很好, Victor Peng也退休了,今天还有一个单独的演讲, 祝好吧~

# 5. Cerebras WSE-3

还是突出自己“大”

讲了一些部署的集群

然后又强调了一次SwarmX和MemoryX构成大的训练集群, 不就是一个超大规模的参数服务器和优化器么

然后估计融资的压力也有的, 开始卷推理了,理由是它内存墙撞烂了


然后解释了为什么并Diss了一下NV

并行放置多个模型也容易, 4个WSE-3就够了

然后开始卖推理服务了

# 6. Intel CPO


有个OCI demo


# 7. Enfabrica

统一ScaleUp和ScaleOut通信是个好事, 但是这家公司还是网党的观点和技术路线, 没啥意思.
原来互联是这样的

然后存在的问题

解法是自己搞一个RPC Domain的Fabric

芯片架构就是一个以太网+PCIe一起的交换机


然后画了一个2层组网524K组网的一个饼

# 8. MN-Core 2

片上多级的broadcast配合MAB的微架构还是有点意思的

PE的架构如下:

多层IR的设计, 感觉有些复杂?

# 9. Stanford Sparse Tensor Accelerator

业务上GNN和稀疏Transformer的需求

E2E的稀疏加速硬件有问题

然后Kernel-Level的稀疏加速也有问题,需要可编程

但是可编程的CGRA又主要针对Dense应用

Onyx搞了一个任意稀疏/密集张量计算的抽象表示

架构是CGRA, 计算和内存节点编排如下

这东西长得有点像神威

稀疏矩阵采用FiberTree表示


后面还有很多内容,熬了两天夜白天还搬砖有点累了, 后面我们会在Tensor系列专题里面介绍Sparse-Tensor的时候详细介绍这一块的内容.

---
**Tags:** [[NaaS]]
