---
title: "汉阳大学2025 Nature Communications论文解析：动态视觉传感的传感器内光电处理技术"
source: "https://mp.weixin.qq.com/s/H7XuMcpUNOHIioWTtIl2nA"
created: 2025-12-27
note_id: "1897100616002623968"
tags:
  - "AI链接笔记"
  - "神经形态计算"
  - "动态视觉传感"
  - "传感器内处理"
  - "get-笔记"
  - "学术论文"
---

# 汉阳大学2025 Nature Communications论文解析：动态视觉传感的传感器内光电处理技术

## 摘要

### **📚 研究背景与核心问题**  **动态视觉感知的技术瓶颈** - **传统帧相机**：数据冗余巨大，无法高效捕捉瞬时变化。 - **新兴事件相机**：响应速度快，但丢失历史记忆，无法直接保留运动轨迹。 - **核心挑战**：如何同时实现**瞬时事件捕捉**与**运动历史记忆**的高效融合

## 正文

今天来学习汉阳大学Won Il Park团队2025年12月27日发表的一篇Nature Communications论文： In-sensor
analog optoelectronic processing of concurrent event and memory signals for
dynamic vision sensing 用于动态视觉传感的并发事件与记忆信号传感器内模拟光电处理 DOI:
10.1038/s41467-025-68013-8

**需要做神经形态应用的老师欢迎后台获取联系方式，CNN/储备池/SNN/光谱仪/神经元/树突/轨迹衰减......各类任务均可实现**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Feb4cda3703d62b569ba074fa1ce51496?Expires=1780062098&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=wzFa7je7f8TzvmPJcuenX8MlCJc%3D)

背景介绍  

    高效动态视觉感知既需要捕捉瞬时变化也需要掌握运动历史轨迹。传统帧相机数据冗余巨大，而新兴事件相机虽响应快却丢失了历史记忆，无法直接保留运动轨迹。

一句话解释

 
  利用硅酸盐长余辉与石榴石快响应的材料特性差异构建双通道差分像素，通过模拟域物理减法直接提取代表瞬时变化的电压尖峰和代表运动历史的电压长尾，在传感器端实现无需ADC参与的存算一体。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F8bb06daa0d546b109ad725cc4188cf29?Expires=1780062098&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=Qa7NKMVRQ0VYMwlPvfLOTdrdL1E%3D)

图1：传感器内信号处理范式对比  

图1a展示动态视觉的三种数据形态，即原始帧、仅含变化的事件帧及含运动拖影的记忆帧。图1b揭示传统DVS处理痛点，即为获得记忆信号必须将模拟事件数字化并存入缓存积分，造成高延迟。图1c展示本文核心架构，像素内集成快慢双光电通道，通过模拟差分电路直接输出A减B的电压，利用A通道的长余辉与B通道的快响应，物理级生成瞬时尖峰与记忆长尾。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F3310900749a0cfac4f0353889c4fb50d?Expires=1780062098&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=CCxZ0rlTqESgOTMxSFC%2FOILMPB0%3D)

图2：AEMS传感器工作原理

图2a像素电路，SensorA涂覆有余辉的硅酸盐，SensorB涂覆无余辉的石榴石，两者接差分放大器。图2b的光致发光曲线证实硅酸盐具备毫秒级长余辉而石榴石为微秒级快衰减。图2c实测波形显示，光照突变瞬间因响应速度差产生尖峰，随后因余辉差保留缓慢衰减的尾部。图2f通过线性储备池模型拟合实验数据，证明该物理器件天然具备递归神经网络计算特性，记忆衰减因子与模型高度吻合。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F70cf1fe957d7b40bb5f76fea5958f027?Expires=1780062098&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=gndvltZlgdX4sIAkWwK23V51rHs%3D)

图3：真实视频事件与记忆重构  

图3b展示单像素电压波形，复杂动作下传感器稳定输出清晰尖峰与长尾。图3c的时空热力图以红蓝颜色反映模拟信号随时间的连续变化。图3d展示重构效果，上方事件帧勾勒轮廓，下方记忆帧保留轨迹，全过程无数字计算。图3e在复杂街景测试中，静态背景因差分被抵消，仅保留行人车辆轨迹，验证了抗干扰能力。

点评：

    这是一篇1+1+1+1<4的经典操作，想法是好的，叠buff自然就有市场，实现方法堪称教科书式整活失败案例。

    看看信号链条就知道了：UV LED → 荧光粉下转换 → 可见光 → 硅PD → TIA → 差分器 → 输出。

   
各位老师手头上应该最不缺的就是那些做的千奇百怪有着快慢不同的光电探测器![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F510a6d8cd976bae8b2c2e952602e8fc4?Expires=1780062098&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=yAfEtdz%2Fd8ON6LMu1ohzkQp31iA%3D)，那么赶紧安排下一篇，整两个光电探测器，响应速度不同就能做整个工作了，同样事件相机+轨迹衰减+存算一体，最后对比个能效，怒减99%，last
author给点力，轻松nc

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 09:41*

## Related Notes

- [[神经形态脉冲大语言模型（NSLLM）：连接AI与神经科学的突破性研究]]
- [[北京大学ISSCC 2025高抗噪语音活动检测芯片研究]]
- [[AutoResearchClaw：全自动端到端AI科研智能体深度解析]]
