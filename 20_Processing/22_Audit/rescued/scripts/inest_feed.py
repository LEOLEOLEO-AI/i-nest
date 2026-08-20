#!/usr/bin/env python3
"""
iNEST Intelligence Feed -- organic research dashboard
=====================================================
Modes:
  feed        Daily: literature -> inspiration pool -> update dashboard
  consolidate Weekly: scan inspirations -> suggest paper/patent threads  
  kanban      Show/set engineering focus module
  dashboard   Rebuild homepage from current state

Architecture:
  iNEST-Home.md          Top-level dashboard
  iNEST_г/           Flowing inspiration notes (1 per paper)
  iNEST_4_̿/.md  Single active module + progress
  iNEST_1_Ŀ߻/·ͼ.md Evolving roadmap
"""

import sys, io, os, re, json, yaml, time, subprocess
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from openai import OpenAI

#  Paths 
AGENT_ROOT = Path(r"D:\\Obsidian\\Agent")
VAULT = Path(r"D:\Obsidian\vault")
NMT_ROOT = Path(r"D:\iNEST\neuromorphic_tools")
INSPIRATION_DIR = VAULT / "iNEST_г"
HOME_PATH = VAULT / "iNEST-Home.md"
KANBAN_PATH = VAULT / "iNEST_4_̿" / ".md"
ROADMAP_PATH = VAULT / "iNEST_1_Ŀ߻" / "·ͼ.md"
SCRIPTS_DIR = AGENT_ROOT / "scripts"

API_KEY = os.environ.get("SILICONFLOW_API_KEY", "")
API_BASE = "https://api.siliconflow.cn/v1"
MODEL = "deepseek-ai/DeepSeek-V3.2"

#  Research Threads 
THREADS = {
    "criticality": "֯ٽӿ",
    "topology": "",
    "plasticity": "ͻѧϰ",
    "embodied": "",
    "wafer": "ԲоƬ",
    "snn": "Ӳ",
    "reservoir": "ؼ",
    "lnn": "Һ̬",
    "free-energy": "ԭ",
    "sdi": "廥",
}

def call_llm(prompt, max_tokens=1500, temp=0.5):
    client = OpenAI(api_key=API_KEY, base_url=API_BASE, timeout=180)
    r = client.chat.completions.create(
        model=MODEL,
        messages=[{"role":"system","content":"Output ONLY valid JSON, no markdown."},
                  {"role":"user","content":prompt}],
        max_tokens=max_tokens, temperature=temp
    )
    raw = r.choices[0].message.content.strip()
    if raw.startswith("```"): raw = raw.split("\n",1)[1][:-3] if raw.endswith("```") else raw.split("\n",1)[1]
    return raw


# TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
# MODE: feed -- daily literature -> inspiration
# TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
def mode_feed(dry_run=False):
    """Daily: fetch latest papers -> brief inspiration notes -> update dashboard."""
    print("[feed] Starting daily intelligence feed...")
    today = datetime.now().strftime("%Y-%m-%d")
    today_ts = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 1. Find latest search results
    results_dir = AGENT_ROOT / "generated_docs"
    json_files = sorted(results_dir.glob("results_*.json"), reverse=True)
    if not json_files:
        print("[feed] No search results found. Run literature search first.")
        return
    latest = json_files[0]
    data = json.loads(latest.read_text(encoding="utf-8"))
    papers = data.get("artifacts", {}).get("search_digest", {}).get("papers", [])
    if not papers:
        print("[feed] No papers in search results.")
        return

    # 2. Check which papers already have inspiration notes
    existing = set()
    for f in INSPIRATION_DIR.glob("*.md"):
        text = f.read_text(encoding="utf-8", errors="ignore")[:500]
        m = re.search(r'paper_title:\s*"(.+?)"', text)
        if m: existing.add(m.group(1).strip().lower()[:80])

    new_papers = [p for p in papers if p.get("title","").strip().lower()[:80] not in existing]
    print(f"[feed] Papers: {len(papers)} total, {len(new_papers)} new")

    if not new_papers:
        print("[feed] All papers already processed. Updating dashboard only.")
        mode_dashboard(dry_run)
        return

    # 3. For each new paper, generate a brief inspiration note
    inspirations = []
    for i, p in enumerate(new_papers[:8], 1):  # max 8 per day
        title = p.get("title", "?")
        abstract = (p.get("abstract") or "")[:800]
        source = p.get("source", "?")
        year = p.get("year", "?")
        print(f"  [{i}/{min(len(new_papers),8)}] {title[:70]}...")

        prompt = f"""Analyze this paper briefly for iNEST research (Physical Complex Network Intelligence Emergence).
Output JSON:
{{
  "core_insight": "one sentence: what is the key finding relevant to iNEST",
  "thread": "which research thread does this connect to (criticality/topology/plasticity/embodied/wafer/snn/reservoir/lnn/free-energy/sdi)",
  "inspiration": "2-3 sentences: what new idea or direction does this suggest for iNEST",
  "action": "concrete next action (e.g. simulate X with Y, read section Z, compare with A)",
  "tags": ["tag1", "tag2"]
}}

Paper: {title} ({year})
Abstract: {abstract}"""

        try:
            raw = call_llm(prompt, max_tokens=600, temp=0.5)
            analysis = json.loads(raw)
        except:
            analysis = {"core_insight":"Auto-extracted","thread":"topology","inspiration":"Review needed","action":"Read full paper","tags":["to-review"]}

        thread = analysis.get("thread", "topology")
        thread_name = THREADS.get(thread, thread)

        note = f"""---
paper_title: "{title}"
source: "{source}"
year: {year}
date: {today}
thread: "{thread}"
tags: [inspiration, {thread}, {', '.join(analysis.get('tags', []))}]
---

# ?? {title}

**{analysis.get('core_insight','')}**

## о߹
߳: **{thread_name}**

{analysis.get('inspiration','')}

## һж
- [ ] {analysis.get('action','')}

---
*Դ: {source} ({year})*
"""
        filename = re.sub(r'[^\w\s-]','', title)[:100].strip()
        filepath = INSPIRATION_DIR / f"{today}_{filename}.md"
        if not dry_run:
            filepath.write_text(note, encoding="utf-8")
        inspirations.append({
            "title": title, "thread": thread, "insight": analysis.get("core_insight",""),
            "filename": filepath.name
        })
        time.sleep(0.5)

    print(f"[feed] Generated {len(inspirations)} inspiration notes")

    # 4. Update dashboard
    mode_dashboard(dry_run, inspirations=inspirations)
    return inspirations


# TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
# MODE: consolidate -- weekly pattern recognition
# TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
def mode_consolidate(dry_run=False):
    """Weekly: scan inspiration pool -> identify patterns -> suggest threads."""
    print("[consolidate] Scanning inspiration pool...")
    today = datetime.now().strftime("%Y-%m-%d")
    week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    # Collect recent inspirations
    recent = []
    for f in sorted(INSPIRATION_DIR.glob("*.md"), reverse=True):
        text = f.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r'date:\s*(\d{4}-\d{2}-\d{2})', text)
        if m:
            note_date = m.group(1)
            if note_date >= week_ago:
                recent.append((f.stem, text[:2000]))

    if not recent:
        print("[consolidate] No recent inspirations to consolidate.")
        return

    print(f"[consolidate] {len(recent)} inspirations from past 7 days")

    # LLM pattern recognition
    snippets = "\n---\n".join([f"## {t}\n{c[:500]}" for t,c in recent[:15]])
    prompt = f"""Review these recent iNEST research inspirations and identify:
1. Emerging patterns across papers
2. 1-2 concrete paper ideas (with research questions, not just titles)
3. 1-2 patent directions (technical novelty areas)
4. Suggested focus for the engineering module
5. Updated project priorities

Recent inspirations:
{snippets}

Return JSON with: patterns, paper_directions, patent_directions, engineering_focus, project_priorities"""

    try:
        raw = call_llm(prompt, max_tokens=2000, temp=0.4)
        consolidation = json.loads(raw)
    except:
        consolidation = {"patterns":["Auto-consolidation failed"],"paper_directions":[],"patent_directions":[],"engineering_focus":"Continue current module","project_priorities":"Unchanged"}

    # Write consolidation note
    patterns = consolidation.get("patterns", [])
    paper_dirs = consolidation.get("paper_directions", [])
    patent_dirs = consolidation.get("patent_directions", [])

    note = f"""---
date: {today}
tags: [consolidation, weekly-review]
type: consolidation
---

# о̬ ({today})

## ֵģʽ
"""
    for p in patterns:
        note += f"- {p}\n"

    note += "\n## ķ\n"
    for pd in paper_dirs:
        note += f"- **{pd.get('direction','')}**: {pd.get('question','')}\n"

    note += "\n## ר\n"
    for pd in patent_dirs:
        note += f"- **{pd.get('area','')}**: {pd.get('novelty','')}\n"

    note += f"\n## ̽\n{consolidation.get('engineering_focus','')}\n"
    note += f"\n## Ŀȼ\n{consolidation.get('project_priorities','')}\n"

    filepath = INSPIRATION_DIR / f"{today}_weekly-consolidation.md"
    if not dry_run:
        filepath.write_text(note, encoding="utf-8")
    print(f"[consolidate] Written: {filepath.name}")
    return consolidation


# TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
# MODE: kanban -- engineering focus management
# TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
def mode_kanban(action="show", module_name=None, task=None):
    """Manage the engineering kanban board."""
    if not KANBAN_PATH.exists():
        KANBAN_PATH.write_text("""---
tags: [kanban, engineering]
updated: ""
---

# ̿

## ǰ۽ģ
**

## 嵥
- [ ] ȷǰģ

## ģ
**
""", encoding="utf-8")
        print("[kanban] Created engineering kanban")

    content = KANBAN_PATH.read_text(encoding="utf-8")

    if action == "set":
        today = datetime.now().strftime("%Y-%m-%d")
        content = re.sub(r'## ǰ۽ģ\n\*.*?\*', f'## ǰ۽ģ\n*{module_name}*', content)
        if task:
            content = re.sub(r'## 嵥\n', f'## 嵥\n- [ ] {task}\n', content)
        content = content.replace('updated: ""', f'updated: "{today}"')
        if not dry_run_local:
            KANBAN_PATH.write_text(content, encoding="utf-8")
        print(f"[kanban] Set focus: {module_name}")

    # Display
    focus = re.search(r'## ǰ۽ģ\n\*(.+?)\*', content)
    tasks = re.findall(r'- \[(.)\] (.+)', content)
    print(f"\nǰ۽: {focus.group(1) if focus else 'δ'}")
    print(":")
    for status, task_text in tasks:
        print(f"  [{'x' if status == 'x' else ' '}] {task_text}")


# TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
# MODE: dashboard -- build/update homepage
# TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
def mode_dashboard(dry_run=False, inspirations=None):
    """Rebuild the iNEST-Home.md dashboard."""
    today = datetime.now().strftime("%Y-%m-%d")
    today_ts = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Gather data from all sources
    # Recent inspirations
    recent_inspirations = []
    for f in sorted(INSPIRATION_DIR.glob("*.md"), reverse=True)[:20]:
        text = f.read_text(encoding="utf-8", errors="ignore")
        m_title = re.search(r'paper_title:\s*"(.+?)"', text)
        m_thread = re.search(r'thread:\s*"(.+?)"', text)
        title = m_title.group(1)[:80] if m_title else f.stem[:80]
        thread = m_thread.group(1) if m_thread else "general"
        recent_inspirations.append({"title": title, "thread": thread, "file": f.name})

    # Thread summary
    thread_count = Counter(i["thread"] for i in recent_inspirations)

    # Engineering kanban summary
    eng_focus = "δ"
    eng_tasks = []
    if KANBAN_PATH.exists():
        k_content = KANBAN_PATH.read_text(encoding="utf-8")
        m = re.search(r'## ǰ۽ģ\n\*(.+?)\*', k_content)
        if m: eng_focus = m.group(1)
        eng_tasks = re.findall(r'- \[(.)\] (.+)', k_content)

    # Roadmap
    roadmap_summary = "·ͼ"
    if ROADMAP_PATH.exists():
        r_content = ROADMAP_PATH.read_text(encoding="utf-8")
        m = re.search(r'## ǰ׶\n(.+?)(?:\n##|\Z)', r_content, re.DOTALL)
        if m: roadmap_summary = m.group(1).strip()[:200]

    # Build dashboard
    dash = f"""---
cssclass: dashboard
tags: [dashboard, home]
updated: {today_ts}
---

# ?? iNEST оǱ

> : {today_ts} | [[iNEST_г/|г]] | [[iNEST_4_̿/|̿]] | [[iNEST_1_Ŀ߻/·ͼ|·ͼ]]

---

## ??  ({today})

"""
    if inspirations:
        for insp in inspirations:
            thread_name = THREADS.get(insp["thread"], insp["thread"])
            dash += f"- ?? [[iNEST_г/{insp['filename']}|{insp['title'][:60]}]]  **{thread_name}**\n"
    else:
        dash += "**\n"

    dash += f"""

---

## ?? гظ

>  {len(recent_inspirations)} У̷ֲ߳

"""
    for thread, count in thread_count.most_common(8):
        thread_name = THREADS.get(thread, thread)
        dash += f"- **{thread_name}**: {count} \n"

    dash += f"""

---

## ?? ̿

> ǰ۽: **{eng_focus}**
"""
    completed = sum(1 for s, _ in eng_tasks if s == 'x')
    total = len(eng_tasks)
    if total > 0:
        dash += f"\n: {completed}/{total}\n"
        for status, task_text in eng_tasks[-8:]:
            icon = "?" if status == 'x' else "?"
            dash += f"- {icon} {task_text}\n"

    dash += f"""

---

## ?? Ŀ·ͼ

{roadmap_summary}

---

## ?? 
"""
    # Find consolidation notes for paper directions
    consolidations = sorted(INSPIRATION_DIR.glob("*consolidation*.md"), reverse=True)[:2]
    for c in consolidations:
        text = c.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r'## ķ\n(.+?)(?:\n##|\Z)', text, re.DOTALL)
        if m:
            dash += f"\n### [{c.stem}](iNEST_г/{c.name})\n{m.group(1).strip()[:300]}\n"

    dash += f"""

---

## ?? ר
"""
    for c in consolidations:
        text = c.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r'## ר\n(.+?)(?:\n##|\Z)', text, re.DOTALL)
        if m:
            dash += f"\n{m.group(1).strip()[:300]}\n"

    dash += f"""

---

## ?? ù ({len(list(NMT_ROOT.iterdir()))} )

"""
    for d in sorted(NMT_ROOT.iterdir()):
        if d.is_dir() and not d.name.startswith('.'):
            has_examples = any(d.rglob("*.py"))
            icon = "??" if has_examples else "??"
            dash += f"- {icon} **{d.name}**\n"

    dash += f"""

---

## ?? ݵ

- [[iNEST_г/|?? г]]
- [[iNEST_1_Ŀ߻/·ͼ|?? ·ͼ]]
- [[iNEST_2_׫д/|?? ]]
- [[iNEST_3_ר׫д/|?? ר]]
- [[iNEST_4_̿/|?? ̿]]
- [[01_MOC/|??? ֪ʶ⵼]]
- [[KB-Optimization-Report|?? ֪ʶⱨ]]
"""

    if not dry_run:
        HOME_PATH.write_text(dash, encoding="utf-8")
        print(f"[dashboard] Written: {HOME_PATH}")

    return dash


# TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
# Main
# TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
def main():
    import argparse
    parser = argparse.ArgumentParser(description="iNEST Intelligence Feed")
    parser.add_argument("--mode", choices=["feed","consolidate","kanban","dashboard","kanban-set"],
                        default="feed", help="Operation mode")
    parser.add_argument("--module", help="Engineering module name (for kanban-set)")
    parser.add_argument("--task", help="Task to add (for kanban-set)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    global dry_run_local
    dry_run_local = args.dry_run

    if args.mode == "feed":
        mode_feed(args.dry_run)
    elif args.mode == "consolidate":
        mode_consolidate(args.dry_run)
    elif args.mode == "kanban":
        mode_kanban("show")
    elif args.mode == "kanban-set":
        mode_kanban("set", args.module, args.task)
    elif args.mode == "dashboard":
        mode_dashboard(args.dry_run)

    print("\nDone.")


if __name__ == "__main__":
    dry_run_local = False
    main()

