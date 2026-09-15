---
direction: both
category: 技术
tags: [GPU互连, HBM4, NVLink, Chiplet, NVL72]
summary: "NVIDIA Rubin GPU四层互连架构从显存到整机柜的深度拆解"
quality: high
processed: 2026-09-12 10:10
---
---
title: "NVIDIA Rubin GPU 互连架构深度拆解：从显存到整机柜的四层数据高速路"
tags:
  - hardware
  - infrastructure
  - design
  - physics
  - semiconductor
  - architecture
  - computing
  - first-principles
  - chip
date: 2026-09-09 21:00
source: GetNotes
score: 10
---

## Original Note

---
note_id: 1920750296148251496
title: "NVIDIA Rubin GPU 互连架构深度拆解：从显存到整机柜的四层数据高速路"
type: link
created: 2026-09-08 11:28:31
source: getnote
kb: 
---

# NVIDIA Rubin GPU 互连架构深度拆解：从显存到整机柜的四层数据高速路

### 🏗️ Rubin GPU 的整体架构长什么样？

Rubin GPU 采用**双计算裸片 + 8颗HBM4显存**的封装布局，核心目标是让数据**又快又省地流动**。
- **计算核心**：单颗GPU含 **224个SM**、**896个Tensor Core**，稀疏NVFP4算力达 **50 PetaFLOPS**。
- **对外接口**：
  - PCIe Gen6 x16 → CPU主机接口带宽 **256 GB/s**
  - NVLink-C2C → CPU-GPU一致性互连带宽 **1,800 GB/s**
  - NVLink 6 → 连NVLink交换机带宽 **3,600 GB/s**
- **安全特性**：支持 **TEE-I/O 可信计算**。
---
### 💾 最外圈的显存层：HBM4 怎么做到又大又快？

8颗HBM4环绕计算裸片，单颗36GB，总容量 **288GB**，总带宽 **22 TB/s**。
- **堆叠结构**：每颗HBM4为 **12-Hi堆栈** = 12层DRAM裸片垂直堆叠 + 1层Base/Logic控制裸片。
- **互连方式**：层间靠 **TSV（硅通孔）** 垂直贯穿连接，底部通过 **Microbump（微凸点）** 连到CoWoS-L中介层。
  说白了，就是把12层内存芯片像叠蛋糕一样摞起来，用垂直通孔穿起来，占地不变但容量翻12倍。
---
### 🔗 裸片之间：为什么一颗GPU要拆成两颗裸片？

因为单颗裸片已顶到**光刻最大面积（reticle-limited）**，塞不下3,360亿晶体管，所以用 **chiplet（小芯片）** 思路拼起来。
- **互连桥梁**：两颗计算裸片之间靠 **NV-HBI（NVIDIA高带宽接口）** 连接。
- **软件效果**：两颗裸片的内存与计算资源完全打通 → 操作系统和CUDA程序看到的是**一颗逻辑GPU**。
---
### 🖥️ CPU 与 GPU 之间：NVLink-C2C 比 PCIe 强在哪？

NVLink-C2C 实现了**硬件级统一地址空间和一致性**，省去了数据来回拷贝的开销。

| 维度 | 传统PCIe（非一致性） | NVLink-C2C（一致性） |
| :--- | :--- | :--- |
| 地址空间 | 内存、显存完全独立 | 统一地址空间 |
| 数据访问 | 需DMA显式搬运 | 直接读写同一份数据 |
| 带宽 | 256 GB/s（PCIe Gen6 x16） | **1,800 GB/s** |
| 延迟 | 高（拷贝开销大） | 低（一方修改另一方立即可见） |
- **适用场景**：连接 **Vera CPU** 与 Rubin GPU，CPU侧最高支持 **1.5TB LPDDR5X 内存**。
---
### 🖧 GPU 与 GPU 之间：72颗GPU怎么连成一颗巨型GPU？

靠 **NVLink 6 + NVLink Switch** 组成全互连拓扑，单柜72颗GPU**单跳可达**。
- **整机柜配置**：NVL72机柜 = 18个计算托盘 + 9个交换托盘
  - 每个计算托盘：2个Vera CPU + 4个Rubin GPU
  - 每个交换托盘：4颗NVLink 6 Switch芯片
  - 总计：**36颗NVLink 6交换机**，全对全互连
- **物理实现**：
  - **Spine Connector（背板连接器）**：托盘盲插在机柜背板上，前面板不直连
  - **Cable Tray（线缆托盘）**：背板侧用线缆托盘实现任意GPU ↔ 任意Switch的全连接
- **单链路带宽**：NVLink 6 单链路带宽 **3,600 GB/s**。
---
### 📝 补充细节
- 四层互连从内到外依次是：**显存层（HBM4）→ 裸片间（NV-HBI）→ CPU-GPU间（NVLink-C2C）→ GPU间（NVLink 6）**，每一层都在解决"数据怎么又快又省流动"的同一个问题。
- 原文提示下期将讲解数据进入GPU后的**传输和处理流程**。

---
*getnote | 2026-09-09 21:00*


---

## Related Notes

[[SDI化合物键_四型架构]]
[[iNEST-MOC]]
[[FPGA原型]]
