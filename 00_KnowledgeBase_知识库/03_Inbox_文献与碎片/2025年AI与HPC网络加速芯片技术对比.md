---
title: "2025年AI与HPC网络加速芯片技术对比"
source: "https://mp.weixin.qq.com/s/AdMYnyIbe_yiYX2qpXWXjQ"
created: 2025-09-10
note_id: "1887052589405664008"
tags:
  - "AI链接笔记"
  - "AI网络加速"
  - "DPU技术对比"
  - "400G/800G以太网"
  - "get-笔记"
  - "AI研究"
---

# 2025年AI与HPC网络加速芯片技术对比

## 摘要

### 1. Intel IPU E2200 400G DPU（代号Mount Morgan）  🔹 **核心定位**：E2100升级版，台积电N5工艺，400G MAC吞吐量，瞄准NVIDIA BlueField-3和AMD Pensando Salina 400市场   ![Intel IPU 

## 正文

Intel IPU E2200 400G DPU（代号Mount Morgan）

参考阅读：[Intel IPU E2100 DPU
正式发布](https://mp.weixin.qq.com/s?__biz=Mzg3MDY0OTQ0NA==&mid=2247496041&idx=1&sn=b4b12a57afbeaf5601e6c288249ef545&scene=21#wechat_redirect)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F745e2efe69257685b00103e2399adcad?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=OZVP%2BuPRIAVzTmVRmzb3X4hSLbw%3D)

* 产品定位：IPU E2200作为E2100系列的升级产品，专为AI和高性能计算（HPC）工作负载而设计，采用台积电N5工艺，提供400G
  MAC吞吐能力。其主要特性包括高性能卸载、灵活模式和可编程性，支持多主机、无头和融合模式。该产品旨在与NVIDIA BlueField-3和AMD
  Pensando Salina 400展开竞争，适用于数据中心基础设施卸载和加速。
* 系统架构：采用单芯片设计，计算复合体包括最多24个Arm Neoverse
  N2核心，配备四通道LPDDR5内存。网络子系统具备P4可编程性、高性能加密和网络NVMe设备呈现功能。内置PCIe Gen5 x32域交换机，与NVIDIA
  BlueField-3类似，可确保高效数据传输。
* 数据包处理：采用FXP数据包处理器，具备P4可编程性和硬件可配置性。其入口/出口阶段包括解析器、转发查找、过滤处理器；其他组件还包括RDMA引擎和流量整形器（基于定时轮算法）。
* 关键特性：支持多种操作模式，提供了部署灵活性（例如无头模式类似于NVIDIA BlueField
  DPU的JBOF应用）。加密引擎支持在线（按流配置）和旁路，可实现高性能加密。流量整形基于定时轮算法，而RDMA引擎可实现高效数据传输。自定义卸载功能可通过加速器和IP块实现，部分操作在网络侧完成，部分则跳转到Arm计算侧。
* 性能指标：支持400G线速处理，提供低延迟卸载，有效释放主机资源。基准测试证实了其在高负载下的稳定性。
* 实现亮点：采用台积电N5工艺，支持高密度集成；内置PCIe交换机；采用Arm Neoverse
  N2核心，可提供高效计算。Intel在DPU领域拥有丰富经验，服务于如Google和中国超大规模云服务商。
* 最新动态：产品已开始出货。它旨在挑战AI网络领域的领先地位，通过提供更快的数据传输和生态系统支持，赢得市场采纳。未来有望扩展至基础设施卸载的多种数据中心用例。

AMD Pensando Pollara 400 AI NIC

参考阅读：

* [AMD发布业界首款UEC就绪AI
  NIC](https://mp.weixin.qq.com/s?__biz=Mzg3MDY0OTQ0NA==&mid=2247499799&idx=1&sn=148a0c5aaa9b56ee5084ed211009ee19&scene=21#wechat_redirect)
* [AMD Advancing AI
  2025峰会主旨演讲](https://mp.weixin.qq.com/s?__biz=Mzg3MDY0OTQ0NA==&mid=2247504631&idx=1&sn=f98a824914db01c8ef7a127a704e1f3b&scene=21#wechat_redirect)
* [AMD Advancing AI
  2025峰会主旨演讲核心内容](https://mp.weixin.qq.com/s?__biz=Mzg3MDY0OTQ0NA==&mid=2247504631&idx=2&sn=8410e63772632f73d81abcc7661d9a5c&scene=21#wechat_redirect)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fdf0034e1da0438fcb0d452bde78f64c2?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=bRO%2BcjG6gIHdv%2BvOA4yLad%2FOr1c%3D)

* 产品定位：Pollara 400作为AMD Pensando产品线的演进，专为大规模GPU集群的后端AI网络而设计。该产品支持Ultra Ethernet
  Consortium (UEC) 1.0规范，提供400
  Gbps的吞吐能力，兼容基于Ethernet的RDMA，相比于先前RoCEv2，性能提升高达1.25倍。通过优化的RDMA和高可用性，它能够有效缩短AI作业完成时间。
* 系统架构：采用PCIe Gen5 x16卡形态，直接与主机相连，无需中间交换机，并支持模块化和耐故障设计。该卡与AMD Infinity
  Fabric集成，可实现全集群RDMA以太网（Ethernet）网络。通过PCIe交换机连接多个NIC、CPU和GPU，可确保单一卡或GPU故障不会导致整个机架中断。在设计上可实现与GPU
  1:1配比，适用于如Gigabyte G893-ZX1-AAX2或ASUS ESC A8A-E12U等系统。
* P4可编程流水线：核心架构基于P4语言，包括P4NET（发送/接收路径）和P4DMA（DMA路径）。组件涵盖表引擎（TE，支持SRAM、TCAM和主机/GPU内存）和匹配处理单元（MPU，支持ALU、分支、加载/存储操作）。该架构支持虚拟到物理地址转换（va2pa），针对每个LIF/MR键-页表，并支持多级页；支持原子操作，紧邻SRAM，可实现加法、向量设置/清除/读取、原子读-递增/递减；并通过广播网络实现流水线缓存的一致性，支持失效/更新逻辑。
* 解决AI扩展网络挑战：针对ECMP负载不均衡、节点拥塞和数据包丢失等问题，Pollara
  400提供了数据包喷洒与重排序、基于RTT的动态发送速率调节以及选择性ACK传输协议。基准测试结果显示，AI模型网络等待时间占比为18-57%（分布式推理中为40-75%），Pollara
  400通过智能负载均衡、拥塞管理和快速故障切换，有效提升了网络利用率。
* UEC就绪特性：全面符合UEC
  1.0规范，旨在增强基于RDMA的AI传输。该产品支持多路径数据包喷洒（基于熵值路径选择、ECN/截断反馈动态调整）、可编程拥塞控制（基于NSCC、RTT测量、ACK/NACK/SACK调整窗口）和快速数据丢失恢复（SACK位图重传）。性能测试显示，其相对于RoCEv2性能提升高达40%，并结合AMD
  RCCL库进一步优化AllReduce等操作。
* 最新动态：产品已开始向客户供货，预计很快将进入量产阶段。Pollara 400主打与AMD
  GPU生态的深度集成，面向Meta和Microsoft等超大规模云服务商。

NVIDIA ConnectX-8 SuperNIC

参考阅读：



* [数据中心处理器市场到2030年将翻倍：GPU与ASIC领跑](https://mp.weixin.qq.com/s?__biz=Mzg3MDY0OTQ0NA==&mid=2247503688&idx=1&sn=22dd55120e24778f2ac73956797efcc0&scene=21#wechat_redirect)
* [NVIDIA发展战略研究（2024）](https://mp.weixin.qq.com/s?__biz=Mzg3MDY0OTQ0NA==&mid=2247500891&idx=1&sn=192e0a054ec1fdc0edb6e75d30028ae5&scene=21#wechat_redirect)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F32bbae301ec7eab7458f75e3804929a1?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=xloyXzG4SBoQ5Lpz%2FnzeWcu1sfg%3D)

* ![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F9e1d6ceb431adea831f49edb20a00065?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=Ek7rsABAIyh%2F%2BGChzcMDUVkVE%2Fo%3D)

  产品定位：ConnectX-8
  SuperNIC作为NVIDIA网络平台的最新产品，专为AI训练和推理工作负载而设计，提供800GbE吞吐能力，支持Spectrum-X
  Ethernet和Quantum-X
  InfiniBand。该产品主打高速度、低延迟、多GPU通信，以及与NVIDIA生态的无缝集成；它兼容UEC标准，支持基于以太网（Ethernet）的RDMA（RoCE），旨在减少网络瓶颈在AI模型训练时间中所占的比重。
* 系统架构：采用单芯片设计，支持高径向拓扑。PCIe接口采用48x PCIe
  Gen6，内置交换功能。网络子系统包括800G以太网MAC，集成Spectrum-X交换机；处理引擎涵盖PSA数据包处理器和基于RISC-V的DPA（数据路径加速器）。该产品支持与其他I/O的多协议通信，确保低延迟数据移动，这对于AI工作负载至关重要。
* P4可编程流水线：其核心是可编程流水线，支持P4语言进行数据平面处理的自定义。组件包括用于解析、匹配和操作的PSA处理器，以及用于高级功能（如拥塞控制）的DPA。此外，它还支持AI特定协议，例如多路径和拥塞控制。
* 关键改进：该产品引入了PCIe
  Gen6集成和内置交换功能，支持Gen5/Gen6混合环境。拥塞控制的硬件加速功能可通过DPA优化流量；RDMA功能得到增强，包括选择性ACK和多路径支持。NCCL性能得到优化，AllReduce和AlltoAll吞吐量在不同消息大小下均表现出色。此外，该产品与NVLink集成，可支持全集群低延迟网络。
* 解决AI扩展网络挑战：针对ECMP不均衡、拥塞和丢失问题，ConnectX-8提供了数据包喷洒和重排序、基于RTT反馈的速率调整以及选择性ACK协议。基准测试显示，网络等待时间得以减少，利用率获得提升；训练步长用时和负载下的尾延迟均有显著改善。Spectrum-X设计专用于AI网络的快速以太网。
* UEC就绪性和特性：全面符合UEC
  1.0规范，旨在增强基于RDMA的AI传输。该产品支持多路径喷洒（基于熵的路径选择）、可编程拥塞控制（基于RTT的NSCC）和丢失恢复（SACK位图重传）。性能相对于RoCEv2有显著提升。
* 性能指标：RDMA在800G速率下可实现性能扩展，支持不同消息大小。产品支持线速处理，并展示了在训练步长用时和尾延迟方面的改进。基准测试证实了其在高负载下的稳定性，性能优于400GbE的竞品。
* 实现亮点：作为PCIe Gen6 x16卡，该产品首发部署于NVIDIA GB300 NVL72系统，提供了从Gen5 x16到Grace CPU、Gen6
  x16到B300 GPU以及Gen5 x4到SSD的连接支持。未来还将在MGX PCIe Switch Board上支持B300 PCIe Gen6卡。
* 最新动态：产品已开始出货。行业反馈高度认可其速度和低延迟表现。与NVIDIA
  GPU生态的深度集成，使其在Meta和Microsoft等云服务商中占据了强势地位。结合Spectrum-XGS以太网，可支持分布式数据中心互联，共同打造AI超级工厂。

Broadcom Tomahawk Ultra Ethernet交换芯片

参考阅读：





* [构建高效AI基础设施：网络性能优化（Broadcom）](https://mp.weixin.qq.com/s?__biz=Mzg3MDY0OTQ0NA==&mid=2247495743&idx=1&sn=b338c0a765931987d91077ccbfa99023&scene=21#wechat_redirect)
* [构建10万GPU集群的挑战与解决方案](https://mp.weixin.qq.com/s?__biz=Mzg3MDY0OTQ0NA==&mid=2247497975&idx=1&sn=84ac8cdee81fd0d86d205755cbee239e&scene=21#wechat_redirect)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F43e344976418f297c890dff61dc9ebfd?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=%2FBUCWyEoKO6qBtzQKg7r7B8fhig%3D)

* 产品定位：Tomahawk Ultra作为博通StrataXGS系列的最新成员，专为AI和高性能计算（HPC）工作负载而设计，提供51.2
  Tbps的单芯片交换解决方案，支持512个100G-PAM4端口。该产品主打超低延迟（<250ns）、高带宽和无损操作，以及针对AI扩展应用的优化。它重点关注网络内计算、低一致延迟和高性能。
* 系统架构：采用单芯片设计，支持高径向拓扑。数据包转发流水线分为入口和出口两个阶段，包括以太网MAC → 解析器 → 转发查找 → 过滤处理器 →
  AR/DLB引擎 → 流量管理缓冲区，以及出口的头部重写和解析器。其他组件还包括集合卸载和遥测/可见性引擎，以确保高效处理。
* 关键特性：该产品引入了链路层重试（LLR）和基于信用的流量控制（CBFC）。LLR作为对以太网FEC的补充，可提高对突发错误的鲁棒性；CBFC则为每种无损流量类型预留缓冲区，并根据可用性发送信用。它通过优化头部（AI
  Fabric Header，AFH），以满足HPC和AI扩展应用的需求，该头部负载较小，支持2B或4B地址字段，用于Scale-up
  Ethernet（SUE）。网络内集合（INC）功能可卸载Reduce、All-Reduce、Broadcast等操作，并仅需最小程度的软件修改。该芯片支持拓扑感知的自适应路由，如TH-Ultra等拓扑，能够选择最小/非最小路径，避免死锁，并提供路径质量指标。可编程可见性能够以微秒级粒度收集队列长度、数据包延迟等指标，并可通过Python程序进行定义。拥塞控制功能包括主动遥测（CSIG和IFA的带内遥测）和反应反馈（数据包修剪、基于缓冲占用和驻留时间的ECN标记）。
* 性能指标：在所有端口上，64B数据包均能实现100%线速处理；延迟低于250纳秒。基准测试证实了其在高负载下的稳定性，并支持小数据包的高性能，而非仅仅针对大数据包的吞吐量。
* 实现亮点：采用单芯片设计，支持高密度端口；基于DSP的100G SerDes；裸片面积为780mm²，采用台积电N3P工艺；BGA封装可兼容Tomahawk
  5，功耗较低。博通的交换产品线涵盖HPC（Tomahawk Ultra 51.2 Tbps）、AI扩展（Tomahawk 6 102.4
  Tbps）和区域扩展（Jericho4 51.2 Tbps）。
* 最新动态：产品已开始出货，旨在与英伟达、AMD和Intel的同类产品展开竞争，例如英伟达的下一代交换ASIC，以挑战英伟达在AI网络领域的现有优势，提供更快的数据传输。该产品正大力推动Scale-up
  Ethernet项目，其部署将在HPC或AI数据中心中得到体现。

Intel IPU E2200 400G DPU（代号Mount Morgan）

Intel推出了代号为Mount Morgan的IPU E2200。Intel称之为IPU，但业界通常称为DPU（数据处理单元）。这是对Intel IPU
E2100的升级版本。

此前在2022年，Intel曾分享了Mount Evans的三大愿景。然而，随着下一代产品的到来，这些愿景可能已有些过时。

以下是Intel IPU E2200系列的概览。该芯片采用TSMC N5工艺制造。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ff33d82ebdb675f0c2fd99980147161dd?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=Uo6TkRiYEuKgxC82zmRWuEr8Qw8%3D)

IPU/DPU的目标是通过网络卸载和加速常见的基础设施工作负载。为提供一些背景，Google曾使用E2100系列作为其DPU解决方案。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fddd6ae3db0dbbd2a37a35f3a73c213a6?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=stHxdmwvOrdFhAsq3AQJ7VJf5sw%3D)

E2200配备了400G MAC，支持高性能网络传输。其计算核心采用Arm Neoverse
N2，包含高达24个核心，并通过四通道LPDDR5内存供电。此外，芯片集成了PCIe Gen5
x32域，内置PCIe交换机。相比之下，NVIDIA在其ConnectX-8中引入PCIe Gen6交换机，而BlueField-3 DPU的PCIe
Gen5交换机也是一大亮点。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fa5ea4b74217fad052ccded8ea00e41b2?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=63mseYAidiXCYOlJjdNDBgc%2Bkgg%3D)

在网络子系统方面，E2200支持P4可编程性（P4
Programmability）、高性能加密等功能。关于NVMe的支持，E2200可以通过网络呈现NVMe设备。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fbbb73a8cf912b242c9c858ad5d358adb?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=%2BYyv1FNcXl64LyJySwAnpN095HM%3D)

计算核心部分包括多达24个Arm Neoverse N2核心，由四通道LPDDR5内存支持。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F4355ecdd8e59de76b1e73b9b4bb785f4?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=22bcoweIs%2Bcg0w3v0Jr7fA67gHU%3D)

Intel表示，E2200支持多主机（Multi-Host）、无头（Headless）和融合（Converged）模式。无头模式类似于我们此前展示的AIC
J2024-04 2U 24x NVMe SSD JBOF（由NVIDIA BlueField
DPU驱动）的案例。在融合模式下，E2200可以混合运行，展现出极高的灵活性。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F5f0242130f2c966d96453e099dab47ae?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=w3nwlAFJiQB0u%2BeqvGtF%2Bl8bpLA%3D)

在数据包处理方面，Intel采用了FXP数据包处理器，利用P4实现可编程性和硬件可配置性。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F4c3c3c12506600651af97b3385e1f088?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=WJqCaHsJzAN4Le5nFgJMSzsVWho%3D)

E2200还集成了可按流量配置的在线加密引擎（Inline Crypto Engine）。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fb97d2cc96c74895a584f59f1b51997a2?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=nm%2Badw6S3uUN%2B4wldM1X7RNHFyU%3D)

E2200配备了基于时间轮算法的流量整形器（Traffic Shaper）。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F6297367caa106a9e842fb5429664489b?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=vUwqjc8h1b24fLsK7dt2ukuTWyM%3D)

以下是RDMA传输引擎的详细信息。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F4dc7bf8c60001068c4753d6271777ecb?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=cN9fRTl0VQgQDtLT3LIfby2HkmM%3D)

E2200同时支持在线加密引擎和旁路（Lookaside）加密引擎。旁路加密引擎未标明支持P4可编程性，这显示了两者之间的差异。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fd2a65aa22a6dcb8d71e512c3b11203c6?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=%2FHK30BI5jDoyCcOXrs7ytn%2F2NPw%3D)

E2200支持可编程卸载选项，通过不同的加速器和IP模块实现。例如，某些操作可在网络侧处理，而其他操作可转移到Arm核心侧。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ffdeec37aacf7fbb850f870e0282d968a?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=TZj2hbOT%2FMH2qZaDq8o2ojG33lM%3D)

Intel为IPU列举了多种数据中心用例。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F64b22e2c93926bbe24aab52ba2e0893b?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=MoAzr4biDpJ8EC3tQH3ZysiPJVw%3D)

最大的挑战在于围绕这些功能构建应用程序。

总结

一方面，E2200是一款令人振奋的产品。NVIDIA在DPU领域需要竞争对手，而Intel凭借与Google及一些中国超大规模云计算客户的合作，在IPU领域积累了丰富经验。希望未来能看到更多Intel
IPU产品。至少，E2200的400G吞吐量已能与NVIDIA BlueField-3和AMD Pensando Salina 400 DPU匹敌。

AMD Pensando Pollara 400 AI NIC

AMD推出了一款新型AI NIC，命名为AMD Pensando Pollara 400 AI NIC。这款NIC支持超以太网（Ultra Ethernet
Consortium，UEC），速率达到400GbE。

以下是该NIC的概述。虽然看似与NVIDIA ConnectX-7竞争，但其功能有所不同。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F8e0e4a87314cb0c908bf2c32c253497f?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=tpzxK%2B4QpgM9u7ezOGUSMOx7jP0%3D)

作为一款AI NIC，AMD对其用途有明确设想。NVIDIA倾向于移除PCIe交换机，而AMD则拥抱PCIe交换机，设想其GPU与Pollara 400
NIC在系统中的1:1配比。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fa033aebc9fa08693bb85678f090916a2?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=394g%2BRYMuPGsoHUWexA7sSqJQ5Q%3D)

以下是该NIC的块图。值得注意的是，AMD未使用PCIe交换机，而是采用P4（Programmable Protocol
Processing，可编程协议处理）实现可编程性。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F1bfee18214a39ddfa3e8876720babf9e?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=SeEipPv1iBGMUfoFLw5CEgn6p0I%3D)

P4架构旨在构建可编程的数据包处理流水线。这种技术并非AMD独有，例如Intel为Google设计的IPU系列也采用了P4。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fbeb93e95c8e620a248c21271c16fefe0?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=L06%2BSgksy6viZtR41nEPVERmM58%3D)

AMD进一步介绍了P4流水线的核心组件。首先是表引擎（Table Engine，TE），负责生成表键并发出内存读取请求。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ff14f35a6e412bfdc666151783ac773cf?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=tPF3%2F4bqwzSczqD5LTmwdtgLZgY%3D)

还有匹配处理单元（Match Processing Unit，MPU）。在网络中，通常需要根据数据包中的模式匹配来选择流量流。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F550a1227d06cbe2d2af7badffeb008f0?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=vrUPOGNsRd2LUVx55cCBsOfvtTU%3D)

AMD还展示了P4架构的其他增强功能，例如虚拟地址到物理地址的转换（va2pa）以及原子内存操作。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F59c8e00035fefdc52ea23fe61e896072?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=OsQW8jHyM%2FK%2FAjw5FSDOkATVhFY%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F814b7e3a59eaecf182e07ea8ef9e1c01?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=Yqbg7a%2BTyFYBBlgY39dki0qHp%2BI%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F028cf0847d0cca61d2f8e9b82fbf925d?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=F%2FXEd5j2kyQU14E8VaXlF8J7e%2Fg%3D)

AMD还实现了流水线缓存一致性（Pipeline Cache Coherency），以优化性能。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F41ba5c4ec2414fd34e5a5b8f182cff16?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=GQCK%2FLVA%2BR3vzEPnOpIbtXBC9Ow%3D)

在AI规模扩展网络（东-西向流量）中，存在诸多挑战。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fd1da64b8a8bcf086acb96032adf8a95c?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=lZvi8x1it63VtbVNA5aar5zV%2F18%3D)

AMD强调网络性能直接影响系统整体性能，尤其是在NIC与GPU 1:1配比的情况下，网络性能对成本高昂的GPU影响尤为显著。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F76ff6bb812630a1e6a5a186143f5a61a?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=0nJDt15JDngjRdEcOjNNvNHD3z4%3D)

高利用率的AI网络推动了对更快交换机和NIC的需求。链路问题可能导致系统性能下降，因此数据包喷射（Packet
Spraying）和重排序（Reordering）变得越来越常见。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F783b55e4ad82ecf78e5e3dd38a0b21e3?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=bOR291u3L3DgrOOXcHF4GhGsIV4%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fbafdcc63d4f44152e5be4980df6d65ee?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=G9SRWgt0yVEDGH5LLcpl1JUJWvI%3D)

在网络和节点层面可能出现拥塞，AMD为此设计了拥塞控制机制（Congestion Control）。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F20f76189729ff6ac203bbfd2aa13efd7?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=JhhQyay7nHSq%2F%2BSz1aC0I%2B70lsM%3D)

在复杂的大型AI网络中，数据包丢失可能影响训练任务的稳定性，AMD对此进行了优化。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F4b116d1f1f669b8a210ea286206c7b43?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=QhEnUfz1NLn2JRxFAaKBhiUWfdg%3D)

UEC通过以太网技术解决上述挑战，不仅限于NIC，还对新型交换机芯片产生重大影响，构建了一个解决这些问题的生态系统。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fd57a7ef58195dec3db6bd899db66df2c?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=S87%2BeSUCDlAOah1q5bA3wFyQn04%3D)

AMD表示，其Pollara 400 NIC已为UEC做好准备，支持多路径传输（Multipathing）、拥塞控制和选择性确认（Selective
Acknowledgment，SACK）等功能。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ff231cfcb1c9baaeb35268af8997765d5?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=Eeq3ew3DNN3MnSwLFvMOiwelGv0%3D)

UEC的多路径传输机制帮助解决了之前提到的许多挑战。AMD展示了发送端和接收端的熵值处理方式。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fd04af01c718eb925beabf36963ce0186?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=PDX9nhW38CUlMmXfwqqd9VuH%2Bgg%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fef8b18bd9d31c8d0e1e9b89d9211e2a7?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=jz4G%2BLODp0V7NIbdsHyeZyBpKmA%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F395edae4574dbb3c5d57c077cba7bbab?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=YnMGeKchq5O5GOChDAxO24S9nHM%3D)

UEC的拥塞控制机制在发送端和接收端均有实现。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F57a2a70a7545feee58741f0713d24ca4?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=G%2F%2Bm8KIi8pKli9oktSmiHMW2IfI%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F5511c13d44efe1061b73fb65894f8e54?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=iDP3%2F1CdCNIC4xefYvVthpXP4w4%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F296bd78d832c6da8d8d56156b5c27429?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=IAJccuTzbaroRd7nCK8WPvTMOKs%3D)

UEC支持选择性确认（SACK），包括接收端和请求端的实现。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F9601467fc21d98ad8bd4fc8fea2cab02?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=hYqOUMi6%2B6EGLyr7f26I5hXkt%2Bc%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fdf2f9e3a4a18d5fdfcd3e349f0f5c1c5?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=VpffYy0rX78mVVasNr10ul2ZdBk%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fdc0e6f376563f7d6e5c6360a0d737d09?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=vCqjWsqsBamB6uRImCNzSPmQtmk%3D)

AMD表示，结合UEC-ready的Pollara 400 NIC，其RCCL（AMD对标NVIDIA NCCL的通信库）能够显著提升性能。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F08e47cd4dbc7c3341312eb5816b67bf9?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=u%2BxBNVlf1Jtm8ZOEyxjKg5CZdS4%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F762fa23cdcfbf72d91310ba70861acd2?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=hpAbYEFkGlXObRJyHW6wrtdcCsc%3D)

总的来看，Pollara 400 NIC利用P4架构和UEC技术，为AI网络提供了高性能和可编程性。

NVIDIA ConnectX-8 SuperNIC

在Hot Chips 2025上，面对众多400G NIC的竞争，NVIDIA推出了已开始出货的ConnectX-8 SuperNIC。这是一款支持PCIe
Gen6的NIC，速率高达800GbE。此外，它还具备内置PCIe Gen6交换机等常被忽视的功能。

NVIDIA指出，AI训练与推理具有不同的特性，因此对网络的需求也不同。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F8ec3ac81a5456c561aa7aee5d540f967?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=Iats0qe6fvsAfc8i7vd5Q%2FDTLQw%3D)

与Enfabrica
ACF-S类似，NVIDIA将其NIC称为SuperNIC。需要注意的是，ConnectX-8同时支持Spectrum-X以太网和Quantum-X
InfiniBand。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F7e627165f8e2afcc1f5a9337617bd3b4?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=nANknSc4TlQBsQ1blMekDHu0W4s%3D)

ConnectX-8虽然外观上使用x16连接器，但实际支持48条PCIe Gen6通道，并内置PCIe Gen6交换机。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F5b335fcf950d2872a0db3035687389d9?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=Fm%2FTW3NQ%2Fho9NESJVRDZ81qZ5p4%3D)

NVIDIA展示了ConnectX-8在不同消息大小下的RDMA展性能，达到800G。Broadcom在其Tomahawk
Ultra发布会上提到64KB对AI和HPC的重要性。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fd7357d9eb527e6ec1162958fd82059d9?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=OHriTzpCY9CeeuDIvVVYKIH%2FQEI%3D)

NVIDIA展示了NCCL AllReduce和AlltoAll在不同消息大小下的吞吐量表现，但未包括64KB和128KB的性能数据。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fe94292665c2585c3714133e0b83d16df?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=6D9Sa22Fr84rKAI66ENIafg11dc%3D)

NVIDIA表示，传统数据中心组件定义明确，而如今数据中心成为计算单元，ASIC需要承担连接GPU与集群其他部分的职责（除了用于规模扩展的NVLink连接外）。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fe6115e18fe424ecbf82a0d38bd495528?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=%2Fh7l4mqD%2F52okTcsEqvpNuMMz4E%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F432c125f646275c0a64583b46683c9d1?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=1fHlF3fWkIypnE3GIprzmYYWFpU%3D)

NVIDIA表示，GB300 NVL72是ConnectX-8 PCIe Gen6 SuperNIC的首次部署。由于NVIDIA Grace运行在PCIe
Gen5速率，其与Grace CPU之间采用Gen5 x16链路，与B300 GPU之间采用Gen6 x16链路，另有一条Gen5
x4链路连接至SSD。这解决了NVIDIA的一个挑战，因为Grace不像大多数服务器CPU那样支持x4分叉。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F5f1a891f13b75bdd251d0192ce529b86?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=Wnv9zVbmL41gmSQSe3FsYyluft0%3D)

NVIDIA在NVIDIA MGX
PCIe交换板中也使用了ConnectX-8。通过该板，NVIDIA能够将Broadcom交换芯片从PCIe卡平台中移除，同时为未来的B300 PCIe
GPU提供PCIe Gen6连接，而非PCIe
Gen5。这些PCIe形态的GPU尚未发布，但NVIDIA多年来一直在生产PCIe版本的GPU，该板的目标是支持即将推出的基于B300的PCIe Gen6卡。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F9e1d6ceb431adea831f49edb20a00065?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=Ek7rsABAIyh%2F%2BGChzcMDUVkVE%2Fo%3D)

以下是ConnectX-8在Spectrum-X以太网中的扩展表现，包括集成的Spectrum-X以太网交换机，以实现可扩展性。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F8ee51d7942e533f22b357626ccaebcd1?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=sPCLW%2Bi5AXmBEoY08rKD54VLwrY%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fe2e1065bb8dd353e3710a1fb5d7c58f6?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=TV6CzMCXh11%2BRgX7f6pC3OV9aUc%3D)

RDMA网络是Mellanox在被NVIDIA收购前成功的关键因素，也是NVIDIA能够扩展到大型集群的原因。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fe039d20fbc392e24927606fae25f9681?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=9tfWBxzPTrV%2Bp725VZ6ruBeZAxU%3D)

以下是PSA（Packet Switching Architecture）数据包处理器的概览。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F2c2ff36fcda1f3a7c472adc4e2662c00?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=nFeDfKbSuRvOaiRqXnjbVva7opo%3D)

ConnectX-8配备了基于RISC-V的事件处理器——数据路径加速器（Data Path Accelerator，DPA）。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fe5484555ae8a34b896eb8b8697fba0d8?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=h38n2ZsGNPejlWsEDJXYQwxckJE%3D)

ConnectX-8支持Spectrum-X以太网的拥塞控制和路由功能，以下是其与DPA协同工作的细节。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F154785d5dec0766b9fd52e70292abab4?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=6VRZOx701MVkV2sDhg4sR%2Fcdolc%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ffdfed2caff393ea4e25cd877f538d9d2?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=OCYO0qdKYqwAarpnZFYu%2B6zAEFc%3D)

NVIDIA展示了一些性能数据，例如训练步骤时间（Training Step Time）。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F4c6bfcb63c4eb2606b5a3825cf4a517f?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=aKStKAnxIotGvuVHg7Pr3fj8NGE%3D)

以下是负载下尾部延迟（Tail Latency）的表现。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F1af0182d124deed4a6ae06703521977c?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=HLev5%2FLsl8UelUhtL6CFwRaPZjI%3D)

除了ConnectX-8 NIC，NVIDIA还介绍了Spectrum-X交换机的相关内容。总体而言，Spectrum-X旨在通过以太网实现快速的AI网络。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F9d9e8fdf056c502f01400f1793b3925d?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=lSAq1QWE0xMdx0jVhIXAEEp70p8%3D)

总结

我们有许可使用多达四张ConnectX-8
NIC，但最终使用了ConnectX-7。由于ConnectX-8（特别是C8240型号）是下一代高速NIC，供应较为紧张。目前若需要高速NIC，ConnectX-8的性能超越了市场上的Broadcom“Thor”
400GbE卡和AMD Pollara 400卡。NVIDIA通过打造整个技术栈，在PCIe Gen6服务器CPU广泛可用之前，就能推动800G
NIC速度并将其集成到系统中。

Broadcom Tomahawk Ultra Ethernet交换芯片

以下是HPC和AI规模扩展网络需求的简要概述：

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F218e303cc0820ac0e8436d50ef35c6f8?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=J5AzYA27fzyCJHJa1lfLDhAep9o%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F3ee8385d1ceea78539d2a90e9139e15b?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=%2BVP5cRWOsLtYRqp3GXGEEeAC9vs%3D)

Broadcom表示，以太网通常被认为不适合这些工作负载，但通过推出Tomahawk Ultra，Broadcom旨在改变这一现状。Tomahawk
Ultra支持512个100G-PAM4端口，意味着它能够处理512个100GbE端口。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F6f549db93b1c58d54f608f6fdebd07d5?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=LWpt052kHCjLIkG3BHdo%2BoHQB%2FM%3D)

Tomahawk Ultra是一款新型51.2T交换机，专为高性能设计，支持网络内计算（In-Network
Computing）、低一致性延迟和高吞吐量。在64字节数据包下，其吞吐量约为每秒770亿个数据包。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F90c0793ec63286bfb35c7361398c437e?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=9w0bsDYNTlUDHL07tl5uZ6ylnEk%3D)

以下是Tomahawk Ultra的数据包转发流水线概览。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F2ddb4da88120046cf6ab73b50dac256c?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=4Z6XSiAHXxNEyU2enQpMjUcK1WQ%3D)

以下再次列出Tomahawk Ultra的关键特性。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F00c6be58c0c9be4f02976f38e6c7c816?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=e2Jq3jAB%2BXrvlUaRJFkWQRr3so4%3D)

Tomahawk Ultra支持链路层重试（Link Layer Retry，LLR）功能，这是一种在交换机低层实现的机制。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F838358cb04a3ce3ee17cd4cf54342ef7?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=w%2Fc%2BReN%2Flj9wckfkVCmeS1cC3%2Fo%3D)

以下是LLR的详细工作原理。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F250a942ad00f5a82df73bb5dd5d868f8?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=nSJath7iexJ6IA9uME1MBTQ6YNA%3D)

Tomahawk Ultra还支持基于信用的流量控制（Credit-Based Flow Control，CBFC）功能，以确保缓冲区安全。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F4d5347a86a3c278eec56fa789c033efc?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=SRmeW8JbJHGVuqTZXh0YZd6qlI4%3D)

Tomahawk Ultra采用了优化的AI网络头部（AI Fabric Header，AFH），通过最小化头部字段来优化头部与有效载荷的比例。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F7a433ae68a16e0625647b6037f778b8e?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=02FtiN%2BT4CODO9xkfFWT%2F7OiwgI%3D)

以下是AFH在规模扩展以太网（Scale-Up Ethernet，SUE）中的工作原理。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F9337ff2f3d7c69923cf7738c60a2598d?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=Lqo0xzn9vBWPuRK4uPYdmZRks9Y%3D)

与NVIDIA类似，Tomahawk Ultra支持网络内计算（In-Network Computing），特别是针对集体操作（Collective
Operations）。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F27a347facf8bc3d18c86c246ad6353c3?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=Z6AXsOAA1dfRpYFumocRzaDntoI%3D)

拓扑感知自适应路由（Topology Aware Adaptive Routing）对于保持网络高效运行至关重要。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fbf120c1178d14705c0be565f5ba140a2?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=Q9fUkxu9KXt8PzYk%2FcK%2FpDRlrJU%3D)

以下是关于交换机可编程可见性（Programmable Visibility）和可观测性（Observability）的详细说明。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F4df7dfec6ebe11fbb8c878516224551e?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=0NAe%2BkrbWeiohpg8MkPbkRt3Kzc%3D)

拥塞控制（Congestion Control）机制确保某些链路不会过载。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F1d60395f63f9b07a462b0713dff99a69?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=glXkZ5q8vggaZ8w2aww9o7fBn1I%3D)

Tomahawk Ultra在所有端口上实现64字节数据包的线速传输。这是该交换机的一大亮点，不仅限于高数据包吞吐量。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F4962bd4493ef004a873b47b49d795ca6?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=jJoPRyZMRl7rp4yGj7QCKQT%2B%2FiI%3D)

Tomahawk Ultra的延迟低至250毫秒。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fabcbcad16a1323bff005f2322bf28c1a?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=PfY%2BM%2F%2FN88TI%2BxNZiJnthnJb9ws%3D)

以下是Broadcom的交换机产品线概览，其中Tomahawk 6是吞吐量高达102.4T的旗舰ASIC。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ffd0cceb2acf4f506deb3fd8bb929d306?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=FKHITA%2F7fl4uCKpIccGGyXJxhKA%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fe062c926f9894a7fe39194b8d7dbe24c?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=50XDTucGeZFjJ7VClbUJr5igim4%3D)

总结

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F176103c692a2fc44a8328167bcc67c37?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=%2FQeVm4EKMz10XFyEpuS8pvI8Y5s%3D)

Tomahawk Ultra无疑是一款非常出色的芯片。Broadcom正在大力推动规模扩展以太网（Scale-Up
Ethernet）项目，我们将拭目以待其部署情况。

更多交流，可加本人微信

（请附中文姓名/公司/关注领域）

![Image](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Facf9c0b9c69a94e01e929fa21a33c598?Expires=1780067380&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=5NFCjx6dacMM6Vwc2FISXMVZtP8%3D)

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 11:09*