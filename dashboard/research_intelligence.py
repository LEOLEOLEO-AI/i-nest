import os, re, json, glob
from datetime import datetime, timedelta
from collections import Counter

WORKSPACE = r"D:\Obsidian\home\work\.openclaw\workspace"
WEB_CLIPS = os.path.join(WORKSPACE, "03_Topics", "Web-Clips")
INDEX_HTML = os.path.join(WORKSPACE, "dashboard", "index.html")

TCC_THEMES = {
    "topology_computing": {"kw": ["topology","topological","graph neural","gnn","graph operator","persistent homology","betti","network topology","interconnect","routing"],"label": "Topology Computing Primitives","branch": ["论文","专利","代码"]},
    "formal_methods": {"kw": ["verification","formal","neural ode","guarantee","safety-critical","robustness bound"],"label": "Formal Verification","branch": ["论文","专利"]},
    "distributed_intelligence": {"kw": ["space data center","orbital computing","agentic","multi-agent","collective intelligence","distributed"],"label": "Distributed Intelligence","branch": ["论文","指南"]},
    "hardware_accel": {"kw": ["fpga","asic","wafer","chip","silicon","accelerator","in-memory","memristor"],"label": "Hardware Acceleration","branch": ["专利","代码"]},
}
INEST_THEMES = {
    "physical_neural": {"kw": ["physical neural","magnonic","neuromorphic","spiking","snn","liquid state","reservoir","nonlinear wave"],"label": "Physical Neural Computing","branch": ["论文","专利","代码"]},
    "criticality": {"kw": ["critical","phase transition","self-organized","avalanche","power law","scale-free","small-world","emergence"],"label": "Criticality & Emergence","branch": ["论文","指南"]},
    "liquid_computing": {"kw": ["liquid time-constant","ltc","continuous-time","neural ode","dynamical system"],"label": "Liquid Computing","branch": ["论文","代码"]},
    "free_energy": {"kw": ["free energy","fep","variational","bayesian brain","active inference","predictive coding"],"label": "Free Energy Principle","branch": ["论文","指南"]},
    "industry": {"kw": ["darpa","roadmap","semiconductor","chiplet","advanced packaging","heterogeneous"],"label": "Industry Trends","branch": ["指南","专利"]},
}

def read_recent_content(days=7):
    papers = []
    cutoff = datetime.now() - timedelta(days=days)
    for f in sorted(glob.glob(os.path.join(WEB_CLIPS, "*.md")), reverse=True):
        mtime = datetime.fromtimestamp(os.path.getmtime(f))
        if mtime < cutoff: continue
        try:
            with open(f, "r", encoding="utf-8") as fh:
                content = fh.read()
            entries = re.findall(r"-\s*\*?\*?\[(.+?)\]\((.+?)\)\*?\*?\s*\n\s*-\s*(.+?)\n\s*-\s*(.+?)(?=\n\s*-|\n\n|\Z)", content, re.DOTALL)
            for title, url, source_line, abstract in entries:
                papers.append({"title": title.strip(), "url": url.strip(), "abstract": abstract.strip()[:500], "date": mtime.strftime("%Y-%m-%d")})
        except: pass
    return papers

def classify_paper(paper):
    text = (paper["title"] + " " + paper["abstract"]).lower()
    results = {"TCC": [], "iNEST": []}
    for tid, theme in TCC_THEMES.items():
        score = sum(1 for kw in theme["kw"] if kw.lower() in text)
        if score > 0: results["TCC"].append({"theme": tid, "label": theme["label"], "score": score, "branches": theme["branch"]})
    for tid, theme in INEST_THEMES.items():
        score = sum(1 for kw in theme["kw"] if kw.lower() in text)
        if score > 0: results["iNEST"].append({"theme": tid, "label": theme["label"], "score": score, "branches": theme["branch"]})
    return results

def read_entries():
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()
    dd_s = html.find("var DEFAULT_DATA = ")
    dd_e = html.find("};", dd_s) + 2
    data_str = html[dd_s + len("var DEFAULT_DATA = "):dd_e - 1]
    m = re.search(r"\{(.+)\}", data_str)
    return json.loads(m.group(0))["entries"]

def cross_reference(papers, entries):
    insights = []
    entry_themes = {}
    for e in entries:
        text = (e["title"] + " " + e.get("desc", "")).lower()
        for kw_set in [TCC_THEMES, INEST_THEMES]:
            for tid, theme in kw_set.items():
                if any(kw in text for kw in theme["kw"]):
                    entry_themes.setdefault(tid, []).append(e)
    for paper in papers:
        themes = classify_paper(paper)
        for dim in ["TCC", "iNEST"]:
            for match in themes[dim]:
                tid = match["theme"]
                label = match["label"]
                existing = entry_themes.get(tid, [])
                if not existing:
                    insights.append({"type":"gap","dim":dim,"theme":label,"title":paper["title"][:80],"message":f"New direction [{label}] from [{paper['title'][:40]}], no existing entry. Consider starting.","branches":match["branches"],"impact":8,"feasibility":5,"priority":"high"})
                else:
                    insights.append({"type":"reinforce","dim":dim,"theme":label,"title":paper["title"][:80],"message":f"Latest [{paper['title'][:40]}] supports [{label}], add to {existing[0]['cat']} [{existing[0]['title'][:30]}].","branches":match["branches"],"impact":5,"feasibility":9,"priority":"medium"})
    seen = set()
    unique = []
    for ins in insights:
        key = (ins["type"], ins["theme"])
        if key not in seen: seen.add(key); unique.append(ins)
    unique.sort(key=lambda x: (x["impact"] + x["feasibility"]), reverse=True)
    return unique[:10]

def generate_plan_from_insights(insights):
    plan = []
    for ins in insights[:5]:
        dim = ins["dim"]
        if ins["type"] == "gap":
            for branch in ins["branches"][:1]:
                tag = {"论文":"[Paper]","专利":"[Patent]","指南":"[Guide]","代码":"[Code]"}.get(branch, "[Research]")
                plan.append({"text": f"{tag} [NEW] {ins['theme']}: {ins['title'][:35]}", "dot": "plan", "dim": dim})
        else:
            plan.append({"text": f"[Ref] Import: {ins['title'][:45]}", "dot": "plan", "dim": dim})
    return plan

def run_intelligence(days=7):
    papers = read_recent_content(days)
    entries = read_entries()
    insights = cross_reference(papers, entries)
    plan = generate_plan_from_insights(insights)
    return {"papers": papers, "insights": insights, "plan": plan}

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    r = run_intelligence(7)
    print(f"Papers: {len(r['papers'])} | Insights: {len(r['insights'])} | Plan: {len(r['plan'])}")
    for ins in r["insights"][:8]:
        tag = "[GAP]" if ins["type"] == "gap" else "[REF]"
        print(f"  {tag} [{ins['dim']}] {ins['theme']} - {ins['message'][:80]}")
