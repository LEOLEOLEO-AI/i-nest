#!/usr/bin/env python3
"""
iNEST 科研日报生成器 v2.0
设计原则：
  1. 任务驱动：从论文/专利清单读取 deadline 和状态，产出"今天应该做什么"
  2. 灵感激发：从最近灵感库 + 近期日记中提炼连接点，提出3个值得深想的问题
  3. 想法收敛：把散落的 Inbox 和灵感分类归拢，推动进入正式研究
  4. 进度可视：显示各论文/专利的当前状态和剩余时间
  5. 简洁可读：总长控制在 400-600 字，手机可快速浏览
"""

import os, re, json, subprocess
from datetime import datetime, timedelta
from pathlib import Path

VAULT = Path("/home/work/obsidian-vault")
WORKSPACE = Path("/home/work/.openclaw/workspace")
DAILY_DIR = VAULT / "Journal" / "每日总结"
GITEE_URL = "https://iBrainNest:Liusansan%406363@gitee.com/iBrainNest/i-nest.git"

# ─────────────────────────────────────────
#  核心任务表（从论文/专利清单提炼的硬约束）
#  每次有新 deadline 或状态变更，手动或由AI更新此表
# ─────────────────────────────────────────
TASKS = [
    # (id, name, deadline_str, status, priority)
    ("A1",  "CST主论文 LaTeX打包→arXiv",       "2026-05-31", "进行中",   "🔴"),
    ("B2",  "P-Mapping V3 → IEEE TPDS投稿",   "2026-06-30", "进行中",   "🔴"),
    ("P1",  "P1专利 CNIPA 申请",              "2026-05-15", "进行中",   "🔴"),
    ("P2",  "P2专利 CNIPA 申请",              "2026-07-31", "草稿",     "🟡"),
    ("A11", "CST英文统一理论论文 NMI",          "2026-06-30", "初稿完成", "🟡"),
    ("PA",  "Paper A (B7) ASPLOS'27",         "2026-09-09", "框架完成", "🟡"),
    ("P3",  "P3专利 拓扑重构FFT",             "2026-12-31", "待启动",   "🟢"),
]

def days_left(deadline_str: str) -> int:
    try:
        dl = datetime.strptime(deadline_str, "%Y-%m-%d")
        return (dl - datetime.now()).days
    except:
        return 999

def read_recent_diary(n=3) -> list[tuple[str,str]]:
    """读最近n天日记正文"""
    result = []
    today = datetime.now()
    for i in range(n):
        d = today - timedelta(days=i)
        for pat in [
            VAULT / "Journal" / f"{d.year}年{d.month}月{d.day}号 日记.md",
            VAULT / "Journal" / f"{d.strftime('%Y-%m-%d')}.md",
        ]:
            if pat.exists():
                txt = pat.read_text(encoding="utf-8")
                m = re.search(r'## 正文\n+(.*?)(?=\n##|\n---|\Z)', txt, re.DOTALL)
                content = m.group(1).strip() if m else ""
                if content:
                    result.append((d.strftime("%m-%d"), content[:400]))
                break
    return result

def read_recent_ideas(n=5) -> list[str]:
    """读最近n条灵感"""
    ideas = []
    idea_dir = VAULT / "灵感库"
    files = sorted(idea_dir.glob("2*.md"), reverse=True)[:n]
    for f in files:
        txt = f.read_text(encoding="utf-8")
        # 提取标题
        m = re.search(r'^# 💡 (.+)', txt, re.MULTILINE)
        title = m.group(1).strip() if m else f.stem
        # 提取核心想法
        m2 = re.search(r'## 核心想法\n+(.+?)(?=\n##|\Z)', txt, re.DOTALL)
        idea = m2.group(1).strip()[:120] if m2 else ""
        ideas.append(f"**{title}**" + (f"：{idea}" if idea else ""))
    return ideas

def read_inbox_count() -> int:
    """统计待分类数量"""
    inbox = VAULT / "Inbox" / "待分类"
    if inbox.exists():
        return len([f for f in inbox.glob("*.md") if not f.name.startswith("无标题")])
    return 0

def get_git_activity() -> str:
    """查询最近24h的git提交摘要"""
    r = subprocess.run(
        ["git", "log", "--oneline", "--since=24 hours ago", "--no-merges"],
        cwd=VAULT, capture_output=True, text=True
    )
    lines = [l.strip() for l in r.stdout.strip().split("\n") if l.strip()]
    return lines[:5] if lines else []

def derive_spark_questions(diaries: list, ideas: list) -> list[str]:
    """基于日记内容 + 当前任务 + 灵感，生成3个值得深想的问题（规则引擎版）"""
    all_text = " ".join(d for _, d in diaries) + " ".join(ideas)
    sparks = []

    # 规则：根据文本出现的主题关联已知研究问题
    if any(k in all_text for k in ["国家项目", "立项", "申报", "产品定义"]):
        sparks.append("💡 **课题申报定位**：国家项目要解决什么核心问题？iNEST的NCC范式能否成为下一个计算范式迁移的旗舰课题？")

    if any(k in all_text for k in ["知识库", "智能体", "GET笔记", "印象笔记", "TRAE"]):
        sparks.append("💡 **工具链闭环**：GET笔记→Obsidian→Genspark Claw的链路能否做到输入即触发研究？下一步是否需要一个自动触发论文初稿的机制？")

    if any(k in all_text for k in ["CST", "Γst", "涌现", "阈值", "自然常数"]):
        sparks.append("💡 **CST理论延伸**：六个自然常数阈值是否存在第七个？量子纠缠网络的Γst是否超越δ≈4.6692？")

    if any(k in all_text for k in ["SDI", "互连", "NCC", "拓扑", "同构"]):
        sparks.append("💡 **NCC实验验证**：FFT-AllReduce图同构定理能否在现有模拟器上先跑出数据？这是Paper A最薄弱的一环。")

    if any(k in all_text for k in ["销售", "商业", "市场", "井芯"]):
        sparks.append("💡 **研产融合**：井芯的销售增长第二曲线与NCC芯片量产路径是否有交集？能否设计NCC芯片→SDI-CC数智升级→标准化产品的商业验证路径？")

    # 保底：始终加一个关于LaTeX/投稿的问题
    if not any("LaTeX" in s or "arXiv" in s for s in sparks):
        sparks.append("💡 **最近行动**：cst_v25.tex 还没写完——今天花1小时完成引言和结论两节，能让整个投稿进度前进30%。")

    return sparks[:3]

def generate_daily_report(target_date: datetime = None) -> Path:
    if target_date is None:
        target_date = datetime.now()

    today_str = target_date.strftime("%Y-%m-%d")
    output_file = DAILY_DIR / f"{today_str}_每日总结.md"

    # ── 数据收集 ──
    diaries  = read_recent_diary(3)
    ideas    = read_recent_ideas(3)
    inbox_n  = read_inbox_count()
    git_acts = get_git_activity()
    sparks   = derive_spark_questions(diaries, ideas)
    tomorrow = (target_date + timedelta(days=1)).strftime("%Y-%m-%d")

    # ── 任务看板：按deadline排序，只显示最近90天内 ──
    urgent_tasks = sorted(
        [(t, d) for t in TASKS if (d := days_left(t[2])) <= 90],
        key=lambda x: x[1]
    )

    # ── 构建报告 ──
    lines = [
        "---",
        f"title: \"{today_str} 科研日报\"",
        f"date: {today_str}",
        "type: daily-report",
        "---",
        "",
        f"# 📋 {today_str} 科研日报",
        "",
        "---",
        "",
        "## ⏰ 紧急任务雷达（90天内到期）",
        "",
        "| 任务 | 截止日 | 剩余 | 状态 |",
        "|------|--------|------|------|",
    ]

    for task, days in urgent_tasks:
        tid, name, dl, status, pri = task
        days_str = f"**{days}天**" if days <= 14 else f"{days}天"
        lines.append(f"| {pri} [{tid}] {name} | {dl} | {days_str} | {status} |")

    lines += [
        "",
        "---",
        "",
        "## 💡 灵感激发（今天可以想3分钟的问题）",
        "",
    ]
    for s in sparks:
        lines.append(f"- {s}")
        lines.append("")

    lines += [
        "---",
        "",
        "## 📥 近期日记摘要",
        "",
    ]
    for date_str, text in diaries:
        snippet = text[:200].replace("\n", " ")
        lines.append(f"**{date_str}**: {snippet}{'...' if len(text)>200 else ''}")
        lines.append("")

    if ideas:
        lines += [
            "---",
            "",
            "## 🌱 最近灵感",
            "",
        ]
        for idea in ideas:
            lines.append(f"- {idea}")
        lines.append("")

    if git_acts:
        lines += [
            "---",
            "",
            "## 🔧 昨日写入（Vault近24h提交）",
            "",
        ]
        for act in git_acts:
            lines.append(f"- `{act}`")
        lines.append("")

    lines += [
        "---",
        "",
        f"## 🎯 明日行动（{tomorrow}）",
        "",
        "> 基于任务雷达，建议明日聚焦：",
        "",
    ]

    # 智能推导：最近deadline任务的下一步行动
    action_map = {
        "A1":  "写完 `cst_v25.tex` 引言节（约1.5h），完成后可立即打包投arXiv",
        "B2":  "检查 P-Mapping V3 图表是否完整，确认 IEEE TPDS 投稿格式",
        "P1":  "P1权利要求书 Claim 11 细化描述，准备CNIPA格式转换",
        "P2":  "P2 五张图（Fig 1-5）绘制 — 已有描述，缺图稿",
        "A11": "把 CST V25 英文摘要改写为 NMI submission 格式（约45min）",
        "PA":  "Paper A：完成 FFT 同构矩阵证明的数学推导草稿",
        "P3":  "P3 专利：拓扑重构FFT电路图框架设计",
    }
    if urgent_tasks:
        top3 = urgent_tasks[:3]
        for i, (task, days) in enumerate(top3, 1):
            tid = task[0]
            action = action_map.get(tid, f"推进 [{tid}] {task[1]}")
            lines.append(f"{i}. **[{tid}]** {action}")
    else:
        lines.append("1. 检查所有任务状态，更新论文清单")

    lines += [
        "",
        "| 优先级 | 任务 | 预估时间 |",
        "|--------|------|---------|",
        "| 🔴 最高 | | |",
        "| 🟡 重要 | | |",
        "| 🟢 日常 | | |",
        "",
    ]

    if inbox_n > 0:
        lines += [
            "---",
            "",
            f"## 📂 Inbox 待处理（{inbox_n} 条）",
            "",
            f"> `Inbox/待分类` 有 {inbox_n} 条笔记等待分类，",
            "> 建议每周五花20分钟统一归档或删除。",
            "",
        ]

    lines += [
        "---",
        f"*自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')} | iNEST科研日报系统 v2.0*",
    ]

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text("\n".join(lines), encoding="utf-8")
    return output_file

def git_push(msg: str):
    subprocess.run(["git", "add", "-A"], cwd=VAULT, capture_output=True)
    r = subprocess.run(["git", "commit", "-m", msg], cwd=VAULT,
                       capture_output=True, text=True)
    if "nothing to commit" not in r.stdout:
        subprocess.run(
            ["git", "push", "origin", "main", "--force-with-lease"],
            cwd=VAULT, capture_output=True, timeout=30
        )

if __name__ == "__main__":
    import sys
    date_arg = sys.argv[1] if len(sys.argv) > 1 else None

    if date_arg:
        target = datetime.strptime(date_arg, "%Y-%m-%d")
    else:
        target = datetime.now()

    print(f"📋 生成 {target.strftime('%Y-%m-%d')} 科研日报...")
    f = generate_daily_report(target)
    git_push(f"daily-report: {target.strftime('%Y-%m-%d')} 科研日报")
    print(f"✅ 已生成并推送: {f.relative_to(VAULT)}")
    print(f"\n--- 报告内容预览 ---")
    print(f.read_text(encoding="utf-8")[:1500])
