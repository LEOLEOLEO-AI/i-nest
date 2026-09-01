---
direction: iNEST
category: 理论
tags: [CST, Γst, AMI, Mantel, 时空协同, 修订]
summary: "修订Γst定义，修复统计与可微性硬伤"
quality: high
processed: 2026-08-11 21:49
---
---
title: "Γst 定义修订提案：判断、方案与依据"
date: "2026-08-07"
updated: "2026-09-01"
status: "[已采纳] 主定义锁定，四项补充已写入"
direction: "iNEST"
tags: [CST, Γst, AMI, Mantel, 时空协同, 修订]
---

# Γst 定义修订提案：判断、方案与依据

## 1. 总体判断

对现行定义

$$
\Gamma_{st}=\mathrm{NMI}(M_s,M_T)\cdot\mathrm{sign}\big(\mathrm{Mantel}(D_A,D_{FC})\big)
$$

的批评**基本成立**，属于可以定性为“统计学与可微性硬伤”的问题，而非单纯表述差异。三点核心批评均有文献依据；其提出的替换方向合理，但仍需补强两项工程约束。

## 2. 现行定义的三处硬伤

### 2.1 `sign(Mantel)` 间断

当 Mantel 相关穿越零点时，$\Gamma_{st}$ 在 $+\mathrm{NMI}$ 与 $-\mathrm{NMI}$ 之间跳跃。后果：

- $\partial\mathrm{CST}/\partial\Gamma_{st}$ 在零点不存在，SDI 控制律无法在最需要控制的区域获得梯度；
- $r_M$ 在零点附近抽样方差最大，估计量在最不稳定处做最激进的方向判断；
- `NMI·sign` 在独立子系统合成下不可加，与“耦合作用量可加”的证明公理脱钩。

### 2.2 Mantel 检验用于空间自相关矩阵

Guillot & Rousset (2013) 明确警告：当两个矩阵各自存在空间自相关时，Mantel 检验的第一类错误率被严重膨胀。结构距离 $D_A$ 与功能距离 $D_{FC}$ 在真实脑网络和晶上网络中均强空间自相关，因此只取 Mantel 符号是这套定义中最脆弱的一环。

### 2.3 NMI 未做机会校正

Vinh, Epps & Bailey (2010) 证明 NMI 随社区数增加而系统性虚高，纯随机划分也可获得较高 NMI。叠加 Louvain 模块度景观的简并性，$\Gamma_{st}$ 幅值对划分算法和分辨率参数敏感。

## 3. 修订定义

### 3.1 主定义（已采纳，2026-09-01 锁定）

$$
\Gamma_{st}=\tanh\!\left(\frac{\mathrm{AMI}(M_s,M_T)}{\Gamma_0}\right)
$$

$$
\mathrm{AMI}=\frac{I(M_s;M_T)-\mathbb{E}[I]_{\mathrm{null}}}{\max\!\left(\tfrac12[H(M_s)+H(M_T)]-\mathbb{E}[I]_{\mathrm{null}},\ \varepsilon\right)},\quad \varepsilon=10^{-10}
$$

> **补充1（分母零除保护）**：分母加 $\varepsilon=10^{-10}$，防止单社区极端情况（$H_s\approx 0$）时零除。

性质：

- 机会校正：扣除随机划分期望互信息；
- 符号自然：低于零模型时 AMI 为负，即反耦合；
- 光滑：$\tanh$ 保证 $\Gamma_{st}\in(-1,1)$ 且处处可微；零点梯度 $\mathrm{d}\Gamma_{st}/\mathrm{d}(\mathrm{AMI})|_0=1/\Gamma_0$，有限非零；
- 空间零模型：$\mathbb{E}[I]_{\mathrm{null}}$ 由保度序、保空间嵌入的替代网络生成，吸收空间自相关来源。

> **补充2（Γ₀ 先验约束）**：数值检验表明 $\Gamma_0\approx 1.0$ 时，AMI=0.17（C. elegans 参考）映射到 $\Gamma_{st}=0.168$，最接近生物文献值。E1 标定实验先验搜索范围定为 $\Gamma_0\in[0.8,1.2]$，实验完成后冻结，**不得事后调整**。

### 3.2 备选定义（节点对级，与主定义并行验证）

为避免 Louvain 划分简并性，用节点对级连续对齐替代社区级划分：

$$
\Gamma_{st}=\tanh\!\left(\frac{\rho\big(\mathrm{Sim}_S,\mathrm{Sim}_F\big)-\mathbb{E}_0[\rho]}{\Gamma_0}\right)
$$

其中：
- $\mathrm{Sim}_S$：结构相似矩阵，$\mathrm{Sim}_S(i,j)=\cos(\mathbf{a}_i,\mathbf{a}_j)$（节点邻接向量余弦相似度）；
- $\mathrm{Sim}_F$：功能相似矩阵，$\mathrm{Sim}_F(i,j)=\mathrm{corr}(\mathbf{x}_i,\mathbf{x}_j)$（激活时间序列 Pearson 相关）；
- 取两矩阵上三角元素向量，计算 Pearson 相关 $\rho$；
- $\mathbb{E}_0[\rho]$ 在空间约束置换零模型下估计（保节点度序和空间嵌入，置换次数 ≥ 1000）。

> **补充3（SimS/SimF 算法明确）**：余弦相似度用于结构矩阵（对稀疏连接组友好），Pearson 相关用于功能矩阵（与 FC 文献一致）。若节点无时间序列（静态网络），$\mathrm{Sim}_F$ 改用 Jaccard 重叠度。

该式不依赖社区划分，机会校正与空间自相关校正均保留，与主定义共用同一 $\Gamma_0$。

### 3.3 强度—广延分工

有界强度量不可能可加，因此可加性不作用于 $\Gamma_{st}$，而作用于耦合作用量：

$$
A=\alpha\Gamma_{st},\qquad \alpha=n_{\mathrm{ch}}\ln M_{\mathrm{eff}}
$$

- $\alpha$：广延量，正比于独立耦合通道数；
- $\Gamma_{st}$：强度量，每通道对齐度，$(-1,1)$；
- $A$：广延耦合作用量，独立子系统合成时相加；
- Cauchy–Aczél 唯一性定理作用于 $A$，指数形式 $e^{\alpha\Gamma_{st}}$ 的证明得以保留。

## 4. 修订依据

| 依据 | 来源 | 核实状态 |
|---|---|---|
| O-information（已移至 §3.4 交叉验证工具，不参与主定义） | — | — |
| Mantel 检验在空间自相关下第一类错误膨胀 | Guillot & Rousset, *Methods Ecol. Evol.* 4, 336 (2013)，[DOI](https://doi.org/10.1111/2041-210x.12018) | 已核对 DOI 与题名 |
| NMI 机会虚高，需使用调整指标 | Vinh, Epps & Bailey, *JMLR* 11, 2837 (2010)，[链接](https://jmlr.org/papers/v11/vinh10a.html) | 文献真实，结论与提案一致 |
| Louvain/模块度景观简并 | Good, de Montjoye & Clauset, *Phys. Rev. E* 81, 046106 (2010)，[DOI](https://doi.org/10.1103/PhysRevE.81.046106) | 文献真实 |
| 小世界系数 σ 定义 | Humphries & Gurney, *PLoS ONE* 3, e0002051 (2008)，[DOI](https://doi.org/10.1371/journal.pone.0002051)；非 Watts & Strogatz 1998 | 文献归属已核对 |

### 3.4 交叉验证工具：O-information（补充4）

> **补充4（O-information 角色重定位）**：O-information（$\Omega$）**不参与** $\Gamma_{st}$ 主定义，仅作独立交叉验证工具。
> - 若主定义结果与 $\Gamma_{st}\propto-\Omega$ 一致 → 作为佐证记录；
> - 若不一致 → 优先以主定义为准，记录差异原因。
> - Rosas et al. (2019) *Phys. Rev. E* 100, 032305 引用保留，标注"交叉验证工具，不影响主定义"。

---

## 5. 实施步骤

1. **E1 定标实验**：在固定参考数据集上确定 $\Gamma_0$，记录拟合数据、范围和敏感性，之后冻结；
2. **零模型冻结**：确定空间约束配置模型的度数保持、空间嵌入和置换次数，预注册；
3. **双定义并行**：同时计算“社区级 AMI”与“节点对级连续对齐”，报告一致性；
4. **控制律验证**：检查 $\partial\mathrm{CST}/\partial\Gamma_{st}$ 在全区间连续，零点附近梯度方向稳定；
5. **O-information 交叉验证**：若使用，写死 $\Gamma_{st}\propto-\Omega$，只作独立佐证，不作主定义；
6. **引用审计**：所有引用标注“已核实原句/未核实”，未核实文献不得作为论据。

## 6. 仍需补强的点

- AMI 修正的是“机会虚高”，不修正“社区划分选择”；需报告分辨率与种子敏感性，或优先采用节点对级连续对齐；
- $\Gamma_0$ 是新增标定参数，必须在 E1 前预注册，否则会变成新的可调旋钮；
- 空间零模型的构造细节需与网络规模、边界效应和节点坐标误差一起审计；
- 修订后应同步更新符号基线、实验对齐诊断、V32 Methods 和指数证明文档，避免多个版本并存。



## 相关链接
- [[CST_V42.1_Review_Revision]]
- [[iNEST_自演化机制全景总结_最小作用量到物理智能]]
- [[CST_RG第一性原理推导协议]]
- [[2026-07-13-2607.09662]]
- [[2026-07-13-2601.10037]]
