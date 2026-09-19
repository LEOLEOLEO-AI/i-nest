# -*- coding: utf-8 -*-
"""sim_platform.metrics — 网络与动力学度量（涌现/临界性分析的核心算法）。

对应研究问题: "复杂网络涌现智能"的常见判据是**临界性**——
系统运行在 σ≈1 的临界点附近时，动态范围、信息容量与记忆容量同时最大。
本模块提供可复现的实现，而不是把结论写在注释里：

    graph_metrics(A)          网络层：密度/聚类/模块度/小世界性
    avalanche(A, ...)         动力学层：概率分支雪崩 -> <S>, <T>, 分支比 σ, 规模分布指数 τ
    criticality_sweep(A, ...) 扫增益找临界点（σ≈1 处），并给出动态范围
    fit_powerlaw(sizes)       离散幂律指数（Hill 估计量）

**证据等级 [仿真]**: 本模块产出的一切都只是仿真观测量，不构成因果或普适定律
（遵守 AGENTS.md §0.1）。所有实验固定随机种子。
"""
from __future__ import annotations

import numpy as np


# ---------------------------------------------------------------- 网络层
def graph_metrics(A) -> dict:
    """基础网络度量。用 networkx 计算聚类/模块度，其余用 scipy/numpy。"""
    import networkx as nx
    from scipy import sparse

    n = A.shape[0]
    edges = int(A.nnz)
    dens = edges / (n * (n - 1)) if n > 1 else 0.0
    G = nx.from_scipy_sparse_array(sparse.csr_matrix(A), create_using=nx.DiGraph)

    und = G.to_undirected()
    cc = nx.average_clustering(und) if und.number_of_nodes() > 2 else 0.0
    # 有向图的最短路径（取最大强连通分量，避免不连通导致的 inf）
    try:
        scc = max(nx.strongly_connected_components(G), key=len)
        pl = nx.average_shortest_path_length(G.subgraph(scc))
    except Exception:
        pl = float("nan")
    try:
        import networkx.algorithms.community as nxc
        comms = nxc.louvain_communities(und, seed=0)
        mod = nxc.modularity(und, comms)
        n_comm = len(comms)
    except Exception:
        mod, n_comm = float("nan"), 0

    # 小世界性: 与同规模同密度的 Erdos-Renyi 随机图比聚类/路径
    try:
        rnd = nx.gnp_random_graph(n, dens, seed=0, directed=False)
        cc_r = nx.average_clustering(rnd)
        small_world_sigma = (cc / cc_r) if cc_r > 0 else float("nan")
    except Exception:
        small_world_sigma = float("nan")

    deg = np.asarray(A.sum(axis=1)).ravel()
    return {
        "n_nodes": int(n), "n_edges": edges, "density": float(dens),
        "avg_clustering": float(cc), "avg_path_len_scc": float(pl),
        "modularity": float(mod), "n_communities": n_comm,
        "small_world_sigma": float(small_world_sigma),
        "degree_mean": float(deg.mean()), "degree_std": float(deg.std()),
        "degree_max": float(deg.max()),
    }


# ---------------------------------------------------------------- 动力学层
def _csr_prob(A, gain: float):
    """把连接权重转成"激活传播概率"矩阵: p_ij = clip(gain * w_ij, 0, 1)。"""
    from scipy import sparse
    A = sparse.csr_matrix(A, dtype=float)
    P = A.copy()
    P.data = np.clip(gain * P.data, 0.0, 1.0)
    return P


def avalanche(A, gain: float = 1.0, n_trials: int = 2000, seed: int = 0,
              max_steps: int = 2000) -> dict:
    """概率分支雪崩模型（神经元雪崩的标准简化）。

    过程: 随机选一个节点激活；每个被激活节点 i 以概率 p_ij 激活其出邻居 j；
          直到没有新节点被激活。记录每次雪崩的规模 S 与时长 T。

    返回 <S>, <T>, 规模分布指数 τ, 以及分支比估计 σ。
    σ 用「后代数/父代数」的比值估计：σ = <S>/<T>（临界时 σ→1）。
    """
    from scipy import sparse
    P = _csr_prob(A, gain)
    indptr, indices, data = P.indptr, P.indices, P.data
    n = P.shape[0]
    rng = np.random.default_rng(seed)

    sizes, durations = [], []
    # σ 的正确估计: 分支比 = 下一代规模 / 上一代规模（跨所有雪崩累计）。
    # 首版 bug（实测暴露）: 把"命中的邻居数"当作后代，但命中里包含**已被激活**的
    # 节点，而它们不会产生下一代。结果在最低增益下 σ 仍报 3.9（应当 →0），
    # 于是"临界增益"被误判到扫描区间的最左端，跨物种对照结论随之无效。
    # 正确做法: 只统计**新增激活**，并按代际比求 σ。
    tot_prev = tot_next = 0
    rng = np.random.default_rng(seed)

    for _ in range(n_trials):
        start = int(rng.integers(n))
        active = np.zeros(n, dtype=bool)
        active[start] = True
        frontier = np.array([start])
        S, T = 1, 1
        steps = 0
        while frontier.size and steps < max_steps:
            new = []
            for i in frontier:
                lo, hi = indptr[i], indptr[i + 1]
                if hi <= lo:
                    continue
                tgt, pr = indices[lo:hi], data[lo:hi]
                hit = tgt[rng.random(tgt.size) < pr]
                if hit.size:
                    new.append(hit)
            cand = (np.unique(np.concatenate(new)) if new else np.array([], dtype=int))
            cand = cand[~active[cand]]
            tot_prev += int(frontier.size)
            tot_next += int(cand.size)
            if cand.size == 0:
                break
            active[cand] = True
            S += int(cand.size)
            T += 1
            frontier = cand
            steps += 1
        sizes.append(S); durations.append(T)

    sizes = np.asarray(sizes); durations = np.asarray(durations)
    sigma = float(tot_next / max(tot_prev, 1))          # 代际分支比，临界时 →1
    tau = fit_powerlaw(sizes)
    return {
        "gain": float(gain), "n_trials": int(n_trials), "seed": int(seed),
        "mean_size": float(sizes.mean()), "mean_duration": float(durations.mean()),
        "max_size": int(sizes.max()),
        "branching_ratio_sigma": sigma,
        "size_exponent_tau": tau,
        "p_large_avalanche": float((sizes > sizes.mean() * 5).mean()),
    }


def fit_powerlaw(values: np.ndarray, xmin: float | None = None) -> float:
    """离散幂律指数 τ 的 Hill 估计（连续近似）。

    τ = 1 + n / Σ ln(x_i / xmin)，xmin 默认取最小值。
    仅用于**同一实验内不同参数之间的相对比较**，不声称精确拟合。
    """
    x = np.asarray(values, dtype=float)
    x = x[x > 0]
    if x.size < 20:
        return float("nan")
    xmin = float(xmin if xmin is not None else x.min())
    x = x[x >= xmin]
    if x.size < 20:
        return float("nan")
    return float(1.0 + x.size / np.sum(np.log(x / xmin)))


def criticality_sweep(A, gains=None, n_trials: int = 600, seed: int = 0) -> dict:
    """扫增益找临界点：σ 随增益单调上升，σ≈1 处即临界点。

    同时给"动态范围"（不同增益下响应强度的跨度），这是临界态的核心功能优势之一。
    """
    if gains is None:
        gains = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0]
    rows = [avalanche(A, g, n_trials=n_trials, seed=seed) for g in gains]
    sig = np.array([r["branching_ratio_sigma"] for r in rows])
    # 临界增益: σ 最接近 1 的那个
    k = int(np.argmin(np.abs(sig - 1.0)))
    sizes = np.array([r["mean_size"] for r in rows])
    dyn_range = float(np.log10(sizes.max() / max(sizes.min(), 1e-9)))
    return {"sweep": rows, "critical_gain": float(gains[k]),
            "sigma_at_critical": float(sig[k]),
            "dynamic_range_decades": dyn_range,
            "subcritical_gain": float(gains[0]),
            "supercritical_gain": float(gains[-1])}


def dynamic_range(A, gains=None, n_trials: int = 400, seed: int = 0) -> dict:
    """标准动态范围定义: Δ = 10·log10(响应最大 / 响应最小)，响应取平均雪崩规模。"""
    if gains is None:
        gains = list(np.logspace(-1, 0.7, 10))
    sizes = []
    for g in gains:
        sizes.append(avalanche(A, float(g), n_trials=n_trials, seed=seed)["mean_size"])
    sizes = np.asarray(sizes)
    if sizes.min() <= 0:
        return {"dynamic_range_db": float("nan"), "gains": gains, "sizes": sizes.tolist()}
    return {"dynamic_range_db": float(10 * np.log10(sizes.max() / sizes.min())),
            "gains": [float(g) for g in gains], "sizes": sizes.tolist()}


# ---------------------------------------------------------------- 交叉仿真
def cross_species(conns: dict, gain: float = 1.0, n_trials: int = 800,
                  seed: int = 0) -> dict:
    """把同一套度量同时跑在多个物种上 —— 这就是"交叉仿真"。

    conns: {name: Conn}
    返回每个物种的 graph_metrics + avalanche，便于横向比较涌现/临界行为差异。
    """
    out = {}
    for name, c in conns.items():
        try:
            gm = graph_metrics(c.adj)
            av = avalanche(c.adj, gain=gain, n_trials=n_trials, seed=seed)
            out[name] = {"species": c.meta.get("species", name),
                         "n": c.n, "edges": c.edges, "graph": gm, "dynamics": av}
        except Exception as e:
            out[name] = {"error": f"{type(e).__name__}: {e}"}
    return out
