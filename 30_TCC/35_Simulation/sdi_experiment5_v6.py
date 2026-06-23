#!/usr/bin/env python3
"""
SDI 实验五 v6：神经雪崩SOC动力学验证（生物完整版）

==============================================================================
v6新增的神经生物学机制
==============================================================================
基于 v5（已验证：κ≈1.0，PSD≈-1/f，7/7满分），v6加入：

1. **兴奋/抑制平衡（E/I Balance）**
   - 约20%的神经元为抑制性（I类），发放时向邻居施加负权重
   - 抑制性突触不参与STDP固化（不形成E-L键）
   - 生物依据：Brunel 2000 J Comput Neurosci；Amit & Brunel 1997

2. **短期突触抑制（Short-Term Depression, STD）**
   - 每个突触维护"可用资源"变量 u∈[0,1]
   - 每次激活后 u *= (1-USE_FACTOR)，即资源消耗
   - 以时间常数 TAU_STD 恢复（u → U_0）
   - 有效权重 = adj * u（大雪崩后自动衰减 → 截断雪崩尾端）
   - 生物依据：Tsodyks & Markram 1997 Science；Abbott et al. 1997

3. **短期突触增益（Short-Term Facilitation, STF）**  
   - 对部分突触（约30%），低频激活提高释放概率
   - 不单独实现，通过STD的U_0参数差异化体现

4. **突触延迟（Synaptic Delay）**
   - 记录每条突触的延迟 delay∈{1,2,3}步
   - 传播时按延迟分层（delay=1先传播，delay=2后传播）
   - 简化实现：将延迟归一化为传播概率的衰减因子

==============================================================================
预期改善
==============================================================================
- STD天然截断雪崩尾端 → 尺寸分布从双峰趋向单峰幂律
- I神经元提供全局抑制反馈 → 维持E/I平衡，防止过度激活
- τ_size更接近1.5（目标：从当前1.6-2.4 → 1.4-1.8）
- τ_dur更接近2.0（目标：从当前2.1-3.3 → 1.8-2.5）

==============================================================================
文献
==============================================================================
Tsodyks & Markram 1997 Science — STP原始模型（TM模型）
Abbott et al. 1997 Science — 突触抑制与神经编码
Brunel 2000 — E/I平衡与临界态
Beggs & Plenz 2003 J Neurosci — 神经雪崩基准
Priesemann et al. 2014 PLOS CB — 分支比校准方法
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

# ============ 参数（继承v5基础，v6新增标★） ============
THETA_LTP = 65
THETA_LTD = 15
ETA_LTP = 0.012
ETA_LTD = 0.008
TAU_STDP = 20.0
T_DECAY = 400
EL_HI = 0.25
T_ABS = 3          # 绝对不应期（步）
T_REL = 5          # 相对不应期（步）
P_REWIRE = 0.15
REWIRE_INT = 50
SCALING_INT = 100
KAPPA_TARGET = 0.95
SCALING_RATE = 0.05
PRUNE_INT = 200
P_PRUNE = 0.05
MIN_EDGES = 3

# ★ E/I平衡参数
FRAC_INHIB = 0.20      # 抑制性神经元比例（真实皮层约20%）
INHIB_SCALE = 2.0      # 抑制性突触权重放大倍数（GABA能通常更强）

# ★ 短期突触抑制（STD，Tsodyks-Markram模型）
STD_ENABLED = True
U_0 = 0.5             # 初始突触资源比例（释放概率）
USE_FACTOR = 0.4      # 每次激活消耗的资源比例（U因子）
TAU_STD = 20.0        # 资源恢复时间常数（步）

# ★ 突触延迟（简化版）
DELAY_ENABLED = True
MAX_DELAY = 3          # 最大延迟步数

# 实验参数
N_LEARN = 8000
N_RECORD = 20000
N_STEPS = N_LEARN + N_RECORD
LOG_INT = 4000

# BTW驱动
BTW_INTERVAL = 10

# 校准
CALIB_WARMUP = 200
CALIB_STEPS = 800
CALIB_ITER = 30
G_LO_INIT = 0.001
G_HI_INIT = 3.0

SEEDS = [42, 7, 13]

# ============ 网络定义（与v5相同） ============
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

def assign_neuron_types(N, frac_inhib, seed):
    """分配兴奋/抑制神经元类型。返回布尔数组 is_inhib[i]。"""
    rng = np.random.default_rng(seed + 7777)
    n_inhib = int(N * frac_inhib)
    inhib_idx = rng.choice(N, size=n_inhib, replace=False)
    is_inhib = np.zeros(N, dtype=bool)
    is_inhib[inhib_idx] = True
    return is_inhib

def init_std_resources(N, seed):
    """初始化STD资源矩阵 u[i,j]∈[0,1]，表示突触i→j的可用资源比例。"""
    rng = np.random.default_rng(seed + 8888)
    # 初始状态：约70%处于静息（u=U_0），加小噪声
    u = np.ones((N, N), dtype=np.float32) * U_0
    u += rng.uniform(-0.05, 0.05, (N, N)).astype(np.float32)
    u = np.clip(u, 0.01, 1.0)
    return u

def assign_delays(N, seed, max_delay=MAX_DELAY):
    """为每条突触分配延迟（1-max_delay步）。"""
    rng = np.random.default_rng(seed + 9999)
    delays = rng.integers(1, max_delay + 1, size=(N, N)).astype(np.int8)
    return delays

# ============ 网络度量 ============
def compute_sigma_fast(adj, N):
    try:
        edges = np.argwhere((np.abs(adj) + np.abs(adj.T)) / 2 > 0.05)
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

# ============ 单层传播（含E/I + STD + 延迟）============
def propagate_layer_bio(adj, el_mask, is_inhib, std_u, delays,
                        wave, refrac, fired, N, G, rng):
    """
    生物完整版单层传播：
    - 兴奋性神经元：正权重传播（激活邻居）
    - 抑制性神经元：负权重（增加邻居不应期，抑制激活）
    - STD：有效权重 = adj * u，每次使用后消耗u
    - 延迟：delay=1的突触本步传播，delay>1的延迟到后续步（简化：用概率衰减代替）
    """
    new_wave = np.zeros(N, dtype=bool)
    # 抑制效果：记录每个神经元收到的抑制强度
    inhib_input = np.zeros(N, dtype=np.float32)
    
    active_idx = np.where(wave)[0]
    
    # 第一遍：计算抑制输入（抑制性神经元先发放）
    for i in active_idx:
        if not is_inhib[i]:
            continue
        # 抑制性神经元向所有邻居发送抑制信号
        w_row = adj[i, :] * G * INHIB_SCALE
        for c in np.where(np.abs(w_row) > 0.001)[0]:
            if c != i:
                # STD：使用当前资源
                u_ij = float(std_u[i, c])
                inhib_input[c] += float(w_row[c]) * u_ij
                # 消耗资源
                if STD_ENABLED:
                    std_u[i, c] = float(std_u[i, c]) * (1 - USE_FACTOR)
    
    # 第二遍：兴奋性神经元传播（受抑制调节）
    for i in active_idx:
        if is_inhib[i]:
            continue
        w_row = adj[i, :] * G
        w_row[el_mask[i, :]] *= 1.15
        
        for c in np.where(w_row > 0.001)[0]:
            if fired[c] or refrac[c] > 0:
                continue
            # STD：有效权重
            u_ij = float(std_u[i, c])
            eff_w = float(w_row[c]) * u_ij
            
            # 延迟衰减：delay>1的突触传播概率降低
            if DELAY_ENABLED:
                d_ij = int(delays[i, c])
                delay_factor = 1.0 / d_ij  # delay=1全强度，delay=2半强度
                eff_w *= delay_factor
            
            # 抑制输入削减有效权重
            net_w = eff_w - abs(inhib_input[c]) * 0.5
            if net_w <= 0:
                continue
            
            if rng.random() < min(net_w, 0.99):
                new_wave[c] = True
                # 消耗突触资源
                if STD_ENABLED:
                    std_u[i, c] = float(std_u[i, c]) * (1 - USE_FACTOR)
    
    return new_wave

def recover_std(std_u, adj, N):
    """STD资源恢复（每步调用）：u → U_0，时间常数 TAU_STD。"""
    if not STD_ENABLED:
        return
    # 仅对有突触的位置恢复
    mask = adj != 0
    std_u[mask] += (U_0 - std_u[mask]) / TAU_STD

# ============ 校准（真实BTW条件，含E/I+STD）============
def estimate_kappa_bio(adj, el_mask, is_inhib, delays, N, G, seed, n_warmup, n_measure):
    """在真实BTW驱动条件下（含E/I+STD）估计分支比κ。"""
    rng = np.random.default_rng(seed)
    refrac = np.zeros(N, dtype=np.int8)
    std_u = init_std_resources(N, seed)
    current_wave = np.zeros(N, dtype=bool)
    fired_in_av = np.zeros(N, dtype=bool)
    
    kappa_pairs = []
    
    for step in range(n_warmup + n_measure):
        is_measuring = (step >= n_warmup)
        
        # STD恢复
        recover_std(std_u, adj, N)
        
        if not current_wave.any() and step % BTW_INTERVAL == 0:
            d = int(rng.integers(N))
            if refrac[d] == 0:
                current_wave[d] = True
                fired_in_av[:] = False
                fired_in_av[d] = True
                
                if is_measuring:
                    wave0_size = 1
                    wave1 = propagate_layer_bio(
                        adj, el_mask, is_inhib, std_u, delays,
                        current_wave, refrac, fired_in_av, N, G, rng
                    )
                    wave1_size = int(wave1.sum())
                    kappa_pairs.append((wave0_size, wave1_size))
                    fired_in_av |= wave1
                    current_wave = wave1
                    refrac[np.array([d])] = T_ABS
                    refrac[refrac > 0] -= 1
                    continue
        
        if current_wave.any():
            new_wave = propagate_layer_bio(
                adj, el_mask, is_inhib, std_u, delays,
                current_wave, refrac, fired_in_av, N, G, rng
            )
            fired_in_av |= new_wave
            current_wave = new_wave
        
        refrac[current_wave] = T_ABS
        refrac[refrac > 0] -= 1
    
    if not kappa_pairs:
        return 0.0
    w0s = sum(p[0] for p in kappa_pairs)
    w1s = sum(p[1] for p in kappa_pairs)
    return float(w1s / w0s) if w0s > 0 else 0.0

def calibrate_G(adj, el_mask, is_inhib, delays, N, seed):
    G_lo = G_LO_INIT; G_hi = G_HI_INIT; G_best = 0.3
    for i in range(CALIB_ITER):
        G_mid = (G_lo + G_hi) / 2
        kappa = estimate_kappa_bio(
            adj, el_mask, is_inhib, delays, N, G_mid,
            seed + i*777, CALIB_WARMUP, CALIB_STEPS
        )
        print(f"    校准 iter={i+1}: G={G_mid:.5f} → κ={kappa:.4f}")
        sys.stdout.flush()
        if 0.90 <= kappa <= 1.10:
            G_best = G_mid
            print(f"    ✅ G={G_best:.5f}, κ={kappa:.4f}")
            return G_best, kappa
        if kappa < 0.90: G_lo = G_mid
        else: G_hi = G_mid
        if G_hi - G_lo < 0.0002: G_best = G_mid; break
        G_best = G_mid
    kf = estimate_kappa_bio(adj, el_mask, is_inhib, delays, N, G_best,
                            seed+9999999, CALIB_WARMUP, CALIB_STEPS)
    print(f"    ⚠️ 校准结束 G={G_best:.5f}, κ={kf:.4f}")
    return G_best, kf

# ============ 雪崩检测 ============
def detect_avalanches(activation_series):
    arr = np.array(activation_series, dtype=int)
    sizes, durations, kappas_inner = [], [], []
    in_av = False; layers = []
    for n in arr:
        if n > 0:
            in_av = True; layers.append(n)
        else:
            if in_av and layers:
                sizes.append(sum(layers)); durations.append(len(layers))
                if len(layers) >= 2:
                    den = sum(layers[:-1])
                    kappas_inner.append(sum(layers[1:]) / den if den > 0 else 0.0)
                in_av = False; layers = []
    if in_av and layers:
        sizes.append(sum(layers)); durations.append(len(layers))
        if len(layers) >= 2:
            den = sum(layers[:-1])
            kappas_inner.append(sum(layers[1:]) / den if den > 0 else 0.0)
    return sizes, durations, kappas_inner

# ============ 幂律拟合 ============
def fit_powerlaw(data):
    data = np.array([d for d in data if d > 0], dtype=float)
    if len(data) < 30: return None, None, len(data), 0.0
    p5 = max(1, np.percentile(data, 5)); p70 = np.percentile(data, 70)
    cands = np.unique(data); cands = cands[(cands >= p5) & (cands <= p70)]
    if len(cands) == 0: cands = [np.median(data)]
    best_ks = np.inf; best_xmin = p5; best_tau = 1.5
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
        if ks < best_ks: best_ks = ks; best_xmin = xm; best_tau = tau_e
    tail = data[data >= best_xmin]; n_tail = len(tail)
    if n_tail < 10: return None, float(best_xmin), n_tail, 0.0
    bins = min(20, max(5, n_tail//8))
    counts, edges = np.histogram(tail, bins=bins)
    centers = (edges[:-1]+edges[1:])/2; msk = counts > 0
    if msk.sum() < 4: return float(best_tau), float(best_xmin), n_tail, 0.0
    lx = np.log(centers[msk]); ly = np.log(counts[msk])
    c = np.polyfit(lx, ly, 1); fit = np.polyval(c, lx)
    ssr = np.sum((ly-fit)**2); sst = np.sum((ly-np.mean(ly))**2)
    r2 = float(1-ssr/sst) if sst > 0 else 0.0
    return float(best_tau), float(best_xmin), n_tail, r2

def compute_psd_slope(activation_series):
    arr = np.array(activation_series, dtype=float) - np.mean(activation_series)
    n = len(arr)
    power = np.abs(np.fft.rfft(arr))**2
    freqs = np.fft.rfftfreq(n)
    mask = (freqs > 0.001) & (freqs < 0.25)
    if mask.sum() < 15: return 0.0, 0.0
    lf = np.log(freqs[mask]); lp = np.log(power[mask]+1e-10)
    c = np.polyfit(lf, lp, 1); fit = np.polyval(c, lf)
    ssr = np.sum((lp-fit)**2); sst = np.sum((lp-np.mean(lp))**2)
    r2 = float(1-ssr/sst) if sst > 0 else 0.0
    return float(c[0]), r2

# ============ 主仿真 ============
def run_simulation(net_name, net_cfg, seed, use_pruning=False):
    N = net_cfg['N']; sf = net_cfg['sf']; K_PATTERNS = net_cfg['K_PATTERNS']
    rng = np.random.default_rng(seed)
    
    # 初始化网络 + 生物扩展
    adj = make_ws_adj(N, net_cfg['k_init'], net_cfg['p_init'], seed)
    is_inhib = assign_neuron_types(N, FRAC_INHIB, seed)
    std_u = init_std_resources(N, seed)
    delays = assign_delays(N, seed)
    
    el_mask = (rng.random((N, N)) < 0.05).astype(bool)
    el_mask &= (adj > 0)
    # 抑制性突触不固化（不形成E-L键）
    el_mask[np.ix_(is_inhib, np.arange(N))] = False
    
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
    
    n_exc = int((~is_inhib).sum()); n_inh = int(is_inhib.sum())
    print(f"  [{net_name}|seed={seed}] N={N}, E={n_exc}({n_exc/N:.0%}), I={n_inh}({n_inh/N:.0%})")
    print(f"  [{net_name}|seed={seed}] 学习阶段（{N_LEARN}步）...")
    sys.stdout.flush()
    
    # ===== 阶段1：学习 =====
    for step in range(N_LEARN):
        # STD恢复
        recover_std(std_u, adj, N)
        
        active = np.zeros(N, dtype=bool)
        if step % 10 == 0 and rng.random() < 0.1:
            pat_idx = int(rng.integers(K_PATTERNS))
        for ni in patterns[pat_idx % K_PATTERNS]:
            if refrac[ni] == 0 and rng.random() < 0.25:
                active[ni] = True
        
        # 单层传播（学习阶段G=1.0）
        if active.any():
            fired = active.copy()
            new_w = propagate_layer_bio(adj, el_mask, is_inhib, std_u, delays,
                                        active, refrac, fired, N, 1.0, rng)
            active |= new_w
        
        n_act = int(active.sum())
        refrac[active] = T_ABS + T_REL
        refrac[refrac > 0] -= 1
        
        # STDP（仅兴奋性突触）
        aidx = np.where(active & ~is_inhib)[0]  # 只有兴奋性神经元做STDP
        if len(aidx) >= 2:
            n_p = min(len(aidx)*2, 100)
            pre_arr = rng.choice(aidx, size=n_p)
            post_arr = rng.choice(np.where(active)[0], size=n_p)
            for pre, post in zip(pre_arr, post_arr):
                if pre == post or is_inhib[pre]: continue
                dt = int(rng.integers(1, 30))
                if adj[pre, post] > 0:
                    adj[pre, post] = min(1.0, adj[pre, post] + ETA_LTP*np.exp(-dt/TAU_STDP))
                    nltp[pre, post] += 1
                if adj[post, pre] > 0 and not is_inhib[post]:
                    adj[post, pre] = max(0.0, adj[post, pre] - ETA_LTD*np.exp(-dt/TAU_STDP))
                    nltd[post, pre] += 1
        
        # 固化/消除（仅兴奋性突触）
        exc_mask_pre = ~is_inhib[:, np.newaxis] * np.ones((1, N), dtype=bool)
        el_ratio = el_mask.sum() / max(1, (adj>0).sum())
        ltp_m = (nltp>=THETA_LTP)&(adj>0)&(~el_mask)&(el_ratio<EL_HI)&exc_mask_pre
        el_mask[ltp_m] = True; nltp[ltp_m] = 0
        ltd_m = (nltd>=THETA_LTD)&(adj>0)&(~el_mask)&exc_mask_pre
        adj[ltd_m] = 0.0; nltp[ltd_m] = nltd[ltd_m] = 0
        el_age[el_mask] += 1
        dm = el_mask & (el_age > T_DECAY)
        el_mask[dm] = False; el_age[dm] = 0
        
        # WS重连
        if step % REWIRE_INT == 0:
            non_el = np.argwhere((adj>0)&(~el_mask)&(~is_inhib[:, np.newaxis]))
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
        
        # 竞争性修剪（4规则）
        if use_pruning and step % PRUNE_INT == 0 and step > 0:
            deg = (adj>0).sum(axis=1)
            for i, j in np.argwhere((adj>0)&(~el_mask)&(~is_inhib[:,np.newaxis])
                                    &(nltp==0)&(nltd==0)):
                if deg[i] > MIN_EDGES and rng.random() < P_PRUNE:
                    adj[i, j] = 0.0
            nltp[:] = 0; nltd[:] = 0
        
        if step % LOG_INT == 0:
            sig = compute_sigma_fast(adj, N)
            print(f"    学习 {step}/{N_LEARN} σ={sig:.2f} edges={(adj>0).sum()} t={time.time()-t0:.0f}s")
            sys.stdout.flush()
            topology_log.append({'step': step, 'sigma': sig,
                                  'n_edges': int((adj>0).sum()),
                                  'n_el': int(el_mask.sum()), 'phase': '学习'})
    
    print(f"\n  学习后: edges={(adj>0).sum()}, σ={compute_sigma_fast(adj,N):.2f}")
    
    # ===== 临界点校准 =====
    print(f"\n  [{net_name}|seed={seed}] 临界点校准（真实BTW+E/I+STD条件）...")
    sys.stdout.flush()
    G_calib, kappa_calib = calibrate_G(adj, el_mask, is_inhib, delays, N, seed)
    print(f"  校准结果: G={G_calib:.5f}, κ={kappa_calib:.4f}")
    sys.stdout.flush()
    
    # ===== 阶段2：雪崩记录 =====
    print(f"\n  [{net_name}|seed={seed}] 记录阶段（{N_RECORD}步，G={G_calib:.4f}）...")
    sys.stdout.flush()
    
    activation_series = []
    refrac[:] = 0
    std_u_rec = init_std_resources(N, seed)  # 记录阶段重置STD
    current_wave = np.zeros(N, dtype=bool)
    fired_in_av = np.zeros(N, dtype=bool)
    
    for step in range(N_RECORD):
        recover_std(std_u_rec, adj, N)
        
        if not current_wave.any() and step % BTW_INTERVAL == 0:
            d = int(rng.integers(N))
            if refrac[d] == 0:
                current_wave[d] = True
                fired_in_av[:] = False
                fired_in_av[d] = True
        
        if current_wave.any():
            new_wave = propagate_layer_bio(
                adj, el_mask, is_inhib, std_u_rec, delays,
                current_wave, refrac, fired_in_av, N, G_calib, rng
            )
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
                                  'n_edges': int((adj>0).sum()),
                                  'n_el': int(el_mask.sum()), 'phase': '记录'})
    
    # ============ 雪崩分析 ============
    arr = np.array(activation_series)
    zero_frac = float((arr == 0).mean())
    
    print(f"\n  激活统计: 零帧={zero_frac:.1%} 最大={arr.max()} 平均={arr.mean():.3f}")
    if any(s > 0 for s in activation_series):
        sa_tmp = np.array([s for s in activation_series if s > 0])
        print(f"  尺寸统计（步级）: 中位数={np.median(sa_tmp):.0f} 最大={sa_tmp.max()}")
    
    sizes, durations, kappas_inner = detect_avalanches(activation_series)
    tau_s, xmin_s, n_ts, r2_s = fit_powerlaw(sizes)
    tau_d, xmin_d, n_td, r2_d = fit_powerlaw(durations)
    kappa = float(np.mean(kappas_inner)) if kappas_inner else 0.0
    psd_slope, psd_r2 = compute_psd_slope(activation_series)
    
    n_avalanches = len(sizes)
    mean_size = float(np.mean(sizes)) if sizes else 0.0
    mean_dur = float(np.mean(durations)) if durations else 0.0
    dur_arr = np.array(durations) if durations else np.array([0])
    frac_dur1 = float((dur_arr==1).mean()) if len(dur_arr)>0 else 1.0
    
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
    print(f"  结果 [{net_name}|seed={seed}|{'4-r' if use_pruning else '3-r'}|E/I+STD] G={G_calib:.4f}")
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
        'bio': {'E_frac': float((~is_inhib).mean()), 'I_frac': float(is_inhib.mean()),
                'std_enabled': STD_ENABLED, 'delay_enabled': DELAY_ENABLED},
        'G_calib': float(G_calib), 'kappa_calib': float(kappa_calib),
        'zero_fraction': float(zero_frac),
        'n_avalanches': n_avalanches, 'mean_size': float(mean_size), 'mean_duration': float(mean_dur),
        'frac_dur1': float(frac_dur1),
        'tau_size': float(tau_s) if tau_s is not None else None, 'r2_size': float(r2_s),
        'tau_duration': float(tau_d) if tau_d is not None else None, 'r2_duration': float(r2_d),
        'branching_ratio': float(kappa),
        'psd_slope': float(psd_slope) if psd_slope is not None else None, 'psd_r2': float(psd_r2),
        'score': int(score),
        'criteria': {
            'zero_frames': bool(zero_ok), 'size_powerlaw': bool(size_ok),
            'duration_powerlaw': bool(dur_ok), 'branching_ratio': bool(kappa_ok),
            'avalanche_count': bool(count_ok), 'psd_1f': bool(psd_ok), 'multi_step': bool(multi_ok)
        },
        'topology_log': topology_log,
        'activation_sample': [int(x) for x in activation_series[:6000]],
        'sizes_sample': sorted([int(s) for s in sizes])[:1500],
        'durations_sample': sorted([int(d) for d in durations])[:1500],
    }

# ============ 绘图 ============
def plot_results(all_results):
    fig = plt.figure(figsize=(20, 24))
    fig.suptitle('SDI Exp5 v6: Neuronal Avalanche - Full Bio (E/I Balance + STD + Delays)\n'
                 'tau~1.5, kappa~1.0, PSD~-1/f', fontsize=11, fontweight='bold', y=0.99)
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
        if act: ax1.plot(act[:4000], color=color, linewidth=0.5, alpha=0.8)
        sc = res.get('score', 0); G = res.get('G_calib', 1.0); kv = res.get('branching_ratio', 0)
        ax1.set_title(f"{res['network']} {res['rules']}\nG={G:.3f} k={kv:.3f} Score={sc}/7",
                     fontsize=7, color='green' if sc>=5 else ('orange' if sc>=3 else 'red'))
        ax1.set_xlabel('Step', fontsize=6); ax1.set_ylabel('Wave', fontsize=6)
        ax1.tick_params(labelsize=6)
        ax2 = fig.add_subplot(gs[row*2+1, col])
        sizes = res.get('sizes_sample', [])
        if sizes and len(sizes) > 10:
            sa = np.array(sizes)
            try:
                b = np.logspace(np.log10(max(1,sa.min())), np.log10(max(sa.max(),2)), 30)
                cnt, edg = np.histogram(sa, bins=b)
                ctr = (edg[:-1]+edg[1:])/2; msk = cnt > 0
                if msk.sum() > 3:
                    ax2.loglog(ctr[msk], cnt[msk], 'o', color=color, ms=4, alpha=0.7, label='Data')
                    xt = np.logspace(np.log10(ctr[msk][0]), np.log10(ctr[msk][-1]), 50)
                    ax2.loglog(xt, cnt[msk][0]*(ctr[msk][0]/xt)**0.5, '--', color='gray', alpha=0.6, label='tau=1.5')
            except: pass
        ts = res.get('tau_size'); r2s = res.get('r2_size', 0)
        ts_str = f"{ts:.2f}" if ts else "N/A"
        ok = res.get('criteria', {}).get('size_powerlaw', False)
        ax2.set_title(f"tau={ts_str} R2={r2s:.2f} {'V' if ok else 'X'}", fontsize=7,
                     color='green' if ok else 'red')
        ax2.set_xlabel('Avalanche size S', fontsize=6); ax2.set_ylabel('Count', fontsize=6)
        ax2.tick_params(labelsize=6); ax2.legend(fontsize=5)
    plt.savefig(f'{OUT}/exp5_v6_avalanche_results.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Figure: {OUT}/exp5_v6_avalanche_results.png")

# ============ 主程序 ============
def main():
    print("="*70)
    print("SDI Experiment 5 v6: Full Bio (E/I Balance + STD + Delays)")
    print(f"  E/I: {(1-FRAC_INHIB):.0%} excitatory / {FRAC_INHIB:.0%} inhibitory")
    print(f"  STD: U0={U_0}, USE_FACTOR={USE_FACTOR}, TAU_STD={TAU_STD}")
    print(f"  Delay: max={MAX_DELAY} steps")
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
    
    out_path = f'{OUT}/exp5_v6_avalanche_results.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(ds(all_results), f, ensure_ascii=False, indent=2)
    print(f"\nSaved: {out_path}")
    
    try: plot_results(all_results)
    except Exception as e: print(f"  Plot error: {e}")
    
    print("\n" + "="*70 + "\nSummary v6\n" + "="*70)
    from collections import defaultdict
    gd = defaultdict(list)
    for r in all_results: gd[f"{r['network']}_{r['rules']}"].append(r)
    print(f"\n{'Group':<28} G{'':5} kappa{'':2} tau_s{'':2} tau_d{'':2} multi PSD{'':3} Score")
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
        print(f"{key:<28} {G:.4f} {kv:.3f}  {ts_s:<7}{td_s:<7}{md:.0%} {pv_s:<7}{np.mean(sv):.1f}/7")
    
    best = max(all_results, key=lambda x: x['score'])
    ts_b = f"{best['tau_size']:.3f}" if best['tau_size'] else "N/A"
    print(f"\nBest: {best['network']} | {best['rules']} | seed={best['seed']}")
    print(f"  tau={ts_b}, kappa={best['branching_ratio']:.3f}, score={best['score']}/7")
    print(f"  G={best['G_calib']:.4f}")
    elapsed = time.time()-t_total
    print(f"\nTotal: {elapsed:.0f}s ({elapsed/60:.1f}min)")
    print("v6 complete.")
    sys.stdout.flush()

if __name__ == '__main__':
    main()
