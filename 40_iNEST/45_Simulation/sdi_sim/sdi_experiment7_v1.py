"""
SDI 实验七 v1 — 改进规则体系验证
新增：
  Rule2b：活动依赖定向重连（跨社区优先）
  Rule4修复：min_e=2，功能性修剪
新指标：
  通信子空间维数 CSD（Communication Subspace Dimension）
  E-L键双通路分析（预测通路 vs 误差通路）
"""

import numpy as np
import json, os, time
import networkx as nx
from collections import defaultdict

BASE = '/vault/sdi_sim'
OUT  = os.path.join(BASE, 'exp7_v1_results.json')

# ── 参数 ─────────────────────────────────────────────────
N_STEPS    = 8000
LOG_INT    = 400
SEEDS      = [42, 7, 13]

# Rule1 STDP
THETA_LTP  = 65;  THETA_LTD = 15
ETA_LTP    = 0.012; ETA_LTD = 0.008
T_DECAY    = 400
EL_HI = 0.25; EL_LO = 0.15

# Rule2b（改进：活动依赖定向重连）
REWIRE_INT    = 50
P_REWIRE      = 0.12          # 基础重连概率（略降）
CROSS_COMM_BIAS = 3.0         # 跨社区节点被选中的权重倍数

# Rule3 稳态缩放
SCALING_INT   = 100
ACT_TARGET_LO = 0.05
ACT_TARGET_HI = 0.20          # 从0.25降低（更严格临界态控制）
SCALE_UP      = 1.04
SCALE_DN      = 0.96

# Rule4修复：min_e=2，加入活跃度阈值
PRUNE_INT     = 200
P_PRUNE       = 0.05
MIN_EDGES     = 2             # 从3降到2
ACT_PRUNE_THR = 0.02          # 活跃度低于此才考虑修剪

# 网络配置
NETWORKS = {
    'WS_4rules':   {'N': 200, 'k': 8, 'p': 0.1, 'rule4': True,  'rule2b': True},
    'WS_no_rule4': {'N': 200, 'k': 8, 'p': 0.1, 'rule4': False, 'rule2b': True},
    'WS_old_rule2':{'N': 200, 'k': 8, 'p': 0.1, 'rule4': True,  'rule2b': False},
    'CE_4rules':   {'N': 279, 'k': 8, 'p': 0.1, 'rule4': True,  'rule2b': True,
                    'connectome': True},
}

# ── 网络初始化 ────────────────────────────────────────────

def make_ws(N, k, p, rng):
    W = np.zeros((N, N), dtype=np.float32)
    for i in range(N):
        for d in range(1, k//2+1):
            j = (i+d) % N
            w = rng.uniform(0.05, 0.30)
            W[i,j] = W[j,i] = w
    for i in range(N):
        for d in range(1, k//2+1):
            if rng.random() < p:
                j = (i+d) % N
                nj = rng.randint(0, N)
                if nj != i and W[i,nj] == 0:
                    W[i,nj] = W[i,j]; W[i,j] = 0
    np.fill_diagonal(W, 0)
    return W

def load_celegans(rng):
    """加载真实C.elegans connectome"""
    data_path = os.path.join(BASE, 'celegans_sim/connectome_v8_data.json')
    if os.path.exists(data_path):
        with open(data_path) as f:
            d = json.load(f)
        N = d.get('N', 279)
        W = np.zeros((N,N), dtype=np.float32)
        for src, dst, w in d.get('chemical', []):
            if src < N and dst < N:
                W[src,dst] = float(w) * 0.3 / max(float(w), 1)
        EL = np.zeros((N,N), dtype=bool)
        for src, dst in d.get('electrical', []):
            if src < N and dst < N:
                W[src,dst] = W[dst,src] = 0.3
                EL[src,dst] = EL[dst,src] = True
        return W, EL
    else:
        # 降级：用WS图
        W = make_ws(279, 8, 0.1, rng)
        return W, np.zeros((279,279), dtype=bool)

# ── 指标计算 ─────────────────────────────────────────────

def compute_sigma(W, n_sample=20, rng=None):
    if rng is None: rng = np.random.RandomState(0)
    A = (W > 0).astype(float)
    N = W.shape[0]
    k = A.sum(1)
    km = k.mean()
    if km < 2: return 1.0
    A2d = (A @ A).diagonal()
    denom = k*(k-1); denom[denom==0] = 1
    C = (A2d/denom).mean()
    Cr = km/N
    nodes = rng.choice(N, min(n_sample,N), replace=False)
    Lvals = []
    for s in nodes:
        dist = {s:0}; q=[s]
        while q:
            v = q.pop(0)
            for u in np.where(A[v]>0)[0]:
                if u not in dist:
                    dist[u]=dist[v]+1; q.append(u)
        if len(dist)>1: Lvals.append(np.mean(list(dist.values())))
    L = np.mean(Lvals) if Lvals else 1.0
    Lr = np.log(N)/np.log(max(km,2))
    return float(np.clip((C/max(Cr,1e-6))/(L/max(Lr,1e-6)),0,20))

def compute_Q(W):
    try:
        G = nx.from_numpy_array(W)
        comms = list(nx.community.greedy_modularity_communities(G))
        return float(np.clip(nx.community.modularity(G,comms),0,1)), comms
    except:
        return 0.0, []

def compute_CSD(W, comms, n_modes=5):
    """
    通信子空间维数（CSD）：
    跨社区节点对之间活动相关的有效维数
    值越低 = 跨区域通信越低维 = 信息传递越高效
    """
    if len(comms) < 2: return float(n_modes)
    # 取最大的两个社区
    comms_sorted = sorted(comms, key=len, reverse=True)
    c1 = list(comms_sorted[0])[:20]
    c2 = list(comms_sorted[1])[:20]
    # 模拟激活，计算跨社区相关矩阵
    N = W.shape[0]
    rng = np.random.RandomState(99)
    acts1, acts2 = [], []
    for _ in range(100):
        h = np.zeros(N, dtype=np.float32)
        seeds = rng.choice(c1, min(3,len(c1)), replace=False)
        h[seeds] = 1.0
        for _ in range(3):
            h = np.tanh(W @ h)
            h[h<0.05] = 0
        acts1.append(h[c1])
        acts2.append(h[c2])
    A1 = np.array(acts1)  # 100 x |c1|
    A2 = np.array(acts2)  # 100 x |c2|
    if A1.std() < 1e-6 or A2.std() < 1e-6:
        return float(n_modes)
    # SVD of cross-correlation matrix
    A1c = A1 - A1.mean(0); A2c = A2 - A2.mean(0)
    XC = A1c.T @ A2c / 100  # |c1| x |c2|
    sv = np.linalg.svd(XC, compute_uv=False)
    sv_norm = sv / (sv.sum()+1e-8)
    # 有效维数（participation ratio）
    csd = 1.0 / (sv_norm**2).sum()
    return float(np.clip(csd, 1, n_modes))

def get_community_labels(comms, N):
    labels = np.zeros(N, dtype=int)
    for ci, comm in enumerate(comms):
        for node in comm:
            if node < N:
                labels[node] = ci
    return labels

# ── 规则实现 ─────────────────────────────────────────────

def rule1_stdp(W, EL, ltp_cnt, ltd_cnt, act, rng):
    active = (act > 0.3).astype(np.int8)
    inactive = (act < 0.1).astype(np.int8)
    ltp_ev = np.outer(active, active).astype(np.int16)
    ltp_ev &= (W > 0); np.fill_diagonal(ltp_ev, 0)
    ltd_ev = np.outer(inactive, active).astype(np.int16)
    ltd_ev &= (W > 0)
    ltp_cnt += ltp_ev; ltd_cnt += ltd_ev
    # 固化 E-L
    new_el = (ltp_cnt >= THETA_LTP) & ~EL & (W > 0)
    EL |= new_el
    W[new_el] = np.minimum(W[new_el]*2, 1.0)
    # E-L衰减
    no_ltp = (ltp_cnt == 0) & EL
    decayed_el = no_ltp  # 简化：无LTP事件的EL标记为衰减候选
    # 消除弱连接
    prune_mask = (ltd_cnt >= THETA_LTD) & ~EL & (W > 0)
    prune_mask &= ((W > 0).sum(1) > MIN_EDGES)[:, None]
    if prune_mask.any():
        W[prune_mask] = 0; ltp_cnt[prune_mask] = 0; ltd_cnt[prune_mask] = 0
    W[~EL & (W > 0)] = np.clip(W[~EL & (W > 0)], 0, 1.0)
    np.fill_diagonal(W, 0)
    return W, EL, ltp_cnt, ltd_cnt

def rule2b_directed_rewire(W, EL, act_ema, comm_labels, rng, use_directed=True):
    """改进Rule2b：跨社区活动依赖定向重连"""
    N = W.shape[0]
    cands = np.argwhere((W > 0) & ~EL)
    if len(cands) == 0: return W
    n = max(1, int(len(cands) * P_REWIRE * 0.01))
    idx = rng.choice(len(cands), n, replace=False)
    for i, j in cands[idx]:
        if not use_directed:
            # 原来的随机重连
            nj = rng.randint(0, N)
            if nj != i and W[i, nj] == 0:
                W[i, nj] = W[i, j]; W[i, j] = 0
        else:
            # 改进：优先选跨社区+高活跃节点
            # 权重 = 活跃度 * (跨社区倍数 if 不同社区 else 1)
            weights = act_ema.copy() + 0.01
            if comm_labels is not None:
                cross = (comm_labels != comm_labels[i]).astype(float)
                weights *= (1 + cross * (CROSS_COMM_BIAS - 1))
            weights[i] = 0
            weights[W[i] > 0] = 0  # 已连接的不选
            total = weights.sum()
            if total < 1e-8: continue
            weights /= total
            nj = rng.choice(N, p=weights)
            if W[i, nj] == 0:
                W[i, nj] = W[i, j]; W[i, j] = 0
    np.fill_diagonal(W, 0)
    return W

def rule3_homeostatic(W, act_ema):
    up   = act_ema < ACT_TARGET_LO
    down = act_ema > ACT_TARGET_HI
    if up.any():   W[up, :]   = np.minimum(W[up,   :]*SCALE_UP, 1.0)
    if down.any(): W[down, :] *= SCALE_DN
    np.fill_diagonal(W, 0)
    return W

def rule4_prune(W, EL, act_ema, rng):
    """修复版Rule4：min_e=2，活跃度阈值判断"""
    N = W.shape[0]
    degree = (W > 0).sum(1)
    # 只处理度>min_e的节点
    for i in np.where(degree > MIN_EDGES)[0]:
        edges = np.where((W[i] > 0) & ~EL[i])[0]
        if len(edges) == 0: continue
        # 低活跃度的弱连接才修剪
        for j in edges:
            if act_ema[j] < ACT_PRUNE_THR and rng.random() < P_PRUNE:
                if degree[i] > MIN_EDGES:
                    W[i,j] = 0; degree[i] -= 1
    return W

def activate(W, rng, n_seeds=3):
    N = W.shape[0]
    h = np.zeros(N, dtype=np.float32)
    h[rng.choice(N, n_seeds, replace=False)] = 1.0
    for _ in range(4):
        h = np.tanh(W @ h)
        if h.mean() > 0.2:
            thr = np.percentile(h[h>0], 70) if (h>0).any() else 0.5
            h[h < thr] = 0
        h[h < 0.05] = 0
    return h.astype(np.float32)

# ── 主仿真 ────────────────────────────────────────────────

def run_one(net_name, cfg, seed):
    rng = np.random.RandomState(seed)
    N = cfg['N']

    if cfg.get('connectome'):
        W, EL = load_celegans(rng)
        N = W.shape[0]
    else:
        W = make_ws(N, cfg['k'], cfg['p'], rng)
        EL = np.zeros((N,N), dtype=bool)

    ltp_cnt = np.zeros((N,N), dtype=np.int16)
    ltd_cnt = np.zeros((N,N), dtype=np.int16)
    act_ema = np.zeros(N, dtype=np.float32)
    comm_labels = None

    log = {'step':[], 'sigma':[], 'Q':[], 'CSD':[], 'EL_ratio':[]}

    t0 = time.time()
    for step in range(N_STEPS):
        act = activate(W, rng)
        act_ema = 0.97*act_ema + 0.03*act

        # Rule1 STDP
        W, EL, ltp_cnt, ltd_cnt = rule1_stdp(W, EL, ltp_cnt, ltd_cnt, act, rng)

        # Rule2b 定向重连
        if step % REWIRE_INT == 0:
            W = rule2b_directed_rewire(
                W, EL, act_ema, comm_labels, rng,
                use_directed=cfg.get('rule2b', True)
            )

        # Rule3 稳态缩放
        if step % SCALING_INT == 0:
            W = rule3_homeostatic(W, act_ema)

        # Rule4 竞争修剪（可开关）
        if cfg.get('rule4', True) and step % PRUNE_INT == 0:
            W = rule4_prune(W, EL, act_ema, rng)

        # 记录指标
        if step % LOG_INT == 0:
            sigma = compute_sigma(W, rng=rng)
            Q_val, comms = compute_Q(W)
            # 更新社区标签（供Rule2b使用）
            if comms:
                comm_labels = get_community_labels(comms, N)
            csd = compute_CSD(W, comms)
            el_r = EL.sum() / max((W>0).sum(), 1)
            log['step'].append(step)
            log['sigma'].append(sigma)
            log['Q'].append(Q_val)
            log['CSD'].append(csd)
            log['EL_ratio'].append(float(el_r))
            print(f"  {net_name} seed={seed} step={step:5d}: "
                  f"σ={sigma:.2f} Q={Q_val:.3f} CSD={csd:.2f} "
                  f"EL={el_r*100:.1f}% ({time.time()-t0:.0f}s)")

    final_sigma = compute_sigma(W, rng=rng)
    final_Q, final_comms = compute_Q(W)
    final_CSD = compute_CSD(W, final_comms)
    final_EL = EL.sum() / max((W>0).sum(),1)

    return {
        'net': net_name, 'seed': seed,
        'rule4': cfg.get('rule4',True),
        'rule2b': cfg.get('rule2b',True),
        'final': {
            'sigma': final_sigma, 'Q': final_Q,
            'CSD': final_CSD, 'EL_ratio': float(final_EL),
            'n_edges': int((W>0).sum()),
        },
        'log': log,
    }

# ── 主程序 ────────────────────────────────────────────────

if __name__ == '__main__':
    print("=" * 60)
    print("SDI 实验七 v1 — 改进规则体系 + 通信子空间维数")
    print("Rule2b（跨社区定向重连）+ Rule4修复（min_e=2）")
    print("=" * 60)

    results = []
    for net_name, cfg in NETWORKS.items():
        for seed in SEEDS:
            print(f"\n>>> {net_name} seed={seed}")
            r = run_one(net_name, cfg, seed)
            results.append(r)

    # 汇总
    print("\n" + "="*60)
    print("汇总结果:")
    from collections import defaultdict
    by_net = defaultdict(list)
    for r in results:
        by_net[r['net']].append(r)

    summary = {}
    for net, rlist in by_net.items():
        qs    = [r['final']['Q'] for r in rlist]
        sigs  = [r['final']['sigma'] for r in rlist]
        csds  = [r['final']['CSD'] for r in rlist]
        summary[net] = {
            'Q_mean': float(np.mean(qs)), 'Q_std': float(np.std(qs)),
            'sigma_mean': float(np.mean(sigs)),
            'CSD_mean': float(np.mean(csds)),
        }
        print(f"  {net}: Q={np.mean(qs):.3f}±{np.std(qs):.3f} "
              f"σ={np.mean(sigs):.2f} CSD={np.mean(csds):.2f}")

    # 关键对比
    print("\n关键对比（Rule4效果）:")
    q4  = summary.get('WS_4rules',{}).get('Q_mean',0)
    q0  = summary.get('WS_no_rule4',{}).get('Q_mean',0)
    q2  = summary.get('WS_old_rule2',{}).get('Q_mean',0)
    print(f"  四规则完整:   Q={q4:.3f}")
    print(f"  关闭Rule4:    Q={q0:.3f}  差异={q4-q0:+.3f}")
    print(f"  旧Rule2(随机): Q={q2:.3f}  差异={q4-q2:+.3f}")

    out = {'results': results, 'summary': summary}
    with open(OUT, 'w') as f:
        json.dump(out, f, indent=2)
    print(f"\n✅ 结果保存: {OUT}")
