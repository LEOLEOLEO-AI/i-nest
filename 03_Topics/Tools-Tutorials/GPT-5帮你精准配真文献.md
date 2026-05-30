---
title: "GPT-5帮你精准配真文献"
created: 2025-10-09
note_id: "1889769267889581520"
tags:
  - "图片笔记"
  - "GPT-5"
  - "文献检索"
  - "小魏博士讲"
  - "get-笔记"
  - "AI研究"
---

# GPT-5帮你精准配真文献

## 摘要

**English Prompt (ready-to-use)**   Act as a Research Assistant (Literature Retrieval & Citation Normalization). Do not fabricate any references. Proc

## 正文

**English Prompt (ready-to-use)**  
Act as a Research Assistant (Literature Retrieval & Citation Normalization). Do not fabricate any references. Process the text I provide as follows.  

INPUT TEXT:  
<<<BEGIN MY PARAGRAPHS  
[Paste your Chinese or English paragraphs here; multiple paragraphs allowed]  
END MY PARAGRAPHS>>>  

**Objectives**  
1. Retrieve recent (preferably 2020-present), high-impact/Top-quartile, and verifiable sources that best support each paragraph;  
2. Insert GB/T 7714—2015 numeric in-text citations (e.g., "...[1]", "...[2-4]") at appropriate locations;  
3. Produce a GB/T 7714—2015-formatted reference list;  
4. Provide a paragraph-to-evidence mapping and a concise search log for transparency.  

**Retrieval & Screening (must comply)**  
- **Databases**: PubMed/MEDLINE, Web of Science, Scopus, Crossref (use at least two for cross-check); optionally Google Scholar for backward searching  
- **Query design**: extract key concepts, add synonyms and MeSH/Emtree, use Boolean logic and phrase search; run bilingual (ZH/EN) queries when helpful;  
- **Quality thresholds** (meet ≥1):  
  - Journal in JCR Q1/Top 25%, or  
  - Systematically reviewed/meta-analysis, RCT, or authoritative guideline/consensus statement;  
- **Recency limit**: last 5 years; if foundational older studies are essential, pair them with a recent high-impact review/guideline;  
- **Exclusions**: non-full-text abstracts, predatory journals, unverifiable DOIs, or references that do not directly support the statement.  

**Output format (strictly)**  
- **In-text citations**: as needed and numbered by first appearance; insert multiple citations per paragraph when required.  
- **Reference list (GB/T 7714—2015; in order of appearance)**:  
  Output sources in their original language.  
  Journal article template:  
  [1] Author A, Author B, Author C, et al. Title[J]. Journal, Year, Volume(Issue): PageStart-PageEnd. DOI.  
  Use "et al." when ≥3 authors. English sources use "."; Chinese sources use "。".  
- **Paragraph-to-evidence mapping**:  
  [Paragraph 1] → refs [1], [3]; brief 1-2 line justification per claim.  
  [Paragraph 2] → refs [2], [4]; (if unavailable)  
- **Search log**:  
  - Databases used (with dates)  
  - Keywords/Boolean strings  
  - Filters (years, article types, quartile/IF)  
  - Hits and main inclusion/exclusion reasons (brief).  
  If recent high-quality evidence is insufficient for any paragraph, clearly state "Insufficient evidence found" and suggest alternatives (e.g., recent high-impact review/guideline or note what data/experiments would be needed.  

别忘了收藏哦  

作者提示: 内容为 AI 技术制作，虚构内容请谨慎甄别  

还在手动找文献？本期直接教你用 GPT-5 高阶指令 ...

---
*来源：Get笔记 | 类型：img_text | 入库：2026-04-29 10:46*

## Related Notes

- [[AgentEvolver vs AlphaEvolve：AI自我进化的两条核心路线对比 🧠]]
- [[AI双引擎的未来之光]]
- [[AI编码代理的质的飞跃：v3.3透明化与v3.4连续性技术解析]]
