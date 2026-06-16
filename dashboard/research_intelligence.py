"""
R&D Intelligence Cockpit - Core Engine
=======================================
Reads new content → analyzes themes → cross-references with entries →
generates ranked insights → feeds back into work plan.

TCC: 拓扑中心计算 — computation paradigm shift from node-centric to topology-centric
iNEST: 复杂网络涌现智能 — intelligence emergence from network complexity

4 Branches: 论文 | 专利 | 项目指南策划 | 产品代码开发
"""
import os, re, json, glob
from datetime import datetime, timedelta
from collections import Counter

WORKSPACE = r"D:\Obsidian\home\work\.openclaw\workspace"
WEB_CLIPS = os.path.join(WORKSPACE, "03_Topics", "Web-Clips")
INBOX = os.path.join(WORKSPACE, "00_Inbox")
INDEX_HTML = os.path.join(WORKSPACE, "dashboard", "index.html")

# ─── Theme Maps ───
TCC_THEMES = {
    "topology_computing": {
        "kw": ["topology", "topological", "graph neural", "gnn", "non-euclidean",
               "graph operator", "persistent homology", "betti", "combinatorial",
               "network topology", "interconnect", "routing", "data center"],
        "label": "拓扑计算原语与架构",
        "branch": ["论文", "专利", "产品代码开发"]
    },
    "formal_methods": {
        "kw": ["verification", "formal", "ode", "neural ode", "guarantee",
               "safety-critical", "reachability", "barrier", "robustness bound"],
        "label": "形式化验证与安全保证",
        "branch": ["论文", "专利"]
    },
    "distributed_intelligence": {
        "kw": ["space data center", "orbital computing", "agentic", "multi-agent",
               "collective intelligence", "distributed system", "coordinated"],
        "label": "分布式智能与群体涌现",
        "branch": ["论文", "项目指南策划"]
    },
    "hardware_accel": {
        "kw": ["fpga", "asic", "wafer", "chip", "silicon", "interconnect",
               "memory", "accelerator", "tpu", "npu", "in-memory"],
        "label": "硬件加速与芯片架构",
        "branch": ["专利", "产品代码开发"]
    }
}

INEST_THEMES = {
    "physical_neural": {
        "kw": ["physical neural", "magnonic", "memristor", "neuromorphic",
               "spiking", "snn", "loihi", "liquid state", "reservoir",
               "nonlinear wave", "magnetic", "spin", "phase change"],
        "label": "物理神经计算与新型硬件",
        "branch": ["论文", "专利", "产品代码开发"]
    },
    "criticality_emergence": {
        "kw": ["critical", "phase transition", "self-organized", "avalanche",
               "power law", "scale-free", "small-world", "renormalization",
               "emergence", "complexity", "bifurcation", "edge of chaos"],
        "label": "临界性与涌现机制",
        "branch": ["论文", "项目指南策划"]
    },
    "liquid_computing": {
        "kw": ["liquid time-constant", "ltc", "continuous-time", "neural ode",
               "dynamical system", "attractor", "trajectory", "ode network"],
        "label": "液态计算与连续时间网络",
        "branch": ["论文", "产品代码开发"]
    },
    "free_energy": {
        "kw": ["free energy", "fep", "variational", "bayesian brain",
               "active inference", "predictive coding", "entropy", "kl divergence"],
        "label": "自由能原理与贝叶斯智能",
        "branch": ["论文", "项目指南策划"]
    },
    "industry_trends": {
        "kw": ["darpa", "roadmap", "semiconductor", "chiplet", "advanced packaging",
               "3d integration", "heterogeneous", "silicon photonics", "quantum"],
        "label": "产业趋势与技术路线",
        "branch": ["项目指南策划", "专利"]
    }
}

BRANCH_MAP = {
    "论文": "paper",
    "专利": "patent",
    "项目指南策划": "guide",
    "产品代码开发": "code"
}

# ─── Content Analyzer ───
def read_recent_content(days=7):
    """Read recent web clips and extract papers/topics"""
    papers = []
    cutoff = datetime.now() - timedelta(days=days)
    
    for f in sorted(glob.glob(os.path.join(WEB_CLIPS, "*.md")), reverse=True):
        mtime = datetime.fromtimestamp(os.path.getmtime(f))
        if mtime < cutoff:
            continue
        try:
            with open(f, 'r', encoding='utf-8') as fh:
                content = fh.read()
            # Extract individual paper entries
            entries = re.findall(r'-\s*\*?\*?\[(.+?)\]\((.+?)\)\*?\*?\s*\n\s*-\s*(.+?)\n\s*-\s*(.+?)(?=\n\s*-|\n\n|\Z)', content, re.DOTALL)
            for title, url, source_line, abstract in entries:
                papers.append({
                    "title": title.strip(),
                    "url": url.strip(),
                    "source": source_line.strip(),
                    "abstract": abstract.strip()[:500],
                    "date": mtime.strftime("%Y-%m-%d"),
                    "crawl_file": os.path.basename(f)
                })
        except Exception:
            pass
    
    return papers

def classify_paper(paper):
    """Classify paper into TCC/iNEST themes"""
    text = (paper["title"] + " " + paper["abstract"]).lower()
    results = {"TCC": [], "iNEST": []}
    
    for theme_id, theme in TCC_THEMES.items():
        score = sum(1 for kw in theme["kw"] if kw.lower() in text)
        if score > 0:
            results["TCC"].append({"theme": theme_id, "label": theme["label"],
                                    "score": score, "branches": theme["branch"]})
    
    for theme_id, theme in INEST_THEMES.items():
        score = sum(1 for kw in theme["kw"] if kw.lower() in text)
        if score > 0:
            results["iNEST"].append({"theme": theme_id, "label": theme["label"],
                                      "score": score, "branches": theme["branch"]})
    
    return results

def read_entries():
    """Read current entries from index.html"""
    with open(INDEX_HTML, 'r', encoding='utf-8') as f:
        html = f.read()
    dd_s = html.find("var DEFAULT_DATA = ")
    dd_e = html.find("};", dd_s) + 2
    data_str = html[dd_s + len("var DEFAULT_DATA = "):dd_e - 1]
    m = re.search(r"\{(.+)\}", data_str)
    return json.loads(m.group(0))["entries"]

# ─── Insight Generator ───
def cross_reference(papers, entries):
    """Cross-reference new papers with existing entries to generate insights"""
    insights = []
    
    # Build entry index by keywords
    entry_themes = {}
    for e in entries:
        text = (e["title"] + " " + e.get("desc", "")).lower()
        cat = e["cat"]
        for kw_set in [TCC_THEMES, INEST_THEMES]:
            for tid, theme in kw_set.items():
                if any(kw in text for kw in theme["kw"]):
                    if tid not in entry_themes:
                        entry_themes[tid] = []
                    entry_themes[tid].append(e)
    
    # Analyze each paper
    for paper in papers:
        themes = classify_paper(paper)
        
        for dim in ["TCC", "iNEST"]:
            for match in themes[dim]:
                tid = match["theme"]
                label = match["label"]
                
                # Check: is this theme already covered in our entries?
                existing = entry_themes.get(tid, [])
                
                if not existing:
                    # GAP: New theme not in our work
                    insights.append({
                        "type": "gap",
                        "dim": dim,
                        "theme": label,
                        "title": paper["title"][:80],
                        "message": f"新发现「{label}」方向({paper['title'][:40]}…)，当前无对应研究条目。建议评估立项。",
                        "branches": match["branches"],
                        "impact": 8,
                        "feasibility": 5,
                        "priority": "高"
                    })
                else:
                    # REINFORCEMENT: Supports existing direction
                    insights.append({
                        "type": "reinforce",
                        "dim": dim,
                        "theme": label,
                        "title": paper["title"][:80],
                        "message": f"最新研究「{paper['title'][:40]}」支持「{label}」方向，可补充到{existing[0]['cat']}「{existing[0]['title'][:30]}」的参考文献。",
                        "branches": match["branches"],
                        "impact": 5,
                        "feasibility": 9,
                        "priority": "中"
                    })
    
    # De-duplicate and sort by impact
    seen = set()
    unique = []
    for ins in insights:
        key = (ins["type"], ins["theme"])
        if key not in seen:
            seen.add(key)
            unique.append(ins)
    
    unique.sort(key=lambda x: (x["impact"] + x["feasibility"]), reverse=True)
    return unique[:10]

def generate_plan_from_insights(insights):
    """Convert top insights into actionable plan items"""
    plan = []
    
    for ins in insights[:5]:
        dim = ins["dim"]
        if ins["type"] == "gap":
            for branch in ins["branches"][:1]:
                tag = {"论文": "[论文]", "专利": "[专利]", 
                       "项目指南策划": "[指南]", "产品代码开发": "[代码]"}.get(branch, "[研究]")
                plan.append({
                    "text": f"{tag} [新方向] {ins['theme']}: {ins['title'][:35]}",
                    "dot": "plan", "dim": dim
                })
        else:
            plan.append({
                "text": f"[资料] 导入参考文献: {ins['title'][:45]}",
                "dot": "plan", "dim": dim
            })
    
    return plan

# ─── Main Analysis ───
def run_intelligence(days=7):
    """Run the full intelligence pipeline"""
    print("=" * 60)
    print(f"R&D Intelligence Cockpit - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    # 1. Read new content
    papers = read_recent_content(days)
    print(f"\n[1] 内容摄入: {len(papers)} 篇论文(近{days}天)")
    
    # 2. Classify
    tcc_count = 0
    inest_count = 0
    theme_stats = Counter()
    for p in papers:
        themes = classify_paper(p)
        if themes["TCC"]: tcc_count += 1
        if themes["iNEST"]: inest_count += 1
        for t in themes["TCC"]:
            theme_stats[f"TCC:{t['label']}"] += 1
        for t in themes["iNEST"]:
            theme_stats[f"iNEST:{t['label']}"] += 1
    
    print(f"    TCC相关: {tcc_count} | iNEST相关: {inest_count}")
    print(f"    主题分布:")
    for theme, count in theme_stats.most_common(8):
        print(f"      {theme}: {count}")
    
    # 3. Cross-reference
    entries = read_entries()
    insights = cross_reference(papers, entries)
    print(f"\n[2] 交叉分析: {len(insights)} 条洞察")
    
    # 4. Generate plan
    plan = generate_plan_from_insights(insights)
    print(f"\n[3] 生成计划: {len(plan)} 条")
    
    return {
        "papers": papers,
        "theme_stats": dict(theme_stats),
        "insights": insights,
        "plan": plan
    }

if __name__ == "__main__":
    result = run_intelligence(7)
    
    print(f"\n{'='*60}")
    print("TOP INSIGHTS:")
    print(f"{'='*60}")
    for i, ins in enumerate(result["insights"][:8]):
        tag = "[GAP]" if ins["type"] == "gap" else "[REF]"
        print(f"\n{tag} [{ins['dim']}] {ins['theme']} (影响:{ins['impact']} 可行:{ins['feasibility']})")
        print(f"   {ins['message'][:100]}")
    
    print(f"\n{'='*60}")
    print("SUGGESTED PLAN ITEMS:")
    print(f"{'='*60}")
    for p in result["plan"]:
        print(f"   [{p['dim']}] {p['text'][:80]}")
