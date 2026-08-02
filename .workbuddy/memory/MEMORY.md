# 项目长期记忆 — Obsidian 知识库 (D:/obsidian/vault)

## 项目定位
TCC（拓扑中心计算）+ iNEST（复杂网络涌现智能）双方向研究知识库。
采用 Karpathy LLM-Wiki 自进化框架，三层心智模型：
**源材料层（只读）→ 编译知识层 `wiki/`（机器生成）→ 产出层 `50_Output/`（对外交付）**

工作目标六类：论文、专利、专著、项目指南、核心代码、原型产品。

## 运行环境（必读）
- vault 内 Python 脚本一律用**系统 Python 3.10**：
  `C:/Users/LEO/AppData/Local/Programs/Python/Python310/python.exe`
  bash 里没有 `python` / `python3` 命令。
- 双远端：`github`（主）、`gitee`。日常推 `git push github main`。

## 目录编号契约（强约束，见 schema.md §2.1）
30_TCC 用 **3x**，40_iNEST 用 **4x**，职能一一对应，编号不得撞车：

| 职能 | TCC | iNEST |
|---|---|---|
| 理论 | 31_Theory | 41_Theory |
| 技术 | 32_Tech | 42_Tech |
| 开发/工程 | 33_Dev | 43_Engineering |
| 项目 | 34_Projects | 44_Projects |
| 仿真 | 35_Simulation | 45_Simulation |

产出层：51_Papers / 52_Patents / 53_Monographs / 54_Code / 55_Guides /
56_Prototypes / 59_Presentations。

目录卫生：禁止自嵌套 `X/X/`；禁止中英同义并存（统一 `01_论文`，不再建裸 `论文/`、`Papers/`）。

## 运行时基础设施（保护名单，永不移动/重命名）
被活跃脚本硬编码引用，移动会直接打断每日自进化：
- `raw/` → import_processor.py（Genspark / 得到大脑 / Codex 落地区）
- `logs/` → pipeline_guard、pipeline_v3、daily_generator、research_publisher
- `state/` → pipeline_guard.py
- `knowledge_graph/` → pipeline_v3.py、knowledge_graph.py（neo4j）

## 关键脚本
- `90_System/scripts/self_evolve.py` — 每日自进化编排器（automation-1785546922604，每日 03:00）
- `90_System/scripts/vault_restructure.py` — 目录重组维护（默认 DRY RUN，`--apply` 才执行）

## 数据安全经验
- **`.gitignore` 有全局 `*.html` 规则**：移动 HTML 到新路径会静默脱离版本控制，须 `git add -f`。
- **别用裸 `git add -A`**：会吞进 AI 工具残留（`.claudian-plus/retrieval/index.json` 曾达 268MB，
  超 GitHub 100MB 限制致 push 被拒）。相关目录已加入 `.gitignore`。
- 大规模改动前先建 git 检查点；改动后用 **blob 哈希集合比对**验证零丢失
  （注意 `git ls-tree -r` 哈希在字段 [2]，`git ls-files -s` 在字段 [1]）。
- `80_Archive/_duplicates_archive/`（957 文件）内为**唯一内容，不可删**；
  内容级精确重复已于上一轮清理归零。
