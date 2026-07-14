"""
SDI 实验十六 — λ和Φ测量方法修正
=====================================
问题：实验十五中λ=Φ=1.0，是因为度量方法不对：
  - 当前λ：逐步激活比（高密度下必然→1.0）
  - 当前Φ：余弦相似度（高密度下必然→1.0）

修正（文献依据）：
  λ_eff：Beggs & Plenz 2003 J.Neurosci.
    → 以时间窗口Δt=5步为单位，统计雪崩尺寸S_t和S_{t+1}
    → λ = mean(S_{t+1}/S_t)，λ=1为临界，>1为超临界，<1为次临界
    → 归一化：score = 1 - |λ-1|/(λ+1)
  
  Φ（相位同步）：Kuramoto 1984
    → 对每个节点的激活序列计算瞬时相位（Hilbert变换）
    → Φ = |mean(exp(i×θ_j))| 跨节点的相位一致性
    → 高密度激活时相位分散→Φ↓，低密度稀疏激活时Φ更真实

其余：继承实验十五（动态E/I平衡）
"""

import numpy as np, json, os, time
import networkx as nx
from collections import defaultdict
from scipy.stats import entropy
from scipy.signal import hilbert

BASE    = '/home/work/.openclaw/workspace/sdi_sim'
OUT     = os.path.join(BASE, 'exp16_lambda_phi_fix_results.json')
CE_DATA = os.path.join(BASE, 'celegans_sim/connectome_v8_data.json')

# ── 继承实验十五全部参数 ──────────────────────────────────
THETA_LTP=60; THETA_LTD=50; LTP_DECAY_INT=500; EL_WT_BOOST=1.5
GROW_INT=50; P_GROW=0.05; W_INIT_LO=0.05; W_INIT_HI=0.10
EI_RATIO=0.20; INH_RATIO=7.0
SCALING_INT=200; ACT_LO=0.03; ACT_HI=0.10
SCALE_UP=1.05; SCALE_DN=0.95
PRUNE_INT=200; P_PRUNE=0.05; MIN_EDGES=2; COMP_THR=0.5
TAU_MU=np.log(20); TAU_SIGMA=1.0; TAU_MIN=5.0; TAU_MAX=200.0
INTRA_SIGMA=0.3

# ── 新增：雪崩窗口参数 ──────────────────────────────────
AVALANCHE_DT = 5   # Beggs 2003: 时间窗口≈1帧间隔（5步≈5ms）

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
# 修正后的 λ_eff 和 Φ 计算
# ══════════════════════════════════════════════════════════

def compute_lambda_beggs(hist, dt=AVALANCHE_DT):
    """
    Beggs & Plenz 2003 雪崩分支比
    以dt步为一帧，统计雪崩传播比λ = <S_{t+1}/S_t>
    λ=1：临界态，λ>1：超临界，λ<1：次临界
    返回归一化值：1 - |λ-1|/(λ+1)，1=临界，0=极端超/次临界
    """
    if len(hist) < dt*2: return 0.0
    mats = np.array(hist)  # T × N
    T = len(mats)
    # 按dt步分帧
    sizes = []
    for t in range(0, T-dt, dt):
        frame = mats[t:t+dt]          # dt步内的激活
        S = (frame > 0.1).sum()        # 帧内总激活数
        sizes.append(float(S))
    if len(sizes) < 2: return 0.0
    ratios = []
    for i in range(len(sizes)-1):
        if sizes[i] > 0:
            ratios.append(sizes[i+1] / sizes[i])
    if not ratios: return 0.0
    lam = float(np.mean(ratios))
    # 归一化：lam=1→score=1.0，lam=2或0→score=0.33
    score = float(np.clip(1.0 - abs(lam-1.0)/(lam+1.0+1e-8), 0, 1))
    return score

def compute_phi_kuramoto(hist, n_sample=40):
    """
    Kuramoto序参数（相位同步）
    对每个节点的激活序列做Hilbert变换获得瞬时相位
    Φ = |<exp(iθ_j)>|_j，跨节点相位一致性
    高密度激活时各节点相位分散→Φ降低（更真实）
    """
    if len(hist) < 10: return 0.0
    mats = np.array(hist)  # T × N
    N = mats.shape[1]
    # 采样节点（效率）
    idx = np.random.choice(N, min(n_sample, N), replace=False)
    phases = []
    for i in idx:
        sig = mats[:, i].astype(float)
        if sig.std() < 1e-6: continue
        try:
            analytic = hilbert(sig)
            phase = np.angle(analytic)  # 瞬时相位
            phases.append(phase)
        except: continue
    if len(phases) < 2: return 0.0
    phases = np.array(phases)  # n_sample × T
    # 每个时间步的Kuramoto序参数
    r_t = np.abs(np.mean(np.exp(1j * phases), axis=0))
    return float(np.clip(np.mean(r_t), 0, 1))

def compute_Psi(W,W0):
    if W0 is None: return 0.0
    w0,wf=W0.flatten(),W.flatten()
    if w0.std()<1e-8 or wf.std()<1e-8: return 0.0
    return float(np.clip((1.0-float(np.corrcoef(w0,wf)[0,1]))/2.0,0,1))

def compute_Sc(W,rng):
    Wa=np.abs(W); A=(Wa>0).astype(float); N=W.shape[0]; k=A.sum(1); km=k.mean()
    if km<1.5: return 0.0
    try:
        G=nx.from_numpy_array(Wa)
        lcc=max(nx.connected_components(G),key=len); C_sc=len(lcc)/N
        cores=nx.core_number(G); k_max=max(cores.values()) if cores else 1
        k_null=np.log(N)/np.log(np.log(N)+1) if N>3 else 2.0
        H_sc=min(k_max/max(k_null*6.667,1.0),1.0)
        comms=list(nx.community.greedy_modularity_communities(G))
        Q=nx.community.modularity(G,comms) if G.number_of_edges()>0 else 0
        M_sc=max((Q-0.02)/(1-0.02),0.01)
    except: C_sc=0.5; H_sc=0.3; M_sc=0.1
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
    return float(np.prod(comps)**(1./len(comps))) if comps else 0.0

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
    cl,nc=get_communities(W); tau=make_tau(N,cl,nc,rng)
    TH=Theta(tau)
    print(f"  E/I:{(ei==1).sum()}E+{(ei==-1).sum()}I  Θ={TH:.3f}")
    ltp=np.zeros((N,N),dtype=np.int16); ltd=ltp.copy()
    ema=np.zeros(N,dtype=np.float32); h=np.zeros(N,dtype=np.float32)
    hist=[]; log=[]; t0=time.time()

    for step in range(N_STEPS):
        h=activate_dynamic_EI(W,h,tau,ei,rng)
        act=h.copy(); ema=0.97*ema+0.03*act
        hist.append(act.copy())
        if len(hist)>50: hist.pop(0)
        W,EL,ltp,ltd=rule1(W,EL,ltp,ltd,act)
        if step%LTP_DECAY_INT==0: ltp=np.maximum(ltp-1,0)
        if step%GROW_INT==0:    W=rule2(W,EL,ema,rng)
        if step%SCALING_INT==0: W=rule3(W,ema)
        if step%PRUNE_INT==0:   W=rule4(W,EL,ema,rng)

        if step%LOG_INT==0:
            Sc  = compute_Sc(W, rng)
            lam = compute_lambda_beggs(hist)   # 修正版λ
            phi = compute_phi_kuramoto(hist)   # 修正版Φ
            psi = compute_Psi(W, W0)
            tc_v= [v for v in [lam,phi,psi,TH] if v>0]
            Tc  = float(np.prod(tc_v)**(1./len(tc_v))) if tc_v else 0.0
            Gst = compute_Gst(W, hist)
            cst = float(Sc*Tc*np.exp(alpha*max(Gst,0))) if Sc>0 and Tc>0 else 0.0
            elr = EL.sum()/max((W>0).sum(),1)
            act_r = float((act>0.1).mean())
            entry={'step':step,'Sc':round(Sc,4),'Tc':round(Tc,4),
                   'lam':round(lam,4),'Phi':round(phi,4),
                   'Psi':round(psi,4),'Theta':round(TH,4),
                   'Gst':round(Gst,4),'CST':round(cst,4),
                   'IIL':IIL(cst),'EL_r':round(float(elr),4),
                   'act':round(act_r,4)}
            log.append(entry)
            print(f"  {name} s={seed} t={step:5d}: "
                  f"Sc={Sc:.3f} Tc={Tc:.3f}"
                  f"(λ={lam:.3f} Φ={phi:.3f} Ψ={psi:.2f} Θ={TH:.2f}) "
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
    print("SDI 实验十六 — λ和Φ测量方法修正")
    print("  λ: Beggs & Plenz 2003 雪崩分支比（帧窗口Δt=5步）")
    print("  Φ: Kuramoto 1984 相位序参数（Hilbert变换）")
    print("  激活：动态E/I平衡（继承实验十五）")
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
    print(f"\n{'网络':<15}{'act%':>6}{'λ':>7}{'Φ':>7}{'Ψ':>7}{'Tc':>7}{'Γst':>7}{'CST':>8}{'IIL':>12}")
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
                      'Gst':float(gst),'CST':float(cst),'IIL':ilv,
                      'act':float(act)}
    print("\n【与论文Table 2对比】")
    for net,ref in {'C_elegans':0.357,'Human_HCP':3.920}.items():
        if net in summary:
            cst=summary[net]['CST']
            print(f"  {net}: 仿真={cst:.3f}  论文={ref}  "
                  f"比值={cst/ref:.2f}×  [{summary[net]['IIL']}]")
    print("\n【vs 实验十五 CST对比】")
    e15={'WS_300':1.681,'C_elegans':0.942,'Human_HCP':1.599}
    for net,s in summary.items():
        delta=s['CST']-e15.get(net,0)
        print(f"  {net}: {e15.get(net,0):.3f}→{s['CST']:.3f}  Δ={delta:+.3f}  [{s['IIL']}]")
    json.dump({'results':results,'summary':summary},open(OUT,'w'),indent=2)
    print(f"\n✅ {OUT}")
