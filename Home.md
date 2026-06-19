---
cssclass: dashboard
---

# 🏠  TCC × iNEST 研发中枢

> **`= date(today).format("YYYY-MM-DD dddd")`**  ·  [📊 研发看板](http://127.0.0.1:8900/home/work/.openclaw/workspace/dashboard/index.html)

---

## 🗺️ 整体概览

| 维度 | 🧠 TCC（拓扑中心计算） | 🔧 iNEST（智能涌现系统） |
|:---|:---|:---|
| **理论攻关** | CST 复杂度理论 · 变分自由能 · 标度律 | 涌现条件 · 自组织临界 · 认知架构 |
| **技术研究** | SDI 互连协议 · Chiplet 集成 · 路由算法 | 神经形态芯片 · 脉冲网络 · 忆阻器 |
| **工程落地** | SDSoW 晶圆级系统 · FPGA 原型 · 仿真平台 | 智涌脑硬件 · 软件栈 · 部署工具链 |
| **项目策划** | 海河实验室 · 苏州实验室 · 国家专项 | iNEST 产品路线 · 双轨战略 · 产业合作 |

---

## ⚡ 今日行动建议

> [!tip]- 🤖 AI 扫视近 7 天动态
> ```dataviewjs
const recent = dv.pages('"TCC_1_项目策划" or "iNEST_1_项目策划" or "TCC_2_论文撰写" or "iNEST_2_论文撰写" or "papers" or "00_Inbox"')
  .where(p => p.file.mtime > dv.date("now") - dv.duration("7 days"))
  .sort(p => p.file.mtime, "desc")
  .limit(6);
if (recent.length === 0) {
  dv.paragraph("📭 近一周无活跃文档。");
} else {
  dv.list(recent.map(p => `**${p.file.link}** — ${p.file.mtime.toFormat("MM-dd HH:mm")}`));
}
dv.paragraph("> 💡 优先处理 00_Inbox → 推进论文/专利 → 仿真验证");
> ```

---

## 📊 四维 × 双轨成果看板

### 📝 论文

| 🧠 TCC | 阶段 | 目标 | 🔧 iNEST | 阶段 | 目标 |
|:---|:---|:---|:---|:---|:---|
| ```dataview
TABLE WITHOUT ID
  file.link AS "标题",
  phase AS "阶段",
  journal AS "目标"
FROM "TCC_2_论文撰写"
WHERE phase
SORT file.mtime DESC
LIMIT 3
``` | | | ```dataview
TABLE WITHOUT ID
  file.link AS "标题",
  phase AS "阶段",
  journal AS "目标"
FROM "iNEST_2_论文撰写"
WHERE phase
SORT file.mtime DESC
LIMIT 3
``` | | |

### 📜 专利

| 🧠 TCC | 阶段 | 类型 | 🔧 iNEST | 阶段 | 类型 |
|:---|:---|:---|:---|:---|:---|
| ```dataview
TABLE WITHOUT ID
  file.link AS "标题",
  phase AS "阶段",
  type AS "类型"
FROM "TCC_3_专利撰写"
WHERE phase
SORT file.mtime DESC
LIMIT 3
``` | | | ```dataview
TABLE WITHOUT ID
  file.link AS "标题",
  phase AS "阶段",
  type AS "类型"
FROM "iNEST_3_专利撰写"
WHERE phase
SORT file.mtime DESC
LIMIT 3
``` | | |

### 🧪 仿真实验

| 🧠 TCC | 更新 | 🔧 iNEST | 更新 |
|:---|:---|:---|:---|
| ```dataview
TABLE WITHOUT ID
  file.link AS "实验",
  file.mtime AS "更新"
FROM "sdi_sim"
SORT file.mtime DESC
LIMIT 3
``` | | ```dataview
TABLE WITHOUT ID
  file.link AS "实验",
  file.mtime AS "更新"
FROM "simulation"
SORT file.mtime DESC
LIMIT 3
``` | |

### 🔧 工程开发

| 🧠 TCC | 状态 | 🔧 iNEST | 状态 |
|:---|:---|:---|:---|
| ```dataview
TABLE WITHOUT ID
  file.link AS "模块",
  status AS "状态"
FROM "TCC_4_工程开发"
WHERE status
SORT file.mtime DESC
LIMIT 3
``` | | ```dataview
TABLE WITHOUT ID
  file.link AS "模块",
  status AS "状态"
FROM "iNEST_4_工程开发"
WHERE status
SORT file.mtime DESC
LIMIT 3
``` | |

### 📋 项目策划

| 🧠 TCC | 阶段 | 截止 | 🔧 iNEST | 阶段 | 截止 |
|:---|:---|:---|:---|:---|:---|
| ```dataview
TABLE WITHOUT ID
  file.link AS "项目",
  phase AS "阶段",
  deadline AS "截止"
FROM "TCC_1_项目策划"
WHERE phase
SORT file.mtime DESC
LIMIT 3
``` | | | ```dataview
TABLE WITHOUT ID
  file.link AS "项目",
  phase AS "阶段",
  deadline AS "截止"
FROM "iNEST_1_项目策划"
WHERE phase
SORT file.mtime DESC
LIMIT 3
``` | | |

---

## 📥 收件箱（待分类）

```dataview
TABLE WITHOUT ID
  file.link AS "笔记",
  file.cday AS "导入日期"
FROM "00_Inbox"
WHERE file.name != "00_Inbox 使用说明"
SORT file.cday DESC
LIMIT 8
```

> 处理完移动到 `03_Topics/<分类>/` 并打标签

---

## 🔬 最新文献摄入

```dataview
TABLE WITHOUT ID
  file.link AS "标题",
  file.mtime AS "日期"
FROM "Literature" or "03_Topics/Web-Clips" or "papers"
SORT file.mtime DESC
LIMIT 6
```

---

> *TCC × iNEST  ·  理论 → 技术 → 工程 → 项目  ·  `$= date(today).format("YYYY-MM-DD")`*
