#!/usr/bin/env python3
"""
v35_alpha_sensitivity.py — α 区间鲁棒性验证

目的：证明 L1 结论对 V_res 估计不敏感
  V_res 范围：2~5mV（C.elegans graded potential noise floor 合理区间）
  α = ln(40mV / V_res) → 区间 [ln(8), ln(20)] = [2.08, 3.00]
  固定 Sc/Tc/Γst（已由 S1 文献锁定），只扫描 α

锁定值（来自前序实验）：
  Sc=0.8350  来源：Varshney 2011 (S2)
  Tc=0.7711  来源：Randi 2023 (S1) + Kato/Schrodel/Nguyen τ分布 (S1-S2) + F-D bins
  Γst=0.1096 来源：Randi 2023 Nature 623:406 (S1)

α 推导依据：
  V_range=40mV：Lockery 2009, Curr.Biol.
  V_res=3mV（基准）：Liu et al. 2009, PNAS
  α = ln(V_range/V_res) = ln(M_eff)，S3级（物理推导）

CST = (Sc × Tc) × exp(α × Γst)
"""

import math, json
import numpy as np
from pathlib import Path

OUT_DIR = Path(__file__).parent

# ── 锁定值 ──
Sc   = 0.8350
Tc   = 0.7711
Gst  = 0.1096
ScTc = Sc * Tc

# ── CST 阈值 ──
THRESHOLDS = [
    (4.669,    "L6-通用认知"),
    (3.14159,  "L5-自主规划"),
    (2.71828,  "L4-模式识别"),
    (1.61803,  "L3-目标导向"),
    (1.00000,  "L2-条件反射"),
    (0.70711,  "L1-信号整合"),
]

def get_level(cst):
    for t, l in THRESHOLDS:
        if cst >= t: return l
    return "L0-反射弧"

def main():
    print("="*60)
    print("v35_alpha_sensitivity.py  —  α 区间鲁棒性验证")
    print(f"固定: Sc={Sc}, Tc={Tc}, Γst={Gst}")
    print(f"扫描: V_res=2~5mV → α=ln(40/V_res)")
    print("="*60)

    V_range = 40.0  # mV，Lockery 2009

    # ── 扫描 V_res ──
    print(f"\n{'V_res(mV)':<12} {'M_eff':<8} {'α':<8} {'CST':<8}  等级")
    print("-"*56)

    results = []
    v_res_list = [2.0, 2.5, 3.0, 3.5, 4.0, 5.0]
    for vr in v_res_list:
        meff  = V_range / vr
        alpha = math.log(meff)
        cst   = ScTc * math.exp(alpha * Gst)
        level = get_level(cst)
        marker = " ← 基准(Liu 2009)" if vr == 3.0 else ""
        print(f"  {vr:<10} {meff:<8.1f} {alpha:<8.4f} {cst:<8.4f}  {level}{marker}")
        results.append({"V_res_mV": vr, "M_eff": round(meff,1),
                        "alpha": round(alpha,4), "CST": round(cst,4),
                        "level": level})

    # ── 统计 ──
    cst_vals = [r["CST"] for r in results]
    print(f"\n{'CST 范围:':<16} {min(cst_vals):.4f} ~ {max(cst_vals):.4f}")
    print(f"{'CST 变化幅度:':<16} {(max(cst_vals)-min(cst_vals)):.4f}")
    print(f"{'L1 阈值(0.707):':<16} 全部 {sum(c>=0.707 for c in cst_vals)}/{len(cst_vals)} 超越")
    print(f"{'L2 阈值(1.000):':<16} {sum(c>=1.0 for c in cst_vals)}/{len(cst_vals)} 超越")

    # ── 结论 ──
    all_l1 = all(get_level(c) >= "L1" or get_level(c) == "L1-信号整合"
                 for c in cst_vals)
    levels  = [r["level"] for r in results]
    l1_count = sum("L1" in l or "L2" in l or "L3" in l or "L4" in l
                   or "L5" in l or "L6" in l for l in levels)

    print(f"\n{'='*60}")
    print("结论：")
    print(f"  V_res 在 2~5mV 全范围内，CST ∈ [{min(cst_vals):.4f}, {max(cst_vals):.4f}]")
    print(f"  L1 阈值(0.707)：{l1_count}/{len(results)} 超越")
    if l1_count == len(results):
        print("  ✅ L1 结论对 V_res 估计完全鲁棒（2~5mV 全部达标）")
    else:
        print(f"  ⚠️ 部分 V_res 未达 L1，需说明")

    # ── 额外：连续扫描（用于绘图）──
    print(f"\n连续扫描（V_res=1~6mV，步长0.5mV）：")
    print(f"{'V_res':<8} {'α':<8} {'CST':<8}  等级")
    cont = []
    for vr_10 in range(10, 65, 5):   # 1.0~6.0 步长0.5
        vr    = vr_10 / 10
        meff  = V_range / vr
        alpha = math.log(meff)
        cst   = ScTc * math.exp(alpha * Gst)
        level = get_level(cst)
        print(f"  {vr:<6} {alpha:<8.4f} {cst:<8.4f}  {level}")
        cont.append({"V_res_mV": vr, "alpha": round(alpha,4),
                     "CST": round(cst,4), "level": level})

    # ── 保存 ──
    result = {
        "experiment":   "v35_alpha_sensitivity",
        "date":         "2026-09-02",
        "purpose":      "α区间鲁棒性验证，证明L1结论对V_res估计不敏感",
        "fixed_values": {"Sc": Sc, "Tc": Tc, "Gst": Gst,
                         "V_range_mV": V_range,
                         "V_range_src": "Lockery 2009 Curr.Biol.",
                         "V_res_base_mV": 3.0,
                         "V_res_src": "Liu et al. 2009 PNAS"},
        "scan_results": results,
        "continuous_scan": cont,
        "summary": {
            "CST_min": round(min(cst_vals), 4),
            "CST_max": round(max(cst_vals), 4),
            "L1_pass": f"{l1_count}/{len(results)}",
            "conclusion": "L1结论对V_res(2~5mV)完全鲁棒" if l1_count==len(results)
                          else "部分范围未达L1",
        },
        "data_sources": [
            {"param": "Sc=0.8350",  "src": "Varshney 2011 PLoS Comput Biol", "level": "S2"},
            {"param": "Tc=0.7711",  "src": "Randi2023(S1)+Kato/Schrodel/Nguyen+F-D bins", "level": "S1-S2"},
            {"param": "Gst=0.1096", "src": "Randi 2023 Nature 623:406",      "level": "S1"},
            {"param": "V_range=40mV","src": "Lockery 2009 Curr.Biol.",        "level": "S2"},
            {"param": "V_res=3mV",  "src": "Liu et al. 2009 PNAS",           "level": "S2"},
        ],
    }
    out = OUT_DIR / "v35_alpha_sensitivity_results.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 保存: {out}")
    return result

if __name__ == "__main__":
    main()
