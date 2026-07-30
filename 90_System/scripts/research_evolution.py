#!/usr/bin/env python3
"""
research_evolution.py — Self-evolution engine
Auto-validates hypotheses, iterates research directions based on new evidence
"""
import os, sys, json, re
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime
from collections import defaultdict

VAULT = Path(r"D:\Obsidian\vault")
WIKI = VAULT / "wiki"
META = VAULT / "99_Meta"

TODAY = datetime.now().strftime("%Y-%m-%d")

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# ============================================================
# Hypothesis validation
# ============================================================

def validate_hypotheses():
    """Check hypotheses against new evidence in wiki"""
    hyp_file = META / "hypothesis_registry.json"
    if not hyp_file.exists():
        return []
    
    try:
        data = json.loads(hyp_file.read_text(encoding='utf-8'))
        hypotheses = data.get("hypotheses", [])
    except:
        return []
    
    # Gather all wiki content as evidence corpus
    evidence = ""
    for d in [WIKI / "articles", WIKI / "concepts"]:
        if d.exists():
            for f in sorted(d.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)[:30]:
                evidence += f.read_text(encoding='utf-8')[:1000] + "\n\n"
    
    updates = []
    for h in hypotheses:
        h_id = h.get("id", "?")
        h_title = h.get("title", "")
        h_keywords = h.get("keywords", [])
        
        if not h_keywords:
            continue
        
        # Check if new evidence mentions hypothesis keywords
        hit_count = 0
        for kw in h_keywords:
            if kw.lower() in evidence.lower():
                hit_count += 1
        
        coverage = hit_count / len(h_keywords) if h_keywords else 0
        
        if coverage > 0.5 and h.get("status") == "pending":
            updates.append({
                "hypothesis": h_id,
                "title": h_title,
                "new_status": "supported",
                "evidence_coverage": f"{coverage:.0%}",
                "hits": hit_count,
                "action": f"Update hypothesis {h_id} status to 'supported' based on {hit_count}/{len(h_keywords)} keyword matches"
            })
        elif coverage > 0.2:
            updates.append({
                "hypothesis": h_id,
                "title": h_title,
                "new_status": "partial_evidence",
                "evidence_coverage": f"{coverage:.0%}",
                "hits": hit_count,
                "action": f"Hypothesis {h_id} has partial evidence ({hit_count}/{len(h_keywords)}). Collect more data."
            })
    
    return updates

# ============================================================
# Research direction iteration
# ============================================================

def iterate_directions():
    """Suggest research direction pivots based on knowledge evolution"""
    directions = []
    
    # Check wiki growth
    concepts_dir = WIKI / "concepts"
    articles_dir = WIKI / "articles"
    
    num_concepts = len(list(concepts_dir.glob("*.md"))) if concepts_dir.exists() else 0
    num_articles = len(list(articles_dir.glob("*.md"))) if articles_dir.exists() else 0
    
    # Check TCC vs iNEST balance
    tcc_count = 0
    inest_count = 0
    if concepts_dir.exists():
        for f in concepts_dir.glob("*.md"):
            content = f.read_text(encoding='utf-8')
            if "**Domain**: TCC" in content:
                tcc_count += 1
            elif "**Domain**: iNEST" in content:
                inest_count += 1
    
    # Direction 1: Balance domains
    if tcc_count > inest_count * 3:
        directions.append({
            "direction": "Deepen iNEST research",
            "rationale": f"TCC:{tcc_count} vs iNEST:{inest_count} — iNEST is under-explored",
            "priority": "HIGH"
        })
    elif inest_count > tcc_count * 3:
        directions.append({
            "direction": "Deepen TCC research",
            "rationale": f"iNEST:{inest_count} vs TCC:{tcc_count} — TCC is under-explored",
            "priority": "HIGH"
        })
    
    # Direction 2: Build bridges
    if tcc_count > 5 and inest_count > 5:
        cross_count = 0
        if concepts_dir.exists():
            for f in concepts_dir.glob("*.md"):
                if "**Domain**: Cross" in f.read_text(encoding='utf-8'):
                    cross_count += 1
        
        if cross_count < 5:
            directions.append({
                "direction": "Build TCC↔iNEST bridges",
                "rationale": f"Both domains are well-populated ({tcc_count}+{inest_count}) but only {cross_count} cross-domain concepts exist",
                "priority": "HIGH"
            })
    
    # Direction 3: Scale up
    if num_concepts < 20:
        directions.append({
            "direction": "Accelerate concept extraction",
            "rationale": f"Only {num_concepts} concepts extracted. Run wiki_compiler on more papers.",
            "priority": "MEDIUM"
        })
    
    return directions

# ============================================================
# Main
# ============================================================

def main():
    log("=== Research Evolution Engine ===")
    
    # 1. Hypothesis validation
    hyp_updates = validate_hypotheses()
    log(f"Hypothesis updates: {len(hyp_updates)}")
    for u in hyp_updates:
        print(f"  [{u['hypothesis']}] {u['action']}")
    
    # 2. Direction iteration
    directions = iterate_directions()
    log(f"Research directions: {len(directions)}")
    for d in directions:
        print(f"  [{d['priority']}] {d['direction']}: {d['rationale']}")
    
    # 3. Generate evolution report
    report = f"""# Research Evolution Report

**Generated**: {TODAY}

## Hypothesis Validation ({len(hyp_updates)} updates)
"""
    for u in hyp_updates:
        report += f"- **{u['hypothesis']}**: {u['action']}\n"
    
    if not hyp_updates:
        report += "*No new hypothesis validation results.*\n"
    
    report += f"""
## Research Direction Recommendations ({len(directions)})
"""
    for d in directions:
        report += f"- [{d['priority']}] **{d['direction']}**: {d['rationale']}\n"
    
    report += """
## Evolution Log
"""
    report += f"- {TODAY}: Research evolution check completed\n"
    
    (WIKI / "evolution_report.md").write_text(report, encoding='utf-8')
    log(f"Report: wiki/evolution_report.md")
    log("=== Done ===")

if __name__ == "__main__":
    main()
