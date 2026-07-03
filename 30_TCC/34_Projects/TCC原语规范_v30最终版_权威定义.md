---
title: "TCC原语规范_v30最终版_权威定义"
date: 2026-07-02
version: v30-final
status: Authoritative
source: "TCC_项目实施方案_v30_最终版.docx (2026-07-01 提交版)"
---

# TCC 原语规范权威定义（v30 最终版）

> **权威性声明**：本文直接提取自 TCC_项目实施方案_v30_最终版.docx（2026年7月1日提交至海河实验室的最终版本）的三张原语场景映射表，是该版本的**字面转录**。此前知识库中的 v8.0（GetNotes）版本已被本版本取代。

---

## 一、T.R.C 三类原语总览

| 类别 | 全称 | 数量 | 定义 |
|------|------|:---:|------|
| **T** | Transport（传输/拓扑通信原语） | 6 | 定义数据在 MacroTile 之间的集体通信模式 |
| **R** | Reduction（归约/变换计算原语） | 6 | 定义 MacroTile 内部执行的数学变换操作 |
| **C** | Control（控制原语） | 4 | 定义拓扑切换、时钟同步、数据搬运的控制行为 |

---

## 二、T 类：Transport 传输原语（6个）

| 原语 | 语义 | 典型用途 |
|------|------|---------|
| **T.FUSE** | AllReduce（全归约） | 梯度同步(DP)、蝶形归约(FFT/DBF)、部分和归约(TP) |
| **T.PULL** | AllGather（全收集） | 参数分发、KV Cache汇聚、频谱聚合、特征汇聚 |
| **T.CAST** | Broadcast（广播） | 权重广播、输入广播、窗函数广播、模型分发 |
| **T.SWAP** | AlltoAll（全交换） | 转置(FFT)、通道交换(视频)、拓扑重排(多智能体) |
| **T.PIPE** | ReduceScatter（流水归约散射） | 流水段归约(TP)、流水FFT |
| **T.MESH** | Neighbor Exchange（邻域交换） | 邻域聚合(视频)、邻居通信(多智能体) |

---

## 三、R 类：Reduction 归约计算原语（6个）

| 原语 | 语义 | 典型用途 |
|------|------|---------|
| **R.GEMM** | 矩阵乘加 | 梯度计算、QKV投影、CNN卷积、协方差 |
| **R.FOLD** | 向量归约 | Loss归约、Softmax、能量归约(FFT)、RoI Pooling |
| **R.MAPS** | 逐元素映射 | 激活函数、LayerNorm、窗函数、NMS/ReLU |
| **R.SCAN** | 前缀扫描 | 蝶形扫描(FFT)、特征排序、轨迹扫描 |
| **R.LOOK** | 查表/LUT | 量化LUT、KV Cache索引、旋转因子LUT(FFT)、动作LUT |
| **R.SPEC** | 特殊函数 | GELU/SwiGLU、RoPE、CORDIC、Softmax |

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

`
v1 (NPC/CPC/SDI) ──→ v8 (6R+6T=12) ──→ v30 (T.R.C=16)
2026/4/2              2026/6/28            2026/7/1 ★权威★

v8 R=Route:    FUSE/CAST/SWAP/FLY/RING/MESH
v8 T=Transform: FOLD/SCAN/MAP/MM/LUT/GRAD

v30 T=Transport: FUSE/PULL/CAST/SWAP/PIPE/MESH  (FLY/RING→PIPE, +PULL)
v30 R=Reduction: GEMM/FOLD/MAPS/SCAN/LOOK/SPEC  (MM→GEMM, MAP→MAPS, LUT→LOOK, GRAD→SPEC)
v30 C=Control:   LINK/TICK/SYNC/MOVE             (新增)
`

---

## 六、与专利 TCC-11 (ncc.*) 的对照

| v30 | TCC-11 (ncc.*) | 变化说明 |
|-----|---------------|---------|
| T.FUSE | ncc.FUSE | 一致 |
| T.PULL | ncc.PULL | v8缺失，v30恢复 |
| T.CAST | ncc.CAST | 一致 |
| T.SWAP | ncc.SWAP | 一致 |
| T.PIPE | — | v30新增（替代v8的FLY/RING） |
| T.MESH | — | v30新增（邻域通信） |
| R.GEMM | ncc.GEMM | 一致（v8称MM） |
| R.FOLD | ncc.FOLD | 一致 |
| R.MAPS | ncc.MAPS | 一致（v8称MAP） |
| R.SCAN | ncc.SCAN | 一致 |
| R.LOOK | — | v30新增（v8称LUT） |
| R.SPEC | — | v30新增（替代v8的GRAD） |
| C.LINK | ncc.LINK | 一致 |
| C.TICK | ncc.TICK | 一致 |
| C.SYNC | — | v30新增 |
| C.MOVE | ncc.MOVE | 一致 |
---

## Related Notes

- [[TCC计算范式_从智能算力中心到新一代计算平台的工程落地与生态构建战略规划_v2.0_完整版]] — 顶层战略规划
- [[待办_原语体系数学统一证明]] — 原语数学证明待办
- [[算力网络架构手记_全面抓取与分析报告_v3.0]] — 产业工程痛点→TCC原语映射
- [[路由即变换——分布式系统中通信与计算的结构同构性]] — Route≡Transform 理论基础
- [[一种基于正交原语集与拓扑融合变换的网络复杂度计算方法及系统]] — TCC-11 专利
- [[TCC原语体系统一方案_v1.0_已归档]] — 已归档的 v1.0 统一方案（基于 GetNotes v8.0）
- [[iNEST_Research_Agent_System_Prompt]] — iNEST 系统提示中的 TCC-11 快速参考