#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Knowledge Evolution Engine v1.0"""
import os, sys, json, re, time, hashlib
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict, Counter

sys.path.insert(0, r"D:\Obsidian\scripts")
from llm_router import llm_call

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
SCRIPTS = VAULT / "90_System" / "scripts"
OUTPUT_DIR = VAULT / "99_Meta"
TODAY = datetime.now().strftime("%Y-%m-%d")
WEEK_AGO = (datetime.now() - timedelta(days=7)).timestamp()
TCC_KW = [
    "chiplet", "noc", "network.on.chip", "wafer.scale", "topology",
    "routing", "interconnect", "memristor", "dark.silicon", "vlsi",
    "crossbar", "signal.integrity", "semiconductor", "manycore",
    "placement", "3d.integration", "tsv", "photonic", "die.to.die",
    "serdes", "packaging", "thermal", "power.delivery", "d2d"
]

INEST_KW = [
    "neuron", "spike", "avalanche", "critical", "emergence",
    "free.energy", "brain", "neuromorphic", "self.organiz",
    "snn", "reservoir", "liquid.state", "complex.system",
    "network.structure", "phase.transition", "bifurcation",
    "attractor", "synaptic", "plasticity", "stdp", "oscillation"
]

ACTIVE_PAPERS = {
    "P-Paradigm": {"title": "Topology-Centric Computing Paradigm", "target": "Nature Electronics", "status": "framework", "track": "TCC"},
    "P-Mapping": {"title": "Physical Topology Mapping", "target": "IEEE TPDS", "status": "drafting", "track": "TCC"},
    "B0-Engineering": {"title": "Baseline Engineering Edition", "target": "TBD", "status": "v7 SUBMISSION", "track": "TCC"},
    "CST-Emergence": {"title": "CST Intelligent Emergence", "target": "TBD", "status": "V25 FINAL", "track": "iNEST"},
    "iNEST-Core": {"title": "iNEST Core Architecture", "target": "TBD", "status": "framework", "track": "iNEST"},
    "Liquid-Computing": {"title": "Liquid Computing Chemistry", "target": "TBD", "status": "framework", "track": "iNEST"}
}

SCAN_DIRS = [
    "00_Inbox", "10_Knowledge", "10_Library", "20_Ideas",
    "03_Topics", "30_TCC", "40_iNEST",
]

HEALTH_EXCLUDE = [
    ".obsidian", ".claude", ".claudian", ".trash", ".venv",
    ".neural_db", ".neural_memory", ".openclaw", ".tasks",
    "__pycache__", "node_modules", "scripts", "state",
    "99_Attachments", "99_Templates", "99_Journal",
    "collective_comm_naas", "fpga", "knowledge_graph",
    "results", "dashboard", "_archive", "_archive_02_Zettelkasten",
    "logs", "90_System"
]

# ============================================================
# 1. SCAN: Find new/modified notes from the past week
# ============================================================

def scan_new_notes():
    """Scan vault for notes modified/created in the past 7 days."""
    new_notes = []
    all_notes_count = 0

    for scan_dir in SCAN_DIRS:
        dir_path = VAULT / scan_dir
        if not dir_path.exists():
            continue
        for md_file in dir_path.rglob("*.md"):
            all_notes_count += 1
            try:
                stat = md_file.stat()
                if stat.st_mtime >= WEEK_AGO:
                    text = md_file.read_text(encoding="utf-8", errors="ignore")
                    rel_path = str(md_file.relative_to(VAULT))
                    new_notes.append({
                        "path": str(md_file),
                        "rel_path": rel_path,
                        "name": md_file.stem,
                        "text": text,
                        "size": len(text),
                        "mtime": stat.st_mtime,
                        "mtime_str": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
                        "folder": scan_dir
                    })
            except Exception as e:
                print(f"  [WARN] Cannot read {md_file}: {e}")

    new_notes.sort(key=lambda x: x["mtime"], reverse=True)
    return new_notes, all_notes_count


# ============================================================
# 2. CLASSIFY: Determine TCC/iNEST relevance
# ============================================================

def keyword_classify(note):
    """Fast keyword-based pre-classification."""
    tl = (note["name"] + " " + note["text"][:500]).lower()
    tcc_score = sum(1 for kw in TCC_KW if re.search(kw, tl))
    inest_score = sum(1 for kw in INEST_KW if re.search(kw, tl))

    if tcc_score > inest_score and tcc_score >= 2:
        return "TCC", tcc_score
    elif inest_score > tcc_score and inest_score >= 2:
        return "iNEST", inest_score
    elif tcc_score >= 1:
        return "TCC-weak", tcc_score
    elif inest_score >= 1:
        return "iNEST-weak", inest_score
    else:
        return "General", 0


def llm_deep_classify(notes, max_notes=25):
    """Use LLM to deeply classify top notes and extract value insights."""
    if not notes:
        return []

    candidates = sorted(notes, key=lambda x: x["size"], reverse=True)[:max_notes]

    note_list = []
    for i, n in enumerate(candidates):
        excerpt = n["text"][:600].replace("\n", " ").strip()
        note_list.append(
            f"[{i}] {n['name'][:80]} | folder: {n['folder']} | "
            f"date: {n['mtime_str']}\n    Excerpt: {excerpt}"
        )

    prompt = f"""You are analyzing {len(candidates)} new research notes imported into a knowledge base
for TCC (Topology-Centric Computing: chiplet, NoC, wafer-scale interconnect)
and iNEST (intelligent Neural Emergence SysTems: neuromorphic, criticality, emergence).

For each note, evaluate its relevance and generate a structured insight.
Output ONLY valid JSON array. Do NOT use markdown fences.

Notes:
{chr(10).join(note_list)}

Return JSON array:
[
  {{
    "note_index": 0,
    "track": "TCC" | "iNEST" | "Both" | "General",
    "relevance": "high" | "medium" | "low",
    "value_summary_cn": "one sentence in Chinese summarizing value to our research",
    "inspiration": "concrete suggestion: what this inspires for our papers/patents/projects",
    "suggested_action": "add_to_paper" | "explore_concept" | "archive_reference" | "patent_idea" | "project_planning" | "knowledge_only",
    "target_paper": "P-Paradigm" | "P-Mapping" | "B0-Engineering" | "CST-Emergence" | "iNEST-Core" | "Liquid-Computing" | null
  }}
]"""

    try:
        result = llm_call(
            prompt,
            system="You are a senior research scientist analyzing knowledge for TCC+iNEST projects. Output pure JSON only, no markdown, no explanations.",
            task_type="evolution",
            max_tokens=4000,
            temperature=0.3
        )
        if not result:
            print("  [LLM WARN] Empty response, retrying once...")
            import time; time.sleep(3)
            result = llm_call(prompt, system="You are a senior research scientist analyzing knowledge for TCC+iNEST projects. Output pure JSON only, no markdown, no explanations.", task_type="evolution", max_tokens=4000, temperature=0.3)
        if not result:
            return []
        result = result.strip()
        if result.startswith("```"):
            result = re.sub(r"^```\w*\n?", "", result)
            result = re.sub(r"\n```$", "", result)
        # Clean common LLM JSON errors
        result = result.replace("\n", "\\n")
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            m = re.search(r"\[.*\]", result, re.DOTALL)
            if m:
                return json.loads(m.group())
            raise
        except json.JSONDecodeError:
            # Try extracting just the JSON array
            m = re.search(r"\[.*\]", result, re.DOTALL)
            if m:
                return json.loads(m.group())
            raise
    except Exception as e:
        print(f"  [LLM ERROR] Deep classify failed: {e}")
        return []

# ============================================================
# 3. CROSS-REFERENCE: Map insights to active papers/projects
# ============================================================

def cross_reference(insights):
    """Map classified insights to active papers and generate suggestions."""
    paper_suggestions = defaultdict(list)
    patent_ideas = []
    project_ideas = []
    concept_explore = []

    for item in insights:
        target = item.get("target_paper")
        action = item.get("suggested_action", "knowledge_only")
        inspiration = item.get("inspiration", "")
        note_idx = item.get("note_index", -1)

        if target and target in ACTIVE_PAPERS:
            paper_suggestions[target].append({
                "inspiration": inspiration,
                "relevance": item.get("relevance", "medium"),
                "note_index": note_idx
            })

        if action == "patent_idea":
            patent_ideas.append({
                "inspiration": inspiration,
                "track": item.get("track", "General"),
                "note_index": note_idx
            })

        if action == "project_planning":
            project_ideas.append({
                "inspiration": inspiration,
                "track": item.get("track", "General"),
                "note_index": note_idx
            })

        if action == "explore_concept":
            concept_explore.append({
                "inspiration": inspiration,
                "track": item.get("track", "General"),
                "note_index": note_idx
            })

    return {
        "paper_suggestions": dict(paper_suggestions),
        "patent_ideas": patent_ideas,
        "project_ideas": project_ideas,
        "concept_explore": concept_explore
    }


# ============================================================
# 4. VAULT HEALTH DIAGNOSTICS
# ============================================================

def run_health_diagnostics():
    """Run comprehensive vault health check."""
    issues = {}
    stats = {}

    all_notes = {}
    all_names = set()
    incoming = defaultdict(list)

    for md_file in VAULT.rglob("*.md"):
        rel = str(md_file.relative_to(VAULT))
        parts = Path(rel).parts
        if any(p in HEALTH_EXCLUDE or p.startswith(".") for p in parts):
            continue
        try:
            text = md_file.read_text(encoding="utf-8", errors="ignore")
            links = re.findall(r"\[\[([^\]|#]+)", text)
            name = md_file.stem
            all_notes[rel] = {
                "path": md_file,
                "name": name,
                "text": text,
                "links": links,
                "size": len(text),
                "mtime": md_file.stat().st_mtime
            }
            all_names.add(name)
            for link in links:
                incoming[link].append(rel)
        except Exception:
            pass

    stats["total_notes"] = len(all_notes)
    stats["total_size_mb"] = round(sum(d["size"] for d in all_notes.values()) / (1024 * 1024), 2)

    # Orphans
    orphans = []
    for rel, data in all_notes.items():
        has_out = len(data["links"]) > 0
        has_in = len(incoming.get(data["name"], [])) > 0
        if not has_out and not has_in and data["size"] > 50:
            orphans.append(rel)
    stats["orphans"] = len(orphans)
    if orphans:
        issues["orphans"] = orphans[:20]

    # Broken links
    broken = []
    for rel, data in all_notes.items():
        for link in data["links"]:
            link_name = link.split("|")[0].split("#")[0].strip()
            if link_name not in all_names:
                broken.append(f"{rel} -> [[{link}]]")
    stats["broken_links"] = len(broken)
    if broken:
        issues["broken_links"] = broken[:15]

    # Tiny notes
    tiny = [rel for rel, d in all_notes.items() if d["size"] < 60]
    stats["tiny_notes"] = len(tiny)
    if tiny:
        issues["tiny_notes"] = tiny[:15]

    # Duplicates
    hashes = defaultdict(list)
    for rel, data in all_notes.items():
        h = hashlib.md5(data["text"][:2000].encode()).hexdigest()
        hashes[h].append(rel)
    dups = {k: v for k, v in hashes.items() if len(v) > 1}
    stats["duplicate_groups"] = len(dups)
    if dups:
        issues["duplicates"] = list(dups.values())[:10]

    # Stale notes
    six_months_ago = (datetime.now() - timedelta(days=180)).timestamp()
    stale = []
    for rel, data in all_notes.items():
        if data["mtime"] < six_months_ago and len(data["links"]) == 0 and data["size"] < 500:
            stale.append(rel)
    stats["stale_notes"] = len(stale)
    if stale:
        issues["stale_notes"] = stale[:20]

    # Folder distribution
    folder_sizes = defaultdict(lambda: {"count": 0, "size": 0})
    for rel, data in all_notes.items():
        folder = Path(rel).parts[0] if Path(rel).parts else "root"
        folder_sizes[folder]["count"] += 1
        folder_sizes[folder]["size"] += data["size"]
    stats["folder_distribution"] = {
        k: {"notes": v["count"], "size_kb": round(v["size"] / 1024, 1)}
        for k, v in sorted(folder_sizes.items())
    }

    return stats, issues

# ============================================================
# 5. GENERATE REPORT
# ============================================================

def generate_report(new_notes, llm_insights, cross_ref, health_stats, health_issues):
    """Generate a comprehensive markdown report."""
    lines = []
    lines.append("---")
    lines.append("title: \"知识库周度自进化报告\"")
    lines.append(f"date: {TODAY}")
    lines.append("type: auto-generated")
    lines.append("purpose: \"知识库自进化：新知识价值评估、论文/专利/项目灵感建议、健康诊断\"")
    lines.append("---")
    lines.append("")
    lines.append(f"# 知识库周度自进化报告 - {TODAY}")
    lines.append("")
    lines.append(f"> 统计周期: {(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')} -> {TODAY}")
    lines.append(f"> 全库笔记总数: {health_stats.get('total_notes', '?')} 篇")
    lines.append(f"> 本周新增/更新: {len(new_notes)} 篇")
    lines.append("")

    # Section 1: New Knowledge Overview
    lines.append("---")
    lines.append("")
    lines.append("## 一、本周新知识概览")
    lines.append("")

    if not new_notes:
        lines.append("> 本周无新增或修改的笔记。建议检查管线运行状态。")
    else:
        track_counts = Counter()
        for n in new_notes:
            track, score = keyword_classify(n)
            track_counts[track] += 1

        lines.append(f"| 轨道 | 数量 |")
        lines.append(f"|------|------|")
        for track in ["TCC", "iNEST", "TCC-weak", "iNEST-weak", "General"]:
            if track_counts.get(track, 0) > 0:
                lines.append(f"| {track} | {track_counts[track]} |")
        lines.append("")

        lines.append("### 新增笔记列表")
        lines.append("")
        lines.append("| # | 笔记名称 | 文件夹 | 修改时间 | 大小 | 轨道 |")
        lines.append("|---|---------|--------|---------|------|------|")
        for i, n in enumerate(new_notes[:50], 1):
            track, _ = keyword_classify(n)
            name_display = n["name"][:60]
            if len(n["name"]) > 60:
                name_display += "..."
            lines.append(
                f"| {i} | {name_display} | {n['folder']} | "
                f"{n['mtime_str']} | {n['size']}B | {track} |"
            )
        if len(new_notes) > 50:
            lines.append(f"| ... | ... 还有 {len(new_notes) - 50} 篇 | ... | ... | ... | ... |")
        lines.append("")

    # Section 2: LLM Deep Insights
    lines.append("---")
    lines.append("")
    lines.append("## 二、LLM 深度价值分析")
    lines.append("")

    if not llm_insights:
        lines.append("> LLM 深度分析未能完成，请检查 API 配置。")
    else:
        for item in llm_insights:
            track = item.get("track", "?")
            relevance = item.get("relevance", "?")
            summary = item.get("value_summary_cn", "")
            inspiration = item.get("inspiration", "")
            target = item.get("target_paper", "")
            action = item.get("suggested_action", "")

            lines.append(f"### [{track}] {relevance.upper()} 相关度")
            lines.append(f"- **价值摘要**: {summary}")
            if inspiration:
                lines.append(f"- **灵感建议**: {inspiration}")
            if target:
                paper_info = ACTIVE_PAPERS.get(target, {})
                lines.append(f"- **关联论文**: `{target}` - {paper_info.get('title', '')}")
            lines.append(f"- **建议动作**: `{action}`")
            lines.append("")

    # Section 3: Paper/Patent/Project Suggestions
    lines.append("---")
    lines.append("")
    lines.append("## 三、论文/专利/项目策划灵感建议")
    lines.append("")

    paper_sugs = cross_ref.get("paper_suggestions", {})
    if paper_sugs:
        lines.append("### 论文增量建议")
        lines.append("")
        for paper_id, suggestions in paper_sugs.items():
            paper = ACTIVE_PAPERS.get(paper_id, {})
            lines.append(f"#### {paper_id}: {paper.get('title', '')}")
            lines.append(f"- 目标期刊: {paper.get('target', 'TBD')} | 状态: {paper.get('status', '?')}")
            for s in suggestions:
                lines.append(f"  - {s['inspiration']} (相关度: {s['relevance']})")
            lines.append("")
    else:
        lines.append("> 本周无直接论文相关的灵感建议。")
        lines.append("")

    patent_ideas = cross_ref.get("patent_ideas", [])
    if patent_ideas:
        lines.append("### 专利灵感")
        lines.append("")
        for p in patent_ideas:
            lines.append(f"- [{p['track']}] {p['inspiration']}")
        lines.append("")

    project_ideas = cross_ref.get("project_ideas", [])
    if project_ideas:
        lines.append("### 项目策划建议")
        lines.append("")
        for p in project_ideas:
            lines.append(f"- [{p['track']}] {p['inspiration']}")
        lines.append("")

    concept_explore = cross_ref.get("concept_explore", [])
    if concept_explore:
        lines.append("### 待探索概念")
        lines.append("")
        for c in concept_explore:
            lines.append(f"- [{c['track']}] {c['inspiration']}")
        lines.append("")

    # Section 4: Vault Health
    lines.append("---")
    lines.append("")
    lines.append("## 四、知识库健康诊断")
    lines.append("")

    lines.append("### 健康指标")
    lines.append("")
    lines.append("| 指标 | 数值 | 状态 |")
    lines.append("|------|------|------|")

    def health_icon(key, val, warn_threshold, crit_threshold):
        if val == 0:
            return ":white_check_mark:"
        elif val <= warn_threshold:
            return ":warning:"
        else:
            return ":red_circle:"

    lines.append(f"| 总笔记数 | {health_stats.get('total_notes', '?')} | - |")
    lines.append(f"| 总大小 | {health_stats.get('total_size_mb', '?')} MB | - |")
    lines.append(f"| 孤立笔记 | {health_stats.get('orphans', 0)} | {health_icon('orphans', health_stats.get('orphans', 0), 5, 20)} |")
    lines.append(f"| 断链 | {health_stats.get('broken_links', 0)} | {health_icon('broken', health_stats.get('broken_links', 0), 10, 50)} |")
    lines.append(f"| 过短笔记 | {health_stats.get('tiny_notes', 0)} | {health_icon('tiny', health_stats.get('tiny_notes', 0), 20, 50)} |")
    lines.append(f"| 重复组 | {health_stats.get('duplicate_groups', 0)} | {health_icon('dup', health_stats.get('duplicate_groups', 0), 3, 10)} |")
    lines.append(f"| 陈旧笔记 | {health_stats.get('stale_notes', 0)} | {health_icon('stale', health_stats.get('stale_notes', 0), 10, 30)} |")
    lines.append("")

    if health_issues:
        lines.append("### 问题详情")
        lines.append("")

        issue_labels = {
            "orphans": "孤立笔记（无链接）",
            "broken_links": "断链（目标不存在）",
            "tiny_notes": "过短笔记（<60字符）",
            "duplicates": "疑似重复笔记组",
            "stale_notes": "陈旧笔记（6月+未修改）"
        }

        for issue_key, items in health_issues.items():
            label = issue_labels.get(issue_key, issue_key)
            lines.append(f"#### {label} ({len(items)} 项)")
            lines.append("")
            if issue_key == "duplicates":
                for group in items:
                    lines.append("```")
                    for f in group:
                        lines.append(f"  {f}")
                    lines.append("```")
            else:
                for item in items[:10]:
                    lines.append(f"- `{item}`")
                if len(items) > 10:
                    lines.append(f"- ... 还有 {len(items) - 10} 项")
            lines.append("")

    # Folder distribution
    lines.append("### 文件夹分布")
    lines.append("")
    lines.append("| 文件夹 | 笔记数 | 大小(KB) |")
    lines.append("|--------|--------|----------|")
    for folder, info in health_stats.get("folder_distribution", {}).items():
        lines.append(f"| {folder} | {info['notes']} | {info['size_kb']} |")
    lines.append("")

    # Section 5: Self-Evolution Actions
    lines.append("---")
    lines.append("")
    lines.append("## 五、自进化行动清单")
    lines.append("")
    lines.append("> 以下为系统自动建议的执行动作，按优先级排列。")
    lines.append("")

    lines.append("### 高优先级")
    lines.append("")
    has_high = False
    if health_stats.get("broken_links", 0) > 10:
        lines.append(f"- [ ] 修复 {health_stats['broken_links']} 处断链")
        has_high = True
    if health_stats.get("duplicate_groups", 0) > 3:
        lines.append(f"- [ ] 清理 {health_stats['duplicate_groups']} 组重复笔记")
        has_high = True
    if paper_sugs:
        paper_count = sum(len(v) for v in paper_sugs.values())
        lines.append(f"- [ ] 审阅 {paper_count} 条论文相关灵感建议（见第三章）")
        has_high = True
    if patent_ideas:
        lines.append(f"- [ ] 评估 {len(patent_ideas)} 条专利灵感（见第三章）")
        has_high = True
    if not has_high:
        lines.append("- [ ] 无紧急待办项，知识库运行良好")
    lines.append("")

    lines.append("### 中优先级")
    lines.append("")
    has_mid = False
    if health_stats.get("orphans", 0) > 0:
        lines.append(f"- [ ] 为 {health_stats['orphans']} 篇孤立笔记添加链接")
        has_mid = True
    if health_stats.get("stale_notes", 0) > 0:
        lines.append(f"- [ ] 审查 {health_stats['stale_notes']} 篇陈旧笔记，决定保留/归档/删除")
        has_mid = True
    if concept_explore:
        lines.append(f"- [ ] 深入探索 {len(concept_explore)} 个新概念")
        has_mid = True
    if not has_mid:
        lines.append("- [ ] 无中等优先级待办项")
    lines.append("")

    lines.append("### 低优先级")
    lines.append("")
    lines.append(f"- [ ] 清理 {health_stats.get('tiny_notes', 0)} 篇过短笔记（<60字符）")
    lines.append("- [ ] 更新项目全景快照 project_snapshot.md")
    lines.append("- [ ] 检查管线配置是否需要更新")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(f"> 本报告由 Knowledge Evolution Engine v1.0 自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"> 输出路径: `99_Meta/knowledge_evolution_{TODAY}.md`")
    lines.append("")

    return "\n".join(lines)

# ============================================================
# 6. AUTO-HEAL: Lightweight self-healing actions
# ============================================================

def auto_heal(health_stats, health_issues, dry_run=False):
    """Execute safe auto-healing actions."""
    actions_taken = []
    skipped = []

    # Log broken links
    broken = health_issues.get("broken_links", [])
    if broken:
        broken_log = OUTPUT_DIR / "broken_links_log.json"
        existing = {}
        if broken_log.exists():
            try:
                existing = json.loads(broken_log.read_text(encoding="utf-8"))
            except Exception:
                pass
        existing[TODAY] = broken
        broken_log.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
        actions_taken.append(f"Logged {len(broken)} broken links to broken_links_log.json")

    # Log duplicate groups
    dups = health_issues.get("duplicates", [])
    if dups:
        dup_log = OUTPUT_DIR / "duplicate_groups_log.json"
        existing = {}
        if dup_log.exists():
            try:
                existing = json.loads(dup_log.read_text(encoding="utf-8"))
            except Exception:
                pass
        existing[TODAY] = [list(g) for g in dups]
        dup_log.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
        actions_taken.append(f"Logged {len(dups)} duplicate groups to duplicate_groups_log.json")

    # Update project_snapshot.md statistics
    snapshot_path = OUTPUT_DIR / "project_snapshot.md"
    if snapshot_path.exists():
        try:
            old_content = snapshot_path.read_text(encoding="utf-8", errors="ignore")
            new_stats = (
                f"| 总笔记数 | {health_stats.get('total_notes', '?')} 篇 |\n"
            )
            if "总笔记数" in old_content:
                old_content = re.sub(
                    r"\| 总笔记数 \|.*\|",
                    new_stats.strip(),
                    old_content
                )
                snapshot_path.write_text(old_content, encoding="utf-8")
                actions_taken.append("Updated project_snapshot.md statistics")
        except Exception as e:
            skipped.append(f"project_snapshot update skipped: {e}")

    return actions_taken, skipped


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 60)
    print("  Knowledge Evolution Engine v1.0")
    print(f"  {TODAY}")
    print("=" * 60)
    print()

    # Step 1: Scan
    print("[1/5] Scanning for new/modified notes...")
    new_notes, total_count = scan_new_notes()
    print(f"       Total vault notes: {total_count}")
    print(f"       New/modified this week: {len(new_notes)}")
    print()

    # Step 2: Classify
    print("[2/5] Classifying notes...")
    tcc_count = sum(1 for n in new_notes if keyword_classify(n)[0].startswith("TCC"))
    inest_count = sum(1 for n in new_notes if keyword_classify(n)[0].startswith("iNEST"))
    general_count = len(new_notes) - tcc_count - inest_count
    print(f"       TCC: {tcc_count} | iNEST: {inest_count} | General: {general_count}")
    print()

    # Step 3: LLM Deep Analysis
    print("[3/5] Running LLM deep analysis...")
    llm_insights = []
    if new_notes:
        llm_insights = llm_deep_classify(new_notes, max_notes=25)
        candidates = sorted(new_notes, key=lambda x: x["size"], reverse=True)[:25]
        for item in llm_insights:
            idx = item.get("note_index", -1)
            if 0 <= idx < len(candidates):
                item["_note"] = candidates[idx]
        print(f"       Generated {len(llm_insights)} structured insights")
    else:
        print("       Skipped (no new notes)")
    print()

    # Step 4: Cross-reference
    print("[4/5] Cross-referencing with active papers...")
    cross_ref = cross_reference(llm_insights)
    paper_count = sum(len(v) for v in cross_ref["paper_suggestions"].values())
    print(f"       Paper suggestions: {paper_count}")
    print(f"       Patent ideas: {len(cross_ref['patent_ideas'])}")
    print(f"       Project ideas: {len(cross_ref['project_ideas'])}")
    print(f"       Concepts to explore: {len(cross_ref['concept_explore'])}")
    print()

    # Step 5: Health diagnostics
    print("[5/5] Running vault health diagnostics...")
    health_stats, health_issues = run_health_diagnostics()
    print(f"       Issues found: {sum(len(v) for v in health_issues.values())}")
    print(f"       Broken links: {health_stats.get('broken_links', 0)}")
    print(f"       Orphans: {health_stats.get('orphans', 0)}")
    print(f"       Duplicates: {health_stats.get('duplicate_groups', 0)}")
    print()

    # Generate report
    print("Generating report...")
    report = generate_report(new_notes, llm_insights, cross_ref, health_stats, health_issues)
    report_path = OUTPUT_DIR / f"knowledge_evolution_{TODAY}.md"
    report_path.write_text(report, encoding="utf-8")
    print(f"   Report saved: {report_path}")
    print()

    # Auto-heal
    print("Running auto-healing...")
    actions, skipped = auto_heal(health_stats, health_issues)
    for a in actions:
        print(f"   {a}")
    for s in skipped:
        print(f"   {s}")
    print()

    # Summary
    print("=" * 60)
    print("  Evolution complete!")
    print(f"  Report: 99_Meta/knowledge_evolution_{TODAY}.md")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())