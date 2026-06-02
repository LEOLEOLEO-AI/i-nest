from __future__ import annotations

import datetime as dt
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

INBOX = ROOT / "00_Inbox"
OUTPUTS = ROOT / "30_Outputs"

KEYWORDS_MEETING = [
    "会议",
    "纪要",
    "启动会",
    "论坛",
    "汇报",
    "座谈",
    "讨论",
]

KEYWORDS_STRATEGY = [
    "战略",
    "规划",
    "建议",
    "建议书",
    "项目群",
    "布局",
    "交底书",
    "专利",
    "课题",
]


def _now() -> str:
    return dt.datetime.now().replace(microsecond=0).isoformat(sep=" ")


def _unique(path: Path) -> Path:
    if not path.exists():
        return path
    idx = 2
    while True:
        candidate = path.with_name(f"{path.stem} ({idx}){path.suffix}")
        if not candidate.exists():
            return candidate
        idx += 1


def _move(src: Path, dst: Path, log: list[str]) -> None:
    if not src.exists():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    final_dst = _unique(dst) if dst.exists() else dst
    shutil.move(str(src), str(final_dst))
    log.append(f"- 迁移 `{src.relative_to(ROOT)}` -> `{final_dst.relative_to(ROOT)}`")


def _move_dir_contents(src: Path, dst: Path, log: list[str]) -> None:
    if not src.exists():
        return
    dst.mkdir(parents=True, exist_ok=True)
    for item in list(src.iterdir()):
        _move(item, dst / item.name, log)
    try:
        src.rmdir()
    except OSError:
        pass


def _classify_note(path: Path) -> str:
    name = path.stem
    text = path.read_text(encoding="utf-8", errors="ignore")[:2000]
    sample = f"{name}\n{text}"
    if any(k in sample for k in KEYWORDS_MEETING):
        return "04_会议战略"
    if any(k in sample for k in KEYWORDS_STRATEGY):
        return "04_会议战略"
    return "03_研究资料"


def _refine_inbox(log: list[str]) -> None:
    for sub in [
        INBOX / "01_导入资料" / "DownloadImports",
        INBOX / "01_导入资料" / "Get",
        INBOX / "02_网页剪藏",
        INBOX / "03_研究资料",
        INBOX / "04_会议战略",
        INBOX / "05_历史遗留",
    ]:
        sub.mkdir(parents=True, exist_ok=True)

    _move_dir_contents(INBOX / "Clippings", INBOX / "02_网页剪藏", log)
    _move_dir_contents(INBOX / "根目录历史导入", INBOX / "05_历史遗留", log)
    _move_dir_contents(INBOX / "文献与碎片" / "Get", INBOX / "01_导入资料" / "Get", log)
    _move_dir_contents(INBOX / "文献与碎片" / "DownloadImports", INBOX / "01_导入资料" / "DownloadImports", log)

    loose_dir = INBOX / "文献与碎片"
    if loose_dir.exists():
        for p in sorted(loose_dir.glob("*.md")):
            bucket = _classify_note(p)
            _move(p, INBOX / bucket / p.name, log)
        try:
            loose_dir.rmdir()
        except OSError:
            pass


def _iter_md(base: Path) -> list[Path]:
    return sorted([p for p in base.rglob("*.md")], key=lambda x: str(x).lower())


def _write_index(path: Path, title: str, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = "\n".join([f"# {title}", "", f"生成时间：{_now()}", "", *lines, ""])
    path.write_text(content, encoding="utf-8", newline="\n")


def _build_outputs_indexes(log: list[str]) -> None:
    papers_dir = OUTPUTS / "论文"
    patents_dir = OUTPUTS / "专利"

    paper_files = [p for p in _iter_md(papers_dir) if p.name not in {"00_论文导航.md"}]
    patent_files = [p for p in _iter_md(patents_dir) if p.name not in {"00_专利导航.md"}] if patents_dir.exists() else []

    paper_lines = ["## 论文文件", ""]
    for p in paper_files:
        rel = p.relative_to(ROOT).with_suffix("")
        paper_lines.append(f"- [[{str(rel).replace(chr(92), '/')}]]")
    _write_index(papers_dir / "00_论文导航.md", "论文导航", paper_lines)
    log.append("- 生成 `30_Outputs/论文/00_论文导航.md`")

    patent_lines = ["## 专利文件", ""]
    if patent_files:
        for p in patent_files:
            rel = p.relative_to(ROOT).with_suffix("")
            patent_lines.append(f"- [[{str(rel).replace(chr(92), '/')}]]")
    else:
        patent_lines.append("- 暂无专利 Markdown 文件")
    _write_index(patents_dir / "00_专利导航.md", "专利导航", patent_lines)
    log.append("- 生成 `30_Outputs/专利/00_专利导航.md`")

    overview_lines = [
        "## 入口",
        "",
        "- [[30_Outputs/论文/00_论文导航|论文导航]]",
        "- [[30_Outputs/专利/00_专利导航|专利导航]]",
        "",
        "## 统计",
        "",
        f"- 论文 Markdown 数：{len(paper_files)}",
        f"- 专利 Markdown 数：{len(patent_files)}",
    ]
    _write_index(OUTPUTS / "00_成果总览.md", "成果总览", overview_lines)
    log.append("- 生成 `30_Outputs/00_成果总览.md`")


def _write_inbox_guide(log: list[str]) -> None:
    guide = INBOX / "00_Inbox 使用说明.md"
    lines = [
        "# 00_Inbox 使用说明",
        "",
        "生成时间：" + _now(),
        "",
        "## 二级入口",
        "",
        "- `01_导入资料`：脚本或外部文件批量导入的材料",
        "- `02_网页剪藏`：网页/阅读过程中的轻量剪藏",
        "- `03_研究资料`：尚未沉淀为 SSOT/项目/成果的研究型资料",
        "- `04_会议战略`：会议纪要、规划、建议、课题、战略材料",
        "- `05_历史遗留`：从旧结构保留的根目录历史笔记",
        "",
        "## 原则",
        "",
        "- Inbox 只做暂存，不做终态归档",
        "- 真正稳定的概念转入 `10_Knowledge`",
        "- 真正推进中的事项转入 `20_Projects`",
        "- 形成论文或专利后转入 `30_Outputs`",
        "",
    ]
    guide.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    log.append("- 生成 `00_Inbox/00_Inbox 使用说明.md`")


def _write_report(log: list[str]) -> None:
    report = ROOT / "90_System" / "重构报告_Inbox与成果二轮整理.md"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(
        "\n".join(
            [
                "# 重构报告：Inbox 与成果二轮整理",
                "",
                f"生成时间：{_now()}",
                "",
                "## 已执行动作",
                "",
                *log,
                "",
            ]
        ),
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    log: list[str] = []
    _refine_inbox(log)
    _build_outputs_indexes(log)
    _write_inbox_guide(log)
    _write_report(log)
    print("refined inbox and outputs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
