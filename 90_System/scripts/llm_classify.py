#!/usr/bin/env python3
"""LLM batch classifier for ambiguous review files."""
import os, json, time, shutil, re
from pathlib import Path
import urllib.request

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
REVIEW = VAULT / "_archive" / "_needs_review"
PROGRESS = VAULT / "60_MOC" / "_review_progress.json"

API_KEY = "sk-ewvmxpqaoqdmzyrizltymazqkbbzhberrgdwhrinpssoauum"
API_URL = "https://api.siliconflow.cn/v1/chat/completions"
MODEL = "deepseek-ai/DeepSeek-V4-Pro"

TARGETS = {
    "TCC": "30_TCC/31_Theory/_llm_classified",
    "iNEST": "40_iNEST/41_Theory/_llm_classified",
    "Library": "10_Library/Papers/_from_review",
    "Ideas": "20_Ideas/Insights",
    "Archive": "_archive/low_quality",
}

def call_llm(title, content):
    prompt = f"""Classify this research note into EXACTLY ONE category. Output ONLY the category name, nothing else.

Title: {title}
Content preview: {content[:800]}

Categories:
- TCC: Topological Centric Computing (chip/Wafer/SDI/interconnect/semiconductor/routing/CST)
- iNEST: intelligent Emergence (neuromorphic/spiking/brain/emergence/neuron/cognitive/memristor)
- Library: Academic paper/article/literature review/survey
- Ideas: Inspiration/fragment/brainstorm/concept note without clear research direction
- Archive: Low quality/irrelevant/duplicate/trash/meeting notes/personal matters

Category:"""
    
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a research classifier. Output only one word from: TCC, iNEST, Library, Ideas, Archive. No explanation."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 10,
        "temperature": 0.0,
    }
    
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            result = data["choices"][0]["message"]["content"].strip()
            # Normalize
            for cat in TARGETS:
                if cat.lower() in result.lower():
                    return cat
            return result
    except Exception as e:
        print(f"  API error: {e}")
        return None

def main(limit=30, dry_run=False):
    files = sorted(
        [f for f in REVIEW.glob("*.md") if not f.name.startswith(".")],
        key=lambda f: f.stat().st_mtime
    )[:limit]
    
    if not files:
        print("No files to classify.")
        return
    
    print(f"Classifying {len(files)} files (dry_run={dry_run})...")
    
    results = {}
    for i, fp in enumerate(files):
        name = fp.name
        try:
            with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except:
            content = ""
        
        # Extract title from frontmatter or filename
        title = name
        if content.startswith("---"):
            m = re.search(r"title:\s*[\"']?(.+?)[\"']?\n", content)
            if m:
                title = m.group(1)
        
        cat = call_llm(title, content)
        if cat and cat in TARGETS:
            results[name] = cat
            print(f"  [{i+1}/{len(files)}] {cat:8s} | {name[:55]}")
        else:
            results[name] = "Unknown"
            print(f"  [{i+1}/{len(files)}] {'????':8s} | {name[:55]} (API fail)")
        
        if not dry_run and cat and cat in TARGETS:
            dst_dir = VAULT / TARGETS[cat]
            dst_dir.mkdir(parents=True, exist_ok=True)
            dst = dst_dir / name
            if dst.exists():
                dst = dst_dir / (Path(name).stem + "_llm.md")
            shutil.move(str(fp), str(dst))
        
        if i < len(files) - 1:
            time.sleep(0.3)  # Rate limit
    
    # Summary
    counts = {}
    for cat in results.values():
        counts[cat] = counts.get(cat, 0) + 1
    
    print(f"\n=== Results ===")
    for cat, cnt in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {cnt}")
    
    if not dry_run:
        remaining = len(list(REVIEW.glob("*.md")))
        print(f"\nRemaining in review: {remaining}")
        
        # Update progress
        if PROGRESS.exists():
            with open(PROGRESS, "r", encoding="utf-8") as f:
                p = json.load(f)
            for name, cat in results.items():
                if cat in TARGETS:
                    p["reviewed"][name] = {"target": cat, "method": "llm", "time": time.strftime("%Y-%m-%dT%H:%M:%S")}
            with open(PROGRESS, "w", encoding="utf-8") as f:
                json.dump(p, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=30)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    main(limit=args.limit, dry_run=args.dry_run)
