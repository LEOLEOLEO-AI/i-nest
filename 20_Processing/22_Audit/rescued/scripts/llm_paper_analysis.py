#!/usr/bin/env python3
"""
LLM-Powered Paper Deep Analysis
Reads search digest results, calls DeepSeek-V4-Pro for each paper,
and writes structured analysis notes to the Obsidian knowledge base.

Usage:
    python llm_paper_analysis.py                          # analyze latest results
    python llm_paper_analysis.py --input results_xxx.json # specific file
    python llm_paper_analysis.py --max-papers 5           # limit to N papers
    python llm_paper_analysis.py --dry-run                # preview without writing
"""

import json
import os
import sys
import time
import argparse
from pathlib import Path
from datetime import datetime
from openai import OpenAI

# ── Configuration ──────────────────────────────────────────────
AGENT_ROOT = Path(r"D:\\Obsidian\\Agent")
OBSIDIAN_VAULT = Path(r"D:\Obsidian\vault")
OBSIDIAN_PAPERS_DIR = OBSIDIAN_VAULT / "03_Topics" / "Papers"
OBSIDIAN_MOC_DIR = OBSIDIAN_VAULT / "01_MOC"
GENERATED_DOCS = AGENT_ROOT / "generated_docs"

API_KEY = os.environ.get(
    "SILICONFLOW_API_KEY",
    "YOUR_SILICONFLOW_API_KEY_HERE"
)
API_BASE = "https://api.siliconflow.cn/v1"
MODEL = "deepseek-ai/DeepSeek-V3.2"

# ── iNEST Research Context ─────────────────────────────────────
INEST_CONTEXT = """
iNEST (intelligent Nest) is a research framework investigating 
"Physical Complex Network Intelligence Emergence" - how intelligence 
emerges from physical complex network dynamics. Key themes:
1. Complex networks (scale-free, small-world, modular)
2. Critical phenomena & self-organized criticality in neural systems
3. Neural dynamics & synaptic plasticity
4. Embodied AI & sensorimotor integration
5. Wafer-scale / chiplet integration for neuromorphic hardware
6. Free energy principle & predictive processing
7. Higher-order network topology & dynamics
"""

ANALYSIS_PROMPT = """You are a senior research scientist analyzing papers for the iNEST research framework.

iNEST studies "Physical Complex Network Intelligence Emergence" - how intelligence emerges from physical complex network dynamics. Key themes: complex networks, critical phenomena, neural dynamics, embodied AI, wafer-scale integration, free energy principle.

Analyze the following paper and output a JSON object with these fields:
{
    "core_contribution": "One paragraph summarizing the main contribution",
    "methodology": "How they did it (experimental, theoretical, computational)",
    "key_findings": ["finding 1", "finding 2", "finding 3"],
    "limitations": ["limitation 1", "limitation 2"],
    "inest_relevance": {
        "score": 0.0-1.0,
        "themes": ["matching iNEST themes"],
        "explanation": "Why this matters for iNEST"
    },
    "cross_connections": ["potential links to other research areas"],
    "research_gaps": ["gaps this paper reveals"],
    "next_steps": "What iNEST should do with this insight",
    "tags": ["relevant", "obsidian", "tags"]
}

Paper to analyze:
Title: {title}
Year: {year}
Source: {source}
Abstract: {abstract}

Return ONLY valid JSON, no markdown fences, no commentary."""


def find_latest_results():
    """Find the most recent search results JSON."""
    json_files = sorted(GENERATED_DOCS.glob("results_*.json"), reverse=True)
    for f in json_files:
        with open(f, "r", encoding="utf-8") as fh:
            data = json.load(fh)
            if data.get("artifacts", {}).get("search_digest", {}).get("papers"):
                return f, data
    return None, None


def load_papers(results_path=None):
    """Load papers from search results."""
    if results_path:
        path = Path(results_path)
    else:
        path, _ = find_latest_results()
        if not path:
            print("No results found.")
            sys.exit(1)

    print(f"Loading: {path}", flush=True)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    papers = data.get("artifacts", {}).get("search_digest", {}).get("papers", [])
    must_read = data.get("artifacts", {}).get("search_digest", {}).get("must_read", [])
    
    # Deduplicate by title
    seen = set()
    unique = []
    for p in papers:
        t = p.get("title", "").strip().lower()
        if t and t not in seen:
            seen.add(t)
            unique.append(p)
    
    # Mark must-read papers
    must_read_titles = {m.get("title", "").strip().lower() for m in must_read}
    for p in unique:
        p["is_must_read"] = p.get("title", "").strip().lower() in must_read_titles

    print(f"Papers: {len(unique)} (must-read: {len(must_read_titles)})", flush=True)
    return unique


def safe_filename(title):
    """Convert paper title to a safe filename."""
    safe = "".join(c if c.isalnum() or c in " _-()[]" else "_" for c in title)
    safe = safe.strip()[:120]
    return safe or "untitled"


def analyze_paper(client, paper, retries=2):
    """Call DeepSeek to analyze a single paper."""
    title = paper.get("title", "Unknown")
    abstract = paper.get("abstract", "") or "No abstract available."
    year = paper.get("year", "?")
    source = paper.get("source", "?")

    prompt = (ANALYSIS_PROMPT
        .replace("{title}", title)
        .replace("{year}", str(year))
        .replace("{source}", source)
        .replace("{abstract}", abstract[:3000])
    )

    for attempt in range(retries + 1):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": "You are a precise research analyst. Output ONLY valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2048,
                timeout=180,
            )
            raw = response.choices[0].message.content.strip()
            # Clean markdown fences if present
            if raw.startswith("```"):
                raw = raw.split("\n", 1)[1]
                if raw.endswith("```"):
                    raw = raw[:-3]
            return json.loads(raw)
        except json.JSONDecodeError:
            if attempt < retries:
                time.sleep(2)
                continue
            return {"error": "JSON parse failed", "raw": raw[:500]}
        except Exception as e:
            if attempt < retries:
                time.sleep(3 * (attempt + 1))
                continue
            return {"error": str(e)}

    return {"error": "max retries exceeded"}


def format_obsidian_note(paper, analysis, timestamp):
    """Format analysis as an Obsidian Markdown note with YAML frontmatter."""
    title = paper.get("title", "Unknown")
    year = paper.get("year", "?")
    source = paper.get("source", "?")
    url = paper.get("url", "")
    authors = paper.get("authors", [])
    is_must_read = paper.get("is_must_read", False)
    citations = paper.get("citation_count", 0)
    abstract = paper.get("abstract", "") or ""

    tags = analysis.get("tags", ["paper", "literature-map"])
    relevance = analysis.get("inest_relevance", {})
    score = relevance.get("score", 0)
    themes = relevance.get("themes", [])

    lines = ["---"]
    lines.append(f'title: "{title}"')
    lines.append(f"year: {year}")
    lines.append(f'source: "{source}"')
    lines.append(f"tags: [{', '.join(tags)}]")
    lines.append(f'inest_score: {score}')
    if is_must_read:
        lines.append("must_read: true")
    lines.append(f"analyzed: {timestamp}")
    lines.append("---")
    lines.append("")
    lines.append(f"# {title}")
    lines.append("")
    if is_must_read:
        lines.append("> [!important] Must-Read Paper")
        lines.append("")
    
    # Meta info
    lines.append(f"- **Year**: {year}")
    lines.append(f"- **Source**: {source}")
    if citations:
        lines.append(f"- **Citations**: {citations}")
    if url:
        lines.append(f"- **URL**: [{url}]({url})")
    if authors:
        author_list = ", ".join(authors[:5])
        if len(authors) > 5:
            author_list += f" et al. ({len(authors)} authors)"
        lines.append(f"- **Authors**: {author_list}")
    lines.append("")

    # iNEST relevance
    lines.append("## iNEST Relevance")
    lines.append(f"**Score**: {score:.2f} | **Themes**: {', '.join(themes) if themes else 'N/A'}")
    lines.append(f"**Why**: {relevance.get('explanation', 'N/A')}")
    lines.append("")

    # Core contribution
    lines.append("## Core Contribution")
    lines.append(analysis.get("core_contribution", "N/A"))
    lines.append("")

    # Key findings
    findings = analysis.get("key_findings", [])
    if findings:
        lines.append("## Key Findings")
        for f in findings:
            lines.append(f"- {f}")
        lines.append("")

    # Methodology
    lines.append("## Methodology")
    lines.append(analysis.get("methodology", "N/A"))
    lines.append("")

    # Limitations
    limitations = analysis.get("limitations", [])
    if limitations:
        lines.append("## Limitations")
        for l in limitations:
            lines.append(f"- {l}")
        lines.append("")

    # Cross connections
    connections = analysis.get("cross_connections", [])
    if connections:
        lines.append("## Cross-Connections")
        for c in connections:
            lines.append(f"- {c}")
        lines.append("")

    # Research gaps
    gaps = analysis.get("research_gaps", [])
    if gaps:
        lines.append("## Research Gaps")
        for g in gaps:
            lines.append(f"- {g}")
        lines.append("")

    # Next steps
    lines.append("## Next Steps for iNEST")
    lines.append(analysis.get("next_steps", "N/A"))
    lines.append("")

    # Abstract
    if abstract and abstract != "No abstract available.":
        lines.append("## Abstract")
        lines.append(f"> {abstract}")
        lines.append("")

    return "\n".join(lines)


def generate_moc(analyzed_papers, timestamp):
    """Generate a Map of Content page for all analyzed papers."""
    lines = ["---"]
    lines.append(f"date: {timestamp}")
    lines.append("tags: [MOC, literature-map, auto-generated]")
    lines.append("---")
    lines.append("")
    lines.append("# Literature Map MOC")
    lines.append(f"Auto-generated: {timestamp}")
    lines.append("")
    lines.append(f"**Total papers analyzed**: {len(analyzed_papers)}")
    lines.append("")

    # Group by iNEST score
    high = [p for p in analyzed_papers if p.get("_score", 0) >= 0.7]
    mid = [p for p in analyzed_papers if 0.4 <= p.get("_score", 0) < 0.7]
    low = [p for p in analyzed_papers if p.get("_score", 0) < 0.4]

    if high:
        lines.append("## [MUST-READ] High Relevance (score >= 0.7)")
        for p in high:
            lines.append(f"- [[{p['_filename']}|{p['title']}]] (score: {p['_score']:.2f})")
        lines.append("")

    if mid:
        lines.append("## [MID] Medium Relevance (0.4 <= score < 0.7)")
        for p in mid:
            lines.append(f"- [[{p['_filename']}|{p['title']}]] (score: {p['_score']:.2f})")
        lines.append("")

    if low:
        lines.append("## [BG] Background / Low Relevance (score < 0.4)")
        for p in low:
            lines.append(f"- [[{p['_filename']}|{p['title']}]] (score: {p['_score']:.2f})")
        lines.append("")

    # By source
    lines.append("## By Source")
    sources = {}
    for p in analyzed_papers:
        src = p.get("source", "unknown")
        sources.setdefault(src, []).append(p)
    for src, papers in sorted(sources.items()):
        lines.append(f"- **{src}** ({len(papers)} papers)")

    return "\n".join(lines)


def main():
# stdout wrapper removed
    parser = argparse.ArgumentParser(description="LLM Paper Deep Analysis for iNEST")
    parser.add_argument("--input", help="Specific results JSON file")
    parser.add_argument("--max-papers", type=int, default=10, help="Max papers to analyze")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--obsidian-dir", default=str(OBSIDIAN_PAPERS_DIR),
                        help="Obsidian papers output directory")
    args = parser.parse_args()

    papers = load_papers(args.input)
    papers = papers[:args.max_papers]

    client = OpenAI(api_key=API_KEY, base_url=API_BASE)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    date_tag = datetime.now().strftime("%Y%m%d")

    obsidian_dir = Path(args.obsidian_dir)
    if not args.dry_run:
        obsidian_dir.mkdir(parents=True, exist_ok=True)

    analyzed = []

    for i, paper in enumerate(papers, 1):
        title = paper.get("title", "Unknown")
        print(f"\n[{i}/{len(papers)}] {title[:80]}...")

        analysis = analyze_paper(client, paper)
        
        if "error" in analysis:
            print(f"  SKIP: {analysis['error']}")
            continue

        score = analysis.get("inest_relevance", {}).get("score", 0)
        must = "[MUST-READ]" if paper.get("is_must_read") else ""
        print(f"  iNEST score: {score:.2f} {must}", flush=True)

        filename = safe_filename(title)
        note = format_obsidian_note(paper, analysis, timestamp)

        if args.dry_run:
            print(f"  [DRY-RUN] Would write: {filename}.md ({len(note)} chars)")
        else:
            filepath = obsidian_dir / f"{filename}.md"
            filepath.write_text(note, encoding="utf-8")
            print(f"  Wrote: {filepath.name}")

        analyzed.append({
            "title": title,
            "_filename": filename,
            "_score": score,
            "source": paper.get("source", "?"),
            "year": paper.get("year", "?"),
            "inest_relevance": analysis.get("inest_relevance", {}),
            "tags": analysis.get("tags", []),
        })

        time.sleep(1)  # Rate limit

    # Generate MOC
    if analyzed:
        moc = generate_moc(analyzed, timestamp)
        moc_filename = f"Literature-Map-{date_tag}.md"

        if args.dry_run:
            print(f"\n[DRY-RUN] Would write MOC: {moc_filename}")
        else:
            moc_path = OBSIDIAN_MOC_DIR / moc_filename
            OBSIDIAN_MOC_DIR.mkdir(parents=True, exist_ok=True)
            moc_path.write_text(moc, encoding="utf-8")
            print(f"\nMOC written: {moc_path}")

        # Save analysis digest JSON
        digest = {
            "timestamp": timestamp,
            "total_analyzed": len(analyzed),
            "papers": analyzed,
        }
        digest_path = AGENT_ROOT / "generated_docs" / f"llm_analysis_{date_tag}.json"
        if not args.dry_run:
            digest_path.write_text(json.dumps(digest, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"Digest saved: {digest_path}")

    print(f"\nDone. Analyzed {len(analyzed)}/{len(papers)} papers.")


if __name__ == "__main__":
    main()




