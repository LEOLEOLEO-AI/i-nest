#!/usr/bin/env python3
"""
生物神经网络复杂度计算工具
从 Codex 获取的数据直接计算 4 大复杂度指标

使用方法：
    python neural_complexity.py --data_path /path/to/codex/data --species elegans
"""

import numpy as np
import pandas as pd
from scipy import signal, stats
from scipy.fft import fft, fftfreq
import networkx as nx
import pickle
import json
from pathlib import Path
from typing import Dict, Tuple, List
import argparse
import warnings
warnings.filterwarnings('ignore')


class NeuralComplexityAnalyzer:
    """神经网络复杂度分析器"""
    
    def __init__(self, data_path: str, dt: float = 1.0, sampling_rate: float = 1000.0):
        """
        初始化分析器
        
        Parameters:
        -----------
        data_path : str
            Codex 数据所在目录
        dt : float
            时间分辨率 (ms)
        sampling_rate : float
            记录采样率 (Hz)
        """
        self.data_path = Path(data_path)
        self.dt = dt
        self.sampling_rate = sampling_rate
        
        # 加载数据
        self.adjacency_matrix = self._load_connectome()
        self.spike_times = self._load_spike_times()
        self.neuron_positions = self._load_positions()
        self.membrane_potential = self._load_membrane_potential()
        
        # 结果存储
        self.results = {}
        
        print(f"✓ 数据加载完成")
        print(f"  - 神经元数: {self.adjacency_matrix.shape[0]}")
        print(f"  - 突触数: {np.sum(self.adjacency_matrix > 0)}")
        print(f"  - 放电数据点: {len(self.spike_times)}")
    
    def _load_connectome(self) -> np.ndarray:
        """加载连接矩阵"""
        candidates = list(self.data_path.glob('*connectome*')) + \
                    list(self.data_path.glob('*adjacency*'))
        
        if not candidates:
            print("⚠️  未找到连接矩阵文件")
            return np.random.binomial(1, 0.05, (100, 100))
        
        path = candidates[0]
        if path.suffix == '.npy':
            return np.load(path)
        elif path.suffix in ['.csv', '.txt']:
            return np.loadtxt(path)
        else:
            return np.load(path)
    
    def _load_spike_times(self) -> Dict[int, np.ndarray]:
        """加载放电时间"""
        spike_files = list(self.data_path.glob('*spike*')) + \
                     list(self.data_path.glob('*spikes*'))
        
        if not spike_files:
            print("⚠️  未找到放电数据文件")
            return {i: np.sort(np.random.rand(100) * 1000) 
                    for i in range(self.adjacency_matrix.shape[0])}
        
        path = spike_files[0]
        if path.suffix == '.pkl':
            with open(path, 'rb') as f:
                return pickle.load(f)
        elif path.suffix == '.npy':
            data = np.load(path, allow_pickle=True).item()
            return data if isinstance(data, dict) else \
                   {i: data[i] for i in range(len(data))}
        elif path.suffix == '.csv':
            df = pd.read_csv(path)
            return {col: df[col].dropna().values for col in df.columns}
        else:
            return {}
    
    def _load_positions(self) -> np.ndarray:
        """加载神经元空间坐标"""
        pos_files = list(self.data_path.glob('*position*')) + \
                   list(self.data_path.glob('*coord*'))
        
        if not pos_files:
            # 生成随机位置
            n_neurons = self.adjacency_matrix.shape[0]
            return np.random.rand(n_neurons, 3) * 100
        
        path = pos_files[0]
        if path.suffix == '.npy':
            return np.load(path)
        elif path.suffix == '.csv':
            return np.loadtxt(path, delimiter=',')
        else:
            return np.load(path)
    
    def _load_membrane_potential(self) -> np.ndarray:
        """加载膜电位"""
        vm_files = list(self.data_path.glob('*membrane*')) + \
                  list(self.data_path.glob('*voltage*'))
        
        if not vm_files:
            return None
        
        path = vm_files[0]
        if path.suffix == '.npy':
            return np.load(path)
        else:
            return None
    
    # ========== 4 大复杂度计算 ==========
    
    def compute_temporal_complexity(self) -> Dict:
        """计算时间复杂度 γ_t"""
        print("\n[1/4] 计算时间复杂度...")
        
        # 转为二进制活动矩阵
        spike_times_list = list(self.spike_times.values())
        T_max = max(max(times) for times in spike_times_list)
        n_neurons = len(self.spike_times)
        n_bins = int(T_max / self.dt)
        
        activity = np.zeros((n_neurons, n_bins))
        for neuron_id, times in self.spike_times.items():
            for t in times:
                idx = int(t / self.dt)
                if idx < n_bins:
                    activity[int(neuron_id), idx] = 1
        
        # 计算功率谱
        pxx_all = []
        for neuron_id in range(n_neurons):
            f, pxx = signal.welch(
                activity[neuron_id, :],
                fs=self.sampling_rate / self.dt,
                window='hann',
                nperseg=min(1024, n_bins // 4)
            )
            pxx_all.append(pxx)
        
        pxx_mean = np.mean(pxx_all, axis=0)
        
        # 功率律拟合 (1-100 Hz)
        mask = (f >= 1) & (f <= 100)
        f_band = f[mask]
        pxx_band = pxx_mean[mask]
        
        logf = np.log10(f_band[f_band > 0])
        logP = np.log10(pxx_band[pxx_band > 0])
        
        coeffs = np.polyfit(logf, logP, 1)
        gamma_t = -coeffs[0]
        r_squared = np.corrcoef(logf, logP)[0, 1] ** 2
        
        result = {
            'gamma_t': gamma_t,
            'gamma_t_err': np.sqrt(1 - r_squared),
            'r_squared': r_squared,
            'frequencies': f,
            'power_spectrum': pxx_mean
        }
        
        print(f"  ✓ γ_t = {gamma_t:.3f} ± {result['gamma_t_err']:.3f} (R² = {r_squared:.4f})")
        self.results['temporal'] = result
        return result
    
    def compute_spatial_complexity(self) -> Dict:
        """计算空间复杂度 γ_s"""
        print("[2/4] 计算空间复杂度...")
        
        G = nx.DiGraph(self.adjacency_matrix)
        
        # 计算出度
        out_degrees = dict(G.out_degree(weight='weight'))
        degree_sequence = np.array([d for d in out_degrees.values() if d > 0])
        
        # 度分布
        k_values = np.unique(degree_sequence)
        k_counts = np.bincount(degree_sequence)
        p_k = k_counts[k_counts > 0] / len(degree_sequence)
        
        # 功率律拟合
        logk = np.log10(k_values[k_values > 0])
        logp = np.log10(p_k[p_k > 0])
        
        coeffs = np.polyfit(logk, logp, 1)
        gamma_s = -coeffs[0]
        r_squared = np.corrcoef(logk, logp)[0, 1] ** 2
        
        # 拓扑指标
        n_neurons = self.adjacency_matrix.shape[0]
        density = np.sum(self.adjacency_matrix > 0) / (n_neurons * (n_neurons - 1))
        try:
            clustering = nx.average_clustering(nx.Graph(self.adjacency_matrix))
            G_undirected = nx.Graph(self.adjacency_matrix)
            if nx.is_connected(G_undirected):
                avg_path = nx.average_shortest_path_length(G_undirected)
            else:
                avg_path = np.nan
        except:
            clustering = 0
            avg_path = np.nan
        
        result = {
            'gamma_s': gamma_s,
            'gamma_s_err': np.sqrt(1 - r_squared),
            'r_squared': r_squared,
            'degree_sequence': degree_sequence,
            'density': density,
            'clustering': clustering,
            'avg_path_length': avg_path
        }
        
        print(f"  ✓ γ_s = {gamma_s:.3f} ± {result['gamma_s_err']:.3f}")
        print(f"    密度 = {density:.4f}, 聚类系数 = {clustering:.4f}")
        self.results['spatial'] = result
        return result
    
    def compute_spatiotemporal_coupling(self) -> Dict:
        """计算时空协同系数"""
        print("[3/4] 计算时空协同系数...")
        
        # 转为二进制活动矩阵
        spike_times_list = list(self.spike_times.values())
        T_max = max(max(times) for times in spike_times_list)
        n_neurons = len(self.spike_times)
        n_bins = int(T_max / self.dt)
        
        activity = np.zeros((n_neurons, n_bins))
        for neuron_id, times in self.spike_times.items():
            for t in times:
                idx = int(t / self.dt)
                if idx < n_bins:
                    activity[int(neuron_id), idx] = 1
        
        # 计算互相关
        temporal_correlation = np.zeros((n_neurons, n_neurons))
        for i in range(min(n_neurons, 50)):  # 限制计算量
            for j in range(i + 1, min(n_neurons, 50)):
                if np.std(activity[i, :]) > 0 and np.std(activity[j, :]) > 0:
                    corr_ij = signal.correlate(activity[i, :], activity[j, :], mode='same')
                    max_corr = np.max(np.abs(corr_ij)) / (np.std(activity[i, :]) * np.std(activity[j, :]))
                    temporal_correlation[i, j] = min(max_corr, 1.0)
                    temporal_correlation[j, i] = min(max_corr, 1.0)
        
        # 计算空间距离
        spatial_distance = np.zeros((n_neurons, n_neurons))
        for i in range(n_neurons):
            for j in range(i + 1, n_neurons):
                dist = np.linalg.norm(self.neuron_positions[i] - self.neuron_positions[j])
                spatial_distance[i, j] = dist
                spatial_distance[j, i] = dist
        
        # 时空耦合
        dist_vec = spatial_distance[np.triu_indices_from(spatial_distance, k=1)]
        corr_vec = temporal_correlation[np.triu_indices_from(temporal_correlation, k=1)]
        
        rho, p_value = stats.spearmanr(-dist_vec[dist_vec > 0], corr_vec[dist_vec > 0])
        STC = max(0, rho)
        
        result = {
            'STC': STC,
            'STC_pvalue': p_value,
            'temporal_correlation': temporal_correlation,
            'spatial_distance': spatial_distance
        }
        
        print(f"  ✓ STC = {STC:.3f} (p = {p_value:.4f})")
        self.results['spatiotemporal'] = result
        return result
    
    def compute_nonlinear_amplification_alpha(self) -> Dict:
        """计算非线性放大指数"""
        print("[4/4] 计算非线性放大指数...")
        
        # 构造放电序列
        all_spikes = []
        for times in self.spike_times.values():
            all_spikes.extend(times)
        all_spikes = np.sort(np.array(all_spikes))
        
        # 离散化 + 计数
        bin_size = 5  # ms
        T_min, T_max = all_spikes.min(), all_spikes.max()
        n_bins = int((T_max - T_min) / bin_size) + 1
        spike_counts = np.zeros(n_bins)
        
        for t in all_spikes:
            idx = int((t - T_min) / bin_size)
            if idx < n_bins:
                spike_counts[idx] += 1
        
        # 识别雪崩
        threshold = 1
        active_bins = spike_counts > threshold
        
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
        
        # 功率律拟合
        s_values = np.unique(avalanche_sizes)
        s_counts = np.bincount(avalanche_sizes)
        p_s = s_counts[s_counts > 0] / len(avalanche_sizes)
        
        logs = np.log10(s_values[s_values > 0])
        logp = np.log10(p_s[p_s > 0])
        
        coeffs = np.polyfit(logs, logp, 1)
        alpha = -coeffs[0]
        r_squared = np.corrcoef(logs, logp)[0, 1] ** 2
        
        result = {
            'alpha': alpha,
            'alpha_err': np.sqrt(1 - r_squared),
            'r_squared': r_squared,
            'avalanche_sizes': avalanche_sizes,
            'avalanche_distribution': p_s,
            'is_critical': 1.4 <= alpha <= 1.6
        }
        
        print(f"  ✓ α = {alpha:.3f} ± {result['alpha_err']:.3f}")
        print(f"    临界态: {'是' if result['is_critical'] else '否'}")
        self.results['avalanche'] = result
        return result
    
    def compute_all(self) -> Dict:
        """计算所有指标"""
        print("\n" + "=" * 60)
        print("🧠 生物神经网络复杂度分析")
        print("=" * 60)
        
        self.compute_temporal_complexity()
        self.compute_spatial_complexity()
        self.compute_spatiotemporal_coupling()
        self.compute_nonlinear_amplification_alpha()
        
        return self.results
    
    def print_summary(self):
        """打印摘要"""
        print("\n" + "=" * 60)
        print("📊 分析结果摘要")
        print("=" * 60)
        
        print(f"\n时间复杂度 γ_t")
        print(f"  值: {self.results['temporal']['gamma_t']:.3f} ± {self.results['temporal']['gamma_t_err']:.3f}")
        print(f"  解释: {'接近 Pink Noise（临界态）' if 0.9 <= self.results['temporal']['gamma_t'] <= 1.1 else '偏离临界态'}")
        
        print(f"\n空间复杂度 γ_s")
        print(f"  值: {self.results['spatial']['gamma_s']:.3f} ± {self.results['spatial']['gamma_s_err']:.3f}")
        print(f"  解释: {'典型生物网络' if 2.0 <= self.results['spatial']['gamma_s'] <= 2.5 else '非典型分布'}")
        
        print(f"\n时空协同系数 STC")
        print(f"  值: {self.results['spatiotemporal']['STC']:.3f}")
        print(f"  解释: {'强时空耦合' if self.results['spatiotemporal']['STC'] > 0.5 else '弱耦合'}")
        
        print(f"\n非线性放大指数 α")
        print(f"  值: {self.results['avalanche']['alpha']:.3f} ± {self.results['avalanche']['alpha_err']:.3f}")
        print(f"  解释: {'临界态（分支过程）' if self.results['avalanche']['is_critical'] else '非临界态'}")
        
        # 综合判定
        print("\n【综合临界态判定】")
        temporal_critical = 0.9 <= self.results['temporal']['gamma_t'] <= 1.1
        spatial_typical = 2.0 <= self.results['spatial']['gamma_s'] <= 2.5
        coupling_strong = self.results['spatiotemporal']['STC'] > 0.3
        avalanche_critical = 1.4 <= self.results['avalanche']['alpha'] <= 1.6
        
        print(f"  时间临界态: {['✗', '✓'][temporal_critical]}")
        print(f"  空间典型性: {['✗', '✓'][spatial_typical]}")
        print(f"  时空耦合强: {['✗', '✓'][coupling_strong]}")
        print(f"  雪崩临界态: {['✗', '✓'][avalanche_critical]}")
        
        all_critical = temporal_critical and avalanche_critical
        print(f"\n  🎯 系统处于临界态: {['❌ 否', '✅ 是'][all_critical]}")
    
    def save_results(self, output_file: str = 'neural_complexity_results.json'):
        """保存结果"""
        # 转为 JSON 序列化格式
        json_results = {
            'temporal': {
                'gamma_t': float(self.results['temporal']['gamma_t']),
                'gamma_t_err': float(self.results['temporal']['gamma_t_err']),
                'r_squared': float(self.results['temporal']['r_squared'])
            },
            'spatial': {
                'gamma_s': float(self.results['spatial']['gamma_s']),
                'gamma_s_err': float(self.results['spatial']['gamma_s_err']),
                'density': float(self.results['spatial']['density']),
                'clustering': float(self.results['spatial']['clustering'])
            },
            'spatiotemporal': {
                'STC': float(self.results['spatiotemporal']['STC']),
                'STC_pvalue': float(self.results['spatiotemporal']['STC_pvalue'])
            },
            'avalanche': {
                'alpha': float(self.results['avalanche']['alpha']),
                'alpha_err': float(self.results['avalanche']['alpha_err']),
                'is_critical': bool(self.results['avalanche']['is_critical'])
            }
        }
        
        with open(output_file, 'w') as f:
            json.dump(json_results, f, indent=2)
        
        print(f"\n✓ 结果已保存到 {output_file}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='生物神经网络复杂度分析工具')
    parser.add_argument('--data_path', type=str, required=True, help='Codex 数据目录')
    parser.add_argument('--output', type=str, default='results.json', help='输出文件')
    parser.add_argument('--dt', type=float, default=1.0, help='时间分辨率 (ms)')
    
    args = parser.parse_args()
    
    # 执行分析
    analyzer = NeuralComplexityAnalyzer(args.data_path, dt=args.dt)
    analyzer.compute_all()
    analyzer.print_summary()
    analyzer.save_results(args.output)
