---
direction: iNEST
title: "QUICKSTART"
created: 2026-07-07
modified: 2026-07-07
provenance: external
---
# 快速使用指南：从 Codex 数据到 4 大复杂度指标

## 📁 数据准备

### 第一步：整理 Codex 导出数据

```bash
mkdir -p ~/neural_data/experiment_001
cd ~/neural_data/experiment_001

# 准备的文件结构：
# connectome.npy              (N×N 邻接矩阵，N = 神经元数)
# spike_times.pkl            (dict: neuron_id → [t1, t2, ...])
# neuron_coords.npy          (N×3 坐标矩阵)
# membrane_potential.npy     (可选，N×T 膜电位)
```

### 第二步：验证数据格式

```python
import numpy as np
import pickle

# 检查连接矩阵
conn = np.load('connectome.npy')
print(f"连接矩阵: {conn.shape}, 类型: {conn.dtype}")

# 检查放电数据
with open('spike_times.pkl', 'rb') as f:
    spikes = pickle.load(f)
print(f"放电数据: {len(spikes)} 个神经元, {sum(len(v) for v in spikes.values())} 次放电")

# 检查坐标
coords = np.load('neuron_coords.npy')
print(f"坐标: {coords.shape}")
```

---

## 🚀 快速开始

### 方式 1：使用脚本

```bash
cd /vault/scripts

# 执行分析
python neural_complexity_analyzer.py \
    --data_path ~/neural_data/experiment_001 \
    --output results.json
```

### 方式 2：在 Python 中使用

```python
from neural_complexity_analyzer import NeuralComplexityAnalyzer

# 初始化分析器
analyzer = NeuralComplexityAnalyzer(
    data_path='~/neural_data/experiment_001',
    dt=1.0,  # 时间分辨率 1 ms
    sampling_rate=1000.0  # 采样率 1 kHz
)

# 计算所有指标
results = analyzer.compute_all()

# 打印摘要
analyzer.print_summary()

# 保存结果
analyzer.save_results('my_results.json')
```

---

## 📊 输出结果解读

### 结果文件格式（JSON）

```json
{
  "temporal": {
    "gamma_t": 1.024,
    "gamma_t_err": 0.087,
    "r_squared": 0.9234
  },
  "spatial": {
    "gamma_s": 2.187,
    "gamma_s_err": 0.156,
    "density": 0.0487,
    "clustering": 0.3421
  },
  "spatiotemporal": {
    "STC": 0.6234,
    "STC_pvalue": 0.0001
  },
  "avalanche": {
    "alpha": 1.512,
    "alpha_err": 0.098,
    "is_critical": true
  }
}
```

### 指标含义

| 指标 | 值范围 | 解释 |
|------|--------|------|
| **γ_t** | 0.5-1.5 | 时间复杂度 (≈1.0 = 临界态) |
| **γ_s** | 1-4 | 空间复杂度 (2.0-2.5 = 典型生物) |
| **STC** | 0-1 | 时空协同 (接近 1 = 强耦合) |
| **α** | 1-2 | 雪崩指数 (≈1.5 = 临界态) |

---

## 🔧 常见问题与调试

### Q1：数据格式不匹配
```python
# 如果 spike_times 是 NumPy 数组而非字典
spike_array = np.load('spike_times.npy')  # (N_neurons, T_max)

# 转换为字典格式
spike_dict = {}
for neuron_id in range(spike_array.shape[0]):
    spike_times = np.where(spike_array[neuron_id, :] > 0)[0]
    spike_dict[neuron_id] = spike_times * dt  # 转为毫秒
```

### Q2：计算时间太长
```python
# 只用前 100 个神经元和前 1000 秒数据
analyzer.spike_times = {k: v[v < 1000*1000] 
                         for k, v in list(analyzer.spike_times.items())[:100]}
analyzer.compute_all()
```

### Q3：结果不合理
```python
# 检查数据质量
def check_data_quality(analyzer):
    n_neurons = analyzer.adjacency_matrix.shape[0]
    n_spikes = sum(len(v) for v in analyzer.spike_times.values())
    duration = max(max(v) for v in analyzer.spike_times.values())
    
    avg_firing_rate = n_spikes / (n_neurons * duration / 1000)
    print(f"平均放电频率: {avg_firing_rate:.2f} Hz")
    
    if avg_firing_rate < 0.1:
        print("⚠️  警告：放电频率过低，结果可能不可靠")

check_data_quality(analyzer)
```

---

## 📈 可视化结果

```python
import matplotlib.pyplot as plt

def plot_complexity_results(results):
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 时间复杂度
    ax = axes[0, 0]
    f = results['temporal']['frequencies']
    pxx = results['temporal']['power_spectrum']
    ax.loglog(f, pxx, 'b-', linewidth=2)
    ax.set_xlabel('频率 (Hz)')
    ax.set_ylabel('功率')
    ax.set_title(f'时间复杂度 γ_t={results["temporal"]["gamma_t"]:.3f}')
    ax.grid(True, alpha=0.3)
    
    # 空间复杂度
    ax = axes[0, 1]
    ax.loglog(range(1, len(results['spatial']['avalanche_distribution'])+1),
              results['spatial']['avalanche_distribution'], 'go')
    ax.set_xlabel('度数')
    ax.set_ylabel('概率')
    ax.set_title(f'空间复杂度 γ_s={results["spatial"]["gamma_s"]:.3f}')
    ax.grid(True, alpha=0.3)
    
    # 时空耦合
    ax = axes[1, 0]
    im = ax.imshow(results['spatiotemporal']['temporal_correlation'], cmap='hot')
    ax.set_title(f'时空耦合 STC={results["spatiotemporal"]["STC"]:.3f}')
    plt.colorbar(im, ax=ax)
    
    # 雪崩分布
    ax = axes[1, 1]
    s_vals = range(1, len(results['avalanche']['avalanche_distribution'])+1)
    ax.loglog(s_vals, results['avalanche']['avalanche_distribution'], 'mo')
    ax.set_xlabel('雪崩大小')
    ax.set_ylabel('概率')
    ax.set_title(f'非线性放大 α={results["avalanche"]["alpha"]:.3f}')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('complexity_analysis.png', dpi=300)
    print("✓ 图已保存为 complexity_analysis.png")
    plt.show()

# 使用
import json
with open('results.json', 'r') as f:
    results = json.load(f)
plot_complexity_results(results)
```

---

## 🎯 典型应用案例

### 案例 1：对比多个物种

```python
species_list = ['elegans', 'larva', 'hemibrain', 'mouse']
results_all = {}

for species in species_list:
    analyzer = NeuralComplexityAnalyzer(f'~/data/{species}')
    results = analyzer.compute_all()
    results_all[species] = {
        'gamma_t': analyzer.results['temporal']['gamma_t'],
        'gamma_s': analyzer.results['spatial']['gamma_s'],
        'STC': analyzer.results['spatiotemporal']['STC'],
        'alpha': analyzer.results['avalanche']['alpha']
    }

# 比较表
import pandas as pd
df = pd.DataFrame(results_all).T
print(df)
```

### 案例 2：提取临界态标志

```python
def assess_criticality(analyzer):
    """评估系统是否处于临界态"""
    
    checks = {
        'temporal_critical': 0.9 <= analyzer.results['temporal']['gamma_t'] <= 1.1,
        'spatial_typical': 2.0 <= analyzer.results['spatial']['gamma_s'] <= 2.5,
        'coupling_strong': analyzer.results['spatiotemporal']['STC'] > 0.3,
        'avalanche_critical': 1.4 <= analyzer.results['avalanche']['alpha'] <= 1.6
    }
    
    criticality_score = sum(checks.values()) / len(checks)
    
    return {
        'checks': checks,
        'criticality_score': criticality_score,
        'is_critical': criticality_score >= 0.75
    }

assessment = assess_criticality(analyzer)
print(f"临界态评分: {assessment['criticality_score']:.1%}")
print(f"是否临界: {'✅ 是' if assessment['is_critical'] else '❌ 否'}")
```

---

## 📚 完整文档

详见：`/vault/research/Neural_Complexity_Computation.md`

包含：
- 数据格式详解
- 算法原理
- 高级配置
- 理论背景
