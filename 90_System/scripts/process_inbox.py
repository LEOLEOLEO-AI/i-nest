#!/usr/bin/env python3
"""
Inbox Processor — classify, tag, and link inbox items using LLM.
Moves processed items from 00_Inbox to 10_Library or 20_Ideas.
"""
import os, json, re, time
from pathlib import Path
from datetime import datetime
import sys
sys.path.insert(0, r"D:\Obsidian\scripts")
from llm_router import llm_call

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
INBOX = VAULT / "00_Inbox"
LOG_DIR = VAULT / "logs"

# DeepSeek Official API (DeepSeek V4)

def call_llm(prompt, max_tokens=300):
    """Call LLM via unified router (auto-fallback)."""
    try:
        return llm_call(
            prompt,
            system="You are a research assistant classifying academic papers and notes. Output ONLY valid JSON, no markdown.",
            model_tier="fast",
            max_tokens=max_tokens,
            temperature=0.1
        )
    except Exception as e:
        print(f"  LLM error: {e}")
        return None

def classify_note(content, filename):
    """Classify a note into track and category."""
    prompt = f"""Classify this research note. Output JSON only:
{{
  "track": "TCC" | "iNEST" | "General",
  "category": "Paper" | "Article" | "Concept" | "Insight" | "Fleeting" | "Code" | "Other",
  "tags": ["tag1", "tag2", "tag3"],
  "summary": "one sentence Chinese summary",
  "quality": "high" | "medium" | "low"
}}

Note title: {filename}
Content: {content[:2000]}
"""
    result = call_llm(prompt, max_tokens=200)
    if not result:
        return None
    # Extract JSON
    match = re.search(r'\{.*\}', result, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            pass
    return None

def determine_target(track, category):
    """Determine target directory based on classification."""
    if category in ("Paper", "Article"):
        return f"10_Library/{category}s"
    elif category in ("Concept", "Insight", "Fleeting"):
        return f"20_Ideas/{category}s"
    elif track == "TCC":
        return "30_TCC/31_Theory"
    elif track == "iNEST":
        return "40_iNEST/41_Theory"
    else:
        return "20_Ideas/Insights"

def update_frontmatter(filepath, classification):
    """Add classification tags to note frontmatter."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    tags = classification.get("tags", [])
    tags.append("classified")
    tags_line = "tags: [" + ", ".join(tags) + "]"
    
    if "tags:" in content:
        content = re.sub(r'tags:\s*\[.*?\]', tags_line, content)
    
    # Add summary
    summary = classification.get("summary", "")
    if summary and "## 摘要" not in content:
        content += f"\n\n## AI 摘要\n\n{summary}\n"
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

def move_to_target(filepath, target_dir):
    """Move file to target directory."""
    target = VAULT / target_dir / filepath.name
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        # Add suffix to avoid overwrite
        stem = target.stem
        target = target.parent / f"{stem}_dup.md"
    os.rename(filepath, target)
    return target

def main(dry_run=False, limit=10):
    print(f"\n{'='*60}")
    print(f"Inbox Processor — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'} | Limit: {limit}")
    print(f"{'='*60}")
    
    md_files = sorted(
        [f for f in INBOX.glob("*.md") if f.name != ".gitkeep"],
        key=lambda f: f.stat().st_mtime
    )[:limit]
    
    if not md_files:
        print("\nNo files to process.")
        return
    
    print(f"\nFound {len(md_files)} files to process.\n")
    
    processed = 0
    for fp in md_files:
        print(f"  Processing: {fp.name[:60]}...")
        
        with open(fp, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        
        classification = classify_note(content, fp.name)
        if not classification:
            print(f"    -> SKIP (classification failed)")
            continue
        
        track = classification.get("track", "General")
        category = classification.get("category", "Other")
        quality = classification.get("quality", "medium")
        tags = classification.get("tags", [])
        
        if quality == "low":
            # Move to _archive
            if not dry_run:
                archive = VAULT / "_archive/low_quality"
                archive.mkdir(exist_ok=True)
                os.rename(fp, archive / fp.name)
            print(f"    -> ARCHIVE (low quality)")
            continue
        
        target_dir = determine_target(track, category)
        
        if not dry_run:
            update_frontmatter(fp, classification)
            new_path = move_to_target(fp, target_dir)
            print(f"    -> {new_path.relative_to(VAULT)} [{track}] [{', '.join(tags[:4])}]")
        else:
            print(f"    -> [DRY] {target_dir} [{track}] [{', '.join(tags[:4])}]")
        
        processed += 1
        time.sleep(0.3)
    
    print(f"\nProcessed: {processed} | {'(dry run - no changes)' if dry_run else 'moved to targets'}")
    
    # Write log
    LOG_DIR.mkdir(exist_ok=True)
    logfile = LOG_DIR / f"inbox_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    with open(logfile, "w") as f:
        json.dump({"date": datetime.now().isoformat(), "processed": processed, "dry_run": dry_run}, f)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()
    main(dry_run=args.dry_run, limit=args.limit)

