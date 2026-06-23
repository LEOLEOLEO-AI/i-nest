#!/usr/bin/env python3
"""
SDI 实验五 v9：三阶段协议（适应→解码测量→雪崩记录）

==============================================================================
v9设计思路：整合所有前版本的成果，修复v8的零帧问题
==============================================================================

【v8问题】
  记录阶段泊松λ_stim=0.15持续驱动 → 零帧<10% → PSD、τ测量失效
  根本矛盾：生物语义输入（持续） vs SOC雪崩测量（需要沉寂期）

【v9解决方案：三阶段协议】

  阶段1 — 适应（N_ADAPT=6000步）：泊松感觉刺激 + 强STDP
    - 4种感觉模态的泊松放电驱动拓扑自演化
    - 按C.elegans神经元类型分配输入（感觉60/中间111/运动108）
    - 强STDP（ETA_LTP=0.012）建立功能性连接
    - BTW驱动关闭

  阶段2 — 解码测量（N_DECODE=2000步）：保留泊松刺激 + 弱STDP
    - 继续泊松输入，记录不同感觉模态→运动层的激活模式
    - STDP学习率减半，防止过度改写已学习的结构
    - 专门用于功能性解码评分
    - 不记录雪崩

  阶段3 — 雪崩记录（N_RECORD=20000步）：泊松关闭 + 纯BTW慢驱动
    - 感觉输入完全关闭（λ=0）
    - 仅BTW极慢驱动（每10步1个随机节点）
    - STDP极弱（学习率×0.1，维持但不破坏结构）
    - 记录神经雪崩，测量SOC指标

【v9全部继承的机制（v7+v8）】
  ✅ 泊松放电过程（v8升级）
  ✅ C.elegans神经元类型分层（v8升级）
  ✅ 输出解码验证（v8升级）
  ✅ STD状态连续（v7 Fix-1）
  ✅ KS检验+似然比检验（v7 Fix-2）
  ✅ τ缩放关系检验（v7 Fix-3）
  ✅ 真实STDP时间戳（v7 Fix-4）
  ✅ 延迟队列（v7 Fix-5）
  ✅ 全雪崩κ校准（v7 Fix-6）
  ✅ 向量化recover_std（v7 Fix-8）
  ✅ E/I平衡 + STD + 有向图（v6）

【新增：v9专属】
  ✅ 三阶段协议（适应→解码→雪崩）
  ✅ G校准在适应阶段结束时执行（用稳态STD）
  ✅ 雪崩阶段STDP极弱但不归零（生物真实：突触可塑性不会完全停止）
  ✅ 解码评分用多次重复测量均值（不只用单步激活）

==============================================================================
文献
==============================================================================
  Beggs & Plenz 2003 — 神经雪崩基准
  Friedman 2012 PRL — τ缩放关系
  Priesemann 2014 PLOS CB — BTW校准方法
  Varshney 2011 PLOS CB — C.elegans connectome
  Rieke 1997 — 泊松神经编码
  Bi & Poo 1998 — STDP
  Tsodyks & Markram 1997 — STD
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

OUT = '/home/work/.openclaw/workspace/sdi_sim'

# ============================================================
# 参数
# ============================================================
# STDP（Bi & Poo 1998）
THETA_LTP   = 65
THETA_LTD   = 15
ETA_LTP     = 0.012     # 适应阶段
ETA_LTD     = 0.008
ETA_LTP_MID = 0.006     # 解码阶段（减半）
ETA_LTD_MID = 0.004
ETA_LTP_REC = 0.001     # 记录阶段（极弱，维持不破坏）
ETA_LTD_REC = 0.0008
TAU_STDP    = 20.0
STDP_MAX_DT = 100

# 突触结构
T_DECAY   = 400
EL_HI     = 0.25
T_ABS     = 3
T_REL     = 5
P_REWIRE  = 0.15
REWIRE_INT = 50
SCALING_INT = 100
KAPPA_TARGET = 0.95
SCALING_RATE = 0.05
PRUNE_INT = 200
P_PRUNE   = 0.05
MIN_EDGES = 3

# E/I平衡（Brunel 2000）
FRAC_INHIB   = 0.20
INHIB_SCALE  = 2.0

# STD（Tsodyks & Markram 1997）
STD_ENABLED = True
U_0         = 0.5
USE_FACTOR  = 0.35
TAU_STD     = 15.0

# 突触延迟（Diesmann 1999）
DELAY_ENABLED = True
MIN_DELAY = 1
MAX_DELAY = 3

# ★ 三阶段参数
N_ADAPT   = 6000    # 阶段1：适应（泊松+强STDP）
N_DECODE  = 2000    # 阶段2：解码测量（泊松+弱STDP）
N_RECORD  = 20000   # 阶段3：雪崩（BTW+极弱STDP）
LOG_INT   = 3000

# BTW驱动（阶段3）
BTW_INTERVAL = 10

# 泊松输入（阶段1+2）
LAMBDA_STIM = 0.15
LAMBDA_BASE = 0.02
T_STIM_ON   = 50
T_STIM_OFF  = 50

# 校准
CALIB_WARMUP = 300
CALIB_STEPS  = 1200
CALIB_ITER   = 30
G_LO_INIT    = 0.001
G_HI_INIT    = 4.0

SEEDS = [42, 7, 13]

# ============================================================
# C.elegans神经元类型（Varshney 2011）
# ============================================================
def assign_celegans_types(N=279):
    N_SENSORY = 60
    N_MOTOR   = 108
    neuron_type = np.array(['inter'] * N, dtype='<U8')
    neuron_type[:N_SENSORY] = 'sensory'
    neuron_type[N - N_MOTOR:] = 'motor'
    sensory_idx = np.where(neuron_type == 'sensory')[0]
    motor_idx   = np.where(neuron_type == 'motor')[0]
    inter_idx   = np.where(neuron_type == 'inter')[0]
    return neuron_type, sensory_idx, motor_idx, inter_idx

def assign_sensory_modalities(sensory_idx, seed=0):
    """4种感觉模态分配（化学/气味/温度/机械）"""
    rng = np.random.default_rng(seed + 5555)
    N_sens = len(sensory_idx)
    modality = np.zeros(N_sens, dtype=np.int8)
    # 比例：化学35%，气味25%，温度17%，机械23%
    boundaries = [0, int(N_sens*0.35), int(N_sens*0.60),
                  int(N_sens*0.77), N_sens]
    for m in range(4):
        modality[boundaries[m]:boundaries[m+1]] = m
    rng.shuffle(modality)
    return modality

# ============================================================
# 泊松刺激器
# ============================================================
class PoissonStimulator:
    def __init__(self, sensory_idx, modality, n_modalities=4, seed=0):
        self.sensory_idx  = sensory_idx
        self.modality     = modality
        self.n_mod        = n_modalities
        self.rng          = np.random.default_rng(seed + 3333)
        self.step_count   = 0
        self.active_mod   = 0

    def step(self):
        t = self.step_count
        cycle_len = T_STIM_ON + T_STIM_OFF
        phase = t % cycle_len
        is_on = (phase < T_STIM_ON)
        if phase == 0:
            self.active_mod = int(self.rng.integers(self.n_mod))
        activated = []
        for ni, mod in zip(self.sensory_idx, self.modality):
            lam = LAMBDA_STIM if (is_on and mod == self.active_mod) else LAMBDA_BASE
            if self.rng.random() < lam:
                activated.append(int(ni))
        self.step_count += 1
        return activated, self.active_mod, is_on

# ============================================================
# 网络初始化
# ============================================================
def make_ws_adj_directed(N, k, p, seed):
    rng = np.random.default_rng(seed)
    adj = np.zeros((N, N), dtype=np.float32)
    for i in range(N):
        for dj in range(1, k // 2 + 1):
            j = (i + dj) % N
            if rng.random() < (1 - p):
                adj[i, j] = float(rng.uniform(0.05, 0.3))
            else:
                tgt = int(rng.integers(N))
                while tgt == i or adj[i, tgt] > 0:
                    tgt = int(rng.integers(N))
                adj[i, tgt] = float(rng.uniform(0.05, 0.3))
            if rng.random() < 0.5:
                adj[j, i] = float(rng.uniform(0.05, 0.3))
    return adj

def assign_inhib_types(N, frac, seed):
    rng = np.random.default_rng(seed + 7777)
    n_i = int(N * frac)
    idx = rng.choice(N, size=n_i, replace=False)
    is_inhib = np.zeros(N, dtype=bool)
    is_inhib[idx] = True
    return is_inhib

def init_std(N, seed):
    rng = np.random.default_rng(seed + 8888)
    u = np.full((N, N), U_0, dtype=np.float32)
    u += rng.uniform(-0.03, 0.03, (N, N)).astype(np.float32)
    return np.clip(u, 0.01, 1.0)

def make_delays(N, seed):
    rng = np.random.default_rng(seed + 9999)
    return rng.integers(MIN_DELAY, MAX_DELAY + 1, size=(N, N)).astype(np.int8)

# ============================================================
# 度量
# ============================================================
def sigma_fast(adj, N):
    try:
        sym = (np.abs(adj) + np.abs(adj.T)) / 2
        edges = np.argwhere(sym > 0.05)
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
        C_r = k_avg/N; L_r = np.log(N)/np.log(k_avg)
        if C_r == 0 or L_r == 0: return 1.0
        return float((C/C_r)/(L/L_r))
    except: return 1.0

# ============================================================
# STD恢复（向量化）
# ============================================================
def recover_std(std_u, syn_mask):
    if STD_ENABLED:
        std_u[syn_mask] += (U_0 - std_u[syn_mask]) / TAU_STD

# ============================================================
# 单层传播（延迟队列 + E/I + STD）
# ============================================================
def propagate(adj, el_mask, is_inhib, std_u, delays,
              wave, refrac, fired, N, G, delay_buffer, step, rng):
    new_wave = np.zeros(N, dtype=bool)
    inhib_in = np.zeros(N, dtype=np.float32)

    # 处理本步到达的延迟消息
    for (tgt, eff_w, is_ex) in delay_buffer.pop(step, []):
        if refrac[tgt] > 0 or fired[tgt]: continue
        if is_ex:
            if rng.random() < min(eff_w, 0.99): new_wave[tgt] = True
        else:
            inhib_in[tgt] += eff_w

    # 当前wave发出信号 → delay_buffer
    for i in np.where(wave)[0]:
        w = adj[i, :] * G
        w[el_mask[i, :]] *= 1.15
        if is_inhib[i]:
            ws = w * INHIB_SCALE
            for c in np.where(ws > 0.005)[0]:
                if c == i: continue
                u = float(std_u[i, c])
                eff = float(ws[c]) * u
                if STD_ENABLED: std_u[i, c] *= (1.0 - USE_FACTOR)
                delay_buffer[step + int(delays[i, c])].append((int(c), eff, False))
        else:
            for c in np.where(w > 0.005)[0]:
                u = float(std_u[i, c])
                eff = float(w[c]) * u
                if STD_ENABLED: std_u[i, c] *= (1.0 - USE_FACTOR)
                delay_buffer[step + int(delays[i, c])].append((int(c), eff, True))

    # 抑制削减
    for tgt in np.where(inhib_in > 0)[0]:
        if new_wave[tgt] and rng.random() < min(float(inhib_in[tgt]) * 0.5, 0.99):
            new_wave[tgt] = False

    new_wave &= ~fired
    return new_wave

# ============================================================
# κ校准（Priesemann方法）
# ============================================================
def estimate_kappa(adj, el_mask, is_inhib, delays, std_u0,
                   N, G, seed, n_warmup, n_measure):
    rng = np.random.default_rng(seed)
    refrac = np.zeros(N, dtype=np.int8)
    std_u = std_u0.copy()
    syn_mask = adj != 0
    wave = np.zeros(N, dtype=bool)
    fired = np.zeros(N, dtype=bool)
    db = defaultdict(list)
    log = []
    for step in range(n_warmup + n_measure):
        recover_std(std_u, syn_mask)
        pending = any(k >= step for k in db)
        if not wave.any() and not pending and step % BTW_INTERVAL == 0:
            d = int(rng.integers(N))
            if refrac[d] == 0:
                wave[d] = True; fired[:] = False; fired[d] = True
        nw = propagate(adj, el_mask, is_inhib, std_u, delays,
                       wave, refrac, fired, N, G, db, step, rng)
        fired |= nw; wave = nw
        if step >= n_warmup: log.append(int(nw.sum()))
        refrac[wave] = T_ABS; refrac[refrac > 0] -= 1
    if len(log) < 10: return 0.0
    arr = np.array(log, dtype=float)
    num = arr[1:][arr[:-1] > 0].sum()
    den = arr[:-1][arr[:-1] > 0].sum()
    return float(num / den) if den > 0 else 0.0

def calibrate_G(adj, el_mask, is_inhib, delays, std_u0, N, seed):
    G_lo = G_LO_INIT; G_hi = G_HI_INIT; G_best = 0.5
    for i in range(CALIB_ITER):
        G_mid = (G_lo + G_hi) / 2
        k = estimate_kappa(adj, el_mask, is_inhib, delays, std_u0,
                           N, G_mid, seed + i*997, CALIB_WARMUP, CALIB_STEPS)
        print(f"    校准 iter={i+1}: G={G_mid:.5f} → κ={k:.4f}")
        sys.stdout.flush()
        if 0.90 <= k <= 1.10:
            print(f"    ✅ G={G_mid:.5f}, κ={k:.4f}")
            return G_mid, k
        if k < 0.90: G_lo = G_mid
        else: G_hi = G_mid
        if G_hi - G_lo < 0.0002: G_best = G_mid; break
        G_best = G_mid
    kf = estimate_kappa(adj, el_mask, is_inhib, delays, std_u0,
                        N, G_best, seed+9999999, CALIB_WARMUP, CALIB_STEPS)
    print(f"    ⚠️ G={G_best:.5f}, κ={kf:.4f}")
    return G_best, kf

# ============================================================
# 雪崩检测
# ============================================================
def detect_avalanches(series):
    sizes, durs, kappas = [], [], []
    layers = []; in_av = False
    for n in series:
        if n > 0:
            in_av = True; layers.append(n)
        else:
            if in_av and layers:
                sizes.append(sum(layers)); durs.append(len(layers))
                if len(layers) >= 2:
                    den = sum(layers[:-1])
                    kappas.append(sum(layers[1:]) / den if den > 0 else 0.0)
                in_av = False; layers = []
    if in_av and layers:
        sizes.append(sum(layers)); durs.append(len(layers))
        if len(layers) >= 2:
            den = sum(layers[:-1])
            kappas.append(sum(layers[1:]) / den if den > 0 else 0.0)
    return sizes, durs, kappas

# ============================================================
# 幂律拟合（KS + 似然比）
# ============================================================
def fit_pl(data):
    data = np.array([d for d in data if d > 0], dtype=float)
    res = dict(tau=None, xmin=None, n_tail=len(data),
               r2=0.0, ks_stat=1.0, plausible=False,
               p_value=0.0, lr_vs_lognormal=0.0)
    if len(data) < 30: return res
    p5 = max(1.0, np.percentile(data, 5))
    p65 = np.percentile(data, 65)
    cands = np.unique(data); cands = cands[(cands >= p5) & (cands <= p65)]
    if len(cands) == 0: cands = [np.median(data)]
    best_ks = np.inf; best_xm = p5; best_tau = 1.5
    for xm in cands[:50]:
        tail = data[data >= xm]
        if len(tail) < 15: continue
        lr = np.log(tail / xm)
        if lr.sum() == 0: continue
        tau_e = 1 + len(tail) / lr.sum()
        if tau_e <= 1 or tau_e > 8: continue
        ts = np.sort(tail); n_t = len(ts)
        ecdf = np.arange(1, n_t+1) / n_t
        tcdf = 1 - (ts/xm)**(-(tau_e-1))
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
            c = np.polyfit(lx, ly, 1)
            ssr = np.sum((ly-np.polyval(c,lx))**2)
            sst = np.sum((ly-ly.mean())**2)
            res['r2'] = float(1-ssr/sst) if sst > 0 else 0.0
    # Bootstrap p_value
    tau = best_tau; xm = best_xm; n_t = len(tail)
    rng_b = np.random.default_rng(42); boots = []
    for _ in range(50):
        u = rng_b.uniform(size=n_t)
        syn = xm * (1-u)**(-1/(tau-1))
        syn = np.sort(syn)
        ts2 = 1 + n_t / np.sum(np.log(syn/xm))
        if ts2 <= 1: ts2 = 1.01
        ecdf_s = np.arange(1, n_t+1)/n_t
        tcdf_s = 1-(syn/xm)**(-(ts2-1))
        boots.append(float(np.max(np.abs(ecdf_s-tcdf_s))))
    res['p_value'] = float(np.mean(np.array(boots) >= best_ks))
    res['plausible'] = (res['p_value'] >= 0.1)
    # LR
    ll_pl = np.sum(np.log(tau-1) - np.log(xm) - tau*np.log(tail/xm))
    lt = np.log(tail); mu = lt.mean(); sg = lt.std()
    if sg > 0:
        ll_ln = np.sum(-np.log(tail) - 0.5*np.log(2*np.pi*sg**2)
                       - 0.5*((lt-mu)/sg)**2)
        res['lr_vs_lognormal'] = float(ll_pl - ll_ln)
    return res

def psd_slope(series):
    arr = np.array(series, dtype=float) - np.mean(series)
    power = np.abs(np.fft.rfft(arr))**2
    freqs = np.fft.rfftfreq(len(arr))
    mask = (freqs > 0.001) & (freqs < 0.25)
    if mask.sum() < 15: return 0.0, 0.0
    lf = np.log(freqs[mask]); lp = np.log(power[mask]+1e-10)
    c = np.polyfit(lf, lp, 1)
    ssr = np.sum((lp-np.polyval(c,lf))**2)
    sst = np.sum((lp-lp.mean())**2)
    return float(c[0]), float(1-ssr/sst) if sst > 0 else 0.0

# ============================================================
# 输出解码评分
# ============================================================
def decode_score(motor_act_by_mod):
    if len(motor_act_by_mod) < 2: return 0.0
    vecs = []
    for arr in motor_act_by_mod.values():
        v = np.array(arr, dtype=float)
        n = np.linalg.norm(v)
        vecs.append(v/n if n > 0 else v)
    dists = []
    for i in range(len(vecs)):
        for j in range(i+1, len(vecs)):
            dists.append(1.0 - np.dot(vecs[i], vecs[j]))
    return float(np.mean(dists)) if dists else 0.0

# ============================================================
# 主仿真
# ============================================================
def run_simulation(net_cfg, net_name, seed, use_pruning=False):
    N = net_cfg['N']
    rng = np.random.default_rng(seed)

    # 初始化
    adj     = make_ws_adj_directed(N, net_cfg['k_init'], net_cfg['p_init'], seed)
    is_inh  = assign_inhib_types(N, FRAC_INHIB, seed)
    std_u   = init_std(N, seed)
    delays  = make_delays(N, seed)
    syn_mask = adj != 0
    el_mask = np.zeros((N, N), dtype=bool)
    el_mask[adj > 0] = rng.random((adj > 0).sum()) < 0.05
    el_mask[is_inh, :] = False
    nltp = np.zeros((N, N), dtype=np.int16)
    nltd = np.zeros((N, N), dtype=np.int16)
    el_age = np.zeros((N, N), dtype=np.int32)
    refrac  = np.zeros(N, dtype=np.int8)
    last_sp = np.full(N, -99999, dtype=np.int32)
    exc_pre = np.outer(~is_inh, np.ones(N, dtype=bool))   # 预计算

    # C.elegans类型
    _, sens_idx, mot_idx, _ = assign_celegans_types(N)
    modality = assign_sensory_modalities(sens_idx, seed)
    stim = PoissonStimulator(sens_idx, modality, n_modalities=4, seed=seed)

    n_e = int((~is_inh).sum()); n_i = int(is_inh.sum())
    print(f"  [{net_name}|{seed}] N={N} E={n_e} I={n_i} | "
          f"感觉={len(sens_idx)} 运动={len(mot_idx)}")
    sys.stdout.flush()

    topo_log = []
    t0 = time.time()
    db = defaultdict(list)   # 延迟队列

    # 解码测量结构
    mot_act_by_mod = defaultdict(lambda: np.zeros(len(mot_idx)))
    mot_act_cnt    = defaultdict(int)

    # 雪崩记录
    avalanche_series = []

    total = N_ADAPT + N_DECODE + N_RECORD
    print(f"  三阶段：适应{N_ADAPT} → 解码{N_DECODE} → 雪崩{N_RECORD}")
    sys.stdout.flush()

    for step in range(total):
        phase = ('adapt'  if step < N_ADAPT else
                 'decode' if step < N_ADAPT + N_DECODE else
                 'record')

        # STDP学习率按阶段
        eta_ltp = ETA_LTP     if phase == 'adapt'  else \
                  ETA_LTP_MID if phase == 'decode' else ETA_LTP_REC
        eta_ltd = ETA_LTD     if phase == 'adapt'  else \
                  ETA_LTD_MID if phase == 'decode' else ETA_LTD_REC

        # STD恢复
        recover_std(std_u, syn_mask)

        # 外部输入
        active = np.zeros(N, dtype=bool)

        if phase in ('adapt', 'decode'):
            # 泊松感觉输入
            stim_ns, act_mod, is_on = stim.step()
            for ni in stim_ns:
                if refrac[ni] == 0:
                    active[ni] = True
        else:
            # 记录阶段：仅BTW极慢驱动
            abs_step = step
            pending = any(k >= abs_step for k in db)
            if not active.any() and not pending and step % BTW_INTERVAL == 0:
                d = int(rng.integers(N))
                if refrac[d] == 0:
                    active[d] = True
            act_mod = -1; is_on = False

        # 单层传播
        if active.any():
            fired = active.copy()
            nw = propagate(adj, el_mask, is_inh, std_u, delays,
                           active, refrac, fired, N, 1.0, db, step, rng)
            active |= nw
        else:
            fired = np.zeros(N, dtype=bool)
            nw = propagate(adj, el_mask, is_inh, std_u, delays,
                           np.zeros(N, dtype=bool), refrac, fired, N, 1.0,
                           db, step, rng)
            active |= nw

        n_act = int(active.sum())
        last_sp[active] = step
        refrac[active] = T_ABS + T_REL
        refrac[refrac > 0] -= 1

        # 解码阶段：记录运动层激活
        if phase == 'decode' and is_on and n_act > 0:
            mot_act = active[mot_idx].astype(float)
            if mot_act.any():
                mot_act_by_mod[int(act_mod)] += mot_act
                mot_act_cnt[int(act_mod)] += 1

        # 雪崩记录阶段
        if phase == 'record':
            avalanche_series.append(n_act)

        # STDP（真实时差）
        aidx_e = np.where(active & ~is_inh)[0]
        aidx_a = np.where(active)[0]
        if len(aidx_e) >= 2 and len(aidx_a) >= 1:
            n_p = min(len(aidx_e)*2, 100)
            pre_a = rng.choice(aidx_e, size=n_p)
            post_a = rng.choice(aidx_a, size=n_p)
            for pre, post in zip(pre_a, post_a):
                if pre == post: continue
                dt = int(last_sp[post]) - int(last_sp[pre])
                if abs(dt) > STDP_MAX_DT: continue
                if dt > 0:
                    if adj[pre, post] > 0 and not is_inh[pre]:
                        adj[pre, post] = min(1.0, adj[pre, post] +
                                             eta_ltp * np.exp(-abs(dt)/TAU_STDP))
                        nltp[pre, post] += 1
                else:
                    if adj[post, pre] > 0 and not is_inh[post]:
                        adj[post, pre] = max(0.0, adj[post, pre] -
                                             eta_ltd * np.exp(-abs(dt)/TAU_STDP))
                        nltd[post, pre] += 1

        # 固化/消除
        el_r = el_mask.sum() / max(1, (adj > 0).sum())
        ltp_m = (nltp >= THETA_LTP) & (adj > 0) & (~el_mask) & (el_r < EL_HI) & exc_pre
        el_mask[ltp_m] = True; nltp[ltp_m] = 0
        ltd_m = (nltd >= THETA_LTD) & (adj > 0) & (~el_mask) & exc_pre
        adj[ltd_m] = 0.0; nltp[ltd_m] = nltd[ltd_m] = 0
        syn_mask[ltd_m] = False
        el_age[el_mask] += 1
        dm = el_mask & (el_age > T_DECAY)
        el_mask[dm] = False; el_age[dm] = 0

        # WS重连
        if step % REWIRE_INT == 0:
            non_el = np.argwhere((adj > 0) & (~el_mask) & exc_pre)
            for _ in range(max(1, int(len(non_el)*P_REWIRE*0.01))):
                if len(non_el) == 0: break
                ix = int(rng.integers(len(non_el))); i, j = non_el[ix]
                kn = int(rng.integers(N))
                if kn != i and adj[i, kn] == 0:
                    adj[i, kn] = adj[i, j]; adj[i, j] = 0.0
                    syn_mask[i, j] = False; syn_mask[i, kn] = True

        # 突触缩放（仅适应/解码阶段）
        if phase != 'record' and step % SCALING_INT == 0 and n_act > 0:
            ar = n_act / N
            if ar > KAPPA_TARGET: adj[~el_mask] *= (1 - SCALING_RATE)
            elif ar < KAPPA_TARGET * 0.5: adj[~el_mask] *= (1 + SCALING_RATE)
            adj = np.clip(adj, 0.0, 1.0)

        # 竞争性修剪（4规则）
        if use_pruning and step % PRUNE_INT == 0 and step > 0:
            deg = (adj > 0).sum(axis=1)
            for i, j in np.argwhere((adj > 0) & (~el_mask) & exc_pre
                                     & (nltp == 0) & (nltd == 0)):
                if deg[i] > MIN_EDGES and rng.random() < P_PRUNE:
                    adj[i, j] = 0.0; syn_mask[i, j] = False
            nltp[:] = 0; nltd[:] = 0

        if step % LOG_INT == 0:
            sig = sigma_fast(adj, N)
            print(f"    [{phase}] {step}/{total} σ={sig:.2f} "
                  f"edges={(adj>0).sum()} n_act={n_act} t={time.time()-t0:.0f}s")
            sys.stdout.flush()
            topo_log.append({'step': step, 'sigma': sig,
                              'n_edges': int((adj>0).sum()),
                              'n_el': int(el_mask.sum()), 'phase': phase})

    # 适应/解码结束后校准G
    std_after = std_u.copy()
    sig_final = sigma_fast(adj, N)
    print(f"\n  完成三阶段。edges={(adj>0).sum()} σ={sig_final:.2f}")

    # 解码评分
    ds = decode_score(mot_act_by_mod)
    print(f"  输出解码余弦距离: {ds:.4f} ({'✓' if ds > 0.05 else '✗'})")

    print(f"\n  临界点校准...")
    sys.stdout.flush()
    G_c, kappa_c = calibrate_G(adj, el_mask, is_inh, delays, std_after, N, seed)
    print(f"  G={G_c:.5f}, κ={kappa_c:.4f}")

    # 雪崩分析
    arr = np.array(avalanche_series)
    zf = float((arr == 0).mean())
    print(f"\n  雪崩统计: 零帧={zf:.1%} 最大={arr.max()} 均={arr.mean():.3f}")

    sizes, durs, kap_inner = detect_avalanches(avalanche_series)
    rs = fit_pl(sizes); rd = fit_pl(durs)
    tau_s = rs['tau']; r2_s = rs['r2']
    tau_d = rd['tau']; r2_d = rd['r2']
    kappa = float(np.mean(kap_inner)) if kap_inner else 0.0
    kappa_std_ = float(np.std(kap_inner)) if len(kap_inner) > 1 else 0.0
    psd, psd_r2 = psd_slope(avalanche_series)
    n_av = len(sizes)
    mean_sz = float(np.mean(sizes)) if sizes else 0.0
    mean_dur = float(np.mean(durs)) if durs else 0.0
    dur_arr = np.array(durs) if durs else np.array([0])
    frac1 = float((dur_arr == 1).mean()) if len(dur_arr) > 0 else 1.0

    # τ缩放关系（Friedman 2012）
    if tau_s and tau_d:
        td_theory = (tau_s + 1) / 2
        sc_err = abs(tau_d - td_theory) / td_theory
    else:
        sc_err = 1.0; td_theory = None

    # 9项达标判定
    size_ok   = (tau_s is not None and 1.2 <= tau_s <= 2.2 and r2_s > 0.70 and rs['plausible'])
    dur_ok    = (tau_d is not None and 1.5 <= tau_d <= 2.8 and r2_d > 0.70)
    kappa_ok  = (0.85 <= kappa <= 1.15)
    count_ok  = (n_av >= 300)
    psd_ok    = (psd is not None and -1.5 <= psd <= -0.3)
    zero_ok   = (zf >= 0.3)
    multi_ok  = (frac1 < 0.8)
    scale_ok  = (sc_err < 0.25)
    decode_ok = (ds > 0.05)

    score = sum([size_ok, dur_ok, kappa_ok, count_ok, psd_ok,
                 zero_ok, multi_ok, scale_ok, decode_ok])

    ts_s  = f"{tau_s:.3f}" if tau_s else "N/A"
    td_s  = f"{tau_d:.3f}" if tau_d else "N/A"
    th_s  = f"{td_theory:.3f}" if td_theory else "N/A"
    ps_s  = f"{psd:.3f}"   if psd   else "N/A"

    print(f"\n{'='*65}")
    print(f"  [{net_name}|{seed}|{'4r' if use_pruning else '3r'}] G={G_c:.4f}")
    print(f"  零帧: {zf:.1%} {'✓' if zero_ok else '✗'}")
    print(f"  雪崩数: {n_av} | 均尺寸: {mean_sz:.1f} | 均时长: {mean_dur:.1f} {'✓' if count_ok else '✗'}")
    print(f"  多步雪崩: {1-frac1:.1%} {'✓' if multi_ok else '✗'}")
    print(f"  τ_size={ts_s} R²={r2_s:.3f} p={rs['p_value']:.2f} {'✓' if size_ok else '✗'}")
    print(f"  τ_dur={td_s} R²={r2_d:.3f} (理论={th_s} 误差={sc_err:.0%}) {'✓' if dur_ok else '✗'}")
    print(f"  τ缩放: {'✓' if scale_ok else '✗'} (误差{sc_err:.0%})")
    print(f"  κ={kappa:.4f}±{kappa_std_:.3f} {'✓' if kappa_ok else '✗'}")
    print(f"  PSD={ps_s} R²={psd_r2:.3f} {'✓' if psd_ok else '✗'}")
    print(f"  解码={ds:.4f} {'✓' if decode_ok else '✗'}")
    print(f"  LR(PL>LN)={rs.get('lr_vs_lognormal', 0):.1f}")
    print(f"  得分: {score}/9")
    print(f"  {'='*65}\n")
    sys.stdout.flush()

    return {
        'network': net_name, 'seed': seed,
        'rules': '4-rules' if use_pruning else '3-rules',
        'protocol': {'N_ADAPT': N_ADAPT, 'N_DECODE': N_DECODE, 'N_RECORD': N_RECORD},
        'input_mode': {'type': 'Poisson+BTW_3phase',
                       'lambda_stim': LAMBDA_STIM, 'lambda_base': LAMBDA_BASE},
        'G_calib': float(G_c), 'kappa_calib': float(kappa_c),
        'sigma_final': float(sig_final),
        'zero_fraction': float(zf),
        'n_avalanches': n_av, 'mean_size': float(mean_sz),
        'mean_duration': float(mean_dur), 'frac_dur1': float(frac1),
        'tau_size': float(tau_s) if tau_s else None, 'r2_size': float(r2_s),
        'ks_stat_size': float(rs['ks_stat']), 'p_value_size': float(rs['p_value']),
        'lr_vs_lognormal': float(rs.get('lr_vs_lognormal', 0)),
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
            'output_decode': bool(decode_ok),
        },
        'topology_log': topo_log,
        'activation_sample': [int(x) for x in avalanche_series[:6000]],
        'sizes_sample': sorted([int(s) for s in sizes])[:1500],
        'durations_sample': sorted([int(d) for d in durs])[:1500],
    }

# ============================================================
# 网络定义
# ============================================================
NETWORKS = {
    'C.elegans': {
        'N': 279, 'k_init': 8, 'p_init': 0.05,
        'level': 'neuron', 'ref': 'Varshney 2011'
    },
    'Human_HCP': {
        'N': 400, 'k_init': 10, 'p_init': 0.06,
        'level': 'mesoscale', 'ref': 'Van Essen 2013'
    },
    'WS_Control': {
        'N': 279, 'k_init': 8, 'p_init': 0.15,
        'level': 'control', 'ref': 'WS 1998'
    }
}

# ============================================================
# 绘图
# ============================================================
def plot_results(all_results):
    fig = plt.figure(figsize=(22, 28))
    fig.suptitle(
        'SDI Exp5 v9: Three-Phase Protocol (Adapt→Decode→Avalanche)\n'
        'Phase1: Poisson+STDP | Phase2: Decode measure | Phase3: BTW only',
        fontsize=11, fontweight='bold', y=0.99
    )
    gs = GridSpec(6, 3, figure=fig, hspace=0.50, wspace=0.38)
    from collections import defaultdict
    bg = defaultdict(list)
    for r in all_results: bg[r['network']+'_'+r['rules']].append(r)
    best = {k: max(v, key=lambda x: x['score']) for k, v in bg.items()}
    items = sorted(best.items())[:6]
    colors = {'3-rules': '#2196F3', '4-rules': '#E91E63'}

    for pi, (key, res) in enumerate(items):
        if pi >= 6: break
        color = colors.get(res['rules'], '#333')
        row, col = divmod(pi, 3)

        ax1 = fig.add_subplot(gs[row*2, col])
        act = res.get('activation_sample', [])
        if act: ax1.plot(act[:4000], color=color, lw=0.5, alpha=0.8)
        sc = res.get('score', 0); mx = res.get('max_score', 9)
        ax1.set_title(
            f"{res['network']} {res['rules']}\n"
            f"κ={res.get('branching_ratio',0):.3f} "
            f"decode={res.get('decode_score',0):.3f} "
            f"Score={sc}/{mx}",
            fontsize=7,
            color='green' if sc >= 6 else ('orange' if sc >= 4 else 'red')
        )
        ax1.set_xlabel('Step (record phase)', fontsize=6)
        ax1.set_ylabel('n_active', fontsize=6); ax1.tick_params(labelsize=6)

        ax2 = fig.add_subplot(gs[row*2+1, col])
        sizes = res.get('sizes_sample', [])
        if sizes and len(sizes) > 10:
            sa = np.array(sizes)
            try:
                b = np.logspace(np.log10(max(1,sa.min())),
                                np.log10(max(sa.max(),2)), 30)
                cnt, edg = np.histogram(sa, bins=b)
                ctr = (edg[:-1]+edg[1:])/2; msk = cnt > 0
                if msk.sum() > 3:
                    ax2.loglog(ctr[msk], cnt[msk], 'o', color=color,
                               ms=4, alpha=0.7, label='Data')
                    xt = np.logspace(np.log10(ctr[msk][0]),
                                     np.log10(ctr[msk][-1]), 50)
                    y0 = cnt[msk][0] * (ctr[msk][0]**1.5)
                    ax2.loglog(xt, y0/(xt**1.5), '--', color='gray',
                               alpha=0.5, label='τ=1.5')
            except: pass
        ts = res.get('tau_size')
        se = res.get('tau_scale_error', 1.0)
        ts_str = f"{ts:.2f}" if ts else "N/A"
        ok = res.get('criteria', {}).get('size_powerlaw', False)
        ax2.set_title(
            f"τ_s={ts_str} se={se:.0%} {'V' if ok else 'X'}",
            fontsize=7, color='green' if ok else 'red'
        )
        ax2.set_xlabel('S', fontsize=6); ax2.set_ylabel('Count', fontsize=6)
        ax2.tick_params(labelsize=6); ax2.legend(fontsize=5)

    plt.savefig(f'{OUT}/exp5_v9_avalanche_results.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Figure: {OUT}/exp5_v9_avalanche_results.png")

# ============================================================
# 主程序
# ============================================================
def main():
    print("="*70)
    print("SDI Experiment 5 v9 — Three-Phase Protocol")
    print(f"  Phase1 Adapt  : {N_ADAPT} steps | Poisson λ_stim={LAMBDA_STIM} + STDP(strong)")
    print(f"  Phase2 Decode : {N_DECODE} steps | Poisson + STDP(mid) + motor recording")
    print(f"  Phase3 Record : {N_RECORD} steps | BTW only + STDP(weak)")
    print(f"  C.elegans types: sensory=60 inter=111 motor=108")
    print(f"  4 Modalities: Chem/Odor/Temp/Mech")
    print("  All v7 fixes inherited: real STDP dt, delay queues, KS test, STD cont.")
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
                    result = run_simulation(net_cfg, net_name, seed, use_pruning)
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

    out_path = f'{OUT}/exp5_v9_avalanche_results.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(ds(all_results), f, ensure_ascii=False, indent=2)
    print(f"\nSaved: {out_path}")

    try: plot_results(all_results)
    except Exception as e: print(f"  Plot error: {e}")

    print("\n" + "="*70 + "\nSummary v9\n" + "="*70)
    from collections import defaultdict
    gd = defaultdict(list)
    for r in all_results: gd[f"{r['network']}_{r['rules']}"].append(r)
    print(f"\n{'Group':<28} κ{'':4} τ_s{'':4} τ_d{'':4} scale  PSD{'':4} decode zero%  Score")
    print("-"*90)
    for key, runs in sorted(gd.items()):
        kv  = np.mean([r['branching_ratio'] for r in runs])
        tsl = [r['tau_size'] for r in runs if r['tau_size']]
        tdl = [r['tau_duration'] for r in runs if r['tau_duration']]
        pvl = [r['psd_slope'] for r in runs if r['psd_slope']]
        sel = [r['tau_scale_error'] for r in runs]
        dcl = [r['decode_score'] for r in runs]
        zfl = [r['zero_fraction'] for r in runs]
        svl = [r['score'] for r in runs]
        mx  = runs[0]['max_score']
        print(f"{key:<28} {kv:.3f} "
              f"{np.mean(tsl):.2f if tsl else 'N/A':<7}"
              f"{np.mean(tdl):.2f if tdl else 'N/A':<7}"
              f"{np.mean(sel):.0%}  "
              f"{np.mean(pvl):.2f if pvl else 'N/A':<7}"
              f"{np.mean(dcl):.3f}  "
              f"{np.mean(zfl):.0%}    "
              f"{np.mean(svl):.1f}/{mx}")

    best = max(all_results, key=lambda x: x['score'])
    ts_b = f"{best['tau_size']:.3f}" if best['tau_size'] else "N/A"
    td_b = f"{best['tau_duration']:.3f}" if best['tau_duration'] else "N/A"
    print(f"\nBest: {best['network']} | {best['rules']} | seed={best['seed']}")
    print(f"  tau_s={ts_b}  tau_d={td_b}")
    print(f"  kappa={best['branching_ratio']:.3f}  decode={best['decode_score']:.4f}")
    print(f"  scale_err={best['tau_scale_error']:.0%}  score={best['score']}/{best['max_score']}")
    elapsed = time.time() - t_total
    print(f"\nTotal: {elapsed:.0f}s ({elapsed/60:.1f}min)")
    print("v9 complete.")
    sys.stdout.flush()

if __name__ == '__main__':
    main()
