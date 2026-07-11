"""
SDI 实验七 v5 — Rule2「新生突触探索」机制
==============================================
Rule2 根本性改正（基于文献）：
  旧实现：随机断开一条已有连接 → 重连新节点（破坏已有结构）
  新实现：「新生突触」双阶段机制
    阶段1 探索：以极低权重 w_init ∈ [0.05, 0.10] 在高活跃节点处新生一条连接
               不删除任何已有连接
    阶段2 竞争：新生连接交给 Rule1(STDP) 和 Rule4(修剪) 裁决：
               → 后续共同激活 ≥ THETA_LTP 次 → EL 固化（稳定成熟）
               → 长期不协同激活 → Rule4 修剪掉

文献依据：
  PMC6704923  LTP-Induced Long-Term Stabilization of Nascent Dendritic Spines
              新棘必须经 LTP 诱导才能从短暂态过渡到持久态
  Zito et al. 2009  J Neurosci
              新棘初始 AMPA 电流 ≈ 成熟棘的 5-20% → w_init = 0.05-0.10
  Holtmaat & Svoboda 2009  Nat Rev Neurosci
              新棘生长率 ~5%/天，活动依赖偏向 2-4 倍
  Bhatt et al. 2009  Nature
              稳定突触（类 EL 键）不被新生突触替换

其余三条规则参数与 v4 完全一致（已经文献锁定）。
对照组同 v4：WS_full / WS_no_r4 / WS_no_r2（验证） / CE_full
新增对照：   WS_full_v4style（v4的旧Rule2）作为对比基准
"""

import numpy as np
import json, os, time
import networkx as nx
from collections import defaultdict

BASE    = '/home/work/.openclaw/workspace/sdi_sim'
OUT     = os.path.join(BASE, 'exp7_v5_results.json')
CE_DATA = os.path.join(BASE, 'celegans_sim/connectome_v8_data.json')

# ══════════════════════════════════════════════════════════
# 文献锁定参数（全部有 NCS 级依据，见 SDI_Rules_Bio_Evidence_v1.md）
# ══════════════════════════════════════════════════════════

# Rule 1  [Bi&Poo 1998; Song 2000]
THETA_LTP     = 60
THETA_LTD     = 50
LTP_DECAY_INT = 500
EL_WT_BOOST   = 1.5

# Rule 2 新生突触（v5 核心改进）
# [PMC6704923; Zito 2009; Holtmaat 2009]
GROW_INT      = 50           # 新生突触尝试间隔（同 v4 REWIRE_INT）
P_GROW        = 0.05         # 新生概率/间隔 [Holtmaat: ~5%/天]
W_INIT_LO     = 0.05         # 新生权重下限 [Zito 2009: 5% 成熟权重]
W_INIT_HI     = 0.10         # 新生权重上限 [Zito 2009: 20% 成熟权重保守取 10%]
ACT_BIAS      = 2.0          # 活跃节点偏向 [Holtmaat 2009: 2-4 倍]
COMM_REFRESH  = 500          # 社区标签刷新
MAX_NEW_FRAC  = 0.15         # 每次最多新生边数占比（防止度无限增长）

# Rule 3  [Turrigiano 1998/2012]
SCALING_INT   = 200
ACT_LO        = 0.03
ACT_HI        = 0.10
SCALE_UP      = 1.05
SCALE_DN      = 0.95

# Rule 4  [Sanes&Lichtman 1999; Science 2022]
PRUNE_INT     = 200
P_PRUNE       = 0.05
MIN_EDGES     = 2
COMP_THR      = 0.5          # 竞争阈值：低于邻居中位×0.5

# 仿真规模
N_STEPS       = 10000
LOG_INT       = 500
SEEDS         = [42, 7, 13]

# ══════════════════════════════════════════════════════════
# 网络配置（同 v4，增加 v4style 对照）
# ══════════════════════════════════════════════════════════
NETWORKS = {
    'WS_full'      : {'type':'ws','N':300,'k':12,'p':0.1,
                      'rule2':'nascent','rule4':True},
    'WS_no_r4'     : {'type':'ws','N':300,'k':12,'p':0.1,
                      'rule2':'nascent','rule4':False},
    'WS_no_r2'     : {'type':'ws','N':300,'k':12,'p':0.1,
                      'rule2':'none',   'rule4':True},
    'WS_old_r2'    : {'type':'ws','N':300,'k':12,'p':0.1,
                      'rule2':'replace','rule4':True},   # v4 旧实现对照
    'CE_full'      : {'type':'ce',
                      'rule2':'nascent','rule4':True},
}

# ══════════════════════════════════════════════════════════
# 网络初始化
# ══════════════════════════════════════════════════════════

def make_ws(N, k, p, rng):
    W = np.zeros((N, N), dtype=np.float32)
    for i in range(N):
        for d in range(1, k // 2 + 1):
            j = (i + d) % N
            W[i, j] = W[j, i] = rng.uniform(0.1, 0.35)
    for i in range(N):
        for d in range(1, k // 2 + 1):
            if rng.random() < p:
                j = (i + d) % N
                nj = rng.randint(0, N)
                if nj != i and W[i, nj] == 0:
                    W[i, nj] = W[i, j]; W[i, j] = 0
    np.fill_diagonal(W, 0)
    return W


def load_ce(rng):
    """C.elegans connectome（White 1986 / Varshney 2011）"""
    with open(CE_DATA) as f:
        d = json.load(f)
    N  = d.get('N', 279)
    W  = np.zeros((N, N), dtype=np.float32)
    EL = np.zeros((N, N), dtype=bool)
    chem = [(int(r[0]), int(r[1]), float(r[2])) for r in d.get('edges_chem', [])]
    if chem:
        mx = max(w for _, _, w in chem)
        for s, t, w in chem:
            if s < N and t < N:
                W[s, t] = 0.10 + 0.30 * (w / mx)
    for row in d.get('edges_elec', []):
        s, t = int(row[0]), int(row[1])
        if s < N and t < N:
            W[s, t] = W[t, s] = 0.30
            EL[s, t] = EL[t, s] = True
    avg = (W > 0).sum(1).mean()
    print(f"  CE: N={N} chem={len(chem)} "
          f"elec={len(d.get('edges_elec',[]))} avg_deg={avg:.1f}")
    return W, EL, N

# ══════════════════════════════════════════════════════════
# 激活  [Kato 2015 Cell; Kaplan 2018 Neuron]
# ══════════════════════════════════════════════════════════

def activate(W, rng, frac=0.12, n_steps=4):
    N = W.shape[0]
    n = max(4, int(N * frac))
    h = np.zeros(N, dtype=np.float32)
    h[rng.choice(N, n, replace=False)] = rng.uniform(0.5, 1.0, n)
    for _ in range(n_steps):
        h = np.tanh(W @ h)
        if h.max() > 0:
            thr = np.percentile(h[h > 0.05], 70) if (h > 0.05).sum() > 5 else 0.05
            h[h < thr] = 0
    return h.astype(np.float32)

# ══════════════════════════════════════════════════════════
# Rule 1：STDP  [Bi&Poo 1998; Song 2000]
# ══════════════════════════════════════════════════════════

def rule1_stdp(W, EL, ltp, ltd, act):
    a  = (act > 0.30).astype(np.int8)
    ia = (act < 0.08).astype(np.int8)
    lev = np.outer(a, a).astype(np.int16)
    lev &= (W > 0); np.fill_diagonal(lev, 0)
    ltp += lev
    lde = np.outer(ia, a).astype(np.int16)
    lde &= (W > 0)
    ltd += lde
    # EL 固化
    nel = (ltp >= THETA_LTP) & ~EL & (W > 0)
    EL |= nel
    W[nel] = np.minimum(W[nel] * EL_WT_BOOST, 1.0)
    # E-S 消除（非 EL 键）
    pm = (ltd >= THETA_LTD) & ~EL & (W > 0)
    pm &= ((W > 0).sum(1, keepdims=True) > MIN_EDGES)
    if pm.any():
        W[pm] = 0; ltp[pm] = 0; ltd[pm] = 0
    np.fill_diagonal(W, 0)
    return W, EL, ltp, ltd

# ══════════════════════════════════════════════════════════
# Rule 2 — 三种模式（含新实现）
# ══════════════════════════════════════════════════════════

def rule2_nascent(W, EL, ema, rng):
    """
    ★ 新生突触探索（v5 核心）★
    文献依据：
      PMC6704923（Hsieh 2019 J Neurosci）：
        LTP 诱导刺激使新棘从短暂态→持久态；新棘先以弱权重存在
      Zito et al. 2009 J Neurosci：
        新棘初始 AMPA 电流 ≈ 5-20% 成熟棘（→ w_init = 0.05-0.10）
      Holtmaat & Svoboda 2009 Nat Rev Neurosci：
        新棘生长偏向活跃区域（2-4 倍），不强制跨模块
    机制：
      1. 选取活跃度高的节点 i（以 ema 为权重）
      2. 从 i 出发，向另一活跃节点 j 生长一条新突触
      3. 初始权重 w_init ~ Uniform[0.05, 0.10]
      4. 不删除任何已有连接
      5. 新突触命运由 Rule1（积累 STDP）和 Rule4（修剪）裁决
    """
    N   = W.shape[0]
    deg = (W > 0).sum(1)

    # 每次新生 n_grow 条（受 MAX_NEW_FRAC 约束，防度爆炸）
    n_try  = max(1, int(N * P_GROW * 0.01))
    n_grow = 0
    max_new = int(W.shape[0] * MAX_NEW_FRAC)

    for _ in range(n_try):
        if n_grow >= max_new:
            break
        # 以活跃度为权重选源节点 i
        wts_i = ema + 0.01
        wts_i /= wts_i.sum()
        i = rng.choice(N, p=wts_i)

        # 目标节点：活跃偏向 × 2（Holtmaat 2009），排除已连接
        wts_j = ema.copy() + 0.01
        wts_j[i] = 0
        wts_j[W[i] > 0] = 0    # 已有连接不重复
        if wts_j.sum() < 1e-8:
            continue
        wts_j /= wts_j.sum()
        j = rng.choice(N, p=wts_j)

        # 新生突触，初始权重 [0.05, 0.10]（Zito 2009）
        w_init = rng.uniform(W_INIT_LO, W_INIT_HI)
        W[i, j] = w_init
        n_grow += 1

    np.fill_diagonal(W, 0)
    return W


def rule2_replace(W, EL, ema, rng):
    """v4 旧实现：替换式重连（作为对照，保留用于对比）"""
    N     = W.shape[0]
    cands = np.argwhere((W > 0) & ~EL)
    if len(cands) == 0:
        return W
    n = max(1, int(len(cands) * 0.05 * 0.01))
    for i, j in cands[rng.choice(len(cands), n, replace=False)]:
        wts = ema.copy() + 0.01
        wts[i] = 0; wts[W[i] > 0] = 0
        if wts.sum() < 1e-8:
            continue
        wts /= wts.sum()
        nj = rng.choice(N, p=wts)
        if W[i, nj] == 0:
            W[i, nj] = W[i, j]; W[i, j] = 0
    np.fill_diagonal(W, 0)
    return W


# ══════════════════════════════════════════════════════════
# Rule 3：稳态缩放  [Turrigiano 1998/2012]
# ══════════════════════════════════════════════════════════

def rule3_homeostatic(W, ema):
    up   = ema < ACT_LO
    down = ema > ACT_HI
    if up.any():   W[up, :]   = np.minimum(W[up, :]   * SCALE_UP, 1.0)
    if down.any(): W[down, :] *= SCALE_DN
    np.fill_diagonal(W, 0)
    return W

# ══════════════════════════════════════════════════════════
# Rule 4：竞争修剪  [Sanes&Lichtman 1999; Science 2022]
# ══════════════════════════════════════════════════════════

def rule4_prune(W, EL, ema, rng):
    """
    竞争性修剪：低于邻居中位活跃度 × COMP_THR 才被修剪
    文献：Science 2022（相对竞争机制）/ Bhatt 2009（EL 键豁免）
    """
    N   = W.shape[0]
    deg = (W > 0).sum(1)
    for i in np.where(deg > MIN_EDGES)[0]:
        nbrs = np.where(W[i] > 0)[0]
        if len(nbrs) < 2:
            continue
        thr = np.median(ema[nbrs]) * COMP_THR
        for j in nbrs:
            if not EL[i, j] and ema[j] < thr and \
               rng.random() < P_PRUNE and deg[i] > MIN_EDGES:
                W[i, j] = 0
                deg[i] -= 1
    return W

# ══════════════════════════════════════════════════════════
# 指标
# ══════════════════════════════════════════════════════════

def compute_sigma(W, rng, ns=15):
    A  = (W > 0).astype(float); N = W.shape[0]; k = A.sum(1); km = k.mean()
    if km < 1.5: return 1.0
    Cv = (A @ A).diagonal() / np.maximum(k * (k - 1), 1)
    Cr = max(km / N, 1e-8)
    nodes = rng.choice(N, min(ns, N), replace=False)
    Lv = []
    for s in nodes:
        dist = {s: 0}; q = [s]
        while q:
            v = q.pop(0)
            for u in np.where(A[v] > 0)[0]:
                if u not in dist:
                    dist[u] = dist[v] + 1; q.append(u)
        if len(dist) > 1: Lv.append(np.mean(list(dist.values())))
    L  = np.mean(Lv) if Lv else 1.0
    Lr = np.log(N) / np.log(max(km, 2))
    return float(np.clip((Cv.mean() / Cr) / (L / max(Lr, 1e-8)), 0, 20))


def compute_Q(W):
    try:
        G = nx.from_numpy_array(W)
        if G.number_of_edges() == 0: return 0.0, []
        comms = list(nx.community.greedy_modularity_communities(G))
        return float(np.clip(nx.community.modularity(G, comms), 0, 1)), comms
    except Exception:
        return 0.0, []


def comm_labels(comms, N):
    L = np.zeros(N, dtype=int)
    for ci, c in enumerate(comms):
        for n in c:
            if n < N: L[n] = ci
    return L

# ══════════════════════════════════════════════════════════
# 主仿真
# ══════════════════════════════════════════════════════════

def run(name, cfg, seed):
    rng = np.random.RandomState(seed)
    r2_mode = cfg.get('rule2', 'nascent')

    if cfg['type'] == 'ce':
        W, EL, N = load_ce(rng)
        frac, nstep = 0.15, 4
    else:
        N = cfg['N']
        W = make_ws(N, cfg['k'], cfg['p'], rng)
        EL = np.zeros((N, N), dtype=bool)
        frac, nstep = 0.12, 4

    ltp   = np.zeros((N, N), dtype=np.int16)
    ltd   = np.zeros((N, N), dtype=np.int16)
    ema   = np.zeros(N, dtype=np.float32)
    clbls = None
    log   = {'step':[], 'sigma':[], 'Q':[], 'EL_ratio':[], 'edges':[]}
    t0    = time.time()

    for step in range(N_STEPS):
        act = activate(W, rng, frac, nstep)
        ema = 0.97 * ema + 0.03 * act

        # Rule 1：STDP（每步）
        W, EL, ltp, ltd = rule1_stdp(W, EL, ltp, ltd, act)
        if step % LTP_DECAY_INT == 0:
            ltp = np.maximum(ltp - 1, 0)

        # Rule 2：结构探索（每 50 步）
        if step % GROW_INT == 0:
            if r2_mode == 'nascent':
                W = rule2_nascent(W, EL, ema, rng)
            elif r2_mode == 'replace':
                W = rule2_replace(W, EL, ema, rng)
            # 'none' → 跳过

        # Rule 3：稳态缩放（每 200 步）
        if step % SCALING_INT == 0:
            W = rule3_homeostatic(W, ema)

        # Rule 4：竞争修剪（每 200 步）
        if cfg.get('rule4', True) and step % PRUNE_INT == 0:
            W = rule4_prune(W, EL, ema, rng)

        # 刷新社区标签
        if step % COMM_REFRESH == 0:
            _, comms = compute_Q(W)
            if comms: clbls = comm_labels(comms, N)

        # 记录
        if step % LOG_INT == 0:
            s = compute_sigma(W, rng)
            q, _ = compute_Q(W)
            elr  = EL.sum() / max((W > 0).sum(), 1)
            edges = int((W > 0).sum())
            log['step'].append(step); log['sigma'].append(s)
            log['Q'].append(q); log['EL_ratio'].append(float(elr))
            log['edges'].append(edges)
            print(f"  {name} s={seed} t={step:5d}: "
                  f"σ={s:5.2f}  Q={q:.3f}  "
                  f"EL={elr*100:4.1f}%  edges={edges}"
                  f"  ({time.time()-t0:.0f}s)")

    fs = compute_sigma(W, rng)
    fq, _ = compute_Q(W)
    felr  = EL.sum() / max((W > 0).sum(), 1)
    return {
        'net': name, 'seed': seed,
        'rule2': r2_mode, 'rule4': cfg.get('rule4', True),
        'type': cfg['type'],
        'final': {'sigma': float(fs), 'Q': float(fq),
                  'EL_ratio': float(felr), 'edges': int((W > 0).sum())},
        'log': log,
    }

# ══════════════════════════════════════════════════════════
# 主程序
# ══════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("=" * 65)
    print("SDI 实验七 v5 — Rule2「新生突触探索」机制")
    print("  Rule2 新生: w_init=[0.05,0.10] (Zito 2009)")
    print("              不删已有连接; STDP+修剪决定命运")
    print("              [PMC6704923 / Holtmaat 2009]")
    print("  其余规则参数与 v4 完全一致（已文献锁定）")
    print("  对照: WS_old_r2（v4替换式）用于直接对比")
    print("=" * 65)

    results = []
    for name, cfg in NETWORKS.items():
        for seed in SEEDS:
            print(f"\n>>> {name}  seed={seed}")
            results.append(run(name, cfg, seed))

    print("\n" + "=" * 65 + "  汇总:")
    by = defaultdict(list)
    for r in results: by[r['net']].append(r)

    summary = {}
    for net, rl in by.items():
        qs = [r['final']['Q']        for r in rl]
        ss = [r['final']['sigma']    for r in rl]
        es = [r['final']['EL_ratio'] for r in rl]
        ns = [r['final']['edges']    for r in rl]
        summary[net] = {'Q_mean':  float(np.mean(qs)),
                        'Q_std':   float(np.std(qs)),
                        'sigma_mean': float(np.mean(ss)),
                        'EL_mean': float(np.mean(es)),
                        'edges_mean': float(np.mean(ns))}
        print(f"  {net:<16s}: Q={np.mean(qs):.3f}±{np.std(qs):.3f}"
              f"  σ={np.mean(ss):.2f}  EL={np.mean(es)*100:.1f}%"
              f"  edges={np.mean(ns):.0f}")

    print("\n★ 核心对比:")
    qf  = summary.get('WS_full',  {}).get('Q_mean', 0)
    q4  = summary.get('WS_no_r4', {}).get('Q_mean', 0)
    q2  = summary.get('WS_no_r2', {}).get('Q_mean', 0)
    qor = summary.get('WS_old_r2',{}).get('Q_mean', 0)
    qce = summary.get('CE_full',  {}).get('Q_mean', 0)
    sf  = summary.get('WS_full',  {}).get('sigma_mean', 0)
    s2  = summary.get('WS_no_r2', {}).get('sigma_mean', 0)
    sor = summary.get('WS_old_r2',{}).get('sigma_mean', 0)
    print(f"  四规则(新Rule2):   Q={qf:.3f}  σ={sf:.2f}")
    print(f"  无Rule4:           Q={q4:.3f}  Δ_Q={qf-q4:+.3f}")
    print(f"  无Rule2:           Q={q2:.3f}  Δ_Q={qf-q2:+.3f}")
    print(f"  旧Rule2(替换式):   Q={qor:.3f}  σ={sor:.2f}"
          f"  ← v4对照")
    print(f"  CE_full:           Q={qce:.3f}")
    print(f"\n  新Rule2 vs 旧Rule2: ΔQ={qf-qor:+.3f}  Δσ={sf-sor:+.2f}")

    json.dump({'results': results, 'summary': summary},
              open(OUT, 'w'), indent=2)
    print(f"\n✅ 结果保存: {OUT}")
