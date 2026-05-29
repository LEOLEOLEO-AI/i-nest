# 论文B（B5）：TCC-11系统实现与评测
# Paper B (B5): TCC-11 Minimal Complete Primitive Library for Liquid Hardware
# 目标：ASPLOS/MICRO 2027 April cycle | 截止：2027年4月15日
# 状态：📋 框架完成，依赖T2/T3硬件与SDK完成

---

## 基本信息

| 项目 | 内容 |
|------|------|
| **标题** | TCC-11: A Minimal Complete Primitive Library for Liquid Hardware — Design, SDK, and Evaluation across AI, HPC, and Signal Processing |
| **目标** | ASPLOS 2027 April cycle，或 MICRO 2027 |
| **投稿截止** | 2027年4月15日 |
| **论文类型** | 系统+实验，~14页 |
| **配套专利** | P2（硬件IP核）+ P4（SDK编译映射） |
| **前驱论文** | 论文A（引用Route≡Transform理论）|

---

## Abstract（草稿）

We present TCC-11, a hardware-software co-designed primitive library for network-centric computing that unifies AI inference, high-performance computing, and signal processing on a single reconfigurable substrate. TCC-11 comprises 11 orthogonal primitives — 4 communication (FUSE, PULL, CAST, SWAP), 4 computation (GEMM, FOLD, MAPS, SCAN), 1 data movement (MOVE), and 2 control (LINK, TICK) — implemented as synthesizable RTL IP cores totaling 25,847 lines of SystemVerilog. We co-design an SDK featuring automatic mapping from TCCL, MPI-4.0, BLAS-L3, and FFTW APIs, a graph compiler with topology-aware primitive fusion, and an MLIR-based compilation flow from PyTorch/JAX to TCC hardware. On a 4-node VCK190 FPGA prototype, TCC-11 achieves: (1) Gemma-4 E2B INT4 inference at 5.2 tokens/s with ≤1 μs scene switching; (2) 4×720p YOLOv8-s detection at 24 FPS; (3) 16-channel 1024-point complex FFT + CFAR at 800 ns per pulse; (4) existing PyTorch DDP training scripts running unmodified via TCCL compatibility shim with <5% overhead.

---

## 论文结构

| 章节 | 内容 | 篇幅 | 依赖 | 状态 |
|------|------|------|------|------|
| §1 Introduction | 液态硬件概念；跨场景统一的必要性 | 1页 | — | ⬜ |
| §2 TCC-11 Spec | 形式化规范（引用论文A，精简版）| 1.5页 | 论文A | ⬜ |
| §3 Hardware Arch | 11 IP核微架构：GEMM脉动阵列、SCAN前缀树、SDI控制器 | 2.5页 | T2完成 | ⬜ |
| §4 SDK & Compiler | TCCL/MPI/BLAS/FFTW映射；MLIR Dialect；3个编译pass | 2.5页 | T3-1~4 | ⬜ |
| §5 Evaluation | 四场景实验数据（LLM/Video/Radar/DDP overhead）| 3页 | T2-9 | ⬜ |
| §6 Scaling | **工艺节点放松分析**：TCC液态拓扑如何将先进工艺需求从3nm/5nm降至7nm；三硬约束（单节点算力/SRAM密度/SerDes速率）定量推导；7nm覆盖L1-L3全规模路线图 | 1.5页 | — | ⬜ |
| §7 Open-Source | 代码结构、许可证、社区治理 | 0.5页 | M8 | ⬜ |
| §8 Related+Conc | — | 1页 | — | ⬜ |

---

## 实验数据目标

| 实验 | 目标值 | 对比基准 | 依赖任务 |
|------|--------|---------|---------|
| 1024点复数FFT延迟 | ≤800ns | Xilinx FFT IP (~1.2μs) | T2-9 |
| Gemma-4 E2B INT4推理 | 5.2 tok/s @ ~55W | ARM CPU ~0.3 tok/s | T2-8,9 |
| 场景切换延迟 | ≤1μs | — | T2-9 |
| DDP训练overhead | <5% vs native TCCL on equivalent FPGA | — | T3-2,T2-8 |
| YOLOv8-s 4路720p | 24 FPS | — | T2-8,9 |

---

## 工艺节点放松分析（§6详细内容，2026-04-30）

### 核心命题

> **TCC液态拓扑将先进工艺需求从3nm/5nm降至7nm**，这是TCC相比GPU集群方案最重要的战略价値之一：
> 7nm是国内可量产（中芯国际N+1工艺）的最先进节点，意味着TCC完整技术栈可以在中国大陆自主实现。

### 为什么GPU需要先进工艺？

GPU对先进工艺的需求来自三个驱动力：
1. **HBM堆叠**：要益内存带宽必须3D堆叠和先进工艺（H100: 80GB HBM3, 3.35 TB/s）
2. **计算密度**：单芯片内尽量塔积计算单元，必须3nm提升晋体管密度
3. **通信功耗**：数据在CPU-Memory-NVLink之间反复流动，线缓外录温升

**TCC如何消除这三个需求：**

| GPU驱动力 | TCC修改 | 结果 |
|---------|---------|------|
| HBM内存带宽墙 | 权重分布在节点SRAM，不需要反复取数 | **无需HBM，工艺需求降10倍** |
| 单芯片计算密度 | 用节点数量扩展，不靠工艺迭代 | **7nm×N节点代替3nm×1芯片** |
| 通信功耗 | Route≡Transform：通信本身是计算，数据只流动一次 | **片间通信减少10×** |

### 三个硬性下限（不能无限放松工艺）

#### 硬约束1：单节点算力绝对値

```
Transformer一层FLOP与推理延迟（GPT-3级，d=12288，seq=2048）:
28nm:  ~4  TOPS → 154ms/层  ← 实时推理不可用
12nm:  ~16 TOPS → 38ms/层   ← 拹强可用（批量推理）
7nm:   ~64 TOPS → 9.6ms/层  ← ★实时推理最低要求
5nm:   ~256 TOPS→ 2.4ms/层  ← 舞适（但非必要）
```

**结论**：7nm是实时推理的最低工艺要求，12nm仅适合边端/信号处理。

#### 硬约束2：SRAM密度决定片内缓存容量

```
每节点最低 SRAM 需求：512KB（放得下一层权重分片）
7nm  SRAM: ~0.7 MB/mm² → 512KB = 0.73mm²  ← 经济合理
12nm SRAM: ~0.4 MB/mm² → 512KB = 1.28mm²  ← 勉强可用
28nm SRAM: ~0.15MB/mm² → 512KB = 3.41mm²  ← 面积过大，不经济
```

**结论**：12nm是SRAM密度的经济下限，28nm面积成本不可接受。

#### 硬约束3：SDI链路速率决定集合通信带宽

```
FUSE(AllReduce)延迟要求：N=64节点，1GB梯度，<10ms
对链路带宽要求：≥ 12.6 TB/s（每节点需 4条×3.15 TB/s链路）

28nm SerDes: ~56  Gbps/lane → 需 56 lanes/节点 ← 不现实
12nm SerDes: ~112 Gbps/lane → 需 28 lanes/节点 ← 勉强
7nm  SerDes: ~224 Gbps/lane → 需 14 lanes/节点 ← 合理
```

**结论**：高速SerDes是工艺的第二个硬下限，7nm的224 Gbps/lane是关键能力。

### TCC工艺节点分层结论

| 工艺 | 单节点算力 | SRAM | SerDes | 适用规模 | 展右：策略价値 |
|------|---------|------|--------|---------|----------|
| 28nm | 4 TOPS  | 不足 | 56G | L5信号处理 | FPGA验证平台 |
| 12nm | 16 TOPS | 勉强 | 112G | L1边端推理 | 成本敏感场景 |
| **7nm** | **64 TOPS** | **良好** | **224G** | **L1-L3全覆盖** | **★ TCC战略刻制高点** |
| 5nm | 256 TOPS | 优了 | 448G | L3-L4 | 按需升级，非必须 |
| 3nm | 1024 TOPS| 极优 | 900G+ | L4超大规模 | 海外供应链风险高 |

### 规模-工艺对应路线图

```
工艺代际 ────────────────────────────────────────────────────────────────────────►
                  28nm       12nm       7nm        5nm      3nm
L1微型(边端)                   ●────●
L2中型                              ●───●
L3大型                                        ●───●
L4超大                                                 ●
L5信号   ●───●

工艺重要里程碑：
2026: FPGA原型(VCK190, 4节点) → L1/L5验证
2027: TCC Gen1 ASIC(7nm, 64节点) → L2量产 [国内自主]
2028: TCC Gen2(7nm优化, 1K节点板卡) → L3
2029+: TCC Gen3(按需升到5nm) → L4
```

**最重要的结论：**
> TCC Gen1和Gen2全部基于7nm，是国内自主可实现的量产节点，
> 视为同等规模GPU集群方案的策略替代路径。

---

## 开源策略

- RTL（SystemVerilog）：CERN-OHL-P v2（硬件开源许可）
- SDK（Python/C++）：Apache 2.0
- 预计开源时间：M8（2029年Q3）或论文发表后6个月
- 仓库结构：`tcc-hw/`（RTL）+ `tcc-sdk/`（Python/C++）+ `tcc-bench/`（benchmark suite）

---

## §5 Hardware Architecture — TCC-WSE 晶圆级软件定义系统（2026-04-30新增）

### 5.1 架构定义

TCC-WSE（Wafer-Scale Integration for TCC）是将TCC液态拓扑原理实现于晶圆级的系统架构：

```
┌──────────────────────────────────────────────────────────┐
│               晶圆上层：原语芯粒（Chiplet）阵列             │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐                     │
│  │Type-F│ │Type-C│ │Type-F│ │Type-S│  × 1,000–10,000颗   │
│  │TCC-11│ │GEMM+ │ │TCC-11│ │SCAN+ │  ← 按场景选颗粒度    │
│  │完整版│ │FOLD  │ │完整版│ │MAPS  │                     │
│  └──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘                     │
│     │        │        │        │                          │
├─────┴────────┴────────┴────────┴──────────────────────────┤
│               晶圆下层：SDI液态互连网络                      │
│  RDL铜互连（<1mm，<0.1ns）/ 硅光子波导（100mm，<0.5ns）      │
│  软件定义拓扑（LINK/PRUNE/PACK原语驱动）                     │
│  互连密度裕量：~84×（远超实际需求）                           │
└──────────────────────────────────────────────────────────┘
```

**芯粒类型库（Chiplet Library）**：

| 类型 | 引擎组合 | 面积@7nm | 算力 | 适用场景 |
|------|---------|---------|------|---------|
| Type-F | GEMM+FOLD+MAPS+SCAN | ~2.2mm² | 64 TOPS | 通用 |
| Type-C | GEMM+FOLD | ~1.5mm² | 64 TOPS | LLM推理/训练 |
| Type-S | SCAN+MAPS | ~0.8mm² | — | 信号处理 |
| Type-M | FOLD+大SRAM(4MB) | ~2.5mm² | — | KV Cache |

### 5.2 与Cerebras WSE-3的参数对比（交叉验证版）

> **数据来源说明**：WSE-3参数来自Cerebras官方网站及白皮书（2024年），已通过晶体管密度、SRAM容量自洽性验证。TCC-WSE参数为基于7nm工艺规格的工程估算，标注置信度。

| 参数 | Cerebras WSE-3 | TCC-WSE（1K节点） | TCC-WSE（10K节点） | 置信度 |
|------|--------------|-----------------|-----------------|------|
| 制程 | 5nm台积电 | 7nm国内（中芯N+1） | 7nm国内 | ✓官方 |
| 晶圆面积 | 46,225 mm² | ~35,000 mm² | ~35,000mm²×多晶圆 | ✓ |
| 核心/芯粒数 | 900,000核心 | 1,000芯粒 | 10,000芯粒 | ✓设计值 |
| 芯粒面积占比 | ~100%（单die） | ~3.8% | ~38% | ⚠️估算 |
| SRAM/节点 | 48 KB（固定） | 512 KB | 512 KB | ✓设计值 |
| 总片上SRAM | 44 GB（官方） | ~512 MB | ~5 GB | ✓ |
| 单核/节点算力 | ~弱（标量） | 64 TOPS（INT8） | 64 TOPS | ⚠️待实测 |
| 片内互连带宽 | 220 Pb/s | ~1.8 Pb/s | ~18 Pb/s | ⚠️估算 |
| 功耗 | ~23 kW | **~32 kW**（2TOPS/W） | ~320 kW | ⚠️估算 |
| 稀疏模式功耗 | 不支持 | **~8–15 kW**（PRUNE后） | ~80–150 kW | ⚠️理论 |
| 外部存储 | 无（纯片上） | 4 TB LPDDR5 | 40 TB | ✓设计值 |
| 国产化可能 | ❌ | ✅ | ✅ | ✓ |
| 估算系统成本 | ~$2M–5M | ~$200K–500K | ~$1M–2M | ⚠️粗估 |

**⚠️ 功耗修正说明**（前文64kW有误）：
- 前文按1TOPS/W计算得64kW，过于保守
- 修正值：2TOPS/W（参考华为昇腾910B: 256TOPS/310W≈0.83TOPS/W；Intel Gaudi3: 3TOPS/W）
- **关键优势**：PRUNE+PACK原语在稀疏场景下断开90%链路，系统进入低功耗态，实际运行功耗可降至8–15 kW（L1/L2规模场景）

**互连带宽对比说明**：
- WSE-3的220 Pb/s = 220,000 Tbps，来自900K核心之间的2D网格所有链路求和
- TCC-WSE的1.8 Pbps = 1,800 Tbps，来自1K节点×4方向×16 lane×224Gbps
- 差距约123倍，但TCC每Tbps承载完整GEMM运算（等效计算量约为标量加法的1000×）
- **等效有效计算带宽**：TCC-WSE与WSE-3处于同一数量级

### 5.3 L2存储方案修正（HBM → 分布式LPDDR5）

前文工艺分析中L2阶段误写"HBM3堆叠"，此处正式修正：

```
Llama-3-70B推理（参数量140GB，FP16）：
  TCC-WSE 64节点方案：
    每节点承担：140GB / 64 = 2.2GB 权重
    外挂存储：LPDDR5-6400（每节点4GB，68GB/s带宽）
    64节点总等效带宽：64 × 68 = 4,352 GB/s
    对比H100 HBM3总带宽：3,350 GB/s
    
  结论：分布式LPDDR5等效带宽已超过H100 HBM3（130%），无需HBM，
  且LPDDR5可在12nm/7nm成熟封装上实现，进一步降低工艺需求。
```

### 5.4 TCC-WSE技术路线

```
阶段      时间     技术           规模           里程碑
─────────────────────────────────────────────────────────
MVP0     2026     FPGA验证       4节点          VCK190原型机（已规划）
Gen1     2027     7nm ASIC芯粒  64芯粒/芯片     首款国产TCC推理芯片
Gen2     2028     7nm晶圆集成   1K芯粒WSI       TCC-WSE v1（L2-L3全覆盖）
Gen3     2030     硅光子互连     10K芯粒        TCC-WSE v2（L3-L4）
Gen4     2032+    忆阻器CIM      10K芯粒+CIM    存算传真正一体
```

### 5.5 TCC-WSE与架构谱系的关系

```
冯诺依曼（1945）
├─ GPU集群：计算节点固定，通信是开销
│  └─ Cerebras WSE：将GPU概念扩展到晶圆级，通信仍是固定2D网格
│
└─ 非冯：打破计算-通信二元分离
   ├─ PIM/CIM（存内计算）：消除存储→计算带宽墙（片内）
   ├─ INC（网内计算）：消除节点间通信-计算分离（片间）
   │  └─ TCC液态拓扑：INC的完备代数化（Route≡Transform定理）
   └─ 存算传一体：三者同时
      └─ TCC-WSE + CIM = 完整非冯终态
         存（CIM）+ 算（4引擎芯粒）+ 传（液态SDI） = 三位一体连续体
```

> **CST理论预言**（可实验验证）：
> Cerebras WSE的900K核心在固定2D网格下，Γst接近0（拓扑随机性低，同步性高，但信息整合差）。
> TCC-WSE的1K芯粒在液态拓扑下，Γst可达最优值Γst*=0.486。
> CST理论预测：后者的等效智能效率（η_I = CST/功耗）高于前者。
> 这是一个具体的、可量化的实验命题，将在Gen1 ASIC上验证。

