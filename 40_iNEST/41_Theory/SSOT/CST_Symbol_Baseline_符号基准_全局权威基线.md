---
title: "CST 理论符号基准"
version: v4.0
date: 2026-06-20
status: 全局权威基线
tags: [CST, baseline, symbols, authoritative]
---

# CST 理论符号基准 — Symbol Baseline for Coordination Spatiotemporal Complexity (CST)

> **版本**: v4.0 (2026-06-20) · **依据**: CST V25 + RG推导协议 · **约束**: 全参数归一化∈[0,1]，等权重几何平均

## 核心公式

$$\text{CST} = (S_c \cdot T_c) \cdot e^{\alpha \cdot \Gamma_{st}}$$

## 空间复杂度 $S_c$（几何测度）

$$S_c = (C \cdot H \cdot M \cdot R_{sw})^{1/4}$$

| 符号 | 中文名 | 英文名 | 物理含义 | 测量方法 | 归一化 |
|------|--------|--------|---------|---------|--------|
| **$C$** | 连接密度 | Global Connectivity | LCC覆盖率，信息全局可达性 | $\|LCC\|/N$ | [0,1]，天然有界 |
| **$H$** | 层级深度 | Hierarchical Depth | k-core嵌套层级，网络组织深度 | $\min(k_{max}/k_{null}/6.667,\ 1)$ | [0,1]，HCP锚定1.0 |
| **$M$** | 模块化 | Modularity | Newman-Girvan功能分区程度 | $\max[(Q-0.02)/(1-0.02),\ 0.01]$ | [0,1]，floor=0.01 |
| **$R_{sw}$** | 小世界性 | Small-World Coefficient | 局部聚类+全局传输平衡 | $\tanh[(\sigma-1)/2]$ | [0,1]，σ=1→0 |

> **符号历史**: v1(2024): X₁/X₂/X₃/X₄ → v2(2026-05): ρ_G/κ_H/Q̃/σ̃ → **v3(2026-05-18): C/H/M/R_sw** (国际通用)

## 时间复杂度 $T_c$（动力学测度）

$$T_c = (\lambda_{eff} \cdot \Phi \cdot \Psi \cdot \Theta)^{1/4}$$

| 符号 | 中文名 | 英文名 | 物理含义 | 测量方法 |
|------|--------|--------|---------|---------|
| **$\lambda_{eff}$** | 临界性 | Criticality | 神经雪崩分支比，SOC临界态 | Branching Ratio ≈1.0 |
| **$\Phi$** | 相位一致性 | Phase Synchrony | Kuramoto序参数，跨区同步 | NMI of oscillatory phases |
| **$\Psi$** | 可塑性 | Plasticity | 功能连接时变性，适应能力 | FC variability over time |
| **$\Theta$** | 时间尺度多样性 | Timescale Diversity | 多尺度动力学Shannon熵 | Shannon entropy of τ distribution |

## 时空耦合 $\Gamma_{st}$

$$\Gamma_{st} = \text{NMI}(M_s,\ M_T) \cdot \text{sign}(\text{Mantel}(D_A,\ D_{FC})) \in [-1, 1]$$

## 设备物理系数 $\alpha$

$$\alpha = \ln(M_{eff})$$

| 设备类型 | $M_{eff}$ | $\alpha$ | 代表系统 |
|---------|:--:|:--:|---------|
| Binary digital | 2 | 0.69 | 现有AI/GPU |
| 分级电位 | 13 | 2.56 | C.elegans，无脊椎动物 |
| 脉冲神经元 | 32 | 3.47 | Loihi-2，SpiNNaker2 |
| **忆阻器（软饱和窗）** | **16-90** | **2.77-4.50** | **苏州实验室核心器件，RG推导α=2.8-4.5** |
| 人类皮层 | 50 | 3.91 | 人脑（保守估计） |

## 三层指标体系

| 指标 | 定义 | 用途 |
|------|------|------|
| **CST** | $(S_c \cdot T_c) \cdot e^{\alpha \cdot \Gamma_{st}}$ | 绝对智能潜力 |
| **IIL** | $\arg\max_k\{\theta_k \mid \text{CST} \geq \theta_k\}$ | 本征智能等级（L0-L6） |
| **RI** | $\text{CST} / E_{env}$ | 相对智能指数（任务相关） |
| **$\eta_I$** | $\text{CST} / P_{norm}$ | 智能效率（$P_{norm}=P/20W$） |

## 六级 IIL 阈值

| 等级 | 常数 | 值 | 第一性原理 | 生物对应 |
|------|------|:--:|---------|---------|
| L1 感知 | $1/\sqrt{2}$ | 0.707 | Shannon-Hartley，SNR_min=1 | C.elegans |
| L2 反应 | $1$ | 1.000 | 热力学第二定律，CST≥E_env | 章鱼，斑马鱼 |
| L3 适应 | $\varphi$ | 1.618 | 黄金分割，资源分配最优 | 乌鸦 |
| L4 创造 | $e$ | 2.718 | Landauer原理，信息生成上界 | 黑猩猩，海豚 |
| L5 通用 | $\pi$ | 3.142 | Kuramoto临界耦合 | 人类 |
| L6 超级 | $\delta$ | 4.669 | Feigenbaum常数，倍周期分岔 | iNEST Gen4+ |

---

> **版本链**: v1(2024) → v2(2026-05-12) → v3(2026-05-18) → **v4(2026-06-20)**
> **关联**: CST_RG第一性原理推导协议 · CST_Intelligence_Emergence_Paper_V25_FINAL · 海河实验室_正式项目申报书_TCC战略版