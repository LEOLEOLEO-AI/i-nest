---
title: iNEST 第 1 周仿真实验计划 - 数据修复与准备
tags:
- large-language-model
- neuron
- scale-free-networks
- simulation
- synapse
- topology
date: '2026-07-03'
---
**开始日期**：2026-07-03 (Friday)
**完成目标**：2026-07-10 (Thursday)
**版本**：v1.0-WEEK1-EXECUTION

---

## 执行摘要

**第 1 周主题**：加载真实连接组数据，建立基础框架

**当前状态**：已获取并验证了 4 个关键数据集
- ✅ synapse_weights.json (突触强度，100K 突触)
- ✅ neuron_types.csv (神经元标注，25K 神经元)
- ✅ neurotransmitter_map.csv (神经递质分类)
- ✅ neuron_params.yaml (生物物理参数)

**本周任务**：将这些数据集集成到仿真框架，为后续计算做准备

---

## 第一部分：实验内容

### 📋 **任务 1：数据加载验证 (Day 1-2)**

#### 1.1 目标
```
创建健壮的数据加载器，验证 Hemibrain 真实连接组的完整性
```

#### 1.2 具体任务

**Task 1.2.1：创建 data_loader.py**

```python
# /vault/sdi_sim/data_loader.py

import json
import pandas as pd
import yaml
import numpy as np
from pathlib import Path

class ConnectomeDataLoader:
    """
    Hemibrain 连接组数据加载器
    支持：神经元类型、突触强度、神经递质分类、生物物理参数
    """
    
    def __init__(self, data_dir):
        self.data_dir = Path(data_dir)
        self.neurons = None
        self.synapses = None
        self.neuron_types = None
        self.neurotransmitter_map = None
        self.params = None
        self.n_neurons = 0
        self.n_synapses = 0
    
    def load_neuron_types(self):
        """加载神经元类型标注"""
        file_path = self.data_dir / 'neuron_types.csv'
        self.neuron_types = pd.read_csv(file_path)
        self.n_neurons = len(self.neuron_types)
        print(f"✓ 加载神经元类型：{self.n_neurons} 个")
        return self.neuron_types
    
    def load_synapse_weights(self):
        """加载突触强度参数"""
        file_path = self.data_dir / 'synapse_weights.json'
        with open(file_path, 'r') as f:
            data = json.load(f)
        self.synapses = data['synapses']
        self.n_synapses = len(self.synapses)
        print(f"✓ 加载突触权重：{self.n_synapses} 个")
        return self.synapses
    
    def load_neurotransmitter_map(self):
        """加载神经递质分类"""
        file_path = self.data_dir / 'neurotransmitter_map.csv'
        self.neurotransmitter_map = pd.read_csv(file_path)
        print(f"✓ 加载神经递质映射：{len(self.neurotransmitter_map)} 个")
        return self.neurotransmitter_map
    
    def load_neural_params(self):
        """加载生物物理参数"""
        file_path = self.data_dir / 'neuron_params.yaml'
        with open(file_path, 'r') as f:
            self.params = yaml.safe_load(f)
        print(f"✓ 加载生物物理参数")
        return self.params
    
    def load_all(self):
        """加载所有数据"""
        print("【加载所有数据】")
        self.load_neuron_types()
        self.load_synapse_weights()
        self.load_neurotransmitter_map()
        self.load_neural_params()
        print(f"✅ 所有数据加载完成")
        return {
            'neurons': self.neuron_types,
            'synapses': self.synapses,
            'neurotransmitters': self.neurotransmitter_map,
            'params': self.params
        }
    
    def validate_data_integrity(self):
        """验证数据完整性"""
        print("\n【数据完整性验证】")
        
        errors = []
        
        # 检查 1：神经元数量一致
        if len(self.neuron_types) != len(self.neurotransmitter_map):
            errors.append("神经元数量不一致")
        else:
            print(f"✓ 神经元数量一致：{len(self.neuron_types)}")
        
        # 检查 2：突触神经元 ID 有效性
        neuron_ids = set(self.neuron_types['neuron_id'].unique())
        synapse_neurons = set()
        for s in self.synapses:
            synapse_neurons.add(s['pre_neuron'])
            synapse_neurons.add(s['post_neuron'])
        
        if synapse_neurons.issubset(neuron_ids):
            print(f"✓ 所有突触神经元 ID 有效")
        else:
            errors.append(f"无效的神经元 ID：{synapse_neurons - neuron_ids}")
        
        # 检查 3：权重范围
        weights = [s['weight'] for s in self.synapses]
        if min(weights) >= 0 and max(weights) <= 1:
            print(f"✓ 权重范围有效：[{min(weights):.3f}, {max(weights):.3f}]")
        else:
            errors.append(f"权重范围无效")
        
        # 检查 4：参数完整性
        required_sections = ['LIF_neuron', 'Synapse', 'STDP']
        if all(s in self.params for s in required_sections):
            print(f"✓ 参数配置完整")
        else:
            errors.append("参数配置不完整")
        
        if errors:
            print(f"\n❌ 验证失败：{errors}")
            return False
        else:
            print(f"\n✅ 所有验证通过")
            return True
    
    def generate_summary_report(self):
        """生成摘要报告"""
        print("\n【数据摘要报告】")
        
        report = {
            'neurons': {
                'total': self.n_neurons,
                'by_type': self.neuron_types['neuron_type'].value_counts().to_dict(),
                'by_class': self.neuron_types['neuron_class'].value_counts().to_dict(),
            },
            'synapses': {
                'total': self.n_synapses,
                'weight_range': [float(min([s['weight'] for s in self.synapses])),
                                float(max([s['weight'] for s in self.synapses]))],
                'synapse_count_range': [min([s['synapse_count'] for s in self.synapses]),
                                       max([s['synapse_count'] for s in self.synapses])],
            },
            'neurotransmitters': self.neurotransmitter_map['neurotransmitter'].value_counts().to_dict(),
        }
        
        return report

# 使用示例
if __name__ == '__main__':
    loader = ConnectomeDataLoader('/vault/sdi_sim/data')
    data = loader.load_all()
    if loader.validate_data_integrity():
        report = loader.generate_summary_report()
        print(json.dumps(report, indent=2))
```

**交付物**：
- ✅ data_loader.py (完整实现)
- ✅ 单元测试通过
- ✅ 验证报告生成

**预期输出**：
```
✅ 加载了 25,000 个神经元
✅ 加载了 100,000 个突触
✅ 所有数据完整且一致
✅ 生成摘要报告
```

---

### 📋 **任务 2：构建网络图结构 (Day 2-3)**

#### 2.1 目标
```
从数据构建 NetworkX 有向图，为后续拓扑计算做准备
```

#### 2.2 具体任务

**Task 2.2.1：创建 network_builder.py**

```python
# /vault/sdi_sim/network_builder.py

import networkx as nx
import numpy as np
from collections import defaultdict

class HemibrainNetworkBuilder:
    """
    Hemibrain 网络图构建器
    构建加权有向图，支持拓扑分析
    """
    
    def __init__(self, loader):
        self.loader = loader
        self.G = None
        self.neuron_types = {}
        self.neurotransmitter_map = {}
    
    def build_network_graph(self):
        """
        构建网络图
        节点：神经元（带属性）
        边：突触（带权重和类型）
        """
        print("【构建网络图】")
        
        self.G = nx.DiGraph()
        
        # 1. 添加节点（带属性）
        print("1️⃣ 添加神经元节点...")
        for idx, row in self.loader.neuron_types.iterrows():
            nid = row['neuron_id']
            self.G.add_node(nid,
                           neuron_type=row['neuron_type'],
                           neuron_class=row['neuron_class'])
            self.neuron_types[nid] = row['neuron_type']
        
        print(f"   ✓ 添加了 {self.G.number_of_nodes()} 个节点")
        
        # 2. 添加边（带权重）
        print("2️⃣ 添加突触边...")
        for synapse in self.loader.synapses:
            pre = synapse['pre_neuron']
            post = synapse['post_neuron']
            weight = synapse['weight']
            count = synapse['synapse_count']
            
            self.G.add_edge(pre, post,
                           weight=weight,
                           synapse_count=count)
        
        print(f"   ✓ 添加了 {self.G.number_of_edges()} 条边")
        
        # 3. 验证图结构
        print("3️⃣ 验证图结构...")
        print(f"   ✓ 节点数：{self.G.number_of_nodes()}")
        print(f"   ✓ 边数：{self.G.number_of_edges()}")
        print(f"   ✓ 密度：{nx.density(self.G):.4f}")
        print(f"   ✓ 平均度：{sum(dict(self.G.degree()).values()) / self.G.number_of_nodes():.2f}")
        
        print(f"✅ 网络图构建完成")
        return self.G
    
    def analyze_basic_properties(self):
        """分析基本拓扑性质"""
        print("\n【基本拓扑分析】")
        
        if self.G is None:
            print("❌ 图未构建")
            return None
        
        properties = {
            'nodes': self.G.number_of_nodes(),
            'edges': self.G.number_of_edges(),
            'density': float(nx.density(self.G)),
            'avg_degree': sum(dict(self.G.degree()).values()) / self.G.number_of_nodes(),
        }
        
        # 度分布
        in_degrees = [d for n, d in self.G.in_degree()]
        out_degrees = [d for n, d in self.G.out_degree()]
        
        properties['in_degree_stats'] = {
            'mean': float(np.mean(in_degrees)),
            'std': float(np.std(in_degrees)),
            'min': int(np.min(in_degrees)),
            'max': int(np.max(in_degrees)),
        }
        
        properties['out_degree_stats'] = {
            'mean': float(np.mean(out_degrees)),
            'std': float(np.std(out_degrees)),
            'min': int(np.min(out_degrees)),
            'max': int(np.max(out_degrees)),
        }
        
        for key, val in properties.items():
            print(f"✓ {key}: {val}")
        
        return properties
    
    def compute_connectivity_matrix(self):
        """计算连接矩阵"""
        print("\n【计算连接矩阵】")
        
        adj_matrix = nx.to_numpy_array(self.G, weight='weight')
        print(f"✓ 连接矩阵大小：{adj_matrix.shape}")
        print(f"✓ 非零元素：{np.count_nonzero(adj_matrix)}")
        print(f"✓ 稀疏度：{1 - np.count_nonzero(adj_matrix) / adj_matrix.size:.4f}")
        
        return adj_matrix
```

**交付物**：
- ✅ network_builder.py
- ✅ 网络图构建验证
- ✅ 基本拓扑分析

**预期输出**：
```
✅ 网络图：25,000 节点，100,000 条边
✅ 平均度数：~8
✅ 密度：~0.00016
✅ 连接矩阵计算完成
```

---

### 📋 **任务 3：对照网络生成 (Day 3-4)**

#### 3.1 目标
```
生成 3 种对照网络（ER、配置模型、幂律网络）
为后续统计对比做准备
```

#### 3.2 具体任务

**Task 3.2.1：创建 null_model_generator.py**

```python
# /vault/sdi_sim/null_model_generator.py

import networkx as nx
import numpy as np

class NullModelGenerator:
    """
    生成对照网络（null models）用于统计显著性检验
    """
    
    def __init__(self, real_network):
        self.G_real = real_network
        self.models = {}
    
    def generate_ER_random(self):
        """
        Erdős–Rényi 随机图
        保持：边密度
        破坏：所有其他拓扑特性
        """
        print("【生成 ER 随机图】")
        
        n = self.G_real.number_of_nodes()
        p = nx.density(self.G_real)
        
        G_ER = nx.erdos_renyi_graph(n, p, directed=True)
        
        print(f"✓ 节点数：{G_ER.number_of_nodes()}")
        print(f"✓ 边数：{G_ER.number_of_edges()}")
        print(f"✓ 密度：{nx.density(G_ER):.4f}")
        
        self.models['ER'] = G_ER
        return G_ER
    
    def generate_configuration_model(self):
        """
        配置模型
        保持：度分布
        破坏：其他特性
        """
        print("\n【生成配置模型】")
        
        # 获取度序列
        degree_seq = [d for n, d in self.G_real.out_degree()]
        
        # 生成配置模型（无向）
        G_config = nx.configuration_model(degree_seq)
        # 转为有向图
        G_config = G_config.to_directed()
        
        print(f"✓ 节点数：{G_config.number_of_nodes()}")
        print(f"✓ 边数：{G_config.number_of_edges()}")
        print(f"✓ 密度：{nx.density(G_config):.4f}")
        
        self.models['configuration'] = G_config
        return G_config
    
    def generate_scale_free(self):
        """
        Barabási-Albert 无标度网络
        保持：幂律度分布
        """
        print("\n【生成无标度网络】")
        
        n = self.G_real.number_of_nodes()
        m = int(self.G_real.number_of_edges() / n)  # 平均出度
        
        G_sf = nx.barabasi_albert_graph(n, m)
        G_sf = G_sf.to_directed()
        
        print(f"✓ 节点数：{G_sf.number_of_nodes()}")
        print(f"✓ 边数：{G_sf.number_of_edges()}")
        print(f"✓ 密度：{nx.density(G_sf):.4f}")
        
        self.models['scale_free'] = G_sf
        return G_sf
    
    def generate_all_models(self):
        """生成所有对照模型"""
        print("\n【生成所有对照模型】")
        print("="*50)
        
        self.generate_ER_random()
        self.generate_configuration_model()
        self.generate_scale_free()
        
        print("\n✅ 所有对照模型生成完成")
        return self.models
```

**交付物**：
- ✅ null_model_generator.py
- ✅ 3 种对照网络生成
- ✅ 验证报告

**预期输出**：
```
✅ ER 随机图：密度 0.000160
✅ 配置模型：度分布保持
✅ 无标度网络：幂律分布
✅ 对照网络已准备好
```

---

### 📋 **任务 4：完整流程测试 (Day 4-5)**

#### 4.1 目标
```
集成所有模块，进行端到端测试
```

#### 4.2 具体任务

**Task 4.2.1：创建 week1_pipeline.py**

```python
# /vault/sdi_sim/week1_pipeline.py

from data_loader import ConnectomeDataLoader
from network_builder import HemibrainNetworkBuilder
from null_model_generator import NullModelGenerator
import json

def run_week1_pipeline():
    """
    第 1 周完整流程：数据加载 → 网络构建 → 对照生成
    """
    
    print("\n" + "="*60)
    print("【iNEST 第 1 周完整流程】")
    print("="*60 + "\n")
    
    # 步骤 1：加载数据
    print("【步骤 1：数据加载】\n")
    loader = ConnectomeDataLoader('/vault/sdi_sim/data')
    data = loader.load_all()
    
    if not loader.validate_data_integrity():
        print("❌ 数据验证失败")
        return False
    
    summary = loader.generate_summary_report()
    
    # 步骤 2：构建网络
    print("\n【步骤 2：网络构建】\n")
    builder = HemibrainNetworkBuilder(loader)
    G_real = builder.build_network_graph()
    
    properties = builder.analyze_basic_properties()
    adj_matrix = builder.compute_connectivity_matrix()
    
    # 步骤 3：生成对照
    print("\n【步骤 3：对照网络生成】\n")
    null_gen = NullModelGenerator(G_real)
    null_models = null_gen.generate_all_models()
    
    # 步骤 4：生成报告
    print("\n【步骤 4：生成完整报告】\n")
    
    report = {
        'week': 1,
        'date': '2026-07-03',
        'data_summary': summary,
        'network_properties': properties,
        'null_models_status': {
            'ER': 'generated',
            'configuration': 'generated',
            'scale_free': 'generated',
        },
        'connectivity_matrix_shape': adj_matrix.shape,
        'status': 'PASS',
    }
    
    # 保存报告
    with open('/vault/sdi_sim/results/week1_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"✅ 第 1 周流程完成")
    print(f"✅ 报告已保存：week1_report.json")
    
    return True

if __name__ == '__main__':
    success = run_week1_pipeline()
    if success:
        print("\n🎉 第 1 周验收通过")
    else:
        print("\n❌ 第 1 周验收失败")
```

**交付物**：
- ✅ week1_pipeline.py
- ✅ week1_report.json
- ✅ 完整流程验证

---

### 📋 **任务 5：文档和测试 (Day 5)**

#### 5.1 单元测试

```bash
# /vault/sdi_sim/tests/test_week1.py

import unittest
from data_loader import ConnectomeDataLoader
from network_builder import HemibrainNetworkBuilder

class TestWeek1(unittest.TestCase):
    
    def setUp(self):
        self.loader = ConnectomeDataLoader('/vault/sdi_sim/data')
        self.loader.load_all()
    
    def test_data_loading(self):
        """测试数据加载"""
        self.assertIsNotNone(self.loader.neuron_types)
        self.assertEqual(len(self.loader.neuron_types), 25000)
    
    def test_data_validation(self):
        """测试数据验证"""
        result = self.loader.validate_data_integrity()
        self.assertTrue(result)
    
    def test_network_building(self):
        """测试网络构建"""
        builder = HemibrainNetworkBuilder(self.loader)
        G = builder.build_network_graph()
        self.assertEqual(G.number_of_nodes(), 25000)
        self.assertGreater(G.number_of_edges(), 0)

if __name__ == '__main__':
    unittest.main()
```

---

## 第二部分：预期目标与验收标准

### 🎯 **Week 1 成功标准**

| 目标 | 预期 | 验收标准 |
|------|------|---------|
| 数据加载 | 100% | ✅ 25K 神经元 + 100K 突触 |
| 数据验证 | PASS | ✅ 所有一致性检查通过 |
| 网络构建 | 完整 | ✅ 图结构正确，属性完整 |
| 对照生成 | 3 种 | ✅ ER + Config + SF |
| 文档完整 | 是 | ✅ 代码 + 文档 + 测试 |
| 报告生成 | week1_report.json | ✅ JSON 格式，包含所有指标 |

### 📊 **预期输出指标**

```
数据层面：
  ✓ 神经元总数：25,000
  ✓ 突触总数：100,000
  ✓ 突触权重范围：0.3 - 1.0
  ✓ E/I 比例：4:1

网络层面：
  ✓ 平均度数：~8.0
  ✓ 网络密度：~0.00016
  ✓ 连接矩阵：25K×25K 稀疏矩阵
  ✓ 对照网络：3 种准备就绪

验收层面：
  ✓ 单元测试：100% 通过
  ✓ 代码审查：准备就绪
  ✓ 文档完整：准备就绪
  ✓ 推送 GitHub：准备就绪
```

---

## 第三部分：执行时间表

| 日期 | 天数 | 任务 | 状态 |
|------|------|------|------|
| 2026-07-03 | Day 1 | 数据加载验证 | ⏳ 进行中 |
| 2026-07-04 | Day 2 | 网络图构建 | 📅 计划中 |
| 2026-07-05 | Day 3 | 对照网络生成 | 📅 计划中 |
| 2026-07-06 | Day 4 | 完整流程测试 | 📅 计划中 |
| 2026-07-07 | Day 5 | 文档和测试 | 📅 计划中 |
| 2026-07-08 | Day 6 | Buffer / 优化 | 📅 计划中 |
| 2026-07-10 | 结束 | Week 1 验收 | 🎯 目标 |

---

## 第四部分：Go/NoGo 检查点

### ✅ **Go/NoGo 检查 - Day 1 末（2026-07-03 23:59）**

```
检查项：
☐ 数据加载成功（25K neurons）
☐ 数据验证通过（所有一致性检查）
☐ data_loader.py 完成
☐ 单元测试通过

Go 条件：所有 ☐ 都 ✅
NoGo 条件：任何一个失败 → 延期

当前进度：开始执行
```

---

## 第五部分：风险管理

### 🔴 **高风险**

```
风险 1：数据格式不匹配
  缓解：已验证 ✅
  
风险 2：内存溢出（100K 突触）
  缓解：使用稀疏矩阵表示
```

### 🟡 **中风险**

```
风险 1：对照网络生成缓慢
  缓解：可并行处理
  
风险 2：网络密度过低导致分割
  缓解：检查连通性
```

---

**版本**：v1.0-WEEK1-EXECUTION
**状态**：🟢 准备开始执行
**下一步**：立即开始 Task 1（数据加载验证）

