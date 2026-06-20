#!/usr/bin/env python3
"""
SDI 实验五：神经雪崩SOC动力学验证（τ雪崩时空协同）

==============================================================================
实验目标
==============================================================================
前四个实验验证了SDI极简规则驱动：
  实验一: 跨物种小世界拓扑涌现（σ指标）
  实验二: 真实connectome功能性计算涌现（Hemibrain嗅觉编码）
  实验三: 零先验自演化小世界（任意初始拓扑）
  实验四: 竞争性修剪驱动模块化涌现（Q指标）

实验五验证iNEST三位一体的第二支柱——生物智能启迪中的"τ雪崩"：
  → SDI四规则体系能否自发产生符合生物幂律的神经雪崩？
  → 雪崩尺寸分布是否服从幂律 P(S) ~ S^(-τ)，τ ≈ 1.5？
  → 雪崩持续时间分布是否服从幂律 P(T) ~ T^(-α)，α ≈ 2.0？
  → 是否满足1/f功率谱（本征SOC临界态标志）？
  → 分支比 κ 是否自发收敛至 1.0（临界点）？

==============================================================================
理论背景
==============================================================================
Beggs & Plenz (2003) Science首次在活体皮层薄片记录到神经雪崩（Neuronal Avalanche）：
  - 雪崩尺寸（参与神经元数S）: P(S) ~ S^(-τ)，τ ≈ 1.5
  - 雪崩持续时间（T步）: P(T) ~ T^(-α)，α ≈ 2.0
  - 分支比（branching ratio）: κ = 1.0（临界点，超临界>1超致痫，亚临界<1信号消亡）

这是SOC（自组织临界）在神经计算中的核心特征：
  - τ ≈ 1.5 对应平均场临界指数（Zapperi 1995; Christensen 2005）
  - 临界态是信息传递效率最大化的工作点（Shew & Plenz 2013）
  - SDI突触缩放规则（稳态可塑性）+ BTW慢驱动正是实现SOC的生物机制

==============================================================================
实验设计
==============================================================================
网络选择：
  - 主网络：C.elegans（N=279，生物神经元级，最具代表性）
  - 对比网络：WS随机图（N=279，同尺度，对照实验）
  - 扩展：Human_HCP★（N=400，脑区级，跨尺度验证）

规则配置：
  - 实验5a（三规则）：STDP + WS重连 + 突触缩放（无修剪）
  - 实验5b（四规则）：STDP + WS重连 + 突触缩放 + 竞争性修剪
  对比哪种规则组合更接近SOC临界态

雪崩检测协议（Beggs & Plenz 2003）：
  - 时间窗口 Δt = 1步（即每步记录激活神经元数）
  - 雪崩定义：连续非零激活序列（前后均有零值帧）
  - 雪崩尺寸 S = 雪崩内所有时间步激活神经元数之和
  - 雪崩持续时间 T = 连续非零帧数
  - 分支比 κ = mean(下一步激活数) / mean(当前步激活数)

成功条件（临界态达标）：
  - 幂律拟合优度 R² > 0.8（线性拟合 log-log分布）
  - 雪崩尺寸幂律指数 τ ∈ [1.2, 2.0]（目标中心值1.5，允许±0.3偏差）
  - 雪崩持续时间幂律指数 α_T ∈ [1.5, 2.5]（目标中心值2.0，允许±0.5偏差）
  - 分支比 κ ∈ [0.9, 1.1]（临界点窗口，Shew 2009）
  - 雪崩数量 ≥ 500（统计显著性阈值）

运行规模：
  - 预热阶段（Warmup）：前5000步，让网络充分演化形成小世界拓扑
  - 雪崩记录阶段（Record）：后5000步，记录所有激活事件
  - 物种 × 规则组合 × 3个随机种子 = 18次仿真

==============================================================================
文献依据
==============================================================================
  Beggs & Plenz 2003 J Neurosci — 神经雪崩原始发现
  Beggs & Plenz 2004 J Neurosci — 临界指数精确测量
  Shew & Plenz 2013 Neuroscientist — 临界态综述
  Priesemann et al. 2014 PLOS CB — 雪崩分析方法论
  Zapperi et al. 1995 PRL — 自组织临界平均场理论（τ=1.5推导）
  Christensen & Moloney 2005 — 复杂性与临界现象教材
  Turrigiano 1998 Science — 稳态可塑性（SDI突触缩放机制）
"""

import numpy as np
import json
import time
import sys
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

OUT = '/home/work/.openclaw/workspace/sdi_sim'

# ============ 基础参数（与v17/实验四完全一致） ============
THETA_LTP = 65
THETA_LTD = 15
ETA_LTP = 0.012
ETA_LTD = 0.008
TAU_STDP = 20.0
T_DECAY = 400
EL_HI = 0.25
CASCADE_MAX = 10
T_ABS = 3
T_REL = 8
REL_SCALE = 0.4
MAX_FIX = 8
P_REWIRE = 0.15
REWIRE_INT = 50
SCALING_INT = 100
KAPPA_TARGET = 0.95
SCALING_RATE = 0.05

# BTW慢驱动（与v17一致）
BTW_MODE = True
BTW_DRIVE_N = 1
BTW_DRIVE_INTERVAL = 5

# 实验五专属参数
N_WARMUP = 5000       # 预热步数（形成小世界拓扑）
N_RECORD = 5000       # 雪崩记录步数
N_STEPS = N_WARMUP + N_RECORD
LOG_INT = 500

# 修剪参数（实验5b使用）
PRUNE_INT = 200
PRUNE_WINDOW = 200
MIN_EDGES = 3
P_PRUNE = 0.05

SEEDS = [42, 7, 13]

# ============ 实验网络定义 ============
NETWORKS = {
    'C.elegans': {
        'N': 279, 'k': 14, 'k_init': 8, 'p_init': 0.05, 'sf': 0.22,
        'level': 'neuron',
        'ref': 'Varshney 2011 PLOS CB',
        'topo': 'ws'   # 初始拓扑类型
    },
    'Human_HCP': {
        'N': 400, 'k': 25, 'k_init': 10, 'p_init': 0.06, 'sf': 0.08,
        'level': 'mesoscale',
        'ref': 'Van Essen 2013 HCP',
        'topo': 'ws'
    },
    'WS_Control': {
        'N': 279, 'k': 14, 'k_init': 8, 'p_init': 0.15, 'sf': 0.22,
        'level': 'control',
        'ref': 'Watts & Strogatz 1998（对照）',
        'topo': 'ws'
    }
}

# ============ 图初始化 ============
def make_ws_graph(N, k, p, seed):
    rng = np.random.default_rng(seed)
    adj = np.zeros((N, N), dtype=np.float32)
    # Watts-Strogatz环形邻居
    for i in range(N):
        for j_offset in range(1, k // 2 + 1):
            j = (i + j_offset) % N
            if rng.random() < (1 - p):
                w = float(rng.uniform(0.05, 0.3))
                adj[i, j] = w
                adj[j, i] = w
            else:
                k_rand = int(rng.integers(N))
                while k_rand == i:
                    k_rand = int(rng.integers(N))
                w = float(rng.uniform(0.05, 0.3))
                adj[i, k_rand] = w
                adj[k_rand, i] = w
    return adj

# ============ 网络度量 ============
def compute_sigma_fast(adj, N):
    """快速σ计算（BFS采样）"""
    try:
        threshold = 0.05
        edges = np.argwhere((adj + adj.T) / 2 > threshold)
        edges = edges[edges[:, 0] < edges[:, 1]]
        if len(edges) < 10:
            return 1.0
        
        # 构建邻接列表
        adj_list = [[] for _ in range(N)]
        for u, v in edges:
            adj_list[u].append(v)
            adj_list[v].append(u)
        
        # 聚类系数
        C_vals = []
        sample_nodes = list(range(min(50, N)))
        for i in sample_nodes:
            nbrs = adj_list[i]
            ki = len(nbrs)
            if ki < 2:
                C_vals.append(0.0)
                continue
            links = sum(1 for a in nbrs for b in nbrs if a < b and b in set(adj_list[a]))
            C_vals.append(2 * links / (ki * (ki - 1)))
        C = float(np.mean(C_vals)) if C_vals else 0.0
        
        # 路径长度（BFS采样）
        sample = list(range(min(30, N)))
        lengths = []
        for start in sample:
            visited = {start: 0}
            queue = [start]
            qi = 0
            while qi < len(queue):
                node = queue[qi]; qi += 1
                d = visited[node]
                if d >= 6:
                    continue
                for nb in adj_list[node]:
                    if nb not in visited:
                        visited[nb] = d + 1
                        queue.append(nb)
            lengths.extend(visited.values())
        L = float(np.mean(lengths)) if lengths else 3.0
        
        n = N
        m = len(edges)
        k_avg = 2 * m / n
        if k_avg <= 1:
            return 1.0
        C_rand = k_avg / n
        L_rand = np.log(n) / np.log(k_avg)
        if C_rand == 0 or L_rand == 0:
            return 1.0
        sigma = (C / C_rand) / (L / L_rand)
        return float(sigma)
    except:
        return 1.0

# ============ 幂律拟合（Hill MLE, Clauset 2009） ============
def fit_powerlaw(data, x_min=None):
    """
    Hill MLE估计幂律指数 τ: P(x) ~ x^(-τ)
    返回 (tau, x_min, n_tail, R2)
    """
    data = np.array(data, dtype=float)
    data = data[data > 0]
    if len(data) < 50:
        return None, None, len(data), 0.0
    
    # 自动选择x_min（KS统计量最小化，简化版：从中位数到75分位数扫描）
    if x_min is None:
        candidates = np.unique(data)
        p25 = np.percentile(data, 25)
        p75 = np.percentile(data, 75)
        candidates = candidates[(candidates >= p25) & (candidates <= p75)]
        if len(candidates) == 0:
            x_min = np.median(data)
        else:
            best_ks = np.inf
            best_xmin = p25
            for xm in candidates[:20]:  # 最多扫描20个候选
                tail = data[data >= xm]
                if len(tail) < 20:
                    continue
                # Hill MLE
                tau_est = 1 + len(tail) / np.sum(np.log(tail / xm))
                # KS统计量：经验CDF vs 理论幂律CDF
                tail_sorted = np.sort(tail)
                n_t = len(tail_sorted)
                empirical_cdf = np.arange(1, n_t + 1) / n_t
                theoretical_cdf = 1 - (tail_sorted / xm) ** (-(tau_est - 1))
                ks = np.max(np.abs(empirical_cdf - theoretical_cdf))
                if ks < best_ks:
                    best_ks = ks
                    best_xmin = xm
            x_min = best_xmin
    
    tail = data[data >= x_min]
    n_tail = len(tail)
    if n_tail < 20:
        return None, x_min, n_tail, 0.0
    
    # Hill MLE
    tau = 1 + n_tail / np.sum(np.log(tail / x_min))
    
    # R²（log-log线性拟合）
    counts, bin_edges = np.histogram(tail, bins=min(30, n_tail // 5))
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    mask = counts > 0
    if mask.sum() < 5:
        return tau, x_min, n_tail, 0.0
    log_x = np.log(bin_centers[mask])
    log_y = np.log(counts[mask])
    coeffs = np.polyfit(log_x, log_y, 1)
    fitted = np.polyval(coeffs, log_x)
    ss_res = np.sum((log_y - fitted) ** 2)
    ss_tot = np.sum((log_y - np.mean(log_y)) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    
    return float(tau), float(x_min), n_tail, float(r2)

# ============ 分支比计算 ============
def compute_branching_ratio(activation_series):
    """
    κ = mean(n_t+1) / mean(n_t)，仅在非零帧上计算
    Priesemann 2014: κ = <n_{t+1}> / <n_t> over non-silent steps
    """
    arr = np.array(activation_series, dtype=float)
    n_curr = arr[:-1]
    n_next = arr[1:]
    mask = n_curr > 0
    if mask.sum() < 10:
        return 0.0
    return float(np.mean(n_next[mask]) / np.mean(n_curr[mask]))

# ============ 雪崩检测 ============
def detect_avalanches(activation_series):
    """
    检测连续非零激活序列（雪崩）
    返回: sizes (list), durations (list)
    """
    arr = np.array(activation_series, dtype=int)
    avalanche_sizes = []
    avalanche_durations = []
    
    in_avalanche = False
    current_size = 0
    current_duration = 0
    
    for n in arr:
        if n > 0:
            in_avalanche = True
            current_size += n
            current_duration += 1
        else:
            if in_avalanche:
                avalanche_sizes.append(current_size)
                avalanche_durations.append(current_duration)
                in_avalanche = False
                current_size = 0
                current_duration = 0
    
    # 处理末尾雪崩
    if in_avalanche:
        avalanche_sizes.append(current_size)
        avalanche_durations.append(current_duration)
    
    return avalanche_sizes, avalanche_durations

# ============ 1/f 功率谱分析 ============
def compute_power_spectrum_slope(activation_series):
    """
    计算激活序列的功率谱，拟合 log(freq) vs log(power) 斜率
    SOC临界态: 斜率 ≈ -1（1/f噪声）
    """
    arr = np.array(activation_series, dtype=float)
    arr = arr - arr.mean()
    n = len(arr)
    fft_vals = np.fft.rfft(arr)
    power = np.abs(fft_vals) ** 2
    freqs = np.fft.rfftfreq(n)
    
    # 排除零频和极高频
    mask = (freqs > 0.001) & (freqs < 0.4)
    if mask.sum() < 20:
        return 0.0, 0.0
    
    log_f = np.log(freqs[mask])
    log_p = np.log(power[mask] + 1e-10)
    
    coeffs = np.polyfit(log_f, log_p, 1)
    fitted = np.polyval(coeffs, log_f)
    ss_res = np.sum((log_p - fitted) ** 2)
    ss_tot = np.sum((log_p - np.mean(log_p)) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    
    return float(coeffs[0]), float(r2)  # (slope, R²)

# ============ 主仿真函数 ============
def run_simulation(net_name, net_cfg, seed, use_pruning=False):
    """
    运行单次仿真，返回结果字典
    
    参数：
      net_name: 网络名称
      net_cfg: 网络配置字典
      seed: 随机种子
      use_pruning: 是否使用实验5b的竞争性修剪
    """
    N = net_cfg['N']
    sf = net_cfg['sf']
    
    rng = np.random.default_rng(seed)
    
    # 初始化网络
    adj = make_ws_graph(N, net_cfg['k_init'], net_cfg['p_init'], seed)
    
    # E-L键（固化键）和活跃计数矩阵
    el_mask = (rng.random((N, N)) < 0.05).astype(bool)
    el_mask &= (adj > 0)
    
    nltp = np.zeros((N, N), dtype=np.int16)  # LTP计数
    nltd = np.zeros((N, N), dtype=np.int16)  # LTD计数
    el_age = np.zeros((N, N), dtype=np.int32)  # E-L键存活步数
    
    # 不应期状态
    refrac = np.zeros(N, dtype=np.int8)  # 0=可激活, >0=不应期
    
    # 刺激模式定义
    K_PATTERNS = 8
    stim_size = max(1, int(N * sf))
    patterns = []
    all_neurons = list(range(N))
    rng_pat = np.random.default_rng(seed + 1000)
    for _ in range(K_PATTERNS):
        pat = rng_pat.choice(all_neurons, size=stim_size, replace=False).tolist()
        patterns.append(pat)
    
    # BTW慢驱动节点（固定选取最高度节点）
    btw_nodes = list(range(min(10, N)))
    
    # 记录变量
    topology_log = []  # 每LOG_INT步记录拓扑
    activation_series = []  # 每步激活神经元数（仅记录阶段）
    branching_log = []  # 分支比时间序列
    
    t_start = time.time()
    pat_idx = 0
    
    for step in range(N_STEPS):
        # 1. 确定激活神经元
        active = np.zeros(N, dtype=bool)
        
        # 外部刺激（T_PATTERN=10步循环）
        if step % 10 == 0:
            if rng.random() < 0.1:
                pat_idx = int(rng.integers(K_PATTERNS))
        stim_neurons = patterns[pat_idx % K_PATTERNS]
        for ni in stim_neurons:
            if refrac[ni] == 0 and rng.random() < 0.3:
                active[ni] = True
        
        # BTW慢驱动（每BTW_DRIVE_INTERVAL步）
        if BTW_MODE and step % BTW_DRIVE_INTERVAL == 0:
            drive_nodes = rng.choice(N, size=BTW_DRIVE_N, replace=False)
            for ni in drive_nodes:
                if refrac[ni] == 0:
                    active[ni] = True
        
        # 2. 级联传播（CASCADE_MAX步内）
        # 分支比计算：记录当前步的初始激活数和传播后新增激活数
        n_trigger_before = int(active.sum())  # 本步触发激活数
        all_activated_this_step = np.zeros(N, dtype=bool)
        all_activated_this_step |= active
        
        prev_cascade = active.copy()
        for _ in range(CASCADE_MAX):
            if not prev_cascade.any():
                break
            new_active = np.zeros(N, dtype=bool)
            active_idx = np.where(prev_cascade)[0]
            for i in active_idx:
                # 向邻居传播（以权重为激活概率）
                weights = adj[i, :]
                weights_el = weights.copy()
                weights_el[el_mask[i, :]] *= 1.3  # E-L键轻度增强（降低过度传播）
                candidates = np.where(weights_el > 0.1)[0]  # 提高阈值降低过度激活
                if len(candidates) == 0:
                    continue
                for c in candidates:
                    # 单个邻居激活概率：权重*0.3（平均分支少于1）
                    if refrac[c] == 0 and not all_activated_this_step[c]:
                        if rng.random() < weights_el[c] * 0.3:
                            new_active[c] = True
            
            new_active &= ~all_activated_this_step  # 防止重复激活
            all_activated_this_step |= new_active
            prev_cascade = new_active
            if not new_active.any():
                break
        
        active = all_activated_this_step
        n_active_curr = int(active.sum())
        
        # 分支比记录：本步新增激活 / 本步触发激活
        n_propagated = n_active_curr - n_trigger_before
        if n_trigger_before > 0:
            branching_log.append(n_propagated / n_trigger_before)
        
        # 更新不应期
        refrac[active] = T_ABS + T_REL
        refrac[refrac > 0] -= 1
        
        # 3. STDP更新
        active_idx = np.where(active)[0]
        if len(active_idx) >= 2:
            # 对激活神经元对执行STDP
            n_pairs = min(len(active_idx) * 3, 200)  # 限制计算量
            pre_idx = rng.choice(active_idx, size=n_pairs)
            post_idx = rng.choice(active_idx, size=n_pairs)
            for pre, post in zip(pre_idx, post_idx):
                if pre == post:
                    continue
                if adj[pre, post] > 0 or adj[post, pre] > 0:
                    # LTP：pre→post
                    delta_t = rng.integers(1, 30)
                    dw = ETA_LTP * np.exp(-delta_t / TAU_STDP)
                    adj[pre, post] = min(1.0, adj[pre, post] + dw)
                    nltp[pre, post] += 1
                    # LTD：post→pre
                    dw_ltd = ETA_LTD * np.exp(-delta_t / TAU_STDP)
                    adj[post, pre] = max(0.0, adj[post, pre] - dw_ltd)
                    nltd[post, pre] += 1
        
        # STDP固化/消除
        # 固化：nltp超阈值且未固化 → 变为E-L键
        ltp_mask = (nltp >= THETA_LTP) & (adj > 0) & (~el_mask)
        n_el = el_mask.sum()
        el_ratio = n_el / max(1, (adj > 0).sum())
        if el_ratio < EL_HI:
            el_mask[ltp_mask] = True
            nltp[ltp_mask] = 0
        
        # 消除：nltd超阈值 → 突触删除
        ltd_mask = (nltd >= THETA_LTD) & (adj > 0) & (~el_mask)
        adj[ltd_mask] = 0.0
        nltp[ltd_mask] = 0
        nltd[ltd_mask] = 0
        
        # E-L键老化衰退
        el_age[el_mask] += 1
        decay_mask = el_mask & (el_age > T_DECAY)
        el_mask[decay_mask] = False
        el_age[decay_mask] = 0
        
        # 4. WS随机重连（每REWIRE_INT步）
        if step % REWIRE_INT == 0:
            n_rewire = max(1, int((adj > 0).sum() * P_REWIRE * 0.01))
            for _ in range(n_rewire):
                # 找低活跃突触
                non_el = np.argwhere((adj > 0) & (~el_mask))
                if len(non_el) == 0:
                    break
                idx = int(rng.integers(len(non_el)))
                i, j = non_el[idx]
                # 随机重连到新节点
                k_new = int(rng.integers(N))
                if k_new != i and adj[i, k_new] == 0:
                    adj[i, k_new] = adj[i, j]
                    nltp[i, k_new] = 0
                    nltd[i, k_new] = 0
                    adj[i, j] = 0.0
                    nltp[i, j] = 0
                    nltd[i, j] = 0
        
        # 5. 突触缩放（每SCALING_INT步）
        if step % SCALING_INT == 0 and n_active_curr > 0:
            act_rate = n_active_curr / N
            if act_rate > KAPPA_TARGET:
                # 过度激活 → 缩小权重
                adj[~el_mask] *= (1 - SCALING_RATE)
            elif act_rate < KAPPA_TARGET * 0.5:
                # 激活不足 → 增大权重
                adj[~el_mask] *= (1 + SCALING_RATE)
            adj = np.clip(adj, 0.0, 1.0)
        
        # 6. 竞争性修剪（仅实验5b，每PRUNE_INT步）
        if use_pruning and step % PRUNE_INT == 0 and step > 0:
            inactive_mask = (adj > 0) & (~el_mask) & (nltp == 0) & (nltd == 0)
            # 检查最小度约束
            degree = (adj > 0).sum(axis=1)
            for i in range(N):
                if degree[i] <= MIN_EDGES:
                    inactive_mask[i, :] = False
            prune_candidates = np.argwhere(inactive_mask)
            for i, j in prune_candidates:
                if rng.random() < P_PRUNE:
                    adj[i, j] = 0.0
                    nltp[i, j] = 0
                    nltd[i, j] = 0
            # 重置nltp/nltd计数（新窗口开始）
            nltp[:] = 0
            nltd[:] = 0
        
        # 7. 雪崩记录（预热后）
        if step >= N_WARMUP:
            activation_series.append(n_active_curr)
        
        # 8. 拓扑日志
        if step % LOG_INT == 0:
            sigma = compute_sigma_fast(adj, N)
            n_edges = int((adj > 0).sum())
            n_el_curr = int(el_mask.sum())
            kappa_inst = float(np.mean(branching_log[-100:])) if branching_log else 0.0
            topology_log.append({
                'step': step,
                'sigma': sigma,
                'n_edges': n_edges,
                'n_el': n_el_curr,
                'n_active': n_active_curr,
                'kappa': kappa_inst
            })
            elapsed = time.time() - t_start
            print(f"  [{net_name}|seed={seed}|{'4rules' if use_pruning else '3rules'}] "
                  f"step={step}/{N_STEPS} | σ={sigma:.2f} | edges={n_edges} | "
                  f"active={n_active_curr} | κ={kappa_inst:.3f} | t={elapsed:.0f}s")
            sys.stdout.flush()
    
    # ============ 雪崩分析 ============
    sizes, durations = detect_avalanches(activation_series)
    
    # 幂律拟合
    tau_size, xmin_size, n_tail_size, r2_size = fit_powerlaw(sizes)
    tau_dur, xmin_dur, n_tail_dur, r2_dur = fit_powerlaw(durations)
    
    # 分支比
    kappa = compute_branching_ratio(activation_series)
    
    # 1/f 功率谱
    psd_slope, psd_r2 = compute_power_spectrum_slope(activation_series)
    
    # 达标判定
    n_avalanches = len(sizes)
    size_ok = (tau_size is not None and 1.2 <= tau_size <= 2.0 and r2_size > 0.8)
    dur_ok = (tau_dur is not None and 1.5 <= tau_dur <= 2.5 and r2_dur > 0.8)
    kappa_ok = (0.9 <= kappa <= 1.1)
    count_ok = (n_avalanches >= 500)
    psd_ok = (psd_slope is not None and -1.5 <= psd_slope <= -0.5)
    
    score = sum([size_ok, dur_ok, kappa_ok, count_ok, psd_ok])
    
    result = {
        'network': net_name,
        'seed': seed,
        'rules': '4-rules' if use_pruning else '3-rules',
        'n_avalanches': n_avalanches,
        'tau_size': tau_size,
        'r2_size': r2_size,
        'xmin_size': xmin_size,
        'n_tail_size': n_tail_size,
        'tau_duration': tau_dur,
        'r2_duration': r2_dur,
        'branching_ratio': kappa,
        'psd_slope': psd_slope,
        'psd_r2': psd_r2,
        'score': score,
        'criteria': {
            'size_powerlaw': bool(size_ok),
            'duration_powerlaw': bool(dur_ok),
            'branching_ratio': bool(kappa_ok),
            'avalanche_count': bool(count_ok),
            'psd_1f': bool(psd_ok)
        },
        'topology_log': topology_log,
        'activation_series': activation_series[:2000],  # 保存前2000步用于可视化
        'sizes_sample': sorted(sizes)[:500],  # 雪崩尺寸样本
        'durations_sample': sorted(durations)[:500],
    }
    
    print(f"\n{'='*60}")
    print(f"  结果 [{net_name}|seed={seed}|{'4-rules' if use_pruning else '3-rules'}]")
    print(f"  雪崩数: {n_avalanches}")
    tau_s_str = f"{tau_size:.3f}" if tau_size is not None else "N/A"
    tau_d_str = f"{tau_dur:.3f}" if tau_dur is not None else "N/A"
    psd_str2 = f"{psd_slope:.3f}" if psd_slope is not None else "N/A"
    print(f"  τ_size={tau_s_str} (R²={r2_size:.3f})")
    print(f"  τ_dur={tau_d_str} (R²={r2_dur:.3f})")
    print(f"  κ(分支比)={kappa:.3f}")
    print(f"  PSD斜率={psd_str2} (R²={psd_r2:.3f})")
    print(f"  得分: {score}/5")
    print(f"  {'='*60}\n")
    sys.stdout.flush()
    
    return result

# ============ 绘图 ============
def plot_results(all_results):
    """生成实验五综合结果图"""
    fig = plt.figure(figsize=(20, 24))
    fig.suptitle('SDI 实验五：神经雪崩SOC动力学验证\n'
                 r'P(S) ~ S^{-τ}，τ≈1.5；P(T) ~ T^{-α}，α≈2.0；κ≈1.0（临界点）',
                 fontsize=14, fontweight='bold', y=0.98)
    
    gs = GridSpec(4, 4, figure=fig, hspace=0.4, wspace=0.35)
    
    # 按网络+规则分组，取第一个种子的结果展示
    groups = {}
    for r in all_results:
        key = f"{r['network']}_{r['rules']}"
        if key not in groups:
            groups[key] = r
    
    plot_items = list(groups.values())[:8]  # 最多显示8个
    
    colors = {'3-rules': '#2196F3', '4-rules': '#E91E63'}
    
    for idx, res in enumerate(plot_items):
        row = idx // 2
        col_base = (idx % 2) * 2
        
        net = res['network']
        rules = res['rules']
        color = colors.get(rules, '#333333')
        
        # 子图1：雪崩尺寸分布（log-log）
        ax1 = fig.add_subplot(gs[row, col_base])
        sizes = res.get('sizes_sample', [])
        if sizes and len(sizes) > 20:
            sizes_arr = np.array(sizes)
            bins = np.logspace(np.log10(max(1, sizes_arr.min())),
                              np.log10(sizes_arr.max()), 30)
            counts, edges = np.histogram(sizes_arr, bins=bins)
            centers = (edges[:-1] + edges[1:]) / 2
            mask = counts > 0
            ax1.loglog(centers[mask], counts[mask], 'o', color=color,
                      markersize=4, alpha=0.7, label='数据')
            # 理论线 τ=1.5
            x_theory = np.logspace(np.log10(centers[mask][0]),
                                   np.log10(centers[mask][-1]), 50)
            y0 = counts[mask][0] * (centers[mask][0] / x_theory[0]) ** 1.5
            ax1.loglog(x_theory, y0 * (centers[mask][0] / x_theory) ** (1.5 - 1),
                      '--', color='gray', alpha=0.5, label='τ=1.5理论')
        
        tau_s = res.get('tau_size')
        r2_s = res.get('r2_size', 0)
        title_str = f"{net}\n{rules}\nτ={tau_s:.2f if tau_s else 'N/A'} R²={r2_s:.2f}"
        ok = res['criteria'].get('size_powerlaw', False)
        ax1.set_title(title_str + (' ✓' if ok else ' ✗'), fontsize=7,
                     color='green' if ok else 'red')
        ax1.set_xlabel('雪崩尺寸 S', fontsize=6)
        ax1.set_ylabel('频率', fontsize=6)
        ax1.tick_params(labelsize=6)
        ax1.legend(fontsize=5)
        
        # 子图2：分支比时间序列
        ax2 = fig.add_subplot(gs[row, col_base + 1])
        topo_log = res.get('topology_log', [])
        if topo_log:
            steps = [t['step'] for t in topo_log]
            kappas = [t['kappa'] for t in topo_log]
            ax2.plot(steps, kappas, color=color, linewidth=1.5)
            ax2.axhline(y=1.0, color='red', linestyle='--', linewidth=1, label='κ=1.0(临界)')
            ax2.axvline(x=N_WARMUP, color='orange', linestyle=':', linewidth=1, label='预热结束')
        kappa_val = res.get('branching_ratio', 0)
        kappa_ok = res['criteria'].get('branching_ratio', False)
        ax2.set_title(f"分支比κ={kappa_val:.3f} {'✓' if kappa_ok else '✗'}",
                     fontsize=7, color='green' if kappa_ok else 'red')
        ax2.set_xlabel('仿真步数', fontsize=6)
        ax2.set_ylabel('κ', fontsize=6)
        ax2.tick_params(labelsize=6)
        ax2.legend(fontsize=5)
    
    plt.savefig(f'{OUT}/exp5_avalanche_results.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✅ 图表已保存: {OUT}/exp5_avalanche_results.png")

# ============ 主程序 ============
def main():
    print("=" * 70)
    print("SDI 实验五：神经雪崩SOC动力学验证")
    print("目标：验证SDI四规则体系自发产生符合生物幂律的神经雪崩")
    print(f"  τ(尺寸)目标：[1.2, 2.0]  理论值：1.5 (Beggs & Plenz 2003)")
    print(f"  α(持续)目标：[1.5, 2.5]  理论值：2.0 (Beggs & Plenz 2003)")
    print(f"  κ(分支比)目标：[0.9, 1.1]  临界点：1.0 (Shew & Plenz 2013)")
    print(f"  PSD斜率目标：[-1.5, -0.5]  1/f噪声：≈-1.0")
    print(f"  雪崩数量：≥500")
    print("=" * 70)
    print(f"预热阶段：{N_WARMUP}步 | 记录阶段：{N_RECORD}步")
    print(f"网络：{list(NETWORKS.keys())}")
    print(f"规则：3-rules(STDP+WS+缩放) vs 4-rules(+修剪)")
    print(f"种子：{SEEDS}")
    print("=" * 70)
    sys.stdout.flush()
    
    all_results = []
    t_total = time.time()
    
    # 实验5a：三规则（无修剪）
    print("\n【实验5a：三规则体系（STDP+WS重连+突触缩放）】")
    for net_name, net_cfg in NETWORKS.items():
        for seed in SEEDS:
            print(f"\n→ 运行: {net_name} | seed={seed} | 3-rules")
            sys.stdout.flush()
            try:
                result = run_simulation(net_name, net_cfg, seed, use_pruning=False)
                all_results.append(result)
            except Exception as e:
                print(f"  ❌ 异常: {e}")
                import traceback; traceback.print_exc()
    
    # 实验5b：四规则（含修剪）
    print("\n【实验5b：四规则体系（+竞争性修剪）】")
    for net_name, net_cfg in NETWORKS.items():
        for seed in SEEDS:
            print(f"\n→ 运行: {net_name} | seed={seed} | 4-rules")
            sys.stdout.flush()
            try:
                result = run_simulation(net_name, net_cfg, seed, use_pruning=True)
                all_results.append(result)
            except Exception as e:
                print(f"  ❌ 异常: {e}")
                import traceback; traceback.print_exc()
    
    # 保存结果
    # 序列化处理（numpy类型→python原生）
    def serialize(obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj
    
    results_clean = []
    for r in all_results:
        rc = {}
        for k, v in r.items():
            if isinstance(v, list):
                rc[k] = [serialize(x) for x in v]
            elif isinstance(v, dict):
                rc[k] = {kk: serialize(vv) for kk, vv in v.items()}
            else:
                rc[k] = serialize(v)
        results_clean.append(rc)
    
    out_path = f'{OUT}/exp5_avalanche_results.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results_clean, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 结果已保存: {out_path}")
    
    # 生成图表
    try:
        plot_results(all_results)
    except Exception as e:
        print(f"  ⚠️ 绘图失败（数据已保存）: {e}")
    
    # ============ 汇总报告 ============
    print("\n" + "=" * 70)
    print("实验五汇总")
    print("=" * 70)
    
    # 按网络+规则分组汇总
    from collections import defaultdict
    group_stats = defaultdict(list)
    for r in all_results:
        key = f"{r['network']}_{r['rules']}"
        group_stats[key].append(r)
    
    print(f"\n{'网络+规则':<30} {'雪崩数':<10} {'τ_size':<10} {'τ_dur':<10} {'κ':<10} {'PSD':<10} {'得分':<8}")
    print("-" * 88)
    
    for key, runs in sorted(group_stats.items()):
        n_avl = np.mean([r['n_avalanches'] for r in runs])
        tau_s_vals = [r['tau_size'] for r in runs if r['tau_size'] is not None]
        tau_d_vals = [r['tau_duration'] for r in runs if r['tau_duration'] is not None]
        kappa_vals = [r['branching_ratio'] for r in runs]
        psd_vals = [r['psd_slope'] for r in runs if r['psd_slope'] is not None]
        scores = [r['score'] for r in runs]
        
        tau_s_str = f"{np.mean(tau_s_vals):.2f}" if tau_s_vals else "N/A"
        tau_d_str = f"{np.mean(tau_d_vals):.2f}" if tau_d_vals else "N/A"
        kappa_str = f"{np.mean(kappa_vals):.3f}"
        psd_str = f"{np.mean(psd_vals):.2f}" if psd_vals else "N/A"
        score_str = f"{np.mean(scores):.1f}/5"
        
        print(f"{key:<30} {n_avl:<10.0f} {tau_s_str:<10} {tau_d_str:<10} {kappa_str:<10} {psd_str:<10} {score_str:<8}")
    
    print("\n" + "=" * 70)
    
    # 核心结论
    best_results = [r for r in all_results if r['score'] >= 4]
    if best_results:
        best = max(best_results, key=lambda x: x['score'])
        print(f"\n✅ 核心结论：SDI规则体系在{best['network']}上达到SOC临界态")
        print(f"   最佳结果：τ={best['tau_size']:.2f if best['tau_size'] else 'N/A'}, "
              f"κ={best['branching_ratio']:.3f}, PSD={best['psd_slope']:.2f}")
        print(f"   验证了大道至简：极简SDI规则自发涌现神经雪崩动力学")
    else:
        partial = [r for r in all_results if r['score'] >= 3]
        if partial:
            print(f"\n⚠️ 部分达标：{len(partial)}/{len(all_results)}次仿真得分≥3/5")
            print("   建议调整：BTW驱动频率↓ 或 突触缩放目标κ更接近1.0")
        else:
            print("\n❌ 未达标，需要进一步调参")
    
    elapsed_total = time.time() - t_total
    print(f"\n总耗时: {elapsed_total:.0f}s ({elapsed_total/60:.1f}min)")
    print("实验五完成。")
    sys.stdout.flush()

if __name__ == '__main__':
    main()
