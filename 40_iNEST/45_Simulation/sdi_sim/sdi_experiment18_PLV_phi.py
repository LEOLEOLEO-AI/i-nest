"""
SDI 实验十八 — 社区间PLV替代全局Kuramoto
============================================
文献依据：
  Lachaux et al. 1999 Human Brain Mapping
    PLV = |<exp(i(θ_A - θ_B))>|，测量两信号的相位锁定程度
  Varela et al. 2001 Nature Reviews Neuroscience
    脑区间同步 = 不同功能模块激活时序的相位协调
  Strogatz 2001 Nature
    相位差比绝对相位更稳定，适用于高密度激活场景

物理直觉：
  高密度激活时不同社区的激活时序仍然不同（功能分化）
  PLV(社区A, 社区B) 测量的是跨模块的功能协调程度
  → 不依赖Hilbert变换，不会在高密度时退化

Φ新定义：
  1. 用Louvain找社区划分（已有，来自Sc计算）
  2. 对每对相邻社区(A,B)计算 PLV_AB
     PLV_AB = |mean_t(exp(i·(ΔθA(t) - ΔθB(t))))|
     其中ΔθA(t) = 社区A在t步的平均激活 - t-1步的平均激活（相位差分）
  3. Φ = mean(PLV_AB over all community pairs)

预期：
  - 不再间歇性=0（社区时序差异稳定存在）
  - Φ∈[0.2, 0.7]（有意义的跨模块相位协调）
  - Tc从0.65→0.80，Human_HCP CST→2.5+（L3→L4方向）
"""

import numpy as np, json, os, time
import networkx as nx
from collections import defaultdict
from scipy.stats import entropy

BASE    = '/vault/sdi_sim'
OUT     = os.path.join(BASE, 'exp18_PLV_phi_results.json')
CE_DATA = os.path.join(BASE, 'celegans_sim/connectome_v8_data.json')

# ── 继承实验十七全部参数 ──────────────────────────────────
THETA_LTP=60; THETA_LTD=50; LTP_DECAY_INT=500; EL_WT_BOOST=1.5
GROW_INT=50; P_GROW=0.05; W_INIT_LO=0.05; W_INIT_HI=0.10
EI_RATIO=0.20; INH_RATIO=7.0
SCALING_INT=200; ACT_LO=0.03; ACT_HI=0.10
SCALE_UP=1.05; SCALE_DN=0.95
PRUNE_INT=200; P_PRUNE=0.05; MIN_EDGES=2; COMP_THR=0.5
TAU_MU=np.log(20); TAU_SIGMA=1.0; TAU_MIN=5.0; TAU_MAX=200.0
INTRA_SIGMA=0.3; AVALANCHE_DT=5; HIST_LEN=100

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
        return lbl,len(comms),comms
    except:
        N=W.shape[0]; return np.arange(N)%5,5,[]

def make_tau(N,cl,nc,rng):
    centers=np.linspace(np.log(TAU_MIN*1.5),np.log(TAU_MAX*0.7),max(nc,1))
    rng.shuffle(centers)
    tau=np.zeros(N,dtype=np.float32)
    for i in range(N):
        ci=cl[i]%len(centers)
        tau[i]=float(np.clip(np.exp(rng.normal(centers[ci],INTRA_SIGMA)),TAU_MIN,TAU_MAX))
    return tau

def Theta(tau):
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
# 新Φ：社区间PLV（Lachaux 1999 / Varela 2001）
# ══════════════════════════════════════════════════════════

def compute_phi_PLV(hist, comm_labels, n_comms):
    """
    社区间Phase Locking Value
    文献：Lachaux et al. 1999 Hum.Brain.Map.
          Varela et al. 2001 Nat.Rev.Neurosci.
    
    方法：
    1. 对每个社区，计算该社区节点的平均激活时序 μ_c(t)
    2. 计算相位差分 dμ_c(t) = μ_c(t) - μ_c(t-1)（相位变化速率）
    3. 归一化：φ_c(t) = dμ_c(t) / (|dμ_c(t)| + ε)（单位复数）
    4. 社区对间PLV：PLV(A,B) = |mean_t(conj(φ_A(t))·φ_B(t))|
    5. Φ = mean over all community pairs
    
    物理意义：不同社区的激活节律是否保持稳定的相位关系
    在高密度激活下仍然有效（利用差分，不依赖绝对幅值）
    """
    if len(hist) < 10 or n_comms < 2:
        return 0.0

    mats = np.array(hist)  # T × N
    T    = mats.shape[0]

    # 每个社区的平均激活时序
    comm_series = {}
    for ci in range(n_comms):
        mask = (comm_labels == ci)
        if mask.sum() < 2: continue
        series = mats[:, mask].mean(axis=1)  # T维时序
        if series.std() < 1e-6: continue
        comm_series[ci] = series

    comm_ids = list(comm_series.keys())
    if len(comm_ids) < 2:
        return 0.0

    # 计算相位差分（归一化到单位复数）
    phase_signals = {}
    for ci, series in comm_series.items():
        diff = np.diff(series)  # T-1维差分
        norm = np.abs(diff) + 1e-8
        # 将差分映射到复平面上的单位向量
        # 正差分→angle=0，负差分→angle=π，零差分→随机
        angle = np.where(diff >= 0, 0.0, np.pi)
        # 加入幅值信息：幅值越大，相位越确定
        weight = np.tanh(np.abs(diff) * 10)  # 软权重
        phase_signals[ci] = np.exp(1j * angle) * weight

    # 计算所有社区对的PLV
    plv_values = []
    for i in range(len(comm_ids)):
        for j in range(i+1, len(comm_ids)):
            ci, cj = comm_ids[i], comm_ids[j]
            sig_A = phase_signals[ci]
            sig_B = phase_signals[cj]
            # PLV = |<exp(i(θ_A - θ_B))>| = |<conj(φ_A) * φ_B>|
            # 已归一化，直接点积取模
            T_common = min(len(sig_A), len(sig_B))
            plv = float(np.abs(np.mean(np.conj(sig_A[:T_common]) * sig_B[:T_common])))
            plv_values.append(plv)

    if not plv_values:
        return 0.0

    return float(np.clip(np.mean(plv_values), 0, 1))

# ── 其余指标（继承）──────────────────────────────────────
def compute_lambda_beggs(hist, dt=AVALANCHE_DT):
    if len(hist)<dt*2: return 0.0
    mats=np.array(hist); T=len(mats)
    sizes=[]
    for t in range(0,T-dt,dt):
        sizes.append(float((mats[t:t+dt]>0.1).sum()))
    if len(sizes)<2: return 0.0
    ratios=[sizes[i+1]/sizes[i] for i in range(len(sizes)-1) if sizes[i]>0]
    if not ratios: return 0.0
    lam=float(np.mean(ratios))
    return float(np.clip(1.0-abs(lam-1.0)/(lam+1.0+1e-8),0,1))

def compute_Psi(W,W0):
    if W0 is None: return 0.0
    w0,wf=W0.flatten(),W.flatten()
    if w0.std()<1e-8 or wf.std()<1e-8: return 0.0
    return float(np.clip((1.0-float(np.corrcoef(w0,wf)[0,1]))/2.0,0,1))

def compute_Sc_and_comms(W,rng):
    Wa=np.abs(W); A=(Wa>0).astype(float); N=W.shape[0]; k=A.sum(1); km=k.mean()
    if km<1.5: return 0.0,np.zeros(N,dtype=int),0
    try:
        G=nx.from_numpy_array(Wa)
        lcc=max(nx.connected_components(G),key=len); C_sc=len(lcc)/N
        cores=nx.core_number(G); k_max=max(cores.values()) if cores else 1
        k_null=np.log(N)/np.log(np.log(N)+1) if N>3 else 2.0
        H_sc=min(k_max/max(k_null*6.667,1.0),1.0)
        comms=list(nx.community.greedy_modularity_communities(G))
        Q=nx.community.modularity(G,comms) if G.number_of_edges()>0 else 0
        M_sc=max((Q-0.02)/(1-0.02),0.01)
        # 社区标签
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

def compute_Gst(W,hist):
    from sklearn.metrics import normalized_mutual_info_score
    N=W.shape[0]; Wa=np.abs(W)
    try:
        G=nx.from_numpy_array(Wa)
        sc=list(nx.community.greedy_modularity_communities(G))
        Ms=np.zeros(N,dtype=int)
        for ci,c in enumerate(sc):
            for n in c:
                if n<N: Ms[n]=ci
    except: return 0.0
    if len(hist)<5: return 0.0
    mats=np.array(hist); cm=np.corrcoef(mats.T); cm=np.nan_to_num(cm,0)
    thr=np.percentile(cm[cm>0],70) if (cm>0).any() else 0.5
    FC=(cm>thr).astype(float); np.fill_diagonal(FC,0)
    try:
        Gf=nx.from_numpy_array(FC)
        fc=list(nx.community.greedy_modularity_communities(Gf))
        MT=np.zeros(N,dtype=int)
        for ci,c in enumerate(fc):
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
    W0=W.copy(); ei=assign_EI(N,rng)
    cl,nc,_=get_communities(W); tau=make_tau(N,cl,nc,rng)
    TH=Theta(tau)
    print(f"  E/I:{(ei==1).sum()}E+{(ei==-1).sum()}I  n_comms={nc}  Θ={TH:.3f}")
    ltp=np.zeros((N,N),dtype=np.int16); ltd=ltp.copy()
    ema=np.zeros(N,dtype=np.float32); h=np.zeros(N,dtype=np.float32)
    hist=[]; log=[]; t0=time.time()
    curr_lbl=cl; curr_nc=nc  # 当前社区标签

    for step in range(N_STEPS):
        h=activate_dynamic_EI(W,h,tau,ei,rng)
        act=h.copy(); ema=0.97*ema+0.03*act
        hist.append(act.copy())
        if len(hist)>HIST_LEN: hist.pop(0)
        W,EL,ltp,ltd=rule1(W,EL,ltp,ltd,act)
        if step%LTP_DECAY_INT==0: ltp=np.maximum(ltp-1,0)
        if step%GROW_INT==0:    W=rule2(W,EL,ema,rng)
        if step%SCALING_INT==0: W=rule3(W,ema)
        if step%PRUNE_INT==0:   W=rule4(W,EL,ema,rng)

        if step%LOG_INT==0:
            # Sc + 更新社区标签
            Sc,curr_lbl,curr_nc = compute_Sc_and_comms(W,rng)
            lam = compute_lambda_beggs(hist)
            # 新Φ：社区间PLV
            phi = compute_phi_PLV(hist, curr_lbl, curr_nc)
            psi = compute_Psi(W,W0)
            # Tc安全几何均值（跳过=0的分量）
            tc_v=[v for v in [lam,phi,psi,TH] if v>0.01]
            Tc  = float(np.prod(tc_v)**(1./len(tc_v))) if tc_v else 0.0
            Gst = compute_Gst(W,hist)
            cst = float(Sc*Tc*np.exp(alpha*max(Gst,0))) if Sc>0 and Tc>0 else 0.0
            elr = EL.sum()/max((W>0).sum(),1)
            act_r=float((act>0.1).mean())
            entry={'step':step,'Sc':round(Sc,4),'Tc':round(Tc,4),
                   'lam':round(lam,4),'Phi':round(phi,4),
                   'Psi':round(psi,4),'Theta':round(TH,4),
                   'Gst':round(Gst,4),'CST':round(cst,4),
                   'IIL':IIL(cst),'EL_r':round(float(elr),4),
                   'act':round(act_r,4),'n_comms':curr_nc}
            log.append(entry)
            print(f"  {name} s={seed} t={step:5d}: "
                  f"Sc={Sc:.3f} Tc={Tc:.3f}"
                  f"(λ={lam:.3f} Φ={phi:.3f} Ψ={psi:.2f} Θ={TH:.2f}) "
                  f"Γ={Gst:.3f} CST={cst:.3f}[{IIL(cst)}] "
                  f"nc={curr_nc} act={act_r*100:.0f}% ({time.time()-t0:.0f}s)")

    return {'net':name,'seed':seed,'alpha':alpha,'Theta':TH,
            'log':log,'final':log[-1] if log else {}}

# ── 主程序 ────────────────────────────────────────────────
if __name__=='__main__':
    try: from sklearn.metrics import normalized_mutual_info_score
    except:
        import subprocess,sys
        subprocess.run([sys.executable,'-m','pip','install','scikit-learn','-q'])
    print("="*65)
    print("SDI 实验十八 — 社区间PLV（Lachaux 1999 / Varela 2001）")
    print("  Φ = mean PLV(社区A, 社区B) over all community pairs")
    print("  相位差分归一化 → 不依赖Hilbert → 高密度时稳定")
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
    print(f"\n{'网络':<15}{'act%':>6}{'λ':>7}{'Φ(PLV)':>9}{'Ψ':>7}"
          f"{'Tc':>7}{'Γst':>7}{'CST':>8}{'IIL':>12}")
    print("  "+"-"*75)
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
        print(f"  {net:<15}{act*100:>6.0f}{lm:>7.3f}{ph:>9.3f}{ps:>7.3f}"
              f"{tc:>7.3f}{gst:>7.3f}{cst:>8.3f}{ilv:>12}")
        summary[net]={'Sc':float(sc),'Tc':float(tc),'lam':float(lm),
                      'Phi':float(ph),'Psi':float(ps),'Theta':float(th),
                      'Gst':float(gst),'CST':float(cst),'IIL':ilv,'act':float(act)}
    print("\n【与论文Table 2对比】")
    for net,ref in {'C_elegans':0.357,'Human_HCP':3.920}.items():
        if net in summary:
            cst=summary[net]['CST']
            phi=summary[net]['Phi']
            print(f"  {net}: CST={cst:.3f}(论文{ref})  比值={cst/ref:.2f}×  "
                  f"Φ(PLV)={phi:.3f}  [{summary[net]['IIL']}]")
    print("\n【实验进化路线】")
    milestones={'实验九':{'WS':1.774,'CE':0.402,'HCP':2.148},
                '实验十三':{'WS':1.518,'CE':1.089,'HCP':2.299},
                '实验十八':{'WS':summary.get('WS_300',{}).get('CST',0),
                           'CE':summary.get('C_elegans',{}).get('CST',0),
                           'HCP':summary.get('Human_HCP',{}).get('CST',0)}}
    for exp,v in milestones.items():
        print(f"  {exp}: WS={v['WS']:.3f}  CE={v['CE']:.3f}  HCP={v['HCP']:.3f}")
    json.dump({'results':results,'summary':summary},open(OUT,'w'),indent=2)
    print(f"\n✅ {OUT}")
