#!/usr/bin/env python3
"""
iNEST Daily Research Pipeline
==============================
Automated daily workflow: search -> analyze -> sync -> commit

Stages:
  1. SEARCH   - Run literature map to find new papers
  2. ANALYZE  - DeepSeek-V3.2 analysis of each paper
  3. SYNC     - Update Obsidian MOC and cross-links
  4. COMMIT   - Git auto-commit + push to Gitee

Usage:
    python daily_pipeline.py              # full pipeline
    python daily_pipeline.py --dry-run    # preview only
    python daily_pipeline.py --stage search    # search only
    python daily_pipeline.py --stage analyze   # analyze only
"""

import json
import os
import sys
import time
import shutil
import subprocess
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from openai import OpenAI

#  Paths 
AGENT_ROOT = Path(r"D:\\Obsidian\\Agent")
OBSIDIAN_VAULT = Path(r"D:\Obsidian\vault")
PIPELINE_DIR = AGENT_ROOT / "scripts" / "pipeline_state"
GENERATED_DOCS = AGENT_ROOT / "generated_docs"
EXECUTION_LOG = AGENT_ROOT / "execution_log"

#  API Config 
API_KEY = os.environ.get("SILICONFLOW_API_KEY", "")
API_BASE = "https://api.siliconflow.cn/v1"
MODEL = "deepseek-ai/DeepSeek-V3.2"

#  State Management 
def load_state():
    """Load pipeline state tracking analyzed papers and last run."""
    PIPELINE_DIR.mkdir(parents=True, exist_ok=True)
    state_file = PIPELINE_DIR / "pipeline_state.json"
    if state_file.exists():
        with open(state_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"last_run": None, "analyzed_papers": [], "total_runs": 0,
            "papers_analyzed_total": 0, "run_history": []}

def save_state(state):
    """Persist pipeline state."""
    PIPELINE_DIR.mkdir(parents=True, exist_ok=True)
    state_file = PIPELINE_DIR / "pipeline_state.json"
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def log(message, level="INFO"):
    """Timestamped log output."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] [{level}] {message}", flush=True)

#  Stage 1: Search 
def stage_search(dry_run=False):
    """Run the literature map task to find new papers."""
    log("STAGE 1: Literature Search", "STAGE")

    task_script = AGENT_ROOT / "01-Theory-Research" / "Task-01-Literature-Map" / "A" / "execute_task.py"
    if not task_script.exists():
        log(f"Task script not found: {task_script}", "ERROR")
        return None

    if dry_run:
        log("[DRY-RUN] Would run literature map search", "DRY-RUN")
        return GENERATED_DOCS / "results_20260530_104537.json"  # use latest existing

    log(f"Running: {task_script.name}")
    result = subprocess.run(
        [sys.executable, str(task_script)],
        cwd=str(AGENT_ROOT),
        capture_output=True, text=True, timeout=600
    )

    if result.returncode != 0:
        log(f"Search failed (code {result.returncode})", "WARN")
        if result.stderr:
            log(f"stderr: {result.stderr[:500]}", "DEBUG")

    # Find the newest results file
    json_files = sorted(GENERATED_DOCS.glob("results_*.json"), reverse=True)
    if json_files:
        latest = json_files[0]
        log(f"Search results: {latest.name}")
        return latest

    log("No search results found", "WARN")
    return None


#  Stage 2: Analyze 
def stage_analyze(results_path, state, dry_run=False):
    """Deep-analyze new papers with LLM, skip already-analyzed ones."""
    log("STAGE 2: LLM Deep Analysis", "STAGE")

    if not results_path or not Path(results_path).exists():
        log("No search results to analyze", "WARN")
        return [], state

    with open(results_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    papers = data.get("artifacts", {}).get("search_digest", {}).get("papers", [])
    if not papers:
        log("No papers in search results", "WARN")
        return [], state

    # Deduplicate against already-analyzed papers (by title hash)
    analyzed_titles = set(state.get("analyzed_papers", []))
    new_papers = []
    for p in papers:
        title_key = p.get("title", "").strip().lower()[:100]
        if title_key not in analyzed_titles:
            new_papers.append(p)

    log(f"Papers: {len(papers)} total, {len(new_papers)} new, {len(analyzed_titles)} already analyzed")

    if not new_papers:
        log("No new papers to analyze", "INFO")
        return [], state

    if dry_run:
        log(f"[DRY-RUN] Would analyze {len(new_papers)} papers", "DRY-RUN")
        return [], state

    client = OpenAI(api_key=API_KEY, base_url=API_BASE, timeout=180)
    obsidian_papers = OBSIDIAN_VAULT / "03_Topics" / "Papers"
    obsidian_papers.mkdir(parents=True, exist_ok=True)
    analyzed = []

    for i, paper in enumerate(new_papers[:15], 1):  # Max 15 per run
        title = paper.get("title", "Unknown")
        log(f"  [{i}/{min(len(new_papers), 15)}] {title[:70]}...")

        analysis = _call_llm_analysis(client, paper)
        if not analysis:
            continue

        score = analysis.get("inest_relevance", {}).get("score", 0)
        note = _format_obsidian_note(paper, analysis)
        filename = _safe_filename(title)
        filepath = obsidian_papers / f"{filename}.md"
        filepath.write_text(note, encoding="utf-8")

        analyzed.append({
            "title": title,
            "filename": filename,
            "score": score,
            "source": paper.get("source", "?"),
        })
        analyzed_titles.add(title.strip().lower()[:100])
        log(f"    score={score:.2f} -> {filepath.name}")
        time.sleep(1)

    state["analyzed_papers"] = list(analyzed_titles)
    log(f"Analyzed {len(analyzed)} new papers")
    return analyzed, state


def _call_llm_analysis(client, paper):
    """Call DeepSeek for structured paper analysis."""
    prompt = f"""Analyze this research paper for the iNEST framework studying "Physical Complex Network Intelligence Emergence". Output ONLY valid JSON with: core_contribution, methodology, key_findings (array), limitations (array), inest_relevance (score 0-1, themes array, explanation), cross_connections (array), research_gaps (array), next_steps, tags (array).

Paper: {paper.get('title','?')} ({paper.get('year','?')})
Abstract: {(paper.get('abstract') or 'N/A')[:2000]}"""

    try:
        r = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": "You output ONLY valid JSON, no markdown."},
                      {"role": "user", "content": prompt}],
            max_tokens=1500, temperature=0.3, timeout=120
        )
        raw = r.choices[0].message.content.strip()
        if raw.startswith("```"): raw = raw.split("\n", 1)[1][:-3] if raw.endswith("```") else raw.split("\n", 1)[1]
        return json.loads(raw)
    except Exception as e:
        log(f"    LLM error: {e}", "WARN")
        return None


def _format_obsidian_note(paper, analysis):
    """Format paper analysis as Obsidian note with type-safe handling."""
    def _s(val, default=''):
        """Ensure value is a string. Lists are joined with newlines."""
        if val is None:
            return default
        if isinstance(val, list):
            return ', '.join(str(v) for v in val)
        return str(val)

    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    rel = analysis.get("inest_relevance", {})
    title = paper.get("title", "?")
    tags = analysis.get("tags", ["paper", "daily-pipeline"])
    authors = paper.get("authors", [])
    url = paper.get("url", "")
    themes = rel.get('themes', [])
    if isinstance(themes, list):
        themes_str = ', '.join(str(t) for t in themes)
    else:
        themes_str = str(themes)

    lines = ["---",
             f'title: "{title}"',
             f'year: {paper.get("year", "?")}',
             f'source: "{paper.get("source", "?")}"',
             f"tags: [{', '.join(tags)}]",
             f'inest_score: {rel.get("score", 0)}',
             f"analyzed: {ts}",
             "---", "",
             f"# {title}", "",
             f"- **Year**: {paper.get('year', '?')}",
             f"- **Source**: {paper.get('source', '?')}"]
    if url: lines.append(f"- **URL**: [{url}]({url})")
    if authors: lines.append(f"- **Authors**: {', '.join(str(a) for a in authors[:5])}")
    lines += ["", "## iNEST Relevance",
              f"**Score**: {rel.get('score',0):.2f} | **Themes**: {themes_str}",
              f"{_s(rel.get('explanation'))}", "",
              "## Core Contribution", _s(analysis.get("core_contribution")), "",
              "## Next Steps for iNEST", _s(analysis.get("next_steps")), ""]
    findings = analysis.get("key_findings", [])
    if findings and isinstance(findings, list):
        lines += ["## Key Findings"] + [f"- {_s(f)}" for f in findings] + [""]
    gaps = analysis.get("research_gaps", [])
    if gaps and isinstance(gaps, list):
        lines += ["## Research Gaps"] + [f"- {_s(g)}" for g in gaps] + [""]
    return "\n".join(lines)

def _safe_filename(title):
    safe = "".join(c if c.isalnum() or c in " _-()[]" else "_" for c in title)
    return safe.strip()[:120] or "untitled"


#  Stage 3: Sync 
def stage_sync(dry_run=False):
    """Update Obsidian MOC and cross-links."""
    log("STAGE 3: Obsidian Sync", "STAGE")

    # Run reorganize.py to refresh MOC with new papers
    reorg_script = OBSIDIAN_VAULT / "90_System" / "scripts" / "reorganize.py"
    if not reorg_script.exists():
        log(f"Reorg script not found: {reorg_script}, skipping", "WARN")
        return

    if dry_run:
        log("[DRY-RUN] Would run --process-inbox on Obsidian", "DRY-RUN")
        return

    obsidian_venv = OBSIDIAN_VAULT / ".venv" / "Scripts" / "python.exe"
    python_exe = obsidian_venv if obsidian_venv.exists() else sys.executable

    try:
        subprocess.run(
            [str(python_exe), str(reorg_script), "--process-inbox"],
            cwd=str(OBSIDIAN_VAULT), capture_output=True, text=True, timeout=300
        )
        log("Obsidian sync complete")
    except Exception as e:
        log(f"Sync warning: {e}", "WARN")


#  Stage 4: Git Commit 
def stage_commit(dry_run=False):
    """Auto-commit and push to Gitee."""
    log("STAGE 4: Git Commit & Push", "STAGE")

    vault = str(OBSIDIAN_VAULT)

    # Check for changes in Obsidian vault
    status = subprocess.run(["git", "-C", vault, "status", "--porcelain"],
                            capture_output=True, text=True)
    if not status.stdout.strip():
        log("No changes to commit in Obsidian vault")
    else:
        if dry_run:
            log(f"[DRY-RUN] Would commit {len(status.stdout.strip().split(chr(10)))} changed files", "DRY-RUN")
        else:
            subprocess.run(["git", "-C", vault, "add", "-A"], capture_output=True)
            date_tag = datetime.now().strftime("%Y-%m-%d")
            msg = f"daily-pipeline: auto-sync {date_tag}"
            subprocess.run(["git", "-C", vault, "commit", "-m", msg], capture_output=True)
            log(f"Committed: {msg}")

    # Check for changes in Agent (generated_docs)
    agent_root = str(AGENT_ROOT)
    agent_git = Path(agent_root) / ".git"
    if not agent_git.exists():
        log("Agent not a git repo, skipping agent commit", "INFO")
    else:
        status2 = subprocess.run(["git", "-C", agent_root, "status", "--porcelain"],
                                 capture_output=True, text=True)
        if status2.stdout.strip():
            if not dry_run:
                subprocess.run(["git", "-C", agent_root, "add", "generated_docs/", "execution_log/",
                                "scripts/pipeline_state/"], capture_output=True)
                subprocess.run(["git", "-C", agent_root, "commit", "-m",
                                f"daily-pipeline: research results {date_tag}"], capture_output=True)
                log("Agent commit done")

    # Push
    if dry_run:
        log("[DRY-RUN] Would push to Gitee", "DRY-RUN")
    else:
        result = subprocess.run(["git", "-C", vault, "push", "origin", "main"],
                                capture_output=True, text=True)
        if result.returncode == 0:
            log("Pushed to Gitee successfully")
        else:
            log(f"Push warning: {result.stderr[:200]}", "WARN")



#  Stage 5: iNEST Orchestrator 
def stage_feed(dry_run=False):
    """Run the four-channel iNEST orchestrator."""
    log("STAGE 5: iNEST Intelligence Feed", "STAGE")
    feed_script = AGENT_ROOT / "scripts" / "inest_feed.py"
    if not feed_script.exists():
        log(f"Orchestrator not found: {orch_script}", "WARN")
        return
    if dry_run:
        log("[DRY-RUN] Would run iNEST orchestrator", "DRY-RUN")
        return
    try:
        result = subprocess.run(
            [sys.executable, str(feed_script) + " --mode feed"],
            cwd=str(AGENT_ROOT), capture_output=True, text=True, timeout=600
        )
        if result.returncode == 0:
            log("iNEST feed completed")
        else:
            log(f"Feed warning (code {result.returncode})", "WARN")
    except Exception as e:
        log(f"Feed error: {e}", "WARN")
#  Summary 
def generate_summary(analyzed, state):
    """Generate and save daily digest."""
    log("Generating daily digest", "INFO")

    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    date_tag = datetime.now().strftime("%Y%m%d")

    lines = ["---",
             f"date: {ts}",
             "tags: [daily-digest, auto-generated, pipeline]",
             "---", "",
             f"# Daily Research Digest - {ts}", "",
             f"**Pipeline run #{state.get('total_runs', 0)}**", "",
             f"- Papers analyzed this run: {len(analyzed)}",
             f"- Total papers analyzed to date: {state.get('papers_analyzed_total', 0)}",
             f"- Sources: {', '.join(set(p.get('source','?') for p in analyzed))}" if analyzed else "",
             ""]

    if analyzed:
        lines.append("## New Papers Today")
        for p in sorted(analyzed, key=lambda x: x.get("score", 0), reverse=True):
            lines.append(f"- **[{p['title'][:80]}]** (score: {p['score']:.2f}, {p['source']})")
        lines.append("")

    digest_path = OBSIDIAN_VAULT / "01_MOC" / f"Daily-Digest-{date_tag}.md"
    digest_path.write_text("\n".join(lines), encoding="utf-8")
    log(f"Digest: {digest_path.name}")


#  Main 
def main():
    parser = argparse.ArgumentParser(description="iNEST Daily Research Pipeline")
    parser.add_argument("--dry-run", action="store_true", help="Preview without changes")
    parser.add_argument("--stage", choices=["search", "analyze", "sync", "commit", "all"],
                        default="all", help="Run specific stage only")
    parser.add_argument("--skip-search", action="store_true", help="Skip search, use latest results")
    args = parser.parse_args()

    log("=" * 60)
    log("iNEST Daily Research Pipeline Started", "PIPELINE")
    log("=" * 60)

    state = load_state()
    run_start = datetime.now()

    # Stage 1: Search
    results_path = None
    if args.stage in ("search", "all") and not args.skip_search:
        results_path = stage_search(args.dry_run)
    elif args.skip_search or args.stage in ("analyze", "all"):
        # Use latest existing results
        json_files = sorted(GENERATED_DOCS.glob("results_*.json"), reverse=True)
        results_path = json_files[0] if json_files else None
        if results_path:
            log(f"Using existing results: {results_path.name}")

    # Stage 2: Analyze
    analyzed = []
    if args.stage in ("analyze", "all") and results_path:
        analyzed, state = stage_analyze(results_path, state, args.dry_run)

    # Stage 3: Sync
    if args.stage in ("sync", "all"):
        stage_sync(args.dry_run)

    # Stage 4: Commit
    if args.stage in ("commit", "all"):
        stage_commit(args.dry_run)

    # Update state
    state["last_run"] = run_start.isoformat()
    state["total_runs"] = state.get("total_runs", 0) + 1
    state["papers_analyzed_total"] = state.get("papers_analyzed_total", 0) + len(analyzed)
    state["run_history"].append({
        "timestamp": run_start.isoformat(),
        "papers_analyzed": len(analyzed),
        "sources": list(set(p.get("source", "?") for p in analyzed)) if analyzed else [],
        "dry_run": args.dry_run,
    })
    # Keep last 30 runs
    state["run_history"] = state["run_history"][-30:]

    if not args.dry_run:
        save_state(state)

    # Generate summary digest
    if analyzed:
        generate_summary(analyzed, state)

    elapsed = (datetime.now() - run_start).total_seconds()
    log("=" * 60)
    log(f"Pipeline complete in {elapsed:.0f}s. Analyzed {len(analyzed)} papers.", "PIPELINE")
    log("=" * 60)

    # Save execution log
    EXECUTION_LOG.mkdir(parents=True, exist_ok=True)
    log_file = EXECUTION_LOG / f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    log_file.write_text(json.dumps({
        "timestamp": run_start.isoformat(),
        "duration_s": elapsed,
        "papers_analyzed": len(analyzed),
        "dry_run": args.dry_run,
    }, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()



