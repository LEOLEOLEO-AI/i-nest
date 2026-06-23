#!/usr/bin/env python3
"""
每日/每周总结自动生成器 v1.0
从Get笔记日记内容 → AI提炼 → 生成Obsidian格式总结+计划
"""
import os, json, subprocess, re
from datetime import datetime, timedelta
from pathlib import Path

VAULT = Path("/home/work/obsidian-vault")
JOURNAL_DIR = VAULT / "Journal"
DAILY_DIR   = JOURNAL_DIR / "每日总结"
WEEKLY_DIR  = JOURNAL_DIR / "每周总结"
IDEA_DIR    = VAULT / "灵感库"

GITEE_URL = "https://iBrainNest:Liusansan%406363@gitee.com/iBrainNest/i-nest.git"

# ── 工具函数 ──────────────────────────────────────────
def git_push(msg):
    subprocess.run(["git","add","-A"], cwd=VAULT, capture_output=True)
    r = subprocess.run(["git","commit","-m",msg], cwd=VAULT,
                       capture_output=True, text=True)
    if "nothing to commit" not in r.stdout:
        subprocess.run(["git","push","origin","main","--force-with-lease"],
                       cwd=VAULT, capture_output=True, timeout=30)

def read_diary(date: datetime) -> str:
    """读取指定日期的日记内容"""
    patterns = [
        JOURNAL_DIR / f"{date.year}年{date.month}月{date.day}号 日记.md",
        JOURNAL_DIR / f"{date.strftime('%Y-%m-%d')}.md",
        JOURNAL_DIR / f"{date.year}年{date.month}月{date.day}日 日记.md",
    ]
    for p in patterns:
        if p.exists():
            return p.read_text(encoding="utf-8")
    # 模糊匹配
    for f in JOURNAL_DIR.glob(f"*{date.year}*{date.month}*{date.day}*日记*.md"):
        return f.read_text(encoding="utf-8")
    return ""

def call_ai(prompt: str) -> str:
    """调用AI生成内容"""
    try:
        r = subprocess.run(
            ["gsk", "web_search", prompt[:500]],  # 先用search作为fallback
            capture_output=True, text=True, timeout=30
        )
        # 实际上用gsk super_agent
        r2 = subprocess.run(
            ["gsk", "task", "super_agent",
             "--task_name", "日报生成",
             "--query", prompt[:2000],
             "--instructions", "直接输出Markdown格式内容，不要额外解释"],
            capture_output=True, text=True, timeout=120
        )
        out = r2.stdout.strip()
        # 提取URL（gsk task会返回URL）
        url_match = re.search(r'https?://[^\s]+', out)
        if url_match:
            # 下载结果
            import urllib.request
            with urllib.request.urlopen(url_match.group(), timeout=30) as resp:
                return resp.read().decode()[:5000]
        return out[:3000] if out else ""
    except Exception as e:
        return f"[AI生成失败: {e}]"

# ── 每日总结生成 ──────────────────────────────────────
def gen_daily_summary(target_date: datetime = None) -> Path:
    """生成指定日期的每日总结（默认今天）"""
    if target_date is None:
        target_date = datetime.now()

    today_str = target_date.strftime("%Y-%m-%d")
    tomorrow  = target_date + timedelta(days=1)
    output_file = DAILY_DIR / f"{today_str}_每日总结.md"

    if output_file.exists():
        print(f"  ℹ️  {today_str} 总结已存在，跳过")
        return output_file

    # 读今天的日记
    diary = read_diary(target_date)
    diary_text = ""
    if diary:
        # 提取正文部分
        m = re.search(r'## 正文\n+(.*?)(?=\n##|\n---|\Z)', diary, re.DOTALL)
        diary_text = m.group(1).strip() if m else diary[:1000]

    print(f"  📝 生成 {today_str} 每日总结...")

    # 构建总结内容（基于日记+模板）
    lines = [
        "---",
        f"title: \"{today_str} 每日总结\"",
        f"date: {today_str}",
        f"type: daily-review",
        "---",
        "",
        f"# 📅 {today_str} 每日总结",
        "",
    ]

    if diary_text:
        lines += [
            "## 📖 今日日记摘要",
            "",
            diary_text[:500] + ("..." if len(diary_text)>500 else ""),
            "",
        ]

    lines += [
        "## ✅ 今日完成",
        "",
        "- [ ] *(请填写今日完成的事项)*",
        "",
        "## 💡 灵感闪现",
        "",
        "> 随时记录，不评判",
        "",
        "- ",
        "",
        "## 📚 今日学到",
        "",
        "- ",
        "",
        "## 🌪️ 遇到的问题",
        "",
        "- ",
        "",
        f"## 🎯 {tomorrow.strftime('%Y-%m-%d')} 明日计划",
        "",
        "| 优先级 | 任务 | 所属方向 | 预计时间 |",
        "|--------|------|---------|---------|",
        "| 🔴 高 | | | |",
        "| 🟡 中 | | | |",
        "| 🟢 低 | | | |",
        "",
        "## 🔗 相关笔记",
        "",
        "- ",
        "",
        "---",
        f"*生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
    ]

    output_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"  ✅ 已生成: {output_file.relative_to(VAULT)}")
    return output_file

# ── 每周总结生成 ──────────────────────────────────────
def gen_weekly_summary(week_start: datetime = None) -> Path:
    """生成本周/指定周的每周总结"""
    if week_start is None:
        today = datetime.now()
        # 本周一
        week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    week_str  = week_start.strftime("%Y-W%W")
    output_file = WEEKLY_DIR / f"{week_str}_每周总结.md"

    if output_file.exists():
        print(f"  ℹ️  {week_str} 周报已存在")
        return output_file

    print(f"  📊 生成 {week_str} 每周总结...")

    # 收集本周每日总结和日记
    week_diaries = []
    for i in range(7):
        d = week_start + timedelta(days=i)
        text = read_diary(d)
        if text:
            week_diaries.append((d.strftime("%Y-%m-%d"), text[:300]))
        # 也收集每日总结
        daily_file = DAILY_DIR / f"{d.strftime('%Y-%m-%d')}_每日总结.md"
        if daily_file.exists():
            week_diaries.append((f"{d.strftime('%Y-%m-%d')}(总结)",
                                 daily_file.read_text()[:300]))

    next_week_start = week_end + timedelta(days=1)
    next_week_end   = next_week_start + timedelta(days=6)

    lines = [
        "---",
        f"title: \"{week_str} 每周总结\"",
        f"week: \"{week_str}\"",
        f"date_start: {week_start.strftime('%Y-%m-%d')}",
        f"date_end: {week_end.strftime('%Y-%m-%d')}",
        "type: weekly-review",
        "---",
        "",
        f"# 📆 {week_str} 每周总结",
        f"**{week_start.strftime('%Y-%m-%d')} ~ {week_end.strftime('%Y-%m-%d')}**",
        "",
        "## 🏆 本周亮点",
        "",
        "1. ",
        "2. ",
        "3. ",
        "",
    ]

    if week_diaries:
        lines += ["## 📖 本周日志摘要", ""]
        for date_str, text in week_diaries[:5]:
            snippet = text[:150].replace("\n", " ")
            lines.append(f"- **{date_str}**: {snippet}")
        lines.append("")

    lines += [
        "## ✅ 本周完成",
        "",
        "### NCC计算范式",
        "- ",
        "",
        "### 智能涌现范式",
        "- ",
        "",
        "### 项目与对外",
        "- ",
        "",
        "## 💡 本周灵感汇总",
        "",
        "- ",
        "",
        "## 📊 回顾与反思",
        "",
        "**做得好的：**",
        "- ",
        "",
        "**可以改进的：**",
        "- ",
        "",
        f"## 🎯 下周计划（{next_week_start.strftime('%m-%d')}~{next_week_end.strftime('%m-%d')}）",
        "",
        "### 核心目标（最重要的3件事）",
        "1. ",
        "2. ",
        "3. ",
        "",
        "### NCC计算范式 待办",
        "- [ ] ",
        "- [ ] ",
        "",
        "### 智能涌现范式 待办",
        "- [ ] ",
        "- [ ] ",
        "",
        "### 项目/对外 待办",
        "- [ ] ",
        "- [ ] ",
        "",
        "## 📅 下周日程",
        "",
        "| 日期 | 重要事项 |",
        "|------|---------|",
    ]
    for i in range(5):  # 周一到周五
        d = next_week_start + timedelta(days=i)
        weekday = ["周一","周二","周三","周四","周五"][i]
        lines.append(f"| {d.strftime('%m-%d')} {weekday} | |")

    lines += [
        "",
        "---",
        f"*生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
    ]

    output_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"  ✅ 已生成: {output_file.relative_to(VAULT)}")
    return output_file

# ── 灵感快捕 ──────────────────────────────────────────
def capture_idea(title: str, content: str = "", context: str = "") -> Path:
    """快速捕捉一个灵感"""
    now = datetime.now()
    safe_title = re.sub(r'[\\/:*?"<>|]', '', title)[:40].strip()
    output_file = IDEA_DIR / f"{now.strftime('%Y-%m-%d')}_{safe_title}.md"

    lines = [
        "---",
        f"title: \"{title}\"",
        f"date: {now.strftime('%Y-%m-%d')}",
        f"time: \"{now.strftime('%H:%M')}\"",
        "type: idea",
        "tags:",
        "  - \"灵感\"",
        "  - \"待评估\"",
        "---",
        "",
        f"# 💡 {title}",
        "",
        f"> **捕捉时间**：{now.strftime('%Y-%m-%d %H:%M')}",
    ]
    if context:
        lines.append(f"> **来源场景**：{context}")
    lines.append("")

    if content:
        lines += ["## 核心想法", "", content, ""]

    lines += [
        "## 可能的应用方向",
        "",
        "- [ ] NCC计算范式",
        "- [ ] 智能涌现范式",
        "- [ ] 产品/工程",
        "- [ ] 其他",
        "",
        "## 初步分析",
        "",
        "**潜力评估**：⭐⭐⭐（待评）",
        "",
        "**需要验证的问题**：",
        "- ",
        "",
        "**相关已有工作**：",
        "- ",
        "",
        "## 下一步行动",
        "",
        "- [ ] ",
        "",
        "---",
        f"*#灵感 #待评估*",
    ]

    output_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"  💡 灵感已保存: {output_file.relative_to(VAULT)}")
    return output_file

# ── 入口 ──────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "daily"

    if cmd == "daily":
        f = gen_daily_summary()
        git_push(f"journal: 每日总结 {datetime.now().strftime('%Y-%m-%d')}")

    elif cmd == "weekly":
        f = gen_weekly_summary()
        git_push(f"journal: 每周总结 {datetime.now().strftime('%Y-W%W')}")

    elif cmd == "idea":
        title   = sys.argv[2] if len(sys.argv) > 2 else "未命名灵感"
        content = sys.argv[3] if len(sys.argv) > 3 else ""
        context = sys.argv[4] if len(sys.argv) > 4 else ""
        f = capture_idea(title, content, context)
        git_push(f"idea: {title[:30]}")

    elif cmd == "all":
        gen_daily_summary()
        # 周五或周日生成周报
        if datetime.now().weekday() in (4, 6):
            gen_weekly_summary()
        git_push(f"journal: 自动归档 {datetime.now().strftime('%Y-%m-%d')}")

    print("Done.")
