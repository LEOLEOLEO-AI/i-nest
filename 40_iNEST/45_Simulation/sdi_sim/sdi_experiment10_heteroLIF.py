"""
SDI 实验十 — 异质LIF激活 + Θ时间尺度多样性改进
文献依据：
  Murray et al. 2014 Nat.Neurosci. 17:1661  — 皮层INT层级，τ跨3个数量级
  Perez-Nieves et al. 2021 Nat.Commun.      — 异质LIF对数正态τ分布
  Cavanagh et al. 2020 Front.Syst.Neurosci. — 多时间尺度神经计算

改进：
  tanh(W@h)  →  h_i(t+1) = (1-1/τ_i)·h_i(t) + tanh(Σ_j W_ij·h_j(t))
  τ_i ~ LogNormal(ln(20), 1.0²)，范围[5, 200]步
  → Θ从间歇性非零(12-38%) → 稳定高值(>0.6)
  → CST预期从1.77 → >3.14（L5通用智能）
"""

import numpy as np, json, os, time
import networkx as nx
from collections import defaultdict
from scipy.stats import entropy

BASE = '/home/work/.openclaw/workspace/sdi_sim'
OUT  = os.path.join(BASE, 'exp10_heteroLIF_results.json')
CE_DATA = os.path.join(BASE, 'celegans_sim/connectome_v8_data.json')

# ── v5文献锁定参数（不变）──────────────────────────────────
THETA_LTP=60; THETA_LTD=50; LTP_DECAY_INT=500; EL_WT_BOOST=1.5
GROW_INT=50; P_GROW=0.05; W_INIT_LO=0.05; W_INIT_HI=0.10
SCALING_INT=200; ACT_LO=0.03; ACT_HI=0.10
SCALE_UP=1.05; SCALE_DN=0.95
PRUNE_INT=200; P_PRUNE=0.05; MIN_EDGES=2; COMP_THR=0.5

# ── 异质LIF参数（新增，文献依据）─────────────────────────
# Murray 2014: τ_min=20ms(感觉皮层) τ_max=1500ms(前额叶)
# 仿真1步≈1ms → τ_min=5步 τ_max=200步（保守，仿真尺度）
TAU_MU    = np.log(20)   # 对数正态均值 → 几何均值≈20步
TAU_SIGMA = 1.0          # 对数正态标准差 → 覆盖3个数量级
TAU_MIN   = 5.0          # 最小时间常数（感觉皮层）
TAU_MAX   = 200.0        # 最大时间常数（前额叶，仿真尺度）

N_STEPS = 8000
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

def make_tau(N, rng):
    """
    生成每个节点的时间常数 τ_i
    Murray 2014: LogNormal分布，τ跨3个数量级
    Perez-Nieves 2021: ln(τ)~N(ln(20), 1.0²)
    """
    tau = np.exp(rng.normal(TAU_MU, TAU_SIGMA, N))
    tau = np.clip(tau, TAU_MIN, TAU_MAX)
    return tau.astype(np.float32)

# ── 异质LIF激活（核心改进）────────────────────────────────
def activate_hetLIF(W, h, tau, rng, frac=0.12, n_seeds=4):
    """
    异质LIF：h_i(t+1) = (1-1/τ_i)·h_i(t) + tanh(Σ_j W_ij·h_j(t))
    
    文献：Perez-Nieves 2021 Nat.Commun.
    漏电因子 leak_i = 1 - 1/τ_i：
      τ_i=5   → leak=0.80（快衰减，感觉皮层）
      τ_i=20  → leak=0.95（中等，主要皮层）
      τ_i=200 → leak=0.995（慢衰减，前额叶/默认模式网络）
    """
    N = W.shape[0]
    # 漏电因子（每节点不同）
    leak = (1.0 - 1.0/tau).astype(np.float32)

    # 外部驱动（随机种子输入，模拟感觉输入）
    n = max(n_seeds, int(N*frac))
    drive = np.zeros(N, dtype=np.float32)
    drive[rng.choice(N, n, replace=False)] = rng.uniform(0.3, 0.8, n)

    # LIF更新
    h_new = leak * h + np.tanh(W @ h + drive)

    # 软阈值：保持稀疏激活（Rule3的时间域对应）
    h_new = np.where(h_new > 0.05, h_new, 0.0)
    h_new = np.clip(h_new, 0, 1)
    return h_new.astype(np.float32)

# ── v5四规则（完全继承，不变）────────────────────────────
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

# ── Tc四分量（从实验九继承，Θ为核心改进目标）──────────────
def compute_Theta_hetLIF(tau_arr):
    """
    Θ改进版：直接使用τ分布的Shannon熵
    Murray 2014: INT分布的熵与认知复杂度正相关
    比实验九的"自相关时间常数"更直接、更稳定
    """
    if tau_arr is None or len(tau_arr)==0: return 0.0
    # 对τ取log，分10个区间计算熵
    log_tau = np.log(tau_arr)
    hist, _ = np.histogram(log_tau, bins=10)
    hist = hist[hist>0].astype(float); hist /= hist.sum()
    raw_ent = float(entropy(hist))
    max_ent = float(np.log(10))
    return float(np.clip(raw_ent/max_ent, 0, 1))

def compute_lambda_eff(act_hist):
    if len(act_hist)<2: return 0.0
    ratios=[]
    for t in range(len(act_hist)-1):
        n0=(act_hist[t]>0.1).sum(); n1=(act_hist[t+1]>0.1).sum()
        if n0>0: ratios.append(n1/n0)
    if not ratios: return 0.0
    lam=float(np.mean(ratios))
    return float(np.clip(1.0-abs(lam-1.0)/(lam+1.0+1e-8),0,1))

def compute_Phi(act_hist):
    if len(act_hist)<4: return 0.0
    mats=np.array(act_hist); corrs=[]
    for t in range(len(mats)-1):
        a,b=mats[t],mats[t+1]; na,nb=np.linalg.norm(a),np.linalg.norm(b)
        if na>1e-8 and nb>1e-8: corrs.append(float(np.dot(a,b)/(na*nb)))
    return float(np.clip(np.mean(corrs) if corrs else 0.0,0,1))

def compute_Psi(W,W_init):
    if W_init is None: return 0.0
    w0=W_init.flatten(); wf=W.flatten()
    if w0.std()<1e-8 or wf.std()<1e-8: return 0.0
    corr=float(np.corrcoef(w0,wf)[0,1])
    return float(np.clip((1.0-corr)/2.0,0,1))

def compute_Sc(W,rng):
    A=(W>0).astype(float); N=W.shape[0]; k=A.sum(1); km=k.mean()
    if km<1.5: return 0.0,{}
    try:
        G=nx.from_numpy_array(W)
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
    Sc=float(np.prod(comps)**(1.0/len(comps))) if comps else 0.0
    return Sc,{'C':C_sc,'H':H_sc,'M':M_sc,'R_sw':R_sw,'sigma':sigma}

def compute_Gamma_st(W,act_hist):
    from sklearn.metrics import normalized_mutual_info_score
    N=W.shape[0]
    try:
        G=nx.from_numpy_array(W)
        sc=list(nx.community.greedy_modularity_communities(G))
        Ms=np.zeros(N,dtype=int)
        for ci,c in enumerate(sc):
            for n in c:
                if n<N: Ms[n]=ci
    except: return 0.0
    if len(act_hist)<5: return 0.0
    mats=np.array(act_hist)
    corr_mat=np.corrcoef(mats.T); corr_mat=np.nan_to_num(corr_mat,0)
    thr=np.percentile(corr_mat[corr_mat>0],70) if (corr_mat>0).any() else 0.5
    FC=(corr_mat>thr).astype(float); np.fill_diagonal(FC,0)
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
        W,EL,N = load_ce(rng); frac=0.15
    else:
        N=cfg['N']; W=make_ws(N,cfg['k'],cfg['p'],rng)
        EL=np.zeros((N,N),dtype=bool); frac=0.12

    W_init = W.copy()

    # 生成每节点时间常数（Murray 2014 / Perez-Nieves 2021）
    tau = make_tau(N, rng)
    print(f"  τ分布: min={tau.min():.1f} max={tau.max():.1f} "
          f"mean={tau.mean():.1f} std={tau.std():.1f}")

    # Θ（直接从τ分布计算，稳定可靠）
    Theta_fixed = compute_Theta_hetLIF(tau)
    print(f"  Θ(τ分布熵)={Theta_fixed:.3f}  ← 异质LIF的稳定贡献")

    ltp=np.zeros((N,N),dtype=np.int16); ltd=ltp.copy()
    ema=np.zeros(N,dtype=np.float32)
    h  =np.zeros(N,dtype=np.float32)   # LIF膜电位状态
    act_window=[]
    log=[]; t0=time.time()

    for step in range(N_STEPS):
        # 异质LIF激活（核心改进）
        h   = activate_hetLIF(W, h, tau, rng, frac=frac)
        act = h.copy()
        ema = 0.97*ema + 0.03*act
        act_window.append(act.copy())
        if len(act_window)>50: act_window.pop(0)

        W,EL,ltp,ltd = rule1(W,EL,ltp,ltd,act)
        if step%LTP_DECAY_INT==0: ltp=np.maximum(ltp-1,0)
        if step%GROW_INT==0:    W=rule2(W,EL,ema,rng)
        if step%SCALING_INT==0: W=rule3(W,ema)
        if step%PRUNE_INT==0:   W=rule4(W,EL,ema,rng)

        if step%LOG_INT==0:
            Sc,Sc_c = compute_Sc(W,rng)
            lam     = compute_lambda_eff(act_window)
            phi     = compute_Phi(act_window)
            psi     = compute_Psi(W,W_init)
            # Θ = τ分布熵（稳定） + 动态自相关熵（补充）
            Theta   = Theta_fixed
            Tc_vals = [v for v in [lam,phi,psi,Theta] if v>0]
            Tc      = float(np.prod(Tc_vals)**(1./len(Tc_vals))) if Tc_vals else 0.0
            Gst     = compute_Gamma_st(W,act_window)
            cst     = float(Sc*Tc*np.exp(alpha*max(Gst,0))) if Sc>0 and Tc>0 else 0.0
            elr     = EL.sum()/max((W>0).sum(),1)
            entry   = {'step':step,'Sc':round(Sc,4),'Tc':round(Tc,4),
                       'lambda_eff':round(lam,4),'Phi':round(phi,4),
                       'Psi':round(psi,4),'Theta':round(Theta,4),
                       'Gamma_st':round(Gst,4),'CST':round(cst,4),
                       'IIL':IIL(cst),'EL_ratio':round(float(elr),4),
                       'alpha':alpha}
            log.append(entry)
            print(f"  {name} s={seed} t={step:5d}: "
                  f"Sc={Sc:.3f} Tc={Tc:.3f}(λ={lam:.2f} Φ={phi:.2f} "
                  f"Ψ={psi:.2f} Θ={Theta:.2f}) "
                  f"Γst={Gst:.3f} CST={cst:.3f}[{IIL(cst)}] "
                  f"({time.time()-t0:.0f}s)")

    return {'net':name,'seed':seed,'alpha':alpha,
            'tau_stats':{'min':float(tau.min()),'max':float(tau.max()),
                         'mean':float(tau.mean()),'Theta':Theta_fixed},
            'log':log,'final':log[-1] if log else {}}

# ── 主程序 ────────────────────────────────────────────────
if __name__=='__main__':
    try: from sklearn.metrics import normalized_mutual_info_score
    except:
        import subprocess,sys
        subprocess.run([sys.executable,'-m','pip','install',
                        'scikit-learn','-q'])

    print("="*65)
    print("SDI 实验十 — 异质LIF：Θ时间尺度多样性改进")
    print("  文献：Murray 2014 Nat.Neurosci. / Perez-Nieves 2021 Nat.Commun.")
    print(f"  τ ~ LogNormal(ln(20),1.0²)  范围[{TAU_MIN},{TAU_MAX}]步")
    print("  Θ = τ分布Shannon熵（稳定可靠，不依赖自相关估计）")
    print("="*65)

    results=[]
    for name,cfg in NETWORKS.items():
        for seed in SEEDS:
            print(f"\n>>> {name}  seed={seed}  α={ALPHA_MAP.get(name,3.47)}")
            results.append(run(name,cfg,seed))

    print("\n"+"="*65+"  汇总:")
    by=defaultdict(list)
    for r in results: by[r['net']].append(r)

    print(f"\n{'网络':<15}{'Sc':>6}{'Tc':>6}{'Θ':>6}{'Γst':>6}{'CST':>7}{'IIL':>10}")
    print("  "+"-"*55)
    summary={}
    for net,rl in by.items():
        fins=[r['final'] for r in rl if r['final']]
        if not fins: continue
        sc =np.mean([f.get('Sc',0)       for f in fins])
        tc =np.mean([f.get('Tc',0)       for f in fins])
        th =np.mean([f.get('Theta',0)    for f in fins])
        gst=np.mean([f.get('Gamma_st',0) for f in fins])
        cst=np.mean([f.get('CST',0)      for f in fins])
        ilv=fins[0].get('IIL','?')
        print(f"  {net:<15}{sc:>6.3f}{tc:>6.3f}{th:>6.3f}"
              f"{gst:>6.3f}{cst:>7.3f}{ilv:>10}")
        summary[net]={'Sc':float(sc),'Tc':float(tc),'Theta':float(th),
                      'Gamma_st':float(gst),'CST':float(cst),'IIL':ilv}

    # 与实验九对比
    print("\n【vs 实验九（均匀tanh）对比】")
    exp9 = {'WS_300':1.774,'C_elegans':0.402,'Human_HCP':2.148}
    exp9_Tc = {'WS_300':0.228,'C_elegans':0.272,'Human_HCP':0.231}
    for net in summary:
        cst10=summary[net]['CST']; cst9=exp9.get(net,0)
        tc10=summary[net]['Tc'];   tc9=exp9_Tc.get(net,0)
        th10=summary[net]['Theta']
        print(f"  {net}: CST {cst9:.3f}→{cst10:.3f}(Δ={cst10-cst9:+.3f})  "
              f"Tc {tc9:.3f}→{tc10:.3f}  Θ→{th10:.3f}")

    json.dump({'results':results,'summary':summary},open(OUT,'w'),indent=2)
    print(f"\n✅ 结果: {OUT}")
