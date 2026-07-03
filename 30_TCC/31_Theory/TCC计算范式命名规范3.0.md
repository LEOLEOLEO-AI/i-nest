---
title: "TCC Naming Convention v3.0"
created: 2026-06-30
aliases: ["TCC命名约定v3", "Primitive Naming v3", "原语命名规范"]
tags: ["ssot", "naming-convention", "TCC", "primitives"]
supersedes: ["NCC_Core_Concepts", "TCC 原语库 v1.0 最终版规范"]
status: authoritative
---

# TCC Naming Convention v3.0 — 统一原语命名体系

## 零、版本沿革与统一动机

### 历史版本

| 版本 | 时期 | 范式名 | 前缀体系 | 原语数 | 问题 |
|------|------|--------|----------|--------|------|
| v0 (非正式) | 2025 | TCC | NPC-/CPC- | 5+4=9 | NPC与CPC前缀冗长，与NCCL混淆 |
| v1.0 (TCC原语库) | 2026.04 | TCC | tcc.VERB | 4+4+1+2=11 | 单层前缀，缺少类别区分 |
| v1.x (项目申报) | 2026.06 | TCC | NPC-/CPC- | 6+6=12 | 沿袭v0前缀，与v1.0动词名脱节 |
| **v3.0 (本规范)** | **2026.06** | **TCC** | **T./R./C.** | **6+6+4=16** | **三层前缀，动词名统一，全体系覆盖** |

> **注**：v2 编号保留给内部草稿 `NCC_Naming_Convention_v2`（存在于得到笔记中，未正式发布）。v3.0 继承 v1.0 的动词命名哲学和 v1.x 的 6R+6T 覆盖宽度，引入 T.R.C 三层前缀体系。

### 统一原则

1. **TCC → TCC**：范式名统一为 Topology-Centric Computing，弃用 Network-Centric Computing（TCC 易与 NVIDIA NCCL 混淆）
2. **NPC → T**：网络通信原语前缀改为 `T.`（Topology），强调"拓扑即计算"
3. **CPC → R**：计算原语前缀改为 `R.`（Reduction），源自 Route-Reduce 分解定理
4. **新增 C.**：控制与系统原语前缀 `C.`（Control），覆盖配置/时钟/同步/DMA
5. **动词名继承 v1.0**：保留四字母英语动词（FUSE/PULL/CAST/SWAP/GEMM/FOLD/MAPS/SCAN/LOOK/SPEC/PIPE/MESH/LINK/TICK/SYNC/MOVE），全部可发音

---

## 一、前缀体系：T.R.C

```
TCC Primitive = <Prefix>.<VERB>

Prefix in { T, R, C }
VERB   = 4-letter English verb, pronounceable, all caps
```

| 前缀 | 全称 | 语义域 | 覆盖旧前缀 | 原语数 |
|------|------|--------|-----------|--------|
| `T.` | **T**opology | 路由/通信/网络拓扑操作 | NPC-*, tcc.{FUSE,PULL,CAST,SWAP} | 6 |
| `R.` | **R**eduction | 计算/变换/节点内代数操作 | CPC-*, tcc.{GEMM,FOLD,MAPS,SCAN} | 6 |
| `C.` | **C**ontrol | 系统控制/配置/时序/DMA | tcc.{LINK,TICK,MOVE}, (new)SYNC | 4 |

**助记**：T = 数据在路上 (on the wire)，R = 数据在节点 (in the node)，C = 系统在掌舵 (at the helm)

---

## 二、原语总表：TCC-16

### 2.1 T.* — Topology Primitives（路由原语，6个）

| # | 原语名 | 发音 | 旧 NPC | 旧 tcc.* | 语义 | 最优拓扑 |
|---|--------|------|--------|----------|------|----------|
| T1 | `T.FUSE` | /fju:z/ | NPC-AR | tcc.FUSE | AllReduce：多节点归约广播 | Butterfly |
| T2 | `T.PULL` | /pul/ | NPC-AG | tcc.PULL | AllGather：全节点数据拼接 | Radial Tree |
| T3 | `T.CAST` | /kaest/ | NPC-BC | tcc.CAST | Broadcast：单源全节点复制 | Sparse Tree |
| T4 | `T.SWAP` | /swop/ | NPC-A2A | tcc.SWAP | AlltoAll：全节点两两交换 | Full Crossbar |
| T5 | `T.PIPE` | /paip/ | NPC-RS | — | ReduceScatter：分段流水归约 | Ring Pipeline |
| T6 | `T.MESH` | /mesh/ | NPC-MESH | — | Neighbor Exchange：邻居通信 | 2D Mesh |

### 2.2 R.* — Reduction Primitives（变换原语，6个）

| # | 原语名 | 发音 | 旧 CPC | 旧 tcc.* | 语义 | 物理实现 |
|---|--------|------|--------|----------|------|----------|
| R1 | `R.GEMM` | /djem/ | CPC-MAC | tcc.GEMM | 矩阵乘加 C=aAB+bC | Systolic Array |
| R2 | `R.FOLD` | /fold/ | CPC-RED | tcc.FOLD | 向量归约 y=Reduce(x,op) | Adder Tree |
| R3 | `R.MAPS` | /maeps/ | CPC-EW | tcc.MAPS | 逐元素映射 y=f(x) | SIMD Lane |
| R4 | `R.SCAN` | /skaen/ | CPC-SHIFT | tcc.SCAN | 前缀扫描/蝶形FFT | Parallel Prefix |
| R5 | `R.LOOK` | /luk/ | CPC-LUT | — | 查表/非线性变换 | BRAM LUT |
| R6 | `R.SPEC` | /spek/ | CPC-SPEC | — | 特殊函数逼近 (exp/GELU) | CORDIC/分段 |

### 2.3 C.* — Control Primitives（控制原语，4个）

| # | 原语名 | 发音 | 旧来源 | 语义 | 硬件成本 |
|---|--------|------|--------|------|----------|
| C1 | `C.LINK` | /link/ | tcc.LINK | SDI拓扑配置/Page Commit/Barrier | ~2K LUT |
| C2 | `C.TICK` | /tik/ | tcc.TICK | 全局分布式逻辑时钟/因果序 | <500 LUT |
| C3 | `C.SYNC` | /sink/ | (新增) | Epoch边界同步/排空检测/Commit | ~1K LUT |
| C4 | `C.MOVE` | /mu:v/ | tcc.MOVE | DMA数据搬运/地址重映射 | ~3K LUT |

---

## 三、旧名->新名迁移表（完整对照）

```
TCC v3.0 MIGRATION MAP

v3.0      v1.0       v0/v1.x    语义
T.R.C     tcc.VERB   NPC/CPC
------    --------   -------    ----
T.FUSE    tcc.FUSE   NPC-AR     AllReduce
T.PULL    tcc.PULL   NPC-AG     AllGather
T.CAST    tcc.CAST   NPC-BC     Broadcast
T.SWAP    tcc.SWAP   NPC-A2A    AlltoAll
T.PIPE    —          NPC-RS     ReduceScatter
T.MESH    —          NPC-MESH   Neighbor Exchange
R.GEMM    tcc.GEMM   CPC-MAC    Matrix Multiply-Accumulate
R.FOLD    tcc.FOLD   CPC-RED    Vector Reduction
R.MAPS    tcc.MAPS   CPC-EW     Element-wise Map
R.SCAN    tcc.SCAN   CPC-SHIFT  Prefix Scan / FFT Butterfly
R.LOOK    —          CPC-LUT    Lookup / Nonlinear
R.SPEC    —          CPC-SPEC   Special Function Approx
C.LINK    tcc.LINK   —          SDI Topology Config
C.TICK    tcc.TICK   —          Global Logical Clock
C.SYNC    —          —          Epoch Barrier / Sync
C.MOVE    tcc.MOVE   —          DMA / Data Movement
```

---

## 四、正交性与完备性验证

### 4.1 正交最小性

T.R.C 三层前缀天然正交：任意 T.* 原语仅操作网络数据流，任意 R.* 原语仅操作节点内数据，任意 C.* 原语仅操作系统状态。不存在跨层等价替代。

### 4.2 代数完备性

- **T.* (6个)**：{FUSE, PULL, CAST, SWAP, PIPE, MESH} 构成分布式路由完备基
- **R.* (6个)**：{GEMM, FOLD, MAPS, SCAN, LOOK, SPEC} 构成节点内图灵完备计算
- **C.* (4个)**：{LINK, TICK, SYNC, MOVE} 覆盖运行时控制全生命周期

---

## 五、使用规范

### 5.1 代码引用

```
// RTL 模块命名
module t_topology_fuse (...)   // T.FUSE RTL IP
module t_reduce_gemm (...)     // R.GEMM RTL IP
module t_control_link (...)    // C.LINK RTL IP

// API 调用
tcc.t.fuse(data, op=SUM);
tcc.r.gemm(a, b, c);
tcc.c.link.config(butterfly);
```

### 5.2 文档与论文引用

项目实施方案中 "6R+6T" 迁移映射：
- "6R" (Route primitives) -> T.{FUSE|PULL|CAST|SWAP|PIPE|MESH}
- "6T" (Transform primitives) -> R.{GEMM|FOLD|MAPS|SCAN|LOOK|SPEC}

论文中使用完整拼写：`T.FUSE: Topology Fuse (AllReduce) primitive`

---

## 六、生效与维护

- **生效日期**：2026-06-30
- **适用范围**：TCC/TCC 方向全部文档、代码、论文、专利、项目申报
- **废弃标记**：NPC-/CPC- 前缀标记为 @deprecated
- **下次评审**：2026-12-30

---
**关联条目**：[[NCC_Core_Concepts]] | [[TCC 原语库 v1.0 最终版规范]] | [[元拓扑+化合键=六类通信原语]]
