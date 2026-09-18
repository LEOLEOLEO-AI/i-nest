#!/usr/bin/env python3
"""
cross_domain_insight.py — Cross-domain bridge discovery
Finds connections between TCC (wafer-scale interconnect) and iNEST (neuromorphic computing)
"""
import os, sys, json, re
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime
from collections import defaultdict

VAULT = Path(r"D:\Obsidian\vault")
WIKI = VAULT / "wiki"
TODAY = datetime.now().strftime("%Y-%m-%d")

# ============================================================
# Cross-domain bridge detection
# ============================================================

# Bridge patterns: terms that appear in BOTH TCC and iNEST contexts
BRIDGE_PATTERNS = {
    "WaferScale_Neuromorphic": {
        "tcc_terms": ["wafer", "晶圆", "wafer-scale"],
        "inest_terms": ["neuromorphic", "neuron", "SNN", "brain"],
        "insight": "Wafer-scale integration could enable massive-scale neuromorphic chips with millions of neurons on a single die."
    },
    "SDI_Plastic_Interconnect": {
        "tcc_terms": ["SDI", "interconnect", "software-defined"],
        "inest_terms": ["plasticity", "STDP", "adaptive", "可塑性"],
        "insight": "SDI's software-defined interconnect could implement plastic (reconfigurable) network topologies inspired by synaptic plasticity."
    },
    "Chiplet_Heterogeneous_Neuromorphic": {
        "tcc_terms": ["chiplet", "heterogeneous", "芯粒"],
        "inest_terms": ["neuromorphic", "忆阻", "memristor", "crossbar"],
        "insight": "Chiplet-based heterogeneous integration enables combining CMOS logic with memristor crossbar arrays for neuromorphic acceleration."
    },
    "NoC_Spiking_Routing": {
        "tcc_terms": ["NoC", "network-on-chip", "routing", "router"],
        "inest_terms": ["spiking", "spike", "脉冲", "event-driven"],
        "insight": "NoC routing algorithms could be redesigned for event-driven spike packet delivery, reducing latency by orders of magnitude."
    },
    "Topology_Brain_Connectome": {
        "tcc_terms": ["topology", "topological", "拓扑"],
        "inest_terms": ["connectome", "brain atlas", "脑图谱", "cortical"],
        "insight": "Brain connectome topology patterns can inspire optimal NoC topologies for wafer-scale AI chips."
    },
    "3DIC_Neural_Stacking": {
        "tcc_terms": ["3D-IC", "3D integration", "TSV", "stacking"],
        "inest_terms": ["cortical column", "laminar", "layer", "皮层柱"],
        "insight": "3D-IC stacking mimics cortical columnar architecture, enabling dense neural processing layers."
    },
    "Memory_Wall_Neuromorphic_Solution": {
        "tcc_terms": ["memory wall", "memory bandwidth", "带宽瓶颈"],
        "inest_terms": ["in-memory computing", "compute-in-memory", "存内计算"],
        "insight": "Neuromorphic in-memory computing is a potential solution to the wafer-scale memory wall problem."
    }
}

# ============================================================
# Keyword-based cross-domain discovery
# ============================================================

def _term_specificity(term, *doc_sets):
    """术语特异性（逆文档频率式）：越少见的词越有区分度。

    背景（2026-09-18 修复）：旧实现用 `matched_tcc[:5]` 取匹配概念，
    而 matched_tcc 是按 concepts 目录的**文件顺序（≈字母序）**累积的，
    于是每条桥反复列出同样的字母序靠前概念
    （[[1024_Card_SuperNode]] / [[2_5D_3D_HeterogeneousIntegration]] /
     [[2_5D_Interposer]]），"Strength" 也只是原始命中计数——
    像 "topology"/"interconnect" 这种高频词能刷出 1212 的假强度。
    这里改为按术语特异性加权排序，并按文档频率归一。
    """
    docs = [d for ds in doc_sets for d in ds]
    if not docs:
        return 1.0
    n = sum(1 for t in docs if term.lower() in t.lower())
    return 1.0 / (1.0 + n)


def scan_concepts_for_bridges():
    """扫描 wiki 概念，按**术语特异性**排序找出真正的跨域桥。

    与旧版的区别：
      * 匹配概念按特异性得分排序，不再按目录字母序取前几个；
      * strength 保留（= 两侧较小命中数）以兼容下游，但另给出
        coverage（占本域概念比例）与 top 概念得分，使强度可复核；
      * 输出 matched 概念时带上得分，便于人工判断是否真有相关性。
    """
    concepts_dir = WIKI / "concepts"
    if not concepts_dir.exists():
        return []

    tcc_texts = {}
    inest_texts = {}

    for f in concepts_dir.glob("*.md"):
        content = f.read_text(encoding='utf-8')
        if "**Domain**: TCC" in content:
            tcc_texts[f.stem] = content
        elif "**Domain**: iNEST" in content:
            inest_texts[f.stem] = content

    bridged = []
    for bridge_name, patterns in BRIDGE_PATTERNS.items():
        def _score_side(texts):
            scored = []
            for name, text in texts.items():
                low = text.lower()
                hits = [t for t in patterns.get("tcc_terms", []) +
                        patterns.get("inest_terms", []) if t.lower() in low]
                # 只用本侧的词表计算（TCC 侧用 tcc_terms，iNEST 侧用 inest_terms）
                hits = [t for t in hits if t in
                        (patterns.get("tcc_terms", []) if texts is tcc_texts
                         else patterns.get("inest_terms", []))]
                if hits:
                    s = sum(_term_specificity(t, tcc_texts, inest_texts) for t in hits)
                    scored.append((round(s, 6), name, hits))
            scored.sort(key=lambda x: -x[0])
            return scored

        tcc_scored = _score_side(tcc_texts)
        inest_scored = _score_side(inest_texts)

        if tcc_scored and inest_scored:
            bridged.append({
                "bridge": bridge_name,
                "insight": patterns["insight"],
                "tcc_concepts": [n for _, n, _ in tcc_scored[:5]],
                "inest_concepts": [n for _, n, _ in inest_scored[:5]],
                "tcc_top_scores": [s for s, _, _ in tcc_scored[:5]],
                "inest_top_scores": [s for s, _, _ in inest_scored[:5]],
                "tcc_matched": len(tcc_scored),
                "inest_matched": len(inest_scored),
                "strength": min(len(tcc_scored), len(inest_scored)),
                "coverage": round(min(
                    len(tcc_scored) / max(len(tcc_texts), 1),
                    len(inest_scored) / max(len(inest_texts), 1)), 4),
                "ranking": "term-specificity-weighted (非字母序)",
            })

    bridged.sort(key=lambda x: x["strength"], reverse=True)
    return bridged

# ============================================================
# Generate insights from paper summaries
# ============================================================

def scan_articles_for_insights():
    """Look for cross-domain mentions in wiki articles"""
    articles_dir = WIKI / "articles"
    if not articles_dir.exists():
        return []
    
    insights = []
    for f in sorted(articles_dir.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)[:20]:
        content = f.read_text(encoding='utf-8')
        
        # Count domain keyword overlap
        tcc_kw = sum(1 for kw in ["SDI", "TCC", "wafer", "chiplet", "interconnect", "NoC"] if kw.lower() in content.lower())
        inest_kw = sum(1 for kw in ["iNEST", "SNN", "spiking", "STDP", "neuromorphic"] if kw.lower() in content.lower())
        
        if tcc_kw >= 2 and inest_kw >= 2:
            insights.append({
                "source": f.stem,
                "tcc_keywords": tcc_kw,
                "inest_keywords": inest_kw,
                "relevance": tcc_kw + inest_kw
            })
    
    return sorted(insights, key=lambda x: x["relevance"], reverse=True)

# ============================================================
# Main
# ============================================================

def main():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] === Cross-Domain Insight Engine ===")
    
    # 1. Pattern-based bridge detection
    bridges = scan_concepts_for_bridges()
    print(f"\nDetected {len(bridges)} cross-domain bridges:")
    for b in bridges:
        print(f"  [{b['strength']}] {b['bridge']}")
        print(f"       TCC: {', '.join(b['tcc_concepts'][:3])}")
        print(f"       iNEST: {', '.join(b['inest_concepts'][:3])}")
    
    # 2. Article-based insight discovery
    insights = scan_articles_for_insights()
    print(f"\nCross-domain articles: {len(insights)}")
    for ins in insights[:5]:
        print(f"  {ins['source']} (TCC:{ins['tcc_keywords']} iNEST:{ins['inest_keywords']})")
    
    # 3. Generate report
    report = f"""# Cross-Domain Insights

**Generated**: {TODAY}

> **口径说明（2026-09-18 修订）**：以下每条桥的匹配概念按**术语特异性**
> （逆文档频率式）排序，不再按概念目录的字母序取前几个——旧实现因此让
> 每条桥都反复列出相同的字母序靠前概念。
> `Strength` = 两侧匹配概念数的较小者，是**语料频次量级**而非相关性度量
> （高频词如 topology/interconnect 会把它推高），故同时给出 `Coverage`
> （占本域概念比例）与 top 概念的特异性得分，供复核。

## Active Bridges ({len(bridges)})
"""
    for b in bridges:
        report += f"""
### {b['bridge']} (Strength: {b['strength']} · Coverage: {b.get('coverage', 0):.4f})
{b['insight']}
- 匹配规模：TCC {b.get('tcc_matched','?')} 个 / iNEST {b.get('inest_matched','?')} 个
- TCC concepts（按特异性）: {', '.join(f'[[{c}]]' for c in b['tcc_concepts'][:3])}
- iNEST concepts（按特异性）: {', '.join(f'[[{c}]]' for c in b['inest_concepts'][:3])}
- 排序依据: {b.get('ranking','')}
"""
    
    report += f"""
## Cross-Domain Papers ({len(insights)})
"""
    for ins in insights:
        report += f"- {ins['source']} (cross-score: {ins['relevance']})\n"
    
    report += """
## Suggested Research Directions
"""
    for b in bridges[:3]:
        report += f"- **{b['bridge']}**: {b['insight']}\n"
    
    output_path = WIKI / "cross_domain_insights.md"
    output_path.write_text(report, encoding='utf-8')
    print(f"\nReport: {output_path}")

if __name__ == "__main__":
    main()
