# iNEST 研发神经网络 · 五工具协同工作流 v2.0

> **大道至简 · Complexity comes from Simplicity**
> 自组织临界机制——找到那"一个"涌现方程

---

## 工具角色映射（iNEST 六层智能架构）

| 层级 | 智能等级 | 核心工具 | 职责 | 输入 | 输出 |
|------|----------|----------|------|------|------|
| **L1** | 感知 Perception | 📱 得到大脑 + 🔍 Genspark | 知识采集 | 互联网 + 课程 | GetNotes_Inbox + Web-Clips |
| **L2** | 反应 Reaction | 📓 Obsidian | 知识拓扑化 | Inbox + Clips | 双向链接知识图谱 |
| **L3** | 适应 Adaptation | 🌳 TreeSolo | 灵感树生成 | 灵感池 + 知识图谱 | 思维树 + 决策 |
| **L4** | 创造 Creation | 💻 Codex | 代码/撰写执行 | 计划 + 决策 | 论文/专利/代码/指南 |
| **L5** | 通用 General | 📊 研发看板 | 全局状态维护 | 四象限进展 | 每日看板 + 计划 |
| **L6** | 超智能 Super | 💼 投资演示 | 周度成果合成 | 全局进展 | 投资者演示网页 |

---

## 五象限并行架构（四维 + 一脑）

```
┌─────────────────────────────────────────────────────┐
│                    🧠 人类决策中枢                     │
│         "灵感对不对？要不要继续推进？"                   │
│         每个质量门控 → 人来判定 → 迭代/推进             │
└──────────┬──────────┬──────────┬──────────┬──────────┘
           │          │          │          │
    ┌──────▼────┐┌────▼────┐┌────▼────┐┌────▼────┐
    │ 📝 论文   ││ 📜 专利  ││ 📋 指南  ││ 💻 代码  │
    │ TCC+iNEST ││ TCC+iNEST││ TCC+iNEST││ TCC+iNEST│
    │ 理论/架构 ││ 方法/系统││ 白皮书/ ││ 引擎/仿真│
    │           ││          ││ 路线图   ││ 平台     │
    └──────────┘└─────────┘└─────────┘└─────────┘
```

---

## 每日工作流（自动执行）

### Phase 1: 感知层 L1（约 5 分钟）
```powershell
# 触发: 每日启动 / 计划任务
.\scripts\iNEST_pipeline.ps1
```

1. **得到大脑** → `pull_getnotes.py` 拉取最新笔记
2. **GetNotes** → `getnotes_importer.py` 导入 Obsidian
3. **Genspark** → `iNEST_crawler.py` 爬取前沿论文
4. **原子化** → `paper_atomizer.py` 生成双向链接笔记

### Phase 2: 反应层 L2（约 2 分钟）
5. **Gitee 同步** → `gitee_sync.ps1` 推送到远程仓库
6. **Genspark 桥接** → 导出 Web-Clips 索引供 Genspark 检索

### Phase 3: 适应层 L3（约 1 分钟）
7. **TreeSolo 桥接** → 导出灵感池供 TreeSolo 生成思维树
8. **质量门控 G1** → 扫描新灵感，标记待审核

### Phase 4: 创造层 L4（人工触发）
9. **Codex** → 用户决策后，执行具体研发任务
   - "推进 TCC 论文撰写"
   - "实现 SDI v31 仿真实验"
   - "更新专利组合文档"

### Phase 5: 通用层 L5（约 1 分钟）
10. **研发看板** → `update_dashboard.py` 自动刷新
11. **质量门控 G4** → 整合检查
12. **打开看板** → 浏览器展示今日计划

### Phase 6: 超智能层 L6（仅周一，约 1 分钟）
13. **投资演示** → `investment_demo.py` 周度更新
14. **打开演示页** → 浏览器展示投资材料

---

## 质量门控系统（人类决策节点）

```
灵感产生 → G1 灵感门控 → [人] 是否值得推进？
              ↓ 通过
           G2 研究门控 → [人] 可行性检查？
              ↓ 通过
           G3 输出门控 → [人] 成果质量达标？
              ↓ 通过
           G4 整合门控 → [人] 与全局体系整合？
              ↓ 通过
          🎯 成果纳入全局进展 & 版本更新
```

### 使用方式
```powershell
# 查看质量门控状态
python scripts/quality_gate.py

# 扫描待审核灵感
python scripts/quality_gate.py scan

# 对灵感进行 G1 门控评分
python scripts/quality_gate.py check G1_Inspiration "Idea_Name"
```

---

## 版本追踪体系

| 层级 | 追踪方式 | 频率 | 文件 |
|------|----------|------|------|
| 知识采集 | Git (Gitee) | 每日 | `gitee_sync.ps1` |
| 看板数据 | `data.js` v2 每日条目 | 每日 | `update_dashboard.py` |
| 投资演示 | `investor_data.js` | 每周 | `investment_demo.py` |
| 论文版本 | Markdown frontmatter `version` | 按需 | Obsidian 笔记 |
| 代码版本 | Git + 语义版本号 | 按需 | `simulation/` |

---

## 桥接文件（跨工具数据交换）

所有桥接文件位于 `state/bridges/`:

| 文件 | 方向 | 用途 |
|------|------|------|
| `genspark_index.json` | Obsidian → Genspark | Web-Clips 索引供 Genspark 检索 |
| `treesolo_input.json` | Obsidian → TreeSolo | 灵感池导出供思维树生成 |
| `treesolo_decisions.json` | TreeSolo → Obsidian | TreeSolo 决策回流到知识库 |
| `quality_gate_log.json` | 全局 | 所有质量门控检查记录 |

---

## 快速命令参考

```powershell
# 完整六层流水线
.\scripts\iNEST_pipeline.ps1

# 仅质量门控检查
.\scripts\iNEST_pipeline.ps1 -QualityGateOnly

# 跳过知识采集（已有最新数据时）
.\scripts\iNEST_pipeline.ps1 -SkipPerception

# 强制周度模式（非周一也要更新投资演示）
.\scripts\iNEST_pipeline.ps1 -WeeklyMode

# 仅更新看板
python scripts/update_dashboard.py

# 仅更新投资演示
python scripts/investment_demo.py

# 每日快速启动（兼容旧版）
.\scripts\daily_startup.ps1
```

---

## 文件清单

| 文件 | 类型 | 说明 |
|------|------|------|
| `scripts/iNEST_pipeline.ps1` | 编排器 | 六层五工具协同流水线 |
| `scripts/investment_demo.py` | 生成器 | 投资演示数据周更新 |
| `scripts/quality_gate.py` | 门控 | 四阶段质量检查 |
| `scripts/update_dashboard.py` | 生成器 | 研发看板每日更新 |
| `scripts/iNEST_crawler.py` | 采集器 | 论文爬虫 |
| `scripts/paper_atomizer.py` | 处理器 | 论文原子化 |
| `scripts/pull_getnotes.py` | 采集器 | 得到大脑笔记拉取 |
| `scripts/getnotes_importer.py` | 处理器 | 笔记导入 Obsidian |
| `scripts/gitee_sync.ps1` | 同步器 | Gitee 版本同步 |
| `scripts/daily_startup.ps1` | 启动器 | 保留兼容旧版 |
| `dashboard/index.html` | 看板 | 研发全景看板网页 |
| `dashboard/investor/index.html` | 演示 | 投资演示网页 |
| `dashboard/investor/investor_data.js` | 数据 | 投资演示数据 |

---

## 日常操作节奏

| 时间 | 动作 | 工具 |
|------|------|------|
| **每日开机** | 自动运行流水线 L1-L5 | Pipeline |
| **上午** | 查看研发看板，确认今日计划 | 看板 |
| **工作中** | 在 Codex 执行具体的研发任务 | Codex |
| **灵感来时** | 记入 Obsidian 灵感池或 GetNotes | Obsidian/得到 |
| **每周一** | Pipeline 自动更新投资演示 L6 | Pipeline |
| **需要决策** | 打开质量门控，人对灵感评分 | Quality Gate |
| **需要全局视角** | 打开投资演示或研发看板 | 浏览器 |

---

*"让每个工具发挥各自所擅长的，人来做只有人才能做的决策。"*
