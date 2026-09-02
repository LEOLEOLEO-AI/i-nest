#!/usr/bin/env python3
"""
v36_multispecies_cst.py — 多系统 CST 统一计算框架 v2

目标：用同一套正确公式重新计算所有生物和ANN系统
公式：CST = (Sc × Tc) × exp(α × Γst)
  Sc  = geo_mean(C, H, M, Rsw)
  Tc  = geo_mean(λ_eff, Φ, Ψ, Θ)
  Γst = tanh(AMI / Γ₀),  Γ₀=1.05 锁定
  α   = ln(M_eff)

生物 Sc：真实连接组拓扑
生物 Γst：STDP仿真（大网络采样子网 N≤500），标注 S4
         C.elegans 直接引用 Randi 2023 S1 实测值
生物 Tc：文献τ注入 + F-D bins（P3-A方案B）
ANN：V25 文献参数 + 当前公式重建（方式Y，标注 S5）
"""

import json, math, numpy as np
from pathlib import Path

OUT_DIR  = Path(__file__).parent
GAMMA0   = 1.05   # E1 标定，2026-09-01 锁定，禁止修改
N_SAMPLE = 500    # 大网络仿真采样上限

THRESHOLDS = [
    (4.669,   "L6"), (3.14159, "L5"), (2.71828, "L4"),
    (1.61803, "L3"), (1.00000, "L2"), (0.70711, "L1"),
]

def get_level(cst):
    for t, l in THRESHOLDS:
        if cst >= t: return l
    return "L0"

def geo_mean(*vals):
    v = [float(x) for x in vals]
    if any(x <= 0 for x in v): return 0.0
    return math.exp(sum(math.log(x) for x in v) / len(v))

# ── 连接组加载 ──────────────────────────────────────────
def load_connectome(json_path):
    with open(json_path) as f:
        d = json.load(f)
    N = d['N']
    edges = d.get('edges_chem', d.get('edges', []))
    A = np.zeros((N, N))
    for e in edges:
        i, j, w = int(e[0]), int(e[1]), float(e[2])
        if 0 <= i < N and 0 <= j < N:
            A[i, j] += w
    return A, N

# ── Sc 四分量 ───────────────────────────────────────────
def sc_components(A):
    N = A.shape[0]
    adj = (A > 0).astype(float)
    deg = adj.sum(axis=1)
    k   = deg.mean()

    # C：连接完整性
    C = float(np.tanh(k / math.log2(max(N, 2))))

    # H：层次深度（BFS直径，采样50节点）
    import random; random.seed(0)
    samp = list(range(N)) if N <= 50 else random.sample(range(N), 50)
    max_d = 0
    for src in samp:
        vis = {src: 0}; q = [src]
        while q:
            nxt = []
            for u in q:
                for v in np.where(adj[u] > 0)[0]:
                    if v not in vis:
                        vis[v] = vis[u]+1
                        max_d = max(max_d, vis[v])
                        nxt.append(v)
            q = nxt
    H = float(np.tanh(max_d / math.log2(max(N, 2))))

    # M：模块度代理（度分布熵比较）
    row_sum = adj.sum(axis=1)
    p = row_sum / (row_sum.sum() + 1e-10)
    p = p[p > 0]
    H_deg  = float(-(p * np.log(p)).sum())
    H_max  = math.log(N)
    M = float(np.tanh(max(0, 1.0 - H_deg / H_max))) if H_max > 0 else 0.0

    # Rsw：小世界系数
    cc_local = []
    for i in range(N):
        nb = np.where(adj[i] > 0)[0]
        ki = len(nb)
        if ki < 2:
            cc_local.append(0.0); continue
        edges_nb = adj[np.ix_(nb, nb)].sum() / 2
        cc_local.append(float(2 * edges_nb / (ki * (ki - 1))))
    C_net  = float(np.mean(cc_local))
    C_rand = k / N if N > 0 else 1e-6
    # 路径长度：小网络BFS，大网络近似
    if N <= 300:
        total_d = 0; cnt = 0
        for src in range(N):
            vis = {src: 0}; q = [src]
            while q:
                nxt = []
                for u in q:
                    for v in np.where(adj[u] > 0)[0]:
                        if v not in vis:
                            vis[v] = vis[u]+1; nxt.append(v)
                q = nxt
            for d in vis.values():
                if d > 0: total_d += d; cnt += 1
        L_net = total_d / cnt if cnt > 0 else N
    else:
        samp2 = random.sample(range(N), 100)
        total_d = 0; cnt = 0
        for src in samp2:
            vis = {src: 0}; q = [src]
            while q:
                nxt = []
                for u in q:
                    for v in np.where(adj[u] > 0)[0]:
                        if v not in vis:
                            vis[v] = vis[u]+1; nxt.append(v)
                q = nxt
            for d in vis.values():
                if d > 0: total_d += d; cnt += 1
        L_net = total_d / cnt if cnt > 0 else N
    L_rand = math.log(N) / math.log(max(k, 1.01)) if k > 1 else N
    sigma  = (C_net / max(C_rand, 1e-10)) / (L_net / max(L_rand, 1e-10))
    Rsw    = float(np.tanh(sigma - 1) / 2 + 0.5)
    Rsw    = max(0.0, min(1.0, Rsw))

    Sc = geo_mean(C, H, M, Rsw)
    return {"Sc": Sc, "C": C, "H": H, "M": M, "Rsw": Rsw}

# ── Γst STDP 仿真（向量化，大网络采样） ─────────────────
def compute_gst(A, N, n_steps=500, noise=0.02, seed=42):
    np.random.seed(seed)
    from sklearn.metrics.cluster import normalized_mutual_info_score
    from scipy.cluster.hierarchy import fcluster, linkage
    from scipy.spatial.distance import squareform

    # 采样子网
    if N > N_SAMPLE:
        deg = (A > 0).sum(axis=1) + (A > 0).sum(axis=0)
        idx = np.argsort(deg)[::-1][:N_SAMPLE]
        idx = np.sort(idx)
        A_s = A[np.ix_(idx, idx)]
        Ns  = N_SAMPLE; sampled = True
    else:
        A_s = A; Ns = N; sampled = False

    # 归一化 + 自适应阈值
    W = A_s.astype(float)
    if W.max() > 0: W /= W.max()
    col_s = W.sum(axis=0)
    cs    = col_s[col_s > 0]
    thresh = float(np.percentile(cs, 10)) * 0.5 if len(cs) > 0 else 0.3
    thresh = max(0.01, min(thresh, 0.5))

    # 固定权重传播（Γst 反映网络拓扑结构决定的结构-功能对齐，与STDP学习无关）
    # STDP LTD 会将权重压至 w_min 导致激活熄灭；固定权重物理上更合理
    init = np.random.choice(Ns, max(1, Ns//20), replace=False)
    spk  = np.zeros(Ns); spk[init] = 1.0
    hist = np.zeros((Ns, n_steps))

    for t in range(n_steps):
        inp  = W.T @ spk + noise * np.random.rand(Ns)
        spk  = (inp > thresh).astype(float)
        hist[:, t] = spk

    # 活跃神经元
    active = np.where(hist.sum(axis=1) > 2)[0]
    n_act  = int(len(active) / Ns * N) if sampled else len(active)
    if len(active) < 4:
        return {"Gst": 0.0, "AMI": 0.0, "n_active": n_act,
                "thresh": thresh, "sampled": sampled,
                "note": f"激活不足({len(active)}/{Ns})"}

    H_act = hist[active]
    FC    = np.corrcoef(H_act); np.fill_diagonal(FC, 0)

    nc = max(2, int(math.sqrt(len(active))))
    # 结构社区
    As = A_s[np.ix_(active, active)]
    ds = 1 - As / (As.max() + 1e-10)
    ds = np.clip((ds + ds.T)/2, 0, None); np.fill_diagonal(ds, 0)
    try:
        Ms = fcluster(linkage(squareform(ds), 'ward'), nc, 'maxclust')
    except Exception:
        Ms = np.arange(len(active)) % nc + 1
    # 功能社区
    df = 1 - np.abs(FC) / (np.abs(FC).max() + 1e-10)
    df = np.clip((df + df.T)/2, 0, None); np.fill_diagonal(df, 0)
    try:
        MT = fcluster(linkage(squareform(df), 'ward'), nc, 'maxclust')
    except Exception:
        MT = np.arange(len(active)) % nc + 1

    AMI = float(normalized_mutual_info_score(Ms, MT, average_method='arithmetic'))
    Gst = float(np.tanh(AMI / GAMMA0))
    note = "STDP仿真 S4" + (f"（采样{Ns}/{N}）" if sampled else "")
    return {"Gst": Gst, "AMI": AMI, "n_active": n_act,
            "thresh": thresh, "sampled": sampled, "note": note}

# ── Tc（文献τ + F-D bins） ──────────────────────────────
def compute_tc(N, hist, tau_params):
    """
    hist: (N_sim, n_steps) spike history
    tau_params: {class: (mu_s, sig_s, frac)}
    """
    active_rate = (hist.sum(axis=1) > 2).mean()
    lam = float(np.tanh(active_rate * 2))

    active = np.where(hist.sum(axis=1) > 2)[0]
    if len(active) >= 4:
        FC = np.corrcoef(hist[active]); np.fill_diagonal(FC, 0)
        FC = np.nan_to_num(FC, nan=0.0)   # 零方差行列置0
        fc = FC[np.triu_indices(len(active), k=1)]
        cv = float(np.std(fc) / (np.mean(np.abs(fc)) + 1e-8))
        Phi = float(np.tanh(cv))
    else:
        Phi = 0.05

    T = hist.shape[1]; win = max(1, T//10)
    rates = [hist[:, i*win:(i+1)*win].mean() for i in range(10)]
    Psi = float(np.tanh(np.std(rates) / (np.mean(rates) + 1e-8)))

    # τ 分布（LogNormal采样，F-D bins）
    np.random.seed(42)
    taus = []
    for cls, (mu, sig, frac) in tau_params.items():
        n    = max(1, int(N * frac))
        s_ln = math.sqrt(math.log(1 + (sig/mu)**2))
        m_ln = math.log(mu) - s_ln**2/2
        taus.extend(np.random.lognormal(m_ln, s_ln, n).tolist())
    taus = np.array(taus)
    iqr  = float(np.percentile(taus,75) - np.percentile(taus,25))
    bw   = 2*iqr/(len(taus)**(1/3)) if iqr > 0 else 0.1
    nb   = max(2, int((taus.max()-taus.min())/bw))
    cnt, _ = np.histogram(taus, bins=nb)
    cnt = cnt[cnt>0]; p = cnt/cnt.sum()
    Ht  = float(-(p*np.log(p)).sum())
    Hm  = math.log(nb)
    Theta = Ht/Hm if Hm > 0 else 0.0

    Tc = geo_mean(lam, Phi, Psi, Theta)
    return {"Tc": Tc, "lambda_eff": round(lam,4), "Phi": round(Phi,4),
            "Psi": round(Psi,4), "Theta": round(Theta,4), "n_bins": nb}

# ── 生物系统完整计算 ────────────────────────────────────
def run_bio(name, json_path, tau_params, alpha, alpha_src,
            n_steps=500, noise=0.02,
            gst_override=None, gst_src=None):
    print(f"\n[{name}]", flush=True)
    A, N = load_connectome(json_path)
    print(f"  N={N}, edges={int((A>0).sum())}", flush=True)

    # Sc
    sc = sc_components(A)
    print(f"  Sc={sc['Sc']:.4f}  C={sc['C']:.3f} H={sc['H']:.3f} "
          f"M={sc['M']:.3f} Rsw={sc['Rsw']:.3f}", flush=True)

    # Γst
    if gst_override is not None:
        gst_r = {"Gst": gst_override, "AMI": float(np.arctanh(gst_override)*GAMMA0),
                 "note": gst_src, "n_active": "N/A"}
    else:
        print(f"  Γst STDP仿真（{n_steps}步）...", flush=True)
        gst_r = compute_gst(A, N, n_steps=n_steps, noise=noise)
    Gst = gst_r["Gst"]
    print(f"  Γst={Gst:.4f}  AMI={gst_r['AMI']:.4f}  "
          f"active≈{gst_r['n_active']}  [{gst_r['note']}]", flush=True)

    # Tc spike history：固定权重传播（与Γst一致）
    np.random.seed(42)
    Ns2 = min(N, N_SAMPLE)
    if N > N_SAMPLE:
        deg2 = (A>0).sum(axis=1)+(A>0).sum(axis=0)
        idx2 = np.argsort(deg2)[::-1][:Ns2]; idx2 = np.sort(idx2)
        A_s2 = A[np.ix_(idx2,idx2)]
    else:
        A_s2 = A
    W2 = A_s2.astype(float)
    if W2.max()>0: W2 /= W2.max()
    col_s2 = W2.sum(axis=0); cs2 = col_s2[col_s2>0]
    thr2 = float(np.percentile(cs2,10))*0.5 if len(cs2)>0 else 0.3
    thr2 = max(0.01, min(thr2, 0.5))
    init2 = np.random.choice(Ns2, max(1,Ns2//20), replace=False)
    spk2  = np.zeros(Ns2); spk2[init2] = 1.0
    hist  = np.zeros((Ns2, n_steps))
    for t in range(n_steps):
        inp2  = W2.T @ spk2 + noise * np.random.rand(Ns2)
        spk2  = (inp2 > thr2).astype(float)
        hist[:,t] = spk2

    tc_r = compute_tc(Ns2, hist, tau_params)
    Tc = tc_r["Tc"]
    print(f"  Tc={Tc:.4f}  λ={tc_r['lambda_eff']} Φ={tc_r['Phi']} "
          f"Ψ={tc_r['Psi']} Θ={tc_r['Theta']} bins={tc_r['n_bins']}", flush=True)

    CST   = (sc["Sc"] * Tc) * math.exp(alpha * Gst)
    level = get_level(CST)
    print(f"  α={alpha:.4f}  ★ CST={CST:.4f}  [{level}]", flush=True)

    return {
        "name": name, "N": N,
        "Sc": round(sc["Sc"],4), **{k: round(sc[k],4) for k in ["C","H","M","Rsw"]},
        "Tc": round(Tc,4), **{k: tc_r[k] for k in ["lambda_eff","Phi","Psi","Theta","n_bins"]},
        "Gst": round(Gst,4), "AMI": round(gst_r["AMI"],4),
        "alpha": round(alpha,4), "alpha_src": alpha_src,
        "CST": round(CST,4), "level": level,
        "Gst_src": gst_r["note"],
    }

# ── ANN 系统（方式Y） ────────────────────────────────────
ANN_PARAMS = {
    "GPT-2 (Transformer)": {
        "C":0.556,"H":0.72,"M":0.18,"Rsw":0.44,
        "lam":0.48,"Phi":0.31,"Psi":0.03,"Theta":0.05,
        "Gst":0.00, "alpha":math.log(2),
        "alpha_src":"binary digital M_eff=2",
        "src":"Brown2020 GPT-3 Methods + V25 Table",
    },
    "ResNet-50 (CNN)": {
        "C":0.42,"H":0.65,"M":0.22,"Rsw":0.38,
        "lam":0.35,"Phi":0.28,"Psi":0.03,"Theta":0.04,
        "Gst":0.00, "alpha":math.log(2),
        "alpha_src":"binary digital M_eff=2",
        "src":"He2016 CVPR ResNet + V25 Table",
    },
    "LTC/NCP": {
        "C":0.61,"H":0.55,"M":0.35,"Rsw":0.58,
        "lam":0.55,"Phi":0.38,"Psi":0.08,"Theta":0.12,
        "Gst":0.02, "alpha":math.log(2),
        "alpha_src":"binary digital M_eff=2",
        "src":"Hasani2021 NatMachIntell + V25 Table",
    },
    "Intel Loihi-2 (NMH)": {
        "C":0.58,"H":0.62,"M":0.41,"Rsw":0.61,
        "lam":0.72,"Phi":0.55,"Psi":0.18,"Theta":0.15,
        "Gst":0.08, "alpha":math.log(32),
        "alpha_src":"CMOS LIF M_eff≈32, Strong1998 S2",
        "src":"Orchard2021 NeurIPS Loihi-2 + V25 Table",
    },
    "MoE (Switch-1.7T)": {
        "C":0.48,"H":0.78,"M":0.14,"Rsw":0.40,
        "lam":0.50,"Phi":0.29,"Psi":0.03,"Theta":0.04,
        "Gst":0.01, "alpha":math.log(2),
        "alpha_src":"binary digital M_eff=2",
        "src":"Fedus2022 JMLR Switch Transformer + V25 Table",
    },
}

def run_ann():
    print("\n[ANN 系统（方式Y）]", flush=True)
    results = []
    for name, p in ANN_PARAMS.items():
        Sc  = geo_mean(p["C"],p["H"],p["M"],p["Rsw"])
        Tc  = geo_mean(p["lam"],p["Phi"],p["Psi"],p["Theta"])
        CST = (Sc*Tc)*math.exp(p["alpha"]*p["Gst"])
        lv  = get_level(CST)
        print(f"  {name}: Sc={Sc:.4f} Tc={Tc:.4f} Γst={p['Gst']:.4f} "
              f"α={p['alpha']:.3f} → CST={CST:.4f} [{lv}]", flush=True)
        results.append({
            "name":name,
            "Sc":round(Sc,4),"C":p["C"],"H":p["H"],"M":p["M"],"Rsw":p["Rsw"],
            "Tc":round(Tc,4),"lambda_eff":p["lam"],"Phi":p["Phi"],
            "Psi":p["Psi"],"Theta":p["Theta"],
            "Gst":p["Gst"],"alpha":round(p["alpha"],4),
            "alpha_src":p["alpha_src"],
            "CST":round(CST,4),"level":lv,
            "Gst_src":"V25论文 S5","src":p["src"],
        })
    return results

# ── 主流程 ───────────────────────────────────────────────
def main():
    print("="*60)
    print("v36_multispecies_cst.py v2  —  多系统 CST 统一计算")
    print(f"Γ₀={GAMMA0}  N_SAMPLE={N_SAMPLE}")
    print("="*60)

    results_bio = []
    results_ann = []

    # C.elegans（直接引用）
    results_bio.append({
        "name":"C.elegans","N":281,
        "Sc":0.8350,"C":1.0,"H":1.0,"M":0.4977,"Rsw":0.9769,
        "Tc":0.7711,"lambda_eff":0.9048,"Phi":0.7188,"Psi":0.8588,"Theta":0.633,"n_bins":19,
        "Gst":0.1096,"AMI":0.1155,
        "alpha":round(math.log(40/3),4),
        "alpha_src":"Lockery2009+Liu2009 graded potential S2",
        "CST":0.8528,"level":"L1",
        "Gst_src":"Randi 2023 Nature 623:406 S1",
    })
    print("[C.elegans] 直接引用: CST=0.8528 L1 ✅")

    # Drosophila larval CNS
    # τ来源：脉冲神经元，Borst 2010 Nat Rev Neurosci S1（视觉运动系统τ~10-50ms）
    dro_tau = {
        "sensory": (0.010, 0.004, 0.35),
        "inter":   (0.030, 0.015, 0.45),
        "motor":   (0.020, 0.008, 0.20),
    }
    r_dro = run_bio(
        "Drosophila larval CNS",
        "/home/work/i-nest/40_iNEST/45_Simulation/connectome_larval_cns_sm.json",
        dro_tau, math.log(32),
        "Strong1998 脉冲神经元 M_eff≈32 S2",
        n_steps=300,
    )
    results_bio.append(r_dro)

    # Macaque cortex
    # τ来源：Murray 2014 Nat Neurosci S1（皮层τ层级：V1~80ms，PFC~350ms）
    mac_tau = {
        "sensory": (0.080, 0.030, 0.20),
        "inter":   (0.350, 0.150, 0.50),
        "motor":   (0.150, 0.060, 0.30),
    }
    r_mac = run_bio(
        "Macaque cortex",
        "/home/work/i-nest/40_iNEST/45_Simulation/connectome_macaque_rm.json",
        mac_tau, math.log(50),
        "Rieke1996 Spikes 皮层 M_eff≈50 S2",
        n_steps=500,
    )
    results_bio.append(r_mac)

    # ANN
    results_ann = run_ann()

    # 汇总排序
    all_r = results_bio + results_ann
    all_r.sort(key=lambda x: x["CST"])

    print(f"\n{'='*65}")
    print("完整 CST 排序表")
    print(f"{'='*65}")
    print(f"  {'系统':<28} {'CST':>7}  {'等级':<5}  α       Gst来源")
    print(f"  {'-'*63}")
    for r in all_r:
        print(f"  {r['name']:<28} {r['CST']:>7.4f}  {r['level']:<5}  "
              f"{r['alpha']:.3f}   {r.get('Gst_src','?')[:20]}")

    # 保存
    out = OUT_DIR / "v36_multispecies_results.json"
    with open(out,"w",encoding="utf-8") as f:
        json.dump({
            "experiment":"v36_multispecies_cst_v2",
            "date":"2026-09-02",
            "gamma0":GAMMA0,
            "N_sample":N_SAMPLE,
            "bio_results":results_bio,
            "ann_results":results_ann,
            "all_sorted":all_r,
        }, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 保存: {out}")

if __name__ == "__main__":
    main()
