"""
轻量级版本 - 跳过复杂计算，先展示结果
"""

from data_loader import ConnectomeDataLoader
from network_builder import HemibrainNetworkBuilder
import numpy as np
import networkx as nx
import json
import os

def run_w23_fast():
    print("\n" + "="*60)
    print("【W2-3 快速验证版本 - 基础指标】")
    print("="*60 + "\n")
    
    # 加载和构建
    loader = ConnectomeDataLoader('./data')
    data = loader.load_all()
    
    builder = HemibrainNetworkBuilder(loader)
    G = builder.build_network_graph()
    
    # 快速计算可行的指标
    print("【快速计算基础指标】\n")
    
    # 1. 度数
    degrees = [d for n, d in G.degree()]
    print(f"1️⃣ 平均度数：{np.mean(degrees):.2f} ± {np.std(degrees):.2f}")
    
    # 2. 聚类系数
    C = nx.average_clustering(G)
    print(f"2️⃣ 聚类系数：{C:.4f}")
    
    # 3. 密度和连通性
    print(f"3️⃣ 网络密度：{nx.density(G):.6f}")
    print(f"4️⃣ 强连通分量数：{nx.number_strongly_connected_components(G)}")
    
    # 4. 度分布
    in_degrees = [d for n, d in G.in_degree()]
    out_degrees = [d for n, d in G.out_degree()]
    print(f"5️⃣ 入度分布：平均 {np.mean(in_degrees):.2f}，最大 {max(in_degrees)}")
    print(f"6️⃣ 出度分布：平均 {np.mean(out_degrees):.2f}，最大 {max(out_degrees)}")
    
    # 5. 度中心性
    degree_centrality = nx.degree_centrality(G)
    print(f"7️⃣ 度中心性：{np.mean(list(degree_centrality.values())):.4f}")
    
    # 保存快速报告
    report = {
        'weeks': '2-3',
        'version': 'fast_validation',
        'metrics': {
            'average_degree': float(np.mean(degrees)),
            'clustering_coefficient': float(C),
            'density': float(nx.density(G)),
            'in_degree_mean': float(np.mean(in_degrees)),
            'out_degree_mean': float(np.mean(out_degrees)),
            'out_degree_max': int(max(out_degrees)),
        },
        'status': 'IN_PROGRESS'
    }
    
    os.makedirs('results', exist_ok=True)
    with open('results/w23_topology_fast.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n✅ 快速验证完成")
    print(f"✓ 报告已保存：results/w23_topology_fast.json")

if __name__ == '__main__':
    run_w23_fast()
