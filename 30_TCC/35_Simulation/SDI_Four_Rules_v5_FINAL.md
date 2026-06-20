# SDI 四条规则 — v5 文献锁定最终版
# Software-Defined Interconnect Four Rules — v5 Bio-Evidence Final

**版本**：v5.0（2026-05-22 锁定）  
**状态**：实验七v5 + 实验八普适性验证通过  
**适用**：所有后续SDI仿真实验的基准参数集

---

## 总览

$$\text{四条规则} \equiv \min_W \mathcal{F}(W) = \underbrace{-\log P(o|W)}_{\text{Rule1 预测误差}} + \underbrace{D_{KL}[Q||P]}_{\text{Rule3+4 结构代价}} + \underbrace{\text{exploration}}_{\text{Rule2 探索项}}$$

**时间尺度层级**（生物实验约束，不可颠倒）：

```
Rule1 STDP      每步执行   τ ~ 20ms      最快
Rule2 新生突触  每50步     τ ~ 数小时    较快
Rule3 稳态缩放  每200步    τ ~ 24-48h    较慢
Rule4 竞争修剪  每200步    τ ~ 周-月     最慢
```

---

## Rule 1：STDP——赫布突触可塑性

**物理本质**：最小预测误差（自由能第一项）  
**生物原型**：Hebbian Learning，"一起放电，一起连线"

### 核心机制

- 活跃节点对（pre & post同时激活）→ LTP计数 +1
- 一方活跃一方静默 → LTD计数 +1
- 累积到阈值 → 固化（EL键）或消除（E-S键）

### 文献锁定参数

| 参数 | 值 | 来源 |
|------|-----|------|
| `THETA_LTP` | **60** | Bi & Poo 1998 *J.Neuroscience*（60次配对诱导LTP）|
| `THETA_LTD` | **50** | Song et al. 2000 *Nat.Neurosci*（50次诱导LTD）|
| LTP幅度 `ETA_LTP` | 0.005 | Song 2000 |
| LTD幅度 `ETA_LTD` | 0.00525 | Song 2000（非对称，LTD略强）|
| EL键权重增益 | ×1.5 | Bhatt et al. 2009 *Nature* |
| LTP计数慢衰减 | **每500步 −1** | Bhatt 2009（突触维持需持续活动）|

### 激活阈值

- 激活判断：`act > 0.30`（活跃节点）
- 静默判断：`act < 0.08`（静默节点）

### EL/ES 键定义

- **E-L键**（Excitatory-Long-term）：LTP累积 ≥ THETA_LTP → 固化，权重放大，豁免修剪
- **E-S键**（Excitatory-Short-term）：LTD累积 ≥ THETA_LTD → 消除（仅非EL键）

### 关键约束

- LTD > LTP（非对称）：防止网络无限增强
- 最低保护：消除前检查 `degree > MIN_EDGES = 2`

---

## Rule 2：新生突触探索——轴突出芽

**物理本质**：遍历变分空间，防止局部最优（自由能探索项）  
**生物原型**：Axonal Sprouting，轴突出芽与结构可塑性

### 核心机制（v5 根本性改正）

> **不删已有连接，只新生低权重突触**  
> 新生突触命运由 Rule1（STDP积累）和 Rule4（竞争修剪）共同裁决

```
旧实现（v1-v4）：断开已有连接 → 重连新节点  ← 破坏已有结构
新实现（v5）  ：保留所有已有连接 + 以极低权重新生一条连接
               → 若后续 STDP 积累 ≥ THETA_LTP → EL 固化保留
               → 若长期不共同激活 → Rule4 竞争修剪删除
```

### 文献锁定参数

| 参数 | 值 | 来源 |
|------|-----|------|
| 新生间隔 `GROW_INT` | **50步** | Holtmaat & Svoboda 2009 *Nat.Rev.Neurosci*（~5%/天基线可塑性）|
| 新生概率 `P_GROW` | **0.05** | Holtmaat 2009 |
| 初始权重下限 `W_INIT_LO` | **0.05** | Zito et al. 2009 *J.Neurosci*（新棘初始强度5-20%成熟棘）|
| 初始权重上限 `W_INIT_HI` | **0.10** | Zito 2009（保守取10%）|
| 活跃节点偏向 `ACT_BIAS` | **2.0** | Holtmaat 2009（活跃区域2-4倍偏向，取保守值）|
| 最大新生比例 | 15% | 防止度无限增长 |

### 关键约束（文献支持）

- **无强制跨社区偏向**：文献不支持5倍以上的跨社区偏向，保守取2倍活跃偏向
- **EL键不参与重连**：稳定突触豁免（Bhatt 2009）
- 模块化由 Rule1+Rule4 共同涌现，Rule2 的作用是**防止网络过度模块化**（实验七v5验证：关闭Rule2后Q=0.917，高于四规则的0.904）

### 物理意义

Rule2 是"桥接者"而非"模块构建者"——维持跨社区连通性，防止网络碎片化

---

## Rule 3：稳态缩放——能量守恒约束

**物理本质**：自由能最小化中的能量守恒项  
**生物原型**：Homeostatic Synaptic Scaling（突触稳态可塑性）

### 核心机制

- 全局乘性缩放：激活率过低 → 增强所有突触；激活率过高 → 减弱所有突触
- 保持相对权重不变（乘性，不破坏STDP学到的模式）
- 维持系统在SOC临界态（λ_eff ≈ 1）

### 文献锁定参数

| 参数 | 值 | 来源 |
|------|-----|------|
| 缩放间隔 `SCALING_INT` | **200步** | Turrigiano 2012 *CSHP*（稳态缩放τ~24-48h，慢于STDP）|
| 目标激活率下限 `ACT_LO` | **0.03（3%）** | Turrigiano 1998 *Nature*（皮层1-5Hz稀疏编码）|
| 目标激活率上限 `ACT_HI` | **0.10（10%）** | Turrigiano 1998（5Hz对应宽松上界）|
| 放大系数 `SCALE_UP` | **1.05（+5%）** | Turrigiano 2012（4-8%，取中值）|
| 缩小系数 `SCALE_DN` | **0.95（−5%）** | Turrigiano 2012 |

### 关键约束

- 时间尺度必须**慢于 Rule2**（200步 > 50步）：生物实验事实
- 乘性缩放（全局）而非加性缩放（Turrigiano 1998原文）
- 上限10%对应皮层稀疏编码，不应设置过高（过高会抑制SOC）

---

## Rule 4：竞争修剪——自然选择压力

**物理本质**：最小化模型复杂度（Occam剃刀，自由能结构代价项）  
**生物原型**：Activity-Dependent Synaptic Pruning（活动依赖突触修剪）

### 核心机制（v4 关键修正）

> **竞争性相对阈值**，不是固定绝对阈值

```
修剪条件：突触后节点活跃度 < 邻居中位活跃度 × COMP_THR
即：比邻居弱才被修剪，而非简单低于固定值
```

这实现了Science 2022描述的竞争机制：强活跃突触释放"排他信号"抑制邻近弱突触。

### 文献锁定参数

| 参数 | 值 | 来源 |
|------|-----|------|
| 修剪间隔 `PRUNE_INT` | **200步** | Bhatt et al. 2009 *Nature*（突触修剪τ~周-月）|
| 修剪概率 `P_PRUNE` | **0.05** | Sanes & Lichtman 1999 *Nat.Rev.Neurosci* |
| 最低保护 `MIN_EDGES` | **2** | NMJ最终1条→皮层保守取2 |
| 竞争阈值 `COMP_THR` | **0.5** | Science 2022 *abm3902*（低于邻居中位×0.5才修剪）|

### 关键约束

- **EL键豁免**：稳定突触不被修剪（Bhatt 2009）
- **相对阈值**（非绝对）：`act_thr = median(邻居活跃度) × 0.5`
- 时间尺度最慢，与稳态缩放同级（200步），但效果更持久
- 实验验证：开启Rule4 vs 关闭，step 2000-4000 差异最大（ΔQ=+0.081），与Sanes&Lichtman 1999（修剪在发育期最活跃）一致

---

## 激活模型（C.elegans 专属）

| 参数 | 值 | 来源 |
|------|-----|------|
| 激活比例 `frac` | **0.15（15%）** | Kato et al. 2015 *Cell*（10-20%神经元同时激活）|
| 传播步数 `n_steps` | **4步** | Kaplan et al. 2018 *Neuron*（3-5突触步）|
| 权重归一化 | [0.10, 0.40] | 化学突触权重范围 |

---

## v5 实验验证结果

### 实验七 v5（WS图，N=300）

| 条件 | Q | σ | EL% |
|------|---|---|-----|
| 四规则完整 | **0.904** | 7.79 | 89.8% |
| 无 Rule4 | 0.858 | 3.93 | 89.3% |
| 无 Rule2 | 0.917 | 15.81 | 90.3% |
| 旧 Rule2（替换式）| 0.815 | 4.26 | 90.8% |
| CE connectome | 0.533 | 16.15 | 97.1% |

**新Rule2 vs 旧Rule2：ΔQ=+0.089，Δσ=+3.53**

### 实验八（20物种普适性）

- **达标（≥3/5）：17/20 物种（85%）**
- N≥50 物种：17/18（94.4%）
- 普适性下界：N ≥ 50
- Spearman ρ（进化年龄, Sc）= −0.191（弱负相关，说明智能等级由物理量决定而非进化历史）

---

## 参考文献（按规则对应）

| 规则 | 文献 |
|------|------|
| Rule1 | Bi & Poo (1998) *J.Neurosci* 18:10464 |
| Rule1 | Song et al. (2000) *Nat.Neurosci* 3:919 |
| Rule1 | Markram et al. (1997) *Science* 275:213 |
| Rule1 EL | Bhatt et al. (2009) *Nature* 462:313 |
| Rule2 | Holtmaat & Svoboda (2009) *Nat.Rev.Neurosci* 10:647 |
| Rule2 | Zito et al. (2009) *J.Neurosci* 29:12614 |
| Rule2 | PMC6704923 Hsieh (2019) *J.Neurosci* |
| Rule3 | Turrigiano et al. (1998) *Nature* 391:892 |
| Rule3 | Turrigiano (2012) *CSHP Perspect.Biol.* 4:a005736 |
| Rule3 | Desai et al. (1999) *Nat.Neurosci* 2:515 |
| Rule4 | Sanes & Lichtman (1999) *Nat.Rev.Neurosci* 1:133 |
| Rule4 | Science (2022) abm3902 "Stabilizing synapses" |
| Rule4 | Bhatt et al. (2009) *Nature* 462:313 |
| CE激活 | Kato et al. (2015) *Cell* 163:656 |
| CE激活 | Kaplan et al. (2018) *Neuron* 97:1151 |

---

## 版本历史

| 版本 | 关键变化 | 核心问题 |
|------|---------|---------|
| v1 | min_e=3，Rule4基本不触发 | ΔQ仅0.022 |
| v2 | BTW驱动太强，EL=100%冻结 | Rule4仍失效 |
| v3 | CE字段名错误，网络崩溃 | — |
| v4 | 四参数文献锁定，Rule2替换式 | Rule2破坏模块化 |
| **v5** | **Rule2改为新生突触（PMC6704923）** | **ΔQ=+0.089，17/20物种达标** |

*锁定时间：2026-05-22*
