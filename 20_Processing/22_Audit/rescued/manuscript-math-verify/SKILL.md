---
name: manuscript-math-verify
description: 手稿数学验证引擎。当用户需要验证理论手稿/论文的数学严谨性（claim 抽取、证明义务、符号定义完整性、公式依赖、推导链、数值一致性如 1/2≈0.707 类错误、证明骨架缺口、仿真交接建议、修订报告）时使用。处理含定理/引理/猜想/假设的理论文档（HTML/Markdown/纯文本），适合 CST/SOC/临界性/涌现类理论稿的投稿前自检，也适用一般数学论文的证明结构审计。
whenToUse: 用户给出理论手稿要"验证数学/检查证明/找推导漏洞/自检理论严谨性/投稿前数学审查"，或指定运行 verify_manuscript.py 时。
metadata:
  source: "考古审计抢救自 D:/Obsidian/Agent/_core_framework/tooluniverse_agent_base.py (L1290-1915)，2026-08-21 提炼为独立技能"
  engine: "verify_manuscript.py（纯标准库，无第三方依赖）"
---

# 手稿数学验证引擎（Manuscript Math Verify）

对理论手稿执行结构化的**数学-逻辑严谨性验证**，产出：claim 清单 → 证明义务 → 符号目录 → 公式依赖检查 → 推导链检查 → 数值一致性检查 → 证明骨架（假设/引理/步骤/缺口）→ 仿真交接建议 → 一致性检查 → 修订报告。

## 何时使用

**使用**：
- 用户给出理论手稿（HTML/Markdown/纯文本），要求"验证数学严谨性 / 检查证明 / 找推导漏洞 / 数值一致性 / 投稿前自检"。
- 手稿含定理（定理/引理/假设/猜想）与公式（如 CST、θ 阈值、Γ_st、α 临界指数等），需要结构化证明审查。
- 用户要求运行本技能的 CLI 引擎 `scripts/verify_manuscript.py`。

**不使用**：
- 纯写作润色（→ light-paper-polishing）。
- idea 层面的创新性批判（→ light-idea-critique）。
- 引用/文献审查（→ light-citation）。
- 审稿意见模拟（→ light-review-rebuttal）。
- 无公式、无证明结构的经验性/实验性文稿。

## 执行流程

1. **定位手稿**：确认输入文件路径（.html/.md/.txt 均可；HTML 会按 h1-h4 分节，Markdown 按 # 标题分节）。
2. **运行引擎**：
   ```bash
   python "C:/Users/LEO/.agents/skills/manuscript-math-verify/scripts/verify_manuscript.py" <手稿路径> --report
   # 或输出全量 JSON：
   python "C:/Users/LEO/.agents/skills/manuscript-math-verify/scripts/verify_manuscript.py" <手稿路径> --json <out.json>
   ```
   （Python 3.8+，仅标准库；Windows 可用 `D:/Obsidian/Agent/.venv/Scripts/python.exe` 或系统 python。）
3. **解读结果**，按以下维度向用户汇报：

### 报告解读模板

| 维度 | 引擎输出 | 汇报要点 |
|---|---|---|
| Claim 抽取 | claims_digest | 抽到几条 claim、类型分布（定理/引理/假设/猜想/推导声明） |
| 证明义务 | proof_obligations_digest | 哪些 claim 要求理论证明（definitions_closed / derivation_chain_present / threshold_algebra_explicit / bounded_domain_explicit / beta_function_specified / stability_condition_explicit） |
| 符号目录 | math_validation.symbol_catalog | CS/CT/CST/Γ_st/α/RI/θ/λ 哪些有定义、哪些缺失 |
| 公式依赖 | dependency_checks | 公式引用了未定义的核心符号 → warn |
| 推导链 | derivation_checks | 关键推导节（θ₁ 热力学、θ₂ 信号检测、CST 阈值映射、RG 固定点）是否齐全 |
| 数值一致性 | numeric_checks | **重点看 fail**：如 "1/2≈0.707" 应为 "1/√2≈0.707"；Γ_st∈[-1,1] 边界是否显式；θ 常量表是否完整 |
| 证明骨架 | proof_skeleton_digest | 每个定理型 claim 的假设/引理/推导步骤/结论/缺口 |
| 仿真交接 | simulation_handoff_digest | 哪些 claim 需要仿真验证，推荐数据集族与指标 |
| 一致性 | consistency_digest | missing_theorem_structure / missing_assumptions / symbol_definition_gap / proof_skeleton_gap |
| 修订报告 | revision_report | **主交付物**：priority_actions 列表 + summary |

4. **结论分级**（按修订报告的 priority_actions 判定）：
   - 全部 pass / 无 fail：可进入下一阶段（投稿/仿真），但仍提醒人工检查证明细节。
   - 有 warn：列出 warn 项，建议补齐（符号定义、推导节缺失、常量表不完整）。
   - 有 fail：**必须修复后重跑**（如数值不一致 1/2 vs 1/√2、Γ_st 边界缺失）。

## 输出规范

- 主交付：**修订报告**（结构化列出 priority_actions），附 claim/公式/缺口统计。
- 涉及仿真验证的 claim，给出交接项（数据集族 + 指标 + required_checks），对接 40_iNEST/45_Simulation。
- 数据真实性纪律（AGENTS.md §0）：引擎的 check 是启发式文本模式匹配，**不是形式化证明**；汇报时必须区分"模式检测结果"与"人工证明结论"，不得把 warn/fail 冒充为数学上已证/已伪。

## 已知局限

- 原引擎针对 iNEST/CST 理论手稿定制（θ 阈值、Γ_st、β(CST) 固定点等模式）；对**一般数学论文**，claim 抽取与推导链检查仍有效，但符号目录/数值检查的领域规则需扩展（改 scripts 中的 symbol_rules / theta_constants / expected_sections）。
- 文献验证（evidence）是启发式占位（按是否有年份引用计数），**不做真实检索**；需要真实文献支撑时配合 light-literature-search / pipeline_v3 检索语义。
- PDF 输入请先用 pdf_to_markdown 类工具转文本；引擎直接吃 HTML 可较好处理 PDF 导出的 HTML。
