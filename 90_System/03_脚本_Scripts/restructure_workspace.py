from __future__ import annotations

import datetime as dt
import os
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

KEEP_ROOT_MD = {
    "AGENTS.md",
    "HEARTBEAT.md",
    "IDENTITY.md",
    "MEMORY.md",
    "SOUL.md",
    "TOOLS.md",
    "USER.md",
}

IGNORE_PARTS = {
    ".git",
    ".obsidian",
    ".smart-env",
    ".openclaw",
    ".neural_db",
    ".neural_memory",
}

TARGET_DIRS = [
    ROOT / "00_Inbox",
    ROOT / "10_Knowledge",
    ROOT / "20_Projects",
    ROOT / "30_Outputs",
    ROOT / "90_System",
]

DIR_MAPPINGS = [
    ("Clippings", "00_Inbox/Clippings"),
    ("00-索引", "10_Knowledge/00_导航"),
    ("00_KnowledgeBase_知识库/00_SSOT_权威条目", "10_Knowledge/SSOT"),
    ("00_KnowledgeBase_知识库/00_ADR_决策记录", "20_Projects/ADR"),
    ("00_KnowledgeBase_知识库/01_宏观规划与战略报告", "20_Projects/战略规划"),
    ("00_KnowledgeBase_知识库/02_CST_核心理论著作", "10_Knowledge/主题知识/CST_核心理论"),
    ("00_KnowledgeBase_知识库/03_Inbox_文献与碎片", "00_Inbox/文献与碎片"),
    ("00_KnowledgeBase_知识库/CST仿真平台", "20_Projects/CST仿真平台"),
    ("00_KnowledgeBase_知识库/知识库_网络超线性增益", "10_Knowledge/主题知识/网络超线性增益"),
    ("01_Ideas_想法", "20_Projects/Ideas"),
    ("05_Projects_项目", "20_Projects/Projects"),
    ("02_Papers_论文", "30_Outputs/论文"),
    ("01-专利", "30_Outputs/专利"),
    ("02-指南", "90_System/指南"),
    ("03-设计", "90_System/设计"),
    ("04-测试", "90_System/测试"),
]


def _now() -> str:
    return dt.datetime.now().replace(microsecond=0).isoformat(sep=" ")


def _log(report: list[str], text: str) -> None:
    report.append(f"- {text}")


def _unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    idx = 2
    while True:
        candidate = parent / f"{stem} ({idx}){suffix}"
        if not candidate.exists():
            return candidate
        idx += 1


def _merge_move(src: Path, dst: Path, report: list[str]) -> None:
    if not src.exists():
        return
    dst.mkdir(parents=True, exist_ok=True)
    for item in list(src.iterdir()):
        target = dst / item.name
        if item.is_dir():
            if target.exists() and target.is_dir():
                _merge_move(item, target, report)
                try:
                    item.rmdir()
                except OSError:
                    pass
            else:
                shutil.move(str(item), str(target))
        else:
            final_target = _unique_path(target) if target.exists() else target
            shutil.move(str(item), str(final_target))
    try:
        src.rmdir()
        _log(report, f"删除空目录 `{src.relative_to(ROOT)}`")
    except OSError:
        pass


def _strip_frontmatter(lines: list[str]) -> list[str]:
    if len(lines) >= 2 and lines[0].strip() == "---":
        for idx in range(1, len(lines)):
            if lines[idx].strip() == "---":
                return lines[idx + 1 :]
    return lines


def _extract_title(text: str, path: Path) -> str:
    lines = _strip_frontmatter(text.splitlines())
    for line in lines:
        s = line.strip()
        if s.startswith("# "):
            return s[2:].strip().strip("*").strip()
    for line in lines:
        s = line.strip().strip("*").strip()
        if not s:
            continue
        if s.startswith((">", "-", "*", "`", "|")):
            continue
        return s[:120]
    if path.name.lower() == "readme.md":
        parent = re.sub(r"^[0-9]+[_-]?", "", path.parent.name).strip("_- ")
        parent = parent or "目录"
        return f"{parent} 目录说明"
    return path.stem


def _clean_name(name: str) -> str:
    name = name.replace("_", " ")
    name = re.sub(r"\s+", " ", name)
    name = re.sub(r'[<>:"/\\|?*]+', " ", name)
    name = re.sub(r"\s+\.\s+", ". ", name)
    name = re.sub(r"\s{2,}", " ", name).strip(" .-_")
    return name[:120] or "未命名笔记"


def _separator_ratio(name: str) -> float:
    if not name:
        return 0.0
    sep_count = sum(1 for ch in name if ch in "_-()[]")
    return sep_count / max(len(name), 1)


def _is_weak_name(path: Path) -> bool:
    stem = path.stem
    low = stem.lower()
    if path.name.lower() == "readme.md":
        return True
    if low.startswith("untitled"):
        return True
    if "无标题" in stem:
        return True
    if re.search(r" \(\d+\)$", stem):
        return True
    if re.search(r"_\d+$", stem):
        return True
    if _separator_ratio(stem) >= 0.16:
        return True
    return False


def _rename_from_content(path: Path, report: list[str]) -> None:
    if path.name in KEEP_ROOT_MD:
        return
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return
    if not text.strip():
        path.unlink()
        _log(report, f"删除空文件 `{path.relative_to(ROOT)}`")
        return
    if not _is_weak_name(path):
        return
    title = _clean_name(_extract_title(text, path))
    if not title or title == path.stem:
        return
    target = _unique_path(path.with_name(f"{title}{path.suffix}"))
    shutil.move(str(path), str(target))
    _log(report, f"重命名 `{path.relative_to(ROOT)}` -> `{target.relative_to(ROOT)}`")


def _move_root_loose_notes(report: list[str]) -> None:
    inbox_root = ROOT / "00_Inbox" / "根目录历史导入"
    inbox_root.mkdir(parents=True, exist_ok=True)
    for p in sorted(ROOT.glob("*.md")):
        if p.name in KEEP_ROOT_MD:
            continue
        target = _unique_path(inbox_root / p.name)
        shutil.move(str(p), str(target))
        _log(report, f"迁移根目录笔记 `{p.name}` -> `{target.relative_to(ROOT)}`")


def _move_legacy_scripts(report: list[str]) -> None:
    scripts_root = ROOT / "90_System" / "脚本"
    scripts_root.mkdir(parents=True, exist_ok=True)
    for name in ["init_vault.bat", "fix_gitee_auth.bat", "kb_engine.py"]:
        p = ROOT / name
        if not p.exists():
            continue
        target = _unique_path(scripts_root / p.name)
        shutil.move(str(p), str(target))
        _log(report, f"迁移脚本 `{p.name}` -> `{target.relative_to(ROOT)}`")


def _move_legacy_kb_root(report: list[str]) -> None:
    kb_root = ROOT / "00_KnowledgeBase_知识库"
    if not kb_root.exists():
        return

    legacy_obsidian = kb_root / ".obsidian"
    if legacy_obsidian.exists():
        dst = ROOT / "90_System" / "legacy_subvault_obsidian"
        _merge_move(legacy_obsidian, dst, report)

    nav_root = ROOT / "10_Knowledge" / "00_导航"
    archive_root = ROOT / "10_Knowledge" / "专题归档"
    for item in list(kb_root.iterdir()):
        if item.name in {".obsidian"}:
            continue
        if item.is_file() and item.suffix.lower() == ".md":
            target = _unique_path(nav_root / item.name)
            nav_root.mkdir(parents=True, exist_ok=True)
            shutil.move(str(item), str(target))
            _log(report, f"迁移知识库根笔记 `{item.relative_to(ROOT)}` -> `{target.relative_to(ROOT)}`")
        elif item.is_dir():
            target = archive_root / item.name
            _merge_move(item, target, report)
            _log(report, f"迁移遗留专题目录 `{item.relative_to(ROOT)}` -> `{target.relative_to(ROOT)}`")
        else:
            target = _unique_path((ROOT / "90_System" / "杂项") / item.name)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(item), str(target))
            _log(report, f"迁移遗留文件 `{item.relative_to(ROOT)}` -> `{target.relative_to(ROOT)}`")

    try:
        kb_root.rmdir()
        _log(report, "删除空目录 `00_KnowledgeBase_知识库`")
    except OSError:
        pass


def _run_dir_mappings(report: list[str]) -> None:
    for src_rel, dst_rel in DIR_MAPPINGS:
        src = ROOT / src_rel
        dst = ROOT / dst_rel
        if not src.exists():
            continue
        _merge_move(src, dst, report)
        _log(report, f"目录重组 `{src_rel}` -> `{dst_rel}`")


def _rename_pass(report: list[str]) -> None:
    for p in sorted(ROOT.rglob("*.md")):
        try:
            rel = p.relative_to(ROOT)
        except ValueError:
            continue
        if any(part in IGNORE_PARTS for part in rel.parts):
            continue
        if "copilot-conversations" in rel.parts:
            continue
        if p.name in KEEP_ROOT_MD and len(rel.parts) == 1:
            continue
        _rename_from_content(p, report)


def _write_guide(report: list[str]) -> None:
    guide = ROOT / "10_Knowledge" / "00_导航" / "最简知识库目录说明.md"
    guide.parent.mkdir(parents=True, exist_ok=True)
    guide.write_text(
        "\n".join(
            [
                "# 最简知识库目录说明",
                "",
                "> 按照至简原则，目录只承担最小分类职责，真正的检索依赖文件名、链接、搜索与 Wiki。",
                "",
                "## 顶层主干",
                "",
                "- `00_Inbox`：所有新输入、网页剪藏、下载导入、待整理材料",
                "- `10_Knowledge`：稳定知识、概念、索引、SSOT、主题知识",
                "- `20_Projects`：研究规划、想法、项目、ADR、战略推进",
                "- `30_Outputs`：论文、专利、面向交付的成果",
                "- `90_System`：脚本、设计、测试、系统性文档",
                "",
                "## 原则",
                "",
                "- 少建目录，多用文件名和链接",
                "- 新内容先进入 `00_Inbox`，整理后再转入长期层",
                "- 概念统一放 `10_Knowledge/SSOT`",
                "- 决策统一放 `20_Projects/ADR`",
                "- 论文与专利统一沉淀到 `30_Outputs`",
                "",
            ]
        ),
        encoding="utf-8",
        newline="\n",
    )
    _log(report, f"写入目录说明 `{guide.relative_to(ROOT)}`")


def _write_report(report: list[str]) -> Path:
    report_path = ROOT / "90_System" / "重构报告_目录优化.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# 重构报告：目录优化",
        "",
        f"生成时间：{_now()}",
        "",
        "## 已执行动作",
        "",
        *report,
        "",
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    return report_path


def main() -> int:
    report: list[str] = []
    for p in TARGET_DIRS:
        p.mkdir(parents=True, exist_ok=True)

    _run_dir_mappings(report)
    _move_legacy_kb_root(report)
    _move_root_loose_notes(report)
    _move_legacy_scripts(report)
    _rename_pass(report)
    _write_guide(report)
    report_path = _write_report(report)
    print(f"Workspace restructured. Report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
