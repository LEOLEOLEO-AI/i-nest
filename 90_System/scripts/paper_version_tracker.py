"""Paper Version Tracker v4 — include intermediate files, version status tracking"""
import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
TODAY = datetime.now().strftime("%Y-%m-%d")

PAPER_GROUPS = [
    ("A1", "CST Theory: 智能涌现的复杂度阈值定理", [
        r"A1_CST.*V\d+", r"A1_CST.*FINAL", r"A1_CST.*CLEAN", r"A1_CST.*SUBMISSION",
        r"A1_Cover", r"A1_Submission", r"A1_Light", r"A1_ARS",
        r"CST_Intelligence_Emergence", r"学生.*A1", r"冲刺.*A1", r"工作包.*A1",
        r"01_ARS_Peer", r"02_ARS_Citation", r"03_ARS_Revision",
        r"FINAL_EXECUTION_REPORT", r"A1_CST_Phase1",
    ]),
    ("B0", "NCC Engineering: 晶圆级拓扑计算工程实现", [
        r"B0_Engineering", r"B0_Cover", r"B0_Submission",
        r"学生.*B0", r"冲刺.*B0", r"TCC_SDI_ARS",
        r"学生1_工作包_TCC", r"学生1_任务包_P1",
    ]),
    ("A_B7", "Route-Transform: 路由变换同构理论 (ASPLOS27)", [
        r"论文A_B7", r"B7_Route", r"Route.*Transform.*ASPLOS",
    ]),
    ("B_B5", "TCC11: 拓扑中心计算11节点系统实现 (ASPLOS27)", [
        r"论文B_B5", r"B5_TCC11", r"TCC11.*ASPLOS",
    ]),
    ("B4", "Route IS Transform Isomorphism Draft", [
        r"B4_Route", r"Route.*IS.*Transform.*Isomorphism",
    ]),
    ("SDI_CC", "SDI-CC: 拓扑即计算新范式", [
        r"SDI.?CC", r"拓扑即计算",
    ]),
    ("P_Paradigm", "P-Paradigm: 综述论文 (Nature Electronics)", [
        r"P.?Paradigm", r"综述论文.*Nature",
    ]),
    ("P_Mapping", "P-Mapping: 六原语物理拓扑映射", [
        r"P.?Mapping", r"六原语.*拓扑映射", r"5plus4.*拓扑映射",
    ]),
]

NON_PAPER = {
    "getnote": [r"getnote", r"GetNote", r"得到"],
    "project_guide": [r"重大专项", r"项目指南", r"项目建议", r"卫星智能体", r"iNEST_项目布局", r"iNEST 项目指南", r"\[V2\] iNEST"],
    "reference": [r"白皮书", r"报告.*深度", r"DARPA", r"Nature论文写作", r"AI辅助综述", r"manual"],
    "admin": [r"模板", r"引用模板", r"iNEST_论文计划", r"iNEST_00_论文", r"00_论文总清单", r"00_冲刺", r"00_TCC_INEST", r"00_TCC_论文", r"Nature论文写作",
              r"iNEST 论文计划", r"论文矩阵计划", r"论文计划\.md", r"论文计划列表", r"00_论文导航", r"学生3_", r"学生4_"],
}

def classify(f):
    name = f.name; stem = f.stem
    for cat, pats in NON_PAPER.items():
        for p in pats:
            if re.search(p, name): return None, cat
    for pid, title, pats in PAPER_GROUPS:
        for p in pats:
            if re.search(p, name) or re.search(p, stem): return pid, title
    try:
        c = f.read_text(encoding="utf-8", errors="replace")[:2000]
        if len(c) > 1000:
            indicators = sum(1 for kw in ["abstract","introduction","conclusion","method",
                            "result","arXiv","doi","参考文献","相关工作"] if kw.lower() in c.lower())
            if indicators >= 3: return stem[:40], f.name[:60]
    except: pass
    return None, "other"

def version_status(name, mtime):
    """Determine version status from filename and date"""
    n = name.lower()
    if "ars_revised" in n or "v31_ars" in n: return "ARS修订后", 3
    if "submission_ready" in n or "v28_submission" in n: return "投稿就绪", 2
    if "_v3" in n and "final" in n: return "终稿", 2
    if "final" in n or "FINAL" in name: return "终稿", 2
    if "_v2" in n or "revised" in n: return "修订版", 1
    if "cover" in n or "checklist" in n: return "投稿附件", 0
    if "ars" in n or "peer_review" in n or "citation_compliance" in n: return "评审材料", 0
    if "execution_report" in n or "phase1" in n: return "中间报告", 0
    return "草稿", 0

# Scan
papers_dir = VAULT / "50_Output" / "51_Papers"
groups = {}; non_papers = {}

for f in papers_dir.rglob("*.md"):
    if "00_Paper" in f.name or f.stat().st_size < 200: continue
    pid, label = classify(f)
    mtime = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d")
    status, priority = version_status(f.name, mtime)
    
    entry = {
        "name": f.name, "path": str(f.relative_to(VAULT)),
        "size": f.stat().st_size, "mtime": mtime,
        "status": status, "priority": priority
    }
    
    if pid:
        groups.setdefault(pid, []).append(entry)
    else:
        non_papers.setdefault(label, []).append(f.name)

# Build report
our_groups = {k: v for k, v in groups.items() if any(k == g[0] for g in PAPER_GROUPS)}
ref_groups = {k: v for k, v in groups.items() if k not in our_groups}

md = [f"# 论文版本跟踪索引 v4", f"",
      f"> **更新时间**: {TODAY}",
      f"> **我们撰写的论文**: {len(our_groups)} 篇",
      f"> **参考文献**: {len(ref_groups)} 篇",
      f"> **排除的非论文**: {sum(len(v) for v in non_papers.values())} 文件",
      f"", f"---", f"## 我们撰写的论文 ({len(our_groups)} 篇)", f""]

for pid, vers in sorted(our_groups.items()):
    vers.sort(key=lambda x: (x["priority"], x["mtime"], x["size"]), reverse=True)
    primary = vers[0]
    title = next((g[1] for g in PAPER_GROUPS if g[0] == pid), pid)
    
    # Count by type
    main_versions = [v for v in vers if v["priority"] >= 1]
    support_files = [v for v in vers if v["priority"] == 0]
    
    md.append(f"### PP-{pid}: {title}")
    md.append(f"- 主版本: **{len(main_versions)}** | 支撑材料: **{len(support_files)}** | 最新: {primary['mtime']}")
    md.append(f"- ⭐ 最新版: `{primary['name'][:80]}` ({primary['mtime']}, {primary['size']//1024}KB) [{primary['status']}]")
    md.append("")
    
    if main_versions:
        md.append("**主版本链**:")
        for v in main_versions:
            m = "→" if v["path"] == primary["path"] else "  "
            md.append(f"  {m} `{v['name'][:80]}` [{v['status']}] {v['mtime']}")
    
    if support_files:
        md.append("")
        md.append("**支撑材料**:")
        for v in support_files:
            md.append(f"  - `{v['name'][:80]}` ({v['size']//1024}KB) {v['mtime']}")
    md.append("")

# References
if ref_groups:
    md.append("---")
    md.append(f"## 参考文献/他人论文 ({len(ref_groups)} 篇)")
    md.append("")
    for pid, vers in sorted(ref_groups.items()):
        md.append(f"- **{pid}**: {vers[0]['name'][:60]} v{len(vers)}")

# Excluded
md.append("")
md.append("---")
md.append("## 已排除的非论文")
md.append("")
for cat, files in sorted(non_papers.items()):
    md.append(f"- **{cat}**: {len(files)} 文件")

out = VAULT / "50_Output/51_Papers/00_Paper_Versions_Index.md"
out.write_text("\n".join(md), encoding="utf-8")

total = sum(len(v) for v in our_groups.values())
main_count = sum(sum(1 for v in vers if v["priority"] >= 1) for vers in our_groups.values())
support_count = sum(sum(1 for v in vers if v["priority"] == 0) for vers in our_groups.values())

print(f"Our papers: {len(our_groups)}")
print(f"  Main versions: {main_count}")
print(f"  Support materials: {support_count}")
print(f"Reference: {len(ref_groups)}")
print(f"Excluded: {sum(len(v) for v in non_papers.values())}")
for pid, vers in sorted(our_groups.items()):
    title = next((g[1] for g in PAPER_GROUPS if g[0] == pid), pid)
    main = [v for v in vers if v["priority"] >= 1]
    support = [v for v in vers if v["priority"] == 0]
    latest = max(vers, key=lambda x: (x["priority"], x["mtime"]))
    print(f"  PP-{pid}: {title}")
    print(f"    Versions: {len(main)}, Support: {len(support)}, Latest: {latest['name'][:60]} [{latest['status']}]")
