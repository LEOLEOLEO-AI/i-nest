# Claw Computer 同步 Gitee 指令

## 触发词
对话中出现 **"同步gitee"** / **"sync gitee"** / **"推送到gitee"** 时执行。

## 仓库信息
- **地址**: `https://gitee.com/iBrainNest/i-nest.git`
- **分支**: `main`
- **本地路径**: `D:\Obsidian\home\work\.openclaw\workspace` （即当前工作区）

## 同步协议 (Pull-First → 分类提交 → Push)

执行增强版同步脚本：
```powershell
powershell -ExecutionPolicy Bypass -File "D:\Obsidian\home\work\.openclaw\workspace\scripts\gitee_sync.ps1"
```

仅查看变更（不提交）：
```powershell
powershell -ExecutionPolicy Bypass -File "D:\Obsidian\home\work\.openclaw\workspace\scripts\gitee_sync.ps1" -StatusOnly
```

## 内容分类（提交时自动标记）
| 分类 | 目录 |
|------|------|
| 代码 | `iNEST_4_工程开发/`, `TCC_4_工程开发/`, `scripts/`, `skills/` |
| 论文 | `papers/`, `iNEST_2_论文撰写/`, `TCC_2_论文撰写/` |
| 专利 | `iNEST_3_专利撰写/`, `TCC_3_专利撰写/` |
| 知识库 | `knowledge_graph/`, `01_MOC/`, `03_Topics/`, `99_Journal/` |
| 仿真 | `simulation/` |
| 灵感 | `iNEST_灵感池/`, `00_Inbox/` |

## 同步后输出格式
- 远程拉取的提交数
- 本地变更分类统计（[代码]X [论文]Y ...）
- 推送是否成功 + 提交哈希
