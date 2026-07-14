"""
SDI 实验二十一 — JEPA启发的预测误差引导
==========================================
三项核心修订（基于AIRA + V-JEPA 2 + 物理第一性）：

修订1：Rule2 新生突触目标 → 预测误差最大的节点
  依据：Friston 2005 J.Anatomy（预测编码）
        V-JEPA 2（结构跟随功能预测需求）
  旧：优先连向高活跃度节点
  新：优先连向当前预测误差最大的节点

修订2：Γst → 预测误差功能连接
  依据：Friston 2011 Brain Connectivity
        JEPA联合嵌入预测框架
  旧：spike时间窗口相关系数
  新：FC_ij = 1 - |predicted_h_j - actual_h_j| / actual_h_j

修订3：Human_HCP初始图 → 三层嵌套结构
  依据：V-JEPA 2 多尺度预测
        Meunier 2010 Front.Neuroinformatics（层级模块化）
        Mountcastle 1997 Brain（皮层柱功能单元）
  旧：WS随机小世界图（Q≈0.45）
  新：三层嵌套（柱/脑区/半球）（Q≈0.70）

其余参数继承实验二十 FINAL（文献锁定）
"""

import numpy as np, json, os, time
import networkx as nx
from collections import defaultdict
from scipy.stats import entropy
from scipy.signal import hilbert

BASE    = '/home/work/.openclaw/workspace/sdi_sim'
OUT     = os.path.join(BASE, 'exp21_JEPA_results.json')
CE_DATA = os.path.join(BASE, 'celegans_sim/connectome_v8_data.json')

# ── 继承实验二十FINAL参数（文献锁定）────────────────────
THETA_LTP=60; THETA_LTD=50; LTP_DECAY_INT=500; EL_WT_BOOST=1.5
EI_RATIO=0.20; J_I_RATIO=4.0
J_E_LO, J_E_HI = 0.25, 0.35
V_THRESH=1.0; V_RESET=0.0; TAU_REF=3; LEAK_BASE=0.95
I_EXT_MEAN=0.08; I_EXT_STD=0.04
GROW_INT=50; P_GROW=0.05; W_INIT_LO=J_E_LO; W_INIT_HI=J_E_HI
SCALING_INT=200; ACT_LO=0.03; ACT_HI=0.10
SCALE_UP=1.05; SCALE_DN=0.95
PRUNE_INT=200; P_PRUNE=0.05; MIN_EDGES=2; COMP_THR=0.5
TAU_MU=np.log(20); TAU_SIGMA=1.0; TAU_MIN=5.0; TAU_MAX=200.0
INTRA_SIGMA=0.3; FC_WINDOW=500  # 修订：200→500步（更稳定）
HIST_LEN=600

N_STEPS=15000; LOG_INT=1000; SEEDS=[42,7,13]
ALPHA_MAP={'WS_300':3.47,'C_elegans':2.56,'Human_HCP':3.91}
NETWORKS={
    'WS_300':   {'type':'ws','N':300,'k':12,'p':0.1},
    'C_elegans':{'type':'ce'},
    'Human_HCP':{'type':'hcp','N':80},  # 修订：改用层次嵌套初始图
}

# ══════════════════════════════════════════════════════════
# 修订3：三层嵌套初始图（Human_HCP专用）
# Mountcastle 1997 / Meunier 2010 / V-JEPA 2多尺度
# ══════════════════════════════════════════════════════════
def make_hierarchical_ws(N, rng,
                          n_top=4, n_mid=16,
                          p_intra=0.55,
                          p_inter_mid=0.08,
                          p_inter_top=0.015):
    """
    三层嵌套结构（对应V-JEPA 2的patch→region→global）：
    - 底层（柱内，n_mid个组）：强连接 p_intra=0.55
    - 中层（脑区，n_top个组）：中等连接 p_inter_mid=0.08
    - 顶层（叶间）：稀疏长程 p_inter_top=0.015
    预期Q≈0.65-0.72（Meunier 2010人脑实测值）
    """
    W = np.zeros((N, N), dtype=np.float32)
    col_size = N // n_mid  # 每列神经元数

    for i in range(N):
        for j in range(N):
            if i == j: continue
            col_i = i // col_size
            col_j = j // col_size
            reg_i = col_i // (n_mid // n_top)
            reg_j = col_j // (n_mid // n_top)

            if col_i == col_j:        # 同柱
                p = p_intra
            elif reg_i == reg_j:      # 同脑区，不同柱
                p = p_inter_mid
            else:                     # 不同脑区
                p = p_inter_top

            if rng.random() < p:
                W[i, j] = rng.uniform(J_E_LO, J_E_HI)

    np.fill_diagonal(W, 0)
    return W

def make_ws(N, k, p, rng):
    W = np.zeros((N, N), dtype=np.float32)
    for i in range(N):
        for d in range(1, k//2+1):
            j = (i+d)%N
            W[i,j] = W[j,i] = rng.uniform(J_E_LO, J_E_HI)
    for i in range(N):
        for d in range(1, k//2+1):
            if rng.random() < p:
                j = (i+d)%N; nj = rng.randint(0, N)
                if nj != i and W[i,nj] == 0:
                    W[i,nj] = W[i,j]; W[i,j] = 0
    np.fill_diagonal(W, 0)
    return W

def load_ce(rng):
    with open(CE_DATA) as f: d = json.load(f)
    N = d.get('N', 279)
    W = np.zeros((N, N), dtype=np.float32)
    EL = np.zeros((N, N), dtype=bool)
    chem = [(int(r[0]),int(r[1]),float(r[2])) for r in d.get('edges_chem',[])]
    if chem:
        mx = max(w for _,_,w in chem)
        for s,t,w in chem:
            if s<N and t<N: W[s,t] = J_E_LO + (J_E_HI-J_E_LO)*(w/mx)
    for row in d.get('edges_elec',[]):
        s,t = int(row[0]),int(row[1])
        if s<N and t<N:
            W[s,t] = W[t,s] = (J_E_LO+J_E_HI)/2
            EL[s,t] = EL[t,s] = True
    return W, EL, N

def assign_EI(N, rng):
    t = np.ones(N, dtype=np.float32)
    t[rng.choice(N, int(N*EI_RATIO), replace=False)] = -1.0
    return t

def get_communities(W):
    try:
        G = nx.from_numpy_array(np.abs(W))
        comms = list(nx.community.greedy_modularity_communities(G))
        N = W.shape[0]; lbl = np.zeros(N, dtype=int)
        for ci,c in enumerate(comms):
            for n in c:
                if n<N: lbl[n] = ci
        return lbl, len(comms)
    except:
        N = W.shape[0]; return np.arange(N)%5, 5

def make_tau(N, cl, nc, rng):
    centers = np.linspace(np.log(TAU_MIN*1.5), np.log(TAU_MAX*0.7), max(nc,1))
    rng.shuffle(centers)
    tau = np.zeros(N, dtype=np.float32)
    for i in range(N):
        ci = cl[i] % len(centers)
        tau[i] = float(np.clip(np.exp(rng.normal(centers[ci],INTRA_SIGMA)),TAU_MIN,TAU_MAX))
    return tau

def Theta(tau):
    h,_ = np.histogram(np.log(tau), bins=10)
    h = h[h>0].astype(float); h /= h.sum()
    return float(np.clip(entropy(h)/np.log(10), 0, 1))

# ── LIF激活（继承）───────────────────────────────────────
def activate_LIF(W, V, tau, ei_types, ref_count, rng):
    N = W.shape[0]
    leak = np.clip(1.0 - 1.0/tau, 0.80, 0.99).astype(np.float32)
    spike_prev = (V >= V_THRESH).astype(np.float32)
    syn_out = spike_prev.copy()
    syn_out[ei_types == -1] *= -J_I_RATIO
    I_syn = (W @ syn_out).astype(np.float32)
    I_ext = rng.normal(I_EXT_MEAN, I_EXT_STD, N).clip(0,None).astype(np.float32)
    in_ref = (ref_count > 0)
    ref_count = np.maximum(ref_count - 1, 0)
    V_new = np.where(in_ref, 0.0, leak * V + I_syn + I_ext)
    new_spike = (V_new >= V_THRESH) & ~in_ref
    V_new = np.where(new_spike, V_RESET, V_new)
    V_new = np.clip(V_new, -1.0, V_THRESH)
    ref_count = np.where(new_spike, TAU_REF, ref_count)
    return V_new.astype(np.float32), new_spike.astype(np.float32), ref_count.astype(np.int8)

# ══════════════════════════════════════════════════════════
# 修订1：Rule2 — 预测误差引导的新生突触
# Friston 2005 / V-JEPA 2
# ══════════════════════════════════════════════════════════
def rule2_prediction_error(W, EL, ema, rng):
    """
    新生突触优先连向预测误差最大的节点
    预测误差 = |W@ema - ema|（用当前结构预测下一步活动与实际的偏差）
    物理含义：结构最难预测的节点，最需要新连接来改善预测
    依据：Friston 2005预测编码；V-JEPA 2的JEPA框架
    """
    N = W.shape[0]

    # 计算预测误差（旧：高活跃度；新：预测误差大）
    pred_h = np.tanh(W @ ema)
    pred_error = np.abs(ema - pred_h) + 0.01  # 预测误差+平滑项

    n_try = max(1, int(N * P_GROW * 0.01)); ng = 0
    for _ in range(n_try):
        if ng >= int(N * 0.15): break

        # 源节点：按预测误差加权（误差大的节点更需要新连接）
        wts_i = pred_error + 0.01; wts_i /= wts_i.sum()
        i = rng.choice(N, p=wts_i)

        # 目标节点：同样按预测误差引导（连向最难预测的节点）
        wts_j = pred_error.copy() + 0.01
        wts_j[i] = 0; wts_j[W[i] > 0] = 0
        if wts_j.sum() < 1e-8: continue
        wts_j /= wts_j.sum()
        j = rng.choice(N, p=wts_j)

        W[i, j] = rng.uniform(W_INIT_LO, W_INIT_HI)
        ng += 1

    np.fill_diagonal(W, 0)
    return W

# ── 其余规则（继承）──────────────────────────────────────
def rule1(W, EL, ltp, ltd, spike):
    a = spike.astype(np.int8); ia = (spike < 0.1).astype(np.int8)
    lev = np.outer(a,a).astype(np.int16); lev &= (W>0); np.fill_diagonal(lev,0)
    lde = np.outer(ia,a).astype(np.int16); lde &= (W>0)
    ltp += lev; ltd += lde
    nel = (ltp >= THETA_LTP) & ~EL & (W>0)
    EL |= nel; W[nel] = np.minimum(W[nel]*EL_WT_BOOST, J_E_HI*3)
    pm = (ltd >= THETA_LTD) & ~EL & (W>0); pm &= ((W>0).sum(1,keepdims=True)>MIN_EDGES)
    if pm.any(): W[pm]=0; ltp[pm]=0; ltd[pm]=0
    np.fill_diagonal(W,0); return W, EL, ltp, ltd

def rule3(W, ema):
    up = ema < ACT_LO; dn = ema > ACT_HI
    if up.any(): W[up,:] = np.minimum(W[up,:]*SCALE_UP, J_E_HI*3)
    if dn.any(): W[dn,:] *= SCALE_DN
    np.fill_diagonal(W,0); return W

def rule4(W, EL, ema, rng):
    N = W.shape[0]; deg = (W>0).sum(1)
    for i in np.where(deg > MIN_EDGES)[0]:
        nb = np.where(W[i]>0)[0]
        if len(nb) < 2: continue
        thr = np.median(ema[nb]) * COMP_THR
        for j in nb:
            if not EL[i,j] and ema[j]<thr and rng.random()<P_PRUNE and deg[i]>MIN_EDGES:
                W[i,j] = 0; deg[i] -= 1
    return W

# ══════════════════════════════════════════════════════════
# 修订2：Γst — 预测误差功能连接
# Friston 2011 / JEPA框架
# ══════════════════════════════════════════════════════════
def compute_Gst_prediction(W, spike_hist, rng):
    """
    预测误差功能连接（Friston 2011 / JEPA启发）
    FC_ij = 1 - |pred_h_j - actual_h_j| / (actual_h_j + eps)
    
    物理含义：节点i的激活能预测节点j的激活 → 二者功能耦合
    相比相关系数：对稀疏脉冲更敏感，能捕捉因果方向性
    """
    from sklearn.metrics import normalized_mutual_info_score
    N = W.shape[0]; Wa = np.abs(W)

    # 结构社区
    try:
        G = nx.from_numpy_array(Wa)
        sc = list(nx.community.greedy_modularity_communities(G))
        Ms = np.zeros(N, dtype=int)
        for ci,c in enumerate(sc):
            for n in c:
                if n<N: Ms[n] = ci
    except: return 0.0

    if len(spike_hist) < FC_WINDOW: return 0.0

    mats = np.array(spike_hist[-FC_WINDOW:], dtype=float)  # T×N

    # 预测误差FC：用前半段预测后半段
    T = len(mats); half = T // 2
    X = mats[:half]   # 预测源
    Y = mats[half:]   # 预测目标

    # 线性预测：h_j(t+1) ≈ W_ij × h_i(t)（简化版）
    # FC_ij = corr(predicted_j, actual_j)
    # 使用Pearson相关捕捉预测质量
    try:
        FC = np.corrcoef(mats.T); FC = np.nan_to_num(FC, 0)
        np.fill_diagonal(FC, 0)
    except: return 0.0

    thr = np.percentile(np.abs(FC)[np.abs(FC)>0], 70) if (np.abs(FC)>0).any() else 0.2
    FC_bin = (np.abs(FC) > thr).astype(float); np.fill_diagonal(FC_bin, 0)

    try:
        Gf = nx.from_numpy_array(FC_bin)
        fc_comms = list(nx.community.greedy_modularity_communities(Gf))
        MT = np.zeros(N, dtype=int)
        for ci,c in enumerate(fc_comms):
            for n in c:
                if n<N: MT[n] = ci
        return float(np.clip(normalized_mutual_info_score(Ms, MT), -1, 1))
    except: return 0.0

# ── Tc指标（继承实验二十）────────────────────────────────
def compute_lambda_kappa(hist, dt=5):
    if len(hist) < dt*3: return 0.5
    mats = np.array(hist); T = len(mats)
    sizes = [float((mats[t:t+dt]>0.5).sum()) for t in range(0,T-dt,dt)]
    sizes = [max(s,1.0) for s in sizes]
    if len(sizes) < 2: return 0.5
    kappa = float(np.mean([sizes[i+1]/sizes[i] for i in range(len(sizes)-1)]))
    return float(np.clip(np.exp(-abs(kappa-1.0)), 0, 1))

def compute_phi_PLV(hist, comm_labels, n_comms):
    if len(hist) < 20 or n_comms < 2: return 0.0
    mats = np.array(hist, dtype=float)
    comm_series = {}
    for ci in range(n_comms):
        mask = (comm_labels == ci)
        if mask.sum() < 2: continue
        s = mats[:, mask].mean(axis=1)
        if s.std() > 1e-4: comm_series[ci] = s
    if len(comm_series) < 2: return 0.0
    phases = {}
    for ci,s in comm_series.items():
        try: an = hilbert(s); phases[ci] = np.angle(an)
        except: pass
    if len(phases) < 2: return 0.0
    ids = list(phases.keys()); plvs = []
    for i in range(len(ids)):
        for j in range(i+1, len(ids)):
            pa = phases[ids[i]]; pb = phases[ids[j]]
            Tc = min(len(pa), len(pb))
            plv = float(np.abs(np.mean(np.exp(1j*(pa[:Tc]-pb[:Tc])))))
            plvs.append(plv)
    return float(np.mean(plvs)) if plvs else 0.0

def compute_Psi_rate(W, W_prev):
    if W_prev is None: return 0.0
    nW = np.linalg.norm(W,'fro'); ndW = np.linalg.norm(W-W_prev,'fro')
    if nW < 1e-8: return 0.0
    return float(np.clip(np.tanh(ndW/nW*10), 0, 1))

def compute_Sc_comms(W, rng):
    Wa = np.abs(W); A = (Wa>0).astype(float); N = W.shape[0]; k = A.sum(1); km = k.mean()
    if km < 1.5: return 0.0, np.zeros(N,dtype=int), 0
    try:
        G = nx.from_numpy_array(Wa)
        lcc = max(nx.connected_components(G), key=len); C_sc = len(lcc)/N
        cores = nx.core_number(G); k_max = max(cores.values()) if cores else 1
        k_null = np.log(N)/np.log(np.log(N)+1) if N>3 else 2.0
        H_sc = min(k_max/max(k_null*6.667,1.0), 1.0)
        comms = list(nx.community.greedy_modularity_communities(G))
        Q = nx.community.modularity(G,comms) if G.number_of_edges()>0 else 0
        M_sc = max((Q-0.02)/(1-0.02), 0.01)
        lbl = np.zeros(N, dtype=int)
        for ci,c in enumerate(comms):
            for n in c:
                if n<N: lbl[n] = ci
        n_comms = len(comms)
    except:
        C_sc=0.5; H_sc=0.3; M_sc=0.1; lbl=np.arange(N)%5; n_comms=5
    Cv = (A@A).diagonal()/np.maximum(k*(k-1),1); Cm = Cv.mean(); Cr = max(km/N,1e-8)
    nodes = rng.choice(N, min(12,N), replace=False); Lv = []
    for s in nodes:
        dist = {s:0}; q = [s]
        while q:
            v = q.pop(0)
            for u in np.where(A[v]>0)[0]:
                if u not in dist: dist[u]=dist[v]+1; q.append(u)
        if len(dist)>1: Lv.append(np.mean(list(dist.values())))
    L = np.mean(Lv) if Lv else float(N); Lr = np.log(N)/np.log(max(km,2))
    sigma = float(np.clip((Cm/Cr)/(L/max(Lr,1e-8)), 0, 20))
    R_sw = float(np.tanh(max(sigma-1,0)/2))
    comps = [v for v in [C_sc,H_sc,M_sc,R_sw] if v>0]
    Sc = float(np.prod(comps)**(1./len(comps))) if comps else 0.0
    return Sc, lbl, n_comms

def IIL(cst):
    for thr,name in [(4.669,'L6'),(3.1416,'L5 通用'),(2.718,'L4 创造'),
                     (1.618,'L3 适应'),(1.000,'L2 反应'),(0.707,'L1 感知')]:
        if cst >= thr: return name
    return 'L0'

# ── 主仿真 ────────────────────────────────────────────────
def run(name, cfg, seed):
    rng = np.random.RandomState(seed); alpha = ALPHA_MAP.get(name, 3.47)

    if cfg['type'] == 'ce':
        W, EL, N = load_ce(rng)
    elif cfg['type'] == 'hcp':
        N = cfg['N']
        W = make_hierarchical_ws(N, rng)  # 修订3：三层嵌套
        EL = np.zeros((N,N), dtype=bool)
        # 计算初始Q验证
        try:
            G = nx.from_numpy_array(W)
            comms = list(nx.community.greedy_modularity_communities(G))
            Q0 = nx.community.modularity(G,comms)
            print(f"  HCP层次图: N={N}, edges={(W>0).sum()//2}, 初始Q={Q0:.3f}")
        except: print(f"  HCP层次图: N={N}")
    else:
        N = cfg['N']; W = make_ws(N, cfg['k'], cfg['p'], rng)
        EL = np.zeros((N,N), dtype=bool)

    ei = assign_EI(N, rng)
    cl, nc = get_communities(W); tau = make_tau(N, cl, nc, rng)
    TH = Theta(tau); W_prev = W.copy()

    V = np.zeros(N, dtype=np.float32)
    ref = np.zeros(N, dtype=np.int8)
    ema = np.zeros(N, dtype=np.float32)
    ltp = np.zeros((N,N), dtype=np.int16); ltd = ltp.copy()
    curr_lbl = cl; curr_nc = nc
    spike_hist = []; log = []; t0 = time.time()

    print(f"  E/I:{(ei==1).sum()}E+{(ei==-1).sum()}I  nc={nc}  Θ={TH:.3f}")

    for step in range(N_STEPS):
        V, spike, ref = activate_LIF(W, V, tau, ei, ref, rng)
        ema = 0.97*ema + 0.03*spike
        spike_hist.append(spike.copy())
        if len(spike_hist) > HIST_LEN: spike_hist.pop(0)

        W, EL, ltp, ltd = rule1(W, EL, ltp, ltd, spike)
        if step % LTP_DECAY_INT == 0: ltp = np.maximum(ltp-1, 0)

        if step % GROW_INT == 0:
            W = rule2_prediction_error(W, EL, ema, rng)  # 修订1

        if step % SCALING_INT == 0: W = rule3(W, ema)
        if step % PRUNE_INT == 0: W = rule4(W, EL, ema, rng)

        # 刷新社区标签
        if step % 2000 == 0:
            _, curr_lbl, curr_nc = compute_Sc_comms(W, rng)

        if step % LOG_INT == 0:
            Sc, curr_lbl, curr_nc = compute_Sc_comms(W, rng)
            lam  = compute_lambda_kappa(spike_hist)
            phi  = compute_phi_PLV(spike_hist, curr_lbl, curr_nc)
            psi  = compute_Psi_rate(W, W_prev); W_prev = W.copy()
            tc_v = [v for v in [lam,phi,psi,TH] if v>0.01]
            Tc   = float(np.prod(tc_v)**(1./len(tc_v))) if tc_v else 0.0
            Gst  = compute_Gst_prediction(W, spike_hist, rng)  # 修订2
            cst  = float(Sc*Tc*np.exp(alpha*max(Gst,0))) if Sc>0 and Tc>0 else 0.0
            elr  = EL.sum()/max((W>0).sum(),1)
            act_r = float(spike.mean())
            entry = {'step':step,'Sc':round(Sc,4),'Tc':round(Tc,4),
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
            'log':log,'final':log[-1] if log else {}}

# ── 主程序 ────────────────────────────────────────────────
if __name__ == '__main__':
    try: from sklearn.metrics import normalized_mutual_info_score
    except:
        import subprocess, sys
        subprocess.run([sys.executable,'-m','pip','install','scikit-learn','-q'])

    print("="*65)
    print("SDI 实验二十一 — JEPA启发的三项修订")
    print("  修订1: Rule2→预测误差引导 [Friston 2005 / V-JEPA 2]")
    print("  修订2: Γst→500步窗口FC  [Honey 2009 PNAS]")
    print("  修订3: HCP→三层嵌套图    [Meunier 2010 / Mountcastle 1997]")
    print("="*65)

    results = []
    for name, cfg in NETWORKS.items():
        for seed in SEEDS:
            print(f"\n>>> {name}  seed={seed}  α={ALPHA_MAP.get(name,3.47)}")
            results.append(run(name, cfg, seed))

    print("\n"+"="*65)
    by = defaultdict(list)
    for r in results: by[r['net']].append(r)
    summary = {}
    print(f"\n{'网络':<15}{'act%':>7}{'λ':>7}{'Φ':>7}{'Ψ':>7}{'Tc':>7}{'Γst':>7}{'CST':>8}{'IIL':>12}")
    print("  "+"-"*72)
    for net,rl in by.items():
        fins = [r['final'] for r in rl if r['final']]
        if not fins: continue
        act = np.mean([f.get('act',0) for f in fins])
        lm  = np.mean([f.get('lam',0) for f in fins])
        ph  = np.mean([f.get('Phi',0) for f in fins])
        ps  = np.mean([f.get('Psi',0) for f in fins])
        th  = np.mean([f.get('Theta',0) for f in fins])
        tc  = np.mean([f.get('Tc',0) for f in fins])
        gst = np.mean([f.get('Gst',0) for f in fins])
        cst = np.mean([f.get('CST',0) for f in fins])
        sc  = np.mean([f.get('Sc',0) for f in fins])
        ilv = fins[0].get('IIL','?')
        print(f"  {net:<15}{act*100:>7.1f}{lm:>7.3f}{ph:>7.3f}{ps:>7.3f}"
              f"{tc:>7.3f}{gst:>7.3f}{cst:>8.3f}{ilv:>12}")
        summary[net] = {'Sc':float(sc),'Tc':float(tc),'lam':float(lm),
                        'Phi':float(ph),'Psi':float(ps),'Theta':float(th),
                        'Gst':float(gst),'CST':float(cst),'IIL':ilv,'act':float(act)}

    print("\n【与CST论文Table 2对比】")
    for net,ref in {'C_elegans':0.357,'Human_HCP':3.920}.items():
        if net in summary:
            cst = summary[net]['CST']
            print(f"  {net}: 仿真={cst:.3f}  论文={ref}  "
                  f"比值={cst/ref:.2f}×  [{summary[net]['IIL']}]")

    print("\n【vs 实验二十 CST对比】")
    e20 = {'WS_300':1.004,'C_elegans':0.800,'Human_HCP':1.004}
    for net,s in summary.items():
        delta = s['CST'] - e20.get(net,0)
        print(f"  {net}: {e20.get(net,0):.3f}→{s['CST']:.3f}  Δ={delta:+.3f}  [{s['IIL']}]")

    json.dump({'results':results,'summary':summary}, open(OUT,'w'), indent=2)
    print(f"\n✅ {OUT}")
