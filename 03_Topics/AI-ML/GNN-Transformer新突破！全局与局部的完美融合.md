---
title: GNN-Transformer新突破！全局与局部的完美融合
tags:
- ai-ml
- artificial-intelligence
- graph-neural-network
- neural-networks
- neuroscience
- paper
- topology
- transformer
---
> 笔记本: 我的剪贴板  
> 创建时间: 2024-03-27  

---

**图神经网络（GNN）和Transformer的结合是近年来的研究热点。**这类结合不仅能够让两者发挥各自的优势，还能推动模型的创新，提高处理图数据的效率和性能。
具体点讲，通过利用Transformer，我们可以扩展GNN的感受野，包括那些距离中心节点较远的相关节点。相对的，GNN也可以帮助Transformer捕捉复杂的图拓扑信息，并从相邻区域高效地聚合相关节点。
目前，**基于Transformer的GNN和图Transformer是GNN+Transformer的两大关键结合方式**，这其中有不少个人认为很值得学习的成果。比如GNN 嵌套 Transformer 模型**GraphFormers**、仅使用一层全局注意力的简化图Transformer模型**SGFormer**。
本文挑选了**18种****GNN结合Transformer的最新创新方案**和同学们分享，并简单提炼了方法和创新点，配套模型和代码也都整理了。
**需要的同学****扫码添加小享******
**回复“****结合18****”即领**
****
# TransGNN
TransGNN: Harnessing the Collaborative Power of Transformers and Graph Neural Networks for Recommender Systems
**方法：**论文提出了TransGNN模型，通过交替使用Transformer和GNN层来相互增强它们的能力。TransGNN利用Transformer层扩大了接受野，并将信息聚合从边缘中解耦，从而增强了GNN的信息传递能力。
为了有效捕捉图结构信息，作者们设计了细致的位置编码，并将其集成到GNN层中，以将结构知识编码到节点属性中，从而提高了Transformer在图上的性能。
为了提高效率，作者们提出了对Transformer进行最相关节点的采样，并提出了两种高效的样本更新策略，以减少复杂性。
**创新点：** 
- 
 引入了一种新颖的模型TransGNN，其中Transformer和GNN协同合作。Transformer扩大了GNN的感受野，而GNN捕捉关键的结构信息以增强Transformer的性能。 
- 
 为了解决复杂性的挑战，作者引入了一种采样策略以及两种更新相关样本的高效方法。 
- 
 对TransGNN的表达能力和计算复杂度进行了理论分析，揭示了TransGNN相对于具有小额外计算开销的GNN来说具有更大的潜力。
 
# GraphFormers
GraphFormers: GNN-nested Transformers for Representation Learning on Textual Graph
**方法：**论文提出了一种名为GraphFormers的模型架构，用于文本图的表示学习。该模型将GNN和预训练语言模型相结合，通过将GNN嵌入到语言模型的Transformer层中，将文本编码和图聚合融合为一个迭代的流程，从而更准确地理解每个节点的语义。此外，还引入了渐进学习策略，通过对操纵过的数据和原始数据进行逐步训练，增强了模型整合图信息的能力。
**创新点：** 
- 
 图神经网络嵌套Transformer（GraphFormers）：它结合了图神经网络（GNNs）和语言模型。在GraphFormers中，GNN组件与语言模型的Transformer层并行设置，允许文本编码和图聚合的融合。这种架构能够从全局角度精确理解每个节点的语义，从而产生高质量的文本图表示。 
- 
 两阶段渐进学习：为了增强模型整合来自图的信息的能力，作者引入了一种两阶段渐进学习策略。在第一阶段，模型在被操纵的数据上进行训练，其中节点被随机污染，迫使模型利用全部输入节点。在第二阶段，模型在原始数据上训练以适应目标分布。这种渐进学习策略提高了GraphFormers的表示质量。 
- 
 单向图注意力：为了减少不必要的计算，作者引入了单向图注意力。只需要中心节点参考其邻居，而邻居节点保持独立编码。这允许缓存和重用现有邻居的编码结果，显著节省了计算成本。
 
**需要GNN结合transformer创新方案****的同学**
**扫码添加小享****，回复“****结合18****”即领******
 
# Exphormer
EXPHORMER: Sparse Transformers for Graphs
**方法：**本文介绍了一种名为EXPHORMER的框架，用于构建强大且可扩展的图变换器。EXPHORMER采用两种机制：虚拟全局节点和扩展图，这些数学特性使得图变换器的复杂度仅与图的大小成线性关系，并且能够证明所得到的变换器模型具有理想的理论特性。
**创新点：** 
- 
 EXPHORMER是一种新的稀疏图转换器架构，具有可扩展性和竞争力的准确性。 
- 
 EXPHORMER基于两种机制，即虚拟全局节点和扩展图，实现了稀疏注意机制。 
- 
 EXPHORMER的数学特性包括谱扩展、伪随机性和稀疏性，使得图转换器具有与图规模线性复杂度和理想的理论特性。 
- 
 在GraphGPS框架中使用EXPHORMER可以产生在各种图数据集上具有竞争力的实证结果，包括在三个数据集上的最新结果。 
- 
 EXPHORMER可以扩展到比以前的图转换器架构更大的图数据集。
 
# SGFormer
SGFormer: Simplifying and Empowering Transformers for Large-Graph Representations
**方法：**本文提出了一种名为SGFormer的模型，通过一个简单的全局注意力模型来学习大图上的节点表示。该模型具有线性的时间和空间复杂度，能够高效地处理大规模图。
**创新点：** 
- 
 SGFormer模型： 
-  
提出了SGFormer模型，它是一种简化的图Transformer模型，只使用了单层单头的注意力机制。 
-  
SGFormer模型具有线性的时间和空间复杂度，能够有效地处理从数千到数十亿个节点的大规模图数据。 
-  
SGFormer模型在12个图数据集上取得了非常有竞争力的性能，比其他强大的图神经网络和最先进的图Transformer模型都要好。   
- 
 单层注意力模型的表达能力： 
-  
通过将Transformer层与信号去噪问题相连接，证明了单层注意力模型可以产生与多层注意力相同的去噪效果。 
-  
单层注意力模型可以实现最速下降，表明它具备足够的表达能力，能够学习全局信息。  
   
**需要GNN结合transformer创新方案****的同学** 
**扫码添加小享****，回复“****结合18****”即领******

---
## 相关笔记 (AI 自动关联)
- [[GNN联合transformer最新突破！！！]]
- [[GNN图神经网络_非结构化数据分析利器_]]

> [!note]- 可能重复: [[GNN联合transformer最新突破！！！]] (相似度: 94%)
