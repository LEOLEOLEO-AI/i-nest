#!/usr/bin/env python3
"""
Interactive review tool for ambiguous files in _archive/_needs_review.
Usage:
  python review_ambig.py batch          # LLM batch pre-classify all
  python review_ambig.py suggest <file> # LLM suggest category for one file
  python review_ambig.py move <file> <target>  # Move file to target dir
  python review_ambig.py stats          # Show progress stats
"""
import os, sys, json, re, shutil
from pathlib import Path
from datetime import datetime

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
REVIEW_DIR = VAULT / "_archive" / "_needs_review"
PROGRESS_FILE = VAULT / "60_MOC" / "_review_progress.json"

TARGETS = {
    "tcc": "30_TCC/31_Theory",
    "inest": "40_iNEST/41_Theory",
    "library": "10_Library/Papers",
    "ideas": "20_Ideas/Insights",
    "archive": "_archive/low_quality",
    "skip": None,
}

def load_progress():
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"reviewed": {}, "suggestions": {}, "total": 0}

def save_progress(progress):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

def get_review_files():
    """Get list of files awaiting review."""
    if not REVIEW_DIR.exists():
        return []
    files = sorted(
        [f for f in REVIEW_DIR.glob("*.md") if not f.name.startswith(".")],
        key=lambda f: f.stat().st_mtime
    )
    return files

def move_file(filename, target_key):
    """Move a file from review dir to target."""
    target_dir = TARGETS.get(target_key)
    if target_dir is None:
        return True  # skip
    
    src = REVIEW_DIR / filename
    dst_dir = VAULT / target_dir
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / filename
    
    if dst.exists():
        stem = dst.stem
        dst = dst_dir / f"{stem}_reviewed.md"
    
    shutil.move(str(src), str(dst))
    
    # Update progress
    progress = load_progress()
    progress["reviewed"][filename] = {
        "target": target_key,
        "moved_to": str(dst.relative_to(VAULT)),
        "time": datetime.now().isoformat()
    }
    save_progress(progress)
    return True

def suggest_category(filename):
    """Use keyword matching to suggest category."""
    filepath = REVIEW_DIR / filename
    if not filepath.exists():
        return {"track": "unknown", "confidence": 0}
    
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except:
        return {"track": "unknown", "confidence": 0}
    
    text = (content[:3000] + " " + filename).lower()
    
    TCC_KW = [
        "topolog", "centric comput", "sdi", "chiplet", "wafer", "interconnect",
        "routing", "noc", "fpga", "sdsow", "silicon", "cst", "scaling law",
        "semiconductor", "transistor", "chip design", "verilog", "3d-ic",
        "copos", "haihe", "suzhou", "晶上", "芯片", "集成电路", "互连", "路由",
        "晶圆", "封装", "半导体", "晶体管", "片上网络"
    ]
    iNEST_KW = [
        "inest", "neuromorphic", "spiking", "neural network", "brain",
        "emergence", "complex system", "self-organized", "criticality",
        "memristor", "cognitive", "consciousness", "neuron", "synapse",
        "stdp", "fep", "free energy", "active inference", "connectome",
        "reservoir", "liquid computing", "神经形态", "涌现", "脉冲", "突触",
        "生物", "脑", "类脑", "智涌", "忆阻器", "复杂系统", "临界"
    ]
    
    tcc = sum(1 for kw in TCC_KW if kw in text)
    inc = sum(1 for kw in iNEST_KW if kw in text)
    
    if tcc > inc * 1.5:
        return {"track": "tcc", "confidence": min(0.9, tcc / (tcc + inc + 1))}
    elif inc > tcc * 1.5:
        return {"track": "inest", "confidence": min(0.9, inc / (tcc + inc + 1))}
    elif tcc > 0 and inc > 0:
        return {"track": "mixed", "confidence": 0.5}
    else:
        return {"track": "unknown", "confidence": 0}

def batch_suggest():
    """Pre-classify all files, save suggestions."""
    files = get_review_files()
    progress = load_progress()
    progress["total"] = len(files)
    
    for fp in files:
        name = fp.name
        if name in progress["suggestions"]:
            continue
        suggestion = suggest_category(name)
        progress["suggestions"][name] = suggestion
    
    save_progress(progress)
    print(f"Batch: {len(progress['suggestions'])} files pre-classified")
    
    # Summary
    counts = {}
    for s in progress["suggestions"].values():
        t = s["track"]
        counts[t] = counts.get(t, 0) + 1
    for t, c in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {t}: {c} files")
    
    # Write summary markdown
    write_summary(progress)

def write_summary(progress):
    """Generate a human-readable summary in Obsidian."""
    counts = {}
    for s in progress["suggestions"].values():
        t = s["track"]
        counts[t] = counts.get(t, 0) + 1
    
    reviewed = len(progress["reviewed"])
    total = progress.get("total", len(get_review_files()))
    
    content = f"""---
cssclass: dashboard
---

# 📋 歧义文件审查进度

> 进度: **{reviewed}/{total}** ({(reviewed/total*100) if total else 0:.0f}%) | 更新: `$= date(today).format("YYYY-MM-DD HH:mm")`

## 📊 预分类统计

| 类别 | 数量 | 占比 |
|:---|---:|---:|
"""
    for t, c in sorted(counts.items(), key=lambda x: -x[1]):
        pct = f"{c/total*100:.1f}%" if total else "0%"
        emoji = {"tcc": "🧠", "inest": "🔧", "mixed": "⚠️", "unknown": "❓"}.get(t, "📄")
        content += f"| {emoji} {t.upper()} | {c} | {pct} |\n"
    
    content += f"""
## 🔍 待审查文件

```dataviewjs
const progress = JSON.parse(await dv.io.load("60_MOC/_review_progress.json"));
const files = dv.pages('"_archive/_needs_review"').where(p => p.file.name != ".gitkeep");

const suggestions = progress?.suggestions || {{}};
const reviewed = progress?.reviewed || {{}};

const rows = [];
for (const p of files) {{
    const name = p.file.name;
    if (reviewed[name]) continue;
    const sug = suggestions[name];
    const track = sug?.track || "?";
    const conf = sug ? Math.round(sug.confidence * 100) : 0;
    const emoji = {{tcc: "🧠", inest: "🔧", mixed: "⚠️"}}[track] || "❓";
    const preview = (p.file.content || "").substring(0, 120);
    rows.push([
        dv.fileLink(p.file.path, false, name.substring(0, 50)),
        emoji + " " + track.toUpperCase(),
        conf + "%",
        preview
    ]);
}}

dv.table(
    ["文件", "建议", "置信度", "预览"],
    rows.slice(0, 50)
);

if (rows.length > 50) {{
    dv.paragraph(`... 还有 ${rows.length - 50} 个文件`);
}}
```

## 🛠️ 操作说明

1. 浏览上方列表，查看文件名和预览
2. 在 Obsidian 中打开文件阅读内容
3. 决定归属后，在终端运行:
   ```
   python 90_System/scripts/review_ambig.py move "文件名.md" tcc|inest|library|ideas|archive
   ```
4. 刷新本页查看进度
"""
    
    summary_path = VAULT / "60_MOC" / "00_Needs_Review.md"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Summary written to 60_MOC/00_Needs_Review.md")

def stats():
    files = get_review_files()
    progress = load_progress()
    reviewed = len(progress["reviewed"])
    total = len(files) + reviewed
    print(f"Total: {total} | Reviewed: {reviewed} | Remaining: {len(files)}")
    if files:
        print(f"Next: {files[0].name[:60]}")

def main():
    if len(sys.argv) < 2:
        print("Usage: review_ambig.py <batch|suggest|move|stats> [args]")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "batch":
        batch_suggest()
    elif cmd == "suggest" and len(sys.argv) > 2:
        result = suggest_category(sys.argv[2])
        print(json.dumps(result, ensure_ascii=False))
    elif cmd == "move" and len(sys.argv) > 3:
        ok = move_file(sys.argv[2], sys.argv[3])
        print(f"Moved: {sys.argv[2]} -> {sys.argv[3]}" if ok else "Failed")
    elif cmd == "stats":
        stats()
    else:
        print("Unknown command")

if __name__ == "__main__":
    main()
