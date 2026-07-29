# -*- coding: utf-8 -*-
"""P0: One-click Inbox processing - called from Obsidian Shell Commands or CLI"""

import subprocess, sys
from pathlib import Path

VAULT = Path(r"D:\Obsidian\vault")
PYTHON = r"C:\Users\LEO\AppData\Local\Programs\Python\Python310\python.exe"

TASKS = {
    "inbox": {
        "script": "process_inbox.py",
        "desc": "处理Inbox → TCC/iNEST分类",
    },
    "pipeline": {
        "script": "pipeline_v3.py",
        "desc": "运行完整研究管线(S2+arXiv+分类)",
    },
    "sync": {
        "script": "gitee_sync.py",
        "desc": "Git同步到Gitee",
    },
    "dashboard": {
        "script": "daily_kanban_update.py",
        "desc": "刷新研发看板数据",
    },
    "health": {
        "script": "wiki_health.py",
        "desc": "知识库健康检查",
    },
    "weekly": {
        "script": "progress_report.py",
        "desc": "生成周度进展报告",
    },
}

def run_task(task_name):
    if task_name not in TASKS:
        print(f"Unknown task: {task_name}")
        print(f"Available: {list(TASKS.keys())}")
        return
    
    task = TASKS[task_name]
    script = VAULT / "90_System" / "scripts" / task["script"]
    
    if not script.exists():
        print(f"Script not found: {script}")
        return
    
    print(f"=== {task['desc']} ===")
    result = subprocess.run([PYTHON, "-X", "utf8", str(script)], 
                          cwd=str(VAULT), capture_output=True, text=True, encoding="utf-8", errors="ignore")
    print(result.stdout)
    if result.stderr:
        print(f"STDERR: {result.stderr[:500]}")
    print(f"Exit: {result.returncode}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Obsidian Quick Tasks")
    parser.add_argument("task", nargs="?", default="inbox", choices=list(TASKS.keys()),
                       help="Task to run")
    parser.add_argument("--list", action="store_true", help="List available tasks")
    args = parser.parse_args()
    
    if args.list:
        for name, info in TASKS.items():
            print(f"  {name}: {info['desc']}")
    else:
        run_task(args.task)
