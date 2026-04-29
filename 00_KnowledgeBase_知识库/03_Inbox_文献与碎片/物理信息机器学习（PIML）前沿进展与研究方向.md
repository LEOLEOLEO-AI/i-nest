---
title: "物理信息机器学习（PIML）前沿进展与研究方向"
source: "https://mp.weixin.qq.com/s/SM5xEC5PYTQL02Lx_S0z7g"
created: 2025-11-15
note_id: "1893205840874320808"
tags:
  - "AI链接笔记"
  - "物理信息机器学习(PIML)"
  - "高维复杂系统"
  - "多尺度动力学"
  - "get-笔记"
  - "学术论文"
---

# 物理信息机器学习（PIML）前沿进展与研究方向

## 摘要

🔬 **领域现状与趋势** - PIML作为《Nature》高频出现方向，2025年保持强劲势头，仅综述类论文已发表多篇（如布朗大学GE Karniadakis院士团队成果） - 发展阶段：从概念验证转向广泛应用，新应用场景持续涌现，存在大量开创性工作空间  📈 **研究策略建议** - 快速发文路

## 正文

作为常在《Nature》出没的方向，物理信息机器学习PIML今年依然势头不减，只综述就发表了许多，比如布朗大学GE Karniadakis院士的那篇。

从这些成果来看，PIML如今已从概念验证逐渐走向广泛应用，新的应用场景正不断涌现。这也意味着有大量可探索的空间，更容易做出开创性的工作。

为助力各位快速找到突破口，我建议：如果想快速发文，试试将现有的PIML方法应用到一个新的、还没人用PIML解决过的具体工程问题；如果想发高区，那就在效率、稳健性、泛化能力以及在真实复杂场景下的表现上下功夫。

当然，大家最终是要根据自身情况才能做决定，我这边也准备了12篇PIML前沿论文作为参考，代码已附，希望各位看完可以有所收获。

**扫码添加小享，******回复“********物理机器********”****

免费获取**全部论文+开源代码**

**![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F035bac9c49916132aff7a84198238497?Expires=1780064218&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=E4Rh98QI4o%2BktGx6wjysgwYeofg%3D)**

#### Generative learning for forecasting the dynamics of high-dimensional complex systems

**方法：**论文提出 G-LED
框架，以物理信息机器学习为核心：将高维数据下采样到低维流形，用多头自回归注意力模型演化其动力学，再通过融入物理信息的贝叶斯扩散模型将低维流形映射回高维空间，实现高维复杂系统模拟加速与准确预测。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F8a72cfe1ae55f2adec823859c963a8fa?Expires=1780064218&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=IySNM9lfUUl%2BAN4nLPna24lSbdM%3D)

**创新点：**

* 提出G-LED框架，结合生成学习与自回归注意力机制，可捕捉湍流等复杂多尺度动力学。
* 用非可训练下采样编码器，且将物理信息融入解码器，提升预测物理一致性。
* 以多头自回归注意力模型替代传统模型，优化效率，在多类测试中实现降本与精准预测。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ff6dbdd63c98062877352386619c74c91?Expires=1780064218&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=5fFVRn1xvk1oIk%2B7WvZBOhBBH9s%3D)

#### Physics-informed machine learning

**方法：**论文围绕物理信息机器学习展开，核心方法是将物理定律与机器学习融合：通过观测偏差、归纳偏差、学习偏差三种路径嵌入物理信息，还结合混合方法，依托核方法、经典数值算法建立理论联系，以解决正逆问题、高维系统求解等问题。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F174725acb090e12c7e624156375df1a0?Expires=1780064218&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=VyGBU4w6fuGvt9L2v4e7hSCUq5M%3D)

**创新点：**

* 通过数据、专用网络架构、物理正则损失（如PINNs嵌PDE）三种路径，将物理信息嵌入机器学习。
* 提出混合方法，如结合DeepONets与PINNs、融合高低保真数据，还将神经网络嵌入传统数值方法。
* 建立与核方法、经典数值算法的理论联系，适配小数据、噪声数据及高维系统。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faa441e119308d86d6d4af7184578adc8?Expires=1780064218&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=FaoBtAFXIiEd7Z%2Bwkp7ZQWs6KGk%3D)

**扫码添加小享，******回复“********物理机器********”****

免费获取**全部论文+开源代码**

**![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F035bac9c49916132aff7a84198238497?Expires=1780064218&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=E4Rh98QI4o%2BktGx6wjysgwYeofg%3D)**

#### Kolmogorov n-Widths for Multitask Physics-Informed Machine Learning (PIML) Methods: Towards Robust Metrics

**方法：**论文针对多任务PIML缺客观指标的问题，以Kolmogorov n 宽度为核心方法：先训练 MH-PINNs、PI-DONs 等 PIML
模型得到基函数，再通过双优化算该宽度，还将其作为正则项融入三优化训练，缓解过拟合、提升泛化性，最终在 1D 泊松方程等任务上验证其能有效对比 PIML
架构性能，避免采样误差误导。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F0eeff13fa10c57db75f6f013c1cc0918?Expires=1780064218&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=SFGhtOtWuWQVLbdm5%2BywH9pWm%2B0%3D)

**创新点：**

* 用Kolmogorov n宽度作多任务PIML的评估指标，通过双优化算宽度，量化模型解空间近似能力，避免采样误差误导。
* 将Kolmogorov n宽度作为正则项，融入三优化训练，缓解PIML模型过拟合，提升泛化性。
* 在1D泊松方程等任务验证该宽度能对比PIML架构、激活函数性能，明确网络参数对泛化的影响。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F4d636f679eced6e4d4c90ce8c8022e0d?Expires=1780064218&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=Uh6ftm2YHvDQyHO7PihJrlq980Y%3D)

#### Separable Physics-Informed DeepONet: Breaking the Curse of Dimensionality in Physics-Informed Machine Learning

**方法：**论文针对传统PINNs求解含间断/多尺度PDE的精度与稳定性问题，提出改进的物理信息机器学习方法：将熵守恒、TVD等物理准则融入模型，结合自适应采样与多尺度网络，保留自动微分算PDE残差、融数据与物理约束优化的核心范式，在高超声速流动等场景验证其提升物理一致性与预测性能的效果。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F7c6984cdee609fca9f5daca31001aaba?Expires=1780064218&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=eBPSei4S26GPp8pZHP%2F6a6JGY%2Fw%3D)

**创新点：**

* 提出Sep-PI-DeepONet，拆分PI-DeepONet为独立子网络实现坐标分解，将主干网络传播次数从降为，突破高维PDE维度灾难。
* 用前向模式AD算PDE梯度项，雅可比矩阵规模大幅缩减，计算成本随离散密度与维度线性增长。
* 在多类基准测试中，Sep-PI-DeepONet精度相当传统PI-DeepONet，训练时间降两个数量级，还能处理高维PDE。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F90a23683754fbd3de069aaeebab69cee?Expires=1780064218&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=53ux6%2BhkHiF%2FpRPCvAlyVhZfnXs%3D)

**扫码添加小享，******回复“********物理机器********”****

免费获取**全部论文+开源代码**

**![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F035bac9c49916132aff7a84198238497?Expires=1780064218&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=E4Rh98QI4o%2BktGx6wjysgwYeofg%3D)**

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 10:16*