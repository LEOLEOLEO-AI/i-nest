#!/usr/bin/env python3
"""
v35实验：纯FEP精度加权梯度下降
修正v34错误：删除entropy正则项，临界态由BCM自然维持

正确物理第一性：
  dW/dt = -η × precision_i × ε_i × h_j   (纯预测误差极小化)
  precision_i 由贝叶斯更新（误差小→精度高）
  临界态 = 涌现结果（BCM θ自然调控，非强制约束）

目标：Γst≥0.25, CST(snn)≥1.618（L3适应φ）
"""
import numpy as np, json, networkx as nx
from sklearn.metrics import normalized_mutual_info_score
from scipy.stats import pearsonr
import community as community_louvain, warnings, os
warnings.filterwarnings('ignore')
np.random.seed(42)

DATA = '/home/work/.openclaw/workspace/sdi_sim/celegans_sim/connectome_v8_data.json'
OUT  = '/home/work/.openclaw/workspace/iNEST_Sim_Research/exp_next/v35_pure_fep/v35_results.json'

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
# v35核心：纯FEP精度加权梯度下降
# ══════════════════════════════════════════════════════════
def simulate_v35(W_in, steps=6000,
                 eta_base=0.005,       # 基础学习率
                 tau_pred=0.10,        # 预测模型时间常数（越小跟踪越快）
                 precision_lr=0.005,   # 精度更新速率
                 bcm_tau=0.002,        # BCM θ时间常数
                 report_every=1000):
    W = W_in.copy()
    h = np.random.uniform(0.1, 0.3, N)
    H = np.zeros((steps, N))

    # 生成模型（预测器）
    mu       = h.copy()          # 广义坐标（节点状态预测）
    precision = np.ones(N) * 2.0  # 精度（越高→越相信预测→学习率越大）
    # BCM滑动阈值（自然维持临界态，来自v25）
    theta_bcm = np.ones(N) * 0.15

    F_history  = []
    Gst_history = []

    for t in range(steps):
        # ── 感知：自下而上激活 ──
        noise = np.random.normal(0, 0.03, N)
        h_pred_td = np.tanh(W.T @ mu)          # 自上而下预测
        epsilon    = h - h_pred_td             # 预测误差
        PE_weighted = precision * epsilon       # 精度加权误差

        # ── 激活更新（误差修正） ──
        dh = -h + np.tanh(W.T @ h + PE_weighted * 0.08 + noise)
        h  = h + dh * 0.05
        h  = np.clip(h, 0, 1)
        H[t] = h

        # ── 广义坐标更新（慢速预测跟踪） ──
        mu = mu * (1 - tau_pred) + h * tau_pred

        # ── 精度贝叶斯更新（误差小→精度升，误差大→精度降） ──
        if t % 50 == 49:
            eps2 = epsilon ** 2
            precision = precision * (1 - precision_lr) + \
                        (1.0 / (eps2 + 0.05)) * precision_lr
            precision = np.clip(precision, 0.5, 15.0)

        # ── 每100步：突触演化 ──
        if t % 100 == 99 and t > 200:
            h_hist = H[max(0,t-100):t].mean(0)

            # BCM滑动阈值（自然临界调控，不强加entropy）
            theta_bcm = theta_bcm * (1 - bcm_tau) + (h_hist**2) * bcm_tau
            theta_bcm = np.clip(theta_bcm, 0.03, 0.50)

            # 核心规则：纯FEP梯度
            # dW_ij = η × precision_i × ε_i × h_j  （最小化预测误差）
            pre  = H[t-1]
            post = h
            eps_now = post - np.tanh(W.T @ mu)

            dW_fep = eta_base * np.outer(precision * eps_now, pre)

            # BCM约束（防止权重无界增长，维持稳态）
            # dW_bcm = η × h_post × (h_post - θ_bcm) × h_pre
            dW_bcm = eta_base * np.outer(post * (post - theta_bcm), pre)

            # 权重衰减（最小作用量：抑制不必要的大权重）
            W_decay = -0.0005 * W

            dW = dW_fep * 0.6 + dW_bcm * 0.4 + W_decay
            np.fill_diagonal(dW, 0)
            W = np.clip(W + dW * 0.12, 0, 1.5)
            np.fill_diagonal(W, 0)

            # 稳态缩放（Rule3 BF-Homeo：EL控制在[15%,35%]）
            act = h_hist
            W[:, act > 0.40] *= 0.96
            W[:, act < 0.04] *= 1.04
            W = np.clip(W, 0, 1.5)

        # ── 变分自由能计算（监控用，不用于梯度） ──
        # F = precision × ε² / 2  (能量项，无entropy项)
        eps2 = (h - np.tanh(W.T @ mu)) ** 2
        F_global = float((precision * eps2 / 2).mean())
        F_history.append(F_global)

        # ── 在线Γst（每500步） ──
        if t % 500 == 499 and t > 1000:
            FC = np.corrcoef(H[max(0,t-500):t].T)
            np.fill_diagonal(FC, 0); FC = np.nan_to_num(FC)
            Gf = nx.from_numpy_array(np.abs(FC))
            MT = community_louvain.best_partition(Gf)
            mt = [MT.get(i,0) for i in range(N)]
            nmi = float(normalized_mutual_info_score(ms_vec, mt))
            Gst_history.append((t, nmi, F_global))
            if t % 2000 == 1999:
                print(f"  step={t}: F={F_global:.4f}, Γst_NMI={nmi:.4f}, "
                      f"precision_mean={precision.mean():.2f}", flush=True)

        if t % report_every == report_every-1:
            act_r = H[max(0,t-200):t].mean()
            prec_m = precision.mean()
            print(f"  step={t+1}/{steps}: act={act_r:.3f} F={F_global:.4f} "
                  f"prec={prec_m:.2f}", flush=True)

    return W, H, F_history, Gst_history

# ── 度量函数（与v32/v33一致）──
def compute_Sc(W):
    adj=(W>0.05).astype(float); np.fill_diagonal(adj,0)
    G=nx.from_numpy_array(adj).to_undirected(); G.remove_edges_from(nx.selfloop_edges(G))
    comps=list(nx.connected_components(G))
    C=max(len(c) for c in comps)/N if comps else 0
    core=nx.core_number(G); H_=min(max(core.values())/max(np.log2(N+1),1),1.)
    part=community_louvain.best_partition(G)
    Qr=community_louvain.modularity(part,G)
    Qrand=1/np.sqrt(max(G.number_of_edges(),1))
    M=max(0.,min((Qr-Qrand)/max(1-Qrand,1e-6),1.))
    try:
        lcc=G.subgraph(max(comps,key=len)).copy(); nodes=list(lcc.nodes)[:60]
        lens=[]
        for n_ in nodes:
            sp=nx.single_source_shortest_path_length(lcc,n_); lens.extend(sp.values())
        L_real=np.mean(lens) if lens else N
        k_mean=max(np.mean([deg for _,deg in G.degree()]),2)
        L_rand=np.log(N)/np.log(k_mean); C_rand=k_mean/(N-1)
        Cv=nx.average_clustering(G)
        sigma=(Cv/max(C_rand,1e-6))/(L_real/max(L_rand,1e-6))
    except: sigma=1.0
    R=float(np.tanh(max(0.,sigma-1.)))
    sc=float((max(C,1e-6)*max(H_,1e-6)*max(M,1e-6)*max(R,1e-6))**0.25)
    return sc,{'C':round(C,4),'H':round(H_,4),'M':round(M,4),'R_sw':round(R,4),'sigma':round(sigma,3)}

def compute_Tc(H):
    T,N_=H.shape
    act=H.mean(1)
    acf=np.correlate(act-act.mean(),act-act.mean(),'full'); acf=acf[T-1:]/(acf[T-1]+1e-8)
    lam=float(np.clip(acf[1],0,2)); lam_n=1/(1+abs(lam-1))
    idx=np.random.choice(N_,min(50,N_),replace=False)
    corrs=[]
    for i in idx:
        for j in idx:
            if i<j:
                a,b=H[:,i],H[:,j]
                if a.std()>1e-4 and b.std()>1e-4:
                    r,_=pearsonr(a,b); corrs.append(abs(r))
    Phi=float(np.mean(corrs)) if corrs else 0.05
    WIN,STR=200,30; fc_list=[]
    for s in range(0,T-WIN,STR):
        seg=H[s:s+WIN]; std=seg.std(0); valid=std>1e-4
        if valid.sum()>10:
            sub=seg[:,valid]; fc=np.corrcoef(sub.T)
            fc_list.append(fc[np.triu_indices(len(fc),k=1)])
    if len(fc_list)>5:
        min_len=min(len(x) for x in fc_list)
        arr=np.array([x[:min_len] for x in fc_list])
        Psi=float(arr.std(0).mean()/max(np.abs(arr).mean(),1e-6)); Psi=min(Psi,1.)
    else: Psi=0.1
    taus=[]
    for i in range(N_):
        s=H[:,i]
        if s.std()>1e-4:
            acf_i=np.correlate(s-s.mean(),s-s.mean(),'full'); acf_i=acf_i[T-1:]/(acf_i[T-1]+1e-8)
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

# ── 参数扫描：精度学习率 × 预测时间常数 ──
configs = [
    ('v35_a', dict(eta_base=0.005, tau_pred=0.10, precision_lr=0.005, bcm_tau=0.002), 'FEP基线'),
    ('v35_b', dict(eta_base=0.007, tau_pred=0.08, precision_lr=0.008, bcm_tau=0.003), 'FEP强化（快速精度更新）'),
    ('v35_c', dict(eta_base=0.006, tau_pred=0.05, precision_lr=0.010, bcm_tau=0.002), 'FEP最强（最慢预测跟踪）'),
]

results = {
    'experiment': 'v35_pure_fep', 'N': N, 'alpha': ALPHA,
    'physics': 'dW = eta * precision * epsilon * h_pre + BCM (no entropy term)',
    'fix_from_v34': 'Removed beta_entropy term; F should decrease not increase',
    'baselines': {'v33_Gamma_st': 0.187, 'v33_CST_snn': 1.268,
                  'v34_Gamma_st': 0.138, 'v34_CST_snn': 0.978},
    'target': 'L3适应 φ=1.618',
    'systems': {}
}

for tag, params, desc in configs:
    print(f"\n{'='*60}\n配置: {tag} ({desc})")
    W_ev, H_ev, F_hist, Gst_hist = simulate_v35(W0, steps=6000, **params)

    H_use = H_ev[-1500:]
    sc, sc_c = compute_Sc(W_ev)
    tc, tc_c = compute_Tc(H_use)
    gst, gst_c = compute_Gst(W_ev, H_use)
    csts = {k: float((sc*tc)*np.exp(a*gst)) for k,a in ALPHA.items()}

    F_arr = np.array(F_hist)
    F_init  = float(np.mean(F_arr[:200]))
    F_final = float(np.mean(F_arr[-200:]))
    F_drop  = F_init - F_final  # 正值 = F下降 = 物理正确！

    print(f"  Sc={sc:.4f} | Tc={tc:.4f} | Γst={gst:.4f}")
    print(f"  CST(snn)={csts['snn']:.4f} → {lvl(csts['snn'])}")
    print(f"  F: {F_init:.4f}→{F_final:.4f} (Δ={F_drop:+.4f}) "
          f"{'✅ F下降(正确)' if F_drop>0 else '🔴 F上升(需修正)'}")
    print(f"  Γst vs v33: {gst-0.187:+.4f}")

    results['systems'][tag] = {
        'desc': desc, 'params': params,
        'Sc':sc, 'Tc':tc, 'Gamma_st':gst,
        'sc_components':sc_c, 'tc_components':tc_c, 'gst_components':gst_c,
        **{f'CST_{k}':v for k,v in csts.items()},
        'level_snn': lvl(csts['snn']),
        'free_energy': {'F_init':F_init,'F_final':F_final,'F_drop':F_drop,
                        'converging': F_drop > 0},
        'Gamma_st_vs_v33': round(gst-0.187, 4),
        'Gamma_st_vs_v34': round(gst-0.138, 4),
        'gst_trajectory': Gst_hist[-5:]
    }

# ── 汇总 ──
print(f"\n{'='*60}")
print(f"v35汇总  (v33基线: Γst=0.187, CST=1.268 | v34: Γst=0.138, CST=0.978)")
print(f"{'配置':<12} {'Γst':>7} {'ΔΓst(v33)':>11} {'CST(snn)':>10} {'F收敛':>8} {'等级'}")
print('-'*70)
for tag,r in results['systems'].items():
    fc = '✅' if r['free_energy']['converging'] else '🔴'
    print(f"{tag:<12} {r['Gamma_st']:>7.4f} {r['Gamma_st_vs_v33']:>+11.4f} "
          f"{r['CST_snn']:>10.4f} {fc:>8} {r['level_snn']}")

best = max(results['systems'], key=lambda k: results['systems'][k]['CST_snn'])
br   = results['systems'][best]
phi  = 1.61803
goal = '✅ 跨越L3(φ)' if br['CST_snn']>=phi else f"距L3差{phi-br['CST_snn']:.4f}"
results['best'] = best
results['conclusion'] = (
    f"最佳{best}: Γst={br['Gamma_st']:.4f}, CST(snn)={br['CST_snn']:.4f}, "
    f"{br['level_snn']}. L3: {goal}. F收敛: {br['free_energy']['converging']}"
)
print(f"\n最佳: {best} | CST={br['CST_snn']:.4f} | L3: {goal} | F收敛: {br['free_energy']['converging']}")

with open(OUT,'w') as f: json.dump(results,f,indent=2)
print(f"✅ 写入 {OUT}")
