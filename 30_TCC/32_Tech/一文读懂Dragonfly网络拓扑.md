---
title: 一文读懂Dragonfly网络拓扑
tags:
- chip-hardware
- chiplet
- paper
- semiconductor
- topology
---
> 笔记本: 微信  
> 创建时间: 2023-03-20  

---

智能摘要
在原先传统数据中心内，计算存储性能未提升前，端到端的时延主要在端侧，即计算和存储所消耗的时延占比较大，而当计算存储器件性能大幅提升后，网络成为了数据中心内端到端的性能瓶颈。业界针对该问题开展了多样的架构研究和新拓扑的设计。将最短路径和非最短路径分为两个VC，分别排队来计算长度。只有在MIN和VAL的输出端口不一样的时候，才用VC的队列长度来进行判断，否则还是直接使用队列长度来判断。本号聚焦相关技术分享，内容观点不代表本号立场，可追溯内容均注明来源，发布文章若存在版权等问题，请留言联系删除
原文约 2158 字 | 图片 10 张 | 建议阅读 5 分钟 | [评价反馈](https://static.app.yinxiang.com/embedded-web/clipper/#/Evaluating?d=2023-03-21&nu=62fd6b0c-fd61-421a-9c10-a3ce26e11194&fr=myyxbj&ud=1bb10ab&v=2&sig=8C68A3D3FFC3633C2DEA80B1D2EFF2BC)


# 一文读懂Dragonfly网络拓扑

架构师技术联盟


据Hyperion Research 公司按照系统验收的时间估算，2021至2026年期间，全球将建成28～38台E级或接近 E 级的超级计算机。本文参考自“[总线级数据中心网络技术白皮书](https://mp.weixin.qq.com/s/MxCnNGAyYl17tZAqhIhOlg)”。


在原先传统数据中心内，计算存储性能未提升前，端到端的时延主要在端侧，即计算和存储所消耗的时延占比较大，而当计算存储器件性能大幅提升后，网络成为了数据中心内端到端的性能瓶颈。下图显示了计算存储性能提升前后，端到端时延的占比变化。


**网络新拓扑架构路由技术，大规模组网实现跳数下降20% 。**针对高性能计算场景，数据中心的流量特征关注静态时延，需要支持超大规模，传统的 CLOS 架构作为主流的网络架构，其主要关注通用性，但是牺牲了时延和性价比。业界针对该问题开展了多样的架构研究和新拓扑的设计。

当前数据中心网络架构设计大多基于工程经验，不同搭建方式之间难以选择，缺乏理论指导，缺乏统一性设计语言。另外网络拓扑性能指标繁多，不同指标之间相互制约，指标失衡很难避免。

Dragonfly是由John Kim等人在2008年的论文Technology-Driven, Highly-Scalable Dragonfly Topology中提出，它的特点是网络直径小、成本较低，对于高性能计算有着非常大的优势。现在已经被运用在使用Cray XC系列网络的各种超算中。
## 拓扑结构

一个简单的dragonfly网络如下图所示。

Dragonfly的拓扑结构分为三层：Switch层，Group层，System层[也叫路由器(Router)、组(Group)、系统(system)层）]。
- 
Switch层：包括一个交换机，及其相连的 **p** 个计算节点
- 
Group层：包含 **a** 个Switch层，这 **a** 个Switch层的 **a** 个交换机是全连接(All-to-all)的，换言之，每个交换机都有 **a-1** 条链路连接分别连接到其他的 **a-1** 台交换机
- 
System层：包含 **g** 个Group层，这 **g** 个Group层也是全连接的
对于单个switch交换机，它有p个端口连接到了计算节点，a-1个端口连接到Group内其他交换机，h个端口连接到其他Group的交换机
因此，我们可以计算得到网络中的如下属性
- 
每个交换机的端口数为 **k**=p+(a-1)+h
- 
Group的数量为 **g**=ah+1
- 
网络中一共有 **N**=ap(ah+1) 个计算节点
- 
如果我们把一个Group内的交换机都合成一个，将它们视为一个交换机，那么这个交换机的端口数为 **k‘**=a(p+h)
在一个较小规模的网络中， g=ah+1 个group可能会较多，可以将任意两个Group之间的连接数由一条增加为多条，这样任意两个Group之间就有 floor((ah+1)/g) 条链路连接。
不难发现，在确定了 p，a，h，g 四个参数之后我们就可以确定一个dragonfly的拓扑，因此一个Dragonfly的拓扑可以用 dfly(p,a,h,g) 来表示
一种推荐的较为平衡的配置是方法是：a=2p=2h
## 路由算法

Dragonfly的路由算法主要有两类，最小路由算法（Minimal Routing，最短路径的路由）与由Valiant提出的可以在系统层面上应用的非最短路径的路由算法（Non-Minimal Routing，非最短路径的路由）。此外作者在论文中还提出了UGAL(Universal Globally-Adaptive Load-balanced，全局自适应负载均衡路由)算法。具体来讲：
- 
Minimal Routing：最短路径的路由，简写为**MIN**。由于拓扑的性质，Minimal Routing中最多只会有1条Global Link和2条Local Link，也就是说最多3跳即可到达。在任由两个Group之间只有一条直连连接时（即**g**=ah+1时），最短路只有一条。
- 
Non-Minimal Routing：非最短路径的路由，可以简写为**Non-Min**，来自论文A scheme for fast parallel communication。有的地方叫Valiant algorithm，简写为**VAL**，还有的地方叫Valiant Load-balanced routing，简写为**VLB**。随机选择一个Group，先发到这个Group然后再发到目的地。由于拓扑的性质，VAL最多会经过2条Global Link和3条Local Link，最多5跳即可到达。
- 
Universal Globally-Adaptive Load-balanced(**UGAL**)：全局自适应负载均衡路由，来自论文Load-Balanced Routing in Interconnection Networks。当一个数据包到达交换机时，交换机根据 最短路径路由MIN 和 非最短路径的路由VAL 的 路径上所有交换机队列的排队长度的和，来选择路由。
因为要获取到全局网络状态信息太难了，所以提出了一系列变种，在Dragonfly中有如下若干种实现方式：
- 
UGAL-G：只根据发送节点所在的Group的所有交换机的队列排队长度来进行判断。但是要实现这个依然很难，也是一个非常理想的情况。
- 
UGAL-L：只根据本地交换机的队列排队长度来进行判断，这种方式会产生一个问题：当在源Group中进行路由时，如果最短路径和非最短路径都要经过源Group中另一个交换机时，此时这两条路径的出口队列一致，因此总是会选择最短路径。
- 
UGAL-LVC：针对UGAL-L的问题进行了一点改进：将最短路径和非最短路径分为两个VC，分别排队来计算长度。但是这样又会导致数据包更偏向选择非最短路由，导致在均匀流量模式下性能不好。
- 
UGAL-LVC_H：针对UGAL-LVC的问题又进行了一点改进：只有在MIN和VAL的输出端口不一样的时候，才用VC的队列长度来进行判断，否则还是直接使用队列长度来判断。
- 
UGAL-LCR：由于只用本地信息来判断拥塞，在buffer越大时反而造成的延迟越大，因为buffer被填满了之后，上游的交换机才能通过没有credit了感知到。为了克服这个问题，可以通过当前拥塞情况主动增加credit的返回延迟，上游交换机认为返回credit越快的交换机拥塞程度越小。
## 死锁避免

在Dragonfly中，形成环路的概率要高很多。因此，如果使用最短路由，需要2个VC来避免死锁；如果使用非最短路由，需要3个VC来避免死锁。


参考资料：
1、https://ngdcn.com/post/208.html
2、https://www.cnblogs.com/Nreyab/p/15590684.html
3、http://blog.sysu.tech

---
**Tags:** [[NaaS]] [[Chiplet]]
