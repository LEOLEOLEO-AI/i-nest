#!/usr/bin/env python3
"""
v36_fix.py — 修复两个问题
1. M：用 Louvain 算法计算真实模块度（替代度分布熵代理）
2. Ψ：用周期性外部刺激驱动网络，体现真实时间变化性

Drosophila/Macaque 的 M 和 Ψ 重新计算后更新 CST。
"""

import json, math, numpy as np
from pathlib import Path

GAMMA0   = 1.05
N_SAMPLE = 500
OUT_DIR  = Path(__file__).parent

THRESHOLDS = [
    (4.669,"L6"),(3.14159,"L5"),(2.71828,"L4"),
    (1.61803,"L3"),(1.0,"L2"),(0.70711,"L1"),
]
def get_level(c):
    for t,l in THRESHOLDS:
        if c >= t: return l
    return "L0"

def geo_mean(*v):
    v = [float(x) for x in v]
    if any(x<=0 for x in v): return 0.0
    return math.exp(sum(math.log(x) for x in v)/len(v))

# ── 修复1：Louvain 真实模块度 ─────────────────────────
def compute_M_louvain(A):
    """
    用 python-louvain 算法计算模块度 Q，映射到 [0,1]
    Q = (实际社区内边权 - 期望值) / 总边权
    Q ∈ [-0.5, 1.0]，实际网络通常 0.1~0.7
    归一化：M = tanh(Q * 2)（Q=0.3→M=0.54，Q=0.5→M=0.76）
    """
    import networkx as nx
    import community as comm_louvain

    N = A.shape[0]
    # 构建无向图（对称化）
    W = (A + A.T) / 2
    G = nx.from_numpy_array(W)
    # 删除自环和零权边
    G.remove_edges_from(nx.selfloop_edges(G))
    G = nx.Graph([(u,v,d) for u,v,d in G.edges(data=True) if d.get('weight',0)>0])

    if G.number_of_edges() == 0:
        return 0.0, {}, 0.0

    partition = comm_louvain.best_partition(G, weight='weight', random_state=42)
    Q = comm_louvain.modularity(partition, G, weight='weight')
    n_comm = len(set(partition.values()))
    M = float(np.tanh(max(0, Q) * 2))
    return M, partition, Q

# ── 修复2：周期性刺激驱动，计算真实 Ψ ───────────────
def compute_Psi_driven(A, N_sim, n_steps=500, noise=0.02,
                        stim_period=50, stim_frac=0.1, seed=42,
                        ei_ratio=0.20):
    """
    Ψ：时间变化性
    1. E-I 平衡：20% 抑制性神经元（Sahara 2012 J Neurosci S2）
       防止过饱和激活，保留时间起伏
    2. 周期性外部刺激
       Drosophila ~20Hz（Ito 2008 Nat Neurosci S1）
       Macaque gamma/beta（Fries 2015 Neuron S1）
    """
    np.random.seed(seed)
    W = A.astype(float)
    if W.max() > 0: W /= W.max()
    col_s = W.sum(axis=0); cs = col_s[col_s>0]
    thresh = float(np.percentile(cs, 10))*0.5 if len(cs)>0 else 0.3
    thresh = max(0.01, min(thresh, 0.5))

    # E-I 平衡：20% 抑制性节点，出边取负
    n_inh = max(1, int(N_sim * ei_ratio))
    inh   = np.random.choice(N_sim, n_inh, replace=False)
    W_ei  = W.copy(); W_ei[inh, :] *= -1.0

    n_stim = max(1, int(N_sim * stim_frac))
    init = np.random.choice(N_sim, max(1, N_sim//20), replace=False)
    spk  = np.zeros(N_sim); spk[init] = 1.0
    hist = np.zeros((N_sim, n_steps))

    for t in range(n_steps):
        inp = W_ei.T @ spk + noise * np.random.rand(N_sim)
        if t % stim_period == 0:
            stim_idx = np.random.choice(N_sim, n_stim, replace=False)
            inp[stim_idx] += thresh * 2.0
        spk = (inp > thresh).astype(float)
        hist[:, t] = spk

    win   = max(1, n_steps // 20)
    n_win = n_steps // win
    rates = np.array([hist[:, i*win:(i+1)*win].mean() for i in range(n_win)])
    Psi   = float(np.tanh(rates.std() / (rates.mean() + 1e-8)))

    active = (hist.sum(axis=1) > 2).sum()
    return hist, Psi, active, thresh, rates

# ── 重新计算每个生物系统 ────────────────────────────
def recompute_system(name, json_path, tau_params, alpha, alpha_src,
                     old_result, n_steps=500):
    print(f"\n[{name}] 修复计算", flush=True)

    with open(json_path) as f: d = json.load(f)
    N = d['N']
    edges = d.get('edges_chem', d.get('edges', []))
    A = np.zeros((N, N))
    for e in edges:
        i,j,w = int(e[0]),int(e[1]),float(e[2])
        if 0<=i<N and 0<=j<N: A[i,j] += w

    # 采样子网（高度节点优先）
    if N > N_SAMPLE:
        deg = (A>0).sum(axis=1)+(A>0).sum(axis=0)
        idx = np.argsort(deg)[::-1][:N_SAMPLE]; idx = np.sort(idx)
        A_s = A[np.ix_(idx,idx)]; Ns = N_SAMPLE
    else:
        A_s = A; Ns = N

    # ── 修复1：Louvain M ──
    print(f"  计算 Louvain 模块度...", flush=True)
    M_new, partition, Q = compute_M_louvain(A_s)
    n_comm = len(set(partition.values())) if partition else 0
    print(f"  M_louvain={M_new:.4f}  Q={Q:.4f}  n_communities={n_comm}  "
          f"(旧M_proxy={old_result['M']:.4f})", flush=True)

    # ── 修复2：Ψ（周期性刺激） ──
    print(f"  计算 Ψ（周期性刺激驱动，{n_steps}步）...", flush=True)
    hist, Psi_new, n_act, thresh, rates = compute_Psi_driven(
        A_s, Ns, n_steps=n_steps)
    print(f"  Ψ={Psi_new:.4f}  活跃={n_act}/{Ns}  thresh={thresh:.4f}  "
          f"(旧Ψ={old_result['Psi']:.4f})", flush=True)

    # ── 重新计算 Tc ──
    # 其余分量不变
    lam  = old_result["lambda_eff"]
    Phi  = old_result["Phi"]

    # 重新算 Φ（用新 hist）
    active = np.where(hist.sum(axis=1) > 2)[0]
    if len(active) >= 4:
        FC = np.corrcoef(hist[active]); np.fill_diagonal(FC, 0)
        FC = np.nan_to_num(FC, nan=0.0)
        fc = FC[np.triu_indices(len(active), k=1)]
        cv = float(np.std(fc) / (np.mean(np.abs(fc)) + 1e-8))
        Phi_new = float(np.tanh(cv))
    else:
        Phi_new = Phi
    print(f"  Φ={Phi_new:.4f}  (旧Φ={Phi:.4f})", flush=True)

    # 重新算 λ_eff
    lam_new = float(np.tanh((hist.sum(axis=1) > 2).mean() * 2))
    print(f"  λ_eff={lam_new:.4f}  (旧λ={lam:.4f})", flush=True)

    Theta = old_result["Theta"]
    Tc_new = geo_mean(lam_new, Phi_new, Psi_new, Theta)
    print(f"  Tc={Tc_new:.4f}  (旧Tc={old_result['Tc']:.4f})", flush=True)

    # ── 更新 Sc（用新 M）──
    C   = old_result["C"]
    H   = old_result["H"]
    Rsw = old_result["Rsw"]
    Sc_new = geo_mean(C, H, M_new, Rsw)
    print(f"  Sc={Sc_new:.4f}  (旧Sc={old_result['Sc']:.4f})", flush=True)

    # ── CST ──
    Gst = old_result["Gst"]
    CST_new = (Sc_new * Tc_new) * math.exp(alpha * Gst)
    level = get_level(CST_new)
    print(f"  ★ CST={CST_new:.4f}  [{level}]  "
          f"(旧CST={old_result['CST']:.4f})", flush=True)

    r = dict(old_result)
    r.update({
        "M": round(M_new,4), "M_Q": round(Q,4), "n_communities": n_comm,
        "Psi": round(Psi_new,4), "Phi": round(Phi_new,4),
        "lambda_eff": round(lam_new,4),
        "Tc": round(Tc_new,4), "Sc": round(Sc_new,4),
        "CST": round(CST_new,4), "level": level,
        "fix_note": "M=Louvain, Ψ=周期性刺激驱动",
    })
    return r


# ── 主流程 ───────────────────────────────────────────
def main():
    # 加载 v36 原始结果
    v36_path = OUT_DIR / "v36_multispecies_results.json"
    with open(v36_path) as f:
        v36 = json.load(f)

    bio_old = {r["name"]: r for r in v36["bio_results"]}

    # τ 参数（与 v36 一致）
    dro_tau = {"sensory":(0.010,0.004,0.35),"inter":(0.030,0.015,0.45),"motor":(0.020,0.008,0.20)}
    mac_tau = {"sensory":(0.080,0.030,0.20),"inter":(0.350,0.150,0.50),"motor":(0.150,0.060,0.30)}

    results_fixed = []

    # C.elegans 不需要修复
    results_fixed.append(bio_old["C.elegans"])
    print("[C.elegans] 不修复，直接沿用: CST=0.8528 L1 ✅")

    # Drosophila
    r_dro = recompute_system(
        "Drosophila larval CNS",
        "/home/work/i-nest/40_iNEST/45_Simulation/connectome_larval_cns_sm.json",
        dro_tau, math.log(32), "Strong1998 M_eff≈32 S2",
        bio_old["Drosophila larval CNS"],
        n_steps=400,
    )
    results_fixed.append(r_dro)

    # Macaque
    r_mac = recompute_system(
        "Macaque cortex",
        "/home/work/i-nest/40_iNEST/45_Simulation/connectome_macaque_rm.json",
        mac_tau, math.log(50), "Rieke1996 M_eff≈50 S2",
        bio_old["Macaque cortex"],
        n_steps=500,
    )
    results_fixed.append(r_mac)

    # ANN 不变
    ann_results = v36["ann_results"]

    # 汇总
    all_r = results_fixed + ann_results
    all_r.sort(key=lambda x: x["CST"])

    print(f"\n{'='*65}")
    print("修复后完整 CST 排序表")
    print(f"{'='*65}")
    print(f"  {'系统':<28} {'CST':>7}  {'等级':<5}  {'Sc':>6} {'Tc':>6} {'Γst':>6}")
    print(f"  {'-'*63}")
    for r in all_r:
        print(f"  {r['name']:<28} {r['CST']:>7.4f}  {r['level']:<5}  "
              f"{r['Sc']:>6.4f} {r['Tc']:>6.4f} {r['Gst']:>6.4f}")

    # 保存
    out = OUT_DIR / "v36_fixed_results.json"
    with open(out,"w",encoding="utf-8") as f:
        json.dump({
            "experiment":"v36_multispecies_fixed",
            "date":"2026-09-02",
            "fixes":["M=Louvain模块度算法","Ψ=周期性刺激驱动时间变化性"],
            "bio_results": results_fixed,
            "ann_results": ann_results,
            "all_sorted": all_r,
        }, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 保存: {out}")

if __name__ == "__main__":
    main()
