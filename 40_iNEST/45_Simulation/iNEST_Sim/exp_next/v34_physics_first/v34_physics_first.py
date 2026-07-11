#!/usr/bin/env python3
"""
v34实验：物理第一性 — 能量极小化驱动智能涌现
目标：CST从1.27→1.618（L3适应 φ）

物理第一性三支柱：
1. 最小自由能（Friston FEP）：每个节点最小化变分自由能 F = E[log p(h)] - H[q]
2. 最小作用量（Hamilton原理）：突触演化路径使作用量 S = ∫L dt 最小
3. 局部自组织 → 全局智能涌现：无全局控制器，仅局部能量梯度

关键：用能量E作为第一抓手
  - 突触权重W_ij的演化 = -∂F/∂W_ij（自由能梯度下降）
  - Γst = 结构-功能对齐度 = 全局自由能的宏观阶参数
"""
import numpy as np, json, networkx as nx
from sklearn.metrics import normalized_mutual_info_score
from scipy.stats import pearsonr
import community as community_louvain, warnings, os
warnings.filterwarnings('ignore')
np.random.seed(42)

DATA = '/home/work/.openclaw/workspace/sdi_sim/celegans_sim/connectome_v8_data.json'
OUT  = '/home/work/.openclaw/workspace/iNEST_Sim_Research/exp_next/v34_physics_first/v34_results.json'

ALPHA = {'graded': np.log(13), 'snn': np.log(32), 'cortex': np.log(50)}
THRESHOLDS = [
    (4.669,'L6超级(δ)'),(3.14159,'L5通用(π)'),(2.71828,'L4创造(e)'),
    (1.61803,'L3适应(φ)'),(1.00000,'L2反应(1)'),(0.70711,'L1感知(1/√2)'),(0.,'L0反射')
]
def lvl(c):
    for t,n in THRESHOLDS:
        if c>=t: return n
    return 'L0反射'

# ── 加载连接组 ──
with open(DATA) as f: d = json.load(f)
N = d['N']
W0 = np.zeros((N,N))
for u,v,w in d['edges_chem']: W0[u,v] += float(w)
for u,v,w in d['edges_elec']: W0[u,v] += float(w)*0.5; W0[v,u] += float(w)*0.5
np.fill_diagonal(W0, 0)
W0 = W0 / max(W0.max(),1) * 0.8

G_anat = nx.from_numpy_array((W0>0.05).astype(float)).to_undirected()
G_anat.remove_edges_from(nx.selfloop_edges(G_anat))
Ms_anat = community_louvain.best_partition(G_anat)
ms_vec  = np.array([Ms_anat.get(i,0) for i in range(N)])
print(f"连接组: N={N}, 解剖社区数={len(set(ms_vec))}")

# ══════════════════════════════════════════════════════════
# 核心：物理第一性仿真引擎
# ══════════════════════════════════════════════════════════
def simulate_physics_first(W_in, steps=6000,
                            eta_free=0.006,      # 自由能梯度学习率
                            beta_entropy=0.3,    # 熵正则化强度（防止过拟合）
                            gamma_action=0.2,    # 最小作用量惯性项
                            tau_pred=0.15,       # 预测模型时间常数
                            report_every=1000):
    """
    物理第一性演化引擎

    变分自由能：F_i = -log p(h_i | h_neighbors) + KL[q(h_i) || p(h_i)]
                    ≈ prediction_error_i^2 / 2 - beta_entropy * H[h_i历史]

    突触梯度：dW_ij/dt = -eta * ∂F/∂W_ij
                       = eta * (h_i - mu_i) * h_j     [最小化预测误差]
                       - gamma * W_ij * ||W||^2        [最小作用量正则]
                       + beta * (H_entropy_i - H_target) * h_j  [熵调控]
    """
    W = W_in.copy()
    h = np.random.uniform(0.1, 0.3, N)
    H_hist = np.zeros((steps, N))

    # 生成模型参数（每个节点维护对邻居的预测）
    mu = h.copy()           # 预测均值（广义坐标）
    sigma2 = np.ones(N)*0.1 # 预测方差（精度的倒数）
    precision = 1.0/sigma2  # 精度矩阵（对角线近似）

    # 最小作用量：保存上一步权重变化（动量项）
    dW_prev = np.zeros((N,N))

    # 能量追踪
    F_history = []
    Gamma_history = []
    H_TARGET = 0.5  # 目标熵（临界态对应最大熵）

    for t in range(steps):
        # ── Step 1：感知-预测循环（自上而下预测 + 自下而上误差）──
        h_pred_top_down = np.tanh(W.T @ mu)          # 预测（基于广义坐标）
        epsilon = h - h_pred_top_down                 # 预测误差（精度加权）
        PE = precision * epsilon                       # 精度加权预测误差

        # ── Step 2：激活更新（梯度下降自由能）──
        noise = np.random.normal(0, 0.03, N)
        dh = -h + np.tanh(W.T @ h + PE * 0.1 + noise)
        h = h + dh * 0.05
        h = np.clip(h, 0, 1)
        H_hist[t] = h

        # ── Step 3：更新广义坐标（预测模型）──
        mu = mu * (1 - tau_pred) + h * tau_pred

        # ── Step 4：计算变分自由能 F ──
        # F = -log likelihood + KL
        # 近似：F_i ≈ precision_i * epsilon_i^2 / 2 - beta * H_entropy_i
        eps2 = epsilon**2
        # 局部熵（用最近200步的激活分布估计）
        if t > 200:
            h_recent = H_hist[max(0,t-200):t]
            h_mean = h_recent.mean(0)
            h_var  = h_recent.var(0) + 1e-6
            H_entropy = 0.5 * np.log(2 * np.pi * np.e * h_var)  # 高斯熵近似
        else:
            h_mean = h; H_entropy = np.ones(N)*0.5

        F_local = precision * eps2 / 2 - beta_entropy * H_entropy
        F_global = float(F_local.mean())
        F_history.append(F_global)

        # ── Step 5：突触权重演化（∂F/∂W 梯度下降）──
        if t % 100 == 99 and t > 200:
            # 自由能梯度（主项）：-∂F/∂W_ij = precision_i * epsilon_i * h_j
            dW_free = np.outer(PE, h)                              # (N,N)

            # 熵正则项：奖励保持临界态熵
            entropy_drive = (H_entropy - H_TARGET)                 # 正→熵不足→增加多样性
            dW_entropy = beta_entropy * np.outer(entropy_drive, h)

            # 最小作用量（Hamilton原理）：抑制过大的权重变化（惯性项）
            # 作用量 S ≈ ∫ (dW/dt)^2 dt → 最小化 → 惩罚剧烈变化
            dW_action = gamma_action * dW_prev  # 动量延续（平滑轨迹）

            # 合并（全局优化目标 = 最小自由能 + 最大熵 + 最小作用量）
            dW = eta_free * (dW_free + dW_entropy) + dW_action
            np.fill_diagonal(dW, 0)

            # Hebbian上限约束（防止无限增长）
            W_new = W + dW * 0.1
            # 权重衰减（L2正则 = 最小作用量的权重项）
            W_new = W_new * (1 - 0.001)
            W = np.clip(W_new, 0, 1.5)
            np.fill_diagonal(W, 0)
            dW_prev = dW.copy()

            # 精度更新（贝叶斯推断：误差小→精度高）
            precision = precision * 0.99 + (1.0 / (eps2 + 0.01)) * 0.01
            precision = np.clip(precision, 0.1, 20.0)

        # ── Step 6：在线Γst监控（每500步）──
        if t % 500 == 499 and t > 1000:
            FC = np.corrcoef(H_hist[max(0,t-500):t].T)
            np.fill_diagonal(FC, 0); FC = np.nan_to_num(FC)
            Gf = nx.from_numpy_array(np.abs(FC))
            MT = community_louvain.best_partition(Gf)
            mt = [MT.get(i,0) for i in range(N)]
            nmi = float(normalized_mutual_info_score(ms_vec, mt))
            Gamma_history.append((t, nmi, F_global))
            if t % 2000 == 1999:
                print(f"  step={t}: F={F_global:.4f}, Γst_NMI={nmi:.4f}", flush=True)

        if t % report_every == report_every-1:
            act = H_hist[max(0,t-200):t].mean()
            print(f"  step={t+1}/{steps}: act={act:.3f} F={F_global:.4f}", flush=True)

    return W, H_hist, F_history, Gamma_history

# ── Sc（同v33）──
def compute_Sc(W):
    adj = (W>0.05).astype(float); np.fill_diagonal(adj,0)
    G = nx.from_numpy_array(adj).to_undirected()
    G.remove_edges_from(nx.selfloop_edges(G))
    comps = list(nx.connected_components(G))
    C = max(len(c) for c in comps)/N if comps else 0
    core = nx.core_number(G)
    H_ = min(max(core.values())/max(np.log2(N+1),1), 1.)
    part = community_louvain.best_partition(G)
    Qr = community_louvain.modularity(part,G)
    Qrand = 1/np.sqrt(max(G.number_of_edges(),1))
    M = max(0., min((Qr-Qrand)/max(1-Qrand,1e-6), 1.))
    try:
        lcc = G.subgraph(max(comps,key=len)).copy()
        nodes = list(lcc.nodes)[:60]
        lens = []
        for n_ in nodes:
            sp = nx.single_source_shortest_path_length(lcc, n_)
            lens.extend(sp.values())
        L_real = np.mean(lens) if lens else N
        k_mean = max(np.mean([deg for _,deg in G.degree()]), 2)
        L_rand = np.log(N)/np.log(k_mean)
        C_rand = k_mean/(N-1)
        Cv = nx.average_clustering(G)
        sigma = (Cv/max(C_rand,1e-6))/(L_real/max(L_rand,1e-6))
    except: sigma=1.0
    R = float(np.tanh(max(0., sigma-1.)))
    sc = float((max(C,1e-6)*max(H_,1e-6)*max(M,1e-6)*max(R,1e-6))**0.25)
    return sc, {'C':round(C,4),'H':round(H_,4),'M':round(M,4),'R_sw':round(R,4),'sigma':round(sigma,3)}

def compute_Tc(H):
    T,N_ = H.shape
    act = H.mean(1)
    acf = np.correlate(act-act.mean(),act-act.mean(),'full')
    acf = acf[T-1:]/(acf[T-1]+1e-8)
    lam = float(np.clip(acf[1],0,2)); lam_n=1/(1+abs(lam-1))
    idx = np.random.choice(N_,min(50,N_),replace=False)
    corrs=[]
    for i in idx:
        for j in idx:
            if i<j:
                a,b=H[:,i],H[:,j]
                if a.std()>1e-4 and b.std()>1e-4:
                    r,_=pearsonr(a,b); corrs.append(abs(r))
    Phi = float(np.mean(corrs)) if corrs else 0.05
    WIN,STR=200,30; fc_list=[]
    for s in range(0,T-WIN,STR):
        seg=H[s:s+WIN]; std=seg.std(0); valid=std>1e-4
        if valid.sum()>10:
            sub=seg[:,valid]; fc=np.corrcoef(sub.T)
            fc_list.append(fc[np.triu_indices(len(fc),k=1)])
    if len(fc_list)>5:
        min_len = min(len(x) for x in fc_list)
        arr=np.array([x[:min_len] for x in fc_list])
        Psi=float(arr.std(0).mean()/max(np.abs(arr).mean(),1e-6)); Psi=min(Psi,1.)
    else: Psi=0.1
    taus=[]
    for i in range(N_):
        s=H[:,i]
        if s.std()>1e-4:
            acf_i=np.correlate(s-s.mean(),s-s.mean(),'full')
            acf_i=acf_i[T-1:]/(acf_i[T-1]+1e-8)
            for lag in range(1,min(200,T)):
                if acf_i[lag]<1/np.e: taus.append(lag); break
    if len(taus)>5:
        h_,_=np.histogram(taus,bins=10); h_=h_/max(h_.sum(),1); h_=h_[h_>0]
        Theta=float(-np.sum(h_*np.log2(h_))/np.log2(10))
    else: Theta=0.3
    tc=float((max(lam_n,1e-4)*max(Phi,1e-4)*max(Psi,1e-4)*max(Theta,1e-4))**0.25)
    return tc,{'lambda_norm':round(lam_n,4),'Phi':round(Phi,4),'Psi':round(Psi,4),'Theta':round(Theta,4)}

def compute_Gst(W,H):
    adj=(W>0.05).astype(float); np.fill_diagonal(adj,0)
    G=nx.from_numpy_array(adj).to_undirected(); G.remove_edges_from(nx.selfloop_edges(G))
    FC=np.corrcoef(H.T); np.fill_diagonal(FC,0); FC=np.nan_to_num(FC)
    Gf=nx.from_numpy_array(np.abs(FC))
    MT=community_louvain.best_partition(Gf); mt=[MT.get(i,0) for i in range(N)]
    nmi=float(normalized_mutual_info_score(ms_vec,mt))
    try:
        comps=list(nx.connected_components(G)); lcc_n=max(comps,key=len)
        sub=G.subgraph(lcc_n); nn=list(lcc_n)[:80]
        L=dict(nx.all_pairs_shortest_path_length(sub))
        DA=np.array([[L.get(i,{}).get(j,N) for j in nn] for i in nn],float)
        DFC=1-np.abs(FC[np.ix_(nn,nn)])
        da_f=DA[np.triu_indices(len(nn),k=1)]; dfc_f=DFC[np.triu_indices(len(nn),k=1)]
        mr,_=pearsonr(da_f,dfc_f) if da_f.std()>1e-6 and dfc_f.std()>1e-6 else (0.,0.)
    except: mr=0.
    sg=float(np.sign(mr)) if mr!=0 else 1.
    return float(nmi*sg),{'NMI':round(nmi,4),'mantel_r':round(float(mr),4)}

# ── 参数扫描：验证物理参数对CST的影响 ──
configs = [
    # (tag, eta_free, beta_entropy, gamma_action)
    ('v34_baseline',  dict(eta_free=0.006, beta_entropy=0.3, gamma_action=0.2), 'FEP基线'),
    ('v34_highFEP',   dict(eta_free=0.010, beta_entropy=0.5, gamma_action=0.1), '高FEP强度（强能量梯度）'),
    ('v34_critEdge',  dict(eta_free=0.008, beta_entropy=0.7, gamma_action=0.3), '临界态优先（熵最大化）'),
]

results = {
    'experiment': 'v34_physics_first', 'N': N, 'alpha': ALPHA,
    'physical_principles': {
        'FEP': 'F = precision*epsilon^2/2 - beta*H_entropy (Friston 2010)',
        'Hamilton': 'S = integral(dW/dt)^2 dt minimized via momentum term',
        'LocalSOC': 'No global controller; only local energy gradient dF/dW'
    },
    'v33_baseline': {'Gamma_st': 0.187, 'CST_snn': 1.268},
    'target': {'level': 'L3适应(φ=1.618)', 'Gamma_st': 0.25, 'CST_snn': 1.618},
    'systems': {}
}

for tag, params, desc in configs:
    print(f"\n{'='*60}\n配置: {tag} ({desc})")
    W_ev, H_ev, F_hist, Gst_hist = simulate_physics_first(W0, steps=6000, **params)

    H_use = H_ev[-1500:]
    sc, sc_c = compute_Sc(W_ev)
    tc, tc_c = compute_Tc(H_use)
    gst, gst_c = compute_Gst(W_ev, H_use)
    csts = {k: float((sc*tc)*np.exp(a*gst)) for k,a in ALPHA.items()}

    # 能量收敛分析
    F_arr = np.array(F_hist)
    F_init  = float(np.mean(F_arr[:200]))
    F_final = float(np.mean(F_arr[-200:]))
    F_drop  = F_init - F_final  # 自由能下降量（越大越好）

    print(f"  Sc={sc:.4f} | Tc={tc:.4f} | Γst={gst:.4f}")
    print(f"  CST(snn)={csts['snn']:.4f} → {lvl(csts['snn'])}")
    print(f"  自由能: F_init={F_init:.4f} → F_final={F_final:.4f} (Δ={F_drop:+.4f})")
    print(f"  Γst提升: {gst-0.187:+.4f}（v33基线0.187）")

    results['systems'][tag] = {
        'desc': desc, 'params': params,
        'Sc': sc, 'Tc': tc, 'Gamma_st': gst,
        'sc_components': sc_c, 'tc_components': tc_c, 'gst_components': gst_c,
        **{f'CST_{k}': v for k,v in csts.items()},
        'level_snn': lvl(csts['snn']),
        'free_energy': {'F_init': F_init, 'F_final': F_final, 'F_drop': F_drop},
        'Gamma_st_vs_v33': round(gst-0.187, 4),
        'gst_trajectory': Gst_hist[-5:]
    }

print(f"\n{'='*60}")
print(f"v34结果汇总（v33基线：Γst=0.187, CST=1.268）")
print(f"{'配置':<20} {'Γst':>7} {'ΔΓst':>7} {'CST(snn)':>10} {'ΔF':>8} {'等级'}")
print('-'*70)
for tag, r in results['systems'].items():
    fe = r['free_energy']
    print(f"{tag:<20} {r['Gamma_st']:>7.4f} {r['Gamma_st_vs_v33']:>+7.4f} "
          f"{r['CST_snn']:>10.4f} {fe['F_drop']:>+8.4f} {r['level_snn']}")

best = max(results['systems'], key=lambda k: results['systems'][k]['CST_snn'])
br = results['systems'][best]
phi = 1.61803
goal = '✅ 跨越L3' if br['CST_snn']>=phi else f"距L3差{phi-br['CST_snn']:.4f}"
results['best'] = best
results['conclusion'] = (
    f"最佳{best}: Γst={br['Gamma_st']:.4f}, CST(snn)={br['CST_snn']:.4f}, "
    f"{br['level_snn']}. L3目标: {goal}"
)
print(f"\n最佳: {best} | CST={br['CST_snn']:.4f} | L3(φ=1.618): {goal}")

with open(OUT,'w') as f: json.dump(results,f,indent=2)
print(f"✅ 写入 {OUT}")
