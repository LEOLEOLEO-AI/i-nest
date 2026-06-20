import os
import glob

workspace = r'd:\Obsidian\home\work\.openclaw\workspace'
md_files = glob.glob(os.path.join(workspace, '**', '*.md'), recursive=True)

paper_files = []

for f in md_files:
    if '30_Outputs\\论文' in f or '.obsidian' in f:
        continue
    
    # Check if file might be a paper draft based on name or content
    filename = os.path.basename(f)
    if '论文' in filename or 'Paper' in filename or 'Draft' in filename:
        # Ignore things that are definitely just index/plannings
        if '00_' not in filename and '规划' not in filename:
            paper_files.append(f)

for f in paper_files:
    print(f)
