# SECURITY FIX: API Key Migration Script
# =======================================
# Replaces hardcoded SILICONFLOW_API_KEY with environment variable.
# Run this once to fix inest_orchestrator.py, daily_pipeline.py, inest_feed.py.
#
# Usage: python fix_api_keys.py --apply
#         python fix_api_keys.py --check  (dry-run, show what would change)

import sys, os, re
from pathlib import Path

FILES = [
    r"D:\Agent\scripts\inest_orchestrator.py",
    r"D:\Agent\scripts\daily_pipeline.py",
    r"D:\Agent\scripts\inest_feed.py",
]

OLD_KEY_PREFIX = "sk-ewvmxpqaoqdmzyrizltymazqkbbzhberrgdwhrinpssoauum"
NEW_LINE = 'API_KEY = os.environ.get("SILICONFLOW_API_KEY", "")'

def fix_file(filepath, dry_run=True):
    path = Path(filepath)
    if not path.exists():
        print(f"  NOT FOUND: {path}")
        return
    
    content = path.read_text(encoding="utf-8")
    
    if OLD_KEY_PREFIX not in content:
        print(f"  CLEAN: {path.name}")
        return
    
    # Replace the pattern: API_KEY = os.environ.get("SILICONFLOW_API_KEY", "sk-...")
    # with: API_KEY = os.environ.get("SILICONFLOW_API_KEY", "")
    old_pattern = r'API_KEY = os\.environ\.get\("SILICONFLOW_API_KEY",\s*\n\s*"[^"]*"\)'
    replacement = 'API_KEY = os.environ.get("SILICONFLOW_API_KEY", "")'
    
    new_content = re.sub(old_pattern, replacement, content)
    
    if new_content != content:
        print(f"  FIXED: {path.name} (key removed)")
        if not dry_run:
            # Backup original
            backup = path.with_suffix(path.suffix + ".bak")
            path.rename(backup)
            path.write_text(new_content, encoding="utf-8")
            print(f"    Backup: {backup.name}")
            print(f"    Written: {path.name}")
    else:
        print(f"  NO CHANGE: {path.name} (pattern not matched)")

def main():
    dry_run = "--check" in sys.argv or "--apply" not in sys.argv
    mode = "DRY-RUN (--apply to write)" if dry_run else "APPLYING FIXES"
    print(f"API Key Security Fix — {mode}")
    print("=" * 60)
    for f in FILES:
        fix_file(f, dry_run)
    print()
    if dry_run:
        print("Run with --apply to write changes.")
    else:
        print("Done. Set SILICONFLOW_API_KEY in your environment.")
        print("  PowerShell: $env:SILICONFLOW_API_KEY='your-key'")
        print("  CMD: set SILICONFLOW_API_KEY=your-key")

if __name__ == "__main__":
    main()
