#!/usr/bin/env python3
"""
P2.1-P2.4: 任务驱动看板系统
- 任务状态机: 规划→进行→验证→完成
- 论文/专利/代码进度追踪
- 每日焦点推送
"""
import os, sys, json, re
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime, timedelta

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
TODAY = datetime.now().strftime("%Y-%m-%d")

STATES = ["规划中", "进行中", "验证中", "已完成"]
TYPES = ["论文", "专利", "代码开发", "仿真实验", "项目策划", "资料整理"]

def scan_all_tasks():
    """Scan vault for all TODO/任务 items with frontmatter context"""
    tasks = {}
    for dim, dpath in [("TCC", "30_TCC"), ("iNEST", "40_iNEST"), ("Output", "50_Output")]:
        p = VAULT / dpath
        if not p.exists(): continue
        for f in p.rglob("*.md"):
            try:
                c = f.read_text(encoding="utf-8", errors="replace")
                task_matches = re.findall(r'-\s*\[([ x])\]\s*(.+)', c)
                for checked, task_text in task_matches:
                    task_id = f"TASK-{hash(task_text[:30]) % 10000:04d}"
                    if task_id not in tasks:
                        tasks[task_id] = {
                            "id": task_id,
                            "text": task_text.strip()[:100],
                            "done": checked == "x",
                            "dim": dim,
                            "file": str(f.relative_to(VAULT)),
                            "mtime": datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d"),
                            "status": "已完成" if checked == "x" else "规划中",
                            "type": classify_task_type(task_text)
                        }
            except: pass
    return tasks

def classify_task_type(text):
    for t in TYPES:
        if t in text: return t
    return "资料整理"

def build_task_board(tasks):
    """Build task board data structure"""
    board = {"columns": {}, "papers": [], "patents": [], "code": [], "focus_today": []}
    
    # Group by status
    for st in STATES:
        board["columns"][st] = []
    
    for tid, t in tasks.items():
        if t["done"]: 
            board["columns"]["已完成"].append(t)
        else:
            board["columns"]["规划中"].append(t)
        
        # Categorize
        if t["type"] == "论文":
            board["papers"].append(t)
        elif t["type"] == "专利":
            board["patents"].append(t)
        elif t["type"] == "代码开发":
            board["code"].append(t)
    
    # Sort by recency
    for col in board["columns"]:
        board["columns"][col].sort(key=lambda x: x.get("mtime", ""), reverse=True)
    
    # Generate today's focus: top 3 non-done tasks
    not_done = [t for t in tasks.values() if not t["done"]]
    not_done.sort(key=lambda x: x.get("mtime", ""), reverse=True)
    board["focus_today"] = not_done[:3]
    
    return board

def generate_focus_md(board):
    """Generate today's focus markdown for Home.md inclusion"""
    focus = board.get("focus_today", [])
    lines = [f"## 🔥 今日焦点 — {TODAY}", ""]
    
    for i, t in enumerate(focus[:3], 1):
        dim_emoji = "🟦" if t.get("dim") == "TCC" else "🟩"
        lines.append(f"{i}. {dim_emoji} [{t.get('type','')}] {t.get('text','')[:80]}")
        lines.append(f"   📁 {t.get('file','')}")
    
    if not focus:
        lines.append("> 暂无活跃任务。运行每日洞察生成今日任务。")
    
    # Also add paper/patent progress
    papers = board.get("papers", [])
    patents = board.get("patents", [])
    code = board.get("code", [])
    
    lines.append("")
    lines.append("## 📊 产出进度")
    lines.append(f"| 类型 | 总数 | 进行中 | 已完成 |")
    lines.append(f"|------|------|--------|--------|")
    lines.append(f"| 📄 论文 | {len(papers)} | {len([p for p in papers if not p['done']])} | {len([p for p in papers if p['done']])} |")
    lines.append(f"| 🏷️ 专利 | {len(patents)} | {len([p for p in patents if not p['done']])} | {len([p for p in patents if p['done']])} |")
    lines.append(f"| 💻 代码 | {len(code)} | {len([p for p in code if not p['done']])} | {len([p for p in code if p['done']])} |")
    
    return "\n".join(lines)

def main():
    print(f"Task Board Generator — {TODAY}")
    
    print("[1/3] Scanning tasks...")
    tasks = scan_all_tasks()
    print(f"  Found {len(tasks)} tasks")
    
    print("[2/3] Building task board...")
    board = build_task_board(tasks)
    for col, items in board["columns"].items():
        print(f"  {col}: {len(items)}")
    print(f"  Focus today: {len(board['focus_today'])}")
    
    # Save task board data
    task_data_path = VAULT / "70_Dashboard" / "task_board.json"
    task_data_path.write_text(json.dumps({
        "generated": TODAY,
        "board": {k: v for k, v in board.items() if k != "columns"},
        "columns": {k: v[:20] for k, v in board["columns"].items()},
        "stats": {
            "total": len(tasks),
            "done": len([t for t in tasks.values() if t["done"]]),
            "active": len([t for t in tasks.values() if not t["done"]])
        }
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  Saved task_board.json")
    
    print("[3/3] Generating focus markdown...")
    focus_md = generate_focus_md(board)
    focus_path = VAULT / "60_MOC" / "04_Daily_Focus.md"
    focus_path.write_text(focus_md, encoding="utf-8")
    print(f"  Saved 04_Daily_Focus.md")
    
    # Print focus
    print("\n=== TODAY FOCUS ===")
    print(focus_md[:500])
    
    return board

if __name__ == "__main__":
    main()
