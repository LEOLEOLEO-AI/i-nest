#!/usr/bin/env python3
"""
SDI 实验五 v4：神经雪崩SOC动力学验证（最终修复版）

==============================================================================
v3问题诊断与根本修复
==============================================================================
v3问题：
  1. 雪崩在一个时间步内完成全部级联 → duration永远=1
  2. κ计算：Priesemann方法在BTW间隔驱动下失效（n_{t+1}在n_t>0后总是0）

v4根本设计修复：
  ► 每个时间步只传播一层（无内部循环）
    → BTW在t=0注入1个神经元
    → t=1: 1个神经元激活多个邻居（第1层传播）
    → t=2: 邻居再传播（第2层）
    → 直到无新激活 → 雪崩自然结束
    → 雪崩持续时间 = 激活非零帧数（多个时间步）

  ► 分支比κ在单次雪崩内计算：
    κ = Σ(第i+1层激活数) / Σ(第i层激活数)，对i=0,1,2,...求和

  ► 关键：不应期重置在每步之后（而不是雪崩内）

这是真正与Beggs & Plenz (2003)实验对应的仿真协议。

==============================================================================
SOC检测原理（Beggs & Plenz 2003重建）
==============================================================================
时间分辨率：Δt = 1步（每步记录激活数）
雪崩定义：连续非零时间步序列
          ___  ________  ___
... 0 0 | 2 3 5 8 3 1 | 0 0 | 4 2 1 | 0 0 ...
              雪崩1          雪崩2

S = 2+3+5+8+3+1 = 22（尺寸）
T = 6（持续时间）
κ_内部 = (3+5+8+3+1)/(2+3+5+8+3) = 20/21 ≈ 0.95
"""

import numpy as np
import json
import time
import sys

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
T_ABS = 2      # 短绝对不应期（允许连续激活）
T_REL = 4
P_REWIRE = 0.15
REWIRE_INT = 50
SCALING_INT = 100
KAPPA_TARGET = 0.95
SCALING_RATE = 0.05

# ============ 实验五v4特有参数 ============
N_LEARN = 8000        # 学习阶段
N_RECORD = 15000      # 雪崩记录阶段（更长以积累统计）
N_STEPS = N_LEARN + N_RECORD
LOG_INT = 2000

# BTW驱动（每步最多激活一个节点）
BTW_INTERVAL = 8      # 每8步注入一次（间隔够长，让上次雪崩结束）

# 临界点校准
CALIB_STEPS = 500
CALIB_ITER = 30
G_LO = 0.01
G_HI = 20.0

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

# ============ 单步传播（一层级联）============
def propagate_single_layer(adj, el_mask, active_in, refrac, fired_set, N, G, rng):
    """
    从active_in激活的神经元，向邻居传播一层。
    fired_set：本次雪崩中已激活的神经元集合（防止重复激活）
    返回：新激活的神经元布尔数组
    """
    new_active = np.zeros(N, dtype=bool)
    for i in np.where(active_in)[0]:
        w = adj[i, :] * G
        w[el_mask[i, :]] *= 1.2
        for c in np.where(w > 0.001)[0]:
            if not fired_set[c] and refrac[c] == 0:
                if rng.random() < min(float(w[c]), 0.99):
                    new_active[c] = True
    return new_active

# ============ 估计κ（用单雪崩内分支比）============
def estimate_kappa_single_shot(adj, el_mask, N, G, rng_seed, n_shots=50):
    """
    注入n_shots次单个神经元，跟踪每次雪崩的分支比。
    κ = Σ(第2层激活数) / Σ(第1层激活数)，平均到所有有效雪崩
    """
    rng = np.random.default_rng(rng_seed)
    refrac = np.zeros(N, dtype=np.int8)
    
    kappa_vals = []
    
    for shot in range(n_shots):
        # 选择一个随机激活节点
        seed_node = int(rng.integers(N))
        while refrac[seed_node] > 0:
            seed_node = int(rng.integers(N))
        
        # 跟踪这次雪崩的分支比
        wave = np.zeros(N, dtype=bool)
        wave[seed_node] = True
        fired = np.zeros(N, dtype=bool)
        fired[seed_node] = True
        
        prev_n = 1
        cascade_kappas = []
        
        for _ in range(20):  # 最多20步级联
            if not wave.any():
                break
            new_wave = propagate_single_layer(adj, el_mask, wave, refrac, fired, N, G, rng)
            fired |= new_wave
            curr_n = int(new_wave.sum())
            if prev_n > 0:
                cascade_kappas.append(curr_n / prev_n)
            if curr_n == 0:
                break
            wave = new_wave
            prev_n = curr_n
        
        if cascade_kappas:
            kappa_vals.append(np.mean(cascade_kappas))
        
        # 更新不应期
        refrac[fired] = T_ABS + T_REL
        refrac[refrac > 0] -= 1
        # 额外等待几步
        for _ in range(BTW_INTERVAL):
            refrac[refrac > 0] -= 1
    
    return float(np.mean(kappa_vals)) if kappa_vals else 0.0

# ============ 校准临界增益G ============
def calibrate_G(adj, el_mask, N, seed):
    G_lo = G_LO
    G_hi = G_HI
    G_best = 1.0
    
    for i in range(CALIB_ITER):
        G_mid = (G_lo + G_hi) / 2
        kappa = estimate_kappa_single_shot(adj, el_mask, N, G_mid, seed + i * 1000)
        print(f"    校准 iter={i+1}: G={G_mid:.5f} → κ={kappa:.4f}")
        sys.stdout.flush()
        
        if 0.85 <= kappa <= 1.15:
            G_best = G_mid
            print(f"    ✅ 校准成功: G={G_best:.5f}, κ={kappa:.4f}")
            return G_best, kappa
        
        if kappa < 0.85:
            G_lo = G_mid
        else:
            G_hi = G_mid
        
        if G_hi - G_lo < 0.0005:
            G_best = G_mid
            break
        
        G_best = G_mid
    
    kappa_final = estimate_kappa_single_shot(adj, el_mask, N, G_best, seed + 999999)
    print(f"    ⚠️ 校准结束: G={G_best:.5f}, κ={kappa_final:.4f}")
    return G_best, kappa_final

# ============ 雪崩检测 ============
def detect_avalanches(activation_series):
    arr = np.array(activation_series, dtype=int)
    sizes, durations, kappas = [], [], []
    in_av = False
    layers = []
    for n in arr:
        if n > 0:
            in_av = True
            layers.append(n)
        else:
            if in_av and layers:
                sizes.append(sum(layers))
                durations.append(len(layers))
                # 雪崩内分支比
                if len(layers) >= 2:
                    k_inner = sum(layers[1:]) / sum(layers[:-1]) if sum(layers[:-1]) > 0 else 0
                    kappas.append(k_inner)
                in_av = False
                layers = []
    if in_av and layers:
        sizes.append(sum(layers))
        durations.append(len(layers))
        if len(layers) >= 2:
            k_inner = sum(layers[1:]) / sum(layers[:-1]) if sum(layers[:-1]) > 0 else 0
            kappas.append(k_inner)
    return sizes, durations, kappas

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
        lr = np.log(tail / xm)
        if lr.sum() == 0:
            continue
        tau_e = 1 + len(tail) / lr.sum()
        ts = np.sort(tail)
        ecdf = np.arange(1, len(ts) + 1) / len(ts)
        tcdf = 1 - (ts / xm) ** (-(tau_e - 1))
        ks = np.max(np.abs(ecdf - tcdf))
        if ks < best_ks:
            best_ks = ks
            best_xmin = xm
            best_tau = tau_e
    
    tail = data[data >= best_xmin]
    n_tail = len(tail)
    if n_tail < 10:
        return None, float(best_xmin), n_tail, 0.0
    
    bins = min(20, max(5, n_tail // 8))
    counts, edges = np.histogram(tail, bins=bins)
    centers = (edges[:-1] + edges[1:]) / 2
    msk = counts > 0
    if msk.sum() < 4:
        return float(best_tau), float(best_xmin), n_tail, 0.0
    lx = np.log(centers[msk])
    ly = np.log(counts[msk])
    c = np.polyfit(lx, ly, 1)
    fit = np.polyval(c, lx)
    ssr = np.sum((ly - fit) ** 2)
    sst = np.sum((ly - np.mean(ly)) ** 2)
    r2 = float(1 - ssr / sst) if sst > 0 else 0.0
    
    return float(best_tau), float(best_xmin), n_tail, r2

# ============ 1/f 功率谱 ============
def compute_psd_slope(activation_series):
    arr = np.array(activation_series, dtype=float)
    arr = arr - arr.mean()
    n = len(arr)
    power = np.abs(np.fft.rfft(arr)) ** 2
    freqs = np.fft.rfftfreq(n)
    mask = (freqs > 0.001) & (freqs < 0.25)
    if mask.sum() < 15:
        return 0.0, 0.0
    lf = np.log(freqs[mask])
    lp = np.log(power[mask] + 1e-10)
    c = np.polyfit(lf, lp, 1)
    fit = np.polyval(c, lf)
    ssr = np.sum((lp - fit) ** 2)
    sst = np.sum((lp - np.mean(lp)) ** 2)
    r2 = float(1 - ssr / sst) if sst > 0 else 0.0
    return float(c[0]), r2

# ============ 主仿真 ============
def run_simulation(net_name, net_cfg, seed, use_pruning=False):
    N = net_cfg['N']
    sf = net_cfg['sf']
    K_PATTERNS = net_cfg['K_PATTERNS']
    
    rng = np.random.default_rng(seed)
    
    adj = make_ws_adj(N, net_cfg['k_init'], net_cfg['p_init'], seed)
    el_mask = (rng.random((N, N)) < 0.05).astype(bool)
    el_mask &= (adj > 0)
    nltp = np.zeros((N, N), dtype=np.int16)
    nltd = np.zeros((N, N), dtype=np.int16)
    el_age = np.zeros((N, N), dtype=np.int32)
    refrac = np.zeros(N, dtype=np.int8)
    
    stim_size = max(1, int(N * sf))
    rng_pat = np.random.default_rng(seed + 1000)
    patterns = [rng_pat.choice(N, size=stim_size, replace=False).tolist()
                for _ in range(K_PATTERNS)]
    
    topology_log = []
    t0 = time.time()
    pat_idx = 0
    
    # ===== 阶段1：学习（STDP + 外部刺激） =====
    print(f"  [{net_name}|seed={seed}] 学习阶段（{N_LEARN}步）...")
    sys.stdout.flush()
    
    for step in range(N_LEARN):
        # ► 外部刺激（连续驱动，每步传播一层）
        active = np.zeros(N, dtype=bool)
        if step % 10 == 0 and rng.random() < 0.1:
            pat_idx = int(rng.integers(K_PATTERNS))
        for ni in patterns[pat_idx % K_PATTERNS]:
            if refrac[ni] == 0 and rng.random() < 0.25:
                active[ni] = True
        
        # ► 单层传播（学习阶段G=1.0）
        if active.any():
            fired = active.copy()
            new_w = propagate_single_layer(adj, el_mask, active, refrac, fired, N, 1.0, rng)
            active |= new_w
        
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
        ltp_m = (nltp >= THETA_LTP) & (adj > 0) & (~el_mask) & (el_ratio < EL_HI)
        el_mask[ltp_m] = True
        nltp[ltp_m] = 0
        ltd_m = (nltd >= THETA_LTD) & (adj > 0) & (~el_mask)
        adj[ltd_m] = 0.0
        nltp[ltd_m] = nltd[ltd_m] = 0
        el_age[el_mask] += 1
        dm = el_mask & (el_age > T_DECAY)
        el_mask[dm] = False
        el_age[dm] = 0
        
        # WS重连
        if step % REWIRE_INT == 0:
            non_el = np.argwhere((adj > 0) & (~el_mask))
            for _ in range(max(1, int(len(non_el) * P_REWIRE * 0.01))):
                if len(non_el) == 0:
                    break
                ix = int(rng.integers(len(non_el)))
                i, j = non_el[ix]
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
        
        # 修剪（4规则）
        if use_pruning and step % PRUNE_INT == 0 and step > 0:
            deg = (adj > 0).sum(axis=1)
            for i, j in np.argwhere((adj > 0) & (~el_mask) & (nltp == 0) & (nltd == 0)):
                if deg[i] > MIN_EDGES and rng.random() < P_PRUNE:
                    adj[i, j] = 0.0
            nltp[:] = 0
            nltd[:] = 0
        
        if step % LOG_INT == 0:
            sig = compute_sigma_fast(adj, N)
            print(f"    学习 step={step}/{N_LEARN} σ={sig:.2f} edges={(adj>0).sum()} t={time.time()-t0:.0f}s")
            sys.stdout.flush()
            topology_log.append({'step': step, 'sigma': sig,
                                  'n_edges': int((adj>0).sum()),
                                  'n_el': int(el_mask.sum()), 'phase': '学习'})
    
    # ===== 临界点校准 =====
    print(f"\n  [{net_name}|seed={seed}] 临界点校准...")
    sys.stdout.flush()
    G_calib, kappa_calib = calibrate_G(adj, el_mask, N, seed)
    print(f"  校准结果: G={G_calib:.5f}, κ={kappa_calib:.4f}")
    sys.stdout.flush()
    
    # ===== 阶段2：雪崩记录（纯BTW，逐步传播）=====
    print(f"\n  [{net_name}|seed={seed}] 记录阶段（{N_RECORD}步，G={G_calib:.4f}）...")
    sys.stdout.flush()
    
    activation_series = []
    refrac[:] = 0
    
    # 当前"活跃波"（跨时间步的雪崩追踪）
    current_wave = np.zeros(N, dtype=bool)
    fired_in_avalanche = np.zeros(N, dtype=bool)
    
    for step in range(N_RECORD):
        # BTW注入（仅当上一次雪崩已结束：current_wave全零）
        if not current_wave.any() and step % BTW_INTERVAL == 0:
            d = int(rng.integers(N))
            if refrac[d] == 0:
                current_wave[d] = True
                fired_in_avalanche[:] = False
                fired_in_avalanche[d] = True
        
        # 单层传播
        if current_wave.any():
            new_wave = propagate_single_layer(
                adj, el_mask, current_wave, refrac, fired_in_avalanche, N, G_calib, rng
            )
            fired_in_avalanche |= new_wave
            current_wave = new_wave
        
        n_act = int(fired_in_avalanche.sum()) if current_wave.any() else 0
        # 注意：记录"当前波"大小，不是fired集合大小
        n_wave = int(current_wave.sum())
        activation_series.append(n_wave)
        
        # 更新不应期（仅当前波中的神经元）
        refrac[current_wave] = T_ABS
        refrac[refrac > 0] -= 1
        
        if step % LOG_INT == 0:
            sig = compute_sigma_fast(adj, N)
            print(f"    记录 step={step}/{N_RECORD} σ={sig:.2f} wave={n_wave} t={time.time()-t0:.0f}s")
            sys.stdout.flush()
            topology_log.append({'step': N_LEARN + step, 'sigma': sig,
                                  'n_edges': int((adj>0).sum()),
                                  'n_el': int(el_mask.sum()), 'phase': '记录'})
    
    # ============ 雪崩分析 ============
    arr = np.array(activation_series)
    zero_frac = float((arr == 0).mean())
    
    print(f"\n  激活统计:")
    print(f"    零值帧: {zero_frac:.1%} | 最大激活: {arr.max()} | 平均: {arr.mean():.3f}")
    
    sizes, durations, kappas_inner = detect_avalanches(activation_series)
    
    tau_s, _, n_ts, r2_s = fit_powerlaw(sizes)
    tau_d, _, n_td, r2_d = fit_powerlaw(durations)
    kappa = float(np.mean(kappas_inner)) if kappas_inner else 0.0
    psd_slope, psd_r2 = compute_psd_slope(activation_series)
    
    n_avalanches = len(sizes)
    mean_size = float(np.mean(sizes)) if sizes else 0.0
    max_size = int(max(sizes)) if sizes else 0
    mean_dur = float(np.mean(durations)) if durations else 0.0
    
    # 持续时间分布统计
    dur_arr = np.array(durations) if durations else np.array([0])
    frac_dur1 = float((dur_arr == 1).mean()) if len(dur_arr) > 0 else 1.0
    
    # 达标判定
    size_ok = (tau_s is not None and 1.2 <= tau_s <= 2.2 and r2_s > 0.70)
    dur_ok = (tau_d is not None and 1.5 <= tau_d <= 2.5 and r2_d > 0.70)
    kappa_ok = (0.85 <= kappa <= 1.15)
    count_ok = (n_avalanches >= 200)
    psd_ok = (psd_slope is not None and -1.5 <= psd_slope <= -0.3)
    zero_ok = (zero_frac >= 0.3)
    multi_ok = (frac_dur1 < 0.8)  # 多步持续时间的雪崩占比>20%
    
    score = sum([size_ok, dur_ok, kappa_ok, count_ok, psd_ok, zero_ok, multi_ok])
    
    ts_str = f"{tau_s:.3f}" if tau_s is not None else "N/A"
    td_str = f"{tau_d:.3f}" if tau_d is not None else "N/A"
    ps_str = f"{psd_slope:.3f}" if psd_slope is not None else "N/A"
    
    print(f"\n{'='*60}")
    print(f"  结果 [{net_name}|seed={seed}|{'4-r' if use_pruning else '3-r'}] G={G_calib:.4f}")
    print(f"  零值帧: {zero_frac:.1%} {'✓' if zero_ok else '✗'}")
    print(f"  雪崩数: {n_avalanches} | 平均尺寸: {mean_size:.1f} | 平均时长: {mean_dur:.1f} {'✓' if count_ok else '✗'}")
    print(f"  多步雪崩占比: {1-frac_dur1:.1%} {'✓' if multi_ok else '✗'}")
    print(f"  τ_size={ts_str} R²={r2_s:.3f} {'✓' if size_ok else '✗'}")
    print(f"  τ_dur={td_str} R²={r2_d:.3f} {'✓' if dur_ok else '✗'}")
    print(f"  κ(内部)={kappa:.4f} {'✓' if kappa_ok else '✗'}")
    print(f"  PSD={ps_str} R²={psd_r2:.3f} {'✓' if psd_ok else '✗'}")
    print(f"  得分: {score}/7")
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
        'max_size': int(max_size),
        'mean_duration': float(mean_dur),
        'frac_dur1': float(frac_dur1),
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
            'psd_1f': bool(psd_ok),
            'multi_step': bool(multi_ok)
        },
        'topology_log': topology_log,
        'activation_sample': [int(x) for x in activation_series[:5000]],
        'sizes_sample': sorted([int(s) for s in sizes])[:1000],
        'durations_sample': sorted([int(d) for d in durations])[:1000],
    }

# ============ 绘图 ============
def plot_results(all_results):
    fig = plt.figure(figsize=(18, 22))
    fig.suptitle('SDI 实验五 v4：神经雪崩SOC动力学验证\n'
                 r'两阶段协议（STDP学习→临界校准G→逐步BTW传播）',
                 fontsize=12, fontweight='bold', y=0.99)
    gs = GridSpec(6, 3, figure=fig, hspace=0.50, wspace=0.35)
    
    from collections import defaultdict
    bg = defaultdict(list)
    for r in all_results:
        bg[r['network'] + '_' + r['rules']].append(r)
    
    best = {k: max(v, key=lambda x: x['score']) for k, v in bg.items()}
    items = sorted(best.items())[:6]
    colors = {'3-rules': '#2196F3', '4-rules': '#E91E63'}
    
    for pi, (key, res) in enumerate(items):
        if pi >= 6:
            break
        color = colors.get(res['rules'], '#333')
        row, col = divmod(pi, 3)
        
        # 激活序列
        ax1 = fig.add_subplot(gs[row * 2, col])
        act = res.get('activation_sample', [])
        if act:
            ax1.plot(act[:3000], color=color, linewidth=0.6, alpha=0.8)
        zf = res.get('zero_fraction', 0)
        kv = res.get('branching_ratio', 0)
        G = res.get('G_calib', 1.0)
        sc = res.get('score', 0)
        ax1.set_title(f"{res['network']} {res['rules']}\nG={G:.3f} κ={kv:.3f} 得分={sc}/7",
                     fontsize=7, color='green' if sc >= 4 else ('orange' if sc >= 2 else 'red'))
        ax1.set_xlabel('步数', fontsize=6)
        ax1.set_ylabel('当前波大小', fontsize=6)
        ax1.tick_params(labelsize=6)
        
        # 雪崩尺寸分布
        ax2 = fig.add_subplot(gs[row * 2 + 1, col])
        sizes = res.get('sizes_sample', [])
        if sizes and len(sizes) > 10:
            sa = np.array(sizes)
            try:
                b = np.logspace(np.log10(max(1, sa.min())), np.log10(max(sa.max(), 2)), 25)
                cnt, edg = np.histogram(sa, bins=b)
                ctr = (edg[:-1] + edg[1:]) / 2
                msk = cnt > 0
                if msk.sum() > 3:
                    ax2.loglog(ctr[msk], cnt[msk], 'o', color=color, ms=4, alpha=0.7, label='数据')
                    xt = np.logspace(np.log10(ctr[msk][0]), np.log10(ctr[msk][-1]), 50)
                    y0 = cnt[msk][0] * (ctr[msk][0] ** 1.5)
                    ax2.loglog(xt, y0 / (xt ** 1.5), '--', color='gray', alpha=0.5, label='τ=1.5')
            except:
                pass
        ts = res.get('tau_size')
        r2s = res.get('r2_size', 0)
        ts_str = f"{ts:.2f}" if ts is not None else "N/A"
        ok = res.get('criteria', {}).get('size_powerlaw', False)
        ax2.set_title(f"τ={ts_str} R²={r2s:.2f} {'✓' if ok else '✗'}",
                     fontsize=7, color='green' if ok else 'red')
        ax2.set_xlabel('雪崩尺寸 S', fontsize=6)
        ax2.set_ylabel('频率', fontsize=6)
        ax2.tick_params(labelsize=6)
        ax2.legend(fontsize=5)
    
    plt.savefig(f'{OUT}/exp5_v4_avalanche_results.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✅ 图表已保存: {OUT}/exp5_v4_avalanche_results.png")

# ============ 主程序 ============
def main():
    print("=" * 70)
    print("SDI 实验五 v4：神经雪崩SOC动力学验证（最终修复版）")
    print("  设计：每步传播一层（非级联内循环）→ 多步雪崩展开")
    print("  校准：注入单个神经元追踪雪崩内分支比κ")
    print("  指标：τ_size≈1.5, τ_dur≈2.0, κ≈1.0, 1/f PSD")
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
        return o
    
    def ds(o):
        if isinstance(o, dict):
            return {k: ds(v) for k, v in o.items()}
        if isinstance(o, list):
            return [ds(v) for v in o]
        return ser(o)
    
    out_path = f'{OUT}/exp5_v4_avalanche_results.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(ds(all_results), f, ensure_ascii=False, indent=2)
    print(f"\n✅ 结果已保存: {out_path}")
    
    try:
        plot_results(all_results)
    except Exception as e:
        print(f"  ⚠️ 绘图失败: {e}")
    
    # ============ 汇总 ============
    print("\n" + "=" * 70)
    print("实验五v4汇总")
    print("=" * 70)
    
    from collections import defaultdict
    gd = defaultdict(list)
    for r in all_results:
        gd[f"{r['network']}_{r['rules']}"].append(r)
    
    print(f"\n{'网络+规则':<28} G{'':4} κ{'':4} τ_sz{'':3} τ_du{'':3} 多步%  PSD{'':3} 得分")
    print("-" * 75)
    
    for key, runs in sorted(gd.items()):
        G = np.mean([r['G_calib'] for r in runs])
        kv = np.mean([r['branching_ratio'] for r in runs])
        ts = [r['tau_size'] for r in runs if r['tau_size'] is not None]
        td = [r['tau_duration'] for r in runs if r['tau_duration'] is not None]
        pv = [r['psd_slope'] for r in runs if r['psd_slope'] is not None]
        md = np.mean([1 - r['frac_dur1'] for r in runs])
        sv = [r['score'] for r in runs]
        
        ts_str = f"{np.mean(ts):.2f}" if ts else "N/A"
        td_str = f"{np.mean(td):.2f}" if td else "N/A"
        pv_str = f"{np.mean(pv):.2f}" if pv else "N/A"
        
        print(f"{key:<28} {G:.3f}  {kv:.3f}  {ts_str:<7} {td_str:<7} {md:.0%}  {pv_str:<7} {np.mean(sv):.1f}/7")
    
    print()
    best = max(all_results, key=lambda x: x['score'])
    ts_str = f"{best['tau_size']:.3f}" if best['tau_size'] is not None else "N/A"
    td_str = f"{best['tau_duration']:.3f}" if best['tau_duration'] is not None else "N/A"
    print(f"最佳: {best['network']} | {best['rules']} | seed={best['seed']}")
    print(f"  τ_size={ts_str}, τ_dur={td_str}, κ={best['branching_ratio']:.3f}")
    print(f"  G_calib={best['G_calib']:.4f}, 得分={best['score']}/7")
    
    elapsed = time.time() - t_total
    print(f"\n总耗时: {elapsed:.0f}s ({elapsed/60:.1f}min)")
    print("实验五v4完成。")
    sys.stdout.flush()

if __name__ == '__main__':
    main()
