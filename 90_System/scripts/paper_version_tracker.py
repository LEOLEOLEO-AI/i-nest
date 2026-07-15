"""Paper Version Tracker v3 — handle Chinese paper names, all our papers"""
import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
TODAY = datetime.now().strftime("%Y-%m-%d")

PAPER_GROUPS = [
    ("A1", "CST Theory: 智能涌现的复杂度阈值定理",
     [r"A1_CST.*V\d+", r"A1_CST.*FINAL", r"A1_CST.*CLEAN", r"A1_CST.*SUBMISSION",
      r"A1_Cover", r"A1_Submission", r"A1_Light", r"A1_ARS",
      r"学生.*A1", r"冲刺.*A1", r"工作包.*A1", r"CST_Intelligence_Emergence"]),
    ("B0", "NCC Engineering: 晶圆级拓扑计算工程实现",
     [r"B0_Engineering", r"B0_Cover", r"B0_Submission", r"学生.*B0", r"冲刺.*B0"]),
    ("A_B7", "Route-Transform: 路由变换同构理论 (ASPLOS27)",
     [r"论文A_B7", r"B7_Route", r"Route.*Transform.*ASPLOS"]),
    ("B_B5", "TCC11: 拓扑中心计算11节点系统实现 (ASPLOS27)",
     [r"论文B_B5", r"B5_TCC11", r"TCC11.*ASPLOS"]),
    ("B4", "Route IS Transform Isomorphism Draft",
     [r"B4_Route", r"Route.*IS.*Transform.*Isomorphism"]),
    ("SDI_CC", "SDI-CC: 拓扑即计算新范式",
     [r"SDI.?CC", r"拓扑即计算"]),
    ("P_Paradigm", "P-Paradigm: 综述论文 (Nature Electronics)",
     [r"P.?Paradigm", r"综述论文.*Nature"]),
    ("P_Mapping", "P-Mapping: 六原语物理拓扑映射",
     [r"P.?Mapping", r"六原语.*拓扑映射", r"5plus4.*拓扑映射"]),
]

NON_PAPER_PATTERNS = {
    "getnote_clipping": [r"getnote", r"GetNote", r"得到"],
    "project_guide": [r"重大专项", r"项目指南", r"项目建议", r"卫星智能体"],
    "reference_material": [r"白皮书", r"报告.*深度", r"DARPA", r"Nature论文写作", r"AI辅助综述"],
    "planning_doc": [r"推进计划", r"总览", r"规划", r"管线", r"导航", r"冲刺|工作包|任务包"],
    "admin_template": [r"模板", r"引用模板", r"ARS.*审查", r"ARS.*报告"],
    "knowledge_base": [r"knowledge.*base", r"baseline", r"知识基线"],
    "index_moc": [r"MOC", r"索引", r"总清单"],
}

def classify(f):
    name = f.name; stem = f.stem
    
    # Check non-paper first
    for cat, pats in NON_PAPER_PATTERNS.items():
        for p in pats:
            if re.search(p, name) or re.search(p, stem): return None, cat
    
    # Check our paper groups
    for pid, title, pats in PAPER_GROUPS:
        for p in pats:
            if re.search(p, name) or re.search(p, stem): return pid, title
    
    # Check generic paper patterns (starts with 论文, or has paper indicators)
    if re.search(r"论文|Paper|paper", name):
        try:
            c = f.read_text(encoding="utf-8", errors="replace")
            if len(c) > 500: return stem[:40], f.name[:60]
        except: pass
    
    # Check for paper-like content
    try:
        c = f.read_text(encoding="utf-8", errors="replace")[:2000]
        indicators = sum(1 for kw in ["abstract","introduction","conclusion","method",
                        "result","arXiv","doi","参考文献","相关工作"] if kw.lower() in c.lower())
        if indicators >= 3 and len(c) > 1000: return stem[:40], f.name[:60]
    except: pass
    
    return None, "other"

# Build index
papers_dir = VAULT / "50_Output" / "51_Papers"
groups = {}; non_papers = {}

for f in papers_dir.rglob("*.md"):
    if "00_Paper" in f.name or f.stat().st_size < 200: continue
    pid, label = classify(f)
    if pid:
        groups.setdefault(pid, []).append({
            "name": f.name, "path": str(f.relative_to(VAULT)),
            "size": f.stat().st_size,
            "mtime": datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d")
        })
    else:
        non_papers.setdefault(label, []).append(f.name)

# Build report
our_groups = {k: v for k, v in groups.items() if any(k == g[0] for g in PAPER_GROUPS)}
ref_groups = {k: v for k, v in groups.items() if k not in our_groups}

md = [f"# 论文版本跟踪索引 v3", f"", f"> **更新时间**: {TODAY}",
      f"> **我们撰写的论文**: {len(our_groups)} 篇",
      f"> **参考文献**: {len(ref_groups)} 篇",
      f"> **排除的非论文**: {sum(len(v) for v in non_papers.values())} 文件", f""]

md.append("---")
md.append(f"## 我们撰写的论文 ({len(our_groups)} 篇)")
md.append("")

for pid, vers in sorted(our_groups.items()):
    vers.sort(key=lambda x: (x["mtime"], x["size"]), reverse=True)
    primary = vers[0]
    title = next((g[1] for g in PAPER_GROUPS if g[0] == pid), pid)
    md.append(f"### PP-{pid}: {title}")
    md.append(f"- 版本数: **{len(vers)}** | 最新: {primary['mtime']}")
    for v in vers:
        m = "⭐" if v["path"] == primary["path"] else "  "
        md.append(f"  {m} `{v['name'][:80]}` ({v['mtime']}, {v['size']//1024}KB)")
    md.append("")

if ref_groups:
    md.append("---")
    md.append(f"## 参考文献/他人论文 ({len(ref_groups)} 篇)")
    md.append("")
    for pid, vers in sorted(ref_groups.items()):
        md.append(f"- **{pid}**: {vers[0]['name'][:60]} v{len(vers)}")

md.append("")
md.append("---")
md.append("## 已排除的非论文")
md.append("")
for cat, files in sorted(non_papers.items()):
    md.append(f"- **{cat}**: {len(files)} 文件")

out = VAULT / "50_Output/51_Papers/00_Paper_Versions_Index.md"
out.write_text("\n".join(md), encoding="utf-8")

total_versions = sum(len(v) for v in our_groups.values())
print(f"Our papers: {len(our_groups)}, total version files: {total_versions}")
for pid, vers in sorted(our_groups.items()):
    title = next((g[1] for g in PAPER_GROUPS if g[0] == pid), pid)
    print(f"  PP-{pid}: {title} ({len(vers)} versions)")
print(f"Reference: {len(ref_groups)}")
print(f"Excluded: {sum(len(v) for v in non_papers.values())}")
