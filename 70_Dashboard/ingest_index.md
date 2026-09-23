# 材料分类与任务相关性索引

> 生成 2026-09-23 04:30 · 共 **927** 条材料

## 一、按工作流分类

| 工作流 | 数量 | 清单页 |
|---|---|---|
| PAPER 论文与专利撰写 | 374 | `10_Knowledge/00_导航/classified/PAPER.md` |
| CODE 核心代码编写与验证 | 277 | `10_Knowledge/00_导航/classified/CODE.md` |
| SIM 复杂网络涌现智能仿真 | 161 | `10_Knowledge/00_导航/classified/SIM.md` |
| GUIDE 项目指南编写 | 63 | `10_Knowledge/00_导航/classified/GUIDE.md` |
| READ 论文阅读与复现 | 52 | `10_Knowledge/00_导航/classified/READ.md` |

## 二、按已采纳研究方向（用于后续复现迭代）

| 方向 | 强相关材料数 | 说明 |
|---|---|---|
| **H10** | 495 | 连接组 等 |
| **HALAPOINT** | 397 | Loihi 等 |
| **H7** | 389 | NoC 等 |
| **H8** | 293 | 晶圆级 等 |
| **MTIA300** | 283 | 通信 等 |
| **H5** | 270 | SDI 等 |
| **H6** | 210 | chiplet 等 |
| **PTHEORY** | 79 | 元拓扑 等 |
| **MOTIF** | 11 | motif 等 |

查某个方向的材料：`python -m research_evolve.ingest --task H7`

## 三、相关性最高的材料

| 相关性 | 来源 | 材料 | 工作流 | 任务 |
|---|---|---|---|---|
| 90 | Guides | 2026_TCC与INEST_全局论文与专利战略规划 | PAPER | H5、H7、H8、H10、MTIA300、HALAPOINT |
| 82 | GetNotes | 忆阻器拓扑流形佐证iNEST | SIM | H5、H6、H7、H8、H10、MOTIF、HALAPOINT、PTHEORY |
| 79 | Guides | 2026_TCC与INEST_全局论文与专利战略规划_v2 | PAPER | H5、H7、H8、H10、MTIA300、HALAPOINT |
| 77 | Guides | [V1] iNEST_项目指南与论文规划 | GUIDE | H5、H6、H7、H8、H10、MTIA300、HALAPOINT、PTHEORY |
| 73 | GetNotes | iNEST理论体系系统性佐证与工程落地路线图（标准化版） | SIM | H5、H6、H7、H8、H10、MOTIF、HALAPOINT、PTHEORY |
| 73 | Patents | 专利A_软件定义互连系统架构及调度方法_完整交底书 | PAPER | H5、H6、H7、H8、H10、MTIA300、HALAPOINT、PTHEORY |
| 73 | Guides | [V1]_NSFC重大项目指南_硅基自组织网络与物理涌现智能 | SIM | H5、H7、H8、H10、MTIA300、HALAPOINT、PTHEORY |
| 73 | Guides | [V1]_海河实验室_项目指南_MetaTopo_MVP | GUIDE | H5、H6、H7、H8、H10、MTIA300、HALAPOINT、PTHEORY |
| 69 | Guides | 海河实验室项目指南（2026年度重大专项） | GUIDE | H5、H6、H7、H8、H10、MTIA300、HALAPOINT、PTHEORY |
| 67 | Guides | 邬院士_先进计算与前沿微纳电子_项目指南说贴_PPT_v2 | GUIDE | H5、H7、H8、H10、MTIA300、HALAPOINT、PTHEORY |
| 66 | Patents | 专利A_ARS审查报告 | PAPER | H5、H6、H7、H8、H10、MTIA300、HALAPOINT、PTHEORY |
| 65 | GetNotes | 拓扑流形计算与iNEST_TCC融合研究路线图 | CODE | H5、H6、H7、H10、MTIA300、HALAPOINT |
| 65 | Guides | 邬院士_三个重点专项项目指南说贴_PPT_v3 | GUIDE | H5、H6、H7、H8、H10、MTIA300、HALAPOINT、PTHEORY |
| 64 | Guides | [V2]_海河实验室_项目指南_MetaTopo_MVP_FPGA版 | CODE | H5、H7、H8、H10、MTIA300、HALAPOINT、PTHEORY |
| 64 | Guides | iNEST计算范式工程落地战略规划_v1.0 | SIM | H5、H6、H8、H10、MTIA300、HALAPOINT |
| 64 | Guides | 上海市科委：TCC原型 | CODE | H5、H6、H7、H8、H10、MTIA300、HALAPOINT、PTHEORY |
| 63 | GetNotes | getnote_1917409580389430544_软件定义晶上系统 | CODE | H5、H6、H7、H8、H10、MTIA300 |
| 63 | Papers | TCC精炼总结_致金海教授斧正_v2.0 | CODE | H5、H7、H10、MTIA300、HALAPOINT、PTHEORY |
| 63 | Papers | P2_LLM_Interconnect_Review_Framework | READ | H5、H6、H7、H8、H10、MTIA300、HALAPOINT、PTHEORY |
| 63 | Patents | P0-1_软件定义互连系统架构及调度方法_交底书草稿 | PAPER | H5、H7、H8、H10、MTIA300、HALAPOINT、PTHEORY |
| 62 | GetNotes | getnote_1917307943209549728_晶圆级异构集成方案详解 | CODE | H5、H6、H7、H8、H10、MTIA300、HALAPOINT、PTHEORY |
| 62 | Papers | SDI-CC论文框架_拓扑即计算新范式 | PAPER | H5、H6、H7、H10、MTIA300、PTHEORY |
| 62 | Guides | TCC计算范式工程落地与生态构建战略规划_v2.0_完整版 | SIM | H5、H6、H7、H8、H10、MTIA300、HALAPOINT |
| 61 | GetNotes | getnote_1917532783674956432_拓扑中心计算范式架构关键技术研究 | CODE | H5、H6、H7、H8、H10、MTIA300、HALAPOINT、PTHEORY |
| 61 | GetNotes | kb_iNEST_getnote_1913997852716339936_智能涌现理论框架 | SIM | H5、H7、H8、H10、MTIA300、HALAPOINT、PTHEORY |
| 61 | Papers | iNEST_00_论文总清单 | PAPER | H5、H6、H10、MTIA300、HALAPOINT、PTHEORY |
| 60 | Papers | 00_TCC_INEST_论文专利总览与推进计划_20260606_详细版 | PAPER | H5、H6、H10、MTIA300、HALAPOINT、PTHEORY |
| 60 | Patents | 00_核心专利群部署计划_四簇三层 | PAPER | H5、H6、H7、H8、H10、MTIA300、HALAPOINT、PTHEORY |
| 59 | Inbox | 晶圆级软件定义可重构互连架构与电路申报方案（LTI版+1.65亿经费完整版） | CODE | H5、H7、H8、H10、MTIA300、HALAPOINT、PTHEORY |
| 59 | Papers | B4_Route_IS_Transform_Isomorphism_Draft | PAPER | H5、H6、H7、H8、H10、MTIA300、HALAPOINT |
| 59 | Papers | 拓扑中心计算范式架构关键技术研究 | CODE | H5、H6、H7、H8、H10、MTIA300、HALAPOINT、PTHEORY |
| 59 | Guides | TCC计算范式工程落地与生态构建战略规划_v1.0 | CODE | H5、H6、H7、H8、H10、MTIA300、HALAPOINT |
| 59 | Guides | 前沿微纳电子专项项目指南_v1 | GUIDE | H5、H6、H7、H8、H10、MTIA300、HALAPOINT |
| 58 | GetNotes | getnote_1916677671790876272_iNEST 理论体系系统总结报告：从物理第一性原理到晶圆 | SIM | H5、H7、H8、H10、MOTIF、PTHEORY |
| 58 | GetNotes | 晶圆级软件定义可重构互连架构与电路申报方案（LTI版+1.65亿经费+物理长程骨架修订版） | CODE | H5、H7、H8、H10、MTIA300、HALAPOINT |
| 58 | Inbox | 晶圆级软件定义可重构互连架构与电路申报方案（LTI版+1.65亿经费+物理长程骨架修订版） | CODE | H5、H7、H8、H10、MTIA300、HALAPOINT、PTHEORY |
| 57 | GetNotes | kb_iNEST_getnote_1913999010209869760_拓扑生成技术框架 | CODE | H5、H7、H8、H10、MTIA300、HALAPOINT、PTHEORY |
| 57 | Papers | 拓扑中心计算——面向通信受限智能计算的第三类体系结构范式 | CODE | H5、H6、H7、H10、MTIA300、HALAPOINT |
| 56 | GetNotes | getnote_1917217265712035088_TCCNPU协同路线图 | CODE | H5、H6、H7、H10、MTIA300、HALAPOINT |
| 56 | GetNotes | 晶圆级软件定义可重构互连架构与电路申报方案（LTI版+1.65亿经费完整版） | CODE | H5、H7、H8、H10、MTIA300、HALAPOINT |

---

**怎么用**：① 「分类保存」看第一节，每类一个清单页；② 「找任务强相关材料」用第二节或 `--task`；③ 找到后进对应工作流的复现迭代（READ 流：笔记 + 复现脚本 + 与原文指标对比）。
