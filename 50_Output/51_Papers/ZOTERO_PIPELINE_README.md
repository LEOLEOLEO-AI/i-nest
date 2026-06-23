# Zotero + Codex 全流程科研管道

## 架构总览

Zotero (存证据) ←→ Codex (跑流程) ←→ Skills (做工序)

## 已实现的工序

### 1. 参考文献提取与键映射
- 从 V29 提取 69 条参考文献
- 自动生成 citation key（firstauthorYEARkeyword）
- 生成 .bib 文件: `cst_references_v29.bib`
- 生成键映射: `ref_key_map.json`

### 2. 论文引用转换
- V29: `[1]...[69]` → V30: `[@tononi2004an]...[@ma2019criticality]`
- 输出: `A1_CST_Theory_V30_CITEKEYS.md`

### 3. 待完成（需 pandoc 安装后）

3.1 Better BibTeX 自动导出配置
- 在 Zotero 中: 工具 → Better BibTeX → Automatic Export
- 导出路径: `cst_references_v29.bib`

3.2 参考文献验证
- CrossRef API: DOI 核查
- PubMed: 生物医学引用核对
- OpenAlex: 作者/年份交叉验证

3.3 Markdown → Zotero-word 文档
- pandoc 转换: `pandoc paper.md --citeproc -o paper.docx`
- Zotero field codes 嵌入 Word

3.4 一键管道
- `pipeline.py`: 提取引用 → 验证 → 生成 .bib → 转换论文 → 导出 Word

## 使用方式

```bash
# 1. 提取引用并生成 .bib
python _gen_bib.py

# 2. 验证引用（需要网络）
python _validate_refs.py

# 3. 转换引用格式 [1] → [@key]
python _convert_citations.py

# 4. 导出 Word（需要 pandoc）
pandoc V30_CITEKEYS.md --citeproc --bibliography=cst_references_v29.bib -o V30_draft.docx
```
