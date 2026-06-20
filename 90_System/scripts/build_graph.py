#!/usr/bin/env python3
"""
Knowledge Graph Builder — bidirectional WikiLink analysis using networkx.
Scans all .md files for [[links]], builds graph, suggests missing backlinks.
"""
import os, re, json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
EXCLUDE_DIRS = {".git", ".obsidian", ".venv", ".trash", ".neural_db", "_archive", "node_modules"}

def scan_links():
    """Scan all md files and extract [[wikilinks]]."""
    links = defaultdict(set)  # source -> {targets}
    backlinks = defaultdict(set)  # target -> {sources}
    files = {}  # path -> relative name
    
    for root, dirs, filenames in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for fn in filenames:
            if not fn.endswith(".md"):
                continue
            fullpath = Path(root) / fn
            try:
                rel = str(fullpath.relative_to(VAULT)).replace("\\", "/")
            except:
                continue
            name_no_ext = fn[:-3]
            files[rel] = name_no_ext
            
            with open(fullpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            # Extract [[wikilinks]] and [alias](wikilinks)
            wiki_links = re.findall(r'\[\[([^\]|#]+)(?:[|#][^\]]+)?\]\]', content)
            md_links = re.findall(r'\[.*?\]\(([^)]+\.md)\)', content)
            
            all_links = set(wiki_links + md_links)
            for target in all_links:
                # Normalize: remove .md extension
                target_name = target.replace(".md", "").strip()
                if target_name and target_name != name_no_ext:
                    links[rel].add(target_name)
                    backlinks[target_name].add(rel)
    
    return links, backlinks, files

def suggest_backlinks(links, backlinks, files):
    """Find links that lack reciprocal backlinks."""
    suggestions = []
    for source, targets in links.items():
        for target in targets:
            # Check if target links back to source
            source_name = files.get(source, "")
            if source_name and source not in backlinks.get(target, set()):
                # Find which file maps to this target
                target_file = None
                for fp, name in files.items():
                    if name == target or fp.endswith(target + ".md") or fp.endswith("/" + target + ".md"):
                        target_file = fp
                        break
                if target_file:
                    suggestions.append({
                        "source": source,
                        "target": target_file,
                        "action": f"Add [[{source_name}]] to {target_file}"
                    })
    return suggestions

def export_graph_json(links, backlinks, files):
    """Export graph data for visualization."""
    nodes = []
    for fp, name in files.items():
        nodes.append({
            "id": fp,
            "label": name,
            "out_degree": len(links.get(fp, set())),
            "in_degree": len(backlinks.get(fp, set())),
        })
    
    edges = []
    for source, targets in links.items():
        for target in targets:
            target_file = None
            for fp, name in files.items():
                if name == target:
                    target_file = fp
                    break
            if target_file:
                edges.append({"source": source, "target": target_file})
    
    graph = {"nodes": nodes, "edges": edges}
    
    outpath = VAULT / "knowledge_graph" / "graph_data.json"
    outpath.parent.mkdir(exist_ok=True)
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
    print(f"Graph data exported: {outpath} ({len(nodes)} nodes, {len(edges)} edges)")

def auto_add_backlinks(suggestions, limit=30):
    """Automatically add backlinks for top suggestions."""
    added = 0
    for s in suggestions[:limit]:
        target_path = VAULT / s["target"]
        if not target_path.exists():
            continue
        source_name = Path(s["source"]).stem
        link_text = f"[[{source_name}]]"
        
        with open(target_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        
        if link_text in content:
            continue
        
        # Add to "## Related" section or create one
        if "## 相关笔记" in content:
            content = content.replace("## 相关笔记", f"## 相关笔记\n\n- {link_text}")
        elif "## Related" in content:
            content = content.replace("## Related", f"## Related\n\n- {link_text}")
        else:
            content += f"\n\n---\n## 相关笔记\n\n- {link_text}\n"
        
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)
        added += 1
        print(f"  + backlink: {link_text} -> {s['target']}")
    
    return added

def main(auto_fix=False):
    print(f"\n{'='*60}")
    print(f"Knowledge Graph Builder — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")
    
    print("\nScanning wiki links...")
    links, backlinks, files = scan_links()
    
    total_links = sum(len(v) for v in links.values())
    print(f"Files: {len(files)} | Links: {total_links} | Orphan nodes: {len(files) - len(links)}")
    
    print("\nFinding missing backlinks...")
    suggestions = suggest_backlinks(links, backlinks, files)
    print(f"Missing backlinks: {len(suggestions)}")
    
    if suggestions:
        print("\nTop suggestions:")
        for s in suggestions[:10]:
            print(f"  {s['action']}")
    
    if auto_fix:
        print(f"\nAuto-adding backlinks...")
        added = auto_add_backlinks(suggestions, limit=20)
        print(f"Added {added} backlinks.")
    
    export_graph_json(links, backlinks, files)
    
    # Stats
    print(f"\n--- Top Nodes by Total Degree ---")
    degrees = {}
    for fp in files:
        degrees[fp] = len(links.get(fp, set())) + len(backlinks.get(fp, set()))
    for fp, deg in sorted(degrees.items(), key=lambda x: -x[1])[:10]:
        if deg > 0:
            print(f"  {files[fp][:50]} ({deg})")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--auto-fix", action="store_true")
    args = parser.parse_args()
    main(auto_fix=args.auto_fix)
