#!/usr/bin/env python3
"""
Main Pipeline Orchestrator — TCC x iNEST Knowledge Automation.
Flow: Crawl -> Inbox -> Classify -> Link -> v2.0 Analysis -> Output

Usage:
  python pipeline.py daily          # Daily pipeline
  python pipeline.py process        # Only process inbox
  python pipeline.py build-links    # Rebuild bidirectional links
  python pipeline.py v2             # Wiki LLM v2.0 analysis
  python pipeline.py full           # Full pipeline
"""
import os, sys, time, subprocess
from pathlib import Path
from datetime import datetime

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
SCRIPTS = VAULT / "90_System" / "scripts"

def run_script(name, *args):
    script = SCRIPTS / name
    cmd = [sys.executable, str(script)] + list(args)
    print(f"\n>>> Running: {' '.join(cmd)}")
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    result = subprocess.run(cmd, cwd=str(VAULT), capture_output=True, text=True, timeout=600, env=env)
    if result.stdout:
        print(result.stdout[-2000:])
    if result.stderr:
        print("STDERR:", result.stderr[-500:])
    return result.returncode == 0

def pipeline_daily():
    """Daily pipeline: crawl + process + links + v2."""
    print(f"\n{'#'*60}")
    print(f"# Daily Pipeline — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'#'*60}")
    
    print("\n[1/4] Crawling new papers...")
    run_script("daily_crawl.py")
    
    print("\n[2/4] Processing inbox...")
    run_script("process_inbox.py", "--limit", "20")
    
    print("\n[3/4] Building links...")
    run_script("build_graph.py")
    
    print("\n[4/4] Wiki LLM v2.0 emerge...")
    run_script("wiki_llm_v2.py", "emerge")
    
    print(f"\n{'#'*60}")
    print("# Pipeline complete.")
    print(f"{'#'*60}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="TCC x iNEST Knowledge Pipeline")
    parser.add_argument("command", choices=["daily", "process", "build-links", "v2", "full"])
    args = parser.parse_args()
    
    if args.command == "daily":
        pipeline_daily()
    elif args.command == "process":
        run_script("process_inbox.py", "--limit", "20")
    elif args.command == "build-links":
        run_script("build_graph.py")
    elif args.command == "v2":
        run_script("wiki_llm_v2.py", "full")
    elif args.command == "full":
        run_script("daily_crawl.py")
        run_script("process_inbox.py", "--limit", "20")
        run_script("build_graph.py")
        run_script("wiki_llm_v2.py", "full")
