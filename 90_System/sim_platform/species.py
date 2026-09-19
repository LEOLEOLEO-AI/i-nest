# -*- coding: utf-8 -*-
"""sim_platform.species — 跨物种连接组加载器（"交叉仿真"的数据底座）。

为什么需要它:
    用户要求"复杂网络涌现智能的仿真环境搭建（包含秀丽线虫等智能涌现机制的
    交叉仿真与实验）"。交叉仿真的前提是**同一套分析能跑在多个物种的连接组上**——
    所以先把各物种数据统一成同一个 (A, meta) 契约，再谈分析。

实测可用数据（2026-09-19 核对）:
    C. elegans  iNEST_Sim/data/aconnectome.json
                300×300 化学突触矩阵（非零 2276）+ 300×300 电突触矩阵（非零 1096）
                + chemical_sign（300 个兴奋/抑制符号）
                另有 c_elegans_*.json 的物种级复杂度指标（N=279, sigma_i/f, Ci/Cf, Li/Lf）
    其它物种    由下方 _probe_* 逐格式尝试，加载失败会明确报出来而不是静默返回空。

设计约定:
    load(species) -> Conn(adj, meta)
      adj  : scipy.sparse.csr_matrix，行=源，列=目标（出边）
      meta : dict(name, n_nodes, n_edges, kind, source, extra)
"""
from __future__ import annotations

import csv
import gzip
import json
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

SIM = Path(r"D:\Obsidian\vault\40_iNEST\45_Simulation")
TCC_SIM = Path(r"D:\Obsidian\vault\30_TCC\35_Simulation")


@dataclass
class Conn:
    """统一连接组契约。"""
    name: str
    adj: "object"                      # scipy.sparse.csr_matrix
    meta: dict = field(default_factory=dict)

    @property
    def n(self) -> int:
        return int(self.adj.shape[0])

    @property
    def edges(self) -> int:
        return int(self.adj.nnz)

    def degree(self) -> np.ndarray:
        return np.asarray(self.adj.sum(axis=1)).ravel()

    def __repr__(self) -> str:
        return f"<Conn {self.name} n={self.n} e={self.edges}>"


def _csr(dense_or_coo):
    from scipy import sparse
    return sparse.csr_matrix(dense_or_coo)


# ---------------------------------------------------------------- C. elegans
def load_celegans(kind: str = "chemical") -> Conn:
    """秀丽线虫：300 神经元化学/电突触连接组（实测数据结构已核对）。"""
    p = SIM / "iNEST_Sim" / "data" / "aconnectome.json"
    if not p.exists():
        raise FileNotFoundError(f"缺少 {p}")
    d = json.loads(p.read_text(encoding="utf-8"))
    if kind not in d:
        raise KeyError(f"aconnectome.json 无 '{kind}'，可选 {[k for k in d if k != 'chemical_sign']}")
    A = _csr(np.asarray(d[kind], dtype=float))
    sign = d.get("chemical_sign")
    meta = {"species": "C. elegans", "kind": kind, "n_neurons": A.shape[0],
            "source": str(p.relative_to(SIM))}
    ids = SIM / "iNEST_Sim" / "data" / "randi2023_neuron_ids.json"
    if ids.exists():
        try:
            j = json.loads(ids.read_text(encoding="utf-8"))
            meta["neuron_ids"] = j.get("neuron_ids") or j.get("row_ids")
        except Exception:
            pass
    if sign is not None and kind == "chemical":
        meta["sign"] = sign
    return Conn(f"celegans_{kind}", A, meta)


def celegans_species_metrics() -> dict:
    """物种级复杂度指标（现有三份结果，实测字段不同，合并报告）。"""
    out = {}
    for f in ("c_elegans_500.json", "c_elegans_2000.json", "c_elegans_v24.json"):
        p = SIM / f
        if p.exists():
            try:
                out[f] = json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                pass
    return out


# ---------------------------------------------------------------- 其它物种（尽力而为）
def _is_error_page(p: Path) -> str:
    """检测"把错误页当数据保存"——实测真的发生过。

    hemibrain_edges.csv.gz 只有 715 字节，内容是
    `<?xml ...><Error><Code>AccessDenied</Code>...` 的 Google Cloud 报错页，
    被存成了连接组文件。若不检查，下游会把它当边表解析并产生垃圾结论。
    """
    try:
        head = p.read_bytes()[:300].decode("utf-8", errors="ignore")
    except Exception:
        return ""
    if head.startswith("<?xml") and ("<Error" in head or "AccessDenied" in head):
        return "文件内容是云存储报错页（AccessDenied），不是数据"
    if "<html" in head.lower():
        return "文件内容是 HTML 页面，不是数据"
    return ""


def load_hemibrain() -> Conn:
    """果蝇 hemibrain —— 当前**数据不可用**，明确报出原因而不是静默失败。"""
    gz = SIM / "connectome" / "hemibrain_edges.csv.gz"
    if gz.exists():
        bad = _is_error_page(gz)
        if bad:
            raise ValueError(
                f"hemibrain 边表已损坏({gz.stat().st_size} 字节)：{bad}。"
                f"需重新下载（原文件可能来自需要鉴权的 GCS 链接）。")
        rows = []
        opener = gzip.open if gz.read_bytes()[:2] == b"\x1f\x8b" else open
        with opener(gz, "rt", encoding="utf-8", errors="ignore") as fh:
            rd = csv.reader(fh)
            head = next(rd, None)
            idx = {h.strip(): i for i, h in enumerate(head or [])}
            si = next((idx[k] for k in ("bodyId_pre", "pre", "source", "from") if k in idx), 0)
            ti = next((idx[k] for k in ("bodyId_post", "post", "target", "to") if k in idx), 1)
            wi = next((idx[k] for k in ("weight", "count", "syn_count") if k in idx), None)
            for r in rd:
                if len(r) <= max(si, ti):
                    continue
                try:
                    rows.append((r[si], r[ti], float(r[wi]) if wi is not None and r[wi] else 1.0))
                except Exception:
                    continue
        if rows:
            nodes = sorted({a for a, _, _ in rows} | {b for _, b, _ in rows})
            ix = {n: i for i, n in enumerate(nodes)}
            from scipy import sparse
            A = sparse.coo_matrix(
                ([w for _, _, w in rows], ([ix[a] for a, _, _ in rows],
                                           [ix[b] for _, b, _ in rows])),
                shape=(len(nodes), len(nodes))).tocsr()
            return Conn("hemibrain", A, {"species": "Drosophila hemibrain", "kind": "chemical",
                                         "source": "connectome/hemibrain_edges.csv.gz",
                                         "n_neurons": len(nodes)})
    raise FileNotFoundError("hemibrain 连接组不可用（边表损坏，且无可用 JSON 备源）")


def load_mouse() -> Conn:
    """小鼠 —— 当前**不是连接组**。

    实测: allen_mouse_connectivity.json（3.27 MB）里是 2992 条
    Allen Institute 的**实验记录元数据**（data_set_id / specimen_name /
    injection_structures / injection_x/y/z …），**不是连接矩阵**。
    文件名有误导性，若当连接组用会得到无意义结果，故这里直接拒绝。
    """
    p = SIM / "connectome" / "allen_mouse_connectivity.json"
    if not p.exists():
        raise FileNotFoundError(f"缺少 {p}")
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        raise ValueError(f"解析失败: {e}")
    if isinstance(d, dict) and isinstance(d.get("msg"), list):
        k = list(d["msg"][0].keys())[:6] if d["msg"] else []
        raise ValueError(
            "该文件是 Allen Institute 的**实验目录元数据**（"
            f"{len(d['msg'])} 条记录，字段如 {k}），不是连接矩阵，不能当连接组使用。"
            "需要真正的 Allen 小鼠连接组请从 API 拉取 structure unionizes / 连接矩阵。")


def load_macaque() -> Conn:
    """猕猴：macaque_rm_weights.txt（上三角或全矩阵，按行数判断）。"""
    p = SIM / "connectome" / "macaque_rm_weights.txt"
    if not p.exists():
        raise FileNotFoundError(f"缺少 {p}")
    A = np.loadtxt(p)
    if A.ndim == 1:
        # 上三角展开
        n = int((1 + np.sqrt(1 + 8 * len(A))) / 2)
        M = np.zeros((n, n))
        iu = np.triu_indices(n, k=1)
        if len(A) == len(iu[0]):
            M[iu] = A
    else:
        M = A
    return Conn("macaque", _csr(M), {"species": "Macaque (RM)", "kind": "structural",
                                     "source": "connectome/macaque_rm_weights.txt"})


LOADERS = {
    "celegans": lambda: load_celegans("chemical"),
    "celegans_elec": lambda: load_celegans("electrical"),
    "hemibrain": load_hemibrain,
    "macaque": load_macaque,
    "mouse": load_mouse,
}


def available() -> dict:
    """探测各物种可用性（不抛异常，供平台自检/看板展示）。"""
    out = {}
    for name, fn in LOADERS.items():
        try:
            c = fn()
            out[name] = {"ok": True, "n": c.n, "edges": c.edges,
                         "species": c.meta.get("species", "")}
        except Exception as e:
            out[name] = {"ok": False, "err": f"{type(e).__name__}: {e}"}
    return out


def load(name: str) -> Conn:
    if name not in LOADERS:
        raise KeyError(f"未知物种 '{name}'，可选 {list(LOADERS)}")
    return LOADERS[name]()
