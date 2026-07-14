#!/usr/bin/env python3
"""
v38：社区频率偏置（Community Frequency Bias）
生物第一性：Fries 2015 CTC理论（Communication Through Coherence）
  - θ节律在解剖社区内锁相 → 功能连接强
  - γ节律跨社区调制 → 维持跨社区弱连接
  - 实现：每个节点加内禀频率偏置 ω_i，同社区相近，跨社区差异
  - 硅基映射：ReRAM弛豫振荡频率差（器件物理天然存在）

核心修改：
  h_i(t+1) = tanh(Σ W_ji·h_j + ω_i·sin(2π·f_i·t) + noise)
  ω_i由解剖社区决定：同社区f相近，跨社区f差0.05-0.10

不加新规则，只加一个标量偏置：大道至简

目标：Γst 0.187→0.30+，CST(snn)≥1.618（L3适应φ）
"""
import numpy as np, json, networkx as nx
from sklearn.metrics import normalized_mutual_info_score
from scipy.stats import pearsonr
import community as community_louvain, warnings
warnings.filterwarnings('ignore')
np.random.seed(42)

DATA = '/home/work/.openclaw/workspace/sdi_sim/celegans_sim/connectome_v8_data.json'
OUT  = '/home/work/.openclaw/workspace/iNEST_Sim_Research/exp_next/v38_freq_bias/v38_results.json'
ALPHA = {'graded':np.log(13),'snn':np.log(32),'cortex':np.log(50)}
THRESHOLDS = [(4.669,'L6超级(δ)'),(3.14159,'L5通用(π)'),(2.71828,'L4创造(e)'),
              (1.61803,'L3适应(φ)'),(1.00000,'L2反应(1)'),(0.70711,'L1感知(1/√2)'),(0.,'L0反射')]
def lvl(c):
    for t,n in THRESHOLDS:
        if c>=t: return n
    return 'L0反射'

with open(DATA) as f: d=json.load(f)
N=d['N']
W0=np.zeros((N,N))
for u,v,w in d['edges_chem']: W0[u,v]+=float(w)
for u,v,w in d['edges_elec']: W0[u,v]+=float(w)*0.5; W0[v,u]+=float(w)*0.5
np.fill_diagonal(W0,0); W0=W0/max(W0.max(),1)*0.8

G_anat=nx.from_numpy_array((W0>0.05).astype(float)).to_undirected()
G_anat.remove_edges_from(nx.selfloop_edges(G_anat))
Ms_anat=community_louvain.best_partition(G_anat)
ms_vec=np.array([Ms_anat.get(i,0) for i in range(N)])
n_comm=len(set(ms_vec))
print(f"N={N}, 解剖社区数={n_comm}")

def make_freq_bias(ms_vec, delta_f=0.07, noise_f=0.01):
    """
    为每个节点分配内禀频率：
      - 同社区：基础频率 f_c + 小随机扰动
      - 跨社区：不同基础频率（相差delta_f）
    Fries 2015: θ(4-8Hz)内社区同步，delta_f对应归一化频率差
    """
    comms = sorted(set(ms_vec))
    n_c = len(comms)
    # 每个社区分配基础频率，均匀分布在[0.05, 0.05+delta_f*(n_c-1)]
    base_freqs = {c: 0.05 + i*delta_f for i,c in enumerate(comms)}
    freqs = np.array([base_freqs[ms_vec[i]] for i in range(N)])
    freqs += np.random.uniform(-noise_f, noise_f, N)
    freqs = np.clip(freqs, 0.01, 0.5)
    return freqs

def simulate_v38(W_in, steps=7000,
                 alpha_fep=0.4,
                 delta_f=0.07,      # 社区间频率差（归一化）
                 noise_f=0.01,      # 社区内频率噪声
                 amp_osc=0.08,      # 振荡幅度（相对于激活均值）
                 report_every=1000):
    W=W_in.copy()
    h=np.random.uniform(0.1,0.3,N)
    H=np.zeros((steps,N))
    theta_bcm=np.ones(N)*0.15
    h_pred=h.copy()
    ETA_BASE=0.005

    # 分配社区频率偏置
    freqs=make_freq_bias(ms_vec, delta_f=delta_f, noise_f=noise_f)
    phases=np.random.uniform(0,2*np.pi,N)  # 初始随机相位

    F_hist=[]; Gst_hist=[]

    for t in range(steps):
        # 振荡偏置（Fries CTC核心）
        phases += 2*np.pi*freqs   # 相位推进
        osc_bias = amp_osc * np.sin(phases)

        # 梯度电位 + 振荡偏置
        noise=np.random.normal(0,0.03,N)
        h_new=np.tanh(W.T@h + osc_bias + noise)
        h=h*0.95+h_new*0.05; h=np.clip(h,0,1); H[t]=h

        # FEP惊讶度（v33最优机制，保留）
        surprise=np.abs(h-h_pred)
        h_pred=h_pred*0.9+h*0.1

        if t%100==99 and t>200:
            h_hist=H[max(0,t-100):t].mean(0)
            theta_bcm=theta_bcm*0.998+(h_hist**2)*0.002
            theta_bcm=np.clip(theta_bcm,0.03,0.50)

            pre=H[t-1]; post=h
            surprise_n=np.abs(post-h_pred)
            eta_n=ETA_BASE*(1+alpha_fep*surprise_n)
            dW=eta_n[:,None]*np.outer(post-theta_bcm,pre)-ETA_BASE*np.outer(pre,post)
            W=np.clip(W+dW*0.12,0,1.5); np.fill_diagonal(W,0)

            act=h_hist
            W[:,act>0.40]*=0.96; W[:,act<0.04]*=1.04
            W=np.clip(W,0,1.5)

        eps2=(h-np.tanh(W.T@h_pred))**2
        F_hist.append(float(eps2.mean()))

        if t%500==499 and t>1000:
            FC=np.corrcoef(H[max(0,t-500):t].T)
            np.fill_diagonal(FC,0); FC=np.nan_to_num(FC)
            Gf=nx.from_numpy_array(np.abs(FC))
            MT=community_louvain.best_partition(Gf)
            mt=[MT.get(i,0) for i in range(N)]
            nmi=float(normalized_mutual_info_score(ms_vec,mt))
            Gst_hist.append((t,nmi))
            if t%2000==499:
                print(f"  step={t}: NMI={nmi:.4f} F={F_hist[-1]:.5f}", flush=True)

        if t%report_every==report_every-1:
            act=H[max(0,t-200):t].mean()
            print(f"  step={t+1}/{steps}: act={act:.3f} F={F_hist[-1]:.5f}", flush=True)

    return W,H,F_hist,Gst_hist,freqs

def compute_Sc(W):
    adj=(W>0.05).astype(float); np.fill_diagonal(adj,0)
    G=nx.from_numpy_array(adj).to_undirected(); G.remove_edges_from(nx.selfloop_edges(G))
    comps=list(nx.connected_components(G))
    C=max(len(c) for c in comps)/N if comps else 0
    core=nx.core_number(G); H_=min(max(core.values())/max(np.log2(N+1),1),1.)
    part=community_louvain.best_partition(G)
    Qr=community_louvain.modularity(part,G); Qrand=1/np.sqrt(max(G.number_of_edges(),1))
    M=max(0.,min((Qr-Qrand)/max(1-Qrand,1e-6),1.))
    try:
        lcc=G.subgraph(max(comps,key=len)).copy(); nodes=list(lcc.nodes)[:60]; lens=[]
        for n_ in nodes:
            sp=nx.single_source_shortest_path_length(lcc,n_); lens.extend(sp.values())
        L_real=np.mean(lens) if lens else N
        k_mean=max(np.mean([deg for _,deg in G.degree()]),2)
        L_rand=np.log(N)/np.log(k_mean); C_rand=k_mean/(N-1)
        sigma=(nx.average_clustering(G)/max(C_rand,1e-6))/(L_real/max(L_rand,1e-6))
    except: sigma=1.
    R=float(np.tanh(max(0.,sigma-1.)))
    sc=float((max(C,1e-6)*max(H_,1e-6)*max(M,1e-6)*max(R,1e-6))**0.25)
    return sc,{'C':round(C,4),'H':round(H_,4),'M':round(M,4),'R_sw':round(R,4),'sigma':round(sigma,3)}

def compute_Tc(H):
    T,N_=H.shape
    act=H.mean(1); acf=np.correlate(act-act.mean(),act-act.mean(),'full')
    acf=acf[T-1:]/(acf[T-1]+1e-8); lam=float(np.clip(acf[1],0,2)); lam_n=1/(1+abs(lam-1))
    idx=np.random.choice(N_,min(50,N_),replace=False); corrs=[]
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
            sub=seg[:,valid]; fc=np.corrcoef(sub.T); fc_list.append(fc[np.triu_indices(len(fc),k=1)])
    if len(fc_list)>5:
        ml=min(len(x) for x in fc_list); arr=np.array([x[:ml] for x in fc_list])
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
        DFC=1-np.abs(FC[np.ix_(nn,nn)]); da_f=DA[np.triu_indices(len(nn),k=1)]
        dfc_f=DFC[np.triu_indices(len(nn),k=1)]
        mr,_=pearsonr(da_f,dfc_f) if da_f.std()>1e-6 and dfc_f.std()>1e-6 else (0.,0.)
    except: mr=0.
    sg=float(np.sign(mr)) if mr!=0 else 1.
    return float(nmi*sg),{'NMI':round(nmi,4),'mantel_r':round(float(mr),4)}

# delta_f扫描：社区间频率差
configs = [
    ('v38_df05', dict(delta_f=0.05, amp_osc=0.06), 'Δf=0.05，小振幅'),
    ('v38_df07', dict(delta_f=0.07, amp_osc=0.08), 'Δf=0.07，中振幅（文献值）'),
    ('v38_df10', dict(delta_f=0.10, amp_osc=0.10), 'Δf=0.10，强分离'),
]

results={
    'experiment':'v38_freq_bias','N':N,'alpha':ALPHA,
    'bio_basis':'Fries 2015 CTC: theta coherence within community, gamma modulation across',
    'hw_mapping':'ReRAM relaxation oscillation frequency difference per community group',
    'baselines':{'v33':{'Gamma_st':0.187,'CST_snn':1.268}},
    'target':{'Gamma_st':0.30,'CST_snn':1.618},
    'systems':{}
}

for tag,params,desc in configs:
    print(f"\n{'='*60}\n配置: {tag} ({desc})")
    W_ev,H_ev,F_hist,Gst_hist,freqs=simulate_v38(W0,steps=7000,**params)
    H_use=H_ev[-1500:]
    sc,sc_c=compute_Sc(W_ev)
    tc,tc_c=compute_Tc(H_use)
    gst,gst_c=compute_Gst(W_ev,H_use)
    csts={k:float((sc*tc)*np.exp(a*gst)) for k,a in ALPHA.items()}
    F_arr=np.array(F_hist)
    F_drop=float(np.mean(F_arr[:200])-np.mean(F_arr[-200:]))
    freq_spread=float(freqs.std())

    print(f"  Sc={sc:.4f} Tc={tc:.4f} Γst={gst:.4f}")
    print(f"  Sc: H={sc_c['H']:.3f} M={sc_c['M']:.3f}")
    print(f"  Tc: Φ={tc_c['Phi']:.4f} Ψ={tc_c['Psi']:.4f}")
    print(f"  CST(snn)={csts['snn']:.4f} → {lvl(csts['snn'])}")
    print(f"  频率分布: std={freq_spread:.4f}  Γst vs v33: {gst-0.187:+.4f}")

    results['systems'][tag]={
        'desc':desc,'params':params,
        'Sc':sc,'Tc':tc,'Gamma_st':gst,
        'sc_components':sc_c,'tc_components':tc_c,'gst_components':gst_c,
        **{f'CST_{k}':v for k,v in csts.items()},
        'level_snn':lvl(csts['snn']),
        'freq_spread':freq_spread,'F_drop':round(F_drop,6),
        'Gamma_st_vs_v33':round(gst-0.187,4),
        'gst_trajectory':Gst_hist[-6:]
    }

print(f"\n{'='*60}")
print(f"v38汇总  (v33基线: Γst=0.187, CST=1.268 | 目标: Γst≥0.30, CST≥1.618)")
print(f"{'配置':<14} {'Γst':>7} {'ΔNMI':>8} {'CST_snn':>9} {'H':>6} {'Φ':>6} {'等级'}")
print('-'*70)
for tag,r in results['systems'].items():
    sc=r['sc_components']; tc=r['tc_components']
    print(f"{tag:<14} {r['Gamma_st']:>7.4f} {r['Gamma_st_vs_v33']:>+8.4f} "
          f"{r['CST_snn']:>9.4f} {sc['H']:>6.3f} {tc['Phi']:>6.4f} {r['level_snn']}")

best=max(results['systems'],key=lambda k:results['systems'][k]['CST_snn'])
br=results['systems'][best]; phi=1.61803
goal='✅ 跨越L3(φ)' if br['CST_snn']>=phi else f"距L3差{phi-br['CST_snn']:.4f}"
results['best']=best
results['conclusion']=(f"最佳{best}: Γst={br['Gamma_st']:.4f}, CST={br['CST_snn']:.4f}, "
                       f"{br['level_snn']}. {goal}")
print(f"\n最佳: {best} | Γst={br['Gamma_st']:.4f} | CST={br['CST_snn']:.4f} | {goal}")

with open(OUT,'w') as f: json.dump(results,f,indent=2)
print(f"✅ 写入 {OUT}")
