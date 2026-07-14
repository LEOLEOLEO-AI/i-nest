"""
SDI 实验十九 — CST参数第一性审查修订版
==========================================
基于 CST_Parameter_Review_v2.md 的系统性修订：

修订项（全部有NCS权威文献依据）：
  λ_eff: 逐步比→ κ临界指数 exp(-|κ-1|)
         [Beggs & Plenz 2003 J.Neurosci. 23:11167]
         [Priesemann et al. 2014 PLOS Comput.Biol.]

  Φ:     Hilbert/PLV → FC异质性 CV(FC)
         [Bullmore & Sporns 2009 Nat.Rev.Neurosci. 10:186]
         原Φ需要稀疏振荡激活，当前80%激活率下物理前提缺失

  Ψ:     总变化量corr → 相对权重变化率 ||ΔW||/||W||
         [Bhatt et al. 2009 Nature 462:313]
         [Turrigiano 2012 CSHP]

  Γst:   瞬时50步窗口FC → EMA慢速FC (β=0.99)
         [Honey et al. 2009 PNAS 106:2035]
         [Bullmore & Sporns 2009]

不变项（已验证正确）：
  Sc四分量(C/H/M/R_sw)、Θ、α、四规则参数
"""
import numpy as np, json, os, time
import networkx as nx
from collections import defaultdict
from scipy.stats import entropy

BASE    = '/home/work/.openclaw/workspace/sdi_sim'
OUT     = os.path.join(BASE, 'exp19_reviewed_results.json')
CE_DATA = os.path.join(BASE, 'celegans_sim/connectome_v8_data.json')

# ── 继承实验十八全部参数 ──────────────────────────────────
THETA_LTP=60; THETA_LTD=50; LTP_DECAY_INT=500; EL_WT_BOOST=1.5
GROW_INT=50; P_GROW=0.05; W_INIT_LO=0.05; W_INIT_HI=0.10
EI_RATIO=0.20; INH_RATIO=7.0
SCALING_INT=200; ACT_LO=0.03; ACT_HI=0.10
SCALE_UP=1.05; SCALE_DN=0.95
PRUNE_INT=200; P_PRUNE=0.05; MIN_EDGES=2; COMP_THR=0.5
TAU_MU=np.log(20); TAU_SIGMA=1.0; TAU_MIN=5.0; TAU_MAX=200.0
INTRA_SIGMA=0.3; HIST_LEN=100

# Γst EMA参数 [Honey 2009]
FC_EMA_BETA = 0.99   # 慢速时间常数≈100步

N_STEPS=10000; LOG_INT=1000; SEEDS=[42,7,13]
ALPHA_MAP={'WS_300':3.47,'C_elegans':2.56,'Human_HCP':3.91}
NETWORKS={
    'WS_300':   {'type':'ws','N':300,'k':12,'p':0.1},
    'C_elegans':{'type':'ce'},
    'Human_HCP':{'type':'ws','N':80,'k':8,'p':0.1},
}

# ── 初始化（继承）────────────────────────────────────────
def make_ws(N,k,p,rng):
    W=np.zeros((N,N),dtype=np.float32)
    for i in range(N):
        for d in range(1,k//2+1):
            j=(i+d)%N; W[i,j]=W[j,i]=rng.uniform(0.1,0.35)
    for i in range(N):
        for d in range(1,k//2+1):
            if rng.random()<p:
                j=(i+d)%N; nj=rng.randint(0,N)
                if nj!=i and W[i,nj]==0: W[i,nj]=W[i,j]; W[i,j]=0
    np.fill_diagonal(W,0); return W

def load_ce(rng):
    with open(CE_DATA) as f: d=json.load(f)
    N=d.get('N',279); W=np.zeros((N,N),dtype=np.float32)
    EL=np.zeros((N,N),dtype=bool)
    chem=[(int(r[0]),int(r[1]),float(r[2])) for r in d.get('edges_chem',[])]
    if chem:
        mx=max(w for _,_,w in chem)
        for s,t,w in chem:
            if s<N and t<N: W[s,t]=0.10+0.30*(w/mx)
    for row in d.get('edges_elec',[]):
        s,t=int(row[0]),int(row[1])
        if s<N and t<N: W[s,t]=W[t,s]=0.30; EL[s,t]=EL[t,s]=True
    return W,EL,N

def assign_EI(N,rng):
    t=np.ones(N,dtype=np.float32)
    t[rng.choice(N,int(N*EI_RATIO),replace=False)]=-1.0
    return t

def get_communities(W):
    try:
        G=nx.from_numpy_array(np.abs(W))
        comms=list(nx.community.greedy_modularity_communities(G))
        N=W.shape[0]; lbl=np.zeros(N,dtype=int)
        for ci,c in enumerate(comms):
            for n in c:
                if n<N: lbl[n]=ci
        return lbl,len(comms)
    except:
        N=W.shape[0]; return np.arange(N)%5,5

def make_tau(N,cl,nc,rng):
    centers=np.linspace(np.log(TAU_MIN*1.5),np.log(TAU_MAX*0.7),max(nc,1))
    rng.shuffle(centers)
    tau=np.zeros(N,dtype=np.float32)
    for i in range(N):
        ci=cl[i]%len(centers)
        tau[i]=float(np.clip(np.exp(rng.normal(centers[ci],INTRA_SIGMA)),TAU_MIN,TAU_MAX))
    return tau

def Theta(tau):
    """Murray 2014: τ分布Shannon熵 ✅ 无需修订"""
    h,_=np.histogram(np.log(tau),bins=10)
    h=h[h>0].astype(float); h/=h.sum()
    return float(np.clip(entropy(h)/np.log(10),0,1))

def activate_dynamic_EI(W,h,tau,ei,rng):
    N=W.shape[0]; leak=(1.0-1.0/tau).astype(np.float32)
    drive=np.zeros(N,dtype=np.float32)
    drive[rng.choice(N,max(3,int(N*0.05)),replace=False)]=rng.uniform(0.2,0.5,max(3,int(N*0.05)))
    h_raw=leak*h+np.tanh(W@h+drive); h_raw=np.clip(h_raw,0,1)
    output=h_raw.copy(); output[ei==-1]*=-INH_RATIO
    h_final=leak*h+np.tanh(W@output+drive)
    h_final=np.where(h_final>0.1,h_final,0.0)
    return np.clip(h_final,0,1).astype(np.float32)

# ── 四规则（继承）────────────────────────────────────────
def rule1(W,EL,ltp,ltd,act):
    a=(act>0.30).astype(np.int8); ia=(act<0.08).astype(np.int8)
    lev=np.outer(a,a).astype(np.int16); lev&=(W>0); np.fill_diagonal(lev,0)
    lde=np.outer(ia,a).astype(np.int16); lde&=(W>0)
    ltp+=lev; ltd+=lde
    nel=(ltp>=THETA_LTP)&~EL&(W>0)
    EL|=nel; W[nel]=np.minimum(W[nel]*EL_WT_BOOST,1.0)
    pm=(ltd>=THETA_LTD)&~EL&(W>0); pm&=((W>0).sum(1,keepdims=True)>MIN_EDGES)
    if pm.any(): W[pm]=0; ltp[pm]=0; ltd[pm]=0
    np.fill_diagonal(W,0); return W,EL,ltp,ltd

def rule2(W,EL,ema,rng):
    N=W.shape[0]; n=max(1,int(N*P_GROW*0.01)); ng=0
    for _ in range(n):
        if ng>=int(N*0.15): break
        wi=ema+0.01; wi/=wi.sum(); i=rng.choice(N,p=wi)
        wj=ema.copy()+0.01; wj[i]=0; wj[W[i]>0]=0
        if wj.sum()<1e-8: continue
        wj/=wj.sum(); j=rng.choice(N,p=wj)
        W[i,j]=rng.uniform(W_INIT_LO,W_INIT_HI); ng+=1
    np.fill_diagonal(W,0); return W

def rule3(W,ema):
    up=ema<ACT_LO; dn=ema>ACT_HI
    if up.any(): W[up,:]=np.minimum(W[up,:]*SCALE_UP,1.0)
    if dn.any(): W[dn,:]*=SCALE_DN
    np.fill_diagonal(W,0); return W

def rule4(W,EL,ema,rng):
    N=W.shape[0]; deg=(W>0).sum(1)
    for i in np.where(deg>MIN_EDGES)[0]:
        nb=np.where(W[i]>0)[0]
        if len(nb)<2: continue
        thr=np.median(ema[nb])*COMP_THR
        for j in nb:
            if not EL[i,j] and ema[j]<thr and rng.random()<P_PRUNE and deg[i]>MIN_EDGES:
                W[i,j]=0; deg[i]-=1
    return W

# ══════════════════════════════════════════════════════════
# 修订后的Tc四分量
# ══════════════════════════════════════════════════════════

def compute_lambda_kappa(hist, dt=5):
    """
    修订版λ_eff：κ临界指数
    [Beggs & Plenz 2003; Priesemann 2014]
    
    κ = mean(S_{t+dt}/S_t)，S_t = 窗口t内激活节点数
    λ = exp(-|κ-1|)：κ=1→λ=1.0，偏离越大→λ越小
    适用于任意激活密度
    """
    if len(hist) < dt*3: return 0.5
    mats = np.array(hist); T = len(mats)
    sizes = []
    for t in range(0, T-dt, dt):
        s = float((mats[t:t+dt] > 0.1).sum())
        sizes.append(max(s, 1.0))  # 避免除零
    if len(sizes) < 2: return 0.5
    kappas = [sizes[i+1]/sizes[i] for i in range(len(sizes)-1)]
    kappa = float(np.mean(kappas))
    # λ = exp(-|κ-1|)，κ=1→λ=1（临界），κ→∞或0→λ→0
    lam = float(np.exp(-abs(kappa - 1.0)))
    return float(np.clip(lam, 0, 1))

def compute_phi_FC_heterogeneity(FC_ema, n_sample=50):
    """
    修订版Φ：功能连接异质性（变异系数）
    [Bullmore & Sporns 2009 Nat.Rev.Neurosci.]
    
    CV_FC = std(FC_ij) / (mean(|FC_ij|) + ε)
    Φ = sigmoid(CV_FC)，归一化到(0,1)
    
    物理意义：不同脑区对功能连接强度的异质性
    高异质性 = 功能分化 = 高级信息处理
    在任意激活密度下有效（不需要振荡信号）
    """
    N = FC_ema.shape[0]
    # 取上三角（避免重复）
    mask = np.triu(np.ones((N,N), dtype=bool), k=1)
    fc_vals = FC_ema[mask]
    if len(fc_vals) < 10: return 0.0
    fc_abs = np.abs(fc_vals)
    mean_fc = fc_abs.mean()
    std_fc  = fc_abs.std()
    if mean_fc < 1e-8: return 0.0
    cv = float(std_fc / (mean_fc + 1e-8))
    # sigmoid归一化：CV=0→Φ=0.27，CV=1→Φ=0.73，CV=2→Φ=0.88
    phi = float(1.0 / (1.0 + np.exp(-2.0*cv + 1.0)))
    return float(np.clip(phi, 0, 1))

def compute_psi_weight_change_rate(W, W_prev):
    """
    修订版Ψ：相对权重变化率
    [Bhatt 2009 Nature; Turrigiano 2012 CSHP]
    
    Ψ = ||W(t) - W(t-Δt)||_F / (||W(t)||_F + ε)
    Frobenius范数的相对变化率
    
    物理意义：突触权重的动态可塑性速率
    （不是总变化量，而是单位时间的变化率）
    """
    if W_prev is None: return 0.0
    norm_W    = float(np.linalg.norm(W, 'fro'))
    norm_dW   = float(np.linalg.norm(W - W_prev, 'fro'))
    if norm_W < 1e-8: return 0.0
    rate = norm_dW / (norm_W + 1e-8)
    # tanh归一化：避免超过1
    return float(np.clip(np.tanh(rate * 10), 0, 1))

def compute_Sc_comms(W, rng):
    """Sc四分量 + 返回社区标签（不变）"""
    Wa=np.abs(W); A=(Wa>0).astype(float); N=W.shape[0]; k=A.sum(1); km=k.mean()
    if km<1.5: return 0.0, np.zeros(N,dtype=int), 0
    try:
        G=nx.from_numpy_array(Wa)
        lcc=max(nx.connected_components(G),key=len); C_sc=len(lcc)/N
        cores=nx.core_number(G); k_max=max(cores.values()) if cores else 1
        k_null=np.log(N)/np.log(np.log(N)+1) if N>3 else 2.0
        H_sc=min(k_max/max(k_null*6.667,1.0),1.0)
        comms=list(nx.community.greedy_modularity_communities(G))
        Q=nx.community.modularity(G,comms) if G.number_of_edges()>0 else 0
        M_sc=max((Q-0.02)/(1-0.02),0.01)
        lbl=np.zeros(N,dtype=int)
        for ci,c in enumerate(comms):
            for n in c:
                if n<N: lbl[n]=ci
        n_comms=len(comms)
    except:
        C_sc=0.5; H_sc=0.3; M_sc=0.1
        lbl=np.arange(N)%5; n_comms=5
    Cv=(A@A).diagonal()/np.maximum(k*(k-1),1); Cm=Cv.mean(); Cr=max(km/N,1e-8)
    nodes=rng.choice(N,min(12,N),replace=False); Lv=[]
    for s in nodes:
        dist={s:0}; q=[s]
        while q:
            v=q.pop(0)
            for u in np.where(A[v]>0)[0]:
                if u not in dist: dist[u]=dist[v]+1; q.append(u)
        if len(dist)>1: Lv.append(np.mean(list(dist.values())))
    L=np.mean(Lv) if Lv else float(N); Lr=np.log(N)/np.log(max(km,2))
    sigma=float(np.clip((Cm/Cr)/(L/max(Lr,1e-8)),0,20))
    R_sw=float(np.tanh(max(sigma-1,0)/2))
    comps=[v for v in [C_sc,H_sc,M_sc,R_sw] if v>0]
    Sc=float(np.prod(comps)**(1./len(comps))) if comps else 0.0
    return Sc, lbl, n_comms

def compute_Gst_EMA(FC_ema, W, rng):
    """
    修订版Γst：用EMA慢速FC计算功能社区
    [Honey 2009 PNAS; Bullmore & Sporns 2009]
    """
    from sklearn.metrics import normalized_mutual_info_score
    N = W.shape[0]; Wa = np.abs(W)
    # 结构社区
    try:
        G=nx.from_numpy_array(Wa)
        sc=list(nx.community.greedy_modularity_communities(G))
        Ms=np.zeros(N,dtype=int)
        for ci,c in enumerate(sc):
            for n in c:
                if n<N: Ms[n]=ci
    except: return 0.0
    # 功能社区（从EMA FC）
    fc_abs = np.abs(FC_ema)
    thr = np.percentile(fc_abs[fc_abs>0], 70) if (fc_abs>0).any() else 0.3
    FC_bin = (fc_abs > thr).astype(float)
    np.fill_diagonal(FC_bin, 0)
    try:
        Gf=nx.from_numpy_array(FC_bin)
        fc_comms=list(nx.community.greedy_modularity_communities(Gf))
        MT=np.zeros(N,dtype=int)
        for ci,c in enumerate(fc_comms):
            for n in c:
                if n<N: MT[n]=ci
        return float(np.clip(normalized_mutual_info_score(Ms,MT),-1,1))
    except: return 0.0

def IIL(cst):
    for thr,name in [(4.669,'L6'),(3.1416,'L5 通用'),(2.718,'L4 创造'),
                     (1.618,'L3 适应'),(1.000,'L2 反应'),(0.707,'L1 感知')]:
        if cst>=thr: return name
    return 'L0'

# ── 主仿真 ────────────────────────────────────────────────
def run(name, cfg, seed):
    rng=np.random.RandomState(seed); alpha=ALPHA_MAP.get(name,3.47)
    if cfg['type']=='ce': W,EL,N=load_ce(rng)
    else:
        N=cfg['N']; W=make_ws(N,cfg['k'],cfg['p'],rng)
        EL=np.zeros((N,N),dtype=bool)
    ei=assign_EI(N,rng)
    cl,nc=get_communities(W); tau=make_tau(N,cl,nc,rng)
    TH=Theta(tau)
    print(f"  E/I:{(ei==1).sum()}E+{(ei==-1).sum()}I  nc={nc}  Θ={TH:.3f}")

    ltp=np.zeros((N,N),dtype=np.int16); ltd=ltp.copy()
    ema=np.zeros(N,dtype=np.float32); h=np.zeros(N,dtype=np.float32)
    # EMA功能连接矩阵（初始化为零）
    FC_ema=np.zeros((N,N),dtype=np.float32)
    # 前一周期权重（用于Ψ）
    W_prev=W.copy()
    hist=[]; log=[]; t0=time.time()

    for step in range(N_STEPS):
        h=activate_dynamic_EI(W,h,tau,ei,rng)
        act=h.copy(); ema=0.97*ema+0.03*act
        hist.append(act.copy())
        if len(hist)>HIST_LEN: hist.pop(0)

        # EMA功能连接更新（每步）[Honey 2009]
        FC_ema = FC_EMA_BETA*FC_ema + (1-FC_EMA_BETA)*np.outer(act,act)

        W,EL,ltp,ltd=rule1(W,EL,ltp,ltd,act)
        if step%LTP_DECAY_INT==0: ltp=np.maximum(ltp-1,0)
        if step%GROW_INT==0:    W=rule2(W,EL,ema,rng)
        if step%SCALING_INT==0: W=rule3(W,ema)
        if step%PRUNE_INT==0:   W=rule4(W,EL,ema,rng)

        if step%LOG_INT==0:
            Sc,cl_cur,nc_cur = compute_Sc_comms(W,rng)

            # 修订后的Tc四分量
            lam = compute_lambda_kappa(hist)            # κ临界指数
            phi = compute_phi_FC_heterogeneity(FC_ema) # FC异质性
            psi = compute_psi_weight_change_rate(W, W_prev)  # 相对权重变化率
            W_prev = W.copy()  # 更新前一周期权重

            # Θ（不变）
            tc_v=[v for v in [lam,phi,psi,TH] if v>0.01]
            Tc  = float(np.prod(tc_v)**(1./len(tc_v))) if tc_v else 0.0

            # 修订后的Γst（EMA FC）
            Gst = compute_Gst_EMA(FC_ema, W, rng)

            cst = float(Sc*Tc*np.exp(alpha*max(Gst,0))) if Sc>0 and Tc>0 else 0.0
            elr = EL.sum()/max((W>0).sum(),1)
            act_r=float((act>0.1).mean())
            entry={'step':step,'Sc':round(Sc,4),'Tc':round(Tc,4),
                   'lam':round(lam,4),'Phi':round(phi,4),
                   'Psi':round(psi,4),'Theta':round(TH,4),
                   'Gst':round(Gst,4),'CST':round(cst,4),
                   'IIL':IIL(cst),'EL_r':round(float(elr),4),
                   'act':round(act_r,4)}
            log.append(entry)
            print(f"  {name} s={seed} t={step:5d}: "
                  f"Sc={Sc:.3f} Tc={Tc:.3f}"
                  f"(λκ={lam:.3f} ΦFC={phi:.3f} Ψ={psi:.3f} Θ={TH:.2f}) "
                  f"Γ={Gst:.3f} CST={cst:.3f}[{IIL(cst)}] "
                  f"act={act_r*100:.0f}% ({time.time()-t0:.0f}s)")

    return {'net':name,'seed':seed,'alpha':alpha,'Theta':TH,
            'log':log,'final':log[-1] if log else {}}

# ── 主程序 ────────────────────────────────────────────────
if __name__=='__main__':
    try: from sklearn.metrics import normalized_mutual_info_score
    except:
        import subprocess,sys
        subprocess.run([sys.executable,'-m','pip','install','scikit-learn','-q'])
    print("="*65)
    print("SDI 实验十九 — CST参数第一性审查修订版")
    print("  λ: κ临界指数 exp(-|κ-1|) [Beggs 2003; Priesemann 2014]")
    print("  Φ: FC异质性 CV(FC) [Bullmore & Sporns 2009]")
    print("  Ψ: ||ΔW||/||W|| 相对变化率 [Bhatt 2009; Turrigiano 2012]")
    print("  Γst: EMA慢速FC → 社区NMI [Honey 2009]")
    print("="*65)
    results=[]
    for name,cfg in NETWORKS.items():
        for seed in SEEDS:
            print(f"\n>>> {name}  seed={seed}  α={ALPHA_MAP.get(name,3.47)}")
            results.append(run(name,cfg,seed))
    print("\n"+"="*65)
    by=defaultdict(list)
    for r in results: by[r['net']].append(r)
    summary={}
    print(f"\n{'网络':<15}{'act%':>6}{'λκ':>7}{'ΦFC':>7}{'Ψ':>7}{'Tc':>7}{'Γst':>7}{'CST':>8}{'IIL':>12}")
    print("  "+"-"*72)
    for net,rl in by.items():
        fins=[r['final'] for r in rl if r['final']]
        if not fins: continue
        act=np.mean([f.get('act',0) for f in fins])
        lm =np.mean([f.get('lam',0) for f in fins])
        ph =np.mean([f.get('Phi',0) for f in fins])
        ps =np.mean([f.get('Psi',0) for f in fins])
        th =np.mean([f.get('Theta',0) for f in fins])
        tc =np.mean([f.get('Tc',0)  for f in fins])
        gst=np.mean([f.get('Gst',0) for f in fins])
        cst=np.mean([f.get('CST',0) for f in fins])
        sc =np.mean([f.get('Sc',0)  for f in fins])
        ilv=fins[0].get('IIL','?')
        print(f"  {net:<15}{act*100:>6.0f}{lm:>7.3f}{ph:>7.3f}{ps:>7.3f}"
              f"{tc:>7.3f}{gst:>7.3f}{cst:>8.3f}{ilv:>12}")
        summary[net]={'Sc':float(sc),'Tc':float(tc),'lam':float(lm),
                      'Phi':float(ph),'Psi':float(ps),'Theta':float(th),
                      'Gst':float(gst),'CST':float(cst),'IIL':ilv,'act':float(act)}
    print("\n【与论文Table 2对比】")
    for net,ref in {'C_elegans':0.357,'Human_HCP':3.920}.items():
        if net in summary:
            cst=summary[net]['CST']
            print(f"  {net}: 仿真={cst:.3f}  论文={ref}  比值={cst/ref:.2f}×  [{summary[net]['IIL']}]")
    json.dump({'results':results,'summary':summary},open(OUT,'w'),indent=2)
    print(f"\n✅ {OUT}")
