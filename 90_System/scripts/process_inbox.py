#!/usr/bin/env python3
"""
P1.1: Inbox消化引擎 — LLM分类+标签+双向链接
Inbox → 分类(TCC/iNEST) → 提取观点 → 建立链接 → 移动归档
"""
import os, sys, json, re, shutil
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime
from openai import OpenAI

# Load .env for API keys
try:
    from dotenv import load_dotenv
    load_dotenv(Path(r"D:\Obsidian\vault\.env"), override=True)
except ImportError:
    pass

VAULT = Path(r"D:\Obsidian\vault")
INBOX = VAULT / "00_Inbox"
KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
DEEPSEEK_MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-v4-pro")
client = OpenAI(api_key=KEY, base_url=DEEPSEEK_BASE_URL)

TCC_DIRS = {"理论": "31_Theory", "技术": "32_Technology", "工程": "33_Engineering", "项目": "34_Projects", "仿真": "35_Simulation"}
INEST_DIRS = {"理论": "41_Theory", "技术": "42_Technology", "工程": "43_Engineering", "项目": "44_Projects", "仿真": "45_Simulation"}

def classify_and_extract(content, filename):
    """DeepSeek V4 Pro: classify + tag + summarize + extract insights"""
    prompt = f"""分析以下研究笔记，返回JSON:

笔记标题: {filename}
内容:
{content[:4000]}

返回:
{{
    "direction": "TCC 或 iNEST 或 both",
    "primary_direction": "TCC 或 iNEST；仅 direction=both 时必填，表示主归档方向",
    "category": "理论/技术/工程/项目/仿真/资料",
    "tags": ["tag1", "tag2", "tag3"],
    "summary": "一句话中文摘要(30字内)",
    "key_points": ["核心观点1", "核心观点2"],
    "tcc_insight": "对TCC拓扑中心计算的启发(无则写无)",
    "inest_insight": "对iNEST神经形态计算的启发(无则写无)",
    "actionable": "可转化为什么具体行动(论文方向/专利点/仿真任务/代码开发，无则写无)",
    "quality": "high/medium/low",
    "suggested_filename": "建议文件名(英文,50字内)"
}}"""
    try:
        resp = client.chat.completions.create(
            model=DEEPSEEK_MODEL, messages=[{"role":"user","content":prompt}],
            temperature=0.3, max_tokens=1024, timeout=60
        )
        text = resp.choices[0].message.content
        m = re.search(r'\{[\s\S]*\}', text)
        if m: return json.loads(m.group())
    except Exception as e:
        print(f"  LLM error: {e}")
    return None

def find_related_files(content, direction, top_n=5):
    """Simple keyword+title based related file finder"""
    keywords = set(re.findall(r'[\w\u4e00-\u9fff]{2,}', content.lower()))
    candidates = []
    search_dirs = [VAULT/"30_TCC", VAULT/"40_iNEST"] if direction == "both" else \
                  [VAULT/"30_TCC"] if direction == "TCC" else [VAULT/"40_iNEST"]
    
    for sd in search_dirs:
        if not sd.exists(): continue
        for f in list(sd.rglob("*.md"))[:500]:
            try:
                fc = f.read_text(encoding="utf-8", errors="replace")[:1000].lower()
                score = sum(1 for kw in keywords if kw in fc)
                if score > 2:
                    candidates.append((score, str(f.relative_to(VAULT))))
            except: pass
    
    candidates.sort(reverse=True)
    return [c[1] for c in candidates[:top_n]]

def add_frontmatter_and_links(filepath, analysis, related):
    """Add frontmatter + bidirectional links to file"""
    content = filepath.read_text(encoding="utf-8", errors="replace")
    direction = analysis.get("direction", "unknown")
    tags = ", ".join(analysis.get("tags", []))
    summary = analysis.get("summary", "")
    
    fm = f"""---
direction: {direction}
category: {analysis.get("category", "")}
tags: [{tags}]
summary: "{summary}"
quality: {analysis.get("quality", "medium")}
processed: {datetime.now().strftime("%Y-%m-%d %H:%M")}
---
"""
    # Add links section if not present
    if "## 相关链接" not in content and "## Related" not in content:
        links_section = "\n\n## 相关链接\n"
        for r in related:
            name = Path(r).stem
            links_section += f"- [[{name}]]\n"
        content = fm + content + links_section
    else:
        content = fm + content
    
    filepath.write_text(content, encoding="utf-8")

def process_inbox(dry_run=False, limit=None):
    """Main inbox processor"""
    if not INBOX.exists():
        print("Inbox not found")
        return
    
    md_files = list(INBOX.rglob("*.md"))
    if limit is not None:
        md_files = md_files[:limit]
    if not md_files:
        print("No files in inbox")
        return
    
    print(f"Processing {len(md_files)} inbox files...")
    results = {"TCC": 0, "iNEST": 0, "both": 0, "skipped": 0, "errors": 0}
    
    for f in md_files:
        if "_pipeline_insights" in f.parts:
            continue
        if "日记" in f.name or "journal" in f.name.lower() or "diary" in f.name.lower():
            print(f"    Journal excluded: {f.name}")
            results["skipped"] += 1
            continue
        print(f"\n  [{f.name[:60]}]")
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
            if len(content.strip()) < 50:
                print("    Too short, skipping")
                results["skipped"] += 1
                continue
            
            # Classify
            analysis = classify_and_extract(content, f.name)
            if not analysis:
                print("    LLM failed, moving to 20_Processing")
                dest = VAULT / "20_Processing" / "21_Pending" / f.name
                dest.parent.mkdir(parents=True, exist_ok=True)
                if not dry_run: shutil.move(str(f), str(dest))
                results["errors"] += 1
                continue
            
            direction = analysis.get("direction", "unknown")
            primary_direction = analysis.get("primary_direction", direction)
            category = analysis.get("category", "资料")
            print(f"    → {direction}/{category}: {analysis.get('summary','?')[:60]}")
            
            # Find related files
            related = find_related_files(content, direction)
            if related:
                print(f"    Links: {len(related)} related files")
            
            # Add frontmatter + links
            add_frontmatter_and_links(f, analysis, related)
            
            # Move to target
            if primary_direction == "TCC":
                subdir = TCC_DIRS.get(category, "31_Theory")
                dest_dir = VAULT / "30_TCC" / subdir
            elif primary_direction == "iNEST":
                subdir = INEST_DIRS.get(category, "41_Theory")
                dest_dir = VAULT / "40_iNEST" / subdir
            else:
                # both or unknown → TCC by default
                dest_dir = VAULT / "30_TCC" / "31_Theory"
                primary_direction = "TCC"
            
            dest_dir.mkdir(parents=True, exist_ok=True)
            # Use suggested filename if available
            new_name = analysis.get("suggested_filename", f.stem)
            if not new_name.endswith(".md"): new_name += ".md"
            dest = dest_dir / new_name
            
            if not dry_run:
                if dest.exists():
                    # Add suffix to avoid overwrite
                    dest = dest_dir / f"{Path(new_name).stem}_{datetime.now().strftime('%H%M')}.md"
                shutil.move(str(f), str(dest))
                print(f"    Moved → {dest.relative_to(VAULT)}")
            
            results[primary_direction] += 1
            
        except Exception as e:
            print(f"    ERROR: {e}")
            results["errors"] += 1
    
    print(f"\nDone: TCC={results['TCC']}, iNEST={results['iNEST']}, both={results['both']}, skipped={results['skipped']}, errors={results['errors']}")
    return results

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Inbox digest engine")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=None,
                        help="process at most N files (default: all)")
    args = parser.parse_args()
    process_inbox(dry_run=args.dry_run, limit=args.limit)
