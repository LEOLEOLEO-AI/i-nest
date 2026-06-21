---
cssclass: dashboard
---

# 📋 歧义文件审查中心

> 📊 自动分类: **139/543** (26%) | 剩余 **404** 待审查 | `$= date(today).format("YYYY-MM-DD HH:mm")`

---

## 🔍 待审文件

```dataviewjs
const files = dv.pages('"_archive/_needs_review"')
  .where(p => p.file.name != ".gitkeep")
  .sort(p => p.file.mtime, "desc");

dv.paragraph("共 " + files.length + " 个文件待审查。点击文件名在 Obsidian 中打开。");

const rows = [];
for (const p of files) {
  const name = p.file.name;
  const text = (p.file.content || "").replace(/^---[\s\S]*?---/, "").trim().substring(0, 100);
  rows.push([
    dv.fileLink(p.file.path, false, name.substring(0, 55)),
    text
  ]);
}

dv.table(
  ["文件名（点击打开）", "内容预览"],
  rows
);
```

---

## 🛠️ 操作方式

### Obsidian 内拖拽（推荐）

1. 点击文件名在 Obsidian 中打开
2. 判断归属后拖动到目标目录:
   - 🧠 **TCC** → `30_TCC/31_Theory/_from_review/`
   - 🔧 **iNEST** → `40_iNEST/41_Theory/_from_review/`
   - 📚 **文献** → `10_Library/Papers/`
   - 💡 **灵感** → `20_Ideas/Insights/`
3. `Ctrl+R` 刷新本页

### 命令行

```bash
python 90_System/scripts/review_ambig.py stats
python 90_System/scripts/review_ambig.py move "文件名.md" tcc|inest
```

---

## 📊 已完成

```dataviewjs
const progress = JSON.parse(await dv.io.load("60_MOC/_review_progress.json"));
const reviewed = progress?.reviewed || {};
const entries = Object.entries(reviewed);
if (entries.length === 0) {
  dv.paragraph("暂无已完成项目");
} else {
  const rows = entries.map(function(e) {
    return [e[0].substring(0, 55), e[1].target, e[1].moved_to || ""];
  });
  dv.table(["文件", "归类", "新位置"], rows);
}
```

---

> 💡 每次审查后按 `Ctrl+R` 刷新 | `python 90_System/scripts/review_ambig.py batch` 重新生成建议
