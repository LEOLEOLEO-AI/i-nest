#!/usr/bin/env python3
"""Promote explicitly approved research proposals into the formal task plan."""
import argparse
import json
from datetime import datetime
from pathlib import Path

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
PROPOSALS = VAULT / "99_Meta" / "research_task_proposals.json"
PLAN = VAULT / "60_MOC" / "06_Task_Plan.md"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", action="append", dest="ids", help="Proposal ID to promote")
    args = parser.parse_args()
    state = json.loads(PROPOSALS.read_text(encoding="utf-8"))
    selected = set(args.ids or [])
    approved = [item for item in state.get("items", [])
                if item.get("status") == "approved" and (not selected or item["id"] in selected)]
    if not approved:
        print("[INFO] No approved proposals to promote")
        return
    plan = PLAN.read_text(encoding="utf-8", errors="replace") if PLAN.exists() else "# Research Task Plan\n"
    marker = "\n## Approved From Research Review\n"
    if marker not in plan:
        plan += marker
    existing = set(line.strip() for line in plan.splitlines() if line.startswith("- [ ] RP-"))
    for item in approved:
        line = f"- [ ] {item['id']} {item['title']} (source: {item['source']})"
        if line not in existing:
            plan += line + "\n"
        item["status"] = "promoted"
        item["promoted_at"] = datetime.now().isoformat(timespec="seconds")
    PLAN.write_text(plan, encoding="utf-8")
    PROPOSALS.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] promoted={len(approved)}")


if __name__ == "__main__":
    main()
