---
title: "NVIDIA 2026年AI光学互连技术路线图：共封装硅光子学引领吉瓦级AI工厂"
source: "https://mp.weixin.qq.com/s/TNce_CvsNKV7rTyrzA3hmA"
created: 2025-09-09
note_id: "1887016281899638120"
tags:
  - "AI链接笔记"
  - "共封装光学(CPO)"
  - "硅光子学"
  - "AI数据中心"
  - "get-笔记"
  - "AI研究"
---

# NVIDIA 2026年AI光学互连技术路线图：共封装硅光子学引领吉瓦级AI工厂

## 摘要

🔬 **AI集群对光学互连的迫切需求**   现代AI训练需同步数千至数百万GPU，传统电互连在800Gbps+速率下存在三大瓶颈：   - **高信号损耗**：200Gbps通道电损耗达22dB，需复杂补偿电路   - **高功耗**：传统交换机每端口功耗约30W，冷却成本显著   - **延迟增

## 正文

数据中心AI工作负载的快速扩展暴露了传统电互连（Electrical
Interconnect）的局限性，促使业界转向光学技术，以实现更高的带宽和更低的能耗。在2025年8月24日至26日于斯坦福大学纪念礼堂举办的Hot
Chips 2025大会上，NVIDIA详细介绍了其将硅光子学（Silicon Photonics）和共封装光学（Co-Packaged
Optics，CPO）技术集成到下一代AI系统的路线图。Gilad Shainer在题为“面向吉瓦级AI工厂的共封装硅光子交换机”（Co-Packaged
Silicon Photonics Switches for Gigawatt AI Factories）的演讲中，阐述了从2026年起在AI
GPU间部署基于光通信的计划，这与行业应对大规模GPU集群数据需求的趋势相一致。

AI集群对光学互连的迫切需求

现代AI训练和推理需要同步数千甚至数百万GPU，将整个数据中心视为单一计算单元。这种规模对网络提出了重大挑战：随着距离增加和速率提升至800
Gbps或更高，铜线缆上的电信号面临高信号损耗、延迟增加和显著的功耗问题。例如，在传统架构中，交换机ASIC的信号需通过印刷电路板和连接器传输后才转换为光信号，在200
Gbps通道上可产生高达22 dB的电损耗。这需要复杂的补偿电路，将每端口功耗推高至约30瓦（W），并增加了冷却需求。

CPO通过将光转换引擎直接嵌入交换机ASIC旁，缩短电信号传输路径，将损耗降至约4
dB，从而将每端口功耗降低至9瓦（W）。这种集成方式减少了易故障的组件，简化了设计并提升了系统可靠性。行业分析表明，此类方法可将能效提高3至4倍，同时改善信号完整性并通过简化组装缩短部署时间。NVIDIA的重点反映了行业共识：随着AI集群扩展至吉瓦（GW）级，光学互连正从可选增强变为关键基础设施。

NVIDIA的2026年路线图：Quantum-X与Spectrum-X平台

NVIDIA的战略依托TSMC的紧凑通用光子引擎（Compact Universal Photonic
Engine，COUPE）平台，该平台通过SoIC-X等先进封装技术将65nm电子集成电路（EIC）与光子集成电路（PIC）堆叠。COUPE路线图分阶段展开：第一阶段为OSFP连接器提供1.6
Tbps的光学引擎；第二阶段采用CoWoS封装实现主板级6.4 Tbps光学互连；第三阶段目标为处理器封装内实现12.8 Tbps，进一步降低延迟和能耗。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F409e3d41bb969d75c901f000cadaf115?Expires=1780067389&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=xgwh3weSFGHsT3AthC2FUjT2Flg%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F957d5ce32ab82e8b5c227c7593bc7ba6?Expires=1780067389&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=zVz0gF3OugYuNPJzKpNd03oSefs%3D)

在InfiniBand方面，NVIDIA计划于2026年初推出Quantum-X交换机，提供115 Tbps的总吞吐量，支持144个端口，每端口运行在800
Gbps。这些交换机集成了具有14.4 TFLOPS网络内处理能力的ASIC，并支持第四代可扩展层次聚合减少协议（Scalable Hierarchical
Aggregation Reduction Protocol，SHARP），优化AI工作负载的集体操作。液冷技术是标配，以应对密集部署的热管理需求。

在以太网方面，Spectrum-X Photonics平台计划于2026年下半年发布，基于Spectrum-6 ASIC，包括SN6810交换机（提供102.4
Tbps带宽，128个端口，每端口800 Gbps）和更大的SN6800（扩展至409.6 Tbps，512个端口，每端口800
Gbps）。关键创新包括使用微环调制器和可拆卸光纤连接器的1.6T
CPO芯片，NVIDIA已在实验室环境中展示了其性能。该架构在固定功耗预算下可提升GPU利用率约3倍，并将激光器数量减少约4倍，相较于可插拔光学模块。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ffa49f2121c81e62be938fcc1b742329e?Expires=1780067389&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=m%2BgiPQ7q%2Bceb1sto%2B3%2F6u38EWPc%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F47802e62d9d2ea49f9da9962ef296f31?Expires=1780067389&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=cdHTe3YwtsFn3LeVwX73VcS1AGM%3D)

此外，NVIDIA推出Spectrum-XGS以实现“跨站点扩展”（Scale-Across）网络，支持500米起的最小抖动通信。通过距离感知算法，该平台在多站点AI训练中可将效率提升1.9倍。CoreWeave等早期采用者预计将部署这些系统，显示其在超大规模环境中的实际应用。

TSMC的赋能角色与更广泛的生态系统

TSMC的参与至关重要，其在2025年光纤通信展（OFC
2025）上进一步披露的硅光子计划为低阻抗、高能效互连提供了核心IP。TSMC的方法强调异构集成，将电子与光子技术结合以应对AI的I/O瓶颈。虽然TSMC的路线图与NVIDIA的时间表紧密对齐，但它也支持其他企业，例如Himax等公司将在供应链中受益。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fc0e87b0455f98487e3a3cdc414920e8b?Expires=1780067389&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=HmW5uqZs0QQnX%2BVFihcDvoINUdQ%3D)

然而，挑战依然存在。硅光子学需要精确的光学组件对齐，而扩展至12.8
Tbps将要求材料和封装技术的进步以进一步降低延迟。能效提升虽显著，但需平衡液冷复杂性及新型光纤基础设施的需求。

竞争动态：AMD与新兴挑战者

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F6bdb662c5aaa09738f63b24553567f5e?Expires=1780067389&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=KcOdnHdGtj42ImMK%2FScdLVl41eA%3D)

NVIDIA的声明正值竞争加剧之际。AMD于2025年5月收购Enosemi，直接回应了这一趋势，增强了其在光子集成电路和CPO技术方面的能力。Enosemi是一家位于硅谷的公司，此前与AMD和GlobalFoundries合作，专注于硅光子学的定制材料和IP，使AMD能够在CPU、GPU和自适应SoC中集成光学技术。这一收购加强了AMD的全栈AI产品线，继ZT
Systems和Silo AI等收购之后，使其在数据中心互连领域对NVIDIA构成挑战。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F7d3e9843a8a00da817b5ce4351a013c2?Expires=1780067389&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=gfSr0L8q%2FS1lnRQFjpaFXIUlm94%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fdee41dadba2dedd2cbbebaf07419efa8?Expires=1780067389&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=c0GRTc4CEmxdmbHhy4DEqfT76sQ%3D)

其他创新者，如Lightmatter在Hot Chips 2025上展示的Passage M1000平台，也在推进面向芯片组时代的CPO解决方案。OFC
2025和IEEE
ECTC等行业论坛强调了CPO在减少占地面积和损耗方面的作用，异构集成路线图突出光子学在满足AI功耗和带宽需求中的重要性。地缘政治因素增加了复杂性：报告显示，中国在硅光子学领域的投资激增，可能加速全球采用，但也引发了供应链安全担忧。

对未来AI基础设施的启示

到2026年，这些光学技术有望实现更快的首次Token生成时间（Time-to-First-Token，TTFT）和改进的多租户性能，减少因网络抖动导致的GPU空闲时间。NCCL（NVIDIA
Collective Communications
Library）吞吐量和混合专家模型（Mixture-of-Experts，MoE）的专家调度性能将显著提升，特别是在以太网环境中，Spectrum-X与通用交换机的差异化尤为明显。然而，这一转型涉及权衡：重新设计的初期成本较高，以及厂商（如NVIDIA）将光学技术与专有协议绑定的潜在生态锁定风险。

展望未来，硅光子学与先进封装的融合可能重新定义AI硬件，扩展至边缘计算。随着带宽需求持续超越摩尔定律，CPO代表了关键的演进，其成功将取决于协作标准和制造可扩展性。Hot
Chips 2025强调了这一转变，表明基于光的互连正成为高性能计算的基石。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F33a8a39ebc97658c7a34bc4f5091a216?Expires=1780067389&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=iX%2BV4MbJDHYakRzv93jvCjb3Yss%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fc7fed16b525077d0e19b0f2013b552f0?Expires=1780067389&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=u%2F8A%2B66T7LjSdxtsfPCHRjTD4ok%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F5a9f915167024ab2244a498e91ff455f?Expires=1780067389&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=UoG2QgqckId3iB97scTTJqLEDUM%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F3fecf1e91670967e46c423277026a7d3?Expires=1780067389&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=cuyQb7TIdgpANDvrfqXEUaUqpnM%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F55233c1a25dba3c776dee40c9b2479e6?Expires=1780067389&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=f8YcT%2BQe8MguVP8LNZlYgdhMPuM%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fcff6745e32a4627ba947db37015d1587?Expires=1780067389&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=suapf2GXl%2Fb6RVepxEp8o0kJJM0%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Feb975698ed36ec94745e318709b70e6e?Expires=1780067389&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=4tHUJRvuNZdebzh7lLOIIAjNIb0%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fa49d485827f32c9e448c1d11e117eb96?Expires=1780067389&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=Ron37tMo8IIpjB%2Bu9JBf7OU1sFo%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F8045052952e530b4fb8cfc95676fab01?Expires=1780067389&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=2mL8ZRrgWHvOd4WgmdQDhnF7oM0%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F57377eedbcf2311ff1227a49c8d92c05?Expires=1780067389&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=wQIs3qx%2FbP0ux4avxkxOM7DHR3o%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F9535a4d373058484b14fc5b37242137c?Expires=1780067389&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=yIz8hwI70C8GeGTlbz4Sm4x%2F%2FWM%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F33a712d991f03518a2d0bbdb8e4d13a2?Expires=1780067389&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=Vc7AFYqr%2F%2BN1aLHYeZ95tCW%2Bl30%3D)

更多交流，可加本人微信

（请附中文姓名/公司/关注领域）

![Image](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F2ab58a1c8d50603f16674c8b0203a060?Expires=1780067389&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=JC%2FdO%2B1j5acX6o1FtW51fU3mZMQ%3D)

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 11:09*