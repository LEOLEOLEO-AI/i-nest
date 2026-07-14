# 三平台 Gitee 同步协议 v2

> 同步指令: **"同步gitee"** 或 **"sync gitee"**  
> 中央仓库: `https://gitee.com/iBrainNest/i-nest.git`  
> 分支: `main`

---

## 架构

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│   Obsidian   │       │   Genspark   │       │ Claw Computer│
│  (本地知识库) │       │  (云端AI协作) │       │  (Agent工作区)│
└──────┬───────┘       └──────┬───────┘       └──────┬───────┘
       │   push/pull         │   push/pull         │   push/pull
       └──────────────────────┼──────────────────────┘
                     ┌────────▼────────┐
                     │  Gitee 中央枢纽  │
                     │  i-nest.git     │
                     └─────────────────┘
```

**核心原则**: Pull-First（先拉后推），任何平台同步前必须先拉取 Gitee 最新内容。

---

## 一、Obsidian 同步

**本地路径**: `D:\Obsidian\home\work\.openclaw\workspace`

### 对话触发
当用户说 **"同步gitee"** 时，Agent 执行：

```powershell
powershell -ExecutionPolicy Bypass -File "D:\Obsidian\scripts\gitee_sync.ps1"
```

### 同步流程
1. `git fetch` → 检查远程更新
2. `git pull` → 拉取其他平台的变更
3. 自动分类检测 → 代码/论文/专利/知识库/仿真/灵感
4. 生成结构化提交信息 → `sync: [代码]X [论文]Y ...`
5. `git push` → 推送到 Gitee

### 状态查看
```powershell
powershell -ExecutionPolicy Bypass -File "D:\Obsidian\scripts\gitee_sync.ps1" -StatusOnly  # 只看变更
powershell -ExecutionPolicy Bypass -File "D:\Obsidian\scripts\gitee_sync.ps1" -DryRun       # 预览不提交
```

---

## 二、Genspark 同步

**本地路径**: `~/i-nest-sync/`

### 首次设置
```bash
git clone https://gitee.com/iBrainNest/i-nest.git ~/i-nest-sync
```

### 对话触发
当用户说 **"同步gitee"** 时，Agent 执行完整 Pull-First 流程。

### Genspark 产出内容对应目录
| 产出类型 | 存放路径 |
|---------|---------|
| 论文草稿 | `papers/iNEST/` |
| 专利草稿 | `iNEST_3_专利撰写/` |
| 仿真代码 | `iNEST_4_工程开发/` |
| 数据分析 | `simulation/reports/` |
| 知识条目 | `03_Topics/` |
| 灵感创意 | `iNEST_灵感池/` |

---

## 三、Claw Computer 同步

**本地路径**: `D:\Obsidian\home\work\.openclaw\workspace`（与 Obsidian 共享）

### 对话触发
当用户说 **"同步gitee"** 时，执行与 Obsidian 相同的同步脚本。

---

## 仓库目录结构

```
i-nest/
├── 00_Inbox/               # 收件箱
├── 01_MOC/                 # 内容地图
├── 03_Topics/              # 主题研究
│   ├── AI-ML/
│   ├── Chip-Hardware/
│   ├── Concepts-Theory/    # v10-v30 分析报告
│   └── ...
├── 90_System/              # 系统配置
├── 99_Journal/             # 日志
├── dashboard/              # 仪表盘
├── iNEST_灵感池/           # 灵感
├── iNEST_1_项目策划/       # 项目策划
├── iNEST_2_论文撰写/       # 论文撰写 (13 篇)
├── iNEST_3_专利撰写/       # 专利撰写 (7 篇)
├── iNEST_4_工程开发/       # 工程代码
│   └── fpga/               # FPGA verilog 源码
├── inspiration_engine/     # 灵感引擎
├── knowledge_graph/        # 知识图谱
├── memory/                 # 记忆库
├── papers/                 # 论文库
│   ├── iNEST/              # (8 篇论文)
│   └── TCC/
├── scripts/                # 工具脚本
│   ├── gitee_sync.ps1      # Windows 同步脚本
│   ├── Genspark_gitee_sync.md
│   └── Claw_gitee_sync.md
├── simulation/             # 仿真 (新增)
│   ├── data/               # v9-v30 仿真结果数据
│   ├── connectome/         # connectome 数据集
│   ├── reports/            # 仿真分析报告
│   └── investor_demo/
├── skills/                 # Agent Skills
├── state/                  # 状态追踪
├── TCC_*/                  # TCC 项目
└── _archive_02_Zettelkasten/ # 归档
```

---

## 冲突解决策略

1. **Pull 时冲突** → stash 本地 → pull → stash pop
2. **合并冲突** → 保留双方版本，以 `.conflict` 后缀标记
3. **禁止操作** → 绝不用 `--force` 推送，不用 `git reset --hard` 覆盖

---

## 版本历史
- v1 (2026-06-03): 初始 auto-sync 脚本
- v2 (2026-06-05): 三平台同步架构 + 分类提交 + 状态追踪
