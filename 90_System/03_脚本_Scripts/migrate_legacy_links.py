from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

IGNORE_PARTS = {
    ".git",
    ".obsidian",
    ".smart-env",
    ".openclaw",
    ".neural_db",
    ".neural_memory",
}

SKIP_FILES = {
    ROOT / "04_Code_代码" / "restructure_workspace.py",
}

REPLACEMENTS = [
    ("10_Knowledge/00_导航/Wiki/", "10_Knowledge/00_导航/Wiki/"),
    ("10_Knowledge/00_导航/研究方向_NCC", "10_Knowledge/00_导航/研究方向_NCC"),
    ("10_Knowledge/00_导航/研究方向_INEST", "10_Knowledge/00_导航/研究方向_INEST"),
    ("10_Knowledge/00_导航/研究建议_NCC×INEST", "10_Knowledge/00_导航/研究建议_NCC×INEST"),
    ("10_Knowledge/00_导航/术语对照表", "10_Knowledge/00_导航/术语对照表"),
    ("10_Knowledge/00_导航/文档依赖图", "10_Knowledge/00_导航/文档依赖图"),
    ("10_Knowledge/00_导航/Get笔记×Obsidian 配置与工作流", "10_Knowledge/00_导航/Get笔记×Obsidian 配置与工作流"),
    ("10_Knowledge/00_导航/", "10_Knowledge/00_导航/"),
    ("10_Knowledge/SSOT/", "10_Knowledge/SSOT/"),
    ("20_Projects/ADR/", "20_Projects/ADR/"),
    ("20_Projects/战略规划/", "20_Projects/战略规划/"),
    ("10_Knowledge/主题知识/CST_核心理论/", "10_Knowledge/主题知识/CST_核心理论/"),
    ("00_Inbox/文献与碎片/", "00_Inbox/文献与碎片/"),
    ("20_Projects/CST仿真平台/CST仿真平台", "20_Projects/CST仿真平台/CST仿真平台"),
    ("20_Projects/CST仿真平台/", "20_Projects/CST仿真平台/"),
    ("10_Knowledge/主题知识/网络超线性增益/", "10_Knowledge/主题知识/网络超线性增益/"),
    ("10_Knowledge/00_导航/00_iNEST_全景知识图谱", "10_Knowledge/00_导航/00_iNEST_全景知识图谱"),
    ("10_Knowledge/00_导航/00_宽屏目录仪表盘", "10_Knowledge/00_导航/00_宽屏目录仪表盘"),
    ("30_Outputs/论文/", "30_Outputs/论文/"),
    ("30_Outputs/专利/", "30_Outputs/专利/"),
    ("20_Projects/Ideas/", "20_Projects/Ideas/"),
    ("20_Projects/Projects/", "20_Projects/Projects/"),
    ("90_System/指南/", "90_System/指南/"),
    ("90_System/设计/", "90_System/设计/"),
    ("90_System/测试/", "90_System/测试/"),
    ("00_Inbox/Clippings/", "00_Inbox/00_Inbox/Clippings/"),
    ("10_Knowledge/SSOT/00 SSOT 权威条目", "10_Knowledge/SSOT/00 SSOT 权威条目"),
    ("20_Projects/ADR/00 ADR 决策记录", "20_Projects/ADR/00 ADR 决策记录"),
]


def _should_skip(path: Path) -> bool:
    if path in SKIP_FILES:
        return True
    try:
        rel = path.relative_to(ROOT)
    except ValueError:
        return True
    if any(part in IGNORE_PARTS for part in rel.parts):
        return True
    if "copilot-conversations" in rel.parts:
        return True
    return False


def main() -> int:
    updated = 0
    scanned = 0
    for pattern in ("**/*.md", "**/*.py", "**/*.bat"):
        for path in ROOT.glob(pattern):
            if _should_skip(path):
                continue
            scanned += 1
            text = path.read_text(encoding="utf-8", errors="ignore")
            new_text = text
            for old, new in REPLACEMENTS:
                new_text = new_text.replace(old, new)
            if new_text != text:
                path.write_text(new_text, encoding="utf-8", newline="\n")
                updated += 1
    print(f"scanned={scanned} updated={updated}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
