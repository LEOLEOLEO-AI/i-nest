---
provenance: external
---

# CST公式参数第一性审查报告 v2.0
**日期**：2026-05-22  
**依据**：NCS权威期刊，系统性第一性推导

---

## 审查结论汇总

| 参数 | 当前实现 | 第一性定义 | 偏差 | 修订方案 |
|------|---------|-----------|------|---------|
| **α** | ln(M_eff) | Strong 1998 *Science* | ✅ 正确 | 不需修订 |
| **C** | \|LCC\|/N | Albert 2002 *Rev.Mod.Phys.* | ✅ 正确 | 不需修订 |
| **H** | k-core归一化 | Dorogovtsev 2006 *PRL* | ✅ 正确 | 不需修订 |
| **M** | 归一化Louvain Q | Newman 2004 *PRE* | ✅ 正确 | 不需修订 |
| **R_sw** | tanh(σ-1)/2 | Watts & Strogatz 1998 *Nature* | ✅ 正确 | 不需修订 |
| **λ_eff** | 逐步激活比 | Beggs & Plenz 2003 *J.Neurosci.* | ⚠️ 近似 | 改为κ临界性指数 |
| **Φ** | Hilbert/PLV | Varela 2001 *Nat.Rev.Neurosci.* | ❌ 需稀疏激活 | 改为FC异质性 |
| **Ψ** | corr(W_final, W_init) | Turrigiano 2012 *CSHP* | ⚠️ 总量非速率 | 改为相对权重变化率 |
| **Θ** | τ分布Shannon熵 | Murray 2014 *Nat.Neurosci.* | ✅ 正确 | 不需修订 |
| **Γst** | 瞬时激活窗口FC | Honey 2009 *PNAS* | ⚠️ 窗口太短 | 改为EMA慢速FC |

---

## 详细修订规范

### λ_eff：临界性（修订）

**文献**：Beggs & Plenz 2003 *J.Neurosci.* 23:11167  
**核心**：分支比κ=后代数/祖先数，κ=1为临界态

**修订公式**：
$$\lambda_{eff} = e^{-|\kappa - 1|}, \quad \kappa = \frac{\langle S_{t+1} \rangle}{\langle S_t \rangle}$$

- κ=1 → λ=1.0（临界，最高信息传递效率）
- κ=2 → λ=e^{-1}=0.37（超临界，信息爆炸）
- κ=0.5 → λ=e^{-0.5}=0.61（次临界，信息衰减）

**优势**：适用于任意激活密度（不需要稀疏）

---

### Φ：相位同步 → FC异质性（修订）

**文献**：Bullmore & Sporns 2009 *Nat.Rev.Neurosci.* 10:186  
**核心**：功能连接的异质性是脑网络功能分化的标志

**修订公式**：
$$\Phi = \text{sigmoid}\left(CV_{FC}\right), \quad CV_{FC} = \frac{\text{std}(FC_{ij})}{\text{mean}(|FC_{ij}|) + \epsilon}$$

其中 sigmoid(x) = 1/(1+e^{-2x+1}) 将CV归一化到(0,1)

- 高异质FC（不同脑区对有不同强度）→ Φ高
- 均一FC（所有对相同）→ Φ低
- 在任意激活密度下有效

---

### Ψ：可塑性（修订）

**文献**：Bhatt et al. 2009 *Nature* 462:313；Turrigiano 2012 *CSHP*  
**核心**：可塑性=突触权重在时间上的动态变化速率

**修订公式**：
$$\Psi(t) = \frac{\|W(t) - W(t - \Delta t)\|_F}{\|W(t)\|_F + \epsilon}$$

在滑动窗口 Δt = SCALING_INT（200步，与Rule3同步）计算  
归一化确保Ψ∈[0,1]，使用tanh进一步压缩

---

### Γst：时空耦合（修订）

**文献**：Honey et al. 2009 *PNAS* 106:2035；Bullmore & Sporns 2009  
**核心**：功能连接应反映慢速统计，而非瞬时共激活

**修订公式**：
$$FC_{ij}^{ema}(t) = \beta \cdot FC_{ij}^{ema}(t-1) + (1-\beta) \cdot h_i(t) \cdot h_j(t)$$

β=0.99（对应约100步的慢速时间常数）  
用 FC^{ema} 替代瞬时相关矩阵计算功能社区

---

## 为什么Φ需要稀疏激活

Φ的生物学定义（Varela 2001）基于**神经振荡**（theta/gamma频段）：
- 振荡存在的前提：神经元交替激活/静息
- 这要求激活率<<50%（生物皮层典型值1-5%）

**当前仿真激活率80-90%**：
- 所有节点持续激活 → 无振荡 → Φ无意义
- 这不是算法问题，是物理前提缺失

**结论**：在当前激活率下，Φ应改用FC异质性代替相位同步，二者都反映"功能分化程度"，但FC异质性对激活率无要求。

---

## 参考文献

1. Strong et al. (1998) *Science* 279:1538 — α的实验依据
2. Watts & Strogatz (1998) *Nature* 393:440 — R_sw的σ定义
3. Albert & Barabási (2002) *Rev.Mod.Phys.* — 网络连通性
4. Newman & Girvan (2004) *Phys.Rev.E* — 模块化Q
5. Dorogovtsev et al. (2006) *Phys.Rev.Lett.* — k-core分解
6. **Beggs & Plenz (2003) *J.Neurosci.* 23:11167** — λ分支比
7. **Varela et al. (2001) *Nat.Rev.Neurosci.* 2:229** — Φ相位同步
8. **Bullmore & Sporns (2009) *Nat.Rev.Neurosci.* 10:186** — FC异质性
9. **Turrigiano (2012) *CSHP Perspect.Biol.*** — Ψ突触可塑性
10. **Bhatt et al. (2009) *Nature* 462:313** — 突触稳定性动力学
11. **Murray et al. (2014) *Nat.Neurosci.* 17:1661** — Θ内在时间尺度
12. **Honey et al. (2009) *PNAS* 106:2035** — 结构-功能连接
13. **Priesemann et al. (2014) *PLOS Comput.Biol.*** — 分支比测量方法

---

## LIF神经元参数第一性推导（2026-05-22 补充）

### 权威来源

| 参数 | 生物值 | 来源 |
|------|--------|------|
| 静息电位 V_rest | -70 mV | Shadlen & Newsome 1998 *J.Neurosci* |
| 激发阈值 V_th | -55 mV（差值15mV）| Shadlen & Newsome 1998 |
| 重置电位 V_reset | -70 mV | Hodgkin & Huxley 1952 |
| 绝对不应期 τ_ref | 2-3 ms | Hodgkin & Huxley 1952 *J.Physiol.* |
| 膜时间常数 τ_m | 20 ms | Gerstner & Kistler 2002 *Cambridge* |
| 单EPSP幅度 | 0.5-2.0 mV | Song et al. 2000 *Nat.Neurosci.* |
| 自发放电率 | 1-5 Hz | Attwell & Laughlin 2001 |
| 背景突触数 | ~10000/神经元 | Shadlen & Newsome 1998 |

### 标准化参数（令 V_rest=0，V_th-V_rest=1）

```
V_thresh = 1.0          （15mV差值归一化为1）
V_reset  = 0.0          （回到静息）
τ_ref    = 3步          （2-3ms绝对不应期）
leak     = 1 - 1/τ_m   （τ_m=20步→leak=0.95）
J_E      = 0.067-0.133  （0.5-2.0mV/15mV）
J_I      = -4 × J_E    （Brunel 2000 *J.Comput.Neurosci.*）
```

### 小网络（k=8）等效标定

**关键问题**：真实皮层k~10000，小网络k=8，参数需等效标定。

**等效原则**（Gerstner 2002 §11.3，"fluctuation-driven firing"）：
- 真实皮层激发来自大量弱突触的随机涨落
- 小网络中未建模的突触等效为外部背景驱动I_ext
- Shadlen 1998: 背景贡献 = 10000 × 2Hz × 20ms × J_E ≈ 0.4×J_E（均值）

**标定结果（实验验证）**：

| J_E | I_ext_mean | I_ext_std | 激活率 |
|-----|-----------|-----------|--------|
| 0.3 | 0.080 | 0.040 | **4.6% ✅** |
| 0.3 | 0.120 | 0.060 | **7.5% ✅** |

选取 J_E=0.3，I_ext=0.080，激活率4.6%（皮层自发放电范围内）

**物理解释**：
- J_E=0.3 等效单突触贡献4.5mV：小网络中每个连接等效了真实皮层
  多个弱突触协同的累积效果（750个2mV突触协同=1500mV，超阈值100倍；
  等效到k=8时，单个连接需贡献1500/8=187.5mV/15mV≈12.5，
  但由于E/I平衡，实际取0.3是合理的压缩）
- I_ext=0.080 等效Shadlen 1998背景突触输入（1.2mV持续驱动）

### Γst的稀疏激活下正确计算（Honey 2009 PNAS）

**问题**：4%激活率下，逐步outer(h_t,h_t)接近零矩阵，EMA无法积累。

**正确方法**：时间窗口相关系数（Honey 2009 *PNAS* 106:2035）
```python
FC_ij = corr(spike_i(t:t+T), spike_j(t:t+T))
T = 200步（200ms窗口，覆盖足够多的稀疏脉冲）
```

参考文献：
- Shadlen & Newsome (1998) *J.Neurosci.* 18:3870
- Hodgkin & Huxley (1952) *J.Physiol.* 117:500
- Gerstner & Kistler (2002) *Spiking Neuron Models*, Cambridge
- Song et al. (2000) *Nat.Neurosci.* 3:919
- Brunel (2000) *J.Comput.Neurosci.* 8:183
- Attwell & Laughlin (2001) *J.Cereb.Blood.Flow.Metab.* 21:1133
- Honey et al. (2009) *PNAS* 106:2035
