import os
from pathlib import Path

VAULT = Path(r"D:\Obsidian\vault")
WRITE = Path(r"D:\iNEST\Write")

# Build vault index: {filename_lower: max_size}
vault_index = {}
for f in VAULT.rglob("*.md"):
    if any(x in f.parts for x in [".git", ".obsidian", ".trash", ".neural_db"]):
        continue
    name = f.name.lower()
    size = f.stat().st_size
    if name not in vault_index or size > vault_index[name]:
        vault_index[name] = size

# Scan Write dir, delete dupes
deleted = 0
kept = 0
errors = 0

for root, dirs, files in os.walk(str(WRITE)):
    # Skip problematic dirs
    dirs[:] = [d for d in dirs if d not in [".git", "node_modules", ".venv", "__pycache__"]]
    
    for fname in files:
        if not fname.endswith(".md"):
            continue
        
        fpath = Path(root) / fname
        name_lower = fname.lower()
        
        if name_lower in vault_index:
            vault_size = vault_index[name_lower]
            file_size = fpath.stat().st_size
            
            # Delete if vault has equal or larger version
            if vault_size >= file_size * 0.9:  # Allow 10% tolerance
                try:
                    fpath.unlink()
                    deleted += 1
                except:
                    errors += 1
            else:
                # D:\iNEST version is bigger - flag for review
                kept += 1

print(f"Deleted (vault >= Write): {deleted}")
print(f"Kept (Write larger than vault): {kept}")
print(f"Errors: {errors}")

# Count remaining
remaining = sum(1 for _ in WRITE.rglob("*.md") if not any(x in _.parts for x in [".git","node_modules",".venv"]))
print(f"Remaining in D:\\iNEST\\Write: {remaining} md")
