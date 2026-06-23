# 重整化群理论在生物神经网络中的验证

## 核心问题

1. **尺度不变性验证**：生物神经网络在不同粒度（功能柱 → 脑区 → 全脑）上的 SCTC 和伽马 St 是否一致？
2. **参数获取路线**：如何从公开连接组学数据库获得计算所需的完整参数集？

---

## 第一部分：理论基础与文献出处

### 关键假设
生物神经网络具有**自相似性**（self-similarity）
- 一个脑区的局部特性 ≈ 整个脑区的特性
- 脑区的特性 ≈ 全脑的特性
- 这是**重整化群（RG）理论**的核心：在临界态附近，系统在不同尺度上表现出相同的行为

### 核心文献

#### 1️⃣ 尺度不变性的实验证据
- **Watts & Strogatz (1998)** - "Collective dynamics of small-world networks"
  - Nature 393: 440-442
  - C. elegans 神经网络呈现小世界拓扑
  - 度分布：P(k) ~ k^(-2.5)（接近功率律）
  - 暗示尺度不变性

#### 2️⃣ 数据来源
- **Hemibrain 果蝇脑连接组**
  - https://www.janelia.org/project-team/flyem/hemibrain
  - 21,000+ 神经元，20M 突触
  - 可从单个功能模块 → 脑区 → 全脑进行递进分析

#### 3️⃣ 功能柱的理论基础
- **Douglas & Martin (2004)** - "Canonical Microcircuits for Biological Vision"
  - Nature Neuroscience
  - 皮层按"柱"（column）组织，直径 ~500 微米
  - 同一柱内连接密度 >> 柱间连接
  - 柱本身构成自相似的功能单元

#### 4️⃣ 重整化群理论的应用
- **Newman et al. (2002-2006)**
  - 复杂网络可被"粗粒化"而不改变拓扑特性
  - 功率律指数在多尺度上保持不变
  - C. elegans 神经网络满足重整化群不变性

#### 5️⃣ 多物种比较
| 物种 | 神经元数 | 突触数 | 小世界特性 | 功率律指数 |
|-----|--------|-------|---------|----------|
| C. elegans | 302 | 7,600 | ✓ | ~2.5 |
| 果蝇幼虫 | ~3,000 | ~20K | ✓ | ~2-3 |
| 果蝇成虫 | ~100,000 | ~20M | ✓ | ~2-3 |
| 小鼠新皮层 | ~500K | ~10M | ✓ | ~2-3 |

---

## 第二部分：参数获取路线图

### 推荐优先级（完整性 + 可行性）

#### Tier 1：完整连接组数据（最优）

**C. elegans**
- 数据库：WormAtlas + OpenWorm
- 规模：302 神经元，7,600 化学突触，1,600 电突触
- 覆盖率：100%
- 获取：https://github.com/openworm，http://neurodata.io/

**果蝇幼虫（Larva）**
- 数据库：L1 connectome
- 规模：3,016 神经元，~400K 突触
- 覆盖率：100%
- 获取：https://l1connectome.github.io

**果蝇成虫（Hemibrain）**
- 数据库：FlyEM Hemibrain
- 规模：21,747 神经元（右半脑），~20M 突触
- 覆盖率：>90%
- 获取：https://neuprint.janelia.org（需注册）

#### Tier 2：部分连接组 + 功能数据
- **Allen Brain Atlas**（小鼠）：脑区级连接 + 功能数据
- **CoCoMac**（猴脑）：387 个脑区级连接

---

## 第三部分：SCTC 与 γSt 的参数集

### 计算 SCTC（结构临界态转变复杂度）

**所需参数**：
1. 拓扑参数：度分布 P(k)，聚类系数 C_i，平均路径长度 L
2. 连通性：邻接矩阵 A[i,j]，权重矩阵 w[i,j]
3. 临界态：雪崩大小分布 P(s) ~ s^(-α)
4. 活动动力学：膜电位、突触衰减时常 τ_s、放电阈值 θ

**计算代码框架**：
```python
import networkx as nx
import numpy as np
from scipy.stats import linregress

# 1. 加载连接矩阵
A = load_connectome()  # n × n 邻接矩阵

# 2. 计算拓扑指标
G = nx.DiGraph(A)
degree_seq = [d for n, d in G.degree()]
clustering = nx.average_clustering(G)
path_length = nx.average_shortest_path_length(G.to_undirected())

# 3. 度分布的功率律指标
k = np.array(degree_seq)
alpha_topo = fit_power_law(k)

# 4. 临界态指标（雪崩模拟）
avalanche_sizes = simulate_avalanches(A, n_steps=10000)
alpha_avalanche = fit_power_law(avalanche_sizes)

# 5. SCTC 综合指数
SCTC = compute_criticality_index(alpha_topo, alpha_avalanche, clustering)
```

### 计算 γSt（时间复杂度）

**所需参数**：
1. 时间尺度：突触衰减 τ_s（100-1000 ms），膜时常 τ_m（10-100 ms）
2. 活动序列：放电时间戳 t_spike[i]
3. 功率谱：S(f) ~ f^(-β)，1/f 噪声指数

**计算代码框架**：
```python
def temporal_complexity(spike_times, dt=1):
    """计算伽马 St（时间复杂度）"""
    # 转为二进制时间序列
    T_max = spike_times.max()
    n_bins = int(T_max / dt)
    s = np.zeros(n_bins)
    for t in spike_times:
        s[int(t/dt)] = 1
    
    # 计算功率谱
    from scipy.fft import fft
    S = np.abs(fft(s))**2
    freq = np.fft.fftfreq(len(s), dt)
    
    # 拟合功率律：S(f) ~ f^(-γ)
    logf = np.log(freq[1:len(freq)//2])
    logS = np.log(S[1:len(S)//2])
    slope, _, _, _, _ = linregress(logf, logS)
    gamma_St = -slope / 2  # 功率谱指数转时间复杂度
    
    return gamma_St

# 估计全网络平均
gamma_St_values = []
for neuron_idx in range(n_neurons):
    spikes_i = spike_times[neuron_id == neuron_idx]
    gamma_i = temporal_complexity(spikes_i)
    gamma_St_values.append(gamma_i)

gamma_St_mean = np.mean(gamma_St_values)
```

---

## 第四部分：多尺度重整化验证方案

### 验证框架：脑区 SCTC ≈ 全脑 SCTC

**尺度分解**（从微观到宏观）：
- Level 1：微观（0-50 微米）- 单突触
- Level 2：局部（50-500 微米）- 功能柱
- Level 3：中观（0.5-2 mm）- 脑区亚区
- Level 4：宏观（2-50 mm）- 脑区
- Level 5：全脑（50+ mm）- 整个脑

**实验设计**：
```python
def renormalization_analysis(connectome, neuron_annotations):
    """在不同粒度上计算 SCTC，验证尺度不变性"""
    results = {}
    
    # Level 1: 全脑
    SCTC_whole = compute_SCTC(connectome)
    results['whole_brain'] = SCTC_whole
    
    # Level 2: 脑区
    brain_regions = get_brain_regions(neuron_annotations)
    SCTC_regions = {}
    for region_name, neuron_ids in brain_regions.items():
        subgraph = connectome[np.ix_(neuron_ids, neuron_ids)]
        SCTC_regions[region_name] = compute_SCTC(subgraph)
    results['by_region'] = SCTC_regions
    
    # Level 3: 功能柱
    columns = detect_functional_columns(connectome, neuron_annotations)
    SCTC_columns = {}
    for col_id, neuron_ids in columns.items():
        if len(neuron_ids) > 10:
            subgraph = connectome[np.ix_(neuron_ids, neuron_ids)]
            SCTC_columns[col_id] = compute_SCTC(subgraph)
    results['by_column'] = SCTC_columns
    
    # 统计验证
    from scipy.stats import ttest_1samp
    t_stat, p_val = ttest_1samp(
        list(SCTC_regions.values()), 
        SCTC_whole
    )
    
    analysis = {
        'whole_brain': SCTC_whole,
        'region_mean': np.mean(list(SCTC_regions.values())),
        'region_std': np.std(list(SCTC_regions.values())),
        'scale_invariance_pval': p_val,
        'scale_invariant': p_val > 0.05  # 尺度不变性成立
    }
    
    return analysis, results
```

**预期结果**：
- H0: 脑区的 SCTC ≠ 全脑的 SCTC（拒绝尺度不变性）
- H1: 脑区的 SCTC = 全脑的 SCTC（支持尺度不变性）
- **如果 p-value > 0.05**，则支持尺度不变性假设

---

## 第五部分：实际执行方案

### 快速验证（C. elegans，1-2 天）

```bash
# 1. 获取数据
git clone https://github.com/openworm/OpenWorm.git
cd OpenWorm/data

# 2. 运行分析
python3 << 'SCRIPT'
import numpy as np
from scipy.io import loadmat

# 加载连接矩阵
data = loadmat('c_elegans.adj')
connectome = data['connectome']  # 302 × 302

# 基本统计
n_neurons = connectome.shape[0]
n_synapses = np.sum(connectome)
print(f"C. elegans: {n_neurons} neurons, {n_synapses} synapses")

# 进行多尺度分析...
SCRIPT
```

### 中等验证（果蝇幼虫，3-5 天）

```python
from neuprint import Client
import pandas as pd
import numpy as np

# 连接到 L1 幼虫数据库
c = Client('https://l1em.catmaid.virtualflybrain.org:7680',
           dataset='larva')

# 获取神经元和突触
neurons = c.fetch_neurons(type='.*')
synapses = c.fetch_synapses()

# 构建邻接矩阵
n = len(neurons)
adjacency = np.zeros((n, n))

for _, synapse in synapses.iterrows():
    pre_id = synapse['pre_id']
    post_id = synapse['post_id']
    weight = synapse['weight']
    # ... 映射并累加
    
# 进行多尺度分析
```

### 完整验证（Hemibrain，1-2 周）

```python
from neuprint import Client
import neuprint.queries as queries

# 连接 Hemibrain 数据库（需 token）
c = Client('https://neuprint.janelia.org:7473',
           dataset='hemibrain:v1.2.1',
           token='YOUR_TOKEN')

# 获取脑区列表并分别分析
brain_regions = {
    'MB': ['DAN', 'MB410B', ...],      # 蕈菇体
    'AL': ['AL-adPN', 'AL-lPN', ...],  # 触角叶
    'LH': ['LH', 'LHClaw', ...],       # 侧角
}

for region_name, neuron_types in brain_regions.items():
    region_neurons = queries.find_neurons(
        'type==({})'.format('|'.join(neuron_types))
    )
    # 计算该脑区的 SCTC 和 γSt
```

---

## 后续工作步骤

1. **立即**（本周）
   - [ ] 获取 C. elegans 完整连接矩阵
   - [ ] 实现 SCTC 计算模块
   - [ ] 验证基本尺度不变性假设

2. **短期**（1-2 周）
   - [ ] 获取果蝇幼虫（L1）完整连接组
   - [ ] 实现多尺度分解算法
   - [ ] 统计验证尺度不变性（t-test）

3. **中期**（2-4 周）
   - [ ] 获取 Hemibrain 果蝇成虫数据
   - [ ] 对比不同物种的 SCTC 分布
   - [ ] 发表第一阶段结果

4. **长期**
   - [ ] 扩展到小鼠新皮层（Allen Brain Atlas）
   - [ ] 建立统一的"临界态指纹"模型
   - [ ] 预测灵长类脑的 SCTC 分布
