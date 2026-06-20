---
title: "Gen1-MVP智涌脑 RTL微架构与IP核详细规格"
date: 2026-06-18
version: v1.0
status: Final
author: iNEST Engineering Team (天津大学/NDSC)
based_on:
  - sdio_bond_core_v24.v (153行, FEP+STDP+异步电路IP)
  - v28_fpga_resource.json (N=321保守, 3.07mW)
  - 六级智能跃迁验证体系 (L1-L6仿真全通过)
target: Xilinx VCK190 (Versal ACAP)
tags:
  - RTL
  - 微架构
  - IP核
  - Gen1-MVP
  - FPGA
  - Verilog
  - 寄存器映射
  - 验证方案
---

# Gen1-MVP智涌脑 RTL微架构与IP核详细规格 v1.0

> **定位**：Gen1-MVP 智涌脑的完整 RTL 设计方案。从顶层架构到模块级接口、寄存器映射、FPGA资源预算、验证策略——可以直接作为硬件团队的开发起点。

---

## 一、顶层架构

### 1.1 顶层框图

```
┌──────────────────────────────────────────────────────────────────┐
│                   iNEST_Gen1_MVP_Top                              │
│                   (Xilinx VCK190 / Versal ACAP)                   │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    SDI Crossbar Matrix                       │ │
│  │                    (sdio_crossbar_4x4)                       │ │
│  │                                                              │ │
│  │   ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐               │ │
│  │   │ PE_0 │◄─►│ PE_1 │◄─►│ PE_2 │◄─►│ PE_3 │               │ │
│  │   │(75N) │   │(75N) │   │(75N) │   │(75N) │               │ │
│  │   └──┬───┘   └──┬───┘   └──┬───┘   └──┬───┘               │ │
│  │      │           │           │           │                    │ │
│  │      └───────────┼───────────┼───────────┘                    │ │
│  │                  │  SDI Config Bus (AXI4-Lite)                │ │
│  │           ┌──────┴──────┐                                    │ │
│  │           │ SDI Config  │                                    │ │
│  │           │ Memory (BRAM)│                                   │ │
│  │           └─────────────┘                                    │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌──────────────────────┐  ┌──────────────────────┐              │
│  │   FEP Engine          │  │   CST Estimator      │              │
│  │   (fep_engine_top)    │  │   (cst_estimator)    │              │
│  │                       │  │                       │              │
│  │  • KL散度流水线       │  │  • S_c 谱分析         │              │
│  │  • 惊讶度跟踪         │  │  • T_c 多尺度熵       │              │
│  │  • 自由能输出         │  │  • σ 小世界指数       │              │
│  └──────────────────────┘  └──────────────────────┘              │
│                                                                   │
│  ┌──────────────────────┐  ┌──────────────────────┐              │
│  │  STDP+BCM Accelerator │  │  SOC Controller       │              │
│  │  (stdp_bcm_accel)    │  │  (soc_controller)    │              │
│  │                       │  │                       │              │
│  │  • 脉冲时间差检测     │  │  • glia缩放事件生成   │              │
│  │  • BCM滑动阈值        │  │  • 全局缩放因子       │              │
│  │  • 权重更新仲裁       │  │  • 临界态维持         │              │
│  └──────────────────────┘  └──────────────────────┘              │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    System Control & I/O                       │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │ │
│  │  │AXI Master│  │ Sensor   │  │ UART     │  │ JTAG     │   │ │
│  │  │(DDR access)│ │ I/F (MIPI│  │ Debug    │  │ Config   │   │ │
│  │  │          │  │ /SPI/I2S)│  │ Port     │  │ Port     │   │ │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  Clock & Reset:                                                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │sys_clk   │  │async_clk │  │sensor_clk│  │axi_clk   │        │
│  │200MHz    │  │50MHz     │  │24MHz     │  │150MHz    │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
└──────────────────────────────────────────────────────────────────┘
```

### 1.2 模块清单与接口

| 模块名 | 文件 | 功能 | 类型 | 接口 | 状态 |
|--------|------|------|------|------|------|
| `iNEST_Gen1_MVP_Top` | `inest_gen1_top.v` | 顶层集成 | Wrapper | AXI4-Lite + Sensor + UART + JTAG | **待开发** |
| `sdio_crossbar_4x4` | `sdio_crossbar_4x4.v` | 4×4 SDI交换矩阵 | Data Path | AXI4-Stream ×4 + Config BRAM | **待开发** |
| `pe_neuron_array` | `pe_neuron_array.v` | 75神经元异步脉冲阵列 | Compute | NCL handshake + Bond I/F | **待开发** |
| `sdio_bond_core_v24` | `sdio_bond_core_v24.v` | **单化合键IP核 (已完成)** | Compute | NCL双轨 + FEP状态 | ✅ **已完成** |
| `sdio_bond_matrix` | `sdio_bond_matrix.v` | 化合键矩阵管理器 | Control | Bond仲裁 + 统计 | **待开发** |
| `fep_engine_top` | `fep_engine_top.v` | FEP自由能计算引擎 | Compute | AXI4-Lite Slave | **待开发** |
| `cst_estimator` | `cst_estimator.v` | CST在线估算 | Compute | AXI4-Lite Slave | **待开发** |
| `stdp_bcm_accel` | `stdp_bcm_accel.v` | STDP+BCM硬件加速器 | Compute | Bond Matrix I/F | **待开发** |
| `soc_controller` | `soc_controller.v` | SOC控制器 | Control | 全局广播 | **待开发** |
| `adaptive_tau_ctrl` | `adaptive_tau_ctrl.v` | 自适应tau控制器 | Control | 时钟分频控制 | **待开发** |
| `sensor_if` | `sensor_if.v` | 传感器接口适配 | I/O | MIPI/SPI/I2S → AXI-Stream | **待开发** |
| `sys_ctrl` | `sys_ctrl.v` | 系统控制器 | Control | AXI4-Lite Master + UART + JTAG | **待开发** |

### 1.3 FPGA资源预算（基于v28实测数据）

| 资源 | v28估测 (N=1024) | Gen1-MVP保守 (N=300) | Gen1-MVP乐观 (N=321) | VCK190可用 | 利用率 |
|------|-----------------|---------------------|---------------------|-----------|--------|
| **LUTs** | 2,150,400 (239%) | 631,000 | 675,000 | ~900K | **70-75%** |
| **DSPs** | 4,096 | ~1,200 | ~1,280 | 1,968 | **61-65%** |
| **BRAM (KB)** | 153.6 | ~45 | ~48 | 34.6Mb | <5% |
| **功耗 (mW)** | 3.07 | ~0.9 | ~1.0 | — | — |
| **等效时钟 (MHz)** | 200 | 200 | 200 | — | — |
| **延迟/脉冲 (ns)** | 5.0 | 5.0 | 5.0 | — | — |
| **吞吐 (M spikes/s)** | 40.0 | ~11.7 | ~12.5 | — | — |

> **关键结论**：N=300节点是VCK190的安全边界（~70% LUT利用率），预留30%给FEP Engine、CST Estimator、STDP/BCM加速器等新增模块。

---

## 二、IP核详细规格

### 2.1 SDI化合键交换矩阵 (`sdio_crossbar_4x4`)

#### 2.1.1 功能描述

4×4全连接Crossbar，支持μs级运行时拓扑重构。每个PE可通过SDI化合键与任意其他PE建立有向/无向连接。

#### 2.1.2 顶层接口

```verilog
module sdio_crossbar_4x4 #(
    parameter DATA_WIDTH = 16,        // 脉冲数据宽度
    parameter NUM_PE      = 4,        // PE数量
    parameter NUM_PORTS   = 16        // 端口数 (4 PE × 4 端口/PE)
) (
    // 脉冲接口 (每个PE 4个端口: N/E/S/W)
    input  wire [NUM_PORTS*DATA_WIDTH-1:0] spike_in,    // PE→Crossbar脉冲
    output wire [NUM_PORTS*DATA_WIDTH-1:0] spike_out,   // Crossbar→PE脉冲
    output wire [NUM_PORTS-1:0]            spike_valid, // 脉冲有效标志

    // SDI配置接口 (AXI4-Lite Slave)
    input  wire        s_axi_aclk,
    input  wire        s_axi_aresetn,
    input  wire [7:0]  s_axi_awaddr,
    input  wire        s_axi_awvalid,
    output wire        s_axi_awready,
    input  wire [31:0] s_axi_wdata,
    input  wire [3:0]  s_axi_wstrb,
    input  wire        s_axi_wvalid,
    output wire        s_axi_wready,
    output wire [1:0]  s_axi_bresp,
    output wire        s_axi_bvalid,
    input  wire        s_axi_bready,
    input  wire [7:0]  s_axi_araddr,
    input  wire        s_axi_arvalid,
    output wire        s_axi_arready,
    output wire [31:0] s_axi_rdata,
    output wire [1:0]  s_axi_rresp,
    output wire        s_axi_rvalid,
    input  wire        s_axi_rready,

    // 状态输出
    output wire [NUM_PE-1:0] pe_active,   // PE活跃指示
    output wire [15:0]       bond_count,  // 活跃化合键数

    // 时钟与复位
    input  wire clk,    // 200MHz系统时钟
    input  wire rst_n
);
```

#### 2.1.3 寄存器映射

| 地址 | 寄存器 | 位宽 | 访问 | 描述 |
|------|--------|------|------|------|
| `0x00` | `SDI_CTRL` | 32 | R/W | [0] enable, [1] reset_bonds, [2] topology_load, [7:4] topology_id |
| `0x04` | `SDI_STATUS` | 32 | RO | [15:0] bond_count, [19:16] pe_active, [31:20] reserved |
| `0x08` | `SDI_TOPO_ID` | 32 | R/W | 拓扑类型: 0=Ring, 1=Butterfly, 2=Star, 3=All-to-All, 4=Custom |
| `0x0C` | `SDI_SWITCH_DELAY` | 32 | R/W | [15:0] 切换延迟(cycles), 200MHz→5ns/cycle, 默认2000→10μs |
| `0x10-0x4C` | `SDI_BOND_CFG[0:15]` | 32×16 | R/W | 每个端口的化合键配置: [3:0] src_pe, [7:4] dst_pe, [8] direction, [9] enable |
| `0x50` | `SDI_BOND_STATS` | 32 | RO | 化合键统计: [15:0] E-S键数, [31:16] E-L键数 |
| `0x54` | `SDI_CUSTOM_TOPO[0:15]` | 32×16 | R/W | 自定义拓扑: 16条键的src→dst映射 |

#### 2.1.4 关键时序

| 参数 | 目标值 | 说明 |
|------|--------|------|
| 拓扑切换延迟 | <10μs (MVP) / <1μs (Gen1 ASIC) | 从配置写入到新拓扑生效 |
| 脉冲路由延迟 | <5ns | Crossbar内脉冲转发延迟 |
| 配置写入延迟 | <100ns (AXI4-Lite) | 单寄存器写入 |
| 时钟频率 | 200MHz | 等效系统时钟 |

#### 2.1.5 内部架构

```
┌─────────────────────────────────────────┐
│           sdio_crossbar_4x4              │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │        Connection Matrix            │ │
│  │    ┌───┬───┬───┬───┐              │ │
│  │ PE0│ ■ │ □ │ □ │ ■ │              │ │
│  │    ├───┼───┼───┼───┤              │ │
│  │ PE1│ □ │ ■ │ ■ │ □ │              │ │
│  │    ├───┼───┼───┼───┤              │ │
│  │ PE2│ ■ │ □ │ ■ │ □ │              │ │
│  │    ├───┼───┼───┼───┤              │ │
│  │ PE3│ □ │ ■ │ □ │ ■ │              │ │
│  │    └───┴───┴───┴───┘              │ │
│  │     ■=connected  □=open            │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌──────────────┐  ┌──────────────┐     │
│  │  Bond Config  │  │  Bond Stats  │     │
│  │  BRAM (512b)  │  │  Counter     │     │
│  └──────────────┘  └──────────────┘     │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │       AXI4-Lite Slave IF           │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

---

### 2.2 PE神经元阵列 (`pe_neuron_array`)

#### 2.2.1 功能描述

每个PE包含75个异步脉冲神经元（NCL逻辑），4个PE共300神经元。神经元通过`sdio_bond_core_v24`与片内/跨PE神经元建立化合键连接。

#### 2.2.2 顶层接口

```verilog
module pe_neuron_array #(
    parameter NUM_NEURONS = 75,          // PE内神经元数
    parameter NUM_BONDS   = 750,         // PE内化合键数 (平均度≈10)
    parameter DATA_WIDTH  = 16
) (
    // 片内键接口 (连接到crossbar的4个端口)
    input  wire [3:0][DATA_WIDTH-1:0] spike_in_port,   // 来自crossbar的脉冲
    output wire [3:0][DATA_WIDTH-1:0] spike_out_port,  // 发往crossbar的脉冲
    output wire [3:0]                 spike_out_valid,

    // 全局控制
    input  wire [DATA_WIDTH-1:0] glia_scale_factor,    // 胶质缩放因子
    input  wire [7:0]            bcm_theta_base,       // BCM基础阈值
    input  wire                  consolidate_enable,   // 全局固化使能

    // FEP状态（发送给FEP Engine）
    output wire [NUM_NEURONS-1:0] neuron_converged,    // 神经元收敛标志
    output wire [15:0]            avg_surprise,        // 平均惊讶度

    // CST数据（发送给CST Estimator）
    output wire [DATA_WIDTH-1:0] spike_rate,           // 发放率
    output wire [DATA_WIDTH-1:0] cv_isi,               // ISI变异系数

    // 时钟与复位
    input  wire clk_equiv,  // 200MHz等效时钟
    input  wire rst_n
);
```

#### 2.2.3 内部架构

```
pe_neuron_array (75 neurons)
│
├── 75× sdio_bond_core_v24 (已完成IP, 153行/实例)
│   ├── 每个实例: FEP+STDP+异步电路
│   ├── NCL双轨握手协议
│   └── 输出: weight, bond_type, consolidate_event, fep_out
│
├── Neuron State Manager
│   ├── 膜电位追踪 (75×16bit寄存器)
│   ├── 发放阈值比较器
│   └── 不应期定时器
│
├── Bond Arbiter
│   ├── 750→4 端口仲裁（每PE 4个crossbar端口）
│   ├── Round-robin调度
│   └── 优先级: E-L键 > E-S键
│
└── PE Statistics Collector
    ├── spike_rate: 75神经元平均发放率
    ├── cv_isi: 发放间隔变异系数
    ├── neuron_converged: FEP收敛标志位图
    └── avg_surprise: 平均惊讶度
```

#### 2.2.4 FPGA实现关键点

| 关键点 | 方案 | 说明 |
|--------|------|------|
| 75×sdio_bond_core_v24实例化 | generate循环 | 每个bond_core约占用~250 LUTs |
| NCL握手到同步桥接 | 双时钟FIFO | NCL异步域→200MHz同步域 |
| bond仲裁 | 固定优先级+轮询混合 | E-L键优先级更高 |
| 膜电位存储 | 分布式RAM (LUTRAM) | 75×16bit, 无需BRAM |

---

### 2.3 FEP自由能计算引擎 (`fep_engine_top`)

#### 2.3.1 功能描述

硬件化FEP自由能计算：KL散度流水线 + 惊讶度跟踪 + 自由能输出。更新频率>1kHz。

#### 2.3.2 顶层接口

```verilog
module fep_engine_top #(
    parameter NUM_NEURONS = 300,         // 全系统神经元数
    parameter DATA_WIDTH  = 16,
    parameter FRAC_BITS   = 8            // Q8.8定点格式
) (
    // 输入：来自所有PE的FEP状态
    input  wire [NUM_NEURONS-1:0] neuron_converged,  // 神经元收敛标志
    input  wire [15:0]            avg_surprise_0,    // PE0平均惊讶度
    input  wire [15:0]            avg_surprise_1,
    input  wire [15:0]            avg_surprise_2,
    input  wire [15:0]            avg_surprise_3,

    // 输出：FEP计算结果
    output wire [DATA_WIDTH-1:0] free_energy,          // 全局自由能 F
    output wire [DATA_WIDTH-1:0] kl_divergence,        // KL散度
    output wire [DATA_WIDTH-1:0] expected_surprise,    // 期望惊讶度
    output wire                  fep_converged,        // FEP收敛标志

    // 配置接口 (AXI4-Lite)
    input  wire        s_axi_aclk,
    input  wire        s_axi_aresetn,
    // ... (标准AXI4-Lite信号, 省略)

    // 时钟与复位
    input  wire clk,    // 200MHz
    input  wire rst_n
);
```

#### 2.3.3 寄存器映射

| 地址 | 寄存器 | 位宽 | 访问 | 描述 |
|------|--------|------|------|------|
| `0x00` | `FEP_CTRL` | 32 | R/W | [0] enable, [1] reset, [3:2] mode (0=continuous, 1=triggered) |
| `0x04` | `FEP_STATUS` | 32 | RO | [0] converged, [1] busy, [15:8] iteration_count |
| `0x08` | `FEP_FREE_ENERGY` | 32 | RO | Q16.16 自由能值 |
| `0x0C` | `FEP_KL_DIV` | 32 | RO | Q16.16 KL散度 |
| `0x10` | `FEP_SURPRISE` | 32 | RO | Q16.16 期望惊讶度 |
| `0x14` | `FEP_PRIOR_MEAN` | 32 | R/W | Q16.16 先验均值 |
| `0x18` | `FEP_PRIOR_VAR` | 32 | R/W | Q16.16 先验方差 |
| `0x1C` | `FEP_CONV_THRESH` | 32 | R/W | Q16.16 收敛阈值, 默认0.01 |
| `0x20` | `FEP_UPDATE_PERIOD` | 32 | R/W | 更新周期(cycles), 默认200K→1kHz@200MHz |

#### 2.3.4 定点运算流水线

```
FEP Engine 流水线 (5级, 200MHz)
│
Stage 1: 惊讶度聚合
├── 4×PE惊讶度 → 加权平均 → 全局惊讶度
└── Delay: 1 cycle

Stage 2: KL散度计算
├── D_KL = Σ p(x)log(p(x)/q(x))
├── DSP: 16×16→32乘法 + 对数查表(BRAM)
└── Delay: 3 cycles (乘法1 + 对数2)

Stage 3: 自由能计算
├── F = D_KL - E[surprise]
├── DSP: 32bit减法
└── Delay: 1 cycle

Stage 4: 收敛检测
├── ΔF < FEP_CONV_THRESH 连续3次 → converged
└── Delay: 1 cycle

Stage 5: 输出锁存
├── 寄存最终值到AXI可读寄存器
└── Delay: 1 cycle

总延迟: 7 cycles = 35ns @ 200MHz
```

---

### 2.4 CST在线估算器 (`cst_estimator`)

#### 2.4.1 功能描述

在线计算CST核心指标：S_c（空间复杂度谱分析）、T_c（时间多尺度熵）、σ（小世界指数）。延迟<1ms。

#### 2.4.2 寄存器映射

| 地址 | 寄存器 | 位宽 | 访问 | 描述 |
|------|--------|------|------|------|
| `0x00` | `CST_CTRL` | 32 | R/W | [0] enable, [1] trigger_single, [2] continuous_mode |
| `0x04` | `CST_S_C` | 32 | RO | Q8.24 空间复杂度 S_c |
| `0x08` | `CST_T_C` | 32 | RO | Q8.24 时间复杂度 T_c |
| `0x0C` | `CST_SIGMA` | 32 | RO | Q8.24 小世界指数 σ |
| `0x10` | `CST_GAMMA_ST` | 32 | RO | Q8.24 时空耦合度 Γ_st |
| `0x14` | `CST_SCORE` | 32 | RO | Q8.24 CST综合分数 |
| `0x18` | `CST_PHASE` | 32 | RO | [1:0] 相态: 0=亚临界, 1=临界, 2=超临界 |
| `0x1C` | `CST_UPDATE_PERIOD` | 32 | R/W | 更新周期, 默认200K→1kHz |
| `0x20` | `CST_THETA_K` | 32 | R/W | 临界阈值, 默认对应σ=4.0的CST值 |

#### 2.4.3 硬件加速策略

| 计算步骤 | 硬件实现 | 资源 | 延迟 |
|---------|---------|------|------|
| S_c: 邻接矩阵特征值 | 幂迭代法 (Power Iteration) | 4 DSP + 2 BRAM | <50μs |
| T_c: 多尺度熵 (MSE) | 粗粒化+样本熵流水线 | 8 DSP + 4 BRAM | <100μs |
| σ: 小世界指数 | S_c/随机等效S_c比值 | 1 DSP | <10μs |
| Γ_st: 时空耦合 | 互信息SVD近似 | 16 DSP + 8 BRAM | <500μs |
| CST综合 | DSP融合 | 2 DSP | <10μs |
| **总计** | | ~30 DSP + ~14 BRAM | **<1ms** |

---

### 2.5 STDP+BCM硬件加速器 (`stdp_bcm_accel`)

#### 2.5.1 功能描述

硬件化STDP脉冲时间差检测 + BCM滑动阈值追踪。与`sdio_bond_core_v24`（已完成LTP/LTD计数）配合，提供全局学习率控制和阈值自适应。

#### 2.5.2 寄存器映射

| 地址 | 寄存器 | 位宽 | 访问 | 描述 |
|------|--------|------|------|------|
| `0x00` | `STDP_CTRL` | 32 | R/W | [0] enable, [1] freeze_weights |
| `0x04` | `BCM_THETA` | 32 | R/W | Q8.24 BCM滑动阈值, 默认15 |
| `0x08` | `BCM_ETA` | 32 | R/W | Q8.24 BCM学习率, 默认0.25 |
| `0x0C` | `BCM_THETA_LTP` | 32 | R/W | 固化阈值, 默认14 |
| `0x10` | `STDP_LTP_RATE` | 32 | R/W | Q8.24 LTP增强系数, 默认1.4 |
| `0x14` | `STDP_LTD_RATE` | 32 | R/W | Q8.24 LTD抑制系数, 默认0.6 |
| `0x18` | `STDP_STATS` | 32 | RO | [15:0] LTP事件数, [31:16] LTD事件数 |

---

### 2.6 SOC控制器 (`soc_controller`)

#### 2.6.1 功能描述

实现自组织临界态（SOC）维持：胶质细胞全局缩放事件生成 + 全局缩放因子广播。基于V11仿真验证。

#### 2.6.2 寄存器映射

| 地址 | 寄存器 | 位宽 | 访问 | 描述 |
|------|--------|------|------|------|
| `0x00` | `SOC_CTRL` | 32 | R/W | [0] enable, [1] auto_scale |
| `0x04` | `SOC_SCALE` | 32 | R/W | Q8.24 全局缩放因子, 默认1.0 |
| `0x08` | `SOC_PERIOD` | 32 | R/W | 缩放事件周期(ms), 默认100ms |
| `0x0C` | `SOC_SIGMA_TARGET` | 32 | R/W | σ目标值, 默认4.0 (Gen1感知级) |
| `0x10` | `SOC_SIGMA_ACTUAL` | 32 | RO | σ实际值（来自CST Estimator） |
| `0x14` | `SOC_DELTA` | 32 | RO | σ_target - σ_actual |

#### 2.6.3 SOC控制算法

```
每SOC_PERIOD:
  1. 读取CST_SIGMA
  2. Δ = SOC_SIGMA_TARGET - CST_SIGMA
  3. IF |Δ| > 0.5:
       SOC_SCALE *= (1 + 0.1 * Δ)  // 比例反馈
       广播SOC_SCALE到所有PE
  4. IF CST_SIGMA持续3周期在[3.8, 4.2]:
       标记SOC_CONVERGED
```

---

### 2.7 自适应tau控制器 (`adaptive_tau_ctrl`)

#### 2.7.1 功能描述

基于惊讶度驱动的可变延迟线：惊喜度↑→tau↓（加速采样），惊喜度↓→tau↑（节省功耗）。基于V9仿真验证。

#### 2.7.2 实现方案

```
┌────────────────────────────────────┐
│      adaptive_tau_ctrl              │
│                                     │
│  avg_surprise ──► Comparator ──► tau_sel (8档)
│                      │              │
│              ┌───────┴───────┐     │
│              │ Surprise→Tau  │     │
│              │ 查表 (LUT)    │     │
│              └───────┬───────┘     │
│                      ▼              │
│              tau_sel [2:0]          │
│              │                      │
│     ┌────────┼────────┐            │
│     ▼        ▼        ▼            │
│  1/1     1/2 ...  1/256            │
│  (5ns)  (10ns)   (1280ns)          │
│                                     │
│  输出: tau_clk (门控时钟)            │
└────────────────────────────────────┘

Surprise→Tau映射表 (V9仿真验证, tau_mean=2.47):
┌──────────┬──────┬─────────────┐
│ Surprise │ Tau  │ Clock Div   │
├──────────┼──────┼─────────────┤
│ <0.3     │ 4.0  │ /16 (80ns)  │ ← 低惊喜, 减缓
│ 0.3-0.5  │ 3.0  │ /8  (40ns)  │
│ 0.5-0.7  │ 2.5  │ /4  (20ns)  │ ← 目标区间
│ 0.7-0.9  │ 2.0  │ /2  (10ns)  │
│ >0.9     │ 1.5  │ /1  (5ns)   │ ← 高惊喜, 加速
└──────────┴──────┴─────────────┘
```

---

## 三、系统集成与时钟架构

### 3.1 时钟域规划

```
┌─────────────────────────────────────────────┐
│              Clock Architecture              │
│                                              │
│  sys_clk (200MHz)                             │
│  ├── SDI Crossbar (同步)                      │
│  ├── FEP Engine (同步)                        │
│  ├── CST Estimator (同步)                     │
│  ├── STDP/BCM Accel (同步)                    │
│  ├── SOC Controller (同步)                    │
│  └── System Ctrl (同步)                       │
│                                              │
│  async_clk (50MHz, 门控)                      │
│  └── PE Neuron Arrays (NCL异步→等效时钟)        │
│      └── adaptive_tau_ctrl → tau_clk          │
│                                              │
│  sensor_clk (24MHz)                           │
│  └── Sensor Interface                         │
│                                              │
│  axi_clk (150MHz)                             │
│  └── AXI Interconnect                         │
│                                              │
│  跨时钟域桥接:                                 │
│  ├── async↔sys: 双时钟FIFO (深度16)           │
│  └── sensor↔sys: 双时钟FIFO (深度256)         │
└─────────────────────────────────────────────┘
```

### 3.2 顶层RTL实例化结构

```verilog
// iNEST_Gen1_MVP_Top 伪代码结构
module iNEST_Gen1_MVP_Top (
    input  wire sys_clk_p, sys_clk_n,    // 200MHz差分
    input  wire sensor_clk,               // 24MHz
    input  wire rst_n,
    // 传感器
    input  wire [3:0] mipi_data_p, mipi_data_n,
    input  wire mipi_clk_p, mipi_clk_n,
    // 调试
    input  wire uart_rx,
    output wire uart_tx,
    // DDR
    // ... AXI Master to DDR
);
    // === 时钟生成 ===
    wire sys_clk, axi_clk, async_clk;
    clk_wiz_0 clk_gen (
        .clk_in1_p(sys_clk_p), .clk_in1_n(sys_clk_n),
        .clk_out1(sys_clk),     // 200MHz
        .clk_out2(axi_clk),     // 150MHz
        .clk_out3(async_clk),   // 50MHz
        .resetn(rst_n), .locked(pll_locked)
    );

    // === SDI Crossbar ===
    wire [63:0] spike_to_crossbar, spike_from_crossbar;
    wire [3:0]  spike_valid;

    sdio_crossbar_4x4 crossbar (
        .spike_in(spike_from_pe), .spike_out(spike_to_pe),
        .spike_valid(spike_valid),
        .s_axi_aclk(axi_clk), .s_axi_aresetn(rst_n),
        // ... AXI连接到sys_ctrl
        .clk(sys_clk), .rst_n(rst_n)
    );

    // === 4× PE Neuron Arrays ===
    genvar i;
    generate
        for (i = 0; i < 4; i = i + 1) begin : pe_gen
            pe_neuron_array #(.NUM_NEURONS(75)) pe_i (
                .spike_in_port(spike_to_pe[i*16+:16]),
                .spike_out_port(spike_from_pe[i*16+:16]),
                .spike_out_valid(spike_valid_pe[i]),
                .glia_scale_factor(soc_scale),
                .bcm_theta_base(bcm_theta),
                .consolidate_enable(consolidate_en),
                .neuron_converged(neuron_conv[i*75+:75]),
                .avg_surprise(pe_surprise[i]),
                .spike_rate(pe_spike_rate[i]),
                .cv_isi(pe_cv_isi[i]),
                .clk_equiv(async_clk_gated[i]),
                .rst_n(rst_n)
            );
        end
    endgenerate

    // === FEP Engine ===
    fep_engine_top fep_eng (
        .neuron_converged(neuron_conv),
        .avg_surprise_0(pe_surprise[0]), // ...
        .free_energy(fep_free_energy),
        .kl_divergence(fep_kl),
        .fep_converged(fep_conv),
        .s_axi_aclk(axi_clk), .s_axi_aresetn(rst_n),
        .clk(sys_clk), .rst_n(rst_n)
    );

    // === CST Estimator ===
    cst_estimator cst_est (
        .bond_matrix(bond_active_bitmap),
        .spike_rates({pe_spike_rate[3:0]}),
        .cv_isis({pe_cv_isi[3:0]}),
        .s_c(cst_s_c), .t_c(cst_t_c), .sigma(cst_sigma),
        .gamma_st(cst_gamma_st), .cst_score(cst_score),
        .phase(cst_phase),
        .s_axi_aclk(axi_clk), .s_axi_aresetn(rst_n),
        .clk(sys_clk), .rst_n(rst_n)
    );

    // === SOC Controller ===
    soc_controller soc_ctrl (
        .cst_sigma(cst_sigma),
        .soc_scale(soc_scale),
        .s_axi_aclk(axi_clk), .s_axi_aresetn(rst_n),
        .clk(sys_clk), .rst_n(rst_n)
    );

    // === STDP+BCM Accelerator ===
    stdp_bcm_accel stdp_bcm (
        .bond_stats(bond_stats),
        .bcm_theta(bcm_theta),
        .s_axi_aclk(axi_clk), .s_axi_aresetn(rst_n),
        .clk(sys_clk), .rst_n(rst_n)
    );

    // === System Controller + AXI Interconnect ===
    sys_ctrl sys_ctrl_inst (
        .uart_rx(uart_rx), .uart_tx(uart_tx),
        // M_AXI → DDR
        // S_AXI → 各模块控制
        .clk(sys_clk), .rst_n(rst_n)
    );
endmodule
```

---

## 四、开发优先级与工作分解

### 4.1 开发阶段

| 阶段 | 时间 | 任务 | 产出 | 依赖 |
|------|------|------|------|------|
| **S1** | 2026 Q3 | 单bond_core验证+4×4 crossbar RTL | sdio_crossbar_4x4.v + 验证环境 | v24已完成 |
| **S2** | 2026 Q3-Q4 | PE Neuron Array集成测试 | pe_neuron_array.v + system_tb | S1 |
| **S3** | 2026 Q4 | FEP Engine + CST Estimator RTL | fep_engine_top.v + cst_estimator.v | S2 |
| **S4** | 2027 Q1 | 全系统集成仿真 | inest_gen1_top.v 功能仿真通过 | S2+S3 |
| **S5** | 2027 Q2 | FPGA综合+布局布线 | VCK190 bitstream + 时序收敛 | S4 |
| **S6** | 2027 Q3 | 片上测试: CST+FEP+行为 | 测试报告 + Demo视频 | S5 |

### 4.2 团队分工

| 模块 | 负责人 | 人数 | 周期 |
|------|--------|------|------|
| SDI Crossbar + Bond Matrix | 天大 (博士生×1) | 1 | 3个月 |
| PE Neuron Array (含75× bond_core集成) | 天大 (博士生×2) | 2 | 4个月 |
| FEP Engine | 复旦 (博士生×1) | 1 | 3个月 |
| CST Estimator | 天大+复旦 (博士生×1+硕士生×1) | 2 | 4个月 |
| STDP/BCM Accel + SOC Ctrl | 复旦 (博士生×1) | 1 | 3个月 |
| Adaptive Tau Ctrl | 天大 (硕士生×1) | 1 | 2个月 |
| Sensor I/F + Sys Ctrl + AXI | NDSC (工程师×1) | 1 | 3个月 |
| 顶层集成+验证 | 天大 (博士后×1) | 1 | 3个月 |
| **合计** | | **10人** | |

### 4.3 开发环境

| 工具 | 用途 | 版本 |
|------|------|------|
| Vivado | RTL综合+布局布线 | 2024.1+ |
| ModelSim/QuestaSim | 功能仿真 | 2023.4+ |
| Vitis HLS | FEP/CST算法C→RTL验证 | 2024.1+ |
| ILA (Integrated Logic Analyzer) | 片上调试 | Vivado内置 |
| Python (cocotb) | 验证框架 | 1.8+ |

---

## 附录A：已完成IP核清单

| IP核 | 文件 | 行数 | 功能 | 验证状态 |
|------|------|------|------|---------|
| `sdio_bond_core_v24` | `sdio_bond_core_v24.v` | 153 | FEP+STDP+异步电路单键IP | ✅ RTL完成, 基础TB通过 |
| `sdio_bond_core_v0.1` | `sdio_bond_core.v` | ~80 | 基础STDP+异步IP | ✅ 基线版本 |

## 附录B：待开发IP核优先级矩阵

| 优先级 | IP核 | 理由 | 阻塞哪些下游 |
|--------|------|------|------------|
| **P0** | `sdio_crossbar_4x4` | 数据通路核心, 所有PE依赖 | PE集成, 全系统 |
| **P0** | `pe_neuron_array` | 计算核心, 所有指标来源 | FEP, CST, 行为验证 |
| **P1** | `fep_engine_top` | 涌现驱动引擎 | CST验证, M0里程碑 |
| **P1** | `cst_estimator` | 涌现度量硬件化 | M0里程碑 |
| **P2** | `stdp_bcm_accel` | 在线学习加速 | Gen1完整Demo |
| **P2** | `soc_controller` | 临界态自动维持 | Gen1完整Demo |
| **P2** | `sys_ctrl` + `sensor_if` | 系统集成+Demo展示 | 最终交付 |
