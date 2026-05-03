from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PROJECTS_DIR = ROOT / "20_Projects"
SYSTEM_DIR = ROOT / "90_System"


@dataclass(frozen=True)
class Stream:
    name: str
    priority: str
    goal: str
    current_work: tuple[str, ...]
    next_work: tuple[str, ...]
    evidence_links: tuple[str, ...]


PROJECT_STREAMS: tuple[Stream, ...] = (
    Stream(
        name="海河实验室重大专项：NCC 端侧原型",
        priority="P0",
        goal="把“晶上网络中心计算 + 液态硬件”收敛成 2000 万元级重大专项的可申报、可汇报、可演示主线。",
        current_work=(
            "收敛 `NCC`、`SDI`、`5+4 原语`、`SDIO-N` 的项目表述口径。",
            "统一申报书、项目指南、Marp 汇报材料与指标口径。",
            "明确 `3+1` 极简 MVP 架构与双场景验证路线。",
        ),
        next_work=(
            "拆出年度里程碑：标准草案、单 FPGA 验证、多 FPGA 原型、热切换演示。",
            "把 `PyiNEST-Lite SDK`、可视化大屏、开源 IP 变成明确交付物。",
            "将申报材料与论文主线、技术开发主线建立一一映射。",
        ),
        evidence_links=(
            "20_Projects/Projects/海河实验室重大专项/海河实验室_项目申报书_晶上网络中心计算_完整版",
            "20_Projects/Projects/海河实验室重大专项/海河实验室_项目汇报_Marp",
            "20_Projects/Projects/项目布局_归口整合/项目布局汇总",
        ),
    ),
    Stream(
        name="NSFC 重大项目：SDSoW 与智能涌现阈值",
        priority="P0",
        goal="形成“复杂网络时空动力学 + SDSoW + 智能相变阈值”的基础理论重大项目叙事。",
        current_work=(
            "收敛 `CST`、`SDI`、`SDSoW`、`FEP/STDP` 的理论闭环。",
            "明确三个关键科学问题与四项主要研究内容。",
            "保持理论主线与工程验证主线彼此支撑而不混乱。",
        ),
        next_work=(
            "把课题拆成理论、机制、工程验证三层任务包。",
            "为 2026 年 9 月前后的窗口提前准备建议书、联合单位和证据链。",
            "补齐与论文主线、仿真主线、硬件路线的映射表。",
        ),
        evidence_links=(
            "20_Projects/Projects/基金委_2000万重大项目指南策划",
            "20_Projects/Projects/项目布局_归口整合/iNEST 国家重大专项项目布局 · 双轨战略框架",
            "20_Projects/Projects/专项时间点",
        ),
    ),
    Stream(
        name="项目布局整合：十年规划与课题矩阵",
        priority="P1",
        goal="把分散的十年规划、项目群、课题编号与论文路线统一为一张项目策划总图。",
        current_work=(
            "保留 81 项项目布局总表作为全局池子。",
            "区分短期申报主线、中期平台路线、长期学科建设路线。",
            "把 `T/K/E/A/D/C` 编号体系作为统一规划语言。",
        ),
        next_work=(
            "提取真正近期要推进的 8-12 个项目，而不是继续平铺 81 项。",
            "按时间窗口建立 `2026-2027`、`2028+` 两层推进板。",
            "将项目、论文、SSOT、ADR 建立双向链接。",
        ),
        evidence_links=(
            "20_Projects/Projects/项目布局_归口整合/项目布局汇总",
            "20_Projects/Projects/项目布局_归口整合/iNEST_项目布局与论文计划总清单",
            "20_Projects/战略规划/iNEST_Academic_Belief_Core",
        ),
    ),
    Stream(
        name="卫星智能体：OODA 闭环液态硬件",
        priority="P1",
        goal="把 `FFT-AllReduce` 同构定理转化为具身智能场景下的液态硬件叙事与专项方向。",
        current_work=(
            "形成超低轨卫星智能体专项建议书。",
            "明确 `观察-决策-行动` 三阶段的时分复用逻辑。",
            "把 `硅基神经重用` 与 `暗硅问题` 绑定成战略卖点。",
        ),
        next_work=(
            "继续拆分雷达、推理、抗干扰三个任务场景的硬件资源配比。",
            "与海河主线共用 `SDI/NCC` 技术底座，避免重复造概念。",
            "形成适合项目建议书与路演的简版故事板。",
        ),
        evidence_links=(
            "20_Projects/Projects/卫星智能体/[V10]_卫星智能体重大专项建议_LiquidOODA版",
            "20_Projects/Ideas/Idea_OODA_卫星智能体_同构定理的战略价值",
            "30_Outputs/论文/B组_SDI-CC互连体系/SDI-CC论文框架_拓扑即计算新范式",
        ),
    ),
)


DEV_STREAMS: tuple[Stream, ...] = (
    Stream(
        name="知识库自动化主线",
        priority="P0",
        goal="把当前 vault 变成可持续生长、可巡检、可标准化提问、可自动导航的知识库系统。",
        current_work=(
            "已完成目录简化、系统提示词接入、Wiki 重建、研究入口与研究面板生成。",
            "已建立 `SSOT/ADR/论文` 的候选与推进面板。",
            "已补齐 `00_Inbox`、`10_Knowledge`、`20_Projects`、`30_Outputs`、`90_System` 的最小可用入口。",
        ),
        next_work=(
            "把 `P0 ADR` 和高价值 `SSOT` 候选直接落成正式文档。",
            "把模板、QuickAdd、Templater 与当前推进板联动。",
            "增加周报/周会自动汇总能力。",
        ),
        evidence_links=(
            "04_Code_代码/restructure_workspace",
            "04_Code_代码/refine_inbox_and_outputs",
            "04_Code_代码/build_knowledge_entrypoints",
            "04_Code_代码/build_research_boards",
        ),
    ),
    Stream(
        name="导入与清洗工具链",
        priority="P0",
        goal="稳定完成 Get 导出、Download 目录、旧链接与旧目录的自动清洗和入库。",
        current_work=(
            "Download 导入已落到 `00_Inbox/01_导入资料/DownloadImports`。",
            "Get 导入已落到 `00_Inbox/01_导入资料/Get`。",
            "旧结构链接已可迁移到新路径。",
        ),
        next_work=(
            "继续降低导入文档中的坏链和预设锚点误差。",
            "将导入后的候选概念自动投递到 `SSOT` 候选池。",
            "为导入链路补报告页和异常页。",
        ),
        evidence_links=(
            "04_Code_代码/download_import/import_download_to_obsidian",
            "04_Code_代码/get_import/import_get_export",
            "04_Code_代码/migrate_legacy_links",
        ),
    ),
    Stream(
        name="仿真与验证平台",
        priority="P1",
        goal="把 `CST` 理论、线虫 connectome 复现和相变扫描，沉淀成稳定的验证平台。",
        current_work=(
            "已有 `v8` 真实 connectome 结果和 `N_min=80` 相变扫描。",
            "已有报告生成脚本和结果图。",
            "已有阶段性技术路线、接口规范和战略提纲文档。",
        ),
        next_work=(
            "整理运行环境、输入数据、结果输出和复现实验说明。",
            "把关键图、关键参数与论文草稿建立强链接。",
            "逐步把仿真结果转为项目指标和论文证据。",
        ),
        evidence_links=(
            "20_Projects/CST仿真平台/CST仿真平台",
            "20_Projects/CST仿真平台/sdi_network_v8.py",
            "20_Projects/CST仿真平台/sdi_phase_transition_scan.py",
        ),
    ),
    Stream(
        name="规划面板生成器",
        priority="P1",
        goal="把 `SSOT`、`ADR`、论文、项目策划、技术开发这些板块都变成可自动重建的面板。",
        current_work=(
            "已支持研究资料导航、会议战略导航、`SSOT` 骨架与研究面板。",
            "已支持论文优先级推进面板。",
            "本轮补齐项目策划与技术开发板块。",
        ),
        next_work=(
            "增加统一的周报/里程碑/风险面板。",
            "把面板入口挂到 Wiki 首页与系统提示词说明中。",
            "形成一键重建所有板块的总控脚本。",
        ),
        evidence_links=(
            "04_Code_代码/build_knowledge_entrypoints",
            "04_Code_代码/build_research_boards",
            "04_Code_代码/build_project_development_boards",
        ),
    ),
    Stream(
        name="Bridge 与外部协同骨架",
        priority="P2",
        goal="保留云端到本地的桥接思路，但不再假设不存在的 TRAE API。",
        current_work=(
            "桥接骨架仍保留在 `trae_bridge` 目录。",
            "目前它更适合作为思路归档，而非当前主线能力。",
        ),
        next_work=(
            "只保留真实可执行的 worker/queue 思路。",
            "避免继续把桌面 GUI 当成可编排 API。",
        ),
        evidence_links=(
            "04_Code_代码/trae_bridge/Genspark Claw → Local Worker Bridge",
            "04_Code_代码/trae_bridge/local_worker.ps1",
        ),
    ),
)


def _now() -> str:
    return dt.datetime.now().replace(microsecond=0).isoformat(sep=" ")


def _render_links(links: tuple[str, ...]) -> list[str]:
    return [f"- [[{link}]]" for link in links]


def _write(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def _build_project_overview() -> None:
    lines = [
        "# 项目策划总览",
        "",
        f"生成时间：{_now()}",
        "",
        "这个板块回答三个问题：",
        "- 当前真正的项目主线是什么",
        "- 这些主线现在在推进什么",
        "- 接下来应该先做什么，而不是继续摊大饼",
        "",
        "## 当前判断",
        "",
        "- `P0`：海河实验室重大专项、NSFC 重大项目",
        "- `P1`：项目布局整合、卫星智能体专项方向",
        "- 长线底座：十年规划、项目群、课题矩阵继续作为储备池存在",
        "",
    ]
    for stream in PROJECT_STREAMS:
        lines.extend(
            [
                f"## {stream.priority} · {stream.name}",
                "",
                f"- 目标：{stream.goal}",
                "- 当前工作：",
                *[f"  - {item}" for item in stream.current_work],
                "- 后续工作：",
                *[f"  - {item}" for item in stream.next_work],
                "- 关键证据：",
                *_render_links(stream.evidence_links),
                "",
            ]
        )
    _write(PROJECTS_DIR / "00_项目策划总览.md", lines)


def _build_project_board() -> None:
    lines = [
        "# 项目推进面板",
        "",
        f"生成时间：{_now()}",
        "",
        "## 本期优先",
        "",
        "| 优先级 | 项目主线 | 当前要推进 | 后续要推进 |",
        "| --- | --- | --- | --- |",
    ]
    for stream in PROJECT_STREAMS:
        current = "；".join(stream.current_work[:2])
        nxt = "；".join(stream.next_work[:2])
        lines.append(f"| {stream.priority} | {stream.name} | {current} | {nxt} |")
    lines.extend(
        [
            "",
            "## 近期工作清单",
            "",
            "- `海河实验室重大专项`：统一申报书、指南、Marp 汇报的表述口径与指标口径。",
            "- `NSFC 重大项目`：将关键科学问题、研究内容与可验证路径进一步收敛成课题包。",
            "- `项目布局整合`：从 81 项中压缩出 2026-2027 真正推进的核心项目池。",
            "- `卫星智能体`：将 OODA 场景拆分为可展示的硬件复用故事板。",
            "",
            "## 后续工作清单",
            "",
            "- 建立项目主线与论文主线的映射表。",
            "- 建立项目主线与技术开发主线的映射表。",
            "- 建立时间窗口清单：2026 年窗口、2027 年窗口、中长期路线。",
            "",
        ]
    )
    _write(PROJECTS_DIR / "00_项目推进面板.md", lines)


def _build_dev_overview() -> None:
    lines = [
        "# 技术开发总览",
        "",
        f"生成时间：{_now()}",
        "",
        "这个板块回答三个问题：",
        "- 当前有哪些真实在开发的工具链和代码主线",
        "- 它们各自服务于哪条项目/知识线",
        "- 哪些是主线，哪些只是归档或低优先级骨架",
        "",
    ]
    for stream in DEV_STREAMS:
        lines.extend(
            [
                f"## {stream.priority} · {stream.name}",
                "",
                f"- 目标：{stream.goal}",
                "- 当前工作：",
                *[f"  - {item}" for item in stream.current_work],
                "- 后续工作：",
                *[f"  - {item}" for item in stream.next_work],
                "- 关键证据：",
                *_render_links(stream.evidence_links),
                "",
            ]
        )
    _write(SYSTEM_DIR / "00_技术开发总览.md", lines)


def _build_dev_board() -> None:
    lines = [
        "# 技术开发推进面板",
        "",
        f"生成时间：{_now()}",
        "",
        "## 当前主线",
        "",
        "| 优先级 | 开发主线 | 当前要推进 | 后续要推进 |",
        "| --- | --- | --- | --- |",
    ]
    for stream in DEV_STREAMS:
        current = "；".join(stream.current_work[:2])
        nxt = "；".join(stream.next_work[:2])
        lines.append(f"| {stream.priority} | {stream.name} | {current} | {nxt} |")
    lines.extend(
        [
            "",
            "## 当前要推进的工作",
            "",
            "- 把 `P0 ADR` 候选落成正式 ADR 文档。",
            "- 把高价值 `SSOT` 候选落成正式 SSOT 草稿。",
            "- 继续增强导入链路，减少旧链接和预设锚点误差。",
            "- 把仿真平台的运行环境、输入输出和复现说明整理成标准文档。",
            "",
            "## 后续要推进的工作",
            "",
            "- 增加项目/技术/论文三线统一周报。",
            "- 增加一键重建全部面板的总控脚本。",
            "- 将模板、QuickAdd、Templater 与推进面板联动。",
            "",
        ]
    )
    _write(SYSTEM_DIR / "00_技术开发推进面板.md", lines)


def main() -> int:
    _build_project_overview()
    _build_project_board()
    _build_dev_overview()
    _build_dev_board()
    print("project and development boards built")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
