from __future__ import annotations

import datetime as dt
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

RESEARCH_DIR = ROOT / "00_Inbox" / "03_研究资料"
STRATEGY_DIR = ROOT / "00_Inbox" / "04_会议战略"
SSOT_DIR = ROOT / "10_Knowledge" / "SSOT"
ADR_DIR = ROOT / "20_Projects" / "ADR"
PAPERS_DIR = ROOT / "30_Outputs" / "论文"


@dataclass(frozen=True)
class ConceptRule:
    name: str
    priority: str
    target_file: str
    keywords: tuple[str, ...]
    action: str


@dataclass(frozen=True)
class DecisionRule:
    title: str
    priority: str
    adr_title: str
    keywords: tuple[str, ...]
    decision: str


SSOT_RULES: tuple[ConceptRule, ...] = (
    ConceptRule("NCC", "P0", "NCC - 网络中心计算.md", ("ncc", "网络中心计算", "network-centric", "网内计算"), "补齐严格定义、边界和与 SDI/AllReduce 的关系。"),
    ConceptRule("CST", "P0", "CST - 时空协同复杂度.md", ("cst", "复杂度", "时空协同", "临界", "相变"), "补齐公式、变量定义、阈值与测量口径。"),
    ConceptRule("SDI", "P0", "SDI - 软件定义互连.md", ("sdi", "软件定义互连", "软件定义互联", "interconnect", "互连"), "补齐物理机制、控制面和适用边界。"),
    ConceptRule("Chiplet", "P1", "Chiplet - 芯粒.md", ("chiplet", "芯粒", "先进封装", "2.5d", "3dic"), "沉淀工程载体、约束与与晶圆级路线的边界。"),
    ConceptRule("忆阻器网络", "P1", "忆阻器网络.md", ("忆阻", "memrist", "memristor"), "建立器件物理、可塑性与拓扑重构的统一条目。"),
    ConceptRule("主动推断与自由能原理", "P1", "主动推断与自由能原理.md", ("主动推断", "自由能", "active inference", "free energy"), "沉淀理论定义及其与 CST/具身智能的关系。"),
    ConceptRule("类脑与神经形态计算", "P1", "类脑与神经形态计算.md", ("类脑", "神经形态", "neuromorphic", "spiking", "脉冲"), "收敛类脑计算的工程定义、任务边界和器件路线。"),
    ConceptRule("晶圆级系统", "P1", "晶圆级系统.md", ("晶圆", "wafer", "wafer-scale", "晶上"), "统一晶圆级系统、晶上网络和 SDSoW 的术语。"),
    ConceptRule("小世界与层级模块性", "P2", "小世界与层级模块性.md", ("small-world", "小世界", "层级", "模块"), "沉淀复杂网络关键结构指标与测量方法。"),
    ConceptRule("拓扑映射", "P2", "拓扑映射.md", ("拓扑映射", "mapping", "allreduce", "alltoall", "reduce"), "把通信原语与物理拓扑的映射关系变成权威条目。"),
)


ADR_RULES: tuple[DecisionRule, ...] = (
    DecisionRule(
        "近期主线聚焦 NCC + SDI-CC",
        "P0",
        "ADR: 以 NCC + SDI-CC 作为 2026-2027 近期工程主线",
        ("ncc", "网络中心", "互连", "互联", "allreduce", "网内计算"),
        "短中期优先押注网络中心计算与 SDI-CC 互连体系，先形成可投稿、可验证、可工程化的主线成果。",
    ),
    DecisionRule(
        "统一采用 CST 作为理论与评价标尺",
        "P0",
        "ADR: 采用 CST 作为统一理论框架与评价指标",
        ("cst", "复杂度", "相变", "临界", "涌现"),
        "后续论文、项目和路线图统一用 CST 解释结构、动力学与耦合收益。",
    ),
    DecisionRule(
        "晶圆级系统与 SDSoW 作为中长期硬件路线",
        "P1",
        "ADR: 将晶圆级系统与 SDSoW 设为中长期硬件演进路线",
        ("晶圆", "wafer", "sdsow", "晶上", "系统"),
        "中长期硬件路线优先围绕晶圆级系统、晶上网络和 SDSoW 展开。",
    ),
    DecisionRule(
        "Chiplet/先进封装作为过渡落地载体",
        "P1",
        "ADR: 以 Chiplet 与先进封装作为近期工程落地载体",
        ("chiplet", "封装", "3dic", "2.5d", "异构集成"),
        "在晶圆级能力完全成熟前，以 Chiplet 和先进封装承接系统验证与产业化过渡。",
    ),
    DecisionRule(
        "忆阻器 + 类脑脉冲作为长期器件方向",
        "P1",
        "ADR: 将忆阻器与类脑脉冲网络设为长期器件路线",
        ("忆阻", "memrist", "类脑", "神经形态", "脉冲"),
        "长期器件路线优先考虑忆阻器、神经形态硬件与拓扑可塑性协同。",
    ),
    DecisionRule(
        "论文与项目按 A/B/C/D 分层推进",
        "P2",
        "ADR: 采用 A/B/C/D 分层推进论文与项目组合",
        ("路线图", "规划", "战略", "项目", "课题"),
        "将理论、互连、具身智能和专项成果拆分为不同时间线并滚动推进。",
    ),
)


PAPER_FILE_HINTS = {
    "A1": "30_Outputs/论文/A组_CST基础理论/论文计划列表",
    "A11": "30_Outputs/论文/CST_Intelligence_Emergence_Paper_V22_Engineering_Format",
    "B1": "30_Outputs/论文/B组_SDI-CC互连体系/P-Theory_v2_MetaTopology_SDI_Bond_Draft",
    "B2": "30_Outputs/论文/B组_SDI-CC互连体系/[V2] 论文框架_P-Mapping_5plus4完备物理拓扑映射",
    "B3": "30_Outputs/论文/B组_SDI-CC互连体系/P-Paradigm 综述论文大纲 (Nature Electronics)",
    "C1": "30_Outputs/论文/00_论文总清单",
    "C2": "30_Outputs/论文/00_论文总清单",
}


def _now() -> str:
    return dt.datetime.now().replace(microsecond=0).isoformat(sep=" ")


def _md_files(base: Path) -> list[Path]:
    return sorted([p for p in base.glob("*.md") if not p.name.startswith("00_")], key=lambda p: p.stem.lower())


def _read_title(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def _wikilink(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    return rel[:-3] if rel.endswith(".md") else rel


def _matches_by_keywords(paths: list[Path], keywords: tuple[str, ...]) -> list[Path]:
    hits: list[Path] = []
    lowers = [k.lower() for k in keywords]
    for path in paths:
        sample = path.stem.lower()
        if any(k in sample for k in lowers):
            hits.append(path)
    return hits


def _write_ssot_candidates() -> None:
    files = _md_files(RESEARCH_DIR)
    lines = [
        "# SSOT 候选概念清单",
        "",
        f"生成时间：{_now()}",
        "",
        "来源：`00_Inbox/03_研究资料`",
        "目的：把高频概念从输入层提升到 `10_Knowledge/SSOT`，减少重复命名和分散定义。",
        "",
        "## 候选列表",
        "",
        "| 优先级 | 概念 | 目标条目 | 当前状态 | 研究资料命中数 | 建议动作 |",
        "| --- | --- | --- | --- | ---: | --- |",
    ]
    detail_lines: list[str] = ["", "## 证据笔记", ""]
    for rule in SSOT_RULES:
        hits = _matches_by_keywords(files, rule.keywords)
        target = SSOT_DIR / rule.target_file
        status = "已建立，待补全" if target.exists() else "待创建"
        lines.append(
            f"| {rule.priority} | {rule.name} | `10_Knowledge/SSOT/{rule.target_file}` | {status} | {len(hits)} | {rule.action} |"
        )
        detail_lines.append(f"### {rule.name}")
        detail_lines.append("")
        if hits:
            for hit in hits[:6]:
                detail_lines.append(f"- [[{_wikilink(hit)}|{_read_title(hit)}]]")
        else:
            detail_lines.append("- 暂无明显标题命中，建议人工补充。")
        detail_lines.append("")
    (SSOT_DIR / "00_SSOT候选概念清单.md").write_text(
        "\n".join(lines + detail_lines),
        encoding="utf-8",
        newline="\n",
    )


def _write_adr_candidates() -> None:
    files = _md_files(STRATEGY_DIR)
    lines = [
        "# ADR 候选决策清单",
        "",
        f"生成时间：{_now()}",
        "",
        "来源：`00_Inbox/04_会议战略`",
        "目的：把会议、战略与规划材料收敛成可追踪的决策记录。",
        "",
        "## 候选列表",
        "",
        "| 优先级 | 决策主题 | 建议 ADR 标题 | 材料命中数 | 建议决策 |",
        "| --- | --- | --- | ---: | --- |",
    ]
    detail_lines: list[str] = ["", "## 证据笔记", ""]
    for rule in ADR_RULES:
        hits = _matches_by_keywords(files, rule.keywords)
        lines.append(f"| {rule.priority} | {rule.title} | `{rule.adr_title}` | {len(hits)} | {rule.decision} |")
        detail_lines.append(f"### {rule.title}")
        detail_lines.append("")
        if hits:
            for hit in hits[:6]:
                detail_lines.append(f"- [[{_wikilink(hit)}|{_read_title(hit)}]]")
        else:
            detail_lines.append("- 暂无明显标题命中，建议人工筛选会议材料补证据。")
        detail_lines.append("")
    (ADR_DIR / "00_ADR候选决策清单.md").write_text(
        "\n".join(lines + detail_lines),
        encoding="utf-8",
        newline="\n",
    )


def _quarter_key(text: str) -> tuple[int, int]:
    m = re.search(r"(20\d{2})\s*Q([1-4])", text)
    if not m:
        return (9999, 9)
    return (int(m.group(1)), int(m.group(2)))


def _paper_priority(status: str, due: str, note: str) -> str:
    combined = f"{status} {due} {note}"
    if "最先投稿" in combined or "全文初稿完成" in combined or "初稿完成" in combined:
        return "P0"
    if due.startswith("2026") or ("📝" in status and "2027 Q1" in due):
        return "P0"
    if "📝" in status or "📋" in status:
        return "P1"
    return "P2"


def _next_action(code: str, status: str) -> str:
    if "✅" in status:
        return "统一投稿版本、补 cover letter、锁定投稿清单。"
    if "全文初稿完成" in status:
        return "压缩结构、统一图表和实验段，进入投稿版清稿。"
    if "📝" in status:
        return "把现有草稿收敛成可审稿版本，补实验与参考文献。"
    if "📋" in status:
        return "从框架升级到正文 30% 以上，先补摘要、引言、方法。"
    if code.startswith("C"):
        return "先明确实验场景、硬件路线和投稿目标，再开写。"
    return "先补一页结构提纲和证据清单，避免长期停留在待启动。"


def _parse_paper_rows() -> list[dict[str, str]]:
    source = PAPERS_DIR / "00_论文总清单.md"
    rows: list[dict[str, str]] = []
    for line in source.read_text(encoding="utf-8", errors="ignore").splitlines():
        if not line.startswith("|"):
            continue
        if "---" in line or "编号" in line or "方向" in line or "题目（简称）" in line:
            continue
        parts = [part.strip().strip("*") for part in line.strip().split("|")[1:-1]]
        if len(parts) == 6:
            code, title, venue, due, status, note = parts
        elif len(parts) == 7:
            code, _alias, title, venue, due, status, note = parts
        elif len(parts) == 5:
            code, title, project, venue, status = parts
            due = ""
            note = project
        else:
            continue
        if not code:
            continue
        rows.append(
            {
                "code": code,
                "title": title,
                "venue": venue,
                "due": due,
                "status": status,
                "note": note,
            }
        )
    return rows


def _write_paper_board() -> None:
    rows = _parse_paper_rows()
    for row in rows:
        row["priority"] = _paper_priority(row["status"], row["due"], row["note"])
    rows.sort(key=lambda r: (r["priority"], _quarter_key(r["due"]), r["code"]))

    lines = [
        "# 论文优先级推进面板",
        "",
        f"生成时间：{_now()}",
        "",
        "来源：`30_Outputs/论文/00_论文总清单.md`",
        "规则：优先级由当前状态、投递时间和“最先投稿”信号综合确定。",
        "",
    ]
    for bucket in ("P0", "P1", "P2"):
        lines.extend([f"## {bucket}", ""])
        bucket_rows = [r for r in rows if r["priority"] == bucket]
        if not bucket_rows:
            lines.append("- 暂无")
            lines.append("")
            continue
        for row in bucket_rows:
            file_hint = PAPER_FILE_HINTS.get(row["code"])
            title_part = row["title"]
            if file_hint:
                title_part = f"[[{file_hint}|{row['code']} - {row['title']}]]"
            else:
                title_part = f"`{row['code']} - {row['title']}`"
            lines.append(f"- {title_part} | {row['status']} | {row['due'] or '未定'} | {row['venue']}")
            lines.append(f"- 下一步：{_next_action(row['code'], row['status'])}")
        lines.append("")

    lines.extend(
        [
            "## 建议节奏",
            "",
            "- 本周优先：先把 `P0` 全部推进到可投稿或可内部评审状态。",
            "- 本月目标：至少把 2 个 `P1` 项目推进到正文级草稿。",
            "- 储备管理：`P2` 只保留提纲和证据，不占用主线写作时间。",
            "",
        ]
    )
    (PAPERS_DIR / "00_论文优先级推进面板.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    ADR_DIR.mkdir(parents=True, exist_ok=True)
    _write_ssot_candidates()
    _write_adr_candidates()
    _write_paper_board()
    print("research boards built")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
