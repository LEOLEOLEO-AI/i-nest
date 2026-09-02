#!/usr/bin/env python3
"""
v34_p3b_lif_stdp.py — P3-B v2：LIF + STDP，τ 多样性从物理机制涌现

改进（相对 v34_p3b_lif.py v1）：
  加入 STDP 突触可塑性（Bi & Poo 1998），让权重异质化
  → 不同路径信号传播速度分化 → τ 分布展宽 → Θ 提升

所有参数来源（S1/S2）：
  LIF τ_m:    Bhatt 2022, Nat.Commun. 13:5104, DOI:10.1038/s41467-022-28971-9
  STDP:       Bi & Poo 1998, J.Neurosci. 18:10464, DOI:10.1523/JNEUROSCI.18-24-10464.1998
              η_LTP=0.010, η_LTD=0.008, τ_STDP=20ms
  W 范围:     Turrigiano 2012, Neuron 73:422 (突触稳态可塑性)
  背景噪声:   Shadlen & Newsome 1998, J.Neurosci. 18:3870
  感觉驱动:   Kato 2015, Cell 163:656 (光遗传等效持续激活)
  连接组:     Varshney 2011, PLoS Comput Biol 7:e1001066
  功能连接:   Randi 2023, Nature 623:406
  Γ₀=1.05:   E1 标定实验 (2026-09-01)
"""

import numpy as np
import pandas as pd
import networkx as nx
import json, math, os, time
from pathlib import Path
from sklearn.metrics import mutual_info_score
from sklearn.metrics.cluster import expected_mutual_information
import community as community_louvain

# ── 路径 ──
CONN_CSV = Path("/home/work/.openclaw/workspace/10_Knowledge/专题归档"
                "/05_Datasets_仿真与实验数据/Simulation_Results"
                "/aconnectome_white_1986_whole.csv")
DATA_DIR = Path("/home/work/i-nest/40_iNEST/45_Simulation/iNEST_Sim/data")
OUT_DIR  = Path(__file__).parent

# ── 全局常数 ──
GAMMA0 = 1.05
ALPHA  = math.log(13)
SEED   = 42

# ── LIF 参数（Bhatt 2022）──
DT        = 0.5e-3    # 0.5ms 时间步
T_TOTAL   = 10.0      # 10s：足够 STDP 收敛
N_STEPS   = int(T_TOTAL / DT)  # 20000步
V_REST    = -0.065
V_TH      = -0.050
V_RESET   = -0.070
W_SCALE   = 1.0 / 50.0
W_MIN     = 0.001
W_MAX     = 0.20     # Turrigiano 2012

# ── STDP 参数（Bi & Poo 1998）──
ETA_LTP  = 0.010
ETA_LTD  = 0.008
TAU_STDP = 20e-3     # 20ms

# ── 噪声 & 驱动 ──
SIGMA_NOISE = 0.002
I_SENSORY   = 0.020

# C. elegans 感觉神经元（Varshney 2011 分类）
SENSORY_NEURONS = [
    'ADAL','ADAR','ADFL','ADFR','ADLL','ADLR',
    'AFDL','AFDR','AIAL','AIAR','AIBL','AIBR',
    'ASEL','ASER','ASGL','ASGR','ASHL','ASHR',
    'ASIL','ASIR','ASJL','ASJR','ASKL','ASKR',
    'AWAL','AWAR','AWBL','AWBR','AWCL','AWCR',
]

RECORD_EVERY = 20   # 每 20 步记录一次（10ms/记录帧）

np.random.seed(SEED)


# ══════════════════════════════════════════════════════
# 1. 连接组加载
# ══════════════════════════════════════════════════════
def load_connectome():
    df   = pd.read_csv(CONN_CSV, sep="\t")
    chem = df[df['type'] == 'chemical']
    G_dir = nx.DiGraph()
    for _, row in chem.iterrows():
        u, v, w = str(row['pre']), str(row['post']), int(row['synapses'])
        if G_dir.has_edge(u, v): G_dir[u][v]['weight'] += w
        else: G_dir.add_edge(u, v, weight=w)
    G_und = nx.Graph()
    for u, v, d in G_dir.edges(data=True):
        if G_und.has_edge(u, v): G_und[u][v]['weight'] += d['weight']
        else: G_und.add_edge(u, v, weight=d['weight'])
    if not nx.is_connected(G_und):
        G_und = G_und.subgraph(
            max(nx.connected_components(G_und), key=len)).copy()
    nodes    = sorted(G_und.nodes())
    N        = len(nodes)
    n2i      = {n: i for i, n in enumerate(nodes)}
    # W[i,j] = j→i 突触强度
    W = np.zeros((N, N), dtype=np.float64)
    for u, v, d in G_dir.edges(data=True):
        if u in n2i and v in n2i:
            W[n2i[v], n2i[u]] = d['weight'] * W_SCALE
    W = np.clip(W, 0, W_MAX)
    return G_und, nodes, n2i, W


# ══════════════════════════════════════════════════════
# 2. τ_m 分配（Bhatt 2022）
# ══════════════════════════════════════════════════════
def assign_tau_m(nodes):
    N = len(nodes)
    np.random.seed(SEED)
    tau = np.full(N, 0.010)
    cfg = [(0.32,0.005,0.010),(0.45,0.010,0.020),(0.23,0.007,0.015)]
    idx = 0
    for frac, lo, hi in cfg:
        n = int(N * frac)
        tau[idx:idx+n] = np.random.uniform(lo, hi, n)
        idx += n
    return tau


# ══════════════════════════════════════════════════════
# 3. LIF + STDP 仿真
# ══════════════════════════════════════════════════════
def run_lif_stdp(W_init, tau_m, nodes):
    N       = len(nodes)
    W       = W_init.copy()
    V       = np.full(N, V_REST)
    t_pre   = np.full(N, -1.0)
    t_post  = np.full(N, -1.0)
    fired_prev = np.zeros(N, dtype=np.float64)

    sensory = np.array(
        [I_SENSORY if nodes[i] in SENSORY_NEURONS else 0.0
         for i in range(N)])

    n_rec     = N_STEPS // RECORD_EVERY
    V_rec     = np.zeros((N, n_rec), dtype=np.float32)
    spike_rec = np.zeros((N, n_rec), dtype=np.float32)
    rec_idx   = 0

    for t_step in range(N_STEPS):
        t_now = t_step * DT

        # 突触电流（上一步发放驱动）
        I_syn   = W @ fired_prev
        I_noise = np.random.normal(0, SIGMA_NOISE, N)
        dV      = DT / tau_m * (-(V - V_REST) + I_syn + I_noise + sensory)
        V      += dV

        # 发放检测
        fired = V >= V_TH
        V[fired] = V_RESET

        # ── 向量化 STDP（Bi & Poo 1998）──
        # Δt_ij = t_post_j - t_pre_i（post j 发放，pre i 的最近发放时刻）
        # LTP：W[j,i] += η_LTP * exp(-Δt/τ_STDP)  当 Δt>0
        # LTD：W[i,j] -= η_LTD * exp(-Δt/τ_STDP)  当 Δt>0（pre先于post）
        if fired.any():
            fired_f = fired.astype(np.float64)
            # 对 post 发放神经元（j）更新 t_post
            t_post = np.where(fired, t_now, t_post)

            # LTP：针对每个 post-j（fired），增强其所有有效突触前体 i
            # dt_pre[i] = t_now - t_pre[i]，若 0 < dt < 5τ_STDP 则 LTP
            dt_pre = t_now - t_pre          # shape (N,) — 每个前体距今时间
            ltp_mask = (dt_pre > 0) & (dt_pre < 5*TAU_STDP) & (t_pre > 0)
            ltp_factor = np.where(ltp_mask, ETA_LTP * np.exp(-dt_pre/TAU_STDP), 0.0)
            # W[j,i] += ltp_factor[i]  对所有 j in fired，i 有效突触
            # 矩阵形式：fired_f[:,None] * ltp_factor[None,:] 广播
            syn_mask_pre = W > W_MIN   # (N,N) 有效突触掩码
            dW_ltp = fired_f[:, None] * ltp_factor[None, :] * syn_mask_pre
            W = np.clip(W + dW_ltp, W_MIN, W_MAX)

            # LTD：pre 发放（上一步）→ 对其后体 j 做 LTD
            dt_post = t_now - t_post        # 每个后体距今时间（t_post 刚更新）
            ltd_mask = (dt_post > 0) & (dt_post < 5*TAU_STDP) & (t_post > 0)
            ltd_factor = np.where(ltd_mask, ETA_LTD * np.exp(-dt_post/TAU_STDP), 0.0)
            syn_mask_post = W > W_MIN
            dW_ltd = fired_prev[:, None] * ltd_factor[None, :] * syn_mask_post
            W = np.clip(W - dW_ltd, W_MIN, W_MAX)

        # 更新 t_pre 和 fired_prev
        t_pre     = np.where(fired, t_now, t_pre)
        fired_prev = fired.astype(np.float64)

        # 记录
        if t_step % RECORD_EVERY == 0 and rec_idx < n_rec:
            V_rec[:, rec_idx]     = np.clip(
                (V - V_REST) / (V_TH - V_REST), 0, 1).astype(np.float32)
            spike_rec[:, rec_idx] = fired.astype(np.float32)
            rec_idx += 1

    return V_rec[:, :rec_idx], spike_rec[:, :rec_idx], W


# ══════════════════════════════════════════════════════
# 4. Sc（与 v32_final 完全一致）
# ══════════════════════════════════════════════════════
def compute_Sc(G):
    N = G.number_of_nodes(); E = G.number_of_edges()
    C = max(len(cc) for cc in nx.connected_components(G)) / N
    kcore = nx.core_number(G)
    H     = min(max(kcore.values()) / max(math.log2(N+1),1), 1.0)
    part  = community_louvain.best_partition(G, random_state=SEED)
    Q_raw = community_louvain.modularity(part, G)
    M     = float(np.clip((Q_raw - 1/math.sqrt(max(E,1)))
                          / max(1 - 1/math.sqrt(max(E,1)), 1e-6), 0, 1))
    try:
        Cg  = nx.average_clustering(G)
        p   = 2*E/max(N*(N-1),1)
        Lg  = nx.average_shortest_path_length(
              G if nx.is_connected(G) else
              G.subgraph(max(nx.connected_components(G),key=len)))
        Lr  = math.log(N)/math.log(max(N*p,2))
        sig = (Cg/max(p,1e-6))/(Lg/max(Lr,1e-6))
        Rsw = float(np.tanh(max(sig-1,0)/2))
    except Exception:
        sig, Rsw = 1.0, 0.0
    Sc = float((C*H*M*Rsw)**0.25)
    return Sc, {"C":round(C,4),"H":round(H,4),"M":round(M,4),
                "Rsw":round(Rsw,4),"sigma":round(sig,3)}


# ══════════════════════════════════════════════════════
# 5. Tc（从 LIF 膜电位轨迹提取，Θ 是核心）
# ══════════════════════════════════════════════════════
def compute_Tc_lif(V_rec, spike_rec, FC_randi, Q_randi):
    N, T_rec = V_rec.shape
    STEP_MS  = DT * RECORD_EVERY * 1000   # 10ms/帧

    # λ_eff（Beggs 2003 分支比概念）
    S   = spike_rec[:, :-1].sum(0); S1 = spike_rec[:,1:].sum(0)
    mk  = S > 0
    kappa      = float(np.mean(S1[mk]/S[mk])) if mk.sum()>1 else 1.0
    lambda_eff = float(np.exp(-abs(kappa-1)))

    # 活跃神经元
    active_mask = spike_rec.sum(1) > 0
    V_act       = V_rec[active_mask]
    n_active    = V_act.shape[0]

    # Φ（Randi 2023 S1）
    sig_mask = (Q_randi > 0.95) & (~np.isnan(FC_randi))
    sig_vals = FC_randi[sig_mask & ~np.isnan(FC_randi)]
    CV   = np.std(sig_vals)/(np.mean(np.abs(sig_vals))+1e-6) if len(sig_vals)>=10 else 1.0
    Phi  = float(np.tanh(CV))

    # Ψ（LIF 膜电位滑动 FC）
    win, stride = 50, 10; fc_list = []
    if n_active >= 4:
        for t0 in range(0, T_rec-win, stride):
            seg = V_act[:, t0:t0+win]
            act = seg.std(1) > 1e-4
            if act.sum() >= 4:
                fc  = np.corrcoef(seg[act])
                fc  = np.nan_to_num(fc, nan=0.0)
                fc_list.append(fc[np.triu_indices_from(fc,k=1)])
    if len(fc_list) >= 3:
        fa    = np.concatenate(fc_list)
        r_Psi = np.std(fa)/(np.mean(np.abs(fa))+1e-6)
        Psi   = float(np.tanh(r_Psi))
    else:
        r_Psi, Psi = 1.0, float(np.tanh(1.0))

    # Θ（P3-B 核心：LIF 膜电位自相关衰减 τ）
    taus_ms = []
    for i in range(n_active):
        v = V_act[i].astype(float); v = v - v.mean()
        if v.std() < 1e-6: continue
        ac = np.correlate(v, v, mode='full')[len(v)-1:]
        ac /= (ac[0] + 1e-10)
        below = np.where(ac < 1/np.e)[0]
        tau_s = float(below[0]) if len(below)>0 else float(T_rec)
        taus_ms.append(tau_s * STEP_MS)

    if len(taus_ms) >= 5:
        ta     = np.array(taus_ms)
        n_bins = min(10, max(3, len(ta)//4))
        hist,_ = np.histogram(ta, bins=n_bins)
        hf     = hist[hist>0]; p = hf/hf.sum()
        H_tau  = float(-np.sum(p*np.log(p+1e-15)))
        H_max  = float(math.log(n_bins))
        Theta  = float(np.clip(H_tau/max(H_max,1.0), 0, 1))
        tau_stats = {"min":round(float(ta.min()),1), "max":round(float(ta.max()),1),
                     "mean":round(float(ta.mean()),1), "CV":round(float(ta.std()/ta.mean()),3)}
    else:
        H_tau, H_max, Theta = 0.0, 1.0, 0.0
        ta = np.array([10.0])
        tau_stats = {"min":10.0,"max":10.0,"mean":10.0,"CV":0.0}

    Tc = float((lambda_eff * Phi * Psi * Theta)**0.25)
    return Tc, {
        "kappa":        round(kappa,      4),
        "lambda_eff":   round(lambda_eff, 4),
        "CV_randi":     round(float(CV),  4),
        "Phi":          round(Phi,        4),
        "Psi":          round(Psi,        4),
        "H_tau":        round(H_tau,      4),
        "Theta":        round(Theta,      4),
        "tau_ms":       tau_stats,
        "n_active":     n_active,
        "n_taus":       len(taus_ms),
    }


# ══════════════════════════════════════════════════════
# 6. Γst（Randi 2023，P1 成果）
# ══════════════════════════════════════════════════════
def compute_AMI(p1, p2, eps=1e-10):
    nodes = sorted(set(p1)&set(p2))
    if len(nodes)<2: return 0.0
    l1=np.array([p1[n] for n in nodes]); l2=np.array([p2[n] for n in nodes])
    if len(set(l1))<2 or len(set(l2))<2: return 0.0
    I  = mutual_info_score(l1,l2)
    ct = pd.crosstab(l1,l2).values
    EI = expected_mutual_information(ct,len(l1))
    def H(x):
        _,c=np.unique(x,return_counts=True); p=c/c.sum()
        return float(-np.sum(p*np.log(p+1e-15)))
    return float((I-EI)/max(0.5*(H(l1)+H(l2))-EI,eps))

def compute_Gamma_st(G, FC_r, Q_r, nids):
    Ms  = community_louvain.best_partition(G, random_state=SEED)
    n   = len(nids)
    sm  = (Q_r>0.95)&(~np.isnan(FC_r))
    Gf  = nx.Graph()
    for i in range(n):
        for j in range(i+1,n):
            if bool(sm[i,j]) or bool(sm[j,i]):
                vals=[v for v in [FC_r[i,j],FC_r[j,i]] if not np.isnan(v)]
                w=abs(float(np.mean(vals))) if vals else 0
                if w>0: Gf.add_edge(nids[i],nids[j],weight=w)
    MT  = community_louvain.best_partition(Gf,random_state=SEED) if Gf.number_of_edges()>0 else {}
    ami = compute_AMI(Ms,MT)
    Gst = float(np.tanh(ami/GAMMA0))
    return Gst,{"AMI":round(ami,5),"Ms_n":len(set(Ms.values())),
                "MT_n":len(set(MT.values()))if MT else 0,
                "common":len(set(Ms)&set(MT))}


# ══════════════════════════════════════════════════════
# 主程序
# ══════════════════════════════════════════════════════
def main():
    print("="*60)
    print("v34_p3b_lif_stdp.py  —  P3-B v2：LIF + STDP")
    print(f"仿真: {T_TOTAL}s，dt={DT*1000:.1f}ms，STDP η_LTP={ETA_LTP} τ={TAU_STDP*1000:.0f}ms")
    print("="*60)
    t0 = time.time()

    print("\n[1] 加载连接组（Varshney 2011）...")
    G, nodes, n2i, W0 = load_connectome()
    N = len(nodes)
    print(f"  节点={N}, 突触连接={int((W0>0).sum())}")

    print("\n[2] 分配 τ_m（Bhatt 2022, S1）...")
    tau_m = assign_tau_m(nodes)
    print(f"  τ_m={tau_m.min()*1000:.1f}~{tau_m.max()*1000:.1f}ms，均值={tau_m.mean()*1000:.1f}ms")

    print(f"\n[3] LIF+STDP 仿真（{N_STEPS}步 = {T_TOTAL}s）...")
    ts = time.time()
    V_rec, spike_rec, W_final = run_lif_stdp(W0, tau_m, nodes)
    print(f"  耗时: {time.time()-ts:.1f}s")
    total_sp = int(spike_rec.sum())
    active_n = int((spike_rec.sum(1)>0).sum())
    fr = total_sp / (N * T_TOTAL)
    print(f"  总发放={total_sp}，活跃={active_n}/{N}({active_n/N*100:.1f}%)，发放率={fr:.2f}Hz")
    W_cv = W_final[W_final>0].std()/W_final[W_final>0].mean()
    print(f"  权重CV（STDP异质化）: {W_cv:.3f}（越大越异质）")

    print("\n[4] 加载 Randi 2023（S1）...")
    FC_r = np.load(DATA_DIR/"randi2023_FC_matrix.npy")
    Q_r  = np.load(DATA_DIR/"randi2023_q_alpha_matrix.npy")
    with open(DATA_DIR/"randi2023_neuron_ids.json") as f:
        nids = json.load(f)["neuron_ids"]

    print("\n[5] Sc...")
    Sc, Sc_d = compute_Sc(G)
    print(f"  C={Sc_d['C']},H={Sc_d['H']},M={Sc_d['M']},Rsw={Sc_d['Rsw']},σ={Sc_d['sigma']}")
    print(f"  Sc={Sc:.4f}")

    print("\n[6] Tc（LIF+STDP 膜电位 τ）...")
    Tc, Tc_d = compute_Tc_lif(V_rec, spike_rec, FC_r, Q_r)
    tm = Tc_d['tau_ms']
    print(f"  λ_eff={Tc_d['lambda_eff']} (κ={Tc_d['kappa']})")
    print(f"  Φ={Tc_d['Phi']} (Randi 2023 S1)")
    print(f"  Ψ={Tc_d['Psi']} (LIF 滑动FC)")
    print(f"  τ: {tm['min']}~{tm['max']}ms，均值={tm['mean']}ms，CV={tm['CV']}")
    print(f"  Θ={Tc_d['Theta']} (H_tau={Tc_d['H_tau']}，{Tc_d['n_taus']}个神经元)")
    print(f"  Tc={Tc:.4f}")

    print("\n[7] Γst（Randi 2023 S1）...")
    Gst, Gst_d = compute_Gamma_st(G, FC_r, Q_r, nids)
    print(f"  AMI={Gst_d['AMI']}，Ms={Gst_d['Ms_n']}社区，MT={Gst_d['MT_n']}社区")
    print(f"  Γst={Gst:.4f}")

    print("\n[8] CST...")
    CST = float((Sc*Tc)*math.exp(ALPHA*Gst))
    print(f"  CST=({Sc:.4f}×{Tc:.4f})×exp({ALPHA:.4f}×{Gst:.4f})")
    print(f"     ={Sc*Tc:.4f}×{math.exp(ALPHA*Gst):.4f}={CST:.4f}")
    ths=[(4.669,"L6"),(3.14159,"L5"),(2.71828,"L4"),(1.61803,"L3"),(1.0,"L2"),(0.70711,"L1")]
    level="L0-反射弧"
    for t,l in ths:
        if CST>=t: level=l; break
    print(f"  等级: {level}")

    print("\n[9] 改进路线汇总")
    print(f"  {'版本':<24} {'Θ':>6} {'Tc':>7} {'Γst':>7} {'CST':>7}  等级")
    print(f"  {'-'*62}")
    rows=[
        ("v32-Final(binary STDP)",  0.040, 0.4441, 0.0251, 0.3624, "L0"),
        ("P1(Randi Γst)",           0.040, 0.4441, 0.1096, 0.4501, "L0"),
        ("P3-A(文献τ注入)",         0.879, 0.7706, 0.1096, 0.8522, "L1"),
        ("P3-B v1(LIF无STDP)",      0.125, 0.5232, 0.1075, 0.5749, "L0"),
        ("P3-B v2(LIF+STDP本次)",   Tc_d['Theta'],Tc,Gst,CST,level[:2]),
    ]
    for name,th,tc,gst,cst,lv in rows:
        print(f"  {name:<24} {th:>6.3f} {tc:>7.4f} {gst:>7.4f} {cst:>7.4f}  {lv}")

    result={
        "experiment":"v34_p3b_lif_stdp","date":"2026-09-02",
        "improvement":"P3-B v2: LIF+STDP，τ从突触可塑性驱动的膜电位动力学涌现",
        "sim_params":{"T_total_s":T_TOTAL,"dt_ms":DT*1000,"N_steps":N_STEPS,
                      "N_neurons":N,"active_n":active_n,
                      "firing_rate_Hz":round(fr,2),"W_CV_after_STDP":round(float(W_cv),3)},
        "Sc":round(Sc,4),"Sc_detail":Sc_d,
        "Tc":round(Tc,4),"Tc_detail":{k:(float(v) if isinstance(v,(np.floating,np.integer)) else v)
                                       for k,v in Tc_d.items()},
        "Gst":round(Gst,4),"Gst_detail":Gst_d,
        "alpha":round(ALPHA,4),"CST":round(CST,4),"level":level,
        "baselines":{
            "v32_final":  {"Sc":0.7652,"Tc":0.4441,"Gst":0.0251,"CST":0.3624},
            "p1_only":    {"Sc":0.7652,"Tc":0.4441,"Gst":0.1096,"CST":0.4501},
            "p3a":        {"Sc":0.8350,"Tc":0.7706,"Gst":0.1096,"CST":0.8522},
            "p3b_v1":     {"Sc":0.8339,"Tc":0.5232,"Gst":0.1075,"CST":0.5749},
        },
        "wall_time_s":round(time.time()-t0,1),
    }
    out = OUT_DIR/"v34_p3b_stdp_results.json"
    with open(out,"w",encoding="utf-8") as f:
        json.dump(result,f,ensure_ascii=False,indent=2)
    print(f"\n✅ 保存: {out}  总耗时: {time.time()-t0:.1f}s")
    return result

if __name__=="__main__":
    main()
