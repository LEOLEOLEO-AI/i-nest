#!/usr/bin/env python3
"""Publish the current knowledge-base state to the TCC+iNEST dashboard.

This is the single publisher for live dashboard data. It reads the vault;
it never embeds static plans or historical dashboard data.
"""
import json
import re
from datetime import datetime, timedelta
from pathlib import Path

VAULT = Path(r"D:\Obsidian\vault")
MOC = VAULT / "60_MOC"
META = VAULT / "99_Meta"
LOGS = VAULT / "logs"
DASHBOARD = VAULT / "70_Dashboard"
STATE_FILE = META / "research_state.json"
DATA_FILE = DASHBOARD / "data.js"
TODAY = datetime.now().strftime("%Y-%m-%d")


def load_json(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def clean_text(text):
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    text = re.sub(r"[*`_]", "", text)
    return re.sub(r"\s+", " ", text).strip(" -:")


def task_track(text):
    lower = text.lower()
    tcc = any(word in lower for word in ("tcc", "p-paradigm", "topology", "interconnect", "chiplet", "noc", "拓扑", "互连", "专利"))
    inest = any(word in lower for word in ("inest", "cst", "snn", "spiking", "emergence", "critical", "涌现", "神经", "临界", "仿真"))
    if tcc and inest:
        return "TCC+iNEST"
    if tcc:
        return "TCC"
    if inest:
        return "iNEST"
    return "System"


def extract_numbered_tasks(path, markers):
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    heading = next((line for line in lines if line.startswith("#")), "")
    # Relax date check — show last available if stale
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', heading)
    if date_match:
        heading_date = date_match.group(1)
        # Accept data within last 7 days
        if (datetime.now() - datetime.strptime(heading_date, "%Y-%m-%d")).days > 7:
            return []
    tasks, active = [], False
    for raw in lines:
        line = raw.strip()
        if line.startswith("#"):
            active = any(marker in line for marker in markers)
            continue
        if active:
            match = re.match(r"^\d+[.)]\s+(.+)$", line)
            if match:
                task = clean_text(match.group(1))
                if task:
                    tasks.append(task)
    return tasks


def current_plan():
    action = extract_numbered_tasks(MOC / "03_Daily_Action.md", ("今日推荐行动", "今日行动"))
    focus = extract_numbered_tasks(MOC / "04_Daily_Focus.md", ("并行主线", "今日焦点"))
    items, seen = [], set()
    for task in action + focus:
        if task.lower() in seen:
            continue
        seen.add(task.lower())
        items.append({
            "text": task,
            "track": task_track(task),
            "status": "进行中" if len(items) < 3 else "待执行",
            "source": "今日行动" if task in action else "今日焦点",
        })
    return items[:8]


def recent_runs():
    latest_by_date = {}
    for path in sorted(LOGS.glob("pipeline_*.json"), reverse=True):
        item = load_json(path, {})
        date = item.get("date", "")[:10]
        if date and date not in latest_by_date:
            latest_by_date[date] = item
    result = []
    for offset in range(3):
        date = (datetime.now() - timedelta(days=offset)).strftime("%Y-%m-%d")
        run = latest_by_date.get(date)
        if run:
            result.append({
                "date": date,
                "papers": run.get("new_papers", 0),
                "nodes": run.get("graph_nodes", 0),
                "edges": run.get("graph_edges", 0),
                "minutes": round(run.get("elapsed_s", 0) / 60),
                "summary": f"科研管线完成：入库 {run.get('new_papers', 0)} 篇；图谱 {run.get('graph_nodes', 0)} 节点 / {run.get('graph_edges', 0)} 边；耗时 {round(run.get('elapsed_s', 0) / 60)} 分钟。",
            })
        else:
            result.append({"date": date, "papers": 0, "nodes": 0, "edges": 0, "minutes": 0,
                           "summary": "当天没有已完成的科研管线记录。"})
    return result


def paper_insights():
    insights = {"TCC": [], "iNEST": []}
    inbox = VAULT / "00_Inbox" / "_pipeline_insights"
    if not inbox.exists():
        return insights
    # Look at most recent 7 days
    recent_dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
    for path in sorted(inbox.glob("*.md"), reverse=True):
        path_date = path.name[:10]
        if not any(path_date.startswith(d) for d in recent_dates):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        title_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else path.stem
        source_match = re.search(r"^source:\s*(.+)$", text, re.MULTILINE)
        source = source_match.group(1).strip() if source_match else "论文"
        for track, heading in (("TCC", "TCC Insights"), ("iNEST", "iNEST Insights")):
            match = re.search(rf"^##\s+{re.escape(heading)}\s*\n+(.+?)(?=^##\s|\Z)", text, re.MULTILINE | re.DOTALL)
            if match:
                insights[track].append({
                    "title": title[:100],
                    "source": source,
                    "summary": clean_text(match.group(1))[:260],
                    "file": str(path.relative_to(VAULT)).replace("\\", "/"),
                })
        if len(insights["TCC"]) >= 5 and len(insights["iNEST"]) >= 5:
            break
    return {key: value[:5] for key, value in insights.items()}


def deliverables():
    groups = {
        "papers": VAULT / "50_Output" / "51_Papers",
        "patents": VAULT / "50_Output" / "52_Patents",
        "code": VAULT / "50_Output" / "54_Code",
        "guides": VAULT / "50_Output" / "55_Guides",
    }
    result = {}
    for key, folder in groups.items():
        files = list(folder.rglob("*.md")) if folder.exists() else []
        recent = sorted(files, key=lambda f: f.stat().st_mtime, reverse=True)[:5]
        result[key] = [{"name": p.stem, "file": str(p.relative_to(VAULT)).replace("\\", "/"),
                        "updated": datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d")}
                       for p in recent]
    return result


def wiki_state():
    """Read wiki evolution state"""
    wiki = VAULT / "wiki"
    concepts_dir = wiki / "concepts"
    articles_dir = wiki / "articles"
    
    if not concepts_dir.exists():
        return {}
    
    tcc = inest = cross = 0
    for f in concepts_dir.glob("*.md"):
        c = f.read_text(encoding='utf-8')
        if "**Domain**: TCC" in c:
            tcc += 1
        elif "**Domain**: iNEST" in c:
            inest += 1
        elif "**Domain**: Cross" in c:
            cross += 1
    
    num_articles = len(list(articles_dir.glob("*.md"))) if articles_dir.exists() else 0
    
    # Cross-domain bridges
    bridges = []
    bridge_file = wiki / "cross_domain_insights.md"
    if bridge_file.exists():
        content = bridge_file.read_text(encoding='utf-8')
        for block in content.split("### ")[1:]:
            lines = block.strip().split("\n")
            if lines and "(Strength:" in lines[0]:
                name = lines[0].split("(Strength:")[0].strip()
                try:
                    strength = int(lines[0].split("Strength:")[1].split(")")[0].strip())
                except:
                    strength = 0
                insight = lines[1] if len(lines) > 1 else ""
                bridges.append({"name": name, "strength": strength, "insight": insight})
    
    # Evolution health
    health = {"density": "Low", "orphans": 0}
    health_file = wiki / "health.md"
    if health_file.exists():
        hc = health_file.read_text(encoding='utf-8')
        if "Medium" in hc:
            health["density"] = "Medium"
        elif "High" in hc:
            health["density"] = "High"
        om = re.search(r'-\s*\*\*Orphan Concepts\*\*:\s*(\d+)', hc)
        if om:
            health["orphans"] = int(om.group(1))
    
    return {
        "concepts": {"tcc": tcc, "inest": inest, "cross": cross, "total": tcc + inest + cross},
        "articles": num_articles,
        "bridges": bridges[:5],
        "health": health,
    }

def pipeline_status():
    """Read pipeline status"""
    status_file = VAULT / "60_MOC" / "07_Pipeline_Status.md"
    if not status_file.exists():
        return {"status": "unknown", "detail": ""}
    content = status_file.read_text(encoding='utf-8')
    status = "running"
    if "paused" in content.lower():
        status = "paused"
    return {"status": status, "detail": content.strip().split('\n')[0] if content else ""}


def publish():
    DASHBOARD.mkdir(parents=True, exist_ok=True)
    state = load_json(STATE_FILE, {})
    vault = state.get("vault", {})
    payload = {
        "schema": "research-dashboard-v2",
        "date": TODAY,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "state": {
            "total_notes": vault.get("total_md", 0),
            "tcc_notes": vault.get("tcc_30", 0),
            "inest_notes": vault.get("inest_40", 0),
            "pending_papers": vault.get("inbox_00", 0),
            "processing": vault.get("processing_20", 0),
            "outputs": vault.get("output_50", 0),
            "services": state.get("services", {}),
        },
        "wiki": wiki_state(),
        "pipeline": pipeline_status(),
        "task_review": state.get("task_review", {}),
        "plan": current_plan(),
        "progress": recent_runs(),
        "insights": paper_insights(),
        "deliverables": deliverables(),
        "sources": {
            "action": "60_MOC/03_Daily_Action.md",
            "focus": "60_MOC/04_Daily_Focus.md",
            "state": "99_Meta/research_state.json",
            "pipeline": "logs/pipeline_*.json",
            "task_review": "60_MOC/05_Task_Review.md",
            "wiki": "wiki/",
        },
    }
    DATA_FILE.write_text(
        "// Generated by research_publisher.py. Do not edit manually.\n"
        "window.RESEARCH_DASHBOARD = " + json.dumps(payload, ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )
    print(f"[OK] Published dashboard: {DATA_FILE}")
    print(f"  Plan={len(payload['plan'])} Insights=TCC:{len(payload['insights']['TCC'])}/iNEST:{len(payload['insights']['iNEST'])}")


if __name__ == "__main__":
    publish()
