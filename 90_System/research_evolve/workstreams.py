# -*- coding: utf-8 -*-
"""research_evolve.workstreams — 五大科研工作流的控制平面。

为什么需要它（当前最核心的缺口）:
    vault 里五条工作流**作为目录是存在的**，但没有任何"控制面"把它们串起来：
    没有状态机说明"一个输入属于哪条流、下一步做什么、什么算做完"。
    后果就是用户反馈的两件事：
      * 每日剪入的内容堆在 GetNotes_Inbox（实测 719 个文件）里无人处置
        —— 问题不是内容多，而是**没有分诊（disposition）这一步**；
      * 看板/主页只是统计数字，不告诉人"现在该动手做什么"。
    本模块定义五条流的**输入 / 产物 / 闸门 / 下一步动作**，并给出分诊规则。

五条流（对应用户点名的五项功能）:
    PAPER  论文与专利撰写
    GUIDE  项目指南编写
    READ   论文阅读与复现
    CODE   核心代码编写与验证
    SIM    复杂网络涌现智能仿真（含秀丽线虫等交叉仿真）
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .common import VAULT


@dataclass
class Workstream:
    """一条科研工作流的定义。"""
    id: str
    name: str
    desc: str
    # 产物落地的目录（相对 vault）
    dirs: list[str]
    # 该流的"入账"信号词（用于分诊）
    keywords: list[str]
    # 硬闸门：不满足就不算完成（对应 AGENTS.md 的证据/引用/复现铁律）
    gates: list[str]
    # 下一步动作模板
    next_actions: list[str] = field(default_factory=list)
    # 该流的最小闭环定义（用于判断"这周有没有推进"）
    closure: str = ""


WORKSTREAMS: dict[str, Workstream] = {
    "PAPER": Workstream(
        id="PAPER",
        name="论文与专利撰写",
        desc="把已验证的结论写成论文/专利，引用与数字必须可追溯",
        dirs=["50_Output/51_Papers", "50_Output/52_Patents", "50_Output/53_Monographs",
              "50_Output/54_Code", "50_Output/55_Guides"],
        keywords=["论文", "投稿", "专利", "交底书", "manuscript", "paper", "patent",
                  "abstract", "introduction", "rebuttal", "审稿", "期刊", "会议",
                  "ASPLOS", "Nature", "IEEE", "稿", "撰写"],
        gates=[
            "正文引用只能取自 papers.yaml 白名单（门禁会拦 citation-unregistered）",
            "任何性能数字必须带 [实测]/[仿真]/[引用]/[推导]/[假设]/[待测] 标签",
            "含公式的理论主张须经 manuscript-math-verify 或显式标 [待测]",
            "每篇稿件在 50_Output/51_Papers 下有唯一版本台账，不得留 v2…v19 并行",
        ],
        next_actions=["补证据标签", "核验引用白名单", "合并并行版本", "写 response letter"],
        closure="提交一次完整稿（含引用核验通过 + 数字全部带标签）",
    ),
    "GUIDE": Workstream(
        id="GUIDE",
        name="项目指南编写",
        desc="申报指南/建议书/任务书：面向评审，结构完整、指标可验证",
        dirs=["50_Output/55_Guides", "50_Output/56_Prototypes", "60_MOC/00_治理"],
        keywords=["指南", "建议书", "任务书", "申报", "立项", "先导专项", "项目书",
                  "proposal", "指南编写", "答辩", "评审", "课题", "指标论证"],
        gates=[
            "每条技术指标必须有验证方式与验收标准（对应 V-* 任务）",
            "不得出现无出处的性能承诺",
            "与 AGENTS.md 的目录命名/白名单一致",
        ],
        next_actions=["补齐指标验证方式", "对齐指南模板", "补团队分工与里程碑"],
        closure="产出一份可提交的指南/建议书，指标全部有验证方式",
    ),
    "READ": Workstream(
        id="READ",
        name="论文阅读与复现",
        desc="读懂 + 复现关键工作：结论要有页面级出处，复现要有可跑代码",
        dirs=["20_Processing/02_Fulltext_Analysis", "50_Output/54_Code",
              "20_Processing/22_Audit/paper_notes"],
        keywords=["阅读", "精读", "复现", "笔记", "解读", "review", "survey", "综述",
                  "论文笔记", "复现代码", "reproduce", "读懂"],
        gates=[
            "结论带页面级出处（citekey + 页码），由 paper_reader 生成",
            "复现必须留：代码 + 固定随机种子 + 依赖版本 + 一键命令",
            "区分「读到的」与「我验证的」",
        ],
        next_actions=["写入阅读笔记", "跑复现脚本", "对比原文指标", "登记到 papers.yaml"],
        closure="一篇论文：笔记 + 可一键复现的脚本 + 与原报告指标的差异说明",
    ),
    "CODE": Workstream(
        id="CODE",
        name="核心代码编写与验证",
        desc="实验/算法代码：可复现、可验证、版本不蔓延",
        dirs=["50_Output/54_Code", "40_iNEST/45_Simulation", "30_TCC/35_Simulation"],
        keywords=["代码", "实现", "算法", "脚本", "重构", "接口", "测试", "验证",
                  "code", "implement", "单元测试", "性能", "加速", "RTL", "FPGA"],
        gates=[
            "一个实验只有一个**规范版本**（其余进 git 历史，不在目录里并存 v2…v19）",
            "固定随机种子 + 锁定依赖版本",
            "留 run_manifest（配置/种子/结果哈希）",
        ],
        next_actions=["收敛版本", "补种子与依赖锁定", "补 run_manifest", "跑验收用例"],
        closure="一个实验：单一规范脚本 + 可复现 manifest + 验收通过",
    ),
    "SIM": Workstream(
        id="SIM",
        name="复杂网络涌现智能仿真",
        desc="涌现/临界性/物理演化计算仿真；含秀丽线虫等生物连接组的交叉仿真与实验",
        dirs=["40_iNEST/45_Simulation", "30_TCC/35_Simulation"],
        keywords=["仿真", "涌现", "临界", "criticality", "涌现智能", "复杂网络",
                  "连接组", "connectome", "秀丽线虫", "C. elegans", "线虫",
                  "神经形态", "neuromorphic", "SNN", "脉冲", "Lyapunov",
                  "相变", "自组织临界", "reservoir", "储备池", "SDDE", "物理演化"],
        gates=[
            "固定种子 + 锁定依赖 + 结果可复现（run_manifest）",
            "区分 [仿真] 与 [实测]；仿真结论不得写成普适定律",
            "每个实验登记进实验注册表（exp_registry），禁止版本蔓延",
        ],
        next_actions=["登记实验", "固定种子重跑", "做基线对照", "评估有限尺度效应"],
        closure="一个仿真实验：登记 + 可复现 + 有基线对照 + 结论带 [仿真] 标签",
    ),
}

# 分诊用的"否定/噪声"信号：命中即判为不进科研流（这正是用户要的"少而有效"）
NOISE_PATTERNS = [
    "招聘", "校招", "申博", "考研", "面经", "实习", "薪资", "offer",
    "股价", "涨停", "财报", "融资快讯", "购物", "优惠", "旅游", "美食",
    "养生", "星座", "娱乐", "八卦", "体育",
]


def dir_paths(ws: Workstream) -> list[Path]:
    return [VAULT / d for d in ws.dirs]


def existing_dirs(ws: Workstream) -> list[Path]:
    return [p for p in dir_paths(ws) if p.exists()]


def all_ids() -> list[str]:
    return list(WORKSTREAMS.keys())


def get(ws_id: str) -> Workstream | None:
    return WORKSTREAMS.get(ws_id.upper())


def summary() -> list[dict]:
    """给看板用：每条流的目录数/文件数与闸门数。"""
    out = []
    for ws in WORKSTREAMS.values():
        files = 0
        for d in existing_dirs(ws):
            try:
                files += sum(1 for _ in d.rglob("*") if _.is_file())
            except Exception:
                pass
        out.append({"id": ws.id, "name": ws.name, "dirs": len(existing_dirs(ws)),
                    "files": files, "gates": len(ws.gates), "closure": ws.closure})
    return out
