# CST理论符号基准文档
# Symbol Baseline for Coordination Spatiotemporal Complexity (CST)

**版本**：v3.0（2026-05-18 正式确定）  
**依据**：图片原始符号定义（2025-12 版本）+ V25论文等权重归一化体系  
**约束**：所有参数归一化 ∈ [0,1]，等权重几何平均（指数1/4），不加权重

---

## 核心公式

$$\text{CST} = (S_c \cdot T_c) \cdot e^{\alpha \cdot \Gamma_{st}}$$

---

## 空间复杂度 Sc（几何测度）

$$S_c = (C \cdot H \cdot M \cdot R_{sw})^{1/4}$$

| 符号 | 中文名 | 英文名 | 物理含义 | 测量方法 | 归一化 |
|------|--------|--------|---------|---------|--------|
| **$C$** | 连接密度/全局连通性 | Global Connectivity | LCC覆盖率，信息全局可达性 | $\|LCC\|/N$ | [0,1]，天然有界 |
| **$H$** | 层级深度 | Hierarchical Depth | k-core嵌套层级，网络组织深度 | $\min(k_{max}/k_{null}/6.667,\ 1)$ | [0,1]，人类HCP锚定为1.0 |
| **$M$** | 模块化 | Modularity | Newman-Girvan功能分区程度 | $\max[(Q-0.02)/(1-0.02),\ 0.01]$ | [0,1]，floor=0.01防塌陷 |
| **$R_{sw}$** | 小世界性 | Small-World Coefficient | Watts-Strogatz局部聚类+全局传输平衡 | $\tanh[(\sigma-1)/2]$ | [0,1]，σ=1→0，σ=4.1(人类)→0.914 |

**符号历史**：
- 第一版（2024）：X₁/X₂/X₃/X₄（下标编号，无物理含义）
- 第二版（2026-05-12）：ρ_G/κ_H/Q̃/σ̃（物理含义符号，过渡版）
- **第三版（2026-05-18）**：C/H/M/R_sw（借鉴图片原始定义，物理含义清晰，国际通用）

---

## 时间复杂度 Tc（动力学测度）

$$T_c = (\lambda_{eff} \cdot \Phi \cdot \Psi \cdot \Theta)^{1/4}$$

| 符号 | 中文名 | 英文名 | 物理含义 | 测量方法 |
|------|--------|--------|---------|---------|
| **$\lambda_{eff}$** | 临界性 | Criticality | 神经雪崩分支比，SOC临界态 | Branching Ratio，目标≈1.0 |
| **$\Phi$** | 相位一致性 | Phase Synchrony | Kuramoto序参数，跨区同步程度 | NMI of oscillatory phases |
| **$\Psi$** | 可塑性 | Plasticity | 功能连接时变性，适应能力 | FC variability over time |
| **$\Theta$** | 时间尺度多样性 | Timescale Diversity | 多尺度动力学Shannon熵 | Shannon entropy of τ distribution |

---

## 时空耦合 Γst

$$\Gamma_{st} = \text{NMI}(M_s,\ M_T) \cdot \text{sign}(\text{Mantel}(D_A,\ D_{FC})) \in [-1, 1]$$

---

## 设备物理系数 α

$$\alpha = \ln(M_{eff})$$

| 设备类型 | $M_{eff}$ | $\alpha$ | 代表系统 |
|---------|-----------|---------|---------|
| Binary digital | 2 | 0.69 | 所有现有AI/GPU |
| 分级电位 | 13 | 2.56 | C.elegans，无脊椎动物 |
| 脉冲神经元 | 32 | 3.47 | Loihi-2，SpiNNaker2 |
| 人类皮层 | 50 | 3.91 | 人脑（保守估计） |

---

## 三层指标体系

| 指标 | 定义 | 用途 |
|------|------|------|
| **CST** | $(S_c \cdot T_c) \cdot e^{\alpha \cdot \Gamma_{st}}$ | 绝对智能潜力 |
| **IIL** | argmax_k{θ_k \| CST ≥ θ_k} | 本征智能等级（L0-L6） |
| **RI** | CST / E_env | 相对智能指数（任务相关）|
| **η_I** | CST / P_norm | 智能效率（P_norm=P/20W）|

---

## 六大IIL阈值

| 等级 | 常数 | 值 | 第一性原理来源 | 生物对应 |
|------|------|----|--------------|---------|
| L1 感知 | $1/\sqrt{2}$ | ≈0.707 | Shannon-Hartley，SNR_min=1 | C.elegans，蜜蜂 |
| L2 反应 | $1$ | 1.000 | 热力学第二定律，CST≥E_env | 章鱼，斑马鱼 |
| L3 适应 | $\varphi$ | ≈1.618 | 黄金分割，资源分配最优 | 乌鸦，工具使用 |
| L4 创造 | $e$ | ≈2.718 | Landauer原理，信息生成上界 | 黑猩猩，海豚 |
| L5 通用 | $\pi$ | ≈3.142 | Kuramoto临界耦合，≥3子系统同步 | 人类 |
| L6 超级 | $\delta$ | ≈4.669 | Feigenbaum常数，倍周期分岔 | iNEST Gen4+ |

---

*基准确定时间：2026-05-18*  
*适用范围：所有CST相关论文、Demo、投资材料、技术文档*
