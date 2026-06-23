#!/usr/bin/env python3
"""
Auto-Frontmatter Generator
===========================
For notes without YAML frontmatter:
  1. Extract title from first # heading or filename
  2. Derive tags from directory path + content keywords
  3. Detect date from filename patterns
  4. Write clean frontmatter

Usage:
    python auto_frontmatter.py --dry-run    # preview
    python auto_frontmatter.py --apply      # write frontmatter
    python auto_frontmatter.py --max 100    # limit batch size
"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import re, yaml
from pathlib import Path
from collections import Counter
from datetime import datetime

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
EXCLUDE = {".venv",".git",".neural_db",".neural_memory",".obsidian",
           ".trash","node_modules","copilot","__pycache__"}

# Directory -> tag mapping
DIR_TAG_MAP = {
    "AI-ML": ["ai-ml", "artificial-intelligence"],
    "Neuroscience": ["neuroscience", "brain-science"],
    "Chip-Hardware": ["chip-hardware", "semiconductor"],
    "Concepts-Theory": ["concepts-theory", "fundamentals"],
    "Papers": ["paper", "literature"],
    "Research-Methods": ["research-methods", "methodology"],
    "Project-Management": ["project-management"],
    "Tools-Tutorials": ["tools", "tutorial"],
    "Web-Clips": ["web-clip"],
    "TCC-SDI": ["tcc-sdi", "software-defined"],
}

# Keywords -> tags (case-insensitive)
KEYWORD_TAG_MAP = {
    "神经网络": "neural-networks",
    "深度学习": "deep-learning",
    "transformer": "transformer",
    "注意力机制": "attention-mechanism",
    "大模型": "large-language-model",
    "llm": "large-language-model",
    "脑": "brain",
    "神经元": "neuron",
    "突触": "synapse",
    "可塑性": "plasticity",
    "复杂网络": "complex-networks",
    "无标度": "scale-free-networks",
    "小世界": "small-world-networks",
    "临界": "criticality",
    "涌现": "emergence",
    "自组织": "self-organization",
    "芯片": "chip",
    "晶圆": "wafer",
    "chiplet": "chiplet",
    "具身": "embodied-ai",
    "机器人": "robotics",
    "自由能": "free-energy-principle",
    "信息论": "information-theory",
    "拓扑": "topology",
    "图神经网络": "graph-neural-network",
    "gnn": "graph-neural-network",
    "动力学": "dynamics",
    "仿真": "simulation",
    "论文": "paper",
    "综述": "survey",
    "专利": "patent",
    "项目": "project",
}


def extract_title(text: str, filepath: Path) -> str:
    """Extract title from first # heading or filename."""
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("# ") and not line.startswith("## "):
            title = line[2:].strip()
            # Clean whitespace
            title = re.sub(r'\s+', ' ', title)
            return title[:200]
    return filepath.stem[:200]


def extract_date(text: str, filepath: Path) -> str:
    """Try to extract date from filename or content."""
    # From filename: 2025-03-15_xxx or 20250315
    name = filepath.stem
    m = re.match(r'(\d{4}-\d{2}-\d{2})', name)
    if m:
        return m.group(1)
    m = re.match(r'(\d{8})', name)
    if m:
        d = m.group(1)
        return f"{d[:4]}-{d[4:6]}-{d[6:8]}"
    # From content first line
    first_line = text.split("\n")[0].strip()
    m = re.search(r'(\d{4}-\d{2}-\d{2})', first_line)
    if m:
        return m.group(1)
    return ""


def derive_tags(text: str, filepath: Path) -> list:
    """Derive tags from directory path + content keywords."""
    tags = set()
    text_lower = text.lower()

    # Directory-based tags
    rel = filepath.relative_to(VAULT)
    for part in rel.parts:
        if part in DIR_TAG_MAP:
            tags.update(DIR_TAG_MAP[part])

    # Content keyword matching
    for kw, tag in KEYWORD_TAG_MAP.items():
        if kw.lower() in text_lower:
            tags.add(tag)

    # Limit
    return sorted(list(tags))[:10]


def generate_frontmatter(text: str, filepath: Path) -> str:
    """Generate YAML frontmatter for a note."""
    title = extract_title(text, filepath)
    date = extract_date(text, filepath)
    tags = derive_tags(text, filepath)

    meta = {"title": title, "tags": tags}
    if date:
        meta["date"] = date

    fm = "---\n"
    fm += yaml.dump(meta, allow_unicode=True, default_flow_style=False,
                     sort_keys=False, width=200).strip()
    fm += "\n---\n"

    # Remove existing # heading to avoid duplication
    body = text
    if text.startswith("# ") and not text.startswith("## "):
        body = text.split("\n", 1)[1] if "\n" in text else ""

    return fm + body.lstrip("\n")


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--max", type=int, default=0)
    args = parser.parse_args()

    md_files = [f for f in VAULT.rglob("*.md")
                if not any(e in f.parts for e in EXCLUDE)]

    no_fm = []
    for f in md_files:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except:
            continue
        if not text.startswith("---"):
            no_fm.append((f, text))

    if args.max and args.max > 0:
        no_fm = no_fm[:args.max]

    print(f"Notes without frontmatter: {len(no_fm)}")

    # Preview stats
    tag_preview = Counter()
    for f, text in no_fm[:50]:
        tags = derive_tags(text, f)
        tag_preview.update(tags)

    print(f"\nTag preview (from first 50):")
    for t, c in tag_preview.most_common(20):
        print(f"  {t}: {c}")

    if args.apply:
        print(f"\nApplying frontmatter to {len(no_fm)} notes...")
        done = 0
        for f, text in no_fm:
            new_text = generate_frontmatter(text, f)
            f.write_text(new_text, encoding="utf-8")
            done += 1
            if done % 100 == 0:
                print(f"  {done}/{len(no_fm)}...")
        print(f"Done. Added frontmatter to {done} notes.")
    elif args.dry_run:
        print("\n[DRY-RUN] Sample output:")
        for f, text in no_fm[:3]:
            print(f"\n--- {f.relative_to(VAULT)} ---")
            print(generate_frontmatter(text, f)[:400])
            print("...")
    else:
        print("\nUse --dry-run to preview, --apply to write.")


if __name__ == "__main__":
    main()
