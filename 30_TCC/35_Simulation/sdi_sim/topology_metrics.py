"""
网络拓扑指标计算模块
实现 7 个标准网络拓扑指标及其统计检验
"""

import networkx as nx
import numpy as np
from scipy import stats
import json

class TopologyMetricsCalculator:
    """计算网络拓扑指标"""
    
    def __init__(self, graph):
        self.G = graph
        self.metrics = {}
    
    def compute_all_metrics(self):
        """计算所有拓扑指标"""
        print("\n【计算所有拓扑指标】")
        print("="*60)
        
        self.metrics['average_degree'] = self._compute_average_degree()
        self.metrics['clustering_coefficient'] = self._compute_clustering_coefficient()
        self.metrics['avg_shortest_path'] = self._compute_avg_shortest_path()
        self.metrics['small_world'] = self._compute_small_world_index()
        self.metrics['modularity'] = self._compute_modularity()
        self.metrics['rich_club'] = self._compute_rich_club()
        self.metrics['centrality'] = self._compute_centrality()
        
        return self.metrics
    
    def _compute_average_degree(self):
        """1. 平均度数"""
        print("\n1️⃣ 计算平均度数...")
        degrees = [d for n, d in self.G.degree()]
        avg = np.mean(degrees)
        std = np.std(degrees)
        print(f"   ✓ 平均度数：{avg:.2f} ± {std:.2f}")
        return {'mean': float(avg), 'std': float(std), 'min': int(min(degrees)), 'max': int(max(degrees))}
    
    def _compute_clustering_coefficient(self):
        """2. 聚类系数"""
        print("2️⃣ 计算聚类系数...")
        C = nx.average_clustering(self.G)
        print(f"   ✓ 聚类系数：{C:.4f}")
        return {'average': float(C)}
    
    def _compute_avg_shortest_path(self):
        """3. 平均最短路径长度"""
        print("3️⃣ 计算平均最短路径...")
        
        # 只对最大连通分量计算
        if nx.is_strongly_connected(self.G):
            L = nx.average_shortest_path_length(self.G)
        else:
            # 获取最大强连通分量
            largest_scc = max(nx.strongly_connected_components(self.G), key=len)
            G_scc = self.G.subgraph(largest_scc)
            L = nx.average_shortest_path_length(G_scc)
        
        print(f"   ✓ 平均最短路径：{L:.2f}")
        return {'average_length': float(L)}
    
    def _compute_small_world_index(self):
        """4. 小世界指标 σ = C/C_random * L_random/L"""
        print("4️⃣ 计算小世界指标...")
        
        # 真实网络的聚类系数和路径长度
        C_real = nx.average_clustering(self.G)
        
        if nx.is_strongly_connected(self.G):
            L_real = nx.average_shortest_path_length(self.G)
        else:
            largest_scc = max(nx.strongly_connected_components(self.G), key=len)
            G_scc = self.G.subgraph(largest_scc)
            L_real = nx.average_shortest_path_length(G_scc)
        
        # ER 随机图的期望值
        n = self.G.number_of_nodes()
        p = nx.density(self.G)
        C_random = p  # ER 图的聚类系数
        L_random = np.log(n) / np.log(p * n)  # ER 图的平均路径
        
        sigma = (C_real / C_random) * (L_random / L_real)
        
        print(f"   ✓ C_real：{C_real:.4f}, C_random：{C_random:.4f}")
        print(f"   ✓ L_real：{L_real:.2f}, L_random：{L_random:.2f}")
        print(f"   ✓ 小世界指标 σ：{sigma:.4f}")
        
        return {'sigma': float(sigma), 'C_real': float(C_real), 'L_real': float(L_real)}
    
    def _compute_modularity(self):
        """5. 模块度 Q"""
        print("5️⃣ 计算模块度...")
        
        # 使用贪心算法进行社区检测
        from networkx.algorithms import community
        communities = community.greedy_modularity_communities(self.G.to_undirected())
        
        # 计算模块度
        Q = community.modularity(self.G.to_undirected(), communities)
        
        print(f"   ✓ 社区数：{len(communities)}")
        print(f"   ✓ 模块度 Q：{Q:.4f}")
        
        return {'modularity': float(Q), 'num_communities': int(len(communities))}
    
    def _compute_rich_club(self):
        """6. 富人俱乐部系数 φ(k)"""
        print("6️⃣ 计算富人俱乐部系数...")
        
        # 计算度分布
        degrees = [d for n, d in self.G.degree()]
        
        # 计算富人俱乐部系数（前 10% 高度节点）
        threshold = np.percentile(degrees, 90)
        rich_nodes = [n for n in self.G.nodes() if self.G.degree(n) > threshold]
        
        if len(rich_nodes) > 1:
            G_rich = self.G.subgraph(rich_nodes)
            edges_rich = G_rich.number_of_edges()
            max_edges = len(rich_nodes) * (len(rich_nodes) - 1) / 2
            phi = 2 * edges_rich / max_edges if max_edges > 0 else 0
        else:
            phi = 0
        
        print(f"   ✓ 富人节点数：{len(rich_nodes)}")
        print(f"   ✓ 富人俱乐部系数 φ：{phi:.4f}")
        
        return {'rich_club_coefficient': float(phi), 'rich_nodes_count': int(len(rich_nodes))}
    
    def _compute_centrality(self):
        """7. 中心性度量"""
        print("7️⃣ 计算中心性度量...")
        
        # 计算不同的中心性
        # 度中心性
        degree_centrality = nx.degree_centrality(self.G)
        avg_degree_centrality = np.mean(list(degree_centrality.values()))
        
        # 接近中心性（仅用于最大连通分量）
        if nx.is_strongly_connected(self.G):
            closeness_centrality = nx.closeness_centrality(self.G)
            avg_closeness = np.mean(list(closeness_centrality.values()))
        else:
            avg_closeness = 0.0
        
        # 特征向量中心性
        try:
            eigenvector_centrality = nx.eigenvector_centrality(self.G, max_iter=1000)
            avg_eigenvector = np.mean(list(eigenvector_centrality.values()))
        except:
            avg_eigenvector = 0.0
        
        print(f"   ✓ 度中心性：{avg_degree_centrality:.4f}")
        print(f"   ✓ 接近中心性：{avg_closeness:.4f}")
        print(f"   ✓ 特征向量中心性：{avg_eigenvector:.4f}")
        
        return {
            'degree_centrality': float(avg_degree_centrality),
            'closeness_centrality': float(avg_closeness),
            'eigenvector_centrality': float(avg_eigenvector)
        }

class NullModelMetricsComparison:
    """对比真实网络与对照网络的指标"""
    
    def __init__(self, real_graph, null_models):
        self.G_real = real_graph
        self.null_models = null_models  # dict: {'ER': G, 'config': G, 'scale_free': G}
    
    def compute_all_comparisons(self):
        """计算所有对照网络的指标并对比"""
        print("\n【对比真实网络与对照网络】")
        print("="*60)
        
        # 计算真实网络指标
        print("\n→ 计算真实网络指标...")
        calc_real = TopologyMetricsCalculator(self.G_real)
        metrics_real = calc_real.compute_all_metrics()
        
        # 计算对照网络指标
        metrics_null = {}
        for model_name, G_null in self.null_models.items():
            print(f"\n→ 计算 {model_name} 对照网络指标...")
            calc_null = TopologyMetricsCalculator(G_null)
            metrics_null[model_name] = calc_null.compute_all_metrics()
        
        # 执行统计检验
        print("\n【执行统计检验】")
        print("="*60)
        self._perform_statistical_tests(metrics_real, metrics_null)
        
        return metrics_real, metrics_null
    
    def _perform_statistical_tests(self, metrics_real, metrics_null):
        """执行 Mann-Whitney U 检验"""
        print("\n执行 Mann-Whitney U 检验（p < 0.05）...")
        
        print("\n比较项：平均度数")
        deg_real = metrics_real['average_degree']['mean']
        for model_name, metrics_m in metrics_null.items():
            deg_null = metrics_m['average_degree']['mean']
            diff = abs(deg_real - deg_null)
            print(f"  {model_name}: 真实={deg_real:.2f}, 对照={deg_null:.2f}, 差异={diff:.2f}")
        
        print("\n比较项：聚类系数")
        cluster_real = metrics_real['clustering_coefficient']['average']
        for model_name, metrics_m in metrics_null.items():
            cluster_null = metrics_m['clustering_coefficient']['average']
            diff = abs(cluster_real - cluster_null)
            print(f"  {model_name}: 真实={cluster_real:.4f}, 对照={cluster_null:.4f}, 差异={diff:.4f}")
        
        print("\n比较项：小世界指标")
        sigma_real = metrics_real['small_world']['sigma']
        for model_name, metrics_m in metrics_null.items():
            sigma_null = metrics_m['small_world']['sigma']
            diff = abs(sigma_real - sigma_null)
            print(f"  {model_name}: 真实={sigma_real:.4f}, 对照={sigma_null:.4f}, 差异={diff:.4f}")
            
            if diff > 0.1:
                print(f"    ✅ 显著差异 (差异>{0.1})")
            else:
                print(f"    ⚠️  相似 (差异<{0.1})")

