---
title: "【iNEST知识库】DASHBOARD"
date: 2026-04-29 03:08:41
source: "????"
note_id: 1908472283874286280
note_type: plain_text
tags: []
source: getnote---

# 【iNEST知识库】DASHBOARD

# iNEST 工作台总控面板 (DASHBOARD.md)
> **唯一入口** — 每次会话从这里开始，所有方向实时状态一览
> 最后更新：2026-04-28

provenance: own
---

## 🧭 四条主线实时状态

### 🔬 主线T：理论研究
**负责人**：刘勤让 | **当前阶段**：CST V25论文投稿准备

| 任务 | 文件 | 状态 | 下一步 |
|------|------|------|--------|
| CST V25 论文 | `02_Papers_论文/CST_Intelligence_Emergence_Paper_V25_FINAL.md` | ✅投稿就绪（V25全量修复完成） | LaTeX打包→arXiv提交 |
| CST V25 Word版 | `02_Papers_论文/CST_Theory_V25_FINAL.docx` | ✅已生成 | 同步修复 |
| LaTeX打包 | `02_Papers_论文/arXiv_submission/` | 🟡进行中（bib已完成，tex构建中） | 完成main.tex→pdflatex编译→zip打包 |
| Mouse>π问题 | V25论文§3.2 | ✅已修复（L5注脚已加入V25） | — |
| B2 P-Mapping素材 | `02_Papers_论文/B组_SDI-CC互连体系/B2_P-Mapping_素材_V3.md` | 📝V3完备 | 启动论文写作 |
| B7 Route≡Transform | `02_Papers_论文/TCC_专利与论文/论文A_B7_Route-Transform_ASPLOS27.md` | 📋框架完成 | §3理论证明展开 |

---

### ⚗️ 主线S：仿真验证
**负责人**：刘勤让 | **当前阶段**：sdi_network v22仿真，等待双阈值收敛

| 任务 | 文件 | 状态 | 下一步 |
|------|------|------|--------|
| sdi_network主仿真 | `00_KnowledgeBase_知识库/CST仿真平台/sdi_network_v8.py` | 🟡运行中 | σ≈1 & τ同时收敛目标 |
| C.elegans复现 | `00_KnowledgeBase_知识库/CST仿真平台/sdi_v8_real_connectome.png` | ✅已完成 | — |
| 40系统UCCP验证数据 | `00_KnowledgeBase_知识库/05_Datasets_仿真与实验数据/Simulation_Results/` | ✅FINAL冻结 | `cst_16samples_FINAL.json`为基准 |
| V25 Figures生成 | `02_Papers_论文/Figures/gen_figures_v25.py` | ✅6张300DPI已生成 | Figure 3是否替换为3轴散点图（待决策） |
| nano-SDIO原型脚本 | `04_Code_代码/nano_SDIO.py` | 📋存在但需验证 | 补充算力对标数据（立项材料用） |

---

### ⚙️ 主线E：关键技术工程实现
**负责人**：刘勤让 | **当前阶段**：TCC-16原语集IP核设计准备

| 任务 | 文件 | 状态 | 下一步 |
|------|------|------|--------|
| P1专利（核心方法） | `02_Papers_论文/TCC_专利与论文/P1_TCC方法与系统专利_框架.md` | 📋框架完成 | 扩写实施方式，目标2026-05 CNIPA申请 |
| P2专利（硬件IP核） | `TCC_IP_Portfolio/专利/P2_可重构原语硬件IP核阵列/` | 📋权利要求框架 | 补充背景技术+实施方式 |
| P3专利（拓扑FFT） | `TCC_IP_Portfolio/专利/P3_可编程拓扑重构FFT/` | 📋权利要求框架 | 补充数学等价性证明 |
| P4专利（SDK编译） | `TCC_IP_Portfolio/专利/P4_NCCL_MPI_BLAS自动映射编译/` | 📋权利要求框架 | 补充MLIR方言定义 |
| P5专利（自演化） | `TCC_IP_Portfolio/专利/P5_能量最小化拓扑自演化/` | ⚠️待补充全文 | 从原对话复制全文 |
| FPGA原型（VCK190） | `04_Code_代码/collective_comm_naas/` | 🟡进行中 | FFT 800ns实测数据收集 |
| TCC-16 RTL | （待创建） | ⬜未启动 | SystemVerilog 11 IP cores |
| SDI控制器 | （待创建） | ⬜未启动 | 64×64 crossbar + shadow register |

---

### 🏭 主线P：产品开发
**负责人**：刘勤让 | **当前阶段**：MVP规划确认，海河实验室专项申报

| 任务 | 文件 | 状态 | 下一步 |
|------|------|------|--------|
| iNEST MVP计划 | `02_Papers_论文/iNEST_MVP_Plan_V1.md` | 📋V1存在 | 细化三大应用场景路线图 |
| 海河实验室专项V8 | `05_Projects_项目/海河实验室重大专项/[V8]_...正式发布版.md` | ✅正式版 | 等待反馈/修订 |
| 战略规划总文档 | `TCC_IP_Portfolio/战略规划/`（⚠️待补充） | ⬜缺文件 | 从原对话复制①号文件 |
| 中汽合作智驾专项 | `00_KnowledgeBase_知识库/专项布局/智驾晶上异构集成_中汽合作_项目指南_v2.md` | ✅V2完成 | — |
| 卫星智能体专项 | `00_KnowledgeBase_知识库/卫星智能体/卫星智能体重大专项建议_v9_FINAL.md` | ✅FINAL | — |
| 苏州实验室合作 | `00_KnowledgeBase_知识库/专项布局/苏州实验室合作/` | ✅完成 | — |

---

## 🚨 当前最高优先级任务（Top 5）

| 优先级 | 任务 | 主线 | 预计时间 |
|--------|------|------|---------|
| 🔴P1 | 完成LaTeX打包 → arXiv提交 → Nature MI投稿 | T | 2小时 |
| 🔴P2 | P1专利说明书扩写完成→2026-05 CNIPA申请 | E | 1周 |
| 🟠P3 | B7 Route≡Transform §3理论证明展开 | T | 3天 |
| 🟠P4 | nano-SDIO.py算力对标数据补充（立项材料） | S/P | 1天 |
| 🟡P5 | TCC-LTC范式图片 + 范式跃迁图已入库，补充论文A Figure说明 | T | 1小时 |

---

## 📁 目录结构速查

```
workspace/
├── DASHBOARD.md          ← 你在这里，总控入口
├── 00_KnowledgeBase_知识库/
│   ├── 02_CST_核心理论著作/    ← CST理论核心定义、TCC命名规范
│   ├── 03_Inbox_文献与碎片/    ← 1105个文献（需定期消化）
│   ├── CST仿真平台/            ← 仿真脚本+结果（主线S）
│   └── 专项布局/               ← 各专项申报材料
├── 01_Ideas_想法/              ← 6个待消化想法
├── 02_Papers_论文/
│   ├── CST V25 FINAL ★         ← 当前最新论文
│   ├── TCC_专利与论文/          ← P1-P4框架+论文A/B/C框架
│   ├── A组_CST基础理论/
│   ├── B组_SDI-CC互连体系/
│   └── Figures/                ← 6张V25配图
├── 04_Code_代码/
│   ├── nano_SDIO.py            ← 原型仿真
│   └── collective_comm_naas/   ← FPGA集合通信仿真
├── 05_Projects_项目/
│   ├── 海河实验室重大专项/      ← V8正式版
│   └── NSFC/卫星智能体/
├── TCC_IP_Portfolio/           ← P2-P4专利框架+论文A/C框架
└── memory/                     ← AI记忆文件
```

---

## 🔄 同步机制说明

| 来源 | 当前状态 | 同步方式 |
|------|---------|---------|
| 印象笔记 | ❌无自动同步 | 手动导出enex/html上传 |
| Get笔记 | ❌无自动同步 | 手动导出docx/md上传 |
| VM本地 | ✅实时 | 直接写入 |
| AI记忆 | ✅每次会话flush到memory/ | `memory/2026-04-XX.md` |

**导入流程**（需要时执行）：
1. 印象笔记/Get笔记导出 → 上传到对话
2. AI解析 → 存入 `03_Inbox_文献与碎片/` 或对应专项目录
3. 高价值内容 → 提炼摘要追加到相关论文/专利文件

---

## 📌 关键约束（每次会话继承）

- 严格手动模式：禁止任何定时任务/cron
- TCC命名：全库只用 `tcc.*` 前缀，TCC-16
- β₁/Betti数：不入V25论文，留companion paper
- X₄定义：Watts-Strogatz σ + tanh归一化
- UCCP参考：Q_rand=0.02，floor ε=0.01
- 文件路径在回复中必须用反引号包裹
- P1 CNIPA目标：2026年5月；P2：2026年7月
- 论文A（B7）ASPLOS'27截止：2026年9月9日


---

## ⚙️ 任务分流规则（Token节约）

| 任务类型 | 执行方式 | Token消耗 | 典型示例 |
|---------|---------|----------|---------|
| Wiki维护、断链修复、索引更新 | exec 运行脚本 | 零 | python3 kb_inspector.py |
| 格式整理、目录调整、分类归档 | exec 运行脚本 | 零 | bash批处理 |
| 结构化Wiki生成、中等内容创作 | subagent（小模型） | 小 | sessions_spawn 小模型 |
| 学术推理、论文分析、复杂理论研究 | 主会话 Claude | 正常 | CST理论讨论、专利可行性分析 |
| 核心算法设计、复杂代码开发 | sessions_spawn Claude | 正常 | TCC-RTL设计、SDI控制器 |

巡检工具：
- 全量巡检：python3 /vault/kb_inspector.py
- 快速模式：python3 /vault/kb_inspector.py --quick
- 自动修复死链接：python3 /vault/kb_inspector.py --fix

---
## 🔒 Atlas 只读目录（AI禁止修改正文）

| 目录 | 内容说明 |
|------|------|
| KB/01_Atlas_SDSoW-TCC/ | 战略规划，定稿文件，AI只读 |
| KB/02_Atlas_CST-iNEST/ | CST理论核心定义、TCC命名规范，AI只读 |

---

## 🗂️ KB 目录结构（物理迁移完成，2026-04-28起）

KB/ 根目录（workspace/KB/）下均为真实目录：
- 01_Atlas_SDSoW-TCC/ ← 宏观规划与战略报告（AI只读）
- 02_Atlas_CST-iNEST/ ← CST核心理论著作、TCC命名规范（AI只读）
- 03_Efforts_CST-iNEST_仿真平台/ ← CST仿真脚本与结果
- 04_Efforts_CST-iNEST_超线性增益/ ← 网络超线性增益知识库
- 05_Efforts_SDSoW-TCC_专项布局/ ← 各专项申报材料
- 06_Efforts_SDSoW-TCC_卫星智能体/ ← 卫星智能体重大专项

尚未迁移（原路径保留）：
- ../02_Papers_论文/ ← CST V25论文、TCC专利论文、B组SDI
- ../04_Code_代码/ ← nano_SDIO、FPGA仿真
- ../05_Projects_项目/ ← 海河实验室、NSFC、卫星项目
- ../TCC_IP_Portfolio/ ← P1-P5专利框架、论文A/B/C框架
- ../00_KnowledgeBase_知识库/03_Inbox/ ← 1105个文献（原地保留）


<!-- orphan-cleanup: linked to MOC -->
## 来源回链

- [[TCC_Master_Index]]
