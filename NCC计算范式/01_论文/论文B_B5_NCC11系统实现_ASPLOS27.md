# 论文B（B5）：NCC-11系统实现与评测
# Paper B (B5): NCC-11 Minimal Complete Primitive Library for Liquid Hardware
# 目标：ASPLOS/MICRO 2027 April cycle | 截止：2027年4月15日
# 状态：📋 框架完成，依赖T2/T3硬件与SDK完成

---

## 基本信息

| 项目 | 内容 |
|------|------|
| **标题** | NCC-11: A Minimal Complete Primitive Library for Liquid Hardware — Design, SDK, and Evaluation across AI, HPC, and Signal Processing |
| **目标** | ASPLOS 2027 April cycle，或 MICRO 2027 |
| **投稿截止** | 2027年4月15日 |
| **论文类型** | 系统+实验，~14页 |
| **配套专利** | P2（硬件IP核）+ P4（SDK编译映射） |
| **前驱论文** | 论文A（引用Route≡Transform理论）|

---

## Abstract（草稿）

We present NCC-11, a hardware-software co-designed primitive library for network-centric computing that unifies AI inference, high-performance computing, and signal processing on a single reconfigurable substrate. NCC-11 comprises 11 orthogonal primitives — 4 communication (FUSE, PULL, CAST, SWAP), 4 computation (GEMM, FOLD, MAPS, SCAN), 1 data movement (MOVE), and 2 control (LINK, TICK) — implemented as synthesizable RTL IP cores totaling 25,847 lines of SystemVerilog. We co-design an SDK featuring automatic mapping from NCCL, MPI-4.0, BLAS-L3, and FFTW APIs, a graph compiler with topology-aware primitive fusion, and an MLIR-based compilation flow from PyTorch/JAX to NCC hardware. On a 4-node VCK190 FPGA prototype, NCC-11 achieves: (1) Gemma-4 E2B INT4 inference at 5.2 tokens/s with ≤1 μs scene switching; (2) 4×720p YOLOv8-s detection at 24 FPS; (3) 16-channel 1024-point complex FFT + CFAR at 800 ns per pulse; (4) existing PyTorch DDP training scripts running unmodified via NCCL compatibility shim with <5% overhead.

---

## 论文结构

| 章节 | 内容 | 篇幅 | 依赖 | 状态 |
|------|------|------|------|------|
| §1 Introduction | 液态硬件概念；跨场景统一的必要性 | 1页 | — | ⬜ |
| §2 NCC-11 Spec | 形式化规范（引用论文A，精简版）| 1.5页 | 论文A | ⬜ |
| §3 Hardware Arch | 11 IP核微架构：GEMM脉动阵列、SCAN前缀树、SDI控制器 | 2.5页 | T2完成 | ⬜ |
| §4 SDK & Compiler | NCCL/MPI/BLAS/FFTW映射；MLIR Dialect；3个编译pass | 2.5页 | T3-1~4 | ⬜ |
| §5 Evaluation | 四场景实验数据（LLM/Video/Radar/DDP overhead）| 3页 | T2-9 | ⬜ |
| §6 Scaling | **工艺节点放松分析**：NCC液态拓扑如何将先进工艺需求从3nm/5nm降至7nm；三硬约束（单节点算力/SRAM密度/SerDes速率）定量推导；7nm覆盖L1-L3全规模路线图 | 1.5页 | — | ⬜ |
| §7 Open-Source | 代码结构、许可证、社区治理 | 0.5页 | M8 | ⬜ |
| §8 Related+Conc | — | 1页 | — | ⬜ |

---

## 实验数据目标

| 实验 | 目标值 | 对比基准 | 依赖任务 |
|------|--------|---------|---------|
| 1024点复数FFT延迟 | ≤800ns | Xilinx FFT IP (~1.2μs) | T2-9 |
| Gemma-4 E2B INT4推理 | 5.2 tok/s @ ~55W | ARM CPU ~0.3 tok/s | T2-8,9 |
| 场景切换延迟 | ≤1μs | — | T2-9 |
| DDP训练overhead | <5% vs native NCCL on equivalent FPGA | — | T3-2,T2-8 |
| YOLOv8-s 4路720p | 24 FPS | — | T2-8,9 |

---

## 工艺节点放松分析（§6详细内容，2026-04-30）

### 核心命题

> **NCC液态拓扑将先进工艺需求从3nm/5nm降至7nm**，这是NCC相比GPU集群方案最重要的战略价値之一：
> 7nm是国内可量产（中芯国际N+1工艺）的最先进节点，意味着NCC完整技术栈可以在中国大陆自主实现。

### 为什么GPU需要先进工艺？

GPU对先进工艺的需求来自三个驱动力：
1. **HBM堆叠**：要益内存带宽必须3D堆叠和先进工艺（H100: 80GB HBM3, 3.35 TB/s）
2. **计算密度**：单芯片内尽量塔积计算单元，必须3nm提升晋体管密度
3. **通信功耗**：数据在CPU-Memory-NVLink之间反复流动，线缓外录温升

**NCC如何消除这三个需求：**

| GPU驱动力 | NCC修改 | 结果 |
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

### NCC工艺节点分层结论

| 工艺 | 单节点算力 | SRAM | SerDes | 适用规模 | 展右：策略价値 |
|------|---------|------|--------|---------|----------|
| 28nm | 4 TOPS  | 不足 | 56G | L5信号处理 | FPGA验证平台 |
| 12nm | 16 TOPS | 勉强 | 112G | L1边端推理 | 成本敏感场景 |
| **7nm** | **64 TOPS** | **良好** | **224G** | **L1-L3全覆盖** | **★ NCC战略刻制高点** |
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
2027: NCC Gen1 ASIC(7nm, 64节点) → L2量产 [国内自主]
2028: NCC Gen2(7nm优化, 1K节点板卡) → L3
2029+: NCC Gen3(按需升到5nm) → L4
```

**最重要的结论：**
> NCC Gen1和Gen2全部基于7nm，是国内自主可实现的量产节点，
> 视为同等规模GPU集群方案的策略替代路径。

---

## 开源策略

- RTL（SystemVerilog）：CERN-OHL-P v2（硬件开源许可）
- SDK（Python/C++）：Apache 2.0
- 预计开源时间：M8（2029年Q3）或论文发表后6个月
- 仓库结构：`ncc-hw/`（RTL）+ `ncc-sdk/`（Python/C++）+ `ncc-bench/`（benchmark suite）
