#!/usr/bin/env python3
"""
P1.4: 每日洞察 → 可执行任务生成器
洞察→论文灵感→专利方向→仿真任务→代码开发→明日计划
"""
import os, sys, json, re
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime
from openai import OpenAI

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
KEY = os.environ.get("DEEPSEEK_API_KEY") or "REDACTED_DEEPSEEK_KEY"
client = OpenAI(api_key=KEY, base_url="https://api.deepseek.com/v1")
TODAY = datetime.now().strftime("%Y-%m-%d")

def scan_context():
    """Gather context: recent files, active tasks, output status"""
    ctx = {"recent_tcc": [], "recent_inest": [], "active_tasks": [], "output_status": {}}
    
    # Recent files
    for dim, d in [("TCC", "30_TCC"), ("iNEST", "40_iNEST")]:
        p = VAULT / d
        if p.exists():
            files = sorted(p.rglob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)[:10]
            for f in files:
                try:
                    c = f.read_text(encoding="utf-8", errors="replace")
                    ctx[f"recent_{dim.lower()}"].append({
                        "file": str(f.relative_to(VAULT)),
                        "summary": c.split("\n")[0][:80] if c else f.name
                    })
                except: pass
    
    # Active tasks from frontmatter
    for f in (VAULT / "30_TCC").rglob("*.md"):
        try:
            c = f.read_text(encoding="utf-8", errors="replace")[:500]
            if any(kw in c for kw in ["- [ ]", "TODO", "待办", "进行中"]):
                ctx["active_tasks"].append(str(f.relative_to(VAULT))[:100])
        except: pass
        if len(ctx["active_tasks"]) > 15: break
    
    # Output counts
    for d in ["51_Papers", "52_Patents", "54_Code"]:
        p = VAULT / "50_Output" / d
        ctx["output_status"][d] = len(list(p.rglob("*.md"))) if p.exists() else 0
    
    return ctx

def generate_actionable_insights(ctx):
    """Generate insights that produce concrete tasks"""
    recent_tcc = json.dumps(ctx["recent_tcc"][:5], ensure_ascii=False)
    recent_inest = json.dumps(ctx["recent_inest"][:5], ensure_ascii=False)
    tasks = "\n".join(ctx["active_tasks"][:10])
    
    prompt = f"""你是TCC+iNEST研发的首席策略官。基于当前研究状态，生成可执行的每日洞察。

当前状态:
- TCC最新文件: {recent_tcc}
- iNEST最新文件: {recent_inest}
- 活跃任务: {tasks}
- 产出: 论文{ctx['output_status'].get('51_Papers',0)}篇, 专利{ctx['output_status'].get('52_Patents',0)}件

输出Markdown(不要代码块):

# DeepSeek 每日行动洞察 — {TODAY}

## 🔥 今日3个最重要行动
(每个行动一行，格式: **编号. 行动描述** — 关联文件 — 预期产出)

## 📄 论文推进建议
(基于当前进展的2-3条具体建议,每条约50字)

## 💡 新灵感速递
(基于最新文献/笔记的2-3个可验证灵感)

## 🏷️ 专利布局建议
(1-2个可布局方向)

## ⚙️ 仿真/开发建议
(1-2个具体仿真或代码任务)

## 📋 明日计划草案
(3-5条明日行动)"""

    try:
        resp = client.chat.completions.create(
            model="deepseek-chat", messages=[{"role":"user","content":prompt}],
            temperature=0.7, max_tokens=3072, timeout=120
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"# 洞察生成失败\n\nError: {e}"

def extract_tasks_from_insights(insight_text):
    """Extract actionable tasks from insights text"""
    tasks = {"today": [], "tomorrow": [], "papers": [], "patents": [], "simulation": []}
    
    current_section = None
    for line in insight_text.split("\n"):
        line = line.strip()
        if "今日3个最重要" in line:
            current_section = "today"
        elif "明日计划" in line:
            current_section = "tomorrow"
        elif "论文推进" in line:
            current_section = "papers"
        elif "专利布局" in line:
            current_section = "patents"
        elif "仿真" in line:
            current_section = "simulation"
        
        if current_section and (line.startswith("- ") or line.startswith("**") or line and line[0].isdigit()):
            tasks[current_section].append(line.strip("- *").strip())
    
    return tasks

def main():
    print(f"Daily Actionable Insights — {TODAY}")
    
    # Scan context
    print("[1/4] Scanning vault context...")
    ctx = scan_context()
    print(f"  TCC: {len(ctx['recent_tcc'])} recent, iNEST: {len(ctx['recent_inest'])} recent")
    print(f"  Active tasks: {len(ctx['active_tasks'])}")
    
    # Generate insights
    print("[2/4] Generating insights via DeepSeek...")
    insights = generate_actionable_insights(ctx)
    
    # Save date-named version
    insight_path = VAULT / "60_MOC" / f"03_Daily_Action_{TODAY}.md"
    insight_path.write_text(insights, encoding="utf-8")
    
    # Save latest
    latest_path = VAULT / "60_MOC" / "03_Daily_Action.md"
    latest_path.write_text(insights, encoding="utf-8")
    
    # Also update legacy 02_DeepSeek_Insights for backward compat
    legacy_path = VAULT / "60_MOC" / "02_DeepSeek_Insights.md"
    legacy_path.write_text(insights, encoding="utf-8")
    
    print(f"  Saved: {insight_path.name} ({len(insights)} chars)")
    
    # Extract tasks
    print("[3/4] Extracting actionable tasks...")
    tasks = extract_tasks_from_insights(insights)
    for cat, items in tasks.items():
        if items:
            print(f"  {cat}: {len(items)} items")
    
    # Update unified data bus
    print("[4/4] Updating unified data bus...")
    try:
        import subprocess
        bus = str(VAULT / "90_System" / "scripts" / "unified_data_bus.py")
        subprocess.run([sys.executable, bus], check=False, timeout=60)
        print("  Unified data bus updated")
    except:
        print("  Unified bus skip")
    
    print(f"\nDone: {TODAY}")
    return tasks

if __name__ == "__main__":
    main()
