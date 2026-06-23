---
cssclass: dashboard
---

# 🏥 Vault 系统诊断报告

> `$= date(today).format("YYYY-MM-DD HH:mm")` | 文件总数 ~3650 md | 双向链接 11555 条

---

## ✅ 健康指标

| 指标 | 状态 | 说明 |
|:---|:---|:---|
| 目录结构 | 🟢 良好 | 9 个核心管道目录就位，深度扫描仅 3 个散落文件 |
| 双向链接 | 🟢 健康 | 11555 条 WikiLink，0 条断裂回链 |
| TCC 分类 | 🟢 完成 | 1435 md 归入 30_TCC |
| iNEST 分类 | 🟢 完成 | 991 md 归入 40_iNEST |
| Git 同步 | 🟢 正常 | Gitee 自动推送 |

---

## 🔴 需要处理的问题

### 问题 1: 根目录散落 (最优先)

| 类型 | 数量 | 示例 |
|:---|:---|:---|
| 元文件 | 9 | AGENTS.md, README.md, MEMORY.md, SOUL.md... |
| iNEST 文件 | 5 | iNEST-Home.md, iNEST_RnD_Workflow_v2.md... |
| TCC/SDI 文件 | 3 | TCC 计算范式 — 全景导航.md, SDI化合物键_四型架构.md... |
| 系统文件 | 2 | Tasks Plugin..., conflict-files-obsidian-git.md |
| 根目录保留 | 1 | Home.md (首页插件需要) |
| **合计** | **20** | |

**处理**: 移动到对应管道目录。Obsidian 的 `[[链接]]` 按文件名解析，**移动不会断链**。

| 文件 | 目标 |
|:---|:---|
| AGENTS.md ~ TOOLS.md (9个) | `60_MOC/meta/` |
| iNEST-*.md (5个) | `40_iNEST/` |
| TCC*.md, SDI*.md (3个) | `30_TCC/` |
| Tasks*, conflict* (2个) | `90_System/` |

### 问题 2: 根目录脚本/配置文件

| 类型 | 数量 | 处理 |
|:---|:---|:---|
| Python 脚本 | 13 | → `90_System/scripts/_migrated/` |
| JSON/TXT 配置 | 4 | → `90_System/config/` |
| iNEST_archive tar.gz | 1 | → `_archive/` |
| desktop-readme.html | 1 | 删除或移到 `_archive/` |

### 问题 3: 收件箱积压

| 指标 | 数值 |
|:---|---:|
| 00_Inbox 总文件 | **140** |
| 其中 Get 笔记 | 3 |
| 近 7 天新增 | 140 (全部！) |
| 待分类歧义文件 | 404 |

**根因**: 自动抓取管道 (`daily_crawl.py`) 和 LLM 分类 (`process_inbox.py`) 尚未执行。文件持续堆积。

**处理**:
1. 运行 `python 90_System/scripts/process_inbox.py --limit 20` 分批处理
2. 处理一批提交一批，避免大量断链风险
3. 质量低的直接归档到 `_archive/low_quality/`

### 问题 4: 同名文件重复 (1643 组)

| 重复次数 | 文件名 | 说明 |
|:---|:---|:---|
| 52x | SKILL.md | 模板文件，可批量清理 |
| 18x | 00_宽屏目录仪表盘.md | 旧 MOC 残留 |
| 9x | README.md | 空模板 |
| 8x | 无标题.md | 空白笔记 |
| 6x | 参考_双轨战略框架总览_v3.md | 同一文件多份拷贝 |
| 6x | 论文计划列表.md | TCC/Output 各一份 |

**处理原则**: 
- SKILL.md / README.md / 无标题.md → 保留 `90_System/templates/` 中的模板，其余删除
- 内容重复 → 保留最新版本，旧版本移到 `_archive/duplicates/`
- 不自动删除，先移到 `_archive/` 审查

### 问题 5: 00_MOC 残留

3 个文件在 `00_MOC/` (已在之前merge中遗漏):
- `iNEST-MOC.md` → `60_MOC/`
- `TCC-MOC.md` → `60_MOC/`
- `健康诊断-MOC.md` → `60_MOC/`

---

## 📋 推荐执行顺序

| 优先级 | 任务 | 风险 | 预计时间 |
|:---|:---|---:|:---|
| 🔴 P0 | 迁移根目录 20 个散落 md | 无 (链接按文件名) | 1 min |
| 🔴 P0 | 清理根目录 35 个脚本/配置 | 无 | 2 min |
| 🟡 P1 | 迁移 00_MOC 残留 3 文件 | 无 | 1 min |
| 🟡 P1 | 运行 inbox 处理 (分批 20) | 低 (LLM可能误分类) | 5 min/批 |
| 🟠 P2 | 清理 52 个 SKILL.md 模板副本 | 无 | 1 min |
| 🟠 P2 | 去重同名文件 (保留1份，其余归档) | 中 (需人工确认) | 10 min |
| 🟢 P3 | 注册 Windows 定时任务 | 无 | 2 min |

---

## ⚡ 管道健康检查

| 管道 | 脚本 | 状态 |
|:---|:---|:---|
| 每日抓取 | `daily_crawl.py` | ❌ 未运行过 |
| 收件箱处理 | `process_inbox.py` | ❌ 未运行过 |
| 链接图谱 | `build_graph.py` | ✅ 手动跑通 |
| 歧义审查 | `review_ambig.py` | ✅ batch 完成 |
| 定时任务 | `setup_scheduler.ps1` | ❌ 未注册 |

> 💡 核心问题: 自动化脚本写好了但没跑。注册定时任务 + 首次手动触发即可激活管道。

---

## 🎯 下一步行动

1. **立即**: 执行 P0 清理 (根目录散落文件)
2. **今天**: 执行 P1 收件箱处理 (分批 20 条)
3. **本周**: 注册定时任务 + 处理歧义文件 404 条
4. **后续**: 去重清理 (P2)
