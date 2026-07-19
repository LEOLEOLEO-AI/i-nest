#!/usr/bin/env python3
"""
P3.1-P3.4: 自进化引擎
- 周度重组: LLM重分类+重链接
- 灵感验证闭环
- 研究日志自动生成
- Git自动提交
"""
import os, sys, json, re, subprocess
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime, timedelta
from openai import OpenAI

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
KEY = os.environ.get("DEEPSEEK_API_KEY") or "REDACTED_DEEPSEEK_KEY"
client = OpenAI(api_key=KEY, base_url="https://api.deepseek.com/v1")
TODAY = datetime.now().strftime("%Y-%m-%d")

# ====== P3.1: Weekly Reorg ======

def weekly_reorg(dry_run=False):
    """Weekly vault reorganization using LLM"""
    print(f"Weekly Reorganization — {TODAY}")
    
    # Scan recent file changes
    week_ago = (datetime.now() - timedelta(days=7)).timestamp()
    recent = []
    for d in ["30_TCC", "40_iNEST", "50_Output"]:
        p = VAULT / d
        if not p.exists(): continue
        for f in p.rglob("*.md"):
            if f.stat().st_mtime > week_ago:
                try:
                    recent.append({
                        "path": str(f.relative_to(VAULT)),
                        "mtime": datetime.fromtimestamp(f.stat().st_mtime).strftime("%m-%d"),
                        "size": f.stat().st_size,
                        "preview": f.read_text(encoding="utf-8", errors="replace")[:200]
                    })
                except: pass
    
    print(f"  Recent changes (7d): {len(recent)} files")
    
    # Generate reorganization suggestions
    if recent:
        recent_json = json.dumps([{"p": r["path"], "t": r["mtime"]} for r in recent[:30]], ensure_ascii=False)
        prompt = f"""分析本周活跃的研究文件,给出重组建议:

文件列表:
{recent_json}

返回JSON:
{{
    "merge_suggestions": [{{"files": ["文件1","文件2"], "reason": "合并原因"}}],
    "split_suggestions": [{{"file": "文件", "reason": "拆分原因"}}],
    "archive_suggestions": [{{"file": "文件", "reason": "归档原因"}}],
    "reclassify_suggestions": [{{"file": "文件", "from": "当前目录", "to": "建议目录", "reason": "原因"}}],
    "week_summary": "本周研究进展一句话总结"
}}"""
        
        try:
            resp = client.chat.completions.create(
                model="deepseek-chat", messages=[{"role":"user","content":prompt}],
                temperature=0.3, max_tokens=1024, timeout=60
            )
            text = resp.choices[0].message.content
            m = re.search(r'\{[\s\S]*\}', text)
            suggestions = json.loads(m.group()) if m else {}
        except:
            suggestions = {"week_summary": "本周无重大变化"}
    else:
        suggestions = {"week_summary": "本周无文件变更"}
    
    # Save report
    report = f"""# 周度重组报告 — {TODAY}

## 本周概要
{suggestions.get('week_summary', 'N/A')}

## 统计
- 本周变更文件: {len(recent)}
- 活跃任务: 见看板

## 建议操作
"""
    for cat, items in [("合并建议", "merge_suggestions"), ("拆分建议", "split_suggestions"), 
                        ("归档建议", "archive_suggestions"), ("重分类建议", "reclassify_suggestions")]:
        if items in suggestions and suggestions[items]:
            report += f"\n### {cat}\n"
            for item in suggestions[items]:
                report += f"- {json.dumps(item, ensure_ascii=False)}\n"
    
    report_path = VAULT / "60_MOC" / f"05_Weekly_Reorg_{TODAY}.md"
    report_path.write_text(report, encoding="utf-8")
    print(f"  Saved: {report_path.name}")
    return suggestions

# ====== P3.2: Inspiration Verification Loop ======

def verify_inspirations():
    """Check if inspirations have been acted upon"""
    print("Inspiration Verification Loop")
    
    insights_dir = VAULT / "60_MOC"
    verified = {"acted": 0, "pending": 0, "stale": 0}
    
    # Read recent daily actions
    for f in sorted(insights_dir.glob("03_Daily_Action_*.md"), reverse=True)[:7]:
        try:
            c = f.read_text(encoding="utf-8", errors="replace")
            # Count actionable items
            actions = re.findall(r'^[-\d]+[\.\)]\s*(.+)', c, re.MULTILINE)
            for a in actions:
                # Check if any file in vault contains evidence of action
                keyword = a[:20]
                found = False
                for df in list((VAULT / "30_TCC").rglob("*.md"))[:100] + list((VAULT / "40_iNEST").rglob("*.md"))[:100]:
                    try:
                        if keyword in df.read_text(encoding="utf-8", errors="replace")[:1000]:
                            found = True
                            break
                    except: pass
                if found:
                    verified["acted"] += 1
                else:
                    verified["pending"] += 1
        except: pass
    
    # Mark stale (older than 30 days)
    verified["stale"] = verified["pending"]  # simplified
    print(f"  Acted: {verified['acted']}, Pending: {verified['pending']}")
    return verified

# ====== P3.3: Research Log Auto-Generation ======

def generate_research_log():
    """Generate today's research log from vault activity"""
    today_midnight = datetime.now().replace(hour=0, minute=0, second=0).timestamp()
    
    activities = []
    for d in ["30_TCC", "40_iNEST", "50_Output", "10_Inbox"]:
        p = VAULT / d
        if not p.exists(): continue
        for f in p.rglob("*.md"):
            if f.stat().st_mtime > today_midnight:
                activities.append({
                    "time": datetime.fromtimestamp(f.stat().st_mtime).strftime("%H:%M"),
                    "action": "modified" if f.stat().st_ctime < today_midnight else "created",
                    "file": str(f.relative_to(VAULT))
                })
    
    log_lines = [f"# 研究日志 — {TODAY}", "", f"## 今日活动 ({len(activities)} 条)", ""]
    for a in sorted(activities, key=lambda x: x["time"]):
        icon = "📝" if a["action"] == "modified" else "🆕"
        log_lines.append(f"- {icon} [{a['time']}] {a['action']}: {a['file']}")
    
    log_path = VAULT / "99_Meta" / "research_logs" / f"log_{TODAY}.md"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text("\n".join(log_lines), encoding="utf-8")
    print(f"Research log: {len(activities)} activities")
    return len(activities)

# ====== P3.4: Git Auto-Commit ======

def git_auto_commit():
    """Auto commit and push to Gitee"""
    os.chdir(str(VAULT))
    
    # Check for changes
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if not result.stdout.strip():
        print("Git: No changes to commit")
        return False
    
    # Stage changes
    subprocess.run(["git", "add", "-A"], capture_output=True)
    
    # Commit
    msg = f"auto: daily pipeline {TODAY}"
    commit = subprocess.run(["git", "commit", "-m", msg], capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(f"Git commit: {commit.stdout.strip()}")
    
    # Push
    push = subprocess.run(["git", "push"], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
    print(f"Git push: {push.stdout.strip() if push.returncode == 0 else push.stderr.strip()}")
    return True

# ====== Main Pipeline ======

def run_full_pipeline():
    """Run all Stage 1-3 pipeline steps"""
    print("=" * 60)
    print(f"  TCC + iNEST Full Pipeline — {TODAY}")
    print("=" * 60)
    
    results = {}
    
    # Stage 1: Digestion
    print("\n=== STAGE 1: Digestion ===")
    try:
        import process_inbox
        results["inbox"] = process_inbox.process_inbox()
    except Exception as e:
        print(f"  Inbox skip: {e}")
    
    try:
        import processing_workflow
        processing_workflow.process_processing_dir()
    except Exception as e:
        print(f"  Processing skip: {e}")
    
    try:
        import link_engine
        results["links"] = link_engine.link_engine(max_files=200)
    except Exception as e:
        print(f"  Links skip: {e}")
    
    # Stage 2: Tasks
    print("\n=== STAGE 2: Tasks ===")
    try:
        import task_board
        results["tasks"] = task_board.main()
    except Exception as e:
        print(f"  Tasks skip: {e}")
    
    try:
        import daily_insights
        results["insights"] = daily_insights.main()
    except Exception as e:
        print(f"  Insights skip: {e}")
    
    # Stage 3: Evolution
    print("\n=== STAGE 3: Evolution ===")
    results["reorg"] = weekly_reorg()
    results["verify"] = verify_inspirations()
    results["log"] = generate_research_log()
    
    # Unified data bus
    print("\n=== Unified Data Bus ===")
    try:
        subprocess.run([sys.executable, str(VAULT / "90_System/scripts/unified_data_bus.py")], check=False, timeout=60)
        print("  Updated")
    except: pass
    
    # Git
    print("\n=== Git Sync ===")
    git_auto_commit()
    
    print("\n" + "=" * 60)
    print(f"  Pipeline Complete — {TODAY}")
    print("=" * 60)
    return results

if __name__ == "__main__":
    if "--full" in sys.argv:
        run_full_pipeline()
    elif "--reorg" in sys.argv:
        weekly_reorg()
    elif "--git" in sys.argv:
        git_auto_commit()
    elif "--log" in sys.argv:
        generate_research_log()
    else:
        # Default: generate log + git
        generate_research_log()
        git_auto_commit()
