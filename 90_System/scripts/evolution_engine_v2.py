#!/usr/bin/env python3
"""
Self-Evolution Engine v1.0
- Evidence Ledger: tracks key findings with sources
- Hypothesis Registry: tracks research hypotheses and verification
- Evolution Queue: pending system improvements
Integrated with research_state.json
"""
import json, os, sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, r"D:\Obsidian\scripts")

VAULT = Path(r"D:\Obsidian\vault")
STATE_FILE = VAULT / "99_Meta" / "research_state.json"
LEDGER_FILE = VAULT / "99_Meta" / "evolution_ledger.json"
HYPOTHESIS_FILE = VAULT / "99_Meta" / "hypothesis_registry.json"
EVOLUTION_FILE = VAULT / "99_Meta" / "evolution_queue.json"
TODAY = datetime.now().strftime("%Y-%m-%d")

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {}

def load_json(path, default=None):
    if default is None:
        default = {}
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except:
            return default
    return default

def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def generate_evidence_ledger():
    """Scan pipeline insights and generate evidence ledger."""
    ledger = load_json(LEDGER_FILE, {"entries": [], "last_updated": None})
    insights_dir = VAULT / "00_Inbox" / "_pipeline_insights"
    
    existing_urls = {e.get("url") for e in ledger.get("entries", [])}
    new_entries = []
    
    if insights_dir.exists():
        for f in sorted(insights_dir.glob("*.md"), reverse=True)[:50]:
            content = f.read_text(encoding="utf-8", errors="ignore")
            # Parse frontmatter
            title = ""
            url = ""
            relevance = 0
            in_front = False
            for line in content.split("\n"):
                if line.strip() == "---":
                    in_front = not in_front
                    continue
                if in_front:
                    if line.startswith("title:"):
                        title = line.split(":", 1)[1].strip().strip('"')
                    elif line.startswith("url:"):
                        url = line.split(":", 1)[1].strip()
                    elif line.startswith("relevance:"):
                        try:
                            relevance = int(line.split(":", 1)[1].strip())
                        except:
                            pass
            
            if url and url not in existing_urls and relevance >= 2:
                new_entries.append({
                    "title": title,
                    "url": url,
                    "relevance": relevance,
                    "file": str(f.relative_to(VAULT)),
                    "discovered": f.stem[:10] if len(f.stem) >= 10 else f.stem[:10],
                    "status": "pending_review"
                })
                existing_urls.add(url)
    
    if new_entries:
        ledger["entries"] = ledger.get("entries", []) + new_entries
        ledger["last_updated"] = datetime.now().isoformat()
        save_json(LEDGER_FILE, ledger)
        print(f"[Evidence] {len(new_entries)} new entries in ledger (total: {len(ledger['entries'])})")
    else:
        print(f"[Evidence] No new entries (total: {len(ledger.get('entries', []))})")
    
    return ledger

def update_hypothesis_registry():
    """Track research hypotheses and their verification status."""
    hypo = load_json(HYPOTHESIS_FILE, {"hypotheses": [], "last_updated": None})
    
    # Ensure default hypotheses exist
    defaults = [
        {"id": "H1", "title": "TCC: 拓扑互连可实现超加性计算增益 (1+1>2)", "status": "proven", "evidence": "P1_Superadditivity proof"},
        {"id": "H2", "title": "CST: 智能涌现依赖自组织临界性", "status": "under_investigation", "evidence": "S2 papers on SOC"},
        {"id": "H3", "title": "iNEST: 脉冲神经网络在晶上系统可实现类脑计算", "status": "proposed", "evidence": ""},
        {"id": "H4", "title": "TCC: SDSoW架构可线性扩展至晶圆级", "status": "under_investigation", "evidence": "架构论文"},
    ]
    
    existing_ids = {h["id"] for h in hypo.get("hypotheses", [])}
    for h in defaults:
        if h["id"] not in existing_ids:
            hypo.setdefault("hypotheses", []).append(h)
    
    hypo["last_updated"] = datetime.now().isoformat()
    save_json(HYPOTHESIS_FILE, hypo)
    print(f"[Hypothesis] {len(hypo['hypotheses'])} hypotheses tracked")
    return hypo

def update_evolution_queue():
    """Track pending system improvements."""
    queue = load_json(EVOLUTION_FILE, {"items": [], "last_updated": None})
    
    # Auto-detect issues from pipeline logs
    state = load_state()
    pipeline = state.get("pipeline", {})
    recent_runs = pipeline.get("recent_runs", [])
    
    items = []

    # Close stale pipeline alarms once a run produces papers again.
    successful_run = any(
        (r.get("new_papers", 0) or r.get("api_results", 0)) > 0
        for r in recent_runs[:3]
    )
    if successful_run:
        for existing in queue.get("items", []):
            if existing.get("type") == "pipeline_fix" and existing.get("status") == "pending":
                existing["status"] = "resolved"
                existing["resolved_at"] = datetime.now().isoformat()
                existing["resolution"] = "A recent run ingested papers successfully; network and relevance gates are working."
    
    # Check for 0-paper runs
    zero_runs = [r for r in recent_runs if r.get("new_papers", 0) == 0]
    if len(zero_runs) >= 2:
        items.append({
            "id": f"EV-{TODAY}-001",
            "priority": "high",
            "type": "pipeline_fix",
            "title": "Pipeline zero-paper alert: API connectivity check",
            "detail": f"Recent runs with zero new papers: {len(zero_runs)}",
            "status": "pending"
        })
    
    # Check git hygiene
    git = state.get("git", {})
    if git.get("uncommitted", 0) > 10:
        items.append({
            "id": f"EV-{TODAY}-002",
            "priority": "medium",
            "type": "git_hygiene",
            "title": f"Git hygiene: {git['uncommitted']} uncommitted changes",
            "detail": "Commit or review outstanding changes.",
            "status": "pending"
        })
    
    existing_ids = {i["id"] for i in queue.get("items", [])}
    for item in items:
        if item["id"] not in existing_ids:
            queue.setdefault("items", []).append(item)
    
    queue["last_updated"] = datetime.now().isoformat()
    save_json(EVOLUTION_FILE, queue)
    print(f"[Evolution] {len(items)} new issues queued (total: {len(queue.get('items', []))})")
    return queue

def run_all():
    print(f"=== Self-Evolution Engine v1.0 === {TODAY}")
    generate_evidence_ledger()
    update_hypothesis_registry()
    update_evolution_queue()
    print("=== Done ===")

if __name__ == "__main__":
    run_all()
