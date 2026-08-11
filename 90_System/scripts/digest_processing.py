# -*- coding: utf-8 -*-
"""Digest 20_Processing backlog (external_imports + inbox_overflow) into 30_TCC / 40_iNEST.

Reuses process_inbox's LLM classify + link logic. Usage:
    python digest_processing.py [--limit N] [--dry-run]
"""
import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, r"D:\Obsidian\vault\90_System\scripts")
from process_inbox import (
    classify_and_extract, find_related_files, add_frontmatter_and_links,
    TCC_DIRS, INEST_DIRS, VAULT,
)

SOURCES = [
    VAULT / "20_Processing" / "external_imports",
    VAULT / "20_Processing" / "inbox_overflow",
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    results = {"moved": 0, "failed": 0, "skipped": 0}
    for src in SOURCES:
        if not src.exists():
            continue
        files = sorted(src.glob("*.md"))[: args.limit]
        for f in files:
            if "日记" in f.name or "journal" in f.name.lower() or "diary" in f.name.lower():
                print("  skip (journal):", f.name)
                results["skipped"] += 1
                continue
            content = f.read_text(encoding="utf-8", errors="replace")
            if len(content.strip()) < 50:
                print("  skip (too short):", f.name)
                results["skipped"] += 1
                continue
            print("  processing:", f.name[:60])
            analysis = classify_and_extract(content, f.name)
            if not analysis:
                print("    LLM failed -> stays in 20_Processing")
                results["failed"] += 1
                continue
            direction = analysis.get("direction", "unknown")
            primary_direction = analysis.get("primary_direction", direction)
            category = analysis.get("category", "资料")
            print("    -> %s/%s : %s" % (direction, category, str(analysis.get("summary", "?"))[:50]))
            related = find_related_files(content, direction)
            if args.dry_run:
                print("    [dry-run] would move with %d links" % len(related))
                continue
            add_frontmatter_and_links(f, analysis, related)
            if primary_direction == "TCC":
                subdir = TCC_DIRS.get(category, "31_Theory")
                dest_dir = VAULT / "30_TCC" / subdir
            elif primary_direction == "iNEST":
                subdir = INEST_DIRS.get(category, "41_Theory")
                dest_dir = VAULT / "40_iNEST" / subdir
            else:
                dest_dir = VAULT / "30_TCC" / "31_Theory"
                primary_direction = "TCC"
            dest_dir.mkdir(parents=True, exist_ok=True)
            new_name = analysis.get("suggested_filename", f.stem)
            if not new_name.endswith(".md"):
                new_name += ".md"
            dest = dest_dir / new_name
            if dest.exists():
                dest = dest_dir / ("%s_%s.md" % (Path(new_name).stem, datetime.now().strftime("%H%M")))
            shutil.move(str(f), str(dest))
            print("    moved -> %s" % dest.relative_to(VAULT))
            results["moved"] += 1
    print("DONE:", results)


if __name__ == "__main__":
    main()
