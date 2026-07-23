# -*- coding: utf-8 -*-
"""P1: Vault file watcher - auto-process Inbox on new files"""

import time, subprocess, sys
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
INBOX = VAULT / "00_Inbox"
PYTHON = r"C:\Users\LEO\AppData\Local\Programs\Python\Python310\python.exe"
PROCESSOR = VAULT / "90_System" / "scripts" / "process_inbox.py"

class InboxHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_run = 0
        self.cooldown = 60  # seconds between runs
    
    def on_created(self, event):
        if event.is_directory:
            return
        if not event.src_path.endswith(".md"):
            return
        if "_pipeline_insights" in Path(event.src_path).parts:
            return
        
        now = time.time()
        if now - self.last_run < self.cooldown:
            return
        self.last_run = now
        
        rel = Path(event.src_path).relative_to(VAULT)
        print(f"\n[{time.strftime('%H:%M:%S')}] New file: {rel}")
        
        # Wait for file to be fully written
        time.sleep(2)
        
        result = subprocess.run(
            [PYTHON, "-X", "utf8", str(PROCESSOR)],
            cwd=str(VAULT),
            capture_output=True, text=True, encoding="utf-8", errors="ignore",
            timeout=120
        )
        if result.stdout:
            print(result.stdout[:500])
        if "error" in (result.stderr or "").lower():
            print(f"ERR: {result.stderr[:200]}")

def main():
    print(f"Watching: {INBOX}")
    print(f"Processor: {PROCESSOR}")
    print("Press Ctrl+C to stop")
    
    observer = Observer()
    observer.schedule(InboxHandler(), str(INBOX), recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
