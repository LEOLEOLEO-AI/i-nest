# 🏠 TCC + iNEST 研发中枢

> 最后更新：2026-06-19 | [研发看板](http://127.0.0.1:8900/home/work/.openclaw/workspace/dashboard/index.html) | [投资演示](http://127.0.0.1:8900/home/work/.openclaw/workspace/dashboard/investor/index.html) | [超级流水线](http://127.0.0.1:8900/home/work/.openclaw/workspace/iNEST_RnD_SuperFlow_v3.md)

---

## ⚡ 快速命令

| 命令 | 说明 |
|---|---|
| `powershell scripts/startup_sync.ps1` | 🔄 Gitee 版本同步 + 流水线 |
| `python scripts/update_dashboard.py` | 📊 更新研发看板数据 |
| `powershell scripts/iNEST_pipeline.ps1` | 🧪 运行 L1-L6 六层流水线 |
| `python scripts/quality_gate.py` | 🛡️ 质量门控检查 |
| `python scripts/clip_article.py <url>` | ✂️ 手动剪藏一篇文章 |

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

## 📆 近三日进展与今日计划

| 日期 | 维度 | 进展 |
|---|---|---|
| **6.17** | 📝 论文 | CST_RG 论文 v1.1 修订完成 |
| | 🧠 iNEST | CST 公理化框架定稿 |
| **6.18** | 🔧 TCC | SDI 仿真实验报告 v2 |
| | 🤖 系统 | 微信机器人 clawbot 上线 |
| **6.19** ← | 🤖 系统 | CC-Connect 微信桥接部署 |
| | ✂️ 工具 | LLM 智能剪藏（DeepSeek 分类+摘要） |
| | 📊 看板 | 研发主页 Home.md 创建 |
| | 🔄 同步 | 每日自动 Gitee 同步脚本 |
| | 🛡️ 守护 | 预览服务器看门狗保活 |

### 今日计划

- [ ] CC-Connect 转发文章 → Obsidian 全链路实测
- [ ] CST 仿真参数扫描启动
- [ ] 专利 CST_涌现智能 权利要求书初稿

---

## 🌐 信息摄入

| 来源 | 今日新增 | 快捷入口 |
|---|---|---|
| 得到大脑 | 待统计 | [Feishu_Inbox](http://127.0.0.1:8900/Feishu_Inbox/) |
| Genspark | 待统计 | [Literature](http://127.0.0.1:8900/home/work/.openclaw/workspace/Literature/) |
| 微信 iNEST | CC-Connect 在线 | 转发文章自动入 00_Inbox |

---

## 🛡️ 系统守护

| 服务 | 保活机制 |
|---|---|
| 预览服务器 :8900 | 计划任务每 5 分钟自检重启 |
| CC-Connect 微信 | daemon 模式 |
| 剪藏队列 | clip_watcher.py 持续运行 |

---

## 📂 目录索引

```
work/.openclaw/workspace/
├── 00_Inbox/          ← 待处理入口
├── Papers/            ← 论文撰写
├── Patents/           ← 专利撰写
├── TCC_1_项目策划/     ← TCC 项目
├── iNEST_Research/    ← iNEST 研究
├── Literature/        ← 文献笔记
├── dashboard/         ← 研发看板
└── simulation/        ← CST 仿真
```

---

## 🤖 Codex 任务模板

```
# 论文撰写
codex "读取 Papers/B0_Engineering，完成 Methods 章节"

# 专利撰写
codex "基于 TCC 的 SDI 方案撰写发明专利权利要求书"

# 文献分析
codex "读取 Literature/ 最新文献，生成研究趋势报告"

# 仿真实验
codex "运行 simulation/CST_simulation.py，分析涌现临界点"
```

---

*Codex 中枢 | Obsidian 知识库 | 得到大脑 + Genspark 摄入 | CC-Connect 移动端*