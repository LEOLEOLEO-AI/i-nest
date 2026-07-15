#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
daily_kanban_update.py - Daily R&D Kanban Auto-Update
Scans yesterday's file changes, generates progress/plan, updates kanban HTML.
"""
import os, json, re, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
from datetime import datetime, timedelta
from collections import defaultdict

KANBAN_PATH = r"D:\Obsidian\home\work\.openclaw\workspace\70_Dashboard\index.html"
WATCH_DIRS = [r"D:\Obsidian\home\work\.openclaw\workspace"]
SKIP = {".venv", ".git", "node_modules", "__pycache__", ".smart-env", ".obsidian",
        ".neural_db", ".neural_memory", ".ajson", ".openclaw", ".tasks", "copilot",
        "state", "memory", "legacy_subvault", "knowledge_graph", "inspiration_engine",
        "dashboard", "skills", "90_System", "99_Journal", "00_Inbox"}

def should_skip(path_parts):
    return bool(set(path_parts) & SKIP)

def scan(target_date):
    results = defaultdict(list)
    for wd in WATCH_DIRS:
        if not os.path.isdir(wd):
            continue
        for root, dirs, files in os.walk(wd):
            parts = set(os.path.relpath(root, wd).split(os.sep))
            if should_skip(parts):
                dirs.clear()
                continue
            dirs[:] = [d for d in dirs if d not in SKIP]
            for fname in files:
                fpath = os.path.join(root, fname)
                try:
                    mtime = datetime.fromtimestamp(os.path.getmtime(fpath))
                except:
                    continue
                if mtime.date() != target_date:
                    continue
                rel = os.path.relpath(fpath, wd)
                ext = os.path.splitext(fname)[1].lower()
                dim = "iNEST" if any(k in rel.lower() for k in ["inest", "sdi", "fep", "stdp", "connectome", "emergence", "liquid"]) else "TCC"
                cat = "璁烘枃" if "璁烘枃" in rel else "涓撳埄" if "涓撳埄" in rel else "浠跨湡绋嬪簭" if ext == ".py" else "浜у搧浠ｇ爜寮€鍙? if ext in (".v",".sv") or "fpga" in rel.lower() else "椤圭洰鎸囧崡绛栧垝" if any(k in rel for k in ["绛栧垝","鎸囧崡","鐧界毊涔?,"涓撹憲"]) else "鐏垫劅" if "鐏垫劅" in rel else "璧勬枡"
                results[(dim, cat)].append({"name": fname, "path": rel, "mtime": mtime.strftime("%H:%M")})
    return results

def generate_progress(results, yesterday_str):
    progress = []
    for (dim, cat), files in sorted(results.items()):
        names = [f["name"].replace(".py","").replace(".md","")[:50] for f in files[:3]]
        progress.append({
            "text": cat + ": " + "銆?.join(names) + ("锛堝叡%d涓枃浠讹級" % len(files) if len(files)>3 else ""),
            "dot": "done", "dim": dim
        })
    if not progress:
        progress.append({"text": "鏄ㄦ棩锛? + yesterday_str + "锛夋棤鏄捐憲鏂囦欢鍙樻洿", "dot": "done", "dim": "TCC+iNEST"})
    progress.append({"text": "鐪嬫澘鑷姩鏇存柊锛氭壂鎻忔槰鏃ヨ繘灞曪紝鐢熸垚浠婃棩寰呭姙", "dot": "done", "dim": "TCC+iNEST"})
    return progress

def generate_plan():
    plans = []
    try:
        with open(KANBAN_PATH, "r", encoding="utf-8", errors="replace") as f:
            html = f.read()
        m = re.search(r'"entries":\s*\[(.*?)\]\s*\}', html, re.DOTALL)
        if m:
            entries = json.loads("[" + m.group(1) + "]")
            active = [e for e in entries if e.get("priority") == "楂? and e.get("status") not in ("宸插畬鎴?,"宸插彂甯?,"瑙勫垝涓?)]
            active.sort(key=lambda x: x.get("date",""), reverse=True)
            for e in active[:5]:
                plans.append({"text": "[" + e["dim"] + "] " + e["title"][:50] + "锛? + e.get("status","") + "", "dot": "plan", "dim": e["dim"]})
    except:
        pass
    if not plans:
        plans = [
            {"text": "妫€鏌DI浠跨湡瀹為獙鏈€鏂拌繘灞?, "dot": "plan", "dim": "iNEST"},
            {"text": "鎺ㄨ繘鏍稿績璁烘枃鎾板啓杩涘害", "dot": "plan", "dim": "TCC"},
            {"text": "瀹℃牳鏄ㄦ棩鏂囦欢鍙樻洿骞舵洿鏂扮湅鏉挎潯鐩?, "dot": "plan", "dim": "TCC+iNEST"},
        ]
    return plans

def update_kanban(today_str, progress, plan, dry_run=False):
    with open(KANBAN_PATH, "r", encoding="utf-8", errors="replace") as f:
        html = f.read()
    
    # Check if today entry already exists
    today_pattern = '"date": "' + today_str + '", "type": "today"'
    if today_pattern in html:
        print("SKIP: Today entry for " + today_str + " already exists, no duplicate created.")
        return True
    
    new_entry = {"date": today_str, "type": "today", "progress": progress, "plan": plan}
    new_json = json.dumps(new_entry, ensure_ascii=False)
    daily_start = html.find('"daily": [')
    if daily_start < 0:
        # Create daily data structure if missing
        body_end = html.find("</body>")
        if body_end < 0:
            body_end = html.find("</html>")
        if body_end > 0:
            script_block = "<" + "script>window.__KANBAN_DATA__ = {'daily': [" + new_json + "]};</" + "script>"
            html = html[:body_end] + script_block + chr(10) + html[body_end:]
            print("Created daily data structure")
            with open(KANBAN_PATH, "w", encoding="utf-8", newline="", errors="replace") as f:
                f.write(html)
            return True
        print("ERROR: daily array not found and cannot create")
        return False
    first_brace = html.find("{", daily_start)
    
    # Only change "today" to "yesterday" for entries that are NOT today's date
    import re as _re
    html = _re.sub(
        r'"date": "(?!' + today_str + r')\d{4}-\d{2}-\d{2}", "type": "today"',
        lambda m: m.group(0).replace('"type": "today"', '"type": "yesterday"'),
        html
    )
    
    html = html[:first_brace] + new_json + ", " + html[first_brace:]
    if dry_run:
        print("[DRY RUN] Would update kanban")
        return True
    with open(KANBAN_PATH, "w", encoding="utf-8", newline="", errors="replace") as f:
        f.write(html)
    return True

def main():
    dry_run = "--dry-run" in sys.argv
    today = datetime.now()
    target_date = today.date() - timedelta(days=1)
    for a in sys.argv:
        if a.startswith("--date="):
            target_date = datetime.strptime(a.split("=")[1], "%Y-%m-%d").date()
    yesterday_str = target_date.strftime("%Y-%m-%d")
    today_str = today.strftime("%Y-%m-%d")
    print("Scanning: " + yesterday_str)
    results = scan(target_date)
    total = sum(len(v) for v in results.values())
    print("Found " + str(total) + " files in " + str(len(results)) + " categories")
    progress = generate_progress(results, yesterday_str)
    plan = generate_plan()
    print("Progress: " + str(len(progress)) + " items, Plan: " + str(len(plan)) + " items")
    for p in progress:
        print("  [" + p["dim"] + "] " + p["text"][:80])
    if update_kanban(today_str, progress, plan, dry_run):
        if not dry_run:
            os.startfile(KANBAN_PATH)
            print("Kanban opened.")
    else:
        print("Failed.")

if __name__ == "__main__":
    main()


# ===== P0.3: Update unified data bus =====
try:
    import subprocess, os
    bus_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "unified_data_bus.py")
    subprocess.run([sys.executable, bus_script], check=False, timeout=60)
    print("[UnifiedBus] Updated after kanban update")
except Exception as e:
    print(f"[UnifiedBus] Skip: {e}")