#!/usr/bin/env python3
"""
Vault Flattener — 将知识库内散落的旧子目录文件迁移到新的标准化结构。
安全原则: 只移动 .md 文件，Obsidian WikiLink 按文件名解析，移动不断链。
"""
import os, shutil, re
from pathlib import Path
from collections import defaultdict

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")

# ============================================================
# MIGRATION RULES: (source glob, destination dir)
# ============================================================
FLATTEN_RULES = [
    # --- 30_TCC/31_Theory subdirs → flatten to 31_Theory ---
    ("30_TCC/31_Theory/_merged_knowledgebase/*.md", "30_TCC/31_Theory"),
    ("30_TCC/31_Theory/AI-ML/*.md", "30_TCC/31_Theory"),
    ("30_TCC/31_Theory/Concepts-Theory/*.md", "30_TCC/31_Theory"),
    ("30_TCC/31_Theory/_from_inbox/*.md", "30_TCC/31_Theory"),
    ("30_TCC/31_Theory/_from_review/*.md", "30_TCC/31_Theory"),
    ("30_TCC/31_Theory/_llm_classified/*.md", "30_TCC/31_Theory"),
    # --- 30_TCC/31_Theory content subdirs → correct targets ---
    ("30_TCC/31_Theory/01_论文/*.md", "50_Output/51_Papers/_from_tcc_theory"),
    ("30_TCC/31_Theory/02_专利/*.md", "50_Output/52_Patents/_from_tcc"),
    ("30_TCC/31_Theory/03_项目策划/*.md", "30_TCC/34_Projects"),
    ("30_TCC/31_Theory/05_关键技术/*.md", "30_TCC/32_Tech"),
    # --- 30_TCC/32_Tech subdirs → flatten ---
    ("30_TCC/32_Tech/Chip-Hardware/*.md", "30_TCC/32_Tech"),
    ("30_TCC/32_Tech/TCC-SDI/*.md", "30_TCC/32_Tech"),
    # --- 40_iNEST/41_Theory subdirs → flatten ---
    ("40_iNEST/41_Theory/_merged_knowledgebase/*.md", "40_iNEST/41_Theory"),
    ("40_iNEST/41_Theory/AI-ML/*.md", "40_iNEST/41_Theory"),
    ("40_iNEST/41_Theory/Concepts-Theory/*.md", "40_iNEST/41_Theory"),
    ("40_iNEST/41_Theory/_from_inbox/*.md", "40_iNEST/41_Theory"),
    ("40_iNEST/41_Theory/_from_review/*.md", "40_iNEST/41_Theory"),
    ("40_iNEST/41_Theory/_llm_classified/*.md", "40_iNEST/41_Theory"),
    ("40_iNEST/41_Theory/01_论文/*.md", "50_Output/51_Papers/_from_inest_theory"),
    ("40_iNEST/41_Theory/03_项目策划/*.md", "40_iNEST/44_Projects"),
    # --- 40_iNEST/42_Tech subdirs → flatten ---
    ("40_iNEST/42_Tech/Neuroscience/*.md", "40_iNEST/42_Tech"),
    # --- 10_Library cleanup ---
    ("10_Library/Papers/Papers/*.md", "10_Library/Papers"),
    ("10_Library/Papers/iNEST/*.md", "10_Library/Papers"),
    ("10_Library/Papers/iNEST_theory/*.md", "10_Library/Papers"),
    ("10_Library/Papers/TCC/*.md", "10_Library/Papers"),
    ("10_Library/Papers/arxiv-auto/*.md", "10_Library/Papers"),
    ("10_Library/Papers/manual/*.md", "10_Library/Papers"),
    ("10_Library/Papers/_from_inbox/*.md", "10_Library/Papers"),
    ("10_Library/Papers/_from_review/*.md", "10_Library/Papers"),
    ("10_Library/Articles/_from_review/*.md", "10_Library/Articles"),
    ("10_Library/Web-Clips/Web-Clips/*.md", "10_Library/Web-Clips"),
    # --- 20_Ideas cleanup ---
    ("20_Ideas/Fleeting/待分类/*.md", "20_Ideas/Fleeting"),
    ("20_Ideas/Fleeting/TCC计算范式/*.md", "20_Ideas/Concepts"),
    ("20_Ideas/Fleeting/智能涌现范式/*.md", "20_Ideas/Concepts"),
    ("20_Ideas/Research/Project-Management/*.md", "30_TCC/34_Projects/_from_ideas"),
    ("20_Ideas/Research/Research-Methods/*.md", "20_Ideas/Concepts"),
    ("20_Ideas/Research/Tools-Tutorials/*.md", "20_Ideas/Insights"),
    ("20_Ideas/Research/arxiv-daily/*.md", "20_Ideas/Concepts"),
]

# --- Root-level stray .md files ---
ROOT_MOVES = [
    ("30_TCC/*.md", "30_TCC"),
    ("40_iNEST/*.md", "40_iNEST"),
    ("90_System/*.md", "90_System"),
]

# --- Empty dirs to remove after migration ---
CLEANUP_DIRS = [
    "30_TCC/31_Theory/_merged_knowledgebase",
    "30_TCC/31_Theory/AI-ML",
    "30_TCC/31_Theory/Concepts-Theory",
    "30_TCC/31_Theory/_from_inbox",
    "30_TCC/31_Theory/_from_review",
    "30_TCC/31_Theory/_llm_classified",
    "30_TCC/31_Theory/01_论文",
    "30_TCC/31_Theory/02_专利",
    "30_TCC/31_Theory/03_项目策划",
    "30_TCC/31_Theory/05_关键技术",
    "30_TCC/32_Tech/Chip-Hardware",
    "30_TCC/32_Tech/TCC-SDI",
    "40_iNEST/41_Theory/_merged_knowledgebase",
    "40_iNEST/41_Theory/AI-ML",
    "40_iNEST/41_Theory/Concepts-Theory",
    "40_iNEST/41_Theory/_from_inbox",
    "40_iNEST/41_Theory/_from_review",
    "40_iNEST/41_Theory/_llm_classified",
    "40_iNEST/41_Theory/01_论文",
    "40_iNEST/41_Theory/03_项目策划",
    "40_iNEST/42_Tech/Neuroscience",
    "10_Library/Papers/Papers",
    "10_Library/Papers/iNEST",
    "10_Library/Papers/iNEST_theory",
    "10_Library/Papers/TCC",
    "10_Library/Papers/arxiv-auto",
    "10_Library/Papers/manual",
    "10_Library/Papers/_from_inbox",
    "10_Library/Papers/_from_review",
    "10_Library/Articles/_from_review",
    "10_Library/Web-Clips/Web-Clips",
    "20_Ideas/Fleeting/待分类",
    "20_Ideas/Fleeting/TCC计算范式",
    "20_Ideas/Fleeting/智能涌现范式",
    "20_Ideas/Research/Project-Management",
    "20_Ideas/Research/Research-Methods",
    "20_Ideas/Research/Tools-Tutorials",
    "20_Ideas/Research/arxiv-daily",
    "03_Topics",
]

def safe_move(src, dst_dir):
    """Move file, handling name conflicts by appending (1)."""
    dst_dir = Path(dst_dir)
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / src.name
    if dst.exists():
        stem = dst.stem
        suffix = dst.suffix
        counter = 1
        while dst.exists():
            dst = dst_dir / f"{stem} ({counter}){suffix}"
            counter += 1
    shutil.move(str(src), str(dst))
    return dst

def main(dry_run=True):
    moved = 0
    skipped = 0
    
    # Phase 1: Flatten subdirectories
    for src_glob, dst_dir in FLATTEN_RULES:
        src_pattern = str(VAULT / src_glob.replace("/", os.sep))
        for f in sorted(Path(src_pattern).parent.glob(Path(src_pattern).name)):
            if not f.is_file() or f.suffix != ".md":
                continue
            rel = f.relative_to(VAULT)
            dst_rel = Path(dst_dir) / f.name
            if dry_run:
                print(f"  [DRY] {rel} → {dst_rel}")
            else:
                try:
                    result = safe_move(f, VAULT / dst_dir)
                    print(f"  ✓ {rel} → {result.relative_to(VAULT)}")
                except Exception as e:
                    print(f"  ✗ {rel}: {e}")
                    skipped += 1
                    continue
            moved += 1
    
    # Phase 2: Clean up empty dirs
    if not dry_run:
        for d in CLEANUP_DIRS:
            dpath = VAULT / d.replace("/", os.sep)
            if dpath.exists():
                try:
                    remaining = list(dpath.glob("*"))
                    if not remaining or all(r.name == ".gitkeep" for r in remaining):
                        for r in remaining:
                            r.unlink()
                        dpath.rmdir()
                        print(f"  🗑 removed empty dir: {d}")
                except Exception as e:
                    print(f"  ⚠ could not remove {d}: {e}")
    
    print(f"\n{moved} files {'would be' if dry_run else ''} moved, {skipped} skipped.")

if __name__ == "__main__":
    import sys
    dry = "--dry-run" in sys.argv or len(sys.argv) == 1
    main(dry_run=dry)
    if dry:
        print("\nRun with --execute to apply changes.")
