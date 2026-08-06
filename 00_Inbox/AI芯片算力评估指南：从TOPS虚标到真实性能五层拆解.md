---
title: "AI芯片算力评估指南：从TOPS虚标到真实性能五层拆解"
tags:
  - infrastructure
  - research
  - architecture
  - ai
  - computing
  - first-principles
  - llm
  - design
  - transformer
  - semiconductor
  - hardware
  - chip
  - physics
  - paper
date: 2026-08-06 21:00
source: GetNotes
score: 25
---

## Original Note

---
note_id: 1917704249506118848
title: "AI芯片算力评估指南：从TOPS虚标到真实性能五层拆解"
type: link
created: 2026-08-06 15:27:39
source: getnote
kb: 
---

# AI芯片算力评估指南：从TOPS虚标到真实性能五层拆解

### 🏆 TOPS为什么几乎没有约束力？

TOPS只描述**乘加器数量与频率**，完全不反映实际喂饱能力。
- **计算公式**：TOPS = MAC单元数 × 每周期MAC数 × 2 × 频率
  - 「×2」来自一次乘加按乘法+加法两次运算计数
- **核心局限**：只算理论峰值，不涉及数据搬运、架构、软件等决定性能的关键因素

### ❓ 看TOPS必须追问哪五件事？

五个口径层层缩水，标称100 TOPS可能只剩个位数可用。
- **追问1：稀疏还是稠密？**
  - NVIDIA A100 INT8标称1248 TOPS = 624稠密 + 624（2:4结构化稀疏）
  - 2:4稀疏需模型稀疏感知训练/微调，多数生产模型无法享受这一倍算力
  - 规格书常将两者挤在同一行，仅用"with sparsity"脚注区分
- **追问2：峰值还是持续？**
  - 峰值 = 所有MAC在最高频率下满载的理论上限
  - 持续 = 功耗墙与结温约束下长期维持水平
  - 移动端受整机热预算限制，持续负载更易降频，峰值参考价值有限
- **追问3：什么精度？**
  - 同一芯片相邻精度算力通常差2倍：H100 FP8/INT8 1979 TOPS vs FP16 989 TFLOPS
  - Blackwell从FP16到FP4算力差4倍
  - 部分端侧NPU不支持满速FP16，跑FP16需退回GPU/CPU，差距是"有"和"没有"
- **追问4：利用率是多少？**
  - 同样标称100 TOPS，ResNet-50上利用率80% vs 30%，实际性能差2.7倍
  - 利用率取决于PE阵列形状、片上SRAM、数据搬运重叠、编译器算子融合
  - 几乎全是架构和软件问题，与MAC数量无关
- **追问5（端侧专属）：单芯片还是平台总和？**
  - 消费电子常见虚标：将NPU+GPU+CPU AI算力相加报成"平台TOPS"
  - 已有标称90+ TOPS机型，NPU单独仅13 TOPS
  - 模型通常由主引擎执行，异构难以线性叠加，CPU/GPU能效低于专用NPU
  - 参照标准：微软Copilot+ PC准入线 = NPU单独≥40 TOPS（INT8）

### 📊 三个利用率指标分别怎么用？

三个指标适用场景不同，用错会得出相反结论。
- **MFU（模型FLOPS利用率）** = 实际模型FLOPS ÷ 峰值FLOPS（稠密）
  - PaLM-540B在6144颗TPU v4上训练MFU为46.2%
  - 业内普遍约30%，顶尖集群约50%
  - 跨卡通信、非矩阵算子、流水线气泡都会拉低MFU，接近100%需高度怀疑
- **HFU（硬件FLOPS利用率）** = 含激活重算的硬件FLOPS ÷ 峰值FLOPS
  - PaLM论文中HFU为57.8%，高于MFU
  - 差值主要来自激活重算（用算力换显存，重算FLOPS非模型必需）
  - HFU统计依赖计数方法，不适合跨系统对比，厂商只报HFU需问清计数口径
- **MBU（模型带宽利用率）** = 实测有效访存带宽 ÷ 峰值带宽
  - decode阶段MFU几乎无意义：自回归生成逐token读权重，计算量极小，天然带宽受限
  - MBU分子 =（模型参数大小 + KV-Cache大小）÷ TPOT 估算的有效带宽
  - decode阶段应以MBU为主，同时保留延迟与goodput约束

| 阶段 | 核心特征 | 主要指标 |
| :--- | :--- | :--- |
| 训练 | 大batch GEMM为主，算力受限 | MFU（追问是否HFU） |
| Prefill | 并行处理prompt，算术强度高 | MFU |
| Decode | 逐token推进，反复读权重 | **MBU** |

### 📈 Roofline模型怎么定位性能瓶颈？

Roofline用一张图区分**带宽受限**还是**算力受限**，指明优化方向。
- **基本构成**：
  - 横轴：算术强度 = FLOPs ÷ 访存字节数
  - 纵轴：可达性能（FLOPS）
  - 左斜线：带宽上限，斜率=峰值带宽
  - 右水平线：峰值算力上限
- **脊点（Ridge Point）** = 峰值算力 ÷ 峰值带宽
  - 物理含义：算术强度低于此门槛的算子，永远碰不到峰值算力
  - H100 SXM FP16稠密脊点 ≈ 295 FLOP/Byte（989.4 TFLOPS ÷ 3.35 TB/s）
  - 注意：若误用带2:4稀疏的1979 TFLOPS计算，脊点会错算为590，优化空间估算错一倍

| 芯片 | 稠密峰值 | 带宽 | 脊点（FLOP/Byte） |
| :--- | :--- | :--- | :--- |
| V100 SXM2 | FP16 125 TFLOPS | 900 GB/s | ≈ 139 |
| A100 SXM 80G | FP16 312 TFLOPS | 2.04 TB/s | ≈ 153 |
| H100 SXM | FP16 989 TFLOPS | 3.35 TB/s | ≈ 295 |
| H200 SXM | FP16 989 TFLOPS | 4.8 TB/s | ≈ 206 |
| B200 | FP16 2250 TFLOPS | 8 TB/s | ≈ 281 |
| B200（FP4） | FP4 9000 TFLOPS | 8 TB/s | ≈ 1125 |
- **三个关键结论**：
  - **同精度脊点总体抬高**：V100到H100从139升至295，更多算子掉进带宽受限区，存储墙效应凸显
  - **H200脊点回落**：只加带宽不加算力，脊点从295降至206，对LLM推理收益更直接
  - **低精度不是免费午餐**：B200 FP4脊点飙至1125，算力翻4倍但带宽不变，原本够到屋顶的算子重新掉回带宽受限区

### 🧩 Transformer各阶段在Roofline上落在哪里？

不同算子算术强度差异极大，瓶颈类型完全不同。

| 阶段/算子 | 算术强度 | 状态 |
| :--- | :--- | :--- |
| QKV投影/FFN（GEMM） | 高（通常>200） | 视batch而定 |
| Attention Score（BMM） | 中（~seq_len量级） | 长序列转算力受限 |
| Softmax/LayerNorm | 极低（<5） | 严重带宽受限 |
| Decode读权重 | FP16≈batch；INT8/FP8≈2×batch | 极度带宽受限 |
- **decode权重侧算术强度上界公式**：≈ 2 × batch ÷ 单权重字节数
  - FP16/BF16（2 Byte）：≈ batch
  - INT8/FP8（1 Byte）：≈ 2 × batch
  - FP4（0.5 Byte）：≈ 4 × batch
- **H100 FP16实例**：
  - batch=1时，算术强度≈1，可达算力上限≈0.34%
  - batch=128时，算术强度≈128，仍在带宽受限区，距脊点约2.3倍
- **decode优化方向**：
  - 增大batch（continuous batching）→ 提高权重复用
  - 权重/KV-Cache量化 → 减少字节数
  - PagedAttention → 降低KV-Cache碎片，提高并发
  - Prefill-Decode分离 → 改善资源隔离与调度

### ⚠️ Roofline有哪些看不到的瓶颈？

Roofline是**稳态峰值模型**，有明确失效边界，不是性能承诺书。
- **只画单层存储**：真实芯片有SRAM/L2/HBM多级，每级有自己的带宽屋顶
  - FlashAttention通过片上SRAM复用减少HBM往返，提高有效算术强度
- **不建模延迟和占用率**：kernel可能因并行度不够而慢，不撞带宽也不撞算力
- **不建模通信**：多卡场景互连带宽往往才是真屋顶
- **不建模流水线气泡**：prefill/decode不重叠、梯度同步等待、负载不均等损失完全不可见

### 🏭 跨厂商横比看什么基准？

MLPerf是目前最权威的第三方基准，但读结果有四个陷阱。
- **MLPerf主要赛道（截至2026年中）**：
  - **Training**：v5.1（2025-11）替换BERT为Llama 3.1 8B，新增Flux.1；v6.0（2026-06）加入MoE基准
  - **Inference**：分Datacenter/Edge赛道，v5.1新增DeepSeek-R1、Llama 3.1 8B、Whisper Large V3；v6.0加入GPT-OSS 120B、文生视频等
  - **Client**（v1.5, 2025-11）：面向AI PC
  - **Automotive**（v0.5, 2025-08）、Storage、Tiny（MCU级）、HPC
- **读结果四个陷阱**：
  - **系统配置差异**：8卡vs16卡不能直接比，先看per-accelerator归一化数据
  - **Closed vs Open Division**：Closed固定模型和预处理，最适合同类对比；Open允许任意改动
  - **三类可获得性**：Available（可购买/租用）、Preview（下轮转Available）、RDI（研究实验性，无商用承诺）
  - **软件栈版本**：同一硬件跨版本两位数百分比提升很常见，必须核对版本号
- **隐藏宝藏**：MLPerf Inference功耗赛道测整机AC平均功率，是公开跨厂商能效数据中最可靠来源之一
- **过时信息更新**：
  - Geekbench ML 2024年8月更名Geekbench AI并发布1.0
  - SPEC ACCEL 2024年6月退役，继任者为SPECaccel 2023

### 💰 最终决策看哪两个数？

买家真正签字的是**能效**和**成本**，但两者都有口径陷阱。
- **能效：TOPS/W**
  - 分母口径差异：是否含片上SRAM、DRAM I/O、整板供电损耗
  - 分子口径差异：峰值还是持续
  - 三个口径各差一点，累计可差2-3倍，跨厂商直接比自报TOPS/W几乎总是错的
  - 芯片设计内部更常用pJ/OP（每次运算能量）和TOPS/mm²（面积效率）
- **成本：$/M tokens**
  - 数据中心推理市场最终决策变量
  - 受电价、折旧年限、假定利用率三个参数影响极大，是TCO计算最易做手脚的地方
  - 看到诱人数字先问这三个假设
- **延迟指标**：
  - TTFT（首token延迟）、TPOT/ITL（token间延迟）、goodput（满足SLA的吞吐）
  - 不注明延迟约束的吞吐数字很难用于服务选型
  - MLPerf Server场景带SLA约束，Offline是无约束吞吐，衡量能力完全不同
  - MLPerf v6.0 DeepSeek-R1 Server阈值：p99 TTFT 2秒、p99 TPOT 80毫秒；Interactive场景：p99 TTFT 1.5秒、p99 TPOT 15毫秒

### 📋 拿到规格书按什么顺序核查？

五层核查清单，从峰值到结账层层递进。
1. **峰值层**：稀疏/稠密？峰值/持续？精度对齐？单NPU还是平台总和？
2. **利用率层**：目标模型MFU/MBU多少？报的是MFU还是HFU？阶段与指标是否匹配？
3. **归因层**：脊点多少？主力算子在脊点哪一侧？decode batch能做到多大？是否有Roofline看不见的瓶颈？
4. **横比层**：有无MLPerf成绩？Closed/Open？Available/RDI？per-accelerator归一化后如何？有无功耗赛道？
5. **结账层**：$/M tokens多少？三个假设是什么？延迟约束下吞吐剩多少？

### 📝 补充细节
- 两颗同标100 TOPS的芯片，实际性能差距可能达十倍，TOPS从定义上就不包含决定实际性能的变量
- 评估AI算力的核心 = 乘加器能不能被持续喂饱数据，而非乘加器本身数量
- 微软Copilot+ PC的NPU≥40 TOPS要求是INT8精度，且仅算NPU单独算力

---
*getnote | 2026-08-06 21:00*


---

## Related Notes

[[SDI化合物键_四型架构]]
[[FPGA原型]]
[[Papers-MOC]]
[[paper2_liquid_computing_chemistry]]
[[iNEST-MOC]]
