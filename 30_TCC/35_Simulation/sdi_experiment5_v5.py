#!/usr/bin/env python3
"""
SDI 实验五 v5：神经雪崩SOC动力学验证（τ幂律修复版）

==============================================================================
v4问题诊断与修复
==============================================================================
v4核心Bug：
  校准G时用"空网络单次注入"（所有神经元无不应期）
  → 需要极大G(≈10)才能使κ=1.0
  → 但真实记录时BTW持续驱动，不应期填满 → 实际分支因子≈23 → 双峰分布
  → 大量雪崩size≈200，无中等尺寸，幂律τ无法拟合

v5修复策略：
  ► 用"真实BTW连续驱动"过程中的分支比来校准G
    → 运行500步连续BTW驱动，记录每次wave层级的激活比
    → 确保校准条件与记录条件完全一致
  ► 目标：记录阶段的实际κ∈[0.90, 1.10]
  ► 预期结果：
    - 产生大量小雪崩（size=1,2,3,...）+ 少量大雪崩
    - 尺寸分布符合幂律 P(S) ~ S^{-1.5}
    - 时长分布符合幂律 P(T) ~ T^{-2.0}

==============================================================================
理论依据
==============================================================================
Beggs & Plenz (2003) J Neurosci：
  临界态的统计特征必须在稳态BTW驱动下测量（不是空网络）
  分支比κ = 时间平均的每代传播比，在稳态驱动下应≈1.0

Zapperi et al. (1995) PRL：
  平均场SOC的分支比与传播概率的关系：
  如果每个节点平均有k个邻居，传播概率为p，则κ=k×p
  临界点：k×p=1.0
  幂律指数τ=3/2（平均场近似）
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
T_ABS = 3      # 略长的不应期，防止重复激活
T_REL = 5
P_REWIRE = 0.15
REWIRE_INT = 50
SCALING_INT = 100
KAPPA_TARGET = 0.95
SCALING_RATE = 0.05

# ============ 实验五v5特有参数 ============
N_LEARN = 8000         # 学习阶段
N_RECORD = 20000       # 雪崩记录阶段（更长，积累更多小雪崩）
N_STEPS = N_LEARN + N_RECORD
LOG_INT = 4000

# BTW驱动（记录阶段）
BTW_INTERVAL = 10     # 每10步注入一次（保证雪崩间有足够沉寂期）

# 校准参数（真实BTW驱动条件下）
CALIB_WARMUP = 200     # 校准前先预热200步，让不应期达到稳态
CALIB_STEPS = 800      # 校准测量步数
CALIB_ITER = 30
G_LO_INIT = 0.001
G_HI_INIT = 2.0

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
                adj[i, j] = w; adj[j, i] = w
            else:
                k2 = int(rng.integers(N))
                while k2 == i: k2 = int(rng.integers(N))
                w = float(rng.uniform(0.05, 0.3))
                adj[i, k2] = w; adj[k2, i] = w
    return adj

# ============ 网络度量 ============
def compute_sigma_fast(adj, N):
    try:
        edges = np.argwhere((adj + adj.T) / 2 > 0.05)
        edges = edges[edges[:, 0] < edges[:, 1]]
        if len(edges) < 10: return 1.0
        al = [[] for _ in range(N)]
        for u, v in edges:
            al[u].append(v); al[v].append(u)
        Cv = []
        for i in range(min(40, N)):
            nb = al[i]; ki = len(nb)
            if ki < 2: Cv.append(0.0); continue
            s = set(nb)
            lk = sum(1 for a in nb for b in al[a] if b in s and b != a)
            Cv.append(lk / (ki * (ki - 1)))
        C = float(np.mean(Cv)) if Cv else 0.0
        lengths = []
        for start in range(min(25, N)):
            vis = {start: 0}; q = [start]; qi = 0
            while qi < len(q):
                nd = q[qi]; qi += 1; d = vis[nd]
                if d >= 6: continue
                for nb in al[nd]:
                    if nb not in vis: vis[nb] = d+1; q.append(nb)
            lengths.extend(vis.values())
        L = float(np.mean(lengths)) if lengths else 3.0
        m = len(edges); k_avg = 2*m/N
        if k_avg <= 1: return 1.0
        C_rand = k_avg/N; L_rand = np.log(N)/np.log(k_avg)
        if C_rand == 0 or L_rand == 0: return 1.0
        return float((C/C_rand)/(L/L_rand))
    except: return 1.0

# ============ 单层传播 ============
def propagate_layer(adj, el_mask, wave, refrac, fired, N, G, rng):
    """从wave传播一层到邻居。fired是已激活集合（避免重复）。"""
    new_wave = np.zeros(N, dtype=bool)
    for i in np.where(wave)[0]:
        w = adj[i, :] * G
        w[el_mask[i, :]] *= 1.15
        for c in np.where(w > 0.001)[0]:
            if not fired[c] and refrac[c] == 0:
                if rng.random() < min(float(w[c]), 0.99):
                    new_wave[c] = True
    return new_wave

# ============ 真实条件下校准κ ============
def estimate_kappa_realcondition(adj, el_mask, N, G, seed, n_warmup, n_measure):
    """
    在真实BTW连续驱动条件下测量分支比。
    先运行n_warmup步让不应期达到稳态，再测量n_measure步的κ。
    
    κ的测量方法：对每次BTW注入后的第一波→第二波传播比求平均
    即：κ = mean(|wave_1| / |wave_0|) 对所有有wave_1>0的雪崩
    """
    rng = np.random.default_rng(seed)
    refrac = np.zeros(N, dtype=np.int8)
    current_wave = np.zeros(N, dtype=bool)
    fired_in_av = np.zeros(N, dtype=bool)
    
    kappa_pairs = []  # (wave_0_size, wave_1_size) 列表
    
    for step in range(n_warmup + n_measure):
        is_measuring = (step >= n_warmup)
        
        # BTW注入（当上一次雪崩结束时）
        if not current_wave.any() and step % BTW_INTERVAL == 0:
            d = int(rng.integers(N))
            if refrac[d] == 0:
                current_wave[d] = True
                fired_in_av[:] = False
                fired_in_av[d] = True
                
                # 测量：记录这次雪崩的wave_0大小
                if is_measuring:
                    wave0_size = 1
                    # 传播一步，测量wave_1
                    wave1 = propagate_layer(adj, el_mask, current_wave, refrac, fired_in_av, N, G, rng)
                    wave1_size = int(wave1.sum())
                    kappa_pairs.append((wave0_size, wave1_size))
                    # 继续推进雪崩
                    fired_in_av |= wave1
                    current_wave = wave1
                    refrac[np.array([d])] = T_ABS
                    refrac[refrac > 0] -= 1
                    continue
        
        # 单层传播
        if current_wave.any():
            new_wave = propagate_layer(adj, el_mask, current_wave, refrac, fired_in_av, N, G, rng)
            fired_in_av |= new_wave
            current_wave = new_wave
        
        refrac[current_wave] = T_ABS
        refrac[refrac > 0] -= 1
    
    if not kappa_pairs:
        return 0.0
    w0s = [p[0] for p in kappa_pairs]
    w1s = [p[1] for p in kappa_pairs]
    # Priesemann方法：κ = Σw1 / Σw0
    kappa = sum(w1s) / sum(w0s) if sum(w0s) > 0 else 0.0
    return float(kappa)

# ============ 校准临界G ============
def calibrate_G(adj, el_mask, N, seed):
    """在真实BTW驱动条件下校准G，使κ∈[0.90, 1.10]。"""
    G_lo = G_LO_INIT
    G_hi = G_HI_INIT
    G_best = 0.1
    
    for i in range(CALIB_ITER):
        G_mid = (G_lo + G_hi) / 2
        kappa = estimate_kappa_realcondition(
            adj, el_mask, N, G_mid, seed + i*777,
            n_warmup=CALIB_WARMUP, n_measure=CALIB_STEPS
        )
        print(f"    校准 iter={i+1}: G={G_mid:.5f} → κ={kappa:.4f}")
        sys.stdout.flush()
        
        if 0.90 <= kappa <= 1.10:
            G_best = G_mid
            print(f"    ✅ 校准成功: G={G_best:.5f}, κ={kappa:.4f}")
            return G_best, kappa
        
        if kappa < 0.90:
            G_lo = G_mid
        else:
            G_hi = G_mid
        
        if G_hi - G_lo < 0.0002:
            G_best = G_mid
            break
        G_best = G_mid
    
    kappa_final = estimate_kappa_realcondition(
        adj, el_mask, N, G_best, seed + 9999999,
        n_warmup=CALIB_WARMUP, n_measure=CALIB_STEPS
    )
    print(f"    ⚠️ 校准结束: G={G_best:.5f}, κ={kappa_final:.4f}")
    return G_best, kappa_final

# ============ 雪崩检测 ============
def detect_avalanches(activation_series):
    """检测连续非零激活序列（雪崩），返回尺寸/时长/内部κ列表。"""
    arr = np.array(activation_series, dtype=int)
    sizes, durations, kappas_inner = [], [], []
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
                if len(layers) >= 2:
                    denom = sum(layers[:-1])
                    ki = sum(layers[1:]) / denom if denom > 0 else 0.0
                    kappas_inner.append(ki)
                in_av = False
                layers = []
    if in_av and layers:
        sizes.append(sum(layers))
        durations.append(len(layers))
        if len(layers) >= 2:
            denom = sum(layers[:-1])
            ki = sum(layers[1:]) / denom if denom > 0 else 0.0
            kappas_inner.append(ki)
    return sizes, durations, kappas_inner

# ============ 幂律拟合（Hill MLE + KS最优xmin）============
def fit_powerlaw(data):
    data = np.array([d for d in data if d > 0], dtype=float)
    if len(data) < 30:
        return None, None, len(data), 0.0
    
    # 候选xmin：从最小值到第70百分位数
    p5 = max(1, np.percentile(data, 5))
    p70 = np.percentile(data, 70)
    cands = np.unique(data)
    cands = cands[(cands >= p5) & (cands <= p70)]
    if len(cands) == 0:
        cands = [np.median(data)]
    
    best_ks = np.inf
    best_xmin = p5
    best_tau = 1.5
    
    for xm in cands[:40]:
        tail = data[data >= xm]
        if len(tail) < 15: continue
        lr = np.log(tail / xm)
        if lr.sum() == 0: continue
        tau_e = 1 + len(tail) / lr.sum()
        if tau_e <= 1 or tau_e > 10: continue
        ts = np.sort(tail)
        ecdf = np.arange(1, len(ts)+1) / len(ts)
        tcdf = 1 - (ts/xm)**(-(tau_e-1))
        ks = np.max(np.abs(ecdf - tcdf))
        if ks < best_ks:
            best_ks = ks; best_xmin = xm; best_tau = tau_e
    
    tail = data[data >= best_xmin]
    n_tail = len(tail)
    if n_tail < 10:
        return None, float(best_xmin), n_tail, 0.0
    
    bins = min(20, max(5, n_tail//8))
    counts, edges = np.histogram(tail, bins=bins)
    centers = (edges[:-1]+edges[1:])/2
    msk = counts > 0
    if msk.sum() < 4:
        return float(best_tau), float(best_xmin), n_tail, 0.0
    lx = np.log(centers[msk]); ly = np.log(counts[msk])
    c = np.polyfit(lx, ly, 1)
    fit = np.polyval(c, lx)
    ssr = np.sum((ly-fit)**2); sst = np.sum((ly-np.mean(ly))**2)
    r2 = float(1 - ssr/sst) if sst > 0 else 0.0
    
    return float(best_tau), float(best_xmin), n_tail, r2

# ============ 1/f 功率谱 ============
def compute_psd_slope(activation_series):
    arr = np.array(activation_series, dtype=float)
    arr = arr - arr.mean()
    n = len(arr)
    power = np.abs(np.fft.rfft(arr))**2
    freqs = np.fft.rfftfreq(n)
    mask = (freqs > 0.001) & (freqs < 0.25)
    if mask.sum() < 15: return 0.0, 0.0
    lf = np.log(freqs[mask]); lp = np.log(power[mask]+1e-10)
    c = np.polyfit(lf, lp, 1)
    fit = np.polyval(c, lf)
    ssr = np.sum((lp-fit)**2); sst = np.sum((lp-np.mean(lp))**2)
    r2 = float(1-ssr/sst) if sst > 0 else 0.0
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
    rng_pat = np.random.default_rng(seed+1000)
    patterns = [rng_pat.choice(N, size=stim_size, replace=False).tolist()
                for _ in range(K_PATTERNS)]
    
    topology_log = []
    t0 = time.time()
    pat_idx = 0
    
    # ===== 阶段1：学习（STDP演化拓扑） =====
    print(f"  [{net_name}|seed={seed}] 学习阶段（{N_LEARN}步）...")
    sys.stdout.flush()
    
    for step in range(N_LEARN):
        active = np.zeros(N, dtype=bool)
        if step % 10 == 0 and rng.random() < 0.1:
            pat_idx = int(rng.integers(K_PATTERNS))
        for ni in patterns[pat_idx % K_PATTERNS]:
            if refrac[ni] == 0 and rng.random() < 0.25:
                active[ni] = True
        
        # 单层传播（学习阶段G=1.0）
        if active.any():
            fired = active.copy()
            new_w = propagate_layer(adj, el_mask, active, refrac, fired, N, 1.0, rng)
            active |= new_w
        
        n_act = int(active.sum())
        refrac[active] = T_ABS + T_REL
        refrac[refrac > 0] -= 1
        
        # STDP
        aidx = np.where(active)[0]
        if len(aidx) >= 2:
            n_p = min(len(aidx)*2, 120)
            pre_arr = rng.choice(aidx, size=n_p)
            post_arr = rng.choice(aidx, size=n_p)
            for pre, post in zip(pre_arr, post_arr):
                if pre == post: continue
                dt = int(rng.integers(1, 30))
                if adj[pre, post] > 0:
                    adj[pre, post] = min(1.0, adj[pre, post] + ETA_LTP*np.exp(-dt/TAU_STDP))
                    nltp[pre, post] += 1
                if adj[post, pre] > 0:
                    adj[post, pre] = max(0.0, adj[post, pre] - ETA_LTD*np.exp(-dt/TAU_STDP))
                    nltd[post, pre] += 1
        
        # 固化/消除
        el_ratio = el_mask.sum() / max(1, (adj>0).sum())
        el_mask[(nltp>=THETA_LTP)&(adj>0)&(~el_mask)&(el_ratio<EL_HI)] = True
        ltd_m = (nltd>=THETA_LTD)&(adj>0)&(~el_mask)
        adj[ltd_m] = 0.0; nltp[ltd_m] = nltd[ltd_m] = 0
        el_age[el_mask] += 1
        dm = el_mask & (el_age > T_DECAY)
        el_mask[dm] = False; el_age[dm] = 0
        
        # WS重连
        if step % REWIRE_INT == 0:
            non_el = np.argwhere((adj>0)&(~el_mask))
            for _ in range(max(1, int(len(non_el)*P_REWIRE*0.01))):
                if len(non_el) == 0: break
                ix = int(rng.integers(len(non_el))); i, j = non_el[ix]
                kn = int(rng.integers(N))
                if kn != i and adj[i, kn] == 0:
                    adj[i, kn] = adj[i, j]; adj[i, j] = 0.0
        
        # 突触缩放
        if step % SCALING_INT == 0 and n_act > 0:
            ar = n_act/N
            if ar > KAPPA_TARGET: adj[~el_mask] *= (1-SCALING_RATE)
            elif ar < KAPPA_TARGET*0.5: adj[~el_mask] *= (1+SCALING_RATE)
            adj = np.clip(adj, 0.0, 1.0)
        
        # 修剪（4规则）
        if use_pruning and step % PRUNE_INT == 0 and step > 0:
            deg = (adj>0).sum(axis=1)
            for i, j in np.argwhere((adj>0)&(~el_mask)&(nltp==0)&(nltd==0)):
                if deg[i] > MIN_EDGES and rng.random() < P_PRUNE:
                    adj[i, j] = 0.0
            nltp[:] = 0; nltd[:] = 0
        
        if step % LOG_INT == 0:
            sig = compute_sigma_fast(adj, N)
            print(f"    学习 {step}/{N_LEARN} σ={sig:.2f} edges={(adj>0).sum()} t={time.time()-t0:.0f}s")
            sys.stdout.flush()
            topology_log.append({'step': step, 'sigma': sig, 'n_edges': int((adj>0).sum()),
                                  'n_el': int(el_mask.sum()), 'phase': '学习'})
    
    # 打印学习后网络状态
    edges_after = int((adj>0).sum())
    weights = adj[adj > 0]
    print(f"\n  学习后网络状态: edges={edges_after}, 平均权重={weights.mean():.4f}, σ={compute_sigma_fast(adj,N):.2f}")
    print(f"  理论κ=1点：需要G ≈ {1.0/(edges_after/N*weights.mean()):.4f}")
    sys.stdout.flush()
    
    # ===== 临界点校准（真实BTW条件）=====
    print(f"\n  [{net_name}|seed={seed}] 临界点校准（真实BTW条件）...")
    sys.stdout.flush()
    G_calib, kappa_calib = calibrate_G(adj, el_mask, N, seed)
    print(f"  校准结果: G={G_calib:.5f}, κ={kappa_calib:.4f}")
    sys.stdout.flush()
    
    # ===== 阶段2：雪崩记录 =====
    print(f"\n  [{net_name}|seed={seed}] 记录阶段（{N_RECORD}步，G={G_calib:.4f}）...")
    sys.stdout.flush()
    
    activation_series = []
    refrac[:] = 0
    current_wave = np.zeros(N, dtype=bool)
    fired_in_av = np.zeros(N, dtype=bool)
    
    for step in range(N_RECORD):
        # BTW注入（仅当雪崩已结束）
        if not current_wave.any() and step % BTW_INTERVAL == 0:
            d = int(rng.integers(N))
            if refrac[d] == 0:
                current_wave[d] = True
                fired_in_av[:] = False
                fired_in_av[d] = True
        
        # 单层传播
        if current_wave.any():
            new_wave = propagate_layer(adj, el_mask, current_wave, refrac, fired_in_av, N, G_calib, rng)
            fired_in_av |= new_wave
            current_wave = new_wave
        
        n_wave = int(current_wave.sum())
        activation_series.append(n_wave)
        
        refrac[current_wave] = T_ABS
        refrac[refrac > 0] -= 1
        
        if step % LOG_INT == 0:
            sig = compute_sigma_fast(adj, N)
            print(f"    记录 {step}/{N_RECORD} wave={n_wave} σ={sig:.2f} t={time.time()-t0:.0f}s")
            sys.stdout.flush()
            topology_log.append({'step': N_LEARN+step, 'sigma': sig,
                                  'n_edges': int((adj>0).sum()), 'n_el': int(el_mask.sum()),
                                  'phase': '记录'})
    
    # ============ 雪崩分析 ============
    arr = np.array(activation_series)
    zero_frac = float((arr == 0).mean())
    
    print(f"\n  激活统计:")
    print(f"    零值帧: {zero_frac:.1%} | 最大: {arr.max()} | 平均: {arr.mean():.3f}")
    
    sizes, durations, kappas_inner = detect_avalanches(activation_series)
    
    # 尺寸分布统计
    if sizes:
        sa = np.array(sizes)
        print(f"    尺寸分布: min={sa.min()} 中位数={np.median(sa):.0f} max={sa.max()}")
        print(f"    size=1: {(sa==1).sum()} | size<=5: {(sa<=5).sum()} | size<=20: {(sa<=20).sum()}")
    
    tau_s, xmin_s, n_ts, r2_s = fit_powerlaw(sizes)
    tau_d, xmin_d, n_td, r2_d = fit_powerlaw(durations)
    kappa = float(np.mean(kappas_inner)) if kappas_inner else 0.0
    psd_slope, psd_r2 = compute_psd_slope(activation_series)
    
    n_avalanches = len(sizes)
    mean_size = float(np.mean(sizes)) if sizes else 0.0
    mean_dur = float(np.mean(durations)) if durations else 0.0
    dur_arr = np.array(durations) if durations else np.array([0])
    frac_dur1 = float((dur_arr == 1).mean()) if len(dur_arr) > 0 else 1.0
    
    # 达标判定
    size_ok = (tau_s is not None and 1.2 <= tau_s <= 2.2 and r2_s > 0.70)
    dur_ok = (tau_d is not None and 1.5 <= tau_d <= 2.5 and r2_d > 0.70)
    kappa_ok = (0.85 <= kappa <= 1.15)
    count_ok = (n_avalanches >= 300)
    psd_ok = (psd_slope is not None and -1.5 <= psd_slope <= -0.3)
    zero_ok = (zero_frac >= 0.3)
    multi_ok = (frac_dur1 < 0.8)
    
    score = sum([size_ok, dur_ok, kappa_ok, count_ok, psd_ok, zero_ok, multi_ok])
    
    ts_str = f"{tau_s:.3f}" if tau_s is not None else "N/A"
    td_str = f"{tau_d:.3f}" if tau_d is not None else "N/A"
    ps_str = f"{psd_slope:.3f}" if psd_slope is not None else "N/A"
    
    print(f"\n{'='*60}")
    print(f"  结果 [{net_name}|seed={seed}|{'4-r' if use_pruning else '3-r'}] G={G_calib:.4f}")
    print(f"  零值帧: {zero_frac:.1%} {'✓' if zero_ok else '✗'}")
    print(f"  雪崩数: {n_avalanches} | 均尺寸: {mean_size:.1f} | 均时长: {mean_dur:.1f} {'✓' if count_ok else '✗'}")
    print(f"  多步雪崩: {1-frac_dur1:.1%} {'✓' if multi_ok else '✗'}")
    print(f"  τ_size={ts_str} (R²={r2_s:.3f}) {'✓' if size_ok else '✗'}")
    print(f"  τ_dur={td_str} (R²={r2_d:.3f}) {'✓' if dur_ok else '✗'}")
    print(f"  κ内部={kappa:.4f} {'✓' if kappa_ok else '✗'}")
    print(f"  PSD={ps_str} (R²={psd_r2:.3f}) {'✓' if psd_ok else '✗'}")
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
            'zero_frames': bool(zero_ok), 'size_powerlaw': bool(size_ok),
            'duration_powerlaw': bool(dur_ok), 'branching_ratio': bool(kappa_ok),
            'avalanche_count': bool(count_ok), 'psd_1f': bool(psd_ok),
            'multi_step': bool(multi_ok)
        },
        'topology_log': topology_log,
        'activation_sample': [int(x) for x in activation_series[:6000]],
        'sizes_sample': sorted([int(s) for s in sizes])[:1500],
        'durations_sample': sorted([int(d) for d in durations])[:1500],
    }

# ============ 绘图 ============
def plot_results(all_results):
    fig = plt.figure(figsize=(20, 24))
    fig.suptitle('SDI Experiment 5 v5: Neuronal Avalanche SOC Dynamics\n'
                 'Two-phase protocol: STDP learning -> G calibration (real BTW) -> Avalanche recording',
                 fontsize=12, fontweight='bold', y=0.99)
    gs = GridSpec(6, 3, figure=fig, hspace=0.50, wspace=0.35)
    
    from collections import defaultdict
    bg = defaultdict(list)
    for r in all_results:
        bg[r['network']+'_'+r['rules']].append(r)
    best = {k: max(v, key=lambda x: x['score']) for k, v in bg.items()}
    items = sorted(best.items())[:6]
    colors = {'3-rules': '#2196F3', '4-rules': '#E91E63'}
    
    for pi, (key, res) in enumerate(items):
        if pi >= 6: break
        color = colors.get(res['rules'], '#333')
        row, col = divmod(pi, 3)
        
        ax1 = fig.add_subplot(gs[row*2, col])
        act = res.get('activation_sample', [])
        if act:
            ax1.plot(act[:4000], color=color, linewidth=0.5, alpha=0.8)
        sc = res.get('score', 0)
        G = res.get('G_calib', 1.0)
        kv = res.get('branching_ratio', 0)
        ax1.set_title(f"{res['network']} {res['rules']}\nG={G:.4f} k={kv:.3f} Score={sc}/7",
                     fontsize=7, color='green' if sc>=5 else ('orange' if sc>=3 else 'red'))
        ax1.set_xlabel('Step', fontsize=6)
        ax1.set_ylabel('Wave size', fontsize=6)
        ax1.tick_params(labelsize=6)
        
        ax2 = fig.add_subplot(gs[row*2+1, col])
        sizes = res.get('sizes_sample', [])
        if sizes and len(sizes) > 10:
            sa = np.array(sizes)
            try:
                mn, mx = max(1, sa.min()), max(sa.max(), 2)
                b = np.logspace(np.log10(mn), np.log10(mx), 30)
                cnt, edg = np.histogram(sa, bins=b)
                ctr = (edg[:-1]+edg[1:])/2
                msk = cnt > 0
                if msk.sum() > 3:
                    ax2.loglog(ctr[msk], cnt[msk], 'o', color=color, ms=4, alpha=0.7, label='Data')
                    xt = np.logspace(np.log10(ctr[msk][0]), np.log10(ctr[msk][-1]), 50)
                    y0 = cnt[msk][0] * (ctr[msk][0]**1.5)
                    ax2.loglog(xt, y0/(xt**1.5), '--', color='gray', alpha=0.6, label='tau=1.5')
            except: pass
        ts = res.get('tau_size'); r2s = res.get('r2_size', 0)
        ts_str = f"{ts:.2f}" if ts else "N/A"
        ok = res.get('criteria', {}).get('size_powerlaw', False)
        ax2.set_title(f"tau={ts_str} R2={r2s:.2f} {'V' if ok else 'X'}",
                     fontsize=7, color='green' if ok else 'red')
        ax2.set_xlabel('Avalanche size S', fontsize=6)
        ax2.set_ylabel('Count', fontsize=6)
        ax2.tick_params(labelsize=6)
        ax2.legend(fontsize=5)
    
    plt.savefig(f'{OUT}/exp5_v5_avalanche_results.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Figure saved: {OUT}/exp5_v5_avalanche_results.png")

# ============ 主程序 ============
def main():
    print("="*70)
    print("SDI Experiment 5 v5: Neuronal Avalanche SOC Dynamics")
    print("Key fix: G calibrated under REAL BTW driving conditions (not empty network)")
    print("="*70)
    sys.stdout.flush()
    
    all_results = []
    t_total = time.time()
    
    for rules_label, use_pruning in [('3-rules', False), ('4-rules', True)]:
        print(f"\n[{'3' if not use_pruning else '4'}-rules]")
        for net_name, net_cfg in NETWORKS.items():
            for seed in SEEDS:
                print(f"\n-> {net_name} | seed={seed} | {rules_label}")
                sys.stdout.flush()
                try:
                    result = run_simulation(net_name, net_cfg, seed, use_pruning)
                    all_results.append(result)
                except Exception as e:
                    print(f"  ERROR: {e}")
                    import traceback; traceback.print_exc()
    
    def ser(o):
        if isinstance(o, (np.integer,)): return int(o)
        if isinstance(o, (np.floating,)): return float(o)
        if isinstance(o, np.ndarray): return o.tolist()
        return o
    def ds(o):
        if isinstance(o, dict): return {k: ds(v) for k, v in o.items()}
        if isinstance(o, list): return [ds(v) for v in o]
        return ser(o)
    
    out_path = f'{OUT}/exp5_v5_avalanche_results.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(ds(all_results), f, ensure_ascii=False, indent=2)
    print(f"\nResults saved: {out_path}")
    
    try:
        plot_results(all_results)
    except Exception as e:
        print(f"  Plot error: {e}")
    
    # ============ 汇总 ============
    print("\n" + "="*70)
    print("Summary v5")
    print("="*70)
    
    from collections import defaultdict
    gd = defaultdict(list)
    for r in all_results:
        gd[f"{r['network']}_{r['rules']}"].append(r)
    
    print(f"\n{'Group':<28} {'G':<7} {'kappa':<7} {'tau_s':<7} {'tau_d':<7} {'multi%':<8} {'PSD':<7} {'Score'}")
    print("-"*80)
    
    for key, runs in sorted(gd.items()):
        G = np.mean([r['G_calib'] for r in runs])
        kv = np.mean([r['branching_ratio'] for r in runs])
        ts = [r['tau_size'] for r in runs if r['tau_size'] is not None]
        td = [r['tau_duration'] for r in runs if r['tau_duration'] is not None]
        pv = [r['psd_slope'] for r in runs if r['psd_slope'] is not None]
        md = np.mean([1-r['frac_dur1'] for r in runs])
        sv = [r['score'] for r in runs]
        ts_s = f"{np.mean(ts):.2f}" if ts else "N/A"
        td_s = f"{np.mean(td):.2f}" if td else "N/A"
        pv_s = f"{np.mean(pv):.2f}" if pv else "N/A"
        print(f"{key:<28} {G:<7.4f} {kv:<7.3f} {ts_s:<7} {td_s:<7} {md:.0%}  {pv_s:<7} {np.mean(sv):.1f}/7")
    
    best = max(all_results, key=lambda x: x['score'])
    ts_str = f"{best['tau_size']:.3f}" if best['tau_size'] else "N/A"
    print(f"\nBest: {best['network']} | {best['rules']} | seed={best['seed']}")
    print(f"  tau={ts_str}, kappa={best['branching_ratio']:.3f}, score={best['score']}/7")
    
    elapsed = time.time() - t_total
    print(f"\nTotal: {elapsed:.0f}s ({elapsed/60:.1f}min)")
    print("Experiment 5 v5 complete.")
    sys.stdout.flush()

if __name__ == '__main__':
    main()
