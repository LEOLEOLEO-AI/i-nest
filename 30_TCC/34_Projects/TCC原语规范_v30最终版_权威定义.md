---
direction: TCC
title: "TCC原语规范 v30最终版 权威定义"
created: 2026-07-07
modified: 2026-07-07
---
> ⚠️ 已废弃 — 内容已合并至 [[TCC_Knowledge_Base_Baseline_v2.0]]（2026-07-03 全库合并）。

---

---
title: "TCC原语规范_v30.1_权威定义"
date: 2026-07-03
version: v30.1-final
status: Deprecated
source: "TCC_项目实施方案_v30_最终版.docx (2026-07-01 提交版)"
naming: "R=Route / T=Transform / C=Control (2026-07-03 全库统一)"
---

# TCC 原语规范权威定义（v30.1 最终版）

> **权威性声明**：本文直接提取自 TCC_项目实施方案_v30_最终版.docx（2026年7月1日提交至海河实验室的最终版本）的三张原语场景映射表，是該版本的字面转录。
>
> **v30.1 命名修订（2026-07-03）**：全库统一采用 **R=Route / T=Transform / C=Control** 的字母与全称映射，与 Route≅Transform 分解定理对齐。

---

## 一、R.T.C 三类原语总览

| 类别 | 全称 | 数量 | 定义 |
|------|------|:---:|------|
| **R** | Route（路由/拓扑通信原语） | 6 | 定义数据在 MacroTile 之间的集体通信模式 |
| **T** | Transform（变换计算原语） | 6 | 定义 MacroTile 内部执行的数学变换操作 |
| **C** | Control（控制原语） | 4 | 定义拓扑切换、时钟同步、数据搬运的控制行为 |

**总计：16 个原语**

---

## 二、R 类：Route 路由原语（6个）

| 原语 | 语义 | 典型用途 |
|------|------|---------|
| **R.FUSE** | AllReduce（全归约） | 梯度同步(DP)、蝶形归约(FFT/DBF)、部分和归约(TP) |
| **R.PULL** | AllGather（全收集） | 参数分发、KV Cache汇聚、频谱聚合、特征汇聚 |
| **R.CAST** | Broadcast（广播） | 权重广播、输入广播、窗函数广播、模型分发 |
| **R.SWAP** | AlltoAll（全交换） | 转置(FFT)、通道交换(视频)、拓扑重排(多智能体) |
| **R.PIPE** | ReduceScatter（流水归约散射） | 流水段归约(TP)、流水FFT |
| **R.MESH** | Neighbor Exchange（邻域交换） | 邻域聚合(视频)、邻居通信(多智能体) |

---

## 三、T 类：Transform 变换原语（6个）

| 原语 | 语义 | 典型用途 |
|------|------|---------|
| **T.GEMM** | 矩阵乘加 | 梯度计算、QKV投影、CNN卷积、协方差 |
| **T.FOLD** | 向量归约 | Loss归约、Softmax、能量归约(FFT)、RoI Pooling |
| **T.MAPS** | 逐元素映射 | 激活函数、LayerNorm、窗函数、RMS/ReLU |
| **T.SCAN** | 前缀扫描 | 蝶形扫描(FFT)、特征排序、轨迹扫描 |
| **T.LOOK** | 查表/LUT | 量化LUT、KV Cache索引、旋转因子LUT(FFT)、动态LUT |
| **T.SPEC** | 特殊函数 | GELU/SwiGLU、RoPE、CORDIC、Softmax |

---

## 四、C 类：Control 控制原语（4个）

| 原语 | 语义 | 典型用途 |
|------|------|---------|
| **C.LINK** | 拓扑配置与提交 | Butterfly拓扑Commit(DP)、All2All Commit(TP)、Butterfly→Ring切换(FFT) |
| **C.TICK** | 逻辑时钟/因果序 | 梯度版本计数、Token因果序、采样时间戳对齐(FFT) |
| **C.SYNC** | Epoch边界同步 | Epoch边界同步(DP)、Layer边界同步(TP)、处理帧边界同步(FFT) |
| **C.MOVE** | DMA数据搬运 | 梯度→HBM写入、KV Cache搬运、ADC→计算搬运(FFT) |

---

## 五、版本演化路径

\`\`\`
v1 (NPC/CPC/SDI) --- v8 (6R+6T=12) --- v30 (R.T.C=16) --- v30.1 (R.T.C=16, 命名统一)
2026/4/2              2026/6/28            2026/7/1 ★v30★       2026/7/3 ★权威★

v8 R=Route:    FUSE/CAST/SWAP/FLY/RING/MESH
v8 T=Transform: FOLD/SCAN/MAP/MM/LUT/GRAD

v30 R=Transport:   FUSE/PULL/CAST/SWAP/PIPE/MESH  (FLY/RING→PIPE, +PULL)
v30 T=Reduction:   GEMM/FOLD/MAPS/SCAN/LOOK/SPEC  (MM→GEMM, MAP→MAPS, LUT→LOOK, GRAD→SPEC)
v30 C=Control:     LINK/TICK/SYNC/MOVE             (新增)

v30.1 R=Route:      FUSE/PULL/CAST/SWAP/PIPE/MESH  (Transport→Route)
v30.1 T=Transform:  GEMM/FOLD/MAPS/SCAN/LOOK/SPEC  (Reduction→Transform)
v30.1 C=Control:    LINK/TICK/SYNC/MOVE             (不变)
\`\`\`

### 命名修订理由

| 原则 | 说明 |
|------|------|
| **字母-词自然对应** | R↔Route（路由）、T↔Transform（变换），字母与全称语义一致 |
| **Route-Transform 分解定理** | TCC 理论基石：Route（Tile间通信）≅ Transform（Tile内计算），结构同构 |
| **Route 比 Transport 更精确** | 强调路由决策而非简单搬运，体现 SDI 拓扑可编程性 |
| **Transform 比 Reduction 更通用** | 归约只是变换的一种，GEMM/SCAN/LOOK 都是变换操作 |

---

## 六、与专利 TCC-11 (ncc.*) 的对照

| v30.1 | TCC-11 (ncc.*) | 变化说明 |
|------|---------------|---------|
| R.FUSE | ncc.FUSE | 一致 |
| R.PULL | ncc.PULL | v8缺失，v30恢复 |
| R.CAST | ncc.CAST | 一致 |
| R.SWAP | ncc.SWAP | 一致 |
| R.PIPE | — | v30新增（替代v8的FLY/RING） |
| R.MESH | — | v30新增（邻域通信） |
| T.GEMM | ncc.GEMM | 一致（v8称MM） |
| T.FOLD | ncc.FOLD | 一致 |
| T.MAPS | ncc.MAPS | 一致（v8称MAP） |
| T.SCAN | ncc.SCAN | 一致 |
| T.LOOK | — | v30新增（v8称LUT） |
| T.SPEC | — | v30新增（替代v8的GRAD） |
| C.LINK | ncc.LINK | 一致 |
| C.TICK | ncc.TICK | 一致 |
| C.SYNC | — | v30新增 |
| C.MOVE | ncc.MOVE | 一致 |

---

## 七、修订记录

| 版本 | 日期 | 修订内容 |
|------|------|---------|
| v30 | 2026-07-01 | 海河实验室提交版，16原语定型（R=Transport, T=Reduction） |
| v1.1 | 2026-07-03 | 首次采纳 R=Route / T=Transform 命名（独立子项生成） |
| v30.1 | 2026-07-03 | 全库统一：R=Route / T=Transform / C=Control，与 v1.1 对齐 |

---

## Related Notes

- [[TCC计算范式_从智能算力中心到新一代计算平台的工程落地与生态构建战略规划_v2.0_完整版]] — 顶层战略规划
- [[待办_原语体系数学统一证明]] — 原语数学证明待办
- [[算力网络架构手记_全面抓取与分析报告_v3.0]] — 产业工程痛点→TCC原语映射
- [[路由即变换——分布式系统中通信与计算的结构同构性]] — Route≅Transform 理论基础
- [[一种基于正交原语集与拓扑融合变换的网络复杂度计算方法及系统]] — TCC-11 专利
- [[TCC原语规范_v1.1_权威定义]] — v1.1 首次 R=Route/T=Transform 版本
- [[TCC_Knowledge_Base_Baseline_v1.1]] — TCC 知识库基线
- [[TCC计算范式命名规范3.0]] — 命名规范
- [[TCC原语体系统一方案_v1.0_已归档]] — 已归档的 v1.0（基于 v8.0）
