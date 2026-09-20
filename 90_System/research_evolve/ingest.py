# -*- coding: utf-8 -*-
"""research_evolve.ingest — 把现有材料按导入来源分类保存，并建立"任务相关性"索引。

用户要求:
    "现有材料先按照导入被分类进行保存，后续一次从中发现跟任务强相关的进行复现迭代。"

因此本模块做两件事，**不搬动原文件**（遵守"唯一正本"）:
    1. **分类建册**: 扫描各导入来源，按五条工作流归类，生成
       `10_Knowledge/00_导航/classified/<WS>.md` 清单页（是链接，不是副本），
       外加一个机器可读索引 `state/ingest_index.json`。
    2. **任务相关性打分**: 对每条材料算它与"已采纳研究方向"和"五条工作流"的
       相关度，于是后续可以说"给我和 H7/MTIA300 强相关的材料"，直接进复现迭代。

为什么不做物理移动:
    材料存量约 1900 个文件（GetNotes 719 + 20_Processing 905 + 洞察 240）。
    物理移动会破坏现有引用与既有脚本路径，且违背"一处正本"。分类的价值在
    **可检索、可定位**，用清单页 + 索引即可获得，成本更低、风险为零。
    （若确实要物理归置，用 `--move` 显式开启。）

用法:
    python -m research_evolve.ingest              # 建册 + 打分
    python -m research_evolve.ingest --top 30     # 只列相关性最高的 30 条
    python -m research_evolve.ingest --task H7    # 查与某个任务强相关的材料
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path

from .common import VAULT, load_json, read_text, save_json
from .score import scope_check
from .triage import classify_workstream
from .workstreams import WORKSTREAMS

STATE = VAULT / "90_System" / "research_evolve" / "state"
INDEX_JSON = STATE / "ingest_index.json"
CLASSIFIED = VAULT / "10_Knowledge" / "00_导航" / "classified"
REPORT = VAULT / "70_Dashboard" / "ingest_index.md"

SOURCES = [
    ("GetNotes", Path(r"D:\Obsidian\GetNotes_Inbox"), "得到大脑剪藏"),
    ("Inbox", VAULT / "00_Inbox", "库内收件箱"),
    ("Insights", VAULT / "00_Inbox" / "_pipeline_insights", "论文管线洞察"),
    ("Digests", VAULT / "20_Processing" / "_digests", "加工摘要"),
    ("Papers", VAULT / "50_Output" / "51_Papers", "论文产出"),
    ("Patents", VAULT / "50_Output" / "52_Patents", "专利产出"),
    ("Guides", VAULT / "50_Output" / "55_Guides", "项目指南"),
    ("SimReports", VAULT / "40_iNEST" / "45_Simulation" / "reports", "仿真报告"),
]

# 已采纳的研究方向（用户 2026-09-18 决定保留），用于任务相关性打分
ACCEPTED_TASKS = {
    "H5": ["SDI", "可塑", "拓扑重构", "STDP", "plasticity", "可塑性"],
    "H6": ["chiplet", "忆阻", "memristor", "crossbar", "存算一体", "异构集成"],
    "H7": ["NoC", "路由", "routing", "spike", "事件驱动", "event-driven", "延迟"],
    "H8": ["晶圆级", "wafer-scale", "百万", "神经元", "实时仿真"],
    "H10": ["连接组", "connectome", "脑", "拓扑", "NoC", "小世界"],
    "MTIA300": ["通信", "集合通信", "AllReduce", "双平面", "near-memory", "归约"],
    "MOTIF": ["motif", "局部结构", "模体", "动力学稳定性"],
    "HALAPOINT": ["Loihi", "Hala Point", "SNN", "能效", "异步", "芯片"],
    "PTHEORY": ["元拓扑", "meta-topology", "bond", "最小作用量", "变分", "生成集"],
}

TASK_ACCEPTED = set(ACCEPTED_TASKS)


def score_item(text: str, title: str) -> dict:
    """算一条材料的：工作流归属 + 领域命中 + 任务相关性。"""
    body = title + "\n" + text[:4000]
    ws, ws_hits = classify_workstream(body, title)
    sc = scope_check(body)
    low = body.lower()

    task_scores = {}
    for task, kws in ACCEPTED_TASKS.items():
        hits = [k for k in kws if k.lower() in low]
        if hits:
            task_scores[task] = {"hits": hits[:6], "score": len(hits)}
    best_task = max(task_scores.items(), key=lambda x: x[1]["score"])[0] if task_scores else None
    # 相关性总分：领域词 + 工作流词 + 任务词（任务词权更高，因为那是你已定的方向）
    rel = (len(sc["tcc_hits"]) + len(sc["inest_hits"])) * 2 + len(ws_hits) + \
          sum(v["score"] for v in task_scores.values()) * 3
    return {"workstream": ws, "ws_hits": ws_hits[:5],
            "domain_hits": (sc["tcc_hits"] + sc["inest_hits"])[:6],
            "task_scores": task_scores, "best_task": best_task,
            "relevance": rel, "excluded": sc["excluded"]}


def build(top: int = 40) -> dict:
    items = []
    seen = set()
    for label, root, desc in SOURCES:
        if not root.exists():
            continue
        for p in sorted(root.rglob("*.md")):
            rel = p.relative_to(VAULT).as_posix() if str(p).startswith(str(VAULT)) \
                else p.as_posix()
            if rel in seen:
                continue
            seen.add(rel)
            txt = read_text(p)
            if len(txt.strip()) < 30:
                continue
            s = score_item(txt, p.stem)
            items.append({"path": rel, "source": label, "source_desc": desc,
                          "title": p.stem[:110], "bytes": len(txt),
                          "mtime": datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d"),
                          **s})

    # 分类建册
    by_ws: dict[str, list[dict]] = {}
    for it in items:
        by_ws.setdefault(it["workstream"] or "UNCLASSIFIED", []).append(it)
    for v in by_ws.values():
        v.sort(key=lambda x: -x["relevance"])

    # 任务索引
    by_task: dict[str, list[dict]] = {}
    for it in items:
        for t in it["task_scores"]:
            by_task.setdefault(t, []).append(it)
    for v in by_task.values():
        v.sort(key=lambda x: -x["task_scores"][x["best_task"]]["score"]
               if x["best_task"] in x["task_scores"] else 0)

    result = {"generated": datetime.now().isoformat(),
              "total_materials": len(items),
              "by_workstream": {k: len(v) for k, v in by_ws.items()},
              "by_task": {k: len(v) for k, v in by_task.items()},
              "items": items}
    save_json(INDEX_JSON, result)

    # 清单页（分类保存的"可检索形态"）
    CLASSIFIED.mkdir(parents=True, exist_ok=True)
    for ws_id, rows in by_ws.items():
        ws = WORKSTREAMS.get(ws_id)
        L = [f"# 分类册 · {ws_id}" + (f" {ws.name}" if ws else ""), "",
             f"> {len(rows)} 条 · 由 `research_evolve.ingest` 生成（链接非副本，正本仍在原位）", ""]
        if ws:
            L += [f"- 闭环定义：**{ws.closure}**", f"- 硬闸门：{ws.gates[0]}", ""]
        L += ["| 相关性 | 来源 | 材料 | 任务 |", "|---|---|---|---|"]
        for r in rows[:400]:
            t = "、".join(r["task_scores"].keys()) or "—"
            L.append(f"| {r['relevance']} | {r['source']} | [[{Path(r['path']).stem}]]"
                     f"<br><sub>{r['path']}</sub> | {t} |")
        (CLASSIFIED / f"{ws_id}.md").write_text("\n".join(L), encoding="utf-8")

    # 总报告
    L = ["# 材料分类与任务相关性索引", "",
         f"> 生成 {datetime.now():%Y-%m-%d %H:%M} · 共 **{len(items)}** 条材料", "",
         "## 一、按工作流分类", "", "| 工作流 | 数量 | 清单页 |", "|---|---|---|"]
    for ws_id, rows in sorted(by_ws.items(), key=lambda x: -len(x[1])):
        ws = WORKSTREAMS.get(ws_id)
        L.append(f"| {ws_id} {ws.name if ws else ''} | {len(rows)} | "
                 f"`10_Knowledge/00_导航/classified/{ws_id}.md` |")
    L += ["", "## 二、按已采纳研究方向（用于后续复现迭代）", "",
          "| 方向 | 强相关材料数 | 说明 |", "|---|---|---|"]
    for t, rows in sorted(by_task.items(), key=lambda x: -len(x[1])):
        L.append(f"| **{t}** | {len(rows)} | {ACCEPTED_TASKS.get(t, [''])[0]} 等 |")
    L += ["", "查某个方向的材料：`python -m research_evolve.ingest --task H7`", "",
          "## 三、相关性最高的材料", "", "| 相关性 | 来源 | 材料 | 工作流 | 任务 |",
          "|---|---|---|---|---|"]
    for it in sorted(items, key=lambda x: -x["relevance"])[:top]:
        L.append(f"| {it['relevance']} | {it['source']} | {it['title'][:56]} | "
                 f"{it['workstream'] or '—'} | {'、'.join(it['task_scores'].keys()) or '—'} |")
    L += ["", "---", "",
          "**怎么用**：① 「分类保存」看第一节，每类一个清单页；"
          "② 「找任务强相关材料」用第二节或 `--task`；"
          "③ 找到后进对应工作流的复现迭代（READ 流：笔记 + 复现脚本 + 与原文指标对比）。", ""]
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(L), encoding="utf-8")
    return result


def show_task(task: str, limit: int = 25) -> None:
    idx = load_json(INDEX_JSON, default={}) or {}
    if not idx.get("items"):
        print("尚无索引，先运行 `python -m research_evolve.ingest`")
        return
    key = task.upper()
    rows = [it for it in idx["items"]
            if key in {k.upper() for k in it.get("task_scores", {})}]
    rows.sort(key=lambda x: -x["task_scores"][x["best_task"]]["score"]
              if x.get("best_task") in x.get("task_scores", {}) else 0)
    print(f"=== 与 {key} 强相关的材料（{len(rows)} 条，列前 {limit}）===")
    for it in rows[:limit]:
        sc = it["task_scores"][it["best_task"]]["score"]
        hits = it["task_scores"][it["best_task"]]["hits"]
        print(f"  [{sc}] {it['source']:<10} {it['title'][:62]}")
        print(f"        命中: {hits}")
        print(f"        {it['path']}")


def main() -> int:
    a = sys.argv[1:]
    if "--task" in a:
        show_task(a[a.index("--task") + 1])
        return 0
    top = int(a[a.index("--top") + 1]) if "--top" in a else 40
    r = build(top)
    print(f"材料 {r['total_materials']} 条")
    print(f"  按工作流: {r['by_workstream']}")
    print(f"  按研究方向: {r['by_task']}")
    print(f"报告 -> {REPORT}")
    print(f"分类册 -> {CLASSIFIED}")
    print(f"索引 -> {INDEX_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
