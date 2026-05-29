---
title: "北京大学研发可重构多功能集成光子计算芯片：突破多模态AI任务硬件瓶颈"
source: "https://mp.weixin.qq.com/s/mQmGmx2WeJE4cSVM-69N2A"
created: 2025-09-01
note_id: "1886263844432665688"
tags:
  - "AI链接笔记"
  - "集成光子计算芯片"
  - "可重构神经网络"
  - "多模态AI硬件"
  - "get-笔记"
  - "AI研究"
---

# 北京大学研发可重构多功能集成光子计算芯片：突破多模态AI任务硬件瓶颈

## 摘要

🔬 **核心技术突破：统一架构下的神经网络原位可重构**   北京大学团队开发的新型光子计算芯片，通过交叉波导耦合微环组件（MRR）与马赫-曾德尔干涉仪（MZI）阵列协同设计，实现三大神经网络的原位动态切换：   - **全连接神经网络（FCNN）**：利用双端口输入与多波长光频梳，完成权重乘法与偏

## 正文

关键词：集成光子计算、可重构神经网络、光子硬件

北京大学研究团队开发了一种新型集成光子计算芯片，通过算法-硬件协同设计策略，在统一结构中实现了全连接、卷积和循环神经网络的原位可重构，支持静态和动态时间任务，实验验证了其在图像分类、情感分析和语音识别中的高效性能。该芯片为芯片级多功能光子信息处理提供了高效解决方案，计算效率高达2.45 TOPS/mm²。

相关成果以“Reconfigurable versatile integrated photonic computing chip”为题，发表在《eLight》期刊上。这项工作不仅解决了传统光子组件难以实现基础计算单元突破的难题，还为集成光子平台的多功能计算开辟了新路径，标志着光子计算向实际应用迈出了关键一步。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F85dbf83cccd9f46cb73ddf4427abd0d0?Expires=1780068089&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=LBj88vHLjlo4gUptcKORVMi4RtM%3D)![图片]()![图片]()![图片]()![图片]()

统一光子配置的多模型重构

该芯片的核心在于释放紧凑型交叉波导耦合微环组件的内在功能，通过统一的光子配置实现跨不同神经网络模型的原位可重构性。

团队利用交叉波导的两个输入端口和对应的下端口、通过端口，结合不同波长的光频梳，实现权重乘法和偏置加法的无缝集成。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F0a3e7cb228515ba10eb0d1caefcb1e5c?Expires=1780068089&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=zg5sOFRYAStDs3Fa3I%2FVpFKGaGM%3D)

例如，在全连接神经网络（FCNN）中，输入信息向量通过上输入端口编码注入MRR阵列，权重由电控微加热器精确调谐，而偏置则通过左端口引入非谐振波长，直接在下端口输出加权求和结果。对于卷积神经网络（CNN），MRR阵列可灵活实现不同尺寸的卷积核和多通道融合，如1×1卷积用于降维和跨通道融合，而无需额外结构调整。

在光子门控循环神经网络（PGRNN）中，多层MRR阵列间引入MZI作为重置门，调控隐藏状态的比例，利用MRR的不同自由光谱范围（FSR）同时调制当前和先前时间步的信息，避免信号串扰。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F60a9dc58aa84ae7bb4f4571d954870c8?Expires=1780068089&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=jlDAyAXWNmUAdq5KIjpE%2B33LINk%3D)

这种设计不仅支持静态任务如图像分类，还能处理动态序列如文本分析，确保网络在统一架构下无缝切换模型，而不依赖混合配置。

多模态任务的实验验证

为验证芯片的适应性和性能，团队开展了多项实验任务。

首先，在图像分类上，采用Inception模型结合CNN和FCNN，在MNIST数据集上实现了92.93%的测试准确率，在更复杂的CIFAR-10数据集上达到了56.57%，根均方误差（RMSE）低至0.0261，证明了卷积操作的精确性。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fd37f07bc9aadf5ce5d249fcc6af2d6e8?Expires=1780068089&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=gSy6rA7y0LiuGicOg1qJrBr9p88%3D)

其次，针对情感分析，使用PGRNN和FCNN处理IMDB数据集，训练准确率高达99.23%，测试准确率为80.81%，成功捕捉文本序列中的长程依赖。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F6c83b903521c0f93c375f1beb0ddeffd?Expires=1780068089&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=5u7fiYVX0JnXTs2BV5%2FlXM1P1vQ%3D)

最后，在语音识别任务中，扩展架构整合CNN、PGRNN和FCNN，对LJ-Speech数据集进行处理，通过短时傅里叶变换（STFT）和连接主义时间分类（CTC）方法，实现了0.55的测试词错误率（WER），即使在复杂音频中也能生成可解读的文本输出。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fdec97089f296a82e74b7d0480aacd060?Expires=1780068089&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=EY%2Fpljj4eU6tZBCfn7rzBFpyDQg%3D)

这些结果突显了芯片在多模态任务中的灵活性和可扩展性，实验中孤子微梳的稳定输出确保了长达1小时的可靠计算。

光子计算的无限潜力

这项研究克服了集成光子平台上执行多功能计算的挑战，为下一代光子计算平台的发展铺平了道路。

通过高效的芯片集成多功能光子信息处理，该工作不仅提升了AI任务的能效，还为大规模模型和多模态学习提供了潜力巨大的解决方案。

未来，随着加工技术的进步，这种可重构光子芯片有望进一步扩展到更复杂的神经网络，推动光子硬件从实验室走向实际应用。

![图片]()![图片]()![图片]()![图片]()

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F47f4990520ad70cfff8ba3f9ceed2470?Expires=1780068089&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=uOKHxZrGwlvEY%2F%2BZY8nOQ8%2FRN%2BY%3D)![图片]()![图片]()![图片]()![图片]()

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 11:21*