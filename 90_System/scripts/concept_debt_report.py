#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""concept_debt_report.py — wiki 概念层负债盘点（只报告，不改动任何文件）。

为什么不是"自动归档脚本"（一次实测推翻的设计）:
    初版脚本的判据是"auto:true **且** 无入链"，据此可安全移动而不产生断链。
    实跑结果为 **0 个** —— 因为 self_evolve.step_grow_missing_concepts 生成占位
    笔记的**动机本身就是**"某个 [[链接]] 指向了不存在的概念"，所以这些占位
    按构造必然有入链。真正无入链的 2921 个反而不带 auto 标记（是 wiki_compiler
    从论文里抽的），属于另一类问题。
    结论: 不存在"既安全又有量"的自动归档集合。标题污染的那 3103 个都有入链，
    移走会制造 3103 条断链；正确处理要改写引用方，属研究内容判断。
    因此本脚本**只盘点、不改动**，把判断交给人。

输出: vault/99_Meta/concept_debt_report.md
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

VAULT = Path(r"D:\Obsidian\vault")
CONCEPTS = VAULT / "wiki" / "concepts"
OUT = VAULT / "99_Meta" / "concept_debt_report.md"
TITLE_LIKE_RE = re.compile(r"[\u4e00-\u9fff]|：|，|（|\)")


def load_orphans() -> set:
    sys.path.insert(0, str(VAULT / "90_System" / "scripts"))
    import self_evolve  # noqa: PLC0415
    nb, np_, fp, dirs, broken_freq, orphans, missing_fm = self_evolve.analyze_links()
    return set(orphans)


def main():
    print("全库链接解析中（约 1 分钟）...")
    orphans = load_orphans()

    buckets = {
        "stub_linked": [],      # auto 占位 + 有入链  -> 移走会断链
        "stub_orphan": [],      # auto 占位 + 无入链  -> 可安全归档
        "real_orphan": [],      # 非 auto + 无入链   -> 未成稿/未链接
        "real_linked": [],      # 非 auto + 有入链   -> 正常概念
    }
    for f in CONCEPTS.glob("*.md"):
        try:
            head = f.read_text(encoding="utf-8", errors="ignore")[:400]
        except Exception:
            continue
        is_auto = "auto: true" in head
        is_orphan = f.stem in orphans
        key = ("stub_" if is_auto else "real_") + ("orphan" if is_orphan else "linked")
        buckets[key].append(f)

    total = sum(len(v) for v in buckets.values())
    title_like = [f for f in buckets["stub_linked"] + buckets["stub_orphan"]
                  if TITLE_LIKE_RE.search(f.stem) or len(f.stem) > 25]

    L = ["# Wiki 概念层负债盘点", "",
         f"**生成**: {datetime.now():%Y-%m-%d %H:%M}  ·  由 `concept_debt_report.py` 生成",
         "", "> 本报告**只盘点、不改动**任何文件。归档决策需人工做，原因见文末。", "",
         "## 一、四象限", "",
         "| 类别 | 数量 | 占比 | 含义 | 可否自动处理 |",
         "|---|---|---|---|---|",
         f"| 占位且**有入链** | {len(buckets['stub_linked'])} | {100*len(buckets['stub_linked'])/max(total,1):.1f}% | "
         f"auto:true 占位，被别的笔记引用着 | ❌ 移走会断链 |",
         f"| 占位且**无入链** | {len(buckets['stub_orphan'])} | {100*len(buckets['stub_orphan'])/max(total,1):.1f}% | "
         f"可安全归档 | ✅ |",
         f"| 非占位且无入链 | {len(buckets['real_orphan'])} | {100*len(buckets['real_orphan'])/max(total,1):.1f}% | "
         f"编译器从论文抽出但未被引用 | ⚠️ 需判断价值 |",
         f"| 非占位且有入链 | {len(buckets['real_linked'])} | {100*len(buckets['real_linked'])/max(total,1):.1f}% | "
         f"正常概念 | — |",
         "",
         f"**概念文件总数**: {total}",
         f"**其中文件名近似文章标题**（占位类内）: {len(title_like)}",
         f"**全库无入链笔记(stem)**: {len(orphans)}",
         "",
         "## 二、为什么不能自动归档",
         "",
         "初版脚本按「`auto:true` **且** 无入链」筛出可安全移动的集合，实跑结果为 **0**。",
         "原因是 `self_evolve.step_grow_missing_concepts` 生成占位的动机本身就是",
         "「某个 `[[链接]]` 指向了不存在的概念」——这些占位**按构造必然有入链**。",
         "因此不存在「既安全又有量」的自动归档集合：",
         "",
         "- 标题污染的那批（约 3100 个）都有入链，移走会制造同等数量的断链；",
         "- 真正无入链的 2921 个大多不带 `auto` 标记，是编译器从论文抽的概念页，",
         "  「没人链接」不等于「没价值」，删掉是丢知识。",
         "",
         "正确做法是**先治源头、再谈清理**：冻结守卫已经止住新增（无新来源不再长概念），",
         "接下来可选：① 把占位从 `index.md`/统计里单列，让水位可见；",
         "② 对高频引用的占位人工补定义（把占位变成真概念）；",
         "③ 对确认无意义的引入，改写引用方后再移走。",
         "",
         "## 三、样例（各取 15 个，供人工判断）", ""]

    for key, label in [("stub_linked", "占位且有入链（标题型优先）"),
                       ("stub_orphan", "占位且无入链（可安全归档）"),
                       ("real_orphan", "非占位且无入链")]:
        L.append(f"### {label} — {len(buckets[key])} 个")
        L.append("")
        files = buckets[key]
        if key == "stub_linked":
            files = [f for f in files if TITLE_LIKE_RE.search(f.stem) or len(f.stem) > 25] or files
        for f in sorted(files, key=lambda x: x.stem)[:15]:
            L.append(f"- `{f.name}`")
        if len(files) > 15:
            L.append(f"- … 其余 {len(files)-15} 个")
        L.append("")

    OUT.write_text("\n".join(L), encoding="utf-8")

    print(f"\n概念总数 {total}")
    for k, v in buckets.items():
        print(f"  {k:<14} {len(v)}")
    print(f"标题型(占位内)  {len(title_like)}")
    print(f"\n报告 -> {OUT}")

    summary = {"generated": datetime.now().isoformat(), "total": total,
               "buckets": {k: len(v) for k, v in buckets.items()},
               "title_like_in_stubs": len(title_like)}
    (VAULT / "99_Meta" / "concept_debt_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
