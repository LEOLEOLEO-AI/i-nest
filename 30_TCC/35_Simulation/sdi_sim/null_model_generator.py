"""
生成对照网络（null models）用于统计显著性检验
"""

import networkx as nx
import numpy as np

class NullModelGenerator:
    def __init__(self, real_network):
        self.G_real = real_network
        self.models = {}
    
    def generate_ER_random(self):
        """Erdős–Rényi 随机图"""
        print("【生成 ER 随机图】")
        
        n = self.G_real.number_of_nodes()
        p = nx.density(self.G_real)
        
        G_ER = nx.erdos_renyi_graph(n, p, directed=True)
        
        print(f"✓ 节点数：{G_ER.number_of_nodes()}")
        print(f"✓ 边数：{G_ER.number_of_edges()}")
        print(f"✓ 密度：{nx.density(G_ER):.6f}")
        print()
        
        self.models['ER'] = G_ER
        return G_ER
    
    def generate_configuration_model(self):
        """配置模型"""
        print("【生成配置模型】")
        
        degree_seq = [d for n, d in self.G_real.out_degree()]
        G_config = nx.configuration_model(degree_seq)
        G_config = G_config.to_directed()
        
        print(f"✓ 节点数：{G_config.number_of_nodes()}")
        print(f"✓ 边数：{G_config.number_of_edges()}")
        print(f"✓ 密度：{nx.density(G_config):.6f}")
        print()
        
        self.models['configuration'] = G_config
        return G_config
    
    def generate_scale_free(self):
        """Barabási-Albert 无标度网络"""
        print("【生成无标度网络】")
        
        n = self.G_real.number_of_nodes()
        m = max(1, int(self.G_real.number_of_edges() / n))
        
        G_sf = nx.barabasi_albert_graph(n, m)
        G_sf = G_sf.to_directed()
        
        print(f"✓ 节点数：{G_sf.number_of_nodes()}")
        print(f"✓ 边数：{G_sf.number_of_edges()}")
        print(f"✓ 密度：{nx.density(G_sf):.6f}")
        print()
        
        self.models['scale_free'] = G_sf
        return G_sf
    
    def generate_all_models(self):
        """生成所有对照模型"""
        print("【生成所有对照模型】")
        print("="*50)
        print()
        
        self.generate_ER_random()
        self.generate_configuration_model()
        self.generate_scale_free()
        
        print("✅ 所有对照模型生成完成\n")
        return self.models
