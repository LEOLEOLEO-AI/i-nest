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

def scan_concepts_for_bridges():
    """Scan wiki concepts to find actual cross-domain bridges"""
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
        tcc_hits = 0
        inest_hits = 0
        matched_tcc = []
        matched_inest = []
        
        for name, text in tcc_texts.items():
            if any(t.lower() in text.lower() for t in patterns["tcc_terms"]):
                tcc_hits += 1
                matched_tcc.append(name)
        
        for name, text in inest_texts.items():
            if any(t.lower() in text.lower() for t in patterns["inest_terms"]):
                inest_hits += 1
                matched_inest.append(name)
        
        if tcc_hits > 0 and inest_hits > 0:
            bridged.append({
                "bridge": bridge_name,
                "insight": patterns["insight"],
                "tcc_concepts": matched_tcc[:5],
                "inest_concepts": matched_inest[:5],
                "strength": min(tcc_hits, inest_hits)
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

## Active Bridges ({len(bridges)})
"""
    for b in bridges:
        report += f"""
### {b['bridge']} (Strength: {b['strength']})
{b['insight']}
- TCC concepts: {', '.join(f'[[{c}]]' for c in b['tcc_concepts'][:3])}
- iNEST concepts: {', '.join(f'[[{c}]]' for c in b['inest_concepts'][:3])}
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
