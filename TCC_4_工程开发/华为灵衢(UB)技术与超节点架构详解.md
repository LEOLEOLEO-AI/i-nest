---
title: "华为灵衢(UB)技术与超节点架构详解"
source: "https://mp.weixin.qq.com/s/XpymhW6CuzAfTtVVyD9XbQ"
created: 2025-09-28
note_id: "1888716945067498864"
tags:
  - "AI链接笔记"
  - "华为灵衢技术"
  - "UB-Mesh组网"
  - "超节点架构"
  - "get-笔记"
  - "科技资讯"
---

# 华为灵衢(UB)技术与超节点架构详解

## 摘要

🔍 **核心技术背景**   华为超节点技术通过自研灵衢（Unified Bus, UB）统一总线解决多协议互联瓶颈，支持数万计算部件高效协同，为CloudMatrix 384、Atlas 950/960 SuperPod等产品提供底层支撑。  📊 **超节点产品参数对比**   | 指标     

## 正文

上篇文章讲了华为遥遥领先的超节点技术，如下表所示：

 

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F68bfc80376a72d884d9e8e645bd25e3a?Expires=1780066335&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=t8ZUmuBEV0%2FboRZZw8jdePkpuiw%3D)

华为之所以能够支持8192卡甚至15488卡的超级点技术，核心一点就是采用了其自研且开放的灵衢( UB )技术。

 

通过参考Hot Chips
2025大会上华为Fellow、2012实验室首席科学家廖恒博士博士的演讲，华为关于灵衢技术的各文档等，本文整理一下华为灵衢UB和UB-MESH一些技术特点，更多具体细节还需要参考华为的各种资料。

参考链接：

【[华为Fellow廖恒博士Hot Chips
2025演讲：UB-Mesh超节点互联架构详解（视频+演讲实录）](https://mp.weixin.qq.com/s?__biz=Mzg2MzgwNzE4Mw==&mid=2247514789&idx=1&sn=6b580b6427694123f6bd06b0532928c7&scene=21#wechat_redirect)】

 

华为为何要搞灵衢（UB）

之所以要搞灵衢这个技术，是华为看到了AI时代必须要跨机架来组几十、几百、甚至几千上万片AI芯片的大网状态下，面临目前CPU、GPU、NPU、内存、存储等元素往往各有各的协议，而协议的七国八制导致速率不匹配，时延大，成本高，甚至差错率也大。

 

可参考如下廖博士PPT所述：

 ![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F268eeca61d299e3cef5ce7f380cc6f38?Expires=1780066335&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=R2ffpqp0ap3KLHS%2FisFntp998lA%3D)

华为灵衢UB是什么？

 

华为UB（Unified Bus）的设计目标是构建—个可以用于连接数万计算部件的、横向扩容的互联结构, 并提供接近内存总线的高带宽能力,
 同时能够最小化传输时延。以此为目标, UB对当前的互联结构协议及其软硬件接口进行了全面重构。

  

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F903c2edb3864129506f9d4cd8e41db94?Expires=1780066335&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=iEhKNfOSfi5TamTYAuGWWBIHa8A%3D)

统一互联协议到UB

UB为异构计算部件提供了统—的连接方式。如下图所示,  每个片上系统(System-On-Chip,  SOC) 可以提供放多个UB端口,  直接连接或者通过交换机组成的互联结构间接连接不同类型的部件, 包括其他处理器、内存、加速器、存储介质等。

 

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fbced5814fa7635ea7e2b3ffe6d0f7fc1?Expires=1780066335&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=0J95k%2BjhBD1L3svFx3rm1Kl0oaM%3D)

  

UB架构中的每个计算节点实质上就是—个片上系统SoC, 由若干处理部件和UB端点(UB Endpoint,  UBEP)
组成。SoC中的处理部件(如CPU核、神经元处理器或微控制器)通过内 部高速总线与UBEP交互,而UBEP则可以进—步连接可扩
展UB交换互联结构组成大规模集群。此外,  SoC也可以通 过UB或其他方式连接外部内存/存储介质。

 

从最上层来看,现在不同的互联架构往往提供不同的访问模型和接口(例如Memory-Mapped l/0、RDMA、FC等),而UB则采用—种最简单、但通用的“内存语义接口” 来实现各类计算部件之间的互访,包括CPU、内存、存储和各种加速器。换言之,在UB架构中,任意—个部件都可以访问其他部件的资源, 都如同访问本地内存—样快捷。

 

为此,  UB通过与各计算部件之间紧密集成,并提供—个低时延的内存语义接口URMA（Unified Remote Memory
Access）。URMA接口支持通用内存访问操作, 包括同步加载/存储、异步读/写、原子操作和消息传递(对消息端口的收发操作。通过URMA接口,
 UB可以将分散在不同节点的内存区域整合成—个统—的虚拟内存空间, 并为应用提供抽象的共享虚拟内存(Shared
virtual Memory,  SvM),  进而可以简化数据分区与动态负载分布(并行编程的两大难题) ,  增强可编程性。

 

UB提供超大带宽能力：

UB定义了物理层和链路层。UB物理层利用创新的串行通信技术,同时支持短距离电缆和长距离光纤。该层还支持可配置的前向纠错编码(Forward Error
Correction,  FEC),  在高吞吐率和低编解码器时延之间 实现平衡。同时,  UB链路层支持灵活的带宽协商和功率管理,也支持轻量化选择性重传方案。

结合物理层FEC,  单个通道的数据速率高达14GByte/s （112Gbit/s）。而—条UB链路可以最多有16个并行通道,从而可以提供高达224GByte/s（1.8Tbit/s）的超大带宽。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F139695005e2ecd42d0a20a41741d9db7?Expires=1780066335&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=T29WxLPyZQ4PS%2FBVBFbV%2BMAhi34%3D)

和其他几种互连技术的比较

 

UB网络层是软件定义的。UB交换机只需负责简单的 数据平面上的数据转发, 而由网络控制器为分布式节点计算路由, 并负责配置UB交换机的转发表。  

UB-MESH是什么？

 

UB-MESH即华为采用UB技术组建超节点\集群而采用的组网技术。

 

（详细可参考论文： UB-Mesh: a Hierarchically Localized nD-FullMesh Datacenter Network
Architecture，

链接：https://arxiv.org/abs/2503.20377）)

 

另：严格来说，CloudMatrix384目前是采用了UB技术，采用了部分UB-MESH技术，不是完整完善的UB-MESH组网，这点请注意区分。  

 

UBPU内嵌UB
Switch，支持UB报文通过UBPU直接转发至直连相邻的UBPU，无需软件中转，同时UB通过链路层虚通道、网络层逐包/逐流多路径路由和传输层通道共享等机制，解决UB报文通过直连路径绕路引入的死锁和带宽利用率下降等难题，为超节点提供UB-Mesh
以及基于光交换的组网技术，实现大规模低成本部署。  

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F9a734309ad3085fbd88ddaf49ccf8bbb?Expires=1780066335&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=xq979WUjWZ1%2F9WzhTsewipJLWzo%3D)

**如上表，每块****NPU配备两个UB IO控制器（提供UBx72 通道）****；每块****CPU则配备一个UB IO控制器（提供UB
x32接口）。**

 

UB-Mesh中的nD-FullMesh拓扑充分利用了业务数据局部性，优先考虑短程直接互连路径，以最大限度减少数据移动距离并减少交换机使用为目标，是一种兼具高性能和低成本的拓扑组网，如下图所示。

 

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F7998815967added4241dbb69a90c5136?Expires=1780066335&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=psBFhf8g5D%2F6K7MF2B3eGdXHQwU%3D)

图  nD-FullMesh 拓扑示意

 

 

 

廖博PPT图：

 ![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fa341df710ece083dafba8be596ea20ec?Expires=1780066335&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=GogGJzn0ZWBzgidH0LpirqvynXI%3D)

 

从互联距离角度出发，也可简单理解为单板上的8块NPU之间是1D全连接、同一机架内叫2D全连接、跨机柜同屋子里叫3D全连接、楼层机柜组的4D全连接，乃至整栋建筑的5D全连接等。

 

 

1D-FullMesh即指NPU单板内的8个NPU芯片之间实现FullMesh互联，采用电气电缆互联。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fff841790806371777fe359f3f0ec4373?Expires=1780066335&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=jKL3u39hOvejxufmd%2Bn3wUI9%2B08%3D)

                 8个NPU芯片FullMesh互联图

 

 

2D-FullMesh是指单机架内（RACK）的共8块NPU单板（共64个NPU芯片）和4块CPU单板（共8个CPU芯片）之间实现Mesh互联。另外考虑到安全性，每个机柜Rack可配置一块备用NPU，从而实现64个常规NPU+1个备用NPU的设计理念。

 

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F635279b0b0146fac35628a9b9db3108d?Expires=1780066335&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=ocPrp86cCTJEHWxAxOTJhsOqJJs%3D)

  

 

每个机架（RACK）内配置有4组交换平面（switch plane），每个交换平面18个LRS交换机组成，其中2个用来连接CPU和备份NUP,8个用于连接柜内的NPU,8个用于对外的机架间之间互联。 4组交换平面共提供了4\*256个对外UB接口以便连接其他机架（RACK）。

 

机架内所有线缆都采用电缆互联，不采用光模块。

  

 

注意：如上这个说法是针对950 Atlas 950 SuperPoD而言，CloudMatrix384单机柜目前只支持32块910C。

 

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fe086f32b019f1f307cd7aa48b691d897?Expires=1780066335&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=LTwtBYIpH6IbNmhugTf1OvDMxa8%3D)

  

通过**UB-Mesh-Pod****组织**4D-FullMesh组网

 

**可把16个**2D-FullMesh的机架**形成一个名为UB-Mesh-Pod的四维全网格架构。**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F89577444da0114fcff2d80c540fff4f1?Expires=1780066335&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=qc906EzPlyaI5OHj5g%2FhWZ0uVk8%3D)

具体方法：

**1、如****图所示，四个相邻机架****排成一列/行，****各机架之间通过LRS端口直接MESH互联。**

**2、如此排列4列/行。**

**3、每行/列之间的4个机架也通过LRS端口直接mesh互联。**

**这样就实现了行、列****两个维度****都通过****连接四个相邻机架构建****了****跨****16个****机架****的****全网状结构（**这是考虑到有源电缆传输距离的最佳方案。**）**

**这样的话，每个POD含有16个RACK机架，而****每个机架配备64个神经处理单元（NPUs），最终形成了名为UB-Mesh-Pod的四维全网状架构。该四维全网状架构UB-Mesh-Pod总共包含1024个****NPU****。**

**更大规模的扩张到8K：**

**在完成1K
UB-Mesh****-****Pod的部署后，****即可****进一步构建了UB-Mesh-SuperPod系统，该系统可容纳多个UB-Mesh-Pod。**

**考虑到当前云场景中中小型语言模型训练任务可能无法填满整个SuperPod，选择采用对称的Clos拓扑结构作为Pod级互联方案，而非继续使用全网格架构。这种设计使云管理团队能够根据用户需求灵活划分SuperPod资源，并确保每个划分区域的带宽充足。**

**如下图所示****，****可****通过****配置****HRS****交换机****将SuperPod内各机架连接起来，平滑扩展，最高可扩展至8192个
NPU。**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fa7e5d14debca5bd9f99ce935010a2871?Expires=1780066335&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=YL5oCWIiclTTHMlF%2F2d41hWGkwc%3D)

廖博士PPT图示：

 

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fa7bf2131f4af707175802b9748932e78?Expires=1780066335&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=WRnhaePqswFmC5YFWl%2BVmwHKLkw%3D)

华为超级点参考架构

 

 

超节点参考架构（SuperPoD Reference
Architecture）是面向AI时代数据中心，基于灵衢（UnifiedBus，UB）的新型计算系统架构，支持CPU、NPU、GPU、MEM、DPU、SSU（Scalable
Storage Unit）和Switch中的一种或者多种组件资源池化和平等协同，构建逻辑上的一台计算机。

 

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fdb1457837b621382324e1b9c09a08587?Expires=1780066335&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=2%2FDdpRy8Fy3Vdp%2B0okanutUL0gU%3D)

图   基于灵衢的超节点参考架构

 

  

六大共性特征：

 

**1.****总线级互联**

基于灵衢的总线级互联，提供百纳秒级同步内存语义访问时延和2~5us异步内存语义访问时延，满足算力单元高并发的访问需求；提供组件间TB/s级带宽，相比传统数据中心网络带宽至少提升10倍。

 

**2.****协议归一**

基于灵衢的协议归一，支持超节点内不同类型、不同距离的组件统一互联，访问无协议转换开销，组件包括CPU、NPU、GPU、MEM、DPU、SSU和Switch等；提供统一的编程模型。

 

**3.****平等协同**

基于灵衢的平等协同机制，支持超节点内所有组件去中心化的互相访问、调用和协同工作，提升组件间访存和通信性能。

 

**4.****全量池化**

基于灵衢和Linux操作系统的灵衢扩展组件，提供超节点的设备管理、内存管理、通信和虚拟化等功能，支持超节点资源的高效池化管理和调用，提升资源弹性和利用率。

 

**5.****大规模组网**

支持超节点以大于90%的线性度从单节点扩展到8192卡，未来还将持续提升至15488卡，甚至更大规模；支持超节点通过UBoE构建百万卡规模的集群，兼容以太组网。

 

**6.****高可用性**

基于灵衢的可靠机制，支持超节点内应用无感知的us级检错和容错，在8192卡超节点范围内实现光互连MTBF（Mean Time Between
Failures）大于6000小时。

 

 

额外感触：

1、华为超节点解决方案倾向于尽量采用电连接方案，而非光连接方案。原因在于电连接方案成本更优，错误率比光连接方案更低。理论上千卡昇腾950以下的超节点都是采用电缆连接即可。

 

2、华为解决方案没有把CPO、OCS这些市场炒作的东西当做主流或者必选。

3、目前的CloudMatrix 384是在950芯片出来之前的方案，明年切换到功能更强大集成度更高的Atlas 950
SuperPod方案后，成本会大幅下滑，光模块用量也会大幅下降。

*【本文内容来自于对公开信息的分析，如有侵权请指出将及时修正或删除。】*

**【如本文对您有用，请转发并点亮大拇指和小红心，谢谢！】**

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 10:52*