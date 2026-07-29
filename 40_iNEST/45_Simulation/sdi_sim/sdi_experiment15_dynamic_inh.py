"""
SDI 实验十五 — 动态反馈抑制（解决λΦ=1.0根本原因）
====================================================
实验十四证明：静态权重×-13无法压制激活率
根本原因：生物抑制是动态的（激活越强→抑制越强）

修复：两阶段激活
  阶段1：所有节点正常LIF积分（兴奋性输入）
  阶段2：抑制性节点输出 = -INH_RATIO × h_inh（动态比例）
         兴奋性节点输出 = h_exc（正常）
  最终激活 = tanh(Σ W_ij × output_j)
  → 激活越强→抑制越强→自然收敛到平衡态

文献：
  Vreeswijk & Sompolinsky 1996 Science：
    平衡态下 I_inh ∝ I_exc（抑制追踪兴奋）
  Brunel 2000：
    快速抑制（GABA_A τ~5ms）vs慢速兴奋（AMPA τ~2ms）
"""

import numpy as np, json, os, time
import networkx as nx
from collections import defaultdict
from scipy.stats import entropy

BASE    = '/vault/sdi_sim'
OUT     = os.path.join(BASE, 'exp15_dynamic_inh_results.json')
CE_DATA = os.path.join(BASE, 'celegans_sim/connectome_v8_data.json')

# ── 继承实验十三所有参数，只改激活机制 ────────────────────
THETA_LTP=60; THETA_LTD=50; LTP_DECAY_INT=500; EL_WT_BOOST=1.5
GROW_INT=50; P_GROW=0.05; W_INIT_LO=0.05; W_INIT_HI=0.10
EI_RATIO=0.20
INH_RATIO=7.0          # 动态抑制下不需要很大，恢复7.0
SCALING_INT=200; ACT_LO=0.03; ACT_HI=0.10
SCALE_UP=1.05; SCALE_DN=0.95
PRUNE_INT=200; P_PRUNE=0.05; MIN_EDGES=2; COMP_THR=0.5
TAU_MU=np.log(20); TAU_SIGMA=1.0; TAU_MIN=5.0; TAU_MAX=200.0
INTRA_SIGMA=0.3

N_STEPS=10000; LOG_INT=1000; SEEDS=[42,7,13]
ALPHA_MAP={'WS_300':3.47,'C_elegans':2.56,'Human_HCP':3.91}
NETWORKS={
    'WS_300':   {'type':'ws','N':300,'k':12,'p':0.1},
    'C_elegans':{'type':'ce'},
    'Human_HCP':{'type':'ws','N':80,'k':8,'p':0.1},
}

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

# ── 核心改进：动态反馈抑制激活 ───────────────────────────
def activate_dynamic_EI(W, h, tau, ei_types, rng):
    """
    两阶段动态反馈抑制（Vreeswijk 1996真实机制）
    
    阶段1：所有节点LIF积分（兴奋性输入）
      h_raw_i = leak_i × h_i + tanh(Σ_j W_ij × h_j + drive_i)
    
    阶段2：计算输出（兴奋/抑制区分）
      output_i = h_raw_i              （兴奋性节点）
      output_i = -INH_RATIO × h_raw_i （抑制性节点，动态！）
    
    阶段3：用output重新计算净输入，再激活一次
      net_input_i = Σ_j W_ij × output_j
      h_final_i   = leak_i × h_i + tanh(net_input_i + drive_i)
    
    → 激活越强→抑制越强→自然收敛到平衡态
    """
    N = W.shape[0]
    leak = (1.0 - 1.0/tau).astype(np.float32)

    # 少量外部驱动
    n_in = max(3, int(N*0.05))
    drive = np.zeros(N, dtype=np.float32)
    drive[rng.choice(N, n_in, replace=False)] = rng.uniform(0.2,0.5,n_in)

    # 阶段1：原始LIF积分
    h_raw = leak * h + np.tanh(W @ h + drive)
    h_raw = np.clip(h_raw, 0, 1)

    # 阶段2：动态输出（抑制性节点输出为负，且与激活强度成比例）
    output = h_raw.copy()
    inh_mask = (ei_types == -1)
    output[inh_mask] = -INH_RATIO * h_raw[inh_mask]  # 动态抑制！

    # 阶段3：用动态输出重算净输入
    net2 = W @ output + drive
    h_final = leak * h + np.tanh(net2)
    h_final = np.where(h_final > 0.1, h_final, 0.0)
    h_final = np.clip(h_final, 0, 1)

    return h_final.astype(np.float32)

# ── 四规则（完全继承实验十三）────────────────────────────
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

# ── 指标 ─────────────────────────────────────────────────
def lam_eff(hist):
    if len(hist)<2: return 0.0
    rs=[]
    for t in range(len(hist)-1):
        n0=(hist[t]>0.1).sum(); n1=(hist[t+1]>0.1).sum()
        if n0>0: rs.append(n1/n0)
    if not rs: return 0.0
    lam=float(np.mean(rs))
    return float(np.clip(1.0-abs(lam-1.0)/(lam+1.0+1e-8),0,1))

def phi_eff(hist):
    if len(hist)<4: return 0.0
    mats=np.array(hist); cs=[]
    for t in range(len(mats)-1):
        a,b=mats[t],mats[t+1]; na,nb=np.linalg.norm(a),np.linalg.norm(b)
        if na>1e-8 and nb>1e-8: cs.append(float(np.dot(a,b)/(na*nb)))
    return float(np.clip(np.mean(cs) if cs else 0.0,0,1))

def psi_eff(W,W0):
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

def run(name,cfg,seed):
    rng=np.random.RandomState(seed); alpha=ALPHA_MAP.get(name,3.47)
    if cfg['type']=='ce': W,EL,N=load_ce(rng)
    else:
        N=cfg['N']; W=make_ws(N,cfg['k'],cfg['p'],rng)
        EL=np.zeros((N,N),dtype=bool)
    W0=W.copy(); ei=assign_EI(N,rng)
    cl,nc=get_communities(W); tau=make_tau(N,cl,nc,rng)
    TH=Theta(tau); n_inh=(ei==-1).sum()
    print(f"  E/I:{N-n_inh}E+{n_inh}I  动态INH={INH_RATIO}×  Θ={TH:.3f}")
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
            Sc=compute_Sc(W,rng)
            lm=lam_eff(hist); ph=phi_eff(hist); ps=psi_eff(W,W0)
            tc_v=[v for v in [lm,ph,ps,TH] if v>0]
            Tc=float(np.prod(tc_v)**(1./len(tc_v))) if tc_v else 0.0
            Gst=compute_Gst(W,hist)
            cst=float(Sc*Tc*np.exp(alpha*max(Gst,0))) if Sc>0 and Tc>0 else 0.0
            elr=EL.sum()/max((W>0).sum(),1)
            act_r=float((act>0.1).mean())
            entry={'step':step,'Sc':round(Sc,4),'Tc':round(Tc,4),
                   'lam':round(lm,4),'Phi':round(ph,4),
                   'Psi':round(ps,4),'Theta':round(TH,4),
                   'Gst':round(Gst,4),'CST':round(cst,4),
                   'IIL':IIL(cst),'EL_r':round(float(elr),4),
                   'act':round(act_r,4)}
            log.append(entry)
            print(f"  {name} s={seed} t={step:5d}: "
                  f"Sc={Sc:.3f} Tc={Tc:.3f}"
                  f"(λ={lm:.2f} Φ={ph:.2f} Ψ={ps:.2f} Θ={TH:.2f}) "
                  f"Γ={Gst:.3f} CST={cst:.3f}[{IIL(cst)}] "
                  f"act={act_r*100:.0f}% ({time.time()-t0:.0f}s)")
    return {'net':name,'seed':seed,'alpha':alpha,'Theta':TH,
            'log':log,'final':log[-1] if log else {}}

if __name__=='__main__':
    try: from sklearn.metrics import normalized_mutual_info_score
    except:
        import subprocess,sys
        subprocess.run([sys.executable,'-m','pip','install','scikit-learn','-q'])
    print("="*65)
    print("SDI 实验十五 — 动态反馈抑制（解决λΦ=1.0根本原因）")
    print("  两阶段：原始LIF积分 → 动态输出(-INH×h_inh) → 重算净输入")
    print(f"  Vreeswijk 1996: I_inh ∝ I_exc（抑制追踪兴奋）")
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
    print(f"\n{'网络':<15}{'act%':>6}{'λ':>6}{'Φ':>6}{'Ψ':>7}{'Tc':>7}{'Γst':>7}{'CST':>8}{'IIL':>12}")
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
        print(f"  {net:<15}{act*100:>6.0f}{lm:>6.3f}{ph:>6.3f}{ps:>7.3f}"
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
                  f"比值={cst/ref:.2f}×  act={summary[net]['act']*100:.0f}%  "
                  f"[{summary[net]['IIL']}]")
    print("\n【vs 实验十三对比】")
    e13={'WS_300':1.518,'C_elegans':1.089,'Human_HCP':2.299}
    e13a={'WS_300':0.87,'C_elegans':0.82,'Human_HCP':0.87}
    for net,s in summary.items():
        print(f"  {net}: act {e13a.get(net,0)*100:.0f}%→{s['act']*100:.0f}%  "
              f"CST {e13.get(net,0):.3f}→{s['CST']:.3f}  [{s['IIL']}]")
    json.dump({'results':results,'summary':summary},open(OUT,'w'),indent=2)
    print(f"\n✅ {OUT}")
