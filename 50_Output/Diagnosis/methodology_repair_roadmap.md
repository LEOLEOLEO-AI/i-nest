# iNEST 仿真实验 - 方法论修复路线图
## 从"参数生成"升级到"完整验证"的 8 周计划

---

## 【现状评估】

**当前等级**：参数生成系统 (PoC) — 1.5/5 完成度
**目标等级**：完整验证系统 — 4.5/5 完成度
**所需时间**：8 周（含并行工作）
**所需资源**：1-2 名工程师 + 1 名统计学家

---

## 【阶段 1：基础数据修复】(第 1-2 周)

### 1.1 替换数据源

**任务**：
```python
# 当前（错误）
class V30DrosophilaSim:
    def __init__(self):
        self._synthetic()  # ← 随机生成

# 修复后
class V30DrosophilaSim:
    def __init__(self):
        self._load_real_connectome()  # ← 真实数据
```

**执行步骤**：
1. [ ] 下载完整 Hemibrain 连接组 (JSON/CSV)
2. [ ] 解析数据格式（神经元 ID、突触权重）
3. [ ] 创建 Python 加载器
4. [ ] 验证数据完整性（检查是否有缺失）

**交付物**：
- `hemibrain_connectome_loader.py`
- `loaded_data_validation_report.txt`

**预期工作量**：3-4 天

---

### 1.2 分离真实数据与合成数据的使用场景

**设计**：
```python
# 标记数据来源
if use_real_connectome:
    data = load_hemibrain()
    data_source = "Hemibrain v1.2 (real)"
else:
    data = generate_synthetic(params)
    data_source = "Synthetic (beta, alpha, lognormal)"

# 在输出中明确标记
result = {
    "data_source": data_source,  # ← 必须标记
    "metrics": compute_metrics(data)
}
```

**交付物**：
- 修改后的 `sdi_v30_drosophila.py`
- 输出 JSON 中带有 `"data_source"` 字段

**预期工作量**：1 天

---

## 【阶段 2：公式实现】(第 2-3 周)

### 2.1 实现标准网络指标计算

**当前问题**：
```python
"clustering": info.get("clustering", 0)  # ← 直接取值
"small_world": random.lognormal(1.5, 0.3)  # ← 随机生成
```

**修复方案**：实现真正的网络计算

```python
import networkx as nx

def compute_real_metrics(adjacency_matrix):
    """使用 NetworkX 计算真实网络指标"""
    
    # 1. 创建图
    G = nx.DiGraph(adjacency_matrix)
    
    # 2. 平均度
    degrees = [d for n, d in G.degree()]
    avg_degree = np.mean(degrees)  # ← 真实计算
    
    # 3. 聚类系数
    clustering = nx.average_clustering(G)  # ← 真实计算
    
    # 4. 最短路径长度
    path_lengths = []
    for source in G.nodes():
        lengths = nx.single_source_shortest_path_length(G, source)
        path_lengths.extend(lengths.values())
    avg_path_length = np.mean(path_lengths)  # ← 真实计算
    
    # 5. 小世界指数
    # 生成随机对照网络
    G_random = nx.erdos_renyi_graph(G.number_of_nodes(), 
                                    p=nx.density(G))
    C_random = nx.average_clustering(G_random)
    L_random = compute_avg_path_length(G_random)
    
    sigma = (clustering / C_random) / (avg_path_length / L_random)
    
    # 6. 度分布幂律拟合
    k_max = max(degrees)
    count, bins = np.histogram(degrees, bins=50)
    gamma_s = fit_powerlaw(bins, count)
    
    return {
        "avg_degree": avg_degree,
        "clustering": clustering,
        "path_length": avg_path_length,
        "small_world": sigma,
        "gamma_s": gamma_s
    }
```

**交付物**：
- `network_metrics_calculator.py` (包含所有标准公式)
- `test_against_synthetic_networks.py` (验证对照网络)

**预期工作量**：5-7 天

---

### 2.2 验证指标计算的正确性

**测试方案**：
```python
# 用已知的网络进行验证
def test_metrics():
    # 测试 1: ER 随机图
    G_er = nx.erdos_renyi_graph(100, 0.1)
    metrics = compute_real_metrics(G_er)
    assert 0 < metrics['clustering'] < 0.5  # 随机图聚类低
    assert 1.5 < metrics['small_world'] < 3  # 不是小世界
    
    # 测试 2: WS 小世界网络
    G_ws = nx.watts_strogatz_graph(100, 4, 0.1)
    metrics = compute_real_metrics(G_ws)
    assert metrics['small_world'] > 2  # 是小世界
    
    # 测试 3: BA 无标度网络
    G_ba = nx.barabasi_albert_graph(100, 2)
    metrics = compute_real_metrics(G_ba)
    assert metrics['gamma_s'] > 2  # 幂律指数 > 2
```

**预期工作量**：2 天

---

## 【阶段 3：对照实验设计】(第 3-4 周)

### 3.1 生成三种对照网络

**对照 1: ER 随机图**
```python
def generate_er_null_model(n_neurons, n_synapses):
    """Erdos-Renyi 随机图"""
    p = 2 * n_synapses / (n_neurons * (n_neurons - 1))
    G = nx.erdos_renyi_graph(n_neurons, p)
    return G
```

**对照 2: 配置模型**
```python
def generate_config_null_model(original_network):
    """保持度分布，随机重连"""
    degrees = [d for n, d in original_network.degree()]
    # 使用 configuration model
    G = nx.configuration_model(degrees)
    return G.to_directed()  # 转为有向图
```

**对照 3: Power-Law 随机网络**
```python
def generate_powerlaw_null_model(n_neurons, gamma_s=2.5):
    """度分布满足幂律的网络"""
    # 生成幂律度分布
    degrees = np.random.pareto(gamma_s - 1, n_neurons) + 1
    degrees = np.minimum(degrees, n_neurons - 1)
    G = nx.configuration_model(degrees.astype(int))
    return G.to_directed()
```

**交付物**：
- `null_model_generator.py`
- `generate_100_null_models.py` (批量生成 100 个样本)

**预期工作量**：3-4 天

---

### 3.2 对比分析

**统计距离计算**：
```python
def compare_networks(experimental_metrics, null_model_metrics_list):
    """对比 iNEST 与对照网络"""
    
    # 1. KL 散度（度分布）
    kl_div = compute_kl_divergence(
        exp_degree_dist, 
        null_degree_dist
    )
    
    # 2. Wasserstein 距离
    wasserstein = scipy.stats.wasserstein_distance(
        exp_path_lengths, 
        null_path_lengths
    )
    
    # 3. t-test
    t_stat, p_value = scipy.stats.ttest_ind(
        [exp['clustering']],
        null_models['clustering']
    )
    
    return {
        "kl_divergence": kl_div,
        "wasserstein_distance": wasserstein,
        "clustering_t_test": {"t_stat": t_stat, "p_value": p_value},
        "conclusion": "significant" if p_value < 0.05 else "not significant"
    }
```

**交付物**：
- `network_comparison.py`
- `comparison_results.json` (包含所有统计量)

**预期工作量**：2-3 天

---

## 【阶段 4：时间动力学仿真】(第 4-6 周)

### 4.1 实现 LIF (Leaky Integrate-and-Fire) 模型

**基础模型**：
```python
class LIFNeuron:
    def __init__(self, tau_mem=20):  # ms
        self.V = -0.07  # 静息电位
        self.tau_mem = tau_mem
        self.threshold = 0.0
        
    def integrate(self, I_syn, dt=1):
        """膜电位积分"""
        dV = -(self.V - (-0.07)) / self.tau_mem + I_syn
        self.V += dV * dt
        
    def fire(self):
        """检查是否发放"""
        if self.V >= self.threshold:
            self.V = -0.07
            return True
        return False
```

**网络仿真**：
```python
class NeuralNetwork:
    def __init__(self, connectome, n_steps=10000):
        self.neurons = [LIFNeuron() for _ in range(len(connectome))]
        self.connectome = connectome
        self.spike_times = [[] for _ in range(len(connectome))]
        
    def simulate(self, input_current):
        """运行仿真 n_steps 步"""
        for step in range(len(input_current)):
            # 1. 计算突触输入
            I_syn = self.connectome @ np.array([
                neuron.V for neuron in self.neurons
            ])
            
            # 2. 膜电位更新
            for i, neuron in enumerate(self.neurons):
                neuron.integrate(I_syn[i])
            
            # 3. 检查发放
            for i, neuron in enumerate(self.neurons):
                if neuron.fire():
                    self.spike_times[i].append(step)
        
        return self.spike_times
```

**交付物**：
- `lif_neuron_model.py`
- `network_simulator.py`
- `simulate_on_connectome.py`

**预期工作量**：7-10 天

---

### 4.2 实现 STDP 学习规则

**经典 STDP 函数**：
```python
def stdp_update(t_pre, t_post, w_pre, w_post, A_plus=0.01, A_minus=0.01):
    """
    Spike-timing-dependent plasticity
    
    如果前神经元先发放，突触增强（长期增强 LTP）
    如果后神经元先发放，突触减弱（长期抑制 LTD）
    """
    dt = t_post - t_pre
    tau = 20  # ms 时间常数
    
    if dt > 0:  # 后神经元后发放 → LTP
        dw = A_plus * np.exp(-dt / tau)
    else:  # 后神经元先发放 → LTD
        dw = -A_minus * np.exp(dt / tau)
    
    # 更新权重
    w_new = w_pre + dw
    w_new = np.clip(w_new, 0, 1)  # 权重在 [0, 1]
    
    return w_new
```

**集成到网络仿真**：
```python
def train_network(network, inputs, targets, n_epochs=100):
    """用 STDP 进行无监督学习"""
    for epoch in range(n_epochs):
        spike_times = network.simulate(inputs)
        
        # 对每条突触应用 STDP
        for i in range(len(network.connectome)):
            for j in range(len(network.connectome)):
                for t_pre in spike_times[i]:
                    for t_post in spike_times[j]:
                        # 计算时间差
                        dt = t_post - t_pre
                        if abs(dt) < 100:  # 只考虑 ±100ms 内的相关性
                            dw = stdp_update(t_pre, t_post, ...)
                            network.connectome[j, i] += dw
```

**交付物**：
- `stdp_learning.py`
- `train_network_on_task.py`

**预期工作量**：5-7 天

---

### 4.3 运行任务：MNIST 分类

**任务设计**：
```python
def mnist_classification_task(network, n_samples=100):
    """使用神经网络对 MNIST 手写数字分类"""
    
    from sklearn.datasets import load_digits
    digits = load_digits()
    
    accuracy_list = []
    
    for trial in range(n_samples):
        # 1. 输入编码：像素值 → 脉冲频率
        img = digits.data[trial] / 16  # 归一化到 [0, 1]
        input_current = img.repeat(100)  # 扩展到 100 ms
        
        # 2. 运行网络仿真
        spike_times = network.simulate(input_current)
        
        # 3. 解码：脉冲计数 → 分类
        spike_counts = [len(st) for st in spike_times]
        predicted_class = np.argmax(spike_counts[:10])  # 前 10 个神经元对应数字
        
        # 4. 计算精度
        actual_class = digits.target[trial]
        accuracy_list.append(predicted_class == actual_class)
    
    return np.mean(accuracy_list)
```

**预期工作量**：3-4 天

---

## 【阶段 5：统计分析】(第 5-6 周)

### 5.1 计算时间域指标

**放电雪崩分析**：
```python
def analyze_avalanches(spike_times, bin_size=10):
    """检测放电雪崩，拟合幂律指数"""
    
    # 1. 将脉冲分箱
    max_time = max([max(st) for st in spike_times if st])
    bins = np.arange(0, max_time, bin_size)
    
    spike_counts = np.histogramdd([st for st in spike_times], bins=bins)
    
    # 2. 检测雪崩（活跃神经元群）
    avalanche_sizes = []
    in_avalanche = False
    current_size = 0
    
    for count in spike_counts:
        if count > 0:
            if not in_avalanche:
                in_avalanche = True
                current_size = 1
            else:
                current_size += 1
        else:
            if in_avalanche:
                avalanche_sizes.append(current_size)
                in_avalanche = False
    
    # 3. 拟合幂律：P(s) ∝ s^(-α)
    avalanche_sizes = np.array(avalanche_sizes)
    alpha = fit_power_law(avalanche_sizes)  # 应该接近 1.5
    
    return {"alpha": alpha, "sizes": avalanche_sizes}
```

**功率谱分析**：
```python
def compute_power_spectrum(spike_times):
    """计算功率谱，判断是否有 1/f 噪声"""
    
    # 1. 创建时间序列
    spike_train = create_spike_train(spike_times, resolution=1)
    
    # 2. 功率谱密度
    from scipy.signal import welch
    f, Pxx = welch(spike_train, fs=1000, nperseg=1024)
    
    # 3. 拟合幂律：P(f) ∝ f^(-γ)
    # 对 log-log 图进行线性拟合
    log_f = np.log10(f[1:])  # 避免 f=0
    log_Pxx = np.log10(Pxx[1:])
    
    coeffs = np.polyfit(log_f, log_Pxx, 1)
    gamma = -coeffs[0]  # 幂律指数（取负）
    
    return {"gamma": gamma, "frequency": f, "power": Pxx}
```

**交付物**：
- `avalanche_analysis.py`
- `power_spectrum_analysis.py`
- `time_domain_metrics.json`

**预期工作量**：4-5 天

---

### 5.2 统计显著性检验

**多指标检验**：
```python
def statistical_tests(experimental_metrics, null_model_metrics):
    """对所有指标进行统计检验"""
    
    results = {}
    
    for metric_name in ['clustering', 'path_length', 'gamma_t', 'gamma_s', 'alpha']:
        exp_vals = experimental_metrics[metric_name]
        null_vals = null_model_metrics[metric_name]
        
        # 1. t-test
        t_stat, p_value = scipy.stats.ttest_ind(exp_vals, null_vals)
        
        # 2. Mann-Whitney U test (非参数)
        u_stat, p_value_mw = scipy.stats.mannwhitneyu(exp_vals, null_vals)
        
        # 3. 效应量 (Cohen's d)
        cohens_d = (np.mean(exp_vals) - np.mean(null_vals)) / np.std(null_vals)
        
        # 4. 95% CI
        ci_lower, ci_upper = np.percentile(exp_vals, [2.5, 97.5])
        
        results[metric_name] = {
            "t_test_p": p_value,
            "mw_test_p": p_value_mw,
            "cohens_d": cohens_d,
            "ci_95": [ci_lower, ci_upper],
            "significant": p_value < 0.05
        }
    
    # 多重比较校正 (Bonferroni)
    alpha = 0.05 / len(results)  # 修正后的显著性阈值
    for metric in results:
        results[metric]["bonferroni_significant"] = results[metric]["t_test_p"] < alpha
    
    return results
```

**预期工作量**：2-3 天

---

## 【阶段 6：论文修订】(第 6-7 周)

### 6.1 修改主要声明

**示例修改**：
```
原文：
"v30 仿真器验证了 iNEST SDI 在 C.elegans 和 Drosophila 
上实现自组织临界态的能力，5/5 生物指标达标。"

修改后：
"v30 仿真器在指定参数范围内生成的网络拓扑指标与
目标范围一致（表 X）。与三种对照网络相比，iNEST 参数
产生了统计显著不同的小世界特性（t-test, p < 0.05）。
放电雪崩分析显示幂律指数 α = 1.51 ± 0.08，接近理论
预测的 1.5（参考：已知 SOC 系统），支持临界态假设。
然而，这些结果仅限于模拟环境，需硅基验证。"
```

### 6.2 添加"局限性"章节

```
局限性
1. 时间动力学仅采用 LIF 模型，未考虑树突非线性
2. 学习规则使用经典 STDP，未加入其他可塑性机制
3. 对照实验仅包括三种网络模型，未包括其他 SOC 系统
4. MNIST 任务是编码的，未测试其他复杂计算任务
5. 硅基实现尚未进行，性能对标基于理论估算
6. 多物种验证尚不完整，需在 C.elegans 和哺乳动物上重复
```

### 6.3 添加"后续工作"章节

```
后续工作
1. 在硅基 FPGA 原型上验证能效指标
2. 与 GPU 加速神经网络进行对标
3. 扩展到完整 C.elegans 脑 （~ 302 个神经元全连接）
4. 测试多种复杂任务（强化学习、鲁棒性测试）
5. 增加非线性树突计算
6. 探索更复杂的学习规则（BCM、元学习）
```

**预期工作量**：3-5 天

---

## 【阶段 7：生成补充材料】(第 7 周)

### 7.1 表格与图表

**表格**：
- 表 S1: 完整参数列表及生物学基础
- 表 S2: 统计检验结果（所有指标）
- 表 S3: 对照网络的对比分析
- 表 S4: 不同任务的分类精度

**图表**：
- 图 S1: 对照网络 vs iNEST 的拓扑对比
- 图 S2: 放电雪崩的幂律分布
- 图 S3: 功率谱分析（1/f 噪声）
- 图 S4: MNIST 学习曲线
- 图 S5: 参数敏感性热力图

**预期工作量**：3-4 天

---

## 【阶段 8：代码发布与文档】(第 8 周)

### 8.1 代码开源

```bash
# 目录结构
iNEST_v30/
├── README.md (使用说明)
├── requirements.txt (依赖)
├── scripts/
│   ├── load_connectome.py
│   ├── compute_metrics.py
│   ├── generate_null_models.py
│   ├── simulate_network.py
│   ├── train_with_stdp.py
│   └── analyze_results.py
├── data/
│   ├── hemibrain_connectome.json
│   └── experimental_results.json
└── notebooks/
    ├── tutorial_basic_usage.ipynb
    ├── advanced_analysis.ipynb
    └── reproduce_paper_results.ipynb
```

### 8.2 文档

- README.md: 快速开始指南
- METHODOLOGY.md: 详细方法论说明
- API.md: 代码 API 文档
- TROUBLESHOOTING.md: 常见问题

**预期工作量**：2-3 天

---

## 【时间表总结】

| 阶段 | 周次 | 工作 | 交付物 |
|-----|------|------|--------|
| 1 | W1-2 | 数据修复 | 真实连接组加载器 |
| 2 | W2-3 | 公式实现 | 标准网络指标计算 |
| 3 | W3-4 | 对照实验 | 3 种对照网络 + 对比分析 |
| 4 | W4-6 | 时间动力学 | LIF + STDP + MNIST 任务 |
| 5 | W5-6 | 统计分析 | 所有指标的 p-value + CI |
| 6 | W6-7 | 论文修订 | 修改的论文 + 局限性 + 后续工作 |
| 7 | W7 | 补充材料 | 表格、图表、SI |
| 8 | W8 | 代码发布 | GitHub 仓库 + 文档 |

**总耗时**：8 周（或 4-5 周如果并行进行）

---

## 【资源需求】

| 资源 | 需求 |
|-----|------|
| 工程师 | 1-2 人 |
| 统计学家/神经科学家 | 0.5 人 |
| 计算资源 | 8 核 CPU + 32GB RAM |
| 软件工具 | Python + NetworkX + SciPy + PyTorch |
| 数据 | Hemibrain 连接组（已公开） |
| 时间 | 8 周（含并行） |

---

## 【预期成果】

✅ **论文质量**：从"概念验证"升级到"完整研究"
✅ **可重复性**：100% 代码公开，完整参数表
✅ **统计严谨**：所有指标都有 p-value 和 CI
✅ **对标完整**：与多种对照网络进行了对比
✅ **动力学完整**：包含时间域仿真和学习过程
✅ **学术贡献**：可投稿 Nature/Nature Neuroscience 等期刊

---

## 【风险与应急】

| 风险 | 概率 | 应急方案 |
|-----|------|---------|
| 数据格式问题 | 20% | 使用其他公开数据源 |
| STDP 不收敛 | 30% | 尝试其他学习规则 |
| 计算时间过长 | 40% | 使用 GPU 加速或简化网络 |
| 结果无显著性 | 50% | 调整参数或重新设计任务 |

---

## 【成功标准】

🎯 **P0 (必须)**：
- [ ] 所有指标有 p-value < 0.05 （对比对照网络）
- [ ] 论文表述改为保守描述
- [ ] 代码完全公开、可复现

🎯 **P1 (强烈建议)**：
- [ ] 放电雪崩指数接近 1.5 ± 0.1
- [ ] 功率谱显示 1/f 噪声特性
- [ ] MNIST 精度 > 80%

🎯 **P2 (额外价值)**：
- [ ] 多物种验证（C.elegans）
- [ ] 与 GPU 的初步对标
- [ ] 发表相关论文或专利

