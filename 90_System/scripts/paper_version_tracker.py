#!/usr/bin/env python3
"""Paper Version Tracker — merge versions, track history, deduplicate counts"""
import json, re, shutil, sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime
from collections import defaultdict

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
TODAY = datetime.now().strftime("%Y-%m-%d")

def normalize_strict(name):
    n = name.lower()
    n = re.sub(r"[_\-\.]v\d+(\.\d+)*", "", n)
    n = re.sub(r"[_\-\.]V\d+", "", n)
    n = re.sub(r"[_\-\.]ver[\s\.]*\d+", "", n)
    n = re.sub(r"[_\-\.]version[\s\.]*\d+", "", n)
    n = re.sub(r"[_\-\.](FINAL|final|DRAFT|draft|clean|dup|copy|WIP)", "", n)
    n = re.sub(r"[_\-\.]\d{8}", "", n)
    n = re.sub(r"[_\-\.]\d{4}[-\.]\d{2}[-\.]\d{2}", "", n)
    n = re.sub(r"^\d+[_\-\.]+", "", n)
    n = re.sub(r"[_\-\.]重新生成版", "", n)
    n = re.sub(r"[_\-\.]副本", "", n)
    n = re.sub(r"\s+", " ", n)
    return n.strip("_- .")[:50]

def build_version_index():
    """Build complete version tracking index"""
    all_files = []
    for d in ["30_TCC", "40_iNEST", "50_Output/51_Papers"]:
        p = VAULT / d
        if p.exists():
            for f in p.rglob("*.md"):
                all_files.append({
                    "name": f.name, "stem": f.stem,
                    "path": str(f.relative_to(VAULT)),
                    "size": f.stat().st_size,
                    "mtime": datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d"),
                    "dir": d
                })

    # Group by normalized name
    groups = defaultdict(list)
    for f in all_files:
        key = normalize_strict(f["stem"])
        groups[key].append(f)

    # Build version index
    index = {}
    paper_id = 1
    for key, files in sorted(groups.items()):
        # Sort: newest first, then largest
        files.sort(key=lambda x: (x["mtime"], x["size"]), reverse=True)
        primary = files[0]
        versions = files[1:] if len(files) > 1 else []
        
        # Determine primary directory
        if "51_Papers" in primary["path"]:
            primary_dir = "51_Papers"
        elif "iNEST" in primary["path"] or "40_iNEST" in primary["path"]:
            primary_dir = "iNEST"
        else:
            primary_dir = "TCC"
        
        index[f"PAPER-{paper_id:04d}"] = {
            "id": f"PAPER-{paper_id:04d}",
            "title": primary["name"].replace(".md", ""),
            "primary_path": primary["path"],
            "primary_dir": primary_dir,
            "version_count": len(files),
            "latest_mtime": primary["mtime"],
            "total_size": sum(f["size"] for f in files),
            "versions": [{"path": f["path"], "mtime": f["mtime"], "size": f["size"]} for f in files],
            "cross_dir": len(set(f["dir"] for f in files)) > 1
        }
        paper_id += 1

    return index

def generate_tracking_md(index):
    """Generate Paper_Versions_Index.md"""
    lines = [
        f"# 📄 论文版本跟踪索引",
        f"",
        f"> **生成时间**: {TODAY}",
        f"> **唯一论文**: {len(index)} 篇",
        f"> **含版本文件**: {sum(v['version_count'] for v in index.values())} 个",
        f"> **跨目录重复**: {sum(1 for v in index.values() if v['cross_dir'])} 组",
        f"",
        f"---",
        f"",
        f"## 📊 统计概览",
        f"",
        f"| 分类 | 数量 |",
        f"|------|------|",
    ]
    
    dir_counts = defaultdict(int)
    for v in index.values():
        dir_counts[v["primary_dir"]] += 1
    
    for d, c in sorted(dir_counts.items()):
        lines.append(f"| {d} | {c} |")
    lines.append(f"| **总计** | **{len(index)}** |")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Multi-version papers
    multi = {k: v for k, v in index.items() if v["version_count"] > 1}
    if multi:
        lines.append(f"## 🔄 多版本论文 ({len(multi)} 组)")
        lines.append("")
        for pid, v in sorted(multi.items(), key=lambda x: x[1]["version_count"], reverse=True):
            lines.append(f"### {pid}: {v['title'][:80]}")
            lines.append(f"- 版本数: {v['version_count']} | 最新: {v['latest_mtime']} | 跨目录: {'是' if v['cross_dir'] else '否'}")
            lines.append(f"- 主文件: `{v['primary_path']}`")
            for ver in v["versions"]:
                marker = "⭐" if ver["path"] == v["primary_path"] else "  "
                lines.append(f"  {marker} `{ver['path']}` ({ver['mtime']}, {ver['size']//1024}KB)")
            lines.append("")
    
    # Cross-directory dupes
    cross = {k: v for k, v in index.items() if v["cross_dir"]}
    if cross:
        lines.append(f"## ⚠️ 跨目录重复 ({len(cross)} 组)")
        lines.append("")
        lines.append("> 以下论文在 TCC 和 iNEST 目录中均有副本。建议保留最主要版本，另一个目录添加 `[[链接]]` 替代。")
        lines.append("")
        for pid, v in sorted(cross.items()):
            dirs = set(Path(ver["path"]).parts[0] for ver in v["versions"])
            lines.append(f"- **{pid}**: {v['title'][:60]} — 存在于 {', '.join(dirs)}")
    
    # Paper list
    lines.append("")
    lines.append("---")
    lines.append(f"## 📋 完整论文清单 ({len(index)} 篇)")
    lines.append("")
    for pid, v in sorted(index.items()):
        lines.append(f"- **{pid}**: [{v['title'][:80]}]({v['primary_path']}) `v{v['version_count']}` {v['latest_mtime']}")
    
    return "\n".join(lines)

def resolve_cross_dupes(index, dry_run=False):
    """For cross-directory dupes, keep primary, add link annotation to copies"""
    cross = {k: v for k, v in index.items() if v["cross_dir"]}
    resolved = 0
    
    for pid, v in cross.items():
        primary_path = VAULT / v["primary_path"]
        for ver in v["versions"]:
            if ver["path"] == v["primary_path"]:
                continue
            dup_path = VAULT / ver["path"]
            if not dup_path.exists():
                continue
            
            try:
                content = dup_path.read_text(encoding="utf-8", errors="replace")
                # Add cross-reference note
                note = f"\n\n> [!note]- 版本跟踪\n> 本文另有版本: [[{primary_path.stem}]]（主版本）\n> 此文件为 {ver['mtime']} 版本，保留用于版本历史追溯。\n"
                if "版本跟踪" not in content:
                    if not dry_run:
                        dup_path.write_text(content + note, encoding="utf-8")
                    resolved += 1
            except Exception as e:
                print(f"  Error on {ver['path']}: {e}")
    
    print(f"Cross-dir dupes annotated: {resolved}")
    return resolved

if __name__ == "__main__":
    print("Building version index...")
    index = build_version_index()
    print(f"  Unique papers: {len(index)}")
    print(f"  Total versions: {sum(v['version_count'] for v in index.values())}")
    
    # Generate tracking doc
    md = generate_tracking_md(index)
    out = VAULT / "50_Output" / "51_Papers" / "00_Paper_Versions_Index.md"
    out.write_text(md, encoding="utf-8")
    print(f"  Index saved: {out.relative_to(VAULT)}")
    
    # Also save JSON for data bus
    json_out = VAULT / "50_Output" / "51_Papers" / "paper_versions.json"
    json_out.write_text(json.dumps({"papers": list(index.values()), "total_unique": len(index), "generated": TODAY}, ensure_ascii=False, indent=2), encoding="utf-8")
    
    # Resolve cross-dupes
    dry = "--dry-run" in sys.argv
    resolve_cross_dupes(index, dry_run=dry)
    
    # Summary
    cross_count = sum(1 for v in index.values() if v["cross_dir"])
    multi_count = sum(1 for v in index.values() if v["version_count"] > 1)
    print(f"\nSummary: {len(index)} unique papers, {multi_count} multi-version, {cross_count} cross-dir")
