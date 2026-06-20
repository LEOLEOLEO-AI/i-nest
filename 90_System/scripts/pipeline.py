#!/usr/bin/env python3
"""
Main Pipeline Orchestrator — TCC x iNEST Knowledge Automation.
Flow: Crawl -> Inbox -> Classify -> Link -> Output

Usage:
  python pipeline.py daily          # Daily 8am crawl + process
  python pipeline.py process        # Only process inbox
  python pipeline.py build-links    # Rebuild bidirectional links
  python pipeline.py full           # Full pipeline: crawl + process + links
"""
import os, sys, time, subprocess
from pathlib import Path
from datetime import datetime

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
SCRIPTS = VAULT / "90_System" / "scripts"

def run_script(name, *args):
    """Run a pipeline script."""
    script = SCRIPTS / name
    cmd = [sys.executable, str(script)] + list(args)
    print(f"\n>>> Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=str(VAULT), capture_output=True, text=True, timeout=600)
    if result.stdout:
        print(result.stdout[-2000:])
    if result.stderr:
        print("STDERR:", result.stderr[-500:])
    return result.returncode == 0

def pipeline_daily():
    """Daily pipeline: crawl new papers + process inbox."""
    print(f"\n{'#'*60}")
    print(f"# Daily Pipeline — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'#'*60}")
    
    # Step 1: Crawl
    print("\n[1/3] Crawling new papers...")
    run_script("daily_crawl.py")
    
    # Step 2: Process inbox (LLM classify + move)
    print("\n[2/3] Processing inbox...")
    run_script("process_inbox.py", "--limit", "20")
    
    # Step 3: Build links
    print("\n[3/3] Building bidirectional links...")
    run_script("build_graph.py")
    
    print(f"\n{'#'*60}")
    print("# Pipeline complete. Review 00_Inbox and commit changes.")
    print(f"{'#'*60}")

def pipeline_process():
    """Only process inbox."""
    run_script("process_inbox.py", "--limit", "20")

def pipeline_build_links():
    """Rebuild links."""
    run_script("build_graph.py")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="TCC x iNEST Knowledge Pipeline")
    parser.add_argument("command", choices=["daily", "process", "build-links", "full"])
    args = parser.parse_args()
    
    if args.command == "daily" or args.command == "full":
        pipeline_daily()
    elif args.command == "process":
        pipeline_process()
    elif args.command == "build-links":
        pipeline_build_links()
