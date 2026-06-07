#!/usr/bin/env python3
"""
v40：双频θ+γ振荡（突破Γst-Φ对冲悖论）
生物第一性：
  Buzsáki & Draguhn 2004 Science: θ-γ耦合是海马/皮层信息整合的基础
  Fries 2015 Neuron CTC: θ(4-8Hz)社区内锁相 + γ(30-80Hz)全局调制
  Canolty & Knight 2010 TICS: 相位-幅度耦合(PAC) — θ相位调制γ幅度

核心设计：
  θ分量：f_θ_i = f_base + community_offset_i（社区内频率近→锁相→Γst↑）
  γ分量：f_γ = 全局公共频率（所有节点同频→全局Φ↑）
  PAC：γ幅度 = amp_γ × (1 + PAC_depth × cos(θ_phase))  ← θ相位调制γ幅度

h_i(t) = tanh(W·h + amp_θ·sin(θ_i) + amp_γ·(1+PAC·cos(θ_i))·sin(γ_global) + noise)

硅基映射（SDSoW天然支持）：
  θ振荡 → ReRAM弛豫振荡（器件内禀，按社区分组调频）
  γ振荡 → 芯片级全局时钟（公共节拍）
  PAC   → 时钟门控深度（硬件寄存器可调）

目标：Γst≥0.28 AND Φ≥0.40 → CST(snn)≥1.618（L3适应φ=1.618）
"""
import numpy as np, json, networkx as nx
from sklearn.metrics import normalized_mutual_info_score
from scipy.stats import pearsonr
import community as community_louvain, warnings
warnings.filterwarnings('ignore')
np.random.seed(42)

DATA = '/home/work/.openclaw/workspace/sdi_sim/celegans_sim/connectome_v8_data.json'
OUT  = '/home/work/.openclaw/workspace/iNEST_Sim_Research/exp_next/v40_dual_freq/v40_results.json'
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

def make_theta_freqs(delta_f=0.10, noise_f=0.008):
    """θ频率：按社区分组，社区内相近，跨社区差delta_f（Fries 2015）"""
    comms=sorted(set(ms_vec))
    base={c: 0.04 + i*delta_f for i,c in enumerate(comms)}
    freqs=np.array([base[ms_vec[i]] for i in range(N)])
    freqs+=np.random.uniform(-noise_f,noise_f,N)
    return np.clip(freqs,0.01,0.45)

def simulate_v40(W_in, steps=8000,
                 alpha_fep=0.45,
                 # θ参数（社区锁相，维持Γst）
                 delta_f_theta=0.10,
                 amp_theta=0.08,
                 # γ参数（全局同步，维持Φ）
                 f_gamma=0.35,       # 全局γ频率（所有节点相同）
                 amp_gamma=0.06,
                 # PAC参数（θ相位调制γ幅度，Canolty 2010）
                 pac_depth=0.5,      # 0=无PAC，1=全调制
                 report_every=1000):

    W=W_in.copy()
    h=np.random.uniform(0.1,0.3,N)
    H=np.zeros((steps,N))
    theta_bcm=np.ones(N)*0.15
    h_pred=h.copy()
    ETA_BASE=0.005

    # θ：每个节点的社区频率（不同社区不同频率）
    theta_freqs=make_theta_freqs(delta_f=delta_f_theta)
    theta_phases=np.random.uniform(0,2*np.pi,N)
    # γ：全局公共频率（所有节点同频，维持全局Φ）
    gamma_phase=0.0

    F_hist=[]; Gst_hist=[]

    for t in range(steps):
        # θ相位推进（每节点独立）
        theta_phases += 2*np.pi*theta_freqs
        # γ相位推进（全局公共）
        gamma_phase  += 2*np.pi*f_gamma

        # PAC：γ幅度被θ相位调制
        # Canolty 2010: 低频相位 → 高频幅度调制
        pac_mod = 1.0 + pac_depth * np.cos(theta_phases)   # [1-pac, 1+pac]
        
        # 双频驱动
        theta_drive = amp_theta * np.sin(theta_phases)          # 社区特异性
        gamma_drive = amp_gamma * pac_mod * np.sin(gamma_phase) # 全局+PAC调制

        noise=np.random.normal(0,0.025,N)
        h_new=np.tanh(W.T@h + theta_drive + gamma_drive + noise)
        h=h*0.95+h_new*0.05; h=np.clip(h,0,1); H[t]=h

        # FEP惊讶度（v33最优机制）
        surprise=np.abs(h-h_pred)
        h_pred=h_pred*0.9+h*0.1

        # BCM + FEP-STDP（每100步）
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

        # 在线Γst监控（每500步）
        if t%500==499 and t>1000:
            FC=np.corrcoef(H[max(0,t-500):t].T)
            np.fill_diagonal(FC,0); FC=np.nan_to_num(FC)
            Gf=nx.from_numpy_array(np.abs(FC))
            MT=community_louvain.best_partition(Gf)
            mt=[MT.get(i,0) for i in range(N)]
            nmi=float(normalized_mutual_info_score(ms_vec,mt))
            # 在线Φ估计
            idx=np.random.choice(N,min(40,N),replace=False)
            corrs=[abs(pearsonr(H[t-500:t,i],H[t-500:t,j])[0])
                   for i in idx for j in idx if i<j
                   and H[t-500:t,i].std()>1e-4 and H[t-500:t,j].std()>1e-4]
            phi_est=float(np.mean(corrs)) if corrs else 0
            Gst_hist.append((t,nmi,phi_est))
            if t%2000==499:
                print(f"  step={t}: NMI={nmi:.4f} Φ_est={phi_est:.4f} F={F_hist[-1]:.5f}", flush=True)

        if t%report_every==report_every-1:
            act=H[max(0,t-200):t].mean()
            print(f"  step={t+1}/{steps}: act={act:.3f} F={F_hist[-1]:.5f}", flush=True)

    return W,H,F_hist,Gst_hist

# ── 度量函数（与之前一致）──
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

# ── 参数扫描：PAC深度 × γ幅度 ──
configs=[
    ('v40_a', dict(amp_theta=0.08, f_gamma=0.35, amp_gamma=0.05, pac_depth=0.3, alpha_fep=0.45),
     '弱PAC(0.3)，小γ'),
    ('v40_b', dict(amp_theta=0.08, f_gamma=0.35, amp_gamma=0.06, pac_depth=0.5, alpha_fep=0.45),
     '中PAC(0.5)，中γ（文献值）'),
    ('v40_c', dict(amp_theta=0.08, f_gamma=0.35, amp_gamma=0.08, pac_depth=0.7, alpha_fep=0.45),
     '强PAC(0.7)，大γ'),
    ('v40_d', dict(amp_theta=0.10, f_gamma=0.40, amp_gamma=0.06, pac_depth=0.5, alpha_fep=0.50),
     '强θ+中PAC+强FEP'),
]

results={
    'experiment':'v40_dual_freq','N':N,'alpha':ALPHA,
    'bio_basis':{
        'Buzsaki2004':'theta-gamma coupling: hippocampal/cortical information integration',
        'Fries2015':'CTC: theta phase locks within community, gamma modulates globally',
        'Canolty2010':'PAC: theta phase modulates gamma amplitude'
    },
    'hw_mapping':{
        'theta':'ReRAM relaxation oscillation, community-grouped frequency',
        'gamma':'chip-level global clock (common beat)',
        'PAC':'clock-gating depth (hardware register)'
    },
    'baselines':{
        'v33':{'Gamma_st':0.187,'Phi':0.576,'CST_snn':1.268,'level':'L2反応'},
        'v38':{'Gamma_st':0.274,'Phi':0.091,'CST_snn':0.841,'level':'L1感知'},
    },
    'target':{'Gamma_st':0.28,'Phi':0.40,'CST_snn':1.618,'level':'L3适应(φ)'},
    'systems':{}
}

for tag,params,desc in configs:
    print(f"\n{'='*60}\n配置: {tag} ({desc})")
    W_ev,H_ev,F_hist,Gst_hist=simulate_v40(W0,steps=8000,**params)
    H_use=H_ev[-1500:]
    sc,sc_c=compute_Sc(W_ev)
    tc,tc_c=compute_Tc(H_use)
    gst,gst_c=compute_Gst(W_ev,H_use)
    csts={k:float((sc*tc)*np.exp(a*gst)) for k,a in ALPHA.items()}
    F_arr=np.array(F_hist)
    F_converged = bool(np.mean(F_arr[-200:]) < np.mean(F_arr[:200]))

    phi_val=tc_c['Phi']
    dual_ok = gst>=0.28 and phi_val>=0.40
    l3_ok   = csts['snn']>=1.618

    print(f"  Sc={sc:.4f} Tc={tc:.4f} Γst={gst:.4f}")
    print(f"  Sc: H={sc_c['H']:.3f} M={sc_c['M']:.3f}")
    print(f"  Tc: Φ={phi_val:.4f} Ψ={tc_c['Psi']:.4f} Θ={tc_c['Theta']:.3f}")
    print(f"  CST(snn)={csts['snn']:.4f} → {lvl(csts['snn'])}")
    print(f"  双目标: Γst≥0.28={'✅' if gst>=0.28 else '❌'}  Φ≥0.40={'✅' if phi_val>=0.40 else '❌'}  L3={'✅' if l3_ok else '❌'}")
    print(f"  Δ(Γst vs v33)={gst-0.187:+.4f}  Δ(Φ vs v33)={phi_val-0.576:+.4f}", flush=True)

    results['systems'][tag]={
        'desc':desc,'params':params,
        'Sc':sc,'Tc':tc,'Gamma_st':gst,
        'sc_components':sc_c,'tc_components':tc_c,'gst_components':gst_c,
        **{f'CST_{k}':v for k,v in csts.items()},
        'level_snn':lvl(csts['snn']),
        'F_converged':F_converged,
        'dual_target_met':dual_ok,
        'L3_met':l3_ok,
        'Gamma_st_vs_v33':round(gst-0.187,4),
        'Phi_vs_v33':round(phi_val-0.576,4),
        'gst_trajectory':Gst_hist[-6:]
    }

# ── 汇总 ──
print(f"\n{'='*60}")
print(f"v40汇总")
print(f"基线 v33: Γst=0.187 Φ=0.576 CST=1.268  目标: Γst≥0.28 Φ≥0.40 CST≥1.618")
print(f"{'配置':<10} {'Γst':>7} {'Φ':>7} {'CST_snn':>9} {'双目标':>7} {'等级'}")
print('-'*60)
for tag,r in results['systems'].items():
    dual='✅' if r['dual_target_met'] else '❌'
    print(f"{tag:<10} {r['Gamma_st']:>7.4f} {r['tc_components']['Phi']:>7.4f} "
          f"{r['CST_snn']:>9.4f} {dual:>7}  {r['level_snn']}")

best=max(results['systems'],key=lambda k:results['systems'][k]['CST_snn'])
br=results['systems'][best]; phi=1.61803
goal='✅ 跨越L3(φ)' if br['CST_snn']>=phi else f"距L3差{phi-br['CST_snn']:.4f}"
results['best']=best
results['conclusion']=(
    f"最佳{best}: Γst={br['Gamma_st']:.4f}, Φ={br['tc_components']['Phi']:.4f}, "
    f"CST={br['CST_snn']:.4f}, {br['level_snn']}. {goal}. "
    f"双目标={'✅达成' if br['dual_target_met'] else '❌未达成'}"
)
print(f"\n{results['conclusion']}")

with open(OUT,'w') as f: json.dump(results,f,indent=2)
print(f"✅ 写入 {OUT}")
