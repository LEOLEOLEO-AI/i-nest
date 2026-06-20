---
title: "Roofline模型"
created: 2026-04-17
note_id: "1907408673878378000"
tags:
  - "get-笔记"
  - "AI研究"
---

# Roofline模型

## 摘要

**Roofline 模型（屋顶线模型）** 是由加州大学伯克利分校（UC Berkeley）于 2008 年提出的**可视化性能分析模型**，核心作用是**直观判断程序 / 算法在特定硬件上的性能瓶颈：是受限于计算能力（算力墙），还是受限于内存带宽（内存墙）**。  ![image](https:

## 正文

**Roofline 模型（屋顶线模型）** 是由加州大学伯克利分校（UC Berkeley）于 2008 年提出的**可视化性能分析模型**，核心作用是**直观判断程序 / 算法在特定硬件上的性能瓶颈：是受限于计算能力（算力墙），还是受限于内存带宽（内存墙）**。

![image](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fd313e86d75f0b3d6924e8f08f087c0f9?Expires=1779004757&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=q2Rlf0pqLiF2ykdQhlQJdaUCLoM%3D&x-oss-process=image%2Fresize%2Cm_lfit%2Cw_720%2Ch_3240)

### 一、核心原理与构成

模型以**二维对数坐标系**呈现：

- **横轴（X 轴）**：**算术强度 (Arithmetic Intensity, AI)**
  - 定义：**每字节内存访问所执行的浮点运算数**（FLOPs/Byte）
  - 反映算法的 “计算密度” 或 “数据复用率”
- **纵轴（Y 轴）**：**实际性能 (Attainable Performance)**
  - 单位：FLOP/s（通常为 GFLOP/s 或 TFLOP/s）
- **两条关键 “屋顶” 线**（硬件理论上限）
  1. **水平顶线（计算上限）**
    - 代表硬件的**峰值计算性能**（Peak Performance）
    - 公式：`Performance = Peak FLOP/s`
    - 当算法计算强度极高时，性能触及此线，为**计算受限 (Compute-bound)**
  2. **斜线（带宽上限）**
    - 代表硬件的**内存带宽**（Memory Bandwidth）
    - 公式：`Performance = Bandwidth × Arithmetic Intensity`
    - 当算法计算强度低时，性能沿斜线上升，为**内存受限 (Memory-bound)**
- **脊点 (Ridge Point)**
  - 两条线的交点。其横坐标是**达到峰值性能所需的最小算术强度**。
  - 若算法强度 > 脊点：计算受限；若 < 脊点：内存受限。

### 二、核心公式

**实际性能 = min (峰值计算性能，内存带宽 × 算术强度)**

- 直观理解：程序性能由 “跑得慢的那条腿” 决定 —— 要么算不动，要么读不快。

### 三、如何读图与定位瓶颈

1. **计算受限区（脊点右侧）**
  - 表现：性能点贴近**水平线**
  - 原因：数据喂得够快，但 ALU / 张量核心跑满
  - 优化方向：提升指令级并行（ILP）、向量化、利用 FMA/Tensor Core
2. **内存受限区（脊点左侧）**
  - 表现：性能点贴近**斜线**
  - 原因：算力闲置，数据搬运跟不上
  - 优化方向：提升缓存命中率（分块 /tiling）、数据复用、减少非连续访问
    ![image](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fb0b99ff67e4285c3c10b7cecfeb86d19?Expires=1779004757&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=I0dBZwtZdTBSabDLNReHYVoVVEU%3D&x-oss-process=image%2Fresize%2Cm_lfit%2Cw_720%2Ch_3240)

### 四、进阶：层级 Roofline 模型

现代芯片（CPU/GPU/TPU）存在多级缓存（L1/L2/L3/HBM），每层带宽与容量不同。**层级 Roofline**会画出多层斜线，精准定位瓶颈在**片上缓存**还是**片外 DRAM**。

![image](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ffac83c700368d44cb0d1f2ce8267a000?Expires=1779004757&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=r5YZ0ygG6JoDcw5z9I3q8UX%2Fmas%3D&x-oss-process=image%2Fresize%2Cm_lfit%2Cw_720%2Ch_3240)

### 五、典型应用场景

- **HPC 高性能计算**：优化矩阵运算（GEMM）、FFT、分子动力学
- **AI 模型部署**：分析 LLM、CNN 推理是计算受限（大批次）还是带宽受限（小批次 / 解码）
- **硬件设计评估**：衡量芯片算力与带宽的平衡设计（如脊点位置是否合理）

### 六、常用分析工具

- **NVIDIA**：Nsight Compute (NCU)
- **AMD**：Omniperf
- **Intel**：Advisor
- **通用**：LIKWID、PAPI（性能计数器采集）

### 总结

Roofline 模型是**性能优化的 “X 光片”**，它抛弃复杂公式，用一张图清晰告诉你：**你的代码瓶颈在哪，优化方向是什么**。

---
*来源：Get笔记 | 类型：plain_text | 入库：2026-04-29 08:21*

## Related Notes

- [[AgentEvolver vs AlphaEvolve：AI自我进化的两条核心路线对比 🧠]]
- [[AI双引擎的未来之光]]
- [[AI编码代理的质的飞跃：v3.3透明化与v3.4连续性技术解析]]
