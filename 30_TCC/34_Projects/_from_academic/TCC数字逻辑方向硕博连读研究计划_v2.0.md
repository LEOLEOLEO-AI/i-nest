---
title: "TCC数字逻辑方向硕博连读研究计划 — 拓扑中心计算的工程实现与理论创新"
date: 2026-07-07
version: v2.0
status: Final
author: TCC/iNEST Research Group
student_profile: 推免研究生, 2026年9月入学, 硕博连读
direction: TCC数字逻辑与硬件工程
advisors: 天津大学/NDSC TCC工程团队
tags:
  - TCC
  - 数字逻辑
  - FPGA
  - RTL设计
  - SDI交换芯片
  - 硕博连读
  - 研究计划
  - 人才培养
replaces: TCC数字逻辑方向硕博连读研究计划_v1.0.md
---

# TCC数字逻辑方向硕博连读研究计划 v2.0

> **学生画像**: 推免研究生，2026年9月入学，硕博连读（2+3年）
> **研究方向**: TCC数字逻辑与硬件工程实现
> **总体定位**: 在TCC理论体系指导下，成为TCC计算范式从纸面定义到硅基实现的核心工程力量。
>
> **v2.0说明**: 精简为范式概述与方向引导。具体课题由学生自主阅读知识库后，在导师指导下选定。

---

## 一、TCC计算范式概述

### 1.1 什么是TCC

**TCC = Topology-Centric Computing（拓扑中心计算）**，是邬江兴院士团队提出的新一代计算范式。

**核心判断**: 在通信受限计算中，网络拓扑不是静态背景，而是直接影响系统性能、能效与可扩展性的**第一性设计变量**。

**范式转换**:

| 维度 | 节点中心（当前主流） | 拓扑中心（TCC） |
|------|-------------------|---------------|
| 拓扑绑定 | 编译时静态确定 | 运行时微秒级液态切换 |
| 硬件底座 | 训推芯片架构割裂 | 同一底座，拓扑自适应 |
| 任务适配 | 面向单一任务优化 | 多任务液态切换 |
| 网内计算 | 有限或无 | R/T/C 原语原生支持 |

### 1.2 技术体系三层架构

```
        理论层                    硬件层                     验证层
  ┌──────────────┐    ┌──────────────────────┐    ┌──────────────┐
  │ Route-Transform│───▶│ SDI交换矩阵 + R/T/C原语 │───▶│ FPGA原型 →   │
  │ 分解定理        │    │ TCC-Link协议栈         │    │ Chiplet流片  │
  │ SDI化合键理论   │    │ Page模板拓扑切换        │    │ SDSoW晶圆级  │
  └──────────────┘    └──────────────────────┘    └──────────────┘
```

### 1.3 R/T/C 原语体系（16原语）

| 类别 | 全称 | 数量 | 定义 |
|------|------|:--:|------|
| **R** | Route（路由原语） | 6 | 定义数据在计算节点间的集体通信模式 |
| **T** | Transform（变换原语） | 6 | 定义节点内部执行的数学变换操作 |
| **C** | Control（控制原语） | 4 | 定义拓扑切换、时钟同步、数据搬运控制 |

> R: FUSE / PULL / CAST / SWAP / PIPE / MESH
> T: GEMM / FOLD / MAPS / SCAN / LOOK / SPEC
> C: LINK / TICK / SYNC / MOVE
>
> 详见 [TCC_Knowledge_Base_Baseline_v2.0.md](http://127.0.0.1:8899/home/work/.openclaw/workspace/30_TCC/TCC_Knowledge_Base_Baseline_v2.0.md)

### 1.4 关键工程概念

- **SDI交换矩阵**: 软件定义互连的物理实现——可运行时重构的Crossbar网络，是液态拓扑的硬件基座
- **Page模板**: 预编译的拓扑配置快照（~1-4KB），通过C.LINK在<100ns内原子提交
- **TCC-Link**: TCC原生协议栈，L1物理层→L2链路层→L3传输层→L4原语层
- **双缓冲拓扑切换**: 影子缓冲区预加载新拓扑，Commit瞬间指针交换，数据路径不中断

---

## 二、数字逻辑方向可开展的工程任务类型

以下为任务**类别**，非具体课题清单。具体课题由学生自主阅读知识库后在导师指导下选定。

### 2.1 原语引擎RTL设计

将16原语从语义定义变为可综合RTL代码。这是TCC硬件化的第一道工序。

**R类原语（通信）的硬件挑战**:
- 信用制多目标流控（广播时避免慢速端口阻塞快速端口）
- 蝶形归约流水线（AllReduce的硬件级优化）
- 非阻塞全连接交换（AlltoAll的单周期Crossbar调度）

**T类原语（计算）的硬件挑战**:
- 拓扑自适应脉动阵列（同一硬件在Butterfly/Mesh/Ring拓扑间切换数据流）
- 混合精度数据路径（FP16/FP32/INT8动态切换）
- 硬件共享设计（归约树可同时服务于R.FUSE和T.FOLD）

### 2.2 SDI交换矩阵微架构

液态拓扑的物理载体。核心指标：路由延迟<5ns，拓扑切换<1μs（ASIC目标）。

**关键设计问题**:
- 可扩展Crossbar拓扑（4×4→16×16→N×N）
- 双缓冲配置存储与原子指针交换
- 带宽-延迟-功耗三相权衡的帕累托最优设计

### 2.3 TCC-Link协议栈实现

从链路层帧格式到L4原语消息的完整协议栈RTL实现。

**关键设计问题**:
- 信用制链路层流控的硬件实现
- 可靠传输的Go-Back-N vs 选择性重传
- 原语消息的序列化/反序列化（与Crossbar的接口）

### 2.4 FPGA原型验证

将RTL设计部署到FPGA（VU13P/VCK190），建立完整的验证体系。

**关键技能**: Vivado/Vitis工具链、cocotb验证框架、时序收敛、ILA在线调试、性能基准测试

### 2.5 ASIC前端设计与Chiplet流片

从FPGA原型到ASIC GDSII的完整数字IC流程。

**关键技能**: 综合（DC/Genus）、DFT、布局布线（Innovus）、STA签核、MPW提交

### 2.6 系统级集成与板卡设计

多Chiplet在Interposer上的集成、DDR/HBM内存子系统、高速SerDes接口。

---

## 三、预期创新方向

### 3.1 工程创新

| 方向 | 核心问题 | 创新空间 |
|------|---------|---------|
| **原语硬件共享架构** | 16种原语能否在统一微架构上实现？ | 可显著降低面积和验证成本 |
| **原子拓扑切换电路** | 如何保证切换期间数据不丢包、不重复？ | 双缓冲+流水线气泡压缩 |
| **拓扑自适应计算** | 同一脉动阵列如何适配不同通信拓扑？ | 数据流可重构 |
| **网内归约加速** | 归约操作在Crossbar内完成vs搬回PE再算？ | 延迟和功耗的阶跃改善 |

### 3.2 理论创新（博士阶段）

> 以下为建议方向，非强制要求。理论创新应与工程实践紧密结合。

| 方向 | 核心问题 | 数学工具 |
|------|---------|---------|
| **R-T硬件映射理论** | Route和Transform在硬件层面是否存在统一实现框架？ | 数据流图同构、组合优化 |
| **拓扑-精度对偶** | 拓扑切换频率与计算精度的定量关系？ | 信息论、误差传播分析 |
| **最优Page调度** | 给定任务序列，如何选择拓扑切换序列使总开销最小？ | 图论最短路径、动态规划 |
| **SDI可扩展性理论** | SDI交换网络的规模极限及其数学证明？ | 排队论、网络演算 |

---

## 四、五年节奏建议

```
硕士阶段（2026.09-2028.06）              博士阶段（2028.09-2031.06）
═══════════════════════                  ═══════════════════════
                                                                  
课程基础 → 工具链掌握 → 首个原语RTL      全原语IP核 → Chiplet流片 → 理论创新
          → FPGA原型验证 → 硕士论文        → 系统验证   → 博士论文
                                                                  
输出: 1-2篇会议论文 + 1-2项专利           输出: 2-3篇期刊论文 + 3-5项专利
      3-5个RTL IP核                           16+原语IP核 + 1颗Chiplet
```

**关键原则**:
- 硕士阶段追求"从0到1"——完成哪怕一个原语的硅基实现，就是里程碑
- 博士阶段追求"从1到N"——建立完整的IP核库，并在理论层面做出原创贡献
- 工程与理论不分离——最好的理论来自对硬件行为的深刻理解

---

## 五、四单位分工与本课题关系

| 单位 | 分工 | 本课题可参与 |
|------|------|------------|
| **NDSC** | SDI交换芯片、TCC-Link协议栈 | 交换矩阵微架构、链路层实现 |
| **复旦** | 架构与应用 | 应用场景约束输入 |
| **苏州实验室** | 材料与网络 | 互联工艺参数参考 |
| **天大** | 工程与实现（总集成） | **核心贡献：RTL IP设计、FPGA原型、验证体系** |

---

## 六、入门路径建议

### 6.1 第一学期推荐课程

- 高等数字集成电路设计（可综合RTL、时序分析）
- FPGA设计与验证（Vivado、时序收敛）
- 计算机体系结构（流水线、缓存、NoC）
- 片上互连与网络（SDI交换矩阵的理论基础）

### 6.2 必读文档（优先级排序）

1. [TCC_Knowledge_Base_Baseline_v2.0.md](http://127.0.0.1:8899/home/work/.openclaw/workspace/30_TCC/TCC_Knowledge_Base_Baseline_v2.0.md) — 16原语权威定义 + 范式全景
2. [TCC_iNEST_LiquidTopology_v1.0.md](http://127.0.0.1:8899/home/work/.openclaw/workspace/30_TCC/31_Theory/TCC_iNEST_LiquidTopology_v1.0.md) — Page模板系统 + 液态拓扑机制
3. [TCC计算范式_NDSC与天大细化工程规划_v1.0.md](http://127.0.0.1:8899/home/work/.openclaw/workspace/30_TCC/34_Projects/TCC计算范式_NDSC与天大细化工程规划_v1.0.md) — 工程分工与芯片架构
4. [Gen1-MVP_RTL微架构与IP核详细规格_v1.0.md](http://127.0.0.1:8899/home/work/.openclaw/workspace/50_Output/54_Code/iNEST/Gen1-MVP_RTL微架构与IP核详细规格_v1.0.md) — 可直接参考的RTL设计范例
5. [00_iNEST工程开发总体规划_v1.0.md](http://127.0.0.1:8899/home/work/.openclaw/workspace/50_Output/54_Code/iNEST/00_iNEST工程开发总体规划_v1.0.md) — 涌现验证体系全景

### 6.3 动手建议

1. 用Vivado跑通一个AXI4-Lite从机的Demo（理解总线协议）
2. 用cocotb写一个简单的Crossbar验证用例（建立验证思维）
3. 阅读`sdio_bond_core_v24.v`（NCL异步电路的实际代码）
4. 读完后提出3个你想做的具体课题，与导师讨论选定

---

## 附录：关键文件索引

| 文件 | 用途 |
|------|------|
| [TCC_Knowledge_Base_Baseline_v2.0.md](http://127.0.0.1:8899/home/work/.openclaw/workspace/30_TCC/TCC_Knowledge_Base_Baseline_v2.0.md) | 原语权威定义 |
| [TCC_iNEST_LiquidTopology_v1.0.md](http://127.0.0.1:8899/home/work/.openclaw/workspace/30_TCC/31_Theory/TCC_iNEST_LiquidTopology_v1.0.md) | 液态拓扑方案 |
| [Gen1-MVP_RTL微架构与IP核详细规格_v1.0.md](http://127.0.0.1:8899/home/work/.openclaw/workspace/50_Output/54_Code/iNEST/Gen1-MVP_RTL微架构与IP核详细规格_v1.0.md) | RTL设计范例 |
| [Gen1-MVP_FPGA验证与测试方案_v1.0.md](http://127.0.0.1:8899/home/work/.openclaw/workspace/50_Output/54_Code/iNEST/Gen1-MVP_FPGA验证与测试方案_v1.0.md) | 验证方法学 |
| [SDI化合键工程参数证明及工程实现方案.md](http://127.0.0.1:8899/home/work/.openclaw/workspace/50_Output/54_Code/iNEST/SDI化合键工程参数证明及工程实现方案.md) | 物理参数 (b=10, g=1.5) |
| [00_iNEST工程开发总体规划_v1.0.md](http://127.0.0.1:8899/home/work/.openclaw/workspace/50_Output/54_Code/iNEST/00_iNEST工程开发总体规划_v1.0.md) | 涌现验证体系 |
| [TCC计算范式_NDSC与天大细化工程规划_v1.0.md](http://127.0.0.1:8899/home/work/.openclaw/workspace/30_TCC/34_Projects/TCC计算范式_NDSC与天大细化工程规划_v1.0.md) | 工程分工 |
| [iNEST_TCC_工程边界定义.md](http://127.0.0.1:8899/home/work/.openclaw/workspace/50_Output/54_Code/iNEST/iNEST_TCC_工程边界定义.md) | 分工边界 |