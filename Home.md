# 🏠 TCC + iNEST 研发中枢

> 最后更新：2026-06-19

---

```button
name 📊 研发看板
type link
action http://127.0.0.1:8900/home/work/.openclaw/workspace/dashboard/index.html
color blue
```
```button
name 💰 投资演示
type link
action http://127.0.0.1:8900/home/work/.openclaw/workspace/dashboard/investor/index.html
color purple
```
```button
name 🔄 Gitee 同步
type command
action Execute CODE: powershell D:\Obsidian\scripts\startup_sync.ps1
color green
```
```button
name 📊 更新看板
type command
action Execute CODE: python D:\Obsidian\home\work\.openclaw\workspace\90_System\scripts\update_dashboard.py
color yellow
```

---

## ⚡ 快速命令

| 命令 | 说明 |
|---|---|
| `powershell D:\Obsidian\scripts\startup_sync.ps1` | 🔄 Gitee 版本同步 + 流水线 |
| `python 90_System/scripts/update_dashboard.py` | 📊 更新研发看板数据 |
| `python 90_System/scripts/quality_gate.py` | 🛡️ 质量门控检查 |

---

## 📋 四维看板

### 📝 论文

| 论文 | 阶段 | 目标期刊 | 下次行动 |
|---|---|---|---|
| B0_Engineering | 撰写中 | Nature Electronics | 补充仿真数据 |
| B1_ARS_投稿版 | 修改中 | IEEE Access | 审稿意见修订 |

### 📜 专利

| 专利 | 阶段 | 类型 | 下次行动 |
|---|---|---|---|
| CST_涌现智能 | 撰写中 | 发明 | 权利要求书 |

### 🔧 TCC 工程研发

| 模块 | 状态 | 下次行动 |
|---|---|---|
| SDI 互联协议 | 设计阶段 | 协议验证 |
| Chiplet 集成方案 | 研究阶段 | 调研报告 |

### 🧠 iNEST 理论研究

| 方向 | 状态 | 下次行动 |
|---|---|---|
| CST 理论仿真 | 进行中 | 参数扫描 |
| 涌现条件推导 | 进行中 | 数学证明 |
| 文献综述 | 进行中 | Genspark 搜索 |

---

## 🌐 信息摄入

| 来源 | 今日新增 | 快捷入口 |
|---|---|---|
| 得到大脑 | 待统计 | [00_Inbox](00_Inbox/) |
| Genspark | 待统计 | [Literature](Literature/) |
| 微信 iNEST | CC-Connect 在线 | 转发文章自动入 00_Inbox |

---

## 🛡️ 系统守护

| 服务 | 保活机制 |
|---|---|
| 预览服务器 :8900 | 计划任务每 5 分钟自检重启 |
| CC-Connect 微信 | daemon 模式 |

---

## 📂 目录索引

- `00_Inbox/` — 待处理入口
- `Papers/` — 论文撰写
- `Patents/` — 专利撰写
- `TCC_1_项目策划/` — TCC 项目
- `iNEST_Research/` — iNEST 研究
- `Literature/` — 文献笔记
- `dashboard/` — 研发看板
- `simulation/` — CST 仿真

---

*Codex 中枢 | Obsidian 知识库 | 得到大脑 + Genspark 摄入 | CC-Connect 移动端*
