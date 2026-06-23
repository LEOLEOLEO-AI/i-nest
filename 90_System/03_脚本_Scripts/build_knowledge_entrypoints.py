from __future__ import annotations

import datetime as dt
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

RESEARCH_DIR = ROOT / "00_Inbox" / "03_研究资料"
STRATEGY_DIR = ROOT / "00_Inbox" / "04_会议战略"
SSOT_DIR = ROOT / "10_Knowledge" / "SSOT"


RESEARCH_GROUPS = {
    "类脑与神经形态": ["类脑", "神经", "neuromorphic", "brain", "snn", "spiking", "plasticity", "neuron"],
    "复杂性与涌现": ["复杂", "涌现", "complex", "critical", "free energy", "自由能", "混沌", "拓扑", "network"],
    "Chiplet与互联": ["chiplet", "芯粒", "互联", "互连", "wafer", "晶圆", "smartnic", "hpc", "rdma", "noc", "interconnect"],
    "AI与模型": ["ai", "人工智能", "llm", "大模型", "智能", "agent", "transformer", "具身"],
}

STRATEGY_GROUPS = {
    "会议与纪要": ["会议", "纪要", "启动会", "论坛", "座谈", "讨论", "汇报"],
    "战略与规划": ["战略", "规划", "布局", "路线图", "十年", "方向"],
    "项目与建议": ["项目", "建议", "建议书", "课题", "专项", "交底", "申报"],
    "政策与产业": ["政策", "产业", "基金", "行动方案", "白皮书", "院士", "大会"],
}

SSOT_SEEDS = [
    {
        "file_name": "NCC - 网络中心计算.md",
        "title": "NCC",
        "aliases": ["网络中心计算", "Network-Centric Computing"],
        "links": [
            "10_Knowledge/主题知识/CST_核心理论/NCC_Core_Concepts",
            "10_Knowledge/00_导航/研究方向_NCC",
            "30_Outputs/论文/B组_SDI-CC互连体系/SDI-CC论文框架_拓扑即计算新范式",
        ],
    },
    {
        "file_name": "INEST - 复杂网络智能涌现.md",
        "title": "INEST",
        "aliases": ["iNEST", "复杂网络智能涌现"],
        "links": [
            "10_Knowledge/00_导航/研究方向_INEST",
            "10_Knowledge/00_导航/00_iNEST_全景知识图谱",
            "20_Projects/战略规划/iNEST_Academic_Belief_Core",
        ],
    },
    {
        "file_name": "CST - 时空协同复杂度.md",
        "title": "CST",
        "aliases": ["时空协同复杂度", "Complexity in Space-Time"],
        "links": [
            "10_Knowledge/主题知识/CST_核心理论/NCC_Core_Concepts",
            "00_Inbox/03_研究资料/网络时空协同复杂度涌现智能",
            "30_Outputs/论文/CST_Intelligence_Emergence_Paper_V22_Engineering_Format",
        ],
    },
    {
        "file_name": "SDI - 软件定义互连.md",
        "title": "SDI",
        "aliases": ["软件定义互连", "软件定义互联", "Software-Defined Interconnect"],
        "links": [
            "00_Inbox/04_会议战略/面向万亿参数大模型训练的SDI_软件定义互联___网内原生_AI_通信加速系统",
            "00_Inbox/03_研究资料/晶圆级SDI互联架构与最优扇出高维拓扑_面向大模型的网内计算设计",
            "30_Outputs/论文/B组_SDI-CC互连体系/SDI-CC论文框架_拓扑即计算新范式",
        ],
    },
    {
        "file_name": "Chiplet - 芯粒.md",
        "title": "Chiplet",
        "aliases": ["芯粒", "Chiplets"],
        "links": [
            "00_Inbox/03_研究资料/Chiplet最强科普",
            "00_Inbox/03_研究资料/Chiplet的机遇与挑战",
            "00_Inbox/03_研究资料/Chiplet先进封装全球格局",
        ],
    },
]


def _now() -> str:
    return dt.datetime.now().replace(microsecond=0).isoformat(sep=" ")


def _note_link(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel.endswith(".md"):
        rel = rel[:-3]
    return rel


def _read_title(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("# "):
            return s[2:].strip()
    return path.stem


def _top_recent(paths: list[Path], limit: int = 30) -> list[Path]:
    return sorted(paths, key=lambda p: p.stat().st_mtime, reverse=True)[:limit]


def _bucket(paths: list[Path], groups: dict[str, list[str]]) -> dict[str, list[Path]]:
    out = {k: [] for k in groups}
    out["其他"] = []
    for path in paths:
        name = path.stem.lower()
        matched = False
        for group, keywords in groups.items():
            if any(k.lower() in name for k in keywords):
                out[group].append(path)
                matched = True
                break
        if not matched:
            out["其他"].append(path)
    return out


def _render_bucket_section(title: str, items: list[Path], limit: int = 40) -> list[str]:
    lines = [f"## {title}", ""]
    if not items:
        lines.append("- 暂无")
        lines.append("")
        return lines
    for path in sorted(items, key=lambda p: p.stem.lower())[:limit]:
        lines.append(f"- [[{_note_link(path)}|{_read_title(path)}]]")
    if len(items) > limit:
        lines.append(f"- ... 其余 {len(items) - limit} 篇请用搜索或 Dataview 继续过滤")
    lines.append("")
    return lines


def _write_nav_page(target: Path, title: str, intro: str, paths: list[Path], groups: dict[str, list[str]]) -> None:
    buckets = _bucket(paths, groups)
    lines = [
        f"# {title}",
        "",
        f"生成时间：{_now()}",
        "",
        intro,
        "",
        f"- 当前条目数：{len(paths)}",
        "",
        "## 最近更新",
        "",
    ]
    for path in _top_recent(paths):
        lines.append(f"- [[{_note_link(path)}|{_read_title(path)}]]")
    lines.append("")
    for bucket_name, _ in groups.items():
        lines.extend(_render_bucket_section(bucket_name, buckets[bucket_name]))
    lines.extend(_render_bucket_section("其他", buckets["其他"], limit=30))
    target.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def _write_ssot_seed(seed: dict[str, object]) -> Path:
    path = SSOT_DIR / str(seed["file_name"])
    if path.exists():
        return path
    aliases = seed["aliases"]
    links = seed["links"]
    content = [
        "---",
        "type: ssot",
        "aliases:",
        *[f"  - {alias}" for alias in aliases],
        "tags:",
        "  - ssot",
        "---",
        "",
        f"# {seed['title']}",
        "",
        "## 定义",
        "",
        "待补充。",
        "",
        "## 边界与非例",
        "",
        "待补充。",
        "",
        "## 关键结论",
        "",
        "待补充。",
        "",
        "## 关联条目",
        "",
        *[f"- [[{link}]]" for link in links],
        "",
        "## 证据与来源",
        "",
        "待补充。",
        "",
    ]
    path.write_text("\n".join(content), encoding="utf-8", newline="\n")
    return path


def _write_ssot_index(seed_paths: list[Path]) -> None:
    lines = [
        "# 00_SSOT_权威条目",
        "",
        "这里放“单一真相源”（SSOT）：",
        "- 权威定义",
        "- 指标基线",
        "- 统一术语",
        "- 可复用结论",
        "",
        "其他笔记只引用/嵌入这里的段落或块，不复制粘贴。",
        "",
        "## 核心入口",
        "",
    ]
    for path in seed_paths:
        lines.append(f"- [[{_note_link(path)}|{_read_title(path)}]]")
    lines.append("")
    lines.extend(
        [
            "## 生长规则",
            "",
            "- 新概念优先从 `99-Templates/SSOT - 概念条目.md` 生成",
            "- 先写定义和边界，再写结论和证据",
            "- 与项目决策相关时，配套在 `20_Projects/ADR` 留痕",
            "",
        ]
    )
    (SSOT_DIR / "00 SSOT 权威条目.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main() -> int:
    research_files = sorted([p for p in RESEARCH_DIR.glob("*.md") if not p.name.startswith("00_")], key=lambda p: p.stem.lower())
    strategy_files = sorted([p for p in STRATEGY_DIR.glob("*.md") if not p.name.startswith("00_")], key=lambda p: p.stem.lower())
    SSOT_DIR.mkdir(parents=True, exist_ok=True)

    _write_nav_page(
        RESEARCH_DIR / "00_研究资料导航.md",
        "研究资料导航",
        "这里是研究型资料的统一入口。遵循至简原则，不再靠深层目录区分主题，而是靠导航、搜索、链接和 SSOT 沉淀来收敛复杂性。",
        research_files,
        RESEARCH_GROUPS,
    )
    _write_nav_page(
        STRATEGY_DIR / "00_会议战略导航.md",
        "会议战略导航",
        "这里集中放会议纪要、战略规划、建议与项目材料。它们服务于决策推进，成熟后应继续沉淀到 `20_Projects/ADR` 或 `10_Knowledge/SSOT`。",
        strategy_files,
        STRATEGY_GROUPS,
    )

    seed_paths = [_write_ssot_seed(seed) for seed in SSOT_SEEDS]
    _write_ssot_index(seed_paths)
    print("entrypoints built")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
