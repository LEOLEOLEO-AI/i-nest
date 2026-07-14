"""
SDI 实验二十 — 真正的LIF激活（根本修复）
==========================================
问题：tanh激活无阈值 → 80%激活率 → 违反物理机理
修复：Leaky Integrate-and-Fire (LIF) 带激发阈值+不应期

文献依据：
  Lapicque 1907 — LIF神经元原始定义
  Gerstner & Kistler 2002 Spiking Neuron Models (Cambridge)
  Olshausen & Field 1996 Nature 381:607
    稀疏编码：皮层视觉区激活率<5%，信息容量最优
  Attwell & Laughlin 2001 J.Cereb.Blood.Flow.Metab.
    脑代谢约束：激活率正比于能耗，皮层≈1-5%
  Turrigiano et al. 1998 Nature 391:892
    稳态缩放目标：1-5Hz（对应激活率3-10%）

LIF参数（标准化单位，对应生物值）：
  V_thresh = 0.5      激发阈值（生物≈-55mV，静息-70mV，差15mV）
  V_reset  = 0.0      激发后重置（生物≈-70mV）
  tau_ref  = 3步      不应期（生物2-5ms，1步≈1ms）
  tau_mem  = 异质τ    膜时间常数（Murray 2014: 5-200ms）

预期结果：
  激活率：80% → 5-15%（符合生物实测）
  Φ（相位同步）：有物理意义的真实振荡相位
  λ_eff：真正的稀疏雪崩，分支比κ接近1.0
  CST：Human_HCP预期 > 2.5（向论文3.92收敛）
"""

import numpy as np, json, os, time
import networkx as nx
from collections import defaultdict
from scipy.stats import entropy
from scipy.signal import hilbert

BASE    = '/home/work/.openclaw/workspace/sdi_sim'
OUT     = os.path.join(BASE, 'exp20_LIF_results.json')
CE_DATA = os.path.join(BASE, 'celegans_sim/connectome_v8_data.json')

# ── 继承实验十九所有参数 ──────────────────────────────────
THETA_LTP=60; THETA_LTD=50; LTP_DECAY_INT=500; EL_WT_BOOST=1.5
GROW_INT=50; P_GROW=0.05; W_INIT_LO=0.05; W_INIT_HI=0.10
EI_RATIO=0.20; INH_RATIO=2.0   # LIF体系：激活已稀疏，轻度抑制
SCALING_INT=200; ACT_LO=0.03; ACT_HI=0.10
SCALE_UP=1.05; SCALE_DN=0.95
PRUNE_INT=200; P_PRUNE=0.05; MIN_EDGES=2; COMP_THR=0.5
TAU_MU=np.log(20); TAU_SIGMA=1.0; TAU_MIN=5.0; TAU_MAX=200.0
INTRA_SIGMA=0.3; HIST_LEN=200   # 更长窗口（稀疏激活需要更长历史）
FC_EMA_BETA=0.90  # 稀疏激活下快速积累FC

# ── LIF参数（Gerstner 2002）──────────────────────────────
V_THRESH  = 0.05   # 修正：基于突触电流范围标定    # 激发阈值
V_RESET   = 0.0    # 重置电位
TAU_REF   = 3      # 不应期步数（生物2-5ms）
V_DRIVE   = 0.05   # 标定：LIF体系驱动强度   # 外部驱动强度（感觉输入）
DRIVE_FRAC= 0.05   # 驱动节点比例（5%）

N_STEPS=15000; LOG_INT=1000; SEEDS=[42,7,13]  # 更长仿真（稀疏收敛慢）
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

# ══════════════════════════════════════════════════════════
# 核心修复：真正的LIF激活
# ══════════════════════════════════════════════════════════

def activate_LIF(W, V, tau, ei_types, ref_count, rng):
    """
    Leaky Integrate-and-Fire 神经元
    [Lapicque 1907; Gerstner & Kistler 2002]

    每步更新：
    1. 处于不应期的节点：V保持0，ref_count减1
    2. 其余节点：V += leak*V + I_syn + I_drive
    3. 超阈值节点：记录激发（spike=1），V重置为0，进入不应期

    E/I平衡：抑制性节点的输出乘以-INH_RATIO
    → 兴奋性输入和抑制性输入在同一时间步竞争
    → 这才是真正的E/I平衡（不是两阶段事后补偿）
    """
    N = W.shape[0]
    leak = (1.0 - 1.0/tau).astype(np.float32)

    # 当前激发状态（上一步的脉冲）
    spike_prev = (V >= V_THRESH).astype(np.float32)

    # 构建突触输出：E节点输出正值，I节点输出负值
    syn_output = spike_prev.copy()
    inh_mask = (ei_types == -1)
    syn_output[inh_mask] *= -INH_RATIO

    # 突触电流：I_syn = W @ syn_output
    I_syn = (W @ syn_output).astype(np.float32)

    # 外部感觉驱动（稀疏，5%节点）
    I_drive = np.zeros(N, dtype=np.float32)
    n_driven = max(2, int(N * DRIVE_FRAC))
    driven_idx = rng.choice(N, n_driven, replace=False)
    I_drive[driven_idx] = V_DRIVE

    # 不应期处理：处于不应期的节点不积分
    in_ref = (ref_count > 0)
    ref_count = np.maximum(ref_count - 1, 0)

    # LIF积分（只对非不应期节点）
    V_new = np.where(in_ref, 0.0, leak * V + I_syn + I_drive)

    # 激发检测：超过阈值 → spike
    new_spike = (V_new >= V_THRESH) & ~in_ref

    # 重置激发节点
    V_new = np.where(new_spike, V_RESET, V_new)
    V_new = np.clip(V_new, -1.0, V_THRESH)

    # 更新不应期计数器
    ref_count = np.where(new_spike, TAU_REF, ref_count)

    # 激活信号（用于后续处理）：激发=1，否则用V归一化
    act = new_spike.astype(np.float32)

    return V_new.astype(np.float32), act, ref_count.astype(np.int8)

# ── 四规则（继承实验十九）────────────────────────────────
def rule1(W,EL,ltp,ltd,act):
    a=(act>0.5).astype(np.int8); ia=(act<0.1).astype(np.int8)
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

# ── 修订后的Tc指标（继承实验十九）───────────────────────
def compute_lambda_kappa(hist, dt=5):
    if len(hist)<dt*3: return 0.5
    mats=np.array(hist); T=len(mats)
    sizes=[]
    for t in range(0,T-dt,dt):
        s=float((mats[t:t+dt]>0.5).sum()); sizes.append(max(s,1.0))
    if len(sizes)<2: return 0.5
    kappas=[sizes[i+1]/sizes[i] for i in range(len(sizes)-1)]
    kappa=float(np.mean(kappas))
    return float(np.clip(np.exp(-abs(kappa-1.0)),0,1))

def compute_phi_PLV_sparse(hist, comm_labels, n_comms):
    """
    稀疏激活下真正可用的相位锁定值
    LIF激活后激活率<15%，Hilbert变换有效
    [Lachaux 1999; Varela 2001]
    """
    if len(hist)<20 or n_comms<2: return 0.0
    mats=np.array(hist,dtype=float); T=mats.shape[0]
    # 按社区计算平均激活时序
    comm_series={}
    for ci in range(n_comms):
        mask=(comm_labels==ci)
        if mask.sum()<2: continue
        s=mats[:,mask].mean(axis=1)
        if s.std()>1e-4: comm_series[ci]=s
    if len(comm_series)<2: return 0.0
    # Hilbert变换获取相位
    phases={}
    for ci,s in comm_series.items():
        try:
            an=hilbert(s); phases[ci]=np.angle(an)
        except: pass
    if len(phases)<2: return 0.0
    ids=list(phases.keys()); plvs=[]
    for i in range(len(ids)):
        for j in range(i+1,len(ids)):
            pa=phases[ids[i]]; pb=phases[ids[j]]
            T_c=min(len(pa),len(pb))
            plv=float(np.abs(np.mean(np.exp(1j*(pa[:T_c]-pb[:T_c])))))
            plvs.append(plv)
    return float(np.mean(plvs)) if plvs else 0.0

def compute_phi_FC(FC_ema):
    """备用：FC异质性（高密度时用）"""
    N=FC_ema.shape[0]
    mask=np.triu(np.ones((N,N),dtype=bool),k=1)
    fc_vals=np.abs(FC_ema[mask])
    if len(fc_vals)<10: return 0.0
    mean_fc=fc_vals.mean(); std_fc=fc_vals.std()
    if mean_fc<1e-8: return 0.0
    cv=std_fc/(mean_fc+1e-8)
    return float(np.clip(1.0/(1.0+np.exp(-2.0*cv+1.0)),0,1))

def compute_Psi_rate(W,W_prev):
    if W_prev is None: return 0.0
    nW=np.linalg.norm(W,'fro'); ndW=np.linalg.norm(W-W_prev,'fro')
    if nW<1e-8: return 0.0
    return float(np.clip(np.tanh(ndW/nW*10),0,1))

def compute_Sc_comms(W,rng):
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
    return Sc,lbl,n_comms

def compute_Gst_EMA(FC_ema,W,rng):
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
    fc_abs=np.abs(FC_ema)
    thr=np.percentile(fc_abs[fc_abs>0],70) if (fc_abs>0).any() else 0.3
    FC_bin=(fc_abs>thr).astype(float); np.fill_diagonal(FC_bin,0)
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
def run(name,cfg,seed):
    rng=np.random.RandomState(seed); alpha=ALPHA_MAP.get(name,3.47)
    if cfg['type']=='ce': W,EL,N=load_ce(rng)
    else:
        N=cfg['N']; W=make_ws(N,cfg['k'],cfg['p'],rng)
        EL=np.zeros((N,N),dtype=bool)
    ei=assign_EI(N,rng)
    cl,nc=get_communities(W); tau=make_tau(N,cl,nc,rng)
    TH=Theta(tau)

    # LIF状态初始化
    V=np.zeros(N,dtype=np.float32)          # 膜电位
    ref_count=np.zeros(N,dtype=np.int8)     # 不应期计数
    W_prev=W.copy()
    FC_ema=np.zeros((N,N),dtype=np.float32)
    ema=np.zeros(N,dtype=np.float32)
    ltp=np.zeros((N,N),dtype=np.int16); ltd=ltp.copy()
    curr_lbl=cl; curr_nc=nc
    hist=[]; log=[]; t0=time.time()

    print(f"  E/I:{(ei==1).sum()}E+{(ei==-1).sum()}I  nc={nc}  Θ={TH:.3f}")

    for step in range(N_STEPS):
        # LIF激活（真正的脉冲激发）
        V,act,ref_count=activate_LIF(W,V,tau,ei,ref_count,rng)
        ema=0.97*ema+0.03*act
        FC_ema=FC_EMA_BETA*FC_ema+(1-FC_EMA_BETA)*np.outer(act,act)
        hist.append(act.copy())
        if len(hist)>HIST_LEN: hist.pop(0)

        W,EL,ltp,ltd=rule1(W,EL,ltp,ltd,act)
        if step%LTP_DECAY_INT==0: ltp=np.maximum(ltp-1,0)
        if step%GROW_INT==0:    W=rule2(W,EL,ema,rng)
        if step%SCALING_INT==0: W=rule3(W,ema)
        if step%PRUNE_INT==0:   W=rule4(W,EL,ema,rng)

        if step%LOG_INT==0:
            Sc,curr_lbl,curr_nc=compute_Sc_comms(W,rng)
            lam=compute_lambda_kappa(hist)
            act_rate=float(act.mean())

            # Φ：激活率<20%用PLV（有振荡），否则用FC异质性
            if act_rate < 0.20:
                phi=compute_phi_PLV_sparse(hist,curr_lbl,curr_nc)
            else:
                phi=compute_phi_FC(FC_ema)

            psi=compute_Psi_rate(W,W_prev); W_prev=W.copy()
            tc_v=[v for v in [lam,phi,psi,TH] if v>0.01]
            Tc=float(np.prod(tc_v)**(1./len(tc_v))) if tc_v else 0.0
            Gst=compute_Gst_EMA(FC_ema,W,rng)
            cst=float(Sc*Tc*np.exp(alpha*max(Gst,0))) if Sc>0 and Tc>0 else 0.0
            elr=EL.sum()/max((W>0).sum(),1)
            entry={'step':step,'Sc':round(Sc,4),'Tc':round(Tc,4),
                   'lam':round(lam,4),'Phi':round(phi,4),
                   'Psi':round(psi,4),'Theta':round(TH,4),
                   'Gst':round(Gst,4),'CST':round(cst,4),
                   'IIL':IIL(cst),'EL_r':round(float(elr),4),
                   'act':round(act_rate,4)}
            log.append(entry)
            print(f"  {name} s={seed} t={step:5d}: "
                  f"Sc={Sc:.3f} Tc={Tc:.3f}"
                  f"(λ={lam:.3f} Φ={phi:.3f} Ψ={psi:.2f} Θ={TH:.2f}) "
                  f"Γ={Gst:.3f} CST={cst:.3f}[{IIL(cst)}] "
                  f"act={act_rate*100:.1f}% ({time.time()-t0:.0f}s)")

    return {'net':name,'seed':seed,'alpha':alpha,'Theta':TH,
            'log':log,'final':log[-1] if log else {}}

# ── 主程序 ────────────────────────────────────────────────
if __name__=='__main__':
    try: from sklearn.metrics import normalized_mutual_info_score
    except:
        import subprocess,sys
        subprocess.run([sys.executable,'-m','pip','install','scikit-learn','-q'])
    print("="*65)
    print("SDI 实验二十 — 真正的LIF激活（根本修复）")
    print(f"  V_thresh={V_THRESH}  V_reset={V_RESET}  tau_ref={TAU_REF}步")
    print(f"  [Lapicque 1907 / Gerstner 2002 / Olshausen & Field 1996]")
    print(f"  目标激活率：5-15%（生物皮层实测值）")
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
    print(f"\n{'网络':<15}{'act%':>7}{'λ':>7}{'Φ':>7}{'Ψ':>7}{'Tc':>7}{'Γst':>7}{'CST':>8}{'IIL':>12}")
    print("  "+"-"*72)
    for net,rl in by.items():
        fins=[r['final'] for r in rl if r['final']]
        if not fins: continue
        act=np.mean([f.get('act',0) for f in fins])
        lm =np.mean([f.get('lam',0) for f in fins])
        ph =np.mean([f.get('Phi',0) for f in fins])
        ps =np.mean([f.get('Psi',0) for f in fins])
        th =np.mean([f.get('Theta',0) for f in fins])
        tc =np.mean([f.get('Tc',0)   for f in fins])
        gst=np.mean([f.get('Gst',0)  for f in fins])
        cst=np.mean([f.get('CST',0)  for f in fins])
        sc =np.mean([f.get('Sc',0)   for f in fins])
        ilv=fins[0].get('IIL','?')
        print(f"  {net:<15}{act*100:>7.1f}{lm:>7.3f}{ph:>7.3f}{ps:>7.3f}"
              f"{tc:>7.3f}{gst:>7.3f}{cst:>8.3f}{ilv:>12}")
        summary[net]={'Sc':float(sc),'Tc':float(tc),'lam':float(lm),
                      'Phi':float(ph),'Psi':float(ps),'Theta':float(th),
                      'Gst':float(gst),'CST':float(cst),'IIL':ilv,'act':float(act)}
    print("\n【与论文Table 2对比】")
    for net,ref in {'C_elegans':0.357,'Human_HCP':3.920}.items():
        if net in summary:
            cst=summary[net]['CST']; act=summary[net]['act']
            print(f"  {net}: 仿真={cst:.3f}  论文={ref}  "
                  f"比值={cst/ref:.2f}×  act={act*100:.1f}%  [{summary[net]['IIL']}]")
    json.dump({'results':results,'summary':summary},open(OUT,'w'),indent=2)
    print(f"\n✅ {OUT}")
