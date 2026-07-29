# Obsidian Vault 诊断报告

**诊断时间**: 2026-07-30 00:25  
**诊断范围**: D:\obsidian\vault 全库  
**诊断工具**: 文件系统扫描 + 语法检查 + Git 状态 + 状态文件解析

---

## 一、核心指标

| 指标 | 数值 | 状态 |
|------|------|------|
| Markdown 文件 | 5,633 | - |
| Python 脚本 | 1,169 | - |
| Canvas 文件 | 2 | - |
| 目录数 | 786 | - |
| 知识图谱节点 | 5,612 | 停滞 (自 7/26 起无增长) |
| 知识图谱边 | 8,950 | 停滞 |
| Git 未提交变更 | 884 | 危险 (最后提交 7/23) |
| 管道暂停时长 | 3 天 (自 7/27) | 瘫痪 |

---

## 二、上次会话修复情况 (6/14 完成)

| # | 项目 | 状态 | 详情 |
|---|------|------|------|
| 1 | 10_Inbox 合并 | ✅ 完成 | arxiv-auto (10文件) 已移入 00_Inbox，10_Inbox 已删除 |
| 2 | .env 创建 | ✅ 完成 | 包含 S2_API_KEY + DEEPSEEK_API_KEY 两行 |
| 3 | .gitignore 更新 | ✅ 完成 | .env 已加入 .gitignore 第 58 行 |
| 4 | S2 密钥移除 (pipeline_v3.py) | ✅ 完成 | 改为 `os.environ.get("S2_API_KEY", "")` |
| 5 | DeepSeek 密钥移除 (4 脚本) | ✅ 完成 | codex_obsidian_linkage.py, evolution_engine.py, process_inbox.py 已移除硬编码 |
| 6 | S2 限流参数改进 | ✅ 完成 | DELAY 1→3.2s, RETRY_DELAY 5→15s, MAX_RETRIES 1→3 |
| 7 | pipeline_guard 超时提升 | ✅ 完成 | 20→35 分钟 |
| 8 | dotenv 导入 | ✅ 完成 | pipeline_v3.py 第 23-26 行 |
| 9 | arXiv 指数退避 | ⚠️ 有语法错误 | 逻辑正确但缩进错误导致文件无法编译 |
| 10 | Git 清理 | ❌ 未完成 | 884 个变更仍未提交 |
| 11 | 密钥轮换 | ❌ 未完成 | 旧密钥仍在 GitHub 历史中 |
| 12 | 其余 8 个脚本密钥 | ❌ 未完成 | 见下方详细清单 |
| 13 | 根目录清理 | ❌ 未完成 | 51 个文件仍散落在根目录 |
| 14 | 重复文件归档 | ❌ 未完成 | 1,246 个仍堆积 |

---

## 三、仍需修复的问题

### P0 — 紧急 (管道完全瘫痪)

#### 3.1 pipeline_v3.py 语法错误

**文件**: `90_System/scripts/pipeline_v3.py`  
**行号**: 497  
**错误类型**: `IndentationError: unindent does not match any outer indentation level`  
**原因**: 上次会话编辑 arXiv 429 重试逻辑时，`if e.code == 429:` 块缩进过深，导致 `elif e.code >= 500:` 无法匹配

**当前代码 (有错误)**:
```python
            except urllib.error.HTTPError as e:
                    if e.code == 429:          # ← 缩进多了 4 格
                        wait = 15 * (2 ** attempt)
                        log("  arXiv %s: 429 rate limit, waiting %ds (exponential backoff)..." % (label, wait))
                        time.sleep(wait)
                elif e.code >= 500:             # ← IndentationError
```

**修复方案**: 统一缩进到 `except` 块级别

**影响**: 管道完全无法运行，所有 Windows 计划任务调用 pipeline_v3.py 都会立即失败

#### 3.2 8 个脚本仍含硬编码 DeepSeek 密钥

以下脚本中仍有 `REDACTED_DEEPSEEK_KEY` 硬编码:

| # | 文件 | 行号 | 当前代码 |
|---|------|------|----------|
| 1 | `deepseek_analyze.py` | 11 | `API_KEY = "sk-0174b6..."` (直接赋值) |
| 2 | `deep_analyze.py` | 10 | `API_KEY = "sk-0174b6..."` (直接赋值) |
| 3 | `deep_analyze_v2.py` | 10 | `API_KEY = "sk-0174b6..."` (直接赋值) |
| 4 | `gen_insights.py` | 9 | `KEY = os.environ.get("DEEPSEEK_API_KEY") or "sk-0174b6..."` (有 fallback) |
| 5 | `link_engine.py` | 13 | `KEY = os.environ.get("DEEPSEEK_API_KEY") or "sk-0174b6..."` (有 fallback) |
| 6 | `processing_workflow.py` | 15 | `KEY = os.environ.get("DEEPSEEK_API_KEY") or "sk-0174b6..."` (有 fallback) |
| 7 | `reconstruct_formulas.py` | 8 | `client = OpenAI(api_key="sk-0174b6...", ...)` (直接赋值) |
| 8 | `task_planner.py` | 8 | `KEY = "sk-0174b6..."` (直接赋值) |

**影响**: 密钥仍可通过 Git 历史被提取

### P1 — 重要

#### 3.3 Git 变更堆积

- **未提交变更**: 884 个 (比上次诊断的 830 增加了 54 个)
- **最后提交**: `0bd45330 sync: 完整同步 2026-07-23` — **6 天前**
- **影响**: 本地修改未同步到 GitHub/Gitee，存在丢失风险

#### 3.4 API 密钥暴露

- S2 API 密钥和 DeepSeek API 密钥在 7/23 之前的 Git 提交中明文存在
- GitHub 仓库为公开仓库
- **需在平台轮换**: Semantic Scholar + DeepSeek 控制台重新生成密钥

#### 3.5 根目录文件散乱 (51 个)

| 类型 | 数量 | 典型文件 |
|------|------|----------|
| .py | 27 | `_build_v23.py`, `_fix_v27.py`, `analyze_hemibrain.py`, `convert_docx.py` |
| .md | 10 | `Home.md`, `MEMORY.md`, `RULES.md`, `V25投稿修改执行计划.md` |
| .sh | 3 | `chromium-env.sh` |
| .bak | 2 | `AGENTS.md.bak.20260604`, `MEMORY.md.bak.20260604` |
| .tar.gz | 1 | `iNEST_archive_20260509.tar.gz` |
| .aux/.log/.out/.toc | 4 | LaTeX 编译残留 |
| 其他 | 4 | `desktop-readme.html`, `LICENSE` 等 |

#### 3.6 重复文件堆积

- **位置**: `80_Archive/duplicates/`
- **数量**: 1,246 个 .md 文件
- **状态**: 上次会话确认"归档到独立目录"，但尚未执行

### P2 — 改进

#### 3.7 Inbox 文件堆积

| 子目录 | 文件数 | 说明 |
|--------|--------|------|
| 00_Inbox/ (根级) | 51 | 得到大脑/手动导入 |
| 00_Inbox/arxiv-auto/ | 10 | arXiv 自动导入 (原 10_Inbox) |
| 00_Inbox/_pipeline_insights/ | 102 | 管道生成的 insights |
| 00_Inbox/13_Codex/ | 0 | 空 |
| 00_Inbox/01_PDF_Source/ | 0 | 空 |
| 00_Inbox/02_网页剪藏/ | 0 | 空 |
| **总计** | **163** | 无自动分类和概念提取 |

#### 3.8 Karpathy 架构未实现

- 无 `raw/` 层 (原始材料保护区)
- 无 `wiki/` 层 (LLM 编译的结构化知识)
- 无 `schema.md` (LLM 操作指令)
- 无概念提取和交叉链接自动化
- 无健康检查机制
- 无自进化循环

#### 3.9 研究状态停滞

- **evolution_queue.json**: 12 个待处理项 (最后更新 7/26)
- **hypothesis_registry.json**: 4 个假设 (H1-H4)，无自动验证
- **research_state.json**: 最后更新 7/26
- **research_task_proposals.json**: 最后更新 7/26

---

## 四、子系统健康度评分

| 子系统 | 评分 | 状态 | 主要问题 |
|--------|------|------|----------|
| 数据管道 | 0% | 瘫痪 | 语法错误 + 暂停 3 天 |
| 密钥安全 | 40% | 部分修复 | 4/12 脚本已修，8 个待处理 |
| Git 卫生 | 10% | 危险 | 884 个变更未提交 |
| 目录结构 | 30% | 部分改善 | Inbox 已合并，根目录仍乱 |
| 自进化系统 | 0% | 未实现 | 无 Karpathy 架构 |
| 研究状态 | 30% | 停滞 | 12 队列项 + 4 假设无进展 |
| 知识图谱 | 50% | 静态 | 5,612 节点/8,950 边，无增长 |
| 插件生态 | 80% | 良好 | 18 插件启用，Smart Connections 运行中 |

**总体健康度: ~29%**

---

## 五、建议修复优先级

1. **立即**: 修复 pipeline_v3.py 缩进错误 → 恢复管道
2. **立即**: 清除 8 个脚本中剩余的硬编码密钥
3. **尽快**: 提交 884 个 Git 变更 (先更新 .gitignore)
4. **尽快**: 在 Semantic Scholar + DeepSeek 平台轮换密钥
5. **本周**: 清理 51 个根目录文件 → 移入 90_System/scripts/ 或归档
6. **本周**: 归档 1,246 个重复文件到 _duplicates_archive/
7. **本周**: 处理 163 个 Inbox 积压文件
8. **下周**: 实现 Karpathy 架构 (raw/ + wiki/ + schema.md)
9. **下周**: 实现自进化系统 (import_processor + task_recommender)
10. **后续**: 重设计仪表盘 + 更新计划任务
