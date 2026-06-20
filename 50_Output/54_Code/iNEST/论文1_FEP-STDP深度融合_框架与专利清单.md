# 论文一：FEP-STDP 深度融合——面向物理自演化智能的神经网络架构

## 完整论文框架与专利保护清单

> 目标期刊：Nature Machine Intelligence / Science Advances  
> 专利策略：先申请临时专利(Provisional), 再提交论文  
> iNEST Research Team, Tianjin University | 2026-06-03

---

## 一、论文结构

### Title
**FEP-STDP Deep Fusion: A Physics-Grounded, Self-Evolving Neural Architecture for Green, Safe, and Scalable Intelligence**

### Authors
[iNEST Research Team], Tianjin University

### Abstract (250 words)

Current AI paradigms—exemplified by large language models—consume megawatts of power, require internet-scale training data, and operate as black boxes. Here we present a fundamentally different approach: a neural architecture that self-evolves its topology and synaptic properties by obeying the Free Energy Principle (FEP), Bienenstock-Cooper-Munro (BCM) metaplasticity, and the Principle of Least Action. Our SDI (Software-Defined Interconnect) architecture treats synaptic connections as evolvable "chemical bonds" with tunable activation energies (E-S↔E-L), driven by local free energy minimization rather than global backpropagation. Across five network scales (N=279 to N=1,953) grounded in real C.elegans connectome topology, we demonstrate: (1) simultaneous achievement of small-world structure (σ=5.0→19.5) and consolidation homeostasis (EL=28-31%), both scale-invariant; (2) six biologically-grounded plasticity mechanisms including BCM sliding threshold, graded FEP convergence, heterosynaptic competition, and minimum-action feedback; (3) a complete NULL Convention Logic (NCL) asynchronous circuit mapping to FPGA, with a single Xilinx VCK190 chip supporting 279-node real-time simulation at 200M spikes/s. The architecture requires no labeled data, no backpropagation, and no global optimization—only local physical principles. This work establishes a pathway toward AI systems that are inherently interpretable, energy-efficient (μW-scale per chip), and safe by construction.

### Sections

#### 1. Introduction
- LLM 三大不可持续问题: 能耗(>1GWh/训练), 数据饥渴, 黑箱不可解释
- 物理自演化智能的愿景: 像大脑一样, 靠局部物理规律自组织
- 核心假设: FEP + BCM + 最小作用量 → 自演化涌现智能
- 本文贡献: 架构设计 + 五尺度验证 + FPGA 映射

#### 2. Theoretical Framework
- 2.1 变分自由能 (Karl Friston 2010)
- 2.2 BCM 滑动阈值 (Bienenstock-Cooper-Munro 1982)
- 2.3 最小作用量原理 (Hamilton 1834; 神经应用: Laughlin 2003)
- 2.4 三原理协同: F_local → basin → consolidation; surprise → BCM_eta; dS/dt → rate

#### 3. SDI Architecture: Six Grounded Mechanisms
- 3.1 FEP 分级收敛 (sigmoid, 非二值)
- 3.2 BCM 滑动阈值 + 惊讶度耦合 (v28)
- 3.3 FEP 周期固化 (蛋白合成窗口)
- 3.4 异突触竞争 (资源有限→胜者多占)
- 3.5 节点能量约束 (轴突输送物理上限)
- 3.6 最小作用量反馈 (代谢效率驱动)

#### 4. Multi-Scale Validation
- 4.1 实验设置: C.elegans 连接组 ×1-×7 (N=279-1953)
- 4.2 σ(N) 标度律: 随N增长 (5.0→19.5)
- 4.3 EL(N) 标度不变: 锁定 28-31%
- 4.4 标度律: bonds ∝ N^1.05, time ∝ N^1.40
- 4.5 v8→v28 版本演进全景

#### 5. FPGA Hardware Mapping
- 5.1 NCL 异步电路原理与优势
- 5.2 SDI Bond Core Verilog RTL
- 5.3 BCM 阈值模块硬件化
- 5.4 资源估计: VCK190 → 279 nodes OK, max 341

#### 6. Discussion
- 6.1 与 LLM 对比: 能耗(μW vs MW), 数据需求(0 vs internet-scale)
- 6.2 安全性: 局部物理约束 → 天然可解释
- 6.3 绿色 AI: 事件驱动 → 仅活动部分耗电
- 6.4 局限性: 当前仅网络特征涌现, 尚未功能涌现

#### 7. Methods
- 7.1 SDI 仿真器 (Python, v28)
- 7.2 连接组缩放方法
- 7.3 评估指标: σ, EL, k_avg, 标度律指数

---

## 二、专利保护清单

### 专利 1: FEP-STDP 深度融合的可塑性规则

**发明名称**: 基于自由能原理和BCM滑动阈值的自演化突触可塑性方法

**技术领域**: 神经形态计算 / 脉冲神经网络硬件

**要保护的核心创新**:

1. **FEP 分级收敛度调制 STDP 速率**
   - 权利要求: 一种突触可塑性方法，其中突触前神经元的自由能盆地收敛度 (F_convergence ∈ [0,1]) 调制该神经元所有传出突触的 LTP 增强因子和 LTD 抑制因子:
     ```
     LTP_rate = ETA_LTP × (1 + α × F_convergence)
     LTD_rate = ETA_LTD × (1 - β × F_convergence)
     ```
   - 区别于现有技术: 现有 STDP 使用固定速率，本发明首次将 FEP 收敛度作为连续调制信号。

2. **BCM 滑动阈值 + 惊讶度耦合**
   - 权利要求: 一种突触固化判定方法，其中每个神经元的 LTP/LTD 阈值 θ_bcm 按以下公式滑动:
     ```
     θ(t+1) = θ(t) + η × h_avg² × (h_avg - θ) × (1 + γ × tanh(surprise))
     ```
   - 惊讶度 surprise = |F_local - μ(F_history)| / σ(F_history)
   - 区别于现有技术: 现有 BCM 规则不包含自由能惊讶度耦合项。

3. **双路径 E-S→E-L 固化机制**
   - 权利要求: 一种突触从短时程态(E-S)向长时程态(E-L)转换的方法，包含:
     (a) STDP 驱动的 BCM 条件路径: 当 LTP 计数超过当前 θ_bcm 时触发
     (b) FEP 驱动的周期固化路径: 每 T 步，FEP 收敛节点的 E-S 边以自适应概率 p 直接转换为 E-L
   - 自适应概率 p 受 EL 偏差和最小作用量 dS/dt 共同调制。

### 专利 2: 软硬件协同的 NCL 异步自演化神经处理器

**发明名称**: 基于 NULL Convention Logic 的 FEP-STDP 自演化神经处理器及其 FPGA 实现

**技术领域**: 集成电路 / 异步电路设计

**要保护的核心创新**:

1. **NCL 双轨编码的脉冲突触 IP 核**
   - 权利要求: 一种异步脉冲突触处理单元，采用 NCL 四态双轨编码 (DATA0/DATA1/NULL/INVALID) 表示脉冲信号，包含:
     - NCL 输入缓冲器 (双轨 → 单轨解码)
     - FEP 调制的 STDP 状态机 (LTP/LTD 衰减式计数器)
     - 固化检测比较器 (BCM 阈值比较)
     - NCL 完成检测器
   - 无全局时钟，仅靠数据流自定时。

2. **BCM 滑动阈值的硬件化模块**
   - 权利要求: 一种硬件实现的 BCM 滑动阈值计算单元，包含:
     - 滚动平均寄存器 (EMA: h_avg = α·h_avg + (1-α)·h_current)
     - 惊讶度计算电路 (tanh 近似: x/(1+|x|))
     - Q8.8 定点乘法器 (h², h_diff, delta 计算)
     - 阈值钳位电路 (BCM_MIN ≤ θ ≤ BCM_MAX)

3. **周期固化定时器 + 自适应率调节器**
   - 权利要求: 一种自适应固化率控制器，基于:
     - EL 偏差: 当前 E-L 比例与目标区间的偏差
     - 最小作用量 dS/dt: 效率变化率
   - 输出自适应固化概率 p ∈ [p_min, p_max]

4. **连通性保持的剪枝门控**
   - 权利要求: 一种突触剪枝方法，在删除一条突触前检查源节点剩余出度，若低于最小出度阈值 (MIN_OUT_DEG) 则保留该突触。

### 专利 3: 多尺度连接组自演化仿真平台

**发明名称**: 基于真实生物连接组的神经网络自演化仿真方法及系统

**要保护的核心创新**:

1. **连接组缩放方法**: 将基准连接组复制 N 份并添加跨模块稀疏连接以生成更大规模的仿真网络
2. **动态 σ 计算**: 基于权重阈值化图 (w > threshold) 的实时小世界系数计算
3. **标度律自动分析**: bonds ∝ N^α, time ∝ N^β 的自动拟合与报告

### 专利 4: 异突触竞争 + 每节点能量约束的稳态可塑性

**要保护的核心创新**:

1. **异突触抑制**: 当一个突触 E-S→E-L 固化时，同一源节点的其他 E-S 突触权重乘以 (1-HETERO_SUPPRESS)
2. **每节点能量约束**: 每个神经元传出总权重超过 PER_NODE_ENERGY_CAP 时等比缩放所有传出权重

---

## 三、专利撰写优先级

| 优先级 | 专利 | 核心权利要求数 | 建议申请类型 |
|--------|------|-------------|------------|
| P0 | 专利1: FEP-STDP 可塑性 | 3 | 发明专利 + PCT |
| P0 | 专利2: NCL 神经处理器 | 4 | 发明专利 + 集成电路布图 |
| P1 | 专利4: 稳态可塑性 | 2 | 发明专利 |
| P2 | 专利3: 仿真平台 | 3 | 发明专利 / 软件著作权 |

### 专利申请时间线

```
2026-06-15: 完成专利1,2 中文初稿
2026-06-20: 提交中国国家知识产权局 (CNIPA) 临时申请
2026-07-01: 提交 PCT 国际申请
2026-07-15: 论文投稿 (此时临时申请已保护优先权)
```

---

## 四、论文撰写任务分解

| 章节 | 依赖 | 预计字数 | 负责人 |
|------|------|---------|--------|
| Abstract | 全部完成 | 250 | — |
| 1. Introduction | 文献调研 | 1500 | — |
| 2. Theoretical Framework | Friston+BCM文献 | 2000 | — |
| 3. SDI Architecture | v28代码+6机制 | 2500 | — |
| 4. Multi-Scale Validation | v27+v28结果 | 2000 | — |
| 5. FPGA Mapping | Verilog+资源估计 | 1500 | — |
| 6. Discussion | 对比分析 | 1000 | — |
| Figures | 所有结果图 | 6-8 图 | — |
| Supplementary | 参数表+代码 | — | — |

---

*论文1框架 | iNEST Research Team | 2026-06-03*
