import json, shutil, os
from pathlib import Path

VAULT_ROOT = r"D:\Obsidian\vault"
report_path = Path(VAULT_ROOT) / "60_MOC" / "system_dedup_report.json"
report = json.loads(report_path.read_text(encoding="utf-8"))

# ===== PHASE 1: Delete c:\tmp clones =====
tmp_dirs_to_delete = [
    r"c:\tmp\i-nest-fresh",
    r"c:\tmp\i-nest-clone",
    r"c:\tmp\i-nest",
]
phase1_deleted = 0
for d in tmp_dirs_to_delete:
    dp = Path(d)
    if dp.exists():
        file_count = sum(1 for _ in dp.rglob("*") if _.is_file())
        print(f"PHASE1: Deleting {d} ({file_count} files)...")
        try:
            shutil.rmtree(str(dp))
            phase1_deleted += file_count
            print(f"  DELETED: {file_count} files")
        except Exception as e:
            print(f"  ERROR: {e}")

# ===== PHASE 2: Delete dupes from D:\iNEST and other locations =====
PROTECTED_PATHS = [
    "neuromorphic_tools",  # Simulation tools - not duplicates
    "Write\\Code\\MNoB",   # Active project code
    "Write\\Code\\.venv",  # Python venv
    "Write\\Code\\node_modules",
]

phase2_deleted = 0
phase2_skipped = 0

for group in report:
    name = group["name"]
    
    # Skip README.md and SKILL.md (false positives)
    if name.lower() in ("readme.md", "skill.md", "changelog.md", "contributing.md"):
        continue
    
    # For each outside file, delete if vault has a copy
    for op in group["outside_paths"]:
        path_lower = op.lower()
        
        # Skip protected paths
        if any(pp.lower() in path_lower for pp in PROTECTED_PATHS):
            phase2_skipped += 1
            continue
        
        # Skip if outside file is in c:\tmp (already handled by phase1)
        if op.startswith(r"c:\tmp"):
            continue
        
        # Delete the outside copy
        fp = Path(op)
        if fp.exists():
            try:
                fp.unlink()
                phase2_deleted += 1
            except Exception as e:
                pass

print(f"\nPHASE2: Deleted {phase2_deleted} duplicate files")
print(f"PHASE2: Skipped {phase2_skipped} protected files")

# ===== PHASE 3: Clean D:\Obsidian root loose files =====
obsidian_root = Path(r"D:\Obsidian")
phase3_deleted = 0
for f in obsidian_root.iterdir():
    if f.is_file() and f.suffix == ".md":
        if VAULT_ROOT not in str(f):
            # Check if exists in vault
            vault_copy = Path(VAULT_ROOT) / f.name
            if vault_copy.exists():
                f.unlink()
                phase3_deleted += 1
                print(f"PHASE3: Deleted {f.name} from Obsidian root")

print(f"\nPHASE3: Deleted {phase3_deleted} loose files")

# ===== SUMMARY =====
print(f"\n=== CLEANUP SUMMARY ===")
print(f"Phase1 (tmp clones): {phase1_deleted} files")
print(f"Phase2 (iNEST dupes): {phase2_deleted} files")  
print(f"Phase3 (root loose): {phase3_deleted} files")
print(f"Total: {phase1_deleted + phase2_deleted + phase3_deleted} files deleted")
print(f"Protected (skipped): {phase2_skipped}")
