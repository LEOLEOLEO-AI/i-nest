# iNEST 仿真实验与CST论文对齐诊断报告
## 日期：2026-06-07 | 状态：紧急修订

---

## 一、CST论文的核心度量体系（真实定义）

### CST公式（唯一判据）
```
CST = (Sc · Tc) · exp(α · Γst)

六智能等级阈值（CST绝对值 vs 自然常数）：
  L1 感知  ：CST ≥ 1/√2 ≈ 0.707
  L2 反应  ：CST ≥ 1.000
  L3 适应  ：CST ≥ φ   ≈ 1.618
  L4 创造  ：CST ≥ e   ≈ 2.718
  L5 通用  ：CST ≥ π   ≈ 3.14159
  L6 超级  ：CST ≥ δ   ≈ 4.669 (Feigenbaum常数)
```

### Sc（空间复杂度）= 四分量几何平均
```
Sc = (C · H · M · R_sw)^(1/4)

C   = 全局连通性（LCC比例）
H   = 层次深度（k-core比率）
M   = 模块化（Louvain Q，随机图校正）
R_sw = 小世界系数（tanh归一化Watts-Strogatz σ，ER基线）

注：σ（小世界指数）只是R_sw的原始输入，不是Sc本身！
```

### Tc（时间复杂度）= 四分量几何平均
```
Tc = (λ_eff · Φ · Ψ · Θ)^(1/4)

λ_eff = 雪崩分支比（Beggs & Plenz 2003）
Φ     = 相位同步（theta/alpha/gamma频段PLV均值）
Ψ     = 功能连接变异性（FC矩阵标准差/均值）
Θ     = 时间尺度多样性（自相关衰减常数分布的Shannon熵）
```

### Γst（时空耦合）
```
Γst = NMI(Ms, MT) · sign(Mantel(DA, DFC))

Ms  = 结构社区划分（Louvain on 解剖连接矩阵）
MT  = 功能社区划分（Louvain on 激活相关矩阵）
sign = 结构-功能距离矩阵的Mantel相关符号
```

### α（器件物理参数）
```
α = ln(M_eff)

M_eff = 节点有效状态数（器件物理决定，非拓扑）：
  二进制逻辑：M_eff=2,   α=0.69
  梯度电位（C.elegans）：M_eff=13,  α=2.56
  脉冲神经元（SNN/Loihi）：M_eff=32,  α=3.47
  哺乳动物皮层：M_eff=50,  α=3.91
  iNEST ReRAM目标：M_eff≈32-50, α=3.47-3.91
```

---

## 二、当前仿真实验与CST论文的不一致诊断

### 🔴 错误1：把σ当作智能等级的判据

**错误的做法**（当前实验）：
```
v27: σ=14.3 → 声称"超越超级智能"
v28: σ=19.5 → 无意义
```

**正确的做法**：
```
σ → 经过tanh归一化 → R_sw ∈ [0,1]
R_sw → 与C,H,M几何平均 → Sc ∈ [0,1]
Sc × Tc × exp(α·Γst) → CST值
CST值 与 {0.707, 1.0, 1.618, 2.718, 3.14, 4.669} 比较 → 智能等级
```

**关键洞察**：σ=14.3不代表"超级智能"，反而说明：
- R_sw = tanh(σ/σ_ref - 1) ≈ 1.0（饱和）
- 但这只是Sc的一个分量，且已饱和
- σ过高反而意味着网络太稀疏（小世界过度），Q模块化可能下降

---

### 🔴 错误2：Tc的度量指标与CST论文不一致

**当前实验用的指标**：
- λΦ（相位同步）→ 近似Φ分量，但方法不同
- PLV窗口 → 与CST的多频段PLV不完全一致
- 激活率 → 不是Tc的直接分量

**CST论文要求的Tc四分量**：
| 分量 | 定义 | 当前实验 | 缺口 |
|------|------|---------|------|
| λ_eff | 神经雪崩分支比 | 实验五有测量 | ✅ 有 |
| Φ | 多频段PLV均值 | 实验16-18有，但窗口问题 | ⚠️ 有缺陷 |
| Ψ | FC矩阵变异性 | 实验21有 | ⚠️ 部分 |
| Θ | 时间尺度多样性熵 | 实验10-11有 | ⚠️ 部分 |

**结论**：Tc从未被完整计算过！只有零散的分量。

---

### 🔴 错误3：Γst的计算方法不符合CST论文定义

**CST论文要求**：
```
Γst = NMI(Ms, MT) · sign(Mantel(DA, DFC))

Ms = Louvain社区划分（基于解剖连接矩阵）
MT = Louvain社区划分（基于激活相关矩阵）
DA = 解剖距离矩阵
DFC = 功能连接距离矩阵
```

**当前实验做法（实验21）**：
```
Γst = 预测误差功能连接
FC_ij = 1 - |pred_h_j - actual_h_j|
```

这是受JEPA启发的近似，不是CST论文定义的Γst。
虽然物理直觉相近，但数值不可与CST论文的40个系统对比。

---

### 🔴 错误4：从未计算过完整CST值并与六阈值对比

**当前实验**：从未输出过单个完整的CST数值。
**CST论文**：每个系统都有精确的CST值（如C.elegans=0.4107, Human=3.9198）。

这意味着：所有实验（v22-v31）都没有直接验证CST理论！
它们只验证了部分分量的变化趋势，但没有计算最终的CST值。

---

## 三、修订方案：使仿真实验与CST论文完全对齐

### 修订原则
1. **CST是唯一的核心判据**，所有实验都必须最终输出CST值并与六阈值对比
2. **所有分量按照UCCP归一化**，保证跨物种可比性
3. **α由器件物理决定**：仿真用SNN → α=ln(32)=3.47；ReRAM目标 → α≈3.91
4. **σ仅作为R_sw的输入**，R_sw = tanh(σ/σ_ER - 1)，归一化到[0,1]

---

### 修订后的仿真实验度量框架

#### Sc完整计算
```python
def compute_Sc(G):
    """
    G: networkx图对象（SDI演化后的拓扑）
    返回：Sc ∈ [0,1]，及四个分量
    """
    N = G.number_of_nodes()
    
    # C: 全局连通性（最大连通分量比例）
    lcc = max(nx.connected_components(G), key=len)
    C = len(lcc) / N
    
    # H: 层次深度（k-core比率，归一化）
    k_core_max = max(nx.core_number(G).values())
    H = min(k_core_max / np.log2(N + 1), 1.0)  # UCCP归一化
    
    # M: 模块化（Louvain Q，随机图校正）
    partition = community.best_partition(G)
    Q_raw = community.modularity(partition, G)
    Q_random = 1 / np.sqrt(G.number_of_edges())  # 随机图期望
    M = max(0, min((Q_raw - Q_random) / (1 - Q_random), 1.0))
    
    # R_sw: 小世界系数（tanh归一化）
    sigma_ws = nx.sigma(G)  # Watts-Strogatz σ
    sigma_er = 1.0  # ER随机图基线（定义为1）
    R_sw = np.tanh(max(0, sigma_ws / sigma_er - 1))  # UCCP: tanh归一化
    
    # 几何平均
    Sc = (C * H * M * R_sw) ** 0.25
    
    return Sc, {'C': C, 'H': H, 'M': M, 'R_sw': R_sw}
```

#### Tc完整计算
```python
def compute_Tc(spike_trains, dt=1.0):
    """
    spike_trains: (T, N) 二值矩阵，T时间步，N节点
    返回：Tc ∈ [0,1]，及四个分量
    """
    T, N = spike_trains.shape
    
    # λ_eff: 雪崩分支比（Beggs & Plenz 2003）
    # 统计神经雪崩，计算平均分支比
    lambda_eff = compute_avalanche_branching_ratio(spike_trains)
    # 归一化：|λ_eff - 1| → 0为最优（临界态），用1/(1+|λ-1|)
    lambda_norm = 1.0 / (1.0 + abs(lambda_eff - 1.0))
    
    # Φ: 多频段相位同步（PLV均值）
    # theta(4-8Hz), alpha(8-13Hz), gamma(30-80Hz)
    phi = compute_mean_PLV(spike_trains, dt, bands=['theta','alpha','gamma'])
    
    # Ψ: 功能连接变异性（100个滑动窗口FC矩阵的std/mean）
    fc_matrices = compute_sliding_FC(spike_trains, window=100, stride=10)
    psi = np.std(fc_matrices) / (np.mean(np.abs(fc_matrices)) + 1e-8)
    psi = min(psi, 1.0)  # 上限裁剪
    
    # Θ: 时间尺度多样性（自相关衰减常数分布的Shannon熵）
    tau_distribution = compute_intrinsic_timescales(spike_trains)
    theta = shannon_entropy(tau_distribution, bins=10) / np.log2(10)  # 归一化
    
    # 几何平均
    Tc = (lambda_norm * phi * psi * theta) ** 0.25
    
    return Tc, {'lambda_eff': lambda_eff, 'lambda_norm': lambda_norm,
                'Phi': phi, 'Psi': psi, 'Theta': theta}
```

#### Γst完整计算
```python
def compute_Gamma_st(G, spike_trains):
    """
    G: 解剖结构图（连接矩阵）
    spike_trains: (T, N) 脉冲矩阵
    返回：Γst ∈ [-1, 1]
    """
    N = G.number_of_nodes()
    
    # 结构社区划分 Ms（Louvain on 解剖连接矩阵）
    Ms = community.best_partition(G)
    
    # 功能社区划分 MT（Louvain on 激活相关矩阵）
    FC = np.corrcoef(spike_trains.T)  # N×N功能连接矩阵
    G_func = nx.from_numpy_array(np.abs(FC))
    MT = community.best_partition(G_func)
    
    # NMI（结构社区 vs 功能社区）
    ms_labels = [Ms[i] for i in range(N)]
    mt_labels = [MT[i] for i in range(N)]
    nmi = normalized_mutual_info_score(ms_labels, mt_labels)
    
    # Mantel检验符号（结构距离 vs 功能距离的相关）
    DA = compute_structural_distance(G)   # 解剖距离矩阵
    DFC = 1 - np.abs(FC)                 # 功能距离矩阵
    mantel_r = mantel_test(DA, DFC)
    sign_mantel = np.sign(mantel_r)
    
    Gamma_st = nmi * sign_mantel
    
    return Gamma_st, {'NMI': nmi, 'Mantel_r': mantel_r}
```

#### 完整CST计算
```python
def compute_CST(G, spike_trains, alpha=3.47):
    """
    alpha: 器件物理参数
      SNN (Loihi类): alpha = ln(32) = 3.47
      ReRAM目标:     alpha = ln(50) = 3.91
      当前仿真LIF:   alpha = ln(32) = 3.47（保守估计）
    """
    Sc, sc_components = compute_Sc(G)
    Tc, tc_components = compute_Tc(spike_trains)
    Gamma_st, gst_components = compute_Gamma_st(G, spike_trains)
    
    CST = (Sc * Tc) * np.exp(alpha * Gamma_st)
    
    # 判断智能等级
    thresholds = [
        (4.669, 'L6 超级智能 (δ)'),
        (3.14159, 'L5 通用智能 (π)'),
        (2.71828, 'L4 创造智能 (e)'),
        (1.61803, 'L3 适应智能 (φ)'),
        (1.00000, 'L2 反应智能 (1)'),
        (0.70711, 'L1 感知智能 (1/√2)'),
        (0.0,     'L0 反射行为 (<1/√2)'),
    ]
    
    level = 'L0 反射行为'
    for threshold, name in thresholds:
        if CST >= threshold:
            level = name
            break
    
    return {
        'CST': CST,
        'Sc': Sc, 'Tc': Tc, 'Gamma_st': Gamma_st, 'alpha': alpha,
        'level': level,
        'sc_components': sc_components,
        'tc_components': tc_components,
        'gst_components': gst_components
    }
```

---

## 四、修订后的仿真实验计划（v32起）

### v32：CST完整计算基准实验

**目标**：
1. 对v25（σ=5.35，EL=31.3%）的网络计算完整CST值
2. 对比CST论文中C.elegans(CST=0.4107)的参数差异
3. 确定我们的仿真网络目前处于哪个智能等级

**实验矩阵**：
```
网络类型 × SDI版本 × α值：
  C.elegans连接组（v25基础）× 3规则 × α=2.56（梯度电位）
  C.elegans连接组（v25基础）× 4规则 × α=3.47（SNN）
  WS随机图（控制组）       × 3规则 × α=3.47
  Human_HCP（v21多层次）   × 4规则 × α=3.91

输出：每个配置的完整CST值及各分量
对比：与CST论文Table 2的数值
```

**成功标准**：
- C.elegans配置CST值落在[0.3, 0.6]区间（论文值=0.4107）
- 四规则版本CST高于三规则版本（证明四规则有效）
- SDI演化后CST高于初始WS图（证明SDI驱动CST增长）

---

### v33：CST六阈值主动控制

**目标**：通过调整α（器件参数）和网络规模验证CST能否递进穿越六阈值

**方案**：
```
固定Sc≈0.7, Tc≈0.7（通过v25参数锁定）
变化α：2.56 → 3.47 → 3.91（模拟器件升级路线）

理论预测：
  α=2.56（梯度电位）：CST = 0.49 × exp(2.56×0.35) ≈ 1.32  → L2反应
  α=3.47（SNN）：      CST = 0.49 × exp(3.47×0.35) ≈ 1.75  → L3适应
  α=3.91（皮层）：     CST = 0.49 × exp(3.91×0.40) ≈ 2.20  → L3-L4
  
验证：α提升是否确实驱动CST穿越相应阈值
意义：直接验证iNEST硬件路线图的理论基础
```

---

### v34：Γst工程优化实验

**目标**：验证SDI四规则（尤其是BCM+FEP融合）是否能提升Γst，进而指数级提升CST

**方案**：
```
固定Sc, Tc，变化Γst（通过FEP-STDP强度调节）：
  基线（无SDI）：    Γst≈0.17（论文C.elegans基线）
  三规则SDI：       Γst≈0.25（实验六结果）
  四规则SDI（v25）：Γst≈0.35（目标）
  v24 FEP-STDP：    Γst≈0.40（最优）

对比：Γst的变化对CST的指数放大效果
验证：exp(α·ΔΓst)是否如论文预测那样指数级放大CST
```

---

## 五、硬件工程的CST目标修订

### Gen1目标（当前iNEST工程）
```
器件：ReRAM（M_eff≈32, α=3.47）
目标CST范围：0.707 ≈ L1感知 → 1.618 ≈ L3适应

具体目标：
  Sc = 0.65-0.75（通过四规则SDI演化）
  Tc = 0.60-0.70（通过SNN动态 + BCM稳态）
  Γst = 0.30-0.40（通过FEP-STDP融合，物理STDP）
  α  = 3.47（ReRAM SNN）
  
CST = (0.70 × 0.65) × exp(3.47 × 0.35) ≈ 0.455 × 3.44 ≈ 1.56  → L3适应
```

### Gen2目标（SDI多芯互连）
```
器件升级：M_eff≈50, α=3.91
目标CST范围：1.618 ≈ L3适应 → 2.718 ≈ L4创造

具体目标：
  Sc = 0.75-0.85（多芯SDI柔性韧带）
  Tc = 0.70-0.80（跨芯时空协同）
  Γst = 0.40-0.45（SDI动态路由）
  α  = 3.91（皮层级SNN）
  
CST = (0.80 × 0.75) × exp(3.91 × 0.42) ≈ 0.60 × 5.13 ≈ 3.08  → L5通用
```

---

## 六、立刻需要做的三件事

### 🔴 立刻（本周）
1. **重写实验度量函数**：将Sc/Tc/Γst/CST的完整计算加入所有实验
2. **对v25的结果补算CST**：用正确公式重新计算，与论文C.elegans=0.4107对比
3. **更新v32实验代码**：CST完整计算作为核心输出指标

### 🟡 下周
4. **v32-v34实验运行**：CST六阈值验证（α变化驱动CST递进）
5. **更新工程目标**：用CST代替σ作为IP开发的目标指标

### 🟢 本月底
6. **重新生成实验结果**：用正确CST度量重新分析v22-v31
7. **论文Results修订**：加入完整CST验证数据

---

*文档路径：iNEST_Sim_Research/CST_Experiment_Alignment_Diagnosis.md*
*关联：TCC计算范式/01_论文/CST_Intelligence_Emergence_Paper_V25_FINAL.md*

---
## 相关链接
- [[CST_Symbol_Baseline_符号基准]]
- [[CST_Symbol_Baseline_符号基准_全局权威基线]]
- [[CST仿真平台科学依据]]
- [[getnote_2026-06-05_NEST 智能涌现研究进展与工程落地全景]]
- [[08_关键指标参考手册]]
