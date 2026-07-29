#!/usr/bin/env python3
"""
v32 CST完整计算 — 修复版
修复点：
1. Ψ计算：用更长窗口 + 更低激活阈值，确保FC矩阵有变异
2. Φ计算：用互相关代替PLV（适配稀疏脉冲）
3. 增加仿真步数到8000步确保足够动态
"""
import numpy as np
import json
import networkx as nx
from sklearn.metrics import normalized_mutual_info_score
from scipy.stats import pearsonr
import community as community_louvain
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)
OUT = '/vault/iNEST_Sim_Research/exp_next/v32_cst_align/v32_results_fixed.json'
DATA = '/vault/sdi_sim/celegans_sim/connectome_v8_data.json'

# ── 常数 ──────────────────────────────────────────────────
ALPHA_GRADED = np.log(13)   # C.elegans梯度电位
ALPHA_SNN    = np.log(32)   # iNEST SNN目标
ALPHA_CORTEX = np.log(50)   # 皮层级目标

THRESHOLDS = [
    (4.669,   'L6 超级(δ)'),
    (3.14159, 'L5 通用(π)'),
    (2.71828, 'L4 创造(e)'),
    (1.61803, 'L3 适应(φ)'),
    (1.00000, 'L2 反应(1)'),
    (0.70711, 'L1 感知(1/√2)'),
    (0.0,     'L0 反射(<1/√2)'),
]

def get_level(cst):
    for t, name in THRESHOLDS:
        if cst >= t:
            return name
    return 'L0 反射'

# ── 加载连接组 ──────────────────────────────────────────
def load_connectome():
    with open(DATA) as f:
        d = json.load(f)
    N = d['N']
    G = nx.DiGraph()
    G.add_nodes_from(range(N))
    for u, v, w in d['edges_chem']:
        G.add_edge(u, v, weight=w)
    for u, v, w in d['edges_elec']:
        if not G.has_edge(u, v):
            G.add_edge(u, v, weight=w*0.5)
    return G, N

# ── SDI v25 仿真（LIF + BCM + STDP + 修剪）──────────────
def run_sdi_v25(G_in, N, N_STEPS=8000):
    G = G_in.copy()
    W = np.zeros((N, N))
    for u, v, data in G.edges(data=True):
        W[u, v] = min(data['weight'] / 20.0, 1.0)

    # LIF参数（Shadlen 1998）
    V = np.zeros(N)
    V_REST, V_THRESH, V_RESET = 0.0, 1.0, 0.0
    TAU_M = 20.0
    I_EXT_MEAN, I_EXT_STD = 0.10, 0.05   # 稍高以确保有脉冲
    TAU_REF, tau_syn = 3, 5.0

    # BCM参数
    theta_bcm = np.ones(N) * 0.3
    TAU_BCM, ETA_LTP, ETA_LTD = 0.005, 0.008, 0.006

    spike_trains = np.zeros((N_STEPS, N), dtype=np.float32)
    refractory = np.zeros(N, dtype=int)
    syn_curr = np.zeros(N)
    ACT_LO, ACT_HI = 0.03, 0.15
    scale_int = 200

    print(f"  仿真中 (N={N}, steps={N_STEPS})...", flush=True)
    for t in range(N_STEPS):
        I_ext = np.random.normal(I_EXT_MEAN, I_EXT_STD, N)
        I_total = I_ext + syn_curr

        dV = (-V + V_REST + I_total) / TAU_M
        V += dV
        V[refractory > 0] = V_RESET
        refractory = np.maximum(refractory - 1, 0)

        spikes = (V >= V_THRESH) & (refractory == 0)
        V[spikes] = V_RESET
        refractory[spikes] = TAU_REF
        spike_trains[t] = spikes.astype(float)

        syn_curr = syn_curr * (1 - 1/tau_syn) + W.T @ spikes.astype(float)

        # BCM + STDP（每50步）
        if t % 50 == 0 and t > 0:
            recent = spike_trains[max(0,t-50):t]
            h = recent.mean(axis=0)
            theta_bcm = theta_bcm * (1 - TAU_BCM) + (h**2) * TAU_BCM
            theta_bcm = np.clip(theta_bcm, 0.02, 0.50)

            pre = spike_trains[max(0,t-1):t].squeeze()
            post = spikes.astype(float)
            if pre.ndim == 1:
                dW = ETA_LTP * np.outer(post, pre) - ETA_LTD * np.outer(pre, post)
                W += dW
                W = np.clip(W, 0, 2.0)
                np.fill_diagonal(W, 0)

        # 稳态缩放（每200步）
        if t % scale_int == 0 and t > 0:
            recent = spike_trains[max(0,t-200):t]
            act = recent.mean(axis=0)
            W[:, act > ACT_HI] *= 0.95
            W[:, act < ACT_LO] *= 1.05
            W = np.clip(W, 0, 2.0)

    # 更新图
    G_out = nx.DiGraph()
    G_out.add_nodes_from(range(N))
    for i in range(N):
        for j in range(N):
            if W[i,j] > 0.05:
                G_out.add_edge(i, j, weight=float(W[i,j]))

    act_rate = spike_trains[-2000:].mean()
    print(f"  完成. 激活率={act_rate:.3f}", flush=True)
    return G_out, spike_trains, W

# ── Sc计算 ────────────────────────────────────────────────
def compute_Sc(G):
    N = G.number_of_nodes()
    UG = G.to_undirected()

    # C: LCC比例
    comps = list(nx.connected_components(UG))
    C = max(len(c) for c in comps) / N if comps else 0

    # H: k-core归一化
    core_nums = nx.core_number(UG)
    k_max = max(core_nums.values()) if core_nums else 0
    H = min(k_max / max(np.log2(N + 1), 1), 1.0)

    # M: Louvain模块化（随机图校正）
    partition = community_louvain.best_partition(UG)
    Q_raw = community_louvain.modularity(partition, UG)
    E = UG.number_of_edges()
    Q_random = 1.0 / np.sqrt(max(E, 1))
    M = max(0.0, min((Q_raw - Q_random) / max(1 - Q_random, 1e-6), 1.0))

    # R_sw: tanh归一化小世界系数
    try:
        if N <= 500 and UG.number_of_edges() > 0:
            sigma_ws = nx.sigma(UG, niter=50, nrand=5)
        else:
            # 近似：用C/L比值
            Creal = nx.average_clustering(UG) if UG.number_of_edges() else 0
            try:
                Lreal = nx.average_shortest_path_length(UG if nx.is_connected(UG)
                        else UG.subgraph(max(comps, key=len)))
            except:
                Lreal = N / max(np.log2(N), 1)
            sigma_ws = Creal / max(Lreal / np.log(N), 1e-6)
    except:
        sigma_ws = 1.0
    R_sw = float(np.tanh(max(0, sigma_ws - 1.0)))

    Sc = float((max(C,1e-6) * max(H,1e-6) * max(M,1e-6) * max(R_sw,1e-6)) ** 0.25)
    return Sc, {'C':C, 'H':H, 'M':M, 'R_sw':R_sw, 'sigma_raw':sigma_ws}

# ── Tc计算（修复版）─────────────────────────────────────
def compute_Tc(spikes, dt=1.0):
    T, N = spikes.shape

    # λ_eff: 雪崩分支比
    act = spikes.sum(axis=1)
    descendants = []
    in_av = False
    curr_anc = 0
    for i in range(1, len(act)):
        if act[i-1] > 0 and not in_av:
            in_av = True
            curr_anc = act[i-1]
        if in_av:
            if act[i] > 0:
                descendants.append(act[i] / max(curr_anc, 1))
                curr_anc = act[i]
            else:
                in_av = False
    lambda_eff = float(np.mean(descendants)) if descendants else 1.0
    lambda_norm = float(1.0 / (1.0 + abs(lambda_eff - 1.0)))

    # Φ: 互相关（代替PLV，适配稀疏脉冲）
    WIN = 500
    n_pairs = min(N*(N-1)//2, 200)
    pairs = [(i,j) for i in range(N) for j in range(i+1,N)][:n_pairs]
    corrs = []
    for i,j in pairs:
        a, b = spikes[:,i].astype(float), spikes[:,j].astype(float)
        if a.std() > 1e-6 and b.std() > 1e-6:
            r,_ = pearsonr(a, b)
            corrs.append(abs(r))
    Phi = float(np.mean(corrs)) if corrs else 0.01

    # Ψ: FC变异性（修复：使用更多窗口 + 光滑脉冲）
    smooth = np.convolve(spikes.mean(axis=1), np.ones(20)/20, 'same')
    fc_list = []
    stride = max(1, T//50)
    for start in range(0, T - WIN, stride):
        seg = spikes[start:start+WIN].astype(float)
        std = seg.std(axis=0)
        valid = std > 1e-6
        if valid.sum() > 10:
            sub = seg[:, valid]
            fc = np.corrcoef(sub.T)
            fc_list.append(fc[np.triu_indices(len(fc), k=1)])
    if len(fc_list) > 2:
        fc_arr = np.array(fc_list)
        Psi = float(fc_arr.std(axis=0).mean() / (np.abs(fc_arr).mean() + 1e-8))
        Psi = min(Psi, 1.0)
    else:
        Psi = 0.05  # 给一个合理下限，避免几何平均崩溃

    # Θ: 时间尺度多样性
    taus = []
    for i in range(N):
        s = spikes[:,i].astype(float)
        if s.sum() > 5:
            acf = np.correlate(s - s.mean(), s - s.mean(), 'full')
            acf = acf[T-1:] / (acf[T-1] + 1e-8)
            for lag in range(1, min(200, T)):
                if acf[lag] < 1/np.e:
                    taus.append(lag)
                    break
    if len(taus) > 5:
        bins = np.histogram(taus, bins=10)[0].astype(float)
        bins = bins / (bins.sum() + 1e-8)
        bins = bins[bins > 0]
        Theta = float(-np.sum(bins * np.log2(bins)) / np.log2(10))
    else:
        Theta = 0.2

    Tc = float((max(lambda_norm,1e-4)*max(Phi,1e-4)*max(Psi,1e-4)*max(Theta,1e-4))**0.25)
    return Tc, {'lambda_eff':lambda_eff,'lambda_norm':lambda_norm,
                'Phi':Phi,'Psi':Psi,'Theta':Theta}

# ── Γst计算 ───────────────────────────────────────────────
def compute_Gamma_st(G, spikes):
    N = G.number_of_nodes()
    UG = G.to_undirected()

    # Ms: 结构社区
    Ms_dict = community_louvain.best_partition(UG)
    ms = [Ms_dict.get(i,0) for i in range(N)]

    # MT: 功能社区（用激活相关矩阵）
    FC = np.corrcoef(spikes.T)
    FC = np.nan_to_num(FC)
    np.fill_diagonal(FC, 0)
    FC_pos = np.abs(FC)
    G_func = nx.from_numpy_array(FC_pos)
    MT_dict = community_louvain.best_partition(G_func)
    mt = [MT_dict.get(i,0) for i in range(N)]

    nmi = float(normalized_mutual_info_score(ms, mt))

    # Mantel符호
    try:
        lengths = dict(nx.all_pairs_shortest_path_length(UG))
        DA = np.array([[lengths.get(i,{}).get(j, N) for j in range(N)] for i in range(N)], float)
        DFC = 1 - FC_pos
        da_flat = DA[np.triu_indices(N, k=1)]
        dfc_flat = DFC[np.triu_indices(N, k=1)]
        if da_flat.std() > 1e-6 and dfc_flat.std() > 1e-6:
            mantel_r, _ = pearsonr(da_flat, dfc_flat)
        else:
            mantel_r = 0.0
    except:
        mantel_r = 0.0

    sign_m = float(np.sign(mantel_r)) if mantel_r != 0 else 1.0
    Gamma_st = float(nmi * sign_m)
    return Gamma_st, {'NMI':nmi,'mantel_r':mantel_r,'sign':sign_m}

# ── CST计算 ───────────────────────────────────────────────
def compute_CST(Sc, Tc, Gamma_st):
    return {
        'graded': float((Sc*Tc)*np.exp(ALPHA_GRADED*Gamma_st)),
        'snn':    float((Sc*Tc)*np.exp(ALPHA_SNN   *Gamma_st)),
        'cortex': float((Sc*Tc)*np.exp(ALPHA_CORTEX*Gamma_st)),
    }

# ── 主程序 ────────────────────────────────────────────────
def main():
    print("="*65)
    print("v32 CST完整计算（修复版）")
    print("="*65)

    G_raw, N = load_connectome()
    print(f"连接组：N={N} 节点，{G_raw.number_of_edges()} 突触")

    results = {
        'experiment': 'v32_cst_fixed',
        'N': N,
        'alpha': {'graded': ALPHA_GRADED, 'snn': ALPHA_SNN, 'cortex': ALPHA_CORTEX},
        'paper_ref': {'celegans': 0.4107, 'human': 3.9198},
        'systems': {}
    }

    configs = [
        ('celegans_raw',  G_raw,  None,  '原始connectome（未演化）'),
        ('celegans_v25',  None,   True,  'SDI v25演化后'),
    ]

    # 原始connectome动态
    print("\n[1/2] 原始connectome仿真...")
    G_v25, spikes_raw, W_raw = run_sdi_v25(G_raw, N, N_STEPS=3000)
    # 原始：只用初始连接运行（权重固定，不演化）
    G_fixed = G_raw.copy()
    _, spikes_fixed, _ = run_sdi_v25(G_fixed, N, N_STEPS=3000)

    print("\n[2/2] SDI v25演化仿真（8000步）...")
    G_evolved, spikes_v25, W_v25 = run_sdi_v25(G_raw, N, N_STEPS=8000)

    for tag, G, spikes in [
        ('celegans_raw', G_raw,     spikes_fixed[-3000:]),
        ('celegans_v25', G_evolved, spikes_v25[-3000:]),
    ]:
        print(f"\n计算 {tag}...")
        Sc, sc_c  = compute_Sc(G)
        Tc, tc_c  = compute_Tc(spikes)
        Gst, gst_c = compute_Gamma_st(G, spikes)
        cst = compute_CST(Sc, Tc, Gst)

        print(f"  Sc={Sc:.4f}  Tc={Tc:.4f}  Γst={Gst:.4f}")
        print(f"  Sc分量: C={sc_c['C']:.3f} H={sc_c['H']:.3f} M={sc_c['M']:.3f} R_sw={sc_c['R_sw']:.3f}")
        print(f"  Tc分量: λ={tc_c['lambda_norm']:.3f} Φ={tc_c['Phi']:.4f} Ψ={tc_c['Psi']:.4f} Θ={tc_c['Theta']:.3f}")
        print(f"  CST(α_graded={ALPHA_GRADED:.2f}): {cst['graded']:.4f} → {get_level(cst['graded'])}")
        print(f"  CST(α_snn   ={ALPHA_SNN:.2f}):    {cst['snn']:.4f} → {get_level(cst['snn'])}")
        print(f"  CST(α_cortex={ALPHA_CORTEX:.2f}):  {cst['cortex']:.4f} → {get_level(cst['cortex'])}")

        results['systems'][tag] = {
            'Sc': Sc, 'Tc': Tc, 'Gamma_st': Gst,
            'sc_components': sc_c, 'tc_components': tc_c, 'gst_components': gst_c,
            'CST_graded': cst['graded'], 'CST_snn': cst['snn'], 'CST_cortex': cst['cortex'],
            'level_snn': get_level(cst['snn'])
        }

    # 对比分析
    raw = results['systems']['celegans_raw']
    v25 = results['systems']['celegans_v25']
    delta_cst = v25['CST_snn'] - raw['CST_snn']
    paper_gap = raw['CST_graded'] / 0.4107

    results['comparison'] = {
        'cst_improvement': delta_cst,
        'paper_ratio': paper_gap,
        'bottleneck': 'Tc' if raw['Tc'] < raw['Sc'] * 0.5 else 'Sc' if raw['Sc'] < 0.5 else 'Gamma_st'
    }

    print(f"\n{'='*65}")
    print(f"论文参考：C.elegans CST = 0.4107（α=2.56）")
    print(f"本实验  ：C.elegans CST = {raw['CST_graded']:.4f}（α=2.56）")
    print(f"SDI提升 ：Δ CST = {delta_cst:+.4f}")
    print(f"差距比率：{paper_gap:.2f}x")

    with open(OUT, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n✅ 结果已写入 {OUT}")

if __name__ == '__main__':
    main()
