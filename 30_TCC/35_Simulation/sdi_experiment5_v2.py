#!/usr/bin/env python3
"""
SDI 实验五 v2：神经雪崩SOC动力学验证

==============================================================================
v1问题诊断与修复
==============================================================================
v1问题：外部刺激P_EXT=0.3太强 → 网络99.2%步数有激活 → 无法检测雪崩边界
        真正的SOC应该：大部分时间沉寂 → BTW慢驱动触发 → 自发雪崩 → 回到沉寂

v2修复策略：
  1. 取消持续外部刺激，改用纯BTW慢驱动（每10步注入1个种子节点）
  2. 传播概率大幅降低（weight × 0.15 → 目标κ≈1.0）
  3. 用独立的"学习阶段"（有外部刺激）+ "雪崩记录阶段"（纯BTW驱动）
     - 阶段1（N_LEARN=8000步）：有外部刺激，让STDP+WS重连充分演化拓扑
     - 阶段2（N_RECORD=5000步）：仅BTW极慢驱动，记录纯自发雪崩

==============================================================================
理论背景
==============================================================================
Beggs & Plenz (2003) Science：神经雪崩的标准检测协议
  - 用 local field potential（LFP）时间分箱
  - 大部分时间箱活动为零（沉寂）
  - 雪崩：连续非零时间箱序列，前后均有零值帧
  - P(S) ~ S^{-τ}, τ ≈ 1.5（幂律尺寸分布）
  - 分支比 κ ≈ 1.0（每个激活神经元平均激活1个后继）

==============================================================================
文献依据
==============================================================================
  Beggs & Plenz 2003 J Neurosci — 神经雪崩原始发现，τ=1.5，κ=1.0
  Priesemann et al. 2014 PLOS CB — 雪崩分析方法，纯慢驱动协议
  Shew & Plenz 2013 Neuroscientist — 临界态综述，κ∈[0.9,1.1]
  Zapperi 1995 PRL — 平均场SOC，τ=3/2推导
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

# ============ 固定参数（与v17一致） ============
THETA_LTP = 65
THETA_LTD = 15
ETA_LTP = 0.012
ETA_LTD = 0.008
TAU_STDP = 20.0
T_DECAY = 400
EL_HI = 0.25
T_ABS = 3
T_REL = 8
REL_SCALE = 0.4
MAX_FIX = 8
P_REWIRE = 0.15
REWIRE_INT = 50
SCALING_INT = 100
KAPPA_TARGET = 0.95
SCALING_RATE = 0.05

# ============ 实验五v2特有参数 ============
N_LEARN = 8000       # 学习阶段（有外部刺激，演化拓扑）
N_RECORD = 8000      # 雪崩记录阶段（纯BTW驱动，记录雪崩）
N_STEPS = N_LEARN + N_RECORD
LOG_INT = 1000

# BTW驱动（Bak-Tang-Wiesenfeld极慢驱动）
BTW_DRIVE_INTERVAL = 10    # 每10步驱动一个种子（极慢驱动）
BTW_DRIVE_N = 1             # 每次激活1个神经元

# 传播概率衰减因子（降低以接近κ=1）
PROP_SCALE = 0.12           # 单神经元传播概率 = weight * PROP_SCALE

# 学习阶段刺激概率
P_EXT_LEARN = 0.25          # 学习阶段外部激活概率（强刺激，促进STDP学习）

# 竞争性修剪参数
PRUNE_INT = 200
PRUNE_WINDOW = 200
MIN_EDGES = 3
P_PRUNE = 0.05

SEEDS = [42, 7, 13]

# ============ 网络定义 ============
NETWORKS = {
    'C.elegans': {
        'N': 279, 'k_init': 8, 'p_init': 0.05, 'sf': 0.22,
        'level': 'neuron', 'K_PATTERNS': 8,
        'ref': 'Varshney 2011 PLOS CB'
    },
    'Human_HCP': {
        'N': 400, 'k_init': 10, 'p_init': 0.06, 'sf': 0.08,
        'level': 'mesoscale', 'K_PATTERNS': 12,
        'ref': 'Van Essen 2013 HCP'
    },
    'WS_Control': {
        'N': 279, 'k_init': 8, 'p_init': 0.15, 'sf': 0.22,
        'level': 'control', 'K_PATTERNS': 8,
        'ref': 'Watts & Strogatz 1998（对照）'
    }
}

# ============ 图初始化 ============
def make_ws_graph(N, k, p, seed):
    rng = np.random.default_rng(seed)
    adj = np.zeros((N, N), dtype=np.float32)
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
    try:
        threshold = 0.05
        edges = np.argwhere((adj + adj.T) / 2 > threshold)
        edges = edges[edges[:, 0] < edges[:, 1]]
        if len(edges) < 10:
            return 1.0
        adj_list = [[] for _ in range(N)]
        for u, v in edges:
            adj_list[u].append(v)
            adj_list[v].append(u)
        C_vals = []
        for i in range(min(50, N)):
            nbrs = adj_list[i]
            ki = len(nbrs)
            if ki < 2:
                C_vals.append(0.0)
                continue
            nbr_set = set(nbrs)
            links = sum(1 for a in nbrs for b in adj_list[a] if b in nbr_set and b != a)
            C_vals.append(links / (ki * (ki - 1)))
        C = float(np.mean(C_vals)) if C_vals else 0.0
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
        n, m = N, len(edges)
        k_avg = 2 * m / n
        if k_avg <= 1:
            return 1.0
        C_rand = k_avg / n
        L_rand = np.log(n) / np.log(k_avg)
        if C_rand == 0 or L_rand == 0:
            return 1.0
        return float((C / C_rand) / (L / L_rand))
    except:
        return 1.0

# ============ 幂律拟合（Hill MLE） ============
def fit_powerlaw(data):
    data = np.array([d for d in data if d > 0], dtype=float)
    if len(data) < 30:
        return None, None, len(data), 0.0
    
    # 扫描x_min候选
    candidates = np.unique(data)
    p25 = max(1, np.percentile(data, 20))
    p75 = np.percentile(data, 70)
    candidates = candidates[(candidates >= p25) & (candidates <= p75)]
    if len(candidates) == 0:
        candidates = [np.median(data)]
    
    best_ks = np.inf
    best_xmin = p25
    best_tau = 1.5
    
    for xm in candidates[:25]:
        tail = data[data >= xm]
        if len(tail) < 20:
            continue
        tau_est = 1 + len(tail) / np.sum(np.log(tail / xm))
        tail_sorted = np.sort(tail)
        n_t = len(tail_sorted)
        ecdf = np.arange(1, n_t + 1) / n_t
        tcdf = 1 - (tail_sorted / xm) ** (-(tau_est - 1))
        ks = np.max(np.abs(ecdf - tcdf))
        if ks < best_ks:
            best_ks = ks
            best_xmin = xm
            best_tau = tau_est
    
    x_min = best_xmin
    tail = data[data >= x_min]
    n_tail = len(tail)
    if n_tail < 15:
        return None, x_min, n_tail, 0.0
    
    tau = float(best_tau)
    
    # R²（log-log bin拟合）
    bins = min(25, max(5, n_tail // 5))
    counts, edges = np.histogram(tail, bins=bins)
    centers = (edges[:-1] + edges[1:]) / 2
    mask = counts > 0
    if mask.sum() < 4:
        return tau, x_min, n_tail, 0.0
    log_x = np.log(centers[mask])
    log_y = np.log(counts[mask])
    coeffs = np.polyfit(log_x, log_y, 1)
    fitted = np.polyval(coeffs, log_x)
    ss_res = np.sum((log_y - fitted) ** 2)
    ss_tot = np.sum((log_y - np.mean(log_y)) ** 2)
    r2 = float(1 - ss_res / ss_tot) if ss_tot > 0 else 0.0
    
    return tau, float(x_min), n_tail, r2

# ============ 雪崩检测 ============
def detect_avalanches(activation_series):
    arr = np.array(activation_series, dtype=int)
    sizes, durations = [], []
    in_av = False
    cur_size = 0
    cur_dur = 0
    for n in arr:
        if n > 0:
            in_av = True
            cur_size += n
            cur_dur += 1
        else:
            if in_av:
                sizes.append(cur_size)
                durations.append(cur_dur)
                in_av = False
                cur_size = 0
                cur_dur = 0
    if in_av:
        sizes.append(cur_size)
        durations.append(cur_dur)
    return sizes, durations

# ============ 分支比（Priesemann 2014方法） ============
def compute_branching_ratio(activation_series):
    """
    κ = Σ(n_{t+1}) / Σ(n_t)，对所有非零n_t步骤求和
    Priesemann 2014 PLOS CB eq. 2
    """
    arr = np.array(activation_series, dtype=float)
    numerator = arr[1:][arr[:-1] > 0].sum()
    denominator = arr[:-1][arr[:-1] > 0].sum()
    if denominator == 0:
        return 0.0
    return float(numerator / denominator)

# ============ 1/f 功率谱 ============
def compute_psd_slope(activation_series):
    arr = np.array(activation_series, dtype=float)
    arr = arr - arr.mean()
    n = len(arr)
    fft_vals = np.fft.rfft(arr)
    power = np.abs(fft_vals) ** 2
    freqs = np.fft.rfftfreq(n)
    mask = (freqs > 0.002) & (freqs < 0.3)
    if mask.sum() < 20:
        return 0.0, 0.0
    log_f = np.log(freqs[mask])
    log_p = np.log(power[mask] + 1e-10)
    coeffs = np.polyfit(log_f, log_p, 1)
    fitted = np.polyval(coeffs, log_f)
    ss_res = np.sum((log_p - fitted) ** 2)
    ss_tot = np.sum((log_p - np.mean(log_p)) ** 2)
    r2 = float(1 - ss_res / ss_tot) if ss_tot > 0 else 0.0
    return float(coeffs[0]), r2

# ============ 主仿真 ============
def run_simulation(net_name, net_cfg, seed, use_pruning=False):
    N = net_cfg['N']
    sf = net_cfg['sf']
    K_PATTERNS = net_cfg['K_PATTERNS']
    
    rng = np.random.default_rng(seed)
    
    adj = make_ws_graph(N, net_cfg['k_init'], net_cfg['p_init'], seed)
    el_mask = (rng.random((N, N)) < 0.05).astype(bool)
    el_mask &= (adj > 0)
    nltp = np.zeros((N, N), dtype=np.int16)
    nltd = np.zeros((N, N), dtype=np.int16)
    el_age = np.zeros((N, N), dtype=np.int32)
    refrac = np.zeros(N, dtype=np.int8)
    
    # 学习阶段刺激模式
    stim_size = max(1, int(N * sf))
    rng_pat = np.random.default_rng(seed + 1000)
    patterns = [rng_pat.choice(N, size=stim_size, replace=False).tolist()
                for _ in range(K_PATTERNS)]
    
    # 记录变量
    topology_log = []
    activation_series = []   # 仅记录阶段
    
    t_start = time.time()
    pat_idx = 0
    
    for step in range(N_STEPS):
        is_learning = (step < N_LEARN)
        is_recording = (step >= N_LEARN)
        
        active = np.zeros(N, dtype=bool)
        
        if is_learning:
            # 学习阶段：使用外部刺激协议（让STDP演化拓扑）
            if step % 10 == 0:
                if rng.random() < 0.1:
                    pat_idx = int(rng.integers(K_PATTERNS))
            stim_neurons = patterns[pat_idx % K_PATTERNS]
            for ni in stim_neurons:
                if refrac[ni] == 0 and rng.random() < P_EXT_LEARN:
                    active[ni] = True
        else:
            # 记录阶段：纯BTW极慢驱动（每BTW_DRIVE_INTERVAL步激活1个随机神经元）
            if (step - N_LEARN) % BTW_DRIVE_INTERVAL == 0:
                drive_idx = int(rng.integers(N))
                if refrac[drive_idx] == 0:
                    active[drive_idx] = True
        
        # 级联传播（单步，不循环——雪崩通过时序自然展开）
        if active.any():
            n_trigger = int(active.sum())
            prev_wave = active.copy()
            all_act = active.copy()
            
            for _cascade in range(12):  # 最多12步级联
                if not prev_wave.any():
                    break
                new_wave = np.zeros(N, dtype=bool)
                for i in np.where(prev_wave)[0]:
                    w_row = adj[i, :]
                    w_row_el = w_row.copy()
                    w_row_el[el_mask[i, :]] *= 1.2
                    cands = np.where(w_row_el > 0.08)[0]
                    for c in cands:
                        if refrac[c] == 0 and not all_act[c]:
                            # 激活概率 = weight * PROP_SCALE
                            if rng.random() < w_row_el[c] * PROP_SCALE:
                                new_wave[c] = True
                new_wave &= ~all_act
                all_act |= new_wave
                prev_wave = new_wave
                if not new_wave.any():
                    break
            
            active = all_act
        
        n_active_curr = int(active.sum())
        
        # 更新不应期
        refrac[active] = T_ABS + T_REL
        refrac[refrac > 0] -= 1
        
        # STDP更新（学习阶段强化，记录阶段弱化）
        active_idx = np.where(active)[0]
        if len(active_idx) >= 2:
            n_pairs = min(len(active_idx) * 2, 150) if is_learning else min(len(active_idx), 50)
            pre_idx = rng.choice(active_idx, size=n_pairs)
            post_idx = rng.choice(active_idx, size=n_pairs)
            for pre, post in zip(pre_idx, post_idx):
                if pre == post:
                    continue
                if adj[pre, post] > 0:
                    delta_t = int(rng.integers(1, 30))
                    dw = ETA_LTP * np.exp(-delta_t / TAU_STDP)
                    adj[pre, post] = min(1.0, adj[pre, post] + dw)
                    nltp[pre, post] += 1
                if adj[post, pre] > 0:
                    dw_ltd = ETA_LTD * np.exp(-delta_t / TAU_STDP)
                    adj[post, pre] = max(0.0, adj[post, pre] - dw_ltd)
                    nltd[post, pre] += 1
        
        # STDP固化/消除
        ltp_mask = (nltp >= THETA_LTP) & (adj > 0) & (~el_mask)
        n_el = el_mask.sum()
        el_ratio = n_el / max(1, (adj > 0).sum())
        if el_ratio < EL_HI:
            el_mask[ltp_mask] = True
            nltp[ltp_mask] = 0
        
        ltd_mask = (nltd >= THETA_LTD) & (adj > 0) & (~el_mask)
        adj[ltd_mask] = 0.0
        nltp[ltd_mask] = 0
        nltd[ltd_mask] = 0
        
        el_age[el_mask] += 1
        decay_mask = el_mask & (el_age > T_DECAY)
        el_mask[decay_mask] = False
        el_age[decay_mask] = 0
        
        # WS重连（每REWIRE_INT步）
        if step % REWIRE_INT == 0:
            n_rewire = max(1, int((adj > 0).sum() * P_REWIRE * 0.01))
            non_el = np.argwhere((adj > 0) & (~el_mask))
            for _ in range(min(n_rewire, len(non_el))):
                idx = int(rng.integers(len(non_el)))
                i, j = non_el[idx]
                k_new = int(rng.integers(N))
                if k_new != i and adj[i, k_new] == 0:
                    adj[i, k_new] = adj[i, j]
                    nltp[i, k_new] = nltp[i, j] = 0
                    nltd[i, k_new] = nltd[i, j] = 0
                    adj[i, j] = 0.0
        
        # 突触缩放（每SCALING_INT步，仅学习阶段）
        if is_learning and step % SCALING_INT == 0 and n_active_curr > 0:
            act_rate = n_active_curr / N
            if act_rate > KAPPA_TARGET:
                adj[~el_mask] *= (1 - SCALING_RATE)
            elif act_rate < KAPPA_TARGET * 0.5:
                adj[~el_mask] *= (1 + SCALING_RATE)
            adj = np.clip(adj, 0.0, 1.0)
        
        # 竞争性修剪（仅实验5b）
        if use_pruning and step % PRUNE_INT == 0 and step > 0:
            inactive_mask = (adj > 0) & (~el_mask) & (nltp == 0) & (nltd == 0)
            degree = (adj > 0).sum(axis=1)
            for i in range(N):
                if degree[i] <= MIN_EDGES:
                    inactive_mask[i, :] = False
            for i, j in np.argwhere(inactive_mask):
                if rng.random() < P_PRUNE:
                    adj[i, j] = 0.0
                    nltp[i, j] = nltd[i, j] = 0
            nltp[:] = 0
            nltd[:] = 0
        
        # 记录雪崩激活序列（记录阶段）
        if is_recording:
            activation_series.append(n_active_curr)
        
        # 拓扑日志
        if step % LOG_INT == 0:
            sigma = compute_sigma_fast(adj, N)
            n_edges = int((adj > 0).sum())
            n_el_curr = int(el_mask.sum())
            phase = "学习" if is_learning else "记录"
            print(f"  [{net_name}|seed={seed}|{'4r' if use_pruning else '3r'}|{phase}] "
                  f"step={step}/{N_STEPS} | σ={sigma:.2f} | edges={n_edges} | "
                  f"active={n_active_curr} | t={time.time()-t_start:.0f}s")
            sys.stdout.flush()
            topology_log.append({
                'step': step,
                'sigma': sigma,
                'n_edges': n_edges,
                'n_el': n_el_curr,
                'n_active': n_active_curr,
                'phase': phase
            })
    
    # ============ 雪崩分析 ============
    arr = np.array(activation_series)
    zero_frac = float((arr == 0).mean())
    
    print(f"\n  激活统计 [{net_name}|seed={seed}]:")
    print(f"    总记录步数: {len(arr)}")
    print(f"    零值帧比例: {zero_frac:.1%}")
    print(f"    平均激活数: {arr.mean():.2f}")
    print(f"    最大激活数: {arr.max()}")
    
    sizes, durations = detect_avalanches(activation_series)
    tau_size, xmin_size, n_tail_size, r2_size = fit_powerlaw(sizes)
    tau_dur, xmin_dur, n_tail_dur, r2_dur = fit_powerlaw(durations)
    kappa = compute_branching_ratio(activation_series)
    psd_slope, psd_r2 = compute_psd_slope(activation_series)
    
    n_avalanches = len(sizes)
    
    # 达标判定
    size_ok = (tau_size is not None and 1.2 <= tau_size <= 2.0 and r2_size > 0.75)
    dur_ok = (tau_dur is not None and 1.5 <= tau_dur <= 2.5 and r2_dur > 0.75)
    kappa_ok = (0.9 <= kappa <= 1.1)
    count_ok = (n_avalanches >= 200)
    psd_ok = (psd_slope is not None and -1.5 <= psd_slope <= -0.3)
    zero_ok = (zero_frac >= 0.3)  # 至少30%零值帧（有真正沉寂期）
    
    score_items = [size_ok, dur_ok, kappa_ok, count_ok, psd_ok, zero_ok]
    score = sum(score_items)
    
    tau_s_str = f"{tau_size:.3f}" if tau_size is not None else "N/A"
    tau_d_str = f"{tau_dur:.3f}" if tau_dur is not None else "N/A"
    psd_str = f"{psd_slope:.3f}" if psd_slope is not None else "N/A"
    
    print(f"\n{'='*60}")
    print(f"  结果 [{net_name}|seed={seed}|{'4-rules' if use_pruning else '3-rules'}]")
    print(f"  零值帧比例: {zero_frac:.1%} {'✓' if zero_ok else '✗'}")
    print(f"  雪崩数: {n_avalanches} {'✓' if count_ok else '✗'}")
    print(f"  τ_size={tau_s_str} (R²={r2_size:.3f}) {'✓' if size_ok else '✗'}")
    print(f"  τ_dur={tau_d_str} (R²={r2_dur:.3f}) {'✓' if dur_ok else '✗'}")
    print(f"  κ(分支比)={kappa:.3f} {'✓' if kappa_ok else '✗'}")
    print(f"  PSD斜率={psd_str} (R²={psd_r2:.3f}) {'✓' if psd_ok else '✗'}")
    print(f"  得分: {score}/6")
    print(f"  {'='*60}\n")
    sys.stdout.flush()
    
    return {
        'network': net_name, 'seed': seed,
        'rules': '4-rules' if use_pruning else '3-rules',
        'zero_fraction': float(zero_frac),
        'n_avalanches': n_avalanches,
        'tau_size': float(tau_size) if tau_size is not None else None,
        'r2_size': float(r2_size),
        'tau_duration': float(tau_dur) if tau_dur is not None else None,
        'r2_duration': float(r2_dur),
        'branching_ratio': float(kappa),
        'psd_slope': float(psd_slope) if psd_slope is not None else None,
        'psd_r2': float(psd_r2),
        'score': int(score),
        'criteria': {
            'zero_frames': bool(zero_ok),
            'size_powerlaw': bool(size_ok),
            'duration_powerlaw': bool(dur_ok),
            'branching_ratio': bool(kappa_ok),
            'avalanche_count': bool(count_ok),
            'psd_1f': bool(psd_ok)
        },
        'topology_log': topology_log,
        'activation_sample': [int(x) for x in activation_series[:3000]],
        'sizes_sample': sorted([int(s) for s in sizes])[:500],
        'durations_sample': sorted([int(d) for d in durations])[:500],
    }

# ============ 绘图 ============
def plot_results(all_results):
    fig = plt.figure(figsize=(20, 20))
    fig.suptitle(
        'SDI 实验五 v2：神经雪崩SOC动力学验证（两阶段协议）\n'
        'P(S)~S^{-τ}，τ≈1.5；κ≈1.0（临界点）；1/f功率谱',
        fontsize=13, fontweight='bold', y=0.98
    )
    gs = GridSpec(4, 3, figure=fig, hspace=0.45, wspace=0.35)
    
    # 选取代表性结果（每个网络取最高分种子）
    from collections import defaultdict
    by_net = defaultdict(list)
    for r in all_results:
        by_net[r['network']+'_'+r['rules']].append(r)
    
    best_per_group = {}
    for k, v in by_net.items():
        best_per_group[k] = max(v, key=lambda x: x['score'])
    
    plot_keys = sorted(best_per_group.keys())[:4]
    colors = {'3-rules': '#2196F3', '4-rules': '#E91E63'}
    
    for pi, key in enumerate(plot_keys):
        res = best_per_group[key]
        row = pi // 2
        col_base = (pi % 2) * 1 + pi % 2  # 每行2个
        color = colors.get(res['rules'], '#333')
        
        # 激活序列
        ax1 = fig.add_subplot(gs[row * 2, pi % 2])
        act = res.get('activation_sample', [])
        if act:
            ax1.plot(act[:1000], color=color, linewidth=0.6, alpha=0.8)
        zero_frac = res.get('zero_fraction', 0)
        ax1.set_title(f"{res['network']}\n{res['rules']} | 零值帧{zero_frac:.0%}",
                     fontsize=8, color='green' if zero_frac >= 0.3 else 'red')
        ax1.set_xlabel('步数（记录阶段）', fontsize=6)
        ax1.set_ylabel('激活数', fontsize=6)
        ax1.tick_params(labelsize=6)
        
        # 雪崩尺寸分布（log-log）
        ax2 = fig.add_subplot(gs[row * 2 + 1, pi % 2])
        sizes = res.get('sizes_sample', [])
        if sizes and len(sizes) > 10:
            sizes_arr = np.array(sizes)
            bins = np.logspace(np.log10(max(1, sizes_arr.min())),
                              np.log10(max(sizes_arr.max(), 2)), 25)
            counts, edges = np.histogram(sizes_arr, bins=bins)
            centers = (edges[:-1] + edges[1:]) / 2
            mask = counts > 0
            if mask.sum() > 3:
                ax2.loglog(centers[mask], counts[mask], 'o', color=color,
                          markersize=4, alpha=0.7, label='数据')
                x_theory = np.logspace(np.log10(centers[mask][0]),
                                       np.log10(centers[mask][-1]), 50)
                y0 = counts[mask][0]
                ax2.loglog(x_theory, y0 * (x_theory[0] / x_theory) ** 0.5,
                          '--', color='gray', alpha=0.5, label='τ=1.5')
        tau_s = res.get('tau_size')
        r2_s = res.get('r2_size', 0)
        tau_s_str = f"{tau_s:.2f}" if tau_s is not None else "N/A"
        size_ok = res['criteria'].get('size_powerlaw', False)
        ax2.set_title(f"τ_size={tau_s_str}, R²={r2_s:.2f} {'✓' if size_ok else '✗'}",
                     fontsize=8, color='green' if size_ok else 'red')
        ax2.set_xlabel('雪崩尺寸 S', fontsize=6)
        ax2.set_ylabel('频率', fontsize=6)
        ax2.tick_params(labelsize=6)
        ax2.legend(fontsize=5)
    
    plt.savefig(f'{OUT}/exp5_v2_avalanche_results.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✅ 图表已保存: {OUT}/exp5_v2_avalanche_results.png")

# ============ 主程序 ============
def main():
    print("=" * 70)
    print("SDI 实验五 v2：神经雪崩SOC动力学验证（两阶段协议）")
    print("阶段1（学习）: 外部刺激驱动STDP演化拓扑")
    print("阶段2（记录）: 纯BTW极慢驱动，检测自发神经雪崩")
    print(f"  τ(尺寸)目标：[1.2, 2.0]  理论值：1.5")
    print(f"  τ(持续)目标：[1.5, 2.5]  理论值：2.0")
    print(f"  κ(分支比)目标：[0.9, 1.1]  临界点：1.0")
    print(f"  PSD斜率目标：[-1.5, -0.3]  1/f噪声：≈-1.0")
    print(f"  零值帧比例：≥30%（有效沉寂期）")
    print(f"  雪崩数量：≥200")
    print("=" * 70)
    print(f"学习阶段：{N_LEARN}步 | 记录阶段：{N_RECORD}步")
    print(f"BTW驱动间隔：{BTW_DRIVE_INTERVAL}步（每{BTW_DRIVE_INTERVAL}步激活1个神经元）")
    print(f"传播概率系数：{PROP_SCALE}")
    print("=" * 70)
    sys.stdout.flush()
    
    all_results = []
    t_total = time.time()
    
    for rules_label, use_pruning in [('3-rules', False), ('4-rules', True)]:
        print(f"\n【实验5a {'3' if not use_pruning else '4'}规则体系】")
        for net_name, net_cfg in NETWORKS.items():
            for seed in SEEDS:
                print(f"\n→ 运行: {net_name} | seed={seed} | {rules_label}")
                sys.stdout.flush()
                try:
                    result = run_simulation(net_name, net_cfg, seed, use_pruning)
                    all_results.append(result)
                except Exception as e:
                    print(f"  ❌ 异常: {e}")
                    import traceback; traceback.print_exc()
    
    # 保存结果
    def serialize(obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, bool):
            return bool(obj)
        return obj
    
    def deep_serialize(obj):
        if isinstance(obj, dict):
            return {k: deep_serialize(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [deep_serialize(v) for v in obj]
        return serialize(obj)
    
    out_path = f'{OUT}/exp5_v2_avalanche_results.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(deep_serialize(all_results), f, ensure_ascii=False, indent=2)
    print(f"\n✅ 结果已保存: {out_path}")
    
    try:
        plot_results(all_results)
    except Exception as e:
        print(f"  ⚠️ 绘图失败: {e}")
    
    # ============ 汇总报告 ============
    print("\n" + "=" * 70)
    print("实验五v2汇总")
    print("=" * 70)
    
    from collections import defaultdict
    group_stats = defaultdict(list)
    for r in all_results:
        key = f"{r['network']}_{r['rules']}"
        group_stats[key].append(r)
    
    print(f"\n{'网络+规则':<28} {'零帧%':<8} {'雪崩数':<8} {'τ_sz':<8} {'τ_du':<8} {'κ':<8} {'PSD':<8} {'得分':<6}")
    print("-" * 82)
    
    for key, runs in sorted(group_stats.items()):
        zf = np.mean([r['zero_fraction'] for r in runs])
        n_avl = np.mean([r['n_avalanches'] for r in runs])
        tau_s = [r['tau_size'] for r in runs if r['tau_size'] is not None]
        tau_d = [r['tau_duration'] for r in runs if r['tau_duration'] is not None]
        kv = [r['branching_ratio'] for r in runs]
        pv = [r['psd_slope'] for r in runs if r['psd_slope'] is not None]
        sv = [r['score'] for r in runs]
        
        ts = f"{np.mean(tau_s):.2f}" if tau_s else "N/A"
        td = f"{np.mean(tau_d):.2f}" if tau_d else "N/A"
        ks = f"{np.mean(kv):.3f}"
        ps = f"{np.mean(pv):.2f}" if pv else "N/A"
        sc = f"{np.mean(sv):.1f}/6"
        
        print(f"{key:<28} {zf:.0%}  {n_avl:<8.0f} {ts:<8} {td:<8} {ks:<8} {ps:<8} {sc:<6}")
    
    print("\n" + "=" * 70)
    best = max(all_results, key=lambda x: x['score'])
    tau_s_str = f"{best['tau_size']:.2f}" if best['tau_size'] is not None else "N/A"
    print(f"\n最佳结果: {best['network']} | {best['rules']} | seed={best['seed']}")
    print(f"  τ_size={tau_s_str}, κ={best['branching_ratio']:.3f}, "
          f"得分={best['score']}/6")
    
    elapsed_total = time.time() - t_total
    print(f"\n总耗时: {elapsed_total:.0f}s ({elapsed_total/60:.1f}min)")
    print("实验五v2完成。")
    sys.stdout.flush()

if __name__ == '__main__':
    main()
