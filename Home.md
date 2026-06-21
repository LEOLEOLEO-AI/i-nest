---
cssclass: dashboard
---

# 🏔️ TCC × iNEST 研发中枢

```dataviewjs
const now = dv.date("now");
const weekdays = ["星期日","星期一","星期二","星期三","星期四","星期五","星期六"];
const wk = weekdays[now.weekday];
const total = dv.pages().length;
const inbox = dv.pages('"00_Inbox"').length;
const pipeText = inbox > 0 ? "⚠️ 待处理" : "✅ 畅通";
dv.span("📅 **" + now.toFormat("yyyy年MM月dd日") + " " + wk + "** · **" + total + "** 篇笔记 · 收件箱 **" + inbox + "** 篇 · 管道 " + pipeText);
```

---

## ⚡ 快捷操作

```dataviewjs
const btns = [
  ["🔄 Git 同步", "obsidian-git:pull"],
  ["🔍 全局搜索", "omnisearch:show-modal"],
  ["📅 今日日记", "daily-notes"],
  ["📂 快速切换", "switcher:open"],
];
const container = dv.el("div", "");
btns.forEach(([label, cmd]) => {
  const btn = container.createEl("button", { text: label });
  btn.style.cssText = "margin:4px 6px;padding:6px 14px;border-radius:6px;border:1px solid var(--interactive-accent);background:var(--interactive-accent);color:white;cursor:pointer;font-size:14px;";
  btn.onmouseover = () => { btn.style.opacity = "0.85"; };
  btn.onmouseout = () => { btn.style.opacity = "1"; };
  btn.onclick = () => app.commands.executeCommandById(cmd);
});
```

---

## 🧠 双轨研发总览

> **TCC** — 拓扑中心计算 · 理论纵深 · 架构突破  
> **iNEST** — 类脑神经形态工程 · 系统集成 · 产业落地

### 🟦 TCC — 拓扑中心计算

```dataview
TABLE file.mtime AS "修改日期"
FROM "30_TCC"
SORT file.mtime DESC
LIMIT 5
```

### 🟩 iNEST — 类脑神经形态

```dataview
TABLE file.mtime AS "修改日期"
FROM "40_iNEST"
SORT file.mtime DESC
LIMIT 5
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

## 📋 近期活跃任务

```dataview
TASK
FROM "30_TCC" OR "40_iNEST" OR "60_MOC"
WHERE !completed
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

---

> 📌 *数据刷新于页面加载时 · Git 自动同步每 30 分钟执行一次*
