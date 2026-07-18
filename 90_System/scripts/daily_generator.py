"""
Daily Content Generator — generates today's Daily_Action, Daily_Focus, Research_Insights
from pipeline results and project state. Run after pipeline_v3.py.
"""
import json, os, sys, urllib.parse
from pathlib import Path
from datetime import datetime

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
MOC = VAULT / "60_MOC"
INSIGHTS = VAULT / "00_Inbox" / "_pipeline_insights"
PAPERS = VAULT / "50_Output" / "51_Papers"
META = VAULT / "99_Meta"
LOGS = VAULT / "logs"

TODAY = datetime.now()
TODAY_STR = TODAY.strftime("%Y-%m-%d")
TODAY_CN = TODAY.strftime("%Y年%m月%d日")

def get_today_papers():
    """Get today's crawled papers with TCC/iNEST relevance."""
    papers = []
    if INSIGHTS.exists():
        for f in sorted(INSIGHTS.glob(f"{TODAY_STR}_*.md"), reverse=True):
            content = f.read_text(encoding="utf-8", errors="ignore")
            title = ""
            for line in content.split("\n"):
                if line.startswith("title:"):
                    title = line.split("title:", 1)[1].strip().strip('"').strip("'")
                    break
            if not title:
                title = f.stem.replace(f"{TODAY_STR}_OA_", "").replace("_", " ")[:80]
            # Check TCC/iNEST relevance
            low = title.lower()
            tcc_kw = ["interconnect","noc","wafer","chiplet","3d-ic","topology","routing","network-on-chip","tsv","through-silicon","sdi","software-defined"]
            inest_kw = ["neuromorphic","spiking","reservoir","critical","emergence","higher-order","stdp","memristor","self-org","neural","brain","synaptic"]
            track = "General"
            if any(k in low for k in tcc_kw): track = "TCC"
            elif any(k in low for k in inest_kw): track = "iNEST"
            papers.append({"title": title, "track": track, "file": str(f.relative_to(VAULT)), "path": str(f)})
    return papers

def get_pipeline_summary():
    """Get latest pipeline run summary."""
    log_files = sorted(LOGS.glob(f"pipeline_{TODAY_STR.replace('-','')}*.json"), reverse=True)
    if log_files:
        return json.loads(log_files[0].read_text(encoding="utf-8"))
    return None

def get_active_papers():
    """Count active papers and patents."""
    paper_dirs = [d for d in PAPERS.iterdir() if d.is_dir() and not d.name.startswith((".","_","figures","manual"))]
    return len(paper_dirs)

def get_patent_count():
    patents = VAULT / "50_Output" / "52_Patents"
    if patents.exists():
        return len([d for d in patents.iterdir() if d.is_dir() and not d.name.startswith((".","_"))])
    return 0

def get_kb_stats():
    """Count vault notes."""
    total = 0
    tcc = 0
    inest = 0
    for root, dirs, files in os.walk(VAULT):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for f in files:
            if f.endswith(".md"):
                total += 1
                path_lower = os.path.join(root, f).lower()
                if "tcc" in path_lower or "30_tcc" in path_lower:
                    tcc += 1
                if "inest" in path_lower or "40_inest" in path_lower:
                    inest += 1
    return total, tcc, inest

def generate_daily_action(papers, pipeline):
    lines = []
    lines.append(f"# 每日行动洞察 — {TODAY_STR}")
    lines.append("")
    lines.append(f"> 自动生成于 {TODAY.strftime('%H:%M')} | 管线论文: {len(papers)} 篇 | 知识图谱: {pipeline.get('graph_nodes','?')}节点/{pipeline.get('graph_edges','?')}边")
    lines.append("")
    
    # Top TCC/iNEST papers
    tcc_papers = [p for p in papers if p["track"] == "TCC"][:3]
    inest_papers = [p for p in papers if p["track"] == "iNEST"][:5]
    
    if tcc_papers or inest_papers:
        lines.append("## 今日入库论文要点")
        lines.append("")
        
        if tcc_papers:
            lines.append("### TCC 相关")
            for p in tcc_papers:
                lines.append(f"- **{p['title'][:80]}** → [查看](http://127.0.0.1:8899/home/work/.openclaw/workspace/{urllib.parse.quote(str(p['file']).replace(chr(92), '/'))})")
            lines.append("")
        
        if inest_papers:
            lines.append("### iNEST 相关")
            for p in inest_papers:
                lines.append(f"- **{p['title'][:80]}** → [查看](http://127.0.0.1:8899/home/work/.openclaw/workspace/{urllib.parse.quote(str(p['file']).replace(chr(92), '/'))})")
            lines.append("")
    
    # Today's recommended actions
    lines.append("## 今日推荐行动")
    lines.append("")
    lines.append("1. **审阅今日入库论文** — 重点阅读 TCC/iNEST 高相关文献，提炼可借鉴方法")
    lines.append("2. **更新研发看板灵感** — 将论文中的新思路迭代到研发路线图")
    lines.append("3. **CST 论文推进** — 继续修订 Section 4 仿真数据，目标 7月30日投稿")
    lines.append("4. **专利修订** — TCC 架构与实现两项专利，7月30日前申报")
    lines.append("5. **Git 同步检查** — 确认今日变更已推送到 GitHub/Gitee")
    lines.append("")
    
    if pipeline:
        lines.append(f"---")
        lines.append(f"*管线 v3.4 运行耗时: {pipeline.get('elapsed_s',0):.0f}s*")
    
    (MOC / "03_Daily_Action.md").write_text("\n".join(lines), encoding="utf-8")
    return True

def generate_daily_focus(papers):
    lines = []
    lines.append(f"## 今日焦点 — {TODAY_STR}")
    lines.append("")
    lines.append("**并行主线**")
    lines.append("")
    lines.append("1.  [论文] CST 智能涌现 — 修订 Section 4 + 5，目标 7.30 投 Engineering")
    lines.append("    → [P1_Superadditivity_1+1_gt_2_Proof.md](http://127.0.0.1:8899/home/work/.openclaw/workspace/50_Output/51_Papers/A%E7%BB%84_CST%E5%9F%BA%E7%A1%80%E7%90%86%E8%AE%BA/P1_Superadditivity_1+1_gt_2_Proof.md)")
    lines.append("2.  [论文] TCC 拓扑中心计算范式 — P-Paradigm 修订，7.30 投 Engineering")
    lines.append("    → [TCC_Software_Defined_Interconnect_%E6%8B%93%E6%89%91%E4%B8%AD%E5%BF%83%E8%AE%A1%E7%AE%97%E8%8C%83%E5%BC%8F.md](http://127.0.0.1:8899/home/work/.openclaw/workspace/50_Output/51_Papers/TCC_Software_Defined_Interconnect_%E6%8B%93%E6%89%91%E4%B8%AD%E5%BF%83%E8%AE%A1%E7%AE%97%E8%8C%83%E5%BC%8F.md)")
    lines.append("3.  [专利] TCC 架构 + 实现专利 — 7.30 前申报")
    lines.append("4.  [工程] CST 仿真实验 — 继续 SDI N=1024 相位扫描")
    lines.append("")
    
    # Today's pipeline insights
    tcc_p = [p for p in papers if p["track"] == "TCC"][:2]
    inest_p = [p for p in papers if p["track"] == "iNEST"][:2]
    
    if tcc_p or inest_p:
        lines.append("## 今日文献启发")
        lines.append("")
        for p in tcc_p + inest_p:
            lines.append(f"- [{p['track']}] {p['title'][:70]}")
        lines.append("")
    
    lines.append(f"---")
    lines.append(f"*生成于 {TODAY.strftime('%Y-%m-%d %H:%M')}*")
    
    (MOC / "04_Daily_Focus.md").write_text("\n".join(lines), encoding="utf-8")
    return True

def generate_research_insights(papers):
    lines = []
    lines.append(f"# 研究洞察 — {TODAY_STR}")
    lines.append("")
    lines.append(f"> 今日入库 {len(papers)} 篇论文 | 自动洞察生成")
    lines.append("")
    
    tcc_p = [p for p in papers if p["track"] == "TCC"][:5]
    inest_p = [p for p in papers if p["track"] == "iNEST"][:5]
    
    if tcc_p:
        lines.append("## TCC 方向洞察")
        lines.append("")
        for p in tcc_p:
            lines.append(f"- [{p['title'][:80]}](http://127.0.0.1:8899/home/work/.openclaw/workspace/{urllib.parse.quote(str(p['file']).replace(chr(92), '/'))})")
        lines.append("")
    
    if inest_p:
        lines.append("## iNEST 方向洞察")
        lines.append("")
        for p in inest_p:
            lines.append(f"- [{p['title'][:80]}](http://127.0.0.1:8899/home/work/.openclaw/workspace/{urllib.parse.quote(str(p['file']).replace(chr(92), '/'))})")
        lines.append("")
    
    lines.append("## 创新迭代建议")
    lines.append("")
    lines.append("1. 审视上述论文方法论，评估是否可融入 TCC 拓扑计算框架")
    lines.append("2. 检查高阶网络/储备池方向的最新进展对 iNEST SNN 架构的启发")
    lines.append("3. 关注存算一体/忆阻器方向的工程化进展，对齐 iNEST 硬件路线")
    lines.append("")
    lines.append(f"*生成于 {TODAY.strftime('%Y-%m-%d %H:%M')}*")
    
    (MOC / "02_Research_Insights.md").write_text("\n".join(lines), encoding="utf-8")
    return True

if __name__ == "__main__":
    print(f"Daily Generator — {TODAY_STR}")
    
    papers = get_today_papers()
    pipeline = get_pipeline_summary() or {}
    kb_total, kb_tcc, kb_inest = get_kb_stats()
    papers_count = get_active_papers()
    patents_count = get_patent_count()
    
    print(f"  Papers crawled: {len(papers)}")
    print(f"  KB: {kb_total} notes ({kb_tcc} TCC, {kb_inest} iNEST)")
    print(f"  Active papers: {papers_count} | Patents: {patents_count}")
    
    generate_daily_action(papers, pipeline)
    print("  [OK] 03_Daily_Action.md")
    
    generate_daily_focus(papers)
    print("  [OK] 04_Daily_Focus.md")
    
    generate_research_insights(papers)
    print("  [OK] 02_Research_Insights.md")
    
    print("Done")
