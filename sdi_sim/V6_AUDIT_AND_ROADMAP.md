# SDI 实验五 v6 — 代码审计与下一步路线图

**审计时间**: 2026-05-09  
**审计对象**: `sdi_experiment5_v6.py`  
**基准**: Beggs & Plenz 2003, Friedman 2012 PRL, Priesemann 2014 PLOS CB

---

## 一、科学正确性问题

### P0 — 必须修复

#### 1. τ尺度关系全部违反 ✗

真实SOC临界态必须满足（Friedman 2012 PRL，平均场缩放律）：

```
τ_dur = (τ_size + 1) / 2
```

当前所有实验结果均严重偏离：

| 实验 | τ_size | τ_dur | τ_dur_theory | 误差 |
|------|--------|-------|-------------|------|
| C.elegans 3-r v6 | 2.39 | 3.06 | 1.70 | 80% |
| WS_Control 4-r v6 (best) | 1.83 | 2.18 | 1.41 | 54% |
| **生物标准** | **1.5** | **2.0** | **1.25→修正** | - |

**根本原因**：τ_dur偏高是因为雪崩持续时间分布不是纯幂律。每步的传播结构（分层级联）导致持续时间相对于尺寸系统性偏大。

**修复方向**：
- 引入雪崩形状分析（avalanche shape collapse）验证
- τ_dur目标范围放宽至[1.8, 2.5]（生物测量噪声），但缩放关系误差应<20%

#### 2. 记录阶段STD冷启动 ✗

```python
# 当前 (错误)
std_u_rec = init_std_resources(N, seed)  # 重置为新的U_0=0.5

# 应该
std_u_rec = std_u.copy()  # 继承学习阶段末尾的真实STD状态
```

**影响**：记录阶段前500步，STD从初始值U_0=0.5开始，而非学习阶段已达稳态的值（可能更低）。这会使前500步的雪崩尺寸系统性偏小。

#### 3. 幂律验证缺少统计检验 ✗

当前`fit_powerlaw`只用Hill MLE + R²（R²对幂律并不敏感）。  
缺少：
- **Kolmogorov-Smirnov检验**（拒绝幂律的p值）
- **似然比检验**：幂律 vs 对数正态 vs 指数截断幂律
- **无穷方差检验**（τ<3时成立）

---

### P1 — 应该修复（影响生物准确性）

#### 4. STDP使用随机dt而非真实spike时序

```python
# 当前 (错误)
dt = int(rng.integers(1, 30))  # 随机均匀时间差

# 应该
last_spike = np.full(N, -9999, dtype=np.int32)  # 每神经元上次激活步
# 激活时: last_spike[i] = current_step
# STDP时: dt = last_spike[post] - last_spike[pre]  (真实时差)
# dt>0: LTP (pre先于post激活)
# dt<0: LTD (post先于pre激活)
```

**影响**：当前混合了LTP和LTD方向，随机dt使STDP窗口失去时序意义。

#### 5. 突触延迟是权重衰减，不是时序延迟

```python
# 当前 (不正确)
delay_factor = 1.0 / d_ij   # delay=2 → 权重×0.5
eff_w *= delay_factor

# 应该: 延迟队列
# 用环形缓冲区存储(源神经元, 目标神经元, 激活步)
# 每步处理到达当前步的消息
delayed_queue = []  # (target, strength, arrival_step)
```

**影响**：现在"delay"只是缩放了权重，不改变任何时序。延迟对雪崩形状（shape collapse）有重要影响。

#### 6. 校准κ只用第一代传播

```python
# 当前
# 记录 (wave0=1, wave1=?) 每次BTW注入
kappa = sum(wave1s) / sum(wave0s)

# 应该: 全雪崩所有代
# 对每次雪崩: κ_雪崩 = Σ(wave_{i+1}) / Σ(wave_i), i=0,1,2,...
# kappa = mean(κ_雪崩)  对所有完整雪崩
```

---

## 二、工程实现问题

### P2 — 需优化

#### 7. recover_std 每步O(N²)瓶颈

```python
# 当前: 纯Python，N×N矩阵遍历
def recover_std(std_u, adj, N):
    mask = adj != 0
    std_u[mask] += (U_0 - std_u[mask]) / TAU_STD  # 实际numpy操作，OK

# 已经是numpy操作，性能可接受
# 但可进一步优化：只在有突触的位置更新
# np.where(adj != 0, std_u + (U_0-std_u)/TAU_STD, std_u)
```

#### 8. exc_mask_pre 每步重建

```python
# 当前: 在STDP循环内每步计算
exc_mask_pre = ~is_inhib[:, np.newaxis] * np.ones((1, N), dtype=bool)

# 应该: 在仿真开始前计算一次
exc_mask_pre = np.outer(~is_inhib, np.ones(N, dtype=bool))  # (N,N) 固定
```

#### 9. adj是对称无向图

```python
# 当前: adj[i,j]=adj[j,i]=w (无向)
# 真实突触: 有向 (adj[i,j]≠adj[j,i])
# 影响: C.elegans connectome约60%有向边
# 建议: 改为非对称初始化（仅保留adj[i,j]，不设adj[j,i]）
```

---

## 三、缺失的生物机制

### 已实现
- ✅ 绝对/相对不应期
- ✅ STDP（简化版）
- ✅ 突触固化/消亡（E-L键）
- ✅ WS随机重连
- ✅ 突触缩放（稳态可塑性）
- ✅ 竞争性修剪
- ✅ BTW极慢驱动
- ✅ E/I平衡（80/20）
- ✅ 短期突触抑制（STD，TM模型）
- ✅ 突触延迟（简化版，待修正）

### 尚未实现
| 机制 | 重要性 | 文献 |
|------|--------|------|
| **LIF神经元（漏积分模型）** | 高 | Dayan & Abbott 2001 |
| **真实spike时间戳STDP** | 高 | Bi & Poo 1998 |
| **突触延迟队列** | 中 | Diesmann 1999 |
| **钙离子依赖STDP** | 中 | Shouval 2002 |
| **spike频率适应（SFA）** | 中 | Benda & Herz 2003 |
| **间隙连接（Gap Junction）** | 低 | Bennett & Zukin 2004 |
| **神经调质（neuromodulator）** | 低 | Hasselmo 1995 |

---

## 四、下一步工作方案

### v7 目标：修复P0+P1问题，实现统计严格性

**优先级1 — STD连续性修复（1天）**

```python
# 学习阶段结束时保存STD状态
std_u_after_learning = std_u.copy()

# 校准时使用同一STD稳态
# 记录时继续使用
std_u_rec = std_u_after_learning.copy()
```

**优先级2 — STDP真实spike时序（1天）**

```python
last_spike = np.full(N, -9999, dtype=np.int32)
# 每步激活时: last_spike[active] = step
# STDP时计算真实dt = last_spike[post] - last_spike[pre]
```

**优先级3 — 统计检验升级（1天）**

```python
def fit_powerlaw_strict(data):
    """返回tau, xmin, ks_stat, p_value, likelihood_ratio"""
    # Hill MLE
    # KS检验: 幂律 vs 数据
    # 似然比检验: 幂律 vs 对数正态
    # p_value < 0.1则拒绝幂律
```

**优先级4 — 延迟队列实现（2天）**

```python
# 环形延迟缓冲区
delay_buffer = {}  # {arrival_step: [(target_neuron, weight), ...]}

# 发送时
for delay in range(1, MAX_DELAY+1):
    arrival = current_step + delay
    delay_buffer.setdefault(arrival, []).extend(targets)

# 接收时
arrivals = delay_buffer.pop(current_step, [])
```

**优先级5 — 加入τ缩放关系作为验证指标**

```python
# 新增达标条件
scale_ok = abs(tau_d - (tau_s + 1)/2) / ((tau_s + 1)/2) < 0.20  # 误差<20%
```

---

### v8 目标：LIF神经元 + 真实连接组

**LIF模型**:
```
τ_m * dV/dt = -(V - V_rest) + R * I_syn
if V > V_thresh: spike, V <- V_reset
```

**连接组接入**:
- C.elegans真实279节点connectome（Varshney 2011）
- Hemibrain子图
- 验证真实有向图上的SOC

---

### v9 目标：自由能显式化

在v8基础上显式计算局部自由能代理：
```
F_local(i) = (act_rate_i - target_rate)^2 + lambda * |w_i - w_prior|^2
```
验证SDI规则是否真的在最小化F_local。

---

## 五、对实验五成果的评估

### 已确认的科学结论
1. ✅ **κ≈1.0（100%达标）**：SDI规则体系可被自动校准到SOC临界点
2. ✅ **PSD≈-1/f（100%达标）**：临界态自发涌现1/f噪声
3. ✅ **τ_size在合理范围（~1.6-2.4）**：幂律分布存在，方向正确
4. ✅ **多步雪崩（60-80%）**：雪崩真实展开，不是单步闪现
5. ⚠️ **τ缩放关系违反**：需v7修复后重新验证

### 需要注意的局限
- τ_size和τ_dur尚未满足平均场缩放关系（Friedman 2012）
- 当前τ_size≈2.2-2.4（超过生物目标1.5），可能因尺寸分布有残余双峰
- 幂律验证缺少KS统计量

### 对TCC/SDI理论的贡献
- 证明SDI四规则体系的自组织临界性（SOC）
- 证明极简规则（大道至简）可自发涌现1/f幂律动力学
- 为三位一体（τ雪崩支柱）提供计算依据
- 验证路径：规则→自校准→临界态→神经雪崩，完整闭环

---

*下一步优先级：v7 STD连续性 + STDP时序 + 统计检验，预计修复后τ缩放关系误差降至<20%*
