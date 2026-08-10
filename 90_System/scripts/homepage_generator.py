#!/usr/bin/env python3
"""
homepage_generator.py — Auto-generate Home.md from live vault + wiki state
Called by pipeline after all evolution engines complete.
"""
import json, os, sys, subprocess, re
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime
from collections import defaultdict

VAULT = Path(r"D:\Obsidian\vault")
STATE_FILE = VAULT / "99_Meta" / "research_state.json"
WIKI = VAULT / "wiki"
HOME = VAULT / "Home.md"
TODAY = datetime.now().strftime("%Y-%m-%d")
NOW = datetime.now().strftime("%Y-%m-%d %H:%M")

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def count_md(d):
    if d.exists():
        return len([f for f in d.rglob('*.md') if not f.name.startswith('.')])
    return 0

def count_wiki_concepts():
    concepts_dir = WIKI / "concepts"
    if not concepts_dir.exists():
        return {"tcc": 0, "inest": 0, "cross": 0, "total": 0}
    tcc = inest = cross = 0
    for f in concepts_dir.glob("*.md"):
        c = f.read_text(encoding='utf-8')
        if "**Domain**: TCC" in c:
            tcc += 1
        elif "**Domain**: iNEST" in c:
            inest += 1
        elif "**Domain**: Cross" in c:
            cross += 1
    return {"tcc": tcc, "inest": inest, "cross": cross, "total": tcc + inest + cross}

def read_bridges():
    """Read top cross-domain bridges"""
    bridge_file = WIKI / "cross_domain_insights.md"
    if not bridge_file.exists():
        return []
    content = bridge_file.read_text(encoding='utf-8')
    bridges = []
    for block in content.split("### ")[1:]:
        lines = block.strip().split("\n")
        if not lines:
            continue
        name_strength = lines[0]
        if "(Strength:" in name_strength:
            name = name_strength.split("(Strength:")[0].strip()
            strength = name_strength.split("Strength:")[1].split(")")[0].strip()
            insight = lines[1] if len(lines) > 1 else ""
            bridges.append({"name": name, "strength": strength, "insight": insight})
    return bridges[:3]

def read_pipeline_status():
    status_file = VAULT / "60_MOC" / "07_Pipeline_Status.md"
    if not status_file.exists():
        return "unknown"
    content = status_file.read_text(encoding='utf-8')
    if "paused" in content.lower():
        return "⚠️ paused"
    if "running" in content.lower():
        return "✅ running"
    return "❓ unknown"

def read_hypotheses():
    hyp_file = VAULT / "99_Meta" / "hypothesis_registry.json"
    if not hyp_file.exists():
        return []
    try:
        data = json.loads(hyp_file.read_text(encoding='utf-8'))
        return data.get("hypotheses", [])
    except:
        return []

def read_git_status():
    # 实时读取 git 工作树未提交改动（缓存易过期，故优先实时计算）
    try:
        r = subprocess.run(
            ["git", "-C", str(VAULT), "status", "--porcelain"],
            capture_output=True, text=True, timeout=30,
        )
        if r.returncode == 0:
            n = len([l for l in r.stdout.splitlines() if l.strip()])
            return n
    except Exception:
        pass
    # 回退到缓存状态文件
    state_file = VAULT / "99_Meta" / "research_state.json"
    if not state_file.exists():
        return 0
    try:
        data = json.loads(state_file.read_text(encoding='utf-8'))
        return data.get("git", {}).get("uncommitted", 0)
    except:
        return 0

# ============================================================
# Phase 5 仪表盘：演化追踪 / 任务推荐 / 健康检查
# ============================================================

def read_self_evolve_trend(n=10):
    """读取 99_Meta/self_evolve_log.json 近期断链/孤儿/缺FM 趋势。"""
    logf = VAULT / "99_Meta" / "self_evolve_log.json"
    if not logf.exists():
        return []
    try:
        data = json.loads(logf.read_text(encoding="utf-8"))
    except Exception:
        return []
    rows = []
    for e in data[-n:]:
        h = e.get("steps", {}).get("health", {})
        rows.append({
            "date": e.get("date", "?"),
            "broken": h.get("broken_links"),
            "orphan": h.get("orphan_notes"),
            "missing_fm": h.get("missing_frontmatter"),
        })
    return rows

def read_task_recommendations(top=5):
    """读取 wiki/task_recommendations.md 的优先级任务。"""
    f = WIKI / "task_recommendations.md"
    if not f.exists():
        return []
    txt = f.read_text(encoding="utf-8")
    items = []
    for line in txt.splitlines():
        m = re.match(r"###\s+\d+\.\s+\[(\w+)\]\s+(.*)", line)
        if m:
            items.append((m.group(1), m.group(2).strip()))
    items.sort(key=lambda x: 0 if x[0] == "HIGH" else (1 if x[0] == "MEDIUM" else 2))
    return items[:top]

def read_health_summary():
    """读取 99_Meta/vault_health.md 的数字指标。"""
    f = VAULT / "99_Meta" / "vault_health.md"
    if not f.exists():
        return {}
    s = {}
    for line in f.read_text(encoding="utf-8").splitlines():
        m = re.match(r"- (.+?):\s+\*\*(\d+)\*\*", line)
        if m:
            s[m.group(1)] = int(m.group(2))
    return s

def generate():
    log("=== Homepage Generator ===")
    
    # Gather data
    total_md = count_md(VAULT)
    inbox = count_md(VAULT / "00_Inbox")
    processing = count_md(VAULT / "20_Processing")
    tcc_files = count_md(VAULT / "30_TCC")
    inest_files = count_md(VAULT / "40_iNEST")
    output_files = count_md(VAULT / "50_Output")
    
    wiki = count_wiki_concepts()
    articles_count = len(list((WIKI / "articles").glob("*.md"))) if (WIKI / "articles").exists() else 0
    bridges = read_bridges()
    pipeline_status = read_pipeline_status()
    hypotheses = read_hypotheses()
    git_uncommitted = read_git_status()
    
    # 溯源归类统计（classify_provenance.py 产出）
    cls_file = VAULT / "99_Meta" / "classification.json"
    own_total = ext_total = 0
    if cls_file.exists():
        try:
            cls = json.loads(cls_file.read_text(encoding="utf-8"))
            own_total = sum(1 for r in cls if r.get("provenance") == "own")
            ext_total = sum(1 for r in cls if r.get("provenance") == "external")
        except Exception:
            pass
    
    # Build status emojis
    h_emojis = {"proven": "✅", "under_investigation": "🔬", "proposed": "📋", "pending": "⏳"}

    # ---- Phase 5 仪表盘新增：演化追踪 / 任务推荐 / 健康检查 ----
    trend = read_self_evolve_trend(10)
    trend_md = (
        "| 日期 | 断链 | 孤儿 | 缺FM |\n|---|---|---|---|\n"
        + "\n".join(f"| {r['date']} | {r['broken']} | {r['orphan']} | {r['missing_fm']} |" for r in trend)
    ) if trend else "（暂无历史记录，运行 self_evolve 后生成）"
    tasks = read_task_recommendations(5)
    tasks_md = (
        "| 优先级 | 建议 |\n|---|---|\n"
        + "\n".join(f"| {p} | {t} |" for p, t in tasks)
    ) if tasks else "（暂无推荐，运行 task_recommender 后生成）"
    hs = read_health_summary()
    health_md = (
        f"- 真正断链：**{hs.get('真正断链(目标不存在)')}**  ·  "
        f"孤儿笔记：**{hs.get('孤儿笔记(无入链)')}**  ·  "
        f"缺 frontmatter：**{hs.get('缺 frontmatter 笔记')}**"
    )
    
    # Build bridges section
    bridges_md = ""
    for i, b in enumerate(bridges):
        bridges_md += f"| {i+1} | **{b['name'].replace('_', ' × ')}** | {b['strength']} | {b['insight'][:80]} |\n"
    
    # Build hypotheses section
    hyp_md = ""
    for h in hypotheses:
        h_id = h.get("id", "?")
        h_title = h.get("title", "")
        h_status = h.get("status", "unknown")
        h_emoji = h_emojis.get(h_status, "❓")
        hyp_md += f"| {h_id} | {h_title[:60]} | {h_emoji} {h_status} |\n"
    
    content = f"""---
cssclass: dashboard
---

# 🔬 TCC × iNEST 自进化研发中枢

> **知识库状态：活跃** | 管线：{pipeline_status} | Git: {git_uncommitted} uncommitted | 更新：{NOW}

---

## 📊 今日快照

| 维度 | 数值 | 入口 |
|---|---|---|
| 📄 知识库总文件 | **{total_md:,}** | [[Home\\|根目录/Home]] |
| 🔬 TCC 资料 | **{tcc_files:,}** | [[30_TCC/TCC_Master_Index\\|TCC 主索引]] |
| 🧠 iNEST 资料 | **{inest_files:,}** | [[40_iNEST/iNEST_Master_Index\\|iNEST 主索引]] |
| 📥 待处理论文 | **{inbox}** | [[00_Inbox/_pipeline_insights/Index\\|论文收件箱]] |
| ⚙️ 处理中 | **{processing}** | [[20_Processing\\|处理区]] |
| 📤 成果区 | **{output_files}** | [[50_Output\\|50_Output 成果区]] |

---

## 🧬 Wiki 知识演化

| 维度 | 数值 | 变化 |
|---|---|---|
| 🏷️ 概念总数 | **{wiki['total']}** | TCC={wiki['tcc']}, iNEST={wiki['inest']}, Cross={wiki['cross']} |
| 📝 编译文章 | **{articles_count}** | raw/ → wiki/articles/ |
| 🌉 跨域桥梁 | **{len(bridges)}** | 强度 {'/'.join(b['strength'] for b in bridges[:3])} |

**入口**：[[wiki/index|Wiki 概念索引]] · [[wiki/health|知识健康报告]] · [[wiki/cross_domain_insights|跨域洞察]] · [[wiki/task_recommendations|任务推荐]]

---

## 🌉 跨域桥梁 TOP 3

| # | 桥梁 | 强度 | 核心洞察 |
|---|---|---|---|
{bridges_md}
> 全部桥梁 → [[wiki/cross_domain_insights|跨域洞察完整报告]]

---

## 🎯 今日行动

>[!important] 并行主线
>1. **[论文]** CST 智能涌现 — 修订 Section 4+5 → 投 Engineering
>2. **[论文]** TCC P-Paradigm 拓扑中心计算 → 投 Engineering  
>3. **[专利]** TCC 架构 + 实现专利 — 申报
>4. **[工程]** CST 仿真实验 — SDI N=1024 相位扫描

>[!tip] 知识库维护
>- [[wiki/task_recommendations|查看自动推荐任务]]
>- [[60_MOC/07_Pipeline_Status|管线状态]]：`{pipeline_status}`
>- Git：{git_uncommitted} uncommitted changes

**入口**：[[60_MOC/03_Daily_Action|每日行动]] · [[60_MOC/04_Daily_Focus|今日焦点]] · [研发看板（浏览器打开）](http://127.0.0.1:8899/vault/70_Dashboard/index.html)

---

## 🔄 并行研发双轨

### TCC：拓扑中心计算

| 层级 | 推进 | 证据要求 |
|---|---|---|
| 理论 | P-Paradigm：拓扑作为计算原语 | 定义、定理、推导、引用和反例 |
| 技术 | SDI/NoC/Chiplet/晶上互连拓扑 | 拓扑参数、路由策略、复杂度和对照组 |
| 工程 | CST 仿真、FPGA/RTL 原型 | 可复现实验脚本、配置、日志和图表 |
| 交付 | TCC 架构专利与实现专利 | 权利要求、实施例、附图和对比 |

入口：[[30_TCC/TCC_Master_Index|TCC 主索引]] · [[wiki/index#TCC — Topology-Centric Computing ({wiki['tcc']} concepts)|TCC Wiki ({wiki['tcc']} 概念)]]

### iNEST：复杂网络涌现智能

| 层级 | 推进 | 证据要求 |
|---|---|---|
| 理论 | CST 智能涌现、临界性、自组织 | 模型假设、动力学方程、临界指标 |
| 技术 | SNN、储备池、STDP/FEP、多尺度 | 网络结构、学习规则、训练配置 |
| 工程 | SNN/异步电路/存算一体 | 仿真、综合、资源、功耗和时延 |
| 交付 | iNEST 论文、专著、白皮书、专利 | 版本、章节状态、引用证据 |

入口：[[40_iNEST/iNEST_Master_Index|iNEST 主索引]] · [[wiki/index#iNEST — In-Network Neuromorphic ({wiki['inest']} concepts)|iNEST Wiki ({wiki['inest']} 概念)]]

---

## 🧪 假设注册表

| ID | 假设 | 状态 |
|---|---|---|
{hyp_md}
> [[99_Meta/hypothesis_registry.json|完整假设注册表]] · [[wiki/evolution_report|进化报告]]

---

## 📈 从知识到成果

```text
论文导入 → Inbox → 管线筛选 → raw/
    ↓
wiki_compiler → wiki/ ({wiki['total']} 概念, {articles_count} 文章)
    ↓
跨域洞察 + 任务推荐 + 假设验证
    ↓
每日行动 → 实验/写作/专利任务
    ↓
Processing → TCC/iNEST → Output
    ↓
验证回写 → 看板更新 → 周度复盘 → 下一轮
```

---

## ⚡ 自动化节奏

| 时间 | 动作 | 产出 |
|---|---|---|
| 08:00 | 科研管线检索 | 新论文 + 摘要 + 相关性评分 |
| 08:30 | Wiki 编译 + 引擎链 | 概念提取 + 交叉链接 + 洞察 |
| 20:00 | Inbox 处理 + 进化 | 去重归类 + 假设验证 |
| 21:00 | Git 同步 | 版本留痕 + 备份 |
| 周日 03:00 | 健康检查 | 诊断报告 + 进化队列 |

---

## 🔬 研究溯源与归类

按来源原则对全库内容重新归类（脚本：`[[90_System/scripts/classify_provenance.py]]`，数据：`[[99_Meta/classification.json]]`）：

- [[60_MOC/10_Own_Research_Diagnosis|🔬 自有研究 · 现状诊断与后续计划]] — 含「刘勤让 / iNEST 研究组」署名的本组产出，共 **{own_total}** 篇（含现状诊断与后续计划）
- [[60_MOC/11_External_Literature_Index|🌐 外部爬取文献索引]] — 含文献名 / 第三方平台名（arXiv、得到、Genspark、Codex、S2 等）的爬取内容，共 **{ext_total}** 篇

---

## 🗺️ 快速入口

| 入口 | 解决什么 |
|---|---|
| [研发看板（浏览器打开）](http://127.0.0.1:8899/vault/70_Dashboard/index.html) | 今日做什么、进展、洞察 |
| [[60_MOC/03_Daily_Action\\|每日行动]] | 论文 → 可执行任务 |
| [[60_MOC/04_Daily_Focus\\|今日焦点]] | 当天最重要任务 |
| [[wiki/index\\|Wiki 概念索引]] | {wiki['total']} 个结构化概念 |
| [[wiki/task_recommendations\\|任务推荐]] | 知识缺口驱动任务 |
| [[60_MOC/TCC_iNEST_成果全景\\|成果全景]] | 论文、专利、代码 |
| [[60_MOC/00_知识库治理中枢\\|治理中枢]] | 目录职责与标准 |
| [[60_MOC/10_Own_Research_Diagnosis\\|自有研究诊断]] | 本组产出现状与计划 |
| [[60_MOC/11_External_Literature_Index\\|外部文献索引]] | 爬取内容按来源归类 |

---

## 📈 知识演化追踪（近 10 次自进化）

{trend_md}

> 完整日志 → [[99_Meta/self_evolve_log.json|自进化日志]] · 健康报告 → [[wiki/health|知识健康报告]]

---

## 🎯 自动任务推荐（Top {len(tasks)}）

{tasks_md}

> 完整列表 → [[wiki/task_recommendations|任务推荐报告]]（由 task_recommender 每日生成）

---

## 🩺 健康检查（来自 wiki/health.md）

{health_md}

> 缺口由每日自进化持续消解；如需扩大清理范围请人工确认。

---

## 🔧 自进化规则

1. 每条结论必须关联论文/实验/仿真 — 无来源数字标记"待测"
2. 每篇论文回答：TCC 价值、iNEST 价值、可执行启发、下一步验证
3. 每个任务有输出物和验收证据
4. 每周检查：重复、断链、过期计划、管线耗时、Git 状态

---

*主页由 homepage_generator.py 自动刷新 | {NOW}*
"""
    
    # Phase 5: 生成浏览器看板数据 70_Dashboard/data.js
    try:
        dash_dir = VAULT / "70_Dashboard"
        dash_dir.mkdir(exist_ok=True)
        dash_data = {
            "updated": NOW,
            "snapshot": {
                "total_md": total_md, "tcc": tcc_files, "inest": inest_files,
                "inbox": inbox, "processing": processing, "output": output_files,
                "git_uncommitted": git_uncommitted,
            },
            "wiki": wiki, "articles": articles_count,
            "bridges": bridges, "hypotheses": hypotheses,
            "trend": trend, "tasks": tasks, "health": hs,
            "classification": {"own": own_total, "external": ext_total},
            "pipeline_status": pipeline_status,
        }
        (dash_dir / "data.js").write_text(
            "window.VAULT_DATA = " + json.dumps(dash_data, ensure_ascii=False, indent=2) + ";\n",
            encoding="utf-8")
        log("70_Dashboard/data.js generated")
    except Exception as e:
        log(f"⚠️ data.js 生成失败: {e}")

    HOME.write_text(content, encoding='utf-8')
    log(f"Home.md generated ({len(content)} chars)")
    log("=== Done ===")

if __name__ == "__main__":
    generate()
