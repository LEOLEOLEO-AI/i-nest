"""Paper Version Tracker v2 — correct classification, proper merging"""
import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime
from collections import defaultdict

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
TODAY = datetime.now().strftime("%Y-%m-%d")

# Paper groups: (id, display_name, base_patterns, is_ours)
PAPER_GROUPS = [
    ("A1", "CST Theory: 智能涌现的复杂度阈值定理", 
     [r"A1_CST.*V\d+", r"A1_CST.*FINAL", r"A1_CST.*CLEAN", r"A1_CST.*SUBMISSION", r"A1_Cover", r"A1_Submission", r"A1_Light", r"A1_ARS", r"学生.*A1", r"冲刺.*A1", r"工作包.*A1"],
     True),
    ("B0", "NCC Engineering: 晶圆级拓扑计算工程实现",
     [r"B0_Engineering", r"B0_Cover", r"B0_Submission", r"学生.*B0", r"冲刺.*B0"],
     True),
]

STANDALONE_PAPERS = [
    ("C0", "CST RG PRL: 临界复杂度阈值定理物理评论快报", 
     [r"CST_RG_PRL"], True),
]

def classify_paper_file(f):
    """Classify a file in 51_Papers as a specific paper or other"""
    name = f.name
    stem = f.stem
    path_str = str(f.relative_to(VAULT))

    # Check if it's a non-paper
    lower = name.lower()
    
    # Skip version index itself
    if "paper_versions" in lower or "00_paper" in lower:
        return None, "index_file"
    
    # Skip non-paper content in papers dir
    non_paper_patterns = {
        "getnote": [r"getnote", r"GetNote"],
        "cover_letter": [r"cover.?letter", r"Cover.?Letter"],
        "checklist": [r"checklist", r"Checklist", r"submission"],
        "project_guide": [r"重大专项", r"项目指南", r"项目建议", r"申报"],
        "reference": [r"综述", r"报告", r"白皮书", r"DARPA"],
        "admin": [r"模板", r"template", r"ARS.*审查", r"ARS.*报告", r"引用模板"],
        "planning": [r"推进计划", r"总览", r"规划", r"管线", r"导航", r"冲刺"],
        "knowledge_base": [r"knowledge.*base", r"baseline", r"知识基线"],
        "moc": [r"MOC", r"索引"],
    }
    
    for cat, patterns in non_paper_patterns.items():
        for pat in patterns:
            if re.search(pat, name) or re.search(pat, stem):
                return None, cat
    
    # Check paper groups
    for pid, title, patterns, is_ours in PAPER_GROUPS + STANDALONE_PAPERS:
        for pat in patterns:
            if re.search(pat, name):
                return pid, title
    
    # Check if it looks like a paper (has paper-like content)
    try:
        content = f.read_text(encoding="utf-8", errors="replace")[:2000]
        paper_indicators = sum(1 for kw in ["abstract", "introduction", "conclusion", "method", "result", "arXiv", "doi", "参考文献"] if kw.lower() in content.lower())
        if paper_indicators >= 3:
            return f.stem[:40], f.stem[:60]  # Standalone paper
    except:
        pass
    
    return None, "other"

def build_correct_index():
    """Build correct paper index from 51_Papers only"""
    papers_dir = VAULT / "50_Output" / "51_Papers"
    if not papers_dir.exists():
        return {}
    
    # Classify all files
    paper_groups = defaultdict(list)
    non_papers = defaultdict(list)
    
    for f in papers_dir.rglob("*.md"):
        if ".git" in str(f): continue
        pid, label = classify_paper_file(f)
        if pid:
            paper_groups[pid].append({
                "name": f.name, "path": str(f.relative_to(VAULT)),
                "size": f.stat().st_size,
                "mtime": datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d"),
                "label": label
            })
        else:
            non_papers[label].append(f.name)
    
    # Build final index
    index = {}
    paper_num = 1
    
    for pid, files in sorted(paper_groups.items()):
        files.sort(key=lambda x: (x["mtime"], x["size"]), reverse=True)
        primary = files[0]
        label = files[0]["label"] if files else pid
        
        index[f"PP-{paper_num:03d}"] = {
            "id": f"PP-{paper_num:03d}",
            "title": label,
            "group_key": pid,
            "primary_path": primary["path"],
            "version_count": len(files),
            "latest_mtime": primary["mtime"],
            "versions": files,
            "is_ours": any(pid == g[0] for g in PAPER_GROUPS + STANDALONE_PAPERS)
        }
        paper_num += 1
    
    return index, dict(non_papers)

def generate_report(index, non_papers):
    """Generate clean paper report"""
    our_papers = {k: v for k, v in index.items() if v["is_ours"]}
    ref_papers = {k: v for k, v in index.items() if not v["is_ours"]}
    
    md = []
    md.append(f"# 📄 论文版本跟踪索引 v2")
    md.append(f"")
    md.append(f"> **更新时间**: {TODAY}")
    md.append(f"> **我们的论文**: {len(our_papers)} 篇")
    md.append(f"> **参考文献/他人论文**: {len(ref_papers)} 篇")
    md.append(f"> **非论文内容**: {sum(len(v) for v in non_papers.values())} 个文件（已排除）")
    md.append(f"")
    
    # OUR PAPERS
    md.append(f"---")
    md.append(f"## 📝 我们撰写的论文 ({len(our_papers)} 篇)")
    md.append(f"")
    
    for pid, v in sorted(our_papers.items()):
        md.append(f"### {pid}: {v['title'][:80]}")
        md.append(f"- **版本数**: {v['version_count']} | **最新**: {v['latest_mtime']}")
        md.append(f"- **主文件**: `{v['primary_path']}`")
        for ver in v["versions"]:
            marker = "⭐" if ver["path"] == v["primary_path"] else "  "
            md.append(f"  {marker} `{ver['name'][:80]}` ({ver['mtime']}, {ver['size']//1024}KB)")
        md.append("")
    
    # REFERENCE PAPERS
    if ref_papers:
        md.append(f"---")
        md.append(f"## 📚 参考文献/他人论文 ({len(ref_papers)} 篇)")
        md.append(f"")
        md.append(f"> 以下为他人发表的论文，作为研究参考")
        md.append(f"")
        for pid, v in sorted(ref_papers.items()):
            md.append(f"- **{pid}**: {v['title'][:60]} `v{v['version_count']}` {v['latest_mtime']}")
    
    # NON-PAPER EXCLUDED
    md.append(f"")
    md.append(f"---")
    md.append(f"## 🚫 已排除的非论文内容")
    md.append(f"")
    for cat, files in sorted(non_papers.items()):
        md.append(f"- **{cat}**: {len(files)} 个文件（如: {files[0][:50] if files else 'N/A'}）")
    
    return "\n".join(md)

if __name__ == "__main__":
    print("Building correct paper index (51_Papers only)...")
    index, non_papers = build_correct_index()
    
    our_count = sum(1 for v in index.values() if v["is_ours"])
    ref_count = sum(1 for v in index.values() if not v["is_ours"])
    
    print(f"  Our papers: {our_count}")
    print(f"  Reference papers: {ref_count}")
    print(f"  Excluded non-papers: {sum(len(v) for v in non_papers.values())}")
    
    # Show our papers
    for pid, v in sorted(index.items()):
        if v["is_ours"]:
            print(f"  {pid}: {v['title'][:60]} ({v['version_count']} versions)")
    
    # Generate report
    report = generate_report(index, non_papers)
    out = VAULT / "50_Output" / "51_Papers" / "00_Paper_Versions_Index.md"
    out.write_text(report, encoding="utf-8")
    
    # Save JSON
    json_out = VAULT / "50_Output" / "51_Papers" / "paper_versions.json"
    json.dump({
        "our_papers": {k: v for k, v in index.items() if v["is_ours"]},
        "reference_papers": {k: v for k, v in index.items() if not v["is_ours"]},
        "excluded": {k: len(v) for k, v in non_papers.items()},
        "total_our_papers": our_count,
        "total_reference": ref_count,
        "generated": TODAY
    }, open(str(json_out), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    
    print(f"\nReport: {out.stat().st_size//1024}KB")
    print(f"JSON: {json_out.stat().st_size//1024}KB")
