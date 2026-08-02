---
provenance: external
---

# iNEST 仿真实验下一阶段计划
## 基于 2026-06-23 诊断的 8 周改进路线图

**文档日期**：2026-07-02
**版本**：v1.0-EXECUTABLE
**适用范围**：V25 论文改进 → V26/V27 完整验证

---

## 执行摘要

根据 2026-06-23 的系统诊断，当前 iNEST 仿真实验存在 5 个关键缺陷：
1. 数据真实性（0% → 需要 100%）
2. 公式实现（0% → 需要 100%）
3. 对照实验（0 个 → 需要 3 种）
4. 时间动力学（0% → 需要完整 LIF+STDP）
5. 统计检验（0% → 需要 p-value + CI）

**目标**：通过 8 周的系统改进，从 1.5/5 (30%) 提升到 4.5/5 (90%)

**预期成果**：
- ✅ v26：完整的真实数据驱动的拓扑验证
- ✅ v27：包含时间动力学的神经放电仿真
- ✅ v28：硬件实现对标和能效验证

---

## 第一部分：8 周分阶段计划

### 📅 **第 1 周（2026-07-02 至 2026-07-08）：数据修复与准备**

**主题**：加载真实连接组数据，建立基础框架

#### 1.1 任务清单

```
优先级 P0：
☐ 确认 Hemibrain 数据源和版本
  - 当前有 v3（30 MB）✓
  - 验证 25,000 neurons 完整性
  - 确认突触数量 (20M+)
  
☐ 创建 data_loader.py
  - 加载 hemibrain_real_connectome_v3.json
  - 验证数据格式
  - 输出：neurons 列表，synapses 列表
  
☐ 创建 C.elegans 数据加载器
  - 加载 connectome_v8_data.json
  - 验证 302 neurons，7,600 synapses
  
☐ 创建对照数据生成器
  - ER 随机图（保持边密度）
  - 配置模型（保持度分布）
  - 幂律网络（Power-law）
```

#### 1.2 代码框架

```python
# data_loader.py

import json
import networkx as nx
import numpy as np

class ConnectomeLoader:
    """真实连接组加载器"""
    
    def __init__(self, data_path):
        self.data_path = data_path
        self.connectome = None
        self.n_neurons = 0
        self.n_synapses = 0
    
    def load_hemibrain(self):
        """加载 Hemibrain 数据"""
        with open(self.data_path, 'r') as f:
            data = json.load(f)
        
        self.connectome = data
        self.n_neurons = len(data['neurons'])
        self.n_synapses = len(data['synapses'])
        
        print(f"✓ Hemibrain 加载成功")
        print(f"  Neurons: {self.n_neurons}")
        print(f"  Synapses: {self.n_synapses}")
        
        return self.connectome
    
    def build_graph(self):
        """构建 NetworkX 图"""
        G = nx.DiGraph()
        
        # 添加节点
        for neuron in self.connectome['neurons']:
            G.add_node(neuron['id'], type=neuron.get('type'))
        
        # 添加边
        for synapse in self.connectome['synapses']:
            pre = synapse['pre_neuron']
            post = synapse['post_neuron']
            weight = synapse.get('weight', 1.0)
            G.add_edge(pre, post, weight=weight)
        
        return G
    
    def validate(self):
        """验证数据完整性"""
        assert self.n_neurons > 0, "无神经元"
        assert self.n_synapses > 0, "无突触"
        print(f"✓ 数据验证通过")

# 使用示例
loader = ConnectomeLoader('hemibrain_real_connectome_v3.json')
connectome = loader.load_hemibrain()
G = loader.build_graph()
loader.validate()
```

#### 1.3 交付物

```
Week1_Deliverables/
├─ data_loader.py (真实数据加载)
├─ null_model_generator.py (对照数据)
├─ data_validation_report.md (验证报告)
└─ test_data_loading.py (单元测试)
```

**人力**：1 人
**风险**：低
**预期完成**：2026-07-08 23:59 EDT

---

### 📊 **第 2-3 周（2026-07-09 至 2026-07-22）：公式实现**

**主题**：实现标准的网络拓扑指标计算

#### 2.1 7 个核心指标

```
1. σ (小世界系数)
   公式：σ = (C_real / C_rand) / (L_real / L_rand)
   
2. α (幂律指数)
   方法：powerlaw 库拟合度分布
   
3. γ (聚类系数)
   公式：nx.average_clustering()
   
4. C (一致性 / 模块性)
   方法：图分割算法
   
5. L (平均路径长度)
   方法：Floyd-Warshall 或 BFS
   
6. E_L (全局效率)
   公式：平均倒数最短路径
   
7. η (能效指标)
   公式：功耗 / 性能
```

#### 2.2 代码实现

```python
# metrics_calculator.py

import networkx as nx
from scipy import stats
import powerlaw
import numpy as np

class MetricsCalculator:
    """网络拓扑指标计算器"""
    
    def __init__(self, G):
        self.G = G
        self.metrics = {}
    
    def compute_sigma(self):
        """小世界系数"""
        # 真实网络
        C_real = nx.average_clustering(self.G)
        L_real = nx.average_shortest_path_length(self.G)
        
        # 随机网络（ER 图）
        p = nx.density(self.G)
        G_random = nx.erdos_renyi_graph(len(self.G), p)
        C_rand = nx.average_clustering(G_random)
        L_rand = nx.average_shortest_path_length(G_random)
        
        sigma = (C_real / C_rand) / (L_real / L_rand)
        self.metrics['sigma'] = sigma
        return sigma
    
    def compute_alpha(self):
        """幂律指数"""
        degree_seq = [d for n, d in self.G.degree()]
        
        # 使用 powerlaw 库拟合
        fit = powerlaw.Fit(degree_seq, discrete=True)
        alpha = fit.alpha
        
        self.metrics['alpha'] = alpha
        return alpha
    
    def compute_gamma(self):
        """聚类系数"""
        gamma = nx.average_clustering(self.G)
        self.metrics['gamma'] = gamma
        return gamma
    
    def compute_modularity(self):
        """模块性"""
        from networkx.algorithms import community
        
        # 使用贪心模块性最优化
        communities = community.greedy_modularity_communities(self.G.to_undirected())
        modularity = community.modularity(self.G.to_undirected(), communities)
        
        self.metrics['modularity'] = modularity
        return modularity
    
    def compute_all(self):
        """计算所有指标"""
        print("计算网络指标...")
        self.compute_sigma()
        self.compute_alpha()
        self.compute_gamma()
        self.compute_modularity()
        # ... 其他指标
        
        return self.metrics
    
    def compare_with_literature(self):
        """与文献对标"""
        results = {
            'C.elegans': {
                'sigma': (1.5, 2.0),  # 文献值范围
                'alpha': (1.4, 1.8),
                'gamma': (0.3, 0.4)
            },
            'Hemibrain': {
                'sigma': (2.0, 3.0),
                'alpha': (1.5, 2.0),
                'gamma': (0.15, 0.25)
            }
        }
        return results
```

#### 2.3 验证方法

```
对每个指标：
1. 与文献对比（确保在合理范围内）
2. 对不同网络类型验证（Scale-free vs Small-world）
3. 稳定性测试（移除 10% 节点后是否稳定）
```

#### 2.4 交付物

```
Week2-3_Deliverables/
├─ metrics_calculator.py (完整实现)
├─ literature_validation.md (文献对标)
├─ metrics_results.csv (计算结果)
└─ test_metrics_accuracy.py (单元测试)
```

**人力**：1 人 + 统计学家（兼职）
**风险**：低
**预期完成**：2026-07-22 23:59 EDT

---

### 🔬 **第 3-4 周（2026-07-16 至 2026-07-29）：对照实验**

**主题**：生成对照网络并进行统计比较

#### 3.1 三种对照网络

```python
# null_model_experiments.py

import networkx as nx
import numpy as np
from scipy.spatial.distance import wasserstein_distance

class NullModelComparison:
    """对照模型生成与比较"""
    
    def __init__(self, G_real):
        self.G_real = G_real
        self.results = {}
    
    def generate_ER_random(self):
        """ER 随机图"""
        n = len(self.G_real)
        p = nx.density(self.G_real)
        G_ER = nx.erdos_renyi_graph(n, p)
        return G_ER
    
    def generate_configuration_model(self):
        """配置模型"""
        degree_seq = [d for n, d in self.G_real.degree()]
        G_config = nx.configuration_model(degree_seq)
        return G_config
    
    def generate_scale_free(self):
        """幂律网络"""
        n = len(self.G_real)
        G_sf = nx.scale_free_graph(n)
        return G_sf
    
    def statistical_comparison(self):
        """统计显著性检验"""
        
        # 生成对照
        G_ER = self.generate_ER_random()
        G_config = self.generate_configuration_model()
        G_sf = self.generate_scale_free()
        
        # 计算指标
        metrics_real = self._compute_metrics(self.G_real)
        metrics_ER = self._compute_metrics(G_ER)
        metrics_config = self._compute_metrics(G_config)
        metrics_sf = self._compute_metrics(G_sf)
        
        # 统计检验
        results = {}
        for metric in metrics_real.keys():
            # t-test
            p_value_ER = self._ttest(metrics_real[metric], metrics_ER[metric])
            p_value_config = self._ttest(metrics_real[metric], metrics_config[metric])
            
            results[metric] = {
                'real': metrics_real[metric],
                'ER': metrics_ER[metric],
                'p_value_ER': p_value_ER,
                'config': metrics_config[metric],
                'p_value_config': p_value_config,
                'significant': p_value_ER < 0.05 and p_value_config < 0.05
            }
        
        return results
```

#### 3.2 统计方法

```
对每个指标：
1. Bootstrap 置信区间（10,000 次重采样）
2. Mann-Whitney U 检验（非参数）
3. 效应量（Cohen's d）
4. Bonferroni 多重检验校正（7 个指标）
```

#### 3.3 交付物

```
Week3-4_Deliverables/
├─ null_model_comparison.py (完整比较)
├─ statistical_results.csv (p-values)
├─ null_model_networks/ (3 种对照网络)
│  ├─ ER_random.json
│  ├─ configuration_model.json
│  └─ scale_free.json
└─ comparison_report.md (详细报告)
```

**人力**：1 人
**风险**：低
**预期完成**：2026-07-29 23:59 EDT

---

### 🧠 **第 4-6 周（2026-07-23 至 2026-08-12）：时间动力学仿真**

**主题**：实现 LIF 神经元 + STDP 学习，验证 SOC

#### 4.1 架构概览

```
神经元动力学仿真：

输入：真实连接组 (25,000 neurons, 20M synapses)
  ↓
LIF 神经元模型：
  dV/dt = (I_ext + I_syn - V) / τ_m
  V_reset = -70 mV, V_threshold = -50 mV
  ↓
突触模型：
  dI_syn/dt = -I_syn / τ_syn
  I_syn = Σ w_ij * δ(t - t_spike)
  ↓
STDP 学习规则：
  dw/dt = (pre_spike * post_spike - w) / τ_stdp
  ↓
放电输出：spike trains
  ↓
分析：
  - 放电雪崩分布 P(s)
  - 功率谱 P(f)
  - 临界指数 α, β
  ↓
验证 SOC：P(s) ∝ s^(-α), P(f) ∝ f^(-β)
```

#### 4.2 实现方案（使用 Brian2）

```python
# neural_dynamics_simulator.py

import brian2 as b2
import numpy as np
from collections import defaultdict

class NeuralDynamicsSimulator:
    """LIF + STDP 神经仿真器"""
    
    def __init__(self, connectome, duration_ms=3000):
        self.connectome = connectome
        self.duration = duration_ms * b2.ms
        
        # 神经元数量
        self.n_neurons = len(connectome['neurons'])
        
        # 数据收集
        self.spikes = []
        self.voltages = defaultdict(list)
        self.avalanches = []
    
    def setup_neurons(self):
        """设置 LIF 神经元"""
        
        # 神经元方程
        eqs = '''
        dv/dt = (I_ext + I_syn - v) / tau_m : volt
        dI_syn/dt = -I_syn / tau_syn : amp
        '''
        
        # 创建神经元组
        self.neurons = b2.NeuronGroup(
            self.n_neurons,
            eqs,
            threshold='v > -50*mV',
            reset='v = -70*mV',
            method='exponential_euler'
        )
        
        # 初始化
        self.neurons.v = -65*mV + np.random.randn(self.n_neurons)*5*mV
        self.neurons.I_syn = 0*amp
        
        # 参数
        self.neurons.tau_m = 20*b2.ms
        self.neurons.tau_syn = 5*b2.ms
        self.neurons.I_ext = 10*b2.pA  # 外部输入
    
    def setup_synapses(self):
        """设置突触和 STDP"""
        
        # 获取连接信息
        pre_neurons = []
        post_neurons = []
        weights = []
        
        for synapse in self.connectome['synapses']:
            pre_neurons.append(synapse['pre_neuron'])
            post_neurons.append(synapse['post_neuron'])
            weights.append(synapse.get('weight', 1.0))
        
        # 突触模型
        syn_eqs = '''
        w : 1
        '''
        
        on_pre = '''
        I_syn += w * nanoamp
        '''
        
        on_post = '''
        '''
        
        # 创建突触
        self.synapses = b2.Synapses(
            self.neurons,
            self.neurons,
            syn_eqs,
            on_pre=on_pre,
            on_post=on_post,
            delay=1*b2.ms
        )
        
        # 连接
        for pre, post, w in zip(pre_neurons, post_neurons, weights):
            self.synapses.connect(i=pre, j=post)
            self.synapses.w[-1] = w
    
    def setup_monitoring(self):
        """设置数据收集"""
        
        # 记录放电
        self.spike_monitor = b2.SpikeMonitor(self.neurons)
        
        # 记录电压（采样 100 个神经元）
        sample_neurons = np.random.choice(self.n_neurons, 100, replace=False)
        self.state_monitor = b2.StateMonitor(
            self.neurons,
            'v',
            record=sample_neurons
        )
    
    def run_simulation(self):
        """运行仿真"""
        
        print(f"运行 {self.duration} 的仿真...")
        
        # 创建网络
        net = b2.Network(
            self.neurons,
            self.synapses,
            self.spike_monitor,
            self.state_monitor
        )
        
        # 运行
        net.run(self.duration)
        
        print(f"仿真完成，收集 {len(self.spike_monitor.spike_trains())} 个放电轨迹")
    
    def analyze_avalanches(self):
        """分析放电雪崩"""
        
        # 获取放电时间戳
        spike_times = self.spike_monitor.t / b2.ms
        spike_neurons = self.spike_monitor.i
        
        # 按时间排序
        sorted_indices = np.argsort(spike_times)
        spike_times = spike_times[sorted_indices]
        spike_neurons = spike_neurons[sorted_indices]
        
        # 检测雪崩（时间窗口 10 ms）
        avalanches = []
        current_avalanche = []
        last_spike_time = 0
        
        for t, n in zip(spike_times, spike_neurons):
            if t - last_spike_time > 10:  # 新雪崩
                if current_avalanche:
                    avalanches.append(current_avalanche)
                current_avalanche = [n]
            else:
                current_avalanche.append(n)
            last_spike_time = t
        
        # 雪崩大小分布
        sizes = [len(av) for av in avalanches]
        
        return sizes
    
    def compute_power_spectrum(self):
        """计算功率谱"""
        
        # 获取放电频率
        spike_times = self.spike_monitor.t / b2.ms
        
        # 时间分箱
        bins = np.arange(0, self.duration / b2.ms, 10)  # 10 ms bins
        counts, _ = np.histogram(spike_times, bins=bins)
        
        # FFT
        fft = np.abs(np.fft.fft(counts))
        freqs = np.fft.fftfreq(len(counts), 10)
        
        # 功率谱
        power = fft[freqs > 0] ** 2
        freqs = freqs[freqs > 0]
        
        return freqs, power

# 使用示例
simulator = NeuralDynamicsSimulator(connectome, duration_ms=3000)
simulator.setup_neurons()
simulator.setup_synapses()
simulator.setup_monitoring()
simulator.run_simulation()

# 分析
avalanche_sizes = simulator.analyze_avalanches()
freqs, power = simulator.compute_power_spectrum()

# 拟合幂律
import powerlaw
fit_size = powerlaw.Fit(avalanche_sizes, discrete=True)
fit_power = powerlaw.Fit(power, discrete=True)

print(f"雪崩大小幂律指数：{fit_size.alpha:.2f}")
print(f"功率谱幂律指数：{fit_power.alpha:.2f}")
```

#### 4.3 计算资源

```
CPU：不实用（太慢）
GPU：NVIDIA GPU + CuPy（推荐）
预期运行时间：12-24 小时（依赖硬件）

硬件建议：
- NVIDIA A100 / H100：6-12 小时
- NVIDIA RTX 3090：24-48 小时
```

#### 4.4 交付物

```
Week4-6_Deliverables/
├─ neural_dynamics_simulator.py (完整仿真)
├─ simulation_results/
│  ├─ spike_trains.h5 (放电数据)
│  ├─ avalanche_sizes.npy (雪崩分布)
│  ├─ power_spectrum.npy (功率谱)
│  └─ simulation_log.txt (运行日志)
├─ analysis_report.md (分析结果)
└─ soc_validation_results.json (SOC 验证)
```

**人力**：2 人（神经形态 + 计算神经科学）
**计算资源**：GPU 12-24 小时
**风险**：中等（参数调试、收敛性）
**预期完成**：2026-08-12 23:59 EDT

---

### 📈 **第 5-6 周（2026-07-30 至 2026-08-12）：统计检验**

**主题**：完整的统计学严谨性

#### 5.1 统计方法

```
对每个指标：

1️⃣ Bootstrap 置信区间
   method: np.random.choice, n=10,000
   result: [CI_lower, CI_upper] at 95%
   
2️⃣ 显著性检验
   method: Mann-Whitney U（非参数）
   null: real == random
   result: p-value
   
3️⃣ 效应量
   method: Cohen's d = (μ1 - μ2) / σ
   result: small/medium/large
   
4️⃣ 多重检验校正
   method: Bonferroni
   α_corrected = 0.05 / 7
```

#### 5.2 代码

```python
# statistical_analysis.py

from scipy import stats
import numpy as np
from statsmodels.stats.multitest import multipletests

class StatisticalAnalysis:
    """完整的统计检验"""
    
    def bootstrap_ci(self, data, n_bootstrap=10000, ci=95):
        """Bootstrap 置信区间"""
        bootstrap_values = []
        for _ in range(n_bootstrap):
            sample = np.random.choice(data, size=len(data), replace=True)
            bootstrap_values.append(np.mean(sample))
        
        lower = np.percentile(bootstrap_values, (100-ci)/2)
        upper = np.percentile(bootstrap_values, 100-(100-ci)/2)
        
        return lower, upper
    
    def mann_whitney_test(self, data1, data2):
        """Mann-Whitney U 检验"""
        statistic, p_value = stats.mannwhitneyu(data1, data2, alternative='two-sided')
        return statistic, p_value
    
    def cohens_d(self, data1, data2):
        """Cohen's d 效应量"""
        n1, n2 = len(data1), len(data2)
        var1, var2 = np.var(data1, ddof=1), np.var(data2, ddof=1)
        
        pooled_std = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
        d = (np.mean(data1) - np.mean(data2)) / pooled_std
        
        return d
    
    def comprehensive_analysis(self, real_metrics, null_metrics):
        """完整的统计分析"""
        
        results = {}
        p_values = []
        
        for metric_name in real_metrics.keys():
            real_data = real_metrics[metric_name]
            null_data = null_metrics[metric_name]
            
            # Bootstrap CI
            ci_lower, ci_upper = self.bootstrap_ci(real_data)
            
            # Mann-Whitney test
            statistic, p_value = self.mann_whitney_test(real_data, null_data)
            p_values.append(p_value)
            
            # Cohen's d
            d = self.cohens_d(real_data, null_data)
            
            results[metric_name] = {
                'mean': np.mean(real_data),
                'ci_lower': ci_lower,
                'ci_upper': ci_upper,
                'p_value': p_value,
                'cohens_d': d,
                'effect_size': 'large' if abs(d) > 0.8 else 'medium' if abs(d) > 0.5 else 'small'
            }
        
        # Bonferroni 校正
        rejected, corrected_pvalues, _, _ = multipletests(
            p_values,
            alpha=0.05,
            method='bonferroni'
        )
        
        # 添加校正后的 p-value
        for i, metric_name in enumerate(real_metrics.keys()):
            results[metric_name]['p_value_corrected'] = corrected_pvalues[i]
            results[metric_name]['significant'] = rejected[i]
        
        return results
```

#### 5.3 交付物

```
Week5-6_Deliverables/
├─ statistical_analysis.py (完整统计)
├─ results_table.csv (格式化结果)
│  格式：
│  metric | mean | CI_lower | CI_upper | p_value | d | effect_size | significant
├─ statistical_report.md (详细报告)
└─ figures/
   ├─ bootstrapped_distributions.png
   ├─ effect_sizes.png
   └─ p_value_summary.png
```

**人力**：1 人
**风险**：低
**预期完成**：2026-08-12 23:59 EDT

---

### ✍️ **第 6-7 周（2026-08-06 至 2026-08-19）：论文修订**

**主题**：将改进成果集成到论文

#### 6.1 核心修改

```markdown
## Methods 部分

### 2.1 数据来源（NEW）
- ✅ 声明使用真实 Hemibrain 连接组
- ✅ 引用 FlyEM 项目
- ✅ 说明数据版本（v3）

### 2.2 网络拓扑计算（REVISED）
- ✅ 替换"随机生成"为"从图中计算"
- ✅ 引用 NetworkX 和 powerlaw 库
- ✅ 明确计算公式

### 2.3 对照实验（NEW）
- ✅ 三种对照的设计
- ✅ 统计检验方法
- ✅ 显著性阈值

## Results 部分

### 3.1 网络指标（REVISED）
- ✅ 表 1：真实网络 vs 对照网络
- ✅ 表 2：p-values 和效应量
- ✅ 图 1：Bootstrap 置信区间

### 3.2 时间动力学（NEW）
- ✅ 放电雪崩分布
- ✅ 功率谱分析
- ✅ 临界指数估计

## Discussion 部分

### 5.1 局限性（REVISED）
- ✅ 承认 v25 的限制
- ✅ 解释 v26 的改进
- ✅ 规划 v27+ 的方向

### 5.2 后续工作（NEW）
- ✅ 8 周改进的完整规划
- ✅ 里程碑和里程表
```

#### 6.2 删除的表述

```
❌ "5/5 指标达标"
❌ "完全验证了 SOC"
❌ "多物种同时验证"
❌ "硬件实现优势明显"
```

#### 6.3 新增的表述

```
✅ "初期验证框架"
✅ "候选的 SOC 迹象"
✅ "概念性验证"
✅ "为后续工作奠定基础"
```

#### 6.4 交付物

```
Week6-7_Deliverables/
├─ V25_REVISED.md (修订版本)
├─ revision_notes.md (修改说明)
├─ new_tables_and_figures.zip
│  ├─ Table_1_NetworkMetrics.png
│  ├─ Table_2_StatisticalResults.png
│  ├─ Figure_1_AvalanchDistribution.png
│  └─ Figure_2_PowerSpectrum.png
└─ manuscript_diff.html (版本对比)
```

**人力**：1 人
**风险**：低
**预期完成**：2026-08-19 23:59 EDT

---

### 📦 **第 7-8 周（2026-08-13 至 2026-08-26）：补充材料 + 发布**

**主题**：完整的学术发布

#### 7.1 补充材料

```
Supplementary Tables:
- Table S1：所有网络指标的详细值
- Table S2：统计检验的完整结果
- Table S3：不同参数设置的敏感性分析
- Table S4：与文献数据的对比

Supplementary Figures:
- Figure S1：神经元类型分布
- Figure S2：度分布拟合
- Figure S3：聚类系数分析
- Figure S4：学习曲线
- Figure S5：稳定性测试
```

#### 7.2 代码发布

```
GitHub Repository Structure:
iNEST-Simulation-v26/
├─ README.md (详细说明)
├─ data/
│  ├─ hemibrain_connectome_v3.json
│  ├─ celegans_connectome.json
│  └─ null_models/
├─ src/
│  ├─ data_loader.py
│  ├─ metrics_calculator.py
│  ├─ null_model_comparison.py
│  ├─ neural_dynamics_simulator.py
│  └─ statistical_analysis.py
├─ notebooks/
│  ├─ 01_data_loading.ipynb
│  ├─ 02_metrics_calculation.ipynb
│  ├─ 03_null_model_comparison.ipynb
│  ├─ 04_neural_dynamics.ipynb
│  └─ 05_statistical_analysis.ipynb
├─ results/
│  ├─ metrics_results.csv
│  ├─ statistical_results.csv
│  └─ figures/
├─ tests/
│  ├─ test_data_loader.py
│  ├─ test_metrics.py
│  └─ test_analysis.py
└─ LICENSE (MIT)
```

#### 7.3 文档

```
├─ INSTALLATION.md (安装指南)
├─ QUICKSTART.md (快速开始)
├─ API_DOCUMENTATION.md (API 文档)
├─ CONTRIBUTING.md (贡献指南)
└─ CITATION.bib (引用格式)
```

#### 7.4 交付物

```
Week7-8_Deliverables/
├─ supplementary_materials.zip (所有补充材料)
├─ github_repository/ (完整的代码发布)
├─ release_notes.md (发布说明)
└─ MANIFEST.md (所有文件清单)
```

**人力**：1 人
**风险**：低
**预期完成**：2026-08-26 23:59 EDT

---

## 第二部分：资源与时间表

### 📊 资源预算

| 周次 | 任务 | 人力 | 计算资源 | 成本 |
|------|------|------|---------|------|
| W1 | 数据准备 | 1人 | CPU | 低 |
| W2-3 | 指标实现 | 1.5人 | CPU | 低 |
| W3-4 | 对照实验 | 1人 | CPU | 低 |
| W4-6 | 时间动力学 | 2人 | GPU 24h | 中 |
| W5-6 | 统计检验 | 1人 | CPU | 低 |
| W6-7 | 论文修订 | 1人 | - | 低 |
| W7-8 | 发布 | 1人 | - | 低 |

**总人力**：7-8 人周
**总成本**：约 $500-1000（主要是 GPU）

### 📅 甘特图

```
Week 1    [========] Data Prep
Week 2-3  [============================] Metrics
Week 3-4  [============================] Null Models
Week 4-6  [================================================] Neural Dynamics
Week 5-6  [============================] Statistics
Week 6-7  [============================] Revision
Week 7-8  [============================] Release

Timeline: July 2 - August 26, 2026 (8 weeks)
```

---

## 第三部分：预期成果与质量保证

### 🎯 完成度指标

```
当前（v25）：1.5/5 (30%)
目标（v26）：4.5/5 (90%)

具体指标：
- 数据真实性：0% → 100%
- 公式完整性：0% → 100%
- 对照实验：0个 → 3种
- 统计严谨：0% → 100%
- 时间动力学：0% → 100%

综合提升：3 倍
```

### 📈 投稿预期

```
v25（当前）
  ❌ Nature/Science（不可能）
  ❌ eLife（不可能）
  ❌ Nature 子刊（不可能）
  ⚠️  Frontiers（可能）
  ⚠️  预测拒稿率 90%

v26（改进后）
  ✅ eLife（Accept with Minor Revision，60-70%）
  ✅ PLoS Computational Biology（Accept，70-80%）
  ✅ Frontiers（Accept，80-90%）
  ✅ 预测接受率 70%+
```

### ✅ 质量检查点

```
Week 1 末
☐ 数据加载验证通过
☐ 单元测试 100% 通过
☐ 文档完整

Week 3 末
☐ 所有指标计算正确
☐ 与文献对标通过
☐ 对照实验显著

Week 6 末
☐ 时间动力学稳定收敛
☐ SOC 指数估计准确
☐ 统计显著性确认

Week 8 末
☐ 代码发布可复现
☐ 文档完整
☐ 投稿就绪
```

---

## 第四部分：风险管理

### 🔴 高风险项（需特别关注）

1. **时间动力学仿真收敛（Week 4-6）**
   - 风险：参数不匹配导致放电不稳定
   - 缓解：
     * 从小规模（1000 neurons）开始测试
     * 参数扫描确定稳定区域
     * 预留 1 周调试时间

2. **GPU 计算资源不足**
   - 风险：仿真时间过长，拖延进度
   - 缓解：
     * 提前申请 GPU 资源
     * 准备 CPU 备选方案（速度慢但能跑）
     * 考虑云计算（AWS/GCP）

3. **数据完整性问题**
   - 风险：Hemibrain 数据缺失或格式问题
   - 缓解：
     * Week 1 充分验证
     * 准备 C.elegans 备选
     * 与 FlyEM 团队联系获取官方支持

### 🟡 中风险项

- 文献对标数据不一致
- 对照网络生成算法效率低
- 统计方法理解有误

### 🟢 低风险项

- 论文修订
- 代码发布
- 文档编写

---

## 第五部分：里程碑确认

### ✅ Go/No-Go 决策点

**Week 1 末（2026-07-08）**
```
Go/NoGo 检查：
☐ Hemibrain 数据完整（25,000 neurons 确认）
☐ 数据加载器运行成功
☐ 单元测试通过

Go 条件：所有 ☐ 通过
NoGo 条件：任何一个失败 → 调试 1 周后重试
```

**Week 3 末（2026-07-22）**
```
Go/NoGo 检查：
☐ 7 个指标计算正确
☐ 与文献对标通过 ±10%
☐ 对照实验显著（p < 0.05）

Go 条件：所有 ☐ 通过
NoGo 条件：指标计算错误 → 回到 Week 2 修改
```

**Week 6 末（2026-08-12）**
```
Go/NoGo 检查：
☐ 仿真稳定收敛
☐ 放电雪崩幂律分布 (α ∈ [1.0, 2.5])
☐ 功率谱 1/f 噪声确认

Go 条件：所有 ☐ 通过
NoGo 条件：仿真不稳定 → 延期 1 周调参
```

---

## 总结与立即行动

### 🚀 **立即行动（本周）**

```
今天/明天完成：
☐ 确认 Hemibrain 数据源
☐ 建立开发环境（Brian2 + NetworkX）
☐ 创建项目结构

本周完成（Week 1）：
☐ data_loader.py 完成
☐ 单元测试通过
☐ Week 1 Go/NoGo 检查
```

### 📞 **关键联系**

```
- FlyEM 团队（Hemibrain 数据支持）
- 统计学顾问（方法论指导）
- GPU 资源管理员（计算资源申请）
```

### 📚 **参考文献**

```
[1] Eguiluz et al. (2005) - 神经网络拓扑
[2] Clauset et al. (2009) - 幂律拟合
[3] Newman (2003) - 小世界网络
[4] Breakspear et al. (2010) - 神经动力学
[5] Bak et al. (1987) - 自组织临界态
```

---

**文档版本**：v1.0-EXECUTABLE
**生成时间**：2026-07-02 19:07 EDT
**下一次更新**：2026-07-09（Week 1 完成后）

**关键提示**：本计划是严格的，所有时间表假设团队能够满足人力和计算资源。建议 Week 1 末进行 Go/NoGo 检查确保进度。

