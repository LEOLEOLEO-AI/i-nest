#!/usr/bin/env python3
"""Inbox classifier - classify getnote and arxiv files to TCC/iNEST based on content keywords"""
import os, sys, re, shutil
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime

VAULT = Path(r"D:\Obsidian\vault")
INBOX = VAULT / "00_Inbox"

# Keyword rules for classification
TCC_KEYWORDS = [
    "TCC", "拓扑中心", "晶圆", "wafer", "chiplet", "芯粒", "CST",
    "interconnect", "互连", "SDI", "network-on-chip", "NoC", "die-to-die",
    "2.5D", "3D-IC", "硅光", "silicon photonic", "封装", "packaging",
    "tile-based", "scale-up", "scale-out", "memory wall", "通信受限",
    "拓扑即计算", "meta topology", "元拓扑"
]

INEST_KEYWORDS = [
    "iNEST", "neuromorphic", "神经形态", "SNN", "spiking", "脉冲",
    "类脑", "brain-inspired", "neuron", "神经元", "synapse", "突触",
    "STDP", "LIF", "memristor", "忆阻", "spike-timing",
    "dendrite", "axon", "cortical", "皮层", "plasticity", "可塑性",
    "neural network", "brain atlas", "脑图谱", "hemibrain", "connectome",
    "多尺度", "multiscale", "形态", "morphology"
]

def classify_file(filepath):
    """Classify a markdown file based on content"""
    try:
        content = filepath.read_text(encoding='utf-8')[:3000]
    except:
        return None
    
    tcc_score = sum(1 for kw in TCC_KEYWORDS if kw.lower() in content.lower())
    inest_score = sum(1 for kw in INEST_KEYWORDS if kw.lower() in content.lower())
    
    if tcc_score > inest_score and tcc_score >= 2:
        return "30_TCC"
    elif inest_score > tcc_score and inest_score >= 2:
        return "40_iNEST"
    elif tcc_score > 0 and inest_score > 0:
        if tcc_score >= inest_score:
            return "30_TCC"
        else:
            return "40_iNEST"
    return None

def main():
    results = {"30_TCC": [], "40_iNEST": [], "unclassified": []}
    
    # Process root-level getnote files
    getnote_files = sorted(INBOX.glob("getnote_*.md"))
    print(f"[Inbox] 找到 {len(getnote_files)} 个 getnote_ 文件")
    
    for f in getnote_files:
        target = classify_file(f)
        if target:
            dest_dir = VAULT / target / "Inbox_imports"
            dest_dir.mkdir(exist_ok=True)
            dest = dest_dir / f.name
            # Avoid overwriting existing
            if dest.exists():
                dest = dest_dir / f"{f.stem}_dup_{int(datetime.now().timestamp())}.md"
            shutil.move(str(f), str(dest))
            results[target].append(f.name)
        else:
            results["unclassified"].append(f.name)
    
    # Process arxiv-auto files
    arxiv_files = sorted((INBOX / "arxiv-auto").glob("*.md")) if (INBOX / "arxiv-auto").exists() else []
    print(f"[Inbox] 找到 {len(arxiv_files)} 个 arxiv-auto 文件")
    
    for f in arxiv_files:
        target = classify_file(f)
        if target:
            dest_dir = VAULT / target / "31_Theory" / "01_论文"
            dest = dest_dir / f.name
            if dest.exists():
                dest = dest_dir / f"{f.stem}_arxiv_{int(datetime.now().timestamp())}.md"
            dest_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(str(f), str(dest))
            results[target].append(f.name)
        else:
            results["unclassified"].append(f.name)
    
    # Report
    print(f"\n=== 分类结果 ===")
    print(f"→ 30_TCC: {len(results['30_TCC'])} 个")
    print(f"→ 40_iNEST: {len(results['40_iNEST'])} 个")
    print(f"→ 未分类: {len(results['unclassified'])} 个")
    
    if results["unclassified"]:
        print(f"\n未分类文件 (移至 20_Processing):")
        proc_dir = VAULT / "20_Processing" / "inbox_overflow"
        proc_dir.mkdir(exist_ok=True)
        for name in results["unclassified"]:
            f = INBOX / name
            if f.exists():
                shutil.move(str(f), str(proc_dir / name))
                print(f"  • {name}")
    
    # Cleanup empty arxiv-auto
    arxiv_dir = INBOX / "arxiv-auto"
    if arxiv_dir.exists() and not any(arxiv_dir.iterdir()):
        arxiv_dir.rmdir()
        print("\n  已清理空的 arxiv-auto 目录")
    
    remaining = list(INBOX.glob("*.md"))
    print(f"\n[Inbox] 剩余根级文件: {len(remaining)}")

if __name__ == "__main__":
    main()
