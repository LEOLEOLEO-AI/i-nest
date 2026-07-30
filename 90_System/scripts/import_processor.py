#!/usr/bin/env python3
"""
import_processor.py — Auto-processor for Genspark, Codex, 得到大脑 imports
Watches for new files → classifies → moves to raw/ → triggers wiki compile
"""
import os, sys, json, re, shutil
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

VAULT = Path(r"D:\Obsidian\vault")
INBOX = VAULT / "00_Inbox"
RAW = VAULT / "raw"
WIKI = VAULT / "wiki"

# Import source directories
GENSPARK_DIR = Path(r"D:\Output\Genspark")
DEDAO_INBOX = Path(r"D:\Obsidian\GetNotes_Inbox")

TODAY = datetime.now().strftime("%Y-%m-%d")

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# ============================================================
# Source-specific processors
# ============================================================

def process_genspark():
    """Process new Genspark .docx/.pptx exports"""
    if not GENSPARK_DIR.exists():
        log("Genspark dir not found, skipping")
        return 0
    
    count = 0
    # Genspark typically produces .docx and .pptx files
    # These should already be converted to .md by the pipeline
    # Here we handle any stragglers
    for ext in ["*.md", "*.txt"]:
        for f in GENSPARK_DIR.glob(ext):
            if f.stat().st_mtime > (datetime.now() - timedelta(days=7)).timestamp():
                dest = RAW / "imports" / f.name
                dest.parent.mkdir(exist_ok=True)
                shutil.copy2(str(f), str(dest))
                count += 1
                log(f"  Genspark → raw/imports/{f.name}")
    
    return count

def process_dedao():
    """Process 得到大脑 imports from GetNotes_Inbox"""
    if not DEDAO_INBOX.exists():
        log("得到大脑 inbox not found, skipping")
        return 0
    
    count = 0
    for f in DEDAO_INBOX.glob("*.md"):
        mtime = f.stat().st_mtime
        if mtime > (datetime.now() - timedelta(days=7)).timestamp():
            dest = RAW / "inbox" / f"dedao_{f.name}"
            dest.parent.mkdir(exist_ok=True)
            shutil.copy2(str(f), str(dest))
            count += 1
            log(f"  得到大脑 → raw/inbox/dedao_{f.name}")
    
    return count

def process_codex():
    """Check Codex output directory"""
    codex_dir = VAULT / "20_Processing"
    if not codex_dir.exists():
        return 0
    
    count = 0
    for f in codex_dir.glob("*codex*.md"):
        mtime = f.stat().st_mtime
        if mtime > (datetime.now() - timedelta(days=7)).timestamp():
            dest = RAW / "imports" / f"codex_{f.name}"
            dest.parent.mkdir(exist_ok=True)
            shutil.copy2(str(f), str(dest))
            count += 1
            log(f"  Codex → raw/imports/codex_{f.name}")
    
    return count

# ============================================================
# Main
# ============================================================

def main():
    log("=== Import Processor ===")
    
    genspark_count = process_genspark()
    dedao_count = process_dedao()
    codex_count = process_codex()
    
    total = genspark_count + dedao_count + codex_count
    log(f"Imported: Genspark={genspark_count}, 得到大脑={dedao_count}, Codex={codex_count}")
    log(f"Total new files in raw/: {total}")
    
    # Check if inbox needs processing
    inbox_files = list(INBOX.glob("*.md"))
    log(f"Inbox pending: {len(inbox_files)} files")
    
    if total > 0 or inbox_files:
        log("New imports detected — wiki_compiler.py should be triggered next")
    
    log("=== Done ===")

if __name__ == "__main__":
    main()
