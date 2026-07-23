"""
Daily Content Generator v2.0 — deep per-paper LLM analysis
Generates: Daily_Action, Daily_Focus, Research_Insights
Run after pipeline_v3.py
"""
import hashlib, json, os, sys, urllib.parse, re
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

import sys
sys.path.insert(0, r"D:\\Obsidian\\scripts")
from llm_router import llm_call

def _call_jojo_fallback(prompt, system="", max_tokens=3000):  # deprecated, use llm_call
    """Direct JOJO call, no proxy."""
    import urllib.request, json
    url = "http://127.0.0.1:57321/v1/chat/completions"
    payload = {
        "model": "deepseek-v4-pro",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.3
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        resp = urllib.request.urlopen(req, timeout=60)
        d = json.loads(resp.read())
        content = d["choices"][0]["message"].get("content", "")
        return content
    except:
        return None

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
MOC = VAULT / "60_MOC"
INSIGHTS = VAULT / "00_Inbox" / "_pipeline_insights"
LOGS = VAULT / "logs"
TODAY = datetime.now(ZoneInfo("Asia/Shanghai"))
TODAY_STR = TODAY.strftime("%Y-%m-%d")
CACHE_FILE = VAULT / "99_Meta" / "daily_analysis_cache.json"


def analysis_cache_key(paper):
    source = "\n".join((paper.get("title", ""), paper.get("abstract", "")))
    return hashlib.sha256(source.encode("utf-8")).hexdigest()


def load_analysis_cache():
    try:
        cached = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        return cached if cached.get("schema") == "daily-analysis-cache-v1" else {"schema": "daily-analysis-cache-v1", "items": {}}
    except (OSError, json.JSONDecodeError):
        return {"schema": "daily-analysis-cache-v1", "items": {}}


def save_analysis_cache(cache):
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    temporary = CACHE_FILE.with_suffix(".tmp")
    temporary.write_text(json.dumps(cache, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(CACHE_FILE)

def get_today_papers():
    papers = []
    if INSIGHTS.exists():
        for f in sorted(INSIGHTS.glob(f"{TODAY_STR}_*.md"), reverse=True):
            content = f.read_text(encoding="utf-8", errors="ignore")
            # Parse frontmatter
            meta = {"file": str(f), "rel_path": str(f.relative_to(VAULT))}
            in_front = False
            for line in content.split("\n"):
                if line.strip() == "---":
                    if not in_front:
                        in_front = True
                        continue
                    else:
                        break
                if in_front and ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip().strip('"').strip("'")
            # Get abstract (after second ---)
            parts = content.split("---", 2)
            abstract = ""
            if len(parts) >= 3:
                abs_section = parts[2]
                m = re.search(r"## Abstract\s*\n+(.*?)(?:\n## |\Z)", abs_section, re.DOTALL)
                if m:
                    abstract = m.group(1).strip()[:2000]
            # Full body (everything after frontmatter, before Topics/Links)
            body = parts[2] if len(parts) >= 3 else ""
            body = re.sub(r"## Topics.*", "", body, flags=re.DOTALL)
            body = re.sub(r"## Links.*", "", body, flags=re.DOTALL)
            meta["abstract"] = abstract
            meta["body"] = body.strip()[:3000]
            meta["title"] = meta.get("title", f.stem.replace(f"{TODAY_STR}_OA_","").replace("_"," ")[:80])
            papers.append(meta)
    return papers

def score_paper(p):
    """Score TCC/iNEST relevance from metadata."""
    title = (p.get("title","") + " " + p.get("abstract","")).lower()
    tcc_kw = ["interconnect","noc","wafer","chiplet","3d","topology","routing","network-on-chip","tsv","through-silicon",
              "sdi","software-defined","photonic","packaging","integration","scale-up","scale-out"]
    inest_kw = ["neuromorphic","spiking","reservoir","critical","emergence","higher-order","stdp","memristor",
                "self-org","neural","brain","synaptic","dynamics","phase transition","bifurcation","snn",
                "plasticity","in-sensor","analog","in-memory computing"]
    tcc_s = sum(1 for k in tcc_kw if k in title)
    inest_s = sum(1 for k in inest_kw if k in title)
    track = p.get("track","")
    if "TCC" in track: tcc_s += 3
    if "iNEST" in track: inest_s += 3
    return tcc_s + inest_s, "TCC" if tcc_s > inest_s else ("iNEST" if inest_s > 0 else "General")

def deep_analyze_papers(papers, cache, top_n=8):
    """Analyze only new or changed title-and-abstract inputs."""
    top = sorted(papers, key=lambda p: score_paper(p)[0], reverse=True)[:top_n]
    results = []
    cache_hits = 0
    
    for i, p in enumerate(top):
        cache_key = analysis_cache_key(p)
        cached = cache["items"].get(cache_key)
        if cached:
            item = dict(cached["analysis"])
            item["id"] = i + 1
            results.append(item)
            cache_hits += 1
            continue

        title = p.get("title", "")[:150]
        abstract = p.get("abstract", "")[:1500]
        journal = p.get("journal", "")
        year = p.get("year", "")
        doi = p.get("doi", "")
        cited = p.get("cited_by", "0")
        
        prompt = (
            "Analyze this paper abstract for TCC (Topology-Centric Computing: NoC/chiplet/wafer-scale interconnect, network topology as computation) and iNEST (intelligent Neural Emergence SysTems: neuromorphic, criticality, SNN, emergence) research. Do not claim to have read the full text.\n\n"
            "Title: " + title + "\n"
            "Journal: " + journal + " | Year: " + year + " | Citations: " + cited + " | DOI: " + doi + "\n"
            "Abstract: " + abstract + "\n\n"
            'Output ONLY a JSON object (not an array):\n'
            '{"title_zh":"论文中文译名","tcc_value":"基于题目和摘要,分析对TCC(晶上互连/拓扑计算/Chiplet/NoC)的具体价值和方法论启发(3-5句中文,无则空)",'
            '"inest_value":"基于题目和摘要,分析对iNEST(神经形态/临界涌现/SNN/储备池)的具体价值和方法论启发(3-5句中文,无则空)",'
            '"inspiration":"基于题目和摘要,提出对TCC+iNEST交叉融合研究的可验证灵感(4-6句中文,包含具体可执行的研究建议)",'
            '"methodology":"论文核心方法论总结(2-3句)","key_finding":"最关键的一个发现或结论","relevance":1-5}\n'
            "No markdown, no explanation."
        )
        
        try:
            result = llm_call(prompt, system="TCC+iNEST research analyst. Output pure JSON only.", task_type="insight", max_tokens=1600)
            if result:
                result = result.strip()
                if result.startswith("```"):
                    result = re.sub(r"```\w*\n?", "", result).replace("```", "").strip()
                start = result.find("{")
                end = result.rfind("}")
                if start >= 0 and end > start:
                    result = result[start:end+1]
                result = re.sub(r",\s*}", "}", result)
                data = json.loads(result)
                data["id"] = i + 1
                data["analysis_basis"] = "abstract"
                data["source_path"] = p.get("rel_path", "")
                results.append(data)
                cache["items"][cache_key] = {"analysis": data, "cached_at": datetime.now().isoformat(timespec="seconds")}
                continue
        except Exception as e:
            pass
        
        # Fallback
        score, track = score_paper(p)
        if score >= 2:
            results.append({
                "id": i+1,
                "title_zh": title[:80],
                "tcc_value": "关键词匹配,需深入阅读" if track=="TCC" else "",
                "inest_value": "关键词匹配,需深入阅读" if track=="iNEST" else "",
                "inspiration": "建议阅读全文,评估方法论借鉴价值",
                "relevance": min(score, 5),
                "analysis_basis": "abstract",
                "source_path": p.get("rel_path", ""),
            })
            cache["items"][cache_key] = {"analysis": results[-1], "cached_at": datetime.now().isoformat(timespec="seconds")}
    
    save_analysis_cache(cache)
    return results, {"cache_hits": cache_hits, "llm_calls": len(results) - cache_hits}

def generate_daily_action(papers, analysis):
    lines = [f"# 每日行动洞察 — {TODAY_STR}", ""]
    lines.append(f"> 自动生成 | 入库 {len(papers)} 篇 | 基于题目与摘要的分析 Top {len(analysis)} 篇")
    lines.append("")
    
    if analysis:
        lines.append("## 今日高价值论文摘要分析")
        lines.append("")
        for item in analysis:
            rid = item.get("id", "?")
            title = item.get("title_zh", "")[:80]
            rel = item.get("relevance", "?")
            star = "⭐" * min(rel, 5)
            rel = str(item.get("source_path", "")).replace("\\", "/")
            paper_url = "http://127.0.0.1:8899/home/work/.openclaw/workspace/" + urllib.parse.quote(rel) if rel else ""
            if paper_url:
                lines.append(f"### {star} [{title}]({paper_url})")
            else:
                lines.append(f"### {star} {title}")
            lines.append("")
            tcc_v = item.get("tcc_value", "")
            inest_v = item.get("inest_value", "")
            insp = item.get("inspiration", "")
            if tcc_v:
                lines.append(f"**TCC 价值**: {tcc_v}")
                lines.append("")
            if inest_v:
                lines.append(f"**iNEST 价值**: {inest_v}")
                lines.append("")
            method = item.get("methodology", "")
            finding = item.get("key_finding", "")
            if method:
                lines.append(f"**方法**: {method}")
                lines.append("")
            if finding:
                lines.append(f"**关键发现**: {finding}")
                lines.append("")
            if insp:
                lines.append(f"**💡 灵感启迪**: {insp}")
                lines.append("")
            lines.append("---")
            lines.append("")
    
    lines.append("## 今日推荐行动")
    lines.append("")
    lines.append("1. **深入阅读** 上述高价值论文全文，提炼可借鉴的方法论与实验设计")
    lines.append("2. **CST 论文推进** — 修订 Section 4 仿真验证，目标 7月30日投 Engineering")
    lines.append("3. **TCC 范式论文** — P-Paradigm 修订，同步投 Engineering")
    lines.append("4. **专利修订** — TCC 架构与实现两项专利，7月30日前申报")
    lines.append("5. **研发路线迭代** — 将文献灵感写入研发看板，更新技术路线图")
    lines.append("")
    lines.append(f"*生成于 {TODAY.strftime('%Y-%m-%d %H:%M')}*")
    
    (MOC / "03_Daily_Action.md").write_text("\n".join(lines), encoding="utf-8")

def generate_research_insights(papers, analysis):
    lines = [f"# 研究洞察 — {TODAY_STR}", ""]
    lines.append(f"> 入库 {len(papers)} 篇 | 基于题目与摘要的分析 Top {len(analysis)} 篇")
    lines.append("")
    
    if analysis:
        lines.append("## 文献方法论启示")
        lines.append("")
        for item in analysis:
            insp = item.get("inspiration", "")
            title = item.get("title_zh", "")[:80]
            if insp:
                lines.append(f"- **{title}**: {insp}")
                lines.append("")
        
        lines.append("## 创新迭代建议")
        lines.append("")
        lines.append("1. 审视上述论文方法论，评估可融入 TCC 拓扑计算框架的技术路径")
        lines.append("2. 检查高阶网络/储备池方向进展对 iNEST SNN 架构设计的启发")
        lines.append("3. 关注 Nature Communications 等高分论文的实验验证范式，对齐自身论文论证强度")
        lines.append("4. 将可借鉴方法写入「研发看板 → 灵感」板块，驱动路线图迭代")
        lines.append("")
    
    lines.append(f"*生成于 {TODAY.strftime('%Y-%m-%d %H:%M')}*")
    (MOC / "02_Research_Insights.md").write_text("\n".join(lines), encoding="utf-8")

def generate_daily_focus(papers):
    tcc_p = [p for p in papers if score_paper(p)[1] == "TCC"]
    inest_p = [p for p in papers if score_paper(p)[1] == "iNEST"]
    
    lines = [f"## 今日焦点 — {TODAY_STR}", ""]
    lines.append("**并行主线 (7月30日前)**")
    lines.append("")
    lines.append("1. [论文] CST 智能涌现 — 修订 Section 4+5 → 投 Engineering")
    lines.append("2. [论文] TCC P-Paradigm 拓扑中心计算范式 → 投 Engineering")
    lines.append("3. [专利] TCC 架构 + 实现专利 — 申报")
    lines.append("4. [工程] CST 仿真实验 — SDI N=1024 相位扫描")
    lines.append("")
    
    if tcc_p or inest_p:
        lines.append(f"## 今日文献 ({len(tcc_p)} TCC + {len(inest_p)} iNEST)")
        lines.append("")
        for p in tcc_p[:3]:
            title = p.get("title","")[:70]
            lines.append(f"- [TCC] {title}")
        for p in inest_p[:3]:
            title = p.get("title","")[:70]
            lines.append(f"- [iNEST] {title}")
        lines.append("")
    
    lines.append(f"*生成于 {TODAY.strftime('%Y-%m-%d %H:%M')}*")
    (MOC / "04_Daily_Focus.md").write_text("\n".join(lines), encoding="utf-8")

if __name__ == "__main__":
    print(f"Daily Generator v2 — {TODAY_STR}")
    papers = get_today_papers()
    print(f"  Papers: {len(papers)}")
    
    # Deep LLM analysis of top papers
    print("  Running LLM analysis...")
    cache = load_analysis_cache()
    analysis, stats = deep_analyze_papers(papers, cache, top_n=8)
    print(f"  Analyzed: {len(analysis)} papers | LLM calls: {stats['llm_calls']} | cache hits: {stats['cache_hits']}")
    
    generate_daily_action(papers, analysis)
    print("  [OK] 03_Daily_Action.md")
    
    generate_research_insights(papers, analysis)
    print("  [OK] 02_Research_Insights.md")
    
    generate_daily_focus(papers)
    print("  [OK] 04_Daily_Focus.md")
    print("Done")
