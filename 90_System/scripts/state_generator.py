#!/usr/bin/env python3
"""
Research State Generator — Unified Data Bus
Generates research_state.json as single source of truth for all pipeline components.
Runs: python state_generator.py [--output FILE]
"""
import json, os, subprocess, time
from pathlib import Path
from datetime import datetime, timedelta

VAULT = Path(r"D:\Obsidian\vault")
DEFAULT_OUTPUT = VAULT / "99_Meta" / "research_state.json"
TODAY = datetime.now().strftime("%Y-%m-%d")

def count_files(path, pattern="*.md"):
    if not path.exists():
        return 0
    return len(list(path.glob(pattern)))

def count_recursive(path, pattern="*.md"):
    if not path.exists():
        return 0
    return len(list(path.rglob(pattern)))

def check_port(port):
    try:
        result = subprocess.run(
            ["netstat", "-ano"], capture_output=True, text=True, timeout=5
        )
        return f":{port}" in result.stdout and "LISTENING" in result.stdout
    except:
        return False

def get_git_status():
    try:
        r = subprocess.run(
            ["git", "-C", str(VAULT), "status", "--porcelain"],
            capture_output=True, text=True, timeout=10
        )
        lines = [l for l in r.stdout.strip().split("\n") if l]
        return {"uncommitted": len(lines), "details": lines[:20]}
    except:
        return {"uncommitted": -1, "error": "git not found"}

def get_pipeline_logs():
    log_dir = VAULT / "logs"
    runs = []
    if log_dir.exists():
        for f in sorted(log_dir.glob("pipeline_*.json"), reverse=True)[:7]:
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                data["_file"] = f.name
                runs.append(data)
            except:
                pass
    return runs

def get_pipeline_insights():
    inbox = VAULT / "00_Inbox" / "_pipeline_insights"
    if not inbox.exists():
        return {"today": 0, "total": 0, "recent": []}
    today_files = list(inbox.glob(f"{TODAY}_*.md"))
    all_files = list(inbox.glob("*.md"))
    recent = []
    for f in sorted(today_files, reverse=True)[:10]:
        content = f.read_text(encoding="utf-8", errors="ignore")[:500]
        recent.append({"file": f.name, "preview": content[:200]})
    return {"today": len(today_files), "total": len(all_files), "recent": recent}

def get_weekly_health():
    moc = VAULT / "60_MOC"
    reports = sorted(moc.glob("weekly_health_*.md"), reverse=True)
    return {
        "latest": reports[0].name if reports else None,
        "count": len(reports)
    }

def get_task_review():
    path = VAULT / "99_Meta" / "research_task_proposals.json"
    if not path.exists():
        return {"pending": 0, "approved": 0, "promoted": 0}
    try:
        items = json.loads(path.read_text(encoding="utf-8")).get("items", [])
    except (OSError, json.JSONDecodeError):
        return {"pending": 0, "approved": 0, "promoted": 0}
    return {status: sum(item.get("status") == status for item in items)
            for status in ("pending_review", "approved", "promoted")}

def count_vault_stats():
    return {
        "total_md": count_recursive(VAULT, "*.md"),
        "inbox_00": count_files(VAULT / "00_Inbox" / "_pipeline_insights", "*.md"),
        "processing_20": count_recursive(VAULT / "20_Processing", "*.md"),
        "tcc_30": count_recursive(VAULT / "30_TCC", "*.md"),
        "inest_40": count_recursive(VAULT / "40_iNEST", "*.md"),
        "output_50": count_recursive(VAULT / "50_Output", "*.md"),
        "moc_60": count_files(VAULT / "60_MOC", "*.md"),
    }

def generate(output_file=None):
    if output_file is None:
        output_file = DEFAULT_OUTPUT
    output_file = Path(output_file)

    state = {
        "generated": datetime.now().isoformat(),
        "generator": "state_generator.py v1.0",
        "vault": count_vault_stats(),
        "services": {
            "preview_server_8899": check_port(8899),
            "jojo_llm_57321": check_port(57321),
            "jojo_fixer_57320": check_port(57320),
        },
        "pipeline": {
            "ingested_today": get_pipeline_insights(),
            "recent_runs": get_pipeline_logs(),
        },
        "git": get_git_status(),
        "health": get_weekly_health(),
        "task_review": get_task_review(),
    }

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[OK] research_state.json -> {output_file}")
    return state

if __name__ == "__main__":
    import sys
    out = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == "--output" else None
    state = generate(out)
    # Print summary
    v = state["vault"]
    p = state["pipeline"]
    print(f"Vault: {v['total_md']} md files, 00_inbox={v['inbox_00']}")
    print(f"Pipeline: {p['ingested_today']['today']} today, {len(p['recent_runs'])} recent runs")
    print(f"Services: 8899={state['services']['preview_server_8899']}, 57321={state['services']['jojo_llm_57321']}, 57320={state['services']['jojo_fixer_57320']}")
    print(f"Git: {state['git']['uncommitted']} uncommitted changes")
