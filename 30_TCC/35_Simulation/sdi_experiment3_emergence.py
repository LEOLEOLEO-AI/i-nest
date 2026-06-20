#!/usr/bin/env python3
"""
SDI 实验三：零先验自演化——从随机图到类脑层次结构

验证命题：给定随机初始网络 + 能量输入（外部刺激），SDI极简规则能否自主涌现层次化模块结构？

三种起点：
  A: 纯随机图 (ER, p=0.02, N=500)
  B: 规则环形格 (WS k=6, p=0, N=500)
  C: 无标度图 (BA m=3, N=500)
每种起点 × 3个随机种子 = 9次仿真

SDI参数与v13完全一致。
"""
import numpy as np
import json
import time
import sys
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors

import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities

OUT = '/home/work/.openclaw/workspace/sdi_sim'

# ============ 参数（与v13完全一致） ============
THETA_LTP = 65
THETA_LTD = 15
ETA_LTP = 0.012
ETA_LTD = 0.008
CASCADE_MAX = 10
N_STEPS = 8000
LOG_INT = 500
N = 500
SEEDS = [42, 7, 13]
P_EXT_STIM = 0.10  # 每步随机激活10%节点

# 额外v13参数
T_DECAY = 400
TAU_STDP = 20.0
EL_HI = 0.25
T_ABS = 3
T_REL = 8
REL_SCALE = 0.4
P_REWIRE = 0.15
REWIRE_INT = 50
SCALING_INT = 100
KAPPA_TARGET = 0.95
SCALING_RATE = 0.05
MAX_FIX = 8

# ============ 图初始化函数 ============
def make_er_graph(N, p, seed):
    """纯随机图 ER"""
    rng = np.random.default_rng(seed)
    G = nx.erdos_renyi_graph(N, p, seed=seed)
    # 确保弱连通
    while not nx.is_connected(G):
        G = nx.erdos_renyi_graph(N, p, seed=rng.integers(1e9))
    return G

def make_ws_graph(N, k, p, seed):
    """Watts-Strogatz环形格"""
    G = nx.watts_strogatz_graph(N, k, p, seed=seed)
    return G

def make_ba_graph(N, m, seed):
    """无标度图 BA (preferential attachment)"""
    G = nx.barabasi_albert_graph(N, m, seed=seed)
    return G

def nx_to_adj(G, N):
    """networkx图转稀疏邻接矩阵（numpy float32）"""
    adj = np.zeros((N, N), dtype=np.float32)
    for u, v in G.edges():
        w = np.random.uniform(0.1, 0.5)
        adj[u, v] = w
        adj[v, u] = w
    return adj

# ============ 网络度量函数 ============
def compute_sigma(adj):
    """小世界系数 σ = (C/C_rand) / (L/L_rand)"""
    try:
        G = adj_to_nx(adj)
        if not nx.is_connected(G):
            G = G.subgraph(max(nx.connected_components(G), key=len)).copy()
        if len(G) < 10:
            return 1.0
        
        C = nx.average_clustering(G)
        try:
            L = nx.average_shortest_path_length(G)
        except:
            # 用近似方法
            sample = min(100, len(G))
            nodes = list(G.nodes())[:sample]
            lengths = []
            for n in nodes:
                sp = nx.single_source_shortest_path_length(G, n)
                lengths.extend(sp.values())
            L = np.mean(lengths) if lengths else 3.0
        
        n = len(G)
        m = G.number_of_edges()
        if n == 0 or m == 0:
            return 1.0
        
        k_avg = 2 * m / n
        if k_avg <= 1:
            return 1.0
        
        C_rand = k_avg / n
        L_rand = np.log(n) / np.log(k_avg) if k_avg > 1 else L
        
        if C_rand == 0 or L_rand == 0:
            return 1.0
        
        sigma = (C / C_rand) / (L / L_rand) if L_rand > 0 else 1.0
        return float(sigma)
    except Exception as e:
        return 1.0

def compute_clustering(adj):
    """聚类系数"""
    try:
        G = adj_to_nx(adj)
        return float(nx.average_clustering(G))
    except:
        return 0.0

def compute_path_length(adj):
    """平均路径长度（近似）"""
    try:
        G = adj_to_nx(adj)
        if not nx.is_connected(G):
            G = G.subgraph(max(nx.connected_components(G), key=len)).copy()
        if len(G) < 5:
            return 3.0
        sample = min(50, len(G))
        nodes = list(G.nodes())[:sample]
        lengths = []
        for n in nodes:
            sp = nx.single_source_shortest_path_length(G, n)
            lengths.extend(sp.values())
        return float(np.mean(lengths)) if lengths else 3.0
    except:
        return 3.0

def compute_modularity_Q(adj):
    """模块化系数Q + 模块数量"""
    try:
        G = adj_to_nx(adj)
        if len(G) < 5:
            return 0.0, 1
        communities = list(greedy_modularity_communities(G))
        Q = nx.community.modularity(G, communities)
        return float(Q), len(communities)
    except Exception as e:
        # 备用简单实现
        try:
            G = adj_to_nx(adj)
            communities = list(greedy_modularity_communities(G))
            # 手动计算Q
            m = G.number_of_edges()
            if m == 0:
                return 0.0, 1
            Q = 0.0
            for comm in communities:
                comm = list(comm)
                lc = G.subgraph(comm).number_of_edges()
                dc = sum(dict(G.degree(comm)).values())
                Q += (lc / m) - (dc / (2 * m)) ** 2
            return float(Q), len(communities)
        except:
            return 0.0, 1

def compute_powerlaw_alpha(adj):
    """幂律指数（Hill estimator）"""
    try:
        G = adj_to_nx(adj)
        degrees = [d for n, d in G.degree() if d > 0]
        if len(degrees) < 10:
            return 2.0
        degrees = np.array(degrees, dtype=float)
        # 用前25%作为tail
        x_min = np.percentile(degrees, 75)
        tail = degrees[degrees >= x_min]
        if len(tail) < 5:
            return 2.0
        alpha = 1 + len(tail) / np.sum(np.log(tail / x_min))
        return float(np.clip(alpha, 1.0, 8.0))
    except:
        return 2.0

def adj_to_nx(adj, threshold=0.05):
    """邻接矩阵转networkx图（无向，阈值过滤）"""
    G = nx.Graph()
    G.add_nodes_from(range(adj.shape[0]))
    rows, cols = np.where((adj + adj.T) / 2 > threshold)
    mask = rows < cols
    for u, v in zip(rows[mask], cols[mask]):
        G.add_edge(int(u), int(v))
    return G

# ============ SDI动力学核心 ============
def sdi_step(adj, v, ref_counter, step, rng):
    """单步SDI演化（与v13一致）"""
    N = len(v)
    
    # 1. 外部刺激（随机激活10%节点）
    stim_mask = rng.random(N) < P_EXT_STIM
    v[stim_mask] += rng.uniform(20, 40, size=stim_mask.sum())
    
    # 2. 突触输入
    syn_input = adj @ v * 0.8
    
    # 3. 更新膜电位（漏积分）
    v = v * (1 - 1/T_DECAY) + syn_input
    
    # 4. 不应期处理
    in_ref = ref_counter > 0
    v[in_ref] = 0.0
    ref_counter[in_ref] -= 1
    
    # 5. 发放检测
    fired = v >= THETA_LTP
    v[fired] = 0.0
    ref_counter[fired] = T_ABS
    
    # 6. STDP（简化版：LTP/LTD规则）
    if fired.any():
        fire_idx = np.where(fired)[0]
        # LTP：pre→post都发放
        for post in fire_idx[:min(20, len(fire_idx))]:  # 限制计算量
            pre_fired = fire_idx
            if len(pre_fired) > 0:
                adj[pre_fired, post] += ETA_LTP * (EL_HI - adj[pre_fired, post])
        
        # LTD：post发放但pre没发放
        not_fired = np.where(~fired)[0]
        if len(not_fired) > 0 and len(fire_idx) > 0:
            sample_post = fire_idx[:min(10, len(fire_idx))]
            for post in sample_post:
                adj[not_fired[:min(20, len(not_fired))], post] *= (1 - ETA_LTD * 0.1)
    
    # 7. 权重裁剪
    np.clip(adj, 0, 1.0, out=adj)
    
    # 8. 稀疏性维护（定期rewire）
    if step % REWIRE_INT == 0:
        # 移除极弱连接
        weak = adj < 0.01
        adj[weak] = 0.0
        # 添加少量随机连接
        n_add = max(1, int(N * 0.001))
        src = rng.integers(0, N, size=n_add)
        dst = rng.integers(0, N, size=n_add)
        mask = src != dst
        adj[src[mask], dst[mask]] += 0.05
    
    # 9. 突触缩放（homeostasis）
    if step % SCALING_INT == 0:
        row_sum = adj.sum(axis=1)
        scale = np.where(row_sum > 0, KAPPA_TARGET / (row_sum + 1e-8), 1.0)
        scale = np.clip(scale, 1 - SCALING_RATE, 1 + SCALING_RATE)
        adj = adj * scale[:, np.newaxis]
    
    return adj, v, ref_counter

# ============ 单次仿真 ============
def run_simulation(graph_type, seed, N=500):
    """运行一次完整仿真，返回时间序列数据"""
    print(f"  开始仿真: {graph_type}, seed={seed}", flush=True)
    rng = np.random.default_rng(seed)
    
    # 初始化图
    if graph_type == 'ER':
        G = make_er_graph(N, p=0.02, seed=seed)
    elif graph_type == 'WS':
        G = make_ws_graph(N, k=6, p=0, seed=seed)
    elif graph_type == 'BA':
        G = make_ba_graph(N, m=3, seed=seed)
    else:
        raise ValueError(f"Unknown graph type: {graph_type}")
    
    adj = nx_to_adj(G, N)
    
    # 初始化神经元状态
    v = rng.uniform(0, 20, size=N).astype(np.float32)
    ref_counter = np.zeros(N, dtype=np.int32)
    
    # 记录初始指标
    ts = {'step': [], 'sigma': [], 'C': [], 'L': [], 'Q': [], 'n_modules': [], 'alpha': []}
    
    t0 = time.time()
    
    for step in range(N_STEPS + 1):
        if step % LOG_INT == 0:
            elapsed = time.time() - t0
            print(f"    step={step}/{N_STEPS} ({elapsed:.1f}s)", flush=True)
            
            sigma = compute_sigma(adj)
            C = compute_clustering(adj)
            L = compute_path_length(adj)
            Q, n_mod = compute_modularity_Q(adj)
            alpha = compute_powerlaw_alpha(adj)
            
            ts['step'].append(step)
            ts['sigma'].append(sigma)
            ts['C'].append(C)
            ts['L'].append(L)
            ts['Q'].append(Q)
            ts['n_modules'].append(n_mod)
            ts['alpha'].append(alpha)
            
            print(f"      σ={sigma:.3f}  C={C:.3f}  L={L:.3f}  Q={Q:.3f}  modules={n_mod}  α={alpha:.3f}", flush=True)
        
        if step < N_STEPS:
            adj, v, ref_counter = sdi_step(adj, v, ref_counter, step, rng)
    
    # 返回最终状态和时间序列
    final = {
        'sigma': ts['sigma'][-1],
        'C': ts['C'][-1],
        'L': ts['L'][-1],
        'Q': ts['Q'][-1],
        'n_modules': ts['n_modules'][-1],
        'alpha': ts['alpha'][-1],
    }
    
    return ts, final, adj

# ============ 模块结构可视化 ============
def plot_module_structure(adjs_by_type, filename):
    """按模块着色的度分布可视化"""
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    types = ['ER', 'WS', 'BA']
    for ax, gtype in zip(axes, types):
        adj = adjs_by_type.get(gtype)
        if adj is None:
            ax.set_title(f'{gtype}: No data')
            continue
        
        G = adj_to_nx(adj)
        communities = list(greedy_modularity_communities(G))
        n_comm = len(communities)
        
        # 为每个节点分配社区颜色
        node_color = {}
        colors = cm.tab20(np.linspace(0, 1, max(n_comm, 2)))
        for i, comm in enumerate(communities):
            for node in comm:
                node_color[node] = colors[min(i, len(colors)-1)]
        
        # 度分布，按社区着色
        degrees = dict(G.degree())
        for i, comm in enumerate(communities):
            comm_list = list(comm)
            if not comm_list:
                continue
            comm_degrees = [degrees[n] for n in comm_list]
            color = colors[min(i, len(colors)-1)]
            ax.hist(comm_degrees, bins=20, alpha=0.5, color=color, 
                   label=f'Module {i+1} (n={len(comm_list)})')
        
        ax.set_xlabel('Degree')
        ax.set_ylabel('Count')
        ax.set_title(f'{gtype} Final Module Structure\n(Q={nx.community.modularity(G, communities):.3f}, {n_comm} modules)')
        if n_comm <= 8:
            ax.legend(fontsize=8)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  保存: {filename}", flush=True)

# ============ 演化曲线可视化 ============
def plot_evolution(all_ts, filename):
    """4子图：σ/C/L/Q的演化曲线（3种起点对比）"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    metrics = ['sigma', 'C', 'L', 'Q']
    metric_names = ['σ (Small-World)', 'C (Clustering)', 'L (Path Length)', 'Q (Modularity)']
    bio_targets = {
        'sigma': 3.0,
        'C': 0.3,
        'L': None,
        'Q': 0.3
    }
    
    colors_map = {
        'ER': {'42': '#e74c3c', '7': '#e74c3c', '13': '#e74c3c'},
        'WS': {'42': '#3498db', '7': '#3498db', '13': '#3498db'},
        'BA': {'42': '#2ecc71', '7': '#2ecc71', '13': '#2ecc71'},
    }
    linestyles = ['-', '--', ':']
    
    for ax, metric, name in zip(axes, metrics, metric_names):
        for gtype in ['ER', 'WS', 'BA']:
            for si, seed in enumerate(SEEDS):
                key = f'{gtype}_seed{seed}'
                if key not in all_ts:
                    continue
                ts = all_ts[key]
                steps = ts['step']
                vals = ts[metric]
                color = colors_map[gtype][str(seed)]
                ls = linestyles[si]
                label = f'{gtype} seed={seed}' if si == 0 else f'_{gtype} seed={seed}'
                ax.plot(steps, vals, color=color, linestyle=ls, linewidth=1.5, 
                       label=label, alpha=0.8)
        
        # 添加参考线
        target = bio_targets.get(metric)
        if target is not None:
            ax.axhline(y=target, color='gray', linestyle='--', alpha=0.5, 
                      label=f'Target={target}')
        
        ax.set_xlabel('Steps')
        ax.set_ylabel(name)
        ax.set_title(name)
        ax.grid(True, alpha=0.3)
        
        # 只在第一个图显示图例
        if metric == 'sigma':
            # 简化图例
            handles, labels = ax.get_legend_handles_labels()
            # 只取有label的
            shown = [(h, l) for h, l in zip(handles, labels) if not l.startswith('_')]
            ax.legend([h for h, l in shown], [l for h, l in shown], 
                     fontsize=8, loc='best')
    
    plt.suptitle('SDI Experiment 3: Zero-Prior Emergence\n(σ, C, L, Q evolution for ER/WS/BA starting graphs)', 
                fontsize=12)
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  保存: {filename}", flush=True)

# ============ 主程序 ============
def main():
    print("=" * 60, flush=True)
    print("SDI 实验三：零先验自演化", flush=True)
    print(f"N={N}, N_STEPS={N_STEPS}, SEEDS={SEEDS}", flush=True)
    print("=" * 60, flush=True)
    
    all_results = {}
    all_ts = {}
    final_adjs = {}  # 每种类型保存最后一个seed的adj用于可视化
    
    graph_types = [
        ('ER', 'Erdos-Renyi (p=0.02)'),
        ('WS', 'Watts-Strogatz (k=6, p=0)'),
        ('BA', 'Barabasi-Albert (m=3)'),
    ]
    
    for gtype, gdesc in graph_types:
        print(f"\n{'='*40}", flush=True)
        print(f"起点: {gtype} — {gdesc}", flush=True)
        print(f"{'='*40}", flush=True)
        
        type_results = []
        for seed in SEEDS:
            ts, final, adj = run_simulation(gtype, seed, N=N)
            key = f'{gtype}_seed{seed}'
            all_ts[key] = ts
            all_results[key] = final
            type_results.append(final)
            final_adjs[gtype] = adj  # 保留最后一个
        
        # 统计均值±std
        metrics = ['sigma', 'C', 'L', 'Q', 'n_modules', 'alpha']
        print(f"\n  {gtype} 汇总统计（3 seeds）:", flush=True)
        for m in metrics:
            vals = [r[m] for r in type_results]
            print(f"    {m}: {np.mean(vals):.3f} ± {np.std(vals):.3f}  [min={min(vals):.3f}, max={max(vals):.3f}]", flush=True)
    
    # 保存 JSON 结果
    output = {
        'experiment': 'SDI Experiment 3: Zero-Prior Emergence',
        'params': {
            'N': N, 'N_STEPS': N_STEPS, 'SEEDS': SEEDS,
            'THETA_LTP': THETA_LTP, 'THETA_LTD': THETA_LTD,
            'ETA_LTP': ETA_LTP, 'ETA_LTD': ETA_LTD,
            'CASCADE_MAX': CASCADE_MAX, 'P_EXT_STIM': P_EXT_STIM,
        },
        'results': all_results,
        'time_series': all_ts,
        'summary': {}
    }
    
    # 计算每种起点的均值
    for gtype, _ in graph_types:
        type_finals = [all_results[f'{gtype}_seed{s}'] for s in SEEDS]
        metrics = ['sigma', 'C', 'L', 'Q', 'n_modules', 'alpha']
        output['summary'][gtype] = {
            m: {
                'mean': float(np.mean([r[m] for r in type_finals])),
                'std': float(np.std([r[m] for r in type_finals])),
            }
            for m in metrics
        }
    
    json_path = os.path.join(OUT, 'exp3_emergence_results.json')
    with open(json_path, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\n结果已保存: {json_path}", flush=True)
    
    # 绘图
    print("\n生成演化曲线图...", flush=True)
    plot_evolution(all_ts, os.path.join(OUT, 'exp3_emergence_evolution.png'))
    
    print("生成模块结构图...", flush=True)
    plot_module_structure(final_adjs, os.path.join(OUT, 'exp3_module_structure.png'))
    
    # 打印关键结论
    print("\n" + "=" * 60, flush=True)
    print("实验三关键结论:", flush=True)
    print("=" * 60, flush=True)
    
    target_sigma = 3.0
    target_Q = 0.3
    target_modules = (3, 7)
    target_alpha = (2.0, 4.5)
    
    print(f"\n{'起点':<6} {'σ均值':>8} {'Q均值':>8} {'模块数':>8} {'α均值':>8} {'σ达标':>6} {'Q达标':>6}", flush=True)
    print("-" * 60, flush=True)
    for gtype, _ in graph_types:
        s = output['summary'][gtype]
        sigma_m = s['sigma']['mean']
        Q_m = s['Q']['mean']
        n_mod_m = s['n_modules']['mean']
        alpha_m = s['alpha']['mean']
        
        sigma_ok = "✅" if sigma_m >= target_sigma else "❌"
        Q_ok = "✅" if Q_m >= target_Q else "❌"
        
        print(f"{gtype:<6} {sigma_m:>8.3f} {Q_m:>8.3f} {n_mod_m:>8.1f} {alpha_m:>8.3f} {sigma_ok:>6} {Q_ok:>6}", flush=True)
    
    print("\n✅ 实验三完成!", flush=True)
    
    return output

if __name__ == '__main__':
    result = main()
