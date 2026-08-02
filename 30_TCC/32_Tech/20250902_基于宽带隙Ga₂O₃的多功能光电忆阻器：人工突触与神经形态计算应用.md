---
provenance: external
---

---
title: "基于宽带隙Ga₂O₃的多功能光电忆阻器：人工突触与神经形态计算应用"
date: 2025-09-02 07:29:11
source: "????"
note_id: 1886316727290050104
note_type: link
tags: [AI链接笔记, 神经形态计算, 光电忆阻器, Ga₂O₃宽带隙材料]
source: getnote---

# 基于宽带隙Ga₂O₃的多功能光电忆阻器：人工突触与神经形态计算应用

🔬 **核心器件与功能集成**  
- **结构**：Ag/Ga₂O₃/Pt三层结构忆阻器，集成紫外光传感、数据存储、逻辑运算和神经形态计算功能  
- **多电平存储**：通过调节电流顺度（Icc）实现4种低阻态（LRS），结合4种紫外光（254 nm）强度实现4种高阻态（HRS），共8种电阻状态（3位数据存储）  
- **逻辑门实现**：以电压极性和紫外光为输入，电流为输出  
  - 正偏压+紫外光 → "或"逻辑门  
  - 负偏压+紫外光 → "与"逻辑门  

📊 **关键特性与实验数据**  
![器件特性曲线](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fd9f7125939305efc62bd731ce6d2db99?Expires=1785911751&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=eJR%2F5t8ZEWOF6dBSj78fKLDkS8g%3D&x-oss-process=image%2Fresize%2Cm_lfit%2Cw_720%2Ch_3240)  
1. **电阻开关性能**  
   - LRS电阻值稳定性高，HRS通过紫外光强度调控（0.8-1.7 mW/cm²）  
   - 8种电阻状态保持特性良好，循环测试80次后性能稳定  

2. **突触功能模拟**  
   - 实现脉冲易化（PPF）、峰值强度/数量/时间/频率依赖可塑性（SIDP/SNDP/STDP/SFDP）  
   - 光脉冲增强（STM→LTM转化）和电脉冲抑制的双极特性  

🧠 **神经形态计算应用**  
![学习-遗忘-再学习行为](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F0b84c7c98a17383b17a2aac6034553df?Expires=1785911751&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=WCZQN4Z%2ByJZL9R01kaUfHgXqpIw%3D&x-oss-process=image%2Fresize%2Cm_lfit%2Cw_720%2Ch_3240)  
- **学习经验行为**：紫外光脉冲（254 nm, 1.8 mW/cm²）刺激下呈现"学习-遗忘-再学习"特征，再学习效率提升  
- **图像识别性能**：基于50组光/电脉冲调控的电导值作为权重，MNIST数据集训练人工神经网络，最高识别精度达90.7%
