---
title: Nature论文解读：不断发展的忆阻器产业（2025）
tags:
- chip
- chiplet
- literature
- neuron
- neuroscience
- paper
---
- **类型**: link
- **时间**: 2025-09-22 11:43:17
- **标签**: AI链接笔记, 忆阻器产业, 存算一体（IMC）, RRAM/PCM/MRAM
- **来源**: https://mp.weixin.qq.com/s/JmW4km8p_TdI7CsDmsbuPg

## 内容

🔬 **论文核心信息**  
- **发表信息**：新加坡国立大学Mario Lanza团队，2025年4月16日发表于《Nature》（观点文章）  
- **作者阵容**：涵盖忆阻器领域"半壁江山"的权威学者  
- **核心结论**：系统分析忆阻器商业化现状与技术前景，预测2029年市场规模达30亿美元  

💡 **技术洞察**  
1. **忆阻器价值定位**  
   - 解决传统计算"存储-计算分离"瓶颈，模拟生物电子功能  
   - 性能优势：接近DRAM的速度、远超SRAM的密度、非易失性（断电不丢失数据）  

2. **三大技术路线对比**  
   - **RRAM（电阻式）**：1962年提出机制，2024年台积电推出22nm IMC芯片  
   - **PCM（相变）**：1971年首次演示阵列，2025年意法半导体计划量产18nm存算一体MCU  
   - **MRAM（磁性）**：基于GMR效应（1984年发现），三星目标2027年实现5nm工艺  

3. **下一代计算架构**  
   - **存算一体（IMC）**：图2a显示多IMC核心集成于CPU，突破传统总线瓶颈  
   - **混合计算模式**：RRAM处理低精度任务，数字计算负责高精度需求  

📊 **市场与应用数据**  
- **市场构成预测**（2029年）：  
  - 微控制器（MCUs）占81%主导地位  
  - 存算一体（IMC）等AI应用为核心增长点  
- **商业化里程碑**：  
  - 2024年：IBM推出14nm PCM存算芯片（16 Mb），台积电量产22nm RRAM-SRAM混合芯片  
  - 2025年：意法半导体计划推出18nm PCM自动MCU  

🔍 **关键图表解析**  
- **图1b（存储技术权衡图）**：忆阻器填补SRAM（高速高成本）与NAND FLASH（低速低成本）的性能空白  
- **图2c（芯片剖面电镜）**：忆阻器单元可集成于CMOS芯片金属布线层（BEOL）  
- **图3（技术路线图）**：2015年后商业化进程显著加速，2024-2025年进入量产爆发期

## 原文

今天来学习新加坡国立大学Mario Lanza老师团队于2025年4月16日发表的一篇Nature论文：The growing memristor
industry 不断发展的忆阻器产业。这篇观点文章作者列表集齐了忆阻器的半壁江山。

### ****需要做神经形态应用的老师欢迎后台获取联系方式，图像识别检测/储备池/SNN/光谱仪/神经元/树突/轨迹衰减......各类任务均可实现****

### 

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fea730295300581983a07937563b0f120?Expires=1776346148&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=kKdXcrOTADf9Xtrlm4DZ8eAzzws%3D)

## 背景介绍

    忆阻器作为两端非易失性存储器件，能够模拟基本的生物电子功能，为突破存储与计算分离的瓶颈提供了新的解决方案

## 一句话解释

**本文系统分析了忆阻器产业的商业化现状和技术前景，揭示了PCM、RRAM和MRAM三大技术路线如何从学术研究走向产业应用，并预测2029年市场规模将达30亿美元**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F25a3d1cdd73f35ad470a96cbc9e6977a?Expires=1776346148&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=%2F1So%2Fh4fP2mScf1cWuSOZSCkwgI%3D)

图 1：基于晶体管的传统数据存储与计算  

图1a 描绘了经典的计算机架构，展示了计算模块（左侧CPU）和存储模块（右侧DRAM和NAND
FLASH）是物理分离的。数据必须通过地址/控制/数据总线在两者之间来回穿梭。 图1b
是一张存储技术的性能-密度-成本权衡图。SRAM速度最快，但密度低且价格昂贵；NAND
FLASH最便宜、密度最高，但速度最慢。图中虚线圈出的忆阻器区域，它有望填补现有存储器之间的空白，提供接近DRAM的速度、远超SRAM的密度和非易失性（断电不丢数据）的特性，潜力巨大。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F011eecadb8d0a667cce8be00c6dd17ea?Expires=1776346148&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=DweKDbfSB0TzGnJPJFfDssaCxw0%3D)

图 2：用于嵌入式存储和存算一体的忆阻器技术  

图2a 展示了基于忆阻器的下一代计算架构。与图1a最大的不同是，图中出现了多个存算一体（IMC）核心。图2b
展示了三种主流忆阻器（相变、金属氧化物、磁性）的工作原理，即通过电学手段改变材料状态，实现高低两种电阻的切换，从而存储信息。 图2c
芯片剖面电镜图，展示了忆阻器单元被完美地集成在CMOS芯片的金属布线层（BEOL）之间。图2d 交叉阵列。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F1b4d98f3cd7763eb6c9bd10aa0930274?Expires=1776346148&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=vOjQks2JLn616CdJJFXH%2B%2FCm9xU%3D)

图 3：忆阻器技术的历史与未来里程碑  

展示了忆阻器技术（RRAM, PCM,
MRAM）的发展历程，从早期理论发现到如今各大厂商（三星、Intel、台积电等）的商业化产品，再到对未来的展望（如2027年实现5nm
MRAM）。我们可以清晰地看到，自2015年以来，商业化进程显著加速，这印证了文章的观点：忆阻器发展的“正确时机”已经到来 。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faad33ee4c985ee32692bc0b43382e471?Expires=1776346148&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=H3p07os81shOixnsRUnbp7IzRxI%3D)

图 4：忆阻器技术的市场前景与性能对比  

图4a 从速度、能耗、面积、耐久性等多个维度对比了三种主流忆阻器技术，需要根据具体应用场景进行选择。 图4b
对忆阻器市场规模做出了预测，嵌入式应用的增长远超独立存储，预计到2029年市场规模将突破30亿美元。 图4c
揭示了未来的市场构成，其中微控制器（MCUs）将占据81%的绝对主导地位，而存算一体（IMC）等AI相关应用也将成为重要的增长点。

点评：

    通过当前多家公司投入研发的新型存储（对标eFlash）的结果来看，没有明显性能优势，反而有很多问题难以解

    未来忆阻器的可能是混合计算，RRAM承担对精度要求不高的任务，数字计算承担精度高的任务。

---
**Tags:** [[BrainInspired]] CST [[Chiplet]]
