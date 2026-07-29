---
direction: TCC
title: "TCC数字逻辑方向硕博连读研究计划 v1.0"
created: 2026-07-07
modified: 2026-07-07
---
﻿---
title: "TCC数字逻辑方向硕博连读研究计划 — 拓扑中心计算的工程实现与理论创新"
date: 2026-07-07
version: v1.0
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
based_on:
  - TCC_Knowledge_Base_Baseline_v2.0
  - Gen1-MVP_RTL微架构与IP核详细规格_v1.0
  - Gen1-MVP_FPGA验证与测试方案_v1.0
  - SDI化合键工程参数证明及工程实现方案
  - 00_iNEST工程开发总体规划_v1.0
  - TCC计算范式_NDSC与天大细化工程规划_v1.0
  - LNN到iNEST到FPGA_持续推进落地路线图
  - TCC_iNEST_LiquidTopology_v1.0
---

# TCC数字逻辑方向硕博连读研究计划 — 拓扑中心计算的工程实现与理论创新

> **学生画像**: 推免研究生，2026年9月入学，计划硕博连读（硕士2年+博士3年，共5年）
> **研究方向**: TCC（拓扑中心计算）数字逻辑与硬件工程实现
> **总体定位**: 在TCC理论体系指导下，从FPGA原型到ASIC流片，完成TCC核心IP核的RTL设计、验证与芯片实现，并在博士阶段形成"Route-Transform硬件映射理论"方向的原创性学术贡献。

---

## 一、研究背景与定位

### 1.1 TCC范式简介

TCC（Topology-Centric Computing，拓扑中心计算）是邬江兴院士团队提出的新一代计算范式。其核心判断是：**在通信受限计算中，拓扑的运行时选择与切换会直接影响系统性能、能效与可扩展性。**

TCC的技术体系包含：

| 层次 | 内容 | 本课题定位 |
|------|------|-----------|
| **理论层** | Route-Transform分解定理、SDI化合键理论 | 理解与应用 |
| **原语层** | R(6)+T(6)+C(4)=16原语体系 | 硬件实现 |
| **硬件层** | SDI交换矩阵、TCC引擎、TCC-Link协议 | **核心攻关** |
| **系统层** | FPGA原型、Chiplet集成、SDSoW晶上系统 | 参与集成 |
| **应用层** | AI训练/推理、信号处理、多智能体协同 | 验证场景 |

### 1.2 本课题的独特价值

在TCC从理论走向工程落地的关键窗口期（2026-2030），本课题聚焦**数字逻辑硬件实现**这一核心瓶颈——将16原语体系、SDI交换网络、液态拓扑Page模板从纸面定义变为可综合RTL代码、FPGA比特流、最终到ASIC GDSII。

> **一句话定位**: TCC计算范式的"从纸到硅"——做TCC的第一个硅基实现者。

### 1.3 与四单位分工的对齐

| 单位 | 分工 | 本课题贡献 |
|------|------|-----------|
| **NDSC** | SDI交换芯片、协议栈 | 参与交换矩阵微架构、TCC-Link链路层 |
| **复旦** | 架构与应用 | 提供应用场景约束 |
| **苏州实验室** | 材料与网络 | 提供互联工艺参数 |
| **天大** | 工程与实现（总集成） | **核心贡献：RTL IP设计、FPGA原型、验证体系** |

---

## 二、五年总体规划：从单原语RTL到多模态芯片

```
硕士阶段（2026.09-2028.06）              博士阶段（2028.09-2031.06）
═══════════════════════                  ═══════════════════════
Year 1 (2026-2027)     Year 2 (2027-2028)  Year 3-5 (2028-2031)
                                                                   
R.CAST广播引擎 ────────▶ R.FUSE归约引擎 ──▶ 16原语全IP核库
  FPGA验证              Chiplet验证         ASIC流片
                                                   
SDI Crossbar 4x4 ──────▶ Crossbar 16x16 ──▶ 可扩展Crossbar架构
  VU13P单板             VCK190系统           SDSoW晶圆级
                                                   
C.LINK Page Commit ────▶ 多Page液态切换 ──▶ 自组织拓扑演化控制器
  固定模板库             动态Page选择         涌现临界态维持
                                                   
论文1: 广播引擎微架构 ──▶ 论文2: 归约引擎 ──▶ 博士论文: Route-Transform
专利1: 原子拓扑切换    专利2: 网内归约流水线   硬件映射理论与实现
```

### 关键里程碑

| 时间 | 项目里程碑 | 本课题对应任务 |
|------|-----------|---------------|
| 2027.06 | M2 单场景MVP | R.CAST + R.FUSE FPGA原型通过 |
| 2027.12 | M3 双主场景联通 | 16原语全链路RTL完成 |
| 2028.06 | M4 多场景扩展 | Chiplet验证 + 硕士答辩 |
| 2028.12 | M5 综合评估 | 参与三元指标实测 |
| 2029-2031 | 博士自主课题 | ASIC流片 + Route-Transform理论 |

---

## 三、硕士阶段：数字逻辑基础+RTL IP核开发（2026.09-2028.06）

### 3.1 第一学年（2026.09-2027.06）：从入门到首个IP核交付

#### 3.1.1 课程学习（2026秋学期）

| 课程 | 与课题关联 | 优先级 |
|------|-----------|--------|
| 高等数字集成电路设计 | RTL可综合编码、时序分析 | ★★★★★ |
| FPGA设计与验证 | Vivado/Vitis、时序收敛、ILA调试 | ★★★★★ |
| 计算机体系结构 | 流水线、缓存、片上网络NoC | ★★★★ |
| 片上互连与网络 | SDI交换矩阵的理论基础 | ★★★★ |
| 异步电路设计 | NCL/Click元件、握手协议 | ★★★ |
| Verilog/SystemVerilog专题 | UVM验证方法学 | ★★★ |

#### 3.1.2 技能树建设（2026.09-2027.01）

```
工具链掌握路线:
Vivado/Vitis ──▶ cocotb + Verilator ──▶ Modelsim/Questa ──▶ OpenROAD/Yosys
                                                                       
开发板掌握路线:
ALINX AXVU13F ──▶ Xilinx VCK190 (Versal) ──▶ 自定义TCC板卡
                                                                       
协议栈掌握路线:
AXI4-Stream ──▶ AXI4-Lite ──▶ TCC-Link L2/L3 ──▶ TCC-Link L4原语层
```

#### 3.1.3 第一阶段工程任务：R.CAST 广播引擎 RTL设计+FPGA验证（2027.01-2027.03）

**目标**：完成TCC 16原语体系中首个原语（R.CAST广播）的RTL实现与FPGA验证，建立从原语定义到硬件实现的完整方法学。

**任务分解**:

| 编号 | 任务 | 输入 | 输出 | 工作量 |
|------|------|------|------|--------|
| T1.1 | R.CAST微架构设计 | 原语语义定义、目标时序 | 微架构设计文档+框图 | 2周 |
| T1.2 | 广播引擎RTL编码 | 微架构文档 | `r_cast_engine.v` (~500行) | 3周 |
| T1.3 | AXI4-Stream接口适配 | TCC-Link帧格式定义 | `tcclink_tx_adapter.v` / `tcclink_rx_adapter.v` | 2周 |
| T1.4 | 单元测试 (cocotb) | RTL代码 | 10+测试用例，覆盖率>95% | 2周 |
| T1.5 | VU13P综合+布局布线 | 约束文件 | 时序收敛报告、资源报告 | 1周 |
| T1.6 | 板级验证 | FPGA比特流 | 功能正确+性能达标确认 | 2周 |
| T1.7 | 设计文档+代码入库 | 全部验证通过 | IP核数据包（RTL+TB+Doc） | 1周 |

**设计规格**:

```verilog
// R.CAST广播引擎顶层接口
module r_cast_engine #(
    parameter DATA_WIDTH = 512,        // 数据位宽（TCC-Link帧）
    parameter MAX_RECIPIENTS = 16,     // 最大广播目标数
    parameter CREDIT_WIDTH = 8         // 流控信用位宽
) (
    // 源端口（单播输入）
    input  wire [DATA_WIDTH-1:0] src_data,
    input  wire                  src_valid,
    output wire                  src_ready,
    
    // 目标端口（广播输出，每端口独立流控）
    output wire [MAX_RECIPIENTS-1:0][DATA_WIDTH-1:0] dst_data,
    output wire [MAX_RECIPIENTS-1:0]                 dst_valid,
    input  wire [MAX_RECIPIENTS-1:0]                 dst_ready,
    
    // 控制接口
    input  wire [MAX_RECIPIENTS-1:0] recipient_mask,  // 广播目标位掩码
    input  wire                      cast_start,      // 广播触发脉冲
    output wire                      cast_done,       // 广播完成
    
    // 统计接口
    output wire [31:0] bytes_sent,
    output wire [15:0] cast_count,
    
    input  wire clk,    // 200MHz
    input  wire rst_n
);
```

**创新点**:
1. **信用制多目标流控**: 基于Credit-based流控，避免慢速目标阻塞快速目标
2. **原子广播语义**: cast_start单脉冲触发，保证所有目标在≤5ns窗口内接收同一数据
3. **硬件统计**: 内嵌字节计数和广播计数，可直接供CST估值器读取

#### 3.1.4 第二阶段工程任务：SDI Crossbar 4×4交换矩阵（2027.03-2027.05）

**目标**：实现SDI交换矩阵的4×4 Crossbar核心，支持μs级拓扑切换，使用双缓冲设计保证切换期间数据不丢包。

**任务分解**:

| 编号 | 任务 | 输入 | 输出 | 工作量 |
|------|------|------|------|--------|
| T2.1 | Crossbar微架构细化 | Gen1-MVP规格 | 详细设计文档 | 1周 |
| T2.2 | 双缓冲拓扑存储 | BRAM双缓冲方案 | `topo_buffer.v` | 1周 |
| T2.3 | 4×4交换核心RTL | Crossbar算法 | `crossbar_core_4x4.v` | 2周 |
| T2.4 | AXI4-Lite配置接口 | 寄存器映射表 | 配置寄存器组RTL | 1周 |
| T2.5 | 拓扑切换原子操作 | C.LINK Commit语义 | 原子切换控制器 | 1周 |
| T2.6 | 集成测试（4 PE直连） | PE模拟器 | INT-01通过 | 2周 |
| T2.7 | 切换延迟精确测量 | 高速示波器/ILA | 延迟<10μs确认 | 1周 |
| T2.8 | 文档+IP核打包 | 全部验证通过 | `sdio_crossbar_4x4` IP数据包 | 1周 |

**关键时序约束**:

| 路径 | 起点 | 终点 | 延迟目标 | 说明 |
|------|------|------|----------|------|
| 脉冲路由路径 | `spike_in` | `spike_out` | <5 ns | Crossbar直通 |
| 配置写入路径 | `s_axi_wdata` | 寄存器 | <2 cycles | AXI4-Lite单拍 |
| 拓扑切换路径 | C.LINK触发 | 新拓扑生效 | <10 μs (MVP) | 双缓冲指针交换 |
| 流控路径 | 下游反压 | 上游暂停 | <3 cycles | 信用计数更新 |

#### 3.1.5 第三阶段：C.LINK Page Commit机制实现（2027.05-2027.06）

**目标**：实现拓扑Page模板的原子提交机制——这是TCC液态拓扑的核心工程创新。

**核心设计**:

```verilog
// C.LINK Page Commit控制器
module clink_page_commit #(
    parameter NUM_PAGES = 10,          // 预编译Page数量
    parameter NUM_BONDS = 16,          // 化合键数量
    parameter PAGE_BITS = 2048         // 每Page配置位宽
) (
    // 双缓冲Page存储
    input  wire [NUM_PAGES-1:0][PAGE_BITS-1:0] page_buffer_active,
    input  wire [NUM_PAGES-1:0][PAGE_BITS-1:0] page_buffer_shadow,
    
    // Commit接口
    input  wire [3:0]  target_page_id,    // 目标Page ID
    input  wire        commit_req,        // Commit请求
    output wire        commit_ack,        // Commit完成确认
    
    // 切换状态输出
    output wire        switch_in_progress,
    output wire [3:0]  current_page_id,
    output wire [31:0] switch_latency_cycles,  // 切换延迟（周期数）
    
    // 与Crossbar的接口
    output wire [PAGE_BITS-1:0] crossbar_config,
    output wire                  config_load,
    input  wire                  config_done,
    
    input  wire clk,
    input  wire rst_n
);
```

**创新点**:
1. **双缓冲+指针交换**: 影子缓冲区预加载新Page，Commit瞬间指针交换，实现<100ns切换
2. **原子性保证**: Commit期间Crossbar锁定，保证切换前后状态一致
3. **切换延迟测量**: 内嵌硬件计时器，精确测量每次切换延迟

---

### 3.2 第二学年（2027.07-2028.06）：多原语集成+首个系统级Demo

#### 3.2.1 R.FUSE 归约引擎RTL设计（2027.07-2027.09）

**目标**：实现蝶形归约（Butterfly AllReduce）的硬件引擎，支持FP16/FP32混合精度。

**设计规格**:

```verilog
module r_fuse_engine #(
    parameter DATA_WIDTH = 512,   // 512b = 32×FP16 / 16×FP32
    parameter NUM_PORTS = 4,      // 4端口（对应4 PE）
    parameter REDUCE_STAGES = 2   // log2(4)=2级归约
) (
    // 数据端口（每端口双向）
    input  wire [NUM_PORTS-1:0][DATA_WIDTH-1:0] port_data_in,
    output wire [NUM_PORTS-1:0][DATA_WIDTH-1:0] port_data_out,
    input  wire [NUM_PORTS-1:0]                 port_valid,
    output wire [NUM_PORTS-1:0]                 port_ready,
    
    // 归约配置
    input  wire [1:0] reduce_op,    // 00=SUM, 01=MAX, 10=MIN, 11=AVG
    input  wire [1:0] data_type,    // 00=FP16, 01=FP32, 10=INT16, 11=INT32
    input  wire       reduce_start,
    output wire       reduce_done,
    
    // 统计接口
    output wire [31:0] bytes_reduced,
    output wire [15:0] reduce_count,
    
    input  wire clk,
    input  wire rst_n
);
```

**归约流水线**:

```
Stage 1 (第一级归约)            Stage 2 (第二级归约)
═══════════════════            ═══════════════════
PE0 ─┬─┐                       PE0 + PE1 ─┬─┐
PE1 ─┘ ├─ SUM1 ─► PE0          PE2 + PE3 ─┘ ├─ SUM2 ─► 广播回所有PE
PE2 ─┬─┤                       (已完成归约)   │
PE3 ─┘ ├─ SUM1 ─► PE2                       └─► PE0,1,2,3 得到相同结果
```

**创新点**:
1. **可配置运算单元**: 同一硬件支持SUM/MAX/MIN/AVG四种归约操作
2. **流水线连续归约**: 不等待上一个归约完成即可启动下一个，吞吐率最大化
3. **混合精度**: FP16/FP32/INT16/INT32自适应数据路径宽度

#### 3.2.2 多原语集成系统（2027.09-2027.12）

**目标**：将R.CAST、R.FUSE、SDI Crossbar、C.LINK集成在VU13P单板上，实现M3里程碑"双主场景联通"。

**系统架构**:

```
┌──────────────────────────────────────────────────────────┐
│                  TCC_Gen1_System                          │
│                  (VU13P FPGA)                             │
│                                                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │ MacroTile │  │ MacroTile │  │ MacroTile │  │ MacroTile │ │
│  │    #0     │  │    #1     │  │    #2     │  │    #3     │ │
│  │           │  │           │  │           │  │           │ │
│  │ R.CAST ◄──┼──┼──R.FUSE──┼──┼──T.GEMM──┼──┼──R.SWAP──┼─│
│  │           │  │           │  │           │  │           │ │
│  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘ │
│        │              │              │              │       │
│        └──────────────┼──────────────┼──────────────┘       │
│                       │  SDI Crossbar 4×4                   │
│                  ┌────┴────┐                                │
│                  │ C.LINK  │                                │
│                  │ Commit  │                                │
│                  └─────────┘                                │
│                                                           │
│  外设接口:                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐               │
│  │ DDR4     │  │ QSFP28   │  │ UART     │               │
│  │ Ctrl     │  │ 100GbE   │  │ Debug    │               │
│  └──────────┘  └──────────┘  └──────────┘               │
└──────────────────────────────────────────────────────────┘
```

**验证场景**:

| 场景 | Page ID | 原语链 | 验证指标 |
|------|---------|--------|---------|
| AI梯度同步 | P01 Butterfly | R.CAST→T.GEMM→R.FUSE | AllReduce延迟<5μs@4节点 |
| 信号FFT | P06 Hypercube | R.SWAP→T.SCAN→R.PIPE | 4K点FFT延迟<10μs |
| 拓扑液态切换 | P01↔P06 | C.LINK Commit | 切换延迟<10μs |

#### 3.2.3 硕士论文撰写与答辩（2028.01-2028.06）

**论文方向**: "拓扑中心计算的数字逻辑实现——R.CAST广播引擎与SDI Crossbar的微架构设计与FPGA验证"

**论文结构**:

| 章节 | 内容 | 字数 |
|------|------|------|
| 第1章 | 引言：TCC计算范式与硬件实现挑战 | 5000 |
| 第2章 | 背景：SDI交换网络、16原语体系、液态拓扑 | 8000 |
| 第3章 | R.CAST广播引擎：微架构设计与实现 | 10000 |
| 第4章 | SDI Crossbar 4×4：拓扑可编程交换矩阵 | 10000 |
| 第5章 | C.LINK Page Commit：原子拓扑切换机制 | 8000 |
| 第6章 | 系统集成与FPGA验证 | 8000 |
| 第7章 | 性能评估与对比分析 | 6000 |
| 第8章 | 总结与展望 | 3000 |

---

## 四、博士阶段：从IP核库到芯片实现+理论创新（2028.09-2031.06）

### 4.1 第三学年（2028.09-2029.06）：16原语全IP核库+ASIC前端

#### 4.1.1 T/T类原语引擎RTL实现（2028.09-2028.12）

在硕士阶段R类（通信原语）积累基础上，完成T类（变换计算原语）和各类C原语的RTL实现：

| 原语 | 模块名 | 核心挑战 | 创新方向 | 工作量 |
|------|--------|---------|---------|--------|
| T.GEMM | `t_gemm_systolic.v` | 脉动阵列+数据重用 | 拓扑自适应脉动（Butterfly→Mesh切换） | 6周 |
| T.FOLD | `t_fold_reduce.v` | 流水线归约树 | 与R.FUSE的硬件共享 | 3周 |
| T.MAPS | `t_maps_elementwise.v` | SIMD向量化 | 动态精度切换（FP16↔FP32） | 3周 |
| T.SCAN | `t_scan_prefix.v` | 前缀扫描流水线 | 与FFT蝶形扫描的硬件复用 | 4周 |
| T.LOOK | `t_look_lut.v` | 高速BRAM查表 | 共享权重LUT | 2周 |
| T.SPEC | `t_spec_cordic.v` | CORDIC/超越函数 | 迭代次数自适应 | 4周 |
| R.PULL | `r_pull_gather.v` | AllGather流水线 | 与广播引擎共享硬件 | 3周 |
| R.SWAP | `r_swap_alltoall.v` | 全连接Crossbar | 非阻塞交换 | 4周 |
| R.PIPE | `r_pipe_scatter.v` | ReduceScatter分段 | 流水线仲裁 | 3周 |
| R.MESH | `r_mesh_neighbor.v` | 邻域窗口滑动 | 可配置邻域形状 | 3周 |
| C.TICK | `c_tick_clock.v` | 分布式逻辑时钟 | 硬件Lamport时钟 | 2周 |
| C.SYNC | `c_sync_barrier.v` | Epoch边界同步 | 零延迟Barrier | 2周 |
| C.MOVE | `c_move_dma.v` | 硬件DMA控制器 | 拓扑感知DMA | 3周 |

**关键创新方向**:
1. **硬件共享设计**: R.FUSE的归约树→T.FOLD复用；R.CAST的扇出→R.PULL复用
2. **拓扑自适应**: T.GEMM脉动阵列根据当前拓扑（Ring/Butterfly/Mesh）自动切换数据流
3. **精度可配置**: 所有T类原语支持FP16/FP32/INT8动态切换

#### 4.1.2 IP核库规范化（2029.01-2029.03）

建立统一的TCC IP核交付标准：

```
tcc_ip_library/
├── r_cast_engine/          # R.CAST广播引擎
│   ├── rtl/                #  可综合RTL (SystemVerilog)
│   ├── tb/                 #  测试平台 (cocotb + UVM)
│   ├── constraints/        #  时序约束 (.xdc)
│   ├── docs/               #  数据手册 + 集成指南
│   └── ip_release/         #  封装IP核 (.xci / .xcix)
├── r_fuse_engine/          # R.FUSE归约引擎
├── sdi_crossbar/           # SDI Crossbar
├── clink_commit/           # C.LINK Page Commit
├── ...（16个原语 + 5个基础设施IP）
└── tcc_ip_catalog.json     # IP目录元数据
```

#### 4.1.3 Chiplet流片准备（2029.04-2029.06）

**目标**：完成TCC首个Chiplet（TCC-1 Chiplet）的前端设计，提交至MPW流片。

**TCC-1 Chiplet规格**:

| 参数 | 目标值 | 说明 |
|------|--------|------|
| 工艺 | 12nm/28nm | 国产工艺优先 |
| 面积 | 4mm×4mm | Chiplet尺寸 |
| 集成模块 | 4×R/T原语引擎 + Crossbar 8×8 + C.LINK | 精简TCC核心 |
| 接口 | UCIe x4 + HBM x1 | Chiplet互联 + 高带宽内存 |
| 时钟 | 500MHz (Core) / 200MHz (I/O) | 核心/IO双时钟域 |
| 功耗 | <5W | Chiplet级 |
| 交付物 | GDSII + 测试向量 + 文档 | MPW提交包 |

---

### 4.2 第四学年（2029.09-2030.06）：流片回片+系统级验证+理论突破

#### 4.2.1 TCC-1 Chiplet回片测试（2029.09-2029.12）

| 测试阶段 | 内容 | 工具 | 通过标准 |
|---------|------|------|---------|
| 直流测试 | VDD/GND、IO电平、功耗 | 万用表/示波器 | 与仿真偏差<10% |
| 功能测试 | 16原语逐一功能验证 | FPGA+Chiplet联合平台 | 所有原语通过单元测试 |
| 性能测试 | 延迟/吞吐/功耗测量 | 高速逻辑分析仪 | 达到设计指标的90%+ |
| 压力测试 | 72小时连续运行 | 随机原语序列 | 无死锁/数据错误 |
| 拓扑切换测试 | 100万次Page Commit | 自动循环测试 | 切换成功率>99.999% |

#### 4.2.2 系统级验证平台（2030.01-2030.03）

**TCC验证板卡**:

```
┌───────────────────────────────────────────────────────────┐
│                   TCC Verification Board                   │
│                                                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │ TCC-1 Chiplet│  │ TCC-1 Chiplet│  │ TCC-1 Chiplet│    │
│  │    (Die 0)   │  │    (Die 1)   │  │    (Die 2)   │    │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘    │
│         │                 │                 │             │
│         └─────────────────┼─────────────────┘             │
│                           │ UCIe Interposer               │
│                    ┌──────┴──────┐                        │
│                    │ TCC-Link v1 │                        │
│                    │ Controller  │                        │
│                    └──────┬──────┘                        │
│                           │                               │
│              ┌────────────┼────────────┐                 │
│         ┌────┴────┐  ┌────┴────┐  ┌────┴────┐           │
│         │ HBM2e   │  │ QSFP-DD │  │ PCIe    │           │
│         │ 8GB     │  │ 400GbE  │  │ Gen5x16 │           │
│         └─────────┘  └─────────┘  └─────────┘           │
└───────────────────────────────────────────────────────────┘
```

#### 4.2.3 理论突破：Route-Transform硬件映射理论（2030.04-2030.09）

**这是博士论文的核心理论贡献。**

**核心问题**：Route原语（通信）与Transform原语（计算）在硬件层面是否存在统一实现框架？

**理论框架（三定理）**:

> **定理1（R-T硬件同构定理）**：在SDI交换网络中，任意R类原语与T类原语可在统一的"流水化归约树+可配置交叉开关"微架构上实现，硬件面积开销为 O(N·log₂N)，N为节点数。

> **定理2（拓扑-精度对偶定理）**：在线性流水线硬件约束下，R-T混合原语链的端到端精度误差 ε 与拓扑切换频率 f_switch 满足: ε(f_switch) ≤ ε₀ + k/√f_switch，其中k为硬件噪声系数。

> **定理3（最优Page切换策略）**：给定任务序列 T₁→T₂→…→T_m 和预编译Page集合 {P₁,…,P_k}，存在多项式时间算法找到最优Page切换序列，使总切换开销最小化。该问题是Page迁移开销图的加权最短路径问题，可在 O(m·k²) 时间内求解。

**数学工具**:
- 信息论（互信息/熵率分析）
- 排队论（crossbar吞吐率建模）
- 图论（Page依赖图、最短路径）

---

### 4.3 第五学年（2030.09-2031.06）：博士论文+SDSoW扩展研究

#### 4.3.1 博士论文撰写（2030.09-2031.03）

**论文题目**: "Route-Transform硬件映射理论：拓扑中心计算的数字逻辑实现与验证"

**章节规划**:

| 章节 | 内容 | 创新等级 |
|------|------|---------|
| 第1章 | 引言：TCC范式背景与硬件实现的科学问题 | — |
| 第2章 | 理论基础：Route-Transform分解与SDI交换模型 | — |
| 第3章 | **R-T硬件同构定理**：统一微架构设计与证明 | ★★★ 原创 |
| 第4章 | **拓扑-精度对偶定理**：切换频率与计算精度关系 | ★★★ 原创 |
| 第5章 | **最优Page切换策略**：多项式时间调度算法 | ★★★ 原创 |
| 第6章 | 16原语IP核库：RTL实现与FPGA/Chiplet验证 | ★★ 工程创新 |
| 第7章 | TCC-1 Chiplet：流片、测试与性能评估 | ★★ 工程创新 |
| 第8章 | SDSoW扩展：晶圆级TCC系统的设计空间探索 | ★ 前瞻研究 |
| 第9章 | 总结与未来方向 | — |

#### 4.3.2 毕业目标

| 类别 | 数量 | 说明 |
|------|:---:|------|
| 期刊论文 | 2-3篇 | 1篇TC/TCAD/IEEE Micro, 1-2篇DAC/DATE/ISCAS |
| 发明专利 | 3-5项 | 广播引擎、归约流水线、原子拓扑切换、动态精度调度 |
| IP核 | 16+5个 | 16原语+5基础设施IP，全部通过FPGA/ASIC验证 |
| 芯片 | 1颗 | TCC-1 Chiplet MPW流片+回片测试 |
| 软件 | 2个 | cocotb验证框架 + TCC-IP自动生成器 |

---

## 五、年度详细规划与时间表

### 5.1 硕士阶段（2026.09-2028.06）

```
2026 ────────────────────────────────────────────────────────
09月 入学，选课：高等数字IC/FPGA/体系结构/片上网络
10月  工具链上手：Vivado, cocotb, Verilator, ModelSim
11月  开发板熟悉：AXVU13F GPIO/UART/DDR4基础实验
12月  选题开题：R.CAST广播引擎微架构设计方案
2027 ────────────────────────────────────────────────────────
01月  ██ R.CAST RTL编码 (T1.2-T1.3)
02月  ██ 单元测试+时序收敛 (T1.4-T1.5)
03月  ██ FPGA板级验证 (T1.6) ← M2-α里程碑：首个原语通过
04月  SDI Crossbar微架构细化 (T2.1-T2.3)
05月  Crossbar集成测试 (T2.4-T2.6)
06月  C.LINK Page Commit + 硕士开题报告 ← M2里程碑对齐
07月  ██ R.FUSE归约引擎RTL (3.2.1)
08月  R.FUSE验证+集成到Crossbar系统
09月  多原语集成：R.CAST+R.FUSE+T.GEMM
10月  全系统联合调试
11月  ██ 双场景验证：AI梯度同步+FFT信号处理
12月  硕士中期检查 + 专利1/2撰写 ← M3里程碑对齐
2028 ────────────────────────────────────────────────────────
01月  ██ 硕士论文撰写（第1-5章）
02月  ██ 硕士论文撰写（第6-8章）
03月  论文修改+预答辩
04月  Chiplet流片准备（前端综合、DFT）← M4对齐
05月  正式答辩
06月  毕业离校，暑假准备博士入学
```

### 5.2 博士阶段（2028.09-2031.06）

```
2028 ────────────────────────────────────────────────────────
09月  博士入学，T类原语引擎启动设计
10月  T.GEMM脉动阵列 (4.1.1)
11月  T.SCAN+T.FOLD (4.1.1)
12月  T.MAPS+T.LOOK+T.SPEC (4.1.1) ← 16原语RTL全部完成
2029 ────────────────────────────────────────────────────────
01月  C类原语+IP核库规范化 (4.1.2)
02月  IP核自动化生成框架
03月  TCC-1 Chiplet前端设计 (RTL综合) (4.1.3)
04月  TCC-1 Chiplet后端（布局布线、时序收敛）
05月  TCC-1 Chiplet签核（DRC/LVS/STA）
06月  ██ MPW流片提交 ← 博士阶段第一个里程碑
07月  暑假：Chiplet测试板PCB设计
08月  等待流片回片，准备理论框架
09月  ██ Chiplet回片+直流测试 (4.2.1)
10月  功能测试+性能测试 (4.2.1)
11月  压力测试+拓扑切换可靠性测试 (4.2.1)
12月  测试报告+数据分析
2030 ────────────────────────────────────────────────────────
01月  系统级验证平台搭建 (4.2.2)
02月  TCC验证板卡调试
03月  全系统Benchmark测试
04月  ██ 理论突破期：R-T硬件同构定理形式化证明 (4.2.3)
05月  拓扑-精度对偶定理证明 (4.2.3)
06月  最优Page切换策略算法设计+复杂度分析 (4.2.3)
07月  理论三定理的仿真验证
08月  SDSoW扩展：晶圆级TCC设计空间探索 (4.3)
09月  ██ 博士论文大纲+第1-3章初稿 (4.3.1)
10月  第4-5章（理论贡献）初稿
11月  第6-7章（工程贡献）初稿
12月  第8-9章（前瞻+总结）+ 全文初稿完成
2031 ────────────────────────────────────────────────────────
01月  博士论文修改（第一轮）
02月  博士论文修改（第二轮）
03月  最终修改+预答辩
04月  期刊论文投稿（TC/TCAD）
05月  正式答辩
06月  毕业
```

---

## 六、核心技术攻关清单（按优先级排序）

### P0：必须攻克（硕士阶段完成）

| 编号 | 技术点 | 难度 | 创新度 | 依赖 | 时间 |
|------|--------|:--:|:---:|------|------|
| K1 | R.CAST硬件广播引擎（信用制多目标流控） | ★★★ | ★★★★ | 原语语义 | 2027Q1 |
| K2 | SDI Crossbar双缓冲拓扑切换 | ★★★★ | ★★★★★ | 无 | 2027Q2 |
| K3 | C.LINK原子Page Commit | ★★★★ | ★★★★★ | K2 | 2027Q2 |
| K4 | R.FUSE蝶形归约流水线 | ★★★★ | ★★★★ | K2 | 2027Q3 |

### P1：博士阶段重点攻关

| 编号 | 技术点 | 难度 | 创新度 | 依赖 | 时间 |
|------|--------|:--:|:---:|------|------|
| K5 | T.GEMM拓扑自适应脉动阵列 | ★★★★★ | ★★★★★ | K2 | 2028Q4 |
| K6 | 16原语硬件共享架构设计 | ★★★★★ | ★★★★★ | K1-K5 | 2029Q1 |
| K7 | Chiplet级物理设计（12nm/28nm） | ★★★★★ | ★★★ | K6 | 2029Q2 |
| K8 | R-T硬件同构定理形式化证明 | ★★★★★ | ★★★★★ | K6 | 2030Q2 |
| K9 | 最优Page切换调度算法 | ★★★★ | ★★★★★ | K3 | 2030Q3 |
| K10 | SDSoW晶圆级扩展架构 | ★★★★★ | ★★★★ | K7 | 2030Q4 |

---

## 七、推荐工具链与学习资源

### 7.1 工具链清单

| 工具 | 用途 | 学习资源 | 优先级 |
|------|------|---------|--------|
| Vivado/Vitis | FPGA综合/布局布线/调试 | Xilinx官方教程 | ★★★★★ |
| cocotb | Python驱动的RTL验证 | cocotb官方文档 | ★★★★★ |
| Verilator | 开源Verilog仿真器 | Verilator Wiki | ★★★★ |
| ModelSim/Questa | 专业仿真器 | 天大EDA实验室 | ★★★ |
| Yosys/OpenROAD | 开源ASIC流程 | OpenROAD教程 | ★★★ |
| GTKWave | 波形查看 | 自带文档 | ★★★ |
| Synopsys DC | ASIC综合 | 天大EDA实验室 | ★★★ |
| Cadence Innovus | 布局布线 | 天大EDA实验室 | ★★★ |
| Python (numpy/scipy) | 算法原型/数据分析 | 本科已有基础 | ★★★ |
| Git/GitHub | 版本控制 | GitHub Guides | ★★★★ |

### 7.2 推荐教材与论文

**教材**:
- Weste & Harris, *CMOS VLSI Design* (第4版) — 数字IC设计圣经
- Hennessy & Patterson, *Computer Architecture: A Quantitative Approach* (第6版) — 体系结构
- Dally & Towles, *Principles and Practices of Interconnection Networks* — 互连网络经典
- Palnitkar, *Verilog HDL* — Verilog入门
- Spear & Tumbush, *SystemVerilog for Verification* (第3版) — UVM验证

**TCC相关论文（团队产出）**:
- [CST_Intelligence_Emergence_Paper_V25_FINAL.md](http://127.0.0.1:8899/vault/50_Output/51_Papers/_from_tcc_theory/CST_Intelligence_Emergence_Paper_V25_FINAL.md)
- [TCC超非线性增益_研究进展与数学证明路线图_v1.0.md](http://127.0.0.1:8899/vault/30_TCC/31_Theory/TCC超非线性增益_研究进展与数学证明路线图_v1.0.md)
- [从加性增益到乘性增益_1+1大于2的非线性证明_文献与证据链_v1.0.md](http://127.0.0.1:8899/vault/30_TCC/31_Theory/从加性增益到乘性增益_1+1大于2的非线性证明_文献与证据链_v1.0.md)

**外部关键论文**:
- Jouppi et al., "TPU v4: An Optically Reconfigurable Supercomputer for ML" (ISCA 2023) — 可重构互连参考
- Norrie et al., "Google's Training Chips Revealed: TPUv4i" — 训练芯片架构
- Choquette et al., "NVIDIA Hopper H100 GPU" (IEEE Micro 2023) — GPU互连参考

---

## 八、预期产出与成果清单

### 8.1 学术论文（5年）

| 序号 | 拟投稿期刊/会议 | 论文方向 | 时间 | 学生贡献 |
|------|--------------|---------|------|---------|
| P1 | DAC/DATE 2028 | "R.CAST: A Credit-Based Hardware Broadcast Engine for Topology-Centric Computing" | 2027.10 | 第一作者 |
| P2 | ISCAS 2028 | "Atomic Page Commit: Nanosecond-Scale Network Topology Switching via Double-Buffered Crossbars" | 2028.01 | 第一作者 |
| P3 | TC/TCAD 2030 | "Route-Transform Hardware Isomorphism: A Unified Microarchitecture for Topology-Centric Primitives" | 2030.04 | 第一作者 |
| P4 | ISCA/MICRO 2030 | "TCC-1: A Topology-Centric Chiplet with Reconfigurable Network-on-Chip for AI and Signal Processing" | 2030.06 | 第一作者 |
| P5 | DAC 2031 | "Optimal Page Migration Scheduling for Liquid-Topology Computing" | 2031.01 | 第一作者 |

### 8.2 发明专利（5年）

| 序号 | 专利名称 | 创新点 | 时间 |
|------|---------|--------|------|
| Z1 | 一种基于信用制的多目标硬件广播引擎及其流控方法 | K1 | 2027.06 |
| Z2 | 一种双缓冲原子拓扑切换的SDI交换矩阵及其配置方法 | K2+K3 | 2027.12 |
| Z3 | 一种拓扑自适应的脉动阵列矩阵乘加加速器 | K5 | 2028.12 |
| Z4 | 一种动态精度可配置的Route-Transform混合运算单元 | K6 | 2029.06 |
| Z5 | 一种基于Page迁移图的拓扑切换调度方法及装置 | K9 | 2030.06 |

### 8.3 IP核与软件

| 编号 | 名称 | 类型 | 规模 | 时间 |
|------|------|------|:---:|------|
| IP-01 | `r_cast_engine` | RTL IP | ~800行 | 2027.03 |
| IP-02 | `sdi_crossbar_4x4` | RTL IP | ~1200行 | 2027.05 |
| IP-03 | `clink_page_commit` | RTL IP | ~600行 | 2027.06 |
| IP-04 | `r_fuse_engine` | RTL IP | ~900行 | 2027.09 |
| IP-05 | `t_gemm_systolic` | RTL IP | ~1500行 | 2028.11 |
| IP-06-20 | 其余12原语+3C | RTL IP | ~8000行 | 2029.03 |
| SW-01 | `tcc_cocotb_framework` | 验证框架 | Python | 2027.06 |
| SW-02 | `tcc_ip_generator` | 代码生成器 | Python | 2029.02 |

### 8.4 芯片

| 编号 | 名称 | 工艺 | 面积 | 时间 |
|------|------|------|:---:|------|
| ASIC-01 | TCC-1 Chiplet | 28nm (MPW) | 4×4mm² | 2029.06 |

---

## 九、博士论文核心创新点的数学基础

### 9.1 R-T硬件同构定理的数学表述

设SDI交换网络为有向图 G=(V, E)，其中 |V|=N，|E|=M。

对于任意 R 类原语 R_i（通信模式）和 T 类原语 T_j（计算模式），定义其硬件实现为：

**定义1（R-T硬件映射）**: 映射 Φ: {R_i} ∪ {T_j} → ℋ 将每个原语映射到一个硬件子模块 ℎ ∈ ℋ。ℋ 为"流水化归约树 + 可配置交叉开关"的微架构空间。

**定理1（同构性）**: ∀ R_i, T_j，∃ 统一硬件配置向量 c ∈ {0,1}^k 使得:
- Φ(R_i) 和 Φ(T_j) 共享相同的功能单元（ALU/MUL/CMP）
- 仅需改变 c 中 ≤ log₂k 比特即可在 R_i 和 T_j 的硬件实现间切换
- 面积上界: Area(Φ(any)) = O(N·log₂N) 逻辑门

**证明思路**: 采用"数据流图同构"方法。证明 R.FUSE（归约树）和 T.FOLD（向量归约）具有相同的归约树数据流图，仅叶子节点操作不同；R.CAST（广播树）和 R.PULL（收集树）是互逆操作，可共享扇出网络。

### 9.2 拓扑-精度对偶定理的数学表述

**定义2（原语链精度）**: 对于原语链 C = p₁→p₂→…→pₗ，其中 pₖ ∈ {R} ∪ {T}，定义端到端精度误差 ε(C) = ‖ŷ − y‖₂，ŷ 为硬件计算结果，y 为无限精度结果。

**定理2（对偶关系）**: 若原语链在硬件流水线上执行，拓扑切换频率 f_switch，则:
```
ε(C; f_switch) ≤ ε₀ + k_hw / √f_switch
```
其中 ε₀ 为静态拓扑下的基线误差，k_hw 为硬件噪声系数（与工艺、电压、温度相关）。

**直观解释**: 切换越频繁，每次切换引入的量化/舍入/流水线气泡累积越多，但边际效应递减（1/√f关系）。

### 9.3 最优Page切换策略

**定义3（Page迁移图）**: 有向图 G_page = (V_page, E_page)，其中:
- V_page = {P₁, ..., P_k} 为预编译Page集合
- 边权重 w(P_a→P_b) = C.LINK切换延迟(P_a→P_b)

**定理3（最优切换）**: 给定任务序列 T₁→T₂→…→T_m 和对应的最优Page映射 τ: T_i → P_{τ(i)}，总切换开销最小化问题等价于在 G_page 上求加权最短路径，复杂度 O(m·k²)。

**动态规划算法**:
```python
def optimal_page_sequence(tasks, pages, switch_cost):
    """
    tasks[i]: 第i个任务的特征向量
    pages[j]: 第j个Page模板的特征向量
    switch_cost[a][b]: 从Page a切换到Page b的延迟(ns)
    返回: 最优Page序列和总切换开销
    """
    m, k = len(tasks), len(pages)
    dp = [[float('inf')] * k for _ in range(m)]  # dp[i][j] = 前i个任务,以Page j结尾的最优cost
    backtrack = [[-1] * k for _ in range(m)]
    
    # 初始化: 第一个任务
    for j in range(k):
        dp[0][j] = dist(tasks[0], pages[j])  # 匹配损失
    
    # 动态规划
    for i in range(1, m):
        for j in range(k):
            match_loss = dist(tasks[i], pages[j])
            for prev_j in range(k):
                candidate = dp[i-1][prev_j] + switch_cost[prev_j][j] + match_loss
                if candidate < dp[i][j]:
                    dp[i][j] = candidate
                    backtrack[i][j] = prev_j
    
    # 回溯最优路径
    best_final = min(range(k), key=lambda j: dp[-1][j])
    path = [best_final]
    for i in range(m-1, 0, -1):
        path.append(backtrack[i][path[-1]])
    return path[::-1], dp[-1][best_final]
```

---

## 十、风险识别与应对

| 风险 | 概率 | 影响 | 应对措施 |
|------|:---:|------|---------|
| FPGA资源不足（VU13P vs VCK190） | 中 | 高 | 预留30%余量；优先VCK190新板 |
| 流片失败（MPW良率） | 中 | 高 | FPGA原型先行；预留第二次流片经费 |
| 时序收敛困难（28nm@500MHz） | 高 | 中 | 备选200MHz降频方案；关键路径手工优化 |
| 理论证明难度超预期 | 中 | 中 | 先做数值验证；与数学系合作 |
| 团队人力不足 | 低 | 中 | 带本科生毕设协助；利用自动化脚本 |
| EDA工具License限制 | 中 | 中 | 优先开源工具(Yosys/OpenROAD)；天大实验室共享 |

---

## 十一、导师与团队支持

| 角色 | 人员 | 支持内容 |
|------|------|---------|
| 学术导师 | 天大TCC团队教授 | 体系结构理论指导、论文方向把关 |
| 工程导师 | NDSC/TCC工程团队 | RTL设计评审、FPGA调试指导、Chiplet流程 |
| 理论协作 | CST理论团队 | Route-Transform定理的数学证明支持 |
| 工具链支持 | 天大EDA实验室 | Synopsys/Cadence License, 高速测试设备 |
| 芯片流片 | 天大+NDSC联合 | MPW流片经费+工艺对接 |

---

## 十二、总结：五年后的你

到2031年博士毕业时，你将拥有：

1. **完整的芯片设计全栈能力**：从RTL编码→FPGA原型→ASIC流片的完整工程经验
2. **独创的理论贡献**：Route-Transform硬件映射三定理，成为TCC工程方法论的理论基石
3. **可交付的IP核库**：16原语+5基础设施IP，可直接用于TCC后续芯片开发
4. **一颗流片验证的Chiplet**：TCC-1，可能是世界上第一个TCC范式芯片
5. **2-3篇顶会/顶刊论文 + 3-5项发明专利**：具备独立科研能力的完整证明
6. **在TCC生态中的核心位置**：从"第一个硅基实现者"成长为TCC硬件架构的核心设计师

> 从单原语RTL到多模态芯片，从FPGA原型到ASIC流片，从工程实现到理论创新。这条路已经铺好——需要的只是你的决心与执行力。

---

## 附录A：TCC 16原语-RTL实现状态跟踪表

| 原语 | 语义 | 模块名 | 状态 | 完成时间 | 验证等级 | 负责人 |
|------|------|--------|------|---------|---------|--------|
| R.CAST | Broadcast | `r_cast_engine` | 硕士课题 | 2027.03 | L3 | 学生 |
| R.FUSE | AllReduce | `r_fuse_engine` | 硕士课题 | 2027.09 | L3 | 学生 |
| C.LINK | Page Commit | `clink_page_commit` | 硕士课题 | 2027.06 | L3 | 学生 |
| SDI Crossbar | 交换矩阵 | `sdi_crossbar_4x4` | 硕士课题 | 2027.05 | L3 | 学生 |
| R.PULL | AllGather | `r_pull_gather` | 博士课题 | 2028.11 | L3 | 学生 |
| R.SWAP | AlltoAll | `r_swap_alltoall` | 博士课题 | 2028.12 | L3 | 学生 |
| R.PIPE | ReduceScatter | `r_pipe_scatter` | 博士课题 | 2028.11 | L3 | 学生 |
| R.MESH | NeighborExchange | `r_mesh_neighbor` | 博士课题 | 2028.11 | L3 | 学生 |
| T.GEMM | 矩阵乘加 | `t_gemm_systolic` | 博士课题 | 2028.10 | L3 | 学生 |
| T.FOLD | 向量归约 | `t_fold_reduce` | 博士课题 | 2028.10 | L3 | 学生 |
| T.MAPS | 逐元素映射 | `t_maps_elementwise` | 博士课题 | 2028.11 | L3 | 学生 |
| T.SCAN | 前缀扫描 | `t_scan_prefix` | 博士课题 | 2028.11 | L3 | 学生 |
| T.LOOK | 查表 | `t_look_lut` | 博士课题 | 2028.10 | L3 | 学生 |
| T.SPEC | 特殊函数 | `t_spec_cordic` | 博士课题 | 2028.12 | L3 | 学生 |
| C.TICK | 逻辑时钟 | `c_tick_clock` | 博士课题 | 2029.01 | L2 | 学生 |
| C.SYNC | Barrier | `c_sync_barrier` | 博士课题 | 2029.01 | L2 | 学生 |
| C.MOVE | DMA | `c_move_dma` | 博士课题 | 2029.02 | L2 | 学生 |

## 附录B：关键文件索引

| 文件 | 路径 | 用途 |
|------|------|------|
| TCC知识基线 | [TCC_Knowledge_Base_Baseline_v2.0.md](http://127.0.0.1:8899/vault/30_TCC/TCC_Knowledge_Base_Baseline_v2.0.md) | 原语权威定义 |
| RTL微架构规格 | [Gen1-MVP_RTL微架构与IP核详细规格_v1.0.md](http://127.0.0.1:8899/vault/50_Output/54_Code/iNEST/Gen1-MVP_RTL微架构与IP核详细规格_v1.0.md) | RTL设计参考 |
| FPGA验证方案 | [Gen1-MVP_FPGA验证与测试方案_v1.0.md](http://127.0.0.1:8899/vault/50_Output/54_Code/iNEST/Gen1-MVP_FPGA验证与测试方案_v1.0.md) | 验证方法学 |
| 天大工程规划 | [TCC计算范式_NDSC与天大细化工程规划_v1.0.md](http://127.0.0.1:8899/vault/30_TCC/34_Projects/TCC计算范式_NDSC与天大细化工程规划_v1.0.md) | 工程分工 |
| iNEST工程总规 | [00_iNEST工程开发总体规划_v1.0.md](http://127.0.0.1:8899/vault/50_Output/54_Code/iNEST/00_iNEST工程开发总体规划_v1.0.md) | 工程验证体系 |
| 液态拓扑方案 | [TCC_iNEST_LiquidTopology_v1.0.md](http://127.0.0.1:8899/vault/30_TCC/31_Theory/TCC_iNEST_LiquidTopology_v1.0.md) | Page模板系统 |
| SDI化合键工程 | [SDI化合键工程参数证明及工程实现方案.md](http://127.0.0.1:8899/vault/50_Output/54_Code/iNEST/SDI化合键工程参数证明及工程实现方案.md) | 物理参数 |
| FPGA落地路线图 | [LNN到iNEST到FPGA_持续推进落地路线图.md](http://127.0.0.1:8899/vault/50_Output/54_Code/iNEST/LNN到iNEST到FPGA_持续推进落地路线图.md) | 四阶段路线 |
| 工程边界定义 | [iNEST_TCC_工程边界定义.md](http://127.0.0.1:8899/vault/50_Output/54_Code/iNEST/iNEST_TCC_工程边界定义.md) | 分工边界 |
