---
title: "TCC核心原理与架构映射（PPT）"
direction: TCC
source: "Genspark"
date: 2026-07-12
tags: [tcc, first-principles, genspark-import]
provenance: external
---

# TCC核心原理与架构映射（PPT）

> 来源: Genspark 创新引擎 | 方向: TCC | 导入日期: 2026-07-12

---

## Slide 1

TOPOLOGY-CENTRIC COMPUTING

TCC 拓扑中心计算范式

核心原理与架构映射

· 从节点中心到拓扑中心的范式迁移

· R/T/C 原语系统与 Page Commit 机制

· 典型业务到 TCC 架构的端到端映射

组会讲解 · 面向博士生与导师组

v2.0 · 审稿友好版

基于 TCC 知识库基线 v2.0



## Slide 2

01 · 研究问题

为什么"拓扑成为了关键变量"?

通信受限计算已让"连接结构"挤进体系结构主语的位置

核心判断

在通信受限计算中,拓扑的运行时选择与切换会直接影响系统性能、能效与可扩展性。

—— TCC 知识库基线 v2.0

三类现实证据

证据 1 · 通信瓶颈

并行策略 + CCL + 网络

三层范式相互制约,跨层协同空间巨大。

证据 2 · 可重构

TPU v4 · OCS · RADICAL

运行时切换互连拓扑已是工业现实。

证据 3 · 流量结构

demand-oblivious 已过时

真实训练与推理具有显著的阶段性、突发性与局部性。

TCC 研究问题

如何把"拓扑选择与切换"

从背景条件提升为体系结构主轴?

不是又一个算子库,而是把"谁和谁怎么连、何时切换"作为运行时一等对象。

来源:TCC综述底稿 Ch.1;TCC知识库基线 v2.0;[E] Distributed Training Comm. Survey;[G] CACM 可重构拓扑

01 / 18



## Slide 3

02 · 范式迁移

从"节点中心"到"拓扑中心"——五维对比

优化对象从节点上移到连接,任务适配从"硬件容纳任务"转为"底座随阶段切换"。

→

范式转移

01

节点中心范式

02

拓扑中心范式 (TCC)

一句结论

从"节点更强"转向"连接更合适"。

来源:TCC综述底稿 Ch.2.1;TCC知识库基线 v2.0

02 / 18



## Slide 4

03 · TCC 总体框架

TCC 总览:三层原语 + 双底座 + 一组提交机制

材料支持 · 图示 = 总览原图(经裁切重排)

图说

R 决定连接骨架

T 决定计算形态

C 决定状态时序

· 任意任务 = 一个或多个 Page Split(路由子图)

· Page Commit 控制提交时点

· 训 / 推 / FFT / DBF 在底座上复用同一抽象

一句结论

拓扑不是"网络参数",而是 TCC 的体系结构对象。

来源:TCC 总览原图(组图 A);TCC 原语规范 v1.1 ;TCC 知识库基线 v2.0

03 / 18



## Slide 5

04 · R.T.C 三层原语

一套原语,把"通信—计算—控制"做成统一抽象

R 答"如何连接",T 答"如何变换",C 答"如何控序"。三者职责互不重叠。

R

Route 路由原语

决定"谁和谁怎么连"

· 通过 SDI 平面组织乒乓型连接

· Crossbar N×N + V 处 VC 仲裁

· 拓扑以 Page 暴露给上层

含:R.FUSE · R.PULL · R.CAST · R.SWAP · R.PIPE · R.MESH(6 项)

T

Transform 变换原语

决定"数据如何被改写"

· 由 SYN 矩阵调度的一组计算

· GEMM / FOLD / MAPS / SCAN / LOO

· K · LOOK / SPEC 等专用计算

含:T.GEMM · T.FOLD · T.MAPS · T.SCAN · T.LOOK · T.SPEC(6 项)

C

Control 控制原语

决定"提交与时序"

· C.LINK 提交 Page 向 SDI

· C.TICK 系统节拍 ~500 LUT

· C.SYNC / C.MOVE 阶段同步与搬数

含:C.LINK · C.TICK · C.SYNC · C.MOVE(4 项)

来源:TCC 原语规范 v1.1(权威定义,3 项主类 / 16 子项);TCC 知识库基线 v2.0

04 / 18



## Slide 6

05 · Tile 微架构

Tile = SDI + SYN + CTRL 三段拼装

SDI 提供外部连接,T 通过 SYN 矩阵展开计算,CTRL 提交 + 节拍。

三段分工

SDI · 交换段

Crossbar N×N + 8 个 VC,

承担外部连接的组织与仲裁。

~2K LUT

SYN · 计算段

6 向量 × 6 矩阵,

调度 GEMM / FOLD / MAPS 等 T.*;

~5K LUT

CTRL · 控制段

C.LINK 提交 Page 向 SDI;

C.TICK 节拍 ~500 LUT 控制全局时序。

来源:TCC 原语规范 v1.1 Ch.1.1;组图 B

05 / 18



## Slide 7

06 · R 路由原语项

R 决定"以何种结构让节点相遇"

共 6 项 · 每项对应一种典型通信骨架。

统一定位

6 项 R 原语 = 6 套典型通信骨架, 而非"6 个并列算子"。

来源:TCC 原语规范 v1.1 Ch.1.3.1

06 / 18



## Slide 8

07 · T 变换原语项

T 决定"以何种方式让数据被改写"

共 6 项 · 由 SYN 矩阵调度,执行典型算子 / 专用变换。

T.GEMM

/djem/ → 矩阵乘

CNN 推理权重、Butterfly 折叠、CNN 训练正向。

~50K LUT · Systolic Array

T.FOLD

/fold/ → 归约折叠

Softmax、Row Pooling、Aggregator。

~5K LUT · Adder Tree

T.MAPS

/mæps/ → 点级映射

ReLU / GeLU、LayerNorm、Activation。

~10K LUT · SIMD Lanés

T.SCAN

/skæn/ → 前缀/扫描

Prefix Sum、区间查询、因果注意力前置。

~15K LUT · Parallel Prefix

T.LOOK

/lʊk/ → 查表/LUT

BRAM LUT、注意力打分核、近邻编码。

~5K LUT + BRAM

T.SPEC

/spek/ → 专用算子

GeLU/Softmax、稀疏算子、雷达/通信专用核。

~8K LUT · custom engine

设计取向

T 抽象统一覆盖 ML 算子与雷达 / 通信专用核,因此 同一底座 可承载训练 / 推理 / 信号处理。

来源:TCC 原语规范 v1.1 Ch.1.3.2

07 / 18



## Slide 9

08 · C 控制原语项

C 决定"何时提交 + 何时同步"

共 4 项 · 承担 Page 提交、节拍、同步与搬数。

C 的核心地位

在固定硬件中,

C 是唯一允许"切换拓扑"的层级。

· R 描写"想用哪一种连接"

· T 描写"哪种数据被变换"

· C 决定"这套组合在何时生效"

一句结论

没有 C,则 R/T 只是静态描述;有 C,R/T 才成为可运行的架构对象。

来源:TCC 原语规范 v1.1 Ch.1.3.3

08 / 18



## Slide 10

09 · SDI vs 传统交换机

SDI ≠ "更快一些的交换芯片"

结论:SDI 是 Page Runtime,且与 ctrl 紧耦合;传统交换机是包转发。

三维对比

含义

路由器换了 CPU 仍是 CPU

SDI 取代了 CPU 体系结构对象

一句话:SDI 是 以 Page 为粒度的运行时重配平面,传统交换机是包转发。

来源:TCC 原语规范 v1.1 Ch.2.1;组图 E

09 / 18



## Slide 11

10 · Page Commit 运行时切换

Page Commit = 把 Page 一次性挂到 SDI 的提交动作

目标量级:~10 ms 全规模切换 · 当前材料给出拆分思路,实测验证待后续工作。

提交流程 · 5 步

步骤 1

Token 准备

按当前 Task/DP

Phase 状态生成

R-Tokens 列表

步骤 2

Page 计算

ctrl 局部计算

Crossbar 配置表,

写 VC 仲裁策略

步骤 3

CMEM 装配

Page 整体写入

CMEM,作为提交

对象的"封面"

步骤 4

原子提交

ctrl 单条指令

提交 Page 到 SDI,

旧拓扑在边界退出

步骤 5

Stage 同步

C.SYNC 收敛,

新拓扑生效,数据

沿新路径继续流动

Token → Page → CMEM → SDI · 单条 C.LINK 提交

两个观察角度

架构师视角

Page Commit 是 TCC 的"系统调用":

把"我要用什么结构连接"以单条指令一次性提交给 SDI。

编译器视角

Page 切换 = 边带信号(side-tag):

切换不重做计算,也不打断数据路径,只切换"路径形状"。

来源:TCC 原语规范 v1.1 Ch.2;[E] Distributed Training Comm.;[G] CACM 可重构拓扑

10 / 18



## Slide 12

11 · 业务项映射

一个业务项如何映射到 TCC 架构

示例:FFT-1k → 8×8 Tile 阵列 + Crossbar + BRAM LUT

映射要点

FFT-1k + 8 阵元 DBF 主成分

8×8 Tile · Crossbar 64×64

LUT < 45% · BRAM < 66%

能力含义

训推 + 雷达信号

同底座同阶段切换

业务规模

硬件规模

资源消耗

结论:一业务项 = 一组 Page 列表 = 在同一硬件底座上按时序切换。

来源:TCC 原语规范 v1.1 Ch.3 + 实测材料;组图 C

11 / 18



## Slide 13

12 · 工作模式

四类工作模式 · 同一底座的不同 Page 组合

纯推理 · 纯训练 · 训推一体 · FFT/DBF 雷达,在 TCC 底座上按时序切换。

模式 1 · Pure Inference

纯推理模式

· Page:前端 GEMM → 中端 SPEC → 后端 SPEC

· κ(推理算力比)较低, σ(通信占比)较高

· KV Cache 仅本地,Page Commit 频率 ~几秒/次

模式 2 · Pure Train

纯训练模式

· Page:前向 GEMM → 反向 SPEC → 0.5~GC FUSE

· κ 高, σ 高, Tratio(切换开销)对总耗时影响显著

· Page Commit 频率约 ~秒级

模式 3 · Train-Inference Coupled

训推一体模式

· Page:训练 T + R 链路 / 推理 T + R 链路 交错

· C.MOVE 接力,DRAM ↔ BRAM KV 共享

· Page Commit 频率 ~百毫秒/次,收益最高

模式 4 · FFT / DBF Radar

FFT / DBF 雷达信号模式

· Page:蝶形 SCAN → 1D FFT → 2D FFT → DBF PULL

· FFT 蝶形图 ≈ AllReduce,在 TCC 中结构对应

· Page Commit 频率 ~毫秒/次

统一定位

四类模式 = 四套 Page 列表 · 同一底座不同拓扑 — 这是 TCC 复用底层硬件的根本来源。

来源:TCC 原语规范 v1.1 Ch.3

12 / 18



## Slide 14

13 · 模式切换时序

模式在底座上"按时序切换",而不是在多个底座间来回

目标:Page Commit ~10ms 实测验证待后续工作 · 当前以"切换思路 + 时序拆分"作为材料支撑。

三段结构性意义

① 切换不重做计算

当前 GEMM / FOLD 结果保持,只是改路径形状。

② 切换不打断数据流

边界退出 / 边界进入,旧 Page 退场与新 Page 进场部分重叠。

③ 切换是边带信号

Page Commit 不进入数据路径,只把"拓扑形状"挂上 SDI。

来源:TCC 原语规范 v1.1 Ch.2;组图 D

13 / 18



## Slide 15

14 · 相关工作对比

TCC 与现有路线的关系:既不是替代,也不是简单叠加

四条主线 + TCC:固定高带宽 / 可重构互连 / 拓扑感知集合通信 / 晶圆级统一底座

TCC 在谱系中的潜在增量

不否认固定高带宽 / 晶圆级 / 算法综合路线的价值,而是把"拓扑切换"从背景条件提升为运行时一等对象,并以 R/T/C 原语 + Page Commit 给出统一抽象。

来源:[A] Cloud TPU Docs;[B] TPU v4;[C] NVLink;[D] WSE-3;[F] TACOS;[G] CACM;[H] RADICAL

14 / 18



## Slide 16

15 · 证据状态

哪些已经能被材料支持,哪些尚待证明

组会层面 + 论文层面,均应避免把"目标"与"已证明"混为一谈。

当前材料可得

Already Supported

· 通信开销与拓扑强耦合

· 运行时可重构互连已是工业现实

· 拓扑感知集合通信已是研究方向

· fft 蝶形 ≈ AllReduce 通信图(结构对应)

· 业务项映射消耗 (LUT 45% / BRAM 66%)

写作建议

可直接进入论文引言 / 相关工作。

尚待证明

Not Yet Proven

· Route-Transform 分解的形式化闭包

· FFT 蝶形与 AllReduce 的同构证明

· TCC 对 workloads 的可形式化收益界

· 多级 SDI / Crossbar 扩展的代价

写作建议

用"结构对应 / 当前材料支持"等克制表述,避免写成既成事实。

建议后续验证

To Be Verified

· Page Commit 的 ~10ms 目标量级实测

· 训推一体 κ / σ / Tratio 指标闭环

· Crossbar 64×64 / 128×128 扩展代价

· ON-CHIP 网络与 off-chip 协同机制

写作建议

列入"未来工作 / 仿真 + 板级 MVP 路径"部分,避免与"已实现"混淆。

写作原则:三类证据状态保持清晰分层,审稿友好 · 不要把目标量级写成"已实现"。

来源:TCC综述底稿 Ch.2.5;Ch.4

15 / 18



## Slide 17

16 · 论文与实验启发

首篇 TCC 论文可由四类引理起步

克制起步 · 不强求全闭环 · 后续论文逐步补齐理论剩余。

引理 1 · 拓扑与性能耦合

在固定计算节点条件下,通信路径的选择差异将带来显著性能差距。

引理 2 · R/T/C 分解存在

任意一段典型计算 → 可拆为 R → T → C 一组原语序列。(存在性证据充分)

引理 3 · Page Commit 边界可积分

模式切换可在 stage 边界进行,旧 Page 沿边界退场 · 实测待板级 MVP 闭环。

引理 4 · 跨域复用存在

FFT 蝶形图 ≈ AllReduce → TCC 中结构对应 → 训推与雷达复用同一底座。

后续实验路线

1.仿真优先 · 在 simulator 上量化 Page Commit 时延与 κ / σ 收益,先建立"目标量级"的边界证据。

2.板级 MVP · 选 FFT / DBF 一个最小业务,实现 8×8 Tile + Crossbar + CTRL,验证"硬件层 Page"。 (M2)

3.理论剩余 · Route-Transform 分解的完整形式化 + FFT/AllReduce 同构证明,由后续论文逐步封闭。 (M3)

4.路线对比 · 与 NVLink / WSE-3 / OCS 在统一指标 (κ · σ · Tratio) 上做闭环对比。 (M4)

来源:TCC 综述底稿 Ch.5;Ch.6 审稿友好表述

16 / 18



## Slide 18

SUMMARY · 总结

TCC 把"拓扑"从背景条件提升为体系结构主轴

▍ R.T.C 原语 让通信—计算—控制被一组统一抽象组织。

▍ Page Commit 让运行时拓扑切换成为单条系统调用。

▍ 业务映射 让训推与信号处理在同一底座上按时序切换。

当前边界

· 范式层与工程层 已有充分的公开材料支撑;

· Route-Transform 分解的形式化闭包尚待证明;

· Page Commit ~10 ms 目标量级与训推一体化收益尚需仿真 + 板级 MVP 闭环。

谢谢 · 欢迎讨论

基于 TCC 知识库基线 v2.0 与原语规范 v1.1 · 组会交流版

17/18

---
## 相关链接
- [[tcc_first_principles]]
- [[tcc_paper_background]]
- [[TCC_Knowledge_Base_Baseline_v2.0]]
- [[TCC_Knowledge_Base_Baseline_v1]]
- [[TCC_Knowledge_Base_Baseline_v1.1]]
