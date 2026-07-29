#!/usr/bin/env python3
"""Create valid, reviewable research-task proposals from evidence notes."""

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

VAULT = Path(r"D:\Obsidian\vault")
INSIGHTS = VAULT / "00_Inbox" / "_pipeline_insights"
FULLTEXT_ANALYSES = VAULT / "20_Processing" / "02_Fulltext_Analysis"
META = VAULT / "99_Meta"
REVIEW_NOTE = VAULT / "60_MOC" / "05_Task_Review.md"
PROPOSALS = META / "research_task_proposals.json"
NOW = datetime.now(ZoneInfo("Asia/Shanghai"))
TODAY = NOW.date()


def extract_section(text, heading):
    match = re.search(rf"^##\s+{re.escape(heading)}\s*$", text, re.MULTILINE)
    if not match:
        return ""
    tail = text[match.end():]
    next_heading = re.search(r"^##\s+", tail, re.MULTILINE)
    return tail[: next_heading.start() if next_heading else None].strip()


def bullet_items(text):
    return [re.sub(r"^[-*]\s+", "", line).strip() for line in text.splitlines()
            if re.match(r"^[-*]\s+", line) and line.strip()]


def actionable_items(text):
    items = []
    for section_name in ("Actionable", "Candidate Tasks"):
        items.extend(bullet_items(extract_section(text, section_name)))
    invalid = {"", "none", "n/a", "na", "\u65e0", "\u6682\u65e0"}
    return [item for item in items if item.strip().lower() not in invalid]


def insight_items(text):
    values = []
    for section_name in ("TCC Insights", "iNEST Insights"):
        values.extend(bullet_items(extract_section(text, section_name)))
    return values[:3]


def load_existing():
    if not PROPOSALS.exists():
        return {"schema": "research-task-proposals-v1", "items": []}
    try:
        return json.loads(PROPOSALS.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        backup = PROPOSALS.with_name(
            f"{PROPOSALS.stem}.invalid_{NOW:%Y%m%d_%H%M%S}{PROPOSALS.suffix}"
        )
        PROPOSALS.replace(backup)
        return {"schema": "research-task-proposals-v1", "items": []}


def write_json_atomic(path, payload):
    serialized = json.dumps(payload, ensure_ascii=False, indent=2)
    json.loads(serialized)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(serialized + "\n", encoding="utf-8")
    temporary.replace(path)


def candidate_sources():
    insight_paths = INSIGHTS.glob(f"{TODAY:%Y-%m-%d}_*.md")
    fulltext_paths = (
        path for path in FULLTEXT_ANALYSES.glob("*.md")
        if datetime.fromtimestamp(path.stat().st_mtime).date() == TODAY
    )
    return sorted([*insight_paths, *fulltext_paths])


def write_review_note(items):
    title = "\u7814\u7a76\u4efb\u52a1\u786e\u8ba4\u961f\u5217"
    lines = [f"# {title} - {TODAY:%Y-%m-%d}", "",
             "> \u8fd9\u91cc\u53ea\u751f\u6210\u5019\u9009\u4efb\u52a1\uff1b\u6279\u51c6\u524d\u4e0d\u4f1a\u5199\u5165\u6b63\u5f0f\u5de5\u4f5c\u8ba1\u5212\u3002", ""]
    pending = [item for item in items if item.get("status") == "pending_review"]
    if not pending:
        lines.append("\u5f53\u524d\u6ca1\u6709\u5f85\u786e\u8ba4\u5019\u9009\u4efb\u52a1\u3002")
    for item in pending:
        lines.extend([
            f"## {item['id']}",
            f"- \u72b6\u6001: `{item['status']}`",
            f"- \u5019\u9009\u4efb\u52a1: {item['title']}",
            f"- \u6765\u6e90: [[{Path(item['source']).stem}]]",
            f"- \u8bc1\u636e: {item['evidence']}",
            "- \u786e\u8ba4\u65b9\u5f0f: \u5c06 JSON \u4e2d\u8be5\u6761\u76ee\u7684 `status` \u6539\u4e3a `approved`\uff0c\u518d\u8fd0\u884c `approve_research_tasks.py`\u3002",
            "",
        ])
    REVIEW_NOTE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    META.mkdir(parents=True, exist_ok=True)
    state = load_existing()
    existing = {item["id"]: item for item in state.get("items", []) if item.get("id")}

    for path in candidate_sources():
        text = path.read_text(encoding="utf-8", errors="replace")
        insights = insight_items(text)
        for action in actionable_items(text):
            digest = hashlib.sha1(f"{path.name}\n{action}".encode("utf-8")).hexdigest()[:12]
            proposal_id = f"RP-{TODAY:%Y-%m-%d}-{digest}"
            existing.setdefault(proposal_id, {
                "id": proposal_id,
                "status": "pending_review",
                "title": action,
                "source": str(path.relative_to(VAULT)).replace("\\", "/"),
                "evidence": "[\u5f15\u7528] \u539f\u59cb\u6587\u732e\u6d1e\u5bdf\u6587\u4ef6\uff0c\u9700\u4eba\u5de5\u6838\u9a8c\u540e\u6267\u884c\u3002",
                "inspiration": insights,
                "created": NOW.isoformat(timespec="seconds"),
            })

    items = sorted(existing.values(), key=lambda item: item.get("created", ""), reverse=True)
    state = {
        "schema": "research-task-proposals-v1",
        "generated": NOW.isoformat(timespec="seconds"),
        "items": items,
    }
    write_json_atomic(PROPOSALS, state)
    write_review_note(items)
    pending = sum(item.get("status") == "pending_review" for item in items)
    print(f"[OK] proposals={len(items)} pending={pending}")


if __name__ == "__main__":
    main()
