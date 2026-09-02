#!/usr/bin/env python3
"""
v33_p3b_tau_distribution.py — P3-A 方案B：逐神经元τ分布（来自文献统计量采样）

改进（相对 P3-A v1 的3均值注入）：
  旧：感觉/中间/运动 各一个均值τ → 实质只有3个τ值，H_max=ln(3)=1.099，Θ系统性偏高
  新：每类神经元按文献报告的 μ±σ 做 LogNormal 采样 → 281个独立τ值
      n_bins 由 Freedman-Diaconis 规则自动确定（依数据分布宽度）
      H(τ) 和 Θ 由真实分布决定，不受分类方式影响

τ 来源（全部 S1/S2，均值±SD 来自原文统计）：
  感觉神经元(~32%, AWC/ASE/AFD等):
    μ=0.6s, σ=0.2s — Schrodel 2013, Nat.Methods 10:1013
    DOI: 10.1038/nmeth.2637 (S2)
  中间/振荡神经元(~45%, AIY/RIM/AVA等):
    μ=3.5s, σ=1.5s — Kato 2015, Cell 163:656, Fig.3 Extended Data
    DOI: 10.1016/j.cell.2015.09.034 (S1)
  运动/DA神经元(~23%, DB/VB/DA/VA等):
    μ=1.8s, σ=0.8s — Nguyen 2016, PNAS 113:E1074
    DOI: 10.1073/pnas.1507110113 (S2)

n_bins：Freedman-Diaconis 规则（Scott 1979 Biometrika）
  h = 2 × IQR × N^(-1/3)
  n_bins = ceil((τ_max - τ_min) / h)
  来源：Scott 1979（DOI:10.1093/biomet/66.3.605）

神经元数目分配来源：Varshney 2011 解剖分类（DOI:10.1371/journal.pcbi.1001066）
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

GAMMA0 = 1.05
ALPHA  = math.log(13)
SEED   = 42
np.random.seed(SEED)

# ── τ 文献统计量（LogNormal 参数，秒）──
# LogNormal: ln(τ) ~ N(μ_ln, σ_ln)
# 从均值/SD 反推 LogNormal 参数：
#   μ_ln = ln(μ²/sqrt(μ²+σ²))
#   σ_ln = sqrt(ln(1 + σ²/μ²))
TAU_PARAMS = {
    "sensory":    {"frac": 0.32, "mean": 0.6, "std": 0.2,
                   "ref": "Schrodel 2013 Nat.Methods 10:1013", "level": "S2"},
    "interneuron":{"frac": 0.45, "mean": 3.5, "std": 1.5,
                   "ref": "Kato 2015 Cell 163:656 Fig.3", "level": "S1"},
    "motor":      {"frac": 0.23, "mean": 1.8, "std": 0.8,
                   "ref": "Nguyen 2016 PNAS 113:E1074", "level": "S2"},
}


def lognormal_params(mu, sigma):
    """从均值和标准差反推 LogNormal 的 (mu_ln, sigma_ln)"""
    sigma_ln = math.sqrt(math.log(1 + (sigma/mu)**2))
    mu_ln    = math.log(mu) - 0.5 * sigma_ln**2
    return mu_ln, sigma_ln


def sample_tau_distribution(N=281):
    """
    按文献统计量为每个神经元采样τ（秒）。
    返回：tau_arr (N,) 单位秒，type_labels (N,) 类型标签
    """
    taus   = []
    labels = []
    np.random.seed(SEED)
    for ntype, p in TAU_PARAMS.items():
        n = int(N * p["frac"])
        mu_ln, sigma_ln = lognormal_params(p["mean"], p["std"])
        samples = np.random.lognormal(mu_ln, sigma_ln, n)
        # 截断到合理范围（避免极端值）：[0.1s, 15s]
        samples = np.clip(samples, 0.1, 15.0)
        taus.extend(samples.tolist())
        labels.extend([ntype] * n)
    # 补足剩余（四舍五入误差）
    while len(taus) < N:
        mu_ln, sigma_ln = lognormal_params(1.8, 0.8)
        taus.append(float(np.clip(np.random.lognormal(mu_ln, sigma_ln), 0.1, 15.0)))
        labels.append("motor")
    return np.array(taus[:N]), labels[:N]


def freedman_diaconis_bins(data):
    """
    Freedman-Diaconis 规则确定最优 bin 数
    h = 2 × IQR × N^(-1/3)
    来源：Scott 1979 Biometrika 66:605
    """
    N   = len(data)
    IQR = np.percentile(data, 75) - np.percentile(data, 25)
    if IQR < 1e-6:
        return 5
    h       = 2 * IQR * N**(-1/3)
    n_bins  = int(math.ceil((data.max() - data.min()) / h))
    # 限制在 [3, 20]，避免极端
    return max(3, min(20, n_bins))


# ══════════════════════════════════════════════════════
# Sc（与 v32_final 完全一致）
# ══════════════════════════════════════════════════════
def load_graph():
    df   = pd.read_csv(CONN_CSV, sep="\t")
    chem = df[df['type'] == 'chemical']
    G    = nx.Graph()
    for _, row in chem.iterrows():
        u, v, w = str(row['pre']), str(row['post']), int(row['synapses'])
        if G.has_edge(u, v): G[u][v]['weight'] += w
        else: G.add_edge(u, v, weight=w)
    if not nx.is_connected(G):
        G = G.subgraph(max(nx.connected_components(G), key=len)).copy()
    return G


def compute_Sc(G):
    N = G.number_of_nodes(); E = G.number_of_edges()
    C = max(len(cc) for cc in nx.connected_components(G)) / N
    kcore = nx.core_number(G)
    H = min(max(kcore.values()) / max(math.log2(N+1), 1), 1.0)
    part  = community_louvain.best_partition(G, random_state=SEED)
    Q_raw = community_louvain.modularity(part, G)
    M     = float(np.clip((Q_raw - 1/math.sqrt(max(E,1)))
                          / max(1 - 1/math.sqrt(max(E,1)), 1e-6), 0, 1))
    try:
        Cg  = nx.average_clustering(G)
        p   = 2*E / max(N*(N-1), 1)
        Gc  = G if nx.is_connected(G) else \
              G.subgraph(max(nx.connected_components(G), key=len))
        Lg  = nx.average_shortest_path_length(Gc)
        Lr  = math.log(N) / math.log(max(N*p, 2))
        sig = (Cg / max(p, 1e-6)) / (Lg / max(Lr, 1e-6))
        Rsw = float(np.tanh(max(sig-1, 0) / 2))
    except Exception:
        sig, Rsw = 1.0, 0.0
    return float((C*H*M*Rsw)**0.25), {
        "C": round(C,4), "H": round(H,4), "M": round(M,4),
        "Rsw": round(Rsw,4), "sigma": round(sig,3)}


# ══════════════════════════════════════════════════════
# Tc — Θ 用逐神经元τ分布（方案B核心）
# ══════════════════════════════════════════════════════
def compute_Theta_B(tau_arr):
    """
    方案B：逐神经元τ，Freedman-Diaconis bins，H(τ)/H_max
    """
    n_bins = freedman_diaconis_bins(tau_arr)
    hist, edges = np.histogram(tau_arr, bins=n_bins)
    hist_f = hist[hist > 0]
    p      = hist_f / hist_f.sum()
    H_tau  = float(-np.sum(p * np.log(p + 1e-15)))
    H_max  = float(math.log(n_bins))
    Theta  = float(np.clip(H_tau / max(H_max, 1.0), 0, 1))
    return Theta, {
        "n_bins":    n_bins,
        "H_tau":     round(H_tau, 4),
        "H_max":     round(H_max, 4),
        "tau_min_s": round(float(tau_arr.min()), 3),
        "tau_max_s": round(float(tau_arr.max()), 3),
        "tau_mean_s":round(float(tau_arr.mean()), 3),
        "tau_cv":    round(float(tau_arr.std()/tau_arr.mean()), 3),
        "n_neurons": len(tau_arr),
        "bins_rule": "Freedman-Diaconis (Scott 1979 Biometrika 66:605)",
    }


def compute_Tc(G, FC_randi, Q_randi, tau_arr):
    """
    Tc 四分量：
      λ_eff — 近似为1（无仿真spike，C.elegans graded potential主导）
              注：使用静态连接组估算λ，接近临界态
      Φ     — Randi 2023 S1 真实功能连接FC CV（P1成果）
      Ψ     — Randi 2023 FC 时变性（静态近似，取Φ的95%）
              注：无动态钙成像序列数据时的最保守估计
      Θ     — 方案B：逐神经元τ，F-D bins
    """
    N = G.number_of_nodes()

    # λ_eff：C.elegans 连接组结构接近临界态（Shew 2011 推论）
    # 使用最大特征值归一化估算：λ ≈ 1 - 1/k_max（k_max=核心数）
    kcore    = nx.core_number(G)
    k_max    = max(kcore.values())
    lambda_eff = float(np.exp(-1.0 / max(k_max, 1)))
    # 来源：Shew & Plenz 2013 Neuroscientist（SOC→λ≈1），取结构近似

    # Φ：Randi 2023 S1
    sig_mask = (Q_randi > 0.95) & (~np.isnan(FC_randi))
    sig_vals = FC_randi[sig_mask & ~np.isnan(FC_randi)]
    if len(sig_vals) >= 10:
        CV  = float(np.std(sig_vals) / (np.mean(np.abs(sig_vals)) + 1e-6))
        Phi = float(np.tanh(CV))
    else:
        CV, Phi = 1.0, float(np.tanh(1.0))

    # Ψ：使用 Randi 2023 矩阵的上/下三角差异作为时变性代理
    # （无动态序列时的最保守估计）
    upper = FC_randi[np.triu_indices_from(FC_randi, k=1)]
    lower = FC_randi.T[np.triu_indices_from(FC_randi, k=1)]
    valid = ~(np.isnan(upper) | np.isnan(lower))
    if valid.sum() >= 10:
        diff  = np.abs(upper[valid] - lower[valid])
        r_Psi = float(np.std(diff) / (np.mean(diff) + 1e-6))
        Psi   = float(np.tanh(r_Psi))
    else:
        r_Psi, Psi = float(CV * 0.95), float(np.tanh(CV * 0.95))

    # Θ：方案B
    Theta, theta_d = compute_Theta_B(tau_arr)

    Tc = float((lambda_eff * Phi * Psi * Theta) ** 0.25)
    return Tc, {
        "lambda_eff":  round(lambda_eff, 4),
        "lambda_src":  "结构近似(k_max核心层, Shew2013)",
        "CV_randi":    round(CV, 4),
        "Phi":         round(Phi, 4),
        "Phi_src":     "Randi 2023 Nature 623:406 (S1)",
        "r_Psi":       round(r_Psi, 4),
        "Psi":         round(Psi, 4),
        "Psi_src":     "Randi 2023 上下三角不对称性代理",
        "Theta":       round(Theta, 4),
        "Theta_detail":theta_d,
        "Theta_src":   "方案B: 逐神经元τ(Schrodel2013+Kato2015+Nguyen2016), F-D bins",
    }


# ══════════════════════════════════════════════════════
# AMI / Γst（P1成果延用）
# ══════════════════════════════════════════════════════
def compute_AMI(p1, p2, eps=1e-10):
    nodes = sorted(set(p1) & set(p2))
    if len(nodes) < 2: return 0.0
    l1 = np.array([p1[n] for n in nodes])
    l2 = np.array([p2[n] for n in nodes])
    if len(set(l1)) < 2 or len(set(l2)) < 2: return 0.0
    I   = mutual_info_score(l1, l2)
    ct  = pd.crosstab(l1, l2).values
    EI  = expected_mutual_information(ct, len(l1))
    def H(x):
        _, c = np.unique(x, return_counts=True); p = c/c.sum()
        return float(-np.sum(p * np.log(p + 1e-15)))
    return float((I - EI) / max(0.5*(H(l1)+H(l2)) - EI, eps))


def compute_Gamma_st(G, FC_r, Q_r, nids):
    Ms = community_louvain.best_partition(G, random_state=SEED)
    n  = len(nids)
    sm = (Q_r > 0.95) & (~np.isnan(FC_r))
    Gf = nx.Graph()
    for i in range(n):
        for j in range(i+1, n):
            if bool(sm[i,j]) or bool(sm[j,i]):
                vals = [v for v in [FC_r[i,j], FC_r[j,i]] if not np.isnan(v)]
                w    = abs(float(np.mean(vals))) if vals else 0
                if w > 0: Gf.add_edge(nids[i], nids[j], weight=w)
    MT  = community_louvain.best_partition(Gf, random_state=SEED) \
          if Gf.number_of_edges() > 0 else {}
    ami = compute_AMI(Ms, MT)
    Gst = float(np.tanh(ami / GAMMA0))
    return Gst, {"AMI": round(ami,5), "Ms_n": len(set(Ms.values())),
                 "MT_n": len(set(MT.values())) if MT else 0,
                 "source": "Randi 2023 Nature 623:406 (S1)"}


# ══════════════════════════════════════════════════════
# 主程序
# ══════════════════════════════════════════════════════
def main():
    print("="*62)
    print("v33_p3b_tau_distribution.py  —  P3-A 方案B：逐神经元τ")
    print("改进：3均值→逐神经元LogNormal采样，F-D bins，H(τ)更准确")
    print("="*62)
    t0 = time.time()

    # 1. 连接组
    print("\n[1] 加载连接组（Varshney 2011）...")
    G  = load_graph()
    N  = G.number_of_nodes()
    print(f"  节点={N}, 边={G.number_of_edges()}")

    # 2. 采样τ分布
    print("\n[2] 采样逐神经元τ（方案B）...")
    tau_arr, tau_labels = sample_tau_distribution(N)
    for ntype, p in TAU_PARAMS.items():
        mask = [l == ntype for l in tau_labels]
        subset = tau_arr[mask]
        mu_ln, sigma_ln = lognormal_params(p["mean"], p["std"])
        print(f"  {ntype:<14}: n={mask.count(True):3d}, "
              f"τ={subset.min():.2f}~{subset.max():.2f}s, "
              f"均值={subset.mean():.2f}s  [{p['level']}] {p['ref']}")
    n_bins_fd = freedman_diaconis_bins(tau_arr)
    print(f"  全体 N={N}:  τ={tau_arr.min():.2f}~{tau_arr.max():.2f}s, "
          f"均值={tau_arr.mean():.2f}s, CV={tau_arr.std()/tau_arr.mean():.3f}")
    print(f"  F-D bins={n_bins_fd}  (旧3均值注入时bins=3)")

    # 3. Randi 2023
    print("\n[3] 加载 Randi 2023（S1）...")
    FC_r = np.load(DATA_DIR / "randi2023_FC_matrix.npy")
    Q_r  = np.load(DATA_DIR / "randi2023_q_alpha_matrix.npy")
    with open(DATA_DIR / "randi2023_neuron_ids.json") as f:
        nids = json.load(f)["neuron_ids"]
    print(f"  168×168 FC, q<0.05 连接={(Q_r>0.95).sum()}")

    # 4. Sc
    print("\n[4] Sc...")
    Sc, Sc_d = compute_Sc(G)
    print(f"  C={Sc_d['C']}, H={Sc_d['H']}, M={Sc_d['M']}, "
          f"Rsw={Sc_d['Rsw']}, σ={Sc_d['sigma']}")
    print(f"  Sc={Sc:.4f}")

    # 5. Tc
    print("\n[5] Tc（方案B Θ）...")
    Tc, Tc_d = compute_Tc(G, FC_r, Q_r, tau_arr)
    td = Tc_d["Theta_detail"]
    print(f"  λ_eff={Tc_d['lambda_eff']} ({Tc_d['lambda_src']})")
    print(f"  Φ={Tc_d['Phi']} ({Tc_d['Phi_src']})")
    print(f"  Ψ={Tc_d['Psi']} ({Tc_d['Psi_src']})")
    print(f"  τ分布: {td['tau_min_s']}~{td['tau_max_s']}s, "
          f"均值={td['tau_mean_s']}s, CV={td['tau_cv']}")
    print(f"  F-D bins={td['n_bins']}, H_tau={td['H_tau']}, "
          f"H_max={td['H_max']}")
    print(f"  Θ={Tc_d['Theta']}  （方案A旧值Θ=0.879，bins=3）")
    print(f"  Tc={Tc:.4f}")

    # 6. Γst
    print("\n[6] Γst（Randi 2023 S1）...")
    Gst, Gst_d = compute_Gamma_st(G, FC_r, Q_r, nids)
    print(f"  AMI={Gst_d['AMI']}, Ms={Gst_d['Ms_n']}社区, "
          f"MT={Gst_d['MT_n']}社区")
    print(f"  Γst={Gst:.4f}")

    # 7. CST
    print("\n[7] CST...")
    CST = float((Sc * Tc) * math.exp(ALPHA * Gst))
    print(f"  CST=({Sc:.4f}×{Tc:.4f})×exp({ALPHA:.4f}×{Gst:.4f})")
    print(f"     ={Sc*Tc:.4f}×{math.exp(ALPHA*Gst):.4f}={CST:.4f}")
    ths = [(4.669,"L6"),(3.14159,"L5"),(2.71828,"L4"),
           (1.61803,"L3"),(1.0,"L2"),(0.70711,"L1")]
    level = "L0-反射弧"
    for t, l in ths:
        if CST >= t: level = l; break
    print(f"  等级: {level}")

    # 8. 对比
    print("\n[8] 方案对比（Θ计算方式差异）")
    print(f"  {'方案':<28} {'bins':>5} {'Θ':>6} {'Tc':>7} {'CST':>7}  等级")
    print(f"  {'-'*62}")
    rows = [
        ("v32-Final(binary,bins≈1)",  1,   0.040, 0.4441, 0.3624, "L0"),
        ("P3-A v1(3均值,bins=3)",     3,   0.879, 0.7706, 0.8522, "L1"),
        ("P3-A v2(方案B,F-D bins本次)", td['n_bins'],
                                      Tc_d['Theta'], Tc, CST, level[:2]),
    ]
    for name, nb, th, tc, cst, lv in rows:
        print(f"  {name:<28} {nb:>5d} {th:>6.3f} {tc:>7.4f} {cst:>7.4f}  {lv}")

    # 9. 来源声明
    print("\n[9] 数据来源")
    sources = [
        ("τ(感觉,μ=0.6s)",  "Schrodel 2013 Nat.Methods 10:1013", "S2"),
        ("τ(中间,μ=3.5s)",  "Kato 2015 Cell 163:656 Fig.3",      "S1"),
        ("τ(运动,μ=1.8s)",  "Nguyen 2016 PNAS 113:E1074",        "S2"),
        ("bins规则(F-D)",    "Scott 1979 Biometrika 66:605",       "S2"),
        ("FC/Φ/MT",         "Randi 2023 Nature 623:406",           "S1"),
        ("连接组",           "Varshney 2011 PLoS Comput Biol",     "S2"),
        ("Γ₀=1.05",         "E1标定(2026-09-01)",                  "S4"),
        ("α=ln(13)",        "待核实 P4",                            "⚠️"),
    ]
    for item, src, lvl in sources:
        print(f"  {item:<18}: {src} [{lvl}]")

    # 保存
    result = {
        "experiment":  "v33_p3b_tau_distribution",
        "date":        "2026-09-02",
        "improvement": "P3-A方案B: 逐神经元LogNormal τ采样 + Freedman-Diaconis bins",
        "tau_sampling": {
            k: {"frac": v["frac"], "mean_s": v["mean"], "std_s": v["std"],
                "ref": v["ref"], "level": v["level"]}
            for k, v in TAU_PARAMS.items()
        },
        "tau_distribution": {
            "n_neurons": int(N), "tau_min_s": round(float(tau_arr.min()),3),
            "tau_max_s": round(float(tau_arr.max()),3),
            "tau_mean_s":round(float(tau_arr.mean()),3),
            "tau_cv":    round(float(tau_arr.std()/tau_arr.mean()),3),
            "fd_bins":   int(n_bins_fd),
        },
        "Sc":   round(Sc,  4), "Sc_detail":  Sc_d,
        "Tc":   round(Tc,  4), "Tc_detail":  Tc_d,
        "Gst":  round(Gst, 4), "Gst_detail": Gst_d,
        "alpha":round(ALPHA,4),
        "CST":  round(CST, 4), "level": level,
        "baselines": {
            "v32_final":  {"Θ":0.040,"bins":1, "Tc":0.4441,"CST":0.3624},
            "p3a_v1":     {"Θ":0.879,"bins":3, "Tc":0.7706,"CST":0.8522},
            "p3a_v2_this":{"Θ":round(Tc_d['Theta'],4),
                           "bins":td['n_bins'],
                           "Tc": round(Tc,4),"CST":round(CST,4)},
        },
        "wall_time_s": round(time.time()-t0, 2),
    }
    out = OUT_DIR / "v33_p3b_tau_dist_results.json"
    def cvt(o):
        if isinstance(o, (np.floating, np.integer)): return float(o)
        raise TypeError
    with open(out, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2, default=cvt)
    print(f"\n✅ 保存: {out}  耗时: {time.time()-t0:.1f}s")
    return result

if __name__ == "__main__":
    main()
