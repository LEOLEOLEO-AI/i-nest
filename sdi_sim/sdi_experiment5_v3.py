#!/usr/bin/env python3
"""
SDI 实验五 v3：神经雪崩SOC动力学验证

==============================================================================
v2问题诊断与修复
==============================================================================
v2问题：
  - 传播概率太低（PROP_SCALE=0.12 × weight≈0.15 ≈ 0.018），
    几乎每次BTW注入后无传播 → 雪崩全部size=1 → κ=0
  - 解决：在记录阶段前做"临界点校准"——
    自动调整全局增益因子G，使平均分支比κ≈1.0

v3核心改进：
  1. 学习阶段完成后，校准传播增益 G
     → 二分法找到使κ∈[0.9, 1.1]的最优G值
  2. 记录阶段使用校准后的G进行传播
  3. BTW驱动频率提高（每5步驱动1次），增加雪崩总数
  4. 雪崩检测：使用连续非零激活帧定义

==============================================================================
SOC临界点校准方法（Priesemann 2014）
==============================================================================
记录阶段前：
  1. 用100步短测试序列估计当前κ值
  2. 若κ<0.8：增大G；若κ>1.2：减小G
  3. 重复直到κ∈[0.9, 1.1]（最多20次迭代）
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

# ============ 固定参数 ============
THETA_LTP = 65
THETA_LTD = 15
ETA_LTP = 0.012
ETA_LTD = 0.008
TAU_STDP = 20.0
T_DECAY = 400
EL_HI = 0.25
T_ABS = 3
T_REL = 8
P_REWIRE = 0.15
REWIRE_INT = 50
SCALING_INT = 100
KAPPA_TARGET = 0.95
SCALING_RATE = 0.05

# ============ 实验五v3特有参数 ============
N_LEARN = 8000        # 学习阶段（外部刺激，STDP演化）
N_RECORD = 10000      # 雪崩记录阶段（BTW驱动）
N_STEPS = N_LEARN + N_RECORD
LOG_INT = 2000

# BTW驱动
BTW_INTERVAL = 5      # 每5步驱动一次（更频繁，增加雪崩数）
BTW_N = 1             # 每次驱动1个节点

# 临界点校准参数
CALIB_STEPS = 500     # 每次校准测试500步
CALIB_ITER = 25       # 最多25次校准迭代
G_INIT = 1.0          # 初始增益
G_LO = 0.1
G_HI = 10.0

# 修剪参数
PRUNE_INT = 200
P_PRUNE = 0.05
MIN_EDGES = 3

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
        'ref': 'WS 1998 对照'
    }
}

# ============ 图初始化 ============
def make_ws_adj(N, k, p, seed):
    rng = np.random.default_rng(seed)
    adj = np.zeros((N, N), dtype=np.float32)
    for i in range(N):
        for dj in range(1, k // 2 + 1):
            j = (i + dj) % N
            if rng.random() < (1 - p):
                w = float(rng.uniform(0.05, 0.3))
                adj[i, j] = w
                adj[j, i] = w
            else:
                k2 = int(rng.integers(N))
                while k2 == i:
                    k2 = int(rng.integers(N))
                w = float(rng.uniform(0.05, 0.3))
                adj[i, k2] = w
                adj[k2, i] = w
    return adj

# ============ 网络度量 ============
def compute_sigma_fast(adj, N):
    try:
        edges = np.argwhere((adj + adj.T) / 2 > 0.05)
        edges = edges[edges[:, 0] < edges[:, 1]]
        if len(edges) < 10:
            return 1.0
        al = [[] for _ in range(N)]
        for u, v in edges:
            al[u].append(v)
            al[v].append(u)
        Cv = []
        for i in range(min(40, N)):
            nb = al[i]
            ki = len(nb)
            if ki < 2:
                Cv.append(0.0)
                continue
            s = set(nb)
            lk = sum(1 for a in nb for b in al[a] if b in s and b != a)
            Cv.append(lk / (ki * (ki - 1)))
        C = float(np.mean(Cv)) if Cv else 0.0
        lengths = []
        for start in range(min(25, N)):
            vis = {start: 0}
            q = [start]
            qi = 0
            while qi < len(q):
                nd = q[qi]; qi += 1
                d = vis[nd]
                if d >= 6:
                    continue
                for nb in al[nd]:
                    if nb not in vis:
                        vis[nb] = d + 1
                        q.append(nb)
            lengths.extend(vis.values())
        L = float(np.mean(lengths)) if lengths else 3.0
        m = len(edges)
        k_avg = 2 * m / N
        if k_avg <= 1:
            return 1.0
        C_rand = k_avg / N
        L_rand = np.log(N) / np.log(k_avg)
        if C_rand == 0 or L_rand == 0:
            return 1.0
        return float((C / C_rand) / (L / L_rand))
    except:
        return 1.0

# ============ 单步传播（可配增益G） ============
def propagate_one_step(adj, el_mask, active_in, refrac, N, G, rng):
    """
    从active_in出发，单步传播（不循环级联）。
    每个发送者i向邻居c发送激活，概率 = adj[i,c]*G（E-L键×1.2）。
    返回：总激活集合（输入+新激活）
    """
    new_active = np.zeros(N, dtype=bool)
    all_active = active_in.copy()
    
    for i in np.where(active_in)[0]:
        w_row = adj[i, :] * G
        w_row_el = w_row.copy()
        w_row_el[el_mask[i, :]] *= 1.2
        candidates = np.where(w_row_el > 0.01)[0]
        for c in candidates:
            if refrac[c] == 0 and not all_active[c]:
                if rng.random() < min(w_row_el[c], 0.95):
                    new_active[c] = True
    
    all_active |= new_active
    return all_active, new_active

# ============ 估计分支比κ（短测试） ============
def estimate_kappa(adj, el_mask, N, G, rng_seed, n_test=300):
    """
    用BTW驱动n_test步，估计分支比κ
    κ = Σ(下一步激活数) / Σ(当前步激活数)，对非零步求和
    """
    rng = np.random.default_rng(rng_seed)
    refrac = np.zeros(N, dtype=np.int8)
    
    numerator = 0.0
    denominator = 0.0
    
    for step in range(n_test):
        active = np.zeros(N, dtype=bool)
        if step % BTW_INTERVAL == 0:
            d = int(rng.integers(N))
            if refrac[d] == 0:
                active[d] = True
        
        if active.any():
            n_trigger = int(active.sum())
            # 单步传播
            _, new_act = propagate_one_step(adj, el_mask, active, refrac, N, G, rng)
            n_prop = int(new_act.sum())
            if n_trigger > 0:
                numerator += n_prop
                denominator += n_trigger
        
        # 合并激活并更新不应期
        all_act = active.copy()
        all_act |= np.zeros(N, dtype=bool)  # placeholder
        refrac[all_act] = T_ABS
        refrac[refrac > 0] -= 1
    
    if denominator == 0:
        return 0.0
    return float(numerator / denominator)

# ============ 校准临界增益G ============
def calibrate_G(adj, el_mask, N, seed):
    """
    二分法找到使κ∈[0.9, 1.1]的增益G
    """
    G_lo = G_LO
    G_hi = G_HI
    G_best = G_INIT
    
    for i in range(CALIB_ITER):
        G_mid = (G_lo + G_hi) / 2
        kappa = estimate_kappa(adj, el_mask, N, G_mid, seed + i * 1000)
        print(f"    校准 iter={i+1}: G={G_mid:.4f} → κ={kappa:.4f}")
        sys.stdout.flush()
        
        if 0.90 <= kappa <= 1.10:
            G_best = G_mid
            print(f"    ✅ 校准成功: G={G_best:.4f}, κ={kappa:.4f}")
            return G_best, kappa
        
        if kappa < 0.90:
            G_lo = G_mid  # 需要更大的G
        else:
            G_hi = G_mid  # 需要更小的G
        
        if G_hi - G_lo < 0.001:
            G_best = G_mid
            break
        
        G_best = G_mid
    
    kappa_final = estimate_kappa(adj, el_mask, N, G_best, seed + 99999)
    print(f"    ⚠️ 校准结束: G={G_best:.4f}, κ={kappa_final:.4f}")
    return G_best, kappa_final

# ============ 雪崩检测 ============
def detect_avalanches(activation_series):
    arr = np.array(activation_series, dtype=int)
    sizes, durations = [], []
    in_av = False
    cur_s = 0
    cur_d = 0
    for n in arr:
        if n > 0:
            in_av = True
            cur_s += n
            cur_d += 1
        else:
            if in_av:
                sizes.append(cur_s)
                durations.append(cur_d)
                in_av = False
                cur_s = 0
                cur_d = 0
    if in_av:
        sizes.append(cur_s)
        durations.append(cur_d)
    return sizes, durations

# ============ 幂律拟合 ============
def fit_powerlaw(data):
    data = np.array([d for d in data if d > 0], dtype=float)
    if len(data) < 30:
        return None, None, len(data), 0.0
    
    p20 = max(1, np.percentile(data, 20))
    p70 = np.percentile(data, 70)
    cands = np.unique(data)
    cands = cands[(cands >= p20) & (cands <= p70)]
    if len(cands) == 0:
        cands = [np.median(data)]
    
    best_ks = np.inf
    best_xmin = p20
    best_tau = 1.5
    
    for xm in cands[:30]:
        tail = data[data >= xm]
        if len(tail) < 15:
            continue
        log_ratio = np.log(tail / xm)
        if log_ratio.sum() == 0:
            continue
        tau_e = 1 + len(tail) / log_ratio.sum()
        ts = np.sort(tail)
        n_t = len(ts)
        ecdf = np.arange(1, n_t + 1) / n_t
        tcdf = 1 - (ts / xm) ** (-(tau_e - 1))
        ks = np.max(np.abs(ecdf - tcdf))
        if ks < best_ks:
            best_ks = ks
            best_xmin = xm
            best_tau = tau_e
    
    tail = data[data >= best_xmin]
    n_tail = len(tail)
    if n_tail < 10:
        return None, best_xmin, n_tail, 0.0
    
    tau = float(best_tau)
    bins = min(20, max(5, n_tail // 8))
    counts, edges = np.histogram(tail, bins=bins)
    centers = (edges[:-1] + edges[1:]) / 2
    mask = counts > 0
    if mask.sum() < 4:
        return tau, float(best_xmin), n_tail, 0.0
    log_x = np.log(centers[mask])
    log_y = np.log(counts[mask])
    coeffs = np.polyfit(log_x, log_y, 1)
    fitted = np.polyval(coeffs, log_x)
    ss_res = np.sum((log_y - fitted) ** 2)
    ss_tot = np.sum((log_y - np.mean(log_y)) ** 2)
    r2 = float(1 - ss_res / ss_tot) if ss_tot > 0 else 0.0
    
    return tau, float(best_xmin), n_tail, r2

# ============ 分支比（Priesemann 2014） ============
def compute_branching_ratio(activation_series):
    arr = np.array(activation_series, dtype=float)
    num = arr[1:][arr[:-1] > 0].sum()
    den = arr[:-1][arr[:-1] > 0].sum()
    if den == 0:
        return 0.0
    return float(num / den)

# ============ 1/f 功率谱 ============
def compute_psd_slope(activation_series):
    arr = np.array(activation_series, dtype=float)
    arr = arr - arr.mean()
    n = len(arr)
    power = np.abs(np.fft.rfft(arr)) ** 2
    freqs = np.fft.rfftfreq(n)
    mask = (freqs > 0.002) & (freqs < 0.3)
    if mask.sum() < 15:
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
    
    # 初始化网络
    adj = make_ws_adj(N, net_cfg['k_init'], net_cfg['p_init'], seed)
    el_mask = (rng.random((N, N)) < 0.05).astype(bool)
    el_mask &= (adj > 0)
    nltp = np.zeros((N, N), dtype=np.int16)
    nltd = np.zeros((N, N), dtype=np.int16)
    el_age = np.zeros((N, N), dtype=np.int32)
    refrac = np.zeros(N, dtype=np.int8)
    
    # 刺激模式
    stim_size = max(1, int(N * sf))
    rng_pat = np.random.default_rng(seed + 1000)
    patterns = [rng_pat.choice(N, size=stim_size, replace=False).tolist()
                for _ in range(K_PATTERNS)]
    
    topology_log = []
    t0 = time.time()
    pat_idx = 0
    
    # ===== 阶段1：学习（8000步，外部刺激 + STDP） =====
    print(f"  [{net_name}|seed={seed}] 学习阶段开始（{N_LEARN}步）...")
    sys.stdout.flush()
    
    for step in range(N_LEARN):
        active = np.zeros(N, dtype=bool)
        
        # 外部刺激
        if step % 10 == 0 and rng.random() < 0.1:
            pat_idx = int(rng.integers(K_PATTERNS))
        for ni in patterns[pat_idx % K_PATTERNS]:
            if refrac[ni] == 0 and rng.random() < 0.28:
                active[ni] = True
        
        # 级联传播（学习阶段用G=1.0，固定）
        if active.any():
            prev_wave = active.copy()
            all_act = active.copy()
            for _ in range(10):
                if not prev_wave.any():
                    break
                new_wave = np.zeros(N, dtype=bool)
                for i in np.where(prev_wave)[0]:
                    w = adj[i, :].copy()
                    w[el_mask[i, :]] *= 1.2
                    for c in np.where(w > 0.08)[0]:
                        if refrac[c] == 0 and not all_act[c]:
                            if rng.random() < w[c] * 0.15:
                                new_wave[c] = True
                new_wave &= ~all_act
                all_act |= new_wave
                prev_wave = new_wave
                if not new_wave.any():
                    break
            active = all_act
        
        n_act = int(active.sum())
        refrac[active] = T_ABS + T_REL
        refrac[refrac > 0] -= 1
        
        # STDP
        aidx = np.where(active)[0]
        if len(aidx) >= 2:
            n_p = min(len(aidx) * 2, 120)
            pre_arr = rng.choice(aidx, size=n_p)
            post_arr = rng.choice(aidx, size=n_p)
            for pre, post in zip(pre_arr, post_arr):
                if pre == post:
                    continue
                dt = int(rng.integers(1, 30))
                if adj[pre, post] > 0:
                    adj[pre, post] = min(1.0, adj[pre, post] + ETA_LTP * np.exp(-dt / TAU_STDP))
                    nltp[pre, post] += 1
                if adj[post, pre] > 0:
                    adj[post, pre] = max(0.0, adj[post, pre] - ETA_LTD * np.exp(-dt / TAU_STDP))
                    nltd[post, pre] += 1
        
        # 固化/消除
        el_ratio = el_mask.sum() / max(1, (adj > 0).sum())
        el_mask[(nltp >= THETA_LTP) & (adj > 0) & (~el_mask) & (el_ratio < EL_HI)] = True
        ltd_m = (nltd >= THETA_LTD) & (adj > 0) & (~el_mask)
        adj[ltd_m] = 0.0
        nltp[ltd_m] = nltd[ltd_m] = 0
        el_age[el_mask] += 1
        decay_m = el_mask & (el_age > T_DECAY)
        el_mask[decay_m] = False
        el_age[decay_m] = 0
        
        # WS重连
        if step % REWIRE_INT == 0:
            non_el = np.argwhere((adj > 0) & (~el_mask))
            n_r = max(1, int(len(non_el) * P_REWIRE * 0.01))
            for _ in range(min(n_r, len(non_el))):
                idx = int(rng.integers(len(non_el)))
                i, j = non_el[idx]
                kn = int(rng.integers(N))
                if kn != i and adj[i, kn] == 0:
                    adj[i, kn] = adj[i, j]
                    adj[i, j] = 0.0
        
        # 突触缩放
        if step % SCALING_INT == 0 and n_act > 0:
            ar = n_act / N
            if ar > KAPPA_TARGET:
                adj[~el_mask] *= (1 - SCALING_RATE)
            elif ar < KAPPA_TARGET * 0.5:
                adj[~el_mask] *= (1 + SCALING_RATE)
            adj = np.clip(adj, 0.0, 1.0)
        
        # 修剪（仅4规则）
        if use_pruning and step % PRUNE_INT == 0 and step > 0:
            deg = (adj > 0).sum(axis=1)
            for i, j in np.argwhere((adj > 0) & (~el_mask) & (nltp == 0) & (nltd == 0)):
                if deg[i] > MIN_EDGES and rng.random() < P_PRUNE:
                    adj[i, j] = 0.0
            nltp[:] = 0
            nltd[:] = 0
        
        if step % LOG_INT == 0:
            sig = compute_sigma_fast(adj, N)
            print(f"    学习 step={step}/{N_LEARN} | σ={sig:.2f} | edges={(adj>0).sum()} | t={time.time()-t0:.0f}s")
            sys.stdout.flush()
            topology_log.append({'step': step, 'sigma': sig, 'n_edges': int((adj>0).sum()),
                                  'n_el': int(el_mask.sum()), 'phase': '学习'})
    
    # ===== 临界点校准 =====
    print(f"\n  [{net_name}|seed={seed}] 临界点校准中...")
    sys.stdout.flush()
    G_calib, kappa_calib = calibrate_G(adj, el_mask, N, seed)
    print(f"  校准结果: G={G_calib:.4f}, κ={kappa_calib:.4f}")
    sys.stdout.flush()
    
    # ===== 阶段2：雪崩记录（10000步，纯BTW驱动） =====
    print(f"\n  [{net_name}|seed={seed}] 记录阶段开始（{N_RECORD}步，G={G_calib:.4f}）...")
    sys.stdout.flush()
    
    activation_series = []
    refrac[:] = 0  # 重置不应期
    
    for step in range(N_RECORD):
        active = np.zeros(N, dtype=bool)
        
        # BTW极慢驱动
        if step % BTW_INTERVAL == 0:
            d = int(rng.integers(N))
            if refrac[d] == 0:
                active[d] = True
        
        # 级联传播（使用校准增益G）
        if active.any():
            prev_wave = active.copy()
            all_act = active.copy()
            for _ in range(15):  # 允许更多级联步骤
                if not prev_wave.any():
                    break
                new_wave = np.zeros(N, dtype=bool)
                for i in np.where(prev_wave)[0]:
                    w = adj[i, :] * G_calib
                    w[el_mask[i, :]] *= 1.2
                    for c in np.where(w > 0.005)[0]:
                        if refrac[c] == 0 and not all_act[c]:
                            if rng.random() < min(w[c], 0.99):
                                new_wave[c] = True
                new_wave &= ~all_act
                all_act |= new_wave
                prev_wave = new_wave
                if not new_wave.any():
                    break
            active = all_act
        
        n_act = int(active.sum())
        activation_series.append(n_act)
        
        refrac[active] = T_ABS
        refrac[refrac > 0] -= 1
        
        if step % LOG_INT == 0:
            sig = compute_sigma_fast(adj, N)
            print(f"    记录 step={step}/{N_RECORD} | σ={sig:.2f} | n_act={n_act} | t={time.time()-t0:.0f}s")
            sys.stdout.flush()
            topology_log.append({'step': N_LEARN + step, 'sigma': sig,
                                  'n_edges': int((adj>0).sum()),
                                  'n_el': int(el_mask.sum()), 'phase': '记录'})
    
    # ============ 雪崩分析 ============
    arr = np.array(activation_series)
    zero_frac = float((arr == 0).mean())
    n_nonzero = int((arr > 0).sum())
    
    print(f"\n  激活统计 [{net_name}|seed={seed}]:")
    print(f"    总记录步: {len(arr)} | 零值帧: {zero_frac:.1%} | 最大激活: {arr.max()}")
    print(f"    平均激活: {arr.mean():.3f}")
    
    sizes, durations = detect_avalanches(activation_series)
    tau_s, xmin_s, n_ts, r2_s = fit_powerlaw(sizes)
    tau_d, xmin_d, n_td, r2_d = fit_powerlaw(durations)
    kappa = compute_branching_ratio(activation_series)
    psd_slope, psd_r2 = compute_psd_slope(activation_series)
    
    n_avalanches = len(sizes)
    mean_size = float(np.mean(sizes)) if sizes else 0.0
    max_size = int(max(sizes)) if sizes else 0
    
    # 达标判定
    size_ok = (tau_s is not None and 1.2 <= tau_s <= 2.2 and r2_s > 0.75)
    dur_ok = (tau_d is not None and 1.5 <= tau_d <= 2.5 and r2_d > 0.75)
    kappa_ok = (0.88 <= kappa <= 1.12)
    count_ok = (n_avalanches >= 300)
    psd_ok = (psd_slope is not None and -1.5 <= psd_slope <= -0.3)
    zero_ok = (zero_frac >= 0.3)
    
    score = sum([size_ok, dur_ok, kappa_ok, count_ok, psd_ok, zero_ok])
    
    tau_s_str = f"{tau_s:.3f}" if tau_s is not None else "N/A"
    tau_d_str = f"{tau_d:.3f}" if tau_d is not None else "N/A"
    psd_str = f"{psd_slope:.3f}" if psd_slope is not None else "N/A"
    
    print(f"\n{'='*60}")
    print(f"  结果 [{net_name}|seed={seed}|{'4-r' if use_pruning else '3-r'}] G={G_calib:.3f}")
    print(f"  零值帧: {zero_frac:.1%} {'✓' if zero_ok else '✗'}")
    print(f"  雪崩数: {n_avalanches} | 平均尺寸: {mean_size:.1f} | 最大: {max_size} {'✓' if count_ok else '✗'}")
    print(f"  τ_size={tau_s_str} R²={r2_s:.3f} {'✓' if size_ok else '✗'}")
    print(f"  τ_dur={tau_d_str} R²={r2_d:.3f} {'✓' if dur_ok else '✗'}")
    print(f"  κ={kappa:.4f} {'✓' if kappa_ok else '✗'}")
    print(f"  PSD={psd_str} R²={psd_r2:.3f} {'✓' if psd_ok else '✗'}")
    print(f"  得分: {score}/6")
    print(f"  {'='*60}\n")
    sys.stdout.flush()
    
    return {
        'network': net_name, 'seed': seed,
        'rules': '4-rules' if use_pruning else '3-rules',
        'G_calib': float(G_calib),
        'kappa_calib': float(kappa_calib),
        'zero_fraction': float(zero_frac),
        'n_avalanches': n_avalanches,
        'mean_size': float(mean_size),
        'max_size': max_size,
        'tau_size': float(tau_s) if tau_s is not None else None,
        'r2_size': float(r2_s),
        'tau_duration': float(tau_d) if tau_d is not None else None,
        'r2_duration': float(r2_d),
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
        'activation_sample': [int(x) for x in activation_series[:4000]],
        'sizes_sample': sorted([int(s) for s in sizes])[:800],
        'durations_sample': sorted([int(d) for d in durations])[:800],
    }

# ============ 绘图 ============
def plot_results(all_results):
    fig = plt.figure(figsize=(18, 18))
    fig.suptitle('SDI 实验五 v3：神经雪崩SOC动力学验证\n'
                 r'两阶段协议：学习→临界点校准(G)→BTW慢驱动雪崩记录',
                 fontsize=12, fontweight='bold', y=0.99)
    gs = GridSpec(4, 3, figure=fig, hspace=0.45, wspace=0.35)
    
    from collections import defaultdict
    by_group = defaultdict(list)
    for r in all_results:
        by_group[r['network'] + '_' + r['rules']].append(r)
    
    best_per_group = {k: max(v, key=lambda x: x['score']) for k, v in by_group.items()}
    plot_items = sorted(best_per_group.items())[:6]
    colors = {'3-rules': '#2196F3', '4-rules': '#E91E63'}
    
    for pi, (key, res) in enumerate(plot_items):
        if pi >= 6:
            break
        color = colors.get(res['rules'], '#333')
        row, col = divmod(pi, 3)
        
        # 激活序列（前3000步）
        ax1 = fig.add_subplot(gs[row * 2, col])
        act = res.get('activation_sample', [])
        if act:
            ax1.plot(act[:2000], color=color, linewidth=0.6, alpha=0.8)
        zf = res.get('zero_fraction', 0)
        kv = res.get('branching_ratio', 0)
        G = res.get('G_calib', 1.0)
        ax1.set_title(f"{res['network']}\n{res['rules']} | G={G:.2f} | κ={kv:.3f}\n零帧{zf:.0%}",
                     fontsize=7, color='green' if res.get('score', 0) >= 3 else 'red')
        ax1.set_xlabel('步数', fontsize=6)
        ax1.set_ylabel('激活数', fontsize=6)
        ax1.tick_params(labelsize=6)
        
        # 雪崩尺寸分布（log-log）
        ax2 = fig.add_subplot(gs[row * 2 + 1, col])
        sizes = res.get('sizes_sample', [])
        if sizes and len(sizes) > 10:
            sa = np.array(sizes)
            b = np.logspace(np.log10(max(1, sa.min())), np.log10(max(sa.max(), 2)), 25)
            cnt, edg = np.histogram(sa, bins=b)
            ctr = (edg[:-1] + edg[1:]) / 2
            msk = cnt > 0
            if msk.sum() > 3:
                ax2.loglog(ctr[msk], cnt[msk], 'o', color=color, ms=4, alpha=0.7, label='数据')
                xt = np.logspace(np.log10(ctr[msk][0]), np.log10(ctr[msk][-1]), 50)
                y0 = cnt[msk][0] * (ctr[msk][0] ** 1.5)
                ax2.loglog(xt, y0 / (xt ** 1.5), '--', color='gray', alpha=0.5, label='τ=1.5')
        ts = res.get('tau_size')
        r2s = res.get('r2_size', 0)
        ts_str = f"{ts:.2f}" if ts is not None else "N/A"
        ok = res['criteria'].get('size_powerlaw', False)
        ax2.set_title(f"τ_size={ts_str} R²={r2s:.2f} {'✓' if ok else '✗'}",
                     fontsize=7, color='green' if ok else 'red')
        ax2.set_xlabel('雪崩尺寸 S', fontsize=6)
        ax2.set_ylabel('频率', fontsize=6)
        ax2.tick_params(labelsize=6)
        ax2.legend(fontsize=5)
    
    plt.savefig(f'{OUT}/exp5_v3_avalanche_results.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✅ 图表已保存: {OUT}/exp5_v3_avalanche_results.png")

# ============ 主程序 ============
def main():
    print("=" * 70)
    print("SDI 实验五 v3：神经雪崩SOC动力学验证")
    print("  阶段1（学习）: 外部刺激 → STDP演化拓扑")
    print("  校准: 二分法找临界增益G → κ∈[0.9, 1.1]")
    print("  阶段2（记录）: 纯BTW极慢驱动 → 自发雪崩")
    print("=" * 70)
    sys.stdout.flush()
    
    all_results = []
    t_total = time.time()
    
    for rules_label, use_pruning in [('3-rules', False), ('4-rules', True)]:
        print(f"\n【{'3' if not use_pruning else '4'}规则体系】")
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
    
    # 序列化
    def ser(o):
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, bool):
            return bool(o)
        return o
    
    def ds(o):
        if isinstance(o, dict):
            return {k: ds(v) for k, v in o.items()}
        if isinstance(o, list):
            return [ds(v) for v in o]
        return ser(o)
    
    out_path = f'{OUT}/exp5_v3_avalanche_results.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(ds(all_results), f, ensure_ascii=False, indent=2)
    print(f"\n✅ 结果已保存: {out_path}")
    
    try:
        plot_results(all_results)
    except Exception as e:
        print(f"  ⚠️ 绘图失败: {e}")
    
    # ============ 汇总 ============
    print("\n" + "=" * 70)
    print("实验五v3汇总")
    print("=" * 70)
    
    from collections import defaultdict
    gs_dict = defaultdict(list)
    for r in all_results:
        gs_dict[f"{r['network']}_{r['rules']}"].append(r)
    
    print(f"\n{'网络+规则':<28} {'G':<7} {'零帧%':<7} {'雪崩数':<8} {'τ_sz':<7} {'τ_du':<7} {'κ':<8} {'PSD':<7} {'分':<5}")
    print("-" * 88)
    
    for key, runs in sorted(gs_dict.items()):
        G = np.mean([r['G_calib'] for r in runs])
        zf = np.mean([r['zero_fraction'] for r in runs])
        n = np.mean([r['n_avalanches'] for r in runs])
        ts = [r['tau_size'] for r in runs if r['tau_size'] is not None]
        td = [r['tau_duration'] for r in runs if r['tau_duration'] is not None]
        kv = [r['branching_ratio'] for r in runs]
        pv = [r['psd_slope'] for r in runs if r['psd_slope'] is not None]
        sv = [r['score'] for r in runs]
        
        print(f"{key:<28} {G:<7.3f} {zf:.0%}  {n:<8.0f} "
              f"{np.mean(ts):.2f if ts else 'N/A':<7} "
              f"{np.mean(td):.2f if td else 'N/A':<7} "
              f"{np.mean(kv):.4f}  "
              f"{np.mean(pv):.2f if pv else 'N/A':<7} "
              f"{np.mean(sv):.1f}/6")
    
    print()
    best = max(all_results, key=lambda x: x['score'])
    ts_str = f"{best['tau_size']:.2f}" if best['tau_size'] is not None else "N/A"
    print(f"最佳: {best['network']} | {best['rules']} | seed={best['seed']} | "
          f"τ={ts_str}, κ={best['branching_ratio']:.3f} | 得分={best['score']}/6")
    
    elapsed = time.time() - t_total
    print(f"\n总耗时: {elapsed:.0f}s ({elapsed/60:.1f}min)")
    print("实验五v3完成。")
    sys.stdout.flush()

if __name__ == '__main__':
    main()
