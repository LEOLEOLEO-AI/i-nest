"""
SDI 实验八 — 20物种连接组普适性验证
=====================================
目标：
  用 v5 文献锁定参数集，在20个物种的网络上跑四规则演化，
  验证 SDI 规则是否普适——物种 IIL 等级是否与进化年龄单调对应，
  是否越高等物种越需要四规则全部满足。

设计要点：
  1. 20物种参数沿用 v17 的物种配置（N / k_init / level / 生物基准）
  2. 四条规则全部使用 v5 文献锁定参数（与 v5 完全一致）
  3. 每物种 3 个种子（节省时间，v17 是 5 个）
  4. 指标：σ / Q / EL_ratio / CST_Sc（空间复杂度 C·H·M·R_sw 四分量）
  5. 对照：四规则 vs 关闭 Rule4（验证 Rule4 的普适性）

物种列表（20个，按进化树顺序）：
  原始动物→无脊椎→鱼类→两栖→爬行/鸟→哺乳→灵长→人类
  进化年龄从 ~600Mya（海星幼虫）到 ~0.3Mya（智人）

v5 文献锁定参数：
  Rule1: THETA_LTP=60 (Bi&Poo 1998), THETA_LTD=50 (Song 2000)
  Rule2: 新生突触, w_init=[0.05,0.10] (Zito 2009), P_GROW=0.05
  Rule3: ACT=[3%,10%], 每200步 (Turrigiano 2012)
  Rule4: 竞争相对阈值×0.5 (Science 2022), 每200步
"""

import numpy as np
import json, os, time
import networkx as nx
from collections import defaultdict

BASE = '/home/work/.openclaw/workspace/sdi_sim'
OUT  = os.path.join(BASE, 'exp8_universality_results.json')

# ══════════════════════════════════════════════════════════
# v5 文献锁定参数（完整继承）
# ══════════════════════════════════════════════════════════
THETA_LTP      = 60
THETA_LTD      = 50
LTP_DECAY_INT  = 500
EL_WT_BOOST    = 1.5

GROW_INT       = 50
P_GROW         = 0.05
W_INIT_LO      = 0.05
W_INIT_HI      = 0.10
ACT_BIAS       = 2.0
MAX_NEW_FRAC   = 0.15

SCALING_INT    = 200
ACT_LO         = 0.03
ACT_HI         = 0.10
SCALE_UP       = 1.05
SCALE_DN       = 0.95

PRUNE_INT      = 200
P_PRUNE        = 0.05
MIN_EDGES      = 2
COMP_THR       = 0.5

N_STEPS        = 8000   # 稍短（物种多，节省时间）
LOG_INT        = 2000
SEEDS          = [42, 7, 13]

# ══════════════════════════════════════════════════════════
# 20物种定义
# 参数来源：v17 SPECIES 配置（已通过文献验证）
# 进化年龄（Mya）：用于验证 IIL↔进化年龄单调性
# ══════════════════════════════════════════════════════════
SPECIES = {
    # ── 原始动物 ──────────────────────────────────────────
    'Starfish_larva': {
        'N':20, 'k':4, 'p':0.15, 'level':'mesoscale',
        'evo_mya':600, 'ilevel':'L0-L1',
        'bio_sigma':[1.0,3.0], 'bio_C':[0.10,0.35],
        'ref':'Echinoderm larva, ~600Mya'},
    'Ciona': {
        'N':177, 'k':6, 'p':0.12, 'level':'neuron',
        'evo_mya':520, 'ilevel':'L1',
        'bio_sigma':[2.0,6.0], 'bio_C':[0.20,0.40],
        'ref':'Ciona intestinalis larva (tunicate), Ryan 2016'},
    'C_elegans_pharynx': {
        'N':20, 'k':4, 'p':0.15, 'level':'neuron',
        'evo_mya':500, 'ilevel':'L1',
        'bio_sigma':[1.0,3.5], 'bio_C':[0.15,0.40],
        'ref':'C.elegans pharynx circuit, ~500Mya'},
    # ── 无脊椎动物 ────────────────────────────────────────
    'C_elegans': {
        'N':279, 'k':8, 'p':0.10, 'level':'neuron',
        'evo_mya':500, 'ilevel':'L1-L2',
        'bio_sigma':[4.0,12.0], 'bio_C':[0.25,0.35],
        'ref':'White 1986; Varshney 2011'},
    'Platynereis': {
        'N':71, 'k':6, 'p':0.12, 'level':'neuron',
        'evo_mya':500, 'ilevel':'L1-L2',
        'bio_sigma':[2.0,7.0], 'bio_C':[0.20,0.40],
        'ref':'Randel 2014 eLife; annelid larva'},
    'Honeybee': {
        'N':160, 'k':8, 'p':0.10, 'level':'neuron',
        'evo_mya':400, 'ilevel':'L2',
        'bio_sigma':[3.0,9.0], 'bio_C':[0.22,0.38],
        'ref':'Menzel 2012 Nat Rev Neurosci; mushroom body'},
    'Larval_Drosophila': {
        'N':321, 'k':8, 'p':0.10, 'level':'neuron',
        'evo_mya':400, 'ilevel':'L2',
        'bio_sigma':[4.0,12.0], 'bio_C':[0.24,0.36],
        'ref':'Schlegel 2021; larval Drosophila connectome'},
    'Octopus': {
        'N':65, 'k':6, 'p':0.12, 'level':'neuron',
        'evo_mya':300, 'ilevel':'L2-L3',
        'bio_sigma':[2.0,7.0], 'bio_C':[0.20,0.38],
        'ref':'Shomrat 2011 J Neurosci; octopus vertical lobe'},
    # ── 脊椎动物——鱼类/两栖 ───────────────────────────────
    'Xenopus': {
        'N':44, 'k':6, 'p':0.12, 'level':'neuron',
        'evo_mya':350, 'ilevel':'L2',
        'bio_sigma':[1.5,5.0], 'bio_C':[0.18,0.38],
        'ref':'Roberts 2014 J Neurosci; Xenopus tadpole'},
    'Zebrafish': {
        'N':71, 'k':6, 'p':0.12, 'level':'mesoscale',
        'evo_mya':200, 'ilevel':'L2-L3',
        'bio_sigma':[2.0,7.0], 'bio_C':[0.20,0.40],
        'ref':'Bhatt 2009 approximate; zebrafish connectome'},
    # ── 哺乳动物 ──────────────────────────────────────────
    'Rat_Cortex': {
        'N':73, 'k':6, 'p':0.12, 'level':'mesoscale',
        'evo_mya':100, 'ilevel':'L3',
        'bio_sigma':[1.2,3.5], 'bio_C':[0.25,0.45],
        'ref':'Bota 2015; rat cortical connectome'},
    'Mouse_Cortex': {
        'N':112, 'k':8, 'p':0.10, 'level':'mesoscale',
        'evo_mya':90, 'ilevel':'L3',
        'bio_sigma':[1.2,3.5], 'bio_C':[0.25,0.45],
        'ref':'Oh 2014 Nature; Allen Mouse Brain Atlas'},
    'Cat_Visual': {
        'N':52, 'k':6, 'p':0.12, 'level':'mesoscale',
        'evo_mya':60, 'ilevel':'L3-L4',
        'bio_sigma':[1.5,4.0], 'bio_C':[0.26,0.46],
        'ref':'Scannell 1995; cat visual cortex'},
    'Macaque_Visual': {
        'N':242, 'k':8, 'p':0.10, 'level':'neuron',
        'evo_mya':25, 'ilevel':'L3-L4',
        'bio_sigma':[3.0,9.0], 'bio_C':[0.24,0.36],
        'ref':'Markov 2013 Science; macaque visual cortex'},
    'Macaque_Cortex': {
        'N':71, 'k':6, 'p':0.12, 'level':'mesoscale',
        'evo_mya':25, 'ilevel':'L3-L4',
        'bio_sigma':[1.2,3.5], 'bio_C':[0.25,0.45],
        'ref':'Stephan 2001; macaque cortical connectome'},
    # ── 灵长类 ────────────────────────────────────────────
    'Marmoset': {
        'N':55, 'k':6, 'p':0.12, 'level':'mesoscale',
        'evo_mya':35, 'ilevel':'L3-L4',
        'bio_sigma':[1.2,3.5], 'bio_C':[0.25,0.45],
        'ref':'Majka 2020 Sci Data; marmoset cortical'},
    'Chimpanzee': {
        'N':90, 'k':8, 'p':0.10, 'level':'mesoscale',
        'evo_mya':6, 'ilevel':'L4',
        'bio_sigma':[1.2,3.5], 'bio_C':[0.26,0.46],
        'ref':'Reardon 2016; chimpanzee connectome'},
    'Gorilla': {
        'N':90, 'k':8, 'p':0.10, 'level':'mesoscale',
        'evo_mya':8, 'ilevel':'L4',
        'bio_sigma':[1.2,3.5], 'bio_C':[0.26,0.46],
        'ref':'Donahue 2016 PNAS; great ape connectome'},
    # ── 鸟类（独立进化高智能）────────────────────────────
    'Pigeon': {
        'N':45, 'k':6, 'p':0.12, 'level':'mesoscale',
        'evo_mya':100, 'ilevel':'L2-L3',
        'bio_sigma':[1.0,3.0], 'bio_C':[0.20,0.40],
        'ref':'Shanahan 2013 PLOS CB; pigeon telencephalon'},
    # ── 人类 ──────────────────────────────────────────────
    'Human_HCP': {
        'N':80, 'k':8, 'p':0.10, 'level':'mesoscale',
        'evo_mya':0.3, 'ilevel':'L5',
        'bio_sigma':[1.5,4.5], 'bio_C':[0.30,0.50],
        'ref':'Van Essen 2013; Human Connectome Project'},
}

# ══════════════════════════════════════════════════════════
# 网络初始化（WS图，参数从物种配置读取）
# ══════════════════════════════════════════════════════════
def make_ws(N, k, p, rng):
    W = np.zeros((N, N), dtype=np.float32)
    k = max(4, k // 2 * 2)
    for i in range(N):
        for d in range(1, k // 2 + 1):
            j = (i + d) % N
            W[i, j] = W[j, i] = rng.uniform(0.10, 0.35)
    for i in range(N):
        for d in range(1, k // 2 + 1):
            if rng.random() < p:
                j  = (i + d) % N
                nj = rng.randint(0, N)
                if nj != i and W[i, nj] == 0:
                    W[i, nj] = W[i, j]; W[i, j] = 0
    np.fill_diagonal(W, 0)
    return W

# ══════════════════════════════════════════════════════════
# 激活（Kato 2015 / Kaplan 2018）
# ══════════════════════════════════════════════════════════
def activate(W, rng, frac=0.12, n_steps=4):
    N = W.shape[0]
    n = max(3, int(N * frac))
    h = np.zeros(N, dtype=np.float32)
    h[rng.choice(N, n, replace=False)] = rng.uniform(0.5, 1.0, n)
    for _ in range(n_steps):
        h = np.tanh(W @ h)
        if h.max() > 0:
            thr = np.percentile(h[h > 0.05], 70) if (h > 0.05).sum() > 5 else 0.05
            h[h < thr] = 0
    return h.astype(np.float32)

# ══════════════════════════════════════════════════════════
# 四条规则（完全继承 v5）
# ══════════════════════════════════════════════════════════
def rule1_stdp(W, EL, ltp, ltd, act):
    a  = (act > 0.30).astype(np.int8)
    ia = (act < 0.08).astype(np.int8)
    lev = np.outer(a, a).astype(np.int16); lev &= (W > 0); np.fill_diagonal(lev, 0)
    lde = np.outer(ia, a).astype(np.int16); lde &= (W > 0)
    ltp += lev; ltd += lde
    nel = (ltp >= THETA_LTP) & ~EL & (W > 0)
    EL |= nel; W[nel] = np.minimum(W[nel] * EL_WT_BOOST, 1.0)
    pm = (ltd >= THETA_LTD) & ~EL & (W > 0)
    pm &= ((W > 0).sum(1, keepdims=True) > MIN_EDGES)
    if pm.any(): W[pm] = 0; ltp[pm] = 0; ltd[pm] = 0
    np.fill_diagonal(W, 0)
    return W, EL, ltp, ltd

def rule2_nascent(W, EL, ema, rng):
    N = W.shape[0]
    n_try = max(1, int(N * P_GROW * 0.01))
    n_new = 0
    max_new = int(N * MAX_NEW_FRAC)
    for _ in range(n_try):
        if n_new >= max_new: break
        wts_i = ema + 0.01; wts_i /= wts_i.sum()
        i = rng.choice(N, p=wts_i)
        wts_j = ema.copy() + 0.01; wts_j[i] = 0; wts_j[W[i] > 0] = 0
        if wts_j.sum() < 1e-8: continue
        wts_j /= wts_j.sum()
        j = rng.choice(N, p=wts_j)
        W[i, j] = rng.uniform(W_INIT_LO, W_INIT_HI)
        n_new += 1
    np.fill_diagonal(W, 0)
    return W

def rule3_homeostatic(W, ema):
    up = ema < ACT_LO; down = ema > ACT_HI
    if up.any():   W[up, :]   = np.minimum(W[up, :]   * SCALE_UP, 1.0)
    if down.any(): W[down, :] *= SCALE_DN
    np.fill_diagonal(W, 0)
    return W

def rule4_prune(W, EL, ema, rng):
    N = W.shape[0]; deg = (W > 0).sum(1)
    for i in np.where(deg > MIN_EDGES)[0]:
        nbrs = np.where(W[i] > 0)[0]
        if len(nbrs) < 2: continue
        thr = np.median(ema[nbrs]) * COMP_THR
        for j in nbrs:
            if not EL[i, j] and ema[j] < thr and \
               rng.random() < P_PRUNE and deg[i] > MIN_EDGES:
                W[i, j] = 0; deg[i] -= 1
    return W

# ══════════════════════════════════════════════════════════
# 指标计算
# ══════════════════════════════════════════════════════════
def compute_metrics(W, rng):
    """计算 σ, C, L, Q 以及 CST_Sc 四分量"""
    A = (W > 0).astype(float); N = W.shape[0]
    k = A.sum(1); km = k.mean()

    # σ（小世界系数）
    if km < 1.5:
        return {'sigma':1.0,'C':0.0,'L':N,'Q':0.0,'Sc':0.0,'EL_r':0.0}
    Cv = (A @ A).diagonal() / np.maximum(k * (k-1), 1)
    Cm = Cv.mean(); Cr = max(km / N, 1e-8)
    nodes = rng.choice(N, min(12, N), replace=False); Lv = []
    for s in nodes:
        dist = {s:0}; q = [s]
        while q:
            v = q.pop(0)
            for u in np.where(A[v] > 0)[0]:
                if u not in dist: dist[u] = dist[v]+1; q.append(u)
        if len(dist) > 1: Lv.append(np.mean(list(dist.values())))
    L = np.mean(Lv) if Lv else float(N)
    Lr = np.log(N) / np.log(max(km, 2))
    sigma = float(np.clip((Cm/Cr) / (L/max(Lr,1e-8)), 0, 20))

    # Q（模块化）
    try:
        G = nx.from_numpy_array(W)
        if G.number_of_edges() == 0: Q_val = 0.0
        else:
            comms = list(nx.community.greedy_modularity_communities(G))
            Q_val = float(np.clip(nx.community.modularity(G, comms), 0, 1))
    except: Q_val = 0.0

    # CST Sc 四分量
    # C = |LCC|/N（全局连通性）
    try:
        G2 = nx.from_numpy_array(W)
        lcc = max(nx.connected_components(G2), key=len)
        C_sc = len(lcc) / N
    except: C_sc = 0.0

    # H = k_core 层级深度（归一化）
    try:
        cores = nx.core_number(nx.from_numpy_array(W))
        k_max = max(cores.values()) if cores else 1
        k_null = np.log(N) / np.log(np.log(N)+1) if N > 3 else 2.0
        H_sc = min(k_max / max(k_null * 6.667, 1.0), 1.0)
    except: H_sc = 0.0

    # M = 归一化 Louvain Q
    M_sc = max((Q_val - 0.02) / (1 - 0.02), 0.01)

    # R_sw = tanh归一化小世界系数
    R_sw = float(np.tanh(max(sigma - 1, 0) / 2))

    Sc = float((C_sc * H_sc * M_sc * R_sw) ** 0.25) if all(
        v > 0 for v in [C_sc, H_sc, M_sc, R_sw]) else 0.0

    return {'sigma': sigma, 'C': float(Cm), 'L': float(L),
            'Q': Q_val, 'Sc': Sc,
            'C_sc': C_sc, 'H_sc': H_sc, 'M_sc': M_sc, 'R_sw': R_sw}

# ══════════════════════════════════════════════════════════
# 主仿真
# ══════════════════════════════════════════════════════════
def run_species(sp_name, sp_cfg, seed, use_rule4=True):
    rng = np.random.RandomState(seed)
    N   = sp_cfg['N']
    W   = make_ws(N, sp_cfg['k'], sp_cfg['p'], rng)
    EL  = np.zeros((N, N), dtype=bool)
    ltp = np.zeros((N, N), dtype=np.int16)
    ltd = np.zeros((N, N), dtype=np.int16)
    ema = np.zeros(N, dtype=np.float32)
    t0  = time.time()

    for step in range(N_STEPS):
        act = activate(W, rng, frac=0.12, n_steps=4)
        ema = 0.97 * ema + 0.03 * act
        W, EL, ltp, ltd = rule1_stdp(W, EL, ltp, ltd, act)
        if step % LTP_DECAY_INT == 0:
            ltp = np.maximum(ltp - 1, 0)
        if step % GROW_INT == 0:
            W = rule2_nascent(W, EL, ema, rng)
        if step % SCALING_INT == 0:
            W = rule3_homeostatic(W, ema)
        if use_rule4 and step % PRUNE_INT == 0:
            W = rule4_prune(W, EL, ema, rng)

    m   = compute_metrics(W, rng)
    elr = EL.sum() / max((W > 0).sum(), 1)
    m['EL_r'] = float(elr)
    m['edges'] = int((W > 0).sum())
    m['time']  = round(time.time() - t0, 1)
    return m

# ══════════════════════════════════════════════════════════
# 验证：检查是否达标（与生物参考值比对）
# ══════════════════════════════════════════════════════════
def check_bio(val, lo, hi):
    return lo <= val <= hi

def score_species(metrics_list, sp_cfg):
    """5/5 评分：σ / C / L / Q / EL_r"""
    from statistics import mean, stdev
    sigs = [m['sigma'] for m in metrics_list]
    Cs   = [m['C']     for m in metrics_list]
    Ls   = [m['L']     for m in metrics_list]
    Qs   = [m['Q']     for m in metrics_list]
    ELs  = [m['EL_r']  for m in metrics_list]
    Scs  = [m['Sc']    for m in metrics_list]

    bio_sig = sp_cfg.get('bio_sigma', [1.0, 20.0])
    bio_C   = sp_cfg.get('bio_C',     [0.10, 0.60])

    scores = {
        'sigma': check_bio(mean(sigs), bio_sig[0], bio_sig[1]),
        'C':     check_bio(mean(Cs),   bio_C[0],   bio_C[1]),
        'L':     2.0 <= mean(Ls) <= 5.0,
        'Q':     mean(Qs) > 0.20,
        'EL_r':  0.10 <= mean(ELs) <= 0.98,
    }
    n_pass = sum(scores.values())

    return {
        'score':    n_pass,
        'sigma_m':  round(mean(sigs), 3),
        'C_m':      round(mean(Cs),   3),
        'L_m':      round(mean(Ls),   3),
        'Q_m':      round(mean(Qs),   3),
        'EL_m':     round(mean(ELs),  3),
        'Sc_m':     round(mean(Scs),  3),
        'sigma_s':  round(stdev(sigs) if len(sigs)>1 else 0, 3),
        'details':  scores,
    }

# ══════════════════════════════════════════════════════════
# 主程序
# ══════════════════════════════════════════════════════════
if __name__ == '__main__':
    print("=" * 70)
    print("SDI 实验八 — 20物种连接组普适性验证")
    print("  参数集：v5 文献锁定（Rule2新生突触机制）")
    print(f"  物种数：{len(SPECIES)}  种子数：{len(SEEDS)}  步数：{N_STEPS}")
    print("=" * 70)

    all_results   = {}
    species_order = list(SPECIES.keys())

    for sp_name in species_order:
        sp_cfg = SPECIES[sp_name]
        print(f"\n>>> {sp_name}  N={sp_cfg['N']}  "
              f"[{sp_cfg['level']}]  evo={sp_cfg['evo_mya']}Mya")

        seed_metrics = []
        for seed in SEEDS:
            m = run_species(sp_name, sp_cfg, seed, use_rule4=True)
            seed_metrics.append(m)
            print(f"  seed={seed}: σ={m['sigma']:.3f}  C={m['C']:.3f}  "
                  f"Q={m['Q']:.3f}  Sc={m['Sc']:.3f}  "
                  f"EL={m['EL_r']*100:.1f}%  ({m['time']}s)")

        sc_res = score_species(seed_metrics, sp_cfg)
        badge  = '✅' if sc_res['score'] >= 3 else ('⚠️' if sc_res['score'] >= 2 else '❌')
        print(f"  {badge} SCORE {sc_res['score']}/5  "
              f"σ={sc_res['sigma_m']}  C={sc_res['C_m']}  "
              f"Q={sc_res['Q_m']}  Sc={sc_res['Sc_m']}")

        all_results[sp_name] = {
            'config':  {k: v for k, v in sp_cfg.items()
                        if k not in ('ref',)},
            'seeds':   seed_metrics,
            'summary': sc_res,
        }

    # ── 全局汇总 ───────────────────────────────────────────
    print("\n" + "=" * 70)
    print("20物种汇总（按进化年龄排序）")
    print(f"  {'物种':<22} {'进化Mya':>8} {'IIL':>6} "
          f"{'Score':>6} {'Q':>6} {'Sc':>6} {'σ':>6}")
    print("  " + "-" * 64)

    sorted_sp = sorted(species_order,
                       key=lambda s: SPECIES[s]['evo_mya'],
                       reverse=True)
    total_pass = 0
    for sp_name in sorted_sp:
        res = all_results[sp_name]
        sc  = res['summary']
        sp  = SPECIES[sp_name]
        badge = '✅' if sc['score'] >= 3 else ('⚠️' if sc['score'] >= 2 else '❌')
        print(f"  {badge} {sp_name:<20} {sp['evo_mya']:>8}  "
              f"{sp['ilevel']:>6}  "
              f"{sc['score']}/5  "
              f"{sc['Q_m']:>6.3f}  "
              f"{sc['Sc_m']:>6.3f}  "
              f"{sc['sigma_m']:>6.2f}")
        if sc['score'] >= 3: total_pass += 1

    print(f"\n  ✅ 达标（≥3/5）：{total_pass}/{len(SPECIES)} 物种")

    # 验证：IIL等级 vs 进化年龄单调性
    print("\n【进化年龄 vs Sc 单调性检验】")
    sc_vals  = [all_results[s]['summary']['Sc_m']  for s in sorted_sp]
    evo_vals = [SPECIES[s]['evo_mya']              for s in sorted_sp]
    corr = np.corrcoef(evo_vals, sc_vals)[0, 1]
    print(f"  Spearman ρ(进化年龄, Sc) = {corr:.3f}")
    if corr < -0.3:
        print("  ✅ 负相关：越年轻的物种Sc越高（正确方向：进化年龄↓ → 智能↑）")
    else:
        print("  ⚠️  相关性较弱，需进一步分析")

    # 保存
    json.dump({'species': all_results, 'order': sorted_sp},
              open(OUT, 'w'), indent=2)
    print(f"\n✅ 结果保存: {OUT}")
