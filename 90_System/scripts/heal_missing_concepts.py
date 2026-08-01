# -*- coding: utf-8 -*-
"""
heal_missing_concepts.py — 一次性自愈: 重建被 wiki_grow 误合并删除的裸概念占位笔记。

背景: wiki_grow 的 norm() 曾把中文 slug 全部归一为空串, 导致所有中文概念被并入
最长的一个并删除。本脚本扫描全库裸概念链接(被引用但不存在的笔记名), 重建占位笔记,
带 frontmatter + 回链来源。幂等(已存在则跳过)。

用法:
    python heal_missing_concepts.py --min-refs 2 --max 0   # 0=不限
"""
import sys, re, json
from pathlib import Path
from collections import defaultdict

VAULT = Path(r"D:\Obsidian\vault")
OUT = VAULT / "wiki" / "concepts"
TODAY = __import__("datetime").datetime.now().strftime("%Y-%m-%d")

DENY = {"双向链接", "嵌入", "标签", "附件", "看板", "图谱", "关系",
        "反链", "出链", "引用", "链接", "笔记", "搜索"}

link_re = re.compile(r"\[\[([^\]]+)\]]")


def scan():
    note_basenames = set()
    note_paths = set()
    file_paths = set()
    dirs = set()
    for f in VAULT.rglob("*"):
        rel = f.relative_to(VAULT).as_posix()
        if rel.startswith(".git") or rel.startswith(".trash"):
            continue
        if f.is_dir():
            dirs.add(rel); continue
        if f.is_file():
            noext = rel[:-len(f.suffix)] if f.suffix else rel
            file_paths.add(rel); file_paths.add(noext)
            if f.suffix.lower() == ".md":
                note_paths.add(noext); note_paths.add(rel)
                note_basenames.add(f.stem)
    broken_freq = defaultdict(int)
    refs = defaultdict(list)  # target -> [source names]
    for f in VAULT.rglob("*.md"):
        rel = f.relative_to(VAULT).as_posix()
        if rel.startswith(".git"):
            continue
        try:
            txt = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for m in link_re.findall(txt):
            raw = m.replace("\\|", "|")
            tgt = raw.split("|")[0].split("#")[0].strip().rstrip("\\").strip()
            if not tgt:
                continue
            ok = (tgt in note_basenames) or (tgt in note_paths) or \
                 (tgt in file_paths) or (tgt in dirs)
            if not ok:
                broken_freq[tgt] += 1
                refs[tgt].append(f.stem)
    return note_basenames, note_paths, file_paths, dirs, broken_freq, refs


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-refs", type=int, default=2)
    ap.add_argument("--max", type=int, default=0)
    args = ap.parse_args()

    nb, np_, fp, dirs, broken_freq, refs = scan()
    OUT.mkdir(parents=True, exist_ok=True)
    candidates = []
    for tgt, c in broken_freq.items():
        if c < args.min_refs:
            continue
        if "/" in tgt or "\\" in tgt:
            continue
        if "." in tgt:
            continue
        if not (2 <= len(tgt) <= 50):
            continue
        if tgt.isdigit():          # 纯数字链接(如 [[10]]  footnote/列表) 非概念
            continue
        if tgt in DENY:
            continue
        if "日记" in tgt or "全景导航" in tgt or "Map of Content" in tgt:
            continue
        if tgt in nb or tgt in np_ or tgt in fp or tgt in dirs:
            continue
        candidates.append((tgt, c))
    candidates.sort(key=lambda x: -x[1])
    if args.max and args.max > 0:
        candidates = candidates[:args.max]

    created = []
    for tgt, c in candidates:
        safe = re.sub(r'[:/\\*?"<>|#^\[\]]', "_", tgt).strip()
        if not safe:
            continue
        path = OUT / f"{safe}.md"
        if path.exists():
            continue
        sources = sorted(set(refs.get(tgt, [])))[:6]
        body = [f"---\nprovenance: derived\ntype: concept-stub\nauto: true\n"
                f"created: {TODAY}\nrefs: {len(refs.get(tgt, []))}\n---",
                f"# {tgt}\n",
                f"> 由 self_evolve 自动生成的占位概念（被引用 {c} 次，来源尚未成稿）。\n"]
        if sources:
            body.append("\n## 引用来源\n")
            for s in sources:
                body.append(f"- [[{s}]]")
        body.append("\n\n_待补充：定义、与 iNEST/TCC 体系的关系、关键文献。_")
        path.write_text("\n".join(body), encoding="utf-8")
        created.append(tgt)
    print(f"候选缺失裸概念(≥{args.min_refs}引用): {len(candidates)}")
    print(f"本次重建占位笔记: {len(created)}")
    if created:
        print("样例:", created[:15])
    # 写一份报告供 self_evolve 参考
    report = {"date": TODAY, "candidates": len(candidates),
              "created": created, "total_broken": sum(broken_freq.values())}
    (VAULT / "99_Meta" / "heal_missing_concepts_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
