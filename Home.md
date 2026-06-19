# 🏠 TCC + iNEST 研发中枢

> 最后更新：2026-06-19 | [研发看板](http://127.0.0.1:8900/home/work/.openclaw/workspace/dashboard/index.html) | [投资演示](http://127.0.0.1:8900/home/work/.openclaw/workspace/dashboard/investor/index.html) | [超级流水线](http://127.0.0.1:8900/home/work/.openclaw/workspace/iNEST_RnD_SuperFlow_v3.md)

---

## ⚡ 快速命令

| 命令                                      | 说明                  |     |
| --------------------------------------- | ------------------- | --- |
| `powershell scripts/startup_sync.ps1`   | 🔄 Gitee 版本同步 + 流水线 |     |
| `python scripts/update_dashboard.py`    | 📊 更新研发看板数据         |     |
| `powershell scripts/iNEST_pipeline.ps1` | 🧪 运行 L1-L6 六层流水线   |     |
| `python scripts/quality_gate.py`        | 🛡️ 质量门控检查          |     |
| `python scripts/clip_article.py <url>`  | ✂️ 手动剪藏一篇文章         |     |

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

## 🔬 Autoresearch 智能研发

| 场景 | 命令 | 说明 |
|---|---|---|
| 📝 论文修改 | `$autoresearch fix` | 逐条消灭审稿意见，直到零错误 |
| 📜 专利撰写 | `$autoresearch plan` → `$autoresearch` | 规划 → 迭代生成说明书+权利要求书 |
| 🧪 CST 仿真 | `$autoresearch debug` | 假设 → 测试 → 证伪循环，加速调参 |
| 🔍 文献分析 | `$autoresearch reason` | 8轮对抗辩论，收敛核心结论 |
| 🛡️ 代码审查 | `$autoresearch security` | STRIDE+OWASP 安全审计 |
| 🚀 版本发布 | `$autoresearch ship` | 8阶段检查表 → 发布 |
| 💡 创新探索 | `$autoresearch improve` | 研究 ICP 挑战 → 发现改进 → 生成 PRD |
| 🎯 场景覆盖 | `$autoresearch scenario` | 12维边缘案例生成，防遗漏 |

### 今日推荐

```
# 论文完稿：对抗辩论 + 查缺补漏
$autoresearch reason "CST_RG_Paper_v1.1" 
$autoresearch scenario "CST_RG_Paper_v1.1"

# 专利撰写：规划→迭代
$autoresearch plan "CST涌现智能发明专利"
```

## 🤖 Codex 任务模板

```dataviewjs
const codexTasks = [
  ["📝 论文撰写", '读取 Papers/CST_RG_Paper_v1.1，完成修订'],
  ["📜 专利撰写", '基于 TCC 的 SDI 方案撰写发明专利权利要求书'],
  ["📚 文献分析", '读取 Literature/ 最新文献，生成研究趋势报告'],
  ["🧪 仿真实验", '运行 simulation/CST_simulation.py，分析涌现临界点'],
];
codexTasks.forEach(([label, prompt]) => {
  const btn = dv.el("button", label, { title: prompt });
  btn.style = "margin:2px 4px; padding:4px 10px; cursor:pointer";
  btn.onclick = () => {
    navigator.clipboard.writeText(prompt);
    new Notice(`已复制到剪贴板: ${label}`);
  };
});
```

> 点击按钮复制提示词，粘贴到 Codex 或微信 iNEST 执行

---

*Codex 中枢 | Obsidian 知识库 | 得到大脑 + Genspark 摄入 | CC-Connect 移动端*