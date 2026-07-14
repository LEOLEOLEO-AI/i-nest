#!/usr/bin/env python3
"""
v37实验：社区感知修剪（Community-Aware Pruning）
生物第一性依据：Γst瓶颈诊断
  → 四条规则足以驱动SOC/Sc，但Rule4是"flat修剪"——不区分模块内外
  → 生物脑修剪方向性：模块内强连接保留，模块间弱连接优先剪
  → Meunier 2010 / Bassett 2010：层级模块性是结构-功能对齐的核心机制

Rule4升级（不增加规则，只改判断逻辑）：
  原版：W_ij < W_min → 剪除
  v37：W_ij < W_min × β_intra    （模块内，β_intra > 1，更难被剪）
       W_ij < W_min × β_inter    （模块间，β_inter < 1，更容易被剪）
  β_intra=1.5, β_inter=0.6  （van den Heuvel 2011 rich-club文献支撑）

目标：Γst从0.187→0.30+，CST(snn)≥1.618（L3适应 φ）
"""
import numpy as np, json, networkx as nx
from sklearn.metrics import normalized_mutual_info_score
from scipy.stats import pearsonr
import community as community_louvain, warnings
warnings.filterwarnings('ignore')
np.random.seed(42)

DATA = '/home/work/.openclaw/workspace/sdi_sim/celegans_sim/connectome_v8_data.json'
OUT  = '/home/work/.openclaw/workspace/iNEST_Sim_Research/exp_next/v37_community_pruning/v37_results.json'

ALPHA = {'graded':np.log(13),'snn':np.log(32),'cortex':np.log(50)}
THRESHOLDS = [(4.669,'L6超级(δ)'),(3.14159,'L5通用(π)'),(2.71828,'L4创造(e)'),
              (1.61803,'L3适应(φ)'),(1.00000,'L2反应(1)'),(0.70711,'L1感知(1/√2)'),(0.,'L0反射')]
def lvl(c):
    for t,n in THRESHOLDS:
        if c>=t: return n
    return 'L0反射'

# ── 加载连接组 ──
with open(DATA) as f: d=json.load(f)
N=d['N']
W0=np.zeros((N,N))
for u,v,w in d['edges_chem']: W0[u,v]+=float(w)
for u,v,w in d['edges_elec']: W0[u,v]+=float(w)*0.5; W0[v,u]+=float(w)*0.5
np.fill_diagonal(W0,0); W0=W0/max(W0.max(),1)*0.8

# 解剖社区（固定，基于初始connectome）
G_anat=nx.from_numpy_array((W0>0.05).astype(float)).to_undirected()
G_anat.remove_edges_from(nx.selfloop_edges(G_anat))
Ms_anat=community_louvain.best_partition(G_anat)
ms_vec=np.array([Ms_anat.get(i,0) for i in range(N)])
n_comm=len(set(ms_vec))
# 社区掩码矩阵：同社区=1，跨社区=0
same_comm = (ms_vec[:,None]==ms_vec[None,:]).astype(float)
np.fill_diagonal(same_comm,0)
print(f"N={N}, 解剖社区数={n_comm}, 社区内突触比={same_comm.sum()/(N*(N-1)):.3f}")

# ══════════════════════════════════════════════════════════
# v37核心：社区感知修剪引擎
# ══════════════════════════════════════════════════════════
def simulate_v37(W_in, steps=7000,
                 alpha_fep=0.4,      # v33最优机制保留
                 beta_intra=1.5,     # 模块内修剪阈值倍数（难剪）
                 beta_inter=0.6,     # 模块间修剪阈值倍数（易剪）
                 W_min=0.05,         # 基础修剪阈值
                 prune_interval=300, # 修剪间隔（生物：发育级，最慢）
                 report_every=1000):
    """
    Rule4升级：社区感知修剪
    生物依据：
      - Meunier et al. 2010: 层级模块性 → 模块内连接优先保留
      - van den Heuvel & Sporns 2011: rich-club → 高度枢纽节点间连接保护
      - Bassett et al. 2010: 发育期活动依赖修剪具有方向性
    """
    W=W_in.copy()
    h=np.random.uniform(0.1,0.3,N)
    H=np.zeros((steps,N))
    theta_bcm=np.ones(N)*0.15
    h_pred=h.copy()
    ETA_BASE=0.005
    # 动态社区标签（每500步更新，追踪功能社区演化）
    func_comm=ms_vec.copy()  # 初始化为解剖社区

    F_hist=[]; Gst_hist=[]; prune_stats=[]

    for t in range(steps):
        # ── 梯度电位激活 ──
        noise=np.random.normal(0,0.03,N)
        h_new=np.tanh(W.T@h+noise)
        h=h*0.95+h_new*0.05; h=np.clip(h,0,1); H[t]=h

        # ── FEP惊讶度（v33最优机制）──
        surprise=np.abs(h-h_pred)
        h_pred=h_pred*0.9+h*0.1
        surprise_g=float(surprise.mean())

        # ── 每100步：BCM + FEP-STDP ──
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

        # ── 每300步：社区感知修剪（Rule4升级核心）──
        if t%prune_interval==prune_interval-1 and t>600:

            # Step1：更新功能社区（基于最近500步的FC）
            if t>1000:
                FC=np.corrcoef(H[max(0,t-500):t].T)
                np.fill_diagonal(FC,0); FC=np.nan_to_num(FC)
                Gf=nx.from_numpy_array(np.abs(FC))
                fc_dict=community_louvain.best_partition(Gf)
                func_comm=np.array([fc_dict.get(i,0) for i in range(N)])

            # Step2：计算每条突触的社区关系
            # 判断标准：解剖社区（固定）+ 功能社区（动态）双重对齐
            struct_same=same_comm  # 解剖社区同属矩阵
            func_same=(func_comm[:,None]==func_comm[None,:]).astype(float)
            np.fill_diagonal(func_same,0)

            # 对齐矩阵：两者都同 → 最强保护；一个同 → 中等；都不同 → 最易剪
            align_score = 0.5*struct_same + 0.5*func_same  # ∈ {0, 0.5, 1.0}

            # Step3：社区感知修剪阈值
            # W_threshold_ij = W_min × [beta_inter + (beta_intra-beta_inter)×align_score_ij]
            W_thresh = W_min * (beta_inter + (beta_intra-beta_inter)*align_score)

            # Step4：应用修剪
            prune_mask = (W > 0) & (W < W_thresh)
            n_pruned_intra = int((prune_mask * struct_same).sum())
            n_pruned_inter = int((prune_mask * (1-struct_same)).sum())
            W[prune_mask] = 0.0
            np.fill_diagonal(W,0)

            prune_stats.append({
                't':t, 'n_intra':n_pruned_intra, 'n_inter':n_pruned_inter,
                'ratio': n_pruned_inter/max(n_pruned_intra+1,1)
            })
            if t%2000==prune_interval-1:
                print(f"  step={t}: 修剪 intra={n_pruned_intra} inter={n_pruned_inter} "
                      f"比值={n_pruned_inter/max(n_pruned_intra+1,1):.2f}", flush=True)

        # ── 自由能监控 ──
        eps2=(h-np.tanh(W.T@h_pred))**2
        F=float(eps2.mean())
        F_hist.append(F)

        # ── 在线Γst（每500步）──
        if t%500==499 and t>1000:
            FC=np.corrcoef(H[max(0,t-500):t].T)
            np.fill_diagonal(FC,0); FC=np.nan_to_num(FC)
            Gf=nx.from_numpy_array(np.abs(FC))
            MT=community_louvain.best_partition(Gf)
            mt=[MT.get(i,0) for i in range(N)]
            nmi=float(normalized_mutual_info_score(ms_vec,mt))
            Gst_hist.append((t,nmi,F))
            if t%2000==499:
                print(f"  step={t}: Γst_NMI={nmi:.4f} F={F:.5f}", flush=True)

        if t%report_every==report_every-1:
            act=H[max(0,t-200):t].mean()
            print(f"  step={t+1}/{steps}: act={act:.3f} F={F:.5f}", flush=True)

    return W,H,F_hist,Gst_hist,prune_stats

# ── 度量函数 ──
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

# ── 三个配置：beta_intra/beta_inter参数扫描 ──
configs = [
    # (tag, beta_intra, beta_inter, desc)
    ('v37_mild',   dict(alpha_fep=0.4, beta_intra=1.3, beta_inter=0.7, W_min=0.05), '轻度社区感知'),
    ('v37_strong', dict(alpha_fep=0.4, beta_intra=1.5, beta_inter=0.6, W_min=0.05), '强社区感知（文献值）'),
    ('v37_max',    dict(alpha_fep=0.4, beta_intra=2.0, beta_inter=0.4, W_min=0.05), '最强社区感知'),
]

results={
    'experiment':'v37_community_pruning','N':N,'alpha':ALPHA,
    'bio_basis': {
        'Meunier2010': 'Hierarchical modularity - intra-community connections preserved',
        'vandenHeuvel2011': 'Rich-club - hub-to-hub connections protected (beta_intra)',
        'Bassett2010': 'Developmental pruning is directional, not flat'
    },
    'baselines':{'v33':{'Gamma_st':0.187,'CST_snn':1.268,'NMI':0.187}},
    'target':{'Gamma_st':0.30,'CST_snn':1.618,'level':'L3适应(φ)'},
    'systems':{}
}

for tag,params,desc in configs:
    print(f"\n{'='*60}\n配置: {tag} ({desc})")
    W_ev,H_ev,F_hist,Gst_hist,prune_s=simulate_v37(W0,steps=7000,**params)

    H_use=H_ev[-1500:]
    sc,sc_c=compute_Sc(W_ev)
    tc,tc_c=compute_Tc(H_use)
    gst,gst_c=compute_Gst(W_ev,H_use)
    csts={k:float((sc*tc)*np.exp(a*gst)) for k,a in ALPHA.items()}

    # 修剪统计
    if prune_s:
        intra_total=sum(p['n_intra'] for p in prune_s)
        inter_total=sum(p['n_inter'] for p in prune_s)
        ratio=inter_total/max(intra_total+1,1)
    else:
        intra_total=inter_total=ratio=0

    F_arr=np.array(F_hist)
    F_drop=float(np.mean(F_arr[:200]))-float(np.mean(F_arr[-200:]))

    print(f"  Sc={sc:.4f} | Tc={tc:.4f} | Γst={gst:.4f}")
    print(f"  Sc分量: C={sc_c['C']} H={sc_c['H']} M={sc_c['M']} R_sw={sc_c['R_sw']}")
    print(f"  CST(snn)={csts['snn']:.4f} → {lvl(csts['snn'])}")
    print(f"  修剪: inter={inter_total} intra={intra_total} 比值={ratio:.2f}（>1说明社区感知生效）")
    print(f"  Γst vs v33基线: {gst-0.187:+.4f}")

    results['systems'][tag]={
        'desc':desc,'params':params,
        'Sc':sc,'Tc':tc,'Gamma_st':gst,
        'sc_components':sc_c,'tc_components':tc_c,'gst_components':gst_c,
        **{f'CST_{k}':v for k,v in csts.items()},
        'level_snn':lvl(csts['snn']),
        'pruning':{'inter_total':inter_total,'intra_total':intra_total,'inter_intra_ratio':round(ratio,3)},
        'F_drop':round(F_drop,6),
        'Gamma_st_vs_v33':round(gst-0.187,4),
        'gst_trajectory':Gst_hist[-5:]
    }

# ── 汇总 ──
print(f"\n{'='*60}")
print(f"v37汇总  (v33基线: Γst=0.187, CST=1.268 | 目标: Γst≥0.30, CST≥1.618)")
print(f"{'配置':<14} {'Γst':>7} {'ΔNMI':>8} {'CST_snn':>9} {'inter/intra':>12} {'等级'}")
print('-'*70)
for tag,r in results['systems'].items():
    ratio=r['pruning']['inter_intra_ratio']
    print(f"{tag:<14} {r['Gamma_st']:>7.4f} {r['Gamma_st_vs_v33']:>+8.4f} "
          f"{r['CST_snn']:>9.4f} {ratio:>12.2f} {r['level_snn']}")

best=max(results['systems'],key=lambda k:results['systems'][k]['CST_snn'])
br=results['systems'][best]; phi=1.61803
goal='✅ 跨越L3(φ)' if br['CST_snn']>=phi else f"距L3差{phi-br['CST_snn']:.4f}"
results['best']=best
results['conclusion']=(
    f"最佳{best}: Γst={br['Gamma_st']:.4f}(NMI={br['gst_components']['NMI']:.4f}), "
    f"CST_snn={br['CST_snn']:.4f}, {br['level_snn']}. L3: {goal}. "
    f"inter/intra修剪比={br['pruning']['inter_intra_ratio']:.2f}"
)
print(f"\n最佳: {best} | Γst={br['Gamma_st']:.4f} | CST={br['CST_snn']:.4f} | {goal}")

with open(OUT,'w') as f: json.dump(results,f,indent=2)
print(f"✅ 写入 {OUT}")
