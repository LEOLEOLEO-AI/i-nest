#!/usr/bin/env python3
"""
task_recommender.py — Research task recommendation engine
Analyzes wiki state, knowledge gaps, hypotheses, and generates prioritized task list
"""
import os, sys, json, re
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime
from collections import defaultdict

VAULT = Path(r"D:\Obsidian\vault")
try:
    from dotenv import load_dotenv
    load_dotenv(VAULT / ".env", override=True)
except Exception:
    pass

WIKI = VAULT / "wiki"
STATE_DIR = VAULT / "state"
META = VAULT / "99_Meta"

TODAY = datetime.now().strftime("%Y-%m-%d")

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# ============================================================
# Knowledge Gap Analysis
# ============================================================

def analyze_gaps():
    """Find knowledge gaps in the wiki"""
    gaps = []
    
    # Check concept count per domain
    tcc_count = 0
    inest_count = 0
    concepts_dir = WIKI / "concepts"
    if concepts_dir.exists():
        for f in concepts_dir.glob("*.md"):
            content = f.read_text(encoding='utf-8')
            if "**Domain**: TCC" in content:
                tcc_count += 1
            elif "**Domain**: iNEST" in content:
                inest_count += 1
    
    if tcc_count < 15:
        gaps.append({
            "type": "domain_coverage",
            "domain": "TCC",
            "gap": f"TCC domain has only {tcc_count} concepts. Target: 30+",
            "priority": "HIGH",
            "action": "Process more TCC papers through raw/tcc/"
        })
    
    if inest_count < 15:
        gaps.append({
            "type": "domain_coverage",
            "domain": "iNEST",
            "gap": f"iNEST domain has only {inest_count} concepts. Target: 30+",
            "priority": "HIGH",
            "action": "Process more iNEST papers through raw/inest/"
        })
    
    # Check cross-domain bridges
    cross_count = 0
    if concepts_dir.exists():
        for f in concepts_dir.glob("*.md"):
            content = f.read_text(encoding='utf-8')
            if "**Domain**: Cross" in content:
                cross_count += 1
    
    if cross_count < 3 and tcc_count > 5 and inest_count > 5:
        gaps.append({
            "type": "cross_domain",
            "gap": f"Only {cross_count} cross-domain concepts. TCC↔iNEST bridges needed.",
            "priority": "MEDIUM",
            "action": "Identify wafer-scale neuromorphic, chiplet brain-like computing concepts"
        })
    
    # Check for orphan concepts
    if concepts_dir.exists():
        all_names = {f.stem for f in concepts_dir.glob("*.md")}
        linked = set()
        for f in concepts_dir.glob("*.md"):
            content = f.read_text(encoding='utf-8')
            for name in all_names:
                if name != f.stem and name in content:
                    linked.add(name)
        orphans = sorted(all_names - linked)
        if len(orphans) > 5:
            gaps.append({
                "type": "orphan_concepts",
                "gap": f"{len(orphans)} orphan concepts with no incoming links",
                "priority": "LOW",
                "action": f"Link these concepts: {', '.join(orphans[:10])}"
            })
    
    return gaps

# ============================================================
# Hypothesis-driven recommendations
# ============================================================

def analyze_hypotheses():
    """Read hypothesis registry and suggest next steps"""
    hyp_file = META / "hypothesis_registry.json"
    if not hyp_file.exists():
        return []
    
    try:
        data = json.loads(hyp_file.read_text(encoding='utf-8'))
        hypotheses = data.get("hypotheses", [])
    except:
        return []
    
    recs = []
    for h in hypotheses:
        status = h.get("status", "unknown")
        if status in ["pending", "proposed"]:
            recs.append({
                "type": "hypothesis_test",
                "hypothesis": h.get("id", "?") + ": " + h.get("title", "")[:60],
                "priority": "HIGH" if status == "pending" else "MEDIUM",
                "action": f"Design experiment to test hypothesis {h.get('id', '?')}"
            })
    
    return recs

# ============================================================
# Evolution queue analysis
# ============================================================

def analyze_evolution_queue(limit=8):
    """读取进化队列中的 **pending** 条目，按真实优先级排序后返回 top-N。

    修正三个已实测缺陷 (2026-09-18)：
      1. 旧实现 `for item in items[:10]` 固定取数组**最旧的 10 条**，与优先级、
         状态都无关 —— 于是每天都重播同一批 2026-07-19 的条目（"同一批建议
         永远重播"的直接原因之一）。
      2. 旧实现 `str(item)[:100]` 把 dict 直接字符串化，报告里因此出现被截断的
         Python repr，形如 `{'id': 'EV-2026-07-19-001', 'priority': 'high', ...`。
      3. 旧实现把每条硬编码为 `"priority": "MEDIUM"`，**丢掉条目自身的真实
         priority**（输出的方括号标签与条目内文自相矛盾）。
    """
    evo_file = META / "evolution_queue.json"
    if not evo_file.exists():
        return []

    try:
        data = json.loads(evo_file.read_text(encoding='utf-8'))
        items = data.get("queue", data.get("items", []))
    except Exception:
        return []

    prio_rank = {"high": 0, "medium": 1, "low": 2}
    pend = []
    seen = set()
    for item in items:
        if not isinstance(item, dict):
            continue
        if str(item.get("status", "pending")).lower() not in ("pending", "open", ""):
            continue
        title = str(item.get("title") or item.get("summary") or "").strip()
        etype = str(item.get("type") or "general")
        key = (etype, title)
        if not title or key in seen:      # 同类同题只报一次
            continue
        seen.add(key)
        pend.append(item)

    pend.sort(key=lambda i: (prio_rank.get(str(i.get("priority", "medium")).lower(), 1),
                             str(i.get("first_seen") or i.get("created") or "")))

    recs = []
    for item in pend[:limit]:
        etype = str(item.get("type") or "general")
        title = str(item.get("title") or item.get("summary") or "").strip()
        occ = item.get("occurrences")
        detail = str(item.get("detail") or "").strip()
        recs.append({
            "type": "evolution_item",
            "item": f"[{etype}] {title}" + (f" (出现 {occ} 次)" if occ else ""),
            "priority": str(item.get("priority", "medium")).upper(),
            "action": detail or "Process evolution queue item",
        })
    return recs

# ============================================================
# Recent research activity analysis
# ============================================================

def analyze_recent_activity():
    """Check what's been recently active"""
    recs = []
    
    # Check 50_Output for recent papers
    output_dir = VAULT / "50_Output"
    if output_dir.exists():
        recent = sorted(output_dir.rglob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)[:5]
        for f in recent:
            days_ago = (datetime.now() - datetime.fromtimestamp(f.stat().st_mtime)).days
            if days_ago < 7:
                recs.append({
                    "type": "recent_output",
                    "item": f"Recent: {f.stem[:60]} ({days_ago}d ago)",
                    "priority": "LOW",
                    "action": "Review and incorporate insights into wiki"
                })
    
    return recs

# ============================================================
# Main: Generate task recommendations
# ============================================================

def main():
    log("=== Task Recommender ===")
    
    all_recommendations = []
    
    # 1. Knowledge gap analysis
    gaps = analyze_gaps()
    all_recommendations.extend(gaps)
    log(f"Knowledge gaps: {len(gaps)}")
    
    # 2. Hypothesis analysis
    hyp_recs = analyze_hypotheses()
    all_recommendations.extend(hyp_recs)
    log(f"Hypothesis recommendations: {len(hyp_recs)}")
    
    # 3. Evolution queue
    evo_recs = analyze_evolution_queue()
    all_recommendations.extend(evo_recs)
    log(f"Evolution queue items: {len(evo_recs)}")
    
    # 4. Recent activity
    activity_recs = analyze_recent_activity()
    all_recommendations.extend(activity_recs)
    log(f"Activity recommendations: {len(activity_recs)}")
    
    # Sort by priority
    priority_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    all_recommendations.sort(key=lambda x: priority_order.get(x["priority"], 3))
    
    # Generate report
    report = f"""# Research Task Recommendations

**Generated**: {TODAY}
**Total**: {len(all_recommendations)} recommendations

"""
    for i, rec in enumerate(all_recommendations, 1):
        report += f"""### {i}. [{rec['priority']}] {rec['type'].replace('_', ' ').title()}
{rec.get('gap', '')}{rec.get('item', '')}{rec.get('hypothesis', '')}
**Action**: {rec['action']}

"""

    output_path = WIKI / "task_recommendations.md"
    output_path.write_text(report, encoding='utf-8')
    log(f"Report written to {output_path}")
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"RECOMMENDATIONS SUMMARY ({len(all_recommendations)} items)")
    print(f"{'='*60}")
    for rec in all_recommendations:
        print(f"  [{rec['priority']:6s}] {rec['action'][:70]}")
    
    log("=== Done ===")

if __name__ == "__main__":
    main()
