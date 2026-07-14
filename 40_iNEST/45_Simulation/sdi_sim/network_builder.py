"""
Hemibrain 网络图构建器
构建加权有向图，支持拓扑分析
"""

import networkx as nx
import numpy as np
from collections import defaultdict

class HemibrainNetworkBuilder:
    def __init__(self, loader):
        self.loader = loader
        self.G = None
        self.neuron_types = {}
        self.neurotransmitter_map = {}
    
    def build_network_graph(self):
        """构建网络图"""
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
        edge_count = 0
        for synapse in self.loader.synapses:
            pre = synapse['pre_neuron']
            post = synapse['post_neuron']
            weight = synapse['weight']
            count = synapse['synapse_count']
            
            self.G.add_edge(pre, post,
                           weight=weight,
                           synapse_count=count)
            edge_count += 1
            
            if edge_count % 20000 == 0:
                print(f"   处理中... {edge_count}/{len(self.loader.synapses)}")
        
        print(f"   ✓ 添加了 {self.G.number_of_edges()} 条边")
        
        # 3. 验证图结构
        print("3️⃣ 验证图结构...")
        print(f"   ✓ 节点数：{self.G.number_of_nodes()}")
        print(f"   ✓ 边数：{self.G.number_of_edges()}")
        print(f"   ✓ 密度：{nx.density(self.G):.6f}")
        avg_degree = sum(dict(self.G.degree()).values()) / self.G.number_of_nodes()
        print(f"   ✓ 平均度：{avg_degree:.2f}")
        
        print(f"✅ 网络图构建完成\n")
        return self.G
    
    def analyze_basic_properties(self):
        """分析基本拓扑性质"""
        print("【基本拓扑分析】")
        
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
        
        print()
        return properties
    
    def compute_connectivity_matrix(self):
        """计算连接矩阵"""
        print("【计算连接矩阵】")
        
        adj_matrix = nx.to_numpy_array(self.G, weight='weight')
        print(f"✓ 连接矩阵大小：{adj_matrix.shape}")
        print(f"✓ 非零元素：{np.count_nonzero(adj_matrix)}")
        sparsity = 1 - np.count_nonzero(adj_matrix) / adj_matrix.size
        print(f"✓ 稀疏度：{sparsity:.4f}")
        print()
        
        return adj_matrix
