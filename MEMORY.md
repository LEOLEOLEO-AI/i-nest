# MEMORY

## Workspace Defaults

- 当前主工作区是一个以 Obsidian 为核心的科研知识库，重点围绕 SSOT、ADR、Inbox、Wiki、知识图谱和自动化脚本形成自生长体系。
- 默认全局问题处理方式：先标准化问题，再诊断或执行，再尽量沉淀到可复用文件，而不是只停留在对话里。
- Copilot 系统提示词入口：`copilot/system-prompts/知识库问题标准化系统提示词.md`，由 `.obsidian/plugins/copilot/data.json` 的 `defaultSystemPromptTitle` 指向。

## Known Gaps

- 工作区曾缺失 `MEMORY.md` 与每日 `memory/YYYY-MM-DD.md`，导致会话连续性弱。
- 模板目录统一使用 `99-Templates`（非 `99-templates`）。
- QQBot/WeChat 的 systemPrompt 不能过长（上限约 500 字），否则撑满 context 导致卡死。
- `sessions_spawn` 子 agent 不加 `streamTo` 时主会话无法感知进度，易误判为"卡死"。
- nohup 后台命令结果需通过文件轮询 + cron 主动通知用户，不能靠工具同步返回。
- git 仓库内含嵌套 git 仓库（ResearchTools/AI-Research-SKILLs 等），add 时需 `--cached` 排除。

## User Preference Signals

- 中文、直接、结构化、可落地的结果。
- 把零散问题自动整理成标准化任务，并持续沉淀为知识库资产。

## 状态追踪基础设施 (2026-05-07)

- `.tasks/track.py` — 长时间命令状态写入工具（供 cron 读取）
- `.tasks/status.sh` — 实时命令状态雷达
- `.tasks/auto_status.sh` — 5 分钟自动状态日志，写入 `.tasks/status_log.txt`
- `task-status-radar` cron（每 5 分钟）— 检测结果文件变化推送到 QQ
- 规则：后台长时任务启动写 track 状态 → 结束写 RESULT_READY → cron 检测推送

## iNEST 学术信仰

- **学术信仰**：大道至简（Complexity comes from Simplicity）
- **核心"一"**：自组织临界机制（Self-Organized Criticality）
- **计算范式**：TCC（拓扑中心计算）← 原 NCC
- **架构**：SDI（软件定义互连）+ SDSoW
- **三位一体**：物理第一性 + 生物智能启迪 + 液态拓扑SDI化合键
- **目标**：把极简规则固化进 SDI 柔性韧带，让硅基网络自主涌现从线虫到超人类的智能

## iNEST 全称修订 (2026-05-11)

- **旧名**：Institute for Neuromorphic & Emergent Systems Technology
- **新名**：Intelligence Emerging from Network Temporal-spatial Synergy
- **中文**：网络时空协同智能涌现范式
- **来源**：刘勤让教授 2026-05-11 正式确认（所有文档、Demo、Logo 副标题已全部更新）

---

## SDI 实验体系——锁定版本汇总

四条 SDI 规则：**STDP + WS 重连 + 突触缩放 + 竞争性修剪**

### 实验一 v17 FINAL（2026-05-08，已锁定）

- 文件：`sdi_sim/sdi_experiment1_v17.py`
- **20/20 物种全部 ≥3/5（100% 覆盖率）**，16/20 达 5/5 满分
- 横跨原始动物（线虫 N=20）→ 海鞘 → 环节动物 → 软体动物 → 鱼类 → 爬行类 → 鸟类 → 哺乳动物 → 灵长类 → 人类
- 代表进化 5 亿年跨度的神经网络均自发演化出 SOC 临界态
- 演化路径：初版 5 物种（v1）→ 7 物种（v11）→ 10 物种锁定（v13）→ BTW 驱动 14 物种（v15/v16）→ 20 物种最终（v17）
- 详细历史：`MEMORY/archive/exp1_versions.md`

### 实验二 Hemibrain 嗅觉编码 (2026-05-06)

- 文件：`sdi_sim/sdi_experiment2_olfactory.py`
- N=1351 嗅觉子环路（ORN=33, PN=124, KC=1099, APL=19, MBON=76）
- KC 稀疏激活率 **2.55% < 10% 目标** ✅
- 气味分辨余弦距离 **0.058 > 0.05** ✅
- σ=113.87, α=2.00（真实 connectome 接近理想 SOC）

### 实验三 零先验自演化 (2026-05-08)

- 文件：`sdi_sim/sdi_experiment3_emergence.py`
- 3 种初始拓扑（ER/WS/BA）× 3 种子，N=500，8000 步
- **关键发现**：500 步内全部 σ>6，SDI 三规则对任意初始拓扑均能快速驱动小世界涌现
- **未通过**：Q 随演化单调下降（终态 Q<0.1），三规则是"小世界涌现器"而非"模块化涌现器"
- 结论：需要第四条规则——竞争性修剪

### 实验四 竞争性修剪——模块化涌现 (2026-05-08)

- 文件：`sdi_sim/sdi_experiment4_modularity.py`
- 新增规则：活动依赖修剪（use it or lose it），P_PRUNE=0.05, PRUNE_INT=200
- 关键结果：

  | 起点 | 实验三 Q | 实验四 Q | 实验四 σ | 模块数 |
  |---|---|---|---|---|
  | ER | 0.010 | 0.278 | 0.869 | 6.3 |
  | WS | 0.075 | **0.664** | **6.778** | 3.7 |
  | BA | 0.008 | 0.365 | 4.746 | 12.0 |

- WS 起点修剪强度不敏感（p=0.02/0.05/0.10 结果近似，Q≈0.66）
- **结论**：竞争性修剪是模块化涌现的关键规则

### 实验五 v14 FINAL（2026-05-10，神经雪崩 SOC，历史最佳）

- 文件：`sdi_sim/sdi_experiment5_v14.py`, `exp5_v14_avalanche_results.json`
- 核心改进：SIZE_TARGET_HI 80→25（防止 mean_size 大导致 duration 双模态）
- **总分 128/162 = 79.0%（v12: 66.7%, v13: 69.1%, v14: 79.0%）**

  | 网络+规则 | s42 | s7 | s13 | 均值 |
  |---|---|---|---|---|
  | C.elegans 3-rules | 7 | 8 | 8 | **7.7** |
  | Human_HCP 3-rules | 8 | 8 | 7 | **7.7** |
  | WS_Control 3-rules | 7 | 7 | 6 | 6.7 |
  | C.elegans 4-rules | 7 | 8 | 6 | 7.0 |
  | Human_HCP 4-rules | 8 | 8 | 7 | **7.7** |
  | WS_Control 4-rules | 7 | 7 | 7 | 7.0 |

- 演化路径：v4（κ 校准）→ v5（真实 BTW）→ v7（KS+LR 严格）→ v12（稳态归一化）→ v13（ECDF）→ v14
- 详细历史：`MEMORY/archive/exp5_versions.md`

### 实验六 真实 C.elegans 连接组 (2026-05-09)

- 文件：`sdi_sim/sdi_experiment6_real_connectome.py`
- 数据：`sdi_sim/celegans_sim/connectome_v8_data.json`（Varshney 2011）

  | 规则 | σ初始 | σ最终 | κ | τ_s | τ_d | PSD | decode | 得分 |
  |---|---|---|---|---|---|---|---|---|
  | 3-rules | 8.63 | 2.95 | 1.053 | 1.44 | 1.65 | -1.56 | 0.202 | 5/9 |
  | **4-rules** | 8.63 | **2.19** | 1.075 | **1.55** | **1.73** | **-1.30** | **0.405** | **6/9** |

- **核心发现**：真实 connectome 初始 σ=8.63（比 WS 随机 σ≈12 低，已有小世界特性）；SDI 演化后 σ 降至 2-3（更强模块化而非更强小世界）
- 4-rules 输出解码 0.405（vs 3-rules 0.202），证明竞争性修剪提升功能分化
- 电突触→E-L 键初始化起锚定作用

### 工具与文档

- 缩略语对照表：`knowledge/SDI_Glossary.md`
- SDSoW 硬件映射：`sdi_sim/SDSoW_Hardware_Mapping.md`（902 行，52KB）
- 研究报告：`sdi_sim/SDI_Research_Report.md`（含 22 篇参考文献）
- 论文草稿：`sdi_sim/SDI_Paper_Draft.md`（中英双语摘要，28 篇参考）

## LaTeX 论文打包 (2026-05-10)

- 目录：`/home/work/.openclaw/workspace/sdi_paper/`
- 文件：`main.tex`（575 行），`references.bib`（408 行），`figures/`（11 个图）
- 产出：`main.pdf`（21 页, 1.5MB），打包 `SDI_paper_v1.zip`（4.7MB）
- 编译：`pdflatex main.tex → bibtex main → pdflatex×2`

---

## 理论桥接

### West2024 复杂度同步 CS 任务 (2026-05-14)

- **来源**：Bruce J. West et al., *Scientific Reports* (2024)
- **核心概念**：CS — 多分形维数 D(t) 的动态共进化，超越相位/频率同步
- **关键发现**：
  - CS 是 Γst 的动态时序版本：Γst_CS(t) = corr[Ds(t), DT(t)]
  - N=10 智能体：MFD 互相关 > 0.95，均值相关 ≈ 0（CS 的强指纹）
  - 能量最小化 ↔ CS 在标度律层面互为对偶
- **高优先级任务**：
  - 证明 ⟨corr[Ds(t), DT(t)]⟩_T = NMI(Ms, MT) 在 ergodic 极限成立
  - 建立 CS 阈值 ↔ CST 六阈值体系映射
  - SDI 实验七：C.elegans 同时计算静态 Γst 与动态 CS，验证相关性
  - 投稿目标：Nature Physics / PRX
- 文献分析：`literature/West2024_CS_Analysis.md`
- PDF：`literature/pdf/2026-05-14/West2024_ComplexitySynchronization_EmergentIntelligence.pdf`

### 预测编码与 SDI 等价关系 (2026-05-16)

- **来源**：NeuroPrior AI（大脑的学习算法并非反向传播）
- **关键洞见**：SDI 四规则是预测编码的物理实现

  | SDI 元素 | 预测编码对应 |
  |---|---|
  | E-L 键 | 表征神经元（预测通路） |
  | E-S 键 | 误差神经元（误差通路） |
  | Rule1 STDP | 局部 Hebbian 可塑性 ΔW ∝ ε × x_pre |
  | Rule3 稳态缩放 | 能量 E = ½Σ‖ε_l‖² 最小化 |

- **已更新**：
  - SDI 论文 `references.bib`：新增 rao1999 / friston2018 / whittington2017
  - SDI 论文 Discussion：新增"SDI as Physical Predictive Coding"段落
  - A9 论文框架：补充 FEP↔预测编码↔SDI↔CST 完整等价链
  - Demo SDI 模块：叙事更新为"持续预测-误差-修正动力学系统"
  - 知识库：`PredictiveCoding_BrainLearning_Analysis.md`
- **实验七扩展**：
  - 区分预测通路（E-L 为主）与误差通路（E-S 为主）
  - 测量二者动态分工随演化自发分化
  - 验证：SDI 自发涌现预测编码架构

---

## 实验二十二到三十完成总结 (2026-06-04 23:12 EDT)

### v22-v28 演化路线：核心突破链

**v22-v23**：自适应θ节律 + FEP全局稳态 → σ=2.74, EL=41%→34%（初步改善）
**v24 🔴核心突破**：FEP-STDP深度融合（惊讶度调制STDP速率）→ σ=6.01, EL=29.8%, **FEP=100%收敛**
**v25**：物理第一性 + BCM滑动阈值 → σ=5.35, EL=31.3%, θ自适应
**v26**：多尺度初版（N=100~200） → σ=2.14, EL=34%, 度标度律验证
**v27**：真实connectome多尺度（N=279→1116） → σ=5.0→14.3, EL=29%, 收敛率99%
**v28 🟢工程锁定**：多尺度最终版（N=279→1953） → σ=5.0→19.5, EL=29-31%, **5/5 PASS**

### 功能层级验证

**L4 多任务学习**（趋光+趋化+避碰）
- photo improvement: 46.8% ✅  chemo improvement: 48.5% ✅
- combo_score: 78.3% ✅  interference: 0% ✅
- **switch_cost: 1.0** ⚠️（目标<0.3，需优化）
- 整体：2.5/3达标

**L5 自改进与元学习** ⚠️
- σ未达标、EL未达标、convergence通过 ✅
- overall=False（需诊断修复）

**L6 通用智能**（三任务） 🟡
- avoidance improvement: 429% ✅✅✅  meta speedup: 8695% ✅✅✅
- generalization combo: 1.88 ⚠️（目标>2.0）
- l6_all=False（σ未达标，但学习能力验证成功）

### 最关键发现：EL根本修复

**本地实验系列问题**：EL=97%（过度固化）→ Rule4无法修剪 → Q模块化无法涌现 → Sc被压制 → CST无法进阶

**v27/v28解决方案**：BCM滑动阈值精确控制EL=29% ✅（恢复Bhatt 2009生物参考）

### 对本地实验的直接指导

1. 把v28三个机制移植进本地LIF框架 → **实验二十二升级**
   - BCM滑动阈值（替代固定THETA_LTP=60）
   - FEP惊讶度调制STDP速率
   - EL目标区间控制[15%,35%]
   
2. 预期效果：EL: 97%→29%, Q: 0.45→0.70, CST: L2→L3+

3. 优先级：立刻启动 → 预计修复本地实验的根本缺陷

