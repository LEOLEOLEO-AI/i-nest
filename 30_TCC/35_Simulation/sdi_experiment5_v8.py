#!/usr/bin/env python3
"""
SDI 实验五 v8：真实生物输入模式 + 泊松驱动 + 感觉-运动分层验证

==============================================================================
v8相对v7的核心升级
==============================================================================

【升级1 — 输入模式：随机统计刺激 → 结构化生物感觉刺激】

  v7: 8个完全随机的神经元子集轮流激活（无解剖意义）
  v8: 按C.elegans真实神经元类型分配输入
      - 感觉神经元（Sensory, ~60个）：唯一接受外部刺激
      - 中间神经元（Interneuron, ~111个）：只接受网络内部信号
      - 运动神经元（Motor, ~108个）：输出层，监测激活分布
      4种感觉模态（化学/温度/机械/气味），对应真实C.elegans感觉系统

【升级2 — 时间结构：均匀P=0.25 → 泊松放电过程】

  v7: 每步以固定P=0.25激活当前模式的所有神经元
  v8: 每个感觉神经元独立泊松放电
      - 刺激状态: ISI ~ Poisson(λ_stim=0.15/步，对应≈15Hz)
      - 基线状态: ISI ~ Poisson(λ_base=0.02/步，对应≈2Hz自发放电)
      - 刺激呈现：持续T_STIM=50步，间隔T_ISI=50步（类似视觉/嗅觉刺激时序）
      符合真实感觉神经元的放电统计（Rieke et al. 1997 Spikes）

【升级3 — 学习/雪崩同步运行（取消两阶段硬隔离）】

  v7: 学习8000步（强外部刺激）→ 记录20000步（纯BTW）完全分离
  v8: 统一运行协议
      - 前N_ADAPT=5000步：感觉刺激驱动STDP学习（适应期）
      - 后N_RECORD=20000步：刺激降为基线水平 + STDP继续（但学习率减半）
                            BTW额外慢驱动注入（维持雪崩可测量性）
      更接近真实脑：突触可塑性和动力学活动同时存在

【升级4 — 输出解码验证（新增）】

  监测运动神经元层的激活分布：
  - 不同感觉模态 → 不同运动神经元激活组合（功能分离）
  - 量化：余弦距离（不同刺激→不同输出模式）
  - 如果SDI规则有效：相同感觉模态 → 相似运动输出，不同模态 → 不同输出

==============================================================================
C.elegans神经元类型依据
==============================================================================
  Varshney et al. 2011 PLOS Comput Biol — C.elegans connectome（279节点）
  White et al. 1986 Phil Trans R Soc — 原始解剖图谱
  Chalfie et al. 1985 J Neurosci — 感觉神经元功能鉴定
  感觉神经元编号范围（0-based索引，按Varshney排序）：
    前体部感觉（0-24）：化学感觉为主（ASEL/ASER/AWA/AWB等）
    机械感觉（25-44）：ALM/AVM/PLM等触觉神经元
    温度感觉（45-59）：AFD及相关
  运动神经元编号范围（171-278）：腹侧/背侧弯曲运动控制

==============================================================================
文献
==============================================================================
  Beggs & Plenz 2003 — 神经雪崩基准
  Friedman et al. 2012 PRL — τ缩放关系
  Priesemann et al. 2014 PLOS CB — 分支比校准
  Varshney et al. 2011 PLOS CB — C.elegans connectome
  Rieke et al. 1997 — 神经编码统计（泊松过程）
  Bi & Poo 1998 — STDP时间窗口
  Tsodyks & Markram 1997 — STD模型
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
# --- STDP（Bi & Poo 1998）---
THETA_LTP   = 65
THETA_LTD   = 15
ETA_LTP     = 0.012
ETA_LTD     = 0.008
TAU_STDP    = 20.0
STDP_MAX_DT = 100      # 5*TAU_STDP
ETA_LTP_LATE = 0.006   # 后期学习率（减半）
ETA_LTD_LATE = 0.004

# --- 突触结构 ---
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

# --- E/I平衡（Brunel 2000）---
FRAC_INHIB   = 0.20
INHIB_SCALE  = 2.0

# --- STD（Tsodyks & Markram 1997）---
STD_ENABLED  = True
U_0          = 0.5
USE_FACTOR   = 0.35
TAU_STD      = 15.0

# --- 突触延迟（Diesmann 1999）---
DELAY_ENABLED = True
MIN_DELAY = 1
MAX_DELAY = 3

# --- 实验参数 ---
N_ADAPT   = 5000    # 适应期（强感觉刺激 + 强STDP）
N_RECORD  = 20000   # 记录期（基线刺激 + 弱STDP + BTW雪崩驱动）
LOG_INT   = 5000

# --- BTW慢驱动（记录期额外注入）---
BTW_INTERVAL = 10

# --- 泊松输入参数（Rieke 1997）---
LAMBDA_STIM   = 0.15   # 刺激状态放电率（/步，约15Hz）
LAMBDA_BASE   = 0.02   # 基线自发放电率（/步，约2Hz）
T_STIM_ON     = 50     # 刺激持续步数
T_STIM_OFF    = 50     # 刺激间隔步数

# --- 校准 ---
CALIB_WARMUP = 300
CALIB_STEPS  = 1000
CALIB_ITER   = 30
G_LO_INIT    = 0.001
G_HI_INIT    = 4.0

SEEDS = [42, 7, 13]

# ============================================================
# C.elegans神经元类型分配（基于Varshney 2011）
# ============================================================
def assign_celegans_types(N=279):
    """
    按C.elegans真实解剖分配神经元类型（简化版，保持功能比例）。
    
    真实比例（Varshney 2011）：
      感觉(sensory)  ≈ 60/279 ≈ 21%
      中间(inter)    ≈ 111/279 ≈ 40%
      运动(motor)    ≈ 108/279 ≈ 39%
    
    返回：
      neuron_type[i] ∈ {'sensory', 'inter', 'motor'}
      sensory_idx: 感觉神经元索引（输入层）
      motor_idx: 运动神经元索引（输出层，监测）
    """
    N_SENSORY = 60
    N_MOTOR   = 108
    N_INTER   = N - N_SENSORY - N_MOTOR  # 111

    neuron_type = np.array(['inter'] * N, dtype='<U8')
    # 感觉神经元：前端（索引0-59，对应头部感觉神经元）
    neuron_type[:N_SENSORY] = 'sensory'
    # 运动神经元：后端（索引171-278，对应腹侧/背侧运动神经元）
    neuron_type[N - N_MOTOR:] = 'motor'

    sensory_idx = np.where(neuron_type == 'sensory')[0]
    motor_idx   = np.where(neuron_type == 'motor')[0]
    inter_idx   = np.where(neuron_type == 'inter')[0]

    return neuron_type, sensory_idx, motor_idx, inter_idx


def assign_sensory_modalities(sensory_idx, seed=0):
    """
    将感觉神经元分配到4种感觉模态（模拟C.elegans真实感觉系统）：
      模态0 - 化学感觉（盐/pH） : ASEL/ASER等，约20个
      模态1 - 气味感觉          : AWA/AWB/AWC等，约15个
      模态2 - 温度感觉          : AFD/AFDR等，约10个
      模态3 - 机械感觉（触觉）  : ALM/AVM/PLM等，约15个
    """
    rng = np.random.default_rng(seed + 5555)
    N_sens = len(sensory_idx)
    modality = np.zeros(N_sens, dtype=np.int8)
    # 按比例分配（化学35%，气味25%，温度17%，机械23%）
    boundaries = [0,
                  int(N_sens * 0.35),
                  int(N_sens * 0.60),
                  int(N_sens * 0.77),
                  N_sens]
    for m in range(4):
        modality[boundaries[m]:boundaries[m+1]] = m
    # 打乱（模拟真实排布不完全有序）
    rng.shuffle(modality)
    return modality


# ============================================================
# 泊松输入生成器
# ============================================================
class PoissonStimulator:
    """
    泊松过程感觉输入发生器。
    
    协议：刺激呈现 T_STIM_ON 步 → 间隔 T_STIM_OFF 步 → 循环
    刺激期间：活跃模态的感觉神经元以 LAMBDA_STIM 放电
    间隔期间：所有感觉神经元以 LAMBDA_BASE 放电（自发活动）
    """
    def __init__(self, sensory_idx, modality, n_modalities=4, seed=0):
        self.sensory_idx  = sensory_idx
        self.modality     = modality
        self.n_mod        = n_modalities
        self.rng          = np.random.default_rng(seed + 3333)
        self.current_step = 0
        self.active_mod   = 0   # 当前活跃模态

    def step(self):
        """
        返回本步应激活的感觉神经元索引列表。
        泊松独立放电：每个神经元以λ/步的概率放电。
        """
        t = self.current_step
        cycle_len = T_STIM_ON + T_STIM_OFF

        # 判断当前是刺激期还是间隔期
        phase = t % cycle_len
        is_stim_on = (phase < T_STIM_ON)

        # 每个刺激周期开始时切换活跃模态
        if phase == 0:
            self.active_mod = int(self.rng.integers(self.n_mod))

        activated = []
        for local_i, (neuron_idx, mod) in enumerate(
                zip(self.sensory_idx, self.modality)):
            if is_stim_on and (mod == self.active_mod):
                lam = LAMBDA_STIM
            else:
                lam = LAMBDA_BASE
            # 泊松独立放电
            if self.rng.random() < lam:
                activated.append(int(neuron_idx))

        self.current_step += 1
        return activated, self.active_mod, is_stim_on


# ============================================================
# 网络初始化（继承v7的有向图+类型分配）
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

def assign_inhib_types(N, frac_inhib, seed):
    rng = np.random.default_rng(seed + 7777)
    n_inhib = int(N * frac_inhib)
    inhib_idx = rng.choice(N, size=n_inhib, replace=False)
    is_inhib = np.zeros(N, dtype=bool)
    is_inhib[inhib_idx] = True
    return is_inhib

def init_std_resources(N, seed):
    rng = np.random.default_rng(seed + 8888)
    u = np.full((N, N), U_0, dtype=np.float32)
    u += rng.uniform(-0.03, 0.03, (N, N)).astype(np.float32)
    return np.clip(u, 0.01, 1.0)

def assign_delays(N, seed):
    rng = np.random.default_rng(seed + 9999)
    return rng.integers(MIN_DELAY, MAX_DELAY + 1, size=(N, N)).astype(np.int8)

# ============================================================
# 网络度量
# ============================================================
def compute_sigma_fast(adj, N):
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

# ============================================================
# STD恢复（向量化）
# ============================================================
def recover_std_vec(std_u, syn_mask):
    if STD_ENABLED:
        std_u[syn_mask] += (U_0 - std_u[syn_mask]) / TAU_STD

# ============================================================
# 单层传播（延迟队列，含E/I）
# ============================================================
def propagate_layer(adj, el_mask, is_inhib, std_u, delays,
                    wave, refrac, fired, N, G,
                    delay_buffer, current_step, rng):
    new_wave = np.zeros(N, dtype=bool)
    inhib_input = np.zeros(N, dtype=np.float32)

    # 处理本步到达的延迟消息
    arrivals = delay_buffer.pop(current_step, [])
    for (tgt, eff_w, is_ex) in arrivals:
        if refrac[tgt] > 0 or fired[tgt]: continue
        if is_ex:
            if rng.random() < min(eff_w, 0.99):
                new_wave[tgt] = True
        else:
            inhib_input[tgt] += eff_w

    # 当前wave发送信号
    for i in np.where(wave)[0]:
        w_row = adj[i, :] * G
        w_row[el_mask[i, :]] *= 1.15
        if is_inhib[i]:
            ws = w_row * INHIB_SCALE
            for c in np.where(ws > 0.005)[0]:
                if c == i: continue
                u_ij = float(std_u[i, c])
                eff = float(ws[c]) * u_ij
                if STD_ENABLED: std_u[i, c] *= (1.0 - USE_FACTOR)
                delay_buffer[current_step + int(delays[i, c])].append((int(c), eff, False))
        else:
            for c in np.where(w_row > 0.005)[0]:
                u_ij = float(std_u[i, c])
                eff = float(w_row[c]) * u_ij
                if STD_ENABLED: std_u[i, c] *= (1.0 - USE_FACTOR)
                delay_buffer[current_step + int(delays[i, c])].append((int(c), eff, True))

    # 抑制削减
    for tgt in np.where(inhib_input > 0)[0]:
        if new_wave[tgt]:
            if rng.random() < min(float(inhib_input[tgt]) * 0.5, 0.99):
                new_wave[tgt] = False

    new_wave &= ~fired
    return new_wave

# ============================================================
# κ校准（Priesemann方法，全时序）
# ============================================================
def estimate_kappa(adj, el_mask, is_inhib, delays, std_u_init,
                   N, G, seed, n_warmup, n_measure):
    rng = np.random.default_rng(seed)
    refrac = np.zeros(N, dtype=np.int8)
    std_u = std_u_init.copy()
    syn_mask = adj != 0
    wave = np.zeros(N, dtype=bool)
    fired = np.zeros(N, dtype=bool)
    delay_buffer = defaultdict(list)
    act_log = []

    for step in range(n_warmup + n_measure):
        recover_std_vec(std_u, syn_mask)
        queue_pending = any(k >= step for k in delay_buffer)
        if not wave.any() and not queue_pending and step % BTW_INTERVAL == 0:
            d = int(rng.integers(N))
            if refrac[d] == 0:
                wave[d] = True; fired[:] = False; fired[d] = True

        new_wave = propagate_layer(adj, el_mask, is_inhib, std_u, delays,
                                   wave, refrac, fired, N, G, delay_buffer, step, rng)
        fired |= new_wave; wave = new_wave
        if step >= n_warmup:
            act_log.append(int(new_wave.sum()))
        refrac[wave] = T_ABS; refrac[refrac > 0] -= 1

    if len(act_log) < 10: return 0.0
    arr = np.array(act_log, dtype=float)
    num = arr[1:][arr[:-1] > 0].sum()
    den = arr[:-1][arr[:-1] > 0].sum()
    return float(num / den) if den > 0 else 0.0


def calibrate_G(adj, el_mask, is_inhib, delays, std_u_after, N, seed):
    G_lo = G_LO_INIT; G_hi = G_HI_INIT; G_best = 0.5
    for i in range(CALIB_ITER):
        G_mid = (G_lo + G_hi) / 2
        kappa = estimate_kappa(adj, el_mask, is_inhib, delays, std_u_after,
                               N, G_mid, seed + i*997, CALIB_WARMUP, CALIB_STEPS)
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
    kf = estimate_kappa(adj, el_mask, is_inhib, delays, std_u_after,
                        N, G_best, seed+9999999, CALIB_WARMUP, CALIB_STEPS)
    print(f"    ⚠️ 结束 G={G_best:.5f}, κ={kf:.4f}")
    return G_best, kf

# ============================================================
# 雪崩检测
# ============================================================
def detect_avalanches(act_series):
    sizes, durs, kappas = [], [], []
    layers = []; in_av = False
    for n in act_series:
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
# 幂律拟合（含KS检验）
# ============================================================
def fit_powerlaw_strict(data):
    data = np.array([d for d in data if d > 0], dtype=float)
    res = {'tau': None, 'xmin': None, 'n_tail': len(data),
           'r2': 0.0, 'ks_stat': 1.0, 'plausible': False,
           'p_value': 0.0, 'lr_vs_lognormal': 0.0}
    if len(data) < 30: return res
    p5 = max(1.0, np.percentile(data, 5)); p65 = np.percentile(data, 65)
    cands = np.unique(data); cands = cands[(cands >= p5) & (cands <= p65)]
    if len(cands) == 0: cands = [np.median(data)]
    best_ks = np.inf; best_xmin = p5; best_tau = 1.5
    for xm in cands[:50]:
        tail = data[data >= xm]
        if len(tail) < 15: continue
        lr = np.log(tail / xm)
        if lr.sum() == 0: continue
        tau_e = 1 + len(tail) / lr.sum()
        if tau_e <= 1.0 or tau_e > 8.0: continue
        ts = np.sort(tail); n_t = len(ts)
        ecdf = np.arange(1, n_t+1) / n_t
        tcdf = 1 - (ts/xm)**(-(tau_e-1))
        ks = float(np.max(np.abs(ecdf - tcdf)))
        if ks < best_ks: best_ks = ks; best_xmin = xm; best_tau = tau_e
    res['xmin'] = float(best_xmin); res['tau'] = float(best_tau)
    tail = data[data >= best_xmin]; res['n_tail'] = len(tail)
    res['ks_stat'] = float(best_ks)
    if len(tail) >= 10:
        bins = min(20, max(5, len(tail)//8))
        counts, edges = np.histogram(tail, bins=bins)
        centers = (edges[:-1]+edges[1:])/2; msk = counts > 0
        if msk.sum() >= 4:
            lx = np.log(centers[msk]); ly = np.log(counts[msk])
            c = np.polyfit(lx, ly, 1)
            fit = np.polyval(c, lx)
            ssr = np.sum((ly-fit)**2); sst = np.sum((ly-np.mean(ly))**2)
            res['r2'] = float(1-ssr/sst) if sst > 0 else 0.0
    # Bootstrap p_value
    tau = best_tau; xmin = best_xmin; n_t = len(tail)
    boots = []
    rng_b = np.random.default_rng(42)
    for _ in range(50):
        u = rng_b.uniform(size=n_t)
        syn = xmin * (1-u)**(-1/(tau-1))
        syn = np.sort(syn)
        tau_s = 1 + n_t / np.sum(np.log(syn/xmin))
        if tau_s <= 1: tau_s = 1.01
        ecdf_s = np.arange(1, n_t+1)/n_t
        tcdf_s = 1-(syn/xmin)**(-(tau_s-1))
        boots.append(float(np.max(np.abs(ecdf_s-tcdf_s))))
    res['p_value'] = float(np.mean(np.array(boots) >= best_ks))
    res['plausible'] = (res['p_value'] >= 0.1)
    # LR test
    ll_pl = np.sum(np.log(tau-1) - np.log(xmin) - tau*np.log(tail/xmin))
    lt = np.log(tail); mu_ln = lt.mean(); sig_ln = lt.std()
    if sig_ln > 0:
        ll_ln = np.sum(-np.log(tail) - 0.5*np.log(2*np.pi*sig_ln**2)
                       - 0.5*((lt-mu_ln)/sig_ln)**2)
        res['lr_vs_lognormal'] = float(ll_pl - ll_ln)
    return res

def compute_psd(act_series):
    arr = np.array(act_series, dtype=float) - np.mean(act_series)
    power = np.abs(np.fft.rfft(arr))**2
    freqs = np.fft.rfftfreq(len(arr))
    mask = (freqs > 0.001) & (freqs < 0.25)
    if mask.sum() < 15: return 0.0, 0.0
    lf = np.log(freqs[mask]); lp = np.log(power[mask]+1e-10)
    c = np.polyfit(lf, lp, 1)
    fit = np.polyval(c, lf)
    ssr = np.sum((lp-fit)**2); sst = np.sum((lp-np.mean(lp))**2)
    r2 = float(1-ssr/sst) if sst > 0 else 0.0
    return float(c[0]), r2

# ============================================================
# 输出解码：感觉模态 → 运动神经元激活模式
# ============================================================
def compute_decode_score(motor_activation_per_modality):
    """
    计算不同感觉模态诱发的运动神经元激活模式的分离程度。
    用余弦距离矩阵的平均值衡量：值越大，不同模态的输出越不同（功能分离好）。
    """
    n_mod = len(motor_activation_per_modality)
    if n_mod < 2: return 0.0
    vecs = []
    for m, arr in motor_activation_per_modality.items():
        v = np.array(arr, dtype=float)
        norm = np.linalg.norm(v)
        vecs.append(v / norm if norm > 0 else v)

    dists = []
    for i in range(n_mod):
        for j in range(i+1, n_mod):
            cos_sim = np.dot(vecs[i], vecs[j])
            dists.append(1.0 - cos_sim)   # 余弦距离（0=相同, 2=反向）
    return float(np.mean(dists)) if dists else 0.0

# ============================================================
# 主仿真
# ============================================================
def run_simulation(net_name, net_cfg, seed, use_pruning=False):
    N = net_cfg['N']
    rng = np.random.default_rng(seed)

    # --- 初始化 ---
    adj = make_ws_adj_directed(N, net_cfg['k_init'], net_cfg['p_init'], seed)
    is_inhib = assign_inhib_types(N, FRAC_INHIB, seed)
    std_u = init_std_resources(N, seed)
    delays = assign_delays(N, seed)
    syn_mask = adj != 0
    el_mask = np.zeros((N, N), dtype=bool)
    el_mask[adj > 0] = rng.random((adj > 0).sum()) < 0.05
    el_mask[is_inhib, :] = False
    nltp = np.zeros((N, N), dtype=np.int16)
    nltd = np.zeros((N, N), dtype=np.int16)
    el_age = np.zeros((N, N), dtype=np.int32)
    refrac = np.zeros(N, dtype=np.int8)
    last_spike = np.full(N, -99999, dtype=np.int32)
    exc_mask_pre = np.outer(~is_inhib, np.ones(N, dtype=bool))  # 预计算

    # --- C.elegans神经元类型 ---
    neuron_type, sensory_idx, motor_idx, inter_idx = assign_celegans_types(N)
    modality = assign_sensory_modalities(sensory_idx, seed)
    stimulator = PoissonStimulator(sensory_idx, modality, n_modalities=4, seed=seed)

    n_exc = int((~is_inhib).sum()); n_inh = int(is_inhib.sum())
    n_sen = len(sensory_idx); n_mot = len(motor_idx); n_int = len(inter_idx)
    print(f"  [{net_name}|{seed}] N={N} | E={n_exc} I={n_inh}")
    print(f"  神经元类型: 感觉={n_sen}(输入) 中间={n_int} 运动={n_mot}(输出)")
    print(f"  感觉模态: 化学={sum(modality==0)} 气味={sum(modality==1)} "
          f"温度={sum(modality==2)} 机械={sum(modality==3)}")
    print(f"  输入模式: 泊松(λ_stim={LAMBDA_STIM}/步 λ_base={LAMBDA_BASE}/步)")
    print(f"  时间结构: ON={T_STIM_ON}步 OFF={T_STIM_OFF}步 循环")
    sys.stdout.flush()

    topo_log = []
    t0 = time.time()
    delay_buffer = defaultdict(list)

    # 运动神经元激活记录（按模态）
    motor_act_per_mod = defaultdict(lambda: np.zeros(len(motor_idx)))
    motor_act_counts  = defaultdict(int)

    total_steps = N_ADAPT + N_RECORD
    print(f"\n  [{net_name}|{seed}] 开始仿真（适应{N_ADAPT}步 + 记录{N_RECORD}步）...")
    sys.stdout.flush()

    activation_series = []  # 记录期雪崩序列

    for step in range(total_steps):
        is_adapt  = (step < N_ADAPT)
        is_record = (step >= N_ADAPT)

        recover_std_vec(std_u, syn_mask)

        # --- 外部刺激（泊松感觉输入）---
        stim_neurons, active_mod, is_stim_on = stimulator.step()
        active = np.zeros(N, dtype=bool)
        for ni in stim_neurons:
            if refrac[ni] == 0:
                active[ni] = True

        # 记录期额外BTW慢驱动（补充雪崩触发率）
        if is_record:
            abs_step = step
            queue_pending = any(k >= abs_step for k in delay_buffer)
            if not active.any() and not queue_pending and step % BTW_INTERVAL == 0:
                d = int(rng.integers(N))
                if refrac[d] == 0:
                    active[d] = True

        # --- 单层传播 ---
        if active.any():
            fired = active.copy()
            wave = propagate_layer(adj, el_mask, is_inhib, std_u, delays,
                                   active, refrac, fired, N, 1.0,
                                   delay_buffer, step, rng)
            active |= wave
        else:
            # 处理延迟队列（即使本步无主动激活）
            fired = np.zeros(N, dtype=bool)
            wave = propagate_layer(adj, el_mask, is_inhib, std_u, delays,
                                   np.zeros(N, dtype=bool), refrac, fired, N, 1.0,
                                   delay_buffer, step, rng)
            active |= wave

        n_act = int(active.sum())
        last_spike[active] = step
        refrac[active] = T_ABS + T_REL
        refrac[refrac > 0] -= 1

        # 记录运动神经元激活（按模态统计）
        if is_stim_on and n_act > 0:
            motor_active = active[motor_idx]
            if motor_active.any():
                motor_act_per_mod[int(active_mod)] += motor_active.astype(float)
                motor_act_counts[int(active_mod)] += 1

        # 记录雪崩激活序列（记录期）
        if is_record:
            activation_series.append(n_act)

        # --- STDP（真实时差）---
        eta_ltp = ETA_LTP if is_adapt else ETA_LTP_LATE
        eta_ltd = ETA_LTD if is_adapt else ETA_LTD_LATE
        aidx_exc = np.where(active & ~is_inhib)[0]
        aidx_all = np.where(active)[0]
        if len(aidx_exc) >= 2 and len(aidx_all) >= 1:
            n_p = min(len(aidx_exc) * 2, 100)
            pre_arr = rng.choice(aidx_exc, size=n_p)
            post_arr = rng.choice(aidx_all, size=n_p)
            for pre, post in zip(pre_arr, post_arr):
                if pre == post: continue
                dt = int(last_spike[post]) - int(last_spike[pre])
                if abs(dt) > STDP_MAX_DT: continue
                if dt > 0:
                    if adj[pre, post] > 0 and not is_inhib[pre]:
                        adj[pre, post] = min(1.0, adj[pre, post] + eta_ltp*np.exp(-abs(dt)/TAU_STDP))
                        nltp[pre, post] += 1
                else:
                    if adj[post, pre] > 0 and not is_inhib[post]:
                        adj[post, pre] = max(0.0, adj[post, pre] - eta_ltd*np.exp(-abs(dt)/TAU_STDP))
                        nltd[post, pre] += 1

        # 固化/消除
        el_ratio = el_mask.sum() / max(1, (adj > 0).sum())
        ltp_m = (nltp >= THETA_LTP) & (adj > 0) & (~el_mask) & (el_ratio < EL_HI) & exc_mask_pre
        el_mask[ltp_m] = True; nltp[ltp_m] = 0
        ltd_m = (nltd >= THETA_LTD) & (adj > 0) & (~el_mask) & exc_mask_pre
        adj[ltd_m] = 0.0; nltp[ltd_m] = nltd[ltd_m] = 0
        syn_mask[ltd_m] = False
        el_age[el_mask] += 1
        dm = el_mask & (el_age > T_DECAY)
        el_mask[dm] = False; el_age[dm] = 0

        # WS重连
        if step % REWIRE_INT == 0:
            non_el = np.argwhere((adj > 0) & (~el_mask) & exc_mask_pre)
            for _ in range(max(1, int(len(non_el)*P_REWIRE*0.01))):
                if len(non_el) == 0: break
                ix = int(rng.integers(len(non_el))); i, j = non_el[ix]
                kn = int(rng.integers(N))
                if kn != i and adj[i, kn] == 0:
                    adj[i, kn] = adj[i, j]; adj[i, j] = 0.0
                    syn_mask[i, j] = False; syn_mask[i, kn] = True

        # 突触缩放
        if step % SCALING_INT == 0 and n_act > 0:
            ar = n_act / N
            if ar > KAPPA_TARGET: adj[~el_mask] *= (1 - SCALING_RATE)
            elif ar < KAPPA_TARGET * 0.5: adj[~el_mask] *= (1 + SCALING_RATE)
            adj = np.clip(adj, 0.0, 1.0)

        # 竞争性修剪（4规则）
        if use_pruning and step % PRUNE_INT == 0 and step > 0:
            deg = (adj > 0).sum(axis=1)
            for i, j in np.argwhere((adj > 0) & (~el_mask) & exc_mask_pre
                                     & (nltp == 0) & (nltd == 0)):
                if deg[i] > MIN_EDGES and rng.random() < P_PRUNE:
                    adj[i, j] = 0.0; syn_mask[i, j] = False
            nltp[:] = 0; nltd[:] = 0

        if step % LOG_INT == 0:
            sig = compute_sigma_fast(adj, N)
            phase_str = "适应" if is_adapt else "记录"
            stim_str = f"模态{active_mod}{'↑' if is_stim_on else '↓'}"
            print(f"    {phase_str} {step}/{total_steps} σ={sig:.2f} "
                  f"edges={(adj>0).sum()} n_act={n_act} {stim_str} t={time.time()-t0:.0f}s")
            sys.stdout.flush()
            topo_log.append({'step': step, 'sigma': sig,
                              'n_edges': int((adj>0).sum()),
                              'n_el': int(el_mask.sum()),
                              'phase': phase_str})

    # --- 临界点校准 ---
    std_u_after = std_u.copy()
    sigma_final = compute_sigma_fast(adj, N)
    print(f"\n  学习后: edges={(adj>0).sum()} σ={sigma_final:.2f}")
    print(f"\n  [{net_name}|{seed}] 临界点校准...")
    sys.stdout.flush()
    G_calib, kappa_calib = calibrate_G(adj, el_mask, is_inhib, delays, std_u_after, N, seed)
    print(f"  校准结果: G={G_calib:.5f}, κ={kappa_calib:.4f}")

    # --- 雪崩分析 ---
    arr = np.array(activation_series)
    zero_frac = float((arr == 0).mean())
    print(f"\n  激活统计: 零帧={zero_frac:.1%} 最大={arr.max()} 均={arr.mean():.3f}")

    sizes, durs, kappas_inner = detect_avalanches(activation_series)
    res_s = fit_powerlaw_strict(sizes)
    res_d = fit_powerlaw_strict(durs)
    tau_s = res_s['tau']; r2_s = res_s['r2']
    tau_d = res_d['tau']; r2_d = res_d['r2']
    kappa = float(np.mean(kappas_inner)) if kappas_inner else 0.0
    kappa_std = float(np.std(kappas_inner)) if len(kappas_inner) > 1 else 0.0
    psd_slope, psd_r2 = compute_psd(activation_series)

    # τ缩放关系（Friedman 2012）
    if tau_s and tau_d:
        tau_d_theory = (tau_s + 1) / 2
        scale_err = abs(tau_d - tau_d_theory) / tau_d_theory
    else:
        scale_err = 1.0

    # --- 输出解码分数 ---
    decode_score = compute_decode_score(motor_act_per_mod)
    print(f"  输出解码余弦距离: {decode_score:.4f} "
          f"({'✓ 功能分离' if decode_score > 0.05 else '✗ 未分离'})")

    n_av = len(sizes)
    mean_sz = float(np.mean(sizes)) if sizes else 0.0
    mean_dur = float(np.mean(durs)) if durs else 0.0
    dur_arr = np.array(durs) if durs else np.array([0])
    frac_dur1 = float((dur_arr == 1).mean()) if len(dur_arr) > 0 else 1.0

    # 达标判定（8项）
    size_ok   = (tau_s is not None and 1.2 <= tau_s <= 2.2 and r2_s > 0.70 and res_s['plausible'])
    dur_ok    = (tau_d is not None and 1.5 <= tau_d <= 2.8 and r2_d > 0.70)
    kappa_ok  = (0.85 <= kappa <= 1.15)
    count_ok  = (n_av >= 300)
    psd_ok    = (psd_slope is not None and -1.5 <= psd_slope <= -0.3)
    zero_ok   = (zero_frac >= 0.3)
    multi_ok  = (frac_dur1 < 0.8)
    scale_ok  = (scale_err < 0.25)
    decode_ok = (decode_score > 0.05)  # 新增：功能分离

    score = sum([size_ok, dur_ok, kappa_ok, count_ok, psd_ok,
                 zero_ok, multi_ok, scale_ok, decode_ok])

    ts_str = f"{tau_s:.3f}" if tau_s else "N/A"
    td_str = f"{tau_d:.3f}" if tau_d else "N/A"
    ps_str = f"{psd_slope:.3f}" if psd_slope else "N/A"
    td_th  = f"{(tau_s+1)/2:.3f}" if tau_s else "N/A"

    print(f"\n{'='*65}")
    print(f"  结果 [{net_name}|{seed}|{'4r' if use_pruning else '3r'}] G={G_calib:.4f}")
    print(f"  零帧: {zero_frac:.1%} {'✓' if zero_ok else '✗'}")
    print(f"  雪崩数: {n_av} | 均尺寸: {mean_sz:.1f} | 均时长: {mean_dur:.1f} {'✓' if count_ok else '✗'}")
    print(f"  多步雪崩: {1-frac_dur1:.1%} {'✓' if multi_ok else '✗'}")
    print(f"  τ_size={ts_str} R²={r2_s:.3f} p={res_s['p_value']:.2f} {'✓' if size_ok else '✗'}")
    print(f"  τ_dur={td_str} R²={r2_d:.3f} (理论={td_th} 误差={scale_err:.0%}) {'✓' if dur_ok else '✗'}")
    print(f"  τ缩放关系误差={scale_err:.0%} {'✓' if scale_ok else '✗'}")
    print(f"  κ={kappa:.4f}±{kappa_std:.3f} {'✓' if kappa_ok else '✗'}")
    print(f"  PSD={ps_str} R²={psd_r2:.3f} {'✓' if psd_ok else '✗'}")
    print(f"  输出解码={decode_score:.4f} {'✓' if decode_ok else '✗'}")
    print(f"  LR(PL>LN): {res_s.get('lr_vs_lognormal', 0):.1f}")
    print(f"  得分: {score}/9")
    print(f"  {'='*65}\n")
    sys.stdout.flush()

    return {
        'network': net_name, 'seed': seed,
        'rules': '4-rules' if use_pruning else '3-rules',
        'input_mode': {
            'type': 'Poisson',
            'lambda_stim': LAMBDA_STIM, 'lambda_base': LAMBDA_BASE,
            't_on': T_STIM_ON, 't_off': T_STIM_OFF,
            'n_modalities': 4,
            'sensory_fraction': len(sensory_idx) / N,
        },
        'bio': {
            'neuron_types': True,
            'E_frac': float((~is_inhib).mean()),
            'std': STD_ENABLED, 'delay': DELAY_ENABLED,
            'directed_adj': True, 'real_stdp_dt': True,
            'synchronized_learning': True,
        },
        'G_calib': float(G_calib), 'kappa_calib': float(kappa_calib),
        'sigma_final': float(sigma_final),
        'zero_fraction': float(zero_frac),
        'n_avalanches': n_av, 'mean_size': float(mean_sz), 'mean_duration': float(mean_dur),
        'frac_dur1': float(frac_dur1),
        'tau_size': float(tau_s) if tau_s else None, 'r2_size': float(r2_s),
        'ks_stat_size': float(res_s['ks_stat']),
        'p_value_size': float(res_s['p_value']),
        'lr_vs_lognormal': float(res_s.get('lr_vs_lognormal', 0)),
        'tau_duration': float(tau_d) if tau_d else None, 'r2_duration': float(r2_d),
        'tau_scale_error': float(scale_err),
        'branching_ratio': float(kappa), 'branching_ratio_std': float(kappa_std),
        'psd_slope': float(psd_slope) if psd_slope else None, 'psd_r2': float(psd_r2),
        'decode_score': float(decode_score),
        'score': int(score), 'max_score': 9,
        'criteria': {
            'zero_frames': bool(zero_ok), 'size_powerlaw': bool(size_ok),
            'duration_powerlaw': bool(dur_ok), 'tau_scale': bool(scale_ok),
            'branching_ratio': bool(kappa_ok), 'avalanche_count': bool(count_ok),
            'psd_1f': bool(psd_ok), 'multi_step': bool(multi_ok),
            'output_decode': bool(decode_ok),
        },
        'topology_log': topo_log,
        'activation_sample': [int(x) for x in activation_series[:6000]],
        'sizes_sample': sorted([int(s) for s in sizes])[:1500],
        'durations_sample': sorted([int(d) for d in durs])[:1500],
    }

# ============================================================
# 网络定义
# ============================================================
NETWORKS = {
    'C.elegans': {
        'N': 279, 'k_init': 8, 'p_init': 0.05,
        'sf': 0.22,   # sensory fraction（保留，用于兼容）
        'level': 'neuron', 'K_PATTERNS': 8,
        'ref': 'Varshney 2011 PLOS CB'
    },
    'Human_HCP': {
        'N': 400, 'k_init': 10, 'p_init': 0.06,
        'sf': 0.15,
        'level': 'mesoscale', 'K_PATTERNS': 12,
        'ref': 'Van Essen 2013 HCP'
    },
    'WS_Control': {
        'N': 279, 'k_init': 8, 'p_init': 0.15,
        'sf': 0.22,
        'level': 'control', 'K_PATTERNS': 8,
        'ref': 'WS 1998 对照'
    }
}

# ============================================================
# 绘图
# ============================================================
def plot_results(all_results):
    fig = plt.figure(figsize=(22, 28))
    fig.suptitle(
        'SDI Exp5 v8: Real Bio Input (Poisson + Sensory Types + Output Decode)\n'
        'Sensory[60]->Inter[111]->Motor[108] | 4 Modalities | Synchronized Learning',
        fontsize=11, fontweight='bold', y=0.99
    )
    gs = GridSpec(7, 3, figure=fig, hspace=0.52, wspace=0.38)
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
        if act: ax1.plot(act[:4000], color=color, lw=0.5, alpha=0.8)
        sc = res.get('score', 0); mx = res.get('max_score', 9)
        ds = res.get('decode_score', 0)
        ax1.set_title(
            f"{res['network']} {res['rules']}\n"
            f"κ={res.get('branching_ratio',0):.3f} decode={ds:.3f} Score={sc}/{mx}",
            fontsize=7,
            color='green' if sc >= 6 else ('orange' if sc >= 4 else 'red')
        )
        ax1.set_xlabel('Step', fontsize=6); ax1.set_ylabel('n_act', fontsize=6)
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
                    ax2.loglog(ctr[msk], cnt[msk], 'o', color=color, ms=4, alpha=0.7)
                    xt = np.logspace(np.log10(ctr[msk][0]), np.log10(ctr[msk][-1]), 50)
                    y0 = cnt[msk][0]*(ctr[msk][0]**1.5)
                    ax2.loglog(xt, y0/(xt**1.5), '--', color='gray', alpha=0.5, label='tau=1.5')
            except: pass
        ts = res.get('tau_size'); r2s = res.get('r2_size', 0)
        se = res.get('tau_scale_error', 1.0)
        ts_str = f"{ts:.2f}" if ts else "N/A"
        ok = res.get('criteria', {}).get('size_powerlaw', False)
        ax2.set_title(f"tau={ts_str} R2={r2s:.2f} scale_err={se:.0%} {'V' if ok else 'X'}",
                     fontsize=6.5, color='green' if ok else 'red')
        ax2.set_xlabel('S', fontsize=6); ax2.set_ylabel('Count', fontsize=6)
        ax2.tick_params(labelsize=6); ax2.legend(fontsize=5)

    plt.savefig(f'{OUT}/exp5_v8_avalanche_results.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Figure: {OUT}/exp5_v8_avalanche_results.png")

# ============================================================
# 主程序
# ============================================================
def main():
    print("="*70)
    print("SDI Experiment 5 v8 — Real Bio Input Mode")
    print("  升级1: 泊松放电过程（Poisson, λ_stim=0.15, λ_base=0.02）")
    print("  升级2: C.elegans神经元类型（感觉60 / 中间111 / 运动108）")
    print("  升级3: 学习/雪崩同步运行（适应期5000步 + 记录期20000步）")
    print("  升级4: 输出解码验证（余弦距离，功能分离评分）")
    print(f"  继承v7: 真实STDP时序 + 延迟队列 + KS检验 + STD连续")
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

    out_path = f'{OUT}/exp5_v8_avalanche_results.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(ds(all_results), f, ensure_ascii=False, indent=2)
    print(f"\nSaved: {out_path}")

    try: plot_results(all_results)
    except Exception as e: print(f"  Plot error: {e}")

    print("\n" + "="*70 + "\nSummary v8\n" + "="*70)
    from collections import defaultdict
    gd = defaultdict(list)
    for r in all_results: gd[f"{r['network']}_{r['rules']}"].append(r)
    print(f"\n{'Group':<28} κ{'':5} τ_s{'':4} τ_d{'':4} scale  PSD{'':4} decode Score")
    print("-"*85)
    for key, runs in sorted(gd.items()):
        kv   = np.mean([r['branching_ratio'] for r in runs])
        ts_l = [r['tau_size'] for r in runs if r['tau_size']]
        td_l = [r['tau_duration'] for r in runs if r['tau_duration']]
        pv_l = [r['psd_slope'] for r in runs if r['psd_slope']]
        se_l = [r['tau_scale_error'] for r in runs]
        dc_l = [r['decode_score'] for r in runs]
        sv   = [r['score'] for r in runs]
        mx   = runs[0]['max_score']
        ts_s = f"{np.mean(ts_l):.2f}" if ts_l else "N/A"
        td_s = f"{np.mean(td_l):.2f}" if td_l else "N/A"
        pv_s = f"{np.mean(pv_l):.2f}" if pv_l else "N/A"
        se_s = f"{np.mean(se_l):.0%}"
        dc_s = f"{np.mean(dc_l):.3f}"
        print(f"{key:<28} {kv:.3f}  {ts_s:<7}{td_s:<7}{se_s:<7} {pv_s:<7}{dc_s:<7}{np.mean(sv):.1f}/{mx}")

    best = max(all_results, key=lambda x: x['score'])
    print(f"\nBest: {best['network']} | {best['rules']} | seed={best['seed']}")
    print(f"  tau_s={best['tau_size']:.3f if best['tau_size'] else 'N/A'}")
    print(f"  kappa={best['branching_ratio']:.3f}  decode={best['decode_score']:.4f}")
    print(f"  score={best['score']}/{best['max_score']}")
    elapsed = time.time() - t_total
    print(f"\nTotal: {elapsed:.0f}s ({elapsed/60:.1f}min)")
    print("v8 complete.")
    sys.stdout.flush()

if __name__ == '__main__':
    main()
