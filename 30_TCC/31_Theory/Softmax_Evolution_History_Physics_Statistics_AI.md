---
direction: both
category: 理论
tags: [softmax, 跨学科演化, 统计力学, 深度学习, 注意力机制, transformer]
summary: "Softmax函数从物理到AI的百年跨学科演化史"
quality: high
processed: 2026-07-15 14:44
provenance: external
---
---
title: getnote_1915565304252630240_横跨物理、统计与AI：Softmax函数的百年演化全史
tags:
  - first-principles
  - neuroscience
  - network
  - transformer
  - ai
  - neural
  - research
  - physics
  - paper
  - llm
  - architecture
  - design
date: 2026-07-14 20:25
source: GetNotes
score: 17
---

## Original Note

---
note_id: 1915565304252630240
title: "横跨物理、统计与AI：Softmax函数的百年演化全史"
type: link
created: 2026-07-14 14:06:51
source: getnote
kb: 
---

# 横跨物理、统计与AI：Softmax函数的百年演化全史

### 🔍 核心背景概述

深度学习模型几乎都在最后一层使用的**softmax函数**，其数学形式的诞生时间比第一台电子计算机早近80年，是一段横跨物理学、统计学、人工智能的跨学科奇妙演化历程。

### 📜 第一阶段：热力学中的起源（1868-1902）

#### 玻尔兹曼的最初推导

1868年，奥地利物理学家**路德维希·玻尔兹曼（Ludwig Boltzmann）**在研究气体分子运动时，推导出描述系统微观状态概率分布的公式：
$$p_i = e^{(-\varepsilon_i/kT)} / \sum_j e^{(-\varepsilon_j/kT)}$$
其中$k$是玻尔兹曼常数，$T$是热力学温度。将公式中的$-\varepsilon_i/k$替换为任意实数$z_i$，就得到了标准softmax的数学形式：
$$\sigma(z)_i = e^{z_i} / \sum_j e^{z_j}$$
这一数学形式的出现比第一台电子计算机早近80年。

#### 吉布斯的系统化推广

1902年，美国物理学家**约西亚·威拉德·吉布斯（Josiah Willard Gibbs）**在著作《统计力学的基本原理》中，将该分布系统化推广，物理学领域将其命名为**玻尔兹曼分布/吉布斯分布**：
- 公式分母$\sum_j e^{(-\varepsilon_j/kT)}$被命名为**配分函数（Partition Function）**，成为统计力学的核心概念。
- 温度参数$T$控制分布的“尖锐程度”：高温时各状态概率趋于均匀，低温时概率集中在最低能量状态，该概念后续完整进入机器学习领域，成为如今广泛使用的temperature参数。

### 📊 第二阶段：统计学的独立发现（1966-1969）

物理学家提出该公式近百年后，统计学家与经济学家在解决多分类问题时，独立“重新发明”了完全等价的数学形式：
1.  二分类场景下，逻辑回归（Logistic Regression）使用sigmoid函数完成任务，但无法适配手写数字识别等多分类需求。
2.  1966年英国统计学家David Cox、1969年荷兰计量经济学家Henri Theil分别独立提出**多项Logit模型（Multinomial Logit Model）**，其数学形式与玻尔兹曼分布完全一致，当时被命名为“多项逻辑回归”或“log-linear model”，也就是如今所说的softmax回归。

### 🎯 第三阶段：“Softmax”命名正式诞生（1989）

该数学形式存在120多年后，“softmax”这一名称才正式出现：
- 英国语音识别研究者**John S. Bridle**在1989年NIPS（当时全称Neural Information Processing Systems）会议的论文中首次使用“softmax”一词。
- 命名逻辑是与硬选择函数argmax形成对应：
  | 函数 | 特性 | 输出形式 |
  |---|---|---|
  | argmax | 硬性选择最大值 | 独热向量(0,0,1,0...) |
  | softmax | 用指数连续函数做“软”选择 | 归一化概率分布，是argmax的平滑近似 |
- 当温度$T \to 0$时，softmax会退化为argmax；反之高温会让分布趋于均匀。Bridle的另一核心贡献是将softmax与交叉熵损失配对使用，证明该组合等价于互信息最大化的判别式训练，大幅提升了语音识别HMM模型的性能。

### 🚀 第四阶段：神经网络时代的普及（1990s-2010s）

softmax凭借独特的数学特性成为深度学习的标准配置：
- 它与交叉熵损失结合后，梯度计算形式极其简洁：$\partial L/\partial z_i = \sigma(z)_i - y_i$，即“预测概率减去真实标签”，不存在复杂的链式展开项与高阶导数，是反向传播算法的完美搭档。
- 2012年AlexNet在ImageNet竞赛中使用softmax完成1000类图像分类一战成名，后续VGG、GoogLeNet、ResNet等所有主流图像分类网络的最后一层均采用softmax，深度学习爆发的十年也成为softmax全面普及的十年。

### ⚡ 第五阶段：Transformer时代的核心升级（2017-至今）

在Transformer架构中，softmax的定位从输出层激活函数升级为核心运算：
1.  缩放点积注意力的标准公式为：$Attention(Q,K,V) = softmax(QK^T/\sqrt{d_k}) \cdot V$，softmax不再仅作为输出层，而是成为注意力机制的核心环节，在模型的每一层、每个注意力头、每个token的计算中都会被执行。
2.  GPT-4级别的大模型单次推理需要执行数千次softmax运算，是当前软硬件协同优化的核心焦点。
3.  当大模型词表规模达到数万甚至数十万时，softmax分母的全量指数求和成为性能瓶颈，业界衍生出多类优化方案：

| 优化方案 | 核心特性 | 提出者/时间 |
|---|---|---|
| 层次化softmax | 用平衡二叉树将计算复杂度从O(K)降至O(log K) | Morin & Bengio, 2005 |
| 分化softmax | 根据词频分配不同维度的嵌入向量 | - |
| 采样softmax | 训练时仅采样部分负样本近似分母求和 | - |
| FlashAttention | 通过分块计算与IO优化加速注意力中的softmax运算 | Dao et al., 2022 |

### 🧩 第六阶段：主流变体探索

为解决原生softmax的缺陷，学界陆续提出多类改进版本：
| 变体名称 | 核心特点 | 提出年份 |
|---|---|---|
| sparsemax | 输出稀疏概率，部分类别的概率可精确为0 | 2016 |
| Gumbel-softmax | 实现可微的离散采样，适配VAE与GAN场景 | 2016 |
| concrete distribution | 与Gumbel-softmax并行的同类研究工作 | 2016 |
| Taylor softmax | 通过二阶泰勒展开近似实现计算加速 | 2017 |
| Adaptive softmax | 根据词频自适应分配模型容量 | 2017 |
| Mixture of Softmaxes (MoS) | 多个softmax混合，提升语言模型表达能力 | 2018 |
| Sigmoid attention | 用sigmoid替代softmax，实现线性计算复杂度 | 2023 |

### 💡 关键洞察

softmax是跨学科演化的典型范例：同一个数学公式在三个完全独立的领域被三次发现——1868年物理学领域用于描述气体分子能级分布、1966-1969年统计学领域用于多类别概率建模、1989年至今深度学习领域作为激活函数与注意力核心运算。21世纪最强大的AI模型的核心运算，其数学形式是物理学家在蒸汽机尚未完全普及的年代，为理解气体分子行为推导出的成果，这一历程也揭示了一个规律：当下基础学科课本中的冷门公式，很可能会成为下一轮技术革命的核心基石。

---
*getnote | 2026-07-14 20:25*


---

## Related Notes

[[iNEST-MOC]]
[[paper2_liquid_computing_chemistry]]
[[paper1_iNEST_core_architecture]]
[[Papers-MOC]]
- [[Non-ideal_effects_in_artificial_synapses_Nature_Reviews_Physics_2026]]
- [[马毅_Yi Ma_UC Berkeley EECS讲座_智能的本质与AI的范式转移_从黑盒工程到第一性原理科学]]
- [[GetNote_20260606_100554_getnote_1911898566117388992_NEST 智能涌现研究进展与工程落地全景]]
- [[getnote_2026-06-15_能量函数驱动神经网络设计]]
- [[BDH_brain-inspired_AI_architecture_analysis]]
- [[GetNote_20260606_100554_kb_iNEST_getnote_1911898566117388992_NEST 智能涌现研究进展与工程落地全景]]
