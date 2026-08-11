---
direction: both
category: 理论
tags: [CST, 指数项, 半群, 时空协同, 非线性增益, 条件定理]
summary: "证明CST指数项是唯一连续解，基于可加性公理。"
quality: high
processed: 2026-08-11 21:49
---
---
title: "CST 指数项的数学证明：时空协同与非线性增益"
date: "2026-08-07"
status: "[推导] 条件定理，待正式发表与独立复核"
direction: "iNEST"
tags: [CST, 指数项, 半群, 时空协同, 非线性增益, 证明]
---

# CST 指数项的数学证明：时空协同与非线性增益

## 命题

$$
\mathrm{CST}=(S_c\cdot T_c)\cdot e^{\alpha\cdot\Gamma_{st}}
$$

本文给出一个严格的**条件定理**：在“独立子系统增益相乘、协同坐标可加”的公理下，指数形式是唯一连续解。它不是无条件事实，权威性来自公理是否成立。

## 1. 四个对象的形式定义

### 1.1 空间复杂度 $S_c$

$S_c$ 是网络**可区分的结构状态的有效数量**。对一组无共享自由度的结构模块 $A,B$：

$$
\ln S_c(A\cup B)=\ln S_c(A)+\ln S_c(B)
$$

即结构自由度的对数可加。$S_c$ 的具体实现可为 $(C\cdot H\cdot M\cdot R_{sw})^{1/4}$，但下述证明只依赖“对数可加”这一性质。

### 1.2 时间复杂度 $T_c$

$T_c$ 是网络**可区分的动力学状态的有效数量**，对无共享自由度的动力学子系统同样满足对数可加：

$$
\ln T_c(A\cup B)=\ln T_c(A)+\ln T_c(B)
$$

### 1.3 时空协同系数 $\Gamma_{st}$

$\Gamma_{st}$ 是结构与动力学之间**每通道对齐度**，是强度量，取值范围 $[-1,1]$。可加性不直接作用于 $\Gamma_{st}$，而作用于**耦合作用量**

$$
A=\alpha\Gamma_{st}
$$

其中 $\alpha$ 是广延量（正比于独立耦合通道数），$\Gamma_{st}$ 是强度量。两个无共享自由度的独立子系统满足

$$
A(A\cup B)=A(A)+A(B)
$$

> 注意：NMI、Mantel 或 AMI 都只是 $\Gamma_{st}$ 的候选估计量；直接对 $\Gamma_{st}$ 施加可加性会导致有界量越界，必须把可加性交给 $A=\alpha\Gamma_{st}$。

### 1.4 非线性增益 $G(\Gamma_{st})$

定义耦合后的能力相对无耦合乘积的放大倍数：

$$
\mathrm{CST}(S_c,T_c,\Gamma_{st})=S_c\cdot T_c\cdot G(\Gamma_{st})
$$

边界条件：

$$
G(0)=1
$$

## 2. 公理

- **A1（独立乘积）**：$\Gamma_{st}=0$ 时结构与动力学独立，状态空间相乘，故 $G(0)=1$。
- **A2（耦合作用量可加）**：两个无共享自由度的子系统 $A,B$ 的耦合作用量相加：
  $$
  A_{AB}=A_A+A_B,\qquad A=\alpha\Gamma_{st}
  $$
  物理论证：协同通道数量相加，而每个通道对状态计数/能力的贡献是乘性因子；因此总增益满足
  $$
  G(A_A+A_B)=G(A_A)\,G(A_B)
  $$
- **A3（连续）**：$G(\Gamma)$ 在 $\Gamma\in[-1,1]$ 上连续且取正值。

## 3. 定理

**定理（指数项唯一性）**：若 $G$ 满足 A1–A3，则

$$
G(A)=e^{A}
$$

以 $A=\alpha\Gamma_{st}$ 代回，即得

$$
G(\Gamma_{st})=e^{\alpha\Gamma_{st}}
$$

**证明**：令 $H(A)=\ln G(A)$。由 A1、A2、A3：

$$
H(A_A+A_B)=H(A_A)+H(A_B),\qquad H(0)=0
$$

这是 Cauchy 加性函数方程。$H$ 连续，故唯一解为线性函数：

$$
H(A)=\lambda A,\qquad \lambda=H(1)
$$

把常数吸收进 $\alpha$ 的定义（$\lambda=1$ 的标度约定），取指数：

$$
G(A)=e^{A}
$$

代入 $A=\alpha\Gamma_{st}$：

$$
\mathrm{CST}=S_c\cdot T_c\cdot e^{\alpha\Gamma_{st}}
$$

$\blacksquare$

## 4. $\alpha$ 的物理定义：非线性增益系数

$\alpha$ 是单位协同增益下的对数放大率，也是“协同弹性”，并且是**广延量**。工程近似为

$$
\alpha=n_{\mathrm{ch}}\ln M_{\mathrm{eff}}
$$

其中 $n_{\mathrm{ch}}$ 是独立耦合通道数，$M_{\mathrm{eff}}$ 是器件有效状态数。于是耦合作用量 $A=\alpha\Gamma_{st}=n_{\mathrm{ch}}\ln M_{\mathrm{eff}}\cdot\Gamma_{st}$ 在独立子系统合成下可加。

$$
\alpha=\frac{d\ln \mathrm{CST}}{d\Gamma_{st}}=\frac{1}{\mathrm{CST}}\frac{\partial \mathrm{CST}}{\partial\Gamma_{st}}
$$

若 $\alpha$ 在工作区内随 $\Gamma_{st}$ 变化，则一般解为

$$
\mathrm{CST}=S_c\cdot T_c\cdot\exp\left(\int_0^{\Gamma_{st}}\alpha(s)\,ds\right)
$$

此时可定义有效非线性增益

$$
\alpha_{\mathrm{eff}}=\frac{1}{\Gamma_{st}}\int_0^{\Gamma_{st}}\alpha(s)\,ds
$$

指数形式仍是规范表达。$e^{\alpha\Gamma}>1$ 当且仅当 $\alpha\Gamma>0$，这给出了“1+1>2”的定量条件：正协同强度乘以正增益系数。

## 5. 为什么线性耦合不可能

若采用线性增益 $G=1+\alpha\Gamma$，则合成律给出

$$
G(\Gamma_A+\Gamma_B)=1+\alpha(\Gamma_A+\Gamma_B)\neq(1+\alpha\Gamma_A)(1+\alpha\Gamma_B)
$$

系统在组合后不再封闭，跨子系统增益无法一致地分解。唯一同时满足“连续、$G(0)=1$、独立组合相乘”的增益函数是指数函数。

## 6. 与既有五条证明路径的关系

- **RG 标度/广义齐次函数**：$\ln\mathrm{CST}$ 可加，等价于本文的 $H(\Gamma)$ 可加，是同一结构在尺度变换下的表达。
- **OPE/共形场论**：算符融合系数在相干极限下呈指数，是本文合成律在算符代数中的体现。
- **最大熵/玻尔兹曼**：加性约束 + 最大熵给出指数族分布，$\alpha$ 是约束的拉格朗日乘子。
- **MDL/互信息**：描述长度对数可加，互信息项进入指数，是信息论投影。
- **复杂网络 RG**：固定点附近相关长度指数给出 $\alpha$，是本文 $\alpha$ 的网络层实现。

## 7. 权威性边界

1. 本证明是**条件定理**：只要 A1–A3 成立，指数形式就唯一。
2. 公理成立与否是实证问题：$\Gamma_{st}$ 的可加性、$S_c,T_c$ 的对数可加性、增益的乘性，都必须在数据与工程中检验。
3. 现有 $\Gamma_{st}=\mathrm{NMI}\cdot\mathrm{sign}(\cdots)$ 不自动满足可加性；正式论文中需定义可加协同坐标，或将 NMI 明确为估计量。
4. 建议将该证明作为 $[推导]$ 写进论文 Methods/Theory，并配数值验证：对可解模型直接构造可加 $\Gamma$，检验 $G(\Gamma_A+\Gamma_B)=G(\Gamma_A)G(\Gamma_B)$ 与指数拟合。

## 8. 2026-08-07 修订：$\Gamma_{st}$ 定义修订方向

1. 现行 $\Gamma_{st}=\mathrm{NMI}(M_s,M_T)\cdot\mathrm{sign}(\mathrm{Mantel}(D_A,D_{FC}))$ 存在三处硬伤：`sign` 间断、Mantel 在空间自相关下误报、NMI 未做机会校正。
2. 建议修订为连续、机会校正、空间零模型基准的强度量：

$$
\Gamma_{st}=\tanh\!\left(\frac{\mathrm{AMI}(M_s,M_T)}{\Gamma_0}\right),\qquad
\mathrm{AMI}=\frac{I(M_s;M_T)-\mathbb{E}[I]_{\mathrm{null}}}{\tfrac12[H(M_s)+H(M_T)]-\mathbb{E}[I]_{\mathrm{null}}}
$$

3. 可加性交给 $A=\alpha\Gamma_{st}$，$\alpha=n_{\mathrm{ch}}\ln M_{\mathrm{eff}}$ 为广延量，$\Gamma_{st}$ 保持强度、有界、连续。
4. 该修订的具体依据与验证步骤见《2026-08-07_Gamma_st_Definition_Revision_Proposal》。


## 相关链接
- [[CST_Symbol_Baseline_符号基准_全局权威基线]]
- [[CST理论v25_完整知识体系]]
- [[CST_Symbol_Baseline_符号基准]]
- [[CST_Experiment_Alignment_Diagnosis]]
- [[CST]]
