#!/usr/bin/env python3
"""
S-TIER: Self-Monitoring Health Dashboard + Quality Scoring
Generates health.json with 8-dimension scores for real-time monitoring
"""
import os, sys, json, re
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime
from collections import defaultdict

VAULT = Path(r"D:\Obsidian\vault")
TODAY = datetime.now().strftime("%Y-%m-%d")

def score_dimension(name, value, thresholds):
    """Score 0-100 based on thresholds: [(min, max, score_if_in_range), ...]"""
    for lo, hi, score in thresholds:
        if lo <= value <= hi:
            return score
    return thresholds[-1][2] if thresholds else 0

def compute_health():
    h = {
        "timestamp": datetime.now().isoformat(),
        "dimensions": {},
        "overall": 0,
        "alerts": [],
        "recommendations": []
    }
    
    # DIM 1: Digestion Health
    inbox_count = len(list((VAULT/"00_Inbox").rglob("*.md"))) if (VAULT/"00_Inbox").exists() else 0
    proc_count = len(list((VAULT/"20_Processing").rglob("*.md"))) if (VAULT/"20_Processing").exists() else 0
    h["dimensions"]["digestion"] = {
        "score": 100 if inbox_count == 0 and proc_count == 0 else 60 if inbox_count < 5 else 20,
        "inbox_pending": inbox_count,
        "processing_pending": proc_count,
        "status": "CLEAR" if inbox_count == 0 else "BACKLOG"
    }
    if inbox_count > 0:
        h["alerts"].append(f"Inbox has {inbox_count} unprocessed files")
    
    # DIM 2: Link Coverage
    total = 0; linked = 0
    for f in list((VAULT/"30_TCC").rglob("*.md"))[:500] + list((VAULT/"40_iNEST").rglob("*.md"))[:500]:
        try:
            c = f.read_text(encoding="utf-8", errors="replace")
            total += 1
            if "[[" in c: linked += 1
        except: pass
    pct = linked/total*100 if total else 0
    h["dimensions"]["linking"] = {
        "score": score_dimension("linking", pct, [(80,100,100),(50,79,70),(0,49,30)]),
        "coverage_pct": round(pct, 1),
        "files_checked": total
    }
    
    # DIM 3: Insight Freshness
    daily_action = VAULT/"60_MOC"/f"03_Daily_Action_{TODAY}.md"
    insight_age_hours = 999
    if daily_action.exists():
        insight_age_hours = (datetime.now() - datetime.fromtimestamp(daily_action.stat().st_mtime)).total_seconds() / 3600
    h["dimensions"]["insights"] = {
        "score": 100 if insight_age_hours < 24 else 60 if insight_age_hours < 48 else 20,
        "age_hours": round(insight_age_hours, 1),
        "file": str(daily_action.relative_to(VAULT)) if daily_action.exists() else "MISSING"
    }
    if insight_age_hours > 24:
        h["alerts"].append(f"Insights stale: {insight_age_hours:.0f}h old")
    
    # DIM 4: Git Sync Health
    import subprocess
    os.chdir(str(VAULT))
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    uncommitted = len([l for l in result.stdout.split("\n") if l.strip()])
    h["dimensions"]["git_sync"] = {
        "score": 100 if uncommitted == 0 else 70 if uncommitted < 10 else 30,
        "uncommitted_files": uncommitted
    }
    if uncommitted > 5:
        h["alerts"].append(f"{uncommitted} uncommitted files")
    
    # DIM 5: Output Pipeline
    papers = len(list((VAULT/"50_Output"/"51_Papers").rglob("*.md"))) if (VAULT/"50_Output"/"51_Papers").exists() else 0
    patents = len(list((VAULT/"50_Output"/"52_Patents").rglob("*.md"))) if (VAULT/"50_Output"/"52_Patents").exists() else 0
    h["dimensions"]["output"] = {
        "score": 85 if papers > 100 and patents > 30 else 60,
        "papers": papers,
        "patents": patents
    }
    
    # DIM 6: Task Tracking
    tasks_total = 0; tasks_done = 0
    for f in list((VAULT/"30_TCC").rglob("*.md"))[:500] + list((VAULT/"40_iNEST").rglob("*.md"))[:500]:
        try:
            c = f.read_text(encoding="utf-8", errors="replace")[:500]
            tasks_total += len(re.findall(r'- \[[ x]\]', c))
            tasks_done += len(re.findall(r'- \[x\]', c))
        except: pass
    h["dimensions"]["tasks"] = {
        "score": 80 if tasks_total > 50 else 50,
        "total": tasks_total,
        "done": tasks_done,
        "completion_rate": round(tasks_done/tasks_total*100, 1) if tasks_total else 0
    }
    
    # DIM 7: Frontmatter Quality
    fm_total = 0; fm_good = 0
    for f in list((VAULT/"30_TCC").rglob("*.md"))[:500]:
        try:
            c = f.read_text(encoding="utf-8", errors="replace")
            fm_total += 1
            if c.startswith("---") and "direction:" in c[:500]:
                fm_good += 1
        except: pass
    fm_pct = fm_good/fm_total*100 if fm_total else 0
    h["dimensions"]["frontmatter"] = {
        "score": score_dimension("fm", fm_pct, [(70,100,100),(40,69,60),(0,39,30)]),
        "with_frontmatter_pct": round(fm_pct, 1)
    }
    
    # DIM 8: Automation
    import subprocess as sp
    task_check = sp.run(["schtasks", "/query", "/tn", "iNEST_S_Tier_Daily"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    h["dimensions"]["automation"] = {
        "score": 100 if task_check.returncode == 0 else 40,
        "daily_pipeline_active": task_check.returncode == 0
    }
    
    # OVERALL
    scores = [d["score"] for d in h["dimensions"].values()]
    h["overall"] = round(sum(scores) / len(scores), 1) if scores else 0
    h["grade"] = "S" if h["overall"] >= 95 else "A" if h["overall"] >= 85 else "B" if h["overall"] >= 70 else "C" if h["overall"] >= 50 else "D"
    
    # Recommendations
    if h["overall"] < 95:
        if inbox_count > 0:
            h["recommendations"].append("Run process_inbox.py to clear inbox backlog")
        if uncommitted > 5:
            h["recommendations"].append("Run git commit+push to sync changes")
        if insight_age_hours > 24:
            h["recommendations"].append("Run daily_insights.py to refresh insights")
        if fm_pct < 70:
            h["recommendations"].append("Run link_engine.py to add frontmatter")
    
    return h

if __name__ == "__main__":
    health = compute_health()
    
    # Save health.json
    out = VAULT / "70_Dashboard" / "health.json"
    out.write_text(json.dumps(health, ensure_ascii=False, indent=2), encoding="utf-8")
    
    # Print summary
    print(f"S-Tier Health: {health['overall']}/100 — Grade {health['grade']}")
    for dim, data in health["dimensions"].items():
        bar = "█" * (data["score"] // 10) + "░" * (10 - data["score"] // 10)
        print(f"  {dim:15s} [{bar}] {data['score']}")
    
    if health["alerts"]:
        print(f"\nAlerts: {len(health['alerts'])}")
        for a in health["alerts"]:
            print(f"  ⚠️ {a}")
    
    if health["recommendations"]:
        print(f"\nRecommendations:")
        for r in health["recommendations"]:
            print(f"  → {r}")
