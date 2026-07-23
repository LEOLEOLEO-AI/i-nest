#!/usr/bin/env python3
"""P0.3: 统一数据总线 — 单一真相源，所有面板从这一个JSON读取"""
import os, sys, json, re
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
TODAY = datetime.now().strftime("%Y-%m-%d")
YESTERDAY = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

def count_md(path):
    if not path.exists():
        return 0
    return len([f for f in path.rglob("*.md") if not any(p in f.parts for p in [".obsidian",".git",".venv","node_modules","80_Archive"])])

def recent_files(path, hours=24):
    cutoff = datetime.now().timestamp() - hours * 3600
    files = []
    if not path.exists():
        return files
    for f in path.rglob("*.md"):
        try:
            if f.stat().st_mtime > cutoff:
                files.append({
                    "name": f.name,
                    "path": str(f.relative_to(VAULT)),
                    "mtime": datetime.fromtimestamp(f.stat().st_mtime).strftime("%H:%M"),
                    "size": f.stat().st_size
                })
        except:
            pass
    return sorted(files, key=lambda x: x["mtime"], reverse=True)[:20]

def scan_tasks():
    """Scan for active tasks in vault files"""
    tasks = {"today": [], "active": [], "papers": [], "patents": [], "code": []}
    # Scan 30_TCC and 40_iNEST for ## 任务 or - [ ] patterns
    for dim_path, dim_name in [(VAULT/"30_TCC", "TCC"), (VAULT/"40_iNEST", "iNEST")]:
        if not dim_path.exists():
            continue
        for f in list(dim_path.rglob("*.md"))[:500]:
            try:
                c = f.read_text(encoding="utf-8", errors="replace")
                task_lines = [l.strip() for l in c.split("\n") if l.startswith("- [ ]") or "TODO" in l or "待办" in l]
                for tl in task_lines[:2]:
                    tasks["active"].append({
                        "text": tl[:100].replace("- [ ]","").replace("TODO","").strip(),
                        "dim": dim_name,
                        "file": str(f.relative_to(VAULT)),
                        "mtime": datetime.fromtimestamp(f.stat().st_mtime).strftime("%m-%d")
                    })
            except:
                pass
    # Deduplicate and limit
    seen = set()
    unique = []
    for t in tasks["active"]:
        key = t["text"][:40]
        if key not in seen:
            seen.add(key)
            unique.append(t)
    tasks["active"] = unique[:15]
    return tasks

def scan_insights():
    """Extract recent insights"""
    insights_dir = VAULT / "60_MOC"
    insights = {"tcc": [], "inest": [], "cross": []}
    # Read latest DeepSeek insight
    latest = insights_dir / "02_DeepSeek_Insights.md"
    if latest.exists():
        c = latest.read_text(encoding="utf-8", errors="replace")
        # Extract lines under insight sections
        current_section = None
        for line in c.split("\n"):
            if "TCC" in line and line.startswith("##"):
                current_section = "tcc"
            elif "iNEST" in line and line.startswith("##"):
                current_section = "inest"
            elif "协同" in line and line.startswith("##"):
                current_section = "cross"
            elif line.startswith("- ") and current_section and len(line) > 10:
                insights[current_section].append(line.strip("- ").strip()[:120])
    return insights

def build_unified_data():
    data = {
        "generated": datetime.now().isoformat(),
        "date": TODAY,
        "vault": {
            "total_md": count_md(VAULT),
            "tcc_total": count_md(VAULT / "30_TCC"),
            "tcc_theory": count_md(VAULT / "30_TCC" / "31_Theory"),
            "tcc_tech": count_md(VAULT / "30_TCC" / "32_Technology"),
            "tcc_eng": count_md(VAULT / "30_TCC" / "33_Engineering"),
            "inest_total": count_md(VAULT / "40_iNEST"),
            "inest_theory": count_md(VAULT / "40_iNEST" / "41_Theory"),
            "inest_tech": count_md(VAULT / "40_iNEST" / "42_Technology"),
            "inest_eng": count_md(VAULT / "40_iNEST" / "43_Engineering"),
        },
        "inbox": {
            "new_24h": len(recent_files(VAULT / "00_Inbox", 24)),
            "pending": count_md(VAULT / "00_Inbox"),
            "processing": count_md(VAULT / "20_Processing"),
        },
        "output": {
            "papers": count_md(VAULT / "50_Output" / "51_Papers"),
            "patents": count_md(VAULT / "50_Output" / "52_Patents"),
            "monographs": count_md(VAULT / "50_Output" / "53_Monographs"),
            "code": count_md(VAULT / "50_Output" / "54_Code"),
            "guides": count_md(VAULT / "50_Output" / "55_Guides"),
        },
        "recent_changes": recent_files(VAULT, 48),
        "tasks": scan_tasks(),
        "insights": scan_insights(),
    }
    return data

if __name__ == "__main__":
    data = build_unified_data()
    out_path = VAULT / "70_Dashboard" / "data.json"
    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    
    # Also write as JS for dashboard consumption
    js_out = VAULT / "70_Dashboard" / "data.js"
    js_out.write_text(f"// Unified Data Bus - generated {TODAY}\nvar UNIFIED_DATA = {json.dumps(data, ensure_ascii=False)};\n", encoding="utf-8")
    
    print(f"Unified data bus written:")
    print(f"  data.json: {out_path.stat().st_size}B")
    print(f"  data.js:   {js_out.stat().st_size}B")
    print(f"  Vault: {data['vault']['total_md']} md, TCC={data['vault']['tcc_total']}, iNEST={data['vault']['inest_total']}")
    print(f"  Inbox: {data['inbox']['pending']} pending, {data['inbox']['new_24h']} new(24h)")
    print(f"  Output: {data['output']['papers']} papers, {data['output']['patents']} patents")
    print(f"  Recent: {len(data['recent_changes'])} files changed")
    print(f"  Tasks: {len(data['tasks']['active'])} active")
    print(f"  Insights: TCC={len(data['insights']['tcc'])}, iNEST={len(data['insights']['inest'])}")
