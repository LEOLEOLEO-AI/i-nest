---
provenance: external
---

---
title: "从「员工」到「公司」：Paperclip重新定义AI Agent规模化落地的开源平台"
date: 2026-06-20 07:34:18
source: "????"
note_id: 1913313503364789704
note_type: link
tags: [AI链接笔记, Paperclip, AI Agent, 多Agent编排]
source: getnote---

# 从「员工」到「公司」：Paperclip重新定义AI Agent规模化落地的开源平台

### **🚀 项目概述与发展历程**

**项目背景**  
2026年3月10日，Paperclip项目首次发布，核心解决"如何协调多个AI Agent（OpenClaw、Claude Code、Codex等）成为有目标、有预算、有治理的团队"问题。

**三个月关键进展**  
| 维度 | 具体数据/成果 |
| :--- | :--- |
| **社区增长** | GitHub Stars达**70.3k**，Forks 13k+，社区贡献者124人 |
| **版本迭代** | 发布v2026.403至v2026.609.0等十余个版本 |
| **核心进化** | 从"核心编排引擎"升级为"完整可扩展的AI公司控制平面" |

**定位与价值主张**  
- **核心定位**：如果OpenClaw是"员工"，Paperclip就是"公司"  
- **产品属性**：开源、自托管的**多Agent编排与治理平台**  
- **核心能力**：提供组织结构图、目标对齐、心跳机制、预算控制、治理审批等企业级功能  

### **🔑 核心功能解析**

#### **1. Bring Your Own Agent（自带Agent）**
- **支持范围**：Claude Code、Codex、Cursor、OpenClaw（HTTP/Webhook）、Bash/CLI、Grok Build、Cursor Cloud等  
- **关键增强**：Grok Build本地运行时适配器（v2026.517）、Cursor Cloud适配器（v2026.512）  
- **实现机制**：通过`tools/agent-shim/`提供沙箱运行时；**只要能接收心跳（heartbeat），就能被"雇佣"**

#### **2. Org Chart & Goal Alignment（组织结构与目标对齐）**
- **Agent属性**：角色、头衔、汇报线、权限、预算、Job Description  
- **目标层级**：完整**目标祖先链（goal ancestry）**：Company Mission → Project Goal → Agent Goal → Task  
- **上下文感知**：通过运行时注入的`SKILL.md`，使Agent始终明确"为什么做这件事"

#### **3. Heartbeats & Routines（心跳与例行任务）**
- **核心机制**：**DB-backed wakeup queue with coalescing**（数据库驱动的唤醒队列，支持合并、预算检查等）  
- **唤醒触发**：按计划（如Copywriter每4小时）或事件（任务分配、@-mention）  
- **例行任务**：支持cron、webhook、API触发，带并发和追赶策略  
- **状态持久化**：跨心跳恢复任务上下文，避免从头开始（liveness continuations + orphaned run recovery）

#### **4. Ticket / Issue System（工单系统）**
- **核心功能**：公司/项目/目标链接、原子检出、blocker依赖、子Issue checklist、视频附件（v2026.609新增）、富文本文档  
- **增强特性**：Source-scoped recovery actions、Issue References（反向链接）、Document Locks（快照保护）  
- **审计能力**：完整工具调用、API请求、决策追踪 + **不可变审计日志**

#### **5. Governance & Approvals（治理与审批）**
- **用户角色**：作为"董事会"批准雇佣、覆盖策略、暂停/恢复/终止Agent、调整预算  
- **结构化交互**：proposals、forms、checkbox confirmation payloads（v2026.609强化）  
- **变更管理**：所有变更可回滚，配置带修订历史

#### **6. Budget & Cost Control（预算与成本控制）**
- **控制机制**：每月每Agent预算，80%软警告，100%硬停止（auto-pause + cancel queued work）  
- **原子保障**：Task checkout和budget enforcement使用事务，杜绝double-work和超支  
- **细粒度追踪**：按company/agent/project/goal/issue/provider/model统计token与成本

#### **7. Workspaces & Plugins & Skills（工作区、插件与技能）**
- **工作区隔离**：项目级覆盖默认路径，支持git worktrees、operator branches  
- **Skills Catalog**（v2026.529）：提供分类`SKILL.md`，运行时注入无需重训，CLI支持install/reset/audit  
- **Plugin System**（v2026.416起）：实例级插件，out-of-process workers，支持独立DB schema和备份

#### **8. 其他生产增强**
- **UI/UX**：移动端就绪、可折叠侧边栏（v2026.609）、全公司模糊搜索、Inline Document Annotations  
- **可观测性**：OpenTelemetry tracing（opt-in）、匿名遥测（可完全关闭）

### **📥 安装与部署指南**

#### **推荐快速开始（npx）**
```bash
npx paperclipai onboard --yes  # 默认本地模式，http://localhost:3100
npx paperclipai onboard --yes --bind lan  # 局域网访问
npx paperclipai onboard --yes --bind tailnet  # Tailscale访问
```
#### **源码安装与开发**
```bash
git clone https://github.com/paperclipai/paperclip.git
cd paperclip
pnpm install  # 需Node 20+ + pnpm 9.15+
pnpm dev  # 启动API + UI（watch模式）
```
**数据库与配置**  
- 默认使用embedded PostgreSQL（数据路径：`~/.paperclip/instances/default/db`）  
- 生产环境可配置外部Postgres：设置`DATABASE_URL`  
- 自动备份：每60分钟，保留30天（路径：`~/.paperclip/instances/default/data/backups`）  

### **💡 高效使用方法与最佳实践**

#### **核心工作流**
1. **定义目标层级**：先设置Company Mission，再建Project/Goal，任务自动继承上下文  
2. **添加Agent**：通过UI/API选择适配器，设置预算、角色、汇报线，注入`SKILL.md`  
3. **创建任务**：使用Issue管理子任务、blocker、文档附件，利用Planning Mode规划  
4. **配置例行工作**：通过Routines设置cron/webhook触发，自动创建Issue并唤醒Agent  

#### **避坑建议**
- 心跳依赖稳定网络/DB；使用worktree时注意seeding模式（minimal/full）  
- 插件开发时启用`allowLocalPathSources`（仅dev环境）  
- 生产环境建议关闭遥测（`PAPERCLIP_TELEMETRY_DISABLED=1`）  

### **🛠️ 技术原理与架构**

**整体架构**  
- **技术栈**：Monorepo（pnpm workspace）、Node.js API、React UI、PostgreSQL数据库  
- **核心引擎**：心跳执行引擎（DB-backed wakeup queue + 恢复机制）  
- **隔离机制**：所有核心实体严格company-scoped，实现多租户隔离  

**关键技术特性**  
- **原子性保障**：Task checkout和budget enforcement使用数据库事务  
- **技能注入**：`SKILL.md`动态加载到Agent上下文，无需模型重训  
- **插件系统**：out-of-process workers + capability-gated host services  

### **📈 项目发展里程碑（2026年3月以来）**

| 时间 | 关键进展 |
| :--- | :--- |
| **4月** | Plugin System Beta、Multi-User Support、Issue Chat Threads、Execution Policies |
| **5月** | Skills Catalog & CLI、Grok Build Adapter、Cursor Cloud Adapter、Full Company Search |
| **6月** | Company Artifacts页面、Video Attachments、Collapsible Sidebar、Structured Checkbox Interactions |

**未来Roadmap**：Memory/Knowledge、Self-Organization、Automatic Organizational Learning、CEO Chat、Cloud deployments等
