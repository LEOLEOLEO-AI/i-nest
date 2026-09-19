# -*- coding: utf-8 -*-
"""research_evolve.triage — 剪入内容的分诊闸门（解决"内容太多、有效太少"）。

诊断（实测 2026-09-19）:
    用户反馈"每日剪入的内容太多，但能对科研起到有效促进的内容太少"。
    实测各入口存量: GetNotes_Inbox 719 个文件、20_Processing 905、
    00_Inbox/_pipeline_insights 240 —— 合计约 1900 个**从未被处置**的条目。
    但抽查发现它们**并不都是垃圾**：里面有《拓扑中心计算网络底座项目建议书》
    《iNEST体系第一性原理诊断报告》《高端AI芯片晶上系统方案项目指标讨论会议》
    这类高价值材料。
    **所以真正缺的不是"少收"，而是"分诊"** —— 没有一步把输入判成
    「属于哪条工作流 / 现在能不能动手 / 不相关就明确拒掉」。

本模块做三件事:
    1. 判相关性（复用 .codex/research_keywords.yaml 的 TCC/iNEST 词表与排除词）
    2. 判工作流（五条流的关键词）
    3. 判可动手性，输出 **keep / park / reject** 三态：
         keep   —— 现在就该处理（进当日行动队列，数量要少）
         park   —— 相关但没有可执行动作（留档，不再重复打扰）
         reject —— 不相关/噪声（明确拒掉，并从后续扫描中排除）

产出:
    70_Dashboard/inbox_triage.md     人读：今天该处理哪几条 + 漏斗效果数字
    90_System/research_evolve/state/triage.json  机器态（含 reject 名单，避免反复扫）
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

from .common import VAULT, load_json, read_text, save_json
from .score import scope_check
from .workstreams import NOISE_PATTERNS, WORKSTREAMS

STATE = VAULT / "90_System" / "research_evolve" / "state" / "triage.json"
REPORT = VAULT / "70_Dashboard" / "inbox_triage.md"

# 分诊来源（入口层 + 未处置的加工层）
SOURCES = [
    ("GetNotes_Inbox", Path(r"D:\Obsidian\GetNotes_Inbox"), "得到大脑剪藏"),
    ("00_Inbox", VAULT / "00_Inbox", "库内收件箱"),
    ("_pipeline_insights", VAULT / "00_Inbox" / "_pipeline_insights", "论文管线洞察"),
    ("20_Processing/_digests", VAULT / "20_Processing" / "_digests", "加工摘要"),
]

SCAN_LIMIT = 4000
# 可动手信号：**必须**是"这份文档本身在推进某件事"，而不是"文中提到了这些词"。
# 实证教训: 首版把这些词放得很宽（含"报告""计划""实验""代码"），结果 891 条里
# 判出 261 条 keep —— 那等于没分诊，用户抱怨的正是"一次给太多"。
# 收紧为"交付物形态"与"显式待办"两类：
ACTIONABLE_STRONG = [
    # 显式待办标记（最强）
    "- [ ]", "[ ]", "TODO", "待办", "待补", "未完成", "下一步", "行动项",
    # 交付物形态（文档本身就是成果）
    "建议书", "任务书", "指南", "交底书", "初稿", "草稿", "草拟",
    "draft", "proposal", "spec", "checklist", "评审意见", "rebuttal",
]
# 显式待办的行内标记（用于加权）
TODO_LINE_RE = re.compile(r"^\s*[-*]\s*\[[ xX]\]|^\s*(?:TODO|待办|行动项)\s*[:：]", re.M)
# 模板与"信息流"类：**不是交付物**，不该进"今天处理"。
# 实测教训: 收紧动作词后，排名前两位变成 `_TEMPLATE_digest` 和
# `2026-08-02_arXiv日报_9篇` —— 它们含 `[ ]` 与 `draft` 字样，被误判成待办。
# 模板是空壳，日报是喂料，两者都属参考材料。
FEED_OR_TEMPLATE_RE = re.compile(
    r"(?i)_?template|模板|日报|周报|月报|digest|index$|^index|汇总|目录$|台账$")
DAILY_CAP = 15          # "今天该处理"的硬上限——分诊的意义就是只看几条


def classify_workstream(text: str, title: str = "") -> tuple[str | None, list[str]]:
    """按五条流的关键词判归属。返回 (流id, 命中词)。

    **标题优先是字典序，不是加权**（两次实测教训）:
      首版按全文命中数取最大 -> 《…项目指南建议》被判成 CODE（正文里
      "算法/实现/验证/性能"远多于"指南"）。
      第二版给标题 ×3 权重 -> **仍然**被判成 CODE，因为一部长篇指南的正文
      可以命中十来个 CODE 词，3 分权重根本压不住。
      结论：标题是**文档性质**的判据，正文只是**内容领域**的判据。
      故改为先比标题命中数，标题打平才比正文 —— 字典序，不是加权。
    """
    low_t, low_b = title.lower(), text.lower()
    best, best_hits, best_key = None, [], (-1, -1)
    for ws in WORKSTREAMS.values():
        th = [k for k in ws.keywords if k.lower() in low_t]
        bh = [k for k in ws.keywords if k.lower() in low_b and k not in th]
        key = (len(th), len(bh))
        if key > best_key:
            best, best_key = ws.id, key
            best_hits = th + bh
    return best, best_hits


def noise_hits(text: str) -> list[str]:
    return [n for n in NOISE_PATTERNS if n in text]


def triage_one(rel: str, title: str, text: str) -> dict:
    """对单个条目分诊。"""
    body = (title + "\n" + text[:3000])
    sc = scope_check(body)
    ws, ws_hits = classify_workstream(body, title)
    noise = noise_hits(body)
    strong = [a for a in ACTIONABLE_STRONG if a.lower() in body.lower()]
    todo_lines = len(TODO_LINE_RE.findall(text[:8000]))
    is_feed = bool(FEED_OR_TEMPLATE_RE.search(Path(rel).stem))

    in_domain = bool(sc["tcc_hits"] or sc["inest_hits"])
    excluded = sc["excluded"]
    domain_n = len(sc["tcc_hits"]) + len(sc["inest_hits"])

    # 优先级分：领域命中 + 流命中 + 强动作信号 + 实际待办条目
    rank = domain_n * 2 + len(ws_hits) + len(strong) * 3 + min(todo_lines, 10) * 2
    if is_feed:
        rank -= 20          # 模板/日报类压到底

    if excluded or (noise and not in_domain):
        verdict, why = "reject", (
            f"命中排除词 {sc['exclusion_hits'][:3]}" if excluded
            else f"噪声信号 {noise[:3]} 且无 TCC/iNEST 领域词")
    elif is_feed:
        verdict, why = "park", "模板/日报类：是喂料或空壳，不是交付物"
    elif in_domain and ws and strong:
        verdict, why = "keep", (f"{ws} 相关(命中 {ws_hits[:3]})；含交付物/待办信号 "
                                f"{strong[:3]}" + (f"；{todo_lines} 个待办条目" if todo_lines else ""))
    elif in_domain:
        verdict, why = "park", (f"领域相关(命中 {(sc['tcc_hits']+sc['inest_hits'])[:3]})"
                                f"但**不是待办或交付物**，属参考材料")
    else:
        verdict, why = "park", "未命中 TCC/iNEST 词表，暂不处理"

    return {"path": rel, "title": title[:110], "verdict": verdict, "why": why,
            "workstream": ws, "ws_hits": ws_hits[:5], "rank": rank,
            "domain_hits": (sc["tcc_hits"] + sc["inest_hits"])[:5],
            "strong": strong[:5], "todo_lines": todo_lines, "bytes": len(text)}


def scan() -> tuple[list[dict], dict]:
    prev = load_json(STATE, default={}) or {}
    already_rejected = set(prev.get("rejected_paths", []))
    results, counts, per_ws = [], {}, {}
    seen = 0
    for label, root, desc in SOURCES:
        if not root.exists():
            continue
        for p in sorted(root.rglob("*.md")):
            if seen >= SCAN_LIMIT:
                break
            seen += 1
            try:
                rel = p.relative_to(VAULT).as_posix()
            except ValueError:
                rel = p.as_posix()
            if rel in already_rejected:
                counts["reject(已判)"] = counts.get("reject(已判)", 0) + 1
                continue
            txt = read_text(p)
            if not txt.strip():
                continue
            r = triage_one(rel, p.stem, txt)
            r["source"] = label
            results.append(r)
            counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
            if r["verdict"] == "keep" and r["workstream"]:
                per_ws[r["workstream"]] = per_ws.get(r["workstream"], 0) + 1
    return results, {"counts": counts, "per_workstream": per_ws, "scanned": seen}


def write_report(results: list[dict], stats: dict) -> None:
    keeps_all = [r for r in results if r["verdict"] == "keep"]
    # 关键一步：keep 里再分「今天」与「积压」，今天有硬上限。
    # 分诊的目的不是让人看更多，而是让人**只看几条**。
    keeps_sorted = sorted(keeps_all, key=lambda r: -r.get("rank", 0))
    # 同名归并：库里存在大量 `X.md` / `X_2.md` / `X（1）.md` 的副本对，
    # 不合并的话"今天 15 条"里会有一半是同一份东西，白白占用注意力配额。
    def norm_title(t: str) -> str:
        return re.sub(r"(?i)[\s_\-—（）()【】\[\]\.]|_?\d+$|_?dup\d*$", "", t).lower()[:60]
    grouped: dict[str, dict] = {}
    for r in keeps_sorted:
        k = norm_title(r["title"])
        if k in grouped:
            grouped[k]["dupes"] = grouped[k].get("dupes", 0) + 1
            grouped[k].setdefault("dupe_paths", []).append(r["path"])
        else:
            r["dupes"] = 0
            r["dupe_paths"] = []
            grouped[k] = r
    uniq = list(grouped.values())
    today = uniq[:DAILY_CAP]
    backlog = uniq[DAILY_CAP:]
    parks = [r for r in results if r["verdict"] == "park"]
    rejects = [r for r in results if r["verdict"] == "reject"]
    c = stats["counts"]

    L = ["# 收件箱分诊 · 今天只看这一页", "",
         f"> 生成 {datetime.now():%Y-%m-%d %H:%M} · 由 `research_evolve.triage` 自动分诊",
         "",
         "## 一、漏斗效果（这就是「内容太多、有效太少」的解法）", "",
         "| 结果 | 数量 | 含义 |", "|---|---|---|",
         f"| 扫描入口条目 | {stats['scanned']} | GetNotes / 00_Inbox / 管线洞察 |",
         f"| **今天处理（硬上限 {DAILY_CAP}）** | **{len(today)}** | 领域相关 + 是交付物或含显式待办 |",
         f"| 积压（同类，排在后面） | {len(backlog)} | 处理完今天的再看 |",
         f"| park（参考材料，不动手） | {len(parks)} | 留档，不再重复打扰 |",
         f"| reject（不相关/噪声） | {len(rejects)} + {c.get('reject(已判)', 0)} 已判 | 明确拒掉并记住 |",
         "",
         f"> **{stats['scanned']} 条输入 → 今天 {len(today)} 条。**"
         f"这个比例才是分诊要的效果；如果你觉得还是多，把 `DAILY_CAP` 再调小。", ""]

    L += [f"## 二、今天处理这 {len(today)} 条", ""]
    for i, it in enumerate(today, 1):
        ws = WORKSTREAMS.get(it["workstream"] or "")
        L.append(f"### {i}. [{it['workstream']}] {it['title']}")
        L.append("")
        L.append(f"- **文件**：`{it['path']}`")
        L.append(f"- **为什么是它**：{it['why']}")
        L.append(f"- **优先级分**：{it.get('rank', 0)}"
                 f"（领域命中 {len(it.get('domain_hits', []))} · 流命中 {len(it.get('ws_hits', []))}"
                 f" · 待办条目 {it.get('todo_lines', 0)}）")
        if ws:
            L.append(f"- **这条流的闭环**：{ws.closure}")
            L.append(f"- **做完前要过**：{ws.gates[0]}")
        if it.get("dupes"):
            L.append(f"- ⚠ 另有 **{it['dupes']}** 个同名副本，建议合并后再处理："
                     + "、".join(f"`{p}`" for p in it["dupe_paths"][:3]))
        L.append(f"- [ ] 处理")
        L.append("")

    L += ["## 三、按工作流分布（今天 + 积压）", "", "| 工作流 | 今天 | 积压 |", "|---|---|---|"]
    for ws_id in WORKSTREAMS:
        t = sum(1 for r in today if r["workstream"] == ws_id)
        b = sum(1 for r in backlog if r["workstream"] == ws_id)
        ws = WORKSTREAMS[ws_id]
        L.append(f"| {ws_id} {ws.name} | {t} | {b} |")
    L.append("")

    if rejects:
        L += ["## 四、已拒（样本，避免这些再占用注意力）", ""]
        for r in rejects[:15]:
            L.append(f"- ~~{r['title'][:70]}~~ — {r['why']}")
        if len(rejects) > 15:
            L.append(f"- … 共 {len(rejects)} 条")
        L.append("")

    L += ["---", "",
          "**用法**：每天只打开第二节。处理完打勾，明天的分诊会自动把积压顶上来。",
          "reject 名单记在 `state/triage.json`，下轮扫描直接跳过。", ""]

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(L), encoding="utf-8")
    stats["today"] = len(today)
    stats["backlog"] = len(backlog)


def main() -> int:
    print("分诊中（扫描各入口）...")
    results, stats = scan()
    write_report(results, stats)
    prev = load_json(STATE, default={}) or {}
    rejected = sorted(set(prev.get("rejected_paths", [])) |
                      {r["path"] for r in results if r["verdict"] == "reject"})
    save_json(STATE, {
        "updated": datetime.now().isoformat(),
        "stats": stats,
        "rejected_paths": rejected,
        "keep": [r for r in results if r["verdict"] == "keep"],
        "park_count": sum(1 for r in results if r["verdict"] == "park"),
    })
    c = stats["counts"]
    print(f"扫描 {stats['scanned']} 条 -> keep {c.get('keep',0)} / "
          f"park {c.get('park',0)} / reject {c.get('reject',0)}")
    print(f"报告 -> {REPORT}")
    print(f"按工作流: {stats['per_workstream']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
