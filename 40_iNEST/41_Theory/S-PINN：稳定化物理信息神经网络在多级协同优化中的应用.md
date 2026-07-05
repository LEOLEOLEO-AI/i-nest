---
title: "S-PINN：稳定化物理信息神经网络在多级协同优化中的应用"
source: "https://mp.weixin.qq.com/s/-ijdQ2OFirIpm_u69kmiNQ"
created: 2025-09-16
note_id: "1887613934115498936"
tags:
  - "AI链接笔记"
  - "S-PINN"
  - "物理信息神经网络"
  - "多级协同优化"
  - "get-笔记"
  - "AI研究"
---

# S-PINN：稳定化物理信息神经网络在多级协同优化中的应用

## 摘要

🔬 **研究背景与挑战**   物理信息神经网络（PINNs）因能融合物理定律与数据驱动模型而广泛应用，但多级协同优化中存在三大核心冲突：   1. **噪声数据与物理方程冲突**：观测噪声导致数据残差与PDE残差无法同时收敛   2. **逐点残差矛盾**：不同配点处的PDE残差相互抵消，降低全局

## 正文

点击上方蓝色文字关注↑↑↑↑↑

**![1757945968729.png](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fd3dcc8db94466ca7e1b4d4f79a43e1e1?Expires=1780067034&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=zDL%2FP3IHUVZS7bCnnZex6EJJqiA%3D)**

**摘要**

> ![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fcb42864c477c96825e8af1f190d0e92b?Expires=1780067034&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=nhL6wWU%2FwyTMQORVbTfBtSQWPpo%3D)
>
> 本文**提出了一种新型稳定化物理信息神经网络（S-PINN），用于缓解物理信息神经网络（PINNs）中多级协同优化所引发的多重冲突。**S-PINN
> 在整个流体域内建立守恒子域，并在每个子域中对守恒量残差进行高斯积分，以此准确计算质量与动量的残差。基于此构建的损失函数，通过最小化守恒误差来训练神经网络，从而获得稳定且高精度的流体动力学预测结果。以
> Navier-Stokes 方程为例的训练与结果表明，**S-PINN
> 能够有效缓解噪声数据与基本方程、逐点配点残差之间的冲突，增强了流场的局部与全局守恒特性。该方法在提高预测精度、加快收敛速度和训练稳定性的同时，避免了过拟合问题。**尽管
> S-PINN 在子域积分中引入了额外计算开销，但数值实验表明，在相同的训练预算下，S-PINN 始终优于传统 PINN 方法。由此，S-PINN
> 为智能流体动力学的多样化应用提供了一条具有前景的途径。
>
> ---
>
> **0****1**
>
> **研究背景**
>
> **近年来，物理信息神经网络（PINNs）因其在偏微分方程（PDEs）建模中的潜力而备受关注。然而，****多级协同优化常导致训练过程中的冲突，如观测数据与物理约束之间的不一致，进而影响模型的收敛性与预测精度。**
>
> 本文提出了一种稳定化物理信息神经网络（S-PINN），通过在流体域中引入**守恒子域（conservation
> subdomains）**，并在每个子域内进行高斯积分来计算质量与动量残差，从而构建新的损失函数。该方法在保持局部与整体守恒的同时，有效缓解了多级优化中的冲突，提升了训练的稳定性和预测精度。

---

**0****2**

**传统 PINN 的挑战与冲突机制**

**PINN 的损失函数通常由四部分组成：**

* **初始条件残差**
* **边界条件残差**
* **PDE 残差**
* **数据残差**

![1757946338439.png](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fb187660af5fe6929371914ac4b1b6de9?Expires=1780067034&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=56Wj3xoKNPk1GKqCyCYUqP1Sopw%3D)![1757946382683.png](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F4da85a3002406e6493a7163e4d7432e2?Expires=1780067034&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=DRhFYIHfmSc0D2ZcqsKYoggSvmg%3D)

**其优化过程存在以下挑战：**

1. **噪声观测与 PDE 的冲突**（图 3）  
   当观测数据包含噪声时，数据残差与 PDE 残差无法同时趋近于零，导致训练过程中出现震荡。
2. **不同 collocation 点之间的冲突**  
   PDE 残差在不同点可能相互矛盾，难以保证全域一致性。

这一问题在复杂流场（如湍流、涡脱落等）中尤为严重，表现为收敛慢、预测不稳健。

![image.png](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F6b7594f710a53c21f2d44c4fe5527547?Expires=1780067034&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=APcObVrrf1SLlJJ7sTFy%2Bazt7Ec%3D)

---

**0****3**

**S-PINN 的核心思路与方法改**

**子域构建**

将计算域划分为多个子域，每个子域作为一个局部积分区域。通过高斯积分计算局部守恒误差。（图 15）

**新的损失函数设计**

基于子域残差构造损失函数，而不是仅依赖单点残差，从而增强整体守恒性。

**与其他 PINN 变体的兼容性**

部分增强型 PINN 方法（如 gPINN、硬约束投影 HCP 等）可以直接嵌入 S-PINN 框架，进一步提升性能。

![1757946844081.png](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F6e99ee9b7aa6a9c4b3569c1615a89149?Expires=1780067034&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=zyduzi0iQjK7vXNwpLllEMV0gSo%3D)![1757946510356.png](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F3a505ded8e3b017ec536be184f6cffe2?Expires=1780067034&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=F%2BrJtnP04sp5iWmjZE5dRb2t%2FXs%3D)

---

**0****4**

**实验结果与分析**

**Poisson 方程测试**

* **预测精度对比**（图 12–13）  
  S-PINN 在高梯度区域与边界层处表现最优，误差分布更加均匀。
* **守恒性对比**（图 14）  
  S-PINN 残差始终维持在低水平，而传统 PINN 出现局部震荡。
* **训练效率**（表 3）  
  尽管 S-PINN 增加了积分计算，但整体训练时间与 PINN (CPs) 接近，且预测精度更高。

## 1757946580976.png

**Burger 方程**

* S-PINN 在捕捉非线性波动方面表现更优，能够在噪声条件下保持稳定收敛。

**三维热扩散问题**

* **误差收敛曲线**（图 26）  
  S-PINN 在整个训练过程中 L2 误差更低。
* **训练时间对比**（表 7）  
  S-PINN 训练时间略高，但在相同预算下预测效果最佳。

### 1757946905208.png

**二维与三维驱动方腔流动**

* **流场预测对比**（图 28–30）  
  S-PINN 能够更快降低误差，并更准确捕捉中心涡旋结构。
* **局部守恒误差**（图 31）  
  S-PINN 在所有子域的守恒性显著优于传统 PINN。

### 1757946946190.png1757946962367.png

**圆柱尾迹反问题**

* **速度场预测与误差分布**（图 41）  
  S-PINN 在无噪声和含 1% 噪声的情况下均保持高精度。
* **守恒性表现**（图 42）  
  S-PINN 在复杂非线性流区依旧能维持全局守恒。
* **训练效率**（表 10）  
  S-PINN 每轮训练时间约为 PINN 的两倍，但预测精度更高，抗噪性更强。

### 1757946995404.png1757947020232.png

---

**0****5**

**结论**

> ![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F41bb8365278b437ea2909dc126581b7f?Expires=1780067034&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=j%2FF7UOEWAmmLF4ELVHhwXAEPBhw%3D)
>
> 本文**提出了一种新型的稳定化物理信息神经网络（S-PINN），用于缓解 PINN 中多级协同优化引发的冲突。**S-PINN 通过在流体域中建立守恒子域，并对子域内的守恒量残差进行高斯积分，从而准确计算质量与动量的残差。其损失函数由这些守恒误差加权求和构成。通过最小化该损失函数，优化器能够训练得到一个稳定的神经网络模型，从而实现对流体动力学的高精度预测。以 Navier-Stokes 方程为例的研究表明，S-PINN 能够有效缓解噪声数据与基本方程、逐点残差之间的冲突，增强流场的局部与全局守恒特性。在预测精度、收敛速度、训练稳定性以及避免过拟合等方面均表现优越。尽管 S-PINN 引入了额外计算成本，但在相同训练预算下，其预测精度始终高于传统 PINN 方法。因此，**S-PINN 在智能流体动力学的多样化应用中展现出广阔前景。其发展代表了物理信息深度学习框架的重要进展，为解决复杂系统挑战提供了新的可能性。**

**总结与启示**

通过对比可见，S-PINN 的优势主要体现在：

1. **增强守恒性**：保证局部与全局物理量守恒；
2. **缓解冲突**：减少数据噪声与 PDE 方程之间的矛盾；
3. **提升稳定性**：收敛更快、训练过程更平稳；
4. **具备兼容性**：可与多种 PINN 变体结合应用。

不足之处在于计算成本提升，但在科研与工程问题中，这一代价是可接受的，尤其适用于高精度要求与数据稀缺场景。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fbb453576fdbc577c2f2bdf9142b382e8?Expires=1780067034&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=UbcrmjD3Lb4MNc63AF7Dj1w69yI%3D)

---

论文链接：

https://doi.org/10.1016/j.cma.2025.118348  
本推文仅对原文献进行简要分享，研究团队的相关信息已在开头注明，如有侵权或信息不准确之处，请通过后台联系。

*SOCIAL PRACTICE*

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 11:03*

## Related Notes

- [[FMPINN：基于傅里叶的混合物理信息神经网络求解多尺度椭圆PDEs]]
- [[Ψ-NN：通过知识蒸馏自动发现物理信息神经网络结构的新方法]]
- [[AgentEvolver vs AlphaEvolve：AI自我进化的两条核心路线对比 🧠]]
