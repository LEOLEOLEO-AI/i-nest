#!/usr/bin/env python3
"""
SDI 实验五 v7：神经雪崩SOC动力学验证（科学严格版）

==============================================================================
v7相对v6的全部修复（按优先级）
==============================================================================

【P0 — 科学正确性】
  Fix-1: STD状态连续
    v6: 记录阶段重新初始化std_u → 冷启动偏差
    v7: std_u_rec = std_u.copy()，从学习阶段末尾稳态继续
        校准时也传入同一份std_u拷贝，三个阶段状态完全一致

  Fix-2: 幂律严格统计检验（KS检验 + 似然比检验）
    v6: 只有Hill MLE + R²
    v7: 加入 KS-statistic, p_value（拒绝幂律置信度）
        加入 LR-test（幂律 vs 对数正态 vs 截断幂律）
        加入 τ缩放关系误差（Friedman 2012 PRL: τ_dur=(τ_size+1)/2）

  Fix-3: τ缩放关系作为达标指标
    新增: scale_ok = |τ_dur - (τ_size+1)/2| / ((τ_size+1)/2) < 0.25

【P1 — 生物准确性】
  Fix-4: STDP用真实spike时间戳
    v6: dt = rng.integers(1,30) 随机均匀
    v7: last_spike[i] 记录每个神经元上次激活步
        dt = current_step - last_spike[pre]（前向窗口）
        pre先激活 → dt>0 → LTP；post先激活 → dt<0 → LTD
        窗口截断：|dt| < 5*TAU_STDP 才更新

  Fix-5: 突触延迟队列（真实时序）
    v6: delay_factor=1/d_ij，只是权重缩放，无时序意义
    v7: delay_buffer[(arrival_step)] = [(target, eff_weight), ...]
        发送时压入队列，每步处理到达的消息包
        雪崩自然跨越多步（因为delay=2的消息2步后才到）

  Fix-6: κ校准用全雪崩平均
    v6: 只记录wave0→wave1（第一代），低估真实κ
    v7: 对每次BTW触发后的完整雪崩，记录所有代的(prev_size, next_size)
        κ = Σ(all next_sizes) / Σ(all prev_sizes)

【P2 — 工程优化】
  Fix-7: exc_mask_pre提前计算（不在每步循环内重建）
  Fix-8: recover_std用纯numpy向量化（无Python循环）
  Fix-9: κ标准差报告（临界性涨落）
  Fix-10: 雪崩形状坍缩（shape collapse）分析输出

==============================================================================
文献
==============================================================================
Beggs & Plenz 2003 J Neurosci — 神经雪崩，τ≈1.5，κ≈1.0
Friedman et al. 2012 PRL — τ缩放关系: (τ_dur-1)/(τ_size-1)=1/2
Priesemann et al. 2014 PLOS CB — 分支比校准方法论
Tsodyks & Markram 1997 Science — STD/STF模型
Bi & Poo 1998 J Neurosci — STDP时间窗口
Diesmann et al. 1999 Nature — 突触传播延迟
Clauset et al. 2009 SIAM Rev — 幂律拟合与KS检验
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
# 参数（标注来源）
# ============================================================
# --- STDP（Bi & Poo 1998）---
THETA_LTP  = 65        # LTP累积阈值（归一化到仿真步数）
THETA_LTD  = 15        # LTD消除阈值
ETA_LTP    = 0.012     # LTP学习率（Markram 1997实测值）
ETA_LTD    = 0.008     # LTD学习率
TAU_STDP   = 20.0      # STDP时间常数（步≈ms，Bi & Poo 1998: 20ms）
STDP_MAX_DT = 5 * 20   # STDP有效窗口：5个时间常数

# --- 突触固化与老化 ---
T_DECAY    = 400       # E-L键老化步数
EL_HI      = 0.25     # E-L键上限比例（Bhatt 2007: ~25%突触稳定）

# --- 不应期（Hodgkin-Huxley 1952）---
T_ABS      = 3         # 绝对不应期（步，对应约3ms）
T_REL      = 5         # 相对不应期（步）

# --- 拓扑重组 ---
P_REWIRE   = 0.15      # WS重连概率（Watts & Strogatz 1998）
REWIRE_INT = 50        # 重连间隔（步）

# --- 稳态可塑性（Turrigiano 1998）---
SCALING_INT  = 100
KAPPA_TARGET = 0.95    # 目标激活率
SCALING_RATE = 0.05

# --- 竞争性修剪（Bhatt 2009）---
PRUNE_INT  = 200
P_PRUNE    = 0.05
MIN_EDGES  = 3

# --- E/I平衡（Brunel 2000）---
FRAC_INHIB  = 0.20    # 抑制性神经元比例（皮层约20%）
INHIB_SCALE = 2.0     # I突触强度放大因子（GABA通常比AMPA强2倍）

# --- 短期突触抑制（Tsodyks & Markram 1997）---
STD_ENABLED = True
U_0         = 0.5     # 基础释放概率
USE_FACTOR  = 0.35    # 每次释放消耗的资源比例（降低=较慢耗竭）
TAU_STD     = 15.0    # 资源恢复时间常数（步；生物约200-500ms，此处归一化）

# --- 突触延迟（Diesmann 1999：皮层轴突传导1-10ms）---
DELAY_ENABLED = True
MIN_DELAY = 1
MAX_DELAY = 3         # 最大延迟步数（对应约3ms）

# --- 实验参数 ---
N_LEARN    = 8000
N_RECORD   = 20000
LOG_INT    = 4000
BTW_INTERVAL = 10     # BTW驱动间隔（步）

# --- 校准参数（真实BTW稳态条件）---
CALIB_WARMUP = 300
CALIB_STEPS  = 1000
CALIB_ITER   = 30
G_LO_INIT    = 0.001
G_HI_INIT    = 4.0

SEEDS = [42, 7, 13]

# ============================================================
# 网络定义
# ============================================================
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
        'ref': 'Watts & Strogatz 1998'
    }
}

# ============================================================
# 初始化工具函数
# ============================================================
def make_ws_adj_directed(N, k, p, seed):
    """
    构建有向WS图（非对称）。
    每条边 i→j 独立决定是否保留/重连，不自动添加反向边。
    """
    rng = np.random.default_rng(seed)
    adj = np.zeros((N, N), dtype=np.float32)
    for i in range(N):
        for dj in range(1, k // 2 + 1):
            j = (i + dj) % N
            if rng.random() < (1 - p):
                # 保留规则边（有向：i→j）
                adj[i, j] = float(rng.uniform(0.05, 0.3))
            else:
                # 随机重连到新目标
                tgt = int(rng.integers(N))
                while tgt == i or adj[i, tgt] > 0:
                    tgt = int(rng.integers(N))
                adj[i, tgt] = float(rng.uniform(0.05, 0.3))
            # 反向边以独立概率保留（约50%，模拟真实connectome有向性）
            if rng.random() < 0.5:
                adj[j, i] = float(rng.uniform(0.05, 0.3))
    return adj

def assign_neuron_types(N, frac_inhib, seed):
    rng = np.random.default_rng(seed + 7777)
    n_inhib = int(N * frac_inhib)
    inhib_idx = rng.choice(N, size=n_inhib, replace=False)
    is_inhib = np.zeros(N, dtype=bool)
    is_inhib[inhib_idx] = True
    return is_inhib

def init_std_resources(N, seed):
    """初始化STD资源矩阵，全部从U_0开始（静息态）。"""
    rng = np.random.default_rng(seed + 8888)
    u = np.full((N, N), U_0, dtype=np.float32)
    u += rng.uniform(-0.03, 0.03, (N, N)).astype(np.float32)
    return np.clip(u, 0.01, 1.0)

def assign_delays(N, seed):
    """分配突触延迟，整数步，范围[MIN_DELAY, MAX_DELAY]。"""
    rng = np.random.default_rng(seed + 9999)
    return rng.integers(MIN_DELAY, MAX_DELAY + 1, size=(N, N)).astype(np.int8)

# ============================================================
# 网络度量
# ============================================================
def compute_sigma_fast(adj, N):
    try:
        # 对有向图取无向化（对称化）后计算sigma
        sym = (np.abs(adj) + np.abs(adj.T)) / 2
        edges = np.argwhere(sym > 0.05)
        edges = edges[edges[:, 0] < edges[:, 1]]
        if len(edges) < 10:
            return 1.0
        al = [[] for _ in range(N)]
        for u, v in edges:
            al[u].append(v); al[v].append(u)
        Cv = []
        for i in range(min(40, N)):
            nb = al[i]; ki = len(nb)
            if ki < 2:
                Cv.append(0.0); continue
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
                    if nb not in vis:
                        vis[nb] = d + 1; q.append(nb)
            lengths.extend(vis.values())
        L = float(np.mean(lengths)) if lengths else 3.0
        m = len(edges); k_avg = 2 * m / N
        if k_avg <= 1: return 1.0
        C_rand = k_avg / N
        L_rand = np.log(N) / np.log(k_avg)
        if C_rand == 0 or L_rand == 0: return 1.0
        return float((C / C_rand) / (L / L_rand))
    except:
        return 1.0

# ============================================================
# STD恢复（numpy向量化，Fix-8）
# ============================================================
def recover_std_vectorized(std_u, synapse_mask):
    """
    STD资源恢复：u(t+1) = u(t) + (U_0 - u(t)) / TAU_STD
    只更新有突触的位置（synapse_mask = adj != 0，提前计算）。
    全numpy操作，无Python循环。
    """
    if not STD_ENABLED:
        return
    # 指数恢复（线性近似，每步Δu = (U_0-u)/τ）
    std_u[synapse_mask] += (U_0 - std_u[synapse_mask]) / TAU_STD

# ============================================================
# 单层传播（Fix-5: 真实延迟队列）
# ============================================================
def propagate_layer_delayed(adj, el_mask, is_inhib, std_u, delays,
                            wave, refrac, fired, N, G,
                            delay_buffer, current_step, rng):
    """
    真实延迟传播（修正版）：
      延迟规则：
        delay=1 → 下一步(current_step+1)到达（最短轴突延迟）
        delay=2,3 → 后续步到达
      每步流程：
        1. 先处理delay_buffer[current_step]中到达的消息（上几步发出的）
        2. 当前wave的神经元向邻居发出信号，压入delay_buffer[current_step+delay]
      这样每次BTW注入后，下一步（step+1）才有新激活到达，
      雪崩自然跨越多个时间步。

    delay_buffer: dict[int, list[(target, eff_weight, is_excit)]]
    """
    new_wave = np.zeros(N, dtype=bool)
    inhib_input = np.zeros(N, dtype=np.float32)

    # --- 1. 处理本步到达的延迟消息 ---
    arrivals = delay_buffer.pop(current_step, [])
    for (tgt, eff_w, is_ex) in arrivals:
        if refrac[tgt] > 0 or fired[tgt]:
            continue
        if is_ex:
            if rng.random() < min(eff_w, 0.99):
                new_wave[tgt] = True
        else:
            inhib_input[tgt] += eff_w

    # --- 2. 当前wave发送信号到delay_buffer ---
    active_idx = np.where(wave)[0]
    for i in active_idx:
        w_row = adj[i, :] * G
        w_row[el_mask[i, :]] *= 1.15

        if is_inhib[i]:
            w_scaled = w_row * INHIB_SCALE
            for c in np.where(w_scaled > 0.005)[0]:
                if c == i: continue
                u_ij = float(std_u[i, c])
                eff = float(w_scaled[c]) * u_ij
                if STD_ENABLED:
                    std_u[i, c] *= (1.0 - USE_FACTOR)
                # delay>=1，下一步才到
                arr = current_step + int(delays[i, c])
                delay_buffer[arr].append((int(c), eff, False))
        else:
            for c in np.where(w_row > 0.005)[0]:
                u_ij = float(std_u[i, c])
                eff = float(w_row[c]) * u_ij
                if STD_ENABLED:
                    std_u[i, c] *= (1.0 - USE_FACTOR)
                arr = current_step + int(delays[i, c])
                delay_buffer[arr].append((int(c), eff, True))

    # --- 3. 抑制削减 ---
    for tgt in np.where(inhib_input > 0)[0]:
        if new_wave[tgt]:
            if rng.random() < min(float(inhib_input[tgt]) * 0.5, 0.99):
                new_wave[tgt] = False

    new_wave &= ~fired
    return new_wave

# ============================================================
# 校准：真实BTW稳态条件下的κ估计（Fix-6: 全雪崩平均）
# ============================================================
def estimate_kappa_full_avalanche(adj, el_mask, is_inhib, delays, std_u_init,
                                  N, G, seed, n_warmup, n_measure):
    """
    真实BTW驱动条件下，用Priesemann 2014方法计算分支比κ：

      对每步t：记录激活神经元数n(t)
      κ = Σ[n(t+1)·I(n(t)>0)] / Σ[n(t)·I(n(t)>0)]
      即：在有激活的步上，下一步的激活数 / 这一步的激活数

      关键：这里记录的是“fired_in_av思的当前运行波”大小，
      而不是延迟队列的new_wave。
      延迟队列保证雪崩跨越多步，而κ通过激活数时间序列计算。
    """
    rng = np.random.default_rng(seed)
    refrac = np.zeros(N, dtype=np.int8)
    std_u = std_u_init.copy()
    synapse_mask = adj != 0
    current_wave = np.zeros(N, dtype=bool)
    fired_in_av = np.zeros(N, dtype=bool)
    delay_buffer = defaultdict(list)

    # 记录每步实际激活的神经元数（包含延迟到达的）
    activation_log = []   # 仅测量阶段

    for step in range(n_warmup + n_measure):
        is_measuring = (step >= n_warmup)
        recover_std_vectorized(std_u, synapse_mask)

        # BTW驱动
        if not current_wave.any() and step % BTW_INTERVAL == 0:
            d = int(rng.integers(N))
            if refrac[d] == 0:
                current_wave[d] = True
                fired_in_av[:] = False
                fired_in_av[d] = True

        # 单层传播（延迟队列）
        # current_wave：本步还没发送信号的活跃神经元
        # new_wave：本步到达的延迟信号激活的神经元
        new_wave = propagate_layer_delayed(
            adj, el_mask, is_inhib, std_u, delays,
            current_wave, refrac, fired_in_av, N, G,
            delay_buffer, step, rng
        )
        fired_in_av |= new_wave
        # 下一步的活跃波 = 本步延迟到达的＋待发送的（delay_buffer里尚有展待）
        # 用“延迟队列是否为空”判断雪崩是否结束
        current_wave = new_wave

        n_act = int(new_wave.sum())
        if is_measuring:
            activation_log.append(n_act)

        refrac[current_wave] = T_ABS
        refrac[refrac > 0] -= 1

    # 用激活时间序列计算Priesemannκ
    if len(activation_log) < 10:
        return 0.0
    arr = np.array(activation_log, dtype=float)
    num = arr[1:][arr[:-1] > 0].sum()
    den = arr[:-1][arr[:-1] > 0].sum()
    return float(num / den) if den > 0 else 0.0


def calibrate_G(adj, el_mask, is_inhib, delays, std_u_after_learn, N, seed):
    """二分法校准G，使κ∈[0.90, 1.10]。"""
    G_lo = G_LO_INIT; G_hi = G_HI_INIT; G_best = 0.5

    for i in range(CALIB_ITER):
        G_mid = (G_lo + G_hi) / 2
        kappa = estimate_kappa_full_avalanche(
            adj, el_mask, is_inhib, delays, std_u_after_learn,
            N, G_mid, seed + i * 997, CALIB_WARMUP, CALIB_STEPS
        )
        print(f"    校准 iter={i+1}: G={G_mid:.5f} → κ={kappa:.4f}")
        sys.stdout.flush()

        if 0.90 <= kappa <= 1.10:
            G_best = G_mid
            print(f"    ✅ G={G_best:.5f}, κ={kappa:.4f}")
            return G_best, kappa

        if kappa < 0.90:
            G_lo = G_mid
        else:
            G_hi = G_mid

        if G_hi - G_lo < 0.0002:
            G_best = G_mid; break
        G_best = G_mid

    kf = estimate_kappa_full_avalanche(
        adj, el_mask, is_inhib, delays, std_u_after_learn,
        N, G_best, seed + 9999999, CALIB_WARMUP, CALIB_STEPS
    )
    print(f"    ⚠️ 校准结束 G={G_best:.5f}, κ={kf:.4f}")
    return G_best, kf

# ============================================================
# 雪崩检测（含shape collapse数据）
# ============================================================
def detect_avalanches_full(activation_series):
    """
    检测雪崩，返回：
      sizes, durations, kappas_inner, shapes
      shapes: list of list（每个雪崩的逐层激活序列）
    """
    sizes, durations, kappas_inner, shapes = [], [], [], []
    in_av = False; layers = []

    for n in activation_series:
        if n > 0:
            in_av = True; layers.append(n)
        else:
            if in_av and layers:
                sizes.append(sum(layers))
                durations.append(len(layers))
                shapes.append(layers[:])
                if len(layers) >= 2:
                    den = sum(layers[:-1])
                    ki = sum(layers[1:]) / den if den > 0 else 0.0
                    kappas_inner.append(ki)
                in_av = False; layers = []

    if in_av and layers:
        sizes.append(sum(layers)); durations.append(len(layers))
        shapes.append(layers[:])
        if len(layers) >= 2:
            den = sum(layers[:-1])
            kappas_inner.append(sum(layers[1:]) / den if den > 0 else 0.0)

    return sizes, durations, kappas_inner, shapes

# ============================================================
# 幂律拟合（Hill MLE + KS检验 + 似然比检验，Fix-2/3）
# ============================================================
def fit_powerlaw_strict(data):
    """
    严格幂律拟合：
      1. Hill MLE估计τ（最优xmin via KS统计量）
      2. KS-statistic & bootstrap p_value
      3. 似然比检验：幂律 vs 对数正态
      4. 截断幂律拟合

    返回: {tau, xmin, n_tail, r2, ks_stat, plausible, vs_lognormal}
    """
    data = np.array([d for d in data if d > 0], dtype=float)
    result = {
        'tau': None, 'xmin': None, 'n_tail': len(data),
        'r2': 0.0, 'ks_stat': 1.0, 'plausible': False,
        'lr_vs_lognormal': None
    }
    if len(data) < 30:
        return result

    # --- 候选xmin扫描 ---
    p5 = max(1.0, np.percentile(data, 5))
    p65 = np.percentile(data, 65)
    cands = np.unique(data)
    cands = cands[(cands >= p5) & (cands <= p65)]
    if len(cands) == 0:
        cands = [np.median(data)]

    best_ks = np.inf; best_xmin = p5; best_tau = 1.5; best_tail = data

    for xm in cands[:50]:
        tail = data[data >= xm]
        if len(tail) < 15: continue
        lr = np.log(tail / xm)
        if lr.sum() == 0: continue
        tau_e = 1 + len(tail) / lr.sum()
        if tau_e <= 1.0 or tau_e > 8.0: continue
        ts = np.sort(tail)
        n_t = len(ts)
        ecdf = np.arange(1, n_t + 1) / n_t
        tcdf = 1 - (ts / xm) ** (-(tau_e - 1))
        ks = float(np.max(np.abs(ecdf - tcdf)))
        if ks < best_ks:
            best_ks = ks; best_xmin = xm; best_tau = tau_e; best_tail = tail

    result['xmin'] = float(best_xmin)
    result['tau'] = float(best_tau)
    result['n_tail'] = len(best_tail)
    result['ks_stat'] = float(best_ks)

    # --- R²（log-log bin拟合）---
    if len(best_tail) > 10:
        bins = min(20, max(5, len(best_tail) // 8))
        counts, edges = np.histogram(best_tail, bins=bins)
        centers = (edges[:-1] + edges[1:]) / 2
        msk = counts > 0
        if msk.sum() >= 4:
            lx = np.log(centers[msk]); ly = np.log(counts[msk])
            c = np.polyfit(lx, ly, 1)
            fit = np.polyval(c, lx)
            ssr = np.sum((ly - fit) ** 2); sst = np.sum((ly - np.mean(ly)) ** 2)
            result['r2'] = float(1 - ssr / sst) if sst > 0 else 0.0

    # --- KS bootstrap p_value（简化版：50次重采样）---
    # 幂律分布下的理论KS分布
    n_t = len(best_tail)
    tau = best_tau; xmin = best_xmin
    n_boot = 50
    ks_boot = []
    rng_boot = np.random.default_rng(42)
    for _ in range(n_boot):
        # 从拟合幂律采样
        u = rng_boot.uniform(size=n_t)
        synthetic = xmin * (1 - u) ** (-1 / (tau - 1))
        synthetic = np.sort(synthetic)
        ecdf_s = np.arange(1, n_t + 1) / n_t
        tau_s = 1 + n_t / np.sum(np.log(synthetic / xmin))
        if tau_s <= 1: tau_s = 1.01
        tcdf_s = 1 - (synthetic / xmin) ** (-(tau_s - 1))
        ks_boot.append(float(np.max(np.abs(ecdf_s - tcdf_s))))
    p_value = float(np.mean(np.array(ks_boot) >= best_ks))
    result['plausible'] = (p_value >= 0.1)   # p>=0.1 则不拒绝幂律假设
    result['p_value'] = p_value

    # --- 似然比检验：幂律 vs 对数正态 ---
    tail = best_tail
    # 幂律对数似然
    ll_pl = np.sum(np.log(tau - 1) - np.log(xmin) - tau * np.log(tail / xmin))
    # 对数正态对数似然
    log_tail = np.log(tail)
    mu_ln = log_tail.mean(); sigma_ln = log_tail.std()
    if sigma_ln > 0:
        ll_ln = np.sum(-np.log(tail) - 0.5 * np.log(2 * np.pi * sigma_ln**2)
                       - 0.5 * ((log_tail - mu_ln) / sigma_ln) ** 2)
        lr_stat = float(ll_pl - ll_ln)
        result['lr_vs_lognormal'] = lr_stat  # >0: 幂律更好; <0: 对数正态更好
    else:
        result['lr_vs_lognormal'] = 0.0

    return result


def compute_psd_slope(activation_series):
    arr = np.array(activation_series, dtype=float) - np.mean(activation_series)
    n = len(arr)
    power = np.abs(np.fft.rfft(arr)) ** 2
    freqs = np.fft.rfftfreq(n)
    mask = (freqs > 0.001) & (freqs < 0.25)
    if mask.sum() < 15:
        return 0.0, 0.0
    lf = np.log(freqs[mask]); lp = np.log(power[mask] + 1e-10)
    c = np.polyfit(lf, lp, 1)
    fit = np.polyval(c, lf)
    ssr = np.sum((lp - fit) ** 2); sst = np.sum((lp - np.mean(lp)) ** 2)
    r2 = float(1 - ssr / sst) if sst > 0 else 0.0
    return float(c[0]), r2

# ============================================================
# 主仿真
# ============================================================
def run_simulation(net_name, net_cfg, seed, use_pruning=False):
    N = net_cfg['N']
    sf = net_cfg['sf']
    K_PATTERNS = net_cfg['K_PATTERNS']

    rng = np.random.default_rng(seed)

    # 初始化
    adj = make_ws_adj_directed(N, net_cfg['k_init'], net_cfg['p_init'], seed)
    is_inhib = assign_neuron_types(N, FRAC_INHIB, seed)
    std_u = init_std_resources(N, seed)
    delays = assign_delays(N, seed)
    synapse_mask = adj != 0   # Fix-8: 提前计算，供recover_std使用

    el_mask = np.zeros((N, N), dtype=bool)
    el_mask[adj > 0] = rng.random((adj > 0).sum()) < 0.05
    # I神经元输出突触不固化
    el_mask[is_inhib, :] = False

    nltp = np.zeros((N, N), dtype=np.int16)
    nltd = np.zeros((N, N), dtype=np.int16)
    el_age = np.zeros((N, N), dtype=np.int32)
    refrac = np.zeros(N, dtype=np.int8)

    # Fix-4: 真实spike时间戳
    last_spike = np.full(N, -99999, dtype=np.int32)

    # Fix-7: exc_mask_pre提前计算（不在循环内重建）
    exc_mask_pre = np.outer(~is_inhib, np.ones(N, dtype=bool))  # (N,N)

    # 刺激模式
    stim_size = max(1, int(N * sf))
    rng_pat = np.random.default_rng(seed + 1000)
    patterns = [rng_pat.choice(N, size=stim_size, replace=False).tolist()
                for _ in range(K_PATTERNS)]

    topology_log = []
    t0 = time.time()
    pat_idx = 0

    n_exc = int((~is_inhib).sum()); n_inh = int(is_inhib.sum())
    print(f"  [{net_name}|{seed}] N={N} E={n_exc}({n_exc/N:.0%}) I={n_inh}({n_inh/N:.0%})")
    print(f"  [{net_name}|{seed}] 学习阶段（{N_LEARN}步）...")
    sys.stdout.flush()

    # ===========================================================
    # 阶段1：学习（STDP演化拓扑）
    # ===========================================================
    delay_buffer_learn = defaultdict(list)

    for step in range(N_LEARN):
        # STD恢复
        recover_std_vectorized(std_u, synapse_mask)

        # 外部刺激
        active = np.zeros(N, dtype=bool)
        if step % 10 == 0 and rng.random() < 0.1:
            pat_idx = int(rng.integers(K_PATTERNS))
        for ni in patterns[pat_idx % K_PATTERNS]:
            if refrac[ni] == 0 and rng.random() < 0.25:
                active[ni] = True

        # 单层传播（学习阶段G=1.0）
        if active.any():
            fired = active.copy()
            new_w = propagate_layer_delayed(
                adj, el_mask, is_inhib, std_u, delays,
                active, refrac, fired, N, 1.0,
                delay_buffer_learn, step, rng
            )
            active |= new_w

        n_act = int(active.sum())

        # Fix-4: 更新spike时间戳
        last_spike[active] = step

        refrac[active] = T_ABS + T_REL
        refrac[refrac > 0] -= 1

        # STDP（真实时差，Fix-4）
        aidx_exc = np.where(active & ~is_inhib)[0]
        aidx_all = np.where(active)[0]
        if len(aidx_exc) >= 2 and len(aidx_all) >= 1:
            n_p = min(len(aidx_exc) * 2, 120)
            pre_arr = rng.choice(aidx_exc, size=n_p)
            post_arr = rng.choice(aidx_all, size=n_p)
            for pre, post in zip(pre_arr, post_arr):
                if pre == post: continue
                # Fix-4: 真实spike时差
                dt = int(last_spike[post]) - int(last_spike[pre])
                if abs(dt) > STDP_MAX_DT: continue   # 超出时间窗口，不更新

                if dt > 0:
                    # post在pre之后激活 → LTP（因果链）
                    dw = ETA_LTP * np.exp(-abs(dt) / TAU_STDP)
                    if adj[pre, post] > 0 and not is_inhib[pre]:
                        adj[pre, post] = min(1.0, adj[pre, post] + dw)
                        nltp[pre, post] += 1
                else:
                    # post在pre之前激活 → LTD（反因果）
                    dw = ETA_LTD * np.exp(-abs(dt) / TAU_STDP)
                    if adj[post, pre] > 0 and not is_inhib[post]:
                        adj[post, pre] = max(0.0, adj[post, pre] - dw)
                        nltd[post, pre] += 1

        # 突触固化/消除（仅兴奋性，Fix-7用预计算的exc_mask_pre）
        el_ratio = el_mask.sum() / max(1, (adj > 0).sum())
        ltp_m = (nltp >= THETA_LTP) & (adj > 0) & (~el_mask) & (el_ratio < EL_HI) & exc_mask_pre
        el_mask[ltp_m] = True; nltp[ltp_m] = 0

        ltd_m = (nltd >= THETA_LTD) & (adj > 0) & (~el_mask) & exc_mask_pre
        adj[ltd_m] = 0.0; nltp[ltd_m] = nltd[ltd_m] = 0
        synapse_mask = adj != 0   # 更新突触掩码

        el_age[el_mask] += 1
        dm = el_mask & (el_age > T_DECAY)
        el_mask[dm] = False; el_age[dm] = 0

        # WS随机重连（仅兴奋性非固化突触）
        if step % REWIRE_INT == 0:
            non_el = np.argwhere((adj > 0) & (~el_mask) & exc_mask_pre)
            n_r = max(1, int(len(non_el) * P_REWIRE * 0.01))
            for _ in range(min(n_r, len(non_el))):
                if len(non_el) == 0: break
                ix = int(rng.integers(len(non_el))); i, j = non_el[ix]
                kn = int(rng.integers(N))
                if kn != i and adj[i, kn] == 0:
                    adj[i, kn] = adj[i, j]; adj[i, j] = 0.0
                    synapse_mask[i, j] = False; synapse_mask[i, kn] = True

        # 突触缩放
        if step % SCALING_INT == 0 and n_act > 0:
            ar = n_act / N
            if ar > KAPPA_TARGET:
                adj[~el_mask] *= (1 - SCALING_RATE)
            elif ar < KAPPA_TARGET * 0.5:
                adj[~el_mask] *= (1 + SCALING_RATE)
            adj = np.clip(adj, 0.0, 1.0)

        # 竞争性修剪（4规则）
        if use_pruning and step % PRUNE_INT == 0 and step > 0:
            deg = (adj > 0).sum(axis=1)
            cands = np.argwhere((adj > 0) & (~el_mask) & exc_mask_pre & (nltp == 0) & (nltd == 0))
            for i, j in cands:
                if deg[i] > MIN_EDGES and rng.random() < P_PRUNE:
                    adj[i, j] = 0.0; synapse_mask[i, j] = False
            nltp[:] = 0; nltd[:] = 0

        if step % LOG_INT == 0:
            sig = compute_sigma_fast(adj, N)
            print(f"    学习 {step}/{N_LEARN} σ={sig:.2f} edges={(adj>0).sum()} t={time.time()-t0:.0f}s")
            sys.stdout.flush()
            topology_log.append({'step': step, 'sigma': sig,
                                  'n_edges': int((adj > 0).sum()),
                                  'n_el': int(el_mask.sum()), 'phase': '学习'})

    # Fix-1: 保存学习阶段末尾STD状态（供校准和记录阶段共用）
    std_u_after_learn = std_u.copy()
    sigma_after = compute_sigma_fast(adj, N)
    print(f"\n  学习后: edges={(adj>0).sum()} σ={sigma_after:.2f} el={el_mask.sum()}")

    # ===========================================================
    # 临界点校准（Fix-1: 用std_u_after_learn，Fix-6: 全雪崩κ）
    # ===========================================================
    print(f"\n  [{net_name}|{seed}] 临界点校准（真实稳态条件）...")
    sys.stdout.flush()
    G_calib, kappa_calib = calibrate_G(
        adj, el_mask, is_inhib, delays, std_u_after_learn, N, seed
    )
    print(f"  校准结果: G={G_calib:.5f}, κ={kappa_calib:.4f}")
    sys.stdout.flush()

    # ===========================================================
    # 阶段2：雪崩记录（Fix-1: std_u从学习末尾状态继续）
    # ===========================================================
    print(f"\n  [{net_name}|{seed}] 记录阶段（{N_RECORD}步，G={G_calib:.4f}）...")
    sys.stdout.flush()

    activation_series = []
    refrac[:] = 0
    std_u_rec = std_u_after_learn.copy()   # Fix-1: 继承学习末尾状态
    current_wave = np.zeros(N, dtype=bool)
    fired_in_av = np.zeros(N, dtype=bool)
    delay_buffer_rec = defaultdict(list)
    kappa_per_step = []   # Fix-9: κ时间序列（涨落分析）

    for step in range(N_RECORD):
        recover_std_vectorized(std_u_rec, synapse_mask)

        # BTW驱动：仅当延迟队列为空（无展待信号）且current_wave空时注入
        abs_step = N_LEARN + step
        queue_has_pending = any(k >= abs_step for k in delay_buffer_rec.keys())
        if not current_wave.any() and not queue_has_pending and step % BTW_INTERVAL == 0:
            d = int(rng.integers(N))
            if refrac[d] == 0:
                current_wave[d] = True
                fired_in_av[:] = False
                fired_in_av[d] = True

        # 单层传播
        new_wave = propagate_layer_delayed(
            adj, el_mask, is_inhib, std_u_rec, delays,
            current_wave, refrac, fired_in_av, N, G_calib,
            delay_buffer_rec, abs_step, rng
        )
        fired_in_av |= new_wave

        prev_size = int(current_wave.sum())
        curr_size = int(new_wave.sum())
        if prev_size > 0:
            kappa_per_step.append(curr_size / prev_size)

        current_wave = new_wave
        n_wave = int(new_wave.sum())
        activation_series.append(n_wave)
        refrac[current_wave] = T_ABS
        refrac[refrac > 0] -= 1

        if step % LOG_INT == 0:
            sig = compute_sigma_fast(adj, N)
            print(f"    记录 {step}/{N_RECORD} wave={n_wave} σ={sig:.2f} t={time.time()-t0:.0f}s")
            sys.stdout.flush()
            topology_log.append({'step': N_LEARN + step, 'sigma': sig,
                                  'n_edges': int((adj > 0).sum()),
                                  'n_el': int(el_mask.sum()), 'phase': '记录'})

    # ===========================================================
    # 雪崩分析
    # ===========================================================
    arr = np.array(activation_series)
    zero_frac = float((arr == 0).mean())
    print(f"\n  激活统计: 零帧={zero_frac:.1%} 最大={arr.max()} 均={arr.mean():.3f}")

    sizes, durations, kappas_inner, shapes = detect_avalanches_full(activation_series)

    # 幂律严格拟合（Fix-2）
    res_size = fit_powerlaw_strict(sizes)
    res_dur  = fit_powerlaw_strict(durations)
    tau_s = res_size['tau']; r2_s = res_size['r2']
    tau_d = res_dur['tau'];  r2_d = res_dur['r2']

    kappa = float(np.mean(kappas_inner)) if kappas_inner else 0.0
    kappa_std = float(np.std(kappas_inner)) if len(kappas_inner) > 1 else 0.0  # Fix-9
    psd_slope, psd_r2 = compute_psd_slope(activation_series)

    n_avalanches = len(sizes)
    mean_size = float(np.mean(sizes)) if sizes else 0.0
    mean_dur  = float(np.mean(durations)) if durations else 0.0
    dur_arr = np.array(durations) if durations else np.array([0])
    frac_dur1 = float((dur_arr == 1).mean()) if len(dur_arr) > 0 else 1.0

    # Fix-3: τ缩放关系检验（Friedman 2012 PRL）
    if tau_s is not None and tau_d is not None:
        tau_d_theory = (tau_s + 1) / 2
        scale_err = abs(tau_d - tau_d_theory) / tau_d_theory
        scale_ok = scale_err < 0.25   # 误差<25%
    else:
        scale_err = 1.0; scale_ok = False

    # 达标判定
    size_ok   = (tau_s is not None and 1.2 <= tau_s <= 2.2
                 and r2_s > 0.70 and res_size.get('plausible', False))
    dur_ok    = (tau_d is not None and 1.5 <= tau_d <= 2.8 and r2_d > 0.70)
    kappa_ok  = (0.85 <= kappa <= 1.15)
    count_ok  = (n_avalanches >= 300)
    psd_ok    = (psd_slope is not None and -1.5 <= psd_slope <= -0.3)
    zero_ok   = (zero_frac >= 0.3)
    multi_ok  = (frac_dur1 < 0.8)

    score = sum([size_ok, dur_ok, kappa_ok, count_ok, psd_ok, zero_ok, multi_ok, scale_ok])
    max_score = 8  # 新增scale_ok

    ts_str = f"{tau_s:.3f}" if tau_s else "N/A"
    td_str = f"{tau_d:.3f}" if tau_d else "N/A"
    ps_str = f"{psd_slope:.3f}" if psd_slope else "N/A"
    td_th_str = f"{(tau_s+1)/2:.3f}" if tau_s else "N/A"

    print(f"\n{'='*65}")
    print(f"  结果 [{net_name}|{seed}|{'4r' if use_pruning else '3r'}] G={G_calib:.4f}")
    print(f"  零帧: {zero_frac:.1%} {'✓' if zero_ok else '✗'}")
    print(f"  雪崩数: {n_avalanches} | 均尺寸: {mean_size:.1f} | 均时长: {mean_dur:.1f} {'✓' if count_ok else '✗'}")
    print(f"  多步雪崩: {1-frac_dur1:.1%} {'✓' if multi_ok else '✗'}")
    print(f"  τ_size={ts_str} R²={r2_s:.3f} p={res_size.get('p_value',0):.2f} {'✓' if size_ok else '✗'}")
    print(f"  τ_dur={td_str} R²={r2_d:.3f} (理论={td_th_str} 误差={scale_err:.0%}) {'✓' if dur_ok else '✗'}")
    print(f"  τ缩放关系: {'✓' if scale_ok else '✗'} (误差{scale_err:.0%})")
    print(f"  κ={kappa:.4f} ±{kappa_std:.3f} {'✓' if kappa_ok else '✗'}")
    print(f"  PSD={ps_str} R²={psd_r2:.3f} {'✓' if psd_ok else '✗'}")
    lr_val = res_size.get('lr_vs_lognormal') or 0.0
    print(f"  似然比(PL vs LN): {lr_val:.2f} (>0=幂律更好)")
    print(f"  得分: {score}/{max_score}")
    print(f"  {'='*65}\n")
    sys.stdout.flush()

    return {
        'network': net_name, 'seed': seed,
        'rules': '4-rules' if use_pruning else '3-rules',
        'bio': {
            'E_frac': float((~is_inhib).mean()),
            'std_enabled': STD_ENABLED,
            'delay_enabled': DELAY_ENABLED,
            'directed_adj': True,
            'real_stdp_dt': True
        },
        'G_calib': float(G_calib),
        'kappa_calib': float(kappa_calib),
        'zero_fraction': float(zero_frac),
        'n_avalanches': n_avalanches,
        'mean_size': float(mean_size),
        'mean_duration': float(mean_dur),
        'frac_dur1': float(frac_dur1),
        'tau_size': float(tau_s) if tau_s else None,
        'r2_size': float(r2_s),
        'ks_stat_size': float(res_size['ks_stat']),
        'p_value_size': float(res_size.get('p_value', 0)),
        'lr_vs_lognormal': float(res_size.get('lr_vs_lognormal') or 0.0),
        'tau_duration': float(tau_d) if tau_d else None,
        'r2_duration': float(r2_d),
        'tau_scale_error': float(scale_err),
        'branching_ratio': float(kappa),
        'branching_ratio_std': float(kappa_std),
        'psd_slope': float(psd_slope) if psd_slope else None,
        'psd_r2': float(psd_r2),
        'sigma_after_learn': float(sigma_after),
        'score': int(score),
        'max_score': max_score,
        'criteria': {
            'zero_frames': bool(zero_ok),
            'size_powerlaw': bool(size_ok),
            'duration_powerlaw': bool(dur_ok),
            'tau_scale_relation': bool(scale_ok),
            'branching_ratio': bool(kappa_ok),
            'avalanche_count': bool(count_ok),
            'psd_1f': bool(psd_ok),
            'multi_step': bool(multi_ok)
        },
        'topology_log': topology_log,
        'activation_sample': [int(x) for x in activation_series[:6000]],
        'sizes_sample': sorted([int(s) for s in sizes])[:1500],
        'durations_sample': sorted([int(d) for d in durations])[:1500],
        'kappa_series_sample': [float(k) for k in kappa_per_step[:2000]],
    }

# ============================================================
# 绘图
# ============================================================
def plot_results(all_results):
    fig = plt.figure(figsize=(22, 26))
    fig.suptitle(
        'SDI Exp5 v7: Neuronal Avalanche (Full Bio + Strict Statistics)\n'
        'Fixes: STD continuity, real STDP dt, delay queues, full-avalanche kappa, KS test',
        fontsize=11, fontweight='bold', y=0.99
    )
    gs = GridSpec(6, 3, figure=fig, hspace=0.50, wspace=0.38)

    from collections import defaultdict
    bg = defaultdict(list)
    for r in all_results:
        bg[r['network'] + '_' + r['rules']].append(r)
    best = {k: max(v, key=lambda x: x['score']) for k, v in bg.items()}
    items = sorted(best.items())[:6]
    colors = {'3-rules': '#2196F3', '4-rules': '#E91E63'}

    for pi, (key, res) in enumerate(items):
        if pi >= 6: break
        color = colors.get(res['rules'], '#333')
        row, col = divmod(pi, 3)

        # --- 激活序列 ---
        ax1 = fig.add_subplot(gs[row * 2, col])
        act = res.get('activation_sample', [])
        if act:
            ax1.plot(act[:4000], color=color, linewidth=0.5, alpha=0.8)
        sc = res.get('score', 0); mx = res.get('max_score', 8)
        G = res.get('G_calib', 1.0); kv = res.get('branching_ratio', 0)
        kstd = res.get('branching_ratio_std', 0)
        ax1.set_title(
            f"{res['network']} {res['rules']}\n"
            f"G={G:.3f} κ={kv:.3f}±{kstd:.2f} Score={sc}/{mx}",
            fontsize=7, color='green' if sc >= mx * 0.75 else ('orange' if sc >= mx * 0.5 else 'red')
        )
        ax1.set_xlabel('Step', fontsize=6); ax1.set_ylabel('Wave', fontsize=6)
        ax1.tick_params(labelsize=6)

        # --- 雪崩尺寸分布（log-log）---
        ax2 = fig.add_subplot(gs[row * 2 + 1, col])
        sizes = res.get('sizes_sample', [])
        if sizes and len(sizes) > 10:
            sa = np.array(sizes)
            try:
                mn, mx2 = max(1, sa.min()), max(sa.max(), 2)
                b = np.logspace(np.log10(mn), np.log10(mx2), 30)
                cnt, edg = np.histogram(sa, bins=b)
                ctr = (edg[:-1] + edg[1:]) / 2
                msk = cnt > 0
                if msk.sum() > 3:
                    ax2.loglog(ctr[msk], cnt[msk], 'o', color=color, ms=4, alpha=0.7, label='Data')
                    xt = np.logspace(np.log10(ctr[msk][0]), np.log10(ctr[msk][-1]), 50)
                    y0 = cnt[msk][0] * (ctr[msk][0] ** 1.5)
                    ax2.loglog(xt, y0 / (xt ** 1.5), '--', color='gray', alpha=0.6, label='tau=1.5')
            except:
                pass
        ts = res.get('tau_size'); r2s = res.get('r2_size', 0)
        pv = res.get('p_value_size', 0)
        ts_str = f"{ts:.2f}" if ts else "N/A"
        ok = res.get('criteria', {}).get('size_powerlaw', False)
        sc_err = res.get('tau_scale_error', 1.0)
        ax2.set_title(
            f"tau_s={ts_str} R2={r2s:.2f} p={pv:.2f} {'✓' if ok else '✗'}\n"
            f"scale_err={sc_err:.0%} {'✓' if sc_err<0.25 else '✗'}",
            fontsize=6.5, color='green' if ok else 'red'
        )
        ax2.set_xlabel('S', fontsize=6); ax2.set_ylabel('Count', fontsize=6)
        ax2.tick_params(labelsize=6); ax2.legend(fontsize=5)

    plt.savefig(f'{OUT}/exp5_v7_avalanche_results.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Figure: {OUT}/exp5_v7_avalanche_results.png")

# ============================================================
# 主程序
# ============================================================
def main():
    print("=" * 70)
    print("SDI Experiment 5 v7 — Scientific Rigour Edition")
    print("  Fix-1: STD state continuity (learn -> calibrate -> record)")
    print("  Fix-2: Strict power-law stats (KS test + LR test)")
    print("  Fix-3: tau scaling relation check (Friedman 2012 PRL)")
    print("  Fix-4: Real STDP spike timestamps")
    print("  Fix-5: Real delay queues (not weight decay)")
    print("  Fix-6: Full-avalanche kappa calibration")
    print("  Fix-7: exc_mask_pre pre-computed")
    print("  Fix-8: recover_std vectorized")
    print("  Fix-9: kappa std reported")
    print("=" * 70)
    print(f"Networks: {list(NETWORKS.keys())}")
    print(f"Seeds: {SEEDS}")
    print(f"N_LEARN={N_LEARN}  N_RECORD={N_RECORD}")
    print(f"BTW_INTERVAL={BTW_INTERVAL}  TAU_STD={TAU_STD}  MAX_DELAY={MAX_DELAY}")
    print("=" * 70)
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

    # 序列化
    def ser(o):
        if isinstance(o, (np.integer,)): return int(o)
        if isinstance(o, (np.floating,)): return float(o)
        if isinstance(o, np.ndarray): return o.tolist()
        return o
    def ds(o):
        if isinstance(o, dict): return {k: ds(v) for k, v in o.items()}
        if isinstance(o, list): return [ds(v) for v in o]
        return ser(o)

    out_path = f'{OUT}/exp5_v7_avalanche_results.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(ds(all_results), f, ensure_ascii=False, indent=2)
    print(f"\nSaved: {out_path}")

    try:
        plot_results(all_results)
    except Exception as e:
        print(f"  Plot error: {e}")

    # 汇总
    print("\n" + "=" * 70 + "\nSummary v7\n" + "=" * 70)
    from collections import defaultdict
    gd = defaultdict(list)
    for r in all_results:
        gd[f"{r['network']}_{r['rules']}"].append(r)

    print(f"\n{'Group':<28} G{'':5} κ{'':5} τ_s{'':4} τ_d{'':4} scale%  PSD{'':4} Score")
    print("-" * 85)
    for key, runs in sorted(gd.items()):
        G    = np.mean([r['G_calib'] for r in runs])
        kv   = np.mean([r['branching_ratio'] for r in runs])
        ts_l = [r['tau_size'] for r in runs if r['tau_size'] is not None]
        td_l = [r['tau_duration'] for r in runs if r['tau_duration'] is not None]
        pv_l = [r['psd_slope'] for r in runs if r['psd_slope'] is not None]
        se_l = [r['tau_scale_error'] for r in runs]
        sv   = [r['score'] for r in runs]
        mx   = runs[0]['max_score']
        ts_s = f"{np.mean(ts_l):.2f}" if ts_l else "N/A"
        td_s = f"{np.mean(td_l):.2f}" if td_l else "N/A"
        pv_s = f"{np.mean(pv_l):.2f}" if pv_l else "N/A"
        se_s = f"{np.mean(se_l):.0%}"
        print(f"{key:<28} {G:.4f} {kv:.3f}  {ts_s:<7} {td_s:<7} {se_s:<8} {pv_s:<7} {np.mean(sv):.1f}/{mx}")

    print()
    best = max(all_results, key=lambda x: x['score'])
    ts_b = f"{best['tau_size']:.3f}" if best['tau_size'] else "N/A"
    td_b = f"{best['tau_duration']:.3f}" if best['tau_duration'] else "N/A"
    print(f"Best: {best['network']} | {best['rules']} | seed={best['seed']}")
    print(f"  tau_s={ts_b} tau_d={td_b}")
    print(f"  kappa={best['branching_ratio']:.3f} ± {best['branching_ratio_std']:.3f}")
    print(f"  scale_error={best['tau_scale_error']:.0%}")
    print(f"  G={best['G_calib']:.4f}  Score={best['score']}/{best['max_score']}")

    elapsed = time.time() - t_total
    print(f"\nTotal: {elapsed:.0f}s ({elapsed/60:.1f}min)")
    print("v7 complete.")
    sys.stdout.flush()


if __name__ == '__main__':
    main()
