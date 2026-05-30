---
title: 基于宽带隙Ga₂O₃的多功能光电忆阻器：人工突触与神经形态计算应用
tags:
- chip-hardware
- chiplet
- neural-networks
- neuroscience
- plasticity
- semiconductor
- simulation
- synapse
---
- **类型**: link
- **时间**: 2025-09-02 07:29:11
- **标签**: AI链接笔记, 神经形态计算, 光电忆阻器, Ga₂O₃宽带隙材料
- **来源**: https://mp.weixin.qq.com/s/JnJ_QkC45UxRDEsCw_s_0w

## 内容

🔬 **核心器件与功能集成**  
- **结构**：Ag/Ga₂O₃/Pt三层结构忆阻器，集成紫外光传感、数据存储、逻辑运算和神经形态计算功能  
- **多电平存储**：通过调节电流顺度（Icc）实现4种低阻态（LRS），结合4种紫外光（254 nm）强度实现4种高阻态（HRS），共8种电阻状态（3位数据存储）  
- **逻辑门实现**：以电压极性和紫外光为输入，电流为输出  
  - 正偏压+紫外光 → "或"逻辑门  
  - 负偏压+紫外光 → "与"逻辑门  

📊 **关键特性与实验数据**  
![器件特性曲线](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fd9f7125939305efc62bd731ce6d2db99?Expires=1776344995&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=BnwvKjlqdesaQaBqcaYL%2F0bccbk%3D&x-oss-process=image%2Fresize%2Cm_lfit%2Cw_720%2Ch_3240)  
1. **电阻开关性能**  
   - LRS电阻值稳定性高，HRS通过紫外光强度调控（0.8-1.7 mW/cm²）  
   - 8种电阻状态保持特性良好，循环测试80次后性能稳定  

2. **突触功能模拟**  
   - 实现脉冲易化（PPF）、峰值强度/数量/时间/频率依赖可塑性（SIDP/SNDP/STDP/SFDP）  
   - 光脉冲增强（STM→LTM转化）和电脉冲抑制的双极特性  

🧠 **神经形态计算应用**  
![学习-遗忘-再学习行为](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F0b84c7c98a17383b17a2aac6034553df?Expires=1776344995&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=WvfOJJDwkRboEAq7zP02ZUjWxWo%3D&x-oss-process=image%2Fresize%2Cm_lfit%2Cw_720%2Ch_3240)  
- **学习经验行为**：紫外光脉冲（254 nm, 1.8 mW/cm²）刺激下呈现"学习-遗忘-再学习"特征，再学习效率提升  
- **图像识别性能**：基于50组光/电脉冲调控的电导值作为权重，MNIST数据集训练人工神经网络，最高识别精度达90.7%

## 原文

**![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F7a8fa07bfd9fc6115adf5e8551e516e3?Expires=1776346158&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=TTnWt9%2B6vQKylkhIwNNfoTJ5QLo%3D)**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F589fc16a3e03566042e5d8126e0c6da2?Expires=1776346158&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=fCK5x2XOxBe%2BKErQmDsEmXCcv5k%3D)

**摘要：**

光电记忆电阻器具有数据存储和模拟人类视觉感知的能力。它们在神经形态视觉系统（NVs）中有很大的应用前景。本研究介绍了一种非晶宽禁带Ga2O3光电突触记忆电阻器，通过调节电流顺度（Icc）和利用可变紫外（UV-254 nm）光强实现3位数据存储。忆阻器辅助逻辑（MAGIC）中的“与”和“或”逻辑门是利用电压极性和紫外光作为输入信号来实现的。该装置还表现出高度稳定的突触特性，如对脉冲易化（PPF）、峰值强度依赖可塑性（SIDP）、峰值数量依赖可塑性（SNDP）、峰值时间依赖可塑性（STDP）、峰值频率依赖可塑性（SFDP）和学习经验行为。最后，当集成到人工神经网络（ANN）时，Ag/Ga2O3/Pt忆阻器件模拟了光脉冲增强和电脉冲抑制，具有较高的模式精度（90.7%）。具有多功能特性的单记忆细胞在光电记忆存储、神经形态计算和人工视觉感知等领域具有广阔的应用前景。

**引言：**

在这项研究中，我们制作了具有Ag/Ga2O3/Pt器件结构的宽带隙Ga2O3薄膜电阻随机存取存储器（rram）。该系统将紫外光传感器、数据存储、逻辑门和神经形态计算集成在一个设备中。我们调整了Icc以实现四个低电阻状态（LRS）。应用四种不同强度的紫外线（254 nm）， Icc为1 mA，可实现四种不同的高阻状态（HRS）。LRS的电阻值保持相当稳定。基于上述两种方法，我们已经确定了八种不同的电阻状态，使器件能够实现多电平电阻开关（MRS）能力。有趣的是，当Icc调整到1µA时，器件表现出一致的波动性。随后，由于该忆阻器的双极特性，当受到负偏置电压而不是正偏置电压时，器件表现出降低的电导。因此，我们认为254 nm光源和偏置电压是器件的两个输入，电流作为输出。正偏置电压用于实现“或”逻辑门。当施加负偏置电压时，实现“与”逻辑门。此外，用一系列紫外光脉冲照射该装置以实现PPF、SIDP、SNDP、STDP和SFDP等突触功能。成功地获得了学习-遗忘-再学习的高级神经形态学特征。在获得50组光脉冲增强和50组电脉冲抑制的电导值后，将电导值作为权值，并将修改后的美国国家标准与技术研究院（MNIST）数据集作为人工神经网络的训练输入。结果表明，该方法的图像识别率最高可达90.7%。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fd9f7125939305efc62bd731ce6d2db99?Expires=1776346158&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=fgbMOS3E2ZtXnOwLqwXIWSjw4ks%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ff33962c22a78d84881d2b8e830a4ea7d?Expires=1776346158&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=ZSlp%2BIIAqtaUZQAjmkbUZh1D%2Bfo%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F0b84c7c98a17383b17a2aac6034553df?Expires=1776346158&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=YieOACKitiPO0cXD2iO76GX9wew%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F8d01315a836e01b35c3ca33eeee40eca?Expires=1776346158&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=uYoChCjNHhxKg9TF0UvqjzXu%2Bl8%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fe7b455b38a89e320c529e45443db01c6?Expires=1776346158&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=Tk7ofpKkp9TyZ7wCUe9PlyZiUh0%3D)

**结论：**

展示了一种集成数据存储、光突触、逻辑门和神经形态计算的基于ga2o3的宽带隙光电突触忆阻器。通过改变Icc和紫外光强度（254 nm）来研究该器件的MRS能力。通过改变输入电压的极性，忆阻器可以实现与与或两个逻辑门的功能。该器件还显示出一致的突触特性，如PPF、SIDP、SNDP、STDP和SFDP。当暴露在紫外线下时，该装置显示出先进的突触特征，如LTM， STM和学习-遗忘-再学习。此外，该装置在人工神经网络仿真中具有较高的模式精度（90.7%）。光电记忆存储和突触学习行为的集成功能使其成为未来内存计算系统的潜在候选者。

标题：Versatile optoelectronic memristor based on wide-bandgap Ga2O3 for artificial synapses and neuromorphic computing

链接： https://doi.org/10.1038/s41377-025-01773-6（阅读原文直达链接）

如有任何问题，欢迎留言私信！！

---
**Tags:** [[BrainInspired]] [[Chiplet]]
