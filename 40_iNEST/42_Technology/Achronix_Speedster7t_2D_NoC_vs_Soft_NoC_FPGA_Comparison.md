---
direction: both
category: 技术
tags: [FPGA, NoC, 片上网络, Achronix, 硬件架构]
summary: "Achronix硬件2D NoC相比软NoC资源省7倍、带宽高24倍、编译快2.4倍"
quality: high
processed: 2026-09-23 18:45
---
---
title: "Achronix Speedster7t 2D NoC vs 软NoC：FPGA片上网络性能对比白皮书"
tags:
  - architecture
  - semiconductor
  - hardware
  - chip
  - network
  - fpga
date: 2026-09-22 22:24
source: GetNotes
score: 7
---

## Original Note

---
note_id: 1922003400099298080
title: "Achronix Speedster7t 2D NoC vs 软NoC：FPGA片上网络性能对比白皮书"
type: link
created: 2026-09-21 23:39:15
source: getnote
kb: 
---

# Achronix Speedster7t 2D NoC vs 软NoC：FPGA片上网络性能对比白皮书

### 🏗️ 为什么要在FPGA里做2D NoC？

高带宽数据流需要**高效跨接口传输**，传统软实现资源占用高、性能差。
- **背景**：现代算法加速工作负载增多，高速接口间数据搬运成为瓶颈。
- **方案**：Achronix Speedster®7t FPGA 集成**硬件2D NoC**（二维片上网络）。
- **对比对象**：米兰理工学院 2017 年开源软2D NoC（虫洞前瞻预测切换、单向mesh结构）。
- **测试基准**：19个AlexNet 2D卷积（conv2d）实例 + GDDR6 存储接口。
- **对比维度**：资源占用、性能、带宽、设计与编译时间。

### 📊 两种NoC的资源占用差多少？

硬件2D NoC的**LUT占用仅为软实现的1/7**，布局更规整。

| 资源类型 | Speedster7t 2D NoC | 软2D NoC | 倍数 |
| :--- | :--- | :--- | :--- |
| LUTs | 10,812 | 80,365 | 7× ↓ |
| BRAMs | 1,178 | 1,724 | 1.5× ↓ |
| MLPs | 1,140 | 1,140 | 1×（相同） |
- **硬件NoC设计细节**：
  - 共使用 **38个NAP**（NoC访问节点），器件总共有80个可用NAP。
  - 每个conv2d实例占用 **64个MLP**，垂直方向覆盖2个NAP。
  - 采用**双AXI-4**接口（读写分离），GDDR6直接连到NoC，无需额外节点。
- **软NoC设计细节**：
  - 配置为 **5×4 mesh** 网络，第20个节点预留给GDDR6。
  - 每个节点需要存储器存储和转发flit（流控制单元）。
  - 布局不规则，资源分散在整个器件上。
  说白了，软NoC要自己用逻辑搭路由器和缓存，硬件NoC是芯片里预先做好的"高速公路网"。

### ⚡ 性能和带宽差距有多大？

硬件NoC频率是软实现的**7倍**，带宽是**24倍**。
- **运行频率**：
  - 硬件2D NoC → **565 MHz**，关键路径在conv2d逻辑内，加节点不降频。
  - 软2D NoC → 5×4 mesh下仅 **82 MHz**，2×3 mesh下94 MHz，规模越大越慢。
  - 软NoC关键路径在mesh网络本身，而非计算逻辑。
- **单节点带宽**：
  - 硬件2D NoC → **512 Gbps**（2 GHz 256位双向总线 + 双NAP连接）。
  - 软2D NoC → **21 Gbps**（五路交叉开关，82 MHz节点间频率）。
- **布线差异**：硬件NoC布线规则整齐，软NoC布线复杂拥挤。

### ⏱️ 设计和编译时间能省多少？

硬件NoC的**编译时间不到软实现的一半**，设计工作量大幅减少。
- **设计时间缩短**：
  - 采用标准 **AXI-4 接口**，设计师无需重新学习。
  - 内置跨时钟域、流量控制、地址解码等功能，用户逻辑不用再实现。
  - 设计师只需专注加速器本身，将其连到NAP即可。
- **编译时间对比**：
  - 硬件2D NoC → **50分钟**
  - 软2D NoC → **120分钟**
  - 提速约 **2.4倍**
- **原因**：资源占用少 → 布局布线逻辑少 → 工具运行更快。

### 📌 补充细节
- **测试工具版本**：Synplify Pro 2021.03X + ACE 8.6.1。
- **测试器件**：Achronix **AC7t1500**（Speedster7t系列）。
- **通信模式**：测试中conv2d节点之间不通信，仅每个节点与GDDR6之间有数据传输。
- **行业地位**：Achronix是**第一家**集成2D NoC的FPGA厂商。

---
*getnote | 2026-09-22 22:23*


---

## Related Notes

[[iNEST-MOC]]
[[paper1_iNEST_core_architecture]]
[[FPGA原型]]
[[SDI化合物键_四型架构]]
