---
direction: iNEST
category: theory
title: "CST V45 Symmetric Theory Candidate"
date: "2026-08-13"
status: "[候选定版] 数学规范冻结；经验命题待 V-CST-12 验证"
supersedes: "V44 两项律作为一般定理的表述"
tags: [CST, V45, symmetry, coordination, scale-first, verification]
---

# CST V45 对称理论候选

## 0. 定版边界

本稿完成的是**理论规范定版**：定义、量纲、组合律、可证伪条件和版本关系均冻结。它**不**把尚未实测的 $\partial m/\partial\Gamma_{st}$、$\zeta$、$n_{ch}$、器件有效态数或智能等级阈值写成既成事实。

因此，本稿的状态是“候选定版”，不是“经验结论定版”。只有 V-CST-12 的预注册实验通过后，才可将其中相应命题升为 `[实测]`。

---

## 1. 对 V44 的科学诊断

### 1.1 总判断

V44 的两个进步应保留：

1. 用总可分辨轨道容量 $\mathcal N$ 与每通道强度密度 $\mathrm{CST}=\mathcal N^{1/n_{ch}}$ 分离广延量和强度量；
2. 用有限分辨率 $(\varepsilon,\tau)$-熵率代替无噪极限的 $h_{KS}$，避免把噪声驱动回响态误写成确定性混沌。

但“协同不是第三项、而只是时间项的导数”不能作为一般定理定版。它只在**完全中介模型**成立时成立：结构—功能对齐只改变相关时间 $\tau_c$，且不改变有效维数 $\hat d$、可分辨态数 $M$、熵率 $\hat h$，也不存在直接的协调增益。上述条件目前均未被实测。

### 1.2 V44 的阻断问题

| 严重度 | 位置 | 问题 | 修订 |
|---|---|---|---|
| Critical | P3 / A1 | V44 定义 $\mathrm{CST}=\mathcal N^{1/n_{ch}}$ 为密度，却要求两模块的 $\ln\mathrm{CST}$ 严格相加；两者不能同时成立 | 总容量 $\ln\mathcal N$ 相加；密度 $\ln\mathrm{CST}$ 按 $n_{ch}$ 加权平均 |
| Critical | 摘要、3.4 | 将 $\Gamma_{st}$ 完全吸收到 $T_c$，把关系量强行改写为时间量；该改写在结构/时间交换下不对称 | 恢复独立的协同作用 $\Lambda_{st}$；V44 两项律降为 $\Lambda_{st}=0$ 的特例 |
| Critical | A2 | Kolmogorov–Szegő 对固定新息方差的高斯 AR(1) 熵率结论，不能推出真实神经/晶上网络的 $\hat h$ 与 $\Gamma$ 无关 | A2 保留为可检验中介假设；活动率钳定不足以钳定新息方差、协方差谱或有效维数 |
| Major | 3.1–3.2 | $\ln(1/\varepsilon)$ 在 $\varepsilon$ 有物理单位时不合法；$M=\mathrm{SNR}$ 也不是严格的态数等式 | 使用 $\ln(R/\varepsilon)$；$M_\varepsilon=R/\varepsilon$ 为固定动态范围和判决准则下的有效态数，SNR 仅为代理 |
| Major | 3.5 | $\tau_c\lesssim\sqrt N$ 被当作普适定理 | 它仅是均场分支过程、$s_c\sim(1-m)^{-2}$ 且 $s_c\lesssim N_{eff}$ 下的基准；一般写为 $\tau_c^{max}\sim N_{eff}^{\zeta}$，$\zeta=1/2$ 待检验 |
| Major | 3.4/3.5 | $\alpha\le\ln M_{dev}$ 没有由计数或 Landauer 定理推出 | 删除此不等式；时间中介斜率与器件态数须独立测量、比较，不得互相定义 |
| Major | A1 | “最大可加分块数”不能由 A1 唯一确定，取决于分块族、尺度、数据长度和容差 | $n_{ch}(\ell,\varepsilon)$ 为尺度标注的有效通道数估计量；A1 是对其组合律的检验，不是唯一计数器 |
| Major | §四 | Frobenius 余弦已天然有界，再作 $\tanh$ 会改变刻度；拉普拉斯与协方差的对角/符号未固定 | 保留去对角、中心化、归一化约定；不再对余弦二次压缩 |
| Major | P1/P2/IIL | $0.068$、$0.50\pm0.05$、$\sigma(m)=2\times10^{-3}$、$\pm0.03$、倍增等级表均未给可复现实测来源，却被写成判决数字 | 统一标 `[待测]` 或 `[待注册]`；功效、误差和阈值在 V-CST-12 先导批后冻结 |

### 1.3 最关键的数学理由：条件化可两项，但不对称

对任意两个非独立的空间与时间描述，链式分解可以写成

$$H(S,T)=H(S)+H(T\mid S).$$

把协同吸收到 $H(T\mid S)$ 总是可行，但这不是对称的基本分解；交换顺序便得到 $H(T)+H(S\mid T)$。

因此，V44 的两项律是“先给定结构，再计算条件时间复杂度”的**条件化表述**，不是“协同不存在”的证明。若目标是拓扑中心计算与智能涌现的共同主线，理论应保留一个在 $S\leftrightarrow T$ 交换下不变的关系项。

---

## 2. V45 的最简对称主方程

### 2.1 三个不可混同的量

令 $\mathcal N_{\rm v}$ 表示在分辨率 $\varepsilon$、观测窗 $\tau$ 与预先冻结任务/稳定性约束下的**可行且可区分**时空轨道数；令 $n_{ch}$ 为尺度标注的有效独立通道数。定义

$$c\equiv\ln\mathrm{CST}\equiv\frac{1}{n_{ch}}\ln\mathcal N_{\rm v}. $$

V45 的唯一主方程为

$$oxed{
c=s+t+\Lambda_{st},\qquad
s=\hat d_{\varepsilon}\ln M_{\varepsilon},\qquad
t=\hat h_{\varepsilon}\tau_c,\qquad
\mathrm{CST}=M_{\varepsilon}^{\hat d_{\varepsilon}}\,e^{\hat h_{\varepsilon}\tau_c}\,e^{\Lambda_{st}}.
}$$

| 项 | 含义 | 是否可由其他项替代 |
|---|---|---|
| $s$ | 空间可达态宽度：有效自由度 × 每自由度可分辨态数 | 否。它描述“同一瞬间能区分多少态” |
| $t$ | 时间记忆深度：每通道熵率 × 相关时间 | 否。它描述“信息能保留多久” |
| $\Lambda_{st}$ | 协同作用：在保持边际空间、时间统计量后，结构—功能对齐带来的剩余可行轨道增益或损失 | 否，除非经实验确认完全中介 |

这不是“三个旋钮”。$s$、$t$、$\Lambda_{st}$ 分别对应宽度、深度、协调；第三项是关系量，不是又一个节点或时间属性。

### 2.2 协同作用的操作定义

构造一个预注册的结构—功能错配零模型 $\mathcal Q_0$：它保持 $\hat d_\varepsilon$、$M_\varepsilon$、$\hat h_\varepsilon$、$\tau_c$ 的边际估计协议和物理约束，但破坏结构—功能的配对关系。定义

$$oxed{
\Lambda_{st}\equiv\frac{1}{n_{ch}}\ln\frac{\mathcal N_{\rm v}^{\rm obs}}{\mathcal N_{\rm v}^{\mathcal Q_0}}.
}$$

- $\Lambda_{st}>0$：对齐增加可行可区分轨道，称为协同增益；
- $\Lambda_{st}<0$：对齐造成冗余或约束，称为协同损失；
- $\Lambda_{st}=0$：给定边际统计量后无剩余协调作用。

在局部工作窗口中，才可作线性响应：

$$\Lambda_{st}=a_{st}\Gamma_{st}+O(\Gamma_{st}^2),$$

其中 $\Gamma_{st}\in[-1,1]$ 是标准化结构—功能对齐度，$a_{st}$ 是待测协调作用量（nat/通道），不可由器件态数或回响时间替代定义。

该式自然给出反演对称：若二阶项可忽略，$G(\Gamma)G(-\Gamma)=1$。

### 2.3 完全中介条件：V44 两项律的准确地位

对 $c$ 求导：

$$rac{dc}{d\Gamma}=ln M\frac{d\hat d}{d\Gamma}+\hat d\frac{d\ln M}{d\Gamma}+\tau_c\frac{d\hat h}{d\Gamma}+\hat h\frac{d\tau_c}{d\Gamma}+rac{d\Lambda_{st}}{d\Gamma}. $$

若以下条件同时被实验证实：

$$rac{d\hat d}{d\Gamma}=0,\quadrac{dM}{d\Gamma}=0,\quadrac{d\hat h}{d\Gamma}=0,\quadrac{d\Lambda_{st}}{d\Gamma}=0,$$

才可在不依赖路径间偶然抵消的意义下写为

$$rac{dc}{d\Gamma}=\hat h\frac{d\tau_c}{d\Gamma}.$$

上述逐路径条件是完全中介的**充分且可操作化**判据，而非从总导数相等反推的必要条件：不同非时间路径可能数值抵消，却不能据此宣称协同被时间中介。满足该判据后，才可以定义条件时间项 $t_{\rm cond}=t+\Lambda_{st}$，使 V44 的两项表达成为 V45 的**完全中介特例**。在此之前，把 $\Gamma_{st}$ 合并入 $T_c$ 会掩盖机制、破坏空间—时间交换对称性，并导致不可区分的双重计数。

---

## 3. 量纲、尺度与组合律

### 3.1 分辨率锚定

$$ln\mathcal N(\tau,\varepsilon)=D_{\varepsilon}\ln\frac{R}{\varepsilon}+h_{\varepsilon}\tau+o(\tau).$$

这里 $R$ 是预注册的状态动态范围，$\varepsilon$ 是噪声底或判别阈值，因而 $M_{\varepsilon}=R/\varepsilon$ 是无量纲的有效态数。若以 SNR 作代理，必须同时报告动态范围、噪声定义与判决准则；不能写成“态数严格等于 SNR”。

### 3.2 正确的组合律

对物理上独立的 A、B：

$$\ln\mathcal N_{A\otimes B}=\ln\mathcal N_A+\ln\mathcal N_B.$$

因此强度密度 obeys

$$oxed{
\ln\mathrm{CST}_{A\otimes B}=rac{n_A\ln\mathrm{CST}_A+n_B\ln\mathrm{CST}_B}{n_A+n_B},\qquad
\mathrm{CST}_{A\otimes B}=\left(\mathrm{CST}_A^{n_A}\mathrm{CST}_B^{n_B}\right)^{1/(n_A+n_B)}.
}$$

故“$\ln\mathrm{CST}$ 严格相加”只适用于未除以 $n_{ch}$ 的总容量，不适用于 CST 密度。

### 3.3 规模第一性：正确命题

在均场分支过程且有限尺度截断满足 $s_c\sim(1-m)^{-2}$、$s_c\lesssim N_{\rm eff}$ 时，

$$\tau_c^{\max}\sim N_{\rm eff}^{1/2}.$$

这给出的是**均场基准**，不是所有拓扑、异质性或高阶网络的普适指数。V45 的一般尺度命题为

$$oxed{\tau_c^{\max}\sim N_{\rm eff}^{\zeta},\qquad \zeta_{\rm MF}=1/2.}$$

$N_{\rm eff}$ 应为有效相互作用规模或有效独立域数，而非裸节点数；其估计方法、尺度和置信区间必须预注册。规模第一性仍然成立：只要 $\zeta>0$，提升可维持时间深度的根本路径就是扩展有效网络规模；但具体指数必须通过 P2 实测。

---

## 4. 三条经验律与四个验证任务

### 4.1 三条经验律（均为待验证，不冒充定理）

| 律 | 陈述 | 状态 |
|---|---|---|
| L1 完全中介律 | $d\Lambda_{st}/d\Gamma=0$ 且 $d\hat d/d\Gamma=d\hat h/d\Gamma=dM/d\Gamma=0$；协同只经 $\tau_c$ 生效 | `[待测]`；若成立，V44 两项律成立 |
| L2 有效规模律 | $\tau_c^{max}\sim N_{eff}^{\zeta}$ | `[待测]`；$\zeta=1/2$ 为均场基准 |
| L3 容量组合律 | $\ln\mathcal N$ 对独立模块可加，CST 密度满足加权几何平均 | `[待测]`；可由物理隔离模块检验 |

### 4.2 验证任务

| 任务 | 测什么 | 方法 | 验收标准 |
|---|---|---|---|
| V-M1 协同残差 | $a_{st}$ 与 $d\Lambda/d\Gamma$ | 固定边际统计量的错配零模型；拟合 $c=s+t+a_{st}\Gamma+O(\Gamma^2)$ | 预注册 TOST 或模型比较；只能在 $a_{st}$ 等价于 0 时接受 L1 |
| V-M2 中介分解 | $d\hat d/d\Gamma,d\hat h/d\Gamma,d\tau/d\Gamma,d\Lambda/d\Gamma$ | Γ 双向扫描；活动率、新息方差、动态范围分别钳定/记录 | 总导数闭合；报告每条路径 CI，不得只报 $m$ |
| V-M3 规模律 | $\zeta$ | 跨 $N_{eff}$ 模块的临界邻域扫描，固定测量窗与噪声底 | 双对数斜率和 CI；检验 $\zeta=1/2$ 是基准而非预设真值 |
| V-M4 组合律 | $\ln\mathcal N$ 与 CST 密度组合 | SDI 物理隔离 A/B 后分别与联合测量 | 总容量相加、密度加权几何平均在预注册容差内成立 |

所有数值门槛（置换数、容差、样本数、Γ 分辨率、功效）由 V-CST-12 阶段 0 先导批冻结；本稿不杜撰具体数值。

---

## 5. IIL 与工程含义

### 5.1 CST 不直接等于智能等级

CST 给出的是网络的时空协调容量，不能只凭一个连续数值宣布“通用智能”。智能等级至少需同时报告：

1. **质量轴**：$c=\ln\mathrm{CST}$（nat/有效通道）；
2. **规模轴**：$N_{\rm eff}$ 或连接规模 $N_{\rm conn}$；
3. **任务轴**：预注册的跨任务迁移、适应与组合能力测验。

V44 的倍增阈值是可用的项目管理分类法，但 $c_1=1$ nat 及各等级门限目前均为 `[待注册]`，不是从 CST 自行推出的自然常数。

### 5.2 工程上的最小闭环

- **器件层**：提高 $M_\varepsilon$ 与可测动态范围；
- **网络层**：提高 $N_{\rm eff}$、控制有限尺度临界邻域；
- **架构层**：通过 SDI 改变结构—功能对齐，测量 $\Lambda_{st}$ 的中介路径和残差；
- **系统层**：在任务轴上检验容量是否转化为可迁移能力。

这比“拓扑只延长记忆”更稳健：拓扑可通过时间深度、状态可达性和直接协调残差三条路径改善能力，哪条成立由 V-M1/V-M2 决定。

---

## 6. 关键来源核验与使用边界

| 来源 | 核验 | 可支持的结论 | 不可外推的结论 |
|---|---|---|---|
| Gaspard & Wang, *Physics Reports* 235, 291–343 (1993), DOI: [10.1016/0370-1573(93)90012-3](https://doi.org/10.1016/0370-1573(93)90012-3) | 已核对题名、卷页、DOI | 噪声、混沌与 $(\varepsilon,\tau)$-熵率的有限分辨率框架 | 不能单独推出 CST 的三项或两项因果分解 |
| Wilting & Priesemann, *Nature Communications* 9 (2018), DOI: [10.1038/s41467-018-04725-4](https://doi.org/10.1038/s41467-018-04725-4) | 已核对题名、DOI | MR 估计量与强亚采样系统的集体动力学推断 | 不直接给出 $\partial m/\partial\Gamma$ 或 CST 参数 |
| Garcia-Millan, Font-Clos & Corral, *Physical Review E* 91, 042122 (2015), DOI: [10.1103/PhysRevE.91.042122](https://doi.org/10.1103/PhysRevE.91.042122) | 已核对题名、DOI；题名为有限尺寸分支过程存活概率 | 有限尺寸分支过程研究的相关性 | 不自动等同于任意晶上网络的雪崩截断指数 |
| Murray et al., *Nature Neuroscience* 17, 1661–1663 (2014), DOI: [10.1038/nn.3862](https://doi.org/10.1038/nn.3862) | 已核对题名、DOI | 灵长类皮层存在内在时间尺度层级 | 不能单独证明 $\sqrt N$ 律 |
| Chaudhuri et al., *Neuron* 88, 419–431 (2015), DOI: [10.1016/j.neuron.2015.09.008](https://doi.org/10.1016/j.neuron.2015.09.008) | 已核对题名、DOI | 局部循环与大尺度回路机制可形成时间尺度层级 | 不能证明 Γ 对 m 为仿射因果关系 |
| Honey et al., *PNAS* 106, 2035–2040 (2009), DOI: [10.1073/pnas.0811168106](https://doi.org/10.1073/pnas.0811168106) | 已核对题名、DOI | 结构连接可预测部分静息态功能连接 | 不等同于结构—功能协同只影响时间项 |
| Kinouchi & Copelli, *Nature Physics* 2, 348–351 (2006), DOI: [10.1038/nphys289](https://doi.org/10.1038/nphys289) | 已核对题名、DOI | 可激网络临界点附近动态范围最优 | 不直接给出 $\tau_c\sim\sqrt N$ 的普适指数 |

---

## 7. 合入规则

1. 本稿暂不覆盖 `CST_Symbol_Baseline`；
2. 团队应先用 V-M1 判定“完全中介”还是“独立协同残差”；
3. 若 L1 通过，则可发布 V45 的两项约化版，并在脚注中明确其适用条件；
4. 若 L1 不通过，则三项对称式为正式 CST 主方程；
5. 无论哪种结果，V44 中所有未实测数值、六自然常数与未经功效计算的判决阈值不得进入正式基线。

**一句话定版**：

> CST 的最简一般形式不是“空间加时间”，而是“空间、时间与协同作用”的对称分解；只有数据证实协同被时间完全中介时，才可安全地约化为两项律。

*证据标识：`[引用]` 为已核对公开来源；`[推导]` 为本稿给出的数学推导；`[待测]`、`[待注册]` 项不得作为已证实事实。*


