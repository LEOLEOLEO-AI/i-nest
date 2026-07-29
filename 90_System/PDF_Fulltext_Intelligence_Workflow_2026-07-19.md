# PDF 全文科研智能处理方案

## 目标

不再把论文摘要直接当作研究依据。每一篇进入 TCC 或 iNEST 的论文都必须基于可访问的全文、可定位的证据片段和人工确认的研究任务。

## 单一数据流

`Zotero 文献库/PDF/批注 -> 00_Inbox/01_PDF_Source -> 20_Processing/01_PDF_Text -> 20_Processing/02_Fulltext_Analysis -> 60_MOC/05_Task_Review -> 人工批准 -> 06_Task_Plan`

- `01_PDF_Source`: 指向 Zotero PDF 的稳定链接或待处理副本，只作来源追溯；PDF 不进入 Git。
- `01_PDF_Text`: MarkItDown 生成的全文 Markdown；保留 PDF 链接、SHA-256 和转换时间。
- `02_Fulltext_Analysis`: Claudian/Codex 基于全文生成的结构化研究笔记。
- `05_Task_Review`: 只放候选任务；正式计划只能由人工批准后写入。

## Zotero 的职责

Zotero 是论文元数据、原 PDF、阅读批注和引用键的单一信源；Obsidian 不是第二个文献管理器。

- 在 Zotero 中完成 DOI/作者/期刊/年份校对、PDF 保存、阅读和高亮批注。
- 每篇进入全文处理的论文在 Obsidian 只建立一份处理入口，记录 `zotero://` 链接、引用键、DOI 和 PDF SHA-256。
- Zotero 批注先导出或同步到全文分析笔记，作为需要回查原 PDF 的证据候选，不能直接升级为研究结论。
- 推荐启用 Better BibTeX 的自动导出，维护一份只读 `references.bib`；论文写作从 Zotero 引用键出发，不手工维护第二份参考文献表。

建议的全文入口 frontmatter：

```yaml
zotero_uri: "zotero://open-pdf/library/items/ITEM_KEY"
citation_key: "AuthorYearShortTitle"
doi: "..."
source_pdf: "[[PDF 文件或副本]]"
pdf_sha256: "..."
```

## 阶段 0：先盘点，后处理

运行：

```powershell
python D:\Obsidian\vault\90_System\scripts\pdf_fulltext_inventory.py
```

输出：`20_Processing/00_PDF_Fulltext_Inventory.md`。

规则：

- 以 SHA-256 去重，避免同一论文在归档、临时目录和附件目录被重复分析。
- `machine_readable` 才进入 MarkItDown 批量转换。
- `ocr_required` 先 OCR；未经 OCR 的扫描 PDF 不进入 LLM 全文分析。
- 自产出论文、图表 PDF、项目申报书与外部论文分开，不把自身文件误当文献证据。

## 阶段 1：全文转换

MarkItDown 不作为论文全文主转换器。它适合快速预览，但双栏、公式、表格、图注、脚注和参考文献常会失序。

采用双引擎转换：

1. GROBID 作为可机读学术论文的主解析器，输出 TEI XML，保留题名、作者、章节、引文标记、图表和参考文献结构。
2. Docling 作为版式和表格兜底，输出 Markdown 加 JSON 文档结构；用于 GROBID 失败、双栏重排异常或需要表格/图片上下文的论文。
3. 扫描件先 OCR，再走 Docling；OCR 文本必须标注来源，不得直接当作原始排版事实。
4. MarkItDown 仅用于非论文附件或前两种工具不可用时的临时兜底。

建议输出目录：

`20_Processing/01_PDF_Text/`

工具选择和验收：

| PDF 类型 | 首选 | 备用 | 验收 |
|---|---|---|---|
| 出版社/预印本学术论文 | GROBID | Docling | 标题、章节、引文和参考文献结构可识别 |
| 双栏、复杂表格、图文混排 | Docling | GROBID + 原 PDF 回查 | 表格不串列，图注与正文不混合 |
| 扫描版 | OCR + Docling | 人工处理 | 关键引用可在原 PDF 页定位 |
| 普通附件 | MarkItDown | Docling | 正文可读、链接和图片保留 |

转换笔记的 frontmatter 最少包含：

```yaml
source_pdf: "[[原始PDF.pdf]]"
source_url: "https://..."
doi: "..."
pdf_sha256: "..."
text_status: extracted
analysis_status: pending_fulltext_review
```

对扫描件：先进行 OCR，再转换。OCR 文本必须标记 `text_status: ocr`，关键结论回查原 PDF 页面。

本机状态：Docker 和 WSL 已可用；Docling、GROBID 尚未安装。首次部署只处理 3 篇代表性论文，比较章节恢复、表格恢复和页码回查，再决定是否批量处理。

## 阶段 2：Claudian 全文分析

在生成的全文 Markdown 中打开 Claudian，并使用下面的固定指令：

```text
基于当前全文 Markdown 和关联原 PDF 生成研究笔记。
不得仅依据摘要，不得补写原文未支持的结论。
输出到 20_Processing/02_Fulltext_Analysis，并包含：
1. [引用] 与页码或章节对应的关键证据；
2. 方法、数据集、实验设置、对照组、限制条件；
3. 对 TCC 的具体可迁移机制；
4. 对 iNEST 的具体可迁移机制；
5. [推导] 仅在前述证据基础上的研究假设；
6. [待测] 不超过三条验证任务，每条有 V- 编号、方法和验收标准；
7. 不修改 06_Task_Plan，只向研究任务确认队列提出候选项。
```

## 阶段 3：分批策略

不要一次处理全部 PDF。

1. 第一批：20 篇，与 CST、SNN、临界性、拓扑、NoC/Chiplet 直接相关。
2. 第二批：按第一批发现的关键词和引用网络选取 30-50 篇。
3. 其余 PDF 只建索引，按任务需要再做全文分析。

每批结束后检查：转换失败率、OCR 比例、重复率、候选任务数量和人工批准比例。失败文件进入 `20_Processing/21_Pending`，不得静默跳过。

## 阶段 4：知识图谱与检索

- Smart Connections 只索引 `01_PDF_Text` 和已确认的分析笔记，不索引重复 PDF 或临时 OCR 文件。
- 主题笔记只链接到 `02_Fulltext_Analysis` 中带 `[引用]` 的结论。
- 每条任务要回链到全文笔记、原 PDF 和证据片段。

## 质量闸门

| 验证 | 方法 | 验收标准 |
|---|---|---|
| V-PDF-01 | SHA-256 与来源核验 | 每篇全文有唯一文件指纹和来源链接 |
| V-PDF-02 | 文本提取检查 | 机器可读 PDF 有可检索正文；扫描件标注 OCR |
| V-PDF-03 | 证据回查 | 每项关键结论具备页码或章节定位 |
| V-PDF-04 | 研究价值审查 | TCC/iNEST 映射包含机制、边界与可验证任务 |
| V-PDF-05 | 任务晋升 | 未批准候选项不进入 `06_Task_Plan` |

## 当前基础

- `[实测]` 本机发现 119 个 PDF，其中 56 个位于当前 Vault。
- `[实测]` 已具备 MarkItDown、pypdf、pdfplumber 和 PDF 页面渲染工具。
- `[待测]` 首批 20 篇的转换成功率、OCR 比例和人工批准率，须在首轮执行后记录。
