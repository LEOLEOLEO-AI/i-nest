"""
SDI 实验十二 — E/I平衡 + 抑制性神经元
========================================
修复实验十一的 λΦ=1.0 过饱和问题

文献依据：
  Vreeswijk & Sompolinsky 1996 Science 274:1724
    E/I平衡态：80%兴奋性 + 20%抑制性神经元
    → 稀疏激活，λ自然降到0.90-0.95
  Brunel 2000 J.Comput.Neurosci. 8:183
    皮层1-5Hz稀疏激活来自E/I平衡
    抑制性神经元权重约为兴奋性的4倍（强抑制）
  Renart et al. 2010 Science 327:587
    皮层E/I平衡的实验证据，抑制性电流追踪兴奋性电流

改进：
  - 20%节点为抑制性（I型），权重为负
  - 兴奋性/抑制性权重比 = 1 : -4（Brunel 2000）
  - → λ从1.0→0.90-0.95，Φ从1.0→0.6-0.8
  - → Ψ从0.07→0.2+，Tc从0.5→0.7+
  - → Human_HCP CST 预期 >3.14（L5通用智能）
"""

import numpy as np, json, os, time
import networkx as nx
from collections import defaultdict
from scipy.stats import entropy

BASE    = '/home/work/.openclaw/workspace/sdi_sim'
OUT     = os.path.join(BASE, 'exp12_EI_balance_results.json')
CE_DATA = os.path.join(BASE, 'celegans_sim/connectome_v8_data.json')

# ── v5文献锁定参数（不变）────────────────────────────────
THETA_LTP=60; THETA_LTD=50; LTP_DECAY_INT=500; EL_WT_BOOST=1.5
GROW_INT=50;  P_GROW=0.05; W_INIT_LO=0.05; W_INIT_HI=0.10
SCALING_INT=200; ACT_LO=0.03; ACT_HI=0.10
SCALE_UP=1.05; SCALE_DN=0.95
PRUNE_INT=200; P_PRUNE=0.05; MIN_EDGES=2; COMP_THR=0.5

# ── 异质LIF参数（继承实验十一）──────────────────────────
TAU_MU=np.log(20); TAU_SIGMA=1.0; TAU_MIN=5.0; TAU_MAX=200.0
INTRA_COMM_SIGMA=0.3
SPARSE_K=0.12

# ── E/I平衡参数（新增，文献依据）────────────────────────
EI_RATIO   = 0.20   # 抑制性神经元比例 [Vreeswijk 1996: ~20%]
INH_WEIGHT = -4.0   # 抑制性权重倍数（负值）[Brunel 2000: 约4倍]

N_STEPS = 10000
LOG_INT  = 1000
SEEDS    = [42, 7, 13]

ALPHA_MAP = {'WS_300':3.47, 'C_elegans':2.56, 'Human_HCP':3.91}
NETWORKS  = {
    'WS_300':    {'type':'ws','N':300,'k':12,'p':0.1},
    'C_elegans': {'type':'ce'},
    'Human_HCP': {'type':'ws','N':80, 'k':8, 'p':0.1},
}

# ── 初始化 ────────────────────────────────────────────────
def make_ws(N,k,p,rng):
    W=np.zeros((N,N),dtype=np.float32)
    for i in range(N):
        for d in range(1,k//2+1):
            j=(i+d)%N; W[i,j]=W[j,i]=rng.uniform(0.1,0.35)
    for i in range(N):
        for d in range(1,k//2+1):
            if rng.random()<p:
                j=(i+d)%N; nj=rng.randint(0,N)
                if nj!=i and W[i,nj]==0:
                    W[i,nj]=W[i,j]; W[i,j]=0
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

def assign_EI(N, rng):
    """
    分配兴奋/抑制神经元类型
    Vreeswijk 1996: 80%兴奋(+1) / 20%抑制(-1)
    """
    types = np.ones(N, dtype=np.float32)
    n_inh = int(N * EI_RATIO)
    inh_idx = rng.choice(N, n_inh, replace=False)
    types[inh_idx] = -1.0
    return types  # +1=兴奋, -1=抑制

def apply_EI_weights(W, ei_types):
    """
    抑制性神经元的输出权重乘以INH_WEIGHT（负值）
    Brunel 2000: 抑制性连接强度约为兴奋性的4倍
    """
    W_ei = W.copy()
    inh_mask = (ei_types == -1)
    W_ei[inh_mask, :] *= INH_WEIGHT  # 抑制性神经元输出变负
    return W_ei

def get_communities(W):
    try:
        G=nx.from_numpy_array(np.abs(W))
        comms=list(nx.community.greedy_modularity_communities(G))
        N=W.shape[0]; labels=np.zeros(N,dtype=int)
        for ci,c in enumerate(comms):
            for n in c:
                if n<N: labels[n]=ci
        return labels, len(comms)
    except:
        N=W.shape[0]; return np.arange(N)%5, 5

def make_tau_structured(N, comm_labels, n_comms, rng):
    comm_centers=np.linspace(np.log(TAU_MIN*1.5),np.log(TAU_MAX*0.7),max(n_comms,1))
    rng.shuffle(comm_centers)
    tau=np.zeros(N,dtype=np.float32)
    for i in range(N):
        ci=comm_labels[i]%len(comm_centers)
        tau[i]=float(np.clip(np.exp(rng.normal(comm_centers[ci],INTRA_COMM_SIGMA)),TAU_MIN,TAU_MAX))
    return tau

def compute_Theta(tau):
    log_tau=np.log(tau); hist,_=np.histogram(log_tau,bins=10)
    hist=hist[hist>0].astype(float); hist/=hist.sum()
    return float(np.clip(entropy(hist)/np.log(10),0,1))

# ── E/I平衡激活（核心改进）───────────────────────────────
def activate_EI(W, W_ei, h, tau, rng):
    """
    E/I平衡异质LIF激活
    Vreeswijk 1996: 抑制性电流追踪兴奋性电流
    → 净输入接近0（平衡态），激活稀疏
    → λ自然降到0.90-0.95
    """
    N = W.shape[0]
    leak = (1.0 - 1.0/tau).astype(np.float32)

    # 外部驱动（少量感觉输入）
    n_in = max(3, int(N*0.05))
    drive = np.zeros(N, dtype=np.float32)
    drive[rng.choice(N, n_in, replace=False)] = rng.uniform(0.2, 0.6, n_in)

    # E/I平衡更新：使用含抑制权重的W_ei
    # 兴奋性输入 - 抑制性输入 → 平衡态接近0
    net_input = W_ei @ h + drive
    h_new = leak * h + np.tanh(net_input)

    # 软阈值稀疏化（比top-K更生物合理）
    # 只保留超过静息阈值的节点
    h_new = np.where(h_new > 0.1, h_new, 0.0)
    h_new = np.clip(h_new, 0, 1)
    return h_new.astype(np.float32)

# ── v5四规则 ─────────────────────────────────────────────
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
def compute_lambda(act_hist):
    if len(act_hist)<2: return 0.0
    rs=[]
    for t in range(len(act_hist)-1):
        n0=(act_hist[t]>0.1).sum(); n1=(act_hist[t+1]>0.1).sum()
        if n0>0: rs.append(n1/n0)
    if not rs: return 0.0
    lam=float(np.mean(rs))
    return float(np.clip(1.0-abs(lam-1.0)/(lam+1.0+1e-8),0,1))

def compute_Phi(act_hist):
    if len(act_hist)<4: return 0.0
    mats=np.array(act_hist); cs=[]
    for t in range(len(mats)-1):
        a,b=mats[t],mats[t+1]; na,nb=np.linalg.norm(a),np.linalg.norm(b)
        if na>1e-8 and nb>1e-8: cs.append(float(np.dot(a,b)/(na*nb)))
    return float(np.clip(np.mean(cs) if cs else 0.0,0,1))

def compute_Psi(W,W0):
    if W0 is None: return 0.0
    w0,wf=W0.flatten(),W.flatten()
    if w0.std()<1e-8 or wf.std()<1e-8: return 0.0
    return float(np.clip((1.0-float(np.corrcoef(w0,wf)[0,1]))/2.0,0,1))

def compute_Sc(W,rng):
    Wa=np.abs(W); A=(Wa>0).astype(float); N=W.shape[0]
    k=A.sum(1); km=k.mean()
    if km<1.5: return 0.0,{}
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
    L=np.mean(Lv) if Lv else float(N)
    Lr=np.log(N)/np.log(max(km,2))
    sigma=float(np.clip((Cm/Cr)/(L/max(Lr,1e-8)),0,20))
    R_sw=float(np.tanh(max(sigma-1,0)/2))
    comps=[v for v in [C_sc,H_sc,M_sc,R_sw] if v>0]
    return float(np.prod(comps)**(1./len(comps))) if comps else 0.0,\
           {'C':C_sc,'H':H_sc,'M':M_sc,'R_sw':R_sw,'sigma':sigma}

def compute_Gst(W,act_hist):
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
    if len(act_hist)<5: return 0.0
    mats=np.array(act_hist)
    cm=np.corrcoef(mats.T); cm=np.nan_to_num(cm,0)
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
    rng   = np.random.RandomState(seed)
    alpha = ALPHA_MAP.get(name, 3.47)

    if cfg['type']=='ce':
        W,EL,N = load_ce(rng)
    else:
        N=cfg['N']; W=make_ws(N,cfg['k'],cfg['p'],rng)
        EL=np.zeros((N,N),dtype=bool)

    W_init = W.copy()

    # E/I分配（Vreeswijk 1996）
    ei_types = assign_EI(N, rng)
    n_inh = (ei_types==-1).sum()
    print(f"  E/I: {N-n_inh}兴奋 + {n_inh}抑制({n_inh/N*100:.0f}%)")

    # τ结构（Murray 2014）
    comm_labels, n_comms = get_communities(W)
    tau = make_tau_structured(N, comm_labels, n_comms, rng)
    Theta = compute_Theta(tau)
    print(f"  τ: mean={tau.mean():.1f}  Θ={Theta:.3f}")

    # 含抑制的权重矩阵
    W_ei = apply_EI_weights(W, ei_types)

    ltp=np.zeros((N,N),dtype=np.int16); ltd=ltp.copy()
    ema=np.zeros(N,dtype=np.float32)
    h  =np.zeros(N,dtype=np.float32)
    act_window=[]; log=[]; t0=time.time()

    for step in range(N_STEPS):
        h   = activate_EI(W, W_ei, h, tau, rng)
        act = h.copy()
        ema = 0.97*ema + 0.03*act
        act_window.append(act.copy())
        if len(act_window)>50: act_window.pop(0)

        # 更新W_ei（W改变时同步更新）
        W,EL,ltp,ltd = rule1(W,EL,ltp,ltd,act)
        if step%LTP_DECAY_INT==0: ltp=np.maximum(ltp-1,0)
        if step%GROW_INT==0:
            W=rule2(W,EL,ema,rng)
            W_ei=apply_EI_weights(W,ei_types)  # 同步
        if step%SCALING_INT==0:
            W=rule3(W,ema)
            W_ei=apply_EI_weights(W,ei_types)
        if step%PRUNE_INT==0:
            W=rule4(W,EL,ema,rng)
            W_ei=apply_EI_weights(W,ei_types)

        if step%LOG_INT==0:
            Sc,_ = compute_Sc(W,rng)
            lam  = compute_lambda(act_window)
            phi  = compute_Phi(act_window)
            psi  = compute_Psi(W,W_init)
            tc_v = [v for v in [lam,phi,psi,Theta] if v>0]
            Tc   = float(np.prod(tc_v)**(1./len(tc_v))) if tc_v else 0.0
            Gst  = compute_Gst(W,act_window)
            cst  = float(Sc*Tc*np.exp(alpha*max(Gst,0))) if Sc>0 and Tc>0 else 0.0
            elr  = EL.sum()/max((W>0).sum(),1)
            act_r= float((act>0.1).mean())
            entry= {'step':step,'Sc':round(Sc,4),'Tc':round(Tc,4),
                    'lam':round(lam,4),'Phi':round(phi,4),
                    'Psi':round(psi,4),'Theta':round(Theta,4),
                    'Gst':round(Gst,4),'CST':round(cst,4),
                    'IIL':IIL(cst),'EL_r':round(float(elr),4),
                    'act_rate':round(act_r,4)}
            log.append(entry)
            print(f"  {name} s={seed} t={step:5d}: "
                  f"Sc={Sc:.3f} Tc={Tc:.3f}"
                  f"(λ={lam:.2f} Φ={phi:.2f} Ψ={psi:.2f} Θ={Theta:.2f}) "
                  f"Γ={Gst:.3f} CST={cst:.3f}[{IIL(cst)}] "
                  f"act={act_r*100:.0f}% ({time.time()-t0:.0f}s)")

    return {'net':name,'seed':seed,'alpha':alpha,'Theta':Theta,
            'n_inh':int(n_inh),'N':N,
            'log':log,'final':log[-1] if log else {}}

# ── 主程序 ────────────────────────────────────────────────
if __name__=='__main__':
    try: from sklearn.metrics import normalized_mutual_info_score
    except:
        import subprocess,sys
        subprocess.run([sys.executable,'-m','pip','install','scikit-learn','-q'])

    print("="*65)
    print("SDI 实验十二 — E/I平衡 + 抑制性神经元")
    print(f"  20%抑制性神经元 (Vreeswijk 1996 Science)")
    print(f"  抑制权重×{INH_WEIGHT} (Brunel 2000 J.Comput.Neurosci.)")
    print(f"  目标: λ 1.0→0.90  Ψ 0.07→0.20+  CST→L5")
    print("="*65)

    results=[]
    for name,cfg in NETWORKS.items():
        for seed in SEEDS:
            print(f"\n>>> {name}  seed={seed}  α={ALPHA_MAP.get(name,3.47)}")
            results.append(run(name,cfg,seed))

    print("\n"+"="*65+"  汇总:")
    by=defaultdict(list)
    for r in results: by[r['net']].append(r)

    print(f"\n{'网络':<15}{'λ':>6}{'Φ':>6}{'Ψ':>7}{'Θ':>7}"
          f"{'Tc':>7}{'Γst':>7}{'CST':>8}{'IIL':>12}")
    print("  "+"-"*72)
    summary={}
    for net,rl in by.items():
        fins=[r['final'] for r in rl if r['final']]
        if not fins: continue
        lam=np.mean([f.get('lam',0) for f in fins])
        phi=np.mean([f.get('Phi',0) for f in fins])
        psi=np.mean([f.get('Psi',0) for f in fins])
        th =np.mean([f.get('Theta',0) for f in fins])
        tc =np.mean([f.get('Tc',0)   for f in fins])
        gst=np.mean([f.get('Gst',0)  for f in fins])
        cst=np.mean([f.get('CST',0)  for f in fins])
        sc =np.mean([f.get('Sc',0)   for f in fins])
        ilv=fins[0].get('IIL','?')
        print(f"  {net:<15}{lam:>6.3f}{phi:>6.3f}{psi:>7.3f}{th:>7.3f}"
              f"{tc:>7.3f}{gst:>7.3f}{cst:>8.3f}{ilv:>12}")
        summary[net]={'Sc':float(sc),'Tc':float(tc),'lam':float(lam),
                      'Phi':float(phi),'Psi':float(psi),'Theta':float(th),
                      'Gst':float(gst),'CST':float(cst),'IIL':ilv}

    # 与实验九/十一对比
    print("\n【实验进化路线 CST对比】")
    e9  = {'WS_300':1.774,'C_elegans':0.402,'Human_HCP':2.148}
    e11 = {'WS_300':0.761,'C_elegans':0.897,'Human_HCP':1.735}
    for net in summary:
        c12=summary[net]['CST']
        print(f"  {net}: 实九={e9.get(net,0):.3f} → "
              f"实十一={e11.get(net,0):.3f} → "
              f"实十二={c12:.3f} [{summary[net]['IIL']}]")

    json.dump({'results':results,'summary':summary},open(OUT,'w'),indent=2)
    print(f"\n✅ 结果: {OUT}")
