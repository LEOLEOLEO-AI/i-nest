---
title: "2025 SIGCOMM：华为AI集群网络的六大技术挑战与突破方向"
source: "https://mp.weixin.qq.com/s/dawQ3IH7fiAIgffnIBGhtA"
created: 2025-09-17
note_id: "1887734980252103232"
tags:
  - "AI链接笔记"
  - "AI集群网络"
  - "SIGCOMM 2025"
  - "高带宽光互联"
  - "get-笔记"
  - "AI研究"
---

# 2025 SIGCOMM：华为AI集群网络的六大技术挑战与突破方向

## 摘要

📡 **算力经济时代的背景与挑战**   - **算力需求爆发**：据“星际之门计划”预测，2028年AGI实现需数百万GPU支撑，总功耗达3500MW（三峡大坝发电量的1/4）；谷歌tokens年增长64倍（10T→634T），微软增长5倍（20T→100T）。   - **集群算力公式**：总有

## 正文

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F752909159cce241adb8c616d8f46ca18?Expires=1780067028&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=zP1zyK%2BgmC7AAIVVvK87B8qMSYo%3D)

◆ 引言

 

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F70ef1976fab349a5adce471db8c95412?Expires=1780067028&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=uvW9AClrGqUoLw7JTchL7FZizfY%3D)

   
在2025年SIGCOMM的赞助演讲中，华为2012实验室专家围绕“AI集群网络的关键技术挑战”展开分享。演讲背景聚焦人工智能驱动的“算力经济新时代”——AI及AI推理应用的爆发式发展，对AI计算基础设施提出了前所未有的需求，而AI集群网络作为突破算力瓶颈的核心，正面临六大关键技术挑战。

一、演讲背景：AI算力需求的爆发与集群网络的核心价值

1.1 算力经济时代的到来

      根据“星际之门计划（Stargate
Project）”预测，到2028年AI将具备自主发现科学知识的能力，而实现这一目标需“数百万块GPU”支撑——其总功耗高达3500MW，相当于三峡大坝总发电量的四分之一。与此同时，AI相关应用正推动算力成为核心生产要素：过去一年，谷歌（Google）的tokens数量从2024年一季度10T增长至2025年一季度634T，年增长率达64倍；微软（Microsoft）则从2024年的20T增长至2025年一季度100T，年增长率5倍。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F7198c10851593874c09eb41180230961?Expires=1780067028&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=%2FtJSkAKH%2Bj1Ti%2BAlrUB0%2FLcxFeU%3D)

1.2 AI集群的算力公式与网络定位

      AI是当前历史上“计算、内存访问、通信密集度最高”的应用，远超单芯片、单服务器的承载能力。集群的总有效算力遵循核心公式：

集群总有效算力 = 单芯片算力 × 集群规模 × 计算效率

     
其中，AI集群网络是满足海量算力需求的“关键突破口”——网络规模越大、层级越复杂，成本、功耗、可靠性与性能的矛盾越突出；而通信性能不足会直接降低计算效率，且网络本身也受摩尔定律约束，因此需直面多维度技术挑战。

二、AI集群网络的六大核心技术挑战

      华为在演讲中明确，当前重点研究的六大挑战包括：高带宽连接、高容量交换、大规模网络拓扑（Large-Scale
Fabric）、高吞吐量传输、短路径数据移动（计算架构视角）、长距离连接。

2.1 挑战一：高带宽连接——448G技术的瓶颈与光互联突破方向

2.1.1 需求背景

 

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fceccb29a64821dbf9f235f9139a18da7?Expires=1780067028&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=C1Fmfw601J%2ByFEMoyd%2FC66qnN%2Fc%3D)

      当前超节点（Super
Node）是连接技术发展的核心驱动力，推动高带宽服务需求升级。目前Nvidia、Broadcom、Marvell已发布224G
serdes芯片，但下一代448G serdes仍处于“初步研究阶段”。

2.1.2 两大核心瓶颈

1. 芯片技术瓶颈：448G服务高度依赖芯片技术，需在架构与算法层面实现创新突破（224G已采用先进芯片技术，448G需在此基础上进一步升级）；

2. 传输距离瓶颈：448G电驱动的传输距离仅“不足1米”，而机柜间互联通常需要1.5米以上距离，导致“机柜间连接无法实现”，全电气互联面临本质限制。

2.1.3 解决方案方向

      需重点研究“高密度光互联技术”，以解决距离、功耗、延迟问题：

- 探索高密度XPO（扩展并行光）或OIO（光互联光）技术，通过多低速并行通道或波分复用，降低对单通道速率的需求；

- 研发高密度EIC（集成电连接器）、高密度PIC（集成光连接器）、高密度光/电连接器及2.5D/3D先进封装技术。

2.2 挑战二：高容量交换——芯粒（Chiplet）架构与“互联损耗”难题

2.2.1 交换容量的演进与瓶颈

     
AI计算推动芯片交换容量快速突破，主流交换芯片容量已从51.2T提升至102.4T，部分产品超100Tbps。但单芯片容量已遇瓶颈：以博通TH系列为例，TH4、TH5基于“单芯片（Single
Die）”设计，而TH6采用“1个主Die+8个IO芯片”架构，标志单芯片能力已经接近极限。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Febdf93812635cd63f90ee9a5df43ed4a?Expires=1780067028&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=wPjRPGIV7DmVzssFBzwm1hd6w%2Fk%3D)

2.2.2 行业方向：芯粒（Chiplet）架构的挑战

      行业正转向“芯粒（Chiplet）架构”（当前热门方向为“晶圆级芯粒”），但大规模芯粒集成的核心难题是“降低互联损耗（Interconnect
Tax）”，具体包括：

1. 芯粒内部的互联与交换开销“随规模呈超线性增长”，需通过架构创新与资源复用减少损耗；

2. 芯粒规模扩大后，内部路由、流量均衡、流控与缓存管理的复杂度“超线性增加”，需提升效率以避免性能瓶颈。

2.3 挑战三：大规模网络拓扑——CLOS拓扑的成本困境与UB-Mesh创新

2.3.1 核心矛盾：扩展需求与CLOS拓扑成本的失衡

      大规模拓扑的本质矛盾是“算力扩展需求”与“CLOS拓扑成本”的不匹配：

- 若单计算芯片能力下降X倍，需将集群规模扩大X倍以维持总算力；

- 若单交换芯片容量下降Y倍，采用两层CLOS拓扑时，扩展能力会下降Y²倍；

- 为匹配集群级算力，需构建XY²规模的网络，且成本因“交换层级增加、互联开销、功耗、可靠性问题”呈“超线性增长”。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fa1ef0e9e42f2864a9471a4b9fdcd3b93?Expires=1780067028&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=0kDIiqS39rg0CqEE3PK6XosAmps%3D)

2.3.2 华为解决方案：UB-Mesh拓扑

      华为在2025年开发者大会发布“UB-Mesh（统一总线网格）”拓扑，其核心设计包括：

- 考虑“传输流量局部性（Traffic Locality）”与高可靠性，采用“混合直连+交换网络”架构；

- 性能表现：训练性能损耗仅约1%，兼具低成本与高可靠性。

2.3.3 系统级挑战与研究方向

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fd3b4be67c36c781df70c2043f00ce940?Expires=1780067028&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=qXOyLueh5BeR6q%2FNNwzSdctdP8A%3D)

      UB-Mesh仅为起点，未来需从系统层面创新拓扑，重点解决四大问题：

1. 结构化编址与查找：通过“短ID（Short ID）”与扁平地址空间（Flat Address
Space），将表项空间从O(N)降至O(1)，最小化封装开销，减少50%控制面“直接交付负载”；

2. 全路径路由：利用拓扑展开与拓扑规律性，实现全路径路由，将带宽提升2倍，降低VC（虚拟通道）需求3倍；

3. 超快速故障处理：替换“逐跳收敛”机制，实现拓扑感知的超快速路由收敛，提升故障应对效率；

4. 拓扑与路由感知流控：应用“环路打破理论”进行通道规划，降低算法复杂度（从O(NlogN)至O(N)）。

2.4 挑战四：高吞吐量传输——Scale-Up网络的协议瓶颈

2.4.1 Scale-Up网络与传统总线的本质差异

      AI网络的核心是“横向扩展网络（Scale-Up Network）”，与传统Host总线（Host Bus）在延迟、带宽、规模、可靠性上差异显著：

- 传统Host总线：1个Host，1Tbps带宽，延迟约60到100ns，典型的传输协议为PCIe；

- Scale-Up网络：256-2048个Host，10Tbps带宽，延迟约2到4μs，。

      当前业界已在Scale-Up网络上推出NV-Link、UALink、统一总线（Unified
Bus）等协议，此类协议的核心共性是“传输层至关重要”。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ff06a8b95d002276d14883bee40e10ba1?Expires=1780067028&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=oglrNv64KWlqhZFFoDBrRZYQkq8%3D)

2.4.2 传输协议的三大核心挑战

1. 未完成资源（Outstanding Resource）受限：AICore的未完成窗口过小，无法支撑全带宽传输——尤其在“同步Load/Store语义”场景下，同步指令会进一步限制窗口大小；

2. 可靠性开销：针对内存语义的传输重传（尤其“远内存”场景），会增加芯片面积与延迟成本；

3. 多路径引入的排序挑战：向大规模AI集群网络引入“非等效多路径”，需解决数据排序问题，避免带宽瓶颈。

2.5 挑战五：短路径数据移动——计算架构视角的效率优化

2.5.1 需求背景：大模型推理的稀疏化趋势

     
当前大型语言模型（如DeepSeek）的推理正逐渐向“稀疏化（Sparsity）”与“层次化（Hierarchy）”发展。在小数据量、稀疏传输场景下，集合通信（尤其“稀疏集合通信”）的延迟主要由“链路延迟与控制面延迟”主导，矛盾从“数据传输”转向“系统架构与结构”。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ff007a07a044ed3df45f443ae387c13e5?Expires=1780067028&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=5CNkcuuvP3PV3kt28PJW9vkXICE%3D)

2.5.2 两大架构瓶颈与解决方案

1. CPU中心架构的控制面开销：传统“以CPU为中心”的架构需多次协议转换，控制面开销显著，需构建“全对等（Full
P2P）互联架构”消除数据迁移瓶颈——华为提出的“统一总线”即基于全P2P架构设计；

2. DMA语义的数据面开销：传统“基于DMA（直接内存访问）”的语义需多次HBM（高带宽内存）读写操作，与集合通信结合后数据面开销巨大，需构建“短路径直接语义”实现HBM旁路——传统DMA需8步完成数据移动，而短路径语义仅需3步即可实现“计算核心间的确定性移动”。

2.6 挑战六：长距离连接——分布式AI训练的算力整合难题

2.6.1 需求背景：算力分散与分布式训练需求

 

     
AI集群规模扩大推动“分布式AI训练”需求，当前中美已部署大量数据中心/AI计算中心（如美国俄亥俄集群、爱荷华集群，中国多地AI计算中心），但“大量闲置算力呈碎片化分布”，需通过长距离连接实现算力整合。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F5e0109ab56f5610fc8249d997e792bcf?Expires=1780067028&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=cFfFx3BrUXTpYh9E5vatDeNnNeo%3D)

2.6.2 三大核心挑战

1. 传输挑战：如何将RoCE（融合以太网的RDMA）协议扩展至广域网（WAN），实现跨地域高吞吐量传输；

2. 并行性挑战：如何最大化“大规模计算与通信并行”的效率；

3. 资源调度挑战：灵活调度计算、网络、存储资源，提升整体效率。

2.6.3 华为实验验证与技术栈

 

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F51a14347d8d250cce93f9d58f669dd78?Expires=1780067028&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=oEK0adUcQ7yOzxXMRSYeU1zQhDA%3D)

      华为基于华为云平台开展长距离传输实验，实现“1000公里内性能损耗<5%”（含PP/DP并行），具体案例包括：

- 500公里（某省3个数据中心）：GPT3-175B训练，性能损耗2.8%；

- 10公里（贵阳AZ4-AZ5）：盘古8×88 MoE训练，性能损耗3.5%；

- 1600公里（贵阳-芜湖2个数据中心）：LaMA2-70B训练，性能损耗2.5%。

      实验采用的技术栈包括：

- 调度创新：自适应模型分割，隐藏30%通信时间，训练加速30%；

- 集合通信创新：多平面层次化并行；

- 传输创新：FlatRate拥塞控制，跨可用区（AZ）P99延迟降低50%以上。

      需注意的是，当前实验仅覆盖“点对点”或“三点拓扑”等简单场景，面对更大规模拓扑或更多数据中心时，需更系统化的解决方案。

三、总结与合作邀请

     
AI集群网络是支撑算力经济、实现超级智能（AGI/ASI）的核心基础设施，其六大技术挑战（高带宽、高容量交换、大规模拓扑、高吞吐量传输、短路径数据移动、长距离连接）需行业共同突破。华为已在部分领域（如UB-Mesh拓扑、统一总线、长距离传输技术栈）开展探索与验证，并邀请全球技术社区共同研究，推动AI集群网络技术成熟。

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 11:03*