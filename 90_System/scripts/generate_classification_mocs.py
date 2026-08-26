# -*- coding: utf-8 -*-
"""
基于 99_Meta/classification.json 生成两份 MOC：
  1) 60_MOC/10_Own_Research_Diagnosis.md  —— 自有研究现状诊断 + 后续计划
  2) 60_MOC/11_External_Literature_Index.md —— 外部爬取文献/平台索引
原则：含 刘勤让/inest研究组 = 自有研究(重点)；含文献名/平台名 = 爬取。
"""
import json, re
from collections import Counter, defaultdict
from pathlib import Path
from datetime import datetime

VAULT = Path(r"D:\obsidian\vault")
DATA = json.loads((VAULT / "99_Meta" / "classification.json").read_text(encoding="utf-8"))


def link(p):
    base = p[:-3] if p.endswith(".md") else p
    return f"[[{base.replace(chr(92), '/')}]]"


def date_from_path(p):
    m = re.search(r"(20\d{2}[-_]\d{2}[-_]\d{2})", p)
    if m:
        return m.group(1).replace("_", "-")
    m2 = re.search(r"20\d{2}\.\d{4,5}", p)
    if m2:
        return m2.group(0)
    return ""


def source_of(r):
    p = r["path"].lower()
    t = r["reason"].lower()
    if "getnote" in p or "得到" in t or "getnote" in t:
        return "得到 / getnote"
    if "genspark" in p or "genspark" in t:
        return "Genspark"
    if "codex" in p or "codex" in t:
        return "Codex"
    if "arxiv" in p or "arxiv" in t or "01_论文" in p or "papers" in p or "arxiv-daily" in p:
        return "arXiv / 学术文献"
    if "semantic" in t:
        return "Semantic Scholar"
    # 细筛新增：web-clips 剪藏 / 含 source 链接的网页导入
    if "web-clips" in t or "剪藏" in t or "category=剪藏" in t:
        return "网页剪藏 / Web-Clips"
    if "source 含链接" in t or "source 含" in t or "frontmatter source" in t:
        return "网页剪藏 / Web-Clips"
    return "其他平台 / 文献"


own_high = [r for r in DATA if r["provenance"] == "own" and r["confidence"] == "high"]
own_loc = [r for r in DATA if r["provenance"] == "own" and r["confidence"] in ("location", "location-dup")]
own_dup = [r for r in DATA if r["provenance"] == "own" and r["confidence"] == "location-dup"]
external = [r for r in DATA if r["provenance"] == "external"]
pending = [r for r in DATA if r["provenance"] == "pending"]

# ---------------- 1) 自有研究诊断 ----------------
def group_by_theme(recs):
    g = defaultdict(list)
    for r in recs:
        g[r["theme"]].append(r)
    return g

def status_breakdown(recs):
    c = Counter(r["status"] for r in recs)
    return dict(c)

STATUS_ACTION = {
    "project(项目)": "推进立项/申报书定稿与答辩准备；明确里程碑、负责人与经费节点。",
    "patent(专利)": "完善交底书，推进专利布局与申报流程，注意新颖性检索。",
    "paper(论文)": "推进投稿/返修；补充实验与最新文献对照，落实合作作者分工。",
    "meeting(纪要)": "把纪要中的决策与待办转化为可执行任务，落实到周计划。",
    "theory(理论/战略)": "将分散笔记整合为系统性论述/战略报告，形成可发表或可汇报的稿本。",
    "legacy(遗留)": "评估是否复活或正式归档，避免知识沉淀流失。",
    "archived(已归档)": "定期回顾，必要时迁出复用。",
    "active(常规)": "纳入周度复盘，保持持续演进。",
}

g_high = group_by_theme(own_high)
g_loc = group_by_theme(own_loc)

lines = []
lines.append(f"---\nprovenance: own\ntags: [MOC, 自有研究, 诊断, 计划]\n---\n")
lines.append("# 自有研究 · 现状诊断与后续计划\n")
lines.append(f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')} ｜ 数据源：`99_Meta/classification.json`")
lines.append(f"> 分类原则：**含「刘勤让 / inest研究组」等署名 = 我们的研究内容（重点）**；含文献名/第三方平台名 = 爬取内容。\n")

lines.append("## 一、总体盘点\n")
lines.append("| 类别 | 数量 | 说明 |")
lines.append("|---|---|---|")
lines.append(f"| 🔬 自有研究（高置信，含署名） | **{len(own_high)}** | 明确由本课题组产出的核心内容，本期重点诊断对象 |")
lines.append(f"| 📌 自有研究（位置候选，需复核） | {len(own_loc)} | 位于 TCC/iNEST/Output 但无署名，按位置启发式归为候选，建议人工复核 |")
lines.append(f"| 🌐 外部爬取内容 | {len(external)} | 含文献名/平台名（arXiv/得到/Genspark/Codex/S2…），作为参考来源 |")
lines.append(f"| ❓ 待审（无标记） | {len(pending)} | 位置启发式无法判定，留待人工审查 |\n")

lines.append("## 二、高置信自有研究 · 现状诊断\n")
lines.append("> 以下为明确由本课题组（刘勤让教授团队 / iNEST 研究组）产出的内容，按主题域分组。\n")

for theme in sorted(g_high, key=lambda k: -len(g_high[k])):
    recs = g_high[theme]
    sb = status_breakdown(recs)
    sb_text = "、".join(f"{k}×{v}" for k, v in sb.items())
    lines.append(f"### {theme}  （{len(recs)} 篇）\n")
    lines.append(f"- 状态分布：{sb_text}")
    # 最近活跃
    dates = [date_from_path(r["path"]) for r in recs if date_from_path(r["path"])]
    if dates:
        lines.append(f"- 文件名可见的最近时间标记：{max(dates)}")
    lines.append("- 代表条目：")
    for r in sorted(recs, key=lambda x: x["path"])[:8]:
        lines.append(f"  - {link(r['path'])} — {r['title'] or '(无标题)'}")
    if len(recs) > 8:
        lines.append(f"  - …（其余 {len(recs)-8} 篇见 `classification.json`）")
    lines.append("")

lines.append("## 三、后续计划（按状态优先级）\n")
lines.append("| 内容状态 | 建议后续动作 |")
lines.append("|---|---|")
for st, act in STATUS_ACTION.items():
    cnt = sum(1 for r in own_high if r["status"] == st)
    if cnt:
        lines.append(f"| {st} （{cnt} 篇） | {act} |")
lines.append("")

lines.append("### 重点方向（基于文件名推断，请核对）\n")
focus = [
    ("TCC 合作规划与软件定义晶上系统（SDSoC/SDSoW）", "30_TCC/31_Theory、34_Projects"),
    ("海河实验室重大专项（液态硬件 / TCC 战略版）申报", "30_TCC/34_Projects/海河实验室重大专项"),
    ("iNEST 学术信仰内核与三原理协同（FEP + 最小作用量 + STDP）", "40_iNEST/41_Theory"),
    ("专利布局（如 SDI 四规则自组织临界涌现方法）", "50_Output/52_Patents"),
    ("CST 基础理论论文投稿", "30_TCC/39_Legacy_TCC、论文相关"),
    ("组会与外部交流纪要跟进（复旦、天大、发改委汇报等）", "30_TCC/32_Technology、40_iNEST"),
]
for name, loc in focus:
    lines.append(f"- **{name}** — 相关目录：`{loc}`")
lines.append("")

lines.append("## 四、位置候选（需复核）\n")
lines.append(f"> 共 {len(own_loc)} 篇位于 TCC/iNEST/Output 但无署名标记，按位置启发式暂归为自有研究候选。"
             f"其中 {len(own_dup)} 篇因文件名带 `(1)/(2)` 等重复后缀、且含自有研究意图（建议/方案/折子/计划等）被保留为候选并打 `location-dup` 标记，"
             f"建议人工抽检后调整 `provenance`。另有 {sum(1 for r in DATA if r['provenance']=='pending')} 篇被移入「待审」（多为剪藏重复/导入痕迹）。\n")
for theme in sorted(g_loc, key=lambda k: -len(g_loc[k]))[:12]:
    recs = g_loc[theme]
    lines.append(f"- {theme}：{len(recs)} 篇")
lines.append("")

lines.append("## 五、关联索引\n")
lines.append(f"- 外部爬取文献索引：[[60_MOC/11_External_Literature_Index]]")
lines.append(f"- 全量分类数据：[[99_Meta/classification.json]]")
lines.append(f"- 重新分类脚本：[[90_System/scripts/classify_provenance.py]]")

(VAULT / "60_MOC" / "10_Own_Research_Diagnosis.md").write_text("\n".join(lines), encoding="utf-8")
print("✅ 60_MOC/10_Own_Research_Diagnosis.md 生成")

# ---------------- 2) 外部文献索引 ----------------
src_groups = defaultdict(list)
for r in external:
    src_groups[source_of(r)].append(r)

el = []
el.append(f"---\nprovenance: external\ntags: [MOC, 外部文献, 索引]\n---\n")
el.append("# 外部爬取内容 · 文献与平台索引\n")
el.append(f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')} ｜ 共 **{len(external)}** 篇爬取内容\n")
el.append("> 判定：含文献名 / 第三方平台名（arXiv、得到/getnote、Genspark、Codex、Semantic Scholar 等）= 从网上爬取，作为参考来源，区别于本组自有研究。\n")
el.append("## 按来源分布\n")
el.append("| 来源 | 数量 |")
el.append("|---|---|")
for s in sorted(src_groups, key=lambda k: -len(src_groups[k])):
    el.append(f"| {s} | {len(src_groups[s])} |")
el.append("")
for s in sorted(src_groups, key=lambda k: -len(src_groups[k])):
    recs = src_groups[s]
    el.append(f"## {s}（{len(recs)} 篇）\n")
    for r in sorted(recs, key=lambda x: x["path"])[:10]:
        el.append(f"- {link(r['path'])} — {r['title'] or '(无标题)'}")
    if len(recs) > 10:
        el.append(f"- …（其余 {len(recs)-10} 篇）")
    el.append("")
el.append("## 关联\n")
el.append(f"- 自有研究诊断：[[60_MOC/10_Own_Research_Diagnosis]]")

(VAULT / "60_MOC" / "11_External_Literature_Index.md").write_text("\n".join(el), encoding="utf-8")
print("✅ 60_MOC/11_External_Literature_Index.md 生成")
print(f"统计: own_high={len(own_high)} own_loc={len(own_loc)} external={len(external)} pending={len(pending)}")
