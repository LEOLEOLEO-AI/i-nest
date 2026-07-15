---
direction: TCC
title: "TCC原语规范 v1.1 权威定义"
created: 2026-07-07
modified: 2026-07-07
---
> ⚠️ 已废弃 — 内容已合并至 [[TCC_Knowledge_Base_Baseline_v2.0]]（2026-07-03 全库合并）。

---

---
title: "TCC原语规范_v1.1_权威定义"
date: 2026-07-03
version: v1.1
status: Deprecated
source: "TCC_项目实施方案_v30_最终版.docx (2026-07-01 提交版) + v1.1 命名修订"
supersedes: "TCC原语规范_v30最终版_权威定义 (v30 Transport/Reduction 旧命名)"
---

# TCC 原语规范权威定义（v1.1）

> **v1.1 里程碑**（2026-07-03）：本版本首次采纳 **R=Route / T=Transform** 的字母-词自然映射方案。v30.1 已与此对齐，全库统一。
> 
> 详细规范请参阅权威版本：[[TCC原语规范_v30最终版_权威定义]]（v30.1，内容更完整）

> **权威性声明**：本文基于 v30 最终版（2026年7月1日提交至海河实验室）的三张原语场景映射表，并进行了 v1.1 命名修订。v30 版本已被本版本取代。
>
> **v1.1 核心修订**：将原语命名从 Transport/Reduction/Control 统一修订为 **Route/Transform/Control**，字母约定从 T/R/C 改为 **R/T/C**，以匹配 Route-Transform 分解定理的语义框架。

---

## 一、R.T.C 三类原语总览

| 类别 | 全称 | 数量 | 定义 |
|------|------|:---:|------|
| **R** | Route（路由/拓扑通信原语） | 6 | 定义数据在 MacroTile 之间的集体通信模式 |
| **T** | Transform（变换计算原语） | 6 | 定义 MacroTile 内部执行的数学变换操作 |
| **C** | Control（控制原语） | 4 | 定义拓扑切换、时钟同步、数据搬运的控制行为 |

**总计: 16 个原语**

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
| **T.MAPS** | 逐元素映射 | 激活函数、LayerNorm、窗函数、NMS/ReLU |
| **T.SCAN** | 前缀扫描 | 蝶形扫描(FFT)、特征排序、轨迹扫描 |
| **T.LOOK** | 查表/LUT | 量化LUT、KV Cache索引、旋转因子LUT(FFT)、动作LUT |
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

```
v1 (NPC/CPC/SDI) —— v8 (6R+6T=12) —— v30 (T.R.C=16) —— v1.1 (R.T.C=16)
2026/4/2              2026/6/28            2026/7/1 ★v30★        2026/7/3 ★权威★

v8 R=Route:    FUSE/CAST/SWAP/FLY/RING/MESH
v8 T=Transform: FOLD/SCAN/MAP/MM/LUT/GRAD

v30 T=Transport: FUSE/PULL/CAST/SWAP/PIPE/MESH  (FLY/RING→PIPE, +PULL)
v30 R=Reduction: GEMM/FOLD/MAPS/SCAN/LOOK/SPEC  (MM→GEMM, MAP→MAPS, LUT→LOOK, GRAD→SPEC)
v30 C=Control:   LINK/TICK/SYNC/MOVE             (新增)

v1.1 R=Route:     FUSE/PULL/CAST/SWAP/PIPE/MESH  (语义同v30 T类，名称回归v8 Route)
v1.1 T=Transform: GEMM/FOLD/MAPS/SCAN/LOOK/SPEC  (语义同v30 R类，名称回归v8 Transform)
v1.1 C=Control:   LINK/TICK/SYNC/MOVE             (不变)
```

### 命名修订理由

Route-Transform 分解定理是 TCC 理论基石：
- **Route**（路由）= 数据在 Tile 间的集体通信模式 —— 比 "Transport" 更精确，强调路由决策而非简单搬运
- **Transform**（变换）= Tile 内部的数学变换操作 —— 比 "Reduction" 更通用，归约只是变换的一种
- Route ≡ Transform 是 TCC 对分布式系统中通信与计算结构同构性的核心洞察

---

## 六、与专利 TCC-11 (tcc.*) 的对照

| v1.1 | TCC-11 (tcc.*) | 变化说明 |
|------|---------------|---------|
| R.FUSE | tcc.FUSE | 一致 |
| R.PULL | tcc.PULL | v8缺失，v30恢复 |
| R.CAST | tcc.CAST | 一致 |
| R.SWAP | tcc.SWAP | 一致 |
| R.PIPE | — | v30新增（替代v8的FLY/RING） |
| R.MESH | — | v30新增（邻域通信） |
| T.GEMM | tcc.GEMM | 一致（v8称MM） |
| T.FOLD | tcc.FOLD | 一致 |
| T.MAPS | tcc.MAPS | 一致（v8称MAP） |
| T.SCAN | tcc.SCAN | 一致 |
| T.LOOK | — | v30新增（v8称LUT） |
| T.SPEC | — | v30新增（替代v8的GRAD） |
| C.LINK | tcc.LINK | 一致 |
| C.TICK | tcc.TICK | 一致 |
| C.SYNC | — | v30新增 |
| C.MOVE | tcc.MOVE | 一致 |

---

## 七、修订记录

| 版本 | 日期 | 修订内容 |
|------|------|---------|
| v30 | 2026-07-01 | 海河实验室提交版，16原语定型 |
| v1.1 | 2026-07-03 | 命名修订：Transport→Route、Reduction→Transform；字母映射 R→Route、T→Transform |

---

## Related Notes

- [[TCC_Knowledge_Base_Baseline_v1.1]] — TCC 知识库基线（权威）
- [[07_核心定义_超非线性增益与智能视角]] — 超非线性增益理论
- [[路由即变换——分布式系统中通信与计算的结构同构性]] — Route≡Transform 理论基础
- [[一种基于正交原语集与拓扑融合变换的网络复杂度计算方法及系统]] — TCC-11 专利
