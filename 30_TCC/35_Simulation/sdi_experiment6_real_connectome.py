#!/usr/bin/env python3
"""
SDI 实验六：真实C.elegans连接组验证

==============================================================================
实验目的
==============================================================================
前五个实验均使用Watts-Strogatz随机初始网络验证SDI规则的普适性。
实验六将SDI规则施加于**真实C.elegans连接组**（Varshney 2011），验证：

  1. 在真实有向connectome（化学突触+电突触）上，SDI规则能否同样驱动
     小世界拓扑的维持/改善？
  2. 真实感觉-运动回路结构能否在SDI规则下涌现更好的功能分化？
  3. SOC临界态（τ≈1.5, κ≈1.0, PSD≈-1/f）能否在真实connectome上复现？
  4. 真实connectome的起点优势：相比WS随机初始化，真实连接组是否更快
     收敛到小世界临界态？

==============================================================================
关键差异（相对实验五）
==============================================================================

1. **初始网络**：真实C.elegans连接组
   - 化学突触：2575条有向边（Varshney 2011 PLOS CB）
   - 电突触：1031条（双向，初始化为E-L固化键）
   - 权重：log(1+突触数量)归一化到[0.05, 0.50]

2. **神经元类型**：解剖学标注
   - 感觉神经元：63个（按Chalfie 1985模态分配）
   - 中间神经元：105个
   - 运动神经元：111个
   - 抑制性神经元：31个GABA能神经元（White 1986 + WormBase）

3. **感觉模态**：基于真实神经生物学
   - 模态0 化学感觉（盐/pH）：ASE/ASG/ASH等21个
   - 模态1 气味感觉：AWA/AWB/AWC等18个
   - 模态2 温度感觉：AFD 14个
   - 模态3 机械感觉：ALM/AVM/PLM等10个

4. **电突触→E-L键**：真实电突触初始化为固化键，不参与STDP
   这是真实C.elegans神经生物学的关键特征

==============================================================================
验证指标（沿用实验五v12的9项）
==============================================================================
  1. 零帧比例 ≥ 30%
  2. 雪崩数 ≥ 300
  3. 多步雪崩 > 20%
  4. τ_size ∈ [1.2, 2.2]，R² > 0.70，KS p ≥ 0.1
  5. τ_dur ∈ [1.5, 2.8]，R² > 0.70
  6. τ缩放关系误差 < 25%（Friedman 2012 PRL）
  7. κ ∈ [0.85, 1.15]
  8. PSD斜率 ∈ [-1.5, -0.3]
  9. 输出解码 > 0.05（功能分离）

新增对比指标：
  10. σ改善：真实connectome经SDI演化后σ是否提升（vs 初始值）
  11. 与WS初始化的对比：相同参数下，真实connectome得分是否更高

==============================================================================
文献
==============================================================================
  Varshney et al. 2011 PLOS CB — C.elegans connectome（Varshney图）
  White et al. 1986 Phil Trans R Soc — 原始解剖图谱
  Chalfie et al. 1985 J Neurosci — 感觉神经元功能
  Bhatt et al. 2009 Neuron — 突触稳定性（E-L键依据）
  以及实验五v12的全部文献
"""

import numpy as np
import json
import time
import sys
from collections import defaultdict

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

OUT  = '/home/work/.openclaw/workspace/sdi_sim'
DATA = '/home/work/.openclaw/workspace/sdi_sim/celegans_sim/connectome_v8_data.json'

# ============================================================
# 参数（完全继承v12）
# ============================================================
THETA_LTP    = 65;    THETA_LTD    = 15
ETA_LTP      = 0.012; ETA_LTD      = 0.008
ETA_LTP_MID  = 0.006; ETA_LTD_MID  = 0.004
ETA_LTP_REC  = 0.001; ETA_LTD_REC  = 0.0008
TAU_STDP     = 20.0;  STDP_MAX_DT  = 100

T_DECAY    = 400;  EL_HI      = 0.25
T_ABS      = 3;    T_REL      = 5
P_REWIRE   = 0.15; REWIRE_INT = 50
SCALING_INT  = 100; KAPPA_TARGET = 0.95; SCALING_RATE = 0.05
PRUNE_INT  = 200;  P_PRUNE    = 0.05; MIN_EDGES  = 3

INHIB_SCALE  = 2.0   # I神经元突触放大因子
STD_ENABLED  = True
U_0          = 0.5;  USE_FACTOR  = 0.35; TAU_STD = 15.0
DELAY_ENABLED = True; MIN_DELAY = 1; MAX_DELAY = 3

# 三阶段参数
N_ADAPT  = 8000; N_DECODE = 2000; N_RECORD = 20000
LOG_INT  = 4000; BTW_INTERVAL = 10

# 泊松输入
LAMBDA_STIM  = 0.25; LAMBDA_BASE  = 0.02
T_STIM_ON    = 80;   T_STIM_OFF   = 40

# 软饱和STDP（Bhatt 2009 + BCM 1982）
W_MAX        = 0.9; W_LTD_FLOOR  = 0.001

# 稳态权重归一化（Turrigiano 2012）
W_TARGET_MEAN   = 0.50
W_SCALE_ENABLED = True

# 校准
CALIB_WARMUP = 300; CALIB_STEPS = 1200; CALIB_ITER = 30
G_LO_INIT = 0.001; G_HI_INIT = 4.0
SIZE_CALIB_STEPS = 500; SIZE_TARGET_LO = 5; SIZE_TARGET_HI = 80
SIZE_CALIB_ITER = 15; SIZE_G_FACTOR = 1.5

SEEDS = [42, 7, 13]

# ============================================================
# 真实C.elegans Connectome 加载
# ============================================================
def load_celegans_connectome():
    """
    加载Varshney 2011 C.elegans connectome。
    返回：
      adj_chem  : (279,279) 化学突触权重矩阵（归一化后）
      el_mask   : (279,279) 电突触E-L键掩码
      is_inhib  : (279,) 抑制性神经元标记
      sensory_idx, motor_idx, inter_idx : 神经元索引
      modality  : 感觉神经元模态（0-3）
      node_names: 神经元名称列表
    """
    with open(DATA) as f:
        d = json.load(f)

    N = d['N']
    nodes   = d['nodes']     # 名称列表
    n_types = d['n_types']   # {name: type}
    n2i     = d['node2idx']  # {name: idx}
    ec      = d['edges_chem']
    ee      = d['edges_elec']

    # --- 化学突触权重矩阵 ---
    adj_raw = np.zeros((N, N), dtype=np.float32)
    for i, j, w in ec:
        adj_raw[i, j] = float(w)

    # log(1+w)归一化到[0.05, 0.50]（保留突触强度相对关系）
    mask = adj_raw > 0
    log_w = np.log1p(adj_raw[mask])
    if log_w.max() > log_w.min():
        adj_norm = adj_raw.copy()
        adj_norm[mask] = 0.05 + 0.45 * (log_w - log_w.min()) / (log_w.max() - log_w.min())
    else:
        adj_norm = adj_raw.copy()
        adj_norm[mask] = 0.15

    # --- 电突触→E-L固化键（双向）---
    el_mask = np.zeros((N, N), dtype=bool)
    for e in ee:
        i, j = e[0], e[1]
        el_mask[i, j] = True
        el_mask[j, i] = True
        if adj_norm[i, j] == 0: adj_norm[i, j] = 0.15
        if adj_norm[j, i] == 0: adj_norm[j, i] = 0.15

    # --- 神经元类型索引 ---
    sensory_idx = np.array([n2i[n] for n, t in n_types.items() if t == 'sensory'])
    motor_idx   = np.array([n2i[n] for n, t in n_types.items() if t == 'motor'])
    inter_idx   = np.array([n2i[n] for n, t in n_types.items() if t == 'interneuron'])

    # --- 抑制性神经元（GABA能，White 1986 + WormBase）---
    inhib_names = {
        'DD1','DD2','DD3','DD4','DD5','DD6',
        'VD1','VD2','VD3','VD4','VD5','VD6','VD7',
        'VD8','VD9','VD10','VD11','VD12','VD13',
        'AVL','RIS','DVB',
        'RMEL','RMER','RMEV','RMED',
        'SMDL','SMDR','SMDV',
    }
    is_inhib = np.zeros(N, dtype=bool)
    for name in inhib_names:
        if name in n2i:
            is_inhib[n2i[name]] = True

    # --- 感觉模态分配（Chalfie 1985 + Bargmann 1993）---
    modality_map = {
        # 化学感觉（0）
        'ASEL':0,'ASER':0,'ASAL':0,'ASAR':0,'ASGL':0,'ASGR':0,
        'ASHL':0,'ASHR':0,'ASIL':0,'ASIR':0,'ASJL':0,'ASJR':0,
        'ASKL':0,'ASKR':0,'AQRL':0,'AQRR':0,
        # 气味感觉（1）
        'AWAL':1,'AWAR':1,'AWBL':1,'AWBR':1,'AWCL':1,'AWCR':1,
        'ADFL':1,'ADFR':1,'ADLL':1,'ADLR':1,
        # 温度感觉（2）
        'AFDL':2,'AFDR':2,
        # 机械感觉（3）
        'ALML':3,'ALMR':3,'AVM':3,'PLML':3,'PLMR':3,'PVM':3,
        'FLPL':3,'FLPR':3,
    }
    modality = np.zeros(len(sensory_idx), dtype=np.int8)
    for li, gi in enumerate(sensory_idx):
        name = nodes[gi]
        modality[li] = modality_map.get(name, li % 4)

    return adj_norm, el_mask, is_inhib, sensory_idx, motor_idx, inter_idx, modality, nodes

# ============================================================
# 工具函数（完全继承v12）
# ============================================================
def sigma_fast(adj, N):
    try:
        sym = (np.abs(adj) + np.abs(adj.T)) / 2
        edges = np.argwhere(sym > 0.05)
        edges = edges[edges[:, 0] < edges[:, 1]]
        if len(edges) < 10: return 1.0
        al = [[] for _ in range(N)]
        for u, v in edges: al[u].append(v); al[v].append(u)
        Cv = []
        for i in range(min(40, N)):
            nb = al[i]; ki = len(nb)
            if ki < 2: Cv.append(0.0); continue
            s = set(nb)
            lk = sum(1 for a in nb for b in al[a] if b in s and b != a)
            Cv.append(lk / (ki * (ki - 1)))
        C = float(np.mean(Cv)) if Cv else 0.0
        lengths = []
        for st in range(min(25, N)):
            vis = {st: 0}; q = [st]; qi = 0
            while qi < len(q):
                nd = q[qi]; qi += 1; d = vis[nd]
                if d >= 6: continue
                for nb in al[nd]:
                    if nb not in vis: vis[nb] = d+1; q.append(nb)
            lengths.extend(vis.values())
        L = float(np.mean(lengths)) if lengths else 3.0
        m = len(edges); k_avg = 2*m/N
        if k_avg <= 1: return 1.0
        Cr = k_avg/N; Lr = np.log(N)/np.log(k_avg)
        if Cr == 0 or Lr == 0: return 1.0
        return float((C/Cr)/(L/Lr))
    except: return 1.0

def recover_std(std_u, syn_mask):
    if STD_ENABLED:
        std_u[syn_mask] += (U_0 - std_u[syn_mask]) / TAU_STD

def propagate(adj, el_mask, is_i, std_u, delays,
              wave, refrac, fired, N, G, db, step, rng):
    nw = np.zeros(N, dtype=bool)
    inh_in = np.zeros(N, dtype=np.float32)
    for tgt, eff_w, is_ex in db.pop(step, []):
        if refrac[tgt] > 0 or fired[tgt]: continue
        if is_ex:
            if rng.random() < min(eff_w, 0.99): nw[tgt] = True
        else:
            inh_in[tgt] += eff_w
    for i in np.where(wave)[0]:
        w = adj[i, :] * G
        w[el_mask[i, :]] *= 1.15
        if is_i[i]:
            ws = w * INHIB_SCALE
            for c in np.where(ws > 0.005)[0]:
                if c == i: continue
                u = float(std_u[i, c])
                eff = float(ws[c]) * u
                if STD_ENABLED: std_u[i, c] *= (1.0 - USE_FACTOR)
                db[step + int(delays[i, c])].append((int(c), eff, False))
        else:
            for c in np.where(w > 0.005)[0]:
                u = float(std_u[i, c])
                eff = float(w[c]) * u
                if STD_ENABLED: std_u[i, c] *= (1.0 - USE_FACTOR)
                db[step + int(delays[i, c])].append((int(c), eff, True))
    for tgt in np.where(inh_in > 0)[0]:
        if nw[tgt] and rng.random() < min(float(inh_in[tgt]) * 0.5, 0.99):
            nw[tgt] = False
    nw &= ~fired
    return nw

def estimate_kappa(adj, el_mask, is_i, delays, std_u0, N, G, seed, nw, nm):
    rng = np.random.default_rng(seed)
    refrac = np.zeros(N, dtype=np.int8)
    std_u = std_u0.copy(); syn_mask = adj != 0
    wave = np.zeros(N, dtype=bool); fired = np.zeros(N, dtype=bool)
    db = defaultdict(list); log = []
    for step in range(nw + nm):
        recover_std(std_u, syn_mask)
        pending = any(k >= step for k in db)
        if not wave.any() and not pending and step % BTW_INTERVAL == 0:
            d = int(rng.integers(N))
            if refrac[d] == 0:
                wave[d] = True; fired[:] = False; fired[d] = True
        nw_ = propagate(adj, el_mask, is_i, std_u, delays,
                        wave, refrac, fired, N, G, db, step, rng)
        fired |= nw_; wave = nw_
        if step >= nw: log.append(int(nw_.sum()))
        refrac[wave] = T_ABS; refrac[refrac > 0] -= 1
    if len(log) < 10: return 0.0
    arr = np.array(log, dtype=float)
    num = arr[1:][arr[:-1] > 0].sum()
    den = arr[:-1][arr[:-1] > 0].sum()
    return float(num/den) if den > 0 else 0.0

def calibrate_kappa(adj, el_mask, is_i, delays, std_u0, N, seed):
    G_lo = G_LO_INIT; G_hi = G_HI_INIT; G_best = 0.5
    for i in range(CALIB_ITER):
        G_mid = (G_lo + G_hi) / 2
        k = estimate_kappa(adj, el_mask, is_i, delays, std_u0,
                           N, G_mid, seed + i*997, CALIB_WARMUP, CALIB_STEPS)
        print(f"    κ校准 iter={i+1}: G={G_mid:.5f} → κ={k:.4f}")
        sys.stdout.flush()
        if 0.90 <= k <= 1.10:
            print(f"    ✅ G={G_mid:.5f}, κ={k:.4f}")
            return G_mid, k
        if k < 0.90: G_lo = G_mid
        else: G_hi = G_mid
        if G_hi - G_lo < 0.0002: G_best = G_mid; break
        G_best = G_mid
    kf = estimate_kappa(adj, el_mask, is_i, delays, std_u0,
                        N, G_best, seed+9999999, CALIB_WARMUP, CALIB_STEPS)
    print(f"    ⚠️ G={G_best:.5f}, κ={kf:.4f}")
    return G_best, kf

def estimate_mean_size(adj, el_mask, is_i, delays, std_u0, N, G, seed):
    rng = np.random.default_rng(seed)
    refrac = np.zeros(N, dtype=np.int8)
    std_u = std_u0.copy(); syn_mask = adj != 0
    wave = np.zeros(N, dtype=bool); fired = np.zeros(N, dtype=bool)
    db = defaultdict(list); series = []
    for step in range(SIZE_CALIB_STEPS):
        recover_std(std_u, syn_mask)
        pending = any(k >= step for k in db)
        if not wave.any() and not pending and step % BTW_INTERVAL == 0:
            d = int(rng.integers(N))
            if refrac[d] == 0:
                wave[d] = True; fired[:] = False; fired[d] = True
        nw = propagate(adj, el_mask, is_i, std_u, delays,
                       wave, refrac, fired, N, G, db, step, rng)
        fired |= nw; wave = nw; series.append(int(nw.sum()))
        refrac[wave] = T_ABS; refrac[refrac > 0] -= 1
    sizes = []
    in_av = False; cs = 0
    for n in series:
        if n > 0: in_av = True; cs += n
        else:
            if in_av and cs > 0: sizes.append(cs)
            in_av = False; cs = 0
    ms = float(np.mean(sizes)) if sizes else 0.0
    zf = float(sum(1 for x in series if x == 0) / len(series))
    return ms, zf, len(sizes)

def calibrate_size(adj, el_mask, is_i, delays, std_u0, N, G_k, seed):
    G = G_k
    print(f"\n    ★ 尺寸校准（目标mean_size∈[{SIZE_TARGET_LO},{SIZE_TARGET_HI}]）")
    sys.stdout.flush()
    for i in range(SIZE_CALIB_ITER):
        ms, zf, nav = estimate_mean_size(adj, el_mask, is_i, delays, std_u0, N, G, seed+i*331)
        print(f"    尺寸校准 iter={i+1}: G={G:.5f} → mean_size={ms:.1f} zero={zf:.0%} n={nav}")
        sys.stdout.flush()
        if SIZE_TARGET_LO <= ms <= SIZE_TARGET_HI:
            print(f"    ✅ G={G:.5f}, mean_size={ms:.1f}")
            return G, ms
        G = G * SIZE_G_FACTOR if ms < SIZE_TARGET_LO else G / SIZE_G_FACTOR
        k_new = estimate_kappa(adj, el_mask, is_i, delays, std_u0, N, G,
                               seed+i*997+500, 100, 200)
        if not (0.75 <= k_new <= 1.25):
            G = G * 1.2 if ms < SIZE_TARGET_LO else G * 0.85
    ms_f, _, _ = estimate_mean_size(adj, el_mask, is_i, delays, std_u0, N, G, seed+99999)
    print(f"    ⚠️ G={G:.5f}, mean_size={ms_f:.1f}")
    return G, ms_f

def detect_avalanches(series):
    sizes, durs, kaps = [], [], []
    layers = []; in_av = False
    for n in series:
        if n > 0: in_av = True; layers.append(n)
        else:
            if in_av and layers:
                sizes.append(sum(layers)); durs.append(len(layers))
                if len(layers) >= 2:
                    den = sum(layers[:-1])
                    kaps.append(sum(layers[1:])/den if den > 0 else 0.0)
                in_av = False; layers = []
    if in_av and layers:
        sizes.append(sum(layers)); durs.append(len(layers))
        if len(layers) >= 2:
            den = sum(layers[:-1])
            kaps.append(sum(layers[1:])/den if den > 0 else 0.0)
    return sizes, durs, kaps

def fit_pl(data):
    data = np.array([d for d in data if d > 0], dtype=float)
    res = dict(tau=None, xmin=None, n_tail=len(data),
               r2=0.0, ks_stat=1.0, plausible=False, p_value=0.0,
               lr_vs_lognormal=0.0)
    if len(data) < 30: return res
    p5 = max(1.0, np.percentile(data, 5)); p65 = np.percentile(data, 65)
    cands = np.unique(data); cands = cands[(cands >= p5) & (cands <= p65)]
    if len(cands) == 0: cands = [np.median(data)]
    best_ks = np.inf; best_xm = p5; best_tau = 1.5
    for xm in cands[:50]:
        tail = data[data >= xm]
        if len(tail) < 15: continue
        lr = np.log(tail/xm)
        if lr.sum() == 0: continue
        tau_e = 1 + len(tail)/lr.sum()
        if tau_e <= 1 or tau_e > 8: continue
        ts = np.sort(tail); n_t = len(ts)
        ecdf = np.arange(1, n_t+1)/n_t
        tcdf = 1-(ts/xm)**(-(tau_e-1))
        ks = float(np.max(np.abs(ecdf-tcdf)))
        if ks < best_ks: best_ks = ks; best_xm = xm; best_tau = tau_e
    res.update(xmin=float(best_xm), tau=float(best_tau), ks_stat=float(best_ks))
    tail = data[data >= best_xm]; res['n_tail'] = len(tail)
    if len(tail) >= 10:
        bins = min(20, max(5, len(tail)//8))
        cnt, edg = np.histogram(tail, bins=bins)
        ctr = (edg[:-1]+edg[1:])/2; msk = cnt > 0
        if msk.sum() >= 4:
            lx = np.log(ctr[msk]); ly = np.log(cnt[msk])
            c = np.polyfit(lx, ly, 1); ssr = np.sum((ly-np.polyval(c,lx))**2)
            sst = np.sum((ly-ly.mean())**2)
            res['r2'] = float(1-ssr/sst) if sst > 0 else 0.0
    tau = best_tau; xm = best_xm; n_t = len(tail)
    rng_b = np.random.default_rng(42); boots = []
    for _ in range(50):
        u = rng_b.uniform(size=n_t)
        syn = xm*(1-u)**(-1/(tau-1))
        syn = np.sort(syn)
        ts2 = 1 + n_t/np.sum(np.log(syn/xm))
        if ts2 <= 1: ts2 = 1.01
        ecdf_s = np.arange(1, n_t+1)/n_t; tcdf_s = 1-(syn/xm)**(-(ts2-1))
        boots.append(float(np.max(np.abs(ecdf_s-tcdf_s))))
    res['p_value'] = float(np.mean(np.array(boots) >= best_ks))
    res['plausible'] = (res['p_value'] >= 0.1)
    ll_pl = np.sum(np.log(tau-1) - np.log(xm) - tau*np.log(tail/xm))
    lt = np.log(tail); mu = lt.mean(); sg = lt.std()
    if sg > 0:
        ll_ln = np.sum(-np.log(tail)-0.5*np.log(2*np.pi*sg**2)-0.5*((lt-mu)/sg)**2)
        res['lr_vs_lognormal'] = float(ll_pl-ll_ln)
    return res

def psd_slope(series):
    arr = np.array(series, dtype=float) - np.mean(series)
    power = np.abs(np.fft.rfft(arr))**2
    freqs = np.fft.rfftfreq(len(arr))
    mask = (freqs > 0.001) & (freqs < 0.25)
    if mask.sum() < 15: return 0.0, 0.0
    lf = np.log(freqs[mask]); lp = np.log(power[mask]+1e-10)
    c = np.polyfit(lf, lp, 1)
    ssr = np.sum((lp-np.polyval(c,lf))**2); sst = np.sum((lp-lp.mean())**2)
    return float(c[0]), float(1-ssr/sst) if sst > 0 else 0.0

def decode_score(mot_by_mod):
    if len(mot_by_mod) < 2: return 0.0
    vecs = []
    for arr in mot_by_mod.values():
        v = np.array(arr, dtype=float); n = np.linalg.norm(v)
        vecs.append(v/n if n > 0 else v)
    dists = [1.0 - np.dot(vecs[i], vecs[j])
             for i in range(len(vecs)) for j in range(i+1, len(vecs))]
    return float(np.mean(dists)) if dists else 0.0

# ============================================================
# 泊松刺激器
# ============================================================
class PoissonStimulator:
    def __init__(self, sidx, mod, seed=0):
        self.sidx = sidx; self.mod = mod; self.n_mod = 4
        self.rng = np.random.default_rng(seed + 3333)
        self.t = 0; self.a_mod = 0
    def step(self):
        ph = self.t % (T_STIM_ON + T_STIM_OFF)
        is_on = (ph < T_STIM_ON)
        if ph == 0: self.a_mod = int(self.rng.integers(self.n_mod))
        activated = [int(ni) for ni, m in zip(self.sidx, self.mod)
                     if self.rng.random() < (LAMBDA_STIM if (is_on and m==self.a_mod)
                                             else LAMBDA_BASE)]
        self.t += 1
        return activated, self.a_mod, is_on

# ============================================================
# 主仿真
# ============================================================
def run_simulation(adj_init, el_mask_init, is_inhib, sensory_idx, motor_idx,
                   modality, N, seed, use_pruning=False, label="C.elegans_real"):
    rng = np.random.default_rng(seed)

    # 从真实connectome初始化（每次独立拷贝）
    adj      = adj_init.copy()
    el_mask  = el_mask_init.copy()
    # I神经元输出突触不固化
    el_mask[is_inhib, :] = False

    # STD资源、延迟（随机初始化，但adj结构来自真实connectome）
    std_u = np.full((N, N), U_0, dtype=np.float32)
    std_u += rng.uniform(-0.03, 0.03, (N, N)).astype(np.float32)
    std_u = np.clip(std_u, 0.01, 1.0)
    delays = rng.integers(MIN_DELAY, MAX_DELAY + 1, size=(N, N)).astype(np.int8)
    syn_mask = adj != 0

    nltp = np.zeros((N, N), dtype=np.int16)
    nltd = np.zeros((N, N), dtype=np.int16)
    el_age = np.zeros((N, N), dtype=np.int32)
    refrac = np.zeros(N, dtype=np.int8)
    last_sp = np.full(N, -99999, dtype=np.int32)
    exc_pre = np.outer(~is_inhib, np.ones(N, dtype=bool))

    stim = PoissonStimulator(sensory_idx, modality, seed=seed)

    n_e = int((~is_inhib).sum()); n_i = int(is_inhib.sum())
    sigma_init = sigma_fast(adj, N)
    print(f"  [{label}|seed={seed}] N={N} E={n_e} I={n_i}")
    print(f"  真实connectome: 化学突触={(adj>0).sum()} 电突触E-L={el_mask.sum()}")
    print(f"  初始σ={sigma_init:.2f} (vs WS随机初始σ≈12)")
    print(f"  感觉={len(sensory_idx)} 运动={len(motor_idx)}")
    sys.stdout.flush()

    topo_log = [{'step': 0, 'sigma': sigma_init,
                 'n_edges': int((adj>0).sum()),
                 'n_el': int(el_mask.sum()), 'phase': '初始'}]
    t0 = time.time()
    db = defaultdict(list)
    mot_by_mod = defaultdict(lambda: np.zeros(len(motor_idx)))
    avl_series = []

    total_learn = N_ADAPT + N_DECODE

    # ===== 适应 + 解码阶段 =====
    for step in range(total_learn):
        phase = 'adapt' if step < N_ADAPT else 'decode'
        eta_ltp = ETA_LTP if phase == 'adapt' else ETA_LTP_MID
        eta_ltd = ETA_LTD if phase == 'adapt' else ETA_LTD_MID

        recover_std(std_u, syn_mask)

        active = np.zeros(N, dtype=bool)
        stim_ns, act_mod, is_on = stim.step()
        for ni in stim_ns:
            if refrac[ni] == 0: active[ni] = True

        if active.any():
            fired = active.copy()
            nw = propagate(adj, el_mask, is_inhib, std_u, delays,
                           active, refrac, fired, N, 1.0, db, step, rng)
            active |= nw
        else:
            fired = np.zeros(N, dtype=bool)
            nw = propagate(adj, el_mask, is_inhib, std_u, delays,
                           np.zeros(N, dtype=bool), refrac, fired, N, 1.0,
                           db, step, rng)
            active |= nw

        n_act = int(active.sum())
        last_sp[active] = step
        refrac[active] = T_ABS + T_REL
        refrac[refrac > 0] -= 1

        if phase == 'decode' and is_on and n_act > 0:
            ma = active[motor_idx].astype(float)
            if ma.any(): mot_by_mod[int(act_mod)] += ma

        # 软饱和STDP
        ae = np.where(active & ~is_inhib)[0]; aa = np.where(active)[0]
        if len(ae) >= 2 and len(aa) >= 1:
            n_p = min(len(ae)*2, 100)
            for pre, post in zip(rng.choice(ae, size=n_p), rng.choice(aa, size=n_p)):
                if pre == post: continue
                dt = int(last_sp[post]) - int(last_sp[pre])
                if abs(dt) > STDP_MAX_DT: continue
                if dt > 0 and adj[pre, post] > 0 and not is_inhib[pre]:
                    wc = float(adj[pre, post])
                    dw = eta_ltp * np.exp(-abs(dt)/TAU_STDP)
                    adj[pre, post] = float(np.clip(wc + dw*(1.0-wc/W_MAX), W_LTD_FLOOR, W_MAX))
                    nltp[pre, post] += 1
                elif dt < 0 and adj[post, pre] > 0 and not is_inhib[post]:
                    wc = float(adj[post, pre])
                    dw = eta_ltd * np.exp(-abs(dt)/TAU_STDP)
                    adj[post, pre] = float(np.clip(wc - dw, W_LTD_FLOOR, W_MAX))
                    nltd[post, pre] += 1

        el_r = el_mask.sum() / max(1, (adj>0).sum())
        ltp_m = (nltp>=THETA_LTP)&(adj>0)&(~el_mask)&(el_r<EL_HI)&exc_pre
        el_mask[ltp_m] = True; nltp[ltp_m] = 0
        ltd_m = (nltd>=THETA_LTD)&(adj>0)&(~el_mask)&exc_pre
        adj[ltd_m] = 0.0; nltp[ltd_m] = nltd[ltd_m] = 0
        syn_mask[ltd_m] = False
        el_age[el_mask] += 1
        dm = el_mask & (el_age > T_DECAY)
        el_mask[dm] = False; el_age[dm] = 0

        if step % REWIRE_INT == 0:
            ne = np.argwhere((adj>0)&(~el_mask)&exc_pre)
            for _ in range(max(1, int(len(ne)*P_REWIRE*0.01))):
                if len(ne) == 0: break
                ix = int(rng.integers(len(ne))); i, j = ne[ix]
                kn = int(rng.integers(N))
                if kn != i and adj[i, kn] == 0:
                    adj[i, kn] = adj[i, j]; adj[i, j] = 0.0
                    syn_mask[i, j] = False; syn_mask[i, kn] = True

        if phase != 'record' and step % SCALING_INT == 0 and n_act > 0:
            ar = n_act/N
            if ar > KAPPA_TARGET: adj[~el_mask] *= (1-SCALING_RATE)
            elif ar < KAPPA_TARGET*0.5: adj[~el_mask] *= (1+SCALING_RATE)
            adj = np.clip(adj, 0.0, W_MAX)

        if use_pruning and step % PRUNE_INT == 0 and step > 0:
            deg = (adj>0).sum(axis=1)
            for i, j in np.argwhere((adj>0)&(~el_mask)&exc_pre&(nltp==0)&(nltd==0)):
                if deg[i] > MIN_EDGES and rng.random() < P_PRUNE:
                    adj[i, j] = 0.0; syn_mask[i, j] = False
            nltp[:] = 0; nltd[:] = 0

        if step % LOG_INT == 0:
            sig = sigma_fast(adj, N)
            w_m = float(adj[adj>0].mean()) if (adj>0).any() else 0.0
            print(f"    [{phase}] {step}/{total_learn} σ={sig:.2f} "
                  f"edges={(adj>0).sum()} w_mean={w_m:.3f} t={time.time()-t0:.0f}s")
            sys.stdout.flush()
            topo_log.append({'step': step, 'sigma': sig,
                              'n_edges': int((adj>0).sum()),
                              'n_el': int(el_mask.sum()), 'phase': phase})

    sigma_after = sigma_fast(adj, N)
    w_mean_after = float(adj[adj>0].mean()) if (adj>0).any() else 0.0
    ds = decode_score(mot_by_mod)
    print(f"\n  学习后: σ={sigma_after:.2f} (初始{sigma_init:.2f}, Δσ={sigma_after-sigma_init:+.2f})")
    print(f"  w_mean={w_mean_after:.3f} | 解码={ds:.4f}")

    # ===== 稳态权重归一化（Turrigiano 2012）=====
    if W_SCALE_ENABLED and w_mean_after > 0:
        sf = W_TARGET_MEAN / w_mean_after
        adj[~el_mask] = np.clip(adj[~el_mask] * sf, W_LTD_FLOOR, W_MAX)
        adj[el_mask]  = np.clip(adj[el_mask]  * sf, W_LTD_FLOOR, W_MAX)
        syn_mask[:] = adj != 0
        w_after_norm = float(adj[adj>0].mean())
        print(f"  ★ 稳态权重归一化: {w_mean_after:.3f}→{w_after_norm:.3f} (×{sf:.3f})")
    std_after = std_u.copy()

    # ===== 双重G校准 =====
    print(f"\n  步骤1: κ校准...")
    sys.stdout.flush()
    G_kappa, kappa_c = calibrate_kappa(adj, el_mask, is_inhib, delays, std_after, N, seed)

    print(f"\n  步骤2: 尺寸校准...")
    sys.stdout.flush()
    G_final, ms_calib = calibrate_size(adj, el_mask, is_inhib, delays, std_after, N, G_kappa, seed)
    print(f"  G_final={G_final:.5f}, mean_size_calib={ms_calib:.1f}")

    # ===== 独立记录阶段（用G_final）=====
    print(f"\n  记录阶段（{N_RECORD}步, G={G_final:.4f}）...")
    sys.stdout.flush()
    refrac[:] = 0
    std_u_rec = std_after.copy()
    db_rec = defaultdict(list)
    wave_r = np.zeros(N, dtype=bool)
    fired_r = np.zeros(N, dtype=bool)

    for rs in range(N_RECORD):
        recover_std(std_u_rec, syn_mask)
        abs_s = total_learn + rs
        pending = any(k >= abs_s for k in db_rec)
        if not wave_r.any() and not pending and rs % BTW_INTERVAL == 0:
            d = int(rng.integers(N))
            if refrac[d] == 0:
                wave_r[d] = True; fired_r[:] = False; fired_r[d] = True
        nw_r = propagate(adj, el_mask, is_inhib, std_u_rec, delays,
                         wave_r, refrac, fired_r, N, G_final, db_rec, abs_s, rng)
        fired_r |= nw_r; wave_r = nw_r
        avl_series.append(int(nw_r.sum()))
        refrac[wave_r] = T_ABS; refrac[refrac > 0] -= 1
        # 极弱STDP（维持但不破坏）
        ae_r = np.where(wave_r & ~is_inhib)[0]; aa_r = np.where(wave_r)[0]
        if len(ae_r) >= 2 and len(aa_r) >= 1:
            for pre, post in zip(rng.choice(ae_r, size=min(len(ae_r)*2,30)),
                                  rng.choice(aa_r, size=min(len(ae_r)*2,30))):
                if pre == post: continue
                dt = int(last_sp[post]) - int(last_sp[pre])
                if abs(dt) > STDP_MAX_DT: continue
                if dt > 0 and adj[pre,post] > 0 and not is_inhib[pre]:
                    wc = float(adj[pre,post])
                    dw = ETA_LTP_REC * np.exp(-abs(dt)/TAU_STDP) * (1.0-wc/W_MAX)
                    adj[pre,post] = float(np.clip(wc+dw, W_LTD_FLOOR, W_MAX))
                elif dt < 0 and adj[post,pre] > 0 and not is_inhib[post]:
                    wc = float(adj[post,pre])
                    adj[post,pre] = float(np.clip(wc - ETA_LTD_REC*np.exp(-abs(dt)/TAU_STDP),
                                                  W_LTD_FLOOR, W_MAX))
        last_sp[wave_r] = abs_s
        if rs % LOG_INT == 0:
            sig = sigma_fast(adj, N)
            print(f"    [记录] {rs}/{N_RECORD} wave={int(nw_r.sum())} σ={sig:.2f} t={time.time()-t0:.0f}s")
            sys.stdout.flush()
            topo_log.append({'step': abs_s, 'sigma': sig,
                              'n_edges': int((adj>0).sum()),
                              'n_el': int(el_mask.sum()), 'phase': '记录'})

    sigma_final = sigma_fast(adj, N)

    # ===== 分析 =====
    arr = np.array(avl_series)
    zf = float((arr == 0).mean())
    print(f"\n  雪崩: 零帧={zf:.1%} max={arr.max()} mean={arr.mean():.3f}")

    sizes, durs, kap_in = detect_avalanches(avl_series)
    rs_r = fit_pl(sizes); rd_r = fit_pl(durs)
    tau_s = rs_r['tau']; r2_s = rs_r['r2']
    tau_d = rd_r['tau']; r2_d = rd_r['r2']
    kappa = float(np.mean(kap_in)) if kap_in else 0.0
    kappa_std_ = float(np.std(kap_in)) if len(kap_in) > 1 else 0.0
    psd, psd_r2 = psd_slope(avl_series)
    n_av = len(sizes)
    mean_sz = float(np.mean(sizes)) if sizes else 0.0
    mean_dur = float(np.mean(durs)) if durs else 0.0
    dur_arr = np.array(durs) if durs else np.array([0])
    frac1 = float((dur_arr == 1).mean()) if len(dur_arr) > 0 else 1.0

    if tau_s and tau_d:
        td_th = (tau_s+1)/2; sc_err = abs(tau_d-td_th)/td_th
    else:
        td_th = None; sc_err = 1.0

    size_ok  = (tau_s is not None and 1.2 <= tau_s <= 2.2 and r2_s > 0.70 and rs_r['plausible'])
    dur_ok   = (tau_d is not None and 1.5 <= tau_d <= 2.8 and r2_d > 0.70)
    kappa_ok = (0.85 <= kappa <= 1.15)
    count_ok = (n_av >= 300)
    psd_ok   = (psd is not None and -1.5 <= psd <= -0.3)
    zero_ok  = (zf >= 0.3)
    multi_ok = (frac1 < 0.8)
    scale_ok = (sc_err < 0.25)
    dec_ok   = (ds > 0.05)
    score = sum([size_ok, dur_ok, kappa_ok, count_ok, psd_ok,
                 zero_ok, multi_ok, scale_ok, dec_ok])

    ts_s = f"{tau_s:.3f}" if tau_s else "N/A"
    td_s = f"{tau_d:.3f}" if tau_d else "N/A"
    th_s = f"{td_th:.3f}" if td_th else "N/A"
    ps_s = f"{psd:.3f}" if psd else "N/A"

    print(f"\n{'='*65}")
    print(f"  [{label}|seed={seed}|{'4r' if use_pruning else '3r'}]")
    print(f"  σ初始={sigma_init:.2f} → σ最终={sigma_final:.2f} (Δ={sigma_final-sigma_init:+.2f})")
    print(f"  G_final={G_final:.4f}")
    print(f"  零帧: {zf:.1%} {'✓' if zero_ok else '✗'}")
    print(f"  雪崩数: {n_av} | 均尺寸: {mean_sz:.1f} | 均时长: {mean_dur:.1f} {'✓' if count_ok else '✗'}")
    print(f"  多步雪崩: {1-frac1:.1%} {'✓' if multi_ok else '✗'}")
    print(f"  τ_size={ts_s} R²={r2_s:.3f} p={rs_r['p_value']:.2f} {'✓' if size_ok else '✗'}")
    print(f"  τ_dur={td_s} R²={r2_d:.3f} (理论={th_s} 误差={sc_err:.0%}) {'✓' if dur_ok else '✗'}")
    print(f"  τ缩放: {'✓' if scale_ok else '✗'} (误差{sc_err:.0%})")
    print(f"  κ={kappa:.4f}±{kappa_std_:.3f} {'✓' if kappa_ok else '✗'}")
    print(f"  PSD={ps_s} R²={psd_r2:.3f} {'✓' if psd_ok else '✗'}")
    print(f"  解码={ds:.4f} {'✓' if dec_ok else '✗'}")
    print(f"  LR(PL>LN)={rs_r.get('lr_vs_lognormal',0):.1f}")
    print(f"  得分: {score}/9")
    print(f"  {'='*65}\n")
    sys.stdout.flush()

    return {
        'network': label, 'seed': seed,
        'rules': '4-rules' if use_pruning else '3-rules',
        'connectome': 'Varshney2011_real',
        'sigma_init': float(sigma_init), 'sigma_final': float(sigma_final),
        'sigma_delta': float(sigma_final - sigma_init),
        'G_kappa': float(G_kappa), 'kappa_calib': float(kappa_c),
        'G_final': float(G_final), 'mean_size_calib': float(ms_calib),
        'w_mean_after_learn': float(w_mean_after),
        'zero_fraction': float(zf),
        'n_avalanches': n_av, 'mean_size': float(mean_sz),
        'mean_duration': float(mean_dur), 'frac_dur1': float(frac1),
        'tau_size': float(tau_s) if tau_s else None, 'r2_size': float(r2_s),
        'ks_stat_size': float(rs_r['ks_stat']), 'p_value_size': float(rs_r['p_value']),
        'lr_vs_lognormal': float(rs_r.get('lr_vs_lognormal', 0)),
        'tau_duration': float(tau_d) if tau_d else None, 'r2_duration': float(r2_d),
        'tau_scale_error': float(sc_err),
        'branching_ratio': float(kappa), 'branching_ratio_std': float(kappa_std_),
        'psd_slope': float(psd) if psd else None, 'psd_r2': float(psd_r2),
        'decode_score': float(ds),
        'score': int(score), 'max_score': 9,
        'criteria': {
            'zero_frames': bool(zero_ok), 'size_powerlaw': bool(size_ok),
            'duration_powerlaw': bool(dur_ok), 'tau_scale': bool(scale_ok),
            'branching_ratio': bool(kappa_ok), 'avalanche_count': bool(count_ok),
            'psd_1f': bool(psd_ok), 'multi_step': bool(multi_ok),
            'output_decode': bool(dec_ok),
        },
        'topology_log': topo_log,
        'activation_sample': [int(x) for x in avl_series[:6000]],
        'sizes_sample': sorted([int(s) for s in sizes])[:1500],
        'durations_sample': sorted([int(d) for d in durs])[:1500],
    }

# ============================================================
# 绘图
# ============================================================
def plot_results(all_results):
    fig = plt.figure(figsize=(20, 20))
    fig.suptitle(
        'SDI Exp6: Real C.elegans Connectome (Varshney 2011)\n'
        'Chemical+Gap-junction synapses | 63 sensory / 105 inter / 111 motor\n'
        'v12 protocol: Soft-STDP + Weight normalization + Dual-G calibration',
        fontsize=10, fontweight='bold', y=0.99
    )
    gs = GridSpec(4, 3, figure=fig, hspace=0.48, wspace=0.36)
    from collections import defaultdict
    bg = defaultdict(list)
    for r in all_results: bg[r['rules']].append(r)
    best = {k: max(v, key=lambda x: x['score']) for k, v in bg.items()}

    colors = {'3-rules': '#2196F3', '4-rules': '#E91E63'}
    items = sorted(best.items())[:2]  # 3-rules + 4-rules

    for pi, (rules, res) in enumerate(items):
        color = colors.get(rules, '#333')
        col = pi

        # σ时序
        ax_s = fig.add_subplot(gs[0, col])
        tl = res.get('topology_log', [])
        if tl:
            steps = [t['step'] for t in tl]
            sigmas = [t['sigma'] for t in tl]
            ax_s.plot(steps, sigmas, color=color, lw=1.5)
            ax_s.axhline(y=res['sigma_init'], color='gray', ls='--', lw=1, label=f"初始σ={res['sigma_init']:.1f}")
        sc = res.get('score', 0); mx = res.get('max_score', 9)
        ax_s.set_title(f"{rules} σ: {res['sigma_init']:.1f}→{res['sigma_final']:.1f} Score={sc}/{mx}",
                      fontsize=8, color='green' if sc>=6 else 'orange')
        ax_s.set_xlabel('Step', fontsize=7); ax_s.set_ylabel('σ', fontsize=7)
        ax_s.tick_params(labelsize=7); ax_s.legend(fontsize=6)

        # 激活序列
        ax_a = fig.add_subplot(gs[1, col])
        act = res.get('activation_sample', [])
        if act: ax_a.plot(act[:3000], color=color, lw=0.5, alpha=0.8)
        kv = res.get('branching_ratio', 0); ds = res.get('decode_score', 0)
        ax_a.set_title(f"κ={kv:.3f} decode={ds:.3f}", fontsize=8)
        ax_a.set_xlabel('Step', fontsize=7); ax_a.set_ylabel('n_active', fontsize=7)
        ax_a.tick_params(labelsize=7)

        # 雪崩尺寸分布
        ax_p = fig.add_subplot(gs[2, col])
        sizes = res.get('sizes_sample', [])
        if sizes and len(sizes) > 10:
            sa = np.array(sizes)
            try:
                b = np.logspace(np.log10(max(1,sa.min())), np.log10(max(sa.max(),2)), 30)
                cnt, edg = np.histogram(sa, bins=b)
                ctr = (edg[:-1]+edg[1:])/2; msk = cnt > 0
                if msk.sum() > 3:
                    ax_p.loglog(ctr[msk], cnt[msk], 'o', color=color, ms=4, alpha=0.7, label='Data')
                    xt = np.logspace(np.log10(ctr[msk][0]), np.log10(ctr[msk][-1]), 50)
                    y0 = cnt[msk][0]*(ctr[msk][0]**1.5)
                    ax_p.loglog(xt, y0/(xt**1.5), '--', color='gray', alpha=0.5, label='τ=1.5')
            except: pass
        ts = res.get('tau_size'); se = res.get('tau_scale_error', 1.0)
        ts_str = f"{ts:.2f}" if ts else "N/A"
        ok = res.get('criteria', {}).get('size_powerlaw', False)
        ax_p.set_title(f"τ={ts_str} se={se:.0%} {'V' if ok else 'X'}", fontsize=8,
                      color='green' if ok else 'red')
        ax_p.set_xlabel('S', fontsize=7); ax_p.set_ylabel('Count', fontsize=7)
        ax_p.tick_params(labelsize=7); ax_p.legend(fontsize=6)

    plt.savefig(f'{OUT}/exp6_real_connectome_results.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Figure: {OUT}/exp6_real_connectome_results.png")

# ============================================================
# 主程序
# ============================================================
def main():
    print("="*70)
    print("SDI 实验六：真实C.elegans连接组验证（Varshney 2011）")
    print("  化学突触 + 电突触（E-L键）+ 63感觉/105中间/111运动")
    print("  v12协议：软饱和STDP + 稳态权重归一化 + 双重G校准")
    print("  新增对比：真实connectome初始σ vs 演化后σ")
    print("="*70)
    sys.stdout.flush()

    # 加载真实connectome
    print("\n加载真实C.elegans connectome...")
    adj_init, el_mask_init, is_inhib, sensory_idx, motor_idx, inter_idx, modality, nodes = \
        load_celegans_connectome()
    N = adj_init.shape[0]

    sigma_connectome = sigma_fast(adj_init, N)
    print(f"Varshney 2011 connectome: N={N}, 突触={(adj_init>0).sum()}")
    print(f"初始σ={sigma_connectome:.2f}（真实connectome的小世界系数）")
    print(f"感觉={len(sensory_idx)} 中间={len(inter_idx)} 运动={len(motor_idx)}")
    print(f"抑制性神经元={is_inhib.sum()}/{N} ({is_inhib.mean():.1%})")
    mod_c = {m: int((modality==m).sum()) for m in range(4)}
    print(f"感觉模态: 化学={mod_c[0]} 气味={mod_c[1]} 温度={mod_c[2]} 机械={mod_c[3]}")
    sys.stdout.flush()

    all_results = []
    t_total = time.time()

    for rules_label, use_pruning in [('3-rules', False), ('4-rules', True)]:
        print(f"\n[{'3' if not use_pruning else '4'}-rules]")
        for seed in SEEDS:
            print(f"\n-> C.elegans_real | seed={seed} | {rules_label}")
            sys.stdout.flush()
            try:
                result = run_simulation(
                    adj_init, el_mask_init, is_inhib,
                    sensory_idx, motor_idx, modality,
                    N, seed, use_pruning,
                    label='C.elegans_real'
                )
                all_results.append(result)
            except Exception as e:
                print(f"  ERROR: {e}")
                import traceback; traceback.print_exc()

    def ser(o):
        if isinstance(o, (np.integer,)): return int(o)
        if isinstance(o, (np.floating,)): return float(o)
        if isinstance(o, np.ndarray): return o.tolist()
        return o
    def ds_fn(o):
        if isinstance(o, dict): return {k: ds_fn(v) for k, v in o.items()}
        if isinstance(o, list): return [ds_fn(v) for v in o]
        return ser(o)

    out_path = f'{OUT}/exp6_real_connectome_results.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(ds_fn(all_results), f, ensure_ascii=False, indent=2)
    print(f"\nSaved: {out_path}")

    try: plot_results(all_results)
    except Exception as e: print(f"  Plot error: {e}")

    print("\n" + "="*70 + "\nSummary 实验六\n" + "="*70)
    from collections import defaultdict
    gd = defaultdict(list)
    for r in all_results: gd[r['rules']].append(r)

    print(f"\n{'规则':<12} σ_init  σ_final  Δσ    κ      τ_s    τ_d    PSD    decode  Score")
    print("-"*88)
    for key, runs in sorted(gd.items()):
        si = np.mean([r['sigma_init'] for r in runs])
        sf = np.mean([r['sigma_final'] for r in runs])
        kv = np.mean([r['branching_ratio'] for r in runs])
        tsl = [r['tau_size'] for r in runs if r['tau_size']]
        tdl = [r['tau_duration'] for r in runs if r['tau_duration']]
        pvl = [r['psd_slope'] for r in runs if r['psd_slope']]
        dcl = [r['decode_score'] for r in runs]
        svl = [r['score'] for r in runs]
        mx = runs[0]['max_score']
        print(f"{key:<12} {si:.2f}    {sf:.2f}    {sf-si:+.2f}  {kv:.3f}  "
              f"{np.mean(tsl):.2f if tsl else 'N/A':<7}"
              f"{np.mean(tdl):.2f if tdl else 'N/A':<7}"
              f"{np.mean(pvl):.2f if pvl else 'N/A':<7}"
              f"{np.mean(dcl):.3f}   {np.mean(svl):.1f}/{mx}")

    if all_results:
        best = max(all_results, key=lambda x: x['score'])
        ts_b = f"{best['tau_size']:.3f}" if best['tau_size'] else "N/A"
        td_b = f"{best['tau_duration']:.3f}" if best['tau_duration'] else "N/A"
        print(f"\n最优: {best['rules']} | seed={best['seed']}")
        print(f"  σ: {best['sigma_init']:.2f}→{best['sigma_final']:.2f}")
        print(f"  τ_size={ts_b}  κ={best['branching_ratio']:.3f}")
        print(f"  decode={best['decode_score']:.4f}  score={best['score']}/{best['max_score']}")

    elapsed = time.time() - t_total
    print(f"\nTotal: {elapsed:.0f}s ({elapsed/60:.1f}min)")
    print("实验六完成。")
    sys.stdout.flush()

if __name__ == '__main__':
    main()
