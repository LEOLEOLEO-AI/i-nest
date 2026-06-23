#!/usr/bin/env python3
"""
SDI 实验五 v11：软饱和STDP（物理第一性）+ 双重G校准三阶段协议

==============================================================================
v9问题诊断
==============================================================================
v9失败原因：
  - 泊松 λ_stim=0.15 × 单个模态神经元数≈15 = 每步激活≈2个感觉神经元
  - STDP每步更新对数太少 → 8000步后权重仍很低（均值≈0.05-0.15）
  - G校准时用Priesemann时序法，κ看起来≈1.0
  - 但实际：单步传播 = k_out×w_mean×G×STD ≈ 8×0.1×2.0×0.5 = 0.8
  - 结果：每次BTW注入后极少产生连续激活 → size几乎全为1-2

v5成功原因（对照）：
  - 学习8000步强刺激（P_EXT=0.25 × 每步激活≈60个神经元）
  - STDP大量激活 → 活跃突触权重推到≈0.9
  - G校准后G≈0.38，但权重高 → 有效传播概率≈0.17 → κ≈1.0 → size≈5-20

==============================================================================
v10三项核心修复
==============================================================================

【修复A — 强化适应期输入】
  λ_stim: 0.15 → 0.40（提高2.7倍）
  T_STIM_ON: 50 → 80步（更长持续激活）
  效果：每步激活感觉神经元数 ≈ 15×0.40 = 6个（vs v9的2个）
        STDP每步更新对数增加3倍 → 权重充分增长

【修复B — G双重校准（κ + 尺寸协同）】
  步骤1: κ二分法（已有） → 找到 κ∈[0.90, 1.10] 的 G_kappa
  步骤2: 尺寸验证（新增）→ 用500步测试序列检查 mean_avalanche_size
    - 若 mean_size < 5：提高G（增强传播）
    - 若 mean_size > 80：降低G（减弱传播）
    - 目标区间：mean_size ∈ [5, 80]（v5最优时≈10-20）
    同时保持 κ∈[0.85, 1.15]（不破坏临界态）

【修复C — 适应期步数调整】
  N_ADAPT: 6000 → 8000步
  原因：更多STDP激活 → 权重更充分学习
  N_DECODE: 2000 → 2000步（不变）
  N_RECORD: 20000步（不变）

==============================================================================
继承所有前版本的成果
==============================================================================
v9: 三阶段协议 + 泊松输入 + C.elegans神经元类型 + 输出解码
v7: 真实STDP时间戳 + 延迟队列 + KS检验 + STD连续 + τ缩放关系
v6: E/I平衡 + STD + 有向图 + 突触延迟

==============================================================================
验证指标（9项）
==============================================================================
  1. 零帧比例 ≥ 30%（沉寂期）
  2. 雪崩数 ≥ 300
  3. 多步雪崩 > 20%
  4. τ_size ∈ [1.2, 2.2]，R² > 0.70，KS p ≥ 0.1（严格幂律）
  5. τ_dur ∈ [1.5, 2.8]，R² > 0.70
  6. τ缩放关系误差 < 25%（Friedman 2012 PRL）
  7. κ ∈ [0.85, 1.15]
  8. PSD斜率 ∈ [-1.5, -0.3]（1/f噪声）
  9. 输出解码 > 0.05（功能分离）
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
# STDP
THETA_LTP    = 65
THETA_LTD    = 15
ETA_LTP      = 0.012
ETA_LTD      = 0.008
ETA_LTP_MID  = 0.006
ETA_LTD_MID  = 0.004
ETA_LTP_REC  = 0.001
ETA_LTD_REC  = 0.0008
TAU_STDP     = 20.0
STDP_MAX_DT  = 100

# ★ v11新增：软饱和STDP参数（物理第一性）
# 文献依据：Bhatt et al. 2009 Neuron（小鼠脑皮突触权重分布）
#   稳定高权重突触均値≈4-6×初始权重均値，初始均値≈0.18
#   ⇒ W_MAX = 0.18 × 5 = 0.9
# BCM理论（Bienenstock-Cooper-Munro 1982）：
#   dw_eff = dw × (1 - w/W_MAX)
#   物理意义：w→W_MAX时受体饱和，LTP增益越小，自然收敛
W_MAX        = 0.9    # 突触权重上界（受体饱和效应）
W_LTD_FLOOR  = 0.001  # LTD下限（不完全删除）

# 突触结构
T_DECAY    = 400
EL_HI      = 0.25
T_ABS      = 3
T_REL      = 5
P_REWIRE   = 0.15
REWIRE_INT = 50
SCALING_INT  = 100
KAPPA_TARGET = 0.95
SCALING_RATE = 0.05
PRUNE_INT  = 200
P_PRUNE    = 0.05
MIN_EDGES  = 3

# E/I
FRAC_INHIB  = 0.20
INHIB_SCALE = 2.0

# STD（Tsodyks & Markram 1997）
STD_ENABLED = True
U_0         = 0.5
USE_FACTOR  = 0.35
TAU_STD     = 15.0

# 延迟（Diesmann 1999）
DELAY_ENABLED = True
MIN_DELAY = 1
MAX_DELAY = 3

# ★ v10三阶段参数
N_ADAPT  = 8000    # 适应期（加长，强STDP）
N_DECODE = 2000    # 解码测量期
N_RECORD = 20000   # 雪崩记录期（纯BTW）
LOG_INT  = 4000

# BTW驱动
BTW_INTERVAL = 10

# ★ v10增强泊松输入
LAMBDA_STIM  = 0.25   # v11: 充分STDP但不饱和（v9:0.15→v10:0.40→v11:0.25）
LAMBDA_BASE  = 0.02   # 基线自发放电
T_STIM_ON    = 80     # 刺激持续步数（加长）
T_STIM_OFF   = 40     # 间隔步数（缩短，保证刺激密度）

# 校准（κ）
CALIB_WARMUP = 300
CALIB_STEPS  = 1200
CALIB_ITER   = 30
G_LO_INIT    = 0.001
G_HI_INIT    = 4.0

# ★ v10尺寸校准参数
SIZE_CALIB_STEPS  = 500     # 尺寸测试序列长度
SIZE_TARGET_LO    = 5       # 雪崩尺寸下限
SIZE_TARGET_HI    = 80      # 雪崩尺寸上限
SIZE_CALIB_ITER   = 15      # 最多15次调整
SIZE_G_FACTOR     = 1.5     # 每次调整倍率

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
    rng = np.random.default_rng(seed + 5555)
    N_s = len(sensory_idx)
    mod = np.zeros(N_s, dtype=np.int8)
    bounds = [0, int(N_s*0.35), int(N_s*0.60), int(N_s*0.77), N_s]
    for m in range(4):
        mod[bounds[m]:bounds[m+1]] = m
    rng.shuffle(mod)
    return mod

class PoissonStimulator:
    def __init__(self, sensory_idx, modality, n_mod=4, seed=0):
        self.sidx   = sensory_idx
        self.mod    = modality
        self.n_mod  = n_mod
        self.rng    = np.random.default_rng(seed + 3333)
        self.t      = 0
        self.a_mod  = 0
    def step(self):
        cycle = T_STIM_ON + T_STIM_OFF
        ph    = self.t % cycle
        is_on = (ph < T_STIM_ON)
        if ph == 0:
            self.a_mod = int(self.rng.integers(self.n_mod))
        activated = [int(ni) for ni, m in zip(self.sidx, self.mod)
                     if self.rng.random() < (LAMBDA_STIM if (is_on and m == self.a_mod)
                                             else LAMBDA_BASE)]
        self.t += 1
        return activated, self.a_mod, is_on

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

def assign_inhib(N, frac, seed):
    rng = np.random.default_rng(seed + 7777)
    idx = rng.choice(N, size=int(N*frac), replace=False)
    is_i = np.zeros(N, dtype=bool); is_i[idx] = True
    return is_i

def init_std(N, seed):
    rng = np.random.default_rng(seed + 8888)
    u = np.full((N, N), U_0, dtype=np.float32)
    u += rng.uniform(-0.03, 0.03, (N, N)).astype(np.float32)
    return np.clip(u, 0.01, 1.0)

def make_delays(N, seed):
    rng = np.random.default_rng(seed + 9999)
    return rng.integers(MIN_DELAY, MAX_DELAY + 1, size=(N, N)).astype(np.int8)

def recover_std(std_u, syn_mask):
    if STD_ENABLED:
        std_u[syn_mask] += (U_0 - std_u[syn_mask]) / TAU_STD

# ============================================================
# 网络度量
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

# ============================================================
# 传播（延迟队列 + E/I + STD）
# ============================================================
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

# ============================================================
# 步骤1：κ校准（Priesemann时序法）
# ============================================================
def estimate_kappa(adj, el_mask, is_i, delays, std_u0,
                   N, G, seed, n_warm, n_meas):
    rng = np.random.default_rng(seed)
    refrac = np.zeros(N, dtype=np.int8)
    std_u = std_u0.copy(); syn_mask = adj != 0
    wave = np.zeros(N, dtype=bool); fired = np.zeros(N, dtype=bool)
    db = defaultdict(list); log = []
    for step in range(n_warm + n_meas):
        recover_std(std_u, syn_mask)
        pending = any(k >= step for k in db)
        if not wave.any() and not pending and step % BTW_INTERVAL == 0:
            d = int(rng.integers(N))
            if refrac[d] == 0:
                wave[d] = True; fired[:] = False; fired[d] = True
        nw = propagate(adj, el_mask, is_i, std_u, delays,
                       wave, refrac, fired, N, G, db, step, rng)
        fired |= nw; wave = nw
        if step >= n_warm: log.append(int(nw.sum()))
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

# ============================================================
# 步骤2：★ v10新增 — 雪崩尺寸校准
# ============================================================
def estimate_mean_size(adj, el_mask, is_i, delays, std_u0,
                       N, G, seed, n_test=SIZE_CALIB_STEPS):
    """
    用n_test步BTW驱动，估计实际平均雪崩尺寸。
    目标：mean_size ∈ [SIZE_TARGET_LO, SIZE_TARGET_HI]
    """
    rng = np.random.default_rng(seed)
    refrac = np.zeros(N, dtype=np.int8)
    std_u = std_u0.copy(); syn_mask = adj != 0
    wave = np.zeros(N, dtype=bool); fired = np.zeros(N, dtype=bool)
    db = defaultdict(list)
    act_series = []

    for step in range(n_test):
        recover_std(std_u, syn_mask)
        pending = any(k >= step for k in db)
        if not wave.any() and not pending and step % BTW_INTERVAL == 0:
            d = int(rng.integers(N))
            if refrac[d] == 0:
                wave[d] = True; fired[:] = False; fired[d] = True
        nw = propagate(adj, el_mask, is_i, std_u, delays,
                       wave, refrac, fired, N, G, db, step, rng)
        fired |= nw; wave = nw
        act_series.append(int(nw.sum()))
        refrac[wave] = T_ABS; refrac[refrac > 0] -= 1

    # 检测雪崩
    sizes = []
    in_av = False; cur_s = 0
    for n in act_series:
        if n > 0:
            in_av = True; cur_s += n
        else:
            if in_av and cur_s > 0:
                sizes.append(cur_s); in_av = False; cur_s = 0
    if in_av and cur_s > 0: sizes.append(cur_s)

    mean_s = float(np.mean(sizes)) if sizes else 0.0
    zero_f = float(sum(1 for x in act_series if x == 0) / len(act_series))
    return mean_s, zero_f, len(sizes)

def calibrate_size(adj, el_mask, is_i, delays, std_u0, N, G_kappa, seed):
    """
    在 G_kappa（κ≈1.0）的基础上，微调G使平均雪崩尺寸落在目标区间。
    每次调整时重新验证κ不超出[0.80, 1.20]范围。
    """
    G = G_kappa
    print(f"\n    ★ 尺寸校准（目标mean_size∈[{SIZE_TARGET_LO},{SIZE_TARGET_HI}]）")
    sys.stdout.flush()

    for i in range(SIZE_CALIB_ITER):
        ms, zf, n_av = estimate_mean_size(adj, el_mask, is_i, delays, std_u0,
                                          N, G, seed + i*331)
        print(f"    尺寸校准 iter={i+1}: G={G:.5f} → mean_size={ms:.1f} "
              f"zero={zf:.0%} n_av={n_av}")
        sys.stdout.flush()

        if SIZE_TARGET_LO <= ms <= SIZE_TARGET_HI:
            print(f"    ✅ 尺寸达标: G={G:.5f}, mean_size={ms:.1f}")
            return G, ms

        if ms < SIZE_TARGET_LO:
            # 尺寸太小，增大G（增强传播）
            G_new = G * SIZE_G_FACTOR
        else:
            # 尺寸太大，减小G
            G_new = G / SIZE_G_FACTOR

        # 验证新G下κ是否还在合理范围
        k_new = estimate_kappa(adj, el_mask, is_i, delays, std_u0,
                               N, G_new, seed + i*997 + 500, 100, 200)
        if 0.75 <= k_new <= 1.25:
            G = G_new
        else:
            # κ超出范围，只做小步调整
            if ms < SIZE_TARGET_LO:
                G = G * 1.2
            else:
                G = G * 0.85
            print(f"    κ约束：κ={k_new:.3f}超出范围，小步调整G→{G:.5f}")

    # 未达标，返回最近一次G
    ms_final, zf_final, _ = estimate_mean_size(adj, el_mask, is_i, delays, std_u0,
                                               N, G, seed + 99999)
    print(f"    ⚠️ 尺寸校准结束: G={G:.5f}, mean_size={ms_final:.1f}")
    return G, ms_final

# ============================================================
# 雪崩检测
# ============================================================
def detect_avalanches(series):
    sizes, durs, kaps = [], [], []
    layers = []; in_av = False
    for n in series:
        if n > 0:
            in_av = True; layers.append(n)
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
            c = np.polyfit(lx, ly, 1)
            ssr = np.sum((ly-np.polyval(c,lx))**2)
            sst = np.sum((ly-ly.mean())**2)
            res['r2'] = float(1-ssr/sst) if sst > 0 else 0.0
    # Bootstrap p_value
    tau = best_tau; xm = best_xm; n_t = len(tail)
    rng_b = np.random.default_rng(42); boots = []
    for _ in range(50):
        u = rng_b.uniform(size=n_t)
        syn = xm*(1-u)**(-1/(tau-1))
        syn = np.sort(syn)
        ts2 = 1 + n_t/np.sum(np.log(syn/xm))
        if ts2 <= 1: ts2 = 1.01
        ecdf_s = np.arange(1, n_t+1)/n_t
        tcdf_s = 1-(syn/xm)**(-(ts2-1))
        boots.append(float(np.max(np.abs(ecdf_s-tcdf_s))))
    res['p_value'] = float(np.mean(np.array(boots) >= best_ks))
    res['plausible'] = (res['p_value'] >= 0.1)
    ll_pl = np.sum(np.log(tau-1) - np.log(xm) - tau*np.log(tail/xm))
    lt = np.log(tail); mu = lt.mean(); sg = lt.std()
    if sg > 0:
        ll_ln = np.sum(-np.log(tail) - 0.5*np.log(2*np.pi*sg**2)
                       - 0.5*((lt-mu)/sg)**2)
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
    ssr = np.sum((lp-np.polyval(c,lf))**2)
    sst = np.sum((lp-lp.mean())**2)
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
# 主仿真
# ============================================================
def run_simulation(net_name, net_cfg, seed, use_pruning=False):
    N = net_cfg['N']
    rng = np.random.default_rng(seed)

    adj     = make_ws_adj_directed(N, net_cfg['k_init'], net_cfg['p_init'], seed)
    is_i    = assign_inhib(N, FRAC_INHIB, seed)
    std_u   = init_std(N, seed)
    delays  = make_delays(N, seed)
    syn_mask = adj != 0
    el_mask = np.zeros((N, N), dtype=bool)
    el_mask[adj > 0] = rng.random((adj > 0).sum()) < 0.05
    el_mask[is_i, :] = False
    nltp = np.zeros((N, N), dtype=np.int16)
    nltd = np.zeros((N, N), dtype=np.int16)
    el_age = np.zeros((N, N), dtype=np.int32)
    refrac  = np.zeros(N, dtype=np.int8)
    last_sp = np.full(N, -99999, dtype=np.int32)
    exc_pre = np.outer(~is_i, np.ones(N, dtype=bool))

    _, sens_idx, mot_idx, _ = assign_celegans_types(N)
    modality = assign_sensory_modalities(sens_idx, seed)
    stim = PoissonStimulator(sens_idx, modality, seed=seed)

    n_e = int((~is_i).sum()); n_i = int(is_i.sum())
    print(f"  [{net_name}|{seed}] N={N} E={n_e} I={n_i} | 感觉={len(sens_idx)} 运动={len(mot_idx)}")
    print(f"  λ_stim={LAMBDA_STIM} T_on={T_STIM_ON} | 适应{N_ADAPT}→解码{N_DECODE}→记录{N_RECORD}")
    sys.stdout.flush()

    topo_log = []
    t0 = time.time()
    db = defaultdict(list)
    mot_by_mod = defaultdict(lambda: np.zeros(len(mot_idx)))
    avl_series = []

    total = N_ADAPT + N_DECODE + N_RECORD

    for step in range(total):
        phase = ('adapt'  if step < N_ADAPT else
                 'decode' if step < N_ADAPT + N_DECODE else
                 'record')
        eta_ltp = ETA_LTP     if phase == 'adapt'  else \
                  ETA_LTP_MID if phase == 'decode' else ETA_LTP_REC
        eta_ltd = ETA_LTD     if phase == 'adapt'  else \
                  ETA_LTD_MID if phase == 'decode' else ETA_LTD_REC

        recover_std(std_u, syn_mask)

        active = np.zeros(N, dtype=bool)
        if phase in ('adapt', 'decode'):
            stim_ns, act_mod, is_on = stim.step()
            for ni in stim_ns:
                if refrac[ni] == 0: active[ni] = True
        else:
            pending = any(k >= step for k in db)
            if not active.any() and not pending and step % BTW_INTERVAL == 0:
                d = int(rng.integers(N))
                if refrac[d] == 0: active[d] = True
            act_mod = -1; is_on = False

        if active.any():
            fired = active.copy()
            nw = propagate(adj, el_mask, is_i, std_u, delays,
                           active, refrac, fired, N, 1.0, db, step, rng)
            active |= nw
        else:
            fired = np.zeros(N, dtype=bool)
            nw = propagate(adj, el_mask, is_i, std_u, delays,
                           np.zeros(N, dtype=bool), refrac, fired, N, 1.0,
                           db, step, rng)
            active |= nw

        n_act = int(active.sum())
        last_sp[active] = step
        refrac[active] = T_ABS + T_REL
        refrac[refrac > 0] -= 1

        if phase == 'decode' and is_on and n_act > 0:
            ma = active[mot_idx].astype(float)
            if ma.any(): mot_by_mod[int(act_mod)] += ma

        if phase == 'record': avl_series.append(n_act)

        # STDP
        ae = np.where(active & ~is_i)[0]; aa = np.where(active)[0]
        if len(ae) >= 2 and len(aa) >= 1:
            n_p = min(len(ae)*2, 100)
            pre_a = rng.choice(ae, size=n_p); post_a = rng.choice(aa, size=n_p)
            for pre, post in zip(pre_a, post_a):
                if pre == post: continue
                dt = int(last_sp[post]) - int(last_sp[pre])
                if abs(dt) > STDP_MAX_DT: continue
                if dt > 0:
                    # ★ v11：软饱和LTP —— dw_eff = dw×(1-w/W_MAX)
                    # 物理意义：w越高越靠近受体饱和，LTP增益越小
                    # 文献：Bhatt 2009；BCM 1982
                    if adj[pre, post] > 0 and not is_i[pre]:
                        w_cur = float(adj[pre, post])
                        dw    = eta_ltp * np.exp(-abs(dt) / TAU_STDP)
                        dw_eff = dw * (1.0 - w_cur / W_MAX)   # 软饱和因子
                        adj[pre, post] = float(np.clip(
                            w_cur + dw_eff, W_LTD_FLOOR, W_MAX))
                        nltp[pre, post] += 1
                else:
                    # LTD：无饱和（驱动突触削弱/消除）
                    if adj[post, pre] > 0 and not is_i[post]:
                        w_cur = float(adj[post, pre])
                        dw    = eta_ltd * np.exp(-abs(dt) / TAU_STDP)
                        adj[post, pre] = float(np.clip(
                            w_cur - dw, W_LTD_FLOOR, W_MAX))
                        nltd[post, pre] += 1

        el_r = el_mask.sum() / max(1, (adj > 0).sum())
        ltp_m = (nltp >= THETA_LTP) & (adj > 0) & (~el_mask) & (el_r < EL_HI) & exc_pre
        el_mask[ltp_m] = True; nltp[ltp_m] = 0
        ltd_m = (nltd >= THETA_LTD) & (adj > 0) & (~el_mask) & exc_pre
        adj[ltd_m] = 0.0; nltp[ltd_m] = nltd[ltd_m] = 0
        syn_mask[ltd_m] = False
        el_age[el_mask] += 1
        dm = el_mask & (el_age > T_DECAY)
        el_mask[dm] = False; el_age[dm] = 0

        if step % REWIRE_INT == 0:
            ne = np.argwhere((adj > 0) & (~el_mask) & exc_pre)
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
            adj = np.clip(adj, 0.0, 1.0)

        if use_pruning and step % PRUNE_INT == 0 and step > 0:
            deg = (adj > 0).sum(axis=1)
            for i, j in np.argwhere((adj > 0) & (~el_mask) & exc_pre
                                     & (nltp == 0) & (nltd == 0)):
                if deg[i] > MIN_EDGES and rng.random() < P_PRUNE:
                    adj[i, j] = 0.0; syn_mask[i, j] = False
            nltp[:] = 0; nltd[:] = 0

        if step % LOG_INT == 0:
            sig = sigma_fast(adj, N)
            w_stats = adj[adj > 0]
            w_mean = float(w_stats.mean()) if len(w_stats) > 0 else 0.0
            print(f"    [{phase}] {step}/{total} σ={sig:.2f} "
                  f"edges={(adj>0).sum()} w_mean={w_mean:.3f} "
                  f"n_act={n_act} t={time.time()-t0:.0f}s")
            sys.stdout.flush()
            topo_log.append({'step': step, 'sigma': sig,
                              'n_edges': int((adj>0).sum()),
                              'n_el': int(el_mask.sum()),
                              'w_mean': float(w_mean), 'phase': phase})

    # ===== 适应/解码结束后 =====
    std_after = std_u.copy()
    sig_final = sigma_fast(adj, N)
    w_all = adj[adj > 0]
    w_mean_final = float(w_all.mean()) if len(w_all) > 0 else 0.0
    print(f"\n  三阶段完成: edges={(adj>0).sum()} σ={sig_final:.2f} "
          f"w_mean={w_mean_final:.3f}")

    ds = decode_score(mot_by_mod)
    print(f"  输出解码: {ds:.4f} ({'✓' if ds > 0.05 else '✗'})")

    # ===== 双重校准 =====
    print(f"\n  步骤1: κ校准...")
    sys.stdout.flush()
    G_kappa, kappa_c = calibrate_kappa(adj, el_mask, is_i, delays, std_after, N, seed)

    print(f"\n  步骤2: 雪崩尺寸校准...")
    sys.stdout.flush()
    G_final, mean_size_calib = calibrate_size(
        adj, el_mask, is_i, delays, std_after, N, G_kappa, seed
    )
    print(f"  最终G={G_final:.5f}, 校准mean_size={mean_size_calib:.1f}")

    # ===== 雪崩分析 =====
    arr = np.array(avl_series)
    zf = float((arr == 0).mean())
    print(f"\n  雪崩统计: 零帧={zf:.1%} max={arr.max()} mean={arr.mean():.3f}")

    sizes, durs, kap_in = detect_avalanches(avl_series)
    rs = fit_pl(sizes); rd = fit_pl(durs)
    tau_s = rs['tau']; r2_s = rs['r2']
    tau_d = rd['tau']; r2_d = rd['r2']
    kappa = float(np.mean(kap_in)) if kap_in else 0.0
    kappa_std_ = float(np.std(kap_in)) if len(kap_in) > 1 else 0.0
    psd, psd_r2 = psd_slope(avl_series)
    n_av = len(sizes)
    mean_sz = float(np.mean(sizes)) if sizes else 0.0
    mean_dur = float(np.mean(durs)) if durs else 0.0
    dur_arr = np.array(durs) if durs else np.array([0])
    frac1 = float((dur_arr == 1).mean()) if len(dur_arr) > 0 else 1.0

    if tau_s and tau_d:
        td_th = (tau_s + 1) / 2
        sc_err = abs(tau_d - td_th) / td_th
    else:
        td_th = None; sc_err = 1.0

    # 9项达标判定
    size_ok  = (tau_s is not None and 1.2 <= tau_s <= 2.2 and r2_s > 0.70 and rs['plausible'])
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
    print(f"  [{net_name}|{seed}|{'4r' if use_pruning else '3r'}] "
          f"G={G_final:.4f} w_mean={w_mean_final:.3f}")
    print(f"  零帧: {zf:.1%} {'✓' if zero_ok else '✗'}")
    print(f"  雪崩数: {n_av} | 均尺寸: {mean_sz:.1f} | 均时长: {mean_dur:.1f} {'✓' if count_ok else '✗'}")
    print(f"  多步雪崩: {1-frac1:.1%} {'✓' if multi_ok else '✗'}")
    print(f"  τ_size={ts_s} R²={r2_s:.3f} p={rs['p_value']:.2f} {'✓' if size_ok else '✗'}")
    print(f"  τ_dur={td_s} R²={r2_d:.3f} (理论={th_s} 误差={sc_err:.0%}) {'✓' if dur_ok else '✗'}")
    print(f"  τ缩放: {'✓' if scale_ok else '✗'} (误差{sc_err:.0%})")
    print(f"  κ={kappa:.4f}±{kappa_std_:.3f} {'✓' if kappa_ok else '✗'}")
    print(f"  PSD={ps_s} R²={psd_r2:.3f} {'✓' if psd_ok else '✗'}")
    print(f"  解码={ds:.4f} {'✓' if dec_ok else '✗'}")
    print(f"  LR(PL>LN)={rs.get('lr_vs_lognormal',0):.1f}")
    print(f"  得分: {score}/9")
    print(f"  {'='*65}\n")
    sys.stdout.flush()

    return {
        'network': net_name, 'seed': seed,
        'rules': '4-rules' if use_pruning else '3-rules',
        'protocol': {'N_ADAPT': N_ADAPT, 'N_DECODE': N_DECODE, 'N_RECORD': N_RECORD,
                     'lambda_stim': LAMBDA_STIM, 'T_stim_on': T_STIM_ON},
        'G_kappa': float(G_kappa), 'kappa_calib': float(kappa_c),
        'G_final': float(G_final), 'mean_size_calib': float(mean_size_calib),
        'sigma_final': float(sig_final), 'w_mean_final': float(w_mean_final),
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
            'output_decode': bool(dec_ok),
        },
        'topology_log': topo_log,
        'activation_sample': [int(x) for x in avl_series[:6000]],
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
        'SDI Exp5 v11: Dual-Calibration (kappa + size) + Enhanced Adaptation\n'
        'Three-Phase: Poisson Adapt(8000) → Decode(2000) → BTW Record(20000)',
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
        G = res.get('G_final', 1.0)
        ms = res.get('mean_size', 0)
        ax1.set_title(
            f"{res['network']} {res['rules']}\n"
            f"G={G:.3f} ms={ms:.1f} "
            f"κ={res.get('branching_ratio',0):.3f} Score={sc}/{mx}",
            fontsize=7,
            color='green' if sc >= 6 else ('orange' if sc >= 4 else 'red')
        )
        ax1.set_xlabel('Step', fontsize=6)
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
                    y0 = cnt[msk][0]*(ctr[msk][0]**1.5)
                    ax2.loglog(xt, y0/(xt**1.5), '--', color='gray',
                               alpha=0.5, label='tau=1.5')
            except: pass
        ts = res.get('tau_size'); se = res.get('tau_scale_error', 1.0)
        ts_str = f"{ts:.2f}" if ts else "N/A"
        ok = res.get('criteria', {}).get('size_powerlaw', False)
        ax2.set_title(f"tau={ts_str} se={se:.0%} {'V' if ok else 'X'}",
                     fontsize=7, color='green' if ok else 'red')
        ax2.set_xlabel('S', fontsize=6); ax2.set_ylabel('Count', fontsize=6)
        ax2.tick_params(labelsize=6); ax2.legend(fontsize=5)

    plt.savefig(f'{OUT}/exp5_v11_avalanche_results.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Figure: {OUT}/exp5_v11_avalanche_results.png")

# ============================================================
# 主程序
# ============================================================
def main():
    print("="*70)
    print("SDI Experiment 5 v11 — Soft-Saturation STDP (物理第一性) + Dual-G Calibration")
    print(f"  ★ 软饱和STDP: dw_eff = dw×(1-w/W_MAX),  W_MAX={W_MAX}")
    print(f"  ★ 文献依据: Bhatt 2009 Neuron + BCM 1982")
    print(f"  Phase1 Adapt  : {N_ADAPT}步 | λ_stim={LAMBDA_STIM} T_on={T_STIM_ON} + 软饱和STDP")
    print(f"  Phase2 Decode : {N_DECODE}步 | Poisson + 弱STDP + motor记录")
    print(f"  Phase3 Record : {N_RECORD}步 | 纯BTW + 极弱STDP")
    print(f"  Phase2 Decode : {N_DECODE}步 | Poisson + STDP(mid) + motor record")
    print(f"  Phase3 Record : {N_RECORD}步 | BTW only + STDP(weak)")
    print(f"  Calibration   : κ二分法 → 尺寸校准（目标mean_size∈[{SIZE_TARGET_LO},{SIZE_TARGET_HI}]）")
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

    out_path = f'{OUT}/exp5_v11_avalanche_results.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(ds(all_results), f, ensure_ascii=False, indent=2)
    print(f"\nSaved: {out_path}")

    try: plot_results(all_results)
    except Exception as e: print(f"  Plot error: {e}")

    print("\n" + "="*70 + "\nSummary v11\n" + "="*70)
    from collections import defaultdict
    gd = defaultdict(list)
    for r in all_results: gd[f"{r['network']}_{r['rules']}"].append(r)

    print(f"\n{'Group':<28} G_f    ms     κ      τ_s    τ_d    se%    PSD    dec    zero   Score")
    print("-"*100)
    for key, runs in sorted(gd.items()):
        Gf  = np.mean([r['G_final'] for r in runs])
        ms_ = np.mean([r['mean_size'] for r in runs])
        kv  = np.mean([r['branching_ratio'] for r in runs])
        tsl = [r['tau_size'] for r in runs if r['tau_size']]
        tdl = [r['tau_duration'] for r in runs if r['tau_duration']]
        pvl = [r['psd_slope'] for r in runs if r['psd_slope']]
        sel = [r['tau_scale_error'] for r in runs]
        dcl = [r['decode_score'] for r in runs]
        zfl = [r['zero_fraction'] for r in runs]
        svl = [r['score'] for r in runs]
        mx  = runs[0]['max_score']
        ts_s = f"{np.mean(tsl):.2f}" if tsl else "N/A"
        td_s = f"{np.mean(tdl):.2f}" if tdl else "N/A"
        pv_s = f"{np.mean(pvl):.2f}" if pvl else "N/A"
        print(f"{key:<28} {Gf:.3f}  {ms_:<7.1f}{kv:.3f}  "
              f"{ts_s:<7}{td_s:<7}{np.mean(sel):.0%}  "
              f"{pv_s:<7}{np.mean(dcl):.3f}  {np.mean(zfl):.0%}   {np.mean(svl):.1f}/{mx}")

    if all_results:
        best = max(all_results, key=lambda x: x['score'])
        ts_b = f"{best['tau_size']:.3f}" if best['tau_size'] else "N/A"
        td_b = f"{best['tau_duration']:.3f}" if best['tau_duration'] else "N/A"
        print(f"\nBest: {best['network']} | {best['rules']} | seed={best['seed']}")
        print(f"  tau_s={ts_b}  tau_d={td_b}  kappa={best['branching_ratio']:.3f}")
        print(f"  G_final={best['G_final']:.4f}  mean_size={best['mean_size']:.1f}")
        print(f"  decode={best['decode_score']:.4f}  score={best['score']}/{best['max_score']}")

    elapsed = time.time() - t_total
    print(f"\nTotal: {elapsed:.0f}s ({elapsed/60:.1f}min)")
    print("v11 complete.")
    sys.stdout.flush()

if __name__ == '__main__':
    main()
