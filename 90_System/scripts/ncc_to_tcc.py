"""Bulk rename: NCC→TCC, 软件定义互联→软件定义互连 (fixed)"""
import re, sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

VAULT = Path(r"D:\Obsidian\vault")
SKIP = {".obsidian", ".git", ".venv", "node_modules", "__pycache__", ".trash", "80_Archive", ".smart-env", ".neural_db", ".neural_memory", ".openclaw", ".claude", ".claudian"}

def should_skip(path):
    return any(p in SKIP for p in path.parts)

def replace_ncc(text):
    # Replace standalone NCC but NOT NCCL
    # Match NCC followed by non-alphabetic char or end of string, that's NOT part of NCCL
    text = re.sub(r'NCC(?!L)', 'TCC', text)
    return text

stats = {"files_changed": 0, "ncc_replaced": 0, "sd_replaced": 0, "files_renamed": 0}

# Phase 1: Replace content
print("Phase 1: Replacing content...")
for f in VAULT.rglob("*.md"):
    if should_skip(f): continue
    try:
        content = f.read_text(encoding="utf-8", errors="replace")
        new_content = content
        
        # NCC→TCC (but keep NCCL)
        ncc_count = content.count("NCC")
        nccl_count = content.count("NCCL")
        if ncc_count > nccl_count:
            new_content = replace_ncc(new_content)
            actual = ncc_count - nccl_count
            stats["ncc_replaced"] += actual
        
        # 软件定义互联→软件定义互连
        sd_count = content.count("软件定义互联")
        if sd_count > 0:
            new_content = new_content.replace("软件定义互联", "软件定义互连")
            stats["sd_replaced"] += sd_count
        
        if new_content != content:
            f.write_text(new_content, encoding="utf-8")
            stats["files_changed"] += 1
            if stats["files_changed"] <= 10:
                print(f"  {f.relative_to(VAULT)}")
    except Exception as e:
        pass

# Phase 2: Rename files
print("\nPhase 2: Renaming files...")
renames = []
for f in VAULT.rglob("*NCC*"):
    if should_skip(f): continue
    if "NCCL" in f.name: continue
    new_name = f.name.replace("NCC", "TCC")
    new_path = f.parent / new_name
    if new_path != f and not new_path.exists():
        renames.append((f, new_path))

renames.sort(key=lambda x: len(x[0].parts), reverse=True)
for old, new in renames:
    try:
        old.rename(new)
        stats["files_renamed"] += 1
        print(f"  {old.name[:60]} →")
        print(f"  {new.name[:60]}")
    except Exception as e:
        pass

print(f"\nResults:")
print(f"  Files changed: {stats['files_changed']}")
print(f"  NCC→TCC replacements: {stats['ncc_replaced']}")
print(f"  软件定义互联→互连: {stats['sd_replaced']}")
print(f"  Files renamed: {stats['files_renamed']}")
