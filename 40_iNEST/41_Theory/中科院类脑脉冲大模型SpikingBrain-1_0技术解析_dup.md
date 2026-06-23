# 中科院类脑脉冲大模型SpikingBrain-1.0技术解析

- **类型**: link
- **时间**: 2025-10-08 05:21:26
- **标签**: AI链接笔记, 类脑大模型, SpikingBrain, 线性复杂度
- **来源**: https://mp.weixin.qq.com/s/ShIGnt1yTFPHPfzqsmiwCA

## 内容

🧠 **技术背景与创新路径**  
- **现有Transformer瓶颈**：训练开销随序列长度呈平方级增长，推理显存线性增加，导致超长序列处理受限；GPT-3单次训练耗电1287兆瓦时（≈3000辆特斯拉行驶20万英里），大模型单次互动耗电3瓦时（为Google搜索的10倍）。  
- **类脑方案突破**：人脑以20W功耗实现1000亿神经元+1000万亿突触的高效计算，SpikingBrain借鉴生物神经网络“内生复杂性”，融合神经元动力学特性，构建线性/近线性复杂度模型。

🚀 **核心性能指标**  
- **GPU端速度**：1M序列长度TTFT（首Token生成时间）较主流模型提升26.5倍，4M长度保守估计提升超100倍（Qwen基线在4M已无法运行）。  
- **手机CPU端速度**：64k/128k/256k长度下，Decoding速度较Llama3.2同规模模型提升4.04x/7.52x/15.39x，256k时达15.39倍。  
- **数据效率**：仅需2%数据资源即可完成训练，支持150B tokens通用数据训练。

🔬 **技术架构细节**  
- **模型设计**：  
  - 7B版本：线性注意力（LA）+稀疏激活（SWA）的层间混合架构，脉冲编码将激活值转为整数计数或脉冲序列。  
  - 76B版本（激活参数12B）：层内混合架构，集成MoE/FFN模块与动态阈值脉冲化稀疏机制（脉冲稀疏度>69%）。  
- **训练与部署**：适配国产GPU集群，开发Triton/CUDA算子库与模型并行策略，实现全流程自主可控；支持事件驱动编码、自适应稀疏性等脑启发机制。

💡 **应用场景与生态**  
- **超长序列任务**：法律/医学文档分析、DNA序列处理、分子动力学模拟等场景具备效率优势。  
- **开源资源**：已开源7B模型（含中英文技术报告），76B模型开放测试（Demo地址：https://controller-fold-injuries-thick.trycloudflare.com）。

## 原文

总结：

* ##### **SpikingBrain借鉴大脑信息处理机制，具有线性/近线性复杂度，在超长序列上具有显著速度优势**
* ##### **GPU上，1M长度下TTFT 速度相比主流大模型提升26.5x， 4M长度下保守估计速度提升超过100x；**
* ##### **手机CPU端，64k-128k-256k长度下较Llama3.2的同规模模型Decoding速度提升4.04x-7.52x-15.39x**
* ##### **借鉴大脑结构和功能构建新一代AI基础模型和架构的研究路径具有强大潜力。**

当前大模型基本都是Transformer的天下，Scaling law驱动下，不断增加网络规模、算力资源和数据量，提升智能水平。

Transformer架构的基本计算单元为点神经元模型：简单乘加后接非线性函数。这条简单神经元+网络规模拓展的技术路径被称为「基于外生复杂性」的通用智能实现方法。

主流Transformer模型存在固有缺点

* 训练时，开销随序列长度呈平方级增长
* 推理时，显存占用随序列长度线性增加

造成资源消耗，导致超长序列处理能力受限。这种方案存在功耗高可解释性差等问题。

LLM规模越来越大，一次小小的请求就耗费大量算力，这跟生物相差甚远。

GPT-3训练一次的耗电量为**1287兆瓦时**，大概相当于3000辆特斯拉共同开跑、每辆车跑20万英里所耗电量的总和。

Google搜索，每次消耗0.3瓦时的电量，而大模型每次互动的耗电量为3瓦时。

反观人脑，包含约1000亿神经元，约1000万亿突触数量，神经元种类丰富，内部结构复杂，但功耗仅20W左右！而且还能举一反三、自学习。

显然，大模型距离生物大脑还有很远的距离。

于是，非transformer架构的类脑成为一种选项。

2025年9月5日，中科院自动化所李国齐团队推出类脑脉冲大模型“瞬悉1.0”（SpikingBrain-1.0）

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F23e5321020f69e161269b35c4b081988?Expires=1776346124&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=xSAvZjX4ftfLqoJ78XNT1j6NhWE%3D)

瞬悉基于“内生复杂性”理论，融合神经元丰富动力学特性，构建具有生物合理性和计算高效性的神经网络新路径，充分利用了生物神经网络在神经元和神经环路上的结构和功能特性，探索出另一条路径。

研发团队借鉴大脑神经元内部复杂工作机制，提出“基于内生复杂性”大模型构架方式，打造类脑脉冲大模型“瞬悉1.0”，在理论上建立脉冲神经元内生动力学与线性注意力模型之间的联系，揭示现有线性注意力机制是树突计算的特殊简化形式，展示出一条不断提升模型复杂度和性能的新型可行路径。

进一步构建并开源了基于脉冲神经元、具有线性及混合线性复杂度的新型类脑基础模型。

SpikingBrain-1.0基于脉冲神经元构建线性（混合）模型架构，具有线性（SpikingBrain-7B）及近线性复杂度（SpikingBrain-76B，激活参数量12B）的类脑基础模型。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F149641715909025bfe025cbfbbf97096?Expires=1776346124&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=A73n4G6vSVpwiyGZnObFeKJfhr0%3D)

团队构建了与现有大模型兼容的通用模型转换技术和高效训练范式，将标准自注意力机制转换为低秩的线性注意力模型，并适配了脉冲化编码框架。

推理阶段，SpikingBrain利用脉冲编码，将激活值转换为整数计数，方便GPU执行，或转为脉冲序列用于事件驱动的神经形态硬件。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ffca84186d14cfae9a70e295e10dfcfea?Expires=1776346124&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=IOnASj1zZvNjL2ZYFBJmw1RzvhM%3D)

此外，为实现国产算力集群对类脑脉冲大模型的全流程训练和推理支持，团队开发了面向国产GPU集群的高效训练和推理框架、Triton/CUDA 算子库、模型并行策略以及集群通信原语，并在国产千卡GPU算力平台上，完成全流程训练和推理，实现大模型在超长序列推理上数量级的效率和速度提升，展现出构建国产自主可控的新型（非Transformer）大模型架构生态的可行性。

SpikingBrain-1.0在多个性能方面实现突破：实现极低数据量高效训练、实现推理效率数量级提升、构建国产自主可控类脑大模型生态、提出基于动态阈值脉冲化的多尺度稀疏机制。

相比于使用标准注意力和A2A通信的Qwen
baseline，SpikingBrain-1.0-7B在512K和1M长度下TTFT（提交提示到生成第一个Token所需的时间）加速分别达到**13.88**倍和**26.5**倍，且随序列长度和卡数扩展具有几乎恒定的时间开销，在4M长度下Qwen已经无法评测，根据拟合scaling曲线，保守估计速度提升超过**100**倍。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F8ec969999904b4a85ca82fca805e7911?Expires=1776346124&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=RsR%2BUGaplpJI2tqpDbaVmDTsEy4%3D)

团队将压缩到1B的SpikingBrain-1.0，部署到手机端推理框架上，在64k-128k-256k长度下，较Llama3.2的1B模型Decoding速度分别提升4.04x-7.52x-15.39x

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Feb58e60d11c48f5fed33df3698e36ed2?Expires=1776346124&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=ltk2Eic6jEyGKjr%2Fc2w%2FqYM%2Bh98%3D)

这是我国首次提出大规模类脑线性基础模型架构，并首次在国产GPU算力集群上构建类脑脉冲大模型的训练和推理框架。其超长序列处理能力在法律与医学文档分析、复杂多智能体模拟、高能粒子物理实验、DNA序列分析、分子动力学轨迹等超长序列任务建模场景中具有显著的潜在效率优势。

团队开源 SpikingBrain-1.0-7B 模型，并开放 SpikingBrain-1.0-76B测试网址，同步公开中英文技术报告。

Demo：https://controller-fold-injuries-thick.trycloudflare.com/

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fcc2a393f1e70a785ed3325388a833d8c?Expires=1776346124&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=z2KNrGK54dKHKeJ10NoJbWQWu6c%3D)

附录：

* 网络端的试用端口网址：https://controller-fold-injuries-thick.trycloudflare.com
* 中文技术报告网址：https://github.com/BICLab/SpikingBrain-7B/blob/main/SpikingBrain\_Report\_Chi.pdf
* 英文技术报告网址：https://arxiv.org/abs/2509.05276
* 模型代码网址：https://github.com/BICLab/SpikingBrain-7B

技术报告：https://arxiv.org/abs/2509.05276

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F77aa4029e2f8c80e09b8ccaf8a28ca05?Expires=1776346124&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=5%2BbGFQFuue%2BL4mBbbjc6FqTCHe8%3D)

官方介绍：https://www.cas.cn/syky/202509/t20250909\_5081771.shtml

新智元介绍：https://news.qq.com/rain/a/20250908A07Y

---
**Tags:** #NaaS #BrainInspired #Chiplet
