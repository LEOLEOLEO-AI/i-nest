---
provenance: external
---

﻿# Zotero + Better BibTeX 完整使用攻略

> TCC iNEST 论文撰写管线 | 2026-07-15

---

## 一、当前配置状态

| 项目 | 状态 |
|------|:--:|
| Zotero 9 (64-bit) | ✅ 已安装 |
| Better BibTeX (BBT) | ✅ 已安装 |
| Citekey 格式 | `auth.lower + shorttitle(3,3) + year` |
| 示例 citekey | `vaswaniAttentionAllYou2017` |
| 快速复制样式 | IEEE |
| iNEST 文献库 BibTeX | `D:\inest\download\inest_library.bib` (241KB, 200条) |

---

## 二、立即操作：导入 + 自动导出

### Step 1：导入 iNEST 文献库

```
Zotero 菜单 → File → Import
→ 选择 D:\inest\download\inest_library.bib
→ 勾选 "Place imported collections and items into new collection"
→ 命名: iNEST_Library
→ 点击 Import
```

### Step 2：设置自动导出（一次配置，永久生效）

```
1. 右键点击 Zotero 中的 "iNEST_Library" 集合
2. 选择 "Export Collection..."
3. 格式选 "Better BibTeX"
4. 勾选 "Keep updated"（关键！）
5. 保存到: D:\inest\download\inest_library.bib
```

之后每次在 Zotero 中添加/修改文献，`.bib` 文件自动更新。

### Step 3：处理剩余 38 条

```
1. 在 Zotero 中选中 iNEST_Library 集合
2. 将 D:\inest\download 中的 PDF 拖入 Zotero
3. 右键 PDF → "Retrieve Metadata for PDF"
4. Zotero 自动补全标题/作者/DOI
5. BBT 自动更新 .bib 文件
```

---

## 三、论文撰写工作流

### 流程 A：Markdown + Pandoc（当前主力）

```
Zotero 管理文献 → BBT 导出 .bib → Pandoc 引用渲染
```

**在 Markdown 中引用：**
```markdown
Transformer 架构首次提出于 @vaswaniAttentionAllYou2017，
后续的 GPT 系列在此基础上扩展 @brownLanguageModelsAre2020。
```

**生成 Word/PDF：**
```bash
pandoc paper.md --bibliography=inest_library.bib --citeproc -o paper.docx
```

### 流程 B：Word + Zotero 插件（备用）

```
Zotero Word 插件 → 插入引用 → 自动生成参考文献列表
```

**操作：**
1. 打开 Word → Zotero 选项卡
2. 光标放需要引用的位置 → "Add/Edit Citation"
3. 搜索作者/关键词 → 选择文献
4. 写完 → "Add/Edit Bibliography" → 自动生成参考文献列表
5. 换期刊：Document Preferences → 选样式（Nature / IEEE / APA...）

### 流程 C：LaTeX / Overleaf

```latex
\usepackage[backend=biber,style=nature]{biblatex}
\addbibresource{D:/inest/download/inest_library.bib}

Transformer 架构首次提出于 \cite{vaswaniAttentionAllYou2017}。

\printbibliography
```

---

## 四、常用操作速查

### 添加文献

| 方法 | 操作 | 适用 |
|------|------|------|
| **拖 PDF** | 直接拖入 Zotero → 自动检索元数据 | 有 PDF 文件 |
| **DOI 添加** | 工具栏魔棒图标 → 输入 DOI | 有 DOI |
| **网页保存** | 浏览器 Zotero Connector 插件 | 网页/arXiv |
| **ISBN 添加** | 魔棒图标 → 输入 ISBN | 书籍 |
| **手动创建** | 右键 → New Item → 选类型 | 无标识符 |

### 组织文献

| 操作 | 快捷键/方式 |
|------|------------|
| 新建集合 | 右键 → New Collection |
| 添加标签 | 选中条目 → Tags 面板 → Add |
| 搜索 | `Ctrl+K` 全局搜索 |
| 高级搜索 | Edit → Advanced Search |
| 查重 | 右键集合 → Duplicate Detection |

### Better BibTeX 核心功能

| 功能 | 操作 |
|------|------|
| 自动导出 | 右键集合 → Export → Better BibTeX → 勾选 Keep Updated |
| 修改 citekey | 选中条目 → Extra 字段 → 加 `citation-key: mykey` |
| 批量生成 citekey | 选中多条 → 右键 → Better BibTeX → Refresh Citekey |
| 固定 citekey | 右键条目 → Better BibTeX → Pin Citekey（防止自动改名） |
| 导出带附件 | Export → Better BibTeX → 勾选 Export Files |

### 引用样式切换

在 Word 中：Zotero → Document Preferences → 选择样式：
- `Nature` — Nature 系列期刊
- `ieee` — IEEE 期刊/会议
- `apa` — APA 格式
- `chinese-gb7714-2005-numeric` — 国标中文参考文献
- `cell` — Cell/NMI 等

---

## 五、论文投稿前的 Zotero 检查清单

- [ ] 所有引用条目在 Zotero 中元数据完整（作者、年份、DOI、期刊名、卷期页码）
- [ ] 无重复条目（右键集合 → Duplicate Detection）
- [ ] citekey 全部 pin 住（选中全部 → Better BibTeX → Pin Citekey）
- [ ] `.bib` 文件已更新（检查修改时间）
- [ ] Word 中 Zotero 引用已刷新（Refresh）
- [ ] 目标期刊的 CSL 样式已应用

---

## 六、常见问题

**Q: Zotero 同步满了（300MB 免费）怎么办？**
A: 用 Zotero 本地模式 + Git 同步 `.bib` 文件。PDF 用 OneDrive/坚果云。Zotero 设置 → Sync → 取消 File Syncing。

**Q: citekey 重复怎么办？**
A: BBT 自动加后缀区分（`smith2023a`, `smith2023b`）。也可手动在 Extra 字段指定。

**Q: 换了机器怎么办？**
A: 新机器装 Zotero + BBT，把 `inest_library.bib` 和 PDF 文件夹复制过去，重新设置自动导出。

**Q: 中文文献怎么办？**
A: Zotero 支持中文。CSL 样式选 `chinese-gb7714-2005-numeric`。中文 PDF 拖入 Zotero 也能自动检索（知网/万方需 Zotero Connector 插件）。

---

> **TCC iNEST 论文管线快速链接：**
> - 文献库 BibTeX: `D:\inest\download\inest_library.bib`
> - KF 列表: `D:\inest\download\failed_imports_v2.txt`
> - Pandoc: `C:\Users\LEO\pandoc\pandoc-3.6.3\pandoc.exe`
