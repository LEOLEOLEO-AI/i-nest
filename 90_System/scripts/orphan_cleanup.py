#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
orphan_cleanup.py — 孤儿笔记专项清理（P1 元进化提案执行）

孤儿定义（与 self_evolve.analyze_links 一致）：全库中"无入链"的 md 笔记
（没有被任何其他笔记 [[引用]]，排除 .git/.smart-env 等系统目录）。

策略（不删除任何内容，只移动/标记/链接）：
  1. 空文件/过短（<100 字节）→ 移入 80_Archive/_duplicates_archive/90_System/stubs/
  2. 有内容的孤儿 → 在文件末尾添加 "## 来源回链" 指向所属一级目录的 MOC
     （使笔记获得入链，消除孤岛；MOC 存在才链接，不存在则仅标记 orphan tag）
  3. 输出统计报告到 99_Meta/orphan_cleanup_report.md

用法:
    python orphan_cleanup.py --dry-run   # 仅统计不修改
    python orphan_cleanup.py             # 执行
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

VAULT = Path(r"D:\Obsidian\vault")
STUB_ARCHIVE = VAULT / "80_Archive" / "_duplicates_archive" / "90_System" / "stubs"
REPORT = VAULT / "99_Meta" / "orphan_cleanup_report.md"

# 系统目录/不应处理的目录
EXCLUDE_PREFIX = (".git", ".smart-env", ".obsidian", ".trash", "node_modules", ".venv")
EXCLUDE_SUBSTR = ("/_vendor/", "licenses", "dist-info")
# 个人杂物类（不链接 MOC，仅标记）
PERSONAL_MISC = ("保险", "今日备忘", "电脑密码", "简历", "好工具", "读书会", "日记")
# 一级目录 -> 建议回链的 MOC 候选
MOC_MAP = {
    "00_Inbox": ["Home"],
    "10_Knowledge": ["Home", "10_Knowledge"],
    "20_Processing": ["Home"],
    "30_TCC": ["TCC_Master_Index", "TCC-MOC", "TCC_iNEST_成果全景"],
    "40_iNEST": ["iNEST_Master_Index", "iNEST-MOC", "TCC_iNEST_成果全景"],
    "50_Output": ["Home", "TCC_iNEST_成果全景"],
    "60_MOC": ["Home"],
    "90_System": ["Home"],
    "99_Meta": ["Home"],
    "70_Dashboard": ["Home"],
    "wiki": ["Home"],
}
SIZE_MIN = 100


def scan():
    """返回 (notes, outgoing) — notes: {relpath: {stem, text, size, dir}}, outgoing: {stem: {targets}}"""
    link_re = re.compile(r"\[\[([^\]]+)\]\]")
    notes = {}
    for f in VAULT.rglob("*.md"):
        rel = f.relative_to(VAULT).as_posix()
        if any(rel.startswith(p) for p in EXCLUDE_PREFIX):
            continue
        if any(s in rel for s in EXCLUDE_SUBSTR):
            continue
        if "/." in rel or rel.startswith("."):
            continue
        try:
            txt = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        notes[rel] = {
            "stem": f.stem,
            "text": txt,
            "size": len(txt.encode("utf-8")),
            "dir": rel.split("/")[0],
            "path": f,
        }
    outgoing = defaultdict(set)
    for rel, info in notes.items():
        for m in link_re.findall(info["text"]):
            tgt = m.split("|")[0].split("#")[0].strip()
            if tgt:
                outgoing[info["stem"]].add(tgt)
    incoming = defaultdict(int)
    for stem, targets in outgoing.items():
        for t in targets:
            incoming[t] += 1
    return notes, outgoing, incoming


def find_moc(dirname, notes):
    """在 notes 中找 MOC 候选文件的完整 stem（精确匹配，避免误链）。"""
    for rel, info in notes.items():
        if info["dir"] != dirname:
            continue
        for cand in MOC_MAP.get(dirname, []):
            if info["stem"] == cand:
                return info["stem"]
    return None


def main():
    dry = "--dry-run" in sys.argv
    notes, outgoing, incoming = scan()
    orphans = []
    for rel, info in notes.items():
        if info["stem"] not in incoming and len(outgoing.get(info["stem"], ())) == 0:
            orphans.append((rel, info))
    orphans.sort(key=lambda x: x[1]["size"])

    stub_archived = []
    linked = []
    skipped = []
    JUNK_PATTERNS = ("无标题笔记", "SKILL_inbox", "无标题")
    EXCLUDED = set()
    for rel, info in orphans:
        is_junk = any(jp in info["stem"] for jp in JUNK_PATTERNS)
        if info["size"] < SIZE_MIN or is_junk:
            stub_archived.append(rel)
            if not dry:
                dst = STUB_ARCHIVE / info["path"].name
                STUB_ARCHIVE.mkdir(parents=True, exist_ok=True)
                # 防止重名
                if dst.exists():
                    dst = STUB_ARCHIVE / f"{info['path'].stem}_{info['path'].stat().st_mtime_ns}.md"
                info["path"].rename(dst)
            continue
        is_personal = any(pm in info["stem"] for pm in PERSONAL_MISC)
        if is_personal:
            stub_archived.append(rel)
            if not dry:
                dst = STUB_ARCHIVE / info["path"].name
                STUB_ARCHIVE.mkdir(parents=True, exist_ok=True)
                if dst.exists():
                    dst = STUB_ARCHIVE / f"{info['path'].stem}_{info['path'].stat().st_mtime_ns}.md"
                info["path"].rename(dst)
            continue
        moc = find_moc(info["dir"], notes)
        if moc is not None:
            linked.append((rel, moc))
            if not dry:
                marker = "\n\n<!-- orphan-cleanup: linked to MOC -->\n## 来源回链\n\n- [[{moc}]]\n"
                if "orphan-cleanup" not in info["text"]:
                    with info["path"].open("a", encoding="utf-8") as fh:
                        fh.write(marker.format(moc=moc))
        else:
            skipped.append(rel)
            if not dry:
                marker = "\n\n<!-- orphan-cleanup: no MOC found, tagged -->\n"
                if "orphan-cleanup" not in info["text"]:
                    with info["path"].open("a", encoding="utf-8") as fh:
                        fh.write(marker)

    # 报告
    lines = [
        f"# 孤儿笔记清理报告（{__import__('datetime').date.today()}）",
        "",
        f"模式: {'DRY-RUN（未修改）' if dry else '已执行'}",
        f"孤儿总数: {len(orphans)}",
        f"- 空/过短归档: {len(stub_archived)}",
        f"- 已链接 MOC: {len(linked)}",
        f"- 无 MOC 标记: {len(skipped)}",
        "",
        "## 归档的 stub（前 30）",
    ]
    lines += [f"- {r}" for r in stub_archived[:30]]
    lines += ["", "## 已链接的孤儿（前 30）"]
    lines += [f"- {r} → [[{m}]]" for r, m in linked[:30]]
    lines += ["", "## 无 MOC 标记（前 20）"]
    lines += [f"- {r}" for r in skipped[:20]]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"孤儿 {len(orphans)} | 归档 {len(stub_archived)} | 链接 {len(linked)} | 标记 {len(skipped)} | 报告: {REPORT}")


if __name__ == "__main__":
    main()
