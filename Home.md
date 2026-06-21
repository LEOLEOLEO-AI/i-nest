---
cssclass: dashboard
---

# 🏔️ TCC × iNEST 研发中枢

```dataviewjs
const now = dv.date("now");
const weekdays = ["星期日","星期一","星期二","星期三","星期四","星期五","星期六"];
const wk = weekdays[now.weekday];
const total = dv.pages().length;
const inbox = dv.pages('"00_Inbox"').where(p => p.file.name != ".gitkeep").length;
const pipeIcon = inbox > 0 ? "⏳ 待处理" : "✅ 畅通";

// Git status check
let gitStatus = "Git ✓";
try {
    const { execSync } = require("child_process");
    const hash = execSync("git rev-parse --short HEAD", {cwd: app.vault.adapter.basePath, timeout: 3000}).toString().trim();
    gitStatus = "Git " + hash;
} catch(e) {}

dv.el("p", "📅 **" + now.toFormat("yyyy年MM月dd日") + " " + wk + "** · **" + total + "** 篇笔记 · 收件箱 **" + inbox + "** 篇 · 管道 " + pipeIcon + " · " + gitStatus);
```

---

## ⚡ 快捷操作

```button
name 🔄 Git 同步
type command
action obsidian-git:pull
color blue
```

```button
name 📥 打开收件箱
type command
action switcher:open
color green
```

```button
name 🔍 搜索笔记
type command
action search:search-in-all-files
color purple
```

```button
name 📊 今日日记
type command
action daily-notes:goto-today
color orange
```

---

## 🧠 双轨研发总览

> **TCC** — 拓扑中心计算 · 理论纵深 · 架构突破  
> **iNEST** — 类脑神经形态工程 · 系统集成 · 产业落地

```dataviewjs
const tccPages = dv.pages().where(p => {
    const fname = p.file.name.toLowerCase();
    return fname.includes("tcc") || (p.tags && p.tags.some(t => t.toLowerCase().includes("tcc")));
});
const inestPages = dv.pages().where(p => {
    const fname = p.file.name.toLowerCase();
    return fname.includes("inest") || (p.tags && p.tags.some(t => t.toLowerCase().includes("inest")));
});

const tccCount = tccPages.length;
const inestCount = inestPages.length;

const tccRecent = tccPages.sort(p => p.file.mtime, "desc").limit(5);
const inestRecent = inestPages.sort(p => p.file.mtime, "desc").limit(5);

dv.header(3, "🟦 TCC — 拓扑中心计算 (" + tccCount + " 篇)");
dv.table(["笔记", "修改日期"], tccRecent.map(p => [p.file.link, p.file.mtime.toFormat("MM-dd HH:mm")]));

dv.header(3, "🟩 iNEST — 类脑神经形态 (" + inestCount + " 篇)");
dv.table(["笔记", "修改日期"], inestRecent.map(p => [p.file.link, p.file.mtime.toFormat("MM-dd HH:mm")]));
```

---

## 📈 研发维度

| 维度 | TCC | iNEST | 成果形态 |
|------|-----|-------|---------|
| 📐 理论攻关 | 拓扑表示论·计算复杂性 | 神经动力学·脉冲编码 | 论文·专著 |
| 🔬 技术研究 | 图计算引擎·分布式拓扑 | 存算一体·忆阻器阵列 | 专利·技术报告 |
| ⚙️ 工程落地 | FPGA原型·工具链 | 硬件加速器·仿真平台 | 可复用IP·产品代码 |
| 📋 项目策划 | 基金申请·白皮书 | 产业孵化·标准提案 | 项目指南·可行性报告 |

---

## 📋 今日任务

```dataview
TASK
FROM "30_TCC" OR "40_iNEST" OR "60_MOC"
WHERE !completed AND file.mtime >= date(today) - dur(3 days)
LIMIT 10
```

---

## 🔗 关键入口

- 📊 [[60_MOC/00_Diagnostic_Report|系统诊断报告]] — 知识库健康检查
- 🔍 [[60_MOC/00_Needs_Review|待审核列表]] — 歧义文件处理
- 📘 [[30_TCC/TCC_Master_Index|TCC 主索引]] — 拓扑中心计算全景
- 📗 [[40_iNEST/iNEST_Master_Index|iNEST 主索引]] — 类脑工程全景
- 📚 [[10_Library/Paper_Library|论文库]] — 学术文献管理
- 💡 [[20_Ideas/Idea_Garden|灵感花园]] — 创意孵化器
- 📝 [[99_Journal/Weekly_Review|周度回顾]] — 每周进展记录

---

> 📌 *数据刷新于页面加载时 · Git 自动同步每 30 分钟执行一次 · 完整诊断请查看 [[60_MOC/00_Diagnostic_Report|诊断报告]]*
