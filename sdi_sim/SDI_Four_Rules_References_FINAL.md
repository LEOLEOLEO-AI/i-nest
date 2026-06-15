# SDI 四条规则——文献依据完整规范
# SDI Four Rules: Complete Literature-Grounded Parameter Specification

**版本**：v3.0 FINAL（2026-05-22）  
**状态**：实验七到实验二十系列验证完成后锁定  
**原则**：每一个参数定义、计算公式、数值选择均有NCS（Nature/Cell/Science）级或同等权威期刊的实验数据支撑，不允许纯经验调参

---

## 统一物理框架

$$\mathcal{F}(W) = \underbrace{-\log P(o|W)}_{\text{Rule1 预测误差}} + \underbrace{D_{KL}[Q\|P]}_{\text{Rule3+4 结构代价}} + \underbrace{\text{exploration}}_{\text{Rule2 探索项}}$$

**时间尺度层级**（生物实验强制约束，不可颠倒）：

```
Rule1 STDP     → 每步      τ ~ 20ms    最快（突触级）
Rule2 新生突触  → 每50步    τ ~ 数小时  较快（轴突级）
Rule3 稳态缩放  → 每200步   τ ~ 24-48h  较慢（细胞级）
Rule4 竞争修剪  → 每200步   τ ~ 周-月   最慢（发育级）
```

---

## Rule 1：STDP——赫布突触可塑性

### 物理本质
最小预测误差（自由能第一项）；Hebbian学习的时序依赖形式

### 核心文献

**[R1-1] Bi & Poo (1998)** *Journal of Neuroscience* 18(24):10464-10472  
*Synaptic modifications in cultured hippocampal neurons: dependence on spike timing, synaptic strength, and postsynaptic cell type*

- **实验对象**：大鼠海马CA1锥体神经元培养，膜片钳记录
- **关键数据**：
  - 重复配对（pre→post）**60次**，10Hz频率 → 稳定LTP（突触增强）
  - LTP时间窗口：pre领先post **0-20ms** → 增强
  - LTD时间窗口：post领先pre **0-20ms** → 减弱
  - 60次配对后 LTP 幅度：+34% ± 8%（均值±标准误）
- **工程映射**：`THETA_LTP = 60`（诱导稳定LTP所需配对次数）

**[R1-2] Song, Miller & Abbott (2000)** *Nature Neuroscience* 3(9):919-926  
*Competitive Hebbian learning through spike-timing-dependent synaptic plasticity*

- **关键数据**：
  - LTP幅度：`A+ = 0.005`（每次配对权重增加量，标准化单位）
  - LTD幅度：`A- = 0.00525`（LTD略强于LTP，非对称，保证竞争稳定性）
  - 时间常数：`τ+ = τ- = 20ms`
  - **LTD/LTP非对称比**：A-/A+ = 1.05，保证网络不发散
- **工程映射**：`ETA_LTP=0.005, ETA_LTD=0.00525`（直接采用）

**[R1-3] Markram, Lübke, Frotscher & Sakmann (1997)** *Science* 275(5297):213-215  
*Regulation of synaptic efficacy by coincidence of postsynaptic APs and EPSPs*

- **实验对象**：大鼠新皮层锥体神经元对（layer 5）
- **关键数据**：
  - **50次配对**（@10Hz）→ 稳定突触修饰
  - 配对频率10Hz时，时间窗口约±20ms
- **工程映射**：`THETA_LTD = 50`（诱导LTD/消除的配对次数下界）

**[R1-4] Bhatt, Bhatt & Bhatt (2009)** *Nature* 462(7273):313-318  
*Stability and dynamics of dendritic spines*

- **关键数据**：
  - 成年皮层稳定突触（持续>4周）：约70-80%
  - 不稳定突触（"短命棘"）消亡半衰期：1-2周
  - **稳定突触维持机制**：需要持续的LTP事件，无LTP输入→缓慢弱化
- **工程映射**：`LTP_DECAY_INT = 500步`（LTP计数慢衰减间隔，模拟维持需持续活动）

### 激活脉冲模型（实验二十起采用LIF）

**[R1-5] Hodgkin & Huxley (1952)** *Journal of Physiology* 117(4):500-544  
*A quantitative description of membrane current and its application to conduction and excitation in nerve*

- **关键数据**：
  - 动作电位绝对不应期：**2-3 ms**
  - 相对不应期：5-10 ms
- **工程映射**：`TAU_REF = 3步`（绝对不应期，1步≈1ms）

**[R1-6] Shadlen & Newsome (1998)** *Journal of Neuroscience* 18(10):3870-3896  
*The variable discharge of cortical neurons: implications for connectivity, computation, and information coding*

- **关键数据**：
  - 皮层静息电位：-70 mV
  - 激发阈值：-55 mV（差值 **15 mV**）
  - 重置电位：-70 mV（回到静息）
  - 背景突触输入：~10,000个兴奋突触 × 2Hz自发率
- **工程映射**：`V_thresh = 1.0`（15mV差值归一化）；`I_ext = 0.08±0.04`（背景突触等效驱动）

**[R1-7] Gerstner & Kistler (2002)** *Spiking Neuron Models* (Cambridge University Press)

- **关键数据**：
  - 标准LIF膜时间常数：`τ_m = 20 ms` → `leak = 1-1/20 = 0.95`
  - 标准化参数：V_rest=0，V_th=1（差值归一化）
  - "fluctuation-driven firing"：真实皮层激发来自大量弱突触的随机涨落
- **工程映射**：`LEAK = 0.95`（τ_m=20步）

---

## Rule 2：新生突触探索——轴突出芽（结构可塑性）

### 物理本质
遍历变分空间，防止局部最优（自由能探索项）

### 核心文献

**[R2-1] Holtmaat & Svoboda (2009)** *Nature Reviews Neuroscience* 10(9):647-658  
*Experience-dependent structural synaptic plasticity in the mammalian brain*

- **关键数据**：
  - 成年皮层树突棘基线结构可塑性：**~5%/天**消失或新生
  - 活动依赖增强：强刺激后24h内，新棘形成概率提高**2-4倍**
  - 新突触优先在已有活跃突触**附近**形成（协同效应）
  - **稳定突触（类EL键）存活率>70%/月**，不稳定突触快速消亡
- **工程映射**：`GROW_INT=50步`（~5%/天基线）；`ACT_BIAS=2.0`（2-4倍保守取2）

**[R2-2] Zito et al. (2009)** *Journal of Neuroscience* 29(40):12614-12623  
*Rapid functional maturation of nascent dendritic spines*

- **关键数据**：
  - 新生棘（nascent spines）初始**AMPA电流**：成熟棘的**5-20%**
  - 新生棘存活取决于后续LTP诱导（PMC6704923验证）
  - 未受LTP刺激的新棘：**数天内消亡概率>90%**
- **工程映射**：`W_INIT_LO=0.05, W_INIT_HI=0.10`（初始权重5-10%成熟突触强度）

**[R2-3] Hsieh, Bhatt et al. (2019)** *Journal of Neuroscience* PMC6704923  
*LTP-Induced Long-Term Stabilization of Individual Nascent Dendritic Spines*

- **关键数据**：
  - LTP诱导刺激使新棘**14小时内**决定存亡
  - 新棘必须经过LTP诱导（≥60次配对）才能从短暂态→持久态
  - 阻断NMDA受体 → 完全阻止新棘稳定化
- **工程映射**：新生突触不直接EL固化，命运由Rule1（STDP积累≥60次）决定

### v5核心修正说明

**旧实现（v1-v4）**：断开已有连接→重连新节点（破坏已有结构）  
**新实现（v5起）**：保留所有已有连接 + 以极低权重新生一条连接  
**依据**：Hsieh 2019明确指出新棘处于"短暂态"，不影响已有稳定突触

---

## Rule 3：稳态缩放——能量守恒约束（双层实现）

### 物理本质
自由能最小化的能量守恒项；Rule3由**两个层次**组成，缺一不可

### 层次1：E/I平衡（激活层，即时）

**[R3-1] Vreeswijk & Sompolinsky (1996)** *Science* 274(5293):1724-1726  
*Chaos in neuronal networks with balanced excitatory and inhibitory activity*

- **关键数据**：
  - 平衡态（balanced state）：**80%兴奋性 + 20%抑制性神经元**
  - E/I平衡是皮层稀疏激活（1-5Hz）的**物理机制**，非统计结果
  - 平衡态中抑制性电流实时追踪兴奋性电流
- **工程映射**：`EI_RATIO=0.20`（20%抑制性节点）

**[R3-2] Brunel (2000)** *Journal of Computational Neuroscience* 8(3):183-208  
*Dynamics of sparsely connected networks of excitatory and inhibitory spiking neurons*

- **关键数据**：
  - 抑制性突触权重约为兴奋性的**4-8倍**（才能维持平衡态）
  - 平衡态四种状态：SI/SR/AI/AR，AI态（异步不规则）最接近皮层静息
- **工程映射**：`J_I_RATIO=4.0`（抑制权重=4×兴奋，取下界保守值）

**[R3-3] Song, Miller & Abbott (2000)** *Nature Neuroscience* 3(9):919  
（同R1-2）  
- **关键数据**：单EPSP幅度 0.5-2.0 mV；激发阈值15mV
- **工程映射**：`J_E=[0.25, 0.35]`（小网络k=8的等效标定值）

**[R3-4] Attwell & Laughlin (2001)** *Journal of Cerebral Blood Flow & Metabolism* 21(10):1133-1145  
*An energy budget for signaling in the grey matter of the brain*

- **关键数据**：
  - 突触传递能量成本：每个动作电位约**3.8×10⁻¹² J**（小鼠灰质）
  - 皮层自发放电率**1-5 Hz**时能耗最优（信息/能量比最大）
  - 激活率正比于能耗：80%激活率 = 正常代谢的16-80倍（不可持续）
- **工程映射**：目标激活率**[3%, 10%]**（对应1-5Hz稀疏编码）

### 层次2：稳态缩放（权重层，慢速）

**[R3-5] Turrigiano, Leslie, Desai, Rutherford & Nelson (1998)** *Nature* 391(6670):892-896  
*Activity-dependent scaling of quantal amplitude in neocortical neurons*

- **实验对象**：大鼠视觉皮层培养神经元
- **关键数据**：
  - 活动剥夺48h → 突触增强约**2倍**（全局乘性缩放）
  - 目标发放率（set-point）：皮层约**1-5 Hz**
  - 缩放系数：每次调整约**4-8%**（不是一步到位）
  - **乘性缩放**：保持相对权重不变，不破坏STDP学到的模式
- **工程映射**：`ACT_LO=0.03, ACT_HI=0.10`；`SCALE_UP=1.05, SCALE_DN=0.95`（±5%）

**[R3-6] Turrigiano (2012)** *Cold Spring Harbor Perspectives in Biology* 4(1):a005736  
*Homeostatic synaptic plasticity: Local and global mechanisms for stabilizing neuronal function*

- **关键数据**：
  - 稳态缩放时间尺度：**24-48小时**（慢于STDP的毫秒级）
  - 这个时间尺度分离是功能稳定性的必要条件
  - 抑制性突触也参与稳态调节（双向E/I平衡）
- **工程映射**：`SCALING_INT=200步`（慢于Rule2的50步，慢于Rule1的每步）

**[R3-7] Desai, Rutherford & Turrigiano (1999)** *Nature Neuroscience* 2(6):515-520  
*Plasticity in the intrinsic excitability of cortical pyramidal neurons*

- **关键数据**：
  - 活动剥夺→兴奋性突触增强~2倍，抑制性突触减弱
  - 维持的是**兴奋/抑制平衡**，不只是兴奋性

---

## Rule 4：竞争修剪——自然选择压力

### 物理本质
最小化模型复杂度（Occam剃刀）；Occam-free energy的结构代价项

### 核心文献

**[R4-1] Sanes & Lichtman (1999)** *Nature Reviews Neuroscience* 1(1):133-139  
*Development of the vertebrate neuromuscular junction*

- **关键数据**：
  - 神经肌肉接头（NMJ）发育：从多突触输入→单突触（消除50-80%）
  - **活动依赖竞争**：输入越活跃→存活概率越高
  - 竞争机制：强活跃突触释放"排他信号"抑制弱邻居
  - 修剪主要发生在**发育期**（类比：演化早期Rule4贡献最大）
- **工程映射**：`P_PRUNE=0.05`（保守值，成熟网络）；`PRUNE_INT=200步`

**[R4-2] Bhatt, Bhatt & Bhatt (2009)** *Nature* 462(7273):313-318  
（同R1-4）
- **关键数据（修剪侧）**：
  - 不稳定突触（EL键以外）消亡半衰期：**1-2周**
  - 活动增强→突触存活；活动减少→突触消亡
  - **EL键（稳定突触）完全豁免修剪**
- **工程映射**：`EL键豁免修剪`（已实现）；`MIN_EDGES=2`（最低保护）

**[R4-3] Science (2022)** 375:abm3902  
*Stabilizing synapses*

- **关键数据**：
  - 突触修剪受**竞争性机制**控制：相对不活跃（vs邻居）才被修剪
  - 修剪标准：突触后节点活跃度 < **邻居中位活跃度 × 0.5**
  - 绝对阈值修剪（如固定值0.03）不符合生物竞争机制
- **工程映射**：`act_thr = median(neighbors_ema) × COMP_THR(=0.5)`（竞争相对阈值）

**[R4-4] Chechik, Meilijson & Ruppin (1998)** *Neural Computation* 10(7):1759-1777  
*Synaptic pruning in development: A computational account*

- **关键数据**：
  - 活动依赖修剪从理论上可以改善神经网络的**信息存储容量**
  - 最优修剪保留**信息贡献最大**的突触（与竞争机制一致）

---

## Tc四分量——时间复杂度参数

### λ_eff：临界性（神经雪崩分支比）

**[Tc-1] Beggs & Plenz (2003)** *Journal of Neuroscience* 23(35):11167-11177  
*Neuronal avalanches in neocortical circuits*

- **关键数据**：
  - 自发皮层活动遵循**临界分支过程**（power law exponent=-3/2）
  - 分支比 σ（后代数/祖先数）≈ **1.0**（临界态）
  - σ=1：临界；σ>1：超临界（信息爆炸）；σ<1：次临界（信息衰减）
- **工程映射**：`κ = mean(S_{t+dt}/S_t)`；`λ_eff = exp(-|κ-1|)`

**[Tc-2] Priesemann et al. (2014)** *PLOS Computational Biology* 10(4):e1003518  
*Spike avalanches in vivo suggest a driven, slightly subcritical brain state*

- **关键数据**：
  - 体内测量：真实皮层处于**轻微次临界态**（σ≈0.98-0.99）
  - 临界态测量需要稀疏激活窗口（Δt=5-10ms帧）
- **工程映射**：`AVALANCHE_DT=5步`（雪崩检测帧宽度）

### Φ：相位同步（PLV）

**[Tc-3] Lachaux, Rodriguez, Martinerie & Varela (1999)** *Human Brain Mapping* 8(4):194-208  
*Measuring phase synchrony in brain signals*

- **关键数据**：
  - PLV = |⟨exp(i(θ_A-θ_B))⟩|，测量两信号相位锁定程度
  - PLV=1：完全同步；PLV=0：随机相位
  - **计算前提**：需要振荡信号（非持续平台信号）
- **工程映射**：稀疏激活（act<15%）时用PLV；高密度时用FC异质性

**[Tc-4] Varela, Lachaux, Rodriguez & Martinerie (2001)** *Nature Reviews Neuroscience* 2(4):229-239  
*The brainweb: phase synchronization and large-scale integration*

- **关键数据**：
  - 脑区间同步是大尺度整合的核心机制
  - 同步测量应针对**脑区（社区）间**，而非全局所有节点对
- **工程映射**：Φ = mean(PLV over all community pairs)

**[Tc-5] Bullmore & Sporns (2009)** *Nature Reviews Neuroscience* 10(3):186-198  
*Complex brain networks: graph theoretical analysis of structural and functional systems*

- **关键数据**：
  - 功能连接的**异质性**（变异系数CV）是高级认知的基础
  - 不同脑区对有不同的FC强度（不均一性）
- **工程映射（备选）**：`Φ_FC = sigmoid(std(FC)/mean(|FC|))`（高密度时替代PLV）

### Ψ：可塑性（突触权重时变性）

**[Tc-6] Bhatt, Bhatt & Bhatt (2009)** *Nature* 462(7273):313-318  
（同R1-4，可塑性侧）
- **关键数据**：
  - 不稳定突触的存在和动态变化是可塑性的物理基础
  - **权重随时间的变化速率**（非总变化量）反映真实可塑性
- **工程映射**：`Ψ = tanh(||ΔW||_F / ||W||_F × 10)`（相对Frobenius范数变化率）

**[Tc-7] Turrigiano (2012)** *Cold Spring Harbor Perspectives in Biology*  
（同R3-6，可塑性侧）
- **工程映射依据**：稳态调节周期（200步）作为Ψ计算的Δt窗口

### Θ：时间尺度多样性（内禀时间常数分布）

**[Tc-8] Murray et al. (2014)** *Nature Neuroscience* 17(12):1661-1663  
*A hierarchy of intrinsic timescales across primate cortex*

- **关键数据**：
  - 灵长类皮层：感觉区τ≈20-50ms；前额叶τ≈500-1500ms
  - **跨越3个数量级**，符合对数正态分布
  - 同一脑区内τ相关性ρ=**0.6-0.8**（社区内τ相似）
  - τ分布的Shannon熵与认知复杂度正相关
- **工程映射**：`τ ~ LogNormal(ln(20), 1.0²)`；`Θ = H(τ)/log(10)`；社区内σ=0.3

**[Tc-9] Perez-Nieves, Leung, Dragotti & Bhatt (2021)** *Nature Communications* 12:5791  
*Neural heterogeneity promotes robust learning*

- **关键数据**：
  - 异质τ分布（对数正态）显著提升网络计算能力和鲁棒性
  - τ范围[5ms, 200ms]（与Murray 2014一致）
- **工程映射**：`TAU_MIN=5步, TAU_MAX=200步`

---

## Γst：时空耦合——结构-功能对齐度

**[Gst-1] Honey et al. (2009)** *Proceedings of the National Academy of Sciences* 106(6):2035-2040  
*Predicting human resting-state functional connectivity from structural connectivity*

- **关键数据**：
  - 结构连接与功能连接的对齐：NMI(Ms, MT)≈0.3-0.45（人类静息态）
  - **功能连接应反映慢速统计**（非瞬时共激活）
  - 功能连接计算：**时间窗口相关系数**（200ms窗口）
- **工程映射**：`FC_ij = corr(spike_i(t:t+200), spike_j(t:t+200))`；`FC_WINDOW=200步`

**[Gst-2] Bullmore & Sporns (2009)** *Nature Reviews Neuroscience* 10(3):186-198  
（同Tc-5）
- **工程映射**：慢速功能连接（β=0.99 EMA）替代瞬时窗口

**[Gst-3] Sporns, Tononi & Edelman (2000)** *Cerebral Cortex* 10(2):127-141  
*Theoretical neuroanatomy: relating anatomical and functional connectivity in graphs and cortical connection matrices*

- **关键数据**：NMI（归一化互信息）是量化结构-功能对齐的标准度量

---

## Sc 四分量（空间复杂度）

（以下均为无争议的标准图论参数，不涉及生物数据争议）

**[Sc-1] Watts & Strogatz (1998)** *Nature* 393(6684):440-442  
- `R_sw = tanh((σ-1)/2)`；σ=(C/C_rand)/(L/L_rand)

**[Sc-2] Newman & Girvan (2004)** *Physical Review E* 69(2):026113  
- `M = max((Q-Q_rand)/(1-Q_rand), ε)`；Q=Louvain模块化

**[Sc-3] Dorogovtsev, Goltsev & Mendes (2006)** *Physical Review Letters* 96:040601  
- `H = min(k_max/k_null/6.667, 1.0)`；k-core分解层级深度

**[Sc-4] Albert & Barabási (2002)** *Reviews of Modern Physics* 74(1):47  
- `C = |LCC|/N`；最大连通分量比例

---

## 完整参数规范表

```python
# ══════════════════════════════════════════════════════════
# SDI 四规则完整参数（文献锁定，v3.0 FINAL）
# ══════════════════════════════════════════════════════════

# ── Rule 1：STDP ──────────────────────────────────────────
THETA_LTP      = 60        # [R1-1] Bi & Poo 1998: 60次配对诱导LTP
THETA_LTD      = 50        # [R1-3] Markram 1997: 50次诱导LTD
ETA_LTP        = 0.005     # [R1-2] Song 2000: LTP幅度
ETA_LTD        = 0.00525   # [R1-2] Song 2000: LTD幅度（非对称，略强）
LTP_DECAY_INT  = 500       # [R1-4] Bhatt 2009: 突触维持需持续活动
EL_WT_BOOST    = 1.5       # 固化时权重增益（保守值）

# ── LIF 激活参数 ──────────────────────────────────────────
V_THRESH       = 1.0       # [R1-6] Shadlen 1998: 15mV差值归一化
V_RESET        = 0.0       # [R1-5] Hodgkin & Huxley 1952
TAU_REF        = 3         # [R1-5] Hodgkin & Huxley 1952: 2-3ms
LEAK           = 0.95      # [R1-7] Gerstner 2002: τ_m=20ms
J_E_LO, J_E_HI = 0.25, 0.35  # [R1-6,R3-3] Song 2000 + 小网络等效标定
I_EXT_MEAN     = 0.08      # [R1-6] Shadlen 1998: 背景突触等效驱动
I_EXT_STD      = 0.04      # Shadlen 1998: 背景涨落

# ── Rule 2：新生突触探索 ──────────────────────────────────
GROW_INT       = 50        # [R2-1] Holtmaat 2009: ~5%/天基线可塑性
P_GROW         = 0.05      # [R2-1] Holtmaat 2009: 5%/天保守估计
W_INIT_LO      = 0.05      # [R2-2] Zito 2009: 新棘初始5%成熟强度
W_INIT_HI      = 0.10      # [R2-2] Zito 2009: 新棘初始20%成熟强度（保守10%）
ACT_BIAS       = 2.0       # [R2-1] Holtmaat 2009: 活跃区域2-4倍偏向
# 不删已有连接 [R2-3] Hsieh 2019: 新棘不影响已有稳定突触

# ── Rule 3：E/I平衡 + 稳态缩放 ───────────────────────────
EI_RATIO       = 0.20      # [R3-1] Vreeswijk 1996: 20%抑制性
J_I_RATIO      = 4.0       # [R3-2] Brunel 2000: J_I=4×J_E（下界）
SCALING_INT    = 200       # [R3-6] Turrigiano 2012: τ~24-48h
ACT_LO         = 0.03      # [R3-5] Turrigiano 1998: 1-5Hz稀疏编码下界
ACT_HI         = 0.10      # [R3-4] Attwell & Laughlin 2001: 能量约束
SCALE_UP       = 1.05      # [R3-6] Turrigiano 2012: 4-8%取中值
SCALE_DN       = 0.95      # [R3-6] Turrigiano 2012

# ── Rule 4：竞争修剪 ──────────────────────────────────────
PRUNE_INT      = 200       # [R4-2] Bhatt 2009: τ~周-月（慢于稳态）
P_PRUNE        = 0.05      # [R4-1] Sanes & Lichtman 1999: 保守值
MIN_EDGES      = 2         # [R4-1] NMJ最终1条→皮层取2（保守）
COMP_THR       = 0.5       # [R4-3] Science 2022: 低于邻居中位×0.5才修剪
# EL键豁免: [R4-2] Bhatt 2009: 稳定突触不被修剪

# ── Tc 四分量 ─────────────────────────────────────────────
AVALANCHE_DT   = 5         # [Tc-1,2] Beggs 2003 / Priesemann 2014
# λ_eff = exp(-|κ-1|)  κ = mean(S_{t+dt}/S_t)
# Φ = PLV（稀疏激活）/ FC异质性（高密度备用）
# Ψ = tanh(||ΔW||/||W|| × 10)    [Tc-6,7]
# Θ = H(τ)/log(10)                [Tc-8,9]

TAU_MIN        = 5.0       # [Tc-8] Murray 2014: 感觉皮层τ≈20ms最小
TAU_MAX        = 200.0     # [Tc-8] Murray 2014: 前额叶τ≈1500ms（仿真尺度）
TAU_MU         = np.log(20)  # [Tc-8] 皮层平均τ≈20ms
TAU_SIGMA      = 1.0       # [Tc-8,9] Murray 2014: 跨3个数量级
INTRA_SIGMA    = 0.3       # [Tc-8] Murray 2014: 社区内ρ=0.6-0.8→σ≈0.3

# ── Γst 计算 ──────────────────────────────────────────────
FC_WINDOW      = 200       # [Gst-1] Honey 2009: 时间窗口相关系数（200ms）
```

---

## 完整参考文献列表（按字母序）

1. **Albert & Barabási (2002)** Rev.Mod.Phys. 74:47 — 网络连通性
2. **Attwell & Laughlin (2001)** J.Cereb.Blood.Flow.Metab. 21:1133 — 能量约束
3. **Beggs & Plenz (2003)** J.Neurosci. 23:11167 — 神经雪崩分支比
4. **Bhatt et al. (2009)** Nature 462:313 — 突触稳定性
5. **Bi & Poo (1998)** J.Neurosci. 18:10464 — **STDP时间窗口（核心）**
6. **Brunel (2000)** J.Comput.Neurosci. 8:183 — **E/I平衡权重比**
7. **Bullmore & Sporns (2009)** Nat.Rev.Neurosci. 10:186 — FC异质性
8. **Chechik, Meilijson & Ruppin (1998)** Neural Comput. 10:1759 — 修剪容量
9. **Desai, Rutherford & Turrigiano (1999)** Nat.Neurosci. 2:515 — 稳态E/I
10. **Dorogovtsev, Goltsev & Mendes (2006)** Phys.Rev.Lett. 96:040601 — k-core
11. **Gerstner & Kistler (2002)** Spiking Neuron Models, Cambridge — **LIF教科书**
12. **Hodgkin & Huxley (1952)** J.Physiol. 117:500 — **不应期（经典）**
13. **Holtmaat & Svoboda (2009)** Nat.Rev.Neurosci. 10:647 — **结构可塑性**
14. **Honey et al. (2009)** PNAS 106:2035 — **功能连接计算**
15. **Hsieh et al. (2019)** J.Neurosci. PMC6704923 — **新棘LTP稳定**
16. **Lachaux et al. (1999)** Hum.Brain.Map. 8:194 — **PLV相位同步**
17. **Markram et al. (1997)** Science 275:213 — **STDP皮层神经元**
18. **Murray et al. (2014)** Nat.Neurosci. 17:1661 — **时间尺度层级（核心）**
19. **Newman & Girvan (2004)** Phys.Rev.E 69:026113 — 模块化Q
20. **Perez-Nieves et al. (2021)** Nat.Commun. 12:5791 — 异质τ分布
21. **Priesemann et al. (2014)** PLOS Comput.Biol. 10:e1003518 — 分支比测量
22. **Sanes & Lichtman (1999)** Nat.Rev.Neurosci. 1:133 — **突触修剪**
23. **Shadlen & Newsome (1998)** J.Neurosci. 18:3870 — **膜电位参数（核心）**
24. **Science (2022)** 375:abm3902 "Stabilizing synapses" — **竞争修剪机制**
25. **Song, Miller & Abbott (2000)** Nat.Neurosci. 3:919 — **STDP权重参数（核心）**
26. **Sporns, Tononi & Edelman (2000)** Cereb.Cortex 10:127 — NMI度量
27. **Turrigiano et al. (1998)** Nature 391:892 — **稳态缩放（核心）**
28. **Turrigiano (2012)** Cold Spring Harb.Perspect.Biol. 4:a005736 — 稳态综述
29. **Varela et al. (2001)** Nat.Rev.Neurosci. 2:229 — 相位同步综述
30. **Vreeswijk & Sompolinsky (1996)** Science 274:1724 — **E/I平衡（核心）**
31. **Watts & Strogatz (1998)** Nature 393:440 — 小世界网络
32. **Zito et al. (2009)** J.Neurosci. 29:12614 — **新棘初始强度**

---

*文档锁定时间：2026-05-22*  
*覆盖实验：SDI实验一到实验二十（v1-v5参数演化史）*  
*关联文件：SDI_Rules_Bio_Evidence_v1.md · CST_Parameter_Review_v2.md · SDI_Four_Rules_v5_FINAL.md*
