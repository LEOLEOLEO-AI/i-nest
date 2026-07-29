"""
SDI 实验十三 — 四规则完整合并版（最终验证）
============================================
把E/I平衡作为Rule3不可分割的物理基底整合进来。
这不是新机制，而是Rule3的正确完整实现。

Rule3完整形式（双层）：
  层1 E/I平衡（即时，激活层）：Vreeswijk 1996 Science
  层2 稳态缩放（慢速，权重层）：Turrigiano 1998 Nature

其余规则与v5完全一致。
参数：INH_RATIO=7.0（Brunel 2000：6-8倍取中值）
"""

import numpy as np, json, os, time
import networkx as nx
from collections import defaultdict
from scipy.stats import entropy

BASE    = '/vault/sdi_sim'
OUT     = os.path.join(BASE, 'exp13_final_results.json')
CE_DATA = os.path.join(BASE, 'celegans_sim/connectome_v8_data.json')

# ══════════════════════════════════════════════════════════
# 完整参数（全部有文献依据，见 SDI_Rules_Bio_Evidence_v1.md）
# ══════════════════════════════════════════════════════════

# Rule1 STDP  [Bi&Poo 1998; Song 2000]
THETA_LTP     = 60
THETA_LTD     = 50
LTP_DECAY_INT = 500
EL_WT_BOOST   = 1.5

# Rule2 新生突触  [PMC6704923; Zito 2009; Holtmaat 2009]
GROW_INT      = 50
P_GROW        = 0.05
W_INIT_LO     = 0.05
W_INIT_HI     = 0.10

# Rule3 层1：E/I平衡  [Vreeswijk 1996 Science; Brunel 2000]
EI_RATIO      = 0.20    # 20%抑制性神经元
INH_RATIO     = 7.0     # 抑制权重倍数（Brunel: 6-8倍取中值）

# Rule3 层2：稳态缩放  [Turrigiano 1998 Nature; Turrigiano 2012 CSHP]
SCALING_INT   = 200
ACT_LO        = 0.03    # 目标激活率下限（皮层1-5Hz稀疏编码）
ACT_HI        = 0.10    # 目标激活率上限
SCALE_UP      = 1.05
SCALE_DN      = 0.95

# Rule4 竞争修剪  [Sanes&Lichtman 1999; Science 2022]
PRUNE_INT     = 200
P_PRUNE       = 0.05
MIN_EDGES     = 2
COMP_THR      = 0.5

# 异质LIF时间常数  [Murray 2014 Nat.Neurosci.; Perez-Nieves 2021 Nat.Commun.]
TAU_MU        = np.log(20)
TAU_SIGMA     = 1.0
TAU_MIN       = 5.0
TAU_MAX       = 200.0
INTRA_SIGMA   = 0.3     # 社区内τ标准差（Murray 2014: ρ=0.6-0.8）

N_STEPS = 10000
LOG_INT = 1000
SEEDS   = [42, 7, 13]

ALPHA_MAP = {
    'WS_300':    3.47,
    'C_elegans': 2.56,
    'Human_HCP': 3.91,
}
NETWORKS = {
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
    """20%抑制性神经元  [Vreeswijk 1996]"""
    types = np.ones(N, dtype=np.float32)
    types[rng.choice(N, int(N*EI_RATIO), replace=False)] = -1.0
    return types

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
        N=W.shape[0]; return np.arange(N)%5,5

def make_tau(N, comm_labels, n_comms, rng):
    """社区感知异质τ  [Murray 2014; Perez-Nieves 2021]"""
    centers=np.linspace(np.log(TAU_MIN*1.5),np.log(TAU_MAX*0.7),max(n_comms,1))
    rng.shuffle(centers)
    tau=np.zeros(N,dtype=np.float32)
    for i in range(N):
        ci=comm_labels[i]%len(centers)
        tau[i]=float(np.clip(np.exp(rng.normal(centers[ci],INTRA_SIGMA)),TAU_MIN,TAU_MAX))
    return tau

def compute_Theta(tau):
    hist,_=np.histogram(np.log(tau),bins=10)
    hist=hist[hist>0].astype(float); hist/=hist.sum()
    return float(np.clip(entropy(hist)/np.log(10),0,1))

# ── Rule3 层1：E/I平衡激活（激活层，即时）────────────────
def activate_EI(W, W_ei, h, tau, rng):
    """
    Rule3-层1：E/I平衡异质LIF
    抑制性输出权重为负 → 稀疏激活 → λ<1
    [Vreeswijk 1996; Brunel 2000]
    """
    N    = W.shape[0]
    leak = (1.0 - 1.0/tau).astype(np.float32)
    # 少量外部驱动（感觉输入）
    n_in = max(3, int(N*0.05))
    drive = np.zeros(N, dtype=np.float32)
    drive[rng.choice(N, n_in, replace=False)] = rng.uniform(0.2, 0.6, n_in)
    # E/I平衡LIF更新
    h_new = leak * h + np.tanh(W_ei @ h + drive)
    h_new = np.where(h_new > 0.1, h_new, 0.0)
    h_new = np.clip(h_new, 0, 1)
    return h_new.astype(np.float32)

# ── Rule1：STDP  [Bi&Poo 1998; Song 2000] ─────────────────
def rule1_stdp(W, EL, ltp, ltd, act):
    a=(act>0.30).astype(np.int8); ia=(act<0.08).astype(np.int8)
    lev=np.outer(a,a).astype(np.int16); lev&=(W>0); np.fill_diagonal(lev,0)
    lde=np.outer(ia,a).astype(np.int16); lde&=(W>0)
    ltp+=lev; ltd+=lde
    nel=(ltp>=THETA_LTP)&~EL&(W>0)
    EL|=nel; W[nel]=np.minimum(W[nel]*EL_WT_BOOST,1.0)
    pm=(ltd>=THETA_LTD)&~EL&(W>0)
    pm&=((W>0).sum(1,keepdims=True)>MIN_EDGES)
    if pm.any(): W[pm]=0; ltp[pm]=0; ltd[pm]=0
    np.fill_diagonal(W,0); return W,EL,ltp,ltd

# ── Rule2：新生突触  [PMC6704923; Zito 2009; Holtmaat 2009] ─
def rule2_nascent(W, EL, ema, rng):
    N=W.shape[0]; n=max(1,int(N*P_GROW*0.01)); ng=0
    for _ in range(n):
        if ng>=int(N*0.15): break
        wi=ema+0.01; wi/=wi.sum(); i=rng.choice(N,p=wi)
        wj=ema.copy()+0.01; wj[i]=0; wj[W[i]>0]=0
        if wj.sum()<1e-8: continue
        wj/=wj.sum(); j=rng.choice(N,p=wj)
        W[i,j]=rng.uniform(W_INIT_LO,W_INIT_HI); ng+=1
    np.fill_diagonal(W,0); return W

# ── Rule3 层2：稳态缩放（权重层，慢速）───────────────────
def rule3_scaling(W, ema):
    """
    Rule3-层2：乘性稳态缩放
    在E/I平衡之上精细调节激活率到[3%,10%]
    [Turrigiano 1998; Turrigiano 2012]
    """
    up=ema<ACT_LO; dn=ema>ACT_HI
    if up.any(): W[up,:]=np.minimum(W[up,:]*SCALE_UP,1.0)
    if dn.any(): W[dn,:]*=SCALE_DN
    np.fill_diagonal(W,0); return W

# ── Rule4：竞争修剪  [Sanes&Lichtman 1999; Science 2022] ─────
def rule4_prune(W, EL, ema, rng):
    N=W.shape[0]; deg=(W>0).sum(1)
    for i in np.where(deg>MIN_EDGES)[0]:
        nb=np.where(W[i]>0)[0]
        if len(nb)<2: continue
        thr=np.median(ema[nb])*COMP_THR
        for j in nb:
            if not EL[i,j] and ema[j]<thr and \
               rng.random()<P_PRUNE and deg[i]>MIN_EDGES:
                W[i,j]=0; deg[i]-=1
    return W

# ── 指标 ─────────────────────────────────────────────────
def compute_lambda(hist):
    if len(hist)<2: return 0.0
    rs=[]
    for t in range(len(hist)-1):
        n0=(hist[t]>0.1).sum(); n1=(hist[t+1]>0.1).sum()
        if n0>0: rs.append(n1/n0)
    if not rs: return 0.0
    lam=float(np.mean(rs))
    return float(np.clip(1.0-abs(lam-1.0)/(lam+1.0+1e-8),0,1))

def compute_Phi(hist):
    if len(hist)<4: return 0.0
    mats=np.array(hist); cs=[]
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
    L=np.mean(Lv) if Lv else float(N); Lr=np.log(N)/np.log(max(km,2))
    sigma=float(np.clip((Cm/Cr)/(L/max(Lr,1e-8)),0,20))
    R_sw=float(np.tanh(max(sigma-1,0)/2))
    comps=[v for v in [C_sc,H_sc,M_sc,R_sw] if v>0]
    return float(np.prod(comps)**(1./len(comps))) if comps else 0.0,\
           {'C':C_sc,'H':H_sc,'M':M_sc,'R_sw':R_sw,'sigma':sigma}

def compute_Gst(W, hist):
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
    mats=np.array(hist)
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

    # Rule3-层1：E/I分配（一次性，固定类型）
    ei_types = assign_EI(N, rng)
    n_inh    = (ei_types==-1).sum()

    # 构建含抑制的有效权重矩阵
    def build_Wei(W, ei):
        Wei = W.copy()
        Wei[ei==-1, :] *= -INH_RATIO
        return Wei

    W_ei = build_Wei(W, ei_types)

    # 异质τ（Murray 2014，社区感知）
    comm_labels, n_comms = get_communities(W)
    tau   = make_tau(N, comm_labels, n_comms, rng)
    Theta = compute_Theta(tau)

    print(f"  E/I: {N-n_inh}E+{n_inh}I({n_inh/N*100:.0f}%)  "
          f"τ_mean={tau.mean():.1f}  Θ={Theta:.3f}")

    ltp=np.zeros((N,N),dtype=np.int16); ltd=ltp.copy()
    ema=np.zeros(N,dtype=np.float32)
    h  =np.zeros(N,dtype=np.float32)
    hist=[]; log=[]; t0=time.time()

    for step in range(N_STEPS):
        # 激活（Rule3-层1 E/I平衡）
        h   = activate_EI(W, W_ei, h, tau, rng)
        act = h.copy()
        ema = 0.97*ema + 0.03*act
        hist.append(act.copy())
        if len(hist)>50: hist.pop(0)

        # Rule1 STDP（每步，最快）
        W,EL,ltp,ltd = rule1_stdp(W,EL,ltp,ltd,act)
        if step%LTP_DECAY_INT==0: ltp=np.maximum(ltp-1,0)

        # Rule2 新生突触（每50步）
        if step%GROW_INT==0:
            W    = rule2_nascent(W,EL,ema,rng)
            W_ei = build_Wei(W, ei_types)  # 同步更新

        # Rule3-层2 稳态缩放（每200步）
        if step%SCALING_INT==0:
            W    = rule3_scaling(W,ema)
            W_ei = build_Wei(W, ei_types)

        # Rule4 竞争修剪（每200步，最慢）
        if step%PRUNE_INT==0:
            W    = rule4_prune(W,EL,ema,rng)
            W_ei = build_Wei(W, ei_types)

        # 记录指标
        if step%LOG_INT==0:
            Sc,Sc_c = compute_Sc(W,rng)
            lam     = compute_lambda(hist)
            phi     = compute_Phi(hist)
            psi     = compute_Psi(W,W_init)
            tc_v    = [v for v in [lam,phi,psi,Theta] if v>0]
            Tc      = float(np.prod(tc_v)**(1./len(tc_v))) if tc_v else 0.0
            Gst     = compute_Gst(W,hist)
            cst     = float(Sc*Tc*np.exp(alpha*max(Gst,0))) if Sc>0 and Tc>0 else 0.0
            elr     = EL.sum()/max((W>0).sum(),1)
            act_r   = float((act>0.1).mean())
            entry   = {'step':step,'Sc':round(Sc,4),'Tc':round(Tc,4),
                       'lam':round(lam,4),'Phi':round(phi,4),
                       'Psi':round(psi,4),'Theta':round(Theta,4),
                       'Gst':round(Gst,4),'CST':round(cst,4),
                       'IIL':IIL(cst),'EL_r':round(float(elr),4),
                       'act':round(act_r,4)}
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
    print("SDI 实验十三 — 四规则完整合并（最终验证）")
    print("  Rule3完整形式：E/I平衡（层1）+ 稳态缩放（层2）")
    print(f"  Vreeswijk 1996: {EI_RATIO*100:.0f}%抑制  "
          f"Brunel 2000: INH={INH_RATIO}×")
    print(f"  Murray 2014: 异质τ[{TAU_MIN},{TAU_MAX}]步")
    print("="*65)

    results=[]
    for name,cfg in NETWORKS.items():
        for seed in SEEDS:
            print(f"\n>>> {name}  seed={seed}  α={ALPHA_MAP.get(name,3.47)}")
            results.append(run(name,cfg,seed))

    print("\n"+"="*65+"  最终汇总:")
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
        tc =np.mean([f.get('Tc',0)  for f in fins])
        gst=np.mean([f.get('Gst',0) for f in fins])
        cst=np.mean([f.get('CST',0) for f in fins])
        sc =np.mean([f.get('Sc',0)  for f in fins])
        ilv=fins[0].get('IIL','?')
        print(f"  {net:<15}{lam:>6.3f}{phi:>6.3f}{psi:>7.3f}{th:>7.3f}"
              f"{tc:>7.3f}{gst:>7.3f}{cst:>8.3f}{ilv:>12}")
        summary[net]={'Sc':float(sc),'Tc':float(tc),'lam':float(lam),
                      'Phi':float(phi),'Psi':float(psi),'Theta':float(th),
                      'Gst':float(gst),'CST':float(cst),'IIL':ilv}

    # 与论文Table2对比
    print("\n【与CST论文Table 2对比】")
    REF = {'C_elegans':0.357,'Human_HCP':3.920}
    for net,ref in REF.items():
        if net in summary:
            cst=summary[net]['CST']
            print(f"  {net}: 仿真={cst:.3f}  论文={ref}  "
                  f"比值={cst/ref:.2f}×  [{summary[net]['IIL']}]")

    # 实验进化路线
    print("\n【实验进化路线 CST】")
    ref_cst = {'WS_300':(1.774,'实验九基准'),
               'C_elegans':(0.402,'实验九基准'),
               'Human_HCP':(2.148,'实验九基准')}
    for net,s in summary.items():
        base,label=ref_cst.get(net,(0,''))
        delta=s['CST']-base
        print(f"  {net}: {base:.3f}({label}) → {s['CST']:.3f} "
              f"Δ={delta:+.3f} [{s['IIL']}]")

    json.dump({'results':results,'summary':summary},open(OUT,'w'),indent=2)
    print(f"\n✅ 结果: {OUT}")
