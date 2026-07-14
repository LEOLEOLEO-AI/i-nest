"""
SDI 实验九 — 时间复杂度Tc四分量 + Γst动态耦合测量
======================================================
验证目标：
  1. Tc四分量（λ_eff / Φ / Ψ / Θ）随SDI四规则演化的变化轨迹
  2. Γst = NMI(Ms, MT) 从初始→演化后的提升
  3. 完整CST数值：CST = (Sc·Tc)·exp(α·Γst)，与论文Table2对比
  4. EL键比例 vs Γst 相关性（EL固化=结构功能耦合加深）

物种：C.elegans（N=279）+ WS_300 + Human_HCP（N=80）
参数：v5文献锁定参数集
"""

import numpy as np, json, os, time
import networkx as nx
from collections import defaultdict
from scipy.stats import entropy

BASE = '/home/work/.openclaw/workspace/sdi_sim'
OUT  = os.path.join(BASE, 'exp9_Tc_Gamma_results.json')
CE_DATA = os.path.join(BASE, 'celegans_sim/connectome_v8_data.json')

# ── v5 文献锁定参数 ─────────────────────────────────────
THETA_LTP=60; THETA_LTD=50; LTP_DECAY_INT=500; EL_WT_BOOST=1.5
GROW_INT=50;  P_GROW=0.05; W_INIT_LO=0.05; W_INIT_HI=0.10
SCALING_INT=200; ACT_LO=0.03; ACT_HI=0.10
SCALE_UP=1.05; SCALE_DN=0.95
PRUNE_INT=200; P_PRUNE=0.05; MIN_EDGES=2; COMP_THR=0.5

N_STEPS  = 8000
LOG_INT  = 1000   # 每1000步记录完整Tc+Γst
SEEDS    = [42, 7, 13]

# α值（CST计算用）
ALPHA_MAP = {
    'WS_300':    3.47,   # spiking神经元（Loihi-2级别）
    'C_elegans': 2.56,   # 分级电位（线虫graded-potential）
    'Human_HCP': 3.91,   # 人类皮层（cortical STDP+多频振荡）
}

NETWORKS = {
    'WS_300':    {'type':'ws', 'N':300, 'k':12, 'p':0.1},
    'C_elegans': {'type':'ce'},
    'Human_HCP': {'type':'ws', 'N':80,  'k':8,  'p':0.1},
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

# ── 激活 ──────────────────────────────────────────────────
def activate(W,rng,frac=0.12,nstep=4):
    N=W.shape[0]; n=max(4,int(N*frac))
    h=np.zeros(N,dtype=np.float32)
    h[rng.choice(N,n,replace=False)]=rng.uniform(0.5,1.0,n)
    for _ in range(nstep):
        h=np.tanh(W@h)
        if h.max()>0:
            thr=np.percentile(h[h>0.05],70) if (h>0.05).sum()>5 else 0.05
            h[h<thr]=0
    return h.astype(np.float32)

# ── v5四规则 ──────────────────────────────────────────────
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
        wi=ema+0.01; wi/=wi.sum()
        i=rng.choice(N,p=wi)
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
# Tc 四分量计算
# ══════════════════════════════════════════════════════════

def compute_lambda_eff(act_history):
    """
    λ_eff：神经雪崩分支比
    方法：Beggs & Plenz 2003 — 连续激活步的传播比
    λ = mean(激活t+1的节点数 / 激活t的节点数)，取对数尺度
    归一化到[0,1]：λ_norm = tanh(λ_eff)，λ_eff≈1→λ_norm≈0.76
    """
    if len(act_history) < 2: return 0.0
    ratios = []
    for t in range(len(act_history)-1):
        n_t  = (act_history[t]   > 0.1).sum()
        n_t1 = (act_history[t+1] > 0.1).sum()
        if n_t > 0:
            ratios.append(n_t1 / n_t)
    if not ratios: return 0.0
    lam = float(np.mean(ratios))
    # 归一化：临界态λ=1对应最高信息传递效率
    # 使用 1 - |λ-1|/(λ+1) 映射到[0,1]
    return float(np.clip(1.0 - abs(lam-1.0)/(lam+1.0+1e-8), 0, 1))

def compute_Phi(act_history):
    """
    Φ：相位同步（Kuramoto序参数）
    方法：对每个时间点，计算活跃节点的相位一致性
    简化：用激活向量的余弦相似度均值近似
    归一化到[0,1]
    """
    if len(act_history) < 4: return 0.0
    mats = np.array(act_history)  # T×N
    # 计算相邻时间步的相关性
    corrs = []
    for t in range(len(mats)-1):
        a, b = mats[t], mats[t+1]
        na, nb = np.linalg.norm(a), np.linalg.norm(b)
        if na > 1e-8 and nb > 1e-8:
            corrs.append(float(np.dot(a,b)/(na*nb)))
    return float(np.clip(np.mean(corrs) if corrs else 0.0, 0, 1))

def compute_Psi(W_history, W_init):
    """
    Ψ：功能连接时变性（突触可塑性）
    方法：权重矩阵随时间变化的程度
    = 1 - corr(W_final, W_init)，变化越大Ψ越高
    归一化到[0,1]
    """
    if W_history is None or W_init is None: return 0.0
    w0 = W_init.flatten()
    wf = W_history.flatten()
    if w0.std() < 1e-8 or wf.std() < 1e-8: return 0.0
    corr = float(np.corrcoef(w0, wf)[0,1])
    return float(np.clip((1.0 - corr) / 2.0, 0, 1))

def compute_Theta(act_history, N):
    """
    Θ：时间尺度多样性
    方法：对每个节点，计算其激活序列的自相关时间常数τ_i
    Θ = Shannon熵（τ_i分布），归一化到[0,1]
    """
    if len(act_history) < 10: return 0.0
    mats = np.array(act_history)  # T×N
    taus = []
    for i in range(min(N, 50)):  # 采样50个节点
        series = mats[:, i]
        if series.std() < 1e-8: continue
        # 自相关：找到首次低于1/e的lag
        ac = np.correlate(series - series.mean(),
                         series - series.mean(), mode='full')
        ac = ac[len(ac)//2:]
        ac = ac / (ac[0] + 1e-8)
        tau = next((t for t, v in enumerate(ac) if v < 1/np.e), len(ac))
        taus.append(tau)
    if not taus: return 0.0
    # Shannon熵（τ分布）
    hist, _ = np.histogram(taus, bins=min(10, len(set(taus))))
    hist = hist[hist > 0].astype(float)
    hist /= hist.sum()
    ent = float(entropy(hist))
    max_ent = float(np.log(len(hist)) + 1e-8)
    return float(np.clip(ent / max_ent, 0, 1))

def compute_Tc(lam, phi, psi, theta):
    """Tc = 几何平均（四分量归一化后）"""
    vals = [v for v in [lam, phi, psi, theta] if v > 0]
    if not vals: return 0.0
    return float(np.prod(vals) ** (1.0/len(vals)))

# ══════════════════════════════════════════════════════════
# Γst 计算：NMI(结构社区, 功能社区)
# ══════════════════════════════════════════════════════════

def compute_Gamma_st(W, act_history):
    """
    Γst = NMI(Ms, MT)
    Ms：结构社区（Louvain，基于权重矩阵W）
    MT：功能社区（激活模式聚类）
    """
    N = W.shape[0]
    # 结构社区
    try:
        G = nx.from_numpy_array(W)
        struct_comms = list(nx.community.greedy_modularity_communities(G))
        Ms = np.zeros(N, dtype=int)
        for ci, c in enumerate(struct_comms):
            for n in c:
                if n < N: Ms[n] = ci
    except:
        return 0.0

    # 功能社区：对激活矩阵做相关性聚类
    if len(act_history) < 5: return 0.0
    mats = np.array(act_history)  # T×N
    # 计算节点间激活相关矩阵
    corr_mat = np.corrcoef(mats.T)  # N×N
    corr_mat = np.nan_to_num(corr_mat, 0)
    # 用阈值化图做社区检测
    threshold = np.percentile(corr_mat[corr_mat > 0], 70)
    FC = (corr_mat > threshold).astype(float)
    np.fill_diagonal(FC, 0)
    try:
        Gf = nx.from_numpy_array(FC)
        func_comms = list(nx.community.greedy_modularity_communities(Gf))
        MT = np.zeros(N, dtype=int)
        for ci, c in enumerate(func_comms):
            for n in c:
                if n < N: MT[n] = ci
    except:
        return 0.0

    # NMI计算
    from sklearn.metrics import normalized_mutual_info_score
    try:
        nmi = float(normalized_mutual_info_score(Ms, MT))
    except:
        nmi = 0.0

    # Mantel test符号：结构距离 vs 功能距离是否同向
    # 简化：用结构Q和功能Q的差异方向
    Qs = nx.community.modularity(G, struct_comms) if G.number_of_edges()>0 else 0
    Qf = nx.community.modularity(Gf, func_comms) if Gf.number_of_edges()>0 else 0
    sign = 1.0 if Qs > 0 and Qf > 0 else -1.0

    return float(np.clip(nmi * sign, -1, 1))

# ══════════════════════════════════════════════════════════
# Sc 计算
# ══════════════════════════════════════════════════════════

def compute_Sc(W, rng):
    A=(W>0).astype(float); N=W.shape[0]; k=A.sum(1); km=k.mean()
    if km<1.5: return 0.0, {}

    # C（全局连通性）
    try:
        G=nx.from_numpy_array(W)
        lcc=max(nx.connected_components(G),key=len)
        C_sc=len(lcc)/N
    except: C_sc=0.0

    # H（k-core层级）
    try:
        cores=nx.core_number(nx.from_numpy_array(W))
        k_max=max(cores.values()) if cores else 1
        k_null=np.log(N)/np.log(np.log(N)+1) if N>3 else 2.0
        H_sc=min(k_max/max(k_null*6.667,1.0),1.0)
    except: H_sc=0.0

    # M（模块化）
    try:
        comms=list(nx.community.greedy_modularity_communities(G))
        Q=nx.community.modularity(G,comms) if G.number_of_edges()>0 else 0
        M_sc=max((Q-0.02)/(1-0.02),0.01)
    except: M_sc=0.01

    # R_sw（小世界）
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
    return Sc, {'C':C_sc,'H':H_sc,'M':M_sc,'R_sw':R_sw,'sigma':sigma}

# ══════════════════════════════════════════════════════════
# 完整CST计算
# ══════════════════════════════════════════════════════════

def compute_CST(Sc, Tc, alpha, Gamma_st):
    if Sc<=0 or Tc<=0: return 0.0
    return float(Sc * Tc * np.exp(alpha * max(Gamma_st, 0)))

def IIL_level(cst):
    thresholds = [(4.669,'L6 超级'),(3.1416,'L5 通用'),(2.718,'L4 创造'),
                  (1.618,'L3 适应'),(1.000,'L2 反应'),(0.707,'L1 感知'),(0,'L0')]
    for thr, name in thresholds:
        if cst >= thr: return name
    return 'L0'

# ══════════════════════════════════════════════════════════
# 主仿真
# ══════════════════════════════════════════════════════════

def run(name, cfg, seed):
    rng = np.random.RandomState(seed)
    alpha = ALPHA_MAP.get(name, 3.47)

    if cfg['type']=='ce':
        W,EL,N=load_ce(rng); frac=0.15
    else:
        N=cfg['N']; W=make_ws(N,cfg['k'],cfg['p'],rng)
        EL=np.zeros((N,N),dtype=bool); frac=0.12

    W_init = W.copy()
    ltp=np.zeros((N,N),dtype=np.int16); ltd=ltp.copy()
    ema=np.zeros(N,dtype=np.float32)

    # 滑动窗口：记录最近50步的激活历史（用于Tc计算）
    act_window = []
    log = []
    t0 = time.time()

    for step in range(N_STEPS):
        act = activate(W, rng, frac=frac)
        ema = 0.97*ema + 0.03*act
        act_window.append(act.copy())
        if len(act_window) > 50: act_window.pop(0)

        W,EL,ltp,ltd = rule1(W,EL,ltp,ltd,act)
        if step%LTP_DECAY_INT==0: ltp=np.maximum(ltp-1,0)
        if step%GROW_INT==0:    W=rule2(W,EL,ema,rng)
        if step%SCALING_INT==0: W=rule3(W,ema)
        if step%PRUNE_INT==0:   W=rule4(W,EL,ema,rng)

        # 记录完整指标
        if step % LOG_INT == 0:
            Sc, Sc_comps = compute_Sc(W, rng)

            # Tc四分量
            lam  = compute_lambda_eff(act_window)
            phi  = compute_Phi(act_window)
            psi  = compute_Psi(W, W_init)
            theta= compute_Theta(act_window, N)
            Tc   = compute_Tc(lam, phi, psi, theta)

            # Γst
            Gst  = compute_Gamma_st(W, act_window)

            # 完整CST
            cst  = compute_CST(Sc, Tc, alpha, Gst)
            ilevel = IIL_level(cst)

            el_r = EL.sum()/max((W>0).sum(),1)

            entry = {
                'step': step,
                'Sc': round(Sc,4), 'Sc_comps': {k:round(v,4) for k,v in Sc_comps.items()},
                'Tc': round(Tc,4),
                'lambda_eff': round(lam,4),
                'Phi': round(phi,4),
                'Psi': round(psi,4),
                'Theta': round(theta,4),
                'Gamma_st': round(Gst,4),
                'CST': round(cst,4),
                'IIL': ilevel,
                'EL_ratio': round(float(el_r),4),
                'alpha': alpha,
            }
            log.append(entry)
            print(f"  {name} s={seed} t={step:5d}: "
                  f"Sc={Sc:.3f} Tc={Tc:.3f} Γst={Gst:.3f} "
                  f"CST={cst:.3f} [{ilevel}] "
                  f"λ={lam:.3f} Φ={phi:.3f} Ψ={psi:.3f} Θ={theta:.3f} "
                  f"({time.time()-t0:.0f}s)")

    final = log[-1] if log else {}
    return {'net': name, 'seed': seed, 'alpha': alpha, 'log': log, 'final': final}


# ══════════════════════════════════════════════════════════
# 主程序
# ══════════════════════════════════════════════════════════

if __name__ == '__main__':
    # sklearn检查
    try:
        from sklearn.metrics import normalized_mutual_info_score
    except ImportError:
        import subprocess, sys
        subprocess.run([sys.executable,'-m','pip','install','scikit-learn','-q'])
        from sklearn.metrics import normalized_mutual_info_score

    print("="*70)
    print("SDI 实验九 — Tc四分量 + Γst动态耦合 + 完整CST数值")
    print("  验证：CST = (Sc·Tc)·exp(α·Γst) 全三分量自洽性")
    print("="*70)

    results = []
    for name, cfg in NETWORKS.items():
        for seed in SEEDS:
            print(f"\n>>> {name}  seed={seed}  α={ALPHA_MAP.get(name,3.47)}")
            results.append(run(name, cfg, seed))

    # 汇总
    print("\n"+"="*70)
    by = defaultdict(list)
    for r in results: by[r['net']].append(r)

    print(f"\n{'网络':<15} {'Sc':>6} {'Tc':>6} {'Γst':>6} "
          f"{'CST':>7} {'IIL':>10} {'EL%':>5}")
    print("  "+"-"*60)

    summary = {}
    for net, rl in by.items():
        finals = [r['final'] for r in rl if r['final']]
        if not finals: continue
        sc  = np.mean([f.get('Sc',0)        for f in finals])
        tc  = np.mean([f.get('Tc',0)        for f in finals])
        gst = np.mean([f.get('Gamma_st',0)  for f in finals])
        cst = np.mean([f.get('CST',0)       for f in finals])
        elr = np.mean([f.get('EL_ratio',0)  for f in finals])
        ilv = finals[0].get('IIL','?') if finals else '?'
        print(f"  {net:<15} {sc:>6.3f} {tc:>6.3f} {gst:>6.3f} "
              f"{cst:>7.3f} {ilv:>10} {elr*100:>5.1f}%")
        summary[net] = {'Sc':float(sc),'Tc':float(tc),'Gamma_st':float(gst),
                        'CST':float(cst),'IIL':ilv,'EL_ratio':float(elr)}

    # 与论文Table2对比
    print("\n【与CST论文Table 2对比】")
    REF = {
        'C_elegans':  {'CST_paper':0.357, 'IIL_paper':'L1'},
        'Human_HCP':  {'CST_paper':3.920, 'IIL_paper':'L5'},
    }
    for net, ref in REF.items():
        if net in summary:
            cst_sim = summary[net]['CST']
            cst_paper = ref['CST_paper']
            ratio = cst_sim / max(cst_paper, 1e-8)
            print(f"  {net}: 仿真CST={cst_sim:.3f}  论文CST={cst_paper}  比值={ratio:.2f}×")

    # Γst趋势
    print("\n【Γst演化趋势（初始→终态）】")
    for net, rl in by.items():
        logs = rl[0]['log']
        if len(logs) >= 2:
            g0 = logs[0]['Gamma_st']
            gf = logs[-1]['Gamma_st']
            print(f"  {net}: Γst {g0:.3f} → {gf:.3f}  "
                  f"{'↑提升' if gf>g0 else '↓下降'} Δ={gf-g0:+.3f}")

    json.dump({'results':results,'summary':summary},
              open(OUT,'w'),indent=2)
    print(f"\n✅ 结果保存: {OUT}")
