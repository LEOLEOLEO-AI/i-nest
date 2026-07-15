"""Systematic paper classifier — separate real papers from all other content"""
import json, re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")

# Classification rules
PAPER_INDICATORS = [
    r"abstract", r"introduction", r"conclusion", r"参考文献", r"acknowledgment",
    r"methodology", r"experiment", r"result", r"discussion", r"相关工作",
    r"arXiv", r"doi", r"submitted", r"manuscript"
]

NOT_PAPER_PATTERNS = {
    "getnote_clipping": [r"^getnote_", r"^GetNote_", r"得到", r"剪藏"],
    "cover_letter": [r"cover.?letter", r"Cover.?Letter"],
    "submission_checklist": [r"submission.?checklist", r"Submission.?Checklist", r"checklist"],
    "project_guide": [r"重大专项", r"项目指南", r"项目建议", r"申报", r"基金申请"],
    "knowledge_baseline": [r"knowledge.?base", r"Knowledge.?Base", r"baseline", r"知识基线"],
    "darpa_report": [r"DARPA", r"darpa"],
    "reference_material": [r"白皮书", r"报告", r"深度分析", r"综述"],
    "admin_doc": [r"模板", r"template", r"评审", r"ARS"],
    "moc_index": [r"MOC", r"索引", r"导航", r"Index"],
}

def classify_file(f):
    """Classify a file as paper or other type"""
    name = f.name.lower()
    path_str = str(f).lower()
    
    # Check if it's in 51_Papers (formal paper area)
    in_papers_dir = "51_papers" in path_str.replace("\\", "/")
    
    # Check NOT_PAPER patterns
    for category, patterns in NOT_PAPER_PATTERNS.items():
        for pat in patterns:
            if re.search(pat, name) or re.search(pat, path_str):
                return category
    
    # If in 51_Papers, likely a real paper
    if in_papers_dir:
        # But still check for known non-paper patterns in papers dir
        if any(kw in name for kw in ["checklist", "cover", "模板"]):
            return "admin_doc"
        return "our_paper"
    
    # In TCC/iNEST but looks like a paper
    try:
        content = f.read_text(encoding="utf-8", errors="replace")[:2000].lower()
        paper_score = sum(1 for ind in PAPER_INDICATORS if ind in content)
        if paper_score >= 3 and len(content) > 2000:
            return "draft_paper"
    except:
        pass
    
    return "other"

# Scan only 51_Papers + paper-like files in TCC/iNEST
print("Scanning and classifying...")
files = []
papers_dir = VAULT / "50_Output" / "51_Papers"
if papers_dir.exists():
    for f in papers_dir.rglob("*.md"):
        files.append(f)

# Also scan for paper drafts in TCC/iNEST
for d in ["30_TCC/31_Theory/论文", "40_iNEST"]:
    p = VAULT / d
    if p.exists():
        for f in p.rglob("*.md"):
            if f not in files:
                files.append(f)

# Classify all
classified = defaultdict(list)
for f in files:
    cat = classify_file(f)
    classified[cat].append(f)

print(f"\nClassification results ({len(files)} files):")
for cat, flist in sorted(classified.items()):
    names = [f.name[:60] for f in flist[:5]]
    print(f"  {cat}: {len(flist)} files")
    for n in names:
        print(f"    - {n}")
    if len(flist) > 5:
        print(f"    ... and {len(flist)-5} more")

# Identify paper groups that need merging
print(f"\n=== Papers needing merge ===")
our_papers = classified.get("our_paper", []) + classified.get("draft_paper", [])
print(f"Total our papers: {len(our_papers)}")

# Find A1 group
a1_files = [f for f in our_papers if "a1" in f.stem.lower()]
print(f"A1 group: {len(a1_files)} files")
for f in a1_files:
    print(f"  {f.relative_to(VAULT)}")

# Find B0 group  
b0_files = [f for f in our_papers if "b0" in f.stem.lower()]
print(f"B0 group: {len(b0_files)} files")
for f in b0_files:
    print(f"  {f.relative_to(VAULT)}")

# Count by category summary
non_paper = sum(len(v) for k, v in classified.items() if k != "our_paper" and k != "draft_paper")
print(f"\nMisclassified (non-paper): {non_paper}")
print(f"Real papers: {len(our_papers)}")
