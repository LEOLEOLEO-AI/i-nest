---
title: CST 智能涌现验证与数据实验协议
tags:
- brain
- criticality
- emergence
- large-language-model
- methodology
- neural-networks
- neuron
- neuroscience
- paper
- research-methods
---
## 核心策略确认：分两步走
*   **Phase 1：完善 CST 理论 + 数据验证（当前论文）**
    *   **核心目标**：使用已发表数据验证 CST 框架；对比 ANN（人工神经网络）和 BNN（生物神经网络）。
    *   **投稿目标**：Nature Communications / PNAS / PLoS Computational Biology。
*   **Phase 2：基础物理推导（留待下一篇）**
    *   **核心目标**：$\alpha$ 的重整化群推导；器件物理的第一性原理。
    *   **投稿目标**：Physical Review Letters / Physical Review E。

---

## 一、 数据来源清单（公开且可复现）

### 1.1 生物神经网络（BNN）数据集
| 数据集 | 物种 | 规模 | 数据类型 | 来源 | CST 可计算性 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **C. elegans 全脑连接组** | 秀丽隐杆线虫 | 302 神经元 | 结构+功能 | `http://www.wormatlas.org/` | ✅✅✅ 完美 |
| **Drosophila Hemibrain** | 果蝇 | 25,000 神经元 | 完整突触 | `https://neuprint.janelia.org/` | ✅✅✅ 完美 |
| **Allen Mouse Brain Connectivity** | 小鼠 | 213 脑区 | 介观投射 | `http://connectivity.brain-map.org/` | ✅✅ 可用（粗粒度） |
| **Human Connectome Project (HCP)** | 人类 | 1200 被试 | fMRI 功能连接 | `https://www.humanconnectome.org/` | ✅✅ 可用（需预处理） |
| **MICrONS Cortical mm³** | 小鼠视皮层 | ~75,000 神经元 | EM 重建 | `https://www.microns-explorer.org/` | ✅✅✅ 完美（2021 Nature） |

*   **关键优势**：C. elegans 拥有完整结构/功能/行为三合一数据；Drosophila 是最大完整连接组；HCP 具有智商测试分数可直接验证 $I$ 与 CST 的相关性。

### 1.2 人工神经网络（ANN）数据集
| 数据集/资源 | 包含内容 | 规模 | 来源 | CST 可计算性 |
| :--- | :--- | :--- | :--- | :--- |
| **Pythia 训练动态** | 8 个尺度模型训练过程 | 70M-12B 参数 | `https://github.com/EleutherAI/pythia` | ✅✅✅ 完美 |
| **TorchVision 预训练模型** | 50+ 视觉模型 | ResNet/VGG 等 | `https://pytorch.org/vision/stable/models.html` | ✅✅✅ 完美 |
| **Hugging Face 模型库** | 10 万+ 模型 | BERT/GPT/T5 等 | `https://huggingface.co/models` | ✅✅ 可筛选 |
| **OpenAI Scaling Laws** | GPT 系列训练曲线 | 125M-175B | `https://arxiv.org/abs/2001.08361` | ✅ 可提取 |
| **Stanford DAWN Benchmarks** | DAWNBench 性能数据 | 100+ 模型×任务 | `https://dawn.cs.stanford.edu/benchmark/` | ✅✅ 结构化数据 |

*   **关键优势**：Pythia 提供同一架构下不同尺度的完整训练轨迹；Hugging Face 的下游任务性能可作为智能指标 $I$。

---

## 二、 数据验证的核心实验设计

### 2.1 验证目标：回答 3 个科学问题
*   **Q1：CST 能否预测智能？（基础验证）**
    *   **假设**：CST 与智能指标 $I$ 正相关（Spearman $\rho > 0.7$）。零假设为随机网络等。
*   **Q2：BNN 与 ANN 遵循同一规律吗？（普适性）**
    *   **假设**：在 $(C_S, C_T, \Gamma_{st})$ 空间中，BNN 和 ANN 分布重叠。BNN 的 $\Gamma_{st}$ 更高，ANN 的 $C_S$ 更规则。
*   **Q3：CST 能否解释智能涌现？（机制洞察）**
    *   **假设**：Pythia 训练过程中，$\Gamma_{st}$ 在“涌现点”突然跃升。

### 2.2 实验矩阵（34 个核心系统）
1.  **BNN (n=10)**: C. elegans, Drosophila larva/adult, 小鼠 V1/全脑, 猕猴 M1, HCP 静息/任务, 海兔, 斑马鱼幼虫。
2.  **ANN-Vision (n=8)**: ResNet-18/50/152, VGG-16, EfficientNet-B0/B7, ViT-B, CLIP。
3.  **ANN-Language (n=10)**: Pythia 8 个尺寸, BERT-base, GPT-2。
4.  **Null Models (n=6)**: 随机网络, 规则网格, 度保留重连, 未训练 ResNet, 过拟合小 CNN, 随机 Transformer。

---

## 三、 CST 参数的可操作计算协议

### 3.1 空间复杂度 $C_S$ 的标准化计算
**指标**：小世界倾向性 (SWP), 层级性 (H), 富人俱乐部 (RC), 通讯能力 (Comm)。
*   **BNN**：输入邻接矩阵，计算 4 个指标后 z-score 标准化，加权求和并通过 sigmoid 归一化。
*   **ANN**：提取层权重并阈值化（保留 Top 10%）构建单一多层图，后续计算同 BNN。

### 3.2 时间复杂度 $C_T$ 的标准化计算
**指标**：临界性 (Crit), 多尺度熵 (MSE), 元稳定性 (Meta), 灵活性 (Flex)。
*   **BNN**：输入时间序列矩阵（如 fMRI/钙成像），标准化并归一化。
*   **ANN**：在验证集上前向传播提取激活轨迹，拼接为时间序列矩阵后同 BNN 计算。

### 3.3 时空协同指数 $\Gamma_{st}$ 的稳健计算
**核心改进**：从不稳定的 Mantel 检验改为 **核对齐（HSIC）**。
*   构建结构核 $K_S$（基于最短路径的 RBF）和功能核 $K_T$（基于相关距离的 RBF）。
*   计算 HSIC 统计量并通过置换检验获取 $p$ 值，最终使用 $\tanh$ 归一化到 $[-1, 1]$。

### 3.4 权重学习与 Discovery-Replication 协议
*   **Discovery Cohort (n=15)**：5 个 BNN, 5 个 ANN-V, 5 个 ANN-L。通过 Ridge 回归学习标准化后的 $w$ 和 $v$ 权重。
*   **Replication Cohort (n=19)**：剩余系统使用固定的 $\mu, \sigma, w, v$ 预测智能 $I_{pred}$，计算 MAPE 和 $R^2$ 误差。

---

## 四、 智能指标 $I$ 的标准化定义
所有指标 $I$ 均归一化至 $[0, 1]$：
*   **BNN**：趋化准确率、方向选择性比例、g 因子（PC1）、运动解码 $R^2$。
*   **ANN**：Top-1 准确率、LAMBADA 准确率、GLUE 平均分。

---

## 五、 论文主图设计 (Storyline)

*   **Figure 1：CST 框架总览**
    *   理论框架图（$C_S, C_T, \Gamma_{st} \rightarrow CST \rightarrow I$）；Discovery 流程图；跨基质结构对比图。
*   **Figure 2：Discovery Cohort 回归分析**
    *   $C_S/C_T$ vs $I_{obs}$ 散点图；$\Gamma_{st}$ 分布（BNN vs ANN）；核心结果：CST vs $I_{obs}$ 对数散点图。
*   **Figure 3：Replication 验证与预测误差**
    *   预测 vs 实测散点图；Bland-Altman 误差图；分类误差箱线图；CST 与 Null 模型的显著性对比。
*   **Figure 4：智能涌现案例研究 (Pythia)**
    *   大模型 $\Gamma_{st}$ 的跃升点检测；CST 与准确率的 S 型涌现轨迹；类似相变的机制解释。
*   **Figure 5：BNN vs ANN 的系统对比**
    *   3D 参数空间散点图（进化优化 vs 工程设计）；雷达图展现 8 个维度的均值差异。

## Related Notes

- [[iNEST研究路线及方案]]
- [[智能算力]]
- [[物理类脑项目群]]
