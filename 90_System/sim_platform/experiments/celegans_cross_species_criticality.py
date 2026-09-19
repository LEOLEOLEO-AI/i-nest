# -*- coding: utf-8 -*-
"""实验: 跨物种临界性交叉仿真（C. elegans 为主，含其它物种对照）。

研究问题: "复杂网络涌现智能"常以**临界性**为判据 —— 系统在 σ≈1 附近时
动态范围/信息容量最大。本实验把同一套度量同时跑在多个生物连接组上，
看临界行为是否跨物种一致（这就是"交叉仿真"的落点）。

证据等级: [仿真]。
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from sim_platform import metrics as M  # noqa: E402
from sim_platform import species as S  # noqa: E402

EXP_ID = "celegans_cross_species_criticality"
TITLE = "跨物种连接组临界性交叉仿真（秀丽线虫/果蝇/猕猴）"


def _gain_grid(cfg: dict) -> list[float]:
    lo, hi, n = cfg["gain_lo"], cfg["gain_hi"], cfg["gain_n"]
    return [round(lo + (hi - lo) * i / (n - 1), 4) for i in range(n)]


def experiment(config: dict, seed: int) -> dict:
    """纯函数式：给定 config + seed 必须可复现。"""
    wanted = config.get("species", ["celegans", "celegans_elec", "hemibrain", "macaque"])
    conns = {}
    skipped = {}
    for name in wanted:
        try:
            conns[name] = S.load(name)
        except Exception as e:
            skipped[name] = f"{type(e).__name__}: {e}"

    gains = _gain_grid(config)
    out = {
        "evidence": "[仿真]",
        "note": "所有数值为仿真观测量，不构成实测结论或普适定律",
        "seed": seed,
        "species_loaded": {k: {"n": v.n, "edges": v.edges,
                               "species": v.meta.get("species", "")}
                           for k, v in conns.items()},
        "species_skipped": skipped,
        "gains": gains,
        "per_species": {},
    }

    for name, c in conns.items():
        gm = M.graph_metrics(c.adj)
        sweep = M.criticality_sweep(c.adj, gains=gains,
                                    n_trials=config["n_trials"], seed=seed)
        rec = {
            "graph": gm,
            "critical_gain": sweep["critical_gain"],
            "sigma_at_critical": sweep["sigma_at_critical"],
            "dynamic_range_decades": sweep["dynamic_range_decades"],
            "sigma_by_gain": [{"gain": r["gain"], "sigma": r["branching_ratio_sigma"],
                               "mean_size": r["mean_size"],
                               "tau": r["size_exponent_tau"]} for r in sweep["sweep"]],
        }
        out["per_species"][name] = rec

    # 交叉对照：临界点的 σ 与动态范围是否跨物种一致
    if len(out["per_species"]) >= 2:
        sig = [v["sigma_at_critical"] for v in out["per_species"].values()]
        dr = [v["dynamic_range_decades"] for v in out["per_species"].values()]
        # 有限尺度饱和检测：若 <S> 在高增益段顶到 N（覆盖全网），σ≈1 是
        # **有限尺度效应**而非临界的证据。必须把这一点标出来，否则会把
        # "雪崩铺满整张图"误读成"系统处于临界态"。
        saturated = []
        for name, r in out["per_species"].items():
            nn = r["graph"]["n_nodes"]
            tail = r["sigma_by_gain"][-3:]
            if tail and all(t["mean_size"] > 0.55 * nn for t in tail):
                saturated.append(name)
        out["cross_species"] = {
            "n_species": len(sig),
            "sigma_at_critical_mean": sum(sig) / len(sig),
            "sigma_spread": max(sig) - min(sig),
            "dynamic_range_mean": sum(dr) / len(dr),
            "consistent_criticality": (max(sig) - min(sig)) < 0.35,
            "finite_size_saturated": saturated,
            "interpretation": (
                "各物种 σ 接近 1，**但注意**：" + "、".join(saturated)
                + " 的高增益段 <S> 已顶到节点总数，σ≈1 属**有限尺度饱和**，"
                  "不构成临界性的证据 [仿真]"
                if saturated else
                ("各物种在各自临界增益处的 σ 接近 1 且彼此接近，"
                 "初步支持临界性作为跨物种的共同组织原则 [仿真]")),
        }
        out["limitations"] = [
            "σ 用代际分支比估计；N 较小时雪崩会铺满全图导致 σ 饱和，"
            "标准做法需**子采样**（只统计随机取样的部分节点）或做有限尺度标度（多 N 对比），"
            "本实验尚未实现，故 σ≈1 不能直接当作临界态证据。",
            "幂律指数 τ 仅用于同一实验内不同增益之间的相对比较，"
            "未做 KS 检验，不声称精确拟合。",
            "所有数值为 [仿真] 观测量，不构成实测结论或普适定律（AGENTS.md §0.1）。",
        ]
    # 顺带带上已有的物种级复杂度指标（若存在）
    cm = S.celegans_species_metrics()
    if cm:
        out["existing_celegans_metrics"] = cm
    return out


DEFAULT_CONFIG = {
    "species": ["celegans", "celegans_elec", "macaque"],
    # 增益范围要能**夹住** σ=1。首版上限 3.0、下限 0.25 且 σ 估计有 bug，
    # 导致"临界点"落在区间最左端 —— 改小下限并加密网格，让 σ 真正穿越 1。
    "gain_lo": 0.02, "gain_hi": 1.5, "gain_n": 10,
    "n_trials": 400,
}


if __name__ == "__main__":
    from sim_platform import harness as H
    r = H.run(EXP_ID, experiment, DEFAULT_CONFIG, seed=0, title=TITLE)
    print(f"run {r.run_id} status={r.manifest['status']} "
          f"result_hash={r.manifest['result_hash']}")
    print(f"报告 -> {r.out_dir/'report.md'}")
