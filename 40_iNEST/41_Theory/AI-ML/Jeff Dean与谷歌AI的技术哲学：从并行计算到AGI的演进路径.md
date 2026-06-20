---
title: "Jeff Dean与谷歌AI的技术哲学：从并行计算到AGI的演进路径"
source: "https://mp.weixin.qq.com/s/-w9V_s_7pDhvorFbZ98x0w"
created: 2026-02-21
note_id: "1902283758913597992"
tags:
  - "AI链接笔记"
  - "知识蒸馏"
  - "Jeff Dean"
  - "Google AI"
  - "get-笔记"
  - "学术论文"
  - "重要"
---

# Jeff Dean与谷歌AI的技术哲学：从并行计算到AGI的演进路径

## 摘要

### **🔍 引言：核心研究背景与目标**  本研究旨在剖析Google首席科学家Jeff Dean在Latent Space播客访谈中披露的核心技术哲学与工程实践。作为Google基础设施与AI发展的总设计师之一，Dean的职业生涯跨越了从1990年代神经网络寒冬到2024年生成式AI爆发期。报

## 正文

# 在谷歌AI的错过与追赶一文中，我们知道，为应对Open AI的chatgpt带来的冲击，2023年4月Google成立新部门“Google DeepMind”，由DeepMind的创始人Demis Hassabis担任CEO，而Google Brain的灵魂人物Jeff Dean转任首席科学家，并承担起来一系列重任。

> Jeff
> Dean则承担起了协调双方技术架构的重任，特别是将DeepMind的各种研究成果迁移到谷歌统一的TPU基础设施上。在处理复杂逻辑和跨模态任务时，Gemini 3
> Pro展现出了Jeff Dean所设计的MoE（混合专家）架构的高效性。
>
> 二庄主，公众号：技术不平等[谷歌AI的“错过”与“追赶”](https://mp.weixin.qq.com/s/xYDbf3Rx733SNQC3Sh3y7A)

# 

在 Latent Space 播客2月13日一期节目中，主持人 Alessio 和 Swyx 与 Jeff Dean
进行了一个多小时的深度对话。话题跨度极大：从蒸馏技术的真实起源，到“能否让 AI 关注整个互联网”的长上下文愿景；从用皮焦耳理解为什么 GPU
需要批处理，到那份改变了 Google AI
格局的一页纸备忘录。见：https://podcasts.apple.com/us/podcast/owning-the-ai-pareto-frontier-jeff-dean/id1674008350?i=1000749498954

本文旨在系统性解构谷歌（Google）首席科学家 Jeff Dean
在访谈中展现的核心技术哲学与工程实践，探索人工智能从早期连接主义寒冬走向现代通用超级系统的内在演进逻辑。文章采用文献分析与技术史回溯相结合的方法，梳理了
Dean 从 1990 年本科论文的理论构建到 2024 年 Gemini
万亿参数模型爆发期间的关键技术断层线。重点剖析了并行训练架构的工业化路径、知识蒸馏理论的系谱演变、基于计算物理学（即皮焦耳能耗与内存墙）的硬件限制，以及应对复杂大模型研发所进行的组织结构重组。

研究发现，“拥有帕累托前沿”的全维度战略贯穿了谷歌 AI 发展的始终。从 DistBelief 到 TensorFlow
验证了规模化并行的技术预言；知识蒸馏通过提取对数几率（Logits）中的“暗知识”实现了模型降维映射；而内存传输中的极高物理能耗，则直接催生了环状注意力（Ring
Attention）及大批处理架构等创新；此外，“一页备忘录”驱动的 Google DeepMind
组织合并，为底层算力与顶层模型设计的统一提供了不可或缺的制度保障。当代生成式人工智能的突破不仅仅是算法模型的胜利，更是对底层热力学物理极限的工程化克服与顶层组织架构重组的必然结果。跨越算力、能耗与组织边界的系统性思维，是迈向通用人工智能（AGI）的核心驱动力。

## 引言（原内容摘要）

本研究旨在剖析 Google（谷歌）首席科学家 Jeff Dean（杰夫·迪恩）在 Latent Space 播客访谈中披露的核心技术哲学与工程实践。作为
Google 基础设施与人工智能（Artificial Intelligence, AI）发展的总设计师之一，Dean 的职业生涯跨越了从 1990
年代的神经网络寒冬到 2024 年的生成式人工智能（Generative
AI）爆发期。本报告将系统性地解构他在访谈中提及的四大关键主题：并行训练的早期起源、知识蒸馏（Knowledge
Distillation）的认识论演变、受物理定律（热力学与能耗）约束的计算瓶颈，以及通过“一页备忘录”推动的 Google AI
组织架构重组。通过对这些技术断层线的分析，我们试图还原从分布式系统到底层物理，再到顶层模型设计的完整技术进化图谱，并探讨“帕累托前沿”（Pareto
Frontier）在现代人工智能系统设计中的指导意义。

## 第一章 思想考古：1990 年本科论文与规模化计算的预言

### 1.1 神经网络寒冬中的逆流

要理解当代大型语言模型（Large Language Model, LLM）的爆发，我们必须回溯到 1990
年。当时的计算机科学界正处于所谓的“人工智能寒冬”（AI Winter）末期。在那个时代，符号主义（Symbolism）和基于规则的专家系统（Expert
Systems）遭遇瓶颈，而以神经网络为代表的连接主义（Connectionism）因缺乏算力和数据而被视为理论上优美但实践中无用的“玩具模型”。

正是在这个历史背景下，当时还在明尼苏达大学（University of Minnesota）攻读本科的 Jeff Dean
完成了一篇具有划时代意义的荣誉论文，题为《神经网络的并行训练》（Parallel Training of Neural Networks）。

作为一名高校教师，当我们审视这份 30 多年前的学术文本时，可以清晰地看到现代深度学习基础设施的雏形。Dean 在 1990
年的核心假设是：神经网络之所以表现不佳，并非因为其算法（如反向传播，Backpropagation）存在根本性缺陷，而是因为我们缺乏能够支撑其规模化运行的计算架构。他提出，如果能够利用并行计算（Parallel
Computing）技术，将单一神经网络的训练任务分散到 64 个处理器上，就能训练出更大规模的网络，从而解决更复杂的问题。

这一思想在当时极具反叛性。主流学界正转向支持向量机（Support Vector Machine, SVM）和概率图模型（Probabilistic
Graphical Model, PGM），因为后者在数学上更具可解释性且对算力要求较低。然而，Dean 坚持了“规模决定论”的早期版本，这一直觉在随后的 25
年中被证明是通向通用人工智能（Artificial General Intelligence, AGI）的关键路径。

### 1.2 从 DistBelief 到 TensorFlow：并行范式的工业化

Dean 在 1990 年论文中探讨的并行模式，实际上预演了后来 Google 内部两大核心训练范式的诞生：

数据并行（Data
Parallelism）：将海量训练数据分割成多个“批次”（Batch），分发给不同的计算节点。每个节点计算梯度（Gradient），然后通过参数服务器（Parameter
Server）进行聚合。这是 2011 年 Google Brain（谷歌大脑）团队开发的 DistBelief 系统的核心机制。

模型并行（Model
Parallelism）：当神经网络的参数量超过单个处理器的内存限制时，将网络本身切分，不同的层（Layer）或神经元组分布在不同的物理设备上。

在访谈中，Dean 回顾了这一历程，指出这种对“规模”的执着最终导致了 2012 年著名的“猫识别”实验（The Cat Experiment）。该实验利用
16,000 个中央处理器（Central Processing Unit, CPU）核心训练了一个拥有 10
亿参数的深度神经网络，在没有监督的情况下学会了识别猫的概念。这一时刻标志着 Dean 1990 年的理论假设终于在工业级基础设施的支持下变成了现实。

| 年份 | 系统/项目 | 核心贡献 | 与 1990 年论文的联系 |
| --- | --- | --- | --- |
| 1990 | 本科论文 | 提出利用 64 个处理器并行训练神经网络 | 奠定了并行训练的理论基础，预见了算力扩展的重要性。 |
| 2004 | MapReduce | 建立大规模数据并行处理的编程模型 | 将并行思想从神经网络推广到通用数据处理，为后来的数据清洗和预训练打下基础。 |
| 2011 | DistBelief | 首个大规模分布式深度学习训练系统 | 实现了 1990 年论文的工业化，引入参数服务器架构。 |
| 2015 | TensorFlow | 通用机器学习框架，支持异构设备 | 将并行策略标准化，支持数据并行与模型并行的灵活组合。 |
| 2024 | Gemini | 原生多模态、万亿参数级模型 | 在 TPU 集群上实现极致的规模化，验证了“更大模型、更多数据”的长期信条。 |

### 1.3 “拥有帕累托前沿”的战略意义

Jeff Dean 在访谈中反复提到的“帕累托前沿”（Pareto Frontier）不仅是一个数学概念，更是 Google AI
研发的战略基石。在多目标优化问题中，帕累托前沿代表了在给定约束条件下无法通过牺牲某一目标来改善另一目标的最优解集合。

对于 AI
系统，主要的权衡维度包括：模型质量（Quality）：准确率、推理能力、多模态理解力。推理延迟（Latency）：生成首个词元（Token）的时间、吞吐量。训练与推理成本（Cost/Energy）：以美元或焦耳为单位的资源消耗。

Dean 的观点是，不仅要构建处于前沿顶端的最强模型（如 Gemini Ultra），还要通过技术手段填充整条曲线，提供极低延迟但质量尚可的模型（如
Gemini Flash）。这种全覆盖战略要求对计算系统进行极致的优化，而不仅仅是算法层面的创新。

## 第二章 知识蒸馏的系谱学：从模型压缩到暗知识的传递

在解释如何让轻量级的 Flash 模型拥有接近 Pro 模型的性能时，Jeff Dean
强调了“蒸馏”（Distillation）的关键作用。作为一名思想考古者，我们需要剥离“蒸馏”这一术语的商业包装，追溯其学术源流，并理解其背后的认知科学隐喻。

### 2.1 历史的修正：Buciluǎ (2006) 与 Hinton (2015)

虽然 Geoffrey Hinton（杰弗里·辛顿）在 2015 年发表的论文《在神经网络中蒸馏知识》（Distilling the Knowledge in
a Neural Network）广为人知，但 Jeff Dean 在访谈中严谨地指出了这一技术的更早源头：2006 年由 Cristian Buciluǎ
等人发表的《模型压缩》（Model Compression）。

2006 年的尝试（模型压缩）：Buciluǎ 等人的工作主要集中在将当时最先进的集成模型（Ensemble
Models，如数千个决策树或神经网络的组合）压缩成一个单一的、较小的神经网络。其核心动机是解决集成模型推理速度过慢、内存占用过高的问题。他们的方法是利用大模型对未标注数据进行标记，生成“伪数据”（Pseudo-data）来训练小模型。

2015 年的突破（知识蒸馏）：Hinton、Vinyals 和 Dean 在 2015
年的论文中，将这一思想升华为了“知识蒸馏”。这一阶段的核心贡献不在于“用大模型教小模型”这一形式，而在于发现了“软目标”（Soft
Targets）中蕴含的丰富信息。

### 2.2 暗知识（Dark Knowledge）与软目标

为什么大模型（教师模型）能教会小模型（学生模型）原本学不到的东西？Jeff Dean 深入解析了其中的机制：Logits（逻辑值）中的暗知识。

在传统的监督学习中，模型的目标是匹配“硬标签”（Hard Labels）。例如，在识别一张“宝马汽车”的图片时，硬标签是 [0, 0, 1,
0,...]（假设索引 2 对应宝马）。这告诉模型“这是宝马”，但也隐含地告诉模型“这绝对不是垃圾车”和“这绝对不是胡萝卜”。

然而，教师模型在输出层产生的未归一化逻辑值（Logits）包含的信息远不止于此。经过 Softmax 函数处理前的 Logits
可能显示：宝马：0.9；奥迪：0.09；垃圾车：0.000001；胡萝卜：0.000000。

这里包含了一个至关重要的结构化知识（Structured
Knowledge）：这张图片虽然是宝马，但它与奥迪的相似度远高于与垃圾车的相似度。这种关于“类别间相似性”的信息，被称为“暗知识”。通过引入温度参数
T（Temperature），蒸馏过程将这些微小的概率分布“软化”并放大，迫使学生模型不仅学习到“是什么”，还学习到“像什么”以及“为什么像”。

qi = exp(zi / T)∑j exp(zj / T)

(公式 1：带有温度参数 T 的 Softmax 函数，用于生成软目标)

### 2.3 现代大模型时代的蒸馏变体

在 Gemini 的研发中，Dean 提到的蒸馏已经超越了 2015 年的 Logits 匹配，演化为更复杂的形态：

思维链蒸馏（Chain-of-Thought Distillation）：教师模型不仅提供最终答案，还提供推理步骤（Reasoning
Steps）。学生模型通过模仿教师的推理过程，习得逻辑能力。

白盒蒸馏（White-box Distillation）：利用对教师模型内部状态的完全访问权限，对齐中间层的激活模式（Activation
Patterns）和注意力矩阵（Attention Matrices）。

Dean 的结论发人深省：“你需要最大的模型来让最小的模型变好。”（You need the biggest model to make the
smallest one good.）这揭示了一个悖论：为了实现边缘计算和低延迟 AI，我们反而必须先构建极其庞大、极其昂贵的超级模型作为知识源头。

## 第三章 计算物理学：皮焦耳与能量瓶颈

本次访谈中最具技术深度的部分，是 Jeff Dean 引入了物理学视角来分析人工智能硬件的未来。他指出，当前 AI
扩展的限制因素不再仅仅是算力（FLOPs，每秒浮点运算次数），而是能量，具体量化单位为皮焦耳（Picojoules, pJ, 10-12 焦耳）。

### 3.1 冯·诺依曼架构的能耗诅咒

在现代计算架构中，计算（运算逻辑）与存储（内存）在物理上是分离的。这种分离导致了所谓的“内存墙”（Memory Wall），不仅限制了速度，更成为了能耗的黑洞。

Jeff Dean 引用了芯片设计领域的基本物理数据：计算极其廉价。在 7nm 或 5nm 工艺下，执行一次 32 位浮点乘法（FP32
Multiply）仅消耗约 3-4 pJ 的能量。数据移动极其昂贵。从芯片外的动态随机存取存储器（Dynamic Random Access Memory,
DRAM）或高带宽内存（High Bandwidth Memory, HBM）读取一个 32 位数据，消耗的能量可能高达 1000 pJ
以上。结论显而易见：移动数据的能耗成本是计算数据的 250 到 300 倍。

### 3.2 批处理（Batching）的物理必要性

这一物理事实解释了为什么深度学习训练和推理必须依赖批处理（Batching）。

如果在推理时 Batch Size = 1（即一次只处理一个用户的请求）：从 HBM 中读取巨大的权重矩阵 W（例如 100GB）。仅与一个向量 x
进行矩阵乘法运算。结果：99% 以上的能量被浪费在将权重从内存搬运到计算单元的路上，计算单元本身的利用率极低，且能效比（Performance per
Watt）极差。

如果在推理时 Batch Size = 128：从 HBM 中读取权重矩阵 W。与 128 个不同的向量 x1, x2, ..., x128
进行运算。结果：昂贵的内存读取成本被 128 次计算分摊。

Dean 指出，这就是为什么我们不能为了追求极致的低延迟（Latency）而无限缩小 Batch Size。在“算术强度”（Arithmetic
Intensity，即每字节数据传输对应的浮点运算次数）不足的情况下，系统将受到内存带宽的严格限制。

### 3.3 未来的架构方向

基于皮焦耳的分析，Dean 展望了未来的硬件架构方向：

近存计算（Near-Memory Computing）：将计算单元尽可能靠近内存，减少数据移动的物理距离。

3D 堆叠（3D Stacking）：利用垂直堆叠技术，缩短互联线长。

稀疏计算（Sparse Computation）：既然移动数据昂贵，那么就只移动和计算那些非零的、有意义的数据。这是 MoE（Mixture of
Experts，混合专家模型）架构在硬件层面的物理动机。

## 第四章 无限上下文的架构：Gemini 1.5 与环状注意力

Jeff Dean 在访谈中提到了 Gemini 1.5 Pro 实现了 100 万到 1000
万词元（Tokens）的上下文窗口，并能在其中进行近乎完美的检索。这一突破不仅仅是显存容量的增加，更是算法与分布式系统架构的革新。

### 4.1 标准注意力机制的 O(N2) 困境

标准的 Transformer 架构使用自注意力机制（Self-Attention），其计算复杂度和内存占用与序列长度 N 的平方成正比。对于 N =
1,000,000（100万），注意力矩阵包含 1012（1万亿）个元素。

即使使用半精度浮点数（FP16），仅存储键值缓存（KV Cache）就需要数 TB 的显存，这远超单张 TPU 或 GPU（如 H100 的 80GB）的容量。

### 4.2 环状注意力（Ring Attention）机制解析

为了突破这一物理限制，Google 采用了环状注意力（Ring Attention）技术。这是一种基于分块（Blockwise）计算的分布式注意力算法。

工作原理：序列分片：将长达 100 万 Token 的序列切分为多个块（Blocks），分布在由成百上千个 TPU 组成的环形拓扑网络中。每个 TPU
只存储序列的一小部分（例如 4096 个 Token）对应的 Query（查询）、Key（键）和 Value（值）。

流转与计算：每个 TPU 首先计算本地 Query 与本地 Key 的注意力分数。关键步骤：每个 TPU 将自己的 Key 和 Value 块发送给环中的下一个
TPU，同时接收上一个 TPU 传来的 Key 和 Value 块。接收到新的 KV 块后，TPU 继续计算其本地 Query 对新 KV 的注意力分数。

通信与计算重叠（Overlap）：Ring Attention 的核心在于掩盖通信延迟。当 TPU 正在全速计算矩阵乘法时，后台的专用互联网络（ICI,
Inter-Chip Interconnect）正在传输下一个数据块。只要计算时间足够长，通信时间就可以被完全“隐藏”。

| 特性 | 标准注意力 (Standard Attention) | 闪存注意力 (FlashAttention) | 环状注意力 (Ring Attention) | 无限注意力 (Infini-attention) |
| --- | --- | --- | --- | --- |
| 核心机制 | 全矩阵计算，O(N2) 显存 | 分块计算，IO 优化，单卡 | 分布式分块，环形通信 | 压缩记忆 + 局部注意力 |
| 显存瓶颈 | 极高，受限于单卡显存 | 较低，受限于单卡显存 | 极低，受限于集群总显存 | 极低，固定内存占用 |
| 通信开销 | 无 | 无 | 高，需计算与通信重叠 | 低 |
| 适用场景 | 短序列 (< 32k) | 中长序列 (< 128k) | 超长序列 (1M - 10M+) | 无限流式输入 |

### 4.3 “幻象”：万亿 Token 的错觉

尽管实现了 1000 万 Token 的物理上下文，Jeff Dean 提出了一个更深远的观点：未来的系统将提供“关注了万亿 Token
的幻象（Illusion）”。

这意味着真正的无限上下文不可能通过物理上将所有数据塞进 Transformer 的窗口来实现（那样成本太高）。相反，AI
系统将演化为类似搜索引擎的架构：外部记忆体：拥有万亿级别的外部索引（类似于 Google Search
的索引）。动态加载：模型根据当前任务，通过极其高效的检索算法（Retrieval），从外部记忆中抓取最相关的片段填入上下文窗口。用户体验：对用户而言，模型似乎“记住”了所有的历史和知识，但实际上它只是在这一瞬间“看到”了相关信息。这就是“幻象”的本质——用有限的计算资源模拟无限的认知能力。

## 第五章 组织工程学：“一页备忘录”与 Gemini 的诞生

Jeff Dean 的访谈不仅涉及技术，还罕见地披露了 Google 内部应对 OpenAI
挑战时的组织变革细节。这一变革的催化剂是一份被称为“一页备忘录”（One-page Memo）的内部文件。

### 5.1 资源碎片的危机

在 ChatGPT 爆发之前，Google 的 AI 力量分散在多个独立且经常相互竞争的团队中：Google Brain 负责大规模工程化模型（如 PaLM,
BERT）；DeepMind 位于伦敦，专注于强化学习和科学问题（如 AlphaFold, Chinchilla）；Google Research
则包含其他分散的研究小组。

Jeff Dean 在备忘录中直言不讳地指出：“我们正在愚蠢地（Stupidly）分割我们的资源。”这种碎片化导致算力无法集中，人才相互内耗，无法训练出能够与
GPT-4 抗衡的统一大模型。

### 5.2 备忘录的内容与 Gemini 的隐喻

备忘录的核心建议是：合并 Brain 和 DeepMind，集中所有算力（TPU 集群），训练单一的、多模态原生的超大模型。

这一建议直接促成了 Google DeepMind (GDM) 的成立。Jeff Dean 随后亲自将这个统一项目命名为 Gemini。这个名字富有深意：

双子座（Twins）：象征着 Brain 和 DeepMind 这两个原本独立的 AI 巨头如双胞胎般合二为一。

NASA Gemini 计划：在航天史上，Gemini
计划是连接单人飞船（Mercury）和登月计划（Apollo）的桥梁。它验证了太空对接等关键技术。Dean 以此寓意 Gemini
模型是通向最终通用人工智能（AGI，即“阿波罗时刻”）的关键一步。

## 结论

通过对 Jeff Dean 访谈及相关文献的“思想考古”，我们可以清晰地看到一条贯穿 30
年的技术主线：对规模（Scale）的极致追求和对物理瓶颈（Physics）的工程化克服。

从并行到集群：1990 年的并行训练思想，经过 30 年的硬件摩尔定律红利，演化为今天数万张 TPU
互联的超级计算机。从压缩到蒸馏：知识蒸馏不再仅仅是模型压缩的手段，而是“帕累托前沿”战略的核心引擎，使得昂贵的智能得以普及。从算力到能量：皮焦耳级别的能耗限制正在重塑算法设计，迫使我们关注数据移动的代价，并催生了
MoE 和稀疏注意力等新架构。从碎片到统一：Gemini 的诞生标志着 AI 研发进入了“大科学”（Big
Science）时代，组织架构的整合与技术架构的整合同样重要。

Jeff Dean 的工作提醒我们，计算机科学的突破往往不仅仅来自于数学公式的推导，更来自于对底层系统物理特性的深刻理解与系统架构的大胆重构。

## 参考文献

Apple Podcasts. (2026). *拥有人工智能帕累托前沿——杰夫·迪恩* [Owning the AI Pareto Frontier —
Jeff Dean]. 检索自 2026年2月18日, 从
https://podcasts.apple.com/us/podcast/owning-the-ai-pareto-frontier-jeff-dean/id1674008350?i=1000749498954

Radio.net. (2026). *潜在空间：AI工程师播客* [Latent Space: The AI Engineer Podcast]. 检索自
2026年2月18日, 从 https://www.radio.net/podcast/latent-space-podcast

Google Research. (n.d.). *杰弗里·迪恩* [Jeffrey Dean]. 检索自 2026年2月18日, 从
https://research.google/people/jeff/

Apple Podcasts. (2026). *拥有人工智能帕累托前沿——杰夫·迪恩* [Owning the AI Pareto Frontier —
Jeff Dean]. 检索自 2026年2月18日, 从
https://podcasts.apple.com/id/podcast/owning-the-ai-pareto-frontier-jeff-dean/id1674008350?i=1000749498954

American Academy of Arts and Sciences. (2022). *人工智能与社会* [AI & Society]. 检索自
2026年2月18日, 从
https://www.amacad.org/sites/default/files/daedalus/downloads/Daedalus\_Sp22\_AI-%26-Society\_0.pdf

ResearchGate. (n.d.). *优化技术以提高大型语音任务中深度神经网络的训练速度* [Optimization Techniques to
Improve Training Speed of Deep Neural Networks for Large Speech Tasks]. 检索自
2026年2月18日, 从
https://www.researchgate.net/publication/260695677\_Optimization\_Techniques\_to\_Improve\_Training\_Speed\_of\_Deep\_Neural\_Networks\_for\_Large\_Speech\_Tasks

arXiv. (2025). *针对开放权重模型的知识蒸馏检测* [Knowledge Distillation Detection for
Open-weights Models]. 检索自 2026年2月18日, 从 https://arxiv.org/html/2510.02302v1

Wikipedia. (n.d.). *知识蒸馏* [Knowledge distillation]. 检索自 2026年2月18日, 从
https://en.wikipedia.org/wiki/Knowledge\_distillation

arXiv. (2024). *基于条件互信息的知识蒸馏贝叶斯条件分布估计* [Bayes Conditional Distribution
Estimation for Knowledge Distillation Based on Conditional Mutual Information].
检索自 2026年2月18日, 从 https://arxiv.org/html/2401.08732v2

arXiv. (2015). *在神经网络中蒸馏知识* [Distilling the Knowledge in a Neural Network]. 检索自
2026年2月18日, 从 https://arxiv.org/abs/1503.02531

UPCommons. (n.d.). *通过在参数空间中平均神经网络实现高效的深度集成* [Efficient Deep Ensembles by
Averaging Neural Networks in Parameter Space]. 检索自 2026年2月18日, 从
https://upcommons.upc.edu/bitstreams/73523797-3fd4-49d8-b37b-b34ad6b7d39b/download

IEEE Computer Society. (2019). *用于知识蒸馏的相关一致性* [Correlation Congruence for
Knowledge Distillation]. 检索自 2026年2月18日, 从
https://www.computer.org/csdl/proceedings-article/iccv/2019/480300f006/1hVll3TMRAA

Intel Labs. (n.d.). *知识蒸馏 - 神经网络蒸馏器* [Knowledge Distillation - Neural Network
Distiller]. 检索自 2026年2月18日, 从
https://intellabs.github.io/distiller/knowledge\_distillation.html

MDPI. (n.d.). *神经网络能耗比较研究：通过缩放权重内存能量与计算能量实现低功耗边缘智能* [Comparative Study on Energy
Consumption of Neural Networks by Scaling of Weight-Memory Energy Versus
Computing Energy for Implementing Low-Power Edge Intelligence]. 检索自 2026年2月18日,
从 https://www.mdpi.com/2079-9292/14/13/2718

OSTI. (n.d.). *超越摩尔定律的计算未来* [The future of computing beyond Moore's Law]. 检索自
2026年2月18日, 从 https://www.osti.gov/servlets/purl/1619164

EDN. (n.d.). *AI处理器架构在功耗效率中的作用* [The role of AI processor architecture in power
consumption efficiency]. 检索自 2026年2月18日, 从
https://www.edn.com/the-role-of-processor-architectures-in-power-consumption-efficiency/

Carnegie Mellon University. (2021). *塑造谷歌TPUv4i的三代经验教训* [Ten Lessons From Three
Generations Shaped Google's TPUv4i]. 检索自 2026年2月18日, 从
https://www.cs.cmu.edu/~18742/papers/Jouppi2021.pdf

arXiv. (2021). *揭秘BERT：对加速器设计的启示* [Demystifying BERT: Implications for
Accelerator Design]. 检索自 2026年2月18日, 从 https://arxiv.org/pdf/2104.08335

Reddit. (n.d.). *[讨论] 理解最佳批次大小计算 - 算术强度* [[D] Understanding Optimal Batch Size
Calculation - Arithmetic Intensity]. 检索自 2026年2月18日, 从
https://www.reddit.com/r/MachineLearning/comments/1lrc7vh/d\_understanding\_optimal\_batch\_size\_calculation/

arXiv. (2024). *Gemini 1.5：跨越数百万词元上下文解锁多模态理解* [Gemini 1.5: Unlocking multimodal
understanding across millions of tokens of context]. 检索自 2026年2月18日, 从
https://arxiv.org/pdf/2403.05530

Reddit. (n.d.). *[新闻] 谷歌博客文章“什么是长上下文窗口？”指出其背后的深度学习创新* [[N] Google blog post
"What is a long context window?"...]. 检索自 2026年2月18日, 从
https://www.reddit.com/r/MachineLearning/comments/1attgz7/n\_google\_blog\_post\_what\_is\_a\_long\_context\_window/

DataNorth AI. (n.d.). *大语言模型中的上下文长度：它是什么以及为什么重要？* [Context Length in LLMs: What
Is It and Why It Is Important?]. 检索自 2026年2月18日, 从
https://datanorth.ai/blog/context-length

Coconut Mode. (n.d.). *环状注意力机制详解* [Ring Attention Explained]. 检索自 2026年2月18日, 从
https://coconut-mode.com/posts/ring-attention/

YouTube. (n.d.). *环状注意力机制详解：100万上下文长度* [RING Attention explained: 1 Mio Context
Length]. 检索自 2026年2月18日, 从 https://www.youtube.com/watch?v=jTJcP8iyoOM

YouTube Music. (n.d.). *拥有人工智能帕累托前沿——杰夫·迪恩* [Owning the AI Pareto Frontier —
Jeff Dean]. 检索自 2026年2月18日, 从 https://music.youtube.com/podcast/F\_1oDPWxpFQ

Search Engine Land. (n.d.). *谷歌的杰夫·迪恩：AI搜索依赖于经典的排名和检索* [Google's Jeff Dean: AI
Search relies on classic ranking and retrieval]. 检索自 2026年2月18日, 从
https://searchengineland.com/google-jeff-dean-ai-search-classic-ranking-retrieval-469386

36氪. (n.d.). *为什么现代AI能够实现？辛顿与杰夫·迪恩的对话* [Why Can Modern AI Be Achieved? A
Conversation between Hinton and Jeff Dean]. 检索自 2026年2月18日, 从
https://eu.36kr.com/de/p/3601707900977926

Latent.Space. (2026). *AI新闻 — 2026年2月13日* [AI News — Feb 13, 2026]. 检索自
2026年2月18日, 从 https://www.latent.space/feed

arXiv. (2024). *子目标蒸馏：一种改进小型语言代理的方法* [Sub-goal Distillation: A Method to Improve
Small Language Agents]. 检索自 2026年2月18日, 从 https://arxiv.org/html/2405.02749v1

arXiv. (2026). *Chronicals：相比Unsloth提升3.51倍速度的高性能大语言模型微调框架* [Chronicals: A
High-Performance Framework for LLM Fine-Tuning with 3.51x Speedup over Unsloth].
检索自 2026年2月18日, 从 https://arxiv.org/html/2601.02609v1

Hugging Face. (n.d.). *一个失败的实验：无限注意力，以及为什么我们应该继续尝试？* [A failed experiment:
Infini-Attention, and why we should keep trying?]. 检索自 2026年2月18日, 从
https://huggingface.co/blog/infini-attention

arXiv. (2024). *USP：一种用于长上下文生成式AI的统一序列并行方法* [USP: A Unified Sequence Parallelism
Approach for Long Context Generative AI]. 检索自 2026年2月18日, 从
https://arxiv.org/html/2405.07719v5

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 09:07*

## Related Notes

- [[神经形态脉冲大语言模型（NSLLM）：连接AI与神经科学的突破性研究]]
- [[谷歌物理智能体的具身智能：Gemini Robotics 1.5 介绍]]
- [[硅基世界的“缘分”——系统与人工智能携手进化 - Microsoft Research]]
