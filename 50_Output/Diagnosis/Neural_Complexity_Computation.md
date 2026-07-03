# 生物神经网络数据分析：从原始数据到 4 大复杂度指标

## 🎯 目标
从 Codex 获取的神经网络数据直接计算：
1. 时间复杂度 (Temporal Complexity, γ_t)
2. 空间复杂度 (Spatial Complexity, γ_s)  
3. 时空协同系数 (Spatio-Temporal Coupling, STC)
4. 非线性放大指数 (Nonlinear Amplification Alpha, α)

---

## 第一部分：数据格式与预处理

### 输入数据格式规范

```python
import numpy as np
import pandas as pd
from scipy import signal, stats
from scipy.fft import fft, fftfreq
import networkx as nx

# 预期的数据结构
class NeuralNetworkData:
    """生物神经网络数据容器"""
    def __init__(self):
        # 1️⃣ 连通性数据
        self.adjacency_matrix = None  # (N_neurons, N_neurons) 邻接矩阵
        self.synaptic_weights = None  # (N_neurons, N_neurons) 突触权重
        
        # 2️⃣ 时间序列数据（多电极阵列或光学成像）
        self.spike_times = None       # dict: neuron_id -> list of spike times (ms)
        self.membrane_potential = None  # (N_neurons, T_samples) 膜电位时间序列
        self.neural_activity = None   # (N_neurons, T_samples) 神经活动二进制矩阵
        
        # 3️⃣ 元数据
        self.neuron_positions = None  # (N_neurons, 3) 或 (N_neurons, 2) 神经元空间坐标
        self.neuron_types = None      # list 神经元类型标注
        self.sampling_rate = 1000     # Hz (默认 1 kHz)
        self.species = None           # 物种名称
        self.brain_region = None      # 脑区

# 示例：从 Codex 获取的数据加载
def load_neural_data_from_codex(data_path):
    """从 Codex 获取的数据加载"""
    data = NeuralNetworkData()
    
    # 假设 Codex 导出的格式
    if 'connectome.npy' in data_path:
        data.adjacency_matrix = np.load(f'{data_path}/connectome.npy')
    
    if 'spike_times.pkl' in data_path:
        import pickle
        with open(f'{data_path}/spike_times.pkl', 'rb') as f:
            data.spike_times = pickle.load(f)
    
    if 'membrane_potential.npy' in data_path:
        data.membrane_potential = np.load(f'{data_path}/membrane_potential.npy')
    
    if 'neuron_coords.npy' in data_path:
        data.neuron_positions = np.load(f'{data_path}/neuron_coords.npy')
    
    return data

# 检查数据完整性
def validate_neural_data(data):
    """验证数据完整性"""
    print("=== 数据验证 ===")
    
    if data.adjacency_matrix is not None:
        n_neurons = data.adjacency_matrix.shape[0]
        n_synapses = np.sum(data.adjacency_matrix > 0)
        print(f"✓ 连接矩阵: {n_neurons} 个神经元, {n_synapses} 个突触")
    
    if data.membrane_potential is not None:
        n_neurons, n_samples = data.membrane_potential.shape
        duration_s = n_samples / data.sampling_rate
        print(f"✓ 膜电位: {n_neurons} 个神经元, {n_samples} 个样本 ({duration_s:.1f}s)")
    
    if data.spike_times is not None:
        n_neurons = len(data.spike_times)
        total_spikes = sum(len(times) for times in data.spike_times.values())
        print(f"✓ 放电数据: {n_neurons} 个神经元, {total_spikes} 次放电")
    
    if data.neuron_positions is not None:
        print(f"✓ 空间坐标: {data.neuron_positions.shape[0]} 个神经元, {data.neuron_positions.shape[1]}D")
```

---

## 第二部分：4 大复杂度指标计算

### 1️⃣ 时间复杂度 (γ_t)

**定义**：神经网络活动时间序列的功率谱中 1/f 噪声的指数。
- γ_t ≈ 1.0：临界态（Pink Noise，1/f）
- γ_t < 1.0：噪音主导（White Noise，1/f^0）
- γ_t > 1.5：高度相关（Brown Noise，1/f^2）

```python
def compute_temporal_complexity(spike_times, dt=1, freq_band=(0.1, 100)):
    """
    计算时间复杂度 γ_t
    
    Parameters:
    -----------
    spike_times : dict or list
        spike_times[neuron_id] = [t1, t2, ...] 放电时间序列
        或 (N_neurons, T_samples) 二进制矩阵
    dt : float
        时间分辨率 (ms，默认 1 ms)
    freq_band : tuple
        要分析的频率范围 (min_Hz, max_Hz)
    
    Returns:
    --------
    gamma_t : float
        时间复杂度指数 (1/f 噪声中的幂律指数)
    power_spectrum : np.ndarray
        功率谱密度
    frequencies : np.ndarray
        频率轴
    """
    
    # Step 1: 转换为二进制时间序列
    if isinstance(spike_times, dict):
        # 将放电时间转为二进制矩阵
        T_max = max(max(times) for times in spike_times.values())
        n_neurons = len(spike_times)
        n_bins = int(T_max / dt)
        
        activity = np.zeros((n_neurons, n_bins))
        for neuron_id, times in spike_times.items():
            for t in times:
                idx = int(t / dt)
                if idx < n_bins:
                    activity[neuron_id, idx] = 1
    else:
        activity = spike_times  # 已经是矩阵形式
    
    # Step 2: 计算平均功率谱（所有神经元的平均）
    n_neurons, n_samples = activity.shape
    pxx_all = []
    
    for neuron_id in range(n_neurons):
        # Welch 方法估计功率谱密度（更稳定）
        f, pxx = signal.welch(
            activity[neuron_id, :],
            fs=1000.0 / dt,  # 采样率 (Hz)
            window='hann',
            nperseg=min(1024, n_samples // 4),
            noverlap=None
        )
        pxx_all.append(pxx)
    
    pxx_mean = np.mean(pxx_all, axis=0)
    
    # Step 3: 提取指定频率范围
    freq_min, freq_max = freq_band
    mask = (f >= freq_min) & (f <= freq_max)
    f_band = f[mask]
    pxx_band = pxx_mean[mask]
    
    # Step 4: 功率律拟合：log(P) = -γ_t * log(f) + constant
    # 即 P(f) ~ f^(-γ_t)
    logf = np.log10(f_band[f_band > 0])
    logP = np.log10(pxx_band[pxx_band > 0])
    
    # 线性回归
    coeffs = np.polyfit(logf, logP, 1)
    gamma_t = -coeffs[0]  # 负斜率 = γ_t
    r_squared = np.corrcoef(logf, logP)[0, 1] ** 2
    
    return {
        'gamma_t': gamma_t,
        'gamma_t_err': np.sqrt(1 - r_squared),  # 拟合误差估计
        'power_spectrum': pxx_mean,
        'frequencies': f,
        'r_squared': r_squared
    }

# 使用示例
spike_data = {
    0: np.array([10, 25, 40, 60, 75, 90, 105]),  # 神经元 0 的放电时间
    1: np.array([15, 35, 55, 70, 85, 100]),       # 神经元 1 的放电时间
    # ...
}

result_t = compute_temporal_complexity(spike_data)
print(f"时间复杂度 γ_t = {result_t['gamma_t']:.3f} ± {result_t['gamma_t_err']:.3f}")
print(f"拟合优度 R² = {result_t['r_squared']:.4f}")
```

---

### 2️⃣ 空间复杂度 (γ_s)

**定义**：神经网络度分布（connectivity distribution）中的功率律指数。
- 度分布：P(k) ~ k^(-γ_s)
- γ_s ≈ 2.0-2.5：典型生物网络
- γ_s → ∞：均匀网络；γ_s = 1：高度集中

```python
def compute_spatial_complexity(adjacency_matrix, method='out_degree'):
    """
    计算空间复杂度 γ_s
    
    Parameters:
    -----------
    adjacency_matrix : np.ndarray
        (N_neurons, N_neurons) 邻接矩阵
    method : str
        'out_degree': 出度分布
        'in_degree': 入度分布
        'total_degree': 总度数
    
    Returns:
    --------
    gamma_s : float
        空间复杂度指数
    """
    
    # Step 1: 转为网络图并计算度分布
    G = nx.DiGraph(adjacency_matrix)
    
    if method == 'out_degree':
        degrees = dict(G.out_degree(weight='weight'))
    elif method == 'in_degree':
        degrees = dict(G.in_degree(weight='weight'))
    else:  # total_degree
        degrees = {n: G.in_degree(n, weight='weight') + G.out_degree(n, weight='weight') 
                   for n in G.nodes()}
    
    degree_sequence = np.array(list(degrees.values()))
    degree_sequence = degree_sequence[degree_sequence > 0]  # 移除零度节点
    
    # Step 2: 计算度分布 P(k)
    k_values = np.unique(degree_sequence)
    k_counts = np.bincount(degree_sequence)
    p_k = k_counts[k_counts > 0] / len(degree_sequence)
    
    # Step 3: 功率律拟合
    # P(k) ~ k^(-γ_s)
    # log(P) = -γ_s * log(k) + constant
    
    logk = np.log10(k_values[k_values > 0])
    logp = np.log10(p_k[p_k > 0])
    
    # 线性回归
    coeffs = np.polyfit(logk, logp, 1)
    gamma_s = -coeffs[0]
    r_squared = np.corrcoef(logk, logp)[0, 1] ** 2
    
    # 计算其他拓扑指标
    n_neurons = adjacency_matrix.shape[0]
    density = np.sum(adjacency_matrix > 0) / (n_neurons * (n_neurons - 1))
    clustering = nx.average_clustering(nx.Graph(adjacency_matrix))
    avg_shortest_path = nx.average_shortest_path_length(nx.Graph(adjacency_matrix))
    
    return {
        'gamma_s': gamma_s,
        'gamma_s_err': np.sqrt(1 - r_squared),
        'degree_sequence': degree_sequence,
        'degree_distribution': p_k,
        'r_squared': r_squared,
        'topology': {
            'n_neurons': n_neurons,
            'n_synapses': np.sum(adjacency_matrix > 0),
            'density': density,
            'avg_clustering': clustering,
            'avg_path_length': avg_shortest_path
        }
    }

# 使用示例
connectome = np.random.binomial(1, 0.05, (100, 100))  # 随机网络
result_s = compute_spatial_complexity(connectome)
print(f"空间复杂度 γ_s = {result_s['gamma_s']:.3f}")
print(f"网络密度 = {result_s['topology']['density']:.4f}")
```

---

### 3️⃣ 时空协同系数 (STC)

**定义**：时间活动与空间拓扑的协同程度。
- 量化：神经元之间的时间关联是否受到空间距离的调制
- STC → 1：强时空耦合（相近的神经元时序相关）
- STC → 0：弱耦合（拓扑和时间独立）

```python
def compute_spatiotemporal_coupling(
    spike_times,
    neuron_positions,
    adjacency_matrix=None,
    dt=1,
    max_lag=100
):
    """
    计算时空协同系数 STC
    
    Parameters:
    -----------
    spike_times : dict
        neuron_id -> list of spike times
    neuron_positions : np.ndarray
        (N_neurons, 3) 或 (N_neurons, 2) 神经元坐标
    adjacency_matrix : np.ndarray
        (N_neurons, N_neurons) 邻接矩阵
    dt : float
        时间分辨率 (ms)
    max_lag : int
        互相关最大时延 (ms)
    
    Returns:
    --------
    STC : float
        时空协同系数 (0-1)
    """
    
    # Step 1: 转为二进制活动矩阵
    T_max = max(max(times) for times in spike_times.values())
    n_neurons = len(spike_times)
    n_bins = int(T_max / dt)
    
    activity = np.zeros((n_neurons, n_bins))
    for neuron_id, times in spike_times.items():
        for t in times:
            idx = int(t / dt)
            if idx < n_bins:
                activity[neuron_id, idx] = 1
    
    # Step 2: 计算所有神经元对的时间关联（互相关）
    max_lag_samples = int(max_lag / dt)
    temporal_correlation = np.zeros((n_neurons, n_neurons))
    
    for i in range(n_neurons):
        for j in range(i + 1, n_neurons):
            # 归一化互相关
            corr_ij = signal.correlate(activity[i, :], activity[j, :], mode='same')
            corr_ij = corr_ij / (np.std(activity[i, :]) * np.std(activity[j, :]) + 1e-10)
            
            # 取最大相关值（在时延范围内）
            max_corr = np.max(np.abs(corr_ij[
                len(corr_ij)//2 - max_lag_samples : len(corr_ij)//2 + max_lag_samples
            ]))
            temporal_correlation[i, j] = max_corr
            temporal_correlation[j, i] = max_corr
    
    # Step 3: 计算空间距离矩阵
    spatial_distance = np.zeros((n_neurons, n_neurons))
    for i in range(n_neurons):
        for j in range(i + 1, n_neurons):
            dist_ij = np.linalg.norm(neuron_positions[i] - neuron_positions[j])
            spatial_distance[i, j] = dist_ij
            spatial_distance[j, i] = dist_ij
    
    # Step 4: 时空关联
    # 假设：相近的神经元应该有高的时间相关性
    # STC = 1 - (距离的标准化) / (时间相关的标准化)
    
    # 方法：计算空间近邻和时间近邻的重叠程度
    # 识别"空间近邻对"（距离 < 25 percentile）
    dist_threshold = np.percentile(spatial_distance[spatial_distance > 0], 25)
    spatial_neighbors = spatial_distance < dist_threshold
    
    # 识别"时间相关对"（相关性 > 75 percentile）
    corr_threshold = np.percentile(temporal_correlation[temporal_correlation > 0], 75)
    temporal_correlated = temporal_correlation > corr_threshold
    
    # STC = 两个条件同时满足的对数 / 空间近邻对数
    overlap = np.sum(spatial_neighbors & temporal_correlated)
    spatial_neighbor_count = np.sum(spatial_neighbors)
    
    if spatial_neighbor_count == 0:
        STC = 0
    else:
        STC = overlap / spatial_neighbor_count
    
    # 或者用 Spearman 相关性（更直接）
    # 将距离和相关性展平成向量
    dist_vec = spatial_distance[np.triu_indices_from(spatial_distance, k=1)]
    corr_vec = temporal_correlation[np.triu_indices_from(temporal_correlation, k=1)]
    
    # 相反相关：距离越近，相关性应该越高
    rho_STC, p_value = stats.spearmanr(-dist_vec, corr_vec)
    STC_method2 = max(0, rho_STC)  # 裁剪到 [0, 1]
    
    return {
        'STC': STC,
        'STC_method2': STC_method2,
        'STC_pvalue': p_value,
        'temporal_correlation': temporal_correlation,
        'spatial_distance': spatial_distance
    }

# 使用示例
positions = np.random.rand(50, 3) * 100  # 3D 坐标
spike_dict = {i: np.sort(np.random.rand(100) * 1000) for i in range(50)}

result_stc = compute_spatiotemporal_coupling(spike_dict, positions)
print(f"时空协同系数 STC = {result_stc['STC']:.3f}")
print(f"Spearman 相关 = {result_stc['STC_method2']:.3f} (p={result_stc['STC_pvalue']:.4f})")
```

---

### 4️⃣ 非线性放大指数 Alpha (α)

**定义**：神经网络雪崩事件（avalanche）的大小分布中的功率律指数。
- P(s) ~ s^(-α)
- α ≈ 1.5：临界态（Branching Process）
- α < 1.0：亚临界（活动衰减）
- α > 2.0：超临界（活动增长）

```python
def compute_nonlinear_amplification_alpha(
    spike_times,
    bin_size=10,
    threshold=1
):
    """
    计算非线性放大指数 α
    
    基于雪崩分析（Avalanche Analysis）
    
    Parameters:
    -----------
    spike_times : dict
        neuron_id -> list of spike times (ms)
    bin_size : float
        时间窗口大小 (ms，用于定义雪崩)
    threshold : int
        单个时间窗口内的放电数阈值
    
    Returns:
    --------
    alpha : float
        雪崩功率律指数
    """
    
    # Step 1: 构造多神经元放电序列
    all_spikes = []
    for neuron_id, times in spike_times.items():
        all_spikes.extend(times)
    all_spikes = np.sort(np.array(all_spikes))
    
    # Step 2: 时间离散化 + 计数
    T_min, T_max = all_spikes.min(), all_spikes.max()
    n_bins = int((T_max - T_min) / bin_size) + 1
    spike_counts = np.zeros(n_bins)
    
    for t in all_spikes:
        bin_idx = int((t - T_min) / bin_size)
        spike_counts[bin_idx] += 1
    
    # Step 3: 识别"活跃"时间窗口（放电数 > threshold）
    active_bins = spike_counts > threshold
    
    # Step 4: 定义"雪崩"为连续活跃时间窗口的聚集
    avalanche_sizes = []
    in_avalanche = False
    current_size = 0
    
    for is_active in active_bins:
        if is_active:
            current_size += 1
            in_avalanche = True
        else:
            if in_avalanche and current_size > 0:
                avalanche_sizes.append(current_size)
            current_size = 0
            in_avalanche = False
    
    if in_avalanche and current_size > 0:
        avalanche_sizes.append(current_size)
    
    avalanche_sizes = np.array(avalanche_sizes)
    avalanche_sizes = avalanche_sizes[avalanche_sizes > 0]
    
    if len(avalanche_sizes) < 10:
        print("警告：雪崩样本过少，结果可能不可靠")
    
    # Step 5: 功率律拟合
    # P(s) ~ s^(-α)
    # log(P) = -α * log(s) + constant
    
    s_values = np.unique(avalanche_sizes)
    s_counts = np.bincount(avalanche_sizes)
    p_s = s_counts[s_counts > 0] / len(avalanche_sizes)
    
    logs = np.log10(s_values[s_values > 0])
    logp = np.log10(p_s[p_s > 0])
    
    # 线性回归
    coeffs = np.polyfit(logs, logp, 1)
    alpha = -coeffs[0]
    r_squared = np.corrcoef(logs, logp)[0, 1] ** 2
    
    # 分支比（Branching Ratio）：评估临界态
    # 计算 M = <s|bin_after> / <s|bin_before>
    # M ≈ 1 表示临界态
    branching_ratio = _compute_branching_ratio(spike_counts, bin_size)
    
    return {
        'alpha': alpha,
        'alpha_err': np.sqrt(1 - r_squared),
        'avalanche_sizes': avalanche_sizes,
        'avalanche_distribution': p_s,
        'r_squared': r_squared,
        'branching_ratio': branching_ratio,
        'is_critical': 0.95 <= branching_ratio <= 1.05 and 1.4 <= alpha <= 1.6
    }

def _compute_branching_ratio(spike_counts, bin_size):
    """计算分支比（Branching Ratio）"""
    # 简化版：计算相邻时间窗口放电的相关性
    spike_counts_norm = spike_counts / (np.mean(spike_counts) + 1e-10)
    
    correlation = np.zeros(10)
    for lag in range(1, 11):
        valid_pairs = np.sum((spike_counts_norm[:-lag] > 0) & (spike_counts_norm[lag:] > 0))
        if valid_pairs > 0:
            correlation[lag - 1] = np.mean(
                spike_counts_norm[lag:][spike_counts_norm[:-lag] > 0]
            )
    
    branching_ratio = np.mean(correlation[correlation > 0])
    return max(0, branching_ratio)

# 使用示例
spike_data = {
    0: np.array([10, 15, 20, 25, 30, 50, 55, 100, 101]),
    1: np.array([12, 18, 22, 28, 52, 58, 102]),
    # ...
}

result_alpha = compute_nonlinear_amplification_alpha(spike_data, bin_size=5)
print(f"非线性放大指数 α = {result_alpha['alpha']:.3f}")
print(f"分支比 = {result_alpha['branching_ratio']:.3f}")
print(f"是否临界态 = {result_alpha['is_critical']}")
```

---

## 第三部分：集成分析管道

```python
class ComplexityAnalyzer:
    """完整的复杂度分析框架"""
    
    def __init__(self, neural_data):
        self.data = neural_data
        self.results = {}
    
    def compute_all_metrics(self):
        """计算所有 4 个复杂度指标"""
        
        print("=" * 60)
        print("🧠 生物神经网络复杂度分析")
        print("=" * 60)
        
        # 1️⃣ 时间复杂度
        print("\n[1/4] 计算时间复杂度 γ_t...")
        self.results['temporal'] = compute_temporal_complexity(
            self.data.spike_times
        )
        print(f"  ✓ γ_t = {self.results['temporal']['gamma_t']:.3f}")
        
        # 2️⃣ 空间复杂度
        print("\n[2/4] 计算空间复杂度 γ_s...")
        self.results['spatial'] = compute_spatial_complexity(
            self.data.adjacency_matrix
        )
        print(f"  ✓ γ_s = {self.results['spatial']['gamma_s']:.3f}")
        
        # 3️⃣ 时空协同系数
        print("\n[3/4] 计算时空协同系数 STC...")
        self.results['spatiotemporal'] = compute_spatiotemporal_coupling(
            self.data.spike_times,
            self.data.neuron_positions,
            self.data.adjacency_matrix
        )
        print(f"  ✓ STC = {self.results['spatiotemporal']['STC']:.3f}")
        
        # 4️⃣ 非线性放大指数
        print("\n[4/4] 计算非线性放大指数 α...")
        self.results['avalanche'] = compute_nonlinear_amplification_alpha(
            self.data.spike_times
        )
        print(f"  ✓ α = {self.results['avalanche']['alpha']:.3f}")
        
        return self
    
    def summary_report(self):
        """生成汇总报告"""
        print("\n" + "=" * 60)
        print("📊 复杂度分析汇总报告")
        print("=" * 60)
        
        report = {
            '时间复杂度 γ_t': f"{self.results['temporal']['gamma_t']:.3f} ± {self.results['temporal']['gamma_t_err']:.3f}",
            '空间复杂度 γ_s': f"{self.results['spatial']['gamma_s']:.3f} ± {self.results['spatial']['gamma_s_err']:.3f}",
            '时空协同系数 STC': f"{self.results['spatiotemporal']['STC']:.3f}",
            '非线性放大指数 α': f"{self.results['avalanche']['alpha']:.3f} ± {self.results['avalanche']['alpha_err']:.3f}",
        }
        
        for key, value in report.items():
            print(f"{key:20s} : {value}")
        
        # 临界态评估
        print("\n【临界态评估】")
        is_critical_time = 0.9 <= self.results['temporal']['gamma_t'] <= 1.1
        is_critical_avalanche = 1.4 <= self.results['avalanche']['alpha'] <= 1.6
        is_critical_branching = 0.95 <= self.results['avalanche']['branching_ratio'] <= 1.05
        
        print(f"  时间临界态 (γ_t ≈ 1): {is_critical_time}")
        print(f"  雪崩临界态 (α ≈ 1.5): {is_critical_avalanche}")
        print(f"  分支临界态 (BR ≈ 1): {is_critical_branching}")
        
        overall_critical = is_critical_time and is_critical_avalanche and is_critical_branching
        print(f"\n  综合临界态判定: {'✓ 是' if overall_critical else '✗ 否'}")
        
        return report

# 使用示例
analyzer = ComplexityAnalyzer(neural_data)
analyzer.compute_all_metrics()
report = analyzer.summary_report()
```

---

## 第四部分：可视化与诊断

```python
import matplotlib.pyplot as plt

def plot_complexity_analysis(results):
    """绘制复杂度分析结果"""
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1️⃣ 时间复杂度 - 功率谱
    ax = axes[0, 0]
    f = results['temporal']['frequencies']
    pxx = results['temporal']['power_spectrum']
    ax.loglog(f, pxx, 'b-', linewidth=2, label='观测数据')
    
    # 理论功率律
    f_fit = f[(f > 0.1) & (f < 100)]
    pxx_fit = pxx[(f > 0.1) & (f < 100)]
    ax.loglog(f_fit, pxx_fit, 'r--', linewidth=2, 
              label=f'γ_t = {results["temporal"]["gamma_t"]:.2f}')
    ax.set_xlabel('频率 (Hz)')
    ax.set_ylabel('功率谱密度')
    ax.set_title('1️⃣ 时间复杂度')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 2️⃣ 空间复杂度 - 度分布
    ax = axes[0, 1]
    k = np.arange(1, len(results['spatial']['degree_distribution']) + 1)
    pk = results['spatial']['degree_distribution']
    ax.loglog(k, pk, 'go', markersize=8, label='观测数据')
    
    k_fit = k[pk > 0]
    pk_fit = pk[pk > 0]
    ax.loglog(k_fit, pk_fit, 'r--', linewidth=2,
              label=f'γ_s = {results["spatial"]["gamma_s"]:.2f}')
    ax.set_xlabel('度数 (k)')
    ax.set_ylabel('概率 P(k)')
    ax.set_title('2️⃣ 空间复杂度')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 3️⃣ 时空协同系数 - 相关图
    ax = axes[1, 0]
    corr = results['spatiotemporal']['temporal_correlation']
    im = ax.imshow(corr, cmap='hot', aspect='auto')
    ax.set_xlabel('神经元 j')
    ax.set_ylabel('神经元 i')
    ax.set_title(f'3️⃣ 时空协同系数 (STC={results["spatiotemporal"]["STC"]:.2f})')
    plt.colorbar(im, ax=ax)
    
    # 4️⃣ 非线性放大指数 - 雪崩分布
    ax = axes[1, 1]
    s = np.arange(1, len(results['avalanche']['avalanche_distribution']) + 1)
    ps = results['avalanche']['avalanche_distribution']
    ax.loglog(s, ps, 'mo', markersize=8, label='观测数据')
    
    s_fit = s[ps > 0]
    ps_fit = ps[ps > 0]
    ax.loglog(s_fit, ps_fit, 'r--', linewidth=2,
              label=f'α = {results["avalanche"]["alpha"]:.2f}')
    ax.set_xlabel('雪崩大小 (s)')
    ax.set_ylabel('概率 P(s)')
    ax.set_title('4️⃣ 非线性放大指数')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('complexity_analysis.png', dpi=300)
    print("✓ 分析图已保存为 complexity_analysis.png")
    plt.show()

# 使用
plot_complexity_analysis(analyzer.results)
```

---

## 快速参考表

| 指标 | 符号 | 含义 | 临界态值 | 计算方法 |
|-----|------|------|---------|---------|
| 时间复杂度 | γ_t | 功率谱 1/f 指数 | ≈ 1.0 | Welch 功率谱 + 功率律拟合 |
| 空间复杂度 | γ_s | 度分布功率律指数 | 2.0-2.5 | 网络拓扑 + 功率律拟合 |
| 时空协同系数 | STC | 拓扑-活动耦合程度 | 高耦合 | 相关性 vs 距离 |
| 非线性放大指数 | α | 雪崩大小功率律指数 | ≈ 1.5 | 雪崩分析 + 分支过程 |

---

## 常见问题与调试

```python
def debug_data_quality(neural_data):
    """数据质量诊断"""
    print("【数据质量诊断】")
    
    # 检查缺失数据
    if neural_data.adjacency_matrix is None:
        print("⚠️  缺少邻接矩阵")
    
    if neural_data.spike_times is None:
        print("⚠️  缺少放电数据")
    
    if neural_data.neuron_positions is None:
        print("⚠️  缺少空间坐标（STC 计算受限）")
    
    # 检查数据量
    if neural_data.membrane_potential is not None:
        duration = neural_data.membrane_potential.shape[1] / neural_data.sampling_rate
        if duration < 10:  # 少于 10 秒
            print(f"⚠️  记录时间较短 ({duration:.1f}s)，可能影响时间复杂度估计")
    
    # 检查放电率
    if neural_data.spike_times is not None:
        n_neurons = len(neural_data.spike_times)
        total_spikes = sum(len(times) for times in neural_data.spike_times.values())
        avg_firing_rate = total_spikes / (n_neurons * duration)
        print(f"✓ 平均放电频率: {avg_firing_rate:.1f} Hz")
        
        if avg_firing_rate < 0.1:
            print("⚠️  放电频率过低，可能影响统计可靠性")

# 使用
debug_data_quality(neural_data)
```
