#!/usr/bin/env python3
"""
v33实验：FEP-STDP融合强化Γst
目标：Γst从0.097→0.30+，CST从0.49→0.93（跨越L1感知阈值0.707）
"""
import numpy as np, json, networkx as nx
from sklearn.metrics import normalized_mutual_info_score
from scipy.stats import pearsonr
import community as community_louvain, warnings, os
warnings.filterwarnings('ignore')

np.random.seed(42)
DATA = '/home/work/.openclaw/workspace/sdi_sim/celegans_sim/connectome_v8_data.json'
OUT  = '/home/work/.openclaw/workspace/iNEST_Sim_Research/exp_next/v33_gamma_st/v33_results.json'

ALPHA = {'graded': np.log(13), 'snn': np.log(32), 'cortex': np.log(50)}
THRESHOLDS = [
    (4.669,'L6超级(δ)'),(3.14159,'L5通用(π)'),(2.71828,'L4创造(e)'),
    (1.61803,'L3适应(φ)'),(1.00000,'L2反应(1)'),(0.70711,'L1感知(1/√2)'),(0.,'L0反射')
]
def lvl(c):
    for t,n in THRESHOLDS:
        if c>=t: return n
    return 'L0反射'

with open(DATA) as f: d = json.load(f)
N = d['N']
W0 = np.zeros((N,N))
for u,v,w in d['edges_chem']: W0[u,v] += float(w)
for u,v,w in d['edges_elec']: W0[u,v] += float(w)*0.5; W0[v,u] += float(w)*0.5
np.fill_diagonal(W0, 0)
W0 = W0 / max(W0.max(), 1) * 0.8

G_anat = nx.from_numpy_array((W0>0.05).astype(float)).to_undirected()
G_anat.remove_edges_from(nx.selfloop_edges(G_anat))
Ms_anat = community_louvain.best_partition(G_anat)
ms_vec = np.array([Ms_anat.get(i,0) for i in range(N)])
print(f"连接组: N={N}, 解剖社区数={len(set(ms_vec))}")

def simulate_v33(W_in, steps=5000, alpha_fep=0.4, beta_align=0.3, report_every=1000):
    W = W_in.copy()
    h = np.random.uniform(0.1, 0.3, N)
    H = np.zeros((steps, N))
    theta_bcm = np.ones(N)*0.15
    h_pred = h.copy()
    ETA_BASE = 0.004
    gst_hist = []

    for t in range(steps):
        noise = np.random.normal(0, 0.04, N)
        h_new = np.tanh(W.T @ h + noise)
        h = h*0.95 + h_new*0.05
        h = np.clip(h, 0, 1)
        H[t] = h

        surprise = np.abs(h - h_pred)
        h_pred = h_pred*0.9 + h*0.1
        surprise_global = float(surprise.mean())

        if t % 200 == 199 and t > 400:
            h_hist = H[max(0,t-200):t].mean(0)
            theta_bcm = theta_bcm*0.99 + (h_hist**2)*0.01
            theta_bcm = np.clip(theta_bcm, 0.05, 0.5)

            pre = H[t-1]; post = h
            surprise_node = np.abs(h - h_pred)
            eta_node = ETA_BASE * (1 + alpha_fep * surprise_node)
            dW = eta_node[:,None] * np.outer(post - theta_bcm, pre) \
               - ETA_BASE * np.outer(pre, post)
            W = np.clip(W + dW*0.15, 0, 1)
            np.fill_diagonal(W, 0)

            act = h_hist
            W[:, act>0.4] *= 0.95
            W[:, act<0.05] *= 1.05
            W = np.clip(W, 0, 1)

            if t % 400 == 399 and t > 800 and beta_align > 0:
                FC = np.corrcoef(H[max(0,t-400):t].T)
                np.fill_diagonal(FC, 0); FC = np.nan_to_num(FC)
                Gf = nx.from_numpy_array(np.abs(FC))
                MT_dict = community_louvain.best_partition(Gf)
                mt_vec = np.array([MT_dict.get(i,0) for i in range(N)])

                align_bonus = np.zeros((N,N))
                for i in range(N):
                    for j in range(N):
                        if i != j:
                            ss = (ms_vec[i] == ms_vec[j])
                            fs = (mt_vec[i] == mt_vec[j])
                            if ss and fs:     align_bonus[i,j] =  beta_align * ETA_BASE
                            elif ss and not fs: align_bonus[i,j] = -beta_align * ETA_BASE * 0.5

                W = np.clip(W + align_bonus * np.outer(h, h), 0, 1)
                np.fill_diagonal(W, 0)

                nmi = normalized_mutual_info_score(ms_vec, mt_vec)
                gst_hist.append((t, float(nmi)))
                if t % 2000 == 1999:
                    print(f"  step={t}: NMI={nmi:.4f}", flush=True)

        if t % report_every == report_every-1:
            print(f"  step={t+1}/{steps}: act={H[max(0,t-200):t].mean():.3f}", flush=True)

    return W, H, gst_hist

def compute_Sc(W):
    adj = (W>0.05).astype(float); np.fill_diagonal(adj,0)
    G = nx.from_numpy_array(adj).to_undirected()
    G.remove_edges_from(nx.selfloop_edges(G))
    comps = list(nx.connected_components(G))
    C = max(len(c) for c in comps)/N if comps else 0
    core = nx.core_number(G)
    H_ = min(max(core.values())/max(np.log2(N+1),1), 1.)
    part = community_louvain.best_partition(G)
    Qr = community_louvain.modularity(part, G)
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
    except: sigma = 1.0
    R = float(np.tanh(max(0., sigma-1.)))
    sc = float((max(C,1e-6)*max(H_,1e-6)*max(M,1e-6)*max(R,1e-6))**0.25)
    return sc, {'C':round(C,4),'H':round(H_,4),'M':round(M,4),'R_sw':round(R,4),'sigma':round(sigma,3)}

def compute_Tc(H):
    T, N_ = H.shape
    act = H.mean(1)
    acf = np.correlate(act-act.mean(), act-act.mean(), 'full')
    acf = acf[T-1:] / (acf[T-1]+1e-8)
    lam = float(np.clip(acf[1], 0, 2))
    lam_n = 1/(1+abs(lam-1))
    idx = np.random.choice(N_, min(50,N_), replace=False)
    corrs = []
    for i in idx:
        for j in idx:
            if i<j:
                a,b = H[:,i], H[:,j]
                if a.std()>1e-4 and b.std()>1e-4:
                    r,_ = pearsonr(a,b); corrs.append(abs(r))
    Phi = float(np.mean(corrs)) if corrs else 0.05
    WIN,STR = 200,30; fc_list = []
    for s in range(0, T-WIN, STR):
        seg = H[s:s+WIN]; std = seg.std(0); valid = std>1e-4
        if valid.sum()>10:
            sub = seg[:,valid]; fc = np.corrcoef(sub.T)
            fc_list.append(fc[np.triu_indices(len(fc),k=1)])
    if len(fc_list)>5:
        arr = np.array(fc_list)
        Psi = float(arr.std(0).mean()/max(np.abs(arr).mean(),1e-6))
        Psi = min(Psi, 1.)
    else: Psi = 0.1
    taus = []
    for i in range(N_):
        s = H[:,i]
        if s.std()>1e-4:
            acf_i = np.correlate(s-s.mean(),s-s.mean(),'full')
            acf_i = acf_i[T-1:]/(acf_i[T-1]+1e-8)
            for lag in range(1, min(200,T)):
                if acf_i[lag]<1/np.e: taus.append(lag); break
    if len(taus)>5:
        h_,_ = np.histogram(taus, bins=10); h_=h_/max(h_.sum(),1); h_=h_[h_>0]
        Theta = float(-np.sum(h_*np.log2(h_))/np.log2(10))
    else: Theta = 0.3
    tc = float((max(lam_n,1e-4)*max(Phi,1e-4)*max(Psi,1e-4)*max(Theta,1e-4))**0.25)
    return tc, {'lambda_norm':round(lam_n,4),'Phi':round(Phi,4),'Psi':round(Psi,4),'Theta':round(Theta,4)}

def compute_Gst(W, H):
    adj = (W>0.05).astype(float); np.fill_diagonal(adj,0)
    G = nx.from_numpy_array(adj).to_undirected()
    G.remove_edges_from(nx.selfloop_edges(G))
    FC = np.corrcoef(H.T); np.fill_diagonal(FC,0); FC = np.nan_to_num(FC)
    Gf = nx.from_numpy_array(np.abs(FC))
    MT = community_louvain.best_partition(Gf)
    mt = [MT.get(i,0) for i in range(N)]
    nmi = float(normalized_mutual_info_score(ms_vec, mt))
    try:
        comps = list(nx.connected_components(G))
        lcc_n = max(comps, key=len); sub = G.subgraph(lcc_n)
        nn = list(lcc_n)[:80]
        L = dict(nx.all_pairs_shortest_path_length(sub))
        DA = np.array([[L.get(i,{}).get(j,N) for j in nn] for i in nn], float)
        DFC = 1-np.abs(FC[np.ix_(nn,nn)])
        da_f=DA[np.triu_indices(len(nn),k=1)]; dfc_f=DFC[np.triu_indices(len(nn),k=1)]
        mr,_ = pearsonr(da_f,dfc_f) if da_f.std()>1e-6 and dfc_f.std()>1e-6 else (0.,0.)
    except: mr = 0.
    sg = float(np.sign(mr)) if mr!=0 else 1.
    return float(nmi*sg), {'NMI':round(nmi,4),'mantel_r':round(float(mr),4)}

def compute_CST(sc, tc, gst):
    return {k: float((sc*tc)*np.exp(a*gst)) for k,a in ALPHA.items()}

# ── 三配置对比 ──
configs = [
    ('v33_fep_only',   dict(alpha_fep=0.4, beta_align=0.0), 'FEP-STDP，无对齐激励'),
    ('v33_align_only', dict(alpha_fep=0.0, beta_align=0.5), '仅结构-功能对齐激励'),
    ('v33_full',       dict(alpha_fep=0.4, beta_align=0.3), 'FEP + 对齐（全融合）'),
]

results = {
    'experiment':'v33_gamma_boost', 'N':N, 'alpha':ALPHA,
    'v32_baseline':{'Gamma_st':0.097,'CST_snn':0.536},
    'paper_ref':{'celegans_CST':0.4107,'celegans_Gamma_st':0.17},
    'systems':{}
}

for tag, params, desc in configs:
    print(f"\n{'='*58}\n配置: {tag} ({desc})")
    W_ev, H_ev, gst_hist = simulate_v33(W0, steps=5000, **params)
    H_use = H_ev[-1500:]
    sc, sc_c = compute_Sc(W_ev)
    tc, tc_c = compute_Tc(H_use)
    gst, gst_c = compute_Gst(W_ev, H_use)
    csts = compute_CST(sc, tc, gst)
    print(f"  Sc={sc:.4f} | Tc={tc:.4f} | Γst={gst:.4f}")
    print(f"  CST(snn)={csts['snn']:.4f} → {lvl(csts['snn'])}")
    print(f"  Γst提升: {gst-0.097:+.4f}")
    results['systems'][tag] = {
        'desc':desc,'params':params,
        'Sc':sc,'Tc':tc,'Gamma_st':gst,
        'sc_components':sc_c,'tc_components':tc_c,'gst_components':gst_c,
        **{f'CST_{k}':v for k,v in csts.items()},
        'level_snn':lvl(csts['snn']),
        'Gamma_st_improvement':round(gst-0.097,4),
        'gst_trajectory':gst_hist[-5:]
    }

print(f"\n{'='*58}")
print(f"{'配置':<22} {'Γst':>7} {'Δ':>7} {'CST(snn)':>10} {'等级':>12}")
print('-'*60)
for tag, r in results['systems'].items():
    print(f"{tag:<22} {r['Gamma_st']:>7.4f} {r['Gamma_st_improvement']:>+7.4f} {r['CST_snn']:>10.4f} {r['level_snn']:>12}")

best = max(results['systems'], key=lambda k: results['systems'][k]['Gamma_st'])
br = results['systems'][best]
goal_l1 = '✅ 跨越L1' if br['CST_snn']>=0.707 else f"差{0.707-br['CST_snn']:.4f}"
goal_gst = '✅ 达标' if br['Gamma_st']>=0.30 else f"差{0.30-br['Gamma_st']:.4f}"
print(f"\n最佳: {best} | Γst目标(≥0.30): {goal_gst} | L1目标(≥0.707): {goal_l1}")
results['best'] = best
results['conclusion'] = f"最佳{best}: Γst={br['Gamma_st']:.4f}, CST(snn)={br['CST_snn']:.4f}, {br['level_snn']}"

with open(OUT,'w') as f: json.dump(results,f,indent=2)
print(f"✅ 写入 {OUT}")
