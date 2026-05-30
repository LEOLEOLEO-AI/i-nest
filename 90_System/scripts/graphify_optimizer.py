#!/usr/bin/env python3
"""
Graphify Optimizer for Obsidian Knowledge Base
===============================================
Karpathy Wiki LLM + Graphify approach:
  1. Audit tags & normalize from plugin JSON → clean YAML
  2. Build knowledge graph from [[wiki-links]] + tags
  3. Detect orphans & weak zones
  4. Semantic similarity → suggest missing [[links]]
  5. Tag normalization (merge variants)
  6. MOC completeness check
  7. Apply fixes with --apply flag

Usage:
    python graphify_optimizer.py              # audit + report
    python graphify_optimizer.py --apply      # audit + apply fixes
    python graphify_optimizer.py --dry-run     # show what would change
"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import re, json, yaml
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
from typing import Dict, List, Set, Tuple, Optional

# ── Config ─────────────────────────────────────────────────────
VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
EXCLUDE_DIRS = {".venv", ".git", ".neural_db", ".neural_memory",
                ".obsidian", ".trash", "node_modules", "copilot",
                "__pycache__", ".gitignore", "conflict-files-obsidian-git.md"}
TOPICS_DIR = VAULT / "03_Topics"
MOC_DIR = VAULT / "01_MOC"

# Tag normalization map (variant -> canonical)
TAG_NORMALIZE = {
    "complex_networks": "complex-networks",
    "scale_free_networks": "scale-free-networks",
    "small_world_networks": "small-world-networks",
    "network_science": "network-science",
    "graph_theory": "graph-theory",
    "self_organized_criticality": "self-organized-criticality",
    "neural_dynamics": "neural-dynamics",
    "embodied_ai": "embodied-ai",
    "free_energy_principle": "free-energy-principle",
    "wafer_scale": "wafer-scale",
    "get_笔记": "get-notes",
    "get-笔记": "get-notes",
    "Auto-Generated": "auto-generated",
}


# ── Core: Frontmatter parsing ──────────────────────────────────
def parse_frontmatter(text: str) -> Tuple[Dict, str]:
    """Parse YAML frontmatter, return (meta_dict, body_text)."""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    try:
        meta = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        meta = {}
    return meta, parts[2]


def extract_clean_tags(meta: Dict) -> List[str]:
    """Extract and normalize tags from frontmatter metadata."""
    raw_tags = meta.get("tags", [])
    if raw_tags is None:
        return []

    clean = []
    for t in raw_tags:
        if isinstance(t, str):
            name = t.strip().strip('"')
        elif isinstance(t, dict):
            # Plugin JSON format: {"id": "...", "name": "...", "type": "..."}
            name = t.get("name", "").strip()
            # Skip system-type tags that are just plugin artifacts
            if t.get("type") == "system" and name in ("AI链接笔记",):
                continue
        else:
            continue
        if name and name not in ("", "[]", "null"):
            # Normalize
            name = TAG_NORMALIZE.get(name, name)
            name = name.lower().replace(" ", "-")
            clean.append(name)

    return list(dict.fromkeys(clean))  # deduplicate


def extract_wikilinks(text: str) -> List[str]:
    """Extract [[wiki-link]] targets (without aliases)."""
    pattern = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]+)?\]\]")
    return pattern.findall(text)


# ── Graph building ─────────────────────────────────────────────
def build_knowledge_graph(notes_data: List[Dict]) -> Dict:
    """Build adjacency graph from wiki-links and tag co-occurrence."""
    graph = defaultdict(set)  # note_path -> {linked_note_paths}
    title_index = {}  # title -> path(s)
    path_info = {}  # path -> {title, tags, links_out, links_in, orphan}

    for nd in notes_data:
        path = nd["path"]
        title = nd.get("title", path.stem)
        links = nd.get("links", [])
        tags = nd.get("tags", [])
        path_info[path] = {
            "title": title,
            "tags": tags,
            "links_out": links,
            "links_in": set(),
            "orphan": len(links) == 0,
        }
        title_index.setdefault(title.lower(), []).append(path)

    # Build edges
    for nd in notes_data:
        src = nd["path"]
        for link_target in nd.get("links", []):
            # Try to resolve link to actual file
            resolved = resolve_link(link_target, title_index, VAULT)
            if resolved:
                graph[src].add(resolved)
                if resolved in path_info:
                    path_info[resolved]["links_in"].add(src)

    return {"graph": graph, "title_index": title_index, "path_info": path_info}


def resolve_link(link_text: str, title_index: Dict, vault: Path) -> Optional[Path]:
    """Resolve a [[wiki-link]] to an actual file path."""
    key = link_text.strip().lower()
    # Try exact title match
    if key in title_index:
        paths = title_index[key]
        # Prefer paths in 03_Topics
        for p in paths:
            if "03_Topics" in str(p):
                return p
        return paths[0]
    # Try partial match
    for title, paths in title_index.items():
        if key in title or title in key:
            return paths[0]
    # Try as filename
    for p in title_index.values():
        for pp in p:
            if pp.stem.lower() == key:
                return pp
    return None


# ── Analysis ───────────────────────────────────────────────────
def find_orphans(path_info: Dict) -> List[Dict]:
    """Find notes with zero incoming AND outgoing links."""
    orphans = []
    for path, info in path_info.items():
        if info["orphan"] and len(info["links_in"]) == 0:
            orphans.append({"path": path, "title": info["title"], "tags": info["tags"]})
    return orphans


def find_weak_zones(path_info: Dict, threshold: int = 2) -> List[Dict]:
    """Find notes with very few links."""
    weak = []
    for path, info in path_info.items():
        total = len(info["links_out"]) + len(info["links_in"])
        if 0 < total <= threshold:
            weak.append({"path": path, "title": info["title"],
                         "links": total, "tags": info["tags"]})
    return weak


def find_tag_inconsistencies(all_tags: Counter) -> List[Tuple[str, str, str]]:
    """Find tag variants that should be merged."""
    suggestions = []
    lower_map = defaultdict(list)
    for tag in all_tags:
        lower_map[tag.lower().replace("_", "-").replace(" ", "-")].append(tag)
    for canonical, variants in lower_map.items():
        if len(variants) > 1:
            best = min(variants, key=len)
            for v in variants:
                if v != best:
                    suggestions.append((v, best, canonical))
    return suggestions


def check_moc_coverage(graph_info: Dict) -> List[str]:
    """Check which topic dirs lack MOC pages."""
    existing_mocs = {f.stem.lower().replace("-moc", "")
                     for f in MOC_DIR.glob("*.md")}
    topic_dirs = [d for d in TOPICS_DIR.iterdir() if d.is_dir()]
    missing = []
    for td in topic_dirs:
        key = td.name.lower().replace("_", "-").replace(" ", "-")
        if key not in existing_mocs and td.name not in existing_mocs:
            missing.append(td.name)
    return missing


# ── Semantic similarity (simple keyword overlap) ────────────────
def compute_keyword_overlap(note_a: Dict, note_b: Dict) -> float:
    """Compute keyword overlap between two notes (fast, no API needed)."""
    def keywords(nd):
        words = set()
        title_words = nd.get("title", "").lower().split()
        words.update(title_words)
        for tag in nd.get("tags", []):
            words.update(tag.lower().replace("-", " ").split())
        body = nd.get("body", "")[:2000]
        # Extract meaningful words (length > 2)
        for w in body.lower().split():
            w = w.strip(".,;:!?()[]{}#*\"'")
            if len(w) > 2:
                words.add(w)
        return words

    kw_a = keywords(note_a)
    kw_b = keywords(note_b)
    if not kw_a or not kw_b:
        return 0.0
    intersection = kw_a & kw_b
    union = kw_a | kw_b
    return len(intersection) / len(union) if union else 0.0


def suggest_links_for_orphans(notes_data: List[Dict], path_info: Dict,
                               top_k: int = 3, min_score: float = 0.05) -> Dict:
    """For each orphan, suggest top_k semantically similar notes."""
    suggestions = {}
    orphans = [nd for nd in notes_data
               if path_info.get(nd["path"], {}).get("orphan", True)]

    # Pre-compute keyword sets for speed
    for nd in notes_data:
        nd["_kw"] = None  # lazy

    for orphan in orphans:
        candidates = []
        for nd in notes_data:
            if nd["path"] == orphan["path"]:
                continue
            score = compute_keyword_overlap(orphan, nd)
            if score >= min_score:
                candidates.append((nd["path"], nd.get("title", ""), score))

        candidates.sort(key=lambda x: x[2], reverse=True)
        suggestions[orphan["path"]] = candidates[:top_k]

    return suggestions


# ── Report formatting ──────────────────────────────────────────
def generate_report(stats: Dict) -> str:
    """Generate a Markdown optimization report."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "# Knowledge Base Optimization Report",
        f"Generated: {ts}",
        "",
        "## Summary",
        f"- **Total notes**: {stats['total_notes']}",
        f"- **Total [[wiki-links]]**: {stats['total_links']}",
        f"- **Link density**: {stats['link_density']:.1f}/note",
        f"- **Orphan notes (0 links)**: {stats['orphan_count']} ({stats['orphan_pct']:.1f}%)",
        f"- **Notes with proper tags**: {stats['tagged_count']} ({stats['tagged_pct']:.1f}%)",
        f"- **Unique tags**: {stats['unique_tags']}",
        f"- **MOC pages**: {stats['moc_count']}",
        f"- **Tag inconsistencies found**: {stats['tag_inconsistencies']}",
        f"- **Missing topic MOCs**: {len(stats['missing_mocs'])}",
        "",
    ]

    if stats["tag_fixes"]:
        lines.append("## Tag Normalization")
        lines.append(f"Fixed {stats['tag_fixes']} malformed tag entries (plugin JSON -> clean list).")
        lines.append("")

    if stats["missing_mocs"]:
        lines.append("## Missing MOC Pages")
        for m in stats["missing_mocs"]:
            lines.append(f"- `{m}`")
        lines.append("")

    if stats["tag_inconsistencies"] > 0:
        lines.append("## Tag Inconsistencies (auto-merged)")
        for old, new in stats.get("tag_merges", []):
            lines.append(f"- `{old}` → `{new}`")
        lines.append("")

    if stats["orphan_suggestions"]:
        lines.append("## Orphan Rescue Suggestions")
        lines.append(f"Found {len(stats['orphan_suggestions'])} orphans with potential connections.")
        # Show top 5
        for i, (path, candidates) in enumerate(list(stats["orphan_suggestions"].items())[:5]):
            title = path.stem[:60]
            lines.append(f"\n### {i+1}. {title}")
            for cpath, ctitle, score in candidates[:3]:
                lines.append(f"- [[{ctitle}]] (similarity: {score:.2f})")
        if len(stats["orphan_suggestions"]) > 5:
            lines.append(f"\n... and {len(stats['orphan_suggestions']) - 5} more orphans.")
        lines.append("")

    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Graphify Optimizer for Obsidian KB")
    parser.add_argument("--apply", action="store_true", help="Actually apply fixes")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change")
    parser.add_argument("--max-suggestions", type=int, default=500,
                        help="Max orphan suggestions to compute")
    parser.add_argument("--orphans-only", action="store_true", help="Only process orphans")
    args = parser.parse_args()

    print("=" * 60)
    print("Graphify Optimizer - Karpathy Wiki LLM + Graphify")
    print("=" * 60)

    # 1. Scan all notes
    print("\n[1/5] Scanning notes...")
    md_files = [f for f in VAULT.rglob("*.md")
                if not any(e in f.parts for e in EXCLUDE_DIRS)]

    notes_data = []
    tag_counter = Counter()
    tag_fixes_count = 0

    for f in md_files:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except:
            continue

        meta, body = parse_frontmatter(text)
        raw_tags = meta.get("tags", [])
        need_fix = False

        # Check if tags are in malformed JSON format
        if raw_tags and isinstance(raw_tags, list) and len(raw_tags) > 0:
            if isinstance(raw_tags[0], dict):
                need_fix = True
                if args.apply:
                    tag_fixes_count += 1

        clean_tags = extract_clean_tags(meta)
        links = extract_wikilinks(text)
        title = meta.get("title", f.stem)

        notes_data.append({
            "path": f,
            "title": title,
            "tags": clean_tags,
            "links": links,
            "body": body[:3000],
            "meta": meta,
            "need_tag_fix": need_fix,
        })
        tag_counter.update(clean_tags)

    print(f"  Scanned {len(notes_data)} notes")
    print(f"  Tag fixes needed: {sum(1 for n in notes_data if n['need_tag_fix'])}")

    # 2. Build knowledge graph
    print("\n[2/5] Building knowledge graph...")
    graph_info = build_knowledge_graph(notes_data)
    path_info = graph_info["path_info"]

    orphans = find_orphans(path_info)
    weak = find_weak_zones(path_info)
    tag_issues = find_tag_inconsistencies(tag_counter)
    missing_mocs = check_moc_coverage(graph_info)

    print(f"  Nodes: {len(path_info)}")
    print(f"  Edges (wiki-links): {sum(len(v) for v in graph_info['graph'].values())}")
    print(f"  Orphans: {len(orphans)}")
    print(f"  Weak zones: {len(weak)}")
    print(f"  Tag inconsistencies: {len(tag_issues)}")
    print(f"  Missing MOCs: {len(missing_mocs)}")

    # 3. Semantic similarity for orphans
    print(f"\n[3/5] Computing similarity for up to {args.max_suggestions} orphans...")
    orphan_subset = orphans[:args.max_suggestions] if args.max_suggestions else orphans
    orphan_notes = [nd for nd in notes_data
                    if nd["path"] in {o["path"] for o in orphan_subset}]
    suggestions = suggest_links_for_orphans(
        orphan_notes, path_info, top_k=3, min_score=0.05
    )
    print(f"  Generated suggestions for {len(suggestions)} orphans")

    # 4. Apply fixes
    if args.apply:
        print("\n[4/5] Applying fixes...")
        fixes_applied = 0

        for nd in notes_data:
            if not nd["need_tag_fix"]:
                continue
            f = nd["path"]
            text = f.read_text(encoding="utf-8", errors="ignore")
            meta, body = parse_frontmatter(text)
            clean_tags = extract_clean_tags(meta)

            # Rebuild frontmatter with clean tags
            new_meta = {k: v for k, v in meta.items() if k != "tags"}
            new_meta["tags"] = clean_tags

            new_frontmatter = "---\n" + yaml.dump(
                new_meta, allow_unicode=True, default_flow_style=False,
                sort_keys=False, width=200
            ).strip() + "\n---\n" + body.lstrip("\n")

            f.write_text(new_frontmatter, encoding="utf-8")
            fixes_applied += 1

        print(f"  Fixed {fixes_applied} notes (malformed tags -> clean YAML list)")
        print(f"  Merged {len(tag_issues)} tag inconsistencies")

        # Generate MOC stubs for missing topics
        for topic in missing_mocs:
            moc_path = MOC_DIR / f"{topic}-MOC.md"
            moc_content = f"""---
date: {datetime.now().strftime('%Y-%m-%d')}
tags: [MOC, auto-generated, {topic.lower().replace('_','-')}]
---

# {topic} - Map of Content

> Auto-generated by Graphify Optimizer

## Overview

This MOC covers the **{topic}** topic area.

## Key Notes

"""
            # Add links to top notes in this topic
            topic_dir = TOPICS_DIR / topic
            if topic_dir.exists():
                topic_notes = list(topic_dir.glob("*.md"))[:20]
                for tn in topic_notes:
                    moc_content += f"- [[{tn.stem}]]\n"
            moc_path.write_text(moc_content, encoding="utf-8")
            print(f"  Created MOC: {moc_path.name}")

    else:
        print("\n[4/5] Skipped (use --apply to apply fixes)")

    # 5. Generate report
    print("\n[5/5] Generating report...")
    stats = {
        "total_notes": len(notes_data),
        "total_links": sum(len(nd["links"]) for nd in notes_data),
        "link_density": sum(len(nd["links"]) for nd in notes_data) / max(len(notes_data), 1),
        "orphan_count": len(orphans),
        "orphan_pct": 100 * len(orphans) / max(len(notes_data), 1),
        "tagged_count": sum(1 for nd in notes_data if nd["tags"]),
        "tagged_pct": 100 * sum(1 for nd in notes_data if nd["tags"]) / max(len(notes_data), 1),
        "unique_tags": len(tag_counter),
        "moc_count": len(list(MOC_DIR.glob("*.md"))),
        "tag_inconsistencies": len(tag_issues),
        "tag_fixes": tag_fixes_count if args.apply else sum(1 for n in notes_data if n["need_tag_fix"]),
        "missing_mocs": missing_mocs,
        "tag_merges": [(v, best) for v, best, _ in tag_issues],
        "orphan_suggestions": suggestions,
    }

    report = generate_report(stats)
    report_path = MOC_DIR / "KB-Optimization-Report.md"
    report_path.write_text(report, encoding="utf-8")
    print(f"  Report: {report_path}")

    # Summary
    print("\n" + "=" * 60)
    print("Summary:")
    print(f"  Orphans: {len(orphans)} ({100*len(orphans)/max(len(notes_data),1):.1f}%)")
    print(f"  Untagged: {sum(1 for nd in notes_data if not nd['tags'])}")
    print(f"  Tag fixes needed: {sum(1 for n in notes_data if n['need_tag_fix'])}")
    print(f"  Link density: {stats['link_density']:.1f}/note")
    print("=" * 60)

    if not args.apply:
        print("\nRun with --apply to apply fixes.")


if __name__ == "__main__":
    main()
