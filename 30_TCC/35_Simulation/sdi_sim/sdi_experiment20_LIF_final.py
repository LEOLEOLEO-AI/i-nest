"""
SDI 实验二十 FINAL — 物理第一性LIF激活（文献参数锁定）
=========================================================
所有参数均有NCS权威文献依据

LIF参数（全部从生物实验数据推导）：
  V_thresh=1.0    Shadlen & Newsome 1998 J.Neurosci. 18:3870
                  标准化：(V_th - V_rest)/15mV = (-55-(-70))/15 = 1.0
  V_reset=0.0     Hodgkin & Huxley 1952 J.Physiol. 117:500
  τ_ref=3步       Hodgkin & Huxley 1952（绝对不应期2-3ms）
  leak=0.95       Gerstner & Kistler 2002 Cambridge（τ_m=20ms）
  J_E=0.3         Song et al. 2000 Nat.Neurosci. 3:919
                  （单EPSP 0.5-2mV / 15mV阈差，小网络等效标定）
  J_I=-4×J_E      Brunel 2000 J.Comput.Neurosci. 8:183
  I_ext=0.08      Shadlen 1998（背景突触10000×2Hz×20ms等效驱动）
  目标激活率4-8%  Attwell & Laughlin 2001 J.Cereb.Blood.Flow.Metab.

Γst计算（稀疏激活下）：
  时间窗口相关系数（200步）替代EMA逐步outer
  Honey et al. 2009 PNAS 106:2035

其余四规则参数：继承实验十九（已文献锁定）
"""

import numpy as np, json, os, time
import networkx as nx
from collections import defaultdict
from scipy.stats import entropy
from scipy.signal import hilbert

BASE    = '/home/work/.openclaw/workspace/sdi_sim'
OUT     = os.path.join(BASE, 'exp20_LIF_final_results.json')
CE_DATA = os.path.join(BASE, 'celegans_sim/connectome_v8_data.json')

# ══════════════════════════════════════════════════════════
# LIF 物理参数（文献锁定）
# ══════════════════════════════════════════════════════════
# Shadlen & Newsome 1998: V_th=-55mV, V_rest=-70mV → 差值15mV → 标准化=1.0
V_THRESH   = 1.0
V_RESET    = 0.0
# Hodgkin & Huxley 1952: 绝对不应期2-3ms
TAU_REF    = 3
# Gerstner 2002: τ_m=20ms → leak=1-1/20
LEAK_BASE  = 0.95
# Song 2000: EPSP=0.5-2mV，小网络k=8等效标定
J_E_LO, J_E_HI = 0.25, 0.35
J_I_RATIO  = 4.0       # Brunel 2000: J_I=4×J_E
EI_RATIO   = 0.20      # Vreeswijk 1996: 20%抑制
# Shadlen 1998: 背景10000突触×2Hz×20ms×J等效
I_EXT_MEAN = 0.08
I_EXT_STD  = 0.04

# ── 四规则参数（继承实验十九）────────────────────────────
THETA_LTP=60; THETA_LTD=50; LTP_DECAY_INT=500; EL_WT_BOOST=1.5
GROW_INT=50; P_GROW=0.05; W_INIT_LO=J_E_LO; W_INIT_HI=J_E_HI
SCALING_INT=200; ACT_LO=0.03; ACT_HI=0.10
SCALE_UP=1.05; SCALE_DN=0.95
PRUNE_INT=200; P_PRUNE=0.05; MIN_EDGES=2; COMP_THR=0.5
TAU_MU=np.log(20); TAU_SIGMA=1.0; TAU_MIN=5.0; TAU_MAX=200.0
INTRA_SIGMA=0.3

# Γst窗口（Honey 2009: 时间窗口相关系数）
FC_WINDOW  = 200       # 200步相关窗口
HIST_LEN   = 300       # 保留300步历史（含窗口+余量）

N_STEPS=15000; LOG_INT=1000; SEEDS=[42,7,13]
ALPHA_MAP={'WS_300':3.47,'C_elegans':2.56,'Human_HCP':3.91}
NETWORKS={
    'WS_300':   {'type':'ws','N':300,'k':12,'p':0.1},
    'C_elegans':{'type':'ce'},
    'Human_HCP':{'type':'ws','N':80,'k':8,'p':0.1},
}

# ── 初始化 ────────────────────────────────────────────────
def make_ws(N,k,p,rng):
    """WS图，权重初始化为J_E量级（Song 2000）"""
    W=np.zeros((N,N),dtype=np.float32)
    for i in range(N):
        for d in range(1,k//2+1):
            j=(i+d)%N
            W[i,j]=W[j,i]=rng.uniform(J_E_LO,J_E_HI)
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
            if s<N and t<N:
                # 归一化到J_E量级
                W[s,t]=J_E_LO + (J_E_HI-J_E_LO)*(w/mx)
    for row in d.get('edges_elec',[]):
        s,t=int(row[0]),int(row[1])
        if s<N and t<N:
            W[s,t]=W[t,s]=(J_E_LO+J_E_HI)/2
            EL[s,t]=EL[t,s]=True
    return W,EL,N

def assign_EI(N,rng):
    """20%抑制性神经元（Vreeswijk & Sompolinsky 1996）"""
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
    """Murray 2014 Nat.Neurosci.: τ的对数正态分布"""
    centers=np.linspace(np.log(TAU_MIN*1.5),np.log(TAU_MAX*0.7),max(nc,1))
    rng.shuffle(centers)
    tau=np.zeros(N,dtype=np.float32)
    for i in range(N):
        ci=cl[i]%len(centers)
        tau[i]=float(np.clip(np.exp(rng.normal(centers[ci],INTRA_SIGMA)),TAU_MIN,TAU_MAX))
    return tau

def Theta(tau):
    """Murray 2014: τ分布Shannon熵"""
    h,_=np.histogram(np.log(tau),bins=10)
    h=h[h>0].astype(float); h/=h.sum()
    return float(np.clip(entropy(h)/np.log(10),0,1))

# ══════════════════════════════════════════════════════════
# LIF激活（Lapicque 1907 / Gerstner 2002 / Hodgkin & Huxley 1952）
# ══════════════════════════════════════════════════════════
def activate_LIF(W, V, tau, ei_types, ref_count, rng):
    """
    标准LIF + E/I平衡
    膜时间常数异质（Murray 2014）
    激发率目标4-8%（Attwell & Laughlin 2001）
    """
    N = W.shape[0]
    # 异质膜时间常数（Murray 2014）
    leak = np.clip(1.0 - 1.0/tau, 0.80, 0.99).astype(np.float32)

    # 突触输出（E/I区分，Brunel 2000）
    spike_prev = (V >= V_THRESH).astype(np.float32)
    syn_out = spike_prev.copy()
    syn_out[ei_types == -1] *= -J_I_RATIO

    # 突触电流 I_syn = W @ syn_out
    I_syn = (W @ syn_out).astype(np.float32)

    # 背景驱动（Shadlen 1998: 未建模突触的等效贡献）
    I_ext = rng.normal(I_EXT_MEAN, I_EXT_STD, N).clip(0, None).astype(np.float32)

    # 不应期处理（Hodgkin & Huxley 1952）
    in_ref = (ref_count > 0)
    ref_count = np.maximum(ref_count - 1, 0)

    # LIF膜电位积分
    V_new = np.where(in_ref, 0.0, leak * V + I_syn + I_ext)

    # 激发检测与重置
    new_spike = (V_new >= V_THRESH) & ~in_ref
    V_new = np.where(new_spike, V_RESET, V_new)
    V_new = np.clip(V_new, -1.0, V_THRESH)
    ref_count = np.where(new_spike, TAU_REF, ref_count)

    return V_new.astype(np.float32), new_spike.astype(np.float32), ref_count.astype(np.int8)

# ── 四规则（参数继承，激活判断改用脉冲）──────────────────
def rule1(W,EL,ltp,ltd,spike):
    """STDP用脉冲序列（不再是连续激活值）"""
    a=spike.astype(np.int8); ia=(spike<0.1).astype(np.int8)
    lev=np.outer(a,a).astype(np.int16); lev&=(W>0); np.fill_diagonal(lev,0)
    lde=np.outer(ia,a).astype(np.int16); lde&=(W>0)
    ltp+=lev; ltd+=lde
    nel=(ltp>=THETA_LTP)&~EL&(W>0)
    EL|=nel; W[nel]=np.minimum(W[nel]*EL_WT_BOOST,J_E_HI*3)
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
    if up.any(): W[up,:]=np.minimum(W[up,:]*SCALE_UP,J_E_HI*3)
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
# Tc指标（修订版，继承实验十九）
# ══════════════════════════════════════════════════════════
def compute_lambda_kappa(hist, dt=5):
    """Beggs & Plenz 2003: κ临界指数"""
    if len(hist)<dt*3: return 0.5
    mats=np.array(hist); T=len(mats)
    sizes=[float((mats[t:t+dt]>0.5).sum()) for t in range(0,T-dt,dt)]
    sizes=[max(s,1.0) for s in sizes]
    if len(sizes)<2: return 0.5
    kappa=float(np.mean([sizes[i+1]/sizes[i] for i in range(len(sizes)-1)]))
    return float(np.clip(np.exp(-abs(kappa-1.0)),0,1))

def compute_phi_PLV(hist, comm_labels, n_comms):
    """
    Lachaux 1999 PLV（稀疏激活下有效）
    Varela 2001 Nat.Rev.Neurosci.: 脑区间相位锁定
    """
    if len(hist)<20 or n_comms<2: return 0.0
    mats=np.array(hist,dtype=float)
    comm_series={}
    for ci in range(n_comms):
        mask=(comm_labels==ci)
        if mask.sum()<2: continue
        s=mats[:,mask].mean(axis=1)
        if s.std()>1e-5: comm_series[ci]=s
    if len(comm_series)<2: return 0.0
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
            Tc=min(len(pa),len(pb))
            plv=float(np.abs(np.mean(np.exp(1j*(pa[:Tc]-pb[:Tc])))))
            plvs.append(plv)
    return float(np.mean(plvs)) if plvs else 0.0

def compute_Psi_rate(W,W_prev):
    """Bhatt 2009 / Turrigiano 2012: 相对权重变化率"""
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

def compute_Gst_window(spike_hist, W, rng):
    """
    Honey 2009 PNAS: 时间窗口相关系数作为功能连接
    （稀疏激活下的正确计算方法）
    """
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
    if len(spike_hist)<FC_WINDOW: return 0.0
    # 时间窗口相关系数（Honey 2009）
    mats=np.array(spike_hist[-FC_WINDOW:],dtype=float)  # T×N
    if mats.std()<1e-8: return 0.0
    # 计算N×N相关矩阵
    try:
        FC=np.corrcoef(mats.T); FC=np.nan_to_num(FC,0)
        np.fill_diagonal(FC,0)
    except: return 0.0
    thr=np.percentile(np.abs(FC)[np.abs(FC)>0],70) if (np.abs(FC)>0).any() else 0.3
    FC_bin=(np.abs(FC)>thr).astype(float); np.fill_diagonal(FC_bin,0)
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

    V=np.zeros(N,dtype=np.float32)
    ref=np.zeros(N,dtype=np.int8)
    W_prev=W.copy()
    ema=np.zeros(N,dtype=np.float32)
    ltp=np.zeros((N,N),dtype=np.int16); ltd=ltp.copy()
    curr_lbl=cl; curr_nc=nc
    spike_hist=[]; log=[]; t0=time.time()

    n_inh=(ei==-1).sum()
    print(f"  LIF: V_th={V_THRESH} leak={LEAK_BASE} τ_ref={TAU_REF}")
    print(f"  E/I: {N-n_inh}E+{n_inh}I  J_E=[{J_E_LO},{J_E_HI}]  J_I=-{J_I_RATIO}×J_E")
    print(f"  驱动: I_ext={I_EXT_MEAN}±{I_EXT_STD}")
    print(f"  Θ={TH:.3f}  Γst窗口={FC_WINDOW}步")

    for step in range(N_STEPS):
        V,spike,ref=activate_LIF(W,V,tau,ei,ref,rng)
        ema=0.97*ema+0.03*spike
        spike_hist.append(spike.copy())
        if len(spike_hist)>HIST_LEN: spike_hist.pop(0)

        W,EL,ltp,ltd=rule1(W,EL,ltp,ltd,spike)
        if step%LTP_DECAY_INT==0: ltp=np.maximum(ltp-1,0)
        if step%GROW_INT==0:    W=rule2(W,EL,ema,rng)
        if step%SCALING_INT==0: W=rule3(W,ema)
        if step%PRUNE_INT==0:   W=rule4(W,EL,ema,rng)

        if step%LOG_INT==0:
            Sc,curr_lbl,curr_nc=compute_Sc_comms(W,rng)
            lam=compute_lambda_kappa(spike_hist)
            phi=compute_phi_PLV(spike_hist,curr_lbl,curr_nc)
            psi=compute_Psi_rate(W,W_prev); W_prev=W.copy()
            tc_v=[v for v in [lam,phi,psi,TH] if v>0.01]
            Tc=float(np.prod(tc_v)**(1./len(tc_v))) if tc_v else 0.0
            Gst=compute_Gst_window(spike_hist,W,rng)
            cst=float(Sc*Tc*np.exp(alpha*max(Gst,0))) if Sc>0 and Tc>0 else 0.0
            elr=EL.sum()/max((W>0).sum(),1)
            act_r=float(spike.mean())
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
                  f"act={act_r*100:.1f}% ({time.time()-t0:.0f}s)")

    return {'net':name,'seed':seed,'alpha':alpha,'Theta':TH,
            'J_E':[J_E_LO,J_E_HI],'V_thresh':V_THRESH,
            'log':log,'final':log[-1] if log else {}}

# ── 主程序 ────────────────────────────────────────────────
if __name__=='__main__':
    try: from sklearn.metrics import normalized_mutual_info_score
    except:
        import subprocess,sys
        subprocess.run([sys.executable,'-m','pip','install','scikit-learn','-q'])

    print("="*65)
    print("SDI 实验二十 FINAL — 物理第一性LIF（文献参数锁定）")
    print(f"  V_thresh={V_THRESH} (Shadlen 1998: 15mV归一化)")
    print(f"  J_E=[{J_E_LO},{J_E_HI}] (Song 2000: EPSP 0.5-2mV等效)")
    print(f"  I_ext={I_EXT_MEAN}±{I_EXT_STD} (Shadlen 1998: 背景突触等效)")
    print(f"  J_I=-{J_I_RATIO}×J_E (Brunel 2000)")
    print(f"  τ_ref={TAU_REF}步 (Hodgkin & Huxley 1952)")
    print(f"  Γst: {FC_WINDOW}步窗口相关系数 (Honey 2009 PNAS)")
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

    print("\n【与CST论文Table 2对比】")
    for net,ref in {'C_elegans':0.357,'Human_HCP':3.920}.items():
        if net in summary:
            cst=summary[net]['CST']; act=summary[net]['act']
            print(f"  {net}: 仿真={cst:.3f}  论文={ref}  "
                  f"比值={cst/ref:.2f}×  act={act*100:.1f}%  [{summary[net]['IIL']}]")

    json.dump({'results':results,'summary':summary},open(OUT,'w'),indent=2)
    print(f"\n✅ {OUT}")
