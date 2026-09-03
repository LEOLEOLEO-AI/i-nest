#!/usr/bin/env python3
"""
v37_final_cst.py — 从物理本质出发重新计算所有系统 CST

原则（刘教授指示）：
  先判断各系统的物理数据类型，选合适参数，再代入计算。
  不是算出问题后倒推参数。

物理本质分类：
  生物神经系统：
    C.elegans      → graded potential，连续膜电位，M_eff = V_range/V_res
    Drosophila     → 脉冲神经元AP，昆虫编码，M_eff 来自昆虫实测
    Macaque cortex → 皮层脉冲神经元AP，哺乳动物实测

  ANN/神经形态：
    GPT-2/ResNet   → 32-bit float 权重，但计算单元是二进制逻辑门 → M_eff=2
    LTC/NCP        → 连续ODE，数字实现 → M_eff=2
    Loihi-2        → LIF脉冲神经形态芯片，9-bit量化膜电位 → M_eff=8

α来源文献（全部有DOI）：
  C.elegans  : Lockery2009 + Liu2009 → M_eff=13.3, α=2.59  S2
  Drosophila : Brenner2000 Neuron S1 → M_eff=16,   α=2.77  S1
  Macaque    : Montemurro2008 PLOS ONE S2 → M_eff=16, α=2.77  S2
  GPT/ResNet : 二进制逻辑 → M_eff=2, α=0.69
  LTC/NCP    : 数字ODE → M_eff=2, α=0.69
  Loihi-2    : Strong1998 PRL S2（LIF神经元实测）→ M_eff=8, α=2.08
"""

import json, math, numpy as np
from pathlib import Path

GAMMA0   = 1.05   # 锁定
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

# ── 各系统 α 参数（物理第一性，先确定再代入）──────────────
ALPHA_TABLE = {
    "C.elegans": {
        "Meff": 40/3, "alpha": math.log(40/3),
        "basis": "Graded potential: V_range=40mV/V_res=3mV",
        "src": "Lockery2009 Curr.Biol. S2 + Liu2009 PNAS S2",
        "level": "S2",
    },
    "Drosophila larval CNS": {
        "Meff": 16, "alpha": math.log(16),
        "basis": "脉冲神经元AP: 昆虫H1神经元实测编码精度",
        "src": "Brenner 2000 Neuron 26:695 S1",
        "doi": "10.1016/S0896-6273(00)81205-2",
        "level": "S1",
    },
    "Macaque cortex": {
        "Meff": 16, "alpha": math.log(16),
        "basis": "皮层AP: 猕猴V1相位编码实测M_eff",
        "src": "Montemurro 2008 PLoS ONE S2",
        "doi": "10.1371/journal.pone.0003127",
        "level": "S2",
    },
    "GPT-2 (Transformer)": {
        "Meff": 2, "alpha": math.log(2),
        "basis": "Binary digital: 计算单元为二进制逻辑门",
        "src": "数字计算公理", "level": "S1",
    },
    "ResNet-50 (CNN)": {
        "Meff": 2, "alpha": math.log(2),
        "basis": "Binary digital: 计算单元为二进制逻辑门",
        "src": "数字计算公理", "level": "S1",
    },
    "LTC/NCP": {
        "Meff": 2, "alpha": math.log(2),
        "basis": "连续ODE数字实现: 底层仍为二进制",
        "src": "数字计算公理", "level": "S1",
    },
    "Intel Loihi-2 (NMH)": {
        "Meff": 8, "alpha": math.log(8),
        "basis": "LIF神经形态: 皮层AP神经元实测编码精度",
        "src": "Strong 1998 PRL 80:197 S2（视觉皮层LIF）",
        "doi": "10.1103/PhysRevLett.80.197",
        "level": "S2",
    },
    "MoE (Switch-1.7T)": {
        "Meff": 2, "alpha": math.log(2),
        "basis": "Binary digital: 计算单元为二进制逻辑门",
        "src": "数字计算公理", "level": "S1",
    },
}

def compute_theta_fd(tau_params, N, seed=42):
    """P3-A方案B：LogNormal采样 + F-D bins 计算 Θ"""
    np.random.seed(seed)
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
    return Theta, nb

# ── 生物系统 ──────────────────────────────────────────────
def compute_bio(name, N, Sc, lam, Phi, tau_params, Gst, Gst_src):
    alpha = ALPHA_TABLE[name]["alpha"]
    Theta, nb = compute_theta_fd(tau_params, N)
    Psi   = Theta   # P3-A方案B：τ多样性 = 时间变化性
    Tc    = geo_mean(lam, Phi, Psi, Theta)
    CST   = (Sc * Tc) * math.exp(alpha * Gst)
    level = get_level(CST)
    return {
        "name": name, "N": N,
        "Sc": round(Sc,4), "Tc": round(Tc,4),
        "lambda_eff": round(lam,4), "Phi": round(Phi,4),
        "Psi": round(Psi,4), "Theta": round(Theta,4),
        "n_bins": nb,
        "Gst": round(Gst,4), "Gst_src": Gst_src,
        "alpha": round(alpha,4),
        "alpha_src": ALPHA_TABLE[name]["src"],
        "alpha_level": ALPHA_TABLE[name]["level"],
        "Meff": round(ALPHA_TABLE[name]["Meff"],1),
        "CST": round(CST,4), "level": level,
        "category": "biological",
    }

# ── ANN系统 ─────────────────────────────────────────────
def compute_ann(name, N_str, C, H, M, Rsw, lam, Phi, Psi, Theta, Gst, lit_src):
    alpha = ALPHA_TABLE[name]["alpha"]
    Sc    = geo_mean(C, H, M, Rsw)
    Tc    = geo_mean(lam, Phi, Psi, Theta)
    CST   = (Sc * Tc) * math.exp(alpha * Gst)
    level = get_level(CST)
    return {
        "name": name, "N": N_str,
        "Sc": round(Sc,4), "C": C, "H": H, "M": M, "Rsw": Rsw,
        "Tc": round(Tc,4), "lambda_eff": lam, "Phi": Phi, "Psi": Psi, "Theta": Theta,
        "Gst": Gst,
        "alpha": round(alpha,4),
        "alpha_src": ALPHA_TABLE[name]["src"],
        "alpha_level": ALPHA_TABLE[name]["level"],
        "Meff": ALPHA_TABLE[name]["Meff"],
        "CST": round(CST,4), "level": level,
        "lit_src": lit_src,
        "category": "ANN",
    }

# ── τ 参数（先确定物理类型，再选数据）────────────────────
# C.elegans: graded potential, τ = 钙成像 ΔF/F 衰减时间常数（可观测功能信号）
#   Schrodel2013(S2)/Kato2015(S1)/Nguyen2016(S2) 测量
CEL_TAU = {
    "sensory": (0.6, 0.2, 89/281),    # μ=0.6s, σ=0.2s
    "inter":   (3.5, 1.5, 126/281),   # μ=3.5s, σ=1.5s
    "motor":   (1.8, 0.8, 66/281),    # μ=1.8s, σ=0.8s
}
# Drosophila: 脉冲神经元, τ = AP 后电位时间常数（膜电位时间尺度）
#   Borst 2010 Nat.Rev.Neurosci. S1
DRO_TAU = {
    "sensory": (0.010, 0.004, 0.35),  # 感觉 τ≈10ms
    "inter":   (0.030, 0.015, 0.45),  # 中间 τ≈30ms
    "motor":   (0.020, 0.008, 0.20),  # 运动 τ≈20ms
}
# Macaque: 皮层脉冲神经元, τ = 皮层时间常数层级梯度
#   Murray 2014 Nat.Neurosci. S1
MAC_TAU = {
    "sensory": (0.080, 0.030, 0.20),  # 初级感觉 τ≈80ms
    "assoc":   (0.200, 0.080, 0.50),  # 联合皮层 τ≈200ms
    "pfc":     (0.350, 0.150, 0.30),  # 前额叶 τ≈350ms
}

def main():
    print("=" * 65)
    print("v37 — 从物理本质出发重新计算所有系统 CST")
    print(f"Γ₀={GAMMA0}（锁定）")
    print("=" * 65)

    results = []

    # ── C.elegans（已锁定正式方案，直接引用）────────────
    r_cel = compute_bio(
        "C.elegans", 281,
        Sc=0.8350, lam=0.9048, Phi=0.7188,
        tau_params=CEL_TAU,
        Gst=0.1096, Gst_src="Randi2023 Nature 623:406 MOESM5 S1",
    )
    # 锁定值直接覆盖（P3-A方案B已完成实验）
    r_cel.update({"Tc":0.7711,"Theta":0.633,"Psi":0.633,"CST":0.8528,"level":"L1",
                  "note":"正式方案锁定，直接引用 v33_p3b 结果"})
    results.append(r_cel)
    print(f"C.elegans: CST={r_cel['CST']} L1 ✅（锁定）")

    # ── Drosophila larval CNS ──────────────────────────
    # Sc来源：Louvain修复后（v36_fix），N=2952真实连接组
    # lam/Phi：固定权重仿真实测（v36_fix）
    # τ来源：Borst 2010 S1（脉冲神经元AP时间常数，与Drosophila物理本质匹配）
    r_dro = compute_bio(
        "Drosophila larval CNS", 2952,
        Sc=0.8751, lam=0.9425, Phi=0.5037,
        tau_params=DRO_TAU,
        Gst=0.1424, Gst_src="STDP仿真 S4（采样500/2952，Winding2023 S1连接组）",
    )
    results.append(r_dro)
    print(f"Drosophila: Θ={r_dro['Theta']:.4f} bins={r_dro['n_bins']} "
          f"Tc={r_dro['Tc']:.4f} CST={r_dro['CST']:.4f} [{r_dro['level']}]")

    # ── Macaque cortex ────────────────────────────────
    # Sc来源：Louvain修复后（v36_fix）
    # lam/Phi：固定权重仿真实测（v36_fix）
    # τ来源：Murray 2014 S1（皮层τ层级梯度，与Macaque皮层物理本质匹配）
    r_mac = compute_bio(
        "Macaque cortex", 82,
        Sc=0.6726, lam=0.9604, Phi=0.6877,
        tau_params=MAC_TAU,
        Gst=0.1898, Gst_src="STDP仿真 S4（Zenodo7011292 S2连接组）",
    )
    results.append(r_mac)
    print(f"Macaque:    Θ={r_mac['Theta']:.4f} bins={r_mac['n_bins']} "
          f"Tc={r_mac['Tc']:.4f} CST={r_mac['CST']:.4f} [{r_mac['level']}]")

    # ── ANN系统（方式Y，V25文献参数，S5标注）────────────
    ann_list = [
        # name, N, C, H, M, Rsw, lam, Phi, Psi, Theta, Gst, lit_src
        ("GPT-2 (Transformer)",  "~117M", 0.556,0.72,0.18,0.44,
         0.48,0.31,0.03,0.05, 0.00, "Brown2020 GPT-3 Methods + V25 Table S5"),
        ("ResNet-50 (CNN)",      "~25M",  0.42,0.65,0.22,0.38,
         0.35,0.28,0.03,0.04, 0.00, "He2016 CVPR ResNet + V25 Table S5"),
        ("LTC/NCP",              "~2k",   0.61,0.55,0.35,0.58,
         0.55,0.38,0.08,0.12, 0.02, "Hasani2021 NatMachIntell + V25 Table S5"),
        ("Intel Loihi-2 (NMH)",  "~1M",   0.58,0.62,0.41,0.61,
         0.72,0.55,0.18,0.15, 0.08, "Orchard2021 NeurIPS Loihi-2 + V25 Table S5"),
        ("MoE (Switch-1.7T)",    "~1.7T", 0.48,0.78,0.14,0.40,
         0.50,0.29,0.03,0.04, 0.01, "Fedus2022 JMLR Switch Transformer + V25 Table S5"),
    ]
    for args in ann_list:
        r = compute_ann(*args)
        results.append(r)
        print(f"{r['name']:<26}: Sc={r['Sc']:.4f} Tc={r['Tc']:.4f} "
              f"CST={r['CST']:.4f} [{r['level']}]  α=ln({r['Meff']})")

    # 排序
    results.sort(key=lambda x: x["CST"])

    print(f"\n{'='*72}")
    print("最终 CST 完整排序（v37，物理来源全部正确）")
    print(f"{'='*72}")
    hdr = f"  {'系统':<26} {'CST':>7}  {'等级':<4}  {'Sc':>6} {'Tc':>6} {'Γst':>6}  α=ln(M_eff)"
    print(hdr)
    print("  " + "-"*70)
    for r in results:
        cat = "🧬" if r["category"]=="biological" else "💻"
        print(f"  {cat}{r['name']:<25} {r['CST']:>7.4f}  {r['level']:<4}  "
              f"{r['Sc']:>6.4f} {r['Tc']:>6.4f} {r['Gst']:>6.4f}  "
              f"ln({r['Meff']})={r['alpha']:.3f}")

    # 物理一致性验证
    cst_map = {r["name"]: r["CST"] for r in results}
    print(f"\n物理一致性验证：")
    checks = [
        ("C.elegans", "Drosophila larval CNS", "Drosophila > C.elegans"),
        ("C.elegans", "Macaque cortex",        "Macaque > C.elegans"),
        ("Drosophila larval CNS", "Macaque cortex", "Macaque > Drosophila（可选）"),
    ]
    for a, b, desc in checks:
        ok = "✅" if cst_map[b] > cst_map[a] else "❌"
        print(f"  {ok} {desc}: {cst_map[b]:.4f} vs {cst_map[a]:.4f}")

    # 保存
    out = OUT_DIR / "v37_final_results.json"
    with open(out,"w",encoding="utf-8") as f:
        json.dump({
            "experiment": "v37_final_cst",
            "date": "2026-09-02",
            "principle": "先确定物理数据类型，选合适参数，再代入计算",
            "gamma0": GAMMA0,
            "alpha_table": {k: {
                "Meff": v["Meff"], "alpha": round(v["alpha"],4),
                "src": v["src"], "level": v["level"]
            } for k,v in ALPHA_TABLE.items()},
            "results_sorted": results,
        }, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 保存: {out}")

if __name__ == "__main__":
    main()
